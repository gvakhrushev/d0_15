#!/usr/bin/env python3
"""Exact first-slow compatibility at the compactified t=infinity endpoint.

This is a task-scoped extension of the finite-amplitude #232 Cayley test.
It includes every joint flat-center direction at the limiting carrier,
without classifying any response-invisible direction as gauge.
"""
from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path

import sympy as sp
from sympy.polys.domains import QQ
from sympy.polys.matrices import DomainMatrix


HERE = Path(__file__).resolve().parent
BASE_CHECK = HERE / "a4d_y232_designated_warp_same_source_firstslow_check.py"
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


def aggregate(terms, row_count: int, moment_axis: int | None = None):
    matrix = sp.zeros(row_count, 96)
    for shift, entries in terms.items():
        weight = 1 if moment_axis is None else shift[moment_axis]
        if not weight:
            continue
        for (row, col), value in entries.items():
            matrix[row, col] += weight * sp.Rational(
                value.numerator, value.denominator
            )
    return matrix


def as_stencil_matrix(matrix, stencil):
    return [
        [
            stencil.F(int(sp.numer(value)), int(sp.denom(value)))
            for value in row
        ]
        for row in matrix.tolist()
    ]


def exact_rank(matrix) -> int:
    return DomainMatrix.from_Matrix(matrix).convert_to(QQ).rank()


def main() -> None:
    check(
        "PINNED_FIRSTSLOW_INPUTS",
        hashlib.sha256(BASE_CHECK.read_bytes()).hexdigest()
        == "1840477790bb1549b5c09e8158e7715e3c6d546bd6ea51fa5d751f48bd5aeaf7"
        and hashlib.sha256(STENCIL_PATH.read_bytes()).hexdigest()
        == "d4cf844b027f8cc34540c385b48922f3a5bcfc42cbedf08d5a704cfb7adb0daa"
        and hashlib.sha256(OWNER_PATH.read_bytes()).hexdigest()
        == "d85c644f22cdcd8b7c7ad63c72dd780c87af3184b4b35bf2b3e438bcde3afd21",
    )
    base = load_module("y232_infinite_base", BASE_CHECK)
    stencil = base.ST
    owner = base.OWNER

    # Cayley Y-link U(t)=I+4t/(4+3t^2)Y+2t^2/(4+3t^2)Y^2.
    # In the regular coordinate s=1/t its endpoint is I+(2/3)Y^2.
    Y = owner.GEN[3] - owner.GEN[4] + owner.GEN[5]
    t = sp.symbols("t", real=True)
    denominator = 4 + 3 * t**2
    family = owner.I4 + 4 * t / denominator * Y + 2 * t**2 / denominator * (Y * Y)
    U = family.applyfunc(lambda value: sp.limit(value, t, sp.oo))
    expected = owner.I4 + sp.Rational(2, 3) * (Y * Y)
    check("CAYLEY_LIMIT_EXACT", U == expected)
    check("LIMIT_IS_PROPER_LORENTZ", U.T * owner.ETA * U == owner.ETA and sp.det(U) == 1)

    U_stencil = as_stencil_matrix(U, stencil)
    stencil.W = (
        U_stencil,
        stencil.I4,
        stencil.linv(U_stencil),
        stencil.I4,
    )
    stencil.build_stencil.cache_clear()
    connection_terms, metric_terms = stencil.build_stencil()

    A0 = aggregate(connection_terms, 96)
    A1 = aggregate(connection_terms, 96, moment_axis=1)
    Q0 = aggregate(metric_terms, 40)
    Q1 = aggregate(metric_terms, 40, moment_axis=1)
    connection_block = A0.col_join(sp.zeros(40, 96))
    joint = A0.col_join(Q0)
    check("LIMIT_CONNECTION_RANK_72", exact_rank(A0) == 72)
    check("LIMIT_JOINT_BASE_RANK_79", exact_rank(joint) == 79)

    # Use the complete kernel of the 136-row flat joint system. This grants
    # every center drift, including directions not present at finite t.
    kernel = joint.nullspace()
    centers = sp.Matrix.hstack(*kernel) if kernel else sp.zeros(96, 0)
    check(
        "COMPLETE_LIMIT_CENTER_KERNEL",
        centers.shape == (96, 17)
        and exact_rank(centers) == 17
        and joint * centers == sp.zeros(136, 17),
    )

    drift = A1.col_join(Q1) * centers
    first_slow = joint.row_join(drift)

    H = base.H
    slope = base.PROFILE_SLOPE

    def solder(site):
        out = sp.eye(4)
        out[2, 2] = out[3, 3] = 1 + H * site[1] * slope
        return out

    logs = [sp.zeros(4) for _ in range(4)]
    logs[2] = -slope * owner.GEN[3]
    logs[3] = -slope * owner.GEN[4]
    wave = [U, owner.I4, owner.linv(U), owner.I4]

    def smooth_link(_site, role):
        return sp.eye(4) + H * logs[role]

    def candidate_link(site, role):
        return smooth_link(site, role) * (
            wave[sum(site) % 4] if role == 0 else owner.I4
        )

    rhs = -base.source_vector(candidate_link, solder)
    check("LIMIT_SOURCE_NONZERO", rhs != sp.zeros(136, 1))
    check("ALL_CENTER_SLOPES_INCLUDED", first_slow.shape == (136, 113))
    check(
        "LIMIT_FIRSTSLOW_RANKS_96_TO_97",
        exact_rank(first_slow) == 96
        and exact_rank(first_slow.row_join(rhs)) == 97,
    )
    print("LIMIT_LINK", U)
    print("LIMIT_BASE_KERNEL_DIMENSION", centers.cols)
    print("LIMIT_FIRSTSLOW_SHAPE", first_slow.shape)
    print("LIMIT_FIRSTSLOW_RANKS", 96, 97)
    print("TERMINAL A4D-Y232-INFINITE-AMPLITUDE-NO-REGULAR-FIRSTSLOW-LIFT")


if __name__ == "__main__":
    main()
