"""Hostile checks for the LEFT residual comparison.  Not assert-based: python -O must still reject a false conclusion."""

from __future__ import annotations

import sys
from pathlib import Path

import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_left_residual_executed_source as chk


def fail(name: str) -> None:
    raise chk.CheckFailure(name)


def expect_fraud(name: str, **kwargs) -> None:
    try:
        chk.compare(**kwargs)
    except chk.LeftResidualFraud:
        return
    fail(name)


def main() -> None:
    verdict = chk.compare()
    if verdict["identity_holds"] is not False:
        fail("identity flag")
    if verdict["scoped_nogo"] is not True:
        fail("nogo flag")
    if verdict["gr_derived"] is not False:
        fail("gr flag")
    if verdict["identity_holds"] is verdict["scoped_nogo"]:
        fail("exactly one verdict")
    if verdict["equation_20_closed"] is not False or verdict["equation_28_closed"] is not False:
        fail("open equations")
    if verdict["missing_primitive"] != chk.MISSING_PRIMITIVE:
        fail("missing primitive")
    if verdict["fiber_gap"] != "-1":
        fail("fiber gap")
    if verdict["recording_distinguishes_fiber_shift"] is not True:
        fail("recording distinction")
    if verdict["address_marginal_distinguishes_fiber_shift"] is not False:
        fail("marginal distinction")
    if verdict["residual_descends_to_address"] is not False:
        fail("descent")
    if verdict["word_field_jet"] != "0":
        fail("field jet")
    if verdict["pin"] != chk.PIN:
        fail("pin")
    if verdict["phase_fiber_versus_dressed_address"] is not True:
        fail("index gap")
    if verdict["phase_index"] == verdict["dressed_index"]:
        fail("indexes collapsed")

    expect_fraud("rename", renamed=True)
    expect_fraud("index identification", identify_phase_with_dressed_site=True)
    expect_fraud("force identity", force_identity=True)
    expect_fraud("q renamed to mu", claim_q_equals_mu=True)
    expect_fraud("equation 20 closed", close_equation_20=True)
    expect_fraud("equation 28 closed", close_equation_28=True)
    expect_fraud("einstein copy", stress=sp.eye(4), einstein=sp.eye(4))
    expect_fraud(
        "flat einstein copy",
        stress=sp.zeros(4),
        einstein=sp.zeros(4),
    )
    print("PASS")


if __name__ == "__main__":
    main()
