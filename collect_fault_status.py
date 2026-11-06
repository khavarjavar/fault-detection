from pathlib import Path
from datetime import datetime, timezone
import csv, hashlib, io, json, os, shutil, subprocess, zipfile

# Read saved evidence only. Never import a trainer or load tensor/data files.

root = Path.cwd().resolve()
if not (root / 'runs').is_dir():
    raise SystemExit('Run this command from your fault_detection project (runs/ missing).')
stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
out = root / 'reports/evaluation' / f'fault_status_refresh_{stamp}.zip'
out.parent.mkdir(parents=True, exist_ok=True)
extensions = {'.json', '.jsonl', '.csv', '.tsv', '.md', '.txt', '.log',
              '.out', '.err', '.yaml', '.yml', '.toml', '.ini', '.cfg', '.py', '.sh'}
prune = {'.git', '__pycache__', 'node_modules', '.venv', '.venv_train',
         'wandb', '.cache', 'probability_cache', 'prediction_cache'}
paths = set()
for folder in ('runs', 'reports', 'logs', 'scripts', 'configs', 'data/manifests'):
    for base, dirs, names in os.walk(root / folder, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in prune
                         and not (Path(base) / d).is_symlink())
        paths.update(Path(base) / name for name in names)
for rel in ('external/attention3d_paper/fault-detection-global-attention.py',
            'external/SAM-Med3D/train.py', 'external/SAM-Med3D/README.md'):
    if (root / rel).is_file():
        paths.add(root / rel)

manifest, histories, issues = [], [], []
total, budget, limit, tail = 0, 100 * 1024**2, 4 * 1024**2, 256 * 1024
with zipfile.ZipFile(out, 'x', zipfile.ZIP_DEFLATED) as z:
    for p in sorted(paths):
        if p == out:
            continue
        rel = p.relative_to(root).as_posix()
        try:
            if p.is_symlink() or not p.is_file():
                issues.append(f'Skipped symlink/non-file: {rel}')
                continue
            before = p.stat()
            record = {'path': rel, 'bytes': before.st_size,
                      'mtime_utc': datetime.fromtimestamp(
                          before.st_mtime, timezone.utc).isoformat(),
                      'included': False}
            manifest.append(record)
            if p.suffix.lower() not in extensions:
                continue
            is_log = p.suffix.lower() in {'.log', '.out', '.err', '.jsonl'}
            is_log |= p.suffix.lower() == '.txt' and 'training' in p.parts
            if not is_log and before.st_size > limit:
                issues.append(f'Oversize text skipped: {rel}')
                continue
            with p.open('rb') as f:
                if is_log:
                    f.seek(max(0, before.st_size - tail))
                    content = f.read(tail)
                else:
                    content = f.read(limit + 1)
            if b'\x00' in content:
                issues.append(f'Binary-looking text skipped: {rel}')
                continue
            if not is_log and len(content) > limit:
                issues.append(f'Text grew beyond limit: {rel}')
                continue
            if total + len(content) > budget:
                issues.append(f'Budget exclusion: {rel}')
                continue
            truncated = is_log and before.st_size > tail
            dest = 'files/' + rel + ('.tail.txt' if truncated else '')
            z.writestr(dest, content)
            total += len(content)
            record.update(included=True, archive_path=dest,
                          tail_only=truncated, captured_bytes=len(content),
                          captured_sha256=hashlib.sha256(content).hexdigest())
            after = p.stat()
            if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
                issues.append(f'Changed during capture: {rel}')
            if p.name == 'history.csv':
                rows = list(csv.DictReader(io.StringIO(content.decode('utf-8-sig'))))
                histories.append({'path': rel, 'rows': len(rows),
                                  'columns': list(rows[0]) if rows else [],
                                  'last_row': rows[-1] if rows else {}})
        except Exception as exc:
            issues.append(f'{rel}: {type(exc).__name__}: {exc}')

    def capture(name, command):
        try:
            r = subprocess.run(command, cwd=root, capture_output=True,
                               text=True, timeout=15)
            z.writestr('system/' + name, r.stdout + '\n' + r.stderr)
        except Exception as exc:
            issues.append(f'{name}: {exc}')

    if shutil.which('nvidia-smi'):
        capture('gpu.txt', ['nvidia-smi'])
    if shutil.which('ps'):
        r = subprocess.run(['ps', '-eo', 'pid,ppid,etime,args'],
                           capture_output=True, text=True, timeout=15)
        matches = [line for line in r.stdout.splitlines()
                   if any(t in line.lower() for t in
                          ('fault_detection', 'r100', 'attention3d', 'sammed3d'))]
        z.writestr('system/project_processes.txt', '\n'.join(matches))
    if shutil.which('git'):
        capture('git_head.txt', ['git', 'rev-parse', 'HEAD'])
        capture('git_status.txt', ['git', 'status', '--short'])
        capture('git_script_history.txt', ['git', 'log', '-30', '--date=iso-strict',
                                         '--format=%H %ad %s', '--', 'scripts'])
    for name, value in [('file_inventory.json', manifest),
                        ('history_summary.json', histories),
                        ('collection_issues.json', issues),
                        ('snapshot.json', {'root': str(root), 'started_utc': stamp,
                          'ended_utc': datetime.now(timezone.utc).isoformat(),
                          'captured_bytes': total,
                          'scope': 'Saved text evidence, source, and file metadata. '
                                   'No training, inference, checkpoint loading, '
                                   'or raw seismic/label data access.'})]:
        z.writestr(name, json.dumps(value, indent=2))

for h in histories:
    print(f"{h['path']}: rows={h['rows']}; last epoch={h['last_row'].get('epoch', '?')}")
print(f'\nCreated: {out}\nArchive bytes: {out.stat().st_size:,}')
print(f'Collection issues: {len(issues)}; see collection_issues.json.')
print('This bundle is evidence, not an automatic completed/failed classification.')
print('No raw seismic/labels, checkpoint tensors, or probability arrays were opened.')
print('Existing project files were not modified. Upload this ZIP for review.')
