#!/usr/bin/env python3
"""Exact finite [a^2 b^2] source/range solve for the 24+16 Cartan system.

This continues the checked cubic local jet on the unwrapped transverse lattice.
It includes the orbit-area null-leg scale, releases all cubic coframe modes,
and solves the complete mixed quartic coefficient in a degree-bounded range.
No periodic-carrier, convergent-series, native-price, or physical-GR claim is
made by this file.
"""
import json
import sys
from pathlib import Path

import sympy as s

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import check_cubic_finite_cartan_range as c


# Reuse the exact finite action and cubic solution while extending its formal
# amplitude algebra by one degree. The fourth exponential term is essential.
c.MAX_DEGREE = 4
c.AMPLITUDES = c.monomials(4)


def exp_lorentz(logarithm):
    identity = c.mat_from_sympy(s.eye(4))
    power = identity
    result = identity
    for degree in range(1, 5):
        power = c.mat_mul(power, logarithm)
        result = c.mat_add(result, c.mat_scale(power, s.Rational(1, s.factorial(degree))))
    return result


c.exp_lorentz = exp_lorentz


def source_profile(A, B):
    """Return the full joint cubic family and the fixed quartic area mode.

    The tested quartic class varies proper-Lorentz link logs through spatial
    degree five. Its only quartic coframe correction is the geometry-fixed
    orbit-area scale sigma; independent quartic coframe modes are outside it.
    """
    point = (0, 0, c.X, c.Y)
    c.MAX_DEGREE = 3
    c.AMPLITUDES = c.monomials(3)
    _, _, _, _, _, family, base_link_solutions = c.solve_full_cubic_40(
        A, B, expose_family=True)
    gamma_parts = [c.gamma_field(base_link_solutions)]
    coframe_solutions = {}
    kernel_parameters = []
    for amplitude in ((2, 1), (1, 2)):
        family_solution, free_parameters = family[amplitude]
        prefix = "aab" if amplitude == (2, 1) else "abb"
        renamed = s.symbols(f"tau_{prefix}_0:{len(free_parameters)}")
        family_solution = family_solution.xreplace(
            dict(zip(free_parameters, renamed)))
        kernel_parameters.extend(renamed)
        gamma_parts.append(c.gamma_field(
            {amplitude: s.Matrix(family_solution[:144])}, c.monomials(2)))
        coframe_solutions[amplitude] = s.Matrix(family_solution[144:])

    gamma = c.merge_gamma_fields(*gamma_parts)
    cubic_cache = c.build_log_cache(A, B, cubic=True, gamma=gamma)
    cubic_modes = c.coframe_field(coframe_solutions, c.monomials(2))
    cubic_link_rows = c.link_rows(
        point, cubic_cache, A, B, cubic=True, coframe_modes=cubic_modes)
    cubic_coframe_rows = c.solder_rows(
        point, cubic_cache, A, B, cubic=True, coframe_modes=cubic_modes)
    for cubic_amplitude in ((1, 1), (2, 1), (1, 2)):
        require(all(c.exact_zero(row.coeff(cubic_amplitude))
                    for row in cubic_link_rows + cubic_coframe_rows),
                f"joint cubic affine family leaves a 40-row source at {cubic_amplitude}")
    c.MAX_DEGREE = 4
    c.AMPLITUDES = c.monomials(4)

    norm_a = A[0]**2 + A[1]**2
    norm_b = B[0]**2 + B[1]**2
    radius2 = c.X**2 + c.Y**2
    sigma = -norm_a * norm_b * radius2**2 / 128

    def modes(point):
        result = cubic_modes(point)
        result[((2, 2), 0, 0)] = s.expand(sigma.subs({c.X: point[2], c.Y: point[3]}))
        return result

    return point, cubic_cache, modes, tuple(kernel_parameters)


def add_quartic_links(cubic_cache, gamma_quartic):
    """Add total-degree-four link jets to the exact solved cubic cache."""
    def get(point):
        logs = [[[c.Jet(dict(entry.c)) for entry in row] for row in matrix]
                for matrix in cubic_cache(point)]
        for axis in range(4):
            for (added_axis, amplitude, row, col), value in gamma_quartic(point, axis).items():
                if added_axis == axis and sum(amplitude) == 4:
                    terms = dict(logs[axis][row][col].c)
                    terms[amplitude] = s.expand(terms.get(amplitude, 0) + value)
                    logs[axis][row][col] = c.Jet(terms)
        return logs
    return get


def polynomial_degree(expr):
    if c.exact_zero(expr):
        return -1
    return s.Poly(s.expand(expr), c.X, c.Y).total_degree()


