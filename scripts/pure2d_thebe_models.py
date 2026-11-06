#!/usr/bin/env python3
"""Pure single-task 2D model families for the Thebe fault benchmark.

Backbones come from the official torchvision implementations. The ViT and Swin
segmentation decoders are local, paper-aligned dense-prediction heads because
the Seismic Fault SAM comparison did not release its reimplementation code.
"""

from __future__ import annotations

import torch
from torch import nn
from torch.nn import functional as F
from torchvision.models import swin_t, vit_b_16
from torchvision.models.segmentation import deeplabv3_resnet50


IMAGE_SIZE = 256


class DeepLabV3Pure(nn.Module):
    """Official torchvision DeepLabV3-ResNet50, random initialization."""

    def __init__(self) -> None:
        super().__init__()
        self.network = deeplabv3_resnet50(
            weights=None,
            weights_backbone=None,
            num_classes=1,
            aux_loss=False,
        )
        self.spec = {
            "family": "DeepLabV3",
            "implementation": "torchvision.models.segmentation.deeplabv3_resnet50",
            "source": "https://docs.pytorch.org/vision/stable/models/deeplabv3.html",
            "backbone": "ResNet-50",
            "initialization": "random",
            "input_channels": "one seismic channel repeated to the expected three channels",
            "claim_scope": "official architecture; local Thebe training protocol",
        }

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.network(x.repeat(1, 3, 1, 1))["out"]


class ViTSETRPure(nn.Module):
    """Official ViT-B/16 encoder with a SETR-style progressive decoder."""

    def __init__(self) -> None:
        super().__init__()
        self.encoder = vit_b_16(weights=None, image_size=IMAGE_SIZE)
        self.encoder.heads = nn.Identity()
        self.decoder = nn.Sequential(
            nn.ConvTranspose2d(768, 256, kernel_size=2, stride=2),
            nn.GroupNorm(16, 256),
            nn.GELU(),
            nn.ConvTranspose2d(256, 128, kernel_size=2, stride=2),
            nn.GroupNorm(8, 128),
            nn.GELU(),
            nn.ConvTranspose2d(128, 64, kernel_size=2, stride=2),
            nn.GroupNorm(8, 64),
            nn.GELU(),
            nn.ConvTranspose2d(64, 1, kernel_size=2, stride=2),
        )
        self.spec = {
            "family": "2D ViT segmentation",
            "encoder": "torchvision ViT-B/16, official Google ViT architecture",
            "encoder_source": "https://github.com/google-research/vision_transformer",
            "decoder": "local progressive upsampling head aligned with SETR-PUP",
            "decoder_source": "https://github.com/LogosIntelligenceLab/SETR",
            "initialization": "random",
            "claim_scope": (
                "official ViT backbone plus paper-aligned local decoder; not the "
                "unreleased ViT reimplementation from Seismic Fault SAM"
            ),
        }

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = x.repeat(1, 3, 1, 1)
        tokens = self.encoder._process_input(x)
        batch = tokens.shape[0]
        cls = self.encoder.class_token.expand(batch, -1, -1)
        tokens = self.encoder.encoder(torch.cat((cls, tokens), dim=1))[:, 1:]
        side = IMAGE_SIZE // 16
        features = tokens.transpose(1, 2).reshape(batch, 768, side, side)
        return self.decoder(features)


class SwinFPNPure(nn.Module):
    """Official Swin-T encoder with a local UPerNet/FPN-style decoder."""

    def __init__(self) -> None:
        super().__init__()
        backbone = swin_t(weights=None)
        self.features = backbone.features
        channels = (96, 192, 384, 768)
        self.lateral = nn.ModuleList([nn.Conv2d(value, 128, 1) for value in channels])
        self.smooth = nn.ModuleList(
            [nn.Conv2d(128, 128, 3, padding=1) for _ in range(3)]
        )
        self.head = nn.Sequential(
            nn.Conv2d(128 * 4, 128, 3, padding=1),
            nn.GroupNorm(8, 128),
            nn.GELU(),
            nn.Conv2d(128, 1, 1),
        )
        self.spec = {
            "family": "2D Swin Transformer segmentation",
            "encoder": "torchvision Swin-T, official Microsoft Swin architecture",
            "encoder_source": "https://github.com/microsoft/Swin-Transformer",
            "decoder": "local four-scale FPN/UPerNet-style decoder",
            "reference_decoder": (
                "https://github.com/SwinTransformer/Swin-Transformer-Semantic-Segmentation"
            ),
            "initialization": "random",
            "claim_scope": (
                "official Swin-T backbone plus local FPN decoder; not the unreleased "
                "Swin reimplementation from Seismic Fault SAM"
            ),
        }

    @staticmethod
    def nchw(value: torch.Tensor) -> torch.Tensor:
        return value.permute(0, 3, 1, 2).contiguous()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        output_size = x.shape[-2:]
        x = x.repeat(1, 3, 1, 1)
        x = self.features[0](x)
        x = self.features[1](x)
        f1 = self.nchw(x)
        x = self.features[2](x)
        x = self.features[3](x)
        f2 = self.nchw(x)
        x = self.features[4](x)
        x = self.features[5](x)
        f3 = self.nchw(x)
        x = self.features[6](x)
        x = self.features[7](x)
        f4 = self.nchw(x)

        p4 = self.lateral[3](f4)
        p3 = self.lateral[2](f3) + F.interpolate(
            p4, size=f3.shape[-2:], mode="bilinear", align_corners=False
        )
        p3 = self.smooth[2](p3)
        p2 = self.lateral[1](f2) + F.interpolate(
            p3, size=f2.shape[-2:], mode="bilinear", align_corners=False
        )
        p2 = self.smooth[1](p2)
        p1 = self.lateral[0](f1) + F.interpolate(
            p2, size=f1.shape[-2:], mode="bilinear", align_corners=False
        )
        p1 = self.smooth[0](p1)
        pyramid = torch.cat(
            [
                p1,
                F.interpolate(p2, size=p1.shape[-2:], mode="bilinear", align_corners=False),
                F.interpolate(p3, size=p1.shape[-2:], mode="bilinear", align_corners=False),
                F.interpolate(p4, size=p1.shape[-2:], mode="bilinear", align_corners=False),
            ],
            dim=1,
        )
        logits = self.head(pyramid)
        return F.interpolate(logits, size=output_size, mode="bilinear", align_corners=False)


MODELS = {
    "deeplabv3": DeepLabV3Pure,
    "vit_setr": ViTSETRPure,
    "swin_fpn": SwinFPNPure,
}


def create_model(name: str) -> nn.Module:
    try:
        return MODELS[name]()
    except KeyError as error:
        raise ValueError(f"Unknown model {name!r}; choices: {sorted(MODELS)}") from error


def count_parameters(model: nn.Module) -> int:
    return sum(parameter.numel() for parameter in model.parameters() if parameter.requires_grad)
