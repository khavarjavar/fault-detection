# Beginner reader: what each fault model does and how to read its result

Date: 2026-11-02

This guide assumes no previous experience with these networks. The final goal
is a reliable 3D fault detector. The 2D models are shorter diagnostic
experiments that tell us which ideas may be worth transferring into 3D.

## Five terms to know

| Term | Simple meaning | Fault-detection role |
|---|---|---|
| **Encoder** | The part that reads the seismic image and turns it into features | Finds discontinuities, offsets, terminations, texture, and larger structures |
| **Context/bottleneck** | The most compressed or globally connected features | Decides whether an edge is likely a geological fault or ordinary seismic texture |
| **Decoder** | Expands features back to the original resolution | Draws the fault probability at every pixel or voxel |
| **Skip connection** | Sends fine features directly from encoder to decoder | Restores thin faults and precise positions lost during compression |
| **Loss** | The training error that tells the network what to correct | Can prioritize voxel accuracy, rare faults, boundaries, or connectivity |

Every segmentation model can be read as:

```text
seismic data
    ↓
encoder: find useful patterns
    ↓
context: decide which patterns look like faults
    ↓
decoder: restore full resolution and draw probabilities
    ↓
validation-selected threshold
    ↓
binary fault mask
```

The probability map is more informative than the binary mask. A missing fault
with moderate probability may be repaired by threshold or calibration. A fault
with almost zero probability requires better features, data, or context.

## Direct 3D candidates

### R100 / FaultSeg3D

```text
128³ seismic cube
 → 3D convolutions
 → pool smaller three times
 → deep 3D features
 → upsample three times + encoder skip connections
 → fault probability cube
```

| Part | What it does |
|---|---|
| Encoder | Ordinary 3D convolutions at 16, 32, 64, and 128 channels |
| Context | Three pooling steps give a wider view but compress fine detail |
| Decoder | Nearest-neighbour upsampling plus U-Net skip connections |
| Current loss | Ordinary BCE on observed voxels |
| Most useful for | A strong, simple 3D reference; major faults with clear displacement |
| Main limitations | Pooling can suppress weak thin faults; BCE does not directly train boundary quality or connectivity; no pretraining or attention |

R100 is the control that tells us whether a more complicated model actually
adds value over a standard 3D U-Net.

### FaultSegV3

```text
128³ seismic cube
 → preserve a full-resolution feature path
 → one main-path downsampling
 → repeatedly exchange high- and lower-resolution information
 → shallow decoder
 → fault probability cube
```

| Part | What it does |
|---|---|
| Encoder | High-resolution 3D backbone with only one main-path downsampling |
| Context | Lower-resolution streams repeatedly exchange information with the high-resolution stream |
| Decoder | Shallow restoration step because fine detail was retained |
| Current loss | Same ordinary BCE as R100, to isolate architecture |
| Most useful for | Fine discontinuities, small offsets, and closely spaced faults |
| Main limitations of our run | Random initialization; released checkpoint and stronger author training recipe are not used; ordinary BCE may underuse its fine-detail capability |

This experiment asks whether preserving spatial resolution is more valuable
than R100's deeper compression on Thebe.

### MONAI SwinUNETR

```text
128³ seismic cube
 → divide features into local 3D windows
 → shifted-window transformer attention at several scales
 → hierarchical compressed features
 → U-Net-like convolutional decoder + skip connections
 → fault probability cube
```

| Part | What it does |
|---|---|
| Encoder | Official 3D Swin transformer; attention exchanges information inside shifted windows |
| Context | Hierarchical transformer features see broader relationships than local convolutions |
| Decoder | Convolutional U-Net decoder restores voxel resolution using skips |
| Current loss | Same ordinary BCE as R100 |
| Most useful for | Separating geological faults from confusing local edges; longer contextual continuity |
| Main limitations of our run | 15.7 M parameters, slow, random initialization, and no seismic SimMIM pretraining; transformers can be data hungry |

