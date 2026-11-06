# R100 ensembling and overlap: what the papers support

Reviewed: 19 October 2026. This is a focused search of primary papers, not a complete novelty review.

**Assessment:** averaging models and blending overlapping patches are established methods. Trying them with the existing R100 models is a realistic experiment. Their existence in papers does not establish that overlap will improve our Dice, and applying these methods alone would not introduce a new algorithm.

## Four relevant papers

| Paper | What it supports | Limit for our project |
|---|---|---|
| Lakshminarayanan, Pritzel and Blundell, **Simple and Scalable Predictive Uncertainty Estimation using Deep Ensembles**, NIPS 2017. [Paper, section 2.4](https://arxiv.org/html/1612.01474v3) | Independently trained networks can be combined by averaging their predicted probabilities. Random initialization and data ordering provide diversity. | Supports our ensemble mechanism; it does not establish R100 performance, geological accuracy, or calibrated uncertainty for our models. |
| Isensee et al., **Automated Design of Deep Learning Methods for Biomedical Image Segmentation**, 2019 nnU-Net preprint. [Paper, Inference paragraph](https://arxiv.org/html/1904.08128) | Describes half-patch overlap and Gaussian weights that favor patch centers when combining predictions. | Medical segmentation evidence, not a measured R100 benefit. Its inference configuration is not an isolated proof that Gaussian blending alone improves every model. |
| An, Ye, Guo and Dong, **Overlap Training to Mitigate Inconsistencies Caused by Image Tiling in CNNs**, AI 2020. [Author manuscript, sections 3.3 and 4](https://researchrepository.ucd.ie/rest/bitstreams/47854/retrieve) | Directly studies stitching artifacts on Thebe. It compares stitching approaches and trains models with a constraint encouraging overlapping predictions to agree. | Training with an overlap-consistency loss differs from blending predictions at inference. The manuscript uses 2D models and its own split and scoring rules; its scores cannot be compared directly with our pooled 3D Dice. |
| Quesada et al., **A Large-scale Benchmark on Geological Fault Delineation Models: Domain Shift, Training Dynamics, Generalizability, Evaluation and Inferential Behavior**, 2025 preprint. [Paper, abstract and section IV](https://arxiv.org/html/2505.08585v1) | Studies more than 200 models using FaultSeg3D, CRACKS and Thebe, including transfer strategies and evaluation issues. | Our dataset selection and broad synthetic-to-real question already have substantial precedent. Its splits and label processing differ from ours. |

## What is already demonstrated in this project?

The saved test results show best individual-seed Dice **0.567466** and ensemble Dice **0.581257**: a difference of **0.013791**, or about **1.38 Dice percentage points**. These are results on the existing Thebe test split, not a statistical significance claim or a guarantee for other surveys. See the [completed evaluation](../evaluation/r100_clean_frozen_test_20261019/report.md).

Overlapping-patch inference has not been tested in this project. The claim that it would improve this ensemble remains a hypothesis.

## Two different uses of overlap

**Overlap during prediction:** use the existing models on overlapping cubes. A voxel receives several predictions, which are combined with equal weights or greater weight near cube centers. No retraining is required. This was the proposed small next experiment.

**Overlap during training:** add a loss encouraging two overlapping views to predict the same shared region consistently. This requires retraining. It is a separate experiment with existing research precedent, as shown in An et al.'s manuscript above.

## Is this a new research contribution?

My assessment is that the current small U-Net, ordinary BCE, multiple seeds, and probability averaging constitute a useful baseline, not an established novel method. Gaussian blending is also existing methodology. Better reproducibility and a higher score do not, by themselves, demonstrate algorithmic novelty.

A stronger research study would need a specific unresolved question and controlled evidence: for example, quantify which inference or training choices preserve fault continuity under limited labels or a different survey. This is a possible research direction, not a claim that such a question is untouched. Its novelty needs a broader targeted search, including the seismic benchmark above.

## A concrete experiment to replace speculation

Use validation only and keep the current checkpoints fixed:

| Variant | Change | Purpose |
|---|---|---|
| A | Existing non-overlap ensemble; validation Dice 0.588951 | Preserve the reference. |
| B | 25% overlap, equal weighting | Measure the effect of overlapping views. |
| C | Same windows as B, Gaussian weighting | Separate the effect of weighting from the overlap amount. |

The earlier 25% suggestion was a practical starting value, not a paper-established optimum. The nnU-Net preprint uses 50%; that can be another configuration if the initial results justify its extra computation.

Combine probabilities first and score each physical voxel once, regardless of how many cubes cover it. Preserve the same validity mask and fault labels. Record performance at the original threshold and at a validation-selected threshold for the new configuration. Also inspect errors near cube edges and examples of fault continuity. Keep normalization consistent between B and C; changing windows also changes the context and per-patch normalization.

The experiment is feasible with patch-based inference, but overlap adds model calls and needs careful accumulation of weighted predictions. Measure runtime alongside Dice. Freeze the chosen settings before any later test evaluation; use the current completed test as the historical reference rather than tuning against it.

This literature check did not run new predictions or training.
