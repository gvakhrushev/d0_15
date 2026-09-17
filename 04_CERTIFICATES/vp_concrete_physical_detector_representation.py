#!/usr/bin/env python3
"""D0-CONCRETE-PHYSICAL-DETECTOR-REPRESENTATION-001 — finite exact mirror.

Exhaustive small-carrier verification of the concrete representation theorem.
Observations are (current,history) with both Boolean. A two-sided catalogue
assigns histories independently to the left and right comparison arguments.

Across all 2^16 Boolean full-comparison tables:
  class-level catalogue invariance <=> full history invariance.

The invariant class has exactly 2^4=16 members, one for every bare current-pair
table. A one-sided catalogue is shown insufficient by a reachable control.
"""
from __future__ import annotations

import sys
from itertools import product

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


CURRENT = (0, 1)
HISTORY = (0, 1)
OBS = tuple(product(CURRENT, HISTORY))
OBS_PAIRS = tuple(product(OBS, repeat=2))
CURRENT_PAIRS = tuple(product(CURRENT, repeat=2))
FUNCTIONS = tuple(product(HISTORY, repeat=len(CURRENT)))  # Current -> History
TWO_SIDED = tuple(product(FUNCTIONS, repeat=2))


def lookup(table, x, y):
    return table[OBS_PAIRS.index((x, y))]


def history_invariant(table):
    for c1, c2 in CURRENT_PAIRS:
        vals = {
            lookup(table, (c1, h1), (c2, h2))
            for h1, h2 in product(HISTORY, repeat=2)
        }
        if len(vals) != 1:
            return False
    return True


def two_sided_catalogue_invariant(table):
    for c1, c2 in CURRENT_PAIRS:
        vals = set()
        for left, right in TWO_SIDED:
            vals.add(lookup(table, (c1, left[c1]), (c2, right[c2])))
        if len(vals) != 1:
            return False
    return True


def main() -> int:
    print("=== D0-CONCRETE-PHYSICAL-DETECTOR-REPRESENTATION-001 ===")
    ok = True

    invariant_count = 0
    mismatch = None
    for table in product((False, True), repeat=len(OBS_PAIRS)):
        hi = history_invariant(table)
        ci = two_sided_catalogue_invariant(table)
        if hi:
            invariant_count += 1
        if hi != ci:
            mismatch = table
            break

    if mismatch is not None:
        print("  FAIL (A): class-M1 invariance != history invariance")
        ok = False
    else:
        print("  ✓ (A) exhaustive 2^16 tables: two-sided class-M1 iff history-invariant")

    if invariant_count != 2 ** len(CURRENT_PAIRS):
        print(f"  FAIL (B): invariant count={invariant_count}, expected=16")
        ok = False
    else:
        print("  ✓ (B) exactly 16 invariant full comparisons = 16 bare current tables")

    # Positive/negative concrete controls.
    membership = tuple(x[0] == y[0] for x, y in OBS_PAIRS)
    history = tuple(x[1] == y[1] for x, y in OBS_PAIRS)
    if not history_invariant(membership) or history_invariant(history):
        print("  FAIL (C): membership/history controls misclassified")
        ok = False
    else:
        print("  ✓ (C) current equality admissible; history equality rejected")

    print("\n  -- can-fail controls --")
    # A single shared catalogue cannot realize h_left != h_right when c_left=c_right.
    # The comparison below differs only on same-current, unequal-history inputs, so a
    # one-sided catalogue would miss it; the two-sided system catches it.
    hidden = tuple(
        (x[0] == y[0] and x[1] != y[1])
        for x, y in OBS_PAIRS
    )
    one_sided_outputs = {
        tuple(lookup(hidden, (c1, f[c1]), (c2, f[c2]))
              for c1, c2 in CURRENT_PAIRS)
        for f in FUNCTIONS
    }
    two_sided_outputs = {
        tuple(lookup(hidden, (c1, left[c1]), (c2, right[c2]))
              for c1, c2 in CURRENT_PAIRS)
        for left, right in TWO_SIDED
    }
    if len(one_sided_outputs) != 1 or len(two_sided_outputs) <= 1:
        print("  FAIL controls: two-sided catalogue load-bearing test failed")
        ok = False
    else:
        print("  ✓ one-sided catalogue misses a same-current history dependence")
        print("  ✓ two-sided catalogue detects it (independent argument histories are load-bearing)")

    print("\n" + (
        "PASS — concrete D0 observation system instantiates class-M1 detector representation"
        if ok else "FAIL"
    ))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
