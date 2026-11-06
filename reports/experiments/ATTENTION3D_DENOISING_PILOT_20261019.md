# Attention3D: decision and short denoising pilot

19 October 2026. The user's attached roadmap was checked against the local project and the authors' sources. The new user instruction authorizes starting a bounded run; it supersedes the attachment's older setup-only instruction.

## Decision

Try the paper's two-stage idea in a small, controlled Attention3D experiment. The existing five-seed R100 study continues independently.

This pilot uses the full local 45,001,057-parameter global-attention architecture, rather than the small R100 model or the custom skip-attention model. It uses denoising followed by supervised training, plus a matched scratch control. It is an **in-domain adaptation and an early learning check**, not a complete paper reproduction or a replacement for the frozen R100 ensemble.

The paper's external pretraining surveys and pretrained denoising weights were not found locally. Using Thebe training seismic substitutes the available data for those surveys. That change must remain explicit.

## Corrections to the attached roadmap

| Proposed stage | Actual state and next action |
|---|---|
| Recover state | Local scripts, configurations, histories and active jobs inspected. No completed denoising-to-segmentation run was found. |
| Repair/evaluate E0 | Already completed. The frozen three-seed ensemble has validation Dice **0.588951** and held-out test Dice **0.581257**. Preserve that result; no new test evaluation is needed now. |
| Audit data and errors | Partly complete. Array shape, input normalization, masks, and file identities are inspectable. Physical survey coordinates and a verified acquisition mask are still unavailable. Do not claim certified spatial independence or new-survey generalization. |
| E3 on R100 | Still a separate proposed experiment. The new attention pilot does **not** establish that R100 E3 has been done. |
| Full attention reproduction | Not ready for a fidelity claim: external pretraining data/weights and the exact paper-to-source training provenance remain unresolved. The bounded local adaptation can test implementation and early learning. |
| C1/C2 then F0/F1 | These labels were not defined in the inspected experiment notes. Do not automatically launch a sequence whose controls are unclear. |
| Replication and final ensemble | Conditional on useful validation evidence from a completed candidate. No automatic architecture sweep or further seeds are scheduled. |

The original FP16 attention run contains nonfinite losses from epoch 74 onward. The BF16 attempt has finite recorded losses through epoch 65, but no completed training record. Both explicitly omit denoising pretraining. Neither proves completion of the paper pipeline.

The five-seed baseline means seeds 42–46. Seeds 45 and 46 are being trained by the existing R100 pipeline. The historical three-seed ensemble and its thresholds remain frozen.

The first launch stopped before training because its proposed internal-validation band was entirely no-data. Its records remain in `runs/attention3d_denoising_pilot_20261019`. Sparse training-seismic-only profiles identified populated regions; the corrected preflight verified all eight internal-validation and all 32 downstream-validation crops before relaunch. See [the training footprint audit](../data_audit/attention3d_pretext_footprint_20261019.json).

## What is running

Run folder: [`runs/attention3d_denoising_pilot_20261019_v2`](../../runs/attention3d_denoising_pilot_20261019_v2).

| Stage | Input and objective | Budget |
|---|---|---:|
| Denoising | Add Gaussian noise to training seismic; reconstruct the original field patch using masked MSE | 256 patches / 64 AdamW updates |
| Scratch control | Fresh Attention3D weights; supervised fault segmentation | 512 patches / 128 updates |
| Fine-tuning | Load denoising features, reset the output head and optimizer; supervised fault segmentation | 512 patches / 128 updates |

The scratch and fine-tuning arms use identical deterministic supervised crop streams, seed 42, optimizer, loss, precision, learning-rate schedule, and update count. A crop-stream hash must match before the final comparison is accepted. Initialization is the intervention. Pretraining adds compute; this is not an equal-total-compute claim.

Settings:

- 64³ patches, batch size one, gradient accumulation four.
- BF16 autocast, FP32 weights/losses, gradient clipping at norm 1.0.
- Authors' Unified Focal Loss for both segmentation arms; masked MSE for denoising.
- AdamW, weight decay 1e-4; peak learning rate 1e-4 for pretraining and 5e-4 for both supervised arms; a short slanted triangular schedule in each stage.
- Valid samples are finite and nonzero, with valid-only patch z-score and reversed axes, following the established R100 conventions. The older paper adaptation used a different mask, so its crop scores are not a numerical control for this run.
- Half the supervised patch indices require an observed positive label; the other half sample uniformly from usable patches. Both arms use the same rule and crop positions.
- All feature tensors and buffers must load exactly. Only the output head is deliberately fresh. Missing/unexpected/mismatched tensors cause failure.
- All layers are trainable. Layer-wise learning-rate decay and gradual unfreezing are deliberately absent from this first comparison, so it isolates initialization. Those paper components require separate controls later.

This budget is much shorter than the old attention runs or R100's 36,000 supervised patches. A low early Dice is not a converged result. A successful pilot establishes that the two-stage implementation runs and provides preliminary validation behavior; it does not establish the final accuracy of the paper method.

## Data separation

Only `train1.h5` through `train9.h5` supply pretraining values. Fault labels are not read by pretext sampling.

Within each training array, pretext-fit crops stay entirely inside stored axis 1 coordinates `[64, 1024)`. Internal reconstruction-validation crops stay inside `[1280, 1536)`. The unused 256-voxel band separates their full crop supports. This is a separation in stored array coordinates; the absent physical survey mapping prevents stronger geological independence claims.

Supervised training can use the original training region, including the internal reconstruction-validation area. That area is still part of the original supervised training split.

Downstream validation uses 32 fixed usable crops, alternating `val1.h5` and `val2.h5`. These downstream validation values never enter denoising or supervised optimization. No `test*.h5` file is opened by this pilot.

