"""Independent actual full Dirac/Riesz source on the fixed-collar chart."""
import json
import itertools
from pathlib import Path
import numpy as np
from scipy.linalg import eigh,expm,expm_frechet

ROOT=Path(__file__).resolve().parents[4]
eta=np.diag([1.,-1.,-1.,-1.]); L=8; ell=1/L
p=(np.sqrt(5)-1)/2;alpha=p*p/(128*L*L);m=256*L*L;beta=m*alpha;z=2**-20
d=.06363519159434453504282969743331663;o=.00401673504323172528738445191482512
a=np.sqrt(d-o);b=(np.sqrt(d+3*o)-a)/4
V0=eta@(a*np.eye(4)+b*np.ones((4,4)))
C=np.zeros((4,16,16))
for i in range(4):
 for mask in range(16):
  if not mask&(1<<i):C[i,mask|(1<<i),mask]=(-1)**((mask&((1<<i)-1)).bit_count())
def create(v):return np.einsum('a,aij->ij',v,C)
def gamma(X):return np.einsum('ab,aij,bkj->ik',X,C,C)
S=np.zeros((5,4,4));S[0,0,0]=1;S[1,0,1:]=1;S[1,1:,0]=-1
S[2]=np.diag([0.,1.,1.,1.]);S[3,1:,1:]=1-np.eye(3);S[4,0,1:]=1;S[4,1:,0]=1
B=np.zeros((4,4,4))
for i in range(1,4):B[i,0,i]=B[i,i,0]=1
families=np.zeros((4,4,4,4));families[0,0]=B.sum(axis=0)
for i in range(1,4):
 families[1,i]=B[i];families[2,i]=B.sum(axis=0)-B[i]
 for j in range(1,4):
  if i!=j:families[3,i,i,j]+=1;families[3,i,j,i]-=1
GF=np.array([[gamma(X) for X in fam] for fam in families])
E0=d*4*L*L*np.sin(np.pi/L)**2

def fields(x,eps):
 V=np.repeat(V0[None],L,axis=0);V[0]=(np.eye(4)+np.einsum('i,iab->ab',x[:5],S))@V0
 V[1]=(np.eye(4)+eps*S[2])@V0
 T=np.repeat(np.eye(16)[None,None],L*4,axis=0).reshape(L,4,16,16)
 N=np.einsum('i,irab->rab',x[5:9],GF)
 for r in range(4):T[0,r]=expm(N[r])
 T[-1,0]=expm(x[9]*GF[0,0])
 derivatives=[]
 for j in range(5):derivatives.append(('coframe',0,np.einsum('ar,aij->rij',S[j]@V0,C)))
 for j in range(4):derivatives.append(('link',0,np.array([expm_frechet(N[r],GF[j,r],compute_expm=False) for r in range(4)])))
 derivatives.append(('link',7,np.array([GF[0,0]@T[7,0],np.zeros((16,16)),np.zeros((16,16)),np.zeros((16,16))])))
 return V,T,derivatives

