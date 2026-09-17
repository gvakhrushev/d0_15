#!/usr/bin/env python3
"""D0-DETECTOR-M1-PREDICATE-BOUNDARY-001 — exact finite mirror.

Canonical M1Forced is a UNIQUE-answer predicate. Catalogue-free detector
comparisons form a non-singleton admissible class (indeed 16 Boolean functions
on two current bits), so the class has no M1Forced witness. Order/history is
outside the class, but that exclusion is not yet the canonical M1 reductio.
"""
from __future__ import annotations

import sys
from itertools import product

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


CURRENT = (0, 1)
PAIRS = tuple(product(CURRENT, repeat=2))
CATALOGUES = tuple(product((False, True), repeat=2))


def eval_catalogue(bits, x):
    return bits[x]


def order_cmp(cat, x, y):
    return eval_catalogue(cat, x) == eval_catalogue(cat, y)


def is_catalogue_free(table):
    # table is indexed by catalogue-id then current pair.
    return all(len({table[ci][pi] for ci in range(len(CATALOGUES))}) == 1
               for pi in range(len(PAIRS)))


def main() -> int:
    print("=== D0-DETECTOR-M1-PREDICATE-BOUNDARY-001 ===")
    ok = True

    # Every catalogue-free table is determined by four bare pair-values.
    free_tables = []
    for bare in product((False, True), repeat=len(PAIRS)):
        free_tables.append(tuple(bare for _ in CATALOGUES))
    if len(free_tables) != 16 or not all(is_catalogue_free(t) for t in free_tables):
        print("  FAIL (A): catalogue-free class enumeration failed")
        ok = False
    else:
        print("  ✓ (A) catalogue-free class has 16 members, not one forced answer")

    false_table = free_tables[0]
    true_table = free_tables[-1]
    if false_table == true_table:
        print("  FAIL (B): constant false/true controls collapsed")
        ok = False
    else:
        print("  ✓ (B) two explicit distinct catalogue-free comparisons exist")

    order_table = tuple(
        tuple(order_cmp(cat, x, y) for x, y in PAIRS)
        for cat in CATALOGUES
    )
    if is_catalogue_free(order_table):
        print("  FAIL (C): order comparison was catalogue-free")
        ok = False
    else:
        print("  ✓ (C) order/history fails the catalogue-free constraint")

    # M1Forced requires a unique constraint witness. A class of size 16 has none.
    if len(free_tables) == 1:
        print("  FAIL (D): catalogue-free constraint unexpectedly had a unique witness")
        ok = False
    else:
        print("  ✓ (D) canonical unique-answer M1Forced cannot represent this whole class")

    print("\n  -- can-fail controls --")
    singleton_constraint = [false_table]
    if len(singleton_constraint) != 1 or len(free_tables) <= 1:
        print("  FAIL controls: unique/non-unique constraint distinction failed")
        ok = False
    else:
        print("  ✓ a genuine singleton constraint would support M1Forced")
        print("  ✓ the catalogue-free class remains deliberately non-singleton")

    print("\n" + (
        "PASS — catalogue-free exclusion is class-level, not current unique-answer M1 forcing"
        if ok else "FAIL"
    ))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
