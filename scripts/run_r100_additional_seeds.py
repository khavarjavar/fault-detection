#!/usr/bin/env python3
"""Train additional clean R100 seeds from scratch, without test evaluation.

Use --prepare-only to write a reviewable plan without training. Resume a prepared
or interrupted queue with --resume-queue. The original trainer and recipe remain
unchanged; this is a seed-count experiment, not fine-tuning.
"""
import argparse
from datetime import datetime, timezone
import fcntl
import json
import os
from pathlib import Path
import signal
import subprocess
import sys

from run_r100_3seed_queue import validate_run


ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "runs/R100_fp16_clean_3seeds_20261014_150435/seed42/run_config.json"


def save(path, value):
    temporary = path.with_suffix(".json.part")
    temporary.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")
    temporary.replace(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-root", type=Path, required=True)
    parser.add_argument("--seeds", type=int, nargs="+", required=True)
    parser.add_argument("--prepare-only", action="store_true")
    parser.add_argument("--resume-queue", action="store_true")
    args = parser.parse_args()
    if len(args.seeds) != len(set(args.seeds)) or any(s in (42, 43, 44) or not 0 <= s < 2**32 for s in args.seeds):
        parser.error("Provide unique new seeds; 42,43,44 already exist")
    os.chdir(ROOT)
    reference = json.loads(REFERENCE.read_text())
    directory = args.run_root.resolve()
    directory.relative_to(ROOT / "runs")  # Keep outputs inside the project runs folder.
    protocol = reference["protocol_hash"]
    plan = {"seeds": args.seeds, "epochs_per_seed": 100, "initialization": "from_scratch",
            "fine_tuning": False, "protocol_hash": protocol, "test_files_read": False,
            "validation_seed": 1042, "trainer": "scripts/train_r100_fp16_clean.py"}
    with (ROOT / "runs/R100_3seed_queue.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        if args.resume_queue:
            saved_plan = json.loads((directory / "plan.json").read_text())
            if saved_plan != plan:
                raise RuntimeError("Saved queue plan differs; use a new phase directory")
            previous = json.loads((directory / "queue_status.json").read_text())
            pid = previous.get("active_child_pid")
            if pid:
                command_path = Path(f"/proc/{pid}/cmdline")
                if command_path.exists() and b"train_r100_fp16_clean.py" in command_path.read_bytes():
                    raise RuntimeError("A previous trainer is still running")
        else:
            directory.mkdir(parents=True, exist_ok=False)
            save(directory / "plan.json", plan)
        state = {**plan, "status": "prepared", "completed_seeds": [], "active_child_pid": None,
                 "queue_pid": os.getpid(), "updated_utc": datetime.now(timezone.utc).isoformat()}
        def persist():
            state["updated_utc"] = datetime.now(timezone.utc).isoformat()
            save(directory / "queue_status.json", state)
        persist()
        if args.prepare_only:
            print(f"Prepared seeds {args.seeds}; no training started: {directory}")
            return
        active = None
        def interrupted(signum, _frame):
            raise KeyboardInterrupt(f"Queue signal {signum}")
        signal.signal(signal.SIGINT, interrupted)
        signal.signal(signal.SIGTERM, interrupted)
        try:
            for seed in args.seeds:
                run_dir = directory / f"seed{seed}"
                if not (run_dir / "status.json").exists():
                    command = [sys.executable, "-u", str(ROOT / plan["trainer"]),
                               "--seed", str(seed), "--validation-seed", "1042",
                               "--expected-protocol", protocol,
                               "--run-dir", str(run_dir.relative_to(ROOT))]
                    if run_dir.exists():
                        if not args.resume_queue:
                            raise RuntimeError("Existing partial run requires --resume-queue")
                        command.append("--resume")
                    with (directory / f"seed{seed}.log").open("a", buffering=1) as log:
                        active = subprocess.Popen(command, stdout=log, stderr=subprocess.STDOUT, cwd=ROOT)
                        state.update(status="training", active_seed=seed, active_child_pid=active.pid)
                        persist()
                        print(f"Training seed={seed}, pid={active.pid}, log={log.name}", flush=True)
                        code = active.wait()
                        active = None
                        state.update(active_child_pid=None, last_exit_code=code)
                        persist()
                        if code:
                            raise RuntimeError(f"Seed {seed} failed; see its log")
                validate_run(run_dir, seed, expected_protocol=protocol)
                state["completed_seeds"].append(seed)
                state.update(status="seed_verified", active_child_pid=None)
                persist()
            state.update(status="complete")
            persist()
            print(f"Completed clean seeds {args.seeds}; no test evaluation", flush=True)
        except BaseException as exc:
            if active is not None and active.poll() is None:
                active.terminate()
                try:
                    active.wait(timeout=15)
                except subprocess.TimeoutExpired:
                    active.kill()
                    active.wait()
            state.update(status="interrupted" if isinstance(exc, KeyboardInterrupt) else "failed",
                         error=str(exc), active_child_pid=None)
            persist()
            raise


if __name__ == "__main__":
    main()
