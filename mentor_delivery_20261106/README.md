# R100 3-D fault detector

This package contains one FaultSeg3D R100 model trained from scratch on Thebe. It runs inference on a 3-D seismic volume and writes a fault-probability volume and a binary fault mask.

The package does not contain SwinUNETR or ensemble code.

## Model and result

| Item | Value |
|---|---|
| Architecture | FaultSeg3D 3-D U-Net |
| Checkpoint | epoch 144 |
| Training data | Thebe train1 through train9 |
| Validation data | Thebe val1 and val2 |
| Full validation Dice | 0.590735 |
| Full validation PR-AUC | 0.622857 |
| Threshold | 0.1923828125 |

The checkpoint was selected using validation data. The Thebe test files were not opened during training or selection. These numbers describe Thebe validation and may change on another survey.

## Training configuration

| Setting | Value |
|---|---|
| Seed | 43 |
| Training epochs | 150 |
| Patches per epoch | 360 |
| Patch size | 128 x 128 x 128 |
| Optimizer | Adam |
| Learning rate | 0.0001 |
| Loss | BCE over valid voxels |
| Gradient accumulation | 2 |
| Precision | float16 autocast |
| Normalization | z-score per cube over valid voxels |

The complete recorded settings are in `training_config.json`. The final run state is in `training_status.json`.

## Hardware and setup

An NVIDIA GPU is recommended for a field volume. The model was trained with Python 3.13, PyTorch 2.7.1, CUDA 11.8, and an NVIDIA RTX A5500.

Run from this directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install torch==2.7.1 --index-url https://download.pytorch.org/whl/cu118
python -m pip install -r requirements.txt
```

For SEG-Y input:

```bash
python -m pip install -r requirements-segy.txt
```

Install the PyTorch build matching the workstation's CUDA version if it does not use CUDA 11.8.

## Verify the package

```bash
sha256sum -c CHECKSUMS.sha256
python smoke_test.py
```

The smoke test checks the checkpoint hash, loads the model strictly, and runs a small CPU inference.

## Input

The input must be one 3-D seismic amplitude volume in one of these formats:

- NumPy `.npy`
- NumPy `.npz`
- HDF5 `.h5` or `.hdf5`
- SEG-Y `.sgy` or `.segy`

Use `--axes` to describe the stored array dimensions:

- `x`: inline
- `y`: crossline
- `z`: time or depth sample

For example, use `--axes xyz` for `(inline, crossline, sample)` and `--axes zyx` for `(sample, crossline, inline)`.

For HDF5 and NPZ files, the default dataset or key is `seismic`. Change it with `--dataset`.

Zero amplitude is treated as no-data, matching training. Add `--valid-all` only when zero is a valid amplitude and the survey has no zero padding.

## Run inference

HDF5 example:

```bash
python infer_volume.py \
  --input survey.h5 \
  --dataset seismic \
  --axes xyz \
  --output survey_r100_faults.h5
```

NumPy example:

```bash
python infer_volume.py \
  --input survey.npy \
  --axes zyx \
  --output survey_r100_faults.h5
```

SEG-Y example:

```bash
python infer_volume.py \
  --input survey.sgy \
  --axes xyz \
  --output survey_r100_faults.h5
```

SEG-Y is read as `(inline, crossline, sample)` and must contain geometry that `segyio` can read.

The script processes non-overlapping 128 x 128 x 128 cubes. Edge cubes are padded internally. Each cube is normalized over its valid voxels.

## Output

The output HDF5 file contains:

- `fault_probability`: float16 probabilities with the input shape and axis order
- `fault_mask`: uint8 mask with the input shape and axis order

The frozen decision rule is:

```text
fault_mask = R100_probability >= 0.1923828125
```

Start with a small subvolume containing a known fault. Check the input axis order and inspect both datasets before running the full survey.

## Files

```text
README.md
infer_volume.py
models.py
smoke_test.py
model_manifest.json
training_config.json
training_status.json
validation_metrics.json
requirements.txt
requirements-segy.txt
CHECKSUMS.sha256
weights/r100_epoch144.pth
```
