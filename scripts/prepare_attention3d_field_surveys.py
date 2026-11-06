#!/usr/bin/env python3
"""Convert verified NZP&M SEG-Y surveys into resumable Attention3D arrays.

The script preserves each survey as one dense ``(inline, crossline, time)``
float32 NumPy array plus a two-dimensional trace-validity mask. Missing bins in
the irregular acquisition footprint are zero-filled and excluded from the
patch manifest. It never creates one file per training cube.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import segyio


def atomic_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def sha256_file(path: Path, block_size: int = 16 * 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(block_size):
            digest.update(block)
    return digest.hexdigest()


def raw_header_values(
    path: Path,
    *,
    trace_count: int,
    trace_bytes: int,
    header_byte_one_based: int,
) -> np.ndarray:
    """Read a strided four-byte signed big-endian trace-header field."""
    mapped = np.memmap(path, mode="r", dtype=np.uint8)
    values = np.ndarray(
        shape=(trace_count,),
        dtype=">i4",
        buffer=mapped,
        offset=3600 + header_byte_one_based - 1,
        strides=(trace_bytes,),
    ).astype(np.int64)
    del mapped
    return values


def axis_indices(values: np.ndarray, axis: dict[str, int], label: str) -> np.ndarray:
    minimum = int(axis["minimum"])
    step = int(axis["step"])
    count = int(axis["count"])
    delta = values - minimum
    if np.any(delta < 0) or np.any(delta % step != 0):
        bad = values[(delta < 0) | (delta % step != 0)][:5]
        raise RuntimeError(f"{label} values do not fit configured axis: {bad.tolist()}")
    indices = delta // step
    if np.any(indices >= count):
        raise RuntimeError(f"{label} values exceed configured axis")
    if int(values.min()) != minimum or int(values.max()) != int(axis["maximum"]):
        raise RuntimeError(f"{label} range differs from configured range")
    return indices.astype(np.int32)


def geometry_for_survey(survey: dict[str, Any]) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    path = Path(survey["path"])
    trace_count = int(survey["trace_count"])
    samples = int(survey["samples_per_trace"])
    trace_bytes = 240 + samples * 4
    inline_values = raw_header_values(
        path,
        trace_count=trace_count,
        trace_bytes=trace_bytes,
        header_byte_one_based=int(survey["inline"]["header_byte_one_based"]),
    )
    crossline_values = raw_header_values(
        path,
        trace_count=trace_count,
        trace_bytes=trace_bytes,
        header_byte_one_based=int(survey["crossline"]["header_byte_one_based"]),
    )
    inline_indices = axis_indices(inline_values, survey["inline"], "inline")
    crossline_indices = axis_indices(crossline_values, survey["crossline"], "crossline")
    width = int(survey["crossline"]["count"])
    flat = inline_indices.astype(np.int64) * width + crossline_indices
    if np.unique(flat).size != trace_count:
        raise RuntimeError(f"{survey['id']} contains duplicate inline/crossline pairs")
    valid = np.zeros(
        (int(survey["inline"]["count"]), width), dtype=np.bool_
    )
    valid[inline_indices, crossline_indices] = True
    return inline_indices, crossline_indices, valid


def window_starts(length: int, patch: int, stride: int) -> np.ndarray:
    if length < patch:
        return np.empty(0, dtype=np.int32)
    return np.arange(0, length - patch + 1, stride, dtype=np.int32)


def full_valid_spatial_starts(
    valid: np.ndarray, patch_inline: int, patch_crossline: int, stride_inline: int, stride_crossline: int
) -> np.ndarray:
    """Return strided spatial starts whose entire trace footprint is present."""
    inline_starts = window_starts(valid.shape[0], patch_inline, stride_inline)
    crossline_starts = window_starts(valid.shape[1], patch_crossline, stride_crossline)
    integral = np.pad(valid.astype(np.int64), ((1, 0), (1, 0))).cumsum(0).cumsum(1)
    required = patch_inline * patch_crossline
    starts: list[tuple[int, int]] = []
    for inline in inline_starts:
        i0, i1 = int(inline), int(inline + patch_inline)
        sums = (
            integral[i1, crossline_starts + patch_crossline]
            - integral[i0, crossline_starts + patch_crossline]
            - integral[i1, crossline_starts]
            + integral[i0, crossline_starts]
        )
        starts.extend((i0, int(x)) for x in crossline_starts[sums == required])
    return np.asarray(starts, dtype=np.int32).reshape(-1, 2)


def enumerate_coordinates(
    valid: np.ndarray,
    sample_count: int,
    patch: tuple[int, int, int],
    stride: tuple[int, int, int],
    train_inline_fraction: float,
) -> tuple[np.ndarray, np.ndarray, dict[str, int]]:
    spatial = full_valid_spatial_starts(valid, patch[0], patch[1], stride[0], stride[1])
    times = window_starts(sample_count, patch[2], stride[2])
    cut = int(math.floor(valid.shape[0] * train_inline_fraction))
    train_spatial = spatial[spatial[:, 0] + patch[0] <= cut]
    validation_spatial = spatial[spatial[:, 0] >= cut]

    def expand(items: np.ndarray) -> np.ndarray:
        if items.size == 0 or times.size == 0:
            return np.empty((0, 3), dtype=np.int32)
        result = np.empty((items.shape[0] * times.size, 3), dtype=np.int32)
        result[:, :2] = np.repeat(items, times.size, axis=0)
        result[:, 2] = np.tile(times, items.shape[0])
        return result

    return expand(train_spatial), expand(validation_spatial), {
        "inline_cut_index": cut,
        "valid_spatial_windows_total": int(spatial.shape[0]),
        "train_spatial_windows": int(train_spatial.shape[0]),
        "validation_spatial_windows": int(validation_spatial.shape[0]),
        "time_windows": int(times.size),
        "excluded_crossing_spatial_windows": int(
            spatial.shape[0] - train_spatial.shape[0] - validation_spatial.shape[0]
        ),
    }


def validate_source(survey: dict[str, Any], verify_sha256: bool) -> None:
    path = Path(survey["path"])
    if not path.is_file():
        raise FileNotFoundError(path)
    actual_bytes = path.stat().st_size
    if actual_bytes != int(survey["expected_bytes"]):
        raise RuntimeError(
            f"{survey['id']} byte size mismatch: {actual_bytes} != {survey['expected_bytes']}"
        )
    expected_from_layout = 3600 + int(survey["trace_count"]) * (
        240 + int(survey["samples_per_trace"]) * 4
    )
    if expected_from_layout != actual_bytes:
        raise RuntimeError(f"{survey['id']} configured SEG-Y layout does not match file size")
    if int(survey["sample_format_code"]) != 1:
        raise RuntimeError("Only verified IBM-float SEG-Y inputs are accepted")
    if verify_sha256:
        actual_hash = sha256_file(path)
        if actual_hash != survey["sha256"]:
            raise RuntimeError(f"{survey['id']} SHA-256 mismatch")


def convert_survey(
    survey: dict[str, Any],
    output_root: Path,
    batch_traces: int,
    patch: tuple[int, int, int],
    stride: tuple[int, int, int],
    train_inline_fraction: float,
    check_only: bool,
) -> dict[str, Any]:
    survey_id = str(survey["id"])
    survey_dir = output_root / survey_id
    survey_dir.mkdir(parents=True, exist_ok=True)
    dense_path = survey_dir / "volume_float32.npy"
    partial_path = survey_dir / "volume_float32.npy.part"
    valid_path = survey_dir / "valid_traces.npy"
    state_path = survey_dir / "conversion_state.json"
    manifest_path = survey_dir / "manifest.json"

    inline_indices, crossline_indices, valid = geometry_for_survey(survey)
    train_coords, validation_coords, patch_counts = enumerate_coordinates(
        valid,
        int(survey["samples_per_trace"]),
        patch,
        stride,
        train_inline_fraction,
    )
    if not train_coords.size or not validation_coords.size:
        raise RuntimeError(f"{survey_id} has an empty training or validation patch set")

    summary: dict[str, Any] = {
        "survey": survey_id,
        "source": survey["path"],
        "source_bytes": int(survey["expected_bytes"]),
        "source_sha256": survey["sha256"],
        "shape_inline_crossline_time": [
            int(survey["inline"]["count"]),
            int(survey["crossline"]["count"]),
            int(survey["samples_per_trace"]),
        ],
        "present_traces": int(valid.sum()),
        "missing_bins": int(valid.size - valid.sum()),
        "patch_counts": {
            **patch_counts,
            "train_cubes": int(train_coords.shape[0]),
            "validation_cubes": int(validation_coords.shape[0]),
        },
        "check_only": check_only,
    }
    if check_only:
        return summary

    np.save(valid_path, valid, allow_pickle=False)
    np.save(survey_dir / "train_coordinates.npy", train_coords, allow_pickle=False)
    np.save(survey_dir / "validation_coordinates.npy", validation_coords, allow_pickle=False)

    shape = tuple(summary["shape_inline_crossline_time"])
    if dense_path.exists():
        volume = np.load(dense_path, mmap_mode="r")
        if volume.shape != shape or volume.dtype != np.float32:
            raise RuntimeError(f"Completed array has unexpected layout: {dense_path}")
        prior_manifest = json.loads(manifest_path.read_text())
        return prior_manifest

    state = {
        "next_trace": 0,
        "finite_count": 0,
        "zero_count": 0,
        "sum": 0.0,
        "sum_squares": 0.0,
        "minimum": None,
        "maximum": None,
    }
    if partial_path.exists():
        if not state_path.exists():
            raise RuntimeError(f"Partial array exists without state: {partial_path}")
        state.update(json.loads(state_path.read_text()))
        volume = np.load(partial_path, mmap_mode="r+")
        if volume.shape != shape or volume.dtype != np.float32:
            raise RuntimeError(f"Partial array has unexpected layout: {partial_path}")
    else:
        volume = np.lib.format.open_memmap(partial_path, mode="w+", dtype=np.float32, shape=shape)
        atomic_json(state_path, state)

    start_trace = int(state["next_trace"])
    trace_count = int(survey["trace_count"])
    source_path = Path(survey["path"])
    with segyio.open(
        str(source_path), mode="r", strict=False, ignore_geometry=True, endian="big"
    ) as handle:
        if handle.tracecount != trace_count or len(handle.samples) != shape[2]:
            raise RuntimeError(f"{survey_id} segyio layout differs from verified config")
        for start in range(start_trace, trace_count, batch_traces):
            stop = min(trace_count, start + batch_traces)
            traces = np.asarray(handle.trace.raw[start:stop], dtype=np.float32)
            if traces.shape != (stop - start, shape[2]) or not np.isfinite(traces).all():
                raise RuntimeError(f"{survey_id} invalid trace batch {start}:{stop}")
            volume[inline_indices[start:stop], crossline_indices[start:stop], :] = traces
            values64 = traces.astype(np.float64, copy=False)
            state["finite_count"] = int(state["finite_count"]) + int(traces.size)
            state["zero_count"] = int(state["zero_count"]) + int(np.count_nonzero(traces == 0))
            state["sum"] = float(state["sum"]) + float(values64.sum())
            state["sum_squares"] = float(state["sum_squares"]) + float(np.square(values64).sum())
            batch_min, batch_max = float(traces.min()), float(traces.max())
            state["minimum"] = batch_min if state["minimum"] is None else min(float(state["minimum"]), batch_min)
            state["maximum"] = batch_max if state["maximum"] is None else max(float(state["maximum"]), batch_max)
            state["next_trace"] = stop
            volume.flush()
            atomic_json(state_path, state)
            print(f"[{survey_id}] traces {stop:,}/{trace_count:,} ({100 * stop / trace_count:.1f}%)", flush=True)

    count = int(state["finite_count"])
    mean = float(state["sum"]) / count
    variance = max(0.0, float(state["sum_squares"]) / count - mean * mean)
    summary["amplitudes_present_traces"] = {
        "finite_count": count,
        "nonfinite_count": 0,
        "zero_count": int(state["zero_count"]),
        "minimum": float(state["minimum"]),
        "maximum": float(state["maximum"]),
        "mean": mean,
        "standard_deviation": math.sqrt(variance),
        "rms": math.sqrt(float(state["sum_squares"]) / count),
    }
    summary.update(
        {
            "created_utc": datetime.now(timezone.utc).isoformat(),
            "dtype": "float32",
            "missing_bin_fill": 0.0,
            "normalization_applied_to_stored_array": False,
            "volume_path": str(dense_path),
            "valid_mask_path": str(valid_path),
            "train_coordinates_path": str(survey_dir / "train_coordinates.npy"),
            "validation_coordinates_path": str(survey_dir / "validation_coordinates.npy"),
            "check_only": False,
        }
    )
    atomic_json(manifest_path, summary)
    os.replace(partial_path, dense_path)
    state_path.unlink(missing_ok=True)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path("configs/attention3d_two_survey_pretrain.json"))
    parser.add_argument("--batch-traces", type=int, default=8192)
    parser.add_argument("--verify-sha256", action="store_true")
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument("--surveys", nargs="*", default=None)
    args = parser.parse_args()
    if args.batch_traces < 1:
        raise SystemExit("--batch-traces must be positive")

    config = json.loads(args.config.read_text(encoding="utf-8"))
    output_root = Path(config["output_root"])
    output_root.mkdir(parents=True, exist_ok=True)
    patch = tuple(map(int, config["patch"]["shape"]))
    stride = tuple(map(int, config["patch"]["stride"]))
    if patch != (64, 64, 64) or stride != (32, 32, 32):
        raise RuntimeError("This frozen protocol requires patch 64 and stride 32")
    selected = set(args.surveys or [s["id"] for s in config["surveys"]])
    known = {s["id"] for s in config["surveys"]}
    if not selected or selected - known:
        raise RuntimeError(f"Unknown or empty survey selection: {sorted(selected - known)}")

    results = []
    for survey in config["surveys"]:
        if survey["id"] not in selected:
            continue
        validate_source(survey, args.verify_sha256)
        result = convert_survey(
            survey,
            output_root,
            args.batch_traces,
            patch,
            stride,
            float(config["validation"]["train_inline_fraction"]),
            args.check_only,
        )
        results.append(result)
        print(json.dumps(result["patch_counts"], sort_keys=True), flush=True)

    combined = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "protocol": config["protocol"],
        "config": str(args.config),
        "config_sha256": sha256_file(args.config),
        "converter_sha256": sha256_file(Path(__file__)),
        "claim_limit": config["paper"]["claim_limit"],
        "kerry_included": False,
        "patch_shape": list(patch),
        "stride": list(stride),
        "surveys": results,
        "total_train_cubes": sum(r["patch_counts"]["train_cubes"] for r in results),
        "total_validation_cubes": sum(r["patch_counts"]["validation_cubes"] for r in results),
        "check_only": args.check_only,
    }
    name = "preflight_manifest.json" if args.check_only else "manifest.json"
    atomic_json(output_root / name, combined)
    print(f"Wrote {output_root / name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
