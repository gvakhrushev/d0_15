#!/usr/bin/env python3
"""Exact real-amplitude classification for the designated #232 first-slow lift.

The SymPy-only generic checker supplies the exact polynomial system.  This
second stage uses python-flint for a fraction-free polynomial minor and exact
linear algebra over Q[t]/(F_26).  The latter field check decides all conjugate
roots of the irreducible exceptional factor at once.

Optional exact-arithmetic dependency: python-flint==0.6.0.  See
requirements-a4d-flint.txt in this directory.
"""
from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path

import sympy as sp
from sympy.polys.domains import QQ
from sympy.polys.matrices import DomainMatrix

try:
    from flint import fmpq, fmpq_poly, fmpz_poly
except ImportError as exc:  # pragma: no cover - environment-specific guidance
    raise SystemExit(
        "Install optional certificate dependency python-flint==0.6.0 "
        "from requirements-a4d-flint.txt"
    ) from exc


HERE = Path(__file__).resolve().parent
GENERIC_CHECK = HERE / "a4d_y232_designated_warp_amplitude_generic_check.py"


def check(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name, flush=True)


def load_generic():
    spec = importlib.util.spec_from_file_location("y232_generic_amplitude", GENERIC_CHECK)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def polynomial_minor_det(minor: sp.MatrixBase, variable) -> tuple[fmpz_poly, int, list[int], list[int]]:
    """Compute an exact polynomial determinant by Bareiss over Z[t]."""
    polynomials = [
        [sp.Poly(minor[i, j], variable) for j in range(minor.cols)]
        for i in range(minor.rows)
    ]
    denominator_lcm = 1
    for row in polynomials:
        for polynomial in row:
            for coefficient in polynomial.all_coeffs():
                denominator_lcm = sp.ilcm(
                    denominator_lcm, int(sp.denom(coefficient))
                )

    matrix = [
        [
            fmpz_poly(
                [int(coefficient * denominator_lcm) for coefficient in reversed(poly.all_coeffs())]
            )
            for poly in row
        ]
        for row in polynomials
    ]
    n = minor.rows
    check("SELECTED_MINOR_SQUARE_98", (n, minor.cols) == (98, 98))
    previous = fmpz_poly(1)
    sign = 1
    exact_divisions = 0
    for column in range(n - 1):
        pivot_row = next(
            (row for row in range(column, n) if matrix[row][column] != 0), None
        )
        if pivot_row is None:
            return fmpz_poly(0), denominator_lcm, [], []
        if pivot_row != column:
            matrix[column], matrix[pivot_row] = matrix[pivot_row], matrix[column]
            sign = -sign
        pivot = matrix[column][column]
        for row in range(column + 1, n):
            below = matrix[row][column]
            for col in range(column + 1, n):
                numerator = matrix[row][col] * pivot - below * matrix[column][col]
                quotient, remainder = divmod(numerator, previous)
                if remainder != 0:
                    raise ArithmeticError((column, row, col, remainder))
                exact_divisions += 1
                matrix[row][col] = quotient
            matrix[row][column] = fmpz_poly(0)
        previous = pivot
        if (column + 1) % 10 == 0:
            print(f"BAREISS_STEP_{column + 1}", flush=True)
    check("ALL_BAREISS_DIVISIONS_EXACT", exact_divisions > 0)
    return sign * matrix[-1][-1], denominator_lcm, [], []


def fmpq_polynomial(expression, variable) -> fmpq_poly:
    polynomial = sp.Poly(expression, variable)
    coefficients = []
    for coefficient in reversed(polynomial.all_coeffs()):
        rational = sp.Rational(coefficient)
        coefficients.append(fmpq(int(rational.p), int(rational.q)))
    return fmpq_poly(coefficients)


def rank_over_number_field(matrix: sp.MatrixBase, modulus: fmpq_poly, variable) -> int:
    """Gaussian rank in the exact field Q[t]/(modulus), with irreducible modulus."""
    rows, cols = matrix.shape
    values = [
        [fmpq_polynomial(matrix[row, col], variable) % modulus for col in range(cols)]
        for row in range(rows)
    ]
    rank = 0
    for col in range(cols):
        pivot_row = next(
            (row for row in range(rank, rows) if values[row][col] != 0), None
        )
        if pivot_row is None:
            continue
        if pivot_row != rank:
            values[rank], values[pivot_row] = values[pivot_row], values[rank]
        pivot = values[rank][col]
        gcd, inverse, _ = pivot.xgcd(modulus)
        if gcd != 1:
            raise ArithmeticError(("nonunit pivot", rank, gcd))
        inverse %= modulus
        for j in range(col, cols):
            values[rank][j] = (values[rank][j] * inverse) % modulus
        for row in range(rank + 1, rows):
            factor = values[row][col]
            if factor == 0:
                continue
            for j in range(col + 1, cols):
                values[row][j] = (values[row][j] - factor * values[rank][j]) % modulus
            values[row][col] = fmpq_poly(0)
        rank += 1
        if rank == rows:
            break
    return rank


