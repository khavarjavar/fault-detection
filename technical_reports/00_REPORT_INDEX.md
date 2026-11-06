# Fault-detection technical reports: run-folder map

## Why 18 run folders become 10 reports

There are **18 top-level directories** under runs/. They do not represent 18 independent scientific experiments. Some are smoke tests, failed launches, repeated seeds, precision variants, or corrected reruns of the same experiment.

The reports are grouped by the scientific question being tested. Every run folder is mapped below.

| Report | Experiment family | Run folders included | Folder status |
|---|---|---|---|
| [01](01_baseline_A_synthetic.md) | Baseline A on synthetic data | baseline_A_smoke; baseline_A_synthetic_bce_seed42 | smoke + completed full run |
| [02](02_loss_ablation_L1.md) | Weighted BCE + Dice loss | loss_ablation_L1_weighted_bce_dice_seed42 | completed |
| [03](03_P1_attention3d_caft_synthetic.md) | P1 attention + CAFT | p1_attention3d_caft_seed42 | completed |
| [04](04_baseline_A_zero_shot_thebe.md) | Baseline A synthetic-to-Thebe transfer | baseline_A_zero_shot_thebe_smoke_20261005_091638; baseline_A_zero_shot_thebe_smoke_20261005_094726; baseline_A_zero_shot_thebe_full_20261005_095032 | two smoke attempts + completed full evaluation |
| [05](05_P1_zero_shot_thebe.md) | P1 synthetic-to-Thebe transfer | p1_zero_shot_thebe_full_20261009_162704 | completed full evaluation |
| [06](06_R100_thebe_original.md) | Original R100 Thebe training | R100_thebe_seed42_20261005_102737 | completed after resume |
| [07](07_R100_clean_three_seeds.md) | Clean R100 three-seed study | R100_fp16_clean_3seeds_20261014_145225; R100_fp16_clean_3seeds_20261014_145510; R100_fp16_clean_3seeds_20261014_150435 | two failed launches + completed three-seed launch |
| [08](08_R100_seed_saturation.md) | Seed/ensemble saturation pilot | R100_seed_saturation_pilot_20261019 | active at report snapshot |
| [09](09_paper_attention3d_supervised.md) | Imported paper Attention3D supervised runs | paper_attention3d_thebe_smoke_20261009_170246; paper_attention3d_thebe_supervised_seed42; paper_attention3d_thebe_supervised_seed42_bf16_clean | smoke + two incomplete main attempts |
| [10](10_attention3d_denoising_pilot.md) | Attention3D denoising pretraining pilot | attention3d_denoising_pilot_20261019; attention3d_denoising_pilot_20261019_v2 | failed v1 + completed corrected v2 |

Count check:

- 2 + 1 + 1 + 3 + 1 + 1 + 3 + 1 + 3 + 2 = **18 run folders**
- These folders answer **10 experiment questions**, so there are **10 experiment reports**

Outputs stored only under reports/evaluation/, such as SAM, CRACKS, and frozen ensemble evaluations, are not extra top-level run folders. When an evaluation is part of one of the ten questions, its results are included in that experiment's report.

The [full Attention3D reproduction plan](11_attention3d_full_reproduction.md) records the 21 October paper/source audit and author questions. It has no new training run or result and is separate from the ten experiment reports above.

## Reporting rule

Each report:

- gives the input, output, data size, pipeline, method, and results;
- separates full runs from smoke tests and failed attempts;
- links the code and saved artifacts;
- explains missing or conflicting evidence instead of guessing;
- ends with simple definitions and metric calculations.

