import numpy as np
from scipy.linalg import expm
from math import log,sqrt
p=(sqrt(5)-1)/2; ELL=log(1/p)
order=(0,2,3,1)
C=[]
for r in range(4):
 m=np.zeros((16,16),complex)
 for bits in range(16):
  if not (bits>>r)&1:
   m[bits|1<<r,bits]=(-1)**sum((bits>>j)&1 for j in order[:order.index(r)])
 C.append(m)
def adj(a):return a.conj().T
def sqrtpsd(A):
 a,w=np.linalg.eigh((A+adj(A))/2)
 assert min(a)>0
 return (w*np.sqrt(a))@adj(w)
def maker(theta):
 I=np.eye(16);X=np.zeros((4,4));X[0,1]=X[1,0]=1
 GX=sum((X[i,j]*C[i]@adj(C[j]) for i in range(4) for j in range(4)),np.zeros((16,16),complex))
 U=expm(theta*GX);nu=.6;phases=(1j,1j,-1.,-1j);words=[]
 for r in range(4):
  fixed=nu*C[r]
  transformed=fixed@(U if r==1 else I)*phases[r]
  L=sqrtpsd(I-transformed@adj(transformed));R=sqrtpsd(I-adj(transformed)@transformed)
  L0=sqrtpsd(I-fixed@adj(fixed));R0=sqrtpsd(I-adj(fixed)@fixed)
  for pair in ((transformed,L),(adj(transformed),R),(-fixed,-L0),(-adj(fixed),-R0)):
   words.extend((pair,pair))
 assert len(words)==32
 N=[]
 for label in range(32):
  for c in range(2):
   N.append(sum(((-1)**((label&j).bit_count()&1)*words[j][c] for j in range(32)),np.zeros((16,16),complex))/32)
 A=N[0]
 assert np.linalg.norm(A-adj(A))<1e-12
 K=[]
 for j,n in enumerate(N):
  common=adj(n)@A
  K.extend(((I if j==0 else np.zeros_like(I))-2*p*p*common,-2*p*sqrt(p)*common))
 assert np.linalg.norm(sum((adj(x)@x for x in K),np.zeros_like(I))-I)<1e-11
 return np.array(K)
def calc(th):
 K=maker(th)
 q=np.einsum('kij,kij->k',K.conj(),K).real/16
 assert abs(sum(q)-1)<1e-12
 H=-sum(x*log(x)/ELL for x in q if x>0)
 flag=np.array([sum(q[0::2]),sum(q[1::2])]);hf=-sum(x*log(x)/ELL for x in flag if x>0)
 nonblank=np.array([[q[2*j],q[2*j+1]] for j in range(1,64)])
 return H,hf,flag,nonblank,q

def psqrt_with_derivative(S,dS):
    eig,V=np.linalg.eigh((S+adj(S))/2)
    assert eig.min()>0.1
    rt=np.sqrt(eig)
    R=(V*rt)@adj(V)
    local=adj(V)@dS@V
    dR=V@(local/(rt[:,None]+rt[None,:]))@adj(V)
    return R,dR

