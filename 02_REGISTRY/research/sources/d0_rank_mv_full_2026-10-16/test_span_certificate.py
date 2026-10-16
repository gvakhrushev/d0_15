#!/usr/bin/env python3
"""Exact checks for the full-rank source span.

The checks do not build a field velocity and do not place a native shell
operator in the span.
"""

from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import span_certificate as span


FAILURES: list[str] = []
INTERIOR = (
    (Fraction(3, 5), Fraction(1, 10)),
    (Fraction(2), Fraction(1)),
    (Fraction(4), Fraction(1)),
)


def check(name: str, condition: bool) -> None:
    print(("PASS " if condition else "FAIL ") + name)
    if not condition:
        FAILURES.append(name)


def det3(gram: list[list[Fraction]]) -> Fraction:
    (a, b, c), (d, e, f), (g, h, i) = gram
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)


def matvec(gram: list[list[Fraction]], vector: tuple[Fraction, Fraction, Fraction]) -> tuple[Fraction, Fraction, Fraction]:
    return tuple(
        sum((gram[row][col] * vector[col] for col in range(3)), Fraction(0))
        for row in range(3)
    )


def local_creators() -> list[list[list[int]]]:
    creators = []
    for axis in range(4):
        matrix = [[0 for _ in range(16)] for _ in range(16)]
        lower = (1 << axis) - 1
        for mask in range(16):
            if mask & (1 << axis):
                continue
            filled = bin(mask & lower).count("1")
            matrix[mask | (1 << axis)][mask] = 1 if filled % 2 == 0 else -1
        creators.append(matrix)
    return creators


def test_carrier() -> None:
    creators = local_creators()
    check("creator_axis0_vacuum", creators[0][1][0] == 1)
    check("creator_axis0_occupied_skipped", creators[0][0][1] == 0)
    check("creator_sign_matches_lower_bits", creators[1][3][1] == -1)
    check("car_anticommutators", span.car_anticommutators_hold())
    check("parts_symmetric_traceless", span.parts_are_symmetric_and_traceless())
    check("carrier_dimension", span.CARRIER_DIMENSION == 16)


def test_gram_polynomial() -> None:
    terms = span.gram_terms_from_operators()
    for index in range(3):
        check(f"gram_diagonal_terms_{index}", terms[index][index] == span.GRAM_DIAGONAL_TERMS)
        for other in range(3):
            if other == index:
                continue
            check(f"gram_off_terms_{index}_{other}", terms[index][other] == span.GRAM_OFF_TERMS)
    for frame_a, frame_b in INTERIOR + ((Fraction(1), Fraction(0)),):
        operators = span.operators_at(frame_a, frame_b)
        for operator in operators:
            check(
                f"operator_symmetric_traceless_{frame_a}_{frame_b}",
                span.is_symmetric(operator) and span.trace(operator) == 0,
            )
        computed = span.gram_matrix(operators)
        closed = span.gram_closed_form(frame_a, frame_b)
        check(f"gram_matches_closed_{frame_a}_{frame_b}", computed == closed)
        check(
            f"det_matches_spectrum_{frame_a}_{frame_b}",
            det3(computed) == span.gram_determinant(frame_a, frame_b),
        )
        check(
            f"positive_definite_{frame_a}_{frame_b}",
            span.gram_is_positive_definite(frame_a, frame_b) and det3(computed) > 0,
        )
        ones = (Fraction(1), Fraction(1), Fraction(1))
        transverse = (Fraction(1), Fraction(-1), Fraction(0))
        transverse_b = (Fraction(1), Fraction(1), Fraction(-2))
        check(
            f"parallel_eigenvector_{frame_a}_{frame_b}",
            matvec(closed, ones) == tuple(span.parallel_eigenvalue(frame_a, frame_b) * item for item in ones),
        )
        check(
            f"transverse_eigenvector_{frame_a}_{frame_b}",
            matvec(closed, transverse)
            == tuple(span.transverse_eigenvalue(frame_a, frame_b) * item for item in transverse),
        )
        check(
            f"transverse_eigenvector_b_{frame_a}_{frame_b}",
            matvec(closed, transverse_b)
            == tuple(span.transverse_eigenvalue(frame_a, frame_b) * item for item in transverse_b),
        )


