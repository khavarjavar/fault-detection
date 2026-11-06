#!/usr/bin/env python3
"""Production denoising pretraining for the Opunake+Kahu Attention3D variant.

Published settings retained here are 64-cube inputs, Gaussian corruption at
5--30% of patch RMS, 50 epochs, learning rate 1e-3, and effective batch 16.
The public release omits crop bounds, batches per pretraining epoch, optimizer
details, and a compatible training entry point. Those local choices are saved
explicitly in ``run_config.json`` and must not be described as author-exact.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import random
import signal
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import torch
from torch.nn import functional as F
from torch.nn.attention import SDPBackend, sdpa_kernel

from train_paper_attention3d_thebe_bf16 import load_paper_code, save_atomic


PATCH = 64
STOP_REQUESTED = False


def sha256_file(path: Path, block_size: int = 8 * 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(block_size):
            digest.update(block)
    return digest.hexdigest()


def atomic_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".part")
    temporary.write_text(json.dumps(payload, indent=2, allow_nan=False) + "\n")
    os.replace(temporary, path)


def append_csv(path: Path, row: dict) -> None:
    exists = path.exists()
    with path.open("a", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(row))
        if not exists:
            writer.writeheader()
        writer.writerow(row)


def require_finite(tensor: torch.Tensor, label: str) -> None:
    if not bool(torch.isfinite(tensor).all().item()):
        raise FloatingPointError(f"Nonfinite {label}")


class SurveyStore:
    def __init__(self, root: Path, survey_id: str) -> None:
        self.id = survey_id
        self.directory = root / survey_id
        self.manifest = json.loads((self.directory / "manifest.json").read_text())
        self.volume = np.load(self.directory / "volume_float32.npy", mmap_mode="r")
        self.train = np.load(self.directory / "train_coordinates.npy", mmap_mode="r")
        self.validation = np.load(self.directory / "validation_coordinates.npy", mmap_mode="r")
        stats = self.manifest["amplitudes_present_traces"]
        self.mean = float(stats["mean"])
        self.std = float(stats["standard_deviation"])
        if self.volume.dtype != np.float32 or self.std <= 0:
            raise RuntimeError(f"Invalid converted survey: {survey_id}")

    def cube(self, coordinate: np.ndarray) -> torch.Tensor:
        inline, crossline, sample = map(int, coordinate)
        raw = np.asarray(
            self.volume[
                inline:inline + PATCH,
                crossline:crossline + PATCH,
                sample:sample + PATCH,
            ],
            dtype=np.float32,
        )
        if raw.shape != (PATCH, PATCH, PATCH) or not np.isfinite(raw).all():
            raise RuntimeError(f"Invalid {self.id} cube at {tuple(coordinate)}")
        normalized = (raw - self.mean) / self.std
        if not np.isfinite(normalized).all():
            raise RuntimeError(f"Invalid normalized {self.id} cube")
        return torch.from_numpy(np.ascontiguousarray(normalized[None, None]))


def build_schedule(
    stores: list[SurveyStore],
    epochs: int,
    train_patches_per_epoch: int,
    validation_patches_per_survey: int,
    seed: int,
) -> tuple[np.ndarray, np.ndarray]:
    survey_count = len(stores)
    if train_patches_per_epoch % survey_count:
        raise ValueError("Training patches per epoch must divide evenly across surveys")
    per_survey_total = epochs * train_patches_per_epoch // survey_count
    train_rows = []
    validation_rows = []
    for survey_index, store in enumerate(stores):
        if per_survey_total > len(store.train):
            raise ValueError(
                f"Requested {per_survey_total} unique {store.id} training cubes, "
                f"but only {len(store.train)} exist"
            )
        if validation_patches_per_survey > len(store.validation):
            raise ValueError(f"Too many validation cubes requested for {store.id}")
        rng = np.random.default_rng(seed + survey_index * 1_000_003)
        chosen = np.asarray(store.train[rng.permutation(len(store.train))[:per_survey_total]])
        train_rows.append(
            np.column_stack((np.full(per_survey_total, survey_index, np.int32), chosen))
        )
        validation_chosen = np.asarray(
            store.validation[
                rng.permutation(len(store.validation))[:validation_patches_per_survey]
            ]
        )
        validation_rows.append(
            np.column_stack(
                (
                    np.full(validation_patches_per_survey, survey_index, np.int32),
                    validation_chosen,
                )
            )
        )

    # Interleave surveys within each epoch while retaining unique coordinates.
    per_survey_epoch = train_patches_per_epoch // survey_count
    schedule = np.empty((epochs, train_patches_per_epoch, 4), dtype=np.int32)
    for epoch in range(epochs):
        chunks = [
            rows[epoch * per_survey_epoch:(epoch + 1) * per_survey_epoch]
            for rows in train_rows
        ]
        interleaved = np.stack(chunks, axis=1).reshape(train_patches_per_epoch, 4)
        epoch_rng = np.random.default_rng(seed + 17_171 * (epoch + 1))
        schedule[epoch] = interleaved[epoch_rng.permutation(train_patches_per_epoch)]
    validation = np.concatenate(validation_rows, axis=0)
    return schedule, validation


def load_or_create_schedule(
    run_dir: Path,
    stores: list[SurveyStore],
    epochs: int,
    train_patches_per_epoch: int,
    validation_patches_per_survey: int,
    seed: int,
) -> tuple[np.ndarray, np.ndarray]:
    train_path = run_dir / "train_schedule.npy"
    validation_path = run_dir / "validation_schedule.npy"
    if train_path.exists() or validation_path.exists():
        if not train_path.exists() or not validation_path.exists():
            raise RuntimeError("Incomplete saved coordinate schedule")
        train = np.load(train_path)
        validation = np.load(validation_path)
    else:
        train, validation = build_schedule(
            stores, epochs, train_patches_per_epoch, validation_patches_per_survey, seed
        )
        np.save(train_path, train, allow_pickle=False)
        np.save(validation_path, validation, allow_pickle=False)
    expected = (epochs, train_patches_per_epoch, 4)
    if train.shape != expected or validation.shape != (
        len(stores) * validation_patches_per_survey,
        4,
    ):
        raise RuntimeError("Saved coordinate schedule conflicts with run arguments")
    return train, validation


def clean_cube(stores: list[SurveyStore], record: np.ndarray) -> torch.Tensor:
    return stores[int(record[0])].cube(record[1:])


def corrupt(
    clean: torch.Tensor, generator: torch.Generator
) -> tuple[torch.Tensor, float, float]:
    rms = clean.float().square().mean().sqrt()
    fraction = float(torch.empty((), device=clean.device).uniform_(0.05, 0.30, generator=generator))
    sigma = rms * fraction
    noise = torch.randn(
        clean.shape, dtype=clean.dtype, device=clean.device, generator=generator
    ) * sigma
    return clean + noise, fraction, float(sigma)


def attention_forward(model: torch.nn.Module, value: torch.Tensor) -> torch.Tensor:
    with sdpa_kernel([SDPBackend.FLASH_ATTENTION, SDPBackend.EFFICIENT_ATTENTION]):
        with torch.autocast("cuda", dtype=torch.bfloat16):
            prediction = model(value)
    prediction = prediction.float()
    require_finite(prediction, "model prediction")
    return prediction


@torch.inference_mode()
def evaluate(
    model: torch.nn.Module,
    stores: list[SurveyStore],
    schedule: np.ndarray,
    seed: int,
) -> dict:
    model.eval()
    generator = torch.Generator(device="cuda").manual_seed(seed)
    network_squared_error = 0.0
    identity_squared_error = 0.0
    voxel_count = 0
    per_survey: dict[str, list[float]] = {store.id: [0.0, 0.0, 0.0] for store in stores}
    fractions = []
    for record in schedule:
        clean = clean_cube(stores, record).pin_memory().cuda(non_blocking=True)
        noisy, fraction, _ = corrupt(clean, generator)
        prediction = attention_forward(model, noisy)
        network_sse = float(F.mse_loss(prediction, clean, reduction="sum"))
        identity_sse = float(F.mse_loss(noisy, clean, reduction="sum"))
        count = clean.numel()
        network_squared_error += network_sse
        identity_squared_error += identity_sse
        voxel_count += count
        bucket = per_survey[stores[int(record[0])].id]
        bucket[0] += network_sse
        bucket[1] += identity_sse
        bucket[2] += count
        fractions.append(fraction)
    network_mse = network_squared_error / voxel_count
    identity_mse = identity_squared_error / voxel_count
    return {
        "network_mse": network_mse,
        "noisy_identity_mse": identity_mse,
        "identity_minus_network_mse": identity_mse - network_mse,
        "network_to_identity_mse_ratio": network_mse / identity_mse,
        "patches": int(len(schedule)),
        "voxels": voxel_count,
        "noise_fraction_range_realized": [min(fractions), max(fractions)],
        "per_survey": {
            key: {
                "network_mse": values[0] / values[2],
                "noisy_identity_mse": values[1] / values[2],
                "patches": int(np.count_nonzero(schedule[:, 0] == index)),
            }
            for index, (key, values) in enumerate(per_survey.items())
            if values[2] > 0
        },
    }


def setup_gpu(memory_fraction: float) -> None:
    if not torch.cuda.is_available() or not torch.cuda.is_bf16_supported():
        raise RuntimeError("A BF16-capable CUDA GPU is required")
    if not 0 < memory_fraction <= 1:
        raise ValueError("memory fraction must be in (0,1]")
    torch.cuda.set_per_process_memory_fraction(memory_fraction)
    torch.backends.cuda.enable_math_sdp(False)
    torch.backends.cudnn.benchmark = False
    torch.set_num_threads(2)


def configure_run(args, stores, train_schedule, validation_schedule, paper_source):
    return {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "experiment": "attention3d_opunake_kahu_denoising_pretraining_variant",
        "paper_doi": "10.1038/s41598-026-54829-x",
        "paper_exact_reproduction": False,
        "claim_limit": "Kerry is absent; author crop bounds, sampler, exact pretraining optimizer details, and compatible denoising checkpoint/source are unpublished.",
        "surveys": [store.id for store in stores],
        "kerry_included": False,
        "paper_source": str(paper_source),
        "paper_source_sha256": sha256_file(paper_source),
        "paper_source_commit": "2a3d69a5d99dfc191508cbceea3db3b95242f216",
        "trainer_sha256": sha256_file(Path(__file__)),
        "data_manifest": str(args.data_root / "manifest.json"),
        "data_manifest_sha256": sha256_file(args.data_root / "manifest.json"),
        "patch_shape": [64, 64, 64],
        "stride_used_to_form_manifest": [32, 32, 32],
        "normalization": "per-survey global z-score using all finite samples on present traces",
        "missing_bins": "excluded by full-valid 64x64 spatial footprint requirement",
        "corruption": "zero-mean Gaussian; sigma uniform 0.05-0.30 times normalized clean patch RMS",
        "target": "normalized original field patch",
        "loss": "voxelwise mean squared error",
        "architecture": "released 45,001,057-parameter segmentation Attention3DUNet used for both pretraining and transfer; output head reinitialized for segmentation",
        "published_defaults_retained": {
            "epochs": 50,
            "learning_rate": 0.001,
            "effective_batch": 16,
        },
        "local_single_gpu_adaptation": {
            "physical_batch": 1,
            "gradient_accumulation": args.accumulate,
            "precision": "BF16 forward; FP32 loss, parameters, optimizer",
            "optimizer": "AdamW",
            "weight_decay": args.weight_decay,
            "train_patches_per_epoch": args.train_patches_per_epoch,
            "training_schedule": "balanced surveys, unique coordinates across all 50 epochs",
            "validation_patches_per_survey": args.validation_patches_per_survey,
            "validation_interval_epochs": args.validation_interval,
            "scheduler": "none; pretraining scheduler was not published",
        },
        "epochs": args.epochs,
        "seed": args.seed,
        "total_training_patches": int(train_schedule.shape[0] * train_schedule.shape[1]),
        "total_optimizer_updates": int(
            train_schedule.shape[0] * math.ceil(train_schedule.shape[1] / args.accumulate)
        ),
        "validation_patches": int(validation_schedule.shape[0]),
        "test_or_thebe_data_read": False,
    }


def preflight(args, paper, stores, train_schedule, validation_schedule) -> None:
    model = paper.Attention3DUNet().cuda()
    parameter_count = sum(parameter.numel() for parameter in model.parameters())
    if parameter_count != 45_001_057:
        raise RuntimeError(f"Unexpected model parameter count: {parameter_count}")
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.learning_rate, weight_decay=args.weight_decay)
    generator = torch.Generator(device="cuda").manual_seed(args.seed + 8_001)
    optimizer.zero_grad(set_to_none=True)
    rows = []
    torch.cuda.reset_peak_memory_stats()
    for index in range(2):
        clean = clean_cube(stores, train_schedule[0, index]).pin_memory().cuda(non_blocking=True)
        noisy, fraction, sigma = corrupt(clean, generator)
        start = time.monotonic()
        prediction = attention_forward(model, noisy)
        loss = F.mse_loss(prediction, clean)
        require_finite(loss, "preflight loss")
        loss.backward()
        grad_norm = torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        require_finite(grad_norm, "preflight gradient norm")
        optimizer.step()
        optimizer.zero_grad(set_to_none=True)
        torch.cuda.synchronize()
        rows.append(
            {
                "step": index + 1,
                "loss": float(loss),
                "noise_fraction": fraction,
                "noise_sigma_normalized": sigma,
                "gradient_norm": float(grad_norm),
                "seconds": time.monotonic() - start,
            }
        )
        print(json.dumps(rows[-1]), flush=True)
    evaluation = evaluate(model, stores, validation_schedule[:4], args.seed + 91_001)
    result = {
        "status": "passed",
        "parameter_count": parameter_count,
        "steps": rows,
        "four_patch_validation": evaluation,
        "peak_allocated_bytes": torch.cuda.max_memory_allocated(),
        "peak_reserved_bytes": torch.cuda.max_memory_reserved(),
        "gpu": torch.cuda.get_device_name(),
        "torch": torch.__version__,
        "test_or_thebe_data_read": False,
    }
    atomic_json(args.run_dir / "gpu_preflight.json", result)
    del model, optimizer
    torch.cuda.empty_cache()


def train(args, paper, stores, train_schedule, validation_schedule, config) -> None:
    config_path = args.run_dir / "run_config.json"
    if config_path.exists():
        prior = json.loads(config_path.read_text())
        # Timestamps and trainer hashes may differ only if somebody changed code;
        # changing code invalidates resume rather than silently mixing executions.
        for key in ("trainer_sha256", "data_manifest_sha256", "epochs", "seed", "total_training_patches"):
            if prior[key] != config[key]:
                raise RuntimeError(f"Run configuration changed at {key}")
        config = prior
    else:
        atomic_json(config_path, config)
    if not (args.run_dir / "gpu_preflight.json").exists():
        raise RuntimeError("Run --phase preflight successfully before --phase train")

    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    torch.cuda.manual_seed_all(args.seed)
    model = paper.Attention3DUNet().cuda()
    optimizer = torch.optim.AdamW(
        model.parameters(), lr=args.learning_rate, weight_decay=args.weight_decay
    )
    last_path = args.run_dir / "last.pt"
    best_path = args.run_dir / "best.pt"
    start_epoch = 0
    best_mse = float("inf")
    if last_path.exists():
        checkpoint = torch.load(last_path, map_location="cpu", weights_only=False)
        if checkpoint["run_config_sha256"] != sha256_file(config_path):
            raise RuntimeError("Checkpoint run configuration hash mismatch")
        model.load_state_dict(checkpoint["model"])
        optimizer.load_state_dict(checkpoint["optimizer"])
        start_epoch = int(checkpoint["next_epoch"])
        best_mse = float(checkpoint["best_validation_mse"])
        random.setstate(checkpoint["python_random_state"])
        np.random.set_state(checkpoint["numpy_random_state"])
        torch.set_rng_state(checkpoint["torch_random_state"])
        torch.cuda.set_rng_state_all(checkpoint["cuda_random_state"])
        print(f"Resuming at epoch {start_epoch + 1}", flush=True)

    history_path = args.run_dir / "history.csv"
    atomic_json(args.run_dir / "state.json", {"status": "running", "next_epoch": start_epoch, "test_or_thebe_data_read": False})
    started = time.monotonic()
    for epoch in range(start_epoch, args.epochs):
        if STOP_REQUESTED:
            break
        model.train()
        optimizer.zero_grad(set_to_none=True)
        generator = torch.Generator(device="cuda").manual_seed(args.seed + 100_003 * (epoch + 1))
        loss_sum = 0.0
        fractions = []
        for patch_index, record in enumerate(train_schedule[epoch]):
            clean = clean_cube(stores, record).pin_memory().cuda(non_blocking=True)
            noisy, fraction, _ = corrupt(clean, generator)
            prediction = attention_forward(model, noisy)
            loss = F.mse_loss(prediction, clean)
            require_finite(loss, "training loss")
            (loss / args.accumulate).backward()
            loss_sum += float(loss.detach())
            fractions.append(fraction)
            should_step = (patch_index + 1) % args.accumulate == 0 or patch_index + 1 == len(train_schedule[epoch])
            if should_step:
                grad_norm = torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
                require_finite(grad_norm, "gradient norm")
                optimizer.step()
                optimizer.zero_grad(set_to_none=True)
            if (patch_index + 1) % 32 == 0:
                print(
                    f"epoch={epoch + 1:02d}/{args.epochs} patch={patch_index + 1}/{len(train_schedule[epoch])} "
                    f"loss={float(loss):.6f}",
                    flush=True,
                )
            if STOP_REQUESTED:
                break

        complete_epoch = not STOP_REQUESTED
        evaluation = None
        if complete_epoch and ((epoch + 1) % args.validation_interval == 0 or epoch == 0 or epoch + 1 == args.epochs):
            evaluation = evaluate(model, stores, validation_schedule, args.seed + 91_001)
            if evaluation["network_mse"] < best_mse:
                best_mse = evaluation["network_mse"]
                save_atomic(
                    best_path,
                    {
                        "model": model.state_dict(),
                        "epoch": epoch + 1,
                        "validation": evaluation,
                        "run_config_sha256": sha256_file(config_path),
                    },
                )

        next_epoch = epoch + 1 if complete_epoch else epoch
        if complete_epoch:
            save_atomic(
                last_path,
                {
                    "model": model.state_dict(),
                    "optimizer": optimizer.state_dict(),
                    "next_epoch": next_epoch,
                    "best_validation_mse": best_mse,
                    "run_config_sha256": sha256_file(config_path),
                    "python_random_state": random.getstate(),
                    "numpy_random_state": np.random.get_state(),
                    "torch_random_state": torch.get_rng_state(),
                    "cuda_random_state": torch.cuda.get_rng_state_all(),
                },
            )
        row = {
            "epoch": epoch + 1,
            "complete": complete_epoch,
            "mean_training_mse": loss_sum / max(1, len(fractions)),
            "validation_mse": "" if evaluation is None else evaluation["network_mse"],
            "identity_validation_mse": "" if evaluation is None else evaluation["noisy_identity_mse"],
            "noise_fraction_min": min(fractions),
            "noise_fraction_max": max(fractions),
            "elapsed_seconds": time.monotonic() - started,
        }
        append_csv(history_path, row)
        atomic_json(
            args.run_dir / "state.json",
            {
                "status": "running" if complete_epoch else "interrupted",
                "next_epoch": next_epoch,
                "best_validation_mse": best_mse,
                "last_epoch": row,
                "test_or_thebe_data_read": False,
            },
        )
        print(json.dumps(row), flush=True)
        if not complete_epoch:
            break

    if not STOP_REQUESTED and start_epoch < args.epochs:
        best_hash = sha256_file(best_path)
        atomic_json(
            args.run_dir / "state.json",
            {
                "status": "complete",
                "next_epoch": args.epochs,
                "best_validation_mse": best_mse,
                "best_checkpoint": str(best_path),
                "best_checkpoint_sha256": best_hash,
                "test_or_thebe_data_read": False,
            },
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", choices=("data-check", "preflight", "train"), required=True)
    parser.add_argument("--data-root", type=Path, default=Path("data/processed/attention3d_nzpam"))
    parser.add_argument("--paper-source", type=Path, default=Path("external/attention3d_paper/fault-detection-global-attention.py"))
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--epochs", type=int, default=50)
    parser.add_argument("--train-patches-per-epoch", type=int, default=352)
    parser.add_argument("--validation-patches-per-survey", type=int, default=32)
    parser.add_argument("--validation-interval", type=int, default=5)
    parser.add_argument("--accumulate", type=int, default=16)
    parser.add_argument("--learning-rate", type=float, default=1e-3)
    parser.add_argument("--weight-decay", type=float, default=1e-4)
    parser.add_argument("--memory-fraction", type=float, default=0.92)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    if args.epochs != 50 or args.learning_rate != 1e-3 or args.accumulate != 16:
        raise ValueError("Published defaults are frozen at 50 epochs, lr=1e-3, effective batch 16")
    if min(args.train_patches_per_epoch, args.validation_patches_per_survey, args.validation_interval) <= 0:
        raise ValueError("Patch counts and validation interval must be positive")
    if args.train_patches_per_epoch % args.accumulate:
        raise ValueError("Training patches per epoch must be divisible by accumulation")

    args.run_dir.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((args.data_root / "manifest.json").read_text())
    if manifest["kerry_included"] or manifest["check_only"]:
        raise RuntimeError("Expected completed two-survey variant manifest")
    stores = [SurveyStore(args.data_root, item["survey"]) for item in manifest["surveys"]]
    train_schedule, validation_schedule = load_or_create_schedule(
        args.run_dir,
        stores,
        args.epochs,
        args.train_patches_per_epoch,
        args.validation_patches_per_survey,
        args.seed,
    )
    config = configure_run(
        args, stores, train_schedule, validation_schedule, args.paper_source
    )
    atomic_json(
        args.run_dir / "data_check.json",
        {
            "status": "passed",
            "train_schedule_shape": list(train_schedule.shape),
            "validation_schedule_shape": list(validation_schedule.shape),
            "train_schedule_sha256": sha256_file(args.run_dir / "train_schedule.npy"),
            "validation_schedule_sha256": sha256_file(args.run_dir / "validation_schedule.npy"),
            "balanced_training_counts": {
                store.id: int(np.count_nonzero(train_schedule[..., 0] == index))
                for index, store in enumerate(stores)
            },
            "unique_training_coordinates": int(
                np.unique(train_schedule.reshape(-1, 4), axis=0).shape[0]
            ),
            "test_or_thebe_data_read": False,
        },
    )
    if args.phase == "data-check":
        print((args.run_dir / "data_check.json").read_text())
        return 0

    setup_gpu(args.memory_fraction)
    paper = load_paper_code(args.paper_source)
    if args.phase == "preflight":
        preflight(args, paper, stores, train_schedule, validation_schedule)
    else:
        train(args, paper, stores, train_schedule, validation_schedule, config)
    return 0


if __name__ == "__main__":
    def request_stop(signum, frame):
        global STOP_REQUESTED
        STOP_REQUESTED = True

    signal.signal(signal.SIGINT, request_stop)
    signal.signal(signal.SIGTERM, request_stop)
    raise SystemExit(main())
