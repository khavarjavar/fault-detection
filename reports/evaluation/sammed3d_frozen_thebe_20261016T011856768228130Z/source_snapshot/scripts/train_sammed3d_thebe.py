#!/usr/bin/env python3
"""Prompt-free SAM-Med3D adaptation for Thebe, with test data disabled.

This is an experimental transfer-learning baseline, not the published
Seismic Fault SAM method.  It loads the official SAM-Med3D-turbo ViT-B
checkpoint, freezes the 3D image encoder, and trains only:

* a zero-initialized residual feature adapter at the encoder output;
* the official SAM-Med3D mask decoder; and
* the no-mask prompt embedding used for prompt-free prediction.

The Thebe reader, normalization, split, patch sampling, masked metric code,
and validation-only selection are imported from the installed clean R100
trainer so that the data protocol is shared exactly.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import random
import subprocess
import sys
import time
import types
from dataclasses import asdict
from pathlib import Path

import numpy as np
import torch
from torch import nn
from torch.nn import functional as F


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = PROJECT_ROOT / "scripts"
SAMMED3D_ROOT = PROJECT_ROOT / "external" / "SAM-Med3D"
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(SAMMED3D_ROOT))

try:
    import train_r100_fp16_clean as r100
except Exception as exc:  # pragma: no cover - server integration guard
    raise RuntimeError(
        "Cannot import scripts/train_r100_fp16_clean.py. Install this kit in "
        "the same project where the clean R100 trainer is installed."
    ) from exc

try:
    # Load only the required 3D package and avoid optional 2D torchvision code.
    package = types.ModuleType("segment_anything")
    package.__path__ = [str(SAMMED3D_ROOT / "segment_anything")]
    package.__package__ = "segment_anything"
    sys.modules["segment_anything"] = package
    from segment_anything.build_sam3D import sam_model_registry3D
except Exception as exc:  # pragma: no cover - server integration guard
    raise RuntimeError(
        "Cannot import the SAM-Med3D 3D implementation."
    ) from exc


SIZE = 128
BINS = 2048
DEFAULT_EPOCHS = 100
DEFAULT_TRAIN_PATCHES = 360
DEFAULT_VAL_PATCHES = 128
GRAD_ACCUMULATION = 2
LEARNING_RATE = 1e-4
EXPECTED_SAM_COMMIT = "f3de1fa10da98e46f49f176773d2b1e306ba131f"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json_atomic(path: Path, value) -> None:
    temporary = path.with_suffix(path.suffix + ".part")
    temporary.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")
    temporary.replace(path)


def sam_source_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "-C", str(SAMMED3D_ROOT), "rev-parse", "HEAD"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        return "not-found"


def checkpoint_state(path: Path) -> dict[str, torch.Tensor]:
    # weights_only avoids executing arbitrary objects from a downloaded file.
    # Official training checkpoints may contain an argparse.Namespace. It is a
    # passive data container and is explicitly allowlisted without enabling a
    # general unsafe pickle load.
    with torch.serialization.safe_globals([argparse.Namespace]):
        payload = torch.load(path, map_location="cpu", weights_only=True)
    if not isinstance(payload, dict):
        raise RuntimeError("SAM-Med3D checkpoint is not a dictionary")
    state = payload.get("model_state_dict", payload)
    if not isinstance(state, dict) or not state:
        raise RuntimeError("SAM-Med3D checkpoint has no model_state_dict")
    if not all(isinstance(key, str) and torch.is_tensor(value) for key, value in state.items()):
        raise RuntimeError("SAM-Med3D model_state_dict contains non-tensor entries")
    if all(key.startswith("module.") for key in state):
        state = {key.removeprefix("module."): value for key, value in state.items()}
    return state


class ResidualFeatureAdapter(nn.Module):
    """Small trainable seismic adapter on the frozen 8x8x8 ViT feature grid."""

    def __init__(self, channels: int = 384, bottleneck: int = 96) -> None:
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv3d(channels, bottleneck, kernel_size=1, bias=False),
            nn.GroupNorm(8, bottleneck),
            nn.GELU(),
            nn.Conv3d(bottleneck, channels, kernel_size=1, bias=False),
        )
        nn.init.zeros_(self.net[-1].weight)

    def forward(self, features: torch.Tensor) -> torch.Tensor:
        return features + self.net(features)


class PromptFreeSAMMed3D(nn.Module):
    """Frozen 3D ViT encoder plus adapter and automatic mask decoder."""

    def __init__(self, checkpoint: Path) -> None:
        super().__init__()
        self.sam = sam_model_registry3D["vit_b_ori"](checkpoint=None)
        state = checkpoint_state(checkpoint)
        incompatible = self.sam.load_state_dict(state, strict=False)
        if incompatible.missing_keys or incompatible.unexpected_keys:
            raise RuntimeError(
                "Checkpoint/model mismatch. "
                f"missing={incompatible.missing_keys[:10]} "
                f"unexpected={incompatible.unexpected_keys[:10]}"
            )

        for parameter in self.sam.parameters():
            parameter.requires_grad_(False)
        for parameter in self.sam.mask_decoder.parameters():
            parameter.requires_grad_(True)
        self.sam.prompt_encoder.no_mask_embed.weight.requires_grad_(True)
        self.adapter = ResidualFeatureAdapter()
        self.sam.image_encoder.eval()

    def train(self, mode: bool = True):
        super().train(mode)
        # A frozen backbone must not change behavior when the decoder trains.
        self.sam.image_encoder.eval()
        return self

    def forward(self, seismic: torch.Tensor) -> torch.Tensor:
        if seismic.ndim != 5 or seismic.shape[1:] != (1, SIZE, SIZE, SIZE):
            raise RuntimeError(f"Expected Bx1x128x128x128, got {tuple(seismic.shape)}")
        # No encoder activation graph is retained: the backbone is truly frozen.
        with torch.no_grad():
            image_embedding = self.sam.image_encoder(seismic)
        image_embedding = self.adapter(image_embedding.detach())
        sparse, dense = self.sam.prompt_encoder(points=None, boxes=None, masks=None)
        batch = seismic.shape[0]
        if batch != 1:
            sparse = sparse.expand(batch, -1, -1)
            dense = dense.expand(batch, -1, -1, -1, -1)
        low_res_logits, _ = self.sam.mask_decoder(
            image_embeddings=image_embedding,
            image_pe=self.sam.prompt_encoder.get_dense_pe(),
            sparse_prompt_embeddings=sparse,
            dense_prompt_embeddings=dense,
            multimask_output=False,
        )
        return F.interpolate(
            low_res_logits,
            size=(SIZE, SIZE, SIZE),
            mode="trilinear",
            align_corners=False,
        )

    def trainable_state_dict(self) -> dict[str, torch.Tensor]:
        prefixes = (
            "adapter.",
            "sam.mask_decoder.",
            "sam.prompt_encoder.no_mask_embed.",
        )
        return {
            name: value.detach().cpu()
            for name, value in self.state_dict().items()
            if name.startswith(prefixes)
        }

    def load_trainable_state_dict(self, state: dict[str, torch.Tensor]) -> None:
        current = self.state_dict()
        unknown = sorted(set(state) - set(current))
        if unknown:
            raise RuntimeError(f"Unknown trainable checkpoint keys: {unknown[:10]}")
        current.update(state)
        self.load_state_dict(current, strict=True)


def parameter_counts(model: nn.Module) -> tuple[int, int]:
    total = sum(parameter.numel() for parameter in model.parameters())
    trainable = sum(parameter.numel() for parameter in model.parameters() if parameter.requires_grad)
    return total, trainable


def make_readers(root: Path):
    train_paths = r100.split_paths(root, "train", 9)
    val_paths = r100.split_paths(root, "val", 2)
    if len({path.resolve() for path in train_paths + val_paths}) != 11:
        raise RuntimeError("Training and validation files overlap")
    train_reader = r100.ConcatenatedThebe(train_paths)
    val_reader = r100.ConcatenatedThebe(val_paths)
    if train_reader.shape != (900, 3174, 1537):
        raise RuntimeError(f"Unexpected training shape: {train_reader.shape}")
    if val_reader.shape != (200, 3174, 1537):
        raise RuntimeError(f"Unexpected validation shape: {val_reader.shape}")
    return train_paths, val_paths, train_reader, val_reader


def trainable_finite(model: PromptFreeSAMMed3D) -> None:
    r100.assert_finite_tree(model.trainable_state_dict(), "trainable_model")


def save_checkpoint(
    path: Path,
    model: PromptFreeSAMMed3D,
    optimizer,
    scaler,
    rng: random.Random,
    epoch: int,
    metrics: dict,
) -> None:
    trainable_finite(model)
    r100.assert_finite_tree(optimizer.state_dict(), "optimizer")
    r100.assert_finite_tree(metrics, "validation_metrics")
    temporary = path.with_suffix(path.suffix + ".part")
    torch.save(
        {
            "epoch": epoch,
            "trainable_model": model.trainable_state_dict(),
            "optimizer": optimizer.state_dict(),
            "scaler": scaler.state_dict(),
            "validation_metrics": metrics,
            "python_rng": rng.getstate(),
            "torch_rng": torch.get_rng_state(),
            "cuda_rng": torch.cuda.get_rng_state_all(),
        },
        temporary,
    )
    temporary.replace(path)


def cpu_preflight(data_root: Path, checkpoint: Path) -> None:
    train_paths, val_paths, train_reader, val_reader = make_readers(data_root)
    try:
        source_commit = sam_source_commit()
        if source_commit != EXPECTED_SAM_COMMIT:
            raise RuntimeError(
                f"SAM-Med3D source changed: expected {EXPECTED_SAM_COMMIT}, got {source_commit}"
            )
        model = PromptFreeSAMMed3D(checkpoint)
        total, trainable = parameter_counts(model)
        all_val, subset = r100.fixed_validation_subset(val_reader.shape, 128, 1042)
        trainable_names = [
            name for name, parameter in model.named_parameters() if parameter.requires_grad
        ]
        if any(name.startswith("sam.image_encoder.") for name in trainable_names):
            raise RuntimeError("Image encoder was not frozen")
        print(json.dumps({
            "status": "cpu_preflight_pass",
            "model": "SAM-Med3D-turbo vit_b_ori, prompt-free",
            "sam_source_commit": source_commit,
            "checkpoint": str(checkpoint),
            "checkpoint_sha256": sha256_file(checkpoint),
            "parameters_total": total,
            "parameters_trainable": trainable,
            "image_encoder_frozen": True,
            "trainable_components": [
                "residual feature adapter",
                "SAM-Med3D mask decoder",
                "no-mask prompt embedding",
            ],
            "train_files": [str(path) for path in train_paths],
            "validation_files": [str(path) for path in val_paths],
            "train_shape": train_reader.shape,
            "validation_shape": val_reader.shape,
            "validation_patches": len(subset),
            "full_validation_patches": len(all_val),
            "test_files_opened": False,
            "gpu_executed": False,
        }, indent=2), flush=True)
    finally:
        train_reader.close()
        val_reader.close()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--thebe-root", type=Path, default=Path("data/processed/thebe_h5"))
    parser.add_argument(
        "--checkpoint",
        type=Path,
        default=Path("external/SAM-Med3D/ckpt/sam_med3d_turbo.pth"),
    )
    parser.add_argument("--run-dir", type=Path)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--validation-seed", type=int, default=1042)
    parser.add_argument("--epochs", type=int, default=DEFAULT_EPOCHS)
    parser.add_argument("--train-patches", type=int, default=DEFAULT_TRAIN_PATCHES)
    parser.add_argument("--validation-patches", type=int, default=DEFAULT_VAL_PATCHES)
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()

    if not args.checkpoint.is_file():
        raise RuntimeError(f"Missing checkpoint: {args.checkpoint}")
    if args.check_only:
        cpu_preflight(args.thebe_root, args.checkpoint)
        return
    if args.run_dir is None:
        parser.error("--run-dir is required unless --check-only is used")
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA GPU is required for smoke/full execution")

    epochs = 1 if args.smoke else args.epochs
    train_patches = 18 if args.smoke else args.train_patches
    validation_patches = 2 if args.smoke else args.validation_patches
    if epochs <= 0 or train_patches <= 0 or train_patches % 18:
        parser.error("epochs must be positive and train-patches a positive multiple of 18")

    torch.cuda.reset_peak_memory_stats()
    free_gpu, _ = torch.cuda.mem_get_info()
    if free_gpu < 10 * 1024**3:
        raise RuntimeError(f"Need at least 10 GiB free GPU memory; found {free_gpu/1024**3:.1f}")

    train_paths, val_paths, train_reader, val_reader = make_readers(args.thebe_root)
    try:
        r100.baseline.seed_everything(args.seed)
        rng = random.Random(args.seed)
        device = torch.device("cuda")
        model = PromptFreeSAMMed3D(args.checkpoint).to(device)
        total_parameters, trainable_parameters = parameter_counts(model)
        optimizer = torch.optim.Adam(
            [parameter for parameter in model.parameters() if parameter.requires_grad],
            lr=LEARNING_RATE,
        )
        scaler = torch.amp.GradScaler("cuda", enabled=True)
        all_val, val_subset = r100.fixed_validation_subset(
            val_reader.shape, validation_patches, args.validation_seed
        )

        config = {
            "experiment": "SAM-Med3D-turbo_prompt-free_Thebe",
            "claim": "experimental adaptation; not Seismic Fault SAM",
            "seed": args.seed,
            "model": "SAM-Med3D vit_b_ori",
            "sam_source_commit": sam_source_commit(),
            "checkpoint": str(args.checkpoint),
            "checkpoint_sha256": sha256_file(args.checkpoint),
            "image_encoder_frozen": True,
            "trainable_components": [
                "zero-initialized residual 384-96-384 feature adapter",
                "official SAM-Med3D mask decoder",
                "no-mask prompt embedding",
            ],
            "prompt_policy": "no points, boxes, ground-truth prompts, or mask prompts",
            "parameters_total": total_parameters,
            "parameters_trainable": trainable_parameters,
            "train_files": [str(path) for path in train_paths],
            "validation_files": [str(path) for path in val_paths],
            "test_files_read": False,
            "train_shape": train_reader.shape,
            "validation_shape": val_reader.shape,
            "patch_size": SIZE,
            "epochs": epochs,
            "train_patches_per_epoch": train_patches,
            "validation_patches_per_epoch": len(val_subset),
            "full_validation_patches": len(all_val),
            "normalization": "R100 per-patch z-score over observed nonzero voxels; axis reversal",
            "validity": "raw seismic != 0; masked BCE and masked metrics",
            "loss": "ordinary BCE over observed voxels (same as R100)",
            "optimizer": "Adam",
            "learning_rate": LEARNING_RATE,
            "precision": "float16 autocast with GradScaler",
            "gradient_accumulation": GRAD_ACCUMULATION,
            "checkpoint_selection": "highest PR-AUC on fixed validation subset",
            "validation_subset_coordinates": val_subset,
            "smoke": args.smoke,
        }
        protocol_hash = hashlib.sha256(
            json.dumps({k: v for k, v in config.items() if k != "seed"}, sort_keys=True).encode()
        ).hexdigest()
        config["protocol_hash"] = protocol_hash

        history: list[dict] = []
        if args.resume:
            if not args.run_dir.is_dir():
                raise RuntimeError("Resume directory does not exist")
            saved_config = json.loads((args.run_dir / "run_config.json").read_text())
            if saved_config != json.loads(json.dumps(config)):
                raise RuntimeError("Saved configuration differs; refusing incompatible resume")
            last = torch.load(args.run_dir / "last.pt", map_location="cpu", weights_only=False)
            model.load_trainable_state_dict(last["trainable_model"])
            optimizer.load_state_dict(last["optimizer"])
            scaler.load_state_dict(last["scaler"])
            rng.setstate(last["python_rng"])
            torch.set_rng_state(last["torch_rng"])
            torch.cuda.set_rng_state_all(last["cuda_rng"])
            with (args.run_dir / "history.csv").open(newline="") as handle:
                history = list(csv.DictReader(handle))
            first_epoch = int(last["epoch"]) + 1
            best_saved = torch.load(
                args.run_dir / "best.pt", map_location="cpu", weights_only=False
            )
            best_score = float(best_saved["validation_metrics"]["pr_auc_approx"])
            print(f"RESUME PASS: continuing at epoch {first_epoch}", flush=True)
        else:
            if args.run_dir.exists():
                raise RuntimeError(f"Run directory already exists: {args.run_dir}")
            args.run_dir.mkdir(parents=True)
            write_json_atomic(args.run_dir / "run_config.json", config)
            first_epoch = 1
            best_score = -1.0
            print(
                "PREFLIGHT PASS: frozen pretrained 3D ViT; prompt-free adapter/decoder; "
                "Thebe train+validation only",
                flush=True,
            )

        print(
            f"parameters_total={total_parameters} trainable={trainable_parameters} "
            f"train_shape={train_reader.shape} val_shape={val_reader.shape}",
            flush=True,
        )

        for epoch in range(first_epoch, epochs + 1):
            started = time.time()
            model.train()
            optimizer.zero_grad(set_to_none=True)
            running_loss = 0.0
            skipped_candidates = 0
            for step in range(1, train_patches + 1):
                file_index = (step - 1) // (train_patches // len(train_paths))
                for _ in range(30):
                    x0 = train_reader.offsets[file_index] + rng.randrange(
                        train_reader.lengths[file_index]
                    )
                    y0 = rng.randrange(train_reader.shape[1] - SIZE + 1)
                    z0 = rng.randrange(train_reader.shape[2] - SIZE + 1)
                    x, target, mask, _, observed, _, constant = r100.read_patch(
                        train_reader, (x0, y0, z0)
                    )
                    if not constant and observed >= int(0.05 * SIZE**3):
                        break
                    skipped_candidates += 1
                else:
                    raise RuntimeError(f"Unable to sample observed data from {train_paths[file_index]}")

                if rng.randrange(2):
                    x, target, mask = x.flip(-3), target.flip(-3), mask.flip(-3)
                x, target, mask = x.to(device), target.to(device), mask.to(device)
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
                if step % 6 == 0 or step == train_patches:
                    print(
                        f"epoch={epoch}/{epochs} train_patch={step}/{train_patches} "
                        f"loss={float(loss):.6f}",
                        flush=True,
                    )

            val_histogram, _, coverage = r100.evaluate(
                model, val_reader, val_subset, device
            )
            metrics = asdict(val_histogram.metrics(0.5))
            r100.assert_finite_tree(metrics, "validation_metrics")
            row = {
                "epoch": epoch,
                "train_loss": running_loss / train_patches,
                "train_patches": train_patches,
                "resampled_no_data_candidates": skipped_candidates,
                "seconds": time.time() - started,
                **{f"val_{key}": value for key, value in metrics.items()},
            }
            history.append(row)
            r100.baseline.write_history(args.run_dir / "history.csv", history)
            save_checkpoint(
                args.run_dir / "last.pt", model, optimizer, scaler, rng, epoch, metrics
            )
            if metrics["pr_auc_approx"] > best_score:
                best_score = metrics["pr_auc_approx"]
                save_checkpoint(
                    args.run_dir / "best.pt", model, optimizer, scaler, rng, epoch, metrics
                )
            print(
                f"epoch={epoch:03d}/{epochs} loss={row['train_loss']:.6f} "
                f"val_dice={metrics['dice']:.6f} "
                f"val_pr_auc={metrics['pr_auc_approx']:.6f} "
                f"minutes={row['seconds']/60:.2f}",
                flush=True,
            )

        best = torch.load(args.run_dir / "best.pt", map_location="cpu", weights_only=False)
        model.load_trainable_state_dict(best["trainable_model"])
        print(f"BEST EPOCH: {best['epoch']}; full validation begins", flush=True)
        final_coords = val_subset if args.smoke else all_val
        histogram, _, coverage = r100.evaluate(model, val_reader, final_coords, device)
        if not args.smoke and coverage["raw_voxels"] != math.prod(val_reader.shape):
            raise RuntimeError("Incomplete full-validation coverage")
        threshold = histogram.best_dice_threshold()
        full_metrics = asdict(histogram.metrics(threshold))
        selection = {
            "best_epoch": int(best["epoch"]),
            "threshold": threshold,
            "threshold_source": "smoke subset" if args.smoke else "complete validation volume",
            "full_validation": full_metrics,
            "full_validation_coverage": coverage,
            "test_files_read": False,
        }
        write_json_atomic(args.run_dir / "validation_selection.json", selection)
        status = {
            "status": "smoke_complete" if args.smoke else "validation_only_complete",
            "seed": args.seed,
            "epochs_completed": len(history),
            "best_epoch": int(best["epoch"]),
            "threshold": float(threshold),
            "test_files_read": False,
            "peak_gpu_allocated_gib": torch.cuda.max_memory_allocated() / 1024**3,
            "peak_gpu_reserved_gib": torch.cuda.max_memory_reserved() / 1024**3,
        }
        write_json_atomic(args.run_dir / "status.json", status)
        print(
            f"SAMMED3D THEBE {'SMOKE' if args.smoke else 'VALIDATION-ONLY'} COMPLETE "
            f"seed={args.seed} best_epoch={best['epoch']} threshold={threshold:.6f}",
            flush=True,
        )
    finally:
        train_reader.close()
        val_reader.close()


if __name__ == "__main__":
    main()
