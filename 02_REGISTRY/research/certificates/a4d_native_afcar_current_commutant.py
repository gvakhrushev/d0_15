#!/usr/bin/env python3
"""Exact commutant boundary for the complete CAR current and AF record step."""
import importlib.util
import sys
from pathlib import Path

import sympy as s

ROOT = Path(__file__).resolve().parents[3]
CERT = Path("02_REGISTRY/research/certificates/a4d_native_afcar_current_commutant")


def load(stem):
    path = ROOT / "02_REGISTRY/research/certificates" / (stem + ".py")
    spec = importlib.util.spec_from_file_location(stem, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


CAR = load("a4d_native_correlated_current_transition")
FRAME = load("a4d_native_reference_memory_preparation")
AF = load("a4d_native_fibonacci_record_activation")
P_MOD, A_MOD = CAR.p, CAR.a
MODULUS = 11
I16 = s.eye(16)


def operators():
    u4, p4, b4, t = FRAME.literal_tuple()
    frame = FRAME.mat(
        FRAME.C.B0 * s.kronecker_product(t.T, s.eye(4))
    )
    record = [
        FRAME.mat(s.kronecker_product(x, s.eye(4)))
        for x in (u4, p4, b4)
    ]
    current = [
        FRAME.mat(frame.T * alpha * frame)
        for alpha in CAR.car_operators()[3]
    ]
    return record + current, frame, current


def commutator_map(matrices):
    return s.Matrix.vstack(*(
        s.kronecker_product(matrix.T, I16)
        - s.kronecker_product(I16, matrix)
        for matrix in matrices
    ))


def reduce_mod11(matrix):
    result = matrix.subs(
        {
            CAR.a: 5,
            CAR.p: 3,
            FRAME.a: 5,
            FRAME.p: 3,
        },
        simultaneous=True,
    ).applyfunc(s.radsimp)
    converted = []
    for entry in result:
        if getattr(s.sympify(entry), "free_symbols", set()):
            raise AssertionError("UNREDUCED_SYMBOL_IN_MODULAR_MATRIX")
        value = s.Rational(entry)
        denominator = int(value.q) % MODULUS
        if denominator == 0:
            raise AssertionError("NONINVERTIBLE_MODULAR_DENOMINATOR")
        converted.append(
            (int(value.p) * pow(denominator, -1, MODULUS)) % MODULUS
        )
    return s.Matrix(result.rows, result.cols, converted)


def coefficients_are_integer_polynomials(matrices):
    for matrix in matrices:
        for entry in matrix:
            numerator, denominator = s.fraction(s.cancel(entry))
            if denominator != 1:
                return False
            try:
                polynomial = s.Poly(numerator, CAR.a, CAR.p, domain="QQ")
            except s.PolynomialError:
                return False
            if any(coefficient.q != 1 for coefficient in polynomial.coeffs()):
                return False
    return True


def modular_rank(matrices):
    from sympy.polys.domains import GF
    from sympy.polys.matrices import DomainMatrix

    reduced = reduce_mod11(commutator_map(matrices))
    return DomainMatrix.from_Matrix(reduced).convert_to(GF(MODULUS)).rank()


def certificate_data():
    from sympy.polys.domains import GF
    from sympy.polys.matrices import DomainMatrix

    ops, frame, current = operators()
    checks = []

    def check(name, proposition):
        if not bool(proposition):
            raise AssertionError(name)
        checks.append(name)

    check("adapted_frame_is_orthogonal", FRAME.mat(frame.T * frame - s.eye(16)) == s.zeros(16))
    check("record_step_is_unitary", FRAME.mat(ops[0].T * ops[0] - I16) == s.zeros(16))
    check("price_cut_is_projection", FRAME.mat(ops[1] * ops[1] - ops[1]) == s.zeros(16))
    check("blank_cut_is_projection", FRAME.mat(ops[2] * ops[2] - ops[2]) == s.zeros(16))
    check("price_and_blank_cuts_differ", ops[1] != ops[2])
    check(
        "adapted_coefficients_are_integer_polynomials",
        coefficients_are_integer_polynomials(ops),
    )
    for i, alpha in enumerate(current):
        check(f"current_{i+1}_selfadjoint", FRAME.mat(alpha.T - alpha) == s.zeros(16))
        for j, other in enumerate(current):
            check(
                f"current_clifford_{i+1}_{j+1}",
                FRAME.mat(alpha * other + other * alpha - 2 * int(i == j) * I16)
                == s.zeros(16),
            )
    check(
        "identity_in_common_kernel",
        all(FRAME.mat(I16 * x - x * I16) == s.zeros(16) for x in ops),
    )

    comm = reduce_mod11(commutator_map(ops))
    domain = DomainMatrix.from_Matrix(comm).convert_to(GF(MODULUS))
    reduced, pivot_columns = domain.rref()
    rank = domain.rank()
    check("modular_common_commutant_rank_255", rank == 255)
    check("modular_pivot_column_count", len(pivot_columns) == 255)

    restricted = domain.extract(range(domain.shape[0]), pivot_columns)
    _, pivot_rows = restricted.transpose().rref()
    minor = domain.extract(pivot_rows, pivot_columns)
    determinant = int(minor.det())
    check("pivot_row_count", len(pivot_rows) == 255)
    check("pivot_minor_rank", minor.rank() == 255)
    check("pivot_minor_determinant_mod11", determinant == 6)

    current_rank = modular_rank(current)
    record_rank = modular_rank(ops[:3])
    without_record_step_rank = modular_rank(ops[1:])
    check("current_only_commutant_dimension_32", 256 - current_rank == 32)
    check("record_only_commutant_dimension_16", 256 - record_rank == 16)
    check("omit_record_step_commutant_dimension_2", 256 - without_record_step_rank == 2)

    def matrix_unit(i, j):
        result = s.zeros(2)
        result[i, j] = 1
        return result

    doubled = [s.kronecker_product(matrix, s.eye(2)) for matrix in ops]
    right_units = {
        (i, j): s.kronecker_product(I16, matrix_unit(j, i))
        for i in range(2)
        for j in range(2)
    }
    check(
        "two_copy_right_M2_commutes_with_fixed_tuple",
        all(
            FRAME.mat(operator * action - action * operator) == s.zeros(32)
            for operator in doubled
            for action in right_units.values()
        ),
    )
    check(
        "two_copy_right_M2_op_matrix_unit_relations",
        all(
            FRAME.mat(
                right_units[(i, j)] * right_units[(k, ell)]
                - int(i == ell) * right_units[(k, j)]
            )
            == s.zeros(32)
            for i in range(2)
            for j in range(2)
            for k in range(2)
            for ell in range(2)
        ),
    )
    af_right = AF.right_frames(1)
    check(
        "level1_AF_path_module_right_multiplicity_34_21",
        AF.counts(1) == (2, 1)
        and AF.counts(4) == (8, 5)
        and [frame["dimension"] for frame in af_right] == [34, 21],
    )

    return {
        "status": "PASS",
        "proof": "02_REGISTRY/research/A4D_NATIVE_AFCAR_CURRENT_COMMUTANT_BOUNDARY.md",
        "source_commit": "3e512e599f3cf69571b1cacb63972e5c315d9a2c",
        "field": {
            "generator": "a",
            "relations": ["p=a^2", "p^2+p=1", "a^4+a^2-1=0"],
            "specialization": {"prime": 11, "a": 5, "p": 3},
            "polynomial_residue": (5**4 + 5**2 - 1) % 11,
        },
        "commutant": {
            "coefficient_matrix_shape": list(commutator_map(ops).shape),
            "modular_rank": rank,
            "complex_rank_by_minor_and_identity": 255,
            "complex_dimension": 1,
            "pivot_rows": list(map(int, pivot_rows)),
            "pivot_columns": list(map(int, pivot_columns)),
            "minor_determinant_mod11": determinant,
        },
        "controls": {
            "current_only_commutant_dimension": 256 - current_rank,
            "record_only_commutant_dimension": 256 - record_rank,
            "without_record_step_commutant_dimension": 256 - without_record_step_rank,
        },
        "single_copy_right_M2_extension_excluded": True,
        "two_copy_abstract_right_M2_extension_realized": True,
        "two_copy_commutant_dimension_by_block_argument": 4,
        "two_copy_AF_path_binding_established": False,
        "AF_right_module_capacity": {
            "input_level": 1,
            "input_simple_sizes": [2, 1],
            "working_level": 4,
            "working_simple_sizes": [8, 5],
            "old_right_multiplicities": [34, 21],
            "two_copy_slots_required": 16,
            "M2_branch_has_capacity": True,
            "path_specific_carrier_established": False,
        },
        "larger_multiplicity_or_covariant_current_excluded": False,
        "whole_core_no_go": False,
        "exact_controls": len(checks),
        "check_names": checks,
    }


if __name__ == "__main__":
    import json

    print(json.dumps(certificate_data(), indent=2, sort_keys=True))
