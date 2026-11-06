#!/usr/bin/env python3
"""Replay pinned owner check in scratch; executing owner code is not sandboxed."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

P = Path(__file__).resolve().parent
M = json.loads((P / 'MANIFEST.json').read_text())


def digest(b):
    return hashlib.sha256(b).hexdigest()


def checked(path, expected, label):
    data = path.read_bytes()
    if digest(data) != expected:
        raise ValueError(label + ' mismatch')
    return data


def main():
    with tempfile.TemporaryDirectory(prefix='d0-7fi-replay-') as tmp:
        root = Path(tmp)
        owner = checked(P / 'original_uniform_source.py', M['original_uniform_source_sha256'], 'constructor')
        prior = checked(P / 'predecessor_checker.py', M['predecessor_checker_sha256'], 'predecessor')
        target = root / M['original_uniform_source_path']
        target.parent.mkdir(parents=True)
        target.write_bytes(owner)
        primary = root / M['predecessor_primary_path']
        primary.parent.mkdir(parents=True, exist_ok=True)
        # Synthetic scratch container, retaining exactly the original 7fh.G1
        # block; owner code checks its own unique marker and pinned block hash.
        envelope = b'#### 7fh.G1. check_transport.py\n\n```python\n' + prior + b'```\n'
        primary.write_bytes(envelope)
        env = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1')
        outputs = []
        for opt in ([], ['-O']):
            checker = P / 'check_born_history.py'
            checked(checker, M['checker_sha256'], 'checker')
            checked(P / 'original_uniform_source.py', M['original_uniform_source_sha256'], 'constructor')
            checked(P / 'predecessor_checker.py', M['predecessor_checker_sha256'], 'predecessor')
            checked(target, M['original_uniform_source_sha256'], 'scratch constructor')
            checked(primary, digest(envelope), 'scratch predecessor container')
            proc = subprocess.run([sys.executable, *opt, '-Werror', str(checker), '--repo', str(root)],
                                  capture_output=True, env=env)
            if proc.returncode:
                sys.stderr.buffer.write(proc.stderr)
                raise SystemExit(proc.returncode)
            if proc.stderr:
                raise ValueError('checker produced stderr')
            result = json.loads(proc.stdout)
            if result['status'] != 'PASS' or result['check_count'] != 65 or result['classifications'] != M['owner_reported_check_counts']:
                raise ValueError('unexpected check classification')
            outputs.append(proc.stdout)
            print('mode', 'optimized' if opt else 'normal', 'sha256', digest(proc.stdout),
                  'stderr bytes', len(proc.stderr), 'environment', result['runtime'])
        if outputs[0] != outputs[1]:
            raise ValueError('normal and optimized receipts differ')
        print('PASS: 65 scoped checks; numerical checks are nominal, not interval certificates')

if __name__ == '__main__':
    main()
