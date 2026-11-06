<!-- Presentation source. Each horizontal rule starts a new slide. Slides 1–18 form the talk; the remaining slides are optional backup for questions. Results are a snapshot of saved artifacts on 19 October 2026. -->

# What I learned from our seismic fault-detection experiments

**Fault detection project · 19 October 2026**

Synthetic faults, real Thebe seismic, transfer tests, attention models, denoising, ensembling, and SAM-Med3D.

---

# I tested the whole path from data to evaluation

- Audited dataset splits, labels, fault prevalence, and missing-data regions.
- Trained a small 3D U-Net on synthetic data; changed its loss and attention design.
- Tested synthetic models on real Thebe data and expert-labelled CRACKS sections.
- Trained real-data R100 models, repeated three seeds, and evaluated a frozen ensemble.
- Piloted imported Attention3D, denoising pretraining, and SAM-Med3D.

**Scope:** 10 run-based experiment families, plus evaluation-only diagnostics.

---

# I learned exactly how much data each result uses

| Dataset | Training | Validation | Held-out test |
|---|---:|---:|---:|
| Synthetic FaultSeg3D | 180 cubes | 20 cubes | 20 cubes |
| Real Thebe HDF5 | 9 blocks | 2 blocks | 7 blocks |

- Each synthetic cube is **128³ = 2,097,152 voxels**; training adds one fixed flipped copy per cube.
- Thebe test contains **3.43 billion raw voxels**; **2.30 billion** pass the implemented valid-data mask.
- CRACKS provides **40 expert-labelled 2D sections** for the reported scores, not a dense 3D test mask.

---

# I learned that the scoring population matters

- Fault labels occupy **7.23%** of synthetic test voxels and **2.50%** of scored Thebe test voxels.
- R100 full-grid evaluation excludes raw zero/no-data positions and boundary padding.
- Clean R100 checkpoints and thresholds came from validation; its test was evaluated after both were frozen.
- I report **Dice, precision, recall, and PR-AUC** alongside coverage; accuracy alone hides many fault errors.

---

# A small 3D U-Net worked well on synthetic data

- Input: a 128³ seismic cube. Output: a 128³ fault-probability map.
- Baseline: **1.46 million parameters**, ordinary binary cross-entropy, 100 epochs, seed 42.
- Held-out synthetic test: **Dice 0.8211**, precision **0.8030**, recall **0.8399**.
- This established a synthetic reference point; it did not establish real-data performance.

---

# Changing the loss did not improve this synthetic run

- I kept the same data, model, seed, and 100-epoch budget.
- I replaced ordinary BCE with **0.5 × weighted BCE + 0.5 × soft Dice loss**.
- Synthetic test Dice: **0.8198** versus baseline **0.8211**; difference **−0.0013**.
- Lesson: this single matched-seed loss change gave no measured Dice gain.

---

# Attention gave a small Dice gain, with a trade-off

- P1 added two attention gates and a connectivity-aware focal Tversky loss.
- Synthetic test Dice: **0.8266** versus baseline **0.8211**.
- Recall rose from **0.8399 to 0.8589**; PR-AUC fell from **0.8905 to 0.7333**.
- The model **and** loss changed together, so I cannot credit attention alone.

---

# Synthetic success did not transfer to real Thebe

- Without real-data weight updates, baseline synthetic → Thebe full-test Dice: **0.0859**.
- P1 synthetic → Thebe full-test Dice: **0.0791**.
- Both used their synthetic validation thresholds; neither was fine-tuned on Thebe.
- Lesson: the real-data domain gap remained large. The retained P1 mask descriptions conflict, so its small difference from baseline is not a clean model ranking.

---

# CRACKS showed why annotation rules must be explicit

- I evaluated the frozen synthetic P1 model on **40 expert-labelled sections**; no retraining.
- With green/blue RGB pixels treated as faults: **Dice 0.0353** on **7.15 million** scored pixels.
- With only certain raw labels scored: **Dice 0.0576** on **1.27 million** different scored pixels.
- Lesson: changing which pixels count changes the question. These are two label policies, not an improvement from one model to another.

