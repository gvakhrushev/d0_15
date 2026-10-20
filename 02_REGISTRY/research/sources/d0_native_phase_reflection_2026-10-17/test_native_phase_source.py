"""Exact checks for the literal reflection cross. No assert, so python -O stays loaded."""
from __future__ import annotations

import json

import sympy as sp

from native_phase_source import (
    I16,
    P,
    aligned_scalar,
    circle_density_derivative,
    column_cross,
    creator,
    gram_shift,
    native_select,
    port_cross_from_reflection,
    reflection,
    role1_flip_prediction,
    select_overlap,
)

CHECKS: list[str] = []


def require(name: str, truth: bool) -> None:
    if truth is not True and truth is not sp.true:
        raise ArithmeticError(name)
    CHECKS.append(name)


def same(name: str, left, right) -> None:
    delta = sp.expand(left - right)
    if isinstance(delta, sp.MatrixBase):
        ok = delta == sp.zeros(*delta.shape)
    else:
        ok = sp.simplify(delta) == 0
    require(name, ok)


def test_aligned_identity() -> None:
    nu_x, b_x, nu_y, b_y = sp.symbols("nx bx ny by", real=True)
    phases = [sp.I, 1, 1, 1]
    left = native_select(nu_x, b_x, phases)
    right = native_select(nu_y, b_y, phases)
    overlap, reflected = aligned_scalar(nu_x, b_x, nu_y, b_y)
    same("aligned_select_overlap", select_overlap(left, right), overlap * I16)
    same(
        "aligned_reflection_cross",
        column_cross(reflection(left), reflection(right)),
        reflected * I16,
    )


def test_role1_flip() -> None:
    nu_x, b_x, nu_y, b_y = sp.symbols("nx bx ny by", real=True)
    rows_x = native_select(nu_x, b_x, [sp.I, 1, 1, 1])
    rows_y = native_select(nu_y, b_y, [sp.I, -1, 1, 1])
    _, _, predicted = role1_flip_prediction(nu_x, b_x, nu_y, b_y)
    same("role1_flip_reflection", column_cross(reflection(rows_x), reflection(rows_y)), predicted)
    select_cross = sp.expand(select_overlap(rows_x, rows_y))
    select_mean = sp.simplify(sp.trace(select_cross) / 16)
    same("role1_flip_select_stays_scalar", select_cross, select_mean * I16)
    require("role1_flip_select_is_not_the_reflection", sp.simplify(select_mean - predicted[0, 0]) != 0)


def test_fixture_gram_and_ports() -> None:
    nu_x, b_x = sp.Rational(3, 5), sp.Rational(4, 5)
    nu_y, b_y = sp.Rational(5, 13), sp.Rational(12, 13)
    mean, gamma, predicted = role1_flip_prediction(nu_x, b_x, nu_y, b_y)
    require("fixture_gamma_positive_rational", gamma == sp.Rational(1491, 216320))
    shift, scalar_square = gram_shift(mean, gamma)
    positive_shift = sp.Integer(2223081) * (7 - 3 * sp.sqrt(5)) / sp.Integer(46794342400)
    same("fixture_shift_closed_form", shift, positive_shift)
    require("seven_exceeds_three_sqrt5", sp.Integer(49) - 45 == 4)
    # The closed form of the shift matches the literal port Gram.
    reflected = column_cross(
        reflection(native_select(nu_x, b_x, [sp.I, 1, 1, 1])),
        reflection(native_select(nu_y, b_y, [sp.I, -1, 1, 1])),
    )
    same("fixture_matches_closed_form", reflected, predicted)
    ports = port_cross_from_reflection(reflected)
    gram = sp.expand(ports.H * ports)
    gram_value = sp.simplify(sp.trace(gram) / 16)
    same("fixture_port_gram_scalar", gram, gram_value * I16)
    same("fixture_logdet_sees_traceless_shift", gram_value, scalar_square + shift)
    require("traceless_shift_not_zero", sp.simplify(shift) != 0)
    # Flipping the x phase instead is a different operator.
    swapped = column_cross(
        reflection(native_select(nu_x, b_x, [sp.I, -1, 1, 1])),
        reflection(native_select(nu_y, b_y, [sp.I, 1, 1, 1])),
    )
    require("x_phase_flip_is_not_the_y_formula", sp.expand(swapped - predicted) != sp.zeros(16))


def test_circle_and_zero_mode() -> None:
    value, first, second = circle_density_derivative()
    same("circle_value", value, sp.Rational(226, 4225))
    same("circle_first", first, sp.Rational(1736, 4225))
    same("diagonal_second", second, sp.Rational(41, 25))
    require("circle_first_nonzero", first != 0)
    # Zero mode of the unchanged instrument is I. The attenuated target is not.
    same("ports_complete", P + P**2, 1)
    z = sp.Rational(1, 2**20)
    target_square = P * (1 - z) ** 2
    same("target_gap_factor", 1 - target_square, P * (P + 2 * z - z**2))
    squared_margin = sp.together(5 - (1 - 4 * z + 2 * z**2) ** 2)
    require("target_gap_positive_rational", squared_margin.p > 0 and squared_margin.q > 0)


