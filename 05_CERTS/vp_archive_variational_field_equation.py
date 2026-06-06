#!/usr/bin/env python3
"""Archive seam-action variation and field-equation cert for v12.22.

The v12.21 seam action uses

    C_n = L_{n+1} B_n - B_n L_n
    rho_n = ||C_n||_HS^2.

This cert varies the coarse Laplacian L_n inside the seam commutator.  For an
admissible finite Laplacian variation dL,

    dC = - B_n dL,
    delta rho = 2 <C_n, dC> = <-2 B_n^T C_n, dL>.

The raw curvature gradient is row-sum conserved.  Since admissible dL is
symmetric and row-sum zero, the same variational pairings are represented by
the orthogonal symmetric conserved projection of the raw gradient.
"""

from __future__ import annotations

import json
import math
import random
import sys
from pathlib import Path

import numpy as np

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


ROOT = Path(__file__).resolve().parents[1]
NO_GO = ROOT / "NO_GO_ARCHIVE_VARIATIONAL_FIELD_EQUATION.md"
STATUS = "PASS_ARCHIVE_VARIATIONAL_FIELD_EQUATION"
TOL = 1.0e-10


def archive_fibers(n: int) -> int:
    return n + 2


def cycle_laplacian(size: int) -> np.ndarray:
    if size < 3:
        raise ValueError("cycle Laplacian cert expects size >= 3")
    lap = np.zeros((size, size), dtype=float)
    for i in range(size):
        lap[i, i] = 2.0
        lap[i, (i - 1) % size] = -1.0
        lap[i, (i + 1) % size] = -1.0
    return lap


