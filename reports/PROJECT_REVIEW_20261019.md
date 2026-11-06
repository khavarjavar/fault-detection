# Project evidence review — 2026-10-19

**Follow-up completed 2026-10-19:** clean R100 held-out testing is now complete. Three-seed test Dice is **0.552587 ± 0.024087** (sample SD); the ensemble achieves **0.581257**. Validation reproduced exactly and independent checks passed. See the [test report](evaluation/r100_clean_frozen_test_20261019/report.md). The review below records the state before this follow-up; its references to pending R100 tests are historical.

Scope: local code, configurations, histories, metric JSONs, reports, source snapshots, archive inventories, and checkpoint file hashes in `/home/khavarj/projects/fault_detection`. This is a static and artifact-consistency review, not an independent GPU reproduction. No training or test evaluation was launched. Pending experiments supplied later may change the recommendation.

## Decision

Continue from the clean R100 baseline. Preserve the data, checkpoints, and historical results. Reorganize the experimental protocol and reporting before adding more model branches. The evidence does not justify discarding the project or restarting all training.

The strongest scientific observation is a synthetic-to-real transfer gap. A small supervised seismic model learns Thebe much better than the tested synthetic-only models or frozen medical model. This supports studying adaptation and label efficiency. It does not establish that any particular self-supervised method will improve results.

## What has actually been done

| Experiment | Training / evaluation domain | Recorded Dice | Evidence status |
|---|---|---:|---|
| Baseline A, ordinary BCE | FaultSeg3D synthetic / synthetic test | 0.821059 | Complete, one seed |
| Loss L1, weighted BCE + Dice | Same synthetic protocol / synthetic test | 0.819766 | Complete, one seed |
| P1, skip attention + connectivity focal Tversky + attention supervision | Synthetic / synthetic test | 0.826646 | Complete, one seed; changes both architecture and loss |
| Baseline A zero-shot | Synthetic / complete Thebe test | 0.085861 | Complete, synthetic-validation threshold |
| P1 zero-shot | Synthetic / complete Thebe test | 0.079128 | Complete, synthetic-validation threshold |
| Original R100 | Real Thebe from scratch / complete Thebe test | 0.542996 | Complete, historical resumed run |
| Clean R100 seed 42 | Real Thebe from scratch / full validation | 0.544072 | 100 epochs; test absent |
| Clean R100 seed 43 | Same / full validation | 0.569856 | 100 epochs; test absent |
| Clean R100 seed 44 | Same / full validation | 0.572980 | 100 epochs; test absent |
| R100 ensemble E0 | Existing three checkpoints / full validation | 0.588951 | Validation complete; test attempt aborted |
| Imported paper global-attention model, FP16 | Thebe / fixed 32 validation crops | 0.539004 best | Incomplete; later nonfinite losses |
| Imported paper global-attention model, BF16 | Thebe / fixed 32 validation crops | 0.309747 best | Incomplete; 65 history rows |
| Frozen SAM-Med3D, no prompts | Medical pretraining / complete Thebe test | 0.048805 | Validation-calibrated threshold; no adaptation |
| Frozen SAM-Med3D, one oracle click | Medical pretraining / complete Thebe test | 0.061343 | Oracle-assisted; not automatic |
| Frozen SAM interactive diagnostic | Selected Thebe validation crops | 0.174908 best calibrated five-click result | Oracle samples/clicks; validation only |

These rows are not one common leaderboard: synthetic tests, full real-survey tests, full validation, and selected validation crops answer different questions.

Primary result artifacts are `runs/*/final_metrics.json`, `runs/R100_fp16_clean_3seeds_20261014_150435/seed*/validation_selection.json`, and the report/evaluation directories named below.

## Data and evaluation foundation

Synthetic FaultSeg3D uses 180 training, 20 internal-validation and 20 official-test volumes, each 128 cubed. Fixed flips double the training samples to 360 per epoch. Recorded audit CSVs contain no duplicate seismic hashes and no duplicate label hashes across their rows. This checks historical audit records; source bytes were not rehashed in this review.

