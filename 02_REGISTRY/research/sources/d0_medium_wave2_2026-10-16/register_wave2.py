#!/usr/bin/env python3
"""Use the existing registration transaction for this bounded second wave.
No dispatch, GitHub writes, commits or merge. --check remains read-only.
"""
from pathlib import Path
import hashlib
import importlib.util
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
OLD=ROOT/'02_REGISTRY/research/sources/d0_medium_agent_wave_2026-10-16/register_wave.py'
OLD_BLOB='d64442f2a5ecbf2da19a1e9f29312a267d9d7668'
IDS=('WRK-A4D-RESEARCH-CLOSURE-RUNNER-WIRING', 'WRK-A4D-LEAN-SCHUR-STATIONARY-TRANSFER', 'WRK-A4D-LEAN-PRIMITIVE-JET-COMPOSITION', 'WRK-A4D-STORED-ADJOINT-TANGENT-MAP', 'WRK-A4D-FULL-REFERENCE-MATTER-RESPONSE', 'WRK-A4D-V8-FULL-HESSIAN-APPLY', 'WRK-A4D-WEIGHTED-SITE-SOURCE-TRANSFER', 'WRK-A4D-RAW-SOURCE-PRECISION-BUDGET', 'WRK-A4D-CORE-PRIMITIVE-ADMISSION-SPLICE')
BRANCH='control/a4d-medium-wave2-registration-2026-10-16'

def load_transaction():
    raw=OLD.read_bytes()
    blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    if blob!=OLD_BLOB:
        raise ValueError('Registration helper changed; review compatibility instead of bypassing the pin')
    spec=importlib.util.spec_from_file_location('_d0_wave2_original_transaction',OLD)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.HERE=HERE
    module.TASK_IDS=IDS
    module.ROWS=module.load_rows()
    module.EXPECTED_BRANCH=BRANCH
    return module

def main():
    try:
        module=load_transaction()
        # The old branch-error wording mentions #324; no old branch is authorised.
        # EXPECTED_BRANCH above is the sole accepted branch for this transaction.
        return module.main()
    except (OSError,ValueError,ImportError) as exc:
        print('WAVE2_REGISTRATION_BLOCKED: '+str(exc),file=sys.stderr)
        return 1

if __name__=='__main__':
    raise SystemExit(main())
