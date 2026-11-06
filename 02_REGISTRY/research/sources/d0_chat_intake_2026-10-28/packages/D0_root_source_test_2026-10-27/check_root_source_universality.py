#!/usr/bin/env python3
"""Exact source-realization test on the existing two-plus-eight sign interface.

This is NOT a proof of the full D0 axioms, nor a native 42-field solver.
It checks a general construction and two different objectives on the same
sign/source interface, with every failure in the full three-status price.
"""
from __future__ import annotations
import hashlib
import itertools
import json
import math
from fractions import Fraction as Q
from pathlib import Path

import mpmath as mp
import sympy as sp

mp.mp.dps = 100
CHECKS = 0

def require(value, description: str) -> None:
    global CHECKS
    CHECKS += 1
    if not bool(value):
        raise ArithmeticError(description)

def equal(a, b, description: str) -> None:
    require(sp.simplify(a-b) == 0, description)

def near(a, b, description: str, tol='1e-75') -> None:
    require(abs(a-b) <= mp.mpf(tol)*max(mp.mpf(1),abs(a),abs(b)), description)

def madd(a, b):
    c = dict(a)
    for k,v in b.items():
        c[k] = c.get(k,Q(0)) + v
        if c[k] == 0: del c[k]
    return c

def mmul(a, b):
    c = {}
    for (i,j),v in a.items():
        for (k,l),w in b.items():
            key = (i+k,j+l)
            c[key] = c.get(key,Q(0))+v*w
    return {k:v for k,v in c.items() if v}

# BOTH objectives use exactly the same original access degree bound: 2+8.
# S_B has a saddle at the origin and TWO further stationary points.
objectives = {
    'A': {(2,0):Q(1),(0,2):Q(1)},
    'B': {(2,0):Q(1),(0,4):Q(1),(0,2):Q(-1,2)},
}
rbase, eps = Q(1,8), Q(1,64)
rows, expectations, limits = {}, {}, {}
for name, pol in objectives.items():
    table = []
    expectation = {}
    for bits in itertools.product((-1,1), repeat=10):
        sflags,tflags = bits[:2],bits[2:]
        score = sum(c*math.prod(sflags[:i])*math.prod(tflags[:j])
                    for (i,j),c in pol.items())
        b = rbase + eps*score
        require(Q(1,16) < b < Q(3,16), f'{name}: every literal branch is strict')
        require((128*b).denominator==1, f'{name}: one common 7-bit selector')
        table.append({'flags':list(bits),'one_threshold':int(128*b),'total':128})
        # Independently multiply the TEN real branch probabilities.  This
        # reconstructs the whole expectation, not a coefficient lookup.
        weight = {(0,0):Q(1)}
        for k,sgn in enumerate(bits):
            monomial = (1,0) if k < 2 else (0,1)
            weight = mmul(weight,{(0,0):Q(1,2),monomial:Q(sgn,2)})
        expectation = madd(expectation,{k:b*v for k,v in weight.items()})
    wanted = madd({(0,0):rbase},{k:eps*v for k,v in pol.items()})
    require(expectation==wanted, f'{name}: exact full 1024-branch source law')
    rows[name] = table
    expectations[name] = {f'{i},{j}':str(v) for (i,j),v in sorted(expectation.items())}
    limits[name] = [min(x['one_threshold'] for x in table),max(x['one_threshold'] for x in table)]

# Exact unconditional herald probabilities: no exact unconditioned 1/2 gate
# is inserted. Seven fair signs come from seven Golden pairs.
p=(sp.sqrt(5)-1)/2
eta=2*p**3
alpha = eta**7
for name, table in rows.items():
    for n in set(x['one_threshold'] for x in table):
        equal(alpha*sp.Rational(n,128),n*p**21,f'{name}: exact unconditional one')
        equal(alpha*sp.Rational(128-n,128),(128-n)*p**21,f'{name}: exact unconditional zero')
    equal(1-alpha+128*p**21,1,f'{name}: failure retained normalization')

# Symbolic source coefficient and the exact real stationary sets.
u,v=sp.symbols('u v', real=True)
SA=u**2+v**2
SB=u**2+v**4-sp.Rational(1,2)*v**2
require(sp.solve([sp.diff(SA,u),sp.diff(SA,v)],(u,v))=={u:0,v:0},'A stationary set')
roots_b=sp.solve([sp.diff(SB,u),sp.diff(SB,v)],(u,v))
require(set(roots_b)=={(0,0),(0,sp.Rational(-1,2)),(0,sp.Rational(1,2))},'B stationary set')
require(sp.hessian(SA,(u,v)).subs({u:0,v:0})==sp.diag(2,2),'A origin minimum Hessian')
require(sp.hessian(SB,(u,v)).subs({u:0,v:0})==sp.diag(2,-1),'B origin saddle Hessian')

q,z,a,r,s=sp.symbols('q z a r s',positive=True)
f=4*q*(1-q)
j=-sp.log(1-z*f)
jpp=sp.diff(j,q,2)
equal(jpp,-8*z*(1-2*z+z*f)/(1-z*f)**2,'full feedback scalar concavity')
Phi=s*sum(j.subs(q,t) for t in (1-a,a*(1-r),a*r))
kappa=sp.diff(Phi,r)
kappa_closed=(8*s*z*a*a*(1-2*r)*(1-2*z+2*a*z-4*a*a*r*(1-r)*z)
              /((1-4*z*a*r*(1-a*r))*(1-4*z*a*(1-r)*(1-a*(1-r)))))
