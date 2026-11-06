#!/usr/bin/env python3
"""Short Attention3D experiment: denoise, transfer, and compare with scratch.

This is an in-domain adaptation, not a full reproduction of the paper.
Only train/validation H5 files are opened. Historical trainers stay unchanged.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import random
import signal
import time
from pathlib import Path

import h5py
import numpy as np
import torch
from torch.nn import functional as F
from torch.nn.attention import SDPBackend, sdpa_kernel

from train_paper_attention3d_thebe_bf16 import load_paper_code, save_atomic

SOURCE = Path("external/attention3d_paper/fault-detection-global-attention.py")
PATCH = 64
BINS = 2048
PRETEXT_FIT = (64, 1024)
PRETEXT_VALIDATION = (1280, 1536)
STOP = False


def write_json(path, value):
    temporary = path.with_name(path.name + ".part")
    temporary.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")
    temporary.replace(path)


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def seed_all(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def finite(value, name):
    if not torch.isfinite(value).all().item():
        raise FloatingPointError(f"Nonfinite {name}")


def normalize(raw):
    """Use R100's nonzero mask, valid-only z-score, and reversed axes."""
    if not np.isfinite(raw).all():
        raise ValueError("Nonfinite seismic")
    mask = raw != 0
    if not mask.any():
        return None
    values = raw[mask]
    std = float(values.std(dtype=np.float64))
    if std <= 1e-8:
        return None
    x = np.zeros_like(raw, dtype=np.float32)
    x[mask] = (raw[mask] - values.mean(dtype=np.float64)) / std
    return tensor(x), tensor(mask)


def tensor(array):
    return torch.from_numpy(np.ascontiguousarray(array.transpose()[None, None]))


def region_y(role, length):
    # The 256-voxel gap separates pretext fit and internal validation crops.
    if role == "pretrain":
        return PRETEXT_FIT
    if role == "reconstruction_validation":
        return PRETEXT_VALIDATION
    return 0, length


class Patches:
    def __init__(self, root):
        self.paths = {
            "train": [root / f"train{i}.h5" for i in range(1, 10)],
            "val": [root / f"val{i}.h5" for i in range(1, 3)],
        }
        self.handles = {}
        self.records = {}
        all_paths = [path.resolve() for paths in self.paths.values() for path in paths]
        if len(set(all_paths)) != len(all_paths):
            raise ValueError("Training/validation paths resolve to overlapping files")
        for paths in self.paths.values():
            for path in paths:
                handle = h5py.File(path, "r")
                self.handles[path] = handle
                if handle["seismic"].shape != handle["fault"].shape:
                    raise ValueError(f"Misaligned seismic/labels: {path}")
                if tuple(handle["seismic"].shape) != (100, 3174, 1537):
                    raise ValueError(f"Unexpected pilot shape: {path}")

    def close(self):
        for handle in self.handles.values():
            handle.close()

    def sample(self, role, index, seed=42):
        downstream_val = role == "validation"
        supervised = role in {"supervised", "validation"}
        paths = self.paths["val" if downstream_val else "train"]
        rng = np.random.default_rng(seed + index * 1009)
        for attempt in range(256):
            # Validation alternates files so both volumes are represented.
            path = paths[index % len(paths)] if downstream_val else paths[int(rng.integers(len(paths)))]
            handle = self.handles[path]
            shape = handle["seismic"].shape
            lo, hi = region_y(role, shape[1])
            start = (int(rng.integers(shape[0] - PATCH + 1)),
                     int(rng.integers(lo, hi - PATCH + 1)),
                     int(rng.integers(shape[2] - PATCH + 1)))
            slices = tuple(slice(s, s + PATCH) for s in start)
            result = normalize(np.asarray(handle["seismic"][slices], dtype=np.float32))
            if result is None:
                continue
            x, mask = result
            target = None
            if supervised:
                raw = np.asarray(handle["fault"][slices])
                if not np.logical_or(raw == 0, raw == 1).all():
                    raise ValueError(f"Nonbinary labels: {path}")
                target = tensor(raw.astype(np.float32))
                if role == "supervised" and index % 2 == 0 and not (target.bool() & mask).any():
                    continue
            self.records[f"{role}:{index}"] = {
                "file": str(path), "start": start, "size": PATCH,
                "attempt": attempt, "valid_voxels": int(mask.sum()),
            }
            return x, target, mask, path.name
        raise RuntimeError(f"No usable {role} patch for index {index}")


