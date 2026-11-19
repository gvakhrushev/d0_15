#!/usr/bin/env python3
"""Direct forcing test: pinned consumed owners, exact mathematics, hostile mutations."""
# D0_CI_TIMEOUT_SECONDS=300
from pathlib import Path
import hashlib
import os
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[3]
SOURCE=ROOT/'02_REGISTRY/research/sources/d0_direct_forcing_attack_2026-10-14'
PINS={
 '03_FORMALIZATION/D0/Foundation/M1ClassAdmissibility.lean':'4c59104c39152dad53c8264de9ae95eb99b0dba3',
 '03_FORMALIZATION/D0/CondensedAnchor/DetectorSupportGoldenWeight.lean':'d7f7f170815cc3ad2052ad48280ae5919652b314',
 '02_REGISTRY/research/A4D_NATIVE_GOLDEN_COST_REFINEMENT.md':'573e2d70c1d7cbefd35670431b1ab9b87624dbdd',
 '02_REGISTRY/research/sources/d0_full_record_tape_v10_2026-10-14/RESULT.md':'248489d082ffeb5e904aa4edcf2c9b2b5a4881dc',
}
for path,expected in PINS.items():
    data=(ROOT/path).read_bytes()
    actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    if actual!=expected:raise SystemExit('CONSUMED_OWNER_PIN_MISMATCH: '+path)
env={**os.environ,'OPENBLAS_NUM_THREADS':'1','PYTHONDONTWRITEBYTECODE':'1'}
for args in ((str(SOURCE/'verify.py'),),('-O',str(SOURCE/'verify.py')),('-O',str(SOURCE/'hostile.py'))):
    run=subprocess.run([sys.executable,*args],cwd=SOURCE,env=env,timeout=90)
    if run.returncode:raise SystemExit(run.returncode)
print('PASS_DIRECT_FORCING_ATTACK_NO_PHYSICAL_ACTION_PROMOTION')
