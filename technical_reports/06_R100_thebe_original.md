# Experiment 6: Original R100 training on real Thebe data

## Quick answer

This experiment trained the small FaultSeg3D U-Net from scratch on real Thebe seismic.

| Item | Answer |
|---|---|
| Initialization | Random; no synthetic checkpoint |
| Training input | 128³ real-data patches |
| Model | 1,459,585-parameter 3D U-Net |
| Seed / epochs | 42 / 100 |
| Selected epoch | 96 |
| Full test Dice | **0.542996** |

Training directly on Thebe improved real-data Dice greatly compared with zero-shot transfer.

## 1. Dataset

| Split | HDF5 blocks | Concatenated shape | Raw voxels |
|---|---:|---:|---:|
| Training | 9 | 900 × 3,174 × 1,537 | 4,390,594,200 |
| Validation | 2 | 200 × 3,174 × 1,537 | 975,687,600 |
| Test | 7 | 703 × 3,174 × 1,537 | 3,429,541,914 |

Full validation scored 613,738,550 valid voxels. Full test scored 2,303,341,553 valid voxels.

Run: [R100_thebe_seed42_20261005_102737](../runs/R100_thebe_seed42_20261005_102737).

## 2. Input → output pipeline

1. Read a 128³ patch from the concatenated HDF5 blocks.
2. Mark finite, nonzero raw seismic voxels as valid.
3. Compute mean and standard deviation only from valid values.
4. Z-score valid values and keep invalid positions at zero.
5. Pad boundary patches to 128³ and exclude padding from metrics.
6. Reverse the three spatial axes.
7. Predict one logit per voxel with the small 3D U-Net.
8. Apply sigmoid and a validation-selected threshold.
9. Calculate loss and metrics only on valid voxels.

## 3. Training method

| Setting | Value |
|---|---|
| Model parameters | 1,459,585 |
| Loss | Ordinary BCE over valid voxels |
| Optimizer | Adam |
| Learning rate | 0.0001 |
| Precision | FP16 autocast with GradScaler |
| Batch / accumulation | 1 / 2 |
| Patches per epoch | 360 |
| Total patch presentations | 36,000 |

Each epoch draws 40 accepted random patches from each of nine training blocks. A candidate must contain enough valid, nonconstant signal. Patches can overlap.

## 4. Resume and checkpoint selection

Training resumed from epoch 23. The checkpoint selection rule changed from Dice at threshold 0.5 to PR-AUC on the same fixed 128 validation patches.

The resume restored model and optimizer state, but the saved epoch-23 checkpoint did not include the earlier random-number-generator or AMP-scaler state. The continuation is therefore valid as a completed run, but not a bit-identical continuation of the interrupted process.

The final threshold, 0.1767578125, was selected on all 650 validation grid patches and frozen for test.

## 5. Results

| Metric | Full validation | Full test |
|---|---:|---:|
| Threshold | 0.176758 | 0.176758 |
| Dice | 0.545409 | **0.542996** |
| IoU | 0.374957 | 0.372679 |
| Precision | 0.527958 | 0.471918 |
| Recall | 0.564053 | 0.639281 |
| Specificity | 0.985521 | 0.981626 |
| Accuracy | 0.973759 | 0.973053 |
| Balanced accuracy | 0.774787 | 0.810453 |
| MCC | 0.532222 | 0.535921 |
| PR-AUC, approximate | 0.557056 | 0.569809 |
| ROC-AUC, approximate | 0.954104 | 0.960459 |
| TP | 9,661,374 | 36,874,035 |
| FP | 8,638,127 | 41,262,560 |
| FN | 7,467,122 | 20,806,461 |
| TN | 587,971,927 | 2,204,398,497 |

Training loss decreased from 0.211608 to 0.052978. The lowest recorded loss was 0.040671. Recorded epoch times total 19,270.55 seconds, about 5.35 hours.

Sources: [final metrics](../runs/R100_thebe_seed42_20261005_102737/final_metrics.json) and [history](../runs/R100_thebe_seed42_20261005_102737/history.csv).

## 6. Comparison with zero-shot transfer

| Real Thebe result | Dice |
|---|---:|
| Synthetic Baseline A, zero-shot | 0.085861 |
| R100 trained on Thebe | **0.542996** |

The difference shows that learning from labelled real-data patches was much more effective than applying the synthetic model unchanged.

## 7. Limits

- This is one seed.
- Random training patches overlap and are not independent volumes.
- Checkpoint selection used 128 fixed validation patches; threshold selection used the full validation grid.
- The test set was used only after the checkpoint and threshold were fixed.
- Nonzero raw amplitude is an implemented no-data rule, not a geological guarantee.

## 8. Evidence

- Configuration: [run_config.json](../runs/R100_thebe_seed42_20261005_102737/run_config.json)
- Resume record: [resume_protocol.json](../runs/R100_thebe_seed42_20261005_102737/resume_protocol.json)
- Validation selection: [validation_selection.json](../runs/R100_thebe_seed42_20261005_102737/validation_selection.json)
- Results: [final_metrics.json](../runs/R100_thebe_seed42_20261005_102737/final_metrics.json)
- Training code used by the later clean implementation: [train_r100_fp16_clean.py](../scripts/train_r100_fp16_clean.py)

## 9. Simple definitions and calculation

| Term | Meaning |
|---|---|
| R100 | This project's real-Thebe training protocol using 100 epochs. |
| Patch | A 128³ crop from the larger survey. |
| Masked BCE | BCE calculated only on valid voxels. |
| Checkpoint selection | Choosing which epoch's weights to keep. |
| Threshold selection | Choosing the probability boundary after weights are fixed. |
| PR-AUC | Precision-recall performance across many thresholds. |
| Resume | Continue training from a saved checkpoint. |

Test Dice:

2×36,874,035 / (2×36,874,035 + 41,262,560 + 20,806,461) = **0.542996**

