#!/usr/bin/env python3
"""Combine the completed FaultEdgeFormer and Attention3D stage reports."""

from __future__ import annotations

import json
import os
from pathlib import Path


FAULTEDGE = Path("reports/evaluation/faultedgeformer_thebe_full_seed42_20261026/result.json")
ATTENTION = Path("reports/evaluation/attention3d_two_survey_pretext_seed42_20261026/result.json")
OUTPUT = Path("reports/experiments/ACTIVE_RUNS_QUICK_RESULTS_20261026.md")


def main() -> int:
    faultedge = json.loads(FAULTEDGE.read_text())
    attention = json.loads(ATTENTION.read_text())
    fm = faultedge["test"]["metrics"]
    fv = faultedge["validation"]["metrics"]
    av = attention["validation"]
    report = f"""# Active experiment results

## FaultEdgeFormer-inspired segmentation

The model was trained on Thebe `train1–train9`, selected and thresholded using `val1–val2`, and evaluated once on all seven frozen Thebe test files.

| Metric | Validation | Frozen test |
|---|---:|---:|
| Dice | {fv['dice']:.6f} | {fm['dice']:.6f} |
| IoU | {fv['iou']:.6f} | {fm['iou']:.6f} |
| Precision | {fv['precision']:.6f} | {fm['precision']:.6f} |
| Recall | {fv['recall']:.6f} | {fm['recall']:.6f} |
| F2 | {fv['f2']:.6f} | {fm['f2']:.6f} |
| MCC | {fv['mcc']:.6f} | {fm['mcc']:.6f} |
| PR-AUC (approx.) | {fv['pr_auc_approx']:.6f} | {fm['pr_auc_approx']:.6f} |

This is a single-seed exploratory result from a FaultEdgeFormer-inspired local implementation, not an exact author-code reproduction.

## Attention3D two-survey denoising pretraining

| Measure | Result |
|---|---:|
| Best epoch | {attention['best_epoch']} |
| Fixed-validation network MSE | {av['network_mse']:.8f} |
| Noisy-input identity MSE | {av['noisy_identity_mse']:.8f} |
| Identity − network MSE | {av['identity_minus_network_mse']:.8f} |
| Beats identity baseline | {attention['beats_noisy_identity_baseline']} |

This stage used 8,800 unique Opunake and 8,800 unique Kahu cubes. Kerry was unavailable. It is a denoising result, so a Thebe fault Dice is not yet defined. The next stage is backbone transfer and supervised Thebe fine-tuning, followed by a separately frozen Thebe test.
"""
    temporary = OUTPUT.with_name(OUTPUT.name + ".part")
    temporary.write_text(report)
    os.replace(temporary, OUTPUT)
    print(OUTPUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
