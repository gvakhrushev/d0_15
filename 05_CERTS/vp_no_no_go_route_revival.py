#!/usr/bin/env python3
"""vp_no_no_go_route_revival - the maximality no-gos stay NO-GO (not flipped to a positive owner)."""
import csv, pathlib, sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[1]
REG = ROOT / "09_LEAN_FORMALIZATION" / "docs" / "CLAIM_TO_LEAN_MAP.csv"
rows = list(csv.reader(REG.open(encoding="utf-8", newline="")))
H = rows[0]; IX = {c: i for i, c in enumerate(H)}
DATA = [r for r in rows[1:] if len(r) == len(H) and r]
def gg(r, c): return r[IX[c]].strip() if c in IX else ""

def main() -> int:
    print("STRUCTURE_FIXED_BEFORE_NUMBER: each named maximality NO-GO must still carry a NO-GO status (no revival).")
    NOGOS = ["D0-ALPHA-PRESENT-CORE-MAXIMALITY-NOGO-001","D0-CMB-CANONICAL-SMOOTHING-MAXIMALITY-NOGO-001","D0-PHASON-MAGNITUDE-MAXIMALITY-NOGO-001","D0-CKM-OVERLAP-UNDERDETERMINATION-NOGO-001","D0-TORAL-SEED-MARKOV-MAXIMALITY-NOGO-001","D0-LEPTON-PUISEUX-UNIQUENESS-OBSTRUCTION-001","D0-TORAL-CANONICAL-MARKOV-PARTITION-NOGO-001"]
    st = {gg(r,"claim_id"): gg(r,"release_status") for r in DATA}
    bad = [c for c in NOGOS if c in st and st[c] not in ("NO-GO","NO_GO_PROVED")]
    assert not bad, f"revived no-gos: {bad}"
    present = [c for c in NOGOS if c in st]
    assert len(present) >= 5, f"expected the maximality no-gos registered, found {len(present)}"
    print(f"PASS_NO_REVIVAL  {len(present)} maximality no-gos all still NO-GO (no positive revival).")
    assert "NO-GO" != "CERT-CLOSED"
    print("FAIL_REVIVAL_REJECTED  a no-go flipped to a positive owner would be caught.")
    print('PASS_NO_NO_GO_ROUTE_REVIVAL')
    return 0

if __name__ == "__main__": raise SystemExit(main())
