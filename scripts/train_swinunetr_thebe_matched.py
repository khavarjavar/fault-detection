#!/usr/bin/env python3
"""Train MONAI SwinUNETR as a matched context-architecture control on Thebe.

This reuses the R100-compatible architecture-control trainer so the Thebe
files, 128-cube sampling, validity mask, normalization, augmentation, masked
BCE, Adam optimizer, seed, step budget, checkpoint rule, and validation
evaluator remain fixed. Only the network changes.
"""

from __future__ import annotations

from pathlib import Path

import torch
from monai.networks.nets import SwinUNETR

import train_faultedgeformer_thebe as trainer


class SwinUNETRMatched(SwinUNETR):
    """Official MONAI SwinUNETR configuration that passed the 128-cube preflight."""

    def __init__(self, use_checkpoint: bool = True) -> None:
        super().__init__(
            in_channels=1,
            out_channels=1,
            feature_size=24,
            use_checkpoint=use_checkpoint,
            spatial_dims=3,
        )
        self.spec = {
            "implementation": "monai.networks.nets.SwinUNETR",
            "monai_version": __import__("monai").__version__,
            "in_channels": 1,
            "out_channels": 1,
            "feature_size": 24,
            "spatial_dims": 3,
            "use_checkpoint": use_checkpoint,
            "initialization": "random",
        }


def count_parameters(model: torch.nn.Module) -> int:
    return sum(parameter.numel() for parameter in model.parameters() if parameter.requires_grad)


_original_make_config = trainer.make_config


def make_config(args, model, train_files, val_files, val_subset, all_val):
    config = _original_make_config(
        args, model, train_files, val_files, val_subset, all_val
    )
    config.update(
        {
            "experiment": "MONAI_SwinUNETR_Thebe_matched_context_architecture_control",
            "paper": "https://arxiv.org/abs/2201.01266",
            "implementation": "https://docs.monai.io/en/stable/networks.html#swinunetr",
            "claim_scope": (
                "matched local architecture control using the official MONAI model; "
                "not a reproduction of FaultSeg Swin-UNETR or SimMIM pretraining"
            ),
            "model_class": "train_swinunetr_thebe_matched.SwinUNETRMatched",
            "model_spec": model.spec,
            "initialization": "random; no medical, ImageNet, or seismic pretraining",
            "comparison_control": (
                "R100 data, 128^3 crop sequence, validity mask, normalization, "
                "augmentation, masked BCE, Adam, step budget, checkpoint rule, "
                "and validation evaluator retained; architecture changed"
            ),
            "hypothesis": (
                "shifted-window attention and hierarchical global context recover weak "
                "or interrupted faults that local convolutional models miss"
            ),
            "known_deviations_from_paper": [
                "random initialization isolates architecture from self-supervised pretraining",
                "R100 masked BCE, Adam, crops, and augmentation replace paper recipes",
                "feature_size 24 is the locally preflighted single-GPU configuration",
                "checkpoint selected by fixed-subset validation PR-AUC",
            ],
        }
    )
    config.pop("paper_reported_parameters", None)
    return config


trainer.EXPERIMENT = "MONAI_SwinUNETR_Thebe_matched_context_architecture_control"
trainer.PAPER_DOI = "https://arxiv.org/abs/2201.01266"
trainer.SOURCE_FILES = (
    Path("scripts/train_swinunetr_thebe_matched.py"),
    Path("scripts/train_faultedgeformer_thebe.py"),
    Path("scripts/train_r100_fp16_clean.py"),
    Path("scripts/faultseg3d_baseline.py"),
    Path("scripts/evaluate_thebe_zero_shot_r100_pinned.py"),
)
trainer.FaultEdgeFormerInspired = SwinUNETRMatched
trainer.count_parameters = count_parameters
trainer.make_config = make_config


if __name__ == "__main__":
    raise SystemExit(trainer.main())
