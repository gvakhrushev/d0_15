#!/usr/bin/env python3
"""Exact Laurent-jet obstruction near zero amplitude on the designated #232 warp.

This checks the polynomial first-slow system M(t)x=b(t) already owned by
a4d_y232_designated_warp_amplitude_generic_check.py. It allows every link
correction and both center slopes, then permits Laurent poles through t^-2.
The result is a finite formal-amplitude statement only.
"""
from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path

import sympy as sp
from sympy.polys.domains import QQ
from sympy.polys.matrices import DomainMatrix

HERE = Path(__file__).resolve().parent
GENERIC_CHECK = HERE / "a4d_y232_designated_warp_amplitude_generic_check.py"
EXPECTED_GENERIC_SHA256 = "8d234c28cc734d4f8dcafd56255ebdbbe550ec878b09a61721ba4e8507aae66c"


def check(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name, flush=True)


def load_generic():
    spec = importlib.util.spec_from_file_location(
        "y232_laurent_generic_amplitude", GENERIC_CHECK
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def coefficient_matrix(matrix: sp.MatrixBase, variable, degree: int) -> sp.Matrix:
    return matrix.applyfunc(lambda entry: sp.Poly(entry, variable).nth(degree))


def truncated_laurent_system(M, b, variable, pole_order: int, top_order: int):
    """Convolution equations for t^-pole_order ... t^top_order."""
    degrees = list(range(-pole_order, top_order + 1))
    M_coefficients = [coefficient_matrix(M, variable, i) for i in range(9)]
    b_coefficients = [coefficient_matrix(b, variable, i) for i in range(9)]
    A = sp.zeros(M.rows * len(degrees), M.cols * len(degrees))
    rhs = sp.zeros(M.rows * len(degrees), 1)

    for row_block, output_degree in enumerate(degrees):
        row_start = M.rows * row_block
        row_stop = row_start + M.rows
        if 0 <= output_degree < len(b_coefficients):
            rhs[row_start:row_stop, 0] = b_coefficients[output_degree]

        for col_block, input_degree in enumerate(degrees):
            symbol_degree = output_degree - input_degree
            if 0 <= symbol_degree < len(M_coefficients):
                col_start = M.cols * col_block
                col_stop = col_start + M.cols
                A[row_start:row_stop, col_start:col_stop] = M_coefficients[symbol_degree]

    return A, rhs


def exact_ranks(A, rhs):
    matrix_rank = DomainMatrix.from_Matrix(A).convert_to(QQ).rank()
    augmented_rank = DomainMatrix.from_Matrix(A.row_join(rhs)).convert_to(QQ).rank()
    return matrix_rank, augmented_rank


def main() -> None:
    source_sha = hashlib.sha256(GENERIC_CHECK.read_bytes()).hexdigest()
    check("PINNED_GENERIC_AMPLITUDE_OWNER", source_sha == EXPECTED_GENERIC_SHA256)

    generic = load_generic()
    M, b, _samples = generic.exact_polynomial_system()
    check("FULL_FIRSTSLOW_SYSTEM_SHAPE", M.shape == (136, 98))
    check("ZERO_AMPLITUDE_SOURCE", coefficient_matrix(b, generic.t, 0) == sp.zeros(136, 1))

    # A correction with pole order <= 2 is embedded by zero coefficients into
    # this four-block unknown vector. Matching through t^0 is possible, but
    # matching the first t coefficient is not.
    A0, rhs0 = truncated_laurent_system(M, b, generic.t, pole_order=2, top_order=0)
    A1, rhs1 = truncated_laurent_system(M, b, generic.t, pole_order=2, top_order=1)
    check("THROUGH_T0_BLOCK_SHAPE", A0.shape == (408, 294))
    check("THROUGH_T1_BLOCK_SHAPE", A1.shape == (544, 392))
    ranks0 = exact_ranks(A0, rhs0)
    ranks1 = exact_ranks(A1, rhs1)
    check("LAURENT_POLE2_COMPATIBLE_THROUGH_T0", ranks0 == (282, 282))
    check("LAURENT_POLE2_OBSTRUCTED_AT_T1", ranks1 == (379, 380))

    print("THROUGH_T0_RANKS", ranks0)
    print("THROUGH_T1_RANKS", ranks1)
    print("SCOPE", "first-slow Laurent corrections with pole order at most 2")
    print("RESULT LOCAL_Y232_FIRSTSLOW_LAURENT_POLE2_OBSTRUCTION")


if __name__ == "__main__":
    main()
