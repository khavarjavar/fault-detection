import sys
from pathlib import Path

import numpy as np
import torch


sys.path.insert(0, str((Path(__file__).parents[1] / "scripts").resolve()))
import train_attention3d_two_survey_pretext as pretext


class DummyStore:
    def __init__(self, survey_id: str, offset: int):
        self.id = survey_id
        base = np.arange(240, dtype=np.int32).reshape(60, 4)[:, 1:]
        self.train = base + offset
        self.validation = base[:20] + offset + 10_000


def test_balanced_schedule_is_unique_and_reproducible():
    stores = [DummyStore("a", 0), DummyStore("b", 1_000)]
    first_train, first_validation = pretext.build_schedule(stores, 3, 20, 5, 42)
    second_train, second_validation = pretext.build_schedule(stores, 3, 20, 5, 42)
    assert np.array_equal(first_train, second_train)
    assert np.array_equal(first_validation, second_validation)
    flattened = first_train.reshape(-1, 4)
    assert np.unique(flattened, axis=0).shape[0] == flattened.shape[0]
    assert np.count_nonzero(flattened[:, 0] == 0) == 30
    assert np.count_nonzero(flattened[:, 0] == 1) == 30


def test_corruption_uses_published_fraction_range():
    clean = torch.ones((1, 1, 64, 64, 64), dtype=torch.float32)
    noisy, fraction, sigma = pretext.corrupt(clean, torch.Generator().manual_seed(7))
    assert noisy.shape == clean.shape
    assert torch.isfinite(noisy).all()
    assert 0.05 <= fraction <= 0.30
    assert abs(sigma - fraction) < 1e-6


if __name__ == "__main__":
    test_balanced_schedule_is_unique_and_reproducible()
    test_corruption_uses_published_fraction_range()
    print("2 pretext-training tests passed")