Thebe is converted from paired NPZ arrays to chunked HDF5, with binary-label checks, finite-input checks, source checksums in audit records, and atomic completion of converted files. The current reader concatenates numbered blocks along axis zero. Combined shapes are training `(900,3174,1537)`, validation `(200,3174,1537)`, and test `(703,3174,1537)`.

Full-volume evaluation uses non-overlapping 128-cube tiles, pads boundary tiles, and excludes padding from scoring. The complete test contains 3,429,541,914 raw voxels, of which 2,303,341,553 are scored under the R100 nonzero-input mask. The baseline, P1, and original R100 test confusion counts agree with that scoring population. Thebe foreground prevalence in that population is approximately 2.50%, making accuracy a poor headline metric.

The no-data audit provides evidence for large empty/muted survey regions. However, `raw != 0` remains a practical definition, not proof that every zero sample is missing data. The imported paper trainer instead preserves zeros between the first and last nonzero sample along each trace. This difference changes normalization and the metric population. Keep the historical R100 definition frozen for its pending evaluations. Evaluate any revised mask as a separate validation sensitivity study, ideally against acquisition metadata or an explicit survey mask.

The code assumes adjacent numbered Thebe files are spatially contiguous. Shape and filename checks do not prove physical adjacency or separation between the train/validation/test survey regions. Confirm coordinate provenance before making strong spatial-generalization claims. No cross-split voxel leakage was demonstrated by this review; physical independence remains unverified.

## R100 is the best continuation point

The clean trainer constructs `baseline.FaultSeg3D()` with fresh initialization; it does not load synthetic pretrained weights. This resolves the older report's uncertainty about initialization at the source-code/configuration level.

It uses 1,459,585 parameters, masked BCE, Adam at 1e-4, 128-cube patches, FP16 autocast with gradient scaling, 360 training patches per epoch, and gradient accumulation of two. Checkpoint selection uses highest PR-AUC on a shared fixed validation subset, then threshold selection uses best Dice on full validation. The reported full-validation Dice does not mean the checkpoint was selected on full-volume Dice.

All three histories contain 100 epochs. Their PR-AUC-best epochs exactly match the saved selections: 95, 93, and 95. Protocol hashes match across seeds. Current best-checkpoint SHA256 hashes match the ensemble's frozen manifest. Validation Dice mean and sample SD are 0.562302 and 0.015865. Three seeds quantify initialization/sampling variation under one dataset split, not uncertainty across independent surveys.

The ensemble validation artifact reports Dice 0.588951, exceeding the best individual seed by 0.015971. Its threshold is frozen at 0.27490234375. Its reproduced member metrics have zero recorded delta from the individual results. This is a useful low-cost candidate, but the gain is still validation-only.

The ensemble console ends with `RuntimeError: Unexpected test shape: (703, 3174, 1537)`. That is the known test shape. No ensemble test metrics were found. The evaluator evidently rejected the test geometry; do not infer a numerical model failure or invent a test result. The exact evaluator used through stdin was not found as a standalone source in the output directory, so reconstruct and archive it before resuming. The validation JSON says test files were not opened at freeze time; the later exception establishes that the subsequent attempt reached test shape inspection.

The three-seed readiness report separately aborts with `KeyError: 'dice'`. The metric lives under `full_validation`, so a failed readiness wrapper is not evidence that the training failed.

The original R100 result remains useful historical evidence, but selection policy changed on resume at epoch 23 and RNG/scaler state was not fully restored. Use clean runs for future controlled comparisons.

## Attention experiments need careful interpretation

P1 in `scripts/attention3d_caft.py` adds two supervised skip gates to the small U-Net and changes the loss to a node-edge focal Tversky statistic plus attention-map Smooth L1. It has 1,467,411 parameters. It is distinct from the imported global-attention architecture with 45,001,057 parameters.

