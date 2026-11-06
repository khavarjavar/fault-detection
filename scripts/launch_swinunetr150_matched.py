#!/usr/bin/env python3
"""Launch the matched 150-epoch SwinUNETR Thebe control."""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    run_dir = ROOT / "runs/swinunetr_matched_150_seed43_20261102"
    log_path = ROOT / "reports/training/swinunetr_matched_150_seed43_20261102.log"
    if run_dir.exists():
        raise FileExistsError(run_dir)
    if log_path.exists():
        raise FileExistsError(log_path)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    command = [
        sys.executable,
        "-u",
        "scripts/train_swinunetr_thebe_matched.py",
        "--run-dir",
        str(run_dir.relative_to(ROOT)),
        "--seed",
        "43",
        "--epochs",
        "150",
    ]
    with log_path.open("ab", buffering=0) as stream:
        process = subprocess.Popen(
            command,
            cwd=ROOT,
            stdin=subprocess.DEVNULL,
            stdout=stream,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
    record = {
        "status": "launched",
        "launched_utc": datetime.now(timezone.utc).isoformat(),
        "pid": process.pid,
        "command": command,
        "run_dir": str(run_dir.relative_to(ROOT)),
        "log": str(log_path.relative_to(ROOT)),
        "comparison": "matched seed-43 R100/V3 recipe; architecture only",
        "test_files_read": False,
    }
    record_path = ROOT / "runs/swinunetr_matched_150_seed43_20261102_launcher.json"
    record_path.write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps(record, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
