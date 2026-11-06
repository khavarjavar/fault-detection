#!/usr/bin/env python3
"""Train a pure single-task 2D segmentation model on Thebe only.

The experiment uses the official Thebe train/validation split, a binary fault
objective, no auxiliary labels, no GeoFWI3D data, and no test access. Model
families and source provenance are recorded in each run configuration.
"""

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

# Required by cuBLAS when deterministic algorithms are enabled below.
os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")

import numpy as np
import torch
from torch.nn import functional as F

import faultseg3d_baseline as baseline
import train_r100_fp16_clean as r100
from evaluate_thebe_zero_shot_r100_pinned import ConcatenatedThebe
from pure2d_thebe_models import IMAGE_SIZE, MODELS, count_parameters, create_model


ROOT = Path(__file__).resolve().parents[1]
BINS = 2048


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def coordinates(shape: tuple[int, int, int]) -> list[tuple[int, int, int]]:
    return list(
        itertools.product(
            range(shape[0]),
            range(0, shape[1], IMAGE_SIZE),
            range(0, shape[2], IMAGE_SIZE),
        )
    )


def fixed_subset(
    shape: tuple[int, int, int], count: int, seed: int
) -> tuple[list[tuple[int, int, int]], list[tuple[int, int, int]]]:
    all_coordinates = coordinates(shape)
    if not 0 < count <= len(all_coordinates):
        raise ValueError("Invalid validation subset size")
    rng = random.Random(seed)
    indices = sorted(rng.sample(range(len(all_coordinates)), count))
    return all_coordinates, [all_coordinates[index] for index in indices]


def read_patch(reader: ConcatenatedThebe, origin: tuple[int, int, int]):
    x0, y0, z0 = origin
    y1 = min(y0 + IMAGE_SIZE, reader.shape[1])
    z1 = min(z0 + IMAGE_SIZE, reader.shape[2])
    raw = reader.read("seismic", x0, x0 + 1, y0, y1, z0, z1)[0].astype(
        np.float32, copy=False
    )
    target = reader.read("fault", x0, x0 + 1, y0, y1, z0, z1)[0].astype(
        np.uint8, copy=False
    )
    if raw.shape != target.shape or not np.isfinite(raw).all():
        raise RuntimeError(f"Invalid patch at {origin}")
    if target.min() < 0 or target.max() > 1:
        raise RuntimeError(f"Non-binary label at {origin}")
    valid = raw != 0.0
    observed = int(valid.sum())
    normalized = np.zeros_like(raw, dtype=np.float32)
    constant = False
    if observed:
        values = raw[valid]
        mean = float(values.mean(dtype=np.float64))
        std = float(values.std(dtype=np.float64))
        if std > 0 and np.isfinite(std):
            normalized[valid] = (values - mean) / std
        else:
            constant = True
    shape = raw.shape
    seismic = np.zeros((IMAGE_SIZE, IMAGE_SIZE), dtype=np.float32)
    label = np.zeros((IMAGE_SIZE, IMAGE_SIZE), dtype=np.float32)
    mask = np.zeros((IMAGE_SIZE, IMAGE_SIZE), dtype=np.bool_)
    bounds = (slice(0, shape[0]), slice(0, shape[1]))
    seismic[bounds] = normalized
    label[bounds] = target
    mask[bounds] = valid
    return (
        torch.from_numpy(seismic[None, None]),
        torch.from_numpy(label[None, None]),
        torch.from_numpy(mask[None, None]),
        shape,
        observed,
        constant,
    )


@torch.inference_mode()
def evaluate(model, reader, selected, device):
    model.eval()
    histogram = baseline.ProbabilityHistogram(BINS)
    raw_voxels = observed_voxels = 0
    started = time.time()
    for number, origin in enumerate(selected, 1):
        x, target, mask, shape, observed, _ = read_patch(reader, origin)
        raw_voxels += math.prod(shape)
        observed_voxels += observed
        if not observed:
            continue
        with torch.autocast("cuda", dtype=torch.float16):
            logits = model(x.to(device))
        probability = torch.sigmoid(logits.float())
        target = target.to(device)
        mask = mask.to(device)
        histogram.update_probabilities(probability[mask], target[mask])
        if number % 500 == 0:
            print(f"validation_patch={number}/{len(selected)}", flush=True)
    return histogram, {
        "patches_planned": len(selected),
        "raw_voxels": raw_voxels,
        "valid_voxels": observed_voxels,
        "excluded_no_data_voxels": raw_voxels - observed_voxels,
        "seconds": time.time() - started,
    }


