#!/usr/bin/env python3
"""ONE true native K(9,11,13) Perron history reconstructs absolute Book edge pressure.
Executed independently on original 33/718 scene; numpy required.
No physical Cost/Info programme selection, Einstein coupling or GR promotion.
"""
import numpy as np

PHI=(1+5**.5)/2
LOGPHI=np.log(PHI)
N=33
zones=np.array([0]*9+[1]*11+[2]*13)
edges=[(u,v) for u in range(N) for v in range(N) if zones[u]!=zones[v]]
assert len(edges)==718
field=.41
theta=.25
I=np.array([.2*(v%5)+.09*np.sin(.6*(v+1)*field) for v in range(N)])
C=np.zeros((N,N))
K=np.zeros((N,N))
for u,v in edges:
    C[u,v]=1+.027*((3*u+7*v)%11)+.018*field*((u+3*v)%5)
    K[u,v]=PHI**(-(C[u,v]-theta*I[u]-(1-theta)*I[v]))
eig,U=np.linalg.eig(K)
j=np.argmax(eig.real)
lam=eig[j].real
r=U[:,j].real
if r.sum()<0:r=-r
r/=r.sum()
ev,L=np.linalg.eig(K.T)
ell=L[:,np.argmin(abs(ev-lam))].real
if ell.sum()<0:ell=-ell
pi=r*ell
pi/=pi.sum()
P=K*r[np.newaxis,:]/(lam*r[:,np.newaxis])
assert np.max(abs(P.sum(1)-1))<1e-12
# Use an explicit elementwise reduction here: some macOS BLAS builds emit
# spurious floating-point overflow warnings for this small finite row vector.
assert np.max(abs(np.sum(pi[:,None]*P,axis=0)-pi))<1e-12
price=C-theta*I[:,None]-(1-theta)*I[None,:]
valid=P>0
entropy=-np.sum(pi[:,None]*P*np.log(np.where(valid,P,1)))/LOGPHI
mean_cost=np.sum(pi[:,None]*P*price)
true_pressure=np.log(lam)/LOGPHI
assert abs(entropy-mean_cost-true_pressure)<1e-12
max_reconstruction_error=max(abs(-np.log(lam)/LOGPHI
                       -np.log(P[u,v])/LOGPHI
                       +np.log(r[v]/r[u])/LOGPHI-price[u,v])
                       for u,v in edges)
assert max_reconstruction_error<1e-12

# Native preparation is the ORIGINAL ONE-SIDED r, not stationary pi.
rng=np.random.default_rng(20261019)
steps=220000
cur=int(rng.choice(N,p=r))
counts=np.zeros((N,N),dtype=np.int64)
for _ in range(steps):
    nxt=int(rng.choice(N,p=P[cur]))
    counts[cur,nxt]+=1
    cur=nxt
occ=counts.sum(1)
Pobs=counts/np.maximum(occ[:,None],1)
active=counts>0
observed_entropy=-np.sum((counts[active]/steps)*np.log(Pobs[active]))/LOGPHI
observed_cost=np.sum(counts*price)/steps
observed_pressure=observed_entropy-observed_cost
assert abs(observed_pressure-true_pressure)<.03

# A true common cost shift changes pressure without changing P/F feedback.
shift=.27
shifted_K=PHI**(-shift)*K
shifted_lam=PHI**(-shift)*lam
assert abs(np.log(shifted_lam)/LOGPHI-(true_pressure-shift))<1e-12
assert np.max(abs((shifted_K*r[None,:]/(shifted_lam*r[:,None]))-P))<1e-12
print("PASS original 33/718 native Perron scene, unique pressure and edge cohomology")
print(f"true log_phi(lambda)={true_pressure:.12f}; entropy-minus-cost={entropy-mean_cost:.12f}")
print(f"ONE original history N={steps}: h={observed_entropy:.12f}, cost={observed_cost:.12f}, pressure={observed_pressure:.12f}")
print(f"one-history pressure error={abs(observed_pressure-true_pressure):.7g}; 718-edge reconstruction error={max_reconstruction_error:.3g}")
print("PASS common real Cost shift changes pressure, not normalized transition/F")
print("SCOPE GIVEN edge Cost/Info; compulsory full physical D0⇒GR OPEN")
