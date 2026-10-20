#!/usr/bin/env python3
"""Research replay only; no physical/source/GR promotion."""
# D0_CI_TIMEOUT_SECONDS=240
from pathlib import Path
import hashlib,json,subprocess,sys,os
ROOT=Path(__file__).resolve().parents[3]
S=ROOT/'02_REGISTRY/research/sources/d0_full_four_dimensional_sheet_2026-10-15'
for f,h in json.loads((S/'MANIFEST.json').read_text()).items():
 if hashlib.sha256((S/f).read_bytes()).hexdigest()!=h:raise RuntimeError('CHANGED_RESEARCH_INPUT: '+f)
env={**os.environ,'OPENBLAS_NUM_THREADS':'1','PYTHONDONTWRITEBYTECODE':'1'}
for argv in [('verify.py',),('-O','verify.py'),('hostile.py',),('invariants.py',)]:
 cmd=[sys.executable]+[str(S/x) if x.endswith('.py') else x for x in argv]
 subprocess.run(cmd,cwd=S,env=env,check=True,timeout=180)
print('PASS_FULL_4D_FINITE_CONNECTION_SHEET_NOT_FULL_GR')
