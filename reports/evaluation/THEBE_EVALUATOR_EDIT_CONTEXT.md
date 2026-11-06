# Thebe Evaluator Edit Context

- Source: `scripts/evaluate_thebe_zero_shot.py`
- Source lines: `765`
- SHA-256: `25d6b9918c78146afdff48b4fa09db4fa2bf249778f14c827a0393c58a30404e`
- Zero-std check line: `450`

## Required correction

- Preserve raw-volume tiling coverage.
- Create a validity mask from finite, nonzero raw seismic.
- Normalize using valid voxels only.
- Exclude invalid voxels from overlap, threshold and structural metrics.
- Abort if positive labels occur outside the validity mask.
- Record excluded voxels and empty patches.

## Function and class index

```text
0033: def natural_key(path: Path) -> list[object]:
0040: def load_baseline_module(path: Path):
0054: class ConcatenatedThebe:
0146: def summarize_rows(
0187: def write_csv_atomic(path: Path, rows: list[dict[str, Any]]) -> None:
0201: def middle_slices(array: np.ndarray) -> dict[str, np.ndarray]:
0209: def build_parser() -> argparse.ArgumentParser:
0246: def main() -> None:
```

## Relevant symbol references

```text
0007: - takes its threshold from synthetic validation;
0160:         "modified_hausdorff_voxels",
0161:         "bidirectional_chamfer_voxels",
0227:             "runs/baseline_A_synthetic_bce_seed42/final_metrics.json"
0281:     # Explicitly reject accidental train/validation use.
0291:             "threshold_selected_on_internal_validation"
0296:         raise RuntimeError(f"Invalid frozen threshold: {threshold}")
0316:     histogram_bins = int(
0317:         checkpoint_args.get("histogram_bins", 2048)
0375:             "independent z-score on each valid 3D patch, "
0384:             "non-overlapping partition; every valid voxel evaluated once"
0386:         "histogram_bins": histogram_bins,
0394:     aggregate = baseline.ProbabilityHistogram(histogram_bins)
0514:             valid_model_shape = (size_z, size_y, size_x)
0515:             valid_z, valid_y, valid_x = valid_model_shape
0517:             probability_valid = probability[
0518:                 :valid_z, :valid_y, :valid_x
0520:             target_valid = target_tensor[
0521:                 :valid_z, :valid_y, :valid_x
0524:             valid_voxels = (
0525:                 valid_z * valid_y * valid_x
0527:             evaluated_voxels += valid_voxels
0530:                 probability_valid,
0531:                 target_valid,
0534:             individual = baseline.ProbabilityHistogram(
0535:                 histogram_bins
0538:                 probability_valid,
0539:                 target_valid,
0552:                 "valid_voxels": valid_voxels,
0559:                 probability_valid.detach().cpu().numpy()
0562:                 target_valid.detach().cpu().numpy() >= 0.5
0569:                 baseline.structural_distances(
0581:                 seismic_valid = seismic_model[
0582:                     :valid_z, :valid_y, :valid_x
0597:                     ("seismic", seismic_valid),
0625:                     args.output_dir / "test_per_patch.csv",
0643:                 f"Coverage failure: evaluated "
0664:             "Baseline A synthetic validation"
0668:         "official_thebe_test_per_patch_summary": (
0681:             "complete_coverage": complete_evaluation,
0690:             "mean_model_inference_seconds_per_patch": (
0701:             "modified_hausdorff": (
0704:             "bidirectional_chamfer": (
0708:                 "valid-patch diagonal penalty"
0718:         args.output_dir / "final_metrics.json.part"
0729:         args.output_dir / "final_metrics.json"
0733:         args.output_dir / "test_per_patch.csv",
0760:         f"{args.output_dir / 'final_metrics.json'}"
```

## Patch loop, normalization and metric updates

Source lines `350`–`649`:

