#!/usr/bin/env python3
"""Verify converted Attention3D volumes against their source SEG-Y traces."""

from __future__ import annotations

import argparse
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import segyio


def load_prepare_module(path: Path):
    spec = importlib.util.spec_from_file_location("attention3d_prepare", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def verify_survey(survey: dict, root: Path, prepare, samples: int) -> dict:
    survey_id = survey["id"]
    directory = root / survey_id
    manifest = json.loads((directory / "manifest.json").read_text())
    volume = np.load(directory / "volume_float32.npy", mmap_mode="r")
    valid = np.load(directory / "valid_traces.npy", mmap_mode="r")
    train = np.load(directory / "train_coordinates.npy", mmap_mode="r")
    validation = np.load(directory / "validation_coordinates.npy", mmap_mode="r")
    shape = tuple(manifest["shape_inline_crossline_time"])
    if volume.shape != shape or volume.dtype != np.float32:
        raise RuntimeError(f"{survey_id}: invalid volume layout")
    if valid.shape != shape[:2] or valid.dtype != np.bool_:
        raise RuntimeError(f"{survey_id}: invalid validity mask")
    if int(valid.sum()) != int(survey["trace_count"]):
        raise RuntimeError(f"{survey_id}: validity count mismatch")
    if train.shape != (manifest["patch_counts"]["train_cubes"], 3):
        raise RuntimeError(f"{survey_id}: training coordinate count mismatch")
    if validation.shape != (manifest["patch_counts"]["validation_cubes"], 3):
        raise RuntimeError(f"{survey_id}: validation coordinate count mismatch")

    patch = 64
    for role, coords in (("train", train), ("validation", validation)):
        if np.any(coords < 0) or np.any(coords[:, 0] + patch > shape[0]) or np.any(coords[:, 1] + patch > shape[1]) or np.any(coords[:, 2] + patch > shape[2]):
            raise RuntimeError(f"{survey_id}: {role} coordinate out of bounds")
        unique_spatial = np.unique(np.asarray(coords[:, :2]), axis=0)
        for inline, crossline in unique_spatial:
            if not valid[inline:inline + patch, crossline:crossline + patch].all():
                raise RuntimeError(f"{survey_id}: {role} coordinate crosses missing traces")
    if int(train[:, 0].max()) + patch > int(validation[:, 0].min()):
        raise RuntimeError(f"{survey_id}: train and validation inline regions overlap")

    inline_indices, crossline_indices, rebuilt_valid = prepare.geometry_for_survey(survey)
    if not np.array_equal(valid, rebuilt_valid):
        raise RuntimeError(f"{survey_id}: stored mask differs from source geometry")
    rng = np.random.default_rng(20261026)
    trace_indices = np.sort(rng.choice(int(survey["trace_count"]), size=min(samples, int(survey["trace_count"])), replace=False))
    with segyio.open(survey["path"], "r", strict=False, ignore_geometry=True, endian="big") as handle:
        source = np.stack(
            [np.asarray(handle.trace.raw[int(index)], dtype=np.float32) for index in trace_indices]
        )
    converted = np.stack(
        [volume[inline_indices[index], crossline_indices[index], :] for index in trace_indices]
    )
    if not np.array_equal(source, converted):
        maximum_error = float(np.max(np.abs(source - converted)))
        raise RuntimeError(f"{survey_id}: converted traces differ; max error {maximum_error}")

    missing = np.argwhere(~valid)
    missing_checked = 0
    if missing.size:
        selected = missing[rng.choice(missing.shape[0], size=min(samples, missing.shape[0]), replace=False)]
        if any(np.any(volume[int(i), int(j), :] != 0) for i, j in selected):
            raise RuntimeError(f"{survey_id}: sampled missing bins are not zero-filled")
        missing_checked = int(selected.shape[0])

    patch_rms = []
    for coords in (train, validation):
        selected_indices = rng.choice(coords.shape[0], size=min(8, coords.shape[0]), replace=False)
        for index in selected_indices:
            i, j, t = map(int, coords[index])
            cube = np.asarray(volume[i:i + patch, j:j + patch, t:t + patch])
            if cube.shape != (patch, patch, patch) or not np.isfinite(cube).all():
                raise RuntimeError(f"{survey_id}: invalid sampled cube")
            patch_rms.append(float(np.sqrt(np.mean(np.square(cube, dtype=np.float64)))))
    if min(patch_rms) <= 0:
        raise RuntimeError(f"{survey_id}: zero-RMS sampled cube")

    return {
        "survey": survey_id,
        "status": "passed",
        "shape": list(shape),
        "present_traces": int(valid.sum()),
        "source_trace_equality_checks": int(trace_indices.size),
        "missing_zero_fill_checks": missing_checked,
        "sampled_cube_count": len(patch_rms),
        "sampled_cube_rms_range_raw": [min(patch_rms), max(patch_rms)],
        "train_validation_inline_separation_voxels": int(validation[:, 0].min() - (train[:, 0].max() + patch)),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path("configs/attention3d_two_survey_pretrain.json"))
    parser.add_argument("--prepare-script", type=Path, default=Path("scripts/prepare_attention3d_field_surveys.py"))
    parser.add_argument("--output", type=Path, default=Path("reports/data_audit/attention3d_two_survey_conversion_verification_20261026.json"))
    parser.add_argument("--source-trace-samples", type=int, default=32)
    args = parser.parse_args()
    config = json.loads(args.config.read_text())
    prepare = load_prepare_module(args.prepare_script)
    results = [
        verify_survey(survey, Path(config["output_root"]), prepare, args.source_trace_samples)
        for survey in config["surveys"]
    ]
    payload = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "status": "passed",
        "config": str(args.config),
        "kerry_included": False,
        "test_or_thebe_data_read": False,
        "surveys": results,
    }
    prepare.atomic_json(args.output, payload)
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
