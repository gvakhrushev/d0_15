#!/usr/bin/env python3
"""Original 718-edge Book CP Cost: exact harmonic gauge normal form.
No actual full128/GR field mapping or neutrino alpha identification.
"""
import math
import numpy as np
n=(9,11,13)
zone=np.repeat(np.arange(3),n)
M=np.sqrt(np.outer(n,n)).astype(float)
np.fill_diagonal(M,0)
eig,Q=np.linalg.eigh(M)
rho=eig[-1]
v=Q[:,-1]
if v.sum()<0:v=-v
r=np.array([v[zone[u]]/math.sqrt(n[zone[u]]) for u in range(33)])
mu0=np.outer(r,r)/rho
pairs=((0,1),(1,2),(0,2))
q={ij:sum(mu0[u,w]+mu0[w,u] for u in range(33) for w in range(u+1,33)
          if (zone[u],zone[w])==ij) for ij in pairs}
resistance=sum(1/a for a in q.values())
hAB,hBC,hCA=3/(resistance*q[0,1]),3/(resistance*q[1,2]),3/(resistance*q[0,2])
xi=[0,-(1-hAB),1-hCA]
assert abs(hAB+hBC+hCA-3)<1e-12
cycle={(0,1),(1,2),(2,0)}
h={(0,1):hAB,(1,2):hBC,(2,0):hCA}
d=np.zeros((33,33));dh=np.zeros((33,33)); mask=np.zeros((33,33),dtype=bool)
for u in range(33):
    for w in range(33):
        i,j=zone[u],zone[w]
        if i==j:continue
        mask[u,w]=True
        if (i,j) in cycle:d[u,w]=1;dh[u,w]=h[i,j]
        else:d[u,w]=-1;dh[u,w]=-h[j,i]
        assert abs(d[u,w]-dh[u,w]-(xi[i]-xi[j]))<1e-13
assert np.max(abs(np.sum(mu0*dh,axis=0)))<1e-12
assert np.max(abs(np.sum(mu0*dh,axis=1)))<1e-12
ell=math.log((1+math.sqrt(5))/2)
assert abs(sum((mu0*dh*dh).ravel())-9/resistance)<1e-12

def stationary(K):
    eigen,R=np.linalg.eig(K);j=np.argmax(eigen.real);lam=eigen[j].real
    rr=R[:,j].real
    if rr.sum()<0:rr=-rr
    eigen,L=np.linalg.eig(K.T);ll=L[:,np.argmin(abs(eigen-lam))].real
    if ll.sum()<0:ll=-ll
    return lam,ll[:,None]*K*rr[None,:]/(lam*(ll@rr))

for eps in (-0.6,-0.2,0.,0.07,0.4,0.8):
    A=np.zeros((33,33));B=np.zeros((33,33))
    A[mask]=np.exp(-ell*(1+eps*d[mask]))
    B[mask]=np.exp(-ell*(1+eps*dh[mask]))
    D=np.exp(-ell*eps*np.array([xi[i] for i in zone]))
    assert np.max(abs(A-D[:,None]*B/D[None,:]))<5e-14
    lamA,flowA=stationary(A);lamB,flowB=stationary(B)
    assert abs(lamA-lamB)<2e-12
    assert np.max(abs(flowA-flowB))<3e-13
print('PASS ORIGINAL_BOOK_CP_HARMONIC_GAUGE all six epsilon finite')
print('native q=',q,'harmonic weights=',hAB,hBC,hCA)
print('Book curvature=',-9*ell/resistance)
print('FIREWALL: scalar native Book Cost gauge, not full physical GR source')
