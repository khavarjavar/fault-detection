# Attention3D reproduction readiness (2026-10-23)

## Decision

Work can continue while another person retrieves the surveys. The download is
only the first blocked input. A faithful run also needs a verified SEG-Y
ingestion path, the compatible denoising architecture/checkpoint format, the
exact pretraining recipe, a paper-consistent Thebe split, and overlapping
full-volume inference.

The three survey names are not guesses: the publication explicitly says that
the denoising backbone was pretrained on **Kerry-3D, Opunake-3D, and Kahu-3D**.
The mapping from the historical filenames to the current NZP&M product IDs is
high-confidence but not yet author-confirmed.

## Why these surveys fit the method

The pretext stage is self-supervised. It needs seismic amplitudes and does not
need fault labels. Each selected input should be a field-acquired **3D
post-stack seismic amplitude volume**:

| Property | Why it matters |
|---|---|
| 3D regular seismic cube | Supplies inline, crossline, and time/depth axes for true volumetric patches. |
| Post-stack | Gives one amplitude value per spatial/time voxel rather than prestack shot/offset gathers. |
| Time-migrated/final stack | Reflectors and faults are positioned as spatially coherent structures, matching the denoising and downstream segmentation inputs. |
| Unlabelled field data | Sufficient for corrupt-input/original-target denoising; no fault mask is needed. |
| Three different surveys | Exposes the model to different geology, acquisition footprints, processing histories, and noise distributions. |

For every clean field patch `y`, the published task adds Gaussian noise with
standard deviation sampled from **5% to 30% of that patch's RMS amplitude** and
trains the network to reconstruct `y`. The target still contains natural field
noise; it is a less-corrupted target, not laboratory-clean ground truth. The
paper's rationale is that reflectors, stratigraphy, and faults recur coherently
in space, while injected random noise does not. Multi-survey variation is
intended to prevent the model from memorizing one survey's noise pattern.

The network then transfers those features to labelled Thebe fault
segmentation. The intended benefit is fewer noise-induced false fault
predictions and better preservation of coherent fault planes.

## Expected files and internal structure

| Survey | Target product | Expected role |
|---|---|---|
| Opunake | `OPUNAKE-3D-PR3461-T-PSTM` | Processed post-stack time-migrated 3D amplitude cube; current counterpart of historical `Final_Stack`. |
| Kahu | `KAHU-3D-PR3177-T-PSTM-FULL` | Full processed post-stack time-migrated 3D amplitude cube; current counterpart of historical `Final_Migration`. |
| Kerry | Historical `Kerry3D.segy`, about 1 GB | Third post-stack 3D amplitude cube; exact current source remains unresolved. |

A SEG-Y file normally contains a 3200-byte textual header, a 400-byte binary
header, and one trace header plus amplitude samples for each trace. For a
regular 3D post-stack survey, trace headers identify inline and crossline bins,
and each trace contains the time samples at that bin. After ingestion the model
should see one numeric array with logical shape:

```text
(inline, crossline, time_sample) -> one seismic amplitude per voxel
```

The NZP&M packages may contain ZIP wrappers, ancillary navigation, reports, or
multiple SEG-Y files. Only the processed PSTM amplitude cube belongs in this
pretraining input. Raw PSTM, angle stacks, velocity files, navigation files,
and PDF reports are different products and must not be silently mixed into the
cube.

Before training, each received file must be audited for:

- SHA-256 and byte size;
- SEG-Y sample format, endianness, sample count, and sample interval;
- inline/crossline header locations and coordinate ranges;
- unique grid dimensions, duplicate traces, missing bins, and trace sorting;
- finite amplitudes, zero/mute regions, and amplitude statistics;
- axis order/orientation and any author-specified crop bounds.

## Readiness checklist

