# CRACKS Expert Evaluation Context

## Evaluation script

```python

--- Lines 1-80 ---
0001: #!/usr/bin/env python3
0002: """Zero-shot evaluation of P1 on the 40 CRACKS expert-labelled sections."""
0003: 
0004: from __future__ import annotations
0005: 
0006: import argparse
0007: import csv
0008: import json
0009: import re
0010: import time
0011: from dataclasses import asdict
0012: from pathlib import Path
0013: 
0014: import numpy as np
0015: import torch
0016: from PIL import Image
0017: 
0018: import faultseg3d_baseline as baseline
0019: from attention3d_caft import Attention3D
0020: 
0021: 
0022: PATCH = 128
0023: STRIDE = 64
0024: 
0025: 
0026: def section_number(path: Path) -> int:
0027:     match = re.fullmatch(r"section_(\d+)\.png", path.name)
0028:     if match is None:
0029:         raise RuntimeError(f"Unexpected filename: {path}")
0030:     return int(match.group(1))
0031: 
0032: 
0033: def starts(length: int) -> list[int]:
0034:     if length < PATCH:
0035:         raise RuntimeError(f"Image dimension {length} is smaller than {PATCH}")
0036:     values = list(range(0, length - PATCH + 1, STRIDE))
0037:     last = length - PATCH
0038:     if values[-1] != last:
0039:         values.append(last)
0040:     return values
0041: 
0042: 
0043: def update_histogram(
0044:     histogram: baseline.ProbabilityHistogram,
0045:     probability: np.ndarray,
0046:     target: np.ndarray,
0047:     valid: np.ndarray,
0048: ) -> None:
0049:     probability_tensor = torch.from_numpy(
0050:         probability[valid].astype(np.float32, copy=False)
0051:     ).reshape(1, 1, 1, -1)
0052:     target_tensor = torch.from_numpy(
0053:         target[valid].astype(np.float32, copy=False)
0054:     ).reshape(1, 1, 1, -1)
0055:     histogram.update_probabilities(probability_tensor, target_tensor)
0056: 
0057: 
0058: def main() -> None:
0059:     parser = argparse.ArgumentParser(description=__doc__)
0060:     parser.add_argument("--checkpoint", type=Path, required=True)
0061:     parser.add_argument("--threshold-metrics", type=Path, required=True)
0062:     parser.add_argument("--images", type=Path, required=True)
0063:     parser.add_argument("--expert-labels", type=Path, required=True)
0064:     parser.add_argument("--output-dir", type=Path, required=True)
0065:     parser.add_argument("--histogram-bins", type=int, default=2048)
0066:     args = parser.parse_args()
0067: 
0068:     if not torch.cuda.is_available():
0069:         raise RuntimeError("CUDA GPU is required")
0070:     if args.output_dir.exists() and any(args.output_dir.iterdir()):
0071:         raise RuntimeError(f"Output directory is not empty: {args.output_dir}")
0072:     args.output_dir.mkdir(parents=True, exist_ok=True)
0073: 
0074:     image_paths = sorted(args.images.glob("section_*.png"), key=section_number)
0075:     label_paths = sorted(
0076:         args.expert_labels.glob("section_*.png"), key=section_number
0077:     )
0078:     if len(label_paths) != 40:
0079:         raise RuntimeError(f"Expected 40 expert labels, found {len(label_paths)}")
0080: 

--- Lines 100-140 ---
0100:     missing_nominal_sections = [
0101:         number
0102:         for number in range(min(ordered_numbers), max(ordered_numbers) + 1)
0103:         if number not in position
0104:     ]
0105: 
0106:     labels: dict[int, tuple[np.ndarray, np.ndarray]] = {}
0107:     for path in label_paths:
0108:         raw = np.asarray(Image.open(path))
0109:         if raw.ndim != 2:
0110:             raise RuntimeError(f"Expected indexed label PNG, got {raw.shape}: {path}")
0111:         unique = set(int(value) for value in np.unique(raw))
0112:         if not unique <= {0, 1, 2, 3}:
0113:             raise RuntimeError(f"Unexpected label values {sorted(unique)} in {path}")
0114:         if raw.shape != (height, width):
0115:             raise RuntimeError(
0116:                 f"Image/label shape mismatch for {path.name}: "
0117:                 f"{(height, width)} vs {raw.shape}"
0118:             )
0119:         # Strict expert evaluation: 1=certain non-fault, 3=certain fault.
0120:         # Values 0 (unlabelled) and 2 (uncertain fault) are ignored.
0121:         labels[section_number(path)] = (raw == 3, (raw == 1) | (raw == 3))
0122: 
0123:     threshold_document = json.loads(
0124:         args.threshold_metrics.read_text(encoding="utf-8")
0125:     )
0126:     threshold = float(
0127:         threshold_document["threshold_selected_on_internal_validation"]
0128:     )
0129:     checkpoint = torch.load(args.checkpoint, map_location="cpu", weights_only=False)
0130:     model = Attention3D().cuda()
0131:     model.load_state_dict(checkpoint["model"], strict=True)
0132:     model.eval()
0133:     for parameter in model.parameters():
0134:         parameter.requires_grad_(False)
0135: 
0136:     aggregate = baseline.ProbabilityHistogram(args.histogram_bins)
0137:     rows: list[dict[str, object]] = []
0138:     y_starts = starts(height)
0139:     x_starts = starts(width)
0140:     torch.cuda.reset_peak_memory_stats()

--- Lines 170-220 ---
0170:                 model_cube = np.ascontiguousarray(np.transpose(cube))
0171:                 tensor = torch.from_numpy(model_cube[None, None]).cuda()
0172:                 with torch.inference_mode(), torch.autocast(
0173:                     device_type="cuda", dtype=torch.float16
0174:                 ):
0175:                     logits = model(tensor)
0176:                 tile_probability = (
0177:                     torch.sigmoid(logits.float())[0, 0, :, :, PATCH // 2]
0178:                     .cpu()
0179:                     .numpy()
0180:                     .T
0181:                 )
0182:                 probability_sum[
0183:                     y0 : y0 + PATCH, x0 : x0 + PATCH
0184:                 ] += tile_probability
0185:                 probability_count[
0186:                     y0 : y0 + PATCH, x0 : x0 + PATCH
0187:                 ] += 1.0
0188:                 tile_count += 1
0189: 
0190:         if np.any(probability_count == 0):
0191:             raise RuntimeError(f"Incomplete spatial coverage for section {number}")
0192:         probability = probability_sum / probability_count
0193:         target, valid = labels[number]
0194:         if not np.any(valid):
0195:             raise RuntimeError(f"No certain expert pixels in {label_path}")
0196:         individual = baseline.ProbabilityHistogram(args.histogram_bins)
0197:         update_histogram(individual, probability, target, valid)
0198:         update_histogram(aggregate, probability, target, valid)
0199:         metrics = asdict(individual.metrics(threshold))
0200:         row: dict[str, object] = {
0201:             "section": number,
0202:             "valid_pixels": int(np.count_nonzero(valid)),
0203:             "certain_fault_pixels": int(np.count_nonzero(target & valid)),
0204:             **metrics,
0205:         }
0206:         rows.append(row)
0207:         print(
0208:             f"expert_section={label_index:02d}/40 id={number:03d} "
0209:             f"dice={metrics['dice']:.6f} pr_auc={metrics['pr_auc_approx']:.6f}",
0210:             flush=True,
0211:         )
0212: 
0213:     with (args.output_dir / "expert_per_section.csv").open(
0214:         "w", newline="", encoding="utf-8"
0215:     ) as stream:
0216:         writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
0217:         writer.writeheader()
0218:         writer.writerows(rows)
0219: 
0220:     final_metrics = asdict(aggregate.metrics(threshold))

--- Lines 230-263 ---
0230:         "cracks_labels_used_for_threshold": False,
0231:         "input_sections": len(image_paths),
0232:         "missing_nominal_section_numbers": missing_nominal_sections,
0233:         "expert_sections_scored": len(rows),
0234:         "image_shape": [height, width],
0235:         "tiles_inferred": tile_count,
0236:         "label_policy": (
0237:             "score raw 1 as certain non-fault and raw 3 as certain fault; "
0238:             "ignore raw 0 and raw 2"
0239:         ),
0240:         "metrics_scope": "expert-labelled 2D planes only; not dense 3D ground truth",
0241:         "cracks_expert": final_metrics,
0242:         "efficiency": {
0243:             "wall_seconds": time.time() - started,
0244:             "peak_cuda_gib": torch.cuda.max_memory_allocated() / 1024**3,
0245:         },
0246:     }
0247:     (args.output_dir / "final_metrics.json").write_text(
0248:         json.dumps(result, indent=2, sort_keys=True), encoding="utf-8"
0249:     )
0250: 
0251:     print("\n=== CRACKS EXPERT ZERO-SHOT RESULT ===")
0252:     print(f"sections={len(rows)}")
0253:     print(f"threshold={threshold:.6f}")
0254:     print(f"dice={final_metrics['dice']:.6f}")
0255:     print(f"iou={final_metrics['iou']:.6f}")
0256:     print(f"precision={final_metrics['precision']:.6f}")
0257:     print(f"recall={final_metrics['recall']:.6f}")
0258:     print(f"pr_auc={final_metrics['pr_auc_approx']:.6f}")
0259:     print(f"results={args.output_dir / 'final_metrics.json'}")
0260: 
0261: 
0262: if __name__ == "__main__":
0263:     main()
```

