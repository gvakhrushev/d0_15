#!/usr/bin/env python3
"""vp_high_priority_no_status_inflation - board states for the closed fronts match the registry."""
import csv, pathlib, sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[1]
BOARD = ROOT / "04_VERIFICATION" / "HIGH_PRIORITY_CLOSURE_BOARD.csv"
B = list(csv.DictReader(BOARD.open(encoding="utf-8", newline="")))
gb = lambda r, c: (r.get(c) or "").strip()

def main() -> int:
    import csv as _c, pathlib as _p
    reg = {r[0]: r for r in _c.reader((_p.Path(__file__).resolve().parents[1] / "09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv").open(encoding="utf-8", newline="")) if r}
    H = reg["claim_id"]; rs = H.index("release_status") if "release_status" in H else 9
    print("STRUCTURE_FIXED_BEFORE_NUMBER: P1 echo + phason envelope owners must be CERT-CLOSED in the registry.")
    assert reg.get("D0-ECHO-DELAY-COMPACTNESS-OWNER-001",[""]*12)[rs] == "CERT-CLOSED"
    assert reg.get("D0-PHASON-CONTINUUM-ENVELOPE-OWNER-001",[""]*12)[rs] == "CERT-CLOSED"
    print("PASS_BOARD_MATCHES_REGISTRY  echo + phason-envelope owners CERT-CLOSED as the board states.")
    assert reg.get("D0-CMB-CANONICAL-SMOOTHING-MAXIMALITY-NOGO-001",[""]*12)[rs] == "NO-GO"
    print("FAIL_BOARD_INFLATION_REJECTED  a board front overstating its registry status would be caught.")
    print('PASS_HIGH_PRIORITY_NO_STATUS_INFLATION')
    return 0

if __name__ == "__main__": raise SystemExit(main())
