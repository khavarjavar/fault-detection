# Three-seed evidence audit

Generated UTC: 2026-10-16T00:14:42+00:00

## Git state

```text
fatal: not a git repository (or any parent up to mount point /)
Stopping at filesystem boundary (GIT_DISCOVERY_ACROSS_FILESYSTEM not set).
fatal: not a git repository (or any parent up to mount point /)
Stopping at filesystem boundary (GIT_DISCOVERY_ACROSS_FILESYSTEM not set).
```

## Seed 42

### Seed/run files

```text
reports/attention3d_identity_audit_20261014.txt
reports/evaluation/p1_attention3d_caft_seed42_to_thebe_smoke_20261009/final_metrics.json
reports/evaluation/p1_attention3d_caft_seed42_to_thebe_smoke_20261009/run_configuration.json
reports/evaluation/p1_attention3d_caft_seed42_to_thebe_smoke9_20261009/final_metrics.json
reports/evaluation/p1_attention3d_caft_seed42_to_thebe_smoke9_20261009/prediction_examples/example_01_x0000_y0000_z0640.npz
reports/evaluation/p1_attention3d_caft_seed42_to_thebe_smoke9_20261009/prediction_examples/example_02_x0000_y0000_z0768.npz
reports/evaluation/p1_attention3d_caft_seed42_to_thebe_smoke9_20261009/prediction_examples/example_03_x0000_y0000_z0896.npz
reports/evaluation/p1_attention3d_caft_seed42_to_thebe_smoke9_20261009/prediction_examples/example_04_x0000_y0000_z1024.npz
reports/evaluation/p1_attention3d_caft_seed42_to_thebe_smoke9_20261009/run_configuration.json
reports/evaluation/p1_attention3d_caft_seed42_to_thebe_smoke9_20261009/test_per_patch.csv
reports/evaluation/p1_cracks_expert_seed42_20261009_134425/expert_per_section.csv
reports/evaluation/p1_cracks_expert_seed42_20261009_134425/final_metrics.json
reports/evaluation/r100_readiness_20261005_101611/audit.txt
reports/paper_attention3d_thebe_supervised_seed42.log
reports/r100_launch_check_20261014_133445.txt
reports/training/baseline_A_synthetic_bce_seed42.log
reports/training/baseline_A_synthetic_bce_seed42.pid
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.pid
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log
reports/training/paper_attention3d_thebe_supervised_seed42_resume.pid
reports/training/r100_fp16_3seed_queue_20261014_145225.log
reports/training/r100_fp16_3seed_queue_20261014_145510.log
reports/training/r100_fp16_3seed_queue_20261014_150435.log
reports/training/R100_thebe_seed42_20261005_102737.log
reports/training/R100_thebe_seed42_20261005_102737.pid
reports/training/R100_thebe_seed42_resume_20261005_131346.log
reports/training/R100_thebe_seed42_resume_20261005_131346.pid
runs/baseline_A_smoke/run_config.json
runs/baseline_A_synthetic_bce_seed42/best.pt
runs/baseline_A_synthetic_bce_seed42/final_metrics.json
runs/baseline_A_synthetic_bce_seed42/history.csv
runs/baseline_A_synthetic_bce_seed42/last.pt
runs/baseline_A_synthetic_bce_seed42/run_config.json
runs/baseline_A_synthetic_bce_seed42/test_per_volume.csv
runs/baseline_A_synthetic_bce_seed42/validation_per_volume.csv
runs/loss_ablation_L1_weighted_bce_dice_seed42/best.pt
runs/loss_ablation_L1_weighted_bce_dice_seed42/final_metrics.json
runs/loss_ablation_L1_weighted_bce_dice_seed42/history.csv
runs/loss_ablation_L1_weighted_bce_dice_seed42/last.pt
runs/loss_ablation_L1_weighted_bce_dice_seed42/pid.txt
runs/loss_ablation_L1_weighted_bce_dice_seed42/run_config.json
runs/loss_ablation_L1_weighted_bce_dice_seed42/test_per_volume.csv
runs/loss_ablation_L1_weighted_bce_dice_seed42/validation_per_volume.csv
runs/p1_attention3d_caft_seed42/best_p1_attention3d_caft_seed42_epoch093_faultseg3d_synthetic_20261009.pt
runs/p1_attention3d_caft_seed42/best.pt
runs/p1_attention3d_caft_seed42/final_metrics.json
runs/p1_attention3d_caft_seed42/history.csv
runs/p1_attention3d_caft_seed42/last.pt
runs/p1_attention3d_caft_seed42/run_config.json
runs/p1_attention3d_caft_seed42/test_per_volume.csv
runs/p1_attention3d_caft_seed42/train.log
runs/p1_attention3d_caft_seed42/train.pid
runs/p1_attention3d_caft_seed42/validation_per_volume.csv
runs/paper_attention3d_thebe_smoke_20261009_170246/run_configuration.json
runs/paper_attention3d_thebe_supervised_seed42/best.pt
runs/paper_attention3d_thebe_supervised_seed42_bf16_clean/best.pt
runs/paper_attention3d_thebe_supervised_seed42_bf16_clean/history.csv
runs/paper_attention3d_thebe_supervised_seed42_bf16_clean/last.pt
runs/paper_attention3d_thebe_supervised_seed42_bf16_clean/run_configuration.json
runs/paper_attention3d_thebe_supervised_seed42/history.csv
runs/paper_attention3d_thebe_supervised_seed42/last.pt
runs/paper_attention3d_thebe_supervised_seed42/run_configuration.json
runs/R100_fp16_clean_3seeds_20261014_145225/queue_status.json
runs/R100_fp16_clean_3seeds_20261014_145510/queue_status.json
runs/R100_fp16_clean_3seeds_20261014_145510/seed42.log
runs/R100_fp16_clean_3seeds_20261014_145510/seed42/run_config.json
runs/R100_fp16_clean_3seeds_20261014_145510/smoke.log
runs/R100_fp16_clean_3seeds_20261014_145510/smoke_seed42/best.pt
runs/R100_fp16_clean_3seeds_20261014_145510/smoke_seed42/history.csv
runs/R100_fp16_clean_3seeds_20261014_145510/smoke_seed42/last.pt
runs/R100_fp16_clean_3seeds_20261014_145510/smoke_seed42/run_config.json
runs/R100_fp16_clean_3seeds_20261014_145510/smoke_seed42/status.json
runs/R100_fp16_clean_3seeds_20261014_145510/smoke_seed42/validation_selection.json
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/best.pt
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/history.csv
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/last.pt
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/run_config.json
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/status.json
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/validation_selection.json
runs/R100_fp16_clean_3seeds_20261014_150435/smoke.log
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/best.pt
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/history.csv
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/last.pt
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/run_config.json
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/status.json
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/validation_selection.json
runs/R100_thebe_seed42_20261005_102737/best.pt
runs/R100_thebe_seed42_20261005_102737/final_metrics.json
runs/R100_thebe_seed42_20261005_102737/history.csv
runs/R100_thebe_seed42_20261005_102737/last.pt
runs/R100_thebe_seed42_20261005_102737/resume_protocol.json
runs/R100_thebe_seed42_20261005_102737/run_config.json
runs/R100_thebe_seed42_20261005_102737/test_per_patch.csv
runs/R100_thebe_seed42_20261005_102737/validation_selection.json
scripts/r100_full_run_ex.py
scripts/r100_full_run.py
scripts/train_r100_fp16_clean.py
```

### Checkpoint metadata only

```text
2026-09-30T14:59:43.5718456000	17547349 bytes	runs/baseline_A_synthetic_bce_seed42/last.pt
2026-09-30T14:59:43.6028961610	17547349 bytes	runs/baseline_A_synthetic_bce_seed42/best.pt
2026-10-02T11:43:42.9153143300	17547349 bytes	runs/loss_ablation_L1_weighted_bce_dice_seed42/last.pt
2026-10-02T11:43:42.9493523010	17547349 bytes	runs/loss_ablation_L1_weighted_bce_dice_seed42/best.pt
2026-10-05T13:08:56.4542867210	17562251 bytes	runs/R100_thebe_seed42_20261005_102737/best.pt
2026-10-05T13:22:24.1747144570	17562315 bytes	runs/R100_thebe_seed42_20261005_102737/last.pt
2026-10-09T06:02:22.8152205560	17653797 bytes	runs/p1_attention3d_caft_seed42/best_p1_attention3d_caft_seed42_epoch093_faultseg3d_synthetic_20261009.pt
2026-10-09T06:02:22.8152205560	17653797 bytes	runs/p1_attention3d_caft_seed42/best.pt
2026-10-09T06:04:48.5126887280	17653797 bytes	runs/p1_attention3d_caft_seed42/last.pt
2026-10-09T13:04:24.7343759270	180032179 bytes	runs/paper_attention3d_thebe_smoke_20261009_170246/best.pt
2026-10-09T13:04:25.2557309950	540106559 bytes	runs/paper_attention3d_thebe_smoke_20261009_170246/last.pt
2026-10-12T07:25:44.4666934400	180032179 bytes	runs/paper_attention3d_thebe_supervised_seed42/best.pt
2026-10-12T08:22:23.7548731230	540106559 bytes	runs/paper_attention3d_thebe_supervised_seed42/last.pt
2026-10-12T19:10:31.9704915780	180032371 bytes	runs/paper_attention3d_thebe_supervised_seed42_bf16_clean/best.pt
2026-10-12T19:44:31.0732620280	540106431 bytes	runs/paper_attention3d_thebe_supervised_seed42_bf16_clean/last.pt
2026-10-14T10:55:26.2829516960	17562443 bytes	runs/R100_fp16_clean_3seeds_20261014_145510/smoke_seed42/last.pt
2026-10-14T10:55:26.3306579770	17562443 bytes	runs/R100_fp16_clean_3seeds_20261014_145510/smoke_seed42/best.pt
2026-10-14T11:04:47.5321731820	17562443 bytes	runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/last.pt
2026-10-14T11:04:47.5634066030	17562443 bytes	runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/best.pt
2026-10-14T15:57:17.5696980420	17562443 bytes	runs/R100_fp16_clean_3seeds_20261014_150435/seed42/best.pt
2026-10-14T16:12:25.0497427080	17562443 bytes	runs/R100_fp16_clean_3seeds_20261014_150435/seed42/last.pt
2026-10-14T21:04:18.6093364070	17562443 bytes	runs/R100_fp16_clean_3seeds_20261014_150435/seed43/best.pt
2026-10-14T21:25:29.7404980360	17562443 bytes	runs/R100_fp16_clean_3seeds_20261014_150435/seed43/last.pt
2026-10-15T02:12:55.4137767480	17562443 bytes	runs/R100_fp16_clean_3seeds_20261014_150435/seed44/best.pt
2026-10-15T02:28:11.9270560240	17562443 bytes	runs/R100_fp16_clean_3seeds_20261014_150435/seed44/last.pt
```

### Settings

```text
reports/2026-10-02_baseline_A_report.md:14:## 2. Dataset split
reports/2026-10-02_baseline_A_report.md:16:| Dataset portion | Volumes | Purpose |
reports/2026-10-02_baseline_A_report.md:18:| Training | 180 | Used to update model weights |
reports/2026-10-02_baseline_A_report.md:19:| Internal validation | 20 | Used to monitor training, select the best checkpoint, and choose the probability threshold |
reports/2026-10-02_baseline_A_report.md:21:| Total | 220 | Complete prepared FaultSeg3D dataset |
reports/2026-10-02_baseline_A_report.md:25:The 180 original training volumes were accompanied by fixed flipped copies, producing 360 training samples per epoch. Validation and test volumes were not augmented.
reports/2026-10-02_baseline_A_report.md:27:## 3. Model
reports/2026-10-02_baseline_A_report.md:46:| Epochs | 100 |
reports/2026-10-02_baseline_A_report.md:47:| Best epoch | 100 |
reports/2026-10-02_baseline_A_report.md:48:| Loss | Ordinary binary cross-entropy |
reports/2026-10-02_baseline_A_report.md:49:| Optimizer | Adam |
reports/2026-10-02_baseline_A_report.md:50:| Learning rate | 0.0001 |
reports/2026-10-02_baseline_A_report.md:51:| Batch size | 1 |
reports/2026-10-02_baseline_A_report.md:53:| Effective batch size | 2 |
reports/2026-10-02_baseline_A_report.md:54:| Optimizer steps per epoch | 180 |
reports/2026-10-02_baseline_A_report.md:55:| Random seed | 42 |
reports/2026-10-02_baseline_A_report.md:56:| Mixed precision | Enabled |
reports/2026-10-02_baseline_A_report.md:57:| Preprocessing | Per-volume z-score normalization |
reports/2026-10-02_baseline_A_report.md:62:No real seismic data, self-supervised learning, seismic attributes, teacher model, distillation, attention module, normalization block, or residual block was used.
reports/2026-10-02_baseline_A_report.md:66:The best checkpoint was selected using internal-validation Dice at a threshold of `0.5`.
reports/2026-10-02_baseline_A_report.md:68:After training, the final probability threshold was selected using only the internal validation set. The selected threshold was:
reports/2026-10-02_baseline_A_report.md:72:This threshold was then frozen and applied to the held-out test set. The test labels were not used for model selection or threshold selection.
reports/2026-10-02_baseline_A_report.md:84:| Precision | 0.7992 | **0.8030** |
reports/2026-10-02_baseline_A_report.md:95:Dice, IoU, PR-AUC, precision, recall, and MCC provide more meaningful measures of fault-segmentation performance.
reports/attention3d_identity_audit_20261014.txt:31:./reports/EXPERIMENT_NAMING.md:26:- Loss Ablation L1 run: `runs/loss_ablation_L1_weighted_bce_dice_seed42`
reports/attention3d_identity_audit_20261014.txt:32:./reports/EXPERIMENT_NAMING.md:27:- Loss Ablation L1 log: `reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log`
reports/attention3d_identity_audit_20261014.txt:109:./reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:431:                raise RuntimeError(f"No Thebe files found for split {split}")
reports/attention3d_identity_audit_20261014.txt:111:./reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:501:    === THEBE SPLIT/COORDINATE REFERENCES ===
reports/attention3d_identity_audit_20261014.txt:117:./reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:700:    272:            raise RuntimeError(f"No Thebe files found for split {split}")
reports/attention3d_identity_audit_20261014.txt:139:./reports/debug/cracks_evaluation_context.md:120:0130:     model = Attention3D().cuda()
reports/attention3d_identity_audit_20261014.txt:176:./reports/evaluation/THEBE_ZERO_PATCH_AUDIT.md:1:# Thebe Zero-Patch Audit
reports/attention3d_identity_audit_20261014.txt:177:./reports/evaluation/THEBE_ZERO_PATCH_AUDIT.md:12:The first evaluator patch is entirely zero, while other sampled Thebe locations contain varying seismic data. This is consistent with an empty, muted, or padded survey region.
reports/attention3d_identity_audit_20261014.txt:178:./reports/evaluation/THEBE_ZERO_PATCH_AUDIT.md:46:Detailed patch statistics: `reports/evaluation/thebe_zero_patch_samples.csv`
reports/attention3d_identity_audit_20261014.txt:231:./reports/evaluation/r100_readiness_20261005_101611/audit.txt:223:top-level keys: ['data', 'efficiency', 'experiment', 'metric_notes', 'official_thebe_test', 'official_thebe_test_per_patch_summary', 'prediction_examples_saved', 'status', 'thebe_labels_used_for_threshold', 'threshold', 'threshold_source', 'training_performed', 'weight_updates']
reports/attention3d_identity_audit_20261014.txt:240:./reports/evaluation/A_TO_T0_FINAL_REPORT_20261005_095032.md:10:- Evaluation data: **official real Thebe test split**
reports/attention3d_identity_audit_20261014.txt:241:./reports/evaluation/A_TO_T0_FINAL_REPORT_20261005_095032.md:12:- Threshold selected using Thebe: **no**
reports/attention3d_identity_audit_20261014.txt:243:./reports/evaluation/A_TO_T0_FINAL_REPORT_20261005_095032.md:141:These results measure how a model trained only on synthetic FaultSeg3D transfers to real Thebe without training or adaptation. They do not measure a model trained using real data.
reports/attention3d_identity_audit_20261014.txt:259: 1655  (   cd ~/projects/fault_detection || exit 1;   set -o pipefail;   mkdir -p reports;    .venv_train/bin/python -u scripts/train_paper_attention3d_thebe.py     --run-dir "runs/paper_attention3d_thebe_smoke_$(date +%Y%m%d_%H%M%S)"     --epochs 1 --train-patches 4 --val-patches 32     2>&1 | tee reports/paper_attention3d_thebe_smoke.log || exit 1;    .venv_train/bin/python -u scripts/train_paper_attention3d_thebe.py     --run-dir runs/paper_attention3d_thebe_supervised_seed42     --epochs 100 --train-patches 64 --val-patches 32     2>&1 | tee -a reports/paper_attention3d_thebe_supervised_seed42.log; )
reports/attention3d_identity_audit_20261014.txt:273: 1695  for f in   reports/training/paper_attention3d_thebe_supervised_seed42_resume.log   reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log; do     echo;     echo "============================================================";     echo "LOG: $f";     stat -c 'modified=%y  bytes=%s' "$f";      echo "--- START ---";     sed -n '1,12p' "$f";      echo "--- LAST 5 COMPLETED EPOCHS ---";     rg '^EPOCH ' "$f" | tail -5;      echo "--- COMPLETION, FAILURE, OR NaN MARKERS ---";     rg -ni       'training complete|completed|finished|done|traceback|killed|terminated|out of memory|cuda error|exception|nan'       "$f" | tail -30 || true;      echo "--- FINAL 25 RAW LINES ---";     tail -25 "$f"; done
reports/attention3d_identity_audit_20261014.txt:278: 1744  history | rg -i 'nohup.*paper_attention3d|paper_attention3d.*(resume|bf16|clean)' | tail -30
reports/attention3d_identity_audit_20261014.txt:304: 1793  {     echo "=== REPOSITORY ===";     date -Is;     pwd;     git status --short;     git log -15 --date=iso --pretty='format:%h %ad %s';      echo;     echo "=== RELEVANT DOCUMENTATION ===";     rg -n -i 'attention3d|bf16|r100|thebe|seed42|roadmap'       --glob '*.md' --glob '*.txt'       --glob '!reports/training/**'       --glob '!runs/**' . || true;      echo;     echo "=== RELEVANT LAUNCH HISTORY ===";     history | rg -i       'paper_attention3d|bf16_clean|train_paper_attention3d_thebe|R100_thebe' || true;     rg -n -i       'paper_attention3d|bf16_clean|train_paper_attention3d_thebe|R100_thebe'       ~/.bash_history 2>/dev/null || true;      echo;     echo "=== TRAINING SCRIPT METADATA ===";     stat scripts/train_paper_attention3d_thebe.py;     sha256sum scripts/train_paper_attention3d_thebe.py;     rg -n -i       'bf16|bfloat|autocast|scaler|resume|sampler|balance|fault.patch|seed|run.dir|learning.rate'       scripts/train_paper_attention3d_thebe.py || true;      echo;     echo "=== UNCOMMITTED SCRIPT CHANGES ===";     git diff -- scripts/train_paper_attention3d_thebe.py;      echo;     echo "=== SCRIPT HISTORY ===";     git log -10 --date=iso --stat -- scripts/train_paper_attention3d_thebe.py;      echo;     echo "=== FILES MODIFIED ON OCTOBER 12 ===";     find scripts configs -type f       -newermt '2026-10-12 00:00:00'       ! -newermt '2026-10-13 00:00:00'       -printf '%TY-%Tm-%Td %TH:%TM:%TS %p\n' 2>/dev/null |       sort;      echo;     echo "=== RUN AND LOG FILES ===";     find runs reports/training -maxdepth 2       -name 'paper_attention3d_thebe_supervised_seed42*'       -printf '%TY-%Tm-%Td %TH:%TM:%TS %s %p\n' |       sort;      echo;     echo "=== TERMINATION EVIDENCE ===";     journalctl --since '2026-10-12 12:10:00'       --until '2026-10-12 12:40:00' --no-pager 2>/dev/null |       rg -i 'oom|killed process|python|nvidia|cuda|segfault' || true;      journalctl --since '2026-10-12 23:30:00'       --until '2026-10-13 00:00:00' --no-pager 2>/dev/null |       rg -i 'oom|killed process|python|nvidia|cuda|segfault' || true; } > "$audit" 2>&1
reports/attention3d_identity_audit_20261014.txt:311:1856:(   cd ~/projects/fault_detection || exit 1;   set -o pipefail;   mkdir -p reports;    .venv_train/bin/python -u scripts/train_paper_attention3d_thebe.py     --run-dir "runs/paper_attention3d_thebe_smoke_$(date +%Y%m%d_%H%M%S)"     --epochs 1 --train-patches 4 --val-patches 32     2>&1 | tee reports/paper_attention3d_thebe_smoke.log || exit 1;    .venv_train/bin/python -u scripts/train_paper_attention3d_thebe.py     --run-dir runs/paper_attention3d_thebe_supervised_seed42     --epochs 100 --train-patches 64 --val-patches 32     2>&1 | tee -a reports/paper_attention3d_thebe_supervised_seed42.log; )
reports/attention3d_identity_audit_20261014.txt:325:1896:for f in   reports/training/paper_attention3d_thebe_supervised_seed42_resume.log   reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log; do     echo;     echo "============================================================";     echo "LOG: $f";     stat -c 'modified=%y  bytes=%s' "$f";      echo "--- START ---";     sed -n '1,12p' "$f";      echo "--- LAST 5 COMPLETED EPOCHS ---";     rg '^EPOCH ' "$f" | tail -5;      echo "--- COMPLETION, FAILURE, OR NaN MARKERS ---";     rg -ni       'training complete|completed|finished|done|traceback|killed|terminated|out of memory|cuda error|exception|nan'       "$f" | tail -30 || true;      echo "--- FINAL 25 RAW LINES ---";     tail -25 "$f"; done
reports/attention3d_identity_audit_20261014.txt:330:1954:history | rg -i 'nohup.*paper_attention3d|paper_attention3d.*(resume|bf16|clean)' | tail -30
reports/attention3d_identity_audit_20261014.txt:367:62:        seed: int,
reports/attention3d_identity_audit_20261014.txt:369:71:        self.seed = seed
reports/attention3d_identity_audit_20261014.txt:371:90:        rng = np.random.default_rng(self.seed + self.epoch * 1_000_003 + index * 1009)
reports/attention3d_identity_audit_20261014.txt:374:163:    parser.add_argument("--seed", type=int, default=42)
reports/attention3d_paper_preflight.txt:29:EXISTING SURVEYS OR PRETRAINED WEIGHTS
reports/data_audit/faultseg3d_volume_statistics.csv:1:split,volume_id,shape,seismic_dtype,fault_dtype,seismic_bytes,fault_bytes,seismic_min,seismic_max,seismic_mean,seismic_std,fault_positive_voxels,total_voxels,fault_positive_pct,fault_labels,finite,seismic_sha256,fault_sha256,seismic_path,fault_path
reports/data_audit/thebe_h5_statistics.csv:1:split,shape,source_seismic_dtype,source_fault_dtype,output_seismic_dtype,output_fault_dtype,seismic_min,seismic_max,seismic_mean,seismic_std,fault_positive_count,total_voxels,fault_positive_pct,source_seismic_sha256,source_fault_sha256,source_seismic_path,source_fault_path,output_path,output_bytes
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:54:split,shape,source_seismic_dtype,source_fault_dtype,output_seismic_dtype,output_fault_dtype,seismic_min,seismic_max,seismic_mean,seismic_std,fault_positive_count,total_voxels,fault_positive_pct,source_seismic_sha256,source_fault_sha256,source_seismic_path,source_fault_path,output_path,output_bytes
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:221:Dataset fault: shape=(100, 3174, 1537), dtype=uint8, chunks=(1, 256, 256), compression=gzip
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:222:Dataset seismic: shape=(100, 3174, 1537), dtype=float32, chunks=(1, 256, 256), compression=gzip
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:235:Dataset fault: shape=(100, 3174, 1537), dtype=uint8, chunks=(1, 256, 256), compression=gzip
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:236:Dataset seismic: shape=(100, 3174, 1537), dtype=float32, chunks=(1, 256, 256), compression=gzip
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:249:Dataset fault: shape=(100, 3174, 1537), dtype=uint8, chunks=(1, 256, 256), compression=gzip
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:250:Dataset seismic: shape=(100, 3174, 1537), dtype=float32, chunks=(1, 256, 256), compression=lzf
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:263:Dataset fault: shape=(100, 3174, 1537), dtype=uint8, chunks=(1, 256, 256), compression=gzip
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:264:Dataset seismic: shape=(100, 3174, 1537), dtype=float32, chunks=(1, 256, 256), compression=lzf
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:321:class FaultSegDataset(Dataset[tuple[Tensor, Tensor, str]]):
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:420:    for split in splits:
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:421:        seismic_files = sorted((source_root / "seis").glob(patterns[split]), key=natural_key)
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:423:            raise RuntimeError(f"No Thebe files found for split {split}")
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:438:                            "split": split,
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:493:=== THEBE SPLIT/COORDINATE REFERENCES ===
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:517:35:            for piece in re.split(r"(\d+)", path.name)]
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:527:52:    for split in ("train", "validation"):
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:528:53:        seis_dir = data_root / "faultseg3d" / split / "seis"
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:529:54:        fault_dir = data_root / "faultseg3d" / split / "fault"
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:536:61:                f"{split}: unmatched pairs; missing fault={missing_fault}, "
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:553:85:                "split": split,
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:571:107:                print(f"{split}: audited {index}/{len(names)} pairs", flush=True)
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:638:199-        "Raw 0 = unknown/unannotated (ignore in loss)\n"
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:643:204:        "Derived valid PNG: 0=ignore, 255=include in loss\n",
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:62:    split,shape,source_seismic_dtype,source_fault_dtype,output_seismic_dtype,output_fault_dtype,seismic_min,seismic_max,seismic_mean,seismic_std,fault_positive_count,total_voxels,fault_positive_pct,source_seismic_sha256,source_fault_sha256,source_seismic_path,source_fault_path,output_path,output_bytes
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:229:    Dataset fault: shape=(100, 3174, 1537), dtype=uint8, chunks=(1, 256, 256), compression=gzip
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:230:    Dataset seismic: shape=(100, 3174, 1537), dtype=float32, chunks=(1, 256, 256), compression=gzip
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:243:    Dataset fault: shape=(100, 3174, 1537), dtype=uint8, chunks=(1, 256, 256), compression=gzip
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:244:    Dataset seismic: shape=(100, 3174, 1537), dtype=float32, chunks=(1, 256, 256), compression=gzip
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:257:    Dataset fault: shape=(100, 3174, 1537), dtype=uint8, chunks=(1, 256, 256), compression=gzip
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:258:    Dataset seismic: shape=(100, 3174, 1537), dtype=float32, chunks=(1, 256, 256), compression=lzf
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:271:    Dataset fault: shape=(100, 3174, 1537), dtype=uint8, chunks=(1, 256, 256), compression=gzip
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:272:    Dataset seismic: shape=(100, 3174, 1537), dtype=float32, chunks=(1, 256, 256), compression=lzf
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:329:    class FaultSegDataset(Dataset[tuple[Tensor, Tensor, str]]):
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:428:        for split in splits:
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:429:            seismic_files = sorted((source_root / "seis").glob(patterns[split]), key=natural_key)
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:431:                raise RuntimeError(f"No Thebe files found for split {split}")
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:446:                                "split": split,
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:501:    === THEBE SPLIT/COORDINATE REFERENCES ===
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:525:    35:            for piece in re.split(r"(\d+)", path.name)]
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:535:    52:    for split in ("train", "validation"):
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:536:    53:        seis_dir = data_root / "faultseg3d" / split / "seis"
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:537:    54:        fault_dir = data_root / "faultseg3d" / split / "fault"
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:544:    61:                f"{split}: unmatched pairs; missing fault={missing_fault}, "
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:561:    85:                "split": split,
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:579:    107:                print(f"{split}: audited {index}/{len(names)} pairs", flush=True)
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:646:    199-        "Raw 0 = unknown/unannotated (ignore in loss)\n"
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:651:    204:        "Derived valid PNG: 0=ignore, 255=include in loss\n",
reports/debug/cracks_evaluation_context.md:29:0022: PATCH = 128
reports/debug/cracks_evaluation_context.md:41:0034:     if length < PATCH:
reports/debug/cracks_evaluation_context.md:42:0035:         raise RuntimeError(f"Image dimension {length} is smaller than {PATCH}")
reports/debug/cracks_evaluation_context.md:43:0036:     values = list(range(0, length - PATCH + 1, STRIDE))
reports/debug/cracks_evaluation_context.md:44:0037:     last = length - PATCH
reports/debug/cracks_evaluation_context.md:68:0061:     parser.add_argument("--threshold-metrics", type=Path, required=True)
reports/debug/cracks_evaluation_context.md:116:0126:     threshold = float(
reports/debug/cracks_evaluation_context.md:120:0130:     model = Attention3D().cuda()
reports/debug/cracks_evaluation_context.md:121:0131:     model.load_state_dict(checkpoint["model"], strict=True)
reports/debug/cracks_evaluation_context.md:122:0132:     model.eval()
reports/debug/cracks_evaluation_context.md:123:0133:     for parameter in model.parameters():
reports/debug/cracks_evaluation_context.md:138:0175:                     logits = model(tensor)
reports/debug/cracks_evaluation_context.md:140:0177:                     torch.sigmoid(logits.float())[0, 0, :, :, PATCH // 2]
reports/debug/cracks_evaluation_context.md:146:0183:                     y0 : y0 + PATCH, x0 : x0 + PATCH
reports/debug/cracks_evaluation_context.md:149:0186:                     y0 : y0 + PATCH, x0 : x0 + PATCH
reports/debug/cracks_evaluation_context.md:162:0199:         metrics = asdict(individual.metrics(threshold))
reports/debug/cracks_evaluation_context.md:183:0220:     final_metrics = asdict(aggregate.metrics(threshold))
reports/debug/cracks_evaluation_context.md:209:0253:     print(f"threshold={threshold:.6f}")
reports/debug/cracks_evaluation_context.md:212:0256:     print(f"precision={final_metrics['precision']:.6f}")
reports/debug/cracks_evaluation_context.md:226:                                           --threshold-metrics THRESHOLD_METRICS
reports/debug/cracks_evaluation_context.md:237:  --threshold-metrics THRESHOLD_METRICS
reports/debug/cracks_evaluation_context.md:303:    -p, --patch           generate patch
reports/debug/cracks_evaluation_context.md:304:    -s, --no-patch        suppress diff output
reports/debug/cracks_evaluation_context.md:305:    -u                    generate patch
reports/evaluation/A_TO_T0_FINAL_REPORT_20261005_095032.md:10:- Evaluation data: **official real Thebe test split**
reports/evaluation/A_TO_T0_FINAL_REPORT_20261005_095032.md:11:- Frozen threshold: `0.438965`
reports/evaluation/A_TO_T0_FINAL_REPORT_20261005_095032.md:12:- Threshold selected using Thebe: **no**
reports/evaluation/A_TO_T0_FINAL_REPORT_20261005_095032.md:33:| Precision | 0.052094 |
reports/evaluation/A_TO_T0_FINAL_REPORT_20261005_095032.md:108:  "precision": {
reports/evaluation/A_TO_T0_FINAL_REPORT_20261005_095032.md:141:These results measure how a model trained only on synthetic FaultSeg3D transfers to real Thebe without training or adaptation. They do not measure a model trained using real data.
reports/evaluation/a_to_t0_final_summary_20261005_095032.txt:4:PRECISION: 0.052094
reports/evaluation/baseline_A_zero_shot_thebe_full_20261005_095032.log:63:threshold=0.438965
reports/evaluation/baseline_A_zero_shot_thebe_full_20261005_095032.log:66:precision=0.052094
reports/evaluation/baseline_A_zero_shot_thebe_smoke_20261005_094726.log:5:threshold=0.438965
reports/evaluation/baseline_A_zero_shot_thebe_smoke_20261005_094726.log:8:precision=0.041877
reports/evaluation/cracks_error_excerpt.md:18:    "precision": 0.024374183477476077,
reports/evaluation/cracks_error_excerpt.md:22:    "threshold": 0.98095703125,
reports/evaluation/cracks_error_excerpt.md:47:  "threshold": 0.98095703125,
reports/evaluation/cracks_error_excerpt.md:58:section,valid_pixels,fault_pixels,threshold,dice,iou,precision,recall,specificity,balanced_accuracy,accuracy,mcc,pr_auc_approx,roc_auc_approx,tp,fp,fn,tn
reports/evaluation/latest_cracks_run.md:49:threshold=0.980957
reports/evaluation/latest_cracks_run.md:52:precision=0.024374
reports/evaluation/latest_cracks_run.md:73:    "precision": 0.024374183477476077,
reports/evaluation/latest_cracks_run.md:77:    "threshold": 0.98095703125,
reports/evaluation/latest_cracks_run.md:102:  "threshold": 0.98095703125,
reports/evaluation/latest_cracks_run.md:113:section,valid_pixels,fault_pixels,threshold,dice,iou,precision,recall,specificity,balanced_accuracy,accuracy,mcc,pr_auc_approx,roc_auc_approx,tp,fp,fn,tn
reports/evaluation/p1_attention3d_caft_seed42_to_thebe_smoke_20261009/final_metrics.json:48:    "one_empty_mask_policy": "valid-patch diagonal penalty"
reports/evaluation/p1_attention3d_caft_seed42_to_thebe_smoke_20261009/final_metrics.json:59:    "precision": 0.0,
reports/evaluation/p1_attention3d_caft_seed42_to_thebe_smoke_20261009/final_metrics.json:63:    "threshold": 0.98095703125,
reports/evaluation/p1_attention3d_caft_seed42_to_thebe_smoke_20261009/final_metrics.json:71:  "threshold": 0.98095703125,
reports/evaluation/p1_attention3d_caft_seed42_to_thebe_smoke_20261009/run_configuration.json:13:  "edge_policy": "zero-pad normalized inputs to 128^3; exclude padding from every metric",
reports/evaluation/p1_attention3d_caft_seed42_to_thebe_smoke_20261009/run_configuration.json:18:  "normalization": "independent z-score on each valid 3D patch, matching Baseline A",
reports/evaluation/p1_attention3d_caft_seed42_to_thebe_smoke_20261009/run_configuration.json:37:  "threshold": 0.98095703125,
reports/evaluation/p1_attention3d_caft_seed42_to_thebe_smoke9_20261009/final_metrics.json:48:    "one_empty_mask_policy": "valid-patch diagonal penalty"
reports/evaluation/p1_attention3d_caft_seed42_to_thebe_smoke9_20261009/final_metrics.json:59:    "precision": 0.08559098766493257,
reports/evaluation/p1_attention3d_caft_seed42_to_thebe_smoke9_20261009/final_metrics.json:63:    "threshold": 0.98095703125,
reports/evaluation/p1_attention3d_caft_seed42_to_thebe_smoke9_20261009/final_metrics.json:131:    "precision": {
reports/evaluation/p1_attention3d_caft_seed42_to_thebe_smoke9_20261009/final_metrics.json:163:  "threshold": 0.98095703125,
reports/evaluation/p1_attention3d_caft_seed42_to_thebe_smoke9_20261009/prediction_examples/example_01_x0000_y0000_z0640.npz: binary file matches (found "\0" byte around offset 5)
reports/evaluation/p1_attention3d_caft_seed42_to_thebe_smoke9_20261009/prediction_examples/example_02_x0000_y0000_z0768.npz: binary file matches (found "\0" byte around offset 5)
reports/evaluation/p1_attention3d_caft_seed42_to_thebe_smoke9_20261009/prediction_examples/example_03_x0000_y0000_z0896.npz: binary file matches (found "\0" byte around offset 5)
reports/evaluation/p1_attention3d_caft_seed42_to_thebe_smoke9_20261009/prediction_examples/example_04_x0000_y0000_z1024.npz: binary file matches (found "\0" byte around offset 5)
reports/evaluation/p1_attention3d_caft_seed42_to_thebe_smoke9_20261009/run_configuration.json:13:  "edge_policy": "zero-pad normalized inputs to 128^3; exclude padding from every metric",
reports/evaluation/p1_attention3d_caft_seed42_to_thebe_smoke9_20261009/run_configuration.json:18:  "normalization": "independent z-score on each valid 3D patch, matching Baseline A",
reports/evaluation/p1_attention3d_caft_seed42_to_thebe_smoke9_20261009/run_configuration.json:37:  "threshold": 0.98095703125,
reports/evaluation/p1_attention3d_caft_seed42_to_thebe_smoke9_20261009/test_per_patch.csv:1:patch_id,raw_x_start,raw_x_stop,raw_y_start,raw_y_stop,raw_z_start,raw_z_stop,raw_voxels,valid_voxels,excluded_no_data_voxels,positive_labels_outside_valid_mask,normalization_mean,normalization_std,threshold,dice,iou,precision,recall,specificity,balanced_accuracy,accuracy,mcc,pr_auc_approx,roc_auc_approx,tp,fp,fn,tn,modified_hausdorff_voxels,bidirectional_chamfer_voxels,prediction_empty,target_empty,inference_seconds
reports/evaluation/p1_cracks_expert_seed42_20261009_134425/expert_per_section.csv:1:section,valid_pixels,certain_fault_pixels,threshold,dice,iou,precision,recall,specificity,balanced_accuracy,accuracy,mcc,pr_auc_approx,roc_auc_approx,tp,fp,fn,tn
reports/evaluation/p1_cracks_expert_seed42_20261009_134425/final_metrics.json:13:    "precision": 0.038205351398402906,
reports/evaluation/p1_cracks_expert_seed42_20261009_134425/final_metrics.json:17:    "threshold": 0.98095703125,
reports/evaluation/p1_cracks_expert_seed42_20261009_134425/final_metrics.json:42:  "threshold": 0.98095703125,
reports/evaluation/r100_readiness_20261005_101611/audit.txt:106:epoch: 100
reports/evaluation/r100_readiness_20261005_101611/audit.txt:108:  "loss": "b0_bce",
reports/evaluation/r100_readiness_20261005_101611/audit.txt:112:  "epochs": 100,
reports/evaluation/r100_readiness_20261005_101611/audit.txt:113:  "batch_size": 1,
reports/evaluation/r100_readiness_20261005_101611/audit.txt:116:  "learning_rate": 0.0001,
reports/evaluation/r100_readiness_20261005_101611/audit.txt:118:  "seed": 42,
reports/evaluation/r100_readiness_20261005_101611/audit.txt:124:model tensors: 30
reports/evaluation/r100_readiness_20261005_101611/audit.txt:125:model parameters: 1459585
reports/evaluation/r100_readiness_20261005_101611/audit.txt:127:  "threshold": 0.5,
reports/evaluation/r100_readiness_20261005_101611/audit.txt:130:  "precision": 0.8161029287143701,
reports/evaluation/r100_readiness_20261005_101611/audit.txt:148:  dataset=fault shape=(100, 3174, 1537) dtype=uint8 chunks=(1, 256, 256) compression=gzip
reports/evaluation/r100_readiness_20261005_101611/audit.txt:149:  dataset=seismic shape=(100, 3174, 1537) dtype=float32 chunks=(1, 256, 256) compression=gzip
reports/evaluation/r100_readiness_20261005_101611/audit.txt:152:  dataset=fault shape=(100, 3174, 1537) dtype=uint8 chunks=(1, 256, 256) compression=gzip
reports/evaluation/r100_readiness_20261005_101611/audit.txt:153:  dataset=seismic shape=(100, 3174, 1537) dtype=float32 chunks=(1, 256, 256) compression=gzip
reports/evaluation/r100_readiness_20261005_101611/audit.txt:156:  dataset=fault shape=(100, 3174, 1537) dtype=uint8 chunks=(1, 256, 256) compression=gzip
reports/evaluation/r100_readiness_20261005_101611/audit.txt:157:  dataset=seismic shape=(100, 3174, 1537) dtype=float32 chunks=(1, 256, 256) compression=gzip
reports/evaluation/r100_readiness_20261005_101611/audit.txt:160:  dataset=fault shape=(100, 3174, 1537) dtype=uint8 chunks=(1, 256, 256) compression=gzip
reports/evaluation/r100_readiness_20261005_101611/audit.txt:161:  dataset=seismic shape=(100, 3174, 1537) dtype=float32 chunks=(1, 256, 256) compression=gzip
reports/evaluation/r100_readiness_20261005_101611/audit.txt:164:  dataset=fault shape=(100, 3174, 1537) dtype=uint8 chunks=(1, 256, 256) compression=gzip
reports/evaluation/r100_readiness_20261005_101611/audit.txt:165:  dataset=seismic shape=(100, 3174, 1537) dtype=float32 chunks=(1, 256, 256) compression=gzip
reports/evaluation/r100_readiness_20261005_101611/audit.txt:168:  dataset=fault shape=(100, 3174, 1537) dtype=uint8 chunks=(1, 256, 256) compression=gzip
reports/evaluation/r100_readiness_20261005_101611/audit.txt:169:  dataset=seismic shape=(100, 3174, 1537) dtype=float32 chunks=(1, 256, 256) compression=gzip
reports/evaluation/r100_readiness_20261005_101611/audit.txt:172:  dataset=fault shape=(103, 3174, 1537) dtype=uint8 chunks=(1, 256, 256) compression=gzip
reports/evaluation/r100_readiness_20261005_101611/audit.txt:173:  dataset=seismic shape=(103, 3174, 1537) dtype=float32 chunks=(1, 256, 256) compression=gzip
reports/evaluation/sammed3d_thebe_cpu_preflight.txt:3:  "model": "SAM-Med3D-turbo vit_b_ori, prompt-free",
reports/evaluation/THEBE_EVALUATOR_EDIT_CONTEXT.md:12:- Normalize using valid voxels only.
reports/evaluation/THEBE_EVALUATOR_EDIT_CONTEXT.md:13:- Exclude invalid voxels from overlap, threshold and structural metrics.
reports/evaluation/THEBE_EVALUATOR_EDIT_CONTEXT.md:33:0007: - takes its threshold from synthetic validation;
reports/evaluation/THEBE_EVALUATOR_EDIT_CONTEXT.md:39:0296:         raise RuntimeError(f"Invalid frozen threshold: {threshold}")
reports/evaluation/THEBE_EVALUATOR_EDIT_CONTEXT.md:42:0375:             "independent z-score on each valid 3D patch, "
reports/evaluation/THEBE_EVALUATOR_EDIT_CONTEXT.md:76:0708:                 "valid-patch diagonal penalty"
reports/evaluation/THEBE_EVALUATOR_EDIT_CONTEXT.md:83:## Patch loop, normalization and metric updates
reports/evaluation/THEBE_EVALUATOR_EDIT_CONTEXT.md:96:0358:         "checkpoint_epoch": int(checkpoint.get("epoch", -1)),
reports/evaluation/THEBE_EVALUATOR_EDIT_CONTEXT.md:101:0363:         "threshold": threshold,
reports/evaluation/THEBE_EVALUATOR_EDIT_CONTEXT.md:112:0374:         "normalization": (
reports/evaluation/THEBE_EVALUATOR_EDIT_CONTEXT.md:113:0375:             "independent z-score on each valid 3D patch, "
reports/evaluation/THEBE_EVALUATOR_EDIT_CONTEXT.md:118:0380:             "zero-pad normalized inputs to 128^3; "
reports/evaluation/THEBE_EVALUATOR_EDIT_CONTEXT.md:144:0406:             x1 = min(x0 + patch_size, total_shape[0])
reports/evaluation/THEBE_EVALUATOR_EDIT_CONTEXT.md:145:0407:             y1 = min(y0 + patch_size, total_shape[1])
reports/evaluation/THEBE_EVALUATOR_EDIT_CONTEXT.md:146:0408:             z1 = min(z0 + patch_size, total_shape[2])
reports/evaluation/THEBE_EVALUATOR_EDIT_CONTEXT.md:173:0435:                     f"NaN/Inf in patch starting at {(x0, y0, z0)}"
reports/evaluation/THEBE_EVALUATOR_EDIT_CONTEXT.md:238:0500:                     logits = model(model_input)
reports/evaluation/THEBE_EVALUATOR_EDIT_CONTEXT.md:293:0555:                 **asdict(individual.metrics(threshold)),
reports/evaluation/THEBE_EVALUATOR_EDIT_CONTEXT.md:303:0565:                 probability_numpy >= threshold
reports/evaluation/THEBE_EVALUATOR_EDIT_CONTEXT.md:328:0590:                     "threshold": np.asarray(
reports/evaluation/THEBE_EVALUATOR_EDIT_CONTEXT.md:329:0591:                         threshold,
reports/evaluation/THEBE_EVALUATOR_EDIT_CONTEXT.md:387:0649:         aggregate.metrics(threshold)
reports/evaluation/THEBE_EVALUATOR_EDIT_CONTEXT.md:418:0649:         aggregate.metrics(threshold)
reports/evaluation/THEBE_EVALUATOR_EDIT_CONTEXT.md:431:0662:         "threshold": threshold,
reports/evaluation/THEBE_SMOKE_RESULT_20261005_094726.md:7:- Threshold: `0.438965`
reports/evaluation/THEBE_SMOKE_RESULT_20261005_094726.md:18:- Precision: `0.041877`
reports/evaluation/THEBE_ZERO_PATCH_AUDIT.md:1:# Thebe Zero-Patch Audit
reports/evaluation/THEBE_ZERO_PATCH_AUDIT.md:6:- Exact first-patch standard deviation: `0`
reports/evaluation/THEBE_ZERO_PATCH_AUDIT.md:7:- Exact first-patch zero fraction: `100.000000%`
reports/evaluation/THEBE_ZERO_PATCH_AUDIT.md:8:- Exact first-patch fault voxels: `0`
reports/evaluation/THEBE_ZERO_PATCH_AUDIT.md:12:The first evaluator patch is entirely zero, while other sampled Thebe locations contain varying seismic data. This is consistent with an empty, muted, or padded survey region.
reports/evaluation/THEBE_ZERO_PATCH_AUDIT.md:46:Detailed patch statistics: `reports/evaluation/thebe_zero_patch_samples.csv`
reports/EXPERIMENT_NAMING.md:10:| 2 | Baseline B | Baseline A model fine-tuned with a small labelled real-data subset | Not started |
reports/EXPERIMENT_NAMING.md:20:| Loss Ablation L1 | Same synthetic data and architecture with weighted BCE plus Dice loss | Complete; no improvement over Baseline A |
reports/EXPERIMENT_NAMING.md:26:- Loss Ablation L1 run: `runs/loss_ablation_L1_weighted_bce_dice_seed42`
reports/EXPERIMENT_NAMING.md:27:- Loss Ablation L1 log: `reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log`
reports/EXPERIMENT_NAMING.md:31:The internal loss keys `b0_bce` and `b1_weighted_dice` are implementation identifiers preserved inside historical checkpoints and configurations. They are not formal experiment names.
reports/p1_thebe_setup.txt:3:                                   [--threshold-metrics THRESHOLD_METRICS]
reports/p1_thebe_setup.txt:9:                                   [--threshold-source-label THRESHOLD_SOURCE_LABEL]
reports/p1_thebe_setup.txt:13:takes its threshold from synthetic validation; - standardizes each 128^3 input
reports/p1_thebe_setup.txt:14:patch like Baseline A; - covers the complete test volume exactly once; -
reports/p1_thebe_setup.txt:21:  --threshold-metrics THRESHOLD_METRICS
reports/p1_thebe_setup.txt:28:  --threshold-source-label THRESHOLD_SOURCE_LABEL
reports/p1_thebe_setup.txt:35:- takes its threshold from synthetic validation;
reports/p1_thebe_setup.txt:36:- standardizes each 128^3 input patch like Baseline A;
reports/p1_thebe_setup.txt:64:        for part in re.split(r"(\d+)", path.name)
reports/p1_thebe_setup.txt:180:        "precision",
reports/p1_thebe_setup.txt:252:        "--threshold-metrics",
reports/p1_thebe_setup.txt:276:        "--threshold-source-label",
reports/p1_thebe_setup.txt:325:    threshold = float(
reports/p1_thebe_setup.txt:331:    if not 0.0 < threshold < 1.0:
reports/p1_thebe_setup.txt:332:        raise RuntimeError(f"Invalid frozen threshold: {threshold}")
reports/p1_thebe_setup.txt:341:    patch_size = volume_shape[0]
reports/p1_thebe_setup.txt:348:    if "model" not in checkpoint:
reports/p1_thebe_setup.txt:349:        raise RuntimeError("Checkpoint does not contain model weights")
reports/p1_thebe_setup.txt:357:    model = baseline.FaultSeg3D().to(device)
reports/p1_thebe_setup.txt:358:    model.load_state_dict(checkpoint["model"], strict=True)
reports/p1_thebe_setup.txt:359:    model.eval()
reports/p1_thebe_setup.txt:361:    for parameter in model.parameters():
reports/p1_thebe_setup.txt:365:    np.random.seed(42)
reports/p1_thebe_setup.txt:373:    x_starts = list(range(0, total_shape[0], patch_size))
reports/p1_zero_shot_thebe_full_20261009_162704.log:78:threshold=0.980957
reports/p1_zero_shot_thebe_full_20261009_162704.log:81:precision=0.050344
reports/p1_zero_shot_thebe_full_20261009_162704.log:92:precision          baseline=0.052094  P1=0.050344  change=-0.001750
reports/paper_attention3d_thebe_smoke.log:2:parameters=45001057 epochs=1 train_patches=4 val_patches=32
reports/paper_attention3d_thebe_smoke.log:3:epoch=1/1 train_patch=4/4 loss=0.41600
reports/paper_attention3d_thebe_smoke.log:4:EPOCH 001 train_loss=0.503052 val_loss=0.493502 val_dice=0.005776 val_precision=0.030397 val_recall=0.003191 best=0.005776 elapsed_min=1.6
reports/paper_attention3d_thebe_supervised_seed42.log:2:parameters=45001057 epochs=100 train_patches=64 val_patches=32
reports/paper_attention3d_thebe_supervised_seed42.log:3:epoch=1/100 train_patch=16/64 loss=0.50337
reports/paper_attention3d_thebe_supervised_seed42.log:4:epoch=1/100 train_patch=32/64 loss=0.48164
reports/paper_attention3d_thebe_supervised_seed42.log:5:epoch=1/100 train_patch=48/64 loss=0.39247
reports/paper_attention3d_thebe_supervised_seed42.log:6:epoch=1/100 train_patch=64/64 loss=0.51057
reports/paper_attention3d_thebe_supervised_seed42.log:7:EPOCH 001 train_loss=0.465636 val_loss=0.485576 val_dice=0.000000 val_precision=0.000000 val_recall=0.000000 best=0.000000 elapsed_min=8.4
reports/paper_attention3d_thebe_supervised_seed42.log:8:epoch=2/100 train_patch=16/64 loss=0.50705
reports/paper_attention3d_thebe_supervised_seed42.log:9:epoch=2/100 train_patch=32/64 loss=0.50695
reports/paper_attention3d_thebe_supervised_seed42.log:10:epoch=2/100 train_patch=48/64 loss=0.50998
reports/paper_attention3d_thebe_supervised_seed42.log:11:epoch=2/100 train_patch=64/64 loss=0.50335
reports/paper_attention3d_thebe_supervised_seed42.log:12:EPOCH 002 train_loss=0.467665 val_loss=0.482280 val_dice=0.000000 val_precision=0.000000 val_recall=0.000000 best=0.000000 elapsed_min=16.6
reports/paper_attention3d_thebe_supervised_seed42.log:13:epoch=3/100 train_patch=16/64 loss=0.50525
reports/paper_attention3d_thebe_supervised_seed42.log:14:epoch=3/100 train_patch=32/64 loss=0.51570
reports/paper_attention3d_thebe_supervised_seed42.log:15:epoch=3/100 train_patch=48/64 loss=0.38128
reports/paper_attention3d_thebe_supervised_seed42.log:16:epoch=3/100 train_patch=64/64 loss=0.51452
reports/paper_attention3d_thebe_supervised_seed42.log:17:EPOCH 003 train_loss=0.454657 val_loss=0.483242 val_dice=0.000000 val_precision=0.000000 val_recall=0.000000 best=0.000000 elapsed_min=24.9
reports/paper_attention3d_thebe_supervised_seed42.log:18:epoch=4/100 train_patch=16/64 loss=0.35714
reports/paper_attention3d_thebe_supervised_seed42.log:19:epoch=4/100 train_patch=32/64 loss=0.51700
reports/paper_attention3d_thebe_supervised_seed42.log:20:epoch=4/100 train_patch=48/64 loss=0.51154
reports/paper_attention3d_thebe_supervised_seed42.log:21:epoch=4/100 train_patch=64/64 loss=0.50385
reports/paper_attention3d_thebe_supervised_seed42.log:22:EPOCH 004 train_loss=0.460656 val_loss=0.480945 val_dice=0.000000 val_precision=0.000000 val_recall=0.000000 best=0.000000 elapsed_min=33.2
reports/paper_attention3d_thebe_supervised_seed42.log:23:epoch=5/100 train_patch=16/64 loss=0.50533
reports/paper_attention3d_thebe_supervised_seed42.log:24:epoch=5/100 train_patch=32/64 loss=0.51463
reports/paper_attention3d_thebe_supervised_seed42.log:25:epoch=5/100 train_patch=48/64 loss=0.50677
reports/r100_launch_check_20261014_133445.txt:28:  "seed": 42,
reports/r100_launch_check_20261014_133445.txt:63:  "epochs": 100,
reports/r100_launch_check_20261014_133445.txt:65:  "patch_size": 128,
reports/r100_launch_check_20261014_133445.txt:68:  "train_sampling": "40 observed random patches per train file each epoch; random axis-0 flip",
reports/r100_launch_check_20261014_133445.txt:70:  "normalization": "per-patch z-score over observed voxels; axis reversal",
reports/r100_launch_check_20261014_133445.txt:72:  "optimizer": "Adam",
reports/r100_launch_check_20261014_133445.txt:73:  "learning_rate": 0.0001,
reports/r100_launch_check_20261014_133445.txt:74:  "loss": "ordinary BCE averaged over observed voxels",
reports/r100_launch_check_20261014_133445.txt:78:  "test_policy": "one complete test evaluation after checkpoint and threshold selection"
reports/r100_launch_check_20261014_133445.txt:84:  "old_selection": "Dice at threshold 0.5 on fixed 128 validation patches",
reports/r100_launch_check_20261014_133445.txt:86:  "why": "Near-zero Dice at 0.5 despite improving PR-AUC; final threshold remains full-validation only",
reports/r100_launch_check_20261014_133445.txt:94:  "threshold": 0.1767578125,
reports/r100_launch_check_20261014_133445.txt:97:    "threshold": 0.1767578125,
reports/r100_launch_check_20261014_133445.txt:100:    "precision": 0.5279583306670493,
reports/r100_launch_check_20261014_133445.txt:153:    "precision": 0.5279583306670493,
reports/r100_launch_check_20261014_133445.txt:157:    "threshold": 0.1767578125,
reports/r100_launch_check_20261014_133445.txt:173:    "train_sampling": "360 randomly sampled observed patches per epoch from all 9 real train files",
reports/r100_launch_check_20261014_133445.txt:185:    "precision": 0.47191760787630943,
reports/r100_launch_check_20261014_133445.txt:189:    "threshold": 0.1767578125,
reports/r100_launch_check_20261014_133445.txt:257:    "precision": {
reports/r100_launch_check_20261014_133445.txt:287:  "resume_note": "Epoch 23 checkpoint had no saved RNG or AMP scaler state; weights and optimizer were restored, while sampling and scaler continued from a new state.",
reports/r100_launch_check_20261014_133445.txt:299:  "threshold": 0.1767578125,
reports/r100_launch_check_20261014_133445.txt:307:"""R100: FaultSeg3D from scratch on real Thebe, then held-out evaluation.
reports/r100_launch_check_20261014_133445.txt:341:SEED = 42
reports/training/baseline_A_smoke.log:1:device=cuda; parameters=1,459,585; amp=True
reports/training/baseline_A_smoke.log:2:/shared/home/khavarj/projects/fault_detection/scripts/faultseg3d_baseline.py:553: FutureWarning: `torch.cuda.amp.GradScaler(args...)` is deprecated. Please use `torch.amp.GradScaler('cuda', args...)` instead.
reports/training/baseline_A_smoke.log:3:  scaler = torch.cuda.amp.GradScaler(enabled=amp_enabled)
reports/training/baseline_A_smoke.log:6:SMOKE PASS: input=(1, 1, 128, 128, 128), output=(1, 1, 128, 128, 128), loss=0.778994, peak_cuda_GiB=1.218
reports/training/baseline_A_synthetic_bce_seed42.log:2:device=cuda; parameters=1,459,585; amp=True
reports/training/baseline_A_synthetic_bce_seed42.log:3:/shared/home/khavarj/projects/fault_detection/scripts/faultseg3d_baseline.py:553: FutureWarning: `torch.cuda.amp.GradScaler(args...)` is deprecated. Please use `torch.amp.GradScaler('cuda', args...)` instead.
reports/training/baseline_A_synthetic_bce_seed42.log:4:  scaler = torch.cuda.amp.GradScaler(enabled=amp_enabled)
reports/training/baseline_A_synthetic_bce_seed42.log:11:epoch=001 loss=0.314965 val_dice=0.000000 val_iou=0.000000 val_pr_auc=0.076771 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:12:epoch=002 loss=0.254361 val_dice=0.000000 val_iou=0.000000 val_pr_auc=0.096252 minutes=0.30
reports/training/baseline_A_synthetic_bce_seed42.log:13:epoch=003 loss=0.238950 val_dice=0.000000 val_iou=0.000000 val_pr_auc=0.182016 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:14:epoch=004 loss=0.200252 val_dice=0.118262 val_iou=0.062847 val_pr_auc=0.390901 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:15:epoch=005 loss=0.168745 val_dice=0.398029 val_iou=0.248462 val_pr_auc=0.481942 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:16:epoch=006 loss=0.153221 val_dice=0.465434 val_iou=0.303300 val_pr_auc=0.539682 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:17:epoch=007 loss=0.141764 val_dice=0.497805 val_iou=0.331385 val_pr_auc=0.586533 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:18:epoch=008 loss=0.135450 val_dice=0.534810 val_iou=0.365011 val_pr_auc=0.613936 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:19:epoch=009 loss=0.128391 val_dice=0.600041 val_iou=0.428614 val_pr_auc=0.641996 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:20:epoch=010 loss=0.122253 val_dice=0.583450 val_iou=0.411881 val_pr_auc=0.643059 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:21:epoch=011 loss=0.118308 val_dice=0.619101 val_iou=0.448332 val_pr_auc=0.686354 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:22:epoch=012 loss=0.112667 val_dice=0.641208 val_iou=0.471895 val_pr_auc=0.700150 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:23:epoch=013 loss=0.109114 val_dice=0.633384 val_iou=0.463469 val_pr_auc=0.715915 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:24:epoch=014 loss=0.106602 val_dice=0.650868 val_iou=0.482435 val_pr_auc=0.711744 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:25:epoch=015 loss=0.102564 val_dice=0.666159 val_iou=0.499429 val_pr_auc=0.731226 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:26:epoch=016 loss=0.099363 val_dice=0.685561 val_iou=0.521562 val_pr_auc=0.750862 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:27:epoch=017 loss=0.097281 val_dice=0.687228 val_iou=0.523494 val_pr_auc=0.757492 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:28:epoch=018 loss=0.093142 val_dice=0.689824 val_iou=0.526513 val_pr_auc=0.765094 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:29:epoch=019 loss=0.093322 val_dice=0.693366 val_iou=0.530651 val_pr_auc=0.769579 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:30:epoch=020 loss=0.089892 val_dice=0.718609 val_iou=0.560804 val_pr_auc=0.786135 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:31:epoch=021 loss=0.088231 val_dice=0.706142 val_iou=0.545765 val_pr_auc=0.776918 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:2:device=cuda; parameters=1,459,585; amp=True
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:3:/shared/home/khavarj/projects/fault_detection/scripts/faultseg3d_baseline.py:553: FutureWarning: `torch.cuda.amp.GradScaler(args...)` is deprecated. Please use `torch.amp.GradScaler('cuda', args...)` instead.
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:4:  scaler = torch.cuda.amp.GradScaler(enabled=amp_enabled)
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:11:epoch=001 loss=1.044174 val_dice=0.220347 val_iou=0.123815 val_pr_auc=0.148267 minutes=0.32
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:12:epoch=002 loss=0.861660 val_dice=0.330021 val_iou=0.197620 val_pr_auc=0.352460 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:13:epoch=003 loss=0.738569 val_dice=0.395203 val_iou=0.246264 val_pr_auc=0.445970 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:14:epoch=004 loss=0.669487 val_dice=0.445811 val_iou=0.286844 val_pr_auc=0.506100 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:15:epoch=005 loss=0.623482 val_dice=0.465448 val_iou=0.303312 val_pr_auc=0.544250 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:16:epoch=006 loss=0.581583 val_dice=0.524423 val_iou=0.355402 val_pr_auc=0.591176 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:17:epoch=007 loss=0.542672 val_dice=0.502238 val_iou=0.335326 val_pr_auc=0.626267 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:18:epoch=008 loss=0.501275 val_dice=0.549318 val_iou=0.378662 val_pr_auc=0.664116 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:19:epoch=009 loss=0.463011 val_dice=0.595464 val_iou=0.423958 val_pr_auc=0.699814 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:20:epoch=010 loss=0.438031 val_dice=0.629139 val_iou=0.458937 val_pr_auc=0.719178 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:21:epoch=011 loss=0.414671 val_dice=0.645080 val_iou=0.476102 val_pr_auc=0.733999 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:22:epoch=012 loss=0.398844 val_dice=0.607199 val_iou=0.435955 val_pr_auc=0.718977 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:23:epoch=013 loss=0.377859 val_dice=0.631336 val_iou=0.461280 val_pr_auc=0.757730 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:24:epoch=014 loss=0.364058 val_dice=0.675847 val_iou=0.510400 val_pr_auc=0.768168 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:25:epoch=015 loss=0.352412 val_dice=0.654198 val_iou=0.486103 val_pr_auc=0.759199 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:26:epoch=016 loss=0.342353 val_dice=0.688899 val_iou=0.525436 val_pr_auc=0.774911 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:27:epoch=017 loss=0.335509 val_dice=0.678364 val_iou=0.513276 val_pr_auc=0.782113 minutes=0.32
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:28:epoch=018 loss=0.322418 val_dice=0.682413 val_iou=0.517926 val_pr_auc=0.791560 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:29:epoch=019 loss=0.317725 val_dice=0.684473 val_iou=0.520303 val_pr_auc=0.783781 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:30:epoch=020 loss=0.312603 val_dice=0.699316 val_iou=0.537653 val_pr_auc=0.800032 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:31:epoch=021 loss=0.304364 val_dice=0.666135 val_iou=0.499402 val_pr_auc=0.798243 minutes=0.31
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:2:parameters=45001057 epochs=100 train_patches=64 val_patches=32
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:3:epoch=1/100 train_patch=16/64 loss=0.50337
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:4:epoch=1/100 train_patch=32/64 loss=0.48165
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:5:epoch=1/100 train_patch=48/64 loss=0.39263
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:6:epoch=1/100 train_patch=64/64 loss=0.51061
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:7:EPOCH 001 train_loss=0.465645 val_loss=0.485600 val_dice=0.000000 val_precision=0.000000 val_recall=0.000000 best=0.000000 elapsed_min=8.5
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:8:epoch=2/100 train_patch=16/64 loss=0.50700
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:9:epoch=2/100 train_patch=32/64 loss=0.50687
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:10:epoch=2/100 train_patch=48/64 loss=0.51004
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:11:epoch=2/100 train_patch=64/64 loss=0.50326
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:12:EPOCH 002 train_loss=0.467679 val_loss=0.482254 val_dice=0.000000 val_precision=0.000000 val_recall=0.000000 best=0.000000 elapsed_min=17.0
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:13:epoch=3/100 train_patch=16/64 loss=0.50515
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:14:epoch=3/100 train_patch=32/64 loss=0.51582
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:15:epoch=3/100 train_patch=48/64 loss=0.38142
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:16:epoch=3/100 train_patch=64/64 loss=0.51498
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:17:EPOCH 003 train_loss=0.454671 val_loss=0.483168 val_dice=0.000000 val_precision=0.000000 val_recall=0.000000 best=0.000000 elapsed_min=25.5
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:18:epoch=4/100 train_patch=16/64 loss=0.35696
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:19:epoch=4/100 train_patch=32/64 loss=0.51711
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:20:epoch=4/100 train_patch=48/64 loss=0.51147
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:21:epoch=4/100 train_patch=64/64 loss=0.50276
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:22:EPOCH 004 train_loss=0.460464 val_loss=0.481467 val_dice=0.000000 val_precision=0.000000 val_recall=0.000000 best=0.000000 elapsed_min=34.0
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:23:epoch=5/100 train_patch=16/64 loss=0.50632
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:24:epoch=5/100 train_patch=32/64 loss=0.51415
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:25:epoch=5/100 train_patch=48/64 loss=0.50639
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:2:RESUME epoch=50 best_val_dice=0.367370
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:4:parameters=45001057 epochs=100 train_patches=64 val_patches=32
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:5:epoch=50/100 train_patch=16/64 loss=0.50684
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:6:epoch=50/100 train_patch=32/64 loss=0.51190
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:7:epoch=50/100 train_patch=48/64 loss=0.52828
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:8:epoch=50/100 train_patch=64/64 loss=0.25706
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:9:EPOCH 050 train_loss=0.416314 val_loss=0.453715 val_dice=0.286637 val_precision=0.180658 val_recall=0.693418 best=0.367370 elapsed_min=8.3
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:10:epoch=51/100 train_patch=16/64 loss=0.52553
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:11:epoch=51/100 train_patch=32/64 loss=0.50325
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:12:epoch=51/100 train_patch=48/64 loss=0.50754
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:13:epoch=51/100 train_patch=64/64 loss=0.50115
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:14:EPOCH 051 train_loss=0.453673 val_loss=0.453172 val_dice=0.262730 val_precision=0.211600 val_recall=0.346444 best=0.367370 elapsed_min=16.5
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:15:epoch=52/100 train_patch=16/64 loss=0.33214
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:16:epoch=52/100 train_patch=32/64 loss=0.50397
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:17:epoch=52/100 train_patch=48/64 loss=0.50738
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:18:epoch=52/100 train_patch=64/64 loss=0.50343
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:19:EPOCH 052 train_loss=0.409309 val_loss=0.442612 val_dice=0.376027 val_precision=0.282215 val_recall=0.563264 best=0.376027 elapsed_min=24.7
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:20:epoch=53/100 train_patch=16/64 loss=0.51703
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:21:epoch=53/100 train_patch=32/64 loss=0.52752
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:22:epoch=53/100 train_patch=48/64 loss=0.50514
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:23:epoch=53/100 train_patch=64/64 loss=0.32922
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:24:EPOCH 053 train_loss=0.439335 val_loss=0.443985 val_dice=0.380571 val_precision=0.424110 val_recall=0.345139 best=0.380571 elapsed_min=32.9
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:25:epoch=54/100 train_patch=16/64 loss=0.51174
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:26:epoch=54/100 train_patch=32/64 loss=0.50349
reports/training/r100_fp16_3seed_queue_20261014_145225.log:2:START seed=42 smoke=True pid=1899203 log=runs/R100_fp16_clean_3seeds_20261014_145225/smoke.log
reports/training/r100_fp16_3seed_queue_20261014_145510.log:1:START seed=42 smoke=True pid=1909458 log=runs/R100_fp16_clean_3seeds_20261014_145510/smoke.log
reports/training/r100_fp16_3seed_queue_20261014_145510.log:2:START seed=42 smoke=False pid=1911189 log=runs/R100_fp16_clean_3seeds_20261014_145510/seed42.log
reports/training/r100_fp16_3seed_queue_20261014_145510.log:8:    execute(run_dir, seed, expected_protocol=expected_protocol)
reports/training/r100_fp16_3seed_queue_20261014_150435.log:2:START seed=42 smoke=True pid=1945423 log=runs/R100_fp16_clean_3seeds_20261014_150435/smoke.log
reports/training/r100_fp16_3seed_queue_20261014_150435.log:3:START seed=42 smoke=False pid=1946437 log=runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log
reports/training/r100_fp16_3seed_queue_20261014_150435.log:4:PASS seed=42 validation_dice=0.544072
reports/training/r100_fp16_3seed_queue_20261014_150435.log:5:START seed=43 smoke=False pid=3264730 log=runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log
reports/training/r100_fp16_3seed_queue_20261014_150435.log:6:PASS seed=43 validation_dice=0.569856
reports/training/r100_fp16_3seed_queue_20261014_150435.log:7:START seed=44 smoke=False pid=379744 log=runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log
reports/training/r100_fp16_3seed_queue_20261014_150435.log:8:PASS seed=44 validation_dice=0.572980
reports/training/R100_thebe_seed42_20261005_102737.log:1:/shared/home/khavarj/projects/fault_detection/scripts/r100_full_run.py:237: FutureWarning: `torch.cuda.amp.GradScaler(args...)` is deprecated. Please use `torch.amp.GradScaler('cuda', args...)` instead.
reports/training/R100_thebe_seed42_20261005_102737.log:2:  scaler = torch.cuda.amp.GradScaler(enabled=True)
reports/training/R100_thebe_seed42_20261005_102737.log:12:epoch=001/100 loss=0.211608 val_dice=0.000006 val_pr_auc=0.034823 minutes=3.26
reports/training/R100_thebe_seed42_20261005_102737.log:14:epoch=002/100 loss=0.131591 val_dice=0.000001 val_pr_auc=0.039528 minutes=3.33
reports/training/R100_thebe_seed42_20261005_102737.log:16:epoch=003/100 loss=0.105220 val_dice=0.000001 val_pr_auc=0.043710 minutes=3.23
reports/training/R100_thebe_seed42_20261005_102737.log:18:epoch=004/100 loss=0.101674 val_dice=0.000000 val_pr_auc=0.043505 minutes=3.32
reports/training/R100_thebe_seed42_20261005_102737.log:20:epoch=005/100 loss=0.113378 val_dice=0.000000 val_pr_auc=0.038386 minutes=3.04
reports/training/R100_thebe_seed42_20261005_102737.log:22:epoch=006/100 loss=0.102869 val_dice=0.000000 val_pr_auc=0.047210 minutes=3.22
reports/training/R100_thebe_seed42_20261005_102737.log:24:epoch=007/100 loss=0.106725 val_dice=0.000000 val_pr_auc=0.049760 minutes=3.20
reports/training/R100_thebe_seed42_20261005_102737.log:26:epoch=008/100 loss=0.096674 val_dice=0.000000 val_pr_auc=0.048672 minutes=3.13
reports/training/R100_thebe_seed42_20261005_102737.log:28:epoch=009/100 loss=0.099541 val_dice=0.000000 val_pr_auc=0.043619 minutes=3.24
reports/training/R100_thebe_seed42_20261005_102737.log:30:epoch=010/100 loss=0.107934 val_dice=0.000000 val_pr_auc=0.055916 minutes=3.05
reports/training/R100_thebe_seed42_20261005_102737.log:32:epoch=011/100 loss=0.099936 val_dice=0.000000 val_pr_auc=0.061880 minutes=3.10
reports/training/R100_thebe_seed42_20261005_102737.log:34:epoch=012/100 loss=0.102164 val_dice=0.000000 val_pr_auc=0.049965 minutes=3.15
reports/training/R100_thebe_seed42_20261005_102737.log:36:epoch=013/100 loss=0.109964 val_dice=0.000000 val_pr_auc=0.061470 minutes=3.00
reports/training/R100_thebe_seed42_20261005_102737.log:38:epoch=014/100 loss=0.096900 val_dice=0.000000 val_pr_auc=0.089677 minutes=3.07
reports/training/R100_thebe_seed42_20261005_102737.log:40:epoch=015/100 loss=0.089464 val_dice=0.000000 val_pr_auc=0.117684 minutes=3.21
reports/training/R100_thebe_seed42_20261005_102737.log:42:epoch=016/100 loss=0.088687 val_dice=0.000000 val_pr_auc=0.107323 minutes=3.15
reports/training/R100_thebe_seed42_20261005_102737.log:44:epoch=017/100 loss=0.083734 val_dice=0.000000 val_pr_auc=0.135083 minutes=3.13
reports/training/R100_thebe_seed42_20261005_102737.log:46:epoch=018/100 loss=0.087998 val_dice=0.000000 val_pr_auc=0.171241 minutes=3.32
reports/training/R100_thebe_seed42_20261005_102737.log:48:epoch=019/100 loss=0.090926 val_dice=0.000000 val_pr_auc=0.184733 minutes=3.11
reports/training/R100_thebe_seed42_20261005_102737.log:50:epoch=020/100 loss=0.077623 val_dice=0.000000 val_pr_auc=0.207758 minutes=3.15
reports/training/R100_thebe_seed42_20261005_102737.log:52:epoch=021/100 loss=0.073180 val_dice=0.000013 val_pr_auc=0.213077 minutes=3.13
reports/training/R100_thebe_seed42_20261005_102737.log:54:epoch=022/100 loss=0.077549 val_dice=0.000690 val_pr_auc=0.212709 minutes=3.08
reports/training/R100_thebe_seed42_resume_20261005_131346.log:1:/shared/home/khavarj/projects/fault_detection/scripts/r100_full_run.py:250: FutureWarning: `torch.cuda.amp.GradScaler(args...)` is deprecated. Please use `torch.amp.GradScaler('cuda', args...)` instead.
reports/training/R100_thebe_seed42_resume_20261005_131346.log:2:  scaler = torch.cuda.amp.GradScaler(enabled=True)
reports/training/R100_thebe_seed42_resume_20261005_131346.log:4:RESUME PASS: completed epoch 23; continuing from epoch 24
reports/training/R100_thebe_seed42_resume_20261005_131346.log:13:epoch=024/100 loss=0.078920 val_dice=0.001420 val_pr_auc=0.236420 minutes=3.32
reports/training/R100_thebe_seed42_resume_20261005_131346.log:15:epoch=025/100 loss=0.065565 val_dice=0.002473 val_pr_auc=0.260316 minutes=3.20
reports/training/R100_thebe_seed42_resume_20261005_131346.log:17:epoch=026/100 loss=0.068080 val_dice=0.003456 val_pr_auc=0.263557 minutes=3.25
reports/training/R100_thebe_seed42_resume_20261005_131346.log:19:epoch=027/100 loss=0.080750 val_dice=0.011536 val_pr_auc=0.259436 minutes=3.12
reports/training/R100_thebe_seed42_resume_20261005_131346.log:21:epoch=028/100 loss=0.075161 val_dice=0.018024 val_pr_auc=0.297481 minutes=3.05
reports/training/R100_thebe_seed42_resume_20261005_131346.log:23:epoch=029/100 loss=0.084217 val_dice=0.048370 val_pr_auc=0.295427 minutes=3.27
reports/training/R100_thebe_seed42_resume_20261005_131346.log:25:epoch=030/100 loss=0.069108 val_dice=0.027934 val_pr_auc=0.322924 minutes=3.16
reports/training/R100_thebe_seed42_resume_20261005_131346.log:27:epoch=031/100 loss=0.078519 val_dice=0.077669 val_pr_auc=0.336544 minutes=3.02
reports/training/R100_thebe_seed42_resume_20261005_131346.log:29:epoch=032/100 loss=0.062892 val_dice=0.304055 val_pr_auc=0.336719 minutes=3.36
reports/training/R100_thebe_seed42_resume_20261005_131346.log:31:epoch=033/100 loss=0.072173 val_dice=0.149602 val_pr_auc=0.348334 minutes=3.39
reports/training/R100_thebe_seed42_resume_20261005_131346.log:33:epoch=034/100 loss=0.070201 val_dice=0.174907 val_pr_auc=0.342185 minutes=3.24
reports/training/R100_thebe_seed42_resume_20261005_131346.log:35:epoch=035/100 loss=0.073527 val_dice=0.148241 val_pr_auc=0.369592 minutes=3.27
reports/training/R100_thebe_seed42_resume_20261005_131346.log:37:epoch=036/100 loss=0.069229 val_dice=0.193048 val_pr_auc=0.379670 minutes=3.25
reports/training/R100_thebe_seed42_resume_20261005_131346.log:39:epoch=037/100 loss=0.063905 val_dice=0.006665 val_pr_auc=0.330679 minutes=3.15
reports/training/R100_thebe_seed42_resume_20261005_131346.log:41:epoch=038/100 loss=0.080337 val_dice=0.244056 val_pr_auc=0.374059 minutes=3.23
reports/training/R100_thebe_seed42_resume_20261005_131346.log:43:epoch=039/100 loss=0.066486 val_dice=0.255052 val_pr_auc=0.404267 minutes=3.12
reports/training/R100_thebe_seed42_resume_20261005_131346.log:45:epoch=040/100 loss=0.065938 val_dice=0.210433 val_pr_auc=0.382206 minutes=3.17
reports/training/R100_thebe_seed42_resume_20261005_131346.log:47:epoch=041/100 loss=0.062026 val_dice=0.407483 val_pr_auc=0.373383 minutes=3.09
reports/training/R100_thebe_seed42_resume_20261005_131346.log:49:epoch=042/100 loss=0.075279 val_dice=0.123915 val_pr_auc=0.388560 minutes=3.06
reports/training/R100_thebe_seed42_resume_20261005_131346.log:51:epoch=043/100 loss=0.065071 val_dice=0.270480 val_pr_auc=0.393687 minutes=3.09
reports/training/R100_thebe_seed42_resume_20261005_131346.log:53:epoch=044/100 loss=0.064441 val_dice=0.172999 val_pr_auc=0.384315 minutes=3.11
runs/baseline_A_smoke/run_config.json:3:  "batch_size": 1,
runs/baseline_A_smoke/run_config.json:8:  "epochs": 100,
runs/baseline_A_smoke/run_config.json:11:  "learning_rate": 0.0001,
runs/baseline_A_smoke/run_config.json:12:  "loss": "b0_bce",
runs/baseline_A_smoke/run_config.json:17:  "seed": 42,
runs/baseline_A_synthetic_bce_seed42/best.pt: binary file matches (found "\0" byte around offset 4)
runs/baseline_A_synthetic_bce_seed42/final_metrics.json:27:    "precision": 0.8030095271846518,
runs/baseline_A_synthetic_bce_seed42/final_metrics.json:31:    "threshold": 0.43896484375,
runs/baseline_A_synthetic_bce_seed42/final_metrics.json:99:    "precision": {
runs/baseline_A_synthetic_bce_seed42/final_metrics.json:138:    "precision": 0.7991951500999772,
runs/baseline_A_synthetic_bce_seed42/final_metrics.json:142:    "threshold": 0.43896484375,
runs/baseline_A_synthetic_bce_seed42/final_metrics.json:210:    "precision": {
runs/baseline_A_synthetic_bce_seed42/history.csv:1:epoch,train_loss,optimizer_steps,seconds,val_threshold,val_dice,val_iou,val_precision,val_recall,val_specificity,val_balanced_accuracy,val_accuracy,val_mcc,val_pr_auc_approx,val_roc_auc_approx,val_tp,val_fp,val_fn,val_tn
runs/baseline_A_synthetic_bce_seed42/last.pt: binary file matches (found "\0" byte around offset 4)
runs/baseline_A_synthetic_bce_seed42/run_config.json:3:  "batch_size": 1,
runs/baseline_A_synthetic_bce_seed42/run_config.json:8:  "epochs": 100,
runs/baseline_A_synthetic_bce_seed42/run_config.json:14:  "learning_rate": 0.0001,
runs/baseline_A_synthetic_bce_seed42/run_config.json:15:  "loss": "b0_bce",
runs/baseline_A_synthetic_bce_seed42/run_config.json:22:  "seed": 42,
runs/baseline_A_synthetic_bce_seed42/test_per_volume.csv:1:volume_id,threshold,dice,iou,precision,recall,specificity,balanced_accuracy,accuracy,mcc,pr_auc_approx,roc_auc_approx,tp,fp,fn,tn,modified_hausdorff_voxels,bidirectional_chamfer_voxels,prediction_empty,target_empty,inference_seconds
runs/baseline_A_synthetic_bce_seed42/validation_per_volume.csv:1:volume_id,threshold,dice,iou,precision,recall,specificity,balanced_accuracy,accuracy,mcc,pr_auc_approx,roc_auc_approx,tp,fp,fn,tn,modified_hausdorff_voxels,bidirectional_chamfer_voxels,prediction_empty,target_empty,inference_seconds
runs/loss_ablation_L1_weighted_bce_dice_seed42/best.pt: binary file matches (found "\0" byte around offset 4)
runs/loss_ablation_L1_weighted_bce_dice_seed42/final_metrics.json:27:    "precision": 0.8041099575085737,
runs/loss_ablation_L1_weighted_bce_dice_seed42/final_metrics.json:31:    "threshold": 0.85302734375,
runs/loss_ablation_L1_weighted_bce_dice_seed42/final_metrics.json:99:    "precision": {
runs/loss_ablation_L1_weighted_bce_dice_seed42/final_metrics.json:138:    "precision": 0.7992400416395384,
runs/loss_ablation_L1_weighted_bce_dice_seed42/final_metrics.json:142:    "threshold": 0.85302734375,
runs/loss_ablation_L1_weighted_bce_dice_seed42/final_metrics.json:210:    "precision": {
runs/loss_ablation_L1_weighted_bce_dice_seed42/history.csv:1:epoch,train_loss,optimizer_steps,seconds,val_threshold,val_dice,val_iou,val_precision,val_recall,val_specificity,val_balanced_accuracy,val_accuracy,val_mcc,val_pr_auc_approx,val_roc_auc_approx,val_tp,val_fp,val_fn,val_tn
runs/loss_ablation_L1_weighted_bce_dice_seed42/last.pt: binary file matches (found "\0" byte around offset 4)
runs/loss_ablation_L1_weighted_bce_dice_seed42/run_config.json:3:  "batch_size": 1,
runs/loss_ablation_L1_weighted_bce_dice_seed42/run_config.json:8:  "epochs": 100,
runs/loss_ablation_L1_weighted_bce_dice_seed42/run_config.json:10:  "experiment_name": "Loss Ablation L1 \u2014 weighted BCE plus Dice",
runs/loss_ablation_L1_weighted_bce_dice_seed42/run_config.json:14:  "learning_rate": 0.0001,
runs/loss_ablation_L1_weighted_bce_dice_seed42/run_config.json:15:  "loss": "b1_weighted_dice",
runs/loss_ablation_L1_weighted_bce_dice_seed42/run_config.json:16:  "loss_description": "0.5 weighted BCE plus 0.5 soft Dice loss",
runs/loss_ablation_L1_weighted_bce_dice_seed42/run_config.json:22:  "seed": 42,
runs/loss_ablation_L1_weighted_bce_dice_seed42/test_per_volume.csv:1:volume_id,threshold,dice,iou,precision,recall,specificity,balanced_accuracy,accuracy,mcc,pr_auc_approx,roc_auc_approx,tp,fp,fn,tn,modified_hausdorff_voxels,bidirectional_chamfer_voxels,prediction_empty,target_empty,inference_seconds
runs/loss_ablation_L1_weighted_bce_dice_seed42/validation_per_volume.csv:1:volume_id,threshold,dice,iou,precision,recall,specificity,balanced_accuracy,accuracy,mcc,pr_auc_approx,roc_auc_approx,tp,fp,fn,tn,modified_hausdorff_voxels,bidirectional_chamfer_voxels,prediction_empty,target_empty,inference_seconds
runs/p1_attention3d_caft_seed42/best_p1_attention3d_caft_seed42_epoch093_faultseg3d_synthetic_20261009.pt: binary file matches (found "\0" byte around offset 4)
runs/p1_attention3d_caft_seed42/best.pt: binary file matches (found "\0" byte around offset 4)
runs/p1_attention3d_caft_seed42/final_metrics.json:27:    "precision": 0.7967662250168426,
runs/p1_attention3d_caft_seed42/final_metrics.json:31:    "threshold": 0.98095703125,
runs/p1_attention3d_caft_seed42/final_metrics.json:99:    "precision": {
runs/p1_attention3d_caft_seed42/final_metrics.json:138:    "precision": 0.7919055523009829,
runs/p1_attention3d_caft_seed42/final_metrics.json:142:    "threshold": 0.98095703125,
runs/p1_attention3d_caft_seed42/final_metrics.json:210:    "precision": {
runs/p1_attention3d_caft_seed42/history.csv:1:epoch,train_loss,optimizer_steps,seconds,val_threshold,val_dice,val_iou,val_precision,val_recall,val_specificity,val_balanced_accuracy,val_accuracy,val_mcc,val_pr_auc_approx,val_roc_auc_approx,val_tp,val_fp,val_fn,val_tn,train_caft_loss,train_attention_loss
runs/p1_attention3d_caft_seed42/last.pt: binary file matches (found "\0" byte around offset 4)
runs/p1_attention3d_caft_seed42/run_config.json:5:  "batch_size": 1,
runs/p1_attention3d_caft_seed42/run_config.json:12:  "epochs": 100,
runs/p1_attention3d_caft_seed42/run_config.json:18:  "learning_rate": 0.0001,
runs/p1_attention3d_caft_seed42/run_config.json:19:  "loss": "p1_connectivity_aware_focal_tversky_plus_aam_smooth_l1",
runs/p1_attention3d_caft_seed42/run_config.json:24:  "seed": 42,
runs/p1_attention3d_caft_seed42/test_per_volume.csv:1:volume_id,threshold,dice,iou,precision,recall,specificity,balanced_accuracy,accuracy,mcc,pr_auc_approx,roc_auc_approx,tp,fp,fn,tn,modified_hausdorff_voxels,bidirectional_chamfer_voxels,prediction_empty,target_empty,inference_seconds
runs/p1_attention3d_caft_seed42/train.log:2:device=cuda; parameters=1,467,411; amp=True
runs/p1_attention3d_caft_seed42/train.log:3:/shared/home/khavarj/projects/fault_detection/scripts/faultseg3d_baseline.py:553: FutureWarning: `torch.cuda.amp.GradScaler(args...)` is deprecated. Please use `torch.amp.GradScaler('cuda', args...)` instead.
runs/p1_attention3d_caft_seed42/train.log:4:  scaler = torch.cuda.amp.GradScaler(enabled=amp_enabled)
runs/p1_attention3d_caft_seed42/train.log:14:epoch=001 loss=0.838507 val_dice=0.127385 val_iou=0.068025 val_pr_auc=0.071179 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:15:epoch=002 loss=0.829427 val_dice=0.127352 val_iou=0.068007 val_pr_auc=0.068252 minutes=0.34
runs/p1_attention3d_caft_seed42/train.log:16:epoch=003 loss=0.827917 val_dice=0.131709 val_iou=0.070497 val_pr_auc=0.071798 minutes=0.34
runs/p1_attention3d_caft_seed42/train.log:17:epoch=004 loss=0.776252 val_dice=0.223383 val_iou=0.125735 val_pr_auc=0.135151 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:18:epoch=005 loss=0.571470 val_dice=0.382732 val_iou=0.236653 val_pr_auc=0.240804 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:19:epoch=006 loss=0.454002 val_dice=0.474475 val_iou=0.311024 val_pr_auc=0.342266 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:20:epoch=007 loss=0.385372 val_dice=0.540523 val_iou=0.370354 val_pr_auc=0.394514 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:21:epoch=008 loss=0.328829 val_dice=0.568067 val_iou=0.396713 val_pr_auc=0.432253 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:22:epoch=009 loss=0.295809 val_dice=0.607155 val_iou=0.435910 val_pr_auc=0.482395 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:23:epoch=010 loss=0.274992 val_dice=0.622836 val_iou=0.452260 val_pr_auc=0.492261 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:24:epoch=011 loss=0.248961 val_dice=0.641727 val_iou=0.472458 val_pr_auc=0.531435 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:25:epoch=012 loss=0.233057 val_dice=0.643216 val_iou=0.474074 val_pr_auc=0.512073 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:26:epoch=013 loss=0.218292 val_dice=0.668364 val_iou=0.501912 val_pr_auc=0.551982 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:27:epoch=014 loss=0.211313 val_dice=0.675591 val_iou=0.510108 val_pr_auc=0.570569 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:28:epoch=015 loss=0.200009 val_dice=0.686478 val_iou=0.522623 val_pr_auc=0.580324 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:29:epoch=016 loss=0.190337 val_dice=0.672484 val_iou=0.506574 val_pr_auc=0.567807 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:30:epoch=017 loss=0.186106 val_dice=0.705062 val_iou=0.544475 val_pr_auc=0.590438 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:31:epoch=018 loss=0.179119 val_dice=0.700617 val_iou=0.539192 val_pr_auc=0.589192 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:32:epoch=019 loss=0.176469 val_dice=0.708570 val_iou=0.548671 val_pr_auc=0.597900 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:33:epoch=020 loss=0.171612 val_dice=0.707628 val_iou=0.547543 val_pr_auc=0.592573 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:34:epoch=021 loss=0.166923 val_dice=0.701295 val_iou=0.539995 val_pr_auc=0.589884 minutes=0.35
runs/p1_attention3d_caft_seed42/validation_per_volume.csv:1:volume_id,threshold,dice,iou,precision,recall,specificity,balanced_accuracy,accuracy,mcc,pr_auc_approx,roc_auc_approx,tp,fp,fn,tn,modified_hausdorff_voxels,bidirectional_chamfer_voxels,prediction_empty,target_empty,inference_seconds
runs/paper_attention3d_thebe_smoke_20261009_170246/history.csv:1:epoch,train_loss,val_loss,val_dice,val_precision,val_recall,val_fault_prevalence,lr,seconds_elapsed
runs/paper_attention3d_thebe_smoke_20261009_170246/run_configuration.json:22:  "threshold": 0.5,
runs/paper_attention3d_thebe_smoke_20261009_170246/run_configuration.json:23:  "patch_size": 64,
runs/paper_attention3d_thebe_smoke_20261009_170246/run_configuration.json:28:  "optimizer": "AdamW 5e-4, weight_decay 1e-4",
runs/paper_attention3d_thebe_smoke_20261009_170246/run_configuration.json:29:  "loss": "authors' UnifiedFocalLoss; lambda=0.5, alpha=0.3, beta=0.7",
runs/paper_attention3d_thebe_smoke_20261009_170246/run_configuration.json:31:  "seed": 42,
runs/paper_attention3d_thebe_supervised_seed42/best.pt: binary file matches (found "\0" byte around offset 4)
runs/paper_attention3d_thebe_supervised_seed42_bf16_clean/best.pt: binary file matches (found "\0" byte around offset 4)
runs/paper_attention3d_thebe_supervised_seed42_bf16_clean/history.csv:1:epoch,train_loss,val_loss,val_dice,val_precision,val_recall,val_fault_prevalence,lr,seconds_elapsed
runs/paper_attention3d_thebe_supervised_seed42_bf16_clean/last.pt: binary file matches (found "\0" byte around offset 4)
runs/paper_attention3d_thebe_supervised_seed42_bf16_clean/run_configuration.json:22:  "threshold": 0.5,
runs/paper_attention3d_thebe_supervised_seed42_bf16_clean/run_configuration.json:23:  "patch_size": 64,
runs/paper_attention3d_thebe_supervised_seed42_bf16_clean/run_configuration.json:28:  "optimizer": "AdamW 5e-4, weight_decay 1e-4",
runs/paper_attention3d_thebe_supervised_seed42_bf16_clean/run_configuration.json:29:  "precision": "BF16 autocast; gradient scaling disabled",
runs/paper_attention3d_thebe_supervised_seed42_bf16_clean/run_configuration.json:30:  "nonfinite_policy": "abort on nonfinite normalized input, logits, loss, or gradient norm",
runs/paper_attention3d_thebe_supervised_seed42_bf16_clean/run_configuration.json:31:  "loss": "authors' UnifiedFocalLoss; lambda=0.5, alpha=0.3, beta=0.7",
runs/paper_attention3d_thebe_supervised_seed42_bf16_clean/run_configuration.json:33:  "seed": 42,
runs/paper_attention3d_thebe_supervised_seed42/history.csv:1:epoch,train_loss,val_loss,val_dice,val_precision,val_recall,val_fault_prevalence,lr,seconds_elapsed
runs/paper_attention3d_thebe_supervised_seed42/last.pt: binary file matches (found "\0" byte around offset 4)
runs/paper_attention3d_thebe_supervised_seed42/run_configuration.json:22:  "threshold": 0.5,
runs/paper_attention3d_thebe_supervised_seed42/run_configuration.json:23:  "patch_size": 64,
runs/paper_attention3d_thebe_supervised_seed42/run_configuration.json:28:  "optimizer": "AdamW 5e-4, weight_decay 1e-4",
runs/paper_attention3d_thebe_supervised_seed42/run_configuration.json:29:  "loss": "authors' UnifiedFocalLoss; lambda=0.5, alpha=0.3, beta=0.7",
runs/paper_attention3d_thebe_supervised_seed42/run_configuration.json:31:  "seed": 42,
runs/R100_fp16_clean_3seeds_20261014_145225/smoke.log:2:QUEUE LAUNCH 2026-10-14T10:52:25.591945+00:00 ["/shared/home/khavarj/projects/fault_detection/.venv_train/bin/python", "-u", "/shared/home/khavarj/projects/fault_detection/scripts/train_r100_fp16_clean.py", "--seed", "42", "--validation-seed", "1042", "--thebe-root", "data/processed/thebe_h5", "--run-dir", "runs/R100_fp16_clean_3seeds_20261014_145225/smoke_seed42", "--smoke"]
runs/R100_fp16_clean_3seeds_20261014_145510/seed42.log:2:QUEUE LAUNCH 2026-10-14T10:55:28.511666+00:00 ["/shared/home/khavarj/projects/fault_detection/.venv_train/bin/python", "-u", "/shared/home/khavarj/projects/fault_detection/scripts/train_r100_fp16_clean.py", "--seed", "42", "--validation-seed", "1042", "--thebe-root", "data/processed/thebe_h5", "--run-dir", "runs/R100_fp16_clean_3seeds_20261014_145510/seed42"]
runs/R100_fp16_clean_3seeds_20261014_145510/seed42/run_config.json:3:  "seed": 42,
runs/R100_fp16_clean_3seeds_20261014_145510/seed42/run_config.json:5:  "precision": "float16_autocast",
runs/R100_fp16_clean_3seeds_20261014_145510/seed42/run_config.json:732:  "epochs": 100,
runs/R100_fp16_clean_3seeds_20261014_145510/seed42/run_config.json:734:  "patch_size": 128,
runs/R100_fp16_clean_3seeds_20261014_145510/seed42/run_config.json:737:  "train_sampling": "40 observed random patches per train file each epoch; random axis-0 flip",
runs/R100_fp16_clean_3seeds_20261014_145510/seed42/run_config.json:739:  "normalization": "per-patch z-score over observed voxels; axis reversal",
runs/R100_fp16_clean_3seeds_20261014_145510/seed42/run_config.json:741:  "optimizer": "Adam",
runs/R100_fp16_clean_3seeds_20261014_145510/seed42/run_config.json:742:  "learning_rate": 0.0001,
runs/R100_fp16_clean_3seeds_20261014_145510/seed42/run_config.json:743:  "loss": "ordinary BCE averaged over observed voxels",
runs/R100_fp16_clean_3seeds_20261014_145510/smoke.log:2:QUEUE LAUNCH 2026-10-14T10:55:10.825417+00:00 ["/shared/home/khavarj/projects/fault_detection/.venv_train/bin/python", "-u", "/shared/home/khavarj/projects/fault_detection/scripts/train_r100_fp16_clean.py", "--seed", "42", "--validation-seed", "1042", "--thebe-root", "data/processed/thebe_h5", "--run-dir", "runs/R100_fp16_clean_3seeds_20261014_145510/smoke_seed42", "--smoke"]
runs/R100_fp16_clean_3seeds_20261014_145510/smoke.log:7:epoch=1/1 train_patch=18/18 loss=0.759043
runs/R100_fp16_clean_3seeds_20261014_145510/smoke.log:12:epoch=001/1 loss=0.779829 val_dice=0.068725 val_pr_auc=0.033207 minutes=0.22
runs/R100_fp16_clean_3seeds_20261014_145510/smoke.log:13:BEST EPOCH: 1; full validation begins
runs/R100_fp16_clean_3seeds_20261014_145510/smoke.log:14:VALIDATION THRESHOLD: 0.427246; test evaluation disabled
runs/R100_fp16_clean_3seeds_20261014_145510/smoke.log:15:R100 VALIDATION-ONLY COMPLETE seed=42 epochs=1 best_epoch=1
runs/R100_fp16_clean_3seeds_20261014_145510/smoke_seed42/best.pt: binary file matches (found "\0" byte around offset 4)
runs/R100_fp16_clean_3seeds_20261014_145510/smoke_seed42/history.csv:1:epoch,train_loss,train_patches,resampled_no_data_candidates,excluded_training_positive_labels,seconds,val_threshold,val_dice,val_iou,val_precision,val_recall,val_specificity,val_balanced_accuracy,val_accuracy,val_mcc,val_pr_auc_approx,val_roc_auc_approx,val_tp,val_fp,val_fn,val_tn
runs/R100_fp16_clean_3seeds_20261014_145510/smoke_seed42/last.pt: binary file matches (found "\0" byte around offset 4)
runs/R100_fp16_clean_3seeds_20261014_145510/smoke_seed42/run_config.json:3:  "seed": 42,
runs/R100_fp16_clean_3seeds_20261014_145510/smoke_seed42/run_config.json:5:  "precision": "float16_autocast",
runs/R100_fp16_clean_3seeds_20261014_145510/smoke_seed42/run_config.json:102:  "epochs": 1,
runs/R100_fp16_clean_3seeds_20261014_145510/smoke_seed42/run_config.json:104:  "patch_size": 128,
runs/R100_fp16_clean_3seeds_20261014_145510/smoke_seed42/run_config.json:107:  "train_sampling": "2 observed random patches per train file each epoch; random axis-0 flip",
runs/R100_fp16_clean_3seeds_20261014_145510/smoke_seed42/run_config.json:109:  "normalization": "per-patch z-score over observed voxels; axis reversal",
runs/R100_fp16_clean_3seeds_20261014_145510/smoke_seed42/run_config.json:111:  "optimizer": "Adam",
runs/R100_fp16_clean_3seeds_20261014_145510/smoke_seed42/run_config.json:112:  "learning_rate": 0.0001,
runs/R100_fp16_clean_3seeds_20261014_145510/smoke_seed42/run_config.json:113:  "loss": "ordinary BCE averaged over observed voxels",
runs/R100_fp16_clean_3seeds_20261014_145510/smoke_seed42/status.json:3:  "seed": 42,
runs/R100_fp16_clean_3seeds_20261014_145510/smoke_seed42/status.json:7:  "precision": "float16_autocast",
runs/R100_fp16_clean_3seeds_20261014_145510/smoke_seed42/status.json:11:  "threshold": 0.42724609375,
runs/R100_fp16_clean_3seeds_20261014_145510/smoke_seed42/validation_selection.json:3:  "threshold": 0.42724609375,
runs/R100_fp16_clean_3seeds_20261014_145510/smoke_seed42/validation_selection.json:6:    "threshold": 0.42724609375,
runs/R100_fp16_clean_3seeds_20261014_145510/smoke_seed42/validation_selection.json:9:    "precision": 0.035650329241587765,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:16:      "seed": 42,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:19:      "threshold": 0.31640625,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:21:        "threshold": 0.31640625,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:24:        "precision": 0.5267658204531103,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:41:      "seed": 43,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:44:      "threshold": 0.279296875,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:46:        "threshold": 0.279296875,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:49:        "precision": 0.5643889729910121,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:66:      "seed": 44,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:69:      "threshold": 0.244140625,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:71:        "threshold": 0.244140625,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:74:        "precision": 0.5655692044103381,
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/best.pt: binary file matches (found "\0" byte around offset 4)
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/history.csv:1:epoch,train_loss,train_patches,resampled_no_data_candidates,excluded_training_positive_labels,seconds,val_threshold,val_dice,val_iou,val_precision,val_recall,val_specificity,val_balanced_accuracy,val_accuracy,val_mcc,val_pr_auc_approx,val_roc_auc_approx,val_tp,val_fp,val_fn,val_tn
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/last.pt: binary file matches (found "\0" byte around offset 4)
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:2:QUEUE LAUNCH 2026-10-14T11:04:49.680315+00:00 ["/shared/home/khavarj/projects/fault_detection/.venv_train/bin/python", "-u", "/shared/home/khavarj/projects/fault_detection/scripts/train_r100_fp16_clean.py", "--seed", "42", "--validation-seed", "1042", "--thebe-root", "data/processed/thebe_h5", "--run-dir", "runs/R100_fp16_clean_3seeds_20261014_150435/seed42"]
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:7:epoch=1/100 train_patch=60/360 loss=0.269200
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:8:epoch=1/100 train_patch=120/360 loss=0.096066
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:9:epoch=1/100 train_patch=180/360 loss=0.145327
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:10:epoch=1/100 train_patch=240/360 loss=0.151376
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:11:epoch=1/100 train_patch=300/360 loss=0.019122
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:12:epoch=1/100 train_patch=360/360 loss=0.668354
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:18:epoch=001/100 loss=0.211608 val_dice=0.000006 val_pr_auc=0.034823 minutes=3.12
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:19:epoch=2/100 train_patch=60/360 loss=0.223522
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:20:epoch=2/100 train_patch=120/360 loss=0.020627
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:21:epoch=2/100 train_patch=180/360 loss=0.265117
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:22:epoch=2/100 train_patch=240/360 loss=0.046374
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:23:epoch=2/100 train_patch=300/360 loss=0.051667
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:24:epoch=2/100 train_patch=360/360 loss=0.037058
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:26:epoch=002/100 loss=0.131591 val_dice=0.000001 val_pr_auc=0.039528 minutes=3.08
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:27:epoch=3/100 train_patch=60/360 loss=0.030490
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:28:epoch=3/100 train_patch=120/360 loss=0.011700
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:29:epoch=3/100 train_patch=180/360 loss=0.011385
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:30:epoch=3/100 train_patch=240/360 loss=0.005840
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:31:epoch=3/100 train_patch=300/360 loss=0.293844
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:32:epoch=3/100 train_patch=360/360 loss=0.045493
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:34:epoch=003/100 loss=0.105220 val_dice=0.000001 val_pr_auc=0.043710 minutes=3.09
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:35:epoch=4/100 train_patch=60/360 loss=0.025259
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:36:epoch=4/100 train_patch=120/360 loss=0.279557
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/run_config.json:3:  "seed": 42,
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/run_config.json:5:  "precision": "float16_autocast",
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/run_config.json:732:  "epochs": 100,
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/run_config.json:734:  "patch_size": 128,
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/run_config.json:737:  "train_sampling": "40 observed random patches per train file each epoch; random axis-0 flip",
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/run_config.json:739:  "normalization": "per-patch z-score over observed voxels; axis reversal",
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/run_config.json:741:  "optimizer": "Adam",
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/run_config.json:742:  "learning_rate": 0.0001,
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/run_config.json:743:  "loss": "ordinary BCE averaged over observed voxels",
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/status.json:3:  "seed": 42,
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/status.json:7:  "precision": "float16_autocast",
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/status.json:11:  "threshold": 0.31640625,
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/validation_selection.json:3:  "threshold": 0.31640625,
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/validation_selection.json:6:    "threshold": 0.31640625,
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/validation_selection.json:9:    "precision": 0.5267658204531103,
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/history.csv:1:epoch,train_loss,train_patches,resampled_no_data_candidates,excluded_training_positive_labels,seconds,val_threshold,val_dice,val_iou,val_precision,val_recall,val_specificity,val_balanced_accuracy,val_accuracy,val_mcc,val_pr_auc_approx,val_roc_auc_approx,val_tp,val_fp,val_fn,val_tn
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:2:QUEUE LAUNCH 2026-10-14T16:13:56.661530+00:00 ["/shared/home/khavarj/projects/fault_detection/.venv_train/bin/python", "-u", "/shared/home/khavarj/projects/fault_detection/scripts/train_r100_fp16_clean.py", "--seed", "43", "--validation-seed", "1042", "--thebe-root", "data/processed/thebe_h5", "--run-dir", "runs/R100_fp16_clean_3seeds_20261014_150435/seed43", "--expected-protocol", "1febc1e47ba203ff08db82816ceadf616a5e7db345054cfbe45274b84c5f5437"]
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:7:epoch=1/100 train_patch=60/360 loss=0.025100
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:8:epoch=1/100 train_patch=120/360 loss=0.089748
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:9:epoch=1/100 train_patch=180/360 loss=0.030659
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:10:epoch=1/100 train_patch=240/360 loss=0.035034
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:11:epoch=1/100 train_patch=300/360 loss=0.176485
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:12:epoch=1/100 train_patch=360/360 loss=0.013613
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:18:epoch=001/100 loss=0.207313 val_dice=0.000010 val_pr_auc=0.032889 minutes=3.25
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:19:epoch=2/100 train_patch=60/360 loss=0.143345
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:20:epoch=2/100 train_patch=120/360 loss=0.170271
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:21:epoch=2/100 train_patch=180/360 loss=0.178730
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:22:epoch=2/100 train_patch=240/360 loss=0.423158
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:23:epoch=2/100 train_patch=300/360 loss=0.202504
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:24:epoch=2/100 train_patch=360/360 loss=0.010068
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:26:epoch=002/100 loss=0.134325 val_dice=0.000000 val_pr_auc=0.037506 minutes=3.40
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:27:epoch=3/100 train_patch=60/360 loss=0.073450
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:28:epoch=3/100 train_patch=120/360 loss=0.002192
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:29:epoch=3/100 train_patch=180/360 loss=0.011881
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:30:epoch=3/100 train_patch=240/360 loss=0.008659
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:31:epoch=3/100 train_patch=300/360 loss=0.012940
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:32:epoch=3/100 train_patch=360/360 loss=0.163898
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:34:epoch=003/100 loss=0.113158 val_dice=0.000000 val_pr_auc=0.044267 minutes=3.32
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:35:epoch=4/100 train_patch=60/360 loss=0.117194
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:36:epoch=4/100 train_patch=120/360 loss=0.025358
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/run_config.json:3:  "seed": 43,
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/run_config.json:5:  "precision": "float16_autocast",
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/run_config.json:732:  "epochs": 100,
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/run_config.json:734:  "patch_size": 128,
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/run_config.json:737:  "train_sampling": "40 observed random patches per train file each epoch; random axis-0 flip",
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/run_config.json:739:  "normalization": "per-patch z-score over observed voxels; axis reversal",
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/run_config.json:741:  "optimizer": "Adam",
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/run_config.json:742:  "learning_rate": 0.0001,
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/run_config.json:743:  "loss": "ordinary BCE averaged over observed voxels",
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/status.json:3:  "seed": 43,
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/status.json:7:  "precision": "float16_autocast",
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/status.json:11:  "threshold": 0.279296875,
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/validation_selection.json:3:  "threshold": 0.279296875,
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/validation_selection.json:6:    "threshold": 0.279296875,
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/validation_selection.json:9:    "precision": 0.5643889729910121,
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/history.csv:1:epoch,train_loss,train_patches,resampled_no_data_candidates,excluded_training_positive_labels,seconds,val_threshold,val_dice,val_iou,val_precision,val_recall,val_specificity,val_balanced_accuracy,val_accuracy,val_mcc,val_pr_auc_approx,val_roc_auc_approx,val_tp,val_fp,val_fn,val_tn
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:2:QUEUE LAUNCH 2026-10-14T21:26:57.138315+00:00 ["/shared/home/khavarj/projects/fault_detection/.venv_train/bin/python", "-u", "/shared/home/khavarj/projects/fault_detection/scripts/train_r100_fp16_clean.py", "--seed", "44", "--validation-seed", "1042", "--thebe-root", "data/processed/thebe_h5", "--run-dir", "runs/R100_fp16_clean_3seeds_20261014_150435/seed44", "--expected-protocol", "1febc1e47ba203ff08db82816ceadf616a5e7db345054cfbe45274b84c5f5437"]
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:7:epoch=1/100 train_patch=60/360 loss=0.128812
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:8:epoch=1/100 train_patch=120/360 loss=0.049892
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:9:epoch=1/100 train_patch=180/360 loss=0.137484
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:10:epoch=1/100 train_patch=240/360 loss=0.094210
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:11:epoch=1/100 train_patch=300/360 loss=0.037499
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:12:epoch=1/100 train_patch=360/360 loss=1.847119
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:18:epoch=001/100 loss=0.214208 val_dice=0.000002 val_pr_auc=0.032531 minutes=2.98
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:19:epoch=2/100 train_patch=60/360 loss=0.102701
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:20:epoch=2/100 train_patch=120/360 loss=0.057482
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:21:epoch=2/100 train_patch=180/360 loss=0.037050
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:22:epoch=2/100 train_patch=240/360 loss=0.015849
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:23:epoch=2/100 train_patch=300/360 loss=0.191525
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:24:epoch=2/100 train_patch=360/360 loss=0.040938
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:26:epoch=002/100 loss=0.131131 val_dice=0.000002 val_pr_auc=0.041499 minutes=2.94
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:27:epoch=3/100 train_patch=60/360 loss=0.005686
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:28:epoch=3/100 train_patch=120/360 loss=0.168815
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:29:epoch=3/100 train_patch=180/360 loss=0.034031
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:30:epoch=3/100 train_patch=240/360 loss=0.198657
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:31:epoch=3/100 train_patch=300/360 loss=0.007568
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:32:epoch=3/100 train_patch=360/360 loss=0.196844
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:34:epoch=003/100 loss=0.093528 val_dice=0.000000 val_pr_auc=0.046544 minutes=3.03
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:35:epoch=4/100 train_patch=60/360 loss=0.133939
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:36:epoch=4/100 train_patch=120/360 loss=0.009925
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/run_config.json:3:  "seed": 44,
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/run_config.json:5:  "precision": "float16_autocast",
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/run_config.json:732:  "epochs": 100,
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/run_config.json:734:  "patch_size": 128,
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/run_config.json:737:  "train_sampling": "40 observed random patches per train file each epoch; random axis-0 flip",
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/run_config.json:739:  "normalization": "per-patch z-score over observed voxels; axis reversal",
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/run_config.json:741:  "optimizer": "Adam",
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/run_config.json:742:  "learning_rate": 0.0001,
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/run_config.json:743:  "loss": "ordinary BCE averaged over observed voxels",
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/status.json:3:  "seed": 44,
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/status.json:7:  "precision": "float16_autocast",
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/status.json:11:  "threshold": 0.244140625,
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/validation_selection.json:3:  "threshold": 0.244140625,
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/validation_selection.json:6:    "threshold": 0.244140625,
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/validation_selection.json:9:    "precision": 0.5655692044103381,
runs/R100_fp16_clean_3seeds_20261014_150435/smoke.log:2:QUEUE LAUNCH 2026-10-14T11:04:35.537330+00:00 ["/shared/home/khavarj/projects/fault_detection/.venv_train/bin/python", "-u", "/shared/home/khavarj/projects/fault_detection/scripts/train_r100_fp16_clean.py", "--seed", "42", "--validation-seed", "1042", "--thebe-root", "data/processed/thebe_h5", "--run-dir", "runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42", "--smoke"]
runs/R100_fp16_clean_3seeds_20261014_150435/smoke.log:7:epoch=1/1 train_patch=18/18 loss=0.759043
runs/R100_fp16_clean_3seeds_20261014_150435/smoke.log:12:epoch=001/1 loss=0.779829 val_dice=0.068725 val_pr_auc=0.033207 minutes=0.17
runs/R100_fp16_clean_3seeds_20261014_150435/smoke.log:13:BEST EPOCH: 1; full validation begins
runs/R100_fp16_clean_3seeds_20261014_150435/smoke.log:14:VALIDATION THRESHOLD: 0.427246; test evaluation disabled
runs/R100_fp16_clean_3seeds_20261014_150435/smoke.log:15:R100 VALIDATION-ONLY COMPLETE seed=42 epochs=1 best_epoch=1
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/best.pt: binary file matches (found "\0" byte around offset 4)
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/history.csv:1:epoch,train_loss,train_patches,resampled_no_data_candidates,excluded_training_positive_labels,seconds,val_threshold,val_dice,val_iou,val_precision,val_recall,val_specificity,val_balanced_accuracy,val_accuracy,val_mcc,val_pr_auc_approx,val_roc_auc_approx,val_tp,val_fp,val_fn,val_tn
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/last.pt: binary file matches (found "\0" byte around offset 4)
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/run_config.json:3:  "seed": 42,
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/run_config.json:5:  "precision": "float16_autocast",
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/run_config.json:102:  "epochs": 1,
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/run_config.json:104:  "patch_size": 128,
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/run_config.json:107:  "train_sampling": "2 observed random patches per train file each epoch; random axis-0 flip",
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/run_config.json:109:  "normalization": "per-patch z-score over observed voxels; axis reversal",
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/run_config.json:111:  "optimizer": "Adam",
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/run_config.json:112:  "learning_rate": 0.0001,
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/run_config.json:113:  "loss": "ordinary BCE averaged over observed voxels",
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/status.json:3:  "seed": 42,
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/status.json:7:  "precision": "float16_autocast",
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/status.json:11:  "threshold": 0.42724609375,
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/validation_selection.json:3:  "threshold": 0.42724609375,
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/validation_selection.json:6:    "threshold": 0.42724609375,
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/validation_selection.json:9:    "precision": 0.035650329241587765,
runs/R100_thebe_seed42_20261005_102737/best.pt: binary file matches (found "\0" byte around offset 4)
runs/R100_thebe_seed42_20261005_102737/final_metrics.json:29:    "precision": 0.5279583306670493,
runs/R100_thebe_seed42_20261005_102737/final_metrics.json:33:    "threshold": 0.1767578125,
runs/R100_thebe_seed42_20261005_102737/final_metrics.json:49:    "train_sampling": "360 randomly sampled observed patches per epoch from all 9 real train files",
runs/R100_thebe_seed42_20261005_102737/final_metrics.json:61:    "precision": 0.47191760787630943,
runs/R100_thebe_seed42_20261005_102737/final_metrics.json:65:    "threshold": 0.1767578125,
runs/R100_thebe_seed42_20261005_102737/final_metrics.json:133:    "precision": {
runs/R100_thebe_seed42_20261005_102737/final_metrics.json:163:  "resume_note": "Epoch 23 checkpoint had no saved RNG or AMP scaler state; weights and optimizer were restored, while sampling and scaler continued from a new state.",
runs/R100_thebe_seed42_20261005_102737/final_metrics.json:175:  "threshold": 0.1767578125,
runs/R100_thebe_seed42_20261005_102737/history.csv:1:epoch,train_loss,train_patches,resampled_no_data_candidates,excluded_training_positive_labels,seconds,val_threshold,val_dice,val_iou,val_precision,val_recall,val_specificity,val_balanced_accuracy,val_accuracy,val_mcc,val_pr_auc_approx,val_roc_auc_approx,val_tp,val_fp,val_fn,val_tn
runs/R100_thebe_seed42_20261005_102737/last.pt: binary file matches (found "\0" byte around offset 4)
runs/R100_thebe_seed42_20261005_102737/resume_protocol.json:3:  "old_selection": "Dice at threshold 0.5 on fixed 128 validation patches",
runs/R100_thebe_seed42_20261005_102737/resume_protocol.json:5:  "why": "Near-zero Dice at 0.5 despite improving PR-AUC; final threshold remains full-validation only",
runs/R100_thebe_seed42_20261005_102737/run_config.json:3:  "seed": 42,
runs/R100_thebe_seed42_20261005_102737/run_config.json:38:  "epochs": 100,
runs/R100_thebe_seed42_20261005_102737/run_config.json:40:  "patch_size": 128,
runs/R100_thebe_seed42_20261005_102737/run_config.json:43:  "train_sampling": "40 observed random patches per train file each epoch; random axis-0 flip",
runs/R100_thebe_seed42_20261005_102737/run_config.json:45:  "normalization": "per-patch z-score over observed voxels; axis reversal",
runs/R100_thebe_seed42_20261005_102737/run_config.json:47:  "optimizer": "Adam",
runs/R100_thebe_seed42_20261005_102737/run_config.json:48:  "learning_rate": 0.0001,
runs/R100_thebe_seed42_20261005_102737/run_config.json:49:  "loss": "ordinary BCE averaged over observed voxels",
runs/R100_thebe_seed42_20261005_102737/run_config.json:53:  "test_policy": "one complete test evaluation after checkpoint and threshold selection"
runs/R100_thebe_seed42_20261005_102737/test_per_patch.csv:1:patch_id,raw_voxels,valid_voxels,excluded_positive,inference_seconds,threshold,dice,iou,precision,recall,specificity,balanced_accuracy,accuracy,mcc,pr_auc_approx,roc_auc_approx,tp,fp,fn,tn,modified_hausdorff_voxels,bidirectional_chamfer_voxels,prediction_empty,target_empty
runs/R100_thebe_seed42_20261005_102737/validation_selection.json:3:  "threshold": 0.1767578125,
runs/R100_thebe_seed42_20261005_102737/validation_selection.json:6:    "threshold": 0.1767578125,
runs/R100_thebe_seed42_20261005_102737/validation_selection.json:9:    "precision": 0.5279583306670493,
scripts/attention3d_caft.py:2:"""Train the P1 AAM-Attention3D model with connectivity-aware focal Tversky.
scripts/attention3d_caft.py:5:pipeline. It replaces only the model and supervised loss. The final mask uses
scripts/attention3d_caft.py:89:            raise RuntimeError("Attention maps are unavailable for the training loss")
scripts/attention3d_caft.py:143:        # Fixed count normalization prevents the three edge sets dominating nodes.
scripts/attention3d_caft.py:175:            raise RuntimeError("P1 model was not initialized")
scripts/attention3d_caft.py:229:        raise RuntimeError("P1 loss was not initialized")
scripts/attention3d_caft.py:249:    args.loss = "p1_connectivity_aware_focal_tversky_plus_aam_smooth_l1"
scripts/evaluate_cracks_expert_zero_shot.py:22:PATCH = 128
scripts/evaluate_cracks_expert_zero_shot.py:34:    if length < PATCH:
scripts/evaluate_cracks_expert_zero_shot.py:35:        raise RuntimeError(f"Image dimension {length} is smaller than {PATCH}")
scripts/evaluate_cracks_expert_zero_shot.py:36:    values = list(range(0, length - PATCH + 1, STRIDE))
scripts/evaluate_cracks_expert_zero_shot.py:37:    last = length - PATCH
scripts/evaluate_cracks_expert_zero_shot.py:61:    parser.add_argument("--threshold-metrics", type=Path, required=True)
scripts/evaluate_cracks_expert_zero_shot.py:131:    threshold = float(
scripts/evaluate_cracks_expert_zero_shot.py:135:    model = Attention3D().cuda()
scripts/evaluate_cracks_expert_zero_shot.py:136:    model.load_state_dict(checkpoint["model"], strict=True)
scripts/evaluate_cracks_expert_zero_shot.py:137:    model.eval()
scripts/evaluate_cracks_expert_zero_shot.py:138:    for parameter in model.parameters():
scripts/evaluate_cracks_expert_zero_shot.py:153:            np.arange(center - PATCH // 2, center + PATCH // 2),
scripts/evaluate_cracks_expert_zero_shot.py:164:                    y0 : y0 + PATCH,
scripts/evaluate_cracks_expert_zero_shot.py:165:                    x0 : x0 + PATCH,
scripts/evaluate_cracks_expert_zero_shot.py:180:                    logits = model(tensor)
scripts/evaluate_cracks_expert_zero_shot.py:182:                    torch.sigmoid(logits.float())[0, 0, :, :, PATCH // 2]
scripts/evaluate_cracks_expert_zero_shot.py:188:                    y0 : y0 + PATCH, x0 : x0 + PATCH
scripts/evaluate_cracks_expert_zero_shot.py:191:                    y0 : y0 + PATCH, x0 : x0 + PATCH
scripts/evaluate_cracks_expert_zero_shot.py:204:        metrics = asdict(individual.metrics(threshold))
scripts/evaluate_cracks_expert_zero_shot.py:225:    final_metrics = asdict(aggregate.metrics(threshold))
scripts/evaluate_cracks_expert_zero_shot.py:232:        "checkpoint_epoch": int(checkpoint.get("epoch", -1)),
scripts/evaluate_cracks_expert_zero_shot.py:233:        "threshold": threshold,
scripts/evaluate_cracks_expert_zero_shot.py:258:    print(f"threshold={threshold:.6f}")
scripts/evaluate_cracks_expert_zero_shot.py:261:    print(f"precision={final_metrics['precision']:.6f}")
scripts/evaluate_thebe_p1_zero_shot.py:7:- takes its threshold from synthetic validation;
scripts/evaluate_thebe_p1_zero_shot.py:8:- standardizes each 128^3 input patch like Baseline A;
scripts/evaluate_thebe_p1_zero_shot.py:36:        for part in re.split(r"(\d+)", path.name)
scripts/evaluate_thebe_p1_zero_shot.py:152:        "precision",
scripts/evaluate_thebe_p1_zero_shot.py:224:        "--threshold-metrics",
scripts/evaluate_thebe_p1_zero_shot.py:248:        "--threshold-source-label",
scripts/evaluate_thebe_p1_zero_shot.py:297:    threshold = float(
scripts/evaluate_thebe_p1_zero_shot.py:303:    if not 0.0 < threshold < 1.0:
scripts/evaluate_thebe_p1_zero_shot.py:304:        raise RuntimeError(f"Invalid frozen threshold: {threshold}")
scripts/evaluate_thebe_p1_zero_shot.py:313:    patch_size = volume_shape[0]
scripts/evaluate_thebe_p1_zero_shot.py:320:    if "model" not in checkpoint:
scripts/evaluate_thebe_p1_zero_shot.py:321:        raise RuntimeError("Checkpoint does not contain model weights")
scripts/evaluate_thebe_p1_zero_shot.py:332:    model = Attention3D().to(device)
scripts/evaluate_thebe_p1_zero_shot.py:333:    model.load_state_dict(checkpoint["model"], strict=True)
scripts/evaluate_thebe_p1_zero_shot.py:334:    model.eval()
scripts/evaluate_thebe_p1_zero_shot.py:336:    for parameter in model.parameters():
scripts/evaluate_thebe_p1_zero_shot.py:340:    np.random.seed(42)
scripts/evaluate_thebe_p1_zero_shot.py:348:    x_starts = list(range(0, total_shape[0], patch_size))
scripts/evaluate_thebe_p1_zero_shot.py:349:    y_starts = list(range(0, total_shape[1], patch_size))
scripts/evaluate_thebe_p1_zero_shot.py:350:    z_starts = list(range(0, total_shape[2], patch_size))
scripts/evaluate_thebe_p1_zero_shot.py:375:        block_x1 = min(block_x0 + patch_size, total_shape[0])
scripts/evaluate_thebe_p1_zero_shot.py:376:        block_y1 = min(block_y0 + patch_size, total_shape[1])
scripts/evaluate_thebe_p1_zero_shot.py:422:        "checkpoint_epoch": int(checkpoint.get("epoch", -1)),
scripts/evaluate_thebe_p1_zero_shot.py:427:        "threshold": threshold,
scripts/evaluate_thebe_zero_shot.py:7:- takes its threshold from synthetic validation;
scripts/evaluate_thebe_zero_shot.py:8:- standardizes each 128^3 input patch like Baseline A;
scripts/evaluate_thebe_zero_shot.py:36:        for part in re.split(r"(\d+)", path.name)
scripts/evaluate_thebe_zero_shot.py:152:        "precision",
scripts/evaluate_thebe_zero_shot.py:224:        "--threshold-metrics",
scripts/evaluate_thebe_zero_shot.py:248:        "--threshold-source-label",
scripts/evaluate_thebe_zero_shot.py:297:    threshold = float(
scripts/evaluate_thebe_zero_shot.py:303:    if not 0.0 < threshold < 1.0:
scripts/evaluate_thebe_zero_shot.py:304:        raise RuntimeError(f"Invalid frozen threshold: {threshold}")
scripts/evaluate_thebe_zero_shot.py:313:    patch_size = volume_shape[0]
scripts/evaluate_thebe_zero_shot.py:320:    if "model" not in checkpoint:
scripts/evaluate_thebe_zero_shot.py:321:        raise RuntimeError("Checkpoint does not contain model weights")
scripts/evaluate_thebe_zero_shot.py:329:    model = baseline.FaultSeg3D().to(device)
scripts/evaluate_thebe_zero_shot.py:330:    model.load_state_dict(checkpoint["model"], strict=True)
scripts/evaluate_thebe_zero_shot.py:331:    model.eval()
scripts/evaluate_thebe_zero_shot.py:333:    for parameter in model.parameters():
scripts/evaluate_thebe_zero_shot.py:337:    np.random.seed(42)
scripts/evaluate_thebe_zero_shot.py:345:    x_starts = list(range(0, total_shape[0], patch_size))
scripts/evaluate_thebe_zero_shot.py:346:    y_starts = list(range(0, total_shape[1], patch_size))
scripts/evaluate_thebe_zero_shot.py:347:    z_starts = list(range(0, total_shape[2], patch_size))
scripts/evaluate_thebe_zero_shot.py:372:        block_x1 = min(block_x0 + patch_size, total_shape[0])
scripts/evaluate_thebe_zero_shot.py:373:        block_y1 = min(block_y0 + patch_size, total_shape[1])
scripts/evaluate_thebe_zero_shot.py:419:        "checkpoint_epoch": int(checkpoint.get("epoch", -1)),
scripts/evaluate_thebe_zero_shot.py:424:        "threshold": threshold,
scripts/evaluate_thebe_zero_shot_r100_pinned.py:7:- takes its threshold from synthetic validation;
scripts/evaluate_thebe_zero_shot_r100_pinned.py:8:- standardizes each 128^3 input patch like Baseline A;
scripts/evaluate_thebe_zero_shot_r100_pinned.py:36:        for part in re.split(r"(\d+)", path.name)
scripts/evaluate_thebe_zero_shot_r100_pinned.py:152:        "precision",
scripts/evaluate_thebe_zero_shot_r100_pinned.py:224:        "--threshold-metrics",
scripts/evaluate_thebe_zero_shot_r100_pinned.py:289:    threshold = float(
scripts/evaluate_thebe_zero_shot_r100_pinned.py:295:    if not 0.0 < threshold < 1.0:
scripts/evaluate_thebe_zero_shot_r100_pinned.py:296:        raise RuntimeError(f"Invalid frozen threshold: {threshold}")
scripts/evaluate_thebe_zero_shot_r100_pinned.py:305:    patch_size = volume_shape[0]
scripts/evaluate_thebe_zero_shot_r100_pinned.py:312:    if "model" not in checkpoint:
scripts/evaluate_thebe_zero_shot_r100_pinned.py:313:        raise RuntimeError("Checkpoint does not contain model weights")
scripts/evaluate_thebe_zero_shot_r100_pinned.py:321:    model = baseline.FaultSeg3D().to(device)
scripts/evaluate_thebe_zero_shot_r100_pinned.py:322:    model.load_state_dict(checkpoint["model"], strict=True)
scripts/evaluate_thebe_zero_shot_r100_pinned.py:323:    model.eval()
scripts/evaluate_thebe_zero_shot_r100_pinned.py:325:    for parameter in model.parameters():
scripts/evaluate_thebe_zero_shot_r100_pinned.py:329:    np.random.seed(42)
scripts/evaluate_thebe_zero_shot_r100_pinned.py:337:    x_starts = list(range(0, total_shape[0], patch_size))
scripts/evaluate_thebe_zero_shot_r100_pinned.py:338:    y_starts = list(range(0, total_shape[1], patch_size))
scripts/evaluate_thebe_zero_shot_r100_pinned.py:339:    z_starts = list(range(0, total_shape[2], patch_size))
scripts/evaluate_thebe_zero_shot_r100_pinned.py:358:        "checkpoint_epoch": int(checkpoint.get("epoch", -1)),
scripts/evaluate_thebe_zero_shot_r100_pinned.py:363:        "threshold": threshold,
scripts/evaluate_thebe_zero_shot_r100_pinned.py:374:        "normalization": (
scripts/evaluate_thebe_zero_shot_r100_pinned.py:375:            "independent z-score on each valid 3D patch, "
scripts/evaluate_thebe_zero_shot_r100_pinned.py:380:            "zero-pad normalized inputs to 128^3; "
scripts/faultseg3d_baseline.py:7:logits so the loss can use numerically stable BCEWithLogitsLoss.
scripts/faultseg3d_baseline.py:11:* b0_bce: official architecture with ordinary BCE (the active loss in the
scripts/faultseg3d_baseline.py:40:from torch.utils.data import DataLoader, Dataset
scripts/faultseg3d_baseline.py:48:def seed_everything(seed: int) -> None:
scripts/faultseg3d_baseline.py:49:    os.environ["PYTHONHASHSEED"] = str(seed)
scripts/faultseg3d_baseline.py:50:    random.seed(seed)
scripts/faultseg3d_baseline.py:51:    np.random.seed(seed)
scripts/faultseg3d_baseline.py:52:    torch.manual_seed(seed)
scripts/faultseg3d_baseline.py:54:        torch.cuda.manual_seed_all(seed)
scripts/faultseg3d_baseline.py:101:def count_parameters(model: nn.Module) -> int:
scripts/faultseg3d_baseline.py:102:    return sum(parameter.numel() for parameter in model.parameters() if parameter.requires_grad)
scripts/faultseg3d_baseline.py:116:class FaultSegDataset(Dataset[tuple[Tensor, Tensor, str]]):
scripts/faultseg3d_baseline.py:201:        raise ValueError(f"Unknown loss variant: {self.variant}")
scripts/faultseg3d_baseline.py:206:    threshold: float
scripts/faultseg3d_baseline.py:209:    precision: float
scripts/faultseg3d_baseline.py:261:    def metrics(self, threshold: float) -> Metrics:
scripts/faultseg3d_baseline.py:262:        threshold_bin = min(max(int(threshold * self.bins), 0), self.bins - 1)
scripts/faultseg3d_baseline.py:270:        precision = tp / (tp + fp + 1e-12)
scripts/faultseg3d_baseline.py:299:            threshold=float(threshold),
scripts/faultseg3d_baseline.py:302:            precision=float(precision),
scripts/faultseg3d_baseline.py:373:    excluded = {"volume_id", "threshold", "tp", "fp", "fn", "tn"}
scripts/faultseg3d_baseline.py:390:    dataset: FaultSegDataset,
scripts/faultseg3d_baseline.py:391:    batch_size: int,
scripts/faultseg3d_baseline.py:394:    seed: int,
scripts/prepare_seismic_datasets.py:35:            for piece in re.split(r"(\d+)", path.name)]
scripts/prepare_seismic_datasets.py:52:    for split in ("train", "validation"):
scripts/prepare_seismic_datasets.py:53:        seis_dir = data_root / "faultseg3d" / split / "seis"
scripts/prepare_seismic_datasets.py:54:        fault_dir = data_root / "faultseg3d" / split / "fault"
scripts/prepare_seismic_datasets.py:61:                f"{split}: unmatched pairs; missing fault={missing_fault}, "
scripts/prepare_seismic_datasets.py:85:                "split": split,
scripts/prepare_seismic_datasets.py:107:                print(f"{split}: audited {index}/{len(names)} pairs", flush=True)
scripts/prepare_seismic_datasets.py:199:        "Raw 0 = unknown/unannotated (ignore in loss)\n"
scripts/prepare_seismic_datasets.py:204:        "Derived valid PNG: 0=ignore, 255=include in loss\n",
scripts/prepare_seismic_datasets.py:269:    for split in splits:
scripts/prepare_seismic_datasets.py:270:        seismic_files = sorted((source_root / "seis").glob(patterns[split]), key=natural_key)
scripts/prepare_seismic_datasets.py:272:            raise RuntimeError(f"No Thebe files found for split {split}")
scripts/prepare_seismic_datasets.py:287:                            "split": split,
scripts/prepare_seismic_datasets.py:409:                        "split": split,
scripts/r100_full_run_ex.py:2:"""R100: FaultSeg3D from scratch on real Thebe, then held-out evaluation.
scripts/r100_full_run_ex.py:36:SEED = 42
scripts/r100_full_run_ex.py:37:EPOCHS = 100
scripts/r100_full_run_ex.py:40:LR = 1e-4
scripts/r100_full_run_ex.py:62:        raise RuntimeError("Baseline A patch size changed")
scripts/r100_full_run_ex.py:65:def split_paths(root: Path, split: str, count: int) -> list[Path]:
scripts/r100_full_run_ex.py:66:    paths = sorted(root.glob(f"{split}*.h5"), key=natural_key)
scripts/r100_full_run_ex.py:67:    expected = [root / f"{split}{number}.h5" for number in range(1, count + 1)]
scripts/r100_full_run_ex.py:87:        raise RuntimeError(f"Patch shape mismatch at {origin}")
scripts/r100_full_run_ex.py:105:        normalized = np.zeros_like(raw, dtype=np.float32)
scripts/r100_full_run_ex.py:106:        normalized[valid] = (raw[valid] - mean) / std
scripts/r100_full_run_ex.py:107:        seismic_padded[slices] = normalized
scripts/r100_full_run_ex.py:121:    model: torch.nn.Module,
scripts/r100_full_run_ex.py:125:    threshold: float = 0.5,
scripts/r100_full_run_ex.py:128:    model.eval()
scripts/r100_full_run_ex.py:146:            logits = model(x)
scripts/r100_full_run_ex.py:159:            predicted = (probability[0, 0][bounds] >= threshold).cpu().numpy()
scripts/r100_full_run_ex.py:170:                **asdict(patch_histogram.metrics(threshold)),
scripts/r100_full_run_ex.py:189:def save_checkpoint(path: Path, model, optimizer, epoch: int, validation: dict) -> None:
scripts/r100_full_run_ex.py:192:        "model": model.state_dict(), "optimizer": optimizer.state_dict(),
scripts/r100_full_run_ex.py:193:        "epoch": epoch, "validation_metrics": validation,
scripts/r100_full_run_ex.py:196:            "loss": "b0_bce_masked", "epochs": EPOCHS,
scripts/r100_full_run_ex.py:197:            "batch_size": 1, "gradient_accumulation": GRAD_ACCUMULATION,
scripts/r100_full_run_ex.py:198:            "learning_rate": LR, "seed": SEED, "histogram_bins": BINS,
scripts/r100_full_run.py:2:"""R100: FaultSeg3D from scratch on real Thebe, then held-out evaluation.
scripts/r100_full_run.py:36:SEED = 42
scripts/r100_full_run.py:37:EPOCHS = 100
scripts/r100_full_run.py:40:LR = 1e-4
scripts/r100_full_run.py:62:        raise RuntimeError("Baseline A patch size changed")
scripts/r100_full_run.py:65:def split_paths(root: Path, split: str, count: int) -> list[Path]:
scripts/r100_full_run.py:66:    paths = sorted(root.glob(f"{split}*.h5"), key=natural_key)
scripts/r100_full_run.py:67:    expected = [root / f"{split}{number}.h5" for number in range(1, count + 1)]
scripts/r100_full_run.py:87:        raise RuntimeError(f"Patch shape mismatch at {origin}")
scripts/r100_full_run.py:106:        normalized = np.zeros_like(raw, dtype=np.float32)
scripts/r100_full_run.py:112:            normalized[valid] = (raw[valid] - mean) / std
scripts/r100_full_run.py:113:        seismic_padded[slices] = normalized
scripts/r100_full_run.py:127:    model: torch.nn.Module,
scripts/r100_full_run.py:131:    threshold: float = 0.5,
scripts/r100_full_run.py:134:    model.eval()
scripts/r100_full_run.py:152:            logits = model(x)
scripts/r100_full_run.py:165:            predicted = (probability[0, 0][bounds] >= threshold).cpu().numpy()
scripts/r100_full_run.py:176:                **asdict(patch_histogram.metrics(threshold)),
scripts/r100_full_run.py:195:def save_checkpoint(path: Path, model, optimizer, scaler, rng, epoch: int, validation: dict) -> None:
scripts/r100_full_run.py:198:        "model": model.state_dict(), "optimizer": optimizer.state_dict(),
scripts/r100_full_run.py:199:        "epoch": epoch, "validation_metrics": validation,
scripts/r100_full_run.py:205:            "loss": "b0_bce_masked", "epochs": EPOCHS,
scripts/r100_full_run.py:206:            "batch_size": 1, "gradient_accumulation": GRAD_ACCUMULATION,
scripts/r100_full_run.py:207:            "learning_rate": LR, "seed": SEED, "histogram_bins": BINS,
scripts/run_r100_3seed_queue.py:2:"""Sequential R100 FP16 smoke followed by exactly three clean seeds.
scripts/run_r100_3seed_queue.py:41:def validate_run(run_dir, seed, smoke=False, expected_protocol=None):
scripts/run_r100_3seed_queue.py:42:    # CPU checkpoint inspection. Importing torch here does not create a CUDA model.
scripts/run_r100_3seed_queue.py:49:    epochs, patches, val_patches = (1, 18, 2) if smoke else (100, 360, 128)
scripts/run_r100_3seed_queue.py:50:    require(config["seed"] == seed and status["seed"] == seed, "Seed mismatch")
scripts/run_r100_3seed_queue.py:53:    require(config["epochs"] == epochs and status["epochs_completed"] == epochs, "Epoch budget mismatch")
scripts/run_r100_3seed_queue.py:54:    require(config["train_patches_per_epoch"] == patches, "Training patch budget mismatch")
scripts/run_r100_3seed_queue.py:55:    require(config["validation_patches_per_epoch"] == val_patches, "Validation patch budget mismatch")
scripts/run_r100_3seed_queue.py:56:    require(config["validation_seed"] == 1042, "Validation seed changed")
scripts/run_r100_3seed_queue.py:57:    require(config["model_parameters"] == 1459585, "Model parameter count changed")
scripts/run_r100_3seed_queue.py:59:        "model_class": "faultseg3d_baseline.FaultSeg3D", "patch_size": 128,
scripts/run_r100_3seed_queue.py:60:        "optimizer": "Adam", "learning_rate": 1e-4, "gradient_accumulation": 2,
scripts/run_r100_3seed_queue.py:61:        "loss": "ordinary BCE averaged over observed voxels",
scripts/run_r100_3seed_queue.py:64:    require(config["precision"] == status["precision"] == "float16_autocast", "Precision mismatch")
scripts/run_r100_3seed_queue.py:69:    protocol = {key: value for key, value in config.items() if key not in ("seed", "protocol_hash")}
scripts/run_r100_3seed_queue.py:74:    require(1 <= selection["best_epoch"] <= epochs, "Invalid best epoch")
scripts/run_r100_3seed_queue.py:75:    require(0 <= selection["threshold"] <= 1, "Invalid threshold")
scripts/run_r100_3seed_queue.py:79:    require([int(row["epoch"]) for row in history] == list(range(1, epochs + 1)), "History is incomplete or duplicated")
scripts/run_r100_3seed_queue.py:91:                for chunk in value.detach().reshape(-1).split(1_048_576):
scripts/run_r100_3seed_queue.py:104:    for filename, expected_epoch in (("last.pt", epochs), ("best.pt", selection["best_epoch"])):
scripts/run_r100_3seed_queue.py:106:        required = {"model", "optimizer", "scaler", "epoch", "args", "validation_metrics", "python_rng", "torch_rng", "cuda_rng"}
scripts/run_r100_3seed_queue.py:108:        require(checkpoint["epoch"] == expected_epoch, f"Checkpoint epoch mismatch: {filename}")
scripts/run_r100_3seed_queue.py:109:        require(checkpoint["args"]["seed"] == seed, "Checkpoint seed mismatch")
scripts/run_r100_3seed_queue.py:113:        require(checkpoint["optimizer"].get("state"), "Optimizer has no saved update state")
scripts/train_paper_attention3d_thebe_bf16.py:4:This is an adaptation of the published architecture and Unified Focal Loss.
scripts/train_paper_attention3d_thebe_bf16.py:5:It deliberately omits the paper's denoising pretraining and does not reproduce
scripts/train_paper_attention3d_thebe_bf16.py:29:from torch.utils.data import DataLoader, Dataset
scripts/train_paper_attention3d_thebe_bf16.py:32:PATCH = 64
scripts/train_paper_attention3d_thebe_bf16.py:33:THRESHOLD = 0.5
scripts/train_paper_attention3d_thebe_bf16.py:41:    # experiment uses its architecture/loss classes and its own training loop.
scripts/train_paper_attention3d_thebe_bf16.py:49:        raise RuntimeError(f"Cannot import the authors' model: {path}")
scripts/train_paper_attention3d_thebe_bf16.py:56:class ThebePatches(Dataset):
scripts/train_paper_attention3d_thebe_bf16.py:63:        seed: int,
scripts/train_paper_attention3d_thebe_bf16.py:72:        self.seed = seed
scripts/train_paper_attention3d_thebe_bf16.py:73:        self.epoch = 0
scripts/train_paper_attention3d_thebe_bf16.py:79:            if shape != tuple(handle["fault"].shape) or any(n < PATCH for n in shape):
scripts/train_paper_attention3d_thebe_bf16.py:91:        rng = np.random.default_rng(self.seed + self.epoch * 1_000_003 + index * 1009)
scripts/train_paper_attention3d_thebe_bf16.py:99:            start = tuple(int(rng.integers(0, n - PATCH + 1)) for n in shape)
scripts/train_paper_attention3d_thebe_bf16.py:100:            slices = tuple(slice(s, s + PATCH) for s in start)
scripts/train_paper_attention3d_thebe_bf16.py:124:            last = PATCH - 1 - nonzero[..., ::-1].argmax(axis=2)
scripts/train_paper_attention3d_thebe_bf16.py:125:            times = np.arange(PATCH)[None, None, :]
scripts/train_paper_attention3d_thebe_bf16.py:132:            normalized = np.zeros_like(seismic)
scripts/train_paper_attention3d_thebe_bf16.py:133:            normalized[valid] = (seismic[valid] - mean) / std
scripts/train_paper_attention3d_thebe_bf16.py:134:            if not np.isfinite(normalized).all():
scripts/train_paper_attention3d_thebe_bf16.py:135:                raise RuntimeError(f"Nonfinite normalized seismic in {self.paths[file_index]}")
scripts/train_paper_attention3d_thebe_bf16.py:137:                torch.from_numpy(np.ascontiguousarray(normalized[None])),
scripts/train_paper_attention3d_thebe_bf16.py:142:            f"Unable to sample {'fault' if want_fault else 'valid'} patch "
scripts/train_paper_attention3d_thebe_bf16.py:162:def require_finite(tensor: torch.Tensor, *, stage: str, epoch: int, patch: int) -> None:
scripts/train_paper_attention3d_thebe.py:4:This is an adaptation of the published architecture and Unified Focal Loss.
scripts/train_paper_attention3d_thebe.py:5:It deliberately omits the paper's denoising pretraining and does not reproduce
scripts/train_paper_attention3d_thebe.py:29:from torch.utils.data import DataLoader, Dataset
scripts/train_paper_attention3d_thebe.py:32:PATCH = 64
scripts/train_paper_attention3d_thebe.py:33:THRESHOLD = 0.5
scripts/train_paper_attention3d_thebe.py:40:    # experiment uses its architecture/loss classes and its own training loop.
scripts/train_paper_attention3d_thebe.py:48:        raise RuntimeError(f"Cannot import the authors' model: {path}")
scripts/train_paper_attention3d_thebe.py:55:class ThebePatches(Dataset):
scripts/train_paper_attention3d_thebe.py:62:        seed: int,
scripts/train_paper_attention3d_thebe.py:71:        self.seed = seed
scripts/train_paper_attention3d_thebe.py:72:        self.epoch = 0
scripts/train_paper_attention3d_thebe.py:78:            if shape != tuple(handle["fault"].shape) or any(n < PATCH for n in shape):
scripts/train_paper_attention3d_thebe.py:90:        rng = np.random.default_rng(self.seed + self.epoch * 1_000_003 + index * 1009)
scripts/train_paper_attention3d_thebe.py:98:            start = tuple(int(rng.integers(0, n - PATCH + 1)) for n in shape)
scripts/train_paper_attention3d_thebe.py:99:            slices = tuple(slice(s, s + PATCH) for s in start)
scripts/train_paper_attention3d_thebe.py:117:            last = PATCH - 1 - nonzero[..., ::-1].argmax(axis=2)
scripts/train_paper_attention3d_thebe.py:118:            times = np.arange(PATCH)[None, None, :]
scripts/train_paper_attention3d_thebe.py:125:            normalized = np.zeros_like(seismic)
scripts/train_paper_attention3d_thebe.py:126:            normalized[valid] = (seismic[valid] - mean) / std
scripts/train_paper_attention3d_thebe.py:128:                torch.from_numpy(np.ascontiguousarray(normalized[None])),
scripts/train_paper_attention3d_thebe.py:133:            f"Unable to sample {'fault' if want_fault else 'valid'} patch "
scripts/train_paper_attention3d_thebe.py:158:    parser.add_argument("--epochs", type=int, default=100)
scripts/train_paper_attention3d_thebe.py:163:    parser.add_argument("--seed", type=int, default=42)
scripts/train_paper_attention3d_thebe.py:168:    if min(args.epochs, args.train_patches, args.val_patches, args.accumulate, args.patience) <= 0:
scripts/train_r100_fp16_clean.py:2:"""R100 FP16 clean-seed training and validation; test files are never opened.
scripts/train_r100_fp16_clean.py:4:Derived from the R100 trainer supplied on 2026-10-14. It retains the model,
scripts/train_r100_fp16_clean.py:5:masked BCE, sampler, normalization, patch size, optimizer and training budget.
scripts/train_r100_fp16_clean.py:6:The changes are explicit seed control, a common validation subset,
scripts/train_r100_fp16_clean.py:40:SEED = 42
scripts/train_r100_fp16_clean.py:41:EPOCHS = 100
scripts/train_r100_fp16_clean.py:44:LR = 1e-4
scripts/train_r100_fp16_clean.py:61:            for chunk in value.detach().reshape(-1).split(1_048_576):
scripts/train_r100_fp16_clean.py:77:        raise ValueError("Invalid validation patch count")
scripts/train_r100_fp16_clean.py:98:        model = baseline.FaultSeg3D()
scripts/train_r100_fp16_clean.py:99:        count = baseline.count_parameters(model)
scripts/train_r100_fp16_clean.py:104:            "status": "cpu_preflight_pass", "model": "faultseg3d_baseline.FaultSeg3D",
scripts/train_r100_fp16_clean.py:128:        raise RuntimeError("Baseline A patch size changed")
scripts/train_r100_fp16_clean.py:131:def split_paths(root: Path, split: str, count: int) -> list[Path]:
scripts/train_r100_fp16_clean.py:132:    paths = sorted(root.glob(f"{split}*.h5"), key=natural_key)
scripts/train_r100_fp16_clean.py:133:    expected = [root / f"{split}{number}.h5" for number in range(1, count + 1)]
scripts/train_r100_fp16_clean.py:153:        raise RuntimeError(f"Patch shape mismatch at {origin}")
scripts/train_r100_fp16_clean.py:172:        normalized = np.zeros_like(raw, dtype=np.float32)
scripts/train_r100_fp16_clean.py:178:            normalized[valid] = (raw[valid] - mean) / std
scripts/train_r100_fp16_clean.py:179:        seismic_padded[slices] = normalized
scripts/train_r100_fp16_clean.py:193:    model: torch.nn.Module,
scripts/train_r100_fp16_clean.py:197:    threshold: float = 0.5,
scripts/train_r100_fp16_clean.py:200:    model.eval()
scripts/train_r100_fp16_clean.py:218:            logits = model(x)
scripts/train_sammed3d_thebe.py:12:The Thebe reader, normalization, split, patch sampling, masked metric code,
scripts/train_sammed3d_thebe.py:71:LEARNING_RATE = 1e-4
scripts/train_sammed3d_thebe.py:146:                "Checkpoint/model mismatch. "
scripts/train_sammed3d_thebe.py:173:        batch = seismic.shape[0]
scripts/train_sammed3d_thebe.py:174:        if batch != 1:
scripts/train_sammed3d_thebe.py:175:            sparse = sparse.expand(batch, -1, -1)
scripts/train_sammed3d_thebe.py:176:            dense = dense.expand(batch, -1, -1, -1, -1)
scripts/train_sammed3d_thebe.py:212:def parameter_counts(model: nn.Module) -> tuple[int, int]:
scripts/train_sammed3d_thebe.py:213:    total = sum(parameter.numel() for parameter in model.parameters())
scripts/train_sammed3d_thebe.py:214:    trainable = sum(parameter.numel() for parameter in model.parameters() if parameter.requires_grad)
scripts/train_sammed3d_thebe.py:232:def trainable_finite(model: PromptFreeSAMMed3D) -> None:
scripts/train_sammed3d_thebe.py:233:    r100.assert_finite_tree(model.trainable_state_dict(), "trainable_model")
scripts/train_sammed3d_thebe.py:238:    model: PromptFreeSAMMed3D,
scripts/train_sammed3d_thebe.py:239:    optimizer,
scripts/train_sammed3d_thebe.py:242:    epoch: int,
scripts/train_sammed3d_thebe.py:245:    trainable_finite(model)
scripts/train_sammed3d_thebe.py:246:    r100.assert_finite_tree(optimizer.state_dict(), "optimizer")
scripts/train_sammed3d_thebe.py:251:            "epoch": epoch,
scripts/train_sammed3d_thebe.py:252:            "trainable_model": model.trainable_state_dict(),
scripts/train_sammed3d_thebe.py:253:            "optimizer": optimizer.state_dict(),
scripts/train_sammed3d_thebe.py:273:        model = PromptFreeSAMMed3D(checkpoint)
scripts/train_sammed3d_thebe.py:274:        total, trainable = parameter_counts(model)
scripts/train_sammed3d_thebe.py:277:            name for name, parameter in model.named_parameters() if parameter.requires_grad
scripts/train_sammed3d_thebe.py:283:            "model": "SAM-Med3D-turbo vit_b_ori, prompt-free",
```

### Results and completion

```text
reports/2026-10-02_baseline_A_report.md:19:| Internal validation | 20 | Used to monitor training, select the best checkpoint, and choose the probability threshold |
reports/2026-10-02_baseline_A_report.md:56:| Mixed precision | Enabled |
reports/2026-10-02_baseline_A_report.md:66:The best checkpoint was selected using internal-validation Dice at a threshold of `0.5`.
reports/2026-10-02_baseline_A_report.md:74:PR-AUC and ROC-AUC were approximated using streaming histograms with 2,048 bins.
reports/2026-10-02_baseline_A_report.md:82:| Dice / F1 | 0.8168 | **0.8211** |
reports/2026-10-02_baseline_A_report.md:83:| Foreground IoU | 0.6904 | **0.6964** |
reports/2026-10-02_baseline_A_report.md:84:| Precision | 0.7992 | **0.8030** |
reports/2026-10-02_baseline_A_report.md:85:| Recall | 0.8353 | **0.8399** |
reports/2026-10-02_baseline_A_report.md:90:| ROC-AUC | 0.9825 | **0.9852** |
reports/2026-10-02_baseline_A_report.md:95:Dice, IoU, PR-AUC, precision, recall, and MCC provide more meaningful measures of fault-segmentation performance.
reports/2026-10-02_baseline_A_report.md:106:Recall was higher than precision, meaning the model detected most fault voxels while producing slightly more false-positive than false-negative errors.
reports/2026-10-02_baseline_A_report.md:112:| Dice | 0.8237 | 0.0423 | 0.8203 | 0.7186 | 0.8970 |
reports/2026-10-02_baseline_A_report.md:113:| IoU | 0.7025 | 0.0607 | 0.6953 | 0.5609 | 0.8132 |
reports/2026-10-02_baseline_A_report.md:114:| Precision | 0.8056 | 0.0412 | 0.8117 | 0.7119 | 0.8781 |
reports/2026-10-02_baseline_A_report.md:115:| Recall | 0.8429 | 0.0457 | 0.8374 | 0.7255 | 0.9167 |
reports/2026-10-02_baseline_A_report.md:118:| ROC-AUC | 0.9852 | 0.0083 | 0.9839 | 0.9686 | 0.9976 |
reports/2026-10-02_baseline_A_report.md:121:The aggregate Dice and mean per-volume Dice differ slightly because the aggregate result pools all voxels, while the per-volume mean gives every volume equal weight.
reports/2026-10-02_baseline_A_report.md:147:## 11. Training behaviour
reports/2026-10-02_baseline_A_report.md:149:The final five epochs produced validation Dice values between approximately 0.807 and 0.816 at the fixed threshold of `0.5`.
reports/2026-10-02_baseline_A_report.md:151:Epoch 100 achieved the best checkpoint-selection Dice. This indicates that the model was still competitive at the end of training, although the final epochs showed normal validation fluctuation.
reports/2026-10-02_baseline_A_report.md:159:The held-out test Dice of 0.8211 and IoU of 0.6964 establish a strong reference result. Test performance was slightly higher than internal-validation performance, so the validation-to-test comparison does not show evidence of overfitting.
reports/2026-10-02_baseline_A_report.md:161:The model achieved recall of 0.8399 and precision of 0.8030. It therefore detected a large proportion of labelled fault voxels, with some remaining false-positive predictions.
reports/2026-10-02_baseline_A_report.md:165:Performance still varied between individual test volumes. The worst test-volume Dice was 0.7186, compared with a maximum of 0.8970. Future work should inspect these weaker cases visually.
reports/2026-10-02_baseline_A_report.md:181:The next experiment is **Loss Ablation L1: weighted BCE plus Dice loss**.
reports/2026-10-02_baseline_A_report.md:199:`0.5 × weighted BCE + 0.5 × soft Dice loss`
reports/attention3d_identity_audit_20261014.txt:31:./reports/EXPERIMENT_NAMING.md:26:- Loss Ablation L1 run: `runs/loss_ablation_L1_weighted_bce_dice_seed42`
reports/attention3d_identity_audit_20261014.txt:32:./reports/EXPERIMENT_NAMING.md:27:- Loss Ablation L1 log: `reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log`
reports/attention3d_identity_audit_20261014.txt:56:./reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:67:    train,100x3174x1537,float64,bool,float32,uint8,-2.6587982177734375,2.834458351135254,-2.925060121001068e-06,0.11106203265206424,3570872,487843800,0.7319703560852879,66027b1f4df037aa0c3dae4a08ff42d11872068d6a9ddc479fd820d62c39ee3e,94d8fe88e7e8ead7d6399cfa2c9bfd256b75f1851a8c242a0180247969d9b7ac,data/thebe/seis/seistrain5.npz,data/thebe/fault/faulttrain5.npz,data/processed/thebe_h5/train5.h5,844142314
reports/attention3d_identity_audit_20261014.txt:57:./reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:68:    train,100x3174x1537,float64,bool,float32,uint8,-2.676699638366699,9.433253288269043,5.592769920060861e-06,0.11655410640016116,3909866,487843800,0.8014585816197726,7580b1a3ba71b9abc1f63f54acf1d2b6c407a9b003d0180886446aa01560529f,71b418f08d9ed0d0a346496e07e82cae9967f5e588f2c825e05eb88bd17a8631,data/thebe/seis/seistrain6.npz,data/thebe/fault/faulttrain6.npz,data/processed/thebe_h5/train6.h5,877969475
reports/attention3d_identity_audit_20261014.txt:58:./reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:69:    train,100x3174x1537,float64,bool,float32,uint8,-2.7207870483398438,2.8281021118164062,1.1942063768727192e-05,0.12574849960104517,6197892,487843800,1.2704664894788045,a8e2deff21c5a1e2fb45a758b466bfb46f30762153d96fd340055a6c37f816d6,1621e3db04c5ea33dc96a87e3f54cf1d5031341f7080fa85c7353d52eab21cc9,data/thebe/seis/seistrain7.npz,data/thebe/fault/faulttrain7.npz,data/processed/thebe_h5/train7.h5,1032693045
reports/attention3d_identity_audit_20261014.txt:61:./reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:72:    val,100x3174x1537,float64,bool,float32,uint8,-3.718324661254883,3.5749521255493164,-8.142081609447118e-06,0.13305340028663978,7906942,487843800,1.620793786863746,f6cca2e72c86d89e2c05feb92a1604a96d22a3557c25249f1cb2244e95205437,88341218e0d5e63b9092985d6c31612d6d64144d676babf8db194342d59c2bfb,data/thebe/seis/seisval1.npz,data/thebe/fault/faultval1.npz,data/processed/thebe_h5/val1.h5,1116731622
reports/attention3d_identity_audit_20261014.txt:207:./reports/evaluation/r100_readiness_20261005_101611/audit.txt:87:runs/loss_ablation_L1_weighted_bce_dice_seed42
reports/attention3d_identity_audit_20261014.txt:273: 1695  for f in   reports/training/paper_attention3d_thebe_supervised_seed42_resume.log   reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log; do     echo;     echo "============================================================";     echo "LOG: $f";     stat -c 'modified=%y  bytes=%s' "$f";      echo "--- START ---";     sed -n '1,12p' "$f";      echo "--- LAST 5 COMPLETED EPOCHS ---";     rg '^EPOCH ' "$f" | tail -5;      echo "--- COMPLETION, FAILURE, OR NaN MARKERS ---";     rg -ni       'training complete|completed|finished|done|traceback|killed|terminated|out of memory|cuda error|exception|nan'       "$f" | tail -30 || true;      echo "--- FINAL 25 RAW LINES ---";     tail -25 "$f"; done
reports/attention3d_identity_audit_20261014.txt:276: 1705      "runs/paper_attention3d_thebe_supervised_seed42_bf16_clean/last.pt",
reports/attention3d_identity_audit_20261014.txt:277: 1706      "runs/paper_attention3d_thebe_supervised_seed42_bf16_clean/best.pt",
reports/attention3d_identity_audit_20261014.txt:278: 1744  history | rg -i 'nohup.*paper_attention3d|paper_attention3d.*(resume|bf16|clean)' | tail -30
reports/attention3d_identity_audit_20261014.txt:283: 1751  old2_run="runs/paper_attention3d_thebe_supervised_seed42_bf16_clean"
reports/attention3d_identity_audit_20261014.txt:284: 1752  old2_log="reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log"
reports/attention3d_identity_audit_20261014.txt:285: 1753  new2_run="runs/paper_attention3d_thebe_supervised_seed42_bf16_clean_stopped_during_ep066"
reports/attention3d_identity_audit_20261014.txt:286: 1754  new2_log="reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean_stopped_during_ep066.log"
reports/attention3d_identity_audit_20261014.txt:292: 1769  src2_run="runs/paper_attention3d_thebe_supervised_seed42_bf16_clean_stopped_during_ep066"
reports/attention3d_identity_audit_20261014.txt:293: 1770  src2_log="reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean_stopped_during_ep066.log"
reports/attention3d_identity_audit_20261014.txt:294: 1771  dst2_run="runs/paper_attention3d_thebe_supervised_seed42_bf16_clean"
reports/attention3d_identity_audit_20261014.txt:295: 1772  dst2_log="reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log"
reports/attention3d_identity_audit_20261014.txt:300: 1786  src2_run="runs/paper_attention3d_thebe_supervised_seed42_bf16_clean_stopped_during_ep066"
reports/attention3d_identity_audit_20261014.txt:301: 1787  src2_log="reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean_stopped_during_ep066.log"
reports/attention3d_identity_audit_20261014.txt:302: 1788  dst2_run="runs/paper_attention3d_thebe_supervised_seed42_bf16_clean"
reports/attention3d_identity_audit_20261014.txt:303: 1789  dst2_log="reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log"
reports/attention3d_identity_audit_20261014.txt:304: 1793  {     echo "=== REPOSITORY ===";     date -Is;     pwd;     git status --short;     git log -15 --date=iso --pretty='format:%h %ad %s';      echo;     echo "=== RELEVANT DOCUMENTATION ===";     rg -n -i 'attention3d|bf16|r100|thebe|seed42|roadmap'       --glob '*.md' --glob '*.txt'       --glob '!reports/training/**'       --glob '!runs/**' . || true;      echo;     echo "=== RELEVANT LAUNCH HISTORY ===";     history | rg -i       'paper_attention3d|bf16_clean|train_paper_attention3d_thebe|R100_thebe' || true;     rg -n -i       'paper_attention3d|bf16_clean|train_paper_attention3d_thebe|R100_thebe'       ~/.bash_history 2>/dev/null || true;      echo;     echo "=== TRAINING SCRIPT METADATA ===";     stat scripts/train_paper_attention3d_thebe.py;     sha256sum scripts/train_paper_attention3d_thebe.py;     rg -n -i       'bf16|bfloat|autocast|scaler|resume|sampler|balance|fault.patch|seed|run.dir|learning.rate'       scripts/train_paper_attention3d_thebe.py || true;      echo;     echo "=== UNCOMMITTED SCRIPT CHANGES ===";     git diff -- scripts/train_paper_attention3d_thebe.py;      echo;     echo "=== SCRIPT HISTORY ===";     git log -10 --date=iso --stat -- scripts/train_paper_attention3d_thebe.py;      echo;     echo "=== FILES MODIFIED ON OCTOBER 12 ===";     find scripts configs -type f       -newermt '2026-10-12 00:00:00'       ! -newermt '2026-10-13 00:00:00'       -printf '%TY-%Tm-%Td %TH:%TM:%TS %p\n' 2>/dev/null |       sort;      echo;     echo "=== RUN AND LOG FILES ===";     find runs reports/training -maxdepth 2       -name 'paper_attention3d_thebe_supervised_seed42*'       -printf '%TY-%Tm-%Td %TH:%TM:%TS %s %p\n' |       sort;      echo;     echo "=== TERMINATION EVIDENCE ===";     journalctl --since '2026-10-12 12:10:00'       --until '2026-10-12 12:40:00' --no-pager 2>/dev/null |       rg -i 'oom|killed process|python|nvidia|cuda|segfault' || true;      journalctl --since '2026-10-12 23:30:00'       --until '2026-10-13 00:00:00' --no-pager 2>/dev/null |       rg -i 'oom|killed process|python|nvidia|cuda|segfault' || true; } > "$audit" 2>&1
reports/attention3d_identity_audit_20261014.txt:325:1896:for f in   reports/training/paper_attention3d_thebe_supervised_seed42_resume.log   reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log; do     echo;     echo "============================================================";     echo "LOG: $f";     stat -c 'modified=%y  bytes=%s' "$f";      echo "--- START ---";     sed -n '1,12p' "$f";      echo "--- LAST 5 COMPLETED EPOCHS ---";     rg '^EPOCH ' "$f" | tail -5;      echo "--- COMPLETION, FAILURE, OR NaN MARKERS ---";     rg -ni       'training complete|completed|finished|done|traceback|killed|terminated|out of memory|cuda error|exception|nan'       "$f" | tail -30 || true;      echo "--- FINAL 25 RAW LINES ---";     tail -25 "$f"; done
reports/attention3d_identity_audit_20261014.txt:328:1907:    "runs/paper_attention3d_thebe_supervised_seed42_bf16_clean/last.pt",
reports/attention3d_identity_audit_20261014.txt:329:1908:    "runs/paper_attention3d_thebe_supervised_seed42_bf16_clean/best.pt",
reports/attention3d_identity_audit_20261014.txt:330:1954:history | rg -i 'nohup.*paper_attention3d|paper_attention3d.*(resume|bf16|clean)' | tail -30
reports/attention3d_identity_audit_20261014.txt:335:1961:old2_run="runs/paper_attention3d_thebe_supervised_seed42_bf16_clean"
reports/attention3d_identity_audit_20261014.txt:336:1962:old2_log="reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log"
reports/attention3d_identity_audit_20261014.txt:337:1963:new2_run="runs/paper_attention3d_thebe_supervised_seed42_bf16_clean_stopped_during_ep066"
reports/attention3d_identity_audit_20261014.txt:338:1964:new2_log="reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean_stopped_during_ep066.log"
reports/attention3d_identity_audit_20261014.txt:344:1979:src2_run="runs/paper_attention3d_thebe_supervised_seed42_bf16_clean_stopped_during_ep066"
reports/attention3d_identity_audit_20261014.txt:345:1980:src2_log="reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean_stopped_during_ep066.log"
reports/attention3d_identity_audit_20261014.txt:346:1981:dst2_run="runs/paper_attention3d_thebe_supervised_seed42_bf16_clean"
reports/attention3d_identity_audit_20261014.txt:347:1982:dst2_log="reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log"
reports/attention3d_identity_audit_20261014.txt:352:1996:src2_run="runs/paper_attention3d_thebe_supervised_seed42_bf16_clean_stopped_during_ep066"
reports/attention3d_identity_audit_20261014.txt:353:1997:src2_log="reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean_stopped_during_ep066.log"
reports/attention3d_identity_audit_20261014.txt:354:1998:dst2_run="runs/paper_attention3d_thebe_supervised_seed42_bf16_clean"
reports/attention3d_identity_audit_20261014.txt:355:1999:dst2_log="reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log"
reports/attention3d_identity_audit_20261014.txt:390:247:        scaler.load_state_dict(previous["scaler"])
reports/attention3d_identity_audit_20261014.txt:391:254:        print(f"RESUME epoch={start_epoch + 1} best_val_dice={best_dice:.6f}", flush=True)
reports/attention3d_identity_audit_20261014.txt:401:351:        "epochs_completed": len(history), "best_checkpoint": str(run_dir / "best.pt"),
reports/attention3d_identity_audit_20261014.txt:542:2026-10-12 14:23:56.8256477150 scripts/train_paper_attention3d_thebe_bf16.py
reports/attention3d_identity_audit_20261014.txt:543:2026-10-12 14:23:56.8586751510 scripts/__pycache__/train_paper_attention3d_thebe_bf16.cpython-313.pyc
reports/attention3d_identity_audit_20261014.txt:549:2026-10-12 14:24:27.2352222680 8 reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.pid
reports/attention3d_identity_audit_20261014.txt:550:2026-10-12 23:44:31.1072060830 4096 runs/paper_attention3d_thebe_supervised_seed42_bf16_clean
reports/attention3d_identity_audit_20261014.txt:551:2026-10-12 23:46:22.3081748470 20708 reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log
reports/attention3d_identity_audit_20261014.txt:565: 'val_loss': 0.4318309361115098,
reports/attention3d_identity_audit_20261014.txt:566: 'val_dice': 0.5390039878151507,
reports/data_audit/faultseg3d_volume_statistics.csv:3:train,1,128x128x128,float32,float32,8388608,8388608,-5.1317243576049805,5.1584086418151855,0.0009396517522350933,1.044352061053755,147227,2097152,7.020330429077148,0.0;1.0,True,1a1907f4b430b8c35f8c8f314d1d6cf16a6c04d6c451a7e39b15dab73722a807,f55dc376ccecb0ed1d49f1b99af9880a5e0e0df543882682051aeafc508a1d41,data/faultseg3d/train/seis/1.dat,data/faultseg3d/train/fault/1.dat
reports/data_audit/faultseg3d_volume_statistics.csv:7:train,5,128x128x128,float32,float32,8388608,8388608,-4.582903861999512,4.566244602203369,0.0008078546927150453,1.0041724713530038,138923,2097152,6.624364852905273,0.0;1.0,True,7495049e8cfdc99a43befcf79941c5344681a0076098084165678ecd7a7bbe77,b34e5b0051d0ff26294dd04d4da22bc47299e84852bc04841c03fe239f15495a,data/faultseg3d/train/seis/5.dat,data/faultseg3d/train/fault/5.dat
reports/data_audit/faultseg3d_volume_statistics.csv:11:train,9,128x128x128,float32,float32,8388608,8388608,-5.502901077270508,5.401592254638672,-0.0009981476334712663,1.1661521474381504,132708,2097152,6.328010559082031,0.0;1.0,True,a7bdcd60cc0d6cbf8d34b0f8d850271dff1df6309bebe91e92002ccffbe243cb,3f2adc0204319d18cc5cccbec736d2b0371a0e2baad85672aba910c92109273e,data/faultseg3d/train/seis/9.dat,data/faultseg3d/train/fault/9.dat
reports/data_audit/faultseg3d_volume_statistics.csv:14:train,12,128x128x128,float32,float32,8388608,8388608,-4.637589931488037,4.71632719039917,0.0003486026545279075,1.0447240732648932,161837,2097152,7.716989517211914,0.0;1.0,True,84564147b95fc52f7ddd279cef8ec92ac603ced892670a4fa3c79bbddc77b65e,a546367a30df1cea7124c9f6c2749c6e1cb1a63a55ce074c837aaef44b80460f,data/faultseg3d/train/seis/12.dat,data/faultseg3d/train/fault/12.dat
reports/data_audit/faultseg3d_volume_statistics.csv:17:train,15,128x128x128,float32,float32,8388608,8388608,-6.055706977844238,6.720053672790527,0.00010231776393540559,1.1155178035316708,157185,2097152,7.49516487121582,0.0;1.0,True,351a5535128f38e4d95c4156bc1e5710d6afbd467de7af1f691f4e9316bfaaf5,710fb395f5f8cc8aa1ae4d5d98e25a722073e815f808e0ae656c17a5f352b47d,data/faultseg3d/train/seis/15.dat,data/faultseg3d/train/fault/15.dat
reports/data_audit/faultseg3d_volume_statistics.csv:19:train,17,128x128x128,float32,float32,8388608,8388608,-4.760252475738525,4.94697380065918,0.0005586663821877114,1.0047012214287332,145212,2097152,6.924247741699219,0.0;1.0,True,85f01509c99cd7ba9647854a641ba8cb1f65867898d70a634a132f4b9f12ee4e,ec5d65b9ca43728ed36b2ba6db399eac3ae7f87b61735901ca302a8ef40c9281,data/faultseg3d/train/seis/17.dat,data/faultseg3d/train/fault/17.dat
reports/data_audit/faultseg3d_volume_statistics.csv:21:train,19,128x128x128,float32,float32,8388608,8388608,-5.375992298126221,5.685787677764893,-0.0005301139407900973,1.116404866462242,166057,2097152,7.918214797973633,0.0;1.0,True,c45db0b9ed154d6c8a8a6335690ae9c45b2ccd13e6e8076fc044f4208c28901e,627855aa7b3a5a58e2c806e2694a6b6f129925246eadc3102d5307f4e2ed9af9,data/faultseg3d/train/seis/19.dat,data/faultseg3d/train/fault/19.dat
reports/data_audit/faultseg3d_volume_statistics.csv:25:train,23,128x128x128,float32,float32,8388608,8388608,-4.923968315124512,4.2370452880859375,0.0005525728663081978,0.9999998652933547,125603,2097152,5.989217758178711,0.0;1.0,True,02b308f9e129aa28892aa06780af76f1d5f3a891432729ce66ba9e9fa4e50732,3a30291ff0199ec586c6b1b4d5886d9d075fa8e34d5dd5cfde2c18b5062f0eb4,data/faultseg3d/train/seis/23.dat,data/faultseg3d/train/fault/23.dat
reports/data_audit/faultseg3d_volume_statistics.csv:26:train,24,128x128x128,float32,float32,8388608,8388608,-4.258067607879639,4.113528251647949,0.004576388556558697,0.999989535199128,89501,2097152,4.267740249633789,0.0;1.0,True,8eb7c74de60065ec7b94468df10cf6f5e82a6c8e8e72ed392d8f1bf8fb7c2c21,f6321cfffc854c38c936cef9dadcc23d4cca275303b5fed3582c586b38fccced,data/faultseg3d/train/seis/24.dat,data/faultseg3d/train/fault/24.dat
reports/data_audit/faultseg3d_volume_statistics.csv:27:train,25,128x128x128,float32,float32,8388608,8388608,-4.495860576629639,4.59214973449707,-0.0020706275547009018,1.0050262918290698,157620,2097152,7.515907287597656,0.0;1.0,True,d2fc6a30e344f25edd98bd1a79e0db56e1c599465fa8301354dedba4fb7ca0aa,9a1a72db1b7084fa090292cd5c0f13b7c410a04fe603e5f185d2a78cf1edfe8f,data/faultseg3d/train/seis/25.dat,data/faultseg3d/train/fault/25.dat
reports/data_audit/faultseg3d_volume_statistics.csv:28:train,26,128x128x128,float32,float32,8388608,8388608,-6.6962690353393555,6.137424945831299,-0.0020873836011575803,1.167079217900215,99757,2097152,4.756784439086914,0.0;1.0,True,3e015c31f16af2b9ad19c500d230efc3752fd1e70e44e89d140c1daee0514d43,0c37cc32c216c9d19b335bd46707242007a890beb107bbd4f072437ce3f90b77,data/faultseg3d/train/seis/26.dat,data/faultseg3d/train/fault/26.dat
reports/data_audit/faultseg3d_volume_statistics.csv:29:train,27,128x128x128,float32,float32,8388608,8388608,-5.017765998840332,5.285662651062012,-0.0009840911593254065,1.1664250292856115,137951,2097152,6.57801628112793,0.0;1.0,True,4a7d351e9f18aa447f9ec6fb840c314d6b079ddf3dcace9e1ad6496205c333d0,5246187b0efb4c009ddd3d2234ebfbe6b65239c9bee43ad5ff11f7d91ef1549c,data/faultseg3d/train/seis/27.dat,data/faultseg3d/train/fault/27.dat
reports/data_audit/faultseg3d_volume_statistics.csv:31:train,29,128x128x128,float32,float32,8388608,8388608,-5.924729347229004,5.177766799926758,-0.002231002152710368,1.076074183465718,152566,2097152,7.274913787841797,0.0;1.0,True,a263c55fcef1b8cd2de02552c9a2ff0ca01a5cb334cea023b37607e15b7b309c,97290677ff97b04187ca4d744233e772952410b4c1adb987eda4dc50574e8f69,data/faultseg3d/train/seis/29.dat,data/faultseg3d/train/fault/29.dat
reports/data_audit/faultseg3d_volume_statistics.csv:36:train,34,128x128x128,float32,float32,8388608,8388608,-6.915876388549805,6.470385551452637,0.0066059749067843565,1.1639137046657988,157472,2097152,7.50885009765625,0.0;1.0,True,56750e8e76f01d6fbf77654857c48ff56589326928210c0b4d662a156f05ee68,977893321bd1596c23e163638cc8e665222d1e81038da9b535499a643f1eb3f4,data/faultseg3d/train/seis/34.dat,data/faultseg3d/train/fault/34.dat
reports/data_audit/faultseg3d_volume_statistics.csv:39:train,37,128x128x128,float32,float32,8388608,8388608,-5.275990962982178,6.128777503967285,0.002214023411515484,1.076190146109364,111679,2097152,5.32526969909668,0.0;1.0,True,5500a764da35c4336d6c4f1375601feaea1742de3245e3cfe05309423d78f619,05b9a64729ce5daa65f033f7d46923c0fe59e2428cb96cb90c2fd15e2277943a,data/faultseg3d/train/seis/37.dat,data/faultseg3d/train/fault/37.dat
reports/data_audit/faultseg3d_volume_statistics.csv:40:train,38,128x128x128,float32,float32,8388608,8388608,-6.162123680114746,5.910310745239258,0.0008928351974271664,1.0433696985537537,155671,2097152,7.422971725463867,0.0;1.0,True,f4e5eb577c6568792b1aae57bf822a1467a4b1856a501dfade902ab53c3f0016,e06a44e6a0dc520c90488a9f11454de283c23e90b52649268545bc15773ae662,data/faultseg3d/train/seis/38.dat,data/faultseg3d/train/fault/38.dat
reports/data_audit/faultseg3d_volume_statistics.csv:41:train,39,128x128x128,float32,float32,8388608,8388608,-4.587521076202393,5.076230049133301,0.0014263621369509163,1.018867580038951,156660,2097152,7.470130920410156,0.0;1.0,True,fda0f40ebcd74b737eed11ae14eaf614a5f67436c3c6a6375915a9705e18b4a1,e0ce80bd03f61ce0db8a8d6a7b9e820cb219f1e1740de39fb3c0d248d0ddf226,data/faultseg3d/train/seis/39.dat,data/faultseg3d/train/fault/39.dat
reports/data_audit/faultseg3d_volume_statistics.csv:43:train,41,128x128x128,float32,float32,8388608,8388608,-6.253270149230957,5.291540145874023,0.00032124126143112663,1.1175617508304594,152806,2097152,7.286357879638672,0.0;1.0,True,972e91e7b621a1272a4d5fc317a00dfae196385aee5dfa56090d743a98ea91e6,f1d40ea896cbecc93f0d788dde171b182f8377f9f7937aa1b769b945888e2242,data/faultseg3d/train/seis/41.dat,data/faultseg3d/train/fault/41.dat
reports/data_audit/faultseg3d_volume_statistics.csv:44:train,42,128x128x128,float32,float32,8388608,8388608,-4.819056034088135,5.334750175476074,0.0005094818787677313,1.078089600127912,115289,2097152,5.497407913208008,0.0;1.0,True,9267274ec392efb6cddb2ce529b20bf30ea5e6e1397a4ac4462a3d5b5c6da9f4,3492bc830a74acd1fbca197a72e8dbf11a6be55b0413409b06525eb01bab043e,data/faultseg3d/train/seis/42.dat,data/faultseg3d/train/fault/42.dat
reports/data_audit/faultseg3d_volume_statistics.csv:45:train,43,128x128x128,float32,float32,8388608,8388608,-4.755434989929199,5.7546234130859375,-0.0007253322034047049,1.0440733462456153,136959,2097152,6.53071403503418,0.0;1.0,True,8dcbd4ce16a733f9634d2d52edb4efd9fa89cb77005140b8ff3ad482ddbad57c,6932551ca6e9f95d0e820b643ecf4f437f93adcc2ead1ed907f72392bb31af19,data/faultseg3d/train/seis/43.dat,data/faultseg3d/train/fault/43.dat
reports/data_audit/faultseg3d_volume_statistics.csv:48:train,46,128x128x128,float32,float32,8388608,8388608,-4.455245018005371,4.589926242828369,0.00343472081198491,0.9999940531111227,139420,2097152,6.648063659667969,0.0;1.0,True,5764869695c5600a2a93dbb9e6a80cc8d880d2a6dc10e6b989f083138baa017e,d317b79e7ba6195de195149f1bbe25f2793ca98c3ce278b6d20a8afdd20c8d9e,data/faultseg3d/train/seis/46.dat,data/faultseg3d/train/fault/46.dat
reports/data_audit/faultseg3d_volume_statistics.csv:49:train,47,128x128x128,float32,float32,8388608,8388608,-4.647228240966797,4.432047367095947,0.0012102959385690143,1.0053139623319556,139368,2097152,6.6455841064453125,0.0;1.0,True,9e576ecc59dc8afc77f167920eec6a108c3a228561e34741c368274327d397bf,b4c50b92c275dc6e4d44ea2043441490833d56f6ae6dd19d1cd758b8ef98522f,data/faultseg3d/train/seis/47.dat,data/faultseg3d/train/fault/47.dat
reports/data_audit/faultseg3d_volume_statistics.csv:50:train,48,128x128x128,float32,float32,8388608,8388608,-5.165307521820068,5.677054405212402,0.002422518566268489,1.0450266487296012,202889,2097152,9.674501419067383,0.0;1.0,True,ce7fe1ec8e5b11fd57ff098c24d32180a48e386ba4c8eb4cbb28905b614f85d8,f1e7f4c12143feed55c69a248073f2ffff298604b6b3af5cc7c21bb8b529018a,data/faultseg3d/train/seis/48.dat,data/faultseg3d/train/fault/48.dat
reports/data_audit/faultseg3d_volume_statistics.csv:51:train,49,128x128x128,float32,float32,8388608,8388608,-4.720161437988281,6.454493522644043,0.0001281455506171869,1.076394361590655,119371,2097152,5.692052841186523,0.0;1.0,True,9c20607d09fc9b8b5e18d7f3e6f97867e833f02f05a0049f16ed5381db907a05,502e5bcae1ca3865e568246cad02635f28aae5ecc2dd8e1d37ee4508c3fcb949,data/faultseg3d/train/seis/49.dat,data/faultseg3d/train/fault/49.dat
reports/data_audit/faultseg3d_volume_statistics.csv:52:train,50,128x128x128,float32,float32,8388608,8388608,-7.0638580322265625,6.421389102935791,0.0014479056714826744,1.1647478282778716,129970,2097152,6.197452545166016,0.0;1.0,True,049b08b7cd7c4144e99f42228104acd1a94bd637752f2568f6096666bf2c03c4,3c45f8459d64b36a7ff1055cecefbcec7459a4e08c4532b1603acd79b66ebe33,data/faultseg3d/train/seis/50.dat,data/faultseg3d/train/fault/50.dat
reports/data_audit/faultseg3d_volume_statistics.csv:54:train,52,128x128x128,float32,float32,8388608,8388608,-6.659264087677002,7.620851993560791,-0.0026097185939491507,1.1657710772660963,156381,2097152,7.456827163696289,0.0;1.0,True,bd1141bd3ed5dadb34afc3c7ad1aba3bf102e0f291fa3502cd1afb439a4eaa4f,b7f2705478f35ab45a011d18fb50f9dadfb4b2fa14ca03707d336ae12c240fa0,data/faultseg3d/train/seis/52.dat,data/faultseg3d/train/fault/52.dat
reports/data_audit/faultseg3d_volume_statistics.csv:55:train,53,128x128x128,float32,float32,8388608,8388608,-5.893111228942871,6.277745723724365,0.0026916961626849006,1.019259129737626,132327,2097152,6.309843063354492,0.0;1.0,True,f76cdcf0c5793a3d94cc71110d66df1e0caf0e1d85bd8a3cdfefee2eb08152cc,33195cf91ab44c95d15ac486072d2cd7a33aa784dfb4b87d8ab30acb814c929f,data/faultseg3d/train/seis/53.dat,data/faultseg3d/train/fault/53.dat
reports/data_audit/faultseg3d_volume_statistics.csv:61:train,59,128x128x128,float32,float32,8388608,8388608,-6.444387912750244,4.515275955200195,0.000163846703627158,1.0000000529837616,136192,2097152,6.494140625,0.0;1.0,True,8eedfb2517ed4fec6a490392172f5d9cabe317ad7f174b998fdcef04d04b0197,9e5e739fb2c1c8a0ca26285446d9809ed17773884da2279f73c6469ba5cb6078,data/faultseg3d/train/seis/59.dat,data/faultseg3d/train/fault/59.dat
reports/data_audit/faultseg3d_volume_statistics.csv:63:train,61,128x128x128,float32,float32,8388608,8388608,-5.614260196685791,5.676007270812988,-7.640234757269604e-05,1.1660855334352116,120197,2097152,5.731439590454102,0.0;1.0,True,acfd17f1cb221524d0a247da43f57830a46ee81f0c5d3f094244534bcb6acaee,ae437cb31e53b558e12e3d254496dc745823431495eca72d2742ceb6b52ab5cf,data/faultseg3d/train/seis/61.dat,data/faultseg3d/train/fault/61.dat
reports/data_audit/faultseg3d_volume_statistics.csv:65:train,63,128x128x128,float32,float32,8388608,8388608,-5.1912689208984375,5.000189304351807,0.0006150453183762624,0.9999998377275376,152287,2097152,7.26161003112793,0.0;1.0,True,ed844e047e5315b5787f57f00762f14d7f5af2ebe9b4765c2146e92d2debc042,bc37bcdac4bcb74a49bfe5652dfc09cdcfa67923ad222126dacb037709ec3e98,data/faultseg3d/train/seis/63.dat,data/faultseg3d/train/fault/63.dat
reports/data_audit/faultseg3d_volume_statistics.csv:70:train,68,128x128x128,float32,float32,8388608,8388608,-4.514305114746094,4.605330467224121,0.0003432913540430127,1.0782654551427853,137710,2097152,6.566524505615234,0.0;1.0,True,a84ee2f287a1ac121b979361d06e2cc4e4c95591850357609f1c665a469d8ad1,e62310d59d23a4f6e90a678a41c92531ddd51af770fcd12069ecd5db2e4e928b,data/faultseg3d/train/seis/68.dat,data/faultseg3d/train/fault/68.dat
reports/data_audit/faultseg3d_volume_statistics.csv:72:train,70,128x128x128,float32,float32,8388608,8388608,-5.672458648681641,5.839572429656982,0.0032332446444545415,1.167950107003017,173795,2097152,8.287191390991211,0.0;1.0,True,d2858914f10322eb6da4d2c128d611f293fd9ccdce6fe752d5d7ef7dc426a344,7a65d9a14c00144ebb6ceea2b46897d50e8df63f689e5ce1fb14133b1716640d,data/faultseg3d/train/seis/70.dat,data/faultseg3d/train/fault/70.dat
reports/data_audit/faultseg3d_volume_statistics.csv:74:train,72,128x128x128,float32,float32,8388608,8388608,-6.445570468902588,4.905670642852783,0.003914182252411927,1.0779355432318571,132971,2097152,6.340551376342773,0.0;1.0,True,0e4b31a0069f94e9a110db517a12ff737b5caaad143b65838afbcebb7276f8b1,cbd86b64b0186f380b49c1f83a4f162da873e88d146b13058079712bb693e5cb,data/faultseg3d/train/seis/72.dat,data/faultseg3d/train/fault/72.dat
reports/data_audit/faultseg3d_volume_statistics.csv:80:train,78,128x128x128,float32,float32,8388608,8388608,-5.253788471221924,6.039716720581055,-0.0009739014294336545,1.0452468939596993,146884,2097152,7.003974914550781,0.0;1.0,True,59ee898634f009179adb58ebd19763d79c942eeca2695423ea63801c0292892c,5befe9045d30f3508798499c9ba331a62a7bef2de98dd496f1cc0801e8efdbf2,data/faultseg3d/train/seis/78.dat,data/faultseg3d/train/fault/78.dat
reports/data_audit/faultseg3d_volume_statistics.csv:85:train,83,128x128x128,float32,float32,8388608,8388608,-5.65297269821167,6.588850498199463,0.0019782228985616296,1.0443346875287778,157859,2097152,7.527303695678711,0.0;1.0,True,e954e76974f126ab1cfbfa6f9fb0209913003f0785ee3abd4df148edc058292c,f5382822cddf71dba260774e1be669cfca14b130e5bb3fdb55d61a3b38f08985,data/faultseg3d/train/seis/83.dat,data/faultseg3d/train/fault/83.dat
reports/data_audit/faultseg3d_volume_statistics.csv:96:train,94,128x128x128,float32,float32,8388608,8388608,-5.619686126708984,6.552521705627441,-0.0012881816794658024,1.1625313388715293,112904,2097152,5.3836822509765625,0.0;1.0,True,9a3034744a3be12cf9af29224bb9129434b5aa97caa89e0a9f16a4f6a85e1bc1,e90a1a339fe5372a702c7112cdd6c4bd3989cabd2a494a0f5d458ddbd294d789,data/faultseg3d/train/seis/94.dat,data/faultseg3d/train/fault/94.dat
reports/data_audit/faultseg3d_volume_statistics.csv:98:train,96,128x128x128,float32,float32,8388608,8388608,-5.419558048248291,4.593428611755371,0.0015208309694864086,1.004578419731196,156187,2097152,7.447576522827148,0.0;1.0,True,5a65bed122c6c1dc9d365948483f4adf325e340bb747ad9f6a4d188f14cf6fcd,e3668d951ee56f73c45609360a158bf0da440055d8f8eb1a7783fbceedc75812,data/faultseg3d/train/seis/96.dat,data/faultseg3d/train/fault/96.dat
reports/data_audit/faultseg3d_volume_statistics.csv:103:train,101,128x128x128,float32,float32,8388608,8388608,-4.871000289916992,5.294002056121826,0.0008203496085734951,1.1194886050248587,133179,2097152,6.350469589233398,0.0;1.0,True,e8b8261ca0477c0b94ff606101f82607c3c7022b3e7151425405bb470d44f314,8bcaa7078199f5433644485708c354b395f1923b5fb558748c6e47a19ae71403,data/faultseg3d/train/seis/101.dat,data/faultseg3d/train/fault/101.dat
reports/data_audit/faultseg3d_volume_statistics.csv:106:train,104,128x128x128,float32,float32,8388608,8388608,-5.645127773284912,5.423936367034912,0.0003862306163582574,1.0435328943467648,140887,2097152,6.718015670776367,0.0;1.0,True,b7af3c517660c17e44d3e1bc0af00dedd382e4e9d03b122e48dbc5c61e98a1ba,3195d312fd4752c74e62c185de6f1921f491f41beb3d83871ac6cfefbda6e419,data/faultseg3d/train/seis/104.dat,data/faultseg3d/train/fault/104.dat
reports/data_audit/faultseg3d_volume_statistics.csv:108:train,106,128x128x128,float32,float32,8388608,8388608,-5.210111618041992,4.604949474334717,0.0018304685622663412,1.0196573310661476,127759,2097152,6.092023849487305,0.0;1.0,True,bd9b3f3c0b6067367bb7fdbd925820f1216473ca9c7447d838fc5471bb631018,880457cf9f65a4d1e408744bd2282bb85787f1f4b99d9b6740c5eaeefbd91777,data/faultseg3d/train/seis/106.dat,data/faultseg3d/train/fault/106.dat
reports/data_audit/faultseg3d_volume_statistics.csv:110:train,108,128x128x128,float32,float32,8388608,8388608,-5.719875335693359,4.940495491027832,-0.002789476947399727,1.0183560876035187,184399,2097152,8.792829513549805,0.0;1.0,True,3914400fc17c1425cb4a4790931a50156db0393b906291b87eb7398af2fe4afe,58cdb5de240a3a61cae799b8cd044aa15f19846fc6d69fb624f93d8674edf490,data/faultseg3d/train/seis/108.dat,data/faultseg3d/train/fault/108.dat
reports/data_audit/faultseg3d_volume_statistics.csv:113:train,111,128x128x128,float32,float32,8388608,8388608,-4.424218654632568,4.636592388153076,-0.0004368046936808797,0.9999998486785602,204105,2097152,9.732484817504883,0.0;1.0,True,4f0b4a059f1240134b402ddd7135d5cba8230896c1831a9acb0fd171c92818e0,5616a770d65ff9f2b7c23b7f116c3b62ef4e63f9d8e95b2e275461d9ccffd800,data/faultseg3d/train/seis/111.dat,data/faultseg3d/train/fault/111.dat
reports/data_audit/faultseg3d_volume_statistics.csv:114:train,112,128x128x128,float32,float32,8388608,8388608,-4.377664566040039,5.756758213043213,0.0008488715992029728,0.9999996192415781,181376,2097152,8.648681640625,0.0;1.0,True,2e8150396763c90285b45e9e3d56aef77d6e1877dcde6b2f8d680197e799d01e,33ced77956edf1b21cc38f35c8f2510c140b89a2e9d050297f0aa12e22900cee,data/faultseg3d/train/seis/112.dat,data/faultseg3d/train/fault/112.dat
reports/data_audit/faultseg3d_volume_statistics.csv:116:train,114,128x128x128,float32,float32,8388608,8388608,-5.313508033752441,5.698538780212402,0.0009918235525940844,1.1144640172469606,131445,2097152,6.267786026000977,0.0;1.0,True,e1ed3a604dacd2302b5702c218a21ea301f8aa2d9ca3673aa0483eab2d7bca33,d6a95642202697c6a788cae8f171ed713405a58e37ab45a4c48845d861b1392b,data/faultseg3d/train/seis/114.dat,data/faultseg3d/train/fault/114.dat
reports/data_audit/faultseg3d_volume_statistics.csv:117:train,115,128x128x128,float32,float32,8388608,8388608,-5.587897777557373,4.881595611572266,-0.001209740097142857,1.019529029727005,201048,2097152,9.586715698242188,0.0;1.0,True,cf668e1c6c77c37667db3dd2525b430e87744935f3b36c95d1a15e9ffa9f14c7,dad244edf6b796736bb080a7d786801391230d884cfcfbaaaf4fe4b5408dca4b,data/faultseg3d/train/seis/115.dat,data/faultseg3d/train/fault/115.dat
reports/data_audit/faultseg3d_volume_statistics.csv:118:train,116,128x128x128,float32,float32,8388608,8388608,-4.372591972351074,4.689971923828125,0.0054110601718749905,0.9999853724513861,191422,2097152,9.12771224975586,0.0;1.0,True,8d866a689bcf8f6c6fc1645aca59ab113b0df385959b159a731c2db764094acf,eda89f9eef18ce5fbe13fe70d3df13abaa67bb73231ed83513d79fc4c4c2abaf,data/faultseg3d/train/seis/116.dat,data/faultseg3d/train/fault/116.dat
reports/data_audit/faultseg3d_volume_statistics.csv:119:train,117,128x128x128,float32,float32,8388608,8388608,-4.209198951721191,4.551249027252197,0.004465262338585463,1.0190943474038225,124455,2097152,5.934476852416992,0.0;1.0,True,c900345a5abee3394d02d132ca04751dccf2e5aad77fa1a0335f6f3bd62f19c7,dbee2538515110cfbce55f9a61d93f15b2810fe8d4d298d4e81ad6106faf2fa0,data/faultseg3d/train/seis/117.dat,data/faultseg3d/train/fault/117.dat
reports/data_audit/faultseg3d_volume_statistics.csv:124:train,122,128x128x128,float32,float32,8388608,8388608,-4.819046497344971,5.258120536804199,-0.0005258400334720303,1.0427365208712667,103450,2097152,4.932880401611328,0.0;1.0,True,72b6d88ff115932e47665b97d0cad75ebad48687439a09720c17b9788c33f3f5,d860778c3945b39ec22935948709fb8ada43bf5663b5a8ecbf1b69d6785a9bb8,data/faultseg3d/train/seis/122.dat,data/faultseg3d/train/fault/122.dat
reports/data_audit/faultseg3d_volume_statistics.csv:127:train,125,128x128x128,float32,float32,8388608,8388608,-5.222195625305176,4.101653099060059,0.002321367292934679,0.9999972716155272,192843,2097152,9.195470809936523,0.0;1.0,True,a1f51af18417a6301fb5fcbda24d2b148e6993cca53d4c9ee81af5e447a03694,2b86e767829bc6a9c90c6c2a32844aeb3538f83864c1bd0f41af48a97fad4c9d,data/faultseg3d/train/seis/125.dat,data/faultseg3d/train/fault/125.dat
reports/data_audit/faultseg3d_volume_statistics.csv:134:train,132,128x128x128,float32,float32,8388608,8388608,-3.802238941192627,6.326815128326416,-0.0016019257704280323,0.9999987549168396,170950,2097152,8.151531219482422,0.0;1.0,True,ad4a675035a35c10355f9edf6bb96308fd7bd507d69df84cfbde6735530add61,3f6b7959f2391309daff1b27a3548ba11b4d7211befe3b12ff35d680be238fe5,data/faultseg3d/train/seis/132.dat,data/faultseg3d/train/fault/132.dat
reports/data_audit/thebe_h5_statistics.csv:6:train,100x3174x1537,float64,bool,float32,uint8,-2.6587982177734375,2.834458351135254,-2.925060121001068e-06,0.11106203265206424,3570872,487843800,0.7319703560852879,66027b1f4df037aa0c3dae4a08ff42d11872068d6a9ddc479fd820d62c39ee3e,94d8fe88e7e8ead7d6399cfa2c9bfd256b75f1851a8c242a0180247969d9b7ac,data/thebe/seis/seistrain5.npz,data/thebe/fault/faulttrain5.npz,data/processed/thebe_h5/train5.h5,844142314
reports/data_audit/thebe_h5_statistics.csv:7:train,100x3174x1537,float64,bool,float32,uint8,-2.676699638366699,9.433253288269043,5.592769920060861e-06,0.11655410640016116,3909866,487843800,0.8014585816197726,7580b1a3ba71b9abc1f63f54acf1d2b6c407a9b003d0180886446aa01560529f,71b418f08d9ed0d0a346496e07e82cae9967f5e588f2c825e05eb88bd17a8631,data/thebe/seis/seistrain6.npz,data/thebe/fault/faulttrain6.npz,data/processed/thebe_h5/train6.h5,877969475
reports/data_audit/thebe_h5_statistics.csv:8:train,100x3174x1537,float64,bool,float32,uint8,-2.7207870483398438,2.8281021118164062,1.1942063768727192e-05,0.12574849960104517,6197892,487843800,1.2704664894788045,a8e2deff21c5a1e2fb45a758b466bfb46f30762153d96fd340055a6c37f816d6,1621e3db04c5ea33dc96a87e3f54cf1d5031341f7080fa85c7353d52eab21cc9,data/thebe/seis/seistrain7.npz,data/thebe/fault/faulttrain7.npz,data/processed/thebe_h5/train7.h5,1032693045
reports/data_audit/thebe_h5_statistics.csv:11:val,100x3174x1537,float64,bool,float32,uint8,-3.718324661254883,3.5749521255493164,-8.142081609447118e-06,0.13305340028663978,7906942,487843800,1.620793786863746,f6cca2e72c86d89e2c05feb92a1604a96d22a3557c25249f1cb2244e95205437,88341218e0d5e63b9092985d6c31612d6d64144d676babf8db194342d59c2bfb,data/thebe/seis/seisval1.npz,data/thebe/fault/faultval1.npz,data/processed/thebe_h5/val1.h5,1116731622
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:59:train,100x3174x1537,float64,bool,float32,uint8,-2.6587982177734375,2.834458351135254,-2.925060121001068e-06,0.11106203265206424,3570872,487843800,0.7319703560852879,66027b1f4df037aa0c3dae4a08ff42d11872068d6a9ddc479fd820d62c39ee3e,94d8fe88e7e8ead7d6399cfa2c9bfd256b75f1851a8c242a0180247969d9b7ac,data/thebe/seis/seistrain5.npz,data/thebe/fault/faulttrain5.npz,data/processed/thebe_h5/train5.h5,844142314
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:60:train,100x3174x1537,float64,bool,float32,uint8,-2.676699638366699,9.433253288269043,5.592769920060861e-06,0.11655410640016116,3909866,487843800,0.8014585816197726,7580b1a3ba71b9abc1f63f54acf1d2b6c407a9b003d0180886446aa01560529f,71b418f08d9ed0d0a346496e07e82cae9967f5e588f2c825e05eb88bd17a8631,data/thebe/seis/seistrain6.npz,data/thebe/fault/faulttrain6.npz,data/processed/thebe_h5/train6.h5,877969475
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:61:train,100x3174x1537,float64,bool,float32,uint8,-2.7207870483398438,2.8281021118164062,1.1942063768727192e-05,0.12574849960104517,6197892,487843800,1.2704664894788045,a8e2deff21c5a1e2fb45a758b466bfb46f30762153d96fd340055a6c37f816d6,1621e3db04c5ea33dc96a87e3f54cf1d5031341f7080fa85c7353d52eab21cc9,data/thebe/seis/seistrain7.npz,data/thebe/fault/faulttrain7.npz,data/processed/thebe_h5/train7.h5,1032693045
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:64:val,100x3174x1537,float64,bool,float32,uint8,-3.718324661254883,3.5749521255493164,-8.142081609447118e-06,0.13305340028663978,7906942,487843800,1.620793786863746,f6cca2e72c86d89e2c05feb92a1604a96d22a3557c25249f1cb2244e95205437,88341218e0d5e63b9092985d6c31612d6d64144d676babf8db194342d59c2bfb,data/thebe/seis/seisval1.npz,data/thebe/fault/faultval1.npz,data/processed/thebe_h5/val1.h5,1116731622
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:383:def soft_dice_loss(logits: Tensor, target: Tensor, smooth: float = 1.0) -> Tensor:
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:931:scripts/faultseg3d_baseline.py-637-        if validation.dice > best_dice:
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:932:scripts/faultseg3d_baseline.py-638-            best_dice = validation.dice
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:936:scripts/faultseg3d_baseline.py-642-            f"val_dice={validation.dice:.6f} val_iou={validation.iou:.6f} "
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:949:scripts/faultseg3d_baseline.py-658-    selected_threshold = validation_histogram.best_dice_threshold()
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:975:scripts/faultseg3d_baseline.py-721-        "--loss", choices=("b0_bce", "b1_weighted_dice"), default="b0_bce"
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:1060:0abe7b6148676b8bd645f04f151177776f75c37c7fdf416c766766bd1fa0970e  reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:1087:import mathimport reimport sysimport timefrom dataclasses import asdictfrom pathlib import Pathfrom typing import Anyimport h5pyimport numpy as npimport torchdef natural_key(path: Path) -> list[object]:    return [        int(part) if part.isdigit() else part.lower()        for part in re.split(r"(\d+)", path.name)    ]def load_baseline_module(path: Path):    specification = importlib.util.spec_from_file_location(        "faultseg3d_baseline_imported",        path,    )    if specification is None or specification.loader is None:        raise RuntimeError(f"Cannot import baseline module: {path}")    module = importlib.util.module_from_spec(specification)    sys.modules[specification.name] = module    specification.loader.exec_module(module)    return moduleclass ConcatenatedThebe:    """Read ordered test H5 blocks as one volume along axis zero."""    def __init__(self, paths: list[Path]) -> None:        if not paths:            raise RuntimeError("No Thebe test H5 files were supplied")        self.paths = paths        self.handles = [h5py.File(path, "r") for path in paths]        self.offsets: list[int] = []        self.lengths: list[int] = []        reference_tail: tuple[int, int] | None = None        running = 0        for path, handle in zip(self.paths, self.handles):            if "seismic" not in handle or "fault" not in handle:                raise RuntimeError(                    f"{path} must contain datasets named seismic and fault"                )            seismic_shape = tuple(handle["seismic"].shape)            fault_shape = tuple(handle["fault"].shape)            if seismic_shape != fault_shape or len(seismic_shape) != 3:                raise RuntimeError(                    f"Shape mismatch in {path}: "                    f"seismic={seismic_shape}, fault={fault_shape}"                )            if reference_tail is None:                reference_tail = seismic_shape[1:]            elif seismic_shape[1:] != reference_tail:                raise RuntimeError(                    f"Incompatible spatial shape in {path}: {seismic_shape}"                )            self.offsets.append(running)            self.lengths.append(seismic_shape[0])            running += seismic_shape[0]        assert reference_tail is not None        self.shape = (running, *reference_tail)    def close(self) -> None:        for handle in self.handles:            handle.close()    def read(        self,        key: str,        x0: int,        x1: int,        y0: int,        y1: int,        z0: int,        z1: int,    ) -> np.ndarray:        pieces: list[np.ndarray] = []        for offset, length, handle in zip(            self.offsets,            self.lengths,            self.handles,        ):            block_end = offset + length            overlap_start = max(x0, offset)            overlap_end = min(x1, block_end)            if overlap_start >= overlap_end:                continue            local_start = overlap_start - offset            local_end = overlap_end - offset            piece = np.asarray(                handle[key][local_start:local_end, y0:y1, z0:z1]            )            pieces.append(piece)        if not pieces:            raise RuntimeError(                f"No data read for {key}: "                f"x={x0}:{x1}, y={y0}:{y1}, z={z0}:{z1}"            )        if len(pieces) == 1:            return pieces[0]        return np.concatenate(pieces, axis=0)def summarize_rows(    rows: list[dict[str, Any]],) -> dict[str, dict[str, float]]:    selected = (        "dice",        "iou",        "precision",        "recall",        "specificity",        "balanced_accuracy",        "accuracy",        "mcc",        "pr_auc_approx",        "roc_auc_approx",        "modified_hausdorff_voxels",        "bidirectional_chamfer_voxels",        "inference_seconds",    )    summary: dict[str, dict[str, float]] = {}    for key in selected:        values = np.asarray(            [float(row[key]) for row in rows if key in row],            dtype=np.float64,        )        if values.size == 0:            continue        summary[key] = {            "mean": float(values.mean()),            "std": float(values.std()),            "median": float(np.median(values)),            "min": float(values.min()),            "max": float(values.max()),        }    return summarydef write_csv_atomic(path: Path, rows: list[dict[str, Any]]) -> None:    if not rows:        return    temporary = path.with_suffix(path.suffix + ".part")    with temporary.open("w", newline="", encoding="utf-8") as stream:        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))        writer.writeheader()        writer.writerows(rows)    temporary.replace(path)def middle_slices(array: np.ndarray) -> dict[str, np.ndarray]:    return {        "axis0": array[array.shape[0] // 2, :, :],        "axis1": array[:, array.shape[1] // 2, :],        "axis2": array[:, :, array.shape[2] // 2],    }def build_parser() -> argparse.ArgumentParser:    parser = argparse.ArgumentParser(description=__doc__)    parser.add_argument(        "--baseline-script",        type=Path,        default=Path("scripts/faultseg3d_baseline.py"),    )    parser.add_argument(        "--checkpoint",        type=Path,        default=Path(            "runs/baseline_A_synthetic_bce_seed42/best.pt"        ),    )    parser.add_argument(        "--threshold-metrics",        type=Path,        default=Path(            "runs/baseline_A_synthetic_bce_seed42/final_metrics.json"        ),    )    parser.add_argument(        "--thebe-root",        type=Path,        default=Path("data/processed/thebe_h5"),    )    parser.add_argument("--output-dir", type=Path, required=True)    parser.add_argument(        "--max-patches",        type=int,        default=None,        help="For smoke testing only. Omit for complete evaluation.",    )    parser.add_argument("--save-examples", type=int, default=12)    return parserdef main() -> None:    args = build_parser().parse_args()    if not torch.cuda.is_available():        raise RuntimeError(            "CUDA GPU is unavailable. Attach a GPU before evaluation."        )    required = (        args.baseline_script,        args.checkpoint,        args.threshold_metrics,    )    for path in required:        if not path.is_file():            raise FileNotFoundError(path)    if args.output_dir.exists() and any(args.output_dir.iterdir()):        raise RuntimeError(            f"Output directory is not empty: {args.output_dir}"        )    args.output_dir.mkdir(parents=True, exist_ok=True)    example_dir = args.output_dir / "prediction_examples"    example_dir.mkdir(parents=True, exist_ok=True)    test_files = sorted(        args.thebe_root.glob("test*.h5"),        key=natural_key,    )    if not test_files:        raise RuntimeError(            f"No official test*.h5 files found in {args.thebe_root}"        )    # Explicitly reject accidental train/validation use.    for path in test_files:        if not path.name.startswith("test"):            raise RuntimeError(f"Non-test file selected: {path}")    threshold_document = json.loads(        args.threshold_metrics.read_text(encoding="utf-8")    )    threshold = float(        threshold_document[            "threshold_selected_on_internal_validation"        ]    )    if not 0.0 < threshold < 1.0:        raise RuntimeError(f"Invalid frozen threshold: {threshold}")    baseline = load_baseline_module(args.baseline_script)    volume_shape = tuple(int(value) for value in baseline.VOLUME_SHAPE)    if len(volume_shape) != 3 or len(set(volume_shape)) != 1:        raise RuntimeError(            f"Expected a cubic baseline volume shape, got {volume_shape}"        )    patch_size = volume_shape[0]    checkpoint = torch.load(        args.checkpoint,        map_location="cpu",        weights_only=False,    )    if "model" not in checkpoint:        raise RuntimeError("Checkpoint does not contain model weights")    checkpoint_args = checkpoint.get("args", {})    histogram_bins = int(        checkpoint_args.get("histogram_bins", 2048)    )    device = torch.device("cuda")    model = baseline.FaultSeg3D().to(device)    model.load_state_dict(checkpoint["model"], strict=True)    model.eval()    for parameter in model.parameters():        parameter.requires_grad_(False)    torch.manual_seed(42)    np.random.seed(42)    torch.backends.cudnn.benchmark = False    torch.backends.cudnn.deterministic = True    torch.cuda.reset_peak_memory_stats()    reader = ConcatenatedThebe(test_files)    total_shape = reader.shape    x_starts = list(range(0, total_shape[0], patch_size))    y_starts = list(range(0, total_shape[1], patch_size))    z_starts = list(range(0, total_shape[2], patch_size))    coordinates = list(        itertools.product(x_starts, y_starts, z_starts)    )    full_patch_count = len(coordinates)    if args.max_patches is not None:        if args.max_patches <= 0:            raise ValueError("--max-patches must be positive")        coordinates = coordinates[: args.max_patches]    complete_evaluation = len(coordinates) == full_patch_count    run_configuration = {        "experiment": "A_to_T0_zero_shot",        "training_performed": False,        "weight_updates": 0,        "checkpoint": str(args.checkpoint),        "checkpoint_epoch": int(checkpoint.get("epoch", -1)),        "checkpoint_training_data": checkpoint_args.get(            "data_root",            "unknown",        ),        "threshold": threshold,        "threshold_source": str(args.threshold_metrics),        "threshold_selected_using_thebe": False,        "data_split": "official Thebe test only",        "test_files": [str(path) for path in test_files],        "test_block_count": len(test_files),        "concatenated_test_shape": list(total_shape),        "patch_shape": list(volume_shape),        "patch_count_planned": full_patch_count,        "patch_count_this_run": len(coordinates),        "complete_official_test_evaluation": complete_evaluation,        "normalization": (            "independent z-score on each valid 3D patch, "            "matching Baseline A"        ),        "axis_transform": "np.transpose, matching Baseline A",        "edge_policy": (            "zero-pad normalized inputs to 128^3; "            "exclude padding from every metric"        ),        "overlap_policy": (            "non-overlapping partition; every valid voxel evaluated once"        ),        "histogram_bins": histogram_bins,    }    (args.output_dir / "run_configuration.json").write_text(        json.dumps(run_configuration, indent=2, sort_keys=True),        encoding="utf-8",    )    aggregate = baseline.ProbabilityHistogram(histogram_bins)    rows: list[dict[str, Any]] = []    evaluated_voxels = 0    total_inference_seconds = 0.0    saved_examples = 0    started = time.time()    try:        for patch_number, (x0, y0, z0) in enumerate(            coordinates,            start=1,        ):            x1 = min(x0 + patch_size, total_shape[0])            y1 = min(y0 + patch_size, total_shape[1])            z1 = min(z0 + patch_size, total_shape[2])            size_x = x1 - x0            size_y = y1 - y0            size_z = z1 - z0            seismic_raw = reader.read(                "seismic", x0, x1, y0, y1, z0, z1            ).astype(np.float32, copy=False)            fault_raw = reader.read(                "fault", x0, x1, y0, y1, z0, z1            ).astype(np.uint8, copy=False)            expected_shape = (size_x, size_y, size_z)            if seismic_raw.shape != expected_shape:                raise RuntimeError(                    f"Unexpected seismic shape: "                    f"{seismic_raw.shape} != {expected_shape}"                )            if fault_raw.shape != expected_shape:                raise RuntimeError(                    f"Unexpected fault shape: "                    f"{fault_raw.shape} != {expected_shape}"                )            if not np.isfinite(seismic_raw).all():                raise RuntimeError(                    f"NaN/Inf in patch starting at {(x0, y0, z0)}"                )            if fault_raw.min() < 0 or fault_raw.max() > 1:                raise RuntimeError(                    f"Non-binary fault values at {(x0, y0, z0)}"                )            patch_mean = float(                seismic_raw.mean(dtype=np.float64)            )            patch_std = float(                seismic_raw.std(dtype=np.float64)            )            if not patch_std > 0.0:                raise RuntimeError(                    f"Zero seismic standard deviation at "                    f"{(x0, y0, z0)}"                )            seismic_normalized = (                seismic_raw - patch_mean            ) / patch_std            seismic_padded = np.zeros(                volume_shape,                dtype=np.float32,            )            fault_padded = np.zeros(                volume_shape,                dtype=np.float32,            )            seismic_padded[                :size_x, :size_y, :size_z            ] = seismic_normalized            fault_padded[                :size_x, :size_y, :size_z            ] = fault_raw            # Match Baseline A axis reversal.            seismic_model = np.ascontiguousarray(                np.transpose(seismic_padded),                dtype=np.float32,            )            fault_model = np.ascontiguousarray(                np.transpose(fault_padded),                dtype=np.float32,            )            model_input = torch.from_numpy(                seismic_model[None, None]            ).to(device)            target_tensor = torch.from_numpy(                fault_model            ).to(device)            torch.cuda.synchronize()            inference_started = time.perf_counter()            with torch.inference_mode():                with torch.autocast(                    device_type="cuda",                    dtype=torch.float16,                ):                    logits = model(model_input)                probability = torch.sigmoid(                    logits.float()                )[0, 0]            torch.cuda.synchronize()            inference_seconds = (                time.perf_counter() - inference_started            )            total_inference_seconds += inference_seconds            # Dimensions reverse after np.transpose.            valid_model_shape = (size_z, size_y, size_x)            valid_z, valid_y, valid_x = valid_model_shape            probability_valid = probability[                :valid_z, :valid_y, :valid_x            ]            target_valid = target_tensor[                :valid_z, :valid_y, :valid_x            ]            valid_voxels = (                valid_z * valid_y * valid_x            )            evaluated_voxels += valid_voxels            aggregate.update_probabilities(                probability_valid,                target_valid,            )            individual = baseline.ProbabilityHistogram(                histogram_bins            )            individual.update_probabilities(                probability_valid,                target_valid,            )            row: dict[str, Any] = {                "patch_id": (                    f"x{x0:04d}_y{y0:04d}_z{z0:04d}"                ),                "raw_x_start": x0,                "raw_x_stop": x1,                "raw_y_start": y0,                "raw_y_stop": y1,                "raw_z_start": z0,                "raw_z_stop": z1,                "valid_voxels": valid_voxels,                "normalization_mean": patch_mean,                "normalization_std": patch_std,                **asdict(individual.metrics(threshold)),            }            probability_numpy = (                probability_valid.detach().cpu().numpy()            )            target_numpy = (                target_valid.detach().cpu().numpy() >= 0.5            )            prediction_numpy = (                probability_numpy >= threshold            )            row.update(                baseline.structural_distances(                    prediction_numpy,                    target_numpy,                )            )            row["inference_seconds"] = inference_seconds            rows.append(row)            if (                saved_examples < args.save_examples                and bool(target_numpy.any())            ):                seismic_valid = seismic_model[                    :valid_z, :valid_y, :valid_x                ]                arrays: dict[str, np.ndarray] = {                    "coordinates_raw": np.asarray(                        [x0, x1, y0, y1, z0, z1],                        dtype=np.int32,                    ),                    "threshold": np.asarray(                        threshold,                        dtype=np.float32,                    ),                }                for prefix, array in (                    ("seismic", seismic_valid),                    ("probability", probability_numpy),                    ("target", target_numpy.astype(np.uint8)),                    (                        "prediction",                        prediction_numpy.astype(np.uint8),                    ),                ):                    for axis_name, image in middle_slices(                        array                    ).items():                        arrays[                            f"{prefix}_{axis_name}"                        ] = image                np.savez_compressed(                    example_dir                    / f"example_{saved_examples + 1:02d}_"                    f"{row['patch_id']}.npz",                    **arrays,                )                saved_examples += 1            if (                patch_number % 25 == 0                or patch_number == len(coordinates)            ):                write_csv_atomic(                    args.output_dir / "test_per_patch.csv",                    rows,                )                print(                    f"processed={patch_number}/"                    f"{len(coordinates)} "                    f"elapsed_minutes="                    f"{(time.time() - started) / 60.0:.2f}",                    flush=True,                )    finally:        reader.close()    if complete_evaluation:        expected_voxels = int(math.prod(total_shape))        if evaluated_voxels != expected_voxels:            raise RuntimeError(                f"Coverage failure: evaluated "                f"{evaluated_voxels} voxels, "                f"expected {expected_voxels}"            )    aggregate_metrics = asdict(        aggregate.metrics(threshold)    )    elapsed_seconds = time.time() - started    final_result = {        "experiment": "A_to_T0_zero_shot",        "status": (            "complete_official_test"            if complete_evaluation            else "smoke_test_only"        ),        "training_performed": False,        "weight_updates": 0,        "threshold": threshold,        "threshold_source": (            "Baseline A synthetic validation"        ),        "thebe_labels_used_for_threshold": False,        "official_thebe_test": aggregate_metrics,        "official_thebe_test_per_patch_summary": (            summarize_rows(rows)        ),        "data": {            "test_files": [str(path) for path in test_files],            "test_shape": list(total_shape),            "patch_shape": list(volume_shape),            "patches_evaluated": len(rows),            "full_patch_count": full_patch_count,            "evaluated_voxels": evaluated_voxels,            "expected_full_test_voxels": int(                math.prod(total_shape)            ),            "complete_coverage": complete_evaluation,            "overlap": False,            "padding_counted_in_metrics": False,        },        "efficiency": {            "wall_seconds": elapsed_seconds,            "total_model_inference_seconds": (                total_inference_seconds            ),            "mean_model_inference_seconds_per_patch": (                total_inference_seconds / len(rows)            ),            "peak_cuda_gib": (                torch.cuda.max_memory_allocated()                / 1024**3            ),        },        "prediction_examples_saved": saved_examples,        "metric_notes": {            "distance_units": "voxels",            "modified_hausdorff": (                "max of directed mean nearest-point distances"            ),            "bidirectional_chamfer": (                "sum of directed mean nearest-point distances"            ),            "one_empty_mask_policy": (                "valid-patch diagonal penalty"            ),            "important": (                "These results measure zero-shot transfer "                "from synthetic FaultSeg3D to real Thebe."            ),        },    }    temporary_json = (        args.output_dir / "final_metrics.json.part"    )    temporary_json.write_text(        json.dumps(            final_result,            indent=2,            sort_keys=True,        ),        encoding="utf-8",    )    temporary_json.replace(        args.output_dir / "final_metrics.json"    )    write_csv_atomic(        args.output_dir / "test_per_patch.csv",        rows,    )    print("\n=== ZERO-SHOT RESULT ===")    print(f"status={final_result['status']}")    print(f"threshold={threshold:.6f}")    print(        f"dice={aggregate_metrics['dice']:.6f}"    )    print(        f"iou={aggregate_metrics['iou']:.6f}"    )    print(        f"precision={aggregate_metrics['precision']:.6f}"    )    print(        f"recall={aggregate_metrics['recall']:.6f}"[7m    )[27m[7m    print([27m[7m        f"mcc={aggregate_metrics['mcc']:.6f}"[27m[7m    )[27m[7m    print([27m[7m        f"pr_auc={aggregate_metrics['pr_auc_approx']:.6f}"[27m[7m    )[27m[7m    print([27m[7m        "results="[27m[7m        f"{args.output_dir / 'final_metrics.json'}"[27m[7m    )[27m[7mif __name__ == "__main__":[27m[7m    main()[27m[7mPY[27m[7mchmod +x scripts/evaluate_thebe_zero_shot.py[27m[7m.venv_train/bin/python -m py_compile \[27m[7m    scripts/evaluate_thebe_zero_shot.py[27m[7mecho "PASS: evaluator created and syntax checked."[27m    )    print(        f"mcc={aggregate_metrics['mcc']:.6f}"    )    print(        f"pr_auc={aggregate_metrics['pr_auc_approx']:.6f}"    )    print(        "results="        f"{args.output_dir / 'final_metrics.json'}"    )if __name__ == "__main__":    main()PYchmod +x scripts/evaluate_thebe_zero_shot.py.venv_train/bin/python -m py_compile \    scripts/evaluate_thebe_zero_shot.pyecho "PASS: evaluator created and syntax checked."
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:67:    train,100x3174x1537,float64,bool,float32,uint8,-2.6587982177734375,2.834458351135254,-2.925060121001068e-06,0.11106203265206424,3570872,487843800,0.7319703560852879,66027b1f4df037aa0c3dae4a08ff42d11872068d6a9ddc479fd820d62c39ee3e,94d8fe88e7e8ead7d6399cfa2c9bfd256b75f1851a8c242a0180247969d9b7ac,data/thebe/seis/seistrain5.npz,data/thebe/fault/faulttrain5.npz,data/processed/thebe_h5/train5.h5,844142314
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:68:    train,100x3174x1537,float64,bool,float32,uint8,-2.676699638366699,9.433253288269043,5.592769920060861e-06,0.11655410640016116,3909866,487843800,0.8014585816197726,7580b1a3ba71b9abc1f63f54acf1d2b6c407a9b003d0180886446aa01560529f,71b418f08d9ed0d0a346496e07e82cae9967f5e588f2c825e05eb88bd17a8631,data/thebe/seis/seistrain6.npz,data/thebe/fault/faulttrain6.npz,data/processed/thebe_h5/train6.h5,877969475
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:69:    train,100x3174x1537,float64,bool,float32,uint8,-2.7207870483398438,2.8281021118164062,1.1942063768727192e-05,0.12574849960104517,6197892,487843800,1.2704664894788045,a8e2deff21c5a1e2fb45a758b466bfb46f30762153d96fd340055a6c37f816d6,1621e3db04c5ea33dc96a87e3f54cf1d5031341f7080fa85c7353d52eab21cc9,data/thebe/seis/seistrain7.npz,data/thebe/fault/faulttrain7.npz,data/processed/thebe_h5/train7.h5,1032693045
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:72:    val,100x3174x1537,float64,bool,float32,uint8,-3.718324661254883,3.5749521255493164,-8.142081609447118e-06,0.13305340028663978,7906942,487843800,1.620793786863746,f6cca2e72c86d89e2c05feb92a1604a96d22a3557c25249f1cb2244e95205437,88341218e0d5e63b9092985d6c31612d6d64144d676babf8db194342d59c2bfb,data/thebe/seis/seisval1.npz,data/thebe/fault/faultval1.npz,data/processed/thebe_h5/val1.h5,1116731622
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:391:    def soft_dice_loss(logits: Tensor, target: Tensor, smooth: float = 1.0) -> Tensor:
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:939:    scripts/faultseg3d_baseline.py-637-        if validation.dice > best_dice:
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:940:    scripts/faultseg3d_baseline.py-638-            best_dice = validation.dice
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:944:    scripts/faultseg3d_baseline.py-642-            f"val_dice={validation.dice:.6f} val_iou={validation.iou:.6f} "
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:957:    scripts/faultseg3d_baseline.py-658-    selected_threshold = validation_histogram.best_dice_threshold()
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:983:    scripts/faultseg3d_baseline.py-721-        "--loss", choices=("b0_bce", "b1_weighted_dice"), default="b0_bce"
reports/debug/cracks_evaluation_context.md:172:0209:             f"dice={metrics['dice']:.6f} pr_auc={metrics['pr_auc_approx']:.6f}",
reports/debug/cracks_evaluation_context.md:210:0254:     print(f"dice={final_metrics['dice']:.6f}")
reports/debug/cracks_evaluation_context.md:211:0255:     print(f"iou={final_metrics['iou']:.6f}")
reports/debug/cracks_evaluation_context.md:212:0256:     print(f"precision={final_metrics['precision']:.6f}")
reports/debug/cracks_evaluation_context.md:213:0257:     print(f"recall={final_metrics['recall']:.6f}")
reports/debug/cracks_evaluation_context.md:433:section,valid_pixels,certain_fault_pixels,threshold,dice,iou,precision,recall,specificity,balanced_accuracy,accuracy,mcc,pr_auc_approx,roc_auc_approx,tp,fp,fn,tn
reports/debug/cracks_evaluation_context.md:485:    "dice": 0.05755252130783045,
reports/debug/cracks_evaluation_context.md:488:    "iou": 0.029628868702581336,
reports/debug/cracks_evaluation_context.md:491:    "precision": 0.038205351398402906,
reports/debug/cracks_evaluation_context.md:492:    "recall": 0.1165973665973666,
reports/debug/cracks_evaluation_context.md:493:    "roc_auc_approx": 0.5417569783713032,
reports/evaluation/A_TO_T0_FINAL_REPORT_20261005_095032.md:31:| Dice/F1 | 0.085861 |
reports/evaluation/A_TO_T0_FINAL_REPORT_20261005_095032.md:32:| IoU | 0.044856 |
reports/evaluation/A_TO_T0_FINAL_REPORT_20261005_095032.md:33:| Precision | 0.052094 |
reports/evaluation/A_TO_T0_FINAL_REPORT_20261005_095032.md:34:| Recall | 0.244065 |
reports/evaluation/A_TO_T0_FINAL_REPORT_20261005_095032.md:39:| ROC-AUC | 0.654087 |
reports/evaluation/A_TO_T0_FINAL_REPORT_20261005_095032.md:66:  "dice": {
reports/evaluation/A_TO_T0_FINAL_REPORT_20261005_095032.md:80:  "iou": {
reports/evaluation/A_TO_T0_FINAL_REPORT_20261005_095032.md:108:  "precision": {
reports/evaluation/A_TO_T0_FINAL_REPORT_20261005_095032.md:115:  "recall": {
reports/evaluation/A_TO_T0_FINAL_REPORT_20261005_095032.md:122:  "roc_auc_approx": {
reports/evaluation/a_to_t0_final_summary_20261005_095032.txt:2:DICE: 0.085861
reports/evaluation/a_to_t0_final_summary_20261005_095032.txt:3:IOU: 0.044856
reports/evaluation/a_to_t0_final_summary_20261005_095032.txt:4:PRECISION: 0.052094
reports/evaluation/a_to_t0_final_summary_20261005_095032.txt:5:RECALL: 0.244065
reports/evaluation/baseline_A_zero_shot_thebe_full_20261005_095032.log:64:dice=0.085861
reports/evaluation/baseline_A_zero_shot_thebe_full_20261005_095032.log:65:iou=0.044856
reports/evaluation/baseline_A_zero_shot_thebe_full_20261005_095032.log:66:precision=0.052094
reports/evaluation/baseline_A_zero_shot_thebe_full_20261005_095032.log:67:recall=0.244065
reports/evaluation/baseline_A_zero_shot_thebe_smoke_20261005_094726.log:6:dice=0.068389
reports/evaluation/baseline_A_zero_shot_thebe_smoke_20261005_094726.log:7:iou=0.035405
reports/evaluation/baseline_A_zero_shot_thebe_smoke_20261005_094726.log:8:precision=0.041877
reports/evaluation/baseline_A_zero_shot_thebe_smoke_20261005_094726.log:9:recall=0.186394
reports/evaluation/cracks_error_excerpt.md:12:    "dice": 0.03527294979404324,
reports/evaluation/cracks_error_excerpt.md:15:    "iou": 0.01795310437159486,
reports/evaluation/cracks_error_excerpt.md:18:    "precision": 0.024374183477476077,
reports/evaluation/cracks_error_excerpt.md:19:    "recall": 0.06380131611553182,
reports/evaluation/cracks_error_excerpt.md:20:    "roc_auc_approx": 0.5010833013464665,
reports/evaluation/cracks_error_excerpt.md:58:section,valid_pixels,fault_pixels,threshold,dice,iou,precision,recall,specificity,balanced_accuracy,accuracy,mcc,pr_auc_approx,roc_auc_approx,tp,fp,fn,tn
reports/evaluation/latest_cracks_run.md:6:expert_section=01/40 id=010 dice=0.049329 pr_auc=0.026505
reports/evaluation/latest_cracks_run.md:7:expert_section=02/40 id=013 dice=0.032290 pr_auc=0.022734
reports/evaluation/latest_cracks_run.md:8:expert_section=03/40 id=017 dice=0.058418 pr_auc=0.035881
reports/evaluation/latest_cracks_run.md:9:expert_section=04/40 id=022 dice=0.043812 pr_auc=0.027374
reports/evaluation/latest_cracks_run.md:10:expert_section=05/40 id=024 dice=0.046500 pr_auc=0.029002
reports/evaluation/latest_cracks_run.md:11:expert_section=06/40 id=035 dice=0.045835 pr_auc=0.030274
reports/evaluation/latest_cracks_run.md:12:expert_section=07/40 id=041 dice=0.041046 pr_auc=0.027501
reports/evaluation/latest_cracks_run.md:13:expert_section=08/40 id=043 dice=0.044772 pr_auc=0.031180
reports/evaluation/latest_cracks_run.md:14:expert_section=09/40 id=046 dice=0.035404 pr_auc=0.036944
reports/evaluation/latest_cracks_run.md:15:expert_section=10/40 id=051 dice=0.034891 pr_auc=0.018577
reports/evaluation/latest_cracks_run.md:16:expert_section=11/40 id=067 dice=0.039859 pr_auc=0.020991
reports/evaluation/latest_cracks_run.md:17:expert_section=12/40 id=068 dice=0.041415 pr_auc=0.023222
reports/evaluation/latest_cracks_run.md:18:expert_section=13/40 id=106 dice=0.047187 pr_auc=0.027899
reports/evaluation/latest_cracks_run.md:19:expert_section=14/40 id=108 dice=0.045554 pr_auc=0.027133
reports/evaluation/latest_cracks_run.md:20:expert_section=15/40 id=116 dice=0.050032 pr_auc=0.031742
reports/evaluation/latest_cracks_run.md:21:expert_section=16/40 id=124 dice=0.036850 pr_auc=0.025786
reports/evaluation/latest_cracks_run.md:22:expert_section=17/40 id=131 dice=0.039086 pr_auc=0.021367
reports/evaluation/latest_cracks_run.md:23:expert_section=18/40 id=133 dice=0.034859 pr_auc=0.020606
reports/evaluation/latest_cracks_run.md:24:expert_section=19/40 id=136 dice=0.045580 pr_auc=0.032211
reports/evaluation/latest_cracks_run.md:25:expert_section=20/40 id=167 dice=0.036127 pr_auc=0.020081
reports/evaluation/latest_cracks_run.md:26:expert_section=21/40 id=168 dice=0.027757 pr_auc=0.019339
reports/evaluation/latest_cracks_run.md:27:expert_section=22/40 id=178 dice=0.036594 pr_auc=0.022646
reports/evaluation/latest_cracks_run.md:28:expert_section=23/40 id=193 dice=0.044079 pr_auc=0.033068
reports/evaluation/latest_cracks_run.md:29:expert_section=24/40 id=196 dice=0.047043 pr_auc=0.044112
reports/evaluation/latest_cracks_run.md:30:expert_section=25/40 id=197 dice=0.039303 pr_auc=0.019375
reports/evaluation/latest_cracks_run.md:31:expert_section=26/40 id=204 dice=0.043495 pr_auc=0.033815
reports/evaluation/latest_cracks_run.md:32:expert_section=27/40 id=213 dice=0.031014 pr_auc=0.031339
reports/evaluation/latest_cracks_run.md:33:expert_section=28/40 id=223 dice=0.028527 pr_auc=0.032726
reports/evaluation/latest_cracks_run.md:34:expert_section=29/40 id=231 dice=0.020176 pr_auc=0.022758
reports/evaluation/latest_cracks_run.md:35:expert_section=30/40 id=239 dice=0.015625 pr_auc=0.013562
reports/evaluation/latest_cracks_run.md:36:expert_section=31/40 id=250 dice=0.040682 pr_auc=0.029886
reports/evaluation/latest_cracks_run.md:37:expert_section=32/40 id=251 dice=0.020108 pr_auc=0.015500
reports/evaluation/latest_cracks_run.md:38:expert_section=33/40 id=256 dice=0.028635 pr_auc=0.031062
reports/evaluation/latest_cracks_run.md:39:expert_section=34/40 id=261 dice=0.024912 pr_auc=0.023240
reports/evaluation/latest_cracks_run.md:40:expert_section=35/40 id=262 dice=0.008059 pr_auc=0.011265
reports/evaluation/latest_cracks_run.md:41:expert_section=36/40 id=267 dice=0.009146 pr_auc=0.017539
reports/evaluation/latest_cracks_run.md:42:expert_section=37/40 id=277 dice=0.015902 pr_auc=0.022731
reports/evaluation/latest_cracks_run.md:43:expert_section=38/40 id=284 dice=0.010868 pr_auc=0.015782
reports/evaluation/latest_cracks_run.md:44:expert_section=39/40 id=287 dice=0.031914 pr_auc=0.027841
reports/evaluation/latest_cracks_run.md:45:expert_section=40/40 id=300 dice=0.014904 pr_auc=0.017871
reports/evaluation/latest_cracks_run.md:50:dice=0.035273
reports/evaluation/latest_cracks_run.md:51:iou=0.017953
reports/evaluation/latest_cracks_run.md:52:precision=0.024374
reports/evaluation/latest_cracks_run.md:53:recall=0.063801
reports/evaluation/latest_cracks_run.md:67:    "dice": 0.03527294979404324,
reports/evaluation/latest_cracks_run.md:70:    "iou": 0.01795310437159486,
reports/evaluation/latest_cracks_run.md:73:    "precision": 0.024374183477476077,
reports/evaluation/latest_cracks_run.md:74:    "recall": 0.06380131611553182,
reports/evaluation/latest_cracks_run.md:75:    "roc_auc_approx": 0.5010833013464665,
reports/evaluation/latest_cracks_run.md:113:section,valid_pixels,fault_pixels,threshold,dice,iou,precision,recall,specificity,balanced_accuracy,accuracy,mcc,pr_auc_approx,roc_auc_approx,tp,fp,fn,tn
reports/evaluation/p1_attention3d_caft_seed42_to_thebe_smoke_20261009/final_metrics.json:53:    "dice": 0.0,
reports/evaluation/p1_attention3d_caft_seed42_to_thebe_smoke_20261009/final_metrics.json:56:    "iou": 0.0,
reports/evaluation/p1_attention3d_caft_seed42_to_thebe_smoke_20261009/final_metrics.json:59:    "precision": 0.0,
reports/evaluation/p1_attention3d_caft_seed42_to_thebe_smoke_20261009/final_metrics.json:60:    "recall": 0.0,
reports/evaluation/p1_attention3d_caft_seed42_to_thebe_smoke_20261009/final_metrics.json:61:    "roc_auc_approx": 0.0,
reports/evaluation/p1_attention3d_caft_seed42_to_thebe_smoke9_20261009/final_metrics.json:53:    "dice": 0.10981343584034393,
reports/evaluation/p1_attention3d_caft_seed42_to_thebe_smoke9_20261009/final_metrics.json:56:    "iou": 0.05809661221942135,
reports/evaluation/p1_attention3d_caft_seed42_to_thebe_smoke9_20261009/final_metrics.json:59:    "precision": 0.08559098766493257,
reports/evaluation/p1_attention3d_caft_seed42_to_thebe_smoke9_20261009/final_metrics.json:60:    "recall": 0.15315731009142955,
reports/evaluation/p1_attention3d_caft_seed42_to_thebe_smoke9_20261009/final_metrics.json:61:    "roc_auc_approx": 0.5071055503375324,
reports/evaluation/p1_attention3d_caft_seed42_to_thebe_smoke9_20261009/final_metrics.json:89:    "dice": {
reports/evaluation/p1_attention3d_caft_seed42_to_thebe_smoke9_20261009/final_metrics.json:103:    "iou": {
reports/evaluation/p1_attention3d_caft_seed42_to_thebe_smoke9_20261009/final_metrics.json:131:    "precision": {
reports/evaluation/p1_attention3d_caft_seed42_to_thebe_smoke9_20261009/final_metrics.json:138:    "recall": {
reports/evaluation/p1_attention3d_caft_seed42_to_thebe_smoke9_20261009/final_metrics.json:145:    "roc_auc_approx": {
reports/evaluation/p1_attention3d_caft_seed42_to_thebe_smoke9_20261009/prediction_examples/example_01_x0000_y0000_z0640.npz: binary file matches (found "\0" byte around offset 5)
reports/evaluation/p1_attention3d_caft_seed42_to_thebe_smoke9_20261009/prediction_examples/example_02_x0000_y0000_z0768.npz: binary file matches (found "\0" byte around offset 5)
reports/evaluation/p1_attention3d_caft_seed42_to_thebe_smoke9_20261009/prediction_examples/example_03_x0000_y0000_z0896.npz: binary file matches (found "\0" byte around offset 5)
reports/evaluation/p1_attention3d_caft_seed42_to_thebe_smoke9_20261009/prediction_examples/example_04_x0000_y0000_z1024.npz: binary file matches (found "\0" byte around offset 5)
reports/evaluation/p1_attention3d_caft_seed42_to_thebe_smoke9_20261009/test_per_patch.csv:1:patch_id,raw_x_start,raw_x_stop,raw_y_start,raw_y_stop,raw_z_start,raw_z_stop,raw_voxels,valid_voxels,excluded_no_data_voxels,positive_labels_outside_valid_mask,normalization_mean,normalization_std,threshold,dice,iou,precision,recall,specificity,balanced_accuracy,accuracy,mcc,pr_auc_approx,roc_auc_approx,tp,fp,fn,tn,modified_hausdorff_voxels,bidirectional_chamfer_voxels,prediction_empty,target_empty,inference_seconds
reports/evaluation/p1_cracks_expert_seed42_20261009_134425/expert_per_section.csv:1:section,valid_pixels,certain_fault_pixels,threshold,dice,iou,precision,recall,specificity,balanced_accuracy,accuracy,mcc,pr_auc_approx,roc_auc_approx,tp,fp,fn,tn
reports/evaluation/p1_cracks_expert_seed42_20261009_134425/final_metrics.json:7:    "dice": 0.05755252130783045,
reports/evaluation/p1_cracks_expert_seed42_20261009_134425/final_metrics.json:10:    "iou": 0.029628868702581336,
reports/evaluation/p1_cracks_expert_seed42_20261009_134425/final_metrics.json:13:    "precision": 0.038205351398402906,
reports/evaluation/p1_cracks_expert_seed42_20261009_134425/final_metrics.json:14:    "recall": 0.1165973665973666,
reports/evaluation/p1_cracks_expert_seed42_20261009_134425/final_metrics.json:15:    "roc_auc_approx": 0.5417569783713032,
reports/evaluation/r100_readiness_20261005_101611/audit.txt:87:runs/loss_ablation_L1_weighted_bce_dice_seed42
reports/evaluation/r100_readiness_20261005_101611/audit.txt:128:  "dice": 0.8158076446363249,
reports/evaluation/r100_readiness_20261005_101611/audit.txt:129:  "iou": 0.6889148042049164,
reports/evaluation/r100_readiness_20261005_101611/audit.txt:130:  "precision": 0.8161029287143701,
reports/evaluation/r100_readiness_20261005_101611/audit.txt:131:  "recall": 0.8155125741616057,
reports/evaluation/r100_readiness_20261005_101611/audit.txt:137:  "roc_auc_approx": 0.9824618783754979,
reports/evaluation/sammed3d_source_commit.txt:1:f3de1fa10da98e46f49f176773d2b1e306ba131f
reports/evaluation/sammed3d_thebe_cpu_preflight.txt:4:  "sam_source_commit": "f3de1fa10da98e46f49f176773d2b1e306ba131f",
reports/evaluation/THEBE_EVALUATOR_EDIT_CONTEXT.md:5:- SHA-256: `25d6b9918c78146afdff48b4fa09db4fa2bf249778f14c827a0393c58a30404e`
reports/evaluation/THEBE_EVALUATOR_EDIT_CONTEXT.md:510:0741:         f"dice={aggregate_metrics['dice']:.6f}"
reports/evaluation/THEBE_EVALUATOR_EDIT_CONTEXT.md:513:0744:         f"iou={aggregate_metrics['iou']:.6f}"
reports/evaluation/THEBE_EVALUATOR_EDIT_CONTEXT.md:516:0747:         f"precision={aggregate_metrics['precision']:.6f}"
reports/evaluation/THEBE_EVALUATOR_EDIT_CONTEXT.md:519:0750:         f"recall={aggregate_metrics['recall']:.6f}"
reports/evaluation/THEBE_SMOKE_RESULT_20261005_094726.md:16:- Dice: `0.068389`
reports/evaluation/THEBE_SMOKE_RESULT_20261005_094726.md:17:- IoU: `0.035405`
reports/evaluation/THEBE_SMOKE_RESULT_20261005_094726.md:18:- Precision: `0.041877`
reports/evaluation/THEBE_SMOKE_RESULT_20261005_094726.md:19:- Recall: `0.186394`
reports/evaluation/THEBE_ZERO_PATCH_AUDIT.md:44:- Do not choose a behavior merely to improve Dice.
reports/EXPERIMENT_NAMING.md:20:| Loss Ablation L1 | Same synthetic data and architecture with weighted BCE plus Dice loss | Complete; no improvement over Baseline A |
reports/EXPERIMENT_NAMING.md:26:- Loss Ablation L1 run: `runs/loss_ablation_L1_weighted_bce_dice_seed42`
reports/EXPERIMENT_NAMING.md:27:- Loss Ablation L1 log: `reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log`
reports/EXPERIMENT_NAMING.md:31:The internal loss keys `b0_bce` and `b1_weighted_dice` are implementation identifiers preserved inside historical checkpoints and configurations. They are not formal experiment names.
reports/p1_thebe_setup.txt:178:        "dice",
reports/p1_thebe_setup.txt:179:        "iou",
reports/p1_thebe_setup.txt:180:        "precision",
reports/p1_thebe_setup.txt:181:        "recall",
reports/p1_thebe_setup.txt:187:        "roc_auc_approx",
reports/p1_thebe_setup.txt:538:            sample_indices = np.arange(
reports/p1_thebe_setup.txt:545:                & (sample_indices >= trace_first[..., None])
reports/p1_thebe_setup.txt:546:                & (sample_indices <= trace_last[..., None])
reports/p1_thebe_setup.txt:930:        f"dice={aggregate_metrics['dice']:.6f}"
reports/p1_thebe_setup.txt:933:        f"iou={aggregate_metrics['iou']:.6f}"
reports/p1_thebe_setup.txt:936:        f"precision={aggregate_metrics['precision']:.6f}"
reports/p1_thebe_setup.txt:939:        f"recall={aggregate_metrics['recall']:.6f}"
reports/p1_zero_shot_thebe_full_20261009_162704.log:79:dice=0.079128
reports/p1_zero_shot_thebe_full_20261009_162704.log:80:iou=0.041194
reports/p1_zero_shot_thebe_full_20261009_162704.log:81:precision=0.050344
reports/p1_zero_shot_thebe_full_20261009_162704.log:82:recall=0.184774
reports/p1_zero_shot_thebe_full_20261009_162704.log:90:dice               baseline=0.085861  P1=0.079128  change=-0.006733
reports/p1_zero_shot_thebe_full_20261009_162704.log:91:iou                baseline=0.044856  P1=0.041194  change=-0.003662
reports/p1_zero_shot_thebe_full_20261009_162704.log:92:precision          baseline=0.052094  P1=0.050344  change=-0.001750
reports/p1_zero_shot_thebe_full_20261009_162704.log:93:recall             baseline=0.244065  P1=0.184774  change=-0.059291
reports/p1_zero_shot_thebe_full_20261009_162704.log:96:roc_auc_approx     baseline=0.654087  P1=0.556206  change=-0.097881
reports/paper_attention3d_thebe_smoke.log:4:EPOCH 001 train_loss=0.503052 val_loss=0.493502 val_dice=0.005776 val_precision=0.030397 val_recall=0.003191 best=0.005776 elapsed_min=1.6
reports/paper_attention3d_thebe_smoke.log:5:TRAINING_COMPLETE best_val_dice=0.005776 checkpoint=runs/paper_attention3d_thebe_smoke_20261009_170246/best.pt
reports/paper_attention3d_thebe_supervised_seed42.log:7:EPOCH 001 train_loss=0.465636 val_loss=0.485576 val_dice=0.000000 val_precision=0.000000 val_recall=0.000000 best=0.000000 elapsed_min=8.4
reports/paper_attention3d_thebe_supervised_seed42.log:12:EPOCH 002 train_loss=0.467665 val_loss=0.482280 val_dice=0.000000 val_precision=0.000000 val_recall=0.000000 best=0.000000 elapsed_min=16.6
reports/paper_attention3d_thebe_supervised_seed42.log:17:EPOCH 003 train_loss=0.454657 val_loss=0.483242 val_dice=0.000000 val_precision=0.000000 val_recall=0.000000 best=0.000000 elapsed_min=24.9
reports/paper_attention3d_thebe_supervised_seed42.log:22:EPOCH 004 train_loss=0.460656 val_loss=0.480945 val_dice=0.000000 val_precision=0.000000 val_recall=0.000000 best=0.000000 elapsed_min=33.2
reports/paper_attention3d_thebe_supervised_seed42.log:27:EPOCH 005 train_loss=0.468298 val_loss=0.481879 val_dice=0.000000 val_precision=0.000000 val_recall=0.000000 best=0.000000 elapsed_min=41.5
reports/paper_attention3d_thebe_supervised_seed42.log:32:EPOCH 006 train_loss=0.458215 val_loss=0.481156 val_dice=0.000000 val_precision=0.000000 val_recall=0.000000 best=0.000000 elapsed_min=49.8
reports/paper_attention3d_thebe_supervised_seed42.log:37:EPOCH 007 train_loss=0.443859 val_loss=0.479730 val_dice=0.000000 val_precision=0.000000 val_recall=0.000000 best=0.000000 elapsed_min=58.0
reports/paper_attention3d_thebe_supervised_seed42.log:42:EPOCH 008 train_loss=0.458977 val_loss=0.476850 val_dice=0.002985 val_precision=0.287908 val_recall=0.001500 best=0.002985 elapsed_min=66.3
reports/paper_attention3d_thebe_supervised_seed42.log:47:EPOCH 009 train_loss=0.448518 val_loss=0.488524 val_dice=0.053982 val_precision=0.292612 val_recall=0.029734 best=0.053982 elapsed_min=74.6
reports/paper_attention3d_thebe_supervised_seed42.log:52:EPOCH 010 train_loss=0.465618 val_loss=0.481553 val_dice=0.000000 val_precision=0.000000 val_recall=0.000000 best=0.053982 elapsed_min=82.8
reports/paper_attention3d_thebe_supervised_seed42.log:57:EPOCH 011 train_loss=0.460839 val_loss=0.479369 val_dice=0.000000 val_precision=0.000000 val_recall=0.000000 best=0.053982 elapsed_min=91.1
reports/paper_attention3d_thebe_supervised_seed42.log:62:EPOCH 012 train_loss=0.439990 val_loss=0.480350 val_dice=0.185195 val_precision=0.142417 val_recall=0.264704 best=0.185195 elapsed_min=99.3
reports/paper_attention3d_thebe_supervised_seed42.log:67:EPOCH 013 train_loss=0.455732 val_loss=0.475154 val_dice=0.098971 val_precision=0.287062 val_recall=0.059793 best=0.185195 elapsed_min=107.5
reports/paper_attention3d_thebe_supervised_seed42.log:72:EPOCH 014 train_loss=0.449874 val_loss=0.475520 val_dice=0.030964 val_precision=0.235834 val_recall=0.016570 best=0.185195 elapsed_min=115.7
reports/paper_attention3d_thebe_supervised_seed42.log:77:EPOCH 015 train_loss=0.460372 val_loss=0.477283 val_dice=0.000489 val_precision=0.075385 val_recall=0.000245 best=0.185195 elapsed_min=123.9
reports/paper_attention3d_thebe_supervised_seed42.log:82:EPOCH 016 train_loss=0.444409 val_loss=0.475890 val_dice=0.056329 val_precision=0.368622 val_recall=0.030494 best=0.185195 elapsed_min=132.2
reports/paper_attention3d_thebe_supervised_seed42.log:87:EPOCH 017 train_loss=0.453968 val_loss=0.472956 val_dice=0.196479 val_precision=0.215728 val_recall=0.180384 best=0.196479 elapsed_min=140.4
reports/paper_attention3d_thebe_supervised_seed42.log:92:EPOCH 018 train_loss=0.443580 val_loss=0.469308 val_dice=0.208551 val_precision=0.172863 val_recall=0.262809 best=0.208551 elapsed_min=148.6
reports/paper_attention3d_thebe_supervised_seed42.log:97:EPOCH 019 train_loss=0.442774 val_loss=0.471064 val_dice=0.191173 val_precision=0.188870 val_recall=0.193533 best=0.208551 elapsed_min=156.8
reports/paper_attention3d_thebe_supervised_seed42.log:102:EPOCH 020 train_loss=0.443858 val_loss=0.472131 val_dice=0.000955 val_precision=0.094395 val_recall=0.000480 best=0.208551 elapsed_min=165.1
reports/paper_attention3d_thebe_supervised_seed42.log:107:EPOCH 021 train_loss=0.439147 val_loss=0.472728 val_dice=0.213008 val_precision=0.144140 val_recall=0.407897 best=0.213008 elapsed_min=173.4
reports/paper_attention3d_thebe_supervised_seed42.log:112:EPOCH 022 train_loss=0.445204 val_loss=0.466717 val_dice=0.160871 val_precision=0.278394 val_recall=0.113119 best=0.213008 elapsed_min=181.7
reports/paper_attention3d_thebe_supervised_seed42.log:117:EPOCH 023 train_loss=0.448208 val_loss=0.463638 val_dice=0.261559 val_precision=0.185300 val_recall=0.444483 best=0.261559 elapsed_min=189.9
reports/paper_attention3d_thebe_supervised_seed42.log:122:EPOCH 024 train_loss=0.445028 val_loss=0.478095 val_dice=0.159220 val_precision=0.090032 val_recall=0.687726 best=0.261559 elapsed_min=198.1
reports/paper_attention3d_thebe_supervised_seed42.log:127:EPOCH 025 train_loss=0.453727 val_loss=0.469634 val_dice=0.248726 val_precision=0.177809 val_recall=0.413744 best=0.261559 elapsed_min=206.3
reports/paper_attention3d_thebe_supervised_seed42.log:132:EPOCH 026 train_loss=0.469620 val_loss=0.468032 val_dice=0.177318 val_precision=0.427994 val_recall=0.111824 best=0.261559 elapsed_min=214.5
reports/paper_attention3d_thebe_supervised_seed42.log:137:EPOCH 027 train_loss=0.452048 val_loss=0.468749 val_dice=0.118957 val_precision=0.451581 val_recall=0.068501 best=0.261559 elapsed_min=222.7
reports/paper_attention3d_thebe_supervised_seed42.log:142:EPOCH 028 train_loss=0.456055 val_loss=0.463978 val_dice=0.136752 val_precision=0.489286 val_recall=0.079484 best=0.261559 elapsed_min=230.8
reports/paper_attention3d_thebe_supervised_seed42.log:147:EPOCH 029 train_loss=0.441141 val_loss=0.460873 val_dice=0.264254 val_precision=0.200075 val_recall=0.389052 best=0.264254 elapsed_min=239.1
reports/paper_attention3d_thebe_supervised_seed42.log:152:EPOCH 030 train_loss=0.443506 val_loss=0.460484 val_dice=0.233563 val_precision=0.143684 val_recall=0.623727 best=0.264254 elapsed_min=247.3
reports/paper_attention3d_thebe_supervised_seed42.log:157:EPOCH 031 train_loss=0.428732 val_loss=0.459202 val_dice=0.230887 val_precision=0.228150 val_recall=0.233690 best=0.264254 elapsed_min=255.5
reports/paper_attention3d_thebe_supervised_seed42.log:162:EPOCH 032 train_loss=0.426155 val_loss=0.458320 val_dice=0.252644 val_precision=0.287545 val_recall=0.225298 best=0.264254 elapsed_min=263.8
reports/paper_attention3d_thebe_supervised_seed42.log:167:EPOCH 033 train_loss=0.422742 val_loss=0.455358 val_dice=0.223501 val_precision=0.137322 val_recall=0.600115 best=0.264254 elapsed_min=272.0
reports/paper_attention3d_thebe_supervised_seed42.log:172:EPOCH 034 train_loss=0.440820 val_loss=0.451925 val_dice=0.280069 val_precision=0.194648 val_recall=0.499100 best=0.280069 elapsed_min=280.2
reports/paper_attention3d_thebe_supervised_seed42.log:177:EPOCH 035 train_loss=0.440077 val_loss=0.457766 val_dice=0.252387 val_precision=0.158295 val_recall=0.622267 best=0.280069 elapsed_min=288.4
reports/paper_attention3d_thebe_supervised_seed42.log:182:EPOCH 036 train_loss=0.420687 val_loss=0.465393 val_dice=0.213387 val_precision=0.126075 val_recall=0.694018 best=0.280069 elapsed_min=296.6
reports/paper_attention3d_thebe_supervised_seed42.log:187:EPOCH 037 train_loss=0.425067 val_loss=0.461357 val_dice=0.269066 val_precision=0.178778 val_recall=0.543603 best=0.280069 elapsed_min=304.8
reports/paper_attention3d_thebe_supervised_seed42.log:192:EPOCH 038 train_loss=0.442261 val_loss=0.452582 val_dice=0.337096 val_precision=0.338930 val_recall=0.335281 best=0.337096 elapsed_min=313.0
reports/paper_attention3d_thebe_supervised_seed42.log:197:EPOCH 039 train_loss=0.443558 val_loss=0.447198 val_dice=0.367370 val_precision=0.295324 val_recall=0.485911 best=0.367370 elapsed_min=321.2
reports/paper_attention3d_thebe_supervised_seed42.log:202:EPOCH 040 train_loss=0.430264 val_loss=0.455424 val_dice=0.344377 val_precision=0.425809 val_recall=0.289092 best=0.367370 elapsed_min=329.3
reports/paper_attention3d_thebe_supervised_seed42.log:207:EPOCH 041 train_loss=0.443416 val_loss=0.467378 val_dice=0.216479 val_precision=0.133304 val_recall=0.575673 best=0.367370 elapsed_min=337.5
reports/paper_attention3d_thebe_supervised_seed42.log:212:EPOCH 042 train_loss=0.440562 val_loss=0.457559 val_dice=0.276312 val_precision=0.269025 val_recall=0.284005 best=0.367370 elapsed_min=345.8
reports/paper_attention3d_thebe_supervised_seed42.log:217:EPOCH 043 train_loss=0.427471 val_loss=0.453988 val_dice=0.324958 val_precision=0.219173 val_recall=0.628123 best=0.367370 elapsed_min=354.0
reports/paper_attention3d_thebe_supervised_seed42.log:222:EPOCH 044 train_loss=0.432488 val_loss=0.450596 val_dice=0.241350 val_precision=0.142761 val_recall=0.780019 best=0.367370 elapsed_min=362.2
reports/paper_attention3d_thebe_supervised_seed42.log:227:EPOCH 045 train_loss=0.430064 val_loss=0.439875 val_dice=0.325035 val_precision=0.251513 val_recall=0.459298 best=0.367370 elapsed_min=370.3
reports/paper_attention3d_thebe_supervised_seed42.log:232:EPOCH 046 train_loss=0.405678 val_loss=0.447801 val_dice=0.352552 val_precision=0.265864 val_recall=0.523122 best=0.367370 elapsed_min=378.6
reports/paper_attention3d_thebe_supervised_seed42.log:237:EPOCH 047 train_loss=0.409205 val_loss=0.462000 val_dice=0.259344 val_precision=0.157762 val_recall=0.728288 best=0.367370 elapsed_min=386.8
reports/paper_attention3d_thebe_supervised_seed42.log:242:EPOCH 048 train_loss=0.420124 val_loss=0.452938 val_dice=0.290982 val_precision=0.183232 val_recall=0.706357 best=0.367370 elapsed_min=395.0
reports/paper_attention3d_thebe_supervised_seed42.log:247:EPOCH 049 train_loss=0.435563 val_loss=0.434204 val_dice=0.359942 val_precision=0.289417 val_recall=0.475913 best=0.367370 elapsed_min=403.2
reports/r100_launch_check_20261014_133445.txt:76:  "checkpoint_selection": "highest Dice at 0.5 on fixed validation subset",
reports/r100_launch_check_20261014_133445.txt:77:  "threshold_selection": "best Dice on complete validation volume with 2048 bins",
reports/r100_launch_check_20261014_133445.txt:84:  "old_selection": "Dice at threshold 0.5 on fixed 128 validation patches",
reports/r100_launch_check_20261014_133445.txt:86:  "why": "Near-zero Dice at 0.5 despite improving PR-AUC; final threshold remains full-validation only",
reports/r100_launch_check_20261014_133445.txt:87:  "best_existing_checkpoint_matches_new_selection": true,
reports/r100_launch_check_20261014_133445.txt:98:    "dice": 0.5454089882642815,
reports/r100_launch_check_20261014_133445.txt:99:    "iou": 0.3749569355673811,
reports/r100_launch_check_20261014_133445.txt:100:    "precision": 0.5279583306670493,
reports/r100_launch_check_20261014_133445.txt:101:    "recall": 0.5640526757282134,
reports/r100_launch_check_20261014_133445.txt:107:    "roc_auc_approx": 0.9541044799759987,
reports/r100_launch_check_20261014_133445.txt:147:    "dice": 0.5454089882642815,
reports/r100_launch_check_20261014_133445.txt:150:    "iou": 0.3749569355673811,
reports/r100_launch_check_20261014_133445.txt:153:    "precision": 0.5279583306670493,
reports/r100_launch_check_20261014_133445.txt:154:    "recall": 0.5640526757282134,
reports/r100_launch_check_20261014_133445.txt:155:    "roc_auc_approx": 0.9541044799759987,
reports/r100_launch_check_20261014_133445.txt:179:    "dice": 0.5429955056245461,
reports/r100_launch_check_20261014_133445.txt:182:    "iou": 0.37267936215756264,
reports/r100_launch_check_20261014_133445.txt:185:    "precision": 0.47191760787630943,
reports/r100_launch_check_20261014_133445.txt:186:    "recall": 0.6392808237987413,
reports/r100_launch_check_20261014_133445.txt:187:    "roc_auc_approx": 0.9604589545976385,
reports/r100_launch_check_20261014_133445.txt:215:    "dice": {
reports/r100_launch_check_20261014_133445.txt:229:    "iou": {
reports/r100_launch_check_20261014_133445.txt:257:    "precision": {
reports/r100_launch_check_20261014_133445.txt:264:    "recall": {
reports/r100_launch_check_20261014_133445.txt:271:    "roc_auc_approx": {
reports/r100_launch_check_20261014_133445.txt:575:            "threshold_selection": "best Dice on complete validation volume with 2048 bins",
reports/r100_launch_check_20261014_133445.txt:587:            best_saved = torch.load(best_path, map_location="cpu", weights_only=False)
reports/r100_launch_check_20261014_133445.txt:596:            previous_pr_auc_best = max(
reports/r100_launch_check_20261014_133445.txt:599:            if int(previous_pr_auc_best["epoch"]) != int(best_saved["epoch"]):
reports/r100_launch_check_20261014_133445.txt:601:                    "Best saved checkpoint is not the PR-AUC best from prior epochs; "
reports/r100_launch_check_20261014_133445.txt:606:                "old_selection": "Dice at threshold 0.5 on fixed 128 validation patches",
reports/r100_launch_check_20261014_133445.txt:608:                "why": "Near-zero Dice at 0.5 despite improving PR-AUC; final threshold remains full-validation only",
reports/r100_launch_check_20261014_133445.txt:609:                "best_existing_checkpoint_matches_new_selection": True,
reports/r100_launch_check_20261014_133445.txt:689:                f"val_dice={val_metrics['dice']:.6f} val_pr_auc={val_metrics['pr_auc_approx']:.6f} "
reports/r100_launch_check_20261014_133445.txt:699:        threshold = full_val_hist.best_dice_threshold()
reports/r100_launch_check_20261014_133445.txt:760:        for key in ("dice", "iou", "precision", "recall", "mcc", "pr_auc_approx"):
reports/r100_launch_check_20261014_133445.txt:1027:            "checkpoint_selection": "highest Dice at 0.5 on fixed validation subset",
reports/r100_launch_check_20261014_133445.txt:1028:            "threshold_selection": "best Dice on complete validation volume with 2048 bins",
reports/r100_launch_check_20261014_133445.txt:1034:        best_dice = -1.0
reports/r100_launch_check_20261014_133445.txt:1088:            if val_metrics["dice"] > best_dice:
reports/r100_launch_check_20261014_133445.txt:1089:                best_dice = val_metrics["dice"]
reports/r100_launch_check_20261014_133445.txt:1093:                f"val_dice={val_metrics['dice']:.6f} val_pr_auc={val_metrics['pr_auc_approx']:.6f} "
reports/r100_launch_check_20261014_133445.txt:1103:        threshold = full_val_hist.best_dice_threshold()
reports/r100_launch_check_20261014_133445.txt:1157:        for key in ("dice", "iou", "precision", "recall", "mcc", "pr_auc_approx"):
reports/training/baseline_A_smoke.log:4:/shared/home/khavarj/projects/fault_detection/.venv_train/lib/python3.13/site-packages/torch/autograd/graph.py:824: UserWarning: max_pool3d_with_indices_backward_cuda does not have a deterministic implementation, but you set 'torch.use_deterministic_algorithms(True, warn_only=True)'. You can file an issue at https://github.com/pytorch/pytorch/issues to help us prioritize adding deterministic support for this operation. (Triggered internally at /pytorch/aten/src/ATen/Context.cpp:93.)
reports/training/baseline_A_synthetic_bce_seed42.log:5:/shared/home/khavarj/projects/fault_detection/.venv_train/lib/python3.13/site-packages/torch/autograd/graph.py:824: UserWarning: max_pool3d_with_indices_backward_cuda does not have a deterministic implementation, but you set 'torch.use_deterministic_algorithms(True, warn_only=True)'. You can file an issue at https://github.com/pytorch/pytorch/issues to help us prioritize adding deterministic support for this operation. (Triggered internally at /pytorch/aten/src/ATen/Context.cpp:93.)
reports/training/baseline_A_synthetic_bce_seed42.log:11:epoch=001 loss=0.314965 val_dice=0.000000 val_iou=0.000000 val_pr_auc=0.076771 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:12:epoch=002 loss=0.254361 val_dice=0.000000 val_iou=0.000000 val_pr_auc=0.096252 minutes=0.30
reports/training/baseline_A_synthetic_bce_seed42.log:13:epoch=003 loss=0.238950 val_dice=0.000000 val_iou=0.000000 val_pr_auc=0.182016 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:14:epoch=004 loss=0.200252 val_dice=0.118262 val_iou=0.062847 val_pr_auc=0.390901 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:15:epoch=005 loss=0.168745 val_dice=0.398029 val_iou=0.248462 val_pr_auc=0.481942 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:16:epoch=006 loss=0.153221 val_dice=0.465434 val_iou=0.303300 val_pr_auc=0.539682 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:17:epoch=007 loss=0.141764 val_dice=0.497805 val_iou=0.331385 val_pr_auc=0.586533 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:18:epoch=008 loss=0.135450 val_dice=0.534810 val_iou=0.365011 val_pr_auc=0.613936 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:19:epoch=009 loss=0.128391 val_dice=0.600041 val_iou=0.428614 val_pr_auc=0.641996 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:20:epoch=010 loss=0.122253 val_dice=0.583450 val_iou=0.411881 val_pr_auc=0.643059 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:21:epoch=011 loss=0.118308 val_dice=0.619101 val_iou=0.448332 val_pr_auc=0.686354 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:22:epoch=012 loss=0.112667 val_dice=0.641208 val_iou=0.471895 val_pr_auc=0.700150 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:23:epoch=013 loss=0.109114 val_dice=0.633384 val_iou=0.463469 val_pr_auc=0.715915 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:24:epoch=014 loss=0.106602 val_dice=0.650868 val_iou=0.482435 val_pr_auc=0.711744 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:25:epoch=015 loss=0.102564 val_dice=0.666159 val_iou=0.499429 val_pr_auc=0.731226 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:26:epoch=016 loss=0.099363 val_dice=0.685561 val_iou=0.521562 val_pr_auc=0.750862 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:27:epoch=017 loss=0.097281 val_dice=0.687228 val_iou=0.523494 val_pr_auc=0.757492 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:28:epoch=018 loss=0.093142 val_dice=0.689824 val_iou=0.526513 val_pr_auc=0.765094 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:29:epoch=019 loss=0.093322 val_dice=0.693366 val_iou=0.530651 val_pr_auc=0.769579 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:30:epoch=020 loss=0.089892 val_dice=0.718609 val_iou=0.560804 val_pr_auc=0.786135 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:31:epoch=021 loss=0.088231 val_dice=0.706142 val_iou=0.545765 val_pr_auc=0.776918 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:32:epoch=022 loss=0.084756 val_dice=0.726282 val_iou=0.570206 val_pr_auc=0.795567 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:33:epoch=023 loss=0.083188 val_dice=0.718521 val_iou=0.560696 val_pr_auc=0.792467 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:34:epoch=024 loss=0.082507 val_dice=0.715403 val_iou=0.556909 val_pr_auc=0.802811 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:35:epoch=025 loss=0.080076 val_dice=0.735477 val_iou=0.581624 val_pr_auc=0.807542 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:36:epoch=026 loss=0.080869 val_dice=0.732477 val_iou=0.577881 val_pr_auc=0.802525 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:37:epoch=027 loss=0.077535 val_dice=0.737478 val_iou=0.584131 val_pr_auc=0.808070 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:38:epoch=028 loss=0.076718 val_dice=0.748352 val_iou=0.597894 val_pr_auc=0.820242 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:39:epoch=029 loss=0.075930 val_dice=0.745820 val_iou=0.594668 val_pr_auc=0.816438 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:40:epoch=030 loss=0.073748 val_dice=0.747954 val_iou=0.597386 val_pr_auc=0.821692 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:41:epoch=031 loss=0.074170 val_dice=0.745570 val_iou=0.594349 val_pr_auc=0.824247 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:42:epoch=032 loss=0.072066 val_dice=0.754636 val_iou=0.605956 val_pr_auc=0.832046 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:43:epoch=033 loss=0.070841 val_dice=0.757549 val_iou=0.609721 val_pr_auc=0.832721 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:44:epoch=034 loss=0.069383 val_dice=0.758069 val_iou=0.610395 val_pr_auc=0.834272 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:45:epoch=035 loss=0.068534 val_dice=0.760320 val_iou=0.613319 val_pr_auc=0.839178 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:46:epoch=036 loss=0.068438 val_dice=0.762048 val_iou=0.615572 val_pr_auc=0.835858 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:47:epoch=037 loss=0.066611 val_dice=0.760876 val_iou=0.614044 val_pr_auc=0.835267 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:48:epoch=038 loss=0.065514 val_dice=0.767338 val_iou=0.622505 val_pr_auc=0.840293 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:49:epoch=039 loss=0.065180 val_dice=0.763551 val_iou=0.617536 val_pr_auc=0.838623 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:50:epoch=040 loss=0.064552 val_dice=0.771029 val_iou=0.627378 val_pr_auc=0.841061 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:51:epoch=041 loss=0.064264 val_dice=0.771959 val_iou=0.628610 val_pr_auc=0.843271 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:52:epoch=042 loss=0.063743 val_dice=0.767876 val_iou=0.623213 val_pr_auc=0.846059 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:53:epoch=043 loss=0.061794 val_dice=0.772249 val_iou=0.628995 val_pr_auc=0.848326 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:54:epoch=044 loss=0.060327 val_dice=0.779469 val_iou=0.638632 val_pr_auc=0.852134 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:55:epoch=045 loss=0.059616 val_dice=0.785259 val_iou=0.646442 val_pr_auc=0.855085 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:56:epoch=046 loss=0.060070 val_dice=0.749423 val_iou=0.599261 val_pr_auc=0.829438 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:57:epoch=047 loss=0.059813 val_dice=0.775634 val_iou=0.633499 val_pr_auc=0.849559 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:58:epoch=048 loss=0.058218 val_dice=0.787302 val_iou=0.649215 val_pr_auc=0.859910 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:59:epoch=049 loss=0.057960 val_dice=0.790558 val_iou=0.653656 val_pr_auc=0.861377 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:5:/shared/home/khavarj/projects/fault_detection/.venv_train/lib/python3.13/site-packages/torch/autograd/graph.py:824: UserWarning: max_pool3d_with_indices_backward_cuda does not have a deterministic implementation, but you set 'torch.use_deterministic_algorithms(True, warn_only=True)'. You can file an issue at https://github.com/pytorch/pytorch/issues to help us prioritize adding deterministic support for this operation. (Triggered internally at /pytorch/aten/src/ATen/Context.cpp:93.)
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:11:epoch=001 loss=1.044174 val_dice=0.220347 val_iou=0.123815 val_pr_auc=0.148267 minutes=0.32
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:12:epoch=002 loss=0.861660 val_dice=0.330021 val_iou=0.197620 val_pr_auc=0.352460 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:13:epoch=003 loss=0.738569 val_dice=0.395203 val_iou=0.246264 val_pr_auc=0.445970 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:14:epoch=004 loss=0.669487 val_dice=0.445811 val_iou=0.286844 val_pr_auc=0.506100 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:15:epoch=005 loss=0.623482 val_dice=0.465448 val_iou=0.303312 val_pr_auc=0.544250 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:16:epoch=006 loss=0.581583 val_dice=0.524423 val_iou=0.355402 val_pr_auc=0.591176 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:17:epoch=007 loss=0.542672 val_dice=0.502238 val_iou=0.335326 val_pr_auc=0.626267 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:18:epoch=008 loss=0.501275 val_dice=0.549318 val_iou=0.378662 val_pr_auc=0.664116 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:19:epoch=009 loss=0.463011 val_dice=0.595464 val_iou=0.423958 val_pr_auc=0.699814 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:20:epoch=010 loss=0.438031 val_dice=0.629139 val_iou=0.458937 val_pr_auc=0.719178 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:21:epoch=011 loss=0.414671 val_dice=0.645080 val_iou=0.476102 val_pr_auc=0.733999 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:22:epoch=012 loss=0.398844 val_dice=0.607199 val_iou=0.435955 val_pr_auc=0.718977 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:23:epoch=013 loss=0.377859 val_dice=0.631336 val_iou=0.461280 val_pr_auc=0.757730 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:24:epoch=014 loss=0.364058 val_dice=0.675847 val_iou=0.510400 val_pr_auc=0.768168 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:25:epoch=015 loss=0.352412 val_dice=0.654198 val_iou=0.486103 val_pr_auc=0.759199 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:26:epoch=016 loss=0.342353 val_dice=0.688899 val_iou=0.525436 val_pr_auc=0.774911 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:27:epoch=017 loss=0.335509 val_dice=0.678364 val_iou=0.513276 val_pr_auc=0.782113 minutes=0.32
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:28:epoch=018 loss=0.322418 val_dice=0.682413 val_iou=0.517926 val_pr_auc=0.791560 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:29:epoch=019 loss=0.317725 val_dice=0.684473 val_iou=0.520303 val_pr_auc=0.783781 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:30:epoch=020 loss=0.312603 val_dice=0.699316 val_iou=0.537653 val_pr_auc=0.800032 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:31:epoch=021 loss=0.304364 val_dice=0.666135 val_iou=0.499402 val_pr_auc=0.798243 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:32:epoch=022 loss=0.296087 val_dice=0.683697 val_iou=0.519407 val_pr_auc=0.792827 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:33:epoch=023 loss=0.289767 val_dice=0.680265 val_iou=0.515455 val_pr_auc=0.790324 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:34:epoch=024 loss=0.283622 val_dice=0.724217 val_iou=0.567665 val_pr_auc=0.819983 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:35:epoch=025 loss=0.276947 val_dice=0.714994 val_iou=0.556413 val_pr_auc=0.817862 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:36:epoch=026 loss=0.276903 val_dice=0.717139 val_iou=0.559015 val_pr_auc=0.820812 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:37:epoch=027 loss=0.265155 val_dice=0.725327 val_iou=0.569030 val_pr_auc=0.814139 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:38:epoch=028 loss=0.265455 val_dice=0.708698 val_iou=0.548824 val_pr_auc=0.816097 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:39:epoch=029 loss=0.260097 val_dice=0.722187 val_iou=0.565174 val_pr_auc=0.826339 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:40:epoch=030 loss=0.253136 val_dice=0.708558 val_iou=0.548656 val_pr_auc=0.821485 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:41:epoch=031 loss=0.246760 val_dice=0.742100 val_iou=0.589952 val_pr_auc=0.830931 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:42:epoch=032 loss=0.245331 val_dice=0.718020 val_iou=0.560087 val_pr_auc=0.831030 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:43:epoch=033 loss=0.239755 val_dice=0.715431 val_iou=0.556942 val_pr_auc=0.831187 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:44:epoch=034 loss=0.237105 val_dice=0.742207 val_iou=0.590087 val_pr_auc=0.832874 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:45:epoch=035 loss=0.235641 val_dice=0.717694 val_iou=0.559690 val_pr_auc=0.823459 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:46:epoch=036 loss=0.228823 val_dice=0.731766 val_iou=0.576995 val_pr_auc=0.839220 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:47:epoch=037 loss=0.227346 val_dice=0.743963 val_iou=0.592310 val_pr_auc=0.834489 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:48:epoch=038 loss=0.226099 val_dice=0.749641 val_iou=0.599541 val_pr_auc=0.836799 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:49:epoch=039 loss=0.221457 val_dice=0.743303 val_iou=0.591474 val_pr_auc=0.845124 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:50:epoch=040 loss=0.218223 val_dice=0.723296 val_iou=0.566534 val_pr_auc=0.840595 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:51:epoch=041 loss=0.219299 val_dice=0.749194 val_iou=0.598969 val_pr_auc=0.842864 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:52:epoch=042 loss=0.217124 val_dice=0.745649 val_iou=0.594450 val_pr_auc=0.841899 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:53:epoch=043 loss=0.211047 val_dice=0.738224 val_iou=0.585067 val_pr_auc=0.837245 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:54:epoch=044 loss=0.210547 val_dice=0.742338 val_iou=0.590252 val_pr_auc=0.845773 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:55:epoch=045 loss=0.205635 val_dice=0.736547 val_iou=0.582963 val_pr_auc=0.847457 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:56:epoch=046 loss=0.208107 val_dice=0.757053 val_iou=0.609079 val_pr_auc=0.851818 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:57:epoch=047 loss=0.204230 val_dice=0.767097 val_iou=0.622187 val_pr_auc=0.856076 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:58:epoch=048 loss=0.198154 val_dice=0.756199 val_iou=0.607974 val_pr_auc=0.851964 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:59:epoch=049 loss=0.203914 val_dice=0.752893 val_iou=0.603711 val_pr_auc=0.846729 minutes=0.31
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:7:EPOCH 001 train_loss=0.465645 val_loss=0.485600 val_dice=0.000000 val_precision=0.000000 val_recall=0.000000 best=0.000000 elapsed_min=8.5
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:12:EPOCH 002 train_loss=0.467679 val_loss=0.482254 val_dice=0.000000 val_precision=0.000000 val_recall=0.000000 best=0.000000 elapsed_min=17.0
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:17:EPOCH 003 train_loss=0.454671 val_loss=0.483168 val_dice=0.000000 val_precision=0.000000 val_recall=0.000000 best=0.000000 elapsed_min=25.5
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:22:EPOCH 004 train_loss=0.460464 val_loss=0.481467 val_dice=0.000000 val_precision=0.000000 val_recall=0.000000 best=0.000000 elapsed_min=34.0
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:27:EPOCH 005 train_loss=0.467914 val_loss=0.481631 val_dice=0.000000 val_precision=0.000000 val_recall=0.000000 best=0.000000 elapsed_min=42.5
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:32:EPOCH 006 train_loss=0.461141 val_loss=0.484556 val_dice=0.000000 val_precision=0.000000 val_recall=0.000000 best=0.000000 elapsed_min=51.0
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:37:EPOCH 007 train_loss=0.446475 val_loss=0.481680 val_dice=0.047903 val_precision=0.161964 val_recall=0.028108 best=0.047903 elapsed_min=59.5
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:42:EPOCH 008 train_loss=0.459167 val_loss=0.479956 val_dice=0.000000 val_precision=0.000000 val_recall=0.000000 best=0.047903 elapsed_min=67.9
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:47:EPOCH 009 train_loss=0.451511 val_loss=0.476000 val_dice=0.149590 val_precision=0.106510 val_recall=0.251190 best=0.149590 elapsed_min=76.4
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:52:EPOCH 010 train_loss=0.457132 val_loss=0.476811 val_dice=0.099883 val_precision=0.186243 val_recall=0.068240 best=0.149590 elapsed_min=84.9
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:57:EPOCH 011 train_loss=0.459216 val_loss=0.476008 val_dice=0.016839 val_precision=0.326531 val_recall=0.008643 best=0.149590 elapsed_min=93.4
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:62:EPOCH 012 train_loss=0.434350 val_loss=0.475353 val_dice=0.180964 val_precision=0.120576 val_recall=0.362529 best=0.180964 elapsed_min=101.9
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:67:EPOCH 013 train_loss=0.450595 val_loss=0.472315 val_dice=0.150950 val_precision=0.159644 val_recall=0.143153 best=0.180964 elapsed_min=110.4
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:72:EPOCH 014 train_loss=0.444658 val_loss=0.470842 val_dice=0.184008 val_precision=0.189435 val_recall=0.178884 best=0.184008 elapsed_min=118.9
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:77:EPOCH 015 train_loss=0.455812 val_loss=0.472264 val_dice=0.151737 val_precision=0.347372 val_recall=0.097069 best=0.184008 elapsed_min=127.4
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:82:EPOCH 016 train_loss=0.439112 val_loss=0.474909 val_dice=0.090741 val_precision=0.263758 val_recall=0.054796 best=0.184008 elapsed_min=135.9
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:87:EPOCH 017 train_loss=0.455355 val_loss=0.472741 val_dice=0.075697 val_precision=0.446105 val_recall=0.041357 best=0.184008 elapsed_min=144.4
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:92:EPOCH 018 train_loss=0.442842 val_loss=0.471527 val_dice=0.238118 val_precision=0.212533 val_recall=0.270706 best=0.238118 elapsed_min=152.9
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:97:EPOCH 019 train_loss=0.441880 val_loss=0.470957 val_dice=0.212381 val_precision=0.284035 val_recall=0.169596 best=0.238118 elapsed_min=161.3
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:102:EPOCH 020 train_loss=0.442190 val_loss=0.465484 val_dice=0.241313 val_precision=0.179586 val_recall=0.367695 best=0.241313 elapsed_min=169.8
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:107:EPOCH 021 train_loss=0.435344 val_loss=0.475311 val_dice=0.158431 val_precision=0.103035 val_recall=0.342663 best=0.241313 elapsed_min=178.3
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:112:EPOCH 022 train_loss=0.442537 val_loss=0.468002 val_dice=0.194564 val_precision=0.130548 val_recall=0.381770 best=0.241313 elapsed_min=186.8
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:117:EPOCH 023 train_loss=0.449759 val_loss=0.464639 val_dice=0.211203 val_precision=0.228455 val_recall=0.196374 best=0.241313 elapsed_min=195.3
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:122:EPOCH 024 train_loss=0.438226 val_loss=0.470474 val_dice=0.206551 val_precision=0.144007 val_recall=0.365130 best=0.241313 elapsed_min=203.7
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:127:EPOCH 025 train_loss=0.450425 val_loss=0.471324 val_dice=0.193218 val_precision=0.122883 val_recall=0.451846 best=0.241313 elapsed_min=212.2
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:132:EPOCH 026 train_loss=0.463187 val_loss=0.463039 val_dice=0.181876 val_precision=0.325241 val_recall=0.126233 best=0.241313 elapsed_min=220.7
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:137:EPOCH 027 train_loss=0.449494 val_loss=0.458801 val_dice=0.275165 val_precision=0.242287 val_recall=0.318366 best=0.275165 elapsed_min=229.2
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:142:EPOCH 028 train_loss=0.451639 val_loss=0.459566 val_dice=0.261107 val_precision=0.231727 val_recall=0.299020 best=0.275165 elapsed_min=237.7
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:147:EPOCH 029 train_loss=0.439577 val_loss=0.461916 val_dice=0.225784 val_precision=0.160429 val_recall=0.380989 best=0.275165 elapsed_min=246.1
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:152:EPOCH 030 train_loss=0.440820 val_loss=0.463329 val_dice=0.220092 val_precision=0.153135 val_recall=0.391092 best=0.275165 elapsed_min=254.6
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:157:EPOCH 031 train_loss=0.433343 val_loss=0.464132 val_dice=0.186347 val_precision=0.178289 val_recall=0.195169 best=0.275165 elapsed_min=263.1
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:162:EPOCH 032 train_loss=0.434500 val_loss=0.470934 val_dice=0.105899 val_precision=0.194278 val_recall=0.072787 best=0.275165 elapsed_min=271.5
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:167:EPOCH 033 train_loss=0.433713 val_loss=0.463354 val_dice=0.214576 val_precision=0.149040 val_recall=0.382985 best=0.275165 elapsed_min=280.0
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:172:EPOCH 034 train_loss=0.441082 val_loss=0.460800 val_dice=0.230288 val_precision=0.169466 val_recall=0.359208 best=0.275165 elapsed_min=288.5
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:177:EPOCH 035 train_loss=0.438050 val_loss=0.461329 val_dice=0.255506 val_precision=0.181839 val_recall=0.429514 best=0.275165 elapsed_min=297.0
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:182:EPOCH 036 train_loss=0.420644 val_loss=0.466383 val_dice=0.239369 val_precision=0.155263 val_recall=0.522302 best=0.275165 elapsed_min=305.5
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:187:EPOCH 037 train_loss=0.420247 val_loss=0.465001 val_dice=0.229943 val_precision=0.149787 val_recall=0.494643 best=0.275165 elapsed_min=313.9
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:192:EPOCH 038 train_loss=0.442221 val_loss=0.454498 val_dice=0.167754 val_precision=0.184183 val_recall=0.154016 best=0.275165 elapsed_min=322.4
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:197:EPOCH 039 train_loss=0.443751 val_loss=0.450430 val_dice=0.249975 val_precision=0.183709 val_recall=0.391022 best=0.275165 elapsed_min=330.9
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:202:EPOCH 040 train_loss=0.430550 val_loss=0.452433 val_dice=0.271401 val_precision=0.283026 val_recall=0.260693 best=0.275165 elapsed_min=339.3
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:207:EPOCH 041 train_loss=0.443002 val_loss=0.453387 val_dice=0.226092 val_precision=0.202020 val_recall=0.256677 best=0.275165 elapsed_min=347.8
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:212:EPOCH 042 train_loss=0.437746 val_loss=0.446105 val_dice=0.291305 val_precision=0.251279 val_recall=0.346499 best=0.291305 elapsed_min=356.5
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:217:EPOCH 043 train_loss=0.427448 val_loss=0.451607 val_dice=0.217372 val_precision=0.142659 val_recall=0.456392 best=0.291305 elapsed_min=365.0
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:222:EPOCH 044 train_loss=0.421100 val_loss=0.439496 val_dice=0.308680 val_precision=0.245374 val_recall=0.416010 best=0.308680 elapsed_min=376.3
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:227:EPOCH 045 train_loss=0.435031 val_loss=0.462024 val_dice=0.243413 val_precision=0.164914 val_recall=0.464529 best=0.308680 elapsed_min=389.1
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:232:EPOCH 046 train_loss=0.421245 val_loss=0.459163 val_dice=0.252154 val_precision=0.167321 val_recall=0.511478 best=0.308680 elapsed_min=398.9
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:237:EPOCH 047 train_loss=0.410241 val_loss=0.454737 val_dice=0.276184 val_precision=0.205788 val_recall=0.419786 best=0.308680 elapsed_min=407.4
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:242:EPOCH 048 train_loss=0.427201 val_loss=0.450336 val_dice=0.269914 val_precision=0.194638 val_recall=0.440137 best=0.308680 elapsed_min=415.9
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:247:EPOCH 049 train_loss=0.442781 val_loss=0.451658 val_dice=0.266500 val_precision=0.257195 val_recall=0.276503 best=0.308680 elapsed_min=424.4
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:252:EPOCH 050 train_loss=0.419376 val_loss=0.457823 val_dice=0.217707 val_precision=0.135386 val_recall=0.555452 best=0.308680 elapsed_min=432.8
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:2:RESUME epoch=50 best_val_dice=0.367370
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:9:EPOCH 050 train_loss=0.416314 val_loss=0.453715 val_dice=0.286637 val_precision=0.180658 val_recall=0.693418 best=0.367370 elapsed_min=8.3
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:14:EPOCH 051 train_loss=0.453673 val_loss=0.453172 val_dice=0.262730 val_precision=0.211600 val_recall=0.346444 best=0.367370 elapsed_min=16.5
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:19:EPOCH 052 train_loss=0.409309 val_loss=0.442612 val_dice=0.376027 val_precision=0.282215 val_recall=0.563264 best=0.376027 elapsed_min=24.7
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:24:EPOCH 053 train_loss=0.439335 val_loss=0.443985 val_dice=0.380571 val_precision=0.424110 val_recall=0.345139 best=0.380571 elapsed_min=32.9
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:29:EPOCH 054 train_loss=0.447276 val_loss=0.445041 val_dice=0.425384 val_precision=0.370854 val_recall=0.498715 best=0.425384 elapsed_min=41.1
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:34:EPOCH 055 train_loss=0.427699 val_loss=0.451420 val_dice=0.350257 val_precision=0.260424 val_recall=0.534700 best=0.425384 elapsed_min=49.3
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:39:EPOCH 056 train_loss=0.426692 val_loss=0.475709 val_dice=0.190790 val_precision=0.108650 val_recall=0.781920 best=0.425384 elapsed_min=57.5
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:44:EPOCH 057 train_loss=0.457442 val_loss=0.456812 val_dice=0.308432 val_precision=0.303325 val_recall=0.313714 best=0.425384 elapsed_min=65.8
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:49:EPOCH 058 train_loss=0.429706 val_loss=0.442806 val_dice=0.347959 val_precision=0.245207 val_recall=0.598945 best=0.425384 elapsed_min=74.0
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:54:EPOCH 059 train_loss=0.429686 val_loss=0.434063 val_dice=0.409925 val_precision=0.329511 val_recall=0.542258 best=0.425384 elapsed_min=82.2
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:59:EPOCH 060 train_loss=0.411757 val_loss=0.438704 val_dice=0.416119 val_precision=0.316983 val_recall=0.605482 best=0.425384 elapsed_min=90.4
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:64:EPOCH 061 train_loss=0.429466 val_loss=0.449119 val_dice=0.349713 val_precision=0.268617 val_recall=0.500950 best=0.425384 elapsed_min=98.6
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:69:EPOCH 062 train_loss=0.441227 val_loss=0.429128 val_dice=0.423200 val_precision=0.365928 val_recall=0.501726 best=0.425384 elapsed_min=106.8
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:74:EPOCH 063 train_loss=0.426974 val_loss=0.442482 val_dice=0.365410 val_precision=0.271615 val_recall=0.558152 best=0.425384 elapsed_min=115.0
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:79:EPOCH 064 train_loss=0.409294 val_loss=0.429752 val_dice=0.489137 val_precision=0.454637 val_recall=0.529304 best=0.489137 elapsed_min=123.2
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:84:EPOCH 065 train_loss=0.429007 val_loss=0.425511 val_dice=0.425216 val_precision=0.387947 val_recall=0.470406 best=0.489137 elapsed_min=131.4
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:89:EPOCH 066 train_loss=0.427213 val_loss=0.427513 val_dice=0.375063 val_precision=0.261715 val_recall=0.661603 best=0.489137 elapsed_min=139.6
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:94:EPOCH 067 train_loss=0.428950 val_loss=0.422227 val_dice=0.282580 val_precision=0.173813 val_recall=0.755102 best=0.489137 elapsed_min=147.8
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:99:EPOCH 068 train_loss=0.444036 val_loss=0.415415 val_dice=0.481035 val_precision=0.504100 val_recall=0.459988 best=0.489137 elapsed_min=156.0
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:104:EPOCH 069 train_loss=0.395316 val_loss=0.410463 val_dice=0.443858 val_precision=0.354308 val_recall=0.593983 best=0.489137 elapsed_min=164.2
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:109:EPOCH 070 train_loss=0.408099 val_loss=0.431831 val_dice=0.539004 val_precision=0.548685 val_recall=0.529659 best=0.539004 elapsed_min=172.4
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:114:EPOCH 071 train_loss=0.413183 val_loss=0.419119 val_dice=0.392210 val_precision=0.275673 val_recall=0.679434 best=0.539004 elapsed_min=180.7
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:119:EPOCH 072 train_loss=0.443808 val_loss=0.438151 val_dice=0.445767 val_precision=0.398119 val_recall=0.506372 best=0.539004 elapsed_min=188.8
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:124:EPOCH 073 train_loss=0.401304 val_loss=0.435013 val_dice=0.434314 val_precision=0.332644 val_recall=0.625493 best=0.539004 elapsed_min=197.0
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:129:EPOCH 074 train_loss=0.412175 val_loss=nan val_dice=0.429887 val_precision=0.315779 val_recall=0.673122 best=0.539004 elapsed_min=205.2
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:134:EPOCH 075 train_loss=nan val_loss=nan val_dice=0.267436 val_precision=0.199014 val_recall=0.407552 best=0.539004 elapsed_min=213.2
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:139:EPOCH 076 train_loss=nan val_loss=nan val_dice=0.267436 val_precision=0.199014 val_recall=0.407552 best=0.539004 elapsed_min=221.2
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:144:EPOCH 077 train_loss=nan val_loss=nan val_dice=0.257658 val_precision=0.186943 val_recall=0.414424 best=0.539004 elapsed_min=229.1
reports/training/r100_fp16_3seed_queue_20261014_150435.log:4:PASS seed=42 validation_dice=0.544072
reports/training/r100_fp16_3seed_queue_20261014_150435.log:6:PASS seed=43 validation_dice=0.569856
reports/training/r100_fp16_3seed_queue_20261014_150435.log:8:PASS seed=44 validation_dice=0.572980
reports/training/r100_fp16_3seed_queue_20261014_150435.log:9:THREE SEEDS COMPLETE validation Dice mean=0.562302 sample_SD=0.015865; no test evaluation
reports/training/R100_thebe_seed42_20261005_102737.log:5:/shared/home/khavarj/projects/fault_detection/.venv_train/lib/python3.13/site-packages/torch/autograd/graph.py:824: UserWarning: max_pool3d_with_indices_backward_cuda does not have a deterministic implementation, but you set 'torch.use_deterministic_algorithms(True, warn_only=True)'. You can file an issue at https://github.com/pytorch/pytorch/issues to help us prioritize adding deterministic support for this operation. (Triggered internally at /pytorch/aten/src/ATen/Context.cpp:93.)
reports/training/R100_thebe_seed42_20261005_102737.log:12:epoch=001/100 loss=0.211608 val_dice=0.000006 val_pr_auc=0.034823 minutes=3.26
reports/training/R100_thebe_seed42_20261005_102737.log:14:epoch=002/100 loss=0.131591 val_dice=0.000001 val_pr_auc=0.039528 minutes=3.33
reports/training/R100_thebe_seed42_20261005_102737.log:16:epoch=003/100 loss=0.105220 val_dice=0.000001 val_pr_auc=0.043710 minutes=3.23
reports/training/R100_thebe_seed42_20261005_102737.log:18:epoch=004/100 loss=0.101674 val_dice=0.000000 val_pr_auc=0.043505 minutes=3.32
reports/training/R100_thebe_seed42_20261005_102737.log:20:epoch=005/100 loss=0.113378 val_dice=0.000000 val_pr_auc=0.038386 minutes=3.04
reports/training/R100_thebe_seed42_20261005_102737.log:22:epoch=006/100 loss=0.102869 val_dice=0.000000 val_pr_auc=0.047210 minutes=3.22
reports/training/R100_thebe_seed42_20261005_102737.log:24:epoch=007/100 loss=0.106725 val_dice=0.000000 val_pr_auc=0.049760 minutes=3.20
reports/training/R100_thebe_seed42_20261005_102737.log:26:epoch=008/100 loss=0.096674 val_dice=0.000000 val_pr_auc=0.048672 minutes=3.13
reports/training/R100_thebe_seed42_20261005_102737.log:28:epoch=009/100 loss=0.099541 val_dice=0.000000 val_pr_auc=0.043619 minutes=3.24
reports/training/R100_thebe_seed42_20261005_102737.log:30:epoch=010/100 loss=0.107934 val_dice=0.000000 val_pr_auc=0.055916 minutes=3.05
reports/training/R100_thebe_seed42_20261005_102737.log:32:epoch=011/100 loss=0.099936 val_dice=0.000000 val_pr_auc=0.061880 minutes=3.10
reports/training/R100_thebe_seed42_20261005_102737.log:34:epoch=012/100 loss=0.102164 val_dice=0.000000 val_pr_auc=0.049965 minutes=3.15
reports/training/R100_thebe_seed42_20261005_102737.log:36:epoch=013/100 loss=0.109964 val_dice=0.000000 val_pr_auc=0.061470 minutes=3.00
reports/training/R100_thebe_seed42_20261005_102737.log:38:epoch=014/100 loss=0.096900 val_dice=0.000000 val_pr_auc=0.089677 minutes=3.07
reports/training/R100_thebe_seed42_20261005_102737.log:40:epoch=015/100 loss=0.089464 val_dice=0.000000 val_pr_auc=0.117684 minutes=3.21
reports/training/R100_thebe_seed42_20261005_102737.log:42:epoch=016/100 loss=0.088687 val_dice=0.000000 val_pr_auc=0.107323 minutes=3.15
reports/training/R100_thebe_seed42_20261005_102737.log:44:epoch=017/100 loss=0.083734 val_dice=0.000000 val_pr_auc=0.135083 minutes=3.13
reports/training/R100_thebe_seed42_20261005_102737.log:46:epoch=018/100 loss=0.087998 val_dice=0.000000 val_pr_auc=0.171241 minutes=3.32
reports/training/R100_thebe_seed42_20261005_102737.log:48:epoch=019/100 loss=0.090926 val_dice=0.000000 val_pr_auc=0.184733 minutes=3.11
reports/training/R100_thebe_seed42_20261005_102737.log:50:epoch=020/100 loss=0.077623 val_dice=0.000000 val_pr_auc=0.207758 minutes=3.15
reports/training/R100_thebe_seed42_20261005_102737.log:52:epoch=021/100 loss=0.073180 val_dice=0.000013 val_pr_auc=0.213077 minutes=3.13
reports/training/R100_thebe_seed42_20261005_102737.log:54:epoch=022/100 loss=0.077549 val_dice=0.000690 val_pr_auc=0.212709 minutes=3.08
reports/training/R100_thebe_seed42_20261005_102737.log:56:epoch=023/100 loss=0.080129 val_dice=0.001580 val_pr_auc=0.250377 minutes=3.05
reports/training/R100_thebe_seed42_resume_20261005_131346.log:6:/shared/home/khavarj/projects/fault_detection/.venv_train/lib/python3.13/site-packages/torch/autograd/graph.py:824: UserWarning: max_pool3d_with_indices_backward_cuda does not have a deterministic implementation, but you set 'torch.use_deterministic_algorithms(True, warn_only=True)'. You can file an issue at https://github.com/pytorch/pytorch/issues to help us prioritize adding deterministic support for this operation. (Triggered internally at /pytorch/aten/src/ATen/Context.cpp:93.)
reports/training/R100_thebe_seed42_resume_20261005_131346.log:13:epoch=024/100 loss=0.078920 val_dice=0.001420 val_pr_auc=0.236420 minutes=3.32
reports/training/R100_thebe_seed42_resume_20261005_131346.log:15:epoch=025/100 loss=0.065565 val_dice=0.002473 val_pr_auc=0.260316 minutes=3.20
reports/training/R100_thebe_seed42_resume_20261005_131346.log:17:epoch=026/100 loss=0.068080 val_dice=0.003456 val_pr_auc=0.263557 minutes=3.25
reports/training/R100_thebe_seed42_resume_20261005_131346.log:19:epoch=027/100 loss=0.080750 val_dice=0.011536 val_pr_auc=0.259436 minutes=3.12
reports/training/R100_thebe_seed42_resume_20261005_131346.log:21:epoch=028/100 loss=0.075161 val_dice=0.018024 val_pr_auc=0.297481 minutes=3.05
reports/training/R100_thebe_seed42_resume_20261005_131346.log:23:epoch=029/100 loss=0.084217 val_dice=0.048370 val_pr_auc=0.295427 minutes=3.27
reports/training/R100_thebe_seed42_resume_20261005_131346.log:25:epoch=030/100 loss=0.069108 val_dice=0.027934 val_pr_auc=0.322924 minutes=3.16
reports/training/R100_thebe_seed42_resume_20261005_131346.log:27:epoch=031/100 loss=0.078519 val_dice=0.077669 val_pr_auc=0.336544 minutes=3.02
reports/training/R100_thebe_seed42_resume_20261005_131346.log:29:epoch=032/100 loss=0.062892 val_dice=0.304055 val_pr_auc=0.336719 minutes=3.36
reports/training/R100_thebe_seed42_resume_20261005_131346.log:31:epoch=033/100 loss=0.072173 val_dice=0.149602 val_pr_auc=0.348334 minutes=3.39
reports/training/R100_thebe_seed42_resume_20261005_131346.log:33:epoch=034/100 loss=0.070201 val_dice=0.174907 val_pr_auc=0.342185 minutes=3.24
reports/training/R100_thebe_seed42_resume_20261005_131346.log:35:epoch=035/100 loss=0.073527 val_dice=0.148241 val_pr_auc=0.369592 minutes=3.27
reports/training/R100_thebe_seed42_resume_20261005_131346.log:37:epoch=036/100 loss=0.069229 val_dice=0.193048 val_pr_auc=0.379670 minutes=3.25
reports/training/R100_thebe_seed42_resume_20261005_131346.log:39:epoch=037/100 loss=0.063905 val_dice=0.006665 val_pr_auc=0.330679 minutes=3.15
reports/training/R100_thebe_seed42_resume_20261005_131346.log:41:epoch=038/100 loss=0.080337 val_dice=0.244056 val_pr_auc=0.374059 minutes=3.23
reports/training/R100_thebe_seed42_resume_20261005_131346.log:43:epoch=039/100 loss=0.066486 val_dice=0.255052 val_pr_auc=0.404267 minutes=3.12
reports/training/R100_thebe_seed42_resume_20261005_131346.log:45:epoch=040/100 loss=0.065938 val_dice=0.210433 val_pr_auc=0.382206 minutes=3.17
reports/training/R100_thebe_seed42_resume_20261005_131346.log:47:epoch=041/100 loss=0.062026 val_dice=0.407483 val_pr_auc=0.373383 minutes=3.09
reports/training/R100_thebe_seed42_resume_20261005_131346.log:49:epoch=042/100 loss=0.075279 val_dice=0.123915 val_pr_auc=0.388560 minutes=3.06
reports/training/R100_thebe_seed42_resume_20261005_131346.log:51:epoch=043/100 loss=0.065071 val_dice=0.270480 val_pr_auc=0.393687 minutes=3.09
reports/training/R100_thebe_seed42_resume_20261005_131346.log:53:epoch=044/100 loss=0.064441 val_dice=0.172999 val_pr_auc=0.384315 minutes=3.11
reports/training/R100_thebe_seed42_resume_20261005_131346.log:55:epoch=045/100 loss=0.063953 val_dice=0.286662 val_pr_auc=0.441626 minutes=3.20
reports/training/R100_thebe_seed42_resume_20261005_131346.log:57:epoch=046/100 loss=0.059598 val_dice=0.413131 val_pr_auc=0.401415 minutes=3.25
reports/training/R100_thebe_seed42_resume_20261005_131346.log:59:epoch=047/100 loss=0.062477 val_dice=0.245688 val_pr_auc=0.443531 minutes=3.15
reports/training/R100_thebe_seed42_resume_20261005_131346.log:61:epoch=048/100 loss=0.059514 val_dice=0.245539 val_pr_auc=0.437099 minutes=3.14
reports/training/R100_thebe_seed42_resume_20261005_131346.log:63:epoch=049/100 loss=0.061393 val_dice=0.279920 val_pr_auc=0.438496 minutes=3.24
reports/training/R100_thebe_seed42_resume_20261005_131346.log:65:epoch=050/100 loss=0.070041 val_dice=0.288117 val_pr_auc=0.453892 minutes=3.29
reports/training/R100_thebe_seed42_resume_20261005_131346.log:67:epoch=051/100 loss=0.065202 val_dice=0.266200 val_pr_auc=0.460510 minutes=3.37
reports/training/R100_thebe_seed42_resume_20261005_131346.log:69:epoch=052/100 loss=0.066613 val_dice=0.356431 val_pr_auc=0.427422 minutes=3.12
reports/training/R100_thebe_seed42_resume_20261005_131346.log:71:epoch=053/100 loss=0.066192 val_dice=0.342636 val_pr_auc=0.433051 minutes=3.27
reports/training/R100_thebe_seed42_resume_20261005_131346.log:73:epoch=054/100 loss=0.064246 val_dice=0.341244 val_pr_auc=0.459710 minutes=3.38
reports/training/R100_thebe_seed42_resume_20261005_131346.log:75:epoch=055/100 loss=0.054061 val_dice=0.428206 val_pr_auc=0.477125 minutes=3.27
reports/training/R100_thebe_seed42_resume_20261005_131346.log:77:epoch=056/100 loss=0.060517 val_dice=0.356121 val_pr_auc=0.480524 minutes=3.22
reports/training/R100_thebe_seed42_resume_20261005_131346.log:79:epoch=057/100 loss=0.063365 val_dice=0.428462 val_pr_auc=0.440082 minutes=3.14
reports/training/R100_thebe_seed42_resume_20261005_131346.log:81:epoch=058/100 loss=0.050335 val_dice=0.308301 val_pr_auc=0.512327 minutes=3.39
reports/training/R100_thebe_seed42_resume_20261005_131346.log:83:epoch=059/100 loss=0.067371 val_dice=0.472297 val_pr_auc=0.479524 minutes=3.24
reports/training/R100_thebe_seed42_resume_20261005_131346.log:85:epoch=060/100 loss=0.061604 val_dice=0.441440 val_pr_auc=0.516968 minutes=3.25
reports/training/R100_thebe_seed42_resume_20261005_131346.log:87:epoch=061/100 loss=0.062467 val_dice=0.247468 val_pr_auc=0.517348 minutes=3.13
reports/training/R100_thebe_seed42_resume_20261005_131346.log:89:epoch=062/100 loss=0.059376 val_dice=0.262464 val_pr_auc=0.489979 minutes=3.06
reports/training/R100_thebe_seed42_resume_20261005_131346.log:91:epoch=063/100 loss=0.063021 val_dice=0.350626 val_pr_auc=0.518379 minutes=3.16
reports/training/R100_thebe_seed42_resume_20261005_131346.log:93:epoch=064/100 loss=0.059923 val_dice=0.359455 val_pr_auc=0.538676 minutes=3.10
reports/training/R100_thebe_seed42_resume_20261005_131346.log:95:epoch=065/100 loss=0.047842 val_dice=0.269996 val_pr_auc=0.492450 minutes=3.30
reports/training/R100_thebe_seed42_resume_20261005_131346.log:97:epoch=066/100 loss=0.055280 val_dice=0.415410 val_pr_auc=0.508203 minutes=3.15
reports/training/R100_thebe_seed42_resume_20261005_131346.log:99:epoch=067/100 loss=0.061079 val_dice=0.383309 val_pr_auc=0.545594 minutes=3.14
reports/training/R100_thebe_seed42_resume_20261005_131346.log:101:epoch=068/100 loss=0.052238 val_dice=0.502782 val_pr_auc=0.544847 minutes=3.20
reports/training/R100_thebe_seed42_resume_20261005_131346.log:103:epoch=069/100 loss=0.058578 val_dice=0.496378 val_pr_auc=0.556591 minutes=3.28
reports/training/R100_thebe_seed42_resume_20261005_131346.log:105:epoch=070/100 loss=0.053104 val_dice=0.313013 val_pr_auc=0.547534 minutes=3.34
reports/training/R100_thebe_seed42_resume_20261005_131346.log:107:epoch=071/100 loss=0.053821 val_dice=0.393332 val_pr_auc=0.567882 minutes=3.18
reports/training/R100_thebe_seed42_resume_20261005_131346.log:109:epoch=072/100 loss=0.059722 val_dice=0.413933 val_pr_auc=0.571626 minutes=3.33
runs/baseline_A_synthetic_bce_seed42/best.pt: binary file matches (found "\0" byte around offset 4)
runs/baseline_A_synthetic_bce_seed42/final_metrics.json:15:    "roc_auc_approximation": "streaming histogram with 2048 bins",
runs/baseline_A_synthetic_bce_seed42/final_metrics.json:21:    "dice": 0.8210585667450961,
runs/baseline_A_synthetic_bce_seed42/final_metrics.json:24:    "iou": 0.6964371117895655,
runs/baseline_A_synthetic_bce_seed42/final_metrics.json:27:    "precision": 0.8030095271846518,
runs/baseline_A_synthetic_bce_seed42/final_metrics.json:28:    "recall": 0.8399376298142152,
runs/baseline_A_synthetic_bce_seed42/final_metrics.json:29:    "roc_auc_approx": 0.985231916138331,
runs/baseline_A_synthetic_bce_seed42/final_metrics.json:57:    "dice": {
runs/baseline_A_synthetic_bce_seed42/final_metrics.json:71:    "iou": {
runs/baseline_A_synthetic_bce_seed42/final_metrics.json:99:    "precision": {
runs/baseline_A_synthetic_bce_seed42/final_metrics.json:106:    "recall": {
runs/baseline_A_synthetic_bce_seed42/final_metrics.json:113:    "roc_auc_approx": {
runs/baseline_A_synthetic_bce_seed42/final_metrics.json:132:    "dice": 0.8168437187101376,
runs/baseline_A_synthetic_bce_seed42/final_metrics.json:135:    "iou": 0.690393764228361,
runs/baseline_A_synthetic_bce_seed42/final_metrics.json:138:    "precision": 0.7991951500999772,
runs/baseline_A_synthetic_bce_seed42/final_metrics.json:139:    "recall": 0.8352893529882043,
runs/baseline_A_synthetic_bce_seed42/final_metrics.json:140:    "roc_auc_approx": 0.9824618783754979,
runs/baseline_A_synthetic_bce_seed42/final_metrics.json:168:    "dice": {
runs/baseline_A_synthetic_bce_seed42/final_metrics.json:182:    "iou": {
runs/baseline_A_synthetic_bce_seed42/final_metrics.json:210:    "precision": {
runs/baseline_A_synthetic_bce_seed42/final_metrics.json:217:    "recall": {
runs/baseline_A_synthetic_bce_seed42/final_metrics.json:224:    "roc_auc_approx": {
runs/baseline_A_synthetic_bce_seed42/history.csv:1:epoch,train_loss,optimizer_steps,seconds,val_threshold,val_dice,val_iou,val_precision,val_recall,val_specificity,val_balanced_accuracy,val_accuracy,val_mcc,val_pr_auc_approx,val_roc_auc_approx,val_tp,val_fp,val_fn,val_tn
runs/baseline_A_synthetic_bce_seed42/last.pt: binary file matches (found "\0" byte around offset 4)
runs/baseline_A_synthetic_bce_seed42/test_per_volume.csv:1:volume_id,threshold,dice,iou,precision,recall,specificity,balanced_accuracy,accuracy,mcc,pr_auc_approx,roc_auc_approx,tp,fp,fn,tn,modified_hausdorff_voxels,bidirectional_chamfer_voxels,prediction_empty,target_empty,inference_seconds
runs/baseline_A_synthetic_bce_seed42/validation_per_volume.csv:1:volume_id,threshold,dice,iou,precision,recall,specificity,balanced_accuracy,accuracy,mcc,pr_auc_approx,roc_auc_approx,tp,fp,fn,tn,modified_hausdorff_voxels,bidirectional_chamfer_voxels,prediction_empty,target_empty,inference_seconds
runs/loss_ablation_L1_weighted_bce_dice_seed42/best.pt: binary file matches (found "\0" byte around offset 4)
runs/loss_ablation_L1_weighted_bce_dice_seed42/final_metrics.json:15:    "roc_auc_approximation": "streaming histogram with 2048 bins",
runs/loss_ablation_L1_weighted_bce_dice_seed42/final_metrics.json:21:    "dice": 0.8197658344077322,
runs/loss_ablation_L1_weighted_bce_dice_seed42/final_metrics.json:24:    "iou": 0.6945789728060917,
runs/loss_ablation_L1_weighted_bce_dice_seed42/final_metrics.json:27:    "precision": 0.8041099575085737,
runs/loss_ablation_L1_weighted_bce_dice_seed42/final_metrics.json:28:    "recall": 0.8360434507017636,
runs/loss_ablation_L1_weighted_bce_dice_seed42/final_metrics.json:29:    "roc_auc_approx": 0.9801792013509681,
runs/loss_ablation_L1_weighted_bce_dice_seed42/final_metrics.json:57:    "dice": {
runs/loss_ablation_L1_weighted_bce_dice_seed42/final_metrics.json:71:    "iou": {
runs/loss_ablation_L1_weighted_bce_dice_seed42/final_metrics.json:99:    "precision": {
runs/loss_ablation_L1_weighted_bce_dice_seed42/final_metrics.json:106:    "recall": {
runs/loss_ablation_L1_weighted_bce_dice_seed42/final_metrics.json:113:    "roc_auc_approx": {
runs/loss_ablation_L1_weighted_bce_dice_seed42/final_metrics.json:132:    "dice": 0.8181935663428848,
runs/loss_ablation_L1_weighted_bce_dice_seed42/final_metrics.json:135:    "iou": 0.6923245152854467,
runs/loss_ablation_L1_weighted_bce_dice_seed42/final_metrics.json:138:    "precision": 0.7992400416395384,
runs/loss_ablation_L1_weighted_bce_dice_seed42/final_metrics.json:139:    "recall": 0.838067871018416,
runs/loss_ablation_L1_weighted_bce_dice_seed42/final_metrics.json:140:    "roc_auc_approx": 0.9781604597074529,
runs/loss_ablation_L1_weighted_bce_dice_seed42/final_metrics.json:168:    "dice": {
runs/loss_ablation_L1_weighted_bce_dice_seed42/final_metrics.json:182:    "iou": {
runs/loss_ablation_L1_weighted_bce_dice_seed42/final_metrics.json:210:    "precision": {
runs/loss_ablation_L1_weighted_bce_dice_seed42/final_metrics.json:217:    "recall": {
runs/loss_ablation_L1_weighted_bce_dice_seed42/final_metrics.json:224:    "roc_auc_approx": {
runs/loss_ablation_L1_weighted_bce_dice_seed42/history.csv:1:epoch,train_loss,optimizer_steps,seconds,val_threshold,val_dice,val_iou,val_precision,val_recall,val_specificity,val_balanced_accuracy,val_accuracy,val_mcc,val_pr_auc_approx,val_roc_auc_approx,val_tp,val_fp,val_fn,val_tn
runs/loss_ablation_L1_weighted_bce_dice_seed42/last.pt: binary file matches (found "\0" byte around offset 4)
runs/loss_ablation_L1_weighted_bce_dice_seed42/run_config.json:10:  "experiment_name": "Loss Ablation L1 \u2014 weighted BCE plus Dice",
runs/loss_ablation_L1_weighted_bce_dice_seed42/run_config.json:15:  "loss": "b1_weighted_dice",
runs/loss_ablation_L1_weighted_bce_dice_seed42/run_config.json:16:  "loss_description": "0.5 weighted BCE plus 0.5 soft Dice loss",
runs/loss_ablation_L1_weighted_bce_dice_seed42/run_config.json:21:  "run_dir": "runs/loss_ablation_L1_weighted_bce_dice_seed42",
runs/loss_ablation_L1_weighted_bce_dice_seed42/test_per_volume.csv:1:volume_id,threshold,dice,iou,precision,recall,specificity,balanced_accuracy,accuracy,mcc,pr_auc_approx,roc_auc_approx,tp,fp,fn,tn,modified_hausdorff_voxels,bidirectional_chamfer_voxels,prediction_empty,target_empty,inference_seconds
runs/loss_ablation_L1_weighted_bce_dice_seed42/validation_per_volume.csv:1:volume_id,threshold,dice,iou,precision,recall,specificity,balanced_accuracy,accuracy,mcc,pr_auc_approx,roc_auc_approx,tp,fp,fn,tn,modified_hausdorff_voxels,bidirectional_chamfer_voxels,prediction_empty,target_empty,inference_seconds
runs/p1_attention3d_caft_seed42/best_p1_attention3d_caft_seed42_epoch093_faultseg3d_synthetic_20261009.pt: binary file matches (found "\0" byte around offset 4)
runs/p1_attention3d_caft_seed42/best.pt: binary file matches (found "\0" byte around offset 4)
runs/p1_attention3d_caft_seed42/final_metrics.json:15:    "roc_auc_approximation": "streaming histogram with 2048 bins",
runs/p1_attention3d_caft_seed42/final_metrics.json:21:    "dice": 0.8266458436496147,
runs/p1_attention3d_caft_seed42/final_metrics.json:24:    "iou": 0.7045152047024095,
runs/p1_attention3d_caft_seed42/final_metrics.json:27:    "precision": 0.7967662250168426,
runs/p1_attention3d_caft_seed42/final_metrics.json:28:    "recall": 0.8588538159195678,
runs/p1_attention3d_caft_seed42/final_metrics.json:29:    "roc_auc_approx": 0.9396824964507412,
runs/p1_attention3d_caft_seed42/final_metrics.json:57:    "dice": {
runs/p1_attention3d_caft_seed42/final_metrics.json:71:    "iou": {
runs/p1_attention3d_caft_seed42/final_metrics.json:99:    "precision": {
runs/p1_attention3d_caft_seed42/final_metrics.json:106:    "recall": {
runs/p1_attention3d_caft_seed42/final_metrics.json:113:    "roc_auc_approx": {
runs/p1_attention3d_caft_seed42/final_metrics.json:132:    "dice": 0.8214084611645242,
runs/p1_attention3d_caft_seed42/final_metrics.json:135:    "iou": 0.6969407416382172,
runs/p1_attention3d_caft_seed42/final_metrics.json:138:    "precision": 0.7919055523009829,
runs/p1_attention3d_caft_seed42/final_metrics.json:139:    "recall": 0.8531947347013198,
runs/p1_attention3d_caft_seed42/final_metrics.json:140:    "roc_auc_approx": 0.935983288714892,
runs/p1_attention3d_caft_seed42/final_metrics.json:168:    "dice": {
runs/p1_attention3d_caft_seed42/final_metrics.json:182:    "iou": {
runs/p1_attention3d_caft_seed42/final_metrics.json:210:    "precision": {
runs/p1_attention3d_caft_seed42/final_metrics.json:217:    "recall": {
runs/p1_attention3d_caft_seed42/final_metrics.json:224:    "roc_auc_approx": {
runs/p1_attention3d_caft_seed42/history.csv:1:epoch,train_loss,optimizer_steps,seconds,val_threshold,val_dice,val_iou,val_precision,val_recall,val_specificity,val_balanced_accuracy,val_accuracy,val_mcc,val_pr_auc_approx,val_roc_auc_approx,val_tp,val_fp,val_fn,val_tn,train_caft_loss,train_attention_loss
runs/p1_attention3d_caft_seed42/last.pt: binary file matches (found "\0" byte around offset 4)
runs/p1_attention3d_caft_seed42/test_per_volume.csv:1:volume_id,threshold,dice,iou,precision,recall,specificity,balanced_accuracy,accuracy,mcc,pr_auc_approx,roc_auc_approx,tp,fp,fn,tn,modified_hausdorff_voxels,bidirectional_chamfer_voxels,prediction_empty,target_empty,inference_seconds
runs/p1_attention3d_caft_seed42/train.log:8:/shared/home/khavarj/projects/fault_detection/.venv_train/lib/python3.13/site-packages/torch/autograd/graph.py:824: UserWarning: max_pool3d_with_indices_backward_cuda does not have a deterministic implementation, but you set 'torch.use_deterministic_algorithms(True, warn_only=True)'. You can file an issue at https://github.com/pytorch/pytorch/issues to help us prioritize adding deterministic support for this operation. (Triggered internally at /pytorch/aten/src/ATen/Context.cpp:93.)
runs/p1_attention3d_caft_seed42/train.log:14:epoch=001 loss=0.838507 val_dice=0.127385 val_iou=0.068025 val_pr_auc=0.071179 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:15:epoch=002 loss=0.829427 val_dice=0.127352 val_iou=0.068007 val_pr_auc=0.068252 minutes=0.34
runs/p1_attention3d_caft_seed42/train.log:16:epoch=003 loss=0.827917 val_dice=0.131709 val_iou=0.070497 val_pr_auc=0.071798 minutes=0.34
runs/p1_attention3d_caft_seed42/train.log:17:epoch=004 loss=0.776252 val_dice=0.223383 val_iou=0.125735 val_pr_auc=0.135151 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:18:epoch=005 loss=0.571470 val_dice=0.382732 val_iou=0.236653 val_pr_auc=0.240804 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:19:epoch=006 loss=0.454002 val_dice=0.474475 val_iou=0.311024 val_pr_auc=0.342266 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:20:epoch=007 loss=0.385372 val_dice=0.540523 val_iou=0.370354 val_pr_auc=0.394514 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:21:epoch=008 loss=0.328829 val_dice=0.568067 val_iou=0.396713 val_pr_auc=0.432253 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:22:epoch=009 loss=0.295809 val_dice=0.607155 val_iou=0.435910 val_pr_auc=0.482395 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:23:epoch=010 loss=0.274992 val_dice=0.622836 val_iou=0.452260 val_pr_auc=0.492261 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:24:epoch=011 loss=0.248961 val_dice=0.641727 val_iou=0.472458 val_pr_auc=0.531435 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:25:epoch=012 loss=0.233057 val_dice=0.643216 val_iou=0.474074 val_pr_auc=0.512073 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:26:epoch=013 loss=0.218292 val_dice=0.668364 val_iou=0.501912 val_pr_auc=0.551982 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:27:epoch=014 loss=0.211313 val_dice=0.675591 val_iou=0.510108 val_pr_auc=0.570569 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:28:epoch=015 loss=0.200009 val_dice=0.686478 val_iou=0.522623 val_pr_auc=0.580324 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:29:epoch=016 loss=0.190337 val_dice=0.672484 val_iou=0.506574 val_pr_auc=0.567807 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:30:epoch=017 loss=0.186106 val_dice=0.705062 val_iou=0.544475 val_pr_auc=0.590438 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:31:epoch=018 loss=0.179119 val_dice=0.700617 val_iou=0.539192 val_pr_auc=0.589192 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:32:epoch=019 loss=0.176469 val_dice=0.708570 val_iou=0.548671 val_pr_auc=0.597900 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:33:epoch=020 loss=0.171612 val_dice=0.707628 val_iou=0.547543 val_pr_auc=0.592573 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:34:epoch=021 loss=0.166923 val_dice=0.701295 val_iou=0.539995 val_pr_auc=0.589884 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:35:epoch=022 loss=0.161732 val_dice=0.721968 val_iou=0.564906 val_pr_auc=0.609664 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:36:epoch=023 loss=0.157391 val_dice=0.701319 val_iou=0.540024 val_pr_auc=0.587490 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:37:epoch=024 loss=0.155300 val_dice=0.742589 val_iou=0.590570 val_pr_auc=0.636356 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:38:epoch=025 loss=0.150285 val_dice=0.739467 val_iou=0.586631 val_pr_auc=0.634767 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:39:epoch=026 loss=0.151153 val_dice=0.736535 val_iou=0.582948 val_pr_auc=0.627589 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:40:epoch=027 loss=0.144357 val_dice=0.742349 val_iou=0.590266 val_pr_auc=0.632478 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:41:epoch=028 loss=0.143262 val_dice=0.719424 val_iou=0.561797 val_pr_auc=0.597831 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:42:epoch=029 loss=0.141514 val_dice=0.742312 val_iou=0.590219 val_pr_auc=0.634946 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:43:epoch=030 loss=0.136325 val_dice=0.725786 val_iou=0.569595 val_pr_auc=0.610305 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:44:epoch=031 loss=0.135256 val_dice=0.755739 val_iou=0.607380 val_pr_auc=0.656764 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:45:epoch=032 loss=0.133813 val_dice=0.737302 val_iou=0.583909 val_pr_auc=0.632831 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:46:epoch=033 loss=0.130487 val_dice=0.747330 val_iou=0.596590 val_pr_auc=0.635324 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:47:epoch=034 loss=0.135323 val_dice=0.750462 val_iou=0.600592 val_pr_auc=0.648544 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:48:epoch=035 loss=0.125358 val_dice=0.753153 val_iou=0.604046 val_pr_auc=0.642489 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:49:epoch=036 loss=0.123199 val_dice=0.764128 val_iou=0.618290 val_pr_auc=0.663117 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:50:epoch=037 loss=0.122790 val_dice=0.758741 val_iou=0.611267 val_pr_auc=0.655906 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:51:epoch=038 loss=0.122854 val_dice=0.759844 val_iou=0.612700 val_pr_auc=0.652983 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:52:epoch=039 loss=0.117098 val_dice=0.772156 val_iou=0.628871 val_pr_auc=0.669024 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:53:epoch=040 loss=0.116440 val_dice=0.766547 val_iou=0.621464 val_pr_auc=0.667631 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:54:epoch=041 loss=0.114330 val_dice=0.770236 val_iou=0.626328 val_pr_auc=0.667975 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:55:epoch=042 loss=0.113242 val_dice=0.764685 val_iou=0.619021 val_pr_auc=0.662146 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:56:epoch=043 loss=0.116130 val_dice=0.771348 val_iou=0.627800 val_pr_auc=0.671310 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:57:epoch=044 loss=0.109066 val_dice=0.766714 val_iou=0.621685 val_pr_auc=0.666058 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:58:epoch=045 loss=0.106280 val_dice=0.754609 val_iou=0.605922 val_pr_auc=0.641951 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:59:epoch=046 loss=0.107376 val_dice=0.774563 val_iou=0.632071 val_pr_auc=0.667324 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:60:epoch=047 loss=0.107808 val_dice=0.780461 val_iou=0.639964 val_pr_auc=0.679347 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:61:epoch=048 loss=0.102630 val_dice=0.778017 val_iou=0.636683 val_pr_auc=0.675086 minutes=0.35
runs/p1_attention3d_caft_seed42/train.log:62:epoch=049 loss=0.103618 val_dice=0.779226 val_iou=0.638305 val_pr_auc=0.675217 minutes=0.35
runs/p1_attention3d_caft_seed42/validation_per_volume.csv:1:volume_id,threshold,dice,iou,precision,recall,specificity,balanced_accuracy,accuracy,mcc,pr_auc_approx,roc_auc_approx,tp,fp,fn,tn,modified_hausdorff_voxels,bidirectional_chamfer_voxels,prediction_empty,target_empty,inference_seconds
runs/paper_attention3d_thebe_smoke_20261009_170246/history.csv:1:epoch,train_loss,val_loss,val_dice,val_precision,val_recall,val_fault_prevalence,lr,seconds_elapsed
runs/paper_attention3d_thebe_smoke_20261009_170246/status.json:3:  "best_validation_dice": 0.005775611169199155,
runs/paper_attention3d_thebe_smoke_20261009_170246/status.json:5:  "best_checkpoint": "runs/paper_attention3d_thebe_smoke_20261009_170246/best.pt",
runs/paper_attention3d_thebe_supervised_seed42/best.pt: binary file matches (found "\0" byte around offset 4)
runs/paper_attention3d_thebe_supervised_seed42_bf16_clean/best.pt: binary file matches (found "\0" byte around offset 4)
runs/paper_attention3d_thebe_supervised_seed42_bf16_clean/history.csv:1:epoch,train_loss,val_loss,val_dice,val_precision,val_recall,val_fault_prevalence,lr,seconds_elapsed
runs/paper_attention3d_thebe_supervised_seed42_bf16_clean/last.pt: binary file matches (found "\0" byte around offset 4)
runs/paper_attention3d_thebe_supervised_seed42_bf16_clean/run_configuration.json:2:  "experiment": "paper_global_attention_real_Thebe_supervised_without_denoising_pretraining_bf16_stability_fixed",
runs/paper_attention3d_thebe_supervised_seed42_bf16_clean/run_configuration.json:29:  "precision": "BF16 autocast; gradient scaling disabled",
runs/paper_attention3d_thebe_supervised_seed42/history.csv:1:epoch,train_loss,val_loss,val_dice,val_precision,val_recall,val_fault_prevalence,lr,seconds_elapsed
runs/paper_attention3d_thebe_supervised_seed42/last.pt: binary file matches (found "\0" byte around offset 4)
runs/R100_fp16_clean_3seeds_20261014_145225/smoke.log:14:RuntimeError: scripts/evaluate_thebe_zero_shot.py changed since inspection. Expected 834ec8aeb8a726c51f6dd65e4f85fac7652dfcc13f8ab58f0784fe359b9374ec, got ebff17dcf7e143113567155a3fbb147d3c82bf311a1108c157eafcb3d837b30f. No training has started.
runs/R100_fp16_clean_3seeds_20261014_145510/seed42.log:5:/shared/home/khavarj/projects/fault_detection/.venv_train/lib/python3.13/site-packages/torch/autograd/graph.py:824: UserWarning: max_pool3d_with_indices_backward_cuda does not have a deterministic implementation, but you set 'torch.use_deterministic_algorithms(True, warn_only=True)'. You can file an issue at https://github.com/pytorch/pytorch/issues to help us prioritize adding deterministic support for this operation. (Triggered internally at /pytorch/aten/src/ATen/Context.cpp:93.)
runs/R100_fp16_clean_3seeds_20261014_145510/seed42/run_config.json:5:  "precision": "float16_autocast",
runs/R100_fp16_clean_3seeds_20261014_145510/seed42/run_config.json:746:  "threshold_selection": "best Dice on complete validation volume with 2048 bins",
runs/R100_fp16_clean_3seeds_20261014_145510/seed42/run_config.json:748:  "protocol_hash": "0d0f64772ba5235888983abbd5389ba1a4f5df15f23fcd93876699c6f6dabca5"
runs/R100_fp16_clean_3seeds_20261014_145510/smoke.log:5:/shared/home/khavarj/projects/fault_detection/.venv_train/lib/python3.13/site-packages/torch/autograd/graph.py:824: UserWarning: max_pool3d_with_indices_backward_cuda does not have a deterministic implementation, but you set 'torch.use_deterministic_algorithms(True, warn_only=True)'. You can file an issue at https://github.com/pytorch/pytorch/issues to help us prioritize adding deterministic support for this operation. (Triggered internally at /pytorch/aten/src/ATen/Context.cpp:93.)
runs/R100_fp16_clean_3seeds_20261014_145510/smoke.log:12:epoch=001/1 loss=0.779829 val_dice=0.068725 val_pr_auc=0.033207 minutes=0.22
runs/R100_fp16_clean_3seeds_20261014_145510/smoke_seed42/best.pt: binary file matches (found "\0" byte around offset 4)
runs/R100_fp16_clean_3seeds_20261014_145510/smoke_seed42/history.csv:1:epoch,train_loss,train_patches,resampled_no_data_candidates,excluded_training_positive_labels,seconds,val_threshold,val_dice,val_iou,val_precision,val_recall,val_specificity,val_balanced_accuracy,val_accuracy,val_mcc,val_pr_auc_approx,val_roc_auc_approx,val_tp,val_fp,val_fn,val_tn
runs/R100_fp16_clean_3seeds_20261014_145510/smoke_seed42/last.pt: binary file matches (found "\0" byte around offset 4)
runs/R100_fp16_clean_3seeds_20261014_145510/smoke_seed42/run_config.json:5:  "precision": "float16_autocast",
runs/R100_fp16_clean_3seeds_20261014_145510/smoke_seed42/run_config.json:116:  "threshold_selection": "best Dice on smoke validation subset",
runs/R100_fp16_clean_3seeds_20261014_145510/smoke_seed42/status.json:7:  "precision": "float16_autocast",
runs/R100_fp16_clean_3seeds_20261014_145510/smoke_seed42/status.json:12:  "best_checkpoint": "runs/R100_fp16_clean_3seeds_20261014_145510/smoke_seed42/best.pt",
runs/R100_fp16_clean_3seeds_20261014_145510/smoke_seed42/validation_selection.json:7:    "dice": 0.06884626641830875,
runs/R100_fp16_clean_3seeds_20261014_145510/smoke_seed42/validation_selection.json:8:    "iou": 0.035650329241587765,
runs/R100_fp16_clean_3seeds_20261014_145510/smoke_seed42/validation_selection.json:9:    "precision": 0.035650329241587765,
runs/R100_fp16_clean_3seeds_20261014_145510/smoke_seed42/validation_selection.json:10:    "recall": 1.0,
runs/R100_fp16_clean_3seeds_20261014_145510/smoke_seed42/validation_selection.json:16:    "roc_auc_approx": 0.4517016441816569,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:22:        "dice": 0.5440719430427761,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:23:        "iou": 0.373694249824297,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:24:        "precision": 0.5267658204531103,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:25:        "recall": 0.562553828427201,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:31:        "roc_auc_approx": 0.9560342463297409,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:47:        "dice": 0.5698556833270347,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:48:        "iou": 0.39846026494216036,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:49:        "precision": 0.5643889729910121,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:50:        "recall": 0.5754293313318344,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:56:        "roc_auc_approx": 0.9612985077763903,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:72:        "dice": 0.5729798256899185,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:73:        "iou": 0.40152188175400944,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:74:        "precision": 0.5655692044103381,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:75:        "recall": 0.5805872272731943,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:81:        "roc_auc_approx": 0.9589852925995812,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:102:  "validation_dice_mean": 0.5623024840199098,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:103:  "validation_dice_sample_sd": 0.015865198852050486
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/best.pt: binary file matches (found "\0" byte around offset 4)
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/history.csv:1:epoch,train_loss,train_patches,resampled_no_data_candidates,excluded_training_positive_labels,seconds,val_threshold,val_dice,val_iou,val_precision,val_recall,val_specificity,val_balanced_accuracy,val_accuracy,val_mcc,val_pr_auc_approx,val_roc_auc_approx,val_tp,val_fp,val_fn,val_tn
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/last.pt: binary file matches (found "\0" byte around offset 4)
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:5:/shared/home/khavarj/projects/fault_detection/.venv_train/lib/python3.13/site-packages/torch/autograd/graph.py:824: UserWarning: max_pool3d_with_indices_backward_cuda does not have a deterministic implementation, but you set 'torch.use_deterministic_algorithms(True, warn_only=True)'. You can file an issue at https://github.com/pytorch/pytorch/issues to help us prioritize adding deterministic support for this operation. (Triggered internally at /pytorch/aten/src/ATen/Context.cpp:93.)
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:18:epoch=001/100 loss=0.211608 val_dice=0.000006 val_pr_auc=0.034823 minutes=3.12
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:26:epoch=002/100 loss=0.131591 val_dice=0.000001 val_pr_auc=0.039528 minutes=3.08
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:34:epoch=003/100 loss=0.105220 val_dice=0.000001 val_pr_auc=0.043710 minutes=3.09
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:42:epoch=004/100 loss=0.101674 val_dice=0.000000 val_pr_auc=0.043505 minutes=3.18
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:50:epoch=005/100 loss=0.113378 val_dice=0.000000 val_pr_auc=0.038386 minutes=2.88
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:58:epoch=006/100 loss=0.102869 val_dice=0.000000 val_pr_auc=0.047210 minutes=3.07
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:66:epoch=007/100 loss=0.106725 val_dice=0.000000 val_pr_auc=0.049760 minutes=3.06
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:74:epoch=008/100 loss=0.096674 val_dice=0.000000 val_pr_auc=0.048672 minutes=2.99
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:82:epoch=009/100 loss=0.099541 val_dice=0.000000 val_pr_auc=0.043619 minutes=3.14
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:90:epoch=010/100 loss=0.107934 val_dice=0.000000 val_pr_auc=0.055916 minutes=2.92
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:98:epoch=011/100 loss=0.099936 val_dice=0.000000 val_pr_auc=0.061880 minutes=2.95
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:106:epoch=012/100 loss=0.102164 val_dice=0.000000 val_pr_auc=0.049965 minutes=3.01
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:114:epoch=013/100 loss=0.109964 val_dice=0.000000 val_pr_auc=0.061470 minutes=2.89
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:122:epoch=014/100 loss=0.096900 val_dice=0.000000 val_pr_auc=0.089677 minutes=2.94
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:130:epoch=015/100 loss=0.089464 val_dice=0.000000 val_pr_auc=0.117684 minutes=3.08
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:138:epoch=016/100 loss=0.088687 val_dice=0.000000 val_pr_auc=0.107323 minutes=3.07
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:146:epoch=017/100 loss=0.083734 val_dice=0.000000 val_pr_auc=0.135083 minutes=3.05
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:154:epoch=018/100 loss=0.087998 val_dice=0.000000 val_pr_auc=0.171241 minutes=3.17
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:162:epoch=019/100 loss=0.090926 val_dice=0.000000 val_pr_auc=0.184733 minutes=2.97
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:170:epoch=020/100 loss=0.077623 val_dice=0.000000 val_pr_auc=0.207758 minutes=3.01
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:178:epoch=021/100 loss=0.073180 val_dice=0.000013 val_pr_auc=0.213077 minutes=3.03
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:186:epoch=022/100 loss=0.077549 val_dice=0.000690 val_pr_auc=0.212709 minutes=2.94
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:194:epoch=023/100 loss=0.080129 val_dice=0.001580 val_pr_auc=0.250377 minutes=2.89
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:202:epoch=024/100 loss=0.085101 val_dice=0.007970 val_pr_auc=0.210663 minutes=3.00
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:210:epoch=025/100 loss=0.067014 val_dice=0.002319 val_pr_auc=0.270853 minutes=3.03
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:218:epoch=026/100 loss=0.074720 val_dice=0.008281 val_pr_auc=0.258356 minutes=3.06
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:226:epoch=027/100 loss=0.078038 val_dice=0.002668 val_pr_auc=0.299218 minutes=3.02
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:234:epoch=028/100 loss=0.069081 val_dice=0.016612 val_pr_auc=0.289297 minutes=3.13
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:242:epoch=029/100 loss=0.067600 val_dice=0.025738 val_pr_auc=0.304789 minutes=3.06
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:250:epoch=030/100 loss=0.069910 val_dice=0.025284 val_pr_auc=0.307485 minutes=3.10
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:258:epoch=031/100 loss=0.071929 val_dice=0.005624 val_pr_auc=0.335175 minutes=3.10
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:266:epoch=032/100 loss=0.074831 val_dice=0.014670 val_pr_auc=0.324274 minutes=2.89
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:274:epoch=033/100 loss=0.069609 val_dice=0.119484 val_pr_auc=0.339538 minutes=3.03
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:282:epoch=034/100 loss=0.061320 val_dice=0.095749 val_pr_auc=0.323181 minutes=3.06
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:290:epoch=035/100 loss=0.071427 val_dice=0.106897 val_pr_auc=0.358173 minutes=3.10
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:298:epoch=036/100 loss=0.070403 val_dice=0.117125 val_pr_auc=0.339758 minutes=3.03
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:306:epoch=037/100 loss=0.072179 val_dice=0.206109 val_pr_auc=0.363270 minutes=2.98
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:314:epoch=038/100 loss=0.072133 val_dice=0.230500 val_pr_auc=0.384911 minutes=3.18
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:322:epoch=039/100 loss=0.066432 val_dice=0.149482 val_pr_auc=0.392297 minutes=2.94
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:330:epoch=040/100 loss=0.059668 val_dice=0.100121 val_pr_auc=0.388984 minutes=3.16
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:338:epoch=041/100 loss=0.060640 val_dice=0.237473 val_pr_auc=0.413392 minutes=3.08
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:346:epoch=042/100 loss=0.065647 val_dice=0.136110 val_pr_auc=0.418763 minutes=3.14
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:354:epoch=043/100 loss=0.065825 val_dice=0.211336 val_pr_auc=0.382685 minutes=3.06
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:362:epoch=044/100 loss=0.058033 val_dice=0.226795 val_pr_auc=0.418009 minutes=3.08
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:370:epoch=045/100 loss=0.068560 val_dice=0.331624 val_pr_auc=0.419339 minutes=3.45
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:378:epoch=046/100 loss=0.064055 val_dice=0.310719 val_pr_auc=0.433676 minutes=3.54
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:386:epoch=047/100 loss=0.065738 val_dice=0.201582 val_pr_auc=0.400658 minutes=3.41
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:394:epoch=048/100 loss=0.064558 val_dice=0.331357 val_pr_auc=0.459623 minutes=3.51
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:402:epoch=049/100 loss=0.057787 val_dice=0.402787 val_pr_auc=0.448123 minutes=3.57
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/run_config.json:5:  "precision": "float16_autocast",
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/run_config.json:746:  "threshold_selection": "best Dice on complete validation volume with 2048 bins",
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/status.json:7:  "precision": "float16_autocast",
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/status.json:12:  "best_checkpoint": "runs/R100_fp16_clean_3seeds_20261014_150435/seed42/best.pt",
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/validation_selection.json:7:    "dice": 0.5440719430427761,
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/validation_selection.json:8:    "iou": 0.373694249824297,
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/validation_selection.json:9:    "precision": 0.5267658204531103,
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/validation_selection.json:10:    "recall": 0.562553828427201,
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/validation_selection.json:16:    "roc_auc_approx": 0.9560342463297409,
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/history.csv:1:epoch,train_loss,train_patches,resampled_no_data_candidates,excluded_training_positive_labels,seconds,val_threshold,val_dice,val_iou,val_precision,val_recall,val_specificity,val_balanced_accuracy,val_accuracy,val_mcc,val_pr_auc_approx,val_roc_auc_approx,val_tp,val_fp,val_fn,val_tn
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:5:/shared/home/khavarj/projects/fault_detection/.venv_train/lib/python3.13/site-packages/torch/autograd/graph.py:824: UserWarning: max_pool3d_with_indices_backward_cuda does not have a deterministic implementation, but you set 'torch.use_deterministic_algorithms(True, warn_only=True)'. You can file an issue at https://github.com/pytorch/pytorch/issues to help us prioritize adding deterministic support for this operation. (Triggered internally at /pytorch/aten/src/ATen/Context.cpp:93.)
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:18:epoch=001/100 loss=0.207313 val_dice=0.000010 val_pr_auc=0.032889 minutes=3.25
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:26:epoch=002/100 loss=0.134325 val_dice=0.000000 val_pr_auc=0.037506 minutes=3.40
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:34:epoch=003/100 loss=0.113158 val_dice=0.000000 val_pr_auc=0.044267 minutes=3.32
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:42:epoch=004/100 loss=0.106803 val_dice=0.000000 val_pr_auc=0.047515 minutes=3.69
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:50:epoch=005/100 loss=0.112586 val_dice=0.000000 val_pr_auc=0.055564 minutes=3.44
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:58:epoch=006/100 loss=0.086832 val_dice=0.000000 val_pr_auc=0.073312 minutes=3.49
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:66:epoch=007/100 loss=0.096694 val_dice=0.000000 val_pr_auc=0.063642 minutes=3.45
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:74:epoch=008/100 loss=0.099798 val_dice=0.000000 val_pr_auc=0.111352 minutes=3.47
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:82:epoch=009/100 loss=0.086573 val_dice=0.000000 val_pr_auc=0.109360 minutes=3.49
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:90:epoch=010/100 loss=0.085202 val_dice=0.000000 val_pr_auc=0.129471 minutes=3.51
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:98:epoch=011/100 loss=0.082043 val_dice=0.000000 val_pr_auc=0.190129 minutes=3.52
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:106:epoch=012/100 loss=0.087391 val_dice=0.000000 val_pr_auc=0.182149 minutes=3.50
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:114:epoch=013/100 loss=0.086629 val_dice=0.051217 val_pr_auc=0.227169 minutes=3.42
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:122:epoch=014/100 loss=0.075188 val_dice=0.156249 val_pr_auc=0.287682 minutes=3.35
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:130:epoch=015/100 loss=0.069022 val_dice=0.128348 val_pr_auc=0.318932 minutes=3.42
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:138:epoch=016/100 loss=0.068342 val_dice=0.144531 val_pr_auc=0.319825 minutes=3.32
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:146:epoch=017/100 loss=0.076954 val_dice=0.317299 val_pr_auc=0.348228 minutes=3.34
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:154:epoch=018/100 loss=0.066294 val_dice=0.330689 val_pr_auc=0.360967 minutes=3.26
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:162:epoch=019/100 loss=0.078325 val_dice=0.154955 val_pr_auc=0.370729 minutes=3.36
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:170:epoch=020/100 loss=0.073825 val_dice=0.170272 val_pr_auc=0.410673 minutes=3.24
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:178:epoch=021/100 loss=0.074191 val_dice=0.326550 val_pr_auc=0.398516 minutes=3.31
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:186:epoch=022/100 loss=0.066618 val_dice=0.254137 val_pr_auc=0.428462 minutes=3.34
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:194:epoch=023/100 loss=0.069498 val_dice=0.275050 val_pr_auc=0.445187 minutes=3.20
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:202:epoch=024/100 loss=0.059472 val_dice=0.351567 val_pr_auc=0.463566 minutes=3.10
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:210:epoch=025/100 loss=0.061590 val_dice=0.290421 val_pr_auc=0.448529 minutes=3.13
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:218:epoch=026/100 loss=0.063974 val_dice=0.367536 val_pr_auc=0.458521 minutes=3.20
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:226:epoch=027/100 loss=0.066937 val_dice=0.184101 val_pr_auc=0.455209 minutes=3.18
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:234:epoch=028/100 loss=0.061171 val_dice=0.436915 val_pr_auc=0.483792 minutes=3.02
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:242:epoch=029/100 loss=0.054366 val_dice=0.275544 val_pr_auc=0.491174 minutes=3.15
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:250:epoch=030/100 loss=0.061534 val_dice=0.440431 val_pr_auc=0.473313 minutes=3.21
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:258:epoch=031/100 loss=0.058599 val_dice=0.331349 val_pr_auc=0.489746 minutes=3.11
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:266:epoch=032/100 loss=0.058002 val_dice=0.317572 val_pr_auc=0.507873 minutes=3.07
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:274:epoch=033/100 loss=0.064508 val_dice=0.132827 val_pr_auc=0.479362 minutes=3.13
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:282:epoch=034/100 loss=0.075195 val_dice=0.320840 val_pr_auc=0.513074 minutes=3.11
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:290:epoch=035/100 loss=0.061724 val_dice=0.474487 val_pr_auc=0.514265 minutes=3.13
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:298:epoch=036/100 loss=0.065400 val_dice=0.426747 val_pr_auc=0.542522 minutes=2.92
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:306:epoch=037/100 loss=0.056895 val_dice=0.471250 val_pr_auc=0.497020 minutes=2.93
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:314:epoch=038/100 loss=0.056790 val_dice=0.273526 val_pr_auc=0.525836 minutes=3.00
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:322:epoch=039/100 loss=0.060411 val_dice=0.326792 val_pr_auc=0.532453 minutes=3.10
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:330:epoch=040/100 loss=0.054520 val_dice=0.531070 val_pr_auc=0.546094 minutes=2.84
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:338:epoch=041/100 loss=0.061186 val_dice=0.334449 val_pr_auc=0.560378 minutes=2.95
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:346:epoch=042/100 loss=0.050234 val_dice=0.319623 val_pr_auc=0.526732 minutes=3.17
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:354:epoch=043/100 loss=0.053101 val_dice=0.448451 val_pr_auc=0.550102 minutes=2.91
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:362:epoch=044/100 loss=0.055038 val_dice=0.513862 val_pr_auc=0.562986 minutes=2.98
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:370:epoch=045/100 loss=0.055149 val_dice=0.341347 val_pr_auc=0.525956 minutes=2.94
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:378:epoch=046/100 loss=0.055819 val_dice=0.411702 val_pr_auc=0.558411 minutes=3.00
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:386:epoch=047/100 loss=0.056744 val_dice=0.540495 val_pr_auc=0.568879 minutes=2.94
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:394:epoch=048/100 loss=0.057409 val_dice=0.400572 val_pr_auc=0.577831 minutes=3.09
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:402:epoch=049/100 loss=0.056376 val_dice=0.510591 val_pr_auc=0.571619 minutes=3.07
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/run_config.json:5:  "precision": "float16_autocast",
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/run_config.json:746:  "threshold_selection": "best Dice on complete validation volume with 2048 bins",
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/status.json:7:  "precision": "float16_autocast",
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/status.json:12:  "best_checkpoint": "runs/R100_fp16_clean_3seeds_20261014_150435/seed43/best.pt",
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/validation_selection.json:7:    "dice": 0.5698556833270347,
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/validation_selection.json:8:    "iou": 0.39846026494216036,
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/validation_selection.json:9:    "precision": 0.5643889729910121,
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/validation_selection.json:10:    "recall": 0.5754293313318344,
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/validation_selection.json:16:    "roc_auc_approx": 0.9612985077763903,
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/history.csv:1:epoch,train_loss,train_patches,resampled_no_data_candidates,excluded_training_positive_labels,seconds,val_threshold,val_dice,val_iou,val_precision,val_recall,val_specificity,val_balanced_accuracy,val_accuracy,val_mcc,val_pr_auc_approx,val_roc_auc_approx,val_tp,val_fp,val_fn,val_tn
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:5:/shared/home/khavarj/projects/fault_detection/.venv_train/lib/python3.13/site-packages/torch/autograd/graph.py:824: UserWarning: max_pool3d_with_indices_backward_cuda does not have a deterministic implementation, but you set 'torch.use_deterministic_algorithms(True, warn_only=True)'. You can file an issue at https://github.com/pytorch/pytorch/issues to help us prioritize adding deterministic support for this operation. (Triggered internally at /pytorch/aten/src/ATen/Context.cpp:93.)
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:18:epoch=001/100 loss=0.214208 val_dice=0.000002 val_pr_auc=0.032531 minutes=2.98
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:26:epoch=002/100 loss=0.131131 val_dice=0.000002 val_pr_auc=0.041499 minutes=2.94
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:34:epoch=003/100 loss=0.093528 val_dice=0.000000 val_pr_auc=0.046544 minutes=3.03
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:42:epoch=004/100 loss=0.094511 val_dice=0.000000 val_pr_auc=0.045681 minutes=3.09
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:50:epoch=005/100 loss=0.103709 val_dice=0.000000 val_pr_auc=0.047491 minutes=3.07
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:58:epoch=006/100 loss=0.102382 val_dice=0.000000 val_pr_auc=0.053118 minutes=3.10
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:66:epoch=007/100 loss=0.096109 val_dice=0.000000 val_pr_auc=0.057679 minutes=3.11
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:74:epoch=008/100 loss=0.094502 val_dice=0.000000 val_pr_auc=0.055288 minutes=3.11
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:82:epoch=009/100 loss=0.099929 val_dice=0.000000 val_pr_auc=0.056435 minutes=3.03
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:90:epoch=010/100 loss=0.091132 val_dice=0.000000 val_pr_auc=0.072109 minutes=2.94
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:98:epoch=011/100 loss=0.091550 val_dice=0.000000 val_pr_auc=0.076607 minutes=3.09
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:106:epoch=012/100 loss=0.082483 val_dice=0.000000 val_pr_auc=0.089395 minutes=3.11
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:114:epoch=013/100 loss=0.095675 val_dice=0.000000 val_pr_auc=0.099517 minutes=3.09
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:122:epoch=014/100 loss=0.087235 val_dice=0.000000 val_pr_auc=0.128630 minutes=3.04
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:130:epoch=015/100 loss=0.092547 val_dice=0.000000 val_pr_auc=0.118855 minutes=2.92
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:138:epoch=016/100 loss=0.094852 val_dice=0.000000 val_pr_auc=0.121884 minutes=3.03
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:146:epoch=017/100 loss=0.087888 val_dice=0.000000 val_pr_auc=0.172786 minutes=3.01
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:154:epoch=018/100 loss=0.083555 val_dice=0.000000 val_pr_auc=0.163500 minutes=3.08
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:162:epoch=019/100 loss=0.089364 val_dice=0.000000 val_pr_auc=0.127726 minutes=3.08
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:170:epoch=020/100 loss=0.086457 val_dice=0.000000 val_pr_auc=0.175177 minutes=3.08
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:178:epoch=021/100 loss=0.069410 val_dice=0.000008 val_pr_auc=0.254670 minutes=2.94
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:186:epoch=022/100 loss=0.074515 val_dice=0.141201 val_pr_auc=0.326820 minutes=2.99
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:194:epoch=023/100 loss=0.072652 val_dice=0.166533 val_pr_auc=0.313903 minutes=3.00
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:202:epoch=024/100 loss=0.064151 val_dice=0.172646 val_pr_auc=0.363963 minutes=3.08
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:210:epoch=025/100 loss=0.073862 val_dice=0.196468 val_pr_auc=0.386662 minutes=3.01
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:218:epoch=026/100 loss=0.072094 val_dice=0.132655 val_pr_auc=0.394473 minutes=2.98
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:226:epoch=027/100 loss=0.065739 val_dice=0.374149 val_pr_auc=0.413061 minutes=3.01
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:234:epoch=028/100 loss=0.068670 val_dice=0.317358 val_pr_auc=0.418032 minutes=3.12
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:242:epoch=029/100 loss=0.070705 val_dice=0.171511 val_pr_auc=0.374978 minutes=2.99
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:250:epoch=030/100 loss=0.064441 val_dice=0.323407 val_pr_auc=0.425493 minutes=3.18
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:258:epoch=031/100 loss=0.069248 val_dice=0.248666 val_pr_auc=0.454737 minutes=2.88
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:266:epoch=032/100 loss=0.061221 val_dice=0.377182 val_pr_auc=0.450258 minutes=3.05
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:274:epoch=033/100 loss=0.062718 val_dice=0.327263 val_pr_auc=0.424330 minutes=2.95
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:282:epoch=034/100 loss=0.063943 val_dice=0.247668 val_pr_auc=0.459621 minutes=3.10
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:290:epoch=035/100 loss=0.058946 val_dice=0.092848 val_pr_auc=0.377327 minutes=2.93
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:298:epoch=036/100 loss=0.059221 val_dice=0.481173 val_pr_auc=0.501920 minutes=3.02
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:306:epoch=037/100 loss=0.053694 val_dice=0.232841 val_pr_auc=0.466201 minutes=2.99
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:314:epoch=038/100 loss=0.061848 val_dice=0.460287 val_pr_auc=0.494024 minutes=3.04
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:322:epoch=039/100 loss=0.057948 val_dice=0.371737 val_pr_auc=0.489074 minutes=3.08
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:330:epoch=040/100 loss=0.059008 val_dice=0.406601 val_pr_auc=0.503391 minutes=3.08
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:338:epoch=041/100 loss=0.056795 val_dice=0.441511 val_pr_auc=0.519499 minutes=3.02
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:346:epoch=042/100 loss=0.065448 val_dice=0.413127 val_pr_auc=0.536155 minutes=3.01
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:354:epoch=043/100 loss=0.059635 val_dice=0.239140 val_pr_auc=0.526799 minutes=2.99
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:362:epoch=044/100 loss=0.069650 val_dice=0.433576 val_pr_auc=0.552912 minutes=3.09
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:370:epoch=045/100 loss=0.055908 val_dice=0.435073 val_pr_auc=0.542746 minutes=2.97
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:378:epoch=046/100 loss=0.054000 val_dice=0.487242 val_pr_auc=0.555513 minutes=2.88
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:386:epoch=047/100 loss=0.055662 val_dice=0.378074 val_pr_auc=0.507225 minutes=3.08
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:394:epoch=048/100 loss=0.059597 val_dice=0.478686 val_pr_auc=0.550781 minutes=3.11
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:402:epoch=049/100 loss=0.059587 val_dice=0.516431 val_pr_auc=0.572820 minutes=3.02
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/run_config.json:5:  "precision": "float16_autocast",
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/run_config.json:746:  "threshold_selection": "best Dice on complete validation volume with 2048 bins",
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/status.json:7:  "precision": "float16_autocast",
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/status.json:12:  "best_checkpoint": "runs/R100_fp16_clean_3seeds_20261014_150435/seed44/best.pt",
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/validation_selection.json:7:    "dice": 0.5729798256899185,
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/validation_selection.json:8:    "iou": 0.40152188175400944,
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/validation_selection.json:9:    "precision": 0.5655692044103381,
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/validation_selection.json:10:    "recall": 0.5805872272731943,
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/validation_selection.json:16:    "roc_auc_approx": 0.9589852925995812,
runs/R100_fp16_clean_3seeds_20261014_150435/smoke.log:5:/shared/home/khavarj/projects/fault_detection/.venv_train/lib/python3.13/site-packages/torch/autograd/graph.py:824: UserWarning: max_pool3d_with_indices_backward_cuda does not have a deterministic implementation, but you set 'torch.use_deterministic_algorithms(True, warn_only=True)'. You can file an issue at https://github.com/pytorch/pytorch/issues to help us prioritize adding deterministic support for this operation. (Triggered internally at /pytorch/aten/src/ATen/Context.cpp:93.)
runs/R100_fp16_clean_3seeds_20261014_150435/smoke.log:12:epoch=001/1 loss=0.779829 val_dice=0.068725 val_pr_auc=0.033207 minutes=0.17
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/best.pt: binary file matches (found "\0" byte around offset 4)
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/history.csv:1:epoch,train_loss,train_patches,resampled_no_data_candidates,excluded_training_positive_labels,seconds,val_threshold,val_dice,val_iou,val_precision,val_recall,val_specificity,val_balanced_accuracy,val_accuracy,val_mcc,val_pr_auc_approx,val_roc_auc_approx,val_tp,val_fp,val_fn,val_tn
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/last.pt: binary file matches (found "\0" byte around offset 4)
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/run_config.json:5:  "precision": "float16_autocast",
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/run_config.json:116:  "threshold_selection": "best Dice on smoke validation subset",
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/status.json:7:  "precision": "float16_autocast",
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/status.json:12:  "best_checkpoint": "runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/best.pt",
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/validation_selection.json:7:    "dice": 0.06884626641830875,
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/validation_selection.json:8:    "iou": 0.035650329241587765,
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/validation_selection.json:9:    "precision": 0.035650329241587765,
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/validation_selection.json:10:    "recall": 1.0,
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/validation_selection.json:16:    "roc_auc_approx": 0.4517016441816569,
runs/R100_thebe_seed42_20261005_102737/best.pt: binary file matches (found "\0" byte around offset 4)
runs/R100_thebe_seed42_20261005_102737/final_metrics.json:23:    "dice": 0.5454089882642815,
runs/R100_thebe_seed42_20261005_102737/final_metrics.json:26:    "iou": 0.3749569355673811,
runs/R100_thebe_seed42_20261005_102737/final_metrics.json:29:    "precision": 0.5279583306670493,
runs/R100_thebe_seed42_20261005_102737/final_metrics.json:30:    "recall": 0.5640526757282134,
runs/R100_thebe_seed42_20261005_102737/final_metrics.json:31:    "roc_auc_approx": 0.9541044799759987,
runs/R100_thebe_seed42_20261005_102737/final_metrics.json:55:    "dice": 0.5429955056245461,
runs/R100_thebe_seed42_20261005_102737/final_metrics.json:58:    "iou": 0.37267936215756264,
runs/R100_thebe_seed42_20261005_102737/final_metrics.json:61:    "precision": 0.47191760787630943,
runs/R100_thebe_seed42_20261005_102737/final_metrics.json:62:    "recall": 0.6392808237987413,
runs/R100_thebe_seed42_20261005_102737/final_metrics.json:63:    "roc_auc_approx": 0.9604589545976385,
runs/R100_thebe_seed42_20261005_102737/final_metrics.json:91:    "dice": {
runs/R100_thebe_seed42_20261005_102737/final_metrics.json:105:    "iou": {
runs/R100_thebe_seed42_20261005_102737/final_metrics.json:133:    "precision": {
runs/R100_thebe_seed42_20261005_102737/final_metrics.json:140:    "recall": {
runs/R100_thebe_seed42_20261005_102737/final_metrics.json:147:    "roc_auc_approx": {
runs/R100_thebe_seed42_20261005_102737/history.csv:1:epoch,train_loss,train_patches,resampled_no_data_candidates,excluded_training_positive_labels,seconds,val_threshold,val_dice,val_iou,val_precision,val_recall,val_specificity,val_balanced_accuracy,val_accuracy,val_mcc,val_pr_auc_approx,val_roc_auc_approx,val_tp,val_fp,val_fn,val_tn
runs/R100_thebe_seed42_20261005_102737/last.pt: binary file matches (found "\0" byte around offset 4)
runs/R100_thebe_seed42_20261005_102737/resume_protocol.json:3:  "old_selection": "Dice at threshold 0.5 on fixed 128 validation patches",
runs/R100_thebe_seed42_20261005_102737/resume_protocol.json:5:  "why": "Near-zero Dice at 0.5 despite improving PR-AUC; final threshold remains full-validation only",
runs/R100_thebe_seed42_20261005_102737/resume_protocol.json:6:  "best_existing_checkpoint_matches_new_selection": true,
runs/R100_thebe_seed42_20261005_102737/run_config.json:51:  "checkpoint_selection": "highest Dice at 0.5 on fixed validation subset",
runs/R100_thebe_seed42_20261005_102737/run_config.json:52:  "threshold_selection": "best Dice on complete validation volume with 2048 bins",
runs/R100_thebe_seed42_20261005_102737/test_per_patch.csv:1:patch_id,raw_voxels,valid_voxels,excluded_positive,inference_seconds,threshold,dice,iou,precision,recall,specificity,balanced_accuracy,accuracy,mcc,pr_auc_approx,roc_auc_approx,tp,fp,fn,tn,modified_hausdorff_voxels,bidirectional_chamfer_voxels,prediction_empty,target_empty
runs/R100_thebe_seed42_20261005_102737/validation_selection.json:7:    "dice": 0.5454089882642815,
runs/R100_thebe_seed42_20261005_102737/validation_selection.json:8:    "iou": 0.3749569355673811,
runs/R100_thebe_seed42_20261005_102737/validation_selection.json:9:    "precision": 0.5279583306670493,
runs/R100_thebe_seed42_20261005_102737/validation_selection.json:10:    "recall": 0.5640526757282134,
runs/R100_thebe_seed42_20261005_102737/validation_selection.json:16:    "roc_auc_approx": 0.9541044799759987,
```

### Errors and numerical warnings

```text
reports/attention3d_identity_audit_20261014.txt:109:./reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:431:                raise RuntimeError(f"No Thebe files found for split {split}")
reports/attention3d_identity_audit_20261014.txt:110:./reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:481:                            raise RuntimeError("Fortran-order Thebe arrays are not supported")
reports/attention3d_identity_audit_20261014.txt:117:./reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:700:    272:            raise RuntimeError(f"No Thebe files found for split {split}")
reports/attention3d_identity_audit_20261014.txt:118:./reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:742:    322:                        raise RuntimeError("Fortran-order Thebe arrays are not supported")
reports/attention3d_identity_audit_20261014.txt:152:./reports/p1_thebe_setup.txt:87:            raise RuntimeError("No Thebe test H5 files were supplied")
reports/attention3d_identity_audit_20261014.txt:273: 1695  for f in   reports/training/paper_attention3d_thebe_supervised_seed42_resume.log   reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log; do     echo;     echo "============================================================";     echo "LOG: $f";     stat -c 'modified=%y  bytes=%s' "$f";      echo "--- START ---";     sed -n '1,12p' "$f";      echo "--- LAST 5 COMPLETED EPOCHS ---";     rg '^EPOCH ' "$f" | tail -5;      echo "--- COMPLETION, FAILURE, OR NaN MARKERS ---";     rg -ni       'training complete|completed|finished|done|traceback|killed|terminated|out of memory|cuda error|exception|nan'       "$f" | tail -30 || true;      echo "--- FINAL 25 RAW LINES ---";     tail -25 "$f"; done
reports/attention3d_identity_audit_20261014.txt:304: 1793  {     echo "=== REPOSITORY ===";     date -Is;     pwd;     git status --short;     git log -15 --date=iso --pretty='format:%h %ad %s';      echo;     echo "=== RELEVANT DOCUMENTATION ===";     rg -n -i 'attention3d|bf16|r100|thebe|seed42|roadmap'       --glob '*.md' --glob '*.txt'       --glob '!reports/training/**'       --glob '!runs/**' . || true;      echo;     echo "=== RELEVANT LAUNCH HISTORY ===";     history | rg -i       'paper_attention3d|bf16_clean|train_paper_attention3d_thebe|R100_thebe' || true;     rg -n -i       'paper_attention3d|bf16_clean|train_paper_attention3d_thebe|R100_thebe'       ~/.bash_history 2>/dev/null || true;      echo;     echo "=== TRAINING SCRIPT METADATA ===";     stat scripts/train_paper_attention3d_thebe.py;     sha256sum scripts/train_paper_attention3d_thebe.py;     rg -n -i       'bf16|bfloat|autocast|scaler|resume|sampler|balance|fault.patch|seed|run.dir|learning.rate'       scripts/train_paper_attention3d_thebe.py || true;      echo;     echo "=== UNCOMMITTED SCRIPT CHANGES ===";     git diff -- scripts/train_paper_attention3d_thebe.py;      echo;     echo "=== SCRIPT HISTORY ===";     git log -10 --date=iso --stat -- scripts/train_paper_attention3d_thebe.py;      echo;     echo "=== FILES MODIFIED ON OCTOBER 12 ===";     find scripts configs -type f       -newermt '2026-10-12 00:00:00'       ! -newermt '2026-10-13 00:00:00'       -printf '%TY-%Tm-%Td %TH:%TM:%TS %p\n' 2>/dev/null |       sort;      echo;     echo "=== RUN AND LOG FILES ===";     find runs reports/training -maxdepth 2       -name 'paper_attention3d_thebe_supervised_seed42*'       -printf '%TY-%Tm-%Td %TH:%TM:%TS %s %p\n' |       sort;      echo;     echo "=== TERMINATION EVIDENCE ===";     journalctl --since '2026-10-12 12:10:00'       --until '2026-10-12 12:40:00' --no-pager 2>/dev/null |       rg -i 'oom|killed process|python|nvidia|cuda|segfault' || true;      journalctl --since '2026-10-12 23:30:00'       --until '2026-10-13 00:00:00' --no-pager 2>/dev/null |       rg -i 'oom|killed process|python|nvidia|cuda|segfault' || true; } > "$audit" 2>&1
reports/attention3d_identity_audit_20261014.txt:325:1896:for f in   reports/training/paper_attention3d_thebe_supervised_seed42_resume.log   reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log; do     echo;     echo "============================================================";     echo "LOG: $f";     stat -c 'modified=%y  bytes=%s' "$f";      echo "--- START ---";     sed -n '1,12p' "$f";      echo "--- LAST 5 COMPLETED EPOCHS ---";     rg '^EPOCH ' "$f" | tail -5;      echo "--- COMPLETION, FAILURE, OR NaN MARKERS ---";     rg -ni       'training complete|completed|finished|done|traceback|killed|terminated|out of memory|cuda error|exception|nan'       "$f" | tail -30 || true;      echo "--- FINAL 25 RAW LINES ---";     tail -25 "$f"; done
reports/attention3d_identity_audit_20261014.txt:387:216:        raise RuntimeError(f"Nonempty run directory without resumable checkpoint: {run_dir}")
reports/data_audit/cracks_masks_run.log:2:Traceback (most recent call last):
reports/data_audit/cracks_masks_run.log:8:    raise RuntimeError(f"Unexpected mask values {labels.tolist()}: {mask_path}")
reports/data_audit/cracks_masks_run.log:9:RuntimeError: Unexpected mask values [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]: data/cracks/Fault segmentations/novice17/section_001.png
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:315:        raise RuntimeError(f"Empty manifest: {path}")
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:317:        raise RuntimeError(f"Duplicate IDs in manifest: {path}")
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:344:                    raise RuntimeError(
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:360:            raise RuntimeError(f"NaN/Inf in pair {name}")
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:362:            raise RuntimeError(f"Non-binary label in {fault_path}")
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:369:            raise RuntimeError(f"Zero standard deviation in {seismic_path}")
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:394:        raise RuntimeError(f"Expected one NPY member, found {members}")
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:402:        raise RuntimeError("h5py is required: python -m pip install h5py") from exc
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:423:            raise RuntimeError(f"No Thebe files found for split {split}")
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:428:                raise RuntimeError(f"Missing pair for {seismic_npz}: {fault_npz}")
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:471:                        raise RuntimeError(f"Shape mismatch: {sshape} vs {fshape}")
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:473:                        raise RuntimeError("Fortran-order Thebe arrays are not supported")
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:479:                        raise RuntimeError(
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:535:60-            raise RuntimeError(
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:542:72-                raise RuntimeError(f"Wrong size: {fault_path}")
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:548:78-                raise RuntimeError(f"NaN/Inf found in pair {name}")
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:601:157:            raise RuntimeError(f"Expected indexed 2D mask, got {mask.shape}: {mask_path}")
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:604:160:            raise RuntimeError(f"Unexpected mask values {labels.tolist()}: {mask_path}")
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:651:227:        raise ValueError("Invalid NPY magic value")
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:658:234:        raise ValueError(f"Unsupported NPY version {(major, minor)}")
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:673:251-        raise RuntimeError("h5py is required: python -m pip install h5py") from exc
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:692:272:            raise RuntimeError(f"No Thebe files found for split {split}")
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:732:320:                        raise RuntimeError(f"Shape mismatch: {sshape} vs {fshape}")
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:734:322:                        raise RuntimeError("Fortran-order Thebe arrays are not supported")
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:771:364-                                raise RuntimeError(
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:772:365-                                    f"NaN/Inf in {seismic_npz}, section {section_index}"
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:784:392-                            raise RuntimeError("Unexpected trailing bytes in NPY data")
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log:1087:import mathimport reimport sysimport timefrom dataclasses import asdictfrom pathlib import Pathfrom typing import Anyimport h5pyimport numpy as npimport torchdef natural_key(path: Path) -> list[object]:    return [        int(part) if part.isdigit() else part.lower()        for part in re.split(r"(\d+)", path.name)    ]def load_baseline_module(path: Path):    specification = importlib.util.spec_from_file_location(        "faultseg3d_baseline_imported",        path,    )    if specification is None or specification.loader is None:        raise RuntimeError(f"Cannot import baseline module: {path}")    module = importlib.util.module_from_spec(specification)    sys.modules[specification.name] = module    specification.loader.exec_module(module)    return moduleclass ConcatenatedThebe:    """Read ordered test H5 blocks as one volume along axis zero."""    def __init__(self, paths: list[Path]) -> None:        if not paths:            raise RuntimeError("No Thebe test H5 files were supplied")        self.paths = paths        self.handles = [h5py.File(path, "r") for path in paths]        self.offsets: list[int] = []        self.lengths: list[int] = []        reference_tail: tuple[int, int] | None = None        running = 0        for path, handle in zip(self.paths, self.handles):            if "seismic" not in handle or "fault" not in handle:                raise RuntimeError(                    f"{path} must contain datasets named seismic and fault"                )            seismic_shape = tuple(handle["seismic"].shape)            fault_shape = tuple(handle["fault"].shape)            if seismic_shape != fault_shape or len(seismic_shape) != 3:                raise RuntimeError(                    f"Shape mismatch in {path}: "                    f"seismic={seismic_shape}, fault={fault_shape}"                )            if reference_tail is None:                reference_tail = seismic_shape[1:]            elif seismic_shape[1:] != reference_tail:                raise RuntimeError(                    f"Incompatible spatial shape in {path}: {seismic_shape}"                )            self.offsets.append(running)            self.lengths.append(seismic_shape[0])            running += seismic_shape[0]        assert reference_tail is not None        self.shape = (running, *reference_tail)    def close(self) -> None:        for handle in self.handles:            handle.close()    def read(        self,        key: str,        x0: int,        x1: int,        y0: int,        y1: int,        z0: int,        z1: int,    ) -> np.ndarray:        pieces: list[np.ndarray] = []        for offset, length, handle in zip(            self.offsets,            self.lengths,            self.handles,        ):            block_end = offset + length            overlap_start = max(x0, offset)            overlap_end = min(x1, block_end)            if overlap_start >= overlap_end:                continue            local_start = overlap_start - offset            local_end = overlap_end - offset            piece = np.asarray(                handle[key][local_start:local_end, y0:y1, z0:z1]            )            pieces.append(piece)        if not pieces:            raise RuntimeError(                f"No data read for {key}: "                f"x={x0}:{x1}, y={y0}:{y1}, z={z0}:{z1}"            )        if len(pieces) == 1:            return pieces[0]        return np.concatenate(pieces, axis=0)def summarize_rows(    rows: list[dict[str, Any]],) -> dict[str, dict[str, float]]:    selected = (        "dice",        "iou",        "precision",        "recall",        "specificity",        "balanced_accuracy",        "accuracy",        "mcc",        "pr_auc_approx",        "roc_auc_approx",        "modified_hausdorff_voxels",        "bidirectional_chamfer_voxels",        "inference_seconds",    )    summary: dict[str, dict[str, float]] = {}    for key in selected:        values = np.asarray(            [float(row[key]) for row in rows if key in row],            dtype=np.float64,        )        if values.size == 0:            continue        summary[key] = {            "mean": float(values.mean()),            "std": float(values.std()),            "median": float(np.median(values)),            "min": float(values.min()),            "max": float(values.max()),        }    return summarydef write_csv_atomic(path: Path, rows: list[dict[str, Any]]) -> None:    if not rows:        return    temporary = path.with_suffix(path.suffix + ".part")    with temporary.open("w", newline="", encoding="utf-8") as stream:        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))        writer.writeheader()        writer.writerows(rows)    temporary.replace(path)def middle_slices(array: np.ndarray) -> dict[str, np.ndarray]:    return {        "axis0": array[array.shape[0] // 2, :, :],        "axis1": array[:, array.shape[1] // 2, :],        "axis2": array[:, :, array.shape[2] // 2],    }def build_parser() -> argparse.ArgumentParser:    parser = argparse.ArgumentParser(description=__doc__)    parser.add_argument(        "--baseline-script",        type=Path,        default=Path("scripts/faultseg3d_baseline.py"),    )    parser.add_argument(        "--checkpoint",        type=Path,        default=Path(            "runs/baseline_A_synthetic_bce_seed42/best.pt"        ),    )    parser.add_argument(        "--threshold-metrics",        type=Path,        default=Path(            "runs/baseline_A_synthetic_bce_seed42/final_metrics.json"        ),    )    parser.add_argument(        "--thebe-root",        type=Path,        default=Path("data/processed/thebe_h5"),    )    parser.add_argument("--output-dir", type=Path, required=True)    parser.add_argument(        "--max-patches",        type=int,        default=None,        help="For smoke testing only. Omit for complete evaluation.",    )    parser.add_argument("--save-examples", type=int, default=12)    return parserdef main() -> None:    args = build_parser().parse_args()    if not torch.cuda.is_available():        raise RuntimeError(            "CUDA GPU is unavailable. Attach a GPU before evaluation."        )    required = (        args.baseline_script,        args.checkpoint,        args.threshold_metrics,    )    for path in required:        if not path.is_file():            raise FileNotFoundError(path)    if args.output_dir.exists() and any(args.output_dir.iterdir()):        raise RuntimeError(            f"Output directory is not empty: {args.output_dir}"        )    args.output_dir.mkdir(parents=True, exist_ok=True)    example_dir = args.output_dir / "prediction_examples"    example_dir.mkdir(parents=True, exist_ok=True)    test_files = sorted(        args.thebe_root.glob("test*.h5"),        key=natural_key,    )    if not test_files:        raise RuntimeError(            f"No official test*.h5 files found in {args.thebe_root}"        )    # Explicitly reject accidental train/validation use.    for path in test_files:        if not path.name.startswith("test"):            raise RuntimeError(f"Non-test file selected: {path}")    threshold_document = json.loads(        args.threshold_metrics.read_text(encoding="utf-8")    )    threshold = float(        threshold_document[            "threshold_selected_on_internal_validation"        ]    )    if not 0.0 < threshold < 1.0:        raise RuntimeError(f"Invalid frozen threshold: {threshold}")    baseline = load_baseline_module(args.baseline_script)    volume_shape = tuple(int(value) for value in baseline.VOLUME_SHAPE)    if len(volume_shape) != 3 or len(set(volume_shape)) != 1:        raise RuntimeError(            f"Expected a cubic baseline volume shape, got {volume_shape}"        )    patch_size = volume_shape[0]    checkpoint = torch.load(        args.checkpoint,        map_location="cpu",        weights_only=False,    )    if "model" not in checkpoint:        raise RuntimeError("Checkpoint does not contain model weights")    checkpoint_args = checkpoint.get("args", {})    histogram_bins = int(        checkpoint_args.get("histogram_bins", 2048)    )    device = torch.device("cuda")    model = baseline.FaultSeg3D().to(device)    model.load_state_dict(checkpoint["model"], strict=True)    model.eval()    for parameter in model.parameters():        parameter.requires_grad_(False)    torch.manual_seed(42)    np.random.seed(42)    torch.backends.cudnn.benchmark = False    torch.backends.cudnn.deterministic = True    torch.cuda.reset_peak_memory_stats()    reader = ConcatenatedThebe(test_files)    total_shape = reader.shape    x_starts = list(range(0, total_shape[0], patch_size))    y_starts = list(range(0, total_shape[1], patch_size))    z_starts = list(range(0, total_shape[2], patch_size))    coordinates = list(        itertools.product(x_starts, y_starts, z_starts)    )    full_patch_count = len(coordinates)    if args.max_patches is not None:        if args.max_patches <= 0:            raise ValueError("--max-patches must be positive")        coordinates = coordinates[: args.max_patches]    complete_evaluation = len(coordinates) == full_patch_count    run_configuration = {        "experiment": "A_to_T0_zero_shot",        "training_performed": False,        "weight_updates": 0,        "checkpoint": str(args.checkpoint),        "checkpoint_epoch": int(checkpoint.get("epoch", -1)),        "checkpoint_training_data": checkpoint_args.get(            "data_root",            "unknown",        ),        "threshold": threshold,        "threshold_source": str(args.threshold_metrics),        "threshold_selected_using_thebe": False,        "data_split": "official Thebe test only",        "test_files": [str(path) for path in test_files],        "test_block_count": len(test_files),        "concatenated_test_shape": list(total_shape),        "patch_shape": list(volume_shape),        "patch_count_planned": full_patch_count,        "patch_count_this_run": len(coordinates),        "complete_official_test_evaluation": complete_evaluation,        "normalization": (            "independent z-score on each valid 3D patch, "            "matching Baseline A"        ),        "axis_transform": "np.transpose, matching Baseline A",        "edge_policy": (            "zero-pad normalized inputs to 128^3; "            "exclude padding from every metric"        ),        "overlap_policy": (            "non-overlapping partition; every valid voxel evaluated once"        ),        "histogram_bins": histogram_bins,    }    (args.output_dir / "run_configuration.json").write_text(        json.dumps(run_configuration, indent=2, sort_keys=True),        encoding="utf-8",    )    aggregate = baseline.ProbabilityHistogram(histogram_bins)    rows: list[dict[str, Any]] = []    evaluated_voxels = 0    total_inference_seconds = 0.0    saved_examples = 0    started = time.time()    try:        for patch_number, (x0, y0, z0) in enumerate(            coordinates,            start=1,        ):            x1 = min(x0 + patch_size, total_shape[0])            y1 = min(y0 + patch_size, total_shape[1])            z1 = min(z0 + patch_size, total_shape[2])            size_x = x1 - x0            size_y = y1 - y0            size_z = z1 - z0            seismic_raw = reader.read(                "seismic", x0, x1, y0, y1, z0, z1            ).astype(np.float32, copy=False)            fault_raw = reader.read(                "fault", x0, x1, y0, y1, z0, z1            ).astype(np.uint8, copy=False)            expected_shape = (size_x, size_y, size_z)            if seismic_raw.shape != expected_shape:                raise RuntimeError(                    f"Unexpected seismic shape: "                    f"{seismic_raw.shape} != {expected_shape}"                )            if fault_raw.shape != expected_shape:                raise RuntimeError(                    f"Unexpected fault shape: "                    f"{fault_raw.shape} != {expected_shape}"                )            if not np.isfinite(seismic_raw).all():                raise RuntimeError(                    f"NaN/Inf in patch starting at {(x0, y0, z0)}"                )            if fault_raw.min() < 0 or fault_raw.max() > 1:                raise RuntimeError(                    f"Non-binary fault values at {(x0, y0, z0)}"                )            patch_mean = float(                seismic_raw.mean(dtype=np.float64)            )            patch_std = float(                seismic_raw.std(dtype=np.float64)            )            if not patch_std > 0.0:                raise RuntimeError(                    f"Zero seismic standard deviation at "                    f"{(x0, y0, z0)}"                )            seismic_normalized = (                seismic_raw - patch_mean            ) / patch_std            seismic_padded = np.zeros(                volume_shape,                dtype=np.float32,            )            fault_padded = np.zeros(                volume_shape,                dtype=np.float32,            )            seismic_padded[                :size_x, :size_y, :size_z            ] = seismic_normalized            fault_padded[                :size_x, :size_y, :size_z            ] = fault_raw            # Match Baseline A axis reversal.            seismic_model = np.ascontiguousarray(                np.transpose(seismic_padded),                dtype=np.float32,            )            fault_model = np.ascontiguousarray(                np.transpose(fault_padded),                dtype=np.float32,            )            model_input = torch.from_numpy(                seismic_model[None, None]            ).to(device)            target_tensor = torch.from_numpy(                fault_model            ).to(device)            torch.cuda.synchronize()            inference_started = time.perf_counter()            with torch.inference_mode():                with torch.autocast(                    device_type="cuda",                    dtype=torch.float16,                ):                    logits = model(model_input)                probability = torch.sigmoid(                    logits.float()                )[0, 0]            torch.cuda.synchronize()            inference_seconds = (                time.perf_counter() - inference_started            )            total_inference_seconds += inference_seconds            # Dimensions reverse after np.transpose.            valid_model_shape = (size_z, size_y, size_x)            valid_z, valid_y, valid_x = valid_model_shape            probability_valid = probability[                :valid_z, :valid_y, :valid_x            ]            target_valid = target_tensor[                :valid_z, :valid_y, :valid_x            ]            valid_voxels = (                valid_z * valid_y * valid_x            )            evaluated_voxels += valid_voxels            aggregate.update_probabilities(                probability_valid,                target_valid,            )            individual = baseline.ProbabilityHistogram(                histogram_bins            )            individual.update_probabilities(                probability_valid,                target_valid,            )            row: dict[str, Any] = {                "patch_id": (                    f"x{x0:04d}_y{y0:04d}_z{z0:04d}"                ),                "raw_x_start": x0,                "raw_x_stop": x1,                "raw_y_start": y0,                "raw_y_stop": y1,                "raw_z_start": z0,                "raw_z_stop": z1,                "valid_voxels": valid_voxels,                "normalization_mean": patch_mean,                "normalization_std": patch_std,                **asdict(individual.metrics(threshold)),            }            probability_numpy = (                probability_valid.detach().cpu().numpy()            )            target_numpy = (                target_valid.detach().cpu().numpy() >= 0.5            )            prediction_numpy = (                probability_numpy >= threshold            )            row.update(                baseline.structural_distances(                    prediction_numpy,                    target_numpy,                )            )            row["inference_seconds"] = inference_seconds            rows.append(row)            if (                saved_examples < args.save_examples                and bool(target_numpy.any())            ):                seismic_valid = seismic_model[                    :valid_z, :valid_y, :valid_x                ]                arrays: dict[str, np.ndarray] = {                    "coordinates_raw": np.asarray(                        [x0, x1, y0, y1, z0, z1],                        dtype=np.int32,                    ),                    "threshold": np.asarray(                        threshold,                        dtype=np.float32,                    ),                }                for prefix, array in (                    ("seismic", seismic_valid),                    ("probability", probability_numpy),                    ("target", target_numpy.astype(np.uint8)),                    (                        "prediction",                        prediction_numpy.astype(np.uint8),                    ),                ):                    for axis_name, image in middle_slices(                        array                    ).items():                        arrays[                            f"{prefix}_{axis_name}"                        ] = image                np.savez_compressed(                    example_dir                    / f"example_{saved_examples + 1:02d}_"                    f"{row['patch_id']}.npz",                    **arrays,                )                saved_examples += 1            if (                patch_number % 25 == 0                or patch_number == len(coordinates)            ):                write_csv_atomic(                    args.output_dir / "test_per_patch.csv",                    rows,                )                print(                    f"processed={patch_number}/"                    f"{len(coordinates)} "                    f"elapsed_minutes="                    f"{(time.time() - started) / 60.0:.2f}",                    flush=True,                )    finally:        reader.close()    if complete_evaluation:        expected_voxels = int(math.prod(total_shape))        if evaluated_voxels != expected_voxels:            raise RuntimeError(                f"Coverage failure: evaluated "                f"{evaluated_voxels} voxels, "                f"expected {expected_voxels}"            )    aggregate_metrics = asdict(        aggregate.metrics(threshold)    )    elapsed_seconds = time.time() - started    final_result = {        "experiment": "A_to_T0_zero_shot",        "status": (            "complete_official_test"            if complete_evaluation            else "smoke_test_only"        ),        "training_performed": False,        "weight_updates": 0,        "threshold": threshold,        "threshold_source": (            "Baseline A synthetic validation"        ),        "thebe_labels_used_for_threshold": False,        "official_thebe_test": aggregate_metrics,        "official_thebe_test_per_patch_summary": (            summarize_rows(rows)        ),        "data": {            "test_files": [str(path) for path in test_files],            "test_shape": list(total_shape),            "patch_shape": list(volume_shape),            "patches_evaluated": len(rows),            "full_patch_count": full_patch_count,            "evaluated_voxels": evaluated_voxels,            "expected_full_test_voxels": int(                math.prod(total_shape)            ),            "complete_coverage": complete_evaluation,            "overlap": False,            "padding_counted_in_metrics": False,        },        "efficiency": {            "wall_seconds": elapsed_seconds,            "total_model_inference_seconds": (                total_inference_seconds            ),            "mean_model_inference_seconds_per_patch": (                total_inference_seconds / len(rows)            ),            "peak_cuda_gib": (                torch.cuda.max_memory_allocated()                / 1024**3            ),        },        "prediction_examples_saved": saved_examples,        "metric_notes": {            "distance_units": "voxels",            "modified_hausdorff": (                "max of directed mean nearest-point distances"            ),            "bidirectional_chamfer": (                "sum of directed mean nearest-point distances"            ),            "one_empty_mask_policy": (                "valid-patch diagonal penalty"            ),            "important": (                "These results measure zero-shot transfer "                "from synthetic FaultSeg3D to real Thebe."            ),        },    }    temporary_json = (        args.output_dir / "final_metrics.json.part"    )    temporary_json.write_text(        json.dumps(            final_result,            indent=2,            sort_keys=True,        ),        encoding="utf-8",    )    temporary_json.replace(        args.output_dir / "final_metrics.json"    )    write_csv_atomic(        args.output_dir / "test_per_patch.csv",        rows,    )    print("\n=== ZERO-SHOT RESULT ===")    print(f"status={final_result['status']}")    print(f"threshold={threshold:.6f}")    print(        f"dice={aggregate_metrics['dice']:.6f}"    )    print(        f"iou={aggregate_metrics['iou']:.6f}"    )    print(        f"precision={aggregate_metrics['precision']:.6f}"    )    print(        f"recall={aggregate_metrics['recall']:.6f}"[7m    )[27m[7m    print([27m[7m        f"mcc={aggregate_metrics['mcc']:.6f}"[27m[7m    )[27m[7m    print([27m[7m        f"pr_auc={aggregate_metrics['pr_auc_approx']:.6f}"[27m[7m    )[27m[7m    print([27m[7m        "results="[27m[7m        f"{args.output_dir / 'final_metrics.json'}"[27m[7m    )[27m[7mif __name__ == "__main__":[27m[7m    main()[27m[7mPY[27m[7mchmod +x scripts/evaluate_thebe_zero_shot.py[27m[7m.venv_train/bin/python -m py_compile \[27m[7m    scripts/evaluate_thebe_zero_shot.py[27m[7mecho "PASS: evaluator created and syntax checked."[27m    )    print(        f"mcc={aggregate_metrics['mcc']:.6f}"    )    print(        f"pr_auc={aggregate_metrics['pr_auc_approx']:.6f}"    )    print(        "results="        f"{args.output_dir / 'final_metrics.json'}"    )if __name__ == "__main__":    main()PYchmod +x scripts/evaluate_thebe_zero_shot.py.venv_train/bin/python -m py_compile \    scripts/evaluate_thebe_zero_shot.pyecho "PASS: evaluator created and syntax checked."
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:323:            raise RuntimeError(f"Empty manifest: {path}")
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:325:            raise RuntimeError(f"Duplicate IDs in manifest: {path}")
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:352:                        raise RuntimeError(
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:368:                raise RuntimeError(f"NaN/Inf in pair {name}")
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:370:                raise RuntimeError(f"Non-binary label in {fault_path}")
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:377:                raise RuntimeError(f"Zero standard deviation in {seismic_path}")
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:402:            raise RuntimeError(f"Expected one NPY member, found {members}")
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:410:            raise RuntimeError("h5py is required: python -m pip install h5py") from exc
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:431:                raise RuntimeError(f"No Thebe files found for split {split}")
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:436:                    raise RuntimeError(f"Missing pair for {seismic_npz}: {fault_npz}")
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:479:                            raise RuntimeError(f"Shape mismatch: {sshape} vs {fshape}")
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:481:                            raise RuntimeError("Fortran-order Thebe arrays are not supported")
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:487:                            raise RuntimeError(
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:543:    60-            raise RuntimeError(
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:550:    72-                raise RuntimeError(f"Wrong size: {fault_path}")
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:556:    78-                raise RuntimeError(f"NaN/Inf found in pair {name}")
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:609:    157:            raise RuntimeError(f"Expected indexed 2D mask, got {mask.shape}: {mask_path}")
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:612:    160:            raise RuntimeError(f"Unexpected mask values {labels.tolist()}: {mask_path}")
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:659:    227:        raise ValueError("Invalid NPY magic value")
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:666:    234:        raise ValueError(f"Unsupported NPY version {(major, minor)}")
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:681:    251-        raise RuntimeError("h5py is required: python -m pip install h5py") from exc
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:700:    272:            raise RuntimeError(f"No Thebe files found for split {split}")
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:740:    320:                        raise RuntimeError(f"Shape mismatch: {sshape} vs {fshape}")
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:742:    322:                        raise RuntimeError("Fortran-order Thebe arrays are not supported")
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:779:    364-                                raise RuntimeError(
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:780:    365-                                    f"NaN/Inf in {seismic_npz}, section {section_index}"
reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md:792:    392-                            raise RuntimeError("Unexpected trailing bytes in NPY data")
reports/debug/cracks_evaluation_context.md:36:0029:         raise RuntimeError(f"Unexpected filename: {path}")
reports/debug/cracks_evaluation_context.md:42:0035:         raise RuntimeError(f"Image dimension {length} is smaller than {PATCH}")
reports/debug/cracks_evaluation_context.md:76:0069:         raise RuntimeError("CUDA GPU is required")
reports/debug/cracks_evaluation_context.md:78:0071:         raise RuntimeError(f"Output directory is not empty: {args.output_dir}")
reports/debug/cracks_evaluation_context.md:86:0079:         raise RuntimeError(f"Expected 40 expert labels, found {len(label_paths)}")
reports/debug/cracks_evaluation_context.md:100:0110:             raise RuntimeError(f"Expected indexed label PNG, got {raw.shape}: {path}")
reports/debug/cracks_evaluation_context.md:103:0113:             raise RuntimeError(f"Unexpected label values {sorted(unique)} in {path}")
reports/debug/cracks_evaluation_context.md:105:0115:             raise RuntimeError(
reports/debug/cracks_evaluation_context.md:154:0191:             raise RuntimeError(f"Incomplete spatial coverage for section {number}")
reports/debug/cracks_evaluation_context.md:158:0195:             raise RuntimeError(f"No certain expert pixels in {label_path}")
reports/evaluation/baseline_A_zero_shot_thebe_smoke_20261005_091638_diagnostic.md:13:Traceback (most recent call last):
reports/evaluation/baseline_A_zero_shot_thebe_smoke_20261005_091638_diagnostic.md:14:    raise RuntimeError(
reports/evaluation/baseline_A_zero_shot_thebe_smoke_20261005_091638_diagnostic.md:15:RuntimeError: Zero seismic standard deviation at (0, 0, 0)
reports/evaluation/baseline_A_zero_shot_thebe_smoke_20261005_091638_diagnostic.md:21:Traceback (most recent call last):
reports/evaluation/baseline_A_zero_shot_thebe_smoke_20261005_091638_diagnostic.md:26:    raise RuntimeError(
reports/evaluation/baseline_A_zero_shot_thebe_smoke_20261005_091638_diagnostic.md:29:RuntimeError: Zero seismic standard deviation at (0, 0, 0)
reports/evaluation/baseline_A_zero_shot_thebe_smoke_20261005_091638_diagnostic.md:35:Traceback (most recent call last):
reports/evaluation/baseline_A_zero_shot_thebe_smoke_20261005_091638_diagnostic.md:40:    raise RuntimeError(
reports/evaluation/baseline_A_zero_shot_thebe_smoke_20261005_091638_diagnostic.md:43:RuntimeError: Zero seismic standard deviation at (0, 0, 0)
reports/evaluation/baseline_A_zero_shot_thebe_smoke_20261005_091638.log:1:Traceback (most recent call last):
reports/evaluation/baseline_A_zero_shot_thebe_smoke_20261005_091638.log:6:    raise RuntimeError(
reports/evaluation/baseline_A_zero_shot_thebe_smoke_20261005_091638.log:9:RuntimeError: Zero seismic standard deviation at (0, 0, 0)
reports/evaluation/THEBE_EVALUATOR_EDIT_CONTEXT.md:39:0296:         raise RuntimeError(f"Invalid frozen threshold: {threshold}")
reports/evaluation/THEBE_EVALUATOR_EDIT_CONTEXT.md:161:0423:                 raise RuntimeError(
reports/evaluation/THEBE_EVALUATOR_EDIT_CONTEXT.md:166:0428:                 raise RuntimeError(
reports/evaluation/THEBE_EVALUATOR_EDIT_CONTEXT.md:172:0434:                 raise RuntimeError(
reports/evaluation/THEBE_EVALUATOR_EDIT_CONTEXT.md:173:0435:                     f"NaN/Inf in patch starting at {(x0, y0, z0)}"
reports/evaluation/THEBE_EVALUATOR_EDIT_CONTEXT.md:176:0438:                 raise RuntimeError(
reports/evaluation/THEBE_EVALUATOR_EDIT_CONTEXT.md:187:0449:                 raise RuntimeError(
reports/evaluation/THEBE_EVALUATOR_EDIT_CONTEXT.md:380:0642:             raise RuntimeError(
reports/evaluation/THEBE_EVALUATOR_EDIT_CONTEXT.md:411:0642:             raise RuntimeError(
reports/p1_thebe_setup.txt:74:        raise RuntimeError(f"Cannot import baseline module: {path}")
reports/p1_thebe_setup.txt:87:            raise RuntimeError("No Thebe test H5 files were supplied")
reports/p1_thebe_setup.txt:99:                raise RuntimeError(
reports/p1_thebe_setup.txt:107:                raise RuntimeError(
reports/p1_thebe_setup.txt:115:                raise RuntimeError(
reports/p1_thebe_setup.txt:163:            raise RuntimeError(
reports/p1_thebe_setup.txt:286:        raise RuntimeError(
reports/p1_thebe_setup.txt:300:        raise RuntimeError(
reports/p1_thebe_setup.txt:313:        raise RuntimeError(
reports/p1_thebe_setup.txt:320:            raise RuntimeError(f"Non-test file selected: {path}")
reports/p1_thebe_setup.txt:332:        raise RuntimeError(f"Invalid frozen threshold: {threshold}")
reports/p1_thebe_setup.txt:338:        raise RuntimeError(
reports/p1_thebe_setup.txt:349:        raise RuntimeError("Checkpoint does not contain model weights")
reports/p1_thebe_setup.txt:384:            raise ValueError("--max-patches must be positive")
reports/p1_thebe_setup.txt:414:            raise RuntimeError(
reports/p1_thebe_setup.txt:415:                f"NaN/Inf while building trace mask at "
reports/p1_thebe_setup.txt:517:                raise RuntimeError(
reports/p1_thebe_setup.txt:522:                raise RuntimeError(
reports/p1_thebe_setup.txt:529:                raise RuntimeError(
reports/p1_thebe_setup.txt:530:                    f"NaN/Inf in patch starting at {(x0, y0, z0)}"
reports/p1_thebe_setup.txt:533:                raise RuntimeError(
reports/p1_thebe_setup.txt:582:                    raise RuntimeError(
reports/p1_thebe_setup.txt:819:            raise RuntimeError(
reports/p1_thebe_setup.txt:992:175-            raise RuntimeError("P1 model was not initialized")
reports/paper_attention3d_thebe_supervised_seed42.log:248:Traceback (most recent call last):
reports/paper_attention3d_thebe_supervised_seed42.log:263:    raise RuntimeError(
reports/paper_attention3d_thebe_supervised_seed42.log:266:RuntimeError: Unable to sample valid patch for index 13; inspect the Thebe H5 labels
reports/r100_launch_check_20261014_133445.txt:359:            raise RuntimeError(f"Missing source file: {path}")
reports/r100_launch_check_20261014_133445.txt:362:            raise RuntimeError(
reports/r100_launch_check_20261014_133445.txt:367:        raise RuntimeError("Baseline A patch size changed")
reports/r100_launch_check_20261014_133445.txt:374:        raise RuntimeError(f"Expected exactly {expected}; found {paths}")
reports/r100_launch_check_20261014_133445.txt:376:        raise RuntimeError(f"Missing H5 file in {paths}")
reports/r100_launch_check_20261014_133445.txt:392:        raise RuntimeError(f"Patch shape mismatch at {origin}")
reports/r100_launch_check_20261014_133445.txt:394:        raise RuntimeError(f"Nonfinite seismic at {origin}")
reports/r100_launch_check_20261014_133445.txt:396:        raise RuntimeError(f"Nonbinary label at {origin}")
reports/r100_launch_check_20261014_133445.txt:410:            raise RuntimeError(f"Nonfinite seismic scale at {origin}")
reports/r100_launch_check_20261014_133445.txt:528:        raise RuntimeError("CUDA GPU required for the full R100 run")
reports/r100_launch_check_20261014_133445.txt:531:        raise RuntimeError(f"Insufficient free GPU memory: {free_gpu / 1024**3:.1f} GiB")
reports/r100_launch_check_20261014_133445.txt:536:        raise RuntimeError("Train/validation/test files overlap")
reports/r100_launch_check_20261014_133445.txt:539:            raise RuntimeError(f"Resume directory does not exist: {args.run_dir}")
reports/r100_launch_check_20261014_133445.txt:541:        raise RuntimeError(f"Run directory already exists: {args.run_dir}")
reports/r100_launch_check_20261014_133445.txt:546:            raise RuntimeError(f"Unexpected Thebe shapes: {train_reader.shape}, {val_reader.shape}")
reports/r100_launch_check_20261014_133445.txt:553:            raise RuntimeError(f"Unexpected model parameter count: {parameters}")
reports/r100_launch_check_20261014_133445.txt:583:                raise RuntimeError("Resume needs last.pt, best.pt, and history.csv")
reports/r100_launch_check_20261014_133445.txt:590:                raise RuntimeError("Checkpoint epoch and history.csv disagree; inspect before resuming")
reports/r100_launch_check_20261014_133445.txt:592:                raise RuntimeError(f"Training already reached epoch {completed}; resume is not needed")
reports/r100_launch_check_20261014_133445.txt:600:                raise RuntimeError(
reports/r100_launch_check_20261014_133445.txt:652:                    raise RuntimeError(f"Unable to sample observed training data from {train_files[file_index]}")
reports/r100_launch_check_20261014_133445.txt:673:                raise RuntimeError("No observed voxels in validation subset")
reports/r100_launch_check_20261014_133445.txt:698:            raise RuntimeError("Incomplete validation coverage")
reports/r100_launch_check_20261014_133445.txt:717:            raise RuntimeError(f"Unexpected test shape: {test_reader.shape}")
reports/r100_launch_check_20261014_133445.txt:723:            raise RuntimeError("Incomplete test coverage")
reports/r100_launch_check_20261014_133445.txt:725:            raise RuntimeError("No observed voxels scored in test")
reports/r100_launch_check_20261014_133445.txt:824:            raise RuntimeError(f"Missing source file: {path}")
reports/r100_launch_check_20261014_133445.txt:827:            raise RuntimeError(
reports/r100_launch_check_20261014_133445.txt:832:        raise RuntimeError("Baseline A patch size changed")
reports/r100_launch_check_20261014_133445.txt:839:        raise RuntimeError(f"Expected exactly {expected}; found {paths}")
reports/r100_launch_check_20261014_133445.txt:841:        raise RuntimeError(f"Missing H5 file in {paths}")
reports/r100_launch_check_20261014_133445.txt:857:        raise RuntimeError(f"Patch shape mismatch at {origin}")
reports/r100_launch_check_20261014_133445.txt:859:        raise RuntimeError(f"Nonfinite seismic at {origin}")
reports/r100_launch_check_20261014_133445.txt:861:        raise RuntimeError(f"Nonbinary label at {origin}")
reports/r100_launch_check_20261014_133445.txt:874:            raise RuntimeError(f"Constant observed seismic at {origin}")
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:129:EPOCH 074 train_loss=0.412175 val_loss=nan val_dice=0.429887 val_precision=0.315779 val_recall=0.673122 best=0.539004 elapsed_min=205.2
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:131:epoch=75/100 train_patch=32/64 loss=nan
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:133:epoch=75/100 train_patch=64/64 loss=nan
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:134:EPOCH 075 train_loss=nan val_loss=nan val_dice=0.267436 val_precision=0.199014 val_recall=0.407552 best=0.539004 elapsed_min=213.2
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:135:epoch=76/100 train_patch=16/64 loss=nan
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:138:epoch=76/100 train_patch=64/64 loss=nan
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:139:EPOCH 076 train_loss=nan val_loss=nan val_dice=0.267436 val_precision=0.199014 val_recall=0.407552 best=0.539004 elapsed_min=221.2
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:140:epoch=77/100 train_patch=16/64 loss=nan
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:142:epoch=77/100 train_patch=48/64 loss=nan
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:144:EPOCH 077 train_loss=nan val_loss=nan val_dice=0.257658 val_precision=0.186943 val_recall=0.414424 best=0.539004 elapsed_min=229.1
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:145:epoch=78/100 train_patch=16/64 loss=nan
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:147:epoch=78/100 train_patch=48/64 loss=nan
reports/training/r100_fp16_3seed_queue_20261014_145225.log:3:Traceback (most recent call last):
reports/training/r100_fp16_3seed_queue_20261014_145225.log:14:    raise RuntimeError(message)
reports/training/r100_fp16_3seed_queue_20261014_145225.log:15:RuntimeError: Trainer exited with code 1; see runs/R100_fp16_clean_3seeds_20261014_145225/smoke.log
reports/training/r100_fp16_3seed_queue_20261014_145510.log:3:Traceback (most recent call last):
reports/training/r100_fp16_3seed_queue_20261014_145510.log:14:    raise RuntimeError(message)
reports/training/r100_fp16_3seed_queue_20261014_145510.log:15:RuntimeError: Trainer exited with code 1; see runs/R100_fp16_clean_3seeds_20261014_145510/seed42.log
reports/training/R100_thebe_seed42_20261005_102737.log:57:Traceback (most recent call last):
reports/training/R100_thebe_seed42_20261005_102737.log:69:    raise RuntimeError(f"Constant observed seismic at {origin}")
reports/training/R100_thebe_seed42_20261005_102737.log:70:RuntimeError: Constant observed seismic at (203, 1696, 199)
runs/baseline_A_synthetic_bce_seed42/best.pt: binary file matches (found "\0" byte around offset 4)
runs/baseline_A_synthetic_bce_seed42/last.pt: binary file matches (found "\0" byte around offset 4)
runs/loss_ablation_L1_weighted_bce_dice_seed42/best.pt: binary file matches (found "\0" byte around offset 4)
runs/loss_ablation_L1_weighted_bce_dice_seed42/last.pt: binary file matches (found "\0" byte around offset 4)
runs/p1_attention3d_caft_seed42/best_p1_attention3d_caft_seed42_epoch093_faultseg3d_synthetic_20261009.pt: binary file matches (found "\0" byte around offset 4)
runs/p1_attention3d_caft_seed42/best.pt: binary file matches (found "\0" byte around offset 4)
runs/p1_attention3d_caft_seed42/last.pt: binary file matches (found "\0" byte around offset 4)
runs/paper_attention3d_thebe_supervised_seed42/best.pt: binary file matches (found "\0" byte around offset 4)
runs/paper_attention3d_thebe_supervised_seed42_bf16_clean/best.pt: binary file matches (found "\0" byte around offset 4)
runs/paper_attention3d_thebe_supervised_seed42_bf16_clean/last.pt: binary file matches (found "\0" byte around offset 4)
runs/paper_attention3d_thebe_supervised_seed42/history.csv:75:74,0.41217497378238477,nan,0.42988675002435567,0.31577885344101436,0.6731219365809743,0.02601744759131709,0.00015555555555555556,12312.27090716362
runs/paper_attention3d_thebe_supervised_seed42/history.csv:76:75,nan,nan,0.2674355254780206,0.1990142826439499,0.40755226567970393,0.02601744759131709,0.0001501736111111111,12793.03427696228
runs/paper_attention3d_thebe_supervised_seed42/history.csv:77:76,nan,nan,0.2674355254780206,0.1990142826439499,0.40755226567970393,0.02601744759131709,0.00014479166666666666,13268.679413795471
runs/paper_attention3d_thebe_supervised_seed42/history.csv:78:77,nan,nan,0.2576584672648431,0.18694287706125617,0.41442432729818945,0.02601744759131709,0.0001394097222222222,13744.171303510666
runs/paper_attention3d_thebe_supervised_seed42/last.pt: binary file matches (found "\0" byte around offset 4)
runs/R100_fp16_clean_3seeds_20261014_145225/queue_status.json:20:  "error": "RuntimeError('Trainer exited with code 1; see runs/R100_fp16_clean_3seeds_20261014_145225/smoke.log')"
runs/R100_fp16_clean_3seeds_20261014_145225/smoke.log:3:Traceback (most recent call last):
runs/R100_fp16_clean_3seeds_20261014_145225/smoke.log:11:    raise RuntimeError(
runs/R100_fp16_clean_3seeds_20261014_145225/smoke.log:14:RuntimeError: scripts/evaluate_thebe_zero_shot.py changed since inspection. Expected 834ec8aeb8a726c51f6dd65e4f85fac7652dfcc13f8ab58f0784fe359b9374ec, got ebff17dcf7e143113567155a3fbb147d3c82bf311a1108c157eafcb3d837b30f. No training has started.
runs/R100_fp16_clean_3seeds_20261014_145510/queue_status.json:21:  "error": "RuntimeError('Trainer exited with code 1; see runs/R100_fp16_clean_3seeds_20261014_145510/seed42.log')"
runs/R100_fp16_clean_3seeds_20261014_145510/seed42.log:7:Traceback (most recent call last):
runs/R100_fp16_clean_3seeds_20261014_145510/seed42.log:15:    raise RuntimeError(f"Nonfinite tensor: {path}")
runs/R100_fp16_clean_3seeds_20261014_145510/seed42.log:16:RuntimeError: Nonfinite tensor: gradient.output.weight
runs/R100_fp16_clean_3seeds_20261014_145510/smoke_seed42/best.pt: binary file matches (found "\0" byte around offset 4)
runs/R100_fp16_clean_3seeds_20261014_145510/smoke_seed42/last.pt: binary file matches (found "\0" byte around offset 4)
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/best.pt: binary file matches (found "\0" byte around offset 4)
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/best.pt: binary file matches (found "\0" byte around offset 4)
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/last.pt: binary file matches (found "\0" byte around offset 4)
runs/R100_thebe_seed42_20261005_102737/best.pt: binary file matches (found "\0" byte around offset 4)
runs/R100_thebe_seed42_20261005_102737/last.pt: binary file matches (found "\0" byte around offset 4)
```

### Newest log tails

`runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log`

```text
epoch=97/100 train_patch=60/360 loss=0.191846
epoch=97/100 train_patch=120/360 loss=0.277550
epoch=97/100 train_patch=180/360 loss=0.091489
epoch=97/100 train_patch=240/360 loss=0.000342
epoch=97/100 train_patch=300/360 loss=0.000000
epoch=97/100 train_patch=360/360 loss=0.036241
evaluation_patches=100/128
epoch=097/100 loss=0.051889 val_dice=0.548214 val_pr_auc=0.633269 minutes=3.00
epoch=98/100 train_patch=60/360 loss=0.136171
epoch=98/100 train_patch=120/360 loss=0.000024
epoch=98/100 train_patch=180/360 loss=0.081139
epoch=98/100 train_patch=240/360 loss=0.116304
epoch=98/100 train_patch=300/360 loss=0.194777
epoch=98/100 train_patch=360/360 loss=0.003614
evaluation_patches=100/128
epoch=098/100 loss=0.047368 val_dice=0.417820 val_pr_auc=0.618263 minutes=3.19
epoch=99/100 train_patch=60/360 loss=0.096293
epoch=99/100 train_patch=120/360 loss=0.000711
epoch=99/100 train_patch=180/360 loss=0.053551
epoch=99/100 train_patch=240/360 loss=0.011706
epoch=99/100 train_patch=300/360 loss=0.030885
epoch=99/100 train_patch=360/360 loss=0.015740
evaluation_patches=100/128
epoch=099/100 loss=0.051740 val_dice=0.571887 val_pr_auc=0.641601 minutes=3.10
epoch=100/100 train_patch=60/360 loss=0.105558
epoch=100/100 train_patch=120/360 loss=0.000385
epoch=100/100 train_patch=180/360 loss=0.002327
epoch=100/100 train_patch=240/360 loss=0.000015
epoch=100/100 train_patch=300/360 loss=0.049922
epoch=100/100 train_patch=360/360 loss=0.008582
evaluation_patches=100/128
epoch=100/100 loss=0.050488 val_dice=0.544014 val_pr_auc=0.647909 minutes=2.94
BEST EPOCH: 95; full validation begins
evaluation_patches=100/650
evaluation_patches=200/650
evaluation_patches=400/650
evaluation_patches=500/650
VALIDATION THRESHOLD: 0.244141; test evaluation disabled
R100 VALIDATION-ONLY COMPLETE seed=44 epochs=100 best_epoch=95
QUEUE CHILD EXIT 2026-10-15T02:29:39.074418+00:00 code=0
```

`reports/training/r100_fp16_3seed_queue_20261014_150435.log`

```text
nohup: ignoring input
START seed=42 smoke=True pid=1945423 log=runs/R100_fp16_clean_3seeds_20261014_150435/smoke.log
START seed=42 smoke=False pid=1946437 log=runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log
PASS seed=42 validation_dice=0.544072
START seed=43 smoke=False pid=3264730 log=runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log
PASS seed=43 validation_dice=0.569856
START seed=44 smoke=False pid=379744 log=runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log
PASS seed=44 validation_dice=0.572980
THREE SEEDS COMPLETE validation Dice mean=0.562302 sample_SD=0.015865; no test evaluation
```

`runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log`

```text
epoch=97/100 train_patch=60/360 loss=0.000206
epoch=97/100 train_patch=120/360 loss=0.000322
epoch=97/100 train_patch=180/360 loss=0.000758
epoch=97/100 train_patch=240/360 loss=0.184065
epoch=97/100 train_patch=300/360 loss=0.005448
epoch=97/100 train_patch=360/360 loss=0.217553
evaluation_patches=100/128
epoch=097/100 loss=0.043323 val_dice=0.499799 val_pr_auc=0.628407 minutes=3.00
epoch=98/100 train_patch=60/360 loss=0.013608
epoch=98/100 train_patch=120/360 loss=0.090962
epoch=98/100 train_patch=180/360 loss=0.005916
epoch=98/100 train_patch=240/360 loss=0.000000
epoch=98/100 train_patch=300/360 loss=0.165707
epoch=98/100 train_patch=360/360 loss=0.094480
evaluation_patches=100/128
epoch=098/100 loss=0.050284 val_dice=0.579185 val_pr_auc=0.642430 minutes=3.08
epoch=99/100 train_patch=60/360 loss=0.118951
epoch=99/100 train_patch=120/360 loss=0.010276
epoch=99/100 train_patch=180/360 loss=0.000355
epoch=99/100 train_patch=240/360 loss=0.000069
epoch=99/100 train_patch=300/360 loss=0.011696
epoch=99/100 train_patch=360/360 loss=0.006897
evaluation_patches=100/128
epoch=099/100 loss=0.043900 val_dice=0.568614 val_pr_auc=0.648535 minutes=3.05
epoch=100/100 train_patch=60/360 loss=0.009470
epoch=100/100 train_patch=120/360 loss=0.002223
epoch=100/100 train_patch=180/360 loss=0.004774
epoch=100/100 train_patch=240/360 loss=0.000046
epoch=100/100 train_patch=300/360 loss=0.112857
epoch=100/100 train_patch=360/360 loss=0.013399
evaluation_patches=100/128
epoch=100/100 loss=0.048542 val_dice=0.477356 val_pr_auc=0.643192 minutes=3.15
BEST EPOCH: 93; full validation begins
evaluation_patches=100/650
evaluation_patches=200/650
evaluation_patches=400/650
evaluation_patches=500/650
VALIDATION THRESHOLD: 0.279297; test evaluation disabled
R100 VALIDATION-ONLY COMPLETE seed=43 epochs=100 best_epoch=93
QUEUE CHILD EXIT 2026-10-14T21:26:57.084942+00:00 code=0
```

## Seed 43

### Seed/run files

```text
reports/training/r100_fp16_3seed_queue_20261014_150435.log
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/best.pt
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/history.csv
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/last.pt
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/run_config.json
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/status.json
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/validation_selection.json
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/best.pt
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/history.csv
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/last.pt
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/run_config.json
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/status.json
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/validation_selection.json
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/best.pt
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/history.csv
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/last.pt
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/run_config.json
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/status.json
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/validation_selection.json
runs/R100_fp16_clean_3seeds_20261014_150435/smoke.log
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/best.pt
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/history.csv
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/last.pt
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/run_config.json
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/status.json
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/validation_selection.json
```

### Checkpoint metadata only

```text
2026-10-14T11:04:47.5321731820	17562443 bytes	runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/last.pt
2026-10-14T11:04:47.5634066030	17562443 bytes	runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/best.pt
2026-10-14T15:57:17.5696980420	17562443 bytes	runs/R100_fp16_clean_3seeds_20261014_150435/seed42/best.pt
2026-10-14T16:12:25.0497427080	17562443 bytes	runs/R100_fp16_clean_3seeds_20261014_150435/seed42/last.pt
2026-10-14T21:04:18.6093364070	17562443 bytes	runs/R100_fp16_clean_3seeds_20261014_150435/seed43/best.pt
2026-10-14T21:25:29.7404980360	17562443 bytes	runs/R100_fp16_clean_3seeds_20261014_150435/seed43/last.pt
2026-10-15T02:12:55.4137767480	17562443 bytes	runs/R100_fp16_clean_3seeds_20261014_150435/seed44/best.pt
2026-10-15T02:28:11.9270560240	17562443 bytes	runs/R100_fp16_clean_3seeds_20261014_150435/seed44/last.pt
```

### Settings

```text
reports/training/baseline_A_smoke.log:1:device=cuda; parameters=1,459,585; amp=True
reports/training/baseline_A_smoke.log:2:/shared/home/khavarj/projects/fault_detection/scripts/faultseg3d_baseline.py:553: FutureWarning: `torch.cuda.amp.GradScaler(args...)` is deprecated. Please use `torch.amp.GradScaler('cuda', args...)` instead.
reports/training/baseline_A_smoke.log:3:  scaler = torch.cuda.amp.GradScaler(enabled=amp_enabled)
reports/training/baseline_A_smoke.log:6:SMOKE PASS: input=(1, 1, 128, 128, 128), output=(1, 1, 128, 128, 128), loss=0.778994, peak_cuda_GiB=1.218
reports/training/baseline_A_synthetic_bce_seed42.log:2:device=cuda; parameters=1,459,585; amp=True
reports/training/baseline_A_synthetic_bce_seed42.log:3:/shared/home/khavarj/projects/fault_detection/scripts/faultseg3d_baseline.py:553: FutureWarning: `torch.cuda.amp.GradScaler(args...)` is deprecated. Please use `torch.amp.GradScaler('cuda', args...)` instead.
reports/training/baseline_A_synthetic_bce_seed42.log:4:  scaler = torch.cuda.amp.GradScaler(enabled=amp_enabled)
reports/training/baseline_A_synthetic_bce_seed42.log:11:epoch=001 loss=0.314965 val_dice=0.000000 val_iou=0.000000 val_pr_auc=0.076771 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:12:epoch=002 loss=0.254361 val_dice=0.000000 val_iou=0.000000 val_pr_auc=0.096252 minutes=0.30
reports/training/baseline_A_synthetic_bce_seed42.log:13:epoch=003 loss=0.238950 val_dice=0.000000 val_iou=0.000000 val_pr_auc=0.182016 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:14:epoch=004 loss=0.200252 val_dice=0.118262 val_iou=0.062847 val_pr_auc=0.390901 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:15:epoch=005 loss=0.168745 val_dice=0.398029 val_iou=0.248462 val_pr_auc=0.481942 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:16:epoch=006 loss=0.153221 val_dice=0.465434 val_iou=0.303300 val_pr_auc=0.539682 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:17:epoch=007 loss=0.141764 val_dice=0.497805 val_iou=0.331385 val_pr_auc=0.586533 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:18:epoch=008 loss=0.135450 val_dice=0.534810 val_iou=0.365011 val_pr_auc=0.613936 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:19:epoch=009 loss=0.128391 val_dice=0.600041 val_iou=0.428614 val_pr_auc=0.641996 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:20:epoch=010 loss=0.122253 val_dice=0.583450 val_iou=0.411881 val_pr_auc=0.643059 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:21:epoch=011 loss=0.118308 val_dice=0.619101 val_iou=0.448332 val_pr_auc=0.686354 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:22:epoch=012 loss=0.112667 val_dice=0.641208 val_iou=0.471895 val_pr_auc=0.700150 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:23:epoch=013 loss=0.109114 val_dice=0.633384 val_iou=0.463469 val_pr_auc=0.715915 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:24:epoch=014 loss=0.106602 val_dice=0.650868 val_iou=0.482435 val_pr_auc=0.711744 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:25:epoch=015 loss=0.102564 val_dice=0.666159 val_iou=0.499429 val_pr_auc=0.731226 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:26:epoch=016 loss=0.099363 val_dice=0.685561 val_iou=0.521562 val_pr_auc=0.750862 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:27:epoch=017 loss=0.097281 val_dice=0.687228 val_iou=0.523494 val_pr_auc=0.757492 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:28:epoch=018 loss=0.093142 val_dice=0.689824 val_iou=0.526513 val_pr_auc=0.765094 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:29:epoch=019 loss=0.093322 val_dice=0.693366 val_iou=0.530651 val_pr_auc=0.769579 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:30:epoch=020 loss=0.089892 val_dice=0.718609 val_iou=0.560804 val_pr_auc=0.786135 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:31:epoch=021 loss=0.088231 val_dice=0.706142 val_iou=0.545765 val_pr_auc=0.776918 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:2:device=cuda; parameters=1,459,585; amp=True
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:3:/shared/home/khavarj/projects/fault_detection/scripts/faultseg3d_baseline.py:553: FutureWarning: `torch.cuda.amp.GradScaler(args...)` is deprecated. Please use `torch.amp.GradScaler('cuda', args...)` instead.
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:4:  scaler = torch.cuda.amp.GradScaler(enabled=amp_enabled)
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:11:epoch=001 loss=1.044174 val_dice=0.220347 val_iou=0.123815 val_pr_auc=0.148267 minutes=0.32
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:12:epoch=002 loss=0.861660 val_dice=0.330021 val_iou=0.197620 val_pr_auc=0.352460 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:13:epoch=003 loss=0.738569 val_dice=0.395203 val_iou=0.246264 val_pr_auc=0.445970 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:14:epoch=004 loss=0.669487 val_dice=0.445811 val_iou=0.286844 val_pr_auc=0.506100 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:15:epoch=005 loss=0.623482 val_dice=0.465448 val_iou=0.303312 val_pr_auc=0.544250 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:16:epoch=006 loss=0.581583 val_dice=0.524423 val_iou=0.355402 val_pr_auc=0.591176 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:17:epoch=007 loss=0.542672 val_dice=0.502238 val_iou=0.335326 val_pr_auc=0.626267 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:18:epoch=008 loss=0.501275 val_dice=0.549318 val_iou=0.378662 val_pr_auc=0.664116 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:19:epoch=009 loss=0.463011 val_dice=0.595464 val_iou=0.423958 val_pr_auc=0.699814 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:20:epoch=010 loss=0.438031 val_dice=0.629139 val_iou=0.458937 val_pr_auc=0.719178 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:21:epoch=011 loss=0.414671 val_dice=0.645080 val_iou=0.476102 val_pr_auc=0.733999 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:22:epoch=012 loss=0.398844 val_dice=0.607199 val_iou=0.435955 val_pr_auc=0.718977 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:23:epoch=013 loss=0.377859 val_dice=0.631336 val_iou=0.461280 val_pr_auc=0.757730 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:24:epoch=014 loss=0.364058 val_dice=0.675847 val_iou=0.510400 val_pr_auc=0.768168 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:25:epoch=015 loss=0.352412 val_dice=0.654198 val_iou=0.486103 val_pr_auc=0.759199 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:26:epoch=016 loss=0.342353 val_dice=0.688899 val_iou=0.525436 val_pr_auc=0.774911 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:27:epoch=017 loss=0.335509 val_dice=0.678364 val_iou=0.513276 val_pr_auc=0.782113 minutes=0.32
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:28:epoch=018 loss=0.322418 val_dice=0.682413 val_iou=0.517926 val_pr_auc=0.791560 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:29:epoch=019 loss=0.317725 val_dice=0.684473 val_iou=0.520303 val_pr_auc=0.783781 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:30:epoch=020 loss=0.312603 val_dice=0.699316 val_iou=0.537653 val_pr_auc=0.800032 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:31:epoch=021 loss=0.304364 val_dice=0.666135 val_iou=0.499402 val_pr_auc=0.798243 minutes=0.31
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:2:parameters=45001057 epochs=100 train_patches=64 val_patches=32
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:3:epoch=1/100 train_patch=16/64 loss=0.50337
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:4:epoch=1/100 train_patch=32/64 loss=0.48165
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:5:epoch=1/100 train_patch=48/64 loss=0.39263
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:6:epoch=1/100 train_patch=64/64 loss=0.51061
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:7:EPOCH 001 train_loss=0.465645 val_loss=0.485600 val_dice=0.000000 val_precision=0.000000 val_recall=0.000000 best=0.000000 elapsed_min=8.5
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:8:epoch=2/100 train_patch=16/64 loss=0.50700
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:9:epoch=2/100 train_patch=32/64 loss=0.50687
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:10:epoch=2/100 train_patch=48/64 loss=0.51004
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:11:epoch=2/100 train_patch=64/64 loss=0.50326
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:12:EPOCH 002 train_loss=0.467679 val_loss=0.482254 val_dice=0.000000 val_precision=0.000000 val_recall=0.000000 best=0.000000 elapsed_min=17.0
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:13:epoch=3/100 train_patch=16/64 loss=0.50515
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:14:epoch=3/100 train_patch=32/64 loss=0.51582
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:15:epoch=3/100 train_patch=48/64 loss=0.38142
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:16:epoch=3/100 train_patch=64/64 loss=0.51498
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:17:EPOCH 003 train_loss=0.454671 val_loss=0.483168 val_dice=0.000000 val_precision=0.000000 val_recall=0.000000 best=0.000000 elapsed_min=25.5
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:18:epoch=4/100 train_patch=16/64 loss=0.35696
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:19:epoch=4/100 train_patch=32/64 loss=0.51711
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:20:epoch=4/100 train_patch=48/64 loss=0.51147
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:21:epoch=4/100 train_patch=64/64 loss=0.50276
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:22:EPOCH 004 train_loss=0.460464 val_loss=0.481467 val_dice=0.000000 val_precision=0.000000 val_recall=0.000000 best=0.000000 elapsed_min=34.0
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:23:epoch=5/100 train_patch=16/64 loss=0.50632
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:24:epoch=5/100 train_patch=32/64 loss=0.51415
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:25:epoch=5/100 train_patch=48/64 loss=0.50639
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:2:RESUME epoch=50 best_val_dice=0.367370
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:4:parameters=45001057 epochs=100 train_patches=64 val_patches=32
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:5:epoch=50/100 train_patch=16/64 loss=0.50684
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:6:epoch=50/100 train_patch=32/64 loss=0.51190
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:7:epoch=50/100 train_patch=48/64 loss=0.52828
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:8:epoch=50/100 train_patch=64/64 loss=0.25706
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:9:EPOCH 050 train_loss=0.416314 val_loss=0.453715 val_dice=0.286637 val_precision=0.180658 val_recall=0.693418 best=0.367370 elapsed_min=8.3
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:10:epoch=51/100 train_patch=16/64 loss=0.52553
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:11:epoch=51/100 train_patch=32/64 loss=0.50325
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:12:epoch=51/100 train_patch=48/64 loss=0.50754
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:13:epoch=51/100 train_patch=64/64 loss=0.50115
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:14:EPOCH 051 train_loss=0.453673 val_loss=0.453172 val_dice=0.262730 val_precision=0.211600 val_recall=0.346444 best=0.367370 elapsed_min=16.5
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:15:epoch=52/100 train_patch=16/64 loss=0.33214
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:16:epoch=52/100 train_patch=32/64 loss=0.50397
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:17:epoch=52/100 train_patch=48/64 loss=0.50738
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:18:epoch=52/100 train_patch=64/64 loss=0.50343
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:19:EPOCH 052 train_loss=0.409309 val_loss=0.442612 val_dice=0.376027 val_precision=0.282215 val_recall=0.563264 best=0.376027 elapsed_min=24.7
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:20:epoch=53/100 train_patch=16/64 loss=0.51703
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:21:epoch=53/100 train_patch=32/64 loss=0.52752
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:22:epoch=53/100 train_patch=48/64 loss=0.50514
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:23:epoch=53/100 train_patch=64/64 loss=0.32922
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:24:EPOCH 053 train_loss=0.439335 val_loss=0.443985 val_dice=0.380571 val_precision=0.424110 val_recall=0.345139 best=0.380571 elapsed_min=32.9
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:25:epoch=54/100 train_patch=16/64 loss=0.51174
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:26:epoch=54/100 train_patch=32/64 loss=0.50349
reports/training/r100_fp16_3seed_queue_20261014_145225.log:2:START seed=42 smoke=True pid=1899203 log=runs/R100_fp16_clean_3seeds_20261014_145225/smoke.log
reports/training/r100_fp16_3seed_queue_20261014_145510.log:1:START seed=42 smoke=True pid=1909458 log=runs/R100_fp16_clean_3seeds_20261014_145510/smoke.log
reports/training/r100_fp16_3seed_queue_20261014_145510.log:2:START seed=42 smoke=False pid=1911189 log=runs/R100_fp16_clean_3seeds_20261014_145510/seed42.log
reports/training/r100_fp16_3seed_queue_20261014_145510.log:8:    execute(run_dir, seed, expected_protocol=expected_protocol)
reports/training/r100_fp16_3seed_queue_20261014_150435.log:2:START seed=42 smoke=True pid=1945423 log=runs/R100_fp16_clean_3seeds_20261014_150435/smoke.log
reports/training/r100_fp16_3seed_queue_20261014_150435.log:3:START seed=42 smoke=False pid=1946437 log=runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log
reports/training/r100_fp16_3seed_queue_20261014_150435.log:4:PASS seed=42 validation_dice=0.544072
reports/training/r100_fp16_3seed_queue_20261014_150435.log:5:START seed=43 smoke=False pid=3264730 log=runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log
reports/training/r100_fp16_3seed_queue_20261014_150435.log:6:PASS seed=43 validation_dice=0.569856
reports/training/r100_fp16_3seed_queue_20261014_150435.log:7:START seed=44 smoke=False pid=379744 log=runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log
reports/training/r100_fp16_3seed_queue_20261014_150435.log:8:PASS seed=44 validation_dice=0.572980
reports/training/R100_thebe_seed42_20261005_102737.log:1:/shared/home/khavarj/projects/fault_detection/scripts/r100_full_run.py:237: FutureWarning: `torch.cuda.amp.GradScaler(args...)` is deprecated. Please use `torch.amp.GradScaler('cuda', args...)` instead.
reports/training/R100_thebe_seed42_20261005_102737.log:2:  scaler = torch.cuda.amp.GradScaler(enabled=True)
reports/training/R100_thebe_seed42_20261005_102737.log:12:epoch=001/100 loss=0.211608 val_dice=0.000006 val_pr_auc=0.034823 minutes=3.26
reports/training/R100_thebe_seed42_20261005_102737.log:14:epoch=002/100 loss=0.131591 val_dice=0.000001 val_pr_auc=0.039528 minutes=3.33
reports/training/R100_thebe_seed42_20261005_102737.log:16:epoch=003/100 loss=0.105220 val_dice=0.000001 val_pr_auc=0.043710 minutes=3.23
reports/training/R100_thebe_seed42_20261005_102737.log:18:epoch=004/100 loss=0.101674 val_dice=0.000000 val_pr_auc=0.043505 minutes=3.32
reports/training/R100_thebe_seed42_20261005_102737.log:20:epoch=005/100 loss=0.113378 val_dice=0.000000 val_pr_auc=0.038386 minutes=3.04
reports/training/R100_thebe_seed42_20261005_102737.log:22:epoch=006/100 loss=0.102869 val_dice=0.000000 val_pr_auc=0.047210 minutes=3.22
reports/training/R100_thebe_seed42_20261005_102737.log:24:epoch=007/100 loss=0.106725 val_dice=0.000000 val_pr_auc=0.049760 minutes=3.20
reports/training/R100_thebe_seed42_20261005_102737.log:26:epoch=008/100 loss=0.096674 val_dice=0.000000 val_pr_auc=0.048672 minutes=3.13
reports/training/R100_thebe_seed42_20261005_102737.log:28:epoch=009/100 loss=0.099541 val_dice=0.000000 val_pr_auc=0.043619 minutes=3.24
reports/training/R100_thebe_seed42_20261005_102737.log:30:epoch=010/100 loss=0.107934 val_dice=0.000000 val_pr_auc=0.055916 minutes=3.05
reports/training/R100_thebe_seed42_20261005_102737.log:32:epoch=011/100 loss=0.099936 val_dice=0.000000 val_pr_auc=0.061880 minutes=3.10
reports/training/R100_thebe_seed42_20261005_102737.log:34:epoch=012/100 loss=0.102164 val_dice=0.000000 val_pr_auc=0.049965 minutes=3.15
reports/training/R100_thebe_seed42_20261005_102737.log:36:epoch=013/100 loss=0.109964 val_dice=0.000000 val_pr_auc=0.061470 minutes=3.00
reports/training/R100_thebe_seed42_20261005_102737.log:38:epoch=014/100 loss=0.096900 val_dice=0.000000 val_pr_auc=0.089677 minutes=3.07
reports/training/R100_thebe_seed42_20261005_102737.log:40:epoch=015/100 loss=0.089464 val_dice=0.000000 val_pr_auc=0.117684 minutes=3.21
reports/training/R100_thebe_seed42_20261005_102737.log:42:epoch=016/100 loss=0.088687 val_dice=0.000000 val_pr_auc=0.107323 minutes=3.15
reports/training/R100_thebe_seed42_20261005_102737.log:44:epoch=017/100 loss=0.083734 val_dice=0.000000 val_pr_auc=0.135083 minutes=3.13
reports/training/R100_thebe_seed42_20261005_102737.log:46:epoch=018/100 loss=0.087998 val_dice=0.000000 val_pr_auc=0.171241 minutes=3.32
reports/training/R100_thebe_seed42_20261005_102737.log:48:epoch=019/100 loss=0.090926 val_dice=0.000000 val_pr_auc=0.184733 minutes=3.11
reports/training/R100_thebe_seed42_20261005_102737.log:50:epoch=020/100 loss=0.077623 val_dice=0.000000 val_pr_auc=0.207758 minutes=3.15
reports/training/R100_thebe_seed42_20261005_102737.log:52:epoch=021/100 loss=0.073180 val_dice=0.000013 val_pr_auc=0.213077 minutes=3.13
reports/training/R100_thebe_seed42_20261005_102737.log:54:epoch=022/100 loss=0.077549 val_dice=0.000690 val_pr_auc=0.212709 minutes=3.08
reports/training/R100_thebe_seed42_resume_20261005_131346.log:1:/shared/home/khavarj/projects/fault_detection/scripts/r100_full_run.py:250: FutureWarning: `torch.cuda.amp.GradScaler(args...)` is deprecated. Please use `torch.amp.GradScaler('cuda', args...)` instead.
reports/training/R100_thebe_seed42_resume_20261005_131346.log:2:  scaler = torch.cuda.amp.GradScaler(enabled=True)
reports/training/R100_thebe_seed42_resume_20261005_131346.log:4:RESUME PASS: completed epoch 23; continuing from epoch 24
reports/training/R100_thebe_seed42_resume_20261005_131346.log:13:epoch=024/100 loss=0.078920 val_dice=0.001420 val_pr_auc=0.236420 minutes=3.32
reports/training/R100_thebe_seed42_resume_20261005_131346.log:15:epoch=025/100 loss=0.065565 val_dice=0.002473 val_pr_auc=0.260316 minutes=3.20
reports/training/R100_thebe_seed42_resume_20261005_131346.log:17:epoch=026/100 loss=0.068080 val_dice=0.003456 val_pr_auc=0.263557 minutes=3.25
reports/training/R100_thebe_seed42_resume_20261005_131346.log:19:epoch=027/100 loss=0.080750 val_dice=0.011536 val_pr_auc=0.259436 minutes=3.12
reports/training/R100_thebe_seed42_resume_20261005_131346.log:21:epoch=028/100 loss=0.075161 val_dice=0.018024 val_pr_auc=0.297481 minutes=3.05
reports/training/R100_thebe_seed42_resume_20261005_131346.log:23:epoch=029/100 loss=0.084217 val_dice=0.048370 val_pr_auc=0.295427 minutes=3.27
reports/training/R100_thebe_seed42_resume_20261005_131346.log:25:epoch=030/100 loss=0.069108 val_dice=0.027934 val_pr_auc=0.322924 minutes=3.16
reports/training/R100_thebe_seed42_resume_20261005_131346.log:27:epoch=031/100 loss=0.078519 val_dice=0.077669 val_pr_auc=0.336544 minutes=3.02
reports/training/R100_thebe_seed42_resume_20261005_131346.log:29:epoch=032/100 loss=0.062892 val_dice=0.304055 val_pr_auc=0.336719 minutes=3.36
reports/training/R100_thebe_seed42_resume_20261005_131346.log:31:epoch=033/100 loss=0.072173 val_dice=0.149602 val_pr_auc=0.348334 minutes=3.39
reports/training/R100_thebe_seed42_resume_20261005_131346.log:33:epoch=034/100 loss=0.070201 val_dice=0.174907 val_pr_auc=0.342185 minutes=3.24
reports/training/R100_thebe_seed42_resume_20261005_131346.log:35:epoch=035/100 loss=0.073527 val_dice=0.148241 val_pr_auc=0.369592 minutes=3.27
reports/training/R100_thebe_seed42_resume_20261005_131346.log:37:epoch=036/100 loss=0.069229 val_dice=0.193048 val_pr_auc=0.379670 minutes=3.25
reports/training/R100_thebe_seed42_resume_20261005_131346.log:39:epoch=037/100 loss=0.063905 val_dice=0.006665 val_pr_auc=0.330679 minutes=3.15
reports/training/R100_thebe_seed42_resume_20261005_131346.log:41:epoch=038/100 loss=0.080337 val_dice=0.244056 val_pr_auc=0.374059 minutes=3.23
reports/training/R100_thebe_seed42_resume_20261005_131346.log:43:epoch=039/100 loss=0.066486 val_dice=0.255052 val_pr_auc=0.404267 minutes=3.12
reports/training/R100_thebe_seed42_resume_20261005_131346.log:45:epoch=040/100 loss=0.065938 val_dice=0.210433 val_pr_auc=0.382206 minutes=3.17
reports/training/R100_thebe_seed42_resume_20261005_131346.log:47:epoch=041/100 loss=0.062026 val_dice=0.407483 val_pr_auc=0.373383 minutes=3.09
reports/training/R100_thebe_seed42_resume_20261005_131346.log:49:epoch=042/100 loss=0.075279 val_dice=0.123915 val_pr_auc=0.388560 minutes=3.06
reports/training/R100_thebe_seed42_resume_20261005_131346.log:51:epoch=043/100 loss=0.065071 val_dice=0.270480 val_pr_auc=0.393687 minutes=3.09
reports/training/R100_thebe_seed42_resume_20261005_131346.log:53:epoch=044/100 loss=0.064441 val_dice=0.172999 val_pr_auc=0.384315 minutes=3.11
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:16:      "seed": 42,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:19:      "threshold": 0.31640625,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:21:        "threshold": 0.31640625,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:24:        "precision": 0.5267658204531103,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:41:      "seed": 43,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:44:      "threshold": 0.279296875,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:46:        "threshold": 0.279296875,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:49:        "precision": 0.5643889729910121,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:66:      "seed": 44,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:69:      "threshold": 0.244140625,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:71:        "threshold": 0.244140625,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:74:        "precision": 0.5655692044103381,
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/best.pt: binary file matches (found "\0" byte around offset 4)
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/history.csv:1:epoch,train_loss,train_patches,resampled_no_data_candidates,excluded_training_positive_labels,seconds,val_threshold,val_dice,val_iou,val_precision,val_recall,val_specificity,val_balanced_accuracy,val_accuracy,val_mcc,val_pr_auc_approx,val_roc_auc_approx,val_tp,val_fp,val_fn,val_tn
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/last.pt: binary file matches (found "\0" byte around offset 4)
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:2:QUEUE LAUNCH 2026-10-14T11:04:49.680315+00:00 ["/shared/home/khavarj/projects/fault_detection/.venv_train/bin/python", "-u", "/shared/home/khavarj/projects/fault_detection/scripts/train_r100_fp16_clean.py", "--seed", "42", "--validation-seed", "1042", "--thebe-root", "data/processed/thebe_h5", "--run-dir", "runs/R100_fp16_clean_3seeds_20261014_150435/seed42"]
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:7:epoch=1/100 train_patch=60/360 loss=0.269200
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:8:epoch=1/100 train_patch=120/360 loss=0.096066
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:9:epoch=1/100 train_patch=180/360 loss=0.145327
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:10:epoch=1/100 train_patch=240/360 loss=0.151376
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:11:epoch=1/100 train_patch=300/360 loss=0.019122
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:12:epoch=1/100 train_patch=360/360 loss=0.668354
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:18:epoch=001/100 loss=0.211608 val_dice=0.000006 val_pr_auc=0.034823 minutes=3.12
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:19:epoch=2/100 train_patch=60/360 loss=0.223522
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:20:epoch=2/100 train_patch=120/360 loss=0.020627
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:21:epoch=2/100 train_patch=180/360 loss=0.265117
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:22:epoch=2/100 train_patch=240/360 loss=0.046374
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:23:epoch=2/100 train_patch=300/360 loss=0.051667
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:24:epoch=2/100 train_patch=360/360 loss=0.037058
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:26:epoch=002/100 loss=0.131591 val_dice=0.000001 val_pr_auc=0.039528 minutes=3.08
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:27:epoch=3/100 train_patch=60/360 loss=0.030490
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:28:epoch=3/100 train_patch=120/360 loss=0.011700
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:29:epoch=3/100 train_patch=180/360 loss=0.011385
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:30:epoch=3/100 train_patch=240/360 loss=0.005840
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:31:epoch=3/100 train_patch=300/360 loss=0.293844
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:32:epoch=3/100 train_patch=360/360 loss=0.045493
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:34:epoch=003/100 loss=0.105220 val_dice=0.000001 val_pr_auc=0.043710 minutes=3.09
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:35:epoch=4/100 train_patch=60/360 loss=0.025259
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:36:epoch=4/100 train_patch=120/360 loss=0.279557
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/run_config.json:3:  "seed": 42,
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/run_config.json:5:  "precision": "float16_autocast",
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/run_config.json:732:  "epochs": 100,
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/run_config.json:734:  "patch_size": 128,
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/run_config.json:737:  "train_sampling": "40 observed random patches per train file each epoch; random axis-0 flip",
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/run_config.json:739:  "normalization": "per-patch z-score over observed voxels; axis reversal",
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/run_config.json:741:  "optimizer": "Adam",
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/run_config.json:742:  "learning_rate": 0.0001,
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/run_config.json:743:  "loss": "ordinary BCE averaged over observed voxels",
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/status.json:3:  "seed": 42,
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/status.json:7:  "precision": "float16_autocast",
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/status.json:11:  "threshold": 0.31640625,
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/validation_selection.json:3:  "threshold": 0.31640625,
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/validation_selection.json:6:    "threshold": 0.31640625,
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/validation_selection.json:9:    "precision": 0.5267658204531103,
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/best.pt: binary file matches (found "\0" byte around offset 4)
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/history.csv:1:epoch,train_loss,train_patches,resampled_no_data_candidates,excluded_training_positive_labels,seconds,val_threshold,val_dice,val_iou,val_precision,val_recall,val_specificity,val_balanced_accuracy,val_accuracy,val_mcc,val_pr_auc_approx,val_roc_auc_approx,val_tp,val_fp,val_fn,val_tn
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/last.pt: binary file matches (found "\0" byte around offset 4)
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:2:QUEUE LAUNCH 2026-10-14T16:13:56.661530+00:00 ["/shared/home/khavarj/projects/fault_detection/.venv_train/bin/python", "-u", "/shared/home/khavarj/projects/fault_detection/scripts/train_r100_fp16_clean.py", "--seed", "43", "--validation-seed", "1042", "--thebe-root", "data/processed/thebe_h5", "--run-dir", "runs/R100_fp16_clean_3seeds_20261014_150435/seed43", "--expected-protocol", "1febc1e47ba203ff08db82816ceadf616a5e7db345054cfbe45274b84c5f5437"]
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:7:epoch=1/100 train_patch=60/360 loss=0.025100
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:8:epoch=1/100 train_patch=120/360 loss=0.089748
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:9:epoch=1/100 train_patch=180/360 loss=0.030659
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:10:epoch=1/100 train_patch=240/360 loss=0.035034
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:11:epoch=1/100 train_patch=300/360 loss=0.176485
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:12:epoch=1/100 train_patch=360/360 loss=0.013613
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:18:epoch=001/100 loss=0.207313 val_dice=0.000010 val_pr_auc=0.032889 minutes=3.25
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:19:epoch=2/100 train_patch=60/360 loss=0.143345
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:20:epoch=2/100 train_patch=120/360 loss=0.170271
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:21:epoch=2/100 train_patch=180/360 loss=0.178730
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:22:epoch=2/100 train_patch=240/360 loss=0.423158
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:23:epoch=2/100 train_patch=300/360 loss=0.202504
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:24:epoch=2/100 train_patch=360/360 loss=0.010068
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:26:epoch=002/100 loss=0.134325 val_dice=0.000000 val_pr_auc=0.037506 minutes=3.40
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:27:epoch=3/100 train_patch=60/360 loss=0.073450
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:28:epoch=3/100 train_patch=120/360 loss=0.002192
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:29:epoch=3/100 train_patch=180/360 loss=0.011881
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:30:epoch=3/100 train_patch=240/360 loss=0.008659
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:31:epoch=3/100 train_patch=300/360 loss=0.012940
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:32:epoch=3/100 train_patch=360/360 loss=0.163898
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:34:epoch=003/100 loss=0.113158 val_dice=0.000000 val_pr_auc=0.044267 minutes=3.32
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:35:epoch=4/100 train_patch=60/360 loss=0.117194
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:36:epoch=4/100 train_patch=120/360 loss=0.025358
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/run_config.json:3:  "seed": 43,
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/run_config.json:5:  "precision": "float16_autocast",
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/run_config.json:732:  "epochs": 100,
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/run_config.json:734:  "patch_size": 128,
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/run_config.json:737:  "train_sampling": "40 observed random patches per train file each epoch; random axis-0 flip",
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/run_config.json:739:  "normalization": "per-patch z-score over observed voxels; axis reversal",
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/run_config.json:741:  "optimizer": "Adam",
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/run_config.json:742:  "learning_rate": 0.0001,
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/run_config.json:743:  "loss": "ordinary BCE averaged over observed voxels",
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/status.json:3:  "seed": 43,
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/status.json:7:  "precision": "float16_autocast",
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/status.json:11:  "threshold": 0.279296875,
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/validation_selection.json:3:  "threshold": 0.279296875,
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/validation_selection.json:6:    "threshold": 0.279296875,
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/validation_selection.json:9:    "precision": 0.5643889729910121,
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/best.pt: binary file matches (found "\0" byte around offset 4)
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/history.csv:1:epoch,train_loss,train_patches,resampled_no_data_candidates,excluded_training_positive_labels,seconds,val_threshold,val_dice,val_iou,val_precision,val_recall,val_specificity,val_balanced_accuracy,val_accuracy,val_mcc,val_pr_auc_approx,val_roc_auc_approx,val_tp,val_fp,val_fn,val_tn
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/last.pt: binary file matches (found "\0" byte around offset 4)
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:2:QUEUE LAUNCH 2026-10-14T21:26:57.138315+00:00 ["/shared/home/khavarj/projects/fault_detection/.venv_train/bin/python", "-u", "/shared/home/khavarj/projects/fault_detection/scripts/train_r100_fp16_clean.py", "--seed", "44", "--validation-seed", "1042", "--thebe-root", "data/processed/thebe_h5", "--run-dir", "runs/R100_fp16_clean_3seeds_20261014_150435/seed44", "--expected-protocol", "1febc1e47ba203ff08db82816ceadf616a5e7db345054cfbe45274b84c5f5437"]
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:7:epoch=1/100 train_patch=60/360 loss=0.128812
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:8:epoch=1/100 train_patch=120/360 loss=0.049892
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:9:epoch=1/100 train_patch=180/360 loss=0.137484
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:10:epoch=1/100 train_patch=240/360 loss=0.094210
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:11:epoch=1/100 train_patch=300/360 loss=0.037499
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:12:epoch=1/100 train_patch=360/360 loss=1.847119
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:18:epoch=001/100 loss=0.214208 val_dice=0.000002 val_pr_auc=0.032531 minutes=2.98
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:19:epoch=2/100 train_patch=60/360 loss=0.102701
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:20:epoch=2/100 train_patch=120/360 loss=0.057482
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:21:epoch=2/100 train_patch=180/360 loss=0.037050
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:22:epoch=2/100 train_patch=240/360 loss=0.015849
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:23:epoch=2/100 train_patch=300/360 loss=0.191525
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:24:epoch=2/100 train_patch=360/360 loss=0.040938
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:26:epoch=002/100 loss=0.131131 val_dice=0.000002 val_pr_auc=0.041499 minutes=2.94
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:27:epoch=3/100 train_patch=60/360 loss=0.005686
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:28:epoch=3/100 train_patch=120/360 loss=0.168815
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:29:epoch=3/100 train_patch=180/360 loss=0.034031
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:30:epoch=3/100 train_patch=240/360 loss=0.198657
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:31:epoch=3/100 train_patch=300/360 loss=0.007568
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:32:epoch=3/100 train_patch=360/360 loss=0.196844
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:34:epoch=003/100 loss=0.093528 val_dice=0.000000 val_pr_auc=0.046544 minutes=3.03
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:35:epoch=4/100 train_patch=60/360 loss=0.133939
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:36:epoch=4/100 train_patch=120/360 loss=0.009925
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/run_config.json:3:  "seed": 44,
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/run_config.json:5:  "precision": "float16_autocast",
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/run_config.json:732:  "epochs": 100,
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/run_config.json:734:  "patch_size": 128,
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/run_config.json:737:  "train_sampling": "40 observed random patches per train file each epoch; random axis-0 flip",
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/run_config.json:739:  "normalization": "per-patch z-score over observed voxels; axis reversal",
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/run_config.json:741:  "optimizer": "Adam",
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/run_config.json:742:  "learning_rate": 0.0001,
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/run_config.json:743:  "loss": "ordinary BCE averaged over observed voxels",
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/status.json:3:  "seed": 44,
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/status.json:7:  "precision": "float16_autocast",
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/status.json:11:  "threshold": 0.244140625,
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/validation_selection.json:3:  "threshold": 0.244140625,
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/validation_selection.json:6:    "threshold": 0.244140625,
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/validation_selection.json:9:    "precision": 0.5655692044103381,
runs/R100_fp16_clean_3seeds_20261014_150435/smoke.log:2:QUEUE LAUNCH 2026-10-14T11:04:35.537330+00:00 ["/shared/home/khavarj/projects/fault_detection/.venv_train/bin/python", "-u", "/shared/home/khavarj/projects/fault_detection/scripts/train_r100_fp16_clean.py", "--seed", "42", "--validation-seed", "1042", "--thebe-root", "data/processed/thebe_h5", "--run-dir", "runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42", "--smoke"]
runs/R100_fp16_clean_3seeds_20261014_150435/smoke.log:7:epoch=1/1 train_patch=18/18 loss=0.759043
runs/R100_fp16_clean_3seeds_20261014_150435/smoke.log:12:epoch=001/1 loss=0.779829 val_dice=0.068725 val_pr_auc=0.033207 minutes=0.17
runs/R100_fp16_clean_3seeds_20261014_150435/smoke.log:13:BEST EPOCH: 1; full validation begins
runs/R100_fp16_clean_3seeds_20261014_150435/smoke.log:14:VALIDATION THRESHOLD: 0.427246; test evaluation disabled
runs/R100_fp16_clean_3seeds_20261014_150435/smoke.log:15:R100 VALIDATION-ONLY COMPLETE seed=42 epochs=1 best_epoch=1
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/best.pt: binary file matches (found "\0" byte around offset 4)
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/history.csv:1:epoch,train_loss,train_patches,resampled_no_data_candidates,excluded_training_positive_labels,seconds,val_threshold,val_dice,val_iou,val_precision,val_recall,val_specificity,val_balanced_accuracy,val_accuracy,val_mcc,val_pr_auc_approx,val_roc_auc_approx,val_tp,val_fp,val_fn,val_tn
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/last.pt: binary file matches (found "\0" byte around offset 4)
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/run_config.json:3:  "seed": 42,
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/run_config.json:5:  "precision": "float16_autocast",
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/run_config.json:102:  "epochs": 1,
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/run_config.json:104:  "patch_size": 128,
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/run_config.json:107:  "train_sampling": "2 observed random patches per train file each epoch; random axis-0 flip",
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/run_config.json:109:  "normalization": "per-patch z-score over observed voxels; axis reversal",
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/run_config.json:111:  "optimizer": "Adam",
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/run_config.json:112:  "learning_rate": 0.0001,
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/run_config.json:113:  "loss": "ordinary BCE averaged over observed voxels",
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/status.json:3:  "seed": 42,
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/status.json:7:  "precision": "float16_autocast",
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/status.json:11:  "threshold": 0.42724609375,
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/validation_selection.json:3:  "threshold": 0.42724609375,
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/validation_selection.json:6:    "threshold": 0.42724609375,
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/validation_selection.json:9:    "precision": 0.035650329241587765,
```

### Results and completion

```text
reports/training/baseline_A_smoke.log:4:/shared/home/khavarj/projects/fault_detection/.venv_train/lib/python3.13/site-packages/torch/autograd/graph.py:824: UserWarning: max_pool3d_with_indices_backward_cuda does not have a deterministic implementation, but you set 'torch.use_deterministic_algorithms(True, warn_only=True)'. You can file an issue at https://github.com/pytorch/pytorch/issues to help us prioritize adding deterministic support for this operation. (Triggered internally at /pytorch/aten/src/ATen/Context.cpp:93.)
reports/training/baseline_A_synthetic_bce_seed42.log:5:/shared/home/khavarj/projects/fault_detection/.venv_train/lib/python3.13/site-packages/torch/autograd/graph.py:824: UserWarning: max_pool3d_with_indices_backward_cuda does not have a deterministic implementation, but you set 'torch.use_deterministic_algorithms(True, warn_only=True)'. You can file an issue at https://github.com/pytorch/pytorch/issues to help us prioritize adding deterministic support for this operation. (Triggered internally at /pytorch/aten/src/ATen/Context.cpp:93.)
reports/training/baseline_A_synthetic_bce_seed42.log:11:epoch=001 loss=0.314965 val_dice=0.000000 val_iou=0.000000 val_pr_auc=0.076771 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:12:epoch=002 loss=0.254361 val_dice=0.000000 val_iou=0.000000 val_pr_auc=0.096252 minutes=0.30
reports/training/baseline_A_synthetic_bce_seed42.log:13:epoch=003 loss=0.238950 val_dice=0.000000 val_iou=0.000000 val_pr_auc=0.182016 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:14:epoch=004 loss=0.200252 val_dice=0.118262 val_iou=0.062847 val_pr_auc=0.390901 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:15:epoch=005 loss=0.168745 val_dice=0.398029 val_iou=0.248462 val_pr_auc=0.481942 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:16:epoch=006 loss=0.153221 val_dice=0.465434 val_iou=0.303300 val_pr_auc=0.539682 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:17:epoch=007 loss=0.141764 val_dice=0.497805 val_iou=0.331385 val_pr_auc=0.586533 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:18:epoch=008 loss=0.135450 val_dice=0.534810 val_iou=0.365011 val_pr_auc=0.613936 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:19:epoch=009 loss=0.128391 val_dice=0.600041 val_iou=0.428614 val_pr_auc=0.641996 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:20:epoch=010 loss=0.122253 val_dice=0.583450 val_iou=0.411881 val_pr_auc=0.643059 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:21:epoch=011 loss=0.118308 val_dice=0.619101 val_iou=0.448332 val_pr_auc=0.686354 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:22:epoch=012 loss=0.112667 val_dice=0.641208 val_iou=0.471895 val_pr_auc=0.700150 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:23:epoch=013 loss=0.109114 val_dice=0.633384 val_iou=0.463469 val_pr_auc=0.715915 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:24:epoch=014 loss=0.106602 val_dice=0.650868 val_iou=0.482435 val_pr_auc=0.711744 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:25:epoch=015 loss=0.102564 val_dice=0.666159 val_iou=0.499429 val_pr_auc=0.731226 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:26:epoch=016 loss=0.099363 val_dice=0.685561 val_iou=0.521562 val_pr_auc=0.750862 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:27:epoch=017 loss=0.097281 val_dice=0.687228 val_iou=0.523494 val_pr_auc=0.757492 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:28:epoch=018 loss=0.093142 val_dice=0.689824 val_iou=0.526513 val_pr_auc=0.765094 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:29:epoch=019 loss=0.093322 val_dice=0.693366 val_iou=0.530651 val_pr_auc=0.769579 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:30:epoch=020 loss=0.089892 val_dice=0.718609 val_iou=0.560804 val_pr_auc=0.786135 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:31:epoch=021 loss=0.088231 val_dice=0.706142 val_iou=0.545765 val_pr_auc=0.776918 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:32:epoch=022 loss=0.084756 val_dice=0.726282 val_iou=0.570206 val_pr_auc=0.795567 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:33:epoch=023 loss=0.083188 val_dice=0.718521 val_iou=0.560696 val_pr_auc=0.792467 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:34:epoch=024 loss=0.082507 val_dice=0.715403 val_iou=0.556909 val_pr_auc=0.802811 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:35:epoch=025 loss=0.080076 val_dice=0.735477 val_iou=0.581624 val_pr_auc=0.807542 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:36:epoch=026 loss=0.080869 val_dice=0.732477 val_iou=0.577881 val_pr_auc=0.802525 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:37:epoch=027 loss=0.077535 val_dice=0.737478 val_iou=0.584131 val_pr_auc=0.808070 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:38:epoch=028 loss=0.076718 val_dice=0.748352 val_iou=0.597894 val_pr_auc=0.820242 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:39:epoch=029 loss=0.075930 val_dice=0.745820 val_iou=0.594668 val_pr_auc=0.816438 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:40:epoch=030 loss=0.073748 val_dice=0.747954 val_iou=0.597386 val_pr_auc=0.821692 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:41:epoch=031 loss=0.074170 val_dice=0.745570 val_iou=0.594349 val_pr_auc=0.824247 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:42:epoch=032 loss=0.072066 val_dice=0.754636 val_iou=0.605956 val_pr_auc=0.832046 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:43:epoch=033 loss=0.070841 val_dice=0.757549 val_iou=0.609721 val_pr_auc=0.832721 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:44:epoch=034 loss=0.069383 val_dice=0.758069 val_iou=0.610395 val_pr_auc=0.834272 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:45:epoch=035 loss=0.068534 val_dice=0.760320 val_iou=0.613319 val_pr_auc=0.839178 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:46:epoch=036 loss=0.068438 val_dice=0.762048 val_iou=0.615572 val_pr_auc=0.835858 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:47:epoch=037 loss=0.066611 val_dice=0.760876 val_iou=0.614044 val_pr_auc=0.835267 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:48:epoch=038 loss=0.065514 val_dice=0.767338 val_iou=0.622505 val_pr_auc=0.840293 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:49:epoch=039 loss=0.065180 val_dice=0.763551 val_iou=0.617536 val_pr_auc=0.838623 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:50:epoch=040 loss=0.064552 val_dice=0.771029 val_iou=0.627378 val_pr_auc=0.841061 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:51:epoch=041 loss=0.064264 val_dice=0.771959 val_iou=0.628610 val_pr_auc=0.843271 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:52:epoch=042 loss=0.063743 val_dice=0.767876 val_iou=0.623213 val_pr_auc=0.846059 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:53:epoch=043 loss=0.061794 val_dice=0.772249 val_iou=0.628995 val_pr_auc=0.848326 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:54:epoch=044 loss=0.060327 val_dice=0.779469 val_iou=0.638632 val_pr_auc=0.852134 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:55:epoch=045 loss=0.059616 val_dice=0.785259 val_iou=0.646442 val_pr_auc=0.855085 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:56:epoch=046 loss=0.060070 val_dice=0.749423 val_iou=0.599261 val_pr_auc=0.829438 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:57:epoch=047 loss=0.059813 val_dice=0.775634 val_iou=0.633499 val_pr_auc=0.849559 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:58:epoch=048 loss=0.058218 val_dice=0.787302 val_iou=0.649215 val_pr_auc=0.859910 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:59:epoch=049 loss=0.057960 val_dice=0.790558 val_iou=0.653656 val_pr_auc=0.861377 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:5:/shared/home/khavarj/projects/fault_detection/.venv_train/lib/python3.13/site-packages/torch/autograd/graph.py:824: UserWarning: max_pool3d_with_indices_backward_cuda does not have a deterministic implementation, but you set 'torch.use_deterministic_algorithms(True, warn_only=True)'. You can file an issue at https://github.com/pytorch/pytorch/issues to help us prioritize adding deterministic support for this operation. (Triggered internally at /pytorch/aten/src/ATen/Context.cpp:93.)
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:11:epoch=001 loss=1.044174 val_dice=0.220347 val_iou=0.123815 val_pr_auc=0.148267 minutes=0.32
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:12:epoch=002 loss=0.861660 val_dice=0.330021 val_iou=0.197620 val_pr_auc=0.352460 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:13:epoch=003 loss=0.738569 val_dice=0.395203 val_iou=0.246264 val_pr_auc=0.445970 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:14:epoch=004 loss=0.669487 val_dice=0.445811 val_iou=0.286844 val_pr_auc=0.506100 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:15:epoch=005 loss=0.623482 val_dice=0.465448 val_iou=0.303312 val_pr_auc=0.544250 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:16:epoch=006 loss=0.581583 val_dice=0.524423 val_iou=0.355402 val_pr_auc=0.591176 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:17:epoch=007 loss=0.542672 val_dice=0.502238 val_iou=0.335326 val_pr_auc=0.626267 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:18:epoch=008 loss=0.501275 val_dice=0.549318 val_iou=0.378662 val_pr_auc=0.664116 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:19:epoch=009 loss=0.463011 val_dice=0.595464 val_iou=0.423958 val_pr_auc=0.699814 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:20:epoch=010 loss=0.438031 val_dice=0.629139 val_iou=0.458937 val_pr_auc=0.719178 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:21:epoch=011 loss=0.414671 val_dice=0.645080 val_iou=0.476102 val_pr_auc=0.733999 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:22:epoch=012 loss=0.398844 val_dice=0.607199 val_iou=0.435955 val_pr_auc=0.718977 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:23:epoch=013 loss=0.377859 val_dice=0.631336 val_iou=0.461280 val_pr_auc=0.757730 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:24:epoch=014 loss=0.364058 val_dice=0.675847 val_iou=0.510400 val_pr_auc=0.768168 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:25:epoch=015 loss=0.352412 val_dice=0.654198 val_iou=0.486103 val_pr_auc=0.759199 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:26:epoch=016 loss=0.342353 val_dice=0.688899 val_iou=0.525436 val_pr_auc=0.774911 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:27:epoch=017 loss=0.335509 val_dice=0.678364 val_iou=0.513276 val_pr_auc=0.782113 minutes=0.32
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:28:epoch=018 loss=0.322418 val_dice=0.682413 val_iou=0.517926 val_pr_auc=0.791560 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:29:epoch=019 loss=0.317725 val_dice=0.684473 val_iou=0.520303 val_pr_auc=0.783781 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:30:epoch=020 loss=0.312603 val_dice=0.699316 val_iou=0.537653 val_pr_auc=0.800032 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:31:epoch=021 loss=0.304364 val_dice=0.666135 val_iou=0.499402 val_pr_auc=0.798243 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:32:epoch=022 loss=0.296087 val_dice=0.683697 val_iou=0.519407 val_pr_auc=0.792827 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:33:epoch=023 loss=0.289767 val_dice=0.680265 val_iou=0.515455 val_pr_auc=0.790324 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:34:epoch=024 loss=0.283622 val_dice=0.724217 val_iou=0.567665 val_pr_auc=0.819983 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:35:epoch=025 loss=0.276947 val_dice=0.714994 val_iou=0.556413 val_pr_auc=0.817862 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:36:epoch=026 loss=0.276903 val_dice=0.717139 val_iou=0.559015 val_pr_auc=0.820812 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:37:epoch=027 loss=0.265155 val_dice=0.725327 val_iou=0.569030 val_pr_auc=0.814139 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:38:epoch=028 loss=0.265455 val_dice=0.708698 val_iou=0.548824 val_pr_auc=0.816097 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:39:epoch=029 loss=0.260097 val_dice=0.722187 val_iou=0.565174 val_pr_auc=0.826339 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:40:epoch=030 loss=0.253136 val_dice=0.708558 val_iou=0.548656 val_pr_auc=0.821485 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:41:epoch=031 loss=0.246760 val_dice=0.742100 val_iou=0.589952 val_pr_auc=0.830931 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:42:epoch=032 loss=0.245331 val_dice=0.718020 val_iou=0.560087 val_pr_auc=0.831030 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:43:epoch=033 loss=0.239755 val_dice=0.715431 val_iou=0.556942 val_pr_auc=0.831187 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:44:epoch=034 loss=0.237105 val_dice=0.742207 val_iou=0.590087 val_pr_auc=0.832874 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:45:epoch=035 loss=0.235641 val_dice=0.717694 val_iou=0.559690 val_pr_auc=0.823459 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:46:epoch=036 loss=0.228823 val_dice=0.731766 val_iou=0.576995 val_pr_auc=0.839220 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:47:epoch=037 loss=0.227346 val_dice=0.743963 val_iou=0.592310 val_pr_auc=0.834489 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:48:epoch=038 loss=0.226099 val_dice=0.749641 val_iou=0.599541 val_pr_auc=0.836799 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:49:epoch=039 loss=0.221457 val_dice=0.743303 val_iou=0.591474 val_pr_auc=0.845124 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:50:epoch=040 loss=0.218223 val_dice=0.723296 val_iou=0.566534 val_pr_auc=0.840595 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:51:epoch=041 loss=0.219299 val_dice=0.749194 val_iou=0.598969 val_pr_auc=0.842864 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:52:epoch=042 loss=0.217124 val_dice=0.745649 val_iou=0.594450 val_pr_auc=0.841899 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:53:epoch=043 loss=0.211047 val_dice=0.738224 val_iou=0.585067 val_pr_auc=0.837245 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:54:epoch=044 loss=0.210547 val_dice=0.742338 val_iou=0.590252 val_pr_auc=0.845773 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:55:epoch=045 loss=0.205635 val_dice=0.736547 val_iou=0.582963 val_pr_auc=0.847457 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:56:epoch=046 loss=0.208107 val_dice=0.757053 val_iou=0.609079 val_pr_auc=0.851818 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:57:epoch=047 loss=0.204230 val_dice=0.767097 val_iou=0.622187 val_pr_auc=0.856076 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:58:epoch=048 loss=0.198154 val_dice=0.756199 val_iou=0.607974 val_pr_auc=0.851964 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:59:epoch=049 loss=0.203914 val_dice=0.752893 val_iou=0.603711 val_pr_auc=0.846729 minutes=0.31
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:7:EPOCH 001 train_loss=0.465645 val_loss=0.485600 val_dice=0.000000 val_precision=0.000000 val_recall=0.000000 best=0.000000 elapsed_min=8.5
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:12:EPOCH 002 train_loss=0.467679 val_loss=0.482254 val_dice=0.000000 val_precision=0.000000 val_recall=0.000000 best=0.000000 elapsed_min=17.0
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:17:EPOCH 003 train_loss=0.454671 val_loss=0.483168 val_dice=0.000000 val_precision=0.000000 val_recall=0.000000 best=0.000000 elapsed_min=25.5
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:22:EPOCH 004 train_loss=0.460464 val_loss=0.481467 val_dice=0.000000 val_precision=0.000000 val_recall=0.000000 best=0.000000 elapsed_min=34.0
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:27:EPOCH 005 train_loss=0.467914 val_loss=0.481631 val_dice=0.000000 val_precision=0.000000 val_recall=0.000000 best=0.000000 elapsed_min=42.5
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:32:EPOCH 006 train_loss=0.461141 val_loss=0.484556 val_dice=0.000000 val_precision=0.000000 val_recall=0.000000 best=0.000000 elapsed_min=51.0
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:37:EPOCH 007 train_loss=0.446475 val_loss=0.481680 val_dice=0.047903 val_precision=0.161964 val_recall=0.028108 best=0.047903 elapsed_min=59.5
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:42:EPOCH 008 train_loss=0.459167 val_loss=0.479956 val_dice=0.000000 val_precision=0.000000 val_recall=0.000000 best=0.047903 elapsed_min=67.9
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:47:EPOCH 009 train_loss=0.451511 val_loss=0.476000 val_dice=0.149590 val_precision=0.106510 val_recall=0.251190 best=0.149590 elapsed_min=76.4
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:52:EPOCH 010 train_loss=0.457132 val_loss=0.476811 val_dice=0.099883 val_precision=0.186243 val_recall=0.068240 best=0.149590 elapsed_min=84.9
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:57:EPOCH 011 train_loss=0.459216 val_loss=0.476008 val_dice=0.016839 val_precision=0.326531 val_recall=0.008643 best=0.149590 elapsed_min=93.4
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:62:EPOCH 012 train_loss=0.434350 val_loss=0.475353 val_dice=0.180964 val_precision=0.120576 val_recall=0.362529 best=0.180964 elapsed_min=101.9
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:67:EPOCH 013 train_loss=0.450595 val_loss=0.472315 val_dice=0.150950 val_precision=0.159644 val_recall=0.143153 best=0.180964 elapsed_min=110.4
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:72:EPOCH 014 train_loss=0.444658 val_loss=0.470842 val_dice=0.184008 val_precision=0.189435 val_recall=0.178884 best=0.184008 elapsed_min=118.9
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:77:EPOCH 015 train_loss=0.455812 val_loss=0.472264 val_dice=0.151737 val_precision=0.347372 val_recall=0.097069 best=0.184008 elapsed_min=127.4
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:82:EPOCH 016 train_loss=0.439112 val_loss=0.474909 val_dice=0.090741 val_precision=0.263758 val_recall=0.054796 best=0.184008 elapsed_min=135.9
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:87:EPOCH 017 train_loss=0.455355 val_loss=0.472741 val_dice=0.075697 val_precision=0.446105 val_recall=0.041357 best=0.184008 elapsed_min=144.4
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:92:EPOCH 018 train_loss=0.442842 val_loss=0.471527 val_dice=0.238118 val_precision=0.212533 val_recall=0.270706 best=0.238118 elapsed_min=152.9
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:97:EPOCH 019 train_loss=0.441880 val_loss=0.470957 val_dice=0.212381 val_precision=0.284035 val_recall=0.169596 best=0.238118 elapsed_min=161.3
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:102:EPOCH 020 train_loss=0.442190 val_loss=0.465484 val_dice=0.241313 val_precision=0.179586 val_recall=0.367695 best=0.241313 elapsed_min=169.8
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:107:EPOCH 021 train_loss=0.435344 val_loss=0.475311 val_dice=0.158431 val_precision=0.103035 val_recall=0.342663 best=0.241313 elapsed_min=178.3
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:112:EPOCH 022 train_loss=0.442537 val_loss=0.468002 val_dice=0.194564 val_precision=0.130548 val_recall=0.381770 best=0.241313 elapsed_min=186.8
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:117:EPOCH 023 train_loss=0.449759 val_loss=0.464639 val_dice=0.211203 val_precision=0.228455 val_recall=0.196374 best=0.241313 elapsed_min=195.3
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:122:EPOCH 024 train_loss=0.438226 val_loss=0.470474 val_dice=0.206551 val_precision=0.144007 val_recall=0.365130 best=0.241313 elapsed_min=203.7
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:127:EPOCH 025 train_loss=0.450425 val_loss=0.471324 val_dice=0.193218 val_precision=0.122883 val_recall=0.451846 best=0.241313 elapsed_min=212.2
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:132:EPOCH 026 train_loss=0.463187 val_loss=0.463039 val_dice=0.181876 val_precision=0.325241 val_recall=0.126233 best=0.241313 elapsed_min=220.7
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:137:EPOCH 027 train_loss=0.449494 val_loss=0.458801 val_dice=0.275165 val_precision=0.242287 val_recall=0.318366 best=0.275165 elapsed_min=229.2
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:142:EPOCH 028 train_loss=0.451639 val_loss=0.459566 val_dice=0.261107 val_precision=0.231727 val_recall=0.299020 best=0.275165 elapsed_min=237.7
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:147:EPOCH 029 train_loss=0.439577 val_loss=0.461916 val_dice=0.225784 val_precision=0.160429 val_recall=0.380989 best=0.275165 elapsed_min=246.1
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:152:EPOCH 030 train_loss=0.440820 val_loss=0.463329 val_dice=0.220092 val_precision=0.153135 val_recall=0.391092 best=0.275165 elapsed_min=254.6
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:157:EPOCH 031 train_loss=0.433343 val_loss=0.464132 val_dice=0.186347 val_precision=0.178289 val_recall=0.195169 best=0.275165 elapsed_min=263.1
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:162:EPOCH 032 train_loss=0.434500 val_loss=0.470934 val_dice=0.105899 val_precision=0.194278 val_recall=0.072787 best=0.275165 elapsed_min=271.5
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:167:EPOCH 033 train_loss=0.433713 val_loss=0.463354 val_dice=0.214576 val_precision=0.149040 val_recall=0.382985 best=0.275165 elapsed_min=280.0
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:172:EPOCH 034 train_loss=0.441082 val_loss=0.460800 val_dice=0.230288 val_precision=0.169466 val_recall=0.359208 best=0.275165 elapsed_min=288.5
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:177:EPOCH 035 train_loss=0.438050 val_loss=0.461329 val_dice=0.255506 val_precision=0.181839 val_recall=0.429514 best=0.275165 elapsed_min=297.0
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:182:EPOCH 036 train_loss=0.420644 val_loss=0.466383 val_dice=0.239369 val_precision=0.155263 val_recall=0.522302 best=0.275165 elapsed_min=305.5
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:187:EPOCH 037 train_loss=0.420247 val_loss=0.465001 val_dice=0.229943 val_precision=0.149787 val_recall=0.494643 best=0.275165 elapsed_min=313.9
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:192:EPOCH 038 train_loss=0.442221 val_loss=0.454498 val_dice=0.167754 val_precision=0.184183 val_recall=0.154016 best=0.275165 elapsed_min=322.4
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:197:EPOCH 039 train_loss=0.443751 val_loss=0.450430 val_dice=0.249975 val_precision=0.183709 val_recall=0.391022 best=0.275165 elapsed_min=330.9
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:202:EPOCH 040 train_loss=0.430550 val_loss=0.452433 val_dice=0.271401 val_precision=0.283026 val_recall=0.260693 best=0.275165 elapsed_min=339.3
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:207:EPOCH 041 train_loss=0.443002 val_loss=0.453387 val_dice=0.226092 val_precision=0.202020 val_recall=0.256677 best=0.275165 elapsed_min=347.8
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:212:EPOCH 042 train_loss=0.437746 val_loss=0.446105 val_dice=0.291305 val_precision=0.251279 val_recall=0.346499 best=0.291305 elapsed_min=356.5
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:217:EPOCH 043 train_loss=0.427448 val_loss=0.451607 val_dice=0.217372 val_precision=0.142659 val_recall=0.456392 best=0.291305 elapsed_min=365.0
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:222:EPOCH 044 train_loss=0.421100 val_loss=0.439496 val_dice=0.308680 val_precision=0.245374 val_recall=0.416010 best=0.308680 elapsed_min=376.3
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:227:EPOCH 045 train_loss=0.435031 val_loss=0.462024 val_dice=0.243413 val_precision=0.164914 val_recall=0.464529 best=0.308680 elapsed_min=389.1
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:232:EPOCH 046 train_loss=0.421245 val_loss=0.459163 val_dice=0.252154 val_precision=0.167321 val_recall=0.511478 best=0.308680 elapsed_min=398.9
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:237:EPOCH 047 train_loss=0.410241 val_loss=0.454737 val_dice=0.276184 val_precision=0.205788 val_recall=0.419786 best=0.308680 elapsed_min=407.4
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:242:EPOCH 048 train_loss=0.427201 val_loss=0.450336 val_dice=0.269914 val_precision=0.194638 val_recall=0.440137 best=0.308680 elapsed_min=415.9
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:247:EPOCH 049 train_loss=0.442781 val_loss=0.451658 val_dice=0.266500 val_precision=0.257195 val_recall=0.276503 best=0.308680 elapsed_min=424.4
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:252:EPOCH 050 train_loss=0.419376 val_loss=0.457823 val_dice=0.217707 val_precision=0.135386 val_recall=0.555452 best=0.308680 elapsed_min=432.8
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:2:RESUME epoch=50 best_val_dice=0.367370
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:9:EPOCH 050 train_loss=0.416314 val_loss=0.453715 val_dice=0.286637 val_precision=0.180658 val_recall=0.693418 best=0.367370 elapsed_min=8.3
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:14:EPOCH 051 train_loss=0.453673 val_loss=0.453172 val_dice=0.262730 val_precision=0.211600 val_recall=0.346444 best=0.367370 elapsed_min=16.5
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:19:EPOCH 052 train_loss=0.409309 val_loss=0.442612 val_dice=0.376027 val_precision=0.282215 val_recall=0.563264 best=0.376027 elapsed_min=24.7
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:24:EPOCH 053 train_loss=0.439335 val_loss=0.443985 val_dice=0.380571 val_precision=0.424110 val_recall=0.345139 best=0.380571 elapsed_min=32.9
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:29:EPOCH 054 train_loss=0.447276 val_loss=0.445041 val_dice=0.425384 val_precision=0.370854 val_recall=0.498715 best=0.425384 elapsed_min=41.1
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:34:EPOCH 055 train_loss=0.427699 val_loss=0.451420 val_dice=0.350257 val_precision=0.260424 val_recall=0.534700 best=0.425384 elapsed_min=49.3
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:39:EPOCH 056 train_loss=0.426692 val_loss=0.475709 val_dice=0.190790 val_precision=0.108650 val_recall=0.781920 best=0.425384 elapsed_min=57.5
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:44:EPOCH 057 train_loss=0.457442 val_loss=0.456812 val_dice=0.308432 val_precision=0.303325 val_recall=0.313714 best=0.425384 elapsed_min=65.8
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:49:EPOCH 058 train_loss=0.429706 val_loss=0.442806 val_dice=0.347959 val_precision=0.245207 val_recall=0.598945 best=0.425384 elapsed_min=74.0
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:54:EPOCH 059 train_loss=0.429686 val_loss=0.434063 val_dice=0.409925 val_precision=0.329511 val_recall=0.542258 best=0.425384 elapsed_min=82.2
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:59:EPOCH 060 train_loss=0.411757 val_loss=0.438704 val_dice=0.416119 val_precision=0.316983 val_recall=0.605482 best=0.425384 elapsed_min=90.4
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:64:EPOCH 061 train_loss=0.429466 val_loss=0.449119 val_dice=0.349713 val_precision=0.268617 val_recall=0.500950 best=0.425384 elapsed_min=98.6
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:69:EPOCH 062 train_loss=0.441227 val_loss=0.429128 val_dice=0.423200 val_precision=0.365928 val_recall=0.501726 best=0.425384 elapsed_min=106.8
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:74:EPOCH 063 train_loss=0.426974 val_loss=0.442482 val_dice=0.365410 val_precision=0.271615 val_recall=0.558152 best=0.425384 elapsed_min=115.0
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:79:EPOCH 064 train_loss=0.409294 val_loss=0.429752 val_dice=0.489137 val_precision=0.454637 val_recall=0.529304 best=0.489137 elapsed_min=123.2
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:84:EPOCH 065 train_loss=0.429007 val_loss=0.425511 val_dice=0.425216 val_precision=0.387947 val_recall=0.470406 best=0.489137 elapsed_min=131.4
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:89:EPOCH 066 train_loss=0.427213 val_loss=0.427513 val_dice=0.375063 val_precision=0.261715 val_recall=0.661603 best=0.489137 elapsed_min=139.6
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:94:EPOCH 067 train_loss=0.428950 val_loss=0.422227 val_dice=0.282580 val_precision=0.173813 val_recall=0.755102 best=0.489137 elapsed_min=147.8
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:99:EPOCH 068 train_loss=0.444036 val_loss=0.415415 val_dice=0.481035 val_precision=0.504100 val_recall=0.459988 best=0.489137 elapsed_min=156.0
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:104:EPOCH 069 train_loss=0.395316 val_loss=0.410463 val_dice=0.443858 val_precision=0.354308 val_recall=0.593983 best=0.489137 elapsed_min=164.2
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:109:EPOCH 070 train_loss=0.408099 val_loss=0.431831 val_dice=0.539004 val_precision=0.548685 val_recall=0.529659 best=0.539004 elapsed_min=172.4
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:114:EPOCH 071 train_loss=0.413183 val_loss=0.419119 val_dice=0.392210 val_precision=0.275673 val_recall=0.679434 best=0.539004 elapsed_min=180.7
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:119:EPOCH 072 train_loss=0.443808 val_loss=0.438151 val_dice=0.445767 val_precision=0.398119 val_recall=0.506372 best=0.539004 elapsed_min=188.8
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:124:EPOCH 073 train_loss=0.401304 val_loss=0.435013 val_dice=0.434314 val_precision=0.332644 val_recall=0.625493 best=0.539004 elapsed_min=197.0
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:129:EPOCH 074 train_loss=0.412175 val_loss=nan val_dice=0.429887 val_precision=0.315779 val_recall=0.673122 best=0.539004 elapsed_min=205.2
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:134:EPOCH 075 train_loss=nan val_loss=nan val_dice=0.267436 val_precision=0.199014 val_recall=0.407552 best=0.539004 elapsed_min=213.2
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:139:EPOCH 076 train_loss=nan val_loss=nan val_dice=0.267436 val_precision=0.199014 val_recall=0.407552 best=0.539004 elapsed_min=221.2
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:144:EPOCH 077 train_loss=nan val_loss=nan val_dice=0.257658 val_precision=0.186943 val_recall=0.414424 best=0.539004 elapsed_min=229.1
reports/training/r100_fp16_3seed_queue_20261014_150435.log:4:PASS seed=42 validation_dice=0.544072
reports/training/r100_fp16_3seed_queue_20261014_150435.log:6:PASS seed=43 validation_dice=0.569856
reports/training/r100_fp16_3seed_queue_20261014_150435.log:8:PASS seed=44 validation_dice=0.572980
reports/training/r100_fp16_3seed_queue_20261014_150435.log:9:THREE SEEDS COMPLETE validation Dice mean=0.562302 sample_SD=0.015865; no test evaluation
reports/training/R100_thebe_seed42_20261005_102737.log:5:/shared/home/khavarj/projects/fault_detection/.venv_train/lib/python3.13/site-packages/torch/autograd/graph.py:824: UserWarning: max_pool3d_with_indices_backward_cuda does not have a deterministic implementation, but you set 'torch.use_deterministic_algorithms(True, warn_only=True)'. You can file an issue at https://github.com/pytorch/pytorch/issues to help us prioritize adding deterministic support for this operation. (Triggered internally at /pytorch/aten/src/ATen/Context.cpp:93.)
reports/training/R100_thebe_seed42_20261005_102737.log:12:epoch=001/100 loss=0.211608 val_dice=0.000006 val_pr_auc=0.034823 minutes=3.26
reports/training/R100_thebe_seed42_20261005_102737.log:14:epoch=002/100 loss=0.131591 val_dice=0.000001 val_pr_auc=0.039528 minutes=3.33
reports/training/R100_thebe_seed42_20261005_102737.log:16:epoch=003/100 loss=0.105220 val_dice=0.000001 val_pr_auc=0.043710 minutes=3.23
reports/training/R100_thebe_seed42_20261005_102737.log:18:epoch=004/100 loss=0.101674 val_dice=0.000000 val_pr_auc=0.043505 minutes=3.32
reports/training/R100_thebe_seed42_20261005_102737.log:20:epoch=005/100 loss=0.113378 val_dice=0.000000 val_pr_auc=0.038386 minutes=3.04
reports/training/R100_thebe_seed42_20261005_102737.log:22:epoch=006/100 loss=0.102869 val_dice=0.000000 val_pr_auc=0.047210 minutes=3.22
reports/training/R100_thebe_seed42_20261005_102737.log:24:epoch=007/100 loss=0.106725 val_dice=0.000000 val_pr_auc=0.049760 minutes=3.20
reports/training/R100_thebe_seed42_20261005_102737.log:26:epoch=008/100 loss=0.096674 val_dice=0.000000 val_pr_auc=0.048672 minutes=3.13
reports/training/R100_thebe_seed42_20261005_102737.log:28:epoch=009/100 loss=0.099541 val_dice=0.000000 val_pr_auc=0.043619 minutes=3.24
reports/training/R100_thebe_seed42_20261005_102737.log:30:epoch=010/100 loss=0.107934 val_dice=0.000000 val_pr_auc=0.055916 minutes=3.05
reports/training/R100_thebe_seed42_20261005_102737.log:32:epoch=011/100 loss=0.099936 val_dice=0.000000 val_pr_auc=0.061880 minutes=3.10
reports/training/R100_thebe_seed42_20261005_102737.log:34:epoch=012/100 loss=0.102164 val_dice=0.000000 val_pr_auc=0.049965 minutes=3.15
reports/training/R100_thebe_seed42_20261005_102737.log:36:epoch=013/100 loss=0.109964 val_dice=0.000000 val_pr_auc=0.061470 minutes=3.00
reports/training/R100_thebe_seed42_20261005_102737.log:38:epoch=014/100 loss=0.096900 val_dice=0.000000 val_pr_auc=0.089677 minutes=3.07
reports/training/R100_thebe_seed42_20261005_102737.log:40:epoch=015/100 loss=0.089464 val_dice=0.000000 val_pr_auc=0.117684 minutes=3.21
reports/training/R100_thebe_seed42_20261005_102737.log:42:epoch=016/100 loss=0.088687 val_dice=0.000000 val_pr_auc=0.107323 minutes=3.15
reports/training/R100_thebe_seed42_20261005_102737.log:44:epoch=017/100 loss=0.083734 val_dice=0.000000 val_pr_auc=0.135083 minutes=3.13
reports/training/R100_thebe_seed42_20261005_102737.log:46:epoch=018/100 loss=0.087998 val_dice=0.000000 val_pr_auc=0.171241 minutes=3.32
reports/training/R100_thebe_seed42_20261005_102737.log:48:epoch=019/100 loss=0.090926 val_dice=0.000000 val_pr_auc=0.184733 minutes=3.11
reports/training/R100_thebe_seed42_20261005_102737.log:50:epoch=020/100 loss=0.077623 val_dice=0.000000 val_pr_auc=0.207758 minutes=3.15
reports/training/R100_thebe_seed42_20261005_102737.log:52:epoch=021/100 loss=0.073180 val_dice=0.000013 val_pr_auc=0.213077 minutes=3.13
reports/training/R100_thebe_seed42_20261005_102737.log:54:epoch=022/100 loss=0.077549 val_dice=0.000690 val_pr_auc=0.212709 minutes=3.08
reports/training/R100_thebe_seed42_20261005_102737.log:56:epoch=023/100 loss=0.080129 val_dice=0.001580 val_pr_auc=0.250377 minutes=3.05
reports/training/R100_thebe_seed42_resume_20261005_131346.log:6:/shared/home/khavarj/projects/fault_detection/.venv_train/lib/python3.13/site-packages/torch/autograd/graph.py:824: UserWarning: max_pool3d_with_indices_backward_cuda does not have a deterministic implementation, but you set 'torch.use_deterministic_algorithms(True, warn_only=True)'. You can file an issue at https://github.com/pytorch/pytorch/issues to help us prioritize adding deterministic support for this operation. (Triggered internally at /pytorch/aten/src/ATen/Context.cpp:93.)
reports/training/R100_thebe_seed42_resume_20261005_131346.log:13:epoch=024/100 loss=0.078920 val_dice=0.001420 val_pr_auc=0.236420 minutes=3.32
reports/training/R100_thebe_seed42_resume_20261005_131346.log:15:epoch=025/100 loss=0.065565 val_dice=0.002473 val_pr_auc=0.260316 minutes=3.20
reports/training/R100_thebe_seed42_resume_20261005_131346.log:17:epoch=026/100 loss=0.068080 val_dice=0.003456 val_pr_auc=0.263557 minutes=3.25
reports/training/R100_thebe_seed42_resume_20261005_131346.log:19:epoch=027/100 loss=0.080750 val_dice=0.011536 val_pr_auc=0.259436 minutes=3.12
reports/training/R100_thebe_seed42_resume_20261005_131346.log:21:epoch=028/100 loss=0.075161 val_dice=0.018024 val_pr_auc=0.297481 minutes=3.05
reports/training/R100_thebe_seed42_resume_20261005_131346.log:23:epoch=029/100 loss=0.084217 val_dice=0.048370 val_pr_auc=0.295427 minutes=3.27
reports/training/R100_thebe_seed42_resume_20261005_131346.log:25:epoch=030/100 loss=0.069108 val_dice=0.027934 val_pr_auc=0.322924 minutes=3.16
reports/training/R100_thebe_seed42_resume_20261005_131346.log:27:epoch=031/100 loss=0.078519 val_dice=0.077669 val_pr_auc=0.336544 minutes=3.02
reports/training/R100_thebe_seed42_resume_20261005_131346.log:29:epoch=032/100 loss=0.062892 val_dice=0.304055 val_pr_auc=0.336719 minutes=3.36
reports/training/R100_thebe_seed42_resume_20261005_131346.log:31:epoch=033/100 loss=0.072173 val_dice=0.149602 val_pr_auc=0.348334 minutes=3.39
reports/training/R100_thebe_seed42_resume_20261005_131346.log:33:epoch=034/100 loss=0.070201 val_dice=0.174907 val_pr_auc=0.342185 minutes=3.24
reports/training/R100_thebe_seed42_resume_20261005_131346.log:35:epoch=035/100 loss=0.073527 val_dice=0.148241 val_pr_auc=0.369592 minutes=3.27
reports/training/R100_thebe_seed42_resume_20261005_131346.log:37:epoch=036/100 loss=0.069229 val_dice=0.193048 val_pr_auc=0.379670 minutes=3.25
reports/training/R100_thebe_seed42_resume_20261005_131346.log:39:epoch=037/100 loss=0.063905 val_dice=0.006665 val_pr_auc=0.330679 minutes=3.15
reports/training/R100_thebe_seed42_resume_20261005_131346.log:41:epoch=038/100 loss=0.080337 val_dice=0.244056 val_pr_auc=0.374059 minutes=3.23
reports/training/R100_thebe_seed42_resume_20261005_131346.log:43:epoch=039/100 loss=0.066486 val_dice=0.255052 val_pr_auc=0.404267 minutes=3.12
reports/training/R100_thebe_seed42_resume_20261005_131346.log:45:epoch=040/100 loss=0.065938 val_dice=0.210433 val_pr_auc=0.382206 minutes=3.17
reports/training/R100_thebe_seed42_resume_20261005_131346.log:47:epoch=041/100 loss=0.062026 val_dice=0.407483 val_pr_auc=0.373383 minutes=3.09
reports/training/R100_thebe_seed42_resume_20261005_131346.log:49:epoch=042/100 loss=0.075279 val_dice=0.123915 val_pr_auc=0.388560 minutes=3.06
reports/training/R100_thebe_seed42_resume_20261005_131346.log:51:epoch=043/100 loss=0.065071 val_dice=0.270480 val_pr_auc=0.393687 minutes=3.09
reports/training/R100_thebe_seed42_resume_20261005_131346.log:53:epoch=044/100 loss=0.064441 val_dice=0.172999 val_pr_auc=0.384315 minutes=3.11
reports/training/R100_thebe_seed42_resume_20261005_131346.log:55:epoch=045/100 loss=0.063953 val_dice=0.286662 val_pr_auc=0.441626 minutes=3.20
reports/training/R100_thebe_seed42_resume_20261005_131346.log:57:epoch=046/100 loss=0.059598 val_dice=0.413131 val_pr_auc=0.401415 minutes=3.25
reports/training/R100_thebe_seed42_resume_20261005_131346.log:59:epoch=047/100 loss=0.062477 val_dice=0.245688 val_pr_auc=0.443531 minutes=3.15
reports/training/R100_thebe_seed42_resume_20261005_131346.log:61:epoch=048/100 loss=0.059514 val_dice=0.245539 val_pr_auc=0.437099 minutes=3.14
reports/training/R100_thebe_seed42_resume_20261005_131346.log:63:epoch=049/100 loss=0.061393 val_dice=0.279920 val_pr_auc=0.438496 minutes=3.24
reports/training/R100_thebe_seed42_resume_20261005_131346.log:65:epoch=050/100 loss=0.070041 val_dice=0.288117 val_pr_auc=0.453892 minutes=3.29
reports/training/R100_thebe_seed42_resume_20261005_131346.log:67:epoch=051/100 loss=0.065202 val_dice=0.266200 val_pr_auc=0.460510 minutes=3.37
reports/training/R100_thebe_seed42_resume_20261005_131346.log:69:epoch=052/100 loss=0.066613 val_dice=0.356431 val_pr_auc=0.427422 minutes=3.12
reports/training/R100_thebe_seed42_resume_20261005_131346.log:71:epoch=053/100 loss=0.066192 val_dice=0.342636 val_pr_auc=0.433051 minutes=3.27
reports/training/R100_thebe_seed42_resume_20261005_131346.log:73:epoch=054/100 loss=0.064246 val_dice=0.341244 val_pr_auc=0.459710 minutes=3.38
reports/training/R100_thebe_seed42_resume_20261005_131346.log:75:epoch=055/100 loss=0.054061 val_dice=0.428206 val_pr_auc=0.477125 minutes=3.27
reports/training/R100_thebe_seed42_resume_20261005_131346.log:77:epoch=056/100 loss=0.060517 val_dice=0.356121 val_pr_auc=0.480524 minutes=3.22
reports/training/R100_thebe_seed42_resume_20261005_131346.log:79:epoch=057/100 loss=0.063365 val_dice=0.428462 val_pr_auc=0.440082 minutes=3.14
reports/training/R100_thebe_seed42_resume_20261005_131346.log:81:epoch=058/100 loss=0.050335 val_dice=0.308301 val_pr_auc=0.512327 minutes=3.39
reports/training/R100_thebe_seed42_resume_20261005_131346.log:83:epoch=059/100 loss=0.067371 val_dice=0.472297 val_pr_auc=0.479524 minutes=3.24
reports/training/R100_thebe_seed42_resume_20261005_131346.log:85:epoch=060/100 loss=0.061604 val_dice=0.441440 val_pr_auc=0.516968 minutes=3.25
reports/training/R100_thebe_seed42_resume_20261005_131346.log:87:epoch=061/100 loss=0.062467 val_dice=0.247468 val_pr_auc=0.517348 minutes=3.13
reports/training/R100_thebe_seed42_resume_20261005_131346.log:89:epoch=062/100 loss=0.059376 val_dice=0.262464 val_pr_auc=0.489979 minutes=3.06
reports/training/R100_thebe_seed42_resume_20261005_131346.log:91:epoch=063/100 loss=0.063021 val_dice=0.350626 val_pr_auc=0.518379 minutes=3.16
reports/training/R100_thebe_seed42_resume_20261005_131346.log:93:epoch=064/100 loss=0.059923 val_dice=0.359455 val_pr_auc=0.538676 minutes=3.10
reports/training/R100_thebe_seed42_resume_20261005_131346.log:95:epoch=065/100 loss=0.047842 val_dice=0.269996 val_pr_auc=0.492450 minutes=3.30
reports/training/R100_thebe_seed42_resume_20261005_131346.log:97:epoch=066/100 loss=0.055280 val_dice=0.415410 val_pr_auc=0.508203 minutes=3.15
reports/training/R100_thebe_seed42_resume_20261005_131346.log:99:epoch=067/100 loss=0.061079 val_dice=0.383309 val_pr_auc=0.545594 minutes=3.14
reports/training/R100_thebe_seed42_resume_20261005_131346.log:101:epoch=068/100 loss=0.052238 val_dice=0.502782 val_pr_auc=0.544847 minutes=3.20
reports/training/R100_thebe_seed42_resume_20261005_131346.log:103:epoch=069/100 loss=0.058578 val_dice=0.496378 val_pr_auc=0.556591 minutes=3.28
reports/training/R100_thebe_seed42_resume_20261005_131346.log:105:epoch=070/100 loss=0.053104 val_dice=0.313013 val_pr_auc=0.547534 minutes=3.34
reports/training/R100_thebe_seed42_resume_20261005_131346.log:107:epoch=071/100 loss=0.053821 val_dice=0.393332 val_pr_auc=0.567882 minutes=3.18
reports/training/R100_thebe_seed42_resume_20261005_131346.log:109:epoch=072/100 loss=0.059722 val_dice=0.413933 val_pr_auc=0.571626 minutes=3.33
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:22:        "dice": 0.5440719430427761,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:23:        "iou": 0.373694249824297,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:24:        "precision": 0.5267658204531103,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:25:        "recall": 0.562553828427201,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:31:        "roc_auc_approx": 0.9560342463297409,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:47:        "dice": 0.5698556833270347,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:48:        "iou": 0.39846026494216036,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:49:        "precision": 0.5643889729910121,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:50:        "recall": 0.5754293313318344,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:56:        "roc_auc_approx": 0.9612985077763903,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:72:        "dice": 0.5729798256899185,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:73:        "iou": 0.40152188175400944,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:74:        "precision": 0.5655692044103381,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:75:        "recall": 0.5805872272731943,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:81:        "roc_auc_approx": 0.9589852925995812,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:102:  "validation_dice_mean": 0.5623024840199098,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:103:  "validation_dice_sample_sd": 0.015865198852050486
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/best.pt: binary file matches (found "\0" byte around offset 4)
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/history.csv:1:epoch,train_loss,train_patches,resampled_no_data_candidates,excluded_training_positive_labels,seconds,val_threshold,val_dice,val_iou,val_precision,val_recall,val_specificity,val_balanced_accuracy,val_accuracy,val_mcc,val_pr_auc_approx,val_roc_auc_approx,val_tp,val_fp,val_fn,val_tn
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/last.pt: binary file matches (found "\0" byte around offset 4)
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:5:/shared/home/khavarj/projects/fault_detection/.venv_train/lib/python3.13/site-packages/torch/autograd/graph.py:824: UserWarning: max_pool3d_with_indices_backward_cuda does not have a deterministic implementation, but you set 'torch.use_deterministic_algorithms(True, warn_only=True)'. You can file an issue at https://github.com/pytorch/pytorch/issues to help us prioritize adding deterministic support for this operation. (Triggered internally at /pytorch/aten/src/ATen/Context.cpp:93.)
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:18:epoch=001/100 loss=0.211608 val_dice=0.000006 val_pr_auc=0.034823 minutes=3.12
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:26:epoch=002/100 loss=0.131591 val_dice=0.000001 val_pr_auc=0.039528 minutes=3.08
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:34:epoch=003/100 loss=0.105220 val_dice=0.000001 val_pr_auc=0.043710 minutes=3.09
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:42:epoch=004/100 loss=0.101674 val_dice=0.000000 val_pr_auc=0.043505 minutes=3.18
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:50:epoch=005/100 loss=0.113378 val_dice=0.000000 val_pr_auc=0.038386 minutes=2.88
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:58:epoch=006/100 loss=0.102869 val_dice=0.000000 val_pr_auc=0.047210 minutes=3.07
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:66:epoch=007/100 loss=0.106725 val_dice=0.000000 val_pr_auc=0.049760 minutes=3.06
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:74:epoch=008/100 loss=0.096674 val_dice=0.000000 val_pr_auc=0.048672 minutes=2.99
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:82:epoch=009/100 loss=0.099541 val_dice=0.000000 val_pr_auc=0.043619 minutes=3.14
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:90:epoch=010/100 loss=0.107934 val_dice=0.000000 val_pr_auc=0.055916 minutes=2.92
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:98:epoch=011/100 loss=0.099936 val_dice=0.000000 val_pr_auc=0.061880 minutes=2.95
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:106:epoch=012/100 loss=0.102164 val_dice=0.000000 val_pr_auc=0.049965 minutes=3.01
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:114:epoch=013/100 loss=0.109964 val_dice=0.000000 val_pr_auc=0.061470 minutes=2.89
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:122:epoch=014/100 loss=0.096900 val_dice=0.000000 val_pr_auc=0.089677 minutes=2.94
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:130:epoch=015/100 loss=0.089464 val_dice=0.000000 val_pr_auc=0.117684 minutes=3.08
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:138:epoch=016/100 loss=0.088687 val_dice=0.000000 val_pr_auc=0.107323 minutes=3.07
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:146:epoch=017/100 loss=0.083734 val_dice=0.000000 val_pr_auc=0.135083 minutes=3.05
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:154:epoch=018/100 loss=0.087998 val_dice=0.000000 val_pr_auc=0.171241 minutes=3.17
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:162:epoch=019/100 loss=0.090926 val_dice=0.000000 val_pr_auc=0.184733 minutes=2.97
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:170:epoch=020/100 loss=0.077623 val_dice=0.000000 val_pr_auc=0.207758 minutes=3.01
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:178:epoch=021/100 loss=0.073180 val_dice=0.000013 val_pr_auc=0.213077 minutes=3.03
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:186:epoch=022/100 loss=0.077549 val_dice=0.000690 val_pr_auc=0.212709 minutes=2.94
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:194:epoch=023/100 loss=0.080129 val_dice=0.001580 val_pr_auc=0.250377 minutes=2.89
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:202:epoch=024/100 loss=0.085101 val_dice=0.007970 val_pr_auc=0.210663 minutes=3.00
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:210:epoch=025/100 loss=0.067014 val_dice=0.002319 val_pr_auc=0.270853 minutes=3.03
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:218:epoch=026/100 loss=0.074720 val_dice=0.008281 val_pr_auc=0.258356 minutes=3.06
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:226:epoch=027/100 loss=0.078038 val_dice=0.002668 val_pr_auc=0.299218 minutes=3.02
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:234:epoch=028/100 loss=0.069081 val_dice=0.016612 val_pr_auc=0.289297 minutes=3.13
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:242:epoch=029/100 loss=0.067600 val_dice=0.025738 val_pr_auc=0.304789 minutes=3.06
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:250:epoch=030/100 loss=0.069910 val_dice=0.025284 val_pr_auc=0.307485 minutes=3.10
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:258:epoch=031/100 loss=0.071929 val_dice=0.005624 val_pr_auc=0.335175 minutes=3.10
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:266:epoch=032/100 loss=0.074831 val_dice=0.014670 val_pr_auc=0.324274 minutes=2.89
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:274:epoch=033/100 loss=0.069609 val_dice=0.119484 val_pr_auc=0.339538 minutes=3.03
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:282:epoch=034/100 loss=0.061320 val_dice=0.095749 val_pr_auc=0.323181 minutes=3.06
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:290:epoch=035/100 loss=0.071427 val_dice=0.106897 val_pr_auc=0.358173 minutes=3.10
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:298:epoch=036/100 loss=0.070403 val_dice=0.117125 val_pr_auc=0.339758 minutes=3.03
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:306:epoch=037/100 loss=0.072179 val_dice=0.206109 val_pr_auc=0.363270 minutes=2.98
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:314:epoch=038/100 loss=0.072133 val_dice=0.230500 val_pr_auc=0.384911 minutes=3.18
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:322:epoch=039/100 loss=0.066432 val_dice=0.149482 val_pr_auc=0.392297 minutes=2.94
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:330:epoch=040/100 loss=0.059668 val_dice=0.100121 val_pr_auc=0.388984 minutes=3.16
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:338:epoch=041/100 loss=0.060640 val_dice=0.237473 val_pr_auc=0.413392 minutes=3.08
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:346:epoch=042/100 loss=0.065647 val_dice=0.136110 val_pr_auc=0.418763 minutes=3.14
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:354:epoch=043/100 loss=0.065825 val_dice=0.211336 val_pr_auc=0.382685 minutes=3.06
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:362:epoch=044/100 loss=0.058033 val_dice=0.226795 val_pr_auc=0.418009 minutes=3.08
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:370:epoch=045/100 loss=0.068560 val_dice=0.331624 val_pr_auc=0.419339 minutes=3.45
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:378:epoch=046/100 loss=0.064055 val_dice=0.310719 val_pr_auc=0.433676 minutes=3.54
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:386:epoch=047/100 loss=0.065738 val_dice=0.201582 val_pr_auc=0.400658 minutes=3.41
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:394:epoch=048/100 loss=0.064558 val_dice=0.331357 val_pr_auc=0.459623 minutes=3.51
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:402:epoch=049/100 loss=0.057787 val_dice=0.402787 val_pr_auc=0.448123 minutes=3.57
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/run_config.json:5:  "precision": "float16_autocast",
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/run_config.json:746:  "threshold_selection": "best Dice on complete validation volume with 2048 bins",
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/status.json:7:  "precision": "float16_autocast",
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/status.json:12:  "best_checkpoint": "runs/R100_fp16_clean_3seeds_20261014_150435/seed42/best.pt",
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/validation_selection.json:7:    "dice": 0.5440719430427761,
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/validation_selection.json:8:    "iou": 0.373694249824297,
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/validation_selection.json:9:    "precision": 0.5267658204531103,
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/validation_selection.json:10:    "recall": 0.562553828427201,
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/validation_selection.json:16:    "roc_auc_approx": 0.9560342463297409,
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/best.pt: binary file matches (found "\0" byte around offset 4)
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/history.csv:1:epoch,train_loss,train_patches,resampled_no_data_candidates,excluded_training_positive_labels,seconds,val_threshold,val_dice,val_iou,val_precision,val_recall,val_specificity,val_balanced_accuracy,val_accuracy,val_mcc,val_pr_auc_approx,val_roc_auc_approx,val_tp,val_fp,val_fn,val_tn
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/last.pt: binary file matches (found "\0" byte around offset 4)
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:5:/shared/home/khavarj/projects/fault_detection/.venv_train/lib/python3.13/site-packages/torch/autograd/graph.py:824: UserWarning: max_pool3d_with_indices_backward_cuda does not have a deterministic implementation, but you set 'torch.use_deterministic_algorithms(True, warn_only=True)'. You can file an issue at https://github.com/pytorch/pytorch/issues to help us prioritize adding deterministic support for this operation. (Triggered internally at /pytorch/aten/src/ATen/Context.cpp:93.)
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:18:epoch=001/100 loss=0.207313 val_dice=0.000010 val_pr_auc=0.032889 minutes=3.25
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:26:epoch=002/100 loss=0.134325 val_dice=0.000000 val_pr_auc=0.037506 minutes=3.40
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:34:epoch=003/100 loss=0.113158 val_dice=0.000000 val_pr_auc=0.044267 minutes=3.32
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:42:epoch=004/100 loss=0.106803 val_dice=0.000000 val_pr_auc=0.047515 minutes=3.69
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:50:epoch=005/100 loss=0.112586 val_dice=0.000000 val_pr_auc=0.055564 minutes=3.44
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:58:epoch=006/100 loss=0.086832 val_dice=0.000000 val_pr_auc=0.073312 minutes=3.49
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:66:epoch=007/100 loss=0.096694 val_dice=0.000000 val_pr_auc=0.063642 minutes=3.45
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:74:epoch=008/100 loss=0.099798 val_dice=0.000000 val_pr_auc=0.111352 minutes=3.47
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:82:epoch=009/100 loss=0.086573 val_dice=0.000000 val_pr_auc=0.109360 minutes=3.49
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:90:epoch=010/100 loss=0.085202 val_dice=0.000000 val_pr_auc=0.129471 minutes=3.51
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:98:epoch=011/100 loss=0.082043 val_dice=0.000000 val_pr_auc=0.190129 minutes=3.52
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:106:epoch=012/100 loss=0.087391 val_dice=0.000000 val_pr_auc=0.182149 minutes=3.50
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:114:epoch=013/100 loss=0.086629 val_dice=0.051217 val_pr_auc=0.227169 minutes=3.42
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:122:epoch=014/100 loss=0.075188 val_dice=0.156249 val_pr_auc=0.287682 minutes=3.35
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:130:epoch=015/100 loss=0.069022 val_dice=0.128348 val_pr_auc=0.318932 minutes=3.42
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:138:epoch=016/100 loss=0.068342 val_dice=0.144531 val_pr_auc=0.319825 minutes=3.32
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:146:epoch=017/100 loss=0.076954 val_dice=0.317299 val_pr_auc=0.348228 minutes=3.34
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:154:epoch=018/100 loss=0.066294 val_dice=0.330689 val_pr_auc=0.360967 minutes=3.26
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:162:epoch=019/100 loss=0.078325 val_dice=0.154955 val_pr_auc=0.370729 minutes=3.36
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:170:epoch=020/100 loss=0.073825 val_dice=0.170272 val_pr_auc=0.410673 minutes=3.24
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:178:epoch=021/100 loss=0.074191 val_dice=0.326550 val_pr_auc=0.398516 minutes=3.31
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:186:epoch=022/100 loss=0.066618 val_dice=0.254137 val_pr_auc=0.428462 minutes=3.34
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:194:epoch=023/100 loss=0.069498 val_dice=0.275050 val_pr_auc=0.445187 minutes=3.20
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:202:epoch=024/100 loss=0.059472 val_dice=0.351567 val_pr_auc=0.463566 minutes=3.10
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:210:epoch=025/100 loss=0.061590 val_dice=0.290421 val_pr_auc=0.448529 minutes=3.13
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:218:epoch=026/100 loss=0.063974 val_dice=0.367536 val_pr_auc=0.458521 minutes=3.20
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:226:epoch=027/100 loss=0.066937 val_dice=0.184101 val_pr_auc=0.455209 minutes=3.18
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:234:epoch=028/100 loss=0.061171 val_dice=0.436915 val_pr_auc=0.483792 minutes=3.02
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:242:epoch=029/100 loss=0.054366 val_dice=0.275544 val_pr_auc=0.491174 minutes=3.15
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:250:epoch=030/100 loss=0.061534 val_dice=0.440431 val_pr_auc=0.473313 minutes=3.21
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:258:epoch=031/100 loss=0.058599 val_dice=0.331349 val_pr_auc=0.489746 minutes=3.11
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:266:epoch=032/100 loss=0.058002 val_dice=0.317572 val_pr_auc=0.507873 minutes=3.07
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:274:epoch=033/100 loss=0.064508 val_dice=0.132827 val_pr_auc=0.479362 minutes=3.13
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:282:epoch=034/100 loss=0.075195 val_dice=0.320840 val_pr_auc=0.513074 minutes=3.11
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:290:epoch=035/100 loss=0.061724 val_dice=0.474487 val_pr_auc=0.514265 minutes=3.13
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:298:epoch=036/100 loss=0.065400 val_dice=0.426747 val_pr_auc=0.542522 minutes=2.92
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:306:epoch=037/100 loss=0.056895 val_dice=0.471250 val_pr_auc=0.497020 minutes=2.93
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:314:epoch=038/100 loss=0.056790 val_dice=0.273526 val_pr_auc=0.525836 minutes=3.00
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:322:epoch=039/100 loss=0.060411 val_dice=0.326792 val_pr_auc=0.532453 minutes=3.10
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:330:epoch=040/100 loss=0.054520 val_dice=0.531070 val_pr_auc=0.546094 minutes=2.84
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:338:epoch=041/100 loss=0.061186 val_dice=0.334449 val_pr_auc=0.560378 minutes=2.95
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:346:epoch=042/100 loss=0.050234 val_dice=0.319623 val_pr_auc=0.526732 minutes=3.17
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:354:epoch=043/100 loss=0.053101 val_dice=0.448451 val_pr_auc=0.550102 minutes=2.91
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:362:epoch=044/100 loss=0.055038 val_dice=0.513862 val_pr_auc=0.562986 minutes=2.98
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:370:epoch=045/100 loss=0.055149 val_dice=0.341347 val_pr_auc=0.525956 minutes=2.94
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:378:epoch=046/100 loss=0.055819 val_dice=0.411702 val_pr_auc=0.558411 minutes=3.00
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:386:epoch=047/100 loss=0.056744 val_dice=0.540495 val_pr_auc=0.568879 minutes=2.94
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:394:epoch=048/100 loss=0.057409 val_dice=0.400572 val_pr_auc=0.577831 minutes=3.09
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:402:epoch=049/100 loss=0.056376 val_dice=0.510591 val_pr_auc=0.571619 minutes=3.07
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/run_config.json:5:  "precision": "float16_autocast",
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/run_config.json:746:  "threshold_selection": "best Dice on complete validation volume with 2048 bins",
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/status.json:7:  "precision": "float16_autocast",
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/status.json:12:  "best_checkpoint": "runs/R100_fp16_clean_3seeds_20261014_150435/seed43/best.pt",
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/validation_selection.json:7:    "dice": 0.5698556833270347,
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/validation_selection.json:8:    "iou": 0.39846026494216036,
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/validation_selection.json:9:    "precision": 0.5643889729910121,
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/validation_selection.json:10:    "recall": 0.5754293313318344,
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/validation_selection.json:16:    "roc_auc_approx": 0.9612985077763903,
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/best.pt: binary file matches (found "\0" byte around offset 4)
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/history.csv:1:epoch,train_loss,train_patches,resampled_no_data_candidates,excluded_training_positive_labels,seconds,val_threshold,val_dice,val_iou,val_precision,val_recall,val_specificity,val_balanced_accuracy,val_accuracy,val_mcc,val_pr_auc_approx,val_roc_auc_approx,val_tp,val_fp,val_fn,val_tn
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/last.pt: binary file matches (found "\0" byte around offset 4)
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:5:/shared/home/khavarj/projects/fault_detection/.venv_train/lib/python3.13/site-packages/torch/autograd/graph.py:824: UserWarning: max_pool3d_with_indices_backward_cuda does not have a deterministic implementation, but you set 'torch.use_deterministic_algorithms(True, warn_only=True)'. You can file an issue at https://github.com/pytorch/pytorch/issues to help us prioritize adding deterministic support for this operation. (Triggered internally at /pytorch/aten/src/ATen/Context.cpp:93.)
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:18:epoch=001/100 loss=0.214208 val_dice=0.000002 val_pr_auc=0.032531 minutes=2.98
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:26:epoch=002/100 loss=0.131131 val_dice=0.000002 val_pr_auc=0.041499 minutes=2.94
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:34:epoch=003/100 loss=0.093528 val_dice=0.000000 val_pr_auc=0.046544 minutes=3.03
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:42:epoch=004/100 loss=0.094511 val_dice=0.000000 val_pr_auc=0.045681 minutes=3.09
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:50:epoch=005/100 loss=0.103709 val_dice=0.000000 val_pr_auc=0.047491 minutes=3.07
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:58:epoch=006/100 loss=0.102382 val_dice=0.000000 val_pr_auc=0.053118 minutes=3.10
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:66:epoch=007/100 loss=0.096109 val_dice=0.000000 val_pr_auc=0.057679 minutes=3.11
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:74:epoch=008/100 loss=0.094502 val_dice=0.000000 val_pr_auc=0.055288 minutes=3.11
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:82:epoch=009/100 loss=0.099929 val_dice=0.000000 val_pr_auc=0.056435 minutes=3.03
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:90:epoch=010/100 loss=0.091132 val_dice=0.000000 val_pr_auc=0.072109 minutes=2.94
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:98:epoch=011/100 loss=0.091550 val_dice=0.000000 val_pr_auc=0.076607 minutes=3.09
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:106:epoch=012/100 loss=0.082483 val_dice=0.000000 val_pr_auc=0.089395 minutes=3.11
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:114:epoch=013/100 loss=0.095675 val_dice=0.000000 val_pr_auc=0.099517 minutes=3.09
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:122:epoch=014/100 loss=0.087235 val_dice=0.000000 val_pr_auc=0.128630 minutes=3.04
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:130:epoch=015/100 loss=0.092547 val_dice=0.000000 val_pr_auc=0.118855 minutes=2.92
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:138:epoch=016/100 loss=0.094852 val_dice=0.000000 val_pr_auc=0.121884 minutes=3.03
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:146:epoch=017/100 loss=0.087888 val_dice=0.000000 val_pr_auc=0.172786 minutes=3.01
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:154:epoch=018/100 loss=0.083555 val_dice=0.000000 val_pr_auc=0.163500 minutes=3.08
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:162:epoch=019/100 loss=0.089364 val_dice=0.000000 val_pr_auc=0.127726 minutes=3.08
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:170:epoch=020/100 loss=0.086457 val_dice=0.000000 val_pr_auc=0.175177 minutes=3.08
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:178:epoch=021/100 loss=0.069410 val_dice=0.000008 val_pr_auc=0.254670 minutes=2.94
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:186:epoch=022/100 loss=0.074515 val_dice=0.141201 val_pr_auc=0.326820 minutes=2.99
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:194:epoch=023/100 loss=0.072652 val_dice=0.166533 val_pr_auc=0.313903 minutes=3.00
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:202:epoch=024/100 loss=0.064151 val_dice=0.172646 val_pr_auc=0.363963 minutes=3.08
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:210:epoch=025/100 loss=0.073862 val_dice=0.196468 val_pr_auc=0.386662 minutes=3.01
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:218:epoch=026/100 loss=0.072094 val_dice=0.132655 val_pr_auc=0.394473 minutes=2.98
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:226:epoch=027/100 loss=0.065739 val_dice=0.374149 val_pr_auc=0.413061 minutes=3.01
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:234:epoch=028/100 loss=0.068670 val_dice=0.317358 val_pr_auc=0.418032 minutes=3.12
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:242:epoch=029/100 loss=0.070705 val_dice=0.171511 val_pr_auc=0.374978 minutes=2.99
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:250:epoch=030/100 loss=0.064441 val_dice=0.323407 val_pr_auc=0.425493 minutes=3.18
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:258:epoch=031/100 loss=0.069248 val_dice=0.248666 val_pr_auc=0.454737 minutes=2.88
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:266:epoch=032/100 loss=0.061221 val_dice=0.377182 val_pr_auc=0.450258 minutes=3.05
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:274:epoch=033/100 loss=0.062718 val_dice=0.327263 val_pr_auc=0.424330 minutes=2.95
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:282:epoch=034/100 loss=0.063943 val_dice=0.247668 val_pr_auc=0.459621 minutes=3.10
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:290:epoch=035/100 loss=0.058946 val_dice=0.092848 val_pr_auc=0.377327 minutes=2.93
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:298:epoch=036/100 loss=0.059221 val_dice=0.481173 val_pr_auc=0.501920 minutes=3.02
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:306:epoch=037/100 loss=0.053694 val_dice=0.232841 val_pr_auc=0.466201 minutes=2.99
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:314:epoch=038/100 loss=0.061848 val_dice=0.460287 val_pr_auc=0.494024 minutes=3.04
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:322:epoch=039/100 loss=0.057948 val_dice=0.371737 val_pr_auc=0.489074 minutes=3.08
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:330:epoch=040/100 loss=0.059008 val_dice=0.406601 val_pr_auc=0.503391 minutes=3.08
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:338:epoch=041/100 loss=0.056795 val_dice=0.441511 val_pr_auc=0.519499 minutes=3.02
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:346:epoch=042/100 loss=0.065448 val_dice=0.413127 val_pr_auc=0.536155 minutes=3.01
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:354:epoch=043/100 loss=0.059635 val_dice=0.239140 val_pr_auc=0.526799 minutes=2.99
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:362:epoch=044/100 loss=0.069650 val_dice=0.433576 val_pr_auc=0.552912 minutes=3.09
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:370:epoch=045/100 loss=0.055908 val_dice=0.435073 val_pr_auc=0.542746 minutes=2.97
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:378:epoch=046/100 loss=0.054000 val_dice=0.487242 val_pr_auc=0.555513 minutes=2.88
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:386:epoch=047/100 loss=0.055662 val_dice=0.378074 val_pr_auc=0.507225 minutes=3.08
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:394:epoch=048/100 loss=0.059597 val_dice=0.478686 val_pr_auc=0.550781 minutes=3.11
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:402:epoch=049/100 loss=0.059587 val_dice=0.516431 val_pr_auc=0.572820 minutes=3.02
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/run_config.json:5:  "precision": "float16_autocast",
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/run_config.json:746:  "threshold_selection": "best Dice on complete validation volume with 2048 bins",
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/status.json:7:  "precision": "float16_autocast",
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/status.json:12:  "best_checkpoint": "runs/R100_fp16_clean_3seeds_20261014_150435/seed44/best.pt",
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/validation_selection.json:7:    "dice": 0.5729798256899185,
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/validation_selection.json:8:    "iou": 0.40152188175400944,
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/validation_selection.json:9:    "precision": 0.5655692044103381,
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/validation_selection.json:10:    "recall": 0.5805872272731943,
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/validation_selection.json:16:    "roc_auc_approx": 0.9589852925995812,
runs/R100_fp16_clean_3seeds_20261014_150435/smoke.log:5:/shared/home/khavarj/projects/fault_detection/.venv_train/lib/python3.13/site-packages/torch/autograd/graph.py:824: UserWarning: max_pool3d_with_indices_backward_cuda does not have a deterministic implementation, but you set 'torch.use_deterministic_algorithms(True, warn_only=True)'. You can file an issue at https://github.com/pytorch/pytorch/issues to help us prioritize adding deterministic support for this operation. (Triggered internally at /pytorch/aten/src/ATen/Context.cpp:93.)
runs/R100_fp16_clean_3seeds_20261014_150435/smoke.log:12:epoch=001/1 loss=0.779829 val_dice=0.068725 val_pr_auc=0.033207 minutes=0.17
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/best.pt: binary file matches (found "\0" byte around offset 4)
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/history.csv:1:epoch,train_loss,train_patches,resampled_no_data_candidates,excluded_training_positive_labels,seconds,val_threshold,val_dice,val_iou,val_precision,val_recall,val_specificity,val_balanced_accuracy,val_accuracy,val_mcc,val_pr_auc_approx,val_roc_auc_approx,val_tp,val_fp,val_fn,val_tn
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/last.pt: binary file matches (found "\0" byte around offset 4)
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/run_config.json:5:  "precision": "float16_autocast",
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/run_config.json:116:  "threshold_selection": "best Dice on smoke validation subset",
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/status.json:7:  "precision": "float16_autocast",
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/status.json:12:  "best_checkpoint": "runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/best.pt",
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/validation_selection.json:7:    "dice": 0.06884626641830875,
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/validation_selection.json:8:    "iou": 0.035650329241587765,
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/validation_selection.json:9:    "precision": 0.035650329241587765,
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/validation_selection.json:10:    "recall": 1.0,
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/validation_selection.json:16:    "roc_auc_approx": 0.4517016441816569,
```

### Errors and numerical warnings

```text
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:129:EPOCH 074 train_loss=0.412175 val_loss=nan val_dice=0.429887 val_precision=0.315779 val_recall=0.673122 best=0.539004 elapsed_min=205.2
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:131:epoch=75/100 train_patch=32/64 loss=nan
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:133:epoch=75/100 train_patch=64/64 loss=nan
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:134:EPOCH 075 train_loss=nan val_loss=nan val_dice=0.267436 val_precision=0.199014 val_recall=0.407552 best=0.539004 elapsed_min=213.2
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:135:epoch=76/100 train_patch=16/64 loss=nan
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:138:epoch=76/100 train_patch=64/64 loss=nan
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:139:EPOCH 076 train_loss=nan val_loss=nan val_dice=0.267436 val_precision=0.199014 val_recall=0.407552 best=0.539004 elapsed_min=221.2
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:140:epoch=77/100 train_patch=16/64 loss=nan
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:142:epoch=77/100 train_patch=48/64 loss=nan
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:144:EPOCH 077 train_loss=nan val_loss=nan val_dice=0.257658 val_precision=0.186943 val_recall=0.414424 best=0.539004 elapsed_min=229.1
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:145:epoch=78/100 train_patch=16/64 loss=nan
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:147:epoch=78/100 train_patch=48/64 loss=nan
reports/training/r100_fp16_3seed_queue_20261014_145225.log:3:Traceback (most recent call last):
reports/training/r100_fp16_3seed_queue_20261014_145225.log:14:    raise RuntimeError(message)
reports/training/r100_fp16_3seed_queue_20261014_145225.log:15:RuntimeError: Trainer exited with code 1; see runs/R100_fp16_clean_3seeds_20261014_145225/smoke.log
reports/training/r100_fp16_3seed_queue_20261014_145510.log:3:Traceback (most recent call last):
reports/training/r100_fp16_3seed_queue_20261014_145510.log:14:    raise RuntimeError(message)
reports/training/r100_fp16_3seed_queue_20261014_145510.log:15:RuntimeError: Trainer exited with code 1; see runs/R100_fp16_clean_3seeds_20261014_145510/seed42.log
reports/training/R100_thebe_seed42_20261005_102737.log:57:Traceback (most recent call last):
reports/training/R100_thebe_seed42_20261005_102737.log:69:    raise RuntimeError(f"Constant observed seismic at {origin}")
reports/training/R100_thebe_seed42_20261005_102737.log:70:RuntimeError: Constant observed seismic at (203, 1696, 199)
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/best.pt: binary file matches (found "\0" byte around offset 4)
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/best.pt: binary file matches (found "\0" byte around offset 4)
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/last.pt: binary file matches (found "\0" byte around offset 4)
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/best.pt: binary file matches (found "\0" byte around offset 4)
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/last.pt: binary file matches (found "\0" byte around offset 4)
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/best.pt: binary file matches (found "\0" byte around offset 4)
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/last.pt: binary file matches (found "\0" byte around offset 4)
```

### Newest log tails

`runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log`

```text
epoch=97/100 train_patch=60/360 loss=0.191846
epoch=97/100 train_patch=120/360 loss=0.277550
epoch=97/100 train_patch=180/360 loss=0.091489
epoch=97/100 train_patch=240/360 loss=0.000342
epoch=97/100 train_patch=300/360 loss=0.000000
epoch=97/100 train_patch=360/360 loss=0.036241
evaluation_patches=100/128
epoch=097/100 loss=0.051889 val_dice=0.548214 val_pr_auc=0.633269 minutes=3.00
epoch=98/100 train_patch=60/360 loss=0.136171
epoch=98/100 train_patch=120/360 loss=0.000024
epoch=98/100 train_patch=180/360 loss=0.081139
epoch=98/100 train_patch=240/360 loss=0.116304
epoch=98/100 train_patch=300/360 loss=0.194777
epoch=98/100 train_patch=360/360 loss=0.003614
evaluation_patches=100/128
epoch=098/100 loss=0.047368 val_dice=0.417820 val_pr_auc=0.618263 minutes=3.19
epoch=99/100 train_patch=60/360 loss=0.096293
epoch=99/100 train_patch=120/360 loss=0.000711
epoch=99/100 train_patch=180/360 loss=0.053551
epoch=99/100 train_patch=240/360 loss=0.011706
epoch=99/100 train_patch=300/360 loss=0.030885
epoch=99/100 train_patch=360/360 loss=0.015740
evaluation_patches=100/128
epoch=099/100 loss=0.051740 val_dice=0.571887 val_pr_auc=0.641601 minutes=3.10
epoch=100/100 train_patch=60/360 loss=0.105558
epoch=100/100 train_patch=120/360 loss=0.000385
epoch=100/100 train_patch=180/360 loss=0.002327
epoch=100/100 train_patch=240/360 loss=0.000015
epoch=100/100 train_patch=300/360 loss=0.049922
epoch=100/100 train_patch=360/360 loss=0.008582
evaluation_patches=100/128
epoch=100/100 loss=0.050488 val_dice=0.544014 val_pr_auc=0.647909 minutes=2.94
BEST EPOCH: 95; full validation begins
evaluation_patches=100/650
evaluation_patches=200/650
evaluation_patches=400/650
evaluation_patches=500/650
VALIDATION THRESHOLD: 0.244141; test evaluation disabled
R100 VALIDATION-ONLY COMPLETE seed=44 epochs=100 best_epoch=95
QUEUE CHILD EXIT 2026-10-15T02:29:39.074418+00:00 code=0
```

`reports/training/r100_fp16_3seed_queue_20261014_150435.log`

```text
nohup: ignoring input
START seed=42 smoke=True pid=1945423 log=runs/R100_fp16_clean_3seeds_20261014_150435/smoke.log
START seed=42 smoke=False pid=1946437 log=runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log
PASS seed=42 validation_dice=0.544072
START seed=43 smoke=False pid=3264730 log=runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log
PASS seed=43 validation_dice=0.569856
START seed=44 smoke=False pid=379744 log=runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log
PASS seed=44 validation_dice=0.572980
THREE SEEDS COMPLETE validation Dice mean=0.562302 sample_SD=0.015865; no test evaluation
```

`runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log`

```text
epoch=97/100 train_patch=60/360 loss=0.000206
epoch=97/100 train_patch=120/360 loss=0.000322
epoch=97/100 train_patch=180/360 loss=0.000758
epoch=97/100 train_patch=240/360 loss=0.184065
epoch=97/100 train_patch=300/360 loss=0.005448
epoch=97/100 train_patch=360/360 loss=0.217553
evaluation_patches=100/128
epoch=097/100 loss=0.043323 val_dice=0.499799 val_pr_auc=0.628407 minutes=3.00
epoch=98/100 train_patch=60/360 loss=0.013608
epoch=98/100 train_patch=120/360 loss=0.090962
epoch=98/100 train_patch=180/360 loss=0.005916
epoch=98/100 train_patch=240/360 loss=0.000000
epoch=98/100 train_patch=300/360 loss=0.165707
epoch=98/100 train_patch=360/360 loss=0.094480
evaluation_patches=100/128
epoch=098/100 loss=0.050284 val_dice=0.579185 val_pr_auc=0.642430 minutes=3.08
epoch=99/100 train_patch=60/360 loss=0.118951
epoch=99/100 train_patch=120/360 loss=0.010276
epoch=99/100 train_patch=180/360 loss=0.000355
epoch=99/100 train_patch=240/360 loss=0.000069
epoch=99/100 train_patch=300/360 loss=0.011696
epoch=99/100 train_patch=360/360 loss=0.006897
evaluation_patches=100/128
epoch=099/100 loss=0.043900 val_dice=0.568614 val_pr_auc=0.648535 minutes=3.05
epoch=100/100 train_patch=60/360 loss=0.009470
epoch=100/100 train_patch=120/360 loss=0.002223
epoch=100/100 train_patch=180/360 loss=0.004774
epoch=100/100 train_patch=240/360 loss=0.000046
epoch=100/100 train_patch=300/360 loss=0.112857
epoch=100/100 train_patch=360/360 loss=0.013399
evaluation_patches=100/128
epoch=100/100 loss=0.048542 val_dice=0.477356 val_pr_auc=0.643192 minutes=3.15
BEST EPOCH: 93; full validation begins
evaluation_patches=100/650
evaluation_patches=200/650
evaluation_patches=400/650
evaluation_patches=500/650
VALIDATION THRESHOLD: 0.279297; test evaluation disabled
R100 VALIDATION-ONLY COMPLETE seed=43 epochs=100 best_epoch=93
QUEUE CHILD EXIT 2026-10-14T21:26:57.084942+00:00 code=0
```

## Seed 44

### Seed/run files

```text
reports/evaluation/p1_cracks_expert_seed42_20261009_134425/expert_per_section.csv
reports/evaluation/p1_cracks_expert_seed42_20261009_134425/final_metrics.json
reports/training/r100_fp16_3seed_queue_20261014_150435.log
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/best.pt
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/history.csv
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/last.pt
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/run_config.json
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/status.json
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/validation_selection.json
```

### Checkpoint metadata only

```text
2026-10-14T11:04:47.5321731820	17562443 bytes	runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/last.pt
2026-10-14T11:04:47.5634066030	17562443 bytes	runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/best.pt
2026-10-14T15:57:17.5696980420	17562443 bytes	runs/R100_fp16_clean_3seeds_20261014_150435/seed42/best.pt
2026-10-14T16:12:25.0497427080	17562443 bytes	runs/R100_fp16_clean_3seeds_20261014_150435/seed42/last.pt
2026-10-14T21:04:18.6093364070	17562443 bytes	runs/R100_fp16_clean_3seeds_20261014_150435/seed43/best.pt
2026-10-14T21:25:29.7404980360	17562443 bytes	runs/R100_fp16_clean_3seeds_20261014_150435/seed43/last.pt
2026-10-15T02:12:55.4137767480	17562443 bytes	runs/R100_fp16_clean_3seeds_20261014_150435/seed44/best.pt
2026-10-15T02:28:11.9270560240	17562443 bytes	runs/R100_fp16_clean_3seeds_20261014_150435/seed44/last.pt
```

### Settings

```text
reports/evaluation/p1_cracks_expert_seed42_20261009_134425/expert_per_section.csv:1:section,valid_pixels,certain_fault_pixels,threshold,dice,iou,precision,recall,specificity,balanced_accuracy,accuracy,mcc,pr_auc_approx,roc_auc_approx,tp,fp,fn,tn
reports/evaluation/p1_cracks_expert_seed42_20261009_134425/final_metrics.json:13:    "precision": 0.038205351398402906,
reports/evaluation/p1_cracks_expert_seed42_20261009_134425/final_metrics.json:17:    "threshold": 0.98095703125,
reports/evaluation/p1_cracks_expert_seed42_20261009_134425/final_metrics.json:42:  "threshold": 0.98095703125,
reports/training/baseline_A_smoke.log:1:device=cuda; parameters=1,459,585; amp=True
reports/training/baseline_A_smoke.log:2:/shared/home/khavarj/projects/fault_detection/scripts/faultseg3d_baseline.py:553: FutureWarning: `torch.cuda.amp.GradScaler(args...)` is deprecated. Please use `torch.amp.GradScaler('cuda', args...)` instead.
reports/training/baseline_A_smoke.log:3:  scaler = torch.cuda.amp.GradScaler(enabled=amp_enabled)
reports/training/baseline_A_smoke.log:6:SMOKE PASS: input=(1, 1, 128, 128, 128), output=(1, 1, 128, 128, 128), loss=0.778994, peak_cuda_GiB=1.218
reports/training/baseline_A_synthetic_bce_seed42.log:2:device=cuda; parameters=1,459,585; amp=True
reports/training/baseline_A_synthetic_bce_seed42.log:3:/shared/home/khavarj/projects/fault_detection/scripts/faultseg3d_baseline.py:553: FutureWarning: `torch.cuda.amp.GradScaler(args...)` is deprecated. Please use `torch.amp.GradScaler('cuda', args...)` instead.
reports/training/baseline_A_synthetic_bce_seed42.log:4:  scaler = torch.cuda.amp.GradScaler(enabled=amp_enabled)
reports/training/baseline_A_synthetic_bce_seed42.log:11:epoch=001 loss=0.314965 val_dice=0.000000 val_iou=0.000000 val_pr_auc=0.076771 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:12:epoch=002 loss=0.254361 val_dice=0.000000 val_iou=0.000000 val_pr_auc=0.096252 minutes=0.30
reports/training/baseline_A_synthetic_bce_seed42.log:13:epoch=003 loss=0.238950 val_dice=0.000000 val_iou=0.000000 val_pr_auc=0.182016 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:14:epoch=004 loss=0.200252 val_dice=0.118262 val_iou=0.062847 val_pr_auc=0.390901 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:15:epoch=005 loss=0.168745 val_dice=0.398029 val_iou=0.248462 val_pr_auc=0.481942 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:16:epoch=006 loss=0.153221 val_dice=0.465434 val_iou=0.303300 val_pr_auc=0.539682 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:17:epoch=007 loss=0.141764 val_dice=0.497805 val_iou=0.331385 val_pr_auc=0.586533 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:18:epoch=008 loss=0.135450 val_dice=0.534810 val_iou=0.365011 val_pr_auc=0.613936 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:19:epoch=009 loss=0.128391 val_dice=0.600041 val_iou=0.428614 val_pr_auc=0.641996 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:20:epoch=010 loss=0.122253 val_dice=0.583450 val_iou=0.411881 val_pr_auc=0.643059 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:21:epoch=011 loss=0.118308 val_dice=0.619101 val_iou=0.448332 val_pr_auc=0.686354 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:22:epoch=012 loss=0.112667 val_dice=0.641208 val_iou=0.471895 val_pr_auc=0.700150 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:23:epoch=013 loss=0.109114 val_dice=0.633384 val_iou=0.463469 val_pr_auc=0.715915 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:24:epoch=014 loss=0.106602 val_dice=0.650868 val_iou=0.482435 val_pr_auc=0.711744 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:25:epoch=015 loss=0.102564 val_dice=0.666159 val_iou=0.499429 val_pr_auc=0.731226 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:26:epoch=016 loss=0.099363 val_dice=0.685561 val_iou=0.521562 val_pr_auc=0.750862 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:27:epoch=017 loss=0.097281 val_dice=0.687228 val_iou=0.523494 val_pr_auc=0.757492 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:28:epoch=018 loss=0.093142 val_dice=0.689824 val_iou=0.526513 val_pr_auc=0.765094 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:29:epoch=019 loss=0.093322 val_dice=0.693366 val_iou=0.530651 val_pr_auc=0.769579 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:30:epoch=020 loss=0.089892 val_dice=0.718609 val_iou=0.560804 val_pr_auc=0.786135 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:31:epoch=021 loss=0.088231 val_dice=0.706142 val_iou=0.545765 val_pr_auc=0.776918 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:2:device=cuda; parameters=1,459,585; amp=True
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:3:/shared/home/khavarj/projects/fault_detection/scripts/faultseg3d_baseline.py:553: FutureWarning: `torch.cuda.amp.GradScaler(args...)` is deprecated. Please use `torch.amp.GradScaler('cuda', args...)` instead.
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:4:  scaler = torch.cuda.amp.GradScaler(enabled=amp_enabled)
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:11:epoch=001 loss=1.044174 val_dice=0.220347 val_iou=0.123815 val_pr_auc=0.148267 minutes=0.32
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:12:epoch=002 loss=0.861660 val_dice=0.330021 val_iou=0.197620 val_pr_auc=0.352460 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:13:epoch=003 loss=0.738569 val_dice=0.395203 val_iou=0.246264 val_pr_auc=0.445970 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:14:epoch=004 loss=0.669487 val_dice=0.445811 val_iou=0.286844 val_pr_auc=0.506100 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:15:epoch=005 loss=0.623482 val_dice=0.465448 val_iou=0.303312 val_pr_auc=0.544250 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:16:epoch=006 loss=0.581583 val_dice=0.524423 val_iou=0.355402 val_pr_auc=0.591176 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:17:epoch=007 loss=0.542672 val_dice=0.502238 val_iou=0.335326 val_pr_auc=0.626267 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:18:epoch=008 loss=0.501275 val_dice=0.549318 val_iou=0.378662 val_pr_auc=0.664116 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:19:epoch=009 loss=0.463011 val_dice=0.595464 val_iou=0.423958 val_pr_auc=0.699814 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:20:epoch=010 loss=0.438031 val_dice=0.629139 val_iou=0.458937 val_pr_auc=0.719178 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:21:epoch=011 loss=0.414671 val_dice=0.645080 val_iou=0.476102 val_pr_auc=0.733999 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:22:epoch=012 loss=0.398844 val_dice=0.607199 val_iou=0.435955 val_pr_auc=0.718977 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:23:epoch=013 loss=0.377859 val_dice=0.631336 val_iou=0.461280 val_pr_auc=0.757730 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:24:epoch=014 loss=0.364058 val_dice=0.675847 val_iou=0.510400 val_pr_auc=0.768168 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:25:epoch=015 loss=0.352412 val_dice=0.654198 val_iou=0.486103 val_pr_auc=0.759199 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:26:epoch=016 loss=0.342353 val_dice=0.688899 val_iou=0.525436 val_pr_auc=0.774911 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:27:epoch=017 loss=0.335509 val_dice=0.678364 val_iou=0.513276 val_pr_auc=0.782113 minutes=0.32
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:28:epoch=018 loss=0.322418 val_dice=0.682413 val_iou=0.517926 val_pr_auc=0.791560 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:29:epoch=019 loss=0.317725 val_dice=0.684473 val_iou=0.520303 val_pr_auc=0.783781 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:30:epoch=020 loss=0.312603 val_dice=0.699316 val_iou=0.537653 val_pr_auc=0.800032 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:31:epoch=021 loss=0.304364 val_dice=0.666135 val_iou=0.499402 val_pr_auc=0.798243 minutes=0.31
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:2:parameters=45001057 epochs=100 train_patches=64 val_patches=32
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:3:epoch=1/100 train_patch=16/64 loss=0.50337
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:4:epoch=1/100 train_patch=32/64 loss=0.48165
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:5:epoch=1/100 train_patch=48/64 loss=0.39263
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:6:epoch=1/100 train_patch=64/64 loss=0.51061
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:7:EPOCH 001 train_loss=0.465645 val_loss=0.485600 val_dice=0.000000 val_precision=0.000000 val_recall=0.000000 best=0.000000 elapsed_min=8.5
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:8:epoch=2/100 train_patch=16/64 loss=0.50700
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:9:epoch=2/100 train_patch=32/64 loss=0.50687
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:10:epoch=2/100 train_patch=48/64 loss=0.51004
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:11:epoch=2/100 train_patch=64/64 loss=0.50326
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:12:EPOCH 002 train_loss=0.467679 val_loss=0.482254 val_dice=0.000000 val_precision=0.000000 val_recall=0.000000 best=0.000000 elapsed_min=17.0
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:13:epoch=3/100 train_patch=16/64 loss=0.50515
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:14:epoch=3/100 train_patch=32/64 loss=0.51582
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:15:epoch=3/100 train_patch=48/64 loss=0.38142
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:16:epoch=3/100 train_patch=64/64 loss=0.51498
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:17:EPOCH 003 train_loss=0.454671 val_loss=0.483168 val_dice=0.000000 val_precision=0.000000 val_recall=0.000000 best=0.000000 elapsed_min=25.5
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:18:epoch=4/100 train_patch=16/64 loss=0.35696
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:19:epoch=4/100 train_patch=32/64 loss=0.51711
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:20:epoch=4/100 train_patch=48/64 loss=0.51147
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:21:epoch=4/100 train_patch=64/64 loss=0.50276
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:22:EPOCH 004 train_loss=0.460464 val_loss=0.481467 val_dice=0.000000 val_precision=0.000000 val_recall=0.000000 best=0.000000 elapsed_min=34.0
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:23:epoch=5/100 train_patch=16/64 loss=0.50632
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:24:epoch=5/100 train_patch=32/64 loss=0.51415
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:25:epoch=5/100 train_patch=48/64 loss=0.50639
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:2:RESUME epoch=50 best_val_dice=0.367370
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:4:parameters=45001057 epochs=100 train_patches=64 val_patches=32
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:5:epoch=50/100 train_patch=16/64 loss=0.50684
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:6:epoch=50/100 train_patch=32/64 loss=0.51190
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:7:epoch=50/100 train_patch=48/64 loss=0.52828
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:8:epoch=50/100 train_patch=64/64 loss=0.25706
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:9:EPOCH 050 train_loss=0.416314 val_loss=0.453715 val_dice=0.286637 val_precision=0.180658 val_recall=0.693418 best=0.367370 elapsed_min=8.3
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:10:epoch=51/100 train_patch=16/64 loss=0.52553
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:11:epoch=51/100 train_patch=32/64 loss=0.50325
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:12:epoch=51/100 train_patch=48/64 loss=0.50754
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:13:epoch=51/100 train_patch=64/64 loss=0.50115
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:14:EPOCH 051 train_loss=0.453673 val_loss=0.453172 val_dice=0.262730 val_precision=0.211600 val_recall=0.346444 best=0.367370 elapsed_min=16.5
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:15:epoch=52/100 train_patch=16/64 loss=0.33214
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:16:epoch=52/100 train_patch=32/64 loss=0.50397
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:17:epoch=52/100 train_patch=48/64 loss=0.50738
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:18:epoch=52/100 train_patch=64/64 loss=0.50343
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:19:EPOCH 052 train_loss=0.409309 val_loss=0.442612 val_dice=0.376027 val_precision=0.282215 val_recall=0.563264 best=0.376027 elapsed_min=24.7
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:20:epoch=53/100 train_patch=16/64 loss=0.51703
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:21:epoch=53/100 train_patch=32/64 loss=0.52752
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:22:epoch=53/100 train_patch=48/64 loss=0.50514
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:23:epoch=53/100 train_patch=64/64 loss=0.32922
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:24:EPOCH 053 train_loss=0.439335 val_loss=0.443985 val_dice=0.380571 val_precision=0.424110 val_recall=0.345139 best=0.380571 elapsed_min=32.9
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:25:epoch=54/100 train_patch=16/64 loss=0.51174
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:26:epoch=54/100 train_patch=32/64 loss=0.50349
reports/training/r100_fp16_3seed_queue_20261014_145225.log:2:START seed=42 smoke=True pid=1899203 log=runs/R100_fp16_clean_3seeds_20261014_145225/smoke.log
reports/training/r100_fp16_3seed_queue_20261014_145510.log:1:START seed=42 smoke=True pid=1909458 log=runs/R100_fp16_clean_3seeds_20261014_145510/smoke.log
reports/training/r100_fp16_3seed_queue_20261014_145510.log:2:START seed=42 smoke=False pid=1911189 log=runs/R100_fp16_clean_3seeds_20261014_145510/seed42.log
reports/training/r100_fp16_3seed_queue_20261014_145510.log:8:    execute(run_dir, seed, expected_protocol=expected_protocol)
reports/training/r100_fp16_3seed_queue_20261014_150435.log:2:START seed=42 smoke=True pid=1945423 log=runs/R100_fp16_clean_3seeds_20261014_150435/smoke.log
reports/training/r100_fp16_3seed_queue_20261014_150435.log:3:START seed=42 smoke=False pid=1946437 log=runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log
reports/training/r100_fp16_3seed_queue_20261014_150435.log:4:PASS seed=42 validation_dice=0.544072
reports/training/r100_fp16_3seed_queue_20261014_150435.log:5:START seed=43 smoke=False pid=3264730 log=runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log
reports/training/r100_fp16_3seed_queue_20261014_150435.log:6:PASS seed=43 validation_dice=0.569856
reports/training/r100_fp16_3seed_queue_20261014_150435.log:7:START seed=44 smoke=False pid=379744 log=runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log
reports/training/r100_fp16_3seed_queue_20261014_150435.log:8:PASS seed=44 validation_dice=0.572980
reports/training/R100_thebe_seed42_20261005_102737.log:1:/shared/home/khavarj/projects/fault_detection/scripts/r100_full_run.py:237: FutureWarning: `torch.cuda.amp.GradScaler(args...)` is deprecated. Please use `torch.amp.GradScaler('cuda', args...)` instead.
reports/training/R100_thebe_seed42_20261005_102737.log:2:  scaler = torch.cuda.amp.GradScaler(enabled=True)
reports/training/R100_thebe_seed42_20261005_102737.log:12:epoch=001/100 loss=0.211608 val_dice=0.000006 val_pr_auc=0.034823 minutes=3.26
reports/training/R100_thebe_seed42_20261005_102737.log:14:epoch=002/100 loss=0.131591 val_dice=0.000001 val_pr_auc=0.039528 minutes=3.33
reports/training/R100_thebe_seed42_20261005_102737.log:16:epoch=003/100 loss=0.105220 val_dice=0.000001 val_pr_auc=0.043710 minutes=3.23
reports/training/R100_thebe_seed42_20261005_102737.log:18:epoch=004/100 loss=0.101674 val_dice=0.000000 val_pr_auc=0.043505 minutes=3.32
reports/training/R100_thebe_seed42_20261005_102737.log:20:epoch=005/100 loss=0.113378 val_dice=0.000000 val_pr_auc=0.038386 minutes=3.04
reports/training/R100_thebe_seed42_20261005_102737.log:22:epoch=006/100 loss=0.102869 val_dice=0.000000 val_pr_auc=0.047210 minutes=3.22
reports/training/R100_thebe_seed42_20261005_102737.log:24:epoch=007/100 loss=0.106725 val_dice=0.000000 val_pr_auc=0.049760 minutes=3.20
reports/training/R100_thebe_seed42_20261005_102737.log:26:epoch=008/100 loss=0.096674 val_dice=0.000000 val_pr_auc=0.048672 minutes=3.13
reports/training/R100_thebe_seed42_20261005_102737.log:28:epoch=009/100 loss=0.099541 val_dice=0.000000 val_pr_auc=0.043619 minutes=3.24
reports/training/R100_thebe_seed42_20261005_102737.log:30:epoch=010/100 loss=0.107934 val_dice=0.000000 val_pr_auc=0.055916 minutes=3.05
reports/training/R100_thebe_seed42_20261005_102737.log:32:epoch=011/100 loss=0.099936 val_dice=0.000000 val_pr_auc=0.061880 minutes=3.10
reports/training/R100_thebe_seed42_20261005_102737.log:34:epoch=012/100 loss=0.102164 val_dice=0.000000 val_pr_auc=0.049965 minutes=3.15
reports/training/R100_thebe_seed42_20261005_102737.log:36:epoch=013/100 loss=0.109964 val_dice=0.000000 val_pr_auc=0.061470 minutes=3.00
reports/training/R100_thebe_seed42_20261005_102737.log:38:epoch=014/100 loss=0.096900 val_dice=0.000000 val_pr_auc=0.089677 minutes=3.07
reports/training/R100_thebe_seed42_20261005_102737.log:40:epoch=015/100 loss=0.089464 val_dice=0.000000 val_pr_auc=0.117684 minutes=3.21
reports/training/R100_thebe_seed42_20261005_102737.log:42:epoch=016/100 loss=0.088687 val_dice=0.000000 val_pr_auc=0.107323 minutes=3.15
reports/training/R100_thebe_seed42_20261005_102737.log:44:epoch=017/100 loss=0.083734 val_dice=0.000000 val_pr_auc=0.135083 minutes=3.13
reports/training/R100_thebe_seed42_20261005_102737.log:46:epoch=018/100 loss=0.087998 val_dice=0.000000 val_pr_auc=0.171241 minutes=3.32
reports/training/R100_thebe_seed42_20261005_102737.log:48:epoch=019/100 loss=0.090926 val_dice=0.000000 val_pr_auc=0.184733 minutes=3.11
reports/training/R100_thebe_seed42_20261005_102737.log:50:epoch=020/100 loss=0.077623 val_dice=0.000000 val_pr_auc=0.207758 minutes=3.15
reports/training/R100_thebe_seed42_20261005_102737.log:52:epoch=021/100 loss=0.073180 val_dice=0.000013 val_pr_auc=0.213077 minutes=3.13
reports/training/R100_thebe_seed42_20261005_102737.log:54:epoch=022/100 loss=0.077549 val_dice=0.000690 val_pr_auc=0.212709 minutes=3.08
reports/training/R100_thebe_seed42_resume_20261005_131346.log:1:/shared/home/khavarj/projects/fault_detection/scripts/r100_full_run.py:250: FutureWarning: `torch.cuda.amp.GradScaler(args...)` is deprecated. Please use `torch.amp.GradScaler('cuda', args...)` instead.
reports/training/R100_thebe_seed42_resume_20261005_131346.log:2:  scaler = torch.cuda.amp.GradScaler(enabled=True)
reports/training/R100_thebe_seed42_resume_20261005_131346.log:4:RESUME PASS: completed epoch 23; continuing from epoch 24
reports/training/R100_thebe_seed42_resume_20261005_131346.log:13:epoch=024/100 loss=0.078920 val_dice=0.001420 val_pr_auc=0.236420 minutes=3.32
reports/training/R100_thebe_seed42_resume_20261005_131346.log:15:epoch=025/100 loss=0.065565 val_dice=0.002473 val_pr_auc=0.260316 minutes=3.20
reports/training/R100_thebe_seed42_resume_20261005_131346.log:17:epoch=026/100 loss=0.068080 val_dice=0.003456 val_pr_auc=0.263557 minutes=3.25
reports/training/R100_thebe_seed42_resume_20261005_131346.log:19:epoch=027/100 loss=0.080750 val_dice=0.011536 val_pr_auc=0.259436 minutes=3.12
reports/training/R100_thebe_seed42_resume_20261005_131346.log:21:epoch=028/100 loss=0.075161 val_dice=0.018024 val_pr_auc=0.297481 minutes=3.05
reports/training/R100_thebe_seed42_resume_20261005_131346.log:23:epoch=029/100 loss=0.084217 val_dice=0.048370 val_pr_auc=0.295427 minutes=3.27
reports/training/R100_thebe_seed42_resume_20261005_131346.log:25:epoch=030/100 loss=0.069108 val_dice=0.027934 val_pr_auc=0.322924 minutes=3.16
reports/training/R100_thebe_seed42_resume_20261005_131346.log:27:epoch=031/100 loss=0.078519 val_dice=0.077669 val_pr_auc=0.336544 minutes=3.02
reports/training/R100_thebe_seed42_resume_20261005_131346.log:29:epoch=032/100 loss=0.062892 val_dice=0.304055 val_pr_auc=0.336719 minutes=3.36
reports/training/R100_thebe_seed42_resume_20261005_131346.log:31:epoch=033/100 loss=0.072173 val_dice=0.149602 val_pr_auc=0.348334 minutes=3.39
reports/training/R100_thebe_seed42_resume_20261005_131346.log:33:epoch=034/100 loss=0.070201 val_dice=0.174907 val_pr_auc=0.342185 minutes=3.24
reports/training/R100_thebe_seed42_resume_20261005_131346.log:35:epoch=035/100 loss=0.073527 val_dice=0.148241 val_pr_auc=0.369592 minutes=3.27
reports/training/R100_thebe_seed42_resume_20261005_131346.log:37:epoch=036/100 loss=0.069229 val_dice=0.193048 val_pr_auc=0.379670 minutes=3.25
reports/training/R100_thebe_seed42_resume_20261005_131346.log:39:epoch=037/100 loss=0.063905 val_dice=0.006665 val_pr_auc=0.330679 minutes=3.15
reports/training/R100_thebe_seed42_resume_20261005_131346.log:41:epoch=038/100 loss=0.080337 val_dice=0.244056 val_pr_auc=0.374059 minutes=3.23
reports/training/R100_thebe_seed42_resume_20261005_131346.log:43:epoch=039/100 loss=0.066486 val_dice=0.255052 val_pr_auc=0.404267 minutes=3.12
reports/training/R100_thebe_seed42_resume_20261005_131346.log:45:epoch=040/100 loss=0.065938 val_dice=0.210433 val_pr_auc=0.382206 minutes=3.17
reports/training/R100_thebe_seed42_resume_20261005_131346.log:47:epoch=041/100 loss=0.062026 val_dice=0.407483 val_pr_auc=0.373383 minutes=3.09
reports/training/R100_thebe_seed42_resume_20261005_131346.log:49:epoch=042/100 loss=0.075279 val_dice=0.123915 val_pr_auc=0.388560 minutes=3.06
reports/training/R100_thebe_seed42_resume_20261005_131346.log:51:epoch=043/100 loss=0.065071 val_dice=0.270480 val_pr_auc=0.393687 minutes=3.09
reports/training/R100_thebe_seed42_resume_20261005_131346.log:53:epoch=044/100 loss=0.064441 val_dice=0.172999 val_pr_auc=0.384315 minutes=3.11
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:16:      "seed": 42,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:19:      "threshold": 0.31640625,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:21:        "threshold": 0.31640625,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:24:        "precision": 0.5267658204531103,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:41:      "seed": 43,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:44:      "threshold": 0.279296875,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:46:        "threshold": 0.279296875,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:49:        "precision": 0.5643889729910121,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:66:      "seed": 44,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:69:      "threshold": 0.244140625,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:71:        "threshold": 0.244140625,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:74:        "precision": 0.5655692044103381,
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/history.csv:1:epoch,train_loss,train_patches,resampled_no_data_candidates,excluded_training_positive_labels,seconds,val_threshold,val_dice,val_iou,val_precision,val_recall,val_specificity,val_balanced_accuracy,val_accuracy,val_mcc,val_pr_auc_approx,val_roc_auc_approx,val_tp,val_fp,val_fn,val_tn
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:2:QUEUE LAUNCH 2026-10-14T11:04:49.680315+00:00 ["/shared/home/khavarj/projects/fault_detection/.venv_train/bin/python", "-u", "/shared/home/khavarj/projects/fault_detection/scripts/train_r100_fp16_clean.py", "--seed", "42", "--validation-seed", "1042", "--thebe-root", "data/processed/thebe_h5", "--run-dir", "runs/R100_fp16_clean_3seeds_20261014_150435/seed42"]
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:7:epoch=1/100 train_patch=60/360 loss=0.269200
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:8:epoch=1/100 train_patch=120/360 loss=0.096066
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:9:epoch=1/100 train_patch=180/360 loss=0.145327
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:10:epoch=1/100 train_patch=240/360 loss=0.151376
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:11:epoch=1/100 train_patch=300/360 loss=0.019122
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:12:epoch=1/100 train_patch=360/360 loss=0.668354
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:18:epoch=001/100 loss=0.211608 val_dice=0.000006 val_pr_auc=0.034823 minutes=3.12
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:19:epoch=2/100 train_patch=60/360 loss=0.223522
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:20:epoch=2/100 train_patch=120/360 loss=0.020627
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:21:epoch=2/100 train_patch=180/360 loss=0.265117
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:22:epoch=2/100 train_patch=240/360 loss=0.046374
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:23:epoch=2/100 train_patch=300/360 loss=0.051667
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:24:epoch=2/100 train_patch=360/360 loss=0.037058
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:26:epoch=002/100 loss=0.131591 val_dice=0.000001 val_pr_auc=0.039528 minutes=3.08
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:27:epoch=3/100 train_patch=60/360 loss=0.030490
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:28:epoch=3/100 train_patch=120/360 loss=0.011700
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:29:epoch=3/100 train_patch=180/360 loss=0.011385
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:30:epoch=3/100 train_patch=240/360 loss=0.005840
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:31:epoch=3/100 train_patch=300/360 loss=0.293844
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:32:epoch=3/100 train_patch=360/360 loss=0.045493
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:34:epoch=003/100 loss=0.105220 val_dice=0.000001 val_pr_auc=0.043710 minutes=3.09
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:35:epoch=4/100 train_patch=60/360 loss=0.025259
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:36:epoch=4/100 train_patch=120/360 loss=0.279557
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/run_config.json:3:  "seed": 42,
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/run_config.json:5:  "precision": "float16_autocast",
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/run_config.json:732:  "epochs": 100,
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/run_config.json:734:  "patch_size": 128,
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/run_config.json:737:  "train_sampling": "40 observed random patches per train file each epoch; random axis-0 flip",
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/run_config.json:739:  "normalization": "per-patch z-score over observed voxels; axis reversal",
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/run_config.json:741:  "optimizer": "Adam",
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/run_config.json:742:  "learning_rate": 0.0001,
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/run_config.json:743:  "loss": "ordinary BCE averaged over observed voxels",
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/status.json:3:  "seed": 42,
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/status.json:7:  "precision": "float16_autocast",
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/status.json:11:  "threshold": 0.31640625,
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/validation_selection.json:3:  "threshold": 0.31640625,
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/validation_selection.json:6:    "threshold": 0.31640625,
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/validation_selection.json:9:    "precision": 0.5267658204531103,
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/history.csv:1:epoch,train_loss,train_patches,resampled_no_data_candidates,excluded_training_positive_labels,seconds,val_threshold,val_dice,val_iou,val_precision,val_recall,val_specificity,val_balanced_accuracy,val_accuracy,val_mcc,val_pr_auc_approx,val_roc_auc_approx,val_tp,val_fp,val_fn,val_tn
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:2:QUEUE LAUNCH 2026-10-14T16:13:56.661530+00:00 ["/shared/home/khavarj/projects/fault_detection/.venv_train/bin/python", "-u", "/shared/home/khavarj/projects/fault_detection/scripts/train_r100_fp16_clean.py", "--seed", "43", "--validation-seed", "1042", "--thebe-root", "data/processed/thebe_h5", "--run-dir", "runs/R100_fp16_clean_3seeds_20261014_150435/seed43", "--expected-protocol", "1febc1e47ba203ff08db82816ceadf616a5e7db345054cfbe45274b84c5f5437"]
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:7:epoch=1/100 train_patch=60/360 loss=0.025100
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:8:epoch=1/100 train_patch=120/360 loss=0.089748
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:9:epoch=1/100 train_patch=180/360 loss=0.030659
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:10:epoch=1/100 train_patch=240/360 loss=0.035034
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:11:epoch=1/100 train_patch=300/360 loss=0.176485
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:12:epoch=1/100 train_patch=360/360 loss=0.013613
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:18:epoch=001/100 loss=0.207313 val_dice=0.000010 val_pr_auc=0.032889 minutes=3.25
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:19:epoch=2/100 train_patch=60/360 loss=0.143345
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:20:epoch=2/100 train_patch=120/360 loss=0.170271
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:21:epoch=2/100 train_patch=180/360 loss=0.178730
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:22:epoch=2/100 train_patch=240/360 loss=0.423158
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:23:epoch=2/100 train_patch=300/360 loss=0.202504
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:24:epoch=2/100 train_patch=360/360 loss=0.010068
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:26:epoch=002/100 loss=0.134325 val_dice=0.000000 val_pr_auc=0.037506 minutes=3.40
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:27:epoch=3/100 train_patch=60/360 loss=0.073450
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:28:epoch=3/100 train_patch=120/360 loss=0.002192
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:29:epoch=3/100 train_patch=180/360 loss=0.011881
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:30:epoch=3/100 train_patch=240/360 loss=0.008659
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:31:epoch=3/100 train_patch=300/360 loss=0.012940
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:32:epoch=3/100 train_patch=360/360 loss=0.163898
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:34:epoch=003/100 loss=0.113158 val_dice=0.000000 val_pr_auc=0.044267 minutes=3.32
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:35:epoch=4/100 train_patch=60/360 loss=0.117194
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:36:epoch=4/100 train_patch=120/360 loss=0.025358
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/run_config.json:3:  "seed": 43,
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/run_config.json:5:  "precision": "float16_autocast",
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/run_config.json:732:  "epochs": 100,
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/run_config.json:734:  "patch_size": 128,
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/run_config.json:737:  "train_sampling": "40 observed random patches per train file each epoch; random axis-0 flip",
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/run_config.json:739:  "normalization": "per-patch z-score over observed voxels; axis reversal",
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/run_config.json:741:  "optimizer": "Adam",
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/run_config.json:742:  "learning_rate": 0.0001,
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/run_config.json:743:  "loss": "ordinary BCE averaged over observed voxels",
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/status.json:3:  "seed": 43,
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/status.json:7:  "precision": "float16_autocast",
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/status.json:11:  "threshold": 0.279296875,
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/validation_selection.json:3:  "threshold": 0.279296875,
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/validation_selection.json:6:    "threshold": 0.279296875,
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/validation_selection.json:9:    "precision": 0.5643889729910121,
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/best.pt: binary file matches (found "\0" byte around offset 4)
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/history.csv:1:epoch,train_loss,train_patches,resampled_no_data_candidates,excluded_training_positive_labels,seconds,val_threshold,val_dice,val_iou,val_precision,val_recall,val_specificity,val_balanced_accuracy,val_accuracy,val_mcc,val_pr_auc_approx,val_roc_auc_approx,val_tp,val_fp,val_fn,val_tn
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/last.pt: binary file matches (found "\0" byte around offset 4)
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:2:QUEUE LAUNCH 2026-10-14T21:26:57.138315+00:00 ["/shared/home/khavarj/projects/fault_detection/.venv_train/bin/python", "-u", "/shared/home/khavarj/projects/fault_detection/scripts/train_r100_fp16_clean.py", "--seed", "44", "--validation-seed", "1042", "--thebe-root", "data/processed/thebe_h5", "--run-dir", "runs/R100_fp16_clean_3seeds_20261014_150435/seed44", "--expected-protocol", "1febc1e47ba203ff08db82816ceadf616a5e7db345054cfbe45274b84c5f5437"]
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:7:epoch=1/100 train_patch=60/360 loss=0.128812
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:8:epoch=1/100 train_patch=120/360 loss=0.049892
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:9:epoch=1/100 train_patch=180/360 loss=0.137484
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:10:epoch=1/100 train_patch=240/360 loss=0.094210
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:11:epoch=1/100 train_patch=300/360 loss=0.037499
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:12:epoch=1/100 train_patch=360/360 loss=1.847119
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:18:epoch=001/100 loss=0.214208 val_dice=0.000002 val_pr_auc=0.032531 minutes=2.98
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:19:epoch=2/100 train_patch=60/360 loss=0.102701
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:20:epoch=2/100 train_patch=120/360 loss=0.057482
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:21:epoch=2/100 train_patch=180/360 loss=0.037050
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:22:epoch=2/100 train_patch=240/360 loss=0.015849
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:23:epoch=2/100 train_patch=300/360 loss=0.191525
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:24:epoch=2/100 train_patch=360/360 loss=0.040938
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:26:epoch=002/100 loss=0.131131 val_dice=0.000002 val_pr_auc=0.041499 minutes=2.94
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:27:epoch=3/100 train_patch=60/360 loss=0.005686
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:28:epoch=3/100 train_patch=120/360 loss=0.168815
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:29:epoch=3/100 train_patch=180/360 loss=0.034031
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:30:epoch=3/100 train_patch=240/360 loss=0.198657
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:31:epoch=3/100 train_patch=300/360 loss=0.007568
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:32:epoch=3/100 train_patch=360/360 loss=0.196844
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:34:epoch=003/100 loss=0.093528 val_dice=0.000000 val_pr_auc=0.046544 minutes=3.03
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:35:epoch=4/100 train_patch=60/360 loss=0.133939
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:36:epoch=4/100 train_patch=120/360 loss=0.009925
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/run_config.json:3:  "seed": 44,
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/run_config.json:5:  "precision": "float16_autocast",
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/run_config.json:732:  "epochs": 100,
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/run_config.json:734:  "patch_size": 128,
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/run_config.json:737:  "train_sampling": "40 observed random patches per train file each epoch; random axis-0 flip",
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/run_config.json:739:  "normalization": "per-patch z-score over observed voxels; axis reversal",
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/run_config.json:741:  "optimizer": "Adam",
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/run_config.json:742:  "learning_rate": 0.0001,
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/run_config.json:743:  "loss": "ordinary BCE averaged over observed voxels",
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/status.json:3:  "seed": 44,
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/status.json:7:  "precision": "float16_autocast",
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/status.json:11:  "threshold": 0.244140625,
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/validation_selection.json:3:  "threshold": 0.244140625,
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/validation_selection.json:6:    "threshold": 0.244140625,
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/validation_selection.json:9:    "precision": 0.5655692044103381,
runs/R100_fp16_clean_3seeds_20261014_150435/smoke.log:2:QUEUE LAUNCH 2026-10-14T11:04:35.537330+00:00 ["/shared/home/khavarj/projects/fault_detection/.venv_train/bin/python", "-u", "/shared/home/khavarj/projects/fault_detection/scripts/train_r100_fp16_clean.py", "--seed", "42", "--validation-seed", "1042", "--thebe-root", "data/processed/thebe_h5", "--run-dir", "runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42", "--smoke"]
runs/R100_fp16_clean_3seeds_20261014_150435/smoke.log:7:epoch=1/1 train_patch=18/18 loss=0.759043
runs/R100_fp16_clean_3seeds_20261014_150435/smoke.log:12:epoch=001/1 loss=0.779829 val_dice=0.068725 val_pr_auc=0.033207 minutes=0.17
runs/R100_fp16_clean_3seeds_20261014_150435/smoke.log:13:BEST EPOCH: 1; full validation begins
runs/R100_fp16_clean_3seeds_20261014_150435/smoke.log:14:VALIDATION THRESHOLD: 0.427246; test evaluation disabled
runs/R100_fp16_clean_3seeds_20261014_150435/smoke.log:15:R100 VALIDATION-ONLY COMPLETE seed=42 epochs=1 best_epoch=1
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/history.csv:1:epoch,train_loss,train_patches,resampled_no_data_candidates,excluded_training_positive_labels,seconds,val_threshold,val_dice,val_iou,val_precision,val_recall,val_specificity,val_balanced_accuracy,val_accuracy,val_mcc,val_pr_auc_approx,val_roc_auc_approx,val_tp,val_fp,val_fn,val_tn
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/run_config.json:3:  "seed": 42,
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/run_config.json:5:  "precision": "float16_autocast",
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/run_config.json:102:  "epochs": 1,
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/run_config.json:104:  "patch_size": 128,
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/run_config.json:107:  "train_sampling": "2 observed random patches per train file each epoch; random axis-0 flip",
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/run_config.json:109:  "normalization": "per-patch z-score over observed voxels; axis reversal",
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/run_config.json:111:  "optimizer": "Adam",
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/run_config.json:112:  "learning_rate": 0.0001,
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/run_config.json:113:  "loss": "ordinary BCE averaged over observed voxels",
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/status.json:3:  "seed": 42,
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/status.json:7:  "precision": "float16_autocast",
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/status.json:11:  "threshold": 0.42724609375,
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/validation_selection.json:3:  "threshold": 0.42724609375,
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/validation_selection.json:6:    "threshold": 0.42724609375,
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/validation_selection.json:9:    "precision": 0.035650329241587765,
```

### Results and completion

```text
reports/evaluation/p1_cracks_expert_seed42_20261009_134425/expert_per_section.csv:1:section,valid_pixels,certain_fault_pixels,threshold,dice,iou,precision,recall,specificity,balanced_accuracy,accuracy,mcc,pr_auc_approx,roc_auc_approx,tp,fp,fn,tn
reports/evaluation/p1_cracks_expert_seed42_20261009_134425/final_metrics.json:7:    "dice": 0.05755252130783045,
reports/evaluation/p1_cracks_expert_seed42_20261009_134425/final_metrics.json:10:    "iou": 0.029628868702581336,
reports/evaluation/p1_cracks_expert_seed42_20261009_134425/final_metrics.json:13:    "precision": 0.038205351398402906,
reports/evaluation/p1_cracks_expert_seed42_20261009_134425/final_metrics.json:14:    "recall": 0.1165973665973666,
reports/evaluation/p1_cracks_expert_seed42_20261009_134425/final_metrics.json:15:    "roc_auc_approx": 0.5417569783713032,
reports/training/baseline_A_smoke.log:4:/shared/home/khavarj/projects/fault_detection/.venv_train/lib/python3.13/site-packages/torch/autograd/graph.py:824: UserWarning: max_pool3d_with_indices_backward_cuda does not have a deterministic implementation, but you set 'torch.use_deterministic_algorithms(True, warn_only=True)'. You can file an issue at https://github.com/pytorch/pytorch/issues to help us prioritize adding deterministic support for this operation. (Triggered internally at /pytorch/aten/src/ATen/Context.cpp:93.)
reports/training/baseline_A_synthetic_bce_seed42.log:5:/shared/home/khavarj/projects/fault_detection/.venv_train/lib/python3.13/site-packages/torch/autograd/graph.py:824: UserWarning: max_pool3d_with_indices_backward_cuda does not have a deterministic implementation, but you set 'torch.use_deterministic_algorithms(True, warn_only=True)'. You can file an issue at https://github.com/pytorch/pytorch/issues to help us prioritize adding deterministic support for this operation. (Triggered internally at /pytorch/aten/src/ATen/Context.cpp:93.)
reports/training/baseline_A_synthetic_bce_seed42.log:11:epoch=001 loss=0.314965 val_dice=0.000000 val_iou=0.000000 val_pr_auc=0.076771 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:12:epoch=002 loss=0.254361 val_dice=0.000000 val_iou=0.000000 val_pr_auc=0.096252 minutes=0.30
reports/training/baseline_A_synthetic_bce_seed42.log:13:epoch=003 loss=0.238950 val_dice=0.000000 val_iou=0.000000 val_pr_auc=0.182016 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:14:epoch=004 loss=0.200252 val_dice=0.118262 val_iou=0.062847 val_pr_auc=0.390901 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:15:epoch=005 loss=0.168745 val_dice=0.398029 val_iou=0.248462 val_pr_auc=0.481942 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:16:epoch=006 loss=0.153221 val_dice=0.465434 val_iou=0.303300 val_pr_auc=0.539682 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:17:epoch=007 loss=0.141764 val_dice=0.497805 val_iou=0.331385 val_pr_auc=0.586533 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:18:epoch=008 loss=0.135450 val_dice=0.534810 val_iou=0.365011 val_pr_auc=0.613936 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:19:epoch=009 loss=0.128391 val_dice=0.600041 val_iou=0.428614 val_pr_auc=0.641996 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:20:epoch=010 loss=0.122253 val_dice=0.583450 val_iou=0.411881 val_pr_auc=0.643059 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:21:epoch=011 loss=0.118308 val_dice=0.619101 val_iou=0.448332 val_pr_auc=0.686354 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:22:epoch=012 loss=0.112667 val_dice=0.641208 val_iou=0.471895 val_pr_auc=0.700150 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:23:epoch=013 loss=0.109114 val_dice=0.633384 val_iou=0.463469 val_pr_auc=0.715915 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:24:epoch=014 loss=0.106602 val_dice=0.650868 val_iou=0.482435 val_pr_auc=0.711744 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:25:epoch=015 loss=0.102564 val_dice=0.666159 val_iou=0.499429 val_pr_auc=0.731226 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:26:epoch=016 loss=0.099363 val_dice=0.685561 val_iou=0.521562 val_pr_auc=0.750862 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:27:epoch=017 loss=0.097281 val_dice=0.687228 val_iou=0.523494 val_pr_auc=0.757492 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:28:epoch=018 loss=0.093142 val_dice=0.689824 val_iou=0.526513 val_pr_auc=0.765094 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:29:epoch=019 loss=0.093322 val_dice=0.693366 val_iou=0.530651 val_pr_auc=0.769579 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:30:epoch=020 loss=0.089892 val_dice=0.718609 val_iou=0.560804 val_pr_auc=0.786135 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:31:epoch=021 loss=0.088231 val_dice=0.706142 val_iou=0.545765 val_pr_auc=0.776918 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:32:epoch=022 loss=0.084756 val_dice=0.726282 val_iou=0.570206 val_pr_auc=0.795567 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:33:epoch=023 loss=0.083188 val_dice=0.718521 val_iou=0.560696 val_pr_auc=0.792467 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:34:epoch=024 loss=0.082507 val_dice=0.715403 val_iou=0.556909 val_pr_auc=0.802811 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:35:epoch=025 loss=0.080076 val_dice=0.735477 val_iou=0.581624 val_pr_auc=0.807542 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:36:epoch=026 loss=0.080869 val_dice=0.732477 val_iou=0.577881 val_pr_auc=0.802525 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:37:epoch=027 loss=0.077535 val_dice=0.737478 val_iou=0.584131 val_pr_auc=0.808070 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:38:epoch=028 loss=0.076718 val_dice=0.748352 val_iou=0.597894 val_pr_auc=0.820242 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:39:epoch=029 loss=0.075930 val_dice=0.745820 val_iou=0.594668 val_pr_auc=0.816438 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:40:epoch=030 loss=0.073748 val_dice=0.747954 val_iou=0.597386 val_pr_auc=0.821692 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:41:epoch=031 loss=0.074170 val_dice=0.745570 val_iou=0.594349 val_pr_auc=0.824247 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:42:epoch=032 loss=0.072066 val_dice=0.754636 val_iou=0.605956 val_pr_auc=0.832046 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:43:epoch=033 loss=0.070841 val_dice=0.757549 val_iou=0.609721 val_pr_auc=0.832721 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:44:epoch=034 loss=0.069383 val_dice=0.758069 val_iou=0.610395 val_pr_auc=0.834272 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:45:epoch=035 loss=0.068534 val_dice=0.760320 val_iou=0.613319 val_pr_auc=0.839178 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:46:epoch=036 loss=0.068438 val_dice=0.762048 val_iou=0.615572 val_pr_auc=0.835858 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:47:epoch=037 loss=0.066611 val_dice=0.760876 val_iou=0.614044 val_pr_auc=0.835267 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:48:epoch=038 loss=0.065514 val_dice=0.767338 val_iou=0.622505 val_pr_auc=0.840293 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:49:epoch=039 loss=0.065180 val_dice=0.763551 val_iou=0.617536 val_pr_auc=0.838623 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:50:epoch=040 loss=0.064552 val_dice=0.771029 val_iou=0.627378 val_pr_auc=0.841061 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:51:epoch=041 loss=0.064264 val_dice=0.771959 val_iou=0.628610 val_pr_auc=0.843271 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:52:epoch=042 loss=0.063743 val_dice=0.767876 val_iou=0.623213 val_pr_auc=0.846059 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:53:epoch=043 loss=0.061794 val_dice=0.772249 val_iou=0.628995 val_pr_auc=0.848326 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:54:epoch=044 loss=0.060327 val_dice=0.779469 val_iou=0.638632 val_pr_auc=0.852134 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:55:epoch=045 loss=0.059616 val_dice=0.785259 val_iou=0.646442 val_pr_auc=0.855085 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:56:epoch=046 loss=0.060070 val_dice=0.749423 val_iou=0.599261 val_pr_auc=0.829438 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:57:epoch=047 loss=0.059813 val_dice=0.775634 val_iou=0.633499 val_pr_auc=0.849559 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:58:epoch=048 loss=0.058218 val_dice=0.787302 val_iou=0.649215 val_pr_auc=0.859910 minutes=0.31
reports/training/baseline_A_synthetic_bce_seed42.log:59:epoch=049 loss=0.057960 val_dice=0.790558 val_iou=0.653656 val_pr_auc=0.861377 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:5:/shared/home/khavarj/projects/fault_detection/.venv_train/lib/python3.13/site-packages/torch/autograd/graph.py:824: UserWarning: max_pool3d_with_indices_backward_cuda does not have a deterministic implementation, but you set 'torch.use_deterministic_algorithms(True, warn_only=True)'. You can file an issue at https://github.com/pytorch/pytorch/issues to help us prioritize adding deterministic support for this operation. (Triggered internally at /pytorch/aten/src/ATen/Context.cpp:93.)
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:11:epoch=001 loss=1.044174 val_dice=0.220347 val_iou=0.123815 val_pr_auc=0.148267 minutes=0.32
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:12:epoch=002 loss=0.861660 val_dice=0.330021 val_iou=0.197620 val_pr_auc=0.352460 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:13:epoch=003 loss=0.738569 val_dice=0.395203 val_iou=0.246264 val_pr_auc=0.445970 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:14:epoch=004 loss=0.669487 val_dice=0.445811 val_iou=0.286844 val_pr_auc=0.506100 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:15:epoch=005 loss=0.623482 val_dice=0.465448 val_iou=0.303312 val_pr_auc=0.544250 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:16:epoch=006 loss=0.581583 val_dice=0.524423 val_iou=0.355402 val_pr_auc=0.591176 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:17:epoch=007 loss=0.542672 val_dice=0.502238 val_iou=0.335326 val_pr_auc=0.626267 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:18:epoch=008 loss=0.501275 val_dice=0.549318 val_iou=0.378662 val_pr_auc=0.664116 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:19:epoch=009 loss=0.463011 val_dice=0.595464 val_iou=0.423958 val_pr_auc=0.699814 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:20:epoch=010 loss=0.438031 val_dice=0.629139 val_iou=0.458937 val_pr_auc=0.719178 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:21:epoch=011 loss=0.414671 val_dice=0.645080 val_iou=0.476102 val_pr_auc=0.733999 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:22:epoch=012 loss=0.398844 val_dice=0.607199 val_iou=0.435955 val_pr_auc=0.718977 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:23:epoch=013 loss=0.377859 val_dice=0.631336 val_iou=0.461280 val_pr_auc=0.757730 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:24:epoch=014 loss=0.364058 val_dice=0.675847 val_iou=0.510400 val_pr_auc=0.768168 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:25:epoch=015 loss=0.352412 val_dice=0.654198 val_iou=0.486103 val_pr_auc=0.759199 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:26:epoch=016 loss=0.342353 val_dice=0.688899 val_iou=0.525436 val_pr_auc=0.774911 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:27:epoch=017 loss=0.335509 val_dice=0.678364 val_iou=0.513276 val_pr_auc=0.782113 minutes=0.32
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:28:epoch=018 loss=0.322418 val_dice=0.682413 val_iou=0.517926 val_pr_auc=0.791560 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:29:epoch=019 loss=0.317725 val_dice=0.684473 val_iou=0.520303 val_pr_auc=0.783781 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:30:epoch=020 loss=0.312603 val_dice=0.699316 val_iou=0.537653 val_pr_auc=0.800032 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:31:epoch=021 loss=0.304364 val_dice=0.666135 val_iou=0.499402 val_pr_auc=0.798243 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:32:epoch=022 loss=0.296087 val_dice=0.683697 val_iou=0.519407 val_pr_auc=0.792827 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:33:epoch=023 loss=0.289767 val_dice=0.680265 val_iou=0.515455 val_pr_auc=0.790324 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:34:epoch=024 loss=0.283622 val_dice=0.724217 val_iou=0.567665 val_pr_auc=0.819983 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:35:epoch=025 loss=0.276947 val_dice=0.714994 val_iou=0.556413 val_pr_auc=0.817862 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:36:epoch=026 loss=0.276903 val_dice=0.717139 val_iou=0.559015 val_pr_auc=0.820812 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:37:epoch=027 loss=0.265155 val_dice=0.725327 val_iou=0.569030 val_pr_auc=0.814139 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:38:epoch=028 loss=0.265455 val_dice=0.708698 val_iou=0.548824 val_pr_auc=0.816097 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:39:epoch=029 loss=0.260097 val_dice=0.722187 val_iou=0.565174 val_pr_auc=0.826339 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:40:epoch=030 loss=0.253136 val_dice=0.708558 val_iou=0.548656 val_pr_auc=0.821485 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:41:epoch=031 loss=0.246760 val_dice=0.742100 val_iou=0.589952 val_pr_auc=0.830931 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:42:epoch=032 loss=0.245331 val_dice=0.718020 val_iou=0.560087 val_pr_auc=0.831030 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:43:epoch=033 loss=0.239755 val_dice=0.715431 val_iou=0.556942 val_pr_auc=0.831187 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:44:epoch=034 loss=0.237105 val_dice=0.742207 val_iou=0.590087 val_pr_auc=0.832874 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:45:epoch=035 loss=0.235641 val_dice=0.717694 val_iou=0.559690 val_pr_auc=0.823459 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:46:epoch=036 loss=0.228823 val_dice=0.731766 val_iou=0.576995 val_pr_auc=0.839220 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:47:epoch=037 loss=0.227346 val_dice=0.743963 val_iou=0.592310 val_pr_auc=0.834489 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:48:epoch=038 loss=0.226099 val_dice=0.749641 val_iou=0.599541 val_pr_auc=0.836799 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:49:epoch=039 loss=0.221457 val_dice=0.743303 val_iou=0.591474 val_pr_auc=0.845124 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:50:epoch=040 loss=0.218223 val_dice=0.723296 val_iou=0.566534 val_pr_auc=0.840595 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:51:epoch=041 loss=0.219299 val_dice=0.749194 val_iou=0.598969 val_pr_auc=0.842864 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:52:epoch=042 loss=0.217124 val_dice=0.745649 val_iou=0.594450 val_pr_auc=0.841899 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:53:epoch=043 loss=0.211047 val_dice=0.738224 val_iou=0.585067 val_pr_auc=0.837245 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:54:epoch=044 loss=0.210547 val_dice=0.742338 val_iou=0.590252 val_pr_auc=0.845773 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:55:epoch=045 loss=0.205635 val_dice=0.736547 val_iou=0.582963 val_pr_auc=0.847457 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:56:epoch=046 loss=0.208107 val_dice=0.757053 val_iou=0.609079 val_pr_auc=0.851818 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:57:epoch=047 loss=0.204230 val_dice=0.767097 val_iou=0.622187 val_pr_auc=0.856076 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:58:epoch=048 loss=0.198154 val_dice=0.756199 val_iou=0.607974 val_pr_auc=0.851964 minutes=0.31
reports/training/loss_ablation_L1_weighted_bce_dice_seed42.log:59:epoch=049 loss=0.203914 val_dice=0.752893 val_iou=0.603711 val_pr_auc=0.846729 minutes=0.31
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:7:EPOCH 001 train_loss=0.465645 val_loss=0.485600 val_dice=0.000000 val_precision=0.000000 val_recall=0.000000 best=0.000000 elapsed_min=8.5
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:12:EPOCH 002 train_loss=0.467679 val_loss=0.482254 val_dice=0.000000 val_precision=0.000000 val_recall=0.000000 best=0.000000 elapsed_min=17.0
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:17:EPOCH 003 train_loss=0.454671 val_loss=0.483168 val_dice=0.000000 val_precision=0.000000 val_recall=0.000000 best=0.000000 elapsed_min=25.5
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:22:EPOCH 004 train_loss=0.460464 val_loss=0.481467 val_dice=0.000000 val_precision=0.000000 val_recall=0.000000 best=0.000000 elapsed_min=34.0
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:27:EPOCH 005 train_loss=0.467914 val_loss=0.481631 val_dice=0.000000 val_precision=0.000000 val_recall=0.000000 best=0.000000 elapsed_min=42.5
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:32:EPOCH 006 train_loss=0.461141 val_loss=0.484556 val_dice=0.000000 val_precision=0.000000 val_recall=0.000000 best=0.000000 elapsed_min=51.0
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:37:EPOCH 007 train_loss=0.446475 val_loss=0.481680 val_dice=0.047903 val_precision=0.161964 val_recall=0.028108 best=0.047903 elapsed_min=59.5
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:42:EPOCH 008 train_loss=0.459167 val_loss=0.479956 val_dice=0.000000 val_precision=0.000000 val_recall=0.000000 best=0.047903 elapsed_min=67.9
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:47:EPOCH 009 train_loss=0.451511 val_loss=0.476000 val_dice=0.149590 val_precision=0.106510 val_recall=0.251190 best=0.149590 elapsed_min=76.4
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:52:EPOCH 010 train_loss=0.457132 val_loss=0.476811 val_dice=0.099883 val_precision=0.186243 val_recall=0.068240 best=0.149590 elapsed_min=84.9
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:57:EPOCH 011 train_loss=0.459216 val_loss=0.476008 val_dice=0.016839 val_precision=0.326531 val_recall=0.008643 best=0.149590 elapsed_min=93.4
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:62:EPOCH 012 train_loss=0.434350 val_loss=0.475353 val_dice=0.180964 val_precision=0.120576 val_recall=0.362529 best=0.180964 elapsed_min=101.9
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:67:EPOCH 013 train_loss=0.450595 val_loss=0.472315 val_dice=0.150950 val_precision=0.159644 val_recall=0.143153 best=0.180964 elapsed_min=110.4
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:72:EPOCH 014 train_loss=0.444658 val_loss=0.470842 val_dice=0.184008 val_precision=0.189435 val_recall=0.178884 best=0.184008 elapsed_min=118.9
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:77:EPOCH 015 train_loss=0.455812 val_loss=0.472264 val_dice=0.151737 val_precision=0.347372 val_recall=0.097069 best=0.184008 elapsed_min=127.4
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:82:EPOCH 016 train_loss=0.439112 val_loss=0.474909 val_dice=0.090741 val_precision=0.263758 val_recall=0.054796 best=0.184008 elapsed_min=135.9
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:87:EPOCH 017 train_loss=0.455355 val_loss=0.472741 val_dice=0.075697 val_precision=0.446105 val_recall=0.041357 best=0.184008 elapsed_min=144.4
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:92:EPOCH 018 train_loss=0.442842 val_loss=0.471527 val_dice=0.238118 val_precision=0.212533 val_recall=0.270706 best=0.238118 elapsed_min=152.9
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:97:EPOCH 019 train_loss=0.441880 val_loss=0.470957 val_dice=0.212381 val_precision=0.284035 val_recall=0.169596 best=0.238118 elapsed_min=161.3
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:102:EPOCH 020 train_loss=0.442190 val_loss=0.465484 val_dice=0.241313 val_precision=0.179586 val_recall=0.367695 best=0.241313 elapsed_min=169.8
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:107:EPOCH 021 train_loss=0.435344 val_loss=0.475311 val_dice=0.158431 val_precision=0.103035 val_recall=0.342663 best=0.241313 elapsed_min=178.3
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:112:EPOCH 022 train_loss=0.442537 val_loss=0.468002 val_dice=0.194564 val_precision=0.130548 val_recall=0.381770 best=0.241313 elapsed_min=186.8
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:117:EPOCH 023 train_loss=0.449759 val_loss=0.464639 val_dice=0.211203 val_precision=0.228455 val_recall=0.196374 best=0.241313 elapsed_min=195.3
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:122:EPOCH 024 train_loss=0.438226 val_loss=0.470474 val_dice=0.206551 val_precision=0.144007 val_recall=0.365130 best=0.241313 elapsed_min=203.7
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:127:EPOCH 025 train_loss=0.450425 val_loss=0.471324 val_dice=0.193218 val_precision=0.122883 val_recall=0.451846 best=0.241313 elapsed_min=212.2
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:132:EPOCH 026 train_loss=0.463187 val_loss=0.463039 val_dice=0.181876 val_precision=0.325241 val_recall=0.126233 best=0.241313 elapsed_min=220.7
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:137:EPOCH 027 train_loss=0.449494 val_loss=0.458801 val_dice=0.275165 val_precision=0.242287 val_recall=0.318366 best=0.275165 elapsed_min=229.2
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:142:EPOCH 028 train_loss=0.451639 val_loss=0.459566 val_dice=0.261107 val_precision=0.231727 val_recall=0.299020 best=0.275165 elapsed_min=237.7
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:147:EPOCH 029 train_loss=0.439577 val_loss=0.461916 val_dice=0.225784 val_precision=0.160429 val_recall=0.380989 best=0.275165 elapsed_min=246.1
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:152:EPOCH 030 train_loss=0.440820 val_loss=0.463329 val_dice=0.220092 val_precision=0.153135 val_recall=0.391092 best=0.275165 elapsed_min=254.6
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:157:EPOCH 031 train_loss=0.433343 val_loss=0.464132 val_dice=0.186347 val_precision=0.178289 val_recall=0.195169 best=0.275165 elapsed_min=263.1
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:162:EPOCH 032 train_loss=0.434500 val_loss=0.470934 val_dice=0.105899 val_precision=0.194278 val_recall=0.072787 best=0.275165 elapsed_min=271.5
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:167:EPOCH 033 train_loss=0.433713 val_loss=0.463354 val_dice=0.214576 val_precision=0.149040 val_recall=0.382985 best=0.275165 elapsed_min=280.0
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:172:EPOCH 034 train_loss=0.441082 val_loss=0.460800 val_dice=0.230288 val_precision=0.169466 val_recall=0.359208 best=0.275165 elapsed_min=288.5
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:177:EPOCH 035 train_loss=0.438050 val_loss=0.461329 val_dice=0.255506 val_precision=0.181839 val_recall=0.429514 best=0.275165 elapsed_min=297.0
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:182:EPOCH 036 train_loss=0.420644 val_loss=0.466383 val_dice=0.239369 val_precision=0.155263 val_recall=0.522302 best=0.275165 elapsed_min=305.5
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:187:EPOCH 037 train_loss=0.420247 val_loss=0.465001 val_dice=0.229943 val_precision=0.149787 val_recall=0.494643 best=0.275165 elapsed_min=313.9
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:192:EPOCH 038 train_loss=0.442221 val_loss=0.454498 val_dice=0.167754 val_precision=0.184183 val_recall=0.154016 best=0.275165 elapsed_min=322.4
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:197:EPOCH 039 train_loss=0.443751 val_loss=0.450430 val_dice=0.249975 val_precision=0.183709 val_recall=0.391022 best=0.275165 elapsed_min=330.9
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:202:EPOCH 040 train_loss=0.430550 val_loss=0.452433 val_dice=0.271401 val_precision=0.283026 val_recall=0.260693 best=0.275165 elapsed_min=339.3
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:207:EPOCH 041 train_loss=0.443002 val_loss=0.453387 val_dice=0.226092 val_precision=0.202020 val_recall=0.256677 best=0.275165 elapsed_min=347.8
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:212:EPOCH 042 train_loss=0.437746 val_loss=0.446105 val_dice=0.291305 val_precision=0.251279 val_recall=0.346499 best=0.291305 elapsed_min=356.5
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:217:EPOCH 043 train_loss=0.427448 val_loss=0.451607 val_dice=0.217372 val_precision=0.142659 val_recall=0.456392 best=0.291305 elapsed_min=365.0
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:222:EPOCH 044 train_loss=0.421100 val_loss=0.439496 val_dice=0.308680 val_precision=0.245374 val_recall=0.416010 best=0.308680 elapsed_min=376.3
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:227:EPOCH 045 train_loss=0.435031 val_loss=0.462024 val_dice=0.243413 val_precision=0.164914 val_recall=0.464529 best=0.308680 elapsed_min=389.1
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:232:EPOCH 046 train_loss=0.421245 val_loss=0.459163 val_dice=0.252154 val_precision=0.167321 val_recall=0.511478 best=0.308680 elapsed_min=398.9
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:237:EPOCH 047 train_loss=0.410241 val_loss=0.454737 val_dice=0.276184 val_precision=0.205788 val_recall=0.419786 best=0.308680 elapsed_min=407.4
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:242:EPOCH 048 train_loss=0.427201 val_loss=0.450336 val_dice=0.269914 val_precision=0.194638 val_recall=0.440137 best=0.308680 elapsed_min=415.9
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:247:EPOCH 049 train_loss=0.442781 val_loss=0.451658 val_dice=0.266500 val_precision=0.257195 val_recall=0.276503 best=0.308680 elapsed_min=424.4
reports/training/paper_attention3d_thebe_supervised_seed42_bf16_clean.log:252:EPOCH 050 train_loss=0.419376 val_loss=0.457823 val_dice=0.217707 val_precision=0.135386 val_recall=0.555452 best=0.308680 elapsed_min=432.8
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:2:RESUME epoch=50 best_val_dice=0.367370
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:9:EPOCH 050 train_loss=0.416314 val_loss=0.453715 val_dice=0.286637 val_precision=0.180658 val_recall=0.693418 best=0.367370 elapsed_min=8.3
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:14:EPOCH 051 train_loss=0.453673 val_loss=0.453172 val_dice=0.262730 val_precision=0.211600 val_recall=0.346444 best=0.367370 elapsed_min=16.5
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:19:EPOCH 052 train_loss=0.409309 val_loss=0.442612 val_dice=0.376027 val_precision=0.282215 val_recall=0.563264 best=0.376027 elapsed_min=24.7
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:24:EPOCH 053 train_loss=0.439335 val_loss=0.443985 val_dice=0.380571 val_precision=0.424110 val_recall=0.345139 best=0.380571 elapsed_min=32.9
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:29:EPOCH 054 train_loss=0.447276 val_loss=0.445041 val_dice=0.425384 val_precision=0.370854 val_recall=0.498715 best=0.425384 elapsed_min=41.1
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:34:EPOCH 055 train_loss=0.427699 val_loss=0.451420 val_dice=0.350257 val_precision=0.260424 val_recall=0.534700 best=0.425384 elapsed_min=49.3
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:39:EPOCH 056 train_loss=0.426692 val_loss=0.475709 val_dice=0.190790 val_precision=0.108650 val_recall=0.781920 best=0.425384 elapsed_min=57.5
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:44:EPOCH 057 train_loss=0.457442 val_loss=0.456812 val_dice=0.308432 val_precision=0.303325 val_recall=0.313714 best=0.425384 elapsed_min=65.8
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:49:EPOCH 058 train_loss=0.429706 val_loss=0.442806 val_dice=0.347959 val_precision=0.245207 val_recall=0.598945 best=0.425384 elapsed_min=74.0
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:54:EPOCH 059 train_loss=0.429686 val_loss=0.434063 val_dice=0.409925 val_precision=0.329511 val_recall=0.542258 best=0.425384 elapsed_min=82.2
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:59:EPOCH 060 train_loss=0.411757 val_loss=0.438704 val_dice=0.416119 val_precision=0.316983 val_recall=0.605482 best=0.425384 elapsed_min=90.4
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:64:EPOCH 061 train_loss=0.429466 val_loss=0.449119 val_dice=0.349713 val_precision=0.268617 val_recall=0.500950 best=0.425384 elapsed_min=98.6
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:69:EPOCH 062 train_loss=0.441227 val_loss=0.429128 val_dice=0.423200 val_precision=0.365928 val_recall=0.501726 best=0.425384 elapsed_min=106.8
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:74:EPOCH 063 train_loss=0.426974 val_loss=0.442482 val_dice=0.365410 val_precision=0.271615 val_recall=0.558152 best=0.425384 elapsed_min=115.0
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:79:EPOCH 064 train_loss=0.409294 val_loss=0.429752 val_dice=0.489137 val_precision=0.454637 val_recall=0.529304 best=0.489137 elapsed_min=123.2
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:84:EPOCH 065 train_loss=0.429007 val_loss=0.425511 val_dice=0.425216 val_precision=0.387947 val_recall=0.470406 best=0.489137 elapsed_min=131.4
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:89:EPOCH 066 train_loss=0.427213 val_loss=0.427513 val_dice=0.375063 val_precision=0.261715 val_recall=0.661603 best=0.489137 elapsed_min=139.6
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:94:EPOCH 067 train_loss=0.428950 val_loss=0.422227 val_dice=0.282580 val_precision=0.173813 val_recall=0.755102 best=0.489137 elapsed_min=147.8
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:99:EPOCH 068 train_loss=0.444036 val_loss=0.415415 val_dice=0.481035 val_precision=0.504100 val_recall=0.459988 best=0.489137 elapsed_min=156.0
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:104:EPOCH 069 train_loss=0.395316 val_loss=0.410463 val_dice=0.443858 val_precision=0.354308 val_recall=0.593983 best=0.489137 elapsed_min=164.2
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:109:EPOCH 070 train_loss=0.408099 val_loss=0.431831 val_dice=0.539004 val_precision=0.548685 val_recall=0.529659 best=0.539004 elapsed_min=172.4
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:114:EPOCH 071 train_loss=0.413183 val_loss=0.419119 val_dice=0.392210 val_precision=0.275673 val_recall=0.679434 best=0.539004 elapsed_min=180.7
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:119:EPOCH 072 train_loss=0.443808 val_loss=0.438151 val_dice=0.445767 val_precision=0.398119 val_recall=0.506372 best=0.539004 elapsed_min=188.8
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:124:EPOCH 073 train_loss=0.401304 val_loss=0.435013 val_dice=0.434314 val_precision=0.332644 val_recall=0.625493 best=0.539004 elapsed_min=197.0
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:129:EPOCH 074 train_loss=0.412175 val_loss=nan val_dice=0.429887 val_precision=0.315779 val_recall=0.673122 best=0.539004 elapsed_min=205.2
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:134:EPOCH 075 train_loss=nan val_loss=nan val_dice=0.267436 val_precision=0.199014 val_recall=0.407552 best=0.539004 elapsed_min=213.2
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:139:EPOCH 076 train_loss=nan val_loss=nan val_dice=0.267436 val_precision=0.199014 val_recall=0.407552 best=0.539004 elapsed_min=221.2
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:144:EPOCH 077 train_loss=nan val_loss=nan val_dice=0.257658 val_precision=0.186943 val_recall=0.414424 best=0.539004 elapsed_min=229.1
reports/training/r100_fp16_3seed_queue_20261014_150435.log:4:PASS seed=42 validation_dice=0.544072
reports/training/r100_fp16_3seed_queue_20261014_150435.log:6:PASS seed=43 validation_dice=0.569856
reports/training/r100_fp16_3seed_queue_20261014_150435.log:8:PASS seed=44 validation_dice=0.572980
reports/training/r100_fp16_3seed_queue_20261014_150435.log:9:THREE SEEDS COMPLETE validation Dice mean=0.562302 sample_SD=0.015865; no test evaluation
reports/training/R100_thebe_seed42_20261005_102737.log:5:/shared/home/khavarj/projects/fault_detection/.venv_train/lib/python3.13/site-packages/torch/autograd/graph.py:824: UserWarning: max_pool3d_with_indices_backward_cuda does not have a deterministic implementation, but you set 'torch.use_deterministic_algorithms(True, warn_only=True)'. You can file an issue at https://github.com/pytorch/pytorch/issues to help us prioritize adding deterministic support for this operation. (Triggered internally at /pytorch/aten/src/ATen/Context.cpp:93.)
reports/training/R100_thebe_seed42_20261005_102737.log:12:epoch=001/100 loss=0.211608 val_dice=0.000006 val_pr_auc=0.034823 minutes=3.26
reports/training/R100_thebe_seed42_20261005_102737.log:14:epoch=002/100 loss=0.131591 val_dice=0.000001 val_pr_auc=0.039528 minutes=3.33
reports/training/R100_thebe_seed42_20261005_102737.log:16:epoch=003/100 loss=0.105220 val_dice=0.000001 val_pr_auc=0.043710 minutes=3.23
reports/training/R100_thebe_seed42_20261005_102737.log:18:epoch=004/100 loss=0.101674 val_dice=0.000000 val_pr_auc=0.043505 minutes=3.32
reports/training/R100_thebe_seed42_20261005_102737.log:20:epoch=005/100 loss=0.113378 val_dice=0.000000 val_pr_auc=0.038386 minutes=3.04
reports/training/R100_thebe_seed42_20261005_102737.log:22:epoch=006/100 loss=0.102869 val_dice=0.000000 val_pr_auc=0.047210 minutes=3.22
reports/training/R100_thebe_seed42_20261005_102737.log:24:epoch=007/100 loss=0.106725 val_dice=0.000000 val_pr_auc=0.049760 minutes=3.20
reports/training/R100_thebe_seed42_20261005_102737.log:26:epoch=008/100 loss=0.096674 val_dice=0.000000 val_pr_auc=0.048672 minutes=3.13
reports/training/R100_thebe_seed42_20261005_102737.log:28:epoch=009/100 loss=0.099541 val_dice=0.000000 val_pr_auc=0.043619 minutes=3.24
reports/training/R100_thebe_seed42_20261005_102737.log:30:epoch=010/100 loss=0.107934 val_dice=0.000000 val_pr_auc=0.055916 minutes=3.05
reports/training/R100_thebe_seed42_20261005_102737.log:32:epoch=011/100 loss=0.099936 val_dice=0.000000 val_pr_auc=0.061880 minutes=3.10
reports/training/R100_thebe_seed42_20261005_102737.log:34:epoch=012/100 loss=0.102164 val_dice=0.000000 val_pr_auc=0.049965 minutes=3.15
reports/training/R100_thebe_seed42_20261005_102737.log:36:epoch=013/100 loss=0.109964 val_dice=0.000000 val_pr_auc=0.061470 minutes=3.00
reports/training/R100_thebe_seed42_20261005_102737.log:38:epoch=014/100 loss=0.096900 val_dice=0.000000 val_pr_auc=0.089677 minutes=3.07
reports/training/R100_thebe_seed42_20261005_102737.log:40:epoch=015/100 loss=0.089464 val_dice=0.000000 val_pr_auc=0.117684 minutes=3.21
reports/training/R100_thebe_seed42_20261005_102737.log:42:epoch=016/100 loss=0.088687 val_dice=0.000000 val_pr_auc=0.107323 minutes=3.15
reports/training/R100_thebe_seed42_20261005_102737.log:44:epoch=017/100 loss=0.083734 val_dice=0.000000 val_pr_auc=0.135083 minutes=3.13
reports/training/R100_thebe_seed42_20261005_102737.log:46:epoch=018/100 loss=0.087998 val_dice=0.000000 val_pr_auc=0.171241 minutes=3.32
reports/training/R100_thebe_seed42_20261005_102737.log:48:epoch=019/100 loss=0.090926 val_dice=0.000000 val_pr_auc=0.184733 minutes=3.11
reports/training/R100_thebe_seed42_20261005_102737.log:50:epoch=020/100 loss=0.077623 val_dice=0.000000 val_pr_auc=0.207758 minutes=3.15
reports/training/R100_thebe_seed42_20261005_102737.log:52:epoch=021/100 loss=0.073180 val_dice=0.000013 val_pr_auc=0.213077 minutes=3.13
reports/training/R100_thebe_seed42_20261005_102737.log:54:epoch=022/100 loss=0.077549 val_dice=0.000690 val_pr_auc=0.212709 minutes=3.08
reports/training/R100_thebe_seed42_20261005_102737.log:56:epoch=023/100 loss=0.080129 val_dice=0.001580 val_pr_auc=0.250377 minutes=3.05
reports/training/R100_thebe_seed42_resume_20261005_131346.log:6:/shared/home/khavarj/projects/fault_detection/.venv_train/lib/python3.13/site-packages/torch/autograd/graph.py:824: UserWarning: max_pool3d_with_indices_backward_cuda does not have a deterministic implementation, but you set 'torch.use_deterministic_algorithms(True, warn_only=True)'. You can file an issue at https://github.com/pytorch/pytorch/issues to help us prioritize adding deterministic support for this operation. (Triggered internally at /pytorch/aten/src/ATen/Context.cpp:93.)
reports/training/R100_thebe_seed42_resume_20261005_131346.log:13:epoch=024/100 loss=0.078920 val_dice=0.001420 val_pr_auc=0.236420 minutes=3.32
reports/training/R100_thebe_seed42_resume_20261005_131346.log:15:epoch=025/100 loss=0.065565 val_dice=0.002473 val_pr_auc=0.260316 minutes=3.20
reports/training/R100_thebe_seed42_resume_20261005_131346.log:17:epoch=026/100 loss=0.068080 val_dice=0.003456 val_pr_auc=0.263557 minutes=3.25
reports/training/R100_thebe_seed42_resume_20261005_131346.log:19:epoch=027/100 loss=0.080750 val_dice=0.011536 val_pr_auc=0.259436 minutes=3.12
reports/training/R100_thebe_seed42_resume_20261005_131346.log:21:epoch=028/100 loss=0.075161 val_dice=0.018024 val_pr_auc=0.297481 minutes=3.05
reports/training/R100_thebe_seed42_resume_20261005_131346.log:23:epoch=029/100 loss=0.084217 val_dice=0.048370 val_pr_auc=0.295427 minutes=3.27
reports/training/R100_thebe_seed42_resume_20261005_131346.log:25:epoch=030/100 loss=0.069108 val_dice=0.027934 val_pr_auc=0.322924 minutes=3.16
reports/training/R100_thebe_seed42_resume_20261005_131346.log:27:epoch=031/100 loss=0.078519 val_dice=0.077669 val_pr_auc=0.336544 minutes=3.02
reports/training/R100_thebe_seed42_resume_20261005_131346.log:29:epoch=032/100 loss=0.062892 val_dice=0.304055 val_pr_auc=0.336719 minutes=3.36
reports/training/R100_thebe_seed42_resume_20261005_131346.log:31:epoch=033/100 loss=0.072173 val_dice=0.149602 val_pr_auc=0.348334 minutes=3.39
reports/training/R100_thebe_seed42_resume_20261005_131346.log:33:epoch=034/100 loss=0.070201 val_dice=0.174907 val_pr_auc=0.342185 minutes=3.24
reports/training/R100_thebe_seed42_resume_20261005_131346.log:35:epoch=035/100 loss=0.073527 val_dice=0.148241 val_pr_auc=0.369592 minutes=3.27
reports/training/R100_thebe_seed42_resume_20261005_131346.log:37:epoch=036/100 loss=0.069229 val_dice=0.193048 val_pr_auc=0.379670 minutes=3.25
reports/training/R100_thebe_seed42_resume_20261005_131346.log:39:epoch=037/100 loss=0.063905 val_dice=0.006665 val_pr_auc=0.330679 minutes=3.15
reports/training/R100_thebe_seed42_resume_20261005_131346.log:41:epoch=038/100 loss=0.080337 val_dice=0.244056 val_pr_auc=0.374059 minutes=3.23
reports/training/R100_thebe_seed42_resume_20261005_131346.log:43:epoch=039/100 loss=0.066486 val_dice=0.255052 val_pr_auc=0.404267 minutes=3.12
reports/training/R100_thebe_seed42_resume_20261005_131346.log:45:epoch=040/100 loss=0.065938 val_dice=0.210433 val_pr_auc=0.382206 minutes=3.17
reports/training/R100_thebe_seed42_resume_20261005_131346.log:47:epoch=041/100 loss=0.062026 val_dice=0.407483 val_pr_auc=0.373383 minutes=3.09
reports/training/R100_thebe_seed42_resume_20261005_131346.log:49:epoch=042/100 loss=0.075279 val_dice=0.123915 val_pr_auc=0.388560 minutes=3.06
reports/training/R100_thebe_seed42_resume_20261005_131346.log:51:epoch=043/100 loss=0.065071 val_dice=0.270480 val_pr_auc=0.393687 minutes=3.09
reports/training/R100_thebe_seed42_resume_20261005_131346.log:53:epoch=044/100 loss=0.064441 val_dice=0.172999 val_pr_auc=0.384315 minutes=3.11
reports/training/R100_thebe_seed42_resume_20261005_131346.log:55:epoch=045/100 loss=0.063953 val_dice=0.286662 val_pr_auc=0.441626 minutes=3.20
reports/training/R100_thebe_seed42_resume_20261005_131346.log:57:epoch=046/100 loss=0.059598 val_dice=0.413131 val_pr_auc=0.401415 minutes=3.25
reports/training/R100_thebe_seed42_resume_20261005_131346.log:59:epoch=047/100 loss=0.062477 val_dice=0.245688 val_pr_auc=0.443531 minutes=3.15
reports/training/R100_thebe_seed42_resume_20261005_131346.log:61:epoch=048/100 loss=0.059514 val_dice=0.245539 val_pr_auc=0.437099 minutes=3.14
reports/training/R100_thebe_seed42_resume_20261005_131346.log:63:epoch=049/100 loss=0.061393 val_dice=0.279920 val_pr_auc=0.438496 minutes=3.24
reports/training/R100_thebe_seed42_resume_20261005_131346.log:65:epoch=050/100 loss=0.070041 val_dice=0.288117 val_pr_auc=0.453892 minutes=3.29
reports/training/R100_thebe_seed42_resume_20261005_131346.log:67:epoch=051/100 loss=0.065202 val_dice=0.266200 val_pr_auc=0.460510 minutes=3.37
reports/training/R100_thebe_seed42_resume_20261005_131346.log:69:epoch=052/100 loss=0.066613 val_dice=0.356431 val_pr_auc=0.427422 minutes=3.12
reports/training/R100_thebe_seed42_resume_20261005_131346.log:71:epoch=053/100 loss=0.066192 val_dice=0.342636 val_pr_auc=0.433051 minutes=3.27
reports/training/R100_thebe_seed42_resume_20261005_131346.log:73:epoch=054/100 loss=0.064246 val_dice=0.341244 val_pr_auc=0.459710 minutes=3.38
reports/training/R100_thebe_seed42_resume_20261005_131346.log:75:epoch=055/100 loss=0.054061 val_dice=0.428206 val_pr_auc=0.477125 minutes=3.27
reports/training/R100_thebe_seed42_resume_20261005_131346.log:77:epoch=056/100 loss=0.060517 val_dice=0.356121 val_pr_auc=0.480524 minutes=3.22
reports/training/R100_thebe_seed42_resume_20261005_131346.log:79:epoch=057/100 loss=0.063365 val_dice=0.428462 val_pr_auc=0.440082 minutes=3.14
reports/training/R100_thebe_seed42_resume_20261005_131346.log:81:epoch=058/100 loss=0.050335 val_dice=0.308301 val_pr_auc=0.512327 minutes=3.39
reports/training/R100_thebe_seed42_resume_20261005_131346.log:83:epoch=059/100 loss=0.067371 val_dice=0.472297 val_pr_auc=0.479524 minutes=3.24
reports/training/R100_thebe_seed42_resume_20261005_131346.log:85:epoch=060/100 loss=0.061604 val_dice=0.441440 val_pr_auc=0.516968 minutes=3.25
reports/training/R100_thebe_seed42_resume_20261005_131346.log:87:epoch=061/100 loss=0.062467 val_dice=0.247468 val_pr_auc=0.517348 minutes=3.13
reports/training/R100_thebe_seed42_resume_20261005_131346.log:89:epoch=062/100 loss=0.059376 val_dice=0.262464 val_pr_auc=0.489979 minutes=3.06
reports/training/R100_thebe_seed42_resume_20261005_131346.log:91:epoch=063/100 loss=0.063021 val_dice=0.350626 val_pr_auc=0.518379 minutes=3.16
reports/training/R100_thebe_seed42_resume_20261005_131346.log:93:epoch=064/100 loss=0.059923 val_dice=0.359455 val_pr_auc=0.538676 minutes=3.10
reports/training/R100_thebe_seed42_resume_20261005_131346.log:95:epoch=065/100 loss=0.047842 val_dice=0.269996 val_pr_auc=0.492450 minutes=3.30
reports/training/R100_thebe_seed42_resume_20261005_131346.log:97:epoch=066/100 loss=0.055280 val_dice=0.415410 val_pr_auc=0.508203 minutes=3.15
reports/training/R100_thebe_seed42_resume_20261005_131346.log:99:epoch=067/100 loss=0.061079 val_dice=0.383309 val_pr_auc=0.545594 minutes=3.14
reports/training/R100_thebe_seed42_resume_20261005_131346.log:101:epoch=068/100 loss=0.052238 val_dice=0.502782 val_pr_auc=0.544847 minutes=3.20
reports/training/R100_thebe_seed42_resume_20261005_131346.log:103:epoch=069/100 loss=0.058578 val_dice=0.496378 val_pr_auc=0.556591 minutes=3.28
reports/training/R100_thebe_seed42_resume_20261005_131346.log:105:epoch=070/100 loss=0.053104 val_dice=0.313013 val_pr_auc=0.547534 minutes=3.34
reports/training/R100_thebe_seed42_resume_20261005_131346.log:107:epoch=071/100 loss=0.053821 val_dice=0.393332 val_pr_auc=0.567882 minutes=3.18
reports/training/R100_thebe_seed42_resume_20261005_131346.log:109:epoch=072/100 loss=0.059722 val_dice=0.413933 val_pr_auc=0.571626 minutes=3.33
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:22:        "dice": 0.5440719430427761,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:23:        "iou": 0.373694249824297,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:24:        "precision": 0.5267658204531103,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:25:        "recall": 0.562553828427201,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:31:        "roc_auc_approx": 0.9560342463297409,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:47:        "dice": 0.5698556833270347,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:48:        "iou": 0.39846026494216036,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:49:        "precision": 0.5643889729910121,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:50:        "recall": 0.5754293313318344,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:56:        "roc_auc_approx": 0.9612985077763903,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:72:        "dice": 0.5729798256899185,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:73:        "iou": 0.40152188175400944,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:74:        "precision": 0.5655692044103381,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:75:        "recall": 0.5805872272731943,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:81:        "roc_auc_approx": 0.9589852925995812,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:102:  "validation_dice_mean": 0.5623024840199098,
runs/R100_fp16_clean_3seeds_20261014_150435/queue_status.json:103:  "validation_dice_sample_sd": 0.015865198852050486
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/history.csv:1:epoch,train_loss,train_patches,resampled_no_data_candidates,excluded_training_positive_labels,seconds,val_threshold,val_dice,val_iou,val_precision,val_recall,val_specificity,val_balanced_accuracy,val_accuracy,val_mcc,val_pr_auc_approx,val_roc_auc_approx,val_tp,val_fp,val_fn,val_tn
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:5:/shared/home/khavarj/projects/fault_detection/.venv_train/lib/python3.13/site-packages/torch/autograd/graph.py:824: UserWarning: max_pool3d_with_indices_backward_cuda does not have a deterministic implementation, but you set 'torch.use_deterministic_algorithms(True, warn_only=True)'. You can file an issue at https://github.com/pytorch/pytorch/issues to help us prioritize adding deterministic support for this operation. (Triggered internally at /pytorch/aten/src/ATen/Context.cpp:93.)
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:18:epoch=001/100 loss=0.211608 val_dice=0.000006 val_pr_auc=0.034823 minutes=3.12
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:26:epoch=002/100 loss=0.131591 val_dice=0.000001 val_pr_auc=0.039528 minutes=3.08
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:34:epoch=003/100 loss=0.105220 val_dice=0.000001 val_pr_auc=0.043710 minutes=3.09
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:42:epoch=004/100 loss=0.101674 val_dice=0.000000 val_pr_auc=0.043505 minutes=3.18
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:50:epoch=005/100 loss=0.113378 val_dice=0.000000 val_pr_auc=0.038386 minutes=2.88
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:58:epoch=006/100 loss=0.102869 val_dice=0.000000 val_pr_auc=0.047210 minutes=3.07
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:66:epoch=007/100 loss=0.106725 val_dice=0.000000 val_pr_auc=0.049760 minutes=3.06
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:74:epoch=008/100 loss=0.096674 val_dice=0.000000 val_pr_auc=0.048672 minutes=2.99
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:82:epoch=009/100 loss=0.099541 val_dice=0.000000 val_pr_auc=0.043619 minutes=3.14
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:90:epoch=010/100 loss=0.107934 val_dice=0.000000 val_pr_auc=0.055916 minutes=2.92
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:98:epoch=011/100 loss=0.099936 val_dice=0.000000 val_pr_auc=0.061880 minutes=2.95
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:106:epoch=012/100 loss=0.102164 val_dice=0.000000 val_pr_auc=0.049965 minutes=3.01
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:114:epoch=013/100 loss=0.109964 val_dice=0.000000 val_pr_auc=0.061470 minutes=2.89
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:122:epoch=014/100 loss=0.096900 val_dice=0.000000 val_pr_auc=0.089677 minutes=2.94
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:130:epoch=015/100 loss=0.089464 val_dice=0.000000 val_pr_auc=0.117684 minutes=3.08
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:138:epoch=016/100 loss=0.088687 val_dice=0.000000 val_pr_auc=0.107323 minutes=3.07
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:146:epoch=017/100 loss=0.083734 val_dice=0.000000 val_pr_auc=0.135083 minutes=3.05
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:154:epoch=018/100 loss=0.087998 val_dice=0.000000 val_pr_auc=0.171241 minutes=3.17
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:162:epoch=019/100 loss=0.090926 val_dice=0.000000 val_pr_auc=0.184733 minutes=2.97
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:170:epoch=020/100 loss=0.077623 val_dice=0.000000 val_pr_auc=0.207758 minutes=3.01
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:178:epoch=021/100 loss=0.073180 val_dice=0.000013 val_pr_auc=0.213077 minutes=3.03
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:186:epoch=022/100 loss=0.077549 val_dice=0.000690 val_pr_auc=0.212709 minutes=2.94
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:194:epoch=023/100 loss=0.080129 val_dice=0.001580 val_pr_auc=0.250377 minutes=2.89
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:202:epoch=024/100 loss=0.085101 val_dice=0.007970 val_pr_auc=0.210663 minutes=3.00
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:210:epoch=025/100 loss=0.067014 val_dice=0.002319 val_pr_auc=0.270853 minutes=3.03
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:218:epoch=026/100 loss=0.074720 val_dice=0.008281 val_pr_auc=0.258356 minutes=3.06
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:226:epoch=027/100 loss=0.078038 val_dice=0.002668 val_pr_auc=0.299218 minutes=3.02
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:234:epoch=028/100 loss=0.069081 val_dice=0.016612 val_pr_auc=0.289297 minutes=3.13
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:242:epoch=029/100 loss=0.067600 val_dice=0.025738 val_pr_auc=0.304789 minutes=3.06
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:250:epoch=030/100 loss=0.069910 val_dice=0.025284 val_pr_auc=0.307485 minutes=3.10
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:258:epoch=031/100 loss=0.071929 val_dice=0.005624 val_pr_auc=0.335175 minutes=3.10
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:266:epoch=032/100 loss=0.074831 val_dice=0.014670 val_pr_auc=0.324274 minutes=2.89
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:274:epoch=033/100 loss=0.069609 val_dice=0.119484 val_pr_auc=0.339538 minutes=3.03
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:282:epoch=034/100 loss=0.061320 val_dice=0.095749 val_pr_auc=0.323181 minutes=3.06
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:290:epoch=035/100 loss=0.071427 val_dice=0.106897 val_pr_auc=0.358173 minutes=3.10
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:298:epoch=036/100 loss=0.070403 val_dice=0.117125 val_pr_auc=0.339758 minutes=3.03
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:306:epoch=037/100 loss=0.072179 val_dice=0.206109 val_pr_auc=0.363270 minutes=2.98
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:314:epoch=038/100 loss=0.072133 val_dice=0.230500 val_pr_auc=0.384911 minutes=3.18
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:322:epoch=039/100 loss=0.066432 val_dice=0.149482 val_pr_auc=0.392297 minutes=2.94
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:330:epoch=040/100 loss=0.059668 val_dice=0.100121 val_pr_auc=0.388984 minutes=3.16
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:338:epoch=041/100 loss=0.060640 val_dice=0.237473 val_pr_auc=0.413392 minutes=3.08
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:346:epoch=042/100 loss=0.065647 val_dice=0.136110 val_pr_auc=0.418763 minutes=3.14
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:354:epoch=043/100 loss=0.065825 val_dice=0.211336 val_pr_auc=0.382685 minutes=3.06
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:362:epoch=044/100 loss=0.058033 val_dice=0.226795 val_pr_auc=0.418009 minutes=3.08
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:370:epoch=045/100 loss=0.068560 val_dice=0.331624 val_pr_auc=0.419339 minutes=3.45
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:378:epoch=046/100 loss=0.064055 val_dice=0.310719 val_pr_auc=0.433676 minutes=3.54
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:386:epoch=047/100 loss=0.065738 val_dice=0.201582 val_pr_auc=0.400658 minutes=3.41
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:394:epoch=048/100 loss=0.064558 val_dice=0.331357 val_pr_auc=0.459623 minutes=3.51
runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log:402:epoch=049/100 loss=0.057787 val_dice=0.402787 val_pr_auc=0.448123 minutes=3.57
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/run_config.json:5:  "precision": "float16_autocast",
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/run_config.json:746:  "threshold_selection": "best Dice on complete validation volume with 2048 bins",
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/status.json:7:  "precision": "float16_autocast",
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/status.json:12:  "best_checkpoint": "runs/R100_fp16_clean_3seeds_20261014_150435/seed42/best.pt",
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/validation_selection.json:7:    "dice": 0.5440719430427761,
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/validation_selection.json:8:    "iou": 0.373694249824297,
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/validation_selection.json:9:    "precision": 0.5267658204531103,
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/validation_selection.json:10:    "recall": 0.562553828427201,
runs/R100_fp16_clean_3seeds_20261014_150435/seed42/validation_selection.json:16:    "roc_auc_approx": 0.9560342463297409,
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/history.csv:1:epoch,train_loss,train_patches,resampled_no_data_candidates,excluded_training_positive_labels,seconds,val_threshold,val_dice,val_iou,val_precision,val_recall,val_specificity,val_balanced_accuracy,val_accuracy,val_mcc,val_pr_auc_approx,val_roc_auc_approx,val_tp,val_fp,val_fn,val_tn
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:5:/shared/home/khavarj/projects/fault_detection/.venv_train/lib/python3.13/site-packages/torch/autograd/graph.py:824: UserWarning: max_pool3d_with_indices_backward_cuda does not have a deterministic implementation, but you set 'torch.use_deterministic_algorithms(True, warn_only=True)'. You can file an issue at https://github.com/pytorch/pytorch/issues to help us prioritize adding deterministic support for this operation. (Triggered internally at /pytorch/aten/src/ATen/Context.cpp:93.)
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:18:epoch=001/100 loss=0.207313 val_dice=0.000010 val_pr_auc=0.032889 minutes=3.25
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:26:epoch=002/100 loss=0.134325 val_dice=0.000000 val_pr_auc=0.037506 minutes=3.40
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:34:epoch=003/100 loss=0.113158 val_dice=0.000000 val_pr_auc=0.044267 minutes=3.32
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:42:epoch=004/100 loss=0.106803 val_dice=0.000000 val_pr_auc=0.047515 minutes=3.69
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:50:epoch=005/100 loss=0.112586 val_dice=0.000000 val_pr_auc=0.055564 minutes=3.44
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:58:epoch=006/100 loss=0.086832 val_dice=0.000000 val_pr_auc=0.073312 minutes=3.49
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:66:epoch=007/100 loss=0.096694 val_dice=0.000000 val_pr_auc=0.063642 minutes=3.45
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:74:epoch=008/100 loss=0.099798 val_dice=0.000000 val_pr_auc=0.111352 minutes=3.47
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:82:epoch=009/100 loss=0.086573 val_dice=0.000000 val_pr_auc=0.109360 minutes=3.49
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:90:epoch=010/100 loss=0.085202 val_dice=0.000000 val_pr_auc=0.129471 minutes=3.51
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:98:epoch=011/100 loss=0.082043 val_dice=0.000000 val_pr_auc=0.190129 minutes=3.52
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:106:epoch=012/100 loss=0.087391 val_dice=0.000000 val_pr_auc=0.182149 minutes=3.50
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:114:epoch=013/100 loss=0.086629 val_dice=0.051217 val_pr_auc=0.227169 minutes=3.42
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:122:epoch=014/100 loss=0.075188 val_dice=0.156249 val_pr_auc=0.287682 minutes=3.35
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:130:epoch=015/100 loss=0.069022 val_dice=0.128348 val_pr_auc=0.318932 minutes=3.42
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:138:epoch=016/100 loss=0.068342 val_dice=0.144531 val_pr_auc=0.319825 minutes=3.32
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:146:epoch=017/100 loss=0.076954 val_dice=0.317299 val_pr_auc=0.348228 minutes=3.34
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:154:epoch=018/100 loss=0.066294 val_dice=0.330689 val_pr_auc=0.360967 minutes=3.26
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:162:epoch=019/100 loss=0.078325 val_dice=0.154955 val_pr_auc=0.370729 minutes=3.36
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:170:epoch=020/100 loss=0.073825 val_dice=0.170272 val_pr_auc=0.410673 minutes=3.24
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:178:epoch=021/100 loss=0.074191 val_dice=0.326550 val_pr_auc=0.398516 minutes=3.31
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:186:epoch=022/100 loss=0.066618 val_dice=0.254137 val_pr_auc=0.428462 minutes=3.34
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:194:epoch=023/100 loss=0.069498 val_dice=0.275050 val_pr_auc=0.445187 minutes=3.20
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:202:epoch=024/100 loss=0.059472 val_dice=0.351567 val_pr_auc=0.463566 minutes=3.10
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:210:epoch=025/100 loss=0.061590 val_dice=0.290421 val_pr_auc=0.448529 minutes=3.13
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:218:epoch=026/100 loss=0.063974 val_dice=0.367536 val_pr_auc=0.458521 minutes=3.20
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:226:epoch=027/100 loss=0.066937 val_dice=0.184101 val_pr_auc=0.455209 minutes=3.18
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:234:epoch=028/100 loss=0.061171 val_dice=0.436915 val_pr_auc=0.483792 minutes=3.02
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:242:epoch=029/100 loss=0.054366 val_dice=0.275544 val_pr_auc=0.491174 minutes=3.15
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:250:epoch=030/100 loss=0.061534 val_dice=0.440431 val_pr_auc=0.473313 minutes=3.21
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:258:epoch=031/100 loss=0.058599 val_dice=0.331349 val_pr_auc=0.489746 minutes=3.11
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:266:epoch=032/100 loss=0.058002 val_dice=0.317572 val_pr_auc=0.507873 minutes=3.07
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:274:epoch=033/100 loss=0.064508 val_dice=0.132827 val_pr_auc=0.479362 minutes=3.13
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:282:epoch=034/100 loss=0.075195 val_dice=0.320840 val_pr_auc=0.513074 minutes=3.11
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:290:epoch=035/100 loss=0.061724 val_dice=0.474487 val_pr_auc=0.514265 minutes=3.13
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:298:epoch=036/100 loss=0.065400 val_dice=0.426747 val_pr_auc=0.542522 minutes=2.92
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:306:epoch=037/100 loss=0.056895 val_dice=0.471250 val_pr_auc=0.497020 minutes=2.93
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:314:epoch=038/100 loss=0.056790 val_dice=0.273526 val_pr_auc=0.525836 minutes=3.00
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:322:epoch=039/100 loss=0.060411 val_dice=0.326792 val_pr_auc=0.532453 minutes=3.10
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:330:epoch=040/100 loss=0.054520 val_dice=0.531070 val_pr_auc=0.546094 minutes=2.84
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:338:epoch=041/100 loss=0.061186 val_dice=0.334449 val_pr_auc=0.560378 minutes=2.95
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:346:epoch=042/100 loss=0.050234 val_dice=0.319623 val_pr_auc=0.526732 minutes=3.17
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:354:epoch=043/100 loss=0.053101 val_dice=0.448451 val_pr_auc=0.550102 minutes=2.91
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:362:epoch=044/100 loss=0.055038 val_dice=0.513862 val_pr_auc=0.562986 minutes=2.98
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:370:epoch=045/100 loss=0.055149 val_dice=0.341347 val_pr_auc=0.525956 minutes=2.94
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:378:epoch=046/100 loss=0.055819 val_dice=0.411702 val_pr_auc=0.558411 minutes=3.00
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:386:epoch=047/100 loss=0.056744 val_dice=0.540495 val_pr_auc=0.568879 minutes=2.94
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:394:epoch=048/100 loss=0.057409 val_dice=0.400572 val_pr_auc=0.577831 minutes=3.09
runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log:402:epoch=049/100 loss=0.056376 val_dice=0.510591 val_pr_auc=0.571619 minutes=3.07
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/run_config.json:5:  "precision": "float16_autocast",
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/run_config.json:746:  "threshold_selection": "best Dice on complete validation volume with 2048 bins",
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/status.json:7:  "precision": "float16_autocast",
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/status.json:12:  "best_checkpoint": "runs/R100_fp16_clean_3seeds_20261014_150435/seed43/best.pt",
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/validation_selection.json:7:    "dice": 0.5698556833270347,
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/validation_selection.json:8:    "iou": 0.39846026494216036,
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/validation_selection.json:9:    "precision": 0.5643889729910121,
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/validation_selection.json:10:    "recall": 0.5754293313318344,
runs/R100_fp16_clean_3seeds_20261014_150435/seed43/validation_selection.json:16:    "roc_auc_approx": 0.9612985077763903,
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/best.pt: binary file matches (found "\0" byte around offset 4)
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/history.csv:1:epoch,train_loss,train_patches,resampled_no_data_candidates,excluded_training_positive_labels,seconds,val_threshold,val_dice,val_iou,val_precision,val_recall,val_specificity,val_balanced_accuracy,val_accuracy,val_mcc,val_pr_auc_approx,val_roc_auc_approx,val_tp,val_fp,val_fn,val_tn
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/last.pt: binary file matches (found "\0" byte around offset 4)
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:5:/shared/home/khavarj/projects/fault_detection/.venv_train/lib/python3.13/site-packages/torch/autograd/graph.py:824: UserWarning: max_pool3d_with_indices_backward_cuda does not have a deterministic implementation, but you set 'torch.use_deterministic_algorithms(True, warn_only=True)'. You can file an issue at https://github.com/pytorch/pytorch/issues to help us prioritize adding deterministic support for this operation. (Triggered internally at /pytorch/aten/src/ATen/Context.cpp:93.)
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:18:epoch=001/100 loss=0.214208 val_dice=0.000002 val_pr_auc=0.032531 minutes=2.98
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:26:epoch=002/100 loss=0.131131 val_dice=0.000002 val_pr_auc=0.041499 minutes=2.94
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:34:epoch=003/100 loss=0.093528 val_dice=0.000000 val_pr_auc=0.046544 minutes=3.03
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:42:epoch=004/100 loss=0.094511 val_dice=0.000000 val_pr_auc=0.045681 minutes=3.09
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:50:epoch=005/100 loss=0.103709 val_dice=0.000000 val_pr_auc=0.047491 minutes=3.07
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:58:epoch=006/100 loss=0.102382 val_dice=0.000000 val_pr_auc=0.053118 minutes=3.10
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:66:epoch=007/100 loss=0.096109 val_dice=0.000000 val_pr_auc=0.057679 minutes=3.11
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:74:epoch=008/100 loss=0.094502 val_dice=0.000000 val_pr_auc=0.055288 minutes=3.11
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:82:epoch=009/100 loss=0.099929 val_dice=0.000000 val_pr_auc=0.056435 minutes=3.03
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:90:epoch=010/100 loss=0.091132 val_dice=0.000000 val_pr_auc=0.072109 minutes=2.94
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:98:epoch=011/100 loss=0.091550 val_dice=0.000000 val_pr_auc=0.076607 minutes=3.09
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:106:epoch=012/100 loss=0.082483 val_dice=0.000000 val_pr_auc=0.089395 minutes=3.11
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:114:epoch=013/100 loss=0.095675 val_dice=0.000000 val_pr_auc=0.099517 minutes=3.09
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:122:epoch=014/100 loss=0.087235 val_dice=0.000000 val_pr_auc=0.128630 minutes=3.04
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:130:epoch=015/100 loss=0.092547 val_dice=0.000000 val_pr_auc=0.118855 minutes=2.92
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:138:epoch=016/100 loss=0.094852 val_dice=0.000000 val_pr_auc=0.121884 minutes=3.03
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:146:epoch=017/100 loss=0.087888 val_dice=0.000000 val_pr_auc=0.172786 minutes=3.01
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:154:epoch=018/100 loss=0.083555 val_dice=0.000000 val_pr_auc=0.163500 minutes=3.08
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:162:epoch=019/100 loss=0.089364 val_dice=0.000000 val_pr_auc=0.127726 minutes=3.08
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:170:epoch=020/100 loss=0.086457 val_dice=0.000000 val_pr_auc=0.175177 minutes=3.08
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:178:epoch=021/100 loss=0.069410 val_dice=0.000008 val_pr_auc=0.254670 minutes=2.94
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:186:epoch=022/100 loss=0.074515 val_dice=0.141201 val_pr_auc=0.326820 minutes=2.99
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:194:epoch=023/100 loss=0.072652 val_dice=0.166533 val_pr_auc=0.313903 minutes=3.00
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:202:epoch=024/100 loss=0.064151 val_dice=0.172646 val_pr_auc=0.363963 minutes=3.08
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:210:epoch=025/100 loss=0.073862 val_dice=0.196468 val_pr_auc=0.386662 minutes=3.01
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:218:epoch=026/100 loss=0.072094 val_dice=0.132655 val_pr_auc=0.394473 minutes=2.98
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:226:epoch=027/100 loss=0.065739 val_dice=0.374149 val_pr_auc=0.413061 minutes=3.01
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:234:epoch=028/100 loss=0.068670 val_dice=0.317358 val_pr_auc=0.418032 minutes=3.12
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:242:epoch=029/100 loss=0.070705 val_dice=0.171511 val_pr_auc=0.374978 minutes=2.99
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:250:epoch=030/100 loss=0.064441 val_dice=0.323407 val_pr_auc=0.425493 minutes=3.18
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:258:epoch=031/100 loss=0.069248 val_dice=0.248666 val_pr_auc=0.454737 minutes=2.88
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:266:epoch=032/100 loss=0.061221 val_dice=0.377182 val_pr_auc=0.450258 minutes=3.05
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:274:epoch=033/100 loss=0.062718 val_dice=0.327263 val_pr_auc=0.424330 minutes=2.95
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:282:epoch=034/100 loss=0.063943 val_dice=0.247668 val_pr_auc=0.459621 minutes=3.10
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:290:epoch=035/100 loss=0.058946 val_dice=0.092848 val_pr_auc=0.377327 minutes=2.93
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:298:epoch=036/100 loss=0.059221 val_dice=0.481173 val_pr_auc=0.501920 minutes=3.02
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:306:epoch=037/100 loss=0.053694 val_dice=0.232841 val_pr_auc=0.466201 minutes=2.99
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:314:epoch=038/100 loss=0.061848 val_dice=0.460287 val_pr_auc=0.494024 minutes=3.04
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:322:epoch=039/100 loss=0.057948 val_dice=0.371737 val_pr_auc=0.489074 minutes=3.08
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:330:epoch=040/100 loss=0.059008 val_dice=0.406601 val_pr_auc=0.503391 minutes=3.08
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:338:epoch=041/100 loss=0.056795 val_dice=0.441511 val_pr_auc=0.519499 minutes=3.02
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:346:epoch=042/100 loss=0.065448 val_dice=0.413127 val_pr_auc=0.536155 minutes=3.01
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:354:epoch=043/100 loss=0.059635 val_dice=0.239140 val_pr_auc=0.526799 minutes=2.99
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:362:epoch=044/100 loss=0.069650 val_dice=0.433576 val_pr_auc=0.552912 minutes=3.09
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:370:epoch=045/100 loss=0.055908 val_dice=0.435073 val_pr_auc=0.542746 minutes=2.97
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:378:epoch=046/100 loss=0.054000 val_dice=0.487242 val_pr_auc=0.555513 minutes=2.88
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:386:epoch=047/100 loss=0.055662 val_dice=0.378074 val_pr_auc=0.507225 minutes=3.08
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:394:epoch=048/100 loss=0.059597 val_dice=0.478686 val_pr_auc=0.550781 minutes=3.11
runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log:402:epoch=049/100 loss=0.059587 val_dice=0.516431 val_pr_auc=0.572820 minutes=3.02
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/run_config.json:5:  "precision": "float16_autocast",
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/run_config.json:746:  "threshold_selection": "best Dice on complete validation volume with 2048 bins",
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/status.json:7:  "precision": "float16_autocast",
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/status.json:12:  "best_checkpoint": "runs/R100_fp16_clean_3seeds_20261014_150435/seed44/best.pt",
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/validation_selection.json:7:    "dice": 0.5729798256899185,
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/validation_selection.json:8:    "iou": 0.40152188175400944,
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/validation_selection.json:9:    "precision": 0.5655692044103381,
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/validation_selection.json:10:    "recall": 0.5805872272731943,
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/validation_selection.json:16:    "roc_auc_approx": 0.9589852925995812,
runs/R100_fp16_clean_3seeds_20261014_150435/smoke.log:5:/shared/home/khavarj/projects/fault_detection/.venv_train/lib/python3.13/site-packages/torch/autograd/graph.py:824: UserWarning: max_pool3d_with_indices_backward_cuda does not have a deterministic implementation, but you set 'torch.use_deterministic_algorithms(True, warn_only=True)'. You can file an issue at https://github.com/pytorch/pytorch/issues to help us prioritize adding deterministic support for this operation. (Triggered internally at /pytorch/aten/src/ATen/Context.cpp:93.)
runs/R100_fp16_clean_3seeds_20261014_150435/smoke.log:12:epoch=001/1 loss=0.779829 val_dice=0.068725 val_pr_auc=0.033207 minutes=0.17
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/history.csv:1:epoch,train_loss,train_patches,resampled_no_data_candidates,excluded_training_positive_labels,seconds,val_threshold,val_dice,val_iou,val_precision,val_recall,val_specificity,val_balanced_accuracy,val_accuracy,val_mcc,val_pr_auc_approx,val_roc_auc_approx,val_tp,val_fp,val_fn,val_tn
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/run_config.json:5:  "precision": "float16_autocast",
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/run_config.json:116:  "threshold_selection": "best Dice on smoke validation subset",
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/status.json:7:  "precision": "float16_autocast",
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/status.json:12:  "best_checkpoint": "runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/best.pt",
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/validation_selection.json:7:    "dice": 0.06884626641830875,
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/validation_selection.json:8:    "iou": 0.035650329241587765,
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/validation_selection.json:9:    "precision": 0.035650329241587765,
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/validation_selection.json:10:    "recall": 1.0,
runs/R100_fp16_clean_3seeds_20261014_150435/smoke_seed42/validation_selection.json:16:    "roc_auc_approx": 0.4517016441816569,
```

### Errors and numerical warnings

```text
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:129:EPOCH 074 train_loss=0.412175 val_loss=nan val_dice=0.429887 val_precision=0.315779 val_recall=0.673122 best=0.539004 elapsed_min=205.2
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:131:epoch=75/100 train_patch=32/64 loss=nan
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:133:epoch=75/100 train_patch=64/64 loss=nan
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:134:EPOCH 075 train_loss=nan val_loss=nan val_dice=0.267436 val_precision=0.199014 val_recall=0.407552 best=0.539004 elapsed_min=213.2
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:135:epoch=76/100 train_patch=16/64 loss=nan
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:138:epoch=76/100 train_patch=64/64 loss=nan
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:139:EPOCH 076 train_loss=nan val_loss=nan val_dice=0.267436 val_precision=0.199014 val_recall=0.407552 best=0.539004 elapsed_min=221.2
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:140:epoch=77/100 train_patch=16/64 loss=nan
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:142:epoch=77/100 train_patch=48/64 loss=nan
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:144:EPOCH 077 train_loss=nan val_loss=nan val_dice=0.257658 val_precision=0.186943 val_recall=0.414424 best=0.539004 elapsed_min=229.1
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:145:epoch=78/100 train_patch=16/64 loss=nan
reports/training/paper_attention3d_thebe_supervised_seed42_resume.log:147:epoch=78/100 train_patch=48/64 loss=nan
reports/training/r100_fp16_3seed_queue_20261014_145225.log:3:Traceback (most recent call last):
reports/training/r100_fp16_3seed_queue_20261014_145225.log:14:    raise RuntimeError(message)
reports/training/r100_fp16_3seed_queue_20261014_145225.log:15:RuntimeError: Trainer exited with code 1; see runs/R100_fp16_clean_3seeds_20261014_145225/smoke.log
reports/training/r100_fp16_3seed_queue_20261014_145510.log:3:Traceback (most recent call last):
reports/training/r100_fp16_3seed_queue_20261014_145510.log:14:    raise RuntimeError(message)
reports/training/r100_fp16_3seed_queue_20261014_145510.log:15:RuntimeError: Trainer exited with code 1; see runs/R100_fp16_clean_3seeds_20261014_145510/seed42.log
reports/training/R100_thebe_seed42_20261005_102737.log:57:Traceback (most recent call last):
reports/training/R100_thebe_seed42_20261005_102737.log:69:    raise RuntimeError(f"Constant observed seismic at {origin}")
reports/training/R100_thebe_seed42_20261005_102737.log:70:RuntimeError: Constant observed seismic at (203, 1696, 199)
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/best.pt: binary file matches (found "\0" byte around offset 4)
runs/R100_fp16_clean_3seeds_20261014_150435/seed44/last.pt: binary file matches (found "\0" byte around offset 4)
```

### Newest log tails

`runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log`

```text
epoch=97/100 train_patch=60/360 loss=0.191846
epoch=97/100 train_patch=120/360 loss=0.277550
epoch=97/100 train_patch=180/360 loss=0.091489
epoch=97/100 train_patch=240/360 loss=0.000342
epoch=97/100 train_patch=300/360 loss=0.000000
epoch=97/100 train_patch=360/360 loss=0.036241
evaluation_patches=100/128
epoch=097/100 loss=0.051889 val_dice=0.548214 val_pr_auc=0.633269 minutes=3.00
epoch=98/100 train_patch=60/360 loss=0.136171
epoch=98/100 train_patch=120/360 loss=0.000024
epoch=98/100 train_patch=180/360 loss=0.081139
epoch=98/100 train_patch=240/360 loss=0.116304
epoch=98/100 train_patch=300/360 loss=0.194777
epoch=98/100 train_patch=360/360 loss=0.003614
evaluation_patches=100/128
epoch=098/100 loss=0.047368 val_dice=0.417820 val_pr_auc=0.618263 minutes=3.19
epoch=99/100 train_patch=60/360 loss=0.096293
epoch=99/100 train_patch=120/360 loss=0.000711
epoch=99/100 train_patch=180/360 loss=0.053551
epoch=99/100 train_patch=240/360 loss=0.011706
epoch=99/100 train_patch=300/360 loss=0.030885
epoch=99/100 train_patch=360/360 loss=0.015740
evaluation_patches=100/128
epoch=099/100 loss=0.051740 val_dice=0.571887 val_pr_auc=0.641601 minutes=3.10
epoch=100/100 train_patch=60/360 loss=0.105558
epoch=100/100 train_patch=120/360 loss=0.000385
epoch=100/100 train_patch=180/360 loss=0.002327
epoch=100/100 train_patch=240/360 loss=0.000015
epoch=100/100 train_patch=300/360 loss=0.049922
epoch=100/100 train_patch=360/360 loss=0.008582
evaluation_patches=100/128
epoch=100/100 loss=0.050488 val_dice=0.544014 val_pr_auc=0.647909 minutes=2.94
BEST EPOCH: 95; full validation begins
evaluation_patches=100/650
evaluation_patches=200/650
evaluation_patches=400/650
evaluation_patches=500/650
VALIDATION THRESHOLD: 0.244141; test evaluation disabled
R100 VALIDATION-ONLY COMPLETE seed=44 epochs=100 best_epoch=95
QUEUE CHILD EXIT 2026-10-15T02:29:39.074418+00:00 code=0
```

`reports/training/r100_fp16_3seed_queue_20261014_150435.log`

```text
nohup: ignoring input
START seed=42 smoke=True pid=1945423 log=runs/R100_fp16_clean_3seeds_20261014_150435/smoke.log
START seed=42 smoke=False pid=1946437 log=runs/R100_fp16_clean_3seeds_20261014_150435/seed42.log
PASS seed=42 validation_dice=0.544072
START seed=43 smoke=False pid=3264730 log=runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log
PASS seed=43 validation_dice=0.569856
START seed=44 smoke=False pid=379744 log=runs/R100_fp16_clean_3seeds_20261014_150435/seed44.log
PASS seed=44 validation_dice=0.572980
THREE SEEDS COMPLETE validation Dice mean=0.562302 sample_SD=0.015865; no test evaluation
```

`runs/R100_fp16_clean_3seeds_20261014_150435/seed43.log`

```text
epoch=97/100 train_patch=60/360 loss=0.000206
epoch=97/100 train_patch=120/360 loss=0.000322
epoch=97/100 train_patch=180/360 loss=0.000758
epoch=97/100 train_patch=240/360 loss=0.184065
epoch=97/100 train_patch=300/360 loss=0.005448
epoch=97/100 train_patch=360/360 loss=0.217553
evaluation_patches=100/128
epoch=097/100 loss=0.043323 val_dice=0.499799 val_pr_auc=0.628407 minutes=3.00
epoch=98/100 train_patch=60/360 loss=0.013608
epoch=98/100 train_patch=120/360 loss=0.090962
epoch=98/100 train_patch=180/360 loss=0.005916
epoch=98/100 train_patch=240/360 loss=0.000000
epoch=98/100 train_patch=300/360 loss=0.165707
epoch=98/100 train_patch=360/360 loss=0.094480
evaluation_patches=100/128
epoch=098/100 loss=0.050284 val_dice=0.579185 val_pr_auc=0.642430 minutes=3.08
epoch=99/100 train_patch=60/360 loss=0.118951
epoch=99/100 train_patch=120/360 loss=0.010276
epoch=99/100 train_patch=180/360 loss=0.000355
epoch=99/100 train_patch=240/360 loss=0.000069
epoch=99/100 train_patch=300/360 loss=0.011696
epoch=99/100 train_patch=360/360 loss=0.006897
evaluation_patches=100/128
epoch=099/100 loss=0.043900 val_dice=0.568614 val_pr_auc=0.648535 minutes=3.05
epoch=100/100 train_patch=60/360 loss=0.009470
epoch=100/100 train_patch=120/360 loss=0.002223
epoch=100/100 train_patch=180/360 loss=0.004774
epoch=100/100 train_patch=240/360 loss=0.000046
epoch=100/100 train_patch=300/360 loss=0.112857
epoch=100/100 train_patch=360/360 loss=0.013399
evaluation_patches=100/128
epoch=100/100 loss=0.048542 val_dice=0.477356 val_pr_auc=0.643192 minutes=3.15
BEST EPOCH: 93; full validation begins
evaluation_patches=100/650
evaluation_patches=200/650
evaluation_patches=400/650
evaluation_patches=500/650
VALIDATION THRESHOLD: 0.279297; test evaluation disabled
R100 VALIDATION-ONLY COMPLETE seed=43 epochs=100 best_epoch=93
QUEUE CHILD EXIT 2026-10-14T21:26:57.084942+00:00 code=0
```