def corrupt(x, mask, generator):
    # Normalized patches have approximately unit RMS. Targets retain field noise.
    rms = x[mask].square().mean().sqrt()
    noise = torch.randn(x.shape, generator=generator, dtype=x.dtype) * (0.1 * rms)
    return torch.where(mask, x + noise, torch.zeros_like(x))


def transfer_features(model, state):
    """Load every feature tensor exactly; keep a fresh segmentation output head."""
    expected = model.state_dict()
    head = {key for key in expected if key.startswith("out_conv.")}
    features = set(expected) - head
    if set(state) != set(expected):
        raise ValueError("Pretraining checkpoint keys differ from the segmentation model")
    for key in expected:
        if state[key].shape != expected[key].shape:
            raise ValueError(f"Transfer shape mismatch: {key}")
        finite(state[key], key)
    original_head = {key: expected[key].clone() for key in head}
    result = model.load_state_dict({key: state[key] for key in features}, strict=False)
    if set(result.missing_keys) != head or result.unexpected_keys:
        raise ValueError(f"Unexpected transfer result: {result}")
    after = model.state_dict()
    if not all(torch.equal(after[key], state[key]) for key in features):
        raise ValueError("Transferred feature tensors do not match")
    if not all(torch.equal(after[key], original_head[key]) for key in head):
        raise ValueError("Fresh segmentation head changed during transfer")
    return {"feature_tensors_loaded": sorted(features), "fresh_head_tensors": sorted(head),
            "unexpected_keys": [], "mismatched_tensors": [], "exact_values_verified": True}


def forward(model, x):
    # Disallow the dense fallback: a full 64-cube score matrix would be enormous.
    with sdpa_kernel([SDPBackend.FLASH_ATTENTION, SDPBackend.EFFICIENT_ATTENTION]):
        with torch.autocast("cuda", dtype=torch.bfloat16):
            logits = model(x)
    finite(logits, "output")
    return logits.float()


def optimizer_step(model, optimizer):
    norm = torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
    finite(norm, "gradient norm")
    optimizer.step()
    optimizer.zero_grad(set_to_none=True)
    return float(norm)


def setup_gpu(fraction):
    torch.set_num_threads(2)
    if not torch.cuda.is_available() or not torch.cuda.is_bf16_supported():
        raise RuntimeError("A BF16-capable CUDA GPU is required")
    torch.cuda.set_per_process_memory_fraction(fraction)
    torch.backends.cudnn.benchmark = False
    torch.backends.cuda.enable_math_sdp(False)


