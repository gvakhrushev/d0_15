#!/usr/bin/env python3
"""D0-PI0-DISCRETE-ANGLE-001 — the seam angle 2π₀(2−φ) = 12/5 EXACTLY in ℚ(φ).

STRUCTURE (THE): π₀ = (6/5)φ² is the angular measure of the discrete minimal cycle, already derived
in BOOK_04 §04.6.π.4 from the δ₀-closure balance δ₀=(3/5)/(π₀φ) with δ₀=½φ⁻³ (REUSED here, not
re-derived). The NEW exact identity is that the seam holonomy angle

    θ_seam = 2·π₀·(2−φ) = 12/5   (exactly, in ℚ(φ), using φ²=φ+1)

is a closed rational — this is what makes the α holonomy angle (vp_seam_holonomy_alpha.py) exact.

DISCRIMINATOR (symbolic, honest): π₀ ≈ π numerically (π₀=(6/5)φ²≈3.14164), so substituting the
transcendental π does NOT grossly change α — therefore the π-vs-π₀ discriminator is the EXACTNESS of
12/5, NOT a gross-α miss. With π, 2π(2−φ) = 2.39996… ≠ 12/5 (irrational, not the closed rational).
This cert proves the exact identity in ℚ(φ) and shows π fails the exactness, without faking a gross test.
"""
from __future__ import annotations

import math
import sys
from fractions import Fraction as F

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PHI = (1.0 + 5.0 ** 0.5) / 2.0


# --- exact ℚ(φ) arithmetic: x = (a, b) means a + b·φ, with φ² = φ + 1 -------------
def mul(x, y):
    a, b = x
    c, d = y
    return (a * c + b * d, a * d + b * c + b * d)


def smul(c, x):
    return (c * x[0], c * x[1])


def add(*xs):
    return (sum(x[0] for x in xs), sum(x[1] for x in xs))


def val(x):
    return float(x[0]) + float(x[1]) * PHI


ONE = (F(1), F(0))
PHIv = (F(0), F(1))


def main() -> int:
    print("=== D0-PI0-DISCRETE-ANGLE-001  2·π₀·(2−φ) = 12/5 exactly in ℚ(φ),  π₀=(6/5)φ² ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: pi0=(6/5)phi^2 derived in BOOK_04 §04.6.π.4 (reused); "
          "phi^2=phi+1; angle target is the closed rational 12/5")

    phi2 = mul(PHIv, PHIv)
    assert phi2 == (F(1), F(1)), f"φ² must be 1+φ: {phi2}"
    print("PASS_PHI_SQ  φ² = 1 + φ  (exact)")

    pi0 = smul(F(6, 5), phi2)                       # π₀ = (6/5)φ²
    print(f"PASS_PI0_VALUE  π₀ = (6/5)φ² = {val(pi0):.10f}  (vs π = {math.pi:.10f}; π₀ is the discrete-cycle measure)")

    two_minus_phi = add(smul(F(2), ONE), smul(F(-1), PHIv))   # 2 − φ
    theta = smul(F(2), mul(pi0, two_minus_phi))               # 2·π₀·(2−φ)
    assert theta == (F(12, 5), F(0)), f"2·π₀·(2−φ) must equal the closed rational 12/5: {theta}"
    print(f"PASS_SEAM_ANGLE_EXACT  2·π₀·(2−φ) = 12/5  (exact in ℚ(φ): {theta})")

    # ---- THE 04.6.π.4 closure-balance FORCING (machine-checked: D0.Geometry.pi0_forced_by_closure_balance) ----
    # δ₀-closure δ₀ = 3/(5·π₀·φ) + owned δ₀ = 1/(2φ³)  ⟺  5·π₀·φ = 6·φ³  (cross-multiplied, exact ℚ(φ))
    phi3 = mul(phi2, PHIv)                                    # φ³ = 1 + 2φ
    assert phi3 == (F(1), F(2)), f"φ³ must be 1 + 2φ: {phi3}"
    lhs = smul(F(5), mul(pi0, PHIv))                          # 5·π₀·φ
    rhs = smul(F(6), phi3)                                    # 6·φ³  (= 3/δ₀, since δ₀ = 1/(2φ³))
    assert lhs == rhs, f"closure balance must force 5·π₀·φ = 6·φ³: {lhs} vs {rhs}"
    print(f"PASS_PI0_FORCED_BY_CLOSURE_BALANCE  5·π₀·φ = 6·φ³ exact ⟹ π₀=(6/5)φ² forced by the δ₀-closure  ({lhs})")
    pi0_bad = smul(F(5, 4), phi2)                             # a wrong cycle-closure ratio (ρ ≠ 3/5)
    assert smul(F(5), mul(pi0_bad, PHIv)) != rhs, "control: a wrong π₀ must break the closure balance"
    print("FAIL_WRONG_PI0_BREAKS_CLOSURE  π₀≠(6/5)φ² fails 5·π₀·φ=6·φ³ (the closure ratio 3/5 is forced)")

    # ---- NEGATIVE CONTROL: π (transcendental) does NOT give the closed rational 12/5 -------
    theta_pi = 2.0 * math.pi * (2.0 - PHI)
    assert abs(theta_pi - 2.4) > 1e-5, "control: with π the angle must NOT be exactly 12/5"
    print(f"FAIL_PI_NOT_EXACT_12_5  2π(2−φ) = {theta_pi:.10f} ≠ 12/5 = 2.4  (only π₀ closes the rational)")
    # honest: numerically π₀≈π so the α-level effect is tiny — the discriminator is exactness, not magnitude
    shift = abs(math.log(PHI) * PHI ** -17 * (math.sin(theta_pi) - math.sin(2.4)))
    print(f"HONEST_PI0_NEAR_PI  numeric α-shift from π-vs-π₀ is only {shift:.2e} (sub-measurement); "
          "the discriminator is the EXACT rational 12/5, not a gross miss")
    print("HONEST_PI0_VALUE_FORCED  π₀=(6/5)φ² is FORCED by the δ₀-closure balance (BOOK_04 §04.6.π.4), now "
          "machine-checked (D0.Geometry.pi0_forced_by_closure_balance); this cert also gives the exact 12/5 angle")

    print("PASS_PI0_DISCRETE_ANGLE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
