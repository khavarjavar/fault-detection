#!/usr/bin/env python3
"""Audit connected-component structure of Thebe validation fault labels.

This checks whether a single-connected-surface topology prior is compatible
with the fixed validation subset. Predictions and test files are never read.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy import ndimage

import train_r100_fp16_clean as r100
from evaluate_thebe_zero_shot_r100_pinned import ConcatenatedThebe


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "runs/r100_150_seed43_20261102/run_config.json"
OUTPUT = ROOT / "reports/evaluation/thebe_validation_topology_audit_20261102.json"


def describe(values: list[float]) -> dict[str, float | None]:
    if not values:
        return {"minimum": None, "median": None, "mean": None, "maximum": None}
    array = np.asarray(values, dtype=np.float64)
    return {
        "minimum": float(array.min()),
        "median": float(np.median(array)),
        "mean": float(array.mean()),
        "maximum": float(array.max()),
    }


def main() -> int:
    if OUTPUT.exists():
        raise FileExistsError(OUTPUT)
    config = json.loads(CONFIG.read_text())
    if config.get("test_files_read") is not False:
        raise RuntimeError("Training configuration does not preserve the closed-test policy")
    paths = [Path(value) if Path(value).is_absolute() else ROOT / value
             for value in config["validation_files"]]
    coordinates = [tuple(value) for value in config["validation_subset_coordinates"]]
    structure = np.ones((3, 3, 3), dtype=np.uint8)
    reader = ConcatenatedThebe(paths)
    rows = []
    try:
        for number, origin in enumerate(coordinates, 1):
            _, target, mask, _, observed, _, _ = r100.read_patch(reader, origin)
            fault = target.numpy()[0, 0].astype(bool)
            valid = mask.numpy()[0, 0].astype(bool)
            fault &= valid
            positive = int(fault.sum())
            if positive:
                labels, component_count = ndimage.label(fault, structure=structure)
                sizes = np.bincount(labels.reshape(-1))[1:]
                sizes.sort()
                components_ge8 = int((sizes >= 8).sum())
                components_ge32 = int((sizes >= 32).sum())
                largest_fraction = float(sizes[-1] / positive)
            else:
                component_count = components_ge8 = components_ge32 = 0
                largest_fraction = 0.0
            rows.append(
                {
                    "origin": origin,
                    "observed_voxels": observed,
                    "positive_voxels": positive,
                    "components_26_connected": int(component_count),
                    "components_at_least_8_voxels": components_ge8,
                    "components_at_least_32_voxels": components_ge32,
                    "largest_component_fraction": largest_fraction,
                }
            )
            if number % 16 == 0:
                print(f"audited={number}/{len(coordinates)}", flush=True)
    finally:
        reader.close()

    positive_rows = [row for row in rows if row["positive_voxels"] > 0]
    document = {
        "purpose": (
            "label-only audit of whether a single-connected-surface topology prior "
            "matches the shared fixed Thebe validation subset"
        ),
        "connectivity": "26-neighbor 3D connected components",
        "selection": "all 128 shared fixed validation-subset coordinates",
        "test_files_read": False,
        "patches": len(rows),
        "fault_present_patches": len(positive_rows),
        "summary_fault_present": {
            "components_all": describe(
                [row["components_26_connected"] for row in positive_rows]
            ),
            "components_at_least_8_voxels": describe(
                [row["components_at_least_8_voxels"] for row in positive_rows]
            ),
            "components_at_least_32_voxels": describe(
                [row["components_at_least_32_voxels"] for row in positive_rows]
            ),
            "largest_component_fraction": describe(
                [row["largest_component_fraction"] for row in positive_rows]
            ),
            "fraction_single_component_all": float(np.mean([
                row["components_26_connected"] == 1 for row in positive_rows
            ])),
            "fraction_single_component_ge32": float(np.mean([
                row["components_at_least_32_voxels"] == 1 for row in positive_rows
            ])),
        },
        "interpretation_rule": (
            "If most fault-present patches contain multiple substantial components, "
            "do not impose a universal Betti-0=1 target; derive topology targets from "
            "each label or use local continuity losses instead."
        ),
        "rows": rows,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(document, indent=2) + "\n")
    print(json.dumps({key: document[key] for key in (
        "patches", "fault_present_patches", "summary_fault_present",
        "test_files_read")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
