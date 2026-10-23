#!/usr/bin/env python3
"""Actually alter executed identities, keeping the original exact targets."""
from pathlib import Path
import json, subprocess, sys, tempfile
P=Path(__file__).resolve().parent
CHANGES=[
 ('wrong_adjoint_in_full_D_jet','e1=q*(ks[1]-ks[2])*(B-B.T)','e1=q*(ks[1]-ks[2])*(B+B.T)','actual_reverse_block_adjoint'),
 ('drop_half_squared_operator_jet','delta1=dtarget*e1+e1*d0','delta1=dtarget*e1','exact_full16_Delta1_norm'),
 ('remove_global_partition','kap=lambda l:-(1-al*l)**(m-1)/Z0+','kap=lambda l:-(1-al*l)**(m-1)+','actual_complete_price_divided_difference'),
 ('wrong_record_power','kap=lambda l:-(1-al*l)**(m-1)/Z0+','kap=lambda l:-(1-al*l)**m/Z0+','actual_complete_price_divided_difference')]
def run():
 source=(P/'check_exact.py').read_text();out=[]
 with tempfile.TemporaryDirectory(prefix='d0-causal-mutants-') as tmp:
  for name,old,new,label in CHANGES:
   if source.count(old)!=1:raise ValueError('nonunique target: '+name)
   path=Path(tmp)/(name+'.py');path.write_text(source.replace(old,new))
   r=subprocess.run([sys.executable,str(path)],capture_output=True,text=True,timeout=35)
   if r.returncode==0 or 'ArithmeticError: '+label not in r.stderr:
    raise ArithmeticError('unexpected rejection '+name+'\n'+r.stderr)
   out.append({'mutation':name,'failed_at':label,'verdict':'REJECTED_MATHEMATICALLY'})
 return {'schema':'d0-finite-causal-mutations/1','mutations':out,'expected_receipts_changed':False}
if __name__=='__main__':print(json.dumps(run(),sort_keys=True,indent=2))
