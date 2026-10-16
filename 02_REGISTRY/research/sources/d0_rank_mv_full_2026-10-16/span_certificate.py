#!/usr/bin/env python3
"""Exact span certificate for the memo source operators B_r.

J_r in WRK-A4D-MV-FULL-RANK-SPAN are these B_r, read from pin
ec45c8cc4085e7bce888d97439251be9e578d4ff. The operators are rebuilt here.
That pin is not merged.

No field velocity is formed, and no native shell operator is placed in the span.
"""

from __future__ import annotations

from fractions import Fraction

SOURCE_PIN = "ec45c8cc4085e7bce888d97439251be9e578d4ff"
MEMO_SHA256 = "8ec54e4838aaa579469896eeaf369e16a24d6a6f0f67824ede6fa88f5cb9b622"
CARRIER_DIMENSION = 16
WITNESS_SHIFT = 3
WITNESS_BETA = (Fraction(1), Fraction(2), Fraction(-1))
MASK_CHI_PLUS = 1
MASK_CHI_MINUS = 15

# Closed Gram of (B_1, B_2, B_3), coefficients of (A^2, A*B, B^2).
# Diagonal 32 A^2 + 96 B^2, off-diagonal -32 A B - 32 B^2.
GRAM_DIAGONAL_TERMS = (32, 0, 96)
GRAM_OFF_TERMS = (0, -32, -32)


def as_fraction(value: Fraction | int) -> Fraction:
    if isinstance(value, Fraction):
        return value
    return Fraction(value)


def zeros() -> list[list[Fraction]]:
    return [[Fraction(0) for _ in range(CARRIER_DIMENSION)] for _ in range(CARRIER_DIMENSION)]


def eye() -> list[list[Fraction]]:
    matrix = zeros()
    for index in range(CARRIER_DIMENSION):
        matrix[index][index] = Fraction(1)
    return matrix


def creator_matrices() -> list[list[list[int]]]:
    """Exterior creators on masks 0..15. Sign is the parity of lower bits."""
    creators = []
    for axis in range(4):
        matrix = [[0 for _ in range(CARRIER_DIMENSION)] for _ in range(CARRIER_DIMENSION)]
        lower = (1 << axis) - 1
        for mask in range(CARRIER_DIMENSION):
            if mask & (1 << axis):
                continue
            sign = 1 if bin(mask & lower).count("1") % 2 == 0 else -1
            matrix[mask | (1 << axis)][mask] = sign
        creators.append(matrix)
    return creators


def _transpose_int(matrix: list[list[int]]) -> list[list[int]]:
    return [[matrix[row][col] for row in range(CARRIER_DIMENSION)] for col in range(CARRIER_DIMENSION)]


def _matmul_int(left: list[list[int]], right: list[list[int]]) -> list[list[int]]:
    product = [[0 for _ in range(CARRIER_DIMENSION)] for _ in range(CARRIER_DIMENSION)]
    for row in range(CARRIER_DIMENSION):
        for mid in range(CARRIER_DIMENSION):
            scale = left[row][mid]
            if scale == 0:
                continue
            right_row = right[mid]
            out = product[row]
            for col in range(CARRIER_DIMENSION):
                if right_row[col]:
                    out[col] += scale * right_row[col]
    return product


def _add_int(
    left: list[list[int]],
    right: list[list[int]],
    left_scale: int = 1,
    right_scale: int = 1,
) -> list[list[int]]:
    return [
        [
            left_scale * left[row][col] + right_scale * right[row][col]
            for col in range(CARRIER_DIMENSION)
        ]
        for row in range(CARRIER_DIMENSION)
    ]


def car_anticommutators_hold() -> bool:
    creators = creator_matrices()
    annihilators = [_transpose_int(matrix) for matrix in creators]
    for left in range(4):
        for right in range(4):
            total = _add_int(
                _matmul_int(creators[left], annihilators[right]),
                _matmul_int(annihilators[right], creators[left]),
            )
            for row in range(CARRIER_DIMENSION):
                for col in range(CARRIER_DIMENSION):
                    expected = 1 if left == right and row == col else 0
                    if total[row][col] != expected:
                        return False
    return True