## Evaluator help

```text
usage: evaluate_cracks_expert_zero_shot.py [-h] --checkpoint CHECKPOINT
                                           --threshold-metrics THRESHOLD_METRICS
                                           --images IMAGES
                                           --expert-labels EXPERT_LABELS
                                           --output-dir OUTPUT_DIR
                                           [--histogram-bins HISTOGRAM_BINS]

Zero-shot evaluation of P1 on the 40 CRACKS expert-labelled sections.

options:
  -h, --help            show this help message and exit
  --checkpoint CHECKPOINT
  --threshold-metrics THRESHOLD_METRICS
  --images IMAGES
  --expert-labels EXPERT_LABELS
  --output-dir OUTPUT_DIR
  --histogram-bins HISTOGRAM_BINS
```

## Expert-label audit

```text
Expert mask count: 40
section_010.png: value=0, rgb=(0, 0, 0), pixels=146787; value=1, rgb=(255, 127, 14), pixels=27431; value=2, rgb=(44, 160, 44), pixels=2414; value=3, rgb=(31, 119, 180), pixels=2123
section_013.png: value=0, rgb=(0, 0, 0), pixels=156699; value=1, rgb=(255, 127, 14), pixels=17967; value=2, rgb=(44, 160, 44), pixels=2015; value=3, rgb=(31, 119, 180), pixels=2074
section_017.png: value=0, rgb=(0, 0, 0), pixels=134082; value=1, rgb=(255, 127, 14), pixels=38494; value=2, rgb=(44, 160, 44), pixels=4283; value=3, rgb=(31, 119, 180), pixels=1896
section_022.png: value=0, rgb=(0, 0, 0), pixels=154709; value=1, rgb=(255, 127, 14), pixels=19259; value=2, rgb=(44, 160, 44), pixels=2832; value=3, rgb=(31, 119, 180), pixels=1955
section_024.png: value=0, rgb=(0, 0, 0), pixels=154089; value=1, rgb=(255, 127, 14), pixels=19690; value=2, rgb=(44, 160, 44), pixels=2769; value=3, rgb=(31, 119, 180), pixels=2207
section_035.png: value=0, rgb=(0, 0, 0), pixels=146718; value=1, rgb=(255, 127, 14), pixels=26744; value=2, rgb=(44, 160, 44), pixels=3610; value=3, rgb=(31, 119, 180), pixels=1683
section_041.png: value=0, rgb=(0, 0, 0), pixels=151078; value=1, rgb=(255, 127, 14), pixels=22919; value=2, rgb=(44, 160, 44), pixels=3043; value=3, rgb=(31, 119, 180), pixels=1715
section_043.png: value=0, rgb=(0, 0, 0), pixels=152301; value=1, rgb=(255, 127, 14), pixels=21055; value=2, rgb=(44, 160, 44), pixels=3804; value=3, rgb=(31, 119, 180), pixels=1595
section_046.png: value=0, rgb=(0, 0, 0), pixels=149714; value=1, rgb=(255, 127, 14), pixels=22279; value=2, rgb=(44, 160, 44), pixels=5470; value=3, rgb=(31, 119, 180), pixels=1292
section_051.png: value=0, rgb=(0, 0, 0), pixels=150145; value=1, rgb=(255, 127, 14), pixels=25574; value=2, rgb=(44, 160, 44), pixels=1508; value=3, rgb=(31, 119, 180), pixels=1528
section_067.png: value=0, rgb=(0, 0, 0), pixels=141573; value=1, rgb=(255, 127, 14), pixels=33530; value=2, rgb=(44, 160, 44), pixels=1635; value=3, rgb=(31, 119, 180), pixels=2017
section_068.png: value=0, rgb=(0, 0, 0), pixels=158466; value=1, rgb=(255, 127, 14), pixels=16271; value=2, rgb=(44, 160, 44), pixels=2314; value=3, rgb=(31, 119, 180), pixels=1704
section_106.png: value=0, rgb=(0, 0, 0), pixels=142366; value=1, rgb=(255, 127, 14), pixels=31562; value=2, rgb=(44, 160, 44), pixels=3664; value=3, rgb=(31, 119, 180), pixels=1163
section_108.png: value=0, rgb=(0, 0, 0), pixels=141693; value=1, rgb=(255, 127, 14), pixels=32366; value=2, rgb=(44, 160, 44), pixels=3350; value=3, rgb=(31, 119, 180), pixels=1346
section_116.png: value=0, rgb=(0, 0, 0), pixels=144240; value=1, rgb=(255, 127, 14), pixels=29005; value=2, rgb=(44, 160, 44), pixels=4191; value=3, rgb=(31, 119, 180), pixels=1319
section_124.png: value=0, rgb=(0, 0, 0), pixels=136325; value=1, rgb=(255, 127, 14), pixels=37846; value=2, rgb=(44, 160, 44), pixels=3041; value=3, rgb=(31, 119, 180), pixels=1543
section_131.png: value=0, rgb=(0, 0, 0), pixels=147457; value=1, rgb=(255, 127, 14), pixels=27553; value=2, rgb=(44, 160, 44), pixels=3374; value=3, rgb=(31, 119, 180), pixels=371
section_133.png: value=0, rgb=(0, 0, 0), pixels=145780; value=1, rgb=(255, 127, 14), pixels=29357; value=2, rgb=(44, 160, 44), pixels=2500; value=3, rgb=(31, 119, 180), pixels=1118
section_136.png: value=0, rgb=(0, 0, 0), pixels=144720; value=1, rgb=(255, 127, 14), pixels=28253; value=2, rgb=(44, 160, 44), pixels=5782
section_167.png: value=0, rgb=(0, 0, 0), pixels=140053; value=1, rgb=(255, 127, 14), pixels=35242; value=2, rgb=(44, 160, 44), pixels=2717; value=3, rgb=(31, 119, 180), pixels=743
section_168.png: value=0, rgb=(0, 0, 0), pixels=131176; value=1, rgb=(255, 127, 14), pixels=44091; value=2, rgb=(44, 160, 44), pixels=2287; value=3, rgb=(31, 119, 180), pixels=1201
section_178.png: value=0, rgb=(0, 0, 0), pixels=128002; value=1, rgb=(255, 127, 14), pixels=46787; value=2, rgb=(44, 160, 44), pixels=2562; value=3, rgb=(31, 119, 180), pixels=1404
section_193.png: value=0, rgb=(0, 0, 0), pixels=134096; value=1, rgb=(255, 127, 14), pixels=38840; value=2, rgb=(44, 160, 44), pixels=4704; value=3, rgb=(31, 119, 180), pixels=1115
section_196.png: value=0, rgb=(0, 0, 0), pixels=127867; value=1, rgb=(255, 127, 14), pixels=42913; value=2, rgb=(44, 160, 44), pixels=6909; value=3, rgb=(31, 119, 180), pixels=1066
section_197.png: value=0, rgb=(0, 0, 0), pixels=140625; value=1, rgb=(255, 127, 14), pixels=34951; value=2, rgb=(44, 160, 44), pixels=2725; value=3, rgb=(31, 119, 180), pixels=454
section_204.png: value=0, rgb=(0, 0, 0), pixels=150266; value=1, rgb=(255, 127, 14), pixels=22391; value=2, rgb=(44, 160, 44), pixels=6098
section_213.png: value=0, rgb=(0, 0, 0), pixels=141279; value=1, rgb=(255, 127, 14), pixels=31676; value=2, rgb=(44, 160, 44), pixels=5800
section_223.png: value=0, rgb=(0, 0, 0), pixels=138803; value=1, rgb=(255, 127, 14), pixels=33985; value=2, rgb=(44, 160, 44), pixels=5967
section_231.png: value=0, rgb=(0, 0, 0), pixels=142461; value=1, rgb=(255, 127, 14), pixels=32075; value=2, rgb=(44, 160, 44), pixels=4219
section_239.png: value=0, rgb=(0, 0, 0), pixels=127500; value=1, rgb=(44, 160, 44), pixels=2482; value=2, rgb=(255, 127, 14), pixels=48773
section_250.png: value=0, rgb=(0, 0, 0), pixels=141376; value=1, rgb=(255, 127, 14), pixels=32157; value=2, rgb=(44, 160, 44), pixels=5222
section_251.png: value=0, rgb=(0, 0, 0), pixels=142149; value=1, rgb=(255, 127, 14), pixels=33761; value=2, rgb=(44, 160, 44), pixels=2845
section_256.png: value=0, rgb=(0, 0, 0), pixels=139408; value=1, rgb=(255, 127, 14), pixels=33685; value=2, rgb=(44, 160, 44), pixels=5662
section_261.png: value=0, rgb=(0, 0, 0), pixels=132540; value=1, rgb=(255, 127, 14), pixels=42094; value=2, rgb=(44, 160, 44), pixels=4121
section_262.png: value=0, rgb=(0, 0, 0), pixels=145725; value=1, rgb=(255, 127, 14), pixels=30987; value=2, rgb=(44, 160, 44), pixels=2043
section_267.png: value=0, rgb=(0, 0, 0), pixels=142377; value=1, rgb=(255, 127, 14), pixels=33058; value=2, rgb=(44, 160, 44), pixels=3320
section_277.png: value=0, rgb=(0, 0, 0), pixels=143168; value=1, rgb=(255, 127, 14), pixels=31332; value=2, rgb=(44, 160, 44), pixels=4255
section_284.png: value=0, rgb=(0, 0, 0), pixels=135797; value=1, rgb=(255, 127, 14), pixels=39984; value=2, rgb=(44, 160, 44), pixels=2974
section_287.png: value=0, rgb=(0, 0, 0), pixels=136250; value=1, rgb=(255, 127, 14), pixels=37408; value=2, rgb=(44, 160, 44), pixels=5097
section_300.png: value=0, rgb=(0, 0, 0), pixels=131966; value=1, rgb=(255, 127, 14), pixels=43434; value=2, rgb=(44, 160, 44), pixels=3355

Aggregate pixel counts:
value=0: 5691826
value=1: 1230488
value=2: 193254
value=3: 34632
```

