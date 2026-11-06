# R100 test evaluation, explained

This document explains how we checked three already-trained R100 models on Thebe seismic data. A **protocol** is simply the set of rules followed during that evaluation.

**Status: completed on 19 October 2026.** The results and independent checks passed. You can read the saved results without running the models again.

## 1. What was the aim?

We wanted to answer two questions:

1. How well does each trained model detect faults in the test data?
2. Does averaging their predictions give a better result?

[evaluate_r100_frozen_test.py](../../scripts/evaluate_r100_frozen_test.py) loads saved models, predicts faults, compares the predictions with existing fault labels, and writes the results. It does **not** train the models again.

## 2. What do the main words mean?

| Word | Meaning here |
|---|---|
| Voxel | One cell in a 3D seismic volume, like a pixel in a 3D image. |
| Seed | A number controlling training randomness. Seeds 42, 43, and 44 produced three versions of the same model design. |
| Checkpoint | A file containing a model saved during training. We load each model's previously selected best checkpoint. |
| Epoch | One training round. A checkpoint from epoch 95 was saved after training round 95. This evaluation does not repeat those rounds. |
| Validation data | Data used earlier to choose checkpoints and decision thresholds. Here it was used again to check that the code reproduces the saved results. |
| Held-out test data | A separate split that was not used to train these models or choose their thresholds. |
| Frozen | Model weights and decision thresholds stay fixed during evaluation. |
| Inference | Running a trained model to produce predictions. |
| Dice | A score measuring overlap between predicted and labelled faults. Higher is better; 1 means perfect overlap. It is not the percentage of all voxels classified correctly. |

## 3. How does the ensemble work?

Each model predicts a fault probability between 0 and 1 for each voxel. We average the probabilities at the same location:

```text
ensemble probability = (seed42 probability + seed43 probability + seed44 probability) / 3
```

For example, `0.2`, `0.4`, and `0.6` give an average of `0.4`.

A **threshold** converts the probability into a fault/no-fault decision. For this ensemble, an average of at least `0.27490234375` means fault. The threshold was chosen earlier using validation data and stayed unchanged during testing.

We average predictions first, then calculate the ensemble's Dice. This is different from averaging three Dice scores.

## 4. What happened during the run?

1. **Check the inputs.** Confirm that saved models, settings, and dataset files match earlier records. File hashes act as fingerprints to detect changed model files or source code. Dataset checks use file sizes and modification dates.
2. **Reproduce validation.** Run the three models on the full validation volume again. Compare with the previously saved results. Stop before test inference if they differ.
3. **Evaluate test data.** Read one small cube at a time and run all three models. Calculate the ensemble from those same predictions; it does not require a fourth model run.
4. **Save and verify.** Save scores and counts. A separate verifier recalculates the scores from saved evidence without predicting the dataset again.

Expected test-file sizes and dates are stored in the R100-specific [test-data manifest](../../configs/r100_test_data_manifest.json). This evaluation uses only the three R100 models; it has no SAM-Med3D dependency.

Validation took about **2 minutes**, and the test pass took about **7.4 minutes**. The averaging was a small part of the work. The program also read and prepared the seismic data, ran three networks, and scored billions of voxels.

## 5. What were the results?

| Model | Saved training epoch | Fixed threshold | Test Dice |
|---|---:|---:|---:|
| Seed 42 | 95 | 0.31640625000 | 0.524797 |
| Seed 43 | 93 | 0.27929687500 | 0.567466 |
| Seed 44 | 95 | 0.24414062500 | 0.565498 |
| Average of the three predictions: ensemble | — | 0.27490234375 | **0.581257** |

The three individual models had mean Dice **0.552587** and sample standard deviation **0.024087**. Standard deviation describes how much their scores varied. The ensemble is a separate result, so it is not included as a fourth seed.

The ensemble scored higher than each individual model on this test split. That does not guarantee the same improvement on another survey.

[Read the full results report](../evaluation/r100_clean_frozen_test_20261019/report.md).

## 6. Did the checks run the dataset repeatedly?

