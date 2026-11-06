"""Frozen SAM-Med3D: automatic and one-oracle-click Thebe evaluation."""
from pathlib import Path
from datetime import datetime, timezone
from dataclasses import asdict
import csv
import hashlib
import itertools
import json
import math
import os
import sys
import time
import traceback

ROOT = Path.cwd()
OUT = Path(os.environ["SAM_FROZEN_OUT"])
MODES = ("no_prompts", "one_oracle_click")
SIZE, BINS, SEED = 128, 2048, 42
state = {"status": "running", "stage": "preflight", "test_files_opened": False,
         "training_performed": False, "weight_updates": 0,
         "test_labels_used_for_prompts": {"no_prompts": False, "one_oracle_click": True},
         "validation": None, "test": None, "started_utc": datetime.now(timezone.utc).isoformat()}
protocol = {"experiment": "frozen_SAM-Med3D-turbo_Thebe", "training_performed": False,
    "weight_updates": 0, "adapter_used": False, "patch_size": SIZE,
    "precision": "float16_autocast", "histogram_bins": BINS,
    "modes": list(MODES), "seed": SEED,
    "normalization": "R100 observed-voxel per-patch z-score and axis reversal",
    "scoring": "all observed nonzero finite seismic voxels; no padding or overlap",
    "prompt_policy": "one uniformly sampled GT-positive voxel if any fault is present; otherwise one uniformly sampled observed negative voxel; no clicks for no-data patches",
    "prompt_information": "GT patch presence and one labelled voxel; oracle-assisted, not automatic",
    "mask_policy": "single mask; no mask prompts, boxes, corrections, or GT-based output selection",
    "threshold_policy": "report 0.5 plus per-mode best-Dice validation threshold; freeze before opening test",
    "test_threshold_tuning": False}

def write_json(path, value):
    temp = path.with_name(path.name + ".part")
    temp.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")
    temp.replace(path)

def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def point_order(model):
    pe = model.prompt_encoder.pe_layer
    image_size = tuple(model.prompt_encoder.input_image_size)
    grid_size = tuple(model.prompt_encoder.image_embedding_size)
    if image_size != (SIZE,) * 3:
        raise RuntimeError(f"Unexpected model input size: {image_size}")
    cell = (1, 2, 3)
    centers = torch.tensor([[(cell[i] + 0.5) * image_size[i] / grid_size[i]
                             for i in range(3)]], device="cuda").unsqueeze(0)
    reference = pe(grid_size)[:, cell[0], cell[1], cell[2]]
    matches = []
    for order in itertools.permutations(range(3)):
        actual = pe.forward_with_coords(centers[..., list(order)], image_size)[0, 0]
        if float((actual - reference).abs().max()) < 1e-5:
            matches.append(order)
    if len(matches) != 1:
        raise RuntimeError(f"Could not uniquely verify point coordinates: {matches}")
    return list(matches[0])