## Current evaluator Git diff

```diff
warning: Not a git repository. Use --no-index to compare two paths outside a working tree
usage: git diff --no-index [<options>] <path> <path>

Diff output format options
    -p, --patch           generate patch
    -s, --no-patch        suppress diff output
    -u                    generate patch
    -U, --unified[=<n>]   generate diffs with <n> lines context
    -W, --[no-]function-context
                          generate diffs with <n> lines context
    --raw                 generate the diff in raw format
    --patch-with-raw      synonym for '-p --raw'
    --patch-with-stat     synonym for '-p --stat'
    --numstat             machine friendly --stat
    --shortstat           output only the last line of --stat
    -X, --dirstat[=<param1>,<param2>...]
                          output the distribution of relative amount of changes for each sub-directory
    --cumulative          synonym for --dirstat=cumulative
    --dirstat-by-file[=<param1>,<param2>...]
                          synonym for --dirstat=files,<param1>,<param2>...
    --check               warn if changes introduce conflict markers or whitespace errors
    --summary             condensed summary such as creations, renames and mode changes
    --name-only           show only names of changed files
    --name-status         show only names and status of changed files
    --stat[=<width>[,<name-width>[,<count>]]]
                          generate diffstat
    --stat-width <width>  generate diffstat with a given width
    --stat-name-width <width>
                          generate diffstat with a given name width
    --stat-graph-width <width>
                          generate diffstat with a given graph width
    --stat-count <count>  generate diffstat with limited lines
    --[no-]compact-summary
                          generate compact summary in diffstat
    --binary              output a binary diff that can be applied
    --[no-]full-index     show full pre- and post-image object names on the "index" lines
    --[no-]color[=<when>] show colored diff
    --ws-error-highlight <kind>
                          highlight whitespace errors in the 'context', 'old' or 'new' lines in the diff
    -z                    do not munge pathnames and use NULs as output field terminators in --raw or --numstat
    --[no-]abbrev[=<n>]   use <n> digits to display object names
    --src-prefix <prefix> show the given source prefix instead of "a/"
    --dst-prefix <prefix> show the given destination prefix instead of "b/"
    --line-prefix <prefix>
                          prepend an additional prefix to every line of output
    --no-prefix           do not show any source or destination prefix
    --default-prefix      use default prefixes a/ and b/
    --inter-hunk-context <n>
                          show context between diff hunks up to the specified number of lines
    --output-indicator-new <char>
                          specify the character to indicate a new line instead of '+'
    --output-indicator-old <char>
                          specify the character to indicate an old line instead of '-'
    --output-indicator-context <char>
                          specify the character to indicate a context instead of ' '

Diff rename options
    -B, --break-rewrites[=<n>[/<m>]]
                          break complete rewrite changes into pairs of delete and create
    -M, --find-renames[=<n>]
                          detect renames
    -D, --irreversible-delete
                          omit the preimage for deletes
    -C, --find-copies[=<n>]
                          detect copies
    --[no-]find-copies-harder
                          use unmodified files as source to find copies
    --no-renames          disable rename detection
    --[no-]rename-empty   use empty blobs as rename source
    --[no-]follow         continue listing the history of a file beyond renames
    -l <n>                prevent rename/copy detection if the number of rename/copy targets exceeds given limit

Diff algorithm options
    --minimal             produce the smallest possible diff
    -w, --ignore-all-space
                          ignore whitespace when comparing lines
    -b, --ignore-space-change
                          ignore changes in amount of whitespace
    --ignore-space-at-eol ignore changes in whitespace at EOL
    --ignore-cr-at-eol    ignore carrier-return at the end of line
    --ignore-blank-lines  ignore changes whose lines are all blank
    -I, --[no-]ignore-matching-lines <regex>
                          ignore changes whose all lines match <regex>
    --[no-]indent-heuristic
                          heuristic to shift diff hunk boundaries for easy reading
    --patience            generate diff using the "patience diff" algorithm
    --histogram           generate diff using the "histogram diff" algorithm
    --diff-algorithm <algorithm>
                          choose a diff algorithm
    --anchored <text>     generate diff using the "anchored diff" algorithm
    --word-diff[=<mode>]  show word diff, using <mode> to delimit changed words
    --word-diff-regex <regex>
                          use <regex> to decide what a word is
    --color-words[=<regex>]
                          equivalent to --word-diff=color --word-diff-regex=<regex>
    --[no-]color-moved[=<mode>]
                          moved lines of code are colored differently
    --[no-]color-moved-ws <mode>
                          how white spaces are ignored in --color-moved

Other diff options
    --[no-]relative[=<prefix>]
                          when run from subdir, exclude changes outside and show relative paths
    -a, --[no-]text       treat all files as text
    -R                    swap two inputs, reverse the diff
    --[no-]exit-code      exit with 1 if there were differences, 0 otherwise
    --[no-]quiet          disable all output of the program
    --[no-]ext-diff       allow an external diff helper to be executed
    --[no-]textconv       run external text conversion filters when comparing binary files
    --ignore-submodules[=<when>]
                          ignore changes to submodules in the diff generation
    --submodule[=<format>]
                          specify how differences in submodules are shown
    --ita-invisible-in-index
                          hide 'git add -N' entries from the index
    --ita-visible-in-index
                          treat 'git add -N' entries as real in the index
    -S <string>           look for differences that change the number of occurrences of the specified string
    -G <regex>            look for differences that change the number of occurrences of the specified regex
    --pickaxe-all         show all changes in the changeset with -S or -G
    --pickaxe-regex       treat <string> in -S as extended POSIX regular expression
    -O <file>             control the order in which files appear in the output
    --rotate-to <path>    show the change in the specified path first
    --skip-to <path>      skip the output to the specified path
    --find-object <object-id>
                          look for differences that change the number of occurrences of the specified object
    --diff-filter [(A|C|D|M|R|T|U|X|B)...[*]]
                          select files by diff type
    --output <file>       output to a specific file
```

