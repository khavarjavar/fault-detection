#!/usr/bin/env python3
"""Evaluate the frozen R100 seeds and probability ensemble, without training.

Full saved validation histograms must reproduce exactly before test HDF5
files are opened. Thresholds come from the existing frozen manifest; this
program never selects a threshold. Run with the project's .venv_train.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import math
from pathlib import Path
import shutil
import sys
import time
import traceback

import numpy as np
import torch

import train_r100_fp16_clean as r100


ROOT = Path(__file__).resolve().parents[1]
RUN = Path("runs/R100_fp16_clean_3seeds_20261014_150435")
REFERENCE = Path("reports/evaluation/r100_ensemble_e0_20261016T120152Z")
SAM_PROTOCOL = Path(
    "reports/evaluation/sammed3d_frozen_thebe_20261016T011856768228130Z/protocol.json"
)
SEEDS = (42, 43, 44)
NAMES = tuple(f"seed{seed}" for seed in SEEDS) + ("ensemble",)
SPLITS = {
    "val": {
        "files": 2, "shape": (200, 3174, 1537), "patches": 650,
        "valid_voxels": 613_738_550, "positive_voxels": 17_128_496,
        "positive_labels_excluded": 23_514,
    },
    "test": {
        "files": 7, "shape": (703, 3174, 1537), "patches": 1950,
        "valid_voxels": 2_303_341_553, "positive_voxels": 57_680_496,
        "positive_labels_excluded": 34_415,
    },
}


def read_json(path):
    return json.loads(Path(path).read_text())


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(8 * 1024**2), b""):
            digest.update(block)
    return digest.hexdigest()


def file_metadata(path):
    stat = Path(path).stat()
    return {"bytes": stat.st_size, "mtime_ns": stat.st_mtime_ns}


def json_write(path, value):
    r100.write_json_atomic(Path(path), value)


def check_shape(split, shape):
    expected = SPLITS[split]["shape"]
    if tuple(shape) != expected:
        raise RuntimeError(f"Unexpected {split} shape: {shape}; expected {expected}")


def check_coverage(split, coverage, histograms):
    expected = SPLITS[split]
    for key in ("patches", "valid_voxels", "positive_voxels", "positive_labels_excluded"):
        if coverage[key] != expected[key]:
            raise RuntimeError(f"{split} {key}: {coverage[key]} != {expected[key]}")
    if coverage["raw_voxels"] != math.prod(expected["shape"]):
        raise RuntimeError(f"Incomplete {split} raw-voxel coverage")
    for name, hist in histograms.items():
        positive = float(hist.positive.sum())
        negative = float(hist.negative.sum())
        if positive != expected["positive_voxels"] or positive + negative != expected["valid_voxels"]:
            raise RuntimeError(f"{split}/{name}: histogram counts disagree with coverage")


def compare_histograms(histograms, reference_path):
    """Exact counts per bin, stronger than a rounded Dice comparison."""
    comparison = {}
    with np.load(reference_path, allow_pickle=False) as reference:
        for name, hist in histograms.items():
            comparison[name] = {}
            for kind in ("positive", "negative"):
                actual = getattr(hist, kind).cpu().numpy()
                expected = reference[f"{name}_{kind}"]
                if not np.array_equal(actual, expected):
                    delta = np.abs(actual - expected)
                    raise RuntimeError(
                        f"Validation histogram mismatch: {name}/{kind}; "
                        f"max count delta={delta.max()}, changed bins={np.count_nonzero(delta)}. "
                        "Test files remain unopened."
                    )
                comparison[name][kind] = {"exact_match": True, "bins": len(actual)}
    return comparison


def compare_metrics(actual, expected, label):
    if set(actual) != set(expected):
        raise RuntimeError(f"Metric schema mismatch: {label}")
    for key, value in actual.items():
        if not math.isclose(value, expected[key], rel_tol=0.0, abs_tol=1e-12):
            raise RuntimeError(f"Metric mismatch: {label}/{key}: {value} != {expected[key]}")


def preflight():
    """Only stat test files here; do not open their HDF5 contents."""
    frozen = read_json(ROOT / REFERENCE / "FROZEN_BEFORE_TEST.json")
    old_validation = read_json(ROOT / REFERENCE / "validation_result.json")
    if frozen["status"] != "frozen_before_test" or frozen["threshold"] != old_validation["threshold"]:
        raise RuntimeError("Missing or inconsistent frozen ensemble threshold")
    thresholds = {f"seed{s}": float(frozen["member_thresholds"][str(s)]) for s in SEEDS}
    thresholds["ensemble"] = float(frozen["threshold"])
    if any(not 0 < t < 1 or t * r100.BINS != int(t * r100.BINS) for t in thresholds.values()):
        raise RuntimeError("Frozen thresholds must lie on the original 2048-bin grid")
    configs, selections, sources, checksums = {}, {}, {}, {}
    for seed in SEEDS:
        directory = ROOT / RUN / f"seed{seed}"
        config = read_json(directory / "run_config.json")
        selection = read_json(directory / "validation_selection.json")
        status = read_json(directory / "status.json")
        if (config["seed"] != seed or config["smoke"] or config["epochs"] != 100
                or config["precision"] != "float16_autocast"
                or config["protocol_hash"] != frozen["protocol_hash"]
                or status["status"] != "validation_only_complete"
                or status["epochs_completed"] != 100 or status["test_files_read"]):
            raise RuntimeError(f"Seed {seed} is not the expected completed frozen run")
        protocol = {k: v for k, v in config.items() if k not in ("seed", "protocol_hash")}
        actual_protocol = hashlib.sha256(json.dumps(protocol, sort_keys=True).encode()).hexdigest()
        if actual_protocol != frozen["protocol_hash"]:
            raise RuntimeError(f"Seed {seed}: saved protocol fingerprint is inconsistent")
        if selection["threshold"] != thresholds[f"seed{seed}"]:
            raise RuntimeError(f"Seed {seed}: threshold changed")
        if selection["best_epoch"] != status["best_epoch"]:
            raise RuntimeError(f"Seed {seed}: best epoch inconsistent")
        compare_metrics(selection["full_validation"],
                        old_validation["members_reproduced"][str(seed)]["metrics"], f"seed{seed}")
        with (directory / "history.csv").open(newline="") as stream:
            history = list(csv.DictReader(stream))
        if [int(row["epoch"]) for row in history] != list(range(1, 101)):
            raise RuntimeError(f"Seed {seed}: incomplete history")
        best_epoch = int(max(history, key=lambda row: float(row["val_pr_auc_approx"]))["epoch"])
        if best_epoch != selection["best_epoch"]:
            raise RuntimeError(f"Seed {seed}: checkpoint selection does not match history")
        expected_sources = {**config["source_hashes"], "scripts/train_r100_fp16_clean.py": config["trainer_sha256"]}
        for relative, expected in expected_sources.items():
            if sha256(ROOT / relative) != expected:
                raise RuntimeError(f"Frozen helper source changed: {relative}")
            sources[relative] = expected
        for relative, expected in config["data_file_metadata"].items():
            if file_metadata(ROOT / relative) != expected:
                raise RuntimeError(f"Training/validation data fingerprint changed: {relative}")
        checksums[str(seed)] = sha256(directory / "best.pt")
        if checksums[str(seed)] != frozen["checkpoint_hashes"][str(seed)]:
            raise RuntimeError(f"Frozen checkpoint changed: seed {seed}")
        configs[seed], selections[seed] = config, selection
    if any(config != {**configs[42], "seed": seed} for seed, config in configs.items()):
        raise RuntimeError("Seeds have different protocols")
    data_root = ROOT / "data/processed/thebe_h5"
    split_files = {split: r100.split_paths(data_root, split, spec["files"])
                   for split, spec in SPLITS.items()}
    all_paths = [path for paths in split_files.values() for path in paths]
    train_paths = [ROOT / path for path in configs[42]["train_files"]]
    if len({p.resolve() for p in all_paths + train_paths}) != len(all_paths + train_paths):
        raise RuntimeError("Training, validation, or test files overlap")
    if len({(p.stat().st_dev, p.stat().st_ino) for p in all_paths + train_paths}) != len(all_paths + train_paths):
        raise RuntimeError("Dataset split contains aliased hardlinks")
    # Test size/mtime fingerprints already existed in the prior SAM evaluation.
    test_reference = {item["path"]: {k: item[k] for k in ("bytes", "mtime_ns")}
                      for item in read_json(ROOT / SAM_PROTOCOL)["data_files"]
                      if Path(item["path"]).name.startswith("test")}
    for path in split_files["test"]:
        if file_metadata(path) != test_reference.get(str(path.relative_to(ROOT))):
            raise RuntimeError(f"Test data fingerprint changed: {path}")
    if str(torch.__version__) != configs[42]["torch_version"] or torch.version.cuda != configs[42]["torch_cuda_build"]:
        raise RuntimeError("PyTorch/CUDA build changed from the training environment")
    return frozen, old_validation, thresholds, configs, selections, split_files, sources


def load_models(configs, selections):
    models = {}
    for seed in SEEDS:
        saved = torch.load(ROOT / RUN / f"seed{seed}/best.pt", map_location="cpu", weights_only=False)
        if (saved["epoch"] != selections[seed]["best_epoch"]
                or saved["args"]["seed"] != seed
                or saved["args"]["protocol_hash"] != configs[seed]["protocol_hash"]):
            raise RuntimeError(f"Checkpoint metadata mismatch: seed {seed}")
        r100.assert_finite_tree(saved["model"], f"seed{seed}.model")
        model = r100.baseline.FaultSeg3D()
        if r100.baseline.count_parameters(model) != 1_459_585:
            raise RuntimeError("Unexpected model parameter count")
        model.load_state_dict(saved["model"], strict=True)
        models[f"seed{seed}"] = model.cuda().eval().requires_grad_(False)
    return models


def save_histograms(path, histograms):
    np.savez_compressed(path, **{f"{name}_{kind}": getattr(hist, kind).cpu().numpy()
                               for name, hist in histograms.items() for kind in ("positive", "negative")})


@torch.inference_mode()
def evaluate_split(split, paths, models, thresholds, output, progress):
    reader = r100.ConcatenatedThebe(paths)
    started = time.monotonic()
    histograms = {name: r100.baseline.ProbabilityHistogram(r100.BINS) for name in NAMES}
    coverage = {"shape": list(reader.shape), "patches": 0, "observed_patches": 0,
                "no_data_patches": 0, "constant_observed_patches": 0, "raw_voxels": 0,
                "valid_voxels": 0, "positive_voxels": 0, "positive_labels_excluded": 0}
    rows = []
    try:
        check_shape(split, reader.shape)
        coordinates = r100.tiling(reader.shape)
        if len(coordinates) != SPLITS[split]["patches"]:
            raise RuntimeError(f"Unexpected {split} tile count")
        for number, origin in enumerate(coordinates, 1):
            x, target, mask, shape, observed, excluded, constant = r100.read_patch(reader, origin)
            if x.shape != (1, 1, 128, 128, 128) or target.shape != x.shape or mask.shape != x.shape:
                raise RuntimeError(f"Malformed tensors at {split}/{origin}")
            if observed != int(mask.sum()) or observed > math.prod(shape):
                raise RuntimeError(f"Invalid scoring mask at {split}/{origin}")
            r100.assert_finite_tree(x, "normalized_input")
            positive = int(target[mask].sum())
            coverage["patches"] += 1
            coverage["raw_voxels"] += math.prod(shape)
            coverage["valid_voxels"] += observed
            coverage["positive_voxels"] += positive
            coverage["positive_labels_excluded"] += excluded
            coverage["constant_observed_patches"] += int(constant and observed > 0)
            common = {"patch_id": "x%04d_y%04d_z%04d" % origin,
                      "x": origin[0], "y": origin[1], "z": origin[2],
                      "raw_voxels": math.prod(shape), "valid_voxels": observed,
                      "positive_voxels": positive, "positive_labels_excluded": excluded}
            if observed:
                coverage["observed_patches"] += 1
                x, target, mask = x.cuda(), target.cuda(), mask.cuda()
                probabilities = []
                for name, model in models.items():
                    with torch.autocast("cuda", dtype=torch.float16):
                        logits = model(x)
                    # Check logits too: sigmoid(inf) would otherwise look finite.
                    r100.assert_finite_tree(logits, f"{split}/{name}.logits")
                    probabilities.append(torch.sigmoid(logits.float()))
                # Equal-weight arithmetic mean of FP32 probabilities in seed order.
                probabilities.append(torch.stack(probabilities, dim=0).mean(dim=0))
                scored_target = target[mask]
                for name, probability in zip(NAMES, probabilities, strict=True):
                    scored = probability[mask]
                    patch_hist = r100.baseline.ProbabilityHistogram(r100.BINS)
                    patch_hist.update_probabilities(scored, scored_target)
                    histograms[name].positive += patch_hist.positive
                    histograms[name].negative += patch_hist.negative
                    metrics = asdict(patch_hist.metrics(thresholds[name]))
                    if split == "test":
                        # Single-class patch AUC is undefined, not zero evidence.
                        if positive == 0 or positive == observed:
                            metrics["roc_auc_approx"] = None
                        if positive == 0:
                            metrics["pr_auc_approx"] = None
                        rows.append({**common, "model": name, **metrics})
                del probabilities, scored, scored_target, logits, x, target, mask
            else:
                coverage["no_data_patches"] += 1
            if number % 25 == 0 or number == len(coordinates):
                progress.update(stage=split, patches_processed=number, patches_planned=len(coordinates),
                                observed_patches=coverage["observed_patches"],
                                elapsed_seconds=time.monotonic() - started)
                json_write(output / "progress.json", progress)
                print(f"{split}: {number}/{len(coordinates)}; observed={coverage['observed_patches']}; "
                      f"minutes={(time.monotonic()-started)/60:.1f}", flush=True)
    finally:
        reader.close()
    coverage["excluded_no_data_voxels"] = coverage["raw_voxels"] - coverage["valid_voxels"]
    check_coverage(split, coverage, histograms)
    metrics = {name: asdict(hist.metrics(thresholds[name])) for name, hist in histograms.items()}
    r100.assert_finite_tree(metrics, f"{split}.metrics")
    save_histograms(output / f"{split}_histograms_2048_bins.npz", histograms)
    result = {"split": split, "complete_coverage": True, "coverage": coverage,
              "metrics": metrics, "wall_seconds": time.monotonic()-started}
    if rows:
        r100.write_csv_atomic(output / "test_per_patch.csv", rows)
        result["patch_dice_summary"] = patch_summary(rows)
    return result, histograms


def patch_summary(rows):
    summary = {}
    for name in NAMES:
        selected = [r for r in rows if r["model"] == name]
        summary[name] = {}
        for group in ("all_observed", "fault_present", "fault_absent"):
            subset = [r for r in selected if group == "all_observed"
                      or (r["positive_voxels"] > 0) == (group == "fault_present")]
            values = np.asarray([r["dice"] for r in subset], dtype=np.float64)
            summary[name][group] = {"patches": len(subset),
                                   "mean_dice": float(values.mean()) if len(values) else None,
                                   "median_dice": float(np.median(values)) if len(values) else None,
                                   "fp": sum(r["fp"] for r in subset)}
    return summary


def seed_summary(test):
    return {metric: {"mean": float(np.mean([test["metrics"][f"seed{s}"][metric] for s in SEEDS])),
                     "sample_sd": float(np.std([test["metrics"][f"seed{s}"][metric] for s in SEEDS], ddof=1))}
            for metric in test["metrics"]["seed42"] if metric not in ("threshold", "tp", "fp", "fn", "tn")}


def report_text(result):
    lines = ["# Frozen clean R100 three-seed and ensemble test evaluation", "",
             f"Completed UTC: {result['completed_utc']}", "",
             "All three seeds and the ensemble reproduced every saved full-validation histogram bin exactly before test HDF5 files were opened. Checkpoints and thresholds match the pre-existing frozen manifest. No training, checkpoint selection, threshold search, test-time augmentation, or overlapping inference was performed.", "",
             "| Model | Best epoch | Frozen threshold | Test Dice | IoU | Precision | Recall | PR-AUC approx. | ROC-AUC approx. |",
             "|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for name in NAMES:
        m = result["test"]["metrics"][name]
        epoch = str(result["best_epochs"][name]) if name != "ensemble" else "—"
        lines.append(f"| {name} | {epoch} | {m['threshold']:.9f} | {m['dice']:.6f} | {m['iou']:.6f} | {m['precision']:.6f} | {m['recall']:.6f} | {m['pr_auc_approx']:.6f} | {m['roc_auc_approx']:.6f} |")
    d = result["seed_summary"]["dice"]
    c = result["test"]["coverage"]
    lines.extend(["", f"Three-seed test Dice: **{d['mean']:.6f} ± {d['sample_sd']:.6f}** (sample SD). Ensemble is reported separately.", "",
                  f"Test geometry: `{tuple(c['shape'])}`; {c['patches']:,} tiles, {c['observed_patches']:,} observed tiles, {c['raw_voxels']:,} raw voxels, **{c['valid_voxels']:,} scored voxels**. Excluded no-data/padding does not enter metrics; {c['positive_labels_excluded']:,} positive labels lie outside the raw-nonzero validity mask.", "",
                  "The ensemble is the equal-weight mean of FP32 probabilities from FP16-autocast inference in seed order 42, 43, 44. Each individual threshold and the ensemble threshold came from the previous full-validation selections. Metrics pool voxel counts; AUC uses the original 2048 bins. Per-patch CSV excludes no-data tiles, includes fault-free observed tiles, and marks undefined single-class ROC-AUC/no-positive PR-AUC as blank. Patch Dice follows the historical formula (both-empty Dice is zero); it is supplementary to pooled Dice.", "",
                  "This evaluates the existing Thebe test split, previously inspected for other experiments. Seed SD measures training variation on this split, not independent-survey generalization. Data fingerprints are size/mtime records plus unchanged source/checkpoint hashes, not new full-volume data hashes. Structural-distance metrics were not computed.", "",
                  "Evidence: `final_metrics.json`, `validation_reproduction.json`, `FROZEN_BEFORE_TEST.json`, `protocol.json`, `test_per_patch.csv`, validation/test histograms, `source_snapshot/`, and `console.log`.", ""])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True, help="Must not already exist")
    parser.add_argument("--validation-only", action="store_true", help="Reproduce validation; never open test HDF5")
    args = parser.parse_args()
    output = args.output_dir.resolve()
    if output.exists():
        raise RuntimeError(f"Refusing to overwrite existing output: {output}")
    lock_path = ROOT / "runs/R100_frozen_test_evaluation.lock"
    with lock_path.open("a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise RuntimeError("Another frozen R100 evaluation is running") from exc
        output.mkdir(parents=True, exist_ok=False)
        progress = {"status": "running", "stage": "preflight", "test_files_opened": False,
                    "started_utc": datetime.now(timezone.utc).isoformat()}
        json_write(output / "progress.json", progress)
        with (output / "console.log").open("x", buffering=1) as log:
            class Tee:
                def __init__(self, original): self.original = original
                def write(self, value): self.original.write(value); log.write(value)
                def flush(self): self.original.flush(); log.flush()
            original_stdout, original_stderr = sys.stdout, sys.stderr
            sys.stdout, sys.stderr = Tee(sys.stdout), Tee(sys.stderr)
            try:
                frozen, prior_val, thresholds, configs, selections, paths, sources = preflight()
                if not torch.cuda.is_available() or torch.cuda.mem_get_info()[0] < 4 * 1024**3:
                    raise RuntimeError("CUDA with at least 4 GiB free memory required")
                if torch.cuda.get_device_name() != configs[42]["gpu_name"]:
                    raise RuntimeError("GPU model differs from original training")
                torch.set_num_threads(4)
                r100.baseline.seed_everything(42)
                torch.cuda.reset_peak_memory_stats()
                models = load_models(configs, selections)
                source_paths = [Path(__file__).resolve(), *(ROOT / path for path in sources)]
                for path in source_paths:
                    destination = output / "source_snapshot" / path.relative_to(ROOT)
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(path, destination)
                for seed in SEEDS:
                    for filename in ("run_config.json", "status.json", "validation_selection.json"):
                        destination = output / "frozen_inputs" / f"seed{seed}" / filename
                        destination.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copyfile(ROOT / RUN / f"seed{seed}" / filename, destination)
                shutil.copyfile(ROOT / REFERENCE / "FROZEN_BEFORE_TEST.json", output / "ORIGINAL_FROZEN_MANIFEST.json")
                protocol = {
                    "checkpoint_hashes": frozen["checkpoint_hashes"], "protocol_hash": frozen["protocol_hash"],
                    "thresholds": thresholds, "source_hashes": {str(p.relative_to(ROOT)): sha256(p) for p in source_paths},
                    "validation_reference_sha256": sha256(ROOT / REFERENCE / "validation_histograms_2048_bins.npz"),
                    "original_manifest_sha256": sha256(ROOT / REFERENCE / "FROZEN_BEFORE_TEST.json"),
                    "prior_validation_result_sha256": sha256(ROOT / REFERENCE / "validation_result.json"),
                    "data_files": {str(p.relative_to(ROOT)): file_metadata(p) for pp in paths.values() for p in pp},
                    "precision": "float16_autocast; FP32 sigmoid and ensemble probability mean",
                    "ensemble": "equal probability mean; seed order 42,43,44",
                    "mask": "finite raw seismic != 0; per-patch observed zscore; reverse axes",
                    "training_performed": False, "threshold_search": False, "overlap": False,
                    "histogram_bins": r100.BINS, "expected_splits": SPLITS,
                    "environment": {"torch": str(torch.__version__), "cuda_build": torch.version.cuda,
                                    "gpu": torch.cuda.get_device_name(), "numpy": np.__version__},
                    "command": sys.argv,
                }
                json_write(output / "protocol.json", protocol)
                print("PREFLIGHT PASSED: checkpoint/source/data fingerprints verified; test HDF5 unopened", flush=True)
                validation, hist = evaluate_split("val", paths["val"], models, thresholds, output, progress)
                comparison = compare_histograms(hist, ROOT / REFERENCE / "validation_histograms_2048_bins.npz")
                for seed in SEEDS:
                    compare_metrics(validation["metrics"][f"seed{seed}"], selections[seed]["full_validation"], f"seed{seed}")
                compare_metrics(validation["metrics"]["ensemble"], prior_val["ensemble"], "ensemble")
                json_write(output / "validation_reproduction.json", {**validation, "histogram_comparison": comparison,
                           "status": "exact_reproduction", "test_files_opened": False})
                print("VALIDATION PASSED: all 8 histograms reproduce exactly; frozen thresholds unchanged", flush=True)
                if args.validation_only:
                    progress.update(status="validation_only_complete", stage="complete")
                    json_write(output / "progress.json", progress)
                    return
                # Recheck input bytes/metadata before test; no mutation during validation.
                preflight()
                json_write(output / "FROZEN_BEFORE_TEST.json", {**protocol, "status": "frozen_before_test",
                           "validation_exactly_reproduced": True, "test_files_opened": False,
                           "frozen_utc": datetime.now(timezone.utc).isoformat()})
                progress.update(test_files_opened=True, stage="test")
                json_write(output / "progress.json", progress)
                test, _ = evaluate_split("test", paths["test"], models, thresholds, output, progress)
                # Detect data changes during this evaluation before accepting the result.
                for relative, metadata in protocol["data_files"].items():
                    if file_metadata(ROOT / relative) != metadata:
                        raise RuntimeError(f"Data changed during evaluation: {relative}")
                result = {"status": "complete_official_test", "training_performed": False,
                          "thresholds_retuned": False, "completed_utc": datetime.now(timezone.utc).isoformat(),
                          "best_epochs": {f"seed{s}": selections[s]["best_epoch"] for s in SEEDS},
                          "checkpoint_hashes": frozen["checkpoint_hashes"], "thresholds": thresholds,
                          "validation_exactly_reproduced": True, "test": test, "seed_summary": seed_summary(test),
                          "peak_cuda_allocated_gib": torch.cuda.max_memory_allocated()/1024**3}
                json_write(output / "final_metrics.json", result)
                (output / "report.md").write_text(report_text(result))
                progress.update(status="complete_official_test", stage="complete")
                json_write(output / "progress.json", progress)
                print(report_text(result), flush=True)
            except BaseException as exc:
                progress.update(status="failed", error=f"{type(exc).__name__}: {exc}")
                json_write(output / "progress.json", progress)
                traceback.print_exc()
                raise
            finally:
                sys.stdout, sys.stderr = original_stdout, original_stderr


if __name__ == "__main__":
    main()
