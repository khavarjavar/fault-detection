termina#!/usr/bin/env python3
"""Audit and prepare FaultSeg3D, CRACKS, and Thebe without altering raw data."""

from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import os
import re
import shutil
import struct
import zipfile
from pathlib import Path

import numpy as np
from PIL import Image


FAULTSEG_SHAPE = (128, 128, 128)
REPORT_DIR = Path("reports/data_audit")


def sha256_file(path: Path, block_size: int = 8 * 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(block_size):
            digest.update(block)
    return digest.hexdigest()


def natural_key(path: Path):
    return [int(piece) if piece.isdigit() else piece.lower()
            for piece in re.split(r"(\d+)", path.name)]


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise RuntimeError(f"No rows produced for {path}")
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def faultseg_csv(data_root: Path) -> None:
    rows: list[dict] = []
    expected_bytes = int(np.prod(FAULTSEG_SHAPE)) * np.dtype(np.float32).itemsize

    for split in ("train", "validation"):
        seis_dir = data_root / "faultseg3d" / split / "seis"
        fault_dir = data_root / "faultseg3d" / split / "fault"
        seis_files = {p.name: p for p in seis_dir.glob("*.dat")}
        fault_files = {p.name: p for p in fault_dir.glob("*.dat")}
        if seis_files.keys() != fault_files.keys():
            missing_fault = sorted(seis_files.keys() - fault_files.keys())
            missing_seis = sorted(fault_files.keys() - seis_files.keys())
            raise RuntimeError(
                f"{split}: unmatched pairs; missing fault={missing_fault}, "
                f"missing seismic={missing_seis}"
            )

        names = sorted(seis_files, key=lambda name: natural_key(Path(name)))
        for index, name in enumerate(names, start=1):
            seis_path = seis_files[name]
            fault_path = fault_files[name]
            if seis_path.stat().st_size != expected_bytes:
                raise RuntimeError(f"Wrong size: {seis_path}")
            if fault_path.stat().st_size != expected_bytes:
                raise RuntimeError(f"Wrong size: {fault_path}")

            seis = np.fromfile(seis_path, dtype=np.float32).reshape(FAULTSEG_SHAPE)
            fault = np.fromfile(fault_path, dtype=np.float32).reshape(FAULTSEG_SHAPE)
            labels = np.unique(fault)
            if not np.isfinite(seis).all() or not np.isfinite(fault).all():
                raise RuntimeError(f"NaN/Inf found in pair {name}")
            if not np.isin(labels, [0.0, 1.0]).all():
                raise RuntimeError(f"Unexpected labels in {fault_path}: {labels.tolist()}")

            positives = int(np.count_nonzero(fault))
            voxels = int(fault.size)
            rows.append({
                "split": split,
                "volume_id": Path(name).stem,
                "shape": "128x128x128",
                "seismic_dtype": str(seis.dtype),
                "fault_dtype": str(fault.dtype),
                "seismic_bytes": seis_path.stat().st_size,
                "fault_bytes": fault_path.stat().st_size,
                "seismic_min": float(seis.min()),
                "seismic_max": float(seis.max()),
                "seismic_mean": float(seis.mean(dtype=np.float64)),
                "seismic_std": float(seis.std(dtype=np.float64)),
                "fault_positive_voxels": positives,
                "total_voxels": voxels,
                "fault_positive_pct": 100.0 * positives / voxels,
                "fault_labels": ";".join(str(float(x)) for x in labels),
                "finite": True,
                "seismic_sha256": sha256_file(seis_path),
                "fault_sha256": sha256_file(fault_path),
                "seismic_path": str(seis_path),
                "fault_path": str(fault_path),
            })
            if index % 25 == 0 or index == len(names):
                print(f"{split}: audited {index}/{len(names)} pairs", flush=True)

    output = REPORT_DIR / "faultseg3d_volume_statistics.csv"
    write_csv(output, rows)
    print(f"PASS: wrote {len(rows)} rows to {output}")


def cracks_masks(data_root: Path) -> None:
    image_dir = data_root / "cracks" / "images"
    mask_root = data_root / "cracks" / "Fault segmentations"
    output_root = data_root / "processed" / "cracks"
    target_root = output_root / "target"
    valid_root = output_root / "valid"
    rows: list[dict] = []

    image_names = {p.name for p in image_dir.glob("section_*.png")}
    mask_paths = sorted(mask_root.glob("*/section_*.png"), key=natural_key)
    if not mask_paths:
        raise RuntimeError(f"No CRACKS masks found under {mask_root}")

    processed = 0
    skipped = 0
    for index, mask_path in enumerate(mask_paths, start=1):
        annotator = mask_path.parent.name
        image_exists = mask_path.name in image_names
        row = {
            "annotator": annotator,
            "section": mask_path.name,
            "image_exists": image_exists,
            "height": "",
            "width": "",
            "raw_0_unknown": "",
            "raw_1_certain_nonfault": "",
            "raw_2_uncertain_fault": "",
            "raw_3_certain_fault": "",
            "valid_pixels": "",
            "positive_pixels": "",
            "positive_pct_of_valid": "",
            "source_sha256": sha256_file(mask_path),
            "source_path": str(mask_path),
            "target_path": "",
            "valid_path": "",
        }
        if not image_exists:
            skipped += 1
            rows.append(row)
            continue

        mask = np.asarray(Image.open(mask_path))
        if mask.ndim != 2:
            raise RuntimeError(f"Expected indexed 2D mask, got {mask.shape}: {mask_path}")
        labels, counts = np.unique(mask, return_counts=True)
        if not np.isin(labels, [0, 1, 2, 3]).all():
            raise RuntimeError(f"Unexpected mask values {labels.tolist()}: {mask_path}")
        count_map = {int(label): int(count) for label, count in zip(labels, counts)}

        target = np.isin(mask, [2, 3]).astype(np.uint8) * 255
        valid = (mask != 0).astype(np.uint8) * 255
        target_path = target_root / annotator / mask_path.name
        valid_path = valid_root / annotator / mask_path.name
        target_path.parent.mkdir(parents=True, exist_ok=True)
        valid_path.parent.mkdir(parents=True, exist_ok=True)
        Image.fromarray(target).save(target_path)
        Image.fromarray(valid).save(valid_path)

        valid_pixels = int(np.count_nonzero(valid))
        positive_pixels = int(np.count_nonzero(target))
        row.update({
            "height": mask.shape[0],
            "width": mask.shape[1],
            "raw_0_unknown": count_map.get(0, 0),
            "raw_1_certain_nonfault": count_map.get(1, 0),
            "raw_2_uncertain_fault": count_map.get(2, 0),
            "raw_3_certain_fault": count_map.get(3, 0),
            "valid_pixels": valid_pixels,
            "positive_pixels": positive_pixels,
            "positive_pct_of_valid": (
                100.0 * positive_pixels / valid_pixels if valid_pixels else 0.0
            ),
            "target_path": str(target_path),
            "valid_path": str(valid_path),
        })
        rows.append(row)
        processed += 1
        if index % 500 == 0 or index == len(mask_paths):
            print(f"CRACKS: examined {index}/{len(mask_paths)} masks", flush=True)

    output = REPORT_DIR / "cracks_mask_statistics.csv"
    write_csv(output, rows)
    semantics = output_root / "LABEL_SEMANTICS.txt"
    semantics.parent.mkdir(parents=True, exist_ok=True)
    semantics.write_text(
        "Raw 0 = unknown/unannotated (ignore in loss)\n"
        "Raw 1 = certain non-fault (valid target 0)\n"
        "Raw 2 = uncertain fault (valid target 1)\n"
        "Raw 3 = certain fault (valid target 1)\n"
        "Derived target PNG: 0=non-fault/ignored, 255=fault\n"
        "Derived valid PNG: 0=ignore, 255=include in loss\n",
        encoding="utf-8",
    )
    print(
        f"PASS: processed {processed}, skipped {skipped} masks without images; "
        f"wrote {output}"
    )


def read_exact(stream, size: int) -> bytes:
    chunks = []
    remaining = size
    while remaining:
        chunk = stream.read(remaining)
        if not chunk:
            raise EOFError(f"Unexpected end of stream; needed {remaining} more bytes")
        chunks.append(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)


def read_npy_header(stream):
    if read_exact(stream, 6) != b"\x93NUMPY":
        raise ValueError("Invalid NPY magic value")
    major, minor = read_exact(stream, 2)
    if major == 1:
        header_length = struct.unpack("<H", read_exact(stream, 2))[0]
    elif major in (2, 3):
        header_length = struct.unpack("<I", read_exact(stream, 4))[0]
    else:
        raise ValueError(f"Unsupported NPY version {(major, minor)}")
    encoding = "utf-8" if major == 3 else "latin1"
    header = ast.literal_eval(read_exact(stream, header_length).decode(encoding).strip())
    return tuple(header["shape"]), bool(header["fortran_order"]), np.dtype(header["descr"])


def only_npy_member(archive: zipfile.ZipFile) -> str:
    members = [name for name in archive.namelist() if name.endswith(".npy")]
    if len(members) != 1:
        raise RuntimeError(f"Expected one NPY member, found {members}")
    return members[0]


def thebe_h5(data_root: Path, splits: list[str]) -> None:
    try:
        import h5py
    except ImportError as exc:
        raise RuntimeError("h5py is required: python -m pip install h5py") from exc

    source_root = data_root / "thebe"
    output_root = data_root / "processed" / "thebe_h5"
    output_root.mkdir(parents=True, exist_ok=True)
    report_path = REPORT_DIR / "thebe_h5_statistics.csv"
    records: dict[str, dict] = {}
    if report_path.exists():
        with report_path.open(newline="", encoding="utf-8") as stream:
            records = {
                row["output_path"]: row
                for row in csv.DictReader(stream)
                if row.get("output_path")
            }
    converted = 0
    patterns = {"train": "seistrain*.npz", "val": "seisval*.npz", "test": "seistest*.npz"}
    reserve_bytes = 15 * 1024**3

    for split in splits:
        seismic_files = sorted((source_root / "seis").glob(patterns[split]), key=natural_key)
        if not seismic_files:
            raise RuntimeError(f"No Thebe files found for split {split}")
        for seismic_npz in seismic_files:
            suffix = seismic_npz.name[len("seis"):]
            fault_npz = source_root / "fault" / f"fault{suffix}"
            if not fault_npz.exists():
                raise RuntimeError(f"Missing pair for {seismic_npz}: {fault_npz}")
            output_path = output_root / seismic_npz.name.replace("seis", "", 1).replace(".npz", ".h5")
            if output_path.exists():
                output_key = str(output_path)
                if output_key not in records:
                    with h5py.File(output_path, "r") as h5:
                        shape = tuple(h5["seismic"].shape)
                        voxel_count = int(np.prod(shape))
                        positive_count = int(h5.attrs["fault_positive_count"])
                        records[output_key] = {
                            "split": split,
                            "shape": "x".join(str(x) for x in shape),
                            "source_seismic_dtype": str(h5.attrs["source_seismic_dtype"]),
                            "source_fault_dtype": str(h5.attrs["source_fault_dtype"]),
                            "output_seismic_dtype": "float32",
                            "output_fault_dtype": "uint8",
                            "seismic_min": float(h5.attrs["seismic_min"]),
                            "seismic_max": float(h5.attrs["seismic_max"]),
                            "seismic_mean": float(h5.attrs["seismic_mean"]),
                            "seismic_std": float(h5.attrs["seismic_std"]),
                            "fault_positive_count": positive_count,
                            "total_voxels": voxel_count,
                            "fault_positive_pct": 100.0 * positive_count / voxel_count,
                            "source_seismic_sha256": sha256_file(seismic_npz),
                            "source_fault_sha256": sha256_file(fault_npz),
                            "source_seismic_path": str(seismic_npz),
                            "source_fault_path": str(fault_npz),
                            "output_path": output_key,
                            "output_bytes": output_path.stat().st_size,
                        }
                    write_csv(report_path, list(records.values()))
                    print(f"RECOVERED CSV row for existing {output_path}", flush=True)
                else:
                    print(f"SKIP: already exists: {output_path}", flush=True)
                continue

            with zipfile.ZipFile(seismic_npz) as szip, zipfile.ZipFile(fault_npz) as fzip:
                smember = only_npy_member(szip)
                fmember = only_npy_member(fzip)
                with szip.open(smember) as sstream, fzip.open(fmember) as fstream:
                    sshape, sfortran, sdtype = read_npy_header(sstream)
                    fshape, ffortran, fdtype = read_npy_header(fstream)
                    if sshape != fshape or len(sshape) != 3:
                        raise RuntimeError(f"Shape mismatch: {sshape} vs {fshape}")
                    if sfortran or ffortran:
                        raise RuntimeError("Fortran-order Thebe arrays are not supported")

                    voxel_count = int(np.prod(sshape))
                    worst_output = voxel_count * 5  # float32 seismic + uint8 mask
                    free = shutil.disk_usage(output_root).free
                    if free < worst_output + reserve_bytes:
                        raise RuntimeError(
                            f"Insufficient free disk for {output_path}. "
                            f"Free={free / 1024**3:.1f} GiB, worst output="
                            f"{worst_output / 1024**3:.1f} GiB, reserve=15 GiB"
                        )

                    section_shape = sshape[1:]
                    section_values = int(np.prod(section_shape))
                    sbytes = section_values * sdtype.itemsize
                    fbytes = section_values * fdtype.itemsize
                    chunk_shape = (1, min(256, sshape[1]), min(256, sshape[2]))
                    part_path = output_path.with_suffix(".h5.part")

                    total_sum = 0.0
                    total_sumsq = 0.0
                    global_min = np.inf
                    global_max = -np.inf
                    positive_count = 0

                    with h5py.File(part_path, "w") as h5:
                        seis_ds = h5.create_dataset(
                            "seismic", shape=sshape, dtype="f4", chunks=chunk_shape,
                            compression="lzf", shuffle=True
                        )
                        fault_ds = h5.create_dataset(
                            "fault", shape=fshape, dtype="u1", chunks=chunk_shape,
                            compression="gzip", compression_opts=1, shuffle=True
                        )
                        for section_index in range(sshape[0]):
                            seismic = np.frombuffer(
                                read_exact(sstream, sbytes), dtype=sdtype
                            ).reshape(section_shape)
                            fault = np.frombuffer(
                                read_exact(fstream, fbytes), dtype=fdtype
                            ).reshape(section_shape)
                            if not np.isfinite(seismic).all():
                                raise RuntimeError(
                                    f"NaN/Inf in {seismic_npz}, section {section_index}"
                                )
                            labels = np.unique(fault)
                            if not np.isin(labels, [0, 1, False, True]).all():
                                raise RuntimeError(
                                    f"Bad labels {labels.tolist()} in {fault_npz}, "
                                    f"section {section_index}"
                                )

                            seismic64 = seismic.astype(np.float64, copy=False)
                            total_sum += float(np.sum(seismic64, dtype=np.float64))
                            total_sumsq += float(
                                np.einsum("ij,ij->", seismic64, seismic64, optimize=True)
                            )
                            global_min = min(global_min, float(seismic.min()))
                            global_max = max(global_max, float(seismic.max()))
                            positive_count += int(np.count_nonzero(fault))
                            seis_ds[section_index] = seismic.astype(np.float32)
                            fault_ds[section_index] = fault.astype(np.uint8)

                            if (section_index + 1) % 10 == 0 or section_index + 1 == sshape[0]:
                                print(
                                    f"{output_path.name}: {section_index + 1}/{sshape[0]} sections",
                                    flush=True,
                                )

                        if sstream.read(1) or fstream.read(1):
                            raise RuntimeError("Unexpected trailing bytes in NPY data")

                        mean = total_sum / voxel_count
                        variance = max(0.0, total_sumsq / voxel_count - mean * mean)
                        std = variance ** 0.5
                        h5.attrs["source_seismic"] = str(seismic_npz)
                        h5.attrs["source_fault"] = str(fault_npz)
                        h5.attrs["source_seismic_dtype"] = str(sdtype)
                        h5.attrs["source_fault_dtype"] = str(fdtype)
                        h5.attrs["seismic_min"] = global_min
                        h5.attrs["seismic_max"] = global_max
                        h5.attrs["seismic_mean"] = mean
                        h5.attrs["seismic_std"] = std
                        h5.attrs["fault_positive_count"] = positive_count

                    os.replace(part_path, output_path)
                    row = {
                        "split": split,
                        "shape": "x".join(str(x) for x in sshape),
                        "source_seismic_dtype": str(sdtype),
                        "source_fault_dtype": str(fdtype),
                        "output_seismic_dtype": "float32",
                        "output_fault_dtype": "uint8",
                        "seismic_min": global_min,
                        "seismic_max": global_max,
                        "seismic_mean": mean,
                        "seismic_std": std,
                        "fault_positive_count": positive_count,
                        "total_voxels": voxel_count,
                        "fault_positive_pct": 100.0 * positive_count / voxel_count,
                        "source_seismic_sha256": sha256_file(seismic_npz),
                        "source_fault_sha256": sha256_file(fault_npz),
                        "source_seismic_path": str(seismic_npz),
                        "source_fault_path": str(fault_npz),
                        "output_path": str(output_path),
                        "output_bytes": output_path.stat().st_size,
                    }
                    records[str(output_path)] = row
                    write_csv(report_path, list(records.values()))
                    converted += 1
                    print(f"RECORDED: {output_path} and updated {report_path}", flush=True)

    if converted:
        print(f"PASS: converted {converted} new Thebe blocks; updated {report_path}")
    else:
        print("PASS: no new Thebe files required conversion; existing files were verified.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", type=Path, default=Path("data"))
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("faultseg-csv")
    commands.add_parser("cracks-masks")
    thebe_parser = commands.add_parser("thebe-h5")
    thebe_parser.add_argument(
        "--splits", nargs="+", choices=("train", "val", "test"),
        default=("train", "val")
    )
    args = parser.parse_args()

    if args.command == "faultseg-csv":
        faultseg_csv(args.data_root)
    elif args.command == "cracks-masks":
        cracks_masks(args.data_root)
    elif args.command == "thebe-h5":
        thebe_h5(args.data_root, args.splits)


if __name__ == "__main__":
    main()
