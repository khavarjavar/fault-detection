#!/usr/bin/env python3
"""Supervised Thebe experiment using Mahzad and Bagheri's Attention3DUNet.

This is an adaptation of the published architecture and Unified Focal Loss.
It can start from random weights or transfer every feature tensor from an
Attention3D denoising checkpoint while keeping a freshly initialized output
head. All parameters remain trainable after transfer. It reads only train*.h5
and val*.h5. Test files are reserved for a separate final evaluation.

Run from the fault_detection project root with its .venv_train Python.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
import random
import sys
import time
import types
from pathlib import Path

import h5py
import numpy as np
import torch
from torch.nn.attention import SDPBackend, sdpa_kernel
from torch.utils.data import DataLoader, Dataset


PATCH = 64
THRESHOLD = 0.5
AMP_DTYPE = torch.bfloat16


def load_paper_code(path: Path):
    if not path.is_file():
        raise FileNotFoundError(path)
    # The upstream module imports TensorBoard at module load, although this
    # experiment uses its architecture/loss classes and its own training loop.
    # This shim avoids installing an unrelated package into the user's venv.
    if importlib.util.find_spec("tensorboard") is None:
        stub = types.ModuleType("torch.utils.tensorboard")
        stub.SummaryWriter = object
        sys.modules["torch.utils.tensorboard"] = stub
    spec = importlib.util.spec_from_file_location("paper_attention3d", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import the authors' model: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class ThebePatches(Dataset):
    """Deterministic, on-demand 64-cube samples from disjoint H5 files."""

    def __init__(
        self,
        paths: list[Path],
        count: int,
        seed: int,
        balance_fault_patches: bool,
    ) -> None:
        if not paths:
            raise RuntimeError("No Thebe H5 files were supplied")
        self.paths = paths
        self.handles = [h5py.File(path, "r") for path in paths]
        self.shapes = []
        self.count = count
        self.seed = seed
        self.epoch = 0
        self.balance_fault_patches = balance_fault_patches
        for path, handle in zip(paths, self.handles):
            if "seismic" not in handle or "fault" not in handle:
                raise RuntimeError(f"Missing seismic/fault datasets: {path}")
            shape = tuple(handle["seismic"].shape)
            if shape != tuple(handle["fault"].shape) or any(n < PATCH for n in shape):
                raise RuntimeError(f"Invalid H5 shapes: {path}: {shape}")
            self.shapes.append(shape)

    def __len__(self) -> int:
        return self.count

    def close(self) -> None:
        for handle in self.handles:
            handle.close()

    def __getitem__(self, index: int):
        rng = np.random.default_rng(self.seed + self.epoch * 1_000_003 + index * 1009)
        # Force faults in half the training patches; sample the rest uniformly.
        # Forcing empty masks in the other half can fail on a fault-rich cube.
        want_fault = True if self.balance_fault_patches and index % 2 == 0 else None
        attempts = 256 if want_fault is True else 64
        for _ in range(attempts):
            file_index = int(rng.integers(len(self.handles)))
            shape = self.shapes[file_index]
            start = tuple(int(rng.integers(0, n - PATCH + 1)) for n in shape)
            slices = tuple(slice(s, s + PATCH) for s in start)
            handle = self.handles[file_index]
            target_raw = np.asarray(handle["fault"][slices])
            if not np.isfinite(target_raw).all():
                raise RuntimeError(f"Nonfinite fault labels in {self.paths[file_index]}")
            if not np.logical_or(target_raw == 0, target_raw == 1).all():
                raise RuntimeError(
                    f"Nonbinary fault labels in {self.paths[file_index]}: "
                    f"min={target_raw.min()} max={target_raw.max()}"
                )
            target = target_raw.astype(np.uint8, copy=False)
            if want_fault is not None and bool(target.any()) != want_fault:
                continue
            seismic = np.asarray(handle["seismic"][slices], dtype=np.float32)
            if not np.isfinite(seismic).all():
                raise RuntimeError(f"Nonfinite seismic in {self.paths[file_index]}")

            # Keep zero samples *within* a populated trace, but mask leading
            # and trailing no-data samples along the time axis (last axis).
            nonzero = seismic != 0.0
            has_data = nonzero.any(axis=2)
            if not has_data.any():
                continue
            first = nonzero.argmax(axis=2)
            last = PATCH - 1 - nonzero[..., ::-1].argmax(axis=2)
            times = np.arange(PATCH)[None, None, :]
            valid = has_data[..., None] & (times >= first[..., None]) & (times <= last[..., None])
            values = seismic[valid]
            std = float(values.std(dtype=np.float64))
            if std <= 1e-8:
                continue
            mean = float(values.mean(dtype=np.float64))
            normalized = np.zeros_like(seismic)
            normalized[valid] = (seismic[valid] - mean) / std
            if not np.isfinite(normalized).all():
                raise RuntimeError(f"Nonfinite normalized seismic in {self.paths[file_index]}")
            return (
                torch.from_numpy(np.ascontiguousarray(normalized[None])),
                torch.from_numpy(np.ascontiguousarray(target[None].astype(np.float32))),
                torch.from_numpy(np.ascontiguousarray(valid[None])),
            )
        raise RuntimeError(
            f"Unable to sample {'fault' if want_fault else 'valid'} patch "
            f"for index {index}; inspect the Thebe H5 labels"
        )


def save_atomic(path: Path, value: object) -> None:
    temporary = path.with_name(path.name + ".part")
    torch.save(value, temporary)
    temporary.replace(path)


def save_history(path: Path, rows: list[dict]) -> None:
    temporary = path.with_name(path.name + ".part")
    with temporary.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def transfer_pretrained_features(model: torch.nn.Module, checkpoint_path: Path) -> dict:
    """Load denoising features exactly and retain a fresh segmentation head."""
    checkpoint = torch.load(checkpoint_path, map_location="cpu", weights_only=False)
    if "model" not in checkpoint or not isinstance(checkpoint["model"], dict):
        raise RuntimeError(f"Checkpoint does not contain a model state: {checkpoint_path}")
    source = checkpoint["model"]
    expected = model.state_dict()
    if set(source) != set(expected):
        missing = sorted(set(expected) - set(source))
        unexpected = sorted(set(source) - set(expected))
        raise RuntimeError(
            f"Pretraining and segmentation schemas differ: missing={missing} "
            f"unexpected={unexpected}"
        )
    head = {name for name in expected if name.startswith("out_conv.")}
    features = set(expected) - head
    if not head:
        raise RuntimeError("Attention3D output head was not found")
    fresh_head = {name: expected[name].clone() for name in head}
    for name, value in source.items():
        if value.shape != expected[name].shape:
            raise RuntimeError(f"Checkpoint shape mismatch for {name}")
        if not torch.isfinite(value).all().item():
            raise FloatingPointError(f"Nonfinite checkpoint tensor: {name}")
    loaded = model.load_state_dict(
        {name: source[name] for name in features}, strict=False
    )
    if set(loaded.missing_keys) != head or loaded.unexpected_keys:
        raise RuntimeError(f"Unexpected feature-transfer result: {loaded}")
    after = model.state_dict()
    if not all(torch.equal(after[name], source[name]) for name in features):
        raise RuntimeError("A transferred feature tensor differs from its source")
    if not all(torch.equal(after[name], fresh_head[name]) for name in head):
        raise RuntimeError("The freshly initialized segmentation head changed")
    return {
        "checkpoint": str(checkpoint_path),
        "checkpoint_sha256": sha256(checkpoint_path),
        "feature_tensor_count": len(features),
        "feature_tensors_loaded": sorted(features),
        "fresh_head_tensors": sorted(head),
        "exact_values_verified": True,
        "all_parameters_trainable_after_transfer": all(
            parameter.requires_grad for parameter in model.parameters()
        ),
    }


def require_finite(tensor: torch.Tensor, *, stage: str, epoch: int, patch: int) -> None:
    finite_mask = torch.isfinite(tensor)
    if bool(finite_mask.all().item()):
        return

    nan_count = int(torch.isnan(tensor).sum().item())
    posinf_count = int(torch.isposinf(tensor).sum().item())
    neginf_count = int(torch.isneginf(tensor).sum().item())
    finite_values = tensor[finite_mask]

    if finite_values.numel():
        finite_min = float(finite_values.min().item())
        finite_max = float(finite_values.max().item())
    else:
        finite_min = float("nan")
        finite_max = float("nan")

    raise FloatingPointError(
        f"NONFINITE stage={stage} epoch={epoch} patch={patch} "
        f"nan={nan_count} posinf={posinf_count} neginf={neginf_count} "
        f"finite_min={finite_min} finite_max={finite_max}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--thebe-root", type=Path, default=Path("data/processed/thebe_h5"))
    parser.add_argument("--paper-source", type=Path, default=Path("external/attention3d_paper/fault-detection-global-attention.py"))
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--pretrained-checkpoint", type=Path)
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--train-patches", type=int, default=64)
    parser.add_argument("--val-patches", type=int, default=32)
    parser.add_argument("--accumulate", type=int, default=4)
    parser.add_argument("--patience", type=int, default=20)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    if not torch.cuda.is_available():
        raise RuntimeError("CUDA GPU required for full global 3D attention")
    if not torch.cuda.is_bf16_supported():
        raise RuntimeError("This stability-fixed run requires a BF16-capable CUDA GPU")
    if min(args.epochs, args.train_patches, args.val_patches, args.accumulate, args.patience) <= 0:
        raise ValueError("Epochs, patch counts, accumulation, and patience must be positive")
    train_paths = sorted(args.thebe_root.glob("train*.h5"))
    val_paths = sorted(args.thebe_root.glob("val*.h5"))
    if not train_paths or not val_paths or set(train_paths) & set(val_paths):
        raise RuntimeError("Expected disjoint train*.h5 and val*.h5 files")
    paper = load_paper_code(args.paper_source)

    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    torch.cuda.manual_seed_all(args.seed)
    torch.backends.cudnn.benchmark = True
    torch.backends.cuda.enable_math_sdp(False)
    torch.cuda.reset_peak_memory_stats()

    model = paper.Attention3DUNet()
    transfer = None
    if args.pretrained_checkpoint is not None:
        if not args.pretrained_checkpoint.is_file():
            raise FileNotFoundError(args.pretrained_checkpoint)
        transfer = transfer_pretrained_features(model, args.pretrained_checkpoint)
    model = model.cuda()
    expected_parameters = 45_001_057
    actual_parameters = paper.count_parameters(model)
    if actual_parameters != expected_parameters:
        raise RuntimeError(f"Unexpected paper model size: {actual_parameters}")
    criterion = paper.UnifiedFocalLoss(
        lambda_param=0.5, tversky_alpha=0.3, tversky_beta=0.7,
        tversky_gamma=1.33, focal_alpha=0.25, focal_gamma=2.0,
    )
    optimizer = torch.optim.AdamW(model.parameters(), lr=5e-4, weight_decay=1e-4)
    scaler = torch.amp.GradScaler("cuda", enabled=False)
    updates_per_epoch = math.ceil(args.train_patches / args.accumulate)
    total_updates = max(1, args.epochs * updates_per_epoch)
    warmup_updates = max(1, total_updates // 10)

    def lr_multiplier(step: int) -> float:
        if step < warmup_updates:
            return (1 / 32) + (31 / 32) * step / warmup_updates
        remaining = max(1, total_updates - warmup_updates)
        return max(1 / 32, 1 - (1 - 1 / 32) * (step - warmup_updates) / remaining)

    scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, lr_multiplier)
    train_set = ThebePatches(train_paths, args.train_patches, args.seed, True)
    val_set = ThebePatches(val_paths, args.val_patches, args.seed + 97_531, False)
    train_loader = DataLoader(train_set, batch_size=1, shuffle=False, num_workers=0, pin_memory=True)
    val_loader = DataLoader(val_set, batch_size=1, shuffle=False, num_workers=0, pin_memory=True)

    run_dir = args.run_dir
    run_dir.mkdir(parents=True, exist_ok=True)
    last_path = run_dir / "last.pt"
    history_path = run_dir / "history.csv"
    if not last_path.exists() and any(run_dir.iterdir()):
        raise RuntimeError(f"Nonempty run directory without resumable checkpoint: {run_dir}")
    config = {
        "experiment": (
            "paper_global_attention_real_Thebe_end_to_end_finetune_from_field_denoising"
            if transfer is not None else
            "paper_global_attention_real_Thebe_supervised_without_denoising_pretraining_bf16_stability_fixed"
        ),
        "paper_source": str(args.paper_source),
        "parameter_count": actual_parameters,
        "train_files": [str(p) for p in train_paths],
        "validation_files": [str(p) for p in val_paths],
        "test_files_read": False,
        "pretraining_performed": transfer is not None,
        "pretraining_transfer": transfer,
        "fine_tuning": "all 45,001,057 parameters trainable end to end",
        "threshold": THRESHOLD,
        "patch_size": PATCH,
        "train_patches_per_epoch": args.train_patches,
        "validation_patches_fixed": args.val_patches,
        "train_sampling": "half of patches contain at least one labeled fault voxel",
        "validation_sampling": "fixed uniform random positions from validation H5 files",
        "optimizer": "AdamW 5e-4, weight_decay 1e-4",
        "precision": "BF16 autocast; gradient scaling disabled",
        "nonfinite_policy": "abort on nonfinite normalized input, logits, loss, or gradient norm",
        "loss": "authors' UnifiedFocalLoss; lambda=0.5, alpha=0.3, beta=0.7",
        "accumulation_steps": args.accumulate,
        "seed": args.seed,
        "paper_results_comparable": False,
    }
    if not last_path.exists():
        (run_dir / "run_configuration.json").write_text(json.dumps(config, indent=2) + "\n")

    start_epoch, best_dice, stale_epochs = 0, float("-inf"), 0
    history: list[dict] = []
    if last_path.exists():
        previous = torch.load(last_path, map_location="cpu", weights_only=False)
        model.load_state_dict(previous["model"], strict=True)
        optimizer.load_state_dict(previous["optimizer"])
        scheduler.load_state_dict(previous["scheduler"])
        scaler.load_state_dict(previous["scaler"])
        start_epoch = int(previous["epoch"]) + 1
        best_dice = float(previous["best_dice"])
        stale_epochs = int(previous["stale_epochs"])
        if history_path.exists():
            with history_path.open(newline="", encoding="utf-8") as stream:
                history = list(csv.DictReader(stream))
        print(f"RESUME epoch={start_epoch + 1} best_val_dice={best_dice:.6f}", flush=True)

    print(f"train_files={len(train_paths)} val_files={len(val_paths)} test_files_read=0", flush=True)
    print(f"parameters={actual_parameters} epochs={args.epochs} "
          f"train_patches={args.train_patches} val_patches={args.val_patches}", flush=True)
    started = time.time()
    try:
        for epoch in range(start_epoch, args.epochs):
            train_set.epoch = epoch
            model.train()
            optimizer.zero_grad(set_to_none=True)
            train_losses = []
            for index, (seismic, target, valid) in enumerate(train_loader):
                seismic = seismic.cuda(non_blocking=True)
                target = target.cuda(non_blocking=True)
                valid = valid.cuda(non_blocking=True)
                with sdpa_kernel([SDPBackend.FLASH_ATTENTION, SDPBackend.EFFICIENT_ATTENTION]):
                    with torch.autocast("cuda", dtype=AMP_DTYPE):
                        logits = model(seismic)
                    require_finite(
                        logits, stage="train_logits",
                        epoch=epoch + 1, patch=index + 1
                    )
                    loss = criterion(logits.float()[valid], target[valid])
                    require_finite(
                        loss, stage="train_loss",
                        epoch=epoch + 1, patch=index + 1
                    )
                train_losses.append(float(loss.detach().item()))
                # Short final accumulation group gets the correct scale.
                group_start = (index // args.accumulate) * args.accumulate
                group_size = min(args.accumulate, len(train_loader) - group_start)
                scaler.scale(loss / group_size).backward()
                if (index + 1) % args.accumulate == 0 or index + 1 == len(train_loader):
                    scaler.unscale_(optimizer)
                    grad_norm = torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
                    require_finite(
                        grad_norm, stage="train_grad_norm",
                        epoch=epoch + 1, patch=index + 1
                    )
                    scaler.step(optimizer)
                    scaler.update()
                    optimizer.zero_grad(set_to_none=True)
                    scheduler.step()
                if (index + 1) % 16 == 0 or index + 1 == len(train_loader):
                    print(f"epoch={epoch + 1}/{args.epochs} train_patch="
                          f"{index + 1}/{len(train_loader)} loss={loss.item():.5f}", flush=True)

            model.eval()
            tp = fp = fn = valid_total = positive_total = 0
            val_losses = []
            with torch.inference_mode():
                for val_index, (seismic, target, valid) in enumerate(val_loader):
                    seismic = seismic.cuda(non_blocking=True)
                    target = target.cuda(non_blocking=True)
                    valid = valid.cuda(non_blocking=True)
                    with sdpa_kernel([SDPBackend.FLASH_ATTENTION, SDPBackend.EFFICIENT_ATTENTION]):
                        with torch.autocast("cuda", dtype=AMP_DTYPE):
                            logits = model(seismic)
                        require_finite(
                            logits, stage="val_logits",
                            epoch=epoch + 1, patch=val_index + 1
                        )
                        val_loss = criterion(logits.float()[valid], target[valid])
                        require_finite(
                            val_loss, stage="val_loss",
                            epoch=epoch + 1, patch=val_index + 1
                        )
                        val_losses.append(float(val_loss.item()))
                    predicted = torch.sigmoid(logits.float()) >= THRESHOLD
                    truth = target >= 0.5
                    tp += int((predicted & truth & valid).sum().item())
                    fp += int((predicted & ~truth & valid).sum().item())
                    fn += int((~predicted & truth & valid).sum().item())
                    valid_total += int(valid.sum().item())
                    positive_total += int((truth & valid).sum().item())
            if positive_total == 0:
                raise RuntimeError("Validation sample contained no fault labels; increase --val-patches")
            dice = 2 * tp / max(1, 2 * tp + fp + fn)
            row = {
                "epoch": epoch + 1, "train_loss": sum(train_losses) / len(train_losses),
                "val_loss": sum(val_losses) / len(val_losses), "val_dice": dice,
                "val_precision": tp / max(1, tp + fp),
                "val_recall": tp / max(1, tp + fn),
                "val_fault_prevalence": positive_total / valid_total,
                "lr": optimizer.param_groups[0]["lr"],
                "seconds_elapsed": time.time() - started,
            }
            history.append(row)
            save_history(history_path, history)
            improved = dice > best_dice
            if improved:
                best_dice = dice
                stale_epochs = 0
                save_atomic(run_dir / "best.pt", {
                    "model": model.state_dict(), "epoch": epoch + 1,
                    "validation_metrics": row, "config": config,
                })
            else:
                stale_epochs += 1
            save_atomic(last_path, {
                "model": model.state_dict(), "optimizer": optimizer.state_dict(),
                "scheduler": scheduler.state_dict(), "scaler": scaler.state_dict(),
                "epoch": epoch, "best_dice": best_dice, "stale_epochs": stale_epochs,
            })
            print(f"EPOCH {epoch + 1:03d} train_loss={row['train_loss']:.6f} "
                  f"val_loss={row['val_loss']:.6f} val_dice={dice:.6f} "
                  f"val_precision={row['val_precision']:.6f} "
                  f"val_recall={row['val_recall']:.6f} "
                  f"best={best_dice:.6f} elapsed_min={(time.time()-started)/60:.1f}", flush=True)
            if stale_epochs >= args.patience:
                print(f"EARLY_STOP after {stale_epochs} unimproved epochs", flush=True)
                break
    finally:
        train_set.close()
        val_set.close()
    (run_dir / "status.json").write_text(json.dumps({
        "status": "supervised_training_complete", "best_validation_dice": best_dice,
        "epochs_completed": len(history), "best_checkpoint": str(run_dir / "best.pt"),
        "test_files_read": False,
    }, indent=2) + "\n")
    print(f"TRAINING_COMPLETE best_val_dice={best_dice:.6f} "
          f"checkpoint={run_dir / 'best.pt'}", flush=True)


if __name__ == "__main__":
    main()
