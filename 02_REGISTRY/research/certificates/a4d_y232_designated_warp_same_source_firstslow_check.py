#!/usr/bin/env python3
"""Exact same-source first-slow compatibility test at the #216 curved sheet.

At a point of a fixed nonconstant spatial warp, take the actual first smooth
#216 link coefficient, multiply it by the finite #232 period-four Y pattern,
and ask whether arbitrary regular first-order link corrections and both
flat-center envelope slopes can satisfy all 96 connection and all 40 metric
rows for the same metric source.  The answer is an exact 97/98 rank
obstruction.  This is a local formal obstruction, not a nonlinear no-go.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import sys

import sympy as sp
from sympy.polys.domains import QQ
from sympy.polys.matrices import DomainMatrix


HERE = Path(__file__).resolve().parent
BIAS_CHECK = HERE / "a4d_warped_smooth_comparator_bias_check.py"
BIAS_RESULTS = HERE / "a4d_warped_smooth_comparator_bias_results.json"
SMOOTH_RESPONSE_OWNER = HERE / "a4d_identity_quarter_nonlinear_response_check.py"
STENCIL_PATH = HERE / "a4d_y_curved_joint_rational_stencil.py"
OWNER_PATH = HERE / "a4d_y_slow_exact_plane_check.py"


def check(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name, flush=True)


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ST = load_module("y232_designated_warp_stencil", STENCIL_PATH)
OWNER = load_module("y232_designated_warp_owner", OWNER_PATH)

H = sp.symbols("h", real=True)
I4 = OWNER.I4
ETA = OWNER.ETA
GEN = OWNER.GEN
PAIRS = OWNER.PAIRS
SYM = [(a, b) for a in range(4) for b in range(a, 4)]
PROFILE_SLOPE = sp.Rational(1, 50)


def h_coefficient(expression):
    return sp.factor(sp.diff(expression, H).subs(H, 0))


def metric_euler(link, site, row, col):
    """Literal ten Gram-slot derivative at the metric-normal site f=1."""
    direction = sp.zeros(4)
    direction[row, col] = direction[col, row] = 1
    variation = direction * ETA / 2
    solder_at_site = sp.eye(4)  # f(0)=1, so the Gram lift is dS=dQ*eta/2.
    total = 0
    for a, b in PAIRS:
        places = [
            (site, a, False),
            (OWNER.shift(site, a), b, False),
            (OWNER.shift(site, b), a, True),
            (site, b, True),
        ]
        factors = [
            OWNER.linv(link(x, role)) if inverse else link(x, role)
            for x, role, inverse in places
        ]
        holonomy = factors[0] * factors[1] * factors[2] * factors[3]
        curvature = (holonomy - OWNER.linv(holonomy)) / 2
        u, v = [j for j in range(4) if j not in (a, b)]
        area_variation = (
            OWNER.wedge(variation[:, u], solder_at_site[:, v])
            + OWNER.wedge(solder_at_site[:, u], variation[:, v])
        )
        total += OWNER.orientation(a, b) * (
            area_variation.T * OWNER.G2 * OWNER.STAR * OWNER.bivector(curvature)
        )[0]
    return sp.factor(total)


def source_vector(link, solder):
    connection = [
        h_coefficient(
            OWNER.edge_euler(solder, link, (phase, 0, 0, 0), role, GEN[generator])
        )
        for phase, role, generator in ST.LABELS
    ]
    metric = [
        h_coefficient(metric_euler(link, (phase, 0, 0, 0), row, col))
        for phase in range(4)
        for row, col in SYM
    ]
    return sp.Matrix(connection + metric)


def stencil_matrix(terms, row_count: int, moment_axis: int | None = None):
    matrix = sp.zeros(row_count, 96)
    for shift, entries in terms.items():
        weight = 1 if moment_axis is None else shift[moment_axis]
        if not weight:
            continue
        for (row, col), value in entries.items():
            matrix[row, col] += weight * sp.Rational(value.numerator, value.denominator)
    return matrix


def left_null_witness(matrix: sp.MatrixBase, rhs: sp.MatrixBase):
    reduced, pivots = DomainMatrix.from_Matrix(matrix.T).convert_to(QQ).rref()
    reduced = reduced.to_Matrix()
    pivot_set = set(pivots)
    candidates = []
    for free_column in range(matrix.rows):
        if free_column in pivot_set:
            continue
        candidate = sp.zeros(matrix.rows, 1)
        candidate[free_column] = 1
        for row, pivot_column in enumerate(pivots):
            candidate[pivot_column] = -reduced[row, free_column]
        pairing = sp.factor((candidate.T * rhs)[0])
        if pairing:
            support = sum(value != 0 for value in candidate)
            candidates.append((support, candidate, pairing))
    if not candidates:
        return None
    _, witness, pairing = min(candidates, key=lambda item: item[0])
    return witness, pairing


def main() -> None:
    # Pin the #216 first smooth coefficient used at f=1.  In the owner's
    # (role-major, K1,K2,K3,J12,J13,J23) coordinates these are -p*J12 on
    # role 2 and -p*J13 on role 3.
    bias = json.loads(BIAS_RESULTS.read_text())
    owner_sha = hashlib.sha1(SMOOTH_RESPONSE_OWNER.read_bytes()).hexdigest()
    check("PINNED_SMOOTH_OWNER_SHA1", owner_sha == bias["owner_sha1"])
    check("PINNED_SMOOTH_GENERATOR_ORDER", bias["generator_order"] == [
        "K1", "K2", "K3", "J12", "J13", "J23"
    ])
    check("PINNED_SMOOTH_A1_SUPPORT", bias["A1"] == [[15, "-p"], [22, "-p"]])

    # The fixed profile f(y)=1+sin(2*pi*y)/(100*pi) is smooth and positive.
    # At y=0, f=1, f'=1/50, f''=0 and the scalar curvature is 1/1250.
    y = sp.symbols("y", real=True)
    f = 1 + sp.sin(2 * sp.pi * y) / (100 * sp.pi)
    f0 = f.subs(y, 0)
    fp0 = sp.diff(f, y).subs(y, 0)
    fpp0 = sp.diff(f, y, 2).subs(y, 0)
    scalar_curvature0 = sp.factor((4 * f * sp.diff(f, y, 2) + 2 * sp.diff(f, y) ** 2) / f**2).subs(y, 0)
    check("FIXED_PROFILE_JET", (f0, fp0, fpp0) == (1, PROFILE_SLOPE, 0))
    check("FIXED_PROFILE_IS_CURVED", scalar_curvature0 == sp.Rational(1, 1250))

    smooth_log_coefficient = [sp.zeros(4) for _ in range(4)]
    smooth_log_coefficient[2] = -PROFILE_SLOPE * GEN[3]
    smooth_log_coefficient[3] = -PROFILE_SLOPE * GEN[4]

    def solder(site):
        # Exact first Taylor coefficient of S(y+hn) at the chosen point.
        out = sp.eye(4)
        out[2, 2] = out[3, 3] = 1 + H * site[1] * PROFILE_SLOPE
        return out

    def smooth_link(_site, role):
        # K_h^sm=I+h*A1+O(h^2), with A1 taken from the pinned #216 owner.
        return sp.eye(4) + H * smooth_log_coefficient[role]

    Y = GEN[3] - GEN[4] + GEN[5]
    amplitude = sp.symbols("amplitude", real=True)
    U_family = OWNER.cayley_simple(Y, 3, amplitude)
    U = U_family.subs(amplitude, 1).applyfunc(sp.factor)
    check("PINNED_Y_CAYLEY_LINK", U == sp.Matrix(ST.U))
    wave = [U, I4, OWNER.linv(U), I4]

    def micro_link(site, role):
        # K_h^sm W: the smooth role-0 coefficient vanishes at this jet,
        # while W is the exact #232 period-four Y carrier.
        return smooth_link(site, role) * (wave[sum(site) % 4] if role == 0 else I4)

    def flat_solder(_site):
        return sp.eye(4)

    def flat_link(site, role):
        return wave[sum(site) % 4] if role == 0 else I4

    check("FLAT_232_BASE_ALL_96_CONNECTION_ROWS", all(
        OWNER.edge_euler(flat_solder, flat_link, (phase, 0, 0, 0), role, gen) == 0
        for phase, role, gen_index in ST.LABELS
        for gen in (GEN[gen_index],)
    ))
    check("FLAT_232_BASE_ALL_40_METRIC_ROWS", all(
        metric_euler(flat_link, (phase, 0, 0, 0), row, col) == 0
        for phase in range(4)
        for row, col in SYM
    ))

    # #216's own coefficient makes both the connection residual and its
    # metric source vanish at order h.  Thus the same-source right-hand side
    # for the candidate is exactly zero in all 136 rows at this order.
    smooth_source = source_vector(smooth_link, solder)
    check("DESIGNATED_SMOOTH_SOURCE_H1_ZERO_ALL_136", smooth_source == sp.zeros(136, 1))
    candidate_source = source_vector(micro_link, solder)
    expected_unit_source = {
        13: sp.Rational(2, 7), 14: -sp.Rational(1, 7),
        19: sp.Rational(3, 7), 20: sp.Rational(2, 7),
        25: sp.Rational(6, 7), 26: sp.Rational(6, 7),
        37: -sp.Rational(2, 7), 38: sp.Rational(1, 7),
        43: -sp.Rational(3, 7), 44: -sp.Rational(2, 7),
        61: sp.Rational(2, 7), 62: sp.Rational(3, 7),
        67: -sp.Rational(1, 7), 68: sp.Rational(2, 7),
        73: sp.Rational(6, 7), 74: sp.Rational(6, 7),
        85: -sp.Rational(2, 7), 86: -sp.Rational(3, 7),
        91: sp.Rational(1, 7), 92: -sp.Rational(2, 7),
        108: -sp.Rational(2, 7), 109: sp.Rational(2, 7),
        128: sp.Rational(2, 7), 129: -sp.Rational(2, 7),
    }
    expected_source = sp.zeros(136, 1)
    for index, value in expected_unit_source.items():
        expected_source[index] = PROFILE_SLOPE * value
    check("CURVED_PROFILE_SOURCE_ALL_136_EXACT", candidate_source == expected_source)

    # The zero-frequency link correction has all 96 phase/role/generator
    # coordinates. Add both allowed slow derivatives of the exact flat
    # center fiber: the Cayley amplitude and the boost-dual center.
    A0 = stencil_matrix(ST.ATERMS, 96)
    A1 = stencil_matrix(ST.ATERMS, 96, moment_axis=1)
    Q0 = stencil_matrix(ST.QTERMS, 40)
    Q1 = stencil_matrix(ST.QTERMS, 40, moment_axis=1)
    centers = sp.zeros(96, 2)
    right_log = (OWNER.linv(U_family) * sp.diff(U_family, amplitude)).subs(
        amplitude, 1
    ).applyfunc(sp.factor)
    for generator, (a, b) in enumerate(PAIRS):
        centers[ST.IDX[(0, 0, generator)], 0] = right_log[a, b]
        centers[ST.IDX[(2, 0, generator)], 0] = -right_log[a, b]
    boost_dual = GEN[0] + GEN[1] + GEN[2]
    for generator, (a, b) in enumerate(PAIRS):
        centers[ST.IDX[(0, 0, generator)], 1] = -boost_dual[a, b]
        centers[ST.IDX[(2, 0, generator)], 1] = boost_dual[a, b]
    connection_rank = DomainMatrix.from_Matrix(A0).convert_to(QQ).rank()
    check("TWO_EXACT_FLAT_CENTER_TANGENTS", A0 * centers == sp.zeros(96, 2))
    check("FLAT_CONNECTION_KERNEL_IS_EXACTLY_THE_TWO_CENTERS",
          connection_rank == 94 and centers.rank() == 2)

    base_joint = A0.col_join(Q0)
    center_slopes = (A1 * centers).col_join(Q1 * centers)
    full_joint = base_joint.row_join(center_slopes)
    rhs = -candidate_source
    matrix_rank = DomainMatrix.from_Matrix(full_joint).convert_to(QQ).rank()
    augmented_rank = DomainMatrix.from_Matrix(full_joint.row_join(rhs)).convert_to(QQ).rank()
    check("ALL_136_ROWS_AND_98_UNKNOWN_SHAPE", full_joint.shape == (136, 98))
    check("FULL_SAME_SOURCE_FIRSTSLOW_OBSTRUCTION_97_TO_98",
          matrix_rank == 97 and augmented_rank == 98)

    witness_data = left_null_witness(full_joint, rhs)
    check("LEFT_NULL_SOURCE_WITNESS_EXISTS", witness_data is not None)
    assert witness_data is not None
    witness, pairing = witness_data
    check("LEFT_NULL_WITNESS_ANNIHILATES_ALL_CORRECTORS",
          full_joint.T * witness == sp.zeros(98, 1))
    check("LEFT_NULL_WITNESS_SEES_PRESCRIBED_SOURCE", pairing != 0)
    check("PINNED_LEFT_NULL_PAIRING",
          pairing == sp.Rational(4105021481, 2353113600))
    print("SOURCE_SUPPORT", sum(value != 0 for value in candidate_source))
    print("LEFT_NULL_WITNESS_SUPPORT", sum(value != 0 for value in witness))
    print("LEFT_NULL_PAIRING", sp.factor(pairing))
    print("TERMINAL A4D-Y232-DESIGNATED-WARP-NO-REGULAR-H1-SAME-SOURCE-LIFT")


if __name__ == "__main__":
    main()
