# Attention3D Opunake + Kahu execution record

**Started:** 2026-10-26 (Asia/Baku)  
**Protocol:** `attention3d_opunake_kahu_two_survey_reproduction_variant_v1`

## Scope and claim

This run is a two-survey reproduction variant of Mahzad and Bagheri's
Attention3D fault-detection method. It uses verified Opunake-3D and Kahu-3D
post-stack PSTM volumes. Kerry-3D is absent because the historical
approximately 1 GB `Kerry3D.segy` object could not be matched unambiguously to
a current NZP&M resource.

The experiment must not be described as an exact reproduction of the paper's
three-survey pretraining corpus. The public release also omits the authors'
pretraining crop bounds, sampler, optimizer implementation, and compatible
pretraining entry point. Every local decision below is therefore frozen and
reported.

## Verified inputs

| Survey | Logical shape `(inline, crossline, time)` | Present traces | Missing envelope bins | Source SHA-256 |
|---|---:|---:|---:|---|
| Opunake | 765 × 2233 × 1501 | 1,662,034 | 46,211 | `931bbbb5f2ec50f3eb6f8d65dd1352c982ef842ed103f7427af1ea73c43364ba` |
| Kahu | 599 × 1697 × 1500 | 994,230 | 22,273 | `079826f39ea6e29b34accd4342e1d2e7fb5fea079a7dc06a74b1d3a4d525b225` |

The streaming converter decoded 3,986,058,034 finite field-amplitude samples.
The dense arrays remain raw `float32`; missing acquisition bins are zero-filled
and separately masked. Verification compared 32 random converted traces per
survey byte-for-value with the decoded source SEG-Y traces, checked sampled
missing bins, and read 16 complete cubes per survey. All checks passed.

Artifacts:

- frozen data configuration: `configs/attention3d_two_survey_pretrain.json`;
- conversion manifest: `data/processed/attention3d_nzpam/manifest.json`;
- verification: `reports/data_audit/attention3d_two_survey_conversion_verification_20261026.json`;
- converter: `scripts/prepare_attention3d_field_surveys.py`.

## Patch protocol

The paper's 64 × 64 × 64 sub-volumes and 50% overlap are retained, giving
stride 32 in all three axes. A patch is eligible only if every trace in its
64 × 64 spatial footprint exists. Terminal windows that are not aligned to the
published stride are not added.

| Survey | Eligible train cubes | Spatially held-out validation cubes |
|---|---:|---:|
| Opunake | 51,255 | 6,030 |
| Kahu | 30,420 | 3,780 |
| **Total** | **81,675** | **9,810** |

Training and pretext validation use disjoint contiguous inline regions with a
32-voxel gap. This is a local leakage-control choice because the authors did
not publish a pretext validation manifest.

## Frozen pretraining execution

The released README specifies 50 epochs, batch size 4, learning rate `1e-3`,
and `model_epoch_49.pt`. The fault-detection paper states an effective batch of
16 consistent with pretraining. The single-GPU adaptation uses physical batch
1 and 16-step gradient accumulation.

The complete converted corpus contains 81,675 eligible training cubes. Fifty
exhaustive passes would require 4,083,750 model evaluations, which would take
well over a year at measured RTX A5500 throughput. The authors' crop bounds and
pretraining batches per epoch are not published. The local schedule therefore
freezes 352 cubes per epoch for 50 epochs: 17,600 unique cubes total, balanced
as 8,800 Opunake and 8,800 Kahu cubes. This is a declared compute adaptation,
not an author setting.

For each cube:

1. apply the survey-wide z-score computed over finite samples on present
   traces;
2. sample Gaussian-noise standard deviation uniformly from 5% to 30% of the
   normalized cube RMS;
3. reconstruct the uncorrupted normalized field cube with mean squared error.

The model is the released 45,001,057-parameter segmentation
`Attention3DUNet`, used for both stages so every feature tensor is transferable;
the segmentation output head will be reinitialized. This differs from the
separate public denoising repository's incompatible four-level network.

Single-GPU numerical choices are BF16 forward, FP32 loss/parameters/AdamW,
weight decay `1e-4`, gradient clipping at 1.0, and no scheduler because a
pretraining scheduler is not published.

The coordinate schedule is immutable within the run:

