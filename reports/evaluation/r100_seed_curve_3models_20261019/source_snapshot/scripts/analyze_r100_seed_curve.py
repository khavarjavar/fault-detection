#!/usr/bin/env python3
"""Measure validation Dice versus ensemble size using cached probabilities.

No models or seismic files are opened. For each subset, average probabilities,
select its validation threshold, and record apparent validation Dice. Error bars
describe variation among subsets of the available seed pool, not survey-level CI.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict
from datetime import datetime, timezone
import fcntl
import itertools
import json
import math
from pathlib import Path
import random
import time

import numpy as np
import torch

from cache_r100_validation import ROOT, read_json, sha256, verify_cache_file
import faultseg3d_baseline as baseline


def choose_subsets(pool_size, sizes, maximum, seed):
    """Use all combinations when small, otherwise sample unique subsets."""
    if maximum < 1:
        raise ValueError("Subset limit must be positive")
    rng = random.Random(seed)
    groups = []
    for size in sizes:
        if size < 1 or size > pool_size:
            raise ValueError(f"Cannot select {size} models from {pool_size}")
        count = math.comb(pool_size, size)
        if count <= maximum:
            selected = list(itertools.combinations(range(pool_size), size))
        else:
            selected = set()
            while len(selected) < maximum:
                selected.add(tuple(sorted(rng.sample(range(pool_size), size))))
            selected = sorted(selected)
        groups.extend(selected)
    return groups


@torch.inference_mode()
def score_subsets(maps, labels, groups, device, block_size, progress=None):
    """Read each map block once; reuse it for all selected combinations."""
    histograms = [baseline.ProbabilityHistogram(2048) for _ in groups]
    for start in range(0, len(labels), block_size):
        stop = min(start+block_size, len(labels))
        predictions = torch.from_numpy(np.stack([array[start:stop] for array in maps])).to(device)
        target = torch.from_numpy(np.array(labels[start:stop], dtype="float32")).to(device)
        if (not torch.isfinite(predictions).all() or (predictions < 0).any()
                or (predictions > 1).any() or ((target != 0) & (target != 1)).any()):
            raise RuntimeError("Invalid cached probability or label")
        for group, histogram in zip(groups, histograms, strict=True):
            probability = predictions[list(group)].mean(dim=0)
            histogram.update_probabilities(probability, target)
        if progress is not None:
            progress(stop, len(labels))
    return histograms


def summarize(rows):
    results = []
    for size in sorted({row["size"] for row in rows}):
        selected = [row for row in rows if row["size"] == size]
        dice = np.array([row["validation"]["dice"] for row in selected])
        results.append({"size": size, "subsets": len(selected), "mean_dice": float(dice.mean()),
                        "subset_sample_sd": float(dice.std(ddof=1)) if len(dice) > 1 else None,
                        "minimum_dice": float(dice.min()), "maximum_dice": float(dice.max()),
                        "median_threshold": float(np.median([r["threshold"] for r in selected]))})
    return results


def report_text(result):
    text = ["# R100 validation ensemble-size measurement", "",
            f"Available clean seeds: {', '.join(map(str, result['seeds']))}.", "",
            "This is a validation-only measurement. Every combination selects its own threshold on the same full validation data it scores. These are apparent validation scores, not held-out performance estimates.", "",
            "| Models averaged | Subsets measured | Mean validation Dice | Subset sample SD | Min | Max |",
            "|---:|---:|---:|---:|---:|---:|"]
    for row in result["curve"]:
        sd = "not estimable (one subset)" if row["subset_sample_sd"] is None else f"{row['subset_sample_sd']:.6f}"
        text.append(f"| {row['size']} | {row['subsets']} | {row['mean_dice']:.6f} | {sd} | {row['minimum_dice']:.6f} | {row['maximum_dice']:.6f} |")
    text += ["", "Subset SD describes sensitivity to which models are selected from this finite pool. Combinations share models and are correlated; the bars are not confidence intervals across new surveys or newly trained seed pools. A single full-pool ensemble does not establish zero uncertainty.", "",
             f"This result is conditional on the {len(result['seeds'])} available seeds. It cannot establish performance at larger sizes than that pool. Three seeds alone cannot establish saturation at eight, ten, or forty.", "",
             "The analysis reads FP32 cached probabilities and labels; it performs arithmetic and histogram scoring, without neural-network inference, training, or opening Thebe HDF5 files. No test evaluation occurs.", "",
             "Keep flip TTA, alternative losses, overlap inference, and checkpoint/weight averaging in separately named experiments. They change factors beyond seed count.", ""]
    return "\n".join(text)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--sizes", nargs="+", type=int, default=None)
    parser.add_argument("--max-subsets", type=int, default=32)
    parser.add_argument("--subset-seed", type=int, default=1042)
    parser.add_argument("--block-size", type=int, default=1_048_576)
    args = parser.parse_args()
    if args.output_dir.exists():
        raise RuntimeError("Output directory already exists")
    if args.block_size < 1:
        raise ValueError("Block size must be positive")
    torch.set_num_threads(4)
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA required for scoring full-volume combinations")
    baseline.seed_everything(42)
    cache_lock = (args.cache_dir / ".lock").open("a")
    fcntl.flock(cache_lock, fcntl.LOCK_SH | fcntl.LOCK_NB)
    manifest = read_json(args.cache_dir / "manifest.json")
    if manifest["status"] != "complete" or manifest["test_files_opened"]:
        raise RuntimeError("Cache is not a completed validation-only cache")
    seeds = sorted(map(int, manifest["members"]))
    maps = [verify_cache_file(args.cache_dir / manifest["members"][str(s)]["probabilities_file"],
                              manifest["members"][str(s)]["probabilities_sha256"], "float32") for s in seeds]
    labels = verify_cache_file(args.cache_dir / manifest["labels_file"], manifest["labels_sha256"], "uint8")
    sizes = sorted(set(args.sizes if args.sizes is not None else [n for n in (1, 2, 3, 5, 8, 10) if n <= len(seeds)]))
    groups = choose_subsets(len(seeds), sizes, args.max_subsets, args.subset_seed)
    args.output_dir.mkdir(parents=True, exist_ok=False)
    from train_r100_fp16_clean import write_json_atomic
    write_json_atomic(args.output_dir / "cache_manifest.json", manifest)
    groups_json = [[seeds[index] for index in group] for group in groups]
    frozen = {"status": "validation_analysis_frozen", "seeds": seeds, "subsets": groups_json,
              "cache_manifest_sha256": sha256(args.output_dir / "cache_manifest.json"),
              "subset_seed": args.subset_seed, "max_subsets_per_size": args.max_subsets,
              "threshold_policy": "best Dice on full validation separately for each subset",
              "test_files_opened": False, "inference_performed": False,
              "analysis_source_sha256": sha256(Path(__file__))}
    write_json_atomic(args.output_dir / "analysis_plan.json", frozen)
    started = time.monotonic()
    last_output = 0.0
    def progress(done, total):
        nonlocal last_output
        elapsed = time.monotonic()-started
        if elapsed-last_output >= 15 or done == total:
            state = {"status": "running", "voxels_scored": done, "total_voxels": total,
                     "subsets": len(groups), "elapsed_seconds": elapsed, "test_files_opened": False}
            write_json_atomic(args.output_dir / "progress.json", state)
            print(f"cached subset scoring {done:,}/{total:,}; minutes={elapsed/60:.1f}", flush=True)
            last_output = elapsed
    histograms = score_subsets(maps, labels, groups, torch.device("cuda"), args.block_size, progress)
    rows = []
    for group, histogram in zip(groups_json, histograms, strict=True):
        if int(histogram.positive.sum()) != manifest["positive_voxels"] or int(histogram.positive.sum()+histogram.negative.sum()) != len(labels):
            raise RuntimeError("Subset histogram coverage differs from cache")
        threshold = histogram.best_dice_threshold()
        row = {"seeds": group, "size": len(group), "threshold": threshold,
               "validation": asdict(histogram.metrics(threshold)), "at_0_5": asdict(histogram.metrics(.5))}
        if len(group) == 1:
            expected = manifest["members"][str(group[0])]["validation_selection"]["full_validation"]
            if row["validation"] != expected:
                raise RuntimeError("Cached single-member result differs from frozen selection")
        if group == [42, 43, 44]:
            reference_path = ROOT / "reports/evaluation/r100_ensemble_e0_20261016T120152Z/validation_histograms_2048_bins.npz"
            with np.load(reference_path) as old:
                if not all(np.array_equal(getattr(histogram, kind).numpy(), old[f"ensemble_{kind}"])
                           for kind in ("positive", "negative")):
                    raise RuntimeError("Cached three-seed ensemble histogram differs from the frozen reference")
            row["original_three_seed_exact"] = True
        rows.append(row)
    result = {**frozen, "status": "complete", "completed_utc": datetime.now(timezone.utc).isoformat(),
              "curve": summarize(rows), "subset_results": rows, "wall_seconds": time.monotonic()-started}
    write_json_atomic(args.output_dir / "curve.json", result)
    (args.output_dir / "report.md").write_text(report_text(result))
    write_json_atomic(args.output_dir / "progress.json", {"status": "complete", "test_files_opened": False})
    print(report_text(result), flush=True)
    cache_lock.close()


if __name__ == "__main__":
    main()