| Check | What it used |
|---|---|
| Six code tests | Small synthetic examples and known dimensions. No Thebe model inference. |
| Validation reproduction | Real validation data, evaluated again before testing. |
| Test evaluation | One test pass per model. The ensemble reused those predictions. |
| Independent result verification | Saved counts, histograms, and CSV rows. No model inference. |

The six code tests covered reading cubes, padding, threshold boundaries, detecting incorrect counts, and calculating seed statistics.

Validation matched all **eight saved histograms** exactly. A histogram groups predictions into 2,048 probability bins and counts the true fault/background labels in each bin. There are two histograms for each of four outputs: three models plus the ensemble.

The independent verifier recalculated scores and checked that all **5,528 per-cube rows** add up to the whole-volume counts. Several scores, such as Dice, precision, and recall, reuse the same predictions; each score does not require another model run.

## 7. How was the volume handled?

The volume was divided into **128 × 128 × 128** cubes without overlap. Smaller boundary cubes were filled out with zeros so the model could accept them. Those added values were excluded from scoring.

The existing R100 rule also excludes raw seismic values equal to zero as no-data. Each cube is normalized using its remaining values, and its axes are put in the order expected by the model. This follows the earlier R100 implementation.

| Coverage check | Expected and verified value |
|---|---:|
| Test volume dimensions | 703 × 3,174 × 1,537 |
| Total cubes visited | 1,950 |
| Cubes containing usable seismic values | 1,382 |
| Original voxels in the test volume | 3,429,541,914 |
| Voxels included in scoring, per output | 2,303,341,553 |
| Labelled fault voxels included in scoring | 57,680,496 |
| Labelled fault voxels excluded by the no-data rule | 34,415 |

The program stops if required counts differ or model outputs contain invalid numbers. It prevents simultaneous copies from running and refuses to overwrite an existing output folder.

For technical reference: GPU prediction uses FP16 autocast; probabilities and their average use FP32. These are number formats used for calculation. There was no new training, threshold search, overlapping blending, or flipped-input prediction. This run did not calculate structural-distance scores or save full 3D prediction maps.

## 8. Where are the results, and what can I run?

| Saved file | What to use it for |
|---|---|
| [report.md](../evaluation/r100_clean_frozen_test_20261019/report.md) | Read the results in a table. Start here. |
| [final_metrics.json](../evaluation/r100_clean_frozen_test_20261019/final_metrics.json) | Get exact scores and coverage counts for analysis. |
| [verification.json](../evaluation/r100_clean_frozen_test_20261019/verification.json) | Confirm that independent verification passed. |
| [test_per_patch.csv](../evaluation/r100_clean_frozen_test_20261019/test_per_patch.csv) | Inspect results for individual cubes. |
| [protocol.json](../evaluation/r100_clean_frozen_test_20261019/protocol.json) | Inspect the exact settings and file fingerprints. |

To recheck the code and saved results, run these commands from `/home/khavarj/projects/fault_detection`. They do not run predictions on Thebe:

```bash
# Six small code tests.
.venv_train/bin/python -u tests/test_r100_frozen_evaluation.py

# Check saved results without model inference.
.venv_train/bin/python -u scripts/verify_r100_frozen_result.py \
  reports/evaluation/r100_clean_frozen_test_20261019
```

For reference, this is the evaluation command already used:

```bash
.venv_train/bin/python -u scripts/evaluate_r100_frozen_test.py \
  --output-dir reports/evaluation/r100_clean_frozen_test_20261019
```

That output folder already exists, so the command will now refuse to overwrite it. Reading the results does not require another evaluation. The optional `--validation-only` flag runs real validation inference but skips test inference; it also requires a new output folder.

## 9. What are the limits?

The existing Thebe test split had already been examined in other experiments. This run kept the R100 checkpoints and thresholds fixed, but it does not provide evidence from a new survey. Variation across three seeds describes training randomness on this dataset, not performance across different surveys.

Exact validation reproduction confirms consistency with the earlier code. It does not prove that every zero seismic value is missing data. Dataset size/date checks also do not replace full checks of file contents.
