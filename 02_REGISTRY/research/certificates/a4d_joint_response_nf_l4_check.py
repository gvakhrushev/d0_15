#!/usr/bin/env python3
"""Exact L=4 flat-solder response-moment check for EXP A4D.

This checks the frozen joint-kernel identity

    v* D_Q H_Q(z)[q] v = 0,  H_Q(z)v = C_Q(z)v = 0

on every character of the four-role L=4 torus at the standard solder.  It
also checks three exact nonstandard-solder samples on the eighteen
one-dimensional flat resonant carriers.  The samples are finite controls;
they do not prove the all-background identity.

Conventions are matched to the direct Fourier maps of #216/#234:
table phase zeta is used in H_Q(zeta), while the direct metric map is
evaluated on physical phase chi=zeta^-1 and equals H_AQ(zeta)^T.
"""
from __future__ import annotations

from collections import Counter
from itertools import combinations, product
from pathlib import Path

import sympy as sp
from sympy.polys.domains import QQ_I
from sympy.polys.matrices import DomainMatrix


def check(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name, flush=True)


HERE = Path(__file__).resolve().parent

# Reuse the merged #216 general-solder BCH symbol without running the rest of
# its expensive certificate.  Its definition block ends at this stable guard.
ir_source = (HERE / "a4d_j2_fixed_realization_ir_check.py").read_text(
    encoding="utf-8"
)
ir_ns: dict[str, object] = {}
exec(ir_source.split('check("LORENTZ_GENERATORS"')[0], ir_ns)

# Reuse the merged #216 direct flat-solder HAB/HAQ owner through construction
# of the full symbols, before its separate diagonal resonance calculations.
owner_source = (HERE / "a4d_j2_smooth_resonance_closure_check.py").read_text(
    encoding="utf-8"
)
owner_marker = "# Exact diagonal quarter-wave data."
if owner_marker not in owner_source:
    raise RuntimeError("#216 owner symbol-construction boundary changed")
owner_ns: dict[str, object] = {}
exec(owner_source.split(owner_marker)[0], owner_ns)

I = sp.I
ETA = ir_ns["ETA"]
PAIRS = ir_ns["PAIRS"]
GENERATORS = ir_ns["GENERATORS"]
G2 = ir_ns["G2"]
STAR = ir_ns["STAR"]
wedge = ir_ns["wedge"]
connection_symbol = ir_ns["connection_symbol"]
metric_owner = owner_ns["HAQ"]
connection_owner = owner_ns["HAB"]
z_owner = owner_ns["z"]

QPAIRS = [(i, j) for i in range(4) for j in range(i, 4)]
Q_DIRECTIONS: list[sp.Matrix] = []
for i, j in QPAIRS:
    q = sp.zeros(4)
    q[i, j] = q[j, i] = 1
    Q_DIRECTIONS.append(q)


def metric_symbol(solder: sp.Matrix, physical_phase: list[sp.Expr],
                  q: sp.Matrix) -> sp.Matrix:
    """Direct metric Euler symbol from the horizontal Gram lift.

    Components pair with q_ii and q_ij+q_ji exactly as in #216.  The lift is
    dE=E(E^T eta E)^-1 q/2.  This returns one 1x24 row for that q.
    """
    d_solder = solder * (solder.T * ETA * solder).inv() * q / 2
    result = sp.zeros(1, 24)
    for r, s in PAIRS:
        u, v = [k for k in range(4) if k not in (r, s)]
        seq = [r, s, u, v]
        orientation = (-1) ** sum(
            seq[a] > seq[b] for a, b in combinations(range(4), 2)
        )
        d_area = wedge(d_solder[:, u], solder[:, v]) + wedge(
            solder[:, u], d_solder[:, v]
        )
        for role, factor in ((r, 1 - physical_phase[s]),
                             (s, physical_phase[r] - 1)):
            for j, generator in enumerate(GENERATORS):
                bivector = factor * generator * ETA
                bivector_coords = sp.Matrix(
                    [bivector[a, b] for a, b in PAIRS]
                )
                result[0, 6 * role + j] += orientation * (
                    d_area.T * G2 * STAR * bivector_coords
                )[0]
    return result.applyfunc(sp.expand)


def exact_rank(matrix: sp.Matrix) -> int:
    return DomainMatrix.from_Matrix(matrix).convert_to(QQ_I).rank()


def exact_nullspace(matrix: sp.Matrix) -> sp.Matrix:
    # DomainMatrix stores basis vectors as rows; transpose to column amplitudes.
    return DomainMatrix.from_Matrix(matrix).convert_to(QQ_I).nullspace().to_Matrix().T


def inverse_character(phase: tuple[sp.Expr, ...]) -> list[sp.Expr]:
    return [sp.Integer(1) / z for z in phase]


def joint_symbols(solder: sp.Matrix, table_phase: tuple[sp.Expr, ...]):
    physical = inverse_character(table_phase)
    h = connection_symbol(solder, list(table_phase))
    c = sp.Matrix.vstack(*[
        metric_symbol(solder, physical, q) for q in Q_DIRECTIONS
    ])
    return h, c


