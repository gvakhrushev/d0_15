#!/usr/bin/env python3
"""D0-DELTA-ALPHA-EXACT-001 — the gluing anomaly Δ_α is an EXACT element of Q(φ).

Finite-core reduction (owner Option 1) of the gluing-anomaly obligation. Δ_α was held at
the level of a numeric CHK / hypothesis ("~4.15e-4, no analytic owner"). But BOTH writings
of α⁻¹ are closed forms in Q(φ) with NO data input:

    α_top⁻¹ = 359·φ⁻² − φ⁻⁵                         (topological / edge trace)
    α_alg⁻¹ = 2¹¹·π₀·φ⁻⁸ + (2/3)·δ₀ ,  π₀=(6/5)φ², δ₀=1/(2φ³)   (algebraic)

so their difference Δ_α is itself an EXACT element of Q(φ). This certificate computes it in
exact Z[φ]/Q(φ) arithmetic (φ²=φ+1, no floats), proving:

WHAT IS PROVED (exact, able to FAIL):
    α_top⁻¹ = 726 − 364·φ
    α_alg⁻¹ = 159739/5 − (294902/15)·φ
    Δ_α = α_top⁻¹ − α_alg⁻¹ = −156109/5 + (289442/15)·φ   (|Δ_α| ≈ 4.1522e-4)
  * Δ_α ≠ 0 — the φ-coefficient 289442/15 ≠ 0, and φ is irrational, so Δ_α ∉ ℚ, in
    particular Δ_α ≠ 0 (this is M1's "no hidden identity Δ_α=0" forced, now exact).
  * |Δ_α| < φ⁻¹⁶ = 1597 − 987·φ ≈ 4.5310e-4 — an EXACT Q(φ) inequality (was a numeric CHK).

HONESTY BOUNDARY (printed, not hidden):
  * This closes the EXACT VALUE + nonzero + bound (the finite shadow). The analytic OWNER —
    deriving the algebraic writing α_alg⁻¹ = 2¹¹π₀/φ⁸ + 2δ₀/3 as a second-order/π₀-phase
    moment of the feedback resolvent (CVFT-F1) — stays frontier; §05.6-obl.4 routes Δ_α and
    the α dimension-pole residue to that one engine.
  * The neutrino link m_ν ∝ Δ_α² is a BRIDGE: Δ_α² is the CORE dimensionless factor, but
    multiplying by m_e (Λ_act = 38 m_e c²) to get ~0.088 eV is a passport, NOT promoted.
  * Distinct from the DATA residual |α_measured − α_top⁻¹| ≈ 3.7e-4 (that one is vs CODATA).
"""
from __future__ import annotations

import sys
from fractions import Fraction as F

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT5 = 5.0 ** 0.5
PHI = (1.0 + ROOT5) / 2.0


# --- exact Q(φ) arithmetic: x = a + b·φ, with φ² = φ + 1 -------------------------
def mul(x, y):
    a, b = x
    c, d = y
    return (a * c + b * d, a * d + b * c + b * d)


def powphi(n):
    if n >= 0:
        r = (F(1), F(0))
        for _ in range(n):
            r = mul(r, (F(0), F(1)))
        return r
    r, inv = (F(1), F(0)), (F(-1), F(1))     # φ⁻¹ = φ − 1
    for _ in range(-n):
        r = mul(r, inv)
    return r


def val(x):
    return float(x[0]) + float(x[1]) * PHI


