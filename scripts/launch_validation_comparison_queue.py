#!/usr/bin/env python3
"""Launch the post-training validation comparison watcher as a detached job."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--r100-pid", type=int, required=True)
    parser.add_argument("--v3-pid", type=int, required=True)
    parser.add_argument("--swin-pid", type=int, required=True)
    args = parser.parse_args()
    log_path = ROOT / "reports/training/r100150_faultsegv3_validation_comparison_queue.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    command = [
        sys.executable,
        "-u",
        "scripts/wait_r100_faultsegv3_validation_comparison.py",
        "--r100-pid",
        str(args.r100_pid),
        "--v3-pid",
        str(args.v3_pid),
        "--swin-pid",
        str(args.swin_pid),
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
        "log": str(log_path.relative_to(ROOT)),
        "test_files_read": False,
    }
    path = ROOT / "runs/r100150_faultsegv3_validation_comparison_launcher.json"
    path.write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps(record, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
