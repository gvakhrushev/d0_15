"""Complete literal action and every one of its 24 local connection rows."""
import json,numpy as np
from pathlib import Path
from itertools import combinations
from scipy.linalg import logm
P=list(combinations(range(4),2)); eta=np.diag([1.,-1.,-1.,-1.]); eye=np.eye(4)
GEN=[]
for a,b in P:
 X=np.zeros((4,4));X[a,b]=1;X[b,a]=-eta[a,a]*eta[b,b];GEN.append(X)
GEN=np.array(GEN);G2=np.diag([eta[a,a]*eta[b,b] for a,b in P]);STAR=np.zeros((6,6))
for a,(b,sg) in {(0,1):((2,3),-1),(0,2):((1,3),1),(0,3):((1,2),-1),(1,2):((0,3),1),(1,3):((0,2),-1),(2,3):((0,1),1)}.items():STAR[P.index(b),P.index(a)]=sg

def wedge(u,v):return np.array([u[a]*v[b]-u[b]*v[a] for a,b in P])
def weight(E,r,s):
 u,v=[a for a in range(4) if a not in (r,s)];seq=[r,s,u,v];sign=(-1)**sum(seq[i]>seq[j] for i,j in combinations(range(4),2))
 return sign*wedge(E[:,u],E[:,v])@G2@STAR

def links(A):
 X=np.einsum('nrk,kab->nrab',A.reshape(-1,4,6),GEN)
 return np.linalg.solve(eye-X/2,eye+X/2)

def residual(E,A,return_metric=False):
 L=len(E);U=links(A); Ui=eta@U.swapaxes(-1,-2)@eta; out=np.zeros((L,4,6)); cost=0.;metric=np.zeros((L,10));
 for n in range(L):
  for r,s in P:
   ids=[(n,r,1),((n+(r==1))%L,s,1),((n+(s==1))%L,r,-1),(n,s,-1)]
   fac=[U[m,a] if sig==1 else Ui[m,a] for m,a,sig in ids]
   prefixes=[eye]
   for F in fac:prefixes.append(prefixes[-1]@F)
   suff=[None]*5;suff[4]=eye
   for i in range(3,-1,-1):suff[i]=fac[i]@suff[i+1]
   plaquette=prefixes[-1];pi=eta@plaquette.T@eta; odd=(plaquette-pi)/2
   wt=weight(E[n],r,s);K=np.zeros((4,4))
   for k,(a,b) in enumerate(P):K[a,b]=wt[k]*eta[b,b]
   cost+=np.sum(K*odd)
   KP=(K+pi.T@K@pi.T)/2
   for i,(m,a,sig) in enumerate(ids):
    d=prefixes[i].T@KP@suff[i+1].T
    d=fac[i].T@d if sig==1 else -d@fac[i].T
    out[m,a]+=np.einsum('ab,kab->k',d,GEN)
   if return_metric:
    gi=np.linalg.inv(E[n].T@eta@E[n]);u,v=[k for k in range(4) if k not in (r,s)];seq=[r,s,u,v];sign=(-1)**sum(seq[i]>seq[j] for i,j in combinations(range(4),2));cc=np.array([(odd@eta)[a,b] for a,b in P])
    for k,(a,b) in enumerate(( (a,b) for a in range(4) for b in range(a,4))):
     V=np.zeros((4,4));V[a,b]=V[b,a]=1; dE=E[n]@gi@V/2
     dwt=sign*(wedge(dE[:,u],E[n][:,v])+wedge(E[n][:,u],dE[:,v]))@G2@STAR
     metric[n,k]+=dwt@cc
 return (out.reshape(L,24),cost,metric) if return_metric else out.reshape(L,24)

from algebra import inverse_coefficients
from functools import lru_cache
@lru_cache(maxsize=1)
def numeric_inverse_coefficients():
    return {k:np.array(mat.tolist(),dtype=float) for k,mat in inverse_coefficients().items()}
def inverse(v):
 L=len(v);nvec=sum(np.roll(v,-k,axis=0)@B.T for k,B in numeric_inverse_coefficients().items())
 den=14+2*np.cos(4*np.pi*np.arange(L)/L)
 return np.fft.ifft(np.fft.fft(nvec,axis=0)/den[:,None],axis=0).real