def save_checkpoint(path, model, epoch, metrics, config):
    """Write inference/selection state only.

    This trainer has no resume path. Saving Adam/SGD buffers in both best and
    last checkpoints would roughly triple storage without improving the
    reproducibility of the completed benchmark.
    """
    temporary = path.with_suffix(path.suffix + ".part")
    torch.save(
        {
            "model": model.state_dict(),
            "epoch": epoch,
            "validation_metrics": metrics,
            "config": config,
        },
        temporary,
    )
    temporary.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", choices=sorted(MODELS), required=True)
    parser.add_argument("--run-dir", type=Path)
    parser.add_argument("--thebe-root", type=Path, default=ROOT / "data/processed/thebe_h5")
    parser.add_argument("--seed", type=int, default=43)
    parser.add_argument("--validation-seed", type=int, default=1042)
    parser.add_argument("--epochs", type=int, default=150)
    parser.add_argument("--train-patches", type=int, default=360)
    parser.add_argument("--validation-patches", type=int, default=128)
    parser.add_argument("--batch-size", type=int, default=2)
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    if args.smoke:
        args.epochs = 1
        args.train_patches = 18
        args.validation_patches = 2
    if args.train_patches % 9 or args.train_patches % args.batch_size:
        parser.error("train-patches must be divisible by 9 and batch-size")

    model = create_model(args.model)
    if args.check_only:
        example = torch.zeros(1, 1, IMAGE_SIZE, IMAGE_SIZE)
        model.eval()
        with torch.inference_mode():
            output = model(example)
        if output.shape != example.shape:
            raise RuntimeError(f"Output shape {output.shape} != {example.shape}")
        print(json.dumps({
            "status": "cpu_check_pass", "model": args.model,
            "parameters": count_parameters(model), "shape": list(output.shape),
            "model_spec": model.spec, "test_files_read": False,
        }, indent=2))
        return 0
    if args.run_dir is None:
        parser.error("--run-dir is required")
    if args.run_dir.exists():
        raise FileExistsError(args.run_dir)
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")

    baseline.seed_everything(args.seed)
    rng = random.Random(args.seed)
    train_files = r100.split_paths(args.thebe_root, "train", 9)
    val_files = r100.split_paths(args.thebe_root, "val", 2)
    train_reader = ConcatenatedThebe(train_files)
    val_reader = ConcatenatedThebe(val_files)
    device = torch.device("cuda")
    try:
        if train_reader.shape != (900, 3174, 1537):
            raise RuntimeError(f"Unexpected train shape {train_reader.shape}")
        if val_reader.shape != (200, 3174, 1537):
            raise RuntimeError(f"Unexpected validation shape {val_reader.shape}")
        all_val, val_subset = fixed_subset(
            val_reader.shape, args.validation_patches, args.validation_seed
        )
        model = model.to(device)
        if args.model == "deeplabv3":
            optimizer = torch.optim.SGD(
                model.parameters(), lr=0.01, momentum=0.9, weight_decay=1e-4
            )
            optimizer_name = "SGD(momentum=0.9, weight_decay=1e-4)"
        else:
            optimizer = torch.optim.AdamW(
                model.parameters(), lr=6e-5, weight_decay=0.01
            )
            optimizer_name = "AdamW(weight_decay=0.01)"
        total_steps = args.epochs * (args.train_patches // args.batch_size)
        scheduler = torch.optim.lr_scheduler.PolynomialLR(
            optimizer, total_iters=total_steps, power=0.9
        )
        scaler = torch.amp.GradScaler("cuda", enabled=True)
        sources = (
            ROOT / "scripts/train_pure2d_thebe.py",
            ROOT / "scripts/pure2d_thebe_models.py",
        )
        config = {
            "experiment": "pure_single_task_2d_Thebe_benchmark",
            "model": args.model,
            "model_parameters": count_parameters(model),
            "model_spec": model.spec,
            "seed": args.seed,
            "train_files": [str(path) for path in train_files],
            "validation_files": [str(path) for path in val_files],
            "train_shape": train_reader.shape,
            "validation_shape": val_reader.shape,
            "patch_size": IMAGE_SIZE,
            "epochs": args.epochs,
            "train_patches_per_epoch": args.train_patches,
            "batch_size": args.batch_size,
            "validation_subset_coordinates": val_subset,
            "full_validation_patches": len(all_val),
            "normalization": "per-2D-patch z-score over observed voxels",
            "augmentation": "independent random flips over both in-plane axes",
            "loss": "masked binary cross-entropy; single fault head only",
            "optimizer": optimizer_name,
            "schedule": "polynomial decay power 0.9 per optimizer step",
            "checkpoint_selection": "highest PR-AUC on fixed validation subset",
            "threshold_selection": (
                "smoke subset" if args.smoke else "complete Thebe validation volume"
            ),
            "initialization": "random; Thebe-only training",
            "source_hashes": {str(path.relative_to(ROOT)): sha256(path) for path in sources},
            "test_files_read": False,
            "test_policy": "test H5 files are never opened",
            "claim_scope": (
                "pure single-task Thebe run; see model_spec for official versus "
                "paper-aligned local components"
            ),
            "smoke": args.smoke,
        }
        args.run_dir.mkdir(parents=True)
        r100.write_json_atomic(args.run_dir / "run_config.json", config)
        history = []
        best_score = -1.0
        torch.cuda.reset_peak_memory_stats()
        patches_per_file = args.train_patches // len(train_files)
        for epoch in range(1, args.epochs + 1):
            epoch_started = time.time()
            model.train()
            origins = []
            for sample in range(args.train_patches):
                file_index = sample // patches_per_file
                for _ in range(30):
                    origin = (
                        train_reader.offsets[file_index]
                        + rng.randrange(train_reader.lengths[file_index]),
                        rng.randrange(train_reader.shape[1] - IMAGE_SIZE + 1),
                        rng.randrange(train_reader.shape[2] - IMAGE_SIZE + 1),
                    )
                    _, _, _, _, observed, constant = read_patch(train_reader, origin)
                    if observed >= int(0.05 * IMAGE_SIZE**2) and not constant:
                        break
                else:
                    raise RuntimeError("Could not sample an observed training patch")
                origins.append(origin)
            running_loss = 0.0
            for start in range(0, len(origins), args.batch_size):
                batch_x, batch_target, batch_mask = [], [], []
                for origin in origins[start : start + args.batch_size]:
                    x, target, mask, _, _, _ = read_patch(train_reader, origin)
                    if rng.randrange(2):
                        x, target, mask = x.flip(-2), target.flip(-2), mask.flip(-2)
                    if rng.randrange(2):
                        x, target, mask = x.flip(-1), target.flip(-1), mask.flip(-1)
                    batch_x.append(x)
                    batch_target.append(target)
                    batch_mask.append(mask)
                x = torch.cat(batch_x).to(device)
                target = torch.cat(batch_target).to(device)
                mask = torch.cat(batch_mask).to(device)
                optimizer.zero_grad(set_to_none=True)
                with torch.autocast("cuda", dtype=torch.float16):
                    logits = model(x)
                loss = F.binary_cross_entropy_with_logits(
                    logits.float()[mask], target[mask]
                )
                if not torch.isfinite(loss):
                    raise RuntimeError("Non-finite training loss")
                scaler.scale(loss).backward()
                scale_before = scaler.get_scale()
                scaler.step(optimizer)
                scaler.update()
                # GradScaler may skip an overflowing step. Advance the schedule
                # only when the corresponding optimizer update was applied.
                if scaler.get_scale() >= scale_before:
                    scheduler.step()
                running_loss += float(loss.detach()) * len(batch_x)
                completed = start + len(batch_x)
                if completed % max(args.batch_size, args.train_patches // 6) == 0:
                    print(
                        f"epoch={epoch}/{args.epochs} patch={completed}/{args.train_patches} "
                        f"loss={float(loss):.6f}", flush=True
                    )
            histogram, coverage = evaluate(model, val_reader, val_subset, device)
            metrics = asdict(histogram.metrics(0.5))
            row = {
                "epoch": epoch,
                "train_loss": running_loss / args.train_patches,
                "seconds": time.time() - epoch_started,
                **{f"val_{key}": value for key, value in metrics.items()},
            }
            history.append(row)
            baseline.write_history(args.run_dir / "history.csv", history)
            save_checkpoint(
                args.run_dir / "last.pt", model, epoch, metrics, config
            )
            if metrics["pr_auc_approx"] > best_score:
                best_score = metrics["pr_auc_approx"]
                save_checkpoint(
                    args.run_dir / "best.pt", model, epoch, metrics, config
                )
            print(
                f"epoch={epoch:03d}/{args.epochs} loss={row['train_loss']:.6f} "
                f"val_dice={metrics['dice']:.6f} val_pr_auc={metrics['pr_auc_approx']:.6f} "
                f"minutes={row['seconds']/60:.2f}", flush=True
            )

        best = torch.load(args.run_dir / "best.pt", map_location="cpu", weights_only=False)
        model.load_state_dict(best["model"], strict=True)
        final_coordinates = val_subset if args.smoke else all_val
        histogram, coverage = evaluate(model, val_reader, final_coordinates, device)
        if not args.smoke and coverage["raw_voxels"] != math.prod(val_reader.shape):
            raise RuntimeError("Incomplete full-validation coverage")
        threshold = histogram.best_dice_threshold()
        final_metrics = asdict(histogram.metrics(threshold))
        selection = {
            "best_epoch": int(best["epoch"]),
            "threshold": float(threshold),
            "threshold_source": "smoke subset" if args.smoke else "complete validation volume",
            "full_validation": final_metrics,
            "full_validation_coverage": coverage,
            "test_files_read": False,
        }
        r100.write_json_atomic(args.run_dir / "validation_selection.json", selection)
        status = {
            "status": "smoke_complete" if args.smoke else "validation_only_complete",
            "model": args.model,
            "seed": args.seed,
            "epochs_completed": len(history),
            "best_epoch": int(best["epoch"]),
            "threshold": float(threshold),
            "validation_dice": float(final_metrics["dice"]),
            "validation_pr_auc_approx": float(final_metrics["pr_auc_approx"]),
            "model_parameters": count_parameters(model),
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
