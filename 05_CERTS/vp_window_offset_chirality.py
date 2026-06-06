#!/usr/bin/env python3
"""Finite certificate for acceptance-window offset chirality."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path


PASS_TOKEN = "PASS_CHIRAL_WINDOW_OFFSET"


def contains(center: Fraction, radius: Fraction, x: Fraction) -> bool:
    return center - radius <= x <= center + radius


def inversion_symmetric(center: Fraction, radius: Fraction, samples: list[Fraction]) -> bool:
    return all(contains(center, radius, x) == contains(center, radius, -x) for x in samples)


def main() -> dict:
    samples = [Fraction(n, 2) for n in range(-8, 9)]
    centered = (Fraction(0), Fraction(2))
    offset = (Fraction(1), Fraction(0))
    witness = Fraction(1)

    left_right_readout = {
        "x": contains(offset[0], offset[1], witness),
        "-x": contains(offset[0], offset[1], -witness),
    }
    checks = {
        "centered_interval_has_inversion_symmetry": inversion_symmetric(*centered, samples),
        "offset_interval_breaks_inversion_symmetry": left_right_readout["x"] and not left_right_readout["-x"],
        "offset_is_nonzero": offset[0] != 0,
        "sign_branch_asymmetric_readout": left_right_readout["x"] != left_right_readout["-x"],
    }
    status = PASS_TOKEN if all(checks.values()) else "FAIL"
    return {
        "status": status,
        "centered": [str(x) for x in centered],
        "offset": [str(x) for x in offset],
        "witness": str(witness),
        "left_right_readout": left_right_readout,
        "checks": checks,
    }


if __name__ == "__main__":
    out = main()
    here = Path(__file__).resolve().parent
    (here / "vp_window_offset_chirality_results.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8"
    )
    print(out["status"])
    for name, ok in out["checks"].items():
        print(f"{name}: {ok}")
    if out["status"] != PASS_TOKEN:
        raise SystemExit(1)
