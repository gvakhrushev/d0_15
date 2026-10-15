"""Independent numerical diagnostic on ALL 6144 real link variables.
Not used as a substitute for interval invertibility or the analytic symmetry proof.
"""
import os
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1';os.environ['JAX_ENABLE_X64']='1'
import jax
jax.config.update('jax_enable_x64',True)
import jax.numpy as j
import numpy as np,json
from pathlib import Path
from itertools import combinations
from symbol import GEN,PAIR,G2,STAR
ROOT=Path(__file__).parent;G=np.array([np.array(x.tolist(),float) for x in GEN]);et=np.diag([1.,-1.,-1.,-1.]);q=np.array((G2*STAR).tolist(),float)

def act(a,E):
 X=j.einsum('...rk,kab->...rab',a.reshape(4,4,4,4,4,6),G);U=j.linalg.solve(j.eye(4)-X/2,j.eye(4)+X/2);Ui=et@j.swapaxes(U,-1,-2)@et
 S=j.array(0.)
 for r,s in PAIR:
  u,v=[i for i in range(4) if i not in (r,s)];seq=[r,s,u,v];sg=(-1)**sum(seq[i]>seq[k] for i,k in combinations(range(4),2))
  P=U[...,r,:,:]@j.roll(U[...,s,:,:],-1,axis=r)@j.roll(Ui[...,r,:,:],-1,axis=s)@Ui[...,s,:,:]
  C=(P-et@j.swapaxes(P,-1,-2)@et)/2
  wc=j.stack([E[...,aa,u]*E[...,bb,v]-E[...,bb,u]*E[...,aa,v] for aa,bb in PAIR],-1)
  b=j.stack([(C@et)[...,aa,bb] for aa,bb in PAIR],-1)
  S+=sg*j.sum(j.einsum('...a,ab,...b->...',wc,q,b))
 return S

grad=jax.grad(act);jvp=jax.jit(lambda a,E,v:jax.jvp(lambda z:grad(z,E),(a,),(v,))[1]);gr=jax.jit(grad)
def main():
 from full_bloch_verify import hessian_enclosure,assemble
 a2=np.array(json.load(open(ROOT/'center.json'))).reshape(4,4,24);A=np.broadcast_to(a2[None,:,:,None,:],(4,4,4,4,24)).copy().reshape(-1)
 E=np.tile(np.eye(4),(4,4,4,4,1,1));c=np.array([1.,0.,-1.,0.]);f=1+c[None,:,None,None]/100+c[None,None,:,None]/1000
 E[...,2,2]=f;E[...,3,3]=f
 res=np.array(gr(A,E));print('full residual diagnostic',np.max(abs(res)),flush=True)
 H,bb=hessian_enclosure(a2.reshape(16,24),0.,True);rng=np.random.default_rng(731)
 report={'status':'NUMERICAL_DIAGNOSTIC_ONLY','full_rows':6144,'full_residual_diagnostic':float(np.max(abs(res))),'bloch_tests':[]}
 for k,l in [(1,1),(1,3),(2,2),(0,0)]:
  w=rng.normal(size=(4,4,24))+1j*rng.normal(size=(4,4,24));realmode=(k%2==0 and l%2==0)
  if realmode:w=w.real.astype(complex)
  phase=(1j)**(k*np.arange(4)[:,None]+l*np.arange(4)[None,:]);V=np.real(phase[:,None,None,:,None]*w[None,:,:,None,:]).reshape(-1)
  out=np.array(jvp(A,E,V)).reshape(4,4,4,4,24)
  recovered=np.einsum('txyzq,tz->xyq',out,np.conj(phase))/16*(1 if realmode else 2)
  hb=assemble(bb,k,l);M=(hb.r.l+hb.r.h)/2+1j*(hb.i.l+hb.i.h)/2
  expected=(M@w.reshape(-1)).reshape(4,4,24);err=float(np.max(abs(recovered-expected)))
  print('full Bloch compare',k,l,err,flush=True)
  if not err<1e-11:raise AssertionError('full Hessian/Bloch discrepancy')
  report['bloch_tests'].append({'q0':k,'q3':l,'absolute_error':err})
 json.dump(report,open(ROOT/'full_diagnostic.json','w'),indent=2)
if __name__=='__main__':main()
