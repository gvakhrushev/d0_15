#!/usr/bin/env python3
"""Pin consumed owners and replay new coherent AF Cost-Info mathematics."""
# D0_CI_TIMEOUT_SECONDS=600
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[3]
SOURCE=ROOT/'02_REGISTRY/research/sources/d0_coherent_af_cost_info_2026-10-14'
PINS={
 '02_REGISTRY/research/A4D_NATIVE_GOLDEN_COST_REFINEMENT.md':'573e2d70c1d7cbefd35670431b1ab9b87624dbdd',
 '02_REGISTRY/research/sources/d0_direct_forcing_attack_2026-10-14/RESULT.md':'d421f20e91c3feb0d636428a1db19233ffb89f5f',
 '01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md':'ecdd31abb52c94e9f2a157a80c7c49a6f5ac31aa',
}
for name,wanted in PINS.items():
    data=(ROOT/name).read_bytes()
    got=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    if got!=wanted:raise RuntimeError('CONSUMED_OWNER_CHANGED: '+name)
for name,wanted in json.loads((SOURCE/'MANIFEST.json').read_text()).items():
    if hashlib.sha256((SOURCE/name).read_bytes()).hexdigest()!=wanted:
        raise RuntimeError('SOURCE_MANIFEST_MISMATCH: '+name)
ENV={**os.environ,'OPENBLAS_NUM_THREADS':'1','PYTHONDONTWRITEBYTECODE':'1'}
for args in (['verify.py'],['-O','verify.py'],['numerical.py'],['hostile.py']):
    cmd=[sys.executable]+[str(SOURCE/a) if a.endswith('.py') else a for a in args]
    result=subprocess.run(cmd,cwd=SOURCE,env=ENV,timeout=180)
    if result.returncode:raise SystemExit(result.returncode)
print('PASS_COHERENT_AF_COST_INFO_NO_PHYSICAL_PROMOTION')
