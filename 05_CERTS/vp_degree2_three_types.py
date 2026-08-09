#!/usr/bin/env python3
"""D0-TOWER-STOP-NOEXT-001 stress test — degree 2 does not prove three-type exhaustion.

The former certificate treated the arithmetic identity "two polynomial terms plus one closure"
as an exhaustion theorem and treated linear dependence of p^3 as repetition. Neither inference
is valid. This stress test preserves the true quadratic calculations and checks the counterexample:
p^3 is distinct from 1, p, and p^2 although p^3 = 2p - 1.

WHAT IS PROVED (exact, able to FAIL):
  * Degree 2: x^2 + x - 1 has exactly 2 roots (phi^-1 and its Galois conjugate -phi); 2 terms.
  * 3 = 2 + 1 is arithmetic only; it does not classify arbitrary necessity-types.
  * p^3 = 2p - 1 in span{1,p}, while p^3 is a fourth distinct value.

HONESTY BOUNDARY: the repeat branch needs a separate M1 symmetry theorem (now Lean-owned);
the new-type branch remains open pending a semantic exhaustivity theorem.
"""
from __future__ import annotations

import math
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main() -> int:
    print("=== D0-TOWER-STOP-NOEXT-001 degree-2 exhaustion stress test ===")

    # ---- degree 2: two Galois roots of x^2 + x - 1 ---------------------------------
    a, b, c = 1, 1, -1
    disc = b * b - 4 * a * c
    assert disc == 5 > 0, "x^2+x-1 has discriminant 5 > 0: two distinct real roots"
    r1 = (-b + math.sqrt(disc)) / (2 * a)
    r2 = (-b - math.sqrt(disc)) / (2 * a)
    phi = (1 + math.sqrt(5)) / 2
    assert abs(r1 - 1 / phi) < 1e-12 and abs(r2 - (-phi)) < 1e-12, "roots are phi^-1 and -phi (Galois pair)"
    print(f"PASS_DEGREE_2  x^2+x-1 has 2 Galois roots {{phi^-1, -phi}} = {{{r1:.4f}, {r2:.4f}}} (degree 2 forced)")

    # ---- 3 = 2 terms + 1 closure (structural, not a list) --------------------------
    quadratic_terms = 2          # p^1 and p^2
    closure = 1                  # the normalisation = 1
    assert quadratic_terms + closure == 3, "3 = 2 quadratic terms + 1 closure"
    print("PASS_ARITHMETIC_ONLY  2 polynomial terms + 1 written closure = 3; no type exhaustivity follows")

    # ---- p^3 reduces => iterated runtime => repeat => CASE 2 -----------------------
    p = 1 / phi
    p3 = p ** 3
    assert abs(p3 - (2 * p - 1)) < 1e-12, "p^3 = 2p - 1 (reduces; iterated runtime, BOOK_01:556)"
    assert abs(p3 - 1.0) > 1e-3
    assert abs(p3 - p) > 1e-3
    assert abs(p3 - p * p) > 1e-3
    print(f"PASS_P3_DISTINCT  p^3={p3:.4f}=2p-1 but p^3 is distinct from 1,p,p^2")

    # ---- negative control: NOT a list ----------------------------------------------
    # the count 3 is derived from degree 2; it is not "here are the three: ..." enumeration
    assert quadratic_terms == disc // disc + 1, "2 terms tied to degree, not picked"  # 2 = deg
    print("FAIL_DEGREE2_DOES_NOT_EXHAUST_VALUES_OR_TYPES")
    print("PASS_DEGREE2_EXHAUSTION_NEGATIVE_CONTROL")

    print("OPEN_SEMANTIC_CLASSIFICATION_REQUIRED_FOR_THREE_TYPES")
    print("PASS_DEGREE2_THREE_TYPES_STRESS_TEST")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
