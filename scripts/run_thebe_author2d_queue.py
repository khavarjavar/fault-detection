#!/usr/bin/env python3
"""Wait for 2D controls, then run model-native Thebe baselines sequentially."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTROL_STATE = ROOT / "runs/pure2d_thebe_architecture_controls_queue.json"
STATE = ROOT / "runs/thebe_author2d_model_native_queue.json"
MINIMUM_FREE_GIB = 3.0
JOBS = ("hed", "rcf", "unet", "deeplabm")


def read_json(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def write_state(payload: dict) -> None:
    temporary = STATE.with_suffix(".json.part")
    temporary.write_text(json.dumps(payload, indent=2) + "\n")
    temporary.replace(STATE)


def free_gib() -> float:
    return shutil.disk_usage(ROOT).free / 1024**3


def main() -> int:
    state = {
        "status": "waiting_for_architecture_controls",
        "started_unix": time.time(),
        "policy": (
            "sequential model-native budgeted adaptations; source-verified "
            "Thebe model graphs and losses; test files closed"
        ),
        "jobs": [],
    }
    write_state(state)
    while True:
        controls = read_json(CONTROL_STATE)
        status = controls.get("status") if controls else None
        if status == "complete":
            break
        if status in {"failed", "paused_low_disk"}:
            state.update(status="blocked_by_architecture_controls", control_status=status)
            write_state(state)
            return 2
        time.sleep(30)
    state["status"] = "running"
    write_state(state)
    for name in JOBS:
        relative_run_dir = f"runs/thebe_author_{name}_native_100_seed43_20261102"
        run_dir = ROOT / relative_run_dir
        log_path = ROOT / "reports/training" / f"{run_dir.name}.log"
        record = {
            "model": name,
            "run_dir": relative_run_dir,
            "log": str(log_path.relative_to(ROOT)),
            "status": "pending",
        }
        state["jobs"].append(record)
        if run_dir.exists():
            record["status"] = "failed_existing_run_dir"
            state["status"] = "failed"
            write_state(state)
            return 3
        available = free_gib()
        if available < MINIMUM_FREE_GIB:
            record.update(status="paused_low_disk", free_gib=available)
            state["status"] = "paused_low_disk"
            write_state(state)
            return 4
        command = [
            sys.executable,
            "-u",
            "scripts/train_thebe_author2d.py",
            "--model",
            name,
            "--run-dir",
            relative_run_dir,
            "--seed",
            "43",
            "--epochs",
            "100",
            "--batch-size",
            "64",
            "--train-patches",
            "23040",
            "--validation-patches",
            "4096",
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
                command, cwd=ROOT, stdout=log,
                stderr=subprocess.STDOUT, check=False
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
