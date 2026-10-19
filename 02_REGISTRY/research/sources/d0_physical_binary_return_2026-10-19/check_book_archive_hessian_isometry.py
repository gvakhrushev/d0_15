#!/usr/bin/env python3
"""Native full718 scalar Book Hessian IS original archive Fisher metric.

Replays original 33->718 current/future isometries, genuine balanced-flow
bijection, cost-source Schur and rank-32 future-reachability test.
Not a native full4D Einstein action or physically admitted Cost compiler.
"""
import numpy as np
from math import log,sqrt
phi=(1+sqrt(5))/2; p=1/phi;ell=log(phi)
verts=range(33)
zone={v:(0 if v<9 else 1 if v<20 else 2) for v in verts}
edges=[(u,v) for u in verts for v in verts if zone[u]!=zone[v]]
assert len(edges)==718
K=np.zeros((33,33))
for u,v in edges:K[u,v]=p
spectrum,vec=np.linalg.eigh(K)
lam=spectrum[-1];r=vec[:,-1]
if r.sum()<0:r=-r
pi=r*r
P=K*r[None,:]/(lam*r[:,None])
mu=np.array([pi[u]*P[u,v] for u,v in edges])
assert abs(mu.sum()-1)<1e-12
S=np.zeros((718,33));J1=np.zeros((718,33))
for i,(u,v) in enumerate(edges):
    S[i,u]=sqrt(P[u,v])
    J1[i,v]=sqrt(mu[i]/pi[v])
assert np.linalg.norm(S.T@S-np.eye(33))<1e-12
assert np.linalg.norm(J1.T@J1-np.eye(33))<1e-12
Q=lambda x:x-S@(S.T@x)
T=S.T@J1
R=Q(J1)
assert np.linalg.norm(R.T@R-(np.eye(33)-T.T@T))<1e-12
singular,sigma,vt=np.linalg.svd(R,full_matrices=False)
assert sigma[-1]<1e-10 and sigma[-2]>.5
assert (sigma>1e-8).sum()==32

fundamental=np.linalg.inv(np.eye(33)-P+np.outer(np.ones(33),pi))
def inverse(eta):
    assert np.linalg.norm(S.T@eta)<1e-10
    b=np.zeros(33)
    for j,(u,v) in enumerate(edges):b[v]+=sqrt(mu[j])*eta[j]
    a=b@fundamental
    z=np.array([a[u]*P[u,v]+sqrt(mu[j])*eta[j]
                for j,(u,v) in enumerate(edges)])
    source=np.zeros(33);target=np.zeros(33)
    for j,(u,v) in enumerate(edges):source[u]+=z[j];target[v]+=z[j]
    assert abs(z.sum())<1e-10
    assert np.linalg.norm(source-target)<1e-10
    assert np.linalg.norm(Q(z/np.sqrt(mu))-eta)<1e-10
    return z,a

def force(ds):
    m=np.zeros(33)
    for j,(u,v) in enumerate(edges):m[u]+=P[u,v]*ds[j]
    pot=fundamental@m
    g=np.array([sqrt(mu[j])*(ds[j]+pot[v])
                for j,(u,v) in enumerate(edges)])
    return Q(g)

rng=np.random.default_rng(8101)
for _ in range(4):
    eta=Q(rng.standard_normal(718))
    z,a=inverse(eta)
    book_hessian=(sum(z*z/mu)-sum(a*a/pi))/ell
    assert abs(book_hessian-(eta@eta)/ell)<2e-10
print('PASS exact Book history Hessian = native invisible Q_A norm on all balanced tangents')
print('PASS reconstruct every 685-dimensional archive innovation by native finite Markov Poisson solve')

ds=np.array([1. if {zone[u],zone[v]}=={0,1} else 0.
             for u,v in edges])
G=force(ds)
for _ in range(3):
    eta=Q(rng.standard_normal(718))
    z,_=inverse(eta)
    assert abs(z@ds-eta@G)<1e-10
hess_correction=ell*(G@G)
assert abs(hess_correction-.1297284254564436)<3e-12
print('PASS mixed primitive edge-Cost source = genuine archived force')
print('PASS negative native history Schur = -ln(phi)||G||²:',-hess_correction)

def future_remainder(g):
    projected=singular[:,:32]@(singular[:,:32].T@g)
    return np.linalg.norm(g-projected)
assert future_remainder(G)<2e-12
print('PASS native class AB Cost source 100% captured by original rank32 future archive')

alpha=rng.standard_normal(33);beta=rng.standard_normal(33)
sep=force(np.array([alpha[u]+beta[v] for u,v in edges]))
assert future_remainder(sep)<2e-12
print('PASS every tested endpoint-separable original Cost source is future-readable')

single=force(np.array([1. if (u,v) in ((0,9),(9,0)) else 0.
                       for u,v in edges]))
res=future_remainder(single)
assert res>.05
print('PASS one genuine localized undirected primitive Cost pair is NOT future-readable')
print('Residual=',res,'invisible squared-force fraction=',res*res/(single@single))
print('SCOPE original scalar Book archive, not full native 4D Lorentz/CAR Einstein')
