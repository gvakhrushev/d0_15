#!/usr/bin/env python3
"""Exact endpoint-metric test on the AF/CAR-welded blank source orbit.

This checks one proposed direct join: retain the owned CAR record gate, read
the positive observer pairing from the correlated CAR current at each end,
and require the full exterior Gram to be transported isometrically. A single
exact scalar-column defect rejects that join; no other joint link/gate update
is classified here.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import sympy as s


ROOT = Path(__file__).resolve().parents[3]
CERT = ROOT / "02_REGISTRY" / "research" / "certificates"
BASE = "f1270f63cffa5fcfc27b469ff2517d8398d5362a"
INPUTS = {
    "a4d_native_reference_memory_preparation.py": "67e416c75cc213efca6040cea8cb796efbcff78037e09b31fb6a83acdcfd0e3a",
    "a4d_native_correlated_current_transition.py": "e659733a8ab4fea30f46de56663dc344249420c7e0a3ea65b2aa1a2091b76e0d",
    "a4d_native_record_metric_chronology_check.py": "16929d026206ee69e126484ed2ac7b1dfd2537c1e50c0fc4c4293408caf58527",
    "a4d_native_fock_record_binding_check.py": "42e83e6f93b48ce4d4420f829d8e79c993a215d7b1a4c6a2f812bd45fd914078",
}


def load(stem: str):
    path = CERT / (stem + ".py")
    spec = importlib.util.spec_from_file_location(stem, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"CANNOT_LOAD_PINNED_OWNER:{stem}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


P = load("a4d_native_reference_memory_preparation")
O = load("a4d_native_correlated_current_transition")
C = load("a4d_native_record_metric_chronology_check")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def interval_add(x, y):
    return (x[0] + y[0], x[1] + y[1])


def interval_mul(x, y):
    products = (x[0] * y[0], x[0] * y[1], x[1] * y[0], x[1] * y[1])
    return (min(products), max(products))


def interval_power(x, exponent: int):
    result = (s.Rational(1), s.Rational(1))
    for _ in range(exponent):
        result = interval_mul(result, x)
    return result


def polynomial_interval(expression, boxes):
    variables = list(boxes)
    poly = s.Poly(expression, *variables, domain=s.QQ)
    total = (s.Rational(0), s.Rational(0))
    for powers, coefficient in poly.terms():
        term = (coefficient, coefficient)
        for variable, exponent in zip(variables, powers):
            term = interval_mul(term, interval_power(boxes[variable], exponent))
        total = interval_add(total, term)
    return total


def run() -> dict:
    for name, expected in INPUTS.items():
        actual = digest(CERT / name)
        if actual != expected:
            raise AssertionError(f"PIN_MISMATCH:{name}:{actual}")

    a, p, fugacity = P.a, P.p, P.z
    eta = s.diag(1, -1, -1, -1)
    I4, I16 = s.eye(4), s.eye(16)
    blank = O.blank_code()
    m0 = P.mat(blank * s.Matrix([a, p]))
    U, _, blank_projector = P.full_tuple()
    U = P.mat(U)
    m1 = P.mat(U * m0)

    def require(name: str, proposition: bool, checks: list[str]) -> None:
        if not proposition:
            raise AssertionError("FAILED:" + name)
        checks.append(name)

    checks: list[str] = []
    require("actual_full_blank_projector", P.mat(blank_projector * m0 - m0) == s.zeros(16, 1), checks)
    require("unit_norm_blank_state", P.red((m0.T * m0)[0] - 1) == 0, checks)
    require("literal_gate_isometry_at_initial_pairing", P.mat(U.T * U - I16) == s.zeros(16), checks)

    J0 = P.mat(O.current(I4, m0))
    J1 = P.mat(O.current(I4, m1))
    j1_expected = s.Matrix([1, 2 * a * p, 0, 0])
    require("blank_correlated_current_is_rest", J0 == s.Matrix([1, 0, 0, 0]), checks)
    require("one_literal_tick_gives_owned_source_current", P.mat(J1 - j1_expected) == s.zeros(4, 1), checks)

    h0 = P.mat(O.observer_pairing(eta, J0))
    h1 = P.mat(O.observer_pairing(eta, J1))
    jnorm = P.red((J1.T * eta * J1)[0])
    h1_expected = s.Matrix(
        [
            [2 / p**6 - 1, -4 * a * p / p**6, 0, 0],
            [-4 * a * p / p**6, 2 / p**6 - 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
    )
    require("source_current_timelike_norm_is_p6", P.red(jnorm - p**6) == 0, checks)
    require("source_pairing_exact_full_matrix", P.mat(h1 - h1_expected) == s.zeros(4), checks)
    require("initial_pairing_is_identity", h0 == I4, checks)
    require(
        "source_pairing_is_positive",
        P.red(h1[0, 0] - 1 - 8 / p**3) == 0
        and P.red(h1[:2, :2].det() - 1) == 0,
        checks,
    )

    W0 = P.mat(C.ext(h0))
    W1 = P.mat(C.ext(h1))
    require("initial_full_exterior_gram_is_identity", W0 == I16, checks)
    e_scalar = I16[:, 0]
    u_scalar = P.mat(U * e_scalar)
    require("literal_gate_scalar_column", u_scalar == a * I16[:, 0] + p * I16[:, 1], checks)
    defect = P.red((u_scalar.T * W1 * u_scalar)[0] - (e_scalar.T * W0 * e_scalar)[0])
    expected_defect = P.red(8 / p)
    require("exact_endpoint_norm_defect_is_8_over_p", P.red(defect - expected_defect) == 0, checks)
    require("defect_is_strictly_positive", P.red(expected_defect - 8 - 8 * p) == 0, checks)
    require("full_endpoint_isometry_fails", P.red(defect) != 0, checks)

    frozen_defect = P.mat(U.T * W0 * U - W0)
    require("frozen_pairing_control_has_zero_defect", frozen_defect == s.zeros(16), checks)
    reverse = s.Matrix([1, -2 * a * p, 0, 0])
    h_reverse = P.mat(O.observer_pairing(eta, reverse))
    reverse_defect = P.red((u_scalar.T * P.mat(C.ext(h_reverse)) * u_scalar)[0] - 1)
    require("opposite_current_has_same_positive_scalar_defect", P.red(reverse_defect - expected_defect) == 0, checks)

    # The already-owned endpoint-frame transport repairs this Gram defect,
    # but only by moving the complete CAR frame and its pairing together.
    # Its two-tick product telescopes back to the original U^2.
    require("source_pairing_has_unit_determinant", P.red(h1.det() - 1) == 0, checks)
    frame = s.eye(4)
    y, zeta = h1[0, 1], h1[1, 1]
    frame[0, 0] = s.sqrt(zeta)
    frame[1, 0] = -y / s.sqrt(zeta)
    frame[1, 1] = 1 / s.sqrt(zeta)
    require(
        "source_pairing_has_oriented_endpoint_frame",
        s.simplify(frame.det() - 1) == 0
        and P.mat(s.simplify(frame * frame.T * h1 - I4)) == s.zeros(4),
        checks,
    )
    E1, W1_frame = P.endpoint_frame(frame)
    require("endpoint_owner_realizes_current_exterior_pairing", P.mat(W1_frame - C.ext(h1)) == s.zeros(16), checks)
    require(
        "current_endpoint_frame_is_full16_isometry",
        P.mat(s.simplify(E1.T * W1_frame * E1 - I16)) == s.zeros(16),
        checks,
    )
    transported_tick = E1 * U
    require(
        "moving_frame_gate_restores_endpoint_isometry",
        P.mat(s.simplify(transported_tick.T * W1_frame * transported_tick - I16)) == s.zeros(16),
        checks,
    )
    transported_return = U * E1.T * W1_frame
    require(
        "two_tick_moving_frame_transport_telescopes",
        P.mat(s.simplify(transported_return * transported_tick - U * U)) == s.zeros(16),
        checks,
    )
    U2 = P.mat(U * U)
    _, cut, _ = P.full_tuple()
    cut = P.mat(cut)
    F2 = P.mat(cut * U2.T * (I16 - cut) * U2 * cut)
    require(
        "frame_repair_retains_original_two_tick_price",
        P.red((I16 - fugacity * F2).det() - (1 - 4 * fugacity * p**3) ** 4) == 0,
        checks,
    )

    # Cross-owner hostile control: the full-CAR current and the chronology's
    # first-grade observer coincide initially, then cease to define the same
    # timelike observer after the chronology's own metric update.
    chrono_blank4 = s.Matrix(
        [[1, 0, 1, 0], [0, 1, 0, 1], [1, 0, 1, 0], [0, 1, 0, 1]]
    ) / 2
    chrono_blank = C.B0 * s.kronecker_product(chrono_blank4, s.eye(4)) * C.B0.T
    chrono_state = s.zeros(16, 1)
    for index, value in {
        0: -a / 2,
        14: -a / 2,
        1: p / 2,
        15: p / 2,
        3: s.Rational(1, 2),
        13: s.Rational(1, 2),
    }.items():
        chrono_state[index] = value
    require("c0_chronology_input_is_actual_whole_blank", C.zero(chrono_blank * chrono_state - chrono_state), checks)
    chrono_first0 = C.first(chrono_state)
    rest_observer = s.Matrix([1, 0, 0, 0])
    require("c0_initial_first_grade_selects_rest", C.zero(chrono_first0 - p * rest_observer / 2), checks)
    chrono_current0 = P.mat(O.current(I4, chrono_state))
    require("c0_initial_full_car_current_is_same_rest_observer", chrono_current0 == rest_observer, checks)
    U_chrono, _ = C.record(I4, rest_observer)
    require("c0_chronology_gate_is_the_same_owned_full_car_gate", C.zero(U_chrono - U), checks)
    chrono_state1 = C.mat(U_chrono * chrono_state)
    w1 = C.first(chrono_state1)
    require("c0_first_tick_chronological_grade_is_exact", C.zero(w1 - s.Matrix([0, -p / 2, 0, 0])), checks)
    q1 = C.mat(-I4 + 2 * w1 * w1.T / (w1.T * w1)[0])
    q1_expected = s.diag(-1, 1, -1, -1)
    require("c0_first_tick_updates_metric_to_lorentz_q1", C.zero(q1 - q1_expected), checks)
    chrono_current1 = P.mat(O.current(I4, chrono_state1))
    require(
        "c0_first_tick_full_car_current_is_exact",
        P.mat(chrono_current1 - s.Matrix([1, -a, 0, 0])) == s.zeros(4, 1),
        checks,
    )
    current_norm_q1 = P.red((chrono_current1.T * q1.inv() * chrono_current1)[0])
    require("c0_updated_metric_current_norm_is_minus_p_squared", P.red(current_norm_q1 + p**2) == 0, checks)
    h_current_q1 = P.mat(O.observer_pairing(q1, chrono_current1))
    require(
        "c0_updated_current_observer_pairing_is_not_positive",
        P.red(h_current_q1[0, 0] - (1 - 2 / p**2)) == 0
        and s.simplify((1 - 2 / ((s.sqrt(5) - 1) / 2) ** 2)).is_negative is True,
        checks,
    )

    # The mismatch also holds at an interior feedback-only stationary point,
    # found by rational interval signs rather than a decimal root.
    angle, sine = s.symbols("chronology_angle chronology_sine", real=True)
    p_lower, p_upper = s.Rational(6180, 10000), s.Rational(6181, 10000)
    a_lower, a_upper = s.Rational(7861, 10000), s.Rational(7862, 10000)
    require(
        "positive_golden_root_is_inside_rational_p_interval",
        p_lower**2 + p_lower - 1 < 0 and p_upper**2 + p_upper - 1 > 0,
        checks,
    )
    require(
        "positive_golden_square_root_is_inside_rational_a_interval",
        a_lower**2 < p_lower and a_upper**2 > p_upper,
        checks,
    )
    lam, tr, det, tr0, det0 = C.polynomials(angle)
    z_test = s.Rational(1, 2)
    A_test = 1 - z_test * lam
    B_test = 1 - z_test * tr + z_test**2 * det
    C_test = 1 - z_test * tr0 + z_test**2 * det0
    nu = s.expand(
        -(2 * s.diff(A_test, angle) * B_test * C_test
          + 2 * s.diff(B_test, angle) * A_test * C_test
          + s.diff(C_test, angle) * A_test * B_test)
    )
    p_chrono = C.p
    nu_left = polynomial_interval(
        nu.subs(angle, -s.Rational(33, 100)), {p_chrono: (p_lower, p_upper)}
    )
    nu_right = polynomial_interval(
        nu.subs(angle, -s.Rational(32, 100)), {p_chrono: (p_lower, p_upper)}
    )
    require("feedback_derivative_is_negative_at_left_bracket", nu_left[1] < 0, checks)
    require("feedback_derivative_is_positive_at_right_bracket", nu_right[0] > 0, checks)

    family = s.zeros(16, 1)
    for index, value in {
        0: (angle - a) / p,
        14: (angle - a) / p,
        1: 1,
        15: 1,
        3: sine / p,
        13: sine / p,
    }.items():
        family[index] = value
    blank4 = s.Matrix(
        [[1, 0, 1, 0], [0, 1, 0, 1], [1, 0, 1, 0], [0, 1, 0, 1]]
    ) / 2
    blank_family = C.B0 * s.kronecker_product(blank4, s.eye(4)) * C.B0.T
    joint_ideal = s.groebner(
        [a * a - p, p * p + p - 1, sine * sine + angle * angle - 1],
        a,
        p,
        sine,
        domain=s.QQ.frac_field(angle),
        order="grevlex",
    )

    def in_joint_ideal(expression) -> bool:
        numerator, _ = s.cancel(expression).as_numer_denom()
        return joint_ideal.reduce(s.expand(numerator))[1] == 0

    require(
        "whole_blank_chronology_family_retained_for_stationary_bracket",
        all(in_joint_ideal(value) for value in blank_family * family - family),
        checks,
    )
    U_family, _ = C.record(I4, rest_observer)
    family_next = U_family * family
    family_current = P.mat(O.current(I4, family_next))
    expected_family_current = s.Matrix([1, sine * (angle - a) / (1 - a * angle), 0, 0])
    require(
        "all_angle_full_car_current_on_chronology_family",
        all(in_joint_ideal(value) for value in family_current - expected_family_current),
        checks,
    )
    w_family = s.Matrix([angle, -sine, 0, 0])
    q_family = -I4 + 2 * w_family * w_family.T
    family_norm = s.cancel(
        (expected_family_current.T * q_family * expected_family_current)[0]
    )
    norm_num, norm_den = s.cancel(family_norm).as_numer_denom()
    norm_num = s.Poly(norm_num, sine).rem(
        s.Poly(sine**2 + angle**2 - 1, sine)
    ).as_expr()
    norm_den = s.Poly(norm_den, sine).rem(
        s.Poly(sine**2 + angle**2 - 1, sine)
    ).as_expr()
    expected_norm = (
        8 * a**2 * angle**4 - 8 * a**2 * angle**2 + a**2
        - 8 * a * angle**5 + 2 * a * angle**3 + 4 * a * angle
        + 2 * angle**6 + angle**4 - angle**2 - 1
    ) / (a * angle - 1) ** 2
    require(
        "chronology_metric_current_norm_exact_all_angle_formula",
        s.factor(norm_num / norm_den - expected_norm) == 0,
        checks,
    )
    norm_num_interval = polynomial_interval(
        norm_num,
        {
            a: (a_lower, a_upper),
            angle: (-s.Rational(33, 100), -s.Rational(32, 100)),
        },
    )
    norm_den_interval = polynomial_interval(
        norm_den,
        {
            a: (a_lower, a_upper),
            angle: (-s.Rational(33, 100), -s.Rational(32, 100)),
        },
    )
    require("stationary_bracket_current_norm_numerator_is_negative", norm_num_interval[1] < 0, checks)
    require("stationary_bracket_current_norm_denominator_is_positive", norm_den_interval[0] > 0, checks)

    return {
        "schema": "d0-native-source-endpoint-metric/1",
        "status": "PASS",
        "input_source_head": BASE,
        "input_sha256": INPUTS,
        "checks": checks,
        "exact_controls": len(checks),
        "witness": {
            "initial_current": "(1,0,0,0)",
            "one_tick_current": "(1,2*a*p,0,0)",
            "current_norm_squared": "p^6",
            "source_pairing_00": "2/p^6-1",
            "scalar_column_endpoint_norm_defect": "8/p=8*(1+p)>0",
            "diagnostic_chronology_stationary_point": {
                "fugacity": "1/2",
                "angle_bracket": ["-33/100", "-32/100"],
                "p_interval": [str(p_lower), str(p_upper)],
                "a_interval": [str(a_lower), str(a_upper)],
                "feedback_numerator_at_left": [str(nu_left[0]), str(nu_left[1])],
                "feedback_numerator_at_right": [str(nu_right[0]), str(nu_right[1])],
                "CAR_current_norm_numerator_on_bracket": [
                    str(norm_num_interval[0]),
                    str(norm_num_interval[1]),
                ],
                "CAR_current_norm_denominator_on_bracket": [
                    str(norm_den_interval[0]),
                    str(norm_den_interval[1]),
                ],
                "interior_feedback_only_stationary_point": True,
                "physical_admission_or_full_action_root": False,
            },
        },
        "scope": "fixed rest frame, literal owned full-CAR gate, current-defined positive observer pairing, existing pure endpoint-frame transport, the c=0 chronology witness, and a diagnostic feedback-only stationary interval",
        "pure_endpoint_frame_transport_repairs_isometry": True,
        "pure_endpoint_frame_transport_changes_two_tick_price": False,
        "c0_chronology_and_full_car_observers_agree_initially": True,
        "c0_full_car_current_remains_timelike_after_chronology_metric_update": False,
        "diagnostic_chronology_stationary_mismatch": {
            "fugacity": "1/2_NOT_A_PHYSICAL_RULE",
            "angle_interval": "[-33/100,-32/100]",
            "feedback_derivative_signs": "NEGATIVE_AT_LEFT_POSITIVE_AT_RIGHT",
            "full_car_current_norm_in_updated_metric": "STRICTLY_NEGATIVE_ON_INTERVAL",
            "interior_feedback_only_stationary_point_exists": True,
            "physical_admission_or_full_action_stationarity": False,
        },
        "other_joint_link_or_gate_updates_classified": False,
        "physical_admission": False,
        "full_native_q_D_b_m_transition": False,
        "source_Ward_stationarity_GR_closed": False,
        "new_Lean_compilation": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = run()
    result["checker_sha256"] = digest(Path(__file__))
    output = CERT / "a4d_native_source_endpoint_metric_results.json"
    if args.write:
        output.write_text(json.dumps(result, indent=2) + "\n")
    elif json.loads(output.read_text()) != result:
        raise AssertionError("IMMUTABLE_RECEIPT_MISMATCH")
    print("PASS_NATIVE_SOURCE_ENDPOINT_METRIC", result["exact_controls"], "exact controls")
    print("SCOPED_OBSTRUCTION: direct current-pairing identification fails endpoint isometry")
    print("CROSS_OWNER_STATIONARY_WITNESS: diagnostic chronology minimum has spacelike retained CAR current")
    print("PHYSICAL_ADMISSION_AND_OTHER_JOINT_UPDATES_OPEN")


if __name__ == "__main__":
    main()
