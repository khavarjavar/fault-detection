#!/usr/bin/env python3
"""R100: FaultSeg3D from scratch on real Thebe, then held-out evaluation.

Install alongside faultseg3d_baseline.py and evaluate_thebe_zero_shot.py in
the project's scripts directory. Run from the project roo  with .venv_train.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import math
import random
import time
from dataclasses import asdict
from pathlib import Path

import h5py
import numpy as np
import torch
from torch.nn import functional as F

import faultseg3d_baseline as baseline
from evaluate_thebe_zero_shot import (
    ConcatenatedThebe,
    natural_key,
    summarize_rows,
    write_csv_atomic,
)

SIZE = 128
BINS = 2048
SEED = 42
EPOCHS = 100
STEPS_PER_EPOCH = 360
GRAD_ACCUMULATION = 2
LR = 1e-4
VAL_PATCHES_PER_EPOCH = 128
SOURCE_HASHES = {
    "scripts/faultseg3d_baseline.py":
        "0089293db07637f7042ed340f47d6ed33957d1f34414b96a5698b1b1ce3e3131",
    "scripts/evaluate_thebe_zero_shot.py":
        "834ec8aeb8a726c51f6dd65e4f85fac7652dfcc13f8ab58f0784fe359b9374ec",
}


def fail_if_changed() -> None:
    for name, expected in SOURCE_HASHES.items():
        path = Path(name)
        if not path.is_file():
            raise RuntimeError(f"Missing source file: {path}")
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            raise RuntimeError(
                f"{path} changed since inspection. Expected {expected}, got {actual}. "
                "No training has started."
            )
    if tuple(baseline.VOLUME_SHAPE) != (SIZE,) * 3:
        raise RuntimeError("Baseline A patch size changed")


def split_paths(root: Path, split: str, count: int) -> list[Path]:
    paths = sorted(root.glob(f"{split}*.h5"), key=natural_key)
    expected = [root / f"{split}{number}.h5" for number in range(1, count + 1)]
    if paths != expected:
        raise RuntimeError(f"Expected exactly {expected}; found {paths}")
    if not all(path.is_file() for path in paths):
        raise RuntimeError(f"Missing H5 file in {paths}")
    return paths


def tiling(shape: tuple[int, int, int]) -> list[tuple[int, int, int]]:
    return list(itertools.product(*(range(0, length, SIZE) for length in shape)))


def read_patch(reader: ConcatenatedThebe, origin: tuple[int, int, int]):
    stops = tuple(min(start + SIZE, length) for start, length in zip(origin, reader.shape))
    x0, y0, z0 = origin
    x1, y1, z1 = stops
    raw = reader.read("seismic", x0, x1, y0, y1, z0, z1).astype(np.float32, copy=False)
    target = reader.read("fault", x0, x1, y0, y1, z0, z1).astype(np.uint8, copy=False)
    actual_shape = tuple(stop - start for start, stop in zip(origin, stops))
    if raw.shape != actual_shape or target.shape != actual_shape:
        raise RuntimeError(f"Patch shape mismatch at {origin}")
    if not np.isfinite(raw).all():
        raise RuntimeError(f"Nonfinite seismic at {origin}")
    if target.min() < 0 or target.max() > 1:
        raise RuntimeError(f"Nonbinary label at {origin}")
    valid = raw != 0.0
    observed = int(np.count_nonzero(valid))
    excluded_positive = int(np.count_nonzero((target > 0) & ~valid))
    seismic_padded = np.zeros((SIZE,) * 3, dtype=np.float32)
    target_padded = np.zeros((SIZE,) * 3, dtype=np.float32)
    mask_padded = np.zeros((SIZE,) * 3, dtype=np.bool_)
    slices = tuple(slice(0, length) for length in actual_shape)
    if observed:
        values = raw[valid]
        mean = float(values.mean(dtype=np.float64))
        std = float(values.std(dtype=np.float64))
        if not np.isfinite(std) or std <= 0:
            raise RuntimeError(f"Constant observed seismic at {origin}")
        normalized = np.zeros_like(raw, dtype=np.float32)
        normalized[valid] = (raw[valid] - mean) / std
        seismic_padded[slices] = normalized
    target_padded[slices] = target
    mask_padded[slices] = valid
    # Identical axis reversal and valid-only z-score to A->T0 evaluation.
    def tensor(array: np.ndarray):
        return torch.from_numpy(np.ascontiguousarray(np.transpose(array))[None, None])
    return (
        tensor(seismic_padded), tensor(target_padded), tensor(mask_padded),
        actual_shape, observed, excluded_positive,
    )


@torch.inference_mode()
def evaluate(
    model: torch.nn.Module,
    reader: ConcatenatedThebe,
    coords: list[tuple[int, int, int]],
    device: torch.device,
    threshold: float = 0.5,
    structural: bool = False,
):
    model.eval()
    histogram = baseline.ProbabilityHistogram(BINS)
    rows = []
    raw_voxels = observed_voxels = excluded_positive = 0
    total_inference_seconds = 0.0
    for number, origin in enumerate(coords, 1):
        x, target, mask, shape, observed, ignored_pos = read_patch(reader, origin)
        raw_voxels += math.prod(shape)
        observed_voxels += observed
        excluded_positive += ignored_pos
        if not observed:
            continue
        x = x.to(device)
        target = target.to(device)
        mask = mask.to(device)
        torch.cuda.synchronize()
        started = time.perf_counter()
        with torch.autocast(device_type="cuda", dtype=torch.float16):
            logits = model(x)
        probability = torch.sigmoid(logits.float())
        torch.cuda.synchronize()
        seconds = time.perf_counter() - started
        total_inference_seconds += seconds
        probability_scored = probability[mask]
        target_scored = target[mask]
        histogram.update_probabilities(probability_scored, target_scored)
        if structural:
            patch_histogram = baseline.ProbabilityHistogram(BINS)
            patch_histogram.update_probabilities(probability_scored, target_scored)
            zsize, ysize, xsize = shape[2], shape[1], shape[0]
            bounds = (slice(0, zsize), slice(0, ysize), slice(0, xsize))
            predicted = (probability[0, 0][bounds] >= threshold).cpu().numpy()
            truth = (target[0, 0][bounds] >= 0.5).cpu().numpy()
            valid = mask[0, 0][bounds].cpu().numpy()
            predicted &= valid
            truth &= valid
            row = {
                "patch_id": "x%04d_y%04d_z%04d" % origin,
                "raw_voxels": math.prod(shape),
                "valid_voxels": observed,
                "excluded_positive": ignored_pos,
                "inference_seconds": seconds,
                **asdict(patch_histogram.metrics(threshold)),
                **baseline.structural_distances(predicted, truth),
            }
            rows.append(row)
        if number % 100 == 0:
            print(f"evaluation_patches={number}/{len(coords)}", flush=True)
    return histogram, rows, {
        "patches_planned": len(coords),
        "patches_scored": (
            len(rows) if structural else None
        ),
        "raw_voxels": raw_voxels,
        "valid_voxels": observed_voxels,
        "excluded_no_data_voxels": raw_voxels - observed_voxels,
        "positive_labels_excluded": excluded_positive,
        "inference_seconds": total_inference_seconds,
    }


def save_checkpoint(path: Path, model, optimizer, epoch: int, validation: dict) -> None:
    temporary = path.with_suffix(".pt.part")
    torch.save({
        "model": model.state_dict(), "optimizer": optimizer.state_dict(),
        "epoch": epoch, "validation_metrics": validation,
        "args": {
            "experiment": "R100", "data_root": "data/processed/thebe_h5",
            "loss": "b0_bce_masked", "epochs": EPOCHS,
            "batch_size": 1, "gradient_accumulation": GRAD_ACCUMULATION,
            "learning_rate": LR, "seed": SEED, "histogram_bins": BINS,
            "train_patches_per_epoch": STEPS_PER_EPOCH,
            "checkpoint_selection": "fixed 128 validation patches at threshold 0.5",
        },
    }, temporary)
    temporary.replace(path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--thebe-root", type=Path, default=Path("data/processed/thebe_h5"))
    parser.add_argument("--run-dir", type=Path, required=True)
    args = parser.parse_args()
    fail_if_changed()
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA GPU required for the full R100 run")
    free_gpu, _ = torch.cuda.mem_get_info()
    if free_gpu < 8 * 1024**3:
        raise RuntimeError(f"Insufficient free GPU memory: {free_gpu / 1024**3:.1f} GiB")
    train_files = split_paths(args.thebe_root, "train", 9)
    val_files = split_paths(args.thebe_root, "val", 2)
    test_files = split_paths(args.thebe_root, "test", 7)
    if len({path.resolve() for path in train_files + val_files + test_files}) != 18:
        raise RuntimeError("Train/validation/test files overlap")
    if args.run_dir.exists():
        raise RuntimeError(f"Run directory already exists: {args.run_dir}")
    train_reader = ConcatenatedThebe(train_files)
    val_reader = ConcatenatedThebe(val_files)
    try:
        if train_reader.shape != (900, 3174, 1537) or val_reader.shape != (200, 3174, 1537):
            raise RuntimeError(f"Unexpected Thebe shapes: {train_reader.shape}, {val_reader.shape}")
        baseline.seed_everything(SEED)
        rng = random.Random(SEED)
        device = torch.device("cuda")
        model = baseline.FaultSeg3D().to(device)  # fresh initialization
        parameters = baseline.count_parameters(model)
        if parameters != baseline.EXPECTED_PARAMETERS:
            raise RuntimeError(f"Unexpected model parameter count: {parameters}")
        optimizer = torch.optim.Adam(model.parameters(), lr=LR)
        scaler = torch.cuda.amp.GradScaler(enabled=True)
        all_val = tiling(val_reader.shape)
        selector = random.Random(SEED + 1000)
        val_subset = [all_val[i] for i in sorted(selector.sample(range(len(all_val)), VAL_PATCHES_PER_EPOCH))]

        args.run_dir.mkdir(parents=True)
        config = {
            "experiment": "R100_real_Thebe_from_scratch", "seed": SEED,
            "train_files": [str(p) for p in train_files],
            "validation_files": [str(p) for p in val_files],
            "held_out_test_files": [str(p) for p in test_files],
            "train_shape": train_reader.shape, "validation_shape": val_reader.shape,
            "epochs": EPOCHS, "train_patches_per_epoch": STEPS_PER_EPOCH,
            "patch_size": SIZE, "validation_patches_per_epoch": len(val_subset),
            "full_validation_patches": len(all_val),
            "train_sampling": "40 observed random patches per train file each epoch; random axis-0 flip",
            "validity": "finite raw seismic != 0; masked BCE and masked metrics",
            "normalization": "per-patch z-score over observed voxels; axis reversal",
            "model_parameters": parameters, "optimizer": "Adam", "learning_rate": LR,
            "loss": "ordinary BCE averaged over observed voxels", "gradient_accumulation": GRAD_ACCUMULATION,
            "checkpoint_selection": "highest Dice at 0.5 on fixed validation subset",
            "threshold_selection": "best Dice on complete validation volume with 2048 bins",
            "test_policy": "one complete test evaluation after checkpoint and threshold selection",
        }
        (args.run_dir / "run_config.json").write_text(json.dumps(config, indent=2) + "\n")
        print("PREFLIGHT PASS: fresh FaultSeg3D; 9 train, 2 validation, 7 held-out test files", flush=True)
        print(f"train_shape={train_reader.shape} val_shape={val_reader.shape} parameters={parameters}", flush=True)
        best_dice = -1.0
        history = []
        for epoch in range(1, EPOCHS + 1):
            started = time.time()
            model.train()
            optimizer.zero_grad(set_to_none=True)
            running_loss = 0.0
            skipped_candidates = 0
            excluded_training_labels = 0
            for step in range(1, STEPS_PER_EPOCH + 1):
                file_index = ((step - 1) // (STEPS_PER_EPOCH // len(train_files)))
                for attempt in range(30):
                    x0 = train_reader.offsets[file_index] + rng.randrange(train_reader.lengths[file_index])
                    y0 = rng.randrange(train_reader.shape[1] - SIZE + 1)
                    z0 = rng.randrange(train_reader.shape[2] - SIZE + 1)
                    x, target, mask, _, observed, ignored_pos = read_patch(
                        train_reader, (x0, y0, z0)
                    )
                    if observed >= int(0.05 * SIZE**3):
                        break
                    skipped_candidates += 1
                else:
                    raise RuntimeError(f"Unable to sample observed training data from {train_files[file_index]}")
                excluded_training_labels += ignored_pos
                if rng.randrange(2):
                    x, target, mask = x.flip(-3), target.flip(-3), mask.flip(-3)
                x, target, mask = x.to(device), target.to(device), mask.to(device)
                with torch.autocast(device_type="cuda", dtype=torch.float16):
                    logits = model(x)
                voxel_loss = F.binary_cross_entropy_with_logits(
                    logits.float(), target, reduction="none"
                )
                full_loss = voxel_loss[mask].mean()
                scaler.scale(full_loss / GRAD_ACCUMULATION).backward()
                running_loss += float(full_loss.detach())
                if step % GRAD_ACCUMULATION == 0:
                    scaler.step(optimizer)
                    scaler.update()
                    optimizer.zero_grad(set_to_none=True)

            val_histogram, _, val_coverage = evaluate(model, val_reader, val_subset, device)
            val_metrics = asdict(val_histogram.metrics(0.5))
            if val_coverage["valid_voxels"] == 0:
                raise RuntimeError("No observed voxels in validation subset")
            row = {
                "epoch": epoch, "train_loss": running_loss / STEPS_PER_EPOCH,
                "train_patches": STEPS_PER_EPOCH, "resampled_no_data_candidates": skipped_candidates,
                "excluded_training_positive_labels": excluded_training_labels,
                "seconds": time.time() - started,
                **{f"val_{key}": value for key, value in val_metrics.items()},
            }
            history.append(row)
            baseline.write_history(args.run_dir / "history.csv", history)
            save_checkpoint(args.run_dir / "last.pt", model, optimizer, epoch, val_metrics)
            if val_metrics["dice"] > best_dice:
                best_dice = val_metrics["dice"]
                save_checkpoint(args.run_dir / "best.pt", model, optimizer, epoch, val_metrics)
            print(
                f"epoch={epoch:03d}/{EPOCHS} loss={row['train_loss']:.6f} "
                f"val_dice={val_metrics['dice']:.6f} val_pr_auc={val_metrics['pr_auc_approx']:.6f} "
                f"minutes={row['seconds']/60:.2f}", flush=True,
            )

        best = torch.load(args.run_dir / "best.pt", map_location="cpu", weights_only=False)
        model.load_state_dict(best["model"], strict=True)
        print(f"BEST EPOCH: {best['epoch']}; full validation begins", flush=True)
        full_val_hist, _, full_val_coverage = evaluate(model, val_reader, all_val, device)
        if full_val_coverage["raw_voxels"] != math.prod(val_reader.shape):
            raise RuntimeError("Incomplete validation coverage")
        threshold = full_val_hist.best_dice_threshold()
        full_val_metrics = asdict(full_val_hist.metrics(threshold))
        selection = {
            "best_epoch": best["epoch"], "threshold": threshold,
            "threshold_source": "complete val1.h5 + val2.h5 only",
            "full_validation": full_val_metrics,
            "full_validation_coverage": full_val_coverage,
        }
        (args.run_dir / "validation_selection.json").write_text(json.dumps(selection, indent=2) + "\n")
        print(f"FROZEN THRESHOLD: {threshold:.6f}; complete held-out test begins", flush=True)
    finally:
        train_reader.close()
        val_reader.close()

    # Test files and labels are opened only after training and validation selection.
    test_reader = ConcatenatedThebe(test_files)
    try:
        if test_reader.shape != (703, 3174, 1537):
            raise RuntimeError(f"Unexpected test shape: {test_reader.shape}")
        test_coords = tiling(test_reader.shape)
        test_histogram, rows, test_coverage = evaluate(
            model, test_reader, test_coords, device, threshold=threshold, structural=True,
        )
        if test_coverage["raw_voxels"] != math.prod(test_reader.shape):
            raise RuntimeError("Incomplete test coverage")
        if test_coverage["valid_voxels"] == 0:
            raise RuntimeError("No observed voxels scored in test")
        test_metrics = asdict(test_histogram.metrics(threshold))
        write_csv_atomic(args.run_dir / "test_per_patch.csv", rows)
        result = {
            "experiment": "R100_real_Thebe_from_scratch", "status": "complete_official_test",
            "training_performed": True, "real_training_files": 9, "validation_files": 2,
            "test_files": [str(path) for path in test_files],
            "best_epoch": best["epoch"], "threshold": threshold,
            "threshold_source": "complete Thebe validation only",
            "full_validation": full_val_metrics,
            "full_validation_coverage": full_val_coverage,
            "official_thebe_test": test_metrics,
            "official_thebe_test_per_patch_summary": summarize_rows(rows),
            "data": {
                **test_coverage, "test_shape": test_reader.shape,
                "expected_full_test_voxels": math.prod(test_reader.shape),
                "complete_coverage": True,
            },
            "metric_notes": {
                "validity": "finite nonzero raw Thebe voxels",
                "test_threshold_policy": "selected on complete validation and frozen",
                "train_sampling": "360 randomly sampled observed patches per epoch from all 9 real train files",
            },
        }
        temporary = args.run_dir / "final_metrics.json.part"
        temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        temporary.replace(args.run_dir / "final_metrics.json")
        print("R100 COMPLETE", flush=True)
        for key in ("dice", "iou", "precision", "recall", "mcc", "pr_auc_approx"):
            print(f"{key}={test_metrics[key]:.6f}", flush=True)
        print(f"results={args.run_dir / 'final_metrics.json'}", flush=True)
    finally:
        test_reader.close()


if __name__ == "__main__":
    main()
