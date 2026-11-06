import importlib.util
from pathlib import Path

import numpy as np


SCRIPT = Path(__file__).parents[1] / "scripts" / "prepare_attention3d_field_surveys.py"
SPEC = importlib.util.spec_from_file_location("prepare_attention3d", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def test_window_starts_does_not_force_unpublished_terminal_window():
    assert MODULE.window_starts(1500, 64, 32).tolist() == list(range(0, 1409, 32))


def test_full_valid_windows_exclude_holes():
    valid = np.ones((96, 128), dtype=bool)
    valid[10, 10] = False
    starts = MODULE.full_valid_spatial_starts(valid, 64, 64, 32, 32)
    assert {tuple(x) for x in starts.tolist()} == {
        (0, 32), (0, 64), (32, 0), (32, 32), (32, 64)
    }


def test_spatial_split_has_no_voxel_overlap():
    valid = np.ones((320, 128), dtype=bool)
    train, validation, summary = MODULE.enumerate_coordinates(
        valid, 128, (64, 64, 64), (32, 32, 32), 0.8
    )
    assert train.size and validation.size
    assert int(train[:, 0].max()) + 64 <= int(validation[:, 0].min())
    assert summary["excluded_crossing_spatial_windows"] >= 1


if __name__ == "__main__":
    test_window_starts_does_not_force_unpublished_terminal_window()
    test_full_valid_windows_exclude_holes()
    test_spatial_split_has_no_voxel_overlap()
    print("3 preprocessing tests passed")
