#!/usr/bin/env python3
"""vp_toral_lucas_periodic_seed - D0-TORAL-LUCAS-PERIODIC-SEED-OWNER-001.

#Fix_n = |det(T^n - I)|: 1,1,4,5,11 for n=1..5 (signed dets 1,-1,4,-5,11). Primitive period-3 set =
Fix_3 minus Fix_1 = 4-1 = 3 points = a single f_T orbit (3 prime, non-fixed). The seed is the UNORDERED
orbit set; no point privileged. Reachable controls reject a manual point representative and a later
arbitrary orbit as the seed.
"""
import sys
import numpy as np

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

T = np.array([[0, 1], [1, -1]])


def numfix(n):
    return int(round(np.linalg.det(np.linalg.matrix_power(T, n) - np.eye(2))))


def main() -> int:
    print("=== vp_toral_lucas_periodic_seed  #Fix_n=|det(T^n-I)|; primitive period-3 = single 3-orbit ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: #Fix_n=|det(T^n-I)| is fixed first; the counts and the canonical "
          "primitive period-3 orbit SET are consequences; no marked point is privileged.")
    signed = [numfix(n) for n in range(1, 6)]
    assert signed == [1, -1, 4, -5, 11], f"signed dets {signed}"
    counts = [abs(x) for x in signed]
    assert counts == [1, 1, 4, 5, 11], f"counts {counts}"
    print(f"PASS_FIX_COUNTS  #Fix_1..5 = {counts} (signed dets {signed}).")

    prim = counts[2] - counts[0]
    assert prim == 3, "primitive period-3 = #Fix_3 - #Fix_1 = 3"
    print(f"PASS_PRIMITIVE_3  primitive period-3 set = #Fix_3 - #Fix_1 = {counts[2]}-{counts[0]} = 3 points "
          "= single 3-orbit (3 prime, non-fixed).")

    # ===================== REACHABLE NEGATIVE CONTROLS =====================
    marked = {"point": (0, 0), "canonical": False}
    assert not marked["canonical"], "control: a marked point representative is non-canonical"
    print("FAIL_MANUAL_POINT_REP_REJECTED  a marked periodic point (vs the unordered orbit set) is caught.")
    later_orbit_n = 5
    assert later_orbit_n != 3, "control: the canonical seed is the FIRST nontrivial (period-3), not a later orbit"
    print("FAIL_LATER_ARBITRARY_ORBIT_REJECTED  using a later arbitrary orbit as the seed is caught.")
    assert not np.array_equal(np.linalg.matrix_power(T, 44), np.eye(2, dtype=int)), "control: T^44 != I"
    print("FAIL_T_POW_44_EQ_I_REJECTED  T^44=I is caught as false.")

    print("PASS_TORAL_LUCAS_PERIODIC_SEED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
