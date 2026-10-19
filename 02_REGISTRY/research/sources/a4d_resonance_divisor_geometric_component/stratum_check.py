#!/usr/bin/env python3
"""Candidate partial certificate of the nullity-at-least-2 stratum.

The conjugate intersection V(P+) ∩ V(conjugate(P+)) is a pure dimension-2
complete intersection on (C*)^4. Its three equal-spatial components are
absolutely irreducible of generic rank 22. Every component through
(-1,-1,i,i) has generic rank 22. The point itself has rank 22 and nullity 2;
that is not the generic nullity 1 of either codimension-one component.

Obstruction, not certified here. The residual piece V(R, Q) and the Fitting
loci where one chiral block has rank at most 10. On the fiber (z2, z3)=(2, 3)
the residual eliminant in z1 has degree 54. Rank at most 10 is the vanishing
of the 11×11 minors of the chiral block. This checker does not reduce those
minors on that scheme, so it cannot see the generic rank of every residual
component, nor a Fitting component that avoids (-1,-1,i,i).
"""
from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

from check import GEN, gao_dimension

HERE = Path(__file__).resolve().parent
LEDGER_PATH = HERE.parents[1] / "certificates" / "a4d_resonance_divisor_chiral_numerator.json"
SOURCE_PATH = HERE.parents[1] / "certificates" / "A_and_mixed_symbol_entries.json"
Z = sp.symbols("z0:4")
I = sp.I


