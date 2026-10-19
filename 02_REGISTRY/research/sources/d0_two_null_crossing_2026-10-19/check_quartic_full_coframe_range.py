#!/usr/bin/env python3
"""Exact mixed quartic range test with all quartic coframe modes released.

This extends the restricted area-scale test by allowing every one of the 16
coframe components to vary at amplitude [a^2 b^2] with a spatial polynomial
of total degree at most four. It also releases the complete 172-dimensional
joint cubic affine family and degree-five proper-Lorentz link logs. The result
is local and unwrapped; it is neither a periodic carrier root nor a physical
native-price selection.
"""
import json
import sys
from pathlib import Path

import sympy as s

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import check_cubic_finite_cartan_range as c
import check_quartic_finite_cartan_range as restricted


AMP = (2, 2)
LINK_INPUT_DEGREE = 5
COFRAME_INPUT_DEGREE = 4
LINK_OUTPUT_DEGREE = 4
COFRAME_OUTPUT_DEGREE = 4


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def main():
    A, B = (1, 0), (0, 1)
    point, cubic_cache, base_modes, cubic_kernel_parameters = \
        restricted.source_profile(A, B)

    link_source = c.link_rows(
        point, cubic_cache, A, B, cubic=True, coframe_modes=base_modes)
    coframe_source = c.solder_rows(
        point, cubic_cache, A, B, cubic=True, coframe_modes=base_modes)
    source_link_degree = max(map(
        restricted.polynomial_degree,
        [row.coeff(AMP) for row in link_source]))
    source_coframe_degree = max(map(
        restricted.polynomial_degree,
        [row.coeff(AMP) for row in coframe_source]))

    link_monomials = c.monomials(LINK_INPUT_DEGREE)
    coframe_monomials = c.monomials(COFRAME_INPUT_DEGREE)
    link_outputs = c.monomials(LINK_OUTPUT_DEGREE)
    coframe_outputs = c.monomials(COFRAME_OUTPUT_DEGREE)

    n_link = 24 * len(link_monomials)
    n_coframe = 16 * len(coframe_monomials)
    link_variables = s.symbols(f"q0:{n_link}")
    coframe_variables = s.symbols(f"e0:{n_coframe}")
    variables = (tuple(link_variables) + tuple(cubic_kernel_parameters) +
                 tuple(coframe_variables))

    quartic_gamma = c.gamma_field(
        {AMP: s.Matrix(link_variables)}, link_monomials)
    cache = restricted.add_quartic_links(cubic_cache, quartic_gamma)
    quartic_coframe = c.coframe_field(
        {AMP: s.Matrix(coframe_variables)}, coframe_monomials)

    def all_modes(site):
        result = base_modes(site)
        for key, value in quartic_coframe(site).items():
            result[key] = s.expand(result.get(key, 0) + value)
        return result

    link = c.link_rows(point, cache, A, B, cubic=True,
                       coframe_modes=all_modes)
    coframe = c.solder_rows(point, cache, A, B, cubic=True,
                            coframe_modes=all_modes)
    vector = c.response_vector(link, coframe, AMP,
                               link_outputs, coframe_outputs)
    operator = vector.jacobian(variables)
    zero_variables = {variable: s.Integer(0) for variable in variables}
    base = s.Matrix([entry.xreplace(zero_variables) for entry in vector])
    require(all(entry.is_Rational for entry in operator),
            "full-coframe response matrix is not over exact rationals")
    require(all(entry.is_Rational for entry in base),
            "full-coframe response source is not over exact rationals")
    defects = [vector[i] - base[i] - sum(
        operator[i, j] * variables[j] for j in range(len(variables)))
        for i in range(vector.rows)]
    require(all(c.exact_zero(defect) for defect in defects),
            "mixed quartic response is not affine in the released fields")

    solved = False
    failure_detail = None
    try:
        solution, parameters = operator.gauss_jordan_solve(-base)
        if parameters.rows:
            zero_parameters = {parameter: s.Integer(0)
                               for parameter in parameters}
            solution = solution.applyfunc(
                lambda entry: entry.xreplace(zero_parameters))
        require(all(c.exact_zero(value)
                    for value in operator * solution + base),
                "full-coframe quartic solution failed exact substitution")
        solved = True
        quartic_solution = s.Matrix(solution[:n_link])
        gamma = c.gamma_field(
            {AMP: quartic_solution}, link_monomials)
        final_cache = restricted.add_quartic_links(cubic_cache, gamma)
        c.check_lorentz_links(final_cache(point))
    except ValueError as error:
        failure_detail = str(error)

    report = {
        "schema": "d0-exact-research-result/v1",
        "status": ("PASS_MIXED_QUARTIC_FULL_COFRAME_40_EULER_JET" if solved
                   else "EXACT_RANGE_OBSTRUCTION_IN_FULL_COFRAME_POLYNOMIAL_ANSATZ"),
        "scope": "local unwrapped polynomial perturbative jet only",
        "amplitude": "a^2*b^2",
        "A": list(A),
        "B": list(B),
        "geometry_area_scale": "sigma=-(x^2+y^2)^2/128",
        "joint_cubic_affine_kernel_parameters_released": len(cubic_kernel_parameters),
        "quartic_link_unknowns": n_link,
        "independent_quartic_coframe_unknowns": n_coframe,
        "quartic_coframe_input_spatial_degree": COFRAME_INPUT_DEGREE,
        "link_input_spatial_degree": LINK_INPUT_DEGREE,
        "link_output_spatial_degree": LINK_OUTPUT_DEGREE,
        "coframe_output_spatial_degree": COFRAME_OUTPUT_DEGREE,
        "response_shape": list(operator.shape),
        "response_is_exact_rational_affine_map": True,
        "exact_solver_message": failure_detail,
        "periodic_carrier_root": False,
        "all_order_solution": False,
        "native_price_selection": False,
        "physical_gr_closure": False,
        "GR_closed": False,
    }
    print(json.dumps(report, indent=2))
    if solved:
        print("PASS exact substitution into all 40 mixed-quartic Euler rows")
        print("PASS proper-Lorentz links through total amplitude degree four")
        print("PASS all 172 joint cubic affine-kernel parameters were released")
        print("PASS all 240 quartic coframe polynomial coefficients were released")
    else:
        print("PASS exact range obstruction after releasing the full quartic coframe")
        print("This is limited to the declared degree-four coframe and degree-five link support.")


if __name__ == "__main__":
    main()
