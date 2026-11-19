#!/usr/bin/env python3
"""D0 original h=1/4 exact full42 CQ root: two authentic complete report
moments reconstruct the ENTIRE two-cell Bernoulli entropy score, while a
specified ordinary iid classical report-discrimination task requires
>2.59e14 fully retained N1 ternary-status launches for Bayes error <=1/4.

Strict consumed evidence: pinned original h4 42-source certificate and
independent report interval bridge. No fresh 42x42 interval replay.
This is NOT Book03 physical heat/cut/Info/writer selection and NOT an
information lower bound against coherent/collective quantum experiments.
"""
from __future__ import annotations
import argparse
from decimal import Decimal, localcontext
from fractions import Fraction
import hashlib
import json
from pathlib import Path

PINS = {
 "02_REGISTRY/research/sources/d0_exact_full42_h4_2026-10-22/"
 "RIGOROUS_EXACT42_CERTIFICATE.json":
 "9f4bdef4c367660539c588db01819330ff0d55b3",
 "02_REGISTRY/research/sources/d0_exact_full42_h4_2026-10-22/"
 "REPORT_BRIDGE_RESULT.json":
 "2c7193f54da76aaf108d2821c45daddac7457f02",
}

# Literal OUTWARD intervals recorded in the original independent proof;
# the new bounds below never rely on unpinned numeric root approximations.
R0_MIN = "1.8512417713660524e-6"
R0_MAX = "1.85124371058701973e-6"
R1_MIN = "1.85130177947843566e-6"
R1_MAX = "1.85132974719277498e-6"


def read_pin(repo: Path, path: str, blob: str) -> dict:
    binary = (repo / path).read_bytes()
    got = hashlib.sha1(
        b"blob " + str(len(binary)).encode("ascii") + b"\0" + binary
    ).hexdigest()
    if got != blob:
        raise AssertionError(("changed historical source", path, got, blob))
    return json.loads(binary.decode("utf-8"))


def exact_polynomial_transport() -> dict:
    # Mathematical equality for every pair of original Bernoulli rates.
    pairs = [
        (Fraction(1, 13), Fraction(1, 7)),
        (Fraction(1, 250), Fraction(1, 200)),
        (Fraction(1, 1000000), Fraction(2, 1000000)),
        (Fraction(3, 10), Fraction(3, 10)),
    ]
    for r0, r1 in pairs:
        m = (r0 + r1) / 2
        coincidence = r0 * r1
        assert m * m - coincidence == ((r1 - r0) / 2) ** 2
        assert (r0 + r1) == 2 * m and r0 * r1 == coincidence
        # Elementary symmetric polynomial: r0,r1 are roots of
        # x^2 -2m*x + coincidence, not newly chosen observables.
        for r in (r0, r1):
            assert r * r - 2 * m * r + coincidence == 0
        jac = (r0 - r1) / 2
        assert (jac == 0) == (r0 == r1)
    return {
        "invertible_two_moment_map": "m=(r0+r1)/2, c=r0*r1",
        "determinant": "(r0-r1)/2",
        "inverse_on_ordered_positive_chart":
            "r0=m-sqrt(m*m-c), r1=m+sqrt(m*m-c)",
        "symmetric_entropy_identity":
            "h_phi(r0)+h_phi(r1)=h_phi(m-sqrt(m*m-c))"
            "+h_phi(m+sqrt(m*m-c))",
        "exact_rational_pair_controls": len(pairs),
    }