def preflight(args, paper, patches):
    # Check every fixed validation crop before committing to GPU training.
    for i in range(8):
        patches.sample("reconstruction_validation", i, 7004)
    for i in range(args.val_patches):
        patches.sample("validation", i, 1042)
    seed_all(42)
    model = paper.Attention3DUNet().cuda()
    if sum(p.numel() for p in model.parameters()) != 45_001_057:
        raise ValueError("Unexpected attention model identity")
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4, weight_decay=1e-4)
    x, _, mask, _ = patches.sample("pretrain", 0)
    generator = torch.Generator().manual_seed(701)
    corrupted = corrupt(x, mask, generator).cuda()
    x, mask = x.cuda(), mask.cuda()
    rows = []
    for step in range(2):
        torch.cuda.synchronize()
        start = time.monotonic()
        prediction = forward(model, corrupted)
        loss = F.mse_loss(prediction[mask], x[mask])
        finite(loss, "preflight loss")
        loss.backward()
        norm = optimizer_step(model, optimizer)
        torch.cuda.synchronize()
        rows.append({"step": step + 1, "loss": float(loss), "gradient_norm": norm,
                     "seconds": time.monotonic() - start})
        print(json.dumps(rows[-1]), flush=True)
    for name, p in model.named_parameters():
        finite(p, name)
    state_steps = [int(state["step"]) for state in optimizer.state.values()]
    if not state_steps or set(state_steps) != {2}:
        raise RuntimeError("Preflight did not update all parameter groups twice")
    write_json(args.run_dir / "gpu_preflight.json", {
        "status": "passed", "parameter_count": 45_001_057, "patch_size": PATCH,
        "precision": "BF16 autocast; FP32 loss and weights", "steps": rows,
        "peak_allocated_bytes": torch.cuda.max_memory_allocated(),
        "peak_reserved_bytes": torch.cuda.max_memory_reserved(),
        "memory_fraction_cap": args.memory_fraction, "gpu": torch.cuda.get_device_name(),
        "source_sha256": sha256(SOURCE), "trainer_sha256": sha256(Path(__file__)),
        "torch": torch.__version__, "test_files_opened": False,
        "sampling": patches.records,
    })


def metrics(positive, negative, threshold=None):
    tp = np.cumsum(positive[::-1], dtype=np.int64)[::-1]
    fp = np.cumsum(negative[::-1], dtype=np.int64)[::-1]
    total_p, total_n = int(positive.sum()), int(negative.sum())
    fn = total_p - tp
    dice = np.divide(2 * tp, 2 * tp + fp + fn, out=np.zeros(BINS), where=(2 * tp + fp + fn) != 0)
    idx = int(np.argmax(dice)) if threshold is None else int(threshold * BINS)
    precision = np.divide(tp, tp + fp, out=np.zeros(BINS), where=(tp + fp) != 0)
    recall = tp / max(1, total_p)
    pr_auc = float(np.sum(np.diff(np.r_[0.0, recall[::-1]]) * precision[::-1]))
    return {"threshold": idx / BINS, "dice": float(dice[idx]),
            "iou": float(tp[idx] / max(1, int(tp[idx] + fp[idx] + fn[idx]))),
            "precision": float(precision[idx]), "recall": float(recall[idx]),
            "pr_auc_approx": pr_auc, "tp": int(tp[idx]), "fp": int(fp[idx]),
            "fn": int(fn[idx]), "tn": int(total_n - fp[idx]),
            "scored_voxels": total_p + total_n}


@torch.inference_mode()
def evaluate(model, samples):
    model.eval()
    histograms = {}
    losses = []
    for x, target, mask, volume in samples:
        x, target, mask = x.cuda(), target.cuda(), mask.cuda()
        logits = forward(model, x)
        p, y = logits[mask].sigmoid(), target[mask].bool()
        index = torch.clamp((p * BINS).long(), 0, BINS - 1)
        positive = torch.bincount(index[y], minlength=BINS).cpu().numpy()
        negative = torch.bincount(index[~y], minlength=BINS).cpu().numpy()
        hp, hn = histograms.setdefault(volume, (np.zeros(BINS, np.int64), np.zeros(BINS, np.int64)))
        hp += positive
        hn += negative
        losses.append(float(F.binary_cross_entropy_with_logits(logits[mask], target[mask])))
    positive = sum(pair[0] for pair in histograms.values())
    negative = sum(pair[1] for pair in histograms.values())
    selected = metrics(positive, negative)
    return {"best_threshold_metrics": selected, "at_0_5": metrics(positive, negative, 0.5),
            "mean_patch_bce": sum(losses) / len(losses),
            "per_volume_at_common_threshold": {
                key: metrics(hp, hn, selected["threshold"]) for key, (hp, hn) in histograms.items()},
            "positive_histogram": positive.tolist(), "negative_histogram": negative.tolist()}


