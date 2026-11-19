#!/usr/bin/env python3
"""Reproduce this packet; do not promote native admission or GR status."""
from pathlib import Path
import hashlib,json,subprocess,sys
ROOT=Path(__file__).resolve().parents[3]
P=ROOT/'02_REGISTRY/research/sources/d0_central_record_2026-10-16'
meta=json.loads((P/'VALIDATION.json').read_text())
for name,digest in meta['sha256'].items():
    if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=digest:
        raise ArithmeticError('Changed central-record input: '+name)
cmd=[sys.executable]+(['-O'] if sys.flags.optimize else [])+[str(P/'check_central_record.py')]
run=subprocess.run(cmd,capture_output=True,text=True,check=True,timeout=120)
if json.loads(run.stdout)!=json.loads((P/'result.json').read_text()):
    raise ArithmeticError('Central-record result mismatch')
print('PASS_CENTRAL_RECORD_VARIATIONAL_EQUIVALENCE: finite program and actual preparation measure; physical selection/GR open')
