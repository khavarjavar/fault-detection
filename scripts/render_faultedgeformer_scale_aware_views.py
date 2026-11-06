#!/usr/bin/env python3
"""Render scale-aware 2D sections and a 3D cube for a frozen Thebe case.

The default case is the first label-selected validation example in the completed
FaultEdgeFormer-inspired evaluation. One spatial probability cube is cached so
later render-only changes do not require another GPU inference.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Rectangle
import numpy as np
from scipy.ndimage import binary_erosion
import torch

import evaluate_faultedgeformer_frozen_test as frozen_eval
import train_r100_fp16_clean as r100
from evaluate_thebe_zero_shot_r100_pinned import ConcatenatedThebe


ROOT = Path(__file__).resolve().parents[1]
RUN_DIR = ROOT / "runs/faultedgeformer_thebe_full_seed42_20261026"
EVAL_DIR = ROOT / "reports/evaluation/faultedgeformer_thebe_full_seed42_20261026"
OUTPUT = EVAL_DIR / "scale_aware_views"
DATA_ROOT = ROOT / "data/processed/thebe_h5"
ORIGIN = (0, 1920, 896)
THRESHOLD = 0.24560546875
PINK = "#fa1775"
GOLD = "#ffbd20"
CYAN = "#00d8ff"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_seismic(raw: np.ndarray) -> np.ndarray:
    valid = raw != 0
    result = np.zeros_like(raw, dtype=np.float32)
    values = raw[valid]
    result[valid] = (values - values.mean(dtype=np.float64)) / values.std(dtype=np.float64)
    return result


def infer_or_load(reader: ConcatenatedThebe) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    cache = OUTPUT / "validation_x0000_y1920_z0896_spatial_cube.npz"
    if cache.is_file():
        saved = np.load(cache)
        return saved["probability"], saved["truth"].astype(bool), saved["valid"].astype(bool)

    config = read_json(RUN_DIR / "run_config.json")
    selection = read_json(RUN_DIR / "validation_selection.json")
    model = frozen_eval.load_model(config, selection, RUN_DIR)
    x, target, mask, shape, observed, _, _ = r100.read_patch(reader, ORIGIN)
    if shape != (128, 128, 128) or not observed:
        raise RuntimeError(f"Unexpected case shape or coverage: {shape}, {observed}")
    with torch.inference_mode(), torch.autocast("cuda", dtype=torch.float16):
        logits = model(x.cuda())
    probability = torch.sigmoid(logits.float()).cpu().numpy()[0, 0].transpose()
    truth = target.numpy()[0, 0].transpose().astype(bool)
    valid = mask.numpy()[0, 0].transpose().astype(bool)
    truth &= valid
    np.savez_compressed(
        cache,
        probability=probability.astype(np.float16),
        truth=truth.astype(np.uint8),
        valid=valid.astype(np.uint8),
        origin_xyz=np.asarray(ORIGIN),
        threshold=np.asarray(THRESHOLD),
    )
    del logits, model, x
    torch.cuda.empty_cache()
    return probability, truth, valid


def render_full_section(
    seismic: np.ndarray,
    full_truth: np.ndarray,
    prediction: np.ndarray,
) -> Path:
    prediction_full = np.zeros_like(full_truth, dtype=bool)
    prediction_full[896:1024, 1920:2048] = prediction[127].T
    inferred = np.zeros_like(full_truth, dtype=bool)
    inferred[896:1024, 1920:2048] = True

    fig, axes = plt.subplots(1, 2, figsize=(17, 6.2), constrained_layout=True)
    for axis in axes:
        axis.imshow(
            np.clip(seismic, -2.5, 2.5), cmap="gray", vmin=-2.5, vmax=2.5,
            origin="upper", aspect="auto", interpolation="nearest",
        )
        axis.add_patch(Rectangle((1920, 896), 128, 128, fill=False, edgecolor=CYAN, linewidth=3))
        axis.set(xlabel="survey y", ylabel="survey z")
    axes[0].imshow(
        np.ma.masked_where(~full_truth, full_truth),
        cmap=ListedColormap([PINK]), alpha=0.82, origin="upper", aspect="auto",
        interpolation="nearest",
    )
    axes[0].set_title("Official Thebe reference — complete 3174 × 1537 section")
    axes[1].imshow(
        np.ma.masked_where(~prediction_full, prediction_full),
        cmap=ListedColormap([GOLD]), alpha=0.86, origin="upper", aspect="auto",
        interpolation="nearest",
    )
    axes[1].imshow(
        np.ma.masked_where(inferred, np.ones_like(inferred)), cmap="gray", alpha=0.18,
        origin="upper", aspect="auto", interpolation="nearest",
    )
    axes[1].set_title("Model prediction inside cyan evaluated cube; outside not inferred")
    fig.suptitle(
        "FaultEdgeFormer-inspired · Thebe validation survey x=127 · full-section scale",
        fontsize=15,
    )
    path = OUTPUT / "validation_2d_full_section.png"
    fig.savefig(path, dpi=180)
    plt.close(fig)
    return path


def render_context(
    seismic: np.ndarray,
    full_truth: np.ndarray,
    probability: np.ndarray,
    prediction: np.ndarray,
) -> Path:
    y0, y1, z0, z1 = 1728, 2240, 704, 1216
    section_probability = np.full_like(seismic, np.nan, dtype=np.float32)
    section_probability[896:1024, 1920:2048] = probability[127].T
    section_prediction = np.zeros_like(full_truth, dtype=bool)
    section_prediction[896:1024, 1920:2048] = prediction[127].T
    crop = np.s_[z0:z1, y0:y1]
    extent = (y0, y1, z1, z0)

    fig, axes = plt.subplots(1, 3, figsize=(17, 6), constrained_layout=True)
    for axis in axes:
        axis.imshow(
            np.clip(seismic[crop], -2.5, 2.5), cmap="gray", vmin=-2.5, vmax=2.5,
            origin="upper", aspect="equal", extent=extent, interpolation="nearest",
        )
        axis.add_patch(Rectangle((1920, 896), 128, 128, fill=False, edgecolor=CYAN, linewidth=2))
        axis.set(xlabel="survey y", ylabel="survey z")
    axes[0].contour(
        full_truth[crop].astype(float), levels=[0.5], colors=[PINK], linewidths=1.4,
        origin="upper", extent=extent,
    )
    axes[0].set_title("Reference boundary (pink)")
    axes[1].imshow(
        np.ma.masked_invalid(section_probability[crop]), cmap="magma", vmin=0, vmax=1,
        alpha=0.72, origin="upper", aspect="equal", extent=extent,
        interpolation="bilinear",
    )
    axes[1].contour(
        full_truth[crop].astype(float), levels=[0.5], colors=[PINK], linewidths=1.0,
        origin="upper", extent=extent,
    )
    axes[1].set_title("Probability in evaluated cube; reference outline")
    axes[2].contour(
        full_truth[crop].astype(float), levels=[0.5], colors=[PINK], linewidths=1.4,
        origin="upper", extent=extent,
    )
    axes[2].contour(
        section_prediction[crop].astype(float), levels=[0.5], colors=[GOLD], linewidths=1.4,
        origin="upper", extent=extent,
    )
    axes[2].set_title("Reference pink · prediction gold")
    fig.suptitle(
        "512 × 512 geological context — boundaries show localization without filled-band exaggeration",
        fontsize=15,
    )
    path = OUTPUT / "validation_2d_context_512.png"
    fig.savefig(path, dpi=180)
    plt.close(fig)
    return path


def render_unlabelled_context(seismic: np.ndarray) -> tuple[Path, Path]:
    """Save the exact 512x512 context with no fault or model overlays."""
    y0, y1, z0, z1 = 1728, 2240, 704, 1216
    crop = np.clip(seismic[z0:z1, y0:y1], -2.5, 2.5)
    extent = (y0, y1, z1, z0)

    fig, axis = plt.subplots(figsize=(8, 8), constrained_layout=True)
    axis.imshow(
        crop, cmap="gray", vmin=-2.5, vmax=2.5, origin="upper",
        aspect="equal", extent=extent, interpolation="nearest",
    )
    axis.set(
        xlabel="survey y", ylabel="survey z",
        title="Unlabelled seismic — same 512 × 512 geological context",
    )
    axes_path = OUTPUT / "validation_2d_context_512_unlabelled_with_axes.png"
    fig.savefig(axes_path, dpi=180)
    plt.close(fig)

    fig, axis = plt.subplots(figsize=(8, 8), frameon=False)
    axis.imshow(
        crop, cmap="gray", vmin=-2.5, vmax=2.5, origin="upper",
        aspect="equal", interpolation="nearest",
    )
    axis.set_axis_off()
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    clean_path = OUTPUT / "validation_2d_context_512_unlabelled_clean.png"
    fig.savefig(clean_path, dpi=180, bbox_inches="tight", pad_inches=0)
    plt.close(fig)
    return axes_path, clean_path


def boundary_points(mask: np.ndarray, maximum: int, seed: int) -> np.ndarray:
    boundary = mask & ~binary_erosion(mask, structure=np.ones((3, 3, 3)), border_value=0)
    points = np.argwhere(boundary)
    if len(points) > maximum:
        rng = np.random.default_rng(seed)
        points = points[rng.choice(len(points), maximum, replace=False)]
    return points


def draw_cube_edges(axis) -> None:
    for x in (0, 127):
        for y in (0, 127):
            axis.plot([x, x], [y, y], [0, 127], color="0.35", lw=0.6, alpha=0.6)
    for x in (0, 127):
        for z in (0, 127):
            axis.plot([x, x], [0, 127], [z, z], color="0.35", lw=0.6, alpha=0.6)
    for y in (0, 127):
        for z in (0, 127):
            axis.plot([0, 127], [y, y], [z, z], color="0.35", lw=0.6, alpha=0.6)


def scatter_mask(axis, mask: np.ndarray, color: str, seed: int, alpha: float = 0.38) -> None:
    points = boundary_points(mask, maximum=18_000, seed=seed)
    # Stored order is x,y,z. Plot horizontal y, receding x, and vertical z.
    axis.scatter(
        points[:, 1], points[:, 0], points[:, 2], s=0.75, c=color,
        alpha=alpha, linewidths=0, depthshade=False,
    )


def style_cube(axis, title: str) -> None:
    draw_cube_edges(axis)
    axis.set(xlim=(0, 127), ylim=(0, 127), zlim=(127, 0))
    axis.set_box_aspect((1, 1, 1))
    axis.set(xlabel="local y", ylabel="local x", zlabel="local z", title=title)
    axis.view_init(elev=23, azim=-56)
    axis.grid(False)


def render_cube(truth: np.ndarray, prediction: np.ndarray) -> Path:
    tp = prediction & truth
    fp = prediction & ~truth
    fn = ~prediction & truth
    tp_count, fp_count, fn_count = int(tp.sum()), int(fp.sum()), int(fn.sum())
    dice = 2 * tp_count / (2 * tp_count + fp_count + fn_count)

    fig = plt.figure(figsize=(18, 6.4), constrained_layout=True)
    reference_axis = fig.add_subplot(131, projection="3d")
    prediction_axis = fig.add_subplot(132, projection="3d")
    error_axis = fig.add_subplot(133, projection="3d")
    scatter_mask(reference_axis, truth, PINK, 1, alpha=0.34)
    scatter_mask(prediction_axis, prediction, GOLD, 2, alpha=0.34)
    scatter_mask(error_axis, tp, "#24d85a", 3, alpha=0.30)
    scatter_mask(error_axis, fp, "#ff8b16", 4, alpha=0.32)
    scatter_mask(error_axis, fn, PINK, 5, alpha=0.32)
    style_cube(reference_axis, "Official reference surface (pink)")
    style_cube(prediction_axis, "Predicted surface at threshold 0.2456 (gold)")
    style_cube(error_axis, "TP green · FP orange · FN pink")
    fig.suptitle(
        f"FaultEdgeFormer-inspired · 128³ validation cube at {ORIGIN} · cube Dice {dice:.3f}\n"
        "Boundary voxels are sampled for readable rendering; metrics use every valid voxel.",
        fontsize=15,
    )
    path = OUTPUT / "validation_3d_cube.png"
    fig.savefig(path, dpi=190)
    plt.close(fig)
    return path


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    paths = r100.split_paths(DATA_ROOT, "val", 2)
    reader = ConcatenatedThebe(paths)
    try:
        probability, truth, valid = infer_or_load(reader)
        prediction = (probability >= THRESHOLD) & valid
        raw = reader.read("seismic", 127, 128, 0, 3174, 0, 1537)[0]
        full_truth = reader.read("fault", 127, 128, 0, 3174, 0, 1537)[0].astype(bool)
    finally:
        reader.close()
    seismic = normalize_seismic(raw).T
    full_truth = full_truth.T
    unlabelled_axes, unlabelled_clean = render_unlabelled_context(seismic)
    outputs = {
        "full_section_2d": str(render_full_section(seismic, full_truth, prediction)),
        "context_2d": str(render_context(seismic, full_truth, probability, prediction)),
        "context_2d_unlabelled_with_axes": str(unlabelled_axes),
        "context_2d_unlabelled_clean": str(unlabelled_clean),
        "cube_3d": str(render_cube(truth, prediction)),
        "spatial_cube_cache": str(OUTPUT / "validation_x0000_y1920_z0896_spatial_cube.npz"),
        "origin_xyz": list(ORIGIN),
        "displayed_survey_x": 127,
        "threshold": THRESHOLD,
        "scope": "Prediction exists only for the marked 128^3 validation cube.",
    }
    (OUTPUT / "manifest.json").write_text(json.dumps(outputs, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(outputs, indent=2))


if __name__ == "__main__":
    main()
