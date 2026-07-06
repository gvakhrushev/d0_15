#!/usr/bin/env python3
"""w5_interface_check.py — certifies the checkable claims of W5_INTERFACE_SPEC.md.

READ-ONLY: reads the registry CSVs, asserts the counts and cross-reference
(de)syncs stated in the spec, prints PASS/FAIL per check. Never writes.

Run from repo root or this directory.
"""
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CLAIM_MAP = os.path.join(ROOT, "09_LEAN_FORMALIZATION", "docs", "CLAIM_TO_LEAN_MAP.csv")
LEDGER = os.path.join(ROOT, "09_LEAN_FORMALIZATION", "docs", "LEAN_ASSUMPTION_LEDGER.csv")
EXT_REG = os.path.join(ROOT, "04_VERIFICATION", "EXTERNAL_ASSUMPTION_REGISTRY.csv")

failures = []


def check(name, cond, detail=""):
    status = "PASS" if cond else "FAIL"
    print(f"[{status}] {name}" + (f"  ({detail})" if detail else ""))
    if not cond:
        failures.append(name)


rows = list(csv.DictReader(open(CLAIM_MAP)))
ledger = list(csv.DictReader(open(LEDGER)))
extreg = list(csv.DictReader(open(EXT_REG)))

# --- Section 0 / 1.0 counts -------------------------------------------------
true_rows = [r for r in rows if r["uses_bridge_assumptions"] == "True"]
cbs = [r for r in rows if r["release_status"] == "CORE_BRIDGE_SPLIT"]
bc = [r for r in rows if r["release_status"] == "BRIDGE-CALIBRATION"]
check("545 registry rows", len(rows) == 545, str(len(rows)))
check("29 uses_bridge_assumptions=True rows", len(true_rows) == 29, str(len(true_rows)))
check("8 CORE_BRIDGE_SPLIT rows", len(cbs) == 8, str(len(cbs)))
check("3 BRIDGE-CALIBRATION rows", len(bc) == 3, str(len(bc)))
overlap = {r["claim_id"] for r in true_rows} & {r["claim_id"] for r in cbs}
check("overlap True∩CBS == {D0-CARRIER-003}", overlap == {"D0-CARRIER-003"}, str(overlap))
unique_bridge_shaped = {r["claim_id"] for r in true_rows} | {r["claim_id"] for r in cbs} | {
    r["claim_id"] for r in bc}
check("39 unique bridge-shaped rows", len(unique_bridge_shaped) == 39,
      str(len(unique_bridge_shaped)))

lp_wba = [r for r in true_rows
          if r["lean_status"] == "LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS"]
check("28 of the 29 are LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS", len(lp_wba) == 28,
      str(len(lp_wba)))
py_true = [r["claim_id"] for r in true_rows if r["lean_status"] == "PYTHON_CERTIFIED"]
check("the 29th is D0-LATTICE-FINITENESS-BRIDGE-001 (PYTHON_CERTIFIED)",
      py_true == ["D0-LATTICE-FINITENESS-BRIDGE-001"], str(py_true))

# --- ASSUMP id inventories (FLAG-1) ------------------------------------------
csv_ids = set()
for r in rows:
    for a in r["assumption_ids"].split(";"):
        a = a.strip()
        if a:
            csv_ids.add(a)
ledger_ids = {r["assumption_id"] for r in ledger}
extreg_ids = {r["assumption_id"] for r in extreg}
check("22 distinct ASSUMP ids in CLAIM_TO_LEAN_MAP", len(csv_ids) == 22, str(len(csv_ids)))
check("24 ASSUMP ids in LEAN_ASSUMPTION_LEDGER", len(ledger_ids) == 24, str(len(ledger_ids)))
check("26 ASSUMP ids in EXTERNAL_ASSUMPTION_REGISTRY", len(extreg_ids) == 26,
      str(len(extreg_ids)))
check("ledger-only ids == {JONES-INDEX, MORDELL-E8}",
      ledger_ids - csv_ids == {"ASSUMP-JONES-INDEX", "ASSUMP-MORDELL-E8"},
      str(ledger_ids - csv_ids))
check("registry-only ids == {PRL-RQM-GENERAL, NO-EXOTIC-FERMIONS, LEPTON-EFT-DECIMALS}",
      extreg_ids - ledger_ids == {"ASSUMP-PRL-RQM-GENERAL", "ASSUMP-NO-EXOTIC-FERMIONS",
                                  "ASSUMP-LEPTON-EFT-DECIMALS"},
      str(extreg_ids - ledger_ids))
check("every CSV ASSUMP id has a ledger entry", csv_ids <= ledger_ids,
      str(csv_ids - ledger_ids))

