#!/usr/bin/env python3
"""Finite golden-cylinder readout consumer; not native action/GR acceptance."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

root=Path(__file__).resolve().parents[3]
packet=root/'02_REGISTRY/research/sources/d0_golden_cylinder_curvature_2026-10-15'
validation=json.loads((packet/'VALIDATION.json').read_text(encoding='utf8'))
for rel,digest in validation['file_sha256'].items():
    if hashlib.sha256((root/rel).read_bytes()).hexdigest()!=digest:
        raise ArithmeticError('Changed golden-curvature input: '+rel)
command=[sys.executable]+(['-O'] if sys.flags.optimize else [])
run=subprocess.run(command+[str(packet/'check_golden_curvature.py')],
                   capture_output=True,text=True,check=True,timeout=120)
actual=json.loads(run.stdout)
expected=json.loads((packet/'result.json').read_text(encoding='utf8'))
if actual!=expected:
    raise ArithmeticError('Golden-cylinder curvature immutable result mismatch')
print('PASS_GOLDEN_CYLINDER_CURVATURE_READOUT: finite calibrated source; native action and GR open')
