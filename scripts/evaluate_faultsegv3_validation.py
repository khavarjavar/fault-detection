#!/usr/bin/env python3
"""Validation-only, zero-shot FaultSegV3 evaluation on the existing Thebe grid.

The model uses its released checkpoint and preprocessing. Thebe labels are read
only for scoring; test files are never opened. A bounded run is a smoke check,
not a checkpoint or threshold-selection result.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict
import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np
import torch

import train_r100_fp16_clean as r100
from evaluate_thebe_zero_shot_r100_pinned import ConcatenatedThebe


ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = ROOT / "external/FaultSegV3"
sys.path.insert(0, str(UPSTREAM))
from framework.FaultSegV3 import FaultSegV3  # noqa: E402


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def upstream_normalize(x: torch.Tensor) -> torch.Tensor:
    """Match FaultSegV3's default z-score, clip, min-max preprocessing."""
    std = x.std()
    if not torch.isfinite(std) or std <= 0:
        return torch.zeros_like(x) - 1
    z = ((x - x.mean()) / std).clamp(-3.0, 3.0)
    low, high = torch.aminmax(z)
    return (z - low) / (high - low + 1e-6) * 2 - 1


def raw_input(reader: ConcatenatedThebe, origin: tuple[int, int, int]) -> torch.Tensor:
    stops = tuple(min(start + r100.SIZE, length) for start, length in zip(origin, reader.shape))
    x0, y0, z0 = origin
    x1, y1, z1 = stops
    raw = reader.read("seismic", x0, x1, y0, y1, z0, z1).astype(np.float32, copy=False)
    if not np.isfinite(raw).all():
        raise RuntimeError(f"Nonfinite seismic at {origin}")
    padded = np.zeros((r100.SIZE,) * 3, dtype=np.float32)
    padded[:x1 - x0, :y1 - y0, :z1 - z0] = raw
    return torch.from_numpy(np.ascontiguousarray(padded.transpose())[None, None])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--max-observed", type=int, default=0,
                        help="Stop after this many observed tiles; 0 runs complete validation")
    args = parser.parse_args()
    if args.max_observed < 0:
        parser.error("--max-observed must be nonnegative")
    if args.output.exists():
        raise FileExistsError(args.output)
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA GPU required")

    weights = UPSTREAM / "framework/faultsegv3.ckpt"
    state = torch.load(weights, map_location="cpu", weights_only=True)
    model = FaultSegV3(c=8).eval().cuda().requires_grad_(False)
    model.load_state_dict(state, strict=True)
    reader = ConcatenatedThebe(r100.split_paths(ROOT / "data/processed/thebe_h5", "val", 2))
    histogram = r100.baseline.ProbabilityHistogram(r100.BINS)
    counts = {"patches": 0, "observed_patches": 0, "valid_voxels": 0,
              "positive_voxels": 0, "raw_voxels": 0, "positive_labels_excluded": 0}
    started = time.monotonic()
    try:
        if reader.shape != (200, 3174, 1537):
            raise RuntimeError(f"Unexpected Thebe validation shape: {reader.shape}")
        coordinates = r100.tiling(reader.shape)
        for origin in coordinates:
            _, target, mask, shape, observed, excluded, _ = r100.read_patch(reader, origin)
            counts["patches"] += 1
            counts["raw_voxels"] += int(np.prod(shape))
            counts["valid_voxels"] += observed
            counts["positive_voxels"] += int(target[mask].sum())
            counts["positive_labels_excluded"] += excluded
            if not observed:
                continue
            counts["observed_patches"] += 1
            x = raw_input(reader, origin).cuda()
            with torch.inference_mode(), torch.autocast("cuda", dtype=torch.float16):
                probability = model(upstream_normalize(x), rank=4, chunk_size=64)
            if probability.shape != (1, 1, 128, 128, 128) or not torch.isfinite(probability).all():
                raise RuntimeError(f"Invalid model output at {origin}")
            histogram.update_probabilities(probability.float().cpu()[mask], target[mask])
            if counts["observed_patches"] % 10 == 0 or args.max_observed:
                print(f"observed {counts['observed_patches']}; tiles {counts['patches']}; "
                      f"seconds {time.monotonic() - started:.1f}", flush=True)
            if args.max_observed and counts["observed_patches"] >= args.max_observed:
                break
    finally:
        reader.close()

    complete = args.max_observed == 0
    if complete and (counts["patches"] != 650 or counts["raw_voxels"] != int(np.prod(reader.shape))
                     or counts["valid_voxels"] != 613_738_550
                     or counts["positive_voxels"] != 17_128_496):
        raise RuntimeError(f"Incomplete or changed validation coverage: {counts}")
    threshold = histogram.best_dice_threshold() if complete else 0.5
    result = {
        "status": "complete_validation" if complete else "bounded_smoke_only",
        "checkpoint": str(weights.relative_to(ROOT)),
        "checkpoint_sha256": sha256(weights),
        "upstream_model_sha256": sha256(UPSTREAM / "framework/FaultSegV3.py"),
        "script_sha256": sha256(Path(__file__)),
        "input": "raw Thebe amplitude, axis-reversed, zero-padded to 128^3",
        "preprocessing": "released FaultSegV3 zscore clip=3 minmax to [-1,1] per tile",
        "mask": "nonzero raw seismic, matching R100 full-grid scoring",
        "threshold_source": "complete validation Dice" if complete else "fixed 0.5 smoke threshold",
        "threshold": threshold,
        "metrics": asdict(histogram.metrics(threshold)),
        "coverage": counts,
        "elapsed_seconds": time.monotonic() - started,
        "test_files_read": False,
    }
    args.output.mkdir(parents=True)
    r100.write_json_atomic(args.output / "result.json", result)
    np.savez_compressed(args.output / "histogram_2048_bins.npz",
                        positive=histogram.positive.numpy(), negative=histogram.negative.numpy())
    print(json.dumps(result, indent=2), flush=True)


if __name__ == "__main__":
    main()
