#!/usr/bin/env python3
"""Verify the immutable v4-v5 source capsule and replay actual mathematical tests.

Default: byte verification and both exact suites. --full-replay additionally
runs the original interval, optimized, simulator, and hostile-program groups.
All restoration and all result-writing legacy programs stay in a temporary tree.
"""
# D0_CI_TIMEOUT_SECONDS=600
from __future__ import annotations
import argparse
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[3]
CAPSULE = ROOT/'02_REGISTRY/research/sources/d0_v4_v5_verified_capsule_2026-10-14'


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--full-replay',action='store_true');args=ap.parse_args()
    spec=importlib.util.spec_from_file_location('d0_v4_v5_restore',CAPSULE/'restore.py')
    if spec is None or spec.loader is None:raise RuntimeError('RESTORE_LOADER')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    env={**os.environ,'OPENBLAS_NUM_THREADS':'1','PYTHONDONTWRITEBYTECODE':'1','PYTHONHASHSEED':'0'}
    with tempfile.TemporaryDirectory(prefix='d0-v4-v5-') as directory:
        target=Path(directory);receipt=module.restore(CAPSULE,target)
        source=target/'02_REGISTRY/research/sources'
        v4=source/'d0_internal_routing_v4_2026-10-14'
        v5=source/'d0_native_controller_v5_2026-10-14'
        if args.full_replay:
            jobs=[(v4,[sys.executable,'src/run_all.py']),
                  (v5,[sys.executable,'src/run_all.py','--workers','2','--log-dir',str(target/'v5_logs')])]
        else:
            jobs=[(v4,[sys.executable,'-O','src/internal_routing_exact.py']),
                  (v5,[sys.executable,'-O','src/exact_check.py'])]
        for cwd,command in jobs:
            result=subprocess.run(command,cwd=cwd,env=env,capture_output=True,text=True,timeout=270)
            if result.returncode:
                print(result.stdout);print(result.stderr,file=sys.stderr)
                raise SystemExit(result.returncode)
            print(result.stdout[-2000:])
        receipt['full_replay']=args.full_replay
        receipt['physical_admission_or_GR_closed']=False
        print(json.dumps(receipt,sort_keys=True))

if __name__=='__main__':main()