def check(label: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(label)
    print("PASS_" + label, flush=True)


def load_parts():
    data = json.loads(LEDGER_PATH.read_text())
    real = 0
    imag = 0
    numerator = {}
    for a0, a1, a2, a3, coeff_text in data["terms"]:
        coeff = sp.sympify(coeff_text)
        re, im = map(int, sp.expand(coeff).as_real_imag())
        monomial = Z[0] ** a0 * Z[1] ** a1 * Z[2] ** a2 * Z[3] ** a3
        real += re * monomial
        imag += im * monomial
        numerator[(a0, a1, a2, a3)] = (re, im)
    return sp.expand(real), sp.expand(imag), numerator, data


def swap(expr, i: int, j: int):
    tmp = sp.symbols("tmp_swap")
    return sp.expand(expr.subs({Z[i]: tmp}).subs({Z[j]: Z[i]}).subs({tmp: Z[j]}))


def univariate(expr, values):
    substituted = sp.expand(expr.subs({Z[1]: values[0], Z[2]: values[1], Z[3]: values[2]}))
    if substituted == 0:
        return sp.Poly(0, Z[0])
    return sp.Poly(substituted, Z[0])


def coordinate_change(sigma: tuple[int, int, int, int]) -> sp.Matrix:
    role = sp.zeros(4)
    for old, new in enumerate(sigma):
        role[new, old] = 1
    generator_change = sp.zeros(6)
    for column, generator in enumerate(GEN):
        transformed = role * generator * role.T
        for row, basis in enumerate(GEN):
            denominator = sum(int(basis[a, b]) ** 2 for a in range(4) for b in range(4))
            generator_change[row, column] = sum(
                transformed[a, b] * basis[a, b] for a in range(4) for b in range(4)
            ) / denominator
    lifted = sp.zeros(24)
    for new_role in range(4):
        old_role = sigma.index(new_role)
        for new_generator in range(6):
            for old_generator in range(6):
                lifted[6 * new_role + new_generator, 6 * old_role + old_generator] = (
                    generator_change[new_generator, old_generator]
                )
    return lifted


def chiral_blocks(symbol: sp.Matrix):
    columns = []
    for chirality in (1, -1):
        for role in range(4):
            for j, k, sign in ((0, 5, 1), (1, 4, -1), (2, 3, 1)):
                vector = sp.zeros(24, 1)
                vector[6 * role + j] = 1
                vector[6 * role + k] = chirality * sign * I
                columns.append(vector)
    change = sp.Matrix.hstack(*columns)
    congruence = (change.T * symbol * change).applyfunc(sp.cancel)
    return change, congruence


def spec_coeffs(poly: dict, z1: int, z2: int, z3: int, modulus: int) -> list[int]:
    coeff = [0] * 7
    for (a0, a1, a2, a3), value in poly.items():
        acc = value % modulus
        acc = acc * pow(z1, a1, modulus) % modulus
        acc = acc * pow(z2, a2, modulus) % modulus
        acc = acc * pow(z3, a3, modulus) % modulus
        coeff[a0] = (coeff[a0] + acc) % modulus
    return coeff


def resultant6(left: list[int], right: list[int], modulus: int) -> int:
    size = 12
    matrix = [[0] * size for _ in range(size)]
    degree = 6
    for shift in range(degree):
        for power in range(degree + 1):
            matrix[shift][shift + power] = left[degree - power] % modulus
            matrix[degree + shift][shift + power] = right[degree - power] % modulus
    det = 1
    for col in range(size):
        pivot = next((row for row in range(col, size) if matrix[row][col] % modulus), None)
        if pivot is None:
            return 0
        if pivot != col:
            matrix[col], matrix[pivot] = matrix[pivot], matrix[col]
            det = (-det) % modulus
        inv = pow(matrix[col][col], -1, modulus)
        det = det * matrix[col][col] % modulus
        for row in range(col + 1, size):
            factor = matrix[row][col] % modulus
            if not factor:
                continue
            factor = factor * inv % modulus
            for index in range(col, size):
                matrix[row][index] = (matrix[row][index] - factor * matrix[col][index]) % modulus
    return det % modulus


def fiber_resultant_degree(real_terms: dict, quotient_terms: dict, modulus: int) -> int:
    values = []
    for z1 in range(modulus):
        values.append(
            resultant6(
                spec_coeffs(real_terms, z1, 2, 3, modulus),
                spec_coeffs(quotient_terms, z1, 2, 3, modulus),
                modulus,
            )
        )
    # Degree of the unique polynomial of degree < modulus interpolating `values`,
    # read from the last nonzero Newton divided difference.
    tableau = values[:]
    degree = 0
    last = tableau[0]
    for level in range(1, len(values)):
        tableau = [(tableau[i + 1] - tableau[i]) % modulus for i in range(len(tableau) - 1)]
        if any(tableau):
            degree = level
            last = tableau[0]
        else:
            break
    check(f"FIBER_LEADING_DIFFERENCE_NONZERO_{modulus}", last % modulus != 0)
    return degree


def homogeneous_part(terms: dict, point, degree: int) -> sp.Expr:
    w = sp.symbols("w0:4")
    acc = 0
    for (e0, e1, e2, e3), (re, im) in terms.items():
        coeff = re + im * I
        factors = []
        for exponent, center in zip((e0, e1, e2, e3), point):
            piece = {}
            for k in range(exponent + 1):
                piece[k] = sp.binomial(exponent, k) * center ** (exponent - k)
            factors.append(piece)
        current = {(): 1}
        for factor in factors:
            nxt = {}
            for prev_exp, prev_c in current.items():
                for k, ck in factor.items():
                    nxt[prev_exp + (k,)] = nxt.get(prev_exp + (k,), 0) + prev_c * ck
            current = nxt
        for exp, cw in current.items():
            if sum(exp) != degree:
                continue
            acc += sp.expand(coeff * cw) * w[0] ** exp[0] * w[1] ** exp[1] * w[2] ** exp[2] * w[3] ** exp[3]
    return sp.expand(acc)


def z0_content_poly(expr) -> sp.Poly:
    gcd_poly = sp.Poly(0, Z[1], Z[2], Z[3])
    for coefficient in sp.Poly(sp.expand(expr), Z[0]).coeffs():
        gcd_poly = sp.gcd(gcd_poly, sp.Poly(sp.expand(coefficient), Z[1], Z[2], Z[3]))
    return gcd_poly


def main() -> None:
    real, imag, numerator, ledger = load_parts()
    check("LEDGER_671_TERMS", ledger["term_count"] == 671 and len(numerator) == 671)
    check("CONJUGATE_WITNESSES", numerator[(6, 4, 4, 4)] == (512, 0) and numerator[(6, 4, 3, 2)] == (0, -512))
    check(
        "NO_VARIABLE_DIVIDES_NUMERATOR",
        all(any(exp[t] == 0 for exp in numerator) for t in range(4)),
    )
    vandermonde = (Z[1] - Z[2]) * (Z[1] - Z[3]) * (Z[2] - Z[3])
    quotient, remainder = sp.div(sp.Poly(imag, *Z), sp.Poly(vandermonde, *Z), domain="QQ")
    check("IMAGINARY_PART_IS_VANDERMONDE_TIMES_QUOTIENT", remainder == 0)
    quotient_expr = sp.expand(quotient.as_expr())
    check("QUOTIENT_NOT_ZERO_ON_z1_EQUALS_z2", sp.expand(quotient_expr.subs({Z[2]: Z[1]})) != 0)
    check("REAL_PART_SYMMETRIC_IN_SPATIAL_VARIABLES", all(sp.expand(real - swap(real, i, j)) == 0 for i, j in ((1, 2), (2, 3), (1, 3))))
    check("QUOTIENT_SYMMETRIC_IN_SPATIAL_VARIABLES", all(sp.expand(quotient_expr - swap(quotient_expr, i, j)) == 0 for i, j in ((1, 2), (2, 3))))
    check("IMAGINARY_PART_ALTERNATING", sp.expand(imag + swap(imag, 1, 2)) == 0)

    coprime_real = univariate(real, (-1, 2, 3))
    coprime_imag = univariate(imag, (-1, 2, 3))
    coprime_quotient = univariate(quotient_expr, (-1, 2, 3))
    check(
        "DEGREE_PRESERVED_COPIME_REAL_IMAGINARY",
        coprime_real.degree() == 6 and coprime_imag.degree() == 6 and sp.gcd(coprime_real, coprime_imag).degree() == 0,
    )
    check("QUOTIENT_Z0_DEGREE_6", sp.degree(quotient_expr, Z[0]) == 6)
    check(
        "DEGREE_PRESERVED_COPRIME_REAL_QUOTIENT",
        coprime_quotient.degree() == 6 and sp.gcd(coprime_real, coprime_quotient).degree() == 0,
    )
    # Positive z0-degree is ruled out by the specializations above.
    # A spatial common factor would divide both z0-contents.
    check(
        "CONTENT_GCD_REAL_IMAGINARY_CONSTANT",
        sp.gcd(z0_content_poly(real), z0_content_poly(imag)).total_degree() == 0,
    )
    check(
        "CONTENT_GCD_REAL_QUOTIENT_CONSTANT",
        sp.gcd(z0_content_poly(real), z0_content_poly(quotient_expr)).total_degree() == 0,
    )
    # The same gcd test sees a common factor when two spatial variables agree.
    forced = univariate(imag, (1, 1, 4))
    check("CONTROL_EQUAL_SPATIAL_GCD_IS_NOT_TRIVIAL", forced.degree() < 0 or sp.gcd(univariate(real, (1, 1, 4)), forced).degree() > 0)

    res_one = int(sp.resultant(univariate(real, (1, 2, 3)), univariate(quotient_expr, (1, 2, 3))))
    res_two = int(sp.resultant(univariate(real, (2, 2, 3)), univariate(quotient_expr, (2, 2, 3))))
    check("RESIDUAL_ELIMINANT_NOT_CONSTANT", res_one != 0 and res_two != 0 and res_one != res_two)

    real_terms = {exp: re for exp, (re, im) in numerator.items() if re}
    quotient_terms = {}
    for mon, coeff in quotient.terms():
        rational = sp.Rational(sp.together(coeff))
        if rational == 0:
            continue
        if rational.q != 1:
            raise AssertionError("QUOTIENT_COEFFICIENT_NOT_INTEGRAL")
        quotient_terms[tuple(int(entry) for entry in mon)] = int(rational.p)
    check("QUOTIENT_Z0_DEGREE_MATCHES_SYLVESTER", max(exp[0] for exp in quotient_terms) == 6)
    degree_251 = fiber_resultant_degree(real_terms, quotient_terms, 251)
    degree_257 = fiber_resultant_degree(real_terms, quotient_terms, 257)
    check("RESIDUAL_FIBER_DEGREE_54", degree_251 == 54 and degree_257 == 54)

    point = (-1, -1, I, I)
    substitution = dict(zip(Z, point))
    check("COUNTEREXAMPLE_ON_RESIDUAL_AND_EQUAL_SPATIAL", all(sp.expand(expr.subs(substitution)) == 0 for expr in (real, imag, quotient_expr)))
    centered = {exp: (re, im) for exp, (re, im) in numerator.items()}
    check(
        "TANGENT_LINEAR_PARTS_VANISH",
        homogeneous_part({exp: (re, 0) for exp, (re, im) in centered.items()}, point, 1) == 0
        and homogeneous_part({exp: (0, im) for exp, (re, im) in centered.items()}, point, 1) == 0,
    )
    quad_real = homogeneous_part({exp: (re, 0) for exp, (re, im) in centered.items()}, point, 2)
    quad_imag = homogeneous_part({exp: (0, im) for exp, (re, im) in centered.items()}, point, 2)
    quad_plus = sp.expand(quad_real + I * quad_imag)
    quad_minus = sp.expand(quad_real - I * quad_imag)
    w = sp.symbols("w0:4")
    check("TANGENT_QUADRICS_NONZERO", quad_plus != 0 and quad_minus != 0)
    summed = sp.factor(sp.expand(quad_plus + quad_minus))
    differ = sp.factor(sp.expand(quad_plus - quad_minus))
    l1 = w[0] - w[1] - w[2] - w[3]
    l2 = w[0] - w[1] + w[2] + w[3]
    m1 = w[0] - w[1]
    m2 = w[2] - w[3]
    check("TANGENT_SUM_FACTORS", sp.expand(summed - sp.Integer(-32768) * l1 * l2) == 0)
    check("TANGENT_DIFFERENCE_FACTORS", sp.expand(differ - sp.Integer(-32768) * I * m1 * m2) == 0)
    planes = ((l1, m1), (l1, m2), (l2, m1), (l2, m2))
    for index, (left, right) in enumerate(planes):
        minors = sp.Matrix([[sp.diff(left, var), sp.diff(right, var)] for var in w])
        check(f"TANGENT_PLANE_{index}_INDEPENDENT", minors.rank() == 2)

    restriction = sp.expand(real.subs({Z[2]: Z[1]}))
    content, factors = sp.factor_list(restriction)
    shape = sorted((sp.total_degree(factor), mult) for factor, mult in factors)
    check("EQUAL_SPATIAL_RESTRICTION_SHAPE", content == 256 and shape == [(1, 2), (16, 1)])
    linear = next(factor for factor, _mult in factors if sp.total_degree(factor) == 1)
    surface = sp.expand(next(factor for factor, _mult in factors if sp.total_degree(factor) > 1))
    check("EQUAL_SPATIAL_LINEAR_FACTOR_IS_z1", sp.expand(linear - Z[1]) == 0)
    check(
        "RESTRICTION_IS_256_z1_SQUARED_SURFACE",
        sp.expand(restriction - content * linear**2 * surface) == 0,
    )
    for variable in (Z[0], Z[1], Z[3]):
        check(f"SURFACE_SURVIVES_{variable}", sp.expand(surface.subs(variable, 0)) != 0)
    u, y = sp.symbols("u y")
    chart = sp.expand(surface.subs({Z[0]: u, Z[1]: u + y, Z[3]: u + 1}))
    chart_poly = sp.Poly(chart, u, y)
    check(
        "SURFACE_CHART_DEGREE_16_LEADING_-4",
        chart_poly.degree(u) == 16 and sp.total_degree(chart) == 16 and chart_poly.LC() == -4,
    )
    chart_terms = {(mon[0], mon[1]): int(coeff) for mon, coeff in chart_poly.terms()}
    for prime in (251, 257):
        reduced = {key: value % prime for key, value in chart_terms.items() if value % prime}
        u_deg, y_deg, dimension = gao_dimension(reduced, prime)
        expression = sum(coeff * u ** a * y ** b for (a, b), coeff in reduced.items())
        mod_poly = sp.Poly(sp.expand(expression), u, y, modulus=prime)
        check(
            f"SURFACE_GAO_DIMENSION_ONE_{prime}",
            u_deg == 16 and y_deg == 8 and prime > (2 * u_deg - 1) * y_deg and dimension == 1,
        )
        check(f"SURFACE_CHART_SQUAREFREE_{prime}", sp.gcd(mod_poly, sp.diff(mod_poly, u)).total_degree() == 0)
    squares = {(2, 0): 1, (0, 2): 1}
    check("CONTROL_SUM_OF_SQUARES_GAO_DIMENSION_2", gao_dimension(squares, 1031)[2] == 2)

    source = json.loads(SOURCE_PATH.read_text())
    symbol = sp.zeros(24)
    for row, col, expression in source["A_entries"]:
        symbol[row, col] = sp.sympify(expression, locals=dict(zip(source["coordinates"], Z)))
    check("PINNED_SYMBOL_96_NONZERO", sum(entry != 0 for entry in symbol) == 96)
    for index, sigma in enumerate(((0, 2, 1, 3), (0, 1, 3, 2))):
        character_map = {Z[r]: Z[sigma.index(r)] for r in range(4)}
        permuted = symbol.subs(character_map, simultaneous=True)
        change = coordinate_change(sigma)
        difference = change.T * permuted * change - symbol
        check(
            f"S3_CONGRUENCE_{index}",
            all(sp.together(sp.expand(entry)) == 0 for entry in difference),
        )
        check(f"S3_DET_ONE_{index}", sp.factor(change.det()) == 1)

    change, congruence = chiral_blocks(symbol)
    check("CHIRAL_CHANGE_DET_4096", sp.factor(change.det()) == 4096)
    off = congruence[:12, 12:]
    check("CONGRUENCE_OFF_BLOCKS_ZERO", all(sp.cancel(entry) == 0 for entry in off))
    block_n = congruence[:12, :12]
    block_m = congruence[12:, 12:]
    similarity = (change.inv() * symbol * change).applyfunc(sp.cancel)
    sim_m = similarity[:12, 12:]
    sim_n = similarity[12:, :12]
    check("CONGRUENCE_BLOCKS_ARE_TWICE_SIMILARITY", all(sp.cancel(block_n[i, j] - 2 * sim_n[i, j]) == 0 for i in range(12) for j in range(12)) and all(sp.cancel(block_m[i, j] - 2 * sim_m[i, j]) == 0 for i in range(12) for j in range(12)))
    check("SECOND_BLOCK_IS_COEFFICIENT_CONJUGATE", all(sp.cancel(sim_n[i, j] - sim_m[i, j].xreplace({I: -I})) == 0 for i in range(12) for j in range(12)))

    sextic = sp.Poly(sp.expand(surface.subs({Z[0]: 1, Z[1]: 2})), Z[3])
    check("SURFACE_SLICE_SEXTIC_IRREDUCIBLE", sp.factor_list(sextic.as_expr())[1] == [(sp.Poly(sextic.as_expr()).as_expr(), 1)] or sextic.degree() == 6 and len(sp.factor_list(sp.primitive(sextic.as_expr())[1])[1]) == 1)
    # factor_list may keep a constant content. Re-check the primitive part directly.
    primitive_sextic = sp.Poly(sp.primitive(sextic.as_expr())[1], Z[3])
    check("SEXTIC_DEGREE_6_ONE_FACTOR", primitive_sextic.degree() == 6 and len(sp.factor_list(primitive_sextic.as_expr())[1]) == 1 and primitive_sextic.TC() != 0)

    def minor_numerator(block):
        specialized = block.subs({Z[0]: 1, Z[1]: 2, Z[2]: 2}).applyfunc(lambda entry: sp.together(sp.expand(entry)))
        minor = sp.together(sp.cancel(specialized[1:, 1:].det(method="domain-ge")))
        numerator_poly, denominator = sp.fraction(sp.together(minor))
        return sp.Poly(sp.expand(numerator_poly), Z[3], extension=I), sp.expand(denominator)

    for label, block in (("M", sim_m), ("N", sim_n)):
        minor_poly, denominator = minor_numerator(block)
        gcd = sp.gcd(minor_poly, sp.Poly(primitive_sextic.as_expr(), Z[3], extension=I))
        check(f"MINOR_{label}_COPRIME_TO_SEXTIC", gcd.degree() == 0)
        denominator_poly = sp.Poly(sp.together(sp.expand(denominator)), Z[3])
        check(
            f"MINOR_{label}_DENOMINATOR_INVERTIBLE_ON_SEXTIC",
            sp.gcd(denominator_poly, primitive_sextic).degree() <= 0,
        )

    field = sp.QQ.algebraic_field(I)

    def block_ranks(values):
        evaluated = congruence.subs(dict(zip(Z, values)))
        domain_matrix = evaluated.to_DM().convert_to(field)
        plus = domain_matrix[:12, :12].rank()
        minus = domain_matrix[12:, 12:].rank()
        return int(plus), int(minus)

    plus_rank, minus_rank = block_ranks(point)
    check("COUNTEREXAMPLE_BLOCK_RANKS_11_11", plus_rank == 11 and minus_rank == 11)
    full_rank = int(symbol.subs(dict(zip(Z, point))).to_DM().convert_to(field).rank())
    check("COUNTEREXAMPLE_FULL_RANK_22", full_rank == 22 and full_rank == plus_rank + minus_rank)
    rank_identity = int(symbol.subs({Z[0]: 1, Z[1]: 1, Z[2]: 1, Z[3]: 1}).to_DM().convert_to(field).rank())
    check("RANK_24_OFF_DIVISOR", rank_identity == 24)
    predicted = 2 * max(sum(value == I for value in point), sum(value == -I for value in point))
    check("PHASE_COUNT_PREDICTS_4_AND_IS_FALSE", predicted == 4 and 24 - full_rank == 2)

    result = {
        "status": "CANDIDATE",
        "carrier": "owned holomorphic connection Hessian A(z) on (C*)^4",
        "intersection_dimension": 2,
        "intersection_decomposition": "V(z1-z2,F12) U V(z1-z3,F13) U V(z2-z3,F23) U V(R,Q)",
        "equal_spatial_component": {
            "absolute_irreducibility": "Gao dimension 1 at 251 and 257",
            "generic_rank": 22,
            "generic_nullity": 2,
        },
        "components_through_(-1,-1,i,i)": {
            "dimension": 2,
            "generic_rank": 22,
            "generic_nullity": 2,
            "rank_at_the_point": 22,
            "nullity_at_the_point": 2,
        },
        "phase_count_at_(-1,-1,i,i)": {
            "predicted_nullity": predicted,
            "exact_rank": full_rank,
            "exact_nullity": 24 - full_rank,
        },
        "residual_fiber": {"z2": 2, "z3": 3, "degree_in_z1": 54},
        "obstruction": (
            "The residual complete intersection V(R,Q) is pure dimension 2, and its "
            "fiber (z2,z3)=(2,3) is a degree-54 scheme in z1. Rank at most 10 is the "
            "vanishing of the 11x11 minors of one chiral block. This checker does not "
            "reduce those minors on that scheme, so it cannot see the generic rank of "
            "every residual component, nor a Fitting component that avoids (-1,-1,i,i)."
        ),
    }
    output = HERE / "stratum_results.json"
    output.write_text(json.dumps(result, indent=2) + "\n")
    print("CANDIDATE_NULLITY_TWO_PARTIAL", flush=True)
    print("RESULT_JSON", output, flush=True)


if __name__ == "__main__":
    main()
