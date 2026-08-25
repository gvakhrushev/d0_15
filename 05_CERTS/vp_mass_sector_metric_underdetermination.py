#!/usr/bin/env python3
"""D0-MASS-SECTOR-METRIC-UNDERDETERMINATION-001 — exact finite mirror.

The admissible shell metric is not an arbitrary radius triple. It is exactly

    (inner, core, outer) = (1, 1+g, 1+2g),  g > 0,

equivalently a torus parameter a=1+2g. Thus naming/order is fixed while one
positive numerical modulus remains. An order-only selector sees the same
(inner<core, core<outer) code for every g and cannot select a unique metric.
"""
from __future__ import annotations

import sys
from fractions import Fraction

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def radii_from_gap(g: Fraction) -> tuple[Fraction, Fraction, Fraction]:
    if g <= 0:
        raise ValueError("the shell gap must be positive")
    return Fraction(1), Fraction(1) + g, Fraction(1) + 2 * g


def gap_from_a(a: Fraction) -> Fraction:
    if a <= 1:
        raise ValueError("the torus parameter must satisfy a>1")
    return (a - 1) / 2


def order_code(radii: tuple[Fraction, Fraction, Fraction]) -> tuple[bool, bool]:
    return radii[0] < radii[1], radii[1] < radii[2]


def main() -> int:
    print("=== D0-MASS-SECTOR-METRIC-UNDERDETERMINATION-001 ===")
    ok = True

    gaps = [Fraction(1, 7), Fraction(1, 2), Fraction(1), Fraction(5, 3), Fraction(9)]
    for g in gaps:
        a = 1 + 2 * g
        recovered = gap_from_a(a)
        radii = radii_from_gap(g)
        if recovered != g or radii != (1, (a + 1) / 2, a):
            print(f"  FAIL (A): roundtrip g={g}, a={a}, recovered={recovered}, radii={radii}")
            ok = False
            break
    else:
        print("  ✓ (A) exact equivalence: a>1 ↔ one positive rational gap g=(a−1)/2")

    for g in gaps:
        inner, core, outer = radii_from_gap(g)
        if core - inner != g or outer - core != g or outer != 1 + 2 * g:
            print(f"  FAIL (B): non-affine shell metric at g={g}")
            ok = False
            break
    else:
        print("  ✓ (B) every shell metric is exactly the affine triple (1,1+g,1+2g)")

    codes = {order_code(radii_from_gap(g)) for g in gaps}
    if codes != {(True, True)}:
        print(f"  FAIL (C): order codes vary: {codes}")
        ok = False
    else:
        print("  ✓ (C) the owned radial-order code is constant for all tested positive gaps")

    g_two = Fraction(1, 2)   # a=2
    g_three = Fraction(1)    # a=3
    r_two = radii_from_gap(g_two)
    r_three = radii_from_gap(g_three)
    if order_code(r_two) != order_code(r_three) or r_two == r_three:
        print(f"  FAIL (D): witnesses do not separate order from metric: {r_two}, {r_three}")
        ok = False
    else:
        print("  ✓ (D) a=2 and a=3 have identical order/naming but distinct numerical metrics")

    # A predicate represented only by the two order bits is constant on the
    # admissible family. Check both possible truth assignments.
    for selected_code in (None, (True, True)):
        selected = [
            g for g in gaps
            if selected_code is not None and order_code(radii_from_gap(g)) == selected_code
        ]
        if len(selected) == 1:
            print(f"  FAIL (E): an order-only selector was uniquely true at {selected[0]}")
            ok = False
            break
    else:
        print("  ✓ (E) every order-only selector chooses either none or the whole family, never one")

    print("\n  -- can-fail controls --")
    rejected = 0
    for bad in (Fraction(0), Fraction(-1, 3)):
        try:
            radii_from_gap(bad)
        except ValueError:
            rejected += 1
    quantitative = [g for g in gaps if g == 1]
    if rejected != 2 or quantitative != [Fraction(1)]:
        print("  FAIL controls: nonpositive gaps or a gap-sensitive unique selector escaped")
        ok = False
    else:
        print("  ✓ nonpositive gaps are rejected")
        print("  ✓ a quantitative gap-sensitive functional can select uniquely")
        print("    (and therefore uses information strictly beyond radial order)")

    print("\n" + (
        "PASS — order/naming is closed; the residual shell metric is exactly one positive modulus"
        if ok else "FAIL"
    ))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
