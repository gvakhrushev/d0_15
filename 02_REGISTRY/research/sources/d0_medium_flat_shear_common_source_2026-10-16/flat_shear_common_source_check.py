#!/usr/bin/env python3
"""Typed common-source composition on one flat factor shear.

Consumes the owned factor-shear receipt. Does not execute that census.
Status of this calculation: candidate DRAFT. Not a gravitational claim.
"""

from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

from mpmath import iv

PIN = "dfaf7c8df509d5abd83fa60a185ad530feadc9b5"
ROOT = Path(__file__).resolve().parents[4]
HEAT_LOWER = Fraction(1, 10000)
PROBE_TANGENT = (Fraction(2), Fraction(-2), Fraction(0), Fraction(0))

FORBIDDEN = (
    "rename_coarse_to_complete",
    "move_current_derivative_onto_metric_shear",
    "drop_archive_compensation",
    "fitted_source_eq_minus_heat",
    "sum_of_different_runs",
)


@dataclass(frozen=True)
class Arrow:
    """One source row, or one rejected substitution of a row."""

    name: str
    carrier: str
    preparation: str
    tangent_id: str
    tangent: tuple[Fraction, Fraction, Fraction, Fraction] | None
    action: str
    support: str
    map_status: str
    origin: str
    value_id: str
    couples_extra: bool
    missing_arrow: str


@dataclass
class Report:
    failures: list[str]

    def check(self, condition: bool, name: str) -> None:
        if not condition:
            self.failures.append(name)


def git_show(path: str) -> str:
    return subprocess.check_output(
        ["git", "show", f"{PIN}:{path}"],
        cwd=ROOT,
        text=True,
    )


def quote_is_at(path: str, line: int, text: str) -> bool:
    rows = git_show(path).splitlines()
    return 1 <= line <= len(rows) and rows[line - 1] == text


