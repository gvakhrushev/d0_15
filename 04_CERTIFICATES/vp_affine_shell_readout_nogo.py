#!/usr/bin/env python3
"""D0-AFFINE-SHELL-READOUT-NOGO-001 — exact finite mirror.

An affine readout m(s) = alpha + beta*radius(s) of the three shells with radii
(1, 1+g, 1+2g) is always equally spaced: both adjacent gaps equal beta*g, so the
discrete second difference is zero and the total span is exactly twice the first
gap, independent of the free modulus g and of alpha, beta.

Consequently any unequally spaced target spectrum is unreachable by every affine
readout. The owned charged-lepton Puiseux row (0, 1/4, 1/3) is not equally spaced,
so the exponent transfer is genuinely nonlinear in the shell radius.
"""
from __future__ import annotations

import sys
from fractions import Fraction

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def affine_readout(g: Fraction, alpha: Fraction, beta: Fraction) -> tuple[Fraction, Fraction, Fraction]:
    if g <= 0:
        raise ValueError("positive shell gap required")
    radii = (Fraction(1), Fraction(1) + g, Fraction(1) + 2 * g)
    return tuple(alpha + beta * r for r in radii)


def main() -> int:
    print("=== D0-AFFINE-SHELL-READOUT-NOGO-001 ===")
    ok = True

    samples = [
        (Fraction(1, 2), Fraction(0), Fraction(1)),
        (Fraction(1), Fraction(-3), Fraction(5)),
        (Fraction(7, 3), Fraction(2), Fraction(-4)),
        (Fraction(9), Fraction(11), Fraction(13)),
    ]

    spaced_ok = True
    ratio_ok = True
    for g, alpha, beta in samples:
        m0, m1, m2 = affine_readout(g, alpha, beta)
        if (m1 - m0) != (m2 - m1):
            spaced_ok = False
            break
        if (m2 - m0) != 2 * (m1 - m0):
            ratio_ok = False
            break
    if not spaced_ok:
        print("  FAIL (A): an affine readout was not equally spaced")
        ok = False
    else:
        print("  ✓ (A) every affine readout is equally spaced (second difference zero)")
    if not ratio_ok:
        print("  FAIL (B): span was not twice the first gap")
        ok = False
    else:
        print("  ✓ (B) total span is exactly twice the first gap for all (g, alpha, beta)")

    # Gap independence: the equal-spacing invariant does not depend on g, alpha, beta.
    codes = {
        ((m1 - m0) == (m2 - m1))
        for g, alpha, beta in samples
        for (m0, m1, m2) in [affine_readout(g, alpha, beta)]
    }
    if codes != {True}:
        print(f"  FAIL (C): equal-spacing invariant varied: {codes}")
        ok = False
    else:
        print("  ✓ (C) equal-spacing is a parameter-free structural invariant")

    # Puiseux row is unequally spaced -> not affine-reachable.
    p_e, p_mu, p_tau = Fraction(0), Fraction(1, 4), Fraction(1, 3)
    if (p_mu - p_e) == (p_tau - p_mu):
        print("  FAIL (D): the Puiseux row was equally spaced")
        ok = False
    else:
        print(f"  ✓ (D) owned Puiseux row (0,1/4,1/3) is unequally spaced: "
              f"1/4 vs {p_tau - p_mu} -> not an affine shell readout")

    print("\n  -- can-fail controls --")
    # An explicitly equally spaced target IS affine-reachable (positive control).
    reachable_target = (Fraction(0), Fraction(1), Fraction(2))
    m = affine_readout(Fraction(1, 2), Fraction(-2), Fraction(2))  # (0,1,2)
    positive_ok = (m == reachable_target)
    # A nonpositive gap must be rejected.
    try:
        affine_readout(Fraction(0), Fraction(0), Fraction(1))
        rejected = False
    except ValueError:
        rejected = True
    if not positive_ok or not rejected:
        print("  FAIL controls: reachable equal-spaced target or nonpositive-gap rejection failed")
        ok = False
    else:
        print("  ✓ an equally spaced target is affine-reachable (linear map suffices there)")
        print("  ✓ a nonpositive shell gap is rejected")

    print("\n" + (
        "PASS — affine shell readout forces equal spacing; the mass transfer must be nonlinear"
        if ok else "FAIL"
    ))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