def main() -> None:
    generic_sha = hashlib.sha256(GENERIC_CHECK.read_bytes()).hexdigest()
    check(
        "PINNED_GENERIC_CHECK_SHA256",
        generic_sha == "8d234c28cc734d4f8dcafd56255ebdbbe550ec878b09a61721ba4e8507aae66c",
    )
    generic = load_generic()
    matrix, rhs, samples = generic.exact_polynomial_system()
    variable = generic.t
    generic_matrix_rank = DomainMatrix.from_Matrix(matrix).convert_to(
        QQ.poly_ring(variable)
    ).to_field().rank()
    generic_augmented_rank = DomainMatrix.from_Matrix(matrix.row_join(rhs)).convert_to(
        QQ.poly_ring(variable)
    ).to_field().rank()
    check(
        "GLOBAL_GENERIC_RANKS_97_TO_98",
        (generic_matrix_rank, generic_augmented_rank) == (97, 98),
    )

    # A necessary condition for a compatible source is vanishing of this
    # 98x98 augmented minor.  Its row/column pivots are selected exactly at
    # t=1, where the established augmented rank is 98.
    sample_one = samples[1]
    amplitude, matrix_one, rhs_one, _A0 = sample_one
    check("FIRST_CONTROL_AMPLITUDE_ONE", amplitude == 1)
    augmented_one = matrix_one.row_join(rhs_one)
    domain_one = DomainMatrix.from_Matrix(augmented_one).convert_to(QQ)
    _, column_pivots = domain_one.rref()
    _, row_pivots = domain_one.transpose().rref()
    check("AUGMENTED_PIVOT_COUNTS_AT_ONE", (len(row_pivots), len(column_pivots)) == (98, 98))
    check("SELECTED_MINOR_INCLUDES_SOURCE", 98 in column_pivots[:98])
    selected_minor = matrix.row_join(rhs).extract(
        list(row_pivots[:98]), list(column_pivots[:98])
    )
    determinant, denominator_lcm, _, _ = polynomial_minor_det(selected_minor, variable)
    check("SELECTED_MINOR_NONZERO_AT_ONE", determinant(1) != 0)
    check("SELECTED_MINOR_DEGREE_746", determinant.degree() == 746)
    print("SELECTED_MINOR_PIVOT_ROWS", list(row_pivots[:98]))
    print("SELECTED_MINOR_PIVOT_COLUMNS", list(column_pivots[:98]))
    print("SELECTED_MINOR_CLEARING_DENOMINATOR", denominator_lcm)

    x_poly = fmpz_poly([0, 1])
    exceptional = fmpz_poly([
        264241152, 0, 2204368896, 0, 8667824128, -2359296,
        20294336512, -14352384, 29726969856, -36716544,
        25823442432, -51904512, 8954889984, -40421376,
        -6051278880, -15614208, -8560584792, -2239488,
        -3595282200, 0, -82574559, 0, 398935044, 0,
        107351082, 0, 6377292,
    ])
    D_poly = fmpz_poly([4, 0, 3])
    unit, factors = determinant.factor()
    factor_degrees = sorted((factor.degree(), multiplicity) for factor, multiplicity in factors)
    check("SELECTED_MINOR_FACTORIZATION_SHAPE", factor_degrees == [(1, 24), (2, 348), (26, 1)])
    check("SELECTED_MINOR_LINEAR_FACTOR", any(factor == x_poly and mult == 24 for factor, mult in factors))
    check("SELECTED_MINOR_LAPSE_FACTOR", any(factor == D_poly and mult == 348 for factor, mult in factors))
    check("SELECTED_MINOR_EXCEPTIONAL_FACTOR", any(factor == exceptional and mult == 1 for factor, mult in factors))
    print("SELECTED_MINOR_UNIT", unit)

    exceptional_expr = sum(
        sp.Integer(coefficient) * variable**degree
        for degree, coefficient in enumerate(exceptional.coeffs())
    )
    exceptional_poly = sp.Poly(exceptional_expr, variable)
    content, irreducible_factors = sp.factor_list(exceptional_poly)
    check("EXCEPTIONAL_FACTOR_IRREDUCIBLE_OVER_Q", content == 1 and irreducible_factors == [(exceptional_poly, 1)])
    intervals = exceptional_poly.intervals(eps=sp.Rational(1, 10**8))
    check("EXCEPTIONAL_FACTOR_HAS_EXACTLY_FOUR_REAL_ROOTS", exceptional_poly.count_roots(-sp.oo, sp.oo) == 4)
    check("FOUR_DISJOINT_REAL_ROOT_INTERVALS", len(intervals) == 4 and all(mult == 1 for _, mult in intervals))
    print("EXCEPTIONAL_REAL_ROOT_INTERVALS", intervals)
    check("LAPSE_FACTOR_HAS_NO_COMMON_ROOT", sp.gcd(exceptional_poly, sp.Poly(4 + 3 * variable**2, variable)).degree() == 0)

    # Irreducibility makes Q[t]/(F_26) a field.  Rank 98 after adjoining the
    # source means at least one 98-minor is coprime to F_26, hence nonzero at
    # every one of its four real roots (all are conjugate embeddings).
    modulus = fmpq_poly([fmpq(int(c), 1) for c in exceptional.coeffs()])
    rank_matrix = rank_over_number_field(matrix, modulus, variable)
    rank_augmented = rank_over_number_field(matrix.row_join(rhs), modulus, variable)
    check("EXCEPTIONAL_FIELD_RANKS_97_TO_98", (rank_matrix, rank_augmented) == (97, 98))

    # At t=0 the carrier disappears and the same-source right-hand side is
    # exactly zero; the equal ranks certify compatibility only for this point.
    _, zero_matrix, zero_rhs, *_ = samples[0]
    zero_rank = DomainMatrix.from_Matrix(zero_matrix).convert_to(QQ).rank()
    zero_augmented_rank = DomainMatrix.from_Matrix(zero_matrix.row_join(zero_rhs)).convert_to(QQ).rank()
    check("ZERO_AMPLITUDE_IS_COMPATIBLE", (zero_rank, zero_augmented_rank) == (90, 90) and zero_rhs == sp.zeros(136, 1))
    print("COMPATIBLE_REAL_AMPLITUDES", "t=0 only; every nonzero real amplitude is incompatible at first-slow order")
    print("TERMINAL A4D-Y232-DESIGNATED-WARP-NO-NONZERO-FIRSTSLOW-AMPLITUDE")


if __name__ == "__main__":
    main()
