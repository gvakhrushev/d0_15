#!/usr/bin/env python3
"""Original Book Hessian Schur: future32 + reversal-even326 + reversal-odd327.
Three genuine primitive 718-edge Cost directions. Research only, no GR.
"""
import math
import numpy as np
n=(9,11,13)
z=np.repeat(np.arange(3),n)
edges=[(u,v) for u in range(33) for v in range(u+1,33) if z[u]!=z[v]]
D=edges+[(v,u) for u,v in edges]
assert len(D)==718
M=np.sqrt(np.outer(n,n)).astype(float)
np.fill_diagonal(M,0)
v,W=np.linalg.eigh(M);rho=v[-1];rr=W[:,-1]
if rr.sum()<0:rr=-rr
r=np.array([rr[z[u]]/math.sqrt(n[z[u]]) for u in range(33)])
pi=r*r
mu=np.array([r[u]*r[v]/rho for u,v in D])
P=np.zeros((33,33))
J0=np.zeros((718,33));J1=np.zeros((718,33))
for j,(u,v) in enumerate(D):
    P[u,v]=mu[j]/pi[u]
    J0[j,u]=math.sqrt(mu[j]/pi[u])
    J1[j,v]=math.sqrt(mu[j]/pi[v])
QA=np.eye(718)-J0@J0.T
X=QA@J1
F=X.T@X
assert np.linalg.matrix_rank(F,tol=1e-10)==32
Fpinv=np.linalg.pinv(F,rcond=1e-10)
ell=math.log((1+math.sqrt(5))/2)
cycle={(0,1),(1,2),(2,0)}
sources={
 'reversal_even_all_AB':np.array([float({z[u],z[v]}=={0,1}) for u,v in D]),
 'reversal_even_local_0_9':np.array([float({u,v}=={0,9}) for u,v in D]),
 'reversal_odd_CP':np.array([1. if (z[u],z[v]) in cycle else -1. for u,v in D]),
}
def split(d):
    c=mu@d
    m=np.zeros(33)
    for j,(u,v) in enumerate(D):m[u]+=mu[j]*d[j]/pi[u]
    m-=c
    xi=np.linalg.solve(np.eye(33)-P+np.outer(np.ones(33),pi),m)
    g=np.array([math.sqrt(mu[j])*(d[j]-c-xi[u]+xi[v]) for j,(u,v) in enumerate(D)])
    assert np.linalg.norm(J0.T@g)<1e-10
    f=X@(Fpinv@(X.T@g))
    dark=g-f
    assert np.linalg.norm(J0.T@dark)<1e-10
    assert np.linalg.norm(J1.T@dark)<1e-10
    reverse=np.r_[dark[359:],dark[:359]]
    even=(dark+reverse)/2
    odd=(dark-reverse)/2
    out=[ell*(c@c) for c in (g,f,even,odd)]
    assert abs(out[0]-sum(out[1:]))<5e-12
    return out,g
out={}
for name,d in sources.items():out[name]=split(d)[0]
assert abs(out['reversal_even_all_AB'][0]-.1297284254564436)<1e-11
assert out['reversal_even_all_AB'][2]<1e-18 and out['reversal_even_all_AB'][3]<1e-18
assert abs(out['reversal_even_local_0_9'][2]-.0013000035359633177)<1e-11
assert out['reversal_even_local_0_9'][3]<1e-18
assert abs(out['reversal_odd_CP'][0]-.4763744515526456)<1e-11
assert out['reversal_odd_CP'][1]<1e-18 and out['reversal_odd_CP'][2]<1e-18
assert abs(split(sources['reversal_even_local_0_9'])[1]@
           split(sources['reversal_odd_CP'])[1])<1e-11
print('PASS native718 original Book historical Schur: 32 + 326 + 327')
for name,x in out.items():print(name, 'total/future/even/odd',x)
print('FIREWALL: scalar macro Book source only; no full128 or GR')