def _gamma_kappa() -> tuple[list[list[list[int]]], list[list[list[int]]]]:
    creators = creator_matrices()
    annihilators = [_transpose_int(matrix) for matrix in creators]
    gamma = [_add_int(creators[axis], annihilators[axis], 1, 1) for axis in range(4)]
    kappa = [_add_int(creators[axis], annihilators[axis], 1, -1) for axis in range(4)]
    return gamma, kappa


def _combine_int(operators: list[list[list[int]]], coeffs: list[int]) -> list[list[int]]:
    matrix = [[0 for _ in range(CARRIER_DIMENSION)] for _ in range(CARRIER_DIMENSION)]
    for coeff, operator in zip(coeffs, operators):
        if coeff == 0:
            continue
        for row in range(CARRIER_DIMENSION):
            for col in range(CARRIER_DIMENSION):
                matrix[row][col] += coeff * operator[row][col]
    return matrix


def operator_parts() -> list[tuple[list[list[int]], list[list[int]]]]:
    """B_r = A P_r + B Q_r for spatial rows r = 1, 2, 3.

    a_1, a_2, a_3 and the row pairing are the memo's source frame, not a new operator.
    """
    gamma, kappa = _gamma_kappa()
    axes = ((0, 0, -1, 1), (0, 1, 0, -1), (0, -1, 1, 0))
    spatial_rows = (1, 2, 3)
    summed = kappa[0]
    for axis in range(1, 4):
        summed = _add_int(summed, kappa[axis])
    parts = []
    for coeffs, row in zip(axes, spatial_rows):
        gamma_a = _combine_int(gamma, list(coeffs))
        along = kappa[row]
        across = _add_int(summed, kappa[row], 1, -1)
        parts.append((_matmul_int(gamma_a, along), _matmul_int(gamma_a, across)))
    return parts


def operators_at(frame_a: Fraction | int, frame_b: Fraction | int) -> list[list[list[Fraction]]]:
    frame_a = as_fraction(frame_a)
    frame_b = as_fraction(frame_b)
    materialized = []
    for along, across in operator_parts():
        matrix = zeros()
        for row in range(CARRIER_DIMENSION):
            for col in range(CARRIER_DIMENSION):
                matrix[row][col] = frame_a * along[row][col] + frame_b * across[row][col]
        materialized.append(matrix)
    return materialized


def trace(matrix: list[list[Fraction]]) -> Fraction:
    return sum(matrix[index][index] for index in range(len(matrix)))


def trace_product(left: list[list[Fraction]], right: list[list[Fraction]]) -> Fraction:
    total = Fraction(0)
    for row in range(CARRIER_DIMENSION):
        left_row = left[row]
        for col in range(CARRIER_DIMENSION):
            scale = left_row[col]
            if scale:
                total += scale * right[col][row]
    return total


def frobenius_square(matrix: list[list[Fraction]]) -> Fraction:
    return sum(entry * entry for row in matrix for entry in row)


def is_symmetric(matrix: list[list[Fraction]]) -> bool:
    for row in range(CARRIER_DIMENSION):
        for col in range(row + 1, CARRIER_DIMENSION):
            if matrix[row][col] != matrix[col][row]:
                return False
    return True


def is_zero(matrix: list[list[Fraction]]) -> bool:
    return all(entry == 0 for row in matrix for entry in row)


def matrices_equal(left: list[list[Fraction]], right: list[list[Fraction]]) -> bool:
    for row in range(CARRIER_DIMENSION):
        for col in range(CARRIER_DIMENSION):
            if left[row][col] != right[row][col]:
                return False
    return True


def _add(left: list[list[Fraction]], right: list[list[Fraction]]) -> list[list[Fraction]]:
    return [
        [left[row][col] + right[row][col] for col in range(CARRIER_DIMENSION)]
        for row in range(CARRIER_DIMENSION)
    ]


def gram_matrix(operators: list[list[list[Fraction]]]) -> list[list[Fraction]]:
    return [
        [trace_product(operators[row], operators[col]) for col in range(3)]
        for row in range(3)
    ]


