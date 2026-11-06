#!/usr/bin/env python3
"""One reversible 128^3 FaultSegV3 training step on Thebe train data."""

from __future__ import annotations

import json
import random
from pathlib import Path

import numpy as np
import torch

import train_r100_fp16_clean as r100
from evaluate_thebe_zero_shot_r100_pinned import ConcatenatedThebe
from evaluate_faultsegv3_validation import ROOT, UPSTREAM, raw_input, upstream_normalize
from framework.FaultSegV3 import FaultSegV3


def main() -> None:
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA GPU required")
    seed = 42
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    reader = ConcatenatedThebe(r100.split_paths(ROOT / "data/processed/thebe_h5", "train", 9))
    try:
        rng = random.Random(seed)
        for _ in range(60):
            origin = (rng.randrange(0, 100), rng.randrange(0, reader.shape[1] - 128),
                      rng.randrange(0, reader.shape[2] - 128))
            _, target, mask, _, observed, _, constant = r100.read_patch(reader, origin)
            if observed >= 128**3 // 2 and target[mask].sum() > 0 and not constant:
                break
        else:
            raise RuntimeError("Could not find an observed labelled train patch")
        x = raw_input(reader, origin).cuda()
    finally:
        reader.close()

    target = target.cuda()
    mask = mask.cuda()
    weights = UPSTREAM / "framework/faultsegv3.ckpt"
    state = torch.load(weights, map_location="cpu", weights_only=True)
    model = FaultSegV3(c=8).train().cuda()
    model.load_state_dict(state, strict=True)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4)
    parameter = next(model.parameters())
    before = parameter.detach().clone()
    torch.cuda.reset_peak_memory_stats()
    optimizer.zero_grad(set_to_none=True)
    with torch.autocast("cuda", dtype=torch.bfloat16):
        probability = model.forward_raw(upstream_normalize(x))
    if probability.shape != target.shape or not torch.isfinite(probability).all():
        raise RuntimeError("Invalid training prediction")
    scored_prediction = probability.float()[mask]
    scored_target = target[mask]
    numerator = 2 * (scored_prediction * scored_target).sum() + 1
    denominator = scored_prediction.sum() + scored_target.sum() + 1
    loss = 1 - numerator / denominator
    if not torch.isfinite(loss):
        raise RuntimeError("Invalid training loss")
    loss.backward()
    gradient = parameter.grad
    if gradient is None or not torch.isfinite(gradient).all():
        raise RuntimeError("Missing or invalid parameter gradient")
    optimizer.step()
    delta = (parameter.detach() - before).abs().max().item()
    if not np.isfinite(delta) or delta <= 0:
        raise RuntimeError("Training step did not update model weights")
    result = {
        "status": "single_training_step_pass",
        "origin": list(origin),
        "valid_voxels": observed,
        "positive_voxels": int(scored_target.sum().item()),
        "loss": float(loss.item()),
        "max_parameter_delta": delta,
        "peak_gpu_allocated_gib": torch.cuda.max_memory_allocated() / 1024**3,
        "peak_gpu_reserved_gib": torch.cuda.max_memory_reserved() / 1024**3,
        "precision": "bfloat16_autocast with float32 loss and weights",
        "purpose": "memory and gradient preflight only; no checkpoint saved",
        "test_files_read": False,
    }
    output = ROOT / "reports/evaluation/faultsegv3_training_preflight_20261102.json"
    if output.exists():
        raise FileExistsError(output)
    r100.write_json_atomic(output, result)
    print(json.dumps(result, indent=2), flush=True)


if __name__ == "__main__":
    main()
