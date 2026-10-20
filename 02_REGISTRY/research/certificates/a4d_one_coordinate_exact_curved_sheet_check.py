#!/usr/bin/env python3
"""Replay the exact one-coordinate curved sheet without physical promotion."""
# D0_CI_TIMEOUT_SECONDS=600
from pathlib import Path
import hashlib,json,os,subprocess,sys
ROOT=Path(__file__).resolve().parents[3]
SOURCE=ROOT/'02_REGISTRY/research/sources/d0_one_coordinate_exact_curved_sheet_2026-10-15'
PINS={
 '02_REGISTRY/research/certificates/a4d_j2_fixed_realization_ir_check.py':'917cb7246e8bb74cc3a91169acecb7bbd743cade',
 '02_REGISTRY/research/certificates/a4d_finite_probe_palatini_check.py':'f2a159e0ad554784223e13a2bdf8fd0170ba53ec',
 '02_REGISTRY/research/A4D_NATIVE_FINITE_PROBE_COMPLETION.md':'90179067ece3dd4959a920029d1dad306a91c5d7',
}
for path,expected in PINS.items():
 data=(ROOT/path).read_bytes()
 actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
 if actual!=expected:raise RuntimeError('CONSUMED_OWNER_CHANGED: '+path)
for path,expected in json.loads((SOURCE/'MANIFEST.json').read_text()).items():
 if hashlib.sha256((SOURCE/path).read_bytes()).hexdigest()!=expected:raise RuntimeError('SOURCE_CHANGED: '+path)
# Compare executed symbol definitions with the actual pinned repository owner.
sys.dont_write_bytecode=True
sys.path.insert(0,str(SOURCE))
import sympy as s
import algebra
owner=(ROOT/'02_REGISTRY/research/certificates/a4d_j2_fixed_realization_ir_check.py').read_text()
marker='check("LORENTZ_GENERATORS"'
if owner.count(marker)!=1:raise RuntimeError('OWNER_DEFINITION_BOUNDARY_CHANGED')
ns={'__name__':'_owned_exact_symbol'}
exec(compile(owner.split(marker)[0],'<pinned D0 symbol definitions>','exec'),ns)
z=s.symbols('z',nonzero=True);ph=[s.Integer(1),z,s.Integer(1),s.Integer(1)]
if ns['connection_symbol'](s.eye(4),ph)!=algebra.symbol(s.eye(4),ph):raise RuntimeError('LITERAL_OWNER_SYMBOL_MISMATCH')
env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','OPENBLAS_NUM_THREADS':'1'}
for args in (['verify.py'],['-O','verify.py','--algebra'],['verify.py','--numeric'],['hostile.py']):
 command=[sys.executable]+[str(SOURCE/a) if a.endswith('.py') else a for a in args]
 p=subprocess.run(command,cwd=SOURCE,env=env,timeout=300)
 if p.returncode:raise SystemExit(p.returncode)
print('PASS_ONE_COORDINATE_EXACT_CURVED_SHEET_RAW_RESPONSE_NOT_FULL_D0_TERMINAL')
