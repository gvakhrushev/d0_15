#!/usr/bin/env python3
"""vp_cosmology_closure_dependency_graph - integrity of the cosmology closure chain.

Checks 04_VERIFICATION/COSMOLOGY_CLOSURE_BLOCKERS.csv against the registry: every CERT-CLOSED row names
a cert + lean_module and is not a global blocker; every PROOF-TARGET row names an exact missing artifact
and IS flagged a global blocker; the 6 campaign owners are registered CERT-CLOSED; the frontier is
non-empty (global closure NOT asserted). Reachable controls reject a closed-without-owner row and a
PROOF-TARGET with no named artifact.
"""
import csv
import pathlib
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parents[1]
BLOCKERS = ROOT / "04_VERIFICATION" / "COSMOLOGY_CLOSURE_BLOCKERS.csv"
REGISTRY = ROOT / "09_LEAN_FORMALIZATION" / "docs" / "CLAIM_TO_LEAN_MAP.csv"
CAMPAIGN = [
    "D0-REHEATING-PHASON-INITIAL-DATA-OWNER-001", "D0-PHASON-INITIAL-COVARIANCE-OWNER-001",
    "D0-CMB-FIEDLER-FREEZEOUT-OWNER-001", "D0-DARK-RATIO-TRANSFER-OWNER-001",
    "D0-ARCHIVE-PHASON-METRIC-TRANSFER-OWNER-001", "D0-COSMOLOGY-INTERNAL-TRANSFER-COMPOSITION-001",
]
CLOSED = {"CERT-CLOSED", "NO-GO", "PASSPORT-CLOSED", "CORE-FORMALIZED", "BRIDGE-ASSUMPTIONS-EXPLICIT"}


def row_violation(r):
    st = r["status"].strip()
    if st in CLOSED:
        if not r["certificate"].strip() and not r["lean_module"].strip():
            return f"{r['claim_id']}: closed ({st}) but names neither cert nor lean_module"
        if r["is_global_blocker"].strip() != "False":
            return f"{r['claim_id']}: closed but flagged a global blocker"
    elif st == "PROOF-TARGET":
        if not r["exact_missing_artifact"].strip():
            return f"{r['claim_id']}: PROOF-TARGET with empty exact_missing_artifact"
        if r["is_global_blocker"].strip() != "True":
            return f"{r['claim_id']}: PROOF-TARGET not flagged is_global_blocker"
    else:
        return f"{r['claim_id']}: unrecognized status {st!r}"
    return ""


def main() -> int:
    print("=== vp_cosmology_closure_dependency_graph  integrity of the cosmology closure chain ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: every closed link names a cert/lean owner; every PROOF-TARGET names "
          "an exact missing artifact and is a flagged global blocker; the frontier stays non-empty -- before "
          "any count.")

    rows = list(csv.DictReader(BLOCKERS.open(encoding="utf-8", newline="")))
    assert rows, "cosmology blockers CSV is empty"
    viol = [v for r in rows for v in [row_violation(r)] if v]
    assert not viol, f"dependency-graph violations: {viol}"
    closed = [r for r in rows if r["status"] in CLOSED]
    pts = [r for r in rows if r["status"] == "PROOF-TARGET"]
    print(f"PASS_ROWS_CONFORMANT  {len(rows)} rows: {len(closed)} closed (cert/lean each), {len(pts)} "
          "PROOF-TARGET (each names an exact missing artifact).")

    reg = {r["claim_id"]: r for r in csv.DictReader(REGISTRY.open(encoding="utf-8", newline=""))}
    for cid in CAMPAIGN:
        assert cid in reg, f"campaign owner {cid} missing from registry"
        assert reg[cid]["release_status"] == "CERT-CLOSED", f"{cid} not CERT-CLOSED ({reg[cid]['release_status']})"
    print(f"PASS_CAMPAIGN_OWNERS_REGISTERED  all {len(CAMPAIGN)} new cosmology owners registered CERT-CLOSED.")

    blockers = [r for r in rows if r["is_global_blocker"].strip() == "True"]
    assert blockers, "graph claims zero global blockers -- verify before any global-closure claim"
    print(f"PASS_FRONTIER_NONEMPTY  {len(blockers)} named global blockers remain (global closure NOT asserted).")

    # ===================== REACHABLE NEGATIVE CONTROLS =====================
    bad_closed = {"claim_id": "PLANT", "status": "CERT-CLOSED", "certificate": "", "lean_module": "",
                  "is_global_blocker": "False", "exact_missing_artifact": ""}
    assert row_violation(bad_closed), "control: a closed row with no owner must be rejected"
    print("FAIL_CLOSED_WITHOUT_OWNER_REJECTED  a planted closed row with no cert/lean owner is caught.")
    bad_pt = {"claim_id": "PLANT", "status": "PROOF-TARGET", "certificate": "", "lean_module": "",
              "is_global_blocker": "True", "exact_missing_artifact": ""}
    assert row_violation(bad_pt), "control: a PROOF-TARGET with no artifact must be rejected"
    print("FAIL_PROOFTARGET_WITHOUT_ARTIFACT_REJECTED  a planted PROOF-TARGET with no named artifact is caught.")

    print("PASS_COSMOLOGY_CLOSURE_DEPENDENCY_GRAPH")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
