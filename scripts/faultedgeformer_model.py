#!/usr/bin/env python3
"""FaultEdgeFormer-inspired 3D segmentation model.

The published FaultEdgeFormer paper specifies the defining operations but does
not provide author code. This implementation preserves those operations:

* nine trainable 3D Sobel directions in the first layer;
* 3x3x3 convolutional Q/K/V projection inside local attention windows;
* alternating regular and shifted 3D windows;
* a depthwise 3x3x3 convolution between the MLP linear layers; and
* parallel high-to-low resolution streams with repeated cross-scale fusion.

Inferred choices (channel widths, normalization around the stem/fusion layers,
and exact Sobel coefficient construction) are explicit in ``model_spec`` and
must not be described as an exact reproduction of the unavailable source.
"""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass

import torch
from torch import Tensor, nn
from torch.nn import functional as F
from torch.utils.checkpoint import checkpoint


@dataclass(frozen=True)
class FaultEdgeFormerSpec:
    input_channels: int = 1
    output_channels: int = 1
    channels: tuple[int, int, int] = (16, 32, 56)
    heads: tuple[int, int, int] = (1, 2, 4)
    window_size: int = 7
    mlp_ratio: int = 4
    sobel_repeats: int = 2
    transformer_pairs_per_resolution: tuple[int, int, int] = (3, 2, 1)
    qkv_projection: str = "3x3x3 convolution within each local window"
    mlp_locality: str = "depthwise 3x3x3 convolution"
    multiscale_fusion: str = "strided 3x3x3 down; trilinear up plus 1x1x1"
    activation: str = "GELU"
    output: str = "logits"
    fidelity: str = (
        "paper-inspired implementation; author code unavailable and exact "
        "figure-only channel/norm details were inferred"
    )


def model_spec(**overrides) -> dict:
    return asdict(FaultEdgeFormerSpec(**overrides))


def _outer3(a: Tensor, b: Tensor, c: Tensor) -> Tensor:
    return torch.einsum("i,j,k->ijk", a, b, c)


def multidirectional_sobel_kernels() -> Tensor:
    """Return three orthogonal and six diagonal zero-sum 3D kernels."""
    smooth = torch.tensor([1.0, 2.0, 1.0])
    derivative = torch.tensor([-1.0, 0.0, 1.0])
    gx = _outer3(derivative, smooth, smooth)
    gy = _outer3(smooth, derivative, smooth)
    gz = _outer3(smooth, smooth, derivative)
    root2 = math.sqrt(2.0)
    kernels = [
        gx,
        gy,
        gz,
        (gx + gy) / root2,
        (gx - gy) / root2,
        (gx + gz) / root2,
        (gx - gz) / root2,
        (gy + gz) / root2,
        (gy - gz) / root2,
    ]
    result = torch.stack(kernels, dim=0)
    # Equalize initial response scales across orthogonal and diagonal filters.
    # This normalization is an explicit numerical-stability inference because
    # the article does not publish its exact integer coefficient scaling.
    result = result / result.abs().sum(dim=(1, 2, 3), keepdim=True).clamp_min(1.0)
    if not torch.allclose(result.sum(dim=(1, 2, 3)), torch.zeros(9), atol=1e-7):
        raise RuntimeError("Sobel kernels must have zero DC response")
    return result[:, None]


class TrainableSobel3D(nn.Module):
    def __init__(self, repeats: int = 2) -> None:
        super().__init__()
        if repeats <= 0:
            raise ValueError("repeats must be positive")
        kernels = multidirectional_sobel_kernels().repeat_interleave(repeats, dim=0)
        self.register_buffer("base_kernels", kernels)
        self.gamma = nn.Parameter(torch.ones(kernels.shape[0]))

    @property
    def out_channels(self) -> int:
        return int(self.base_kernels.shape[0])

    def forward(self, x: Tensor) -> Tensor:
        weight = self.base_kernels * self.gamma[:, None, None, None, None]
        return F.conv3d(x, weight, padding=1)


def _pad_channels_last(x: Tensor, window_size: int) -> tuple[Tensor, tuple[int, int, int]]:
    _, depth, height, width, _ = x.shape
    pd = (-depth) % window_size
    ph = (-height) % window_size
    pw = (-width) % window_size
    if pd or ph or pw:
        x = F.pad(x.permute(0, 4, 1, 2, 3), (0, pw, 0, ph, 0, pd))
        x = x.permute(0, 2, 3, 4, 1).contiguous()
    return x, (pd, ph, pw)


