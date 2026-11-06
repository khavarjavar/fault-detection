#!/usr/bin/env python3
"""Validation-only zero-shot evaluation of the released FaultNet TorchScript model."""

from __future__ import annotations

import argparse
from dataclasses import asdict
import hashlib
import json
import time
from pathlib import Path

import numpy as np
import torch

import train_r100_fp16_clean as r100
from evaluate_thebe_zero_shot_r100_pinned import ConcatenatedThebe


ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--gamma", choices=("0.5", "0.6", "0.7"), default="0.7")
    parser.add_argument("--max-observed", type=int, default=0)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    if args.max_observed < 0:
        parser.error("--max-observed must be nonnegative")
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA GPU required")

    weights = ROOT / f"external/FaultNet/network/FaultNet_Gamma{args.gamma}.pt"
    model = torch.jit.load(str(weights), map_location="cpu").eval().half().cuda()
    reader = ConcatenatedThebe(r100.split_paths(ROOT / "data/processed/thebe_h5", "val", 2))
    histogram = r100.baseline.ProbabilityHistogram(r100.BINS)
    counts = {"patches": 0, "observed_patches": 0, "valid_voxels": 0,
              "positive_voxels": 0, "raw_voxels": 0, "positive_labels_excluded": 0}
    started = time.monotonic()
    try:
        if reader.shape != (200, 3174, 1537):
            raise RuntimeError(f"Unexpected validation shape: {reader.shape}")
        for origin in r100.tiling(reader.shape):
            _, target, mask, shape, observed, excluded, _ = r100.read_patch(reader, origin)
            counts["patches"] += 1
            counts["raw_voxels"] += int(np.prod(shape))
            counts["valid_voxels"] += observed
            counts["positive_voxels"] += int(target[mask].sum())
            counts["positive_labels_excluded"] += excluded
            if not observed:
                continue
            counts["observed_patches"] += 1
            starts = origin
            stops = tuple(min(start + r100.SIZE, length) for start, length in zip(starts, reader.shape))
            raw = reader.read("seismic", starts[0], stops[0], starts[1], stops[1],
                              starts[2], stops[2]).astype(np.float32, copy=False)
            if not np.isfinite(raw).all():
                raise RuntimeError(f"Nonfinite seismic at {origin}")
            # Match released cubing_prediction: fill the inference block with
            # 0.5, paste seismic, then min-max normalize that whole block.
            padded = np.full((r100.SIZE,) * 3, 0.5, dtype=np.float32)
            padded[:shape[0], :shape[1], :shape[2]] = raw
            x = torch.from_numpy(np.ascontiguousarray(padded.transpose())[None, None]).cuda()
            low, high = torch.aminmax(x)
            x = torch.zeros_like(x) if high <= low else (x - low) / (high - low)
            with torch.inference_mode():
                probability = model(x.half()).float().cpu()
            if probability.shape != (1, 1, 128, 128, 128) or not torch.isfinite(probability).all():
                raise RuntimeError(f"Invalid model output at {origin}")
            if probability.min() < 0 or probability.max() > 1:
                raise RuntimeError(f"Model output is not probability at {origin}")
            histogram.update_probabilities(probability[mask], target[mask])
            if counts["observed_patches"] % 25 == 0 or args.max_observed:
                print(f"observed {counts['observed_patches']}; tiles {counts['patches']}; "
                      f"seconds {time.monotonic() - started:.1f}", flush=True)
            if args.max_observed and counts["observed_patches"] >= args.max_observed:
                break
    finally:
        reader.close()

    complete = args.max_observed == 0
    if complete and (counts["patches"] != 650 or counts["valid_voxels"] != 613_738_550
                     or counts["positive_voxels"] != 17_128_496
                     or counts["raw_voxels"] != int(np.prod(reader.shape))):
        raise RuntimeError(f"Incomplete or changed validation coverage: {counts}")
    threshold = histogram.best_dice_threshold() if complete else 0.5
    result = {
        "status": "complete_validation" if complete else "bounded_smoke_only",
        "checkpoint": str(weights.relative_to(ROOT)),
        "checkpoint_sha256": sha256(weights),
        "script_sha256": sha256(Path(__file__)),
        "gamma": args.gamma,
        "input": "raw Thebe amplitude, axis-reversed, padded with 0.5 to 128^3",
        "preprocessing": "released FaultNet cubing_prediction per-block minmax, computed in float32 before half-precision model input",
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
