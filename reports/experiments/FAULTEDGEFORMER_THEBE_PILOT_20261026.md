# FaultEdgeFormer-inspired Thebe architecture pilot

**Started:** 2026-10-26  
**Status:** completed; budget-matched pilot favors FaultEdgeFormer-inspired  
**Primary reference:** [FaultEdgeFormer (Journal of Geophysics and Engineering)](https://doi.org/10.1093/jge/gxag041)

## Question

Does replacing the R100 3D U-Net with a compact edge-aware, multiresolution
window-attention model improve fault segmentation when the data, labels,
normalization, mask, loss, optimizer, sampling seed, and checkpoint-selection
principle remain controlled?

This is an **architecture control**, not an exact FaultEdgeFormer reproduction.
The article describes the defining blocks but no author implementation was found.
Channel widths, normalization around the stem and fusion layers, and exact Sobel
coefficient scaling therefore had to be stated and inferred.

## Why this candidate

FaultEdgeFormer is the cleanest first comparison among the reviewed recent
architectures because its reported size (1.34 million trainable parameters) is
close to R100/FaultSeg3D (1.46 million). It can train from scratch on the same
Thebe supervision and does not introduce external pretraining, pseudo-labels,
or a new data split. This makes an observed difference easier to attribute to
the architecture.

The implementation contains the paper's defining ideas:

- nine trainable 3D Sobel directions at the input;
- local 3D attention with convolutional Q/K/V projections;
- alternating regular and shifted windows, window size 7;
- a depthwise `3x3x3` convolution inside each transformer MLP;
- three parallel resolutions with repeated cross-scale fusion; and
- attention heads `[1, 2, 4]`.

The resulting model has **1,389,697 parameters**, 3.7% above the paper's
reported 1.34 million and slightly below R100's 1,459,585.

## Controlled protocol

| Item | Setting |
|---|---|
| Train data | `train1.h5` through `train9.h5`; combined shape `900 x 3174 x 1537` |
| Validation data | `val1.h5`, `val2.h5`; combined shape `200 x 3174 x 1537` |
| Test policy | test files are never opened |
| Input | `128^3`, per-patch observed-voxel z-score, original axis reversal |
| Invalid samples | raw seismic zero/nonfinite mask retained in loss and metrics |
| Loss | ordinary masked binary cross-entropy |
| Optimizer | Adam, learning rate `1e-4` |
| Precision | FP16 autocast with gradient scaling |
| Accumulation | 2 patches per optimizer update |
| Augmentation | random axis-0 flip, matching R100 |
| Seed | 42; validation-coordinate seed 1042 |
| Checkpoint | maximum approximate PR-AUC on a fixed validation subset |

## Verification completed before launch

- Static preflight confirmed the exact 9/2 train-validation file layout and
  combined array dimensions.
- Three CPU invariants passed: zero-sum/trainable Sobel filters; exact window
  partition reversal; and finite gradients through shifted padded windows.
- A real GPU end-to-end smoke run completed in 22 seconds: 18 training patches,
  two validation patches, checkpoints, threshold selection, and JSON status.
- Smoke peak allocation was 3.73 GiB on the RTX A5500.
- The smoke status records `test_files_read: false`.
- cuBLAS deterministic workspace configuration is enabled. PyTorch reports that
  trilinear-upsample backward and CUDA histogram binning have no deterministic
  kernels; this limitation is recorded rather than hidden.

## Completed screening run

The first gate is deliberately smaller than a publishable comparison:

- 10 epochs;
- 90 training patches per epoch (900 total);
- 32 fixed validation patches each epoch;
- checkpoint selection on the same 32 fixed validation patches for both models;
- final calibrated metrics on the complete 650-tile validation set for both.

The R100 control was freshly trained with the same seed, crop stream, optimizer,
loss, 10 epochs, and 90 patches per epoch. This avoids comparing the pilot with
R100's already mature 100-epoch model.

| 900-patch result (seed 42) | FaultEdgeFormer-inspired | R100 | Ratio (FaultEdgeFormer / R100) |
|---|---:|---:|---:|
| Complete-validation Dice | **0.20057** | 0.06869 | **2.92x** |
| Complete-validation PR-AUC | **0.11639** | 0.03480 | **3.34x** |
| Complete-validation ROC-AUC | **0.81556** | 0.59300 | 1.38x |
| Training plus checkpoint validation | 1,027.3 s | 507.9 s | 2.02x slower |
| Complete-validation inference | 86.6 s | 7.46 s | 11.61x slower |
| Peak allocated GPU memory | 3.73 GiB | 1.25 GiB | 2.99x |
| Trainable parameters | 1,389,697 | 1,459,585 | 0.95x |

Both checkpoints were selected at epoch 10. FaultEdgeFormer's selected
full-validation threshold was `0.06543`; R100's was `0.01904`. Test data were
never opened. The result is strong evidence that the edge-aware attention model
learns useful fault rankings earlier under this protocol. It does not establish
superiority after convergence because it is one seed and only 2.5% of the final
R100 training budget.

Run directory:
`runs/faultedgeformer_thebe_pilot_seed42_20261026`

Log:
`reports/training/faultedgeformer_thebe_pilot_seed42_20261026.log`

Matched R100 directory:
`runs/r100_thebe_matched900_seed42_20261026`

FaultEdgeFormer complete-validation result:
`runs/faultedgeformer_thebe_pilot_seed42_20261026/complete_validation.json`

## Existing reference

R100 seed 42 reached full-validation Dice **0.5441** and approximate PR-AUC
**0.5521** after its full 100-epoch budget. These are reference values for the
next 100-epoch FaultEdgeFormer run, not targets that this short pilot was
expected to meet. A full seed-42 run is justified by the pilot. At measured
throughput, 100 epochs x 360 patches should take approximately 11.4 hours.

## Promoted full run

The full validation-only seed-42 run was launched after the matched pilot
passed. It uses the original R100 budget: 100 epochs, 360 training patches per
epoch, 128 fixed checkpoint-validation patches per epoch, and complete
validation after selecting the best checkpoint. The test split remains disabled.

- Session: `tmux attach -t faultedgeformer_full`
- Run: `runs/faultedgeformer_thebe_full_seed42_20261026`
- Log: `reports/training/faultedgeformer_thebe_full_seed42_20261026.log`

## Files

- `scripts/faultedgeformer_model.py`
- `scripts/train_faultedgeformer_thebe.py`
- `scripts/evaluate_faultedgeformer_validation.py`
- `tests/test_faultedgeformer_model.py`
- `runs/faultedgeformer_thebe_smoke_v2_20261026/status.json`
- `runs/faultedgeformer_thebe_pilot_seed42_20261026/status.json`
- `runs/r100_thebe_matched900_seed42_20261026/status.json`