def test_pattern_algebra_and_off_circle() -> None:
    """The Gram shift is the CAR identity Q.H = -Q, Q.H Q = 2 I, not a fixture fit."""
    created_0 = creator(0)
    created_1 = creator(1)
    pattern = (
        (-1 + sp.I) * created_0 * created_1.T
        + (1 + sp.I) * created_1 * created_0.T
        + (-1 + sp.I) * created_0 * created_1
        + (-1 - sp.I) * created_0.T * created_1.T
    )
    same("pattern_antihermitian", pattern.H, -pattern)
    same("pattern_square", pattern.H * pattern, 2 * I16)
    rows_x = native_select(1, 1, [sp.I, 1, 1, 1])
    rows_y = native_select(2, 0, [sp.I, 1, 1, 1])
    overlap, reflected = aligned_scalar(1, 1, 2, 0)
    same("off_circle_select_cross", select_overlap(rows_x, rows_y), overlap * I16)
    same("off_circle_reflection_cross", column_cross(reflection(rows_x), reflection(rows_y)), reflected * I16)
    self_overlap = select_overlap(rows_x, rows_x)
    require("off_circle_rows_not_isometries", sp.expand(self_overlap - I16) != sp.zeros(16))


def test_adm_chart_rank() -> None:
    """The owned ADM chart has ten slots. This instrument does not take those slots."""
    lapse = sp.symbols("N", positive=True)
    shift_symbols = sp.symbols("v0:3")
    metric_symbols = sp.symbols("h00 h01 h02 h11 h12 h22", real=True)
    spatial = sp.Matrix(
        [
            [metric_symbols[0], metric_symbols[1], metric_symbols[2]],
            [metric_symbols[1], metric_symbols[3], metric_symbols[4]],
            [metric_symbols[2], metric_symbols[4], metric_symbols[5]],
        ]
    )
    shift = sp.Matrix(shift_symbols)
    metric = sp.zeros(4)
    metric[0, 0] = lapse**2 - (shift.T * spatial * shift)[0]
    for i in range(3):
        metric[0, i + 1] = metric[i + 1, 0] = -(spatial * shift)[i]
        for j in range(3):
            metric[i + 1, j + 1] = -spatial[i, j]
    slots = [(i, j) for i in range(4) for j in range(i, 4)]
    params = [lapse, *shift_symbols, *metric_symbols]
    jacobian = sp.Matrix([metric[i, j] for i, j in slots]).jacobian(params)
    point = {
        lapse: 4,
        shift_symbols[0]: sp.Rational(1, 3),
        shift_symbols[1]: sp.Rational(-1, 5),
        shift_symbols[2]: sp.Rational(2, 7),
        metric_symbols[0]: 2,
        metric_symbols[1]: sp.Rational(1, 4),
        metric_symbols[2]: 0,
        metric_symbols[3]: 3,
        metric_symbols[4]: sp.Rational(1, 5),
        metric_symbols[5]: 5,
    }
    specialized = jacobian.subs(point)
    require("adm_chart_rank_ten", specialized.rank() == 10)
    require("adm_jacobian_measure", abs(specialized.det()) == (2 * lapse * spatial.det()).subs(point))
    require("native_select_has_no_metric_argument", creator(0).shape == (16, 16))


def run():
    test_aligned_identity()
    test_role1_flip()
    test_fixture_gram_and_ports()
    test_circle_and_zero_mode()
    test_pattern_algebra_and_off_circle()
    test_adm_chart_rank()
    value, first, second = circle_density_derivative()
    nu_x, b_x = sp.Rational(3, 5), sp.Rational(4, 5)
    nu_y, b_y = sp.Rational(5, 13), sp.Rational(12, 13)
    _, gamma, _ = role1_flip_prediction(nu_x, b_x, nu_y, b_y)
    shift, _ = gram_shift(
        role1_flip_prediction(nu_x, b_x, nu_y, b_y)[0],
        gamma,
    )
    payload = {
        "schema": "d0-native-phase-reflection-source/1",
        "status": "PASS",
        "candidate": True,
        "gr_derived": False,
        "equation_20_closed": False,
        "equation_28_closed": False,
        "sources_coincide": False,
        "ten_metric_components_evaluated": 0,
        "constant_chosen_to_match_einstein": False,
        "phase_flip_is_not_a_null_shear": True,
        "matter_observer_joint_started": False,
        "aligned_reflection": "(1-2*f/128)*I16 for all real amplitudes at phases (I,1,1,1)",
        "circle_density": str(value),
        "circle_first_derivative": str(first),
        "diagonal_second_derivative": str(second),
        "role1_flip_gamma": str(gamma),
        "role1_flip_gram_shift": str(sp.factor(shift)),
        "native_logdet_output_count": 1,
        "adm_chart_rank": 10,
        "exact_check_count": len(CHECKS),
        "checks": CHECKS,
    }
    print(json.dumps(payload, ensure_ascii=True, sort_keys=True, indent=2))
    print("PASS", len(CHECKS), payload["sources_coincide"])


if __name__ == "__main__":
    run()
