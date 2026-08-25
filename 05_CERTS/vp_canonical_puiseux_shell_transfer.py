#!/usr/bin/env python3
"""D0-CANONICAL-PUISEUX-SHELL-TRANSFER-001 — exact finite mirror.

Normalize shell radii (1,1+g,1+2g) to u=(r-1)/g=(0,1,2). The unique
quadratic P(u)=c0+c1*u+c2*u^2 matching the owned Puiseux row
(0,1/4,1/3) has

    (c0,c1,c2) = (0, 1/3, -1/12).

Thus the minimal polynomial shell-coordinate transfer has degree exactly two:
affine readout is excluded by unequal spacing, while the unique quadratic is
strictly concave and independent of the free metric gap after normalization.
"""
from __future__ import annotations

import sys
from fractions import Fraction

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def normalized_coords(g: Fraction) -> tuple[Fraction, Fraction, Fraction]:
    if g <= 0:
        raise ValueError("positive shell gap required")
    radii = (Fraction(1), Fraction(1) + g, Fraction(1) + 2 * g)
    return tuple((r - 1) / g for r in radii)


def qshape(c: tuple[Fraction, Fraction, Fraction], u: Fraction) -> Fraction:
    c0, c1, c2 = c
    return c0 + c1 * u + c2 * u * u


def solve_three(y0: Fraction, y1: Fraction, y2: Fraction) -> tuple[Fraction, Fraction, Fraction]:
    # From P(0)=y0, P(1)=y1, P(2)=y2.
    c0 = y0
    c2 = (y2 - 2 * y1 + y0) / 2
    c1 = y1 - c0 - c2
    return c0, c1, c2


def main() -> int:
    print("=== D0-CANONICAL-PUISEUX-SHELL-TRANSFER-001 ===")
    ok = True

    gaps = [Fraction(1, 9), Fraction(1, 2), Fraction(1), Fraction(7, 3), Fraction(11)]
    coords = {normalized_coords(g) for g in gaps}
    if coords != {(Fraction(0), Fraction(1), Fraction(2))}:
        print(f"  FAIL (A): normalized shell coordinates vary: {coords}")
        ok = False
    else:
        print("  ✓ (A) every positive metric gap normalizes the shells to u=(0,1,2)")

    target = (Fraction(0), Fraction(1, 4), Fraction(1, 3))
    coeff = solve_three(*target)
    expected = (Fraction(0), Fraction(1, 3), Fraction(-1, 12))
    if coeff != expected:
        print(f"  FAIL (B): coefficients={coeff}, expected={expected}")
        ok = False
    else:
        print("  ✓ (B) unique quadratic coefficients are (0,1/3,-1/12)")

    values = tuple(qshape(coeff, u) for u in (Fraction(0), Fraction(1), Fraction(2)))
    if values != target:
        print(f"  FAIL (C): quadratic values={values}, target={target}")
        ok = False
    else:
        print("  ✓ (C) P(u)=u/3-u²/12 gives exactly (0,1/4,1/3)")

    curvature = target[2] - 2 * target[1] + target[0]
    if curvature != Fraction(-1, 6) or coeff[2] != curvature / 2 or coeff[2] >= 0:
        print(f"  FAIL (D): curvature={curvature}, c2={coeff[2]}")
        ok = False
    else:
        print("  ✓ (D) discrete curvature=-1/6 and quadratic coefficient=-1/12<0")

    first_gap = target[1] - target[0]
    second_gap = target[2] - target[1]
    if first_gap == second_gap or coeff[2] == 0:
        print("  FAIL (E): affine no-go / genuine quadratic degree was not detected")
        ok = False
    else:
        print("  ✓ (E) unequal spacing excludes degree≤1; nonzero c2 realizes degree 2")

    print("\n  -- can-fail controls --")
    equally_spaced = (Fraction(0), Fraction(1, 6), Fraction(1, 3))
    affine_coeff = solve_three(*equally_spaced)
    try:
        normalized_coords(Fraction(0))
        rejected = False
    except ValueError:
        rejected = True
    # Mutation must collapse quadratic curvature to zero; this ensures the sign/degree
    # conclusion is actually data-dependent rather than a hard-coded PASS.
    if affine_coeff[2] != 0 or not rejected:
        print("  FAIL controls: equally-spaced mutation or nonpositive-gap rejection failed")
        ok = False
    else:
        print("  ✓ equally-spaced mutation collapses c2 to zero (affine control)")
        print("  ✓ nonpositive metric gap is rejected")

    print("\n" + (
        "PASS — unique normalized transfer is the concave quadratic u/3-u²/12"
        if ok else "FAIL"
    ))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
