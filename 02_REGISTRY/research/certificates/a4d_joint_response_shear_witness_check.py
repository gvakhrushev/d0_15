#!/usr/bin/env python3
"""Exact shear witness for the joint-response microstructure task.

Reproduces, from the #216/#234 symbol convention already used by
a4d_joint_response_nf_l4_check.py:

    z = (-1, 1, -1, 1)
    dim ker H_Q(z) ∩ ker C_Q(z) = 1
    v* D_Q H_Q(z)[q_11] v = -2

on the upper-triangular shear solder.  q_11 is the symmetric Gram slot
(1,1) in the ten-component order (00,01,02,03,11,12,13,22,23,33).

This is a finite algebraic failure of the frozen moment identity (NF).
It does not by itself produce a joint-critical smooth-background NOGO.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import sympy as sp


def load_owner():
    path = Path(__file__).resolve().parent / "a4d_joint_response_nf_l4_check.py"
    spec = importlib.util.spec_from_file_location("nf_l4_owner", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


nf = load_owner()


def check(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name, flush=True)


def primitive_column(basis: sp.Matrix) -> sp.Matrix:
    raw = [sp.Integer(sp.together(entry)) for entry in basis[:, 0]]
    content = 0
    for entry in raw:
        content = sp.igcd(content, abs(int(entry)))
    vector = sp.Matrix([entry // content for entry in raw])
    if vector[5] < 0:
        vector = -vector
    return vector


SHEAR = sp.Matrix([
    [1, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1],
])
CHARACTER = (sp.Integer(-1), sp.Integer(1), sp.Integer(-1), sp.Integer(1))
Q_SLOTS = [(i, j) for i in range(4) for j in range(i, 4)]
# Generator order K1, K2, K3, J12, J13, J23.  Role blocks of six.
WITNESS = sp.Matrix([
    0, 0, 0, 0, 0, 1,
    0, 0, 0, 0, 0, 0,
    0, 0, -1, 0, -1, 1,
    2, 1, 0, 1, 0, 0,
])


def moments(solder: sp.Matrix, vector: sp.Matrix) -> list[sp.Expr]:
    gram = solder.T * nf.ETA * solder
    values = []
    for q in nf.Q_DIRECTIONS:
        lift = solder * gram.inv() * q / 2
        derivative = (
            nf.connection_symbol(solder + lift, list(CHARACTER))
            - nf.connection_symbol(solder - lift, list(CHARACTER))
        ) / 2
        values.append(sp.simplify((sp.conjugate(vector).T * derivative * vector)[0]))
    return values


def main() -> None:
    gram = sp.factor(SHEAR.T * nf.ETA * SHEAR)
    check("SHEAR_DET_ONE", sp.factor(SHEAR.det()) == 1)
    check("SHEAR_GRAM_NONDEGENERATE", sp.factor(gram.det()) != 0)
    check("CHARACTER_REAL_AND_SELF_INVERSE", nf.inverse_character(CHARACTER) == list(CHARACTER))
    check("CHARACTER_SQUARE_IS_ZERO_FREQUENCY", tuple(z**2 for z in CHARACTER) == (1, 1, 1, 1))

    # Narrow convention check against the literal #216 matrices.  Not a census.
    owner_sub = dict(zip(nf.z_owner, CHARACTER))
    h_flat, c_flat = nf.joint_symbols(sp.eye(4), CHARACTER)
    check(
        "FLAT_H_MATCHES_216_AT_CHARACTER",
        (h_flat - nf.connection_owner.subs(owner_sub)).applyfunc(sp.simplify) == sp.zeros(24),
    )
    check(
        "FLAT_C_MATCHES_216_AT_CHARACTER",
        (c_flat - nf.metric_owner.subs(owner_sub).T).applyfunc(sp.simplify) == sp.zeros(10, 24),
    )
    check("FLAT_JOINT_RANK_FULL", nf.exact_rank(h_flat.col_join(c_flat)) == 24)

    h, c = nf.joint_symbols(SHEAR, CHARACTER)
    check("SHEAR_H_RANK_20", nf.exact_rank(h) == 20)
    check("SHEAR_C_RANK_9", nf.exact_rank(c) == 9)
    joint = h.col_join(c)
    check("SHEAR_JOINT_RANK_23", nf.exact_rank(joint) == 23)
    basis = nf.exact_nullspace(joint)
    check("SHEAR_JOINT_NULLITY_ONE", basis.cols == 1)
    check("COMPUTED_WITNESS_MATCHES_RECORDED", primitive_column(basis) == WITNESS)
    check("WITNESS_IN_JOINT_KERNEL", (joint * WITNESS).applyfunc(sp.simplify) == sp.zeros(34, 1))
    check("WITNESS_CONTENT_ONE", sp.igcd(*[abs(int(entry)) for entry in WITNESS]) == 1)

    response = moments(SHEAR, WITNESS)
    expected = [0, 0, 0, 0, -2, 0, 0, 0, 0, 0]
    check("FULL_TEN_COMPONENT_RESPONSE", response == expected)
    q11_index = Q_SLOTS.index((1, 1))
    check("Q11_MOMENT_MINUS_TWO", response[q11_index] == -2)

    # Sign flip does not change a quadratic moment; the opposite primitive
    # vector is the only other content-one integer generator.
    check("SIGN_FLIP_SAME_MOMENT", moments(SHEAR, -WITNESS)[q11_index] == -2)

    print("RESULT_SOLDER: upper shear E=I+E_01+E_12")
    print("RESULT_CHARACTER: (-1,1,-1,1), table phase equals physical phase")
    print("RESULT_RANKS: H=20, C=9, joint=23, nullity=1")
    print("RESULT_WITNESS:", list(WITNESS))
    print("RESULT_TEN_MOMENTS:", response)
    print("RESULT_Q11: -2")
    print("BOUNDARY: finite shear counterexample to (NF); not a joint-critical NOGO.")


if __name__ == "__main__":
    main()
