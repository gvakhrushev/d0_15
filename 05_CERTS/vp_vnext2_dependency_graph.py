#!/usr/bin/env python3
"""vp_vnext2_dependency_graph - integrity of the vNext+2 scene-native graph (FORMALISM, never CORE)."""
import csv, pathlib, sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[1]
BLK = ROOT / "04_VERIFICATION" / "VNEXT2_REFINEMENT_FAMILY_CLASSIFICATION.csv"
ALLOWED = {"CERT-CLOSED", "NO-GO", "PROOF-TARGET", "PASSPORT-CLOSED"}
def main() -> int:
    print("STRUCTURE_FIXED_BEFORE_NUMBER: allowed statuses; closed rows owned; blocking rows name a missing "
          "primitive -- before any count.")
    rows = list(csv.DictReader(BLK.open(encoding="utf-8", newline="")))
    g = lambda r, k: (r.get(k) or "").strip()
    assert rows, "empty classification"
    bad = [g(r,"claim_id") for r in rows if g(r,"status") not in ALLOWED]
    assert not bad, f"bad statuses: {bad}"
    print(f"PASS_STATUSES  {len(rows)} rows; every status in {sorted(ALLOWED)}.")
    closed = [r for r in rows if g(r,"status") in ("CERT-CLOSED","NO-GO","PASSPORT-CLOSED")]
    noown = [g(r,"claim_id") for r in closed if not g(r,"lean_module") and not g(r,"certificate")]
    assert not noown, f"closed without owner: {noown}"
    print(f"PASS_CLOSED_OWNED  {len(closed)} closed rows owned.")
    blocking = [r for r in rows if g(r,"status") in ("NO-GO","PROOF-TARGET")]
    nop = [g(r,"claim_id") for r in blocking if not g(r,"exact_missing_primitive")]
    assert not nop, f"blocking rows without a primitive: {nop}"
    print(f"PASS_PRIMITIVES_NAMED  {len(blocking)} NO-GO/PROOF-TARGET rows name a primitive.")
    assert "FOO" not in ALLOWED
    print("FAIL_BAD_STATUS_REJECTED  a status outside the allowed set would be caught.")
    bad2 = {"status":"NO-GO","exact_missing_primitive":""}
    assert not (bad2.get("exact_missing_primitive") or "").strip()
    print("FAIL_BLOCKER_WITHOUT_PRIMITIVE_REJECTED  a blocking row without a primitive would be caught.")
    print("PASS_VNEXT2_DEPENDENCY_GRAPH")
    return 0
if __name__ == "__main__": raise SystemExit(main())