---

# Training on labelled Thebe data improved the measured result

- Original R100: the small 3D U-Net trained from scratch on real **128³ patches** for 100 epochs.
- Full Thebe test Dice: **0.5430**; synthetic baseline zero-shot Dice: **0.0859** under their recorded evaluations.
- I selected the final threshold on the full validation grid, then held it fixed for test.
- This run resumed after epoch 23 with an incomplete saved random/scaler state; I treated it as a useful result, not a perfectly reproducible continuation.

---

# Repeating R100 exposed seed-to-seed variation

| Clean R100 seed | Full validation Dice | Frozen full-test Dice |
|---:|---:|---:|
| 42 | 0.5441 | 0.5248 |
| 43 | 0.5699 | 0.5675 |
| 44 | 0.5730 | 0.5655 |

- Same architecture, data, 100 epochs, and checkpoint-selection protocol.
- Mean individual test Dice: **0.5526**; sample standard deviation: **0.0241**.

---

# Averaging three R100 models improved the frozen test

- I averaged the three models' **voxel probabilities**; the ensemble threshold **0.2749** came from validation.
- Ensemble full-test Dice: **0.5813**, versus best individual **0.5675**.
- Full-test IoU **0.4097**, recall **0.6633**, approximate PR-AUC **0.6203**.
- The seven-block result covers **2.30 billion scored voxels**. Independent checks passed for checkpoint hashes, validation reproduction, and saved test counts.

---

# The ensemble-size evidence reaches three models

| Models averaged | Mean full-validation Dice across available subsets |
|---:|---:|
| 1 | 0.5623 |
| 2 | 0.5814 |
| 3 | 0.5890 (one subset) |

- The curve uses the same validation data for every subset and its threshold.
- Seeds 45 and 46 were **still in training at this snapshot**; there is no five-model result here.
- Lesson: the measured curve rises to three models; it does not establish saturation.

---

# The imported global Attention3D was harder to establish

- I adapted a **45.0-million-parameter** imported model to supervised **64³ Thebe crops**.
- FP16 attempt: best selected-crop validation Dice **0.5390**, but later losses became non-finite; run incomplete.
- BF16 attempt: best selected-crop validation Dice **0.3097**; run stopped without a recorded completion cause.
- No full-survey validation or held-out test score exists for these attempts. Crop Dice is not comparable with R100 full-survey Dice.

---

# A short denoising pilot did not help this model

- The first launch failed before training because its reconstruction-validation band had no usable crop; the corrected second launch completed.
- After **256 denoising crops**, network validation MSE was **0.01310**; returning the noisy input unchanged gave **0.01001**.
- After matched **512-crop** segmentation budgets: scratch Dice **0.07759**, pretrained then fine-tuned Dice **0.07006**.
- Lesson: this short validation-crop pilot showed no benefit from the tested denoising initialization. It has no held-out test result.

---

# Frozen SAM-Med3D was weak as an automatic detector

- Prompt-free, frozen SAM-Med3D full-Thebe test Dice: **0.0488** with a validation-chosen threshold.
- One **ground-truth-selected** click per patch gave **0.0613**; that setting is oracle-assisted, not automatic.
- A separate validation-only study reached **0.1749** Dice on label-centred positive crops with five oracle clicks.
- Lesson: selected interactive crops and full-survey automatic detection answer different questions.

---

# I prepared, but did not finish, a SAM adaptation test

- I implemented a residual feature adapter with a frozen SAM image encoder and trainable mask decoder.
- CPU preflight passed: **100.58 million total parameters**, **7.65 million trainable**.
- No GPU training or held-out result exists for this adapter; it is implementation evidence only.

---

# What I learned

