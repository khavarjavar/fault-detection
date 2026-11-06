# Fair training protocol and next experiment branches

Date: 2026-11-02  
Test policy: validation-only development; test remains closed

## The fairness correction

Using the same data, seed, loss, optimizer, learning rate, augmentation, and epoch budget for every architecture is good experimental design for one question:

> Does the architecture itself improve results under the current R100 pipeline?

It is not a fair answer to a different question:

> How well can each model perform when trained with a suitable recipe?

The current seed-43 R100, FaultSegV3, and SwinUNETR runs belong to the first category. They are controlled architecture ablations. Their rankings must not be presented as the maximum capability of V3 or Swin.

The study will therefore report three separate tracks:

| Track | What remains equal | What may change | Valid claim |
|---|---|---|---|
| **A. Matched architecture control** | Split, crop sequence, seed, BCE, Adam, LR, augmentation, steps, checkpoint rule, evaluator | Architecture only | Which architecture helps the existing pipeline? |
| **B. Equal-search-budget capability** | Split, evaluator, maximum trials per model, screening epochs, promotion rule, final seeds, no test access | Model-appropriate loss, optimizer, schedule, regularization, augmentation | Which model performs best after the same tuning opportunity? |
| **C. Published-system reproduction** | The paper's documented protocol as far as assets allow | Pretraining, model-specific decoder, augmentation, epochs and metric | Can the reported system be reproduced? This is not an architecture-only comparison. |

The tables for A, B, and C must remain separate. A model can lose Track A and win Track B without contradiction.

## Why the current recipe can understate V3 and Swin

The local upstream FaultSegV3 source uses MaskDice, AdamW, cosine step decay, bfloat16 mixed precision, drop path 0.1, EMA, multiscale batch shapes, transpose plus GPU augmentations, and optionally released synthetic weights. The matched local V3 run instead uses BCE, Adam, constant 1e-4, float16, one fixed crop size, a single flip, no EMA, no drop path, and random initialization. That is deliberate for Track A but is not V3's native recipe.

