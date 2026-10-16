#!/usr/bin/env python3
"""Narrow exact replay; no native physical admission or GR certification."""
from pathlib import Path
import hashlib, json, subprocess, sys
ROOT=Path(__file__).resolve().parents[3]
P=ROOT/'02_REGISTRY/research/sources/d0_native_memory_source_2026-10-16'
meta=json.loads((P/'VALIDATION.json').read_text())
for rel,expected in meta['sha256'].items():
    if hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()!=expected:
        raise ArithmeticError('Changed memory/source packet: '+rel)
cmd=[sys.executable]+(['-O'] if sys.flags.optimize else [])+[str(P/'check_memory_source.py')]
run=subprocess.run(cmd,text=True,capture_output=True,check=True,timeout=45)
if json.loads(run.stdout)!=json.loads((P/'result.json').read_text()):
    raise ArithmeticError('Memory/source exact output mismatch')
print('PASS_NATIVE_MEMORY_SOURCE: exact conditional roots and source; native dynamics/GR remain open')
