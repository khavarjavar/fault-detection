#!/usr/bin/env python3
"""Reconcile queue metadata after a duplicate recovery hit the run-dir guard."""

from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
from datetime import datetime, timezone


ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "runs/pure2d_thebe_architecture_controls_queue.json"
RUN = ROOT / "runs/vit_setr_pure_thebe_150_seed43_20261102"
ARCHIVE = Path(
    "/tmp/fault_detection_redundant_last_archive_20261102/runs/"
    "vit_setr_pure_thebe_150_seed43_20261102_recovery_interrupted_epoch29"
)
TRAINER_PID = 146783
RECOVERY_PID = 146781


def main() -> int:
    os.kill(TRAINER_PID, 0)
    os.kill(RECOVERY_PID, 0)
    history = RUN / "history.csv"
    rows = history.read_text(encoding="utf-8").strip().splitlines()
    last_epoch = int(rows[-1].split(",", 1)[0])
    if last_epoch < 29:
        raise RuntimeError(f"Unexpected live history epoch: {last_epoch}")
    config = RUN / "run_config.json"
    if not config.exists():
        shutil.copy2(ARCHIVE / "run_config.json", config)

    state = json.loads(STATE.read_text(encoding="utf-8"))
    records = [row for row in state["jobs"] if row.get("model") == "vit_setr"]
    if len(records) != 1:
        raise RuntimeError(f"Expected one ViT record, found {len(records)}")
    record = records[0]
    record.update(
        status="running_recovery",
        active_recovery_pid=RECOVERY_PID,
        active_trainer_pid=TRAINER_PID,
        last_verified_epoch=last_epoch,
        reconciled_utc=datetime.now(timezone.utc).isoformat(),
        duplicate_recovery_result={
            "returncode": record.get("recovery_returncode"),
            "reason": "A duplicate launcher encountered the existing run-directory guard; the original clean recovery remained live.",
        },
        active_run_directory=str(RUN.relative_to(ROOT)),
        epoch29_snapshot=str(ARCHIVE),
    )
    state.update(
        status="recovering_vit_after_disk_full",
        reconciliation=(
            "Original clean ViT recovery is live. Duplicate recovery stopped safely "
            "on FileExistsError and did not alter the model."
        ),
    )
    temporary = STATE.with_suffix(".json.reconciled")
    temporary.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    temporary.replace(STATE)
    print(json.dumps({"status": state["status"], "last_epoch": last_epoch}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
