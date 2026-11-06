#!/usr/bin/env python3
"""Modern PyTorch ports of the Thebe dataset authors' 2D baselines.

Sources (GPL-3.0):
https://github.com/anyuzoey/CNNforFaultInterpretation/tree/master/model_zoo

The layer graphs, dropout placement, side outputs, and bilinear transposed
convolutions follow the released UNET.py, HED.py, and RCF.py.  The only
intentional numerical change is returning logits and using BCE-with-logits in
the trainer instead of applying sigmoid before BCE.
"""

from __future__ import annotations

import torch
from torch import nn
from torch.nn import functional as F


PATCH_SIZE = 96


def center_crop(value: torch.Tensor, height: int, width: int) -> torch.Tensor:
    source_h, source_w = value.shape[-2:]
    x0 = int(round((source_w - width) / 2.0))
    y0 = int(round((source_h - height) / 2.0))
    return value[:, :, y0 : y0 + height, x0 : x0 + width]


def bilinear_kernel(size: int) -> torch.Tensor:
    factor = (size + 1) // 2
    center = factor - 1 if size % 2 else factor - 0.5
    axis = torch.arange(size, dtype=torch.float32)
    one_d = 1.0 - torch.abs(axis - center) / factor
    return (one_d[:, None] * one_d[None, :])[None, None]


class DoubleConv(nn.Module):
    def __init__(self, in_channels: int, out_channels: int, padding: int) -> None:
        super().__init__()
        self.layers = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, 3, padding=padding),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.Dropout2d(0.25),
            nn.Conv2d(out_channels, out_channels, 3, padding=padding),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.Dropout2d(0.25),
        )

    def forward(self, value: torch.Tensor) -> torch.Tensor:
        return self.layers(value)


class ThebeAuthorUNet(nn.Module):
    """Port of model_zoo/UNET.py from the official Thebe repository."""

    def __init__(self) -> None:
        super().__init__()
        width = 32
        self.down1 = DoubleConv(1, width, padding=1)
        self.down2 = DoubleConv(width, width * 2, padding=1)
        self.down3 = DoubleConv(width * 2, width * 4, padding=1)
        self.bottom = DoubleConv(width * 4, width * 8, padding=2)
        self.pool = nn.MaxPool2d(2)
        self.up3 = nn.ConvTranspose2d(width * 8, width * 4, 2, 2)
        self.decode3 = DoubleConv(width * 8, width * 4, padding=2)
        self.up2 = nn.ConvTranspose2d(width * 4, width * 2, 2, 2)
        self.decode2 = DoubleConv(width * 4, width * 2, padding=2)
        self.up1 = nn.ConvTranspose2d(width * 2, width, 2, 2)
        self.decode1 = DoubleConv(width * 2, width, padding=2)
        self.head = nn.Conv2d(width, 1, 1)
        self.spec = {
            "family": "Thebe-author 2D UNet",
            "implementation": "modern port of model_zoo/UNET.py",
            "source": "https://github.com/anyuzoey/CNNforFaultInterpretation/blob/master/model_zoo/UNET.py",
            "license": "GPL-3.0",
            "claim_scope": "author-code port; logits replace sigmoid-plus-BCE",
        }

    def forward(self, value: torch.Tensor) -> torch.Tensor:
        output_size = value.shape[-2:]
        d1 = self.down1(value)
        d2 = self.down2(self.pool(d1))
        d3 = self.down3(self.pool(d2))
        bottom = self.bottom(self.pool(d3))
        u3 = center_crop(self.up3(bottom), *d3.shape[-2:])
        u3 = self.decode3(torch.cat((d3, u3), dim=1))
        u2 = center_crop(self.up2(u3), *d2.shape[-2:])
        u2 = self.decode2(torch.cat((d2, u2), dim=1))
        u1 = center_crop(self.up1(u2), *d1.shape[-2:])
        u1 = self.decode1(torch.cat((d1, u1), dim=1))
        return center_crop(self.head(u1), *output_size)


