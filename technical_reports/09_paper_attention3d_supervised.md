# Experiment 9: Imported paper Attention3D supervised attempts

## Quick answer

This experiment adapted the imported global-attention 3D network to supervised Thebe crops without denoising pretraining.

| Attempt | Recorded epochs | Best epoch | Best crop-validation Dice | Status |
|---|---:|---:|---:|---|
| Smoke | 1 | 1 | 0.005776 | Completed smoke |
| FP16 | 77 | 70 | **0.539004** | Incomplete; later non-finite losses |
| BF16 | 65 | 61 | 0.309747 | Incomplete; stop cause not recorded |

These are crop-validation results. There is no full-survey validation or test result.

## 1. Why three folders belong together

| Folder | Role |
|---|---|
| [smoke](../runs/paper_attention3d_thebe_smoke_20261009_170246) | One-epoch pipeline check |
| [FP16](../runs/paper_attention3d_thebe_supervised_seed42) | Main original-precision attempt |
| [BF16](../runs/paper_attention3d_thebe_supervised_seed42_bf16_clean) | Numerical-stability revision |

All three test the same imported architecture and supervised crop task.

## 2. Data and pipeline

- Training source: nine Thebe training HDF5 blocks.
- Validation source: two Thebe validation blocks.
- Patch size: 64³.
- Main training budget: 64 random patches per epoch.
- Validation: 32 fixed patches.
- Half of training indices require at least one labelled fault; the rest sample usable patches.
- No test file was read.

Pipeline:

64³ HDF5 crop → local trace-envelope mask → valid-only z-score → tensor without the R100 axis reversal → global Attention3D model → sigmoid → threshold 0.5 → pooled crop metrics.

Because this pipeline uses 64³ selected crops and a different mask/orientation, its Dice should not be directly compared with full-survey R100 Dice.

## 3. Model

The imported Attention3D U-Net has **45,001,057 parameters**.

- Feature widths: 176, 336, and 680.
- Five convolution blocks contain global attention.
- Each attention block has eight heads.
- Downsampling uses stride-2 convolution.
- Upsampling uses transposed convolution.
- GroupNorm and LayerNorm are used.

Global attention lets every feature location exchange information with all other locations in the crop.

Source: [fault-detection-global-attention.py](../external/attention3d_paper/fault-detection-global-attention.py#L497).

## 4. Training method

Both main attempts use:

- random initialization;
- AdamW, peak learning rate 0.0005;
- weight decay 0.0001;
- batch 1, gradient accumulation 4;
- Unified Focal Loss;
- seed 42;
- no denoising pretraining.

Unified Focal Loss is:

0.5 × focal Tversky loss + 0.5 × focal BCE

Tversky gives false negatives weight 0.7 and false positives weight 0.3. Focal terms give more weight to harder mistakes.

FP16 uses GradScaler. BF16 disables gradient scaling, calculates the loss in FP32, and explicitly stops on non-finite inputs, logits, loss, or gradient norm.

## 5. Results

Best saved checkpoint rows:

| Attempt | Train loss | Validation loss | Dice | Precision | Recall |
|---|---:|---:|---:|---:|---:|
| Smoke, epoch 1 | 0.503052 | 0.493502 | 0.005776 | 0.030397 | 0.003191 |
| FP16, epoch 70 | 0.408099 | 0.431831 | **0.539004** | 0.548685 | 0.529659 |
| BF16, epoch 61 | 0.419863 | 0.420612 | 0.309747 | 0.299325 | 0.320921 |

The validation fault prevalence recorded by both main histories is 0.0260174.

FP16 recorded 77 epoch rows. Training loss became non-finite in three rows and validation loss in four rows, beginning late in the run. The best epoch-70 checkpoint occurs before those failures and its saved weights are finite.

BF16 recorded 65 complete rows and finite losses. The log stops during the following epoch, and no completion/status artifact explains why. It must be reported as incomplete.

## 6. What is not available

The wrapper saved only crop loss, Dice, precision, recall, prevalence, learning rate, and elapsed time. It did not save:

- IoU;
- PR-AUC or ROC-AUC;
- full-volume confusion counts;
- a calibrated threshold;
- full-survey validation;
- held-out test metrics.

Those values are not reconstructed or guessed.

## 7. Interpretation

The FP16 attempt reached the higher saved crop Dice, but later numerical failure makes the overall run incomplete. The BF16 revision remained finite in its saved rows but also did not finish.

The two trajectories do not isolate the effect of numerical precision because their termination behaviour differs. Neither result is evidence of a completed paper reproduction.

## 8. Evidence

- Imported architecture/loss: [paper source](../external/attention3d_paper/fault-detection-global-attention.py)
- FP16 wrapper: [train_paper_attention3d_thebe.py](../scripts/train_paper_attention3d_thebe.py)
- BF16 wrapper: [train_paper_attention3d_thebe_bf16.py](../scripts/train_paper_attention3d_thebe_bf16.py)
- FP16 history: [history.csv](../runs/paper_attention3d_thebe_supervised_seed42/history.csv)
- BF16 history: [history.csv](../runs/paper_attention3d_thebe_supervised_seed42_bf16_clean/history.csv)
- Smoke status: [status.json](../runs/paper_attention3d_thebe_smoke_20261009_170246/status.json)

## 9. Simple definitions and calculation

| Term | Meaning |
|---|---|
| Global attention | Every crop location can use information from every other location. |
| Attention head | One parallel set of attention relationships. This model uses eight. |
| AdamW | Optimizer that includes separated weight decay. |
| Weight decay | Regularization that discourages large weights. |
| Non-finite | NaN or positive/negative infinity; invalid as an ordinary loss. |
| FP16 / BF16 | Two 16-bit number formats with different precision and numerical range. |
| Crop Dice | Dice on selected patches, not necessarily an entire survey. |

Using the best FP16 precision and recall:

2×0.548685×0.529659 / (0.548685+0.529659) = **0.539004**