## Existing result: reports/evaluation/p1_cracks_expert_seed42_20261009_134425/expert_per_section.csv

```text
section,valid_pixels,certain_fault_pixels,threshold,dice,iou,precision,recall,specificity,balanced_accuracy,accuracy,mcc,pr_auc_approx,roc_auc_approx,tp,fp,fn,tn
10,29554,2123,0.98095703125,0.12101255402346159,0.06440306681270536,0.10745614035087715,0.13848327837965138,0.9109766322773505,0.524729955328501,0.8554848751438046,0.04406338985389873,0.08223862288780126,0.5564346669817521,294,2442,1829,24989
13,20041,2074,0.98095703125,0.08381351492928232,0.043739748496446136,0.091743119266055,0.07714561234329795,0.9118383703456336,0.4944919913444658,0.8254578114864528,-0.011904292388762729,0.10422624138457572,0.5234410117251818,160,1584,1914,16383
17,40390,1896,0.98095703125,0.08606975321231897,0.044970161977834607,0.07016960425673427,0.11128691983122357,0.927365303683691,0.5193261117574572,0.8890566972022778,0.031144859809229715,0.051910900816104194,0.5357631286831043,211,2796,1685,35698
22,21214,1955,0.98095703125,0.09636517328825019,0.05062166962699821,0.10727728983688826,0.08746803069053705,0.9261124668985928,0.5067902487945649,0.848826246818139,0.014900892108557974,0.0979138429255112,0.539498920954882,171,1423,1784,17836
24,21897,2207,0.98095703125,0.10554870530209616,0.05571465764123925,0.11580086580086574,0.09696420480289983,0.9170137125444388,0.5069889586736693,0.83436087135224,0.01513802267449395,0.10807966979019548,0.5459105256993132,214,1634,1993,18056
35,28427,1683,0.98095703125,0.09370955216153247,0.04915806626833242,0.08302752293577978,0.10754604872251926,0.9252542626383488,0.516400155680434,0.8768424385267527,0.029091433617111244,0.06553092997097516,0.5460197179516297,181,1999,1502,24745
41,24634,1715,0.98095703125,0.09299781181619254,0.04876649454962707,0.08758371973209682,0.09912536443148683,0.9227278677080152,0.510926616069751,0.8653892993423723,0.020643667211710414,0.076127334038318,0.5465323626100129,170,1771,1545,21148
43,22650,1595,0.98095703125,0.10387374461979912,0.05478208232445519,0.09576719576719572,0.11347962382445134,0.9188316314414628,0.5161556276329571,0.8621192052980132,0.029892842934842963,0.07593753469442042,0.5371891351878084,181,1709,1414,19346
46,23571,1292,0.98095703125,0.07204525156296515,0.03736874613959233,0.05853894533139813,0.09365325077399374,0.9126531711477176,0.5031532109608556,0.8677612320224004,0.005074955784099461,0.056590787313025956,0.5211718868662081,121,1946,1171,20333
51,27102,1528,0.98095703125,0.0774889651790093,0.04030612244897958,0.06196078431372547,0.10340314136125649,0.906467506060843,0.5049353237110498,0.8611910560106265,0.007798177546890894,0.05944640764820462,0.5360854313752063,158,2392,1370,23182
67,35547,2017,0.98095703125,0.11060668592653733,0.058540847531673205,0.0947331212442559,0.13287059990084277,0.923620638234417,0.5282456190676299,0.878752074717979,0.04828819495201961,0.06469200823382937,0.542177415026258,268,2561,1749,30969
68,17975,1704,0.98095703125,0.13100704009794914,0.07009498853586633,0.13691618682021744,0.12558685446009382,0.9170917583430642,0.521339306401579,0.8420584144645341,0.044370259588243824,0.10635951017412701,0.5538243932074198,214,1349,1490,14922
106,32725,1163,0.98095703125,0.10473946059177792,0.05526388505111908,0.07530120481927709,0.17196904557179693,0.9221849058994994,0.5470769757356482,0.8955233002291826,0.06383180693661261,0.045242845467439986,0.5666025891906209,200,2456,963,29106
108,33712,1346,0.98095703125,0.09614924659172444,0.05050251256281406,0.07089947089947088,0.14933135215453183,0.9186183031576346,0.5339748276560832,0.8879034171808258,0.04793582678360573,0.0478592765371535,0.5573059419112324,201,2634,1145,29732
116,30324,1319,0.98095703125,0.10528834649437663,0.05556958827986864,0.0769230769230769,0.16679302501895363,0.9089812101361834,0.5378871175775685,0.8766983247592666,0.05288292670089046,0.05253557216297332,0.5614389900881115,220,2640,1099,26365
124,39389,1543,0.98095703125,0.08729668519662341,0.0456404736275565,0.06397103198551597,0.13739468567725202,0.9180362521798869,0.5277154689285695,0.8874558886998908,0.03874054805191449,0.04481277887041247,0.55019191429989,212,3102,1331,34744
131,27924,371,0.98095703125,0.052839116719242886,0.02713649250708788,0.030946882217090056,0.18059299191374614,0.9238558414691685,0.5522244166914574,0.9139808050422575,0.04471791484568979,0.017104418596169967,0.5536499466893635,67,2098,304,25455
133,30475,1118,0.98095703125,0.1080478975215817,0.05710921401236384,0.07844723008491708,0.17352415026833617,0.9223694519194741,0.5479468010939051,0.8948974569319114,0.0660176084168169,0.046555169381916076,0.5652115195560319,194,2279,924,27078
136,28253,0,0.98095703125,0.0,0.0,0.0,0.0,0.9232293915690369,0.46161469578451847,0.9232293915690369,0.0,0.0,0.0,0,2169,0,26084
167,35985,743,0.98095703125,0.039585296889726666,0.020192307692307686,0.023993144815766917,0.11305518169582757,0.903041825095057,0.5080485033954423,0.8867305821870224,0.007723941952621484,0.021749611241140165,0.5246589377060874,84,3417,659,31825
168,45292,1201,0.98095703125,0.05388397246804325,0.027687954729183503,0.035272914521112246,0.11407160699417143,0.9150166700687216,0.5145441385314465,0.8937781506667845,0.016691014651939853,0.02798435697847364,0.5150910356072105,137,3747,1064,40344
178,48191,1404,0.98095703125,0.04486839780957427,0.02294904228406216,0.029833215879727502,0.0904558404558404,0.9117276166456494,0.5010917285507449,0.8878006266730303,0.001294012939755389,0.029888778256111637,0.5233573614240249,127,4130,1277,42657
193,39955,1115,0.98095703125,0.04036933648271419,0.020600482138943672,0.02653867871259175,0.08430493273542594,0.9112255406797116,0.4977652367075688,0.8881491678137905,-0.002589918275124023,0.028639804819064765,0.5242051904328665,94,3448,1021,35392
196,43979,1066,0.98095703125,0.0485458123769954,0.02487673688928731,0.03165098374679212,0.10412757973733575,0.9208631417053107,0.5124953607213232,0.9010664180631666,0.014187524294786319,0.026300486165627985,0.5372704532565973,111,3396,955,39517
197,35405,454,0.98095703125,0.0277056277056277,0.014047410008779628,0.015941547658585183,0.1057268722466958,0.9152241709822323,0.5104755216144641,0.9048439485948312,0.008450369820011162,0.013293205093179047,0.509999745395598,48,2963,406,31988
204,22391,0,0.98095703125,0.0,0.0,0.0,0.0,0.9187620025903265,0.45938100129516324,0.9187620025903265,0.0,0.0,0.0,0,1819,0,20572
213,31676,0,0.98095703125,0.0,0.0,0.0,0.0,0.9230332112640485,0.46151660563202423,0.9230332112640485,0.0,0.0,0.0,0,2438,0,29238
223,33985,0,0.98095703125,0.0,0.0,0.0,0.0,0.9195233191113726,0.4597616595556863,0.9195233191113726,0.0,0.0,0.0,0,2735,0,31250
231,32075,0,0.98095703125,0.0,0.0,0.0,0.0,0.92012470771629,0.460062353858145,0.92012470771629,0.0,0.0,0.0,0,2562,0,29513
239,2482,0,0.98095703125,0.0,0.0,0.0,0.0,0.956486704270749,0.4782433521353745,0.956486704270749,0.0,0.0,0.0,0,108,0,2374
250,32157,0,0.98095703125,0.0,0.0,0.0,0.0,0.9168143794508194,0.4584071897254097,0.9168143794508194,0.0,0.0,0.0,0,2675,0,29482
251,33761,0,0.98095703125,0.0,0.0,0.0,0.0,0.9097183140309825,0.45485915701549123,0.9097183140309825,0.0,0.0,0.0,0,3048,0,30713
256,33685,0,0.98095703125,0.0,0.0,0.0,0.0,0.9069318687843254,0.4534659343921627,0.9069318687843254,0.0,0.0,0.0,0,3135,0,30550
261,42094,0,0.98095703125,0.0,0.0,0.0,0.0,0.9143583408561791,0.45717917042808953,0.9143583408561791,0.0,0.0,0.0,0,3605,0,38489
262,30987,0,0.98095703125,0.0,0.0,0.0,0.0,0.9179655984767806,0.4589827992383903,0.9179655984767806,0.0,0.0,0.0,0,2542,0,28445
267,33058,0,0.98095703125,0.0,0.0,0.0,0.0,0.9141508863210116,0.4570754431605058,0.9141508863210116,0.0,0.0,0.0,0,2838,0,30220
277,31332,0,0.98095703125,0.0,0.0,0.0,0.0,0.9154219328482063,0.45771096642410314,0.9154219328482063,0.0,0.0,0.0,0,2650,0,28682
284,39984,0,0.98095703125,0.0,0.0,0.0,0.0,0.9177921168467387,0.45889605842336934,0.9177921168467387,0.0,0.0,0.0,0,3287,0,36697
287,37408,0,0.98095703125,0.0,0.0,0.0,0.0,0.9226636013686912,0.4613318006843456,0.9226636013686912,0.0,0.0,0.0,0,2893,0,34515
300,43434,0,0.98095703125,0.0,0.0,0.0,0.0,0.9255422019615969,0.46277110098079843,0.9255422019615969,0.0,0.0,0.0,0,3234,0,40200
```

