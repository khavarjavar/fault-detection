#!/usr/bin/env python3
"""Export explicitly downsampled, non-test volumes for the seismic viewer.

The generated arrays are qualitative visualization aids. They are never inputs to
training or quantitative evaluation, and the manifest records every sampling
stride so they cannot be mistaken for native-resolution data.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import h5py
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "data" / "processed" / "viewer_previews"

SPECS: tuple[dict[str, Any], ...] = (
    {
        "id": "kahu_seismic_vis_s3x4x3",
        "source": ROOT
        / "data/processed/attention3d_nzpam/kahu/volume_float32.npy",
        "dataset": None,
        "stride": (3, 4, 3),
        "split": "unlabelled_pretraining",
        "kind": "seismic",
    },
    {
        "id": "opunake_seismic_vis_s3x5x3",
        "source": ROOT
        / "data/processed/attention3d_nzpam/opunake/volume_float32.npy",
        "dataset": None,
        "stride": (3, 5, 3),
        "split": "unlabelled_pretraining",
        "kind": "seismic",
    },
    {
        "id": "thebe_train1_seismic_vis_s1x6x3",
        "source": ROOT / "data/processed/thebe_h5/train1.h5",
        "dataset": "seismic",
        "stride": (1, 6, 3),
        "split": "train",
        "kind": "seismic",
    },
    {
        "id": "thebe_train1_fault_mask_vis_s1x6x3",
        "source": ROOT / "data/processed/thebe_h5/train1.h5",
        "dataset": "fault",
        "stride": (1, 6, 3),
        "split": "train",
        "kind": "fault_mask",
    },
    {
        "id": "thebe_val1_seismic_vis_s1x6x3",
        "source": ROOT / "data/processed/thebe_h5/val1.h5",
        "dataset": "seismic",
        "stride": (1, 6, 3),
        "split": "validation",
        "kind": "seismic",
    },
    {
        "id": "thebe_val1_fault_mask_vis_s1x6x3",
        "source": ROOT / "data/processed/thebe_h5/val1.h5",
        "dataset": "fault",
        "stride": (1, 6, 3),
        "split": "validation",
        "kind": "fault_mask",
    },
)


def sampled_shape(shape: tuple[int, ...], stride: tuple[int, ...]) -> tuple[int, ...]:
    if len(shape) != 3 or len(stride) != 3:
        raise ValueError(f"Expected 3D shape and stride, got {shape=} {stride=}")
    return tuple((size + step - 1) // step for size, step in zip(shape, stride))


def export_array(
    source: Any,
    destination: Path,
    stride: tuple[int, int, int],
    force: bool,
) -> tuple[tuple[int, ...], str]:
    source_shape = tuple(int(value) for value in source.shape)
    output_shape = sampled_shape(source_shape, stride)
    dtype = np.dtype(source.dtype)

    if destination.exists() and not force:
        existing = np.load(destination, mmap_mode="r", allow_pickle=False)
        if existing.shape != output_shape or existing.dtype != dtype:
            raise RuntimeError(
                f"Existing preview does not match request: {destination} "
                f"has {existing.shape}/{existing.dtype}, expected {output_shape}/{dtype}"
            )
        print(f"reuse {destination.name}: {output_shape} {dtype}", flush=True)
        return output_shape, str(dtype)

    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(destination.suffix + ".part")
    if temporary.exists():
        temporary.unlink()
    output = np.lib.format.open_memmap(
        temporary, mode="w+", dtype=dtype, shape=output_shape
    )

    first_indices = list(range(0, source_shape[0], stride[0]))
    report_every = max(1, len(first_indices) // 10)
    for output_index, source_index in enumerate(first_indices):
        output[output_index] = source[
            source_index, :: stride[1], :: stride[2]
        ]
        if (output_index + 1) % report_every == 0 or output_index + 1 == len(
            first_indices
        ):
            print(
                f"{destination.name}: {output_index + 1}/{len(first_indices)} planes",
                flush=True,
            )
    output.flush()
    del output
    temporary.replace(destination)
    return output_shape, str(dtype)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    records: list[dict[str, Any]] = []
    for spec in SPECS:
        source_path = Path(spec["source"])
        if not source_path.is_file():
            raise FileNotFoundError(source_path)
        destination = args.output_dir / f"{spec['id']}.npy"
        dataset_name = spec["dataset"]

        if dataset_name is None:
            source = np.load(source_path, mmap_mode="r", allow_pickle=False)
            source_shape = tuple(int(value) for value in source.shape)
            output_shape, dtype = export_array(
                source, destination, spec["stride"], args.force
            )
            del source
        else:
            with h5py.File(source_path, "r") as handle:
                source = handle[dataset_name]
                source_shape = tuple(int(value) for value in source.shape)
                output_shape, dtype = export_array(
                    source, destination, spec["stride"], args.force
                )

        records.append(
            {
                "id": spec["id"],
                "output": str(destination.resolve()),
                "output_bytes": destination.stat().st_size,
                "output_shape": output_shape,
                "dtype": dtype,
                "source": str(source_path.resolve()),
                "source_dataset": dataset_name,
                "source_shape": source_shape,
                "stride_inline_crossline_sample": spec["stride"],
                "axis_order": ["inline", "crossline", "sample"],
                "split": spec["split"],
                "kind": spec["kind"],
                "purpose": "qualitative visualization only",
            }
        )

    manifest = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "contains_test_split": False,
        "warning": (
            "Downsampled visualization previews only; never use for training, "
            "threshold selection, or quantitative evaluation."
        ),
        "volumes": records,
    }
    manifest_path = args.output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"wrote {manifest_path}", flush=True)


if __name__ == "__main__":
    main()
