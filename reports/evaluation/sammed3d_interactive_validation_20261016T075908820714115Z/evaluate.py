"""Validation-only SAM-Med3D interactive protocol diagnostic for Thebe."""
from pathlib import Path
from datetime import datetime, timezone
from dataclasses import asdict
import csv
import hashlib
import itertools
import json
import math
import os
import statistics
import sys
import time
import traceback


ROOT = Path.cwd()
OUT = Path(os.environ["SAM_INTERACTIVE_OUT"])
SIZE, BINS, SEED = 128, 2048, 42
CLICK_CHECKPOINTS = (1, 3, 5)
CROP_POLICIES = ("fixed_positive_grid", "label_centered")
NORMALIZATIONS = ("r100_observed_zscore", "sam_positive_zscore")
MAX_CLICKS = max(CLICK_CHECKPOINTS)
EXPECTED_HELPER_SHA = "0d1c9f7329dc4b4e477a823d5eb210ee419fff5226f0ffdadeab1bca2a0157ef"
EXPECTED_SAM_COMMIT = "f3de1fa10da98e46f49f176773d2b1e306ba131f"
EXPECTED_CHECKPOINT_SHA = "899a46d04d3b70f723282ceb489149373558bf0aaba389a346f5ab57da5cdd3c"

state = {
    "status": "running",
    "stage": "preflight",
    "validation_only": True,
    "test_files_opened": False,
    "training_performed": False,
    "weight_updates": 0,
    "adapter_used": False,
    "started_utc": datetime.now(timezone.utc).isoformat(),
    "validation": None,
}
protocol = {
    "experiment": "frozen_SAM-Med3D-turbo_Thebe_interactive_validation_diagnostic",
    "validation_only": True,
    "test_files_opened": False,
    "training_performed": False,
    "weight_updates": 0,
    "adapter_used": False,
    "patch_size": SIZE,
    "precision": "float16_autocast",
    "seed": SEED,
    "crop_policies": list(CROP_POLICIES),
    "normalizations": list(NORMALIZATIONS),
    "click_checkpoints": list(CLICK_CHECKPOINTS),
    "prompt_policy": (
        "First click is a deterministic GT-positive anchor. Later clicks are sampled "
        "uniformly from current false-negative/false-positive voxels and labelled from GT."
    ),
    "point_history": "latest click only, matching SAM-Med3D default multi_click=False",
    "mask_feedback": (
        "zero 32^3 low-resolution mask on click 1; previous decoder logits on later clicks"
    ),
    "scoring": (
        "micro Dice over observed voxels in GT-positive oracle samples, plus mean/median "
        "per-sample Dice; this is interactive and not an automatic whole-survey result"
    ),
    "threshold_policy": (
        "report fixed 0.5 and best micro-Dice threshold on validation; no test data accessed"
    ),
    "normalization_details": {
        "r100_observed_zscore": (
            "existing R100 reader: statistics over raw nonzero observed voxels; invalid/padding kept zero"
        ),
        "sam_positive_zscore": (
            "TorchIO-equivalent formula used by official SAM-Med3D: statistics over raw values > 0, "
            "then the affine z-score is applied to the entire zero-padded patch"
        ),
    },
    "crop_details": {
        "fixed_positive_grid": "non-overlapping validation grid patches that contain observed fault labels",
        "label_centered": (
            "paired 128^3 crops centered on the exact same deterministic positive anchors; crops may overlap"
        ),
    },
    "limitations": [
        "Thebe provides a binary fault class, not fault-instance IDs; metrics therefore score the full fault class in each sample.",
        "Label-centered crops, prompts, corrective clicks, and empty-patch exclusion use validation labels and are oracle-assisted.",
        "These interactive results are not directly comparable with an automatic R100 whole-survey score.",
    ],
}