def window_partition(x: Tensor, window_size: int) -> Tensor:
    batch, depth, height, width, channels = x.shape
    if depth % window_size or height % window_size or width % window_size:
        raise ValueError("padded spatial dimensions must divide by window_size")
    x = x.view(
        batch,
        depth // window_size,
        window_size,
        height // window_size,
        window_size,
        width // window_size,
        window_size,
        channels,
    )
    return (
        x.permute(0, 1, 3, 5, 2, 4, 6, 7)
        .contiguous()
        .view(-1, window_size, window_size, window_size, channels)
    )


def window_reverse(
    windows: Tensor,
    window_size: int,
    batch: int,
    depth: int,
    height: int,
    width: int,
) -> Tensor:
    channels = windows.shape[-1]
    x = windows.view(
        batch,
        depth // window_size,
        height // window_size,
        width // window_size,
        window_size,
        window_size,
        window_size,
        channels,
    )
    return (
        x.permute(0, 1, 4, 2, 5, 3, 6, 7)
        .contiguous()
        .view(batch, depth, height, width, channels)
    )


class WindowAttention3D(nn.Module):
    def __init__(self, channels: int, heads: int, window_size: int) -> None:
        super().__init__()
        if channels % heads:
            raise ValueError("channels must be divisible by heads")
        self.channels = channels
        self.heads = heads
        self.window_size = window_size
        self.head_dim = channels // heads
        self.scale = self.head_dim**-0.5
        self.qkv = nn.Conv3d(channels, 3 * channels, kernel_size=3, padding=1)
        self.projection = nn.Linear(channels, channels)

        side = 2 * window_size - 1
        self.relative_bias = nn.Parameter(torch.zeros(side**3, heads))
        coordinates = torch.stack(
            torch.meshgrid(
                torch.arange(window_size),
                torch.arange(window_size),
                torch.arange(window_size),
                indexing="ij",
            )
        ).flatten(1)
        relative = coordinates[:, :, None] - coordinates[:, None, :]
        relative = relative.permute(1, 2, 0).contiguous() + window_size - 1
        relative[:, :, 0] *= side * side
        relative[:, :, 1] *= side
        self.register_buffer("relative_index", relative.sum(-1), persistent=False)
        nn.init.trunc_normal_(self.relative_bias, std=0.02)

    def forward(
        self,
        windows: Tensor,
        attention_mask: Tensor | None,
        valid_keys: Tensor | None,
        windows_per_sample: int,
    ) -> Tensor:
        count = windows.shape[0]
        size = self.window_size
        tokens = size**3
        source = windows.permute(0, 4, 1, 2, 3).contiguous()
        qkv = self.qkv(source).flatten(2).transpose(1, 2)
        qkv = qkv.view(count, tokens, 3, self.heads, self.head_dim)
        qkv = qkv.permute(2, 0, 3, 1, 4)
        query, key, value = qkv.unbind(0)
        scores = (query * self.scale) @ key.transpose(-2, -1)
        bias = self.relative_bias[self.relative_index.reshape(-1)]
        bias = bias.view(tokens, tokens, self.heads).permute(2, 0, 1)
        scores = scores + bias.unsqueeze(0)

        batch = count // windows_per_sample
        scores = scores.view(batch, windows_per_sample, self.heads, tokens, tokens)
        if attention_mask is not None:
            scores = scores + attention_mask[None, :, None]
        if valid_keys is not None:
            scores = scores.masked_fill(~valid_keys[None, :, None, None, :], -100.0)
        scores = scores.view(count, self.heads, tokens, tokens)
        attention = scores.softmax(dim=-1)
        output = (attention @ value).transpose(1, 2).reshape(count, tokens, self.channels)
        output = self.projection(output)
        return output.view(count, size, size, size, self.channels)


class ConvMlp3D(nn.Module):
    def __init__(self, channels: int, ratio: int = 4) -> None:
        super().__init__()
        hidden = channels * ratio
        self.first = nn.Linear(channels, hidden)
        self.depthwise = nn.Conv3d(
            hidden, hidden, kernel_size=3, padding=1, groups=hidden
        )
        self.second = nn.Linear(hidden, channels)

    def forward(self, x: Tensor) -> Tensor:
        x = F.gelu(self.first(x))
        x = x.permute(0, 4, 1, 2, 3).contiguous()
        x = F.gelu(self.depthwise(x))
        x = x.permute(0, 2, 3, 4, 1).contiguous()
        return self.second(x)


