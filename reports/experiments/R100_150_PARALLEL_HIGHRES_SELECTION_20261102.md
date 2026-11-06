# R100-150 parallel experiment: matched high-resolution FaultSegV3 control

Date: 2026-11-02  
Status: R100, FaultSegV3, and SwinUNETR 150-epoch jobs launched on GPU 0; test data remain closed

The fairness distinction between matched architecture controls and model-native tuned capability, plus the topology, 2.5D, and GeoFWI3D execution plans, is documented in `reports/experiments/FAIR_TRAINING_AND_NEXT_BRANCHES_20261102.md`.

## Decision

Run the 150-epoch R100 extension and a randomly initialized FaultSegV3 architecture control concurrently, with the same seed and Thebe training recipe.

This is a test of one specific hypothesis: **the current R100 pipeline loses thin-fault position and nearby-fault separation because its encoder compresses a 128-cube three times, while its nearest-neighbor decoder cannot fully recover the missing detail.** FaultSegV3 preserves a full-resolution stream and downsamples its main path once. It therefore changes the factor implicated by the visual errors while holding the data and optimization protocol fixed.

The second run is not a reproduction of the FaultSegV3 manuscript and does not use its released weights. It is a local architecture ablation on Thebe.

## Evidence from the frozen R100 test review

The frozen three-seed R100 test ensemble reached Dice 0.581257 and PR-AUC 0.620308. The visual review used its already frozen threshold of 0.274902 and did not tune anything on test.

The selected sections show two recurring errors:

1. **Boundary displacement and thickness:** predictions often cover the correct structure but spread around, or shift away from, the one-voxel reference. In the middle displayed section there are 800 false-positive and 544 false-negative pixels around 1,625 positive reference pixels.
2. **Weak or adjacent structures disappear:** the difficult slab has patch Dice 0.2904, while the other fixed slabs reach 0.5318 and 0.6451. This is a spatially uneven failure, rather than a uniform inability to recognize faults.
3. **The 100-epoch cutoff is active:** the five seed-specific best epochs were 95, 93, 95, 94, and 89. Three runs peaked within five epochs of the cutoff, so 150 epochs is a justified saturation check.

These observations do not prove that compression is the cause. The matched FaultSegV3 run is designed to test that causal claim.

Evidence and images:

- `reports/evaluation/r100_test_visuals_20261102/casebook.png`
- `reports/evaluation/r100_test_visuals_20261102/seed43_casebook.png`
- `reports/evaluation/r100_test_visuals_20261102/test_summary.png`
- `reports/evaluation/r100_test_visuals_20261102/manifest.json`

## Alternatives considered

Paper metrics below are context only. OIS/ODS, tolerance IoU, Dice, data splits, pretraining, and label thickness are not interchangeable; none is treated as a direct numerical comparison with the local frozen test.