This is an architecture test. It is not the private-pretrained Swin result from
the comparison paper.

### FaultEdgeFormer-inspired model — completed

```text
128³ seismic cube
 → trainable 3D Sobel edge filters
 → local and shifted-window attention
 → three fused resolution streams
 → multiscale decoder
 → fault probability cube
```

| Part | What it does |
|---|---|
| Encoder | Begins with directional edge filters, then convolutional window attention |
| Context | Alternating local/shifted windows plus cross-scale fusion |
| Decoder | Combines high-resolution edge detail with lower-resolution context |
| Loss | Ordinary masked BCE |
| Most useful for | Obvious edge-like faults with useful local context |
| Observed limitation | Predictions can be too wide or laterally shifted; secondary and weak faults may disappear |
| Scientific limitation | Paper-inspired local implementation because verified author code was unavailable; one seed |

Completed result: validation Dice **0.563981**, frozen test Dice **0.574603**.
See the [validation casebook](../evaluation/faultedgeformer_thebe_full_seed42_20261026/validation_casebook.png)
and [frozen test casebook](../evaluation/faultedgeformer_thebe_full_seed42_20261026/test_casebook.png).

## 2D diagnostic models

These models process one seismic section at a time. They cannot establish final
3D continuity, but they are fast ways to learn which feature extractor or loss
is promising.

| Model | Simplified pipeline | What question it answers | Main limitation |
|---|---|---|---|
| **DeepLabV3-ResNet50** | CNN encoder → dilated multiscale context → simple upsampling head | Do several context sizes help distinguish obvious faults from texture? | Coarse decoder and no adjacent-section information can blur thin faults |
| **Swin-T + FPN** | Hierarchical shifted-window encoder → feature pyramid decoder | Does local attention plus multiple spatial scales help? | Random-init transformer may need more data or pretraining; still 2D |
| **ViT-B/16 + SETR** | Split image into 16×16 tokens → global attention → progressive upsampling | Does global section-wide context help? | Tokenization can discard thin local evidence; large and data hungry; still 2D |

These three use the same Thebe-only training recipe and random initialization.
Their comparison isolates the architecture more cleanly than comparisons using
different pretrained weights or losses.

## Thebe author-protocol 2D baselines

These models use their own source-released losses and optimizers. They answer a
different question: how well does each complete published recipe work?

| Model | Encoder and decoder in simple words | Useful for | Limitation |
|---|---|---|---|
| **U-Net** | Compress through convolution/pooling, then expand with matching skip features | General section segmentation and a source-verified reference | No explicit edge, topology, or adjacent-section supervision |
| **HED** | Five encoder depths each predict an edge map; the five maps are enlarged and fused | Teaching fault boundaries at fine and coarse scales | Edge responses can also follow nonfault reflectors; 2D only |
| **RCF** | Like HED, but uses features from every convolution in each stage before fusion | Richer weak-edge and multiscale detail | More possible clutter and no 3D continuity |
| **DeepLabM** | Lightweight MobileNet encoder → four dilation rates plus global context → low/high-feature decoder | Efficient multiscale detection and possible lightweight deployment | Lightweight encoder may miss difficult faults; 2D only |

HED and RCF are especially relevant to the current visual finding that detected
faults can be too wide or misaligned. If they improve boundaries visibly, their
side-output supervision can be translated into a 3D boundary head.

## Which experiment addresses which failure?

| Visible problem | Most relevant current experiment | What we would transfer into 3D if it works |
|---|---|---|
| Major fault is completely missing | FaultSegV3, SwinUNETR, later 2.5D | High-resolution features or more adjacent/context information |
| Fault is detected but too wide | HED or RCF | Boundary side head and boundary-aware loss |
| Fault breaks into pieces | SwinUNETR; later local topology/continuity loss | Wider context first, then label-conditioned continuity supervision |
| Texture produces false faults | DeepLabV3, Swin, ViT | Multiscale or attention context |
| Several nearby faults merge | FaultSegV3, HED/RCF | Preserve fine resolution and sharpen boundaries |
| Model must be small and fast | FaultSegV3 or DeepLabM | Compact encoder and shallow decoder |