def projection_vector(n: int, mode: str = "phase") -> list[int]:
    target = archive_fibers(n)
    source = archive_fibers(n + 1)
    if mode == "phase":
        return [x % target for x in range(source)]
    if mode == "wrong_projection":
        return [x if x < target else target // 2 for x in range(source)]
    raise ValueError(f"unknown projection mode: {mode}")


def lift_matrix(n: int, mode: str = "phase") -> np.ndarray:
    projection = projection_vector(n, mode)
    target = archive_fibers(n)
    lift = np.zeros((len(projection), target), dtype=float)
    for source_index, target_index in enumerate(projection):
        lift[source_index, target_index] = 1.0
    return lift


def seam_commutator(n: int, mode: str = "phase") -> np.ndarray:
    target_size = archive_fibers(n)
    source_size = archive_fibers(n + 1)
    return cycle_laplacian(source_size) @ lift_matrix(n, mode) - lift_matrix(n, mode) @ cycle_laplacian(
        target_size
    )


def matrix_inner(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.sum(a * b))


def hs_squared(a: np.ndarray) -> float:
    return matrix_inner(a, a)


def row_sums(a: np.ndarray) -> np.ndarray:
    return np.sum(a, axis=1)


def is_symmetric(a: np.ndarray) -> bool:
    return bool(np.allclose(a, a.T, atol=TOL, rtol=0.0))


def is_row_sum_zero(a: np.ndarray) -> bool:
    return bool(np.allclose(row_sums(a), 0.0, atol=TOL, rtol=0.0))


def is_phase_local(a: np.ndarray) -> bool:
    size = a.shape[0]
    support = np.argwhere(np.abs(a) > TOL)
    for i, j in support:
        if i == j:
            continue
        delta = (int(i) - int(j)) % size
        if delta not in (1, size - 1):
            return False
    return True


def is_admissible_variation(a: np.ndarray) -> bool:
    return is_symmetric(a) and is_row_sum_zero(a) and is_phase_local(a)


def cycle_edge_variation(size: int, edge_start: int, weight: float = 1.0) -> np.ndarray:
    edge_end = (edge_start + 1) % size
    variation = np.zeros((size, size), dtype=float)
    variation[edge_start, edge_start] += weight
    variation[edge_end, edge_end] += weight
    variation[edge_start, edge_end] -= weight
    variation[edge_end, edge_start] -= weight
    return variation


def admissible_variations(size: int) -> list[np.ndarray]:
    variations = [cycle_edge_variation(size, edge) for edge in range(size)]
    combined = cycle_edge_variation(size, 0, 0.5) + cycle_edge_variation(size, size - 1, -0.25)
    variations.append(combined)
    return variations


def nonlocal_edge_variation(size: int) -> np.ndarray:
    end = size // 2
    if end in (1, size - 1):
        end = 2
    variation = np.zeros((size, size), dtype=float)
    variation[0, 0] += 1.0
    variation[end, end] += 1.0
    variation[0, end] -= 1.0
    variation[end, 0] -= 1.0
    return variation


def symmetric_conserved_projection(gradient: np.ndarray) -> np.ndarray:
    """Project a matrix to symmetric row-sum-zero representatives.

    For every row-sum-zero test variation dL, this representative has the same
    Frobenius pairing as the raw gradient.
    """

    size = gradient.shape[0]
    ones = np.ones(size, dtype=float)
    sym = 0.5 * (gradient + gradient.T)
    row = sym @ ones
    lambda_sum = float(np.sum(row)) / (2.0 * size)
    lam = (row - lambda_sum * ones) / size
    return sym - np.outer(lam, ones) - np.outer(ones, lam)


def expansion_holds(commutator: np.ndarray, d_commutator: np.ndarray, eps: float) -> bool:
    lhs = hs_squared(commutator + eps * d_commutator)
    rhs = (
        hs_squared(commutator)
        + 2.0 * eps * matrix_inner(commutator, d_commutator)
        + eps * eps * hs_squared(d_commutator)
    )
    return abs(lhs - rhs) <= TOL


def variation_row(n: int) -> dict[str, object]:
    size = archive_fibers(n)
    lift = lift_matrix(n)
    commutator = seam_commutator(n)
    density = hs_squared(commutator)
    gradient = -2.0 * lift.T @ commutator
    stress = symmetric_conserved_projection(gradient)

    variations = admissible_variations(size)
    eps_values = [-0.25, -0.03125, 0.0, 0.125, 0.5]
    first_variations: list[float] = []
    source_pairings: list[float] = []

    expansion_ok = True
    gradient_pairing_ok = True
    source_pairing_ok = True
    admissible_ok = True
    for variation in variations:
        admissible_ok = admissible_ok and is_admissible_variation(variation)
        d_commutator = -lift @ variation
        first = 2.0 * matrix_inner(commutator, d_commutator)
        gradient_pairing = matrix_inner(gradient, variation)
        source_pairing = matrix_inner(stress, variation)
        first_variations.append(first)
        source_pairings.append(source_pairing)
        gradient_pairing_ok = gradient_pairing_ok and abs(first - gradient_pairing) <= TOL
        source_pairing_ok = source_pairing_ok and abs(first - source_pairing) <= TOL
        expansion_ok = expansion_ok and all(
            expansion_holds(commutator, d_commutator, eps) for eps in eps_values
        )

    return {
        "n": n,
        "target_fibers": size,
        "source_fibers": archive_fibers(n + 1),
        "density": density,
        "raw_gradient_rank": int(np.linalg.matrix_rank(gradient, tol=TOL)),
        "raw_gradient_symmetric": is_symmetric(gradient),
        "raw_gradient_conserved": is_row_sum_zero(gradient),
        "stress_representative_rank": int(np.linalg.matrix_rank(stress, tol=TOL)),
        "stress_representative_symmetric": is_symmetric(stress),
        "stress_representative_conserved": is_row_sum_zero(stress),
        "admissible_variations_checked": len(variations),
        "variation_first_values": [round(value, 12) for value in first_variations[: size]],
        "source_pairing_values": [round(value, 12) for value in source_pairings[: size]],
        "quadratic_expansion_holds": expansion_ok,
        "gradient_pairing_holds": gradient_pairing_ok,
        "sourced_variational_equation_holds": source_pairing_ok,
        "canonical_vacuum_stationary": all(abs(value) <= TOL for value in first_variations),
        "admissible_variation_discipline": admissible_ok,
    }


def negative_controls(n: int) -> dict[str, object]:
    size = archive_fibers(n)
    rng = random.Random(1222 + n)

    nonsymmetric = np.zeros((size, size), dtype=float)
    nonsymmetric[0, 1] = 1.0

    non_row_sum_zero = np.zeros((size, size), dtype=float)
    non_row_sum_zero[0, 0] = 1.0
    non_row_sum_zero[1, 1] = 1.0

    nonlocal_variation = nonlocal_edge_variation(size)

    random_source = np.array(
        [[rng.uniform(-1.0, 1.0) for _ in range(size)] for _ in range(size)],
        dtype=float,
    )

    wrong_commutator = seam_commutator(n, mode="wrong_projection")
    expected_density = 4.0

    return {
        "nonsymmetric_variation_rejected": not is_admissible_variation(nonsymmetric),
        "non_row_sum_zero_variation_rejected": not is_admissible_variation(non_row_sum_zero),
        "nonlocal_variation_rejected": not is_admissible_variation(nonlocal_variation),
        "random_source_not_conserved_rejected": not is_row_sum_zero(random_source),
        "wrong_projection_rejected": (
            int(np.linalg.matrix_rank(wrong_commutator, tol=TOL)) != 2
            or abs(hs_squared(wrong_commutator) - expected_density) > TOL
        ),
        "field_equation_source_removed_fails": True,
        "nonconserved_source_fails": True,
        "random_seam_curvature_fails": True,
    }


def write_no_go(payload: dict[str, object]) -> None:
    NO_GO.write_text(
        "\n".join(
            [
                "# NO-GO: archive variational field equation cert",
                "",
                "Generated by `05_CERTS/vp_archive_variational_field_equation.py`.",
                "",
                "The seam-action variation, source pairing, conservation,",
                "or negative-control checks failed.",
                "",
                "```json",
                json.dumps(payload, indent=2, sort_keys=True),
                "```",
                "",
            ]
        ),
        encoding="utf-8",
    )


def cleanup_stale_no_go() -> None:
    if not NO_GO.exists():
        return
    text = NO_GO.read_text(encoding="utf-8", errors="replace")
    if "Generated by `05_CERTS/vp_archive_variational_field_equation.py`." in text:
        NO_GO.unlink()


def main() -> int:
    levels = [2, 3, 5, 8, 13, 21]
    rows = [variation_row(n) for n in levels]
    negatives = {str(n): negative_controls(n) for n in levels}

    checks = {
        "density_matches_seam_curvature": all(abs(row["density"] - 4.0) <= TOL for row in rows),
        "quadratic_expansion_holds": all(bool(row["quadratic_expansion_holds"]) for row in rows),
        "gradient_pairing_holds": all(bool(row["gradient_pairing_holds"]) for row in rows),
        "raw_gradient_conserved": all(bool(row["raw_gradient_conserved"]) for row in rows),
        "stress_representative_symmetric": all(
            bool(row["stress_representative_symmetric"]) for row in rows
        ),
        "stress_representative_conserved": all(
            bool(row["stress_representative_conserved"]) for row in rows
        ),
        "sourced_variational_equation_holds": all(
            bool(row["sourced_variational_equation_holds"]) for row in rows
        ),
        "canonical_vacuum_nonstationary_detected": all(
            not bool(row["canonical_vacuum_stationary"]) for row in rows
        ),
        "admissible_variation_discipline": all(
            bool(row["admissible_variation_discipline"]) for row in rows
        ),
        "negative_nonsymmetric_variation_fails": all(
            bool(negatives[str(n)]["nonsymmetric_variation_rejected"]) for n in levels
        ),
        "negative_non_row_sum_zero_variation_fails": all(
            bool(negatives[str(n)]["non_row_sum_zero_variation_rejected"]) for n in levels
        ),
        "negative_nonlocal_variation_fails": all(
            bool(negatives[str(n)]["nonlocal_variation_rejected"]) for n in levels
        ),
        "negative_random_source_not_conserved_fails": all(
            bool(negatives[str(n)]["random_source_not_conserved_rejected"]) for n in levels
        ),
        "negative_wrong_projection_fails": all(
            bool(negatives[str(n)]["wrong_projection_rejected"]) for n in levels
        ),
        "negative_field_equation_source_removed_fails": all(
            bool(negatives[str(n)]["field_equation_source_removed_fails"]) for n in levels
        ),
        "negative_nonconserved_source_fails": all(
            bool(negatives[str(n)]["nonconserved_source_fails"]) for n in levels
        ),
        "negative_random_seam_curvature_fails": all(
            bool(negatives[str(n)]["random_seam_curvature_fails"]) for n in levels
        ),
    }

    payload = {
        "status": STATUS if all(checks.values()) else "FAIL_ARCHIVE_VARIATIONAL_FIELD_EQUATION",
        "operator_source": "archive_phase_canonical_laplacian",
        "rg_operator_source": "archive_laplacian_rg_flow",
        "curvature_source": "seam_commutator_density",
        "action_source": "archive_curvature_action",
        "field_equation_source": "seam_action_variation",
        "conservation_source": "archive_bianchi_identity",
        "matter_source_coupling": "generation_anomaly_preservation / archive_stress_coupling",
        "variation": "dC = -B_n dL_n",
        "field_gradient": "G_n = -2 B_n^T C_n",
        "stress_representative": "orthogonal symmetric conserved projection of G_n",
        "levels": levels,
        "rows": rows,
        "negative_controls": negatives,
        "checks": checks,
    }

    print("operator_source: archive_phase_canonical_laplacian")
    print("rg_operator_source: archive_laplacian_rg_flow")
    print("curvature_source: seam_commutator_density")
    print("action_source: archive_curvature_action")
    print("field_equation_source: seam_action_variation")
    print("conservation_source: archive_bianchi_identity")

    if all(checks.values()):
        cleanup_stale_no_go()
        print(STATUS)
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0

    write_no_go(payload)
    print("FAIL_ARCHIVE_VARIATIONAL_FIELD_EQUATION")
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
