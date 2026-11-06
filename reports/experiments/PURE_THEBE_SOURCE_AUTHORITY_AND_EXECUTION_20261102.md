# Pure Thebe source authority and execution plan

Date: 2026-11-02

## Why this audit is required

The Seismic Fault SAM paper says that its comparison methods were reimplemented
from official implementations with default settings. Its v1 manuscript does
not identify code commits, configuration files, checkpoints, or a public author
repository for those experiments. It also states that the MAE and SimMIM
variants used private unlabeled field seismic data. The numerical table is
therefore useful evidence, but it is not a complete executable specification.

Every local result must use one of these labels:

1. **Author-code reproduction**: model and Thebe protocol come from code
   released by the relevant paper or dataset authors.
2. **Official architecture adaptation**: an official implementation or
   backbone is used, while the Thebe input, head, or trainer is local and fully
   disclosed.
3. **Paper-described reconstruction**: the paper describes the method, but no
   verified author implementation was found; local code is not described as an
   author reproduction.

## Model-by-model authority map

| Comparison entry | Primary model source | Thebe-specific source | What is verifiable | Local claim and action |
|---|---|---|---|---|
| FaultSeg3D | [Author repository](https://github.com/xinwucwp/faultSeg), [Geophysics paper DOI](https://doi.org/10.1190/geo2018-0646.1) | [Thebe author comparison code](https://github.com/anyuzoey/CNNforFaultInterpretation/tree/master/faultSeg) | Author architecture and a Thebe port are public. | Use the author code/port as the reference. Do not rename a different 3D U-Net as FaultSeg3D. |
| Swin-UNETR | [MONAI author contribution](https://github.com/Project-MONAI/research-contributions/tree/main/SwinUNETR), [paper](https://arxiv.org/abs/2201.01266) | Seismic comparison settings are described in [FaultSeg Swin-UNETR](https://www.mdpi.com/2072-4292/16/5/922). | Official architecture is public. The paper's private seismic SimMIM corpus is unavailable. | Active MONAI run is an official-architecture Thebe adaptation with random initialization, not the paper's SimMIM result. |
| FaultSeg Swin-UNETR | [Remote Sensing paper](https://www.mdpi.com/2072-4292/16/5/922) | Same paper | Architecture, multi-scale decoder, optimizer family, and figures are described. No verified author code/checkpoint was located. | Label the current implementation **paper-described local reconstruction**. Keep it separate from MONAI Swin-UNETR. |
| 2D U-Net | [Original author page, paper, and release](https://lmb.informatik.uni-freiburg.de/people/ronneber/u-net/) | [Thebe dataset-author code](https://github.com/anyuzoey/CNNforFaultInterpretation/blob/master/model_zoo/UNET.py) and [trainer](https://github.com/anyuzoey/CNNforFaultInterpretation/blob/master/train.ipynb) | Exact Thebe baseline architecture/trainer is public: 96-pixel patches, BCE, Adam, ReduceLROnPlateau, early stopping. | Port this code to current PyTorch and preserve the published loss/optimizer. This is the reference U-Net run. |
| HED | [Original author code](https://github.com/s9xie/hed), [ICCV paper](https://arxiv.org/abs/1504.06375) | [Thebe dataset-author HED](https://github.com/anyuzoey/CNNforFaultInterpretation/blob/master/model_zoo/HED.py), [trainer](https://github.com/anyuzoey/CNNforFaultInterpretation/blob/master/train.ipynb), and [loss](https://github.com/anyuzoey/CNNforFaultInterpretation/blob/master/functions.py) | The Thebe port and deeply supervised class-balanced loss are public. | Preserve all five side losses plus fused-output BCE. A generic one-head BCE run is not called HED reproduction. |
| RCF | [Original author code](https://github.com/yun-liu/rcf), [TPAMI paper](https://doi.org/10.1109/TPAMI.2018.2878849) | [Thebe dataset-author RCF](https://github.com/anyuzoey/CNNforFaultInterpretation/blob/master/model_zoo/RCF.py), [trainer](https://github.com/anyuzoey/CNNforFaultInterpretation/blob/master/train.ipynb), and [loss](https://github.com/anyuzoey/CNNforFaultInterpretation/blob/master/functions.py) | The Thebe port and its class-balanced side-output loss are public. | Preserve the RCF side outputs and the published 1.1 negative-class factor. |
| DeeplabM | [Thebe benchmark paper](https://doi.org/10.1109/ACCESS.2023.3244683) | [Thebe dataset-author MobileNet DeepLab code](https://github.com/anyuzoey/CNNforFaultInterpretation/tree/master/model_zoo/DEEPLAB) and trainer | Exact Thebe baseline is public: MobileNet DeepLab, BCE, Adam, 96-pixel overlapping patches. | Reproduce this separately from DeepLabV3-ResNet. |
| DeepLabV3 | [Google DeepLab source](https://github.com/google-research/deeplab2), [torchvision implementation](https://docs.pytorch.org/vision/stable/models/deeplabv3.html) | The Thebe prior-knowledge paper identifies ImageNet-pretrained ResNet-101. | Official architecture/weights exist; the Seismic Fault SAM paper does not expose its exact training config. | Run an official torchvision adaptation and record backbone, weight enum, patching, and optimizer. Current ResNet-50 random run is explicitly an architecture control. |
| 2D ViT | [Google Research implementation](https://github.com/google-research/vision_transformer), [ViT paper](https://arxiv.org/abs/2010.11929), [MAE author code](https://github.com/facebookresearch/mae) | No public comparison-paper decoder/config found. Its seismic MAE data are private. | Official encoder and public ImageNet/MAE weights exist; exact seismic segmentation head is unspecified. | Current ViT-B/16 plus SETR-style local head is an official-backbone adaptation, not the comparison implementation. Test random and public ImageNet/MAE variants separately. |
| 2D Swin | [Microsoft author implementation](https://github.com/microsoft/Swin-Transformer), [paper](https://arxiv.org/abs/2103.14030), [official semantic segmentation code](https://github.com/SwinTransformer/Swin-Transformer-Semantic-Segmentation), [SimMIM](https://github.com/microsoft/SimMIM) | No public comparison-paper config found. Its seismic SimMIM data are private. | Official encoder, segmentation reference, ImageNet weights, and generic SimMIM are public. | Current Swin-T plus local FPN is an official-backbone adaptation. Public ImageNet and random variants are valid; private-seismic SimMIM is not exactly reproducible. |
| SAM-b / SAM-h | [Meta author code and checkpoints](https://github.com/facebookresearch/segment-anything), [ICCV paper](https://arxiv.org/abs/2304.02643) | Seismic adaptation is described in the [comparison paper](https://arxiv.org/html/2407.14121v1). | Base SAM is official. The paper's automatic decoder, adapters, regularizer, and five-slice input are described, but no verified author code/checkpoint was located. | Direct SAM uses official code/weights. Adapter and 2.5D variants are labeled paper-described reconstructions and must report trainable parameters and deviations. |

## Dataset authority

- **Thebe**: use the [dataset paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC8220338/),
  [Harvard Dataverse record](https://doi.org/10.7910/DVN/YBYGBK), and the
  [dataset-author preprocessing code](https://github.com/anyuzoey/CNNforFaultInterpretation).
  Keep the official 900/200/703 crossline train/validation/test split. Model
  selection and threshold selection use validation only; test remains closed
  until the experiment family and visualization cases are frozen.
  The local index reconstruction has been verified against the author notebook:
  it reproduces exactly **181,029 training** and **64,317 validation**
  fault-rich patches at 96×96 with stride 48 and the 3% fault-pixel filter.
- **Private seismic pretraining data**: unavailable. Results depending on the
  paper's private MAE/SimMIM corpus cannot be claimed as exact reproductions.
- **GeoFWI3D**: retain as a separate new-data branch using its
  [author repository](https://github.com/aaspip/geofwi3d),
  [paper](https://arxiv.org/abs/2610.01033), and
  [Zenodo data record](https://zenodo.org/records/20148778). It is not inserted
  into pure Thebe architecture controls.

## Execution tracks

### A. Running 3D controls

- R100, 150 epochs, seed 43.
- official MONAI Swin-UNETR Thebe adaptation, 150 epochs, seed 43.
- paper-described FaultSeg Swin-UNETR reconstruction, 150 epochs, seed 43.

All three select checkpoints and thresholds on validation and keep test closed.

### B. Preflighted 2D architecture controls

- torchvision DeepLabV3-ResNet50, random initialization.
- torchvision Swin-T plus disclosed local FPN head, random initialization.
- torchvision ViT-B/16 plus disclosed SETR-style progressive head, random
  initialization.

These run sequentially on the same GPU so that only one extra model competes
with the 3D jobs. They are probes of context and tokenization, not replicas of
the comparison paper's best pretrained rows.

### C. Author-protocol Thebe baselines

Port and preflight U-Net, HED, RCF, and MobileNet DeepLab from the Thebe
dataset-author repository. Preserve each model's own loss and optimizer. This
directly addresses the risk that one shared loss can suppress a model that
needs side-output supervision or class balancing.

All four ports passed forward/backward smoke tests. Synthetic batch-64 peak GPU
allocations were 1.03 GiB (HED), 1.13 GiB (RCF), 2.08 GiB (U-Net), and 1.60 GiB
(MobileNet DeepLab). Their queue waits for the three scratch 2D controls, then
runs HED, RCF, U-Net, and MobileNet DeepLab one at a time.

### D. Pretrained and adapter variants

After the scratch controls, compare official public ImageNet weights for
DeepLabV3, ViT, and Swin. Implement direct SAM-b first, then the five-slice
SAM-b adapter reconstruction. SAM-h is deferred until storage is sufficient;
its much larger checkpoint must not displace active run artifacts.

### E. Broader retained branches

Topology/geology losses, GeoFWI3D fault-only and fault-plus-RGT pretraining,
and joint objectives remain active research branches. They are evaluated after
the pure-model controls identify which spatial errors and encoder failures need
repair.

## Completed FaultEdgeFormer visual diagnostic

The completed seed-42 FaultEdgeFormer-inspired architecture control selected
epoch 99 and threshold 0.24560546875 using complete validation. It obtained
validation Dice 0.563981 and PR-AUC 0.592442. Its previously frozen test result,
with the same threshold, was Dice 0.574603 and PR-AUC 0.603953.

Artifacts:

- [validation casebook](../evaluation/faultedgeformer_thebe_full_seed42_20261026/validation_casebook.png)
- [frozen test casebook](../evaluation/faultedgeformer_thebe_full_seed42_20261026/test_casebook.png)
- [complete-volume metric and precision-recall summary](../evaluation/faultedgeformer_thebe_full_seed42_20261026/frozen_metrics_summary.png)
- [case-selection and section-metric manifest](../evaluation/faultedgeformer_thebe_full_seed42_20261026/visual_manifest.json)

The validation views were chosen from reference labels in the fixed validation
subset before inference. The test views reuse the three label-selected origins
from the earlier frozen R100 visualization, so predictions did not select easy
FaultEdgeFormer cases.

The pictures separate three errors. Strong primary faults are usually
continuous, but the prediction is wider or laterally displaced. Secondary
faults can be absent even when the primary fault is found. A weak fault beside
an irregular no-data boundary receives almost no foreground probability. The
last failure has no predicted component for a topology loss to connect. The
evidence therefore prioritizes stronger weak-fault/context features and
fault-positive sampling, followed by boundary or distance supervision for
width and alignment. Connectivity or persistent-homology penalties remain a
later controlled branch for cases where foreground exists but fragments.

## Visualization gate

For every completed family, generate the same validation casebook: seismic,
label, probability, fixed-threshold mask, false positives, false negatives,
and connected-component summaries. Include high-fault, fragmented, noisy,
and near-empty slices selected without test access. Quantitative tables alone
do not decide the next experiment.