P1 improves synthetic test Dice by only 0.005586 over Baseline A in one seed. Its reported synthetic PR-AUC falls from about 0.8905 to 0.7333 and ROC-AUC from about 0.9852 to 0.9397. The selected threshold rises to 0.980957. This combination warrants inspecting score distributions and histogram resolution near saturation before diagnosing ranking versus calibration. The implementation uses FP32 sigmoid after mixed-precision inference, but fixed-width probability histograms can still merge highly saturated scores. Do not explain the AUC change purely as calibration: exact rank AUC is invariant to strictly monotonic recalibration, whereas binning and saturation can affect the approximation.

Its full Thebe zero-shot Dice is worse than Baseline A (0.079128 versus 0.085861). Thus the existing P1 evidence does not support improved real-data transfer. Separate attention-only, loss-only, and combined ablations would be needed to attribute an effect.

The imported paper trainer uses 64-cube crops, 64 training patches per epoch, 32 fixed validation patches, a different mask/orientation convention, AdamW and a different loss. R100's nominal per-epoch input voxel budget is 45 times larger: `360*128^3 / (64*64^3)`. This is not a compute-equivalence calculation; the paper model is much larger. Direct comparison of its crop Dice to R100 full-volume Dice is invalid.

The FP16 history first records a nonfinite validation loss at epoch 74, then nonfinite training and validation losses through epoch 77. A finite Dice in those rows is not proof of valid predictions because comparisons with NaN logits can silently produce false values. The best epoch 70 predates those recorded failures but needs checkpoint/output checks before reuse. The BF16 run records finite losses through epoch 65 and a best epoch 61; the log stops during epoch 66 without proving the termination cause. Neither is a completed paper reproduction. The runs explicitly omit denoising pretraining.

## SAM-Med3D evidence

The frozen evaluations are complete and distinguish automatic output from label-assisted clicks. They use full validation for threshold selection before test, record hashes, and exclude padding/no-data. Automatic test Dice 0.048805 is close to the approximately 0.04886 Dice obtained by predicting every scored voxel as fault at this foreground prevalence; ROC-AUC is 0.496594. This is strong evidence that this particular frozen setup has little useful automatic discrimination on Thebe.

One oracle click raises calibrated test Dice to 0.061343, still weak. The later interactive diagnostic obtains 0.174908 only on label-centered validation crops with five corrective clicks and validation threshold calibration. Label-derived crop selection, overlaps, and corrective clicks prevent comparison with automatic whole-survey R100.

This does not establish that all SAM adaptation will fail. `train_sammed3d_thebe.py` implements a separate frozen-encoder residual adapter plus trainable decoder/no-mask embedding. The CPU preflight records about 100.6 million total and 7.65 million trainable parameters, with GPU execution false. No completed adapter training result was found. Treat this as implementation readiness, not an achieved result, and do not call it a reproduction of Seismic Fault SAM.

## CRACKS is not yet a stable benchmark

Two result directories use materially different target/validity policies. The certain-only run reports Dice 0.057553, treating raw 1 as background and raw 3 as foreground while ignoring raw 0 and 2. The combined run reports 0.035273, decoding green/blue as foreground and scoring every other pixel as background. Current `evaluate_cracks_expert_zero_shot.py:119-126` implements the latter; preprocessing still defines another raw-index policy.

PNG palette indices can vary between files, and treating unknown pixels as background changes the question being measured. Choose the intended annotation semantics from the dataset documentation and actual palettes before adopting either metric. Preserve both historical results with explicit policies.

The evaluator also stacks 396 display PNG sections as a pseudo-volume, converts them to grayscale, and compresses four missing nominal slice positions. That differs from native raw seismic sampling and is an additional transfer limitation. These scores cannot isolate architecture quality and do not establish dense 3D performance.

## Engineering and scientific gaps to address

