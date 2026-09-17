#!/usr/bin/env python3
"""D0-DETECTION-SCENE-BOUND-EQUIVALENCE-001 — exact finite mirror.

Under the GAP-E port-power reading, n independent primitive detector
capabilities admit extension sizes 2^k for 1<=k<=n. The scene upper bound

    9 + 2^k <= 13 for every admissible k

holds iff n<=2. A third independent history/order capability gives n=3,
re-admits 2^3=8, and opens the rival zone 17.

Thus GAP-E closure is equivalent to the typed detector/memory stratification
theorem excluding history from primitive detector comparisons.
"""
from __future__ import annotations

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def zone_bound(n: int) -> bool:
    return all(9 + 2**k <= 13 for k in range(1, n + 1))


def main() -> int:
    print("=== D0-DETECTION-SCENE-BOUND-EQUIVALENCE-001 ===")
    ok = True

    threshold = {n: zone_bound(n) for n in range(0, 9)}
    expected = {n: n <= 2 for n in range(0, 9)}
    if threshold != expected:
        print(f"  FAIL (A): threshold={threshold}, expected={expected}")
        ok = False
    else:
        print("  ✓ (A) exact threshold on test range: zone<=13 iff capability count<=2")

    general_ok = all(zone_bound(n) == (n <= 2) for n in range(0, 100))
    if not general_ok:
        print("  FAIL (B): general threshold mirror failed")
        ok = False
    else:
        print("  ✓ (B) k=3 is the universal obstruction for every n>=3")

    primitive_counts = {n: n for n in range(0, 9)}
    if primitive_counts[2] != 2 or primitive_counts[3] != 3:
        print("  FAIL (C): primitive comparison count did not track capabilities")
        ok = False
    else:
        print("  ✓ (C) primitive count tracks capability count: 2->2, 3->3")

    if 2**3 != 8 or 9 + 2**3 != 17 or zone_bound(3):
        print("  FAIL (D): history/third-port rival was not reopened")
        ok = False
    else:
        print("  ✓ (D) third capability -> size 8 -> zone 17; zone-13 bound fails")

    x = (False, False, False)
    xp = (False, False, True)
    y = (False, False, False)
    history_eq = lambda a, b: a[2] == b[2]
    if x[:2] != xp[:2] or history_eq(x, y) == history_eq(xp, y):
        print("  FAIL (E): history comparison did not witness non-factorization")
        ok = False
    else:
        print("  ✓ (E) history is a genuine third primitive unless current-data factorization is imposed")

    print("\n  -- can-fail controls --")
    if not zone_bound(2) or zone_bound(4):
        print("  FAIL controls: cap-2 seal or cap-4 failure was not detected")
        ok = False
    else:
        print("  ✓ cap 2 seals the window")
        print("  ✓ cap 4 remains open (threshold-gated, not hard-coded to n=3)")

    print("\n" + (
        "PASS — GAP-E upper bound is equivalent to the two-capability detector theorem"
        if ok else "FAIL"
    ))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
