#!/usr/bin/env python3
"""Independent checks for the published stored-adjoint chart jets.

The checks compare the chart with the original tied rows. They do not count
coordinates and do not classify the Euler operator.
"""
from __future__ import annotations

import sys
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import sympy as s

import stored_tangent as st


FAILURES: list[str] = []


def check(name: str, cond: bool) -> None:
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        FAILURES.append(name)


def all_zero(mapping) -> bool:
    return all(st.is_zero(value) for value in mapping.values())


def jets_vanish(builder, roles, orders) -> bool:
    for role in roles:
        for order in orders:
            if not all_zero(st.curve_constraint_jet(builder, role, order)):
                return False
    return True


def main() -> int:
    a = s.Rational(1, 4)
    b = s.Rational(1, 125)
    frame = st.homogeneous_frame(a, b)
    site = (0, 0, 0, 0)

    check("fixture_rho0_positive", frame.rho2[0] == 3 * b ** 2 and frame.rho2[0] != 0)
    check("fixture_outside_root_box", _outside_root_box(frame))
    _root_and_flat(frame)
    _whitening_and_inverse(frame)
    _named_kernel(frame)
    _jets_match_chart(frame)
    _generating_curves(a, b, frame, site)
    _conformal(a, b, frame, site)
    _lorentz_and_own_edge(frame)
    _so4(frame)
    _affine(frame)
    _c2(a, b)
    _reality_and_row_wave(frame)
    _ambient_symbol(frame)
    _result_language()

    if FAILURES:
        print("FAILED " + ", ".join(FAILURES))
        return 1
    print("ALL_PASS")
    return 0


def _outside_root_box(frame) -> bool:
    box = st.receipt_root_box()
    diagonal = Decimal(frame.car_diagonal.p) / Decimal(frame.car_diagonal.q)
    return diagonal < Decimal(box["lower_d"]) or diagonal > Decimal(box["upper_d"])


def _root_and_flat(frame) -> None:
    box = st.receipt_root_box()
    check("root_rectangle_regular", box["rectangle_in_regular_component"] is True)
    check("root_rho0_positive", box["rho0_positive_on_rectangle"] is True)
    check("root_not_physical_admission", box["physical_native_admission"] is False)
    try:
        st.homogeneous_frame(1, 0)
        check("flat_frame_rejected", False)
    except st.ChartSingular:
        check("flat_frame_rejected", True)
    jet = st.flat_formal_jet()
    check("flat_rho0_zero", jet.rho0_squared == 0)
    check("flat_zero_mode_c1", all(st.is_zero(row) for row in jet.own_leg + jet.lorentz))
    try:
        st.edge_inverse(st.E0, st.E0, jet.v[0], jet.v[0], s.eye(4))
        check("flat_inverse_rejected", False)
    except st.ChartSingular:
        check("flat_inverse_rejected", True)