- Root-level source versioning is absent according to existing git audits; `src/` and `configs/` are empty while scripts, backups, kits and snapshots contain the working implementations. Preserve hashes and archive history, then introduce version control and one canonical implementation per protocol.
- README and the experiment naming roadmap omit newer ensemble/interactive findings or describe obsolete statuses. Add one experiment index with model identity, initialization, labels used, split, mask, threshold source, and completion status.
- Frozen R100 dependencies are hash-pinned, which protects old experiments from accidental evaluator edits. Retain that benefit while reducing duplicated readers and metric implementations for future experiments.
- FP16 GradScaler legitimately skips overflowing updates. The clean trainer records neither skipped-update counts nor scale evolution, so absence of numerical exceptions does not prove every intended optimizer update occurred. Add that telemetry to new runs, preserving the completed run's recipe.
- Three-seed configurations fingerprint data size/mtime rather than HDF5 contents. Existing source checksums help provenance, but a full content/coordinate manifest would support stronger reproducibility claims.
- Non-overlap tiling may introduce edge artifacts. Investigate overlap-and-blend inference on validation only as an explicit new inference protocol.
- Patch-averaged Dice and pooled voxel Dice differ substantially in sparse data. Report both with fault-present/fault-absent strata; do not interpret a zero median patch Dice alone as whole-survey failure. Undefined AUC on single-class patches should be reported as undefined, rather than averaged as zero.
- Existing test results have been inspected across multiple experiments. No direct use of test labels for threshold selection was established, but the same survey test cannot now be described as completely untouched by the overall research process. Freeze future decisions on validation and seek an additional spatial holdout or survey for final generalization evidence.

## Recommended path and decision gates

1. Close the existing baseline evidence. Repair/archive the ensemble evaluator's geometry check and readiness JSON handling. Keep the saved checkpoints and thresholds fixed. Evaluate the three clean seeds and ensemble once on the existing test protocol, recording expected `(703,3174,1537)` geometry and 2,303,341,553 scored voxels. Do not retrain these baselines merely to repair evaluation tooling.
2. Resolve data semantics on validation: coordinate provenance, no-data mask, label alignment, fault thickness and patch-boundary examples. Use a small fixed visual panel plus quantitative sensitivity checks. Any protocol revision gets a new experiment ID and a matched baseline.
3. Make real-label efficiency the first controlled research direction. Compare the same small U-Net from random initialization with synthetic-pretrained initialization under matched real-label budgets, for example nested spatially separated 1%, 5%, 10%, and 100% labelled regions. Define percentages by labelled region/voxel coverage, not repeated random patch counts. Keep evaluation and sampling budgets matched and run seeds 42/43/44 for finalist comparisons.
4. Test seismic self-supervised pretraining only after that adaptation baseline. Pretrain on the permitted training-region raw data and compare against random and synthetic initialization using the same backbone and fine-tuning budget. Evaluate low-label performance and resource cost. Do not introduce attributes, EMA teachers, distance heads and new attention simultaneously.
5. Use validation to choose the next branch. Continue an intervention only if gains are consistent across seeds and useful on difficult spatial regions without unacceptable false positives or compute cost. There is no universal meaningful Dice-gain cutoff; define one before seeing new test results.

If the intended goal is highest in-domain performance, prioritize R100, ensemble completion and controlled inference/sampling changes. If the intended goal is a research contribution, prioritize label-efficient adaptation and then SSL. If the goal is faithfully reproducing the global-attention paper, use a separate track with the actual pretraining and full evaluation protocol. Freeze SAM adaptation as an optional pilot until its validation evidence justifies its cost.

## Checks performed and limits

All 15 primary Python scripts parse successfully with Python AST. Recorded synthetic manifests have the expected 180/20/20 sizes, and historical audit hashes contain no duplicates. Checked result Dice values agree with saved confusion counts. Clean-seed history selections, protocol hashes and current checkpoint file hashes agree with the frozen ensemble manifest. These checks do not verify checkpoint tensor contents, fresh model predictions, full raw-data identity, spatial independence, or paper fidelity. No runtime training/inference tests were performed.

The immediate decision is therefore to keep the working foundation and finish its evidence. A new experimental plan is warranted; a total project restart is not supported by the current artifacts.