def coupled_response(cubic_cache, base_modes, kernel_parameters, max_link_degree,
                     max_link_output_degree, max_coframe_output_degree):
    amplitude = (2, 2)
    input_monomials = c.monomials(max_link_degree)
    link_outputs = c.monomials(max_link_output_degree)
    coframe_outputs = c.monomials(max_coframe_output_degree)
    n_link = 24 * len(input_monomials)
    quartic_link_variables = s.symbols(f"q0:{n_link}")
    variables = tuple(quartic_link_variables) + tuple(kernel_parameters)
    gamma = c.gamma_field({amplitude: s.Matrix(quartic_link_variables)},
                          input_monomials)
    cache = add_quartic_links(cubic_cache, gamma)
    modes = base_modes

    point = (0, 0, c.X, c.Y)
    link = c.link_rows(point, cache, (1, 0), (0, 1), cubic=True,
                       coframe_modes=modes)
    coframe = c.solder_rows(point, cache, (1, 0), (0, 1), cubic=True,
                            coframe_modes=modes)
    vector = c.response_vector(link, coframe, amplitude,
                               link_outputs, coframe_outputs)
    operator = vector.jacobian(variables)
    require(all(entry.is_Rational for entry in operator),
            "quartic response matrix is not over exact rationals")
    zero_variables = {variable: s.Integer(0) for variable in variables}
    base = s.Matrix([entry.xreplace(zero_variables)
                     for entry in vector])
    require(all(entry.is_Rational for entry in base),
            "quartic response source is not over exact rationals")
    defects = [vector[i] - base[i] - sum(
        operator[i, j] * variables[j] for j in range(len(variables)))
        for i in range(vector.rows)]
    require(all(c.exact_zero(defect) for defect in defects),
            "quartic response is not affine in quartic links and cubic solution-kernel modes")
    return (operator, -base, variables, input_monomials,
            link_outputs, coframe_outputs, modes, gamma, link, coframe)


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def main():
    A, B = (1, 0), (0, 1)
    point, cubic_cache, modes, kernel_parameters = source_profile(A, B)
    cache = cubic_cache
    c.check_lorentz_links(cache(point))
    link = c.link_rows(point, cache, A, B, cubic=True, coframe_modes=modes)
    coframe = c.solder_rows(point, cache, A, B, cubic=True, coframe_modes=modes)
    amplitude = (2, 2)
    link_source = [s.expand(row.coeff(amplitude)) for row in link]
    coframe_source = [s.expand(row.coeff(amplitude)) for row in coframe]
    link_degree = max(map(polynomial_degree, link_source))
    coframe_degree = max(map(polynomial_degree, coframe_source))
    # Conservative polynomial support through one spatial degree above the
    # observed link source and one below it for the curvature rows. Release
    # every cubic coframe polynomial mode as well: those modes are invisible
    # through degree three but can enter the quartic source.
    # A degree-five link jet contributes at most degree three to link rows
    # (two finite differences) and degree four to solder rows (one).
    input_degree = max(2, max(link_degree, coframe_degree) + 2)
    base_modes = modes
    (operator, rhs, variables, input_monomials, link_outputs,
     coframe_outputs, modes, gamma_q, link_equations,
     coframe_equations) = coupled_response(
        cache, base_modes, kernel_parameters, input_degree,
        max(2, link_degree), input_degree - 1)
    failure_stage = None
    failure_amplitude = None
    failure_detail = None
    quartic_amplitudes_solved = []
    quartic_amplitudes_attempted = []
    try:
        quartic_amplitudes_attempted.append(amplitude)
        solution, parameters = operator.gauss_jordan_solve(rhs)
        if parameters.rows:
            zero_parameters = {parameter: s.Integer(0)
                               for parameter in parameters}
            solution = solution.applyfunc(lambda entry: entry.xreplace(zero_parameters))
        solved = True
        residual = operator * solution - rhs
        require(all(c.exact_zero(value) for value in residual),
                "exact quartic solution failed substitution into the full response map")
        quartic_amplitudes_solved.append(amplitude)
        n_link = 24 * len(input_monomials)
        source_substitution = {variable: s.Integer(0)
                               for variable in variables[:n_link]}
        source_substitution.update({variable: solution[n_link + i]
                                    for i, variable in enumerate(
                                        variables[n_link:])})

        def freeze_rows(rows):
            return [c.Jet({amp: expression.xreplace(source_substitution)
                           for amp, expression in row.c.items()})
                    for row in rows]

        frozen_link = freeze_rows(link_equations)
        frozen_coframe = freeze_rows(coframe_equations)
        for lower_amplitude in c.monomials(3):
            require(all(c.exact_zero(row.coeff(lower_amplitude))
                        for row in frozen_link + frozen_coframe),
                    f"released cubic coframe mode changes lower Euler row {lower_amplitude}")

        link_response = operator[:, :n_link]
        quartic_link_solutions = {
            amplitude: s.Matrix(solution[:n_link])
        }
        remaining_amplitudes = ((4, 0), (3, 1), (1, 3), (0, 4))
        for quartic_amplitude in remaining_amplitudes:
            quartic_amplitudes_attempted.append(quartic_amplitude)
            source_vector = c.response_vector(
                frozen_link, frozen_coframe, quartic_amplitude,
                link_outputs, coframe_outputs)
            local_link_degree = max(map(
                polynomial_degree,
                [row.coeff(quartic_amplitude) for row in frozen_link]))
            local_coframe_degree = max(map(
                polynomial_degree,
                [row.coeff(quartic_amplitude) for row in frozen_coframe]))
            require(local_link_degree <= max(2, link_degree) and
                    local_coframe_degree <= input_degree - 1,
                    f"quartic source {quartic_amplitude} exceeds declared full support")
            try:
                sector_solution, sector_parameters = link_response.gauss_jordan_solve(
                    -source_vector)
            except ValueError as error:
                failure_stage = "remaining_degree_four_sector"
                failure_amplitude = quartic_amplitude
                raise error
            if sector_parameters.rows:
                zero_parameters = {parameter: s.Integer(0)
                                   for parameter in sector_parameters}
                sector_solution = sector_solution.applyfunc(
                    lambda entry: entry.xreplace(zero_parameters))
            require(all(c.exact_zero(value)
                        for value in link_response * sector_solution + source_vector),
                    f"quartic sector {quartic_amplitude} failed exact substitution")
            quartic_link_solutions[quartic_amplitude] = sector_solution
            quartic_amplitudes_solved.append(quartic_amplitude)

        final_gamma = c.gamma_field(quartic_link_solutions, input_monomials)
        final_cache = add_quartic_links(cache, final_gamma)
        c.check_lorentz_links(final_cache(point))
    except ValueError as error:
        solved = False
        solution = None
        failure_detail = str(error)
        if failure_stage is None:
            failure_stage = "mixed_quartic_sector"
            failure_amplitude = amplitude

    report = {
        "status": ("PASS_FINITE_DEGREE4_40_EULER_JET" if solved else
                   "EXACT_RANGE_OBSTRUCTION_IN_DECLARED_ANSATZ"),
        "scope": "local unwrapped polynomial perturbative jet only",
        "quartic_amplitudes_checked": [
            f"a^{a}*b^{b}" for a, b in quartic_amplitudes_solved],
        "quartic_amplitudes_attempted": [list(amp)
                                         for amp in quartic_amplitudes_attempted],
        "failure_stage": failure_stage,
        "failure_amplitude": (list(failure_amplitude)
                              if failure_amplitude is not None else None),
        "exact_solver_message": failure_detail,
        "mixed_sector_exact_inconsistent": failure_stage == "mixed_quartic_sector",
        "A": [str(v) for v in A],
        "B": [str(v) for v in B],
        "geometry_sigma": "-(x^2+y^2)^2/128",
        "independent_quartic_coframe_modes": False,
        "link_source_rows": 24,
        "coframe_source_rows": 16,
        "joint_cubic_affine_kernel_parameters_released": len(kernel_parameters),
        "quartic_link_unknowns": 24 * len(input_monomials),
        "joint_mixed_response_unknowns": len(variables),
        "all_joint_cubic_family_members_satisfy_affected_lower_40_rows": True,
        "max_link_source_spatial_degree": link_degree,
        "max_coframe_source_spatial_degree": coframe_degree,
        "operator_shape": list(operator.shape),
        "other_quartic_link_response_shape": list(link_response.shape) if solved else None,
        "link_input_spatial_degree": input_degree,
        "link_output_spatial_degree": max(2, link_degree),
        "coframe_output_spatial_degree": input_degree - 1,
        "quartic_sectors_with_exact_solutions": len(quartic_amplitudes_solved),
        "periodic_carrier_root": False,
        "all_order_solution": False,
        "native_price_selection": False,
        "physical_gr_closure": False,
    }
    print(json.dumps(report, indent=2))
    if solved:
        print("PASS all five degree-four amplitude sectors across all 40 finite Euler rows")
        print("PASS exact substitution into complete spatial polynomial support")
        print("PASS all 600 Euler row/amplitude identities through total degree four")
        print("PASS proper-Lorentz link constraint through total degree four")
    else:
        print("PASS exact scoped range obstruction in the declared finite polynomial ansatz")
        print("The full joint cubic affine family is released while solving the")
        print("mixed [a^2*b^2] sector with degree-5 quartic Lorentz-link profiles.")
        print("This does not exclude other geometric profiles, larger link support,")
        print("periodic solutions, or nonpolynomial corrections.")


if __name__ == "__main__":
    main()
