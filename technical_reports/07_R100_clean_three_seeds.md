# Experiment 7: Clean R100 three-seed study and frozen test

## Quick answer

Three independently initialized R100 models were trained with the same fixed protocol.

| Result | Dice |
|---|---:|
| Mean full-validation Dice | 0.562302 |
| Mean individual test Dice | 0.552587 |
| Three-model ensemble test Dice | **0.581257** |

The ensemble performed better than every individual member on the frozen test.

## 1. Why there are three top-level folders

| Folder | Outcome |
|---|---|
| [145225](../runs/R100_fp16_clean_3seeds_20261014_145225) | Failed during smoke test; no completed seed |
| [145510](../runs/R100_fp16_clean_3seeds_20261014_145510) | Smoke passed, then seed 42 trainer exited; no completed seed set |
| [150435](../runs/R100_fp16_clean_3seeds_20261014_150435) | Smoke passed; seeds 42, 43, and 44 completed |

These are launch attempts for one three-seed experiment, not three scientific methods.

## 2. Dataset and pipeline

The experiment uses the same nine training and two validation HDF5 blocks as Experiment 6. Each model receives 360 accepted 128³ patches per epoch for 100 epochs.

Pipeline:

HDF5 patch → finite/nonzero valid mask → valid-only z-score → zero padding when needed → axis reversal → small 3D U-Net → masked BCE → validation metrics.

Training never opens the seven test files.

## 3. Fixed training protocol

All seeds use:

- random initialization;
- 1,459,585-parameter FaultSeg3D;
- Adam at 0.0001;
- batch 1 and gradient accumulation 2;
- FP16 autocast and gradient scaling;
- 360 patches per epoch;
- the same validation subset seed, 1042;
- the same protocol hash: 1febc1e47ba203ff08db82816ceadf616a5e7db345054cfbe45274b84c5f5437.

The best epoch is chosen by PR-AUC on 128 fixed validation patches. Each final threshold is then selected on the full 650-patch validation grid.

## 4. Validation results

| Seed | Best epoch | Threshold | Dice | IoU | Precision | Recall | PR-AUC |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 42 | 95 | 0.316406 | 0.544072 | 0.373694 | 0.526766 | 0.562554 | 0.552091 |
| 43 | 93 | 0.279297 | 0.569856 | 0.398460 | 0.564389 | 0.575429 | 0.592053 |
| 44 | 95 | 0.244141 | 0.572980 | 0.401522 | 0.565569 | 0.580587 | 0.593405 |

Validation Dice mean = **0.562302**. Sample standard deviation = **0.015865**.

## 5. Frozen test protocol

Before test evaluation:

1. checkpoint hashes were frozen;
2. all three validation histograms were reproduced exactly;
3. each seed's validation threshold remained unchanged;
4. the three-model ensemble threshold, 0.27490234375, was chosen on validation;
5. test inference then covered the full seven-block test grid once.

The ensemble averages the three FP32 probabilities for each voxel. It does not average weights or logits.

## 6. Frozen test results

| Metric | Seed 42 | Seed 43 | Seed 44 | Ensemble |
|---|---:|---:|---:|---:|
| Threshold | 0.316406 | 0.279297 | 0.244141 | 0.274902 |
| Dice | 0.524797 | 0.567466 | 0.565498 | **0.581257** |
| IoU | 0.355745 | 0.396128 | 0.394212 | 0.409699 |
| Precision | 0.451651 | 0.502357 | 0.508718 | 0.517305 |
| Recall | 0.626213 | 0.651965 | 0.636545 | 0.663253 |
| Specificity | 0.980472 | 0.983411 | 0.984211 | 0.984104 |
| Accuracy | 0.971601 | 0.975111 | 0.975504 | 0.976069 |
| Balanced accuracy | 0.803342 | 0.817688 | 0.810378 | 0.823678 |
| MCC | 0.517810 | 0.559877 | 0.556738 | 0.573795 |
| PR-AUC | 0.542555 | 0.600605 | 0.595039 | 0.620308 |
| ROC-AUC | 0.961577 | 0.966376 | 0.964450 | 0.970100 |
| TP | 36,120,265 | 37,605,673 | 36,716,218 | 38,256,762 |
| FP | 43,853,508 | 37,252,723 | 35,457,728 | 35,697,272 |
| FN | 21,560,231 | 20,074,823 | 20,964,278 | 19,423,734 |
| TN | 2,201,807,549 | 2,208,408,334 | 2,210,203,329 | 2,209,963,785 |

The individual-seed test Dice mean is 0.552587 with sample SD 0.024087. The ensemble improves over that mean by 0.028670 and over the best single seed by 0.013791.

Full test inference took 444.46 seconds for the shared three-forward-pass evaluation. Peak CUDA allocation was 1.039 GiB.

## 7. Interpretation and limits

The different seed results show that initialization and sampling matter. Three seeds provide some evidence of variability, but still form a small sample.

The ensemble improved Dice, recall, PR-AUC, ROC-AUC, MCC, and balanced accuracy. Its test set was not used to set the threshold.

The three models are correlated because they share architecture, data, and protocol. Ensemble members should not be treated as independent surveys.

## 8. Evidence

- Completed queue: [queue_status.json](../runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json)
- Seed selections: [seed42](../runs/R100_fp16_clean_3seeds_20261014_150435/seed42/validation_selection.json), [seed43](../runs/R100_fp16_clean_3seeds_20261014_150435/seed43/validation_selection.json), [seed44](../runs/R100_fp16_clean_3seeds_20261014_150435/seed44/validation_selection.json)
- Frozen test: [final_metrics.json](../reports/evaluation/r100_clean_frozen_test_20261019/final_metrics.json)
- Independent verification: [verification.json](../reports/evaluation/r100_clean_frozen_test_20261019/verification.json)
- Trainer: [train_r100_fp16_clean.py](../scripts/train_r100_fp16_clean.py)

The verification passed: checkpoint hashes matched, validation histograms matched exactly, and independent metric recomputation agreed to floating-point precision.

## 9. Simple definitions and calculations

| Term | Meaning |
|---|---|
| Seed | Controls random initialization and sampling. Different seeds can produce different models. |
| Sample SD | Spread among repeated runs, using division by n−1. |
| Ensemble | Combines predictions from several models. |
| Probability averaging | Mean of member probabilities at each voxel. |
| Frozen test | Test evaluated only after model and threshold choices are fixed. |
| Protocol hash | Fingerprint of the agreed experimental procedure. |

Ensemble test Dice:

2×38,256,762 / (2×38,256,762 + 35,697,272 + 19,423,734) = **0.581257**

Seed-mean Dice:

(0.524797 + 0.567466 + 0.565498) / 3 = **0.552587**
