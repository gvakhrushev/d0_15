#!/usr/bin/env python3
"""Read-only validation. Compare actual outputs to frozen receipts; never update them."""
from __future__ import annotations
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys

ROOT=Path(__file__).resolve().parent

def checked(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)

def verify_manifest() -> dict[str,str]:
    pins=json.loads((ROOT/'MANIFEST.json').read_text())['sha256']
    for name,digest in pins.items():
        actual=hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
        checked(actual==digest,'Changed pinned file: '+name)
    old=json.loads((ROOT/'previous/MANIFEST.json').read_text())
    for name,digest in old.items():
        checked(hashlib.sha256((ROOT/'previous'/name).read_bytes()).hexdigest()==digest,
                'Changed historical file: '+name)
    return pins

def replay(args: list[str], expected: str) -> dict:
    env=dict(os.environ,OPENBLAS_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
    completed=subprocess.run([sys.executable,*args],cwd=ROOT,env=env,
                             capture_output=True,check=False,timeout=120)
    checked(completed.returncode==0,
            'Failed '+repr(args)+'\n'+completed.stderr.decode('utf-8',errors='replace'))
    checked(completed.stdout==(ROOT/expected).read_bytes(),
            'Output differs from frozen receipt: '+expected)
    return {'command':['python',*args], 'expected':expected,
            'stdout_sha256':hashlib.sha256(completed.stdout).hexdigest(),
            'returncode':completed.returncode}

def main() -> None:
    before=verify_manifest()
    outputs=[replay(['check_spectral_closure.py'],'RESULT.json'),
             replay(['-O','check_spectral_closure.py'],'RESULT_OPTIMIZED.json'),
             replay(['inputs/check_all40_arbitrary_brinkmann.py'],'GEOMETRY_REPLAY.txt'),
             replay(['previous/check_global_spectral.py'],'previous/RESULT.json')]
    checked(before==verify_manifest(),'Manifest changed during replay')
    print(json.dumps({'status':'PASS_READ_ONLY_ACCEPTANCE',
                      'pinned_files':len(before),'new_active_checks_per_run':190,
                      'replays':outputs,'sources_unchanged':True,
                      'remote_published':False,'new_Lean_build':False,
                      'physical_GR_closed':False},ensure_ascii=False,indent=2))

if __name__=='__main__':
    main()
