#!/usr/bin/env python3
"""Checks for the raw-l1 precision budget.

No assert statement: python -O must keep every scientific check.
A PASS is a sufficient bound. It is not a native refining solution.
"""

from __future__ import annotations

import json
from fractions import Fraction

import precision_budget as pb


CHECKS = []


def require(condition, label):
    if not bool(condition):
        raise AssertionError(label)
    CHECKS.append(label)


def fraction(text):
    return Fraction(text)


def base_spec(**overrides):
    spec = pb.v8_spec_from_enclosure(
        Fraction(1, 8),
        {**pb._rate(1, 8), "stage": "reconstructed_source"},
        {**pb._rate(1, 8), "stage": "reconstructed_source"},
        {**pb._rate(1, 8), "stage": "euler_residual"},
    )
    spec.update(overrides)
    return spec


def expect_map(spec, map_name):
    try:
        result = pb.evaluate_v8(spec)
    except pb.BudgetRefusal as refusal:
        result = refusal.payload()
    text = json.dumps(result)
    require(result["verdict"] == "REFUSE", "%s verdict" % map_name)
    require(result["map"] == map_name, "%s map, got %s" % (map_name, result.get("map")))
    require('"verdict": "PASS"' not in text, "%s printed a pass" % map_name)
    return result


def pieces_sum(result):
    total = Fraction(0)
    for value in result["pieces"].values():
        total += Fraction(value)
    return total


def check_boundary_identity():
    for h in (Fraction(1, 8), Fraction(1, 16), Fraction(1, 32)):
        require(pb.historical_boundary_value(h) == 6, "six-slot witness is 6 at h=%s" % h)
        require(
            pb.raw_l1_from_pointwise(h, 10, h ** 6) == 10,
            "ten packed rows of h^6 sum to 10",
        )
        volume = pb.volume_normalized_reading(h, 6, h ** 6)
        require(volume == 6 * h ** 4, "volume reading is a different power")
        require(volume != 6, "volume reading is not the raw witness")
    expect_map(base_spec(norm="volume"), "volume_norm_is_not_raw_l1")


def check_positive_v8():
    first = pb.published_v8_budget()
    second = pb.published_v8_budget_second()
    require(first["verdict"] == "PASS", "first v8 budget")
    require(second["verdict"] == "PASS", "second v8 budget")
    require(first["vanishing"] is True and second["vanishing"] is True, "both budgets vanish")
    require(first["native_refining_solutions_proved"] is False, "not a refining existence proof")
    require(first["gr_derived"] is False and second["gr_derived"] is False, "no relativity claim")
    require(first["programs_added"] is False, "v8 budget did not absorb another price")
    require(first["field_shell_hessian_inverted"] is False, "Hessian was not inverted")
    require(pieces_sum(first) == Fraction(first["bound"]), "first pieces sum to the bound")
    require(pieces_sum(second) == Fraction(second["bound"]), "second pieces sum to the bound")
    require(Fraction(first["pieces"]["gap"]) == Fraction(1, 64), "gap share at h=1/8")
    require(Fraction(first["pieces"]["operator"]) == Fraction(5, 32), "operator share at h=1/8")
    require(Fraction(first["pieces"]["quadrature"]) == Fraction(5, 32), "quadrature share at h=1/8")
    require(Fraction(first["pieces"]["observer"]) == Fraction(15, 64), "observer share at h=1/8")
    require(first["chosen"]["k"] == 0, "return depth at h=1/8")
    require(second["h"] == "1/16", "second mesh")
    require(second["assumed_rates"]["operator"]["exponent"] == 7, "second operator exponent")
    require(first["assumed_rates"]["operator"]["exponent"] == 8, "first operator exponent")
    require(Fraction(second["bound"]) < Fraction(first["bound"]), "finer mesh has the smaller sufficient bound")
    require(first["scales"]["M"] == 128, "feedback multiplicity stays 128")
    require(first["scales"]["hs_dimension"] == 16, "fibre dimension stays 16")
    require(Fraction(first["scales"]["D_hs"]) == 4 * Fraction(first["scales"]["D_op"]), "HS factor sqrt(16)")
    require(Fraction(first["scales"]["Delta_1"]) == 16 * Fraction(first["scales"]["D_op"]), "trace factor 16")
    require(Fraction(first["scales"]["sqrt_dimension"]) == 4, "square root was not dropped")
    names = [item["name"] for item in first["terms"]]
    require(
        names[:6]
        == [
            "auxiliary_gap",
            "return_tail",
            "operator_approximation",
            "coframe_observer",
            "spatial_quadrature",
            "source_after_right_inverse",
        ],
        "six compatible terms",
    )
    for item in first["terms"]:
        require(item["domain"] and item["norm"] and item["add_predicate"], "term %s is incomplete" % item["name"])
        require(item["added"] is True, "term %s was not admitted" % item["name"])


