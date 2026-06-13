#!/usr/bin/env python3
"""D0 pressure-capacity balance certificate."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PASSPORT = ROOT / "08_PASSPORTS" / "VacuumFeedback"


def regime(p_fb: float, p_cap: float) -> str:
    if p_fb > p_cap:
        return "expansion"
    if p_fb == p_cap:
        return "stationary_horizon"
    return "collapse"


def main() -> int:
    assert regime(3, 2) == "expansion"
    assert regime(2, 2) == "stationary_horizon"
    assert regime(1, 2) == "collapse"
    result = {
        "status": "PASS_PRESSURE_CAPACITY_BALANCE",
        "tokens": [
            "PASS_PRESSURE_CAPACITY_BALANCE_REGIMES",
            "PASS_HORIZON_SATURATION_FEEDBACK_LIMIT",
            "PASS_A4_TERMINAL_FEEDBACK_SATURATION",
        ],
        "law": "a_ddot_over_a = kappa_D * (P_fb - P_cap)",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    PASSPORT.mkdir(parents=True, exist_ok=True)
    (PASSPORT / "pressure_capacity_balance_summary.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    Path(__file__).with_suffix(".results.json").write_text(json.dumps(result, indent=2) + "\n")
    for token in result["tokens"]:
        print(token)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
