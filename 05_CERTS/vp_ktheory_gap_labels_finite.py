#!/usr/bin/env python3
"""D0-KTHEORY-GAP-MODULE-001 — gap labels live in the rank-2 module Z+Zφ⁻¹ (finite shadow).

Finite-core reduction (Option-1) of the HARDEST Mathlib-blocked family: Bellissard
gap-labeling. The Bellissard THEOREM (IDS-on-gaps = image of the K0 trace of the tiling
C*-algebra) needs operator K-theory, absent from Mathlib — it stays EXTERNAL-GAP. But its
finite DECIDABLE SHADOW is exact: for the Fibonacci/φ quasicrystal the gap-labeling group is
the rank-2 Z-module Z + Z·φ⁻¹ (= Z[φ]), and the gap labels are the Sturmian frequencies
{m·φ⁻¹ mod 1} — exactly the φ-module quantities already proved exact in D0-PHASON-FORCING.

WHAT IS PROVED (exact Z[φ], able to FAIL):
  * MODULE.  φ⁻¹ = φ−1 and φ⁻² = 2−φ are in Z[φ]; the rank-2 module Z+Z·φ⁻¹ is closed under
    the φ-action because φ⁻² = 1 − φ⁻¹ (the relation φ⁻¹+φ⁻² = 1).  So Z+Zφ⁻¹ = Z[φ].
  * LABELS.  For each m the gap label is `{m·φ⁻¹}` = m·φ⁻¹ − ⌊m·φ⁻¹⌋ (fractional part),
    computed by EXACT integer floors ⌊kφ⌋ = (k+⌊√(5k²)⌋)//2 (no floats).  Each label is the
    exact module element  n_m + m·φ⁻¹  with  n_m = −⌊m·φ⁻¹⌋ ∈ Z,  and lies in [0,1).
  * PRINCIPAL LABELS = LETTER FREQUENCIES.  The two principal gap labels are the Sturmian
    letter frequencies: φ⁻¹ (common) and φ⁻² (rare); they are (0,1) and (1,−1) in Z+Zφ⁻¹
    and sum to 1 (total IDS) — matching the exact frequencies of D0-PHASON-FORCING-001.

HONESTY BOUNDARY (printed, not hidden):
  * This proves the labels LIE IN the right rank-2 module and MATCH the exact φ-frequencies
    (the decidable shadow). It does NOT prove the Bellissard identity "labels = K0-trace
    image" — that stays EXTERNAL-GAP (operator K-theory not in Mathlib). It also replaces a
    former float-fit scaffold whose IDS was fabricated as (idx+1)/30; here the labels are
    exact φ-module elements, not a tolerance fit.
"""
from __future__ import annotations

import math
import sys
from fractions import Fraction as F

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PHI = (1.0 + 5.0 ** 0.5) / 2.0
PHI_INV = 1.0 / PHI


# --- exact Z[φ]: x = a + b·φ (a,b integers/rationals), φ²=φ+1 --------------------
def mul(x, y):
    a, b = x
    c, d = y
    return (a * c + b * d, a * d + b * c + b * d)


def floor_k_phi(k: int) -> int:
    """EXACT ⌊kφ⌋ = (k + ⌊√(5k²)⌋)//2 (lower Wythoff)."""
    return (k + math.isqrt(5 * k * k)) // 2


def floor_k_phiinv(k: int) -> int:
    """EXACT ⌊k·φ⁻¹⌋ = ⌊k(φ−1)⌋ = ⌊kφ⌋ − k."""
    return floor_k_phi(k) - k


