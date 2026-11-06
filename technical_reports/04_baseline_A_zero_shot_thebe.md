# Experiment 4: Baseline A zero-shot transfer to Thebe

## Quick answer

The synthetic Baseline A model was applied directly to real Thebe seismic without retraining.

| Item | Answer |
|---|---|
| Training performed here | No |
| Weight updates | 0 |
| Source model | Synthetic Baseline A, epoch 100 |
| Frozen threshold | 0.43896484375 |
| Real test Dice | **0.085861** |

The large drop from synthetic Dice 0.821059 to real-data Dice 0.085861 shows poor zero-shot transfer.

## 1. Run folders

| Folder | Purpose | Status |
|---|---|---|
| [smoke 091638](../runs/baseline_A_zero_shot_thebe_smoke_20261005_091638) | Two-patch setup check | No final metric file |
| [smoke 094726](../runs/baseline_A_zero_shot_thebe_smoke_20261005_094726) | Sixteen-patch evaluator check | Completed smoke only |
| [full 095032](../runs/baseline_A_zero_shot_thebe_full_20261005_095032) | Entire held-out Thebe test | Completed |

These three directories belong to one experiment because they use the same frozen model and transfer question.

## 2. Data size

The held-out test consists of seven HDF5 blocks concatenated to shape:

703 × 3,174 × 1,537 = **3,429,541,914 raw voxels**

| Coverage item | Count |
|---|---:|
| Non-overlapping 128³ grid patches | 1,950 |
| Patches with scored data | 1,382 |
| Valid voxels scored | 2,303,341,553 |
| Raw no-data voxels excluded | 1,126,200,361 |
| Labelled fault voxels scored | 57,680,496 |
| Positive labels outside valid mask | 34,415 |

## 3. Pipeline

The full evaluator:

1. logically concatenates test1.h5 through test7.h5;
2. divides the volume into non-overlapping 128³ patches;
3. pads boundary patches but excludes padding from metrics;
4. treats finite raw seismic values not equal to zero as valid;
5. z-scores each patch using only valid values;
6. transposes axes to match synthetic training;
7. runs the frozen Baseline A model;
8. applies the frozen synthetic threshold;
9. scores each valid voxel once.

Archived evaluator: [evaluate_thebe_zero_shot_r100_pinned.py](../scripts/evaluate_thebe_zero_shot_r100_pinned.py).

## 4. Method

This is zero-shot inference:

- no real-data training;
- no fine-tuning;
- no threshold selection on Thebe;
- no weight changes.

The model and threshold come from [Experiment 1](01_baseline_A_synthetic.md).

## 5. Results

| Metric | Full Thebe test |
|---|---:|
| Dice | **0.085861** |
| IoU | 0.044856 |
| Precision | 0.052094 |
| Recall | 0.244065 |
| Specificity | 0.885930 |
| Accuracy | 0.869856 |
| Balanced accuracy | 0.564998 |
| MCC | 0.063119 |
| PR-AUC, approximate | 0.041552 |
| ROC-AUC, approximate | 0.654087 |
| TP | 14,077,798 |
| FP | 256,162,580 |
| FN | 43,602,698 |
| TN | 1,989,498,477 |

Efficiency:

- model forward time: 31.06 seconds total;
- mean forward time: 0.01593 seconds per inferred patch;
- complete wall time: 684.68 seconds;
- peak CUDA allocation: 1.040 GiB.

Source: [final_metrics.json](../runs/baseline_A_zero_shot_thebe_full_20261005_095032/final_metrics.json).

## 6. Interpretation

The model found only 24.41% of labelled real fault voxels, and only 5.21% of its predicted fault voxels agreed with labels. This is a clear synthetic-to-real domain gap.

Accuracy is not a useful headline here because most scored voxels are background.

## 7. Limits

- The result tests one synthetic model and one frozen threshold.
- Zero amplitude is treated as no-data by the implemented mask.
- Physical spacing is unavailable, so distance units cannot be converted to meters.
- This experiment measures transfer failure; it is not a trained real-data model.

## 8. Evidence

- Full configuration: [run_configuration.json](../runs/baseline_A_zero_shot_thebe_full_20261005_095032/run_configuration.json)
- Full metrics: [final_metrics.json](../runs/baseline_A_zero_shot_thebe_full_20261005_095032/final_metrics.json)
- Per-patch results: [test_per_patch.csv](../runs/baseline_A_zero_shot_thebe_full_20261005_095032/test_per_patch.csv)
- Frozen synthetic checkpoint: [best.pt](../runs/baseline_A_synthetic_bce_seed42/best.pt)

## 9. Simple definitions and calculation

| Term | Meaning |
|---|---|
| Zero-shot transfer | Apply a trained model to a new dataset without updating it. |
| Domain gap | Difference between training data and deployment data. |
| Frozen model | Model weights are not changed. |
| No-data mask | Selects which voxels contain usable recorded input. |
| Padding | Added cells used to complete a boundary patch; excluded here. |
| Valid voxel | A voxel included in the metric. |

Test Dice:

2×14,077,798 / (2×14,077,798 + 256,162,580 + 43,602,698) = **0.085861**