def _quadratic(terms: tuple[int, int, int], frame_a: Fraction, frame_b: Fraction) -> Fraction:
    aa, ab, bb = terms
    return aa * frame_a * frame_a + ab * frame_a * frame_b + bb * frame_b * frame_b


def gram_closed_form(frame_a: Fraction | int, frame_b: Fraction | int) -> list[list[Fraction]]:
    frame_a = as_fraction(frame_a)
    frame_b = as_fraction(frame_b)
    diagonal = _quadratic(GRAM_DIAGONAL_TERMS, frame_a, frame_b)
    off = _quadratic(GRAM_OFF_TERMS, frame_a, frame_b)
    return [
        [diagonal, off, off],
        [off, diagonal, off],
        [off, off, diagonal],
    ]


def gram_terms_from_operators() -> list[list[tuple[int, int, int]]]:
    """Return Tr(B_r B_s) as coefficients of A^2, AB, B^2."""
    parts = operator_parts()

    def tr_int(left: list[list[int]], right: list[list[int]]) -> int:
        total = 0
        for row in range(CARRIER_DIMENSION):
            for col in range(CARRIER_DIMENSION):
                scale = left[row][col]
                if scale:
                    total += scale * right[col][row]
        return total

    terms: list[list[tuple[int, int, int]]] = []
    for row_along, row_across in parts:
        row_terms = []
        for col_along, col_across in parts:
            aa = tr_int(row_along, col_along)
            ab = tr_int(row_along, col_across) + tr_int(row_across, col_along)
            bb = tr_int(row_across, col_across)
            row_terms.append((aa, ab, bb))
        terms.append(row_terms)
    return terms


def parallel_eigenvalue(frame_a: Fraction | int, frame_b: Fraction | int) -> Fraction:
    frame_a = as_fraction(frame_a)
    frame_b = as_fraction(frame_b)
    return 32 * (frame_a - frame_b) * (frame_a - frame_b)


def transverse_eigenvalue(frame_a: Fraction | int, frame_b: Fraction | int) -> Fraction:
    frame_a = as_fraction(frame_a)
    frame_b = as_fraction(frame_b)
    quad = frame_a * frame_a + frame_a * frame_b + 4 * frame_b * frame_b
    return 32 * quad


def gram_determinant(frame_a: Fraction | int, frame_b: Fraction | int) -> Fraction:
    parallel = parallel_eigenvalue(frame_a, frame_b)
    transverse = transverse_eigenvalue(frame_a, frame_b)
    return parallel * transverse * transverse


def gram_is_positive_definite(frame_a: Fraction | int, frame_b: Fraction | int) -> bool:
    """True exactly on A ≠ B. The transverse factor vanishes only at (0, 0)."""
    return as_fraction(frame_a) != as_fraction(frame_b)


def neutral_operator() -> list[list[Fraction]]:
    """|chi><chi| - I/16 for chi = (e_1 - e_15) / sqrt(2). Entries are rational."""
    matrix = zeros()
    for index in range(CARRIER_DIMENSION):
        matrix[index][index] = Fraction(-1, 16)
    matrix[MASK_CHI_PLUS][MASK_CHI_PLUS] += Fraction(1, 2)
    matrix[MASK_CHI_MINUS][MASK_CHI_MINUS] += Fraction(1, 2)
    matrix[MASK_CHI_PLUS][MASK_CHI_MINUS] = Fraction(-1, 2)
    matrix[MASK_CHI_MINUS][MASK_CHI_PLUS] = Fraction(-1, 2)
    return matrix


def neutral_parts_pairings() -> list[tuple[int, int]]:
    """Tr(neutral P_r) and Tr(neutral Q_r). Both are zero for every frame."""
    neutral = neutral_operator()
    pairings = []
    for along, across in operator_parts():
        along_trace = 0
        across_trace = 0
        for row in range(CARRIER_DIMENSION):
            for col in range(CARRIER_DIMENSION):
                weight = neutral[row][col]
                if weight:
                    along_trace += weight * along[col][row]
                    across_trace += weight * across[col][row]
        pairings.append((along_trace, across_trace))
    return pairings