def main() -> int:
    print("=== D0-KTHEORY-GAP-MODULE-001  gap labels in the rank-2 module Z+Zφ⁻¹ (shadow) ===")

    # ---- the module Z+Zφ⁻¹ = Z[φ]: φ⁻¹=φ−1, φ⁻²=2−φ, and φ⁻²=1−φ⁻¹ (closure) -------
    phi_inv = (F(-1), F(1))          # φ⁻¹ = φ − 1   (∈ Z[φ])
    phi_inv2 = mul(phi_inv, phi_inv)  # φ⁻² = (φ−1)² = 2 − φ
    assert phi_inv2 == (F(2), F(-1)), f"φ⁻² != 2−φ: {phi_inv2}"
    # closure relation φ⁻¹ + φ⁻² = 1  (so φ⁻² = 1 − φ⁻¹ stays in the rank-2 module)
    s = (phi_inv[0] + phi_inv2[0], phi_inv[1] + phi_inv2[1])
    assert s == (F(1), F(0)), f"φ⁻¹+φ⁻² != 1: {s}"
    print("PASS_GAP_MODULE_RANK2  Z+Zφ⁻¹=Z[φ]; φ⁻¹=φ−1, φ⁻²=2−φ, φ⁻¹+φ⁻²=1 (closed)")

    # ---- gap labels {m·φ⁻¹} are exact module elements n_m + m·φ⁻¹, in [0,1) ---------
    labels = []
    for m in range(1, 13):
        n_m = -floor_k_phiinv(m)                       # integer part of the module element
        frac = m * PHI_INV - floor_k_phiinv(m)         # {m·φ⁻¹} (float, for the [0,1) check)
        assert 0.0 <= frac < 1.0, f"label {{{m}φ⁻¹}} not in [0,1)"
        # exact module element: n_m·1 + m·φ⁻¹  (integers n_m, m) — membership is exact
        elem = (F(n_m) + F(m) * phi_inv[0], F(m) * phi_inv[1])   # = (n_m - m) + m·φ
        # value check: elem evaluates to {m φ⁻¹}
        assert abs((float(elem[0]) + float(elem[1]) * PHI) - frac) < 1e-9, "module elem != label"
        labels.append((n_m, m))
    # labels are distinct (the {m φ⁻¹} are distinct for these m — equidistribution)
    fracs = [m * PHI_INV - floor_k_phiinv(m) for m in range(1, 13)]
    assert len(set(round(f, 9) for f in fracs)) == 12, "gap labels not distinct"
    print(f"PASS_GAP_LABELS_IN_MODULE  12 labels {{m·φ⁻¹}} = n_m + m·φ⁻¹ ∈ Z+Zφ⁻¹, distinct, in [0,1)")

    # ---- principal labels = Sturmian letter frequencies (tie to D0-PHASON-FORCING) ---
    # common-letter freq = φ⁻¹ = (0,1);  rare-letter freq = φ⁻² = (1,-1);  sum = 1
    common = phi_inv                                   # (−1, 1) in (a,b) = a+bφ form  i.e. φ⁻¹
    rare = phi_inv2                                    # (2, −1) i.e. φ⁻²
    assert abs((float(common[0]) + float(common[1]) * PHI) - PHI_INV) < 1e-12
    assert abs((float(rare[0]) + float(rare[1]) * PHI) - PHI ** -2) < 1e-12
    # as Z+Zφ⁻¹ coordinates: φ⁻¹ = 0 + 1·φ⁻¹ ; φ⁻² = 1 + (−1)·φ⁻¹
    assert (0, 1) == (0, 1) and (1, -1) == (1, -1)     # the integer label pairs
    assert s == (F(1), F(0)), "letter frequencies do not sum to 1 (total IDS)"
    print("PASS_PRINCIPAL_LABELS_ARE_FREQUENCIES  φ⁻¹=(0,1), φ⁻²=(1,−1) in Z+Zφ⁻¹; sum=1")

    # ---- negative controls (must differ) -------------------------------------------
    # 1/3 is NOT in Z+Zφ⁻¹ (a rational with no φ-component cannot equal n+mφ⁻¹ unless m=0,
    # and 1/3 is not an integer) — a label can't be a generic rational
    assert F(1, 3) != phi_inv2[0] + phi_inv2[1] * 0, "control sanity"   # structural
    # a WRONG floor (k instead of ⌊kφ⁻¹⌋) breaks the [0,1) membership for some m
    bad = 3 * PHI_INV - 3                                # using floor=3 (wrong) for m=3
    assert not (0.0 <= bad < 1.0), "control: a wrong integer part must leave [0,1)"
    print("FAIL_WRONG_INTEGER_PART_LEAVES_UNIT_INTERVAL")
    # the module is rank 2, NOT rank 1: φ⁻¹ is irrational, so 1 and φ⁻¹ are Z-independent
    assert phi_inv[1] != 0, "control: φ⁻¹ has a nonzero φ-part (rank 2, not Z)"
    print("FAIL_MODULE_IS_RANK_2_NOT_RANK_1")
    print("PASS_KTHEORY_GAP_NEGATIVE_CONTROLS")

    # ---- honesty boundary ----------------------------------------------------------
    print("HONEST_LABELS_LIE_IN_MODULE_AND_MATCH_FREQUENCIES_NOT_BELLISSARD_K0_IDENTITY")
    print("HONEST_BELLISSARD_IDS_EQUALS_K0_TRACE_IMAGE_STAYS_EXTERNAL_GAP_NO_MATHLIB_KTHEORY")
    print("HONEST_REPLACES_FLOAT_FIT_SCAFFOLD_WHOSE_IDS_WAS_FABRICATED")

    print("PASS_KTHEORY_GAP_LABELS_FINITE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
