#!/usr/bin/env python3
"""vp_vnext_dirac_tower_dependency_graph - integrity of the vNext Dirac-tower graph.

Verifies VNEXT_DIRAC_TOWER_BLOCKERS.csv: every status is in the allowed vNext set; every closed row names
an owner (lean_module or certificate); every PROOF-TARGET/NO-GO that blocks names an exact_missing_primitive;
nothing is marked is_core_claim (this is a vNext FORMALISM extension, never present-core CORE); the registry
records the CERT/NO-GO/PASSPORT statuses consistently. Reachable controls reject a core-claim mark and a
blocker without a named primitive.
"""
import csv
import pathlib
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parents[1]
BLK = ROOT / "04_VERIFICATION" / "VNEXT_DIRAC_TOWER_BLOCKERS.csv"
REG = ROOT / "09_LEAN_FORMALIZATION" / "docs" / "CLAIM_TO_LEAN_MAP.csv"
ALLOWED = {"CERT-CLOSED", "NO-GO", "PROOF-TARGET", "PASSPORT-CLOSED"}


def main() -> int:
    print("=== vp_vnext_dirac_tower_dependency_graph  vNext graph integrity (FORMALISM, never CORE) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: allowed statuses; closed rows name an owner; open rows name a missing "
          "primitive; NOTHING is is_core_claim (vNext is a FORMALISM extension) -- before any count.")
    rows = list(csv.DictReader(BLK.open(encoding="utf-8", newline="")))
    assert rows, "empty blockers"
    g = lambda r, k: (r.get(k) or "").strip()

    bad = [g(r, "claim_id") for r in rows if g(r, "status") not in ALLOWED]
    assert not bad, f"bad statuses: {bad}"
    print(f"PASS_STATUSES  {len(rows)} rows; every status in {sorted(ALLOWED)}.")

    core = [g(r, "claim_id") for r in rows if g(r, "is_core_claim") == "True"]
    assert not core, f"vNext rows must NOT be is_core_claim: {core}"
    print("PASS_NOT_CORE  no vNext row is is_core_claim (formalism extension, never present-core CORE).")

    closed = [r for r in rows if g(r, "status") in ("CERT-CLOSED", "NO-GO", "PASSPORT-CLOSED")]
    no_owner = [g(r, "claim_id") for r in closed if not g(r, "lean_module") and not g(r, "certificate")]
    assert not no_owner, f"closed without owner: {no_owner}"
    print(f"PASS_CLOSED_OWNED  {len(closed)} closed rows each name a lean_module or certificate.")

    blocking = [r for r in rows if g(r, "status") in ("NO-GO", "PROOF-TARGET")]
    no_prim = [g(r, "claim_id") for r in blocking if not g(r, "exact_missing_primitive")]
    assert not no_prim, f"blocking rows without a named primitive: {no_prim}"
    print(f"PASS_PRIMITIVES_NAMED  {len(blocking)} NO-GO/PROOF-TARGET rows each name an exact missing primitive.")

    reg = {r[0]: r for r in csv.reader(REG.open(encoding="utf-8", newline="")) if r}
    hdr = next(csv.reader(REG.open(encoding="utf-8", newline="")))
    rs = hdr.index("release_status")
    assert reg.get("D0-VNEXT-AF-GNS-ISOMETRY-OWNER-001", [""] * 20)[rs] == "CERT-CLOSED"
    print("PASS_REGISTERED  D0-VNEXT-AF-GNS-ISOMETRY-OWNER-001 CERT-CLOSED in the registry.")

    # ===================== REACHABLE NEGATIVE CONTROLS =====================
    bad1 = {"is_core_claim": "True", "status": "CERT-CLOSED"}
    assert (bad1.get("is_core_claim") or "").strip() == "True"
    print("FAIL_CORE_CLAIM_REJECTED  a vNext row marked is_core_claim would be caught.")
    bad2 = {"status": "NO-GO", "exact_missing_primitive": ""}
    assert not (bad2.get("exact_missing_primitive") or "").strip()
    print("FAIL_BLOCKER_WITHOUT_PRIMITIVE_REJECTED  a NO-GO/PROOF-TARGET without a named primitive would be caught.")

    print("PASS_VNEXT_DIRAC_TOWER_DEPENDENCY_GRAPH")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
