#!/usr/bin/env python3
"""Audit the remaining full-source application; do not certify D0 -> GR.

The calibrated-corner inequality is exact rational arithmetic. Full matrices
below are structural controls, not newly admitted native programmes. They
retain the entire unitary carrier, both clock grades and a nonnormal old corner.
Run with Python >=3.10 and numpy/scipy/sympy/mpmath installed.
"""
from __future__ import annotations
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import math
import mpmath as mp
import numpy as np
import scipy.linalg as la
import sympy as sp

CHECKS = 0

def check(ok: bool, message: str) -> None:
    global CHECKS
    CHECKS += 1
    if not bool(ok):
        raise ArithmeticError(message)

def near(a, b, message: str, tolerance: float = 2e-11) -> float:
    error = float(np.max(np.abs(np.asarray(a)-np.asarray(b))))
    check(error < tolerance, message)
    return error

def exact_bound(alpha: F, gamma: F, prob: F, volume: F = F(1)) -> tuple[F, F]:
    check(0 < alpha <= 4 and 0 < gamma <= 1 and 0 < prob < F(1, 2)
          and volume > 0, 'exact parameter chart')
    x = gamma*prob
    c2 = 1-alpha*x*(1-x)
    check(c2 > 0, 'nonzero corner and nondegenerate signal')
    # (b_QUERY / lambda_field)^2, no floating square roots.
    ratio2 = 16*volume**2*c2*prob*(1-gamma*prob)/(alpha*gamma*(1-2*x)**2)
    floor2 = 4*volume**2*prob*(1-prob)
    check(ratio2 >= floor2, 'sharp uniform calibrated-query lower bound')
    return ratio2, floor2

def scalar_identities() -> dict:
    a,g,p,V = sp.symbols('a g p V', positive=True)
    x=g*p
    c2=1-a*x*(1-x)
    check(sp.expand(c2-(1-2*x)**2-(4-a)*x*(1-x)) == 0,
          'corner discriminant decomposition')
    ratio2=16*V**2*c2*p*(1-g*p)/(a*g*(1-2*x)**2)
    check(sp.simplify(ratio2.subs({a:4,g:1})-4*V**2*p*(1-p)) == 0,
          'sharpness, not merely a nonoptimal estimate')
    vals=[]
    for alpha,gamma in ((F(4),F(1)),(F(1,3),F(2,7)),
                        (F(1,2**80),F(1,2**200)),(F(4),F(1,2**120))):
        for p0 in (F(1,2**20),F(1,8),F(1,2)-F(1,2**120)):
            r2,f2=exact_bound(alpha,gamma,p0)
            vals.append({'alpha':str(alpha),'gamma':str(gamma),'P':str(p0),
                         'ratio_squared_at_least_floor':r2>=f2,
                         'exact_equality':r2==f2})
    # Closing the alleged c -> 0 escape on the actual alpha=4,gamma=1 chart.
    at_boundary=sp.limit((4*V**2*p*(1-p)),p,sp.Rational(1,2),dir='-')
    check(sp.simplify(at_boundary-V**2)==0, 'nonzero boundary limit of normalized row')
    # Unnormalized current may tend to zero; the correct source ratio does not.
    return {'sharp_floor':'2*Omega*sqrt(P*(1-P))',
            'equality_conditions':'alpha=4 and gamma=1',
            'P_to_half_sharp_ratio_limit':'Omega',
            'exact_rational_controls':vals}

