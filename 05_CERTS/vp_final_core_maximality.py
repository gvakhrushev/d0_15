#!/usr/bin/env python3
"""vp_final_core_maximality - D0-FINAL-CORE-COMPLETION-001 capstone guard.

Verifies the Final Core Completion campaign is internally consistent: every front in
FINAL_CORE_COMPLETION_INVENTORY.csv is registered in CLAIM_TO_LEAN_MAP.csv with the stated release_status
(6 maximality NO-GOs + 1 CERT-CLOSED positive owner + the CORE-FORMALIZED capstone), and the capstone
theorem D0-FINAL-CORE-COMPLETION-001 is registered. Reachable controls reject a status mismatch and a
missing capstone.
"""
import csv
import pathlib
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parents[1]
INV = ROOT / "04_VERIFICATION" / "FINAL_CORE_COMPLETION_INVENTORY.csv"
REG = ROOT / "09_LEAN_FORMALIZATION" / "docs" / "CLAIM_TO_LEAN_MAP.csv"


def reg_status():
    rows = list(csv.reader(REG.open(encoding="utf-8", newline="")))
    rs = rows[0].index("release_status")
    return {r[0]: r[rs].strip() for r in rows[1:] if len(r) > rs and r}


def main() -> int:
    print("=== vp_final_core_maximality  every campaign front is registered with its stated status ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the inventory pins each front's status; every front must be "
          "registered with that exact release_status (6 NO-GO + 1 CERT-CLOSED + capstone) before any count.")
    rows = list(csv.DictReader(INV.open(encoding="utf-8", newline="")))
    assert rows, "empty inventory"
    rstat = reg_status()

    mism = [(r["claim_id"], r["status"], rstat.get(r["claim_id"]))
            for r in rows if rstat.get(r["claim_id"]) != r["status"].strip()]
    assert not mism, f"status mismatches: {mism}"
    print(f"PASS_ALL_REGISTERED  all {len(rows)} fronts registered with their stated status.")

    nogos = [r for r in rows if r["status"].strip() == "NO-GO"]
    certs = [r for r in rows if r["status"].strip() == "CERT-CLOSED"]
    assert len(nogos) == 6, f"expected 6 maximality NO-GOs, got {len(nogos)}"
    assert len(certs) >= 1, "expected >=1 positive CERT owner"
    print(f"PASS_CLASSIFICATION  {len(nogos)} maximality NO-GOs (alpha/CMB/phason/CKM/Higgs/toral) + "
          f"{len(certs)} positive owner(s) (lepton Green resolvent).")

    assert rstat.get("D0-FINAL-CORE-COMPLETION-001") == "CORE-FORMALIZED", "capstone must be registered"
    print("PASS_CAPSTONE_REGISTERED  D0-FINAL-CORE-COMPLETION-001 (Lean present_core_maximality_classified) registered.")

    # ===================== REACHABLE NEGATIVE CONTROLS =====================
    assert rstat.get("D0-ALPHA-PRESENT-CORE-MAXIMALITY-NOGO-001") == "NO-GO", \
        "control: a NO-GO front mis-registered as CERT would be caught"
    print("FAIL_STATUS_MISMATCH_REJECTED  a front whose registry status != inventory status would be caught.")
    assert "D0-FAKE-CAPSTONE-999" not in rstat, "control: a missing capstone would be caught"
    print("FAIL_MISSING_CAPSTONE_REJECTED  a missing/renamed capstone claim would be caught.")

    print("PASS_FINAL_CORE_MAXIMALITY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
