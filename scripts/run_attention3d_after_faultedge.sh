#!/usr/bin/env bash
set -euo pipefail

cd /shared/home/khavarj/projects/fault_detection

faultedge_pattern='[t]rain_faultedgeformer_thebe.py --run-dir runs/faultedgeformer_thebe_full_seed42_20261026'
faultedge_status='runs/faultedgeformer_thebe_full_seed42_20261026/status.json'
attention_run='runs/attention3d_two_survey_pretext_seed42_20261026'

echo "$(date --iso-8601=seconds) waiting for FaultEdgeFormer seed 42"
while pgrep -f "$faultedge_pattern" >/dev/null; do
    sleep 60
done

.venv_train/bin/python - "$faultedge_status" <<'PY'
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
if not path.is_file():
    raise SystemExit(f"FaultEdgeFormer ended without completion marker: {path}")
status = json.loads(path.read_text())
if status.get("status") != "validation_only_complete":
    raise SystemExit(f"FaultEdgeFormer completion status is invalid: {status.get('status')}")
if status.get("epochs_completed") != status.get("epochs_requested"):
    raise SystemExit("FaultEdgeFormer did not complete every requested epoch")
print("FaultEdgeFormer completion gate passed")
PY

echo "$(date --iso-8601=seconds) running exclusive Attention3D GPU preflight"
.venv_train/bin/python -u scripts/train_attention3d_two_survey_pretext.py \
    --phase preflight \
    --run-dir "$attention_run" \
    --memory-fraction 0.92

echo "$(date --iso-8601=seconds) starting Attention3D two-survey pretraining"
.venv_train/bin/python -u scripts/train_attention3d_two_survey_pretext.py \
    --phase train \
    --run-dir "$attention_run" \
    --memory-fraction 0.92
