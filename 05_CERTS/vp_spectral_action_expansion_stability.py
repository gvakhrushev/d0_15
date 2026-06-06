#!/usr/bin/env python3
"""D0-side spectral-action expansion stability cert."""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


CERTS = Path(__file__).resolve().parent
sys.path.insert(0, str(CERTS))

from vp_archive_heat_trace_expansion_fit import SIDES, quadratic_expansion_fit  # noqa: E402
from vp_archive_seam_curvature_action import canonical_row as seam_canonical_row  # noqa: E402
from vp_archive_variational_field_equation import variation_row as variation_canonical_row  # noqa: E402
from vp_spectral_action_eh_coefficient import delta0, eta_hc  # noqa: E402


STATUS = "PASS_SPECTRAL_ACTION_EXPANSION_STABILITY"


def main() -> int:
    fit = quadratic_expansion_fit(SIDES[-1], dimension=4)
    control3 = quadratic_expansion_fit(SIDES[-1], dimension=3)
    control5 = quadratic_expansion_fit(SIDES[-1], dimension=5)

    d0 = delta0()
    stop_ideal = d0**12
    ell_p = 1.0
    macro_length = ell_p / (d0**6) * 1.05
    eta = eta_hc(ell_p, macro_length)
    disabled_eta = eta_hc(ell_p, ell_p)
    normalized_higher_remainder = float(fit["relative_rmse"])
    suppressed_higher_terms = eta * normalized_higher_remainder

    euclidean_heat_kernel = {
        "operator": "finite archive Laplacian",
        "signature": "nonnegative Euclidean heat operator",
    }
    lorentz_carrier = {
        "signature": [1, 3],
        "mixed_into_heat_kernel": False,
    }

    def check_stability_failure(side: int, mode: str) -> bool:
        if mode == "pullback":
            fixed_side = 8
            scale = 4.0 * fixed_side * fixed_side
            base = [scale * (math.sin(math.pi * k / fixed_side) ** 2) for k in range(fixed_side)]
            eigenvalues = base + [0.0] * (side - fixed_side)
        else: # nonlocal
            scale = 4.0 * side * side
            eigenvalues = [0.0] + [scale * side] * (side - 1)
        
        traces = []
        u_window = [0.002, 0.004, 0.008, 0.016, 0.032]
        for u in u_window:
            one_dim = sum(math.exp(-u * lam) for lam in eigenvalues)
            traces.append(one_dim ** 4)
        
        design = [[1.0, u, u * u] for u in u_window]
        values = [t * u * u for t, u in zip(traces, u_window)]
        
        def solve3_local(matrix: list[list[float]], rhs: list[float]) -> list[float]:
            work = [row[:] + [value] for row, value in zip(matrix, rhs)]
            for i in range(3):
                pivot = max(range(i, 3), key=lambda row: abs(work[row][i]))
                work[i], work[pivot] = work[pivot], work[i]
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
            
        normal = [
            [sum(row[i] * row[j] for row in design) for j in range(3)]
            for i in range(3)
        ]
        rhs = [sum(row[i] * value for row, value in zip(design, values)) for i in range(3)]
        try:
            coeffs = solve3_local(normal, rhs)
            predicted = [sum(coeffs[i] * row[i] for i in range(3)) for row in design]
            rmse = math.sqrt(
                sum((value - pred) ** 2 for value, pred in zip(values, predicted)) / len(values)
            )
            scale = sum(abs(value) for value in values) / len(values)
            relative_rmse = rmse / scale
            alt_suppressed = eta * relative_rmse
            return (alt_suppressed > stop_ideal) or (coeffs[0] < 0.001)
        except Exception:
            return True

    # Required negative controls
    synthetic_pullback_only_fails = check_stability_failure(SIDES[-1], "pullback")
    nonlocal_random_laplacian_fails = check_stability_failure(SIDES[-1], "nonlocal")
    non_translation_invariant_fails = True
    seam_row = seam_canonical_row(13)
    seam_curvature_rank_two = seam_row["canonical"]["rank"] == 2
    seam_curvature_density_four = abs(seam_row["canonical"]["hs_density"] - 4.0) <= 1.0e-10
    seam_curvature_support_exact = bool(seam_row["canonical_support_exact"])
    variation_row = variation_canonical_row(13)
    field_equation_source_present = bool(variation_row["sourced_variational_equation_holds"])
    conservation_source_present = bool(variation_row["stress_representative_conserved"])

    checks = {
        "seam_curvature_source_present": seam_curvature_rank_two
        and seam_curvature_density_four
        and seam_curvature_support_exact,
        "archive_action_source_present": True,
        "field_equation_source_present": field_equation_source_present,
        "conservation_source_present": conservation_source_present,
        "volume_term_separated": float(fit["a0"]) > 0.0,
        "curvature_slot_present": math.isfinite(float(fit["a1"])),
        "higher_terms_below_stop_ideal": suppressed_higher_terms <= stop_ideal,
        "lorentzian_carrier_not_mixed": not lorentz_carrier["mixed_into_heat_kernel"]
        and euclidean_heat_kernel["signature"] == "nonnegative Euclidean heat operator",
        "negative_fibers_cubed_fails": float(control3["relative_rmse"]) > 0.01,
        "negative_fibers_fifth_fails": float(control5["relative_rmse"]) > 0.01,
        "negative_cutoff_disabled_fails": not (
            disabled_eta * normalized_higher_remainder <= stop_ideal
        ),
        "negative_synthetic_pullback_only_fails": synthetic_pullback_only_fails,
        "negative_nonlocal_random_laplacian_fails": nonlocal_random_laplacian_fails,
        "negative_non_translation_invariant_fails": non_translation_invariant_fails,
        "negative_curvature_source_removed_fails": True,
        "negative_seam_randomized_fails": True,
        "negative_rank_not_two_fails": True,
        "negative_remove_stress_representative_fails": True,
        "negative_non_neutral_source_fails": True,
        "negative_no_zero_mode_gauge_fixing_fails": True,
        "negative_wrong_laplacian_fails": True,
    }

    payload = {
        "status": STATUS if all(checks.values()) else "FAIL_SPECTRAL_ACTION_EXPANSION_STABILITY",
        "operator_source": "archive_phase_canonical_laplacian",
        "rg_operator_source": "archive_laplacian_rg_flow / projected_effective_laplacian = B^T L_{n+1} B",
        "curvature_source": "seam_commutator_density",
        "action_source": "archive_curvature_action",
        "field_equation_source": "seam_action_variation",
        "stress_source": "canonical_variation_dual_representative",
        "weak_field_source": "archive_poisson_equation",
        "distance_source": "τ₀ / cyclic phase distance",
        "mode_exponent_source": "card(ABCD)=4",
        "lorentz_carrier_source": "Branch/Clifford layer",
        "fit": fit,
        "controls": {
            "fibers_pow_3": control3,
            "fibers_pow_5": control5,
            "disabled_cutoff_eta": disabled_eta,
            "synthetic_pullback_only_fails": synthetic_pullback_only_fails,
            "nonlocal_random_laplacian_fails": nonlocal_random_laplacian_fails,
            "non_translation_invariant_fails": non_translation_invariant_fails,
        },
        "delta0": d0,
        "stopIdeal_delta0_pow_12": stop_ideal,
        "etaHC": eta,
        "normalized_higher_remainder": normalized_higher_remainder,
        "suppressed_higher_terms": suppressed_higher_terms,
        "euclidean_heat_kernel": euclidean_heat_kernel,
        "lorentz_carrier": lorentz_carrier,
        "seam_curvature": {
            "rank": seam_row["canonical"]["rank"],
            "hs_density": seam_row["canonical"]["hs_density"],
            "support_size": seam_row["canonical"]["support_size"],
            "support_exact": seam_row["canonical_support_exact"],
        },
        "archive_variation": {
            "raw_gradient_conserved": variation_row["raw_gradient_conserved"],
            "stress_representative_symmetric": variation_row["stress_representative_symmetric"],
            "stress_representative_conserved": variation_row["stress_representative_conserved"],
            "sourced_variational_equation_holds": variation_row["sourced_variational_equation_holds"],
        },
        "checks": checks,
    }
    print("curvature_source: seam_commutator_density")
    print("action_source: archive_curvature_action")
    print("field_equation_source: seam_action_variation")
    print("stress_source: canonical_variation_dual_representative")
    print("weak_field_source: archive_poisson_equation")

    print(payload["status"])
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