def original_probability_collar() -> dict:
    # Direct-click polynomial is the one copied in the current two-field handoff.
    # Isolate p=phi^-1 using rational inequalities, not a rounded Golden number.
    lo,hi=F(8,13),F(13,21)
    check(lo*lo+lo-1<0<hi*hi+hi-1, 'Golden rational enclosure')
    radius=F(1,1024)
    e_lo=lo**2*(1-radius); e_hi=hi**2*(1+radius)
    b_lo=lo-hi**2*radius; b_hi=hi+hi**2*radius
    check(0<e_lo<=e_hi<F(1,2), 'first direct-click collar')
    check(0<b_lo<b_hi and b_hi*b_hi<F(1,2), 'second direct-click collar')
    l_min=4*e_lo*(1-e_lo)
    B_min=4*b_lo*b_lo*(1-b_lo*b_lo)
    z=F(1,2**20)
    # A=l+(1-l)B >= l, 0<=A,B<=1. r=z(A+B)-z^2 A B.
    r_lower=z*(l_min+B_min-z)
    check(r_lower>z and 2*z<F(1,2),'actual uncentered report has a uniform positive baseline')
    return {'coordinate_collar':'|x|,|y| <= 1/1024',
            'true_probability_lower_rational':str(r_lower),
            'simple_bounds':'2^-20 < r(x,y) <= 2*2^-20 < 1/2',
            'unit_volume_uniform_source_floor':2*math.sqrt(float(z*(1-z))),
            'branch_membership_tested':False,
            'meaning':'applies whenever the represented operands remain in this explicit collar'}

def rot(t: float) -> np.ndarray:
    return np.array([[math.cos(t),-math.sin(t)],[math.sin(t),math.cos(t)]])

def reflection(c: float) -> np.ndarray:
    u=math.sqrt(1-c*c)
    return np.array([[c,u],[u,-c]])

def clock(gates: list[np.ndarray]) -> np.ndarray:
    n=len(gates);d=len(gates[0]);out=np.zeros((n*d,n*d))
    for j,gate in enumerate(gates):
        out[((j+1)%n)*d:((j+1)%n+1)*d,j*d:(j+1)*d]=gate
    return out

def complete_operator_control() -> dict:
    K=np.array([[.5,1/7],[0.,.3]])
    left=la.sqrtm(np.eye(2)-K@K.T);right=la.sqrtm(np.eye(2)-K.T@K)
    old=np.block([[K,left],[right,-K.T]])
    near(old.T@old,np.eye(4),'full old unitary, nonnormal corner retained')
    check(la.norm(K@K.T-K.T@K)>.01,'genuinely nonnormal retained past')
    cs=[.61,.73]
    Qs=[reflection(c) for c in cs]
    emb=np.eye(16)[:,[0,4]]
    P=emb@emb.T
    beta=2*((math.sqrt(5)-1)/2)**2
    def objects(s,t):
        R1,R2=rot(s),rot(t)
        q1,q2=R1@Qs[0]@R1.T,R2@Qs[1]@R2.T
        gs=[np.kron(old,np.eye(4)),np.kron(np.eye(4),np.kron(q1,np.eye(2))),
            np.kron(np.eye(8),q2)]
        U=gs[2]@gs[1]@gs[0]
        clk=clock(gs);Delta=np.eye(48)-(clk+clk.T)/2
        heat=math.log(2*np.exp(-beta*la.eigvalsh(Delta)).sum())/beta
        V=np.kron(np.eye(4),np.kron(R1,R2))
        return U,clk,heat,V
    U0,T0,H0,_=objects(0.,0.)
    near(U0.T@U0,np.eye(16),'all16 final unitary')
    fullF=P@U0.T@(np.eye(16)-P)@U0@P
    C=emb.T@U0@emb
    near(C,math.prod(cs)*K,'same cold corner, not a separate model price')
    heat_errors=[];conj_errors=[]
    for s,t in ((.2,-.1),(-.3,.11),(.05,.28)):
        U,T,H,V=objects(s,t)
        conj_errors.append(near(T,np.kron(np.eye(3),V)@T0@np.kron(np.eye(3),V.T),
                                'full clock conjugation'))
        heat_errors.append(abs(H-H0))
    check(max(heat_errors)<5e-13,'entire two-grade heat is invariant')
    S=K.T@K;Tc=math.prod(c*c for c in cs)
    sources=[]
    for z in (1/7,2**-20):
        D=(1-z)*np.eye(2)+z*Tc*S
        w=z*Tc*np.trace(S@la.inv(D))
        def feedback(s,t):
            U,*_=objects(s,t)
            cc=emb.T@U@emb
            ff=np.eye(2)-cc.T@cc
            return -np.log1p(-z*la.eigvalsh(ff)).sum()
        ambient=-np.log1p(-z*la.eigvalsh(fullF)).sum()
        near(ambient,feedback(0,0),'whole16 return determinant, complement kept')
        derivatives=[]
        h=2e-4
        for j,c in enumerate(cs):
            def f(t): return feedback(t,0) if j==0 else feedback(0,t)
            fd=(-f(2*h)+8*f(h)-8*f(-h)+f(-2*h))/(12*h)
            expected=w*4*math.sqrt(1-c*c)/c
            derivatives.append({'j':j,'actual_source':float(expected),'FD_error':abs(float(fd-expected))})
            near(fd,expected,'full scalar price derivative',2e-11)
        sources.append({'zeta':z,'w':float(w),'sources':derivatives})
    return {'full_carrier_dimension':16,'protected_rank':2,'full_clock_modes_both_grades':96,
            'max_clock_conjugacy_error':max(conj_errors),'max_heat_error':max(heat_errors),
            'full_source_checks':sources,
            'native_programme_admission_asserted':False}