# --- per-type multiplicities (Section 1) -------------------------------------
from collections import Counter
mult = Counter()
for r in rows:
    for a in r["assumption_ids"].split(";"):
        a = a.strip()
        if a:
            mult[a] += 1
expected_mult = {
    "ASSUMP-HST-EXTERNAL": 4,
    "ASSUMP-LINDEMANN-LNPHI": 7,
    "ASSUMP-LORENTZ-MACRO": 2,
    "ASSUMP-RG-SMOOTH-INTERP": 2,
    "ASSUMP-SMOOTH-COVARIANCE": 2,
    "ASSUMP-SMOOTH-HEATTRACE": 2,
    "ASSUMP-HURWITZ-GOLDEN": 1,
}
for aid, n in expected_mult.items():
    check(f"{aid} carried by {n} row(s)", mult[aid] == n, f"actual {mult[aid]}")
singletons = [a for a in csv_ids if mult[a] == 1]
check("16 singleton ASSUMP ids in CSV (incl. HURWITZ-GOLDEN)", len(singletons) == 16,
      str(len(singletons)))

# six-type coverage: rows whose ids are all within the ORIGINAL six (LINDEMANN excluded)
six = set(expected_mult) - {"ASSUMP-LINDEMANN-LNPHI"}
six_rows = [r for r in true_rows
            if all(a.strip() in six for a in r["assumption_ids"].split(";") if a.strip())]
check("6-type block covers 7 of the 29 True-rows", len(six_rows) == 7, str(len(six_rows)))

# --- the 8 conditional owners (Section 2) ------------------------------------
owners = [
    "D0-CONNES-RECONSTRUCTION-OWNER-001", "D0-DIXMIER-RESIDUE-OWNER-001",
    "D0-RIEFFEL-GHP-CONTINUUM-OWNER-001", "D0-TIME-MODULAR-FLOW-OWNER-001",
    "D0-ADLER-WEISS-PARTITION-OWNER-001", "D0-COMPLEX-QM-FORCING-001",
    "D0-M1-INFO-RECONSTRUCTION-001", "D0-ENTROPIC-DARK-GRAVITY-001",
]
byid = {r["claim_id"]: r for r in rows}
ok = True
for o in owners:
    r = byid.get(o)
    if r is None or r["uses_bridge_assumptions"] != "True" or ";" in r["assumption_ids"].strip(";"):
        ok = False
check("8 owner rows exist, True, single-ASSUMP each", ok)

# --- LINDEMANN consumer roster (Section 1.B / FLAG-6) -------------------------
lind = sorted(r["claim_id"] for r in rows
              if "ASSUMP-LINDEMANN-LNPHI" in r["assumption_ids"])
expected_lind = sorted([
    "D0-CVFT-F1", "D0-ALPHA-LOG-CESARO-MEASURABILITY-NOGO-001",
    "D0-POSTCORE-DIXMIER-WODZICKI-PASSPORT-001", "D0-POSTCORE-EXTENSION-BOUNDARY-001",
    "D0-ALPHA-ANALYTIC-FORMALISM-BOUNDARY-001",
    "D0-RAW-ALPHA-ANALYTIC-RESIDUE-BOUNDARY-001", "D0-X5-ALPHA-BOUNDARY-001",
])
check("LINDEMANN consumer roster matches spec (7 rows)", lind == expected_lind, str(lind))

# --- FLAG-2: phantom ledger claim_id ------------------------------------------
ledger_claims = {r["claim_id"] for r in ledger}
csv_claims = {r["claim_id"] for r in rows}
phantom = ledger_claims - csv_claims
check("ledger claim_ids absent from CLAIM_TO_LEAN_MAP == {D0-CONVEX-RESPONSE-BRIDGE}",
      phantom == {"D0-CONVEX-RESPONSE-BRIDGE"}, str(phantom))

# --- FLAG-5: adjacency rows are False/CORE-FORMALIZED --------------------------
for cid in ["D0-PHI-HURWITZ-001", "D0-JONES-INDEX-PHI-001", "D0-ICOSIAN-E8-GRAM-001"]:
    r = byid[cid]
    check(f"{cid} is uses_bridge=False + CORE-FORMALIZED",
          r["uses_bridge_assumptions"] == "False" and r["release_status"] == "CORE-FORMALIZED")

# --- 053040 guard: none of the 39 rows is a 053040 row -------------------------
check("no bridge-shaped row contains '053040'",
      not any("053040" in cid for cid in unique_bridge_shaped))

# --- verdict -------------------------------------------------------------------
print()
if failures:
    print(f"RESULT: FAIL ({len(failures)} failed): {failures}")
    sys.exit(1)
print("RESULT: ALL CHECKS PASS")
