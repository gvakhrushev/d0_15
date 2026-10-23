from pathlib import Path
import subprocess,json
base=Path(__file__).resolve().parent
src=(base/'check_phase_metric_source.py').read_text()
changes=[
 ('freeze_phase_lift','    return lift,inv','    lift[12:,:] = S.zeros(12,12)\n    return lift,inv'),
 ('omit_amplitude_connection','-2*v*d*dtmu*dtnu','-0*v*d*dtmu*dtnu'),
 ('wrong_twotick_factor',"S.diag(4*a*a*b*b,0),'full repeated-gate leakage'","S.diag(2*a*a*b*b,0),'full repeated-gate leakage'"),
]
out=[]
for name,a,b in changes:
 if src.count(a)!=1:raise ValueError((name,src.count(a)))
 target=base/('_mutant_'+name+'.py')
 target.write_text(src.replace(a,b))
 try:
  run=subprocess.run(['python','-O',str(target)],text=True,capture_output=True,timeout=40)
  if run.returncode==0: raise ValueError('Mutant survived: '+name)
  if 'ArithmeticError:' not in run.stderr:raise ValueError('Not mathematical rejection:'+run.stderr)
  out.append({'name':name,'mode':'Python -O','returncode':run.returncode,'mathematical_rejection':run.stderr.strip().splitlines()[-1]})
 finally:target.unlink()
(base/'mutations.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False,indent=2))
