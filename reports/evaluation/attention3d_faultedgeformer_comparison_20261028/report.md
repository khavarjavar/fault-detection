# Attention3D transfer and FaultEdgeFormer held-out results

**Completed:** 28 October 2026  
**Dataset:** Thebe fault segmentation  
**Metric policy:** pooled valid voxels; validation-selected thresholds; 2,048-bin PR/ROC approximations

## Result summary

| Experiment | Evaluation scope | Dice | IoU | Precision | Recall | PR-AUC | ROC-AUC | MCC |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| FaultEdgeFormer-inspired, seed 42 | Complete seven-block test; 2.303B valid voxels | **0.574603** | **0.403118** | **0.528904** | **0.628947** | **0.603953** | **0.972073** | **0.564939** |
| R100, best individual seed 43 | Same complete test | 0.567466 | 0.396128 | 0.502357 | 0.651965 | 0.600605 | 0.966376 | 0.559877 |
| R100, three-model ensemble | Same complete test | **0.581257** | **0.409699** | 0.517305 | **0.663253** | **0.620308** | 0.970100 | **0.573795** |
| Attention3D pretrained linear probe | Fixed 64-cube sample; 32.73M valid voxels | 0.054170 | 0.027839 | 0.027906 | 0.920793 | 0.027396 | 0.509454 | 0.009117 |

The first three rows are directly comparable because they use the same full
test geometry, validity mask, and pooled evaluation population. The
Attention3D row is a sampled representation-transfer diagnostic and must not
be placed on the full-grid leaderboard.

## FaultEdgeFormer-inspired model

The model was trained on labelled `train1.h5` through `train9.h5`. Checkpoint
epoch 99 and threshold `0.24560546875` were selected using complete
`val1.h5 + val2.h5` before any test file was opened. All seven test blocks were
then evaluated once with the frozen state.

| Metric | Validation | Frozen test | Test at threshold 0.5 |
|---|---:|---:|---:|
| Dice | 0.563981 | **0.574603** | 0.532693 |
| IoU | 0.392739 | **0.403118** | 0.363042 |
| Precision | 0.559185 | **0.528904** | 0.704236 |
| Recall | 0.568860 | **0.628947** | 0.428352 |
| Specificity | 0.987125 | **0.985611** | 0.995379 |
| Balanced accuracy | 0.777992 | **0.807279** | 0.711866 |
| Accuracy | 0.975452 | **0.976679** | 0.981180 |
| MCC | 0.551374 | **0.564939** | 0.540599 |
| PR-AUC | 0.592442 | **0.603953** | 0.603953 |
| ROC-AUC | 0.964473 | **0.972073** | 0.972073 |

Frozen-test confusion counts: TP 36,277,964; FP 32,312,845; FN 21,402,532;
TN 2,213,348,212. Test inference covered 3,429,541,914 raw voxels and scored
2,303,341,553 valid voxels. No test-threshold tuning was performed.

Against the best R100 individual seed, FaultEdgeFormer gains `+0.007137` Dice,
`+0.003349` PR-AUC, and `+0.005062` MCC. Against the three-model R100
ensemble, it is `-0.006654` Dice and `-0.016354` PR-AUC, while its precision
and ROC-AUC are slightly higher. This makes it the strongest tested single
model by Dice, but it does not beat the R100 ensemble.

## Attention3D Opunake + Kahu pretraining

The `best.pt` checkpoint completed 50 epochs of self-supervised Gaussian
denoising on Opunake and Kahu. It reconstructed held-out noisy field cubes
with MSE `0.00986143`, compared with `0.03193139` for leaving the noisy input
unchanged. Kerry was not included.

That checkpoint is a reconstruction network rather than a semantic fault
detector. A valid downstream test therefore transferred all 78 feature
tensors, reinitialized the output convolution, froze 45,000,880 feature
parameters, and trained only the new 177-parameter head on 256 labelled Thebe
training patches. Step 128 and threshold `0.2060546875` were selected on a
fixed 128-patch validation sample before test files were opened.

