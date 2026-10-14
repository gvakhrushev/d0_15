#!/usr/bin/env python3
"""v9 immutable exact/interval replay and executed hostile programs."""
# D0_CI_TIMEOUT_SECONDS=600
from pathlib import Path
import os
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[3]
SOURCE=ROOT/'02_REGISTRY/research/sources/d0_two_projection_archive_v9_2026-10-14'
ENV={**os.environ,'OPENBLAS_NUM_THREADS':'1','PYTHONDONTWRITEBYTECODE':'1'}
for args in (['verify.py'],['-O','verify.py'],['hostile.py'],['-O','numerical.py']):
    command=[sys.executable]+[str(SOURCE/a) if a.endswith('.py') else a for a in args]
    result=subprocess.run(command,cwd=SOURCE,env=ENV,timeout=180)
    if result.returncode:raise SystemExit(result.returncode)
print('PASS_V9_ACTIVE_COMPILER_WORKSPACE_NOT_PHYSICAL_GR_CLOSURE')