1. A high synthetic score did **not** predict real Thebe performance.
2. Training on labelled real patches changed the result far more than the tested synthetic loss or attention changes.
3. Repeated seeds mattered; three-model probability averaging improved the frozen real-data test.
4. Mask rules, annotation policies, thresholds, and evaluation scope can change what a score means.
5. The attention, denoising, and SAM pilots produced useful diagnostics, but not a better completed full-survey detector.

---

# Backup: the data and input → output pipeline

| Item | Synthetic experiments | Real R100 experiments |
|---|---|---|
| Input | 128³ seismic cube | 128³ patch from HDF5 survey |
| Label/output | One fault label/probability per voxel | One fault label/probability per valid voxel |
| Split | 180/20/20 original cubes | 9/2/7 train/val/test blocks |
| Train volume | 377d
,487,360 raw voxels | 4,390,594,200 raw voxels |
| Validation volume | 41,943,040 raw voxels | 975,687,600 raw; 613,738,550 scored |
| Test volume | 41,943,040 raw voxels | 3,429,541,914 raw; 2,303,341,553 scored |
| Preprocessing | Per-cube z-score, axis transpose, fixed flip in training | Finite/nonzero mask, valid-only patch z-score, axis reversal, masked loss/metrics |
| Threshold | Chosen on validation, applied to synthetic test | Chosen on full validation, applied to full test |

Thebe full test uses 1,950 non-overlapping 128³ grid patches: 1,382 observed and 568 no-data. Padding and no-data voxels are excluded. The real train/validation/test HDF5 blocks are distinct file splits; physical survey-coordinate independence is not proven by these files.

---

# Backup: training and selection cheat sheet

| Experiment | Model and training | Checkpoint / threshold decision |
|---|---|---|
| Synthetic baseline | Small 3D U-Net; ordinary BCE; 100 epochs; seed 42 | Best epoch 100 by val Dice@0.5; val threshold 0.438965 |
| Synthetic L1 | Same U-Net; weighted BCE + soft Dice; 100 epochs; seed 42 | Best epoch 100; val threshold 0.853027 |
| Synthetic P1 | Attention-gated U-Net; connectivity-aware focal Tversky + attention supervision; 100 epochs; seed 42 | Best epoch 93; val threshold 0.980957 |
| Original R100 | Same small U-Net, random start; masked BCE; 360 real 128³ patches/epoch; 100 epochs | Best epoch 96 after resume; val threshold 0.176758 |
| Clean R100 | Three independent small U-Nets; same patch budget and 100 epochs each | Best epochs 95/93/95 by fixed-crop val PR-AUC; each and ensemble threshold selected on full val |
| Imported Attention3D | 45.0M parameters; unified focal loss; 64³ selected crops; incomplete FP16/BF16 attempts | Best saved crop Dice only; no full-survey threshold or test |
| Denoising pilot | 256 reconstruction crops, then matched scratch/fine-tuned 512-crop segmentation | Comparison on same 32 development crops; no held-out test |
| Frozen SAM | No weight updates; prompt-free and oracle-click modes | Separate validation thresholds; full test used frozen settings |

The clean R100 ensemble threshold was **0.274902**. The three seed thresholds were **0.316406**, **0.279297**, and **0.244141**. CRACKS kept P1's synthetic threshold **0.980957**.

---

# Backup: exact measured scores by evaluation scope

| Model/experiment | Scope | Dice | IoU | Precision | Recall | PR-AUC* |
|---|---|---:|---:|---:|---:|---:|
| Synthetic baseline A | 20-cube synthetic test | 0.821059 | 0.696437 | 0.803010 | 0.839938 | 0.890460 |
| Weighted BCE + Dice | Same synthetic test | 0.819766 | 0.694579 | 0.804110 | 0.836043 | 0.876373 |
| P1 attention + CAFT | Same synthetic test | 0.826646 | 0.704515 | 0.796766 | 0.858854 | 0.733316 |
| Baseline A, zero-shot | Full Thebe test | 0.085861 | 0.044856 | 0.052094 | 0.244065 | 0.041552 |
| P1, zero-shot | Full Thebe test; mask record conflict | 0.079128 | 0.041194 | 0.050344 | 0.184774 | 0.030899 |
| Original R100 | Full Thebe test | 0.542996 | 0.372679 | 0.471918 | 0.639281 | 0.569809 |
| Clean R100 ensemble | Frozen full Thebe test | **0.581257** | **0.409699** | **0.517305** | **0.663253** | **0.620308** |
| P1 on CRACKS, RGB policy | 40 expert-labelled sections | 0.035273 | 0.017953 | 0.024374 | 0.063801 | 0.025374 |
| Frozen SAM, no prompt | Full Thebe test | 0.048805 | 0.025013 | 0.025042 | 0.955600 | 0.024793 |
| Frozen SAM, oracle click | Full Thebe test, label-assisted | 0.061343 | 0.031642 | 0.034110 | 0.304293 | 0.032168 |

