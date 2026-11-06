# Next working day experiment tracker

## Current status — 2026-11-04 11:11 +04

All three November 2 queues are complete: the matched 3D validation comparison, the modern 2D controls, and the author-model 2D queue. GPU 0 was idle at this check (3 MiB used, 0% utilization). No trainer or queue process is active. The post-training 3D casebook is available at `reports/evaluation/r100150_vs_faultsegv3_validation_20261102/validation_casebook.png`. These runs remain validation-only; the Thebe test set was not read.

Final validation-only joint check on November 4: a convex probability ensemble of R100 and SwinUNETR selected 0.55/0.45 weights and threshold 0.20068359375. It reached Dice **0.605794** and PR-AUC **0.648634**, versus 0.590735 and 0.622857 for R100 alone. The 50/50 ensemble reached Dice 0.605683, showing a broad optimum. Result: `reports/evaluation/r100150_swinunetr_validation_ensemble_20261104/result.json`. Mentor handoff: `reports/handoff/MENTOR_FAULT_ENSEMBLE_HANDOFF_20261104.md`.

### Comparable full-validation protocol: valid seismic voxels only

| Model | Completed / requested epochs | Selected epoch | Dice | PR-AUC | State |
|---|---:|---:|---:|---:|---|
| R100 3D, seed 43 | 150 / 150 | 144 | **0.590735** | **0.622857** | Complete |
| MONAI SwinUNETR 3D, seed 43 | 150 / 150 | 140 | 0.577868 | 0.607603 | Complete |
| FaultSegV3 matched 3D, seed 43 | 150 / 150 | 147 | 0.535443 | 0.544422 | Complete |
| DeepLabV3-ResNet50 2D, seed 43 | 150 / 150 | 120 | 0.499617 | 0.481613 | Complete |
| Swin-T + FPN 2D, seed 43 | 150 / 150 | 140 | 0.479883 | 0.455768 | Complete |
| ViT-B/16 + SETR 2D, seed 43 | 150 / 150 | 147 | 0.313481 | 0.244076 | Complete after clean restart from epoch 1 following storage failure |
| SAMMed3D 3D, seed 42 | 100 / 100 | 97 | 0.294016 | 0.229465 | Complete; separate model/seed control |

R100's earlier 100-epoch seed-43 validation result was Dice 0.569856 and PR-AUC 0.592053. The 150-epoch run is higher by 0.020879 Dice and 0.030805 PR-AUC, with no added loss.

### Author-style 2D protocol: full raw validation grid

These four runs score the full 975,687,600-voxel grid, including no-data voxels, whereas the table above scores 613,738,550 valid voxels. Their values must not be ranked directly against the table above.

| Model | Completed / requested epochs | Selected epoch | Dice | PR-AUC | State |
|---|---:|---:|---:|---:|---|
| HED | 26 / 100 | 6 | 0.034558 | 0.012566 | Early stopping; predicts almost everything as fault at its selected threshold |
| RCF | 100 / 100 | 100 | 0.370490 | 0.328659 | Complete |
| U-Net | 52 / 100 | 32 | 0.531632 | 0.524425 | Early stopping |
| DeepLabM | 34 / 100 | 14 | 0.441083 | 0.412422 | Early stopping |

The 3D casebook manifest also contains per-case overlap, surface distance, HD95, tolerance F1, positive volume ratio, and connected-component counts. Its three label-selected validation cases show two ordinary fault cases and one weak/boundary case missed by all three matched 3D models. The casebook is diagnostic, not a replacement for the full-validation scores.

Snapshot: 2026-11-02 10:54 +04

