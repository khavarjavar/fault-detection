# Geological fault detection experiments

Research code and experiment records for seismic fault segmentation on FaultSeg3D, CRACKS, and Thebe. The repository covers 3-D CNN and transformer models, 2-D controls, validation protocols, visual comparisons, and field-survey preparation.

Raw seismic data, virtual environments, model checkpoints, training caches, and cloned third-party repositories are excluded. The original working directory is 94 GB; this repository contains the reproducible code and reports only.

## Selected Thebe validation result

| Model | Dice | PR-AUC |
|---|---:|---:|
| FaultSeg3D R100, epoch 144 | 0.5907 | 0.6229 |
| MONAI SwinUNETR, epoch 140 | 0.5779 | 0.6076 |
| R100 0.55 + SwinUNETR 0.45 | **0.6058** | **0.6486** |

The ensemble weight and threshold were selected on the complete Thebe validation split. Thebe test data was not used for this selection. See the [ensemble result](reports/evaluation/r100150_swinunetr_validation_ensemble_20261104/result.json) and the [mentor handoff note](reports/handoff/MENTOR_FAULT_ENSEMBLE_HANDOFF_20261104.md).

The earlier three-seed R100 study used a frozen held-out test protocol. Its equal-probability ensemble reached test Dice 0.5813. See the [test report](reports/evaluation/r100_clean_frozen_test_20261019/report.md) and [protocol](reports/experiments/R100_FROZEN_TEST_PROTOCOL_20261019.md).

## Repository layout

- `scripts/`: training, evaluation, visualization, and dataset preparation
- `configs/`: experiment configuration files
- `tests/`: focused pipeline and model checks
- `reports/`: experiment records, metrics, audits, and figures
- `technical_reports/`: short reports for the main experiment stages
- `EXTERNAL_SOURCES.md`: third-party repositories and pinned revisions

## Environment

The most recent runs used Python 3.13, PyTorch 2.7.1, CUDA 11.8, and MONAI 1.5.1.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install torch==2.7.1 torchvision==0.22.1 --index-url https://download.pytorch.org/whl/cu118
python -m pip install -r requirements.txt
```

Install a PyTorch build matching the local CUDA driver when CUDA 11.8 is not appropriate.

## Data

Dataset files are deliberately not stored in Git. Training scripts expect local HDF5 or SEG-Y data under `data/`; individual run configurations and reports record the exact files and split rules used. Review dataset licenses before downloading or redistributing any survey.

The main entry points are:

- `scripts/train_r100_fp16_clean.py`
- `scripts/train_swinunetr_thebe_matched.py`
- `scripts/evaluate_r100_swin_validation_ensemble.py`
- `scripts/visualize_r100_faultsegv3_validation.py`
- `scripts/prepare_attention3d_field_surveys.py`

Use `--help` on a script before running it. Several experiment scripts intentionally require exact data manifests and will stop if files or source hashes differ.
