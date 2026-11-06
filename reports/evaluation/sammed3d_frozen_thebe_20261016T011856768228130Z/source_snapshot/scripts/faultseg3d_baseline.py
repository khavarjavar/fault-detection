#!/usr/bin/env python3
"""Train an architecture-faithful PyTorch FaultSeg3D baseline.

The network mirrors xinwucwp/faultSeg/unet3.py: channels 16/32/64/128,
two 3x3x3 convolutions per level, max pooling, nearest-neighbour upsampling,
skip concatenation, and a 1x1x1 output convolution.  The PyTorch module emits
logits so the loss can use numerically stable BCEWithLogitsLoss.

Two controlled runs are supported:

* b0_bce: official architecture with ordinary BCE (the active loss in the
  public training script).
* b1_weighted_dice: the identical architecture with train-only pos_weight and
  soft Dice, isolating imbalance handling from architectural changes.

Expected project layout:

  data/faultseg3d/train/{seis,fault}/*.dat
  data/faultseg3d/validation/{seis,fault}/*.dat
  data/manifests/faultseg3d_{train,val,test}.txt
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import random
import time
from contextlib import nullcontext
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
import torch
from torch import Tensor, nn
from torch.utils.data import DataLoader, Dataset


VOLUME_SHAPE = (128, 128, 128)
EXPECTED_PARAMETERS = 1_459_585
DEFAULT_POS_WEIGHT = 13.211662


def seed_everything(seed: int) -> None:
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True
    torch.use_deterministic_algorithms(True, warn_only=True)


class DoubleConv(nn.Module):
    def __init__(self, in_channels: int, out_channels: int) -> None:
        super().__init__()
        self.block = nn.Sequential(
            nn.Conv3d(in_channels, out_channels, kernel_size=3, padding=1, bias=True),
            nn.ReLU(inplace=True),
            nn.Conv3d(out_channels, out_channels, kernel_size=3, padding=1, bias=True),
            nn.ReLU(inplace=True),
        )

    def forward(self, x: Tensor) -> Tensor:
        return self.block(x)


class FaultSeg3D(nn.Module):
    """Simplified 3D U-Net from the official FaultSeg3D repository."""

    def __init__(self) -> None:
        super().__init__()
        self.enc1 = DoubleConv(1, 16)
        self.enc2 = DoubleConv(16, 32)
        self.enc3 = DoubleConv(32, 64)
        self.bottleneck = DoubleConv(64, 128)
        self.pool = nn.MaxPool3d(kernel_size=2, stride=2)
        self.up = nn.Upsample(scale_factor=2, mode="nearest")
        self.dec3 = DoubleConv(128 + 64, 64)
        self.dec2 = DoubleConv(64 + 32, 32)
        self.dec1 = DoubleConv(32 + 16, 16)
        self.output = nn.Conv3d(16, 1, kernel_size=1, bias=True)

    def forward(self, x: Tensor) -> Tensor:
        e1 = self.enc1(x)
        e2 = self.enc2(self.pool(e1))
        e3 = self.enc3(self.pool(e2))
        b = self.bottleneck(self.pool(e3))
        d3 = self.dec3(torch.cat((self.up(b), e3), dim=1))
        d2 = self.dec2(torch.cat((self.up(d3), e2), dim=1))
        d1 = self.dec1(torch.cat((self.up(d2), e1), dim=1))
        return self.output(d1)


def count_parameters(model: nn.Module) -> int:
    return sum(parameter.numel() for parameter in model.parameters() if parameter.requires_grad)


def read_manifest(path: Path) -> list[str]:
    if not path.is_file():
        raise FileNotFoundError(f"Missing manifest: {path}")
    names = [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not names:
        raise RuntimeError(f"Empty manifest: {path}")
    if len(names) != len(set(names)):
        raise RuntimeError(f"Duplicate IDs in manifest: {path}")
    return names


class FaultSegDataset(Dataset[tuple[Tensor, Tensor, str]]):
    def __init__(
        self,
        split_root: Path,
        manifest: Path,
        include_fixed_flip: bool,
    ) -> None:
        self.split_root = split_root
        self.names = read_manifest(manifest)
        self.samples: list[tuple[str, bool]] = []
        for name in self.names:
            self.samples.append((name, False))
            if include_fixed_flip:
                self.samples.append((name, True))

        expected_values = math.prod(VOLUME_SHAPE)
        expected_bytes = expected_values * np.dtype(np.float32).itemsize
        for name in self.names:
            for kind in ("seis", "fault"):
                path = self.split_root / kind / name
                if not path.is_file():
                    raise FileNotFoundError(path)
                if path.stat().st_size != expected_bytes:
                    raise RuntimeError(
                        f"Unexpected size for {path}: {path.stat().st_size}; "
                        f"expected {expected_bytes}"
                    )

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, index: int) -> tuple[Tensor, Tensor, str]:
        name, flipped = self.samples[index]
        seismic_path = self.split_root / "seis" / name
        fault_path = self.split_root / "fault" / name

        seismic = np.fromfile(seismic_path, dtype=np.float32).reshape(VOLUME_SHAPE)
        fault = np.fromfile(fault_path, dtype=np.float32).reshape(VOLUME_SHAPE)
        if not np.isfinite(seismic).all() or not np.isfinite(fault).all():
            raise RuntimeError(f"NaN/Inf in pair {name}")
        if not np.isin(np.unique(fault), (0.0, 1.0)).all():
            raise RuntimeError(f"Non-binary label in {fault_path}")

        # Match the public FaultSeg3D loader: standardize each seismic volume
        # independently, then reverse the axis order for seismic conventions.
        mean = float(seismic.mean(dtype=np.float64))
        std = float(seismic.std(dtype=np.float64))
        if not std > 0.0:
            raise RuntimeError(f"Zero standard deviation in {seismic_path}")
        seismic = (seismic - mean) / std
        seismic = np.transpose(seismic)
        fault = np.transpose(fault)
        if flipped:
            seismic = np.flip(seismic, axis=0)
            fault = np.flip(fault, axis=0)

        seismic = np.ascontiguousarray(seismic[None], dtype=np.float32)
        fault = np.ascontiguousarray(fault[None], dtype=np.float32)
        sample_id = f"{Path(name).stem}{'_flip' if flipped else ''}"
        return torch.from_numpy(seismic), torch.from_numpy(fault), sample_id


def soft_dice_loss(logits: Tensor, target: Tensor, smooth: float = 1.0) -> Tensor:
    probability = torch.sigmoid(logits)
    dims = tuple(range(1, probability.ndim))
    intersection = torch.sum(probability * target, dim=dims)
    denominator = torch.sum(probability, dim=dims) + torch.sum(target, dim=dims)
    return 1.0 - ((2.0 * intersection + smooth) / (denominator + smooth)).mean()


class SegmentationLoss(nn.Module):
    def __init__(self, variant: str, pos_weight: float) -> None:
        super().__init__()
        self.variant = variant
        self.register_buffer("positive_weight", torch.tensor([pos_weight], dtype=torch.float32))

    def forward(self, logits: Tensor, target: Tensor) -> Tensor:
        if self.variant == "b0_bce":
            return nn.functional.binary_cross_entropy_with_logits(logits, target)
        if self.variant == "b1_weighted_dice":
            bce = nn.functional.binary_cross_entropy_with_logits(
                logits, target, pos_weight=self.positive_weight
            )
            dice = soft_dice_loss(logits, target)
            return 0.5 * bce + 0.5 * dice
        raise ValueError(f"Unknown loss variant: {self.variant}")


@dataclass
class Metrics:
    threshold: float
    dice: float
    iou: float
    precision: float
    recall: float
    specificity: float
    balanced_accuracy: float
    accuracy: float
    mcc: float
    pr_auc_approx: float
    roc_auc_approx: float
    tp: int
    fp: int
    fn: int
    tn: int


class ProbabilityHistogram:
    """Streaming binary metrics and approximate curve AUCs without retaining voxels."""

    def __init__(self, bins: int = 2048) -> None:
        self.bins = bins
        self.positive = torch.zeros(bins, dtype=torch.float64)
        self.negative = torch.zeros(bins, dtype=torch.float64)

    @torch.no_grad()
    def update_probabilities(self, probability: Tensor, target: Tensor) -> None:
        probability = probability.detach().reshape(-1)
        target = target.detach().reshape(-1)
        indices = torch.clamp((probability * self.bins).long(), 0, self.bins - 1)
        positive = torch.bincount(
            indices, weights=target.to(torch.float32), minlength=self.bins
        )
        negative = torch.bincount(
            indices, weights=(1.0 - target).to(torch.float32), minlength=self.bins
        )
        self.positive += positive.cpu().to(torch.float64)
        self.negative += negative.cpu().to(torch.float64)

    def _descending_counts(self) -> tuple[Tensor, Tensor, Tensor, Tensor]:
        true_positive = torch.flip(self.positive, dims=(0,)).cumsum(0)
        false_positive = torch.flip(self.negative, dims=(0,)).cumsum(0)
        total_positive = self.positive.sum()
        total_negative = self.negative.sum()
        false_negative = total_positive - true_positive
        true_negative = total_negative - false_positive
        return true_positive, false_positive, false_negative, true_negative

    def best_dice_threshold(self) -> float:
        tp, fp, fn, _ = self._descending_counts()
        dice = (2.0 * tp + 1e-12) / (2.0 * tp + fp + fn + 1e-12)
        reverse_index = int(torch.argmax(dice).item())
        original_bin = self.bins - 1 - reverse_index
        return original_bin / self.bins

    def metrics(self, threshold: float) -> Metrics:
        threshold_bin = min(max(int(threshold * self.bins), 0), self.bins - 1)
        tp = self.positive[threshold_bin:].sum()
        fp = self.negative[threshold_bin:].sum()
        fn = self.positive[:threshold_bin].sum()
        tn = self.negative[:threshold_bin].sum()

        dice = (2.0 * tp) / (2.0 * tp + fp + fn + 1e-12)
        iou = tp / (tp + fp + fn + 1e-12)
        precision = tp / (tp + fp + 1e-12)
        recall = tp / (tp + fn + 1e-12)
        specificity = tn / (tn + fp + 1e-12)
        balanced_accuracy = 0.5 * (recall + specificity)
        accuracy = (tp + tn) / (tp + fp + fn + tn + 1e-12)
        mcc_denominator = torch.sqrt(
            (tp + fp) * (tp + fn) * (tn + fp) * (tn + fn)
        )
        mcc = (
            (tp * tn - fp * fn) / mcc_denominator
            if float(mcc_denominator) > 0.0
            else torch.tensor(0.0, dtype=torch.float64)
        )

        curve_tp, curve_fp, _, _ = self._descending_counts()
        curve_precision = curve_tp / (curve_tp + curve_fp + 1e-12)
        curve_recall = curve_tp / (self.positive.sum() + 1e-12)
        recall_increment = torch.diff(
            torch.cat((torch.zeros(1, dtype=torch.float64), curve_recall))
        )
        pr_auc = torch.sum(recall_increment * curve_precision)
        curve_tpr = curve_recall
        curve_fpr = curve_fp / (self.negative.sum() + 1e-12)
        roc_auc = torch.trapz(
            torch.cat((torch.zeros(1, dtype=torch.float64), curve_tpr)),
            torch.cat((torch.zeros(1, dtype=torch.float64), curve_fpr)),
        )

        return Metrics(
            threshold=float(threshold),
            dice=float(dice),
            iou=float(iou),
            precision=float(precision),
            recall=float(recall),
            specificity=float(specificity),
            balanced_accuracy=float(balanced_accuracy),
            accuracy=float(accuracy),
            mcc=float(mcc),
            pr_auc_approx=float(pr_auc),
            roc_auc_approx=float(roc_auc),
            tp=int(tp),
            fp=int(fp),
            fn=int(fn),
            tn=int(tn),
        )


def structural_distances(
    prediction: np.ndarray,
    target: np.ndarray,
) -> dict[str, float | bool]:
    """Compute paper-aligned 3D fault distances in voxel units.

    Modified Hausdorff is the maximum of the two directed mean nearest-point
    distances. Bidirectional Chamfer is their sum. If exactly one mask is
    empty, both receive the volume diagonal as a finite, explicit penalty.
    """
    try:
        from scipy.ndimage import distance_transform_edt
    except ImportError as error:
        raise RuntimeError(
            "Final structural metrics require SciPy. Install it with: "
            "python -m pip install scipy"
        ) from error

    prediction = np.asarray(prediction, dtype=bool).squeeze()
    target = np.asarray(target, dtype=bool).squeeze()
    if prediction.shape != target.shape:
        raise RuntimeError(
            f"Structural metric shape mismatch: {prediction.shape} != {target.shape}"
        )

    prediction_empty = not bool(prediction.any())
    target_empty = not bool(target.any())
    if prediction_empty and target_empty:
        modified_hausdorff = 0.0
        bidirectional_chamfer = 0.0
    elif prediction_empty or target_empty:
        diagonal = math.sqrt(sum((size - 1) ** 2 for size in prediction.shape))
        modified_hausdorff = diagonal
        bidirectional_chamfer = 2.0 * diagonal
    else:
        prediction_to_target = float(
            distance_transform_edt(~target)[prediction].mean()
        )
        target_to_prediction = float(
            distance_transform_edt(~prediction)[target].mean()
        )
        modified_hausdorff = max(prediction_to_target, target_to_prediction)
        bidirectional_chamfer = prediction_to_target + target_to_prediction

    return {
        "modified_hausdorff_voxels": modified_hausdorff,
        "bidirectional_chamfer_voxels": bidirectional_chamfer,
        "prediction_empty": prediction_empty,
        "target_empty": target_empty,
    }


def summarize_per_volume(rows: list[dict[str, object]]) -> dict[str, dict[str, float]]:
    """Return macro mean/std/median/min/max for numeric per-volume metrics."""
    if not rows:
        return {}
    excluded = {"volume_id", "threshold", "tp", "fp", "fn", "tn"}
    summary: dict[str, dict[str, float]] = {}
    for key in rows[0]:
        if key in excluded or isinstance(rows[0][key], bool):
            continue
        values = np.asarray([float(row[key]) for row in rows], dtype=np.float64)
        summary[key] = {
            "mean": float(values.mean()),
            "std": float(values.std(ddof=0)),
            "median": float(np.median(values)),
            "min": float(values.min()),
            "max": float(values.max()),
        }
    return summary


def make_loader(
    dataset: FaultSegDataset,
    batch_size: int,
    shuffle: bool,
    workers: int,
    seed: int,
    use_cuda: bool,
) -> DataLoader:
    generator = torch.Generator()
    generator.manual_seed(seed)
    return DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        num_workers=workers,
        pin_memory=use_cuda,
        persistent_workers=workers > 0,
        generator=generator,
        drop_last=False,
    )


def autocast_context(enabled: bool):
    if not enabled:
        return nullcontext()
    return torch.autocast(device_type="cuda", dtype=torch.float16)


@torch.no_grad()
def evaluate(
    model: nn.Module,
    loader: DataLoader,
    device: torch.device,
    amp_enabled: bool,
    threshold: float,
    histogram_bins: int,
    save_per_volume: Path | None = None,
    compute_structural: bool = False,
    measure_inference: bool = False,
) -> tuple[Metrics, ProbabilityHistogram, list[dict[str, object]]]:
    model.eval()
    aggregate = ProbabilityHistogram(histogram_bins)
    per_volume_rows: list[dict[str, object]] = []
    for seismic, fault, sample_ids in loader:
        seismic = seismic.to(device, non_blocking=True)
        fault = fault.to(device, non_blocking=True)
        if measure_inference and device.type == "cuda":
            torch.cuda.synchronize()
        inference_started = time.perf_counter()
        with autocast_context(amp_enabled):
            logits = model(seismic)
        if measure_inference and device.type == "cuda":
            torch.cuda.synchronize()
        inference_seconds = time.perf_counter() - inference_started
        probability = torch.sigmoid(logits.float())
        aggregate.update_probabilities(probability, fault)

        if save_per_volume is not None or compute_structural or measure_inference:
            for batch_index, sample_id in enumerate(sample_ids):
                individual = ProbabilityHistogram(histogram_bins)
                individual.update_probabilities(
                    probability[batch_index : batch_index + 1],
                    fault[batch_index : batch_index + 1],
                )
                row = asdict(individual.metrics(threshold))
                row = {"volume_id": sample_id, **row}
                if compute_structural:
                    predicted_mask = (
                        probability[batch_index].detach().cpu().numpy() >= threshold
                    )
                    target_mask = fault[batch_index].detach().cpu().numpy() >= 0.5
                    row.update(structural_distances(predicted_mask, target_mask))
                if measure_inference:
                    row["inference_seconds"] = inference_seconds / len(sample_ids)
                per_volume_rows.append(row)

    metrics = aggregate.metrics(threshold)
    if save_per_volume is not None:
        save_per_volume.parent.mkdir(parents=True, exist_ok=True)
        with save_per_volume.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(per_volume_rows[0]))
            writer.writeheader()
            writer.writerows(per_volume_rows)
    return metrics, aggregate, per_volume_rows


def save_checkpoint(
    path: Path,
    model: nn.Module,
    optimizer: torch.optim.Optimizer,
    epoch: int,
    args: argparse.Namespace,
    metrics: Metrics,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(
        {
            "model": model.state_dict(),
            "optimizer": optimizer.state_dict(),
            "epoch": epoch,
            "args": vars(args),
            "validation_metrics": asdict(metrics),
        },
        path,
    )


def write_history(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def train(args: argparse.Namespace) -> None:
    seed_everything(args.seed)
    use_cuda = torch.cuda.is_available()
    if not use_cuda and not args.allow_cpu:
        raise RuntimeError(
            "CUDA GPU is not available. Attach a GPU, or use --allow-cpu only for a smoke test."
        )
    device = torch.device("cuda" if use_cuda else "cpu")
    amp_enabled = use_cuda and not args.disable_amp
    if use_cuda:
        torch.cuda.reset_peak_memory_stats()

    model = FaultSeg3D().to(device)
    parameters = count_parameters(model)
    if parameters != EXPECTED_PARAMETERS:
        raise RuntimeError(f"Parameter mismatch: {parameters} != {EXPECTED_PARAMETERS}")
    print(f"device={device}; parameters={parameters:,}; amp={amp_enabled}", flush=True)

    data_root = Path(args.data_root)
    manifest_root = Path(args.manifest_root)
    train_manifest = manifest_root / "faultseg3d_train.txt"
    val_manifest = manifest_root / "faultseg3d_val.txt"
    test_manifest = manifest_root / "faultseg3d_test.txt"
    train_ids = set(read_manifest(train_manifest))
    val_ids = set(read_manifest(val_manifest))
    if train_ids & val_ids:
        raise RuntimeError("Train/validation manifest overlap")

    train_dataset = FaultSegDataset(
        data_root / "train", train_manifest, include_fixed_flip=True
    )
    val_dataset = FaultSegDataset(
        data_root / "train", val_manifest, include_fixed_flip=False
    )
    test_dataset = FaultSegDataset(
        data_root / "validation", test_manifest, include_fixed_flip=False
    )
    train_loader = make_loader(
        train_dataset, args.batch_size, True, args.workers, args.seed, use_cuda
    )
    val_loader = make_loader(
        val_dataset, 1, False, args.workers, args.seed, use_cuda
    )
    test_loader = make_loader(
        test_dataset, 1, False, args.workers, args.seed, use_cuda
    )

    criterion = SegmentationLoss(args.loss, args.pos_weight).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=args.learning_rate)
    scaler = torch.cuda.amp.GradScaler(enabled=amp_enabled)
    run_dir = Path(args.run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)
    metadata = {
        **vars(args),
        "device": str(device),
        "cuda_name": torch.cuda.get_device_name(0) if use_cuda else None,
        "torch_version": torch.__version__,
        "parameter_count": parameters,
        "train_original_volumes": len(train_ids),
        "train_samples_with_fixed_flip": len(train_dataset),
        "validation_volumes": len(val_dataset),
        "test_volumes": len(test_dataset),
    }
    (run_dir / "run_config.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True), encoding="utf-8"
    )

    if args.smoke_test:
        seismic, fault, _ = next(iter(train_loader))
        seismic = seismic.to(device)
        fault = fault.to(device)
        optimizer.zero_grad(set_to_none=True)
        with autocast_context(amp_enabled):
            logits = model(seismic)
            loss = criterion(logits, fault)
        scaler.scale(loss).backward()
        scaler.step(optimizer)
        scaler.update()
        peak_gib = (
            torch.cuda.max_memory_allocated() / 1024**3 if use_cuda else float("nan")
        )
        print(
            f"SMOKE PASS: input={tuple(seismic.shape)}, output={tuple(logits.shape)}, "
            f"loss={float(loss):.6f}, peak_cuda_GiB={peak_gib:.3f}",
            flush=True,
        )
        return

    best_dice = -1.0
    history: list[dict[str, object]] = []
    for epoch in range(1, args.epochs + 1):
        started = time.time()
        model.train()
        optimizer.zero_grad(set_to_none=True)
        running_loss = 0.0
        optimizer_steps = 0
        for step, (seismic, fault, _) in enumerate(train_loader, start=1):
            seismic = seismic.to(device, non_blocking=True)
            fault = fault.to(device, non_blocking=True)
            with autocast_context(amp_enabled):
                logits = model(seismic)
                full_loss = criterion(logits, fault)
                loss = full_loss / args.gradient_accumulation
            scaler.scale(loss).backward()
            running_loss += float(full_loss.detach())

            should_step = (
                step % args.gradient_accumulation == 0 or step == len(train_loader)
            )
            if should_step:
                scaler.step(optimizer)
                scaler.update()
                optimizer.zero_grad(set_to_none=True)
                optimizer_steps += 1

        validation, _, _ = evaluate(
            model,
            val_loader,
            device,
            amp_enabled,
            threshold=0.5,
            histogram_bins=args.histogram_bins,
        )
        row: dict[str, object] = {
            "epoch": epoch,
            "train_loss": running_loss / len(train_loader),
            "optimizer_steps": optimizer_steps,
            "seconds": time.time() - started,
            **{f"val_{key}": value for key, value in asdict(validation).items()},
        }
        history.append(row)
        write_history(run_dir / "history.csv", history)
        save_checkpoint(run_dir / "last.pt", model, optimizer, epoch, args, validation)
        if validation.dice > best_dice:
            best_dice = validation.dice
            save_checkpoint(run_dir / "best.pt", model, optimizer, epoch, args, validation)
        print(
            f"epoch={epoch:03d} loss={row['train_loss']:.6f} "
            f"val_dice={validation.dice:.6f} val_iou={validation.iou:.6f} "
            f"val_pr_auc={validation.pr_auc_approx:.6f} "
            f"minutes={row['seconds'] / 60.0:.2f}",
            flush=True,
        )

    best = torch.load(run_dir / "best.pt", map_location=device, weights_only=False)
    model.load_state_dict(best["model"])
    _, validation_histogram, _ = evaluate(
        model,
        val_loader,
        device,
        amp_enabled,
        threshold=0.5,
        histogram_bins=args.histogram_bins,
    )
    selected_threshold = validation_histogram.best_dice_threshold()
    validation_final, _, validation_rows = evaluate(
        model,
        val_loader,
        device,
        amp_enabled,
        threshold=selected_threshold,
        histogram_bins=args.histogram_bins,
        save_per_volume=run_dir / "validation_per_volume.csv",
        compute_structural=True,
        measure_inference=True,
    )
    test_final, _, test_rows = evaluate(
        model,
        test_loader,
        device,
        amp_enabled,
        threshold=selected_threshold,
        histogram_bins=args.histogram_bins,
        save_per_volume=run_dir / "test_per_volume.csv",
        compute_structural=True,
        measure_inference=True,
    )
    result = {
        "best_epoch": int(best["epoch"]),
        "threshold_selected_on_internal_validation": selected_threshold,
        "validation": asdict(validation_final),
        "validation_per_volume_summary": summarize_per_volume(validation_rows),
        "official_test": asdict(test_final),
        "official_test_per_volume_summary": summarize_per_volume(test_rows),
        "efficiency": {
            "parameter_count": parameters,
            "peak_cuda_gib": (
                torch.cuda.max_memory_allocated() / 1024**3
                if use_cuda
                else None
            ),
            "cuda_total_memory_gib": (
                torch.cuda.get_device_properties(0).total_memory / 1024**3
                if use_cuda
                else None
            ),
        },
        "metric_notes": {
            "overlap_scope": "positive fault class",
            "pr_auc_approximation": f"streaming histogram with {args.histogram_bins} bins",
            "roc_auc_approximation": f"streaming histogram with {args.histogram_bins} bins",
            "distance_units": "voxels",
            "modified_hausdorff": "max of the two directed mean nearest-point distances",
            "bidirectional_chamfer": "sum of the two directed mean nearest-point distances",
            "one_empty_mask_policy": "volume diagonal penalty",
            "test_threshold_policy": "selected only on internal validation and frozen for test",
        },
    }
    (run_dir / "final_metrics.json").write_text(
        json.dumps(result, indent=2, sort_keys=True), encoding="utf-8"
    )
    print(json.dumps(result, indent=2), flush=True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--loss", choices=("b0_bce", "b1_weighted_dice"), default="b0_bce"
    )
    parser.add_argument("--data-root", default="data/faultseg3d")
    parser.add_argument("--manifest-root", default="data/manifests")
    parser.add_argument("--run-dir", default="runs/faultseg3d_b0_seed42")
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--gradient-accumulation", type=int, default=2)
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--learning-rate", type=float, default=1e-4)
    parser.add_argument("--pos-weight", type=float, default=DEFAULT_POS_WEIGHT)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--histogram-bins", type=int, default=2048)
    parser.add_argument("--disable-amp", action="store_true")
    parser.add_argument("--allow-cpu", action="store_true")
    parser.add_argument("--smoke-test", action="store_true")
    return parser


if __name__ == "__main__":
    train(build_parser().parse_args())
