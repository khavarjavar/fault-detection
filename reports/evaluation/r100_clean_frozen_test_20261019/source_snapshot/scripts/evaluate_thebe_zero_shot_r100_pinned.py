#!/usr/bin/env python3
"""Zero-shot evaluation of synthetic Baseline A on official real Thebe test data.

This script:
- performs no training or weight updates;
- uses only test*.h5;
- takes its threshold from synthetic validation;
- standardizes each 128^3 input patch like Baseline A;
- covers the complete test volume exactly once;
- excludes zero-padding from all metrics.
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import itertools
import json
import math
import re
import sys
import time
from dataclasses import asdict
from pathlib import Path
from typing import Any

import h5py
import numpy as np
import torch


def natural_key(path: Path) -> list[object]:
    return [
        int(part) if part.isdigit() else part.lower()
        for part in re.split(r"(\d+)", path.name)
    ]


def load_baseline_module(path: Path):
    specification = importlib.util.spec_from_file_location(
        "faultseg3d_baseline_imported",
        path,
    )
    if specification is None or specification.loader is None:
        raise RuntimeError(f"Cannot import baseline module: {path}")

    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


class ConcatenatedThebe:
    """Read ordered test H5 blocks as one volume along axis zero."""

    def __init__(self, paths: list[Path]) -> None:
        if not paths:
            raise RuntimeError("No Thebe test H5 files were supplied")

        self.paths = paths
        self.handles = [h5py.File(path, "r") for path in paths]
        self.offsets: list[int] = []
        self.lengths: list[int] = []

        reference_tail: tuple[int, int] | None = None
        running = 0

        for path, handle in zip(self.paths, self.handles):
            if "seismic" not in handle or "fault" not in handle:
                raise RuntimeError(
                    f"{path} must contain datasets named seismic and fault"
                )

            seismic_shape = tuple(handle["seismic"].shape)
            fault_shape = tuple(handle["fault"].shape)

            if seismic_shape != fault_shape or len(seismic_shape) != 3:
                raise RuntimeError(
                    f"Shape mismatch in {path}: "
                    f"seismic={seismic_shape}, fault={fault_shape}"
                )

            if reference_tail is None:
                reference_tail = seismic_shape[1:]
            elif seismic_shape[1:] != reference_tail:
                raise RuntimeError(
                    f"Incompatible spatial shape in {path}: {seismic_shape}"
                )

            self.offsets.append(running)
            self.lengths.append(seismic_shape[0])
            running += seismic_shape[0]

        assert reference_tail is not None
        self.shape = (running, *reference_tail)

    def close(self) -> None:
        for handle in self.handles:
            handle.close()

    def read(
        self,
        key: str,
        x0: int,
        x1: int,
        y0: int,
        y1: int,
        z0: int,
        z1: int,
    ) -> np.ndarray:
        pieces: list[np.ndarray] = []

        for offset, length, handle in zip(
            self.offsets,
            self.lengths,
            self.handles,
        ):
            block_end = offset + length
            overlap_start = max(x0, offset)
            overlap_end = min(x1, block_end)

            if overlap_start >= overlap_end:
                continue

            local_start = overlap_start - offset
            local_end = overlap_end - offset

            piece = np.asarray(
                handle[key][local_start:local_end, y0:y1, z0:z1]
            )
            pieces.append(piece)

        if not pieces:
            raise RuntimeError(
                f"No data read for {key}: "
                f"x={x0}:{x1}, y={y0}:{y1}, z={z0}:{z1}"
            )

        if len(pieces) == 1:
            return pieces[0]

        return np.concatenate(pieces, axis=0)


def summarize_rows(
    rows: list[dict[str, Any]],
) -> dict[str, dict[str, float]]:
    selected = (
        "dice",
        "iou",
        "precision",
        "recall",
        "specificity",
        "balanced_accuracy",
        "accuracy",
        "mcc",
        "pr_auc_approx",
        "roc_auc_approx",
        "modified_hausdorff_voxels",
        "bidirectional_chamfer_voxels",
        "inference_seconds",
    )

    summary: dict[str, dict[str, float]] = {}

    for key in selected:
        values = np.asarray(
            [float(row[key]) for row in rows if key in row],
            dtype=np.float64,
        )

        if values.size == 0:
            continue

        summary[key] = {
            "mean": float(values.mean()),
            "std": float(values.std()),
            "median": float(np.median(values)),
            "min": float(values.min()),
            "max": float(values.max()),
        }

    return summary


def write_csv_atomic(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return

    temporary = path.with_suffix(path.suffix + ".part")

    with temporary.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    temporary.replace(path)


def middle_slices(array: np.ndarray) -> dict[str, np.ndarray]:
    return {
        "axis0": array[array.shape[0] // 2, :, :],
        "axis1": array[:, array.shape[1] // 2, :],
        "axis2": array[:, :, array.shape[2] // 2],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--baseline-script",
        type=Path,
        default=Path("scripts/faultseg3d_baseline.py"),
    )
    parser.add_argument(
        "--checkpoint",
        type=Path,
        default=Path(
            "runs/baseline_A_synthetic_bce_seed42/best.pt"
        ),
    )
    parser.add_argument(
        "--threshold-metrics",
        type=Path,
        default=Path(
            "runs/baseline_A_synthetic_bce_seed42/final_metrics.json"
        ),
    )
    parser.add_argument(
        "--thebe-root",
        type=Path,
        default=Path("data/processed/thebe_h5"),
    )
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument(
        "--max-patches",
        type=int,
        default=None,
        help="For smoke testing only. Omit for complete evaluation.",
    )
    parser.add_argument("--save-examples", type=int, default=12)
    return parser


def main() -> None:
    args = build_parser().parse_args()

    if not torch.cuda.is_available():
        raise RuntimeError(
            "CUDA GPU is unavailable. Attach a GPU before evaluation."
        )

    required = (
        args.baseline_script,
        args.checkpoint,
        args.threshold_metrics,
    )
    for path in required:
        if not path.is_file():
            raise FileNotFoundError(path)

    if args.output_dir.exists() and any(args.output_dir.iterdir()):
        raise RuntimeError(
            f"Output directory is not empty: {args.output_dir}"
        )
    args.output_dir.mkdir(parents=True, exist_ok=True)

    example_dir = args.output_dir / "prediction_examples"
    example_dir.mkdir(parents=True, exist_ok=True)

    test_files = sorted(
        args.thebe_root.glob("test*.h5"),
        key=natural_key,
    )
    if not test_files:
        raise RuntimeError(
            f"No official test*.h5 files found in {args.thebe_root}"
        )

    # Explicitly reject accidental train/validation use.
    for path in test_files:
        if not path.name.startswith("test"):
            raise RuntimeError(f"Non-test file selected: {path}")

    threshold_document = json.loads(
        args.threshold_metrics.read_text(encoding="utf-8")
    )
    threshold = float(
        threshold_document[
            "threshold_selected_on_internal_validation"
        ]
    )

    if not 0.0 < threshold < 1.0:
        raise RuntimeError(f"Invalid frozen threshold: {threshold}")

    baseline = load_baseline_module(args.baseline_script)

    volume_shape = tuple(int(value) for value in baseline.VOLUME_SHAPE)
    if len(volume_shape) != 3 or len(set(volume_shape)) != 1:
        raise RuntimeError(
            f"Expected a cubic baseline volume shape, got {volume_shape}"
        )
    patch_size = volume_shape[0]

    checkpoint = torch.load(
        args.checkpoint,
        map_location="cpu",
        weights_only=False,
    )
    if "model" not in checkpoint:
        raise RuntimeError("Checkpoint does not contain model weights")

    checkpoint_args = checkpoint.get("args", {})
    histogram_bins = int(
        checkpoint_args.get("histogram_bins", 2048)
    )

    device = torch.device("cuda")
    model = baseline.FaultSeg3D().to(device)
    model.load_state_dict(checkpoint["model"], strict=True)
    model.eval()

    for parameter in model.parameters():
        parameter.requires_grad_(False)

    torch.manual_seed(42)
    np.random.seed(42)
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True
    torch.cuda.reset_peak_memory_stats()

    reader = ConcatenatedThebe(test_files)
    total_shape = reader.shape

    x_starts = list(range(0, total_shape[0], patch_size))
    y_starts = list(range(0, total_shape[1], patch_size))
    z_starts = list(range(0, total_shape[2], patch_size))

    coordinates = list(
        itertools.product(x_starts, y_starts, z_starts)
    )
    full_patch_count = len(coordinates)

    if args.max_patches is not None:
        if args.max_patches <= 0:
            raise ValueError("--max-patches must be positive")
        coordinates = coordinates[: args.max_patches]

    complete_evaluation = len(coordinates) == full_patch_count

    run_configuration = {
        "experiment": "A_to_T0_zero_shot",
        "training_performed": False,
        "weight_updates": 0,
        "checkpoint": str(args.checkpoint),
        "checkpoint_epoch": int(checkpoint.get("epoch", -1)),
        "checkpoint_training_data": checkpoint_args.get(
            "data_root",
            "unknown",
        ),
        "threshold": threshold,
        "threshold_source": str(args.threshold_metrics),
        "threshold_selected_using_thebe": False,
        "data_split": "official Thebe test only",
        "test_files": [str(path) for path in test_files],
        "test_block_count": len(test_files),
        "concatenated_test_shape": list(total_shape),
        "patch_shape": list(volume_shape),
        "patch_count_planned": full_patch_count,
        "patch_count_this_run": len(coordinates),
        "complete_official_test_evaluation": complete_evaluation,
        "normalization": (
            "independent z-score on each valid 3D patch, "
            "matching Baseline A"
        ),
        "axis_transform": "np.transpose, matching Baseline A",
        "edge_policy": (
            "zero-pad normalized inputs to 128^3; "
            "exclude padding from every metric"
        ),
        "overlap_policy": (
            "non-overlapping partition; every valid voxel evaluated once"
        ),
        "no_data_policy": "score only finite raw seismic != 0",
        "evaluator_patch": "raw_zero_no_data_mask_v1",
        "histogram_bins": histogram_bins,
    }

    (args.output_dir / "run_configuration.json").write_text(
        json.dumps(run_configuration, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    aggregate = baseline.ProbabilityHistogram(histogram_bins)
    rows: list[dict[str, Any]] = []
    evaluated_voxels = 0
    valid_data_voxels = 0
    excluded_no_data_voxels = 0
    positive_labels_outside_valid_mask = 0
    total_inference_seconds = 0.0
    saved_examples = 0
    started = time.time()

    try:
        for patch_number, (x0, y0, z0) in enumerate(
            coordinates,
            start=1,
        ):
            x1 = min(x0 + patch_size, total_shape[0])
            y1 = min(y0 + patch_size, total_shape[1])
            z1 = min(z0 + patch_size, total_shape[2])

            size_x = x1 - x0
            size_y = y1 - y0
            size_z = z1 - z0

            seismic_raw = reader.read(
                "seismic", x0, x1, y0, y1, z0, z1
            ).astype(np.float32, copy=False)
            fault_raw = reader.read(
                "fault", x0, x1, y0, y1, z0, z1
            ).astype(np.uint8, copy=False)

            expected_shape = (size_x, size_y, size_z)
            if seismic_raw.shape != expected_shape:
                raise RuntimeError(
                    f"Unexpected seismic shape: "
                    f"{seismic_raw.shape} != {expected_shape}"
                )
            if fault_raw.shape != expected_shape:
                raise RuntimeError(
                    f"Unexpected fault shape: "
                    f"{fault_raw.shape} != {expected_shape}"
                )

            finite_raw = np.isfinite(seismic_raw)
            if not finite_raw.all():
                raise RuntimeError(
                    f"NaN/Inf in patch starting at {(x0, y0, z0)}"
                )
            if fault_raw.min() < 0 or fault_raw.max() > 1:
                raise RuntimeError(
                    f"Non-binary fault values at {(x0, y0, z0)}"
                )

            data_valid_raw = finite_raw & (seismic_raw != 0.0)
            patch_valid_voxels = int(
                np.count_nonzero(data_valid_raw)
            )
            patch_raw_voxels = int(seismic_raw.size)
            patch_excluded_voxels = (
                patch_raw_voxels - patch_valid_voxels
            )
            masked_positive_patch = int(
                np.count_nonzero(
                    (fault_raw > 0) & ~data_valid_raw
                )
            )

            valid_data_voxels += patch_valid_voxels
            excluded_no_data_voxels += patch_excluded_voxels
            positive_labels_outside_valid_mask += (
                masked_positive_patch
            )

            seismic_normalized = np.zeros_like(
                seismic_raw,
                dtype=np.float32,
            )

            if patch_valid_voxels:
                values = seismic_raw[data_valid_raw]
                patch_mean = float(
                    values.mean(dtype=np.float64)
                )
                patch_std = float(
                    values.std(dtype=np.float64)
                )

                if not patch_std > 0.0:
                    raise RuntimeError(
                        "Zero standard deviation among valid "
                        f"voxels at {(x0, y0, z0)}"
                    )

                seismic_normalized[data_valid_raw] = (
                    seismic_raw[data_valid_raw] - patch_mean
                ) / patch_std
            else:
                patch_mean = 0.0
                patch_std = 1.0

            seismic_padded = np.zeros(
                volume_shape,
                dtype=np.float32,
            )
            fault_padded = np.zeros(
                volume_shape,
                dtype=np.float32,
            )
            validity_padded = np.zeros(
                volume_shape,
                dtype=np.bool_,
            )

            seismic_padded[
                :size_x, :size_y, :size_z
            ] = seismic_normalized
            fault_padded[
                :size_x, :size_y, :size_z
            ] = fault_raw
            validity_padded[
                :size_x, :size_y, :size_z
            ] = data_valid_raw

            # Match Baseline A axis reversal.
            seismic_model = np.ascontiguousarray(
                np.transpose(seismic_padded),
                dtype=np.float32,
            )
            fault_model = np.ascontiguousarray(
                np.transpose(fault_padded),
                dtype=np.float32,
            )
            validity_model = np.ascontiguousarray(
                np.transpose(validity_padded),
                dtype=np.bool_,
            )

            model_input = torch.from_numpy(
                seismic_model[None, None]
            ).to(device)

            target_tensor = torch.from_numpy(
                fault_model
            ).to(device)
            validity_tensor = torch.from_numpy(
                validity_model
            ).to(device)

            torch.cuda.synchronize()
            inference_started = time.perf_counter()

            with torch.inference_mode():
                with torch.autocast(
                    device_type="cuda",
                    dtype=torch.float16,
                ):
                    logits = model(model_input)

                probability = torch.sigmoid(
                    logits.float()
                )[0, 0]

            torch.cuda.synchronize()
            inference_seconds = (
                time.perf_counter() - inference_started
            )

            total_inference_seconds += inference_seconds

            # Dimensions reverse after np.transpose.
            valid_z, valid_y, valid_x = (
                size_z,
                size_y,
                size_x,
            )

            probability_valid = probability[
                :valid_z, :valid_y, :valid_x
            ]
            target_valid = target_tensor[
                :valid_z, :valid_y, :valid_x
            ]
            metric_mask = validity_tensor[
                :valid_z, :valid_y, :valid_x
            ]

            raw_voxels = valid_z * valid_y * valid_x
            metric_voxels = int(metric_mask.sum().item())
            evaluated_voxels += raw_voxels

            if metric_voxels == 0:
                continue

            probability_scored = probability_valid[
                metric_mask
            ]
            target_scored = target_valid[metric_mask]

            aggregate.update_probabilities(
                probability_scored,
                target_scored,
            )

            individual = baseline.ProbabilityHistogram(
                histogram_bins
            )
            individual.update_probabilities(
                probability_scored,
                target_scored,
            )

            row: dict[str, Any] = {
                "patch_id": (
                    f"x{x0:04d}_y{y0:04d}_z{z0:04d}"
                ),
                "raw_x_start": x0,
                "raw_x_stop": x1,
                "raw_y_start": y0,
                "raw_y_stop": y1,
                "raw_z_start": z0,
                "raw_z_stop": z1,
                "raw_voxels": raw_voxels,
                "valid_voxels": metric_voxels,
                "excluded_no_data_voxels": (
                    patch_excluded_voxels
                ),
                "positive_labels_outside_valid_mask": (
                    masked_positive_patch
                ),
                "normalization_mean": patch_mean,
                "normalization_std": patch_std,
                **asdict(individual.metrics(threshold)),
            }

            probability_numpy = (
                probability_valid.detach().cpu().numpy()
            )
            target_numpy = (
                target_valid.detach().cpu().numpy() >= 0.5
            )
            validity_numpy = validity_model[
                :valid_z, :valid_y, :valid_x
            ]
            prediction_numpy = (
                probability_numpy >= threshold
            )

            prediction_numpy &= validity_numpy
            target_numpy &= validity_numpy

            row.update(
                baseline.structural_distances(
                    prediction_numpy,
                    target_numpy,
                )
            )
            row["inference_seconds"] = inference_seconds
            rows.append(row)

            if (
                saved_examples < args.save_examples
                and bool(target_numpy.any())
            ):
                seismic_valid = seismic_model[
                    :valid_z, :valid_y, :valid_x
                ]

                arrays: dict[str, np.ndarray] = {
                    "coordinates_raw": np.asarray(
                        [x0, x1, y0, y1, z0, z1],
                        dtype=np.int32,
                    ),
                    "threshold": np.asarray(
                        threshold,
                        dtype=np.float32,
                    ),
                }

                for prefix, array in (
                    ("seismic", seismic_valid),
                    ("validity", validity_numpy.astype(np.uint8)),
                    ("probability", probability_numpy),
                    ("target", target_numpy.astype(np.uint8)),
                    (
                        "prediction",
                        prediction_numpy.astype(np.uint8),
                    ),
                ):
                    for axis_name, image in middle_slices(
                        array
                    ).items():
                        arrays[
                            f"{prefix}_{axis_name}"
                        ] = image

                np.savez_compressed(
                    example_dir
                    / f"example_{saved_examples + 1:02d}_"
                    f"{row['patch_id']}.npz",
                    **arrays,
                )
                saved_examples += 1

            if (
                patch_number % 25 == 0
                or patch_number == len(coordinates)
            ):
                write_csv_atomic(
                    args.output_dir / "test_per_patch.csv",
                    rows,
                )
                print(
                    f"processed={patch_number}/"
                    f"{len(coordinates)} "
                    f"elapsed_minutes="
                    f"{(time.time() - started) / 60.0:.2f}",
                    flush=True,
                )

    finally:
        reader.close()

    if complete_evaluation:
        expected_voxels = int(math.prod(total_shape))
        if evaluated_voxels != expected_voxels:
            raise RuntimeError(
                f"Coverage failure: evaluated "
                f"{evaluated_voxels} voxels, "
                f"expected {expected_voxels}"
            )

    aggregate_metrics = asdict(
        aggregate.metrics(threshold)
    )
    elapsed_seconds = time.time() - started

    final_result = {
        "experiment": "A_to_T0_zero_shot",
        "status": (
            "complete_official_test"
            if complete_evaluation
            else "smoke_test_only"
        ),
        "training_performed": False,
        "weight_updates": 0,
        "threshold": threshold,
        "threshold_source": (
            "Baseline A synthetic validation"
        ),
        "thebe_labels_used_for_threshold": False,
        "official_thebe_test": aggregate_metrics,
        "official_thebe_test_per_patch_summary": (
            summarize_rows(rows)
        ),
        "data": {
            "test_files": [str(path) for path in test_files],
            "test_shape": list(total_shape),
            "patch_shape": list(volume_shape),
            "patches_inferred": len(coordinates),
            "patches_scored": len(rows),
            "full_patch_count": full_patch_count,
            "raw_voxels_covered": evaluated_voxels,
            "valid_data_voxels_evaluated": (
                valid_data_voxels
            ),
            "excluded_no_data_voxels": (
                excluded_no_data_voxels
            ),
            "positive_labels_outside_valid_mask": (
                positive_labels_outside_valid_mask
            ),
            "valid_data_fraction": (
                valid_data_voxels / evaluated_voxels
            ),
            "expected_full_test_voxels": int(
                math.prod(total_shape)
            ),
            "complete_coverage": complete_evaluation,
            "overlap": False,
            "padding_counted_in_metrics": False,
        },
        "efficiency": {
            "wall_seconds": elapsed_seconds,
            "total_model_inference_seconds": (
                total_inference_seconds
            ),
            "mean_model_inference_seconds_per_patch": (
                total_inference_seconds / len(coordinates)
            ),
            "peak_cuda_gib": (
                torch.cuda.max_memory_allocated()
                / 1024**3
            ),
        },
        "prediction_examples_saved": saved_examples,
        "metric_notes": {
            "distance_units": "voxels",
            "metric_domain": "finite nonzero raw Thebe voxels",
            "modified_hausdorff": (
                "max of directed mean nearest-point distances"
            ),
            "bidirectional_chamfer": (
                "sum of directed mean nearest-point distances"
            ),
            "one_empty_mask_policy": (
                "valid-patch diagonal penalty"
            ),
            "important": (
                "These results measure zero-shot transfer "
                "from synthetic FaultSeg3D to real Thebe."
            ),
        },
    }

    temporary_json = (
        args.output_dir / "final_metrics.json.part"
    )
    temporary_json.write_text(
        json.dumps(
            final_result,
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    temporary_json.replace(
        args.output_dir / "final_metrics.json"
    )

    write_csv_atomic(
        args.output_dir / "test_per_patch.csv",
        rows,
    )

    print("\n=== ZERO-SHOT RESULT ===")
    print(f"status={final_result['status']}")
    print(f"threshold={threshold:.6f}")
    print(
        f"dice={aggregate_metrics['dice']:.6f}"
    )
    print(
        f"iou={aggregate_metrics['iou']:.6f}"
    )
    print(
        f"precision={aggregate_metrics['precision']:.6f}"
    )
    print(
        f"recall={aggregate_metrics['recall']:.6f}"
    )
    print(
        f"mcc={aggregate_metrics['mcc']:.6f}"
    )
    print(
        f"pr_auc={aggregate_metrics['pr_auc_approx']:.6f}"
    )
    print(
        "results="
        f"{args.output_dir / 'final_metrics.json'}"
    )


if __name__ == "__main__":
    main()