equal(kappa,kappa_closed,'factorized full derivative, including failure')

# Structural all-column unitary test: 3 status channels, full complement.
# This is a compact dilation of the genuine probabilities, NOT a claim that
# this 3x3 matrix is a literal single elementary native gate.
pm=(mp.sqrt(5)-1)/2
am=(2*pm**3)**7
zm=mp.mpf(2)**-20
sm=128
rm=mp.mpf(1)/8

def j_mp(t): return -mp.log1p(-4*zm*t*(1-t))
def k_mp(rr):
    dd=lambda t: 4*zm*(1-2*t)/(1-4*zm*t*(1-t))
    return sm*am*(dd(am*rr)-dd(am*(1-rr)))
def phi_mp(rr):
    return sm*sum(j_mp(t) for t in (1-am,am*(1-rr),am*rr))
def obj(name,x,y):
    return x*x+y*y if name=='A' else x*x+y**4-y*y/2

def direct_dilation(rr):
    probabilities=(1-am,am*(1-rr),am*rr)
    vv=mp.matrix([mp.sqrt(t) for t in probabilities])
    e=mp.matrix([1,0,0]); d=e-vv
    U=mp.eye(3)-2*(d*d.T)/(d.T*d)[0]
    near(mp.norm(U.T*U-mp.eye(3)),0,'whole dilating matrix is orthogonal')
    near(mp.norm(U*e-vv),0,'preparation on literal input')
    P=mp.diag([1,0,0]); I=mp.eye(3)
    value=mp.mpf(0)
    for jj,prob in enumerate(probabilities):
        Qj=mp.zeros(3);Qj[jj,jj]=1
        W=U.T*(I-2*Qj)*U
        near(mp.norm(W.T*W-I),0,'whole comparison orthogonal')
        near(mp.norm(W*W-I),0,'whole comparison is reflection')
        FF=P*W.T*(I-P)*W*P
        near(FF[0,0],4*prob*(1-prob),'exact true complement, no selected output replacement')
        value -= sm*mp.log(mp.det(I-zm*FF))
    near(value,phi_mp(rr),'whole determinant equals the THREE-status price')
    return value

results=[]
for name in objectives:
    for x0,y0 in ((mp.mpf(0),mp.mpf(0)),(mp.mpf(0),mp.mpf(1)/2),
                  (mp.mpf(1)/5,mp.mpf(1)/3)):
        rr=rm+mp.mpf(eps.numerator)/eps.denominator*obj(name,x0,y0)
        direct=direct_dilation(rr)
        def fun(x,y): return phi_mp(rm+mp.mpf(1)/64*obj(name,x,y))
        du=mp.diff(lambda xx:fun(xx,y0),x0)
        dv=mp.diff(lambda yy:fun(x0,yy),y0)
        dsx=2*x0
        dsy=2*y0 if name=='A' else 4*y0**3-y0
        near(du,k_mp(rr)*dsx/64,'same full price source, x')
        near(dv,k_mp(rr)*dsy/64,'same full price source, y')
        require(k_mp(rr)>0,'all source gains positive on tested chart')
        results.append({'objective':name,'x':mp.nstr(x0,20),'y':mp.nstr(y0,20),
                        'probability':mp.nstr(rr,40),'price':mp.nstr(direct,45),
                        'source_x':mp.nstr(du,45),'source_y':mp.nstr(dv,45)})
# The second action has an EXACT algebraic root absent from the first.
near(mp.diff(lambda t:phi_mp(rm+(t**4-t*t/2)/64),mp.mpf(1)/2),0,
     'B root t=1/2 remains a full-price root')
extra_A=k_mp(rm+mp.mpf(1)/256)/64
require(extra_A>0,'A source at the same state is strictly nonzero')

# Sanity control: a field-dependent extra baseline is NOT covered by the
# monotone-composition argument. This prevents claiming unrestricted D0.
extra=sp.Rational(1,16)*u
require(sp.diff(extra,u)!=0,'independent extra full-price source retained')

out = {
    'status':'PASS_FIXED_INTERFACE_POLYNOMIAL_SOURCE_REALIZATION',
    'checks':CHECKS,
    'arithmetic':'Fractions + symbolic algebraic Q(sqrt(5)); mpmath100 for dilation controls',
    'original_access_interface':'two geometric signs plus eight material signs',
    'decoded_table_count':2,'branches_per_table':1024,
    'common_threshold_denominator':128,'threshold_min_max':limits,
    'fair_resource_count':7,'direct_Golden_calls_coin_layer_only':14,
    'coin_readiness':mp.nstr(am,60),
    'unconditional_one_law':'k * p^21; failure=1-128*p^21',
    'exact_expected_reports':expectations,
    'stationary_points_A':[['0','0']],
    'stationary_points_B':[['0','0'],['0','-1/2'],['0','1/2']],
    'full_price_source_A_at_B_root':mp.nstr(extra_A,60),
    'whole_dilation_checks':results,
    'native_logical_gate_palette': 'same conditional heralded interface as prior packet, not newly derived',
    'large_native_word_emitted':False,
    'the_two_examples_are_full_models_of_D0':False,
    'unconditional_GR_closed':False,
}
print(json.dumps(out,indent=2,ensure_ascii=False,sort_keys=True))