- training schedule SHA-256: `988d96a6ffe0ff80e56e0cb921cbde21f6cc9fd66b81c21001eb35685b379d6c`;
- validation schedule SHA-256: `373b5c1bf15a85e99423183022acc53633c1aa8245127e0a69c9d140fd55726a`.

## Preflight and execution state

The real-data GPU preflight passed with finite outputs, losses, gradients, and
parameter updates. Peak memory was 5,502,567,424 allocated bytes and
6,213,861,376 reserved bytes on the RTX A5500. Before training, the untrained
network's four-patch MSE was 3.9281 versus 0.1320 for the noisy-input identity
baseline. Beating that identity baseline on the fixed validation schedule is a
required denoising sanity check, not a guaranteed outcome.

At the user's direction, the full pretraining run started concurrently with
the FaultEdgeFormer experiment in persistent tmux session
`attention3d_pretrain`. Both processes share the single RTX A5500. At startup,
FaultEdgeFormer occupied approximately 4.7 GB and Attention3D approximately
5.9 GB, leaving about 13.3 GB free; aggregate GPU utilization reached 100%.
This has sufficient measured memory but slows both runs and makes their wall
times unsuitable for uncontended throughput comparison.

The resumable pretraining run is at:

`runs/attention3d_two_survey_pretext_seed42_20261026`

The queue log is:

`reports/training/attention3d_two_survey_pretext_seed42_20261026.log`

The uncontended preflight took approximately 11–12 seconds per training cube.
The 55–60 GPU-hour estimate for 17,600 training cubes plus validation will
increase while FaultEdgeFormer shares the device.

## Gate before supervised fine-tuning

Use the minimum fixed-validation-MSE checkpoint. Continue to Thebe transfer
only after confirming finite training, correct schedule hashes, complete
checkpoint provenance, and improvement over the noisy-input identity MSE.
Fine-tuning must keep the held-out Thebe test region unopened until model,
checkpoint, stopping epoch, and threshold are frozen.

## Completed downstream linear-probe test — 28 October 2026

The pretraining run completed all 50 epochs. Its best checkpoint was epoch 50
with fixed-validation MSE `0.00986143`, compared with `0.03193139` for leaving
the noisy input unchanged. The checkpoint therefore passed the denoising gate.

The checkpoint is not a semantic fault detector: its output head reconstructs
seismic amplitude. A downstream representation test transferred all 78 feature
tensors exactly, reinitialized the two output-head tensors, froze the
45,000,880 feature parameters, and trained only the 177-parameter output
convolution on 256 labelled Thebe training patches.

Checkpoint selection and threshold search used one fixed 128-patch Thebe
validation sample. The checkpoint, threshold `0.2060546875`, and 256-patch
test-coordinate schedule were frozen before any test HDF5 dataset was opened.
The held-out sample spans all seven Thebe test blocks.

| Metric | Validation | Held-out Thebe sample |
|---|---:|---:|
| Dice | 0.073137 | 0.054170 |
| IoU | 0.037956 | 0.027839 |
| Precision | 0.038109 | 0.027906 |
| Recall | 0.904461 | 0.920793 |
| Specificity | 0.099446 | 0.095586 |
| Balanced accuracy | 0.501954 | 0.508189 |
| MCC | 0.002497 | 0.009117 |
| PR-AUC, 2,048-bin approximation | 0.039540 | 0.027396 |
| ROC-AUC, 2,048-bin approximation | 0.503032 | 0.509454 |

The test pooled 32,733,012 valid voxels from 175 observed cubes. The model
predicted faults very broadly: it obtained high recall but 2.79% precision and
28,792,349 false-positive voxels. ROC-AUC near 0.5 and MCC near zero show that
the frozen denoising representation was not linearly sufficient for Thebe
fault segmentation under this protocol.

This is a fixed-budget linear-probe result, not a full-network fine-tuning
result and not a full-survey score. It does not establish that full Attention3D
fine-tuning will fail. It does establish that denoising success alone cannot be
presented as fault-detection performance.

Evidence:

- `runs/attention3d_opunake_kahu_linear_probe_thebe_seed42_20261028/result.json`;
- `runs/attention3d_opunake_kahu_linear_probe_thebe_seed42_20261028/FROZEN_BEFORE_TEST.json`;
- `runs/attention3d_opunake_kahu_linear_probe_thebe_seed42_20261028/test_patch_manifest.json`;
- `runs/attention3d_opunake_kahu_linear_probe_thebe_seed42_20261028/histograms_2048_bins.npz`.
