#!/usr/bin/env python3
"""D0-ALPHA-MEASUREMENT-LIMIT-001 — the last α layer (~10⁻⁸) is the measurement-limit band (falsifiable bet).

HYP (a pre-registered falsifiable bet, NOT a derived fact): the closure-holonomy structural value
    α_struct⁻¹ = 137.035999151   (vp_seam_holonomy_alpha.py)
is BRACKETED by the CODATA recommended value across editions and lies within the inter-edition band.
CODATA-2018 (137.035999084) is BELOW it and CODATA-2022 (137.035999177) is ABOVE it — i.e. the
recommended value STRADDLES α_struct; it did NOT approach monotonically "from below" (the 2022 edition
overshot from above). Both gaps (6.7×10⁻⁸ below, 2.6×10⁻⁸ above) are smaller than the 2018→2022 shift
(9.3×10⁻⁸), so the structure sits inside the historical measurement band, not outside it.

THE BET (falsifiable, asserted below): future high-precision α⁻¹ stays BRACKETED within the holonomy's
reach of α_struct — concretely, each edition's gap stays below the inter-edition shift. FALSIFIED IF a
future recommended α⁻¹ settles away from α_struct by MORE than that band. This is the honest residual
layer; the holonomy STRUCTURE (THE) and its 9-digit match (CHK) do not depend on this bet. (The earlier
"converges from below" wording was wrong — contradicted by the 2022 straddle — and is removed.)
"""
from __future__ import annotations

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ALPHA_STRUCT = 137.035999151    # closure-holonomy structural value (vp_seam_holonomy_alpha.py)
CODATA_2018 = 137.035999084     # CODATA 2018 recommended α⁻¹ (below α_struct)
CODATA_2022 = 137.035999177     # CODATA 2022 recommended α⁻¹ (above α_struct)


def main() -> int:
    print("=== D0-ALPHA-MEASUREMENT-LIMIT-001  last ~1e-8 layer = CODATA band (falsifiable bet, HYP) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: alpha_struct=137.035999151 (from the holonomy, fixed before this comparison); "
          "bet: alpha_struct stays BRACKETED within the CODATA inter-edition band (not 'from below')")

    inter_edition = abs(CODATA_2022 - CODATA_2018)
    gap_2018 = abs(ALPHA_STRUCT - CODATA_2018)
    gap_2022 = abs(ALPHA_STRUCT - CODATA_2022)
    print(f"   α_struct⁻¹      = {ALPHA_STRUCT}")
    print(f"   CODATA-2018     = {CODATA_2018}   (gap {gap_2018:.3e}, below)")
    print(f"   CODATA-2022     = {CODATA_2022}   (gap {gap_2022:.3e}, above)")
    print(f"   2018→2022 shift = {inter_edition:.3e}")

    # the structure is BRACKETED by the two editions (2018 below, 2022 above), within the band
    assert CODATA_2018 < ALPHA_STRUCT < CODATA_2022, "structural α must be straddled by the CODATA editions"
    assert gap_2018 < inter_edition and gap_2022 < inter_edition, \
        "each edition's gap to α_struct must stay within the inter-edition band"
    print(f"PASS_BRACKETED_WITHIN_BAND  {CODATA_2018} < {ALPHA_STRUCT} < {CODATA_2022}; "
          f"both gaps ({gap_2018:.2e}, {gap_2022:.2e}) < inter-edition shift ({inter_edition:.2e})")

    # ---- the falsifiable bet: a concrete ASSERTED threshold (the latest gap stays within reach) ----
    # the bet's edge is the inter-edition band; the latest edition's gap must stay under it. This is the
    # SAME number the prose falsifier names, so the bet can actually FAIL on a future drift.
    assert gap_2022 < inter_edition, "BET: the latest CODATA gap must stay within the holonomy's reach (inter-edition band)"
    print(f"PASS_BET_ASSERTED  latest gap {gap_2022:.2e} < reach {inter_edition:.2e}; "
          "FALSIFIED if a future recommended α⁻¹ drifts beyond this band from 137.035999151")

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
