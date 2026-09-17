#!/usr/bin/env python3
"""D0-PMNS-SEAM-TOPOLOGY-001 — the three PMNS angles as one δ₀-family (empirical passport, CHK).

STRUCTURE (δ₀-family ansatz, CHK values): the closure-holonomy that fixes α, projected onto the three
channels of the kernel 30 = 8⊕10⊕12, is used to ASSIGN a δ₀-degree per angle by seam topology:
    * bare seam (puncture)        → δ₀⁰ :  sin²θ₁₃ = φ⁻⁵/|ABCD| = φ⁻⁵/4
    * open tilt (one leg)         → δ₀¹ :  sin²θ₂₃ = 1/2 + δ₀/2
    * closed loop (two legs)      → δ₀² :  sin²θ₁₂ = 1/3 − 2δ₀²
with δ₀ = (√5−2)/2 = ½φ⁻³ (forced upstream, BOOK_01/02) and baselines {0,1/2,1/3} M1-forced.

SCOPE (honest, corrected — was over-claimed as "THE discriminating rule"): all three land <1σ vs
JUNO-2026 + NuFIT-6.0 — a genuine, non-trivial three-angle match. BUT the (degree, coefficient)
assignment is NOT uniquely forced: permuting the degree AT FIXED COEFFICIENT breaks the fits
(θ₁₂ at degree-1 with coeff 2 → ~24σ), yet REFITTING the coefficient at degree-1 recovers <1σ
(sin²θ₁₂ = 1/3 − δ₀/4 = 0.30382, 0.26σ). Under joint (degree, coefficient) freedom the family is not
discriminated, and the Lean directional theorem (D0.Matter.PMNSSeamTopology) is true by construction of
the chosen signs. So the angle VALUES are CHK (post-hoc-consistent empirical δ₀-family), NOT a forced or
discriminating prediction; only δ₀ = ½φ⁻³ itself is forced.
"""
from __future__ import annotations

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PHI = (1.0 + 5.0 ** 0.5) / 2.0
DELTA0 = (5.0 ** 0.5 - 2.0) / 2.0          # = ½φ⁻³ (forced)
ABCD = 4                                    # |ABCD| role count (forced)

# --- pinned external data (source + date) ----------------------------------------------
# JUNO 2026 (first solar-sector reactor result; Nature 2026):
JUNO_2026 = {"sin2_th12": (0.3092, 0.0087), "dm2_21": (7.50e-5, 0.0)}
# NuFIT 6.0 (JHEP 12(2024)216, arXiv:2410.05380), normal ordering:
NUFIT_60 = {"sin2_th13": (0.02195, 0.0007), "sin2_th23": (0.561, 0.020)}


def sigma(pred, datum):
    val, err = datum
    return abs(pred - val) / err


