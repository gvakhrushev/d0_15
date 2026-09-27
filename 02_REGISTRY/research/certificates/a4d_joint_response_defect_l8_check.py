#!/usr/bin/env python3
"""L=8 joint support on the two defect solders.

An F_17 screen of all 8^4 characters is calibrated against the exact symbol
at one mixed 8th root. Full modular rank certifies full rank over
Q(sqrt(2), i). Every modularly singular character is checked exactly.
On each solder the only nonzero moment is the already cut carrier, on q_11.
"""
from __future__ import annotations

import importlib.util
from itertools import product
from pathlib import Path

import sympy as sp
from sympy.polys.matrices import DomainMatrix

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    "support", HERE / "a4d_joint_response_shear_l4_support_check.py"
)
support = importlib.util.module_from_spec(spec)
spec.loader.exec_module(support)
nf = support.nf

MOD = 17
OMEGA = 9
INV2 = pow(2, -1, MOD)
ROOT2 = sp.sqrt(2)
I = sp.I
FIELD = sp.QQ.algebraic_field(ROOT2, I)
ROOTS = (
    sp.Integer(1),
    ROOT2 * (1 + I) / 2,
    I,
    ROOT2 * (-1 + I) / 2,
    sp.Integer(-1),
    ROOT2 * (-1 - I) / 2,
    -I,
    ROOT2 * (1 - I) / 2,
)
PAIRS = list(nf.PAIRS)


def mod_int(value):
    rational = sp.together(sp.expand(value))
    numerator, denominator = map(int, sp.fraction(sp.Rational(rational)))
    if denominator % MOD == 0:
        raise AssertionError(f"denominator {denominator} vanishes mod 17")
    return numerator * pow(denominator, -1, MOD) % MOD


