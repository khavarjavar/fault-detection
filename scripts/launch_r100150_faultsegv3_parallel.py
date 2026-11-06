#!/usr/bin/env python3
"""Launch the matched 150-epoch R100 and FaultSegV3 validation-only runs."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PYTHON = ROOT / ".venv_train/bin/python"
RUNS = (
    {
        "name": "r100_150_seed43",
        "run_dir": ROOT / "runs/r100_150_seed43_20261102",
        "log": ROOT / "reports/training/r100_150_seed43_20261102.log",
        "command": [
            str(PYTHON), "-u", "scripts/train_r100_fp16_clean.py",
            "--run-dir", "runs/r100_150_seed43_20261102",
            "--seed", "43", "--epochs", "150",
        ],
    },
    {
        "name": "faultsegv3_matched_150_seed43",
        "run_dir": ROOT / "runs/faultsegv3_matched_150_seed43_20261102",
        "log": ROOT / "reports/training/faultsegv3_matched_150_seed43_20261102.log",
        "command": [
            str(PYTHON), "-u", "scripts/train_faultsegv3_thebe_matched.py",
            "--run-dir", "runs/faultsegv3_matched_150_seed43_20261102",
            "--seed", "43", "--epochs", "150",
        ],
    },
)


def main() -> None:
    if not PYTHON.is_file():
        raise FileNotFoundError(PYTHON)
    for spec in RUNS:
        if spec["run_dir"].exists():
            raise FileExistsError(spec["run_dir"])
        if spec["log"].exists():
            raise FileExistsError(spec["log"])
        spec["log"].parent.mkdir(parents=True, exist_ok=True)

    launched = []
    for spec in RUNS:
        stream = spec["log"].open("x", buffering=1)
        process = subprocess.Popen(
            spec["command"],
            cwd=ROOT,
            stdin=subprocess.DEVNULL,
            stdout=stream,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
        stream.close()
        launched.append(
            {
                "name": spec["name"],
                "pid": process.pid,
                "command": spec["command"],
                "run_dir": str(spec["run_dir"].relative_to(ROOT)),
                "log": str(spec["log"].relative_to(ROOT)),
            }
        )

    record = {
        "status": "launched",
        "launched_utc": datetime.now(timezone.utc).isoformat(),
        "gpu_policy": "both jobs share CUDA device 0; measured combined peak allocation from prior checks is about 3.43 GiB",
        "test_files_read": False,
        "runs": launched,
    }
    output = ROOT / "runs/r100150_faultsegv3_parallel_20261102_launcher.json"
    temporary = output.with_suffix(".json.part")
    temporary.write_text(json.dumps(record, indent=2) + "\n")
    temporary.replace(output)
    print(json.dumps(record, indent=2), flush=True)


if __name__ == "__main__":
    main()
