#!/usr/bin/env python3
"""Narrow exact consumer; no physical action or GR status promotion."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[3]
P=ROOT/'02_REGISTRY/research/sources/d0_coherent_compilation_2026-10-16'
validation=json.loads((P/'VALIDATION.json').read_text())
for rel,digest in validation['file_sha256'].items():
    if hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()!=digest:
        raise ArithmeticError('changed compilation artifact: '+rel)
inputs=json.loads((P/'INPUTS.json').read_text())
for parent in inputs['owners']:
    data=(ROOT/parent['path']).read_bytes()
    blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    if blob!=parent['git_blob']:
        raise ArithmeticError('changed compilation parent: '+parent['path'])
cmd=[sys.executable]
if sys.flags.optimize:cmd.append('-O')
cmd.append(str(P/'check_coherent_compilation.py'))
run=subprocess.run(cmd,capture_output=True,text=True,check=True,timeout=120)
if json.loads(run.stdout)!=json.loads((P/'result.json').read_text()):
    raise ArithmeticError('coherent compilation result mismatch')
print('PASS_COHERENT_COMPILATION_COST_DESCENT: exact finite/source results; native action and GR open')