```python
0350: 
0351:     complete_evaluation = len(coordinates) == full_patch_count
0352: 
0353:     run_configuration = {
0354:         "experiment": "A_to_T0_zero_shot",
0355:         "training_performed": False,
0356:         "weight_updates": 0,
0357:         "checkpoint": str(args.checkpoint),
0358:         "checkpoint_epoch": int(checkpoint.get("epoch", -1)),
0359:         "checkpoint_training_data": checkpoint_args.get(
0360:             "data_root",
0361:             "unknown",
0362:         ),
0363:         "threshold": threshold,
0364:         "threshold_source": str(args.threshold_metrics),
0365:         "threshold_selected_using_thebe": False,
0366:         "data_split": "official Thebe test only",
0367:         "test_files": [str(path) for path in test_files],
0368:         "test_block_count": len(test_files),
0369:         "concatenated_test_shape": list(total_shape),
0370:         "patch_shape": list(volume_shape),
0371:         "patch_count_planned": full_patch_count,
0372:         "patch_count_this_run": len(coordinates),
0373:         "complete_official_test_evaluation": complete_evaluation,
0374:         "normalization": (
0375:             "independent z-score on each valid 3D patch, "
0376:             "matching Baseline A"
0377:         ),
0378:         "axis_transform": "np.transpose, matching Baseline A",
0379:         "edge_policy": (
0380:             "zero-pad normalized inputs to 128^3; "
0381:             "exclude padding from every metric"
0382:         ),
0383:         "overlap_policy": (
0384:             "non-overlapping partition; every valid voxel evaluated once"
0385:         ),
0386:         "histogram_bins": histogram_bins,
0387:     }
0388: 
0389:     (args.output_dir / "run_configuration.json").write_text(
0390:         json.dumps(run_configuration, indent=2, sort_keys=True),
0391:         encoding="utf-8",
0392:     )
0393: 
0394:     aggregate = baseline.ProbabilityHistogram(histogram_bins)
0395:     rows: list[dict[str, Any]] = []
0396:     evaluated_voxels = 0
0397:     total_inference_seconds = 0.0
0398:     saved_examples = 0
0399:     started = time.time()
0400: 
0401:     try:
0402:         for patch_number, (x0, y0, z0) in enumerate(
0403:             coordinates,
0404:             start=1,
0405:         ):
0406:             x1 = min(x0 + patch_size, total_shape[0])
0407:             y1 = min(y0 + patch_size, total_shape[1])
0408:             z1 = min(z0 + patch_size, total_shape[2])
0409: 
0410:             size_x = x1 - x0
0411:             size_y = y1 - y0
0412:             size_z = z1 - z0
0413: 
0414:             seismic_raw = reader.read(
0415:                 "seismic", x0, x1, y0, y1, z0, z1
0416:             ).astype(np.float32, copy=False)
0417:             fault_raw = reader.read(
0418:                 "fault", x0, x1, y0, y1, z0, z1
0419:             ).astype(np.uint8, copy=False)
0420: 
0421:             expected_shape = (size_x, size_y, size_z)
0422:             if seismic_raw.shape != expected_shape:
0423:                 raise RuntimeError(
0424:                     f"Unexpected seismic shape: "
0425:                     f"{seismic_raw.shape} != {expected_shape}"
0426:                 )
0427:             if fault_raw.shape != expected_shape:
0428:                 raise RuntimeError(
0429:                     f"Unexpected fault shape: "
0430:                     f"{fault_raw.shape} != {expected_shape}"
0431:                 )
0432: 
0433:             if not np.isfinite(seismic_raw).all():
0434:                 raise RuntimeError(
0435:                     f"NaN/Inf in patch starting at {(x0, y0, z0)}"
0436:                 )
0437:             if fault_raw.min() < 0 or fault_raw.max() > 1:
0438:                 raise RuntimeError(
0439:                     f"Non-binary fault values at {(x0, y0, z0)}"
0440:                 )
0441: 
0442:             patch_mean = float(
0443:                 seismic_raw.mean(dtype=np.float64)
0444:             )
0445:             patch_std = float(
0446:                 seismic_raw.std(dtype=np.float64)
0447:             )
0448:             if not patch_std > 0.0:
0449:                 raise RuntimeError(
0450:                     f"Zero seismic standard deviation at "
0451:                     f"{(x0, y0, z0)}"
0452:                 )
0453: 
0454:             seismic_normalized = (
0455:                 seismic_raw - patch_mean
0456:             ) / patch_std
0457: 
0458:             seismic_padded = np.zeros(
0459:                 volume_shape,
0460:                 dtype=np.float32,
0461:             )
0462:             fault_padded = np.zeros(
0463:                 volume_shape,
0464:                 dtype=np.float32,
0465:             )
0466: 
0467:             seismic_padded[
0468:                 :size_x, :size_y, :size_z
0469:             ] = seismic_normalized
0470:             fault_padded[
0471:                 :size_x, :size_y, :size_z
0472:             ] = fault_raw
0473: 
0474:             # Match Baseline A axis reversal.
0475:             seismic_model = np.ascontiguousarray(
0476:                 np.transpose(seismic_padded),
0477:                 dtype=np.float32,
0478:             )
0479:             fault_model = np.ascontiguousarray(
0480:                 np.transpose(fault_padded),
0481:                 dtype=np.float32,
0482:             )
0483: 
0484:             model_input = torch.from_numpy(
0485:                 seismic_model[None, None]
0486:             ).to(device)
0487: 
0488:             target_tensor = torch.from_numpy(
0489:                 fault_model
0490:             ).to(device)
0491: 
0492:             torch.cuda.synchronize()
0493:             inference_started = time.perf_counter()
0494: 
0495:             with torch.inference_mode():
0496:                 with torch.autocast(
0497:                     device_type="cuda",
0498:                     dtype=torch.float16,
0499:                 ):
0500:                     logits = model(model_input)
0501: 
0502:                 probability = torch.sigmoid(
0503:                     logits.float()
0504:                 )[0, 0]
0505: 
0506:             torch.cuda.synchronize()
0507:             inference_seconds = (
0508:                 time.perf_counter() - inference_started
0509:             )
0510: 
0511:             total_inference_seconds += inference_seconds
0512: 
0513:             # Dimensions reverse after np.transpose.
0514:             valid_model_shape = (size_z, size_y, size_x)
0515:             valid_z, valid_y, valid_x = valid_model_shape
0516: 
0517:             probability_valid = probability[
0518:                 :valid_z, :valid_y, :valid_x
0519:             ]
0520:             target_valid = target_tensor[
0521:                 :valid_z, :valid_y, :valid_x
0522:             ]
0523: 
0524:             valid_voxels = (
0525:                 valid_z * valid_y * valid_x
0526:             )
0527:             evaluated_voxels += valid_voxels
0528: 
0529:             aggregate.update_probabilities(
0530:                 probability_valid,
0531:                 target_valid,
0532:             )
0533: 
0534:             individual = baseline.ProbabilityHistogram(
0535:                 histogram_bins
0536:             )
0537:             individual.update_probabilities(
0538:                 probability_valid,
0539:                 target_valid,
0540:             )
0541: 
0542:             row: dict[str, Any] = {
0543:                 "patch_id": (
0544:                     f"x{x0:04d}_y{y0:04d}_z{z0:04d}"
0545:                 ),
0546:                 "raw_x_start": x0,
0547:                 "raw_x_stop": x1,
0548:                 "raw_y_start": y0,
0549:                 "raw_y_stop": y1,
0550:                 "raw_z_start": z0,
0551:                 "raw_z_stop": z1,
0552:                 "valid_voxels": valid_voxels,
0553:                 "normalization_mean": patch_mean,
0554:                 "normalization_std": patch_std,
0555:                 **asdict(individual.metrics(threshold)),
0556:             }
0557: 
0558:             probability_numpy = (
0559:                 probability_valid.detach().cpu().numpy()
0560:             )
0561:             target_numpy = (
0562:                 target_valid.detach().cpu().numpy() >= 0.5
0563:             )
0564:             prediction_numpy = (
0565:                 probability_numpy >= threshold
0566:             )
0567: 
0568:             row.update(
0569:                 baseline.structural_distances(
0570:                     prediction_numpy,
0571:                     target_numpy,
0572:                 )
0573:             )
0574:             row["inference_seconds"] = inference_seconds
0575:             rows.append(row)
0576: 
0577:             if (
0578:                 saved_examples < args.save_examples
0579:                 and bool(target_numpy.any())
0580:             ):
0581:                 seismic_valid = seismic_model[
0582:                     :valid_z, :valid_y, :valid_x
0583:                 ]
0584: 
0585:                 arrays: dict[str, np.ndarray] = {
0586:                     "coordinates_raw": np.asarray(
0587:                         [x0, x1, y0, y1, z0, z1],
0588:                         dtype=np.int32,
0589:                     ),
0590:                     "threshold": np.asarray(
0591:                         threshold,
0592:                         dtype=np.float32,
0593:                     ),
0594:                 }
0595: 
0596:                 for prefix, array in (
0597:                     ("seismic", seismic_valid),
0598:                     ("probability", probability_numpy),
0599:                     ("target", target_numpy.astype(np.uint8)),
0600:                     (
0601:                         "prediction",
0602:                         prediction_numpy.astype(np.uint8),
0603:                     ),
0604:                 ):
0605:                     for axis_name, image in middle_slices(
0606:                         array
0607:                     ).items():
0608:                         arrays[
0609:                             f"{prefix}_{axis_name}"
0610:                         ] = image
0611: 
0612:                 np.savez_compressed(
0613:                     example_dir
0614:                     / f"example_{saved_examples + 1:02d}_"
0615:                     f"{row['patch_id']}.npz",
0616:                     **arrays,
0617:                 )
0618:                 saved_examples += 1
0619: 
0620:             if (
0621:                 patch_number % 25 == 0
0622:                 or patch_number == len(coordinates)
0623:             ):
0624:                 write_csv_atomic(
0625:                     args.output_dir / "test_per_patch.csv",
0626:                     rows,
0627:                 )
0628:                 print(
0629:                     f"processed={patch_number}/"
0630:                     f"{len(coordinates)} "
0631:                     f"elapsed_minutes="
0632:                     f"{(time.time() - started) / 60.0:.2f}",
0633:                     flush=True,
0634:                 )
0635: 
0636:     finally:
0637:         reader.close()
0638: 
0639:     if complete_evaluation:
0640:         expected_voxels = int(math.prod(total_shape))
0641:         if evaluated_voxels != expected_voxels:
0642:             raise RuntimeError(
0643:                 f"Coverage failure: evaluated "
0644:                 f"{evaluated_voxels} voxels, "
0645:                 f"expected {expected_voxels}"
0646:             )
0647: 
0648:     aggregate_metrics = asdict(
0649:         aggregate.metrics(threshold)
```