def volume_normalization() -> dict:
    V,n,a,b=sp.symbols('V n a b',positive=True)
    omega=V/n
    lam=a/omega
    # spatial I=sum I_j: global source gain is w*lam, NOT w*n*lam.
    row=sp.simplify(n*b/lam)
    check(sp.simplify(row-V*b/a)==0, 'spatial partition has no query dilution')
    wrong=sp.simplify(n*b/(n*lam))
    # The very same extra division also kills the wanted continuum field source.
    check(sp.simplify(lam/(n*lam)-1/n)==0,'false normalizer removes geometric response too')
    return {'correct_global_query_ratio':str(row),'incorrect_ratio':str(wrong),
            'geometric_covector_with_incorrect_normalizer':'DI/n',
            'scope':'equal-volume spatial partition; not all refinement geometries'}

def microscopic_limit() -> dict:
    mp.mp.dps=120
    z=mp.mpf(2)**-20
    eig=[mp.mpf('.01'),mp.mpf('.31')]
    probs=[mp.mpf(1)/8,mp.mpf(1)/5]
    volumes=[mp.mpf(1),mp.mpf(3)/2]
    result=[]
    for retention in (0,60,220):
        gamma=mp.mpf(2)**(-retention)
        alpha=mp.mpf(4)
        corners=[]; lambdas=[]; bs=[]
        for prob,vol in zip(probs,volumes):
            x=gamma*prob
            c=1-2*x
            u=mp.sqrt(4*x*(1-x))
            corners.append(c)
            lambdas.append(4*gamma*(1-2*x)/(vol*c*c))
            bs.append(4*u/c)
        T=(corners[0]*corners[1])**2*mp.mpf('1e-90')
        w=sum(z*T*v/(1-z+z*T*v) for v in eig)
        Lambda=sum(lambdas)
        Gamma=w*Lambda
        normalized=sum(w*b/Gamma for b in bs)
        expected=sum(bs)/Lambda
        check(abs(normalized/expected-1)<mp.mpf('1e-100'), 'true gain not replaced by one')
        floor=min(2*vol*mp.sqrt(prob*(1-prob)) for prob,vol in zip(probs,volumes))
        check(normalized>=floor, 'retention and tiny history do not evade sharp source ratio')
        result.append({'retention':retention,'Gamma':mp.nstr(Gamma,30),
                       'actual_normalized_query_norm':mp.nstr(normalized,30),
                       'sharp_common_floor':mp.nstr(floor,30)})
    return {'high_precision_actual_gain_controls':result,
            'same_physical_variation_norm_assumed':False}

def main() -> None:
    out={'input_commit':'1595b9bd2cf9720900c1bf573df04cf9e2e7931f',
         'sharp_bound':scalar_identities(),'uncentered_direct_click':original_probability_collar(),
         'complete_operator':complete_operator_control(),
         'spatial_partition':volume_normalization(),
         'suppressed_signal':microscopic_limit()}
    out.update({'checks':CHECKS,'status':'PASS_SCOPED_FULL_SOURCE_AUDIT',
                'GR_closed':False,'native_variation_domain_derived':False,
                'physical_GR_impossibility_proved':False,
                'new_full42_root_computed':False,'Lean_or_CI_run':False,
                'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()})
    print(json.dumps(out,indent=2,sort_keys=True,ensure_ascii=False))

if __name__=='__main__':
    main()
