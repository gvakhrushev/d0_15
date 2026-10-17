#!/usr/bin/env python3
"""Exact local golden Bernoulli/Jacobi focusing diagnostic for D0 Draft #334.

Tests a HYPOTHETICAL complete two-outcome area-sensitive readout, not
native D0 gate admission or the full historical tape/Cost-Info price.
No old root/certificate/Lean computations are repeated.
"""
import sympy as S

p = (S.sqrt(5)-1)/2
phi = (1+S.sqrt(5))/2
ell = S.log(phi)
t, Ric = S.symbols("s Ric", real=True)
w = 1 - Ric*t**2/2  # exact second jet of screen-area / area(0)
N = p*w+p**2
q = S.factor(p*w/N)


def check(ok, name):
    if not bool(ok):
        raise RuntimeError(name)


check(S.simplify(p+p**2-1)==0, "golden normalization")
check(S.simplify(N.subs(t,0)-1)==0, "moving raw N0")
check(S.simplify(q.subs(t,0)-p)==0, "complete output preparation")
check(S.simplify(S.diff(q,t).subs(t,0))==0, "normal initial pencil")
q2 = S.simplify(S.diff(q,t,2).subs(t,0))
n2 = S.simplify(S.diff(S.log(N),t,2).subs(t,0))
check(S.simplify(q2+p**3*Ric)==0, "normalization-corrected probability jet")
check(S.simplify(n2+p*Ric)==0, "nonfrozen raw-normalizer jet")
Hprime_at_p = S.log((1-p)/p)
check(S.simplify(Hprime_at_p+ell)==0, "golden entropy slope")
H2 = Hprime_at_p*q2
check(S.simplify(H2/ell-p**3*Ric)==0, "linear Shannon Ricci response")
cost2 = H2/ell-n2/ell
check(S.simplify(cost2-(p**3+p/ell)*Ric)==0, "moving-weight Cost-Info jet")
D2 = S.Integer(0)  # D(q||p) is quadratically flat at q=p and q'(0)=0
D4coeff = S.simplify(q2**2/(8*p*(1-p)))
check(S.simplify(D4coeff-p**3*Ric**2/8)==0, "KL fourth-order obstruction")
check(S.simplify(D2)==0, "KL cannot supply Ric at second order")
check(S.simplify(S.log((1-S.Rational(1,2))/S.Rational(1,2)))==0,
      "balanced prior has no first-order entropy slope")
print("PASS complete golden probabilities and moving-normalizer source")
print("PASS Shannon null Ricci coefficient p^3, raw-price p^3+p/log(phi)")
print("PASS symmetric KL second-source zero, fourth coefficient p^3 Ric^2/8")
print("p^3 =", S.simplify(p**3), "=", S.N(p**3,12))
