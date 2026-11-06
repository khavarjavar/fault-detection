# Experiment 10: Attention3D denoising-pretraining pilot

## Quick answer

This short pilot tested whether in-domain denoising pretraining helps the 45-million-parameter Attention3D model learn fault segmentation.

| Arm | Selected crop Dice |
|---|---:|
| Training from scratch | **0.077589** |
| Denoising pretraining, then fine-tuning | 0.070065 |
| Fine-tuning minus scratch | **−0.007525** |

The short pretrained arm did not improve Dice. The denoiser also failed to beat the simple identity baseline.

## 1. Why there are two folders

| Folder | Status |
|---|---|
| [v1](../runs/attention3d_denoising_pilot_20261019) | Failed before training: no usable reconstruction-validation patch in the chosen band |
| [v2](../runs/attention3d_denoising_pilot_20261019_v2) | Corrected data bands; all stages completed |

The v1 failure is setup evidence, not a training result.

## 2. Data

All stages use Thebe HDF5 data with 64³ crops.

| Role | Data |
|---|---|
| Denoising training | Training seismic only; raw axis-1 band [64,1024) |
| Denoising validation | Training seismic only; band [1280,1536) |
| Segmentation training | 512 deterministic crops from training blocks |
| Segmentation validation | 32 fixed crops from val1.h5 and val2.h5 |
| Test | Not opened |

The pretext train and validation bands have a 256-index gap. Stored crop locations are disjoint, but physical survey-coordinate independence cannot be proven.

The segmentation validation contains 7,748,896 scored voxel presentations, including 159,308 labelled faults. Crops may overlap.

## 3. Denoising task

For each valid crop:

1. z-score the observed seismic values;
2. add Gaussian noise with standard deviation 0.1 × crop RMS;
3. ask the model to reconstruct the original normalized field input;
4. calculate mean squared error only on valid voxels.

The target is the original field input, which can already contain natural noise. There is no separate noise-free ground truth.

## 4. Model and transfer

The model is the imported 45,001,057-parameter global Attention3D U-Net from Experiment 9.

After denoising:

- 78 feature tensors were copied exactly;
- the segmentation output head was newly initialized;
- the optimizer was reset;
- every layer remained trainable;
- there was no gradual unfreezing or layer-specific learning rate.

The scratch and fine-tuning arms used identical supervised crop-stream hashes.

## 5. Budgets

| Stage | Crop presentations | Optimizer updates | Peak LR | Time |
|---|---:|---:|---:|---:|
| Denoising pretraining | 256 | 64 | 0.0001 | 2,376.99 s |
| Scratch segmentation | 512 | 128 | 0.0005 | 4,502.52 s |
| Fine-tuned segmentation | 512 | 128 | 0.0005 | 4,496.31 s |

All stages use batch 1, accumulation 4, AdamW, BF16 forward operations, FP32 loss/weights, finite checks, and gradient clipping.

## 6. Reconstruction results

Identity means returning the noisy input unchanged.

| Pretraining crops | Network MSE | Identity MSE | Identity − network |
|---:|---:|---:|---:|
| 128 | 0.032463 | 0.010007 | −0.022456 |
| 256 | 0.013096 | 0.010007 | −0.003090 |

Negative improvement means the network is worse than identity. The 256-crop checkpoint was selected because it had the lower network MSE, but it still did not beat identity.

## 7. Segmentation validation history

Each row uses the threshold that maximized Dice on the same 32 development crops.

| Crops | Scratch Dice | Scratch PR-AUC | Fine-tune Dice | Fine-tune PR-AUC |
|---:|---:|---:|---:|---:|
| 128 | 0.045995 | 0.020975 | 0.046642 | 0.021817 |
| 256 | 0.046681 | 0.021821 | 0.049285 | 0.024147 |
| 384 | 0.049840 | 0.024258 | 0.066822 | 0.032736 |
| 512 | **0.077589** | **0.037056** | 0.070065 | 0.036330 |

The final selected comparison:

| Metric | Scratch | Fine-tune |
|---|---:|---:|
| Threshold | 0.349609 | 0.364258 |
| Dice | **0.077589** | 0.070065 |
| IoU | 0.040360 | 0.036304 |
| Precision | 0.046966 | 0.038939 |
| Recall | 0.222977 | 0.349179 |
| PR-AUC | 0.037056 | 0.036330 |
| TP | 35,522 | 55,627 |
| FP | 720,811 | 1,372,937 |
| FN | 123,786 | 103,681 |
| TN | 6,868,777 | 6,216,651 |
| Mean patch BCE | 0.333870 | 0.300665 |

At threshold 0.5, scratch Dice was 0 and fine-tune Dice was 0.057390.

## 8. Interpretation and evidence

The pretraining network learned to reduce its own reconstruction error, but did not beat the noisy-input identity baseline. Its transferred features also did not improve the final matched segmentation Dice.

This is a short development-crop pilot. It is not converged training, a full-survey evaluation, or a paper reproduction. No test files were opened.

Evidence:

- Final comparison: [comparison.json](../runs/attention3d_denoising_pilot_20261019_v2/comparison.json)
- Configuration: [config.json](../runs/attention3d_denoising_pilot_20261019_v2/config.json)
- Transfer check: [transfer_report.json](../runs/attention3d_denoising_pilot_20261019_v2/transfer_report.json)
- Completed state: [state.json](../runs/attention3d_denoising_pilot_20261019_v2/state.json)
- Archived executing code: [paper_attention3d_pilot.py](../runs/attention3d_denoising_pilot_20261019_v2/source_snapshot/scripts/paper_attention3d_pilot.py)
- Failed v1 state: [state.json](../runs/attention3d_denoising_pilot_20261019/state.json)

## 9. Simple definitions and calculations

| Term | Meaning |
|---|---|
| Pretext task | A preparatory task used to learn features before the main task. |
| Denoising | Reconstruct an input after artificial noise is added. |
| RMS | Square root of the mean squared signal value. |
| MSE | Mean of squared prediction errors. Lower is better. |
| Identity baseline | Return the noisy input without processing it. |
| Feature transfer | Copy internal model weights to initialize another task. |
| Scratch control | Same supervised training, but with random initialization. |
| Matched crop stream | Both arms receive the same crop coordinates in the same order. |

Masked MSE = Σ(valid prediction − target)² / number of valid voxels.

Final Dice difference:

0.070065 − 0.077589 = **−0.007525**