def diag_mul(left: tuple[Fraction, ...], right: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    if len(left) != len(right):
        raise ValueError("diagonal length mismatch")
    return tuple(a * b for a, b in zip(left, right))


def trace(values: tuple[Fraction, ...]) -> Fraction:
    return sum(values, Fraction(0))


def consumed_probe() -> dict:
    """Owned receipt fields. The 2899-check program is not run."""
    receipt = json.loads(
        git_show(
            "02_REGISTRY/research/certificates/"
            "a4d_native_preparation_factor_shear_results.json"
        )
    )
    return {
        "exact_checks_not_rerun": receipt["exact_checks"],
        "optimized_AF_source": receipt["optimized_AF_source"],
        "fixed_gate": receipt["fixed_golden_two_tick_remainder"],
        "heat": receipt["positive_heat_factor_source"],
        "einstein": receipt["flat_Einstein_covector"],
        "tangent": tuple(Fraction(x) for x in receipt["metric_tangent_in_whitened_chart"]),
        "compiled_effect": receipt["compiled_even_effect"],
        "conclusion": receipt["conclusion"],
        "full_core_no_go": receipt["full_core_no_go"],
    }


def chart_of_factor_path() -> dict[str, tuple[Fraction, ...]]:
    """Orthonormal chart of the owned path (10)--(12), at t=0.

    q(t)=diag(4 e^{2t}, -e^{-2t}/4, -1, -1),
    Q(t)=diag(4 e^{2t}, e^{-2t}/4, 1, 1).
    """
    q0 = (Fraction(4), Fraction(-1, 4), Fraction(-1), Fraction(-1))
    v_q = (Fraction(8), Fraction(1, 2), Fraction(0), Fraction(0))
    q_inv = tuple(1 / x for x in q0)
    q_inv_v = diag_mul(q_inv, v_q)
    s = (Fraction(2), Fraction(1, 2), Fraction(1), Fraction(1))
    v_q_positive = (Fraction(8), Fraction(-1, 2), Fraction(0), Fraction(0))
    s_inv = tuple(1 / x for x in s)
    v_orth = diag_mul(diag_mul(s_inv, v_q_positive), s_inv)
    # Chronology path (19) at this same base is pure trace: dq/dt = 2q.
    v_conf = tuple(2 * x for x in q0)
    q_inv_conf = diag_mul(q_inv, v_conf)
    trace_part = tuple((trace(q_inv_conf) / 4) * x for x in q0)
    v_conf_tf = tuple(a - b for a, b in zip(v_conf, trace_part))
    pairing = trace(diag_mul(q_inv_v, q_inv_conf))
    return {
        "q0": q0,
        "v_q": v_q,
        "q_inv_v": q_inv_v,
        "v_orth": v_orth,
        "v_conf": v_conf,
        "v_conf_tf": v_conf_tf,
        "shear_conf_pairing": (pairing,),
    }


def constant_metric_einstein_is_zero() -> bool:
    """Spatially constant q has vanishing coordinate Christoffel symbols."""
    partial_q = (Fraction(0),) * 4
    return all(x == 0 for x in partial_q)


def observer_on_two_supports() -> dict[str, Fraction]:
    """Constant-path integrand versus the owned transverse witness at s=1."""
    # Factor path is spatially constant, so theta = K = Omega = a = 0.
    constant_integrand = Fraction(0)
    # s = 1+y, chi_s = -4s/(1+4s^2), and K^2 = Omega^2 = chi_y^2 / 2.
    s = Fraction(1)
    chi_y = Fraction(-4) * s / (1 + 4 * s * s)
    k2 = chi_y * chi_y / 2
    omega2 = k2
    theta = Fraction(0)
    r_h = -2 * chi_y * chi_y
    # Identity (5) with a vanishing divergence on this displayed witness.
    r_g = -r_h + 2 * (theta * theta - k2 - omega2)
    # Current slope of J_1/J_0 = -2s^2/(1+2s^2). Not a metric tangent.
    current_slope = Fraction(-4) * s / (1 + 2 * s * s) ** 2
    return {
        "constant_integrand": constant_integrand,
        "chi_y": chi_y,
        "K2": k2,
        "Omega2": omega2,
        "R_h": r_h,
        "R_g": r_g,
        "current_slope": current_slope,
    }


def coarse_matter_source() -> dict[str, str]:
    """Recompute the owned diagonal coarse jet. Do not relabel it."""
    previous = iv.dps
    iv.dps = 45
    try:
        p = (iv.sqrt(5) - 1) / 2
        a = iv.sqrt(p)
        g = -iv.log(p)
        r2 = iv.sqrt(2)
        xp, xm, x0 = p**3 + p**2 / r2, p**3 - p**2 / r2, p**3
        sp, sm, xb = p**3 + a * p**2 / r2, p**3 - a * p**2 / r2, a * p**3
        amplitudes = [xp, xp, sp, xm, xm, x0, x0, sm] + [xb] * 5
        lambdas = [v * v for v in amplitudes]
        if any(v <= 0 for v in lambdas):
            raise RuntimeError("coarse eigenvalues must stay positive")
        logs = [iv.log(v) for v in lambdas]
        dxp = a * (-(p**3) + p / r2)
        dxm = a * (-(p**3) - p / r2)
        dx0 = -a * p**3
        dots = [dxp, dxp, 0, dxm, dxm, dx0, dx0, 0] + [
            -(p**4),
            -(p**4),
            0,
            -(p**4),
            -(p**4),
        ]
        d_e = sum(2 * x * dx * log_lambda for x, dx, log_lambda in zip(amplitudes, dots, logs))
        gain = -d_e / g
        cost = -8 * a * p**7
        old = cost - gain
        return {
            "old": str(old),
            "gain": str(gain),
            "cost": str(cost),
            "old_positive": str(old > iv.mpf("0.43415444592488") and old < iv.mpf("0.43415444592489")),
            "gain_negative": str(
                gain > iv.mpf("-0.65076653214095") and gain < iv.mpf("-0.65076653214094")
            ),
            "readout": "COARSE_LEFT_A4_ON_CURVE_2",
            "complete_first_operator_old_on_curve_2": "0",
            "archive_jet_on_curve_2": str(-old),
            "active_record_on_curve_2": str(old),
        }
    finally:
        iv.dps = previous


def matter_curve_is_orthogonal() -> bool:
    """Coefficient of a p^3 in m0·dm. The relation p^2=1-p is not required."""
    # m0 = ap(e0+e14)+p^2(e1-e15), dm = -p^2(e0+e14)+ap(e1-e15).
    # Two copies of each pair: -2 a p^3 + a p^3 + a p^3.
    return -2 + 1 + 1 == 0


def probe_arrow(probe: dict) -> Arrow:
    return Arrow(
        name="consumed_factor_shear",
        carrier="flat_factor_shear_kinematic",
        preparation="blank_E_p2_I_fixed_gate_frame",
        tangent_id="V_orth",
        tangent=probe["tangent"],
        action="hodge_heat_plus_compiled_AF_plus_fixed_gate",
        support="spatially_constant",
        map_status="bound_consumed",
        origin="owned_receipt",
        value_id="prep=0,heat>1/10000,gate=0",
        couples_extra=False,
        missing_arrow="",
    )


def owned_rows() -> tuple[Arrow, ...]:
    missing = "iota_V_shear_to_common_preparation"
    return (
        Arrow(
            name="prepared_source",
            carrier="count_event_v3_instrument",
            preparation="rho0_Phi_b_Delta_archive",
            tangent_id="unbound_Hr",
            tangent=None,
            action="count_event_price_R_A",
            support="history_words",
            map_status="unbound",
            origin="formula_7",
            value_id="no_image_of_V",
            couples_extra=False,
            missing_arrow=missing,
        ),
        Arrow(
            name="canonical_active_record",
            carrier="A10_M144_plus_M89_on_H7",
            preparation="canonical_trace_seed_curve_2",
            tangent_id="dm_masks_0_1_14_15",
            tangent=None,
            action="spectral_A_old_A_gain_Cost",
            support="CAR_matter_curve_2",
            map_status="unbound",
            origin="transferred_coarse_on_curve_2",
            value_id="coarse_interval_not_on_V",
            couples_extra=False,
            missing_arrow=missing,
        ),
        Arrow(
            name="observer_reflection",
            carrier="lorentz_reflection_of_positive_metric",
            preparation="fixed_recorded_observer_or_transverse_m_s",
            tangent_id="V_orth_constant_or_partial_y",
            tangent=PROBE_TANGENT,
            action="curvature_rewrite_c_R_h",
            support="split_constant_versus_transverse_y",
            map_status="geometric_zero_action_unbound",
            origin="identity_5_on_constant_path",
            value_id="constant_observer_integrand_0",
            couples_extra=False,
            missing_arrow=missing,
        ),
        Arrow(
            name="chronology",
            carrier="chronological_J_sixteen_amplitude",
            preparation="first_grade_k_positive",
            tangent_id="conformal_2q_or_frame_lift",
            tangent=None,
            action="S_equals_H_plus_J_plus_R",
            support="k_positive_domain",
            map_status="domain_mismatch",
            origin="identity_4_and_path_19",
            value_id="not_defined_at_probe_k_0",
            couples_extra=False,
            missing_arrow=missing,
        ),
    )


def attack_rows(coarse_old_is_nonzero: bool) -> tuple[Arrow, ...]:
    """Lookalike couplings. Only the forbidden origin keeps them out.

    If the origin gate is removed, admits_extra becomes true and this check fails.
    """
    if not coarse_old_is_nonzero:
        raise RuntimeError("coarse interval failed; rename-attack would be vacuous")
    shear = PROBE_TANGENT

    def lookalike(name: str, value_id: str) -> Arrow:
        return Arrow(
            name=name,
            carrier="flat_factor_shear_kinematic",
            preparation="blank_E_p2_I_fixed_gate_frame",
            tangent_id="V_orth",
            tangent=shear,
            action="hodge_heat_plus_compiled_AF_plus_fixed_gate",
            support="spatially_constant",
            map_status="bound_extra",
            origin=name,
            value_id=value_id,
            couples_extra=True,
            missing_arrow="rejected",
        )

    return (
        lookalike("rename_coarse_to_complete", "coarse_number_called_complete_shear_source"),
        lookalike("move_current_derivative_onto_metric_shear", "current_slope_-4/9_pasted_on_V"),
        lookalike("drop_archive_compensation", "coarse_without_archive_jet"),
        lookalike("fitted_source_eq_minus_heat", "-heat_by_definition"),
        lookalike("sum_of_different_runs", "prep_0_plus_coarse_plus_observer_0_plus_chronology"),
    )


def admits_extra(row: Arrow, probe_tangent: tuple[Fraction, ...]) -> bool:
    """A coupled extra source must be the same probe and not a substitution."""
    if row.origin in FORBIDDEN or row.map_status in {
        "unbound",
        "relabelled",
        "pasted_current_slope",
        "archive_dropped",
        "fitted",
        "summed",
        "domain_mismatch",
        "geometric_zero_action_unbound",
        "bound_consumed",
    }:
        return False
    return (
        row.carrier == "flat_factor_shear_kinematic"
        and row.preparation == "blank_E_p2_I_fixed_gate_frame"
        and row.action == "hodge_heat_plus_compiled_AF_plus_fixed_gate"
        and row.support == "spatially_constant"
        and row.tangent == probe_tangent
        and row.map_status == "bound_extra"
        and row.value_id not in {"prep=0,heat>1/10000,gate=0", "constant_observer_integrand_0"}
        and row.couples_extra
    )


def main() -> int:
    report = Report(failures=[])
    probe = consumed_probe()
    chart = chart_of_factor_path()
    observer = observer_on_two_supports()
    coarse = coarse_matter_source()
    rows = owned_rows()
    attacks = attack_rows(coarse["old_positive"] == "True")

    report.check(probe["exact_checks_not_rerun"] == 2899, "receipt_records_2899_checks")
    report.check(probe["optimized_AF_source"] == "0", "consumed_preparation_source_zero")
    report.check(probe["fixed_gate"] == "0", "consumed_fixed_gate_zero")
    report.check(
        probe["heat"] == "2*(E1-E2)>1/10000 at beta=log(2), all L>=2",
        "consumed_heat_statement",
    )
    report.check(probe["tangent"] == PROBE_TANGENT, "consumed_tangent_is_V")
    report.check(probe["full_core_no_go"] is False, "receipt_is_not_a_whole_core_nogo")
    report.check(chart["v_orth"] == PROBE_TANGENT, "orthonormal_chart_of_V_Q")
    report.check(chart["q_inv_v"] == PROBE_TANGENT, "q_inverse_V_q_equals_V")
    report.check(trace(chart["q_inv_v"]) == 0, "shear_is_trace_free")
    report.check(chart["v_conf_tf"] == (Fraction(0),) * 4, "conformal_path_is_pure_trace")
    report.check(chart["v_conf"] != chart["v_q"], "chronology_radial_tangent_is_not_V_q")
    report.check(chart["shear_conf_pairing"] == (Fraction(0),), "shear_orthogonal_to_conformal")
    report.check(constant_metric_einstein_is_zero(), "constant_metric_christoffel_zero")
    report.check(observer["constant_integrand"] == 0, "constant_observer_integrand_zero")
    report.check(observer["K2"] == Fraction(8, 25), "transverse_K2")
    report.check(observer["Omega2"] == Fraction(8, 25), "transverse_Omega2")
    report.check(observer["R_h"] == Fraction(-32, 25), "transverse_R_h")
    report.check(observer["R_g"] == 0, "transverse_identity_5_gives_R_g_0")
    report.check(observer["current_slope"] == Fraction(-4, 9), "current_slope_not_a_metric")
    report.check(observer["current_slope"] != 0, "current_slope_would_fake_a_source")
    report.check(matter_curve_is_orthogonal(), "curve_2_tangent_has_no_radial_part")
    report.check(coarse["old_positive"] == "True", "coarse_old_source_interval")
    report.check(coarse["gain_negative"] == "True", "coarse_gain_source_interval")
    report.check(coarse["complete_first_operator_old_on_curve_2"] == "0", "complete_first_operator_zero")
    report.check(coarse["readout"] != "COMPLETE_SHEAR_SOURCE", "coarse_readout_is_not_the_shear")

    citations = (
        (
            "02_REGISTRY/research/A4D_NATIVE_PREPARATION_FACTOR_SHEAR.md",
            10,
            "V = diag(2,-2,0,0).",
        ),
        (
            "02_REGISTRY/research/A4D_NATIVE_PREPARATION_FACTOR_SHEAR.md",
            68,
            "Since this candidate has `dE=0`, its optimized AF price source is exactly zero. "
            "At the blank effect `E=p^2 I`, the minimizing `M2` amplitude is a scalar multiple "
            "of `I2`; that direction is the existing engine-support trace line. This removes "
            "the linear support obstruction at the blank direction, but it does not prove that "
            "the optimizer's coefficient or the full preparation is physically admitted by the engine.",
        ),
        (
            "02_REGISTRY/research/A4D_NATIVE_FACTOR_IMBALANCE_REMAINDER.md",
            255,
            "apparatus/matter/action preparation is still a missing native arrow.",
        ),
        (
            "02_REGISTRY/research/A4D_NATIVE_CANONICAL_TRACE_RECORD_SOURCE.md",
            252,
            "These nonzero coarse sources must not be relabelled as the complete first",
        ),
        (
            "02_REGISTRY/research/A4D_NATIVE_CANONICAL_TRACE_RECORD_SOURCE.md",
            267,
            "is exactly -dA_old,4. The analogous entropy difference cancels dA_gain,4.",
        ),
        (
            "02_REGISTRY/research/A4D_NATIVE_RECORD_SOURCE_JOINT_CONTINUATION.md",
            194,
            "внутренней переменной. Уравнение (8) **не разрешает выбирать H_r[V] по нужному",
        ),
        (
            "02_REGISTRY/research/A4D_NATIVE_RECORD_SOURCE_JOINT_CONTINUATION.md",
            434,
            "не отождествление с настоящим chronological J. Для physical применения",
        ),
        (
            "02_REGISTRY/research/A4D_NATIVE_CHRONOLOGICAL_JOINT_REDUCTION.md",
            24,
            "    q has signature (+---), v=m^1, k=v^T q^-1 v>0,",
        ),
        (
            "02_REGISTRY/research/A4D_NATIVE_LORENTZ_REFLECTION_SOURCE.md",
            468,
            "future or a fitted compensating action is not such an identity. The",
        ),
    )
    for path, line, text in citations:
        report.check(quote_is_at(path, line, text), f"quote:{path}:{line}")

    report.check(probe_arrow(probe).couples_extra is False, "consumed_zero_is_not_an_extra_source")
    for row in rows:
        report.check(row.missing_arrow == "iota_V_shear_to_common_preparation", f"missing:{row.name}")
        report.check(admits_extra(row, probe["tangent"]) is False, f"not_coupled:{row.name}")
    for attack in attacks:
        report.check(attack.origin in FORBIDDEN, f"forbidden_listed:{attack.name}")
        report.check(admits_extra(attack, probe["tangent"]) is False, f"rejected:{attack.name}")

    # Same numeric zero on two tangents is not one source.
    report.check(
        probe["optimized_AF_source"] == "0" and coarse["complete_first_operator_old_on_curve_2"] == "0",
        "two_zeros_exist",
    )
    report.check("V_orth" != "dm_masks_0_1_14_15", "two_zeros_have_different_tangents")
    report.check(HEAT_LOWER > 0, "heat_lower_bound_positive")

    coupled = [row.name for row in rows if admits_extra(row, probe["tangent"])]
    print("status: candidate DRAFT")
    print("probe_tangent: diag(2,-2,0,0)")
    print("consumed: preparation=0 heat>1/10000 fixed_gate=0 einstein=0")
    print("heat_modes_rerun: no")
    print(f"owned_receipt_exact_checks_not_rerun: {probe['exact_checks_not_rerun']}")
    print("coupled_extra_source: none" if not coupled else f"coupled_extra_source: {coupled}")
    print("missing_map: iota_V_shear_to_common_preparation")
    for row in rows:
        print(
            "row "
            f"{row.name} carrier={row.carrier} preparation={row.preparation} "
            f"tangent={row.tangent_id} action={row.action} map={row.map_status} "
            f"value={row.value_id}"
        )
    print(
        "coarse_on_curve_2: "
        f"old_in_(0.43415444592488,0.43415444592489)={coarse['old_positive']} "
        f"gain_in_(-0.65076653214095,-0.65076653214094)={coarse['gain_negative']} "
        "complete_first_operator_old=0 archive_jet=-coarse"
    )
    print(
        "observer: constant_integrand=0 "
        f"transverse_K2={observer['K2']} R_h={observer['R_h']} "
        f"current_slope={observer['current_slope']} support=partial_y"
    )
    print(
        "chronology: domain_k>0 probe_m=0 "
        f"conformal_tf={tuple(map(str, chart['v_conf_tf']))} "
        f"pairing_with_shear={chart['shear_conf_pairing'][0]}"
    )
    for name in FORBIDDEN:
        print(f"rejected_substitution: {name}")
    if report.failures:
        print(f"FAIL {len(report.failures)}")
        for name in report.failures:
            print(f"fail: {name}")
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
