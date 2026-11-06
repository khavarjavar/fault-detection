# Frozen clean R100 three-seed and ensemble test evaluation

Completed UTC: 2026-10-19T05:26:46.282430+00:00

All three seeds and the ensemble reproduced every saved full-validation histogram bin exactly before test HDF5 files were opened. Checkpoints and thresholds match the pre-existing frozen manifest. No training, checkpoint selection, threshold search, test-time augmentation, or overlapping inference was performed.

| Model | Best epoch | Frozen threshold | Test Dice | IoU | Precision | Recall | PR-AUC approx. | ROC-AUC approx. |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| seed42 | 95 | 0.316406250 | 0.524797 | 0.355745 | 0.451651 | 0.626213 | 0.542555 | 0.961577 |
| seed43 | 93 | 0.279296875 | 0.567466 | 0.396128 | 0.502357 | 0.651965 | 0.600605 | 0.966376 |
| seed44 | 95 | 0.244140625 | 0.565498 | 0.394212 | 0.508718 | 0.636545 | 0.595039 | 0.964450 |
| ensemble | — | 0.274902344 | 0.581257 | 0.409699 | 0.517305 | 0.663253 | 0.620308 | 0.970100 |

Three-seed test Dice: **0.552587 ± 0.024087** (sample SD). Ensemble is reported separately.

Test geometry: `(703, 3174, 1537)`; 1,950 tiles, 1,382 observed tiles, 3,429,541,914 raw voxels, **2,303,341,553 scored voxels**. Excluded no-data/padding does not enter metrics; 34,415 positive labels lie outside the raw-nonzero validity mask.

The ensemble is the equal-weight mean of FP32 probabilities from FP16-autocast inference in seed order 42, 43, 44. Each individual threshold and the ensemble threshold came from the previous full-validation selections. Metrics pool voxel counts; AUC uses the original 2048 bins. Per-patch CSV excludes no-data tiles, includes fault-free observed tiles, and marks undefined single-class ROC-AUC/no-positive PR-AUC as blank. Patch Dice follows the historical formula (both-empty Dice is zero); it is supplementary to pooled Dice.

This evaluates the existing Thebe test split, previously inspected for other experiments. Seed SD measures training variation on this split, not independent-survey generalization. Data fingerprints are size/mtime records plus unchanged source/checkpoint hashes, not new full-volume data hashes. Structural-distance metrics were not computed.

Evidence: `final_metrics.json`, `validation_reproduction.json`, `FROZEN_BEFORE_TEST.json`, `protocol.json`, `test_per_patch.csv`, validation/test histograms, `source_snapshot/`, and `console.log`.

Validation: six regression tests passed; all eight validation histograms reproduced exactly. Independent NumPy calculations and all 5,528 per-patch rows reconciled with the global results (maximum metric difference 1.11e-16). See `verification.json` and `checks.json`.

[Protocol and commands](../../experiments/R100_FROZEN_TEST_PROTOCOL_20261019.md).
