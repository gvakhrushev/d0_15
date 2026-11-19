#!/usr/bin/env python3
"""Immutable v8 algebra, outward intervals and actual hostile programs."""
# D0_CI_TIMEOUT_SECONDS=600
from pathlib import Path
import os
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[3]
SOURCE=ROOT/'02_REGISTRY/research/sources/d0_record_generated_heat_v8_2026-10-14'
ENV={**os.environ,'OPENBLAS_NUM_THREADS':'1','PYTHONDONTWRITEBYTECODE':'1'}
for args in (['verify.py'],['-O','verify.py'],['hostile.py']):
    command=[sys.executable]+[str(SOURCE/a) if a.endswith('.py') else a for a in args]
    result=subprocess.run(command,cwd=SOURCE,env=ENV,timeout=300)
    if result.returncode:raise SystemExit(result.returncode)
print('PASS_V8_RECORD_GENERATED_HEAT_NO_NATIVE_GR_PROMOTION')
