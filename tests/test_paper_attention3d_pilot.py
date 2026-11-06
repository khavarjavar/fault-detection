"""CPU checks for the scientific controls in the short attention pilot."""
import sys
import unittest
from pathlib import Path

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import paper_attention3d_pilot as pilot


class SmallModel(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.features = torch.nn.Conv3d(1, 2, 1)
        self.register_buffer("feature_buffer", torch.tensor([3.0]))
        self.out_conv = torch.nn.Conv3d(2, 1, 1)


class LazyArray:
    shape = (100, 3174, 1537)

    def __init__(self, labels=False):
        self.labels = labels

    def __getitem__(self, slices):
        shape = tuple(s.stop - s.start for s in slices)
        x = np.indices(shape)[-1]
        return (x % 13 == 0).astype(np.uint8) if self.labels else (x + 1).astype(np.float32)


class NoLabels(dict):
    def __getitem__(self, key):
        if key == "fault":
            raise AssertionError("Pretext sampling read fault labels")
        return super().__getitem__(key)


class PilotTests(unittest.TestCase):
    def test_normalization_preserves_mask_and_reverses_non_cubic_axes(self):
        raw = np.arange(24, dtype=np.float32).reshape(2, 3, 4)
        x, mask = pilot.normalize(raw)
        self.assertEqual(tuple(x.shape), (1, 1, 4, 3, 2))
        np.testing.assert_array_equal(mask.numpy()[0, 0], (raw != 0).transpose())
        self.assertAlmostEqual(float(x[mask].mean()), 0, places=6)
        self.assertAlmostEqual(float(x[mask].square().mean()), 1, places=6)
        self.assertEqual(float(x[~mask].sum()), 0)
        self.assertIsNone(pilot.normalize(np.zeros((3, 4, 5), np.float32)))

    def test_internal_regions_are_separated_for_complete_crops(self):
        fit = pilot.region_y("pretrain", 3174)
        val = pilot.region_y("reconstruction_validation", 3174)
        self.assertGreaterEqual(val[0] - fit[1], 256)
        self.assertGreaterEqual(fit[1] - fit[0], pilot.PATCH)
        self.assertGreaterEqual(val[1] - val[0], pilot.PATCH)

    def test_corruption_only_touches_valid_input_and_keeps_target(self):
        x, mask = pilot.normalize(np.arange(27, dtype=np.float32).reshape(3, 3, 3))
        original = x.clone()
        a = pilot.corrupt(x, mask, torch.Generator().manual_seed(17))
        b = pilot.corrupt(x, mask, torch.Generator().manual_seed(17))
        self.assertTrue(torch.equal(a, b))
        self.assertTrue(torch.equal(x, original))
        self.assertTrue((a[~mask] == 0).all())
        self.assertFalse(torch.equal(a[mask], x[mask]))

    def test_transfer_includes_buffers_and_keeps_new_head(self):
        source, target = SmallModel(), SmallModel()
        source.feature_buffer.fill_(9)
        head = target.out_conv.weight.detach().clone()
        report = pilot.transfer_features(target, source.state_dict())
        self.assertTrue(report["exact_values_verified"])
        self.assertTrue(torch.equal(target.features.weight, source.features.weight))
        self.assertEqual(float(target.feature_buffer[0]), 9)
        self.assertTrue(torch.equal(target.out_conv.weight, head))

    def test_transfer_rejects_incomplete_and_mismatched_checkpoints(self):
        model = SmallModel()
        state = dict(model.state_dict())
        state.pop("feature_buffer")
        with self.assertRaises(ValueError):
            pilot.transfer_features(model, state)
        state = dict(model.state_dict())
        state["features.weight"] = torch.ones(3)
        with self.assertRaises(ValueError):
            pilot.transfer_features(model, state)

    def test_threshold_metrics_use_one_common_mask(self):
        positive = np.zeros(pilot.BINS, np.int64)
        negative = np.zeros_like(positive)
        positive[1500], positive[500] = 3, 1
        negative[1500], negative[100] = 2, 8
        result = pilot.metrics(positive, negative, 0.5)
        self.assertEqual([result[k] for k in ["tp", "fp", "fn", "tn"]], [3, 2, 1, 8])
        self.assertAlmostEqual(result["dice"], 6 / 9)
        self.assertGreaterEqual(pilot.metrics(positive, negative)["dice"], result["dice"])

    def test_paired_crop_stream_and_no_pretext_label_reads(self):
        data = pilot.Patches.__new__(pilot.Patches)
        path = Path("train1.h5")
        data.paths = {"train": [path], "val": []}
        data.handles = {path: {"seismic": LazyArray(), "fault": LazyArray(True)}}
        data.records = {}
        a = data.sample("supervised", 0)
        first = data.records.copy()
        b = data.sample("supervised", 0)
        self.assertEqual(first, data.records)
        self.assertTrue(all(torch.equal(x, y) for x, y in zip(a[:3], b[:3])))
        data.handles[path] = NoLabels({"seismic": LazyArray()})
        x, target, mask, _ = data.sample("pretrain", 0)
        self.assertIsNone(target)
        start = data.records["pretrain:0"]["start"]
        self.assertGreaterEqual(start[1], pilot.PRETEXT_FIT[0])
        self.assertLessEqual(start[1] + pilot.PATCH, pilot.PRETEXT_FIT[1])


if __name__ == "__main__":
    unittest.main()
