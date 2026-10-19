#!/usr/bin/env python3
"""Try all five quartic amplitude sectors on one valid cubic solution branch.

The cubic family is fixed to the exact particular branch obtained by setting
the algebraic kernel parameters to zero. A single exact 600x744 quartic
operator is checked against all five source vectors at once. This is a local
unwrapped continuation test, not physical branch selection or GR closure.
"""
import json
import sys
from pathlib import Path

import sympy as s

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import check_cubic_finite_cartan_range as c
import check_quartic_finite_cartan_range as restricted


SECTORS = ((4, 0), (3, 1), (2, 2), (1, 3), (0, 4))
LINK_INPUT_DEGREE = 5
COFRAME_INPUT_DEGREE = 4
OUTPUT_DEGREE = 4


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def freeze_cache(cache, substitutions):
    def get(site):
        return [[[c.Jet({amp: s.expand(value.xreplace(substitutions))
                         for amp, value in entry.c.items()})
                  for entry in row] for row in matrix] for matrix in cache(site)]
    return get


def main():
    A, B = (1, 0), (0, 1)
    point, cubic_cache, cubic_modes, kernel_parameters = \
        restricted.source_profile(A, B)
    zero_kernel = {parameter: s.Integer(0)
                   for parameter in kernel_parameters}
    cubic_cache = freeze_cache(cubic_cache, zero_kernel)

    def frozen_cubic_modes(site):
        return {key: s.expand(value.xreplace(zero_kernel))
                for key, value in cubic_modes(site).items()}

    link_monomials = c.monomials(LINK_INPUT_DEGREE)
    coframe_monomials = c.monomials(COFRAME_INPUT_DEGREE)
    outputs = c.monomials(OUTPUT_DEGREE)
    link_variables = s.symbols(f"q0:{24 * len(link_monomials)}")
    coframe_variables = s.symbols(f"e0:{16 * len(coframe_monomials)}")
    variables = tuple(link_variables) + tuple(coframe_variables)

    # The background equations for all five coefficient sectors come from a
    # single exact finite evaluation. Quartic perturbations are inserted once
    # at [a^2 b^2] to construct the common flat response operator.
    base_link_rows = c.link_rows(
        point, cubic_cache, A, B, cubic=True,
        coframe_modes=frozen_cubic_modes)
    base_coframe_rows = c.solder_rows(
        point, cubic_cache, A, B, cubic=True,
        coframe_modes=frozen_cubic_modes)
    sources = []
    for amplitude in SECTORS:
        require(max(map(restricted.polynomial_degree,
                        [row.coeff(amplitude) for row in base_link_rows])) <= OUTPUT_DEGREE,
                f"base link source exceeds degree {OUTPUT_DEGREE} at {amplitude}")
        require(max(map(restricted.polynomial_degree,
                        [row.coeff(amplitude) for row in base_coframe_rows])) <= OUTPUT_DEGREE,
                f"base coframe source exceeds degree {OUTPUT_DEGREE} at {amplitude}")
        sources.append(-c.response_vector(
            base_link_rows, base_coframe_rows, amplitude, outputs, outputs))
    rhs = s.Matrix.hstack(*sources)

    reference_amplitude = (2, 2)
    gamma = c.gamma_field(
        {reference_amplitude: s.Matrix(link_variables)}, link_monomials)
    cache = restricted.add_quartic_links(cubic_cache, gamma)
    quartic_coframe = c.coframe_field(
        {reference_amplitude: s.Matrix(coframe_variables)}, coframe_monomials)

    def response_modes(site):
        result = frozen_cubic_modes(site)
        for key, value in quartic_coframe(site).items():
            result[key] = s.expand(result.get(key, 0) + value)
        return result

    response_link_rows = c.link_rows(
        point, cache, A, B, cubic=True, coframe_modes=response_modes)
    response_coframe_rows = c.solder_rows(
        point, cache, A, B, cubic=True, coframe_modes=response_modes)
    response_vector = c.response_vector(
        response_link_rows, response_coframe_rows,
        reference_amplitude, outputs, outputs)
    reference = response_vector.jacobian(variables)
    zero = {variable: s.Integer(0) for variable in variables}
    base_reference = s.Matrix([entry.xreplace(zero)
                               for entry in response_vector])
    require(all(entry.is_Rational for entry in reference),
            "quartic response operator is not over exact rationals")
    require(all(entry.is_Rational for entry in base_reference),
            "reference mixed quartic source is not over exact rationals")
    require(all(c.exact_zero(base_reference[i] + rhs[:, 2][i])
                for i in range(rhs.rows)),
            "reference source disagrees with the common base Euler rows")
    defects = [response_vector[i] - base_reference[i] - sum(
        reference[i, j] * variables[j] for j in range(len(variables)))
        for i in range(response_vector.rows)]
    require(all(c.exact_zero(defect) for defect in defects),
            "common quartic response is not affine")
    solved = False
    failure_detail = None
    try:
        solution, parameters = reference.gauss_jordan_solve(rhs)
        if parameters.rows:
            zero_parameters = {parameter: s.Integer(0)
                               for parameter in parameters}
            solution = solution.applyfunc(
                lambda value: value.xreplace(zero_parameters))
        residual = reference * solution - rhs
        require(all(c.exact_zero(value) for value in residual),
                "shared-branch quartic multi-source solve failed substitution")
        Path("/tmp/d0_quartic_all_sectors_shared_solution.json").write_text(
            json.dumps([[str(solution[i, j]) for j in range(solution.cols)]
                        for i in range(solution.rows)]))
        solved = True
    except ValueError as error:
        failure_detail = str(error)

    direct_euler_checks = {}
    lorentz_ok = False
    if solved:
        gamma_fields = []
        n_link = len(link_variables)
        for column, amplitude in enumerate(SECTORS):
            gamma_fields.append(c.gamma_field(
                {amplitude: solution[:n_link, column]}, link_monomials))
        quartic_gamma = c.merge_gamma_fields(*gamma_fields)
        final_cache = restricted.add_quartic_links(cubic_cache, quartic_gamma)
        coframe_solution = c.coframe_field(
            {amplitude: solution[n_link:, column]
             for column, amplitude in enumerate(SECTORS)}, coframe_monomials)

        def final_modes(site):
            result = frozen_cubic_modes(site)
            for key, value in coframe_solution(site).items():
                result[key] = s.expand(result.get(key, 0) + value)
            return result

        final_link_rows = c.link_rows(
            point, final_cache, A, B, cubic=True, coframe_modes=final_modes)
        final_coframe_rows = c.solder_rows(
            point, final_cache, A, B, cubic=True, coframe_modes=final_modes)
        for amplitude in c.monomials(4):
            failures = []
            for row_index, row in enumerate(final_link_rows + final_coframe_rows):
                polynomial = s.Poly(s.expand(row.coeff(amplitude)), c.X, c.Y)
                if not polynomial.is_zero:
                    failures.append({
                        "row": row_index,
                        "spatial_degree": polynomial.total_degree(),
                        "nonzero_terms": len(polynomial.terms()),
                        "sample_terms": [
                            {"monomial": list(monomial), "coefficient": str(coefficient)}
                            for monomial, coefficient in polynomial.terms()[:3]
                        ],
                    })
            direct_euler_checks[f"{amplitude[0]},{amplitude[1]}"] = {
                "exactly_zero_all_spatial_degrees": not failures,
                "failure_row_count": len(failures),
                "first_failures": failures[:8],
            }
        c.check_lorentz_links(final_cache(point))
        lorentz_ok = True

    direct_euler_ok = solved and all(
        result["exactly_zero_all_spatial_degrees"]
        for result in direct_euler_checks.values())

    report = {
        "schema": "d0-exact-research-result/v1",
        "status": (
            "PASS_LOCAL_FULL_DEGREE4_40_EULER_JET_ON_SHARED_CUBIC_BRANCH"
            if direct_euler_ok else
            "TRUNCATED_RANGE_SOLVE_DOES_NOT_CLOSE_FULL_EULER_ROWS"
            if solved else "EXACT_SHARED_CUBIC_BRANCH_QUARTIC_RANGE_OBSTRUCTION"),
        "scope": "local unwrapped polynomial perturbative jet only",
        "A": list(A),
        "B": list(B),
        "quartic_amplitude_sectors": [list(amplitude) for amplitude in SECTORS],
        "cubic_kernel_parameters_fixed_to_zero_in_one_valid_affine_section": len(kernel_parameters),
        "quartic_link_unknowns_per_sector": len(link_variables),
        "quartic_coframe_unknowns_per_sector": len(coframe_variables),
        "quartic_operator_shape_per_sector": list(reference.shape),
        "multi_source_shape": list(rhs.shape),
        "total_quartic_spatial_equations": rhs.rows * rhs.cols,
        "exact_solver_message": failure_detail,
        "all_five_sources_solved_on_one_cubic_section": solved,
        "direct_substitution_all_five_sectors": direct_euler_ok,
        "direct_euler_checks": direct_euler_checks,
        "proper_lorentz_links_through_amplitude_degree_four": lorentz_ok,
        "periodic_carrier_root": False,
        "uniform_refinement": False,
        "native_price_selection": False,
        "physical_gr_closure": False,
        "GR_closed": False,
    }
    print(json.dumps(report, indent=2))
    if direct_euler_ok:
        print("PASS exact simultaneous multi-source solve for all five quartic sectors")
        print("PASS direct substitution into all 40 Euler rows over spatial degree <= 4")
        print("PASS proper-Lorentz links through total amplitude degree four")
        print("SCOPE: one common exact cubic affine section; no physical selector is inferred")
    elif solved:
        print("FAIL truncated response solve does not close the full finite Euler rows")
        for amplitude, result in direct_euler_checks.items():
            if not result["exactly_zero_all_spatial_degrees"]:
                print(f"FAIL amplitude {amplitude}: {result['failure_row_count']} rows retain spatial residuals")
                print(json.dumps(result["first_failures"], indent=2))
    else:
        print("PASS exact obstruction for this common cubic affine section only")
        print("Other choices in the joint cubic kernel remain unclassified.")


if __name__ == "__main__":
    main()
