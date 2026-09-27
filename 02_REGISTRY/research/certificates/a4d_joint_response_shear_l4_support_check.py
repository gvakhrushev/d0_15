#!/usr/bin/env python3
"""L=4 joint support on the upper shear solder.

Bracket forms depend only on the solder. All 256 characters are assembled
from that precomputation. Exactly three are jointly singular: the two
diagonal quarter-waves, whose ten moment blocks vanish, and
z=(-1,1,-1,1), whose content-one moment is the committed
(0,0,0,0,-2,0,0,0,0,0). No other character on this solder and grid is an
NF defect.
"""
from __future__ import annotations

import importlib.util
from itertools import combinations, product
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    "nf", HERE / "a4d_joint_response_nf_l4_check.py"
)
nf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(nf)

SHEAR = sp.Matrix([[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
PAIRS = list(nf.PAIRS)
GENERATORS = list(nf.GENERATORS)
ROOTS = (sp.Integer(1), sp.I, sp.Integer(-1), -sp.I)
SHEAR_CHARACTER = (sp.Integer(-1), sp.Integer(1), sp.Integer(-1), sp.Integer(1))
DIAGONAL = (
    (sp.I, sp.I, sp.I, sp.I),
    (-sp.I, -sp.I, -sp.I, -sp.I),
)
WITNESS = sp.Matrix([
    0, 0, 0, 0, 0, 1,
    0, 0, 0, 0, 0, 0,
    0, 0, -1, 0, -1, 1,
    2, 1, 0, 1, 0, 0,
])


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


def brackets(solder):
    stored = []
    for r, s in PAIRS:
        u, v = [i for i in range(4) if i not in (r, s)]
        seq = [r, s, u, v]
        sign = (-1) ** sum(seq[i] > seq[j] for i, j in combinations(range(4), 2))
        pairing = sign * nf.wedge(solder[:, u], solder[:, v]).T * nf.G2 * nf.STAR
        form = []
        for left in GENERATORS:
            row = []
            for right in GENERATORS:
                commutator = (left * right - right * left) * nf.ETA
                coords = sp.Matrix([commutator[a, b] for a, b in PAIRS])
                row.append(sp.together((pairing * coords)[0]))
            form.append(row)
        stored.append((r, s, form))
    return stored


def connection(stored, phase):
    result = sp.zeros(24)
    for r, s, form in stored:
        roles = [r, s, r, s]
        direct = [sp.Integer(1), phase[r], -phase[s], sp.Integer(-1)]
        inverse = [sp.Integer(1), 1 / phase[r], -1 / phase[s], sp.Integer(-1)]
        role = sp.zeros(4)
        for i, j in combinations(range(4), 2):
            role[roles[i], roles[j]] += direct[i] * inverse[j] / 2
            role[roles[j], roles[i]] -= inverse[i] * direct[j] / 2
        result += sp.kronecker_product(role, sp.Matrix(form))
    return result


def metric_units(solder):
    gram = solder.T * nf.ETA * solder
    units = []
    for q in nf.Q_DIRECTIONS:
        lift = solder * gram.inv() * q / 2
        faces = []
        for r, s in PAIRS:
            u, v = [k for k in range(4) if k not in (r, s)]
            seq = [r, s, u, v]
            orientation = (-1) ** sum(seq[a] > seq[b] for a, b in combinations(range(4), 2))
            d_area = nf.wedge(lift[:, u], solder[:, v]) + nf.wedge(solder[:, u], lift[:, v])
            packed = orientation * d_area.T * nf.G2 * nf.STAR
            role_units = []
            for role in (r, s):
                coeffs = []
                for generator in GENERATORS:
                    coords = sp.Matrix([(generator * nf.ETA)[a, b] for a, b in PAIRS])
                    coeffs.append(sp.together((packed * coords)[0]))
                role_units.append((role, coeffs))
            faces.append((r, s, role_units))
        units.append(faces)
    return units


def metric(units, physical):
    rows = []
    for faces in units:
        row = [sp.Integer(0)] * 24
        for r, s, role_units in faces:
            factors = {r: 1 - physical[s], s: physical[r] - 1}
            for role, coeffs in role_units:
                for j, coeff in enumerate(coeffs):
                    row[6 * role + j] += factors[role] * coeff
        rows.append([sp.together(entry) for entry in row])
    return sp.Matrix(rows)


def moment_blocks(phase, basis):
    gram = SHEAR.T * nf.ETA * SHEAR
    blocks = []
    for q in nf.Q_DIRECTIONS:
        lift = SHEAR * gram.inv() * q / 2
        derivative = (
            nf.connection_symbol(SHEAR + lift, list(phase))
            - nf.connection_symbol(SHEAR - lift, list(phase))
        ) / 2
        blocks.append(sp.simplify(sp.conjugate(basis).T * derivative * basis))
    return blocks


def main():
    stored = brackets(SHEAR)
    units = metric_units(SHEAR)
    fast_h = connection(stored, SHEAR_CHARACTER)
    fast_c = metric(units, [1 / z for z in SHEAR_CHARACTER])
    owner_h, owner_c = nf.joint_symbols(SHEAR, SHEAR_CHARACTER)
    check(
        "SHEAR_CHARACTER_MATCHES_216",
        (fast_h - owner_h).applyfunc(sp.expand) == sp.zeros(24)
        and (fast_c - owner_c).applyfunc(sp.expand) == sp.zeros(10, 24),
    )

    singular = {}
    for phase in product(ROOTS, repeat=4):
        joint = connection(stored, phase).col_join(
            metric(units, [1 / z for z in phase])
        ).applyfunc(sp.expand)
        rank = nf.exact_rank(joint)
        if rank < 24:
            basis = nf.exact_nullspace(joint)
            singular[tuple(phase)] = (rank, basis)
    check("EXACTLY_THREE_SINGULAR_CHARACTERS", len(singular) == 3)
    check("SINGULAR_SET", set(singular) == {SHEAR_CHARACTER, *DIAGONAL})

    for phase in DIAGONAL:
        rank, basis = singular[phase]
        check(f"DIAGONAL_RANK_20_{phase[0]}", rank == 20 and basis.cols == 4)
        blocks = moment_blocks(phase, basis)
        check(
            f"DIAGONAL_MOMENTS_ZERO_{phase[0]}",
            all(block == sp.zeros(4) for block in blocks),
        )

    rank, basis = singular[SHEAR_CHARACTER]
    check("SHEAR_RANK_23", rank == 23 and basis.cols == 1)
    check("SHEAR_WITNESS", primitive_column(basis) == WITNESS)
    blocks = moment_blocks(SHEAR_CHARACTER, WITNESS)
    expected = [sp.Integer(0)] * 10
    expected[4] = sp.Integer(-2)
    check(
        "SHEAR_MOMENT_MINUS_TWO",
        [sp.simplify(block[0]) for block in blocks] == expected,
    )
    print("RESULT_SHEAR_L4_SUPPORT: 253 full rank, two moment-free diagonal kernels, one cut defect")
    print("BOUNDARY: this solder and the L=4 grid only; not a global NF theorem and not a response NOGO")


if __name__ == "__main__":
    main()
