#!/usr/bin/env python3
"""Render selected frozen R100 test predictions with ground-truth overlays.

The three tiles are fixed from the existing test-per-patch CSV: within x slabs
0, 256, and 512, each is the median-positive fault tile among tiles with more
than 1.5 million valid voxels. The
displayed x section maximizes visible reference fault pixels within that tile.
This selection is for qualitative inspection only; all reported scores remain
the original full-test scores with validation-frozen thresholds.
"""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np
import torch

import evaluate_r100_frozen_test as evaluator


ROOT = Path(__file__).resolve().parents[1]
CASES = ((0, 512, 896), (256, 1792, 1024), (512, 1536, 768))
COLORS = ListedColormap([(0, 0, 0, 0), (0.22, 0.9, 0.35, 0.8),
                         (1.0, 0.56, 0.10, 0.8), (0.95, 0.15, 0.75, 0.8)])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path,
                        default=ROOT / "reports/evaluation/r100_test_visuals_20261102")
    args = parser.parse_args()
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)

    frozen, _, thresholds, configs, selections, paths, _ = evaluator.preflight()
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required for the frozen inference recipe")
    models = evaluator.load_models(configs, selections)
    source = ROOT / "reports/evaluation/r100_clean_frozen_test_20261019/test_per_patch.csv"
    with source.open(newline="") as stream:
        rows = {r["patch_id"]: r for r in csv.DictReader(stream) if r["model"] == "ensemble"}

    reader = evaluator.r100.ConcatenatedThebe(paths["test"])
    fig, axes = plt.subplots(len(CASES), 4, figsize=(18, 12), constrained_layout=True)
    single_fig, single_axes = plt.subplots(len(CASES), 3, figsize=(14, 12), constrained_layout=True)
    manifest = {"created_utc": datetime.now(timezone.utc).isoformat(),
                "source_evaluation": str(source.relative_to(ROOT)),
                "checkpoint_hashes": frozen["checkpoint_hashes"],
                "threshold": thresholds["ensemble"],
                "selection": "Fixed x slabs 0,256,512; median-positive fault tile among tiles with >1.5 million valid voxels in each slab. Within tile, display x section with maximum reference fault pixels.",
                "purpose": "Qualitative test visualization; no model or threshold selection",
                "cases": []}
    try:
        for i, origin in enumerate(CASES):
            patch_id = "x%04d_y%04d_z%04d" % origin
            reference = rows[patch_id]
            x, target, mask, shape, observed, _, _ = evaluator.r100.read_patch(reader, origin)
            if observed != int(reference["valid_voxels"]) or int(target[mask].sum()) != int(reference["positive_voxels"]):
                raise RuntimeError(f"Saved test row disagrees with current data: {patch_id}")
            probabilities = []
            with torch.inference_mode():
                x_gpu = x.cuda()
                for model in models.values():
                    with torch.autocast("cuda", dtype=torch.float16):
                        logits = model(x_gpu)
                    probabilities.append(torch.sigmoid(logits.float()).cpu().numpy()[0, 0])
            # read_patch reverses the axes for the model; undo for visualization.
            prob = np.mean(np.stack(probabilities), axis=0).transpose()
            seed43_prob = probabilities[1].transpose()
            seismic = x.numpy()[0, 0].transpose()
            truth = target.numpy()[0, 0].transpose().astype(bool)
            valid = mask.numpy()[0, 0].transpose().astype(bool)
            predicted = (prob >= thresholds["ensemble"]) & valid
            local_x = int(np.argmax((truth & valid).sum(axis=(1, 2))))
            cut = np.s_[local_x, :shape[1], :shape[2]]
            amp = seismic[cut].T
            gt = (truth & valid)[cut].T
            pred = predicted[cut].T
            seed43_pred = ((seed43_prob >= thresholds["seed43"]) & valid)[cut].T
            confidence = prob[cut].T
            valid_cut = valid[cut].T
            error = np.zeros(gt.shape, dtype=np.uint8)
            error[pred & gt] = 1
            error[pred & ~gt] = 2
            error[~pred & gt] = 3
            panels = axes[i]
            for ax in panels:
                ax.imshow(np.clip(amp, -2.5, 2.5), cmap="gray", vmin=-2.5, vmax=2.5,
                          origin="upper", aspect="auto", interpolation="nearest")
                ax.set_xlabel("survey y within tile")
                ax.set_ylabel("survey z within tile")
            panels[0].imshow(np.ma.masked_where(~gt, gt), cmap=ListedColormap(["#fa1775"]),
                             alpha=0.78, origin="upper", aspect="auto", interpolation="nearest")
            panels[0].set_title(f"{patch_id}\nreference fault (pink)")
            panels[1].imshow(np.ma.masked_where(~valid_cut, confidence), cmap="magma", vmin=0, vmax=1,
                             alpha=0.8, origin="upper", aspect="auto", interpolation="nearest")
            panels[1].set_title("Ensemble fault probability")
            panels[2].imshow(np.ma.masked_where(~pred, pred), cmap=ListedColormap(["#ffcd28"]),
                             alpha=0.78, origin="upper", aspect="auto", interpolation="nearest")
            panels[2].set_title(f"Predicted fault, threshold {thresholds['ensemble']:.4f}")
            panels[3].imshow(np.ma.masked_where(error == 0, error), cmap=COLORS,
                             vmin=0, vmax=3, origin="upper", aspect="auto", interpolation="nearest")
            panels[3].set_title("TP green · FP orange · FN pink")
            sp = single_axes[i]
            for ax in sp:
                ax.imshow(np.clip(amp, -2.5, 2.5), cmap="gray", vmin=-2.5, vmax=2.5,
                          origin="upper", aspect="auto", interpolation="nearest")
                ax.set_xlabel("survey y within tile")
                ax.set_ylabel("survey z within tile")
            sp[0].imshow(np.ma.masked_where(~gt, gt), cmap=ListedColormap(["#fa1775"]),
                         alpha=0.78, origin="upper", aspect="auto", interpolation="nearest")
            sp[0].set_title(f"{patch_id}\nreference fault (pink)")
            sp[1].imshow(np.ma.masked_where(~seed43_pred, seed43_pred),
                         cmap=ListedColormap(["#ffcd28"]), alpha=0.78,
                         origin="upper", aspect="auto", interpolation="nearest")
            sp[1].set_title(f"Seed 43 prediction, threshold {thresholds['seed43']:.4f}")
            single_error = np.zeros(gt.shape, dtype=np.uint8)
            single_error[seed43_pred & gt] = 1
            single_error[seed43_pred & ~gt] = 2
            single_error[~seed43_pred & gt] = 3
            sp[2].imshow(np.ma.masked_where(single_error == 0, single_error), cmap=COLORS,
                         vmin=0, vmax=3, origin="upper", aspect="auto", interpolation="nearest")
            sp[2].set_title("TP green · FP orange · FN pink")
            manifest["cases"].append({"patch_id": patch_id, "origin": origin,
                                       "displayed_x": origin[0] + local_x,
                                       "patch_positive_voxels": int(reference["positive_voxels"]),
                                       "patch_dice_from_frozen_test": float(reference["dice"]),
                                       "displayed_section_positive_pixels": int(gt.sum()),
                                       "displayed_section_tp": int((pred & gt).sum()),
                                       "displayed_section_fp": int((pred & ~gt).sum()),
                                       "displayed_section_fn": int((~pred & gt).sum())})
    finally:
        reader.close()
    fig.suptitle("Thebe frozen test: R100 seeds 42–44 probability ensemble (qualitative sections)", fontsize=15)
    fig.savefig(output / "casebook.png", dpi=150)
    plt.close(fig)
    single_fig.suptitle("Thebe frozen test: R100 seed 43 (test Dice 0.567466)", fontsize=15)
    single_fig.savefig(output / "seed43_casebook.png", dpi=150)
    plt.close(single_fig)
    fig, axes = plt.subplots(1, 2, figsize=(13, 5), constrained_layout=True)
    positive_rows = [r for r in rows.values() if int(r["positive_voxels"]) > 0]
    slabs = sorted({int(r["x"]) for r in positive_rows})
    dice_groups = [[float(r["dice"]) for r in positive_rows if int(r["x"]) == slab]
                   for slab in slabs]
    axes[0].boxplot(dice_groups, tick_labels=[str(s) for s in slabs],
                    showfliers=False, patch_artist=True,
                    boxprops={"facecolor": "#54a7b5", "alpha": 0.75})
    axes[0].set_title("Frozen test patch Dice where reference fault exists")
    axes[0].set_xlabel("Test x slab origin")
    axes[0].set_ylabel("Patch Dice")
    axes[0].set_ylim(0, 1)
    axes[0].grid(axis="y", alpha=0.25)
    hist = np.load(ROOT / "reports/evaluation/r100_clean_frozen_test_20261019/test_histograms_2048_bins.npz")
    tp = np.cumsum(hist["ensemble_positive"][::-1], dtype=np.float64)
    fp = np.cumsum(hist["ensemble_negative"][::-1], dtype=np.float64)
    recall = tp / tp[-1]
    precision = np.divide(tp, tp + fp, out=np.ones_like(tp), where=(tp + fp) > 0)
    axes[1].plot(recall, precision, color="#c13977", lw=2, label="R100 ensemble")
    prevalence = tp[-1] / (tp[-1] + fp[-1])
    axes[1].axhline(prevalence, color="gray", ls="--", lw=1, label="fault prevalence")
    axes[1].set_title("Full frozen test precision–recall curve")
    axes[1].set_xlabel("Recall")
    axes[1].set_ylabel("Precision")
    axes[1].set_xlim(0, 1)
    axes[1].set_ylim(0, 1)
    axes[1].legend(loc="upper right")
    axes[1].grid(alpha=0.25)
    fig.savefig(output / "test_summary.png", dpi=150)
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(9, 5), constrained_layout=True)
    training_roots = (ROOT / "runs/R100_fp16_clean_3seeds_20261014_150435",
                      ROOT / "runs/R100_seed_saturation_pilot_20261019")
    best_epochs = {}
    for seed in range(42, 47):
        run_dir = training_roots[0] if seed <= 44 else training_roots[1]
        with (run_dir / f"seed{seed}/history.csv").open(newline="") as stream:
            history = list(csv.DictReader(stream))
        epoch = np.array([int(r["epoch"]) for r in history])
        auc = np.array([float(r["val_pr_auc_approx"]) for r in history])
        best_epochs[str(seed)] = int(epoch[np.argmax(auc)])
        ax.plot(epoch, auc, lw=1.2, alpha=0.8, label=f"seed {seed}, best {best_epochs[str(seed)]}")
    ax.set_title("R100 subset-validation PR-AUC by epoch")
    ax.set_xlabel("Training epoch")
    ax.set_ylabel("Approximate PR-AUC on fixed 128-patch validation subset")
    ax.set_xlim(1, 100)
    ax.set_ylim(0, 0.75)
    ax.grid(alpha=0.25)
    ax.legend(loc="lower right")
    fig.savefig(output / "training_curves.png", dpi=150)
    plt.close(fig)
    manifest["summary"] = {"fault_present_patches": len(positive_rows),
                           "all_observed_patches": len(rows),
                           "fault_prevalence_scored_voxels": float(prevalence),
                           "best_epoch_by_seed": best_epochs}
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({"output": str(output / "casebook.png"), "cases": manifest["cases"]}, indent=2))


if __name__ == "__main__":
    main()
