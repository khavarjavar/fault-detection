# Open source fault methods and a joint experiment for Thebe

**Broader follow-up:** [Swin-UNETR, 2.5D/SAM, new paired fault–RGT data, five-seed evidence and frozen test visualizations](BROADER_MODELS_DATA_AND_R100_VISUAL_REVIEW_20261102.md). The FaultSegV3 study below is one option rather than the full architecture shortlist.

**Research date:** 2026-11-02 (Asia/Baku)  
**Task:** detect geologic fault surfaces in 3D reflection seismic, using the local Thebe fault labels and the existing held-out evaluation protocol.

## Decision

Run a matched **FaultSegV3 fine-tuning study**, first with seismic amplitude alone and then with a fault-sensitive structural attribute. Compare each arm with the existing R100 and FaultEdgeFormer results on the same complete validation and frozen test grid. The released zero-shot checkpoint is an informative baseline but does not currently transfer well to Thebe. Keep porosity/property prediction as a separate hypothesis until matching well logs or pre-stack data exist.

## The supplied video/channel lead

The Bing video URL did not expose a stable video page to the research tools, so its exact item could not be verified. The channel ID points to Ruslan Miftakhov's [YouTube channel](https://www.youtube.com/channel/UC1HyCbG5SO4hC7b_Ddl8cGg/videos). His own posts identify two relevant tutorials: [Fault Detection Made Easy](https://www.linkedin.com/posts/ruslan-miftakhov_run-latest-fault-prediction-code-on-your-activity-7020995166161227776-sxXI), which describes sparse 2D-label training and links to Yimin Dou's [FaultNet](https://github.com/douyimin/FaultNet), and [3D Fault Detection on Your Data](https://www.linkedin.com/posts/ruslan-miftakhov_test-out-3d-fault-detection-on-your-data-activity-7003717775516930051-PDsg), which demonstrates his [EFramework](https://github.com/RMiftakhov/EFramework) wrapper for FaultSeg3D and FaultNet. A related post points to [Thilo Wrona's seismic deep learning tutorials](https://github.com/thilowrona/seismic_deep_learning), which cover faults, horizons, and salt.

The channel is therefore useful for finding implementations and visual workflows. The underlying model repositories and their papers are the better source for experimental settings and claims.

## Ranked source inventory

| Source | What is actually available | Fit to our project | Use |
|---|---|---|---|
| [FaultSegV3](https://github.com/douyimin/FaultSegV3) | 3D high-resolution model, included checkpoint and inference; about 0.563M parameters. Training entry point is incomplete in the current clone. | **High**: direct 3D fault mask, successful local inference on the RTX A5500 | Matched scratch/pretrained fine-tuning arms using a local trainer. Its released field demo uses 2x scaling, so native-scale results below are specifically native-scale. |
| [FaultNet / MD loss](https://github.com/douyimin/FaultNet) | Apache-2.0 source, three scripted inference checkpoints (`gamma` 0.5/0.6/0.7), sparse-label method description | **High** for the channel lead; training implementation is not included in this clone | Zero-shot comparator now; sparse-label training later requires an independently implemented training loop. |
| [FaultSSL](https://github.com/douyimin/FaultSSL) | Apache-2.0 checkpoint and inference, mean-teacher/overlap-consistency method | **High** for the unlabeled Opunake/Kahu volumes; released repo mainly supports prediction | Later semi-supervised arm after a strong supervised baseline. |
| [CIG-Bench](https://github.com/douyimin/CIG-bench) | MIT inference library and pretrained fault, relative-geologic-time (RGT), geobody and well-conditioned property predictors | **High** as an independent fault baseline; **medium** for RGT as a structural feature | Benchmark fault predictor; test whether RGT discontinuities or horizon mismatch add information to Thebe fault segmentation. |
| [Hale's IPF](https://github.com/dhale/ipf) and [optimal surface voting](https://github.com/xinwucwp/osv) | Classical fault likelihood, strike/dip, thinning, skins and surface voting; older processing stack | **High scientific relevance**, more integration work | Non-neural comparator and post-processing hypothesis for coherent surfaces. |
| [SeismicFlowCore](https://github.com/SeismicFlow/SeismicFlowCore) | Cython implementations of local variance and GST coherence among other 3D attributes | **High** as a structural input; needs build and independent numerical check | Compute an attribute on train/validation/test consistently; compare amplitude-only with amplitude+attribute. |
| [NCS seismic foundation models](https://github.com/NorskRegnesentral/NCS_models) | Apache-2.0 2D, 2.5D and 3D seismic-pretrained ViT code/weights and feature extraction pipeline | **Medium**: seismic domain is right, but weights yield features, not fault masks | Later frozen-feature/segmentation-head study. The 2.5D model is the practical first ViT candidate. |
| [GeoFWI3D](https://github.com/aaspip/geofwi3d) | CC BY 4.0 synthetic p-reflectivity, velocity, RGT and fault-index volumes on the same 3D grid | **High** for a paired fault+RGT pretraining test, **low** as a direct Thebe substitute | Compare fault-only with fault+RGT pretraining on its `image3d.bin`; p-reflectivity is a proxy for seismic, so any transfer gain must be measured on field Thebe. |
| [Seis2Rock](https://github.com/DeepWave-KAUST/Seis2Rock) | MIT pre-stack seismic-to-petrophysical inversion code and well-log experiments | **Low now**: our Thebe HDF5 contains post-stack amplitude and fault labels, not matching pre-stack gathers/well logs | Revisit only if co-registered well logs and suitable gathers are obtained. |

Other leads were screened out of the immediate experiment. [SCF](https://github.com/lanl/scf) explicitly uses seismicity locations as an additional input, which Thebe does not provide. The [GeoSSL paper](https://www.geophysical-press.com/journal/JSE/35/2/10.36922/JSE025510127) proposes masked reconstruction and attribute contrast but I did not verify a public implementation. Earthquake waveform/event detectors such as SeisLM or Qseek address a different seismic task.

## Local feasibility check

Thebe is already prepared as nine training HDF5 blocks, two validation blocks, and seven held-out test blocks. The established full-grid protocol uses 128-cubed tiles, reversal to model axis order, and scores only voxels with nonzero raw seismic. The existing [comparison report](../evaluation/attention3d_faultedgeformer_comparison_20261028/report.md) gives validation Dice 0.563981 for FaultEdgeFormer and full test Dice 0.574603; the R100 three-model ensemble gives full test Dice 0.581257. These test values are context, never inputs to new checkpoint or threshold selection.

The released FaultSegV3 checkpoint was loaded with PyTorch `weights_only=True` and evaluated through [the validation-only adapter](../../scripts/evaluate_faultsegv3_validation.py). The run covered all 650 validation tiles, 450 observed tiles, and exactly 613,738,550 valid voxels. It used raw amplitudes, the released per-tile z-score/clip/min-max preprocessing, 128-cubed native-scale inference, and the same mask and pooled 2,048-bin metric code as R100. The channel-referenced FaultNet `gamma=0.7` checkpoint was evaluated by [its validation adapter](../../scripts/evaluate_faultnet_validation.py) on precisely the same scoring population. Its block normalization was computed in float32 before the author's half-precision model input. Saved evidence: [FaultSegV3](../evaluation/faultsegv3_complete_validation_20261102/result.json), [FaultNet](../evaluation/faultnet_gamma07_complete_validation_20261102/result.json), and the earlier [R100 validation ensemble](../evaluation/r100_ensemble_e0_20261016T120152Z/validation_result.json).

| Model | Complete validation Dice | PR-AUC | ROC-AUC | Validation-selected threshold |
|---|---:|---:|---:|---:|
| FaultSegV3 checkpoint, zero shot, native scale | 0.120286 | 0.044963 | 0.608230 | 0.999512 |
| FaultNet `gamma=0.7` checkpoint, zero shot | 0.171366 | 0.057326 | 0.614540 | 0.999512 |
| Existing Thebe-trained R100 three-model ensemble | 0.588951 | 0.616182 | 0.964916 | 0.274902 |

Both zero-shot models are weak on this validation survey despite being valid open-source leads. Their thresholds are at the highest bin, which is a strong domain/calibration warning; it does not show whether fine-tuning helps. The source's F3 demo upscales 2x, while the local FaultSegV3 native-scale protocol preserves Thebe voxel spacing and grid. A scale sensitivity check belongs on validation if needed. FaultNet's other two released gamma checkpoints were not tested. The FaultSegV3 clone at commit `b0e62ee1752e966ab182c5b2ed5ed08cff22ed02` has no repository-wide LICENSE file, although its README references a `LICENSE-CIG-Bench` file that is absent from the clone. Use the code for local research; clarify redistribution terms before including its source or weights in a public release.

The same clone's `train.py` imports `seisDataset.dataset`, but `seisDataset` contains only `__init__.py`, and local `pytorch_lightning` is absent. The released training command is therefore not runnable here as-is. The local R100 trainer already supplies the Thebe HDF5 reader, sampling, validity mask, metric accumulator, checkpoint provenance, and validation protocol. A FaultSegV3 training adapter should reuse those pieces and use the V3 model directly with a fixed masked loss. A [single 128-cubed Thebe training-step preflight](../../scripts/preflight_faultsegv3_thebe_training.py) completed forward, backward, and AdamW update with finite loss `0.858403`, nonzero parameter change, and **2.173 GiB peak allocated GPU memory**. [Preflight evidence](../evaluation/faultsegv3_training_preflight_20261102.json) confirms basic trainability and memory fit; it does not validate a training schedule or convergence. Building the resumable matched trainer remains the next implementation step before launching the four-arm study.

Both complete validation passes checked geometry and exact validity/positive counts; neither opened held-out test files. The first one-tile smoke tests passed model execution but happened to contain zero positive labels, so their accuracy values were not used as evidence.

## Proposed joint experiment

1. **Direct transfer screen.** Complete validation-only zero-shot checks of FaultSegV3, FaultNet, and the CIG-Bench fault predictor. Keep all three source checkpoints fixed; do not use test labels to choose scales, thresholds, or model order. A weak zero-shot model is still useful for studying domain shift, but should not be fused into the current ensemble by assumption.
2. **Matched supervised transfer.** Build the resumable local FaultSegV3 trainer from the existing Thebe reader; the 128-cubed forward/backward memory check has passed. Train FaultSegV3 from random initialization and from its released weights on the same nine Thebe train blocks, patch sampler, augmentations, update budget, and seeds. Use full `val1+val2` for checkpoint and threshold selection. A seed-42 pilot checks learning and resource use; three matched seeds quantify variability before comparing with R100.
3. **Structural attribute arm.** Compute one coherence/semblance or local-variance volume using train-only parameter selection. Add it as a second input channel to both FaultSegV3 initializations. Compare four arms: amplitude/scratch, amplitude/pretrained, amplitude+attribute/scratch, amplitude+attribute/pretrained. Check whether apparent gains are from the attribute, initialization, or their interaction. For pretrained two-channel models, copy the amplitude input weights and initialize only the new channel; record that rule.
4. **Frozen evaluation.** Select the final checkpoint, threshold, and any ensemble weights on complete validation. Then run one full seven-block test pass with the existing validity mask and pooled Dice, PR-AUC, ROC-AUC, MCC, precision and recall. Report inference cost and per-block variation; add a boundary-tolerant fault score only if its definition is frozen before the test pass.

The porosity idea can be tested later as a controlled auxiliary signal, but it is not automatically a proxy for fault geometry. The local files do not provide co-registered porosity targets or sparse wells. [CIG-Bench property prediction](https://github.com/douyimin/CIG-bench) conditions on well-property samples; [Seis2Rock](https://github.com/DeepWave-KAUST/Seis2Rock) uses pre-stack data and wells. RGT and reflector discontinuity are closer to the visible fault evidence in the current amplitude cube.

## Reproduction commands

From the project root:

```bash
.venv_train/bin/python -u scripts/evaluate_faultsegv3_validation.py \
  --output reports/evaluation/faultsegv3_complete_validation_20261102

.venv_train/bin/python -u scripts/evaluate_faultnet_validation.py \
  --output reports/evaluation/faultnet_gamma07_complete_validation_20261102 \
  --gamma 0.7
```

Both commands refuse to overwrite existing evidence. To rerun, choose new output directories. Both only enumerate `val1.h5` and `val2.h5`; neither opens a test block.

The training memory check uses only `train1.h5` through `train9.h5`:

```bash
.venv_train/bin/python -u scripts/preflight_faultsegv3_thebe_training.py
```

It writes its single-step evidence file once and then refuses to overwrite it.