def check_tolerances_are_exact():
    spec = base_spec()
    result = pb.evaluate_v8(spec)
    h = Fraction(spec["h"])
    beta = Fraction(spec["beta"])
    b0 = Fraction(spec["b0"])
    allowance_target = h ** 2
    scalar = allowance_target * h ** 6 / (Fraction(spec["C_W"]) * 10)
    half = scalar / 2
    eps_h = pb.choose_eps_h(half, beta, b0, spec["D_op"])
    eps_j = pb.choose_eps_j(half, spec["q"], spec["M"], spec["z"], beta, 4)
    channel_h, channel_j = pb.gap_channels(eps_h, eps_j, beta, b0, spec["D_op"], spec["q"], spec["M"], spec["z"], 4)
    require(channel_h == half and channel_j == half, "auxiliary channels meet their allowances")
    require(result["chosen"]["eps_H"] == pb.show(eps_h), "published eps_H")
    require(result["chosen"]["eps_J"] == pb.show(eps_j), "published eps_J")
    scales = pb.schatten_scales(1, 16, 0, False)
    depth = pb.choose_return_depth(scalar, 128, beta, spec["z"], scales["Delta_1"])
    require(depth == 0, "minimal return depth")
    require(
        pb.tail_scalar(depth, 128, beta, spec["z"], scales["Delta_1"])
        == Fraction(result["pieces"]["tail"]) * h ** 6 / (Fraction(spec["C_W"]) * 10),
        "tail piece matches (15)",
    )
    require(
        pb.tail_scalar(0, 256, beta, spec["z"], scales["Delta_1"])
        == 2 * pb.tail_scalar(0, 128, beta, spec["z"], scales["Delta_1"]),
        "tail is linear in M",
    )


def check_enclosure():
    enc = pb.v8_calibration_enclosure()
    lower = enc["sqrt5_lower"]
    require(lower * lower <= 5, "sqrt(5) lower bound")
    require(enc["sqrt5_upper"] * enc["sqrt5_upper"] > 5, "sqrt(5) upper bound")
    require(enc["beta_upper"] == 3 - lower, "beta majorant")
    require(enc["b0_lower"] == lower - 2, "b0 minorant")
    require(enc["b0_lower"] > 0 and enc["beta_upper"] > 0, "enclosure signs")
    require(enc["z"] == Fraction(1, 2**20) and enc["M"] == 128, "fixed z and M")
    require(enc["length_ell"] == Fraction(1, 8) and enc["length_ell_is_field"] is False, "length ell is not a field")
    ell = pb.af_ell_bounds()
    require(ell["lower"] > Fraction(1, 8), "AF log(phi) is above the v8 length")
    require(ell["upper"] < Fraction(1, 2), "AF log(phi) upper bound")
    require(pb.p_pow(1) * pb.p_pow(-1) == pb.Golden(1, 0) or (pb.p_pow(1) * pb.p_pow(-1)).a == 1, "p inverse")
    unit = pb.p_pow(1) * pb.p_pow(-1)
    require(unit.a == 1 and unit.b == 0, "golden inverse is exact")


