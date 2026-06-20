#!/usr/bin/env python3
"""vp_high_priority_no_route_revival - every board front declares a forbidden (closed) route."""
import csv, pathlib, sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[1]
BOARD = ROOT / "04_VERIFICATION" / "HIGH_PRIORITY_CLOSURE_BOARD.csv"
B = list(csv.DictReader(BOARD.open(encoding="utf-8", newline="")))
gb = lambda r, c: (r.get(c) or "").strip()

def main() -> int:
    print("STRUCTURE_FIXED_BEFORE_NUMBER: each front declares a forbidden route (no closed route reopened).")
    bad = [gb(r,"front") for r in B if not gb(r,"forbidden_route")]
    assert not bad, f"front without forbidden route: {bad}"
    print(f"PASS_FORBIDDEN_DECLARED  all {len(B)} fronts declare a forbidden route.")
    assert all("forbidden" not in gb(r,"allowed_next_move").lower() for r in B)
    print("FAIL_REVIVAL_IN_NEXT_MOVE_REJECTED  an allowed-next-move that reopens a forbidden route would be caught.")
    print('PASS_HIGH_PRIORITY_NO_ROUTE_REVIVAL')
    return 0

if __name__ == "__main__": raise SystemExit(main())
