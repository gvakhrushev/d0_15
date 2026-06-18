#!/usr/bin/env python3
"""
vp_sm_hypercharge_minimal_denominator.py  (PROOF-TARGET manifest)

D0-SM-HYPERCHARGE-MINIMAL-DENOMINATOR-001 / Front P1.

WHAT IS REAL HERE (verified finite fact): the minimal common denominator of the
one-generation hypercharge row {1/6, -2/3, 1/3, -1/2, 1, 0} is
    lcm(6, 3, 3, 2, 1, 1) = 6,
computed exactly via fractions.Fraction.denominator + math.lcm.

WHAT STAYS OPEN (PROOF-TARGET -- exact missing artifact printed below):
  Deriving 6 as FORCED by the Kirchhoff graph-flow solution space on K(9,11,13)
  (i.e. that the divergence-free edge-current quantization makes 6 the unique minimal
  common denominator), rather than 6 being read off the already-given row. No SM
  charge table is used to DEFINE the D0 object; the lcm fact is a property of the row,
  the forcing is the open derivation.
"""
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from fractions import Fraction as F
import math


def common_denominator(fracs):
    """Minimal common denominator = lcm of the reduced denominators."""
    dens = [f.denominator for f in fracs]
    return math.lcm(*dens), dens


def main() -> int:
    print("=== vp_sm_hypercharge_minimal_denominator (PROOF-TARGET manifest) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the one-generation hypercharge ROW as a set of "
          "rationals {1/6,-2/3,1/3,-1/2,1,0}, the notion of minimal common denominator "
          "= lcm of reduced Fraction.denominator values, and the K(9,11,13) Kirchhoff "
          "flow solution space whose quantization is supposed to FORCE that denominator -- "
          "all structure fixed BEFORE asserting the number 6.")

    # --- The row, as exact Fractions (reduced automatically). ---------------------
    row = [F(1, 6), F(-2, 3), F(1, 3), F(-1, 2), F(1, 1), F(0, 1)]
    mcd, dens = common_denominator(row)
    print(f"PASS_ROW_DENOMINATORS reduced denominators = {dens} "
          "(for 1/6,-2/3,1/3,-1/2,1,0 respectively).")

    # --- The verified finite fact: minimal common denominator = 6. ----------------
    assert mcd == 6, f"minimal common denominator = {mcd} != 6"
    assert math.lcm(6, 3, 3, 2, 1, 1) == 6, "lcm(6,3,3,2,1,1) != 6"
    print(f"PASS_MINIMAL_DENOMINATOR lcm({', '.join(map(str, dens))}) = {mcd} == 6 (exact).")

    # Each row entry, scaled by 6, is an exact integer (the '6 is sufficient' direction).
    scaled = [r * 6 for r in row]
    assert all(s.denominator == 1 for s in scaled), f"6 does not clear all denominators: {scaled}"
    print(f"PASS_SIX_CLEARS row*6 = {[int(s) for s in scaled]} (all integers; 6 is a common denom).")

    # And 6 is MINIMAL: no proper divisor of 6 clears every denominator.
    for d in (1, 2, 3):
        cleared = all((r * d).denominator == 1 for r in row)
        assert not cleared, f"proper divisor {d} of 6 unexpectedly cleared all denominators"
    print("PASS_SIX_MINIMAL no proper divisor in {1,2,3} clears all denominators; 6 is minimal.")

    # --- The EXACT missing artifact (PROOF-TARGET) --------------------------------
    print("MISSING_ARTIFACT (D0-SM-HYPERCHARGE-MINIMAL-DENOMINATOR-001, PROOF-TARGET):")
    print("  Required: a proof that the Kirchhoff divergence-free flow solution space on "
          "K(9,11,13), under its zone-normalized U(1)-holonomy quantization, FORCES the "
          "minimal common denominator of the resulting hypercharge row to be exactly 6 "
          "(i.e. 6 emerges from the graph-flow constraints, not from the pre-given row).")
    print("  Status: ABSENT. Only the lcm fact (6 is the minimal common denominator OF the "
          "already-given row) is verified above. The forcing-from-flow derivation does not exist.")

    # ===================== REACHABLE NEGATIVE CONTROLS =====================
    # (a) 5 is NOT the minimal common denominator of the row.
    assert mcd != 5, "row minimal common denominator equals 5 (impossible)"
    cleared_by_5 = all((r * 5).denominator == 1 for r in row)
    assert not cleared_by_5, "5 unexpectedly cleared all denominators"
    print(f"FAIL_DENOM5_CAUGHT 5 is rejected: it is not the minimal common denominator "
          f"(min={mcd}) and does not clear 1/6 (1/6*5 = {F(1,6)*5}).")

    # (b) 7 is NOT the minimal common denominator of the row.
    assert mcd != 7, "row minimal common denominator equals 7 (impossible)"
    cleared_by_7 = all((r * 7).denominator == 1 for r in row)
    assert not cleared_by_7, "7 unexpectedly cleared all denominators"
    print(f"FAIL_DENOM7_CAUGHT 7 is rejected: it is not the minimal common denominator "
          f"(min={mcd}) and does not clear 1/6 (1/6*7 = {F(1,6)*7}).")

    # (c) "6 is DERIVED from graph flow" -- rejected: only the lcm fact is checked.
    claim_six_derived_from_flow = False
    assert claim_six_derived_from_flow is False, "would over-claim: 6 forced by graph flow"
    print("FAIL_SIX_DERIVED_FROM_FLOW_CAUGHT '6 is DERIVED/forced by the K(9,11,13) graph "
          "flow' is rejected -- only the lcm-of-the-given-row fact is verified; the forcing "
          "is the missing artifact above.")

    print("CROSS_REF row anomaly-freeness CERT-CLOSED in vp_sm_anomaly_cancellation_owner.py "
          "(D0-GAUGE-MATTER-002, Lean D0.Gauge.AnomalySums); flow scaffold in "
          "vp_hypercharge_graph_flow_owner.py.")
    print("PASS_VP_SM_HYPERCHARGE_MINIMAL_DENOMINATOR lcm(6,3,3,2,1,1)=6 verified exactly and "
          "minimal; flow-forcing NAMED as missing artifact; manifest PROOF-TARGET.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
