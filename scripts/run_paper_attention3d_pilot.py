#!/usr/bin/env python3
"""Supervise the bounded attention pilot without controlling existing jobs."""
from __future__ import annotations

import datetime as dt
import fcntl
import json
import os
from pathlib import Path
import subprocess
import sys
import time

from paper_attention3d_pilot import sha256, write_json

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "runs/attention3d_denoising_pilot_20261019_v2"
SEED_RUN = ROOT / "runs/R100_seed_saturation_pilot_20261019"


def utc_now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def seed_snapshot():
    state = json.loads((SEED_RUN / "pipeline_state.json").read_text())
    queue = json.loads((SEED_RUN / "queue_status.json").read_text())
    return {"pipeline": state, "queue": queue}


def main():
    RUN.mkdir(parents=True, exist_ok=True)
    with (RUN / ".supervisor.lock").open("a+") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        if (RUN / "config.json").exists():
            raise FileExistsError("Pilot already started; refusing a duplicate run")
        plan = json.loads((RUN / "launch_plan.json").read_text())
        for name, expected in plan["source_sha256"].items():
            if sha256(ROOT / name) != expected:
                raise RuntimeError(f"Source changed after freezing plan: {name}")
        command = [sys.executable, "-u", "scripts/paper_attention3d_pilot.py",
                   "--phase", "run", "--run-dir", str(RUN),
                   "--memory-fraction", "0.40", "--pretrain-patches", "256",
                   "--supervised-patches", "512", "--val-patches", "32",
                   "--eval-every", "128", "--max-seconds", "12600"]
        started = time.monotonic()
        state = {"status": "running", "supervisor_pid": os.getpid(), "started_utc": utc_now(),
                 "hard_wall_limit_seconds": 14400, "command": command, "test_files_opened": False}
        write_json(RUN / "seed_run_before.json", seed_snapshot())
        with (RUN / "training.log").open("a", buffering=1) as stream:
            child = subprocess.Popen(command, cwd=ROOT, stdin=subprocess.DEVNULL,
                                     stdout=stream, stderr=subprocess.STDOUT)
            state["training_pid"] = child.pid
            write_json(RUN / "supervisor_state.json", state)
            try:
                while child.poll() is None:
                    elapsed = time.monotonic() - started
                    if elapsed >= 14400:
                        child.terminate()
                        try:
                            child.wait(timeout=30)
                        except subprocess.TimeoutExpired:
                            child.kill()
                            child.wait()
                        state["status"] = "hard_budget_stopped"
                        break
                    state.update({"updated_utc": utc_now(), "elapsed_seconds": elapsed})
                    write_json(RUN / "supervisor_state.json", state)
                    time.sleep(15)
            finally:
                if child.poll() is None:
                    child.terminate()
                    try:
                        child.wait(timeout=30)
                    except subprocess.TimeoutExpired:
                        child.kill()
                        child.wait()
            if state["status"] == "running":
                state["status"] = "complete" if child.returncode == 0 else "failed"
            state.update({"returncode": child.returncode, "finished_utc": utc_now(),
                          "elapsed_seconds": time.monotonic() - started})
            write_json(RUN / "supervisor_state.json", state)
            write_json(RUN / "seed_run_after.json", seed_snapshot())
        if state["status"] == "complete":
            comparison = json.loads((RUN / "comparison.json").read_text())
            scratch = comparison["results"]["scratch"]["validation"]["best_threshold_metrics"]
            tuned = comparison["results"]["finetune"]["validation"]["best_threshold_metrics"]
            text = ("# Attention3D short denoising pilot\n\n"
                    "Completed a matched scratch/pretrained comparison on 32 fixed validation crops. "
                    "These are short training runs, not full-survey R100 results or a complete paper reproduction.\n\n"
                    "| Initialization | Dice | Precision | Recall | Approximate PR-AUC | Threshold |\n"
                    "|---|---:|---:|---:|---:|---:|\n")
            for label, value in [("Scratch", scratch), ("Denoising pretrained", tuned)]:
                text += f"| {label} | {value['dice']:.6f} | {value['precision']:.6f} | {value['recall']:.6f} | {value['pr_auc_approx']:.6f} | {value['threshold']:.6f} |\n"
            text += (f"\nPretrained minus scratch Dice: {comparison['dice_difference']:+.6f}. "
                     "Both use identical supervised crops and update counts; thresholds were selected separately. "
                     "A positive result supports a longer controlled run; a flat short result does not establish failure at convergence. "
                     "No test files were opened. See comparison.json for per-volume metrics and checkpoint identities.\n")
            (RUN / "report.md").write_text(text)
        print(json.dumps(state, indent=2), flush=True)


if __name__ == "__main__":
    main()
