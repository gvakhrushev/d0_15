#!/usr/bin/env python3
"""T3 CORRECTED check (v2, supersedes t3_hull_v4_check.py's implementation).
Corrections: (1) the golden datum enters the owned hull product as the FORCED SCALE
eps^2 = phi^-16 (u = eps^2 t, 06.30a FORCED) — not as a generator summand (G_space is the
SPATIAL generator; the toral pair is tick/Floquet data); the joint decay exponents of the
product flow are eps^2 * lambda_window. (2) field automorphisms implemented in the explicit
basis (a + b*sqrt2 + c*sqrt5 + d*sqrt10) — symbol-level sqrt-flips are NOT automorphisms once
sqrt2*sqrt5 products appear (sympy auto-merges to sqrt10; the v1 sum-form check was valid only
because sums produce no cross products).
Verifies: V4 acts simply transitively on the joint-exponent quadruple, factor-wise:
flip-sqrt2 (fix Q(sqrt5)) = window swap alone; flip-both (fix Q(sqrt10)) = golden conj alone;
flip-sqrt5 (fix Q(sqrt2)) = double swap; orbit generates K. Negative control: a non-automorphism
scaling of sqrt10 leaves the orbit. Exit 1 on failure."""
from fractions import Fraction as F
import sys

def mul(x, y):
    a,b,c,d = x; e,f,g,h = y
    return (a*e + 2*b*f + 5*c*g + 10*d*h,
            a*f + b*e + 5*(c*h + d*g),
            a*g + c*e + 2*(b*h + d*f),
            a*h + d*e + b*g + c*f)
def aut(x, f2, f5):
    a,b,c,d = x
    s2 = -1 if f2 else 1; s5 = -1 if f5 else 1
    return (a, s2*b, s5*c, s2*s5*d)

eps2  = (F(2207,2), F(0), F(-987,2), F(0))    # phi^-16 = (L16 - F16*sqrt5)/2, owned forced scale
w0    = (F(3,2), F(0), F(0), F(-1,40))         # archive window lambda_c
w1    = (F(3,2), F(0), F(0), F(+1,40))         # lambda_r
eps2c = aut(eps2, 0, 1)
e00   = mul(eps2, w0)

ok = True
def check(name, cond):
    global ok
    print(("PASS " if cond else "FAIL ")+name); ok = ok and bool(cond)

check("flip sqrt2 (fix Q(sqrt5)) = window swap only",  aut(e00,1,0) == mul(eps2,  w1))
check("flip both (fix Q(sqrt10)) = golden conj only",  aut(e00,1,1) == mul(eps2c, w0))
check("flip sqrt5 (fix Q(sqrt2)) = double swap",       aut(e00,0,1) == mul(eps2c, w1))
orbit = {aut(e00,a,b) for a in (0,1) for b in (0,1)}
check("V4 simply transitive on the joint-exponent quadruple", len(orbit) == 4)
check("orbit generates K (all four basis components hit)", all(any(x[i]!=0 for x in orbit) for i in range(4)))
bad = mul(e00, (F(1),F(0),F(0),F(1)))  # multiply by (1+sqrt10): NOT an automorphism image
check("negative control: non-automorphism image leaves the orbit", bad not in orbit)
print("RESULT:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
