# Thebe Zero-Shot Smoke-Test Result

- Status: **PASS**
- Purpose: pipeline check only; not the final score
- Training performed on Thebe: **no**
- Real Thebe labels used for training: **0%**
- Threshold: `0.438965`
- Patches inferred: `16`
- Patches containing scorable data: `11`
- Valid voxels evaluated: `11351241`
- No-data voxels excluded: `20122423`
- Positive labels outside the data mask: `2186`

## Provisional smoke metrics

- Dice: `0.068389`
- IoU: `0.035405`
- Precision: `0.041877`
- Recall: `0.186394`
- MCC: `0.013585`
- PR-AUC: `0.037830`

These values cover only 16 patches and must not be reported as the final A→T0 result.

- Complete metrics: `runs/baseline_A_zero_shot_thebe_smoke_20261005_094726/final_metrics.json`
- Complete command output: `reports/evaluation/baseline_A_zero_shot_thebe_smoke_20261005_094726.log`
