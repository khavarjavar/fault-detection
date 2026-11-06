# Thebe failure taxonomy and repair plan

Date: 2026-11-02  
Development rule: diagnose and select changes on validation; keep test closed until the choice is frozen.

## Main diagnosis

The strongest completed 3D models usually recognize the dominant fault surface. Their first visible problem is not general discontinuity. It is **spatial localization**: the probability ridge is displaced from the reference, too wide, or both. In Azerbaijani, the prediction looks *sürüşüb* (shifted/slid).

The repair order should therefore be:

1. localization and thickness;
2. recall of weak and secondary faults;
3. separation of adjacent faults;
4. crop-edge and no-data robustness;
5. local continuity and dip consistency;
6. global topology only when the earlier errors are controlled.

The order matters. A strong connectivity penalty can connect a surface in the wrong location or merge two valid faults.

## Why predictions can be shifted

| Candidate cause | Evidence in this project | Diagnostic test | Repair if confirmed |
|---|---|---|---|
| Thick raster reference | The official mask appears as a filled band in enlarged crops. BCE rewards overlap with the band but does not explicitly constrain its central surface. | Measure reference and prediction thickness plus signed normal offset. Inspect the raw Petrel/IESX interpretation if available. | Boundary-distance auxiliary loss; optionally a separate ridge/center-surface head derived from the original interpretation rather than an arbitrary skeleton. |
| Encoder compression | R100 pools three times, so one deep feature cell represents several input voxels. | Compare R100 with the matched limited-downsampling FaultSegV3 run using the same crop sequence and recipe. | Preserve a full-resolution branch or use limited downsampling and high-resolution fusion. |
| Decoder interpolation | Nearest, bilinear, and trilinear upsampling restore size but cannot guarantee exact surface position. | Compare signed offset and width before and after the decoder; inspect logits rather than only the thresholded mask. | Learned high-resolution refinement or boundary/ridge head with shallow full-resolution features. |
| Threshold expansion | The useful operating thresholds are below 0.5, so weak probability skirts can become a wide mask. | Sweep threshold and plot Dice, width ratio, and signed offset. | Recalibration or loss change if only width changes; thresholding cannot repair a displaced ridge center. |
| Local seismic ambiguity | Reflection termination can span several samples, and the offset direction changes among sections. | Stratify errors by local discontinuity strength and compare adjacent slices. | 2.5D/3D context, local attributes, or uncertainty output. |
| Limited crop context | A 128-cube may cut the continuation of a dipping surface; crop borders and no-data zones are visibly harder. | Report metrics by distance to crop edge and valid-data edge. | Halo/overlap inference with blending; larger-context encoder only if the edge-stratified test supports it. |
| Sampling and class imbalance | Fault voxels are about 2.5% of scored test voxels. Secondary faults can disappear while the dominant fault controls the loss. | Component-level recall split by component size and contrast. | Fault-positive and hard-component sampling; Dice/Tversky-style regional term alongside BCE. |
| Registration/axis error | Existing coordinate audits use the same crop and transpose for seismic and label; the visible shift changes direction. | Estimate signed offsets over many validation surfaces. A nearly constant vector would reopen registration debugging. | Fix coordinates only if the offset distribution has a consistent direction and magnitude. |

## Model-by-model problem definition

| Model / experiment | Current evidence | Dominant problem | Most logical improvement | What would be premature |
|---|---|---|---|---|
| R100, seed 43, 100 epochs | Validation Dice 0.569856 and PR-AUC 0.592053. Main surfaces are often continuous, but bands can be shifted or wide and weaker faults are missed. | Localization, thickness, and component recall; some spatially uneven failures. | Finish the 150-epoch saturation run. Then test one boundary-distance term with the same encoder and sampling. Separately test positive/hard-component sampling if secondary-fault recall is low. | Adding a global one-component topology target before measuring component errors. |
| R100, seed 43, 150 epochs | Active. At epoch 55 the subset reached Dice 0.530178 and PR-AUC 0.604712; later epochs fluctuate, so the frozen best checkpoint matters. This run adds epochs only. | Training variance plus the same geometric errors as R100-100. | Keep checkpoint selection on validation PR-AUC and compare the final full-validation geometry profile with the 100-epoch checkpoint. | Claiming improvement or failure from the latest epoch instead of the selected checkpoint. |
| FaultEdgeFormer-inspired | Full-validation Dice 0.563981; test Dice 0.574603. Visuals show coherent dominant faults and relatively strong recall, with false-positive width/offset and missed secondary faults. | Boundary precision and selectivity more than gross continuity. | Add boundary-distance or center-surface supervision; use hard negatives around horizon-like discontinuities and explicit valid-data masking near no-data boundaries. | A heavy connectivity loss as the first change. |
| FaultSegV3 matched control | Active matched architecture test. Epoch 33 produced no positives and PR-AUC 0.104818, then epoch 34 rebounded to Dice 0.056034 and PR-AUC 0.422982. | The matched BCE/Adam recipe is unstable and often becomes extremely conservative; architecture capability is not yet measured fairly. | Let the controlled run finish for the architecture claim. In a separately named capability run use its native MaskDice, AdamW, cosine schedule, drop path, EMA, multiscale batches, and stronger augmentation. Evaluate the released synthetic checkpoint separately as transfer. | Concluding that the high-resolution architecture is poor from this recipe-mismatched run. |
| MONAI SwinUNETR matched control | Active. Epoch 27 subset Dice reached 0.224903 with precision 0.552094 and recall 0.141215, while PR-AUC was 0.336159. | It detects a small confident subset and misses most faults. BCE plus random initialization underuses the 15.7M-parameter transformer. | DiceCE/BCE+Dice, AdamW, warmup/cosine, then seismic SimMIM pretraining as a separate experiment. The published FaultSeg Swin-UNETR also uses multiscale dilated supervision. | Judging the pretrained FaultSeg Swin-UNETR system from this plain matched control. |
| DeepLabV3-ResNet50 2D | Completed: validation Dice 0.499617, PR-AUC 0.481613, precision 0.481805, recall 0.518796. Better than Swin-T 2D but below R100-3D. | Missing crossline context and exact 3D surface consistency; atrous context alone is insufficient, with both false positives and misses. | Transfer its useful idea into a 3D or five-slice 2.5D ASPP/context head. Add overlap reconstruction and boundary evaluation. | Spending the first budget on more identical 2D epochs. |
| Swin-T + FPN 2D | Completed: validation Dice 0.479883, PR-AUC 0.455768, precision 0.449060, recall 0.515249. | More false-positive spread than DeepLabV3, no through-volume evidence, and bilinear FPN reconstruction does not solve fine localization. | Pretrained five-slice 2.5D Swin-T with the center slice as target, then compare against the same pretrained one-slice model. | Treating 2D Swin-T as evidence that Swin context cannot help in 3D. |
| ViT-B/16 + SETR 2D | Active clean recovery at epoch 33. Dice at threshold 0.5 is still zero and PR-AUC is 0.179350. | Coarse patch tokens, random-init data hunger, weak local detail, and low probability calibration. | Pretraining, a smaller effective patch scale or convolutional high-resolution stem, and adjacent-slice input. | Interpreting early zero Dice as final failure; inspect PR-AUC and logits first. |
| HED / RCF author controls | Queued. Deep side-output edge supervision is relevant to localization. | If trained directly against a thick mask, an edge model may learn the two sides of the band rather than the intended fault surface. | Derive a defensible boundary/ridge target and use edge prediction as an auxiliary high-resolution head in the eventual 3D system. | Assuming that edge detection automatically produces a one-voxel geological surface. |
| U-Net / DeepLabM author controls | Queued as source-linked Thebe baselines. | Expected limits are local receptive field, compression, and 2D consistency. | Use them to identify whether simpler multiscale convolution is enough before adding transformer complexity. | Using their paper metric as a direct comparison with the local pooled Dice protocol. |

