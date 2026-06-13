#!/usr/bin/env python3
"""Derivation step: boundary off-diagonal curvature stationarity audit."""

from __future__ import annotations

import json
import math
from pathlib import Path

from d0_graph import PARTS, delta_0, phi


def _q_res() -> tuple[float, float, float]:
    root = Path(__file__).resolve().parents[1]
    numeric = json.loads((root / "00_INDEX" / "NUMERIC_SUMMARY.json").read_text(encoding="utf-8"))
    alpha_g_dressed = float(numeric["electron"]["alphaG_dressed"])
    omega8 = 8.0
    v9, v11, v13 = PARTS
    length_projection = omega8 * phi ** (v9 * v11) * (1.0 + delta_0 / v13)
    gamma_length = (2.0 * math.pi / (38.0 * length_projection)) ** 2
    q_exact = alpha_g_dressed / gamma_length
    q_layer = 1.0 / (1.0 + delta_0**3)
    return q_exact, q_layer, q_exact / q_layer


def _qres_from_c2(c2: float) -> float:
    a = delta_0**3
    b = delta_0**6
    return 1.0 / (1.0 - c2 / ((1.0 + a) * (1.0 + b)))


def run_vp_derivation_boundary_curvature_stationarity() -> dict[str, object]:
    q_exact, q_layer, q_res = _q_res()
    target_inc = q_res - 1.0
    a = delta_0**3
    b = delta_0**6
    required_c2 = (1.0 + a) * (1.0 + b) * (1.0 - 1.0 / q_res)
    required_ratio = required_c2 / b

    # Candidate stationarity rules.  These are derived from simple internal
    # balancing principles and then tested against the required residual.
    rules = {
        "rank_cycle_balance_8_over_5": 8.0 / 5.0,
        "terminal_cycle_balance_13_over_8": 13.0 / 8.0,
        "terminal_cycle_with_cycle_attenuation": (13.0 / 8.0) / (1.0 + delta_0 / 8.0),
        "terminal_cycle_with_layer3_rank_correction": (13.0 / 8.0)
        / (1.0 + delta_0 / 9.0)
        * (1.0 + delta_0**3 / 38.0),
        "best_previous_candidate": (13.0 / 8.0) / (1.0 + delta_0 / 8.0) * (1.0 + delta_0**3 / 3.0),
    }
    ledger = []
    for name, ratio in rules.items():
        c2 = b * ratio
        inc = _qres_from_c2(c2) - 1.0
        ledger.append(
            {
                "rule": name,
                "c2_over_delta0_6": ratio,
                "c2": c2,
                "q_res_minus_1": inc,
                "relative_error_to_required_c2": abs(ratio / required_ratio - 1.0),
                "relative_error_to_q_res_increment": abs(inc / target_inc - 1.0),
            }
        )
    ledger.sort(key=lambda row: row["relative_error_to_required_c2"])
    exact = [row for row in ledger if row["relative_error_to_required_c2"] < 1e-10]
    return {
        "status": "PASS_BOUNDARY_CURVATURE_STATIONARITY_NO_GO" if not exact else "PASS_BOUNDARY_CURVATURE_STATIONARITY_DERIVED",
        "offdiag_resolvent_formula": "q_res = 1/(1-c^2/((1+delta0^3)(1+delta0^6)))",
        "q_exact": q_exact,
        "q_layer": q_layer,
        "q_res": q_res,
        "required_c2": required_c2,
        "required_c2_over_delta0_6": required_ratio,
        "stationarity_rule_ledger": ledger,
        "no_go": (
            "Simple stationarity balances narrow the coupling but do not derive "
            "the exact q_res residual.  A valid closure needs an additional "
            "non-diagonal boundary action term whose Euler equation fixes c."
        ),
    }


def main() -> None:
    result = run_vp_derivation_boundary_curvature_stationarity()
    print(f"VP derivation boundary curvature stationarity: [{result['status']}]")
    for key, value in result.items():
        if key != "status":
            print(f"{key}= {value}")


if __name__ == "__main__":
    main()