## Why did the 100-epoch R100 result sometimes look lower?

First, Dice means overlap: **1 is perfect and 0 means no overlap**. Several
different R100 Dice numbers exist because they answer different questions.

### Final complete-validation results

| Seed | Selected epoch | Validation threshold | Complete-validation Dice |
|---:|---:|---:|---:|
| 42 | 95 | 0.3164 | 0.5441 |
| 43 | 93 | 0.2793 | 0.5699 |
| 44 | 95 | 0.2441 | 0.5730 |

The frozen test Dice values were 0.5248, 0.5675, and 0.5655. Averaging their
probabilities produced ensemble test Dice **0.5813**.

### Why a training-log Dice can be smaller

1. **Training logs use threshold 0.5.** The final seed-43 threshold was 0.2793.
   A lower threshold recovered more true fault voxels.
2. **Training logs use a fixed 128-patch subset.** The final score covers the
   complete validation volume with 650 tiles.
3. **The final model is the best checkpoint.** Seed 43 peaked at epoch 93. The
   epoch-100 weights were not automatically considered better.
4. **Random initialization changes results.** Seed 42 reached 0.5441 while
   seeds 43 and 44 reached about 0.57 under the same protocol.
5. **Faults are rare.** Ordinary BCE sees far more background than fault
   voxels, so a model can obtain low loss while still missing weak faults.

The 100-epoch run does **not** clearly show that training stopped too early.
All three selected checkpoints were at epochs 93–95. The current 150-epoch job
tests whether a later improvement appears, but epochs 1–100 repeat the old
seed-43 run exactly. Only epochs 101–150 will provide new evidence. If the best
validation PR-AUC stays near epoch 93, adding epochs did not solve the limiting
problem.

### Architectural reasons for the remaining R100 error

- Three pooling stages can erase thin or low-contrast discontinuities.
- Ordinary BCE does not directly penalize broken surfaces or inaccurate width.
- A 128³ crop has limited geological context beyond its boundaries.
- Training starts from random weights and uses no additional seismic/RGT data.
- Random patches include many easy background regions, reducing the fraction
  of updates focused on difficult fault examples.

These are hypotheses to test with controlled experiments. The current model
comparisons are designed to separate them.

## Important limitations of the current experiment collection

| Limitation | Why it matters |
|---|---|
| Most architecture controls use ordinary BCE | Fair for isolating architecture, but may understate a model that needs its native loss |
| Current transformer controls start randomly | They do not test the expected benefit from public or seismic pretraining |
| 2D metrics do not measure volume continuity | A visually good section model can flicker between adjacent sections |
| Thebe is one survey family | Strong Thebe performance does not guarantee the same behavior on a mentor's survey |
| Topology is not universally one component | Only 47.4% of audited fault-present patches had one substantial component; a naive one-component loss may join separate faults |
| Some source papers use different metrics | Tolerance IoU and strict voxel Dice cannot be compared as if they were identical |

## Productive work while training runs

1. Open the FaultEdgeFormer validation and test casebooks linked above.
2. For every row, answer four questions: Was the main fault found? Was it
   continuous? Is its width correct? Is there false-fault clutter?
3. Decide what the mentor needs: probability volume, binary mask, or both.
4. Record the mentor volume format, axis order, sample spacing, approximate
   volume shape, and available GPU memory.
5. Prepare one representative mentor volume without using it to tune on hidden
   labels. We will run the selected frozen model and return its probability and
   mask for independent review.

A useful first product may reliably detect obvious faults while documenting
that weak secondary faults remain a later target.

For exact source authority and implementation labels, see
[Pure Thebe source authority and execution plan](PURE_THEBE_SOURCE_AUTHORITY_AND_EXECUTION_20261102.md).
For live run locations, see
[Next working day experiment tracker](NEXT_WORKING_DAY_TRACKER_20261102.md).
