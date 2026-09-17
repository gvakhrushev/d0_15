#!/usr/bin/env python3
"""D0-FIBONACCI-IF-FORCING-001 — I_f = log phi from two independent routes (LEM).

Self-calibrated status: LEM, NOT forcing/THE. Both the Fibonacci quantum dimension and the
toral automorphism give log phi, but the categorical<->toral ISOMORPHISM is not constructed.
We certify the "one number, two computations" fact and NAME the open isomorphism gap. Do not
inflate to THE on the strength of a coincident number (M1 at the meta-level).

TWO INDEPENDENT COMPUTATIONS OF phi (exact):
  * Fibonacci anyons: d_tau = phi is the unique POSITIVE root of the fusion relation
    d^2 = d + 1 (tau (x) tau = 1 (+) tau; Nayak et al., Rev. Mod. Phys. 80, 1083, 2008).
    Hilbert-space growth ~ phi^n => distinguishability per step = log phi = I_f.
  * Toral automorphism: T = [[0,1],[1,-1]] has characteristic polynomial x^2 + x - 1
    (trace -1, det -1), roots (-1 +/- sqrt5)/2 = {phi^-1, -phi}; the spectral RADIUS is
    |lambda_max| = |-phi| = phi => Kolmogorov-Sinai entropy h_KS = log|lambda_max| = log phi.

So I_f = log phi = h_KS: the SAME number phi reached two ways.

WHAT IS PROVED (exact, able to FAIL):
  * d_tau = phi satisfies d^2 = d + 1 (fusion), and the conjugate root < 0 is rejected
    (a quantum dimension is >= 1) => phi is the UNIQUE admissible fusion dimension.
  * -phi satisfies the toral charpoly x^2 + x - 1 = 0, and |-phi| = phi is the spectral
    radius (|phi^-1| < |-phi|) => h_KS = log phi.
  * The two arguments coincide exactly: d_tau = |lambda_max(T)| = phi.

HONESTY BOUNDARY (printed, not hidden):
  * The two routes give the SAME log phi, but the ISOMORPHISM between the Fibonacci-category
    state growth (~phi^n) and the symbolic dynamics of T (h_KS = log phi) is NOT constructed
    here. In D0 distinguishability = information, so "growth of distinguishable states" and
    "rate of information production" SHOULD be one object -- but that map must be exhibited,
    not postulated. Status: LEM (named gap "both give log phi; categorical<->toral iso open").
  * The two quadratics differ by a sign (x^2-x-1 for the fusion dim vs x^2+x-1 for the toral
    charpoly); phi and -phi are DIFFERENT roots that share the magnitude phi. Not conflated.
"""
from __future__ import annotations

import math
import sys
from fractions import Fraction as F

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


class Surd:
    """Exact a + b*sqrt5 over Q."""

    def __init__(self, a, b=0):
        self.a, self.b = F(a), F(b)

    def __add__(self, o):
        o = o if isinstance(o, Surd) else Surd(o)
        return Surd(self.a + o.a, self.b + o.b)

    def __sub__(self, o):
        o = o if isinstance(o, Surd) else Surd(o)
        return Surd(self.a - o.a, self.b - o.b)

    def __mul__(self, o):
        o = o if isinstance(o, Surd) else Surd(o)
        return Surd(self.a * o.a + 5 * self.b * o.b, self.a * o.b + self.b * o.a)

    def __eq__(self, o):
        o = o if isinstance(o, Surd) else Surd(o)
        return self.a == o.a and self.b == o.b

    def fval(self):
        return float(self.a) + float(self.b) * math.sqrt(5.0)


def main() -> int:
    print("=== D0-FIBONACCI-IF-FORCING-001  I_f = log phi via two routes (LEM) ===")

    phi = Surd(F(1, 2), F(1, 2))       # (1+sqrt5)/2
    neg_phi = Surd(F(-1, 2), F(-1, 2))  # -(1+sqrt5)/2
    phi_inv = Surd(F(-1, 2), F(1, 2))   # (-1+sqrt5)/2 = phi^-1 (other toral root)
    one = Surd(1)

    # ---- route 1: Fibonacci fusion d^2 = d + 1, positive root unique --------------
    assert phi * phi == phi + one, "d_tau=phi must satisfy d^2=d+1 (fusion)"
    conj = Surd(F(1, 2), F(-1, 2))      # (1-sqrt5)/2, the conjugate fusion root
    assert conj * conj == conj + one, "conjugate also solves d^2=d+1"
    assert conj.fval() < 0 < phi.fval(), "conjugate < 0 < phi"
    assert phi.fval() >= 1.0, "a quantum dimension is >= 1, so phi is the unique admissible root"
    print(f"PASS_FUSION_DIM  d_tau = phi = {phi.fval():.9f} unique positive root of d^2=d+1")

    # ---- route 2: toral charpoly x^2 + x - 1, spectral radius = phi ----------------
    # T=[[0,1],[1,-1]]: trace -1, det -1 => charpoly x^2 - (trace)x + det = x^2 + x - 1.
    def charpoly(x: Surd) -> Surd:
        return x * x + x - one
    assert charpoly(neg_phi) == Surd(0), "-phi must satisfy the toral charpoly x^2+x-1"
    assert charpoly(phi_inv) == Surd(0), "phi^-1 must satisfy the toral charpoly x^2+x-1"
    assert abs(neg_phi.fval()) > abs(phi_inv.fval()), "|-phi| > |phi^-1| (spectral radius is |-phi|)"
    spectral_radius = abs(neg_phi.fval())
    assert abs(spectral_radius - phi.fval()) < 1e-12, "spectral radius |lambda_max(T)| = phi"
    print(f"PASS_TORAL_SPECTRAL_RADIUS  |lambda_max(T)| = |-phi| = {spectral_radius:.9f} = phi")

    # ---- the two arguments coincide => I_f = log phi = h_KS ------------------------
    I_f = math.log(phi.fval())
    h_KS = math.log(spectral_radius)
    assert abs(I_f - h_KS) < 1e-12, "I_f = log phi must equal h_KS = log|lambda_max(T)|"
    print(f"PASS_IF_EQUALS_HKS  I_f = log phi = h_KS = {I_f:.9f} (same number, two routes)")

    # ---- negative controls (must hold) ---------------------------------------------
    # the fusion quadratic and the toral charpoly differ by a sign; do not conflate roots
    assert phi * phi - phi - one == Surd(0), "phi solves x^2-x-1 (fusion), not x^2+x-1"
    assert not (charpoly(phi) == Surd(0)), "control: phi does NOT solve the toral charpoly x^2+x-1"
    # the conjugate fusion root is not a quantum dimension
    assert conj.fval() < 1.0, "control: conjugate root < 1 cannot be a quantum dimension"
    print("FAIL_PHI_DOES_NOT_SOLVE_TORAL_CHARPOLY_x2_plus_x_minus_1")
    print("FAIL_CONJUGATE_ROOT_NOT_A_QUANTUM_DIMENSION")
    print("PASS_FIBONACCI_NEGATIVE_CONTROLS")

    # ---- honesty boundary ----------------------------------------------------------
    print("HONEST_TWO_ROUTES_GIVE_SAME_LOG_PHI_BUT_CATEGORICAL_TORAL_ISOMORPHISM_NOT_CONSTRUCTED")
    print("HONEST_STATUS_LEM_NOT_THE_NAMED_GAP_FIB_CATEGORY_TO_TORAL_T_MAP_OPEN")

    print("PASS_FIBONACCI_IF_BRIDGE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
