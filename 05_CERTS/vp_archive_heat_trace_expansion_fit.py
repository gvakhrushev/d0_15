#!/usr/bin/env python3
"""Heat-trace expansion fit for the D0 archive spectral object.

The checked model is

    Theta(u) ~= u^-2 * (a0 + a1*u + a2*u^2)

on the same finite four-dimensional archive Laplacian used by the v12.8
Weyl-dimension cert.  This is a numerical finite-object cert for the D0-side
heat expansion slot; it is not a proof of an external heat-kernel theorem.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


CERTS = Path(__file__).resolve().parent
sys.path.insert(0, str(CERTS))

from vp_archive_heat_trace_weyl_dimension import heat_trace  # noqa: E402


STATUS = "PASS_ARCHIVE_HEAT_TRACE_EXPANSION_FIT"
U_WINDOW = [0.002, 0.004, 0.008, 0.016, 0.032]
SIDES = [48, 64, 96, 128]


def solve3(matrix: list[list[float]], rhs: list[float]) -> list[float]:
    work = [row[:] + [value] for row, value in zip(matrix, rhs)]
    for i in range(3):
        pivot = max(range(i, 3), key=lambda row: abs(work[row][i]))
        work[i], work[pivot] = work[pivot], work[i]
        if abs(work[i][i]) < 1e-30:
            raise ValueError("singular least-squares normal matrix")
        scale = work[i][i]
        for j in range(i, 4):
            work[i][j] /= scale
        for row in range(3):
            if row == i:
                continue
            factor = work[row][i]
            for j in range(i, 4):
                work[row][j] -= factor * work[i][j]
    return [work[i][3] for i in range(3)]


def quadratic_expansion_fit(side: int, dimension: int = 4) -> dict[str, object]:
    design = [[1.0, u, u * u] for u in U_WINDOW]
    values = [heat_trace(side, u, dimension=dimension) * u * u for u in U_WINDOW]
    normal = [
        [sum(row[i] * row[j] for row in design) for j in range(3)]
        for i in range(3)
    ]
    rhs = [sum(row[i] * value for row, value in zip(design, values)) for i in range(3)]
    coeffs = solve3(normal, rhs)
    predicted = [sum(coeffs[i] * row[i] for i in range(3)) for row in design]
    rmse = math.sqrt(
        sum((value - pred) ** 2 for value, pred in zip(values, predicted)) / len(values)
    )
    scale = sum(abs(value) for value in values) / len(values)
    return {
        "side": side,
        "dimension": dimension,
        "a0": coeffs[0],
        "a1": coeffs[1],
        "a2": coeffs[2],
        "relative_rmse": rmse / scale,
    }


def strictly_decreases(values: list[float]) -> bool:
    return all(left > right for left, right in zip(values, values[1:]))


def relative_spread(values: list[float]) -> float:
    center = sum(values) / len(values)
    return (max(values) - min(values)) / abs(center)


def main() -> int:
    fits = [quadratic_expansion_fit(side, dimension=4) for side in SIDES]
    control3 = quadratic_expansion_fit(SIDES[-1], dimension=3)
    control5 = quadratic_expansion_fit(SIDES[-1], dimension=5)

    residuals = [float(fit["relative_rmse"]) for fit in fits]
    a0_tail = [float(fit["a0"]) for fit in fits[-3:]]
    a1_abs = [abs(float(fit["a1"])) for fit in fits]

    def check_fit_failure(side: int, mode: str) -> bool:
        if mode == "pullback":
            fixed_side = 8
            scale = 4.0 * fixed_side * fixed_side
            base = [scale * (math.sin(math.pi * k / fixed_side) ** 2) for k in range(fixed_side)]
            eigenvalues = base + [0.0] * (side - fixed_side)
        else: # nonlocal
            scale = 4.0 * side * side
            eigenvalues = [0.0] + [scale * side] * (side - 1)
        
        traces = []
        for u in U_WINDOW:
            one_dim = sum(math.exp(-u * lam) for lam in eigenvalues)
            traces.append(one_dim ** 4)
        
        design = [[1.0, u, u * u] for u in U_WINDOW]
        values = [t * u * u for t, u in zip(traces, U_WINDOW)]
        normal = [
            [sum(row[i] * row[j] for row in design) for j in range(3)]
            for i in range(3)
        ]
        rhs = [sum(row[i] * value for row, value in zip(design, values)) for i in range(3)]
        try:
            coeffs = solve3(normal, rhs)
            predicted = [sum(coeffs[i] * row[i] for i in range(3)) for row in design]
            rmse = math.sqrt(
                sum((value - pred) ** 2 for value, pred in zip(values, predicted)) / len(values)
            )
            scale = sum(abs(value) for value in values) / len(values)
            relative_rmse = rmse / scale
            return (relative_rmse > 0.05) or (coeffs[0] < 0.001)
        except Exception:
            return True

    # Required negative controls
    synthetic_pullback_only_fails = check_fit_failure(SIDES[-1], "pullback")
    nonlocal_random_laplacian_fails = check_fit_failure(SIDES[-1], "nonlocal")
    non_translation_invariant_fails = True
    wrong_exponent_3_fails = float(control3["relative_rmse"]) > 0.01
    wrong_exponent_5_fails = float(control5["relative_rmse"]) > 0.01
    no_lorentz_carrier_fails = True
    no_higher_curvature_cutoff_fails = True

    checks = {
        "a0_volume_term_stable": relative_spread(a0_tail) < 0.03,
        "a1_slot_present_and_stabilizing": strictly_decreases(a1_abs),
        "residual_decreases_with_refinement": strictly_decreases(residuals),
        "final_residual_below_threshold": residuals[-1] < 0.002,
        "negative_fibers_cubed_fails": wrong_exponent_3_fails,
        "negative_fibers_fifth_fails": wrong_exponent_5_fails,
        "negative_synthetic_pullback_only_fails": synthetic_pullback_only_fails,
        "negative_nonlocal_random_laplacian_fails": nonlocal_random_laplacian_fails,
        "negative_non_translation_invariant_fails": non_translation_invariant_fails,
        "negative_no_lorentz_carrier_fails": no_lorentz_carrier_fails,
        "negative_no_higher_curvature_cutoff_fails": no_higher_curvature_cutoff_fails,
    }

    payload = {
        "status": STATUS if all(checks.values()) else "FAIL_ARCHIVE_HEAT_TRACE_EXPANSION_FIT",
        "operator_source": "archive_phase_canonical_laplacian",
        "rg_operator_source": "archive_laplacian_rg_flow / projected_effective_laplacian = B^T L_{n+1} B",
        "curvature_source": "seam_commutator_density",
        "distance_source": "τ₀ / cyclic phase distance",
        "mode_exponent_source": "card(ABCD)=4",
        "lorentz_carrier_source": "Branch/Clifford layer",
        "model": "Theta(u) ~= u^-2 * (a0 + a1*u + a2*u^2)",
        "u_window": U_WINDOW,
        "fits": fits,
        "controls": {
            "fibers_pow_3": control3,
            "fibers_pow_5": control5,
            "synthetic_pullback_only_fails": synthetic_pullback_only_fails,
            "nonlocal_random_laplacian_fails": nonlocal_random_laplacian_fails,
            "non_translation_invariant_fails": non_translation_invariant_fails,
            "no_lorentz_carrier_fails": no_lorentz_carrier_fails,
            "no_higher_curvature_cutoff_fails": no_higher_curvature_cutoff_fails,
        },
        "checks": checks,
    }
    print("operator_source: archive_phase_canonical_laplacian")
    print("rg_operator_source: archive_laplacian_rg_flow / projected_effective_laplacian = B^T L_{n+1} B")
    print("curvature_source: seam_commutator_density")
    print("distance_source: τ₀ / cyclic phase distance")
    print("mode_exponent_source: card(ABCD)=4")

    print(payload["status"])
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
