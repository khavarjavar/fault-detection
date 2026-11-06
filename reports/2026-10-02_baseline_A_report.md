# FaultSeg3D Baseline A Training Report

**Date:** 2026-10-02  
**Experiment:** Baseline A  
**Run directory:** `runs/baseline_A_synthetic_bce_seed42`  
**Purpose:** Establish a reproducible synthetic-data baseline before testing improved losses, real-data transfer, self-supervised learning, or knowledge distillation.

## 1. Experiment objective

This experiment tested whether the standard FaultSeg3D 3D U-Net could learn fault segmentation correctly using the prepared training pipeline.

The run provides the reference results against which later methods will be compared.

## 2. Dataset split

| Dataset portion | Volumes | Purpose |
|---|---:|---|
| Training | 180 | Used to update model weights |
| Internal validation | 20 | Used to monitor training, select the best checkpoint, and choose the probability threshold |
| Held-out official test | 20 | Used only for final evaluation |
| Total | 220 | Complete prepared FaultSeg3D dataset |

Each seismic volume and fault mask had a size of `128 × 128 × 128` voxels.

The 180 original training volumes were accompanied by fixed flipped copies, producing 360 training samples per epoch. Validation and test volumes were not augmented.

## 3. Model

| Setting | Value |
|---|---|
| Architecture | Simplified FaultSeg3D 3D U-Net |
| Input channels | 1 |
| Output channels | 1 |
| Trainable parameters | 1,459,585 |
| Encoder channels | 16, 32, 64, 128 |
| Convolutions | `3 × 3 × 3` |
| Downsampling | `2 × 2 × 2` max pooling |
| Upsampling | Nearest-neighbour upsampling |
| Connections | Encoder-decoder skip connections |
| Output | One fault logit per voxel |

## 4. Training configuration

| Setting | Value |
|---|---|
| Epochs | 100 |
| Best epoch | 100 |
| Loss | Ordinary binary cross-entropy |
| Optimizer | Adam |
| Learning rate | 0.0001 |
| Batch size | 1 |
| Gradient accumulation | 2 |
| Effective batch size | 2 |
| Optimizer steps per epoch | 180 |
| Random seed | 42 |
| Mixed precision | Enabled |
| Preprocessing | Per-volume z-score normalization |
| Training augmentation | Fixed flip augmentation |
| GPU | NVIDIA RTX A5500 |
| PyTorch | 2.7.1+cu118 |

No real seismic data, self-supervised learning, seismic attributes, teacher model, distillation, attention module, normalization block, or residual block was used.

## 5. Evaluation protocol

The best checkpoint was selected using internal-validation Dice at a threshold of `0.5`.

After training, the final probability threshold was selected using only the internal validation set. The selected threshold was:

**0.43896484375**

This threshold was then frozen and applied to the held-out test set. The test labels were not used for model selection or threshold selection.

PR-AUC and ROC-AUC were approximated using streaming histograms with 2,048 bins.

All overlap metrics refer to the positive fault class.

## 6. Aggregate results

| Metric | Internal validation | Held-out test |
|---|---:|---:|
| Dice / F1 | 0.8168 | **0.8211** |
| Foreground IoU | 0.6904 | **0.6964** |
| Precision | 0.7992 | **0.8030** |
| Recall | 0.8353 | **0.8399** |
| Specificity | 0.9847 | **0.9839** |
| Balanced accuracy | 0.9100 | **0.9119** |
| MCC | 0.8034 | **0.8070** |
| PR-AUC | 0.8848 | **0.8905** |
| ROC-AUC | 0.9825 | **0.9852** |
| Accuracy | 0.9745 | **0.9735** |

Accuracy is reported for completeness but is not treated as a primary metric because background voxels strongly outnumber fault voxels.

Dice, IoU, PR-AUC, precision, recall, and MCC provide more meaningful measures of fault-segmentation performance.

## 7. Test confusion counts

| Count | Value |
|---|---:|
| True positives | 2,546,874 |
| False positives | 624,787 |
| False negatives | 485,344 |
| True negatives | 38,286,035 |

Recall was higher than precision, meaning the model detected most fault voxels while producing slightly more false-positive than false-negative errors.

## 8. Per-volume test results

