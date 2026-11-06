#!/usr/bin/env python3
"""Create the completion report for two-survey Attention3D pretraining."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
from pathlib import Path

import torch


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(8 * 1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--output", type=Path, default=Path("reports/evaluation/attention3d_two_survey_pretext_seed42_20261026"))
    args = parser.parse_args()
    state = json.loads((args.run_dir / "state.json").read_text())
    config = json.loads((args.run_dir / "run_config.json").read_text())
    data_check = json.loads((args.run_dir / "data_check.json").read_text())
    if state.get("status") != "complete" or state.get("next_epoch") != 50:
        raise RuntimeError(f"Attention3D pretraining is not complete: {state}")
    with (args.run_dir / "history.csv").open(newline="") as stream:
        history = list(csv.DictReader(stream))
    if len(history) != 50 or [int(row["epoch"]) for row in history] != list(range(1, 51)):
        raise RuntimeError("Attention3D history is incomplete")
    best_path = Path(state["best_checkpoint"])
    if sha256(best_path) != state["best_checkpoint_sha256"]:
        raise RuntimeError("Attention3D best checkpoint changed")
    best = torch.load(best_path, map_location="cpu", weights_only=False)
    validation = best["validation"]
    result = {
        "status": "complete",
        "experiment": config["experiment"],
        "claim_scope": "two-survey self-supervised denoising pretraining variant",
        "seed": config["seed"],
        "epochs": config["epochs"],
        "training_patches": config["total_training_patches"],
        "balanced_training_counts": data_check["balanced_training_counts"],
        "best_epoch": int(best["epoch"]),
        "best_checkpoint": str(best_path),
        "best_checkpoint_sha256": state["best_checkpoint_sha256"],
        "validation": validation,
        "beats_noisy_identity_baseline": validation["network_mse"] < validation["noisy_identity_mse"],
        "kerry_included": False,
        "thebe_data_read": False,
        "fault_segmentation_test_status": "not applicable until transfer and supervised Thebe fine-tuning",
    }
    args.output.mkdir(parents=True, exist_ok=True)
    temporary_json = args.output / "result.json.part"
    temporary_json.write_text(json.dumps(result, indent=2) + "\n")
    os.replace(temporary_json, args.output / "result.json")
    text = f"""# Attention3D two-survey pretraining result

- Status: complete
- Best epoch: {result['best_epoch']}
- Training patches: {result['training_patches']:,} ({data_check['balanced_training_counts']['opunake']:,} Opunake; {data_check['balanced_training_counts']['kahu']:,} Kahu)
- Fixed-validation network MSE: {validation['network_mse']:.8f}
- Noisy-input identity MSE: {validation['noisy_identity_mse']:.8f}
- Identity minus network MSE: {validation['identity_minus_network_mse']:.8f}
- Beats identity baseline: {result['beats_noisy_identity_baseline']}
- Best checkpoint SHA-256: `{result['best_checkpoint_sha256']}`

This result measures self-supervised denoising on spatially held-out Opunake/Kahu cubes. It is not a Thebe fault-segmentation score. The checkpoint must be transferred and fine-tuned on Thebe train/validation before any frozen Thebe fault test. Kerry was not included.
"""
    temporary_report = args.output / "report.md.part"
    temporary_report.write_text(text)
    os.replace(temporary_report, args.output / "report.md")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