def _whitening_and_inverse(frame) -> None:
    n = st.observer_vector((s.Rational(3, 4), 0, 0))
    left = st.whitening(n)
    form = st.observer_form(n)
    check("whitening_sends_observer_to_rest", st.is_zero(left * n - st.E0))
    check("whitening_square_is_h", st.is_zero(left * left - form))
    check("whitening_preserves_eta", st.is_zero(left * st.ETA * left - st.ETA))

    sx = (s.Rational(3, 4), 0, 0)
    sy = (0, s.Rational(5, 12), 0)
    zx = (s.Rational(3, 5), s.Rational(4, 5), 0)
    zy = (0, s.Rational(3, 5), s.Rational(4, 5))
    tau, rho = s.Rational(2, 5), s.Rational(3, 7)
    theta = s.atan2(s.Rational(4, 5), s.Rational(3, 5))
    value = st.edge_value(sx, sy, tau, rho, zx, zy, theta)
    check("edge_lorentz", st.is_zero(value.A.T * st.ETA * value.A - st.ETA))
    check("edge_pairing", st.is_zero(value.A.T * value.h_x * value.A - value.h_y))
    check("edge_own_leg", st.is_zero(value.A * value.v_y - value.v_x))
    check("edge_h_from_observer", st.is_zero(value.h_x - st.observer_form(value.n_x)))
    inverse = st.edge_inverse(value.n_x, value.n_y, value.v_x, value.v_y, value.A)
    check("inverse_sin", st.is_zero(inverse.sin_theta - s.Rational(4, 5)))
    check("inverse_cos", st.is_zero(inverse.cos_theta - s.Rational(3, 5)))
    check("inverse_tau_rho", inverse.tau == tau and inverse.rho == rho)
    check("inverse_observers", st.is_zero(inverse.s_x - st.column(sx)) and st.is_zero(inverse.s_y - st.column(sy)))
    check("inverse_directions", st.is_zero(inverse.z_x - st.column(zx)) and st.is_zero(inverse.z_y - st.column(zy)))
    rested = st.edge_value(sx, sy, tau, rho, zx, zy, 0)
    back = st.edge_inverse(rested.n_x, rested.n_y, rested.v_x, rested.v_y, rested.A)
    check("inverse_zero_angle", st.is_zero(back.sin_theta) and st.is_zero(back.cos_theta - 1))
    try:
        st.edge_value(sx, sy, tau, rho, (1, 1, 0), zy, 0)
        check("nonunit_direction_rejected", False)
    except st.ChartSingular:
        check("nonunit_direction_rejected", True)
    try:
        st.edge_value(sx, sy, tau, 0, zx, zy, 0)
        check("zero_rho_rejected", False)
    except st.ChartSingular:
        check("zero_rho_rejected", True)
    try:
        st.edge_value(sx, sy, tau, rho, (1, 0, 0), (-1, 0, 0), 0)
        check("antipodal_rejected", False)
    except st.ChartSingular:
        check("antipodal_rejected", True)


def _named_kernel(frame) -> None:
    phases = ((0, 0, 0, 0), (3, 3, 0, 0), (1, 2, 3, 4))
    for phase in phases:
        names = st.kernel_coordinate_names(phase)
        pure = set(st.PURE_FRAME_COORDINATES)
        check(
            f"pure_frame_proper_subset_{phase[0]}_{phase[1]}",
            pure < set(names) and "observer_nu[0]" in names and "observer_nu[0]" not in pure,
        )
        for role in range(4):
            slot = f"line_alpha[{role}]" in names and f"line_radial[{role}]" in names
            check(f"line_slot_phase_{phase[0]}_role_{role}", slot is (int(phase[role]) % 8 == 0))
        for name in names:
            tangent = st.kernel_tangent(frame, phase, {name: 1})
            residual = st.fourier_c1_action(frame, phase, tangent)
            check(f"kernel_c1_{phase[0]}_{name}", residual.nonzero_rows() == ())
            read = st.read_kernel_coordinates(frame, phase, tangent)
            others = [key for key in names if key != name]
            check(
                f"kernel_roundtrip_{phase[0]}_{name}",
                st.is_zero(read[name] - 1) and all(st.is_zero(read[key]) for key in others),
            )
    moving = {
        "observer_nu[0]": s.Rational(1, 3),
        "observer_nu[2]": s.Rational(-2, 5),
        "edge_angle[0]": s.Rational(1, 7),
        "leg_transverse[0][1]": s.Rational(2, 9),
        "leg_transverse[2][0]": s.I,
        "edge_angle[3]": 2 + s.I,
    }
    phase = (1, 2, 3, 4)
    tangent = st.kernel_tangent(frame, phase, moving)
    read = st.read_kernel_coordinates(frame, phase, tangent)
    check("combined_roundtrip", all(st.is_zero(read[key] - value) for key, value in moving.items()))
    check("observer_not_frozen", not st.is_zero(tangent.dn[1:4, :]) and not st.is_zero(tangent.dA[0]))
    check("moving_q", not st.is_zero(tangent.dq))
    pure = st.kernel_tangent(frame, phase, {"edge_angle[1]": 1})
    check("pure_frame_fixes_q_and_legs", st.is_zero(pure.dq) and all(st.is_zero(leg) for leg in pure.dv))
    check("pure_frame_moves_link", not st.is_zero(pure.dA[1]))
    transverse = st.kernel_tangent(frame, phase, {"leg_transverse[0][0]": 1})
    check("transverse_moves_q", not st.is_zero(transverse.dq) and not st.is_zero(transverse.dv[0]))
    try:
        st.kernel_tangent(frame, phase, {"line_alpha[1]": 1})
        check("line_coordinate_rejected", False)
    except st.InadmissibleCoordinate:
        check("line_coordinate_rejected", True)
    aa, bb = s.symbols("a b", positive=True)
    symbolic = st.homogeneous_frame(aa, bb)
    symbol_phase = (3, 3, 0, 0)
    symbol_tangent = st.kernel_tangent(symbolic, symbol_phase, {
        "observer_nu[0]": 1,
        "leg_transverse[1][0]": 1,
        "edge_angle[2]": 1,
        "line_alpha[2]": 1,
        "line_radial[3]": 1,
    })
    symbol_rows = st.fourier_c1_action(symbolic, symbol_phase, symbol_tangent).nonzero_rows()
    check("symbolic_positive_frame_c1", symbol_rows == () and symbolic.rho2[0] == 3 * bb ** 2)


