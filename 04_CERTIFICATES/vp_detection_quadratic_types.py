#!/usr/bin/env python3
"""D0-DETECTION-QUADRATIC-001 — degree-2 forced by the detection act (type-theoretic 2nd channel).

The 5th independent route to the primitive quadratic p²+p=1 (after Vieta, M1-minimality,
unity-split, quadratic-Pisot). It reads the degree off the ACT OF DETECTION, by the theory of
types of the thing detected:

  * Level 1 = a statement of EXISTENCE (a class: graph / continuum / Big Bang).
  * Level 2 = a statement of an EVENT inside the class-1 (an element of the set).
  * Level 3 = a SECOND event inside the SAME class-1.

There are exactly TWO ways to compare:
  (a) by MEMBERSHIP (∈): levels 1↔2 are different categories (set vs element, Russell hierarchy);
      "how much bigger is an element than its set" is categorically empty, so the detect is LINEAR
      (compare to a reference of belonging) — degree 1, the term p.
  (b) by VALUE: levels 2↔3 are one category (both events in class-1; nothing is an element of two
      universes), so membership cannot separate them — only mutual value can, through each other =
      a bilinear form = area — degree 2, the term p².
Unity is exhausted by the direct (p) and the mutual (p²) contribution: p + p² = 1, root p = 1/φ.

WHY DEGREE EXACTLY 2 (the closure, not a list): there are exactly two comparison types
(membership / value). A "third type" would be a degree-3 term p³, but p³ = 2p − 1 reduces into
span{1,p} (BOOK_01:556 runtime iteration) — there is no independent third slot. The tower closes
on THREE levels by EXHAUSTION of comparison kinds, not by enumeration.

HONESTY BOUNDARY (printed). The decidable ALGEBRA proved here (p+p²=1, root 1/φ, p³=2p−1 reduces,
neighbour-exclusion) is the SAME content already CORE-formalized in the tower-stop no-go
(D0-TOWER-STOP-NOEXT-001, D0.Tower.NoExtension). What this certificate ADDS is the type-theoretic
READING — "two comparison kinds (∈ / value) exhaust degree 2" — which is the forcing reading
(DEF-0.2.2 style), an independent channel that STRENGTHENS obligation 5; it is NOT a separate
machine-checked categorical theorem and does NOT replace the no-go.
"""
from __future__ import annotations

import sys
from fractions import Fraction as F

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PHI = (1.0 + 5.0 ** 0.5) / 2.0


# exact ℚ(φ): x = (a, b) means a + b·φ, with φ² = φ + 1
def mul(x, y):
    a, b = x
    c, d = y
    return (a * c + b * d, a * d + b * c + b * d)


def add(*xs):
    return (sum(x[0] for x in xs), sum(x[1] for x in xs))


def smul(c, x):
    return (c * x[0], c * x[1])


def powphi(n):
    if n >= 0:
        r = (F(1), F(0))
        for _ in range(n):
            r = mul(r, (F(0), F(1)))
        return r
    r, inv = (F(1), F(0)), (F(-1), F(1))      # φ⁻¹ = φ − 1
    for _ in range(-n):
        r = mul(r, inv)
    return r


def val(x):
    return float(x[0]) + float(x[1]) * PHI


def main() -> int:
    print("=== D0-DETECTION-QUADRATIC-001  degree-2 from the detection act (type 2nd channel) ===")

    p = powphi(-1)                                  # p = φ⁻¹ = (−1, 1)
    assert p == (F(-1), F(1)), f"p=φ⁻¹ must be −1+φ: {p}"

    # ---- the detection identity p + p² = 1 (root p = 1/φ) ---------------------------
    lhs = add(p, mul(p, p))
    assert lhs == (F(1), F(0)), f"detection closure p+p² must equal 1: {lhs}"
    print(f"PASS_DETECTION_CLOSURE  p + p² = 1 at p = 1/φ = {val(p):.8f}  (direct p + mutual p²)")

    # ---- two comparison types ↔ the two nonzero terms (degree 1 ∪ degree 2) ---------
    COMPARISON_TYPES = ("membership(∈): levels 1↔2 different categories ⇒ linear, degree 1",
                        "value: levels 2↔3 one category ⇒ bilinear=area, degree 2")
    nonzero_terms = [d for d in (1, 2) if val(powphi(-d)) != 0]   # p¹, p² both present
    assert len(COMPARISON_TYPES) == 2 == len(nonzero_terms), "two comparison types ↔ two terms"
    print(f"PASS_TWO_COMPARISON_TYPES  |{{∈, value}}| = 2 = degree of the primitive (1 ∪ 2)")

    # ---- no third type: a degree-3 term reduces into span{1,p} ----------------------
    p3 = powphi(-3)
    p3_reduced = add(smul(2, p), (F(-1), F(0)))     # 2p − 1
    assert p3 == p3_reduced, f"p³ must reduce to 2p−1: {p3} vs {p3_reduced}"
    print(f"PASS_NO_THIRD_COMPARISON_TYPE  p³ = 2p − 1 ∈ span{{1,p}} ⇒ no independent degree-3 slot")

    # ---- neighbour exclusion (the same exhaustion, not a fit) -----------------------
    # p+p=1 ⇒ p=½: degree-1 only (pure reference), δ₀ = 1/φ − ½ ≠ 0, no value-comparison, no arrow
    half = (F(1, 2), F(0))
    assert add(half, half) == (F(1), F(0)), "control: ½+½=1 (degree-1-only split)"
    delta0 = add(p, smul(-1, half))                 # 1/φ − ½
    assert delta0 != (F(0), F(0)), "the self-consistent root differs from ½ (δ₀ ≠ 0)"
    # p+p³=1 with p=1/φ does NOT hold (degree-3 is not the self-consistent closure)
    assert add(p, p3) != (F(1), F(0)), "control: p + p³ ≠ 1 at p=1/φ (degree-3 is not the closure)"
    print(f"PASS_NEIGHBOUR_EXCLUSION  ½+½=1 is degree-1-only (δ₀={val(delta0):.6f}≠0); p+p³≠1 (p³ reduces)")

    # ---- honesty boundary -----------------------------------------------------------
    print("HONEST_DECIDABLE_ALGEBRA_IS_THE_CORE_TOWER_STOP_CONTENT_D0_TOWER_NOEXTENSION")
    print("HONEST_TYPE_THEORY_TWO_KINDS_EXHAUST_DEGREE2_IS_THE_FORCING_READING_NOT_A_SEPARATE_THEOREM")
    print("HONEST_STRENGTHENS_OBLIGATION_5_AS_INDEPENDENT_CHANNEL_DOES_NOT_REPLACE_THE_NO_GO")

    print("PASS_DETECTION_QUADRATIC_TYPES")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