def write_json(path, value):
    temporary = path.with_name(path.name + ".part")
    temporary.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")
    temporary.replace(path)


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def point_coordinate_order(model):
    """Derive the prompt-coordinate permutation from the model's own dense PE."""
    pe = model.prompt_encoder.pe_layer
    image_size = tuple(model.prompt_encoder.input_image_size)
    grid_size = tuple(model.prompt_encoder.image_embedding_size)
    if image_size != (SIZE,) * 3:
        raise RuntimeError(f"Unexpected SAM input size: {image_size}")
    cell = (1, 2, 3)
    centers = torch.tensor(
        [[(cell[index] + 0.5) * image_size[index] / grid_size[index] for index in range(3)]],
        device="cuda",
    ).unsqueeze(0)
    reference = pe(grid_size)[:, cell[0], cell[1], cell[2]]
    matches = []
    for candidate in itertools.permutations(range(3)):
        actual = pe.forward_with_coords(centers[..., list(candidate)], image_size)[0, 0]
        if float((actual - reference).abs().max()) < 1e-5:
            matches.append(candidate)
    if len(matches) != 1:
        raise RuntimeError(f"Could not uniquely verify prompt coordinates: {matches}")
    return list(matches[0])


def centered_origin(anchor, shape):
    result = []
    for coordinate, length in zip(anchor, shape):
        if length < SIZE:
            raise RuntimeError(f"Volume axis {length} is smaller than patch size {SIZE}")
        result.append(max(0, min(int(coordinate) - SIZE // 2, length - SIZE)))
    return tuple(result)


def model_to_raw_local(model_voxel):
    return tuple(int(value) for value in reversed(model_voxel))


def raw_to_model_local(raw_voxel):
    return tuple(int(value) for value in reversed(raw_voxel))


def discover_positive_samples(reader):
    coordinates = list(itertools.product(*(range(0, length, SIZE) for length in reader.shape)))
    coverage = {
        "grid_patches": len(coordinates),
        "grid_patches_processed": 0,
        "observed_grid_patches": 0,
        "no_data_grid_patches": 0,
        "positive_grid_patches": 0,
        "fault_free_observed_grid_patches": 0,
        "raw_voxels": 0,
        "valid_voxels": 0,
        "positive_voxels": 0,
        "positive_labels_excluded": 0,
    }
    samples = []
    for number, origin in enumerate(coordinates, 1):
        _, target, mask, _, _, excluded, _ = sam.r100.read_patch(reader, origin)
        valid = mask[0, 0].cpu().numpy().astype(bool)
        truth = target[0, 0].cpu().numpy() >= 0.5
        raw_voxels = math.prod(
            min(SIZE, length - start)
            for length, start in zip(reader.shape, origin)
        )
        observed = int(valid.sum())
        positive = np.flatnonzero(truth & valid)
        coverage["grid_patches_processed"] = number
        coverage["raw_voxels"] += raw_voxels
        coverage["valid_voxels"] += observed
        coverage["positive_voxels"] += int(len(positive))
        coverage["positive_labels_excluded"] += int(excluded)

        if observed == 0:
            coverage["no_data_grid_patches"] += 1
        else:
            coverage["observed_grid_patches"] += 1
            if len(positive) == 0:
                coverage["fault_free_observed_grid_patches"] += 1
            else:
                coverage["positive_grid_patches"] += 1
                generator = np.random.default_rng(SEED + number)
                flat = int(positive[generator.integers(len(positive))])
                model_voxel = tuple(
                    int(value)
                    for value in np.unravel_index(flat, valid.shape)
                )
                raw_local = model_to_raw_local(model_voxel)
                anchor = tuple(
                    int(start + offset)
                    for start, offset in zip(origin, raw_local)
                )
                samples.append({
                    "sample": len(samples) + 1,
                    "source_grid_patch": number,
                    "anchor_raw": anchor,
                    "fixed_positive_grid": tuple(int(value) for value in origin),
                    "label_centered": centered_origin(anchor, reader.shape),
                })

        if number % 50 == 0 or number == len(coordinates):
            print(
                f"scan: patch {number}/{len(coordinates)}; "
                f"positive={coverage['positive_grid_patches']}",
                flush=True,
            )

    if coverage["raw_voxels"] != math.prod(reader.shape):
        raise RuntimeError(
            "Validation grid does not cover the complete volume exactly once"
        )
    if coverage["valid_voxels"] == 0 or not samples:
        raise RuntimeError(
            "No observed GT-positive validation samples were found"
        )

    for policy in CROP_POLICIES:
        origins = [tuple(sample[policy]) for sample in samples]
        coverage[f"{policy}_samples"] = len(origins)
        coverage[f"{policy}_unique_origins"] = len(set(origins))
        coverage[f"{policy}_repeated_origins"] = (
            len(origins) - len(set(origins))
        )

    return samples, coverage


def write_samples(samples):
    with (OUT / "samples.csv").open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow([
            "sample", "source_grid_patch",
            "anchor_raw0", "anchor_raw1", "anchor_raw2",
            "fixed_raw0", "fixed_raw1", "fixed_raw2",
            "centered_raw0", "centered_raw1", "centered_raw2",
        ])
        for sample in samples:
            writer.writerow([
                sample["sample"],
                sample["source_grid_patch"],
                *sample["anchor_raw"],
                *sample["fixed_positive_grid"],
                *sample["label_centered"],
            ])


def sam_positive_normalized_input(reader, origin):
    """Reproduce tio.ZNormalization(masking_method=lambda x: x > 0)."""
    stops = tuple(
        min(start + SIZE, length)
        for start, length in zip(origin, reader.shape)
    )
    raw = reader.read(
        "seismic",
        origin[0], stops[0],
        origin[1], stops[1],
        origin[2], stops[2],
    )
    raw = raw.astype(np.float32, copy=False)
    expected_shape = tuple(
        stop - start for start, stop in zip(origin, stops)
    )
    if raw.shape != expected_shape or not np.isfinite(raw).all():
        raise RuntimeError(
            f"Invalid raw seismic patch at {origin}: "
            f"{raw.shape}, expected {expected_shape}"
        )

    padded = np.zeros((SIZE,) * 3, dtype=np.float32)
    slices = tuple(slice(0, length) for length in expected_shape)
    padded[slices] = raw

    tensor = torch.from_numpy(padded)[None]
    selected = tensor > 0
    count = int(selected.sum().item())
    if count < 2:
        raise RuntimeError(
            f"Fewer than two positive intensities for SAM normalization at {origin}"
        )

    values = tensor[selected]
    mean = values.mean()
    standard_deviation = values.std()
    if (
        not torch.isfinite(standard_deviation).item()
        or not float(standard_deviation) > 0.0
    ):
        raise RuntimeError(
            f"Invalid SAM-positive intensity scale at {origin}"
        )

    normalized = (tensor - mean) / standard_deviation
    if not torch.isfinite(normalized).all().item():
        raise RuntimeError(
            f"Nonfinite SAM-positive normalized input at {origin}"
        )

    model_order = np.ascontiguousarray(
        np.transpose(normalized[0].numpy())
    )
    return torch.from_numpy(model_order)[None, None], {
        "positive_intensity_voxels": count,
        "mean": float(mean),
        "std": float(standard_deviation),
    }


def new_accumulator():
    return {
        "histogram": sam.r100.baseline.ProbabilityHistogram(BINS),
        "patch_dice_at_0_5": [],
        "samples": 0,
        "valid_voxels": 0,
        "positive_voxels": 0,
    }


def record_prediction(accumulator, probability, target, valid_mask):
    scored_probability = probability[valid_mask]
    scored_target = target[valid_mask]
    if scored_probability.numel() == 0:
        raise RuntimeError("Attempted to score an empty sample")

    accumulator["histogram"].update_probabilities(
        scored_probability,
        scored_target.float(),
    )

    predicted = scored_probability >= 0.5
    truth = scored_target.bool()
    true_positive = int((predicted & truth).sum().item())
    false_positive = int((predicted & ~truth).sum().item())
    false_negative = int((~predicted & truth).sum().item())
    denominator = 2 * true_positive + false_positive + false_negative
    if denominator <= 0:
        raise RuntimeError(
            "GT-positive sample produced an undefined Dice denominator"
        )

    accumulator["patch_dice_at_0_5"].append(
        2 * true_positive / denominator
    )
    accumulator["samples"] += 1
    accumulator["valid_voxels"] += int(scored_probability.numel())
    accumulator["positive_voxels"] += int(truth.sum().item())


def summarize_accumulator(accumulator):
    histogram = accumulator["histogram"]
    threshold = float(histogram.best_dice_threshold())
    fixed = asdict(histogram.metrics(0.5))
    calibrated = asdict(histogram.metrics(threshold))
    expected = accumulator["valid_voxels"]

    if sum(fixed[key] for key in ("tp", "fp", "fn", "tn")) != expected:
        raise RuntimeError(
            "Fixed-threshold confusion counts disagree with recorded voxels"
        )
    if (
        sum(
            calibrated[key]
            for key in ("tp", "fp", "fn", "tn")
        )
        != expected
    ):
        raise RuntimeError(
            "Calibrated confusion counts disagree with recorded voxels"
        )

    dice_values = accumulator["patch_dice_at_0_5"]
    return {
        "samples": accumulator["samples"],
        "valid_voxels": accumulator["valid_voxels"],
        "positive_voxels": accumulator["positive_voxels"],
        "positive_prevalence": (
            accumulator["positive_voxels"]
            / accumulator["valid_voxels"]
        ),
        "micro_at_0_5": fixed,
        "validation_threshold": threshold,
        "micro_at_validation_threshold": calibrated,
        "patch_dice_at_0_5": {
            "mean": statistics.fmean(dice_values),
            "median": statistics.median(dice_values),
            "minimum": min(dice_values),
            "maximum": max(dice_values),
        },
    }


def flat_to_voxel(index):
    axis0, remainder = divmod(int(index), SIZE * SIZE)
    axis1, axis2 = divmod(remainder, SIZE)
    return axis0, axis1, axis2


def run_interaction(
    x,
    target,
    mask,
    sample,
    policy,
    normalization,
    accumulators,
    clicks_writer,
):
    origin = tuple(sample[policy])
    raw_local = tuple(
        anchor - start
        for anchor, start in zip(sample["anchor_raw"], origin)
    )
    if any(value < 0 or value >= SIZE for value in raw_local):
        raise RuntimeError(
            f"Anchor escaped {policy} crop: {sample}"
        )

    anchor_model = raw_to_model_local(raw_local)
    truth_cpu = target[0, 0].bool()
    valid_cpu = mask[0, 0].bool()
    if (
        not bool(valid_cpu[anchor_model].item())
        or not bool(truth_cpu[anchor_model].item())
    ):
        raise RuntimeError(
            f"Anchor is not an observed positive voxel: {sample}"
        )

    truth = target.to("cuda").bool()
    valid = mask.to("cuda").bool()
    x_gpu = x.to("cuda")
    generator = np.random.default_rng(
        SEED
        + int(sample["sample"]) * 1009
        + CROP_POLICIES.index(policy) * 1_000_003
        + NORMALIZATIONS.index(normalization) * 10_000_019
    )
    recorded = set()

    with torch.inference_mode(), torch.autocast(
        "cuda",
        dtype=torch.float16,
    ):
        embedding = model.image_encoder(x_gpu)
        low_resolution_mask = torch.zeros(
            (1, 1, SIZE // 4, SIZE // 4, SIZE // 4),
            dtype=torch.float32,
            device="cuda",
        )
        full_logits = torch.zeros_like(
            truth,
            dtype=torch.float32,
        )

        for click_number in range(1, MAX_CLICKS + 1):
            if click_number == 1:
                model_voxel = anchor_model
                point_label_value = 1
                click_kind = "positive_anchor"
            else:
                prediction = full_logits > 0.0
                error = (prediction != truth) & valid
                candidates = torch.nonzero(
                    error.reshape(-1),
                    as_tuple=False,
                ).reshape(-1)

                if candidates.numel() == 0:
                    probability = torch.sigmoid(full_logits.float())
                    for checkpoint in CLICK_CHECKPOINTS:
                        if checkpoint not in recorded:
                            record_prediction(
                                accumulators[checkpoint],
                                probability,
                                truth,
                                valid,
                            )
                            recorded.add(checkpoint)

                    clicks_writer.writerow([
                        policy,
                        normalization,
                        sample["sample"],
                        click_number,
                        "converged_no_error",
                        *origin,
                        *sample["anchor_raw"],
                        "", "", "",
                        "", "", "",
                        "",
                    ])
                    break

                selected_position = int(
                    generator.integers(int(candidates.numel()))
                )
                selected_flat = int(
                    candidates[selected_position].item()
                )
                model_voxel = flat_to_voxel(selected_flat)
                point_label_value = int(
                    truth[0, 0][model_voxel].item()
                )
                click_kind = (
                    "corrective_positive"
                    if point_label_value
                    else "corrective_negative"
                )

            prompt_voxel = tuple(
                model_voxel[index] for index in point_order
            )
            point = torch.tensor(
                prompt_voxel,
                dtype=torch.float32,
                device="cuda",
            )[None, None]
            point_label = torch.tensor(
                [[point_label_value]],
                dtype=torch.int64,
                device="cuda",
            )

            sparse, dense = model.prompt_encoder(
                points=(point, point_label),
                boxes=None,
                masks=low_resolution_mask,
            )
            low_resolution_mask, _ = model.mask_decoder(
                image_embeddings=embedding,
                image_pe=model.prompt_encoder.get_dense_pe(),
                sparse_prompt_embeddings=sparse,
                dense_prompt_embeddings=dense,
                multimask_output=False,
            )
            full_logits = F.interpolate(
                low_resolution_mask,
                size=(SIZE,) * 3,
                mode="trilinear",
                align_corners=False,
            )

            if tuple(full_logits.shape) != (
                1, 1, SIZE, SIZE, SIZE
            ):
                raise RuntimeError(
                    f"Unexpected decoder output shape: "
                    f"{tuple(full_logits.shape)}"
                )
            if not torch.isfinite(full_logits).all().item():
                raise RuntimeError(
                    f"Nonfinite output: policy={policy}, "
                    f"norm={normalization}, "
                    f"sample={sample['sample']}, "
                    f"click={click_number}"
                )

            clicks_writer.writerow([
                policy,
                normalization,
                sample["sample"],
                click_number,
                click_kind,
                *origin,
                *sample["anchor_raw"],
                *model_voxel,
                *prompt_voxel,
                point_label_value,
            ])

            if click_number in CLICK_CHECKPOINTS:
                probability = torch.sigmoid(full_logits.float())
                record_prediction(
                    accumulators[click_number],
                    probability,
                    truth,
                    valid,
                )
                recorded.add(click_number)

    if recorded != set(CLICK_CHECKPOINTS):
        raise RuntimeError(
            f"Missing click checkpoints for sample "
            f"{sample['sample']}: {recorded}"
        )


def make_report():
    lines = [
        "# SAM-Med3D interactive Thebe validation diagnostic",
        "",
        f"Status: **{state['status']}**.",
        "",
        "This run is validation-only. It does not open Thebe test files, "
        "train weights, or use an adapter.",
        "It compares the two normalization and crop choices using "
        "zero/previous-mask feedback and corrective clicks.",
        "All reported results are oracle-assisted because labels define "
        "samples, prompts, corrections, and scoring.",
        "They are not automatic whole-survey results and are not directly "
        "comparable with R100 Dice.",
        "",
    ]

    validation = state.get("validation")
    if validation and validation.get("rows"):
        lines.extend([
            "| Crop | Normalization | Clicks | Micro Dice @ 0.5 | "
            "Mean patch Dice @ 0.5 | Val threshold | "
            "Micro Dice @ val threshold | Precision | Recall | ROC-AUC |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: | "
            "---: | ---: | ---: |",
        ])

        for row in validation["rows"]:
            fixed = row["metrics"]["micro_at_0_5"]
            calibrated = row["metrics"][
                "micro_at_validation_threshold"
            ]
            lines.append(
                f"| {row['crop_policy']} | "
                f"{row['normalization']} | "
                f"{row['clicks']} | "
                f"{fixed['dice']:.6f} | "
                f"{row['metrics']['patch_dice_at_0_5']['mean']:.6f} | "
                f"{row['metrics']['validation_threshold']:.9f} | "
                f"{calibrated['dice']:.6f} | "
                f"{calibrated['precision']:.6f} | "
                f"{calibrated['recall']:.6f} | "
                f"{calibrated['roc_auc_approx']:.6f} |"
            )

        selection = validation.get("selection", {})
        if selection:
            lines.extend([
                "",
                "## Validation-only ranking",
                "",
                "Best five-click fixed-0.5 configuration: "
                f"`{selection['best_five_click_at_0_5']['key']}` "
                "with Dice "
                f"{selection['best_five_click_at_0_5']['dice']:.6f}.",
                "Best five-click validation-calibrated configuration: "
                f"`{selection['best_five_click_calibrated']['key']}` "
                "with Dice "
                f"{selection['best_five_click_calibrated']['dice']:.6f}.",
                "These are diagnostic rankings on validation, "
                "not held-out test results.",
            ])

    lines.extend([
        "",
        "## Interpretation limits",
        "",
        "- Thebe contains a binary fault class but no fault-instance IDs, "
        "so the full fault mask in each crop is scored.",
        "- Label-centered crops can overlap; their metrics are sample "
        "metrics, not unique survey-volume coverage.",
        "- A later held-out test must freeze the chosen normalization, "
        "crop rule, click policy, and threshold first.",
        "",
        "Evidence: `protocol.json`, `samples.csv`, `clicks.csv`, "
        "`validation_metrics.json`, `selection.json`, `evaluate.py`, "
        "source snapshots, and `console.log`.",
    ])

    if "error" in state:
        lines.extend([
            "",
            "## Failure",
            "",
            "```text",
            state["traceback"],
            "```",
        ])

    (OUT / "report.md").write_text("\n".join(lines) + "\n")


try:
    import numpy as np
    import torch
    from torch.nn import functional as F

    state["stage"] = "source_preflight"
    helper = ROOT / "scripts/train_sammed3d_thebe.py"
    if (
        not helper.is_file()
        or sha256(helper) != EXPECTED_HELPER_SHA
    ):
        raise RuntimeError(
            "SAM helper changed or is missing; "
            "refusing an unreviewed protocol"
        )

    sys.path.insert(0, str(ROOT / "scripts"))
    import train_sammed3d_thebe as sam

    if sam.sam_source_commit() != EXPECTED_SAM_COMMIT:
        raise RuntimeError(
            "SAM-Med3D source commit changed; "
            "refusing an unreviewed implementation"
        )
    if (
        not torch.cuda.is_available()
        or torch.cuda.mem_get_info()[0] < 10 * 1024**3
    ):
        raise RuntimeError(
            "CUDA with at least 10 GiB free memory is required"
        )

    checkpoint = (
        ROOT
        / "external/SAM-Med3D/ckpt/sam_med3d_turbo.pth"
    )
    if (
        not checkpoint.is_file()
        or sha256(checkpoint) != EXPECTED_CHECKPOINT_SHA
    ):
        raise RuntimeError(
            "Original SAM-Med3D-Turbo checkpoint is missing or changed"
        )

    validation_paths = [
        ROOT / "data/processed/thebe_h5" / f"val{index}.h5"
        for index in (1, 2)
    ]
    if not all(path.is_file() for path in validation_paths):
        raise RuntimeError("Missing val1.h5 or val2.h5")
    if len({path.resolve() for path in validation_paths}) != 2:
        raise RuntimeError("Validation paths overlap")

    source_paths = [
        helper,
        ROOT / "scripts/train_r100_fp16_clean.py",
        ROOT / "scripts/faultseg3d_baseline.py",
    ]
    protocol["source_hashes"] = {}
    for source in source_paths:
        if not source.is_file():
            raise RuntimeError(
                f"Missing reviewed source: {source}"
            )
        relative = source.relative_to(ROOT)
        protocol["source_hashes"][str(relative)] = sha256(source)
        destination = OUT / "source_snapshot" / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(source.read_bytes())

    protocol["validation_files"] = [
        {
            "path": str(path.relative_to(ROOT)),
            "bytes": path.stat().st_size,
            "mtime_ns": path.stat().st_mtime_ns,
        }
        for path in validation_paths
    ]
    protocol["checkpoint_sha256"] = EXPECTED_CHECKPOINT_SHA
    protocol["sam_commit"] = EXPECTED_SAM_COMMIT
    protocol["gpu"] = torch.cuda.get_device_name(0)
    protocol["torch"] = str(torch.__version__)
    protocol["evaluator_sha256"] = sha256(
        Path(__file__).resolve()
    )

    torch.manual_seed(SEED)
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True
    torch.cuda.reset_peak_memory_stats()

    model = sam.sam_model_registry3D["vit_b_ori"](
        checkpoint=None
    )
    model.load_state_dict(
        sam.checkpoint_state(checkpoint),
        strict=True,
    )
    model.eval().requires_grad_(False).to("cuda")

    with torch.inference_mode():
        point_order = point_coordinate_order(model)

    protocol["point_coordinate_order"] = point_order
    write_json(OUT / "protocol.json", protocol)

    state["stage"] = "discover_validation_samples"
    reader = sam.r100.ConcatenatedThebe(validation_paths)

    try:
        if tuple(reader.shape) != (200, 3174, 1537):
            raise RuntimeError(
                f"Unexpected validation shape: {reader.shape}"
            )

        samples, discovery = discover_positive_samples(reader)
        write_samples(samples)

        accumulators = {
            policy: {
                normalization: {
                    clicks: new_accumulator()
                    for clicks in CLICK_CHECKPOINTS
                }
                for normalization in NORMALIZATIONS
            }
            for policy in CROP_POLICIES
        }
        normalization_audit = {
            policy: {
                "samples": 0,
                "positive_intensity_voxels": 0,
                "mean_sum": 0.0,
                "std_sum": 0.0,
            }
            for policy in CROP_POLICIES
        }

        total_interactions = (
            len(samples)
            * len(CROP_POLICIES)
            * len(NORMALIZATIONS)
        )
        completed_interactions = 0
        evaluation_started = time.monotonic()
        state["stage"] = "interactive_validation"

        with (OUT / "clicks.csv").open(
            "w",
            newline="",
        ) as click_handle:
            clicks_writer = csv.writer(click_handle)
            clicks_writer.writerow([
                "crop_policy",
                "normalization",
                "sample",
                "click",
                "kind",
                "origin_raw0",
                "origin_raw1",
                "origin_raw2",
                "anchor_raw0",
                "anchor_raw1",
                "anchor_raw2",
                "model_axis0",
                "model_axis1",
                "model_axis2",
                "prompt_axis0",
                "prompt_axis1",
                "prompt_axis2",
                "label",
            ])

            for policy in CROP_POLICIES:
                for sample in samples:
                    origin = tuple(sample[policy])
                    (
                        x_r100,
                        target,
                        mask,
                        _,
                        observed,
                        _,
                        constant,
                    ) = sam.r100.read_patch(reader, origin)

                    if tuple(x_r100.shape) != (
                        1, 1, SIZE, SIZE, SIZE
                    ):
                        raise RuntimeError(
                            f"Unexpected R100 input shape at {origin}: "
                            f"{tuple(x_r100.shape)}"
                        )
                    if (
                        target.shape != x_r100.shape
                        or mask.shape != x_r100.shape
                    ):
                        raise RuntimeError(
                            f"Target/mask shape mismatch at {origin}"
                        )
                    if observed <= 0 or constant:
                        raise RuntimeError(
                            "Oracle sample has no usable seismic "
                            f"variation at {origin}"
                        )

                    x_sam, audit = (
                        sam_positive_normalized_input(
                            reader,
                            origin,
                        )
                    )
                    entry = normalization_audit[policy]
                    entry["samples"] += 1
                    entry["positive_intensity_voxels"] += (
                        audit["positive_intensity_voxels"]
                    )
                    entry["mean_sum"] += audit["mean"]
                    entry["std_sum"] += audit["std"]

                    inputs = {
                        "r100_observed_zscore": x_r100,
                        "sam_positive_zscore": x_sam,
                    }

                    for normalization in NORMALIZATIONS:
                        run_interaction(
                            inputs[normalization],
                            target,
                            mask,
                            sample,
                            policy,
                            normalization,
                            accumulators[policy][normalization],
                            clicks_writer,
                        )
                        completed_interactions += 1

                        if (
                            completed_interactions % 10 == 0
                            or completed_interactions
                            == total_interactions
                        ):
                            click_handle.flush()
                            progress = {
                                "stage": state["stage"],
                                "completed_interactions":
                                    completed_interactions,
                                "total_interactions":
                                    total_interactions,
                                "crop_policy": policy,
                                "normalization": normalization,
                                "sample": sample["sample"],
                                "minutes": round(
                                    (
                                        time.monotonic()
                                        - evaluation_started
                                    )
                                    / 60,
                                    2,
                                ),
                                "test_files_opened": False,
                            }
                            write_json(
                                OUT / "progress.json",
                                progress,
                            )
                            print(
                                "interactive: "
                                f"{completed_interactions}/"
                                f"{total_interactions}; "
                                f"policy={policy}; "
                                f"norm={normalization}; "
                                f"sample={sample['sample']}; "
                                f"minutes={progress['minutes']}",
                                flush=True,
                            )

        rows = []
        nested_metrics = {}

        for policy in CROP_POLICIES:
            nested_metrics[policy] = {}
            audit = normalization_audit[policy]
            audit["mean_of_patch_positive_means"] = (
                audit.pop("mean_sum") / audit["samples"]
            )
            audit["mean_of_patch_positive_stds"] = (
                audit.pop("std_sum") / audit["samples"]
            )

            for normalization in NORMALIZATIONS:
                nested_metrics[policy][normalization] = {}

                for clicks in CLICK_CHECKPOINTS:
                    metrics = summarize_accumulator(
                        accumulators[policy][normalization][clicks]
                    )
                    nested_metrics[policy][normalization][
                        str(clicks)
                    ] = metrics
                    row = {
                        "crop_policy": policy,
                        "normalization": normalization,
                        "clicks": clicks,
                        "key": (
                            f"{policy}/{normalization}/"
                            f"{clicks}_clicks"
                        ),
                        "metrics": metrics,
                    }
                    rows.append(row)
                    print(
                        f"RESULT {row['key']} "
                        "Dice@0.5="
                        f"{metrics['micro_at_0_5']['dice']:.6f} "
                        "Dice@val_threshold="
                        f"{metrics['micro_at_validation_threshold']['dice']:.6f}",
                        flush=True,
                    )

        five_click_rows = [
            row for row in rows if row["clicks"] == 5
        ]
        best_fixed = max(
            five_click_rows,
            key=lambda row:
                row["metrics"]["micro_at_0_5"]["dice"],
        )
        best_calibrated = max(
            five_click_rows,
            key=lambda row:
                row["metrics"][
                    "micro_at_validation_threshold"
                ]["dice"],
        )

        selection = {
            "source": "val1.h5 + val2.h5 only",
            "test_files_opened": False,
            "ranking_scope":
                "oracle-assisted GT-positive interactive samples",
            "best_five_click_at_0_5": {
                "key": best_fixed["key"],
                "dice": best_fixed[
                    "metrics"
                ]["micro_at_0_5"]["dice"],
            },
            "best_five_click_calibrated": {
                "key": best_calibrated["key"],
                "threshold": best_calibrated[
                    "metrics"
                ]["validation_threshold"],
                "dice": best_calibrated[
                    "metrics"
                ]["micro_at_validation_threshold"]["dice"],
            },
            "warning": (
                "This ranking may define a later frozen interactive "
                "test protocol; it is not an automatic detector selection."
            ),
        }

        validation = {
            "split": "validation only",
            "files": [
                str(path.relative_to(ROOT))
                for path in validation_paths
            ],
            "shape": list(reader.shape),
            "discovery": discovery,
            "normalization_audit": normalization_audit,
            "seconds": time.monotonic() - evaluation_started,
            "metrics": nested_metrics,
            "rows": rows,
            "selection": selection,
        }
        state["validation"] = validation
        write_json(
            OUT / "validation_metrics.json",
            validation,
        )
        write_json(OUT / "selection.json", selection)

    finally:
        reader.close()

    state["peak_gpu_allocated_gib"] = (
        torch.cuda.max_memory_allocated() / 1024**3
    )
    state["status"] = "complete"
    state["stage"] = "complete"

except Exception as exception:
    state["status"] = "failed"
    state["error"] = repr(exception)
    state["traceback"] = traceback.format_exc()

finally:
    state["finished_utc"] = (
        datetime.now(timezone.utc).isoformat()
    )
    protocol["test_files_opened"] = False
    write_json(OUT / "protocol.json", protocol)
    make_report()
    write_json(OUT / "final_metrics.json", state)

print("STATUS=" + state["status"], flush=True)
if "error" in state:
    print(state["traceback"], flush=True)
print("REPORT=" + str(OUT / "report.md"), flush=True)
print(
    "METRICS=" + str(OUT / "validation_metrics.json"),
    flush=True,
)
print("TEST_FILES_OPENED=false", flush=True)

if state["status"] != "complete":
    raise SystemExit(1)
