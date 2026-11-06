#!/usr/bin/env python3
"""Evaluate a trained FaultEdgeFormer-inspired checkpoint on complete validation."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from dataclasses import asdict
from pathlib import Path

os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")

import torch

import train_r100_fp16_clean as r100
from evaluate_thebe_zero_shot_r100_pinned import ConcatenatedThebe
from faultedgeformer_model import FaultEdgeFormerInspired, count_parameters


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dir", type=Path)
    parser.add_argument(
        "--thebe-root", type=Path, default=Path("data/processed/thebe_h5")
    )
    args = parser.parse_args()
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA GPU required")

    config_path = args.run_dir / "run_config.json"
    checkpoint_path = args.run_dir / "best.pt"
    if not config_path.is_file() or not checkpoint_path.is_file():
        raise FileNotFoundError("run_config.json and best.pt are required")
    config = json.loads(config_path.read_text())
    if config.get("test_files_read") is not False:
        raise RuntimeError("Run configuration does not prove test isolation")
    expected_model_hash = config["source_hashes"]["scripts/faultedgeformer_model.py"]
    actual_model_hash = sha256(Path("scripts/faultedgeformer_model.py"))
    if actual_model_hash != expected_model_hash:
        raise RuntimeError("Model source differs from the source used for training")

    specification = config["model_spec"]
    model = FaultEdgeFormerInspired(
        channels=tuple(specification["channels"]),
        heads=tuple(specification["heads"]),
        window_size=int(specification["window_size"]),
        mlp_ratio=int(specification["mlp_ratio"]),
        sobel_repeats=int(specification["sobel_repeats"]),
        use_checkpoint=False,
    )
    checkpoint = torch.load(checkpoint_path, map_location="cpu", weights_only=False)
    model.load_state_dict(checkpoint["model"], strict=True)
    device = torch.device("cuda")
    model.to(device)

    validation_files = r100.split_paths(args.thebe_root, "val", 2)
    reader = ConcatenatedThebe(validation_files)
    try:
        coordinates = r100.tiling(reader.shape)
        histogram, _, coverage = r100.evaluate(model, reader, coordinates, device)
        if coverage["raw_voxels"] != reader.shape[0] * reader.shape[1] * reader.shape[2]:
            raise RuntimeError("Incomplete validation coverage")
        threshold = histogram.best_dice_threshold()
        metrics = asdict(histogram.metrics(threshold))
        r100.assert_finite_tree(metrics, "complete_validation_metrics")
        result = {
            "status": "complete_validation_only",
            "run_dir": str(args.run_dir),
            "checkpoint": str(checkpoint_path),
            "checkpoint_sha256": sha256(checkpoint_path),
            "checkpoint_epoch": int(checkpoint["epoch"]),
            "model_parameters": count_parameters(model),
            "threshold": float(threshold),
            "threshold_source": "complete val1.h5 + val2.h5 only",
            "metrics": metrics,
            "coverage": coverage,
            "validation_files": [str(path) for path in validation_files],
            "test_files_read": False,
        }
        r100.write_json_atomic(args.run_dir / "complete_validation.json", result)
        print(json.dumps(result, indent=2), flush=True)
    finally:
        reader.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
