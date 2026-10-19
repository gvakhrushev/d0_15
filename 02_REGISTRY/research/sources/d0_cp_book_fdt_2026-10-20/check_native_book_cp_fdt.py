#!/usr/bin/env python3
"""Exact original K(9,11,13) CP Book cycle: full 718-edge FDT.
Scope: original scalar Book flow macro-action only; not full128, neutrino or GR.
"""
import math
import sympy as sp
import numpy as np

N = (9, 11, 13)
phi = (1 + math.sqrt(5)) / 2
ell = math.log(phi)
x, p, q = sp.symbols("x p q", nonzero=True)
M = p * sp.Matrix([[0, 11*q, 13/q], [9/q, 0, 13*q], [9*q, 11/q, 0]])
assert sp.simplify((x*sp.eye(3)-M).det()
    - (x**3 - 359*p*p*x - 1287*p**3*(q**3 + q**-3))) == 0

zones = np.repeat(np.arange(3), N)
edges = [(u,v) for u in range(33) for v in range(33) if zones[u] != zones[v]]
assert len(edges) == 718
cycle = {(0,1), (1,2), (2,0)}
d = lambda i,j: 1 if (i,j) in cycle else -1

def scene(e):
    K = np.zeros((33,33), dtype=float)
    for u,v in edges:
        K[u,v] = math.exp(-ell*(1+e*d(zones[u],zones[v])))
    vals,R = np.linalg.eig(K)
    k = np.argmax(vals.real)
    lam = vals[k].real
    r = R[:,k].real
    if r.sum() < 0: r = -r
    vals,L = np.linalg.eig(K.T)
    l = L[:,np.argmin(abs(vals-lam))].real
    if l.sum() < 0: l = -l
    mu = (l[:,None]*K*r[None,:])/(lam*np.dot(l,r))
    pi = mu.sum(axis=1)
    assert np.max(abs(pi-mu.sum(axis=0))) < 1e-12
    assert abs(mu.sum()-1) < 1e-13
    mean = sum(mu[u,v]*d(zones[u],zones[v]) for u,v in edges)
    entropy = sum(mu[u,v]*math.log(mu[u,v]/mu[v,u]) for u,v in edges)
    assert abs(entropy+2*ell*e*mean) < 1e-11
    return mu,pi,mean,entropy,lam

zero = scene(0)
qmass = []
for i,j in ((0,1),(1,2),(0,2)):
    qmass.append(sum(zero[0][u,v] for u,v in edges
                     if {zones[u],zones[v]} == {i,j}))
resistance = sum(1/qv for qv in qmass)
rho = zero[-1]*phi
second = -23166*ell/(rho*(3*rho**2-359))
assert abs(second+9*ell/resistance) < 1e-13
jprime = second/3
z = {(u,v):jprime*d(zones[u],zones[v])/(2*N[zones[u]]*N[zones[v]])
     for u,v in edges}
for v in range(33):
    assert abs(sum(z.get((v,w),0) for w in range(33))) < 1e-14
    assert abs(sum(z.get((w,v),0) for w in range(33))) < 1e-14
info = sum(z[u,v]**2/zero[0][u,v] for u,v in edges)
assert abs(info+ell*second) < 1e-13

for eps in (0.001,0.03,0.15):
    a,b = scene(eps),scene(-eps)
    assert np.max(abs(a[0]-b[0].T)) < 1e-11
    assert np.max(abs(a[1]-b[1])) < 1e-11
    kl = sum(a[0][u,v]*math.log(a[0][u,v]/b[0][u,v])
             for u,v in edges)
    assert abs(kl-a[3]) < 1e-11
    aa,bb,cc = 0,9,20
    odds = (a[0][aa,bb]*a[0][bb,cc]*a[0][cc,aa]) / (
            a[0][aa,cc]*a[0][cc,bb]*a[0][bb,aa])
    assert abs(math.log(odds)+6*ell*eps) < 1e-10

print("PASS native718 Book CP: cubic, Fisher, dark current,")
print("      current/entropy/KL, exact reversal and triangle odds")
print("A_second=",second,"I_edge=",info,"entropy quadratic=",2*info)
