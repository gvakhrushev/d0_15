#!/usr/bin/env python3
"""D0-TYPED-DETECTOR-PRIMITIVE-EXHAUSTION-001 — exact finite mirror.

Inside the full three-capability ambient (membership,value,history), primitive
profiles are singleton supports. Requiring history-blindness leaves exactly
two: membership and value. The history singleton is retained as a negative
control. Count=2 seals the port-power zone bound; admitting history gives
count=3 and zone 17.
"""
from __future__ import annotations

import sys
from itertools import product

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def primitive(v):
    return sum(bool(x) for x in v) == 1


def zone_bound(n):
    return all(9 + 2**k <= 13 for k in range(1, n + 1))


def main() -> int:
    print("=== D0-TYPED-DETECTOR-PRIMITIVE-EXHAUSTION-001 ===")
    ok = True

    ambient = list(product((False, True), repeat=3))
    primitives = [v for v in ambient if primitive(v)]
    detector = [v for v in primitives if not v[2]]
    expected = [(False, True, False), (True, False, False)]

    if set(detector) != set(expected) or len(detector) != 2:
        print(f"  FAIL (A): detector primitive profiles={detector}")
        ok = False
    else:
        print("  ✓ (A) exactly two history-blind primitive profiles: membership and value")

    history = (False, False, True)
    if history not in primitives or history in detector:
        print("  FAIL (B): history negative control misclassified")
        ok = False
    else:
        print("  ✓ (B) history remains primitive in ambient but is excluded from detector layer")

    if not zone_bound(len(detector)):
        print("  FAIL (C): typed detector count did not seal zone 13")
        ok = False
    else:
        print("  ✓ (C) detector primitive count 2 seals all port-power zones at <=13")

    print("\n  -- can-fail controls --")
    unstratified_count = len(primitives)
    if unstratified_count != 3 or zone_bound(unstratified_count):
        print("  FAIL controls: unstratified third capability did not reopen the bound")
        ok = False
    else:
        print("  ✓ restoring history gives 3 primitives and reopens size 8 / zone 17")

    print("\n" + (
        "PASS — typed detector layer has exactly two primitive capability kinds"
        if ok else "FAIL"
    ))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