def _jets_match_chart(frame) -> None:
    phase = (1, 0, 3, 4)
    coords = {
        "observer_nu[0]": s.Rational(1, 3),
        "observer_nu[2]": s.Rational(-2, 5),
        "edge_angle[0]": s.Rational(1, 7),
        "leg_transverse[0][1]": s.Rational(2, 9),
    }
    jet = st.fourier_first_jet(frame, 0, phase, coords)
    tangent = st.kernel_tangent(frame, phase, coords)
    omega = st.phase_factor(phase[0])
    check("first_jet_link", st.is_zero(jet["A"] - tangent.dA[0]))
    check("first_jet_source_leg", st.is_zero(jet["v_x"] - tangent.dv[0]))
    check("first_jet_target_leg", st.is_zero(jet["v_y"] - omega * tangent.dv[0]))
    check("first_jet_observers", st.is_zero(jet["n_x"] - tangent.dn) and st.is_zero(jet["n_y"] - omega * tangent.dn))
    line = {"line_alpha[1]": s.Rational(4, 11), "line_radial[1]": s.Rational(-3, 8), "edge_angle[1]": 1}
    line_jet = st.fourier_first_jet(frame, 1, (0, 0, 0, 0), line)
    line_tangent = st.kernel_tangent(frame, (0, 0, 0, 0), line)
    check(
        "first_jet_line_coordinates",
        st.is_zero(line_jet["A"] - line_tangent.dA[1])
        and st.is_zero(line_jet["v_x"] - line_tangent.dv[1])
        and st.is_zero(line_jet["v_y"] - line_tangent.dv[1]),
    )
    angle = {"edge_angle[0]": 1}
    mixed = st.fourier_mixed_second(frame, 0, ((0, 0, 0, 0), angle), ((0, 0, 0, 0), angle))
    _, _, acceleration = st.field_taylor(st.edge_angle_curve(frame.a, frame.b, 0))
    check("mixed_edge_angle_is_curve_acceleration", st.is_zero(mixed["A"] - acceleration["A"]) and not st.is_zero(mixed["A"]))
    transverse = {"leg_transverse[0][0]": 1}
    mode = (3, 3, 0, 0)
    polar = st.fourier_mixed_second(frame, 0, (mode, transverse), (mode, transverse))
    parameter = s.symbols("polar_t")
    fields = st.fourier_chart_fields(frame, 0, ((parameter, mode, transverse),))
    check(
        "transverse_polarization",
        st.is_zero(polar["A"] - s.diff(fields.A, parameter, 2).subs(parameter, 0))
        and st.is_zero(polar["v_x"] - s.diff(fields.v_x, parameter, 2).subs(parameter, 0)),
    )

    def angle_family(t):
        chart = st.fourier_chart_fields(frame, 0, ((t, mode, angle),))
        return st.SimpleNamespace(n_x=chart.n_x, n_y=chart.n_y, F_x=chart.F_x, F_y=chart.F_y, A=chart.A)

    def moving_family(t):
        chart = st.fourier_chart_fields(frame, 0, ((t, mode, {
            "observer_nu[0]": s.Rational(1, 6),
            "leg_transverse[0][0]": s.Rational(1, 5),
            "edge_angle[0]": s.Rational(1, 4),
        }),))
        return st.SimpleNamespace(n_x=chart.n_x, n_y=chart.n_y, F_x=chart.F_x, F_y=chart.F_y, A=chart.A)

    check("fourier_angle_family_through_order_two", jets_vanish(angle_family, [0], (0, 1, 2)))
    check("fourier_moving_family_orders_zero_and_one", jets_vanish(moving_family, [0], (0, 1)))


