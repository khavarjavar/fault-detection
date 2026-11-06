# Experiment 8: R100 ensemble-size curve and additional-seed pilot

## Quick answer

This experiment asks whether adding more independently trained R100 models keeps improving the validation ensemble.

Two stages must be separated:

| Stage | Status |
|---|---|
| Curve using completed seeds 42, 43, 44 | Complete |
| New seeds 45 and 46 for a five-model curve | Still training at the report snapshot |

The completed evidence reaches three models only. It does not yet prove where performance saturates.

## 1. Completed three-model curve

The cached validation probabilities from seeds 42–44 were combined in every possible subset.

| Ensemble size | Number of subsets | Mean Dice | Sample SD | Minimum | Maximum |
|---:|---:|---:|---:|---:|---:|
| 1 | 3 | 0.562302 | 0.015865 | 0.544072 | 0.572980 |
| 2 | 3 | 0.581409 | 0.004551 | 0.577464 | 0.586388 |
| 3 | 1 | 0.588951 | undefined | 0.588951 | 0.588951 |

For each subset, member probabilities were averaged and a new best-Dice threshold was selected on the full validation grid.

The three-model validation ensemble used threshold 0.274902 and obtained:

| Metric | Value |
|---|---:|
| Dice | 0.588951 |
| IoU | 0.417385 |
| Precision | 0.583128 |
| Recall | 0.594892 |
| Specificity | 0.987790 |
| Accuracy | 0.976825 |
| Balanced accuracy | 0.791341 |
| MCC | 0.577059 |
| PR-AUC | 0.616182 |
| ROC-AUC | 0.964916 |

Source: [curve.json](../reports/evaluation/r100_seed_curve_3models_20261019/curve.json).

## 2. How the curve was calculated

1. Run each trained model over the same full validation grid.
2. Cache FP32 probabilities and labels.
3. Choose a subset of model seeds.
4. Average their probabilities voxel by voxel.
5. Search the 2,048 histogram thresholds for the best validation Dice.
6. Repeat for all subsets of each available size.

The curve analysis performed no new neural-network inference and opened no test files. Its checks passed for seven subsets.

## 3. Additional-seed plan

The extension trains seeds 45 and 46 from scratch using the exact clean-R100 protocol.

| Setting | Value |
|---|---|
| Planned seeds | 45, 46 |
| Planned epochs per seed | 100 |
| Fine-tuning | No |
| Validation seed | 1042 |
| Test access | Disabled |
| Next analysis sizes | 1, 2, 3, 5 |

After both models complete, the pipeline plans to cache their validation predictions and measure a five-model curve.

## 4. Live status snapshot

Snapshot: **2026-10-19 15:16:52 +04:00**.

- Queue state: training.
- Completed new seeds: none.
- Active seed: 45.
- Completed recorded epochs for seed 45: 67 of 100.
- Seed 46 had not started.
- Test files had not been opened.

Latest seed-45 row at epoch 67:

| Metric at threshold 0.5 | Value |
|---|---:|
| Training loss | 0.056682 |
| Validation Dice | 0.531178 |
| IoU | 0.361635 |
| Precision | 0.723010 |
| Recall | 0.419796 |
| Specificity | 0.994681 |
| Balanced accuracy | 0.707238 |
| Accuracy | 0.976274 |
| MCC | 0.540209 |
| PR-AUC | 0.608146 |
| ROC-AUC | 0.957069 |

The highest Dice seen in the first 67 history rows was 0.564473. The highest PR-AUC was 0.620218. These are interim fixed-subset values, not final full-validation results.

## 5. Interpretation

The completed curve shows improvement from one to two to three models on validation. The gain becomes smaller, but one three-model point cannot establish saturation.

Five-model evidence does not exist yet. Planned seeds and planned epochs must not be counted as completed results.

## 6. Limits

- Subsets share models and are correlated.
- The size-three SD is undefined because there is only one three-member subset.
- Every subset threshold was optimized on validation, so this is a development curve.
- No five-model result or new-seed frozen test result was available at the snapshot.

## 7. Evidence

- Completed curve: [curve.json](../reports/evaluation/r100_seed_curve_3models_20261019/curve.json)
- Curve checks: [checks.json](../reports/evaluation/r100_seed_curve_3models_20261019/checks.json)
- New-seed plan: [plan.json](../runs/R100_seed_saturation_pilot_20261019/plan.json)
- Queue state: [queue_status.json](../runs/R100_seed_saturation_pilot_20261019/queue_status.json)
- Seed-45 history: [history.csv](../runs/R100_seed_saturation_pilot_20261019/seed45/history.csv)
- Pipeline stages: [pipeline_plan.json](../runs/R100_seed_saturation_pilot_20261019/pipeline_plan.json)

## 8. Simple definitions

| Term | Meaning |
|---|---|
| Ensemble size | Number of models whose probabilities are averaged. |
| Subset | A selected group of available models. |
| Saturation | Adding models gives little or no further improvement. |
| Cached probability | Saved model output reused without another forward pass. |
| Sample SD | Spread across multiple measured subsets; impossible with one subset. |
| Interim result | Measurement from a run that has not completed its planned protocol. |

For three seeds there are three one-model subsets, three two-model subsets, and one three-model subset.

## 9. Metric reminder

Dice = 2TP/(2TP+FP+FN). Higher is better.

The curve's mean Dice is the arithmetic mean across subsets of the same size. It is not a confidence interval and does not make overlapping subsets independent.