| Area | Status | Required result |
|---|---|---|
| Survey identity | Partial | Opunake and Kahu mappings are high-confidence; Kerry and exact author-used bytes await confirmation. |
| Secure retrieval | Assigned externally | Download to `data/raw/nz_pretraining/`; retain original archives and record hashes. |
| Disk | At risk | Shared filesystem has about 142 GB free and is 95% full. Reserve at least 60-80 GB for archives, extracted SEG-Y, processed arrays, checkpoints, and temporary files. Do not download a 158 GB Kerry selection. |
| SEG-Y support | Ready | Installed `segyio==1.9.14` and `PyYAML==6.0.3` in `.venv_train`; versions are pinned in `configs/attention3d_data_requirements.txt`. |
| Survey ingestion | Complete for Opunake + Kahu | Streaming conversion and source-trace equality checks passed; see `ATTENTION3D_TWO_SURVEY_EXECUTION_20261026.md`. Kerry remains unavailable. |
| Pretext patch source | Complete for two-survey variant | Frozen 64x64x64/stride-32 manifest has 81,675 eligible train cubes and 9,810 spatially held-out validation cubes. |
| Pretext normalization | Frozen local choice | Per-survey global z-score over finite amplitudes on present traces; missing bins are excluded from eligible cubes. Exact author treatment remains unpublished. |
| Pretext corruption | Implemented | Gaussian sigma is drawn uniformly from 0.05-0.30 times each normalized patch RMS; target is the uncorrupted field patch. |
| Denoising validation | Implemented | Fixed spatially separated cubes compare network MSE against noisy-input identity MSE. |
| Architecture transfer | Resolved for named variant | The same released 45,001,057-parameter segmentation network is used in both stages and its output head will be reset. This is compatible locally but differs from the separate four-level denoising release. |
| Fine-tuning model/loss | Mostly present | Imported 45,001,057-parameter model and Unified Focal Loss exist locally. Production wrapper still needs paper-consistent transfer, layer groups, and resumable state. |
| Thebe data | Prepared, split must be reconciled | Seventeen GB of HDF5 files exist. Map them exactly to the paper's inline-based 60/40 split and 70/30 development split; do not substitute the R100 protocol. |
| Fine-tuning schedule | Partly present | Implement/verify AdamW, LLRD 0.95, unfreezing at epochs 0/10/20/30, STLR 10% warm-up and ratio 32, clipping 1.0, maximum 100 epochs, patience 20. |
| Effective batch | Unresolved | Public config says batch 2 x accumulation 4 x 4 GPUs but labels it 16; the arithmetic is 32. Authors must clarify scheduler and optimizer-step semantics. |
| GPU | Usable with adaptation | One RTX A5500 with 24 GB is available; the paper config states four RTX 4090 GPUs. Batch 1, checkpointing, and accumulation may fit but will not reproduce the distributed execution exactly. |
| Numerical path | Available | PyTorch 2.7.1+cu118 and BF16-capable local training work. Paper specifies FP16 forward with FP32 loss/optimizer; run a finite-gradient and memory smoke test before the full job. |
| Full-volume inference | Missing for this protocol | Implement 64-cube inference at stride 32 with Gaussian-weighted overlap blending and boundary coverage checks. |
| Frozen evaluation | Needs Attention3D-specific implementation | Freeze checkpoint and threshold 0.5, then compute Dice, IoU, precision, recall, specificity, F2, MCC, balanced accuracy, and kappa on the untouched test region. |
| Provenance/resume | Partly present | Save code/config hashes, data hashes, patch manifests, RNG states, optimizer/scaler/scheduler state, transfer report, histories, and atomic resumable checkpoints. |

## Already available locally

- Imported public segmentation source and its verified hash.
- A working 64-cube Attention3D path and successful single-GPU pilot.
- BF16 finite-value checks, gradient clipping, feature-transfer checks, and
  deterministic patch manifests from the pilot infrastructure.
- Prepared Thebe HDF5 volumes (about 17 GB).
- Unified Focal Loss and the published fine-tuning configuration.
- A completed R100 frozen evaluation framework that provides useful integrity
  patterns, although its 128-cube partition, zero mask, tuned thresholds, and
  checkpoints must not be reused as the Attention3D protocol.
- A read-only SEG-Y/archive auditor, validated on a synthetic 2x3x4 regular
  cube, plus pinned `segyio` and `PyYAML` ingestion dependencies.

## Work to complete while data retrieval proceeds

1. **Completed:** add pinned SEG-Y/YAML dependencies and validate the read-only
   SEG-Y inventory/audit tool on a synthetic regular 3D cube.
2. After the first real-file audit, implement streaming conversion with explicit `(inline, crossline, time)`
   metadata and an immutable input manifest.
3. Implement the paper's multi-survey 64/32 pretext patch index and variable
   5-30% RMS noise corruption.
4. Implement Gaussian overlap blending and verify that a constant prediction
   remains constant after stitching and every voxel is covered.
5. Build a production training configuration with resume support and a short
   single-GPU memory/finite-gradient smoke test.
6. Gate the expensive run on author confirmation of survey bytes/crops,
   backbone compatibility, Thebe split coordinates, and effective batch rules.

## Storage fidelity decision

Storage efficiency must not change the scientific protocol. The checked author
repository describes the pretraining inputs as three survey-level `.npz` files,
not a directory containing one file per 64-cube. Its available segmentation
dataset stores patch coordinates and slices each overlapping cube from the
loaded volume in `__getitem__`. The pretraining entry point advertised by the
repository is absent, so the exact pretraining storage implementation remains
unpublished.

The local reproduction variant will therefore preserve complete survey-level
arrays plus an immutable coordinate manifest and will extract the documented
64x64x64, stride-32 cubes from those arrays. This choice follows the available
author code rather than using disk limits to alter sampling. If later author
evidence shows that pretraining materialized individual cube files, reproduce
that layout and request the required storage before conversion.

## Evidence and limits

- Published method: <https://pmc.ncbi.nlm.nih.gov/articles/PMC13434476/>
- Authors' segmentation repository:
  <https://github.com/Matin-Mahzad/fault-detection-global-attention>
- Authors' separate denoising repository:
  <https://github.com/Matin-Mahzad/3D_Global_Attention>
- Local dataset mapping:
  `reports/experiments/ATTENTION3D_NZPAM_DATASET_MATCH_20261021.md`
- Local reproduction audit:
  `technical_reports/11_attention3d_full_reproduction.md`

The publication establishes the three survey identities and the post-stack
denoising methodology. It does not establish that the present NZP&M resource
objects are byte-identical to the authors' historical files. That claim must
remain conditional until checksums, shapes, bounds, or author confirmation are
available.