def analytic_native(theta):
    I=np.eye(16,dtype=complex)
    X=np.zeros((4,4));X[0,1]=X[1,0]=1
    GX=sum((X[i,j]*C[i]@adj(C[j]) for i in range(4) for j in range(4)),np.zeros((16,16),complex))
    U=expm(theta*GX); dU=GX@U
    nu=.6;phases=(1j,1j,-1.,-1j); words=[]; dwords=[]
    for r in range(4):
      fixed=nu*C[r]
      P=fixed@(U if r==1 else I)*phases[r]
      dP=fixed@dU*phases[r] if r==1 else np.zeros_like(P)
      L,dL=psqrt_with_derivative(I-P@adj(P),-dP@adj(P)-P@adj(dP))
      R,dR=psqrt_with_derivative(I-adj(P)@P,-adj(dP)@P-adj(P)@dP)
      L0=sqrtpsd(I-fixed@adj(fixed));R0=sqrtpsd(I-adj(fixed)@fixed)
      pairs=((P,L),(adj(P),R),(-fixed,-L0),(-adj(fixed),-R0))
      dpairs=((dP,dL),(adj(dP),dR),(np.zeros_like(P),np.zeros_like(P)),(np.zeros_like(P),np.zeros_like(P)))
      for pair,dpair in zip(pairs,dpairs):
       words.extend((pair,pair));dwords.extend((dpair,dpair))
    N=[];dN=[]
    for label in range(32):
      for c in range(2):
       signs=np.array([(-1)**((label&j).bit_count()&1) for j in range(32)])
       N.append(sum((signs[j]*words[j][c] for j in range(32)),np.zeros((16,16),complex))/32)
       dN.append(sum((signs[j]*dwords[j][c] for j in range(32)),np.zeros((16,16),complex))/32)
    A=N[0];dA=dN[0];K=[];dK=[]
    for j,(n,dn) in enumerate(zip(N,dN)):
      shared=adj(n)@A
      dshared=adj(dn)@A+adj(n)@dA
      K.extend(((I if j==0 else np.zeros_like(I))-2*p*p*shared,-2*p*sqrt(p)*shared))
      dK.extend((-2*p*p*dshared,-2*p*sqrt(p)*dshared))
    K=np.array(K);dK=np.array(dK)
    q=np.einsum('kij,kij->k',K.conj(),K).real/16
    dq=2*np.einsum('kij,kij->k',K.conj(),dK).real/16
    assert abs(q.sum()-1)<1e-12 and abs(dq.sum())<1e-11
    assert np.linalg.norm(sum((adj(k)@dk+adj(dk)@k for k,dk in zip(K,dK)),np.zeros_like(I)))<1e-10
    pos=q>1e-17
    assert np.max(abs(dq[~pos]))<1e-11
    H=-sum(q[pos]*np.log(q[pos]))/ELL
    dH=-sum(dq[pos]*np.log(q[pos]))/ELL
    xk=(q[2:]).reshape((63,2)).sum(1)
    dxk=(dq[2:]).reshape((63,2)).sum(1)
    assert max(abs(q[2::2]-p*p*xk))<2e-14 and max(abs(q[3::2]-p*xk))<2e-14
    assert max(abs(dq[2::2]-p*p*dxk))<2e-14 and max(abs(dq[3::2]-p*dxk))<2e-14
    grouped=np.r_[q[:2],xk]
    dgrouped=np.r_[dq[:2],dxk]
    mask=grouped>1e-17
    golden_entropy=-(p*p*log(p*p)+p*log(p))/ELL
    H2=-np.sum(grouped[mask]*np.log(grouped[mask]))/ELL+xk.sum()*golden_entropy
    dH2=-np.sum(dgrouped[mask]*np.log(grouped[mask]))/ELL+dxk.sum()*golden_entropy
    assert abs(H-H2)<1e-13 and abs(dH-dH2)<1e-11
    mean_port=1+q[1::2].sum(); dC=dq[1::2].sum()
    return {'theta':theta,'H':H,'dH_analytic':dH,'H_decomposed':H2,'dH_decomposed':dH2,'dH_mean_minus_pressure':dH/2,
            'mean_port_cost':mean_port,'d_mean_port_cost':dC,'d_CQ_price':dC-dH,
            'grouped_positive_bins':int(mask.sum()),'total_positive_outcomes':int(pos.sum()),
            'nonblank_total':float(xk.sum()),'nonblank_conditional_port0':float(p*p),
            'nonblank_conditional_port1':float(p)}

if __name__=='__main__':
 import json
 for th in (.04,.08,.12):
  ans=analytic_native(th)
  for dh in (1e-4,1e-5,1e-6):
   hp=calc(th+dh)[0];hm=calc(th-dh)[0]
   ans['secant_error_'+str(dh)]=float((hp-hm)/(2*dh)-ans['dH_analytic'])
  print(json.dumps(ans,indent=2))
