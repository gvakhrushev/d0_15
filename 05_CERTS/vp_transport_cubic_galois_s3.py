#!/usr/bin/env python3
"""D0-TRANSPORT-CUBIC-GALOIS-S3-001 — deterministic symbolic mirror.

The Lean owner proves the full transport-cubic Galois closure without importing
the usual discriminant/Galois parity theorem:

  * enumerate the three roots;
  * construct the oriented Vandermonde delta;
  * prove delta^2 is the genuine polynomial discriminant;
  * show an order-three Galois group acts only by even root permutations;
  * hence delta would be rational and the discriminant a rational square;
  * contradict the exact non-square discriminant 6185264.

This certificate checks the load-bearing cubic arithmetic, the symbolic
Vandermonde identity, all six root permutations, and square/non-square controls.
"""
from __future__ import annotations

import sys
from itertools import permutations
from math import isqrt

import sympy as sp

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def cubic_discr(a3: int, a2: int, a1: int, a0: int) -> int:
    return (
        a2**2 * a1**2
        - 4 * a3 * a1**3
        - 4 * a2**3 * a0
        - 27 * a3**2 * a0**2
        + 18 * a3 * a2 * a1 * a0
    )


def is_square(n: int) -> bool:
    if n < 0:
        return False
    r = isqrt(n)
    return r * r == n


def parity(perm: tuple[int, int, int]) -> int:
    inversions = sum(
        perm[i] > perm[j]
        for i in range(3)
        for j in range(i + 1, 3)
    )
    return -1 if inversions % 2 else 1


def compose(p: tuple[int, int, int], q: tuple[int, int, int]) -> tuple[int, int, int]:
    """Composition p∘q."""
    return tuple(p[q[i]] for i in range(3))


def perm_order(p: tuple[int, int, int]) -> int:
    identity = (0, 1, 2)
    power = identity
    for n in range(1, 7):
        power = compose(p, power)
        if power == identity:
            return n
    raise AssertionError(f"invalid S3 element: {p}")


def has_rational_root_monic_int(coeffs: list[int]) -> bool:
    a0 = coeffs[0]
    if a0 == 0:
        return True
    for d in range(1, abs(a0) + 1):
        if a0 % d:
            continue
        for x in (d, -d):
            if sum(c * x**i for i, c in enumerate(coeffs)) == 0:
                return True
    return False


def main() -> int:
    print("=== D0-TRANSPORT-CUBIC-GALOIS-S3-001 ===")
    ok = True

    disc = cubic_discr(1, 0, -359, -2574)
    irreducible = not has_rational_root_monic_int([-2574, -359, 0, 1])
    if disc != 6185264 or is_square(disc) or not irreducible:
        print(
            f"  FAIL (A): discr={disc}, square={is_square(disc)}, "
            f"irreducible={irreducible}"
        )
        ok = False
    else:
        print("  ✓ (A) irreducible cubic, discr=6185264=2⁴·193·2003 is non-square")

    r0, r1, r2 = sp.symbols("r0 r1 r2")
    s1 = r0 + r1 + r2
    s2 = r0 * r1 + r0 * r2 + r1 * r2
    s3 = r0 * r1 * r2
    delta = (r1 - r0) * (r2 - r0) * (r2 - r1)
    discr_symmetric = (
        s1**2 * s2**2
        - 4 * s2**3
        - 4 * s1**3 * s3
        - 27 * s3**2
        + 18 * s1 * s2 * s3
    )
    symbolic_ok = sp.expand(delta**2 - discr_symmetric) == 0
    specialized = -4 * (-359) ** 3 - 27 * 2574**2
    if not symbolic_ok or specialized != 6185264:
        print(
            f"  FAIL (B): Vandermonde identity={symbolic_ok}, "
            f"specialized={specialized}"
        )
        ok = False
    else:
        print("  ✓ (B) symbolic Vandermonde² identity specializes exactly to 6185264")

    perms = list(permutations(range(3)))
    action_ok = True
    for p in perms:
        transformed = delta.xreplace({r0: (r0, r1, r2)[p[0]],
                                      r1: (r0, r1, r2)[p[1]],
                                      r2: (r0, r1, r2)[p[2]]})
        if sp.expand(transformed - parity(p) * delta) != 0:
            action_ok = False
            break
    exponent_three = [p for p in perms if 3 % perm_order(p) == 0]
    parity_obstruction = (
        len(perms) == 6
        and len(exponent_three) == 3
        and all(parity(p) == 1 for p in exponent_three)
        and all(perm_order(p) == 2 for p in perms if parity(p) == -1)
    )
    if not action_ok or not parity_obstruction:
        print(
            f"  FAIL (C): sign action={action_ok}, "
            f"exponent-three subgroup={exponent_three}"
        )
        ok = False
    else:
        print("  ✓ (C) all 6 permutations: σ(δ)=sign(σ)δ; order-dividing-3 part is A₃")

    # Can-fail controls: the classical square-discriminant A3 cubic and a
    # reducible cubic must not be classified with the target.
    disc_a3 = cubic_discr(1, 0, -3, -1)
    reducible_control = has_rational_root_monic_int([0, -1, 0, 1])
    if disc_a3 != 81 or not is_square(disc_a3) or not reducible_control:
        print(
            f"  FAIL controls: A3 discr={disc_a3}, "
            f"square={is_square(disc_a3)}, reducible={reducible_control}"
        )
        ok = False
    else:
        print("  ✓ controls: x³−3x−1 has square discr 81; x³−x is reducible")

    if ok:
        print("\nPASS — transport cubic has the S₃ parity signature (order 6)")
        return 0
    print("\nFAIL")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
