# Untouched SAM-Med3D-turbo zero-shot Thebe smoke test

- Data: two deterministic fault-containing validation patches
- Training/adaptation: none; zero weight updates
- Held-out test opened: no
- Threshold: fixed probability 0.5; no tuning
- `no_prompt`: diagnostic only
- `one_positive_point`: one oracle point derived from validation ground truth

This is a quick feasibility check, not a final benchmark. The prompted result is not directly comparable with an automatic R100 result.

| Mode | Mean Dice | Mean IoU | Mean precision | Mean recall |
|---|---:|---:|---:|---:|
| `no_prompt` | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| `one_positive_point` | 0.000000 | 0.000000 | 0.000000 | 0.000000 |

Machine-readable results: `reports/evaluation/sammed3d_zero_shot_validation_smoke_20261016T010054Z/results.json`
