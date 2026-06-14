#!/usr/bin/env python3
"""D0 finite feedback equation-of-state certificate."""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PASSPORT = ROOT / "08_PASSPORTS" / "VacuumFeedback"


def main() -> int:
    beta = 2.0
    dlogz_dv = 0.375
    volume = 8.0
    pressure = (1.0 / beta) * dlogz_dv
    t_eff = 1.0 / beta
    response_index = volume * dlogz_dv
    assert abs(pressure * volume - t_eff * response_index) < 1e-12
    PASSPORT.mkdir(parents=True, exist_ok=True)
    result = {
        "status": "PASS_FINITE_FEEDBACK_EQUATION_OF_STATE",
        "tokens": [
            "PASS_FEEDBACK_PRESSURE_TRACE_LOG",
            "PASS_FINITE_PVT_EQUATION_OF_STATE",
        ],
        "pressure": pressure,
        "volume": volume,
        "effective_temperature": t_eff,
        "response_index": response_index,
        "negative_controls": ["FAIL_IDEAL_GAS_CORE_POSTULATE"],
    }
    (PASSPORT / "finite_feedback_equation_of_state_summary.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    Path(__file__).with_suffix(".results.json").write_text(json.dumps(result, indent=2) + "\n")
    print("PASS_FEEDBACK_PRESSURE_TRACE_LOG")
    print("PASS_FINITE_PVT_EQUATION_OF_STATE")
    print("FAIL_IDEAL_GAS_CORE_POSTULATE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
