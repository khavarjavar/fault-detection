#!/usr/bin/env python3
"""Compare completed R100, FaultSegV3, and SwinUNETR on fixed validation views.

Cases are chosen from the shared fixed validation subset using reference labels
only. Predictions never influence case selection, and test files are not read.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np
import torch

import faultseg3d_baseline as baseline
import train_r100_fp16_clean as r100
from evaluate_thebe_zero_shot_r100_pinned import ConcatenatedThebe
from train_faultsegv3_thebe_matched import FaultSegV3Logits
from train_swinunetr_thebe_matched import SwinUNETRMatched


ROOT = Path(__file__).resolve().parents[1]
ERROR_COLORS = ListedColormap(
    [(0, 0, 0, 0), (0.22, 0.90, 0.35, 0.82),
     (1.00, 0.56, 0.10, 0.82), (0.95, 0.15, 0.75, 0.82)]
)


def load_json(path: Path) -> dict:
    if not path.is_file():
        raise FileNotFoundError(path)
    return json.loads(path.read_text())


def require_complete(run_dir: Path) -> tuple[dict, dict, dict]:
    config = load_json(run_dir / "run_config.json")
    selection = load_json(run_dir / "validation_selection.json")
    status = load_json(run_dir / "status.json")
    if status["status"] != "validation_only_complete":
        raise RuntimeError(f"Run is not complete: {run_dir}: {status['status']}")
    if status.get("test_files_read") is not False:
        raise RuntimeError(f"Test policy is not closed in {run_dir}")
    if not (run_dir / "best.pt").is_file():
        raise FileNotFoundError(run_dir / "best.pt")
    return config, selection, status


def choose_cases(reader: ConcatenatedThebe, coordinates: list[tuple[int, int, int]]):
    label_rows = []
    for origin in coordinates:
        _, target, mask, _, observed, _, _ = r100.read_patch(reader, origin)
        positives = int((target[mask] > 0.5).sum()) if observed else 0
        if positives:
            label_rows.append((positives, origin))
    if len(label_rows) < 3:
        raise RuntimeError("Fewer than three fault-present fixed validation patches")
    label_rows.sort(key=lambda item: (item[0], item[1]))

    selected = []
    # One median-positive patch from each x slab preserves spatial coverage.
    for x0 in sorted({origin[0] for _, origin in label_rows}):
        slab = [item for item in label_rows if item[1][0] == x0]
        selected.append(slab[len(slab) // 2])
    # Add a weak-fault case chosen at the lower quartile, independent of models.
    for item in label_rows:
        if item[0] >= label_rows[len(label_rows) // 4][0] and item not in selected:
            selected.append(item)
            break
    if len(selected) < 3:
        for item in label_rows:
            if item not in selected:
                selected.append(item)
            if len(selected) == 3:
                break
    return selected[:3]


def infer(model: torch.nn.Module, x: torch.Tensor) -> np.ndarray:
    with torch.inference_mode(), torch.autocast("cuda", dtype=torch.float16):
        logits = model(x.cuda())
    probability = torch.sigmoid(logits.float()).cpu().numpy()[0, 0]
    return probability.transpose()


def error_map(prediction: np.ndarray, truth: np.ndarray) -> np.ndarray:
    result = np.zeros(truth.shape, dtype=np.uint8)
    result[prediction & truth] = 1
    result[prediction & ~truth] = 2
    result[~prediction & truth] = 3
    return result


def counts(prediction: np.ndarray, truth: np.ndarray) -> dict[str, int | float]:
    tp = int((prediction & truth).sum())
    fp = int((prediction & ~truth).sum())
    fn = int((~prediction & truth).sum())
    denominator = 2 * tp + fp + fn
    return {
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "section_dice": float(2 * tp / denominator) if denominator else 1.0,
    }


def geometry_metrics(
    prediction: np.ndarray,
    truth: np.ndarray,
) -> dict[str, object]:
    """Describe placement, tolerance overlap, thickness proxy, and fragmentation."""
    from scipy import ndimage

    prediction = np.asarray(prediction, dtype=bool).squeeze()
    truth = np.asarray(truth, dtype=bool).squeeze()
    if prediction.shape != truth.shape:
        raise RuntimeError(
            f"Geometry metric shape mismatch: {prediction.shape} != {truth.shape}"
        )

    prediction_positive = int(prediction.sum())
    truth_positive = int(truth.sum())
    both_empty = prediction_positive == 0 and truth_positive == 0
    one_empty = (prediction_positive == 0) != (truth_positive == 0)

    tolerance = {}
    if both_empty:
        hd95 = 0.0
        for radius in (1, 2, 4, 8):
            tolerance[str(radius)] = {
                "precision": 1.0, "recall": 1.0, "f1": 1.0,
            }
    elif one_empty:
        hd95 = float(np.sqrt(sum((size - 1) ** 2 for size in truth.shape)))
        for radius in (1, 2, 4, 8):
            tolerance[str(radius)] = {
                "precision": 0.0, "recall": 0.0, "f1": 0.0,
            }
    else:
        prediction_to_truth = ndimage.distance_transform_edt(~truth)[prediction]
        truth_to_prediction = ndimage.distance_transform_edt(~prediction)[truth]
        hd95 = float(max(
            np.percentile(prediction_to_truth, 95),
            np.percentile(truth_to_prediction, 95),
        ))
        for radius in (1, 2, 4, 8):
            precision = float(np.mean(prediction_to_truth <= radius))
            recall = float(np.mean(truth_to_prediction <= radius))
            denominator = precision + recall
            tolerance[str(radius)] = {
                "precision": precision,
                "recall": recall,
                "f1": float(2 * precision * recall / denominator)
                if denominator else 0.0,
            }

    structure = ndimage.generate_binary_structure(prediction.ndim, prediction.ndim)

    def components(mask: np.ndarray) -> dict[str, int]:
        labels, count = ndimage.label(mask, structure=structure)
        sizes = np.bincount(labels.ravel())[1:] if count else np.empty(0, dtype=int)
        return {
            "all": int(count),
            "at_least_8_voxels": int(np.sum(sizes >= 8)),
            "at_least_32_voxels": int(np.sum(sizes >= 32)),
        }

    result = {
        **baseline.structural_distances(prediction, truth),
        "hd95_voxels": hd95,
        "prediction_positive_voxels": prediction_positive,
        "reference_positive_voxels": truth_positive,
        "positive_volume_ratio": (
            float(prediction_positive / truth_positive)
            if truth_positive else None
        ),
        "prediction_components": components(prediction),
        "reference_components": components(truth),
        "tolerance_f1": tolerance,
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--r100-run", type=Path,
        default=ROOT / "runs/r100_150_seed43_20261102",
    )
    parser.add_argument(
        "--v3-run", type=Path,
        default=ROOT / "runs/faultsegv3_matched_150_seed43_20261102",
    )
    parser.add_argument(
        "--swin-run", type=Path,
        default=ROOT / "runs/swinunetr_matched_150_seed43_20261102",
    )
    parser.add_argument(
        "--output-dir", type=Path,
        default=ROOT / "reports/evaluation/r100150_vs_faultsegv3_validation_20261102",
    )
    args = parser.parse_args()
    r100_run = args.r100_run.resolve()
    v3_run = args.v3_run.resolve()
    swin_run = args.swin_run.resolve()
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)

    r100_config, r100_selection, r100_status = require_complete(r100_run)
    v3_config, v3_selection, v3_status = require_complete(v3_run)
    swin_config, swin_selection, swin_status = require_complete(swin_run)
    for name, config in (("FaultSegV3", v3_config), ("SwinUNETR", swin_config)):
        if r100_config["seed"] != config["seed"]:
            raise RuntimeError(f"Run seed differs for {name}")
        if r100_config["validation_files"] != config["validation_files"]:
            raise RuntimeError(f"Validation files differ for {name}")
        if (
            r100_config["validation_subset_coordinates"]
            != config["validation_subset_coordinates"]
        ):
            raise RuntimeError(f"Fixed validation subset differs for {name}")
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")

    r100_model = baseline.FaultSeg3D().cuda().eval()
    v3_model = FaultSegV3Logits(use_checkpoint=False).cuda().eval()
    swin_model = SwinUNETRMatched(use_checkpoint=True).cuda().eval()
    r100_checkpoint = torch.load(r100_run / "best.pt", map_location="cpu", weights_only=False)
    v3_checkpoint = torch.load(v3_run / "best.pt", map_location="cpu", weights_only=False)
    swin_checkpoint = torch.load(swin_run / "best.pt", map_location="cpu", weights_only=False)
    r100_model.load_state_dict(r100_checkpoint["model"], strict=True)
    v3_model.load_state_dict(v3_checkpoint["model"], strict=True)
    swin_model.load_state_dict(swin_checkpoint["model"], strict=True)

    coordinates = [tuple(row) for row in r100_config["validation_subset_coordinates"]]
    validation_paths = []
    for value in r100_config["validation_files"]:
        path = Path(value)
        validation_paths.append(path if path.is_absolute() else ROOT / path)
    reader = ConcatenatedThebe(validation_paths)
    manifest = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "purpose": "predefined qualitative validation comparison; test files not read",
        "selection": (
            "Reference-label-only selection from the shared fixed validation subset: "
            "median-positive patch in each x slab plus a lower-quartile positive patch; "
            "within each patch, the section with most reference fault pixels."
        ),
        "test_files_read": False,
        "r100": {
            "run": str(r100_run.relative_to(ROOT)),
            "best_epoch": r100_status["best_epoch"],
            "full_validation": r100_selection["full_validation"],
            "threshold": r100_selection["threshold"],
        },
        "faultsegv3": {
            "run": str(v3_run.relative_to(ROOT)),
            "best_epoch": v3_status["best_epoch"],
            "full_validation": v3_selection["full_validation"],
            "threshold": v3_selection["threshold"],
        },
        "swinunetr": {
            "run": str(swin_run.relative_to(ROOT)),
            "best_epoch": swin_status["best_epoch"],
            "full_validation": swin_selection["full_validation"],
            "threshold": swin_selection["threshold"],
        },
        "cases": [],
    }
    try:
        cases = choose_cases(reader, coordinates)
        fig, axes = plt.subplots(
            len(cases), 7, figsize=(29, 4.3 * len(cases)), constrained_layout=True
        )
        for row_index, (positive_voxels, origin) in enumerate(cases):
            x, target, mask, shape, _, _, _ = r100.read_patch(reader, origin)
            seismic = x.numpy()[0, 0].transpose()
            truth3d = target.numpy()[0, 0].transpose().astype(bool)
            valid3d = mask.numpy()[0, 0].transpose().astype(bool)
            r100_probability = infer(r100_model, x)
            v3_probability = infer(v3_model, x)
            swin_probability = infer(swin_model, x)
            r100_pred3d = (
                (r100_probability >= r100_selection["threshold"]) & valid3d
            )
            v3_pred3d = (
                (v3_probability >= v3_selection["threshold"]) & valid3d
            )
            swin_pred3d = (
                (swin_probability >= swin_selection["threshold"]) & valid3d
            )
            local_x = int(np.argmax((truth3d & valid3d).sum(axis=(1, 2))))
            cut = np.s_[local_x, :shape[1], :shape[2]]
            amp = seismic[cut].T
            truth = (truth3d & valid3d)[cut].T
            valid = valid3d[cut].T
            r100_prob = r100_probability[cut].T
            v3_prob = v3_probability[cut].T
            swin_prob = swin_probability[cut].T
            r100_pred = (r100_prob >= r100_selection["threshold"]) & valid
            v3_pred = (v3_prob >= v3_selection["threshold"]) & valid
            swin_pred = (swin_prob >= swin_selection["threshold"]) & valid

            panels = axes[row_index]
            for panel in panels:
                panel.imshow(
                    np.clip(amp, -2.5, 2.5), cmap="gray", vmin=-2.5, vmax=2.5,
                    origin="upper", aspect="auto", interpolation="nearest",
                )
                panel.set_xlabel("survey y within tile")
                panel.set_ylabel("survey z within tile")
            panels[0].imshow(
                np.ma.masked_where(~truth, truth),
                cmap=ListedColormap(["#fa1775"]), alpha=0.80,
                origin="upper", aspect="auto", interpolation="nearest",
            )
            patch_id = "x%04d_y%04d_z%04d" % origin
            panels[0].set_title(f"{patch_id}\nreference fault (pink)")
            panels[1].imshow(
                np.ma.masked_where(~valid, r100_prob), cmap="magma", vmin=0, vmax=1,
                alpha=0.82, origin="upper", aspect="auto", interpolation="nearest",
            )
            panels[1].set_title(f"R100 probability\nthreshold {r100_selection['threshold']:.4f}")
            panels[2].imshow(
                np.ma.masked_where(error_map(r100_pred, truth) == 0,
                                   error_map(r100_pred, truth)),
                cmap=ERROR_COLORS, vmin=0, vmax=3,
                origin="upper", aspect="auto", interpolation="nearest",
            )
            panels[2].set_title("R100: TP green · FP orange · FN pink")
            panels[3].imshow(
                np.ma.masked_where(~valid, v3_prob), cmap="magma", vmin=0, vmax=1,
                alpha=0.82, origin="upper", aspect="auto", interpolation="nearest",
            )
            panels[3].set_title(f"FaultSegV3 probability\nthreshold {v3_selection['threshold']:.4f}")
            panels[4].imshow(
                np.ma.masked_where(error_map(v3_pred, truth) == 0,
                                   error_map(v3_pred, truth)),
                cmap=ERROR_COLORS, vmin=0, vmax=3,
                origin="upper", aspect="auto", interpolation="nearest",
            )
            panels[4].set_title("V3: TP green · FP orange · FN pink")
            panels[5].imshow(
                np.ma.masked_where(~valid, swin_prob), cmap="magma", vmin=0, vmax=1,
                alpha=0.82, origin="upper", aspect="auto", interpolation="nearest",
            )
            panels[5].set_title(
                f"SwinUNETR probability\nthreshold {swin_selection['threshold']:.4f}"
            )
            swin_error = error_map(swin_pred, truth)
            panels[6].imshow(
                np.ma.masked_where(swin_error == 0, swin_error),
                cmap=ERROR_COLORS, vmin=0, vmax=3,
                origin="upper", aspect="auto", interpolation="nearest",
            )
            panels[6].set_title("Swin: TP green · FP orange · FN pink")
            manifest["cases"].append(
                {
                    "patch_id": patch_id,
                    "origin": origin,
                    "patch_reference_positive_voxels": positive_voxels,
                    "displayed_x": origin[0] + local_x,
                    "displayed_reference_positive_pixels": int(truth.sum()),
                    "r100": {
                        **counts(r100_pred, truth),
                        "displayed_section_geometry": geometry_metrics(r100_pred, truth),
                        "patch_geometry": geometry_metrics(
                            r100_pred3d, truth3d & valid3d
                        ),
                    },
                    "faultsegv3": {
                        **counts(v3_pred, truth),
                        "displayed_section_geometry": geometry_metrics(v3_pred, truth),
                        "patch_geometry": geometry_metrics(v3_pred3d, truth3d & valid3d),
                    },
                    "swinunetr": {
                        **counts(swin_pred, truth),
                        "displayed_section_geometry": geometry_metrics(swin_pred, truth),
                        "patch_geometry": geometry_metrics(
                            swin_pred3d, truth3d & valid3d
                        ),
                    },
                }
            )
    finally:
        reader.close()
    fig.suptitle(
        "Thebe validation: matched seed-43 R100, high-resolution V3, and SwinUNETR",
        fontsize=15,
    )
    figure_path = output / "validation_casebook.png"
    fig.savefig(figure_path, dpi=150)
    plt.close(fig)
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({"figure": str(figure_path), "cases": manifest["cases"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
