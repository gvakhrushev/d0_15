#!/usr/bin/env python3
"""All-original 33 vertex Info parity of 718-edge scalar Book pressure.

Exact all-zone Info chiral cubic + arbitrary inhomogeneous Info spectral
parity, nonzero chiral Hessian and vanishing first/mixed Info source.
NO compulsory native ActionProtocol price, CAR action or GR closure.
"""
from math import exp, log, sqrt
import numpy as np
import sympy as sp

phi=(1+sqrt(5))/2
p=1/phi
ell=log(phi)

# ORIGINAL three unequal graph parts, all literal 718 supported arcs.
zone=np.array([0]*9+[1]*11+[2]*13)
n=len(zone)
u,v=np.where(zone[:,None]!=zone[None,:])
assert n==33 and len(u)==718
arc=np.zeros((n,n))
arc[u,v]=1
odd=np.zeros((n,n))
for i,j in zip(u,v):
    odd[i,j]=1 if (zone[i],zone[j]) in ((0,1),(1,2),(2,0)) else -1
assert np.array_equal(odd,-odd.T)

# Exact original Perron 3-zone characteristic, with arbitrary nonlinear
# vertex-Info multipliers a=phi^IA, b=phi^IB, c=phi^IC.
a,b,c,q,x,g=sp.symbols('a b c q x g',positive=True)
Z=sp.Matrix([[0,11*g*sp.sqrt(a*b)*q,13*g*sp.sqrt(a*c)/q],
             [9*g*sp.sqrt(a*b)/q,0,13*g*sp.sqrt(b*c)*q],
             [9*g*sp.sqrt(a*c)*q,11*g*sp.sqrt(b*c)/q,0]])
B=g**2*(99*a*b+117*a*c+143*b*c)
C=2574*g**3*a*b*c
char=x**3-B*x-C*(q**3+q**-3)/2
assert sp.simplify((x*sp.eye(3)-Z).det()-char)==0
print('PASS exact nonlinear native 9/11/13 all-Info odd-cycle cubic')

# Endpoint Info allocation theta: no source hidden by changing vertex
# allocations. Test fully inhomogeneous I across all 33 original vertices.
rng=np.random.default_rng(4021)
I=rng.uniform(-0.7,0.7,n)
theta=0.23
symmetric_cost=1+0.06*np.cos(np.add.outer(np.arange(n),np.arange(n)))
assert np.max(abs(symmetric_cost-symmetric_cost.T))<1e-15

def transfer(t,I,theta):
    K=np.zeros((n,n))
    K[u,v]=np.exp(-ell*(symmetric_cost[u,v]+t*odd[u,v]-
                     theta*I[u]-(1-theta)*I[v]))
    return K

def rho33(t,I,theta):
    e=np.linalg.eigvals(transfer(t,I,theta))
    return float(np.max(e.real))

def F33(t,I,theta):
    return -log(rho33(t,I,theta))/ell

D=np.exp(ell*(theta-.5)*I)
for t in (0.0,.04,.22):
    K=transfer(t,I,theta)
    H=transfer(t,I,.5)
    assert np.max(abs(K-(D[:,None]*H/D[None,:])))<2e-14
    assert np.max(abs(H.T-transfer(-t,I,.5)))<2e-14
    assert abs(rho33(t,I,theta)-rho33(-t,I,theta))<2e-12
print('PASS arbitrary 33 Info, nonconstant reversible base Cost, any allocation')
print('PASS exact matrix similarity/transposition and scalar Perron parity')

h=0.001
first=(F33(h,I,theta)-F33(-h,I,theta))/(2*h)
Ip=I.copy();Ip[3]+=h
Im=I.copy();Im[3]-=h
mixed=(F33(h,Ip,theta)-F33(-h,Ip,theta)
      -F33(h,Im,theta)+F33(-h,Im,theta))/(4*h*h)
assert abs(first)<2e-9 and abs(mixed)<1e-7
print('PASS first odd Cost and mixed Info×odd Cost derivatives vanish')

# Nonlinear original 3-zone background Info has NONZERO pure chiral
# second source. Its exact characteristic gives Lambda'' analytically.
def zone_lambda(t,A,Bv,Cv):
    weights=np.array([A,Bv,Cv])
    z=np.array([[0,11*p*sqrt(A*Bv)*exp(-ell*t),
                 13*p*sqrt(A*Cv)*exp(ell*t)],
                [9*p*sqrt(A*Bv)*exp(ell*t),0,
                 13*p*sqrt(Bv*Cv)*exp(-ell*t)],
                [9*p*sqrt(A*Cv)*exp(-ell*t),
                 11*p*sqrt(Bv*Cv)*exp(ell*t),0]])
    return float(max(np.linalg.eigvals(z).real))

def zone_action(t,A,Bv,Cv):
    return -log(zone_lambda(t,A,Bv,Cv))/ell

for A,Bv,Cv in ((1.,1.,1.),(1.3,.7,1.6),(.8,1.1,1.4)):
    lam=zone_lambda(0,A,Bv,Cv)
    quad=p*p*(99*A*Bv+117*A*Cv+143*Bv*Cv)
    triple=2574*p**3*A*Bv*Cv
    assert abs(lam**3-quad*lam-triple)<1e-10
    analytic=-9*ell*triple/(lam*(3*lam*lam-quad))
    fd=(zone_action(.002,A,Bv,Cv)-2*zone_action(0,A,Bv,Cv)
        +zone_action(-.002,A,Bv,Cv))/.002**2
    assert analytic<0 and abs(analytic-fd)<2e-6
    if A==Bv==Cv==1.:
        assert abs(analytic+0.4763744515526456)<2e-12
    print('PASS native 3-zone nonlinear Info chiral Hessian:',
          tuple((A,Bv,Cv)),round(analytic,13))
print('RESULT: moving ALL 33 native scalar vertex Info does not supply a')
print('first signed pressure source; stationary Info-only preparation')
print('cannot create a mixed odd/Info Schur source on a parity-even action')
print('FIREWALL: compulsory whole Book3/HJR, native field mapping and GR OPEN')
