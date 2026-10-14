#!/usr/bin/env python3
"""Pinned v10 input proofs, immutable matrices/intervals and actual mutants."""
# D0_CI_TIMEOUT_SECONDS=600
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[3]
SOURCE=ROOT/'02_REGISTRY/research/sources/d0_full_record_tape_v10_2026-10-14'
INPUTS={
 '02_REGISTRY/research/sources/d0_two_projection_archive_v9_2026-10-14/RESULT.md':'4e6d6adcee280902ba7854f0bc51a7e47c0092ab',
 '02_REGISTRY/research/sources/d0_record_generated_heat_v8_2026-10-14/RESULT.md':'e5b08043d3156fb30248a482e3c72342ff13add9',
}
for rel,want in INPUTS.items():
    data=(ROOT/rel).read_bytes()
    got=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    if got!=want:raise SystemExit('V10_INPUT_BLOB_MISMATCH: '+rel)
for rel,want in json.loads((SOURCE/'MANIFEST.json').read_text()).items():
    if hashlib.sha256((SOURCE/rel).read_bytes()).hexdigest()!=want:
        raise SystemExit('V10_PAYLOAD_MISMATCH: '+rel)
ENV={**os.environ,'OPENBLAS_NUM_THREADS':'1','PYTHONDONTWRITEBYTECODE':'1'}
for args in (['verify.py'],['-O','verify.py'],['hostile.py']):
    command=[sys.executable]+[str(SOURCE/a) if a.endswith('.py') else a for a in args]
    run=subprocess.run(command,cwd=SOURCE,env=ENV,timeout=240)
    if run.returncode:raise SystemExit(run.returncode)
print('PASS_V10_FULL_RECORD_TAPE_NO_PHYSICAL_PROMOTION')
