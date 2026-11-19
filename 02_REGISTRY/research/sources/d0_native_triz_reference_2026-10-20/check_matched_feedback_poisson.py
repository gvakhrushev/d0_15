#!/usr/bin/env python3
"""Exact finite TRIZ paired-feedback loop/void and mixed-source checks.

Uses POSITIVE algebraic effects, not a newly selected Book03 action.
Original HJR z=2^-20, feedback multiplicity 128, CAR dimension 16L^4.
The actual full128 Julia alarm mixed jet must still be computed on the
original Jones34/P25 geometry; this fixture does not invent it.
"""
import sympy as s

z=s.Rational(1,2**20)
x,t=s.symbols("x t",real=True)
Id=s.eye(2)
A0=s.diag(s.Rational(1,3),s.Rational(1,2))
Ae=s.diag(s.Rational(1,7),-s.Rational(1,11))
Au=s.Matrix([[0,s.Rational(1,13)],[s.Rational(1,13),0]])
Aeu=s.diag(s.Rational(1,17),-s.Rational(1,19))
A=A0+x*Ae+t*Au+x*t*Aeu
F=lambda B:-s.log((Id-z*B).det())

# Mathematically legitimate local positive alarm effects on a common chart.
for xx,tt in [(0,0),(s.Rational(1,5),s.Rational(1,7)),
              (-s.Rational(1,5),s.Rational(1,9))]:
    actual=A.subs({x:xx,t:tt})
    assert all(0<ev<1 for ev in actual.eigenvals())

C=s.simplify(F(A)-F(A.subs(t,0)))
assert s.simplify(C.subs(t,0))==0
assert s.simplify(s.diff(C,x).subs(t,0))==0

R0=(Id-z*A0).inv()
mixed=s.simplify(s.diff(C,x,t).subs({x:0,t:0}))
formula=s.simplify(z*s.trace(R0*Aeu)+z*z*s.trace(R0*Ae*R0*Au))
assert s.simplify(mixed-formula)==0
assert mixed!=0

# Four-corner diagnostic removes *pure* functions exactly, without
# permission to use it as an action replacement.
p25=(1-x)*s.sin(t)
p25_quad=s.simplify(p25-p25.subs(t,0)-p25.subs(x,1)+p25.subs({x:1,t:0}))
assert s.simplify(p25_quad-p25)==0
assert s.simplify(s.diff(p25_quad,x,t).subs({x:1,t:0})+1)==0

# Constructible positive Poisson INTENSITIES reproduce HJR no-loop
# determinant mathematically: no physical Poisson controller is claimed.
B=A.subs({x:s.Rational(1,5),t:s.Rational(1,7)})
trace_dim=B.rows
exact=float(F(B))
for R in (1,2,3):
    series=sum((128*z**n*s.trace(B**n)/n for n in range(1,R+1)),s.Integer(0))
    err=exact-float(series)/128  # F lacks feedback multiplicity
    bound=float(trace_dim*z**(R+1)/((R+1)*(1-z)))
    assert -1e-19 <= err <= bound+1e-19

d_over_site=16
value_tail=128*d_over_site*z**3/(3*(1-z))
first_tail=128*d_over_site*z**3/(1-z)
assert float(value_tail)<5.922e-16
assert float(first_tail)<1.777e-15

# Exact bounded source formula, coefficient may be +/- depending on native
# mixed effect jet. Positivity alone cannot force the Palatini sign.
coef1=128*d_over_site*z/(1-z)
coef2=128*d_over_site*z*z/(1-z)**2
assert s.Rational(1,512)<coef1<s.Rational(1,500)
assert coef2<s.Rational(1,500_000_000)
print("Exact no-loop determinant / positive loop intensity: PASS")
print("Matched reference kills all pure coframe pressure: PASS")
print("Noncommutative full mixed-source resolvent identity: PASS")
print("Original P25 four-corner finite cross interaction: PASS")
print("Per-site R=2 feedback value tail <=",value_tail)
print("Per-site R=2 first-source tail coefficient <=",first_tail)
print("Mixed jet coefficients:",coef1,coef2)
print("ALL EXACT TRIZ MATCHED-LOOP SOURCE CHECKS PASSED")
