#!/usr/bin/env python3
"""Render validation and frozen-test casebooks for FaultEdgeFormer.

The checkpoint and threshold come from the completed frozen evaluation.
Validation views are selected from labels in the fixed validation subset.
Test views reuse the previously frozen R100 qualitative locations, preventing
prediction-driven case selection.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np
import torch

import evaluate_faultedgeformer_frozen_test as frozen_eval
import train_r100_fp16_clean as r100
from evaluate_thebe_zero_shot_r100_pinned import ConcatenatedThebe


ROOT = Path(__file__).resolve().parents[1]
TEST_CASES = ((0, 512, 896), (256, 1792, 1024), (512, 1536, 768))
ERROR_COLORS = ListedColormap(
    [(0, 0, 0, 0), (0.22, 0.90, 0.35, 0.84),
     (1.00, 0.56, 0.10, 0.84), (0.95, 0.15, 0.75, 0.84)]
)


def read_json(path: Path) -> dict:
    if not path.is_file():
        raise FileNotFoundError(path)
    return json.loads(path.read_text())


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(8 * 1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def choose_validation_cases(reader, coordinates):
    """Choose three fault-present cases from labels before model inference."""
    rows = []
    for origin in coordinates:
        _, target, mask, _, observed, _, _ = r100.read_patch(reader, origin)
        positives = int((target[mask] > 0.5).sum()) if observed else 0
        if positives:
            rows.append((positives, origin))
    if len(rows) < 3:
        raise RuntimeError("Fewer than three fault-present validation patches")
    rows.sort(key=lambda item: (item[0], item[1]))
    selected = []
    for x0 in sorted({origin[0] for _, origin in rows}):
        slab = [item for item in rows if item[1][0] == x0]
        selected.append(slab[len(slab) // 2])
    lower_quartile = rows[len(rows) // 4][0]
    for item in rows:
        if item[0] >= lower_quartile and item not in selected:
            selected.append(item)
            break
    if len(selected) < 3:
        for item in rows:
            if item not in selected:
                selected.append(item)
            if len(selected) == 3:
                break
    return [origin for _, origin in selected[:3]]


def infer(model: torch.nn.Module, x: torch.Tensor) -> np.ndarray:
    with torch.inference_mode(), torch.autocast("cuda", dtype=torch.float16):
        logits = model(x.cuda())
    # Model axes are z,y,x. Restore survey axes x,y,z for visualization.
    return torch.sigmoid(logits.float()).cpu().numpy()[0, 0].transpose()


def binary_metrics(prediction: np.ndarray, truth: np.ndarray):
    tp = int((prediction & truth).sum())
    fp = int((prediction & ~truth).sum())
    fn = int((~prediction & truth).sum())
    return {
        "tp": tp, "fp": fp, "fn": fn,
        "dice": float(2 * tp / (2 * tp + fp + fn)) if 2 * tp + fp + fn else 1.0,
        "precision": float(tp / (tp + fp)) if tp + fp else 1.0,
        "recall": float(tp / (tp + fn)) if tp + fn else 1.0,
    }


def error_map(prediction: np.ndarray, truth: np.ndarray) -> np.ndarray:
    result = np.zeros(truth.shape, dtype=np.uint8)
    result[prediction & truth] = 1
    result[prediction & ~truth] = 2
    result[~prediction & truth] = 3
    return result


def render_split(
    *, split, reader, origins, model, threshold, full_metrics, output, selection_text
):
    fig, axes = plt.subplots(
        len(origins), 4, figsize=(19, 4.35 * len(origins)), constrained_layout=True
    )
    if len(origins) == 1:
        axes = axes[None, :]
    case_rows = []
    for row_index, origin in enumerate(origins):
        x, target, mask, shape, observed, excluded_positive, _ = r100.read_patch(
            reader, origin
        )
        if not observed:
            raise RuntimeError(f"Selected {split} case has no observed voxels: {origin}")
        probability = infer(model, x)
        seismic = x.numpy()[0, 0].transpose()
        truth3d = target.numpy()[0, 0].transpose().astype(bool)
        valid3d = mask.numpy()[0, 0].transpose().astype(bool)
        truth3d &= valid3d
        prediction3d = (probability >= threshold) & valid3d
        local_x = int(np.argmax(truth3d.sum(axis=(1, 2))))
        cut = np.s_[local_x, : shape[1], : shape[2]]
        amplitude = seismic[cut].T
        truth = truth3d[cut].T
        valid = valid3d[cut].T
        prediction = prediction3d[cut].T
        confidence = probability[cut].T
        section_metrics = binary_metrics(prediction, truth)
        patch_metrics = binary_metrics(prediction3d, truth3d)
        errors = error_map(prediction, truth)
        patch_id = "x%04d_y%04d_z%04d" % origin

        panels = axes[row_index]
        for panel in panels:
            panel.imshow(
                np.clip(amplitude, -2.5, 2.5), cmap="gray", vmin=-2.5, vmax=2.5,
                origin="upper", aspect="auto", interpolation="nearest",
            )
            panel.set_xlabel("survey y within tile")
            panel.set_ylabel("survey z within tile")
        panels[0].imshow(
            np.ma.masked_where(~truth, truth), cmap=ListedColormap(["#fa1775"]),
            alpha=0.80, origin="upper", aspect="auto", interpolation="nearest",
        )
        panels[0].set_title(
            f"{patch_id}, survey x={origin[0] + local_x}\nreference fault (pink)"
        )
        panels[1].imshow(
            np.ma.masked_where(~valid, confidence), cmap="magma", vmin=0, vmax=1,
            alpha=0.82, origin="upper", aspect="auto", interpolation="nearest",
        )
        panels[1].set_title("fault probability over seismic")
        panels[2].imshow(
            np.ma.masked_where(~prediction, prediction),
            cmap=ListedColormap(["#ffcd28"]), alpha=0.80,
            origin="upper", aspect="auto", interpolation="nearest",
        )
        panels[2].set_title(
            f"threshold {threshold:.4f}\nsection Dice {section_metrics['dice']:.3f}"
        )
        panels[3].imshow(
            np.ma.masked_where(errors == 0, errors), cmap=ERROR_COLORS,
            vmin=0, vmax=3, origin="upper", aspect="auto", interpolation="nearest",
        )
        panels[3].set_title("TP green · FP orange · FN pink")
        case_rows.append({
            "patch_id": patch_id, "origin": list(origin),
            "actual_shape_xyz": list(shape),
            "displayed_survey_x": origin[0] + local_x,
            "valid_voxels": observed,
            "excluded_positive_labels": excluded_positive,
            "patch_positive_voxels": int(truth3d.sum()),
            "section_positive_pixels": int(truth.sum()),
            "patch_metrics_at_frozen_threshold": patch_metrics,
            "displayed_section_metrics_at_frozen_threshold": section_metrics,
        })
    fig.suptitle(
        f"FaultEdgeFormer-inspired · Thebe {split} · full {split} Dice "
        f"{full_metrics['dice']:.4f}, PR-AUC {full_metrics['pr_auc_approx']:.4f}\n"
        f"{selection_text}", fontsize=14,
    )
    fig.savefig(output / f"{split}_casebook.png", dpi=160)
    plt.close(fig)
    return case_rows


def render_summary(result: dict, histogram_path: Path, output: Path) -> None:
    histograms = np.load(histogram_path)
    fig, axes = plt.subplots(1, 2, figsize=(13, 5), constrained_layout=True)
    metric_names = ("dice", "precision", "recall", "pr_auc_approx")
    x = np.arange(len(metric_names))
    val = [result["validation"]["metrics"][name] for name in metric_names]
    test = [result["test"]["metrics"][name] for name in metric_names]
    width = 0.36
    axes[0].bar(x - width / 2, val, width, label="validation", color="#4c9cb5")
    axes[0].bar(x + width / 2, test, width, label="frozen test", color="#c44d87")
    axes[0].set_xticks(x, ["Dice", "Precision", "Recall", "PR-AUC"])
    axes[0].set_ylim(0, 0.75)
    axes[0].set_title("Complete-volume metrics at validation-frozen threshold")
    axes[0].grid(axis="y", alpha=0.25)
    axes[0].legend()
    for split, color in (("validation", "#4c9cb5"), ("test", "#c44d87")):
        positive = histograms[f"{split}_positive"].astype(np.float64)
        negative = histograms[f"{split}_negative"].astype(np.float64)
        tp = np.cumsum(positive[::-1])
        fp = np.cumsum(negative[::-1])
        recall = tp / tp[-1]
        precision = np.divide(tp, tp + fp, out=np.ones_like(tp), where=tp + fp > 0)
        axes[1].plot(
            recall, precision, lw=2, color=color,
            label=f"{split} (AUC {result[split]['metrics']['pr_auc_approx']:.3f})",
        )
    axes[1].set(xlim=(0, 1), ylim=(0, 1), xlabel="Recall", ylabel="Precision")
    axes[1].set_title("Complete-volume precision–recall curves")
    axes[1].grid(alpha=0.25)
    axes[1].legend(loc="upper right")
    fig.savefig(output / "frozen_metrics_summary.png", dpi=160)
    plt.close(fig)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--run-dir", type=Path,
        default=Path("runs/faultedgeformer_thebe_full_seed42_20261026"),
    )
    parser.add_argument(
        "--data-root", type=Path, default=Path("data/processed/thebe_h5")
    )
    parser.add_argument(
        "--evaluation-dir", type=Path,
        default=ROOT / "reports/evaluation/faultedgeformer_thebe_full_seed42_20261026",
    )
    args = parser.parse_args()
    # Preserve the checkpoint spelling recorded before the frozen test.
    run_dir = args.run_dir
    # The frozen evaluator intentionally compares the original relative paths
    # against configs/r100_test_data_manifest.json. Keep that representation.
    data_root = args.data_root
    output = args.evaluation_dir.resolve()
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")
    result = read_json(output / "result.json")
    if result.get("status") != "complete" or result.get("test_threshold_tuning") is not False:
        raise RuntimeError("Frozen evaluation result is incomplete or test-tuned")
    config, selection, val_paths, test_paths, frozen = frozen_eval.preflight(
        run_dir, data_root, output
    )
    if result["checkpoint_sha256"] != sha256(run_dir / "best.pt"):
        raise RuntimeError("Checkpoint differs from completed frozen evaluation")
    if float(result["threshold"]) != float(selection["threshold"]):
        raise RuntimeError("Result and validation selection thresholds differ")
    model = frozen_eval.load_model(config, selection, run_dir)
    validation_reader = ConcatenatedThebe(val_paths)
    test_reader = ConcatenatedThebe(test_paths)
    manifest = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "experiment": result["experiment"], "claim_scope": result["claim_scope"],
        "checkpoint": str(run_dir / "best.pt"),
        "checkpoint_sha256": frozen["checkpoint_sha256"],
        "checkpoint_epoch": result["checkpoint_epoch"],
        "threshold": result["threshold"],
        "threshold_source": result["threshold_source"],
        "selection_uses_predictions": False, "test_threshold_tuning": False,
        "test_was_already_opened_by_completed_frozen_evaluation": True,
        "validation": {}, "test": {},
    }
    try:
        validation_coordinates = [tuple(map(int, row)) for row in config["validation_subset_coordinates"]]
        validation_cases = choose_validation_cases(validation_reader, validation_coordinates)
        manifest["validation"] = {
            "selection": (
                "Reference-label-only selection from the fixed validation subset: "
                "median-positive patch in each survey-x slab plus a lower-quartile "
                "positive patch; within each patch, the x section with the most "
                "reference fault pixels."
            ),
            "full_split_metrics": result["validation"]["metrics"],
            "cases": render_split(
                split="validation", reader=validation_reader, origins=validation_cases,
                model=model, threshold=float(result["threshold"]),
                full_metrics=result["validation"]["metrics"], output=output,
                selection_text="Cases chosen from labels only; predictions did not select views.",
            ),
        }
        manifest["test"] = {
            "selection": (
                "Reuses the three R100 qualitative test origins selected before "
                "FaultEdgeFormer inference: median-positive fault tile in survey-x "
                "slabs 0, 256, and 512 among tiles with >1.5 million valid voxels."
            ),
            "full_split_metrics": result["test"]["metrics"],
            "cases": render_split(
                split="test", reader=test_reader, origins=list(TEST_CASES), model=model,
                threshold=float(result["threshold"]),
                full_metrics=result["test"]["metrics"], output=output,
                selection_text=(
                    "Same label-selected locations as the prior R100 review; "
                    "threshold remained frozen from validation."
                ),
            ),
        }
    finally:
        validation_reader.close()
        test_reader.close()
    render_summary(result, output / "histograms_2048_bins.npz", output)
    r100.write_json_atomic(output / "visual_manifest.json", manifest)
    print(json.dumps({
        "validation_casebook": str(output / "validation_casebook.png"),
        "test_casebook": str(output / "test_casebook.png"),
        "summary": str(output / "frozen_metrics_summary.png"),
        "manifest": str(output / "visual_manifest.json"),
    }, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
