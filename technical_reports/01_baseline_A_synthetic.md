# Experiment 1: Baseline A on synthetic FaultSeg3D

## Quick answer

This experiment trained a small **3D U-Net** to mark fault voxels in synthetic seismic cubes.

| Item | Answer |
|---|---|
| Input | One seismic cube, `128 × 128 × 128` voxels |
| Output | One fault mask of the same size |
| Training data | 180 original cubes |
| Validation data | 20 cubes |
| Test data | 20 held-out cubes |
| Loss | Ordinary binary cross-entropy (BCE) |
| Seed | 42 |
| Selected model | Epoch 100 |
| Main test result | **Dice = 0.821059** |

The run completed successfully. It shows strong overlap with the synthetic test labels. It does not prove that the model works equally well on real seismic data.

## 1. Purpose

The question was:

> How well can the basic FaultSeg3D model segment faults in synthetic data using ordinary BCE loss?

This result is the baseline for comparing later loss functions and models.

## 2. Dataset

Every example contains a seismic volume and a matching label volume. A label of `1` means fault; `0` means background.

Each cube contains:

`128 × 128 × 128 = 2,097,152 voxels`

| Split | Original cubes | Total voxels | Fault voxels | Fault percentage |
|---|---:|---:|---:|---:|
| Training | 180 | 377,487,360 | 26,561,803 | 7.0365% |
| Validation | 20 | 41,943,040 | 2,851,880 | 6.7994% |
| Test | 20 | 41,943,040 | 3,032,218 | 7.2294% |

The code makes one fixed flipped copy of every training cube. It therefore presents 360 samples per epoch, but only **180 are independent original cubes**. Across 100 epochs, it presents 36,000 samples.

The 180 training and 20 validation IDs come from the local training folder. The 20 held-out test cubes come from the dataset's validation folder. Exact IDs are in the [training](../data/manifests/faultseg3d_train.txt), [validation](../data/manifests/faultseg3d_val.txt), and [test](../data/manifests/faultseg3d_test.txt) manifests.

The stored [dataset audit](../reports/data_audit/faultseg3d_volume_statistics.csv) verifies the counts. Physical voxel spacing and the original synthetic-generation settings are not recorded, so they are unknown.

## 3. Input → output pipeline

1. Read a seismic file and its matching fault-label file.
2. Reshape each file to `128 × 128 × 128`.
3. Normalize the seismic cube using its own mean and standard deviation.
4. Reverse the array-axis order using `np.transpose`.
5. During training, use the original cube and its fixed flipped copy.
6. Pass a tensor shaped `[batch, channel, depth, height, width] = [1,1,128,128,128]` to the model.
7. Produce one score per voxel.
8. Apply sigmoid to convert each score to a probability.
9. Predict fault when probability ≥ `0.43896484375`.

All voxels are scored. This synthetic experiment has no missing-data mask.