class EdgeSideNetwork(nn.Module):
    """Shared released HED/RCF encoder and side-output geometry."""

    def __init__(self, richer: bool) -> None:
        super().__init__()
        self.richer = richer
        self.conv1_1 = nn.Conv2d(1, 32, 3, padding=1)
        self.conv1_2 = nn.Conv2d(32, 32, 3, padding=1)
        self.conv2_1 = nn.Conv2d(32, 64, 3, padding=1)
        self.conv2_2 = nn.Conv2d(64, 64, 3, padding=1)
        self.conv3_1 = nn.Conv2d(64, 128, 3, padding=1)
        self.conv3_2 = nn.Conv2d(128, 128, 3, padding=1)
        self.conv3_3 = nn.Conv2d(128, 128, 3, padding=1)
        self.conv4_1 = nn.Conv2d(128, 256, 3, padding=1)
        self.conv4_2 = nn.Conv2d(256, 256, 3, padding=1)
        self.conv4_3 = nn.Conv2d(256, 256, 3, padding=1)
        self.conv5_1 = nn.Conv2d(256, 256, 3, padding=2, dilation=2)
        self.conv5_2 = nn.Conv2d(256, 256, 3, padding=2, dilation=2)
        self.conv5_3 = nn.Conv2d(256, 256, 3, padding=2, dilation=2)
        self.pool = nn.MaxPool2d(2, stride=2, ceil_mode=True)
        self.pool4 = nn.MaxPool2d(2, stride=1, ceil_mode=True)
        self.relu = nn.ReLU()
        dropout = nn.Dropout2d if richer else nn.Dropout
        self.dropout = dropout(0.2)
        stage_channels = ((32, 32), (64, 64), (128, 128, 128),
                          (256, 256, 256), (256, 256, 256))
        if richer:
            self.down = nn.ModuleList(
                [nn.ModuleList([nn.Conv2d(ch, 21, 1) for ch in stage])
                 for stage in stage_channels]
            )
        else:
            self.down = nn.ModuleList(
                [nn.ModuleList([nn.Conv2d(stage[-1], 21, 1)])
                 for stage in stage_channels]
            )
        self.side = nn.ModuleList([nn.Conv2d(21, 1, 1) for _ in range(5)])
        self.fuse = nn.Conv2d(5, 1, 1)
        self.register_buffer("up2", bilinear_kernel(4), persistent=True)
        self.register_buffer("up3", bilinear_kernel(8), persistent=True)
        self.register_buffer("up4", bilinear_kernel(16), persistent=True)
        self.register_buffer("up5", bilinear_kernel(32), persistent=True)

    def activated(self, layer: nn.Module, value: torch.Tensor) -> torch.Tensor:
        return self.dropout(self.relu(layer(value)))

    def forward(self, value: torch.Tensor) -> list[torch.Tensor]:
        height, width = value.shape[-2:]
        c11 = self.activated(self.conv1_1, value)
        c12 = self.activated(self.conv1_2, c11)
        c21 = self.activated(self.conv2_1, self.pool(c12))
        c22 = self.activated(self.conv2_2, c21)
        c31 = self.activated(self.conv3_1, self.pool(c22))
        c32 = self.activated(self.conv3_2, c31)
        c33 = self.activated(self.conv3_3, c32)
        c41 = self.activated(self.conv4_1, self.pool(c33))
        c42 = self.activated(self.conv4_2, c41)
        c43 = self.activated(self.conv4_3, c42)
        c51 = self.activated(self.conv5_1, self.pool4(c43))
        c52 = self.activated(self.conv5_2, c51)
        c53 = self.activated(self.conv5_3, c52)
        stages = ((c11, c12), (c21, c22), (c31, c32, c33),
                  (c41, c42, c43), (c51, c52, c53))
        side_logits = []
        for stage_index, stage in enumerate(stages):
            selected = stage if self.richer else (stage[-1],)
            reduced = sum(
                layer(feature)
                for layer, feature in zip(self.down[stage_index], selected, strict=True)
            )
            side_logits.append(self.side[stage_index](reduced))
        expanded = [
            side_logits[0],
            F.conv_transpose2d(side_logits[1], self.up2, stride=2),
            F.conv_transpose2d(side_logits[2], self.up3, stride=4),
            F.conv_transpose2d(side_logits[3], self.up4, stride=8),
            F.conv_transpose2d(side_logits[4], self.up5, stride=8),
        ]
        cropped = [center_crop(item, height, width) for item in expanded]
        return [*cropped, self.fuse(torch.cat(cropped, dim=1))]


