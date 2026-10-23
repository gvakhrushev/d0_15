#!/usr/bin/env python3
"""Execute actual altered v6 programs and reject a false physical-closure receipt."""
from __future__ import annotations
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

HERE=Path(__file__).resolve().parent
CASES=[
 ('normalized_partial_trace','sum(M[2*i+a,2*j+a] for a in range(2))','sum(M[2*i+a,2*j+a] for a in range(2))/2'),
 ('drop_moving_full_state','remainder = s.trace(drho*(L-tensor(K,I2)))+s.trace((rho-adjoint(rhoR))*V)','remainder = s.trace((rho-adjoint(rhoR))*V)'),
 ('replace_adjoint_by_state_channel','return s.Rational(4,5)*kubo(tensor(T,I2))','return tensor(T,I2/2)'),
 ('discard_noncommuting_log_derivative','direct=additive_log(partial(additive_kubo(V)))','direct=md.inv()*partial(additive_kubo(V))'),
 ('freeze_thermal_archive_state','dtau=2*beta*tauA*(AA-mu*I2)','dtau=s.zeros(2)'),
 ('replace_actual_flag_cut_by_data_cut','flagcut=s.diag(*[(i>>3)&1 for i in range(16)])','flagcut=s.diag(*[(i>>2)&1 for i in range(16)])'),
 ('remove_one_energy_level','exponential = P0+P2/4','exponential = P0+P2/2'),
 ('discard_joint_correlations','correlated=s.diag(s.Rational(2,3),0,0,s.Rational(1,3))','correlated=tensor(tauA,tauA)')]


def controls():
    text=(HERE/'archive_source_check.py').read_text()
    env={**os.environ,'OPENBLAS_NUM_THREADS':'1','PYTHONDONTWRITEBYTECODE':'1'}
    def case(item):
        name,before,after=item
        if text.count(before)!=1:raise AssertionError('UNIQUE_MUTATION:'+name)
        changed=text.replace(before,after)
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'mutant.py';p.write_text(changed)
            run=subprocess.run([sys.executable,'-O',str(p),'--math-only'],capture_output=True,text=True,env=env,timeout=60)
            if run.returncode==0 or 'AssertionError:' not in run.stderr:
                raise AssertionError('NOT_A_MATHEMATICAL_REJECTION:'+name+'\n'+run.stderr)
            return {'name':name,'exit_code':run.returncode,'failure':run.stderr.strip().splitlines()[-1],
                    'mutant_sha256':hashlib.sha256(changed.encode()).hexdigest()}
    with ThreadPoolExecutor(max_workers=2) as executor:
        rows=list(executor.map(case,CASES))
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp)
        for name in ('archive_source_check.py','A4D_NATIVE_ARCHIVE_SOURCE_COMPLETION.md','archive_source_receipt.json'):
            (root/name).write_bytes((HERE/name).read_bytes())
        obj=json.loads((root/'archive_source_receipt.json').read_text())
        obj['scope']['GR_or_original_parent_closed']=True
        (root/'archive_source_receipt.json').write_text(json.dumps(obj))
        run=subprocess.run([sys.executable,'-O',str(root/'archive_source_check.py')],capture_output=True,text=True,env=env,timeout=60)
        if run.returncode==0 or 'IMMUTABLE_RECEIPT_MISMATCH' not in run.stderr:
            raise AssertionError('FALSE_CLOSURE_RECEIPT_NOT_REJECTED')
    return {'schema':'d0-v6-executed-hostiles/1','status':'PASS','program_mutants':rows,
            'false_physical_closure_receipt_rejected':True}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args()
    obj=controls();obj['checker_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    path=HERE/'hostile_receipt.json'
    if args.write:path.write_text(json.dumps(obj,indent=2)+'\n')
    elif json.loads(path.read_text())!=obj:raise AssertionError('IMMUTABLE_HOSTILE_RECEIPT_MISMATCH')
    print('PASS_V6_HOSTILES',len(obj['program_mutants']),'programs + false closure receipt')
    for row in obj['program_mutants']:print(row['name'],row['failure'])
if __name__=='__main__':main()