## Metrics and interpretation

During denoising, record training loss, gradient norm, optimizer updates, elapsed time, and masked reconstruction MSE on eight fixed internal-validation patches. Also record the MSE obtained by simply returning the noisy input. A network that performs worse than that identity baseline has not demonstrated useful denoising under this check. The reconstruction target retains the original field noise; it is not certified noise-free seismic.

For both segmentation arms, evaluate after every 128 training patches. Select the checkpoint with the highest approximate PR-AUC on the fixed 32 validation crops. The approximation is stepwise precision-recall area from 2048 probability bins.

For each saved evaluation, record:

- Dice, IoU, precision, recall, confusion counts and scored voxel count.
- Best-Dice threshold selected on these same validation crops, plus metrics at threshold 0.5.
- Per-volume metrics at the common aggregate-selected threshold.
- Positive and negative probability histograms and mean patch BCE.

The final comparison uses each arm's selected checkpoint and its own validation-selected threshold. These are **crop-based development scores**; crops may overlap, and their voxels are not independent replicates. They are not directly comparable with full-volume R100 Dice or with the paper's reported scores. The roadmap's proposed +0.01 full-validation screening rule is not applied to this short pilot.

## GPU feasibility and limits

The full model passed two real 64³ training updates while seed 45 was running:

- Updates took 8.25 and 7.89 seconds, excluding input loading.
- Peak allocated memory was 5.12 GiB; peak reserved memory was 5.79 GiB.
- Model parameters and gradients stayed finite; every optimizer state advanced twice.
- Seven focused CPU tests passed: masking/axes, separate pretext crop supports, corruption, exact feature/buffer transfer, transfer rejection, threshold metrics, deterministic paired sampling and no pretext label access.
- Two subprocess tests also passed: the supervisor's hard stop terminates only its own child, and a failed child cannot generate a completed result report. [Verification record](../../runs/attention3d_denoising_pilot_20261019_v2/post_launch_checks.json).

The corrected launch subsequently completed its first 16 real denoising patches and four optimizer updates, with finite loss and gradient norm. This verifies initial training progress, not completion of pretraining or the later transfer stage.

The new process is capped at 40% of GPU memory through PyTorch's allocator. This is not GPU partitioning or compute isolation. Concurrent execution can slow either experiment; future memory demand can also change. Failures stop the new pilot and are recorded. The supervisor does not signal or modify existing jobs.

The model uses fused all-to-all attention and disallows the dense math fallback. The often-quoted 1 TiB calculation concerns a hypothetical stored dense score tensor for one 64³ layer with eight FP16 heads; it is not the measured footprint above. Fused attention avoids that full tensor but retains expensive pairwise computation.

Launch: **11:31 Asia/Baku**. Training-only estimate from the preflight is 2.87 hours; loading, validation and contention add time. The worker checks a 3.5-hour budget, and a supervisor enforces a four-hour wall limit, with up to 30 seconds allowed for shutdown. No further experiments launch automatically.

## Files to follow

- [Current stage](../../runs/attention3d_denoising_pilot_20261019_v2/state.json)
- [Training log](../../runs/attention3d_denoising_pilot_20261019_v2/training.log)
- [Latest training metrics](../../runs/attention3d_denoising_pilot_20261019_v2/progress.json)
- [Frozen launch settings and source hashes](../../runs/attention3d_denoising_pilot_20261019_v2/launch_plan.json)
- [GPU preflight](../../runs/attention3d_denoising_pilot_20261019_v2/gpu_preflight.json)
- [Supervisor status](../../runs/attention3d_denoising_pilot_20261019_v2/supervisor_state.json)
- [Result report](../../runs/attention3d_denoising_pilot_20261019_v2/report.md), written after successful completion.

Check `transfer_report.json` after the fine-tuning stage begins. Successful completion writes `comparison.json` and `report.md`. A failed or budget-stopped run is not labelled complete. The source snapshot and historical records are retained.

To launch this prepared run, the supervisor command was:

```bash
.venv_train/bin/python -u scripts/run_paper_attention3d_pilot.py
```

It is already running. Duplicate-launch checks reject another start in this run directory.

## What to decide afterward

First check reconstruction quality, finite updates, exact transfer, matched supervised crops, per-volume validation behavior and measured cost. Useful evidence can justify a longer matched attention comparison. A weak short result can reflect insufficient training; it does not justify claiming that the paper fails. An implementation error should be repaired before interpreting Dice.

After the five-seed curve finishes, decide between a longer attention experiment and the smaller controlled R100 denoising pilot. Keep the alternatives distinct. Replicate a promising completed recipe before adding it to an ensemble; use validation to choose it and freeze thresholds before any new held-out evaluation.

## Sources

The [paper](https://www.nature.com/articles/s41598-026-54829-x) describes multi-survey denoising followed by discriminative fault-segmentation transfer. The [author segmentation repository](https://github.com/Matin-Mahzad/fault-detection-global-attention) and [denoising implementation](https://github.com/Matin-Mahzad/3D_Global_Attention/blob/main/GlobalAttention3D.py) are distinct releases. Local execution pins the segmentation repository's clean commit `2a3d69a5d99dfc191508cbceea3db3b95242f216`, source SHA256 `dc332c431b035c590141f0e542573d9445dfdae65a232cbe799516be8df18b37`.

The [project review](../PROJECT_REVIEW_20261019.md), [completed frozen test report](../evaluation/r100_clean_frozen_test_20261019/report.md), and [seed-size study](R100_SEED_SATURATION_20261019.md) provide the local baseline evidence. The attached roadmap is a proposal with outdated state, not an execution record.
