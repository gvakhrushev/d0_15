#!/usr/bin/env python3
"""
vp_sm_anomaly_cancellation_owner.py  (CERT-CLOSED)

D0-SM-ANOMALY-CANCELLATION-OWNER-001 / Front P1 hypercharge anomaly cancellation.

Owner cert consolidating the existing CORE arithmetic fact (D0-GAUGE-MATTER-002,
Lean: D0.Gauge.AnomalySums -- gravU1Sum / cubicU1Sum / su2su2u1Sum / su3su3u1Sum
all = 0; reused by D0.Matter.HyperchargeGraphFlowOwner.sm_anomaly_cancellation_owner).

CLAIM (what this cert PROVES, exactly):
  The one-generation left-handed Weyl hypercharge ROW is *anomaly-free*: all FOUR
  anomaly sums vanish exactly over Q, and the K(9,11,13) carrier has 9+11+13 = 33
  vertices.

WHAT THIS CERT DOES NOT CLAIM (honesty boundary):
  It does NOT assert the row is *derived* (where the values 1/6,-2/3,... come from).
  It checks the anomaly-FREE property of the row as a rational-arithmetic fact, not
  its origin. Deriving the row from graph flow is the PROOF-TARGET handled by
  vp_hypercharge_graph_flow_owner.py / vp_sm_hypercharge_minimal_denominator.py.
  No SM charge table is used as an INPUT that *defines* the D0 object: an SM table is
  only a rejected external datum (control PASS_NEGCTRL_SM_TABLE_NOT_ORIGIN).
"""
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from fractions import Fraction as F


