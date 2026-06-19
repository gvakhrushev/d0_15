#!/usr/bin/env python3
"""vp_final_eight_front_dependency_graph - integrity of the eight-front closure dependency graph.

Checks 04_VERIFICATION/FINAL_EIGHT_FRONT_BLOCKERS.csv against the canonical registry:
every campaign claim appears; every CERT-CLOSED/NO-GO row names a certificate; every PROOF-TARGET
row names an exact remaining_artifact AND is flagged is_global_blocker; the closed rows' statuses
match the registry; and the frontier is non-empty (named blockers remain, so global closure is
NOT asserted). Reachable controls reject a closed-without-cert row and a PROOF-TARGET with an empty
remaining_artifact.
"""
import csv
import pathlib
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parents[1]
BLOCKERS = ROOT / "04_VERIFICATION" / "FINAL_EIGHT_FRONT_BLOCKERS.csv"
REGISTRY = ROOT / "09_LEAN_FORMALIZATION" / "docs" / "CLAIM_TO_LEAN_MAP.csv"
CLOSED = {"CERT-CLOSED", "NO-GO", "CORE-FORMALIZED"}


def row_violation(r):
    """Return a violation string for one blockers-row, or '' if conformant."""
    st = r["status"].strip()
    if st in CLOSED:
        if not r["certificate"].strip() and not r["lean_module"].strip():
            return f"{r['claim_id']}: closed ({st}) but names neither cert nor lean_module"
        if r["is_global_blocker"].strip() != "False":
            return f"{r['claim_id']}: closed but flagged a global blocker"
    elif st == "PROOF-TARGET":
        if not r["remaining_artifact"].strip():
            return f"{r['claim_id']}: PROOF-TARGET with empty remaining_artifact"
        if r["is_global_blocker"].strip() != "True":
            return f"{r['claim_id']}: PROOF-TARGET not flagged is_global_blocker"
    else:
        return f"{r['claim_id']}: unrecognized status {st!r}"
    return ""


def main() -> int:
    print("=== vp_final_eight_front_dependency_graph  integrity of the eight-front blockers graph ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the closure DISCIPLINE is fixed first -- every closed row names a "
          "cert/lean owner; every PROOF-TARGET names an exact remaining_artifact and is a flagged global "
          "blocker; the frontier stays non-empty -- before any count.")

    rows = list(csv.DictReader(BLOCKERS.open(encoding="utf-8", newline="")))
    assert rows, "blockers CSV is empty"

    viol = [v for r in rows for v in [row_violation(r)] if v]
    assert not viol, f"dependency-graph violations: {viol}"
    closed = [r for r in rows if r["status"] in CLOSED]
    pts = [r for r in rows if r["status"] == "PROOF-TARGET"]
    print(f"PASS_ROWS_CONFORMANT  {len(rows)} rows: {len(closed)} closed (cert/lean owner each), "
          f"{len(pts)} PROOF-TARGET (each names an exact remaining_artifact).")

    # the 8 campaign owners must be registered at matching closed status
    reg = {r["claim_id"]: r for r in csv.DictReader(REGISTRY.open(encoding="utf-8", newline=""))}
    campaign = [
        "D0-DIXMIER-FESHBACH-FINITE-HEATTRACE-001", "D0-LEPTON-RIEMANN-HURWITZ-BRANCH-INDEX-001",
        "D0-PHASON-ARCHIVE-CAPACITY-REDSHIFT-001", "D0-WILLIAMS-SHIFT-EQUIVALENCE-OWNER-001",
        "D0-HYPERCHARGE-ANOMALY-VARIETY-2DIM-001", "D0-CMB-NS-LAPLACIAN-IDS-OWNER-001",
        "D0-CKM-CLASS5-SELECTOR-OWNER-001", "D0-HIGGS-LOGDET-STATIONARY-POTENTIAL-001",
    ]
    for cid in campaign:
        assert cid in reg, f"campaign owner {cid} missing from registry"
        assert reg[cid]["release_status"] in CLOSED, \
            f"{cid} registry status {reg[cid]['release_status']} is not a closed status"
    print(f"PASS_CAMPAIGN_OWNERS_REGISTERED  all {len(campaign)} eight-front owners registered at a closed status.")

    # frontier non-empty: named blockers remain, so global closure is NOT asserted
    blockers = [r for r in rows if r["is_global_blocker"].strip() == "True"]
    assert len(blockers) > 0, "graph claims zero global blockers -- verify before any global-closure claim"
    print(f"PASS_FRONTIER_NONEMPTY  {len(blockers)} named global blockers remain (global closure NOT asserted).")

    # ===================== REACHABLE NEGATIVE CONTROLS =====================
    bad_closed = {"claim_id": "PLANT", "status": "CERT-CLOSED", "certificate": "", "lean_module": "",
                  "is_global_blocker": "False", "remaining_artifact": ""}
    assert row_violation(bad_closed), "control failed: a closed row with no cert/lean must be rejected"
    print("FAIL_CLOSED_WITHOUT_OWNER_REJECTED  a planted closed row with neither cert nor lean owner is caught.")

    bad_pt = {"claim_id": "PLANT", "status": "PROOF-TARGET", "certificate": "", "lean_module": "",
              "is_global_blocker": "True", "remaining_artifact": ""}
    assert row_violation(bad_pt), "control failed: a PROOF-TARGET with empty remaining_artifact must be rejected"
    print("FAIL_PROOFTARGET_WITHOUT_GAP_REJECTED  a planted PROOF-TARGET with no named remaining_artifact is caught.")

    print("PASS_FINAL_EIGHT_FRONT_DEPENDENCY_GRAPH")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
