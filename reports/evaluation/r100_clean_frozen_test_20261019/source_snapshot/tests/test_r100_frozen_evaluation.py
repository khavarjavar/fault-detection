"""Regression checks for geometry, masks, frozen thresholds and count gates."""
import math
from pathlib import Path
import sys
import tempfile
import unittest

import h5py
import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import evaluate_r100_frozen_test as evaluation


class FrozenEvaluationTests(unittest.TestCase):
    def test_test_geometry_is_not_validation_geometry(self):
        evaluation.check_shape("test", (703, 3174, 1537))
        evaluation.check_shape("val", (200, 3174, 1537))
        with self.assertRaisesRegex(RuntimeError, "Unexpected test shape"):
            evaluation.check_shape("test", (200, 3174, 1537))
        for split, expected in evaluation.SPLITS.items():
            coords = evaluation.r100.tiling(expected["shape"])
            self.assertEqual(len(coords), expected["patches"])
            covered = sum(math.prod(min(128, n-start) for n, start in zip(expected["shape"], origin))
                          for origin in coords)
            self.assertEqual(covered, math.prod(expected["shape"]))

    def test_cross_file_reader_mask_padding_and_axis_reversal(self):
        raw = np.arange(5*4*3, dtype=np.float32).reshape(5, 4, 3)
        target = np.zeros_like(raw, dtype=np.uint8)
        target[0, 0, 0] = 1  # A positive outside the nonzero-input mask.
        target[4, 2, 1] = 1
        with tempfile.TemporaryDirectory() as tmp:
            paths = []
            for index, section in enumerate((slice(0, 2), slice(2, 5))):
                path = Path(tmp) / f"block{index}.h5"
                with h5py.File(path, "w") as handle:
                    handle["seismic"] = raw[section]
                    handle["fault"] = target[section]
                paths.append(path)
            reader = evaluation.r100.ConcatenatedThebe(paths)
            try:
                x, y, mask, shape, observed, excluded, constant = evaluation.r100.read_patch(reader, (0, 0, 0))
            finally:
                reader.close()
        self.assertEqual(shape, (5, 4, 3))
        self.assertEqual(observed, 59)
        self.assertEqual(excluded, 1)
        self.assertFalse(constant)
        self.assertEqual(int(mask.sum()), 59)
        self.assertEqual(int(y[mask].sum()), 1)
        self.assertTrue(mask[0, 0, 1, 2, 4])  # Reversed (x,y,z) -> (z,y,x).
        self.assertFalse(mask[0, 0, 0, 0, 0])
        self.assertEqual(int(mask[..., 5:].sum()), 0)  # Padded axis-zero samples.
        self.assertAlmostEqual(float(x[mask].mean()), 0, places=6)
        self.assertAlmostEqual(float(x[mask].std(correction=0)), 1, places=6)

    def test_frozen_grid_threshold_matches_direct_confusion(self):
        threshold = 0.27490234375
        p = torch.tensor([0., threshold-1/2048, threshold, 1.], dtype=torch.float32)
        y = torch.tensor([0., 1., 1., 0.])
        hist = evaluation.r100.baseline.ProbabilityHistogram(2048)
        hist.update_probabilities(p, y)
        m = hist.metrics(threshold)
        self.assertEqual((m.tp, m.fp, m.fn, m.tn), (1, 1, 1, 1))
        self.assertAlmostEqual(m.dice, 0.5, places=12)

    def test_histogram_gate_rejects_same_totals_in_different_bins(self):
        hist = evaluation.r100.baseline.ProbabilityHistogram(2048)
        hist.positive[10] = 2
        hist.negative[20] = 3
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "reference.npz"
            evaluation.save_histograms(path, {"seed42": hist})
            self.assertTrue(evaluation.compare_histograms({"seed42": hist}, path)["seed42"]["positive"]["exact_match"])
            hist.positive[10] -= 1
            hist.positive[11] += 1
            with self.assertRaisesRegex(RuntimeError, "Test files remain unopened"):
                evaluation.compare_histograms({"seed42": hist}, path)

    def test_coverage_gate_rejects_missing_scored_voxel(self):
        spec = evaluation.SPLITS["test"]
        coverage = {k: spec[k] for k in ("patches", "valid_voxels", "positive_voxels", "positive_labels_excluded")}
        coverage["raw_voxels"] = math.prod(spec["shape"])
        hist = evaluation.r100.baseline.ProbabilityHistogram(2048)
        hist.positive[0] = spec["positive_voxels"]
        hist.negative[0] = spec["valid_voxels"] - spec["positive_voxels"]
        evaluation.check_coverage("test", coverage, {"ensemble": hist})
        hist.negative[0] -= 1
        with self.assertRaisesRegex(RuntimeError, "histogram counts disagree"):
            evaluation.check_coverage("test", coverage, {"ensemble": hist})

    def test_seed_summary_uses_sample_sd_and_excludes_ensemble(self):
        test = {"metrics": {f"seed{s}": {"dice": value, "threshold": .5} for s, value in zip((42, 43, 44), (.4, .5, .6))}}
        test["metrics"]["ensemble"] = {"dice": .99, "threshold": .5}
        summary = evaluation.seed_summary(test)
        self.assertAlmostEqual(summary["dice"]["mean"], .5)
        self.assertAlmostEqual(summary["dice"]["sample_sd"], .1)
        self.assertNotIn("threshold", summary)


if __name__ == "__main__":
    torch.set_num_threads(2)
    unittest.main()