def check_refusals():
    expect_map(
        base_spec(
            operator_rate={**pb._rate(1, 6), "stage": "reconstructed_source"},
            quadrature_rate={**pb._rate(0, 8), "stage": "reconstructed_source"},
            observer_rate={**pb._rate(0, 8), "stage": "euler_residual"},
        ),
        "pointwise_h6_after_raw_sum",
    )
    expect_map(
        base_spec(operator_rate={**pb._rate(1, 5), "stage": "reconstructed_source"}),
        "pointwise_coarser_than_h6_raw_sum",
    )
    grown = base_spec()
    grown["operator_rate"] = {**pb._rate(1, 8), "stage": "reconstructed_source", "uses_growing_dimension": True}
    grown["dimension_exponent"] = -4
    expect_map(grown, "pointwise_h6_after_raw_sum")
    expect_map(base_spec(beta_depends_on_h=True), "fixed_beta_bound_versus_beta_of_h")
    expect_map(base_spec(alpha_depends_on_h=True), "fixed_alpha_unfolding_versus_alpha_of_h")
    expect_map(base_spec(t_depends_on_h=True), "fixed_z_tail_versus_t_of_h")
    expect_map(base_spec(rescue="beta(h)"), "beta_of_h_rescue")
    expect_map(base_spec(rescue="alpha(h)"), "alpha_of_h_rescue")
    expect_map(base_spec(rescue="t(h)"), "t_of_h_rescue")
    expect_map(base_spec(declared_multiplicity=16), "multiplicity_mismatch")
    expect_map(base_spec(feedback_multiplicity=16), "multiplicity_mismatch")
    expect_map(base_spec(right_inverse_supplied=False), "missing_right_inverse")
    expect_map(base_spec(inverse_kind="left"), "left_inverse_is_not_right_inverse")
    expect_map(base_spec(constant_source="28/s", neumann_ball=False, price_s=Fraction(1, 8)), "twenty_eight_over_s_without_neumann_ball")
    expect_map(base_spec(return_group="SO(4)"), "n05_so4_return_rejected")
    expect_map(base_spec(chart_regular=False), "n05_chart_singular")
    expect_map(base_spec(source_fitted_to_solution=True), "fitted_source_rejected")
    expect_map(base_spec(weight_law="endogenous_moving"), "n08_endogenous_weight_conditional")
    expect_map(base_spec(drop_dimension_factor=True), "hs_bound_independent_of_dimension")
    expect_map(base_spec(q=Fraction(1, 2)), "auxiliary_gap_domain")
    expect_map(base_spec(z=1), "auxiliary_gap_domain")
    expect_map(base_spec(b0=0), "auxiliary_gap_domain")
    expect_map(base_spec(invert_lower_block=True), "lower_block_is_not_inverted")
    expect_map(base_spec(compose_with_other_price=True), "v8_plus_central_price")
    expect_map(base_spec(slots=6), "slot_count_is_not_parent_packed_rows")
    expect_map(base_spec(h=Fraction(2, 3)), "mesh_step_not_reciprocal_integer")
    expect_map(
        base_spec(include_gq=True, use_gq_as_hessian_inverse=True, gap_exceeds_certified=True),
        "gq_is_not_field_shell_hessian_inverse",
    )
    expect_map(
        base_spec(include_gq=True, use_gq_as_spatial_refinement=True, gap_exceeds_certified=True),
        "gq_does_not_give_spatial_refinement",
    )
    expect_map(
        base_spec(
            include_gq=True,
            gap_exceeds_certified=True,
            delta_op_norm=Fraction(1, 8),
            epsilon_shift=0,
            gq_to_slot=1,
        ),
        "gq_outside_declared_window",
    )
    moving = expect_map(base_spec(weight_law="endogenous_moving"), "n08_endogenous_weight_conditional")
    require(pb.N08_TASK in moving["detail"] and pb.N08_PATH in moving["detail"], "N08 path is named")


def check_right_inverse_constant_and_replay():
    constant = pb.right_inverse_constant(
        {"right_inverse_supplied": True, "inverse_kind": "right", "constant_source": "28/s", "neumann_ball": True, "price_s": Fraction(1, 8)}
    )
    require(constant == Fraction(28) / Fraction(1, 8), "28/s inside the Neumann ball")
    beta = pb.v8_calibration_enclosure()["beta_upper"]
    certificate = {"M": 128, "k": 0, "tail_scalar": pb.tail_scalar(0, 128, beta, Fraction(1, 2**20), 16), "beta": beta}
    replay = pb.replay_certificate(
        certificate,
        {"M": 128, "beta": beta, "z": Fraction(1, 2**20), "Delta_1": 16},
    )
    require(replay["verdict"] == "PASS", "frozen certificate replays at the same M")
    try:
        pb.replay_certificate(
            certificate,
            {"M": 64, "beta": beta, "z": Fraction(1, 2**20), "Delta_1": 16},
        )
        require(False, "changed multiplicity must not replay")
    except pb.BudgetRefusal as refusal:
        require(refusal.map_name == "multiplicity_mismatch", "replay names multiplicity")
    try:
        pb.replay_certificate(
            certificate,
            {"M": 128, "beta": beta / 2, "beta_depends_on_h": True, "z": Fraction(1, 2**20), "Delta_1": 16},
        )
        require(False, "beta(h) replay must not pass")
    except pb.BudgetRefusal as refusal:
        require(refusal.map_name == "fixed_beta_bound_versus_beta_of_h", "replay names beta(h)")


