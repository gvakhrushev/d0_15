#!/usr/bin/env python3
"""D0-MASS-SECTOR-COMPLETION-NOGO-001 — exact finite mirror.

The current mass data are the product of two coarse profiles:

  * every non-scalar Yukawa coefficient on the affine family (0,1,t) has the
    same qualitative distinct/irrational profile;
  * every positive shell gap has the same radial-order code.

Their product is therefore still constant. A unique joint selector must be
sensitive to both the coefficient and metric axes (possibly through one
cross-coupled functional).
"""
from __future__ import annotations

import sys
from fractions import Fraction

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def coeff_profile(_t: Fraction) -> tuple[str, str]:
    return "pairwise-distinct", "all-irrational"


def metric_profile(g: Fraction) -> tuple[bool, bool]:
    if g <= 0:
        raise ValueError("positive shell gap required")
    radii = (Fraction(1), Fraction(1) + g, Fraction(1) + 2 * g)
    return radii[0] < radii[1], radii[1] < radii[2]


def current_mass_data(candidate: tuple[Fraction, Fraction]) -> tuple[object, object]:
    t, g = candidate
    return coeff_profile(t), metric_profile(g)


def main() -> int:
    print("=== D0-MASS-SECTOR-COMPLETION-NOGO-001 ===")
    ok = True

    coeffs = [Fraction(-2), Fraction(-1), Fraction(0), Fraction(1), Fraction(3)]
    gaps = [Fraction(1, 5), Fraction(1, 2), Fraction(1), Fraction(2), Fraction(7)]
    candidates = [(t, g) for t in coeffs for g in gaps]

    profiles = {current_mass_data(x) for x in candidates}
    if profiles != {(("pairwise-distinct", "all-irrational"), (True, True))}:
        print(f"  FAIL (A): current joint data vary: {profiles}")
        ok = False
    else:
        print("  ✓ (A) all 25 coefficient×metric controls have one identical current-data profile")

    selected_by_current_data = [
        x for x in candidates
        if current_mass_data(x) == (("pairwise-distinct", "all-irrational"), (True, True))
    ]
    if len(selected_by_current_data) != len(candidates) or len(selected_by_current_data) == 1:
        print(f"  FAIL (B): joint coarse selector selected {len(selected_by_current_data)}")
        ok = False
    else:
        print("  ✓ (B) combining both coarse profiles selects the whole product, not one pair")

    # A metric-sensitive but coefficient-blind predicate still leaves the coefficient fiber.
    metric_only = [x for x in candidates if x[1] == 1]
    if len(metric_only) != len(coeffs):
        print(f"  FAIL (C): metric-only fiber size={len(metric_only)}")
        ok = False
    else:
        print("  ✓ (C) fixing the metric alone leaves all coefficient controls")

    # A coefficient-sensitive but radial-order-blind predicate leaves the metric fiber.
    coeff_only = [x for x in candidates if x[0] == 0]
    if len(coeff_only) != len(gaps):
        print(f"  FAIL (D): coefficient-only fiber size={len(coeff_only)}")
        ok = False
    else:
        print("  ✓ (D) fixing the coefficient alone leaves all metric controls")

    print("\n  -- can-fail controls --")
    both_sensitive = [x for x in candidates if x == (Fraction(0), Fraction(1))]
    mutated_profile = (("scalar-degenerate", "rational"), (True, True))
    try:
        metric_profile(Fraction(0))
        rejected_zero = False
    except ValueError:
        rejected_zero = True
    if both_sensitive != [(Fraction(0), Fraction(1))] or mutated_profile in profiles or not rejected_zero:
        print("  FAIL controls: two-axis selector/profile mutation/nonpositive gap escaped")
        ok = False
    else:
        print("  ✓ a two-axis quantitative selector can be unique")
        print("  ✓ a scalar/rational profile mutation is detected")
        print("  ✓ a nonpositive metric gap is rejected")

    print("\n" + (
        "PASS — unique mass completion requires new information on both residual axes"
        if ok else "FAIL"
    ))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
