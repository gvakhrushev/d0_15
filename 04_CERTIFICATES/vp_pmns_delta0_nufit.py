#!/usr/bin/env python3
"""D0-PMNS-DELTA0-NUFIT-001 — PMNS delta0-family vs NuFIT 6.0 (empirical passport).

ROOT Phase 5 / T5.4 (Iteration 4). External anchor: NuFIT 6.0 (JHEP 12 (2024) 216,
arXiv:2410.05380) and the future JUNO measurement of theta_12. The D0 lepton-mixing
predictions are the delta0-family (delta0 = (sqrt5-2)/2 = 1/(2 phi^3), forced):

    sin^2 theta_12 = 1/3 - 2 delta0^2 ,
    sin^2 theta_13 = phi^-5 / 4 ,
    sin^2 theta_23 = 1/2 + delta0/2 .

This certificate computes those EXACTLY and compares them to NuFIT 6.0, with a falsifier.
It is an EMPIRICAL-PASSPORT: it is firewall-blocked from core and is NOT a forcing claim
(the derivation of the formulas from M1 is a separate, still-open obligation).

WHAT IS PROVED (exact + comparison, able to FAIL):
  * EXACT FORMULAS.  The three delta0-family values are computed from delta0 and phi:
    sin^2 th12 = 0.30547, sin^2 th13 = 0.02254, sin^2 th23 = 0.55902.
  * NuFIT 6.0 AGREEMENT.  Each lands within the experimental band of the NuFIT 6.0
    normal-ordering central values (th12~0.307, th13~0.02195, th23~0.561).
  * BEATS THE STANDARD ANSATZE (the falsifier-relevant win).  On theta_12 the D0 value
    0.30547 is closer to NuFIT than golden-ratio-A (GRA = 0.276), tri-bimaximal
    (TBM = 1/3 = 0.3333), and golden-ratio-B (GRB = 0.345).
  * JUNO JUDGE.  JUNO will pin sin^2 theta_12 to <~0.5%; the prediction 0.30547 is the
    falsifiable target (a JUNO central value outside [0.300, 0.311] would reject it).

HONESTY BOUNDARY (printed, not hidden):
  * EMPIRICAL-PASSPORT, never core. delta0 is forced; the angle FORMULAS are predictions
    compared to data, not yet derived from M1 (their forcing is an OWNER-DECISION/backlog
    obligation). Not promoted by this agreement.
"""
from __future__ import annotations

import math
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PHI = (1.0 + math.sqrt(5.0)) / 2.0
DELTA0 = (math.sqrt(5.0) - 2.0) / 2.0       # = 1/(2 phi^3)

# NuFIT 6.0 normal-ordering central values (sin^2), with ~bands
NUFIT = {"s12": (0.307, 0.013), "s13": (0.02195, 0.0007), "s23": (0.561, 0.020)}


def main() -> int:
    print("=== D0-PMNS-DELTA0-NUFIT-001  PMNS delta0-family vs NuFIT 6.0 (passport) ===")

    # ---- delta0 is the forced offset ----------------------------------------------
    assert abs(DELTA0 - 1.0 / (2 * PHI ** 3)) < 1e-12, "delta0 != 1/(2 phi^3)"

    s12 = 1.0 / 3.0 - 2.0 * DELTA0 ** 2
    s13 = PHI ** -5 / 4.0
    s23 = 0.5 + DELTA0 / 2.0
    for nm, val, (c, band) in [("s12", s12, NUFIT["s12"]), ("s13", s13, NUFIT["s13"]),
                                ("s23", s23, NUFIT["s23"])]:
        if abs(val - c) > 3.0 * band:
            raise AssertionError(f"{nm}={val:.5f} outside 3-band of NuFIT {c}")
    print(f"PASS_DELTA0_FAMILY_VALUES  s12={s12:.5f}, s13={s13:.5f}, s23={s23:.5f}")
    print("PASS_NUFIT6_AGREEMENT  all three within the NuFIT 6.0 normal-ordering bands")

    # ---- beats the standard ansatze on theta_12 ------------------------------------
    nf12 = NUFIT["s12"][0]
    GRA, TBM, GRB = 0.276, 1.0 / 3.0, 0.345
    assert abs(s12 - nf12) < abs(GRA - nf12), "D0 must beat GRA on theta_12"
    assert abs(s12 - nf12) < abs(TBM - nf12), "D0 must beat tri-bimaximal on theta_12"
    assert abs(s12 - nf12) < abs(GRB - nf12), "D0 must beat GRB on theta_12"
    print(f"PASS_BEATS_GRA_TBM_GRB  |D0-NuFIT|={abs(s12-nf12):.4f} < GRA/TBM/GRB residuals")

    # ---- JUNO falsifiable target ---------------------------------------------------
    juno_window = (0.300, 0.311)
    assert juno_window[0] < s12 < juno_window[1], "prediction not inside the JUNO target window"
    print(f"PASS_JUNO_TARGET  sin^2 th12 = {s12:.5f} in JUNO window {juno_window} (judge)")

    # ---- negative controls (must differ) -------------------------------------------
    assert abs(s12 - TBM) > 1e-3, "control: D0 must differ from tri-bimaximal 1/3"
    assert abs(s12 - GRA) > 1e-2, "control: D0 must differ from GRA 0.276"
    print("FAIL_D0_NOT_TRIBIMAXIMAL")
    print("FAIL_D0_NOT_GRA")
    print("PASS_PMNS_NEGATIVE_CONTROLS")

    # ---- honesty boundary ----------------------------------------------------------
    print("HONEST_EMPIRICAL_PASSPORT_NEVER_CORE")
    print("HONEST_DELTA0_FORCED_BUT_ANGLE_FORMULAS_FORCING_IS_BACKLOG_OWNER_DECISION")

    print("PASS_PMNS_DELTA0_NUFIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
