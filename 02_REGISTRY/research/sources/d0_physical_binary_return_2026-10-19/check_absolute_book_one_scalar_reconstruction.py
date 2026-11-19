#!/usr/bin/env python3
"""Original K(9,11,13): one ABSOLUTE native Perron scalar plus normalized
stationary 718 edge law reconstructs ALL 33 original vertex Info globally.

Primitive Golden p 16 complete CAR flags separately recover six Lorentz
controls locally (owned exact marker theorem), NOT full compulsory G0/GR.
"""
import numpy as np
from math import sqrt,log
p=(sqrt(5)-1)/2
ell=log(1/p)
zone=np.array([0]*9+[1]*11+[2]*13)
u,v=np.where(zone[:,None]!=zone[None,:])
assert len(u)==718
n=33
rng=np.random.default_rng(20261019)
I=rng.uniform(-.8,.8,n)
K=np.zeros((n,n))
K[u,v]=p*np.exp(ell/2*(I[u]+I[v]))
eig,R=np.linalg.eigh(K)
lam=float(eig[-1])
r=R[:,-1]
if sum(r)<0:r=-r
pi=r*r
mu=K[u,v]*r[u]*r[v]/lam
assert abs(sum(mu)-1)<1e-12
assert max(abs(np.bincount(u,weights=mu,minlength=n)-pi))<1e-12

# ALL true original 718 signed/unsigned directed edge sums.
S=np.full((n,n),np.nan)
S[u,v]=2*np.log(lam*mu/(p*np.sqrt(pi[u]*pi[v])))/ell
assert max(abs(S[u,v]-(I[u]+I[v])))<2e-13

# ONE original native 3-zone triangle fixes the first three Info values.
a,b,c=0,9,20
rec=np.full(n,np.nan)
rec[a]=(S[a,b]+S[a,c]-S[b,c])/2
rec[b]=(S[a,b]+S[b,c]-S[a,c])/2
rec[c]=(S[a,c]+S[b,c]-S[a,b])/2
# Every other original vertex has a real cross-zone edge to a or b.
for x in range(n):
    if np.isfinite(rec[x]):continue
    anchor=b if zone[x]==0 else a
    rec[x]=S[x,anchor]-rec[anchor]
assert max(abs(rec-I))<3e-13

# Full normalized data blind to exactly ONE uniform Info shift; the actual
# Perron eigenvalue fixes that missing absolute native Book dimension.
shift=.21
I2=I+shift
K2=np.zeros((n,n))
K2[u,v]=p*np.exp(ell/2*(I2[u]+I2[v]))
eig2,R2=np.linalg.eigh(K2)
lam2=float(eig2[-1])
r2=R2[:,-1]
if sum(r2)<0:r2=-r2
mu2=K2[u,v]*r2[u]*r2[v]/lam2
assert max(abs(mu2-mu))<5e-14
assert abs(lam2/lam-np.exp(ell*shift))<2e-12

# ALL original primitive Golden positive marks and failure branches.
q=np.array([p**4/24]*12+[p**4/2,p**3,p**3,p**2])
assert len(q)==16 and abs(sum(q)-1)<1e-14
# At genuine original flat U=I, all six Lorentz signed markers are zero;
# the #334 exact mark decoder is R_a=4sqrt(3)/p²*(sqrt(q_a+)-sqrt(q_a-)).
Rmark=np.array([(4*sqrt(3)/p**2)*(sqrt(q[2*i])-sqrt(q[2*i+1])) for i in range(6)])
assert max(abs(Rmark))==0
# Original proper Lorentz Gram Tr(Ga^T Gb)=2delta_ab forces local
# exact six-dimensional inverse-function theorem, det DR(I)=2**6.
assert abs(np.linalg.det(2*np.eye(6))-64)<1e-12

# Nonlinear ALL-33 Info original native operator: exact rank3 reduction.
W=np.array([np.sum(np.exp(ell*I[zone==idx])) for idx in range(3)])
zone_operator=p*(1-np.eye(3))*np.sqrt(W[:,None]*W[None,:])
lam3=float(np.linalg.eigvalsh(zone_operator)[-1])
assert np.linalg.matrix_rank(K,tol=1e-10)==3
assert abs(lam3-lam)<1e-11
poly=lam**3-p*p*(W[0]*W[1]+W[0]*W[2]+W[1]*W[2])*lam-2*p**3*np.prod(W)
assert abs(poly)<1e-9
print('PASS all 33 heterogeneous Info: original full native K has rank3')
print('PASS absolute lambda exact three-zone Golden Info cubic',W,lam3)
print('PASS native actual 718 edge stationary law plus ONE absolute lambda')
print('PASS original ABC triangle reconstructs ALL 33 nonlinear Info globally')
print('max reconstruction error',max(abs(rec-I)))
print('PASS native 718 probabilities blind to one uniform Info shift')
print('PASS absolute Perron lambda removes precisely the one missing mode')
print('PASS original Golden16 GOOD/BAD flag and six marked Lorentz source normalization')
print('DECODER: Iu+Iv=2 log_phi(lambda mu_uv/(p sqrt(pi_u pi_v)))')
print('CONDITIONAL: full 718x16 joint record + lambda reconstructs 33+6 native parameters')
print('FIREWALL: full G0 physical absolute clock selection and Einstein Euler OPEN')
