#!/usr/bin/env python3
"""Train a released Thebe 2D baseline with its model-specific native loss."""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict
import hashlib
import itertools
import json
import math
import os
import random
import time
from pathlib import Path

import numpy as np

os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")

import torch

import faultseg3d_baseline as baseline
import train_r100_fp16_clean as r100
from evaluate_thebe_zero_shot_r100_pinned import ConcatenatedThebe
from thebe_author_2d_models import (
    MODELS, PATCH_SIZE, author_loss, create_model, fused_logits,
)


ROOT = Path(__file__).resolve().parents[1]
FINAL_TILE = 256
HISTOGRAM_BINS = 2048


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_index(path: Path) -> tuple[dict, list[tuple[int, int, int]]]:
    payload = json.loads(path.read_text())
    coordinates = [
        (crossline, row, column)
        for crossline, positions in enumerate(payload["by_slice"])
        for row, column in positions
    ]
    if len(coordinates) != payload["patches"]:
        raise RuntimeError(f"Index count mismatch in {path}")
    return payload, coordinates


def read_author_slice(
    reader: ConcatenatedThebe, crossline: int, pad: dict
) -> tuple[np.ndarray, np.ndarray]:
    seismic = reader.read(
        "seismic", crossline, crossline + 1,
        0, reader.shape[1], 0, reader.shape[2]
    )[0].T.astype(np.float32, copy=False)
    target = reader.read(
        "fault", crossline, crossline + 1,
        0, reader.shape[1], 0, reader.shape[2]
    )[0].T.astype(np.float32, copy=False)
    if not np.isfinite(seismic).all() or target.min() < 0 or target.max() > 1:
        raise RuntimeError(f"Invalid Thebe crossline {crossline}")
    minimum = float(seismic.min())
    maximum = float(seismic.max())
    if maximum <= minimum:
        raise RuntimeError(f"Constant Thebe crossline {crossline}")
    seismic = (seismic - minimum) / (maximum - minimum)
    padding = ((pad["top"], pad["bottom"]), (pad["left"], pad["right"]))
    return (
        np.pad(seismic, padding, mode="reflect"),
        np.pad(target, padding, mode="reflect"),
    )


def batches(
    reader: ConcatenatedThebe,
    selected: list[tuple[int, int, int]],
    pad: dict,
    batch_size: int,
    rng: random.Random | None,
):
    grouped: dict[int, list[tuple[int, int]]] = {}
    for crossline, row, column in selected:
        grouped.setdefault(crossline, []).append((row, column))
    slice_order = list(grouped)
    if rng is not None:
        rng.shuffle(slice_order)
    images: list[np.ndarray] = []
    labels: list[np.ndarray] = []
    for crossline in slice_order:
        positions = grouped[crossline]
        if rng is not None:
            rng.shuffle(positions)
        seismic, target = read_author_slice(reader, crossline, pad)
        for row, column in positions:
            y0, x0 = row * 48, column * 48
            images.append(seismic[y0 : y0 + PATCH_SIZE, x0 : x0 + PATCH_SIZE])
            labels.append(target[y0 : y0 + PATCH_SIZE, x0 : x0 + PATCH_SIZE])
            if len(images) == batch_size:
                yield (
                    torch.from_numpy(np.stack(images)[:, None]),
                    torch.from_numpy(np.stack(labels)[:, None]),
                )
                images.clear()
                labels.clear()
    if images:
        yield (
            torch.from_numpy(np.stack(images)[:, None]),
            torch.from_numpy(np.stack(labels)[:, None]),
        )


@torch.inference_mode()
def evaluate_subset(model, name, reader, selected, pad, batch_size, device):
    model.eval()
    histogram = baseline.ProbabilityHistogram(HISTOGRAM_BINS)
    total_loss = 0.0
    total_batches = 0
    for image, target in batches(reader, selected, pad, batch_size, rng=None):
        image = image.to(device)
        target = target.to(device)
        output = model(image)
        loss = author_loss(name, output, target)
        probability = torch.sigmoid(fused_logits(output).float())
        histogram.update_probabilities(probability.flatten(), target.flatten())
        total_loss += float(loss)
        total_batches += 1
    return histogram, total_loss / total_batches