def check_budget(deadline):
    if STOP or time.monotonic() >= deadline:
        raise TimeoutError("Pilot stopped at its wall-time limit or termination request")


def append_history(path, row):
    exists = path.exists()
    with path.open("a", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(row))
        if not exists:
            writer.writeheader()
        writer.writerow(row)


def train_phase(args, paper, patches, phase, deadline, initial_state=None):
    supervised = phase != "pretrain"
    seed_all(42 if supervised else 7001)
    model = paper.Attention3DUNet()
    if initial_state is not None:
        report = transfer_features(model, initial_state)
        report["pretraining_checkpoint_sha256"] = sha256(args.run_dir / "pretrain_best.pt")
        write_json(args.run_dir / "transfer_report.json", report)
    # Reset sampling and corruption streams independently of initialization.
    generator = torch.Generator().manual_seed(7002)
    model = model.cuda()
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4 if not supervised else 5e-4, weight_decay=1e-4)
    criterion = paper.UnifiedFocalLoss(lambda_param=0.5, tversky_alpha=0.3, tversky_beta=0.7,
                                     tversky_gamma=1.33, focal_alpha=0.25, focal_gamma=2.0)
    count = args.supervised_patches if supervised else args.pretrain_patches
    accumulation = 4
    updates = count // accumulation
    best = float("-inf")
    history_path = args.run_dir / f"{phase}_history.csv"
    val_samples = [patches.sample("validation", i, 1042) for i in range(args.val_patches)] if supervised else []
    recon_samples = []
    if not supervised:
        validation_noise = torch.Generator().manual_seed(7003)
        for i in range(8):
            x, _, mask, _ = patches.sample("reconstruction_validation", i, 7004)
            recon_samples.append((corrupt(x, mask, validation_noise), x, mask))
    start = time.monotonic()
    current = {}
    training_losses = []
    sampling_digest = hashlib.sha256()
    try:
        for index in range(count):
            check_budget(deadline)
            model.train()
            update = index // accumulation
            cut = max(1, updates // 10)
            progress = update / cut if update < cut else 1 - (update - cut) / max(1, updates - cut)
            multiplier = (1 + 31 * max(0.0, progress)) / 32
            for group in optimizer.param_groups:
                group["lr"] = (5e-4 if supervised else 1e-4) * multiplier
            x, target, mask, _ = patches.sample("supervised" if supervised else "pretrain", index)
            key = f"{'supervised' if supervised else 'pretrain'}:{index}"
            sampling_digest.update(json.dumps(patches.records[key], sort_keys=True).encode())
            input_x = x if supervised else corrupt(x, mask, generator)
            target = target if supervised else x
            prediction = forward(model, input_x.cuda())
            mask, target = mask.cuda(), target.cuda()
            loss = criterion(prediction[mask], target[mask]) if supervised else F.mse_loss(prediction[mask], target[mask])
            finite(loss, f"{phase} loss")
            training_losses.append(float(loss.detach()))
            (loss / accumulation).backward()
            grad_norm = None
            if (index + 1) % accumulation == 0:
                grad_norm = optimizer_step(model, optimizer)
            current = {"phase": phase, "patches": index + 1, "optimizer_updates": (index + 1) // accumulation,
                       "loss": float(loss.detach()), "gradient_norm": grad_norm,
                       "seconds": time.monotonic() - start}
            if (index + 1) % 16 == 0:
                append_history(history_path, current)
                write_json(args.run_dir / "progress.json", current)
                print(json.dumps(current), flush=True)
            if (index + 1) % args.eval_every == 0 or index + 1 == count:
                check_budget(deadline)
                model.eval()
                if supervised:
                    evaluation = evaluate(model, val_samples)
                    score = evaluation["best_threshold_metrics"]["pr_auc_approx"]
                else:
                    with torch.inference_mode():
                        errors = [float(F.mse_loss(forward(model, noisy.cuda())[mask.cuda()], target.cuda()[mask.cuda()]))
                                  for noisy, target, mask in recon_samples]
                    identity_errors = [float(F.mse_loss(noisy[mask], target[mask]))
                                       for noisy, target, mask in recon_samples]
                    identity_mse = sum(identity_errors) / len(identity_errors)
                    evaluation = {"mean_masked_mse": sum(errors) / len(errors),
                                  "noisy_input_identity_mse": identity_mse,
                                  "mse_improvement_over_noisy_input": identity_mse - sum(errors) / len(errors)}
                    score = -evaluation["mean_masked_mse"]
                write_json(args.run_dir / f"{phase}_validation_{index + 1:05d}.json", evaluation)
                write_json(args.run_dir / "patch_manifest.json", patches.records)
                if score > best:
                    best = score
                    save_atomic(args.run_dir / f"{phase}_best.pt", {
                        "model": model.state_dict(), "phase": phase, "patches": index + 1,
                        "optimizer_updates": (index + 1) // accumulation, "validation": evaluation,
                        "config_sha256": sha256(args.run_dir / "config.json"),
                    })
                print(f"{phase} validation patches={index + 1} score={score:.6f}", flush=True)
        state = {key: value.detach().cpu().clone() for key, value in model.state_dict().items()}
        for key, value in state.items():
            finite(value, key)
        write_json(args.run_dir / f"{phase}_complete.json", {**current,
                   "seconds": time.monotonic() - start, "status": "complete",
                   "mean_training_loss": sum(training_losses) / len(training_losses),
                   "crop_stream_sha256": sampling_digest.hexdigest(),
                   "peak_allocated_bytes": torch.cuda.max_memory_allocated(), "test_files_opened": False})
        return state
    except BaseException:
        # Keep progress from an interrupted trial; it is never labelled complete.
        save_atomic(args.run_dir / f"{phase}_interrupted.pt", {"model": model.state_dict(),
                    "optimizer": optimizer.state_dict(), "progress": current})
        raise
    finally:
        del model, optimizer
        torch.cuda.empty_cache()


def run(args, paper, patches):
    deadline = time.monotonic() + args.max_seconds
    for phase in ["pretrain", "scratch", "finetune"]:
        check_budget(deadline)
        write_json(args.run_dir / "state.json", {"status": "running", "phase": phase, "test_files_opened": False})
        pretrained = None
        if phase == "finetune":
            pretrained = torch.load(args.run_dir / "pretrain_best.pt", map_location="cpu", weights_only=False)["model"]
        train_phase(args, paper, patches, phase, deadline, pretrained)
        write_json(args.run_dir / "patch_manifest.json", patches.records)
    results = {}
    scratch_control = json.loads((args.run_dir / "scratch_complete.json").read_text())
    finetune_control = json.loads((args.run_dir / "finetune_complete.json").read_text())
    if scratch_control["crop_stream_sha256"] != finetune_control["crop_stream_sha256"]:
        raise RuntimeError("Scratch and fine-tuning did not use identical supervised crops")
    for phase in ["scratch", "finetune"]:
        checkpoint = torch.load(args.run_dir / f"{phase}_best.pt", map_location="cpu", weights_only=False)
        results[phase] = {"checkpoint_sha256": sha256(args.run_dir / f"{phase}_best.pt"),
                          "patches_at_selection": checkpoint["patches"], "validation": checkpoint["validation"]}
    difference = results["finetune"]["validation"]["best_threshold_metrics"]["dice"] - results["scratch"]["validation"]["best_threshold_metrics"]["dice"]
    write_json(args.run_dir / "comparison.json", {"results": results, "dice_difference": difference,
               "matched_supervised_crop_stream_verified": True,
               "interpretation": "Short crop-based validation screening; not converged R100 or full-survey evidence",
               "test_files_opened": False})
    write_json(args.run_dir / "state.json", {"status": "complete", "phase": "all_complete", "test_files_opened": False})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", choices=["preflight", "run"], required=True)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--thebe-root", type=Path, default=Path("data/processed/thebe_h5"))
    parser.add_argument("--memory-fraction", type=float, default=0.40)
    parser.add_argument("--pretrain-patches", type=int, default=128)
    parser.add_argument("--supervised-patches", type=int, default=512)
    parser.add_argument("--val-patches", type=int, default=32)
    parser.add_argument("--eval-every", type=int, default=128)
    parser.add_argument("--max-seconds", type=int, default=12600)
    args = parser.parse_args()
    if not 0 < args.memory_fraction <= 0.40:
        raise ValueError("The concurrent pilot is limited to 40% of GPU memory")
    if any(n <= 0 or n % 4 for n in [args.pretrain_patches, args.supervised_patches, args.eval_every]):
        raise ValueError("Training counts must be positive multiples of four")
    if args.val_patches < 2 or args.max_seconds <= 0:
        raise ValueError("Validation must cover both volumes; time cap must be positive")
    args.run_dir.mkdir(parents=True, exist_ok=True)
    if args.phase == "run" and (args.run_dir / "config.json").exists():
        raise FileExistsError("Refusing to overwrite an existing pilot")
    setup_gpu(args.memory_fraction)
    paper = load_paper_code(SOURCE)
    patches = Patches(args.thebe_root)
    def request_stop(signum, frame):
        global STOP
        STOP = True
    signal.signal(signal.SIGTERM, request_stop)
    signal.signal(signal.SIGINT, request_stop)
    try:
        if args.phase == "preflight":
            preflight(args, paper, patches)
        else:
            if not (args.run_dir / "gpu_preflight.json").exists():
                raise RuntimeError("Run the bounded GPU preflight first")
            checked = json.loads((args.run_dir / "gpu_preflight.json").read_text())
            if checked["status"] != "passed" or checked["source_sha256"] != sha256(SOURCE):
                raise RuntimeError("The GPU preflight did not pass for this source")
            config = vars(args).copy()
            config = {key: str(value) if isinstance(value, Path) else value for key, value in config.items()}
            config.update({"experiment": "in_domain_attention3d_denoising_short_pilot", "parameter_count": 45_001_057,
                "source_sha256": sha256(SOURCE), "trainer_sha256": sha256(Path(__file__)),
                "paper_reproduction": False, "test_files_opened": False, "patch_size": PATCH,
                "pretext_data": "train1..9 seismic only; axis 1 [64,1024)",
                "pretext_validation": "train1..9 seismic only; axis 1 [1280,1536)",
                "spatial_provenance": "Stored crops disjoint; physical survey coordinates unavailable",
                "supervised_sampling": "Identical deterministic crop stream for scratch and fine-tune; seed 42",
                "mask": "finite raw != 0; valid-only z-score; reverse axes",
                "corruption": "Gaussian std 0.1*valid patch RMS; masked MSE to uncorrupted field input",
                "checkpoint_selection": "pretrain: minimum internal MSE; supervised: maximum approximate validation PR-AUC",
                "pr_auc_definition": "2048-bin stepwise precision-recall area (average precision approximation)",
                "threshold_selection": "best aggregate crop Dice; 2048 bins; newly selected per model",
                "transfer": "all feature tensors exactly; fresh output head; AdamW reset",
                "fine_tuning": "all layers trainable; no LLRD or gradual unfreezing in this isolated pretraining comparison"})
            write_json(args.run_dir / "config.json", config)
            run(args, paper, patches)
    except BaseException as error:
        write_json(args.run_dir / "state.json", {"status": "failed" if not isinstance(error, TimeoutError) else "budget_stopped",
                   "error": f"{type(error).__name__}: {error}", "test_files_opened": False})
        raise
    finally:
        patches.close()


if __name__ == "__main__":
    main()
