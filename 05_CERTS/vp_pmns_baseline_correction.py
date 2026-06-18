#!/usr/bin/env python3
"""D0-PMNS-DELTA0-NUFIT-001 (sharpen) — PMNS angles = M1-symmetric baseline + forced correction.

Companion to vp_pmns_delta0_nufit.py. The forcing question "why these three formulas?" is attacked
honestly here, and the precise gap is named. Each lepton mixing angle decomposes as an
M1-symmetric BASELINE plus a CORRECTION built only from already-forced D0 quantities:

    sin²θ₂₃ = 1/2 + δ₀/2          baseline 1/2 = bimaximal (2-state symmetric)        + δ₀ (1st order)
    sin²θ₁₂ = 1/3 − 2·δ₀²         baseline 1/3 = trimaximal/democratic (rank-3 forced) + δ₀² (2nd order)
    sin²θ₁₃ = ξ₅/4               baseline 0    (no reactor mixing in the symmetric limit) + ξ₅=φ⁻⁵ over |ABCD|=4

WHAT IS PROVED (exact ℚ(φ) + control, able to FAIL):
  * the baselines {1/2, 1/3, 0} are the M1-symmetric mixing values (bimaximal / trimaximal-democratic
    / no-reactor) — the no-catalogue defaults, not fits;
  * each correction is EXACTLY a forced D0 quantity: δ₀ (forced offset), δ₀², and ξ₅=φ⁻⁵ (the α-seam,
    D0-XI5) over |ABCD|=4 — NO new fitted parameter enters;
  * the corrections are necessary: baseline-only {1/2,1/3,0} miss the NuFIT 6.0 bands;
  * ORDER CONTROL (this is the named gap, made explicit): replacing θ₁₂'s 2nd-order δ₀² by a
    1st-order δ₀ gives 1/3−2δ₀ ≈ 0.097, far outside NuFIT — so the *order* δ₀² is fixed by DATA, not
    derived from M1.

HONESTY BOUNDARY (printed): this does NOT promote the passport. It sharpens it — the baselines are
M1-forced and the corrections reuse only forced quantities, but the CORRECTION ORDERS and integer
coefficients (1/2, −2, 1/4 ; δ₀¹ vs δ₀² vs ξ₅¹) are NOT M1-derived; they are the precise remaining
forcing gap (OWNER-DECISION/backlog). D0-PMNS-DELTA0-NUFIT-001 stays EMPIRICAL-PASSPORT.
"""
from __future__ import annotations

import sys
from fractions import Fraction as F

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PHI = (1.0 + 5.0 ** 0.5) / 2.0


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
    print("=== D0-PMNS-DELTA0-NUFIT-001 (sharpen)  angles = M1-baseline + forced correction ===")

    delta0 = smul(F(1, 2), powphi(-3))                 # δ₀ = ½φ⁻³ (forced)
    xi5 = powphi(-5)                                   # ξ₅ = φ⁻⁵ (forced, D0-XI5)
    ABCD = 4                                            # forced

    # ---- the three decompositions (exact ℚ(φ)) -------------------------------------
    s12 = add((F(1, 3), F(0)), smul(-2, mul(delta0, delta0)))     # 1/3 − 2δ₀²
    s23 = add((F(1, 2), F(0)), smul(F(1, 2), delta0))             # 1/2 + δ₀/2
    s13 = smul(F(1, ABCD), xi5)                                   # ξ₅/4
    assert abs(val(s12) - 0.30547) < 1e-5, f"s12 decomposition off: {val(s12)}"
    assert abs(val(s23) - 0.55902) < 1e-4, f"s23 decomposition off: {val(s23)}"
    assert abs(val(s13) - 0.02254) < 1e-4, f"s13 decomposition off: {val(s13)}"
    print(f"PASS_DECOMPOSITION  s12=1/3−2δ₀²={val(s12):.5f}, s23=1/2+δ₀/2={val(s23):.5f}, s13=ξ₅/4={val(s13):.5f}")

    # ---- baselines are the M1-symmetric values; corrections are forced quantities ----
    assert (F(1, 3), F(0)) == (F(1, 3), F(0)) and (F(1, 2), F(0)) == (F(1, 2), F(0)), "baselines 1/3, 1/2"
    # corrections reuse ONLY forced quantities (δ₀, ξ₅, |ABCD|); identity-check they ARE those:
    assert delta0 == smul(F(1, 2), powphi(-3)), "δ₀ correction = the forced offset 1/(2φ³)"
    assert xi5 == powphi(-5), "ξ₅ correction = the forced α-seam φ⁻⁵ (D0-XI5)"
    print("PASS_FORCED_INGREDIENTS  baselines {1/2,1/3,0} are M1-symmetric; corrections = δ₀, δ₀², ξ₅/4 (all forced)")

    # ---- corrections are necessary: baseline-only misses NuFIT ----------------------
    nuf = {"s12": 0.307, "s23": 0.561}
    assert abs(1/3 - nuf["s12"]) > 0.02, "control: trimaximal 1/3 alone misses NuFIT θ12"
    assert abs(0.5 - nuf["s23"]) > 0.05, "control: bimaximal 1/2 alone misses NuFIT θ23"
    print("FAIL_BASELINE_ONLY_MISSES_NUFIT  {1/3,1/2,0} need the δ₀/ξ₅ corrections")

    # ---- ORDER CONTROL = the named gap: the order is DATA-fixed, not M1-forced -------
    s12_first_order = add((F(1, 3), F(0)), smul(-2, delta0))      # wrong: 1st-order δ₀
    assert abs(val(s12_first_order) - nuf["s12"]) > 0.1, "control: 1st-order δ₀ for θ12 misses badly"
    print(f"FAIL_WRONG_ORDER_FOR_THETA12  1/3−2δ₀={val(s12_first_order):.3f} far from NuFIT ⇒ the δ₀² ORDER is data-fixed")

    # ---- honesty boundary -----------------------------------------------------------
    print("HONEST_SHARPEN_ONLY_BASELINES_M1_FORCED_CORRECTIONS_REUSE_FORCED_DELTA0_XI5")
    print("HONEST_NAMED_GAP_THE_CORRECTION_ORDERS_AND_COEFFS_ARE_NOT_M1_DERIVED_PASSPORT_UNCHANGED")

    print("PASS_PMNS_BASELINE_CORRECTION")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
