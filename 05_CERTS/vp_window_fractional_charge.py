#!/usr/bin/env python3
"""Finite certificate for fractional charge as window-sector weight."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path


PASS_TOKEN = "PASS_FRACTIONAL_CHARGE_WINDOW_WEIGHT"


SECTORS = ("c0", "c1", "c2")


def weight(selected: set[str]) -> Fraction:
    return Fraction(len(selected), len(SECTORS))


def signed(sign: int, selected: set[str]) -> Fraction:
    return sign * weight(selected)


def main() -> dict:
    one_sector = {"c0"}
    two_sector = {"c0", "c1"}
    signed_values = {
        signed(sign, selected)
        for sign in (-1, 1)
        for selected in (one_sector, two_sector)
    }
    neutral_triple = sum(weight({s}) for s in SECTORS) - 1
    checks = {
        "three_sector_partition": len(SECTORS) == 3 and len(set(SECTORS)) == 3,
        "single_sector_weight_eq_one_third": weight(one_sector) == Fraction(1, 3),
        "double_sector_weight_eq_two_thirds": weight(two_sector) == Fraction(2, 3),
        "sign_branch_gives_plus_minus": signed_values
        == {Fraction(-2, 3), Fraction(-1, 3), Fraction(1, 3), Fraction(2, 3)},
        "neutral_triple_sum_cancels": neutral_triple == 0,
    }
    status = PASS_TOKEN if all(checks.values()) else "FAIL"
    return {
        "status": status,
        "signed_values": sorted(str(v) for v in signed_values),
        "neutral_triple": str(neutral_triple),
        "checks": checks,
    }


if __name__ == "__main__":
    out = main()
    here = Path(__file__).resolve().parent
    (here / "vp_window_fractional_charge_results.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8"
    )
    print(out["status"])
    for name, ok in out["checks"].items():
        print(f"{name}: {ok}")
    if out["status"] != PASS_TOKEN:
        raise SystemExit(1)
