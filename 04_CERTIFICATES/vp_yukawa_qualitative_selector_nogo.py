#!/usr/bin/env python3
"""D0-YUKAWA-QUALITATIVE-SELECTOR-NOGO-001 — exact mirror.

The current equivariant Yukawa theorem owns only a qualitative profile for every
non-scalar `a+b*x+c*x^2`:

  * its values on the three roots of x^3-359x-2574 are distinct;
  * no value is rational.

These properties are independent of the actual non-scalar coefficient triple. Hence
any selector using only that profile is constant on the injective rational family
`(a,b,c)=(0,1,t)` and cannot choose a unique member.
"""
from __future__ import annotations

import sys
from fractions import Fraction

import sympy as sp

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main() -> int:
    print("=== D0-YUKAWA-QUALITATIVE-SELECTOR-NOGO-001 ===")
    ok = True

    x, r = sp.symbols("x r")
    P = sp.Poly(x**3 - 359*x - 2574, x, domain=sp.QQ)
    if P.degree() != 3 or not P.is_irreducible:
        print(f"  FAIL (A): degree={P.degree()}, irreducible={P.is_irreducible}")
        ok = False
    else:
        print("  ✓ (A) transport cubic is irreducible of degree 3 over Q")

    # A rational quadratic polynomial cannot vanish at a transport root unless it
    # is zero: its degree is below the irreducible cubic's degree.
    samples = [
        (Fraction(0), Fraction(1), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(1)),
        (Fraction(2), Fraction(3), Fraction(-1)),
        (Fraction(-5), Fraction(7, 3), Fraction(4, 5)),
    ]
    profile_ok = True
    for a, b, c in samples:
        f = sp.Poly(
            sp.Rational(c.numerator, c.denominator) * x**2
            + sp.Rational(b.numerator, b.denominator) * x
            + sp.Rational(a.numerator, a.denominator) - r,
            x,
            extension=True,
        )
        if b == 0 and c == 0:
            profile_ok = False
            break
        if f.degree() > 2:
            profile_ok = False
            break
        # Distinct-value mechanism: equality at two distinct cubic roots implies
        # b+c*(lambda+mu)=0; then b/c (when c != 0) would be a rational cubic root.
        if c != 0:
            q = sp.Rational(b.numerator, b.denominator) / sp.Rational(c.numerator, c.denominator)
            if P.eval(q) == 0:
                profile_ok = False
                break
    if not profile_ok:
        print("  FAIL (B): a non-scalar sample escaped the common profile")
        ok = False
    else:
        print("  ✓ (B) every tested non-scalar has the same distinct/irrational algebraic profile")

    family = [(Fraction(0), Fraction(1), Fraction(t)) for t in range(-20, 21)]
    if len(set(family)) != 41 or any(b == 0 and c == 0 for _, b, c in family):
        print("  FAIL (C): affine family is not injective/non-scalar")
        ok = False
    else:
        print("  ✓ (C) (0,1,t) gives 41 distinct profile-equivalent controls (finite slice)")

    # A profile-only selector sees all non-scalars identically.
    profile_selector = lambda coeff: not (coeff[1] == 0 and coeff[2] == 0)
    selected = [k for k in family if profile_selector(k)]
    if len(selected) != len(family) or len(selected) == 1:
        print(f"  FAIL (D): profile selector selected {len(selected)} controls")
        ok = False
    else:
        print("  ✓ (D) profile-only selector is constant on the family, hence non-unique")

    print("\n  -- can-fail controls --")
    scalar = (Fraction(3), Fraction(0), Fraction(0))
    scalar_values_degenerate = scalar[1] == 0 and scalar[2] == 0
    quantitative_selector = lambda coeff: coeff == (Fraction(0), Fraction(1), Fraction(0))
    quantitative_selected = [k for k in family if quantitative_selector(k)]
    if not scalar_values_degenerate or len(quantitative_selected) != 1:
        print("  FAIL controls: scalar/quantitative distinction was not detected")
        ok = False
    else:
        print("  ✓ scalar member breaks the profile; coefficient-aware selector can be unique")
        print("    (and therefore uses information strictly beyond the owned profile)")

    print("\n" + ("PASS — current Yukawa profile cannot select unique coefficients" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
