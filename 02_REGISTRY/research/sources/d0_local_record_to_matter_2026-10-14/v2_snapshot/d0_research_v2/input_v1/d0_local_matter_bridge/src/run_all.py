#!/usr/bin/env python3
"""Reproduce this LOCAL packet. No network, GitHub, CI or Lean claims.
The interval and exact checks are proofs within the report's hypotheses.
The finite refinement scan remains explicitly labelled numerical.
"""
from __future__ import annotations
import json,os,platform,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
commands=[
 ('exact_algebra',[sys.executable,'src/exact_algebra.py']),
 ('exact_algebra_optimized',[sys.executable,'-O','src/exact_algebra.py']),
 ('full_local_operator',[sys.executable,'src/full_local_operator_check.py']),
 ('interval_L8',[sys.executable,'src/interval_l8.py']),
 ('interval_L8_optimized',[sys.executable,'-O','src/interval_l8.py']),
 ('pi0_phase_hostile',[sys.executable,'src/pi0_phase_boundary.py']),
 ('actual_code_mutations',[sys.executable,'src/hostile_mutations.py']),
 ('finite_refinement_diagnostics',[sys.executable,'src/continuum_and_sources.py']),
]
results=[]
for name,command in commands:
    start=time.monotonic()
    p=subprocess.run(command,cwd=ROOT,text=True,capture_output=True,timeout=180,
                     env={**os.environ,'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1','PYTHONHASHSEED':'0'})
    (ROOT/'logs'/f'{name}.txt').write_text(p.stdout+'\n--- STDERR ---\n'+p.stderr)
    results.append({'name':name,'command':command[1:],'exit_code':p.returncode,
                    'elapsed_seconds':round(time.monotonic()-start,3)})
    print(name,'PASS' if p.returncode==0 else 'FAIL',flush=True)
    if p.returncode:raise RuntimeError(f'{name} failed; see logs')
record={'schema':'d0-local-replay/1','status':'PASS','checks':results,'python':platform.python_version(),
        'network_used_by_this_runner':False,'GitHub_published':False,'CI_run':False,'Lean_compilation':False,
        'all_D0_action_terms_tested':False,'native_pi0_matter_preparation_proved':False}
(ROOT/'results/replay.json').write_text(json.dumps(record,indent=2)+'\n')
