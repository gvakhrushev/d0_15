#!/usr/bin/env python3
"""Actually execute four altered formulae; no claim of full native closure."""
from pathlib import Path
import json,sys,subprocess,tempfile
P=Path(__file__).resolve().parent
MUTATIONS=[
 ('resplit_pending_history','kids=split(parent) if parent[1]<n else [parent]',
  'kids=split(parent)','cut_2_retains_pending'),
 ('wrong_density_exponent','eh=2*e; g=e.T*ETA*e;',
  'eh=4*e; g=e.T*ETA*e;','density_coframe_metric'),
 ('freeze_volume_derivative','dpw=chi*(dP-P*S.trace(e.inv()*V))',
  'dpw=chi*dP','weighted_coframe_source_00'),
 ('wrong_coupled_wave_coefficient','H=(s*s/(4*c)+a)*x*x+(s*s/(4*c)-a)*y*y',
  'H=(s*s/(2*c)+a)*x*x+(s*s/(2*c)-a)*y*y','ppwave_all_ten_Einstein_scalar_rows')]
def run():
 text=(P/'check_density_palatini.py').read_text(); out=[]
 with tempfile.TemporaryDirectory(prefix='d0-density-mutations-') as tmp:
  for index,(name,a,b,label) in enumerate(MUTATIONS):
   if text.count(a)!=1: raise ValueError('Nonunique mutation: '+name)
   f=Path(tmp)/(name+'.py');f.write_text(text.replace(a,b))
   function=('clocks','geometry','geometry','curved_control')[index]
   driver="import runpy; m=runpy.run_path("+repr(str(f))+"); m["+repr(function)+"]()"
   r=subprocess.run([sys.executable,'-c',driver],capture_output=True,text=True,timeout=35)
   if r.returncode==0 or 'ArithmeticError: '+label not in r.stderr:
    raise ArithmeticError('Wrong rejection for '+name+'\n'+r.stderr)
   out.append({'mutation':name,'result':'REJECTED_MATHEMATICALLY','check':label})
 return {'schema':'d0-history-density-mutations/1','executed':len(out),'mutations':out}
if __name__=='__main__':print(json.dumps(run(),sort_keys=True,indent=2))
