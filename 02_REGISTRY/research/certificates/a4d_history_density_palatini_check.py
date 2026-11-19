#!/usr/bin/env python3
"""Reproduce the bounded packet, not a native/physical GR certificate."""
from pathlib import Path
import hashlib,json,subprocess,sys
ROOT=Path(__file__).resolve().parents[3]
P=ROOT/'02_REGISTRY/research/sources/d0_history_density_palatini_2026-10-16'
meta=json.loads((P/'VALIDATION.json').read_text())
for path,digest in meta['sha256'].items():
    if hashlib.sha256((ROOT/path).read_bytes()).hexdigest()!=digest:
        raise ArithmeticError('Changed history-density packet input: '+path)
cmd=[sys.executable]+(['-O'] if sys.flags.optimize else [])+[str(P/'check_density_palatini.py')]
run=subprocess.run(cmd,capture_output=True,text=True,check=True,timeout=120)
if json.loads(run.stdout)!=json.loads((P/'result.json').read_text()):
    raise ArithmeticError('History-density exact output mismatch')
print('PASS_HISTORY_DENSITY_PALATINI: golden clocks and conditional first-order source; native full action/GR remain open')
