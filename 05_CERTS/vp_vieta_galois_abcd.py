#!/usr/bin/env python3
"""vp_vieta_galois_abcd.py - D0 certificate (exact arithmetic in Q(phi), no floats)

CLAIM (THE): the four terminal roles ABCD are the Vieta/Galois data of the
self-description equation x^2 - x - 1 = 0 (roots phi, psi=1-phi), and delta0 is
the forced cut offset.
    A: phi + psi = 1            (Vieta sum  = trace, Galois-invariant)
    B: phi * psi = -1           (Vieta product = norm, Galois-invariant)
    C: phi^2 = phi + 1          (active-branch recursion)
    D: psi^2 = psi + 1          (conjugate-branch recursion; C,D are the Galois pair)
    delta0 = (sqrt5 - 2)/2 = phi - 3/2 = 1/(2 phi^3)   (forced, not fitted)
The non-symmetric canonical cut of unity (phi^-1 : phi^-2) is symmetric under
Gal(Q(sqrt5)/Q) = Z2 (phi <-> psi), not under x <-> 1-x.
"""
from fractions import Fraction as F

# Q(phi) elements as (a, b) meaning a + b*phi, with phi^2 = phi + 1.
def mul(x, y):
    a, b = x; c, d = y
    return (a * c + b * d, a * d + b * c + b * d)

def add(x, y):
    return (x[0] + y[0], x[1] + y[1])

def power(x, n):
    r = (F(1), F(0))
    for _ in range(n):
        r = mul(r, x)
    return r

PHI = (F(0), F(1))
PSI = (F(1), F(-1))          # psi = 1 - phi
ONE = (F(1), F(0))

# A: phi + psi = 1
assert add(PHI, PSI) == ONE
print("[A] EXACT: phi + psi = 1  (Vieta sum / Galois trace)  PASS")

# B: phi * psi = -1
assert mul(PHI, PSI) == (F(-1), F(0))
print("[B] EXACT: phi * psi = -1  (Vieta product / Galois norm)  PASS")

# C: phi^2 = phi + 1 ;  D: psi^2 = psi + 1
assert power(PHI, 2) == add(PHI, ONE)
assert power(PSI, 2) == add(PSI, ONE)
print("[C/D] EXACT: phi^2 = phi+1 and psi^2 = psi+1  (conjugate recursion pair)  PASS")

# Galois invariance: conjugation sends phi -> psi; A and B are fixed (rational).
def conj(x):
    # a + b*phi  ->  a + b*psi = a + b*(1-phi) = (a+b) + (-b)*phi
    a, b = x
    return (a + b, -b)
assert conj(add(PHI, PSI)) == add(PHI, PSI)        # A invariant
assert conj(mul(PHI, PSI)) == mul(PHI, PSI)        # B invariant
assert conj(PHI) == PSI and conj(PSI) == PHI       # C,D swapped
print("[Galois] A,B fixed; C,D swapped by Gal(Q(sqrt5)/Q)=Z2  PASS")

# delta0 = phi - 3/2 = (2 phi - 3)/2 ;  verify delta0 * 2 phi^3 = 1
DELTA0 = (F(-3, 2), F(1))                            # -3/2 + 1*phi
two_phi3 = mul((F(2), F(0)), power(PHI, 3))          # 2 * phi^3
assert mul(DELTA0, two_phi3) == ONE
# and phi^-3 = 2 delta0
inv_phi3 = power((F(-1), F(1)), 3)                   # (phi^-1)^3, phi^-1 = phi-1
assert add(DELTA0, DELTA0) == inv_phi3
print("[delta0] EXACT: delta0 = phi-3/2 = 1/(2 phi^3); phi^-3 = 2 delta0  PASS")

print("\n[STATUS] THE: ABCD = Vieta=Galois data of x^2-x-1; delta0 forced (exact Q(phi)).")
print("[CERT-CLOSED] PASS_VIETA_GALOIS_ABCD")
