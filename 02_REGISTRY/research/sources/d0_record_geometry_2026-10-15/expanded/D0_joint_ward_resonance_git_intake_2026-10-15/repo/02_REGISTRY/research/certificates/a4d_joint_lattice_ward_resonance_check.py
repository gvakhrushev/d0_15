#!/usr/bin/env python3
"""Exact joint-quadratic source identities; no nonlinear physical promotion."""
# D0_CI_TIMEOUT_SECONDS=300
from pathlib import Path
import os,subprocess,sys
ROOT=Path(__file__).resolve().parents[3]
SRC=ROOT/'02_REGISTRY/research/sources/d0_joint_lattice_ward_resonance_2026-10-15'
env={**os.environ,'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1','PYTHONDONTWRITEBYTECODE':'1'}
for args in ([str(SRC/'verify.py')],['-O',str(SRC/'verify.py')],[str(SRC/'hostile.py')]):
    result=subprocess.run([sys.executable,*args],cwd=SRC,env=env,timeout=240)
    if result.returncode:raise SystemExit(result.returncode)
print('PASS_JOINT_LATTICE_WARD_AND_RESONANCE_NOT_NONLINEAR_GR')