def check_gq_window():
    record, tail = pb._owned_gq(0, 0, True, 1, Fraction(1, 3))
    require(record["window_open"] is True, "open window")
    require(record["gq_strict_upper"] == 4, "constant 4 only inside the window")
    require(record["field_inverse_estimated"] is False, "constant 4 is not a Hessian inverse")
    require(tail["exact_tail"] < tail["uniform_tail"], "Neumann tail is strict")
    require(tail["uniform_tail"] == Fraction(4, 2 ** 2), "uniform tail keeps the factor 4 * 2^{-(k+1)}")
    outside, _empty = pb._owned_gq(Fraction(1, 8), 0, True, 1, Fraction(1, 3))
    require(outside["gq_strict_upper"] is None and outside["window_open"] is False, "boundary is outside")
    missing, _empty = pb._owned_gq(0, 0, False, 1, Fraction(1, 3))
    require(missing["gq_strict_upper"] is None and missing["rq_norm_upper"] is None, "no gap, no constant")


def check_central_is_separate():
    central = pb.published_central_budget()
    require(central["verdict"] == "PASS", "central budget")
    require(central["program"] == pb.CENTRAL_PROGRAM, "central program id")
    require(central["transferred_to_raw_l1"] is False, "central budget stays off the raw target")
    require(central["native_refining_solutions_proved"] is False, "central budget is not existence")
    require(Fraction(central["bound"]["compiler_dual"]) == Fraction(1, 4), "assumed lambda compiler")
    require(Fraction(central["bound"]["reading"]) <= Fraction(1, 1000), "reading meets the tolerance")
    require(central["chosen"]["k"] == (16 * central["chosen"]["c"]) // 17, "central depth rule")
    require(Fraction(central["bound"]["lambda_route_alternative"]) != Fraction(central["bound"]["compiler_dual"]), "lambda route is not the assumed lambda")
    v8 = pb.published_v8_budget()
    try:
        pb.compose_programs(v8, central)
        require(False, "composition must refuse")
    except pb.BudgetRefusal as refusal:
        text = json.dumps(refusal.payload())
        require(refusal.map_name == "v8_plus_central_price", "composition map")
        require('"verdict": "PASS"' not in text, "composition printed a pass")
    expect_central = (
        ("ell", "1/8", "v8_length_ell_is_not_af_log_phi"),
        ("transfer_to_raw_l1", True, "central_to_raw_without_lead_link"),
        ("apply_to_v8", True, "central_rate_on_v8_without_same_program"),
    )
    for key, value, map_name in expect_central:
        spec = {
            "lambda": Fraction(1, 10),
            "residual_dual": Fraction(1, 100),
            "tolerance": Fraction(1, 1000),
            "lead_link_proved": False,
        }
        spec[key] = value
        try:
            pb.evaluate_central(spec)
            require(False, map_name)
        except pb.BudgetRefusal as refusal:
            require(refusal.map_name == map_name, map_name)
    deeper, _bound = pb.choose_central_depth(1, 1, Fraction(1, 1000), *pb.sqrt5_bounds())
    shallower, _looser = pb.choose_central_depth(1, 1, Fraction(1, 10), *pb.sqrt5_bounds())
    require(deeper > shallower, "a tighter tolerance chooses a larger central depth")


def check_native_gates():
    chart = pb.native_chart_gate()
    require(chart["rho0_squared"] == "3/15625", "N05 rational frame")
    require(chart["flat_frame_rejected"] is True, "N05 flat frame")
    require(chart["return_group"] == "SO(3)" and chart["so4_return_admitted"] is False, "N05 return")
    require(chart["physical_native_admission"] is False, "chart is not admission")
    calibration = pb.native_calibration_gate()
    require(calibration["beta"] == "3-sqrt(5)", "N07 beta")
    require(calibration["b0"] == "sqrt(5)-2", "N07 b0")
    require(calibration["M"] == 128 and calibration["z"] == "1/1048576", "N07 z and M")
    require(calibration["af_preparation_added"] is False, "AF second variation stays out of v8")
    require(calibration["lower_block_inverted"] is False, "N07 does not invert the shell block")
    require(calibration["pairing"] == pb.PAIRING, "N07 pairing")
    pins = pb.provenance()
    require(pins["sha256"]["n05"] == pb.file_sha256(pb.REPO / pb.N05_PATH), "N05 hash")
    require(pins["sha256"]["n06"] == pb.file_sha256(pb.REPO / pb.N06_PATH), "N06 hash")
    require(pins["sha256"]["n07"] == pb.file_sha256(pb.REPO / pb.N07_PATH), "N07 hash")
    require(pins["n08_conditional"]["merged"] is False, "N08 is not merged into this budget")
    require(pins["historical_source"] == pb.HISTORICAL_SOURCE, "historical pin")


def main():
    check_boundary_identity()
    check_positive_v8()
    check_tolerances_are_exact()
    check_enclosure()
    check_refusals()
    check_right_inverse_constant_and_replay()
    check_gq_window()
    check_central_is_separate()
    check_native_gates()
    print(json.dumps({"status": "PASS", "checks": len(CHECKS)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
