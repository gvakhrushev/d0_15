#!/usr/bin/env python3
"""Run altered programs at mathematical gates, not merely at changed hashes."""
from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
H=Path(__file__).resolve().parent
source=(H/'verify.py').read_text()
mutants=[
 ('erase_alternative','f = x + c*x*x*(1-x)','f = x'),
 ('wrong_third_moment','-c*int(n==3)/(s**3)','+c*int(n==3)/(s**3)'),
 ('wrong_radial_direction','radial = S.diff(diff,e)*(-2*e)','radial = S.diff(diff,e)*(-e)'),
 ('drop_h_minus2','radial.subs(kappa,h*h/256)/h**2','radial.subs(kappa,h*h/256)/h'),
 ('lose_new_cutoff','Kplus = J*K*J.T+S.eye(12)-J*J.T','Kplus = J*K*J.T'),
 ('wrong_native_reference','return mat((A.T*A)/P**len(code(w)))','return mat((A.T*A)/P**len(w))'),
 ('erase_return_zero',"return ''.join('10' if y else '0' for y in word)","return ''.join('11' if y else '0' for y in word)"),
]
rows=[]
for name,old,new in mutants:
    if source.count(old)!=1:raise AssertionError('MUTATION_ANCHOR_'+name)
    with tempfile.TemporaryDirectory(prefix='d0_forcing_mutant_') as tmp:
        d=Path(tmp)
        shutil.copyfile(H/'RESULT.md',d/'RESULT.md')
        (d/'verify.py').write_text(source.replace(old,new))
        r=subprocess.run([sys.executable,'-O',str(d/'verify.py'),'--write'],
                         stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,
                         timeout=60,env={**os.environ,'OPENBLAS_NUM_THREADS':'1','PYTHONDONTWRITEBYTECODE':'1'})
        if r.returncode==0:raise AssertionError('SURVIVING_MUTANT_'+name)
        # Receipt is generated only after all mathematical/interval gates.
        if (d/'receipt.json').exists():raise AssertionError('MUTANT_REACHED_RECEIPT_'+name)
        if not ('AssertionError' in r.stderr or 'ValueError' in r.stderr):
            raise AssertionError('NONMATHEMATICAL_FAILURE_'+name+': '+r.stderr)
        rows.append({'name':name,'rejected':True,'last_error':r.stderr.strip().splitlines()[-1]})
with tempfile.TemporaryDirectory(prefix='d0_false_scope_') as tmp:
    d=Path(tmp)
    for n in ('RESULT.md','verify.py','receipt.json'):shutil.copyfile(H/n,d/n)
    f=d/'receipt.json';data=json.loads(f.read_text())
    data['scope']['full_Cost_minus_Info_physical_action_identity_proved']=True
    f.write_text(json.dumps(data))
    r=subprocess.run([sys.executable,'-O',str(d/'verify.py')],
                     capture_output=True,text=True,timeout=60,
                     env={**os.environ,'OPENBLAS_NUM_THREADS':'1','PYTHONDONTWRITEBYTECODE':'1'})
    if r.returncode==0 or 'IMMUTABLE_RECEIPT_MISMATCH' not in r.stderr:
        raise AssertionError('FALSE_PHYSICAL_SCOPE_ACCEPTED')
    rows.append({'name':'false_full_action_claim','rejected':True,'last_error':'IMMUTABLE_RECEIPT_MISMATCH'})
report={'schema':'d0-direct-forcing-mutants/1','status':'PASS','results':rows,
        'source_sha256':hashlib.sha256(source.encode()).hexdigest()}
if '--write' in sys.argv:(H/'hostile_receipt.json').write_text(json.dumps(report,indent=2)+'\n')
else:
    if json.loads((H/'hostile_receipt.json').read_text())!=report:
        raise AssertionError('HOSTILE_IMMUTABLE_RECEIPT_MISMATCH')
print(json.dumps(report,indent=2))
