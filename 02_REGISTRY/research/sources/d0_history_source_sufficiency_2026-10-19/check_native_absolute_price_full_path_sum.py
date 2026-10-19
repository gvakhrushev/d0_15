#!/usr/bin/env python3
"""One *finite* complete original K(9,11,13) Book pressure and source.

All 718 positive native supported edges, 33 true Perron terminal values.
Research-only: a given Book scalar K and genuine one-sided r are inputs,
not yet proven physically selected by full G0/Book 03.
"""
from math import log,sqrt
import numpy as np
phi=(1+sqrt(5.0))/2.0; ell=log(phi)
zones=np.array([0]*9+[1]*11+[2]*13)
support=zones[:,None]!=zones[None,:]
assert int(support.sum())==718
u,v=np.indices((33,33))
def matrix(y):
    C=1.28+.1*np.sin(.117*(u+1)+.167*(v+1))
    C=C+.03*y*np.cos(.21*(u+1)-.13*(v+1))
    I=.06*np.sin(.23*(np.arange(33)+1))+.09*y*np.cos(.14*(np.arange(33)+2))
    return np.where(support,np.exp(-ell*(C-.4*I[:,None]-.6*I[None,:])),0.0)
def perron(y):
    K=matrix(y)
    lamall,vec=np.linalg.eig(K)
    k=int(np.argmax(lamall.real)); lam=float(lamall[k].real)
    r=vec[:,k].real
    if np.sum(r)<0:r=-r
    assert np.min(r)>0
    r=r/np.sum(r)
    assert np.max(np.abs(K@r-lam*r))<1e-11
    return K,lam,r
def rate(y,n):
    K,lam,r=perron(y)
    # Complete finite original weighted walks with terminal factor r_end.
    # Matrix multiplication sums EVERY allowed path, not a sample.
    vec=r.copy()
    for _ in range(n): vec=K@vec
    B=float(np.sum(vec))
    assert abs(B-lam**n)<2e-9*max(1.0,lam**n)
    return -log(B)/(ell*n),-log(lam)/ell
for y in (-.15,-.07,0.0,.09,.19):
    for n in (1,2,3,4,6,10):
        a,b=rate(y,n)
        assert abs(a-b)<2e-12
    h=1e-5
    for n in (1,2,5):
        D=(rate(y+h,n)[0]-rate(y-h,n)[0])/(2*h)
        Dlam=(rate(y+h,n)[1]-rate(y-h,n)[1])/(2*h)
        assert abs(D-Dlam)<2e-8
    print("PASS y=%.2f, full all-718 PF-terminated walk depths 1/2/3/4/6/10 and moving first sources"%y)
print("PASS exact finite absolute pressure from original Perron terminal history, no infinite-depth limit")
print("FIREWALL: physical same-run oldRIGHT/PF prep and compulsory Book scalar K must still be selected")
