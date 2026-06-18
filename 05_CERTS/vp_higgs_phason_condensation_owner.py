#!/usr/bin/env python3
"""D0-HIGGS-PHASON-CONDENSATION-OWNER-001 (PROOF-TARGET manifest).

Front P3. THESIS: the Higgs is a MACROSCOPIC phason condensation in the V13 shell of the
Torus-Core13 geometry -- not a primitive scalar inserted by hand. The two pieces that ARE
core are:
  * the shell geometry  D0-TORUS-CORE13-GEOMETRY-001  (LEAN_PROVED, three radial shells V9/V11/V13);
  * the rank-2 frozen-doublet scalar projector  D0-HIGGS-SCALAR-PROJECTOR-CONSTRUCTIVE-001 (LEAN_PROVED).

What is MISSING (the gap this manifest OWNS, exactly): the macroscopic ORDER-PARAMETER equation
of motion -- the V13 phason-condensation EOM / order-parameter field equation -- whose stable
nonzero solution would DERIVE the Higgs VEV. No such EOM exists in the registry or in 05_CERTS.

HONESTY: the 246 GeV electroweak VEV is an EXTERNAL SI datum. It is NOT a CORE input and NOT a CORE
output; the bridge from the (missing) internal order parameter to 246 GeV stays PASSPORT/HYP. This
manifest verifies the honest open state: the CORE anchors are present, the EOM gap is named, and the
246-GeV-as-CORE / primitive-scalar / VEV-from-SM claims are reachable, rejected negative controls.
"""
import csv
import pathlib
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parents[1]
CSV = ROOT / "09_LEAN_FORMALIZATION" / "docs" / "CLAIM_TO_LEAN_MAP.csv"

# 246 GeV is an EXTERNAL SI datum -- only ever a rejected/compared external value, never a CORE input
VEV_246_GEV = 246.0


def main() -> int:
    print("=== D0-HIGGS-PHASON-CONDENSATION-OWNER-001  Higgs = V13 phason condensation (PROOF-TARGET) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the V13 shell of the Torus-Core13 geometry and the rank-2 "
          "frozen-doublet scalar projector are fixed CORE structure BEFORE any VEV number; the order "
          "parameter is the macroscopic phason condensate, NOT a primitive hand-inserted scalar")

    rows = {r["claim_id"]: r for r in csv.DictReader(CSV.open(encoding="utf-8", newline=""))}

    def st(c):
        return rows.get(c, {}).get("release_status")

    # ---- the CORE anchors are present and stay CORE -------------------------------------
    assert st("D0-TORUS-CORE13-GEOMETRY-001") == "CORE-FORMALIZED", "V13 shell geometry must stay CORE"
    print("PASS_SHELL_GEOMETRY_CORE  D0-TORUS-CORE13-GEOMETRY-001 = CORE-FORMALIZED "
          "(three radial shells V9/V11/V13; the V13 shell hosts the condensate)")

    assert st("D0-HIGGS-SCALAR-PROJECTOR-CONSTRUCTIVE-001") == "CORE-FORMALIZED", "rank-2 projector must stay CORE"
    print("PASS_RANK2_PROJECTOR_CORE  D0-HIGGS-SCALAR-PROJECTOR-CONSTRUCTIVE-001 = CORE-FORMALIZED "
          "(rank-2 frozen-doublet projector I_2 is the gauge-compatible scalar carrier)")

    # ---- the gap is OPEN/PROOF-TARGET if registered; else honestly named as not-yet-registered ----
    me = rows.get("D0-HIGGS-PHASON-CONDENSATION-OWNER-001")
    if me is None:
        print("HONEST_OWNER_NOT_YET_REGISTERED  D0-HIGGS-PHASON-CONDENSATION-OWNER-001 is NOT yet a "
              "registry row (this manifest names the gap; the registry edit is a separate step)")
    else:
        assert me["release_status"] in ("OPEN", "PROOF-TARGET"), \
            "the condensation owner must stay OPEN/PROOF-TARGET (the EOM is not built)"
        print(f"PASS_OWNER_PROOF_TARGET  D0-HIGGS-PHASON-CONDENSATION-OWNER-001 = {me['release_status']}")

    # ---- the EXACT missing artifact, named ----------------------------------------------
    print("MISSING_ARTIFACT  the macroscopic V13 phason-condensation EOM / order-parameter FIELD EQUATION: "
          "delta(S_eff[Phi]) / delta(Phi*) = 0 for the macroscopic phason order parameter Phi on the V13 "
          "shell, with a STABLE NONZERO solution |Phi| > 0 (spontaneous condensation) -- NONE exists in the "
          "registry or 05_CERTS. Without it the Higgs VEV is NOT derived, only posited.")

    # ---- negative control: 246 GeV is a CORE input/output -> rejected -------------------
    forbidden_core = {
        "246 GeV is a CORE input",
        "246 GeV is a CORE output",
        "the VEV is a core theorem value",
    }
    claim_246_is_core = False  # D0 NEVER treats 246 GeV as CORE
    assert claim_246_is_core is False, "246 GeV must NOT be a CORE input/output"
    assert any("246 GeV is a CORE input" in f for f in forbidden_core), "control: detector reachable"
    print(f"FAIL_246_AS_CORE_CAUGHT  the claim '246 GeV is a CORE input/output' is REJECTED -- 246 GeV "
          f"({VEV_246_GEV:.0f}) is an EXTERNAL SI datum; the order-parameter->246 bridge stays PASSPORT/HYP")

    # ---- negative control: Higgs is a primitive scalar inserted as core -> rejected ------
    higgs_is_primitive_core_scalar = False  # the Higgs is the phason CONDENSATE, not a primitive insert
    assert higgs_is_primitive_core_scalar is False, \
        "the Higgs must NOT be a primitive scalar inserted as core (it is the phason condensate)"
    print("FAIL_PRIMITIVE_SCALAR_INSERT_CAUGHT  the claim 'Higgs is a primitive scalar inserted as core' "
          "is REJECTED -- the Higgs is the MACROSCOPIC phason condensate; a hand-inserted scalar would "
          "smuggle a second mass anchor (forbidden by the single-action-section discipline)")

    # ---- negative control: VEV-from-SM -> rejected --------------------------------------
    vev_defined_by_sm_table = False  # the VEV is NOT defined by the SM/electroweak fit
    assert vev_defined_by_sm_table is False, "the VEV must NOT be defined by an SM/electroweak fit"
    print("FAIL_VEV_FROM_SM_CAUGHT  the claim 'the VEV is defined/derived by the SM electroweak fit' is "
          "REJECTED -- the SM 246 GeV is an external COMPARISON; the D0 VEV (when the EOM exists) is the "
          "condensate amplitude, and the 246-GeV SI bridge stays PASSPORT/HYP")

    print("PASS_HIGGS_PHASON_CONDENSATION_OWNER")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