def check_report_and_cost(repo: Path) -> dict:
    cert, report = [
        read_pin(repo, path, gitblob) for path, gitblob in PINS.items()
    ]
    assert cert["status"] == (
        "RIGOROUS_BANACH_NEWTON_EXACT_FULL42_ROOT_ON_RATIONAL_COLLAR"
    )
    assert report["status"] == "PASS_INTERVAL_OFF_NULL_REPORT_BRIDGE_OBSTRUCTION"
    assert cert["dimension"] == 42
    assert cert["time_intervals"] == 2
    assert cert["root_cube_radius"] == "1E-30"
    assert cert["scope"]["all42_mathematically_stationary"] is True
    assert cert["scope"]["compulsory_Book03_selected"] is False
    assert report["scope"]["exact_root_used_from_interval_certificate"] is True

    with localcontext() as ctx:
        ctx.prec = 80
        r0a, r0b, r1a, r1b = map(
            Decimal, (R0_MIN, R0_MAX, R1_MIN, R1_MAX)
        )
        delta_cert_min = Decimal(report["report_interval_gap_lower"])
        gap_upper = r1b - r0a
        gap_box_min = r1a - r0b
        assert r0a > 0 and r0b < r1a and r1b < Decimal(1)
        assert delta_cert_min > Decimal("5.806889141593e-11") - Decimal("1e-25")
        assert gap_box_min >= delta_cert_min
        assert gap_upper < Decimal("8.797582672249e-11")
        det_lower = delta_cert_min / 2
        assert det_lower > Decimal("2.90344e-11")
        inverse_sensitivity_lower = Decimal(1) / gap_upper
        assert inverse_sensitivity_lower > Decimal("1.136e10")

        # The same ORIGINAL cap9/20 N1 readiness. The conservative upper
        # 0.46 suffices for the source distinction bound. Evaluate rather
        # than replacing the true factory law by a Bernoulli shortcut.
        p = (Decimal(5).sqrt() - Decimal(1)) / 2
        alpha = (1 - (1 - 2 * p ** 3) ** 9) ** 128
        beta_factory = (
            (1 - p ** 120) ** 4 *
            (1 - (1 - 16 * p ** 9) ** 20)
        ) ** 43
        gamma = alpha * beta_factory
        assert Decimal("0.45") < gamma < Decimal("0.46")
        gamupper = Decimal("0.46")

        # The classic inequality KL(P||Q) <= chi2(P||Q) follows from
        # log x<=x-1, with complete 3-status laws
        # (1-gamma, gamma(1-r), gamma r).
        # For same gamma, chi2=gamma*(r1-r0)^2/[r1*(1-r1)].
        chi_square_upper = (
            gamupper * gap_upper ** 2 / (r1a * (1 - r1b))
        )
        assert chi_square_upper < Decimal("1.9232e-15")
        lower_launches = Decimal(1) / (2 * chi_square_upper)
        assert lower_launches > Decimal("2.59e14")

        # Classical equal-prior Bayes error <=1/4 forces TV>=1/2.
        # Pinsker says TV<=sqrt(n KL /2).
        # Therefore n>=1/(2 KL)>1/(2 chi2_upper).
        # This is an iid classical ternary REPORT testing task, not a
        # quantum-work/Book03/full-primitive-cost lower bound.

        # Mean-report source was already certified nonzero by an
        # independent interval report jet (not recalculated here).
        certified_mean_source = Decimal(
            report["mean_report_D_abs_lower_at_root"]
        )
        assert certified_mean_source > Decimal("2.68978e-14")
        H_neumann = (
            Decimal(cert["qcenter_including_error"])
            + Decimal(cert["qchange_via_cauchy_bound"])
        )
        assert H_neumann < Decimal("0.001")

        # Reconstruct the *joint* positive paid event from original two
        # independent complete N1 launches: expected unconditioned click
        # product is gamma² * r0*r1. The event is positive but rare.
        coincidence_lower = gamma ** 2 * r0a * r1a
        coincidence_upper = gamma ** 2 * r0b * r1b
        assert coincidence_lower > 0
        assert coincidence_upper < Decimal("1e-12")

        return {
            "original_interval_collar": "h=1/4; two sites; PF=(1,1)",
            "certified_CQ_Hessian_rank": 42,
            "certified_Hessian_Neumann_bound": str(H_neumann),
            "original_report_0_interval": [R0_MIN, R0_MAX],
            "original_report_1_interval": [R1_MIN, R1_MAX],
            "strict_original_report_gap_lower": str(delta_cert_min),
            "report_gap_upper": str(gap_upper),
            "jacobian_det_abs_strict_lower": str(det_lower),
            "inverse_from_collision_sensitivity_lower":
                str(inverse_sensitivity_lower),
            "original_gamma_from_literal_caps": str(gamma),
            "complete_classical_ternary_chi2_upper":
                str(chi_square_upper),
            "KL_upper_by_log_leq_linear": str(chi_square_upper),
            "minimum_full_independent_classical_ternary_launches_for_"
            "Bayes_error_leq_one_quarter_strict_lower": str(lower_launches),
            "certified_mean_report_D29_lower": str(certified_mean_source),
            "unconditioned_two_launch_READY1_coincidence_probability_interval":
                [str(coincidence_lower), str(coincidence_upper)],
        }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo", type=Path, default=Path(__file__).resolve().parents[4]
    )
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()
    result = {
        "status": "PASS_TWO_NATIVE_REPORT_MOMENTS_AND_CLASSICAL_COST_WALL",
        "historical_inputs": PINS,
        "exact_symmetric_algebra": exact_polynomial_transport(),
        "certified_interval_consumers": check_report_and_cost(
            args.repo.resolve()
        ),
        "scope": {
            "same_original_two_N1_conditional_reports": True,
            "joint_event_requires_two_independently_paid_original_launches": True,
            "complete_fail_ready0_ready1_law_retained": True,
            "two_moments_sufficient_for_entire_report_CQ_entropy": True,
            "two_moments_prove_full_quantum_work_Book03_Info": False,
            "classical_lower_bound_applies_to_iid_ternary_status_testing":
                True,
            "coherent_quantum_discrimination_lower_bound": False,
            "complete_native_gate_cost_per_launch_computed": False,
            "new_42_Hessian_interval_replayed": False,
            "physically_compulsory_Book03_selected": False,
            "GR_closed": False,
        },
    }
    data = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    print(data, end="")
    if args.json:
        args.json.write_text(data, encoding="utf-8")


if __name__ == "__main__":
    main()
