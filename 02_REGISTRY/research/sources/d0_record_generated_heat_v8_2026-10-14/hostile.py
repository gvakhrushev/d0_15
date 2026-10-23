#!/usr/bin/env python3
"""Execute changed programs: --write prevents hash mismatch masquerading as math rejection."""
from pathlib import Path
import json, os, subprocess, sys, tempfile
HERE=Path(__file__).resolve().parent
changes=[
 ('wrong_Dirac_scale','A==D/16','A==D/8'),
 ('drop_curvature_commutators','D*D!=scalar','D*D==scalar'),
 ('wrong_survivor_sign','w[0]==I-2*A.T*A','w[0]==I+2*A.T*A'),
 ('erase_reference_multiplicity','multiplicity=2048','multiplicity=16'),
 ('omit_program_feedback','omit_feedback=False','omit_feedback=True'),
 ('replace_count_matter_by_log_matter','-target,mu[1]','-target/B1,mu[1]'),
 ('freeze_local_coefficient_jet','s.diag(-s.Rational(3,4),0)','s.diag(0,0)'),
 ('heat_from_wrong_record_length','e=(1-alpha*x)**(2*n)','e=(1-alpha*x)**n'),
]
source=(HERE/'verify.py').read_text();out=[]
env={**os.environ,'OPENBLAS_NUM_THREADS':'1','PYTHONDONTWRITEBYTECODE':'1'}
for name,before,after in changes:
 if source.count(before)!=1:raise AssertionError('MUTATION_ANCHOR_'+name)
 with tempfile.TemporaryDirectory() as tmp:
  root=Path(tmp);(root/'RESULT.md').write_bytes((HERE/'RESULT.md').read_bytes())
  (root/'verify.py').write_text(source.replace(before,after))
  r=subprocess.run([sys.executable,'-O',str(root/'verify.py'),'--write'],capture_output=True,text=True,env=env,timeout=30)
  if r.returncode==0 or 'AssertionError' not in r.stderr:
   raise AssertionError('MUTANT_SURVIVED_OR_CRASHED_'+name+'\n'+r.stderr)
  out.append({'mutant':name,'verdict':'REJECTED','gate':r.stderr.splitlines()[-1]})
# Reject a false scientific-scope receipt by an unchanged checker.
with tempfile.TemporaryDirectory() as tmp:
 root=Path(tmp)
 for f in ('verify.py','RESULT.md','receipt.json'):(root/f).write_bytes((HERE/f).read_bytes())
 receipt=json.loads((root/'receipt.json').read_text());receipt['Einstein_GR']=True
 (root/'receipt.json').write_text(json.dumps(receipt))
 r=subprocess.run([sys.executable,'-O',str(root/'verify.py')],capture_output=True,text=True,env=env,timeout=30)
 if r.returncode==0 or 'IMMUTABLE_RECEIPT_MISMATCH' not in r.stderr:raise AssertionError('FALSE_GR_SCOPE_NOT_REJECTED')
 out.append({'mutant':'false_GR_receipt','verdict':'REJECTED','gate':'IMMUTABLE_RECEIPT_MISMATCH'})
print(json.dumps({'status':'PASS','executed_mutants':out},indent=2))
