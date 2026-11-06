#!/usr/bin/env python3
"""Run the authorized five-model pilot from training through validation analysis.

1. Train fresh seeds 45 and 46 using the existing R100 queue.
2. Add their validation predictions to the existing three-model cache.
3. Measure every subset of sizes 1, 2, 3, and 5 and draw the curve.
No stage evaluates test data. Results and process state survive this chat.
"""
import argparse
import csv
from datetime import datetime, timezone
import fcntl
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
PILOT = ROOT / "runs/R100_seed_saturation_pilot_20261019"
CACHE = ROOT / "data/cache/r100_seed_saturation_20261019"
RESULT = ROOT / "reports/evaluation/r100_seed_curve_5models_20261019"


def write_json(path, value):
    temporary = path.with_suffix(".json.part")
    temporary.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")
    temporary.replace(path)


def steps():
    python = sys.executable
    uv = shutil.which("uv")
    if uv is None:
        raise RuntimeError("The existing uv plotting environment is unavailable")
    return [
        {"name": "train_seeds_45_46", "command": [python, "-u", "scripts/run_r100_additional_seeds.py",
            "--run-root", str(PILOT.relative_to(ROOT)), "--seeds", "45", "46", "--resume-queue"]},
        {"name": "cache_new_validation_predictions", "command": [python, "-u", "scripts/cache_r100_validation.py",
            "--cache-dir", str(CACHE.relative_to(ROOT)), "--run-dirs",
            str((PILOT/"seed45").relative_to(ROOT)), str((PILOT/"seed46").relative_to(ROOT))]},
        {"name": "measure_five_model_curve", "command": [python, "-u", "scripts/analyze_r100_seed_curve.py",
            "--cache-dir", str(CACHE.relative_to(ROOT)), "--output-dir", str(RESULT.relative_to(ROOT)),
            "--sizes", "1", "2", "3", "5"]},
        {"name": "plot_curve", "command": [uv, "run", "--offline", "--with", "matplotlib", "python",
            "scripts/plot_r100_seed_curve.py", str(RESULT.relative_to(ROOT))]},
    ]


def execute_steps(directory, planned_steps, cwd):
    state = {"status": "running", "pipeline_pid": os.getpid(),
             "started_utc": datetime.now(timezone.utc).isoformat(), "active_child_pid": None,
             "test_files_opened": False, "completed_steps": []}
    state_path = directory / "pipeline_state.json"
    active = None
    def save():
        state["updated_utc"] = datetime.now(timezone.utc).isoformat()
        write_json(state_path, state)
    def interrupted(signum, _frame):
        raise KeyboardInterrupt(f"Pipeline signal {signum}")
    previous_handlers = {s: signal.signal(s, interrupted) for s in (signal.SIGINT, signal.SIGTERM)}
    try:
        for step in planned_steps:
            with (directory / f"pipeline_{step['name']}.log").open("a", buffering=1) as log:
                active = subprocess.Popen(step["command"], cwd=cwd, stdin=subprocess.DEVNULL,
                                          stdout=log, stderr=subprocess.STDOUT)
                state.update(stage=step["name"], active_child_pid=active.pid, command=step["command"], log=str(log.name))
                save()
                print(f"START {step['name']}: pid={active.pid}", flush=True)
                code = active.wait()
                active = None
                state.update(active_child_pid=None, last_exit_code=code)
                if code:
                    raise RuntimeError(f"Stage {step['name']} failed with exit code {code}; see {log.name}")
                state["completed_steps"].append(step["name"])
                save()
        state.update(status="steps_complete", stage="summarize")
        save()
        return state
    except BaseException as exc:
        if active is not None and active.poll() is None:
            active.terminate()
            try:
                active.wait(timeout=30)
            except subprocess.TimeoutExpired:
                active.kill()
                active.wait()
        state.update(status="interrupted" if isinstance(exc, KeyboardInterrupt) else "failed",
                     error=str(exc), active_child_pid=None)
        save()
        raise
    finally:
        for sig, handler in previous_handlers.items():
            signal.signal(sig, handler)


def summarize():
    result = json.loads((RESULT / "curve.json").read_text())
    if result["status"] != "complete" or result["seeds"] != [42, 43, 44, 45, 46]:
        raise RuntimeError("Five-member result is missing or incomplete")
    if result["test_files_opened"] or result["inference_performed"]:
        raise RuntimeError("Curve analysis violated the cache-only validation protocol")
    full = next(row for row in result["subset_results"] if row["seeds"] == [42,43,44,45,46])
    original = next(row for row in result["subset_results"] if row["seeds"] == [42,43,44])
    three_mean = next(row["mean_dice"] for row in result["curve"] if row["size"] == 3)
    five = full["validation"]["dice"]
    summary = {"status": "complete", "test_files_opened": False,
               "original_three_dice": original["validation"]["dice"], "five_model_dice": five,
               "gain_over_original_three": five-original["validation"]["dice"],
               "mean_three_model_dice_within_five_seed_pool": three_mean,
               "gain_over_mean_three_within_same_pool": five-three_mean,
               "decision_reference_gain": .002,
               "above_practical_gain_reference": five-three_mean >= .002,
               "note": "Exploratory validation comparison, not a statistical significance test or proof of saturation."}
    write_json(RESULT / "pilot_summary.json", summary)
    with (RESULT / "subsets.csv").open("w", newline="") as stream:
        fields = ["seeds", "size", "threshold", "dice", "iou", "precision", "recall"]
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for row in result["subset_results"]:
            writer.writerow({"seeds": ",".join(map(str,row["seeds"])), "size": row["size"],
                             "threshold": row["threshold"], **{k: row["validation"][k] for k in fields[3:]}})
    report = RESULT / "report.md"
    report.write_text(report.read_text()+f"\n## Pilot comparison\n\nOriginal three-model validation Dice: **{original['validation']['dice']:.6f}**. Five-model Dice: **{five:.6f}**. Difference: **{summary['gain_over_original_three']:+.6f}**.\n\nWithin the same five-seed pool, mean three-model Dice is {three_mean:.6f}; five-model gain over that mean is {summary['gain_over_mean_three_within_same_pool']:+.6f}. The 0.002 reference is a compute-budget heuristic, not a significance test.\n\n![Validation curve](curve.png)\n")
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    plan = json.loads((PILOT / "plan.json").read_text())
    if plan["seeds"] != [45,46] or plan["fine_tuning"] or not CACHE.joinpath("manifest.json").is_file():
        raise RuntimeError("Prepared pilot or existing cache differs")
    planned = steps()
    if args.dry_run:
        print(json.dumps(planned, indent=2))
        return
    if RESULT.exists():
        raise RuntimeError("Five-model result directory already exists; inspect before restarting")
    with (PILOT / ".pipeline.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        write_json(PILOT / "pipeline_plan.json", {"steps": planned, "seeds": [45,46],
                   "test_files_opened": False, "additional_seeds_after_46": False})
        state = execute_steps(PILOT, planned, ROOT)
        try:
            summary = summarize()
            state.update(status="complete", stage="complete", summary=summary,
                         updated_utc=datetime.now(timezone.utc).isoformat())
        except BaseException as exc:
            state.update(status="failed", stage="summarize", error=str(exc))
            raise
        finally:
            write_json(PILOT / "pipeline_state.json", state)
        print(json.dumps(summary, indent=2), flush=True)


if __name__ == "__main__":
    main()
