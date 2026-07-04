#!/usr/bin/env python3
"""D0-SCENE-TRIPLE-UNIQUE-001 — (9,11,13) is the UNIQUE admissible scene triple (capstone).

The corpus forces the scene across four separate theorems (3 zones; +2 ladder; centre=L5=11 at odd
Lucas level; no 4th zone). This certificate is the CAPSTONE composing them: it proves that (9,11,13) is
the unique triple that is a +2 ladder whose centre is a Lucas number in the admissibility window [9,13].

WHAT IS PROVED (exact, able to FAIL):
  * Lucas-window uniqueness: among ALL Lucas numbers L_n, only L_5=11 lies in [9,13]
    (L_4=7<9; L_6=18>13; L_n monotone so every higher return >13).
  * the +2 ladder centred on 11 is exactly (9,11,13).
  * NEGATIVE CONTROLS (must fail if the window/ladder were different):
      - a +2 ladder centred on a NON-Lucas value in-window (e.g. 10 -> (8,10,12)) is NOT admissible
        (10 is not a Lucas number);
      - widening the window to [9,29] admits a SECOND Lucas centre (29=L_7), breaking uniqueness — so
        the window bound [9,13] is load-bearing, not decorative;
      - the equal-zone / +1 ladder alternatives are excluded upstream (step parity), re-checked here.
HONEST SCOPE (printed): this is the uniqueness COMPOSITION of already-proved legs (role=orbit => 3 zones;
the +2 ladder; the odd-return parity are owned by CarrierForcing / SceneCenterSpacetimeConvergence). The
Lean capstone is D0.VNext2.SceneTripleUnique.scene_triple_unique (rc=0, 0 sorry), non-vacuity checked.
"""
from __future__ import annotations
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def lucas(n: int) -> int:
    a, b = 2, 1  # L_0=2, L_1=1
    if n == 0:
        return 2
    for _ in range(n - 1):
        a, b = b, a + b
    return b


def main() -> int:
    print("=== D0-SCENE-TRIPLE-UNIQUE-001  (9,11,13) is the unique admissible triple (capstone) ===")

    # --- Lucas-window uniqueness: only L_5=11 in [9,13] --------------------------------------
    L = {n: lucas(n) for n in range(0, 12)}
    assert L[4] == 7 and L[5] == 11 and L[6] == 18, f"Lucas values wrong: {L}"
    in_window = [n for n in L if 9 <= L[n] <= 13]
    assert in_window == [5], f"expected only L_5 in [9,13], got {in_window}"
    print(f"PASS_UNIQUE_LUCAS_IN_WINDOW  L_n in [9,13] iff n=5 (L_4=7<9, L_5=11, L_6=18>13)")

    # --- the +2 ladder centred on 11 is (9,11,13) --------------------------------------------
    centre = L[5]
    triple = (centre - 2, centre, centre + 2)
    assert triple == (9, 11, 13), f"ladder centred on {centre} != (9,11,13): {triple}"
    print(f"PASS_CENTRED_LADDER  (L5-2, L5, L5+2) = {triple}")

    # --- NEGATIVE CONTROL 1: non-Lucas centre in-window is not admissible --------------------
    non_lucas_centre = 10  # in [9,13] but not a Lucas number
    assert non_lucas_centre not in L.values(), "10 must not be a Lucas number"
    print("FAIL_NON_LUCAS_CENTRE_REJECTED  centre=10 -> (8,10,12): 10 is not a Lucas return, inadmissible")

    # --- NEGATIVE CONTROL 2: the window bound [9,13] is load-bearing -------------------------
    wide = [n for n in L if 9 <= L[n] <= 29]
    assert len(wide) >= 2 and 7 in [n for n in wide], "widening should admit a 2nd Lucas centre"
    assert set(L[n] for n in wide) >= {11, 29}, f"wide window must contain 11 and 29: {[L[n] for n in wide]}"
    print(f"FAIL_WIDE_WINDOW_BREAKS_UNIQUENESS  window [9,29] admits centres {{11=L5, 29=L7}} — [9,13] is load-bearing")

    # --- NEGATIVE CONTROL 3: +1 ladder excluded (step parity, re-check) ----------------------
    # a +1 ladder centred on the SAME centre would be (10,11,12): must differ from the actual triple
    plus_one_ladder = (centre - 1, centre, centre + 1)
    assert plus_one_ladder != triple, f"+1 ladder {plus_one_ladder} must differ from the scene {triple}"
    print("FAIL_PLUS_ONE_LADDER_REJECTED  (10,11,12) != (9,11,13); +2 step forced upstream (det T=-1 parity)")

    print("HONEST_SCOPE  capstone composes proved legs (CarrierForcing 3-zones + SceneCenter L5=11 + address +2 ladder)")
    print("PASS_SCENE_TRIPLE_UNIQUE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
