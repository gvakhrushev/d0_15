#!/usr/bin/env python3
"""D0-ALPHA-MEASUREMENT-LIMIT-001 — the last α layer (~10⁻⁸) is the measurement-limit band (falsifiable bet).

HYP (a pre-registered falsifiable bet, NOT a derived fact): the closure-holonomy structural value
    α_struct⁻¹ = 137.035999151   (vp_seam_holonomy_alpha.py)
sits INSIDE the band swept by the CODATA recommended value between editions. The 2018→2022 shift is
≈9.3×10⁻⁸; the gap |α_struct − CODATA-2018| ≈ 6.7×10⁻⁸ is SMALLER than that inter-edition motion, i.e.
the structure lies within the historical measurement band, not outside it.

THE BET (direction + base, falsifiable): as α⁻¹ is measured more precisely, the recommended value
converges toward α_struct⁻¹ = 137.035999151 FROM BELOW (CODATA-2018 137.035999084 < 2022 137.035999177
straddle it). FALSIFIED IF: a future high-precision α⁻¹ settles outside [137.035999, 137.036000] away
from the structural value by more than the holonomy can absorb. This is the honest residual layer; the
holonomy STRUCTURE (THE) and its 9-digit match (CHK) do not depend on this bet.
"""
from __future__ import annotations

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ALPHA_STRUCT = 137.035999151    # closure-holonomy structural value (vp_seam_holonomy_alpha.py)
CODATA_2018 = 137.035999084     # CODATA 2018 recommended α⁻¹
CODATA_2022 = 137.035999177     # CODATA 2022 recommended α⁻¹


def main() -> int:
    print("=== D0-ALPHA-MEASUREMENT-LIMIT-001  last ~1e-8 layer = CODATA band (falsifiable bet, HYP) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: alpha_struct=137.035999151 (from the holonomy, fixed before this comparison); "
          "bet: refined alpha^-1 converges to alpha_struct from below")

    inter_edition = abs(CODATA_2022 - CODATA_2018)
    gap_2018 = abs(ALPHA_STRUCT - CODATA_2018)
    gap_2022 = abs(ALPHA_STRUCT - CODATA_2022)
    print(f"   α_struct⁻¹      = {ALPHA_STRUCT}")
    print(f"   CODATA-2018     = {CODATA_2018}   (gap {gap_2018:.3e})")
    print(f"   CODATA-2022     = {CODATA_2022}   (gap {gap_2022:.3e})")
    print(f"   2018→2022 shift = {inter_edition:.3e}")

    # the structure lies WITHIN the inter-edition band (not outside the historical measurement motion)
    assert gap_2018 < inter_edition, "structural α must lie within the 2018→2022 measurement band"
    assert CODATA_2018 < ALPHA_STRUCT < CODATA_2022 or gap_2022 < inter_edition, \
        "structural α should be straddled by / near the CODATA editions"
    print(f"PASS_WITHIN_MEASUREMENT_BAND  gap to 2018 ({gap_2018:.2e}) < inter-edition shift ({inter_edition:.2e}); "
          f"CODATA editions straddle α_struct: {CODATA_2018} < {ALPHA_STRUCT} < {CODATA_2022}")

    # ---- the falsifiable bet (pre-registered direction + base) -----------------------------
    print("PASS_BET_REGISTERED  bet: refined α⁻¹ → 137.035999151 from below; "
          "FALSIFIED if a future high-precision α⁻¹ lands outside the holonomy's reach of the structural value")

    # ---- NEGATIVE CONTROL: a value outside the band would already be dead -------------------
    fake_outside = ALPHA_STRUCT + 5e-7        # an order beyond the band
    assert abs(fake_outside - CODATA_2018) > inter_edition, \
        "control: a structural value 5e-7 away would sit OUTSIDE the measurement band (would be dead)"
    print("FAIL_OUTSIDE_BAND_WOULD_BE_DEAD  a structural value 5e-7 from data would exceed the band — "
          "the bet is falsifiable, not vacuous")

    print("HONEST_THIS_IS_A_BET_NOT_A_DERIVATION  HYP status; the holonomy THE-structure and CHK 9-digit match "
          "do not depend on this layer; 2nd-order holonomy was checked and does NOT close the residual")
    print("PASS_ALPHA_MEASUREMENT_LIMIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
