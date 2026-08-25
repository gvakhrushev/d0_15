#!/usr/bin/env python3
"""D0-PUISEUX-TRANSFER-SATURATION-001 — exact finite mirror.

For P(u)=u/3-u^2/12:

    P(2)-P(u) = (u-2)^2/12 >= 0,

so u=2 is the unique global maximum. On the owned shell coordinates 0,1,2,
the adjacent increments are 1/4 and 1/12; the first is exactly three times
the second. This is a structural saturation/compression law for exponents,
not a physical mass-difference claim.
"""
from __future__ import annotations

import sys
from fractions import Fraction

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def p(u: Fraction) -> Fraction:
    return u / Fraction(3) - u * u / Fraction(12)


def main() -> int:
    print("=== D0-PUISEUX-TRANSFER-SATURATION-001 ===")
    ok = True

    samples = [Fraction(n, 3) for n in range(-15, 28)]
    vertex = Fraction(2)
    identity_ok = all(p(vertex) - p(u) == (u - vertex) ** 2 / Fraction(12) for u in samples)
    if not identity_ok:
        print("  FAIL (A): completed-square vertex identity failed")
        ok = False
    else:
        print("  ✓ (A) P(2)-P(u)=(u-2)²/12 on the exact rational test grid")

    max_ok = all(p(u) <= p(vertex) for u in samples)
    eq_points = [u for u in samples if p(u) == p(vertex)]
    if not max_ok or eq_points != [vertex]:
        print(f"  FAIL (B): max_ok={max_ok}, equality points={eq_points}")
        ok = False
    else:
        print("  ✓ (B) u=2 is the unique global vertex on the test grid")

    values = (p(Fraction(0)), p(Fraction(1)), p(Fraction(2)))
    if values != (Fraction(0), Fraction(1, 4), Fraction(1, 3)):
        print(f"  FAIL (C): shell values={values}")
        ok = False
    else:
        print("  ✓ (C) shell values remain exactly (0,1/4,1/3)")

    d01 = values[1] - values[0]
    d12 = values[2] - values[1]
    if d01 != Fraction(1, 4) or d12 != Fraction(1, 12) or d01 != 3 * d12:
        print(f"  FAIL (D): increments={d01},{d12}")
        ok = False
    else:
        print("  ✓ (D) adjacent increments are 1/4 and 1/12: exact 3:1 compression")

    print("\n  -- can-fail controls --")
    def convex_mutation(u: Fraction) -> Fraction:
        return u / Fraction(3) + u * u / Fraction(12)

    mutated_max = all(convex_mutation(u) <= convex_mutation(vertex) for u in samples)
    mutated_values = tuple(convex_mutation(Fraction(i)) for i in range(3))
    mutated_compression = (
        mutated_values[1] - mutated_values[0]
        == 3 * (mutated_values[2] - mutated_values[1])
    )
    if mutated_max or mutated_compression:
        print("  FAIL controls: convex-sign mutation preserved saturation/compression")
        ok = False
    else:
        print("  ✓ flipping the curvature sign destroys the vertex maximum")
        print("  ✓ curvature mutation destroys the 3:1 compression law")

    print("\n" + (
        "PASS — canonical transfer saturates uniquely at outer shell with 3:1 increment compression"
        if ok else "FAIL"
    ))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
