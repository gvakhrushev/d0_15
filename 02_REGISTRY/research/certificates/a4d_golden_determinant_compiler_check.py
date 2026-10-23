#!/usr/bin/env python3
"""Narrow compiler and immutable-source consumer; no physical GR promotion."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

root=Path(__file__).resolve().parents[3]
packet=root/'02_REGISTRY/research/sources/d0_golden_determinant_compiler_2026-10-16'
validation=json.loads((packet/'VALIDATION.json').read_text())
for rel,digest in validation['file_sha256'].items():
    if hashlib.sha256((root/rel).read_bytes()).hexdigest()!=digest:
        raise ArithmeticError('Changed compiler artifact: '+rel)
inputs=json.loads((packet/'INPUTS.json').read_text())
for owner in inputs['documentary_owners']:
    data=(root/owner['path']).read_bytes()
    actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    if actual!=owner['git_blob']:
        raise ArithmeticError('Changed parent theorem/declaration: '+owner['path'])
command=[sys.executable]
if sys.flags.optimize:
    command.append('-O')
command.append(str(packet/'check_golden_determinant.py'))
run=subprocess.run(command,capture_output=True,text=True,check=True,timeout=120)
if json.loads(run.stdout)!=json.loads((packet/'result.json').read_text()):
    raise ArithmeticError('Golden determinant immutable result mismatch')
print('PASS_GOLDEN_DETERMINANT_COMPILER: finite matrix/price/return bridge; native action and GR open')