class ThebeAuthorHED(EdgeSideNetwork):
    def __init__(self) -> None:
        super().__init__(richer=False)
        self.spec = {
            "family": "Thebe-author HED",
            "implementation": "modern port of model_zoo/HED.py",
            "source": "https://github.com/anyuzoey/CNNforFaultInterpretation/blob/master/model_zoo/HED.py",
            "license": "GPL-3.0",
            "claim_scope": "author-code port; logits replace sigmoid-plus-BCE",
        }


class ThebeAuthorRCF(EdgeSideNetwork):
    def __init__(self) -> None:
        super().__init__(richer=True)
        self.spec = {
            "family": "Thebe-author RCF",
            "implementation": "modern port of model_zoo/RCF.py",
            "source": "https://github.com/anyuzoey/CNNforFaultInterpretation/blob/master/model_zoo/RCF.py",
            "license": "GPL-3.0",
            "claim_scope": "author-code port; logits replace sigmoid-plus-BCE",
        }


def fixed_padding(value: torch.Tensor, kernel_size: int, dilation: int) -> torch.Tensor:
    effective = kernel_size + (kernel_size - 1) * (dilation - 1)
    total = effective - 1
    begin = total // 2
    return F.pad(value, (begin, total - begin, begin, total - begin))


class InvertedResidual(nn.Module):
    def __init__(
        self, in_channels: int, out_channels: int, stride: int,
        dilation: int, expansion: int
    ) -> None:
        super().__init__()
        hidden = round(in_channels * expansion)
        self.use_residual = stride == 1 and in_channels == out_channels
        self.dilation = dilation
        layers: list[nn.Module] = []
        if expansion != 1:
            layers.extend((
                nn.Conv2d(in_channels, hidden, 1, bias=False),
                nn.BatchNorm2d(hidden),
                nn.ReLU6(inplace=True),
            ))
        layers.extend((
            nn.Conv2d(
                hidden, hidden, 3, stride=stride, padding=0,
                dilation=dilation, groups=hidden, bias=False
            ),
            nn.BatchNorm2d(hidden),
            nn.ReLU6(inplace=True),
            nn.Conv2d(hidden, out_channels, 1, bias=False),
            nn.BatchNorm2d(out_channels),
        ))
        self.layers = nn.Sequential(*layers)

    def forward(self, value: torch.Tensor) -> torch.Tensor:
        output = self.layers(fixed_padding(value, 3, self.dilation))
        return value + output if self.use_residual else output


