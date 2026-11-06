# Thebe Zero-Shot Smoke-Test Diagnostic

- Generated: `2026-10-05T09:19:18`
- Status: **SMOKE TEST FAILED**
- Evaluator exists: `True`
- Evaluator syntax valid: `True`
- Source log: `reports/evaluation/baseline_A_zero_shot_thebe_smoke_20261005_091638.log`
- Log lines: `9`

## Detected error-related lines

```text
Traceback (most recent call last):
    raise RuntimeError(
RuntimeError: Zero seismic standard deviation at (0, 0, 0)
```

## Last 40 non-empty log lines

```text
Traceback (most recent call last):
  File "/shared/home/khavarj/projects/fault_detection/scripts/evaluate_thebe_zero_shot.py", line 765, in <module>
    main()
    ~~~~^^
  File "/shared/home/khavarj/projects/fault_detection/scripts/evaluate_thebe_zero_shot.py", line 449, in main
    raise RuntimeError(
    ...<2 lines>...
    )
RuntimeError: Zero seismic standard deviation at (0, 0, 0)
```

## Complete smoke-test log

```text
Traceback (most recent call last):
  File "/shared/home/khavarj/projects/fault_detection/scripts/evaluate_thebe_zero_shot.py", line 765, in <module>
    main()
    ~~~~^^
  File "/shared/home/khavarj/projects/fault_detection/scripts/evaluate_thebe_zero_shot.py", line 449, in main
    raise RuntimeError(
    ...<2 lines>...
    )
RuntimeError: Zero seismic standard deviation at (0, 0, 0)

```

## Smoke output directories

- `runs/baseline_A_zero_shot_thebe_smoke_20261005_091638`
  - `run_configuration.json` — 1321 bytes