def parts_are_symmetric_and_traceless() -> bool:
    for along, across in operator_parts():
        if trace_int(along) != 0 or trace_int(across) != 0:
            return False
        for row in range(CARRIER_DIMENSION):
            for col in range(row + 1, CARRIER_DIMENSION):
                if along[row][col] != along[col][row] or across[row][col] != across[col][row]:
                    return False
    return True


def trace_int(matrix: list[list[int]]) -> int:
    return sum(matrix[index][index] for index in range(CARRIER_DIMENSION))


def singular_parts_sum_to_zero() -> bool:
    """A = B forces B_1 + B_2 + B_3 = 0, so the written inverse is undefined."""
    total_along = [[0 for _ in range(CARRIER_DIMENSION)] for _ in range(CARRIER_DIMENSION)]
    total_across = [[0 for _ in range(CARRIER_DIMENSION)] for _ in range(CARRIER_DIMENSION)]
    for along, across in operator_parts():
        for row in range(CARRIER_DIMENSION):
            for col in range(CARRIER_DIMENSION):
                total_along[row][col] += along[row][col]
                total_across[row][col] += across[row][col]
    for row in range(CARRIER_DIMENSION):
        for col in range(CARRIER_DIMENSION):
            if total_along[row][col] + total_across[row][col] != 0:
                return False
    # The sum is zero on A = B, but the operators are not identically zero.
    return any(
        along[row][col] != 0
        for along, _across in operator_parts()
        for row in range(CARRIER_DIMENSION)
        for col in range(CARRIER_DIMENSION)
    )


def invert3(gram: list[list[Fraction]]) -> list[list[Fraction]]:
    augmented = [
        [gram[row][col] for col in range(3)]
        + [Fraction(1 if row == col else 0) for col in range(3)]
        for row in range(3)
    ]
    for col in range(3):
        candidates = [row for row in range(col, 3) if augmented[row][col] != 0]
        if not candidates:
            raise ZeroDivisionError("singular source Gram")
        pivot = candidates[0]
        if pivot != col:
            augmented[col], augmented[pivot] = augmented[pivot], augmented[col]
        scale = augmented[col][col]
        if scale == 0:
            raise ZeroDivisionError("singular source Gram")
        for index in range(6):
            augmented[col][index] /= scale
        for row in range(3):
            if row == col:
                continue
            factor = augmented[row][col]
            if factor == 0:
                continue
            for index in range(6):
                augmented[row][index] -= factor * augmented[col][index]
    return [row[3:] for row in augmented]


def _matvec3(matrix: list[list[Fraction]], vector: tuple[Fraction, Fraction, Fraction]) -> tuple[Fraction, Fraction, Fraction]:
    return tuple(
        sum(matrix[row][col] * vector[col] for col in range(3))
        for row in range(3)
    )


def span_combination(
    shift: Fraction,
    beta: tuple[Fraction, Fraction, Fraction],
    operators: list[list[list[Fraction]]],
) -> list[list[Fraction]]:
    matrix = zeros()
    for index in range(CARRIER_DIMENSION):
        matrix[index][index] = shift
    for coeff, operator in zip(beta, operators):
        if coeff == 0:
            continue
        for row in range(CARRIER_DIMENSION):
            for col in range(CARRIER_DIMENSION):
                matrix[row][col] += coeff * operator[row][col]
    return matrix


def witness_operator(frame_a: Fraction | int, frame_b: Fraction | int) -> list[list[Fraction]]:
    return span_combination(
        Fraction(WITNESS_SHIFT),
        WITNESS_BETA,
        operators_at(frame_a, frame_b),
    )


