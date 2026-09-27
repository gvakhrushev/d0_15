#!/usr/bin/env python3
"""The reciprocal character is defined on every root of unity of a cyclic grid.

A previous draft of this certificate claimed that chi = zeta^{-1} requires
gcd(k, L) = 1, and used that to declare the non-primitive rows of the L = 4,
L = 8 and L = 16 censuses a convention gap.  That reading was wrong and is
withdrawn.

On a cyclic L-grid the component is zeta = omega^{k} with omega^{L} = 1, so

    zeta^{-1} = omega^{-k},

the grid point of exponent (-k) mod L.  This holds for EVERY exponent, including
non-primitive ones.  The count phi(L) counts primitive L-th roots; it does not
decide invertibility.  The phases 1 (exponent 0) and -1 (exponent L/2 for even
L) are invertible.

This matters concretely: both NF defect characters are fixed by the reciprocal,

    (-1, 1, -1, 1)^{-1} = (-1, 1, -1, 1)
    (-1, 1,  1, -1)^{-1} = (-1, 1,  1, -1),

and on L in {4, 8, 16} every exponent of either character fails gcd(k, L) = 1.
The withdrawn reading would have placed the certified counterexamples to (NF)
outside the domain of the convention, which is exactly the error avoided here.

What this certificate does establish: the inverse-character convention is
defined on the whole cyclic grid for every L tested, so characters that are not
L-th roots remain a genuine open part of the moment census rather than a
convention gap.  It does not restore (NF) and does not change any moment.
"""
from __future__ import annotations

from sympy import I, N, exp, expand_complex, nsimplify, pi, simplify

LENGTHS = (2, 3, 4, 6, 8, 9, 10, 12, 15, 16)
DEFECTS = ((-1, 1, -1, 1), (-1, 1, 1, -1))


def check(name: str, condition: bool, detail: str = "") -> None:
    if not condition:
        raise AssertionError(name + ((" :: " + detail) if detail else ""))
    print("PASS_" + name, flush=True)


def grid(L: int):
    w = exp(2 * pi * I / L)
    return [nsimplify(expand_complex(w ** k)) for k in range(L)]


def main() -> None:
    print("  L   all exponents have a grid reciprocal   defect characters fixed")
    for L in LENGTHS:
        g = grid(L)
        ok_all = True
        for k in range(L):
            # Compare numerically: the reciprocal and the negative-exponent
            # grid point are the same complex number, but sympy may print one
            # as exp(-I*t) and the other as cos(t) + I*sin(t).
            got = complex(N(1 / g[k]))
            want = complex(N(g[(-k) % L]))
            if abs(got - want) > 1e-12:
                ok_all = False
        check(f"L_{L}_EVERY_EXPONENT_HAS_RECIPROCAL", ok_all)
        fixed = []
        for d in DEFECTS:
            exps = [L // 2 if v < 0 else 0 for v in d]
            inv_exps = [(-e) % L for e in exps]
            fixed.append("yes" if inv_exps == exps else "no")
        print(f"  {L:<3} {str(ok_all):<35} {fixed}", flush=True)

    # The concrete cases that the withdrawn reading would have excluded.
    for L in (4, 8, 16):
        g = grid(L)
        for d in DEFECTS:
            dd = tuple(complex(N(v)) for v in d)
            on_grid = all(any(abs(complex(N(x)) - c) < 1e-12 for x in g)
                          for c in dd)
            if not on_grid:
                continue
            inv = tuple(complex(N(1 / x)) for x in dd)
            same = all(abs(a - b) < 1e-12 for a, b in zip(inv, dd))
            check(f"L_{L}_DEFECT_ON_GRID_AND_FIXED", same,
                  f"{dd} -> {inv}")

    print()
    print("RESULT: zeta^{-1} = omega^{-k} is the grid point of exponent")
    print("  (-k) mod L, for every k.  No exponent is excluded.  phi(L)")
    print("  counts primitive roots and does not decide invertibility.")
    print()
    print("CONSEQUENCE: the earlier 'convention gap' reading is withdrawn.  The")
    print("  non-primitive rows of the L=4, L=8 and L=16 censuses are inside")
    print("  the domain after all, and both certified NF defect characters sit")
    print("  there.  Characters that are not L-th roots are therefore a genuine")
    print("  open part of the moment census, not a defect of the convention.")
    print("TERMINAL: RECIPROCAL-DEFINED-ON-THE-WHOLE-CYCLIC-GRID")
    print("BOUNDARY: a statement about the inverse-character convention and")
    print("  the cyclic grid.  It does not restore (NF) and changes no moment.")


if __name__ == "__main__":
    main()
