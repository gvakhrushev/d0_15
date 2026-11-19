#!/usr/bin/env python3
"""Narrow geometric normalizer consumer; native action/GR binding stays open."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

root=Path(__file__).resolve().parents[3]
packet=root/'02_REGISTRY/research/sources/d0_record_normal_volume_2026-10-15'
validation=json.loads((packet/'VALIDATION.json').read_text(encoding='utf8'))
for rel,digest in validation['file_sha256'].items():
    if hashlib.sha256((root/rel).read_bytes()).hexdigest()!=digest:
        raise ArithmeticError('Changed normal-volume input: '+rel)
command=[sys.executable]
if sys.flags.optimize: command.append('-O')
command.append(str(packet/'check_normal_volume.py'))
run=subprocess.run(command,capture_output=True,text=True,check=True,timeout=120)
actual=json.loads(run.stdout)
expected=json.loads((packet/'result.json').read_text(encoding='utf8'))
if actual!=expected:
    raise ArithmeticError('Normal-volume source immutable result mismatch')
print('PASS_RECORD_NORMAL_VOLUME_SOURCE: exact geometric source; native action and GR closure open')
