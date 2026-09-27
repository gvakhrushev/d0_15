#!/usr/bin/env python3
"""Shear witness along the phase line z=(-1, t, -1, 1).

The quadratic form and the metric block on the witness vanish for every t.
The symmetric connection Euler vanishes only at t=1, to order (t-1)^2.
The joint symbol has rank 24 over the rational functions of t.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

import sympy as sp
from sympy import QQ
from sympy.polys.matrices import DomainMatrix


def load_nf():
    path = Path(__file__).resolve().parent / "a4d_joint_response_nf_l4_check.py"
    spec = importlib.util.spec_from_file_location("nf_l4_owner", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


nf = load_nf()


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name, flush=True)


SHEAR = sp.Matrix([[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
WITNESS = sp.Matrix([
    0, 0, 0, 0, 0, 1,
    0, 0, 0, 0, 0, 0,
    0, 0, -1, 0, -1, 1,
    2, 1, 0, 1, 0, 0,
])


def numerator(entry):
    return sp.factor(sp.fraction(sp.together(entry))[0])


def main():
    t = sp.symbols("t")
    phase = [sp.Integer(-1), t, sp.Integer(-1), sp.Integer(1)]
    symbol = nf.connection_symbol(SHEAR, phase)
    form = sp.together((WITNESS.T * symbol * WITNESS)[0])
    check("QUADRATIC_FORM_IDENTICALLY_ZERO", sp.expand(form) == 0)
    physical = [1 / entry for entry in phase]
    metric = sp.Matrix.vstack(*[
        nf.metric_symbol(SHEAR, physical, q) for q in nf.Q_DIRECTIONS
    ])
    check("METRIC_BLOCK_ON_WITNESS_IDENTICALLY_ZERO",
          sp.expand(sp.together(metric * WITNESS)) == sp.zeros(10, 1))
    raw = (symbol * WITNESS).applyfunc(sp.together)
    symmetric = ((symbol + symbol.T) * WITNESS).applyfunc(sp.together)
    expected_raw = {
        2: (t - 1) * (t + 1) / (2 * t),
        8: (t - 1) / t,
        10: (t - 1) / t,
        11: (t - 1) / t,
        16: (t - 1) * (t + 1) / (2 * t),
        17: (t - 1) * (t + 1) / (2 * t),
        20: (t - 1) * (t + 1) / (2 * t),
        22: (t - 1) * (t + 1) / (2 * t),
        23: (t - 1) * (t + 1) / (2 * t),
    }
    for index in range(24):
        got = sp.expand(sp.together(raw[index] - expected_raw.get(index, 0)))
        check("RAW_RESIDUAL_%d" % index, got == 0)
    for index, value in ((8, 1), (10, 1), (11, 1)):
        got = sp.expand(sp.together(symmetric[index] + value * (t - 1)**2 / t))
        check("SYMMETRIC_RESIDUAL_%d" % index, got == 0)
    for index in range(24):
        if index not in (8, 10, 11):
            check("SYMMETRIC_RESIDUAL_ZERO_%d" % index, sp.expand(symmetric[index]) == 0)
    common = None
    for index in expected_raw:
        piece = sp.Poly(sp.expand(numerator(raw[index])), t)
        common = piece if common is None else sp.gcd(common, piece)
    check("RAW_GCD_IS_T_MINUS_ONE", sp.expand(common.as_expr() - (t - 1)) == 0)
    check("NOT_A_KERNEL_AT_MINUS_ONE", sp.expand(raw[8].subs(t, -1)) == 2)
    joint = symbol.col_join(metric).applyfunc(sp.together)
    rank = DomainMatrix.from_Matrix(joint).convert_to(QQ.frac_field(t)).rank()
    check("GENERIC_JOINT_RANK_24", rank == 24)
    cleared = (2 * t * symbol).applyfunc(lambda entry: sp.expand(sp.together(entry)))
    determinant = DomainMatrix.from_Matrix(cleared).convert_to(QQ[t]).det()
    determinant = sp.Add(*[
        sp.Integer(int(coefficient)) * t**monomial[0]
        for monomial, coefficient in determinant.to_dict().items()
    ])
    octic = (
        2 * t**8 + 6 * t**7 + 29 * t**6 + 54 * t**5 + 74 * t**4
        + 54 * t**3 + 29 * t**2 + 6 * t + 2
    )
    check(
        "CONNECTION_DETERMINANT",
        sp.expand(determinant - 16777216 * t**18 * (t - 1)**4 * octic) == 0,
    )
    w = sp.symbols("w")
    reciprocal = sp.expand(octic / t**4)
    reduced = (
        2 * (w**4 - 4 * w**2 + 2)
        + 6 * (w**3 - 3 * w)
        + 29 * (w**2 - 2)
        + 54 * w
        + 74
    )
    check(
        "RECIPROCAL_REDUCTION",
        sp.expand(reciprocal - reduced.subs(w, t + 1 / t)) == 0,
    )
    check("RECIPROCAL_QUARTIC_NO_REAL_ROOT", sp.real_roots(sp.Poly(sp.expand(reduced), w)) == [])
    print("RESULT_PHASE_LINE: on the unit circle the witness is stationary only at t=1")
    print("BOUNDARY: this is one phase coordinate of the upper shear, not a variable background")


if __name__ == "__main__":
    main()