class ThebeMobileNetV2(nn.Module):
    def __init__(self, output_stride: int = 16) -> None:
        super().__init__()
        features: list[nn.Module] = [nn.Sequential(
            nn.Conv2d(1, 32, 3, stride=2, padding=1, bias=False),
            nn.BatchNorm2d(32),
            nn.ReLU6(inplace=True),
        )]
        current_stride = 2
        dilation_rate = 1
        in_channels = 32
        settings = ((1, 16, 1, 1), (6, 24, 2, 2), (6, 32, 3, 2),
                    (6, 64, 4, 2), (6, 96, 3, 1), (6, 160, 3, 2),
                    (6, 320, 1, 1))
        for expansion, out_channels, repeats, nominal_stride in settings:
            if current_stride == output_stride:
                first_stride = 1
                dilation = dilation_rate
                dilation_rate *= nominal_stride
            else:
                first_stride = nominal_stride
                dilation = 1
                current_stride *= nominal_stride
            for repeat in range(repeats):
                stride = first_stride if repeat == 0 else 1
                features.append(InvertedResidual(
                    in_channels, out_channels, stride, dilation, expansion
                ))
                in_channels = out_channels
        self.low = nn.Sequential(*features[:4])
        self.high = nn.Sequential(*features[4:])

    def forward(self, value: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        low = self.low(value)
        return self.high(low), low


class ASPPBranch(nn.Sequential):
    def __init__(self, kernel_size: int, padding: int, dilation: int) -> None:
        super().__init__(
            nn.Conv2d(
                320, 256, kernel_size, padding=padding,
                dilation=dilation, bias=False
            ),
            nn.BatchNorm2d(256),
            nn.ReLU(),
        )


class ThebeASPP(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.branches = nn.ModuleList((
            ASPPBranch(1, 0, 1),
            ASPPBranch(3, 6, 6),
            ASPPBranch(3, 12, 12),
            ASPPBranch(3, 18, 18),
        ))
        self.global_pool = nn.Sequential(
            nn.AdaptiveAvgPool2d(1),
            nn.Conv2d(320, 256, 1, bias=False),
            nn.BatchNorm2d(256),
            nn.ReLU(),
        )
        self.project = nn.Sequential(
            nn.Conv2d(1280, 256, 1, bias=False),
            nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.Dropout(0.5),
        )

    def forward(self, value: torch.Tensor) -> torch.Tensor:
        outputs = [branch(value) for branch in self.branches]
        pooled = self.global_pool(value)
        outputs.append(F.interpolate(
            pooled, size=value.shape[-2:], mode="bilinear", align_corners=True
        ))
        return self.project(torch.cat(outputs, dim=1))


class ThebeDeepLabDecoder(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.low = nn.Sequential(
            nn.Conv2d(24, 48, 1, bias=False),
            nn.BatchNorm2d(48),
            nn.ReLU(),
        )
        self.output = nn.Sequential(
            nn.Conv2d(304, 256, 3, padding=1, bias=False),
            nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Conv2d(256, 256, 3, padding=1, bias=False),
            nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Conv2d(256, 1, 1),
        )

    def forward(self, value: torch.Tensor, low: torch.Tensor) -> torch.Tensor:
        low = self.low(low)
        value = F.interpolate(
            value, size=low.shape[-2:], mode="bilinear", align_corners=True
        )
        return self.output(torch.cat((value, low), dim=1))


class ThebeAuthorDeepLabM(nn.Module):
    """Port of the released Thebe MobileNetV2 DeepLabV3+ baseline."""

    def __init__(self) -> None:
        super().__init__()
        self.backbone = ThebeMobileNetV2(output_stride=16)
        self.aspp = ThebeASPP()
        self.decoder = ThebeDeepLabDecoder()
        for module in self.modules():
            if isinstance(module, nn.Conv2d):
                nn.init.kaiming_normal_(module.weight)
            elif isinstance(module, nn.BatchNorm2d):
                nn.init.ones_(module.weight)
                nn.init.zeros_(module.bias)
        self.spec = {
            "family": "Thebe-author MobileNet DeepLab (DeeplabM)",
            "implementation": "modern port of model_zoo/DEEPLAB",
            "source": "https://github.com/anyuzoey/CNNforFaultInterpretation/tree/master/model_zoo/DEEPLAB",
            "license": "GPL-3.0",
            "initialization": "random, matching released backbone default",
            "claim_scope": "author-code port; logits replace sigmoid-plus-BCE",
        }

    def forward(self, value: torch.Tensor) -> torch.Tensor:
        output_size = value.shape[-2:]
        value, low = self.backbone(value)
        value = self.aspp(value)
        value = self.decoder(value, low)
        return F.interpolate(
            value, size=output_size, mode="bilinear", align_corners=True
        )


MODELS = {
    "unet": ThebeAuthorUNet,
    "hed": ThebeAuthorHED,
    "rcf": ThebeAuthorRCF,
    "deeplabm": ThebeAuthorDeepLabM,
}


def create_model(name: str) -> nn.Module:
    return MODELS[name]()


def fused_logits(output: torch.Tensor | list[torch.Tensor]) -> torch.Tensor:
    return output[-1] if isinstance(output, list) else output


def balanced_side_loss(
    logits: torch.Tensor, target: torch.Tensor, negative_factor: float
) -> torch.Tensor:
    positive = (target == 1).sum(dtype=torch.float32)
    negative = (target == 0).sum(dtype=torch.float32)
    total = positive + negative
    weights = torch.where(
        target == 1,
        negative / total,
        negative_factor * positive / total,
    )
    return F.binary_cross_entropy_with_logits(
        logits.float(), target.float(), weight=weights, reduction="sum"
    )


def author_loss(
    name: str, output: torch.Tensor | list[torch.Tensor], target: torch.Tensor
) -> torch.Tensor:
    if name in {"unet", "deeplabm"}:
        return F.binary_cross_entropy_with_logits(output.float(), target.float())
    if not isinstance(output, list) or len(output) != 6:
        raise ValueError(f"{name} must return five side logits and one fused logit")
    if name == "hed":
        side = sum(balanced_side_loss(item, target, 1.0) for item in output[:5])
        return side + F.binary_cross_entropy_with_logits(
            output[-1].float(), target.float()
        )
    if name == "rcf":
        return sum(balanced_side_loss(item, target, 1.1) for item in output)
    raise ValueError(name)
