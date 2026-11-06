#!/usr/bin/env bash
set -euo pipefail

cd /shared/home/khavarj/projects/fault_detection
attention_result='reports/evaluation/attention3d_two_survey_pretext_seed42_20261026/result.json'
faultedge_result='reports/evaluation/faultedgeformer_thebe_full_seed42_20261026/result.json'

echo "$(date --iso-8601=seconds) waiting for Attention3D pretraining completion"
while pgrep -f '[t]rain_attention3d_two_survey_pretext.py --phase train' >/dev/null; do
    sleep 60
done

.venv_train/bin/python -u scripts/report_attention3d_pretext.py \
    runs/attention3d_two_survey_pretext_seed42_20261026

echo "$(date --iso-8601=seconds) waiting for FaultEdgeFormer frozen test result"
while [[ ! -f "$faultedge_result" ]]; do
    sleep 60
done

if [[ ! -f "$attention_result" ]]; then
    echo "Missing Attention3D report: $attention_result" >&2
    exit 1
fi
.venv_train/bin/python -u scripts/make_active_runs_quick_report.py
