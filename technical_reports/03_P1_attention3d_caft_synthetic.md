# Experiment 3: P1 attention + CAFT on synthetic FaultSeg3D

## Quick answer

P1 adds attention gates and a connectivity-aware loss to the small 3D U-Net.

| Item | Answer |
|---|---|
| Data | Same 180/20/20 synthetic split as Experiment 1 |
| Parameters | 1,467,411 |
| Seed / epochs | 42 / 100 |
| Selected epoch | 93 |
| Test Dice | **0.826646** |
| Baseline A test Dice | 0.821059 |

P1 increased Dice by 0.005587 in this one-seed comparison, but its PR-AUC and ROC-AUC were lower.

## 1. Purpose

Test whether attention-guided skip connections plus connectivity-aware focal Tversky loss improve synthetic fault segmentation.

Run: [p1_attention3d_caft_seed42](../runs/p1_attention3d_caft_seed42)

## 2. Dataset and pipeline

The data and preprocessing match Experiment 1:

- 180 training, 20 validation, and 20 test cubes;
- each cube is 128³;
- per-volume z-score, axis transpose, and fixed training flip;
- 360 training presentations per epoch;
- all voxels scored.

## 3. Model

P1 starts with the same U-Net and adds two attention gates on the deeper encoder-to-decoder skip connections.

Each gate combines:

1. an encoder feature map;
2. a coarser decoder feature map;
3. a learned sigmoid attention mask.

The mask multiplies the encoder feature map before it enters the decoder. The model has 7,826 more parameters than Baseline A.

Code: [Attention3D and ActiveAttentionModule](../scripts/attention3d_caft.py#L31).

## 4. Training loss

The total loss combines:

- connectivity-aware focal Tversky loss;
- Smooth L1 supervision for the two attention maps.

Saved settings:

| Setting | Value |
|---|---:|
| False-positive weight | 0.3 |
| False-negative weight | 0.7 |
| Focal power | 4/3 |
| Connectivity | Undirected 6-neighbour |
| Attention-target Gaussian sigma | 1.5 |
| Attention-loss weight | 1.0 |

The connectivity calculation includes fault voxels and neighbouring fault-to-fault edges along the three positive spatial directions. The attention target is made from pooled and Gaussian-smoothed labels.

Other settings match the baseline: Adam, learning rate 0.0001, batch 1, accumulation 2, FP16, seed 42, 100 epochs.

## 5. Model selection

The best epoch was selected using validation Dice at threshold 0.5. Epoch 93 was selected. The final threshold, 0.98095703125, was selected only on validation and frozen for test.

## 6. Results

Full precision: [final_metrics.json](../runs/p1_attention3d_caft_seed42/final_metrics.json).

| Metric | Final validation | Test |
|---|---:|---:|
| Threshold | 0.980957 | 0.980957 |
| Dice | 0.821408 | **0.826646** |
| IoU | 0.696941 | 0.704515 |
| Precision | 0.791906 | 0.796766 |
| Recall | 0.853195 | 0.858854 |
| Specificity | 0.983644 | 0.982928 |
| Accuracy | 0.974774 | 0.973959 |
| Balanced accuracy | 0.918419 | 0.920891 |
| MCC | 0.808507 | 0.813258 |
| PR-AUC, approximate | 0.721467 | 0.733316 |
| ROC-AUC, approximate | 0.935983 | 0.939682 |
| TP | 2,433,209 | 2,604,232 |
| FP | 639,391 | 664,270 |
| FN | 418,671 | 427,986 |
| TN | 38,451,769 | 38,246,552 |

Training loss fell from 0.838507 to 0.063203. Total recorded epoch time was 2,078.37 seconds. Peak CUDA allocation was 1.308 GiB.

Per-cube values: [validation CSV](../runs/p1_attention3d_caft_seed42/validation_per_volume.csv) and [test CSV](../runs/p1_attention3d_caft_seed42/test_per_volume.csv).

## 7. Interpretation

| Test metric | Baseline A | P1 | Difference |
|---|---:|---:|---:|
| Dice | 0.821059 | 0.826646 | +0.005587 |
| Recall | 0.839938 | 0.858854 | +0.018916 |
| Precision | 0.803010 | 0.796766 | −0.006243 |
| PR-AUC | 0.890460 | 0.733316 | −0.157144 |

P1 has slightly better thresholded overlap and recall, but weaker probability ranking. It also changed both the architecture and the loss, so this experiment cannot say which change caused the difference.

## 8. Evidence

- Settings: [run_config.json](../runs/p1_attention3d_caft_seed42/run_config.json)
- Results: [final_metrics.json](../runs/p1_attention3d_caft_seed42/final_metrics.json)
- History: [history.csv](../runs/p1_attention3d_caft_seed42/history.csv)
- Checkpoint: [best.pt](../runs/p1_attention3d_caft_seed42/best.pt)
- Implementation: [attention3d_caft.py](../scripts/attention3d_caft.py)

## 9. Simple definitions and calculation

| Term | Meaning |
|---|---|
| Attention gate | A learned mask that controls which feature locations pass to the decoder. |
| Skip connection | Sends encoder features directly to the matching decoder level. |
| Connectivity | Whether neighbouring predicted fault voxels form connected structures. |
| Tversky score | Dice-like overlap with separate penalties for FP and FN. |
| Focal power | Gives harder mistakes more influence in the loss. |
| Smooth L1 | A stable difference measure used to train attention maps. |
| PR-AUC | Precision-recall quality across many thresholds. |

Test Dice:

2×2,604,232 / (2×2,604,232 + 664,270 + 427,986) = **0.826646**

