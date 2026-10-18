"""Replay the lapse/Reynolds comparison and reject a fitted match.

python3 and python3 -O must both print PASS. Assertions are not used.
"""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

import mpmath as mp

sys.path.insert(0, str(Path(__file__).resolve().parent))

from check_lapse_reynolds_residual import (  # noqa: E402
    PIN_ANCESTOR,
    PIN_TIP,
    FittedFactorRejected,
    accept_fitted_match,
    run,
)


def main() -> None:
    receipt = run()
    if receipt["status"] != "PASS":
        raise ArithmeticError("status")
    if receipt["candidate"] is not True:
        raise ArithmeticError("candidate")
    if receipt["exact_cancellation"] is not False:
        raise ArithmeticError("exact_cancellation")
    if receipt["coefficient_chosen"] is not False:
        raise ArithmeticError("coefficient_chosen")
    if receipt["gr_derived"] is not False:
        raise ArithmeticError("gr_derived")
    if receipt["native_measure_admission_claimed"] is not False:
        raise ArithmeticError("native_measure_admission")
    if receipt["finite_schur_limit_claimed"] is not False:
        raise ArithmeticError("finite_schur")
    if receipt["boundary_is_summand_of_reduced_lapse_hessian"] is not False:
        raise ArithmeticError("summand")
    if receipt["observables"] != "different":
        raise ArithmeticError("observables")
    if receipt["boundary_epsilon_order"] != 1:
        raise ArithmeticError("epsilon_order")
    if receipt["q7_internal_sum"] != "0":
        raise ArithmeticError("q7")
    if receipt["cell_mass_residual_all_orders_through_eps3"] != "0":
        raise ArithmeticError("mass_residual")
    if receipt["quantitative_residual"] != "reduced_lapse - boundary_eps1":
        raise ArithmeticError("residual_name")
    if receipt["pin_tip"] != PIN_TIP or receipt["pin_ancestor"] != PIN_ANCESTOR:
        raise ArithmeticError("pin")
    if receipt["beta"] != "2*p**2" or receipt["z"] != "2**(-20)" or receipt["M"] != 128:
        raise ArithmeticError("root_parameters")
    if receipt["check_count"] < 59:
        raise ArithmeticError("check_count")
    if "fitted_factor" in receipt or "lambda" in receipt:
        raise ArithmeticError("factor_was_stored")

    shells = len(
        Counter(
            x * x + y * y + w * w
            for x in range(-7, 8)
            for y in range(-7, 8)
            for w in range(-7, 8)
        )
    )
    if receipt["spatial_shells"] != shells:
        raise ArithmeticError("spatial_shells")

    mp.mp.dps = 40
    p = (mp.sqrt(5) - 1) / 2
    if abs((p + p**2) - 1) > mp.mpf("1e-30"):
        raise ArithmeticError("golden")
    boundary = -mp.sin(2 * mp.pi * p) / (2 * mp.pi)
    interior = mp.sin(2 * mp.pi * p) / (2 * mp.pi)
    if abs(interior + boundary) > mp.mpf("1e-30"):
        raise ArithmeticError("independent_q7")
    reported = mp.mpf(receipt["boundary_contribution"][0])
    if abs(reported - boundary) > mp.mpf("1e-18"):
        raise ArithmeticError("boundary_digits")
    reduced = mp.mpf(receipt["lapse_reduced_computed"][0])
    if not (mp.mpf("0.0057230") < reduced < mp.mpf("0.0057231")):
        raise ArithmeticError("lapse_window")
    residual = mp.mpf(receipt["residual_enclosure"][0])
    if abs(residual - (reduced - reported)) > mp.mpf("1e-18"):
        raise ArithmeticError("residual_digits")
    if not (mp.mpf("-0.11") < residual < mp.mpf("-0.10")):
        raise ArithmeticError("residual_window")
    opposite = mp.mpf(receipt["residual_opposite_sign"][0])
    if abs(opposite - (reduced + reported)) > mp.mpf("1e-18"):
        raise ArithmeticError("opposite_digits")
    if abs(opposite) < mp.mpf("0.1"):
        raise ArithmeticError("opposite_too_small")
    order2 = mp.mpf(receipt["boundary_order_eps2_motion"][0])
    if abs(order2 - reduced) < mp.mpf("1e-3"):
        raise ArithmeticError("order2_matches_lapse")
    if abs(boundary - mp.mpf("0.005723")) < mp.mpf("1e-3"):
        raise ArithmeticError("boundary_already_matches_target")

    solved = mp.mpf("0.005723") / reported
    if abs(solved - 1) < mp.mpf("1e-3") or abs(solved + 1) < mp.mpf("1e-3"):
        raise ArithmeticError("unit_factor")
    caught = False
    try:
        accept_fitted_match(reported, mp.mpf("0.005723"))
    except FittedFactorRejected as exc:
        if str(exc) != "fitted_factor_rejected":
            raise
        caught = True
    if not caught:
        raise ArithmeticError("fitted_control_did_not_raise")
    print("PASS")


if __name__ == "__main__":
    main()
