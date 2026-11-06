# Attention3D: Kerry status, dataset roles, and defensible two-survey experiment

**Evidence cut-off:** 2026-10-23 (Asia/Baku)  
**Target paper:** Matin Mahzad and Majid Bagheri, *Fault detection in seismic data using a true 3D global attention convolutional network with self-supervised denoising pretext training*, Scientific Reports (2026), DOI: [10.1038/s41598-026-54829-x](https://www.nature.com/articles/s41598-026-54829-x).

## Decision

Proceed with Opunake + Kahu as a **two-survey pretraining variant and controlled ablation**. It is scientifically useful, but it is not an exact reproduction of the paper's pretraining corpus. Do not claim that a Dice of 0.853 validation or 0.822 test has been reproduced unless the evaluation protocol and all three surveys also match.

Missing Kerry does not imply that high Dice is impossible. The paper does not publish a leave-one-survey-out experiment, however, so there is no evidence-based numerical penalty that can be assigned to omitting it. The larger risks to exact reproduction are the incompatible public pretraining/fine-tuning architectures, the ambiguous Thebe split, unpublished crop and sampling manifests, inconsistent effective-batch arithmetic, and the absence of the authors' pretrained checkpoint.

## Current transfer state

At 2026-10-23 14:02:44 +04, Kahu was still downloading in the persistent `nzpam` tmux session:

- active output: `data/raw/nz_pretraining/kahu/KAHU-3D-PR3177-T-PSTM-FULL.sgy.part`
- size at that instant: 290,877,440 bytes (about 277.4 MiB)
- expected catalogue size: 5.78 GiB (approximately 6.2 decimal GB)
- final path after successful validation: `data/raw/nz_pretraining/kahu/KAHU-3D-PR3177-T-PSTM-FULL.sgy`

Opunake is complete at `data/raw/nz_pretraining/opunake/OPUNAKE-3D-PR3461-T-PSTM.sgy`:

- 10,377,743,896 bytes (10.378 decimal GB; 9.665 GiB)
- SHA-256: `931bbbb5f2ec50f3eb6f8d65dd1352c982ef842ed103f7427af1ea73c43364ba`
- 1,662,034 traces, 1,501 samples per trace, 4 ms sampling, 0–6000 ms
- 765 inlines and 2,233 crosslines, with 97.29% coverage of the bounding grid
- embedded textual header identifies the final Opunake stack

## What happened with Kerry

The desired historical machine-learning cube is well identified by name: `Kerry3D.segy`. The [SEG Kerry-3D record](https://wiki.seg.org/wiki/Kerry-3D) describes it as an approximately 1 GB final time-migrated volume. Its historical S3 URL now returns HTTP 403.

The current NZP&M catalogue does not expose a proven byte-equivalent replacement:

| Candidate | What the portal exposes | Why it is unresolved |
|---|---|---|
| PR1556, original 1996 Kerry survey | Portal selection about 46.97 GB; current products include a large raw migration | A raw migration package is not demonstrated to be the canonical 1 GB final post-stack cube. |
| PR4184, 2004 reprocessing | Broad portal selection about 158 GB; `KERRY-3D-PR4184-FS` resource is 13.35 GB | Plausible final stack, but it is a later reprocessing and is much larger than `Kerry3D.segy`; no checksum, dimensions, or crop proves identity. |

Choosing the largest package, the newest processing, or a file containing “Kerry” would be guesswork. Downloading 47–158 GB would also consume time and disk without establishing that it is the authors' input.

An email was sent on 2026-10-21 to Matin Mahzad and copied to Majid Bagheri asking for exact filenames, source/resource IDs, byte sizes, checksums, loaded dimensions, crop bounds, and preprocessing. The mailbox was checked directly on 2026-10-23: **there was no reply from either author**. This is a current status, not evidence that they will not reply.

## What each dataset is

| Data | Labels | Learning role | Contents and scale |
|---|---|---|---|
| Opunake-3D | No fault mask | Self-supervised pretraining | Real field 3D post-stack time-migrated seismic amplitudes in SEG-Y; measured local file 10.378 GB. |
| Kahu-3D | No fault mask | Self-supervised pretraining | Real field 3D post-stack time-migrated seismic amplitudes in SEG-Y; expected about 6.2 GB. |
| Kerry-3D | No fault mask | Self-supervised pretraining | Real field final time-migrated seismic volume; canonical public ML copy about 1 GB; exact obtainable object unresolved. |
| Thebe | Expert binary fault mask paired with seismic | Supervised fine-tuning, validation, and test | Real field volume of 1,803 sections, each 3,174 × 1,537 samples; total logical shape is 1,803 × 3,174 × 1,537. The original release uses 900/200/703 sections for train/validation/test. |

The pretraining surveys are **unlabelled**. For an amplitude patch `y`, the method samples Gaussian noise with standard deviation between 5% and 30% of that patch's RMS amplitude, feeds `y + noise`, and trains the network to reconstruct `y`. The target is the original field patch, which can still contain acquisition and processing noise; it is not laboratory-clean ground truth. This is self-supervised because the target is constructed from the input without human fault labels.

Thebe is **supervised binary voxel segmentation**: every target voxel is fault or background. The [dataset publication](https://doi.org/10.1016/j.dib.2021.107219) documents expert annotations and the public NumPy representation. Published descriptions report sparse, line-like masks and the standard 900/200/703 inline split. The local prepared HDF5 subset occupies about 17 GB. Dice is computed on these labels, not on Opunake, Kahu, or Kerry.

SEG-Y itself is a trace format: a textual header, a binary header, then repeated trace headers and amplitude samples. Inline and crossline trace-header values reconstruct a logical array `(inline, crossline, time_sample)`. PDF reports, navigation, velocities, angle stacks, and prestack/raw gathers are not interchangeable with the processed post-stack cube required here.

## What the paper's method combines

The method is a combination of established ideas adapted to volumetric seismic segmentation:

1. **3D U-Net structure.** The encoder, decoder, skip connections, and dense segmentation logic descend from [U-Net](https://arxiv.org/abs/1505.04597), extended from 2D to 3D convolutions.
2. **Unfactorized multi-head self-attention.** The attention equation comes from [scaled dot-product attention](https://papers.nips.cc/paper_files/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html). In the released source, every voxel attends to every other voxel at 64³, 32³, and 16³ feature resolutions; it uses PyTorch fused scaled-dot-product attention to avoid materializing the full score matrix. Compute still grows quadratically with voxel count even when fused memory is reduced.
3. **Denoising representation learning.** Corrupting an input and reconstructing its less-corrupted form follows the [denoising-autoencoder principle](https://mlanthology.org/icml/2008/vincent2008icml-extracting/). Here it is used as domain-specific pretraining on unlabelled field seismic.
4. **Transfer schedule.** Discriminative layer-wise learning rates, gradual unfreezing, and the slanted triangular schedule derive from [ULMFiT](https://aclanthology.org/P18-1031/), transferred from language modelling to this 3D CNN-attention network.
5. **Class-imbalance loss.** [Unified Focal Loss](https://doi.org/10.1016/j.compmedimag.2021.102026) combines focal cross-entropy and focal Tversky terms. That is relevant because faults occupy only a small fraction of Thebe voxels.
6. **Seismic segmentation lineage.** [FaultSeg3D](https://doi.org/10.1190/geo2018-0646.1) established end-to-end 3D binary fault segmentation trained on synthetic seismic/fault pairs. Attention3D changes the representation and transfer strategy and fine-tunes on real labelled Thebe data.

The scientific hypothesis is coherent: convolutions learn local reflector discontinuities; global attention connects distant voxels on the same fault plane; denoising pretraining exposes the network to real seismic texture before scarce labels; and focal/Tversky terms limit domination by background.

## What the reported scores establish

The final Scientific Reports paper reports the following Thebe validation ablation:

| Configuration | Validation Dice |
|---|---:|
| Baseline 3D CNN | 0.789 |
| Global attention only | 0.821 |
| Denoising pretraining only | 0.809 |
| Unified Focal Loss only | 0.803 |
| Global attention + denoising pretraining + Unified Focal Loss | 0.853 |

The full method reports validation Dice 0.853 and held-out test Dice 0.822. These numbers support the value of the complete package under the authors' protocol. They do not isolate Kerry: there is no Kerry-only, Opunake+Kahu, or leave-one-survey-out row.

The pretext-only row improved validation Dice by 0.020 over the authors' 0.789 baseline. The full method improved it by 0.064, so the final gain cannot be attributed to the three-survey corpus alone. Interactions among attention, pretraining, loss, split, and optimization matter.

## Can Opunake + Kahu still reach high Dice?

**Possible: yes. Demonstrated or guaranteed: no.**

- The paper states 64³ sub-volumes with 50% overlap (stride 32). Applying that rule to the published canonical dimensions gives about 5,586 unique Kerry windows and 39,015 Kahu windows. Opunake gives about 42,126 windows using a commonly published historical geometry, or 67,320 using the currently verified local grid. Under exhaustive enumeration, Kerry contributes only about **5.0-6.4%** of unique three-survey windows.
- This patch-count result supports the original approximate 5.8% file-size estimate. It is more relevant than byte size because it follows the model's declared extraction geometry.
- No equal-survey sampler is documented. Equal sampling remains technically possible, but there is no evidence that the authors used it and it should not be the main assumption. The denoising repository contains only `GlobalAttention3D.py` and `README.md`; it contains no dataset, sampler, or training implementation.
- Kerry's plausible contribution is therefore mainly a small amount of distinct geology and a third acquisition/processing/noise distribution, rather than a large fraction of training patches. No published ablation converts that contribution into a Dice change.

### What geological variety Kerry adds

Kerry covers the Kupe inversion structure in the southern Taranaki Basin. [Published structural reconstruction](https://shareok.org/items/1c5d9acf-ffe6-44d7-b308-739f23b6fac8) describes a Cretaceous extensional fault system later reactivated by Oligocene-Miocene compression. The volume contains the reverse-faulted Manaia inversion anticline, overlapping Manaia and Rua fault systems, normal and reverse faults in several orientations, fault-propagation/fault-bend folding, and many secondary fault planes. Other work reports [steep en-echelon normal faults and gas-related anomalies](https://gsnz.org.nz/assets/Uploads/Shop/Products/GSNZ_annual_conference/MP124_2008_Wellington/MP124A_2008_GSNZ_conference_Wellington_abstract_volume.pdf), [crossing or closely spaced faults with small offsets](https://pure.unileoben.ac.at/files/3369722/AC15246471n01.pdf), and [subtle faults with little visible displacement](https://www.mdpi.com/2079-9292/14/15/3078).

This differs usefully from the other two surveys:

- [Opunake](https://wiki.seg.org/wiki/Opunake-3D) is dominated by a large extensional normal-fault system and contains incoherent noise and attenuated middle/deep reflectors.
- [Kahu](https://pubs.geoscienceworld.org/gsa/geosphere/article/11/2/266/132203/Spatial-patterns-of-deformation-and-paleoslope) includes faults together with the North Awakino mass-transport deposit and soft-sediment deformation in volcaniclastic sandstone/mudstone sequences.
- Kerry adds inversion/compressional structure, reverse-fault geometry, intersecting multi-orientation fault networks, subtle low-displacement fractures, and a separate 1996 acquisition plus later processing history.

All three surveys are still from the Taranaki Basin. Kerry broadens within-basin structural and noise diversity; it does not provide cross-basin diversity. There is no accepted scalar measure of “geological variety,” and the paper reports no feature-distribution or leave-one-survey-out analysis. The defensible numerical proxy is therefore 5.0-6.4% of unique sliding windows, plus one of three survey-level acquisition/processing domains.

The most responsible expectation is that a score above 0.80 may be attainable because the authors report 0.821 for global attention alone and other Thebe studies also achieve strong overlap/boundary scores. This is a research target, not a prediction. Reaching exactly 0.853 validation or 0.822 test depends on much more than adding Kerry.

## Evidence from other work and what it means

| Study | Relevant finding | Consequence for this experiment |
|---|---|---|
| [FaultSeg Swin-UNETR, Remote Sensing 2024](https://www.mdpi.com/2072-4292/16/5/922) | On Thebe, full-network SimMIM pretraining raised OIS/ODS from 0.851/0.847 without pretraining to 0.875/0.870. Its unlabelled pretraining corpus is private. | Independent support that seismic-domain self-supervision can help. OIS/ODS are boundary metrics, not Dice, so the numbers cannot be ranked directly against 0.853 Dice. |
| [Large-scale fault delineation benchmark, 2025/2026 revision](https://arxiv.org/abs/2505.08585) | More than 200 model/data/training combinations show strong effects from domain shift, catastrophic forgetting, fine-tuning strategy, and inconsistent evaluation protocols. | More pretraining data does not automatically improve a target. Domain match and transfer procedure must be tested rather than assumed. |
| [Thebe dataset paper](https://doi.org/10.1016/j.dib.2021.107219) | Provides real seismic plus expert fault annotations and a public benchmark, but annotations reflect an interpretation workflow rather than exhaustive physical truth. | Dice measures agreement with this mask. Visual/geological review and boundary/distance measures should accompany overlap scores. |
| [Unified Focal Loss](https://doi.org/10.1016/j.compmedimag.2021.102026) | Demonstrates improved robustness on multiple class-imbalanced 2D/3D medical segmentation datasets. | The loss has a sound imbalance rationale, but its seismic benefit still requires the paper's own ablation and our matched local control. |

The local short pilot is not evidence against the paper. It used Thebe itself for only 256 pretraining patches/64 optimizer updates, fixed 10% RMS corruption, and 512 supervised patches/128 updates. Its pretrained Dice (0.0701) was below scratch (0.0776), but the task, data source, duration, and protocol differ too much to estimate the full experiment.

## Remaining reproduction requirements separate from Kerry

1. The authors' separate denoising release has four encoder stages, while the imported segmentation source has two encoder stages. A checkpoint cannot be assumed compatible without an exact architecture or verified tensor mapping.
2. The paper describes a 60% development / 40% held-out Thebe division, with a 70/30 split inside development. The established public Thebe protocol is 900/200/703 sections. Exact coordinates must be reconciled before comparing scores.
3. No author patch manifest, crop bounds, volume orientation, missing-bin treatment, normalization details, or survey-sampling probabilities are published.
4. The configuration says batch 2 × accumulation 4 × 4 GPUs and calls the effective batch 16; the arithmetic is 32 unless another convention is being used.
5. The public repository advertises files that are absent and supplies no pretrained denoising checkpoint. The released monolithic segmentation source alone is insufficient for byte-for-byte reproduction.
6. The paper used four RTX 4090 GPUs. The local RTX A5500 can support a carefully adapted run, but distributed execution and optimizer-step semantics will differ.

Most of these are tractable engineering decisions for a transparent local reproduction variant: use one architecture for both stages, publish the chosen spatial split and patch manifest, define an internally consistent effective batch, and record the single-GPU adaptation. They prevent a claim of byte-for-byte or author-execution equivalence, but they do not prevent beginning the complete controlled Opunake+Kahu experiment after Kahu is verified. Obtaining Kerry alone would not resolve the undocumented author choices.

## Experiment that supports a publishable conclusion

Use one frozen Thebe split, one implementation, equal optimizer-update budgets, and the same patch manifest rules for every arm:

| Arm | Initialization | Purpose |
|---|---|---|
| A | Random | Required scratch control. |
| B | Opunake denoising | Measures one-survey transfer. |
| C | Kahu denoising | Measures the other survey independently. |
| D | Opunake + Kahu denoising | Main available-data result. |
| E | Kerry + Opunake + Kahu, only if exact Kerry is later verified | Closest paper-corpus reproduction and direct estimate of Kerry's marginal effect. |

Run at least three seeds per arm if compute allows. For B–E, equalize the number of optimizer updates; also report whether patches are survey-balanced or volume-proportional. That prevents “more surveys” from being confounded with “more gradient steps.”

Freeze the selected configuration before the held-out test. Report Dice, IoU, precision, recall, F2, MCC, and a boundary/distance measure, plus full-volume visual sections. Use 64³ patches, stride 32, and Gaussian overlap blending as described by the target paper. Report both the fixed 0.5 threshold and any validation-selected threshold clearly; never tune on the test region.

Until arm E exists, describe arm D as:

> A two-survey reproduction variant of Mahzad and Bagheri's denoising-pretrained Attention3D method, using the verified Opunake-3D and Kahu-3D post-stack PSTM volumes; Kerry-3D was omitted because the canonical approximately 1 GB object could not be matched unambiguously to current NZP&M resources.

That statement is accurate, reviewable, and still supports a strong experiment. A claim of exact paper replication would not be accurate.

## Local evidence

- Dataset mapping: `reports/experiments/ATTENTION3D_NZPAM_DATASET_MATCH_20261021.md`
- Reproduction readiness: `reports/experiments/ATTENTION3D_REPRODUCTION_READINESS_20261023.md`
- Reproduction audit: `reports/experiments/ATTENTION3D_REPRODUCTION_AUDIT_20261021.json`
- Verified Opunake audit: `reports/data_audit/OPUNAKE_VERIFICATION_20261023.md`
- Authors' source snapshot: `external/attention3d_paper/`
- Short local pilot: `runs/attention3d_denoising_pilot_20261019_v2/report.md`

