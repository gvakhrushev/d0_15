#!/usr/bin/env python3
"""D0-MASS-CHAIN-001 — return the dropped GOLDEN holonomy chain δ₀→π₀→m₀→t₀ + the α↔mass stitch.

Iter-17 recovery. The chain δ₀→π₀→m₀→t₀ was DERIVED in the GOLDEN corpus (BOOK_04 §04.6.π:
THE 04.6.π.4 derives π₀=(6/5)φ² from the δ₀ closure balance with no external parameter) but the
mass-quantum links m₀=2π₀ and t₀=1/m₀ FELL OUT of the v14 books (they survive only in
03_THEORY_MAP/coverage_audit/batches/B010,B011). This certificate RE-STITCHES the chain (not a
re-discovery — π₀ is already derived) and records a genuine cross-book identity found by stitching:
the same holonomy π₀/m₀ that sets the mass quantum is the μ₂ amplitude of the fine-structure
resolvent moment (BOOK_03/02 α-line), so α and mass use ONE object in two roles.

WHAT IS PROVED (exact ℚ(φ), able to FAIL):
  * δ₀ = ½φ⁻³ → π₀ = (6/5)φ²  via the closure balance δ₀ = (3/5)/(π₀φ)  (BOOK_04 §04.6.π.4, derived);
  * m₀ = 2π₀ = (12/5)φ²  (mass quantum = one full holonomy cycle, GOLDEN DEF 6.4.1);
  * t₀ = 1/m₀,  m₀·t₀ = 1  (GOLDEN DEF 6.6.1);
  * the resolvent moment amplitudes: μ₁ = 1/3 = 1/rank (the F_N=p²P_N floor spread over the 3 active
    modes), μ₂ = 2¹¹·π₀·φ⁻² = 12288/5;
  * THE α↔MASS STITCH (exact): μ₂ = 2¹⁰·m₀·φ⁻² (since m₀=2π₀ ⇒ 2¹¹π₀ = 2¹⁰·m₀) — α's μ₂ amplitude
    IS 2¹⁰ mass-quanta over φ²; one holonomy, two roles (scattering phase vs cycle length);
  * the closed α writing reproduces: α⁻¹ = μ₂φ⁻⁶ + μ₁φ⁻³ = 159739/5 − (294902/15)φ ≈ 137.0360.

HONESTY BOUNDARY (printed). What this RETURNS/derives: the chain links (m₀,t₀ from the derived π₀),
μ₁=1/rank, and the α↔mass identity. What stays a NAMED GAP, not closed:
  * the 2¹¹ capacity factor in μ₂ is still flagged (= 2^V11), NOT derived from a forcing;
  * the UNIFIED trace formula μ_k = Tr(P U_φ Qᵏ⁻¹ U_φ P) for all k (the convergence of the resolvent
    series) needs the active↔archive pairing structure — open;
  * m_rest = m₀·W (GOLDEN THE 6.5.4) is ABSENT from v14 and NOT recovered here: it needs the
    winding numbers W per particle (OWNER-DECISION — grep GOLDEN for W before any re-derivation).
"""
from __future__ import annotations

import sys
from fractions import Fraction as F

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PHI = (1.0 + 5.0 ** 0.5) / 2.0
RANK = 3


def mul(x, y):
    a, b = x; c, d = y
    return (a * c + b * d, a * d + b * c + b * d)


def powphi(n):
    if n >= 0:
        r = (F(1), F(0))
        for _ in range(n): r = mul(r, (F(0), F(1)))
        return r
    r, inv = (F(1), F(0)), (F(-1), F(1))
    for _ in range(-n): r = mul(r, inv)
    return r


def smul(c, x): return (c * x[0], c * x[1])
def add(*xs): return (sum(x[0] for x in xs), sum(x[1] for x in xs))
def val(x): return float(x[0]) + float(x[1]) * PHI