def check_moment(solder: sp.Matrix, table_phase: tuple[sp.Expr, ...],
                 basis: sp.Matrix, label: str) -> int:
    gram = solder.T * ETA * solder
    for q_index, q in enumerate(Q_DIRECTIONS):
        lift = solder * gram.inv() * q / 2
        # H is quadratic in solder columns, so symmetric polarization is the
        # exact derivative, with no finite-difference truncation error.
        j_q = (
            connection_symbol(solder + lift, list(table_phase))
            - connection_symbol(solder - lift, list(table_phase))
        ) / 2
        response = (sp.conjugate(basis).T * j_q * basis).applyfunc(sp.simplify)
        if response != sp.zeros(basis.cols):
            raise AssertionError(f"{label}: response moment failed at q[{q_index}]")
    return len(Q_DIRECTIONS)


def main() -> None:
    roots = (sp.Integer(1), I, sp.Integer(-1), -I)
    flat = sp.eye(4)
    singular_data: list[tuple[tuple[sp.Expr, ...], int, sp.Matrix]] = []
    owner_matches = 0
    flat_moment_tests = 0

    # Independent all-column convention replay against the primary #216
    # matrices.  All 256 H and C symbols agree exactly, not just on selected
    # null vectors.  This also fixes the inverse-character placement.
    for table_phase in product(roots, repeat=4):
        owner_sub = dict(zip(z_owner, table_phase))
        h_expected = connection_owner.subs(owner_sub)
        c_expected = metric_owner.subs(owner_sub).T
        h_direct, c_direct = joint_symbols(flat, table_phase)
        if (h_direct - h_expected).applyfunc(sp.simplify) != sp.zeros(24):
            raise AssertionError(f"#216 H symbol mismatch at {table_phase}")
        if (c_direct - c_expected).applyfunc(sp.simplify) != sp.zeros(10, 24):
            raise AssertionError(f"#216 C symbol mismatch at {table_phase}")
        owner_matches += 1

        joint = h_direct.col_join(c_direct)
        rank = exact_rank(joint)
        if rank < 24:
            basis = exact_nullspace(joint)
            if basis.cols != 24 - rank:
                raise AssertionError(f"nullity mismatch at {table_phase}")
            if ((joint * basis).applyfunc(sp.simplify)
                    != sp.zeros(34, basis.cols)):
                raise AssertionError(f"joint-kernel membership failed at {table_phase}")
            flat_moment_tests += check_moment(
                flat, table_phase, basis, f"FLAT_CHAR_{table_phase}"
            )
            singular_data.append((table_phase, h_direct.rank(), basis))

    check("OWNER_ALL_256_H_C_SYMBOLS", owner_matches == 256)
    check("FLAT_ALL_200_RESPONSE_MOMENTS", flat_moment_tests == 200)
    dim_counts = Counter(basis.cols for _, _, basis in singular_data)
    rank_dim_counts = Counter(
        (rank_h, basis.cols) for _, rank_h, basis in singular_data
    )
    check("L4_JOINT_SINGULAR_COUNT_20", len(singular_data) == 20)
    check("L4_JOINT_NULLITY_COUNTS", dim_counts == Counter({1: 18, 4: 2}))
    check(
        "L4_CONNECTION_RANK_COUNTS",
        rank_dim_counts == Counter({(22, 1): 12, (20, 1): 6, (16, 4): 2}),
    )
    check("L4_TOTAL_SOURCE_INVISIBLE_DIMENSION_26",
          sum(basis.cols for _, _, basis in singular_data) == 26)

    # The three exact curved nongauge one-dimensional orbits from #234 are
    # among the 18 carriers above.  Test their whole stabilizer/conjugation
    # orbits on three exact, nondegenerate curved constant-solder samples.
    one_d = [phase for phase, _, basis in singular_data if basis.cols == 1]
    samples = {
        "DIAGONAL_2_3_5_7": sp.diag(2, 3, 5, 7),
        "UPPER_SHEAR": sp.Matrix([[1, 1, 0, 0], [0, 1, 1, 0],
                                   [0, 0, 1, 0], [0, 0, 0, 1]]),
        "CURVED_RATIONAL": sp.Matrix([[2, 1, 0, 1], [0, 1, 1, 0],
                                      [1, 0, 1, 0], [0, 0, 0, 1]]),
    }
    for sample_name, solder in samples.items():
        gram = solder.T * ETA * solder
        check(f"{sample_name}_NONDEGENERATE", gram.det() != 0)
        lifted = 0
        for char_index, table_phase in enumerate(one_d):
            h, c = joint_symbols(solder, table_phase)
            joint = h.col_join(c)
            rank = exact_rank(joint)
            if rank < 24:
                basis = exact_nullspace(joint)
                if ((joint * basis).applyfunc(sp.simplify)
                        != sp.zeros(34, basis.cols)):
                    raise AssertionError(
                        f"{sample_name}: joint-kernel membership failed "
                        f"at {table_phase}"
                    )
                check_moment(
                    solder, table_phase, basis,
                    f"{sample_name}_CHAR_{char_index}",
                )
            if rank != 24:
                raise AssertionError(
                    f"{sample_name}: flat carrier persists at {table_phase}"
                )
            lifted += 1
        check(f"{sample_name}_ALL_18_ONE_D_CARRIERS_LIFTED", lifted == 18)

    print(
        "RESULT: the full flat-solder L=4 joint-kernel support has zero "
        "quadratic response moment; all 18 one-dimensional carriers lift "
        "on the three exact curved-solder samples."
    )
    print(
        "BOUNDARY: finite L=4 and finite solder samples only; the all-phase, "
        "all-background NF and the EXP terminal remain open."
    )


if __name__ == "__main__":
    main()
