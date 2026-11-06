# Attention3D two-survey pretraining result

- Status: complete
- Best epoch: 50
- Training patches: 17,600 (8,800 Opunake; 8,800 Kahu)
- Fixed-validation network MSE: 0.00986143
- Noisy-input identity MSE: 0.03193139
- Identity minus network MSE: 0.02206995
- Beats identity baseline: True
- Best checkpoint SHA-256: `b8baa66e3f33395e17af6c971f6712abffca0d1edc006227df02f776869dc574`

This result measures self-supervised denoising on spatially held-out Opunake/Kahu cubes. It is not itself a Thebe fault-segmentation score. Kerry was not included.

## Downstream representation test

On 28 October 2026, a frozen-backbone linear probe transferred all feature
tensors, reinitialized the 177-parameter segmentation head, trained that head
on labelled Thebe training patches, selected checkpoint and threshold on a
fixed validation sample, and then evaluated a fixed sample spanning all seven
held-out Thebe test blocks.

The test result was Dice `0.054170`, PR-AUC `0.027396`, ROC-AUC `0.509454`, and
MCC `0.009117` over 32,733,012 valid voxels. This near-random ranking result
shows that the frozen denoising features were not linearly sufficient for
Thebe fault detection. It is a sampled linear-probe screen; full-network
fine-tuning and full-grid evaluation remain separate experiments.

Evidence: `runs/attention3d_opunake_kahu_linear_probe_thebe_seed42_20261028/result.json`.
