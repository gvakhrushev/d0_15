#!/usr/bin/env python3
"""D0-LAPLACIAN-SPECTRUM-FIX-001 — reforge the §02.21 error: two matrices, two spectra.

Researcher doc 2 (§02.21) made a fixable error: it read "char.poly -> phi^-1" off the 3x3 zone
matrix M, but M is ROW-STOCHASTIC (rho(M)=1), so phi^-1 is NOT in its spectrum. The number it
actually hit (1.42 / 1.58) is the spectrum of (I - M), the S_DE relaxation window (Book 08) --
a DIFFERENT object from the fractal tick phi^-1 (Book 06 §06.2 envelope recursion). The error is
not discarded; it is reforged into the correct separation of two operators.

M = [[0, 11/24, 13/24], [9/22, 0, 13/22], [9/20, 11/20, 0]]  (row-stochastic zone matrix).

WHAT IS PROVED (exact rational + exact surd, able to FAIL):
  * M is row-stochastic: every row sums to 1, so rho(M)=1 (Perron eigenvalue exactly 1).
  * char poly of M factors exactly: (lambda - 1)(lambda^2 + lambda + 39/160); the other two
    eigenvalues are -1/2 +/- sqrt(10)/40 ~ -0.421, -0.579 (both |lambda|<1). NOT 1.42/1.58.
  * The researcher's quadratic 160 lambda^2 - 480 lambda + 359 (roots ~1.42, ~1.58) is the
    char poly of (I - M) under lambda -> 1 - lambda: its roots are 1 - (M-eigenvalues) =
    {1.421, 1.579} = the S_DE window (Book 08). It is the relaxation spectrum, not M's spectrum.
  * phi^-1 = (sqrt5-1)/2 ~ 0.618 (the fractal tick A_{n+1}=phi^-1 A_n, Book 06 §06.2) is NOT an
    eigenvalue of M and NOT in {1.42, 1.58}: it belongs to a DIFFERENT operator.

HONESTY BOUNDARY (printed): the fix separates THREE distinct numbers that were conflated --
M's spectrum {1, -0.421, -0.579}, the (I-M)/S_DE window {1.42, 1.58}, and the envelope tick
phi^-1. Two matrices, two spectra, two roles. This clarifies the Book02 <-> Book08 link.
"""
from __future__ import annotations

import math
import sys
from fractions import Fraction as F

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

M = [[F(0), F(11, 24), F(13, 24)],
     [F(9, 22), F(0), F(13, 22)],
     [F(9, 20), F(11, 20), F(0)]]


