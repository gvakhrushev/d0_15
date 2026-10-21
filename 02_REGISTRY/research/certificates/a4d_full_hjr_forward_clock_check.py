#!/usr/bin/env python3
"""Read-only authored replay; upstream native root existence is consumed."""
from __future__ import annotations
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / '02_REGISTRY/research/sources/d0_full_hjr_forward_clock_2026-10-21'
INPUTS = (
    '02_REGISTRY/research/A4D_FULL_HJR_FORWARD_CLOCK_TRANSPORT_2026_10_21.md',
    '02_REGISTRY/research/sources/d0_full_hjr_forward_clock_2026-10-21/PROOF.md',
    '02_REGISTRY/research/sources/d0_full_hjr_forward_clock_2026-10-21/README.md',
    '02_REGISTRY/research/sources/d0_full_hjr_forward_clock_2026-10-21/SOURCES.json',
    '02_REGISTRY/research/sources/d0_full_hjr_forward_clock_2026-10-21/RESULT.json',
    '02_REGISTRY/research/sources/d0_full_hjr_forward_clock_2026-10-21/check_full_hjr_clock.py',
    '02_REGISTRY/research/sources/d0_full_hjr_forward_clock_2026-10-21/SHA256SUMS.json',
)

def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def verify_files() -> dict:
    manifest = json.loads((BASE/'SHA256SUMS.json').read_text())
    for name, expected in manifest['files'].items():
        if digest(ROOT/name) != expected:
            raise RuntimeError('Input hash changed: '+name)
    return {name: digest(ROOT/name) for name in INPUTS}

def compare_payload(actual, expected, path='$', stats=None) -> None:
    if stats is None:
        stats={'float_comparisons':0,'max_absolute_difference':0.0}
    if isinstance(expected, dict):
        if not isinstance(actual, dict) or actual.keys() != expected.keys():
            raise RuntimeError('Result keys differ at '+path)
        for key in expected:
            compare_payload(actual[key],expected[key],path+'.'+key,stats)
    elif isinstance(expected, list):
        if not isinstance(actual, list) or len(actual) != len(expected):
            raise RuntimeError('Result sequence differs at '+path)
        for index,(got,want) in enumerate(zip(actual,expected)):
            compare_payload(got,want,f'{path}[{index}]',stats)
    elif isinstance(expected, float):
        if not isinstance(actual, float) or not math.isclose(actual,expected,rel_tol=2e-15,abs_tol=2e-15):
            raise RuntimeError(f'Numeric result differs at {path}: {actual!r} != {expected!r}')
        stats['float_comparisons']+=1
        stats['max_absolute_difference']=max(stats['max_absolute_difference'],abs(actual-expected))
    elif type(actual) is not type(expected) or actual != expected:
        raise RuntimeError('Exact result differs at '+path)
    return stats

def main() -> None:
    before=verify_files()
    env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
    runs=[]
    for optimized in (False,True):
        command=[sys.executable]+(['-O'] if optimized else [])+[str(BASE/'check_full_hjr_clock.py')]
        run=subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                           env=env,timeout=90,check=False)
        if run.returncode:
            raise RuntimeError('Checker failed: '+run.stderr.decode('utf-8','replace'))
        runs.append(run)
    if runs[0].stdout != runs[1].stdout:
        raise RuntimeError('Normal and optimized checker outputs differ.')
    expected=json.loads((BASE/'RESULT.json').read_text(encoding='utf-8'))
    actual=json.loads(runs[0].stdout.decode('utf-8'))
    comparison=compare_payload(actual,expected)
    if verify_files() != before:
        raise RuntimeError('Replay mutated an input.')
    print(json.dumps({'status':'PASS','authored_conditions':actual['checks']['count'],
                      'inputs_unchanged':True,'normal_optimized_output_equal':True,
                      'pinned_result_structure_and_exact_fields_match':True,
                      'floating_point_tolerance':{'rel_tol':2e-15,'abs_tol':2e-15,
                          'comparisons':comparison['float_comparisons'],
                          'max_absolute_difference':comparison['max_absolute_difference']},
                      'independent_review':False,
                      'upstream_root_existence_reproved':False,
                      'GR_closed':False},sort_keys=True,indent=2))

if __name__=='__main__':
    main()
