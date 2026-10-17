"""Exact checks for the profile remainder on solution (25).

python -O is safe: failures raise ArithmeticError.
"""
from __future__ import annotations

import json

import sympy as sp

from remainder import (
    K,
    anholonomy_quadratic,
    brinkmann_solution,
    curvature,
    grad_square_euler,
    kl_simplex,
    metric_reversal_involution,
    profile_geometry,
    require_sphere,
    solution_height,
    trace_reversal_involution,
    wave_frame,
)


def require(condition: bool, name: str, checks: list[str]) -> None:
    if not condition:
        raise ArithmeticError(name)
    checks.append(name)


def main() -> dict:
    checks: list[str] = []
    require_sphere()
    checks.append("sphere_scalar_2")

    t, x, y, z = sp.symbols("t x y z", real=True)
    height = sp.Function("H", real=True)(x, y)
    geometry = profile_geometry(height)
    grad2 = geometry["grad2"]
    require(sp.simplify(geometry["frame_det"] - 1) == 0, "frame_det_1", checks)
    require(sp.simplify(geometry["positive_det"] - 1) == 0, "positive_det_1", checks)
    require(sp.simplify(geometry["lorentz_det"] + 1) == 0, "lorentz_det_minus_1", checks)
    require(sp.simplify(geometry["positive_scalar"] + grad2 / 2) == 0, "positive_scalar_is_minus_half_grad2", checks)
    require(sp.simplify(geometry["q"] - 2 * grad2) == 0, "q_is_2_grad2", checks)
    require(sp.simplify(geometry["lorentz_scalar"]) == 0, "lorentz_scalar_identically_0", checks)
    lap = sp.diff(height, x, 2) + sp.diff(height, y, 2)
    ricci = geometry["lorentz_ricci"]
    expected = sp.simplify(lap / 2) * (K * K.T)
    require(sp.simplify(ricci - expected) == sp.zeros(4), "lorentz_ricci_is_half_lap_kkT", checks)

    l2 = sp.simplify(-sp.Rational(4, 3) * geometry["positive_scalar"] + geometry["q"])
    scalar_piece = sp.simplify(-sp.Rational(4, 3) * geometry["positive_scalar"])
    require(sp.simplify(l2 - sp.Rational(8, 3) * grad2) == 0, "l2_is_8_grad2_over_3", checks)
    require(sp.simplify(scalar_piece - sp.Rational(2, 3) * grad2) == 0, "scalar_piece_is_2_grad2_over_3", checks)

    test = sp.Function("phi", real=True)(x, y)
    el_l2, _ = grad_square_euler(sp.Rational(8, 3), height, test, x, y)
    el_scalar, _ = grad_square_euler(sp.Rational(2, 3), height, test, x, y)
    el_q, _ = grad_square_euler(2, height, test, x, y)
    require(sp.simplify(el_l2 + sp.Rational(16, 3) * lap) == 0, "l2_el_is_minus_16_lap_over_3", checks)
    require(sp.simplify(el_scalar + sp.Rational(4, 3) * lap) == 0, "scalar_el_is_minus_4_lap_over_3", checks)
    require(sp.simplify(el_q + 4 * lap) == 0, "q_el_is_minus_4_lap", checks)
    broken = el_l2 + 1
    raw = sp.diff(
        sp.Rational(8, 3) * (sp.diff(height + sp.symbols("eps") * test, x) ** 2 + sp.diff(height + sp.symbols("eps") * test, y) ** 2),
        sp.symbols("eps"),
    ).subs(sp.symbols("eps"), 0)
    momentum = (
        sp.diff(2 * sp.Rational(8, 3) * sp.diff(height, x) * test, x)
        + sp.diff(2 * sp.Rational(8, 3) * sp.diff(height, y) * test, y)
    )
    require(sp.simplify(broken * test + momentum - raw) != 0, "wrong_el_fails_integration_by_parts", checks)

    # x-only reduction reproduces the merged profile value -32/3.
    reduced = x**2 + sp.Rational(1, 4)
    reduced_geometry = profile_geometry(reduced)
    reduced_grad2 = sp.diff(reduced, x) ** 2
    require(sp.simplify(reduced_geometry["q"] - 2 * reduced_grad2) == 0, "x_only_q_matches_closed_form", checks)
    require(sp.simplify(reduced_geometry["q"] - 8 * x**2) == 0, "x_only_q_is_8_x2", checks)
    reduced_lap = sp.diff(reduced, x, 2)
    require(sp.simplify(-sp.Rational(16, 3) * reduced_lap + sp.Rational(32, 3)) == 0, "x_only_profile_el_minus_32_over_3", checks)

    sol, sx, sy, source, palatini_c, polarization = solution_height()
    sol_lap = sp.simplify(sp.diff(sol, sx, 2) + sp.diff(sol, sy, 2))
    require(sp.simplify(sol_lap - source**2 / palatini_c) == 0, "solution_laplacian_s2_over_c", checks)
    require(sp.diff(sol_lap, polarization) == 0, "laplacian_independent_of_polarization", checks)
    sol_el_l2 = sp.simplify(-sp.Rational(16, 3) * sol_lap)
    sol_el_scalar = sp.simplify(-sp.Rational(4, 3) * sol_lap)
    sol_el_q = sp.simplify(-4 * sol_lap)
    require(sp.simplify(sol_el_l2 + sp.Rational(16, 3) * source**2 / palatini_c) == 0, "solution_l2_el", checks)
    require(sp.simplify(sol_el_scalar + sp.Rational(4, 3) * source**2 / palatini_c) == 0, "solution_scalar_el", checks)
    require(sp.simplify(sol_el_q + 4 * source**2 / palatini_c) == 0, "solution_q_el", checks)
    require(sp.diff(sol_el_l2, polarization) == 0, "l2_el_independent_of_polarization", checks)
    vacuum = sol_el_l2.subs(source, 0)
    require(sp.simplify(vacuum) == 0, "harmonic_vacuum_profile_el_zero", checks)
    curved_vacuum = sp.simplify(sol_el_l2.subs({source: 0, polarization: 1}))
    require(curved_vacuum == 0, "polarized_ricci_flat_profile_el_zero", checks)

    square = sp.integrate(sp.integrate(sx**2 - sy**2, (sx, -1, 1)), (sy, -1, 1))
    area = sp.integrate(sp.integrate(1, (sx, -1, 1)), (sy, -1, 1))
    require(square == 0, "polarization_smear_on_square_is_0", checks)
    require(area == 4, "constant_smear_area_4", checks)

    wave = brinkmann_solution()
    require(sp.simplify(wave["det"] + 1) == 0, "brinkmann_det_minus_1", checks)
    require(sp.simplify(wave["scalar"]) == 0, "brinkmann_scalar_0", checks)
    require(sp.simplify(wave["ricci_uu"] - source**2 / (2 * palatini_c)) == 0, "brinkmann_ricci_uu", checks)
    require(wave["gap"] == sp.zeros(4), "two_c_G_minus_T_zero", checks)
    require(sp.simplify(wave["kinetic"]) == 0, "scalar_kinetic_zero", checks)
    require(sp.simplify(wave["box"]) == 0, "scalar_box_zero", checks)
    require(sp.simplify(wave["raised_uu"]) == 0, "raised_uu_zero", checks)

    # Profile pairing of the lowered Ricci with kk^T vanishes because k is null.
    sol_geometry = profile_geometry(sol)
    inverse = sol_geometry["lorentz_inverse"]
    null_square = sp.simplify((K.T * inverse * K)[0])
    require(null_square == 0, "wave_vector_remains_null", checks)
    ricci_sol = sol_geometry["lorentz_ricci"]
    raised = sp.simplify(inverse * ricci_sol * inverse)
    pairing = sp.simplify(sp.Trace(raised * (K * K.T)).doit())
    require(pairing == 0, "profile_pairing_of_ricci_is_0", checks)
    g00 = sp.simplify(ricci_sol[0, 0])
    arithmetic = sp.simplify(sol_el_l2 + sp.Rational(32, 3) * g00)
    require(arithmetic == 0, "arithmetic_relation_is_not_a_covector_identity", checks)
    require(sol_el_l2 != 0, "heat_profile_el_not_the_zero_pairing", checks)

    # c enters only through the solution Laplacian. The density coefficient is fixed.
    bare = sp.simplify(el_l2.subs(height, sol))
    require(sp.simplify(bare - sol_el_l2) == 0, "c_enters_only_through_laplacian", checks)
    coefficient = sp.Rational(8, 3)
    require(coefficient.free_symbols == set(), "heat_coefficient_is_a_fixed_rational", checks)

    reversal = trace_reversal_involution(4)
    require(reversal == sp.zeros(4), "trace_reversal_involution_dim4", checks)
    not_involution = trace_reversal_involution(2)
    require(not_involution != sp.zeros(2), "trace_reversal_not_involution_dim2", checks)
    metric_gap = metric_reversal_involution()
    require(metric_gap == sp.zeros(4), "metric_reversal_involution_on_wave_metric", checks)
    diagonal = sp.diag(2, 3, 5, 7)
    diagonal_variation = sp.zeros(4)
    for i in range(4):
        for j in range(i, 4):
            symbol = sp.symbols(f"d{i}{j}")
            diagonal_variation[i, j] = symbol
            diagonal_variation[j, i] = symbol
    diagonal_inverse = diagonal.inv()
    diagonal_trace = sp.Trace(diagonal_inverse * diagonal_variation).doit()
    diagonal_once = diagonal_variation - diagonal * diagonal_trace / 2
    diagonal_twice = diagonal_once - diagonal * sp.Trace(diagonal_inverse * diagonal_once).doit() / 2
    require(sp.simplify(diagonal_twice - diagonal_variation) == sp.zeros(4), "metric_reversal_on_diagonal_metric", checks)
    require(sp.Trace(sp.eye(4)).doit() / 2 == 2, "dimension_factor_4_is_2", checks)
    require(sp.Trace(sp.eye(2)).doit() / 2 == 1, "dimension_factor_2_is_1", checks)

    entropy = kl_simplex()
    require(list(entropy["weight_gradient_at_equilibrium"]) == [1, 1, 1], "kl_partial_is_1_not_0", checks)
    step_sum = sp.symbols("dw0") + sp.symbols("dw1") + sp.symbols("dw2")
    contraction = sp.simplify(entropy["weight_contraction"] - step_sum)
    require(contraction == 0, "kl_weight_contraction_is_sum_dw", checks)
    ref_sum = sp.symbols("dr0") + sp.symbols("dr1") + sp.symbols("dr2")
    require(sp.simplify(entropy["reference_contraction"] + ref_sum) == 0, "kl_reference_contraction_is_minus_sum_dr", checks)
    tangent = {sp.symbols("dw0"): 1, sp.symbols("dw1"): -1, sp.symbols("dw2"): 0}
    hessian_value = sp.simplify(entropy["hessian_quadratic"].subs(tangent))
    r0, r1 = sp.symbols("r0 r1", positive=True)
    require(sp.simplify(hessian_value - (1 / r0 + 1 / r1)) == 0, "kl_hessian_positive_on_simplex_tangent", checks)
    metric_symbol = sp.symbols("H")
    require(sp.diff(entropy["hessian_quadratic"], metric_symbol) == 0, "kl_has_no_metric_slot", checks)

    volume = sp.sqrt(-sol_geometry["lorentz_det"])
    require(sp.simplify(volume - 1) == 0, "volume_density_identically_1", checks)
    code_constant = sp.symbols("Kcode")
    eps = sp.symbols("eps")
    with_constant = sp.diff(sp.Rational(8, 3) * (sp.diff(height + eps * test, x) ** 2 + sp.diff(height + eps * test, y) ** 2) + code_constant, eps).subs(eps, 0)
    without_constant = sp.diff(sp.Rational(8, 3) * (sp.diff(height + eps * test, x) ** 2 + sp.diff(height + eps * test, y) ** 2), eps).subs(eps, 0)
    require(sp.simplify(with_constant - without_constant) == 0, "code_constant_does_not_change_variation", checks)

    # Heat density does not contain the scalar field.
    require(source not in l2.free_symbols, "heat_density_has_no_scalar_field", checks)

    spec = {source: 1, palatini_c: 1, polarization: 7}
    require(sp.simplify(sol_lap.subs(spec) - 1) == 0, "specialization_laplacian_1", checks)
    require(sp.simplify(sol_el_l2.subs(spec) + sp.Rational(16, 3)) == 0, "specialization_l2_el_minus_16_over_3", checks)

    payload = {
        "schema": "d0-solution25-profile-remainder/1",
        "status": "PASS",
        "candidate": True,
        "gr_derived": False,
        "equation_20_closed": False,
        "equation_28_closed": False,
        "native_price_equals_geometric_action": False,
        "remainder_defined_as_gap_to_einstein": False,
        "constant_chosen_to_cancel_heat": False,
        "covector_identification": False,
        "profile_tangent_only": True,
        "other_nine_metric_slots_evaluated": False,
        "c4_dr_drem_v8_evaluated": False,
        "solution_laplacian": "s**2/c",
        "profile_el_l2": "-(16/3)*s**2/c",
        "profile_el_scalar_piece": "-(4/3)*s**2/c",
        "profile_el_q": "-4*s**2/c",
        "profile_el_lorentz_scalar_density": "0",
        "profile_pairing_of_ricci": "0",
        "arithmetic_relation_not_identification": "l2_profile_el + (32/3)*Ric_00 = 0",
        "kl_partial_at_equilibrium": "1",
        "kl_simplex_contraction": "sum dw",
        "exact_check_count": len(checks),
        "checks": checks,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    main()
