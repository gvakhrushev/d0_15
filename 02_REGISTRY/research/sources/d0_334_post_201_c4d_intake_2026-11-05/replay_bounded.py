#!/usr/bin/env python3
"""Run pinned owner checker in scratch; output comparison, no stored receipt mutation."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

P = Path(__file__).resolve().parent
M = json.loads((P / 'MANIFEST.json').read_text())

def digest(x):
    return hashlib.sha256(x).hexdigest()

def main():
    with tempfile.TemporaryDirectory(prefix='d0-7fh-replay-') as tmp:
        target = Path(tmp) / M['original_uniform_source_path']
        target.parent.mkdir(parents=True)
        source = (P / 'original_uniform_source.py').read_bytes()
        if digest(source) != M['original_uniform_source_sha256']:
            raise ValueError('constructor source mismatch')
        target.write_bytes(source)
        env = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1')
        outputs = []
        for opt in ([], ['-O']):
            checker = P / 'check_transport.py'
            if digest(checker.read_bytes()) != M['checker_sha256']:
                raise ValueError('checker source mismatch')
            proc = subprocess.run([sys.executable, *opt, '-Werror', str(checker), '--repo', tmp],
                                  capture_output=True, env=env)
            if proc.returncode:
                sys.stderr.buffer.write(proc.stderr)
                raise SystemExit(proc.returncode)
            if proc.stderr:
                raise ValueError('checker produced stderr')
            parsed = json.loads(proc.stdout)
            if parsed['check_count'] != 65 or parsed['check_counts_by_kind'] != M['owner_reported_check_counts']:
                raise ValueError('unexpected check classification')
            outputs.append(proc.stdout)
            print('mode', 'optimized' if opt else 'normal', 'sha256', digest(proc.stdout), 'stderr bytes', len(proc.stderr), 'environment', parsed['environment'])
        if outputs[0] != outputs[1]:
            raise ValueError('normal and optimized receipts differ')
        print('PASS: 65 scoped checks; nominal numeric results are not interval certificates')

if __name__ == '__main__':
    main()
