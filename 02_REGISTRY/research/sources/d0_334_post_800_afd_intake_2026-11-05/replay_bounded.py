#!/usr/bin/env python3
"""Run pinned §7fj checker in scratch; never overwrite retained receipts."""
import hashlib
import json
import lzma
import os
from pathlib import Path
import subprocess
import sys
import tempfile

P = Path(__file__).resolve().parent
M = json.loads((P / 'MANIFEST.json').read_text())

def sha(data):
    return hashlib.sha256(data).hexdigest()

def main():
    memo_path = next(x for x in M['changed_blobs'] if x.startswith('02_REGISTRY/'))
    memo = lzma.decompress((P / M['changed_blobs'][memo_path]['snapshot']).read_bytes())
    original = (P / 'original_uniform_source.py').read_bytes()
    if sha(memo) != M['changed_blobs'][memo_path]['head_sha256']:
        raise ValueError('memo snapshot mismatch')
    if sha(original) != M['original_constructor_sha256']:
        raise ValueError('constructor mismatch')
    env = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1')
    with tempfile.TemporaryDirectory(prefix='d0-7fj-replay-') as tmp:
        root = Path(tmp)
        for rel, data in ((memo_path, memo), (M['original_constructor_path'], original)):
            path = root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        outputs = []
        for flags in (['-Werror'], ['-O', '-Werror']):
            checker = P / 'check_clock_price.py'
            if sha(checker.read_bytes()) != M['checker_sha256']:
                raise ValueError('checker mismatch')
            if sha((root / memo_path).read_bytes()) != M['changed_blobs'][memo_path]['head_sha256']:
                raise ValueError('scratch memo mismatch')
            if sha((root / M['original_constructor_path']).read_bytes()) != M['original_constructor_sha256']:
                raise ValueError('scratch constructor mismatch')
            result = subprocess.run([sys.executable, *flags, str(checker), '--repo', tmp],
                                    capture_output=True, env=env)
            if result.returncode:
                sys.stderr.buffer.write(result.stderr)
                raise SystemExit(result.returncode)
            if result.stderr:
                raise ValueError('checker wrote stderr')
            parsed = json.loads(result.stdout)
            if parsed['status'] != 'PASS' or parsed['check_count'] != 90 or parsed['classifications'] != M['owner_counts']:
                raise ValueError('unexpected check classifications')
            outputs.append(result.stdout)
            print('mode', ' '.join(flags), 'sha256', sha(result.stdout), 'runtime', parsed['runtime'])
        if outputs[0] != outputs[1]:
            raise ValueError('normal and optimized receipts differ')
    print('PASS: 90 scoped checks; nominal numerical checks are not interval certificates')

if __name__ == '__main__':
    main()
