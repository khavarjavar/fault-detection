# Mentor handoff: final Thebe fault ensemble

Date: 2026-11-04  
Selection data: complete Thebe validation only  
Thebe test files read during selection: no

## Recommended system

Use the probability ensemble of the completed R100 and MONAI SwinUNETR models:

```text
fault_probability = 0.55 * sigmoid(R100_logits)
                  + 0.45 * sigmoid(SwinUNETR_logits)

fault_mask = fault_probability >= 0.20068359375
```

Both models receive the same normalized 128 x 128 x 128 input cube. The ensemble is one system with two checkpoints.

## Validation result

| System | Dice | PR-AUC | Precision | Recall | MCC |
|---|---:|---:|---:|---:|---:|
| R100 alone | 0.590735 | 0.622857 | 0.589082 | 0.592398 | 0.578954 |
| SwinUNETR alone | 0.577868 | 0.607603 | 0.577961 | 0.577775 | 0.565750 |
| 50/50 ensemble | 0.605683 | 0.648269 | 0.601717 | 0.609702 | 0.594299 |
| **55/45 ensemble** | **0.605794** | **0.648634** | **0.603499** | **0.608107** | **0.594437** |

Relative to R100 alone, the selected ensemble adds 0.015059 Dice and 0.025776 PR-AUC. The 50/50 result is only 0.000111 Dice lower, indicating that the gain does not depend on a sharp weight optimum.

## Checkpoints

| Component | Selected epoch | Checkpoint | SHA-256 | Size |
|---|---:|---|---|---:|
| R100 | 144 | `runs/r100_150_seed43_20261102/best.pt` | `c38b04dcf40c7e302d35e0dd4594f9d027202b3efc5d13dc37b1703f981d0adc` | 17 MiB |
| MONAI SwinUNETR | 140 | `runs/swinunetr_matched_150_seed43_20261102/best.pt` | `748597d4a5593abff8ffb5a50103d42ed7caae782931e0f7ae15f9ec66ea4a82` | 188 MiB |

Model definitions:

- R100: `scripts/faultseg3d_baseline.py`
- SwinUNETR wrapper: `scripts/train_swinunetr_thebe_matched.py`
- Reference ensemble evaluator: `scripts/evaluate_r100_swin_validation_ensemble.py`

## Input and inference protocol

1. Form 128 x 128 x 128 seismic cubes.
2. Define valid voxels as raw seismic amplitude not equal to zero.
3. Compute mean and standard deviation from valid voxels within each cube.
4. Z-score only valid voxels; retain zero outside the valid region.
5. Apply the same axis reversal used by the training reader.
6. Run both models under FP16 autocast, then compute sigmoid probabilities in FP32.
7. Combine probabilities using the frozen 0.55/0.45 weights.
8. Apply threshold 0.20068359375 and clear predictions outside the valid mask.

If the mentor requires one checkpoint rather than a two-model system, use R100 epoch 144 with threshold 0.1923828125. It is the strongest single model under the comparable full-validation protocol.

## Known limitation to inspect on mentor data

All three matched 3D models missed the same weak/no-data-boundary validation case. The mentor should therefore include at least one subtle fault and one survey-boundary region, rather than testing only obvious faults. Review the probability volume as well as the thresholded mask because a different survey may need threshold recalibration.

## Evidence

- Ensemble result: `reports/evaluation/r100150_swinunetr_validation_ensemble_20261104/result.json`
- Three-model visual casebook: `reports/evaluation/r100150_vs_faultsegv3_validation_20261102/validation_casebook.png`
- Visual geometry metrics: `reports/evaluation/r100150_vs_faultsegv3_validation_20261102/manifest.json`

