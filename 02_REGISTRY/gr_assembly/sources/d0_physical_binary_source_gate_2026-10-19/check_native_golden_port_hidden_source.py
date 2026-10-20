#!/usr/bin/env python3
"""Symbolic original Golden port KL and flat nonblank-label source.
Uses actual based programme identities, NOT a physical GR selector.
"""
import sympy as S
p,h,lam,beta=S.symbols('p h lam beta',positive=True,real=True)
rel=S.Poly(p-p**2-p**3,p).rem(S.Poly(p**2+p-1,p))
assert rel.is_zero
# Native full-label operators: A=hD/16, epsilon=p**2*h**2/64.
eta=h**2*lam/256
eps=p**2*h**2/64
# Sum over nonblank labels, both ports: sum K*K =4 p² A²(1-A²).
e_label=S.expand(4*p**2*eta*(1-eta))
assert S.simplify(e_label-eps*lam*(1-eta))==0
# On flat first shell Delta=lambda I; fixed integer-depth beta=n epsilon.
count=S.expand(beta*lam*(1-eta))
port_info=S.expand(p**3*count)
assert S.simplify(S.diff(port_info,lam)-p**3*beta*(1-2*eta))==0
assert S.limit(port_info,h,0)==p**3*beta*lam
assert S.limit(S.diff(port_info,lam),h,0)==p**3*beta
# Special blank-label port1 is NOT among nonblank and is explicitly retained.
port1=p*beta*lam
nonblank_port1=p*count
blank_port1=S.simplify(port1-nonblank_port1)
assert S.simplify(blank_port1-p*beta*lam*eta)==0
assert S.simplify(nonblank_port1+blank_port1-port1)==0

from math import sqrt
pv=(sqrt(5)-1)/2
hv=1/16
n=4096
ell=pv**2*hv**2/64
nu=.62
k2=2.0
lambda_at=lambda v:v*v*k2
z=lambda v:pv**3*n*float(ell)*lambda_at(v)*(1-hv**2*lambda_at(v)/256)
e=1e-5
num=(z(nu+e)-z(nu-e))/(2*e)
expected=float((p**3*beta*(1-2*eta)).subs({p:pv,beta:n*ell,h:hv,lam:lambda_at(nu)}))*2*nu*k2
assert abs(num-expected)<1e-9
assert num>0
print('PASS exact: native Golden (p²,p) vs code(p,p²) relative info = p³')
print('PASS exact: nonblank-label effect = epsilon Delta(1-h²Delta/256)')
print('PASS exact: first-shell info = p³ beta lambda(1-h²lambda/256)')
print('PASS exact: first source = p³ beta (1-h²lambda/128) Dlambda')
print('PASS exact: special blank/port1 retained')
print(f'PASS finite jet: hidden-price derivative={num:.12g}')
print('SCOPE: conditional full-code KL, native 128-channel equations; no GR closure')
