#!/usr/bin/env python3
"""Draw the saved ensemble-size measurement; no training or dataset access."""
import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("result_dir", type=Path)
    args = parser.parse_args()
    result = json.loads((args.result_dir / "curve.json").read_text())
    rows = result["curve"]
    fig, ax = plt.subplots(figsize=(7.5, 4.8), layout="constrained")
    for row in rows:
        dots = [item["validation"]["dice"] for item in result["subset_results"] if item["size"] == row["size"]]
        jitter = np.linspace(-.07, .07, len(dots)) if len(dots) > 1 else np.zeros(1)
        ax.scatter(row["size"]+jitter, dots, s=28, color="#94a3b8", zorder=2)
    ax.plot([r["size"] for r in rows], [r["mean_dice"] for r in rows], color="#2563eb", zorder=3,
            label="Mean Dice across measured subsets")
    estimated = [row for row in rows if row["subset_sample_sd"] is not None]
    if estimated:
        ax.errorbar([r["size"] for r in estimated], [r["mean_dice"] for r in estimated],
                    yerr=[r["subset_sample_sd"] for r in estimated], fmt="o", capsize=5,
                    color="#2563eb", zorder=4, label="Subset sample SD (not a confidence interval)")
    single = [row for row in rows if row["subset_sample_sd"] is None]
    if single:
        ax.scatter([r["size"] for r in single], [r["mean_dice"] for r in single], marker="D", s=50,
                   color="#d97706", zorder=5, label="One subset: SD cannot be estimated")
    for row in rows:
        ax.annotate(f"{row['mean_dice']:.4f}", (row["size"], row["mean_dice"]),
                    xytext=(8, 9), textcoords="offset points", fontsize=10)
    ax.set_xticks([r["size"] for r in rows])
    ax.set_xlabel("Number of models averaged")
    ax.set_ylabel("Validation Dice")
    ax.set_title("R100 ensemble size — available seeds " + ", ".join(map(str, result["seeds"])))
    ax.grid(axis="y", alpha=.25)
    ax.spines[["top", "right"]].set_visible(False)
    ax.margins(x=.15, y=.22)
    ax.legend(loc="lower right", fontsize=8, framealpha=.95)
    fig.supxlabel("Each subset chooses its threshold on the same validation volume. No test results.", fontsize=8)
    fig.savefig(args.result_dir / "curve.png", dpi=180)
    fig.savefig(args.result_dir / "curve.svg")
    plt.close(fig)
    print(args.result_dir / "curve.png")


if __name__ == "__main__":
    main()
