#!/usr/bin/env python3
"""Quadratic reduced action of the shear witness, from one symbol.

Phi(u, Q) = (1/2) u^2 v* H(Q) v on the upper-shear carrier at
z=(-1, 1, -1, 1).  Both Euler slots are derivatives of this Phi.
The moving-germ line q0=d d^T has zero q_11 entry at this character,
so frequency absorption does not travel in the stress direction.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

import sympy as sp


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


SHEAR = sp.Matrix([
    [1, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1],
])
PHASE = [sp.Integer(-1), sp.Integer(1), sp.Integer(-1), sp.Integer(1)]
WITNESS = sp.Matrix([
    0, 0, 0, 0, 0, 1,
    0, 0, 0, 0, 0, 0,
    0, 0, -1, 0, -1, 1,
    2, 1, 0, 1, 0, 0,
])
QPAIRS = [(i, j) for i in range(4) for j in range(i, 4)]


def moment(q_matrix):
    gram = SHEAR.T * nf.ETA * SHEAR
    lift = SHEAR * gram.inv() * q_matrix / 2
    derivative = (
        nf.connection_symbol(SHEAR + lift, PHASE)
        - nf.connection_symbol(SHEAR - lift, PHASE)
    ) / 2
    return sp.expand((WITNESS.T * derivative * WITNESS)[0])


def main():
    d = sp.Matrix([1 / t - 1 for t in PHASE])
    q0 = sp.expand(d * d.T)
    check("GERM_Q11_SLOT_VANISHES", q0[1, 1] == 0)
    slots = [sp.expand(q0[a, b]) for a, b in QPAIRS]
    check(
        "GERM_SUPPORT_IS_00_02_22",
        slots == [4, 0, 4, 0, 0, 0, 0, 4, 0, 0],
    )
    h = nf.connection_symbol(SHEAR, PHASE)
    check("WITNESS_IN_CONNECTION_KERNEL", sp.expand(h * WITNESS) == sp.zeros(24, 1))
    q11 = sp.zeros(4)
    q11[1, 1] = 1
    check("Q11_STRESS_IS_MINUS_TWO", moment(q11) == -2)
    check("GERM_DIRECTION_STRESS_IS_ZERO", moment(q0) == 0)
    u = sp.symbols("u")
    quadratic = sp.expand((WITNESS.T * h * WITNESS)[0])
    phi = sp.Rational(1, 2) * u**2 * quadratic
    # Both slots are derivatives of this one quadratic action.
    check("CONNECTION_SLOT_VANISHES_FOR_EVERY_U", sp.diff(phi, u) == 0)
    metric_slot = sp.Rational(1, 2) * u**2 * moment(q11)
    check("METRIC_SLOT_IS_MINUS_U_SQUARED", sp.expand(metric_slot + u**2) == 0)
    print("RESULT_REDUCED_QUADRATIC: partial_u Phi=0 and partial_q11 Phi=-u^2")
    print("RESULT_GERM_MISALIGNED: q0 has no q_11 entry and zero witness stress")
    print("BOUNDARY: frozen shear mode; modulation and the order-u^5 jet stay open")


if __name__ == "__main__":
    main()
