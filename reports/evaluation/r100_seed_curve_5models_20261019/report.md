# R100 validation ensemble-size measurement

Available clean seeds: 42, 43, 44, 45, 46.

This is a validation-only measurement. Every combination selects its own threshold on the same full validation data it scores. These are apparent validation scores, not held-out performance estimates.

| Models averaged | Subsets measured | Mean validation Dice | Subset sample SD | Min | Max |
|---:|---:|---:|---:|---:|---:|
| 1 | 5 | 0.567004 | 0.013429 | 0.544072 | 0.579161 |
| 2 | 10 | 0.585089 | 0.005637 | 0.576436 | 0.594420 |
| 3 | 10 | 0.591796 | 0.003179 | 0.586883 | 0.596052 |
| 5 | 1 | 0.597311 | not estimable (one subset) | 0.597311 | 0.597311 |

Subset SD describes sensitivity to which models are selected from this finite pool. Combinations share models and are correlated; the bars are not confidence intervals across new surveys or newly trained seed pools. A single full-pool ensemble does not establish zero uncertainty.

This result is conditional on the 5 available seeds. It cannot establish performance at larger sizes than that pool. Three seeds alone cannot establish saturation at eight, ten, or forty.

The analysis reads FP32 cached probabilities and labels; it performs arithmetic and histogram scoring, without neural-network inference, training, or opening Thebe HDF5 files. No test evaluation occurs.

Keep flip TTA, alternative losses, overlap inference, and checkpoint/weight averaging in separately named experiments. They change factors beyond seed count.

## Pilot comparison

Original three-model validation Dice: **0.588951**. Five-model Dice: **0.597311**. Difference: **+0.008360**.

Within the same five-seed pool, mean three-model Dice is 0.591796; five-model gain over that mean is +0.005515. The 0.002 reference is a compute-budget heuristic, not a significance test.

![Validation curve](curve.png)
