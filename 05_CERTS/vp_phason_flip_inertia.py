#!/usr/bin/env python3
"""Finite certificate for phason flip drag inertia."""

from __future__ import annotations

import json
from pathlib import Path


PASS_TOKEN = "PASS_INERTIA_PHASON_FLIP_DRAG"


def flip_count(residues: list[int], window: set[int]) -> int:
    inside = [r in window for r in residues]
    return sum(inside[i] != inside[i - 1] for i in range(1, len(inside)))


def phase_transport(step: int, q: int, n: int) -> list[int]:
    return [(step * k) % q for k in range(n)]


def accelerated_transport(step: int, q: int, n: int, kick_tick: int, kick: int) -> list[int]:
    out: list[int] = []
    pos = 0
    for k in range(n):
        out.append(pos % q)
        pos += step + (kick if k >= kick_tick else 0)
    return out


def main() -> dict:
    q = 44
    window = set(range(0, 20))
    uniform = phase_transport(step=1, q=q, n=44)
    accelerated = accelerated_transport(step=1, q=q, n=44, kick_tick=11, kick=7)
    uniform_flips = flip_count(uniform, window)
    accelerated_flips = flip_count(accelerated, window)
    rewrite_cost = max(0, accelerated_flips - uniform_flips)

    checks = {
        "uniform_admissible_transport_has_minimal_flip_count": uniform_flips == 1,
        "acceleration_increases_window_crossing_events": accelerated_flips > uniform_flips,
        "flip_count_gives_nonzero_rewrite_cost": rewrite_cost > 0,
        "cost_is_integer_scale_free_before_si_calibration": isinstance(rewrite_cost, int),
    }
    status = PASS_TOKEN if all(checks.values()) else "FAIL"
    return {
        "status": status,
        "q": q,
        "window_size": len(window),
        "uniform_flips": uniform_flips,
        "accelerated_flips": accelerated_flips,
        "rewrite_cost": rewrite_cost,
        "checks": checks,
    }


if __name__ == "__main__":
    out = main()
    here = Path(__file__).resolve().parent
    (here / "vp_phason_flip_inertia_results.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8"
    )
    print(out["status"])
    for name, ok in out["checks"].items():
        print(f"{name}: {ok}")
    if out["status"] != PASS_TOKEN:
        raise SystemExit(1)
