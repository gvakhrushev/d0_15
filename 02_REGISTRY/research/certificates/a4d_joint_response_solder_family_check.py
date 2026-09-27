#!/usr/bin/env python3
"""Finite solder family for L=4 response moments, plus the second defect.

The family is fixed below. On it, the only characters with a nonzero
response moment are the upper shear at z=(-1,1,-1,1) and the chain
I+E_01+E_13 at z=(-1,1,1,-1). Both moments are
(0,0,0,0,-2,0,0,0,0,0).

For the chain, the period-2 quadratic connection source has a unique
constant solution, and the cell metric jet stays -16 on q_11. Vacuum
therefore cuts that amplitude at order u^2. This is not a response NOGO.
"""
from __future__ import annotations

import importlib.util
from itertools import product
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
support_spec = importlib.util.spec_from_file_location(
    "support", HERE / "a4d_joint_response_shear_l4_support_check.py"
)
support = importlib.util.module_from_spec(support_spec)
support_spec.loader.exec_module(support)
nf = support.nf

reduction_spec = importlib.util.spec_from_file_location(
    "reduction", HERE / "a4d_joint_response_shear_reduction_check.py"
)
reduction = importlib.util.module_from_spec(reduction_spec)
reduction_spec.loader.exec_module(reduction)

ROOTS = support.ROOTS
UPPER_WITNESS = support.WITNESS
CHAIN_WITNESS = sp.Matrix([
    0, 0, 0, 0, 0, 1,
    0, 0, 0, 0, 0, 0,
    -2, 0, -1, 0, -1, 0,
    0, 1, 0, 1, 0, 1,
])
CHAIN_SOURCE = [
    0, 16, 24, -16, -24, 0,
    -8, -24, 0, -8, 16, 16,
    0, 0, 0, 0, 0, 0,
    0, -16, -24, 16, 24, 0,
]
CHAIN_ZETA = sp.sympify(
    "[-1/2, 1/2, 1/2, 1/2, 1/2, 0, 0, 0, 0, 0, 0, 0,"
    " -2, 1, -1, 1, -1, 2, -1/2, -1/2, -1, -1/2, -1, 0]"
)
METRIC_POINT = [0, 0, 0, 0, -16, 0, 0, 0, 0, 0]
MOMENT = [0, 0, 0, 0, -2, 0, 0, 0, 0, 0]


def check(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name, flush=True)


def eye_plus(*pairs):
    matrix = sp.eye(4)
    for i, j in pairs:
        matrix[i, j] += 1
    return matrix


def phase_of(*values):
    converted = []
    for value in values:
        if value == "I":
            converted.append(sp.I)
        elif value == "-I":
            converted.append(-sp.I)
        else:
            converted.append(sp.Integer(value))
    return tuple(converted)


FAMILY = [
    ("UPPER_SHEAR", eye_plus((0, 1), (1, 2)), 3),
    ("PURE_01", eye_plus((0, 1)), 14),
    ("PURE_02", eye_plus((0, 2)), 14),
    ("PURE_03", eye_plus((0, 3)), 14),
    ("PURE_12", eye_plus((1, 2)), 6),
    ("PURE_13", eye_plus((1, 3)), 6),
    ("PURE_23", eye_plus((2, 3)), 6),
    ("CHAIN_12_23", eye_plus((1, 2), (2, 3)), 4),
    ("CHAIN_01_13", eye_plus((0, 1), (1, 3)), 3),
    ("DIAG_2357", sp.diag(2, 3, 5, 7), 2),
    ("CURVED_RATIONAL", sp.Matrix([[2, 1, 0, 1], [0, 1, 1, 0], [1, 0, 1, 0], [0, 0, 0, 1]]), 2),
]
DEFECTS = {
    ("UPPER_SHEAR", phase_of(-1, 1, -1, 1)): UPPER_WITNESS,
    ("CHAIN_01_13", phase_of(-1, 1, 1, -1)): CHAIN_WITNESS,
}


def moments_of(solder, phase, vector):
    gram = solder.T * nf.ETA * solder
    values = []
    for q in nf.Q_DIRECTIONS:
        lift = solder * gram.inv() * q / 2
        derivative = (
            nf.connection_symbol(solder + lift, list(phase))
            - nf.connection_symbol(solder - lift, list(phase))
        ) / 2
        values.append(sp.simplify((sp.conjugate(vector).T * derivative * vector)[0]))
    return values


