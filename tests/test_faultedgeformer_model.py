"""CPU invariants for the FaultEdgeFormer-inspired architecture."""

import sys
import unittest
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from faultedgeformer_model import (
    FaultEdgeFormerInspired,
    TrainableSobel3D,
    multidirectional_sobel_kernels,
    window_partition,
    window_reverse,
)


class FaultEdgeFormerModelTests(unittest.TestCase):
    def test_nine_sobel_directions_are_zero_sum_and_trainable(self):
        kernels = multidirectional_sobel_kernels()
        self.assertEqual(tuple(kernels.shape), (9, 1, 3, 3, 3))
        self.assertTrue(torch.allclose(kernels.sum((1, 2, 3, 4)), torch.zeros(9)))
        layer = TrainableSobel3D(repeats=2)
        output = layer(torch.randn(1, 1, 7, 8, 9))
        self.assertEqual(tuple(output.shape), (1, 18, 7, 8, 9))
        output.square().mean().backward()
        self.assertIsNotNone(layer.gamma.grad)
        self.assertTrue(torch.isfinite(layer.gamma.grad).all())

    def test_window_partition_reverse_is_exact(self):
        value = torch.arange(2 * 8 * 12 * 16 * 3).reshape(2, 8, 12, 16, 3)
        windows = window_partition(value, 4)
        restored = window_reverse(windows, 4, 2, 8, 12, 16)
        self.assertTrue(torch.equal(value, restored))

    def test_non_divisible_volume_preserves_shape_and_has_finite_gradient(self):
        model = FaultEdgeFormerInspired(
            channels=(4, 8, 8),
            heads=(1, 2, 2),
            window_size=4,
            mlp_ratio=2,
            sobel_repeats=1,
            use_checkpoint=False,
        )
        value = torch.randn(1, 1, 13, 15, 17, requires_grad=True)
        output = model(value)
        self.assertEqual(output.shape, value.shape)
        output.square().mean().backward()
        self.assertIsNotNone(value.grad)
        self.assertTrue(torch.isfinite(value.grad).all())
        self.assertTrue(all(
            parameter.grad is None or torch.isfinite(parameter.grad).all()
            for parameter in model.parameters()
        ))


if __name__ == "__main__":
    torch.set_num_threads(2)
    unittest.main()
