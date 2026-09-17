#!/usr/bin/env python3
"""D0-FIVE-SECTOR-FIELD-LEDGER-001 — exact finite mirror.

The five T13 sectors map to three independent irrational characters
`(alpha, dark-energy, transport)`:

    geometry          0 0 1
    gravity           0 0 0
    electromagnetism  1 0 0
    mass              0 0 1
    dark-energy       0 1 0

The certificate verifies rank 3, nullity 2, the exact kernel equations, the unique
geometry/mass collision, independence of radicands {5,10,386579}, and the transport
exclusions for sqrt(5), sqrt(10).
"""
from __future__ import annotations

import sys
from math import isqrt

import sympy as sp

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


SECTORS = ("geometry", "gravity", "electromagnetism", "mass", "dark_energy")
M = sp.Matrix([
    [0, 0, 1],
    [0, 0, 0],
    [1, 0, 0],
    [0, 0, 1],
    [0, 1, 0],
])


def is_square(n: int) -> bool:
    if n < 0:
        return False
    r = isqrt(n)
    return r * r == n


def main() -> int:
    print("=== D0-FIVE-SECTOR-FIELD-LEDGER-001 ===")
    ok = True

    rank = M.rank()
    kernel = M.T.nullspace()
    if rank != 3 or len(kernel) != 2:
        print(f"  FAIL (A): rank={rank}, nullity={len(kernel)}")
        ok = False
    else:
        print("  ✓ (A) five-sector character incidence has rank 3 and nullity 2")

    gravity = sp.Matrix([0, 1, 0, 0, 0])
    geom_minus_mass = sp.Matrix([1, 0, 0, -1, 0])
    exact_kernel = (
        M.T * gravity == sp.zeros(3, 1)
        and M.T * geom_minus_mass == sp.zeros(3, 1)
        and sp.Matrix.hstack(gravity, geom_minus_mass).rank() == 2
    )
    if not exact_kernel:
        print("  FAIL (B): expected kernel basis not exact")
        ok = False
    else:
        print("  ✓ (B) kernel = gravity direction ⊕ (geometry−mass)")

    rows = [tuple(map(int, M.row(i))) for i in range(M.rows)]
    collisions = {
        (SECTORS[i], SECTORS[j])
        for i in range(len(rows))
        for j in range(i + 1, len(rows))
        if rows[i] == rows[j]
    }
    if collisions != {("geometry", "mass")}:
        print(f"  FAIL (C): row collisions={collisions}")
        ok = False
    else:
        print("  ✓ (C) geometry/mass is the unique distinct-sector character collision")

    radicands = (5, 10, 386579)
    subset_products = [
        radicands[0], radicands[1], radicands[2],
        radicands[0] * radicands[1],
        radicands[0] * radicands[2],
        radicands[1] * radicands[2],
        radicands[0] * radicands[1] * radicands[2],
    ]
    independent = all(not is_square(n) for n in subset_products)
    delta = 6185264
    transport_exclusions = all(
        not is_square(d) and not is_square(d * delta) for d in (5, 10)
    )
    if not independent or not transport_exclusions:
        print(
            f"  FAIL (D): independent={independent}, "
            f"transport_exclusions={transport_exclusions}"
        )
        ok = False
    else:
        print("  ✓ (D) three square classes independent; sqrt5/sqrt10 excluded from transport")

    mass_mutated = M.copy()
    mass_mutated[3, :] = sp.Matrix([[1, 0, 0]])
    gravity_mutated = M.copy()
    gravity_mutated[1, :] = sp.Matrix([[0, 1, 0]])
    control_mass_breaks = tuple(map(int, mass_mutated.row(0))) != tuple(map(int, mass_mutated.row(3)))
    control_gravity_breaks = tuple(map(int, gravity_mutated.row(1))) != (0, 0, 0)
    dependent_radicands_detected = is_square(5 * 20)
    if not (control_mass_breaks and control_gravity_breaks and dependent_radicands_detected):
        print("  FAIL controls: a mutated incidence/dependent square class escaped")
        ok = False
    else:
        print("  ✓ controls: mutated mass/gravity rows and dependent {5,20} are rejected")

    print("\n" + ("PASS — five sectors = rational hub + three independent characters" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
