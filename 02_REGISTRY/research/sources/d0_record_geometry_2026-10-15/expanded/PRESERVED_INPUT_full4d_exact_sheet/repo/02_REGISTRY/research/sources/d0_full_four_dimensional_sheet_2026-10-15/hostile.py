"""Executed semantic mutations. A missing import does not count as detection."""
from pathlib import Path
import tempfile,shutil,subprocess,sys,os,json
R=Path(__file__).parent
cases=[
 ('interval_check.py','self.l=np.array(l,float,copy=True);self.h=np.array(l if h is None else h,float,copy=True)','self.l=np.asarray(l,float);self.h=np.asarray(l if h is None else h,float)','independent_interval_endpoint_storage'),
 ('interval_check.py','ex=(off[j][0]-off[i][0],off[j][1]-off[i][1])','ex=(0,0)','literal_full_Bloch_placement'),
 ('interval_check.py','coef=ee[u]*ee[v]*.5','coef=-ee[u]*ee[v]*.5','literal_full_Bloch_placement'),
 ('blas_bounds.py','GAMMA=2.**-38','GAMMA=0.','BLAS_error_factor_proved'),
]
receipt=[]
for file,old,new,expected in cases:
 with tempfile.TemporaryDirectory() as td:
  d=Path(td)
  for p in R.glob('*.py'):shutil.copy2(p,d/p.name)
  shutil.copy2(R/'center.json',d/'center.json')
  f=d/file;txt=f.read_text()
  if old not in txt:raise AssertionError('mutation anchor absent')
  f.write_text(txt.replace(old,new,1))
  p=subprocess.run([sys.executable,str(d/'verify.py'),'--kernel-only'],capture_output=True,text=True,env={**os.environ,'OPENBLAS_NUM_THREADS':'1','PYTHONDONTWRITEBYTECODE':'1'},timeout=40)
  out=p.stdout+p.stderr
  if p.returncode==0 or expected not in out:raise AssertionError('mutation not mathematically detected: '+file+' '+out[-700:])
  receipt.append({'file':file,'mutation':old+' -> '+new,'returncode':p.returncode,'detected_by':expected})
print(json.dumps(receipt,indent=2));
if '--write' in sys.argv:(R/'hostile_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
