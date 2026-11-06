#!/usr/bin/env python3
"""Synthetic batch-64 forward/backward memory preflight for author baselines."""

from __future__ import annotations

import gc
import os
import sys
from pathlib import Path

os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")

import torch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from thebe_author_2d_models import author_loss, create_model  # noqa: E402


def main() -> int:
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA required")
    for name in ("hed", "rcf", "unet", "deeplabm"):
        torch.cuda.empty_cache()
        torch.cuda.reset_peak_memory_stats()
        model = create_model(name).cuda().train()
        image = torch.randn(64, 1, 96, 96, device="cuda")
        target = (torch.rand(64, 1, 96, 96, device="cuda") > 0.97).float()
        output = model(image)
        loss = author_loss(name, output, target)
        loss.backward()
        print(
            f"{name} loss={float(loss):.6f} "
            f"peak_allocated_gib={torch.cuda.max_memory_allocated()/1024**3:.3f} "
            f"peak_reserved_gib={torch.cuda.max_memory_reserved()/1024**3:.3f}",
            flush=True,
        )
        del loss, output, target, image, model
        gc.collect()
        torch.cuda.empty_cache()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
