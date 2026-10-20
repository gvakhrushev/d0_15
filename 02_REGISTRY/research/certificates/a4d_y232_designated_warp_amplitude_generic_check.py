#!/usr/bin/env python3
"""Generic-amplitude exact rank test for the designated #232 first-slow lift.

This extends the pinned t=1 same-source system to the entire real Cayley
parameter t.  After multiplying every row by D(t)^4, D=4+3t^2, all entries
are polynomials of degree at most eight: every local Euler coefficient is a
sum of products with at most four Cayley-link factors.  Nine exact samples
therefore reconstruct the polynomial matrix exactly.  The calculation proves
generic incompatibility and finiteness of possible exceptional amplitudes; it
does not isolate those amplitudes, and t=0 is a known compatible zero-carrier
exception.
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


BASE = load_module("y232_amplitude_base", BASE_CHECK)
ST = BASE.ST
OWNER = BASE.OWNER
H = BASE.H
I4 = OWNER.I4
GEN = OWNER.GEN
PROFILE_SLOPE = BASE.PROFILE_SLOPE
RING = QQ.poly_ring(sp.Symbol("t", real=True))
t = RING.symbols[0]


def cayley_fraction(amplitude: int):
    a = ST.F(amplitude)
    denominator = ST.F(4) + ST.F(3) * a * a
    return ST.madd(
        ST.eye(),
        ST.madd(
            ST.mscale(ST.F(4) * a / denominator, ST.Y),
            ST.mscale(ST.F(2) * a * a / denominator, ST.Y2),
        ),
    )


def stencil_at(amplitude: int):
    U = cayley_fraction(amplitude)
    ST.W = (U, ST.I4, ST.linv(U), ST.I4)
    ST.build_stencil.cache_clear()
    return ST.build_stencil()


def aggregate(terms, row_count: int, moment_axis: int | None = None):
    matrix = sp.zeros(row_count, 96)
    for shift, entries in terms.items():
        weight = 1 if moment_axis is None else shift[moment_axis]
        if not weight:
            continue
        for (row, col), value in entries.items():
            matrix[row, col] += weight * sp.Rational(value.numerator, value.denominator)
    return matrix


def coframe_and_links(amplitude: int):
    Y = GEN[3] - GEN[4] + GEN[5]
    U = OWNER.cayley_simple(Y, 3, sp.Integer(amplitude))
    wave = [U, I4, OWNER.linv(U), I4]
    smooth_log = [sp.zeros(4) for _ in range(4)]
    smooth_log[2] = -PROFILE_SLOPE * GEN[3]
    smooth_log[3] = -PROFILE_SLOPE * GEN[4]

    def solder(site):
        out = sp.eye(4)
        out[2, 2] = out[3, 3] = 1 + H * site[1] * PROFILE_SLOPE
        return out

    def smooth_link(_site, role):
        return sp.eye(4) + H * smooth_log[role]

    def candidate_link(site, role):
        return smooth_link(site, role) * (
            wave[sum(site) % 4] if role == 0 else I4
        )

    return solder, smooth_link, candidate_link


def center_directions():
    # The exact amplitude tangent is (4/D)Y.  Replacing it by Y only rescales
    # the corresponding unknown by D/4, which is nonzero for every real t.
    center = sp.zeros(96, 2)
    Y = GEN[3] - GEN[4] + GEN[5]
    boost_dual = GEN[0] + GEN[1] + GEN[2]
    for generator, (a, b) in enumerate(OWNER.PAIRS):
        center[ST.IDX[(0, 0, generator)], 0] = Y[a, b]
        center[ST.IDX[(2, 0, generator)], 0] = -Y[a, b]
        center[ST.IDX[(0, 0, generator)], 1] = -boost_dual[a, b]
        center[ST.IDX[(2, 0, generator)], 1] = boost_dual[a, b]
    return center


CENTERS = center_directions()


def full_system(amplitude: int):
    connection_terms, metric_terms = stencil_at(amplitude)
    A0 = aggregate(connection_terms, 96)
    A1 = aggregate(connection_terms, 96, moment_axis=1)
    Q0 = aggregate(metric_terms, 40)
    Q1 = aggregate(metric_terms, 40, moment_axis=1)
    matrix = A0.col_join(Q0).row_join(A1.col_join(Q1) * CENTERS)

    solder, smooth_link, candidate_link = coframe_and_links(amplitude)
    source = BASE.source_vector(candidate_link, solder)
    return matrix, -source, A0


def interpolate(values, inverse_vandermonde):
    coefficients = [
        sum(inverse_vandermonde[j, i] * values[i] for i in range(9))
        for j in range(9)
    ]
    return sp.Poly.from_list(list(reversed(coefficients)), gens=t).as_expr()


def exact_polynomial_system():
    smooth_solder, smooth_link, _candidate_link = coframe_and_links(0)
    smooth_source = BASE.source_vector(smooth_link, smooth_solder)
    check("DESIGNATED_SMOOTH_SOURCE_ZERO", smooth_source == sp.zeros(136, 1))

    samples = []
    for amplitude in range(9):
        matrix, rhs, A0 = full_system(amplitude)
        D = 4 + 3 * amplitude * amplitude
        samples.append((amplitude, matrix * D**4, rhs * D**4, A0))
        check(f"SAMPLE_{amplitude}_CENTER_KERNEL", A0 * CENTERS == sp.zeros(96, 2))

    check("ZERO_CARRIER_SOURCE", samples[0][2] == sp.zeros(136, 1))
    V = sp.Matrix([[amplitude**j for j in range(9)] for amplitude in range(9)])
    inverse_vandermonde = V.inv()
    rows, cols = samples[0][1].shape
    matrix = sp.MutableDenseMatrix(
        rows,
        cols,
        lambda i, j: interpolate(
            [samples[k][1][i, j] for k in range(9)], inverse_vandermonde
        ),
    )
    rhs = sp.MutableDenseMatrix(
        rows,
        1,
        lambda i, _j: interpolate(
            [samples[k][2][i, 0] for k in range(9)], inverse_vandermonde
        ),
    )

    # A tenth exact point is a hostile replay control.  Exactness for all t
    # follows from the denominator/degree bound stated in the module docstring.
    matrix9, rhs9, _A09 = full_system(9)
    check("TENTH_POINT_MATRIX_REPLAY", matrix.subs(t, 9) == matrix9 * (4 + 3 * 9**2) ** 4)
    check("TENTH_POINT_SOURCE_REPLAY", rhs.subs(t, 9) == rhs9 * (4 + 3 * 9**2) ** 4)
    return matrix, rhs, samples


def main() -> None:
    check(
        "PINNED_FIRSTSLOW_CHECK_SHA256",
        hashlib.sha256(BASE_CHECK.read_bytes()).hexdigest()
        == "1840477790bb1549b5c09e8158e7715e3c6d546bd6ea51fa5d751f48bd5aeaf7",
    )
    check(
        "PINNED_STENCIL_SHA256",
        hashlib.sha256(STENCIL_PATH.read_bytes()).hexdigest()
        == "d4cf844b027f8cc34540c385b48922f3a5bcfc42cbedf08d5a704cfb7adb0daa",
    )
    check(
        "PINNED_OWNER_SHA256",
        hashlib.sha256(OWNER_PATH.read_bytes()).hexdigest()
        == "d85c644f22cdcd8b7c7ad63c72dd780c87af3184b4b35bf2b3e438bcde3afd21",
    )

    matrix, rhs, samples = exact_polynomial_system()
    ring_matrix = DomainMatrix.from_Matrix(matrix).convert_to(RING).to_field()
    ring_augmented = DomainMatrix.from_Matrix(matrix.row_join(rhs)).convert_to(RING).to_field()
    rank = ring_matrix.rank()
    augmented_rank = ring_augmented.rank()
    check("GENERIC_SAME_SOURCE_FIRSTSLOW_RANK_97_TO_98", (rank, augmented_rank) == (97, 98))

    # Exact specialization checks: t=0 is the zero-carrier compatible point;
    # t=1 replays the established rank obstruction; t=2 is a nontrivial new
    # amplitude control.
    for index, expected in ((0, (90, 90)), (1, (97, 98)), (2, (97, 98))):
        amplitude, matrix_value, rhs_value, *_ = samples[index]
        actual = (
            DomainMatrix.from_Matrix(matrix_value).convert_to(QQ).rank(),
            DomainMatrix.from_Matrix(matrix_value.row_join(rhs_value)).convert_to(QQ).rank(),
        )
        check(f"SPECIALIZATION_{amplitude}_RANKS", actual == expected)

    print("GENERIC_RANKS", {"matrix": rank, "augmented": augmented_rank})
    print("EXCEPTION_SET", "finite algebraic subset of R; t=0 is compatible; nonzero roots not isolated")
    print("TERMINAL A4D-Y232-DESIGNATED-WARP-GENERIC-AMPLITUDE-FIRSTSLOW-OBSTRUCTION")


if __name__ == "__main__":
    main()
