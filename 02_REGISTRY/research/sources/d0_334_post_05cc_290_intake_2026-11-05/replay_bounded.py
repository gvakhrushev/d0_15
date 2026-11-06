#!/usr/bin/env python3
"""Re-execute the four pinned bounded checkers in a disposable directory.

This executes the trusted owner Python blocks. It does not run in a sandbox or
establish the research theorem. Requires Python >= 3.10 and SymPy 1.14.0.
"""
from __future__ import annotations
import hashlib
import json
import lzma
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent


def need(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def main() -> None:
    if sys.version_info < (3, 10):
        raise RuntimeError('Python >= 3.10 is required by the pinned owner checkers')
    import sympy
    need(sympy.__version__ == '1.14.0', 'SymPy 1.14.0 is required')
    subprocess.run([sys.executable, str(ROOT / 'verify_intake.py')], check=True)
    manifest = json.loads((ROOT / 'MANIFEST.json').read_text(encoding='utf-8'))
    source = next(x for x in manifest['snapshots'] if x['commit'] == manifest['head'] and
                  x['source_path'] == manifest['changed_paths']['memo'])
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    results = {}
    with tempfile.TemporaryDirectory(prefix='d0-334-bounded-') as temporary:
        tmp = Path(temporary)
        source_path = tmp / source['source_path']
        source_path.parent.mkdir(parents=True, exist_ok=True)
        source_path.write_bytes(lzma.decompress((ROOT / source['snapshot']).read_bytes()))
        for item in manifest['inputs']:
            dest = tmp / item['source_path']
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes((ROOT / item['path']).read_bytes())
        for name, item in manifest['checks'].items():
            outputs = []
            for mode in ('normal', 'optimized'):
                out = tmp / (name + '_' + mode + '.json')
                cmd = [sys.executable, *(['-O'] if mode == 'optimized' else []), '-Werror',
                       str(ROOT / 'checks' / (name + '.py'))]
                if name in ('sr', 'xf'):
                    cmd += ['--root', str(tmp), '--out', str(out)]
                run = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
                need(run.returncode == 0 and not run.stderr,
                     f'{name}/{mode} failed: {run.stderr.decode(errors="replace")}')
                data = out.read_bytes() if name in ('sr', 'xf') else run.stdout
                need(hashlib.sha256(data).hexdigest() == item['owner_receipt_sha256'],
                     f'{name}/{mode} receipt differs from pinned owner')
                outputs.append(data)
            need(outputs[0] == outputs[1], name + ': normal/optimized differ')
            results[name] = {'checks': item['checks'], 'receipt_sha256': item['owner_receipt_sha256']}
    print(json.dumps({'status': 'PASS_BOUNDED_REPLAY', 'checks': results,
                      'python': sys.version.split()[0], 'sympy': sympy.__version__,
                      'scientific_acceptance': False, 'GR_closed': False}, sort_keys=True))


if __name__ == '__main__':
    main()
