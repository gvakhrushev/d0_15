#!/usr/bin/env python3
"""vp_continuation_no_status_only_diff - D0-CONTINUATION-NO-STATUS-ONLY-DIFF-001.

Enforces the invariant a status-only diff would violate: a closed-status claim row must carry a real
owner (a python cert and/or a Lean module), never status alone. Specifically every CERT-CLOSED /
NO-GO / PASSPORT-CLOSED row must name a python_cert or a lean_module; no closed row may be a bare
status with no owner-of-record. Reachable control: a planted closed row with neither cert nor module
is rejected.
"""
import csv
import pathlib
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "09_LEAN_FORMALIZATION" / "docs" / "CLAIM_TO_LEAN_MAP.csv"
OWNER_REQUIRED = {"CERT-CLOSED", "NO-GO", "NO_GO_PROVED", "PASSPORT-CLOSED"}


def has_owner(r):
    return bool((r.get("python_cert") or "").strip()) or bool((r.get("lean_module") or "").strip())


def main() -> int:
    print("=== vp_continuation_no_status_only_diff  no closed status without a real owner-of-record ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the rule is fixed first -- every CERT-CLOSED/NO-GO/PASSPORT-CLOSED "
          "row must carry a python cert and/or a Lean module (never status alone) -- before any count.")

    rows = list(csv.DictReader(REGISTRY.open(encoding="utf-8", newline="")))
    offenders = [r["claim_id"] for r in rows if r["release_status"] in OWNER_REQUIRED and not has_owner(r)]
    assert not offenders, f"closed-status rows with NO owner (cert/module) -- status-only: {offenders[:10]}"
    closed = [r for r in rows if r["release_status"] in OWNER_REQUIRED]
    print(f"PASS_NO_STATUS_ONLY  all {len(closed)} closed-status rows carry a cert and/or a Lean module owner.")

    # PASSPORT-CLOSED rows must additionally name a cert (the protocol owner-of-record)
    pp = [r for r in rows if r["release_status"] == "PASSPORT-CLOSED"]
    pp_bad = [r["claim_id"] for r in pp if not (r.get("python_cert") or "").strip()]
    assert not pp_bad, f"PASSPORT-CLOSED rows without a protocol cert: {pp_bad}"
    print(f"PASS_PASSPORT_HAS_CERT  all {len(pp)} PASSPORT-CLOSED rows name a protocol cert.")

    # ===================== REACHABLE NEGATIVE CONTROL =====================
    planted = {"claim_id": "PLANT", "release_status": "CERT-CLOSED", "python_cert": "", "lean_module": ""}
    assert not has_owner(planted), "control mis-set"
    is_status_only = (planted["release_status"] in OWNER_REQUIRED and not has_owner(planted))
    assert is_status_only, "control failed: a closed row with no owner must be flagged status-only"
    print("FAIL_STATUS_ONLY_DIFF_REJECTED  a planted CERT-CLOSED row with neither cert nor module is caught (reachable).")

    print("PASS_CONTINUATION_NO_STATUS_ONLY_DIFF")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