| Metric | Validation | Held-out test sample | Test at threshold 0.5 |
|---|---:|---:|---:|
| Dice | 0.073137 | **0.054170** | 0.000351 |
| IoU | 0.037956 | **0.027839** | 0.000176 |
| Precision | 0.038109 | **0.027906** | 0.057122 |
| Recall | 0.904461 | **0.920793** | 0.000176 |
| Specificity | 0.099446 | **0.095586** | 0.999918 |
| Balanced accuracy | 0.501954 | **0.508189** | 0.500047 |
| Accuracy | 0.129997 | **0.118216** | 0.972502 |
| MCC | 0.002497 | **0.009117** | 0.001672 |
| PR-AUC | 0.039540 | **0.027396** | 0.027396 |
| ROC-AUC | 0.503032 | **0.509454** | 0.509454 |

The test sample requested 256 cubes, of which 175 contained usable observed
data. It spans all seven test blocks and contains 32,733,012 valid voxels.
Frozen-threshold confusion counts are TP 826,546; FP 28,792,349; FN 71,100;
TN 3,043,017.

The high recall comes from predicting faults across most valid voxels. The
2.79% precision, ROC-AUC near 0.5, and MCC near zero show that the frozen
denoising representation does not linearly separate fault and non-fault
voxels under this protocol.

### Attention3D result by test block

All rows use the one validation-selected threshold.

| Block | Dice | Precision | Recall | PR-AUC | ROC-AUC | MCC |
|---|---:|---:|---:|---:|---:|---:|
| test1 | 0.052886 | 0.027225 | 0.920983 | 0.027226 | 0.503506 | 0.003778 |
| test2 | 0.046049 | 0.023621 | 0.911823 | 0.024138 | 0.512698 | 0.004621 |
| test3 | 0.052663 | 0.027097 | 0.931459 | 0.025234 | 0.505890 | 0.015770 |
| test4 | 0.049618 | 0.025513 | 0.898545 | 0.024981 | 0.490304 | -0.000032 |
| test5 | 0.039568 | 0.020214 | 0.929294 | 0.020471 | 0.529780 | 0.012833 |
| test6 | 0.085167 | 0.044624 | 0.931403 | 0.042778 | 0.512031 | 0.018239 |
| test7 | 0.031581 | 0.016076 | 0.888668 | 0.019585 | 0.515400 | -0.009086 |

## Conclusions and limits

1. FaultEdgeFormer provides a valid full-grid single-seed result and slightly
   improves over the best individual R100 seed. The three-model R100 ensemble
   remains best by Dice, PR-AUC, recall, and MCC.
2. Successful denoising did not produce linearly fault-discriminative frozen
   Attention3D features on Thebe. The denoising metric cannot be used as a
   fault-detection claim.
3. The Attention3D result is a linear-probe screen. It does not rule out
   end-to-end fine-tuning, because almost all model parameters were frozen.
4. FaultEdgeFormer is a local inspired implementation, not an exact author
   reproduction, and one seed does not quantify training variation.
5. Attention3D is a two-survey reproduction variant because Kerry and several
   unpublished training details remain unavailable.

## Evidence

- FaultEdgeFormer: `reports/evaluation/faultedgeformer_thebe_full_seed42_20261026/result.json`
- FaultEdgeFormer frozen manifest: `reports/evaluation/faultedgeformer_thebe_full_seed42_20261026/FROZEN_BEFORE_TEST.json`
- Attention3D pretraining: `reports/evaluation/attention3d_two_survey_pretext_seed42_20261026/result.json`
- Attention3D transfer: `runs/attention3d_opunake_kahu_linear_probe_thebe_seed42_20261028/result.json`
- Attention3D frozen manifest: `runs/attention3d_opunake_kahu_linear_probe_thebe_seed42_20261028/FROZEN_BEFORE_TEST.json`
- Attention3D test manifest: `runs/attention3d_opunake_kahu_linear_probe_thebe_seed42_20261028/test_patch_manifest.json`
- R100 reference: `reports/evaluation/r100_clean_frozen_test_20261019/final_metrics.json`

