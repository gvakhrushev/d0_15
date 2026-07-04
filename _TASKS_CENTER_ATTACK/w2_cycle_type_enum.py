#!/usr/bin/env python3
"""TASK W2, Step 1 — EXACT enumeration of the order-12 cycle types in S_8 (and S_7).

Purpose (VERIFIED, computational only):
  Enumerate every integer partition of n (= cycle type of an element of S_n) and its
  lcm (= element order). Report which cycle types have order exactly 12. The claim under
  test is: (4,3,1) is the UNIQUE cycle type of order 12 in S_8.

Discipline:
  - All arithmetic is exact integer arithmetic (partitions, gcd/lcm). No floats.
  - Deterministic: partition generation is a fixed recursion; output is sorted.
  - This decides ONLY the cycle-type uniqueness question. It does NOT claim the 8-point
    carrier is forced (that is the OPEN forcing question, W3 + architect memo).
"""
from math import gcd
from functools import reduce


def lcm(a, b):
    return a * b // gcd(a, b)


def partitions(n, max_part=None):
    """Yield every integer partition of n as a non-increasing tuple. Exact, deterministic."""
    if max_part is None:
        max_part = n
    if n == 0:
        yield ()
        return
    for first in range(min(n, max_part), 0, -1):
        for rest in partitions(n - first, first):
            yield (first,) + rest


def order_of_cycle_type(parts):
    """Order of a permutation with this cycle type = lcm of the cycle lengths (exact)."""
    if not parts:
        return 1
    return reduce(lcm, parts, 1)


def report(n, target_order=12):
    parts_list = list(partitions(n))
    order_map = {p: order_of_cycle_type(p) for p in parts_list}
    hits = sorted(p for p, o in order_map.items() if o == target_order)
    print("=== S_%d : cycle-type (partition) enumeration, exact lcm ===" % n)
    print("total partitions of %d = %d" % (n, len(parts_list)))
    print("cycle types of order exactly %d:" % target_order)
    for p in hits:
        print("   %-18s lcm = %d" % (str(p), order_map[p]))
    print("count of order-%d cycle types = %d" % (target_order, len(hits)))
    return hits, len(parts_list)


def main():
    # ---- S_7 : re-check the frozen no-go premise, (4,3) unique order-12 among 15 partitions ----
    hits7, tot7 = report(7)
    assert tot7 == 15, "S_7 must have 15 partitions"
    assert hits7 == [(4, 3)], "S_7 order-12 cycle type must be exactly {(4,3)}"
    print("PASS_S7_UNIQUE_ORDER12  (4,3) is the unique order-12 cycle type of the 15 partitions of 7.")
    print()

    # ---- S_8 : the task's central uniqueness claim ----
    hits8, tot8 = report(8)
    assert tot8 == 22, "S_8 must have 22 partitions"
    assert hits8 == [(4, 3, 1)], "S_8 order-12 cycle type must be exactly {(4,3,1)}"
    print("PASS_S8_UNIQUE_ORDER12  (4,3,1) is the UNIQUE order-12 cycle type of the 22 partitions of 8.")
    print()

    # ---- Adversarial cross-check: why no rival. Any order-12 type needs a part div. by 4 and a
    #      part div. by 3 (since 12 = 4*3, and no single part <= 8 is divisible by 12). ----
    #      Enumerate ALL order-12 types by that structural argument and confirm the enumeration agrees.
    structural = []
    for p in partitions(8):
        has4 = any(part % 4 == 0 for part in p)   # a part divisible by 4 (i.e. a 4, since 8 alone->order8)
        has3 = any(part % 3 == 0 for part in p)   # a part divisible by 3
        if order_of_cycle_type(p) == 12:
            assert has4 and has3, "order-12 forces a mult-of-4 part and a mult-of-3 part"
            structural.append(p)
    assert structural == [(4, 3, 1)], "structural argument agrees: only (4,3,1)"
    print("PASS_STRUCTURAL_CROSSCHECK  order-12 in S_8 forces one part div by 4 and one div by 3; "
          "with total 8 the only fit is 4+3+1 = (4,3,1).")
    print()
    print("PASS_W2_STEP1_CYCLE_TYPE_UNIQUENESS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
