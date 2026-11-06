# Reports

<!-- BEGIN AUTO:R100_FP16_THREE_SEEDS -->
## R100 non-paper FP16 — seeds 42, 43, 44

| Status | Validation Dice | Test Dice | Ensemble test Dice | Report |
|---|---:|---:|---:|---|
| Training, validation, and frozen test complete | 0.562302 ± 0.015865 | 0.552587 ± 0.024087 | 0.581257 | [Test report](evaluation/r100_clean_frozen_test_20261019/report.md) |

Seed variability uses sample SD. [Training/validation report](experiments/R100_FP16_THREE_SEEDS_20261014.md) · [Evaluation protocol](experiments/R100_FROZEN_TEST_PROTOCOL_20261019.md)
<!-- END AUTO:R100_FP16_THREE_SEEDS -->

<!-- sam-frozen-results:start -->

## Frozen SAM-Med3D evaluations

- [Frozen SAM-Med3D: sammed3d_frozen_thebe_20261016T011856768228130Z](evaluation/sammed3d_frozen_thebe_20261016T011856768228130Z/report.md) — complete; automatic and oracle one-click results.

<!-- sam-frozen-results:end -->

## R100 ensemble-size measurement

[Existing three-seed validation curve](evaluation/r100_seed_curve_3models_20261019/report.md) measures all singles, pairs and the full ensemble. [Study explanation](experiments/R100_SEED_SATURATION_20261019.md). The two-seed pilot was launched on 19 October; [live pipeline state](../runs/R100_seed_saturation_pilot_20261019/pipeline_state.json) records training and automatic follow-up progress.

## Attention3D denoising pilot

[Roadmap review and bounded pilot](experiments/ATTENTION3D_DENOISING_PILOT_20261019.md): an in-domain denoising stage followed by matched scratch/fine-tuning comparisons using the full local attention model. Launched alongside the seed study on 19 October, with a four-hour supervisor limit. [Live stage](../runs/attention3d_denoising_pilot_20261019_v2/state.json). This is an early learning check, not a full paper reproduction.

## FaultEdgeFormer and field-pretrained Attention3D

[Held-out comparison report](evaluation/attention3d_faultedgeformer_comparison_20261028/report.md): the FaultEdgeFormer-inspired single model reached full-grid frozen-test Dice **0.574603**, while an Opunake+Kahu-pretrained Attention3D frozen-backbone linear probe reached sampled Thebe Dice **0.054170**. The report keeps these scopes separate and compares FaultEdgeFormer directly with the frozen R100 individual and ensemble references.