def _generating_curves(a, b, frame, site) -> None:
    check("curve_registry", st.GENERATING_CURVES == (
        "homogeneous_frame_curve",
        "row_rotation_curve",
        "observer_boost_curve",
        "edge_angle_curve",
        "endpoint_alignment_curve",
    ))
    check("homogeneous_c1", jets_vanish(st.homogeneous_frame_curve(a, b), range(4), (0, 1, 2)))
    _, velocity, _ = st.field_taylor(st.homogeneous_frame_curve(a, b))
    base_f = frame.F
    dq = velocity["F_x"] * st.ETA * base_f.T + base_f * st.ETA * velocity["F_x"].T
    check("homogeneous_moves_q", not st.is_zero(dq))

    spun = st.row_rotation_curve(a, b, site, 2, c=s.Rational(1, 3))
    check("row_rotation_c1", jets_vanish(spun, range(4), (0, 1, 2)))
    _, row_velocity, row_acceleration = st.field_taylor(spun)
    _, plain_velocity, plain_acceleration = st.field_taylor(st.row_rotation_curve(a, b, site, 2, c=0))
    generator = s.zeros(4)
    generator[2, 3], generator[3, 2] = -1, 1
    moved = st.ETA * row_velocity["F_x"].row(2).T
    check("row_rotation_first_derivative_ignores_length", st.is_zero(moved - generator * frame.v[2]))
    check("row_rotation_c_invisible_at_first_order", st.is_zero(row_velocity["F_x"] - plain_velocity["F_x"]))
    expected = (generator * generator + s.Rational(1, 3) * s.eye(4)) * frame.v[2]
    check(
        "row_rotation_second_derivative",
        st.is_zero(st.ETA * row_acceleration["F_x"].row(2).T - expected)
        and not st.is_zero(row_acceleration["F_x"] - plain_acceleration["F_x"]),
    )

    boosted = st.observer_boost_curve(a, b)
    check("observer_curve_constraints", jets_vanish(boosted, range(4), (0, 1, 2)))
    _, boost_velocity, _ = st.field_taylor(boosted)
    check(
        "observer_velocity_not_frozen",
        st.is_zero(boost_velocity["n_x"] - st.column((0, 1, 0, 0))) and not st.is_zero(boost_velocity["F_x"]),
    )
    check("edge_angle_constraints", jets_vanish(st.edge_angle_curve(a, b, 0), [0], (0, 1, 2)))
    check("alignment_constraints", jets_vanish(st.endpoint_alignment_curve(a, b), [0], (0, 1, 2)))


def _conformal(a, b, frame, site) -> None:
    factor = (2 + s.sqrt(2)) / 4
    for role in range(4):
        jet = st.curve_constraint_jet(st.conformal_edge(a, b, site, role), role, 1)
        broken = factor * frame.v[role]
        if role in (0, 1):
            check(f"conformal_broken_row_{role}", st.is_zero(jet["own_leg"] + broken))
            length = (1 + s.sqrt(2) / 2) * (frame.v[role].T * frame.v[role])[0]
            check(f"conformal_length_{role}", st.is_zero(jet["length"] - length))
            check(f"conformal_length_from_leg_{role}", st.is_zero(jet["length"] + 2 * (frame.v[role].T * jet["own_leg"])[0]))
        else:
            check(f"conformal_inert_row_{role}", st.is_zero(jet["own_leg"]) and st.is_zero(jet["length"]))
        check(f"conformal_pairing_lorentz_clear_{role}", st.is_zero(jet["pairing"]) and st.is_zero(jet["lorentz"]))
        parameter = s.symbols("conf_t")
        data = st.conformal_edge(a, b, site, role)(parameter)
        same_phase = role in (2, 3)
        check(f"conformal_endpoints_{role}", st.is_zero(data.F_x - data.F_y) is same_phase)

    tangent, residual = st.conformal_symbol(frame)
    check("conformal_symbol_rows", residual.nonzero_rows() == ("own_leg[0]", "own_leg[1]"))
    reconstructed = None
    for phase in ((3, 3, 0, 0), (5, 5, 0, 0)):
        action = st.fourier_c1_action(frame, phase, tangent)
        reconstructed = action.own_leg[0] if reconstructed is None else reconstructed + action.own_leg[0]
        check(f"conformal_symbol_pairing_{phase[0]}", st.is_zero(action.pairing[0]) and st.is_zero(action.lorentz[0]))
    curve = st.curve_constraint_jet(st.conformal_edge(a, b, site, 0), 0, 1)["own_leg"]
    check("conformal_real_pair_rebuilds_row", st.is_zero(reconstructed - curve))


