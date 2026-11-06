#!/usr/bin/env python3
"""One labeled 128-cube MONAI SwinUNETR training step on Thebe train data."""

from __future__ import annotations

import json
import random
from pathlib import Path

import numpy as np
import torch
from monai.networks.nets import SwinUNETR

import train_r100_fp16_clean as r100


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA GPU required")
    seed = 42
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    reader = r100.ConcatenatedThebe(r100.split_paths(ROOT / "data/processed/thebe_h5", "train", 9))
    try:
        rng = random.Random(seed)
        for _ in range(60):
            origin = (rng.randrange(0, 100), rng.randrange(0, reader.shape[1] - 128),
                      rng.randrange(0, reader.shape[2] - 128))
            x, target, mask, _, observed, _, constant = r100.read_patch(reader, origin)
            if observed >= 128**3 // 2 and target[mask].sum() > 0 and not constant:
                break
        else:
            raise RuntimeError("Could not find an observed labelled train patch")
    finally:
        reader.close()
    x, target, mask = x.cuda(), target.cuda(), mask.cuda()
    model = SwinUNETR(in_channels=1, out_channels=1, feature_size=24,
                      use_checkpoint=True, spatial_dims=3).train().cuda()
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4)
    parameter = next(model.parameters())
    before = parameter.detach().clone()
    torch.cuda.reset_peak_memory_stats()
    optimizer.zero_grad(set_to_none=True)
    with torch.autocast("cuda", dtype=torch.bfloat16):
        logits = model(x)
    if logits.shape != target.shape or not torch.isfinite(logits).all():
        raise RuntimeError("Invalid training prediction")
    loss = torch.nn.functional.binary_cross_entropy_with_logits(logits.float()[mask], target[mask])
    if not torch.isfinite(loss):
        raise RuntimeError("Invalid loss")
    loss.backward()
    if parameter.grad is None or not torch.isfinite(parameter.grad).all():
        raise RuntimeError("Missing or invalid gradient")
    optimizer.step()
    delta = (parameter.detach() - before).abs().max().item()
    if not np.isfinite(delta) or delta <= 0:
        raise RuntimeError("Training step did not update weights")
    result = {"status": "single_training_step_pass", "architecture": "MONAI SwinUNETR",
              "feature_size": 24, "use_checkpoint": True, "patch_size": [128, 128, 128],
              "parameters": sum(p.numel() for p in model.parameters()),
              "origin": list(origin), "valid_voxels": observed,
              "positive_voxels": int(target[mask].sum().item()),
              "loss": float(loss.item()), "max_parameter_delta": delta,
              "peak_gpu_allocated_gib": torch.cuda.max_memory_allocated() / 1024**3,
              "peak_gpu_reserved_gib": torch.cuda.max_memory_reserved() / 1024**3,
              "precision": "bfloat16_autocast, float32 masked BCE and weights",
              "purpose": "memory/gradient feasibility only; random initialization; no checkpoint saved",
              "test_files_read": False}
    output = ROOT / "reports/evaluation/swinunetr_training_preflight_20261102.json"
    if output.exists():
        raise FileExistsError(output)
    r100.write_json_atomic(output, result)
    print(json.dumps(result, indent=2), flush=True)


if __name__ == "__main__":
    main()