FaultSeg Swin-UNETR uses AdamW, cosine annealing, self-supervised SimMIM pretraining, and multiscale/dilated supervision. The current MONAI SwinUNETR run is a plain randomly initialized architecture with R100 BCE and Adam. It tests context under the existing pipeline and is not a reproduction of FaultSeg Swin-UNETR. [FaultSeg Swin-UNETR paper](https://www.mdpi.com/2072-4292/16/5/922).

## Track B: equal tuning opportunity

Use validation only and give every architecture the same search budget. Search within each architecture; do not rank architectures from short pilots because convergence rates differ.

### Stage B1: recipe screening within each model

Allow at most three named recipes per architecture. Each receives the same number of training patches and the same 30-epoch screening budget. Select one recipe per architecture using a preregistered combination of full-validation PR-AUC and Dice, with fixed qualitative validation sections used only as a structural check.

| Model | Already running | Model-appropriate candidates to screen |
|---|---|---|
| R100 | BCE + Adam + constant LR | BCE+soft-Dice with AdamW+cosine; boundary-aware BCE/Dice with AdamW+cosine |
| FaultSegV3 | BCE + Adam + constant LR | upstream MaskDice + AdamW+cosine+drop path+EMA; BCE+soft-Dice + AdamW+cosine; released-weight fine-tuning is recorded separately as transfer |
| SwinUNETR | BCE + Adam + constant LR | DiceCE/BCE+Dice + AdamW+cosine; the same with stronger geometric augmentation; seismic self-supervised pretraining is a separate Track C arm |

The released V3 checkpoint and any pretrained Swin/SAM weights are not mixed into the random-initialization recipe search. Pretraining changes the information available to the model and receives its own label.

### Stage B2: full training

Promote the best validation recipe for each architecture to the full 150-epoch budget. Run seeds 42, 43, and 44 for promoted recipes. Freeze thresholds on complete validation, compare mean and seed variance, and open test once after model and recipe selection are final.

This design gives each model appropriate training while controlling researcher effort and validation overfitting.

## Branch 1: structural and geological losses

The 2025 TGRS method combines an Allen-Cahn curvature prior, persistent-homology topology, and geological penalties for total variation, dip smoothness, local connectivity, and branch suppression. These are architecture-agnostic and relevant to fragmented predictions. [TGRS paper](https://ieeexplore.ieee.org/document/11208699/).

### Thebe topology audit

Before adopting a connected-surface prior, the shared fixed validation subset was audited using 26-neighbor 3D connected components. Test data were not read.

| Label-only result | Value |
|---|---:|
| Fixed validation patches | 128 |
| Fault-present patches | 38 |
| Median components, all sizes | 2 |
| Median components at least 32 voxels | 2 |
| Maximum substantial components | 6 |
| Patches with exactly one component at least 32 voxels | 47.4% |
| Median fraction in largest component | 97.6% |

The labels often contain one dominant surface plus one or more separate faults. A universal Betti-0=1 target would merge valid structures or penalize correct disconnected predictions.

### Safe loss order

1. **Boundary-distance auxiliary loss:** tests the observed thick and shifted bands. Use the public DTL formulation as a reference, adapted explicitly to binary 3D surfaces. [DTL paper](https://www.sciencedirect.com/science/article/pii/S0098300425002110), [code](https://github.com/rafaelvareto/segmentation-loss).
2. **Local continuity and dip loss:** penalize small gaps and implausible local orientation changes without requiring all faults to connect.
3. **Allen-Cahn/curvature regularization:** test sharpening and surface smoothness with a coefficient chosen only on validation.
4. **Persistent homology:** use label-derived Betti targets per patch or per connected region. Do not impose a fixed single-component target.
5. Add one term at a time to the same backbone and recipe. Only combine terms after each has shown an independent validation gain and an interpretable visual effect.

The cheapest initial backbone is R100, because loss behavior can be isolated quickly. Repeat a successful loss on the selected high-resolution/context architecture to measure interaction.

Audit artifact: `reports/evaluation/thebe_validation_topology_audit_20261102.json`  
Reproduction script: `scripts/audit_thebe_validation_topology.py`

## Branch 2: 2.5D Swin and SAM

The supplied Seismic Fault SAM paper stacks adjacent slices as channels and predicts the center slice. Its ablation reports five slices outperforming one, three, and seven after 100 epochs; its main comparison uses five slices and 300 epochs. It also shows that adapters and natural-image/SAM pretraining are large parts of the gain, so the result is not a 2.5D-only claim. [Seismic Fault SAM](https://arxiv.org/html/2407.14121v1).

Use the following staged comparison on the unchanged Thebe x split:

1. **Center-slice 2D Swin-T** with ImageNet weights.
2. **Five-slice 2.5D Swin-T**, predicting the center label. This isolates adjacent-slice context with the same encoder and training recipe.
3. **Five-slice SAM-B adapter**, freezing the foundation encoder and training adapters plus a full-resolution fault decoder. Begin with SAM-B rather than SAM-H to establish the pipeline at lower cost.
4. Add the paper's horizontal flip and affine/wave-propagation augmentation as a separate ablation.

Reconstruct validation probabilities into the full 3D grid and score them with the existing pooled valid-voxel Dice and PR-AUC. Also report paper-style OIS/ODS descriptively, without using them to replace the frozen local protocol. Keep edge slices and no-data masking explicit.

This sequence distinguishes the benefit of five-slice context from the benefit of foundation pretraining and adapters.

## Branch 3: GeoFWI3D fault plus RGT pretraining

GeoFWI3D contains 10,000 co-registered 96-cube models with p-reflectivity, fault indices, RGT, velocity, and salt information. The 96-cube dataset is 73.5 GB in ten compressed archives of about 7.3-7.4 GB each. [Dataset record](https://zenodo.org/records/20148778), [author code](https://github.com/aaspip/geofwi3d).

Only 17 GB is currently free on `/shared`. One archive plus all extracted modalities would exceed the safe working margin. Do not download the full dataset into the current filesystem.

### Storage-safe pilot

1. Fetch the small metadata/parameter table first and select 100-250 faulted, non-salt models from one archive.
2. Stream the archive and retain only `image3d.bin`, `fault3d.bin`, and `rgt3d.bin` for selected folders; do not store the tarball or velocity volumes.
3. Verify float32 shapes, hashes where provided, fault prevalence, RGT range/monotonicity, and image-label registration.
4. Keep a model-level train/validation split so crops from one geological model never cross splits.

### Three required pretraining arms

| Arm | Pretraining objective | Purpose |
|---|---|---|
| C0 | None | Random-initialization control |
| C1 | Binary fault segmentation from reflectivity | Tests ordinary supervised synthetic pretraining |
| C2 | Shared encoder with fault head plus RGT regression/gradient head | Tests whether depositional-coordinate supervision adds information beyond fault labels |

Use identical model-level samples, augmentations, steps, and Thebe fine-tuning for C1 and C2. A C2 gain over C1 is required to support the RGT hypothesis; a gain only over C0 supports generic synthetic pretraining.

Pretrain at native 96³ resolution and fine-tune on the existing 128³ Thebe crops if the selected fully convolutional encoder supports both. Mask salt/undefined RGT and normalize RGT per model. Report transfer to Thebe and later to a second field survey to distinguish in-domain fitting from generalization.

## Execution order under the current hardware

The three matched 150-epoch jobs currently saturate GPU compute and use about 14.3 GiB. Additional concurrent training would slow every experiment and make timing comparisons harder. The next work is ordered as follows:

1. Finish the active R100, V3, and Swin matched controls and generate their queued validation casebook.
2. Run model-native recipe screening with equal trials per architecture.
3. Start the loss branch with boundary distance and local continuity; introduce persistent homology only with label-derived topology.
4. Build the five-slice 2.5D Swin baseline, then SAM-B adapter.
5. Free or relocate storage, acquire a streamed GeoFWI3D subset, and run C0/C1/C2 pretraining.

Each branch answers a distinct question. Results will identify whether the current gap comes primarily from spatial compression, long-range context, unsuitable optimization, boundary/continuity supervision, or missing geological pretraining.
