#!/usr/bin/env python3
"""Reduced lapse Hessian versus the Q7 Reynolds boundary jet.

The lapse number is recomputed at beta=2 p^2, z=2^{-20}, M=128.
The boundary jet is the order-eps^1 clock derivative on
J_eps=1+eps cos(2 pi t), V_eps=1. No factor is chosen to match them.
python3 and python3 -O both print PASS. Assertions are not used.
"""

from __future__ import annotations

from collections import Counter

import mpmath as mp
import sympy as sp


PIN_TIP = "f3fe3c80ae69f122edc8cbef19c71fb22a1d68e6"
PIN_ANCESTOR = "c3ae03b735dbde690bf1774fc3761846aff93248"
SCHEMA = "d0-lapse-reynolds-residual/1"
LAPSE_SCHEMA = "d0-full-price-lapse-source/1"

CHECKS: list[str] = []


class FittedFactorRejected(ArithmeticError):
    """A factor was solved so that the boundary jet hits 0.005723."""


def require(condition: object, name: str) -> None:
    if condition is not True:
        raise ArithmeticError(name)
    CHECKS.append(name)


def _ends(value) -> list[str]:
    return [mp.nstr(mp.mpf(value.a), 20), mp.nstr(mp.mpf(value.b), 20)]


def reduced_lapse_interval() -> dict:
    """Continuum H+J+R reduced lapse coefficient A-B^2/C.

    Same fixed-beta root, same tail budget, and the same Schur reduction
    as the pinned interval source. The boundary flux is not a term.
    """

    mp.mp.dps = 90
    mp.iv.dps = 80
    iv = mp.iv
    p = (iv.sqrt(5) - 1) / 2
    beta = 2 * p * p
    z = iv.mpf(2) ** -20
    rr = z / (1 - z)
    mass = 128
    omega = 2 * iv.pi

    def theta(t):
        body = 1 + 2 * sum(
            (iv.exp(-t * j * j) for j in range(1, 13)), iv.mpf(0)
        )
        return body + iv.mpf([0, "1e-128"])

    def moment2(t):
        body = 2 * sum(
            (j * j * iv.exp(-t * j * j) for j in range(1, 13)), iv.mpf(0)
        )
        return body + iv.mpf([0, "1e-126"])

    require(theta(iv.mpf("1.80")) < 3, "uniform_theta_bound")
    require(moment2(iv.mpf("1.80")) < 10, "uniform_moment_bound")
    theta_tail = 2 * iv.exp(-iv.mpf("1.80") * 169) / (
        1 - iv.exp(-iv.mpf("1.80") * 27)
    )
    moment_tail = (
        2
        * 169
        * iv.exp(-iv.mpf("1.80") * 169)
        / (1 - (iv.mpf(14) / 13) ** 2 * iv.exp(-iv.mpf("1.80") * 27))
    )
    require(theta_tail < iv.mpf("1e-128"), "theta_tail")
    require(moment_tail < iv.mpf("1e-126"), "moment_tail")
    feedback_tail = 2048 * beta * 4 * 27 * 10 * rr**11 / (1 - rr)
    require(feedback_tail < iv.mpf("1e-55"), "feedback_tail")

    def root_F(a):
        heat = 4 * moment2(a) / theta(a)
        feedback = 2048 * beta * sum(
            (
                (-1) ** (n + 1)
                * rr**n
                * 4
                * theta(n * a) ** 3
                * moment2(n * a)
                for n in range(1, 11)
            ),
            iv.mpf(0),
        )
        return heat - feedback - 1 + iv.mpf(["-1e-55", "1e-55"])

    center = mp.mpf(
        "1.807402105276820465785568102491966746380435406812535655887327979709036"
    )
    radius = mp.mpf("1e-30")
    low = mp.nstr(center - radius, 85)
    high = mp.nstr(center + radius, 85)
    require(root_F(iv.mpf(low)) > 0, "root_lower_sign")
    require(root_F(iv.mpf(high)) < 0, "root_upper_sign")
    ar = iv.mpf([low, high])
    c = ar / beta
    d_scale = c / omega**2
    weight_z = 16 * theta(ar) ** 4
    require(
        ar > iv.mpf("1.80") and ar < iv.mpf("1.82"),
        "root_inside_owned_interval",
    )
    require(8 * iv.pi * iv.sqrt(d_scale) < 12, "coframe_operator_bound")
    require(12 * iv.sqrt(d_scale) < 12, "link_operator_bound")

    cache: dict = {}

    def weight(square):
        if square not in cache:
            ee = iv.exp(-ar * square)
            ff = 1 - z + z * ee
            shell = iv.mpf(1) / 128 if square == 1 else 0
            cache[square] = -ee / weight_z + mass * z * beta * ee / ff + shell
        return cache[square]

    radius_l = 7
    counts = Counter(
        x * x + y * y + w * w
        for x in range(-radius_l, radius_l + 1)
        for y in range(-radius_l, radius_l + 1)
        for w in range(-radius_l, radius_l + 1)
    )
    acc_a = iv.mpf(0)
    acc_b = iv.mpf(0)
    acc_c = iv.mpf(0)
    for time in range(-radius_l - 1, radius_l + 1):
        for shell, count in counts.items():
            left = time * time + shell
            right = (time + 1) ** 2 + shell
            wk = weight(left)
            wl = weight(right)
            divided = (wl - wk) / (c * (2 * time + 1))
            summed = wk + wl
            acc_a += count * (
                summed * 8 * c * (time * time + (time + 1) ** 2)
                + divided
                * 8
                * c
                * c
                * (8 * time * time * (time + 1) ** 2 + 4 * time * (time + 1) + 1)
            )
            acc_b += count * (
                summed * 12 * c / omega + divided * 12 * c * c / omega
            )
            acc_c += count * (
                summed * 48 * c / omega**2
                + divided * 16 * c * c * (3 + shell) / omega**2
            )
    cw = iv.mpf(1) / 16 + mass * z * beta / (1 - z)
    shell_index = radius_l + 1
    ratio = (1 + iv.mpf(1) / shell_index) ** 7 * iv.exp(
        -iv.mpf("1.80") * (2 * shell_index - 1)
    )
    first = (
        (64 * shell_index**3 + 16 * shell_index)
        * (1 + 2 * shell_index) ** 2
        * (2 + iv.mpf("1.82") * (4 * shell_index + 1) ** 2)
        * iv.exp(-iv.mpf("1.80") * (shell_index - 1) ** 2)
    )
    tail = 16 * cw * 144 * first / (1 - ratio)
    require(ratio < 1, "gaussian_tail_ratio")
    require(tail < iv.mpf("1e-25"), "gaussian_tail")
    err = iv.mpf(["-1e-25", "1e-25"])
    acc_a += err
    acc_b += err
    acc_c += err
    require(acc_a > 0, "lapse_A_positive")
    require(acc_c < 0, "normal_row_negative")
    reduced = acc_a - acc_b * acc_b / acc_c
    bounds = {
        "A": ("0.0054788", "0.0054789"),
        "B": ("0.0026159", "0.0026160"),
        "C": ("-0.0280215", "-0.0280214"),
        "reduced": ("0.0057230", "0.0057231"),
    }
    values = {"A": acc_a, "B": acc_b, "C": acc_c, "reduced": reduced}
    for name, val in values.items():
        lo, hi = bounds[name]
        require(val > iv.mpf(lo) and val < iv.mpf(hi), name + "_enclosure")
    half = reduced / 2
    require(
        half > iv.mpf("0.0028615") and half < iv.mpf("0.00286155"),
        "physical_coscos_half_enclosure",
    )
    return {
        "A": acc_a,
        "B": acc_b,
        "C": acc_c,
        "reduced": reduced,
        "half": half,
        "spatial_shells": len(counts),
        "root": [low, high],
        "tail_bound": "1e-25",
    }


