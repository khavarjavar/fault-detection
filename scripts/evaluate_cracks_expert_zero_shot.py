#!/usr/bin/env python3
"""Zero-shot evaluation of P1 on the 40 CRACKS expert-labelled sections."""

from __future__ import annotations

import argparse
import csv
import json
import re
import time
from dataclasses import asdict
from pathlib import Path

import numpy as np
import torch
from PIL import Image

import faultseg3d_baseline as baseline
from attention3d_caft import Attention3D


PATCH = 128
STRIDE = 64


def section_number(path: Path) -> int:
    match = re.fullmatch(r"section_(\d+)\.png", path.name)
    if match is None:
        raise RuntimeError(f"Unexpected filename: {path}")
    return int(match.group(1))


def starts(length: int) -> list[int]:
    if length < PATCH:
        raise RuntimeError(f"Image dimension {length} is smaller than {PATCH}")
    values = list(range(0, length - PATCH + 1, STRIDE))
    last = length - PATCH
    if values[-1] != last:
        values.append(last)
    return values


def update_histogram(
    histogram: baseline.ProbabilityHistogram,
    probability: np.ndarray,
    target: np.ndarray,
    valid: np.ndarray,
) -> None:
    probability_tensor = torch.from_numpy(
        probability[valid].astype(np.float32, copy=False)
    ).reshape(1, 1, 1, -1)
    target_tensor = torch.from_numpy(
        target[valid].astype(np.float32, copy=False)
    ).reshape(1, 1, 1, -1)
    histogram.update_probabilities(probability_tensor, target_tensor)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--threshold-metrics", type=Path, required=True)
    parser.add_argument("--images", type=Path, required=True)
    parser.add_argument("--expert-labels", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--histogram-bins", type=int, default=2048)
    args = parser.parse_args()

    if not torch.cuda.is_available():
        raise RuntimeError("CUDA GPU is required")
    if args.output_dir.exists() and any(args.output_dir.iterdir()):
        raise RuntimeError(f"Output directory is not empty: {args.output_dir}")
    args.output_dir.mkdir(parents=True, exist_ok=True)

    image_paths = sorted(args.images.glob("section_*.png"), key=section_number)
    label_paths = sorted(
        args.expert_labels.glob("section_*.png"), key=section_number
    )
    if len(label_paths) != 40:
        raise RuntimeError(f"Expected 40 expert labels, found {len(label_paths)}")

    image_by_number = {section_number(path): path for path in image_paths}
    missing_labels = [
        path.name for path in label_paths
        if section_number(path) not in image_by_number
    ]
    if missing_labels:
        raise RuntimeError(f"Expert labels without seismic images: {missing_labels}")

    sections = [
        np.asarray(Image.open(path).convert("L"), dtype=np.float32)
        for path in image_paths
    ]
    shapes = {section.shape for section in sections}
    if len(shapes) != 1:
        raise RuntimeError(f"Inconsistent seismic image shapes: {sorted(shapes)}")
    volume = np.stack(sections, axis=0)
    height, width = volume.shape[1:]
    ordered_numbers = [section_number(path) for path in image_paths]
    position = {number: index for index, number in enumerate(ordered_numbers)}
    missing_nominal_sections = [
        number
        for number in range(min(ordered_numbers), max(ordered_numbers) + 1)
        if number not in position
    ]

    labels: dict[int, tuple[np.ndarray, np.ndarray]] = {}
    for path in label_paths:
        raw = np.asarray(Image.open(path))
        if raw.ndim != 2:
            raise RuntimeError(f"Expected indexed label PNG, got {raw.shape}: {path}")
        unique = set(int(value) for value in np.unique(raw))
        if not unique <= {0, 1, 2, 3}:
            raise RuntimeError(f"Unexpected label values {sorted(unique)} in {path}")
        if raw.shape != (height, width):
            raise RuntimeError(
                f"Image/label shape mismatch for {path.name}: "
                f"{(height, width)} vs {raw.shape}"
            )
        # Combine green uncertain faults and blue certain faults.
        # Use RGB because PNG palette indices vary between files.
        rgb = np.asarray(Image.open(path).convert("RGB"))
        green_fault = np.all(rgb == (44, 160, 44), axis=-1)
        blue_fault = np.all(rgb == (31, 119, 180), axis=-1)
        fault_mask = green_fault | blue_fault
        valid_mask = np.ones_like(fault_mask, dtype=bool)
        labels[section_number(path)] = (fault_mask, valid_mask)

    threshold_document = json.loads(
        args.threshold_metrics.read_text(encoding="utf-8")
    )
    threshold = float(
        threshold_document["threshold_selected_on_internal_validation"]
    )
    checkpoint = torch.load(args.checkpoint, map_location="cpu", weights_only=False)
    model = Attention3D().cuda()
    model.load_state_dict(checkpoint["model"], strict=True)
    model.eval()
    for parameter in model.parameters():
        parameter.requires_grad_(False)

    aggregate = baseline.ProbabilityHistogram(args.histogram_bins)
    rows: list[dict[str, object]] = []
    y_starts = starts(height)
    x_starts = starts(width)
    torch.cuda.reset_peak_memory_stats()
    started = time.time()
    tile_count = 0

    for label_index, label_path in enumerate(label_paths, start=1):
        number = section_number(label_path)
        center = position[number]
        context_indices = np.clip(
            np.arange(center - PATCH // 2, center + PATCH // 2),
            0,
            len(image_paths) - 1,
        )
        probability_sum = np.zeros((height, width), dtype=np.float32)
        probability_count = np.zeros((height, width), dtype=np.float32)

        for y0 in y_starts:
            for x0 in x_starts:
                cube = volume[
                    context_indices,
                    y0 : y0 + PATCH,
                    x0 : x0 + PATCH,
                ].copy()
                mean = float(cube.mean(dtype=np.float64))
                std = float(cube.std(dtype=np.float64))
                if not std > 0.0:
                    raise RuntimeError(
                        f"Constant CRACKS cube: section={number}, y={y0}, x={x0}"
                    )
                cube = (cube - mean) / std
                # Match the axis reversal used in synthetic and Thebe evaluation.
                model_cube = np.ascontiguousarray(np.transpose(cube))
                tensor = torch.from_numpy(model_cube[None, None]).cuda()
                with torch.inference_mode(), torch.autocast(
                    device_type="cuda", dtype=torch.float16
                ):
                    logits = model(tensor)
                tile_probability = (
                    torch.sigmoid(logits.float())[0, 0, :, :, PATCH // 2]
                    .cpu()
                    .numpy()
                    .T
                )
                probability_sum[
                    y0 : y0 + PATCH, x0 : x0 + PATCH
                ] += tile_probability
                probability_count[
                    y0 : y0 + PATCH, x0 : x0 + PATCH
                ] += 1.0
                tile_count += 1

        if np.any(probability_count == 0):
            raise RuntimeError(f"Incomplete spatial coverage for section {number}")
        probability = probability_sum / probability_count
        target, valid = labels[number]
        if not np.any(valid):
            raise RuntimeError(f"No scorable expert pixels in {label_path}")
        individual = baseline.ProbabilityHistogram(args.histogram_bins)
        update_histogram(individual, probability, target, valid)
        update_histogram(aggregate, probability, target, valid)
        metrics = asdict(individual.metrics(threshold))
        row: dict[str, object] = {
            "section": number,
            "valid_pixels": int(np.count_nonzero(valid)),
            "fault_pixels": int(np.count_nonzero(target & valid)),
            **metrics,
        }
        rows.append(row)
        print(
            f"expert_section={label_index:02d}/40 id={number:03d} "
            f"dice={metrics['dice']:.6f} pr_auc={metrics['pr_auc_approx']:.6f}",
            flush=True,
        )

    with (args.output_dir / "expert_per_section.csv").open(
        "w", newline="", encoding="utf-8"
    ) as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    final_metrics = asdict(aggregate.metrics(threshold))
    result = {
        "experiment": "p1_cracks_expert_zero_shot",
        "status": "complete_40_expert_sections",
        "training_performed": False,
        "weight_updates": 0,
        "checkpoint": str(args.checkpoint),
        "checkpoint_epoch": int(checkpoint.get("epoch", -1)),
        "threshold": threshold,
        "threshold_source": str(args.threshold_metrics),
        "cracks_labels_used_for_threshold": False,
        "input_sections": len(image_paths),
        "missing_nominal_section_numbers": missing_nominal_sections,
        "expert_sections_scored": len(rows),
        "image_shape": [height, width],
        "tiles_inferred": tile_count,
        "label_policy": (
            "score green and blue pixels as fault; "
            "use RGB colours and score all other pixels as background"
        ),
        "metrics_scope": "expert-labelled 2D planes only; not dense 3D ground truth",
        "cracks_expert": final_metrics,
        "efficiency": {
            "wall_seconds": time.time() - started,
            "peak_cuda_gib": torch.cuda.max_memory_allocated() / 1024**3,
        },
    }
    (args.output_dir / "final_metrics.json").write_text(
        json.dumps(result, indent=2, sort_keys=True), encoding="utf-8"
    )

    print("\n=== CRACKS EXPERT ZERO-SHOT RESULT ===")
    print(f"sections={len(rows)}")
    print(f"threshold={threshold:.6f}")
    print(f"dice={final_metrics['dice']:.6f}")
    print(f"iou={final_metrics['iou']:.6f}")
    print(f"precision={final_metrics['precision']:.6f}")
    print(f"recall={final_metrics['recall']:.6f}")
    print(f"pr_auc={final_metrics['pr_auc_approx']:.6f}")
    print(f"results={args.output_dir / 'final_metrics.json'}")


if __name__ == "__main__":
    main()
