#!/usr/bin/env python3
"""Build static visuals for the project experiment-status dashboard."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports" / "experiment_status_20261030" / "assets"
OUT.mkdir(parents=True, exist_ok=True)


def read_json(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text())


def read_history(relative: str) -> dict[str, np.ndarray]:
    with (ROOT / relative).open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    keys = rows[0].keys()
    result: dict[str, np.ndarray] = {}
    for key in keys:
        values = []
        for row in rows:
            try:
                values.append(float(row[key]))
            except (TypeError, ValueError):
                values.append(np.nan)
        result[key] = np.asarray(values, dtype=np.float64)
    return result


def save(fig: plt.Figure, name: str) -> None:
    fig.savefig(OUT / name, dpi=170, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def leaderboard() -> None:
    r100 = read_json(
        "reports/evaluation/r100_clean_frozen_test_20261019/final_metrics.json"
    )["test"]["metrics"]
    fef = read_json(
        "reports/evaluation/faultedgeformer_thebe_full_seed42_20261026/result.json"
    )["test"]["metrics"]
    sam = read_json(
        "reports/evaluation/sammed3d_frozen_thebe_20261016T011856768228130Z/"
        "final_metrics.json"
    )["test"]["modes"]
    attn = read_json(
        "runs/attention3d_opunake_kahu_linear_probe_thebe_seed42_20261028/"
        "result.json"
    )["test"]["metrics"]

    labels = ["R100\nensemble", "FaultEdgeFormer\nseed 42", "R100\nseed 43"]
    comparable = [r100["ensemble"], fef, r100["seed43"]]
    diagnostic_labels = ["Frozen SAM\nno prompt", "Frozen SAM\n1 oracle click", "Attention3D\nlinear probe"]
    diagnostic = [
        sam["no_prompts"]["at_validation_threshold"],
        sam["one_oracle_click"]["at_validation_threshold"],
        attn,
    ]

    fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.8), gridspec_kw={"width_ratios": [1, 1]})
    for ax, names, rows, title, color in (
        (axes[0], labels, comparable, "Comparable full-grid Thebe test", "#2563eb"),
        (
            axes[1],
            diagnostic_labels,
            diagnostic,
            "Diagnostics — different protocols/scopes",
            "#d97706",
        ),
    ):
        x = np.arange(len(names))
        width = 0.36
        dice = [row["dice"] for row in rows]
        pr = [row["pr_auc_approx"] for row in rows]
        bars1 = ax.bar(x - width / 2, dice, width, label="Dice", color=color)
        bars2 = ax.bar(x + width / 2, pr, width, label="PR-AUC", color="#0f766e")
        ax.set_xticks(x, names)
        ax.set_ylim(0, max(0.68, max(dice + pr) * 1.18))
        ax.set_title(title, fontweight="bold")
        ax.grid(axis="y", alpha=0.22)
        ax.legend(frameon=False)
        ax.bar_label(bars1, fmt="%.3f", fontsize=8, padding=2)
        ax.bar_label(bars2, fmt="%.3f", fontsize=8, padding=2)
    axes[1].text(
        0.5,
        -0.27,
        "SAM uses frozen medical weights; Attention3D is sampled, not full-grid.",
        ha="center",
        transform=axes[1].transAxes,
        fontsize=9,
        color="#7c2d12",
    )
    fig.suptitle("What has actually been measured", fontsize=15, fontweight="bold")
    fig.tight_layout()
    save(fig, "test_leaderboard.png")


def sam_progress() -> None:
    history = read_history("runs/sammed3d_thebe_full_seed42_20261030/history.csv")
    epoch = history["epoch"]
    best = int(np.nanargmax(history["val_pr_auc_approx"]))
    fig, axes = plt.subplots(2, 1, figsize=(10.5, 7), sharex=True)
    axes[0].plot(epoch, history["train_loss"], color="#334155", lw=1.8, label="train loss")
    axes[0].set_ylabel("Masked BCE")
    axes[0].grid(alpha=0.22)
    axes[0].legend(frameon=False)
    axes[1].plot(epoch, history["val_pr_auc_approx"], color="#0f766e", lw=2, label="val PR-AUC")
    axes[1].plot(epoch, history["val_dice"], color="#dc2626", lw=1.4, alpha=0.8, label="Dice @ 0.5")
    axes[1].scatter(
        epoch[best],
        history["val_pr_auc_approx"][best],
        color="#f59e0b",
        s=70,
        zorder=4,
        label=f"best PR-AUC {history['val_pr_auc_approx'][best]:.3f} @ ep {int(epoch[best])}",
    )
    axes[1].set_xlabel("Epoch completed")
    axes[1].set_ylabel("Validation metric")
    axes[1].set_ylim(0, max(0.3, np.nanmax(history["val_pr_auc_approx"]) * 1.2))
    axes[1].grid(alpha=0.22)
    axes[1].legend(frameon=False, ncol=3, fontsize=9)
    fig.suptitle(
        f"SAM-Med3D seismic adapter — live snapshot through epoch {int(epoch[-1])}",
        fontsize=15,
        fontweight="bold",
    )
    fig.tight_layout()
    save(fig, "sam_training_progress.png")


def attention3d_status() -> None:
    runs = [
        (
            "Imported FP16\nNaNs from ep 74",
            "runs/paper_attention3d_thebe_supervised_seed42/history.csv",
            "#dc2626",
        ),
        (
            "Imported BF16 clean\nstopped after ep 65",
            "runs/paper_attention3d_thebe_supervised_seed42_bf16_clean/history.csv",
            "#7c3aed",
        ),
        (
            "Opunake+Kahu e2e\ncollapsed, stopped ep 12",
            "runs/attention3d_opunake_kahu_e2e_thebe_seed42_20261028/history.csv",
            "#d97706",
        ),
    ]
    fig, ax = plt.subplots(figsize=(10.5, 5.6))
    for label, path, color in runs:
        history = read_history(path)
        ax.plot(history["epoch"], history["val_dice"], lw=2, label=label, color=color)
        finite = np.where(np.isfinite(history["val_dice"]))[0]
        if len(finite):
            best = finite[np.argmax(history["val_dice"][finite])]
            ax.scatter(history["epoch"][best], history["val_dice"][best], color=color, s=55)
            ax.annotate(
                f"{history['val_dice'][best]:.3f}",
                (history["epoch"][best], history["val_dice"][best]),
                xytext=(4, 5),
                textcoords="offset points",
                fontsize=8,
            )
    ax.set_xlabel("Epoch completed")
    ax.set_ylabel("Validation Dice @ fixed 0.5")
    ax.set_title("Attention3D supervised attempts — none is a completed reliable run", fontweight="bold")
    ax.grid(alpha=0.22)
    ax.legend(frameon=False, fontsize=9)
    fig.tight_layout()
    save(fig, "attention3d_training_status.png")


def r100_patch_distribution() -> None:
    path = ROOT / "reports/evaluation/r100_clean_frozen_test_20261019/test_per_patch.csv"
    fault_dice: list[float] = []
    false_positives: list[int] = []
    with path.open(newline="") as handle:
        for row in csv.DictReader(handle):
            if row["model"] != "ensemble":
                continue
            if int(row["positive_voxels"]) > 0:
                fault_dice.append(float(row["dice"]))
            else:
                false_positives.append(int(row["fp"]))
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.7))
    axes[0].hist(fault_dice, bins=np.linspace(0, 1, 31), color="#2563eb", alpha=0.88)
    axes[0].axvline(np.median(fault_dice), color="#dc2626", lw=2, label=f"median {np.median(fault_dice):.3f}")
    axes[0].set_title("Fault-present test patches")
    axes[0].set_xlabel("Patch Dice")
    axes[0].set_ylabel("Patches")
    axes[0].legend(frameon=False)
    axes[0].grid(alpha=0.2)
    fp = np.asarray(false_positives)
    axes[1].hist(np.log10(fp[fp > 0] + 1), bins=28, color="#d97706", alpha=0.88)
    axes[1].text(
        0.97,
        0.95,
        f"{np.count_nonzero(fp == 0)} / {len(fp)} have zero FP",
        ha="right",
        va="top",
        transform=axes[1].transAxes,
    )
    axes[1].set_title("Fault-absent observed patches")
    axes[1].set_xlabel("log10(false-positive voxels + 1)")
    axes[1].set_ylabel("Patches")
    axes[1].grid(alpha=0.2)
    fig.suptitle("R100 three-seed ensemble: the pooled Dice hides heterogeneous patches", fontsize=14, fontweight="bold")
    fig.tight_layout()
    save(fig, "r100_patch_distribution.png")


def historical_prediction_example() -> None:
    path = ROOT / (
        "runs/baseline_A_zero_shot_thebe_full_20261005_095032/"
        "prediction_examples/example_06_x0000_y0128_z0768.npz"
    )
    with np.load(path, allow_pickle=False) as data:
        seismic = data["seismic_axis0"]
        target = data["target_axis0"]
        probability = data["probability_axis0"]
        prediction = data["prediction_axis0"]
        threshold = float(data["threshold"])
    valid_values = seismic[np.isfinite(seismic)]
    lo, hi = np.percentile(valid_values, [2, 98])
    fig, axes = plt.subplots(1, 4, figsize=(13, 3.5))
    panels = [
        (seismic, "Seismic", "gray", lo, hi),
        (target, "Ground truth", "Reds", 0, 1),
        (probability, "Probability", "magma", 0, 1),
        (prediction, f"Prediction @ {threshold:.3f}", "Reds", 0, 1),
    ]
    for ax, (image, title, cmap, vmin, vmax) in zip(axes, panels):
        ax.imshow(image.T, origin="lower", cmap=cmap, vmin=vmin, vmax=vmax, interpolation="nearest")
        ax.set_title(title)
        ax.set_xticks([])
        ax.set_yticks([])
    fig.suptitle(
        "Historical synthetic-to-Thebe zero-shot example — visual evidence, not the current best model",
        fontsize=13,
        fontweight="bold",
    )
    fig.tight_layout()
    save(fig, "historical_zero_shot_example.png")


def dataset_overview() -> None:
    base = ROOT / "data/processed/viewer_previews"
    specs = [
        ("kahu_seismic_vis_s3x4x3.npy", "Kahu seismic preview", 100, "gray"),
        ("opunake_seismic_vis_s3x5x3.npy", "Opunake seismic preview", 127, "gray"),
        ("thebe_train1_seismic_vis_s1x6x3.npy", "Thebe train1 seismic", 95, "gray"),
        ("thebe_train1_fault_mask_vis_s1x6x3.npy", "Thebe train1 mask", 95, "Reds"),
    ]
    fig, axes = plt.subplots(1, 4, figsize=(14, 4))
    for ax, (name, title, index, cmap) in zip(axes, specs):
        array = np.load(base / name, mmap_mode="r", allow_pickle=False)
        image = np.asarray(array[index])
        if cmap == "gray":
            present = image[np.isfinite(image) & (image != 0)]
            lo, hi = np.percentile(present if present.size else image, [2, 98])
        else:
            lo, hi = 0, 1
        ax.imshow(image.T, origin="lower", cmap=cmap, vmin=lo, vmax=hi, interpolation="nearest")
        ax.set_title(title)
        ax.set_xticks([])
        ax.set_yticks([])
    fig.suptitle("Datasets now available in the 3D viewer (downsampled visual previews)", fontsize=14, fontweight="bold")
    fig.tight_layout()
    save(fig, "dataset_overview.png")


def main() -> None:
    leaderboard()
    sam_progress()
    attention3d_status()
    r100_patch_distribution()
    historical_prediction_example()
    dataset_overview()
    print(f"wrote visuals to {OUT}")


if __name__ == "__main__":
    main()
