#!/usr/bin/env python3
"""Exact global modal history for actual original full128 round on flat shell.

Conditional on SAME Book/Born path-weight identification; no GR promotion.
The huge 128**n history collection is controlled by one first-difference bound.
"""
from fractions import Fraction as Q
import sympy as s

r5=s.sqrt(5);p=(r5-1)/2
h=s.Rational(1,4);ell=s.log(1/p)
lam=s.Rational(288,25);dlam_tr=-s.Rational(144,25)
eps=p*p*h*h/64
b=s.simplify(1-eps*lam/2)
q0=s.expand(b*b)
dq0=s.simplify(-b*eps*dlam_tr)
qcert=(5034167+28557*r5)/s.Integer(5120000)
dqcert=(42633-14157*r5)/s.Integer(5120000)
assert s.simplify(q0-qcert)==0
assert s.simplify(dq0-dqcert)==0

# Exact rational interval and strict n-step global-MAP certificate.
lo,hi=Q(9957,10000),Q(9958,10000)
assert s.simplify(q0-s.Rational(lo.numerator,lo.denominator)).is_positive
assert s.simplify(s.Rational(hi.numerator,hi.denominator)-q0).is_positive
n=1024
assert lo.numerator**n*10000 > 43*lo.denominator**n
# For any other full word, the FIRST nonblank/port0 is reached with
# probability <=q0**(j-1)*(1-q0)<=1-q0, its future <=1.
assert float(s.N(q0,40))**n > float(s.N(1-q0,40))

Smap=-n*s.log(q0)/ell
Dmap=-n*dq0/(q0*ell)
assert s.simplify(-dq0/(q0*ell)-eps*dlam_tr/(b*ell))==0
beta,t=s.symbols("beta t",positive=True)
assert s.simplify(s.limit(-2*(beta/t)*s.log(1-t*lam/2)/ell,t,0,dir="+")
                  -beta*lam/ell)==0
assert s.simplify(s.limit((beta/t)*t*dlam_tr/((1-t*lam/2)*ell),t,0,dir="+")
                  -beta*dlam_tr/ell)==0

print("PASS: original full128 q_blank0 and J23 source match pinned algebraic receipt")
print("PASS: exact rational certificate globally rules out all 128**1024 alternatives")
print(" q0^1024 =",format(float(s.N(q0,30))**n,'.16g'))
print(" 1-q0    =",s.N(1-q0,17))
print(" Unique modal word: full 1024 blank-label/port0 records")
print(" Conditional same-history modal Book code =",s.N(Smap,16))
print(" Actual J23 modal path first source       =",s.N(Dmap,16))
print("PASS: native fixed-clock continuum modal action beta*lambda/ln(phi)")
print("SCOPE: original flat-shell record; physical Book/Born map remains OPEN")
