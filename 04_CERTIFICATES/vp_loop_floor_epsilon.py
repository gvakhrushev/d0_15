#!/usr/bin/env python3
"""D0-GENERATIVE-DYNAMICS-001 (A.3) — loop floor epsilon^2 = phi^-16, no UV divergence.

The Feshbach-Schur series (vp_feshbach_schur_dynamics.py) is a sum over archive excursions; the
branch weight of a depth-k excursion is phi^-(2k) (each golden step costs phi^-2 in the
return-branch measure). The series TRUNCATES at the structural floor epsilon^2 = phi^-16: once
the cumulative branch weight drops below it there is no resolvable contribution. So a "loop" is a
FINITE memory cycle, not an integral to infinity -- there are no UV divergences in D0.

WHAT IS PROVED (exact Z[phi] / Fibonacci arithmetic, able to FAIL):
  * epsilon^2 = phi^-16 = (L_16 - F_16*sqrt5)/2 = (2207 - 987*sqrt5)/2 (exact), ~ 4.5317e-4.
  * The branch weight phi^-(2k) crosses the floor at 2k = 16, i.e. excursion depth k = 8
    (exponent 16): for k > 8 the weight phi^-(2k) < epsilon^2, so the series is finite.

HONESTY BOUNDARY (printed): epsilon^2 = phi^-16 ~ 4.532e-4 is CLOSE in order of magnitude to the
gluing anomaly Delta_alpha ~ 3.71e-4 (D0-DELTA-ALPHA-EXACT-001) but is NOT equal to it -- they
are different exact Q(phi) numbers (4.532e-4 vs 3.71e-4). NAMED GAP: do NOT identify the loop
floor with the gluing anomaly; they are kept distinct.
"""
from __future__ import annotations

import math
import sys
from fractions import Fraction as F

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


class Surd:
    def __init__(self, a, b=0):
        self.a, self.b = F(a), F(b)

    def __mul__(self, o):
        o = o if isinstance(o, Surd) else Surd(o)
        return Surd(self.a * o.a + 5 * self.b * o.b, self.a * o.b + self.b * o.a)

    def __eq__(self, o):
        o = o if isinstance(o, Surd) else Surd(o)
        return self.a == o.a and self.b == o.b

    def fval(self):
        return float(self.a) + float(self.b) * math.sqrt(5.0)


def phi_pow(n: int) -> Surd:
    """phi^n as an exact element a + b*sqrt5 (phi = 1/2 + 1/2 sqrt5; phi^-1 = -1/2 + 1/2 sqrt5)."""
    base = Surd(F(1, 2), F(1, 2)) if n >= 0 else Surd(F(-1, 2), F(1, 2))
    r = Surd(1)
    for _ in range(abs(n)):
        r = r * base
    return r


def main() -> int:
    print("=== D0-GENERATIVE-DYNAMICS-001 (A.3)  loop floor epsilon^2 = phi^-16 ===")

    eps2 = phi_pow(-16)
    # exact closed form: phi^-16 = (L_16 - F_16 sqrt5)/2 = (2207 - 987 sqrt5)/2
    assert eps2 == Surd(F(2207, 2), F(-987, 2)), f"phi^-16 exact form wrong: {eps2.a}+{eps2.b}sqrt5"
    assert abs(eps2.fval() - 4.5317e-4) < 1e-7, f"phi^-16 ~ 4.5317e-4, got {eps2.fval():.3e}"
    print(f"PASS_LOOP_FLOOR_EXACT  epsilon^2 = phi^-16 = (2207 - 987 sqrt5)/2 = {eps2.fval():.6e}")

    # branch weight phi^-(2k) crosses the floor at 2k = 16 (depth k = 8)
    weights = {k: phi_pow(-2 * k).fval() for k in range(0, 12)}
    assert weights[8] > 0 and abs(weights[8] - eps2.fval()) < 1e-12, "weight at k=8 equals the floor phi^-16"
    assert weights[9] < eps2.fval(), "k=9 weight is below the floor (series truncated)"
    assert all(weights[k] > eps2.fval() for k in range(0, 8)), "k<8 weights are above the floor"
    print("PASS_FINITE_TRUNCATION  branch weight phi^-(2k) < floor for k>8 => loop is a finite cycle, no UV divergence")

    # ---- negative control / honesty: epsilon^2 != Delta_alpha ----------------------
    delta_alpha = 3.71e-4   # |Delta_alpha| ~ 3.71e-4 (D0-DELTA-ALPHA-EXACT-001)
    assert abs(eps2.fval() - delta_alpha) > 5e-5, "control: phi^-16 (4.53e-4) != Delta_alpha (3.71e-4)"
    assert eps2.fval() > delta_alpha, "phi^-16 is larger than Delta_alpha (distinct numbers)"
    print(f"FAIL_LOOP_FLOOR_IS_NOT_DELTA_ALPHA  phi^-16={eps2.fval():.3e} != Delta_alpha~{delta_alpha:.3e}")
    print("PASS_LOOP_FLOOR_NEGATIVE_CONTROLS")

    print("HONEST_LOOP_FLOOR_PHI_M16_CLOSE_IN_ORDER_TO_DELTA_ALPHA_BUT_DISTINCT_DO_NOT_IDENTIFY")
    print("PASS_LOOP_FLOOR_EPSILON")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
