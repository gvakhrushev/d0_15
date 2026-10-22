#!/usr/bin/env python3
"""Original CAR16 full128 no-reset two-tick fine archive and Poisson smoke.
Numerical controls only; not physical HJR or GR closure.
"""
import json
import math
import sys
from pathlib import Path
import numpy as np

sys.path.insert(0,str(Path(__file__).resolve().parent.parent/"d0_native65_causal_source_2026-10-22"))
from native_excerpt import native
p=(math.sqrt(5)-1)/2
K,dK=native(2*math.atanh(1/9),.6,(1j,1j,-1,-1j))
I=np.eye(16,dtype=complex)
Delta=(I-K[0])/(2*p*p)
inv=np.linalg.inv(Delta)
rho=inv/np.trace(inv)
def phi(X):
    return np.einsum("aij,jk,alk->il",K,X,K.conj(),optimize=True)
E=np.einsum("aij,aik->ajk",K.conj(),K,optimize=True)
X=np.einsum("aij,jk,alk->ail",K,rho,K.conj(),optimize=True)
P1=np.maximum(np.trace(X,axis1=1,axis2=2).real,0)
P2=np.maximum(np.einsum("aij,bji->ab",X,E,optimize=True).real,0)
def h(v):
    y=v.ravel()
    y=y[y>1e-20]
    return float(-np.dot(y,np.log(y)))
checks=[]
def verify(x,desc):
    if not x:raise ArithmeticError(desc)
    checks.append(desc)
verify(np.linalg.norm(phi(rho)-rho)<1e-11,"native stationary state")
verify(abs(P1.sum()-1)<1e-11,"complete 128 output normalization")
verify(abs(P2.sum()-1)<1e-11,"complete 128x128 no-reset normalization")
verify(np.max(np.abs(P2.sum(axis=1)-P1))<1e-11,"physical prefix marginal")
h1,h2=h(P1),h(P2)
mutual=2*h1-h2
verify(-1e-11<mutual<math.log(16),"finite DATA past/future mutual information")
C=1+sum(P1[1::2])
s1=C-h1/math.log(1/p)
s2=2*C-h2/math.log(1/p)
verify(abs(s1-.7283481307600606)<1e-9,"original one-tick Cost-Info")
verify(abs(s2-1.4566962628734839)<1e-9,"original two-tick Cost-Info")
Deltaj=-dK[0]/(2*p*p)
invj=-inv@Deltaj@inv
drho=invj/np.trace(inv)-inv*np.trace(invj)/(np.trace(inv)**2)
Dphi=np.einsum("aij,jk,alk->il",dK,rho,K.conj(),optimize=True)
Dphi+=np.einsum("aij,jk,alk->il",K,rho,dK.conj(),optimize=True)
poisson=drho-phi(drho)-Dphi
verify(np.linalg.norm(poisson)<1e-10,"full native Poisson first-source")
print(json.dumps({"status":"NUMERIC_SMOKE_ONLY","checks":len(checks),
  "H1_natural":h1,"H2_natural":h2,"adjacent_MI_natural":mutual,
  "cost1_Golden":C,"net1_Golden":s1,"net2_Golden":s2,
  "poisson_source_residual":float(np.linalg.norm(poisson)),
  "physical_Book03_GR_closed":False},indent=2))