def evaluate(prefix, count, thresholds=None):
    state["stage"] = prefix
    paths = [ROOT / "data/processed/thebe_h5" / f"{prefix}{i}.h5" for i in range(1, count + 1)]
    if prefix == "test":
        state["test_files_opened"] = True
    reader = sam.r100.ConcatenatedThebe(paths)
    try:
        expected = (200 if prefix == "val" else 703, 3174, 1537)
        if tuple(reader.shape) != expected:
            raise RuntimeError(f"Unexpected {prefix} shape: {reader.shape}; expected {expected}")
        coords = list(itertools.product(*(range(0, n, SIZE) for n in reader.shape)))
        hist = {mode: sam.r100.baseline.ProbabilityHistogram(BINS) for mode in MODES}
        coverage = {"patches_planned": len(coords), "patches_processed": 0,
            "patches_scored": 0, "no_data_patches": 0, "constant_observed_patches": 0,
            "raw_voxels": 0, "valid_voxels": 0, "positive_labels_excluded": 0,
            "positive_clicks": 0, "negative_clicks": 0}
        started = time.monotonic()
        with (OUT / f"{prefix}_clicks.csv").open("w", newline="") as handle:
            clicks = csv.writer(handle)
            clicks.writerow(["patch", "x0", "y0", "z0", "model_axis0", "model_axis1",
                             "model_axis2", "prompt_axis0", "prompt_axis1", "prompt_axis2", "label"])
            for number, origin in enumerate(coords, 1):
                x, target, mask, _, _, _, constant = sam.r100.read_patch(reader, origin)
                if tuple(x.shape) != (1, 1, SIZE, SIZE, SIZE) or target.shape != x.shape or mask.shape != x.shape:
                    raise RuntimeError("Unexpected patch tensor shapes")
                raw = math.prod(min(SIZE, n - a) for n, a in zip(reader.shape, origin))
                valid = mask[0, 0].cpu().numpy().astype(bool)
                truth = target[0, 0].cpu().numpy() >= 0.5
                observed = int(valid.sum())
                if observed > raw:
                    raise RuntimeError("Observed mask includes padded voxels")
                coverage["raw_voxels"] += raw
                coverage["valid_voxels"] += observed
                coverage["positive_labels_excluded"] += int((truth & ~valid).sum())
                coverage["patches_processed"] = number
                if observed:
                    coverage["patches_scored"] += 1
                    coverage["constant_observed_patches"] += int(bool(constant))
                    foreground = np.flatnonzero(truth & valid)
                    label = int(len(foreground) > 0)
                    choices = foreground if label else np.flatnonzero(valid)
                    rng = np.random.default_rng(SEED + number)
                    voxel = np.asarray(np.unravel_index(int(choices[rng.integers(len(choices))]), valid.shape))
                    prompt_voxel = voxel[order]
                    point = torch.tensor(prompt_voxel, dtype=torch.float32, device="cuda")[None, None]
                    point_label = torch.tensor([[label]], dtype=torch.int64, device="cuda")
                    coverage["positive_clicks" if label else "negative_clicks"] += 1
                    clicks.writerow([number, *origin, *voxel.tolist(), *prompt_voxel.tolist(), label])
                    metric_mask = mask.to("cuda").bool()
                    target_scored = target.to("cuda")[metric_mask]
                    with torch.inference_mode(), torch.autocast("cuda", dtype=torch.float16):
                        embedding = model.image_encoder(x.to("cuda"))
                        for mode in MODES:
                            points = None if mode == "no_prompts" else (point, point_label)
                            sparse, dense = model.prompt_encoder(points=points, boxes=None, masks=None)
                            low, _ = model.mask_decoder(image_embeddings=embedding,
                                image_pe=model.prompt_encoder.get_dense_pe(),
                                sparse_prompt_embeddings=sparse, dense_prompt_embeddings=dense,
                                multimask_output=False)
                            logits = F.interpolate(low, size=(SIZE,) * 3, mode="trilinear", align_corners=False)
                            if tuple(logits.shape) != tuple(x.shape) or not torch.isfinite(logits).all().item():
                                raise RuntimeError(f"Invalid {mode} output at {prefix} patch {number}")
                            probability = torch.sigmoid(logits.float())[metric_mask]
                            hist[mode].update_probabilities(probability, target_scored)
                else:
                    coverage["no_data_patches"] += 1
                if number % 10 == 0 or number == len(coords):
                    handle.flush()
                    progress = {"split": prefix, **coverage,
                                "minutes": round((time.monotonic() - started) / 60, 2)}
                    write_json(OUT / "progress.json", progress)
                    print(f"{prefix}: patch {number}/{len(coords)}; scored={coverage['patches_scored']}; minutes={progress['minutes']}", flush=True)
        if coverage["raw_voxels"] != math.prod(reader.shape) or coverage["valid_voxels"] == 0:
            raise RuntimeError("Incomplete coverage or no observed voxels")
        coverage["excluded_no_data_voxels"] = coverage["raw_voxels"] - coverage["valid_voxels"]
        document = {"split": prefix, "files": [str(p.relative_to(ROOT)) for p in paths],
            "shape": list(reader.shape), "coverage": coverage,
            "seconds": time.monotonic() - started, "modes": {}}
        for mode in MODES:
            threshold = float(hist[mode].best_dice_threshold()) if prefix == "val" else float(thresholds[mode])
            fixed = asdict(hist[mode].metrics(0.5))
            calibrated = asdict(hist[mode].metrics(threshold))
            if sum(calibrated[k] for k in ("tp", "fp", "fn", "tn")) != coverage["valid_voxels"]:
                raise RuntimeError("Metric voxel counts disagree with coverage")
            document["modes"][mode] = {"threshold": threshold, "at_0_5": fixed,
                "at_validation_threshold": calibrated}
            print(prefix, mode, f"Dice@0.5={fixed['dice']:.6f}",
                  f"Dice@val_threshold={calibrated['dice']:.6f}", flush=True)
        write_json(OUT / f"{prefix}_metrics.json", document)
        return document
    finally:
        reader.close()

