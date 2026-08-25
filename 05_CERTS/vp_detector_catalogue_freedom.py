#!/usr/bin/env python3
"""D0-DETECTOR-CATALOGUE-FREEDOM-001 — exact finite mirror.

M1 half of the detector/memory stratification. A detector comparison may consult
an external orientation catalogue o : Current -> Bool. It is catalogue-free
(M1-admissible) when its output never depends on o.

  * catalogue-free  <=>  factors through a bare current-data comparison (order-blind);
  * the order/history comparison is NOT catalogue-free: two catalogues give
    different outputs on the same current pair, so it requires the external
    orientation datum M1 forbids as mandatory.
"""
from __future__ import annotations

import sys
from itertools import product

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


CURRENT = [0, 1]  # a two-point current-data carrier (Bool)
CATALOGUES = [dict(zip(CURRENT, bits)) for bits in product([False, True], repeat=len(CURRENT))]


def order_comparison(o, x, y):
    return o[x] == o[y]


def lift(base, o, x, y):
    return base(x, y)


def is_catalogue_free(cmp):
    for x, y in product(CURRENT, repeat=2):
        outs = {cmp(o, x, y) for o in CATALOGUES}
        if len(outs) > 1:
            return False
    return True


def main() -> int:
    print("=== D0-DETECTOR-CATALOGUE-FREEDOM-001 ===")
    ok = True

    # (A) every lift of a bare comparison is catalogue-free.
    bases = [
        lambda x, y: x == y,          # value/membership equality
        lambda x, y: x != y,
        lambda x, y: True,
        lambda x, y: False,
    ]
    if all(is_catalogue_free(lambda o, x, y, b=b: lift(b, o, x, y)) for b in bases):
        print("  ✓ (A) every bare current-data comparison lifts to a catalogue-free detector")
    else:
        print("  FAIL (A): a bare lift depended on the catalogue")
        ok = False

    # (B) catalogue-free <=> factors through a bare comparison.
    #     bareOf(cmp) := cmp(constant-false); catalogue-free cmp must equal its lift.
    def bare_of(cmp):
        const_false = {c: False for c in CURRENT}
        return lambda x, y: cmp(const_false, x, y)

    cf_lift = lambda o, x, y: lift(lambda a, b: a == b, o, x, y)
    reconstructed = bare_of(cf_lift)
    if all(cf_lift(o, x, y) == reconstructed(x, y)
           for o in CATALOGUES for x, y in product(CURRENT, repeat=2)):
        print("  ✓ (B) catalogue-free comparisons equal the lift of their bare projection")
    else:
        print("  FAIL (B): factorization failed")
        ok = False

    # (C) the order comparison is NOT catalogue-free.
    if not is_catalogue_free(order_comparison):
        print("  ✓ (C) order/history comparison requires the external orientation catalogue")
    else:
        print("  FAIL (C): order comparison was catalogue-free")
        ok = False

    # (D) exact separating witnesses.
    o_const = {0: False, 1: False}
    o_id = {0: False, 1: True}
    if order_comparison(o_const, 0, 1) and not order_comparison(o_id, 0, 1):
        print("  ✓ (D) witnesses: constant catalogue -> equal; identity catalogue -> separated")
    else:
        print("  FAIL (D): separating witnesses not realized")
        ok = False

    print("\n  -- can-fail controls --")
    # A comparison that ignores the catalogue but is mislabeled must still be catalogue-free;
    # and a genuinely order-reading comparison must be caught.
    ignores = lambda o, x, y: (x == y)
    if is_catalogue_free(ignores) and not is_catalogue_free(order_comparison):
        print("  ✓ the test distinguishes catalogue-free from catalogue-consulting comparisons")
    else:
        print("  FAIL controls: catalogue-dependence detector is not discriminating")
        ok = False

    print("\n" + (
        "PASS — detector catalogue-freedom (M1) forces order-blindness; order needs a catalogue"
        if ok else "FAIL"
    ))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
