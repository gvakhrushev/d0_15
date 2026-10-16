#!/usr/bin/env python3
"""Execute actual faulty programs; never count a checksum failure as a math rejection."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
HERE=Path(__file__).resolve().parent
MUTATIONS=[
 ('restore_spectator_tape','s.kronecker_product(s.eye(alphabet**n)-Z,I)','s.kronecker_product(s.eye(alphabet**n)-Z,K)'),
 ('wrong_two_projection_loop','V=-(2*P-I)*(2*R-I)','V=(2*P-I)*(2*R-I)'),
 ('freeze_completed_operator','F=(U*bare(n)*U.T).applyfunc(s.expand)','F=bare(n)'),
 ('double_new_cutoff','Fn[2]-J12*Fn[1]*J12.T-(s.eye(96)-J12*J12.T)','Fn[2]-J12*Fn[1]*J12.T-2*(s.eye(96)-J12*J12.T)'),
 ('freeze_actual_refinement_jet','dJ=embed(dW,1,2)*pad','dJ=s.zeros(96,24)'),
 ('change_original_feedback_cut','fb=P0*U.T*(s.eye(N)-P0)*U*P0','fb=PF*U.T*(s.eye(N)-PF)*U*PF'),
 ('erase_full_tape_multiplicity','junk=(iv.mpf(32)*iv.mpf(4)**n-1)*4096*gamma','junk=31*4096*gamma'),
 ('omit_purifying_reference','def equations(x,multiplicity=2048):','def equations(x,multiplicity=16):'),
]
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true');args=parser.parse_args()
 source=(HERE/'verify.py').read_text();results=[]
 env={**os.environ,'OPENBLAS_NUM_THREADS':'1','PYTHONDONTWRITEBYTECODE':'1'}
 with tempfile.TemporaryDirectory(prefix='d0-v10-hostile-') as tmp:
  root=Path(tmp)
  for name,old,new in MUTATIONS:
   if source.count(old)!=1:raise AssertionError('MUTATION_ANCHOR_'+name)
   file=root/'mutant.py';file.write_text(source.replace(old,new))
   run=subprocess.run([sys.executable,'-O',str(file),'--math-only'],capture_output=True,text=True,env=env,timeout=90)
   if run.returncode==0 or 'AssertionError:' not in run.stderr or 'IMMUTABLE_RECEIPT' in run.stderr:
    raise AssertionError('MUTANT_SURVIVED_OR_NOT_A_MATH_FAILURE_'+name+'\n'+run.stderr)
   gate=run.stderr.strip().splitlines()[-1]
   results.append({'mutant':name,'rejected_at':gate})
   print(name,gate,flush=True)
  shutil.copy2(HERE/'verify.py',root/'verify.py');shutil.copy2(HERE/'RESULT.md',root/'RESULT.md')
  receipt=json.loads((HERE/'receipt.json').read_text());receipt['scope']['physical_Ward_or_GR']=True
  (root/'receipt.json').write_text(json.dumps(receipt))
  run=subprocess.run([sys.executable,'-O',str(root/'verify.py')],capture_output=True,text=True,env=env,timeout=90)
  if run.returncode==0 or 'IMMUTABLE_RECEIPT_MISMATCH' not in run.stderr:raise AssertionError('FALSE_GR_RECEIPT_NOT_REJECTED')
 result={'schema':'d0-v10-executed-mutants/1','status':'PASS','executed_mathematical_mutants':results,
  'false_GR_receipt_rejected':True,'optimized_execution':True,
  'checker_sha256':hashlib.sha256((HERE/'verify.py').read_bytes()).hexdigest()}
 path=HERE/'hostile_receipt.json'
 if args.write:path.write_text(json.dumps(result,indent=2)+'\n')
 elif json.loads(path.read_text())!=result:raise AssertionError('HOSTILE_RECEIPT_MISMATCH')
 print('PASS_V10_HOSTILE',len(results),'actual code mutants and false GR receipt')
if __name__=='__main__':main()
