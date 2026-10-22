#!/usr/bin/env python3
"""No-go: at the exact h=1/4 configured Golden N1 42-field CQ critical root,
ANY C2 scalar function of the equal (or near-equal FIXED weighted) mean
report has either a nonzero first source or a rank-at-most-one Hessian and
a 41-dimensional critical fiber.

Consumes original strictly outward interval reports and the original
nonsingular 42x42 full-price Hessian, with their frozen Git blobs.
Not a no-go for full Book03 HJR with independent spectral/clock/Info sources.
"""
from __future__ import annotations
import argparse
from decimal import Decimal, localcontext
from fractions import Fraction
import hashlib
import json
from pathlib import Path

SOURCES = {
    "02_REGISTRY/research/sources/d0_exact_full42_h4_2026-10-22/"
    "RIGOROUS_EXACT42_CERTIFICATE.json":
        "9f4bdef4c367660539c588db01819330ff0d55b3",
    "02_REGISTRY/research/sources/d0_exact_full42_h4_2026-10-22/"
    "REPORT_BRIDGE_RESULT.json":
        "2c7193f54da76aaf108d2821c45daddac7457f02",
}


def load_frozen(repo: Path, path: str, required_sha: str) -> dict:
    raw = (repo / path).read_bytes()
    actual = hashlib.sha1(
        b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw
    ).hexdigest()
    if actual != required_sha:
        raise AssertionError(("owner Git blob changed", path, actual, required_sha))
    return json.loads(raw)


def check_outer_product_rank() -> dict:
    # This algebraic test is an exact rational 42-dimensional representative
    # of H_B=Phi''(m*) (dm tensor dm), NOT a numeric CQ Hessian replay.
    # General proof: for any i,j,k,l,
    # (v_i v_j)(v_k v_l) -(v_i v_l)(v_k v_j) =0.
    v = [Fraction(i * i - 2 * i + 3, 7) for i in range(42)]
    coeff = Fraction(-19, 13)
    for i in range(42):
        for j in range(42):
            a = coeff * v[i] * v[j]
            b = coeff * v[j] * v[i]
            assert a == b
    for i in (0, 3, 11, 27):
        for j in (1, 13, 28, 41):
            for k in (0, 21):
                for l in (6, 39):
                    assert (coeff * v[i] * v[j]) * (coeff * v[k] * v[l]) == (
                        coeff * v[i] * v[l]) * (coeff * v[k] * v[j]
                    )
    assert coeff * v[0] * v[0] != 0
    # v0 != 0: the 41 linearly independent explicit kernel vectors
    # v0*e_j - vj*e0 are all killed by the actual outer-product matrix.
    for j in range(1, 42):
        t = [Fraction(0)] * 42
        t[0] = -v[j]
        t[j] = v[0]
        assert sum(v[k] * t[k] for k in range(42)) == 0
    return {
        "generic_outer_product_rank": "<=1, equality if Phi'' and dm nonzero",
        "exact_rational_42dimensional_witness_rank": 1,
        "independent_kernel_vectors": 41,
        "critical_fiber_dimension_if_dm_nonzero": 41,
    }


