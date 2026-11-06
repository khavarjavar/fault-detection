# Experiment 2: Weighted BCE + Dice loss on synthetic FaultSeg3D

## Quick answer

This experiment kept the same data and 3D U-Net as Experiment 1, but changed the training loss.

| Item | Answer |
|---|---|
| Input/output | 128³ seismic cube → 128³ fault mask |
| Model | Small FaultSeg3D U-Net, 1,459,585 parameters |
| Changed component | Training loss only |
| Seed / epochs | 42 / 100 |
| Selected epoch | 100 |
| Test Dice | **0.819766** |
| Baseline A test Dice | 0.821059 |

The changed loss did not improve test Dice in this single matched-seed comparison. The difference was −0.001293.

## 1. Purpose

Test whether class-weighted BCE plus soft Dice loss improves synthetic fault segmentation relative to ordinary BCE.

Run: [loss_ablation_L1_weighted_bce_dice_seed42](../runs/loss_ablation_L1_weighted_bce_dice_seed42)

## 2. Dataset

The split is identical to Experiment 1.

| Split | Original cubes | Voxels | Fault voxels |
|---|---:|---:|---:|
| Training | 180 | 377,487,360 | 26,561,803 |
| Validation | 20 | 41,943,040 | 2,851,880 |
| Test | 20 | 41,943,040 | 3,032,218 |

A fixed flipped copy gives 360 training presentations per epoch. Exact IDs are in the [manifests](../data/manifests).

## 3. Pipeline

Raw seismic/label pair → reshape to 128³ → per-volume z-score → transpose axes → optional fixed flip → 3D U-Net → sigmoid probability → validation-selected threshold → binary fault mask.

All synthetic voxels are scored. Code: [faultseg3d_baseline.py](../scripts/faultseg3d_baseline.py).

## 4. Method

Training settings match Experiment 1: Adam, learning rate 0.0001, batch 1, accumulation 2, FP16 autocast, and 100 epochs.

The loss is:

**total loss = 0.5 × weighted BCE + 0.5 × soft Dice loss**

- Weighted BCE multiplies the positive fault term by 13.211662.
- Soft Dice loss is 1 − (2Σpy + 1)/(Σp + Σy + 1).
- p is predicted probability and y is the 0/1 label.

Unlike Experiment 1, this run really uses pos_weight. The model architecture is unchanged, so this comparison changes the loss rather than model size.

## 5. Evaluation

The checkpoint was selected by validation Dice at threshold 0.5. The final threshold, 0.85302734375, was selected on all validation cubes and then frozen for test.

## 6. Results

Full precision: [final_metrics.json](../runs/loss_ablation_L1_weighted_bce_dice_seed42/final_metrics.json).

| Metric | Final validation | Test |
|---|---:|---:|
| Threshold | 0.853027 | 0.853027 |
| Dice | 0.818194 | **0.819766** |
| IoU | 0.692325 | 0.694579 |
| Precision | 0.799240 | 0.804110 |
| Recall | 0.838068 | 0.836043 |
| Specificity | 0.984642 | 0.984129 |
| Accuracy | 0.974676 | 0.973423 |
| Balanced accuracy | 0.911355 | 0.910086 |
| MCC | 0.804853 | 0.805603 |
| PR-AUC, approximate | 0.875304 | 0.876373 |
| ROC-AUC, approximate | 0.978160 | 0.980179 |
| TP | 2,390,069 | 2,535,066 |
| FP | 600,358 | 617,570 |
| FN | 461,811 | 497,152 |
| TN | 38,490,802 | 38,293,252 |

Training loss fell from 1.044174 to 0.144759; the minimum was 0.143432. Recorded epoch time totals 1,880.78 seconds. Peak CUDA allocation was 1.239 GiB.

Per-cube values: [validation CSV](../runs/loss_ablation_L1_weighted_bce_dice_seed42/validation_per_volume.csv) and [test CSV](../runs/loss_ablation_L1_weighted_bce_dice_seed42/test_per_volume.csv).

## 7. Interpretation

Compared with ordinary BCE:

| Test metric | Ordinary BCE | Changed loss | Difference |
|---|---:|---:|---:|
| Dice | 0.821059 | 0.819766 | −0.001293 |
| Precision | 0.803010 | 0.804110 | +0.001100 |
| Recall | 0.839938 | 0.836043 | −0.003894 |
| PR-AUC | 0.890460 | 0.876373 | −0.014087 |

This one-seed result does not support an improvement. A repeated-seed study would be needed to estimate run-to-run variation.

## 8. Evidence

- Settings: [run_config.json](../runs/loss_ablation_L1_weighted_bce_dice_seed42/run_config.json)
- Full history: [history.csv](../runs/loss_ablation_L1_weighted_bce_dice_seed42/history.csv)
- Results: [final_metrics.json](../runs/loss_ablation_L1_weighted_bce_dice_seed42/final_metrics.json)
- Checkpoint: [best.pt](../runs/loss_ablation_L1_weighted_bce_dice_seed42/best.pt)
- Loss code: [SegmentationLoss](../scripts/faultseg3d_baseline.py#L186)

## 9. Simple definitions and calculation

| Term | Meaning |
|---|---|
| Ablation | Change one component to study its effect. Here, the loss changed. |
| BCE | Penalizes wrong fault/background probabilities. |
| Class weight | Gives fault voxels more influence in BCE. |
| Soft Dice | Dice-like calculation using probabilities instead of thresholded 0/1 predictions. |
| TP / FP / FN / TN | Correct fault / false fault / missed fault / correct background. |
| Dice | 2TP/(2TP+FP+FN). Higher is better. |
| Precision | TP/(TP+FP). Of predicted faults, how many were correct? |
| Recall | TP/(TP+FN). Of labelled faults, how many were found? |

Test Dice:

2×2,535,066 / (2×2,535,066 + 617,570 + 497,152) = **0.819766**