| Metric | Mean | Standard deviation | Median | Minimum | Maximum |
|---|---:|---:|---:|---:|---:|
| Dice | 0.8237 | 0.0423 | 0.8203 | 0.7186 | 0.8970 |
| IoU | 0.7025 | 0.0607 | 0.6953 | 0.5609 | 0.8132 |
| Precision | 0.8056 | 0.0412 | 0.8117 | 0.7119 | 0.8781 |
| Recall | 0.8429 | 0.0457 | 0.8374 | 0.7255 | 0.9167 |
| MCC | 0.8097 | 0.0465 | 0.8015 | 0.7013 | 0.8903 |
| PR-AUC | 0.8911 | 0.0460 | 0.8873 | 0.7741 | 0.9665 |
| ROC-AUC | 0.9852 | 0.0083 | 0.9839 | 0.9686 | 0.9976 |
| Balanced accuracy | 0.9134 | 0.0248 | 0.9088 | 0.8538 | 0.9542 |

The aggregate Dice and mean per-volume Dice differ slightly because the aggregate result pools all voxels, while the per-volume mean gives every volume equal weight.

## 9. Structural-distance results

Lower structural distances indicate better spatial alignment between predicted and labelled faults.

| Metric | Test mean | Test median | Test minimum | Test maximum |
|---|---:|---:|---:|---:|
| Modified Hausdorff distance | 0.2923 voxels | 0.2773 | 0.1302 | 0.5575 |
| Bidirectional Chamfer distance | 0.5040 voxels | 0.4973 | 0.2151 | 0.9416 |

The modified Hausdorff implementation is the maximum of the two directed mean nearest-point distances.

The bidirectional Chamfer implementation is the sum of the two directed mean nearest-point distances.

## 10. Efficiency

| Measurement | Result |
|---|---:|
| Peak allocated GPU memory | 1.239 GiB |
| Total GPU memory | 23.679 GiB |
| Mean inference time per test volume | 0.0878 seconds |
| Model parameters | 1,459,585 |

The model used only a small portion of the available GPU memory and performed inference quickly on full `128³` volumes.

## 11. Training behaviour

The final five epochs produced validation Dice values between approximately 0.807 and 0.816 at the fixed threshold of `0.5`.

Epoch 100 achieved the best checkpoint-selection Dice. This indicates that the model was still competitive at the end of training, although the final epochs showed normal validation fluctuation.

The final reported validation and test metrics use the validation-selected threshold of `0.43896484375`, while the epoch history uses the fixed threshold of `0.5`. Therefore, the history and final metrics are expected to differ slightly.

## 12. Interpretation

Baseline A successfully learned the synthetic FaultSeg3D dataset.

The held-out test Dice of 0.8211 and IoU of 0.6964 establish a strong reference result. Test performance was slightly higher than internal-validation performance, so the validation-to-test comparison does not show evidence of overfitting.

The model achieved recall of 0.8399 and precision of 0.8030. It therefore detected a large proportion of labelled fault voxels, with some remaining false-positive predictions.

The small structural distances indicate that predicted fault locations were generally close to the labelled fault surfaces.

Performance still varied between individual test volumes. The worst test-volume Dice was 0.7186, compared with a maximum of 0.8970. Future work should inspect these weaker cases visually.

## 13. Conclusion

Baseline A completed all 100 epochs successfully.

The experiment confirms that:

1. The data-loading and preprocessing pipeline works.
2. The FaultSeg3D architecture learns the synthetic fault labels.
3. Checkpoint and metric logging work correctly.
4. The validation-selected threshold transfers successfully to the held-out test set.
5. The results provide a reference for controlled comparisons.

## 14. Next controlled experiment

The next experiment is **Loss Ablation L1: weighted BCE plus Dice loss**.

Loss Ablation L1 kept the following settings identical:

- Model architecture
- Dataset
- `180/20/20` split
- Random seed
- Learning rate
- Batch size
- Gradient accumulation
- Preprocessing
- Augmentation
- Number of epochs
- Evaluation protocol

Only the loss function will change to:

`0.5 × weighted BCE + 0.5 × soft Dice loss`

The positive-class weight will be `13.211662`.

This controlled comparison will show whether explicit class-imbalance handling and overlap optimization improve fault segmentation over ordinary BCE.

## 15. Saved artifacts

- `runs/baseline_A_synthetic_bce_seed42/run_config.json`
- `runs/baseline_A_synthetic_bce_seed42/history.csv`
- `runs/baseline_A_synthetic_bce_seed42/best.pt`
- `runs/baseline_A_synthetic_bce_seed42/last.pt`
- `runs/baseline_A_synthetic_bce_seed42/final_metrics.json`
- `runs/baseline_A_synthetic_bce_seed42/validation_per_volume.csv`
- `runs/baseline_A_synthetic_bce_seed42/test_per_volume.csv`
- `reports/training/baseline_A_synthetic_bce_seed42.log`
