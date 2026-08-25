#!/usr/bin/env python3
"""D0-CHARGED-LEPTON-SHELL-BRIDGE-001 — exact finite mirror.

Owned orders:
  electron < muon < tau by Puiseux exponents 0 < 1/4 < 1/3;
  innerD9 < coreD11 < outerD13 by every admissible torus radius.

Exactly one of the 3! branch→shell bijections preserves those orders.
"""
from __future__ import annotations

import sys
from fractions import Fraction
from itertools import permutations

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main() -> int:
    print("=== D0-CHARGED-LEPTON-SHELL-BRIDGE-001 ===")
    ok = True

    branches = ("electron", "muon", "tau")
    exponents = (Fraction(0), Fraction(1, 4), Fraction(1, 3))
    shells = ("innerD9", "coreD11", "outerD13")
    # Any a>1 has radii (1, (a+1)/2, a); use exact a=2 as deterministic witness.
    a = Fraction(2)
    radii = (Fraction(1), (a + 1) / 2, a)

    if not (exponents[0] < exponents[1] < exponents[2]):
        print(f"  FAIL (A): exponent order not strict: {exponents}")
        ok = False
    else:
        print("  ✓ (A) owned Puiseux order: electron < muon < tau")

    if not (radii[0] < radii[1] < radii[2]):
        print(f"  FAIL (B): radial order not strict: {radii}")
        ok = False
    else:
        print("  ✓ (B) owned radial order: innerD9 < coreD11 < outerD13")

    preserving = []
    for p in permutations(range(3)):
        mapped = [radii[p[i]] for i in range(3)]
        if mapped[0] < mapped[1] < mapped[2]:
            preserving.append(p)
    if preserving != [(0, 1, 2)]:
        print(f"  FAIL (C): order-preserving bridges={preserving}")
        ok = False
    else:
        print("  ✓ (C) unique bridge: electron→inner, muon→core, tau→outer")

    bridge = dict(zip(branches, shells))
    if bridge != {"electron": "innerD9", "muon": "coreD11", "tau": "outerD13"}:
        print(f"  FAIL (D): bridge={bridge}")
        ok = False
    else:
        print("  ✓ (D) exact typed branch→shell naming map")

    print("\n  -- can-fail controls --")
    swapped = (1, 0, 2)
    reversed_p = (2, 1, 0)
    def preserves(p):
        m = [radii[p[i]] for i in range(3)]
        return m[0] < m[1] < m[2]
    if preserves(swapped) or preserves(reversed_p):
        print("  FAIL controls: swapped/reversed branch naming was accepted")
        ok = False
    else:
        print("  ✓ controls: swapped and reversed physical names are rejected")

    print("\n" + ("PASS — charged-lepton structural naming is uniquely order-preserving"
                  if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
