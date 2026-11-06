#!/usr/bin/env python3
"""Inventory NZP&M archives and audit 3D post-stack SEG-Y candidates.

The audit is intentionally read-only.  It records enough geometry and amplitude
evidence to decide whether a file is a regular inline/crossline/time cube before
building a training array from it.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

try:
    import segyio
except ImportError as exc:  # pragma: no cover - exercised by environment setup
    raise SystemExit(
        "segyio is required. Install it in the training environment with: "
        "uv pip install --python .venv_train/bin/python segyio"
    ) from exc


SEGY_SUFFIXES = {".sgy", ".segy"}


def sha256_file(path: Path, block_size: int = 16 * 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(block_size):
            digest.update(block)
    return digest.hexdigest()


def json_number(value: float) -> float | None:
    return float(value) if math.isfinite(float(value)) else None


def candidate_paths(inputs: list[Path]) -> tuple[list[Path], list[dict]]:
    segy_paths: list[Path] = []
    archives: list[dict] = []
    seen: set[Path] = set()

    def add_file(path: Path) -> None:
        resolved = path.resolve()
        if resolved in seen:
            return
        seen.add(resolved)
        if path.suffix.lower() in SEGY_SUFFIXES:
            segy_paths.append(path)
            return
        if path.suffix.lower() == ".zip" or zipfile.is_zipfile(path):
            with zipfile.ZipFile(path) as archive:
                members = [
                    {
                        "name": info.filename,
                        "uncompressed_bytes": info.file_size,
                        "compressed_bytes": info.compress_size,
                        "is_segy_candidate": Path(info.filename).suffix.lower()
                        in SEGY_SUFFIXES,
                    }
                    for info in archive.infolist()
                    if not info.is_dir()
                ]
            archives.append(
                {
                    "path": str(path.resolve()),
                    "bytes": path.stat().st_size,
                    "members": members,
                    "segy_candidate_count": sum(
                        item["is_segy_candidate"] for item in members
                    ),
                    "action": "extract selected SEG-Y member before geometry audit",
                }
            )

    for supplied in inputs:
        if not supplied.exists():
            raise FileNotFoundError(supplied)
        if supplied.is_dir():
            for path in sorted(supplied.rglob("*")):
                if path.is_file() and (
                    path.suffix.lower() in SEGY_SUFFIXES
                    or path.suffix.lower() == ".zip"
                ):
                    add_file(path)
        else:
            add_file(supplied)
    return segy_paths, archives


def sampled_trace_indices(trace_count: int, requested: int) -> np.ndarray:
    count = min(trace_count, requested)
    if count <= 0:
        return np.empty(0, dtype=np.int64)
    return np.unique(np.linspace(0, trace_count - 1, count, dtype=np.int64))


def amplitude_sample(handle, requested: int) -> dict:
    indices = sampled_trace_indices(handle.tracecount, requested)
    finite_count = 0
    zero_count = 0
    value_count = 0
    sampled: list[np.ndarray] = []
    nonfinite_count = 0

    for index in indices:
        trace = np.asarray(handle.trace[int(index)], dtype=np.float32)
        finite = np.isfinite(trace)
        finite_values = trace[finite]
        finite_count += int(finite.sum())
        nonfinite_count += int((~finite).sum())
        zero_count += int(np.count_nonzero(finite_values == 0))
        value_count += int(trace.size)
        if finite_values.size:
            sampled.append(finite_values)

    values = np.concatenate(sampled) if sampled else np.empty(0, np.float32)
    return {
        "trace_indices": indices.tolist(),
        "sampled_trace_count": int(indices.size),
        "sampled_value_count": value_count,
        "finite_count": finite_count,
        "nonfinite_count": nonfinite_count,
        "zero_count": zero_count,
        "zero_fraction_of_finite": (
            zero_count / finite_count if finite_count else None
        ),
        "minimum": json_number(values.min()) if values.size else None,
        "maximum": json_number(values.max()) if values.size else None,
        "mean": json_number(values.mean(dtype=np.float64)) if values.size else None,
        "standard_deviation": (
            json_number(values.std(dtype=np.float64)) if values.size else None
        ),
        "rms": (
            json_number(np.sqrt(np.mean(np.square(values, dtype=np.float64))))
            if values.size
            else None
        ),
    }


def header_value(handle, field) -> int | None:
    try:
        return int(handle.bin[field])
    except (KeyError, RuntimeError, TypeError, ValueError):
        return None


def audit_segy(
    path: Path,
    inline_byte: int,
    crossline_byte: int,
    sample_traces: int,
    calculate_sha256: bool,
    endian: str,
) -> dict:
    with segyio.open(
        str(path),
        mode="r",
        iline=inline_byte,
        xline=crossline_byte,
        strict=False,
        ignore_geometry=True,
        endian=endian,
    ) as handle:
        trace_count = int(handle.tracecount)
        samples = np.asarray(handle.samples)
        inline = np.asarray(handle.attributes(inline_byte)[:], dtype=np.int64)
        crossline = np.asarray(handle.attributes(crossline_byte)[:], dtype=np.int64)
        if inline.size != trace_count or crossline.size != trace_count:
            raise RuntimeError("trace-header count differs from SEG-Y trace count")

        pairs = np.column_stack((inline, crossline))
        unique_pairs, counts = np.unique(pairs, axis=0, return_counts=True)
        unique_inline = np.unique(inline)
        unique_crossline = np.unique(crossline)
        rectangular_bins = int(unique_inline.size * unique_crossline.size)
        duplicate_pair_count = int(np.count_nonzero(counts > 1))
        extra_duplicate_traces = int(np.sum(counts[counts > 1] - 1))
        missing_rectangular_bins = rectangular_bins - int(unique_pairs.shape[0])

        report = {
            "path": str(path.resolve()),
            "bytes": path.stat().st_size,
            "sha256": sha256_file(path) if calculate_sha256 else None,
            "endian": endian,
            "trace_count": trace_count,
            "samples_per_trace": int(samples.size),
            "sample_axis": {
                "first": json_number(samples[0]) if samples.size else None,
                "last": json_number(samples[-1]) if samples.size else None,
                "step": (
                    json_number(np.median(np.diff(samples)))
                    if samples.size > 1
                    else None
                ),
            },
            "binary_header": {
                "sample_interval_microseconds": header_value(
                    handle, segyio.BinField.Interval
                ),
                "samples_per_trace": header_value(handle, segyio.BinField.Samples),
                "format_code": header_value(handle, segyio.BinField.Format),
                "sorting_code": header_value(handle, segyio.BinField.SortingCode),
                "measurement_system": header_value(
                    handle, segyio.BinField.MeasurementSystem
                ),
            },
            "trace_headers": {
                "inline_byte": inline_byte,
                "crossline_byte": crossline_byte,
                "inline_unique_count": int(unique_inline.size),
                "inline_minimum": int(unique_inline.min()) if inline.size else None,
                "inline_maximum": int(unique_inline.max()) if inline.size else None,
                "crossline_unique_count": int(unique_crossline.size),
                "crossline_minimum": (
                    int(unique_crossline.min()) if crossline.size else None
                ),
                "crossline_maximum": (
                    int(unique_crossline.max()) if crossline.size else None
                ),
                "unique_inline_crossline_pairs": int(unique_pairs.shape[0]),
                "duplicate_pair_count": duplicate_pair_count,
                "extra_duplicate_traces": extra_duplicate_traces,
                "rectangular_grid_bins": rectangular_bins,
                "missing_rectangular_bins": missing_rectangular_bins,
                "rectangular_coverage_fraction": (
                    unique_pairs.shape[0] / rectangular_bins
                    if rectangular_bins
                    else None
                ),
                "is_complete_unique_rectangular_grid": bool(
                    trace_count == rectangular_bins
                    and duplicate_pair_count == 0
                    and missing_rectangular_bins == 0
                ),
            },
            "sampled_amplitudes": amplitude_sample(handle, sample_traces),
        }
    return report


def write_json_atomic(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read-only inventory and geometry audit for NZP&M SEG-Y products."
    )
    parser.add_argument("inputs", nargs="+", type=Path)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/data_audit/nzpam_segy_audit.json"),
    )
    parser.add_argument("--inline-byte", type=int, default=189)
    parser.add_argument("--crossline-byte", type=int, default=193)
    parser.add_argument("--sample-traces", type=int, default=128)
    parser.add_argument("--endian", choices=("big", "little"), default="big")
    parser.add_argument(
        "--skip-sha256",
        action="store_true",
        help="Skip the expensive full-file hash during an exploratory audit.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.sample_traces < 1:
        raise SystemExit("--sample-traces must be positive")
    try:
        segy_paths, archives = candidate_paths(args.inputs)
        reports = []
        for path in segy_paths:
            print(f"Auditing {path}", flush=True)
            reports.append(
                audit_segy(
                    path,
                    args.inline_byte,
                    args.crossline_byte,
                    args.sample_traces,
                    not args.skip_sha256,
                    args.endian,
                )
            )
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1

    payload = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "read_only": True,
        "inputs": [str(path.resolve()) for path in args.inputs],
        "archives": archives,
        "segy_files": reports,
        "notes": [
            "A complete rectangular grid is useful evidence, not proof of the authors' crop.",
            "Confirm trace-header byte locations from delivery documentation before conversion.",
            "Do not treat zero amplitudes as missing data without survey-specific evidence.",
        ],
    }
    write_json_atomic(args.output, payload)
    print(
        f"Wrote {len(reports)} SEG-Y audit(s) and {len(archives)} archive inventory item(s) "
        f"to {args.output}"
    )
    if archives and not reports:
        print("Extract the selected SEG-Y archive member, then rerun the geometry audit.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
