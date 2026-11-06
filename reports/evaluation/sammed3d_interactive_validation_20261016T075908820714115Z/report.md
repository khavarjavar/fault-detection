# SAM-Med3D interactive Thebe validation diagnostic

Status: **complete**.

This run is validation-only. It does not open Thebe test files, train weights, or use an adapter.
It compares the two normalization and crop choices using zero/previous-mask feedback and corrective clicks.
All reported results are oracle-assisted because labels define samples, prompts, corrections, and scoring.
They are not automatic whole-survey results and are not directly comparable with R100 Dice.

| Crop | Normalization | Clicks | Micro Dice @ 0.5 | Mean patch Dice @ 0.5 | Val threshold | Micro Dice @ val threshold | Precision | Recall | ROC-AUC |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| fixed_positive_grid | r100_observed_zscore | 1 | 0.019819 | 0.014181 | 0.002929688 | 0.111786 | 0.060677 | 0.708926 | 0.517627 |
| fixed_positive_grid | r100_observed_zscore | 3 | 0.030880 | 0.020070 | 0.007324219 | 0.129131 | 0.072407 | 0.596209 | 0.585075 |
| fixed_positive_grid | r100_observed_zscore | 5 | 0.050680 | 0.028482 | 0.015625000 | 0.142980 | 0.082078 | 0.554189 | 0.622515 |
| fixed_positive_grid | sam_positive_zscore | 1 | 0.017029 | 0.009955 | 0.000000000 | 0.109643 | 0.058001 | 1.000000 | 0.493231 |
| fixed_positive_grid | sam_positive_zscore | 3 | 0.035973 | 0.019609 | 0.002441406 | 0.125279 | 0.069062 | 0.673506 | 0.568742 |
| fixed_positive_grid | sam_positive_zscore | 5 | 0.043775 | 0.023970 | 0.003906250 | 0.129005 | 0.071899 | 0.626951 | 0.580102 |
| label_centered | r100_observed_zscore | 1 | 0.037134 | 0.037967 | 0.000000000 | 0.155494 | 0.084301 | 1.000000 | 0.528337 |
| label_centered | r100_observed_zscore | 3 | 0.055433 | 0.052597 | 0.014160156 | 0.167596 | 0.099741 | 0.524237 | 0.558607 |
| label_centered | r100_observed_zscore | 5 | 0.071752 | 0.061003 | 0.021484375 | 0.174908 | 0.105562 | 0.509813 | 0.579077 |
| label_centered | sam_positive_zscore | 1 | 0.047059 | 0.046197 | 0.000000000 | 0.155494 | 0.084301 | 1.000000 | 0.524580 |
| label_centered | sam_positive_zscore | 3 | 0.063546 | 0.058003 | 0.003906250 | 0.161837 | 0.091237 | 0.715490 | 0.546548 |
| label_centered | sam_positive_zscore | 5 | 0.075061 | 0.065371 | 0.013671875 | 0.166206 | 0.097730 | 0.555234 | 0.560292 |

## Validation-only ranking

Best five-click fixed-0.5 configuration: `label_centered/sam_positive_zscore/5_clicks` with Dice 0.075061.
Best five-click validation-calibrated configuration: `label_centered/r100_observed_zscore/5_clicks` with Dice 0.174908.
These are diagnostic rankings on validation, not held-out test results.

## Interpretation limits

- Thebe contains a binary fault class but no fault-instance IDs, so the full fault mask in each crop is scored.
- Label-centered crops can overlap; their metrics are sample metrics, not unique survey-volume coverage.
- A later held-out test must freeze the chosen normalization, crop rule, click policy, and threshold first.

Evidence: `protocol.json`, `samples.csv`, `clicks.csv`, `validation_metrics.json`, `selection.json`, `evaluate.py`, source snapshots, and `console.log`.