def save_report():
    lines = ["# Frozen SAM-Med3D-Turbo on Thebe", "", f"Status: **{state['status']}**.", "",
        "Original pretrained model; no adapter, weight updates, or training. Seismic preprocessing uses the R100 reader.",
        "One-click results are oracle-assisted: GT patch presence determines positive/negative click type, and GT supplies its location. They are separate from automatic results.",
        "Fault-free patches are included. All fault labels in each patch are scored; one click is not supplied per fault instance.",
        "Global voxel metrics use non-overlapping 128³ patches and exclude raw no-data/padding. AUC metrics use 2048 bins.", "",
        "| Split | Mode | Dice @ 0.5 | Val threshold | Dice @ val threshold | IoU | Precision | Recall | ROC-AUC (approx.) |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for split in ("validation", "test"):
        document = state.get(split)
        if document:
            for mode, values in document["modes"].items():
                m = values["at_validation_threshold"]
                lines.append(f"| {split} | {mode} | {values['at_0_5']['dice']:.6f} | {values['threshold']:.9f} | {m['dice']:.6f} | {m['iou']:.6f} | {m['precision']:.6f} | {m['recall']:.6f} | {m['roc_auc_approx']:.6f} |")
    lines += ["", "Thresholds are selected only on full validation and saved before opening test. Fixed-0.5 results are also retained.",
        "Evidence: protocol.json, threshold_selection.json, val_metrics.json, test_metrics.json, per-split click CSVs, evaluate.py, and console.log."]
    if "error" in state:
        lines += ["", "## Failure", "", "```text", state["traceback"], "```"]
    (OUT / "report.md").write_text("\n".join(lines) + "\n")

def update_indexes():
    root_readme = next((p for p in sorted(ROOT.iterdir()) if p.is_file() and p.name.lower() == "readme.md"), ROOT / "README.md")
    for index in (root_readme, ROOT / "reports/README.md"):
        previous = index.read_text() if index.exists() else "# Experiment reports\n"
        start, end = "<!-- sam-frozen-results:start -->", "<!-- sam-frozen-results:end -->"
        if previous.count(start) != previous.count(end) or previous.count(start) > 1 or (start in previous and previous.index(end) < previous.index(start)):
            raise RuntimeError(f"Malformed SAM report markers: {index}")
        link = os.path.relpath((OUT / "report.md").resolve(), index.parent)
        entry = f"- [Frozen SAM-Med3D: {OUT.name}]({link}) — {state['status']}; automatic and oracle one-click results.\n"
        if link in previous:
            continue
        if start in previous:
            before, after = previous.split(end, 1)
            updated = before.rstrip() + "\n" + entry + end + after
        else:
            updated = previous.rstrip() + f"\n\n{start}\n\n## Frozen SAM-Med3D evaluations\n\n" + entry + f"\n{end}\n"
        if index.exists():
            backup = OUT / "readme_backups" / index.relative_to(ROOT)
            backup.parent.mkdir(parents=True, exist_ok=True)
            backup.write_text(previous)
        index.parent.mkdir(parents=True, exist_ok=True)
        temp = index.with_name(index.name + ".part")
        temp.write_text(updated)
        temp.replace(index)

try:
    import numpy as np
    import torch
    from torch.nn import functional as F
    script = ROOT / "scripts/train_sammed3d_thebe.py"
    if sha(script) != "0d1c9f7329dc4b4e477a823d5eb210ee419fff5226f0ffdadeab1bca2a0157ef":
        raise RuntimeError("SAM helper changed since the reviewed archive")
    sys.path.insert(0, str(ROOT / "scripts"))
    import train_sammed3d_thebe as sam
    if sam.sam_source_commit() != "f3de1fa10da98e46f49f176773d2b1e306ba131f":
        raise RuntimeError("SAM source commit changed")
    if not torch.cuda.is_available() or torch.cuda.mem_get_info()[0] < 10 * 1024**3:
        raise RuntimeError("CUDA with at least 10 GiB free memory is required")
    checkpoint = ROOT / "external/SAM-Med3D/ckpt/sam_med3d_turbo.pth"
    protocol["checkpoint_sha256"] = sha(checkpoint)
    if protocol["checkpoint_sha256"] != "899a46d04d3b70f723282ceb489149373558bf0aaba389a346f5ab57da5cdd3c":
        raise RuntimeError("Pretrained checkpoint checksum changed")
    files = [ROOT / "data/processed/thebe_h5" / f"{prefix}{i}.h5"
             for prefix, count in (("val", 2), ("test", 7)) for i in range(1, count + 1)]
    if not all(p.is_file() for p in files) or len({p.resolve() for p in files}) != 9:
        raise RuntimeError("Missing or overlapping validation/test files")
    protocol["data_files"] = [{"path": str(p.relative_to(ROOT)), "bytes": p.stat().st_size,
        "mtime_ns": p.stat().st_mtime_ns} for p in files]
    protocol["source_hashes"] = {str(p.relative_to(ROOT)): sha(p) for p in (
        script, ROOT / "scripts/train_r100_fp16_clean.py", ROOT / "scripts/faultseg3d_baseline.py")}
    for relative in protocol["source_hashes"]:
        snapshot = OUT / "source_snapshot" / relative
        snapshot.parent.mkdir(parents=True, exist_ok=True)
        snapshot.write_bytes((ROOT / relative).read_bytes())
    protocol["sam_commit"] = sam.sam_source_commit()
    protocol["gpu"] = torch.cuda.get_device_name(0)
    protocol["torch"] = str(torch.__version__)
    torch.manual_seed(SEED)
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True
    torch.cuda.reset_peak_memory_stats()
    model = sam.sam_model_registry3D["vit_b_ori"](checkpoint=None)
    model.load_state_dict(sam.checkpoint_state(checkpoint), strict=True)
    model.eval().requires_grad_(False).to("cuda")
    with torch.inference_mode():
        order = point_order(model)
    protocol["point_coordinate_order"] = order
    protocol["evaluator_sha256"] = sha(Path(__file__).resolve())
    write_json(OUT / "protocol.json", protocol)
    print("FROZEN SAM: full validation, then held-out test; no training or adapter.", flush=True)
    state["validation"] = evaluate("val", 2)
    thresholds = {mode: state["validation"]["modes"][mode]["threshold"] for mode in MODES}
    write_json(OUT / "threshold_selection.json", {"source": "val1.h5 + val2.h5 only",
        "thresholds": thresholds, "test_files_opened_at_selection": False,
        "checkpoint_sha256": protocol["checkpoint_sha256"]})
    state["test"] = evaluate("test", 7, thresholds)
    state["peak_gpu_allocated_gib"] = torch.cuda.max_memory_allocated() / 1024**3
    state["status"] = "complete"
    state["stage"] = "complete"
except Exception as exc:
    state["status"] = "failed"
    state["error"] = repr(exc)
    state["traceback"] = traceback.format_exc()
finally:
    state["finished_utc"] = datetime.now(timezone.utc).isoformat()
    write_json(OUT / "protocol.json", protocol)
    save_report()
    try:
        update_indexes()
    except Exception as exc:
        state["readme_update_error"] = repr(exc)
    write_json(OUT / "final_metrics.json", state)
print("STATUS=" + state["status"], flush=True)
if "readme_update_error" in state:
    print("README_UPDATE_ERROR=" + state["readme_update_error"], flush=True)
if "error" in state:
    print(state["traceback"], flush=True)
print("REPORT=" + str(OUT / "report.md"), flush=True)
print("METRICS=" + str(OUT / "final_metrics.json"), flush=True)
if state["status"] != "complete" or "readme_update_error" in state:
    raise SystemExit(1)
