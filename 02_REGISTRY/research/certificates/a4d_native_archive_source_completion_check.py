#!/usr/bin/env python3
"""Replay the v6 exact receipt, executed mutants and labelled numerical controls."""
# D0_CI_TIMEOUT_SECONDS=600
from pathlib import Path
import os
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[3]
SOURCE=ROOT/'02_REGISTRY/research/sources/d0_archive_source_completion_v6_2026-10-14'
ENV={**os.environ,'OPENBLAS_NUM_THREADS':'1','PYTHONDONTWRITEBYTECODE':'1'}
for name in ('archive_source_check.py','hostile_check.py','numerical_frechet_check.py'):
    result=subprocess.run([sys.executable,'-O',str(SOURCE/name)],cwd=SOURCE,env=ENV,timeout=180)
    if result.returncode:raise SystemExit(result.returncode)
print('PASS_V6_ARCHIVE_SOURCE_REPLAY_NO_PHYSICAL_CLOSURE')