def _lorentz_and_own_edge(frame) -> None:
    nu = st.column((s.Rational(1, 3), s.Rational(1, 5), 0))
    phase = (1, 2, 3, 4)
    dn = st.column((0, nu[0], nu[1], nu[2]))
    dh = st.dh_at_rest(dn)
    matched = st.kernel_tangent(frame, phase, {"observer_nu[0]": nu[0], "observer_nu[1]": nu[1]})
    check("matched_boost_c1", st.fourier_c1_action(frame, phase, matched).nonzero_rows() == ())
    matched_link = st.boost(st.kappa_of(phase, 0) * nu)
    check("matched_boost_is_kappa_link", st.is_zero(matched.dA[0] - matched_link) and not st.is_zero(matched_link))
    unmatched_link = st.boost(nu)
    unmatched = st.SimpleNamespace(
        dn=dn,
        dv=tuple(st.boost(nu) * frame.v[role] for role in range(4)),
        dA=tuple(unmatched_link for _ in range(4)),
        dh=dh,
    )
    action = st.fourier_c1_action(frame, phase, unmatched)
    lorentz_clear = all(st.is_zero(row) for row in action.lorentz)
    pairing_exact = all(
        st.is_zero(action.pairing[role] - 2 * (1 - st.kappa_of(phase, role)) * unmatched_link)
        for role in range(4)
    )
    check("unmatched_boost_lorentz_clear", lorentz_clear)
    check("unmatched_boost_pairing", pairing_exact and action.nonzero_rows() != ())

    radial = st.column((0, frame.w[1][0], frame.w[1][1], frame.w[1][2]))
    zero = st.column((0, 0, 0, 0))
    own = st.SimpleNamespace(
        dn=zero,
        dv=tuple(radial if role == 1 else zero for role in range(4)),
        dA=tuple(s.zeros(4) for _ in range(4)),
        dh=st.dh_at_rest(zero),
    )
    own_phase = (3, 3, 0, 0)
    own_action = st.fourier_c1_action(frame, own_phase, own)
    check("own_edge_only_role_1", own_action.nonzero_rows() == ("own_leg[1]",))
    mutated = st.SimpleNamespace(
        dn=zero,
        dv=tuple(frame.v[role] if role != 1 else radial for role in range(4)),
        dA=own.dA,
        dh=own.dh,
    )
    mutated_action = st.fourier_c1_action(frame, own_phase, mutated)
    check("own_edge_ignores_other_rows", st.is_zero(mutated_action.own_leg[1] - own_action.own_leg[1]))
    check("other_row_has_its_own_residual", not st.is_zero(mutated_action.own_leg[0]))


def _so4(frame) -> None:
    tangent, residual, finite = st.so4_time_space_tangent(frame, (3, 3, 0, 0))
    check("so4_lorentz_row", residual.lorentz[0][0, 1] == -2 and residual.lorentz[0][1, 0] == -2)
    check("so4_pairing_passes_skew", st.is_zero(residual.pairing[0]))
    check("so4_breaks_lorentz", "lorentz[0]" in residual.nonzero_rows())
    witness = s.zeros(4)
    witness[0, 0] = s.Rational(-32, 25)
    witness[1, 1] = s.Rational(32, 25)
    witness[0, 1] = witness[1, 0] = s.Rational(-24, 25)
    check("so4_finite_witness", st.is_zero(finite.T * st.ETA * finite - st.ETA - witness))
    try:
        st.edge_inverse(st.E0, st.E0, frame.v[0], frame.v[0], finite)
        check("so4_return_rejected", False)
    except st.ChartSingular:
        check("so4_return_rejected", True)
    del tangent


