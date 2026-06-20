#!/usr/bin/env python3
"""vp_high_priority_board - every front names an owner, exit condition, and a primitive-or-external."""
import csv, pathlib, sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[1]
BOARD = ROOT / "04_VERIFICATION" / "HIGH_PRIORITY_CLOSURE_BOARD.csv"
B = list(csv.DictReader(BOARD.open(encoding="utf-8", newline="")))
gb = lambda r, c: (r.get(c) or "").strip()

def main() -> int:
    print("STRUCTURE_FIXED_BEFORE_NUMBER: each board front names owner + exit_condition + (primitive or external) before any count.")
    assert B, "empty board"
    bad = [gb(r,"front") for r in B if not gb(r,"owner") or not gb(r,"exit_condition")]
    assert not bad, f"front without owner/exit: {bad}"
    print(f"PASS_BOARD_OWNED  {len(B)} fronts each name an owner and exit condition.")
    nogap = [gb(r,"front") for r in B if not gb(r,"minimum_new_primitive") and not gb(r,"external_passport")]
    assert not nogap, f"front naming neither primitive nor external: {nogap}"
    print("PASS_BOARD_GAP_NAMED  each front names a minimum new primitive or an external passport.")
    assert all(gb(r,"forbidden_route") for r in B)
    print("FAIL_BOARD_WITHOUT_FORBIDDEN_REJECTED  a front without a named forbidden route would be caught.")
    print('PASS_HIGH_PRIORITY_BOARD')
    return 0

if __name__ == "__main__": raise SystemExit(main())
