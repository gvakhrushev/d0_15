"""High precision approximate 42 root; NOT by itself a certified existence theorem."""
from mp_euler import mp,eval_euler,build
from rational_fixture import newproblem
from scipy.optimize._numdiff import approx_derivative
import numpy as np,json,time
from pathlib import Path
HERE=Path(__file__).resolve().parent

def run(loops=8):
 h,base=build()
 _,_,euler=newproblem()
 x=np.zeros(42)
 J=approx_derivative(euler,x,method='3-point',abs_step=2e-6)
 A=np.linalg.inv(J)
 print('A infinity',np.linalg.norm(A,np.inf))
 A_mp=[[mp.mpf(float(A[i,j])) for j in range(42)] for i in range(42)]
 z=[mp.mpf(0) for _ in range(42)]
 start=time.time()
 for i in range(loops):
  f=eval_euler(z,h,base)
  err=max(abs(x) for x in f)
  print(i,'error',mp.nstr(err,20),'sec',round(time.time()-start,1),flush=True)
  z=[z[j]-sum(A_mp[j][k]*f[k] for k in range(42)) for j in range(42)]
 residual=eval_euler(z,h,base)
 print('final',mp.nstr(max(map(abs,residual)),35),'seconds',time.time()-start)
 # Store rational decimal center with 52 significant fractional digits.
 center=[mp.nstr(v,58) for v in z]
 outfile=HERE/'mp_center.json';outfile.write_text(json.dumps({'center':center,'h':str(h),'residual_mp':mp.nstr(max(map(abs,residual)),30),'inverse_inf_double':str(np.linalg.norm(A,np.inf))},indent=2)+'\n')
 # need certify after rounding decimal center
 z2=[mp.mpf(v) for v in center]
 e2=max(abs(x) for x in eval_euler(z2,h,base))
 print('rounded center residual',mp.nstr(e2,30))
 return z
if __name__=='__main__':run()