def _affine(frame) -> None:
    shift = (st.column((1, 2, 3, 4)),) * 4
    assembly = st.native_assembly(frame, affine_shifts=shift)
    check("affine_shift_not_read", st.is_zero(assembly.affine_source_row))
    check("assembly_ties_q", st.is_zero(assembly.q - frame.F * st.ETA * frame.F.T))
    mutated = frame.F.copy()
    mutated[0, :] = mutated[0, :] + s.Matrix([[1, 0, 0, 0]])
    rows = st.tied_constraints(st.E0, st.E0, frame.F, mutated, s.eye(4), 0)
    check("shift_added_into_leg_breaks_row", not st.is_zero(rows["own_leg"]))


def _c2(a, b) -> None:
    check("c2_equation_declared", st.C2_COMPATIBILITY == "DC(eta) + D2C(xi, xi) = 0")
    check("c2_not_claimed_solvable", st.C2_SOLVABILITY == "not claimed")
    check("formal_integrability_open", st.INTEGRABILITY_OUTSIDE_GENERATING_FAMILIES == "OPEN")
    base, velocity, _ = st.field_taylor(st.endpoint_alignment_curve(a, b))
    zero = {name: s.zeros(*value.shape) for name, value in velocity.items()}
    truncated = st.c2_polynomial_jet(base, velocity, zero, 0)
    expected = st.column((0, s.Rational(-2, 125), s.Rational(-2, 125), s.Rational(-2, 125)))
    check("alignment_truncation_own_leg", st.is_zero(truncated["own_leg"] - expected))
    check(
        "alignment_truncation_not_flat",
        not st.is_zero(truncated["lorentz"])
        and not st.is_zero(truncated["pairing"])
        and not st.is_zero(truncated["length"]),
    )
    _, angle_velocity, _ = st.field_taylor(st.edge_angle_curve(a, b, 0))
    combined = {name: velocity[name] + angle_velocity[name] for name in velocity}
    first = st.curve_constraint_jet(st.polynomial_edge(base, combined, zero), 0, 1)
    check("formal_sum_is_c1", all_zero(first))
    scale = s.symbols("scale")
    _, _, alignment_acceleration = st.field_taylor(st.endpoint_alignment_curve(a, b))
    accelerated = {name: scale * alignment_acceleration[name] for name in alignment_acceleration}
    second = st.c2_polynomial_jet(base, combined, accelerated, 0)
    at_zero = second["own_leg"].subs(scale, 0)
    coefficient = s.diff(second["own_leg"], scale)
    check("formal_eta0_nonzero", not st.is_zero(at_zero))
    check("formal_acceleration_coefficient_nonzero", not st.is_zero(coefficient))
    check("formal_residual_affine_in_scale", st.is_zero(second["own_leg"] - (at_zero + scale * coefficient)))


