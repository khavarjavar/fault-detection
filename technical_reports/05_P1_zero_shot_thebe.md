# Experiment 5: P1 zero-shot transfer to Thebe

## Quick answer

The synthetic P1 model was applied to real Thebe data without retraining.

| Item | Answer |
|---|---|
| Training performed here | No |
| Weight updates | 0 |
| Source model | Synthetic P1, epoch 93 |
| Frozen threshold | 0.98095703125 |
| Full Thebe test Dice | **0.079128** |

P1 also transfers poorly from synthetic to real data.

## 1. Data

The full run covers the same seven-block Thebe test volume used in Experiment 4.

| Coverage item | Count |
|---|---:|
| Raw voxels | 3,429,541,914 |
| Grid patches | 1,950 |
| Patches with scored data | 1,382 |
| Scored voxels | 2,303,341,553 |
| Excluded voxels | 1,126,200,361 |
| Scored fault voxels | 57,680,496 |

Run: [p1_zero_shot_thebe_full_20261009_162704](../runs/p1_zero_shot_thebe_full_20261009_162704).

## 2. Pipeline

The intended pipeline is:

Thebe HDF5 blocks → non-overlapping 128³ patches → valid-data mask → valid-only z-score → axis transpose → frozen P1 model → sigmoid → frozen threshold → binary fault mask.

No test label was used to choose the threshold.

## 3. Important evidence conflict

The saved run configuration says the valid-data rule was a per-trace first-to-last nonzero envelope. The saved final metric notes describe the domain as finite nonzero raw voxels. The final scored-voxel count exactly matches the earlier nonzero-mask evaluator.

These records conflict. The exact historical mask cannot be proven from the retained artifacts, so this report does not guess which description is correct. This also weakens a strict numerical comparison with Experiment 4.

Current evaluator code: [evaluate_thebe_p1_zero_shot.py](../scripts/evaluate_thebe_p1_zero_shot.py).

## 4. Method

- Model: P1 Attention3D with CAFT, trained only on synthetic data.
- Checkpoint: epoch 93.
- Threshold: 0.98095703125, selected on synthetic validation.
- Real-data weight updates: zero.
- Patch overlap: none.
- Padding: excluded from metrics.

## 5. Results

| Metric | Full Thebe test |
|---|---:|
| Dice | **0.079128** |
| IoU | 0.041194 |
| Precision | 0.050344 |
| Recall | 0.184774 |
| Specificity | 0.910474 |
| Accuracy | 0.892301 |
| Balanced accuracy | 0.547624 |
| MCC | 0.051515 |
| PR-AUC, approximate | 0.030899 |
| ROC-AUC, approximate | 0.556206 |
| TP | 10,657,851 |
| FP | 201,044,552 |
| FN | 47,022,645 |
| TN | 2,044,616,505 |

Efficiency:

- total model forward time: 32.93 seconds;
- mean forward time: 0.01689 seconds per patch;
- wall time: 663.62 seconds;
- peak CUDA allocation: 1.060 GiB.

Source: [final_metrics.json](../runs/p1_zero_shot_thebe_full_20261009_162704/final_metrics.json).

## 6. Interpretation

P1 synthetic test Dice was 0.826646, but its real Thebe zero-shot Dice is 0.079128. Attention and connectivity-aware training did not solve the synthetic-to-real domain gap.

The Baseline A zero-shot Dice was 0.085861. Because the retained P1 mask descriptions conflict, the small difference between the two transfer scores should not be treated as a clean model comparison.

## 7. Smoke evidence

Earlier smoke evaluations exist under reports/evaluation/. One nine-patch smoke scored seven usable patches and produced Dice 0.109813. Smoke values cover only a tiny, selected part of the survey and are not substitutes for the full result.

## 8. Evidence

- Configuration: [run_configuration.json](../runs/p1_zero_shot_thebe_full_20261009_162704/run_configuration.json)
- Metrics: [final_metrics.json](../runs/p1_zero_shot_thebe_full_20261009_162704/final_metrics.json)
- Per-patch values: [test_per_patch.csv](../runs/p1_zero_shot_thebe_full_20261009_162704/test_per_patch.csv)
- Source model report: [Experiment 3](03_P1_attention3d_caft_synthetic.md)

## 9. Simple definitions and calculation

| Term | Meaning |
|---|---|
| Trace envelope | From the first to last nonzero sample of each trace, including internal zeros. |
| Nonzero mask | Scores only raw samples whose value is not zero. |
| Evidence conflict | Two saved artifacts describe the same historical operation differently. |
| Smoke test | Small run used to check that a pipeline executes. |
| Full evaluation | Covers the complete planned grid. |

Test Dice:

2×10,657,851 / (2×10,657,851 + 201,044,552 + 47,022,645) = **0.079128**
