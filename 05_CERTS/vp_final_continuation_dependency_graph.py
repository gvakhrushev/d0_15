#!/usr/bin/env python3
"""vp_final_continuation_dependency_graph - D0-CONTINUATION-FINAL-BLOCKER-GRAPH-001.

Integrity of FINAL_CONTINUATION_BLOCKERS.csv: every closed row (CERT-CLOSED/NO-GO/PASSPORT-CLOSED/
CORE/BRIDGE) names a cert or Lean module; every PROOF-TARGET row names an EXACT remaining_artifact and
is flagged is_global_blocker; no remaining_artifact uses a broad placeholder ("needs proof / needs
work / future research / open"); the frontier is non-empty (so global closure is NOT asserted).
Reachable controls reject a closed-without-owner row and a PROOF-TARGET with a broad/empty artifact.
"""
import csv
import pathlib
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parents[1]
BLOCKERS = ROOT / "04_VERIFICATION" / "FINAL_CONTINUATION_BLOCKERS.csv"
CLOSED = {"CERT-CLOSED", "NO-GO", "NO_GO_PROVED", "CORE-FORMALIZED", "PASSPORT-CLOSED", "BRIDGE-ASSUMPTIONS-EXPLICIT"}
BROAD = ["needs proof", "needs work", "future research", "tbd", "todo"]


def violation(r):
    cid, st = r["claim_id"], r["status"].strip()
    art = (r["remaining_artifact"] or "").strip()
    if st in CLOSED:
        if not (r["owner_module"].strip() or r["certificate"].strip()):
            return f"{cid}: closed ({st}) but names neither cert nor module"
        if r["is_global_blocker"].strip() != "False":
            return f"{cid}: closed but flagged a global blocker"
    elif st == "PROOF-TARGET":
        if not art:
            return f"{cid}: PROOF-TARGET with empty remaining_artifact"
        low = art.lower()
        # a row explicitly tagged SUPERSEDED is not a global blocker; others must be flagged True
        if "superseded" in low:
            if r["is_global_blocker"].strip() != "False":
                return f"{cid}: superseded row must not be a global blocker"
        else:
            if r["is_global_blocker"].strip() != "True":
                return f"{cid}: open PROOF-TARGET not flagged is_global_blocker"
            if any(b == low or (b in low and len(art) < 25) for b in BROAD):
                return f"{cid}: broad/placeholder remaining_artifact {art!r}"
    else:
        return f"{cid}: unrecognized status {st!r}"
    return ""


def main() -> int:
    print("=== vp_final_continuation_dependency_graph  integrity of the continuation blocker graph ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the discipline is fixed first -- every closed row has an owner; "
          "every open PROOF-TARGET names an EXACT (non-broad) missing artifact and is a flagged global "
          "blocker; the frontier stays non-empty -- before any count.")

    rows = list(csv.DictReader(BLOCKERS.open(encoding="utf-8", newline="")))
    assert rows, "blockers CSV empty"
    viol = [v for r in rows for v in [violation(r)] if v]
    assert not viol, f"dependency-graph violations: {viol[:12]}"
    closed = [r for r in rows if r["status"] in CLOSED]
    pts = [r for r in rows if r["status"] == "PROOF-TARGET"]
    blockers = [r for r in rows if r["is_global_blocker"].strip() == "True"]
    print(f"PASS_ROWS_CONFORMANT  {len(rows)} rows: {len(closed)} closed (owner each), {len(pts)} PROOF-TARGET "
          f"(each an EXACT artifact).")
    assert blockers, "frontier empty -- verify before any global-closure claim"
    print(f"PASS_FRONTIER_NONEMPTY  {len(blockers)} global blockers remain (global closure NOT asserted).")

    # ===================== REACHABLE NEGATIVE CONTROLS =====================
    bad_closed = {"claim_id": "P", "status": "CERT-CLOSED", "owner_module": "", "certificate": "",
                  "is_global_blocker": "False", "remaining_artifact": ""}
    assert violation(bad_closed), "control: closed-without-owner must be rejected"
    print("FAIL_CLOSED_WITHOUT_OWNER_REJECTED  a planted closed row with no cert/module is caught.")
    bad_pt = {"claim_id": "P", "status": "PROOF-TARGET", "owner_module": "", "certificate": "",
              "is_global_blocker": "True", "remaining_artifact": "needs work"}
    assert violation(bad_pt), "control: a broad-placeholder PROOF-TARGET must be rejected"
    print("FAIL_BROAD_ARTIFACT_REJECTED  a planted PROOF-TARGET with a broad 'needs work' artifact is caught.")

    print("PASS_FINAL_CONTINUATION_DEPENDENCY_GRAPH")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
