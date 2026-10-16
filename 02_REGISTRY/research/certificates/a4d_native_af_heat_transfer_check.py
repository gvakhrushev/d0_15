#!/usr/bin/env python3
"""Replay native AF full-heat transfer without rewriting scientific receipts."""
# D0_CI_TIMEOUT_SECONDS=600
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys

SOURCE=Path(__file__).resolve().parents[1]/'sources/d0_native_af_heat_transfer_v7_2026-10-14'
for name,expected in json.loads((SOURCE/'MANIFEST.json').read_text()).items():
    if Path(name).name!=name:raise AssertionError('MANIFEST_PATH')
    if hashlib.sha256((SOURCE/name).read_bytes()).hexdigest()!=expected:
        raise AssertionError('SOURCE_HASH_MISMATCH: '+name)
env={**os.environ,'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1','PYTHONDONTWRITEBYTECODE':'1'}
for filename in ('af_heat_check.py','hostile_check.py','af_heat_numeric.py'):
    result=subprocess.run([sys.executable,'-O',str(SOURCE/filename)],cwd=SOURCE,env=env,timeout=240)
    if result.returncode:raise SystemExit(result.returncode)
print('PASS_V7_NATIVE_AF_FULL_HEAT_SOURCE_TRANSFER_PHYSICAL_GENERATOR_OPEN')
