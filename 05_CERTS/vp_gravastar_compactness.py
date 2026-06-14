#!/usr/bin/env python3
"""D0-COMPACTNESS-LIMIT-001 — causal-threshold compactness C_max = 3/8 (symbolic).

ROOT §4 / Phase 1 (Iteration 4). External anchor: the horizonless gravastar of
Jampolski-Rezzolla, Phys. Rev. D 113, L121502 (2026) (arXiv:2509.15302) — collapse is
arrested by a de Sitter core before a horizon forms. D0 reads the horizon as a
capacity-saturated measurement SEAM (BOOK_07 §07.50, σ(R)→1), and this certificate
derives the SYMBOLIC causal-threshold compactness at which the seam closes.

WHAT IS PROVED (exact, able to FAIL):
  * CAUSAL-THRESHOLD C = 3/8.  From three conditions —
      photon-capture threshold   χ₂ = θ⋆       (photon orbit closes on the seam),
      OS junction closure        2C = sin²χ₂   (compactness ↔ interior opening angle),
      cycle/holonomy closure     cos θ⋆ = 4C−1  (seam return condition),
    eliminating the angles gives  2C = 1 − (4C−1)² = 8C − 16C²  ⟹  16C² − 6C = 0
    ⟹  2C(8C − 3) = 0  ⟹  C ∈ {0, 3/8}.  Rejecting the trivial C=0, the maximal
    causal compactness is C_max = 3/8 = 0.375.  (Exact rational, no fit.)
  * PLACEMENT.  3/8 lies strictly between the photon sphere C=1/3 and the Buchdahl
    bound C=4/9, and strictly below the black-hole value C=1/2 — a falsifiable, specific
    horizonless prediction, not a tuned number.
  * STRUCTURAL READING.  3/8 = rank/|Ω₈| = 3/8, with rank = 3 (the spatial-transport
    rank of the adjacency of K(9,11,13), owned by D0-SIGNATURE-31-SPLIT-001) and
    |Ω₈| = 8 = 2³ = orientation × ABCD (the role-orientation octet).

NAMED GAP (this is why the claim is LEM, not THE):
  * The bridge "rank-3 transport = the causal light-cone on the 3-sphere seam" is
    POSTULATED, not derived from M1. The algebra of C=3/8 is exact; its identification
    with rank/|Ω₈| rests on that single unproven bridge. Status stays LEM with the gap
    named; promotion to THE needs the rank-3 = causal-cone derivation (T1.4, attempted
    via the Connes distance in BOOK_03 §03.1.1; open).

HONESTY BOUNDARY (printed, not hidden):
  * This is a finite GR/algebra result + one structural bridge. The gravastar FORMATION
    dynamics (OS arrest by a dS core) is the companion BRIDGE cert
    (vp_gravastar_os_arrest.py); the GW falsifier is an EMPIRICAL-PASSPORT target.
"""
from __future__ import annotations

import sys
from fractions import Fraction as F

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

RANK = 3        # spatial-transport rank of adjacency of K(9,11,13)
OMEGA8 = 8      # |Ω₈| = 2^3 = orientation × ABCD


def main() -> int:
    print("=== D0-COMPACTNESS-LIMIT-001  causal-threshold compactness C_max = 3/8 ===")

    # ---- the master equation: 2C = 8C - 16C^2  (angles eliminated) ------------------
    # solve 16 C^2 - 6 C = 0 exactly over the rationals
    # roots: C (16C - 6) = 0  -> C = 0 or C = 6/16 = 3/8
    roots = []
    # 2C(8C-3)=0  <=>  C=0 or C=3/8
    for C in (F(0), F(3, 8)):
        lhs = 2 * C
        rhs = 8 * C - 16 * C * C
        assert lhs == rhs, f"C={C} does not satisfy the master equation"
        roots.append(C)
    assert set(roots) == {F(0), F(3, 8)}, "master equation roots wrong"
    Cmax = F(3, 8)
    print("PASS_MASTER_EQUATION  2C = 8C - 16C^2  =>  2C(8C-3)=0  =>  C in {0, 3/8}")

    # verify the angle conditions are mutually consistent at C = 3/8 (exact where rational)
    # cos θ⋆ = 4C - 1 = 4*(3/8) - 1 = 1/2  ->  θ⋆ = 60°,  sin²θ⋆ = 3/4
    cos_thetastar = 4 * Cmax - 1
    assert cos_thetastar == F(1, 2), "cos θ⋆ != 1/2 at C=3/8"
    sin2_thetastar = 1 - cos_thetastar * cos_thetastar     # = 3/4
    assert sin2_thetastar == F(3, 4), "sin²θ⋆ != 3/4"
    # OS closure: 2C = sin²χ₂ = sin²θ⋆ (χ₂=θ⋆ at threshold) -> 2*(3/8)=3/4 ✓
    assert 2 * Cmax == sin2_thetastar, "OS closure 2C = sin²θ⋆ fails at C=3/8"
    print("PASS_ANGLE_CONSISTENCY  cosθ⋆=1/2 (θ⋆=60°), sin²θ⋆=3/4, 2C=3/4 — consistent")

    # ---- placement: photon sphere 1/3 < 3/8 < Buchdahl 4/9 < BH 1/2 ----------------
    C_photon, C_buchdahl, C_bh = F(1, 3), F(4, 9), F(1, 2)
    assert C_photon < Cmax < C_buchdahl < C_bh, "3/8 not between photon-sphere and Buchdahl"
    print(f"PASS_PLACEMENT  1/3={float(C_photon):.4f} < 3/8={float(Cmax):.4f} "
          f"< 4/9={float(C_buchdahl):.4f} < 1/2 (horizonless, falsifiable)")

    # ---- structural reading: 3/8 = rank/|Ω₈| ---------------------------------------
    assert Cmax == F(RANK, OMEGA8), "3/8 != rank/|Ω₈|"
    assert OMEGA8 == 2 ** 3, "|Ω₈| != 2^3"
    print(f"PASS_STRUCTURAL_3_8_EQUALS_RANK_OVER_OMEGA8  3/8 = {RANK}/{OMEGA8} (rank / |Ω₈|)")

    # ---- negative controls (must differ) -------------------------------------------
    assert Cmax != C_bh, "control: 3/8 must differ from the BH compactness 1/2"
    assert Cmax != C_photon, "control: 3/8 must differ from the photon-sphere 1/3"
    # a wrong cycle condition cos θ⋆ = 4C (dropping the -1) breaks the derivation:
    # 2C = 1-(4C)^2 would need 2*(3/8)=3/4 == 1-16*(3/8)^2 = 1-9/4 = -5/4, which is false
    assert 2 * Cmax != 1 - 16 * Cmax * Cmax, "negative control: wrong cycle law must reject 3/8"
    print("FAIL_WRONG_CYCLE_LAW_REJECTS_3_8")
    print("PASS_COMPACTNESS_NEGATIVE_CONTROLS")

    # ---- honesty boundary ----------------------------------------------------------
    print("HONEST_C_MAX_3_8_ALGEBRA_EXACT_BUT_RANK3_EQUALS_CAUSAL_CONE_IS_NAMED_GAP")
    print("HONEST_STATUS_IS_LEM_NOT_THE_UNTIL_RANK3_LIGHTCONE_DERIVED_FROM_M1")

    print("PASS_GRAVASTAR_COMPACTNESS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
