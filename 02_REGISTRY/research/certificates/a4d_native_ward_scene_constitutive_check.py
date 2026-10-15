#!/usr/bin/env python3
"""Replay exact conditional Ward/scene closure; no physical-action promotion."""
# D0_CI_TIMEOUT_SECONDS=180
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[3]
SOURCE=ROOT/'02_REGISTRY/research/sources/d0_ward_scene_constitutive_closure_2026-10-15'
for name,expected in json.loads((SOURCE/'MANIFEST.json').read_text()).items():
    if hashlib.sha256((SOURCE/name).read_bytes()).hexdigest()!=expected:
        raise RuntimeError('SOURCE_MANIFEST_MISMATCH: '+name)
env={**os.environ,'OPENBLAS_NUM_THREADS':'1','PYTHONDONTWRITEBYTECODE':'1'}
for args in (['verify.py'],['-O','verify.py'],['hostile.py']):
    cmd=[sys.executable]+[str(SOURCE/a) if a.endswith('.py') else a for a in args]
    result=subprocess.run(cmd,cwd=SOURCE,env=env,timeout=80)
    if result.returncode:
        raise SystemExit(result.returncode)
print('PASS_WARD_SCENE_SYNTHESIS_PHYSICAL_ACTION_AND_GR_NOT_PROMOTED')
