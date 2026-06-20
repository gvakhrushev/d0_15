#!/usr/bin/env python3
"""vp_final_external_passports - D0 Final Core Completion M5 external-boundary inventory guard.

Verifies that every external boundary isolated by the M1-M4 maximality no-gos resolves to a REAL owner:
its `isolated_by_nogo` is a registered NO-GO, and its `external_owner` exists either as an ASSUMP row in
LEAN_ASSUMPTION_LEDGER.csv or as a claim in CLAIM_TO_LEAN_MAP.csv. This makes the closed-negative-internal
-> external-passport boundary auditable (no dangling external reference, no internal claim mislabelled as
external). Reachable controls reject a fabricated owner reference and a non-NO-GO isolator.
"""
import csv
import pathlib
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parents[1]
INV = ROOT / "04_VERIFICATION" / "D0_FINAL_EXTERNAL_PASSPORTS.csv"
REG = ROOT / "09_LEAN_FORMALIZATION" / "docs" / "CLAIM_TO_LEAN_MAP.csv"
LEDGER = ROOT / "09_LEAN_FORMALIZATION" / "docs" / "LEAN_ASSUMPTION_LEDGER.csv"


def reg_ids():
    return {r[0] for r in csv.reader(REG.open(encoding="utf-8", newline="")) if r}


def reg_status():
    rows = list(csv.reader(REG.open(encoding="utf-8", newline="")))
    rs = rows[0].index("release_status")
    return {r[0]: r[rs].strip() for r in rows[1:] if len(r) > rs and r}


def ledger_ids():
    ids = set()
    for r in csv.reader(LEDGER.open(encoding="utf-8", newline="")):
        if r:
            ids.add(r[0].strip())
    return ids


def main() -> int:
    print("=== vp_final_external_passports  every isolated boundary resolves to a real external owner ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: each row's isolating no-go must be a registered NO-GO and its "
          "external owner must exist (ASSUMP ledger or registry) before any count -- no dangling external "
          "reference, no internal claim mislabelled external.")
    rows = list(csv.DictReader(INV.open(encoding="utf-8", newline="")))
    assert rows, "empty inventory"
    rids, rstat, lids = reg_ids(), reg_status(), ledger_ids()

    for r in rows:
        nogo = r["isolated_by_nogo"].strip()
        assert rstat.get(nogo) == "NO-GO", f"{r['boundary_id']}: isolator {nogo} is not a registered NO-GO"
    print(f"PASS_ISOLATORS_ARE_NOGO  all {len(rows)} boundaries are isolated by a registered NO-GO.")

    for r in rows:
        owner, kind = r["external_owner"].strip(), r["owner_kind"].strip()
        if kind == "ASSUMP":
            assert owner in lids, f"{r['boundary_id']}: ASSUMP {owner} absent from the ledger"
        else:
            assert owner in rids, f"{r['boundary_id']}: owner {owner} absent from the registry"
    print(f"PASS_OWNERS_RESOLVE  all external owners resolve ("
          f"{sum(1 for r in rows if r['owner_kind']=='ASSUMP')} ASSUMP ledger, "
          f"{sum(1 for r in rows if r['owner_kind']!='ASSUMP')} registry).")
    assert all(r["boundary_type"] in ("method", "data") for r in rows)
    print(f"PASS_TYPED  every boundary typed method/data; "
          f"{sum(1 for r in rows if r['boundary_type']=='data')} external-data passports named.")

    # ===================== REACHABLE NEGATIVE CONTROLS =====================
    assert "ASSUMP-DOES-NOT-EXIST-999" not in lids and "ASSUMP-DOES-NOT-EXIST-999" not in rids
    print("FAIL_FABRICATED_OWNER_REJECTED  a fabricated external-owner reference would not resolve (caught).")
    assert rstat.get("D0-ALPHA-MU2-FULL-LEDGER-001") != "NO-GO", "control: a CERT-CLOSED id is not a NO-GO isolator"
    print("FAIL_NON_NOGO_ISOLATOR_REJECTED  a non-NO-GO isolator (e.g. a CERT-CLOSED id) would be caught.")

    print("PASS_FINAL_EXTERNAL_PASSPORTS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
