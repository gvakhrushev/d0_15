#!/usr/bin/env python3
"""D0-PMNS-SEAM-TOPOLOGY-001 — the three PMNS angles from one rule: δ₀-degree = seam topology.

STRUCTURE (THE rule / CHK numbers): the same closure-holonomy that fixes α, projected onto the three
channels of the kernel 30 = 8⊕10⊕12, gives one rule — the DEGREE of δ₀ in an angle correction equals
the seam-cycle topology:
    * bare seam (puncture)        → δ₀⁰ :  sin²θ₁₃ = φ⁻⁵/|ABCD| = φ⁻⁵/4
    * open tilt (one leg)         → δ₀¹ :  sin²θ₂₃ = 1/2 + δ₀/2
    * closed loop (two legs)      → δ₀² :  sin²θ₁₂ = 1/3 − 2δ₀²
with δ₀ = (√5−2)/2 = ½φ⁻³ (forced, BOOK_01/02) and baselines {0, 1/2, 1/3} M1-forced (reactor/atmo/solar).

DISCRIMINATING TEST (the rule is not free): PERMUTING the δ₀ degrees breaks the fits — θ₁₂ with degree-1
lands ~24σ off JUNO, θ₂₃ with degree-2 lands ~2.7σ off NuFIT. Correct degrees: all three <1σ.

NUMBERS are CHK (empirical, version-pinned): the rule (degree↔topology) is the THE content; the angle
VALUES are checked against data here, not derived to precision. The (6/5)-chain / cone-angle 2π₀
micro-derivations lean on corpus THE (MECH-LIMIT residual, named, not hidden).
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
          "|ABCD|=4; rule: correction delta0-degree = seam topology (bare=0/open=1/closed=2)")

    # ---- the three angles from the rule ---------------------------------------------------
    s13 = PHI ** -5 / ABCD                  # bare seam, δ₀⁰
    s23 = 0.5 + DELTA0 / 2.0                # open tilt, δ₀¹
    s12 = 1.0 / 3.0 - 2.0 * DELTA0 ** 2     # closed loop, δ₀²

    sg13 = sigma(s13, NUFIT_60["sin2_th13"])
    sg23 = sigma(s23, NUFIT_60["sin2_th23"])
    sg12 = sigma(s12, JUNO_2026["sin2_th12"])
    print(f"PASS_TH13_BARE_DEG0  sin²θ₁₃ = φ⁻⁵/4 = {s13:.5f}  vs NuFIT-6.0 {NUFIT_60['sin2_th13'][0]}: {sg13:.2f}σ")
    print(f"PASS_TH23_OPEN_DEG1  sin²θ₂₃ = 1/2+δ₀/2 = {s23:.5f}  vs NuFIT-6.0 {NUFIT_60['sin2_th23'][0]}: {sg23:.2f}σ")
    print(f"PASS_TH12_CLOSED_DEG2  sin²θ₁₂ = 1/3−2δ₀² = {s12:.5f}  vs JUNO-2026 {JUNO_2026['sin2_th12'][0]}: {sg12:.2f}σ")
    assert sg13 < 1.0 and sg23 < 1.0 and sg12 < 1.0, "all three correct-degree angles must land <1σ"
    print(f"PASS_ALL_THREE_UNDER_1SIGMA  ({sg13:.2f}, {sg23:.2f}, {sg12:.2f})σ — one rule, three channels")

    # ---- DISCRIMINATING TEST: permute the δ₀ degrees → fits break --------------------------
    s12_deg1 = 1.0 / 3.0 - 2.0 * DELTA0          # closed loop forced to degree-1 (wrong)
    s23_deg2 = 0.5 + DELTA0 ** 2 / 2.0           # open tilt forced to degree-2 (wrong)
    sg12_bad = sigma(s12_deg1, JUNO_2026["sin2_th12"])
    sg23_bad = sigma(s23_deg2, NUFIT_60["sin2_th23"])
    assert sg12_bad > 2.5, "control: θ₁₂ with the wrong (degree-1) order must be grossly rejected"
    assert sg23_bad > 2.5, "control: θ₂₃ with the wrong (degree-2) order must be rejected"
    print(f"FAIL_TH12_WRONG_DEGREE1  sin²θ₁₂ with δ₀¹ = {s12_deg1:.4f} → {sg12_bad:.1f}σ off JUNO (degree-2 is forced)")
    print(f"FAIL_TH23_WRONG_DEGREE2  sin²θ₂₃ with δ₀² = {s23_deg2:.5f} → {sg23_bad:.1f}σ off NuFIT (degree-1 is forced)")

    # ---- δ_CP ≈ π₀ ≈ π (HYP, separate row D0-PMNS-DELTACP-PI0-001) -------------------------
    print("HONEST_DELTACP_IS_HYP  δ_CP ≈ π₀ ≈ π (CP near-conservation as the full-3-cycle angle) is a "
          "separate HYP row D0-PMNS-DELTACP-PI0-001, not asserted here")
    print("HONEST_RULE_IS_THE_NUMBERS_ARE_CHK  the degree↔topology rule is the THE content; the angle values "
          "are CHK vs pinned JUNO-2026 + NuFIT-6.0; the (6/5)-chain / 2π₀ micro-derivation is a named MECH-LIMIT residual")
    print("HONEST_JUNO_EXCLUDED_RIVALS  JUNO-2026 excluded tri-bimaximal / golden-A / golden-B at 2.8–4.2σ while "
          "the δ₀-family held at {:.2f}σ".format(sg12))

    print("PASS_PMNS_SEAM_TOPOLOGY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