def main() -> int:
    print("=== D0-PMNS-SEAM-TOPOLOGY-001  δ₀-degree = seam topology (bare/open/closed → δ₀^{0,1,2}) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: delta0=(sqrt5-2)/2=½phi^-3 (forced); baselines {0,1/2,1/3} M1-forced; "
          "|ABCD|=4; ansatz: correction delta0-degree assigned by seam topology (bare=0/open=1/closed=2)")

    # ---- the three angles from the family (chosen degrees + coefficients) ------------------
    s13 = PHI ** -5 / ABCD                  # bare seam, δ₀⁰
    s23 = 0.5 + DELTA0 / 2.0                # open tilt, δ₀¹
    s12 = 1.0 / 3.0 - 2.0 * DELTA0 ** 2     # closed loop, δ₀²

    sg13 = sigma(s13, NUFIT_60["sin2_th13"])
    sg23 = sigma(s23, NUFIT_60["sin2_th23"])
    sg12 = sigma(s12, JUNO_2026["sin2_th12"])
    print(f"PASS_TH13_BARE_DEG0  sin²θ₁₃ = φ⁻⁵/4 = {s13:.5f}  vs NuFIT-6.0 {NUFIT_60['sin2_th13'][0]}: {sg13:.2f}σ")
    print(f"PASS_TH23_OPEN_DEG1  sin²θ₂₃ = 1/2+δ₀/2 = {s23:.5f}  vs NuFIT-6.0 {NUFIT_60['sin2_th23'][0]}: {sg23:.2f}σ")
    print(f"PASS_TH12_CLOSED_DEG2  sin²θ₁₂ = 1/3−2δ₀² = {s12:.5f}  vs JUNO-2026 {JUNO_2026['sin2_th12'][0]}: {sg12:.2f}σ")
    assert sg13 < 1.0 and sg23 < 1.0 and sg12 < 1.0, "all three chosen-family angles must land <1σ"
    print(f"PASS_ALL_THREE_UNDER_1SIGMA  ({sg13:.2f}, {sg23:.2f}, {sg12:.2f})σ — genuine non-trivial match")

    # ---- degree permutation AT FIXED COEFFICIENT breaks (necessary, NOT sufficient) --------
    s12_deg1 = 1.0 / 3.0 - 2.0 * DELTA0          # θ₁₂ at degree-1, SAME coefficient 2
    s23_deg2 = 0.5 + DELTA0 ** 2 / 2.0           # θ₂₃ at degree-2, same coefficient
    sg12_bad = sigma(s12_deg1, JUNO_2026["sin2_th12"])
    sg23_bad = sigma(s23_deg2, NUFIT_60["sin2_th23"])
    assert sg12_bad > 2.5 and sg23_bad > 2.5, "fixed-coefficient degree swaps must break (else even this is vacuous)"
    print(f"PASS_FIXED_COEFF_DEGREE_SWAP_BREAKS  θ₁₂@deg1={s12_deg1:.4f}→{sg12_bad:.1f}σ, "
          f"θ₂₃@deg2={s23_deg2:.5f}→{sg23_bad:.1f}σ (necessary, not sufficient)")

    # ---- but REFITTING the coefficient at degree-1 recovers <1σ → NOT discriminating -------
    s12_deg1_refit = 1.0 / 3.0 - DELTA0 / 4.0    # θ₁₂ at degree-1 with a refit coefficient
    sg12_refit = sigma(s12_deg1_refit, JUNO_2026["sin2_th12"])
    assert sg12_refit < 1.0, "coefficient-freedom rescue: degree-1 with a refit coefficient also lands <1σ"
    print(f"HONEST_COEFFICIENT_FREEDOM  θ₁₂ = 1/3 − δ₀/4 = {s12_deg1_refit:.5f} → {sg12_refit:.2f}σ "
          "(degree-1 refit ALSO <1σ ⇒ joint (degree,coefficient) freedom is NOT discriminated)")

    # ---- honest verdict + δ_CP note --------------------------------------------------------
    print("HONEST_LEAN_DIRECTIONS_TRUE_BY_CONSTRUCTION  D0.Matter.PMNSSeamTopology proves θ₁₃>0, θ₂₃>1/2, "
          "θ₁₂<1/3 — true by construction of the chosen signs (+δ₀/2, −2δ₀², φ⁻⁵/4>0), not a forcing")
    print("HONEST_JUNO_EXCLUDED_RIVALS  JUNO-2026 excluded tri-bimaximal / golden-A / golden-B at 2.8–4.2σ")
    print("HONEST_DELTACP_IS_HYP  δ_CP ≈ π₀ ≈ π is a separate HYP row D0-PMNS-DELTACP-PI0-001, not asserted here")
    print("HONEST_VALUES_ARE_POSTHOC_CHK_NOT_FORCED  the δ₀-family reproduces all three angles <1σ (real), but the "
          "(degree,coefficient) assignment is post-hoc-consistent, not forced/discriminating; only δ₀=½φ⁻³ is forced")

    # ---- FAIL control: the retracted 'values are forced/discriminating' claim must be refuted
    forced_or_discriminating_holds = sg12_refit >= 1.0   # would hold only if the degree-1 refit ALSO failed
    assert not forced_or_discriminating_holds, \
        "FAIL control: 'values are forced/discriminating' is refuted by the coefficient-refit rescue"
    print("FAIL_VALUES_ARE_FORCED_OR_DISCRIMINATING  refuted (degree-1 refit lands <1σ)")

    print("PASS_PMNS_SEAM_TOPOLOGY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
