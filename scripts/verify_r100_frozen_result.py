#!/usr/bin/env python3
"""Check saved R100 evidence using NumPy and CSV; never run model inference."""
import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

import numpy as np


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("result_dir", type=Path)
    args = parser.parse_args()
    directory = args.result_dir.resolve()
    root = Path(__file__).resolve().parents[1]
    result = json.loads((directory / "final_metrics.json").read_text())
    protocol = json.loads((directory / "protocol.json").read_text())
    frozen = json.loads((directory / "ORIGINAL_FROZEN_MANIFEST.json").read_text())
    reproduction = json.loads((directory / "validation_reproduction.json").read_text())
    require(result["status"] == "complete_official_test", "Evaluation did not complete")
    require(not result["training_performed"] and not result["thresholds_retuned"], "Training or retuning recorded")
    require(reproduction["status"] == "exact_reproduction" and not reproduction["test_files_opened"], "Validation gate failed")
    thresholds = {f"seed{s}": frozen["member_thresholds"][str(s)] for s in (42, 43, 44)}
    thresholds["ensemble"] = frozen["threshold"]
    require(result["thresholds"] == thresholds == protocol["thresholds"], "Thresholds changed")
    for seed in (42, 43, 44):
        checkpoint = root / f"runs/R100_fp16_clean_3seeds_20261014_150435/seed{seed}/best.pt"
        require(digest(checkpoint) == frozen["checkpoint_hashes"][str(seed)], "Checkpoint changed")
    for relative, expected in protocol["source_hashes"].items():
        require(digest(directory / "source_snapshot" / relative) == expected, "Source snapshot hash mismatch")
    reference = root / "reports/evaluation/r100_ensemble_e0_20261016T120152Z/validation_histograms_2048_bins.npz"
    require(digest(reference) == protocol["validation_reference_sha256"], "Validation reference changed")
    with np.load(reference) as old, np.load(directory / "val_histograms_2048_bins.npz") as new:
        require(set(old.files) == set(new.files), "Validation histogram schema changed")
        for key in old.files:
            require(np.array_equal(old[key], new[key]), f"Validation differs: {key}")
    with (directory / "test_per_patch.csv").open(newline="") as stream:
        rows = list(csv.DictReader(stream))
    coverage = result["test"]["coverage"]
    require(coverage["shape"] == [703, 3174, 1537], "Wrong test geometry")
    require(coverage["patches"] == 1950 and coverage["observed_patches"] == 1382, "Wrong test tile counts")
    require(coverage["valid_voxels"] == 2_303_341_553, "Wrong scoring population")
    require(coverage["raw_voxels"] == 3_429_541_914, "Wrong raw coverage")
    require(len(rows) == 4 * coverage["observed_patches"], "Missing per-patch evidence")
    deltas = {}
    with np.load(directory / "test_histograms_2048_bins.npz") as hist:
        for name, threshold in thresholds.items():
            p, n = hist[f"{name}_positive"], hist[f"{name}_negative"]
            require(np.all(p >= 0) and np.all(n >= 0), "Negative histogram count")
            require(np.all(p == np.floor(p)) and np.all(n == np.floor(n)), "Noninteger histogram count")
            b = int(threshold * 2048)
            tp, fp, fn, tn = p[b:].sum(), n[b:].sum(), p[:b].sum(), n[:b].sum()
            require(tp+fp+fn+tn == coverage["valid_voxels"], "Histogram coverage mismatch")
            require(tp+fn == 57_680_496, "Positive-label count mismatch")
            selected = [r for r in rows if r["model"] == name]
            require(len(selected) == coverage["observed_patches"], "Missing model rows")
            require(len({r["patch_id"] for r in selected}) == len(selected), "Duplicate tile scored")
            for key, expected in (("tp", tp), ("fp", fp), ("fn", fn), ("tn", tn)):
                require(sum(int(r[key]) for r in selected) == expected, f"CSV {name}/{key} mismatch")
            require(sum(int(r["raw_voxels"]) for r in selected) <= coverage["raw_voxels"], "CSV raw count overflow")
            require(sum(int(r["valid_voxels"]) for r in selected) == coverage["valid_voxels"], "CSV valid count mismatch")
            for row in selected:
                require(int(row["tp"])+int(row["fn"]) == int(row["positive_voxels"]), "Patch label count mismatch")
                require(float(row["threshold"]) == threshold, "Patch threshold changed")
            ct, cf = np.cumsum(p[::-1]), np.cumsum(n[::-1])
            recall = ct / p.sum()
            precision = ct / np.maximum(ct+cf, 1e-12)
            calculated = {
                "tp": tp, "fp": fp, "fn": fn, "tn": tn,
                "dice": 2*tp/(2*tp+fp+fn), "iou": tp/(tp+fp+fn),
                "precision": tp/(tp+fp), "recall": tp/(tp+fn),
                "specificity": tn/(tn+fp), "accuracy": (tp+tn)/(tp+fp+fn+tn),
                "balanced_accuracy": .5*(tp/(tp+fn)+tn/(tn+fp)),
                "mcc": (tp*tn-fp*fn)/np.sqrt((tp+fp)*(tp+fn)*(tn+fp)*(tn+fn)),
                "pr_auc_approx": np.sum(np.diff(np.r_[0., recall])*precision),
                "roc_auc_approx": np.trapezoid(np.r_[0., recall], np.r_[0., cf/n.sum()]),
            }
            reported = result["test"]["metrics"][name]
            require(reported["threshold"] == threshold, "Final threshold changed")
            deltas[name] = max(abs(float(value)-reported[key]) for key, value in calculated.items())
            require(deltas[name] < 1e-12, f"Independent metric calculation differs: {name}")
    for key, summary in result["seed_summary"].items():
        values = [result["test"]["metrics"][f"seed{s}"][key] for s in (42, 43, 44)]
        require(abs(np.mean(values)-summary["mean"]) < 1e-12, "Seed mean differs")
        require(abs(np.std(values, ddof=1)-summary["sample_sd"]) < 1e-12, "Seed SD differs")
    verified = {"status": "passed", "verified_utc": datetime.now(timezone.utc).isoformat(),
                "inference_performed": False, "checkpoint_and_snapshot_hashes": "match",
                "validation_histograms": "exact_match", "test_csv_rows": len(rows),
                "scored_voxels_per_model": coverage["valid_voxels"],
                "independent_numpy_maximum_metric_delta": deltas,
                "seed_mean_and_sample_sd": "match", "verifier_sha256": digest(Path(__file__))}
    (directory / "verification.json").write_text(json.dumps(verified, indent=2) + "\n")
    print(json.dumps(verified, indent=2))


if __name__ == "__main__":
    main()
