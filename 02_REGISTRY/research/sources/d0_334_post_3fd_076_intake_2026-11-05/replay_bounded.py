#!/usr/bin/env python3
"""Replay two hash-pinned owner checkers; this is not a sandbox or science acceptance."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

P = Path(__file__).resolve().parent
M = json.loads((P / 'MANIFEST.json').read_text())

def sha(data):
    return hashlib.sha256(data).hexdigest()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-dir', type=Path)
    args = parser.parse_args()
    env = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1', PYTHONDONTWRITEBYTECODE='1')
    if args.output_dir:
        args.output_dir.mkdir(parents=True, exist_ok=True)
    for name, pins in M['checkers'].items():
        outputs = []
        for mode, flags in (('normal', []), ('optimized', ['-O'])):
            checker = P / name
            if sha(checker.read_bytes()) != pins['sha256']:
                raise ValueError('checker mismatch: ' + name)
            proc = subprocess.run([sys.executable, *flags, '-Werror', str(checker)], capture_output=True, env=env)
            if args.output_dir:
                (args.output_dir / (name + '.' + mode + '.json')).write_bytes(proc.stdout)
                (args.output_dir / (name + '.' + mode + '.stderr')).write_bytes(proc.stderr)
            if proc.returncode or proc.stderr:
                raise RuntimeError(f'{name} {mode} failed, code {proc.returncode}, stderr {proc.stderr!r}')
            result = json.loads(proc.stdout)
            if result.get('status', 'PASS') != 'PASS' or result.get('check_count') != pins['check_count'] or len(result.get('checks', [])) != pins['check_count']:
                raise ValueError('result mismatch: ' + name)
            outputs.append(proc.stdout)
            print(name, mode, 'sha256', sha(proc.stdout), 'matches_owner', sha(proc.stdout) == pins['owner_stdout_sha256'])
        if outputs[0] != outputs[1]:
            raise ValueError('normal/optimized mismatch: ' + name)
    print('PASS: pinned owner checker replay; no scientific acceptance implied')

if __name__ == '__main__':
    main()
