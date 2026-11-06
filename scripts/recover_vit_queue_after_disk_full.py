#!/usr/bin/env python3
"""Restart the interrupted pure-2D ViT run and close its queue cleanly.

The first ViT attempt reached epoch 20 but its trainer intentionally stores no
optimizer or scheduler state. It is therefore restarted from epoch 1 rather
than continued under a changed optimization protocol. The failed directory is
preserved in /tmp/fault_detection_redundant_last_archive_20261102.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "runs/pure2d_thebe_architecture_controls_queue.json"
RUN_DIR = ROOT / "runs/vit_setr_pure_thebe_150_seed43_20261102"
LOG = ROOT / "reports/training/vit_setr_pure_thebe_150_seed43_20261102.log"
MINIMUM_FREE_GIB = 3.5


def write_state(payload: dict) -> None:
    temporary = STATE.with_suffix(".json.recovery")
    temporary.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    temporary.replace(STATE)


def main() -> int:
    if RUN_DIR.exists():
        raise RuntimeError(f"Recovery requires an absent fresh run directory: {RUN_DIR}")
    available = shutil.disk_usage(ROOT).free / 1024**3
    if available < MINIMUM_FREE_GIB:
        raise RuntimeError(f"Only {available:.2f} GiB free; refusing ViT restart")
    state = json.loads(STATE.read_text(encoding="utf-8"))
    jobs = state.get("jobs", [])
    records = [row for row in jobs if row.get("model") == "vit_setr"]
    if len(records) != 1:
        raise RuntimeError(f"Expected one stale ViT queue record, found {len(records)}")
    record = records[0]
    command = [
        sys.executable, "-u", "scripts/train_pure2d_thebe.py",
        "--model", "vit_setr", "--run-dir", str(RUN_DIR.relative_to(ROOT)),
        "--seed", "43", "--epochs", "150", "--batch-size", "1",
    ]
    record.update(
        status="restarted_after_disk_full",
        recovery_started_unix=time.time(),
        recovery_command=command,
        failed_attempt_preserved=(
            "/tmp/fault_detection_redundant_last_archive_20261102/runs/"
            "vit_setr_pure_thebe_150_seed43_20261102_failed_disk_full"
        ),
        restart_reason=(
            "trainer checkpoint lacks optimizer/scheduler state; exact continuation "
            "is impossible, so restart from epoch 1 preserves protocol"
        ),
        free_gib_at_recovery_start=available,
    )
    state["status"] = "recovering_vit_after_disk_full"
    write_state(state)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as stream:
        stream.write("\n=== CLEAN VIT RESTART AFTER DISK-FULL FAILURE ===\n")
        stream.flush()
        result = subprocess.run(
            command, cwd=ROOT, stdout=stream, stderr=subprocess.STDOUT, check=False
        )
    record.update(
        status="complete" if result.returncode == 0 else "failed_recovery",
        recovery_returncode=result.returncode,
        recovery_ended_unix=time.time(),
        free_gib_at_recovery_end=shutil.disk_usage(ROOT).free / 1024**3,
    )
    state.update(
        status="complete" if result.returncode == 0 else "failed",
        recovery_ended_unix=time.time(),
    )
    write_state(state)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