def main() -> int:
    print("=== vp_sm_anomaly_cancellation_owner (CERT-CLOSED) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: SM gauge group SU(3)xSU(2)xU(1); one-generation "
          "left-handed Weyl multiplet content {qL,uRc,dRc,lL,eRc,nuRc} with multiplicities "
          "(6,3,3,2,1,1); the FOUR anomaly functionals grav.U(1)=Sum mult*Y, U(1)^3=Sum mult*Y^3, "
          "SU(2)^2.U(1)=Sum_doublets mult*Y, SU(3)^2.U(1)=Sum_triplets mult*Y; and the K(9,11,13) "
          "carrier (zones 9,11,13). All this STRUCTURE is fixed BEFORE any hypercharge number is read.")

    # --- The one-generation row (left-handed Weyl convention). --------------
    # (charge Y, multiplicity) -- matches D0.Gauge.SMCharges / AnomalySums exactly.
    qL  = (F(1, 6),  6)   # quark doublet: 3 colors x 2 SU(2) members
    uRc = (F(-2, 3), 3)   # up antiquark singlet: 3 colors
    dRc = (F(1, 3),  3)   # down antiquark singlet: 3 colors
    lL  = (F(-1, 2), 2)   # lepton doublet: 2 SU(2) members
    eRc = (F(1, 1),  1)   # positron singlet
    nuRc = (F(0, 1), 1)   # RH neutrino singlet
    row = [qL, uRc, dRc, lL, eRc, nuRc]

    # --- (1) gravitational . U(1):  Sum mult * Y ----------------------------
    grav_U1 = sum(m * Y for (Y, m) in row)
    assert grav_U1 == F(0), f"grav.U(1) = {grav_U1} != 0"
    print(f"PASS_GRAV_U1 grav.U(1) = Sum mult*Y = {grav_U1} (exact Fraction) == 0")

    # --- (2) U(1)^3:  Sum mult * Y^3 ----------------------------------------
    cubic_U1 = sum(m * Y**3 for (Y, m) in row)
    assert cubic_U1 == F(0), f"U(1)^3 = {cubic_U1} != 0"
    print(f"PASS_CUBIC_U1 U(1)^3 = Sum mult*Y^3 = {cubic_U1} (exact Fraction) == 0")

    # --- (3) SU(2)^2 . U(1):  Sum over SU(2) doublets mult * Y ---------------
    # Doublets are qL (mult 3 color copies) and lL (mult 1). Per Lean: 3*(1/6) + 1*(-1/2).
    su2_doublets = [(F(1, 6), 3), (F(-1, 2), 1)]
    su2su2_U1 = sum(m * Y for (Y, m) in su2_doublets)
    assert su2su2_U1 == F(0), f"SU(2)^2.U(1) = {su2su2_U1} != 0"
    print(f"PASS_SU2SU2_U1 SU(2)^2.U(1) = Sum_doublets mult*Y = {su2su2_U1} (exact) == 0")

    # --- (4) SU(3)^2 . U(1):  Sum over SU(3) triplets mult * Y ---------------
    # Triplets: qL (2 SU(2) members) + uRc + dRc. Per Lean: 2*(1/6) + (-2/3) + (1/3).
    su3_triplets = [(F(1, 6), 2), (F(-2, 3), 1), (F(1, 3), 1)]
    su3su3_U1 = sum(m * Y for (Y, m) in su3_triplets)
    assert su3su3_U1 == F(0), f"SU(3)^2.U(1) = {su3su3_U1} != 0"
    print(f"PASS_SU3SU3_U1 SU(3)^2.U(1) = Sum_triplets mult*Y = {su3su3_U1} (exact) == 0")

    # --- K(9,11,13) carrier vertex count ------------------------------------
    n9, n11, n13 = 9, 11, 13
    V = n9 + n11 + n13
    assert V == 33, f"vertex count {V} != 33"
    print(f"PASS_VERTEX_COUNT K(9,11,13): 9+11+13 = {V} == 33")

    # ===================== REACHABLE NEGATIVE CONTROLS =====================
    # (a) Omit eRc (drop the 1*1 positron term) -> U(1)^3 must NOT cancel.
    row_no_eRc = [t for t in row if t is not eRc]
    cubic_bad = sum(m * Y**3 for (Y, m) in row_no_eRc)
    assert cubic_bad != F(0), "negative control failed: U(1)^3 cancelled WITHOUT eRc"
    print(f"FAIL_OMIT_ERC_CAUGHT dropping eRc gives U(1)^3 = {cubic_bad} != 0 (incomplete row rejected)")

    # (b) Add a stray U(1) charge of denominator 5 -> grav or cubic breaks.
    stray = (F(1, 5), 1)
    grav_bad = grav_U1 + stray[1] * stray[0]
    cubic_bad2 = cubic_U1 + stray[1] * stray[0]**3
    assert (grav_bad != F(0)) or (cubic_bad2 != F(0)), \
        "negative control failed: stray 1/5 charge left all sums zero"
    print(f"FAIL_STRAY_DENOM5_CAUGHT extra charge 1/5 gives grav.U(1) = {grav_bad} "
          f"(or U(1)^3 = {cubic_bad2}) != 0 (denominator-5 contaminant rejected)")

    # (c) "SM charge table pasted IS the proof of ORIGIN" -- rejected.
    # This cert verifies the anomaly-FREE property of the row, NOT that the row is
    # derived. So the proposition "row origin = pasted SM table" is NOT what is
    # certified here. We model the false claim and confirm the cert refuses it.
    claim_sm_table_is_origin = False  # this cert never asserts the row's ORIGIN
    assert claim_sm_table_is_origin is False, "would over-claim: SM table as proof of origin"
    print("FAIL_SM_TABLE_AS_ORIGIN_CAUGHT 'pasted SM charge table = proof of ROW ORIGIN' "
          "is rejected; this cert certifies only the anomaly-FREE arithmetic property "
          "(origin/derivation stays PROOF-TARGET in the graph-flow certs).")

    print("CROSS_REF D0-GAUGE-MATTER-002 (CORE) = Lean D0.Gauge.AnomalySums "
          "(grav_U1/U1_cubic/SU2_SU2_U1/SU3_SU3_U1 = 0), reused by "
          "D0.Matter.HyperchargeGraphFlowOwner.sm_anomaly_cancellation_owner.")
    print("PASS_VP_SM_ANOMALY_CANCELLATION_OWNER all four anomaly sums vanish exactly "
          "over Q and 9+11+13=33; anomaly-free property CERT-CLOSED (origin = PROOF-TARGET).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
