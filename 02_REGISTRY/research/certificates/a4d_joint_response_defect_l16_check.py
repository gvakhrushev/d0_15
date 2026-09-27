#!/usr/bin/env python3
"""L=16 joint support on the two defect solders.

All 16^4 characters are ranked in F_17. A character of full modular rank is
full rank over the cyclotomic field. Characters that stay singular in F_97
are checked exactly. On each solder they are the two diagonal quarter-waves,
with vanishing moments, and the carrier already cut at order u^5.
"""
from __future__ import annotations

import importlib.util
from itertools import product
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    "support", HERE / "a4d_joint_response_shear_l4_support_check.py"
)
support = importlib.util.module_from_spec(spec)
spec.loader.exec_module(support)
nf = support.nf

CHAIN_WITNESS = sp.Matrix([
    0, 0, 0, 0, 0, 1,
    0, 0, 0, 0, 0, 0,
    -2, 0, -1, 0, -1, 0,
    0, 1, 0, 1, 0, 1,
])


def check(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name, flush=True)


def mod_int(value, modulus):
    rational = sp.Rational(sp.together(sp.expand(value)))
    numerator, denominator = map(int, sp.fraction(rational))
    if denominator % modulus == 0:
        raise AssertionError(f"denominator {denominator} vanishes mod {modulus}")
    return numerator * pow(denominator, -1, modulus) % modulus


def rank_mod(rows, modulus):
    table = [row[:] for row in rows]
    rank = 0
    for col in range(24):
        pivot = next((r for r in range(rank, len(table)) if table[r][col] % modulus), None)
        if pivot is None:
            continue
        table[rank], table[pivot] = table[pivot], table[rank]
        inverse = pow(table[rank][col], -1, modulus)
        table[rank] = [(entry * inverse) % modulus for entry in table[rank]]
        for row_index in range(len(table)):
            if row_index == rank or table[row_index][col] % modulus == 0:
                continue
            factor = table[row_index][col]
            table[row_index] = [
                (entry - factor * pivot_entry) % modulus
                for entry, pivot_entry in zip(table[row_index], table[rank])
            ]
        rank += 1
    return rank


def prepare(solder, modulus):
    half = pow(2, -1, modulus)
    stored = []
    for r, s, form in support.brackets(solder):
        stored.append((r, s, [[mod_int(entry, modulus) for entry in row] for row in form]))
    units = []
    for faces in support.metric_units(solder):
        units.append([
            (r, s, [(role, [mod_int(coeff, modulus) for coeff in coeffs]) for role, coeffs in role_units])
            for r, s, role_units in faces
        ])
    return stored, units, half


def assemble(stored, units, half, exponents, omega, modulus):
    phase = [pow(omega, k, modulus) for k in exponents]
    inverse = [pow(value, -1, modulus) for value in phase]
    connection = [[0] * 24 for _ in range(24)]
    for r, s, form in stored:
        roles = [r, s, r, s]
        direct = [1, phase[r], (-phase[s]) % modulus, modulus - 1]
        inv = [1, inverse[r], (-inverse[s]) % modulus, modulus - 1]
        role = [[0] * 4 for _ in range(4)]
        for i in range(4):
            for j in range(i + 1, 4):
                role[roles[i]][roles[j]] = (
                    role[roles[i]][roles[j]] + direct[i] * inv[j] * half
                ) % modulus
                role[roles[j]][roles[i]] = (
                    role[roles[j]][roles[i]] - inv[i] * direct[j] * half
                ) % modulus
        for a in range(4):
            for b in range(4):
                scale = role[a][b]
                if scale == 0:
                    continue
                for i in range(6):
                    for j in range(6):
                        connection[6 * a + i][6 * b + j] = (
                            connection[6 * a + i][6 * b + j] + scale * form[i][j]
                        ) % modulus
    metric_rows = []
    for faces in units:
        row = [0] * 24
        for r, s, role_units in faces:
            factors = {
                r: (1 - inverse[s]) % modulus,
                s: (inverse[r] - 1) % modulus,
            }
            for role, coeffs in role_units:
                for j, coeff in enumerate(coeffs):
                    row[6 * role + j] = (row[6 * role + j] + factors[role] * coeff) % modulus
        metric_rows.append(row)
    return connection + metric_rows


def moments(solder, phase, vector):
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


def diagonal_moments_vanish(solder, phase):
    stored = support.brackets(solder)
    units = support.metric_units(solder)
    joint = support.connection(stored, phase).col_join(
        support.metric(units, [1 / z for z in phase])
    ).applyfunc(sp.expand)
    basis = nf.exact_nullspace(joint)
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
    return basis.cols == 4


def screen(solder):
    stored17, units17, half17 = prepare(solder, 17)
    stored97, units97, half97 = prepare(solder, 97)
    omega97 = pow(5, 6, 97)
    counts = {}
    survivors = []
    for exponents in product(range(16), repeat=4):
        rank17 = rank_mod(assemble(stored17, units17, half17, exponents, 3, 17), 17)
        counts[rank17] = counts.get(rank17, 0) + 1
        if rank17 == 24:
            continue
        rank97 = rank_mod(assemble(stored97, units97, half97, exponents, omega97, 97), 97)
        if rank97 < 24:
            survivors.append(exponents)
    return counts, survivors


def main():
    upper = sp.Matrix([[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    chain = sp.eye(4)
    chain[0, 1] += 1
    chain[1, 3] += 1
    expected_counts = {24: 65459, 23: 69, 22: 6, 20: 2}
    phases = {
        (4, 4, 4, 4): (sp.I, sp.I, sp.I, sp.I),
        (12, 12, 12, 12): (-sp.I, -sp.I, -sp.I, -sp.I),
    }
    jobs = (
        ("UPPER", upper, (8, 0, 8, 0), (sp.Integer(-1), sp.Integer(1), sp.Integer(-1), sp.Integer(1)), support.WITNESS),
        ("CHAIN", chain, (8, 0, 0, 8), (sp.Integer(-1), sp.Integer(1), sp.Integer(1), sp.Integer(-1)), CHAIN_WITNESS),
    )
    for name, solder, defect, defect_phase, witness in jobs:
        counts, survivors = screen(solder)
        check(f"{name}_MOD17_COUNTS", counts == expected_counts)
        check(f"{name}_SURVIVORS", set(survivors) == {(4, 4, 4, 4), defect, (12, 12, 12, 12)})
        for exponents, phase in phases.items():
            check(f"{name}_DIAGONAL_{exponents[0]}", diagonal_moments_vanish(solder, phase))
        stored = support.brackets(solder)
        units = support.metric_units(solder)
        joint = support.connection(stored, defect_phase).col_join(
            support.metric(units, [1 / z for z in defect_phase])
        ).applyfunc(sp.expand)
        found = support.primitive_column(nf.exact_nullspace(joint))
        check(f"{name}_WITNESS", found == witness)
        check(
            f"{name}_MOMENT",
            moments(solder, defect_phase, witness) == [0, 0, 0, 0, -2, 0, 0, 0, 0, 0],
        )
    print("RESULT_L16: only the two cut carriers have a nonzero moment")
    print("BOUNDARY: these two solders and the 16th-root grid")


if __name__ == "__main__":
    main()
