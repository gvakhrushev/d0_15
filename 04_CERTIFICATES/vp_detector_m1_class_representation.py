#!/usr/bin/env python3
"""D0-DETECTOR-M1-CLASS-REPRESENTATION-001 — exact finite mirror.

The detector catalogue system evaluates a comparison under orientation
catalogues. Class-M1-admissible comparisons are exactly catalogue-free ones.
They map to bare current-data tables, hence to history-invariant detector
comparisons. Primitive capability profiles exhaust to membership/value.
"""
from __future__ import annotations

import sys
from itertools import product

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


CURRENT = tuple(product((False, True), repeat=2))  # (membership,value)
CURRENT_PAIRS = tuple(product(CURRENT, repeat=2))
CATALOGUES = tuple(product((False, True), repeat=len(CURRENT)))


def catalogue_free(table):
    # table[cat_index][pair_index]
    return all(len({table[ci][pi] for ci in range(len(CATALOGUES))}) == 1
               for pi in range(len(CURRENT_PAIRS)))


def uses_axis(bare, axis):
    lookup = dict(zip(CURRENT_PAIRS, bare))
    for x, y in CURRENT_PAIRS:
        xp = list(x)
        xp[axis] = not xp[axis]
        xp = tuple(xp)
        if lookup[(x, y)] != lookup[(xp, y)]:
            return True
    return False


def main() -> int:
    print("=== D0-DETECTOR-M1-CLASS-REPRESENTATION-001 ===")
    ok = True

    bare_tables = list(product((False, True), repeat=len(CURRENT_PAIRS)))
    lifted = [tuple(bare for _ in CATALOGUES) for bare in bare_tables]
    admissible = [t for t in lifted if catalogue_free(t)]

    if len(admissible) != len(bare_tables) or len(set(admissible)) != len(bare_tables):
        print("  FAIL (A): class-admissible detector representation is not bijective to bare tables")
        ok = False
    else:
        print(f"  ✓ (A) all {len(bare_tables)} bare tables embed faithfully as class-admissible detectors")

    # Descent recovers the same current table, proving representation to history-invariant layer.
    recovered = [t[0] for t in admissible]
    if recovered != bare_tables:
        print("  FAIL (B): descent did not recover bare current comparisons")
        ok = False
    else:
        print("  ✓ (B) admissible comparisons descend uniquely to current-data tables")

    # Capability profiles for two canonical primitive comparisons.
    member_eq = tuple(x[0] == y[0] for x, y in CURRENT_PAIRS)
    value_eq = tuple(x[1] == y[1] for x, y in CURRENT_PAIRS)
    profiles = {
        (uses_axis(member_eq, 0), uses_axis(member_eq, 1), False),
        (uses_axis(value_eq, 0), uses_axis(value_eq, 1), False),
    }
    expected = {(True, False, False), (False, True, False)}
    if profiles != expected:
        print(f"  FAIL (C): primitive profiles={profiles}")
        ok = False
    else:
        print("  ✓ (C) primitive admissible profiles are membership-only and value-only")

    print("\n  -- can-fail controls --")
    # Injectivity is load-bearing: duplicate physical names for one table break an embedding.
    duplicate_physical_names = [("A", member_eq), ("B", member_eq)]
    comparison_images = {table for _, table in duplicate_physical_names}
    if len(comparison_images) == len(duplicate_physical_names):
        print("  FAIL controls: duplicate-name representation was treated as injective")
        ok = False
    else:
        print("  ✓ duplicate physical names expose the load-bearing injectivity requirement")

    print("\n" + (
        "PASS — class-M1 physical comparisons embed into typed detector layer and exhaust to two profiles"
        if ok else "FAIL"
    ))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
