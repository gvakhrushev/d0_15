#!/usr/bin/env python3
"""Scoped algebra and finite complex-instrument diagnostics for 7fy.

The random-matrix checks are numerical; native compiler and full price are
not replayed. Ideal angles are targets, not newly admitted primitive gates.
"""
from math import asin, cos, exp, log, log1p, sin, sqrt
import numpy as np
import sympy as sp

p = (sqrt(5)-1)/2
ell = -log(p)
rng = np.random.default_rng(715)
counts = {'target_projectors': 0, 'amplitude_boundaries': 0,
          'scalar_minimum': 0, 'complex_instrument': 0, 'exact_native_echo': 0}

def H(x):
    if x <= 0 or x >= 1:
        return 0.0
    return -x*log(x)-(1-x)*log1p(-x)

def entropy(mat):
    values = np.linalg.eigvalsh((mat+mat.conj().T)/2)
    return -sum(float(x)*log(float(x)) for x in values if x > 1e-14)

def P(q,u,a):
    return 2+q+(1-q)*u-a*(H(q)+(1-q)*H(u))/ell

def opt(a):
    if a == 0: return 0.0, 0.0
    x = exp(-ell/a)
    return x/(1+x), -a*log1p(x)/ell

def rot(theta):
    return np.array([[cos(theta),-sin(theta)],[sin(theta),cos(theta)]])

P0=np.diag([1,1,0,0]); P1=np.diag([0,0,1,0]); Pi=np.diag([0,0,0,1])
ps=(sp.sqrt(5)-1)/2
Gs=sp.Matrix([[sp.sqrt(ps),-ps],[ps,sp.sqrt(ps)]])
cx=sp.diag(1,1,1,1); cx[2,2]=0; cx[3,3]=0; cx[2,3]=1; cx[3,2]=1
g=sp.kronecker_product(sp.eye(2),Gs)
actual=cx*g*cx*g
target=sp.diag(1,1,1,1); target[:2,:2]=Gs**2
assert all(sp.simplify(x)==0 for x in actual-target)
counts['exact_native_echo']+=1
v=np.array([sqrt(p),p]); start=asin(p)
for u in np.linspace(0,1,101):
    delta=asin(sqrt(float(u)))-start
    U=np.eye(4); U[:2,:2]=rot(delta)
    assert all(np.linalg.norm(U.T @ P @ U-P)<1e-13 for P in (P0,P1,Pi))
    assert np.linalg.norm(U[:2,:2]@v-np.array([sqrt(1-u),sqrt(u)]))<1e-13
    counts['target_projectors']+=1

for q in [p*p,0.4,0.47,0.5]:
  for a in [0,0.01,0.1,0.3,1,2,10]:
    u,m=opt(a)
    assert m <= p*p-a*(1+p*p)+2e-14
    d=1-m-a*log((1-q)/q)/ell
    assert d >= p+a*p*p-3e-14
    if a > 0 and u > 1e-14:
        assert abs(1-a*log((1-u)/u)/ell)<1e-11
    for other in [0,p*p,0.8,1]:
        assert P(q,other,a)>=P(q,u,a)-1e-12
    counts['scalar_minimum']+=1
    if a==0:
        for theta in [1e-2,1e-3,1e-4]:
            assert abs((P(q,sin(theta)**2,0)-P(q,0,0))/theta**2-(1-q))<3e-5
            counts['amplitude_boundaries']+=1

# Random efficient 3-label instrument: E00+E01=(1-q)I, E10=qI.
# Complex unitaries are ambient competitors, not native gates. The entire
# conditional quantum output is retained, and rho_R^x is computed from
# sqrt(rho) E_x sqrt(rho) by the purification identity.
def unitary():
    z=rng.normal(size=(2,2))+1j*rng.normal(size=(2,2))
    q,r=np.linalg.qr(z)
    return q @ np.diag(np.diag(r)/np.abs(np.diag(r)))

for _ in range(200):
    q=float(rng.uniform(p*p,0.5)); a=float(rng.uniform(0.1,3))
    bq=float(rng.uniform(0,a)); bc=a-bq
    z=rng.normal(size=(2,2))+1j*rng.normal(size=(2,2))
    rho=z@z.conj().T; rho/=np.trace(rho)
    vals,vec=np.linalg.eigh(rho); sr=(vec*np.sqrt(vals))@vec.conj().T
    x,y=rng.uniform(.02,.98,2)
    V=unitary(); W0,W1,W2=unitary(),unitary(),unitary()
    A=V@np.diag([sqrt(x),sqrt(y)])@V.conj().T
    B=V@np.diag([sqrt(1-x),sqrt(1-y)])@V.conj().T
    ks=[sqrt(1-q)*W0@A,sqrt(1-q)*W1@B,sqrt(q)*W2]
    probs=[float(np.trace(k@rho@k.conj().T).real) for k in ks]
    u=probs[1]/(1-q)
    hc=-sum(v*log(v) for v in probs if v>0)
    iq=hc+sum(prob*entropy(k@rho@k.conj().T/prob) for prob,k in zip(probs,ks))-entropy(rho)
    chi=entropy(rho)-sum(prob*entropy(sr@k.conj().T@k@sr/prob) for prob,k in zip(probs,ks))
    assert chi >= -1e-12 and abs(iq-(hc-chi))<1e-11
    val=2+q+(1-q)*u-(bq*iq+bc*hc)/ell
    ua,_=opt(a)
    kl=(1-u)*log((1-u)/(1-ua))+u*log(u/ua)
    gap=(a/ell)*(1-q)*kl+(bq/ell)*chi
    assert abs((val-P(q,ua,a))-gap)<1e-11 and gap>=-1e-12
    counts['complex_instrument']+=1

print('PASS:', counts)
print('Not checked: full H.1 compiler, exact finite Gibbs target, 425D heat, Book03 physical C.')