def rank_mod(rows):
    a = [row[:] for row in rows]
    nrows, ncols = len(a), len(a[0])
    rank = 0
    for col in range(ncols):
        pivot = next((r for r in range(rank, nrows) if a[r][col] % MOD), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        inv = pow(a[rank][col] % MOD, -1, MOD)
        a[rank] = [(x * inv) % MOD for x in a[rank]]
        for r in range(nrows):
            if r == rank or a[r][col] % MOD == 0:
                continue
            factor = a[r][col] % MOD
            a[r] = [(x - factor * y) % MOD for x, y in zip(a[r], a[rank])]
        rank += 1
        if rank == nrows:
            break
    return rank


def prepare(solder):
    stored = []
    for r, s, form in support.brackets(solder):
        stored.append((r, s, [[mod_int(entry) for entry in row] for row in form]))
    units = []
    for faces in support.metric_units(solder):
        converted = []
        for r, s, role_units in faces:
            converted.append((r, s, [(role, [mod_int(c) for c in coeffs]) for role, coeffs in role_units]))
        units.append(converted)
    return stored, units


def assemble(stored, units, exponents):
    phase = [pow(OMEGA, k, MOD) for k in exponents]
    inverse = [pow(value, -1, MOD) for value in phase]
    h = [[0] * 24 for _ in range(24)]
    for r, s, form in stored:
        roles = [r, s, r, s]
        direct = [1, phase[r], (-phase[s]) % MOD, MOD - 1]
        inv = [1, inverse[r], (-inverse[s]) % MOD, MOD - 1]
        role = [[0] * 4 for _ in range(4)]
        for i in range(4):
            for j in range(i + 1, 4):
                role[roles[i]][roles[j]] = (
                    role[roles[i]][roles[j]] + direct[i] * inv[j] * INV2
                ) % MOD
                role[roles[j]][roles[i]] = (
                    role[roles[j]][roles[i]] - inv[i] * direct[j] * INV2
                ) % MOD
        for a in range(4):
            for b in range(4):
                if role[a][b] == 0:
                    continue
                for i in range(6):
                    for j in range(6):
                        h[6 * a + i][6 * b + j] = (
                            h[6 * a + i][6 * b + j] + role[a][b] * form[i][j]
                        ) % MOD
    c = []
    for faces in units:
        row = [0] * 24
        for r, s, role_units in faces:
            factors = {
                r: (1 - inverse[s]) % MOD,
                s: (inverse[r] - 1) % MOD,
            }
            for role, coeffs in role_units:
                factor = factors[role]
                for j, coeff in enumerate(coeffs):
                    row[6 * role + j] = (row[6 * role + j] + factor * coeff) % MOD
        c.append(row)
    return h + c


def exact_rank(matrix):
    return DomainMatrix.from_Matrix(matrix.applyfunc(sp.expand)).convert_to(FIELD).rank()


def exact_nullspace(matrix):
    return DomainMatrix.from_Matrix(matrix.applyfunc(sp.expand)).convert_to(FIELD).nullspace().to_Matrix().T


def moment_nonzero(solder, phase, basis):
    gram = solder.T * nf.ETA * solder
    hits = []
    for q_index, q in enumerate(nf.Q_DIRECTIONS):
        lift = solder * gram.inv() * q / 2
        derivative = (
            nf.connection_symbol(solder + lift, list(phase))
            - nf.connection_symbol(solder - lift, list(phase))
        ) / 2
        block = sp.simplify(sp.conjugate(basis).T * derivative * basis)
        if any(sp.simplify(entry) != 0 for entry in block):
            hits.append(q_index)
    return hits


def check(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name, flush=True)


def screen(name, solder):
    stored, units = prepare(solder)
    # Calibration: the known real character must match an exact rank.
    known = (4, 0, 4, 0)  # (-1, 1, -1, 1)
    modular = assemble(stored, units, known)
    print(name, "MOD_KNOWN_RANK", rank_mod(modular), flush=True)
    candidates = []
    counts = {}
    for exponents in product(range(8), repeat=4):
        rank = rank_mod(assemble(stored, units, exponents))
        counts[rank] = counts.get(rank, 0) + 1
        if rank < 24:
            candidates.append(exponents)
    print(name, "MOD_COUNTS", counts, "CANDIDATES", len(candidates), flush=True)
    exact = {}
    stored_exact = support.brackets(solder)
    units_exact = support.metric_units(solder)
    for exponents in candidates:
        phase = tuple(ROOTS[k] for k in exponents)
        joint = support.connection(stored_exact, phase).col_join(
            support.metric(units_exact, [1 / z for z in phase])
        )
        rank = exact_rank(joint)
        if rank == 24:
            exact[exponents] = (24, 0, [])
            continue
        basis = exact_nullspace(joint)
        hits = moment_nonzero(solder, phase, basis)
        vector = support.primitive_column(basis) if basis.cols == 1 else None
        exact[exponents] = (rank, basis.cols, hits, vector)
    return counts, exact


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


def calibrate(solder):
    exponents = (1, 2, 3, 5)
    phase = tuple(ROOTS[k] for k in exponents)
    stored_exact = support.brackets(solder)
    units_exact = support.metric_units(solder)
    joint = support.connection(stored_exact, phase).col_join(
        support.metric(units_exact, [1 / z for z in phase])
    ).applyfunc(sp.expand)
    modular = assemble(*prepare(solder), exponents)
    for i in range(34):
        for j in range(24):
            reduced = sp.together(sp.expand(joint[i, j]).subs({sp.sqrt(2): 11, sp.I: 13}))
            numerator, denominator = map(int, sp.fraction(reduced))
            value = numerator * pow(denominator, -1, MOD) % MOD
            if value != modular[i][j]:
                raise AssertionError(f"specialization mismatch at {(i, j)}")
    check("SPECIALIZATION_MATCHES_EXACT_SYMBOL", True)
    check("CALIBRATION_CHARACTER_FULL_RANK", exact_rank(joint) == 24 == rank_mod(modular))


def expect_kernel(exact, exponents, rank, nullity, hits):
    got = exact[exponents]
    check(
        f"EXACT_{exponents}",
        got[0] == rank and got[1] == nullity and got[2] == hits,
    )


def main():
    upper = sp.Matrix([[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    chain = sp.eye(4)
    chain[0, 1] += 1
    chain[1, 3] += 1
    calibrate(upper)
    for name, solder, defect, witness in (
        ("UPPER", upper, (4, 0, 4, 0), support.WITNESS),
        ("CHAIN", chain, (4, 0, 0, 4), sp.Matrix([
            0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0,
            -2, 0, -1, 0, -1, 0, 0, 1, 0, 1, 0, 1,
        ])),
    ):
        counts, exact = screen(name, solder)
        check(f"{name}_MOD_COUNTS", counts == {24: 4092, 20: 2, 23: 2})
        check(f"{name}_CANDIDATES", set(exact) == {
            (2, 2, 2, 2), defect, (6, 6, 6, 6),
            (3, 0, 6, 3) if name == "UPPER" else (3, 0, 3, 6),
        })
        expect_kernel(exact, (2, 2, 2, 2), 20, 4, [])
        expect_kernel(exact, (6, 6, 6, 6), 20, 4, [])
        expect_kernel(exact, defect, 23, 1, [4])
        false_positive = (3, 0, 6, 3) if name == "UPPER" else (3, 0, 3, 6)
        check(f"{name}_FALSE_POSITIVE_FULL", exact[false_positive] == (24, 0, []))
        phase = tuple(ROOTS[k] for k in defect)
        stored_exact = support.brackets(solder)
        units_exact = support.metric_units(solder)
        joint = support.connection(stored_exact, phase).col_join(
            support.metric(units_exact, [1 / z for z in phase])
        ).applyfunc(sp.expand)
        witness_now = support.primitive_column(nf.exact_nullspace(joint))
        check(f"{name}_WITNESS", witness_now == witness)
        check(
            f"{name}_MOMENT_MINUS_TWO",
            moments_of(solder, phase, witness) == [0, 0, 0, 0, -2, 0, 0, 0, 0, 0],
        )
    print("RESULT_L8_DEFECT_SOLDERS: only the two cut carriers have a nonzero moment")
    print("BOUNDARY: these two solders and the 8th-root grid; not every character")


if __name__ == "__main__":
    main()