def evaluate(x,eps):
 V,T,derivatives=fields(np.array(x),eps);CV=np.einsum('tar,aij->trij',V,C)
 eig=[];vectors=[];phases=[];modes=[]
 for k in itertools.product(range(L),repeat=3):
  phase=np.r_[1,np.exp(2j*np.pi*np.array(k)/L)];phases.append(phase);modes.append(k)
  dd=np.zeros((128,128),complex)
  for t in range(L):
   sl=slice(16*t,16*(t+1));sn=slice(16*((t+1)%L),16*((t+1)%L+1))
   dd[sl,sn]+=CV[t,0]@T[t,0]/ell
   dd[sl,sl]+=(sum(CV[t,r]@(phase[r]*T[t,r]-np.eye(16)) for r in range(1,4))-CV[t,0])/ell
  D=dd+dd.conj().T
  val,Q=eigh(D,check_finite=False,driver='evd');eig.append(val);vectors.append(Q)
 en=np.array(eig)**2;bb=1-alpha*en;ee=np.exp(m*np.log1p(-alpha*en));Z=ee.sum()
 occupied=abs(en-E0)<.25
 assert occupied.sum()==128,(occupied.sum(),eps)
 kap=ee/bb*(-1/Z+128*z*beta/(1-z+z*ee));ww=kap+occupied/128
 grad=np.zeros(10);gram_error=0.;prep_commutator_error=0.;projector_motion=0.
 for val,Q,occ,k in zip(eig,vectors,occupied,modes):
  if not occ.any():continue
  P=Q[:,occ]@Q[:,occ].conj().T
  us=[1,L-1] if sum(k)==0 else [0]
  Phi=np.hstack([np.kron(np.exp(2j*np.pi*u*np.arange(L)/L)[:,None]/np.sqrt(L),np.eye(16)) for u in us])
  assert Phi.shape[1]==occ.sum()
  W=P@Phi;g=Phi.conj().T@W;ev,B=eigh(g)
  Amp=W@(B*(1/np.sqrt(ev)))@B.conj().T/np.sqrt(128)
  gram_error=max(gram_error,float(np.max(abs(Amp.conj().T@Amp-np.eye(Amp.shape[1])/128))))
  rho=Amp@Amp.conj().T;Delta=(Q*val**2)@Q.conj().T
  prep_commutator_error=max(prep_commutator_error,float(np.max(abs(Delta@rho-rho@Delta))))
  projector_motion+=float(np.linalg.norm(P-Phi@Phi.conj().T,'fro')**2)

 for val,Q,w,phase in zip(eig,vectors,ww,phases):
  ED=(Q*(2*val*w))@Q.conj().T
  for j,(typ,t,dq) in enumerate(derivatives):
   sl=slice(16*t,16*(t+1));sn=slice(16*((t+1)%L),16*((t+1)%L+1))
   if typ=='coframe':
    off=dq[0]@T[t,0]/ell
    on=(sum(dq[r]@(phase[r]*T[t,r]-np.eye(16)) for r in range(1,4))-dq[0])/ell
   else:
    off=CV[t,0]@dq[0]/ell
    on=sum(CV[t,r]@dq[r]*phase[r] for r in range(1,4))/ell
   grad[j]+=2*np.real(np.trace(ED[sn,sl]@off)+np.trace(ED[sl,sl]@on))
 return grad,{'R':float(en[occupied].sum()/128),'Z':float(Z),'occupied':int(occupied.sum()),'Bmin':float(bb.min()),'fixed_RIGHT_Gram_error':gram_error,'preparation_commutator_error':prep_commutator_error,'Riesz_projector_motion_HS':float(np.sqrt(projector_motion))}

if __name__=='__main__':
 src=json.loads((ROOT/'02_REGISTRY/research/sources/d0_af_star_full_lattice_2026-10-17/NATIVE_SCALAR_FINITE_EXPLORATION.json').read_text())
 ks=[]
 for q in range(8):
  a=src['cases']['L8_q'+str(min(q,8-q))]['K'];K=np.array(a['real'])+1j*np.array(a['imag']);ks.append(K if q<=4 else K.conj())
 def hh(dist):return sum(np.exp(2j*np.pi*q*dist/8)*ks[q] for q in range(8)).real/8
 pos=[0]*9+[-1];idx=list(range(9))+[5]
 A=np.array([[hh(pos[i]-pos[j])[idx[i],idx[j]] for j in range(10)] for i in range(10)])
 bv=np.array([hh(pos[i]-1)[idx[i],2] for i in range(10)])
 response=-np.linalg.solve(A,bv)
 results=[]
 for eps in [0,1e-4,1e-5]:
  x=eps*response
  g,diagnostic=evaluate(x,eps)
  record={'eps':eps,'linear_response_max_source':float(abs(g).max()),'x':x.tolist(),**diagnostic};results.append(record);print(json.dumps(record),flush=True)
  if eps:
   for it in range(3):
    x-=np.linalg.solve(A/8,g)
    g,diagnostic=evaluate(x,eps)
    record={'eps':eps,'iteration':it,'max_source':float(abs(g).max()),'x':x.tolist(),**diagnostic};results.append(record);print(json.dumps(record),flush=True)
    if abs(g).max()<1e-11:break

 if '--output' in __import__('sys').argv:
  out=Path(__import__('sys').argv[__import__('sys').argv.index('--output')+1]);out.write_text(json.dumps({'status':'DIAGNOSTIC_FLOAT64','independent_actual_D_source':True,'full_modes':65536,'reference':128,'results':results,'scope':'Numerical diagnostic, not the interval nonsingularity proof or GR closure.'},indent=2)+'\n')
