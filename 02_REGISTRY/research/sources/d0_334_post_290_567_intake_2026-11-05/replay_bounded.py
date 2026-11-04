#!/usr/bin/env python3
"""Execute the trusted pinned 7ff checker in ordinary and optimized modes.

This is not a sandbox or an acceptance of the scientific source theorem.
Requires the exact SymPy version used by the owner.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
EXPECTED = '9c475bad9680141457ca6c4a519e02716ea1072aac3486cd0c4e6929145c3881'


def main():
    import sympy
    if sympy.__version__ != '1.14.0':
        raise RuntimeError('SymPy 1.14.0 is required')
    subprocess.run([sys.executable, str(ROOT / 'verify_intake.py')], check=True)
    results = []
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    for optimized in (False, True):
        cmd = [sys.executable, *(['-O'] if optimized else []), '-Werror', str(ROOT / 'check_virtual_source.py')]
        cp = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        if cp.returncode or cp.stderr:
            raise RuntimeError('bounded checker failed: ' + cp.stderr.decode(errors='replace'))
        if hashlib.sha256(cp.stdout).hexdigest() != EXPECTED:
            raise RuntimeError('bounded result differs from the owner receipt')
        results.append(cp.stdout)
    if results[0] != results[1]:
        raise RuntimeError('normal and optimized outputs differ')
    print(json.dumps({'status':'PASS_7FF_BOUNDED_REPLAY', 'checks':42,
                      'python':sys.version.split()[0], 'sympy':sympy.__version__,
                      'scientific_promotion':False, 'GR_closed':False}, sort_keys=True))


if __name__ == '__main__':
    main()
