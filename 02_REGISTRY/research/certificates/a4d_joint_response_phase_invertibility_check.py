#!/usr/bin/env python3
"""The inverse character is defined at every root of unity.

The joint symbol evaluates the connection block at the table phase zeta and
the metric block at chi = zeta^{-1}.  On a cyclic L-grid each component is
an L-th root of unity.  Every such root is invertible, and the inverse is
the grid point whose exponent is the additive inverse.

gcd(k, L) = 1 counts primitive L-th roots.  It does not decide invertibility.
In particular the components 1 and -1 are invertible, and both certified
defect characters are fixed by the reciprocal.  The earlier terminal
INVERSE-CHARACTER-DOMAIN-IS-THE-UNIT-SUBGRID is retracted: that reading
excluded the defect characters themselves.
"""
from __future__ import annotations

import importlib.util
import math
from pathlib import Path

import sympy as sp

NF_PATH = Path(__file__).resolve().parent / "a4d_joint_response_nf_l4_check.py"
LENGTHS = (4, 6, 8, 9, 10, 12, 15, 16)
DEFECTS = {
    "shear": (-1, 1, -1, 1),
    "chain": (-1, 1, 1, -1),
}


def check(name: str, condition: bool, detail: str = "") -> None:
    if not condition:
        raise AssertionError(name + ((" :: " + detail) if detail else ""))
    print("PASS_" + name, flush=True)


def load_nf():
    spec = importlib.util.spec_from_file_location("nf_l4", str(NF_PATH))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def root(length: int, exponent: int):
    value = sp.expand(sp.simplify(
        sp.exp(2 * sp.pi * sp.I * sp.Rational(exponent, length))
    ))
    if value.has(sp.Float):
        raise AssertionError(f"float root L={length} k={exponent}: {value}")
    return value


def main() -> None:
    nf = load_nf()
    for length in LENGTHS:
        primitive = [k for k in range(length) if math.gcd(k, length) == 1]
        check(
            f"L{length}_PRIMITIVE_COUNT",
            len(primitive) == int(sp.totient(length)),
            str(primitive),
        )
        # Exponent 0 is the phase 1.  It is never primitive for L > 1, and
        # it is invertible.
        check(f"L{length}_ZERO_IS_NOT_PRIMITIVE", math.gcd(0, length) != 1)
        nonprimitive_inverted = 0
        for exponent in range(length):
            zeta = root(length, exponent)
            inverse = nf.inverse_character((zeta,))[0]
            inverse = sp.expand(sp.simplify(inverse))
            expected = root(length, (-exponent) % length)
            check(
                f"L{length}_K{exponent}_INVERTS_ON_THE_GRID",
                sp.expand(zeta * inverse - 1) == 0
                and sp.expand(inverse - expected) == 0,
            )
            if math.gcd(exponent, length) != 1:
                nonprimitive_inverted += 1
        check(
            f"L{length}_NONPRIMITIVE_ROOTS_STILL_INVERT",
            nonprimitive_inverted == length - len(primitive),
        )

    for name, phase in DEFECTS.items():
        exact = tuple(sp.Integer(component) for component in phase)
        inverse = tuple(sp.expand(item) for item in nf.inverse_character(exact))
        check(f"{name.upper()}_DEFECT_IS_ITS_OWN_INVERSE", inverse == exact)
        for length in (4, 8, 16):
            exponents = tuple(0 if component == 1 else length // 2 for component in phase)
            check(
                f"{name.upper()}_L{length}_DEFECT_NOT_PRIMITIVE",
                all(math.gcd(exponent, length) != 1 for exponent in exponents),
                str(exponents),
            )

    print()
    print("RESULT: chi = zeta^{-1} is defined at every L-th root of unity")
    print("  on the checked grids.  The inverse is the grid point with the")
    print("  opposite exponent.  gcd(k, L) = 1 selects primitive roots and")
    print("  rejects both defect characters, which are invertible.")
    print("RETRACTED: INVERSE-CHARACTER-DOMAIN-IS-THE-UNIT-SUBGRID")
    print("BOUNDARY: characters outside a finite root-of-unity grid remain")
    print("  inside the domain of the reciprocal.  This certificate does not")
    print("  restore (NF) and does not claim a response NOGO.")


if __name__ == "__main__":
    main()