## Final metric and output construction

Source lines `626`–`765`:

```python
0626:                     rows,
0627:                 )
0628:                 print(
0629:                     f"processed={patch_number}/"
0630:                     f"{len(coordinates)} "
0631:                     f"elapsed_minutes="
0632:                     f"{(time.time() - started) / 60.0:.2f}",
0633:                     flush=True,
0634:                 )
0635: 
0636:     finally:
0637:         reader.close()
0638: 
0639:     if complete_evaluation:
0640:         expected_voxels = int(math.prod(total_shape))
0641:         if evaluated_voxels != expected_voxels:
0642:             raise RuntimeError(
0643:                 f"Coverage failure: evaluated "
0644:                 f"{evaluated_voxels} voxels, "
0645:                 f"expected {expected_voxels}"
0646:             )
0647: 
0648:     aggregate_metrics = asdict(
0649:         aggregate.metrics(threshold)
0650:     )
0651:     elapsed_seconds = time.time() - started
0652: 
0653:     final_result = {
0654:         "experiment": "A_to_T0_zero_shot",
0655:         "status": (
0656:             "complete_official_test"
0657:             if complete_evaluation
0658:             else "smoke_test_only"
0659:         ),
0660:         "training_performed": False,
0661:         "weight_updates": 0,
0662:         "threshold": threshold,
0663:         "threshold_source": (
0664:             "Baseline A synthetic validation"
0665:         ),
0666:         "thebe_labels_used_for_threshold": False,
0667:         "official_thebe_test": aggregate_metrics,
0668:         "official_thebe_test_per_patch_summary": (
0669:             summarize_rows(rows)
0670:         ),
0671:         "data": {
0672:             "test_files": [str(path) for path in test_files],
0673:             "test_shape": list(total_shape),
0674:             "patch_shape": list(volume_shape),
0675:             "patches_evaluated": len(rows),
0676:             "full_patch_count": full_patch_count,
0677:             "evaluated_voxels": evaluated_voxels,
0678:             "expected_full_test_voxels": int(
0679:                 math.prod(total_shape)
0680:             ),
0681:             "complete_coverage": complete_evaluation,
0682:             "overlap": False,
0683:             "padding_counted_in_metrics": False,
0684:         },
0685:         "efficiency": {
0686:             "wall_seconds": elapsed_seconds,
0687:             "total_model_inference_seconds": (
0688:                 total_inference_seconds
0689:             ),
0690:             "mean_model_inference_seconds_per_patch": (
0691:                 total_inference_seconds / len(rows)
0692:             ),
0693:             "peak_cuda_gib": (
0694:                 torch.cuda.max_memory_allocated()
0695:                 / 1024**3
0696:             ),
0697:         },
0698:         "prediction_examples_saved": saved_examples,
0699:         "metric_notes": {
0700:             "distance_units": "voxels",
0701:             "modified_hausdorff": (
0702:                 "max of directed mean nearest-point distances"
0703:             ),
0704:             "bidirectional_chamfer": (
0705:                 "sum of directed mean nearest-point distances"
0706:             ),
0707:             "one_empty_mask_policy": (
0708:                 "valid-patch diagonal penalty"
0709:             ),
0710:             "important": (
0711:                 "These results measure zero-shot transfer "
0712:                 "from synthetic FaultSeg3D to real Thebe."
0713:             ),
0714:         },
0715:     }
0716: 
0717:     temporary_json = (
0718:         args.output_dir / "final_metrics.json.part"
0719:     )
0720:     temporary_json.write_text(
0721:         json.dumps(
0722:             final_result,
0723:             indent=2,
0724:             sort_keys=True,
0725:         ),
0726:         encoding="utf-8",
0727:     )
0728:     temporary_json.replace(
0729:         args.output_dir / "final_metrics.json"
0730:     )
0731: 
0732:     write_csv_atomic(
0733:         args.output_dir / "test_per_patch.csv",
0734:         rows,
0735:     )
0736: 
0737:     print("\n=== ZERO-SHOT RESULT ===")
0738:     print(f"status={final_result['status']}")
0739:     print(f"threshold={threshold:.6f}")
0740:     print(
0741:         f"dice={aggregate_metrics['dice']:.6f}"
0742:     )
0743:     print(
0744:         f"iou={aggregate_metrics['iou']:.6f}"
0745:     )
0746:     print(
0747:         f"precision={aggregate_metrics['precision']:.6f}"
0748:     )
0749:     print(
0750:         f"recall={aggregate_metrics['recall']:.6f}"
0751:     )
0752:     print(
0753:         f"mcc={aggregate_metrics['mcc']:.6f}"
0754:     )
0755:     print(
0756:         f"pr_auc={aggregate_metrics['pr_auc_approx']:.6f}"
0757:     )
0758:     print(
0759:         "results="
0760:         f"{args.output_dir / 'final_metrics.json'}"
0761:     )
0762: 
0763: 
0764: if __name__ == "__main__":
0765:     main()
```