def test_equivalence_on_frames() -> None:
    neutral = span.neutral_operator()
    pairings = span.neutral_parts_pairings()
    check("neutral_polynomial_moments", pairings == [(0, 0), (0, 0), (0, 0)])
    check("neutral_trace", span.trace(neutral) == 0)
    check("neutral_symmetric", span.is_symmetric(neutral))
    check("neutral_square", span.trace_product(neutral, neutral) == Fraction(15, 16))
    check("neutral_not_zero", not span.is_zero(neutral))
    image = span.ray_on_integer_difference(neutral)
    expected = [Fraction(0) for _ in range(16)]
    expected[span.MASK_CHI_PLUS] = Fraction(15, 16)
    expected[span.MASK_CHI_MINUS] = Fraction(-15, 16)
    check("neutral_ray_is_not_span_test", image == expected)

    for frame_a, frame_b in INTERIOR:
        operators = span.operators_at(frame_a, frame_b)
        witness = span.witness_operator(frame_a, frame_b)
        built = span.span_combination(Fraction(span.WITNESS_SHIFT), span.WITNESS_BETA, operators)
        check(f"witness_in_span_{frame_a}_{frame_b}", span.matrices_equal(witness, built))
        shift, beta, residual = span.remainder(witness, frame_a, frame_b)
        check(
            f"witness_remainder_zero_{frame_a}_{frame_b}",
            shift == span.WITNESS_SHIFT and beta == span.WITNESS_BETA and span.is_zero(residual),
        )
        check(
            f"witness_pairs_with_admissible_zero_{frame_a}_{frame_b}",
            span.admissible_pairing(shift, beta, 0, (0, 0, 0)) == 0,
        )
        check(
            f"witness_neutral_pairing_{frame_a}_{frame_b}",
            span.trace_product(neutral, witness) == 0,
        )
        out_shift, out_beta, out_residual = span.remainder(neutral, frame_a, frame_b)
        check(
            f"negative_control_outside_{frame_a}_{frame_b}",
            out_shift == 0
            and out_beta == (0, 0, 0)
            and span.matrices_equal(out_residual, neutral)
            and span.trace_product(out_residual, neutral) == Fraction(15, 16),
        )
        for operator in operators:
            check(
                f"negative_control_admissible_{frame_a}_{frame_b}",
                span.trace_product(operator, neutral) == 0,
            )
        count = span.hermitian_basis_splits(frame_a, frame_b)
        check(f"hermitian_basis_split_{frame_a}_{frame_b}", count == 16 * 16)


def test_singular_boundary() -> None:
    check("equal_frame_sum_vanishes", span.singular_parts_sum_to_zero())
    check("equal_frame_not_positive", not span.gram_is_positive_definite(1, 1))
    check("equal_frame_det_zero", span.gram_determinant(1, 1) == 0)
    operators = span.operators_at(1, 1)
    total = span.zeros()
    for operator in operators:
        for row in range(16):
            for col in range(16):
                total[row][col] += operator[row][col]
    check("equal_frame_operator_sum", span.is_zero(total))
    raised = False
    try:
        span.remainder(span.neutral_operator(), 1, 1)
    except ZeroDivisionError:
        raised = True
    check("equal_frame_inverse_undefined", raised)
    # On the dependent frame the first two operators still span the image.
    left = span.gram_matrix(operators)[0][0]
    off = span.gram_matrix(operators)[0][1]
    gram2 = [[left, off], [off, left]]
    det = gram2[0][0] * gram2[1][1] - gram2[0][1] * gram2[1][0]
    neutral = span.neutral_operator()
    moments = (
        span.trace_product(operators[0], neutral),
        span.trace_product(operators[1], neutral),
    )
    check("equal_frame_reduced_gram", det == 192 * 64 and det > 0 and moments == (0, 0))
    witness = span.witness_operator(1, 1)
    check(
        "equal_frame_witness_still_combination",
        span.matrices_equal(
            witness,
            span.span_combination(Fraction(3), span.WITNESS_BETA, operators),
        ),
    )


def test_result_language() -> None:
    text = (Path(__file__).resolve().parent / "RESULT_RU.md").read_text(encoding="utf-8")
    required = (
        "кандидат",
        span.SOURCE_PIN,
        "15/16",
        "32768",
        "A>B>0",
        "не вычисляется",
        "claims.csv",
        "(27)",
        "B_1+B_2+B_3=0",
    )
    for phrase in required:
        check(f"result_has_{phrase}", phrase in text)
    for phrase in ("GR is derived", "ОТО выведена", "ОТО получена", "полевая скорость вычислена"):
        check(f"result_without_{phrase}", phrase not in text)
    check(
        "limits_not_a_native_membership",
        "native" in text and "Не утверждается" in text and "уже лежит" in text,
    )


def main() -> int:
    test_carrier()
    test_gram_polynomial()
    test_equivalence_on_frames()
    test_singular_boundary()
    test_result_language()
    if FAILURES:
        print("FAILED " + ", ".join(FAILURES))
        return 1
    print("ALL_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
