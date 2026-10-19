#!/usr/bin/env python3
"""Solve the complete local degree-four amplitude jet through spatial degree 5.

The checker reuses exact solutions for the four non-mixed quartic sectors,
then solves the mixed (2,2) sector with all degree<=6 proper-Lorentz links
and degree<=5 original coframe components released at once. It directly
substitutes the assembled field into all 40 finite Euler rows and checks every
spatial coefficient through total amplitude degree four.

Scope remains local and unwrapped on one exact cubic affine section.
"""
import hashlib
import json
import sys
from pathlib import Path

import sympy as s

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import check_cubic_finite_cartan_range as c
import check_quartic_finite_cartan_range as restricted

SECTORS = ((4, 0), (3, 1), (2, 2), (1, 3), (0, 4))
MIXED = (2, 2)
OLD_SOLUTION = HERE / "quartic_all_sectors_shared_cubic_branch_solution.json"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def freeze_cache(cache, substitutions):
    def get(site):
        return [[[c.Jet({amp: s.expand(value.xreplace(substitutions))
                         for amp, value in entry.c.items()})
                  for entry in row] for row in matrix] for matrix in cache(site)]
    return get


def freeze_modes(modes, substitutions):
    def get(site):
        return {key: s.expand(value.xreplace(substitutions))
                for key, value in modes(site).items()}
    return get


def full_checks(rows, amplitudes):
    checks = {}
    for amplitude in amplitudes:
        failures = []
        for row_index, row in enumerate(rows):
            polynomial = s.Poly(s.expand(row.coeff(amplitude)), c.X, c.Y)
            if not polynomial.is_zero:
                failures.append({
                    "row": row_index,
                    "spatial_degree": polynomial.total_degree(),
                    "terms": [
                        {"monomial": list(monomial), "coefficient": str(coefficient)}
                        for monomial, coefficient in polynomial.terms()
                    ],
                })
        checks[f"{amplitude[0]},{amplitude[1]}"] = {
            "exactly_zero_all_spatial_degrees": not failures,
            "failure_row_count": len(failures),
            "failures": failures,
        }
    return checks