*PR-AUC in these artifacts is histogram-based/approximate. The no-prompt SAM threshold is very low (0.01416), yielding high recall with extremely low precision. Scores from different datasets, masks, prompts, or crop selection should not be ranked as one leaderboard.

---

# Backup: development-only and incomplete results

| Work | Measured result | What it does and does not show |
|---|---|---|
| Three-model R100 ensemble | Validation Dice 0.588951; test Dice 0.581257 | Full-grid evaluation; test threshold fixed from validation |
| Ensemble-size curve | One/two/three-model mean validation Dice 0.562302/0.581409/0.588951 | Same validation set; size three has one subset; no five-model claim |
| Paper Attention3D FP16 | Best selected-crop val Dice 0.539004 | 77 recorded epochs; later non-finite loss; incomplete; no full test |
| Paper Attention3D BF16 | Best selected-crop val Dice 0.309747 | 65 complete rows; stop cause not recorded; no full test |
| Denoising reconstruction | MSE 0.013096 vs identity 0.010007 | Corrected pilot completed; identity was better on pretext validation |
| Denoising transfer | Scratch crop Dice 0.077589 vs fine-tuned 0.070065 | Matched 512-crop budget, same 32 development crops; no test |
| CRACKS certain-only labels | Dice 0.057553 | Different scored pixels from RGB policy; not a fair score gain |
| SAM interactive | Best five-click calibrated crop Dice 0.174908 | Positive, label-centred validation crops with oracle clicks; no test |
| SAM adapter | CPU preflight passed | No GPU execution or trained-result metric |

---

# Backup: additional recorded metrics

| Completed evaluation | Specificity | Accuracy | Balanced accuracy | MCC | ROC-AUC* |
|---|---:|---:|---:|---:|---:|
| Synthetic baseline A test | 0.983943 | 0.973532 | 0.911940 | 0.807013 | 0.985232 |
| Synthetic weighted BCE + Dice test | 0.984129 | 0.973423 | 0.910086 | 0.805603 | 0.980179 |
| Synthetic P1 test | 0.982928 | 0.973959 | 0.920891 | 0.813258 | 0.939682 |
| Baseline A zero-shot Thebe | 0.885930 | 0.869856 | 0.564998 | 0.063119 | 0.654087 |
| P1 zero-shot Thebe | 0.910474 | 0.892301 | 0.547624 | 0.051515 | 0.556206 |
| Original R100 Thebe test | 0.981626 | 0.973053 | 0.810453 | 0.535921 | 0.960459 |
| Clean R100 ensemble Thebe test | 0.984104 | 0.976069 | 0.823678 | 0.573795 | 0.970100 |

*ROC-AUC is approximate in these saved metrics. Different dataset and mask scopes still apply. These are supporting figures, not a cross-dataset ranking.

---

# Backup: quick metric answers

