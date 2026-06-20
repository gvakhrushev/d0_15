#!/usr/bin/env python3
"""vp_higgs_phason_orbit_dependency_graph - integrity of the Higgs phason-orbit closure graph."""
import csv, pathlib, sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[1]
BLOCKERS = ROOT / "04_VERIFICATION" / "HIGGS_PHASON_ORBIT_BLOCKERS.csv"
REG = ROOT / "09_LEAN_FORMALIZATION" / "docs" / "CLAIM_TO_LEAN_MAP.csv"
CLOSED = {"CERT-CLOSED", "NO-GO", "CORE-FORMALIZED", "PASSPORT-CLOSED"}


def viol(r):
    st = r["status"].strip()
    if st in CLOSED:
        if not r["certificate"].strip() and not r["lean_module"].strip():
            return f"{r['claim_id']}: closed but no owner"
        if r["is_global_blocker"].strip() != "False":
            return f"{r['claim_id']}: closed but flagged global blocker"
    elif st == "PROOF-TARGET":
        if not r["exact_missing_artifact"].strip(): return f"{r['claim_id']}: PT no artifact"
        if r["is_global_blocker"].strip() != "True": return f"{r['claim_id']}: PT not flagged"
    else:
        return f"{r['claim_id']}: bad status {st!r}"
    return ""


def main() -> int:
    print("=== vp_higgs_phason_orbit_dependency_graph  integrity of the Higgs phason-orbit graph ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: closed rows name an owner + not global blocker; PROOF-TARGETs name "
          "an exact missing artifact and are flagged; frontier non-empty -- before any count.")
    rows = list(csv.DictReader(BLOCKERS.open(encoding="utf-8", newline="")))
    assert rows, "empty blockers"
    vs = [v for r in rows for v in [viol(r)] if v]
    assert not vs, f"violations: {vs}"
    print(f"PASS_ROWS_CONFORMANT  {len(rows)} rows; closed name owners, PROOF-TARGETs name artifacts.")
    reg = {r["claim_id"]: r for r in csv.DictReader(REG.open(encoding="utf-8", newline=""))}
    assert reg.get("D0-HIGGS-RETURN-QUOTIENT-ACTION-OWNER-001", {}).get("release_status") == "CERT-CLOSED"
    assert reg.get("D0-HIGGS-PHASON-ORBIT-TRIVIAL-NOGO-001", {}).get("release_status") == "NO-GO"
    print("PASS_OWNERS_REGISTERED  return-action CERT-CLOSED + phason-orbit NO-GO registered.")
    blk = [r for r in rows if r["is_global_blocker"].strip() == "True"]
    assert blk, "frontier must be non-empty"
    print(f"PASS_FRONTIER_NONEMPTY  {len(blk)} named global blockers (condensation route open).")
    bad = {"claim_id": "X", "status": "CERT-CLOSED", "certificate": "", "lean_module": "", "is_global_blocker": "False", "exact_missing_artifact": ""}
    assert viol(bad), "control"
    print("FAIL_CLOSED_WITHOUT_OWNER_REJECTED  a planted closed-without-owner row is caught.")
    bad2 = {"claim_id": "X", "status": "PROOF-TARGET", "certificate": "", "lean_module": "", "is_global_blocker": "True", "exact_missing_artifact": ""}
    assert viol(bad2), "control"
    print("FAIL_PROOFTARGET_WITHOUT_ARTIFACT_REJECTED  a planted PROOF-TARGET without artifact is caught.")
    print("PASS_HIGGS_PHASON_ORBIT_DEPENDENCY_GRAPH")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
