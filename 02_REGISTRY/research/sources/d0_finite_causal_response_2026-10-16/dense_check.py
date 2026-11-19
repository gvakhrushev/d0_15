"""Independent proper-link assembly; diagnostics are floating-point, not proof."""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import expm, eigvalsh
from itertools import product,combinations
from finite_symbol import curvature
C=np.zeros((4,16,16))
for r in range(4):
 for m in range(16):
  if not m&(1<<r):C[r,m|(1<<r),m]=(-1)**((m&((1<<r)-1)).bit_count())
groups=[list(combinations(range(4),k)) for k in range(5)]
def exterior(A):
 R=np.zeros((16,16))
 for group in groups:
  for i in group:
   for j in group:
    R[sum(1<<r for r in i),sum(1<<r for r in j)]=np.linalg.det(A[np.ix_(i,j)]) if i else 1.
 return R

def vec(y,eps):
 t=np.sqrt(2)*eps*np.cos(2*np.pi*y);dt=-np.sqrt(2)*eps*2*np.pi*np.sin(2*np.pi*y)
 a=np.array([np.cos(t),np.sin(t)/np.sqrt(2),np.sin(t)/np.sqrt(2),0.])
 da=dt*np.array([-np.sin(t),np.cos(t)/np.sqrt(2),np.cos(t)/np.sqrt(2),0.])
 return a,da

def matrices(y,eps):
 a,da=vec(y,eps);g=2*np.outer(a,a)-np.eye(4);dg=2*(np.outer(da,a)+np.outer(a,da));direction=[0,1,1,0]
 out=[]
 for r in range(4):
  G=np.zeros((4,4))
  for aa,b in product(range(4),repeat=2):
   G[aa,b]=sum(g[aa,d]*(direction[r]*dg[d,b]+direction[b]*dg[d,r]-direction[d]*dg[r,b]) for d in range(4))/2
  out.append(-G.T)
 return out

def actual(L,eps,scale=2.):
 h=1/L;p=(np.sqrt(5)-1)/2;beta=2*p*p;alpha=p*p*h*h/128;m=256*L*L;z=2**-20;M=128
 links=[];proper_defect=0.
 for j in range(L):
  y=j*h
  Ms=matrices(y,eps);ps=[expm(h*Ms[0]),None,None,np.eye(4)]
  for r in [1,2]:
   def rhs(t,v):return (v.reshape(4,4)@matrices(y+t,eps)[r]).ravel()
   sol=solve_ivp(rhs,[0,h],np.eye(4).ravel(),method='DOP853',rtol=2e-12,atol=2e-14)
   if not sol.success:raise ArithmeticError('proper link ODE')
   ps[r]=sol.y[:,-1].reshape(4,4)
  a0,_=vec(y,eps);gs=2*np.outer(a0,a0)-np.eye(4)
  for r,A in enumerate(ps):
   at,_=vec(y+h*(r in (1,2)),eps);gt=2*np.outer(at,at)-np.eye(4)
   proper_defect=max(proper_defect,float(np.max(np.abs(A.T@gs@A-gt))))
  links.append([exterior(A) for A in ps])
 ZZ=JJ=0.;vacres=0.;Ractual=None
 for k0,kt,k3 in product(range(L),repeat=3):
  ph0=np.exp(2j*np.pi*k0/L);pht=np.exp(2j*np.pi*kt/L);ph3=np.exp(2j*np.pi*k3/L)
  d=np.zeros((16*L,16*L),complex)
  for j in range(L):
   sl=slice(16*j,16*(j+1));sj=slice(16*((j+1)%L),16*((j+1)%L+1))
   d[sl,sl]+=(C[0]@(ph0*links[j][0]-np.eye(16))+C[3]*(ph3-1)-C[1]-C[2])/(scale*h)
   d[sl,sj]+=(C[1]@links[j][1]+pht*C[2]@links[j][2])/(scale*h)
  D=d+d.conj().T;lam=eigvalsh(D)**2;K=np.exp(m*np.log1p(-alpha*lam));ZZ+=K.sum();JJ-=M*np.log1p(-z+z*K).sum()
  if k0==kt==k3==0:
   vac=np.zeros(16*L);vac[::16]=1/np.sqrt(L);vacres=np.linalg.norm(D@vac)
   psi=np.zeros(16*L)
   for j in range(L):
    a,_=vec(j*h,eps)
    for r in range(4):psi[j*16+(1<<r)]=a[r]/np.sqrt(L)
   Ractual=float(np.vdot(D@psi,D@psi).real)
 return float(np.log(ZZ)/beta+JJ),float(ZZ),vacres,Ractual,proper_defect
if __name__=='__main__':
 import json
 for L in [4,6]:
  a0=actual(L,0);pred=curvature(L,(0,1,1,0),(1.,1.,0.),cutoff=None)['Spp']
  for eps in [.002,.001]:
   ap=actual(L,eps);am=actual(L,-eps);fd=(ap[0]+am[0]-2*a0[0])/eps**2
   print(json.dumps(dict(L=L,eps=eps,analytic=pred,finite_difference=fd,vacuum_residual=ap[2],P1_matter_price=ap[3],value0=a0[0])),flush=True)
