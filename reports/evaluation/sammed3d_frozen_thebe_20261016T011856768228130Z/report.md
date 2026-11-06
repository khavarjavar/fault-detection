# Frozen SAM-Med3D-Turbo on Thebe

Status: **complete**.

Original pretrained model; no adapter, weight updates, or training. Seismic preprocessing uses the R100 reader.
One-click results are oracle-assisted: GT patch presence determines positive/negative click type, and GT supplies its location. They are separate from automatic results.
Fault-free patches are included. All fault labels in each patch are scored; one click is not supplied per fault instance.
Global voxel metrics use non-overlapping 128³ patches and exclude raw no-data/padding. AUC metrics use 2048 bins.

| Split | Mode | Dice @ 0.5 | Val threshold | Dice @ val threshold | IoU | Precision | Recall | ROC-AUC (approx.) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| validation | no_prompts | 0.000931 | 0.014160156 | 0.054317 | 0.027917 | 0.027949 | 0.960226 | 0.502411 |
| validation | one_oracle_click | 0.000960 | 0.098632812 | 0.068658 | 0.035549 | 0.038608 | 0.309749 | 0.583263 |
| test | no_prompts | 0.000408 | 0.014160156 | 0.048805 | 0.025013 | 0.025042 | 0.955600 | 0.496594 |
| test | one_oracle_click | 0.000403 | 0.098632812 | 0.061343 | 0.031642 | 0.034110 | 0.304293 | 0.578207 |

Thresholds are selected only on full validation and saved before opening test. Fixed-0.5 results are also retained.
Evidence: protocol.json, threshold_selection.json, val_metrics.json, test_metrics.json, per-split click CSVs, evaluate.py, and console.log.
