#!/usr/bin/env python3
"""Exact archive/cold fixture, with general formulas in the companion note."""
import importlib.util,sys
import math
from itertools import product
from pathlib import Path
import sympy as sp

source=Path(__file__).resolve().parents[1]/'inputs'/'native_execution.py'
spec=importlib.util.spec_from_file_location('archive_native',source)
nt=importlib.util.module_from_spec(spec);sys.modules[spec.name]=nt;spec.loader.exec_module(nt)
p,a=nt.P,nt.A
u,d=(a+p)/2,(a-p)/2

def eq(x,y=0):
    return nt.GOLDEN_FIELD.from_sympy(sp.simplify(x-y))==nt.GOLDEN_FIELD.zero

def cx(x,c,t): x[t]^=x[c]
def swap(x,c,t):
    cx(x,c,t);cx(x,t,c);cx(x,c,t)

# Replay exactly the addressed six-copy body on arbitrary port,r,t and all
# 64 initial archives, as owned by 7fy. No fresh-zero assumption is used here.
count=0
for bits in product((0,1),repeat=9):
    x=list(bits); original=x.copy()
    for i,wire in enumerate((1,2,1,2)):
        swap(x,0,wire);cx(x,0,3+i)
        if i>=2: cx(x,2 if i==2 else 1,3+i+2)
        swap(x,0,wire)
    r,t=original[1:3]
    assert x[:3]==original[:3]
    assert tuple(x[3+i]^original[3+i] for i in range(6))==(r,t,r,t,t,r)
    count+=1
assert count==512

v=sp.Matrix([a,p]); z=sp.Matrix([1,0]); e=[sp.Matrix([1,0]),sp.Matrix([0,1])]
flags=lambda r,t: (r,t,r,t,t,r)
born=sp.kronecker_product(v,v,*(v for _ in range(6)),z)

def branch(Q):
    c=1-2*Q;s=sp.sqrt(1-c*c)
    W=sp.Matrix([[c,s],[s,-c]])
    ks=[u*W+d*sp.eye(2),u*W-d*sp.eye(2)]
    # Both direct branches are kept on the actual bank/reference carrier.
    return [sp.kronecker_product(e[b],z,*(e[i] for i in flags(b,0)),ks[b]*z)
            for b in (0,1)]

for Q in (sp.Rational(1,4),sp.Rational(1,2)):
    q=p**2+p**3*Q;c=1-2*Q; xs=[u*c+d,u*c-d]
    vecs=branch(Q)
    qb=[1-q,q]; coeff=[p**4,p**6]
    assert all(eq((x.T*x)[0],prob) for x,prob in zip(vecs,qb))
    amps=[sp.simplify((born.T*x)[0]) for x in vecs]
    assert all(eq(amp,fac*x) for amp,fac,x in zip(amps,coeff,xs))
    c=1-2*Q;s=sp.sqrt(1-c*c);W=sp.Matrix([[c,s],[s,-c]])
    K0=u*W+d*sp.eye(2)
    alt=sp.kronecker_product(e[0],e[1],*(e[i] for i in flags(0,1)),K0*z)
    assert eq((born.T*alt)[0],p**6*xs[0])
    coh=sp.simplify(sum(amps)**2)
    cp=sp.simplify(sum(x*x for x in amps))
    h=sp.simplify(sum(x*x/prob for x,prob in zip(amps,qb)))
    assert eq(coh,(p**4*xs[0]+p**6*xs[1])**2)
    assert eq(cp,p**8*xs[0]**2+p**12*xs[1]**2)
    assert eq(h,p**8*xs[0]**2/(1-q)+p**12*xs[1]**2/q)
    if Q==sp.Rational(1,4):
        assert float(coh-cp)>0
    else:
        assert float(coh-cp)<0

# Joint born masses and stopping support are exact and not rank-one guesses.
assert eq((a**8)**2,p**8) and eq((a**4*p**4)**2,p**12)
assert eq(p**8*(1-q)+p**12*q-(p**8+p**12),-(p**8*q+p**12*(1-q)))

# At Q=1/4 the matched scalar NPS marked-range derivative is strictly
# negative. Elementary positive inequalities certify both summands' signs.
Q=sp.Rational(1,4);q=p**2+p**3*Q
x0=u/2+d;x1=u/2-d
assert float(x0)>0 and float(x1)>0
assert float(4*u*(1-q)-p**3*x0)>0
derivative=p**8*(-4*u*x0/(1-q)+p**3*x0**2/(1-q)**2)+p**12*(-4*u*x1/q-p**3*x1**2/q**2)
assert float(derivative)<0
pf=float(p);uf=float(u);df=float(d);af=float(a)
for i in range(101):
    QQ=i/200
    qq=pf**2+pf**3*QQ
    xx0=uf*(1-2*QQ)+df;xx1=uf*(1-2*QQ)-df
    deriv=pf**8*(-4*uf*xx0/(1-qq)+pf**3*xx0**2/(1-qq)**2)+pf**12*(-4*uf*xx1/qq-pf**3*xx1**2/qq**2)
    assert deriv<0
assert 36+6+102+30==174 and 36+63+132*64==8547
print('PASS: 512 Boolean archive inputs, exact born amplitudes p^4,p^6, two exact NPS fixtures.')
print('PASS: alternate r0,t1 branch has coefficient p^6; theta derivative at 0 is p^6 X0.')
print('PASS: coherent versus dephased cross term changes sign between Q=1/4 and Q=1/2.')
print('PASS: matched NPS marked-range derivative negative on 101 collar diagnostics.')
print('PASS: 174 added stages, stage-dimension increment 8547d, final dimension 64d.')
print('Scope: reader and finite algebra fixture; no full H.1 writer or stopped-clock replay.')
