#!/usr/bin/env python3
"""Train a controlled FaultEdgeFormer-inspired model on the R100 Thebe protocol.

This is an architecture comparison, not a reproduction of the source paper.
It keeps R100's Thebe files, 128^3 inputs, observed-voxel mask, per-patch
normalization, random sampling, single axis flip, masked BCE, Adam optimizer,
checkpoint-selection rule, and validation evaluator. Test files are never read.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import random
import time
from dataclasses import asdict
from pathlib import Path

# Required by cuBLAS when deterministic algorithms are enabled below.
os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")

import torch
from torch.nn import functional as F

import faultseg3d_baseline as baseline
import train_r100_fp16_clean as r100
from evaluate_thebe_zero_shot_r100_pinned import ConcatenatedThebe
from faultedgeformer_model import FaultEdgeFormerInspired, count_parameters


EXPERIMENT = "FaultEdgeFormer_inspired_Thebe_architecture_control"
PAPER_DOI = "https://doi.org/10.1093/jge/gxag041"
SIZE = 128
BINS = 2048
LR = 1e-4
GRAD_ACCUMULATION = 2
SOURCE_FILES = (
    Path("scripts/faultedgeformer_model.py"),
    Path("scripts/train_faultedgeformer_thebe.py"),
    Path("scripts/train_r100_fp16_clean.py"),
    Path("scripts/faultseg3d_baseline.py"),
    Path("scripts/evaluate_thebe_zero_shot_r100_pinned.py"),
)


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_hashes() -> dict[str, str]:
    missing = [str(path) for path in SOURCE_FILES if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"Missing source files: {missing}")
    return {str(path): file_hash(path) for path in SOURCE_FILES}


def save_checkpoint(
    path: Path,
    model: FaultEdgeFormerInspired,
    optimizer: torch.optim.Optimizer,
    scaler: torch.amp.GradScaler,
    rng: random.Random,
    epoch: int,
    validation: dict,
    config: dict,
) -> None:
    r100.assert_finite_tree(model.state_dict(), "checkpoint.model")
    r100.assert_finite_tree(optimizer.state_dict(), "checkpoint.optimizer")
    temporary = path.with_suffix(path.suffix + ".part")
    torch.save(
        {
            "model": model.state_dict(),
            "optimizer": optimizer.state_dict(),
            "epoch": epoch,
            "validation_metrics": validation,
            "scaler": scaler.state_dict(),
            "python_rng": rng.getstate(),
            "torch_rng": torch.get_rng_state(),
            "cuda_rng": torch.cuda.get_rng_state_all(),
            "args": config,
        },
        temporary,
    )
    temporary.replace(path)


def cpu_preflight(thebe_root: Path) -> None:
    train_files = r100.split_paths(thebe_root, "train", 9)
    val_files = r100.split_paths(thebe_root, "val", 2)
    train_reader = ConcatenatedThebe(train_files)
    val_reader = ConcatenatedThebe(val_files)
    try:
        model = FaultEdgeFormerInspired(use_checkpoint=False)
        example = torch.zeros(1, 1, 16, 16, 16)
        output = model(example)
        if output.shape != example.shape:
            raise RuntimeError(f"Shape mismatch: {output.shape} != {example.shape}")
        document = {
            "status": "cpu_preflight_pass",
            "model": type(model).__name__,
            "model_parameters": count_parameters(model),
            "paper_reported_parameters": 1_340_000,
            "parameter_difference_fraction": (
                count_parameters(model) - 1_340_000
            ) / 1_340_000,
            "train_shape": train_reader.shape,
            "validation_shape": val_reader.shape,
            "model_spec": model.spec,
            "source_hashes": source_hashes(),
            "test_files_read": False,
        }
        print(json.dumps(document, indent=2), flush=True)
    finally:
        train_reader.close()
        val_reader.close()


def make_config(args, model, train_files, val_files, val_subset, all_val) -> dict:
    return {
        "experiment": EXPERIMENT,
        "paper": PAPER_DOI,
        "claim_scope": "paper-inspired architecture control; not exact reproduction",
        "seed": args.seed,
        "model_class": "faultedgeformer_model.FaultEdgeFormerInspired",
        "model_spec": model.spec,
        "model_parameters": count_parameters(model),
        "paper_reported_parameters": 1_340_000,
        "precision": "float16_autocast",
        "gradient_scaling": True,
        "determinism": {
            "seeded_python_numpy_torch_cuda": True,
            "cudnn_deterministic": True,
            "cublas_workspace_config": os.environ["CUBLAS_WORKSPACE_CONFIG"],
            "known_cuda_exception": (
                "trilinear-upsample backward has no deterministic CUDA implementation; "
                "PyTorch warn-only policy retained"
            ),
        },
        "source_hashes": source_hashes(),
        "torch_version": str(torch.__version__),
        "torch_cuda_build": torch.version.cuda,
        "gpu_name": torch.cuda.get_device_name(),
        "train_files": [str(path) for path in train_files],
        "validation_files": [str(path) for path in val_files],
        "data_file_metadata": {
            str(path): {"bytes": path.stat().st_size, "mtime_ns": path.stat().st_mtime_ns}
            for path in train_files + val_files
        },
        "test_files_read": False,
        "epochs": args.epochs,
        "train_patches_per_epoch": args.train_patches,
        "patch_size": SIZE,
        "validation_patches_per_epoch": len(val_subset),
        "full_validation_patches": len(all_val),
        "validation_seed": args.validation_seed,
        "validation_subset_coordinates": val_subset,
        "train_sampling": (
            f"{args.train_patches // len(train_files)} observed random patches "
            "per train file each epoch; random axis-0 flip"
        ),
        "validity": "finite raw seismic != 0; masked BCE and masked metrics",
        "normalization": "per-patch z-score over observed voxels; axis reversal",
        "optimizer": "Adam",
        "learning_rate": LR,
        "loss": "ordinary BCE averaged over observed voxels",
        "gradient_accumulation": GRAD_ACCUMULATION,
        "checkpoint_selection": "highest PR-AUC on fixed validation subset",
        "threshold_selection": (
            "best Dice on smoke validation subset"
            if args.smoke
            else (
                "best Dice on fixed checkpoint-selection validation subset; pilot only"
                if args.selection_only
                else "best Dice on complete val1.h5 + val2.h5 after training"
            )
        ),
        "test_policy": "training and validation only; test files are never opened",
        "comparison_control": (
            "R100 data/mask/normalization/sampling/loss/optimizer/selection retained; "
            "architecture changed"
        ),
        "known_deviations_from_paper": [
            "author code unavailable",
            "paper figure-only channel and normalization details inferred",
            "128^3 R100 patches replace paper's 96^3 synthetic crops",
            "R100 augmentation retained to isolate architecture",
            "invalid Thebe voxels excluded from loss and metrics",
            "validation checkpoint selected by PR-AUC instead of paper fixed final epoch",
        ],
        "smoke": args.smoke,
        "selection_only": args.selection_only,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--thebe-root", type=Path, default=Path("data/processed/thebe_h5")
    )
    parser.add_argument("--run-dir", type=Path)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--validation-seed", type=int, default=1042)
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--train-patches", type=int, default=360)
    parser.add_argument("--validation-patches", type=int, default=128)
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument(
        "--selection-only",
        action="store_true",
        help="Finish on the fixed validation subset; intended only for pilot screening",
    )
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()

    if args.smoke:
        args.epochs = 1
        args.train_patches = 18
        args.validation_patches = 2
    if args.epochs <= 0 or args.train_patches <= 0 or args.train_patches % 9:
        parser.error("epochs must be positive and train-patches a positive multiple of 9")
    if args.validation_patches <= 0:
        parser.error("validation-patches must be positive")
    if args.check_only:
        cpu_preflight(args.thebe_root)
        return 0
    if args.run_dir is None:
        parser.error("--run-dir is required for GPU execution")
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA GPU required")

    train_files = r100.split_paths(args.thebe_root, "train", 9)
    val_files = r100.split_paths(args.thebe_root, "val", 2)
    if len({path.resolve() for path in train_files + val_files}) != 11:
        raise RuntimeError("Train/validation files overlap")
    if args.resume:
        if not args.run_dir.is_dir():
            raise RuntimeError(f"Missing resume directory: {args.run_dir}")
    elif args.run_dir.exists():
        raise RuntimeError(f"Run directory already exists: {args.run_dir}")

    torch.cuda.reset_peak_memory_stats()
    free_gpu, _ = torch.cuda.mem_get_info()
    if free_gpu < 8 * 1024**3:
        raise RuntimeError(f"Insufficient free GPU memory: {free_gpu / 1024**3:.1f} GiB")

    train_reader = ConcatenatedThebe(train_files)
    val_reader = ConcatenatedThebe(val_files)
    try:
        if train_reader.shape != (900, 3174, 1537):
            raise RuntimeError(f"Unexpected train shape: {train_reader.shape}")
        if val_reader.shape != (200, 3174, 1537):
            raise RuntimeError(f"Unexpected validation shape: {val_reader.shape}")

        baseline.seed_everything(args.seed)
        rng = random.Random(args.seed)
        device = torch.device("cuda")
        model = FaultEdgeFormerInspired(use_checkpoint=True).to(device)
        optimizer = torch.optim.Adam(model.parameters(), lr=LR)
        scaler = torch.amp.GradScaler("cuda", enabled=True)
        all_val, val_subset = r100.fixed_validation_subset(
            val_reader.shape, args.validation_patches, args.validation_seed
        )
        config = make_config(
            args, model, train_files, val_files, val_subset, all_val
        )
        protocol = {key: value for key, value in config.items() if key != "seed"}
        protocol_hash = hashlib.sha256(
            json.dumps(protocol, sort_keys=True).encode()
        ).hexdigest()
        config["protocol_hash"] = protocol_hash

        checkpoint_path = args.run_dir / "last.pt"
        best_path = args.run_dir / "best.pt"
        history_path = args.run_dir / "history.csv"
        if args.resume:
            saved_config = json.loads((args.run_dir / "run_config.json").read_text())
            if saved_config != json.loads(json.dumps(config)):
                raise RuntimeError("Saved configuration differs; refusing incompatible resume")
            if not all(path.is_file() for path in (checkpoint_path, best_path, history_path)):
                raise RuntimeError("Resume requires last.pt, best.pt, and history.csv")
            with history_path.open(newline="") as stream:
                history = list(csv.DictReader(stream))
            last = torch.load(checkpoint_path, map_location="cpu", weights_only=False)
            best_saved = torch.load(best_path, map_location="cpu", weights_only=False)
            completed = int(last["epoch"])
            if not history or int(history[-1]["epoch"]) != completed:
                raise RuntimeError("Checkpoint and history disagree")
            model.load_state_dict(last["model"], strict=True)
            optimizer.load_state_dict(last["optimizer"])
            scaler.load_state_dict(last["scaler"])
            rng.setstate(last["python_rng"])
            torch.set_rng_state(last["torch_rng"])
            torch.cuda.set_rng_state_all(last["cuda_rng"])
            best_score = float(best_saved["validation_metrics"]["pr_auc_approx"])
            first_epoch = completed + 1
        else:
            args.run_dir.mkdir(parents=True)
            r100.write_json_atomic(args.run_dir / "run_config.json", config)
            history = []
            best_score = -1.0
            first_epoch = 1

        print(
            f"PREFLIGHT PASS model={type(model).__name__} "
            f"parameters={count_parameters(model)} train={train_reader.shape} "
            f"val={val_reader.shape} test_disabled=True",
            flush=True,
        )

        for epoch in range(first_epoch, args.epochs + 1):
            epoch_started = time.time()
            model.train()
            optimizer.zero_grad(set_to_none=True)
            running_loss = 0.0
            skipped_candidates = 0
            excluded_training_labels = 0
            patches_per_file = args.train_patches // len(train_files)
            for step in range(1, args.train_patches + 1):
                file_index = (step - 1) // patches_per_file
                for _ in range(30):
                    x0 = (
                        train_reader.offsets[file_index]
                        + rng.randrange(train_reader.lengths[file_index])
                    )
                    y0 = rng.randrange(train_reader.shape[1] - SIZE + 1)
                    z0 = rng.randrange(train_reader.shape[2] - SIZE + 1)
                    x, target, mask, _, observed, ignored_pos, constant = r100.read_patch(
                        train_reader, (x0, y0, z0)
                    )
                    if not constant and observed >= int(0.05 * SIZE**3):
                        break
                    skipped_candidates += 1
                else:
                    raise RuntimeError("Unable to sample an observed training patch")
                excluded_training_labels += ignored_pos
                if rng.randrange(2):
                    x, target, mask = x.flip(-3), target.flip(-3), mask.flip(-3)
                x = x.to(device)
                target = target.to(device)
                mask = mask.to(device)
                with torch.autocast(device_type="cuda", dtype=torch.float16):
                    logits = model(x)
                voxel_loss = F.binary_cross_entropy_with_logits(
                    logits.float(), target, reduction="none"
                )
                loss = voxel_loss[mask].mean()
                r100.assert_finite_tree(loss, "training_loss")
                scaler.scale(loss / GRAD_ACCUMULATION).backward()
                running_loss += float(loss.detach())
                if step % GRAD_ACCUMULATION == 0:
                    scaler.step(optimizer)
                    scaler.update()
                    optimizer.zero_grad(set_to_none=True)
                if step % max(1, args.train_patches // 6) == 0:
                    print(
                        f"epoch={epoch}/{args.epochs} "
                        f"train_patch={step}/{args.train_patches} "
                        f"loss={float(loss):.6f}",
                        flush=True,
                    )

            val_histogram, _, val_coverage = r100.evaluate(
                model, val_reader, val_subset, device
            )
            val_metrics = asdict(val_histogram.metrics(0.5))
            r100.assert_finite_tree(val_metrics, "validation_metrics")
            row = {
                "epoch": epoch,
                "train_loss": running_loss / args.train_patches,
                "train_patches": args.train_patches,
                "resampled_no_data_candidates": skipped_candidates,
                "excluded_training_positive_labels": excluded_training_labels,
                "seconds": time.time() - epoch_started,
                **{f"val_{key}": value for key, value in val_metrics.items()},
            }
            history.append(row)
            baseline.write_history(history_path, history)
            save_checkpoint(
                checkpoint_path,
                model,
                optimizer,
                scaler,
                rng,
                epoch,
                val_metrics,
                config,
            )
            if val_metrics["pr_auc_approx"] > best_score:
                best_score = val_metrics["pr_auc_approx"]
                save_checkpoint(
                    best_path,
                    model,
                    optimizer,
                    scaler,
                    rng,
                    epoch,
                    val_metrics,
                    config,
                )
            print(
                f"epoch={epoch:03d}/{args.epochs} "
                f"loss={row['train_loss']:.6f} "
                f"val_dice={val_metrics['dice']:.6f} "
                f"val_pr_auc={val_metrics['pr_auc_approx']:.6f} "
                f"minutes={row['seconds'] / 60:.2f}",
                flush=True,
            )

        best = torch.load(best_path, map_location="cpu", weights_only=False)
        model.load_state_dict(best["model"], strict=True)
        final_coordinates = val_subset if (args.smoke or args.selection_only) else all_val
        print(
            f"BEST EPOCH: {best['epoch']}; "
            f"validation_patches={len(final_coordinates)}",
            flush=True,
        )
        final_histogram, _, final_coverage = r100.evaluate(
            model, val_reader, final_coordinates, device
        )
        if (
            not args.smoke
            and not args.selection_only
            and final_coverage["raw_voxels"] != math.prod(val_reader.shape)
        ):
            raise RuntimeError("Incomplete full-validation coverage")
        threshold = final_histogram.best_dice_threshold()
        final_metrics = asdict(final_histogram.metrics(threshold))
        selection = {
            "best_epoch": int(best["epoch"]),
            "threshold": float(threshold),
            "threshold_source": (
                "smoke subset"
                if args.smoke
                else (
                    "fixed checkpoint-selection subset; pilot only"
                    if args.selection_only
                    else "complete val1.h5 + val2.h5"
                )
            ),
            "full_validation": final_metrics,
            "full_validation_coverage": final_coverage,
            "test_files_read": False,
        }
        r100.write_json_atomic(args.run_dir / "validation_selection.json", selection)
        status = {
            "status": (
                "smoke_complete"
                if args.smoke
                else (
                    "selection_subset_pilot_complete"
                    if args.selection_only
                    else "validation_only_complete"
                )
            ),
            "experiment": EXPERIMENT,
            "seed": args.seed,
            "epochs_completed": len(history),
            "epochs_requested": args.epochs,
            "protocol_hash": protocol_hash,
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
