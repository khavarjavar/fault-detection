# Attention3D full reproduction: verified steps and missing inputs

Checked: 21 October 2026. Status: source audit complete; faithful training has not started.

The objective is to reproduce the published method. Experiment 10 remains a short Thebe adaptation. Its checkpoints do not establish completion of this reproduction.

The paper reports validation Dice **0.853** and test Dice **0.822**. These are separate targets, not guaranteed outcomes.

## Steps in plain language

1. Obtain the original pretraining surveys and the matching model code.
2. Normalize the seismic and extract 64-cube patches at stride 32.
3. Add Gaussian noise at 5–30% of patch RMS and train reconstruction of the original field input.
4. Transfer the denoising checkpoint into fault segmentation.
5. Fine-tune on the original Thebe partitions with Unified Focal Loss and discriminative learning rates.
6. Select the checkpoint on validation Dice, using the original stopping rule.
7. Blend overlapping predictions with Gaussian weights and score at probability greater than 0.5.

Source: [published methodology, training, and evaluation](https://www.nature.com/articles/s41598-026-54829-x).

## Settings to preserve

| Setting | Published value |
|---|---|
| Pretraining surveys | Kerry-3D; Opunake-3D; Kahu-3D |
| Thebe split | 60% development / 40% test; development split 70/30 |
| Peak LR / depth decay | 0.0005 / 0.95 |
| Unfreezing epochs | 0, 10, 20, 30 |
| LR warm-up / ratio | 10% / 32 |
| Optimizer / weight decay | AdamW / 0.0001 |
| Maximum epochs / patience | 100 / 20 |
| Forward / loss precision | FP16 / FP32 |
| Gradient clipping | 1.0 |

Exact spatial bounds, source/checkpoint compatibility, and effective batch size still need confirmation. Do not substitute the existing R100 partitions or its validation-selected threshold.

## What the source check found

- The main repository advertises `pretrain_denoising.py`, but the checked file tree does not include it or the requested `model_epoch_4.pt`. The supplied entry point starts by loading that checkpoint.
- Its example uses a random 80/20 patch split. That differs from the published split. Overlapping patches also require care when interpreting spatial separation.
- The separate denoising release has four encoder stages. Our imported segmentation source has two. Their tensor names and attention implementations also differ. A shared class name or approximate parameter count does not prove checkpoint compatibility.
- The supplied training loop updates the optimizer every batch. It does not implement the stated four-step accumulation in that loop.
- The reported hardware, per-device batch, and accumulation imply 4 × 2 × 4 = 32 samples per update, while the article states 16. Scheduler steps versus optimizer updates also need clarification.
- The full denoising article is subscription content at the checked publisher page. Its abstract is accessible, but that does not supply a complete training recipe.

Sources: [segmentation repository](https://github.com/Matin-Mahzad/fault-detection-global-attention), [released entry point](https://github.com/Matin-Mahzad/fault-detection-global-attention/blob/main/fault-detection-global-attention.py), [separate denoising model](https://github.com/Matin-Mahzad/3D_Global_Attention/blob/main/GlobalAttention3D.py), [denoising article](https://link.springer.com/article/10.1007/s13369-025-10974-5).

Local execution source: `external/attention3d_paper/fault-detection-global-attention.py`; commit `2a3d69a5d99dfc191508cbceea3db3b95242f216`; SHA256 `dc332c431b035c590141f0e542573d9445dfdae65a232cbe799516be8df18b37`. This identifies our imported source, not proof that this revision generated the publication's results.

## Work that comes next

The [author email draft](../reports/experiments/ATTENTION3D_AUTHOR_EMAIL_DRAFT_20261021.md) requests the missing recipe, exact data coordinates, compatible checkpoints, and resolved batch settings. It has not been sent.

No survey-named candidates were found by filename under local `data/`. The earlier pilot audit also recorded that the original surveys and weights were unavailable locally. This search does not rule out files stored elsewhere or under unrelated names. Public New Zealand data access exists, but the exact processed products and crop bounds used by the authors are not identified by that fact alone. [Official data access](https://www.nzpam.govt.nz/maps-geoscience/petroleum-datapack).

When the inputs are identified, record file checksums, axes, units, label version, crop bounds, normalization, and the scored region. Verify checkpoint keys and shapes before a forward pass. Test the reconstruction target, finite gradients, layer groups, unfreezing, accumulation, and the learning-rate trajectory on a short run. Check that stitched constant predictions remain constant and every intended voxel is covered. Then run pretraining and fine-tuning in a new run folder with resumable optimizer, scaler, scheduler, and RNG state.

If the authors provide the final checkpoint, first evaluate it under their protocol. That separates evaluation mismatches from training mismatches before a costly retraining run. A supplied denoising checkpoint can verify fine-tuning sooner, while reproducing pretraining remains a separate unfinished stage.

The [machine-readable audit](../reports/experiments/ATTENTION3D_REPRODUCTION_AUDIT_20261021.json) records the unresolved inputs. No new GPU training or held-out test inference was launched for this audit.

## Why accuracy and Dice differ

Accuracy counts correctly identified background voxels. Foreground Dice/F1 does not reward true negatives.

`Accuracy = (TP + TN) / (TP + TN + FP + FN)`

`Dice = F1 = 2TP / (2TP + FP + FN)`

Recomputed from the frozen R100 ensemble counts:

| Prediction | Accuracy | Dice/F1 |
|---|---:|---:|
| Predict background everywhere | 97.4958% | 0 |
| Trained three-seed R100 ensemble | 97.6069% | 0.581257 |

Only 2.5042% of the scored voxels are labeled faults. Background dominates accuracy, while Dice measures the balance of fault overlap, false alarms, and misses. Dice is not the percentage of complete fault planes found.

Evidence: [frozen counts and metrics](../reports/evaluation/r100_clean_frozen_test_20261019/final_metrics.json). TP = 38,256,762; FP = 35,697,272; FN = 19,423,734; TN = 2,209,963,785. Independent arithmetic reproduced the saved accuracy and Dice, and confirmed Dice equals binary F1.
