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
    """Return all checked cubic fields and the geometry-fixed quartic sigma."""
    point = (0, 0, c.X, c.Y)
    c.MAX_DEGREE = 3
    c.AMPLITUDES = c.monomials(3)
    _, extra, full_cubic_cache, _, _ = c.solve_full_cubic_40(A, B)
    c.MAX_DEGREE = 4
    c.AMPLITUDES = c.monomials(4)

    coframe_solutions = {}
    for amplitude, (_, coframe_solution) in extra.items():
        coframe_solutions[amplitude] = coframe_solution

    cubic_modes = c.coframe_field(coframe_solutions, c.monomials(2))
    norm_a = A[0]**2 + A[1]**2
    norm_b = B[0]**2 + B[1]**2
    radius2 = c.X**2 + c.Y**2
    sigma = -norm_a * norm_b * radius2**2 / 128

    def modes(point):
        result = cubic_modes(point)
        result[((2, 2), 0, 0)] = s.expand(sigma.subs({c.X: point[2], c.Y: point[3]}))
        return result

    return point, full_cubic_cache, modes


def add_quartic_links(cubic_cache, gamma_quartic):
    """Add only [a^2 b^2] link jets to the exact solved cubic cache."""
    def get(point):
        logs = [[[c.Jet(dict(entry.c)) for entry in row] for row in matrix]
                for matrix in cubic_cache(point)]
        for axis in range(4):
            for (added_axis, amplitude, row, col), value in gamma_quartic(point, axis).items():
                if added_axis == axis and amplitude == (2, 2):
                    terms = dict(logs[axis][row][col].c)
                    terms[amplitude] = s.expand(terms.get(amplitude, 0) + value)
                    logs[axis][row][col] = c.Jet(terms)
        return logs
    return get


def polynomial_degree(expr):
    if c.exact_zero(expr):
        return -1
    return s.Poly(s.expand(expr), c.X, c.Y).total_degree()


def coupled_response(cubic_cache, base_modes, max_link_degree,
                     max_link_output_degree, max_coframe_output_degree):
    amplitude = (2, 2)
    input_monomials = c.monomials(max_link_degree)
    link_outputs = c.monomials(max_link_output_degree)
    coframe_outputs = c.monomials(max_coframe_output_degree)
    n_link = 24 * len(input_monomials)
    n_coframe_per_amplitude = 16 * len(c.monomials(2))
    n_coframe = 2 * n_coframe_per_amplitude
    variables = s.symbols(f"q0:{n_link + n_coframe}")
    gamma = c.gamma_field({amplitude: s.Matrix(variables[:n_link])},
                          input_monomials)
    cache = add_quartic_links(cubic_cache, gamma)
    cubic_kernel = c.coframe_field({
        (2, 1): s.Matrix(variables[n_link:n_link + n_coframe_per_amplitude]),
        (1, 2): s.Matrix(variables[n_link + n_coframe_per_amplitude:]),
    }, c.monomials(2))

    def modes(point):
        result = base_modes(point)
        for key, value in cubic_kernel(point).items():
            result[key] = s.expand(result.get(key, 0) + value)
        return result

    point = (0, 0, c.X, c.Y)
    link = c.link_rows(point, cache, (1, 0), (0, 1), cubic=True,
                       coframe_modes=modes)
    coframe = c.solder_rows(point, cache, (1, 0), (0, 1), cubic=True,
                            coframe_modes=modes)
    vector = c.response_vector(link, coframe, amplitude,
                               link_outputs, coframe_outputs)
    operator = vector.jacobian(variables)
    zero_variables = {variable: s.Integer(0) for variable in variables}
    base = s.Matrix([entry.xreplace(zero_variables)
                     for entry in vector])
    defects = [vector[i] - base[i] - sum(
        operator[i, j] * variables[j] for j in range(len(variables)))
        for i in range(vector.rows)]
    require(all(c.exact_zero(defect) for defect in defects),
            "quartic response is not affine in link/coframe correction modes")
    return (operator, -base, variables, input_monomials,
            link_outputs, coframe_outputs, modes, gamma)


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def main():
    A, B = (1, 0), (0, 1)
    point, cubic_cache, modes = source_profile(A, B)
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
     coframe_outputs, modes, gamma_q) = coupled_response(
        cache, base_modes, input_degree, max(2, link_degree),
        input_degree - 1)
    try:
        solution, parameters = operator.gauss_jordan_solve(rhs)
        if parameters.rows:
            zero_parameters = {parameter: s.Integer(0)
                               for parameter in parameters}
            solution = solution.applyfunc(lambda entry: entry.xreplace(zero_parameters))
        solved = True
        residual = operator * solution - rhs
        require(all(c.exact_zero(value) for value in residual),
                "exact quartic solution failed substitution into the full response map")
        n_link = 24 * len(input_monomials)
        final_gamma = c.gamma_field({amplitude: s.Matrix(solution[:n_link])},
                                   input_monomials)
        final_cache = add_quartic_links(cache, final_gamma)
        c.check_lorentz_links(final_cache(point))
    except ValueError:
        solved = False
        solution = None

    report = {
        "status": "PASS_QUARTIC_FINITE_40_JET" if solved else "NO_RANGE_SOLUTION_IN_DECLARED_ANSATZ",
        "scope": "local unwrapped polynomial perturbative jet only",
        "amplitude": "a^2*b^2",
        "A": [str(v) for v in A],
        "B": [str(v) for v in B],
        "geometry_sigma": "-(x^2+y^2)^2/128",
        "link_source_rows": 24,
        "coframe_source_rows": 16,
        "cubic_coframe_kernel_modes_released": 192,
        "max_link_source_spatial_degree": link_degree,
        "max_coframe_source_spatial_degree": coframe_degree,
        "operator_shape": list(operator.shape),
        "link_input_spatial_degree": input_degree,
        "link_output_spatial_degree": max(2, link_degree),
        "coframe_output_spatial_degree": input_degree - 1,
        "periodic_carrier_root": False,
        "all_order_solution": False,
        "native_price_selection": False,
        "physical_gr_closure": False,
    }
    print(json.dumps(report, indent=2))
    if solved:
        print("PASS all 40 quartic finite Euler equations over complete polynomial support")
        print("PASS exact substitution into the 480-row response system")
        print("PASS proper-Lorentz link constraint through total degree four")
    else:
        print("PASS exact scoped obstruction: even after releasing all cubic coframe")
        print("modes and degree-5 quartic link modes, this selected cubic link witness")
        print("has no root in the declared polynomial range; cubic link kernels and")
        print("nonpolynomial or periodic corrections remain unclassified.")


if __name__ == "__main__":
    main()
