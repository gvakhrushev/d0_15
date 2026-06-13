#!/usr/bin/env python3
"""vp_xi5_torus_defect.py — D0 certificate (exact arithmetic in Z[phi], no floats)

CLAIM (THE, promoted): xi5 is the integerization defect of the torus address.
    (i)   phi^5 = 11 + phi^-5            [exact identity in Z[phi]]
    (ii)  xi5 := phi^-5 = phi^5 - L5,  L5 = 11 = |V_11| (memory-torus zone)
    (iii) Tr(T^5) = -11 for the toral time operator T, chi_T = x^2 + x - 1
    => GOLDEN §52 address language "11 + xi5" is the exact odd-n Lucas identity;
       the alpha-form correction term is the torus-address rounding error.

STATUS BOUNDARY (per GOLDEN §16.3, unchanged):
    alpha^-1_top = 359/phi^2 - xi5 = 137.0356...  vs  exp 137.035999084
    residual Delta_alpha ~ 3.7e-4 remains CHK (declared gluing anomaly),
    NOT promoted to THE until Delta_alpha receives an analytic owner.
"""
from fractions import Fraction

# Z[phi] elements as (a, b) meaning a + b*phi, with phi^2 = phi + 1
def mul(x, y):
    a, b = x; c, d = y
    # (a+b phi)(c+d phi) = ac + (ad+bc) phi + bd phi^2 = (ac+bd) + (ad+bc+bd) phi
    return (a*c + b*d, a*d + b*c + b*d)

def power(x, n):
    r = (Fraction(1), Fraction(0))
    for _ in range(n):
        r = mul(r, x)
    return r

PHI = (Fraction(0), Fraction(1))

# (i) phi^5 exactly
p5 = power(PHI, 5)
assert p5 == (Fraction(3), Fraction(5)), p5          # phi^5 = 3 + 5 phi
# phi^-1 = phi - 1  (exact);  phi^-5 = (phi-1)^5
INV = (Fraction(-1), Fraction(1))
ip5 = power(INV, 5)
assert ip5 == (Fraction(-8), Fraction(5)), ip5       # phi^-5 = -8 + 5 phi
# identity: phi^5 - 11 = phi^-5  <=>  (3+5phi) - 11 = (-8+5phi)
lhs = (p5[0] - 11, p5[1])
assert lhs == ip5
print("[1] EXACT: phi^5 = 11 + phi^-5  (i.e. 3+5phi = 11 + (-8+5phi))  PASS")

# (ii) L5 via Galois trace: L5 = phi^5 + psi^5, psi = 1 - phi
PSI = (Fraction(1), Fraction(-1))
s5 = power(PSI, 5)
L5 = (p5[0] + s5[0], p5[1] + s5[1])
assert L5 == (Fraction(11), Fraction(0))
print("[2] EXACT: L5 = phi^5 + psi^5 = 11 = |V_11| (memory-torus zone)  PASS")
print("    => xi5 = phi^5 - L5 = -psi^5 = phi^-5 : torus-address integerization defect")

# (iii) toral time operator: integer matrix power
T = [[0, 1], [1, -1]]
def mmul(A, B):
    return [[A[0][0]*B[0][0]+A[0][1]*B[1][0], A[0][0]*B[0][1]+A[0][1]*B[1][1]],
            [A[1][0]*B[0][0]+A[1][1]*B[1][0], A[1][0]*B[0][1]+A[1][1]*B[1][1]]]
P = [[1,0],[0,1]]
for _ in range(5):
    P = mmul(P, T)
tr5 = P[0][0] + P[1][1]
assert tr5 == -11
print("[3] EXACT: Tr(T^5) = -11 = -(L5)  (5th time-return lands on the torus address)  PASS")

print("\n[STATUS] THE: xi5 = torus-address defect (items 1-3, exact).")
print("[STATUS] CHK (unchanged, per GOLDEN 16.3): alpha^-1 = 359/phi^2 - xi5;")
print("         residual Delta_alpha awaits an analytic owner before any promotion.")
print("[CERT-CLOSED] PASS_XI5_TORUS_DEFECT")
