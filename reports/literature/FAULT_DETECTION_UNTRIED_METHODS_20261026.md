# Fault-detection methods not yet tested in this project

**Audit date:** 26 October 2026  
**Scope:** local code, run artifacts, and reports in `projects/fault_detection`, checked against primary papers and author repositories available by the audit date.

## Decision

The project has tested a useful but narrow part of the method space: a small 3D U-Net, one synthetic loss ablation, one attention/loss package, direct real-Thebe training, seed ensembling, incomplete Global Attention3D runs, a short Gaussian-denoising pilot, and frozen SAM-Med3D evaluation. It has **not** completed the most important controls around the current R100 model, a competitive self-configuring segmentation baseline, a 2.5D model, modern masked self-supervision, semi-supervised target-volume learning, explicit incomplete-label handling, or a structural/topological loss.

The best next work is therefore not to select another large architecture at random. The recommended order is:

1. finish inference and ensemble controls on the existing R100 models;
2. improve the real-Thebe training recipe through isolated loss, sampling, augmentation, normalization, and deep-supervision ablations;
3. establish 3D nnU-Net and 2.5D from-scratch baselines;
4. test one label-aware or semi-supervised method;
5. only then spend substantial compute reproducing a large Transformer, Mamba, or foundation-model system.

This order has the highest chance of separating a real method gain from a protocol or implementation gain.

## What has actually been tried

| Family | Local status | Best defensible conclusion |
|---|---|---|
| Small 3D U-Net on synthetic FaultSeg3D | Complete | Dice 0.821059 on the held-out synthetic test. |
| Weighted BCE + soft Dice | Complete on synthetic data only | Dice 0.819766; no gain over synthetic BCE in the matched run. This does **not** answer whether Dice-based loss helps sparse real Thebe labels. |
| Attention gates + connectivity-aware focal Tversky package | Complete on synthetic data | Dice 0.826646, but architecture and loss changed together; PR-AUC decreased. |
| Synthetic-to-Thebe zero-shot transfer | Complete | Weak: Dice 0.085861 for the baseline and 0.079128 for P1 under their recorded evaluations. |
| R100 small 3D U-Net trained from scratch on real Thebe | Complete | Strongest completed family. Three-model frozen full-test ensemble Dice 0.581257. |
| Seed scaling | Five seeds trained; validation analysis complete | Five-model validation Dice 0.597311. No five-model held-out test result exists. |
| Imported 45M-parameter Global Attention3D | Incomplete | FP16 and BF16 supervised attempts have crop-level development results only; neither produced a full-volume test result. |
| Gaussian denoising pretraining | Short pilot complete | Denoiser was worse than the identity baseline and fine-tuning was worse than scratch in the small development experiment. It did not test masked-image modeling or full paper-scale pretraining. |
| SAM-Med3D | Frozen evaluation complete; adapter only preflighted | Frozen prompt-free and oracle-click results were weak. The trainable adapter has no GPU training result. |
| CRACKS transfer | Frozen 2D evaluation only | Weak zero-shot performance; two label policies score different pixel populations. |

The local five-seed result is in `reports/evaluation/r100_seed_curve_5models_20261019/report.md`; the ten original experiment families are mapped in `technical_reports/00_REPORT_INDEX.md`.

## High-priority methods that remain untried

### 1. Overlapping sliding-window inference, Gaussian blending, and test-time augmentation

**Status:** completely untested on R100. Existing inference uses non-overlapping 128-cube partitions.

Run the already specified validation-only comparison:

- non-overlap reference;
- 25% overlap with equal averaging;
- the same windows with Gaussian center weighting;
- optional axis flips as a separate test-time augmentation factor.

