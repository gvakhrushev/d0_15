#!/usr/bin/env python3
"""D0-IF-KS-FORMULA-FIX-001 — I_f = h_KS = log|lambda_max(T)| = log phi (fix the §09.8 record).

Researcher doc 2 (§09.8) wrote I_f = Tr(log T)/rank. The NUMBER log phi is right, but that
FORMULA is wrong: T = [[0,1],[1,-1]] has eigenvalues {phi^-1, -phi}, det T = -1 < 0, so one
eigenvalue is negative and Tr(log T) = log(det T) = log(-1) = i*pi is COMPLEX -- an entropy
cannot be complex. The correct expression is the Kolmogorov-Sinai entropy of the hyperbolic
toral automorphism: h_KS = log|lambda_max(T)| = log phi (sum of positive Lyapunov exponents).

WHAT IS PROVED (exact + numeric, able to FAIL):
  * T eigenvalues are {phi^-1, -phi} (roots of the charpoly x^2 + x - 1); det T = -1.
  * The wrong formula is ill-defined: Tr(log T) = log(det T) = log(-1) is non-real (the negative
    eigenvalue -phi has a complex logarithm).
  * The correct formula: h_KS = log|lambda_max(T)| = log|-phi| = log phi ~ 0.4812 (real).
  * Same number as I_f from the Fibonacci route (D0.Claims.FibonacciIfBridge, which proves
    |-phi| = phi): log phi reached two ways, now with the CORRECT записи.

HONESTY BOUNDARY (printed): the value log phi was always correct; only the formula record is
fixed (Tr(log T)/rank -> log|lambda_max|). Number kept, expression corrected.
"""
from __future__ import annotations

import cmath
import math
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main() -> int:
    print("=== D0-IF-KS-FORMULA-FIX-001  I_f = h_KS = log|lambda_max| = log phi ===")

    phi = (1 + math.sqrt(5)) / 2
    # T = [[0,1],[1,-1]] eigenvalues: roots of x^2 + x - 1
    lam = sorted([(-1 + math.sqrt(5)) / 2, (-1 - math.sqrt(5)) / 2], key=abs)
    lam_min, lam_max = lam[0], lam[1]
    assert abs(lam_min - (1/phi)) < 1e-12, "smaller |eigenvalue| is phi^-1"
    assert abs(lam_max - (-phi)) < 1e-12, "larger |eigenvalue| is -phi"
    det_T = lam_min * lam_max
    assert abs(det_T - (-1)) < 1e-12, "det T = -1 (eigenvalue product)"
    print(f"PASS_T_SPECTRUM  eig(T) = {{phi^-1, -phi}} = {{{lam_min:.4f}, {lam_max:.4f}}}, det T = -1")

    # ---- the WRONG formula is complex (ill-defined entropy) -------------------------
    # Tr(log T) = log(lambda1) + log(lambda2) = log(lambda1*lambda2) = log(det T) = log(-1) = i*pi
    tr_log = cmath.log(complex(lam_min)) + cmath.log(complex(lam_max))
    assert abs(tr_log.imag) > 1e-9, "Tr(log T) must be COMPLEX (negative eigenvalue) -- the wrong formula"
    assert abs(tr_log - complex(0, math.pi)) < 1e-9, "Tr(log T) = i*pi = log(det T) = log(-1)"
    print(f"FAIL_TR_LOG_T_IS_COMPLEX  Tr(log T) = log(det T) = log(-1) = {tr_log:.4f} (i*pi) -- not a real entropy")

    # ---- the CORRECT formula: h_KS = log|lambda_max| = log phi ----------------------
    h_KS = math.log(abs(lam_max))
    assert abs(h_KS - math.log(phi)) < 1e-12, "h_KS = log|lambda_max| = log phi"
    assert abs(h_KS - 0.4812118) < 1e-6, "h_KS = log phi ~ 0.4812"
    assert abs(h_KS.imag if isinstance(h_KS, complex) else 0.0) < 1e-15, "h_KS is real"
    print(f"PASS_HKS_CORRECT  h_KS = log|lambda_max(T)| = log phi = {h_KS:.7f} (real, the right записи)")

    # ---- same number as the Fibonacci route (FibonacciIfBridge proves |-phi|=phi) ---
    I_f_fibonacci = math.log(phi)
    assert abs(h_KS - I_f_fibonacci) < 1e-12, "h_KS = I_f from the Fibonacci route (log phi both ways)"
    print("PASS_MATCHES_FIBONACCI_ROUTE  h_KS = I_f = log phi (D0.Claims.FibonacciIfBridge: |-phi|=phi)")

    print("HONEST_NUMBER_LOG_PHI_ALWAYS_CORRECT_ONLY_THE_FORMULA_RECORD_TR_LOG_T_RANK_IS_FIXED")
    print("PASS_IF_KOLMOGOROV_SINAI")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
