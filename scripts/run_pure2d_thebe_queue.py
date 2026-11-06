#!/usr/bin/env python3
"""Run the preflighted pure 2D Thebe architecture controls sequentially.

Only one queued model occupies the GPU at a time.  The queue is deliberately
separate from the author-protocol UNet/HED/RCF/DeepLabM reproductions: these
three runs test modern official backbones with explicitly disclosed local
dense-prediction heads.
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
MINIMUM_FREE_GIB = 3.0
JOBS = (
    ("deeplabv3", 2, "runs/deeplabv3_pure_thebe_150_seed43_20261102"),
    ("swin_fpn", 2, "runs/swin_fpn_pure_thebe_150_seed43_20261102"),
    ("vit_setr", 1, "runs/vit_setr_pure_thebe_150_seed43_20261102"),
)


def write_state(payload: dict) -> None:
    temporary = STATE.with_suffix(".json.part")
    temporary.write_text(json.dumps(payload, indent=2) + "\n")
    temporary.replace(STATE)


def free_gib() -> float:
    return shutil.disk_usage(ROOT).free / 1024**3


def main() -> int:
    state = {
        "status": "running",
        "started_unix": time.time(),
        "policy": "sequential; test files closed; random-initialized architecture controls",
        "jobs": [],
    }
    write_state(state)
    for model, batch_size, relative_run_dir in JOBS:
        run_dir = ROOT / relative_run_dir
        log_path = ROOT / "reports/training" / f"{run_dir.name}.log"
        record = {
            "model": model,
            "run_dir": relative_run_dir,
            "log": str(log_path.relative_to(ROOT)),
            "batch_size": batch_size,
            "status": "pending",
        }
        state["jobs"].append(record)
        if run_dir.exists():
            record["status"] = "failed_existing_run_dir"
            state["status"] = "failed"
            write_state(state)
            return 2
        available = free_gib()
        if available < MINIMUM_FREE_GIB:
            record.update(status="paused_low_disk", free_gib=available)
            state["status"] = "paused_low_disk"
            write_state(state)
            return 3
        command = [
            sys.executable,
            "-u",
            "scripts/train_pure2d_thebe.py",
            "--model",
            model,
            "--run-dir",
            relative_run_dir,
            "--seed",
            "43",
            "--epochs",
            "150",
            "--batch-size",
            str(batch_size),
        ]
        record.update(
            status="running",
            command=command,
            started_unix=time.time(),
            free_gib_at_start=available,
        )
        write_state(state)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("w") as log:
            result = subprocess.run(
                command,
                cwd=ROOT,
                stdout=log,
                stderr=subprocess.STDOUT,
                check=False,
            )
        record.update(
            status="complete" if result.returncode == 0 else "failed",
            returncode=result.returncode,
            ended_unix=time.time(),
            free_gib_at_end=free_gib(),
        )
        write_state(state)
        if result.returncode:
            state["status"] = "failed"
            write_state(state)
            return result.returncode
    state.update(status="complete", ended_unix=time.time())
    write_state(state)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
