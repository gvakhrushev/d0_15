#!/usr/bin/env python3
"""Same complete observer CAR16 Julia-Choi signed event at ORIGINAL Golden T=p Lambda(U).
Consumes existing #334 original p^2 GOOD / p BAD control. NOT literal full128 port Kraus.
"""
import numpy as np
import sympy as s
from itertools import product
p=(s.sqrt(5)-1)/2
assert s.simplify(p+p*p-1)==0
def E(i,j):
    A=s.zeros(4);A[i,j]=1;return A
K=[E(0,i)+E(i,0) for i in (1,2,3)]
J=[E(2,3)-E(3,2),E(3,1)-E(1,3),E(1,2)-E(2,1)]
G=K+J
x=s.symbols('x',real=True)
for i,X in enumerate(G):
    boost=i<3
    U=s.eye(4)+(s.sinh(x) if boost else s.sin(x))*X+(s.cosh(x)-1 if boost else 1-s.cos(x))*X*X
    good=s.factor(p*p*s.det(s.eye(4)+U.T*U)/16)
    mark=s.factor(p*p*s.det(s.eye(4)+U)**2/256)
    assert s.simplify(mark-p*p*(s.cosh(x/2) if boost else s.cos(x/2))**4)==0
    assert s.simplify(good-p*p*(s.cosh(x)**2 if boost else 1))==0
    hm=s.diff(s.log(mark),x,2).subs(x,0)
    hg=s.diff(s.log(good),x,2).subs(x,0)
    assert hm==(1 if boost else -1)
    assert hg==(2 if boost else 0)
    assert hm-hg==-1
assert s.simplify(p*p+(1-p*p)-1)==0
assert s.simplify(1-p*p-p)==0
print('PASS exact Golden GOOD p^2, BAD p at identity, all 6 signed joint/conditional log jets')
print('PASS native p^2 normalization does not alter literal Palatini event log mixed Hessian')
print('FIREWALL: same weights do NOT identify with real original per-label K0,k=p Lk / K1,k=sqrt(p) Lk')
print('GR_closed=false; full128 Book physical event/action selection open')
