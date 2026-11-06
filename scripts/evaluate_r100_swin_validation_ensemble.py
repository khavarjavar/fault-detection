#!/usr/bin/env python3
"""Evaluate a validation-only R100/SwinUNETR probability ensemble.

The script never opens Thebe test files. It sweeps a small, declared convex
weight grid on complete validation and records both the best Dice and best
PR-AUC choices. Individual endpoints reproduce the two source models.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict
from datetime import datetime, timezone
import json
from pathlib import Path
import time

import numpy as np
import torch

import faultseg3d_baseline as baseline
import train_r100_fp16_clean as r100
from evaluate_thebe_zero_shot_r100_pinned import ConcatenatedThebe
from train_swinunetr_thebe_matched import SwinUNETRMatched


ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def require_complete(run_dir: Path) -> tuple[dict, dict]:
    status = load_json(run_dir / "status.json")
    config = load_json(run_dir / "run_config.json")
    if status.get("status") != "validation_only_complete":
        raise RuntimeError(f"Incomplete source run: {run_dir}")
    if status.get("test_files_read") is not False:
        raise RuntimeError(f"Source run did not keep test closed: {run_dir}")
    return status, config


def infer(model: torch.nn.Module, x: torch.Tensor) -> torch.Tensor:
    with torch.inference_mode(), torch.autocast("cuda", dtype=torch.float16):
        logits = model(x.cuda())
    return torch.sigmoid(logits.float())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--r100-run", type=Path,
        default=ROOT / "runs/r100_150_seed43_20261102",
    )
    parser.add_argument(
        "--swin-run", type=Path,
        default=ROOT / "runs/swinunetr_matched_150_seed43_20261102",
    )
    parser.add_argument(
        "--output-dir", type=Path,
        default=ROOT / "reports/evaluation/r100150_swinunetr_validation_ensemble_20261104",
    )
    parser.add_argument("--weight-step", type=float, default=0.05)
    args = parser.parse_args()

    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")
    r100_run = args.r100_run.resolve()
    swin_run = args.swin_run.resolve()
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    r100_status, r100_config = require_complete(r100_run)
    swin_status, swin_config = require_complete(swin_run)
    if r100_config["validation_files"] != swin_config["validation_files"]:
        raise RuntimeError("Validation files differ")
    if r100_config["seed"] != swin_config["seed"]:
        raise RuntimeError("Seeds differ")

    steps = round(1.0 / args.weight_step)
    if steps < 1 or not np.isclose(steps * args.weight_step, 1.0):
        raise ValueError("weight-step must divide 1 exactly")
    weights = [index / steps for index in range(steps + 1)]
    histograms = {weight: baseline.ProbabilityHistogram(2048) for weight in weights}

    r100_model = baseline.FaultSeg3D().cuda().eval()
    swin_model = SwinUNETRMatched(use_checkpoint=True).cuda().eval()
    r100_checkpoint = torch.load(r100_run / "best.pt", map_location="cpu", weights_only=False)
    swin_checkpoint = torch.load(swin_run / "best.pt", map_location="cpu", weights_only=False)
    r100_model.load_state_dict(r100_checkpoint["model"], strict=True)
    swin_model.load_state_dict(swin_checkpoint["model"], strict=True)

    validation_paths = [
        path if path.is_absolute() else ROOT / path
        for path in map(Path, r100_config["validation_files"])
    ]
    reader = ConcatenatedThebe(validation_paths)
    coords = r100.tiling(reader.shape)
    raw_voxels = valid_voxels = 0
    started = time.time()
    try:
        for number, origin in enumerate(coords, 1):
            x, target, mask, shape, observed, _, _ = r100.read_patch(reader, origin)
            raw_voxels += int(np.prod(shape))
            valid_voxels += observed
            if not observed:
                continue
            r100_probability = infer(r100_model, x)
            swin_probability = infer(swin_model, x)
            target = target.cuda()
            mask = mask.cuda()
            truth = target[mask]
            for weight in weights:
                probability = (
                    weight * r100_probability + (1.0 - weight) * swin_probability
                )
                histograms[weight].update_probabilities(probability[mask], truth)
            if number % 100 == 0:
                print(f"validation_patches={number}/{len(coords)}", flush=True)
    finally:
        reader.close()

    rows = []
    for weight in weights:
        histogram = histograms[weight]
        threshold = histogram.best_dice_threshold()
        metrics = asdict(histogram.metrics(threshold))
        rows.append({
            "r100_weight": weight,
            "swinunetr_weight": 1.0 - weight,
            "threshold": threshold,
            "metrics": metrics,
        })
    best_dice = max(rows, key=lambda row: (row["metrics"]["dice"], row["metrics"]["pr_auc_approx"]))
    best_pr_auc = max(rows, key=lambda row: (row["metrics"]["pr_auc_approx"], row["metrics"]["dice"]))
    equal_weight = next(row for row in rows if np.isclose(row["r100_weight"], 0.5))
    result = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "status": "complete",
        "experiment": "R100_150_plus_SwinUNETR_150_validation_probability_ensemble",
        "selection_scope": "complete Thebe validation only",
        "test_files_read": False,
        "weight_grid": weights,
        "checkpoint_epochs": {
            "r100": r100_status["best_epoch"],
            "swinunetr": swin_status["best_epoch"],
        },
        "coverage": {
            "patches": len(coords),
            "raw_voxels": raw_voxels,
            "valid_voxels": valid_voxels,
            "excluded_no_data_voxels": raw_voxels - valid_voxels,
            "seconds": time.time() - started,
        },
        "best_by_dice": best_dice,
        "best_by_pr_auc": best_pr_auc,
        "equal_weight": equal_weight,
        "all_weights": rows,
        "notes": {
            "ensemble": "convex mean of FP32 sigmoid probabilities from FP16-autocast inference",
            "weight_meaning": "r100_weight=1 is R100 only; r100_weight=0 is SwinUNETR only",
            "threshold": "best pooled validation Dice threshold independently selected for each weight",
        },
    }
    (output / "result.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output / "result.json"),
        "best_by_dice": best_dice,
        "best_by_pr_auc": best_pr_auc,
        "equal_weight": equal_weight,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
