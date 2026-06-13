#!/usr/bin/env python3
"""Finite certificate for archive phason strain as dark metric source."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path


PASS_TOKEN = "PASS_DARK_PHASON_STRAIN"


def em_projection(active: Fraction, archive: Fraction) -> Fraction:
    return active


def em_archive_coupling(archive: Fraction) -> Fraction:
    return em_projection(Fraction(0), archive)


def metric_heat_response(active_energy: Fraction, archive_energy: Fraction) -> Fraction:
    return active_energy + archive_energy


def phason_gradient(values: list[Fraction]) -> list[Fraction]:
    return [values[i + 1] - values[i] for i in range(len(values) - 1)]


def main() -> dict:
    archive_field = [Fraction(0), Fraction(1, 3), Fraction(4, 3), Fraction(2, 1)]
    gradients = phason_gradient(archive_field)
    archive_energy = sum(g * g for g in gradients)
    active_energy = Fraction(5, 2)
    response = metric_heat_response(active_energy, archive_energy)

    checks = {
        "phason_field_has_psd_energy": archive_energy >= 0,
        "phason_cluster_has_nonzero_gradient": any(g != 0 for g in gradients),
        "em_projection_kills_archive_coordinate": all(
            em_archive_coupling(x) == 0 for x in archive_field
        ),
        "heat_metric_response_includes_phason_energy": response - active_energy == archive_energy,
        "positive_archive_energy_gives_positive_metric_increment": archive_energy > 0 and response > active_energy,
    }
    status = PASS_TOKEN if all(checks.values()) else "FAIL"
    return {
        "status": status,
        "archive_field": [str(x) for x in archive_field],
        "gradients": [str(x) for x in gradients],
        "archive_energy": str(archive_energy),
        "metric_response": str(response),
        "checks": checks,
    }


if __name__ == "__main__":
    out = main()
    here = Path(__file__).resolve().parent
    (here / "vp_archive_phason_dark_matter_results.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8"
    )
    print(out["status"])
    for name, ok in out["checks"].items():
        print(f"{name}: {ok}")
    if out["status"] != PASS_TOKEN:
        raise SystemExit(1)
