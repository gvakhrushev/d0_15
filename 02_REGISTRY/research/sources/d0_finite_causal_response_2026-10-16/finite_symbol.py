"""Full16 analytic Fourier jets of actual proper links, no finite differences."""
import numpy as np
from itertools import product
from functools import lru_cache
@lru_cache(None)
def tables(q,v):
 q=np.array(q);v=np.array(v);C=np.zeros((4,16,16),complex)
 for r in range(4):
  for m in range(16):
   if not m&(1<<r):C[r,m|(1<<r),m]=(-1)**((m&((1<<r)-1)).bit_count())
 eta=np.diag([1,-1,-1,-1]);H=np.zeros((4,4));H[0,1:]=2*v;H[1:,0]=2*v
 MM=[]
 for r in range(4):
  G=np.array([[sum(eta[a,d]*(q[r]*H[d,b]+q[b]*H[d,r]-q[d]*H[r,b]) for d in range(4))/2 for b in range(4)] for a in range(4)])
  V=-G.T
  MM.append(sum((V[i,j]*(C[i]@C[j].T) for i,j in product(range(4),repeat=2)),np.zeros((16,16),complex)))
 MM=np.array(MM);AA=np.array([C[r]@MM[r] for r in range(4)])
 if np.max(np.abs(AA.sum(0)))>1e-10:raise ArithmeticError('torsionfree first jet')
 AA=np.concatenate([AA,AA.transpose(0,2,1).conj()]);DD=np.concatenate([C,C.transpose(0,2,1).conj()])
 products=np.concatenate([np.einsum('aij,bjk->abik',DD,AA).reshape(64,16,16),np.einsum('bij,ajk->abik',AA,DD).reshape(64,16,16)])
 paulis=[np.eye(2),np.array([[0,1],[1,0]]),np.array([[0,-1j],[1j,0]]),np.diag([1,-1])];PC=[]
 for ids in product(range(4),repeat=4):
  P=paulis[ids[0]]
  for i in ids[1:]:P=np.kron(P,paulis[i])
  coeff=np.einsum('aij,ji->a',products,P)/16
  if np.max(np.abs(coeff))>1e-12:PC.append(coeff)
 PC=np.array(PC).T
 UU=np.array([C[r]@MM[r]@MM[r] for r in range(4)])
 HH=np.einsum('aij,bji->ab',DD,UU);HHt=np.einsum('aij,bji->ab',DD,UU.transpose(0,2,1).conj())
 GG=np.einsum('aij,bij->ab',AA.conj(),AA)
 return C,MM,AA,DD,PC,HH,HHt,GG

def curvature(L,mode=(0,0,1,0),polar=(1.,0.,0.),scale=2.,beta=None,z=2**-20,M=128,cutoff=None,chunk=2048,continuum_clock=False):
 if not isinstance(L,int) or L<4 or L%2: raise ValueError('L must be an even integer >=4')
 if scale<=0 or not (0<z<1) or M<=0: raise ValueError('invalid spectral domain')
 if cutoff is not None and cutoff<2: raise ValueError('cutoff must be >=2')
 p=(np.sqrt(5)-1)/2
 if beta is None:beta=2*p*p
 h=1/L;q=2*np.pi*np.array(mode,float)
 C,MM,AA,DD,PC,HH,HHt,GG=tables(tuple(q),tuple(polar))
 r=np.arange(-L//2,(L+1)//2)
 if cutoff is not None:r=r[np.abs(r)<=cutoff]
 grid=np.array(list(product(r,repeat=4)),int);phase=np.exp(2j*np.pi*grid/L)
 lam=np.sum(np.abs((phase-1)/(scale*h))**2,axis=1)
 alpha=p*p*h*h/128;m_real=beta/alpha
 if not continuum_clock and abs(m_real-round(m_real))>1e-9*max(1,m_real): raise ValueError('noninteger native record count')
 m=round(m_real)
 if np.any(1-alpha*lam<=0): raise ValueError('outside positive B chart')
 weights=np.exp(-beta*lam) if continuum_clock else np.exp(m*np.log1p(-alpha*lam))
 Z=16*weights.sum()
 def fw(l):
  B=1-alpha*l
  if continuum_clock:K=np.exp(-beta*l);PP=K;be=beta;BB=np.ones_like(l)
  else:K=np.exp(m*np.log1p(-alpha*l));PP=K/B;be=(m-1)*alpha;BB=B
  FF=1-z+z*K
  k=-PP/Z+M*z*beta*PP/FF
  kp=be*PP/(BB*Z)+M*z*beta*(-be*PP/(BB*FF)+z*beta*PP*PP/(FF*FF))
  return k,kp
 U=q*h/2;fd=1j*h/2*np.exp(1j*U)*np.sinc(U/np.pi);second=h*h/2*np.sinc(U/np.pi)**2
 direct=square=sus=0.
 for begin in range(0,len(grid),chunk):
  ph=phase[begin:begin+chunk];lk=lam[begin:begin+chunk];phl=ph*np.exp(1j*q*h)
  dl=(phl-1)/(scale*h);dk=(ph-1)/(scale*h)
  dco=np.concatenate([dk,dk.conj()],1);dcl=np.concatenate([dl,dl.conj()],1)
  eco=np.concatenate([ph*fd/(scale*h),(phl*fd.conj()).conj()/(scale*h)],1)
  nE=np.einsum('na,ab,nb->n',eco.conj(),GG,eco).real
  ab1=np.einsum('na,nb->nab',dcl,eco).reshape(len(ph),64);ab2=np.einsum('na,nb->nab',dco,eco).reshape(len(ph),64)
  coeff=np.concatenate([ab1,ab2],1)@PC;nA=16*np.sum(np.abs(coeff)**2,1)
  dd2=ph*second/(scale*h)
  tD=2*(np.einsum('na,ab,nb->n',dco,HH,dd2)+np.einsum('na,ab,nb->n',dco,HHt,dd2.conj())).real
  ll=np.sum(np.abs(dl)**2,1);kk,kpk=fw(lk);kl,kpl=fw(ll)
  close=np.abs(ll-lk)<1e-9;div=np.empty(len(ph));div[close]=(kpk[close]+kpl[close])/2
  div[~close]=(kl[~close]-kk[~close])/(ll[~close]-lk[~close])
  direct+=np.sum(kk*tD);square+=2*np.sum((kk+kl)*nE);sus+=2*np.sum(div*nA)
 total=direct+square+sus
 return dict(L=L,mode=mode,polar=polar,beta=beta,scale=scale,cutoff=cutoff,count=len(grid),Z=float(Z),Spp=float(total),rescaled=float(total/h**2),direct=float(direct/h**2),square=float(square/h**2),sus=float(sus/h**2))
