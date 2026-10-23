#!/usr/bin/env python3
"""Replay only the three newly reconstructed calculations, with input integrity.

Run from any directory. Requires SymPy 1.14 and mpmath 1.3 (no network).
No historical certificate, expected result, registry or lifecycle is rewritten.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import time


PACKET = Path(__file__).resolve().parent
ROOT = PACKET.parents[3]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def integrity():
    manifest_path = PACKET / 'MANIFEST.json'
    manifest = json.loads(manifest_path.read_text())
    for row in manifest['artifacts']:
        p = ROOT / row['path']
        require(p.is_file(), 'Missing restored artifact: ' + row['path'])
        require(sha(p.read_bytes()) == row['sha256'], 'Changed restored artifact: ' + row['path'])
    intake = json.loads((PACKET / 'INTAKE.json').read_text())
    for row in intake['original_texts']:
        data = (ROOT / row['saved_original']).read_bytes()
        require(len(data) == row['bytes'] and sha(data) == row['sha256'], 'Original supplied text changed')
    source_count = 0
    for rel in ['oriented/SOURCE_PINS.json', 'all_flag/SOURCE_PINS.json',
                'normal_form/SOURCE_PINS.json', 'SOURCE_PINS.json']:
        pins = json.loads((PACKET / rel).read_text())
        revision = pins['repository_head']
        for row in pins['sources']:
            blob = subprocess.check_output(['git', 'rev-parse', revision + ':' + row['path']], cwd=ROOT).decode().strip()
            require(blob == row['git_blob'], 'Pinned Git object mismatch: ' + row['path'])
            data = subprocess.check_output(['git', 'show', revision + ':' + row['path']], cwd=ROOT)
            require(sha(data) == row['sha256'], 'Pinned source bytes mismatch: ' + row['path'])
            source_count += 1
    return {'artifacts': len(manifest['artifacts']), 'source_pin_checks': source_count,
            'manifest_sha256': sha(manifest_path.read_bytes()),
            'originals': len(intake['original_texts'])}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--integrity-only', action='store_true')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = {'status': 'PASS', 'kind': 'new reconstruction replay, not historical receipt',
              'utc': datetime.now(timezone.utc).isoformat(), 'python': platform.python_version(),
              'integrity': integrity(), 'runs': []}
    if not args.integrity_only:
        for rel in ['all_flag/check_reconstructed_allflag.py',
                    'normal_form/check_nonvacuum_normal_form.py',
                    'oriented/check_oriented_complete_price.py']:
            script = PACKET / rel
            start = time.perf_counter()
            run = subprocess.run([sys.executable, str(script)], cwd=ROOT,
                                 capture_output=True, text=True)
            require(run.returncode == 0, 'Calculation failed: ' + rel + '\n' + run.stderr + run.stdout)
            require(not run.stderr.strip(), 'Unexpected diagnostic from ' + rel + ': ' + run.stderr)
            payload = json.loads(run.stdout)
            require(str(payload.get('status', '')).startswith('PASS'), 'No PASS receipt: ' + rel)
            result['runs'].append({'entrypoint': rel, 'checker_sha256': sha(script.read_bytes()),
                                   'elapsed_seconds': time.perf_counter()-start, 'result': payload})
    payload = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.output:
        args.output.write_text(payload)
        print(json.dumps({'status': result['status'], 'output': str(args.output),
                          'runs': len(result['runs']), 'integrity': result['integrity']}))
    else:
        print(payload, end='')


if __name__ == '__main__':
    main()
