#!/usr/bin/env python3
"""Frozen single-seed Thebe test for a completed FaultEdgeFormer run.

The checkpoint and threshold must already be selected using validation only.
Validation is reproduced before any test HDF5 dataset is opened. The test
histogram is then scored at the unchanged validation-selected threshold.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")

import numpy as np
import torch

import train_r100_fp16_clean as r100
from evaluate_thebe_zero_shot_r100_pinned import ConcatenatedThebe
from faultedgeformer_model import FaultEdgeFormerInspired, count_parameters


EXPECTED = {
    "val": {
        "files": 2,
        "shape": (200, 3174, 1537),
        "patches": 650,
        "valid_voxels": 613_738_550,
        "positive_voxels": 17_128_496,
        "positive_labels_excluded": 23_514,
    },
    "test": {
        "files": 7,
        "shape": (703, 3174, 1537),
        "patches": 1950,
        "valid_voxels": 2_303_341_553,
        "positive_voxels": 57_680_496,
        "positive_labels_excluded": 34_415,
    },
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(8 * 1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text())


def file_metadata(path: Path) -> dict:
    stat = path.stat()
    return {"bytes": stat.st_size, "mtime_ns": stat.st_mtime_ns}


def assert_metric_match(actual: dict, expected: dict, label: str) -> None:
    if set(actual) != set(expected):
        raise RuntimeError(f"Metric schema mismatch: {label}")
    for key, value in actual.items():
        if not math.isclose(value, expected[key], rel_tol=0.0, abs_tol=1e-12):
            raise RuntimeError(f"Metric mismatch {label}/{key}: {value} != {expected[key]}")


def validate_coverage(split: str, reader, coordinates, histogram, coverage) -> None:
    expected = EXPECTED[split]
    if tuple(reader.shape) != expected["shape"] or len(coordinates) != expected["patches"]:
        raise RuntimeError(f"Unexpected {split} shape or tiling")
    if coverage["raw_voxels"] != math.prod(expected["shape"]):
        raise RuntimeError(f"Incomplete {split} raw coverage")
    if coverage["valid_voxels"] != expected["valid_voxels"]:
        raise RuntimeError(f"Unexpected {split} valid-voxel count")
    if coverage["positive_labels_excluded"] != expected["positive_labels_excluded"]:
        raise RuntimeError(f"Unexpected {split} excluded-positive count")
    positive = int(histogram.positive.sum())
    negative = int(histogram.negative.sum())
    if positive != expected["positive_voxels"]:
        raise RuntimeError(f"Unexpected {split} positive-voxel count")
    if positive + negative != expected["valid_voxels"]:
        raise RuntimeError(f"Unexpected {split} histogram coverage")


def preflight(run_dir: Path, data_root: Path, output: Path):
    required = [
        run_dir / "run_config.json",
        run_dir / "history.csv",
        run_dir / "best.pt",
        run_dir / "status.json",
        run_dir / "validation_selection.json",
    ]
    if not all(path.is_file() for path in required):
        raise RuntimeError("FaultEdgeFormer run is not complete")
    config = read_json(required[0])
    status = read_json(required[3])
    selection = read_json(required[4])
    if status.get("status") != "validation_only_complete":
        raise RuntimeError(f"Invalid training status: {status.get('status')}")
    if status.get("epochs_completed") != 100 or status.get("epochs_requested") != 100:
        raise RuntimeError("Expected a completed 100-epoch run")
    if config.get("test_files_read") is not False or selection.get("test_files_read") is not False:
        raise RuntimeError("Training artifacts do not prove test isolation")
    if selection["threshold_source"] != "complete val1.h5 + val2.h5":
        raise RuntimeError("Threshold was not selected on complete validation")
    threshold = float(selection["threshold"])
    if not 0 < threshold < 1:
        raise RuntimeError("Invalid frozen threshold")
    if status["best_epoch"] != selection["best_epoch"] or status["threshold"] != threshold:
        raise RuntimeError("Status and validation selection disagree")
    with required[1].open(newline="") as stream:
        history = list(csv.DictReader(stream))
    if [int(row["epoch"]) for row in history] != list(range(1, 101)):
        raise RuntimeError("Training history is incomplete")
    if int(max(history, key=lambda row: float(row["val_pr_auc_approx"]))["epoch"]) != selection["best_epoch"]:
        raise RuntimeError("Best checkpoint selection differs from history")
    if sha256(Path("scripts/faultedgeformer_model.py")) != config["source_hashes"]["scripts/faultedgeformer_model.py"]:
        raise RuntimeError("FaultEdgeFormer model source changed after training")
    checkpoint_hash = sha256(run_dir / "best.pt")
    validation_paths = r100.split_paths(data_root, "val", EXPECTED["val"]["files"])
    test_paths = r100.split_paths(data_root, "test", EXPECTED["test"]["files"])
    train_paths = [Path(path) for path in config["train_files"]]
    all_paths = train_paths + validation_paths + test_paths
    if len({path.resolve() for path in all_paths}) != len(all_paths):
        raise RuntimeError("Train, validation, and test paths overlap")
    if len({(path.stat().st_dev, path.stat().st_ino) for path in all_paths}) != len(all_paths):
        raise RuntimeError("Dataset split contains aliased files")
    test_manifest = read_json(Path("configs/r100_test_data_manifest.json"))["data_files"]
    for path in test_paths:
        relative = str(path)
        if test_manifest.get(relative) != file_metadata(path):
            raise RuntimeError(f"Test data fingerprint changed: {path}")
    frozen = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "status": "frozen_before_test",
        "experiment": config["experiment"],
        "claim_scope": "single-seed exploratory frozen test",
        "seed": config["seed"],
        "checkpoint": str(run_dir / "best.pt"),
        "checkpoint_sha256": checkpoint_hash,
        "checkpoint_epoch": selection["best_epoch"],
        "threshold": threshold,
        "threshold_source": selection["threshold_source"],
        "protocol_hash": config["protocol_hash"],
        "test_file_metadata": {str(path): file_metadata(path) for path in test_paths},
        "test_hdf5_datasets_opened_before_freeze": False,
    }
    output.mkdir(parents=True, exist_ok=True)
    frozen_path = output / "FROZEN_BEFORE_TEST.json"
    if frozen_path.exists() and read_json(frozen_path) != frozen:
        # A rerun is allowed only with the originally frozen scientific fields;
        # ignore the timestamp when comparing records.
        old = read_json(frozen_path)
        if {k: v for k, v in old.items() if k != "created_utc"} != {k: v for k, v in frozen.items() if k != "created_utc"}:
            raise RuntimeError("Existing frozen-test record differs")
        frozen = old
    else:
        r100.write_json_atomic(frozen_path, frozen)
    return config, selection, validation_paths, test_paths, frozen


def load_model(config: dict, selection: dict, run_dir: Path):
    spec = config["model_spec"]
    model = FaultEdgeFormerInspired(
        channels=tuple(spec["channels"]),
        heads=tuple(spec["heads"]),
        window_size=int(spec["window_size"]),
        mlp_ratio=int(spec["mlp_ratio"]),
        sobel_repeats=int(spec["sobel_repeats"]),
        use_checkpoint=False,
    )
    if count_parameters(model) != config["model_parameters"]:
        raise RuntimeError("Model parameter count changed")
    checkpoint = torch.load(run_dir / "best.pt", map_location="cpu", weights_only=False)
    if checkpoint["epoch"] != selection["best_epoch"]:
        raise RuntimeError("Checkpoint epoch differs from frozen selection")
    r100.assert_finite_tree(checkpoint["model"], "checkpoint.model")
    model.load_state_dict(checkpoint["model"], strict=True)
    return model.cuda().eval().requires_grad_(False)


def evaluate_split(split: str, paths: list[Path], model, device, threshold: float):
    reader = ConcatenatedThebe(paths)
    try:
        coordinates = r100.tiling(reader.shape)
        histogram, _, coverage = r100.evaluate(model, reader, coordinates, device)
        validate_coverage(split, reader, coordinates, histogram, coverage)
        return {
            "split": split,
            "complete_coverage": True,
            "threshold": threshold,
            "metrics": asdict(histogram.metrics(threshold)),
            "metrics_at_0_5": asdict(histogram.metrics(0.5)),
            "coverage": coverage,
        }, histogram
    finally:
        reader.close()


def report_text(config, selection, validation, test, frozen) -> str:
    names = ["dice", "iou", "precision", "recall", "specificity", "f2", "mcc", "balanced_accuracy", "kappa", "pr_auc_approx"]
    available = [name for name in names if name in test["metrics"]]
    lines = [
        "# FaultEdgeFormer-inspired frozen Thebe test",
        "",
        f"- Seed: {config['seed']}",
        f"- Selected checkpoint epoch: {selection['best_epoch']}",
        f"- Frozen threshold: {selection['threshold']:.9f} (selected on complete validation)",
        f"- Checkpoint SHA-256: `{frozen['checkpoint_sha256']}`",
        "- Claim scope: single-seed exploratory architecture-control result",
        "",
        "| Metric | Validation | Test |",
        "|---|---:|---:|",
    ]
    for name in available:
        lines.append(f"| {name} | {validation['metrics'][name]:.6f} | {test['metrics'][name]:.6f} |")
    lines.extend(
        [
            "",
            "The model was trained on Thebe `train1.h5` through `train9.h5` and selected using `val1.h5` plus `val2.h5`. All seven `test*.h5` files were opened only after checkpoint and threshold freezing. The test threshold was not optimized on test labels.",
            "",
            "This is a FaultEdgeFormer-inspired local implementation because author code and several exact architecture details were unavailable. One seed does not estimate seed variance.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--data-root", type=Path, default=Path("data/processed/thebe_h5"))
    parser.add_argument("--output", type=Path, default=Path("reports/evaluation/faultedgeformer_thebe_full_seed42_20261026"))
    args = parser.parse_args()
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA GPU required")
    config, selection, validation_paths, test_paths, frozen = preflight(
        args.run_dir, args.data_root, args.output
    )
    model = load_model(config, selection, args.run_dir)
    device = torch.device("cuda")
    validation, validation_histogram = evaluate_split(
        "val", validation_paths, model, device, float(selection["threshold"])
    )
    assert_metric_match(validation["metrics"], selection["full_validation"], "validation")
    # Test HDF5 arrays are opened only after validation reproduction succeeds.
    test, test_histogram = evaluate_split(
        "test", test_paths, model, device, float(selection["threshold"])
    )
    np.savez_compressed(
        args.output / "histograms_2048_bins.npz",
        validation_positive=validation_histogram.positive.cpu().numpy(),
        validation_negative=validation_histogram.negative.cpu().numpy(),
        test_positive=test_histogram.positive.cpu().numpy(),
        test_negative=test_histogram.negative.cpu().numpy(),
    )
    result = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "status": "complete",
        "experiment": config["experiment"],
        "claim_scope": "single-seed exploratory frozen test",
        "seed": config["seed"],
        "checkpoint_epoch": selection["best_epoch"],
        "checkpoint_sha256": frozen["checkpoint_sha256"],
        "threshold": selection["threshold"],
        "threshold_source": selection["threshold_source"],
        "validation": validation,
        "test": test,
        "test_threshold_tuning": False,
    }
    r100.write_json_atomic(args.output / "result.json", result)
    report = report_text(config, selection, validation, test, frozen)
    temporary = args.output / "report.md.part"
    temporary.write_text(report)
    os.replace(temporary, args.output / "report.md")
    print(json.dumps(result, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
