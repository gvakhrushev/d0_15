#!/usr/bin/env python3
"""Coefficientwise audit of the merged #270 metric-response null identity.

Terminal: A4D-HAQ-LINEARITY-AND-Q0-IDENTITY-COEFFICIENTWISE-EXACT

The accepted #270 builder is executed only through construction of C(d); the
rank/kernel and later orbit checks are not run. This checker exports all four
24x10 coefficient matrices and the full 20-by-24 cubic coefficient table.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import sympy as sp


ROOT = Path(__file__).resolve().parents[3]
OWNER_RELATIVE = Path(
    "02_REGISTRY/research/certificates/a4d_metric_null_hessian_complex_check.py"
)
OWNER_SHA256 = "d7707248af8a30beb14591991d5a78f37cd73c9fef2ac7c29aae0e8b2003f0b7"
OWNER_MERGE = "7103412403e672ce7416bbfcc63028988f543494"
OUTPUT_RELATIVE = Path(
    "02_REGISTRY/research/certificates/a4d_haq_coefficientwise_identity_coefficients.json"
)

FAILS: list[str] = []


def check(name: str, condition: bool, detail: str = "") -> None:
    if condition:
        print("PASS_" + name)
    else:
        FAILS.append(name)
        print("FAIL_" + name + (" :: " + detail if detail else ""))


def monomial(exponents: tuple[int, ...], variables: tuple[sp.Symbol, ...]) -> sp.Expr:
    result = sp.Integer(1)
    for variable, exponent in zip(variables, exponents):
        result *= variable**exponent
    return result


def monomial_name(exponents: tuple[int, ...]) -> str:
    factors = []
    for j, exponent in enumerate(exponents):
        if exponent:
            factors.append(f"d{j}" if exponent == 1 else f"d{j}^{exponent}")
    return "*".join(factors)


def cubic_exponents() -> list[tuple[int, int, int, int]]:
    # Lexicographic descending order for d0 > d1 > d2 > d3.
    result = []
    for e0 in range(3, -1, -1):
        for e1 in range(3 - e0, -1, -1):
            for e2 in range(3 - e0 - e1, -1, -1):
                e3 = 3 - e0 - e1 - e2
                result.append((e0, e1, e2, e3))
    return result


def scalar_text(value: sp.Expr) -> str:
    return str(sp.cancel(value))


def load_accepted_symbol() -> tuple[sp.Matrix, tuple[sp.Symbol, ...], list[tuple[int, int]]]:
    owner_path = ROOT / OWNER_RELATIVE
    source_bytes = owner_path.read_bytes()
    source_digest = hashlib.sha256(source_bytes).hexdigest()
    check("OWNER_SOURCE_SHA256", source_digest == OWNER_SHA256, source_digest)
    if source_digest != OWNER_SHA256:
        raise RuntimeError("the pinned #270 owner source changed")

    source = source_bytes.decode("utf-8")
    # Cut immediately after C = sp.simplify(HAH * B), before even the owner's
    # global-zero test, projective rank proof, or L4 orbit calculations.
    marker = 'check("C_SHAPE", C.shape == (24, 10))'
    if marker not in source:
        raise RuntimeError("accepted #270 symbol-construction marker not found")
    prefix = source.split(marker, 1)[0]
    namespace = {
        "__name__": "_accepted_a4d_metric_null_symbol_prefix",
        "__file__": str(owner_path),
    }
    exec(compile(prefix, str(owner_path), "exec"), namespace)
    C = namespace["C"]
    d = tuple(namespace["d"])
    SYM = namespace["SYM"]
    check("OWNER_SYMBOL_SHAPE_24x10", C.shape == (24, 10))
    check("OWNER_SYM_ORDER", SYM == [(a, b) for a in range(4) for b in range(a, 4)])
    return C, d, SYM


def main() -> int:
    C, d, SYM = load_accepted_symbol()

    coefficient_matrices = [sp.zeros(24, 10) for _ in range(4)]
    constant_zero = True
    degree_bound = True
    field_Q = True
    for row in range(24):
        for col in range(10):
            polynomial = sp.Poly(sp.expand(C[row, col]), *d, domain=sp.QQ)
            field_Q &= polynomial.domain == sp.QQ
            constant_zero &= polynomial.coeff_monomial(1) == 0
            degree_bound &= polynomial.total_degree() <= 1
            for r in range(4):
                coefficient_matrices[r][row, col] = polynomial.coeff_monomial(d[r])
            reconstructed = sum(d[r] * coefficient_matrices[r][row, col] for r in range(4))
            degree_bound &= sp.expand(C[row, col] - reconstructed) == 0

    check("C_FIELD_Q", field_Q)
    check("C_HOMOGENEOUS_LINEAR_IN_D", constant_zero and degree_bound)
    check("C_CONSTANT_TERM_ZERO", constant_zero)

    matrix_records = []
    matrix_shapes_and_counts = True
    for r, coefficient_matrix in enumerate(coefficient_matrices):
        nonzero = [value for value in coefficient_matrix if value != 0]
        denominators = sorted({int(sp.denom(value)) for value in nonzero})
        matrix_shapes_and_counts &= coefficient_matrix.shape == (24, 10)
        matrix_shapes_and_counts &= len(nonzero) == 18
        matrix_shapes_and_counts &= denominators == [2]
        matrix_records.append(
            {
                "variable": f"d{r}",
                "shape": [24, 10],
                "nonzero_count": len(nonzero),
                "nonzero_denominators": denominators,
                "matrix": [
                    [scalar_text(coefficient_matrix[row, col]) for col in range(10)]
                    for row in range(24)
                ],
            }
        )
        check(
            f"C{r}_18_NONZERO_DENOMINATOR_2",
            len(nonzero) == 18 and denominators == [2],
            f"count={len(nonzero)} denominators={denominators}",
        )
    check("FOUR_COEFFICIENT_MATRICES_24x10", matrix_shapes_and_counts)

    q0_vector = sp.Matrix([sp.expand(d[a] * d[b]) for a, b in SYM])
    product = C * q0_vector
    polynomials = [sp.Poly(sp.expand(product[j]), *d, domain=sp.QQ) for j in range(24)]
    degree_three_only = all(
        coefficient == 0 or sum(exponents) == 3
        for polynomial in polynomials
        for exponents, coefficient in polynomial.terms()
    )
    product_zero = all(polynomial.is_zero for polynomial in polynomials)
    check("PRODUCT_HAS_ONLY_CUBIC_MONOMIALS", degree_three_only)
    check("PRODUCT_IDENTICALLY_ZERO", product_zero)

    exponents = cubic_exponents()
    check(
        "TWENTY_CUBIC_MONOMIALS_LEXICOGRAPHIC",
        len(exponents) == 20
        and exponents[0] == (3, 0, 0, 0)
        and exponents[-1] == (0, 0, 0, 3)
        and exponents == sorted(exponents, reverse=True),
    )

    cubic_records = []
    cubic_zero = True
    for exponent_tuple in exponents:
        term = monomial(exponent_tuple, d)
        coefficient_vector = [
            polynomial.coeff_monomial(term) for polynomial in polynomials
        ]
        vector_zero = all(value == 0 for value in coefficient_vector)
        cubic_zero &= vector_zero
        cubic_records.append(
            {
                "exponents_d0_d1_d2_d3": list(exponent_tuple),
                "monomial": monomial_name(exponent_tuple),
                "coefficient_vector_24": [scalar_text(value) for value in coefficient_vector],
            }
        )
        check(
            "CUBIC_COEFFICIENT_ZERO_" + "_".join(map(str, exponent_tuple)),
            vector_zero,
        )
    scalar_equalities = sum(len(record["coefficient_vector_24"]) for record in cubic_records)
    check("ALL_480_CUBIC_SCALAR_EQUALITIES_ZERO", cubic_zero and scalar_equalities == 480)

    z = sp.symbols("z0:4", nonzero=True)
    d_to_z = {d[r]: 1 / z[r] - 1 for r in range(4)}
    C_z = C.subs(d_to_z)
    q0_z = sp.Matrix([sp.expand(entry.subs(d_to_z)) for entry in q0_vector])
    laurent_product = C_z * q0_z
    laurent_zero = all(sp.cancel(sp.together(entry)) == 0 for entry in laurent_product)
    check("LAURENT_SUBSTITUTION_ZERO", laurent_zero)

    q0_at_one = q0_vector.subs({d[r]: 0 for r in range(4)})
    check("TRIVIAL_CHARACTER_D_AND_Q0_ZERO", q0_at_one == sp.zeros(10, 1))

    if FAILS:
        print("A4D-HAQ-LINEARITY-AND-Q0-IDENTITY-COEFFICIENTWISE-EXACT: FAIL")
        print("FAILS:", ", ".join(FAILS))
        return 1

    payload = {
        "schema": "a4d-haq-coefficientwise-identity/1",
        "terminal": "A4D-HAQ-LINEARITY-AND-Q0-IDENTITY-COEFFICIENTWISE-EXACT",
        "owner_pr": 270,
        "owner_merge_commit": OWNER_MERGE,
        "owner_source": OWNER_RELATIVE.as_posix(),
        "owner_source_sha256": OWNER_SHA256,
        "coefficient_field": "Q",
        "d_variables": [f"d{r}" for r in range(4)],
        "sym_order": [list(pair) for pair in SYM],
        "sym_off_diagonal_scaling": "none",
        "C_decomposition": "C(d)=sum_r d_r C_r",
        "C_shape": [24, 10],
        "C_r": matrix_records,
        "C_q0_product_degree": 3,
        "C_q0_product_zero": product_zero,
        "cubic_monomial_order": "lexicographic descending for d0 > d1 > d2 > d3",
        "cubic_coefficients": cubic_records,
        "cubic_scalar_equalities": scalar_equalities,
        "all_cubic_coefficients_zero": cubic_zero,
        "laurent_substitution": "d_r=z_r^-1-1",
        "laurent_product_zero": laurent_zero,
        "at_z_equals_one_d_and_q0_zero": True,
        "nonzero_ir_germ_claimed": False,
        "rank_or_kernel_recomputed": False,
    }
    output_path = ROOT / OUTPUT_RELATIVE
    output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("COEFFICIENT_JSON:", OUTPUT_RELATIVE.as_posix())
    print("MATRIX_SUMMARY: field=Q; four C_r; each shape=24x10; 18 nonzero entries; denominator=2")
    print("CUBIC_SUMMARY: 20 monomials; 24 coefficients each; all 480 scalar coefficients are zero")
    print("LAURENT_SUMMARY: C(z) vec_sym(q0(z)) is identically zero")
    print("SCOPE: no rank/kernel calculation; q0 is zero at z=(1,1,1,1); no nonzero IR germ inferred")
    print("A4D-HAQ-LINEARITY-AND-Q0-IDENTITY-COEFFICIENTWISE-EXACT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
