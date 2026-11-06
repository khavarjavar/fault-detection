# FaultSeg3D Architecture Check

- Model source: `scripts/faultseg3d_baseline.py`

```python
#!/usr/bin/env python3
"""Train an architecture-faithful PyTorch FaultSeg3D baseline.

The network mirrors xinwucwp/faultSeg/unet3.py: channels 16/32/64/128,
two 3x3x3 convolutions per level, max pooling, nearest-neighbour upsampling,
skip concatenation, and a 1x1x1 output convolution.  The PyTorch module emits
logits so the loss can use numerically stable BCEWithLogitsLoss.

Two controlled runs are supported:

* b0_bce: official architecture with ordinary BCE (the active loss in the
  public training script).
* b1_weighted_dice: the identical architecture with train-only pos_weight and
  soft Dice, isolating imbalance handling from architectural changes.

Expected project layout:

  data/faultseg3d/train/{seis,fault}/*.dat
  data/faultseg3d/validation/{seis,fault}/*.dat
  data/manifests/faultseg3d_{train,val,test}.txt
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import random
import time
from contextlib import nullcontext
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
import torch
from torch import Tensor, nn
from torch.utils.data import DataLoader, Dataset


VOLUME_SHAPE = (128, 128, 128)
EXPECTED_PARAMETERS = 1_459_585
DEFAULT_POS_WEIGHT = 13.211662


def seed_everything(seed: int) -> None:
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True
    torch.use_deterministic_algorithms(True, warn_only=True)


class DoubleConv(nn.Module):
    def __init__(self, in_channels: int, out_channels: int) -> None:
        super().__init__()
        self.block = nn.Sequential(
            nn.Conv3d(in_channels, out_channels, kernel_size=3, padding=1, bias=True),
            nn.ReLU(inplace=True),
            nn.Conv3d(out_channels, out_channels, kernel_size=3, padding=1, bias=True),
            nn.ReLU(inplace=True),
        )

    def forward(self, x: Tensor) -> Tensor:
        return self.block(x)


class FaultSeg3D(nn.Module):
    """Simplified 3D U-Net from the official FaultSeg3D repository."""

    def __init__(self) -> None:
        super().__init__()
        self.enc1 = DoubleConv(1, 16)
        self.enc2 = DoubleConv(16, 32)
        self.enc3 = DoubleConv(32, 64)
        self.bottleneck = DoubleConv(64, 128)
        self.pool = nn.MaxPool3d(kernel_size=2, stride=2)
        self.up = nn.Upsample(scale_factor=2, mode="nearest")
        self.dec3 = DoubleConv(128 + 64, 64)
        self.dec2 = DoubleConv(64 + 32, 32)
        self.dec1 = DoubleConv(32 + 16, 16)
        self.output = nn.Conv3d(16, 1, kernel_size=1, bias=True)

    def forward(self, x: Tensor) -> Tensor:
        e1 = self.enc1(x)
        e2 = self.enc2(self.pool(e1))
        e3 = self.enc3(self.pool(e2))
        b = self.bottleneck(self.pool(e3))
        d3 = self.dec3(torch.cat((self.up(b), e3), dim=1))
        d2 = self.dec2(torch.cat((self.up(d3), e2), dim=1))
        d1 = self.dec1(torch.cat((self.up(d2), e1), dim=1))
        return self.output(d1)


def count_parameters(model: nn.Module) -> int:
    return sum(parameter.numel() for parameter in model.parameters() if parameter.requires_grad)


def read_manifest(path: Path) -> list[str]:
    if not path.is_file():
        raise FileNotFoundError(f"Missing manifest: {path}")
    names = [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not names:
        raise RuntimeError(f"Empty manifest: {path}")
    if len(names) != len(set(names)):
        raise RuntimeError(f"Duplicate IDs in manifest: {path}")
    return names


class FaultSegDataset(Dataset[tuple[Tensor, Tensor, str]]):
    def __init__(
        self,
        split_root: Path,
        manifest: Path,
        include_fixed_flip: bool,
    ) -> None:
        self.split_root = split_root
        self.names = read_manifest(manifest)
        self.samples: list[tuple[str, bool]] = []
        for name in self.names:
            self.samples.append((name, False))
            if include_fixed_flip:
                self.samples.append((name, True))

        expected_values = math.prod(VOLUME_SHAPE)
        expected_bytes = expected_values * np.dtype(np.float32).itemsize
        for name in self.names:
            for kind in ("seis", "fault"):
                path = self.split_root / kind / name
                if not path.is_file():
                    raise FileNotFoundError(path)
                if path.stat().st_size != expected_bytes:
                    raise RuntimeError(
                        f"Unexpected size for {path}: {path.stat().st_size}; "
                        f"expected {expected_bytes}"
                    )

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, index: int) -> tuple[Tensor, Tensor, str]:
        name, flipped = self.samples[index]
        seismic_path = self.split_root / "seis" / name
        fault_path = self.split_root / "fault" / name

        seismic = np.fromfile(seismic_path, dtype=np.float32).reshape(VOLUME_SHAPE)
        fault = np.fromfile(fault_path, dtype=np.float32).reshape(VOLUME_SHAPE)
        if not np.isfinite(seismic).all() or not np.isfinite(fault).all():
            raise RuntimeError(f"NaN/Inf in pair {name}")
        if not np.isin(np.unique(fault), (0.0, 1.0)).all():
            raise RuntimeError(f"Non-binary label in {fault_path}")

        # Match the public FaultSeg3D loader: standardize each seismic volume
        # independently, then reverse the axis order for seismic conventions.
        mean = float(seismic.mean(dtype=np.float64))
        std = float(seismic.std(dtype=np.float64))
        if not std > 0.0:
            raise RuntimeError(f"Zero standard deviation in {seismic_path}")
        seismic = (seismic - mean) / std
        seismic = np.transpose(seismic)
        fault = np.transpose(fault)
        if flipped:
            seismic = np.flip(seismic, axis=0)
            fault = np.flip(fault, axis=0)

        seismic = np.ascontiguousarray(seismic[None], dtype=np.float32)
        fault = np.ascontiguousarray(fault[None], dtype=np.float32)
        sample_id = f"{Path(name).stem}{'_flip' if flipped else ''}"
        return torch.from_numpy(seismic), torch.from_numpy(fault), sample_id


def soft_dice_loss(logits: Tensor, target: Tensor, smooth: float = 1.0) -> Tensor:
    probability = torch.sigmoid(logits)
    dims = tuple(range(1, probability.ndim))
    intersection = torch.sum(probability * target, dim=dims)
    denominator = torch.sum(probability, dim=dims) + torch.sum(target, dim=dims)
    return 1.0 - ((2.0 * intersection + smooth) / (denominator + smooth)).mean()


class SegmentationLoss(nn.Module):
    def __init__(self, variant: str, pos_weight: float) -> None:
        super().__init__()
        self.variant = variant
        self.register_buffer("positive_weight", torch.tensor([pos_weight], dtype=torch.float32))

    def forward(self, logits: Tensor, target: Tensor) -> Tensor:
        if self.variant == "b0_bce":
            return nn.functional.binary_cross_entropy_with_logits(logits, target)
        if self.variant == "b1_weighted_dice":
            bce = nn.functional.binary_cross_entropy_with_logits(
                logits, target, pos_weight=self.positive_weight
            )
            dice = soft_dice_loss(logits, target)
            return 0.5 * bce + 0.5 * dice
        raise ValueError(f"Unknown loss variant: {self.variant}")


@dataclass
class Metrics:
    threshold: float
    dice: float
    iou: float
    precision: float
    recall: float
    specificity: float
    balanced_accuracy: float
    accuracy: float
    mcc: float
    pr_auc_approx: float
    roc_auc_approx: float
    tp: int
    fp: int
    fn: int
    tn: int


class ProbabilityHistogram:
    """Streaming binary metrics and approximate curve AUCs without retaining voxels."""

    def __init__(self, bins: int = 2048) -> None:
        self.bins = bins
        self.positive = torch.zeros(bins, dtype=torch.float64)
        self.negative = torch.zeros(bins, dtype=torch.float64)

    @torch.no_grad()
    def update_probabilities(self, probability: Tensor, target: Tensor) -> None:
        probability = probability.detach().reshape(-1)
        target = target.detach().reshape(-1)
        indices = torch.clamp((probability * self.bins).long(), 0, self.bins - 1)
        positive = torch.bincount(
            indices, weights=target.to(torch.float32), minlength=self.bins
        )
        negative = torch.bincount(
            indices, weights=(1.0 - target).to(torch.float32), minlength=self.bins
        )
        self.positive += positive.cpu().to(torch.float64)
        self.negative += negative.cpu().to(torch.float64)

    def _descending_counts(self) -> tuple[Tensor, Tensor, Tensor, Tensor]:
        true_positive = torch.flip(self.positive, dims=(0,)).cumsum(0)
        false_positive = torch.flip(self.negative, dims=(0,)).cumsum(0)
        total_positive = self.positive.sum()
        total_negative = self.negative.sum()
        false_negative = total_positive - true_positive
        true_negative = total_negative - false_positive
        return true_positive, false_positive, false_negative, true_negative

    def best_dice_threshold(self) -> float:
        tp, fp, fn, _ = self._descending_counts()
        dice = (2.0 * tp + 1e-12) / (2.0 * tp + fp + fn + 1e-12)
        reverse_index = int(torch.argmax(dice).item())
        original_bin = self.bins - 1 - reverse_index
        return original_bin / self.bins

    def metrics(self, threshold: float) -> Metrics:
        threshold_bin = min(max(int(threshold * self.bins), 0), self.bins - 1)
        tp = self.positive[threshold_bin:].sum()
        fp = self.negative[threshold_bin:].sum()
        fn = self.positive[:threshold_bin].sum()
        tn = self.negative[:threshold_bin].sum()

        dice = (2.0 * tp) / (2.0 * tp + fp + fn + 1e-12)
        iou = tp / (tp + fp + fn + 1e-12)
        precision = tp / (tp + fp + 1e-12)
        recall = tp / (tp + fn + 1e-12)
        specificity = tn / (tn + fp + 1e-12)
        balanced_accuracy = 0.5 * (recall + specificity)
        accuracy = (tp + tn) / (tp + fp + fn + tn + 1e-12)
        mcc_denominator = torch.sqrt(
            (tp + fp) * (tp + fn) * (tn + fp) * (tn + fn)
        )
        mcc = (
            (tp * tn - fp * fn) / mcc_denominator
            if float(mcc_denominator) > 0.0
            else torch.tensor(0.0, dtype=torch.float64)
        )

        curve_tp, curve_fp, _, _ = self._descending_counts()
        curve_precision = curve_tp / (curve_tp + curve_fp + 1e-12)
        curve_recall = curve_tp / (self.positive.sum() + 1e-12)
        recall_increment = torch.diff(
            torch.cat((torch.zeros(1, dtype=torch.float64), curve_recall))
        )
        pr_auc = torch.sum(recall_increment * curve_precision)
        curve_tpr = curve_recall
        curve_fpr = curve_fp / (self.negative.sum() + 1e-12)
        roc_auc = torch.trapz(
            torch.cat((torch.zeros(1, dtype=torch.float64), curve_tpr)),
            torch.cat((torch.zeros(1, dtype=torch.float64), curve_fpr)),
        )

        return Metrics(
            threshold=float(threshold),
            dice=float(dice),
```
