#!/usr/bin/env python3
"""Save R100 validation probabilities once for later ensemble-size measurements.

Inputs: completed clean R100 training directories. Output: one FP32 probability
file per seed, a shared label file, and a manifest. Only val1/val2 are opened.
Existing completed members can be reused when additional seeds become available.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import math
from pathlib import Path
import shutil
import time

import numpy as np
import torch

import train_r100_fp16_clean as r100
from run_r100_3seed_queue import validate_run


ROOT = Path(__file__).resolve().parents[1]
REFERENCE_RUN = ROOT / "runs/R100_fp16_clean_3seeds_20261014_150435/seed42"
SHAPE = (200, 3174, 1537)
VOXELS = 613_738_550
POSITIVES = 17_128_496


def read_json(path):
    return json.loads(Path(path).read_text())


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(8 * 1024**2), b""):
            digest.update(block)
    return digest.hexdigest()


def metadata(path):
    stat = path.stat()
    return {"bytes": stat.st_size, "mtime_ns": stat.st_mtime_ns}


def inspect_run(directory, reference):
    config = read_json(directory / "run_config.json")
    seed = config["seed"]
    validate_run(directory, seed, expected_protocol=reference["protocol_hash"])
    if config != {**reference, "seed": seed}:
        raise RuntimeError(f"Seed {seed}: recipe differs from the original clean runs")
    for relative, expected in config["data_file_metadata"].items():
        if metadata(ROOT / relative) != expected:
            raise RuntimeError(f"Data fingerprint changed: {relative}")
    return config, read_json(directory / "validation_selection.json")


def load_model(directory, seed):
    checkpoint = torch.load(directory / "best.pt", map_location="cpu", weights_only=False)
    if checkpoint["args"]["seed"] != seed:
        raise RuntimeError("Checkpoint seed mismatch")
    model = r100.baseline.FaultSeg3D()
    model.load_state_dict(checkpoint["model"], strict=True)
    return model.cuda().eval().requires_grad_(False)


def verify_cache_file(path, expected_sha, expected_dtype, count=VOXELS):
    if sha256(path) != expected_sha:
        raise RuntimeError(f"Cached file checksum differs: {path}")
    array = np.load(path, mmap_mode="r", allow_pickle=False)
    if array.shape != (count,) or array.dtype != np.dtype(expected_dtype):
        raise RuntimeError(f"Cached file shape/dtype differs: {path}")
    return array


@torch.inference_mode()
def build_cache(cache_dir, directories):
    torch.set_num_threads(4)
    reference = read_json(REFERENCE_RUN / "run_config.json")
    source_hashes = {**reference["source_hashes"],
                     "scripts/train_r100_fp16_clean.py": reference["trainer_sha256"]}
    for relative, expected in source_hashes.items():
        if sha256(ROOT / relative) != expected:
            raise RuntimeError(f"Frozen helper changed: {relative}")
    records = {}
    for directory in directories:
        config, selection = inspect_run(directory, reference)
        seed = config["seed"]
        if seed in records:
            raise RuntimeError(f"Duplicate seed: {seed}")
        records[seed] = {"directory": directory, "config": config, "selection": selection,
                         "checkpoint_sha256": sha256(directory / "best.pt")}
    manifest_path = cache_dir / "manifest.json"
    if manifest_path.exists():
        manifest = read_json(manifest_path)
        if manifest["status"] != "complete" or manifest["protocol_hash"] != reference["protocol_hash"]:
            raise RuntimeError("Existing cache is incomplete or uses another protocol")
        labels_existing = verify_cache_file(cache_dir / manifest["labels_file"], manifest["labels_sha256"], "uint8")
    else:
        if any(cache_dir.glob("*.npy")):
            raise RuntimeError("Unfinished cache files exist; inspect before rebuilding")
        manifest = {"status": "building", "protocol_hash": reference["protocol_hash"],
                    "source_hashes": source_hashes, "shape": list(SHAPE), "valid_voxels": VOXELS,
                    "positive_voxels": POSITIVES, "labels_file": "labels.npy", "members": {},
                    "test_files_opened": False, "training_performed": False}
        labels_existing = None
    pending = {}
    for seed, record in records.items():
        old = manifest["members"].get(str(seed))
        if old:
            if old["checkpoint_sha256"] != record["checkpoint_sha256"]:
                raise RuntimeError(f"Seed {seed}: cached checkpoint differs")
            verify_cache_file(cache_dir / old["probabilities_file"], old["probabilities_sha256"], "float32")
        else:
            pending[seed] = record
    if not pending:
        print("All requested members already have verified caches; no inference needed", flush=True)
        return
    required_bytes = VOXELS * (4 * len(pending) + int(labels_existing is None)) + 5 * 1024**3
    if shutil.disk_usage(cache_dir).free < required_bytes:
        raise RuntimeError("Insufficient space for FP32 cache plus 5 GiB reserve")
    if not torch.cuda.is_available() or torch.cuda.mem_get_info()[0] < 4 * 1024**3:
        raise RuntimeError("CUDA with at least 4 GiB free memory required")
    if (str(torch.__version__) != reference["torch_version"]
            or torch.version.cuda != reference["torch_cuda_build"]
            or torch.cuda.get_device_name() != reference["gpu_name"]):
        raise RuntimeError("GPU/PyTorch environment differs from the frozen run")
    r100.baseline.seed_everything(42)
    models = {seed: load_model(record["directory"], seed) for seed, record in pending.items()}
    paths = [ROOT / relative for relative in reference["validation_files"]]
    if [path.name for path in paths] != ["val1.h5", "val2.h5"]:
        raise RuntimeError("Cache must read only the two validation files")
    reader = r100.ConcatenatedThebe(paths)
    arrays = {seed: np.lib.format.open_memmap(cache_dir / f"seed{seed}.partial.npy", mode="w+", dtype="float32", shape=(VOXELS,))
              for seed in pending}
    labels = labels_existing if labels_existing is not None else np.lib.format.open_memmap(
        cache_dir / "labels.partial.npy", mode="w+", dtype="uint8", shape=(VOXELS,))
    hist = {seed: r100.baseline.ProbabilityHistogram(2048) for seed in pending}
    ensemble_hist = r100.baseline.ProbabilityHistogram(2048) if set(pending) == {42, 43, 44} else None
    tiles, offset, raw_count, positive_count, excluded_count = [], 0, 0, 0, 0
    started = time.monotonic()
    progress = {"status": "running", "test_files_opened": False, "pending_seeds": sorted(pending)}
    try:
        if reader.shape != SHAPE:
            raise RuntimeError(f"Validation shape differs: {reader.shape}")
        coordinates = r100.tiling(reader.shape)
        if len(coordinates) != 650:
            raise RuntimeError("Validation tiling differs")
        for number, origin in enumerate(coordinates, 1):
            x, target, mask, shape, observed, excluded, _ = r100.read_patch(reader, origin)
            end = offset + observed
            if end > VOXELS:
                raise RuntimeError("Validation cache exceeds expected size")
            raw_count += math.prod(shape)
            excluded_count += excluded
            tiles.append({"origin": list(origin), "offset": offset, "count": observed})
            if observed:
                truth_cpu = target[mask].numpy().astype("uint8")
                positive_count += int(truth_cpu.sum())
                if labels_existing is None:
                    labels[offset:end] = truth_cpu
                elif not np.array_equal(labels[offset:end], truth_cpu):
                    raise RuntimeError("Cached labels/ordering differ from validation data")
                x, target, mask = x.cuda(), target.cuda(), mask.cuda()
                truth = target[mask]
                predictions = []
                for seed, model in models.items():
                    with torch.autocast("cuda", dtype=torch.float16):
                        logits = model(x)
                    r100.assert_finite_tree(logits, "cache.logits")
                    probability = torch.sigmoid(logits.float())
                    hist[seed].update_probabilities(probability[mask], truth)
                    arrays[seed][offset:end] = probability[mask].cpu().numpy()
                    if ensemble_hist is not None:
                        predictions.append(probability)
                if ensemble_hist is not None:
                    ensemble_hist.update_probabilities(torch.stack(predictions).mean(0)[mask], truth)
            offset = end
            if number % 25 == 0 or number == len(coordinates):
                progress.update(patches=number, valid_voxels=offset, elapsed_seconds=time.monotonic()-started)
                r100.write_json_atomic(cache_dir / "progress.json", progress)
                print(f"validation cache {number}/650; minutes={(time.monotonic()-started)/60:.1f}", flush=True)
        if (offset, positive_count, raw_count, excluded_count) != (VOXELS, POSITIVES, math.prod(SHAPE), 23_514):
            raise RuntimeError("Validation coverage/label counts differ")
        if labels_existing is not None and tiles != manifest["tiles"]:
            raise RuntimeError("Validation tile ordering changed")
        for seed, histogram in hist.items():
            selection = pending[seed]["selection"]
            actual = asdict(histogram.metrics(selection["threshold"]))
            if actual != selection["full_validation"]:
                raise RuntimeError(f"Seed {seed}: cached predictions do not reproduce saved validation metrics")
        if ensemble_hist is not None:
            reference_hist = ROOT / "reports/evaluation/r100_ensemble_e0_20261016T120152Z/validation_histograms_2048_bins.npz"
            with np.load(reference_hist) as old:
                for seed, histogram in hist.items():
                    for kind in ("positive", "negative"):
                        if not np.array_equal(getattr(histogram, kind).numpy(), old[f"seed{seed}_{kind}"]):
                            raise RuntimeError("Original member validation histogram differs")
                for kind in ("positive", "negative"):
                    if not np.array_equal(getattr(ensemble_hist, kind).numpy(), old[f"ensemble_{kind}"]):
                        raise RuntimeError("Original ensemble validation histogram differs")
            manifest["original_three_seed_histograms_exact"] = True
        for array in arrays.values():
            array.flush()
        if labels_existing is None:
            labels.flush()
            (cache_dir / "labels.partial.npy").replace(cache_dir / "labels.npy")
            manifest["labels_sha256"] = sha256(cache_dir / "labels.npy")
        for seed, record in pending.items():
            filename = f"seed{seed}.npy"
            (cache_dir / f"seed{seed}.partial.npy").replace(cache_dir / filename)
            manifest["members"][str(seed)] = {
                "run_dir": str(record["directory"].relative_to(ROOT)),
                "checkpoint_sha256": record["checkpoint_sha256"],
                "probabilities_file": filename, "probabilities_sha256": sha256(cache_dir / filename),
                "validation_selection": record["selection"],
            }
        for path in paths:
            if metadata(path) != reference["data_file_metadata"][str(path.relative_to(ROOT))]:
                raise RuntimeError("Validation file changed during caching")
        manifest.update(status="complete", tiles=tiles, updated_utc=datetime.now(timezone.utc).isoformat(),
                        validation_data={str(path.relative_to(ROOT)): metadata(path) for path in paths},
                        cache_script_sha256=sha256(Path(__file__)))
        r100.write_json_atomic(manifest_path, manifest)
        progress.update(status="complete", cached_seeds=sorted(map(int, manifest["members"])))
        r100.write_json_atomic(cache_dir / "progress.json", progress)
        print(f"CACHE COMPLETE: seeds {progress['cached_seeds']}; FP32; no test files opened", flush=True)
    except BaseException as exc:
        progress.update(status="failed", error=str(exc))
        r100.write_json_atomic(cache_dir / "progress.json", progress)
        raise
    finally:
        reader.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache-dir", type=Path, required=True)
    parser.add_argument("--run-dirs", type=Path, nargs="+", required=True)
    args = parser.parse_args()
    cache = args.cache_dir.resolve()
    cache.mkdir(parents=True, exist_ok=True)
    with (cache / ".lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        build_cache(cache, [path.resolve() for path in args.run_dirs])


if __name__ == "__main__":
    main()