## Existing result: reports/evaluation/p1_cracks_expert_seed42_20261009_134425/final_metrics.json

```text
{
  "checkpoint": "runs/p1_attention3d_caft_seed42/best.pt",
  "checkpoint_epoch": 93,
  "cracks_expert": {
    "accuracy": 0.8954660427469331,
    "balanced_accuracy": 0.5169923072917657,
    "dice": 0.05755252130783045,
    "fn": 30594,
    "fp": 101654,
    "iou": 0.029628868702581336,
    "mcc": 0.020040884105310363,
    "pr_auc_approx": 0.030105754298819044,
    "precision": 0.038205351398402906,
    "recall": 0.1165973665973666,
    "roc_auc_approx": 0.5417569783713032,
    "specificity": 0.9173872479861649,
    "threshold": 0.98095703125,
    "tn": 1128834,
    "tp": 4038
  },
  "cracks_labels_used_for_threshold": false,
  "efficiency": {
    "peak_cuda_gib": 1.0148916244506836,
    "wall_seconds": 49.97105884552002
  },
  "experiment": "p1_cracks_expert_zero_shot",
  "expert_sections_scored": 40,
  "image_shape": [
    255,
    701
  ],
  "input_sections": 396,
  "label_policy": "score raw 1 as certain non-fault and raw 3 as certain fault; ignore raw 0 and raw 2",
  "metrics_scope": "expert-labelled 2D planes only; not dense 3D ground truth",
  "missing_nominal_section_numbers": [
    9,
    185,
    249,
    336
  ],
  "status": "complete_40_expert_sections",
  "threshold": 0.98095703125,
  "threshold_source": "runs/p1_attention3d_caft_seed42/final_metrics.json",
  "tiles_inferred": 1200,
  "training_performed": false,
  "weight_updates": 0
}
```

