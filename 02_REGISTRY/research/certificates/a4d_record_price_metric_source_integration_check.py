#!/usr/bin/env python3
"""Narrow exact SOURCE consumer; no claim of native admission or GR closure."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

root=Path(__file__).resolve().parents[3]
packet=root/'02_REGISTRY/research/sources/d0_record_geometry_source_integration_2026-10-15'
validation=json.loads((packet/'VALIDATION.json').read_text(encoding='utf8'))
for rel,digest in validation['file_sha256'].items():
    if hashlib.sha256((root/rel).read_bytes()).hexdigest()!=digest:
        raise ArithmeticError('Changed integration input: '+rel)
command=[sys.executable]
if sys.flags.optimize:command.append('-O')
command.append(str(packet/'check_phase_metric_source.py'))
run=subprocess.run(command,capture_output=True,text=True,check=True,timeout=120)
actual=json.loads(run.stdout)
expected=json.loads((packet/'result.json').read_text(encoding='utf8'))
if actual!=expected:
    raise ArithmeticError('Price/metric/source immutable result mismatch')
print('PASS_RECORD_PRICE_METRIC_SOURCE_INTEGRATION: exact comparator and smooth nonhomogeneous lift; native/GR open')