class SwinConvBlock3D(nn.Module):
    def __init__(
        self,
        channels: int,
        heads: int,
        window_size: int,
        shifted: bool,
        mlp_ratio: int,
    ) -> None:
        super().__init__()
        self.window_size = window_size
        self.shift = window_size // 2 if shifted else 0
        self.norm1 = nn.LayerNorm(channels)
        self.attention = WindowAttention3D(channels, heads, window_size)
        self.norm2 = nn.LayerNorm(channels)
        self.mlp = ConvMlp3D(channels, mlp_ratio)

    def _masks(
        self,
        depth: int,
        height: int,
        width: int,
        original: tuple[int, int, int],
        device: torch.device,
    ) -> tuple[Tensor | None, Tensor]:
        size = self.window_size
        od, oh, ow = original
        valid = torch.zeros((1, depth, height, width, 1), dtype=torch.bool, device=device)
        valid[:, :od, :oh, :ow] = True
        if self.shift:
            valid = torch.roll(valid, shifts=(-self.shift,) * 3, dims=(1, 2, 3))
        valid_windows = window_partition(valid, size).view(-1, size**3)
        if not self.shift:
            return None, valid_windows

        labels = torch.zeros((1, depth, height, width, 1), device=device)
        depth_slices = (
            slice(0, -size),
            slice(-size, -self.shift),
            slice(-self.shift, None),
        )
        height_slices = depth_slices
        width_slices = depth_slices
        counter = 0
        for ds in depth_slices:
            for hs in height_slices:
                for ws in width_slices:
                    labels[:, ds, hs, ws] = counter
                    counter += 1
        label_windows = window_partition(labels, size).view(-1, size**3)
        difference = label_windows[:, None, :] - label_windows[:, :, None]
        mask = difference.masked_fill(difference != 0, -100.0).masked_fill(
            difference == 0, 0.0
        )
        return mask, valid_windows

    def forward(self, x: Tensor) -> Tensor:
        # Input/output use channels-first for efficient convolutions elsewhere.
        residual = x
        x = x.permute(0, 2, 3, 4, 1).contiguous()
        original = x.shape[1:4]
        x = self.norm1(x)
        x, _ = _pad_channels_last(x, self.window_size)
        batch, depth, height, width, _ = x.shape
        if self.shift:
            x = torch.roll(x, shifts=(-self.shift,) * 3, dims=(1, 2, 3))
        windows = window_partition(x, self.window_size)
        windows_per_sample = windows.shape[0] // batch
        attention_mask, valid_keys = self._masks(
            depth, height, width, original, x.device
        )
        windows = self.attention(
            windows, attention_mask, valid_keys, windows_per_sample
        )
        x = window_reverse(
            windows, self.window_size, batch, depth, height, width
        )
        if self.shift:
            x = torch.roll(x, shifts=(self.shift,) * 3, dims=(1, 2, 3))
        od, oh, ow = original
        x = x[:, :od, :oh, :ow]
        x = residual + x.permute(0, 4, 1, 2, 3).contiguous()

        residual = x
        x = x.permute(0, 2, 3, 4, 1).contiguous()
        x = self.mlp(self.norm2(x))
        return residual + x.permute(0, 4, 1, 2, 3).contiguous()


class SwinConvPair3D(nn.Module):
    def __init__(self, channels: int, heads: int, window_size: int, mlp_ratio: int) -> None:
        super().__init__()
        self.regular = SwinConvBlock3D(
            channels, heads, window_size, shifted=False, mlp_ratio=mlp_ratio
        )
        self.shifted = SwinConvBlock3D(
            channels, heads, window_size, shifted=True, mlp_ratio=mlp_ratio
        )

    def forward(self, x: Tensor) -> Tensor:
        return self.shifted(self.regular(x))


class Exchange(nn.Module):
    def __init__(self, source: int, target: int, steps: int) -> None:
        super().__init__()
        if steps == 0:
            if source != target:
                raise ValueError("identity exchange requires matching channels")
            self.mode = "identity"
            self.operation = nn.Identity()
        elif steps > 0:
            self.mode = "down"
            layers: list[nn.Module] = []
            current = source
            for index in range(steps):
                output = target if index == steps - 1 else current
                layers.extend(
                    [
                        nn.Conv3d(current, output, 3, stride=2, padding=1, bias=False),
                        nn.GroupNorm(1, output),
                        nn.GELU(),
                    ]
                )
                current = output
            self.operation = nn.Sequential(*layers)
        else:
            self.mode = "up"
            self.steps = -steps
            self.operation = nn.Conv3d(source, target, 1, bias=False)

    def forward(self, x: Tensor, target_shape: tuple[int, int, int]) -> Tensor:
        x = self.operation(x)
        if self.mode == "up":
            x = F.interpolate(x, size=target_shape, mode="trilinear", align_corners=False)
        return x


