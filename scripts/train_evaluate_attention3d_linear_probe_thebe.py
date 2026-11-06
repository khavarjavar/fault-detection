#!/usr/bin/env python3
"""Frozen-backbone Attention3D linear probe on held-out Thebe data.

The source checkpoint was trained to denoise Opunake and Kahu seismic cubes.
It is therefore not a fault detector by itself.  This program reinitializes
the one-channel output convolution, freezes every pretrained feature tensor,
trains only that output head on Thebe train files, selects a threshold on a
fixed validation sample, freezes the scientific state, and only then opens a
fixed sample from all seven Thebe test files.

This is a representation-transfer screening experiment.  Its 64-cube sampled
metrics are not a replacement for a full-grid fine-tuning result.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import itertools
import json
import math
import os
import random
import re
import sys
import time
import types
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

import h5py
import numpy as np
import torch
from torch.nn import functional as F
from torch.nn.attention import SDPBackend, sdpa_kernel


PATCH = 64
BINS = 2048


def natural_key(path: Path) -> list[object]:
    return [int(part) if part.isdigit() else part.lower()
            for part in re.split(r"(\d+)", path.name)]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(8 * 1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def write_json(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".part")
    temporary.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")
    os.replace(temporary, path)


def save_torch(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".part")
    torch.save(value, temporary)
    os.replace(temporary, path)


def load_paper_code(path: Path):
    if importlib.util.find_spec("tensorboard") is None:
        stub = types.ModuleType("torch.utils.tensorboard")
        stub.SummaryWriter = object
        sys.modules["torch.utils.tensorboard"] = stub
    spec = importlib.util.spec_from_file_location("attention3d_linear_probe_model", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import Attention3D source: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def split_paths(root: Path, role: str, expected: int) -> list[Path]:
    paths = sorted(root.glob(f"{role}*.h5"), key=natural_key)
    wanted = [root / f"{role}{index}.h5" for index in range(1, expected + 1)]
    if paths != wanted or not all(path.is_file() for path in wanted):
        raise RuntimeError(f"Expected exactly {wanted}; found {paths}")
    return paths


def validate_disjoint(path_groups: list[list[Path]]) -> None:
    paths = [path for group in path_groups for path in group]
    if len({path.resolve() for path in paths}) != len(paths):
        raise RuntimeError("Train, validation, and test paths overlap")
    if len({(path.stat().st_dev, path.stat().st_ino) for path in paths}) != len(paths):
        raise RuntimeError("A dataset split contains aliased files")


class ThebeFiles:
    def __init__(self, paths: list[Path]):
        self.paths = paths
        self.handles = [h5py.File(path, "r") for path in paths]
        self.shapes: list[tuple[int, int, int]] = []
        for path, handle in zip(paths, self.handles):
            if "seismic" not in handle or "fault" not in handle:
                raise RuntimeError(f"Missing datasets in {path}")
            shape = tuple(int(x) for x in handle["seismic"].shape)
            if shape != tuple(handle["fault"].shape) or len(shape) != 3:
                raise RuntimeError(f"Misaligned HDF5 datasets in {path}")
            self.shapes.append(shape)

    def close(self) -> None:
        for handle in self.handles:
            handle.close()

    def read(self, file_index: int, origin: tuple[int, int, int]):
        shape = self.shapes[file_index]
        stops = tuple(min(start + PATCH, length) for start, length in zip(origin, shape))
        slices = tuple(slice(start, stop) for start, stop in zip(origin, stops))
        seismic = np.asarray(self.handles[file_index]["seismic"][slices], dtype=np.float32)
        target = np.asarray(self.handles[file_index]["fault"][slices], dtype=np.uint8)
        actual = tuple(stop - start for start, stop in zip(origin, stops))
        if seismic.shape != actual or target.shape != actual:
            raise RuntimeError("HDF5 patch shape mismatch")
        if not np.isfinite(seismic).all() or not np.logical_or(target == 0, target == 1).all():
            raise RuntimeError("Nonfinite seismic or nonbinary label")

        # Use the same raw-nonzero validity rule and per-patch valid-only
        # normalization as the frozen R100/FaultEdgeFormer evaluations.
        valid = seismic != 0.0
        observed = int(valid.sum())
        if not observed:
            return None
        values = seismic[valid]
        std = float(values.std(dtype=np.float64))
        if not math.isfinite(std) or std <= 1e-8:
            return None
        normalized = np.zeros_like(seismic, dtype=np.float32)
        normalized[valid] = (seismic[valid] - values.mean(dtype=np.float64)) / std

        padded_x = np.zeros((PATCH,) * 3, dtype=np.float32)
        padded_y = np.zeros((PATCH,) * 3, dtype=np.float32)
        padded_m = np.zeros((PATCH,) * 3, dtype=np.bool_)
        bounds = tuple(slice(0, length) for length in actual)
        padded_x[bounds] = normalized
        padded_y[bounds] = target
        padded_m[bounds] = valid

        def tensor(array: np.ndarray) -> torch.Tensor:
            return torch.from_numpy(np.ascontiguousarray(array.transpose())[None, None])

        metadata = {
            "file": self.paths[file_index].name,
            "origin": list(origin),
            "actual_shape": list(actual),
            "raw_voxels": int(math.prod(actual)),
            "valid_voxels": observed,
            "positive_voxels": int(np.count_nonzero(target & valid)),
            "positive_labels_excluded": int(np.count_nonzero((target > 0) & ~valid)),
        }
        return tensor(padded_x), tensor(padded_y), tensor(padded_m), metadata


def all_coordinates(files: ThebeFiles) -> list[tuple[int, tuple[int, int, int]]]:
    records = []
    for file_index, shape in enumerate(files.shapes):
        for origin in itertools.product(*(range(0, length, PATCH) for length in shape)):
            records.append((file_index, tuple(int(x) for x in origin)))
    return records


def fixed_uniform_coordinates(files: ThebeFiles, count: int, seed: int):
    all_coords = all_coordinates(files)
    if count < len(files.paths) or count > len(all_coords):
        raise ValueError("Fixed evaluation sample count is invalid")
    rng = random.Random(seed)
    # Guarantee every file occurs, then fill uniformly without replacement.
    selected_indices = set()
    by_file: dict[int, list[int]] = {i: [] for i in range(len(files.paths))}
    for index, (file_index, _) in enumerate(all_coords):
        by_file[file_index].append(index)
    for file_index in range(len(files.paths)):
        selected_indices.add(rng.choice(by_file[file_index]))
    remaining = [index for index in range(len(all_coords)) if index not in selected_indices]
    selected_indices.update(rng.sample(remaining, count - len(selected_indices)))
    return [all_coords[index] for index in sorted(selected_indices)]


def sample_training_patch(files: ThebeFiles, index: int, seed: int):
    rng = np.random.default_rng(seed + index * 1_000_003)
    want_fault = index % 2 == 0
    for _ in range(512 if want_fault else 128):
        file_index = int(rng.integers(len(files.paths)))
        shape = files.shapes[file_index]
        origin = tuple(int(rng.integers(0, max(1, length - PATCH + 1))) for length in shape)
        value = files.read(file_index, origin)
        if value is None:
            continue
        if want_fault and value[3]["positive_voxels"] == 0:
            continue
        return value
    raise RuntimeError(f"Unable to sample training patch {index}")


@dataclass
class Metrics:
    threshold: float
    dice: float
    iou: float
    precision: float
    recall: float
    specificity: float
    balanced_accuracy: float
    accuracy: float
    mcc: float
    pr_auc_approx: float
    roc_auc_approx: float
    tp: int
    fp: int
    fn: int
    tn: int


class Histogram:
    def __init__(self):
        self.positive = np.zeros(BINS, dtype=np.int64)
        self.negative = np.zeros(BINS, dtype=np.int64)

    def update(self, probabilities: torch.Tensor, target: torch.Tensor) -> None:
        index = torch.clamp((probabilities * BINS).long(), 0, BINS - 1)
        truth = target >= 0.5
        self.positive += torch.bincount(index[truth], minlength=BINS).cpu().numpy()
        self.negative += torch.bincount(index[~truth], minlength=BINS).cpu().numpy()

    def curves(self):
        tp = np.cumsum(self.positive[::-1], dtype=np.int64)[::-1]
        fp = np.cumsum(self.negative[::-1], dtype=np.int64)[::-1]
        total_p, total_n = int(self.positive.sum()), int(self.negative.sum())
        fn, tn = total_p - tp, total_n - fp
        return tp, fp, fn, tn

    def best_threshold(self) -> float:
        tp, fp, fn, _ = self.curves()
        denominator = 2 * tp + fp + fn
        dice = np.divide(2 * tp, denominator, out=np.zeros(BINS), where=denominator != 0)
        return int(np.argmax(dice)) / BINS

    def metrics(self, threshold: float) -> Metrics:
        index = min(BINS - 1, max(0, int(threshold * BINS)))
        tp_all, fp_all, fn_all, tn_all = self.curves()
        tp, fp, fn, tn = (int(x[index]) for x in (tp_all, fp_all, fn_all, tn_all))
        precision = tp / max(1, tp + fp)
        recall = tp / max(1, tp + fn)
        specificity = tn / max(1, tn + fp)
        accuracy = (tp + tn) / max(1, tp + fp + fn + tn)
        mcc_den = math.sqrt(max(1, (tp + fp) * (tp + fn) * (tn + fp) * (tn + fn)))
        mcc = (tp * tn - fp * fn) / mcc_den

        # Match faultseg3d_baseline.ProbabilityHistogram exactly: traverse
        # thresholds from the highest probability bin to the lowest, integrate
        # PR as right-endpoint recall increments, and ROC trapezoidally.  This
        # keeps AUC definitions comparable with R100 and FaultEdgeFormer.
        total_p, total_n = max(1, int(self.positive.sum())), max(1, int(self.negative.sum()))
        curve_tp = np.cumsum(self.positive[::-1], dtype=np.int64)
        curve_fp = np.cumsum(self.negative[::-1], dtype=np.int64)
        recall_curve = curve_tp / total_p
        precision_curve = np.divide(
            curve_tp, curve_tp + curve_fp,
            out=np.zeros(BINS, dtype=np.float64), where=(curve_tp + curve_fp) != 0,
        )
        recall_increment = np.diff(np.r_[0.0, recall_curve])
        pr_auc = float(np.sum(recall_increment * precision_curve))
        fpr_curve = curve_fp / total_n
        roc_auc = float(np.trapezoid(np.r_[0.0, recall_curve], np.r_[0.0, fpr_curve]))
        return Metrics(
            threshold=threshold,
            dice=2 * tp / max(1, 2 * tp + fp + fn),
            iou=tp / max(1, tp + fp + fn),
            precision=precision,
            recall=recall,
            specificity=specificity,
            balanced_accuracy=(recall + specificity) / 2,
            accuracy=accuracy,
            mcc=mcc,
            pr_auc_approx=pr_auc,
            roc_auc_approx=roc_auc,
            tp=tp, fp=fp, fn=fn, tn=tn,
        )


def require_finite(value: torch.Tensor, label: str) -> None:
    if not torch.isfinite(value).all().item():
        raise FloatingPointError(f"Nonfinite {label}")


def forward(model, value):
    with sdpa_kernel([SDPBackend.FLASH_ATTENTION, SDPBackend.EFFICIENT_ATTENTION]):
        with torch.autocast("cuda", dtype=torch.bfloat16):
            output = model(value)
    require_finite(output, "Attention3D output")
    return output.float()


def initialize_model(paper, checkpoint: dict, seed: int):
    torch.manual_seed(seed)
    model = paper.Attention3DUNet()
    expected = model.state_dict()
    source = checkpoint["model"]
    if set(source) != set(expected):
        raise RuntimeError("Pretraining and segmentation model state schemas differ")
    head = {name for name in expected if name.startswith("out_conv.")}
    for name in expected:
        if source[name].shape != expected[name].shape:
            raise RuntimeError(f"Checkpoint shape mismatch: {name}")
        require_finite(source[name], f"checkpoint {name}")
    fresh_head = {name: expected[name].clone() for name in head}
    loaded = model.load_state_dict({name: source[name] for name in expected if name not in head}, strict=False)
    if set(loaded.missing_keys) != head or loaded.unexpected_keys:
        raise RuntimeError(f"Feature transfer failed: {loaded}")
    after = model.state_dict()
    if not all(torch.equal(after[name], source[name]) for name in expected if name not in head):
        raise RuntimeError("Transferred feature tensor differs")
    if not all(torch.equal(after[name], fresh_head[name]) for name in head):
        raise RuntimeError("Fresh segmentation head was not preserved")
    for name, parameter in model.named_parameters():
        parameter.requires_grad_(name.startswith("out_conv."))
    return model, sorted(set(expected) - head), sorted(head)


@torch.inference_mode()
def evaluate(model, files: ThebeFiles, coordinates, threshold: float | None):
    model.eval()
    pooled = Histogram()
    per_file = {path.name: Histogram() for path in files.paths}
    manifest = []
    coverage = {"raw_voxels": 0, "valid_voxels": 0, "positive_voxels": 0,
                "positive_labels_excluded": 0, "patches_requested": len(coordinates),
                "patches_scored": 0, "inference_seconds": 0.0}
    for number, (file_index, origin) in enumerate(coordinates, 1):
        value = files.read(file_index, origin)
        if value is None:
            manifest.append({"file": files.paths[file_index].name, "origin": list(origin),
                             "status": "no_observed_or_constant_data"})
            continue
        x, target, mask, metadata = value
        x, target, mask = x.cuda(), target.cuda(), mask.cuda()
        torch.cuda.synchronize()
        started = time.perf_counter()
        probabilities = torch.sigmoid(forward(model, x))
        torch.cuda.synchronize()
        seconds = time.perf_counter() - started
        scored_p, scored_y = probabilities[mask], target[mask]
        pooled.update(scored_p, scored_y)
        per_file[metadata["file"]].update(scored_p, scored_y)
        metadata.update({"status": "scored", "inference_seconds": seconds})
        manifest.append(metadata)
        coverage["raw_voxels"] += metadata["raw_voxels"]
        coverage["valid_voxels"] += metadata["valid_voxels"]
        coverage["positive_voxels"] += metadata["positive_voxels"]
        coverage["positive_labels_excluded"] += metadata["positive_labels_excluded"]
        coverage["patches_scored"] += 1
        coverage["inference_seconds"] += seconds
        if number % 32 == 0:
            print(f"evaluation_patch={number}/{len(coordinates)}", flush=True)
    if pooled.positive.sum() == 0 or pooled.negative.sum() == 0:
        raise RuntimeError("Evaluation sample does not contain both classes")
    selected = pooled.best_threshold() if threshold is None else threshold
    return {
        "threshold": selected,
        "metrics": asdict(pooled.metrics(selected)),
        "metrics_at_0_5": asdict(pooled.metrics(0.5)),
        "per_file_at_common_threshold": {
            name: asdict(hist.metrics(selected)) if hist.positive.sum() and hist.negative.sum() else None
            for name, hist in per_file.items()
        },
        "coverage": coverage,
        "manifest": manifest,
        "histogram_positive": pooled.positive,
        "histogram_negative": pooled.negative,
    }


def append_history(path: Path, row: dict) -> None:
    exists = path.exists()
    with path.open("a", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(row))
        if not exists:
            writer.writeheader()
        writer.writerow(row)


def serializable_evaluation(value: dict) -> dict:
    return {key: item for key, item in value.items()
            if key not in {"manifest", "histogram_positive", "histogram_negative"}}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pretraining-checkpoint", type=Path,
                        default=Path("runs/attention3d_two_survey_pretext_seed42_20261026/best.pt"))
    parser.add_argument("--paper-source", type=Path,
                        default=Path("external/attention3d_paper/fault-detection-global-attention.py"))
    parser.add_argument("--thebe-root", type=Path, default=Path("data/processed/thebe_h5"))
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--train-patches", type=int, default=256)
    parser.add_argument("--validation-patches", type=int, default=128)
    parser.add_argument("--test-patches", type=int, default=256)
    parser.add_argument("--evaluation-interval", type=int, default=64)
    parser.add_argument("--learning-rate", type=float, default=1e-3)
    parser.add_argument("--weight-decay", type=float, default=0.0)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    if not torch.cuda.is_available() or not torch.cuda.is_bf16_supported():
        raise RuntimeError("A BF16-capable CUDA GPU is required")
    if min(args.train_patches, args.validation_patches, args.test_patches,
           args.evaluation_interval) <= 0:
        raise ValueError("Patch counts must be positive")
    if args.train_patches % args.evaluation_interval:
        raise ValueError("--train-patches must be divisible by --evaluation-interval")
    if args.run_dir.exists() and any(args.run_dir.iterdir()):
        raise FileExistsError(f"Refusing to overwrite nonempty run: {args.run_dir}")
    args.run_dir.mkdir(parents=True, exist_ok=True)

    train_paths = split_paths(args.thebe_root, "train", 9)
    val_paths = split_paths(args.thebe_root, "val", 2)
    test_paths = split_paths(args.thebe_root, "test", 7)
    validate_disjoint([train_paths, val_paths, test_paths])
    config = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "experiment": "attention3d_opunake_kahu_pretrained_frozen_backbone_thebe_linear_probe",
        "claim_scope": "fixed-budget 64-cube sampled Thebe representation-transfer screening",
        "pretraining_checkpoint": str(args.pretraining_checkpoint),
        "pretraining_checkpoint_sha256": sha256(args.pretraining_checkpoint),
        "paper_source": str(args.paper_source),
        "paper_source_sha256": sha256(args.paper_source),
        "trainer_sha256": sha256(Path(__file__)),
        "train_files": [str(path) for path in train_paths],
        "validation_files": [str(path) for path in val_paths],
        "test_files": [str(path) for path in test_paths],
        "patch_size": PATCH,
        "train_patches": args.train_patches,
        "validation_patches": args.validation_patches,
        "test_patches": args.test_patches,
        "evaluation_interval": args.evaluation_interval,
        "optimizer": f"AdamW head-only lr={args.learning_rate} weight_decay={args.weight_decay}",
        "loss": "UnifiedFocalLoss(lambda=0.5, tversky alpha=0.3 beta=0.7 gamma=1.33, focal alpha=0.25 gamma=2.0)",
        "normalization": "per-patch z-score on raw-nonzero voxels; axes reversed to model order",
        "validity_mask": "raw seismic != 0",
        "sampling": "training alternates fault-present and uniform patches; validation/test are fixed uniform nonoverlapping-grid samples",
        "validation_seed": args.seed + 10_000,
        "test_seed": args.seed + 20_000,
        "test_files_opened_during_training": False,
        "paper_exact_reproduction": False,
    }
    write_json(args.run_dir / "config.json", config)

    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    torch.cuda.manual_seed_all(args.seed)
    torch.backends.cudnn.benchmark = False
    torch.backends.cuda.enable_math_sdp(False)
    torch.cuda.reset_peak_memory_stats()

    paper = load_paper_code(args.paper_source)
    checkpoint = torch.load(args.pretraining_checkpoint, map_location="cpu", weights_only=False)
    model, feature_names, head_names = initialize_model(paper, checkpoint, args.seed)
    if sum(p.numel() for p in model.parameters()) != 45_001_057:
        raise RuntimeError("Unexpected Attention3D parameter count")
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    if trainable != 177:
        raise RuntimeError(f"Expected a 177-parameter linear head; found {trainable}")
    model = model.cuda()
    optimizer = torch.optim.AdamW(
        [parameter for parameter in model.parameters() if parameter.requires_grad],
        lr=args.learning_rate, weight_decay=args.weight_decay,
    )
    criterion = paper.UnifiedFocalLoss(
        lambda_param=0.5, tversky_alpha=0.3, tversky_beta=0.7,
        tversky_gamma=1.33, focal_alpha=0.25, focal_gamma=2.0,
    )

    train_files = ThebeFiles(train_paths)
    validation_files = ThebeFiles(val_paths)
    validation_coordinates = fixed_uniform_coordinates(
        validation_files, args.validation_patches, args.seed + 10_000
    )
    best_score = float("-inf")
    best_step = 0
    started = time.time()
    try:
        for index in range(args.train_patches):
            model.train()
            x, target, mask, metadata = sample_training_patch(train_files, index, args.seed)
            x, target, mask = x.cuda(), target.cuda(), mask.cuda()
            optimizer.zero_grad(set_to_none=True)
            logits = forward(model, x)
            loss = criterion(logits[mask], target[mask])
            require_finite(loss, "linear-probe loss")
            loss.backward()
            grad_norm = torch.nn.utils.clip_grad_norm_(
                [parameter for parameter in model.parameters() if parameter.requires_grad], 1.0
            )
            require_finite(grad_norm, "linear-probe gradient")
            optimizer.step()
            row = {
                "step": index + 1,
                "loss": float(loss.detach()),
                "gradient_norm": float(grad_norm),
                "file": metadata["file"],
                "positive_voxels": metadata["positive_voxels"],
                "elapsed_seconds": time.time() - started,
            }
            append_history(args.run_dir / "history.csv", row)
            if (index + 1) % 16 == 0:
                print(json.dumps(row), flush=True)
            if (index + 1) % args.evaluation_interval == 0:
                validation = evaluate(model, validation_files, validation_coordinates, None)
                validation_serial = serializable_evaluation(validation)
                score = validation_serial["metrics"]["pr_auc_approx"]
                write_json(args.run_dir / f"validation_step_{index + 1:04d}.json", validation_serial)
                if score > best_score:
                    best_score = score
                    best_step = index + 1
                    save_torch(args.run_dir / "best.pt", {
                        "model": model.state_dict(),
                        "step": best_step,
                        "validation": validation_serial,
                        "config_sha256": sha256(args.run_dir / "config.json"),
                    })
                print(f"validation step={index + 1} pr_auc={score:.6f} "
                      f"dice={validation_serial['metrics']['dice']:.6f} "
                      f"best_step={best_step}", flush=True)
    finally:
        train_files.close()
        validation_files.close()

    best_checkpoint = torch.load(args.run_dir / "best.pt", map_location="cpu", weights_only=False)
    model.load_state_dict(best_checkpoint["model"], strict=True)
    model.eval().requires_grad_(False)
    validation = best_checkpoint["validation"]
    threshold = float(validation["threshold"])
    frozen = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "status": "frozen_before_test",
        "checkpoint": str(args.run_dir / "best.pt"),
        "checkpoint_sha256": sha256(args.run_dir / "best.pt"),
        "checkpoint_step": int(best_checkpoint["step"]),
        "threshold": threshold,
        "threshold_source": f"fixed {args.validation_patches}-patch Thebe validation sample",
        "validation_metrics": validation["metrics"],
        "test_coordinate_seed": args.seed + 20_000,
        "test_patch_count": args.test_patches,
        "test_files_opened_before_freeze": False,
        "feature_tensors_loaded": len(feature_names),
        "fresh_head_tensors": head_names,
        "total_parameters": 45_001_057,
        "trained_parameters": 177,
    }
    write_json(args.run_dir / "FROZEN_BEFORE_TEST.json", frozen)

    # Test HDF5 files are first opened after checkpoint and threshold freezing.
    test_files = ThebeFiles(test_paths)
    try:
        test_coordinates = fixed_uniform_coordinates(
            test_files, args.test_patches, args.seed + 20_000
        )
        test = evaluate(model, test_files, test_coordinates, threshold)
    finally:
        test_files.close()
    np.savez_compressed(
        args.run_dir / "histograms_2048_bins.npz",
        test_positive=test.pop("histogram_positive"),
        test_negative=test.pop("histogram_negative"),
    )
    test_manifest = test.pop("manifest")
    write_json(args.run_dir / "test_patch_manifest.json", test_manifest)

    result = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "status": "complete",
        "experiment": config["experiment"],
        "claim_scope": config["claim_scope"],
        "pretraining": {
            "surveys": ["Opunake", "Kahu"],
            "task": "self-supervised Gaussian denoising",
            "checkpoint_sha256": config["pretraining_checkpoint_sha256"],
            "Kerry_included": False,
        },
        "downstream": {
            "dataset": "Thebe",
            "trained_parameters": 177,
            "frozen_parameters": 45_001_057 - 177,
            "training_patches": args.train_patches,
            "best_step": best_step,
            "validation_patches": args.validation_patches,
            "test_patches": args.test_patches,
        },
        "checkpoint_sha256": frozen["checkpoint_sha256"],
        "threshold": threshold,
        "threshold_source": frozen["threshold_source"],
        "validation": validation,
        "test": serializable_evaluation(test),
        "test_threshold_tuning": False,
        "peak_gpu_allocated_gib": torch.cuda.max_memory_allocated() / 2**30,
    }
    write_json(args.run_dir / "result.json", result)
    write_json(args.run_dir / "status.json", {
        "status": "complete", "best_step": best_step,
        "threshold": threshold, "test_files_read": True,
    })
    print(json.dumps(result, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
