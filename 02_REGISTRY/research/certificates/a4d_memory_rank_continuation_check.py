#!/usr/bin/env python3
"""Narrow exact packet replay; not a physical GR or nonlinear-root certificate."""
from pathlib import Path
import hashlib,json,subprocess,sys
ROOT=Path(__file__).resolve().parents[3]
P=ROOT/'02_REGISTRY/research/sources/d0_memory_rank_continuation_2026-10-16'
meta=json.loads((P/'VALIDATION.json').read_text())
for rel,digest in meta['sha256'].items():
    if hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()!=digest:
        raise ArithmeticError('changed continuation artifact: '+rel)
for owner in json.loads((P/'INPUTS.json').read_text())['consumed_unchanged_owners']:
    if hashlib.sha256((ROOT/owner['path']).read_bytes()).hexdigest()!=owner['sha256']:
        raise ArithmeticError('changed memory-source owner: '+owner['path'])
cmd=[sys.executable]+(['-O'] if sys.flags.optimize else [])+[str(P/'check_rank_continuation.py')]
proc=subprocess.run(cmd,capture_output=True,text=True,check=True,timeout=120)
if json.loads(proc.stdout)!=json.loads((P/'result.json').read_text()):
    raise ArithmeticError('new exact result mismatch')
print('PASS_MEMORY_SOURCE_CAPACITY_AND_NONLINEAR_SELECTION: finite source/rank/jet results; physical GR and nonflat native root OPEN')
