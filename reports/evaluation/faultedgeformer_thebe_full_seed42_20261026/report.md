# FaultEdgeFormer-inspired frozen Thebe test

- Seed: 42
- Selected checkpoint epoch: 99
- Frozen threshold: 0.245605469 (selected on complete validation)
- Checkpoint SHA-256: `6ffeda98c35580347bf7bf489a79355f02af355f8ebd2b71bd03d31534394243`
- Claim scope: single-seed exploratory architecture-control result

| Metric | Validation | Test |
|---|---:|---:|
| dice | 0.563981 | 0.574603 |
| iou | 0.392739 | 0.403118 |
| precision | 0.559185 | 0.528904 |
| recall | 0.568860 | 0.628947 |
| specificity | 0.987125 | 0.985611 |
| mcc | 0.551374 | 0.564939 |
| balanced_accuracy | 0.777992 | 0.807279 |
| pr_auc_approx | 0.592442 | 0.603953 |

The model was trained on Thebe `train1.h5` through `train9.h5` and selected using `val1.h5` plus `val2.h5`. All seven `test*.h5` files were opened only after checkpoint and threshold freezing. The test threshold was not optimized on test labels.

This is a FaultEdgeFormer-inspired local implementation because author code and several exact architecture details were unavailable. One seed does not estimate seed variance.

## Visual review

- [Validation casebook](validation_casebook.png)
- [Frozen test casebook](test_casebook.png)
- [Metric and precision-recall summary](frozen_metrics_summary.png)
- [Auditable case-selection manifest](visual_manifest.json)

Cases were selected from reference labels rather than predictions. The frozen
test views reuse locations chosen for the earlier R100 review, and the threshold
remains the value selected on complete validation.

Strong primary faults are usually continuous, with visible width and lateral
alignment error. Secondary faults can be missed. One weak fault next to an
irregular no-data boundary has zero section recall. This points first to
weak-fault/context representation and fault-positive sampling, then to boundary
or distance supervision for mask width. Connectivity loss is most relevant
after foreground exists for a fragmented surface.