Code: [dataset loader](../scripts/faultseg3d_baseline.py#L116) and [evaluation function](../scripts/faultseg3d_baseline.py#L418).

## 4. Model and training

The model is a small 3D U-Net with **1,459,585 trainable parameters**.

| Model part | Channels | Spatial size |
|---|---:|---:|
| Input | 1 | 128³ |
| Encoder | 16 → 32 → 64 | 128³ → 64³ → 32³ |
| Bottleneck | 128 | 16³ |
| Decoder | 64 → 32 → 16 | 32³ → 64³ → 128³ |
| Output | 1 | 128³ |

It uses 3D convolutions and ReLU, max pooling to reduce size, nearest-neighbour upsampling to restore size, and skip connections between the encoder and decoder. It has no batch normalization or dropout. Code: [FaultSeg3D model](../scripts/faultseg3d_baseline.py#L74).

| Training setting | Value |
|---|---|
| Epochs | 100 |
| Optimizer | Adam |
| Learning rate | 0.0001 |
| Batch size | 1 |
| Gradient accumulation | 2 |
| Effective batch size | 2 |
| Attempted optimizer steps | 180 per epoch; 18,000 total |
| Precision | FP16 autocast with GradScaler |
| GPU | NVIDIA RTX A5500 |
| PyTorch | 2.7.1+cu118 |

The loss is ordinary BCE. The saved configuration contains `pos_weight = 13.211662`, but the selected `b0_bce` code path does not use it. This experiment therefore did **not** use weighted BCE. Code: [loss implementation](../scripts/faultseg3d_baseline.py#L186).

## 5. How the final model was chosen

1. After each epoch, calculate validation Dice at threshold `0.5`.
2. Save the epoch with the highest Dice. Epoch 100 won.
3. Using that checkpoint, find the threshold with the best validation Dice.
4. Freeze that threshold: `0.43896484375`.
5. Use the frozen threshold on the test set.

The test labels were not used to select the threshold.

## 6. Results

Values are rounded to six decimal places. [final_metrics.json](../runs/baseline_A_synthetic_bce_seed42/final_metrics.json) contains full precision.

| Metric | Validation at 0.5 | Final validation | Test |
|---|---:|---:|---:|
| Threshold | 0.500000 | 0.438965 | 0.438965 |
| Dice | 0.815808 | 0.816844 | **0.821059** |
| IoU | 0.688915 | 0.690394 | **0.696437** |
| Precision | 0.816103 | 0.799195 | **0.803010** |
| Recall | 0.815513 | 0.835289 | **0.839938** |
| Specificity | 0.986594 | 0.984689 | **0.983943** |
| Accuracy | 0.974961 | 0.974530 | **0.973532** |
| Balanced accuracy | 0.901053 | 0.909989 | **0.911940** |
| MCC | 0.802375 | 0.803391 | **0.807013** |
| PR-AUC (approximate) | 0.884834 | 0.884834 | **0.890460** |
| ROC-AUC (approximate) | 0.982462 | 0.982462 | **0.985232** |

### Test voxel counts

| Count | Meaning | Value |
|---|---|---:|
| TP | Fault correctly detected | 2,546,874 |
| FP | Background incorrectly called fault | 624,787 |
| FN | Fault missed | 485,344 |
| TN | Background correctly detected | 38,286,035 |
| Total | All test voxels | 41,943,040 |

### Variation across the 20 cubes

The table shows mean ± population standard deviation.

| Metric | Validation | Test |
|---|---:|---:|
| Dice | 0.814626 ± 0.047553 | 0.823715 ± 0.042342 |
| IoU | 0.689806 ± 0.064285 | 0.702450 ± 0.060669 |
| Modified Hausdorff, voxels | 0.365260 ± 0.227977 | 0.292329 ± 0.105241 |
| Bidirectional Chamfer, voxels | 0.600640 ± 0.333454 | 0.504011 ± 0.176213 |
| Model forward time per cube | 0.077607 ± 0.013397 s | 0.087784 ± 0.006291 s |

Every cube's results are in [validation_per_volume.csv](../runs/baseline_A_synthetic_bce_seed42/validation_per_volume.csv) and [test_per_volume.csv](../runs/baseline_A_synthetic_bce_seed42/test_per_volume.csv).

### Training summary

- Loss decreased from **0.314965** at epoch 1 to **0.040481** at epoch 100.
- Lowest recorded loss: **0.039896**.
- Sum of recorded epoch times: **2,855.94 seconds**, about **47.6 minutes**.
- Peak recorded CUDA allocation: **1.239 GiB**.
- The saved checkpoint contains no non-finite weights.

The full 100-epoch record is in [history.csv](../runs/baseline_A_synthetic_bce_seed42/history.csv).

## 7. Meaning and limits

On the test set:

- Recall `0.839938`: the model found about 84.0% of labelled fault voxels.
- Precision `0.803010`: about 80.3% of predicted fault voxels were labelled faults.
- Dice `0.821059`: predicted and labelled fault regions had strong overlap.
- Accuracy `0.973532`: 97.35% of all voxels were correct. Because 92.77% of voxels are background, accuracy alone can look better than fault detection really is.

Limits:

- This is one training run with one seed.
- The test data are synthetic, not real field surveys.
- Some CUDA operations in the log are not fully deterministic, so the same seed may not produce identical weights.
- The saved artifacts were checked, but inference was not rerun for this report.
- This early run did not save a source-code hash, so the exact historical code file cannot be proven byte-for-byte.

## 8. Evidence

| Information | Verified source |
|---|---|
| Settings | [run_config.json](../runs/baseline_A_synthetic_bce_seed42/run_config.json) |
| Final results | [final_metrics.json](../runs/baseline_A_synthetic_bce_seed42/final_metrics.json) |
| Training history | [history.csv](../runs/baseline_A_synthetic_bce_seed42/history.csv) |
| Training messages | [training log](../reports/training/baseline_A_synthetic_bce_seed42.log) |
| Code | [faultseg3d_baseline.py](../scripts/faultseg3d_baseline.py) |
| Dataset audit | [faultseg3d_volume_statistics.csv](../reports/data_audit/faultseg3d_volume_statistics.csv) |
| Model weights | [best.pt](../runs/baseline_A_synthetic_bce_seed42/best.pt) |

The report uses code and saved artifacts as evidence. Missing facts are labelled unknown instead of guessed.

## 9. Simple vocabulary and calculations

### Basic terms

| Term | Simple meaning |
|---|---|
| Voxel | One cell in a 3D volume; the 3D equivalent of a pixel. |
| Label | The supplied answer: fault or background. |
| Segmentation | Predicting a class for every voxel. |
| 3D U-Net | A model that compresses a volume, learns features, then expands it into a full-size mask. |
| Encoder / decoder | The encoder reduces size; the decoder restores it. |
| Skip connection | Passes encoder information directly to the decoder. |
| Epoch | One pass through the configured training samples. |
| Loss | The value minimized while training. |
| BCE | A loss for a two-class prediction such as fault/background. |
| Logit | The model's raw output. |
| Sigmoid | Converts a logit into a probability from 0 to 1. |
| Threshold | The probability boundary between fault and background. |
| Checkpoint | Saved model weights from one epoch. |
| TP / FP / FN / TN | Correct fault / false fault / missed fault / correct background. |

### Metric formulas

| Metric | Formula | Meaning |
|---|---|---|
| Dice | `2TP / (2TP + FP + FN)` | Fault overlap. Higher is better. |
| IoU | `TP / (TP + FP + FN)` | Fault intersection divided by union. Higher is better. |
| Precision | `TP / (TP + FP)` | Fraction of predicted faults that are correct. |
| Recall | `TP / (TP + FN)` | Fraction of labelled faults found. |
| Specificity | `TN / (TN + FP)` | Fraction of background correctly kept as background. |
| Accuracy | `(TP + TN) / all voxels` | Fraction of all voxels classified correctly. |
| Balanced accuracy | `(recall + specificity) / 2` | Equal average of fault and background performance. |
| MCC | `(TP×TN−FP×FN) / sqrt((TP+FP)(TP+FN)(TN+FP)(TN+FN))` | Balanced score from −1 to 1. Higher is better. |
| PR-AUC | Area under the precision-recall curve | Performance across many thresholds. Higher is better. |
| ROC-AUC | Area under the recall/false-positive-rate curve | Ranking quality across many thresholds. Higher is better. |
| Modified Hausdorff | Larger directed mean nearest-fault distance | Location error in voxels. Lower is better. |
| Bidirectional Chamfer | Sum of both directed mean nearest-fault distances | Location error in voxels. Lower is better. |

PR-AUC and ROC-AUC are approximate because the code groups probabilities into 2,048 bins.

### Worked calculations with the real test counts

`TP = 2,546,874`, `FP = 624,787`, `FN = 485,344`, `TN = 38,286,035`

| Metric | Calculation | Result |
|---|---|---:|
| Dice | `2×2,546,874 / (2×2,546,874 + 624,787 + 485,344)` | 0.821059 |
| IoU | `2,546,874 / (2,546,874 + 624,787 + 485,344)` | 0.696437 |
| Precision | `2,546,874 / (2,546,874 + 624,787)` | 0.803010 |
| Recall | `2,546,874 / (2,546,874 + 485,344)` | 0.839938 |
| Specificity | `38,286,035 / (38,286,035 + 624,787)` | 0.983943 |
| Accuracy | `(2,546,874 + 38,286,035) / 41,943,040` | 0.973532 |
| Balanced accuracy | `(0.839938 + 0.983943) / 2` | 0.911940 |

PR-AUC and ROC-AUC need predictions at many thresholds. They cannot be reconstructed from one TP/FP/FN/TN table.
