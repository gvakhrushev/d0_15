#!/usr/bin/env python3
"""Narrow exact replay of the same-price theorem; not a GR certificate."""
from pathlib import Path
import hashlib,json,subprocess,sys
ROOT=Path(__file__).resolve().parents[3]
P=ROOT/'02_REGISTRY/research/sources/d0_native_price_unfolding_2026-10-16'
meta=json.loads((P/'VALIDATION.json').read_text())
for name,digest in meta['sha256'].items():
    if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=digest:
        raise ArithmeticError('changed same-price artifact: '+name)
command=[sys.executable]+(['-O'] if sys.flags.optimize else [])+[str(P/'check_unfolding.py')]
run=subprocess.run(command,capture_output=True,text=True,check=True,timeout=120)
if json.loads(run.stdout)!=json.loads((P/'result.json').read_text()):
    raise ArithmeticError('same-price exact replay mismatch')
print('PASS_NATIVE_PRICE_EXACT_UNFOLDING: same finite action/source; physical admission and GR remain OPEN')
