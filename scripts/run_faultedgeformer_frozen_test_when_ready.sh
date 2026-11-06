#!/usr/bin/env bash
set -euo pipefail

cd /shared/home/khavarj/projects/fault_detection
run_dir='runs/faultedgeformer_thebe_full_seed42_20261026'
pattern='[t]rain_faultedgeformer_thebe.py --run-dir runs/faultedgeformer_thebe_full_seed42_20261026'
log='reports/training/faultedgeformer_frozen_test_20261026.log'

echo "$(date --iso-8601=seconds) waiting for completed FaultEdgeFormer training"
while pgrep -f "$pattern" >/dev/null; do
    sleep 60
done

echo "$(date --iso-8601=seconds) starting frozen validation and Thebe test"
.venv_train/bin/python -u scripts/evaluate_faultedgeformer_frozen_test.py "$run_dir" 2>&1 | tee "$log"
