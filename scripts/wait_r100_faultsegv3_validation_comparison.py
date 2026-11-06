#!/usr/bin/env python3
"""Wait for all three 150-epoch jobs, then render the validation comparison."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[1]


def alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def write_state(path: Path, value: dict) -> None:
    temporary = path.with_suffix(path.suffix + ".part")
    temporary.write_text(json.dumps(value, indent=2) + "\n")
    temporary.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--r100-pid", type=int, default=4131776)
    parser.add_argument("--v3-pid", type=int, default=4131777)
    parser.add_argument("--swin-pid", type=int, default=156201)
    parser.add_argument(
        "--r100-run", type=Path,
        default=ROOT / "runs/r100_150_seed43_20261102",
    )
    parser.add_argument(
        "--v3-run", type=Path,
        default=ROOT / "runs/faultsegv3_matched_150_seed43_20261102",
    )
    parser.add_argument(
        "--swin-run", type=Path,
        default=ROOT / "runs/swinunetr_matched_150_seed43_20261102",
    )
    parser.add_argument("--poll-seconds", type=int, default=60)
    parser.add_argument("--timeout-hours", type=float, default=72.0)
    args = parser.parse_args()
    state_path = ROOT / "runs/r100150_faultsegv3_validation_comparison_queue.json"
    started = time.time()
    while time.time() - started < args.timeout_hours * 3600:
        statuses = []
        for name, run_dir, pid in (
            ("r100", args.r100_run, args.r100_pid),
            ("faultsegv3", args.v3_run, args.v3_pid),
            ("swinunetr", args.swin_run, args.swin_pid),
        ):
            status_path = run_dir / "status.json"
            status = json.loads(status_path.read_text()) if status_path.is_file() else None
            statuses.append(
                {"name": name, "pid": pid, "alive": alive(pid), "status": status}
            )
        write_state(
            state_path,
            {"queue_status": "waiting", "elapsed_seconds": time.time() - started,
             "runs": statuses, "test_files_read": False},
        )
        if all(
            item["status"] is not None
            and item["status"].get("status") == "validation_only_complete"
            for item in statuses
        ):
            command = [
                sys.executable,
                str(ROOT / "scripts/visualize_r100_faultsegv3_validation.py"),
                "--r100-run", str(args.r100_run),
                "--v3-run", str(args.v3_run),
                "--swin-run", str(args.swin_run),
            ]
            completed = subprocess.run(command, cwd=ROOT, check=False)
            final = {
                "queue_status": "complete" if completed.returncode == 0 else "visualizer_failed",
                "visualizer_returncode": completed.returncode,
                "elapsed_seconds": time.time() - started,
                "runs": statuses,
                "test_files_read": False,
            }
            write_state(state_path, final)
            return completed.returncode
        failed = [
            item for item in statuses
            if not item["alive"] and item["status"] is None
        ]
        if failed:
            write_state(
                state_path,
                {"queue_status": "training_process_ended_without_status",
                 "elapsed_seconds": time.time() - started,
                 "runs": statuses, "test_files_read": False},
            )
            return 2
        time.sleep(args.poll_seconds)
    write_state(
        state_path,
        {"queue_status": "timeout", "elapsed_seconds": time.time() - started,
         "test_files_read": False},
    )
    return 3


if __name__ == "__main__":
    raise SystemExit(main())
