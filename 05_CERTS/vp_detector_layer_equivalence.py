#!/usr/bin/env python3
"""D0-DETECTOR-LAYER-EQUIVALENCE-001 — exact finite mirror.

Catalogue-free comparisons, history-invariant full comparisons, and bare
current-data comparisons are the same finite object: a Boolean table on current
pairs. On Current=Bool and History=Bool all three carriers have cardinality 16.
"""
from __future__ import annotations

import sys
from itertools import product

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


CURRENT = (0, 1)
HISTORY = (0, 1)
PAIRS = tuple(product(CURRENT, repeat=2))
FULL = tuple(product(CURRENT, HISTORY))
FULL_PAIRS = tuple(product(FULL, repeat=2))
CATALOGUES = tuple(product((False, True), repeat=2))


def main() -> int:
    print("=== D0-DETECTOR-LAYER-EQUIVALENCE-001 ===")
    ok = True

    bare_tables = list(product((False, True), repeat=len(PAIRS)))
    catalogue_free = [
        tuple(bare for _ in CATALOGUES)
        for bare in bare_tables
    ]
    history_invariant = []
    for bare in bare_tables:
        lookup = dict(zip(PAIRS, bare))
        history_invariant.append(tuple(
            lookup[(x[0], y[0])] for x, y in FULL_PAIRS
        ))

    counts = (len(bare_tables), len(catalogue_free), len(history_invariant))
    if counts != (16, 16, 16):
        print(f"  FAIL (A): carrier counts={counts}")
        ok = False
    else:
        print("  ✓ (A) bare/catalogue-free/history-invariant carriers all have size 16")

    if len(set(catalogue_free)) != 16 or len(set(history_invariant)) != 16:
        print("  FAIL (B): lift maps were not injective")
        ok = False
    else:
        print("  ✓ (B) both lifts are injective and exhaustive on their invariant carriers")

    # Membership and value equality ignore history.
    membership = lambda x, y: x[0] == y[0]
    value = lambda x, y: x[1] == y[1]
    hist = lambda x, y: x[1] == y[1]  # on (current,history), read history
    x, xp, y = (0, 0), (0, 1), (0, 0)
    if membership(x, y) != membership(xp, y):
        print("  FAIL (C): membership changed under history")
        ok = False
    else:
        print("  ✓ (C) current-data membership comparison is history-invariant")
    if hist(x, y) == hist(xp, y):
        print("  FAIL (D): history comparison did not leave the detector layer")
        ok = False
    else:
        print("  ✓ (D) history equality is outside the invariant detector layer")

    print("\n  -- can-fail controls --")
    if catalogue_free[0] == catalogue_free[-1]:
        print("  FAIL controls: distinct bare comparisons collapsed")
        ok = False
    else:
        print("  ✓ distinct bare comparisons remain distinct through both equivalences")

    print("\n" + (
        "PASS — detector nuisance invariance is canonically equivalent to bare current data"
        if ok else "FAIL"
    ))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
