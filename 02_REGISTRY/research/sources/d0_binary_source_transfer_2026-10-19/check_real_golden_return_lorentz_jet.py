#!/usr/bin/env python3
"""Native two-scene-tick F and k-Golden GOOD/BAD exact local link-jet.

The full Lorentz Hessian M is an already-owned result of the ORIGINAL six-face
all40 checker; optional --M imports it. This does NOT select a Book action.
"""
from math import sqrt, log, log1p, exp
from pathlib import Path
import runpy
import sys

p=(sqrt(5)-1)/2
phi=1/p
LOGPHI=log(phi)
d=1056

def params(k):
    x=p**(2*k)
    z=x/(1-x)
    A=exp(2*d*log1p(-x))   # MANDATORY Golden filling prefactor
    B=4*p**3               # two-tick scene effect at q=0
    return z,A,B

def original_j(k,f,t=1.0):
    z,A,B=params(k)
    E=p*p*(1+t*t*f)
    lam=4*E*(1-E)          # original four-copy AF return
    Q=1-z*B
    R=1-z*(B+(1-B)*lam)
    if not (0<E<1 and Q>0 and R>0):
        raise ValueError("outside original positive operator chart")
    return -(d/2)*(log(Q)+log(R))

def native_good(k,f,t=1.0):
    _,A,_=params(k)
    return A*exp(-2*original_j(k,f,t))

def native_odds(k,f,t=1.0):
    g=native_good(k,f,t)
    return (log1p(-g)-log(g))/LOGPHI

def analytic_alpha(k,t=1.0):
    z,A,B=params(k)
    E0=p*p
    R0=1-z*(B+(1-B)*4*E0*(1-E0))
    return (d/2)*z*(1-B)*4*p*p*(1-2*p*p)*t*t/R0

def check(k):
    z,A,B=params(k)
    g=native_good(k,0)
    alpha=analytic_alpha(k)
    factor=2*alpha/((1-g)*LOGPHI)
    assert 0<g<1 and alpha>0 and factor>0
    R0=1-z*(B+(1-B)*4*p*p*(1-p*p))
    assert abs(alpha-(d/2)*z*4*p**11/R0)<1e-12
    h=1e-4
    numeric=(original_j(k,h)-original_j(k,-h))/(2*h)
    assert abs(numeric-alpha)/alpha<1e-5
    # Existing original 24-link M has eigenvalues +/-2 (four each).
    # Test the exact f(omega) = m*omega**2/2 second-jet composition.
    for m in (-2.0,2.0):
        h=.01
        f=lambda y: .5*m*y*y
        q2=(native_odds(k,f(h))+native_odds(k,f(-h))
            -2*native_odds(k,0))/(h*h)
        target=factor*m
        assert abs(q2-target)/abs(target)<.001
    return g,alpha,factor

if __name__=="__main__":
    refs={2:1.155885924e-311,9:.486548287616,10:.759460770278}
    for k,want in refs.items():
        g,alpha,factor=check(k)
        if k==2: assert abs(g-want)/want<1e-8
        else: assert abs(g-want)<1e-11
        print(f"PASS original k={k}, GOOD={g:.16g}, DJ/df={alpha:.16g}, Hessian/M={factor:.16g}")
    g10=native_good(10,0)
    fake=exp(-2*original_j(10,0))
    assert abs(fake-g10)>.1
    print("PASS Golden prefactor is mandatory: fake",fake,"actual",g10)
    if "--M" in sys.argv:
        import sympy as sp
        path=(Path(__file__).resolve().parents[1]
              /"d0_two_null_crossing_2026-10-19"/"check_mixed_cartan_exact.py")
        assert path.is_file(),str(path)
        M=runpy.run_path(str(path),run_name="not_main")["flat_hessian"]()
        assert M.shape==(24,24) and M.det()==256
        assert M.eigenvals()=={sp.Integer(2):4,sp.Integer(-2):4,
                              sp.Integer(1):8,sp.Integer(-1):8}
        print("PASS independently imported original M with 12+ and 12-")
    print("GR_closed=false; native physical Book admission remains open")