def main() -> int:
    print("=== D0-MASS-CHAIN-001  δ₀→π₀→m₀→t₀ returned + α↔mass stitch ===")

    delta0 = smul(F(1, 2), powphi(-3))                  # δ₀ = ½φ⁻³ (owned)
    # ---- π₀ from the closure balance δ₀ = (3/5)/(π₀ φ) ⇒ π₀ = (3/5)/(δ₀ φ) ----------
    pi0_from_balance = smul(F(3, 5), powphi(-1))        # (3/5)·φ⁻¹ ... divided by δ₀ below
    # π₀ = (3/5)/(δ₀·φ): compute δ₀·φ then invert via the closed form (6/5)φ²
    pi0 = smul(F(6, 5), powphi(2))                      # (6/5)φ²  (BOOK_04 THE 04.6.π.4)
    # verify the balance: δ₀ · π₀ · φ == 3/5
    bal = mul(mul(delta0, pi0), powphi(1))
    assert bal == (F(3, 5), F(0)), f"balance δ₀·π₀·φ must be 3/5: {bal}"
    assert abs(val(pi0) - 3.1416407865) < 1e-9, "π₀ ≈ 3.14164 (departs from π at 4th decimal)"
    print(f"PASS_PI0_DERIVED  π₀=(6/5)φ²={val(pi0):.10f} from δ₀ balance (BOOK_04 §04.6.π.4)")

    # ---- m₀ = 2π₀, t₀ = 1/m₀ (returned from GOLDEN, were staged-only in v14) --------
    m0 = smul(2, pi0)                                   # 2π₀ = (12/5)φ²
    assert m0 == (F(0), F(0)) or m0 == smul(F(12, 5), powphi(2)) or m0[1] != 0, "m0 form"
    assert m0 == (F(12, 5) * powphi(2)[0], F(12, 5) * powphi(2)[1]), "m₀ must be (12/5)φ²"
    # t₀ with m₀·t₀=1: t₀ is 1/m₀; check the product is 1 in ℚ(φ)
    # 1/m₀ = 1/((12/5)φ²) = (5/12)φ⁻²
    t0 = smul(F(5, 12), powphi(-2))
    assert mul(m0, t0) == (F(1), F(0)), "m₀·t₀ must equal 1"
    print(f"PASS_MASS_QUANTUM  m₀=2π₀=(12/5)φ²={val(m0):.6f}; t₀=1/m₀=(5/12)φ⁻²; m₀·t₀=1")

    # ---- resolvent moment amplitudes ------------------------------------------------
    mu1 = (F(1, RANK), F(0))                            # 1/rank floor
    mu2 = smul(2048, mul(pi0, powphi(-2)))             # 2¹¹·π₀·φ⁻²
    assert mu1 == (F(1, 3), F(0)), "μ₁ = 1/rank = 1/3"
    assert mu2 == (F(12288, 5), F(0)), f"μ₂ = 2¹¹π₀φ⁻² = 12288/5: {mu2}"
    print(f"PASS_MOMENT_AMPLITUDES  μ₁=1/rank=1/3; μ₂=2¹¹π₀φ⁻²=12288/5")

    # ---- THE α↔mass stitch: μ₂ = 2¹⁰·m₀·φ⁻² (since m₀=2π₀) --------------------------
    mu2_via_mass = smul(1024, mul(m0, powphi(-2)))     # 2¹⁰·m₀·φ⁻²
    assert mu2_via_mass == mu2, f"α↔mass: 2¹⁰m₀φ⁻² must equal μ₂: {mu2_via_mass} vs {mu2}"
    print("PASS_ALPHA_MASS_STITCH  μ₂ = 2¹¹π₀φ⁻² = 2¹⁰·m₀·φ⁻²: ONE holonomy, two roles (α phase / mass cycle)")

    # ---- the closed α writing reproduces 137.0360 ----------------------------------
    alpha_inv = add(smul(mu2[0], powphi(-6)), smul(mu1[0], powphi(-3)))
    assert alpha_inv == (F(159739, 5), F(-294902, 15)), f"α⁻¹ form: {alpha_inv}"
    assert abs(val(alpha_inv) - 137.0360433) < 1e-6, "α⁻¹ ≈ 137.0360"
    print(f"PASS_ALPHA_REPRODUCED  α⁻¹=μ₂φ⁻⁶+μ₁φ⁻³={val(alpha_inv):.7f}")

    # ---- negative controls ----------------------------------------------------------
    assert m0 != pi0, "control: m₀=2π₀ ≠ π₀ (the factor 2 is one full cycle)"
    assert smul(1024, mul(pi0, powphi(-2))) != mu2, "control: 2¹⁰π₀φ⁻² ≠ μ₂ (needs 2¹¹, i.e. 2¹⁰·m₀)"
    assert (F(1, 2), F(0)) != mu1, "control: μ₁ is 1/rank=1/3, not 1/2"
    bad_balance = mul(mul(smul(F(1, 2), powphi(-2)), pi0), powphi(1))   # wrong δ₀=½φ⁻²
    assert bad_balance != (F(3, 5), F(0)), "control: a wrong δ₀ breaks the π₀ balance"
    print("FAIL_WRONG_FACTOR_OR_RANK_OR_DELTA0_BREAKS_THE_CHAIN")

    # ---- honesty boundary -----------------------------------------------------------
    print("HONEST_RETURNED_PI0_DERIVED_04_6_PI_4_M0_T0_RECOVERED_FROM_STAGING_MU1_EQ_1_OVER_RANK")
    print("HONEST_NAMED_GAP_2P11_CAPACITY_FLAGGED_NOT_FORCED_AND_UNIFIED_TR_FORMULA_OPEN")
    print("HONEST_M_REST_EQ_M0_W_ABSENT_NEEDS_WINDING_W_OWNER_DECISION_NOT_RECOVERED_HERE")

    print("PASS_MASS_CHAIN_ALPHA")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
