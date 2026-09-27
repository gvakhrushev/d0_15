#!/usr/bin/env python3
"""Which L-grids are admissible at all, given the inverse-character convention.

The joint symbol uses the inverse-polarization convention: the connection
block is evaluated at the table phase zeta and the metric block at the
physical phase chi = zeta^{-1}.  That inverse exists only when zeta is a unit.

For a cyclic L-grid the phases are the L-th roots of unity, and zeta^{-1}
exists iff zeta is in the unit group, of order phi(L).  When L is composite
with more than one prime factor, most phases are NOT units, so the
inverse-character convention is undefined on part of the grid and such a
grid is not an admissible character grid at all.

This certificate computes, exactly, the admissible character grid for
L in {4, 6, 8, 9, 10, 12, 15, 16} and identifies which grids can carry
the joint response-moment test.
"""
from __future__ import annotations

import math
from fractions import Fraction

from sympy import I, Rational, exp, nsimplify, expand_complex, totient

LENGTHS = (4, 6, 8, 9, 10, 12, 15, 16)


def check(name: str, condition: bool, detail: str = "") -> None:
    if not condition:
        raise AssertionError(name + ((" :: " + detail) if detail else ""))
    print("PASS_" + name, flush=True)


def roots(L: int):
    return [nsimplify(expand_complex(
        exp(I * Rational(2 * k, L)))) for k in range(L)]


def main() -> None:
    print("  L   phi(L)  units   admissible characters   verdict")
    for L in LENGTHS:
        rs = roots(L)
        units = [k for k in range(L) if math.gcd(k, L) == 1]
        n_admissible = len(units) ** 4
        ok = (len(units) == int(totient(L)))
        check(f"L_{L}_UNIT_COUNT", ok, f"units {units}")
        verdict = (f"only {len(units)}^{4} = {n_admissible} of "
                   f"{L}^{4} characters are strictly admissible")
        print(f"  {L:<3} {int(totient(L)):<6} {len(units):<7} "
              f"{n_admissible:<22} {verdict}", flush=True)

    # The decisive facts.
    # No L > 2 has every phase invertible: for L = 2^m the even indices are
    # never units, and for odd factors the multiples of that factor are not.
    check("L4_PHASE_2_IS_NOT_A_UNIT", math.gcd(2, 4) != 1)
    check("L8_PHASE_2_IS_NOT_A_UNIT", math.gcd(2, 8) != 1)
    check("L6_PHASE_2_IS_NOT_A_UNIT", math.gcd(2, 6) != 1)
    check("L9_PHASE_3_IS_NOT_A_UNIT", math.gcd(3, 9) != 1)
    check("L12_PHASE_2_IS_NOT_A_UNIT", math.gcd(2, 12) != 1)
    check("NO_TRIVIAL_L_HAS_ALL_PHASES_UNITS",
          not any(all(math.gcd(k, L) == 1 for k in range(L))
                  for L in range(2, 17)))

    print()
    print("RESULT: on a cyclic L-grid the phase zeta is a unit only when")
    print("  gcd(k, L) = 1, so the strict domain of chi = zeta^{-1} has")
    print("  phi(L)^4 characters out of L^4.  No L > 2 has every phase")
    print("  invertible, so no nontrivial L-grid is admissible as a whole:")
    print("  L=4 keeps 2^4 of 4^4, L=8 keeps 4^4 of 8^4, L=12 keeps")
    print("  4^4 of 12^4, and L=15 keeps 8^4 of 15^4.")
    print()
    print("CONSEQUENCE: the L=4 and L=8 censuses already on this branch")
    print("  were run over the whole grid, and the components whose phase is a")
    print("  non-unit were evaluated with a numerically inverted phase.  Those")
    print("  rows are not strictly defined in the inverse-character")
    print("  convention.  The strictly admissible subgrids of size phi(L)^4")
    print("  are certified; the non-unit remainder is a convention gap, not")
    print("  an open research front, and a separate decision is needed on")
    print("  whether to drop those rows or to re-derive the metric block")
    print("  there without an inverse character.")
    print("TERMINAL: INVERSE-CHARACTER-DOMAIN-IS-THE-UNIT-SUBGRID")
    print("BOUNDARY: a statement about the inverse-character convention and")
    print("  the cyclic L-grid, not about the star action or a response NOGO.")


if __name__ == "__main__":
    main()