def main() -> int:
    print("=== D0-LAPLACIAN-SPECTRUM-FIX-001  two matrices, two spectra (reforge §02.21) ===")

    # ---- M is row-stochastic => rho(M)=1 -------------------------------------------
    for i, row in enumerate(M):
        assert sum(row) == 1, f"row {i} of M does not sum to 1 (not stochastic)"
    print("PASS_M_ROW_STOCHASTIC  every row sums to 1 => rho(M)=1 (Perron eigenvalue exactly 1)")

    # ---- exact char poly: e1=tr, e2=sum principal 2x2 minors, e3=det -----------------
    e1 = M[0][0] + M[1][1] + M[2][2]
    e2 = (M[0][0]*M[1][1]-M[0][1]*M[1][0]) + (M[0][0]*M[2][2]-M[0][2]*M[2][0]) + (M[1][1]*M[2][2]-M[1][2]*M[2][1])
    e3 = (M[0][0]*(M[1][1]*M[2][2]-M[1][2]*M[2][1])
          - M[0][1]*(M[1][0]*M[2][2]-M[1][2]*M[2][0])
          + M[0][2]*(M[1][0]*M[2][1]-M[1][1]*M[2][0]))
    assert e1 == 0 and e2 == F(-121, 160) and e3 == F(1287, 5280), f"char poly coeffs: {e1},{e2},{e3}"
    # char poly p(l) = l^3 - e1 l^2 + e2 l - e3 ; check l=1 is a root
    def p(l): return l**3 - e1*l**2 + e2*l - e3
    assert p(F(1)) == 0, "lambda=1 must be a root (stochastic)"
    # factor (l-1): quotient l^2 + l + 39/160
    assert e2 == F(-121, 160) and (F(1) + e2) == F(39, 160) - F(0), "quotient constant 39/160"
    # discriminant of l^2 + l + 39/160 is 1 - 4*39/160 = 1/40
    disc = F(1) - 4*F(39, 160)
    assert disc == F(1, 40), f"discriminant must be 1/40, got {disc}"
    lam2 = -0.5 + math.sqrt(1/40)/2
    lam3 = -0.5 - math.sqrt(1/40)/2
    assert abs(lam2 - (-0.421)) < 0.01 and abs(lam3 - (-0.579)) < 0.01, "M eigenvalues ~ -0.421,-0.579"
    assert abs(lam2) < 1 and abs(lam3) < 1, "subdominant eigenvalues inside unit disk"
    print(f"PASS_M_SPECTRUM  eigenvalues of M = {{1, -1/2+/-sqrt(10)/40}} = {{1, {lam2:.3f}, {lam3:.3f}}} (NOT 1.42/1.58)")

    # ---- the researcher's 160 l^2 - 480 l + 359 is char poly of (I-M) ---------------
    # roots of 160 l^2 - 480 l + 359:
    a, b, c = 160, -480, 359
    r1 = (-b + math.sqrt(b*b - 4*a*c)) / (2*a)
    r2 = (-b - math.sqrt(b*b - 4*a*c)) / (2*a)
    assert abs(r1 - 1.579) < 0.01 and abs(r2 - 1.421) < 0.01, "1.42/1.58 are the roots"
    # they equal 1 - (eigenvalues of M): 1-(-0.579)=1.579, 1-(-0.421)=1.421
    assert abs(r1 - (1 - lam3)) < 1e-9 and abs(r2 - (1 - lam2)) < 1e-9, "1.42/1.58 = 1 - eig(M) = eig(I-M)"
    print(f"PASS_S_DE_WINDOW_IS_I_MINUS_M  {{1.42,1.58}} = eig(I-M) = 1 - eig(M) = S_DE window (Book 08), NOT M's spectrum")

    # ---- phi^-1 is a DIFFERENT operator (envelope tick, §06.2) ----------------------
    phi_inv = (math.sqrt(5) - 1) / 2
    assert abs(phi_inv - 0.618034) < 1e-5
    assert all(abs(phi_inv - x) > 0.03 for x in (1.0, lam2, lam3)), "phi^-1 is not an eigenvalue of M"
    assert all(abs(phi_inv - x) > 0.5 for x in (r1, r2)), "phi^-1 is not in the S_DE window 1.42/1.58"
    print(f"PASS_PHI_INV_IS_DIFFERENT_OPERATOR  phi^-1={phi_inv:.6f} (envelope tick §06.2) not in spec(M) nor S_DE window")

    # ---- negative control: the original wrong reading ------------------------------
    # "char.poly of M -> phi^-1" is false: phi^-1 solves neither p(l)=0 nor 160l^2-480l+359=0
    assert abs(float(p(F(phi_inv).limit_denominator(10**6)))) > 1e-3, "phi^-1 does not solve char poly of M"
    print("FAIL_PHI_INV_DOES_NOT_SOLVE_CHARPOLY_OF_M_THE_ORIGINAL_ERROR")
    print("PASS_LAPLACIAN_FIX_NEGATIVE_CONTROLS")

    print("HONEST_THREE_NUMBERS_SEPARATED_SPEC_M_VS_S_DE_WINDOW_VS_PHI_INV_TICK_TWO_MATRICES")
    print("PASS_LAPLACIAN_3X3_CORRECT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
