#!/usr/bin/env python3
"""Replay the selected crossed-null jet and test its first omitted Ward source.

The registered quartic and asymmetric-order-four checkers construct one exact
RREF representative through thirteen amplitude coefficients. This checker
extends the Lorentz exponential to degree five, forms the original coframe
Euler rows, and evaluates the four adjoint coframe-gradient Ward projections
at [a^3*b^2] and [a^2*b^3]. It does not vary the lower-order kernel choices.
"""
import contextlib
import io
import json
import runpy
from pathlib import Path

import sympy as s


ROOT = Path(__file__).resolve().parents[4]
SOURCE = (ROOT / "02_REGISTRY/gr_assembly/sources/"
          "d0_double_null_asymmetric_order4_jet_2026-10-19/"
          "check_asymmetric_order4_jet.py")


def expected_result():
    return {
        "3,2": [
            [[[1, 0], "3/32"], [[0, 0], "-3/128"]], [], [], []
        ],
        "2,3": [
            [],
            [[[1, 0], "-1/128"], [[0, 1], "11/128"], [[0, 0], "13/256"]],
            [], [],
        ],
    }


def main():
    # This performs the exact registered mixed-quartic and asymmetric-quartic
    # RREF replays and retains their selected solution dictionaries in state.
    with contextlib.redirect_stdout(io.StringIO()):
        state = runpy.run_path(str(SOURCE))

    replay = state["replay"]
    x, y = state["x"], state["y"]
    replay.MAX = 3

    def expj_degree_five(logarithm):
        result = replay.Jet(replay.I)
        term = replay.Jet(replay.I)
        for degree in range(1, 6):
            term = term * logarithm / s.Integer(degree)
            result = result + term
        return result

    replay.expj = expj_degree_five
    coframe_rows = replay.solder_rows((0, 0, x, y))
    require = lambda condition, message: (_ for _ in ()).throw(
        AssertionError(message)) if not condition else None
    require(len(coframe_rows) == 16, "expected all 16 coframe Euler rows")

    report = {
        "status": "EXACT_NONZERO_SELECTED_BRANCH_WARD_SOURCE",
        "amplitude_orders": [[3, 2], [2, 3]],
        "lorentz_exponential_degree": 5,
        "ward_convention": "sum_mu (E_e[a,mu](x) - E_e[a,mu](x+e_mu)); null-axis shifts vanish on this transverse carrier",
        "ward_components": {},
        "selected_branch_only": True,
        "all_degree_five_corrections_compatible": False,
    }

    for amplitude in ((3, 2), (2, 3)):
        internal_rows = []
        for internal in range(4):
            divergence = s.expand(sum(
                coframe_rows[4 * internal + mu].coeff(*amplitude)
                - coframe_rows[4 * internal + mu].coeff(*amplitude).subs(
                    {x: x + (1 if mu == 2 else 0),
                     y: y + (1 if mu == 3 else 0)})
                for mu in range(4)))
            polynomial = s.Poly(divergence, x, y)
            terms = [[list(monomial), str(coefficient)]
                     for monomial, coefficient in polynomial.terms()
                     if coefficient != 0]
            internal_rows.append(terms)
        report["ward_components"][f"{amplitude[0]},{amplitude[1]}"] = internal_rows

    require(report["ward_components"] == expected_result(),
            "exact fifth-order Ward source changed")
    print(json.dumps(report, indent=2, sort_keys=True))
    print("PASS: the pinned RREF representative has a nonzero exact fifth-order coframe-gradient Ward source")
    print("SCOPE: other lower-order homogeneous modes, all-order roots, refinement and physical D0 selection remain open")


if __name__ == "__main__":
    main()