@torch.inference_mode()
def evaluate_full_volume(model, reader, batch_size, device):
    model.eval()
    histogram = baseline.ProbabilityHistogram(HISTOGRAM_BINS)
    raw_voxels = 0
    started = time.time()
    height, width = reader.shape[2], reader.shape[1]
    for crossline in range(reader.shape[0]):
        seismic = reader.read(
            "seismic", crossline, crossline + 1,
            0, reader.shape[1], 0, reader.shape[2]
        )[0].T.astype(np.float32, copy=False)
        target = reader.read(
            "fault", crossline, crossline + 1,
            0, reader.shape[1], 0, reader.shape[2]
        )[0].T.astype(np.float32, copy=False)
        minimum, maximum = float(seismic.min()), float(seismic.max())
        seismic = (seismic - minimum) / (maximum - minimum)
        padded_h = math.ceil(height / FINAL_TILE) * FINAL_TILE
        padded_w = math.ceil(width / FINAL_TILE) * FINAL_TILE
        pad = ((0, padded_h - height), (0, padded_w - width))
        seismic = np.pad(seismic, pad, mode="reflect")
        target = np.pad(target, pad, mode="constant")
        origins = list(itertools.product(
            range(0, padded_h, FINAL_TILE), range(0, padded_w, FINAL_TILE)
        ))
        for start in range(0, len(origins), batch_size):
            current = origins[start : start + batch_size]
            image_batch, target_batch, valid_batch = [], [], []
            for y0, x0 in current:
                image_batch.append(seismic[y0 : y0 + FINAL_TILE, x0 : x0 + FINAL_TILE])
                target_batch.append(target[y0 : y0 + FINAL_TILE, x0 : x0 + FINAL_TILE])
                valid = np.zeros((FINAL_TILE, FINAL_TILE), dtype=np.bool_)
                valid[: max(0, min(FINAL_TILE, height - y0)),
                      : max(0, min(FINAL_TILE, width - x0))] = True
                valid_batch.append(valid)
            image = torch.from_numpy(np.stack(image_batch)[:, None]).to(device)
            output = model(image)
            probability = torch.sigmoid(fused_logits(output).float())
            truth = torch.from_numpy(np.stack(target_batch)[:, None]).to(device)
            valid = torch.from_numpy(np.stack(valid_batch)[:, None]).to(device)
            histogram.update_probabilities(probability[valid], truth[valid])
            raw_voxels += int(valid.sum())
        if (crossline + 1) % 25 == 0:
            print(
                f"full_validation_crossline={crossline + 1}/{reader.shape[0]}",
                flush=True,
            )
    if raw_voxels != math.prod(reader.shape):
        raise RuntimeError(f"Full-validation coverage {raw_voxels} != {math.prod(reader.shape)}")
    return histogram, {"raw_voxels": raw_voxels, "seconds": time.time() - started}


