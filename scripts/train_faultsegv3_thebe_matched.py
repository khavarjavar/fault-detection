#!/usr/bin/env python3
"""Train FaultSegV3 as a matched high-resolution architecture control on Thebe.

This deliberately reuses the completed FaultEdgeFormer architecture-control
trainer so data files, 128-cube sampling, masking, normalization, BCE, Adam,
checkpoint selection, and validation coverage stay aligned with R100. Only the
model changes. The released FaultSegV3 checkpoint is not loaded: this run tests
the high-resolution architecture from random initialization, not transfer.
"""

from __future__ import annotations

import sys
from pathlib import Path

import torch
from torch import nn


ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = ROOT / "external/FaultSegV3"
sys.path.insert(0, str(UPSTREAM))

from framework.FaultSegV3 import FaultSegV3  # noqa: E402
import train_faultedgeformer_thebe as trainer  # noqa: E402


class FaultSegV3Logits(FaultSegV3):
    """Official c=8 network with its parameter-free sigmoid removed."""

    def __init__(self, use_checkpoint: bool = True) -> None:
        del use_checkpoint
        super().__init__(c=8, out_channels=1, drop_path_rate=0.0)
        if not isinstance(self.dec_out[-1], nn.Sigmoid):
            raise RuntimeError("Unexpected FaultSegV3 output head")
        self.dec_out[-1] = nn.Identity()
        self.spec = {
            "upstream": "douyimin/FaultSegV3",
            "upstream_commit": "b0e62ee1752e966ab182c5b2ed5ed08cff22ed02",
            "channels_c": 8,
            "output": "logits (upstream parameter-free sigmoid removed)",
            "initialization": "random",
            "main_path_downsampling_stages": 1,
            "full_resolution_skip": True,
            "drop_path_rate": 0.0,
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
            "experiment": "FaultSegV3_Thebe_matched_high_resolution_architecture_control",
            "paper": "https://github.com/douyimin/FaultSegV3",
            "claim_scope": (
                "matched local architecture control using official model source; "
                "not a manuscript reproduction or pretrained fine-tune"
            ),
            "model_class": "train_faultsegv3_thebe_matched.FaultSegV3Logits",
            "model_spec": model.spec,
            "initialization": "random; released faultsegv3.ckpt not loaded",
            "comparison_control": (
                "R100 data, 128^3 crop sequence, validity mask, normalization, "
                "augmentation, masked BCE, Adam, step budget, checkpoint rule, "
                "and validation evaluator retained; architecture changed"
            ),
            "hypothesis": (
                "R100 loses thin-fault position and separation through three "
                "downsampling stages; FaultSegV3 preserves a full-resolution "
                "branch and downsamples the main path only once"
            ),
            "known_deviations_from_upstream_training": [
                "random initialization isolates architecture from synthetic pretraining",
                "masked BCE and Adam retained from R100 instead of MaskDice and AdamW",
                "R100 target-domain crops and augmentation replace upstream synthetic recipe",
                "drop-path disabled to avoid adding a second regularization factor",
                "checkpoint selected by fixed-subset validation PR-AUC",
            ],
        }
    )
    config.pop("paper_reported_parameters", None)
    return config


trainer.EXPERIMENT = "FaultSegV3_Thebe_matched_high_resolution_architecture_control"
trainer.PAPER_DOI = "https://github.com/douyimin/FaultSegV3"
trainer.SOURCE_FILES = (
    Path("scripts/train_faultsegv3_thebe_matched.py"),
    Path("scripts/train_faultedgeformer_thebe.py"),
    Path("scripts/train_r100_fp16_clean.py"),
    Path("scripts/faultseg3d_baseline.py"),
    Path("scripts/evaluate_thebe_zero_shot_r100_pinned.py"),
    Path("external/FaultSegV3/framework/FaultSegV3.py"),
)
trainer.FaultEdgeFormerInspired = FaultSegV3Logits
trainer.count_parameters = count_parameters
trainer.make_config = make_config


if __name__ == "__main__":
    raise SystemExit(trainer.main())
