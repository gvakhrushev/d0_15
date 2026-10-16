#!/usr/bin/env python3
"""Execute altered mathematics, not merely checksum failures."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
HERE=Path(__file__).resolve().parent
mutants={
    'omit_time_derivative_family':('for alpha in range(n):','for alpha in range(1,n):'),
    'replace_scalar_kernel_by_trace_reverse':('null[0]==flat(s.eye(k))','null[0]==flat(2*s.eye(k))'),
    'overstate_quantitative_bound':('half = s.Rational(1,2)','half = s.Rational(2,1)'),
    'freeze_state_in_material_source':('return s.trace(drho*L) + s.trace(rho*dL)','return s.trace(rho*dL)'),
    'replace_sector_measure_by_raw_sizes':('v = s.Matrix([s.sqrt(n) for n in sizes])','v = s.Matrix(sizes)'),
    'drop_transverse_plane_weight':('s.Rational(33,2)-n for n in sizes','s.Rational(31,2)-n for n in sizes'),
}
source=(HERE/'verify.py').read_text()
rows=[]
env={**os.environ,'OPENBLAS_NUM_THREADS':'1','PYTHONDONTWRITEBYTECODE':'1'}
for name,(old,new) in mutants.items():
    if source.count(old)!=1:
        raise RuntimeError('MUTATION_ANCHOR_NOT_UNIQUE: '+name)
    with tempfile.TemporaryDirectory() as d:
        root=Path(d)
        (root/'verify.py').write_text(source.replace(old,new))
        (root/'receipt.json').write_bytes((HERE/'receipt.json').read_bytes())
        r=subprocess.run([sys.executable,'-O',str(root/'verify.py')],capture_output=True,text=True,env=env,timeout=35)
        if r.returncode==0 or 'FAILED_MATH:' not in r.stderr:
            raise RuntimeError('MUTANT_NOT_REJECTED_MATHEMATICALLY: '+name+'\n'+r.stderr)
        failure=r.stderr.strip().splitlines()[-1]
        rows.append({'mutation':name,'rejected_at':failure})
with tempfile.TemporaryDirectory() as d:
    root=Path(d)
    (root/'verify.py').write_text(source)
    data=json.loads((HERE/'receipt.json').read_text())
    data['physical_GR_closed']=True
    (root/'receipt.json').write_text(json.dumps(data))
    r=subprocess.run([sys.executable,'-O',str(root/'verify.py')],capture_output=True,text=True,env=env,timeout=35)
    if r.returncode==0 or 'IMMUTABLE_RECEIPT_MISMATCH' not in r.stderr:
        raise RuntimeError('FALSE_PHYSICAL_CLAIM_NOT_REJECTED')
print(json.dumps({'status':'PASS_EXECUTED_MUTANTS','mathematical_mutations':rows,'false_GR_receipt_rejected':True},indent=2))
