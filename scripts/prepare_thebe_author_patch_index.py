#!/usr/bin/env python3
"""Rebuild the Thebe authors' 96/48 fault-rich patch index from H5 files."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np

import train_r100_fp16_clean as r100
from evaluate_thebe_zero_shot_r100_pinned import ConcatenatedThebe


ROOT = Path(__file__).resolve().parents[1]
PATCH = 96
STEP = 48
MINIMUM_FAULT_PIXELS = int(0.03 * PATCH * PATCH)
EXPECTED = {"train": 181_029, "val": 64_317}


def padding(height: int, width: int) -> tuple[int, int, int, int, int, int]:
    rows = math.ceil((height - (PATCH - STEP)) / STEP)
    columns = math.ceil((width - (PATCH - STEP)) / STEP)
    padded_h = STEP * rows + PATCH - STEP
    padded_w = STEP * columns + PATCH - STEP
    top = (padded_h - height) // 2
    left = (padded_w - width) // 2
    return top, padded_h - height - top, left, padded_w - width - left, rows, columns


def build(split: str, root: Path, max_slices: int | None) -> dict:
    count = 9 if split == "train" else 2
    files = r100.split_paths(root, split, count)
    reader = ConcatenatedThebe(files)
    try:
        # The H5 reader is (crossline, inline, time). The author notebook moves
        # the original cube to (crossline, time, inline) before patching.
        height, width = reader.shape[2], reader.shape[1]
        top, bottom, left, right, rows, columns = padding(height, width)
        planned = reader.shape[0] if max_slices is None else min(max_slices, reader.shape[0])
        by_slice: list[list[list[int]]] = []
        total = 0
        for crossline in range(planned):
            label = reader.read(
                "fault", crossline, crossline + 1,
                0, reader.shape[1], 0, reader.shape[2]
            )[0].T
            if label.shape != (height, width) or label.min() < 0 or label.max() > 1:
                raise RuntimeError(f"Invalid label slice {crossline}: {label.shape}")
            label = np.pad(label, ((top, bottom), (left, right)), mode="reflect")
            selected: list[list[int]] = []
            for row in range(rows):
                y0 = row * STEP
                for column in range(columns):
                    x0 = column * STEP
                    if int(label[y0 : y0 + PATCH, x0 : x0 + PATCH].sum()) >= MINIMUM_FAULT_PIXELS:
                        selected.append([row, column])
            by_slice.append(selected)
            total += len(selected)
            if (crossline + 1) % 50 == 0:
                print(
                    f"split={split} slices={crossline + 1}/{planned} patches={total}",
                    flush=True,
                )
        exact_expected = max_slices is None and total == EXPECTED[split]
        if max_slices is None and not exact_expected:
            raise RuntimeError(
                f"{split} patch count {total} != author notebook {EXPECTED[split]}"
            )
        return {
            "split": split,
            "files": [str(path) for path in files],
            "reader_shape": reader.shape,
            "author_orientation": [reader.shape[0], height, width],
            "patch_size": PATCH,
            "step": STEP,
            "minimum_fault_pixels": MINIMUM_FAULT_PIXELS,
            "padding": {"top": top, "bottom": bottom, "left": left, "right": right},
            "grid": {"rows": rows, "columns": columns},
            "slices_indexed": planned,
            "patches": total,
            "author_notebook_expected_patches": EXPECTED[split],
            "matches_author_notebook": exact_expected,
            "by_slice": by_slice,
            "test_files_read": False,
            "source": "https://github.com/anyuzoey/CNNforFaultInterpretation/blob/master/generatePatchipyTrainValTest.ipynb",
        }
    finally:
        reader.close()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--thebe-root", type=Path, default=ROOT / "data/processed/thebe_h5")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "data/processed/thebe_author_patch_index")
    parser.add_argument("--max-slices", type=int)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for split in ("train", "val"):
        payload = build(split, args.thebe_root, args.max_slices)
        destination = args.output_dir / f"{split}.json"
        temporary = destination.with_suffix(".json.part")
        temporary.write_text(json.dumps(payload, separators=(",", ":")) + "\n")
        temporary.replace(destination)
        print(json.dumps({
            "split": split,
            "patches": payload["patches"],
            "matches_author_notebook": payload["matches_author_notebook"],
            "output": str(destination),
        }), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