## Geometry profile required for every completed model

Dice and PR-AUC do not distinguish a shifted correct-looking surface from a broken surface. The same fixed validation cases should report:

1. **Symmetric surface distance and HD95**: how far the predicted surface lies from the reference.
2. **Signed normal or horizontal offset distribution**: whether *sürüşüb* is systematic or changes locally.
3. **Prediction/reference thickness ratio** and probability-ridge width.
4. **Tolerance F1/Dice at 1, 2, 4, and 8 voxels** beside strict Dice.
5. **Component recall by reference-component size**: especially weak and secondary faults.
6. **Merge and split counts** for adjacent surfaces.
7. **Maximum and total gap length** along locally estimated strike/dip.
8. **Metrics by distance to crop edge and no-data boundary**.
9. **Metrics by local seismic discontinuity strength**.
10. Full-section/context and 3D-cube views selected from labels only, with both filled masks and thin outlines.

## Decision rule for the next experiment

| Measured failure | Next controlled change |
|---|---|
| Large offset or width error, acceptable component recall | BCE plus a 3D boundary-distance auxiliary loss; keep architecture and sampling fixed. |
| Low secondary-component recall, acceptable placement on detected faults | Fault-positive/hard-component sampling plus a Dice or Tversky regional term. |
| Short internal gaps after localization is good | Local continuity and dip-consistency loss. |
| Errors concentrate near crop borders | Overlap/halo inference with weighted blending before retraining. |
| Errors concentrate in weak/ambiguous seismic but improve with adjacent slices | Five-slice 2.5D or 3D long-context branch. |
| Multiple real faults are merged | Component separation/instance cue; avoid a universal connectedness prior. |
| Model is all-background or PR-AUC collapses | Repair optimization and imbalance before adding geological priors. |

## Recommended first repair

After the current controlled runs finish, the first loss experiment should target the error already visible in the strongest models:

**R100 or the winning high-resolution encoder + existing regional loss + a low-weight 3D boundary-distance term.**

Use a small validation-only coefficient screen, preserve the same seed/crops/steps, and select with both PR-AUC/Dice and surface-distance metrics. This is more directly tied to the shifted bands than a topology loss. If the geometry profile instead shows that gaps dominate after correct placement, promote the local continuity/dip term next.

## Research support

- Distance Transform Loss was designed for seismic boundary misclassification and penalizes errors according to distance from the true boundary: https://doi.org/10.1016/j.cageo.2025.106061
- Boundary Loss treats the contour directly and complements regional losses in highly imbalanced segmentation: https://arxiv.org/abs/1812.07032
- Hausdorff-distance losses directly target large surface-location errors: https://arxiv.org/abs/1904.10030
- FaultSeg Swin-UNETR uses full-network SimMIM pretraining and multiscale dilated supervision rather than plain random-init SwinUNETR: https://doi.org/10.3390/rs16050922
- The topology/geology-informed seismic work combines curvature, persistent homology, dip, connectivity, and branch terms; its single-surface topological assumption must be adapted to Thebe's multiple valid components: https://doi.org/10.1109/TGRS.2025.3623694
- soft-clDice is supported for tubular or network-like structures. A seismic fault is a surface in 3D, so direct use requires care and should follow a surface-specific validation: https://openaccess.thecvf.com/content/CVPR2021/html/Shit_clDice_-_A_Novel_Topology-Preserving_Loss_Function_for_Tubular_Structure_CVPR_2021_paper.html