def remainder(
    hermitian: list[list[Fraction]],
    frame_a: Fraction | int,
    frame_b: Fraction | int,
) -> tuple[Fraction, tuple[Fraction, Fraction, Fraction], list[list[Fraction]]]:
    """Formula (27). Requires a frame with invertible G_B, that is A ≠ B."""
    operators = operators_at(frame_a, frame_b)
    inverse = invert3(gram_matrix(operators))
    shift = trace(hermitian) / CARRIER_DIMENSION
    moments = tuple(trace_product(operator, hermitian) for operator in operators)
    beta = _matvec3(inverse, moments)
    projected = span_combination(shift, beta, operators)
    residual = zeros()
    for row in range(CARRIER_DIMENSION):
        for col in range(CARRIER_DIMENSION):
            residual[row][col] = hermitian[row][col] - projected[row][col]
    return shift, beta, residual


def admissible_pairing(
    shift: Fraction,
    beta: tuple[Fraction, Fraction, Fraction],
    trace_s: Fraction,
    source_moments: tuple[Fraction, Fraction, Fraction],
) -> Fraction:
    """Tr(S (shift I + sum beta_r B_r)) reduced by linearity. No matrix is built."""
    return shift * trace_s + sum(coeff * moment for coeff, moment in zip(beta, source_moments))


def ray_on_integer_difference(neutral: list[list[Fraction]]) -> list[Fraction]:
    """neutral (e_1 - e_15) as a rational vector. This is not a field velocity."""
    vector = [Fraction(0) for _ in range(CARRIER_DIMENSION)]
    vector[MASK_CHI_PLUS] = Fraction(1)
    vector[MASK_CHI_MINUS] = Fraction(-1)
    return [
        sum(neutral[row][col] * vector[col] for col in range(CARRIER_DIMENSION))
        for row in range(CARRIER_DIMENSION)
    ]


def hermitian_basis_splits(frame_a: Fraction | int, frame_b: Fraction | int) -> int:
    """Check formula (27) on a real basis of all 16×16 Hermitian matrices.

    Real diagonal, real off-diagonal and imaginary off-diagonal directions are
    included. This is the coordinate basis, not an enumeration of preparations.
    """
    operators = operators_at(frame_a, frame_b)
    inverse = invert3(gram_matrix(operators))
    checked = 0

    def split_real(symmetric: list[list[Fraction]]) -> None:
        nonlocal checked
        shift = trace(symmetric) / CARRIER_DIMENSION
        moments = tuple(trace_product(operator, symmetric) for operator in operators)
        beta = _matvec3(inverse, moments)
        projected = span_combination(shift, beta, operators)
        residual = zeros()
        for row in range(CARRIER_DIMENSION):
            for col in range(CARRIER_DIMENSION):
                residual[row][col] = symmetric[row][col] - projected[row][col]
        if trace(residual) != 0:
            raise ArithmeticError("residual trace")
        for operator in operators:
            if trace_product(operator, residual) != 0:
                raise ArithmeticError("residual source moment")
        if not matrices_equal(_add(projected, residual), symmetric):
            raise ArithmeticError("basis split")
        if trace_product(residual, symmetric) != trace_product(residual, residual):
            raise ArithmeticError("residual pairing")
        if trace_product(residual, residual) != frobenius_square(residual):
            raise ArithmeticError("residual norm")
        checked += 1

    for index in range(CARRIER_DIMENSION):
        basis = zeros()
        basis[index][index] = Fraction(1)
        split_real(basis)
    for row in range(CARRIER_DIMENSION):
        for col in range(row + 1, CARRIER_DIMENSION):
            symmetric = zeros()
            symmetric[row][col] = Fraction(1)
            symmetric[col][row] = Fraction(1)
            split_real(symmetric)
            skew = zeros()
            skew[row][col] = Fraction(1)
            skew[col][row] = Fraction(-1)
            # A purely imaginary Hermitian matrix is orthogonal to every real
            # symmetric operator, so its real projection is zero.
            if any(trace_product(operator, skew) != 0 for operator in operators):
                raise ArithmeticError("imaginary source moment")
            if trace(skew) != 0:
                raise ArithmeticError("imaginary trace")
            if frobenius_square(skew) == 0:
                raise ArithmeticError("imaginary zero")
            if trace_product(skew, skew) != -frobenius_square(skew):
                raise ArithmeticError("imaginary square")
            checked += 1
    return checked