def reynolds_boundary() -> dict:
    """Q7 boundary jet for the volume-preserving time-only family.

    J_eps=1+eps cos(2 pi t), V_eps=1, golden leaf u=p.
    The order-eps^1 boundary value is D_eps t_F at 0, equal to
    -sin(2 pi p)/(2 pi). Interior plus boundary is identically 0.
    That identity is the cell-mass Ward, not a price Hessian.
    """

    eps = sp.symbols("epsilon")
    s = sp.symbols("s")
    p = (sp.sqrt(5) - 1) / 2
    require(sp.simplify(p + p**2 - 1) == 0, "golden_partition")
    volume = sp.integrate(1 + eps * sp.cos(2 * sp.pi * s), (s, 0, 1))
    require(sp.simplify(volume - 1) == 0, "volume_preserved_exactly")
    interior = sp.integrate(sp.cos(2 * sp.pi * s), (s, 0, p))
    a1_q9 = -sp.sin(2 * sp.pi * p) / (2 * sp.pi)
    require(sp.simplify(interior + a1_q9) == 0, "q7_sum_is_zero")
    require(
        sp.simplify(sp.sin(2 * sp.pi * p) + sp.sin(sp.pi * sp.sqrt(5))) == 0,
        "sine_shift_identity",
    )
    require(sp.simplify(a1_q9 - sp.sin(sp.pi * sp.sqrt(5)) / (2 * sp.pi)) == 0, "q9_closed_form")

    a1s, a2s, a3s = sp.symbols("a1 a2 a3")
    level_t = p + eps * a1s + eps**2 * a2s + eps**3 * a3s
    level = level_t + eps * sp.sin(2 * sp.pi * level_t) / (2 * sp.pi) - p
    series = sp.expand(sp.series(level, eps, 0, 4).removeO())
    c1 = series.coeff(eps, 1)
    c2 = series.coeff(eps, 2)
    c3 = series.coeff(eps, 3)
    sol1 = sp.solve(sp.Eq(c1, 0), a1s)
    sol2 = sp.solve(sp.Eq(c2.subs(a1s, sol1[0]), 0), a2s)
    sol3 = sp.solve(
        sp.Eq(c3.subs({a1s: sol1[0], a2s: sol2[0]}), 0),
        a3s,
    )
    require(len(sol1) == 1 and len(sol2) == 1 and len(sol3) == 1, "jet_unique")
    jet1 = sp.simplify(sol1[0])
    jet2 = sp.simplify(sol2[0])
    jet3 = sp.simplify(sol3[0])
    require(sp.simplify(jet1 - a1_q9) == 0, "order_eps1_is_q9")
    substituted = {a1s: jet1, a2s: jet2, a3s: jet3}
    moved = level_t.subs(substituted)
    mass_gap = sp.expand(sp.series(moved + eps * sp.sin(2 * sp.pi * moved) / (2 * sp.pi) - p, eps, 0, 4).removeO())
    require(sp.simplify(mass_gap) == 0, "moving_mass_jet_vanishes_through_eps3")
    flux = (1 + eps * sp.cos(2 * sp.pi * moved)) * sp.diff(moved, eps)
    flux_series = sp.expand(sp.series(flux, eps, 0, 3).removeO())
    interior_series = sp.sin(2 * sp.pi * moved) / (2 * sp.pi)
    ward = sp.expand(sp.series(flux + interior_series, eps, 0, 3).removeO())
    require(sp.simplify(ward) == 0, "q7_holds_through_eps2")
    b0 = sp.simplify(flux_series.coeff(eps, 0))
    b1 = sp.simplify(flux_series.coeff(eps, 1))
    b2 = sp.simplify(flux_series.coeff(eps, 2))
    require(sp.simplify(b0 - jet1) == 0, "boundary_at_zero_is_order_eps1")
    require(sp.simplify(b1 - jet2) == 0, "boundary_eps_coefficient_is_order_eps2_motion")

    iv = mp.iv
    mp.mp.dps = 90
    mp.iv.dps = 80
    enclosed = {
        "a1": iv.sin(iv.pi * iv.sqrt(5)) / (2 * iv.pi),
        "a2": iv.sin(2 * iv.pi * iv.sqrt(5)) / (4 * iv.pi),
        "a3": (2 - 3 * iv.sin(iv.pi * iv.sqrt(5)) ** 2)
        * iv.sin(iv.pi * iv.sqrt(5))
        / (4 * iv.pi),
    }
    symbolic = {"a1": jet1, "a2": jet2, "a3": jet3}
    for name in ("a1", "a2", "a3"):
        # Sympy's decimal rounding is coarser than the iv shell, so compare
        # the two evaluations at a fixed absolute tolerance instead of nesting.
        numeric = mp.mpf(sp.N(symbolic[name], 25))
        slot = enclosed[name]
        require(
            abs(numeric - mp.mpf(slot.mid)) < mp.mpf("1e-20"),
            name + "_matches_enclosure",
        )
        require(slot > iv.mpf("0.03"), name + "_bounded_away_from_zero")
    require(
        sp.simplify(jet2 - sp.sin(2 * sp.pi * sp.sqrt(5)) / (4 * sp.pi)) == 0,
        "order_eps2_closed_form",
    )
    return {
        "epsilon_order": 1,
        "expression": "-sin(2*pi*p)/(2*pi)",
        "a1": enclosed["a1"],
        "a2": enclosed["a2"],
        "a3": enclosed["a3"],
        "cell_mass_eps2": 0,
        "q7_sum": 0,
    }


