# Thebe Zero-Patch Audit

- Generated: `2026-10-05T09:23:24`
- Test files: `7`
- Combined shape: `(703, 3174, 1537)`
- Exact first-patch standard deviation: `0`
- Exact first-patch zero fraction: `100.000000%`
- Exact first-patch fault voxels: `0`

## Interpretation

The first evaluator patch is entirely zero, while other sampled Thebe locations contain varying seismic data. This is consistent with an empty, muted, or padded survey region.

## Sampled 128-cube results

| Origin `(x,y,z)` | Std | Zero % | Varying traces % | Fault voxels |
|---|---:|---:|---:|---:|
| `(0,0,0)` | 0 | 100.0000 | 0.0000 | 0 |
| `(0,0,128)` | 0 | 100.0000 | 0.0000 | 0 |
| `(0,0,512)` | 0.062706455 | 81.9149 | 22.9858 | 0 |
| `(0,0,1024)` | 0.05780686 | 26.9805 | 80.2185 | 3748 |
| `(0,512,0)` | 0 | 100.0000 | 0.0000 | 0 |
| `(0,1523,0)` | 0 | 100.0000 | 0.0000 | 0 |
| `(0,1523,704)` | 0.21399832 | 0.0000 | 100.0000 | 12994 |
| `(287,1523,704)` | 0.216121 | 0.0000 | 100.0000 | 4419 |
| `(575,3046,1409)` | 0 | 100.0000 | 0.0000 | 0 |

## Per-file coarse sampling

| File | Shape | Sample std | Sample zero % | Top-128 std | Top-128 zero % |
|---|---|---:|---:|---:|---:|
| `test1.h5` | `(100, 3174, 1537)` | 0.13605884 | 34.7061 | 0 | 100.0000 |
| `test2.h5` | `(100, 3174, 1537)` | 0.13130205 | 31.4327 | 0 | 100.0000 |
| `test3.h5` | `(100, 3174, 1537)` | 0.13641545 | 28.7429 | 0 | 100.0000 |
| `test4.h5` | `(100, 3174, 1537)` | 0.1320557 | 28.5918 | 0 | 100.0000 |
| `test5.h5` | `(100, 3174, 1537)` | 0.13109826 | 33.8449 | 0 | 100.0000 |
| `test6.h5` | `(100, 3174, 1537)` | 0.12857349 | 41.5878 | 0 | 100.0000 |
| `test7.h5` | `(103, 3174, 1537)` | 0.12253118 | 49.7588 | 0 | 100.0000 |

## Decision rule

- If only zero/no-data patches are constant, exclude them using an explicit validity mask and record how many voxels were excluded.
- If valid-looking patches are also constant, inspect preprocessing and axis order before changing the evaluator.
- Do not choose a behavior merely to improve Dice.

Detailed patch statistics: `reports/evaluation/thebe_zero_patch_samples.csv`
