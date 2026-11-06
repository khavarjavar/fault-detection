#!/usr/bin/env python3
"""Detach the recovered ViT queue and its dependent author-model queue."""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def launch(name: str, command: list[str]) -> dict[str, object]:
    log_path = ROOT / "reports/training" / f"{name}_launcher.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("ab", buffering=0) as stream:
        process = subprocess.Popen(
            command,
            cwd=ROOT,
            stdin=subprocess.DEVNULL,
            stdout=stream,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
    return {
        "name": name,
        "pid": process.pid,
        "command": command,
        "log": str(log_path.relative_to(ROOT)),
    }


def main() -> int:
    launched = [
        launch(
            "vit_setr_recovery_queue",
            [sys.executable, "-u", "scripts/recover_vit_queue_after_disk_full.py"],
        ),
        launch(
            "thebe_author2d_queue",
            [sys.executable, "-u", "scripts/run_thebe_author2d_queue.py"],
        ),
    ]
    record = {
        "status": "launched",
        "launched_utc": datetime.now(timezone.utc).isoformat(),
        "jobs": launched,
        "test_files_read": False,
    }
    path = ROOT / "runs/recovered_experiment_queue_launchers_20261102.json"
    path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