| Experiment | What it tests | State at snapshot | Where to check |
|---|---|---|---|
| R100, seed 43, 150 epochs | **Epoch-count extension only:** same 3D model, ordinary masked BCE, Adam 1e-4, sampling, seed, and validation as the earlier 100-epoch run; no topology or new loss | **Running:** epoch 24 complete; epoch 25 active. The first 24 non-time history rows exactly reproduce the old run. Val Dice 0.3516, PR-AUC 0.4636 | `reports/training/r100_150_seed43_20261102.log` |
| FaultSegV3 matched, seed 43, 150 epochs | Newer fault-specific 3D architecture against R100 | **Running:** epoch 14 complete; epoch 15 active. Val Dice 0.0015, PR-AUC 0.3400 | `reports/training/faultsegv3_matched_150_seed43_20261102.log` |
| MONAI SwinUNETR, seed 43, 150 epochs | Official 3D Swin architecture and long-range context | **Running:** epoch 10 complete; epoch 11 active. Val Dice 0.0001, PR-AUC 0.1547 | `reports/training/swinunetr_matched_150_seed43_20261102.log` |
| DeepLabV3-ResNet50 2D | Dilated multiscale context as a fast architecture probe | **Running:** epoch 67 complete. Val Dice 0.3046, PR-AUC 0.3196 | `reports/training/deeplabv3_pure_thebe_150_seed43_20261102.log` |
| Swin-T + FPN 2D | Whether hierarchical attention improves fault context | **Queued after DeepLabV3** | `runs/pure2d_thebe_architecture_controls_queue.json` |
| ViT-B/16 + SETR head 2D | Whether global token context helps weak or interrupted faults | **Queued after Swin-T** | `runs/pure2d_thebe_architecture_controls_queue.json` |
| HED, Thebe author recipe | Deep edge supervision and class-balanced side losses | **Queued after the three 2D controls** | `runs/thebe_author2d_model_native_queue.json` |
| RCF, Thebe author recipe | Rich multiscale edge features and side-output supervision | **Queued after HED** | `runs/thebe_author2d_model_native_queue.json` |
| U-Net, Thebe author recipe | Source-verified 2D Thebe baseline | **Queued after RCF** | `runs/thebe_author2d_model_native_queue.json` |
| MobileNet DeepLab, Thebe author recipe | Source-verified light atrous Thebe baseline | **Queued after U-Net** | `runs/thebe_author2d_model_native_queue.json` |
| 3D comparison casebook watcher | Builds the same label-selected validation visuals after R100, FaultSegV3, and SwinUNETR finish | **Waiting; all three PIDs alive** | `runs/r100150_faultsegv3_validation_comparison_queue.json` |

## Next-day order

1. Check the four active logs and the two queue JSON files.
2. Confirm each completed run has `status.json`, `validation_selection.json`, and `best.pt`.
3. Inspect the generated validation casebook before selecting another 3D experiment.
4. Promote only a useful 2D finding into 3D: edge supervision, multiscale context, or transformer encoder.

All active and queued experiments keep Thebe test files closed. GPU usage was
100% with 15,494 MiB allocated; shared storage had 8.5 GiB available.

Retained after pure-model screening: public-pretrained variants, SAM/2.5D SAM,
GeoFWI3D fault/RGT pretraining, boundary/topology losses, and joint objectives.

## R100 clarification

The active 150-epoch R100 job starts again at epoch 1; it is not a continuation
loaded from the old epoch-100 checkpoint. The only scientific change is the
150-epoch budget. Its completed epochs 1–24 are bit-for-bit identical to the
earlier seed-43 run for loss, sampling counts, and every validation metric.

## 13:44 recovery snapshot

The shared filesystem reached 100% during simultaneous checkpoint writes. This
was a storage failure, not a CUDA or model failure. Incomplete `.part` files and
uncheckpointed final history rows were preserved for audit. Redundant smoke and
historical checkpoints were moved reversibly to `/tmp`, restoring working space.
The exact recovery record is
`reports/data_audit/DISK_FULL_RECOVERY_20261102.json`.

| Experiment | Verified state after recovery |
|---|---|
| R100 3D | Resumed from complete epoch 54 with optimizer, scaler, and RNG state; epoch 55 active |
| FaultSegV3 3D | Resumed from complete epoch 32 with optimizer, scaler, and RNG state; epoch 33 active |
| MONAI SwinUNETR 3D | Resumed from complete epoch 25 with optimizer, scaler, and RNG state; epoch 26 active |
| DeepLabV3 2D | Complete, 150/150; best epoch 120; full-validation Dice 0.4996, PR-AUC 0.4816 |
| Swin-T + FPN 2D | Complete, 150/150; best epoch 140; full-validation Dice 0.4799, PR-AUC 0.4558 |
| ViT-B/16 + SETR 2D | Initial attempt stopped after epoch 20. Because its compact checkpoint omits optimizer/scheduler state, it restarted from epoch 1 to preserve the protocol; epoch 1 active |
| Author HED → RCF → U-Net → DeepLabM | Waiting for the clean ViT run; all four one-epoch preflights passed |

At 13:44 +04, all four active trainers were alive. GPU memory was 16,676 MiB
of 24,564 MiB and the sampled utilization was 49%. Shared storage had 4.5 GiB
available. The author-model queue remains automatic after ViT completes.