def main():
    old_record = json.loads(OLD_SOLUTION.read_text())
    require(sha256(HERE / old_record["source_checker"]) ==
            old_record["source_checker_sha256"],
            "prior shared-branch checker SHA-256 mismatch")
    require(sha256(HERE / old_record["source_output"]) ==
            old_record["source_output_sha256"],
            "prior shared-branch solver output SHA-256 mismatch")
    old_matrix = s.Matrix([[s.Rational(value) for value in row]
                           for row in old_record["matrix"]])
    old_link_monomials = c.monomials(5)
    old_coframe_monomials = c.monomials(4)
    old_n_link = 24 * len(old_link_monomials)
    old_n_coframe = 16 * len(old_coframe_monomials)
    require(old_matrix.shape == (old_n_link + old_n_coframe, len(SECTORS)),
            "prior exact quartic solution has an unexpected shape")
    require(all(value.is_Rational for value in old_matrix),
            "prior exact quartic solution contains non-rational entries")

    A, B = (1, 0), (0, 1)
    point, cubic_cache, cubic_modes, kernel_parameters = \
        restricted.source_profile(A, B)
    zero_kernel = {parameter: s.Integer(0) for parameter in kernel_parameters}
    cubic_cache = freeze_cache(cubic_cache, zero_kernel)
    cubic_modes = freeze_modes(cubic_modes, zero_kernel)

    old_gamma_fields = []
    old_coframe_solutions = {}
    for column, amplitude in enumerate(SECTORS):
        if amplitude == MIXED:
            continue
        old_gamma_fields.append(c.gamma_field(
            {amplitude: old_matrix[:old_n_link, column]}, old_link_monomials))
        old_coframe_solutions[amplitude] = old_matrix[old_n_link:, column]
    old_gamma = c.merge_gamma_fields(*old_gamma_fields)
    old_coframe = c.coframe_field(old_coframe_solutions,
                                  old_coframe_monomials)

    link_monomials = c.monomials(6)
    coframe_monomials = c.monomials(5)
    outputs = c.monomials(5)
    n_link = 24 * len(link_monomials)
    n_coframe = 16 * len(coframe_monomials)
    link_variables = s.symbols(f"q0:{n_link}")
    coframe_variables = s.symbols(f"e0:{n_coframe}")
    variables = tuple(link_variables) + tuple(coframe_variables)
    mixed_gamma = c.gamma_field(
        {MIXED: s.Matrix(link_variables)}, link_monomials)
    combined_gamma = c.merge_gamma_fields(old_gamma, mixed_gamma)
    cache = restricted.add_quartic_links(cubic_cache, combined_gamma)
    mixed_coframe = c.coframe_field(
        {MIXED: s.Matrix(coframe_variables)}, coframe_monomials)

    def modes(site):
        result = cubic_modes(site)
        for field in (old_coframe, mixed_coframe):
            for key, value in field(site).items():
                result[key] = s.expand(result.get(key, 0) + value)
        return result

    link_rows = c.link_rows(point, cache, A, B, cubic=True,
                            coframe_modes=modes)
    coframe_rows = c.solder_rows(point, cache, A, B, cubic=True,
                                 coframe_modes=modes)
    response = c.response_vector(link_rows, coframe_rows, MIXED,
                                 outputs, outputs)
    operator = response.jacobian(variables)
    zero = {variable: s.Integer(0) for variable in variables}
    source = s.Matrix([entry.xreplace(zero) for entry in response])
    require(all(entry.is_Rational for entry in operator),
            "full spatial response operator is not rational")
    require(all(entry.is_Rational for entry in source),
            "mixed quartic source is not rational")
    defects = [response[row] - source[row] - sum(
        operator[row, col] * variables[col]
        for col in range(len(variables)))
        for row in range(response.rows)]
    require(all(c.exact_zero(defect) for defect in defects),
            "full spatial quartic response is not affine")

    solved = False
    solver_message = None
    solution = None
    try:
        solution, parameters = operator.gauss_jordan_solve(-source)
        if parameters.rows:
            zero_parameters = {parameter: s.Integer(0)
                               for parameter in parameters}
            solution = solution.applyfunc(
                lambda value: value.xreplace(zero_parameters))
        require(all(c.exact_zero(value)
                    for value in operator * solution + source),
                "full spatial quartic solution failed exact substitution")
        solved = True
    except ValueError as error:
        solver_message = str(error)

    direct_checks = {}
    lorentz_ok = False
    solution_path = None
    if solved:
        final_cache = restricted.add_quartic_links(
            cubic_cache,
            c.merge_gamma_fields(
                old_gamma,
                c.gamma_field({MIXED: s.Matrix(solution[:n_link])},
                              link_monomials)))
        new_mixed_coframe = c.coframe_field(
            {MIXED: s.Matrix(solution[n_link:])}, coframe_monomials)

        def final_modes(site):
            result = cubic_modes(site)
            for field in (old_coframe, new_mixed_coframe):
                for key, value in field(site).items():
                    result[key] = s.expand(result.get(key, 0) + value)
            return result

        final_link_rows = c.link_rows(
            point, final_cache, A, B, cubic=True,
            coframe_modes=final_modes)
        final_coframe_rows = c.solder_rows(
            point, final_cache, A, B, cubic=True,
            coframe_modes=final_modes)
        direct_checks = full_checks(
            final_link_rows + final_coframe_rows, c.monomials(4))
        c.check_lorentz_links(final_cache(point))
        lorentz_ok = True
        solution_path = HERE / "quartic_full_spatial_jet_solution.json"
        solution_path.write_text(json.dumps({
            "schema": "d0-exact-polynomial-solution/v1",
            "amplitude": list(MIXED),
            "link_spatial_degree_at_most": 6,
            "coframe_spatial_degree_at_most": 5,
            "variable_order": "all link coefficients then all coframe coefficients in checker monomial order",
            "solution": [str(value) for value in solution],
        }, indent=2) + "\n")

    direct_ok = solved and all(
        result["exactly_zero_all_spatial_degrees"]
        for result in direct_checks.values())
    report = {
        "schema": "d0-exact-research-result/v1",
        "status": ("PASS_LOCAL_FULL_SPATIAL_DEGREE4_40_EULER_JET"
                   if direct_ok else
                   "EXACT_FULL_SPATIAL_QUARTIC_RANGE_OBSTRUCTION"
                   if not solved else
                   "SOLVED_PROJECTED_SYSTEM_BUT_FULL_EULER_RESIDUAL_REMAINS"),
        "scope": "local unwrapped polynomial perturbative jet on one cubic affine section",
        "A": list(A),
        "B": list(B),
        "quartic_amplitude_sectors": [list(amplitude) for amplitude in SECTORS],
        "mixed_sector_solved_with_all_lower_and_higher_spatial_modes_released": list(MIXED),
        "cubic_kernel_parameters_fixed_to_zero_in_one_valid_affine_section": len(kernel_parameters),
        "prior_four_sector_solution_sha256": sha256(OLD_SOLUTION),
        "quartic_link_spatial_degree_at_most": 6,
        "quartic_coframe_spatial_degree_at_most": 5,
        "quartic_link_unknowns_mixed_sector": n_link,
        "quartic_coframe_unknowns_mixed_sector": n_coframe,
        "spatial_output_degree": 5,
        "response_shape": list(operator.shape),
        "exact_solver_message": solver_message,
        "mixed_sector_solved_exactly": solved,
        "direct_substitution_all_40_rows_all_spatial_degrees_through_amp_degree4": direct_ok,
        "direct_euler_checks": direct_checks,
        "proper_lorentz_links_through_amplitude_degree_four": lorentz_ok,
        "solution_file": solution_path.name if solution_path else None,
        "solution_sha256": sha256(solution_path) if solution_path else None,
        "periodic_carrier_root": False,
        "uniform_refinement": False,
        "native_price_selection": False,
        "physical_gr_closure": False,
        "GR_closed": False,
    }
    (HERE / "quartic_full_spatial_jet_result.json").write_text(
        json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    if direct_ok:
        print("PASS exact mixed-sector solve with all degree<=6 link and degree<=5 coframe modes released")
        print("PASS direct full-polynomial substitution in all 40 Euler rows and all 15 amplitude sectors")
        print("PASS proper-Lorentz links through amplitude degree four")
        print("SCOPE: local unwrapped jet only; no periodic recovery or physical GR closure")
    elif solved:
        print("FAIL: projected response solved, but full polynomial Euler rows retain a residual")
    else:
        print("PASS: exact obstruction in the declared full spatial polynomial ansatz")


if __name__ == "__main__":
    main()