- **TP:** a labelled fault voxel predicted as fault. **FP:** background predicted as fault. **FN:** a missed fault. **TN:** correctly predicted background.
- **Dice** = `2TP / (2TP + FP + FN)`. For the frozen ensemble: `2 × 38,256,762 / (2 × 38,256,762 + 35,697,272 + 19,423,734) = 0.581257`.
- **IoU** = `TP / (TP + FP + FN)`; it is another overlap score.
- **Precision** = `TP / (TP + FP)`: of predicted faults, how many matched labels?
- **Recall** = `TP / (TP + FN)`: of labelled faults, how many were found?
- **Threshold:** probability cutoff for calling a voxel a fault; our final thresholds were selected on validation, then frozen for test.
- **PR-AUC:** summary of precision versus recall over many thresholds; higher is better. Unlike Dice, it is not tied to one cutoff. Reported values here are approximate from saved histograms.
- **MSE** = mean of squared prediction errors; lower is better. The denoising target was the uncorrupted field input, not a known noise-free geological volume.
- **Pooled/full-grid Dice:** add TP, FP, and FN over all scored voxels before calculating Dice. It is different from averaging the Dice of individual patches.

---

# Backup: where every claim can be checked

| Topic | Code and saved evidence |
|---|---|
| Dataset sizes and split | [Synthetic manifests](../data/manifests), [synthetic audit](../reports/data_audit/faultseg3d_volume_statistics.csv), [Thebe HDF5 audit](../reports/data_audit/thebe_h5_statistics.csv) |
| Synthetic model/loss | [Baseline code](../scripts/faultseg3d_baseline.py), [baseline metrics](../runs/baseline_A_synthetic_bce_seed42/final_metrics.json), [loss metrics](../runs/loss_ablation_L1_weighted_bce_dice_seed42/final_metrics.json) |
| P1 attention and transfer | [P1 code](../scripts/attention3d_caft.py), [synthetic metrics](../runs/p1_attention3d_caft_seed42/final_metrics.json), [baseline transfer](../runs/baseline_A_zero_shot_thebe_full_20261005_095032/final_metrics.json), [P1 transfer](../runs/p1_zero_shot_thebe_full_20261009_162704/final_metrics.json) |
| CRACKS policies | [Evaluator](../scripts/evaluate_cracks_expert_zero_shot.py), [RGB results](../reports/evaluation/p1_cracks_combined_20261009_110136/final_metrics.json), [certain-only results](../reports/evaluation/p1_cracks_expert_seed42_20261009_134425/final_metrics.json) |
| R100 real-data training | [Original result](../runs/R100_thebe_seed42_20261005_102737/final_metrics.json), [clean trainer](../scripts/train_r100_fp16_clean.py), [three-seed report](07_R100_clean_three_seeds.md) |
| Frozen ensemble and curve | [Frozen test metrics](../reports/evaluation/r100_clean_frozen_test_20261019/final_metrics.json), [verification](../reports/evaluation/r100_clean_frozen_test_20261019/verification.json), [curve data](../reports/evaluation/r100_seed_curve_3models_20261019/curve.json), [plot for a slide](../reports/evaluation/r100_seed_curve_3models_20261019/curve.png), [additional-seed queue](../runs/R100_seed_saturation_pilot_20261019/queue_status.json) |
| Global Attention3D and denoising | [Imported architecture](../external/attention3d_paper/fault-detection-global-attention.py), [supervised report](09_paper_attention3d_supervised.md), [pilot comparison](../runs/attention3d_denoising_pilot_20261019_v2/comparison.json), [archived pilot code](../runs/attention3d_denoising_pilot_20261019_v2/source_snapshot/scripts/paper_attention3d_pilot.py) |
| SAM-Med3D | [Frozen full-test metrics](../reports/evaluation/sammed3d_frozen_thebe_20261016T011856768228130Z/final_metrics.json), [interactive validation](../reports/evaluation/sammed3d_interactive_validation_20261016T075908820714115Z/final_metrics.json), [adapter code](../scripts/train_sammed3d_thebe.py), [CPU preflight](../reports/evaluation/sammed3d_thebe_cpu_preflight.txt) |

The [technical report index](00_REPORT_INDEX.md) links the ten run-based experiment reports. Each report contains the detailed input/output pipeline, settings, metrics, limits, and simple definitions.