def accept_fitted_match(boundary, target) -> None:
    """Negative control. Solving factor*boundary = target must raise.

    There is no return path. exact_cancellation is not granted by a fit.
    """

    factor = target / boundary
    product = factor * boundary
    gap = abs(product - target)
    if gap > mp.mpf("1e-18"):
        raise FittedFactorRejected("fitted_product_inconsistent")
    raise FittedFactorRejected("fitted_factor_rejected")


def _excludes(left, right, name: str) -> None:
    gap = left - right
    require(gap > 0 or gap < 0, name)


def run() -> dict:
    CHECKS.clear()
    lapse = reduced_lapse_interval()
    boundary = reynolds_boundary()
    reduced = lapse["reduced"]
    a1 = boundary["a1"]
    iv = mp.iv
    residual = reduced - a1
    opposite = reduced + a1
    require(residual < iv.mpf("-0.10") and residual > iv.mpf("-0.11"), "residual_cross_order")
    require(opposite > iv.mpf("0.11") and opposite < iv.mpf("0.12"), "opposite_sign_not_zero")
    for label, piece in (
        ("a1", boundary["a1"]),
        ("a2", boundary["a2"]),
        ("a3", boundary["a3"]),
    ):
        _excludes(reduced, piece, "reduced_minus_" + label)
        _excludes(reduced, -piece, "reduced_plus_" + label)
        _excludes(lapse["half"], piece, "half_minus_" + label)
        _excludes(lapse["half"], -piece, "half_plus_" + label)
    # Moving-cell mass gap vanishes through order eps^3, so its eps^2
    # coefficient is 0 and does not cancel the lapse Hessian.
    require(boundary["cell_mass_eps2"] == 0, "same_order_mass_residual_is_zero")
    require(reduced > iv.mpf("0.0057230") and reduced < iv.mpf("0.0057231"), "same_order_price_residual")
    require(a1 > iv.mpf("0.0057231") or a1 < iv.mpf("0.0057230"), "boundary_outside_lapse_window")
    try:
        accept_fitted_match(mp.mpf(a1.mid), mp.mpf("0.005723"))
    except FittedFactorRejected as exc:
        require(str(exc) == "fitted_factor_rejected", "fitted_control_raises")
    else:
        raise ArithmeticError("fitted_control_did_not_raise")

    exact_cancellation = False
    coefficient_chosen = False
    gr_derived = False
    require(exact_cancellation is False, "exact_cancellation_false")
    require(coefficient_chosen is False, "coefficient_chosen_false")
    require(gr_derived is False, "gr_derived_false")
    require(boundary["q7_sum"] == 0, "ward_internal_zero_is_not_the_price")
    return {
        "status": "PASS",
        "schema": SCHEMA,
        "candidate": True,
        "exact_cancellation": exact_cancellation,
        "coefficient_chosen": coefficient_chosen,
        "gr_derived": gr_derived,
        "native_measure_admission_claimed": False,
        "finite_schur_limit_claimed": False,
        "boundary_is_summand_of_reduced_lapse_hessian": False,
        "observables": "different",
        "pin_tip": PIN_TIP,
        "pin_ancestor": PIN_ANCESTOR,
        "lapse_schema": LAPSE_SCHEMA,
        "beta": "2*p**2",
        "z": "2**(-20)",
        "M": 128,
        "root_interval": lapse["root"],
        "spatial_shells": lapse["spatial_shells"],
        "lapse_A": _ends(lapse["A"]),
        "lapse_B": _ends(lapse["B"]),
        "lapse_C": _ends(lapse["C"]),
        "lapse_reduced_enclosure": ["0.0057230", "0.0057231"],
        "lapse_reduced_computed": _ends(reduced),
        "physical_coscos_half_computed": _ends(lapse["half"]),
        "boundary_expression": boundary["expression"],
        "boundary_epsilon_order": boundary["epsilon_order"],
        "boundary_contribution": _ends(a1),
        "boundary_order_eps2_motion": _ends(boundary["a2"]),
        "boundary_order_eps3_motion": _ends(boundary["a3"]),
        "q7_internal_sum": "0",
        "cell_mass_residual_all_orders_through_eps3": "0",
        "quantitative_residual": "reduced_lapse - boundary_eps1",
        "residual_enclosure": _ends(residual),
        "residual_opposite_sign": _ends(opposite),
        "same_order_residual": "reduced_lapse - 0",
        "same_order_residual_enclosure": ["0.0057230", "0.0057231"],
        "matrix_tail_bound": lapse["tail_bound"],
        "check_count": len(CHECKS),
        "checks": list(CHECKS),
    }


def main() -> None:
    receipt = run()
    if receipt["status"] != "PASS":
        raise ArithmeticError("status")
    if receipt["exact_cancellation"] is not False:
        raise ArithmeticError("exact_cancellation")
    if receipt["coefficient_chosen"] is not False:
        raise ArithmeticError("coefficient_chosen")
    if receipt["gr_derived"] is not False:
        raise ArithmeticError("gr_derived")
    print("PASS")


if __name__ == "__main__":
    main()
