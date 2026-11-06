# Canonical Experiment Names

**Updated:** 2026-10-02

## Formal roadmap

| Step | Canonical name | Definition | Status |
|---|---|---|---|
| 1 | Baseline A | FaultSeg3D U-Net trained on synthetic data with ordinary BCE | Complete |
| 2 | Baseline B | Baseline A model fine-tuned with a small labelled real-data subset | Not started |
| 3 | SSL experiment | Raw seismic masked reconstruction | Not started |
| 4 | Attribute-guided SSL | Coherence, variance and dip auxiliary objectives | Not started |
| 5 | EMA teacher consistency | Teacher-student consistency after SSL is proven useful | Not started |
| 6 | Distance-to-fault head | Conditional experiment for fault-boundary continuity | Not started |

## Supplementary experiment

| Name | Definition | Result |
|---|---|---|
| Loss Ablation L1 | Same synthetic data and architecture with weighted BCE plus Dice loss | Complete; no improvement over Baseline A |

## Canonical artifact names

- Baseline A run: `runs/baseline_A_synthetic_bce_seed42`
- Baseline A log: `reports/training/baseline_A_synthetic_bce_seed42.log`
- Loss Ablation L1 run: `runs/loss_ablation_L1_weighted_bce_dice_seed42`
- Loss Ablation L1 log: `reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log`
- Future Baseline B run: `runs/baseline_B_real_finetune_seed42`
- Future Baseline B log: `reports/training/baseline_B_real_finetune_seed42.log`

The internal loss keys `b0_bce` and `b1_weighted_dice` are implementation identifiers preserved inside historical checkpoints and configurations. They are not formal experiment names.
