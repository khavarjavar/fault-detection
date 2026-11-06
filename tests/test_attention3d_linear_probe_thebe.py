#!/usr/bin/env python3
import math
import sys
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import train_evaluate_attention3d_linear_probe_thebe as probe
import faultseg3d_baseline as baseline


def test_histogram_confusion_and_auc_are_finite():
    histogram = probe.Histogram()
    probability = torch.tensor([0.9, 0.8, 0.2, 0.1])
    target = torch.tensor([1.0, 0.0, 1.0, 0.0])
    histogram.update(probability, target)
    metrics = histogram.metrics(0.5)
    assert (metrics.tp, metrics.fp, metrics.fn, metrics.tn) == (1, 1, 1, 1)
    assert math.isclose(metrics.dice, 0.5)
    assert math.isclose(metrics.iou, 1 / 3)
    assert math.isfinite(metrics.pr_auc_approx)
    assert math.isfinite(metrics.roc_auc_approx)


def test_best_threshold_uses_validation_dice():
    histogram = probe.Histogram()
    histogram.update(
        torch.tensor([0.95, 0.80, 0.70, 0.10]),
        torch.tensor([1.0, 1.0, 0.0, 0.0]),
    )
    threshold = histogram.best_threshold()
    metrics = histogram.metrics(threshold)
    assert metrics.dice > histogram.metrics(0.9).dice
    assert metrics.tp == 2


def test_auc_and_metrics_match_existing_project_histogram():
    probability = torch.tensor([0.99, 0.80, 0.70, 0.51, 0.49, 0.20, 0.01])
    target = torch.tensor([1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0])
    ours = probe.Histogram()
    existing = baseline.ProbabilityHistogram(probe.BINS)
    ours.update(probability, target)
    existing.update_probabilities(probability, target)
    threshold = ours.best_threshold()
    left = ours.metrics(threshold)
    right = existing.metrics(threshold)
    for name in left.__dataclass_fields__:
        assert math.isclose(float(getattr(left, name)), float(getattr(right, name)),
                            rel_tol=0.0, abs_tol=1e-12), name


if __name__ == "__main__":
    test_histogram_confusion_and_auc_are_finite()
    test_best_threshold_uses_validation_dice()
    test_auc_and_metrics_match_existing_project_histogram()
    print("3 Attention3D linear-probe tests passed")
