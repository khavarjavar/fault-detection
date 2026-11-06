#!/usr/bin/env python3
"""R100 FP16 clean-seed training and validation; test files are never opened.

Derived from the R100 trainer supplied on 2026-10-14. It retains the model,
masked BCE, sampler, normalization, patch size, optimizer and training budget.
The changes are explicit seed control, a common validation subset,
numerical checks, and training/validation-only completion.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import math
import os
import sys
import random
import time
from dataclasses import asdict
from pathlib import Path

import h5py
import numpy as np
import torch
from torch.nn import functional as F

import faultseg3d_baseline as baseline
from evaluate_thebe_zero_shot_r100_pinned import (
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
    "scripts/evaluate_thebe_zero_shot_r100_pinned.py":
        "834ec8aeb8a726c51f6dd65e4f85fac7652dfcc13f8ab58f0784fe359b9374ec",
}


PROTOCOL_HASH = ""
ORIGINAL_R100_TRAINER_SHA256 = "0b39cffa31d275d48544a232466e56b4dedd206b1bc5d8975337ab6337f699f4"


def assert_finite_tree(value, path="state"):
    if torch.is_tensor(value):
        if value.is_floating_point() or value.is_complex():
            for chunk in value.detach().reshape(-1).split(1_048_576):
                if not torch.isfinite(chunk).all().item():
                    raise RuntimeError(f"Nonfinite tensor: {path}")
    elif isinstance(value, dict):
        for name, item in value.items():
            assert_finite_tree(item, f"{path}.{name}")
    elif isinstance(value, (list, tuple)):
        for index, item in enumerate(value):
            assert_finite_tree(item, f"{path}[{index}]")
    elif isinstance(value, (float, np.floating)) and not math.isfinite(value):
        raise RuntimeError(f"Nonfinite number: {path}")


def fixed_validation_subset(shape, count, validation_seed):
    coords = tiling(shape)
    if not 0 < count <= len(coords):
        raise ValueError("Invalid validation patch count")
    selector = random.Random(validation_seed)
    return coords, [coords[i] for i in sorted(selector.sample(range(len(coords)), count))]


def write_json_atomic(path, value):
    temporary = path.with_suffix(path.suffix + ".part")
    temporary.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")
    temporary.replace(path)


def cpu_preflight(root):
    train_files = split_paths(root, "train", 9)
    val_files = split_paths(root, "val", 2)
    if len({p.resolve() for p in train_files + val_files}) != 11:
        raise RuntimeError("Training/validation files overlap")
    train_reader = ConcatenatedThebe(train_files)
    val_reader = ConcatenatedThebe(val_files)
    try:
        if train_reader.shape != (900, 3174, 1537) or val_reader.shape != (200, 3174, 1537):
            raise RuntimeError(f"Unexpected shapes: {train_reader.shape}, {val_reader.shape}")
        model = baseline.FaultSeg3D()
        count = baseline.count_parameters(model)
        if count != 1459585 or count != baseline.EXPECTED_PARAMETERS:
            raise RuntimeError(f"Unexpected parameter count: {count}")
        coords, subset = fixed_validation_subset(val_reader.shape, 128, 1042)
        print(json.dumps({
            "status": "cpu_preflight_pass", "model": "faultseg3d_baseline.FaultSeg3D",
            "parameters": count, "train_files": len(train_files), "validation_files": len(val_files),
            "train_shape": train_reader.shape, "validation_shape": val_reader.shape,
            "validation_patches": len(subset), "full_validation_patches": len(coords),
            "test_files_opened": False,
            "note": "Source hashes, CPU construction and reader shapes checked; GPU execution not tested."
        }, indent=2), flush=True)
    finally:
        train_reader.close()
        val_reader.close()


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
    constant_observed = False
    if observed:
        values = raw[valid]
        mean = float(values.mean(dtype=np.float64))
        std = float(values.std(dtype=np.float64))
        if not np.isfinite(std):
            raise RuntimeError(f"Nonfinite seismic scale at {origin}")
        normalized = np.zeros_like(raw, dtype=np.float32)
        if std <= 0:
            # Keep the original validity mask for evaluation, but never
            # divide by zero. Training rejects this candidate below.
            constant_observed = True
        else:
            normalized[valid] = (raw[valid] - mean) / std
        seismic_padded[slices] = normalized
    target_padded[slices] = target
    mask_padded[slices] = valid
    # Identical axis reversal and valid-only z-score to A->T0 evaluation.
    def tensor(array: np.ndarray):
        return torch.from_numpy(np.ascontiguousarray(np.transpose(array))[None, None])
    return (
        tensor(seismic_padded), tensor(target_padded), tensor(mask_padded),
        actual_shape, observed, excluded_positive, constant_observed,
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
        x, target, mask, shape, observed, ignored_pos, _ = read_patch(reader, origin)
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
        assert_finite_tree(probability, "validation_probability")
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


def save_checkpoint(path: Path, model, optimizer, scaler, rng, epoch: int, validation: dict) -> None:
    assert_finite_tree(model.state_dict(), "checkpoint.model")
    assert_finite_tree(optimizer.state_dict(), "checkpoint.optimizer")
    assert_finite_tree(validation, "checkpoint.validation")
    temporary = path.with_suffix(".pt.part")
    torch.save({
        "model": model.state_dict(), "optimizer": optimizer.state_dict(),
        "epoch": epoch, "validation_metrics": validation,
        "scaler": scaler.state_dict(), "python_rng": rng.getstate(),
        "torch_rng": torch.get_rng_state(),
        "cuda_rng": torch.cuda.get_rng_state_all(),
        "args": {
            "experiment": "R100_fp16_clean", "data_root": "data/processed/thebe_h5",
            "precision": "float16_autocast", "gradient_scaling": True,
            "protocol_hash": PROTOCOL_HASH,
            "loss": "b0_bce_masked", "epochs": EPOCHS,
            "batch_size": 1, "gradient_accumulation": GRAD_ACCUMULATION,
            "learning_rate": LR, "seed": SEED, "histogram_bins": BINS,
            "train_patches_per_epoch": STEPS_PER_EPOCH,
            "checkpoint_selection": "highest PR-AUC on the common fixed validation subset",
        },
    }, temporary)
    temporary.replace(path)


def main() -> None:
    global SEED, EPOCHS, STEPS_PER_EPOCH, VAL_PATCHES_PER_EPOCH, PROTOCOL_HASH
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--thebe-root", type=Path, default=Path("data/processed/thebe_h5"))
    parser.add_argument("--run-dir", type=Path)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--validation-seed", type=int, default=1042)
    parser.add_argument("--expected-protocol", help="Refuse a changed recipe/data snapshot before training")
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--train-patches", type=int, default=360)
    parser.add_argument("--validation-patches", type=int, default=128)
    parser.add_argument("--check-only", action="store_true", help="CPU source/model/reader preflight; no training")
    parser.add_argument("--smoke", action="store_true", help="One epoch: 18 training and two validation patches; not a research result")
    parser.add_argument("--resume", action="store_true", help="Continue from this run's last.pt")
    args = parser.parse_args()
    SEED = args.seed
    EPOCHS = 1 if args.smoke else args.epochs
    STEPS_PER_EPOCH = 18 if args.smoke else args.train_patches
    VAL_PATCHES_PER_EPOCH = 2 if args.smoke else args.validation_patches
    if EPOCHS <= 0 or STEPS_PER_EPOCH <= 0 or STEPS_PER_EPOCH % 18:
        parser.error("Epochs must be positive; training patch count must be a positive multiple of 18")
    if not args.check_only and args.run_dir is None:
        parser.error("--run-dir is required for GPU execution")
    fail_if_changed()
    if args.check_only:
        cpu_preflight(args.thebe_root)
        return
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA GPU required for the full R100 run")
    torch.cuda.reset_peak_memory_stats()
    free_gpu, _ = torch.cuda.mem_get_info()
    if free_gpu < 8 * 1024**3:
        raise RuntimeError(f"Insufficient free GPU memory: {free_gpu / 1024**3:.1f} GiB")
    train_files = split_paths(args.thebe_root, "train", 9)
    val_files = split_paths(args.thebe_root, "val", 2)
    if len({path.resolve() for path in train_files + val_files}) != 11:
        raise RuntimeError("Train/validation files overlap")
    if args.resume:
        if not args.run_dir.is_dir():
            raise RuntimeError(f"Resume directory does not exist: {args.run_dir}")
    elif args.run_dir.exists():
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
        scaler = torch.amp.GradScaler("cuda", enabled=True)
        all_val, val_subset = fixed_validation_subset(
            val_reader.shape, VAL_PATCHES_PER_EPOCH, args.validation_seed
        )

        config = {
            "experiment": "R100_fp16_clean_Thebe_from_scratch", "seed": SEED,
            "model_class": "faultseg3d_baseline.FaultSeg3D",
            "precision": "float16_autocast", "gradient_scaling": True,
            "smoke": args.smoke, "validation_seed": args.validation_seed,
            "validation_subset_coordinates": val_subset,
            "source_hashes": SOURCE_HASHES,
            "original_trainer_sha256": ORIGINAL_R100_TRAINER_SHA256,
            "trainer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "torch_version": str(torch.__version__), "torch_cuda_build": torch.version.cuda,
            "gpu_name": torch.cuda.get_device_name(),
            "train_files": [str(p) for p in train_files],
            "validation_files": [str(p) for p in val_files],
            "data_file_metadata": {
                str(p): {"bytes": p.stat().st_size, "mtime_ns": p.stat().st_mtime_ns}
                for p in train_files + val_files
            },
            "test_files_read": False,
            "train_shape": train_reader.shape, "validation_shape": val_reader.shape,
            "epochs": EPOCHS, "train_patches_per_epoch": STEPS_PER_EPOCH,
            "patch_size": SIZE, "validation_patches_per_epoch": len(val_subset),
            "full_validation_patches": len(all_val),
            "train_sampling": f"{STEPS_PER_EPOCH // len(train_files)} observed random patches per train file each epoch; random axis-0 flip",
            "validity": "finite raw seismic != 0; masked BCE and masked metrics",
            "normalization": "per-patch z-score over observed voxels; axis reversal",
            "model_parameters": parameters, "optimizer": "Adam", "learning_rate": LR,
            "loss": "ordinary BCE averaged over observed voxels", "gradient_accumulation": GRAD_ACCUMULATION,
            "checkpoint_selection": "highest PR-AUC on fixed validation subset",
            "threshold_selection": "best Dice on smoke validation subset" if args.smoke else "best Dice on complete validation volume with 2048 bins",
            "test_policy": "training and validation only; test files are never opened",
        }
        protocol = {key: value for key, value in config.items() if key != "seed"}
        PROTOCOL_HASH = hashlib.sha256(json.dumps(protocol, sort_keys=True).encode()).hexdigest()
        config["protocol_hash"] = PROTOCOL_HASH
        if args.expected_protocol is not None and PROTOCOL_HASH != args.expected_protocol:
            raise RuntimeError("Recipe/data snapshot differs from the first seed; no training has started")
        if args.resume:
            saved_config = json.loads((args.run_dir / "run_config.json").read_text())
            if saved_config != json.loads(json.dumps(config)):
                raise RuntimeError("Saved configuration differs; refusing incompatible resume")
            checkpoint_path = args.run_dir / "last.pt"
            best_path = args.run_dir / "best.pt"
            history_path = args.run_dir / "history.csv"
            if not all(path.is_file() for path in (checkpoint_path, best_path, history_path)):
                raise RuntimeError("Resume needs last.pt, best.pt, and history.csv")
            with history_path.open(newline="") as file:
                history = list(csv.DictReader(file))
            last = torch.load(checkpoint_path, map_location="cpu", weights_only=False)
            best_saved = torch.load(best_path, map_location="cpu", weights_only=False)
            completed = int(last["epoch"])
            if not history or int(history[-1]["epoch"]) != completed:
                raise RuntimeError("Checkpoint epoch and history.csv disagree; inspect before resuming")
            if completed > EPOCHS:
                raise RuntimeError(f"Checkpoint epoch {completed} exceeds requested budget {EPOCHS}")
            model.load_state_dict(last["model"], strict=True)
            optimizer.load_state_dict(last["optimizer"])
            best_score = float(best_saved["validation_metrics"]["pr_auc_approx"])
            previous_pr_auc_best = max(
                history, key=lambda row: float(row["val_pr_auc_approx"])
            )
            if int(previous_pr_auc_best["epoch"]) != int(best_saved["epoch"]):
                raise RuntimeError(
                    "Best saved checkpoint is not the PR-AUC best from prior epochs; "
                    "cannot change selection policy safely without that checkpoint"
                )
            write_json_atomic(args.run_dir / "resume_protocol.json", {
                "resumed_at_epoch": completed, "selection_policy_unchanged": True,
                "test_files_read": False,
            })
            if not all(key in last for key in ("scaler", "python_rng", "torch_rng", "cuda_rng")):
                raise RuntimeError("This clean-seed checkpoint lacks complete RNG state")
            assert_finite_tree(last, "resume_checkpoint")
            assert_finite_tree(best_saved, "resume_best")
            scaler.load_state_dict(last["scaler"])
            rng.setstate(last["python_rng"])
            torch.set_rng_state(last["torch_rng"])
            torch.cuda.set_rng_state_all(last["cuda_rng"])
            first_epoch = completed + 1
            print(f"RESUME PASS: completed epoch {completed}; continuing from epoch {first_epoch}", flush=True)
        else:
            args.run_dir.mkdir(parents=True)
            (args.run_dir / "run_config.json").write_text(json.dumps(config, indent=2) + "\n")
            best_score = -1.0
            history = []
            first_epoch = 1
            print("PREFLIGHT PASS: fresh FaultSeg3D; 9 train, 2 validation; test disabled", flush=True)
        print(f"train_shape={train_reader.shape} val_shape={val_reader.shape} parameters={parameters}", flush=True)
        for epoch in range(first_epoch, EPOCHS + 1):
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
                    x, target, mask, _, observed, ignored_pos, constant_observed = read_patch(
                        train_reader, (x0, y0, z0)
                    )
                    if not constant_observed and observed >= int(0.05 * SIZE**3):
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
                assert_finite_tree(full_loss, "training_loss")
                scaler.scale(full_loss / GRAD_ACCUMULATION).backward()
                running_loss += float(full_loss.detach())
                if step % GRAD_ACCUMULATION == 0:
                    # GradScaler detects overflow, skips that update, and lowers
                    # its scale before later optimizer updates.
                    scaler.step(optimizer)
                    scaler.update()
                    optimizer.zero_grad(set_to_none=True)
                if step % 60 == 0 or step == STEPS_PER_EPOCH:
                    print(f"epoch={epoch}/{EPOCHS} train_patch={step}/{STEPS_PER_EPOCH} loss={float(full_loss):.6f}", flush=True)

            val_histogram, _, val_coverage = evaluate(model, val_reader, val_subset, device)
            val_metrics = asdict(val_histogram.metrics(0.5))
            assert_finite_tree(val_metrics, "validation_metrics")
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
            save_checkpoint(args.run_dir / "last.pt", model, optimizer, scaler, rng, epoch, val_metrics)
            if val_metrics["pr_auc_approx"] > best_score:
                best_score = val_metrics["pr_auc_approx"]
                save_checkpoint(args.run_dir / "best.pt", model, optimizer, scaler, rng, epoch, val_metrics)
            print(
                f"epoch={epoch:03d}/{EPOCHS} loss={row['train_loss']:.6f} "
                f"val_dice={val_metrics['dice']:.6f} val_pr_auc={val_metrics['pr_auc_approx']:.6f} "
                f"minutes={row['seconds']/60:.2f}", flush=True,
            )

        best = torch.load(args.run_dir / "best.pt", map_location="cpu", weights_only=False)
        model.load_state_dict(best["model"], strict=True)
        print(f"BEST EPOCH: {best['epoch']}; full validation begins", flush=True)
        final_val_coords = val_subset if args.smoke else all_val
        full_val_hist, _, full_val_coverage = evaluate(model, val_reader, final_val_coords, device)
        if not args.smoke and full_val_coverage["raw_voxels"] != math.prod(val_reader.shape):
            raise RuntimeError("Incomplete validation coverage")
        threshold = full_val_hist.best_dice_threshold()
        full_val_metrics = asdict(full_val_hist.metrics(threshold))
        assert_finite_tree(full_val_metrics, "full_validation_metrics")
        selection = {
            "best_epoch": best["epoch"], "threshold": threshold,
            "threshold_source": "smoke validation subset only" if args.smoke else "complete val1.h5 + val2.h5 only",
            "full_validation": full_val_metrics,
            "full_validation_coverage": full_val_coverage,
        }
        (args.run_dir / "validation_selection.json").write_text(json.dumps(selection, indent=2) + "\n")
        print(f"VALIDATION THRESHOLD: {threshold:.6f}; test evaluation disabled", flush=True)
    finally:
        train_reader.close()
        val_reader.close()

    status = {
        "status": "smoke_complete" if args.smoke else "validation_only_complete",
        "seed": SEED, "epochs_completed": len(history), "epochs_requested": EPOCHS,
        "protocol_hash": PROTOCOL_HASH, "precision": "float16_autocast",
        "gradient_scaling": True, "test_files_read": False,
        "best_epoch": int(best["epoch"]), "threshold": float(threshold),
        "best_checkpoint": str(args.run_dir / "best.pt"),
        "last_checkpoint": str(args.run_dir / "last.pt"),
        "peak_gpu_allocated_gib": torch.cuda.max_memory_allocated() / 1024**3,
        "peak_gpu_reserved_gib": torch.cuda.max_memory_reserved() / 1024**3,
    }
    write_json_atomic(args.run_dir / "status.json", status)
    print(f"R100 VALIDATION-ONLY COMPLETE seed={SEED} epochs={len(history)} best_epoch={best['epoch']}", flush=True)


if __name__ == "__main__":
    main()
