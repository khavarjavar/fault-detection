#!/usr/bin/env python3
"""Sequential R100 FP16 smoke followed by exactly three clean seeds.

The gate checks completion, finite saved state, common protocol and no test use.
"""
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import math
import os
from pathlib import Path
import signal
import socket
import subprocess
import sys

SEEDS = (42, 43, 44)
DEFAULT_ROOT = Path("runs") / ("R100_fp16_clean_3seeds_" + datetime.now().strftime("%Y%m%d_%H%M%S"))


def atomic_json(path, value):
    tmp = path.with_suffix(path.suffix + ".part")
    tmp.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")
    tmp.replace(path)


def now():
    return datetime.now(timezone.utc).isoformat()


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def validate_run(run_dir, seed, smoke=False, expected_protocol=None):
    # CPU checkpoint inspection. Importing torch here does not create a CUDA model.
    import torch

    torch.set_num_threads(2)
    config = json.loads((run_dir / "run_config.json").read_text())
    status = json.loads((run_dir / "status.json").read_text())
    selection = json.loads((run_dir / "validation_selection.json").read_text())
    epochs, patches, val_patches = (1, 18, 2) if smoke else (100, 360, 128)
    require(config["seed"] == seed and status["seed"] == seed, "Seed mismatch")
    require(config["smoke"] is smoke, "Smoke/training mismatch")
    require(status["status"] == ("smoke_complete" if smoke else "validation_only_complete"), "Run is incomplete")
    require(config["epochs"] == epochs and status["epochs_completed"] == epochs, "Epoch budget mismatch")
    require(config["train_patches_per_epoch"] == patches, "Training patch budget mismatch")
    require(config["validation_patches_per_epoch"] == val_patches, "Validation patch budget mismatch")
    require(config["validation_seed"] == 1042, "Validation seed changed")
    require(config["model_parameters"] == 1459585, "Model parameter count changed")
    for key, expected in {
        "model_class": "faultseg3d_baseline.FaultSeg3D", "patch_size": 128,
        "optimizer": "Adam", "learning_rate": 1e-4, "gradient_accumulation": 2,
        "loss": "ordinary BCE averaged over observed voxels",
    }.items():
        require(config[key] == expected, f"Fixed recipe field changed: {key}")
    require(config["precision"] == status["precision"] == "float16_autocast", "Precision mismatch")
    require(config["gradient_scaling"] is True and status["gradient_scaling"] is True, "Gradient scaling changed")
    require(config["test_files_read"] is False and status["test_files_read"] is False, "Test-access marker changed")
    require(not (run_dir / "final_metrics.json").exists(), "Unexpected final-test metrics in validation-only run")
    require(not (run_dir / "test_per_patch.csv").exists(), "Unexpected test results in validation-only run")
    protocol = {key: value for key, value in config.items() if key not in ("seed", "protocol_hash")}
    protocol_hash = hashlib.sha256(json.dumps(protocol, sort_keys=True).encode()).hexdigest()
    require(config["protocol_hash"] == status["protocol_hash"] == protocol_hash, "Protocol hash mismatch")
    if expected_protocol is not None:
        require(protocol_hash == expected_protocol, "Configurations differ across seeds")
    require(1 <= selection["best_epoch"] <= epochs, "Invalid best epoch")
    require(0 <= selection["threshold"] <= 1, "Invalid threshold")

    with (run_dir / "history.csv").open(newline="") as handle:
        history = list(csv.DictReader(handle))
    require([int(row["epoch"]) for row in history] == list(range(1, epochs + 1)), "History is incomplete or duplicated")
    for row in history:
        for key in ("train_loss", "val_pr_auc_approx", "val_dice"):
            require(math.isfinite(float(row[key])), f"Nonfinite history field: {key}")

    float_tensors = 0

    def finite_tree(value, path):
        nonlocal float_tensors
        if torch.is_tensor(value):
            if value.is_floating_point() or value.is_complex():
                float_tensors += 1
                for chunk in value.detach().reshape(-1).split(1_048_576):
                    require(torch.isfinite(chunk).all().item(), f"Nonfinite tensor: {path}")
        elif isinstance(value, dict):
            for key, item in value.items():
                finite_tree(item, f"{path}.{key}")
        elif isinstance(value, (list, tuple)):
            for index, item in enumerate(value):
                finite_tree(item, f"{path}[{index}]")
        elif isinstance(value, float):
            require(math.isfinite(value), f"Nonfinite number: {path}")

    finite_tree(status, "status")
    finite_tree(selection, "selection")
    for filename, expected_epoch in (("last.pt", epochs), ("best.pt", selection["best_epoch"])):
        checkpoint = torch.load(run_dir / filename, map_location="cpu", weights_only=False)
        required = {"model", "optimizer", "scaler", "epoch", "args", "validation_metrics", "python_rng", "torch_rng", "cuda_rng"}
        require(required <= checkpoint.keys(), f"Incomplete checkpoint: {filename}")
        require(checkpoint["epoch"] == expected_epoch, f"Checkpoint epoch mismatch: {filename}")
        require(checkpoint["args"]["seed"] == seed, "Checkpoint seed mismatch")
        require(checkpoint["args"]["protocol_hash"] == protocol_hash, "Checkpoint protocol mismatch")
        require(checkpoint["scaler"], "Enabled gradient scaler state is missing")
        finite_tree(checkpoint["scaler"], f"{filename}.scaler")
        require(checkpoint["optimizer"].get("state"), "Optimizer has no saved update state")
        steps = [entry.get("step", 0) for entry in checkpoint["optimizer"]["state"].values()]
        require(any(float(step) > 0 for step in steps), "Optimizer has no positive update count")
        finite_tree(checkpoint, filename)
        del checkpoint
    require(float_tensors > 0, "No floating checkpoint tensors checked")
    return {
        "seed": seed, "protocol_hash": protocol_hash,
        "best_epoch": selection["best_epoch"], "threshold": selection["threshold"],
        "validation": selection["full_validation"], "checked_float_tensors": float_tensors,
        "run_dir": str(run_dir),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--thebe-root", type=Path, default=Path("data/processed/thebe_h5"))
    parser.add_argument("--resume-queue", action="store_true")
    args = parser.parse_args()
    root = Path.cwd()
    trainer = root / "scripts/train_r100_fp16_clean.py"
    require(trainer.is_file(), "Run from the project root after installing the two new scripts")
    require(args.thebe_root.is_dir(), "Thebe directory is missing")
    (root / "runs").mkdir(exist_ok=True)
    with (root / "runs/R100_3seed_queue.lock").open("a+") as lock:
        try:
            fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise RuntimeError("Another R100 seed queue holds the project lock")

        if args.resume_queue:
            require(args.run_root.is_dir(), "Queue root is missing")
            previous = json.loads((args.run_root / "queue_status.json").read_text())
            require(previous.get("seeds") == list(SEEDS), "Seed list differs from this queue")
            child_pid = previous.get("active_child_pid")
            if child_pid:
                cmdline = Path(f"/proc/{child_pid}/cmdline")
                if cmdline.exists():
                    command = cmdline.read_bytes().replace(b"\0", b" ").decode(errors="replace")
                    require("train_r100_fp16_clean.py" not in command, "A previous trainer process is still alive; inspect it first")
        else:
            args.run_root.mkdir(parents=True, exist_ok=False)

        state = {
            "status": "starting", "started_utc": now(), "updated_utc": now(),
            "queue_pid": os.getpid(), "hostname": socket.gethostname(), "seeds": list(SEEDS),
            "rule": "exactly three completed finite matching validation-only runs",
            "test_files_read": False, "results": [], "active_child_pid": None,
        }
        active = None

        def save():
            state["updated_utc"] = now()
            atomic_json(args.run_root / "queue_status.json", state)

        def interrupted(signum, _frame):
            raise KeyboardInterrupt(f"Queue received signal {signum}")

        signal.signal(signal.SIGTERM, interrupted)
        signal.signal(signal.SIGINT, interrupted)

        def execute(run_dir, seed, smoke=False, expected_protocol=None):
            nonlocal active
            if (run_dir / "status.json").exists():
                # Completed artifacts still have to pass the full gate below.
                return
            command = [sys.executable, "-u", str(trainer), "--seed", str(seed), "--validation-seed", "1042",
                       "--thebe-root", str(args.thebe_root), "--run-dir", str(run_dir)]
            if smoke:
                command.append("--smoke")
            if expected_protocol is not None:
                command += ["--expected-protocol", expected_protocol]
            if run_dir.exists():
                require(args.resume_queue, f"Run directory already exists: {run_dir}")
                command.append("--resume")
            logfile = args.run_root / ("smoke.log" if smoke else f"seed{seed}.log")
            with logfile.open("a", buffering=1) as log:
                log.write(f"\nQUEUE LAUNCH {now()} {json.dumps(command)}\n")
                active = subprocess.Popen(command, stdout=log, stderr=subprocess.STDOUT)
                state.update(status="smoke_running" if smoke else "seed_running", active_seed=seed,
                             active_child_pid=active.pid, active_run_dir=str(run_dir), active_log=str(logfile))
                save()
                print(f"START seed={seed} smoke={smoke} pid={active.pid} log={logfile}", flush=True)
                code = active.wait()
                log.write(f"QUEUE CHILD EXIT {now()} code={code}\n")
                active = None
                state.update(active_child_pid=None, last_exit_code=code)
                save()
                require(code == 0, f"Trainer exited with code {code}; see {logfile}")

        try:
            save()
            smoke_dir = args.run_root / "smoke_seed42"
            execute(smoke_dir, 42, smoke=True)
            validate_run(smoke_dir, 42, smoke=True)
            state["smoke_passed"] = True
            expected_protocol = None
            for seed in SEEDS:
                run_dir = args.run_root / f"seed{seed}"
                execute(run_dir, seed, expected_protocol=expected_protocol)
                result = validate_run(run_dir, seed, expected_protocol=expected_protocol)
                expected_protocol = result["protocol_hash"]
                state["results"].append(result)
                state.update(status="seed_verified", completed_seeds=[r["seed"] for r in state["results"]])
                save()
                print(f"PASS seed={seed} validation_dice={result['validation']['dice']:.6f}", flush=True)
            dice = [item["validation"]["dice"] for item in state["results"]]
            mean = sum(dice) / len(dice)
            sd = math.sqrt(sum((value-mean)**2 for value in dice)/(len(dice)-1))
            state.update(status="three_seeds_complete", validation_dice_mean=mean, validation_dice_sample_sd=sd)
            save()
            print(f"THREE SEEDS COMPLETE validation Dice mean={mean:.6f} sample_SD={sd:.6f}; no test evaluation", flush=True)
        except BaseException as exc:
            if active is not None and active.poll() is None:
                active.terminate()
                try:
                    active.wait(timeout=15)
                except subprocess.TimeoutExpired:
                    active.kill()
                    active.wait()
            state.update(status="interrupted" if isinstance(exc, KeyboardInterrupt) else "failed",
                         error=repr(exc), active_child_pid=None)
            save()
            raise


if __name__ == "__main__":
    main()
