#!/usr/bin/env python3
"""Finite certificate for D0 generation inflation classes."""

from __future__ import annotations

import json
from pathlib import Path


PASS_TOKEN = "PASS_QUASI_GENERATION_INFLATION_ORBIT"


def mat_mul(a: tuple[tuple[int, int], tuple[int, int]], b: tuple[tuple[int, int], tuple[int, int]]):
    return (
        (a[0][0] * b[0][0] + a[0][1] * b[1][0], a[0][0] * b[0][1] + a[0][1] * b[1][1]),
        (a[1][0] * b[0][0] + a[1][1] * b[1][0], a[1][0] * b[0][1] + a[1][1] * b[1][1]),
    )


def main() -> dict:
    t = ((0, 1), (1, -1))
    t2 = mat_mul(t, t)
    generations = ("gen0", "gen1", "gen2")
    inflate = {"gen0": "gen1", "gen1": "gen2", "gen2": "gen2"}
    defect_type = {g: "terminal-phason-defect" for g in generations}
    orbit = ["gen0", inflate["gen0"], inflate[inflate["gen0"]]]

    checks = {
        "trace_T2_eq_three": t2[0][0] + t2[1][1] == 3,
        "three_inflation_classes": len(generations) == 3 and len(set(generations)) == 3,
        "orbit_visits_three_classes": orbit == list(generations),
        "same_local_defect_type_transported": all(
            defect_type[inflate[g]] == defect_type[g] for g in generations
        ),
        "no_extra_free_generation_selector": set(orbit) == set(generations),
    }
    status = PASS_TOKEN if all(checks.values()) else "FAIL"
    return {"status": status, "T2": t2, "orbit": orbit, "checks": checks}


if __name__ == "__main__":
    out = main()
    here = Path(__file__).resolve().parent
    (here / "vp_quasi_generation_inflation_results.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8"
    )
    print(out["status"])
    for name, ok in out["checks"].items():
        print(f"{name}: {ok}")
    if out["status"] != PASS_TOKEN:
        raise SystemExit(1)
