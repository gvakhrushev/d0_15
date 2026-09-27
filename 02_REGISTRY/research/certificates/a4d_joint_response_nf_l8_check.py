#!/usr/bin/env python3
"""Exact L=8 flat-solder joint-response moment census for EXP A4D.

The 8^4 character scan is reduced by a sound F_17 specialization of the
#216 owner symbols. A full-rank modular minor certifies full rank over
K=Q(sqrt(2), i); modularly singular points are then checked exactly in K.
For every exact joint kernel, all ten Gram-direction response moments are
computed from the literal solder symbol. This is a finite L=8 flat-solder
certificate, not a continuous-torus or all-background theorem.
"""
from __future__ import annotations

from collections import Counter
from itertools import product
from pathlib import Path
import runpy

import sympy as sp
from sympy.polys.matrices import DomainMatrix

HERE = Path(__file__).resolve().parent
shared = runpy.run_path(str(HERE / "a4d_joint_response_nf_l4_check.py"))
HAB = shared["connection_owner"]
HAQ = shared["metric_owner"]
z = shared["z_owner"]
connection_symbol = shared["connection_symbol"]
joint_symbols = shared["joint_symbols"]
Q_DIRECTIONS = shared["Q_DIRECTIONS"]
ETA = shared["ETA"]

MOD = 17
OMEGA_MOD = 9  # order eight in F_17; sqrt(2) maps to 11 and i to 13.
ROOT2 = sp.sqrt(2)
I = sp.I
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
FIELD = sp.QQ.algebraic_field(ROOT2, I)


def check(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name, flush=True)


def laurent_entry(expr: sp.Expr):
    """Compile a rational Laurent entry to F_17 monomials."""
    result = []
    for term in sp.Add.make_args(sp.expand(expr)):
        powers_map = term.as_powers_dict()
        powers = tuple(int(powers_map.get(zi, 0)) for zi in z)
        coefficient = sp.cancel(term / sp.prod(zi ** power for zi, power in zip(z, powers)))
        if coefficient.is_Rational is not True:
            raise AssertionError(f"non-rational Laurent coefficient: {coefficient}")
        numerator, denominator = map(int, sp.fraction(coefficient))
        if denominator % MOD == 0:
            raise AssertionError("a Laurent coefficient denominator vanishes mod 17")
        residue = numerator * pow(denominator, -1, MOD) % MOD
        result.append((powers, residue))
    return tuple(result)


def compile_matrix(matrix: sp.Matrix):
    return tuple(tuple(laurent_entry(matrix[i, j]) for j in range(matrix.cols))
                 for i in range(matrix.rows))


def eval_entry(poly, character):
    return sum(
        coefficient * pow(OMEGA_MOD,
                          sum(exponent * k for exponent, k in zip(powers, character)),
                          MOD)
        for powers, coefficient in poly
    ) % MOD


def eval_matrix(poly, character):
    return [[eval_entry(poly[i][j], character) for j in range(len(poly[i]))]
            for i in range(len(poly))]


def rank_mod(matrix):
    a = [row[:] for row in matrix]
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
            if r == rank:
                continue
            factor = a[r][col] % MOD
            if factor:
                a[r] = [(x - factor * y) % MOD
                        for x, y in zip(a[r], a[rank])]
        rank += 1
        if rank == nrows:
            break
    return rank


def zero_matrix(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(value) == 0 for value in matrix)


def exact_rank(matrix: sp.Matrix) -> int:
    return DomainMatrix.from_Matrix(matrix).convert_to(FIELD).rank()


def exact_nullspace(matrix: sp.Matrix) -> sp.Matrix:
    # DomainMatrix stores nullspace vectors as rows; return column amplitudes.
    return DomainMatrix.from_Matrix(matrix).convert_to(FIELD).nullspace().to_Matrix().T


def main() -> None:
    # H and C are the merged #216 owner symbols, compiled once as Laurent
    # polynomials. C=HAQ^T in the documented inverse-polarization convention.
    h_poly = compile_matrix(HAB)
    c_poly = compile_matrix(HAQ.T)
    candidates = []
    modular_ranks = Counter()
    for character in product(range(8), repeat=4):
        h_mod = eval_matrix(h_poly, character)
        c_mod = eval_matrix(c_poly, character)
        rank = rank_mod(h_mod + c_mod)
        modular_ranks[rank] += 1
        if rank < 24:
            candidates.append(character)
    check("MOD17_SCAN_ALL_4096_CHARACTERS", sum(modular_ranks.values()) == 8**4)
    check("MOD17_FILTER_44_CANDIDATES", len(candidates) == 44)
    check("MOD17_RANK_COUNTS", modular_ranks == Counter({24: 4052, 23: 42, 20: 2}))

    exact_joint_ranks = Counter()
    exact_h_rank_nullities = Counter()
    total_moments = 0
    for index, character in enumerate(candidates):
        phase = tuple(ROOTS[k] for k in character)
        h, c = joint_symbols(sp.eye(4), phase)
        owner_sub = dict(zip(z, phase))
        if not zero_matrix(h - HAB.subs(owner_sub)):
            raise AssertionError(f"#216 H owner mismatch at {character}")
        if not zero_matrix(c - HAQ.subs(owner_sub).T):
            raise AssertionError(f"#216 C owner mismatch at {character}")

        joint = h.col_join(c)
        rank_joint = exact_rank(joint)
        basis = exact_nullspace(joint) if rank_joint < 24 else sp.zeros(24, 0)
        nullity = 24 - rank_joint
        if basis.cols != nullity or not zero_matrix(joint * basis):
            raise AssertionError(f"exact joint-kernel check failed at {character}")
        rank_h = exact_rank(h)
        exact_joint_ranks[rank_joint] += 1
        exact_h_rank_nullities[(rank_h, nullity)] += 1
        if nullity == 0:
            # A mod-singular point may be a false positive and is harmless.
            print(f"EXACT_CANDIDATE {index:02d} {character} nullity=0", flush=True)
            continue

        gram = sp.eye(4).T * ETA * sp.eye(4)
        for q_index, q in enumerate(Q_DIRECTIONS):
            lift = sp.eye(4) * gram.inv() * q / 2
            # H is exactly quadratic in the solder columns, so this central
            # difference is the exact derivative D_Q H[q], not an approximation.
            jq = (connection_symbol(sp.eye(4) + lift, list(phase))
                  - connection_symbol(sp.eye(4) - lift, list(phase))) / 2
            moment = basis.conjugate().T * jq * basis
            if not zero_matrix(moment):
                raise AssertionError(
                    f"response moment failed at {character}, q[{q_index}]"
                )
            total_moments += 1
        print(
            f"EXACT_CANDIDATE {index:02d} {character} "
            f"rankH={rank_h} nullity={nullity} all10NF=True",
            flush=True,
        )

    check("EXACT_ALL_44_HAVE_JOINT_KERNEL", exact_joint_ranks == Counter({23: 42, 20: 2}))
    check("EXACT_JOINT_NULLITY_DISTRIBUTION",
          exact_h_rank_nullities == Counter({(22, 1): 36, (20, 1): 6, (16, 4): 2}))
    check("EXACT_ALL_440_RESPONSE_MOMENTS", total_moments == 44 * 10)
    print("RESULT: all 4096 L=8 flat-solder characters are exhausted exactly.")
    print("RESULT: only 44 have a joint kernel; every one has zero D_Q H moment in all ten Gram directions.")
    print("BOUNDARY: finite L=8 flat-solder grid only; continuous phases and general solder remain open.")


if __name__ == "__main__":
    main()