| Candidate | Factor it tests | Evidence and fit to the observed gap | Confounding factors / readiness | Decision |
|---|---|---|---|---|
| **FaultSegV3, matched from scratch** | Retaining full-resolution local discontinuities and limiting spatial compression | The public model has 0.563M parameters and one main-path downsampling stage. Its stated design premise is that local terminations and offsets can matter more than model size. This directly matches R100's displaced, thick, and missed-neighbor errors. | The upstream training recipe and synthetic data differ, so this run deliberately retains the R100 recipe and changes only the network. Local preflight and one-epoch smoke test passed. | **Run now. Cleanest and cheapest causal test.** |
| **Plain SwinUNETR** | Windowed attention and broader learned context | Official MONAI implementation passed a local 128-cube training preflight at 15.7M parameters and 6.09 GiB. | It changes capacity, tokenization, downsampling, and attention together. On the same Thebe literature table, plain SwinUNETR trails the hybrid/topology variants. It is therefore a context control rather than a direct repair of the observed resolution error. | **Added as a third matched 150-epoch run at the user's request.** Interpret separately from the cleaner V3 resolution test. |
| **FaultSeg Swin-UNETR / SimMIM** | Seismic self-supervised pretraining plus Swin and multi-scale decoding | Published specifically for Thebe and improves over plain Swin in the reported OIS/ODS protocol. | Architecture, decoder, pretraining corpus, and schedule change together. A reproduction requires the exact pretraining pipeline and is not a one-factor parallel control. | High-priority reproduction after the local architecture ablation. |
| **TopSUMseg** | Local detail, long-range continuity, global-local attention, and topology-aware structural loss | The 2026 study reports Thebe OIS/ODS 0.879/0.875 from scratch. Its visual analysis targets fragmentation and noise. Ablation shows that global-local attention and structural supervision add value beyond the base encoder; its pure Swin sequence is weaker than the hybrid sequence. | The reported run uses four A100 GPUs, several coupled components, and no verified official implementation was found. A fresh reimplementation would not be a clean quick control. | Use as the design map: local detail first, then continuity loss/context. Do not claim reproduction yet. |
| **Distance Transform Loss (DTL)** | Boundary placement | Public 2025 code and package explicitly penalize predictions more strongly as their boundary moves farther from the target. This fits the shifted/thick R100 bands. | Published experiments are semantic segmentation on F3, Parihaka, and Penobscot; adapting its 2D/multiclass boundary construction to binary 3D thin surfaces is new work and adds a loss factor. | Most logical next loss ablation if high resolution improves overlap but boundaries remain thick. |
| **Topology/geology-informed losses** | Continuity, curvature, dip smoothness, branch suppression | The 2025 TGRS work combines Allen-Cahn, persistent homology, total variation, dip, connectivity, and branch priors. It directly addresses broken or geologically implausible surfaces. | Several penalties and hyperparameters move together; persistent homology is computationally heavier. | Defer until the simpler architecture and boundary-loss ablations identify the remaining error. |
| **UMamba3D / hybrid Swin-Mamba** | Long-range continuity plus local structure | 2026 papers report better continuity/noise suppression than U-Net and emphasize loss of high-frequency structure in standard encoders. | Current UMamba3D source/model availability is by request; TopSUMseg code is unverified. Both are multi-factor reimplementations. | Keep as the long-context branch of the experiment tree. |
| **2.5D SAM / Fault-SAM / SeisSAM-3D** | Foundation features, slice context, prompting, cross-domain transfer | Visual results make continuity and cross-domain behavior inspectable and may be valuable for interactive interpretation. | Prompting, natural-image pretraining, 2D-to-3D reconstruction, and different evaluation protocols obscure the cause of a gain. Reproduction assets vary by paper. | Evaluate later as an interactive/cross-domain track, not the immediate R100 repair. |
| **GeoFWI3D fault-only vs fault+RGT pretraining** | Whether depositional-coordinate supervision creates representations that transfer to field faults | The new open dataset contains 10,000 co-registered 96-cube models with reflectivity, fault masks, and relative geological time. It enables the proposed joint experiment cleanly. | It tests synthetic-to-field transfer and geological pretraining, while the immediate evidence is an in-domain spatial-precision gap. It needs dataset download, a pretraining head, and a separate fine-tuning matrix. | **Approved as the next new-data experiment**, after the matched architecture result chooses the encoder to pretrain. Compare no pretraining, fault-only, and fault+RGT with identical Thebe fine-tuning. |
| **nnU-Net** | A strong automatically configured training system | Useful systems baseline and may discover a better patch/normalization/schedule recipe. | It changes architecture, loss, sampling, augmentation, and inference at once. A win would not identify what should be added to the current pipeline. | Run after factor-level experiments as an upper-bound systems baseline. |

## Why this is more informative than another model race

The local FaultEdgeFormer-inspired seed-42 run already suggests that retaining edge and high-resolution information can help: its frozen test Dice was 0.574603 versus 0.524797 for R100 seed 42. That comparison changes several model details, so it is supporting evidence rather than proof.

The new pair is stricter:

| Controlled item | R100-150 | FaultSegV3 matched-150 |
|---|---:|---:|
| Thebe training/validation split | same | same |
| Random seed | 43 | 43 |
| Training patches per epoch | 360 | 360 |
| Epochs | 150 | 150 |
| Crop size | 128 x 128 x 128 | 128 x 128 x 128 |
| Validity mask and per-patch z-score | same | same |
| Augmentation | same axis-0 flip | same axis-0 flip |
| Objective | masked BCE | masked BCE |
| Optimizer and learning rate | Adam, 1e-4 | Adam, 1e-4 |
| Gradient accumulation | 2 | 2 |
| Checkpoint selection | fixed-validation-subset PR-AUC | fixed-validation-subset PR-AUC |
| Trainable parameters | 1,459,585 | 562,625 |
| Main-path downsampling | 3 stages | 1 stage plus full-resolution branch |
| Initialization | random | random; released V3 checkpoint not loaded |

The crop sequence is identical because the data loader, seed, and trainer are shared. Drop path is disabled in V3 so regularization is not a second changing factor.

## Running jobs

Launched at 2026-11-02 05:19:51 UTC on the same NVIDIA RTX A5500 (24,564 MiB):

| Run | PID at launch | Log | Initial status |
|---|---:|---|---|
| `r100_150_seed43_20261102` | 4131776 | `reports/training/r100_150_seed43_20261102.log` | epoch 1 complete: subset PR-AUC 0.032889, 3.64 min |
| `faultsegv3_matched_150_seed43_20261102` | 4131777 | `reports/training/faultsegv3_matched_150_seed43_20261102.log` | epoch 1 complete: subset PR-AUC 0.031992, 5.17 min |
| `swinunetr_matched_150_seed43_20261102` | 156201 | `reports/training/swinunetr_matched_150_seed43_20261102.log` | epoch 1 complete: subset PR-AUC 0.036825, 6.93 min |