def main() -> int:
    print("=== D0-DELTA-ALPHA-EXACT-001  gluing anomaly Δ_α as an exact Q(φ) element ===")

    # ---- α_top⁻¹ = 359 φ⁻² − φ⁻⁵ = 726 − 364 φ -------------------------------------
    t = powphi(-2)
    top = (359 * t[0] - powphi(-5)[0], 359 * t[1] - powphi(-5)[1])
    assert top == (F(726), F(-364)), f"α_top⁻¹ != 726 − 364φ: {top}"
    print(f"PASS_ALPHA_TOP_EXACT  α_top⁻¹ = 726 − 364φ = {val(top):.8f}")

    # ---- α_alg⁻¹ = 2¹¹ π₀ φ⁻⁸ + (2/3) δ₀,  π₀=(6/5)φ², δ₀=(1/2)φ⁻³ ------------------
    pi0 = (F(6, 5) * powphi(2)[0], F(6, 5) * powphi(2)[1])
    term1 = mul(pi0, powphi(-8))
    term1 = (2048 * term1[0], 2048 * term1[1])
    d0 = (F(1, 2) * powphi(-3)[0], F(1, 2) * powphi(-3)[1])
    term2 = (F(2, 3) * d0[0], F(2, 3) * d0[1])
    alg = (term1[0] + term2[0], term1[1] + term2[1])
    assert alg == (F(159739, 5), F(-294902, 15)), f"α_alg⁻¹ != 159739/5 − 294902/15 φ: {alg}"
    print(f"PASS_ALPHA_ALG_EXACT  α_alg⁻¹ = 159739/5 − (294902/15)φ = {val(alg):.8f}")

    # ---- Δ_α = α_top⁻¹ − α_alg⁻¹ (exact) -------------------------------------------
    da = (top[0] - alg[0], top[1] - alg[1])
    assert da == (F(-156109, 5), F(289442, 15)), f"Δ_α exact form wrong: {da}"
    assert abs(val(da) - (-4.1521686e-4)) < 1e-9, "Δ_α numeric value off"
    print(f"PASS_DELTA_ALPHA_EXACT  Δ_α = −156109/5 + (289442/15)φ = {val(da):.6e}")

    # ---- Δ_α ≠ 0: φ-coefficient nonzero ⇒ (φ irrational) Δ_α ∉ ℚ ⇒ ≠ 0 -------------
    assert da[1] != 0, "Δ_α has zero φ-coefficient (would be rational)"
    # if Δ_α = 0 then φ = -a/b ∈ ℚ, contradicting φ irrational; exact a,b shown nonzero-combo
    assert not (da[0] == 0 and da[1] == 0), "Δ_α is identically zero"
    print("PASS_DELTA_ALPHA_NONZERO  φ-coeff 289442/15 ≠ 0 ⇒ Δ_α ∉ ℚ ⇒ Δ_α ≠ 0 (M1-forced)")

    # ---- |Δ_α| < φ⁻¹⁶ = 1597 − 987 φ  (exact Q(φ) inequality) ----------------------
    bound = powphi(-16)
    assert bound == (F(1597), F(-987)), f"φ⁻¹⁶ != 1597 − 987φ: {bound}"
    # compare exactly: |Δ_α| and φ⁻¹⁶ are both a+bφ; decide the sign of (φ⁻¹⁶ − |Δ_α|)
    # via the EXACT √5: a+bφ = (a + b/2) + (b/2)√5, then exact sign of p + q√5.
    def to_surd(x):                               # returns (p, q) meaning p + q√5
        return (x[0] + x[1] * F(1, 2), x[1] * F(1, 2))

    def surd_pos(p, q) -> bool:                    # is p + q√5 > 0 ?  (exact, no floats)
        if p >= 0 and q >= 0:
            return p > 0 or q > 0
        if p <= 0 and q <= 0:
            return False
        if p < 0 < q:                              # q√5 vs −p, both ≥ 0 ⇒ square
            return 5 * q * q > p * p
        return p * p > 5 * q * q                    # p > 0 > q

    absda = (-da[0], -da[1])                       # Δ_α < 0, so |Δ_α| = −Δ_α
    diff = (bound[0] - absda[0], bound[1] - absda[1])   # φ⁻¹⁶ − |Δ_α|, want > 0
    p, q = to_surd(diff)
    assert surd_pos(p, q), "exact: φ⁻¹⁶ − |Δ_α| is not positive"
    print(f"PASS_DELTA_ALPHA_BOUND  |Δ_α| = {abs(val(da)):.6e} < φ⁻¹⁶ = {val(bound):.6e} (exact)")

    # ---- negative controls (must differ) -------------------------------------------
    assert top != alg, "control: the two α writings must NOT coincide (Δ_α ≠ 0)"
    assert da != (F(0), F(0)), "control: Δ_α is not the zero element"
    # the seam term φ⁻⁵ (= 5φ−8) is DISTINCT from Δ_α (a recurring conflation)
    assert powphi(-5) != da, "control: Δ_α must differ from the seam term φ⁻⁵"
    print("FAIL_TWO_ALPHA_WRITINGS_DO_NOT_COINCIDE")
    print("FAIL_DELTA_ALPHA_DISTINCT_FROM_PHI_MINUS_5")
    print("PASS_DELTA_ALPHA_NEGATIVE_CONTROLS")

    # ---- honesty boundary ----------------------------------------------------------
    print("HONEST_EXACT_VALUE_AND_BOUND_CLOSED_ANALYTIC_RESOLVENT_OWNER_STAYS_CVFT_F1_FRONTIER")
    print("HONEST_NEUTRINO_M_NU_PROP_DELTA_ALPHA_SQUARED_IS_BRIDGE_VIA_M_E_NOT_PROMOTED")
    print("HONEST_DISTINCT_FROM_DATA_RESIDUAL_VS_CODATA_3_7E-4")

    print("PASS_DELTA_ALPHA_EXACT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