def run(repo: Path) -> dict:
    with localcontext() as ctx:
        ctx.prec = 75
        cert = load_frozen(repo, *next(iter(SOURCES.items())))
        report = load_frozen(repo, *list(SOURCES.items())[1])
        assert cert["status"] == "RIGOROUS_BANACH_NEWTON_EXACT_FULL42_ROOT_ON_RATIONAL_COLLAR"
        assert report["status"] == "PASS_INTERVAL_OFF_NULL_REPORT_BRIDGE_OBSTRUCTION"
        assert cert["dimension"] == 42 and cert["time_intervals"] == 2
        assert cert["root_cube_radius"] == "1E-30"
        assert cert["scope"]["all42_mathematically_stationary"] is True
        assert cert["scope"]["compulsory_Book03_selected"] is False

        # Rigorous Neumann-Hessian input, consumed: not a new 1764-entry proof.
        original_AJ = Decimal(cert["qcenter_including_error"])
        actual_movement = Decimal(cert["qchange_via_cauchy_bound"])
        invertible_certificate = original_AJ + actual_movement
        assert invertible_certificate < Decimal("0.001")

        d0 = Decimal(report["report0_D_abs_lower_at_root"])
        s_minus_one = Decimal(report["hprime_ratio_minus_one_lower"])
        mean_from_owners = Decimal(report["mean_report_D_abs_lower_at_root"])
        report_gap = Decimal(report["report_interval_gap_lower"])
        assert d0 > Decimal("2.2637805e-8")
        assert s_minus_one > Decimal("2.37636e-6")
        assert report_gap > Decimal("5.80688e-11")
        assert mean_from_owners > Decimal("2.6897805e-14")

        # CQ criticality supplies Dr1=-(h'_0/h'_1)Dr0 EXACTLY.
        # Since h'_0/h'_1>1+margin, the actual equal mean is a
        # SUBMERSION. The receipt supplies independent strict bounds.
        mean_derived = d0 * s_minus_one / 2
        assert mean_derived > Decimal("2.6897805e-14")
        assert abs(mean_from_owners - mean_derived) < Decimal("1e-25")

        # Robust fixed positive weighted means. With t=w0/w1,
        # |t-1|<=eps and w0+w1=1, w1=1/(1+t)>=1/(2+eps).
        eps = Decimal("0.000001")
        near_equal_bound = (
            d0 * (s_minus_one - eps) / (Decimal(2) + eps)
        )
        assert near_equal_bound > Decimal("1.55788e-14")
        exact_rank_test = check_outer_product_rank()
        return {
            "status": "PASS_EXACT_SINGLE_MEAN_41D_CRITICAL_FIBER_NO_GO",
            "input": {
                "original_h": "1/4",
                "original_full_field_dimension": cert["dimension"],
                "physical_price": "configured N1 CQ; compulsory Book03 OPEN",
                "owner_blobs": SOURCES,
            },
            "certified_inputs": {
                "nonsingular_full42_Hessian_Neumann_Q_upper":
                    str(invertible_certificate),
                "CQ_Hessian_rank": 42,
                "r0_r1_report_gap_lower": str(report_gap),
                "original_D29_r0_abs_lower": str(d0),
                "entropy_slope_ratio_minus_one_lower": str(s_minus_one),
            },
            "derived": {
                "D29_equal_mean_abs_lower": str(mean_derived),
                "certified_independent_D29_equal_mean_abs_lower":
                    str(mean_from_owners),
                "near_equal_fixed_weight_ratio_window": "abs(w0/w1-1)<=1e-6",
                "D29_weighted_mean_abs_lower_on_window":
                    str(near_equal_bound),
                "cases": {
                    "Phi_prime_nonzero": "NONSTATIONARY at exact CQ root",
                    "Phi_prime_zero": (
                        "stationary but 41-dimensional level-set critical "
                        "manifold; Hessian rank <= 1"
                    ),
                },
                "exact_rational_rank_control": exact_rank_test,
            },
            "scope": {
                "applies_to": "C + Phi(fixed equal/near-equal LINEAR mean of two reports)",
                "nonlinear_full_two_report_thermal_action_ruled_out": False,
                "field_dependent_weight_or_cut_ruled_out": False,
                "additional_preparation_clock_heat_source_ruled_out": False,
                "physically_compulsory_Book03_selected": False,
                "GR_closed": False,
            },
        }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[4])
    parser.add_argument("--json", type=Path, default=None)
    args = parser.parse_args()
    result = run(args.repo.resolve())
    output = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    print(output, end="")
    if args.json:
        args.json.write_text(output, encoding="utf-8")


if __name__ == "__main__":
    main()
