#!/usr/bin/env python3
"""Train the P1 AAM-Attention3D model with connectivity-aware focal Tversky.

This file reuses the verified FaultSeg3D data, metric, checkpoint, and training
pipeline. It replaces only the model and supervised loss. The final mask uses
one joint voxel-edge focal Tversky statistic; two deeper skip connections use
actively supervised attention maps with Smooth L1.
"""

from __future__ import annotations

import math

import torch
import torch.nn.functional as F
from torch import Tensor, nn

import faultseg3d_baseline as baseline


FALSE_POSITIVE_WEIGHT = 0.3
FALSE_NEGATIVE_WEIGHT = 0.7
FOCAL_POWER = 4.0 / 3.0
ATTENTION_WEIGHT = 1.0
ATTENTION_SIGMA = 1.5
EXPECTED_PARAMETERS = 1_467_411
DEFAULT_BASELINE_RUN_DIR = "runs/faultseg3d_b0_seed42"
DEFAULT_P1_RUN_DIR = "runs/p1_attention3d_caft_seed42"


class ActiveAttentionModule(nn.Module):
    """Gate one encoder skip using a coarser decoder feature map."""

    def __init__(self, low_channels: int, high_channels: int) -> None:
        super().__init__()
        hidden_channels = max(low_channels // 2, 1)
        self.low_projection = nn.Conv3d(low_channels, hidden_channels, kernel_size=1)
        self.high_projection = nn.Conv3d(high_channels, hidden_channels, kernel_size=1)
        self.score = nn.Conv3d(hidden_channels, 1, kernel_size=1)

    def forward(self, low: Tensor, high: Tensor) -> tuple[Tensor, Tensor]:
        high = F.interpolate(
            high, size=low.shape[2:], mode="trilinear", align_corners=False
        )
        fused = F.relu(
            self.low_projection(low) + self.high_projection(high), inplace=False
        )
        attention = torch.sigmoid(self.score(fused))
        return low * attention, attention


_ACTIVE_MODEL = None
_ACTIVE_LOSS = None


class Attention3D(baseline.FaultSeg3D):
    """FaultSeg3D backbone with active attention on its two deeper skips."""

    def __init__(self) -> None:
        super().__init__()
        global _ACTIVE_MODEL
        self.att3 = ActiveAttentionModule(64, 128)
        self.att2 = ActiveAttentionModule(32, 64)
        self._training_attention_maps: tuple[Tensor, ...] | None = None
        _ACTIVE_MODEL = self

    def forward(self, x: Tensor) -> Tensor:
        e1 = self.enc1(x)
        e2 = self.enc2(self.pool(e1))
        e3 = self.enc3(self.pool(e2))
        bottleneck = self.bottleneck(self.pool(e3))

        gated_e3, attention3 = self.att3(e3, bottleneck)
        d3 = self.dec3(torch.cat((self.up(bottleneck), gated_e3), dim=1))
        gated_e2, attention2 = self.att2(e2, d3)
        d2 = self.dec2(torch.cat((self.up(d3), gated_e2), dim=1))
        d1 = self.dec1(torch.cat((self.up(d2), e1), dim=1))

        if self.training:
            self._training_attention_maps = (attention3, attention2)
        else:
            self._training_attention_maps = None
        return self.output(d1)

    def pop_training_attention_maps(self) -> tuple[Tensor, ...]:
        maps = self._training_attention_maps
        self._training_attention_maps = None
        if maps is None:
            raise RuntimeError("Attention maps are unavailable for the training loss")
        return maps


class P1SegmentationLoss(nn.Module):
    """One joint node-edge focal Tversky plus original AAM supervision."""

    def __init__(self, _variant: str, _unused_pos_weight: float | None) -> None:
        super().__init__()
        global _ACTIVE_LOSS
        radius = max(1, math.ceil(3.0 * ATTENTION_SIGMA))
        coordinates = torch.arange(-radius, radius + 1, dtype=torch.float32)
        kernel = torch.exp(
            -(coordinates.square()) / (2.0 * ATTENTION_SIGMA**2)
        )
        self.register_buffer("gaussian_kernel", kernel / kernel.sum())
        self._reported_components = False
        self._epoch_caft = 0.0
        self._epoch_attention = 0.0
        self._epoch_batches = 0
        _ACTIVE_LOSS = self

    @staticmethod
    def _sum_per_sample(values: Tensor) -> Tensor:
        return values.sum(dim=tuple(range(1, values.ndim)))

    def _connectivity_counts(
        self, probability: Tensor, target: Tensor
    ) -> tuple[Tensor, Tensor, Tensor]:
        node_tp = self._sum_per_sample(probability * target)
        node_fp = self._sum_per_sample(probability * (1.0 - target))
        node_fn = self._sum_per_sample((1.0 - probability) * target)
        edge_tp = torch.zeros_like(node_tp)
        edge_fp = torch.zeros_like(node_tp)
        edge_fn = torch.zeros_like(node_tp)
        edge_candidates = 0

        # Three positive-axis pairs represent each undirected 6-neighbour edge once.
        for axis in (2, 3, 4):
            first = [slice(None)] * probability.ndim
            second = [slice(None)] * probability.ndim
            first[axis] = slice(0, -1)
            second[axis] = slice(1, None)
            predicted_edge = probability[tuple(first)] * probability[tuple(second)]
            target_edge = target[tuple(first)] * target[tuple(second)]
            edge_tp = edge_tp + self._sum_per_sample(predicted_edge * target_edge)
            edge_fp = edge_fp + self._sum_per_sample(
                predicted_edge * (1.0 - target_edge)
            )
            edge_fn = edge_fn + self._sum_per_sample(
                (1.0 - predicted_edge) * target_edge
            )
            edge_candidates += predicted_edge[0].numel()

        # Fixed count normalization prevents the three edge sets dominating nodes.
        edge_scale = probability[0].numel() / edge_candidates
        return (
            node_tp + edge_scale * edge_tp,
            node_fp + edge_scale * edge_fp,
            node_fn + edge_scale * edge_fn,
        )

    def _attention_target(self, target: Tensor, output_size: tuple[int, ...]) -> Tensor:
        reduced = F.adaptive_max_pool3d(target.float(), output_size)
        kernel = self.gaussian_kernel
        radius = kernel.numel() // 2
        blurred = F.conv3d(
            reduced,
            kernel.view(1, 1, -1, 1, 1),
            padding=(radius, 0, 0),
        )
        blurred = F.conv3d(
            blurred,
            kernel.view(1, 1, 1, -1, 1),
            padding=(0, radius, 0),
        )
        blurred = F.conv3d(
            blurred,
            kernel.view(1, 1, 1, 1, -1),
            padding=(0, 0, radius),
        )
        return torch.maximum(reduced, blurred.clamp_(0.0, 1.0))

    def forward(self, logits: Tensor, target: Tensor) -> Tensor:
        global _ACTIVE_MODEL
        if _ACTIVE_MODEL is None:
            raise RuntimeError("P1 model was not initialized")
        attention_maps = _ACTIVE_MODEL.pop_training_attention_maps()
        probability = torch.sigmoid(logits.float())
        target = target.float()
        true_positive, false_positive, false_negative = self._connectivity_counts(
            probability, target
        )
        tversky = (true_positive + 1e-6) / (
            true_positive
            + FALSE_POSITIVE_WEIGHT * false_positive
            + FALSE_NEGATIVE_WEIGHT * false_negative
            + 1e-6
        )
        caft = (1.0 - tversky).clamp_min(0.0).pow(FOCAL_POWER).mean()

        attention_losses = []
        for attention in attention_maps:
            expected = self._attention_target(target, attention.shape[2:])
            attention_losses.append(
                F.smooth_l1_loss(attention.float(), expected, reduction="mean")
            )
        attention_loss = torch.stack(attention_losses).mean()
        total = caft + ATTENTION_WEIGHT * attention_loss
        self._epoch_caft = self._epoch_caft + caft.detach()
        self._epoch_attention = self._epoch_attention + attention_loss.detach()
        self._epoch_batches += 1
        if not self._reported_components:
            print(
                "first_loss_components="
                f"caft:{caft.detach().item():.6f},"
                f"attention:{attention_loss.detach().item():.6f},"
                f"total:{total.detach().item():.6f}",
                flush=True,
            )
            self._reported_components = True
        return total

    def pop_epoch_components(self) -> dict[str, float]:
        count = max(self._epoch_batches, 1)
        result = {
            "train_caft_loss": float(self._epoch_caft / count),
            "train_attention_loss": float(self._epoch_attention / count),
        }
        self._epoch_caft = 0.0
        self._epoch_attention = 0.0
        self._epoch_batches = 0
        return result


_BASELINE_WRITE_HISTORY = baseline.write_history


def write_history_with_p1_components(path, rows) -> None:
    if _ACTIVE_LOSS is None:
        raise RuntimeError("P1 loss was not initialized")
    components = _ACTIVE_LOSS.pop_epoch_components()
    rows[-1].update(components)
    _BASELINE_WRITE_HISTORY(path, rows)


def configure_baseline_pipeline() -> None:
    baseline.FaultSeg3D = Attention3D
    baseline.SegmentationLoss = P1SegmentationLoss
    baseline.EXPECTED_PARAMETERS = EXPECTED_PARAMETERS
    baseline.write_history = write_history_with_p1_components
    baseline.__doc__ = __doc__


def main() -> None:
    configure_baseline_pipeline()
    parser = baseline.build_parser()
    args = parser.parse_args()
    if args.run_dir == DEFAULT_BASELINE_RUN_DIR:
        args.run_dir = DEFAULT_P1_RUN_DIR
    args.loss = "p1_connectivity_aware_focal_tversky_plus_aam_smooth_l1"
    args.pos_weight = None
    args.false_positive_weight = FALSE_POSITIVE_WEIGHT
    args.false_negative_weight = FALSE_NEGATIVE_WEIGHT
    args.focal_power = FOCAL_POWER
    args.connectivity = "6-neighbour-undirected"
    args.edge_normalization = "voxel_count/edge_count"
    args.attention_weight = ATTENTION_WEIGHT
    args.attention_sigma = ATTENTION_SIGMA
    baseline.train(args)


if __name__ == "__main__":
    main()
