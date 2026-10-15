#!/usr/bin/env python3
"""Replay complete-gain mathematics. Exact tests do not declare physical closure."""
# D0_CI_TIMEOUT_SECONDS=180
from pathlib import Path
import hashlib,json,os,subprocess,sys
ROOT=Path(__file__).resolve().parents[3]
SOURCE=ROOT/'02_REGISTRY/research/sources/d0_operational_gain_2026-10-15'
PINS={
 '02_REGISTRY/research/A4D_NATIVE_BRANCH_INFORMATION_COCYCLE.md':'011018f98d0162f474bddbbbef1c3c07d20f7953',
 '02_REGISTRY/research/sources/d0_coherent_af_cost_info_2026-10-14/RESULT.md':'8155bef275c50e58da468038b8d6913dcd9d5325',
 '02_REGISTRY/research/A4D_NATIVE_GOLDEN_COST_REFINEMENT.md':'573e2d70c1d7cbefd35670431b1ab9b87624dbdd',
}
for path,expected in PINS.items():
    data=(ROOT/path).read_bytes()
    actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    if actual!=expected:raise RuntimeError('CONSUMED_OWNER_CHANGED: '+path)
for path,expected in json.loads((SOURCE/'MANIFEST.json').read_text()).items():
    if hashlib.sha256((SOURCE/path).read_bytes()).hexdigest()!=expected:
        raise RuntimeError('SOURCE_CHANGED: '+path)
env={**os.environ,'OPENBLAS_NUM_THREADS':'1','PYTHONDONTWRITEBYTECODE':'1'}
for args in (['verify.py'],['-O','verify.py'],['hostile.py']):
    command=[sys.executable]+[str(SOURCE/a) if a.endswith('.py') else a for a in args]
    run=subprocess.run(command,cwd=SOURCE,env=env,timeout=120)
    if run.returncode:raise SystemExit(run.returncode)
print('PASS_OPERATIONAL_GAIN_AND_FINITE_MEMORY_NOT_PHYSICAL_INFO_SELECTION')