This needs no retraining and directly targets patch-edge artifacts. nnU-Net uses sliding-window inference and Gaussian weighting as part of a highly validated segmentation pipeline; the local evidence review already distinguishes inference blending from overlap-consistency training. See the [official nnU-Net repository](https://github.com/MIC-DKFZ/nnUNet), the [nnU-Net paper](https://www.nature.com/articles/s41592-020-01008-z), and the local `R100_ENSEMBLE_AND_OVERLAP_EVIDENCE_20261019.md`.

**Priority:** first. **Cost:** low compute, moderate implementation. **Scientific role:** inference control, not a novel algorithm.

### 2. Complete the five-model ensemble on held-out data

**Status:** the five-model probability ensemble was measured on validation only. It improved validation Dice from the original three-model 0.588951 to 0.597311. The frozen full test has only been evaluated for seeds 42–44.

This is not a new architecture, but it is unfinished evidence. Freeze the five checkpoints, probability averaging rule, and validation-selected threshold before one full-test run. Report it as a five-seed extension rather than retroactively replacing the original three-seed confirmatory result.

**Priority:** first. **Cost:** inference only. **Risk:** repeated use of the same test set can gradually turn it into a development set, so do this after the inference settings are fixed.

### 3. A real-Thebe loss and sparse-sampling ablation

**Status:** R100 uses ordinary masked BCE, 360 random observed patches per epoch, per-patch z-score normalization, and only a random axis-0 flip. The BCE-versus-BCE+Dice comparison was performed on synthetic data, not real Thebe.

The minimum controlled experiment is the same R100 architecture and split with:

1. masked BCE reference;
2. masked BCE + soft Dice;
3. the selected loss plus foreground-aware patch oversampling;
4. deep supervision as a separate factor.

Fault voxels are sparse, so ordinary random patches can spend much of the budget on background. Foreground oversampling and Dice/CE-style compound losses are standard parts of nnU-Net. The 2026 large-scale seismic benchmark also found that window size and loss interact, which makes a real-data ablation more informative than the old synthetic loss result. See the [large-scale fault benchmark](https://arxiv.org/abs/2505.08585) and its [author code](https://github.com/olivesgatech/large-bench-geo).

**Priority:** first new training experiment. **Cost:** one to three R100-scale runs per seed. **Expected value:** high, because it changes the treatment of the exact class imbalance present in the target data.

### 4. Stronger seismic augmentation and normalization

**Status:** not tested beyond one axis flip and per-patch z-score.

Candidate isolated factors are amplitude scaling, gamma/contrast changes, band-limited noise, polarity reversal where geologically appropriate, in-plane rotations, additional valid axis flips, and survey-level or robust percentile normalization. The large-scale benchmark measured Thebe intensity standard deviation at 0.124 versus 1.149 for CRACKS and 1.052 for FaultSeg3D, and found that models trained from scratch on Thebe generally beat models transferred from those datasets. That makes target-specific normalization and augmentation more defensible than another generic synthetic-to-Thebe transfer run.

FaultSSL supplies a seismic-specific strong/weak augmentation design, including coordinate transforms, random-scale Gaussian noise, and gamma transforms. See [FaultSSL](https://arxiv.org/abs/2309.02930).

**Priority:** high. **Cost:** low to moderate. **Control requirement:** change one augmentation package at a time and keep validation/test masks fixed.

### 5. A real nnU-Net baseline

**Status:** not tried. The small local U-Net is not nnU-Net merely because both are U-Nets.

nnU-Net adds dataset fingerprinting, data-dependent 2D/3D configuration, foreground oversampling, compound losses, extensive augmentation, deep supervision, cross-validation, sliding-window inference, Gaussian blending, and model ensembling. Its value here is disciplined configuration and a strong baseline, not domain novelty. The [official implementation](https://github.com/MIC-DKFZ/nnUNet) supports 2D and 3D data and training from scratch.

**Priority:** high. **Cost:** moderate to high. **Practical route:** first reproduce the present split and evaluation rules with a fixed 3D full-resolution configuration; do not silently replace the project’s mask or test protocol with nnU-Net defaults.

### 6. A 2.5D target-domain baseline

**Status:** no 2D or 2.5D model has been trained locally on Thebe.

A 2.5D model predicts the center slice from neighboring slices. It trades full volumetric convolution for a much larger in-plane field of view at lower memory cost. This is especially relevant to thin, long fault traces. Published candidates include the [2.5D Transformer U-Net](https://doi.org/10.3390/rs15041039) and the [2.5D channel-attention U-Net](https://doi.org/10.1190/geo2021-0805.1). Seismic Fault SAM found five adjacent slices best in its ablation, although its OIS/ODS results use a different protocol.

The most informative local version is a modest 2.5D U-Net or DeepLab model trained from scratch on the same physical train/validation/test regions, followed by the same frozen full-volume metrics. This isolates dimensionality and context before introducing SAM or a Transformer.

**Priority:** high. **Cost:** moderate and likely cheaper than 3D R100. **Scientific value:** high because it tests whether the present 3D patch field of view is the limiting factor.

### 7. Explicit incomplete-label learning

**Status:** not tried. The current BCE objective treats every scored zero as a reliable negative.

Field fault labels can omit real but subtle faults. [Visual Attention-Guided Learning With Incomplete Labels](https://doi.org/10.1109/TGRS.2024.3370037) changes sampling and loss weighting to reflect where an interpreter was likely to attend; the authors provide [public code](https://github.com/olivesgatech/attention-fault-interpretation). [Fault-Net and MD loss](https://doi.org/10.1109/TGRS.2022.3196810) weaken anomalous negative supervision under sparse 2D labels; [author code is public](https://github.com/douyimin/FaultNet).

This family answers a different question from feature-attention gates. It asks whether some apparent false positives are actually unlabeled faults and whether the loss should trust every background voxel equally.

**Priority:** high if a blinded visual audit confirms missing faults in Thebe labels; otherwise medium. **Cost:** moderate. **Main risk:** down-weighting true negatives can increase false positives if label incompleteness is assumed without evidence.

### 8. Semi-supervised target-volume learning

**Status:** not tried.

[FaultSSL](https://arxiv.org/abs/2309.02930) uses a mean teacher, a few labeled 2D slices, unlabeled field cubes, panning consistency over overlapping views, and patching consistency between full and cropped views. It specifically targets discontinuity and stitching artifacts. Opunake and Kahu could eventually supply unlabeled field data, but their domain differs from Thebe; the safest first test is a controlled label-scarcity experiment inside Thebe, where most training labels are hidden and used only for evaluation.

**Priority:** medium-high for annotation efficiency and cross-survey deployment; lower for maximizing Thebe Dice when dense Thebe labels are already available. **Cost:** high. **Main risk:** pseudo-label confirmation error and domain mismatch.

### 9. Masked-volume self-supervision instead of Gaussian denoising

**Status:** not tried. The local pilot added fixed Gaussian noise and reconstructed the original crop for only 256 training crops. It does not test masked-image modeling.

[FaultSeg Swin-UNETR](https://arxiv.org/abs/2310.17974) uses SimMIM-style masked seismic reconstruction and a multiscale decoder. A more reproducible generic alternative is the [Seismic Foundation Model author repository](https://github.com/shenghanlin/SeismicFoundationModel), which supplies a seismic masked-autoencoder pipeline and pretrained weights, although its published downstream tasks do not establish fault-segmentation performance.

Run masked pretraining first on unlabeled Thebe training-region amplitudes, then optionally add audited Kahu/Opunake cubes. This respects the benchmark evidence that mismatched-source pretraining can hurt Thebe.

**Priority:** medium. **Cost:** high. **Go/no-go gate:** the pretrained encoder must beat scratch on frozen validation across more than one seed before any held-out test.

### 10. Joint reconstruction and segmentation

**Status:** not tried. This differs from two-stage denoising transfer because reconstruction remains an auxiliary task during supervised fault training.

[MTL-FaultNet](https://doi.org/10.1109/TGRS.2023.3299378) jointly predicts the seismic reconstruction and fault mask. A local low-risk version can add a reconstruction decoder to the existing R100 encoder while leaving the segmentation branch and evaluation unchanged.

**Priority:** medium. **Cost:** moderate. **Scientific value:** clean test of whether preserving reflector structure regularizes fault segmentation.

### 11. Trained 2.5D SAM or directional 3D foundation-model adaptation

**Status:** not completed. Frozen SAM-Med3D was tested, and a SAM-Med3D residual adapter passed CPU preflight, but neither result tests the published seismic-specific adaptation designs.

[Seismic Fault SAM](https://arxiv.org/abs/2407.14121) removes prompt dependence, inserts bottleneck adapters into 2D SAM, predicts from five adjacent slices, and trains a higher-resolution decoder. Its frozen-backbone adapter result therefore cannot be inferred from the local frozen SAM-Med3D failure. A newer early-online method, [3D CSFM](https://doi.org/10.1016/j.aei.2026.105170), adds spatial-view and depth-view 3D adapters, a deeply supervised decoder, and collaborative synthetic/field pseudo-label training.

**Priority:** medium after a plain 2.5D baseline. **Cost:** high. **Reproducibility risk:** I did not find an author implementation for either design during this audit.

### 12. Structural, topology, and physics-informed losses

**Status:** only a simple local-connectivity term has been included in P1, bundled with an architecture change and focal Tversky. Persistent topology, curvature, dip smoothness, branch suppression, and perceptual structure alignment have not been isolated.

[Physics-Informed Neural Networks for 3-D Seismic Fault Segmentation](https://doi.org/10.1109/TGRS.2025.3623694) proposes architecture-independent Allen–Cahn curvature, persistent-homology, and geological consistency losses. [TopSUMseg](https://doi.org/10.3233/FAIA250865) combines Swin and Mamba blocks with a VGG19 perceptual feature loss. Despite its name, TopSUMseg's TASC is a frozen-VGG feature-distance loss rather than persistent homology.

The sensible local experiment is to add one structural term to R100 and report Dice together with bidirectional Chamfer, modified Hausdorff, connected-component count, and visual continuity. Do not transplant the entire TopSUMseg system first.

**Priority:** medium for a publishable structure-aware contribution. **Cost:** moderate for perceptual/curvature losses, high for persistent homology. **Risk:** a smooth continuous mask can improve a structural metric while merging nearby faults or suppressing branches.

### 13. Edge-enhanced, Transformer, and Mamba architectures

**Status:** no completed held-out result exists for a Transformer or Mamba model.

Relevant designs include:

- [FaultEdgeFormer](https://doi.org/10.1093/jge/gxag041): trainable 3D Sobel initialization, convolution-enhanced Swin blocks, and parallel high-resolution multiscale streams; 1.34M parameters, but its published field evidence is mainly qualitative and I found no author code.
- [TopSUMseg](https://doi.org/10.3233/FAIA250865): Swin–Mamba hybrid plus global-local attention and perceptual structural loss; trained on four A100 GPUs in the paper.
- [MSDA-UNet](https://doi.org/10.1016/j.marger.2026.207664): multiscale deformable attention and depthwise separable convolution; primarily validated quantitatively on synthetic data.

**Priority:** medium-low until stronger baselines are complete. **Reason:** architecture, loss, context, augmentation, and evaluation often change together, making a gain hard to attribute. FaultEdgeFormer is the most feasible compact architecture of this group.

### 14. Explicit domain adaptation for new surveys

**Status:** not tried. Existing work used zero-shot transfer or ordinary fine-tuning/pretraining.

Frequency-domain alignment, adversarial domain adaptation, mean-teacher consistency, and the collaborative branch training used by 3D CSFM are relevant when the final target is Kahu, Opunake, Kerry, F3, or another unlabeled survey. They are not the first choice for improving Thebe because the large benchmark found that training directly on Thebe generally beat transfer from FaultSeg3D or CRACKS.

**Priority:** high for deployment to a new unlabeled survey; low for the immediate Thebe score. **Required evidence:** a target-survey audit and at least a small blinded set of expert labels.

## Methods worth tracking, but not first in the queue

| Method | Why it is lower priority now |
|---|---|
| Full Global Attention3D reproduction | Scientifically relevant and already planned, but blocked by exact pretraining data, backbone/checkpoint compatibility, split details, and expensive training. Complete it as a named reproduction, not as the only route forward. |
| UNETR/Swin-UNETR from scratch | Useful architecture controls, but published seismic benchmarks do not show that a large Transformer automatically beats a well-configured target-domain CNN. |
| U-Net++, HED, RCF | The large benchmark reports fragmented U-Net++ behavior and noisy/distorted HED/RCF outputs on Thebe. They may be reference baselines, not leading candidates. |
| Generic synthetic pretraining followed by Thebe fine-tuning | Already contradicted by the local zero-shot failures and by the 200-model benchmark’s Thebe results. Only revisit with an explicit domain-alignment hypothesis. |
| EWC-style continual learning | Relevant to catastrophic forgetting, but not the direct bottleneck for in-domain Thebe performance. |
| CRF, skeletonization, component pruning | Potentially useful postprocessing, but easy to tune against labels and capable of changing fault thickness. Apply only after validation freezing and score structural as well as overlap metrics. |
| Point-cloud instance segmentation | Methods such as MC-DBRG address separating fault instances after a fault point cloud exists. They do not replace the voxel detector and require a reliable initial segmentation. |

## Recommended experiment sequence

### Phase A: finish the current baseline without training

1. Cache the five frozen R100 probability volumes on validation.
2. Compare non-overlap, 25% overlap/equal blend, and 25% overlap/Gaussian blend.
3. Test flip TTA as its own factor.
4. Select exactly one inference rule and threshold on validation.
5. Run the selected five-model configuration once on full test.

This establishes how much performance remains in existing checkpoints.

### Phase B: strengthen the target-domain CNN

Run a small factorial ladder, initially seed 42 and then three seeds only for survivors:

1. current R100 masked BCE;
2. BCE + soft Dice;
3. selected loss + foreground oversampling;
4. selected setup + seismic augmentation;
5. selected setup + deep supervision;
6. selected setup under per-patch versus robust survey-level normalization.

Use the same data split, crop budget, optimizer budget, checkpoint rule, validation coverage, and evaluation code. This phase is more informative than substituting an unverified large model.

### Phase C: establish dimensional and framework baselines

1. plain 2.5D U-Net with 1, 3, 5, and 7 neighboring slices selected on validation;
2. nnU-Net 3D full-resolution under the same mask and regions;
3. optional 2D/2.5D DeepLabV3 or SegFormer using the benchmark code.

### Phase D: choose one research contribution

Choose based on the failure observed in Phases A–C:

- missing or uncertain labels: visual-attention/MD-loss learning;
- patch seams and scarce labels: FaultSSL consistency;
- fragmented faults: a single topology/structure loss;
- weak large-scale context: 2.5D SAM adapter or compact FaultEdgeFormer;
- new-survey deployment: explicit domain adaptation;
- abundant unlabeled target amplitudes: SimMIM masked-volume pretraining.

## What the published scores do and do not mean

Do not compare the local pooled full-volume Dice 0.581257 directly with published OIS/ODS values near 0.87. TopSUMseg and Seismic Fault SAM use Thebe’s 900/200/703 crossline split and boundary-style OIS/ODS evaluation. OIS selects thresholds per image; ODS uses one dataset threshold. The local protocol concatenates HDF5 blocks, masks invalid voxels, predicts 3D patches, and computes pooled voxel counts over 2.30 billion scored test voxels. Different splits, masks, label thickness, dimensionality, threshold rules, and aggregation can move the number substantially.

For every future method, retain:

- frozen pooled Dice, IoU, precision, recall, MCC, and PR-AUC;
- bidirectional Chamfer and modified Hausdorff distances;
- per-block and per-patch distributions;
- connected-component and continuity descriptors;
- runtime, peak memory, parameter count, and coverage;
- blinded visual review of fixed sections.

The [large-scale benchmark](https://arxiv.org/abs/2505.08585) demonstrates that Dice can disagree with distance metrics and visual structure. A method should therefore be called better only when the predeclared primary metric improves without an unacceptable structural or precision/recall failure.

## Final ranking for this repository

| Rank | Next method | Expected information per unit cost | Recommendation |
|---:|---|---|---|
| 1 | Five-seed ensemble + overlap/Gaussian blending + separate TTA | Very high | Do now; no training required. |
| 2 | Real-Thebe BCE/Dice + foreground-sampling ablation | Very high | First controlled training study. |
| 3 | Seismic augmentation and normalization ablation | High | Run on the winning R100 loss/sampler. |
| 4 | Plain 2.5D target-domain U-Net | High | Best architecture-level comparison for modest compute. |
| 5 | 3D nnU-Net | High | Necessary strong general segmentation baseline. |
| 6 | Incomplete-label learning with public code | High if labels are incomplete | Audit labels first, then run. |
| 7 | FaultSSL target consistency | High for sparse labels/new surveys | Use when unlabeled target volumes and a few labels are available. |
| 8 | SimMIM masked-volume pretraining | Medium-high | Distinct from the failed denoising pilot; gate on validation. |
| 9 | Joint reconstruction/segmentation | Medium | Clean, relatively inexpensive auxiliary-task experiment. |
| 10 | One structural/topological loss on R100 | Medium-high novelty | Isolate the loss before adopting a large hybrid architecture. |
| 11 | Seismic Fault SAM / 3D CSFM | Potentially high, high risk | Run after the plain 2.5D baseline. |
| 12 | FaultEdgeFormer or TopSUMseg reproduction | Potentially high, highest implementation risk | Later architecture track; code/protocol availability is the constraint. |

The central research conclusion is that the project has already shown the largest empirical effect comes from **training on labeled target-domain Thebe data**, followed by ensembling. The untried methods most likely to improve the result are therefore target-domain sampling/loss/context/inference controls. Cross-survey pretraining and larger architectures remain valuable research questions, but current evidence does not justify treating them as automatic improvements.
