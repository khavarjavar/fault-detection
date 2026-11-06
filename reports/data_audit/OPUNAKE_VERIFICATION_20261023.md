# Opunake verification — 23 October 2026

Opunake appears fully downloaded and passes the structural checks below. Exact equality to the authors' input is unconfirmed.

## Local download evidence

- File: `data/raw/nz_pretraining/opunake/OPUNAKE-3D-PR3461-T-PSTM.sgy`.
- Exact size: **10,377,743,896 bytes** = 10.377743896 decimal GB = 9.665027164 GiB. The saved portal page displays 9.67 GB; that agrees numerically when using GiB but is only rounded size evidence.
- A complete read of all bytes produced SHA-256 `931bbbb5f2ec50f3eb6f8d65dd1352c982ef842ed103f7427af1ea73c43364ba`.
- All **1,662,034 trace headers** were checked: trace sequences in both byte 1 and byte 5 run continuously from 1 through 1,662,034; every trace declares **1,501 samples** at **4,000 microseconds**.
- Exact file accounting: `3,600 + 1,662,034 × (240 + 1,501 × 4) = 10,377,743,896` bytes. No partial final trace or trailing bytes.
- The time axis is 0–6,000 ms in 4 ms steps; SEG-Y format code 1 is IBM floating point.
- Across 128 evenly spaced traces including the first and last, all 192,128 sampled amplitude values are finite. This is a sample, not an exhaustive amplitude-quality check.
- The file modification time remained unchanged between the full hash and the final structural check. No active `.part` data file was present. Old HTML challenge/rejected artifacts remain separate.

## Identity and paper match

The embedded EBCDIC header explicitly says `DATA-SET : FINAL STACK (OPUNAKE)`, `AREA : TARANAKI BASIN (NEW ZEALAND)`, and `CLIENT : POGO PRODUCTION COMPANY`. It lists the processing sequence including pre-stack time migration and stacking. The saved successful HTTP response named the download `opunake-3d-pr3461-t-pstm_pstm_3d_0.sgy`.

The [fault-segmentation paper](https://www.nature.com/articles/s41598-026-54829-x) identifies Kerry-3D, Opunake-3D, and Kahu-3D as its post-stack pretraining surveys, and refers to the [denoising paper](https://link.springer.com/article/10.1007/s13369-025-10974-5) for further details. The available paper/repository evidence does not establish the authors' exact filename, file checksum, or crop bounds. Therefore survey identity and the final-stack product are strongly supported; byte-for-byte equality and identical preprocessing/crops are unconfirmed.

The portal mapping is [Opunake PR3461](https://geodata.nzpam.govt.nz/survey/78683ccd-4fb8-5eff-98fe-e5b04358450d), processed PSTM resource `8ecd25f5-522f-59da-bcef-6c4f9d6d03c3`. The historical public final-stack filename is `OPUNAKE3D-PR3461-FS.3D.Final_Stack.sgy`; an exact-byte equivalence to that legacy object has not been demonstrated.

## Limits on certainty

The saved final HTTP response has no exact Content-Length or reference checksum. Fresh catalogue API and historical S3 requests returned 403. The saved delivery endpoint rejected HEAD with 405 and the bounded GET returned 404. These checks could not independently establish the complete source-object size. A syntactically complete file could still omit whole traces at the end; only an authoritative expected byte count/trace count or matching source checksum would exclude that possibility.

The measured footprint spans 765 inlines (1987–2751) and 2,233 crosslines (2038–6502, step 2), with 46,211 absent bins in its bounding rectangle and no duplicate inline/crossline pairs. The 300 nonstandard within-inline steps and nonrectangular footprint require survey-specific interpretation; they alone do not establish truncation.

Geometry must be read as 4-byte big-endian integers at bytes 197 and 201, as documented in the embedded header. Bytes 189/193 hold coordinates. `segyio.attributes(201)` applies the standard 2-byte scalar width and incorrectly returns zero; the final audit uses raw 4-byte parsing.

The local SHA-256 makes this copy reproducibly identifiable. It is not evidence of equality to the paper without an author/reference checksum. Exact version confirmation requires the authors' hash or exact source-product identification and crop/preprocessing details.

Machine-readable evidence: `opunake_verification_20261023.json` and `opunake_remote_checks_20261023.json`.