def block_is_zero(solder, phase, basis):
    gram = solder.T * nf.ETA * solder
    for q in nf.Q_DIRECTIONS:
        lift = solder * gram.inv() * q / 2
        derivative = (
            nf.connection_symbol(solder + lift, list(phase))
            - nf.connection_symbol(solder - lift, list(phase))
        ) / 2
        block = sp.simplify(sp.conjugate(basis).T * derivative * basis)
        if block != sp.zeros(basis.cols):
            return False
    return True


def screen():
    seen = []
    for name, solder, expected_count in FAMILY:
        gram = solder.T * nf.ETA * solder
        check(f"{name}_NONDEGENERATE", sp.factor(solder.det()) != 0 and sp.factor(gram.det()) != 0)
        stored = support.brackets(solder)
        units = support.metric_units(solder)
        singular = []
        for phase in product(ROOTS, repeat=4):
            joint = support.connection(stored, phase).col_join(
                support.metric(units, [1 / z for z in phase])
            ).applyfunc(sp.expand)
            rank = nf.exact_rank(joint)
            if rank < 24:
                basis = nf.exact_nullspace(joint)
                singular.append((phase, rank, basis))
        check(f"{name}_SINGULAR_COUNT_{expected_count}", len(singular) == expected_count)
        for phase, _rank, basis in singular:
            key = (name, tuple(phase))
            if key in DEFECTS:
                witness = support.primitive_column(basis)
                check(f"{name}_WITNESS", witness == DEFECTS[key])
                check(f"{name}_MOMENT", moments_of(solder, phase, witness) == MOMENT)
                seen.append(key)
            else:
                check(f"{name}_MOMENT_ZERO_{phase}", block_is_zero(solder, phase, basis))
    check("EXACTLY_TWO_DEFECTS", seen == list(DEFECTS))


def chain_quadratic():
    solder = eye_plus((0, 1), (1, 3))
    roles = []
    for role in range(4):
        matrix = reduction.Z4 * 0
        for j, generator in enumerate(reduction.GENERATORS):
            matrix += CHAIN_WITNESS[6 * role + j] * generator
        roles.append(matrix)
    reduction.SHEAR = solder
    reduction.ROLES = roles

    def sigma(site):
        return 1 if (site[0] + site[3]) % 2 == 0 else -1

    reduction.sigma = sigma
    pure = reduction.euler_jets([sp.Integer(0)] * 24)
    check(
        "CHAIN_LINEAR_EULER_VANISHES",
        all(sp.expand(row[0]) == 0 and sp.expand(row[1]) == 0 for row in pure),
    )
    source = [sp.expand(row[2]) for row in pure]
    check("CHAIN_QUADRATIC_SOURCE", source == [sp.Integer(x) for x in CHAIN_SOURCE])
    check("CHAIN_PURE_METRIC", reduction.metric_u2([sp.Integer(0)] * 24) == METRIC_POINT)
    columns = []
    for index in range(24):
        direction = [sp.Integer(0)] * 24
        direction[index] = sp.Integer(1)
        rows = reduction.euler_jets(direction)
        columns.append([sp.expand(rows[i][2] - source[i]) for i in range(24)])
    check("CHAIN_EVEN_RANK_24", sp.Matrix(columns).rank() == 24)
    solved = reduction.euler_jets(list(CHAIN_ZETA))
    check("CHAIN_ZETA_KILLS_EULER", all(sp.expand(row[2]) == 0 for row in solved))
    check("CHAIN_REDUCED_METRIC", reduction.metric_u2(list(CHAIN_ZETA)) == METRIC_POINT)


def main():
    screen()
    chain_quadratic()
    print("RESULT_FAMILY: two NF defects, both with moment -2 on q_11")
    print("RESULT_CHAIN: order-u^2 metric jet stays -16 on q_11, so vacuum forces u=0")
    print("BOUNDARY: this finite family only; the chain cut is quadratic, not a response NOGO")


if __name__ == "__main__":
    main()