def save_checkpoint(path, model, epoch, validation_loss, metrics, config):
    temporary = path.with_suffix(path.suffix + ".part")
    torch.save({
        "model": model.state_dict(),
        "epoch": epoch,
        "validation_loss": validation_loss,
        "validation_metrics": metrics,
        "config": config,
    }, temporary)
    temporary.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", choices=sorted(MODELS), required=True)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--thebe-root", type=Path, default=ROOT / "data/processed/thebe_h5")
    parser.add_argument("--index-dir", type=Path, default=ROOT / "data/processed/thebe_author_patch_index")
    parser.add_argument("--seed", type=int, default=43)
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--train-patches", type=int, default=23_040)
    parser.add_argument("--validation-patches", type=int, default=4_096)
    parser.add_argument("--early-stopping-patience", type=int, default=20)
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    if args.smoke:
        args.epochs = 1
        args.batch_size = 2
        args.train_patches = 18
        args.validation_patches = 8
    if args.run_dir.exists():
        raise FileExistsError(args.run_dir)
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")

    train_index, train_coordinates = load_index(args.index_dir / "train.json")
    val_index, val_coordinates = load_index(args.index_dir / "val.json")
    if args.train_patches > len(train_coordinates) or args.validation_patches > len(val_coordinates):
        parser.error("Requested more patches than the author index contains")
    baseline.seed_everything(args.seed)
    rng = random.Random(args.seed)
    validation_rng = random.Random(1042)
    selected_validation = validation_rng.sample(val_coordinates, args.validation_patches)
    train_reader = ConcatenatedThebe(r100.split_paths(args.thebe_root, "train", 9))
    val_reader = ConcatenatedThebe(r100.split_paths(args.thebe_root, "val", 2))
    model = create_model(args.model).cuda()
    device = torch.device("cuda")
    if args.model in {"hed", "rcf"}:
        optimizer = torch.optim.SGD(
            model.parameters(), lr=1e-6, momentum=0.9, weight_decay=2e-4
        )
        optimizer_spec = "SGD(lr=1e-6,momentum=0.9,weight_decay=0.0002)"
    else:
        optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
        optimizer_spec = "Adam(lr=0.01)"
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, mode="min", factor=0.1, patience=5
    )
    source_files = (
        ROOT / "scripts/thebe_author_2d_models.py",
        ROOT / "scripts/train_thebe_author2d.py",
        ROOT / "scripts/prepare_thebe_author_patch_index.py",
    )
    config = {
        "experiment": "Thebe_author_model_native_budgeted_adaptation",
        "model": args.model,
        "model_spec": model.spec,
        "seed": args.seed,
        "epochs_maximum": args.epochs,
        "patch_size": PATCH_SIZE,
        "patch_step_in_author_index": 48,
        "author_train_index_patches": len(train_coordinates),
        "author_validation_index_patches": len(val_coordinates),
        "train_patches_per_epoch": args.train_patches,
        "validation_selection_patches": args.validation_patches,
        "batch_size": args.batch_size,
        "normalization": "per-crossline min-max, matching Thebe author notebook",
        "augmentation": "none, matching released no-augmentation baseline",
        "loss": "model-native released Thebe loss; see source",
        "optimizer": optimizer_spec,
        "schedule": "ReduceLROnPlateau(factor=0.1,patience=5)",
        "checkpoint_selection": "minimum fixed-subset validation loss",
        "early_stopping_patience": args.early_stopping_patience,
        "final_validation": "complete 200-crossline volume, non-overlapping 256 tiles",
        "protocol_deviation": (
            "budgeted random subset of the released fault-rich index per epoch; "
            "the author notebook uses all 181029 patches and 64317 validation patches"
        ),
        "source_hashes": {str(path.relative_to(ROOT)): sha256(path) for path in source_files},
        "test_files_read": False,
        "smoke": args.smoke,
    }
    args.run_dir.mkdir(parents=True)
    r100.write_json_atomic(args.run_dir / "run_config.json", config)
    history: list[dict] = []
    best_loss = math.inf
    stale = 0
    torch.cuda.reset_peak_memory_stats()
    try:
        for epoch in range(1, args.epochs + 1):
            started = time.time()
            model.train()
            selected_train = rng.sample(train_coordinates, args.train_patches)
            loss_total = 0.0
            batch_count = 0
            patches_seen = 0
            for image, target in batches(
                train_reader, selected_train, train_index["padding"],
                args.batch_size, rng
            ):
                image, target = image.to(device), target.to(device)
                optimizer.zero_grad(set_to_none=True)
                output = model(image)
                loss = author_loss(args.model, output, target)
                if not torch.isfinite(loss):
                    raise RuntimeError("Non-finite training loss")
                loss.backward()
                optimizer.step()
                loss_total += float(loss.detach())
                batch_count += 1
                patches_seen += len(image)
                if patches_seen % max(args.batch_size, args.train_patches // 6) < args.batch_size:
                    print(
                        f"epoch={epoch}/{args.epochs} patches={patches_seen}/{args.train_patches} "
                        f"loss={float(loss):.6f}", flush=True
                    )
            histogram, validation_loss = evaluate_subset(
                model, args.model, val_reader, selected_validation,
                val_index["padding"], args.batch_size, device
            )
            metrics = asdict(histogram.metrics(0.5))
            row = {
                "epoch": epoch,
                "train_loss_per_batch": loss_total / batch_count,
                "validation_loss_per_batch": validation_loss,
                "validation_dice_at_0.5": metrics["dice"],
                "validation_pr_auc_approx": metrics["pr_auc_approx"],
                "seconds": time.time() - started,
                "learning_rate": optimizer.param_groups[0]["lr"],
            }
            history.append(row)
            baseline.write_history(args.run_dir / "history.csv", history)
            save_checkpoint(
                args.run_dir / "last.pt", model, epoch,
                validation_loss, metrics, config
            )
            improved = validation_loss < best_loss
            if improved:
                best_loss = validation_loss
                stale = 0
                save_checkpoint(
                    args.run_dir / "best.pt", model, epoch,
                    validation_loss, metrics, config
                )
            else:
                stale += 1
            scheduler.step(validation_loss)
            print(
                f"epoch={epoch:03d} train_loss={row['train_loss_per_batch']:.6f} "
                f"val_loss={validation_loss:.6f} val_pr_auc={metrics['pr_auc_approx']:.6f} "
                f"minutes={row['seconds']/60:.2f} stale={stale}", flush=True
            )
            if stale >= args.early_stopping_patience:
                print("early_stopping", flush=True)
                break
        best = torch.load(args.run_dir / "best.pt", map_location="cpu", weights_only=False)
        model.load_state_dict(best["model"], strict=True)
        if args.smoke:
            histogram, validation_loss = evaluate_subset(
                model, args.model, val_reader, selected_validation,
                val_index["padding"], args.batch_size, device
            )
            coverage = {"mode": "smoke subset", "patches": len(selected_validation)}
        else:
            histogram, coverage = evaluate_full_volume(
                model, val_reader, args.batch_size, device
            )
        threshold = histogram.best_dice_threshold()
        final_metrics = asdict(histogram.metrics(threshold))
        selection = {
            "best_epoch": int(best["epoch"]),
            "best_subset_validation_loss": float(best["validation_loss"]),
            "threshold": float(threshold),
            "full_validation": final_metrics,
            "coverage": coverage,
            "test_files_read": False,
        }
        r100.write_json_atomic(args.run_dir / "validation_selection.json", selection)
        status = {
            "status": "smoke_complete" if args.smoke else "validation_only_complete",
            "model": args.model,
            "epochs_completed": len(history),
            "best_epoch": int(best["epoch"]),
            "validation_dice": float(final_metrics["dice"]),
            "validation_pr_auc_approx": float(final_metrics["pr_auc_approx"]),
            "peak_gpu_allocated_gib": torch.cuda.max_memory_allocated() / 1024**3,
            "peak_gpu_reserved_gib": torch.cuda.max_memory_reserved() / 1024**3,
            "test_files_read": False,
        }
        r100.write_json_atomic(args.run_dir / "status.json", status)
        print(json.dumps(status, indent=2), flush=True)
    finally:
        train_reader.close()
        val_reader.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