class MultiResolutionStage(nn.Module):
    def __init__(
        self,
        channels: tuple[int, ...],
        heads: tuple[int, ...],
        window_size: int,
        mlp_ratio: int,
        use_checkpoint: bool,
    ) -> None:
        super().__init__()
        self.use_checkpoint = use_checkpoint
        self.transformers = nn.ModuleList(
            [
                SwinConvPair3D(channel, head, window_size, mlp_ratio)
                for channel, head in zip(channels, heads)
            ]
        )
        self.exchanges = nn.ModuleList(
            [
                nn.ModuleList(
                    [
                        Exchange(channels[source], channels[target], target - source)
                        for source in range(len(channels))
                    ]
                )
                for target in range(len(channels))
            ]
        )

    def _transform(self, module: nn.Module, value: Tensor) -> Tensor:
        if self.use_checkpoint and self.training and torch.is_grad_enabled():
            return checkpoint(module, value, use_reentrant=False)
        return module(value)

    def forward(self, inputs: list[Tensor]) -> list[Tensor]:
        transformed = [
            self._transform(module, value)
            for module, value in zip(self.transformers, inputs)
        ]
        outputs: list[Tensor] = []
        for target, target_value in enumerate(transformed):
            shape = tuple(target_value.shape[2:])
            contributions = [
                self.exchanges[target][source](value, shape)
                for source, value in enumerate(transformed)
            ]
            outputs.append(F.gelu(torch.stack(contributions, dim=0).sum(dim=0)))
        return outputs


class FaultEdgeFormerInspired(nn.Module):
    def __init__(
        self,
        channels: tuple[int, int, int] = (16, 32, 56),
        heads: tuple[int, int, int] = (1, 2, 4),
        window_size: int = 7,
        mlp_ratio: int = 4,
        sobel_repeats: int = 2,
        use_checkpoint: bool = True,
    ) -> None:
        super().__init__()
        if len(channels) != 3 or len(heads) != 3:
            raise ValueError("this controlled model uses exactly three parallel streams")
        self.spec = model_spec(
            channels=channels,
            heads=heads,
            window_size=window_size,
            mlp_ratio=mlp_ratio,
            sobel_repeats=sobel_repeats,
        )
        self.sobel = TrainableSobel3D(sobel_repeats)
        self.stem = nn.Sequential(
            nn.Conv3d(self.sobel.out_channels, channels[0], 3, padding=1, bias=False),
            nn.GroupNorm(1, channels[0]),
            nn.GELU(),
            nn.Conv3d(channels[0], channels[0], 3, padding=1, bias=False),
            nn.GroupNorm(1, channels[0]),
            nn.GELU(),
        )
        self.first_down = nn.Sequential(
            nn.Conv3d(channels[0], channels[0], 3, stride=2, padding=1, bias=False),
            nn.GroupNorm(1, channels[0]),
            nn.GELU(),
        )
        self.stage2 = MultiResolutionStage(
            channels[:1], heads[:1], window_size, mlp_ratio, use_checkpoint
        )
        self.add_second = Exchange(channels[0], channels[1], 1)
        self.stage3 = MultiResolutionStage(
            channels[:2], heads[:2], window_size, mlp_ratio, use_checkpoint
        )
        self.add_third = nn.ModuleList(
            [
                Exchange(channels[0], channels[2], 2),
                Exchange(channels[1], channels[2], 1),
            ]
        )
        self.stage4 = MultiResolutionStage(
            channels, heads, window_size, mlp_ratio, use_checkpoint
        )
        self.final_to_high = nn.ModuleList(
            [
                Exchange(channels[0], channels[0], 0),
                Exchange(channels[1], channels[0], -1),
                Exchange(channels[2], channels[0], -2),
            ]
        )
        self.head = nn.Conv3d(channels[0], 1, 1)

    def forward(self, x: Tensor) -> Tensor:
        output_shape = tuple(x.shape[2:])
        x = self.stem(self.sobel(x))
        high = self.first_down(x)
        high = self.stage2([high])[0]

        second_shape = tuple((length + 1) // 2 for length in high.shape[2:])
        medium = self.add_second(high, second_shape)
        high, medium = self.stage3([high, medium])

        third_shape = tuple((length + 1) // 2 for length in medium.shape[2:])
        low = self.add_third[0](high, third_shape) + self.add_third[1](medium, third_shape)
        high, medium, low = self.stage4([high, medium, F.gelu(low)])

        high_shape = tuple(high.shape[2:])
        fused = sum(
            exchange(value, high_shape)
            for exchange, value in zip(self.final_to_high, (high, medium, low))
        )
        fused = F.gelu(fused)
        fused = F.interpolate(fused, size=output_shape, mode="trilinear", align_corners=False)
        return self.head(fused)


def count_parameters(model: nn.Module) -> int:
    return sum(parameter.numel() for parameter in model.parameters() if parameter.requires_grad)


if __name__ == "__main__":
    model = FaultEdgeFormerInspired(use_checkpoint=False)
    example = torch.randn(1, 1, 32, 32, 32)
    output = model(example)
    print({"parameters": count_parameters(model), "shape": tuple(output.shape), "spec": model.spec})
