"""Small synthetic checks; these do not open Thebe or run a model."""
from pathlib import Path
import sys
import tempfile
import unittest

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import analyze_r100_seed_curve as analysis
from cache_r100_validation import sha256, verify_cache_file


class SeedCurveTests(unittest.TestCase):
    def test_all_existing_combinations_are_measured(self):
        groups = analysis.choose_subsets(3, [1, 2, 3], 32, 1042)
        self.assertEqual(len(groups), 7)
        self.assertEqual(len(set(groups)), 7)
        self.assertEqual([sum(len(g) == n for g in groups) for n in (1, 2, 3)], [3, 3, 1])

    def test_sampling_is_unique_and_reproducible(self):
        first = analysis.choose_subsets(10, [5], 32, 1042)
        self.assertEqual(first, analysis.choose_subsets(10, [5], 32, 1042))
        self.assertEqual(len(set(first)), 32)
        self.assertTrue(all(len(group) == 5 for group in first))
        with self.assertRaises(ValueError):
            analysis.choose_subsets(3, [5], 32, 1042)

    def test_streamed_counts_match_direct_average(self):
        maps = np.array([[.05, .9, .4, .8, .3], [.2, .7, .1, .6, .4], [.1, .8, .2, .7, .2]], dtype="float32")
        labels = np.array([0, 1, 0, 1, 1], dtype="uint8")
        groups = analysis.choose_subsets(3, [1, 2, 3], 32, 1042)
        hist = analysis.score_subsets(maps, labels, groups, torch.device("cpu"), 2)
        for group, h in zip(groups, hist):
            probability = maps[list(group)].mean(0)
            indices = np.minimum((probability*2048).astype("int64"), 2047)
            self.assertTrue(np.array_equal(h.positive.numpy(), np.bincount(indices[labels == 1], minlength=2048)))
            self.assertTrue(np.array_equal(h.negative.numpy(), np.bincount(indices[labels == 0], minlength=2048)))

    def test_threshold_is_selected_for_the_averaged_prediction(self):
        maps = np.array([[.15, .35, .05, .25], [.25, .45, .15, .35]], dtype="float32")
        labels = np.array([1, 1, 0, 0], dtype="uint8")
        histogram = analysis.score_subsets(maps, labels, [(0, 1)], torch.device("cpu"), 3)[0]
        threshold = histogram.best_dice_threshold()
        self.assertEqual(threshold, 409/2048)
        self.assertAlmostEqual(histogram.metrics(threshold).dice, .8)
        self.assertEqual(histogram.metrics(.5).dice, 0)

    def test_single_full_pool_subset_has_no_estimated_sd(self):
        rows = [{"size": 1, "threshold": .5, "validation": {"dice": .4}},
                {"size": 1, "threshold": .5, "validation": {"dice": .6}},
                {"size": 2, "threshold": .5, "validation": {"dice": .7}}]
        summary = analysis.summarize(rows)
        self.assertAlmostEqual(summary[0]["mean_dice"], .5)
        self.assertAlmostEqual(summary[0]["subset_sample_sd"], np.sqrt(.02))
        self.assertIsNone(summary[1]["subset_sample_sd"])

    def test_corrupted_cache_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "probabilities.npy"
            np.save(path, np.array([.2, .8], dtype="float32"))
            expected = sha256(path)
            verify_cache_file(path, expected, "float32", count=2)
            data = bytearray(path.read_bytes())
            data[-1] ^= 1
            path.write_bytes(data)
            with self.assertRaisesRegex(RuntimeError, "checksum differs"):
                verify_cache_file(path, expected, "float32", count=2)


if __name__ == "__main__":
    torch.set_num_threads(2)
    unittest.main()