After startup, both processes were live and combined GPU memory use was 4,760 MiB. The earlier separate memory measurements were 1.25 GiB peak allocation for R100 and 2.18 GiB for V3, leaving ample capacity. Shared-GPU execution may lengthen wall time but should not alter the step budget.

The epoch-1 metrics are startup evidence only and are too early to compare. At the observed concurrent speed, the training loops are approximately 9.1 hours for R100 and 12.9 hours for V3, followed by each run's full-validation sweep.

The V3 smoke run completed one short epoch before the full launch and used 2.18 GiB peak allocated memory. Its metric is intentionally ignored because it used only 18 patches.

The matched MONAI SwinUNETR smoke run also completed 18 patches with float16 masked BCE and Adam, using 6.22 GiB peak allocated and 8.92 GiB peak reserved memory. Its metric is likewise ignored. With all three full jobs active, process-level GPU use was approximately 1.78 GiB for R100, 2.68 GiB for V3, and 8.12 GiB for SwinUNETR, within the 24.56 GiB device capacity. The third job increases compute contention and therefore wall time for all runs.

## Evaluation rule fixed before results

1. Select each checkpoint only by the existing fixed validation subset PR-AUC rule.
2. At completion, compare full-validation pooled Dice, PR-AUC, precision, recall, selected threshold, runtime, and peak memory.
3. Generate side-by-side fixed validation sections with seismic, reference, probability, thresholded prediction, false positives, and false negatives. Inspect fault thickness/offset, adjacent-surface separation, continuity, and noise.
4. Do not choose architecture or threshold from test. Open test only after the comparison decision is frozen, then use the same predefined full-volume tiling and report both aggregate and patch distributions.
5. Treat one seed as exploratory. Promote V3 to seeds 42 and 44 only if it improves both full-validation Dice and PR-AUC over the matched R100-150 run, or if a small aggregate change is accompanied by a clear reduction in displacement/thickness errors without a continuity regression.
6. Reject the hypothesis if V3 does not improve spatial errors under the matched recipe. Do not rescue it by silently adding pretraining, Dice loss, or augmentation; those become separately named experiments.

The side-by-side validation renderer is already queued (updated three-model watcher PID 164705 at launch). It will wait for R100, FaultSegV3, and SwinUNETR; choose cases from the shared fixed validation subset using reference labels only; render `reports/evaluation/r100150_vs_faultsegv3_validation_20261102/validation_casebook.png`; and keep test files closed.

## What to add next, conditional on this result

1. **V3 improves position/separation:** add a limited-downsampling/full-resolution branch to the main pipeline, then repeat across three seeds. Use the winning encoder for GeoFWI3D pretraining.
2. **Overlap improves but surfaces remain thick or shifted:** add a 3D binary boundary-distance auxiliary loss, first in a small coefficient sweep fixed on validation.
3. **Local accuracy improves but faults remain fragmented:** add one continuity mechanism at a time: a topology/structure loss first, then a long-context Mamba/Swin stage if needed.
4. **V3 does not improve:** retain R100 and test context rather than resolution, beginning with the already preflighted SwinUNETR and then a hybrid encoder if plain Swin fails.
5. **In-domain performance becomes good but field transfer remains weak:** run the GeoFWI3D three-arm experiment: no pretraining, fault-only pretraining, and fault+RGT multitask pretraining, followed by identical Thebe fine-tuning and an external-survey check.

This order turns each result into a pipeline decision. It also prevents a paper's attractive visualization or headline score from being mistaken for evidence under a different label tolerance, split, or pretraining regime.

## Primary sources

- FaultSegV3 repository and manuscript assets: https://github.com/douyimin/FaultSegV3
- TopSUMseg (2026): https://journals.sagepub.com/doi/full/10.3233/FAIA250865
- Distance Transform Loss (2025): https://www.sciencedirect.com/science/article/pii/S0098300425002110
- DTL implementation: https://github.com/rafaelvareto/segmentation-loss
- Physics/topology/geology-informed fault segmentation (2025): https://doi.org/10.1109/TGRS.2025.3623694
- FaultSeg Swin-UNETR: https://arxiv.org/abs/2310.17974
- GeoFWI3D paper: https://arxiv.org/abs/2610.01033
- GeoFWI3D code: https://github.com/aaspip/geofwi3d
- GeoFWI3D dataset record: https://zenodo.org/records/20148778
- Structure-constrained UMamba3D (2026): https://www.frontiersin.org/journals/earth-science/articles/10.3389/feart.2026.1930523/full
- Fault-SAM (2026): https://www.sciencedirect.com/science/article/pii/S0950705126019118
- Seismic Fault SAM / 2.5D comparison supplied by the user: https://arxiv.org/html/2407.14121v1
- Large-scale seismic fault benchmark and domain-shift study: https://arxiv.org/abs/2505.08585
- Benchmark code: https://github.com/olivesgatech/large-bench-geo