def _reality_and_row_wave(frame) -> None:
    phase = (1, 2, 3, 4)
    coords = {
        "leg_transverse[0][0]": s.I,
        "observer_nu[1]": s.Rational(1, 7) + s.I / 3,
        "edge_angle[3]": 2 + s.I,
    }
    tangent = st.kernel_tangent(frame, phase, coords)
    partner_phase, partner = st.reality_partner(frame, phase, coords)
    check("reality_phase", partner_phase == (7, 6, 5, 4))
    check(
        "reality_coordinates_conjugate",
        all(st.is_zero(partner.dv[role] - s.conjugate(tangent.dv[role])) for role in range(4))
        and all(st.is_zero(partner.dA[role] - s.conjugate(tangent.dA[role])) for role in range(4)),
    )
    check(
        "reality_preserves_line_slots",
        st.kernel_coordinate_names(phase) == st.kernel_coordinate_names(partner_phase),
    )
    generator = s.zeros(4)
    generator[2, 3], generator[3, 2] = -1, 1
    half = s.simplify(generator * frame.v[2] / 2)
    zero = st.column((0, 0, 0, 0))
    synthetic = st.SimpleNamespace(
        dn=zero,
        dv=tuple(half if role == 2 else zero for role in range(4)),
        dA=tuple(s.zeros(4) for _ in range(4)),
    )
    wave = (3, 3, 0, 0)
    coordinates = st.read_kernel_coordinates(frame, wave, synthetic)
    rebuilt = st.kernel_tangent(frame, wave, coordinates)
    check("row_wave_symbol_c1", st.fourier_c1_action(frame, wave, rebuilt).nonzero_rows() == ())
    check("row_wave_moves_q", not st.is_zero(rebuilt.dq))
    partner_wave, partner_tangent = st.reality_partner(frame, wave, coordinates)
    check("row_wave_partner_phase", partner_wave == (5, 5, 0, 0))
    check(
        "row_wave_real_partner",
        all(st.is_zero(partner_tangent.dv[role] - rebuilt.dv[role]) for role in range(4)),
    )
    character = st.phase_factor(3)
    partner_character = st.phase_factor(5)
    probe = (1, 0, 0, 0)
    phi = s.cos(s.pi * (3 * probe[0] + 3 * probe[1]) / 4)
    reconstructed = character * half + partner_character * half
    check("row_wave_cosine_pairing", st.is_zero(reconstructed - phi * generator * frame.v[2]))


def _ambient_symbol(frame) -> None:
    dn = st.column((s.Rational(1, 9), s.Rational(2, 7), 0, s.Rational(-1, 4)))
    link = s.Matrix([[0, 1, 0, 0], [2, 0, 3, 0], [0, -1, 0, 4], [5, 0, 0, 0]])
    legs = [st.column((s.Rational(role + 1, 5), role, 0, 1)) for role in range(4)]
    d_frame = s.zeros(4)
    for role, leg in enumerate(legs):
        d_frame[role, :] = (st.ETA * leg).T
    phase = (2, 5, 1, 7)
    role = 0
    omega = st.phase_factor(phase[role])

    def builder(t):
        return st.SimpleNamespace(
            n_x=st.E0 + t * dn,
            n_y=st.E0 + t * omega * dn,
            F_x=frame.F + t * d_frame,
            F_y=frame.F + t * omega * d_frame,
            A=s.eye(4) + t * link,
        )

    jet = st.curve_constraint_jet(builder, role, 1)
    tangent = st.SimpleNamespace(
        dn=dn,
        dv=tuple(legs),
        dA=tuple(link if index == role else s.zeros(4) for index in range(4)),
        dh=st.dh_at_rest(dn),
    )
    symbol = st.fourier_c1_action(frame, phase, tangent)
    check("ambient_observer_source", st.is_zero(jet["observer_unit_x"] - symbol.observer_unit))
    check("ambient_lorentz", st.is_zero(jet["lorentz"] - symbol.lorentz[role]))
    check("ambient_pairing", st.is_zero(jet["pairing"] - symbol.pairing[role]))
    check("ambient_own_leg", st.is_zero(jet["own_leg"] - symbol.own_leg[role]))
    parameter = s.symbols("ambient_t")
    rows = st.tied_constraints(
        st.E0 + parameter * dn,
        st.E0 + parameter * omega * dn,
        frame.F + parameter * d_frame,
        frame.F + parameter * omega * d_frame,
        s.eye(4) + parameter * link,
        role,
    )
    target = s.diff(rows["observer_unit_y"], parameter).subs(parameter, 0)
    check("ambient_observer_target", st.is_zero(target - omega * symbol.observer_unit))


def _result_language() -> None:
    text = (Path(__file__).resolve().parent / "RESULT_RU.md").read_text(encoding="utf-8")
    for banned in ("23-2p", "23−2p", "ОТО вывед", "ОТО замкн", "GR derived", "размерность ядра 19"):
        check(f"result_omits_{banned}", banned not in text)
    check("result_says_candidate", "candidate" in text)
    check("result_marks_open", "OPEN" in text)


if __name__ == "__main__":
    raise SystemExit(main())
