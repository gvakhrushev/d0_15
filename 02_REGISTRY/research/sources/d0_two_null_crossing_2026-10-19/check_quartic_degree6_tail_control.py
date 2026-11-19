#!/usr/bin/env python3
"""Audit and repair the degree-five spatial tail of the quartic local jet.

The four non-mixed quartic sectors use the exact rational solution from the
shared-branch solve. In the mixed (2,2) sector, this checker adds only
homogeneous degree-six proper-Lorentz link coefficients and solves the full
spatial degree-five Euler response. It then directly checks every spatial
coefficient of all 40 Euler rows through total amplitude degree four.

This is still a local, unwrapped polynomial jet on one exact cubic affine
section, not a periodic solution or physical D0/GR closure.
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


def exact_polynomial_failures(rows, amplitudes):
    checks = {}
    for amplitude in amplitudes:
        failures = []
        for row_index, row in enumerate(rows):
            polynomial = s.Poly(s.expand(row.coeff(amplitude)), c.X, c.Y)
            if not polynomial.is_zero:
                failures.append({
                    "row": row_index,
                    "spatial_degree": polynomial.total_degree(),
                    "nonzero_terms": len(polynomial.terms()),
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
    old_matrix = s.Matrix([[s.Rational(value) for value in row]
                           for row in old_record["matrix"]])
    old_link_monomials = c.monomials(5)
    old_coframe_monomials = c.monomials(4)
    old_n_link = 24 * len(old_link_monomials)
    old_n_coframe = 16 * len(old_coframe_monomials)
    require(old_matrix.shape == (old_n_link + old_n_coframe, len(SECTORS)),
            "prior exact quartic solution has an unexpected shape")
    require(all(value.is_Rational for value in old_matrix),
            "prior quartic solution contains non-rational entries")

    A, B = (1, 0), (0, 1)
    point, cubic_cache, cubic_modes, kernel_parameters = \
        restricted.source_profile(A, B)
    zero_kernel = {parameter: s.Integer(0) for parameter in kernel_parameters}
    cubic_cache = freeze_cache(cubic_cache, zero_kernel)
    cubic_modes = freeze_modes(cubic_modes, zero_kernel)

    old_gamma_fields = [c.gamma_field(
        {amplitude: old_matrix[:old_n_link, column]}, old_link_monomials)
        for column, amplitude in enumerate(SECTORS)]
    old_gamma = c.merge_gamma_fields(*old_gamma_fields)
    old_cache = restricted.add_quartic_links(cubic_cache, old_gamma)
    old_coframe = c.coframe_field(
        {amplitude: old_matrix[old_n_link:, column]
         for column, amplitude in enumerate(SECTORS)}, old_coframe_monomials)

    def old_modes(site):
        result = cubic_modes(site)
        for key, value in old_coframe(site).items():
            result[key] = s.expand(result.get(key, 0) + value)
        return result

    # Add only the seven homogeneous degree-six monomials for each of the
    # 24 proper-Lorentz generators, keeping every lower coefficient fixed.
    expanded_link_monomials = c.monomials(6)
    homogeneous_indices = [index for index, monomial in
                           enumerate(expanded_link_monomials)
                           if sum(monomial) == 6]
    require(len(homogeneous_indices) == 7,
            "degree-six homogeneous monomial count is not seven")
    tail_variables = s.symbols(f"q6_0:{24 * len(homogeneous_indices)}")
    expanded_vector = [s.Integer(0)] * (24 * len(expanded_link_monomials))
    for generator_slot in range(24):
        for local_index, monomial_index in enumerate(homogeneous_indices):
            expanded_vector[generator_slot * len(expanded_link_monomials) +
                            monomial_index] = tail_variables[
                                generator_slot * len(homogeneous_indices) +
                                local_index]
    tail_gamma = c.gamma_field(
        {MIXED: s.Matrix(expanded_vector)}, expanded_link_monomials)
    combined_gamma = c.merge_gamma_fields(old_gamma, tail_gamma)
    tail_cache = restricted.add_quartic_links(cubic_cache, combined_gamma)

    link_rows = c.link_rows(
        point, tail_cache, A, B, cubic=True, coframe_modes=old_modes)
    coframe_rows = c.solder_rows(
        point, tail_cache, A, B, cubic=True, coframe_modes=old_modes)
    # Degree-six link perturbations can contribute through spatial degree five
    # in either Euler family. Keep that complete support in the response map.
    outputs = c.monomials(5)
    response = c.response_vector(link_rows, coframe_rows, MIXED,
                                 outputs, outputs)
    operator = response.jacobian(tail_variables)
    zero_tail = {variable: s.Integer(0) for variable in tail_variables}
    source = s.Matrix([entry.xreplace(zero_tail) for entry in response])
    require(all(entry.is_Rational for entry in operator),
            "degree-six response operator is not rational")
    require(all(entry.is_Rational for entry in source),
            "degree-five mixed source is not rational")
    defects = [response[row] - source[row] - sum(
        operator[row, col] * tail_variables[col]
        for col in range(len(tail_variables)))
        for row in range(response.rows)]
    require(all(c.exact_zero(defect) for defect in defects),
            "degree-six tail response is not affine")

    solved = False
    solver_message = None
    try:
        tail_solution, parameters = operator.gauss_jordan_solve(-source)
        if parameters.rows:
            zero_parameters = {parameter: s.Integer(0)
                               for parameter in parameters}
            tail_solution = tail_solution.applyfunc(
                lambda value: value.xreplace(zero_parameters))
        require(all(c.exact_zero(value)
                    for value in operator * tail_solution + source),
                "degree-six tail solve failed exact substitution")
        solved = True
    except ValueError as error:
        solver_message = str(error)

    direct_checks = {}
    lorentz_ok = False
    if solved:
        solved_tail_field = c.gamma_field(
            {MIXED: tail_solution}, [expanded_link_monomials[index]
                                      for index in homogeneous_indices])
        # tail_solution is ordered by generator slot then degree-six monomial.
        solved_cache = restricted.add_quartic_links(
            old_cache, solved_tail_field)
        all_link_rows = c.link_rows(
            point, solved_cache, A, B, cubic=True, coframe_modes=old_modes)
        all_coframe_rows = c.solder_rows(
            point, solved_cache, A, B, cubic=True, coframe_modes=old_modes)
        all_rows = all_link_rows + all_coframe_rows
        direct_checks = exact_polynomial_failures(all_rows, c.monomials(4))
        c.check_lorentz_links(solved_cache(point))
        lorentz_ok = True

    direct_ok = solved and all(
        result["exactly_zero_all_spatial_degrees"]
        for result in direct_checks.values())
    report = {
        "schema": "d0-exact-research-result/v1",
        "status": ("PASS_LOCAL_FULL_SPATIAL_DEGREE4_40_EULER_JET"
                   if direct_ok else
                   "DEGREE6_LINK_TAIL_RANGE_OBSTRUCTION"
                   if not solved else
                   "SOLVED_DEGREE6_TAIL_BUT_FULL_EULER_RESIDUAL_REMAINS"),
        "scope": "local unwrapped polynomial perturbative jet on one cubic affine section",
        "A": list(A),
        "B": list(B),
        "quartic_amplitude_sectors": [list(amplitude) for amplitude in SECTORS],
        "mixed_sector_repaired": list(MIXED),
        "cubic_kernel_parameters_fixed_to_zero_in_one_valid_affine_section": len(kernel_parameters),
        "prior_solution_sha256": sha256(OLD_SOLUTION),
        "prior_link_degree": 5,
        "added_link_degree": 6,
        "added_homogeneous_degree6_link_unknowns": len(tail_variables),
        "spatial_output_degree": 5,
        "response_shape": list(operator.shape),
        "exact_solver_message": solver_message,
        "degree6_tail_solved_exactly": solved,
        "direct_substitution_all_40_rows_all_spatial_degrees": direct_ok,
        "direct_euler_checks": direct_checks,
        "proper_lorentz_links_through_amplitude_degree_four": lorentz_ok,
        "periodic_carrier_root": False,
        "uniform_refinement": False,
        "native_price_selection": False,
        "physical_gr_closure": False,
        "GR_closed": False,
    }
    result_path = HERE / "quartic_full_spatial_support_result.json"
    result_path.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    if direct_ok:
        print("PASS degree-six proper-Lorentz link tail cancels the degree-five mixed residual")
        print("PASS direct full-polynomial substitution in all 40 Euler rows")
        print("PASS proper-Lorentz links through amplitude degree four")
        print("SCOPE: local unwrapped jet only; no periodic recovery or physical GR closure")
    elif solved:
        print("FAIL: exact degree-six response solved, but full Euler rows retain a tail")
    else:
        print("PASS: exact obstruction for this degree-six-only response correction")
        print("Lower quartic coefficients and the cubic affine section were held fixed.")


if __name__ == "__main__":
    main()
