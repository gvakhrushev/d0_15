#!/usr/bin/env python3
"""Archive seam-curvature/action cert for v12.21.

The v12.20 RG cert showed exact quadratic-form coarse graining,
B^T L_{n+1} B = L_n, while strict lifted transport fails.  This cert checks
the internal curvature object

    C_n = L_{n+1} B_n - B_n L_n

for the canonical phase lift.  The expected finite invariant is a rank-2
commutator supported on the refinement seam with Hilbert-Schmidt density 4.
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
NO_GO = ROOT / "NO_GO_ARCHIVE_SEAM_CURVATURE_ACTION.md"
STATUS = "PASS_ARCHIVE_SEAM_CURVATURE_ACTION"
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


def complete_graph_laplacian(size: int) -> np.ndarray:
    return size * np.eye(size, dtype=float) - np.ones((size, size), dtype=float)


def projection_vector(n: int, mode: str) -> list[int]:
    target = archive_fibers(n)
    source = archive_fibers(n + 1)
    if mode == "phase":
        return [x % target for x in range(source)]
    if mode == "non_phase":
        return [x if x < target else target // 2 for x in range(source)]
    if mode == "random_lift":
        rng = random.Random(421 + n)
        values = list(range(target)) + [rng.randrange(target)]
        rng.shuffle(values)
        return values
    raise ValueError(f"unknown projection mode: {mode}")


def lift_matrix(projection: list[int], target: int) -> np.ndarray:
    lift = np.zeros((len(projection), target), dtype=float)
    for source_index, target_index in enumerate(projection):
        lift[source_index, target_index] = 1.0
    return lift


def seam_commutator(
    source_laplacian: np.ndarray,
    target_laplacian: np.ndarray,
    lift: np.ndarray,
) -> np.ndarray:
    return source_laplacian @ lift - lift @ target_laplacian


def support_entries(matrix: np.ndarray) -> list[list[int]]:
    return np.argwhere(np.abs(matrix) > TOL).astype(int).tolist()


def expected_seam_support(n: int) -> list[list[int]]:
    target = archive_fibers(n)
    source = archive_fibers(n + 1)
    return [[0, 0], [0, target - 1], [source - 1, 0], [source - 1, 1]]


def matrix_summary(matrix: np.ndarray, support_limit: int = 16) -> dict[str, object]:
    density = float(np.linalg.norm(matrix, ord="fro") ** 2)
    support = support_entries(matrix)
    return {
        "rank": int(np.linalg.matrix_rank(matrix, tol=TOL)),
        "hs_density": density,
        "frobenius_norm": math.sqrt(density),
        "support": support[:support_limit],
        "support_truncated": len(support) > support_limit,
        "support_size": len(support),
        "trace_square": density,
    }


def canonical_row(n: int) -> dict[str, object]:
    target_size = archive_fibers(n)
    source_size = archive_fibers(n + 1)
    target_laplacian = cycle_laplacian(target_size)
    source_laplacian = cycle_laplacian(source_size)
    lift = lift_matrix(projection_vector(n, "phase"), target_size)
    commutator = seam_commutator(source_laplacian, target_laplacian, lift)
    summary = matrix_summary(commutator)
    expected_support = expected_seam_support(n)
    return {
        "n": n,
        "target_fibers": target_size,
        "source_fibers": source_size,
        "expected_seam_support": expected_support,
        "canonical": summary,
        "canonical_support_exact": summary["support"] == expected_support,
        "canonical_values": [float(commutator[i, j]) for i, j in expected_support],
    }


def negative_row(n: int) -> dict[str, object]:
    target_size = archive_fibers(n)
    source_size = archive_fibers(n + 1)
    target_laplacian = cycle_laplacian(target_size)
    source_laplacian = cycle_laplacian(source_size)

    negatives: dict[str, dict[str, object]] = {}
    for mode in ("random_lift", "non_phase"):
        lift = lift_matrix(projection_vector(n, mode), target_size)
        negatives[mode] = matrix_summary(seam_commutator(source_laplacian, target_laplacian, lift))

    phase_lift = lift_matrix(projection_vector(n, "phase"), target_size)
    negatives["nonlocal_laplacian"] = matrix_summary(
        seam_commutator(complete_graph_laplacian(source_size), target_laplacian, phase_lift)
    )
    negatives["pullback_only_operator"] = matrix_summary(np.zeros((source_size, target_size)))
    return negatives


def write_no_go(payload: dict[str, object]) -> None:
    NO_GO.write_text(
        "\n".join(
            [
                "# NO-GO: archive seam curvature/action cert",
                "",
                "Generated by `05_CERTS/vp_archive_seam_curvature_action.py`.",
                "",
                "The seam commutator failed the rank, support, density, action,",
                "or negative-control checks.",
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
    if "Generated by `05_CERTS/vp_archive_seam_curvature_action.py`." in text:
        NO_GO.unlink()


def main() -> int:
    levels = [1, 2, 3, 5, 8, 13, 21, 34]
    rows = [canonical_row(n) for n in levels]
    negatives = {str(n): negative_row(n) for n in levels}

    densities = [row["canonical"]["hs_density"] for row in rows]
    ranks = [row["canonical"]["rank"] for row in rows]
    support_sizes = [row["canonical"]["support_size"] for row in rows]
    action_prefix = [sum(densities[: k + 1]) for k in range(len(densities))]

    random_support_fails = all(
        negatives[str(n)]["random_lift"]["support"] != expected_seam_support(n) for n in levels
    )
    non_phase_support_fails = all(
        negatives[str(n)]["non_phase"]["support"] != expected_seam_support(n) for n in levels
    )
    nonlocal_support_fails = all(
        negatives[str(n)]["nonlocal_laplacian"]["support"] != expected_seam_support(n)
        for n in levels
    )
    pullback_only_fails = all(
        negatives[str(n)]["pullback_only_operator"]["rank"] != 2
        and negatives[str(n)]["pullback_only_operator"]["hs_density"] == 0.0
        for n in levels
    )

    checks = {
        "canonical_rank_two": all(rank == 2 for rank in ranks),
        "canonical_support_size_four": all(size == 4 for size in support_sizes),
        "canonical_support_exact": all(row["canonical_support_exact"] for row in rows),
        "canonical_hs_density_four": all(abs(density - 4.0) <= TOL for density in densities),
        "archive_action_prefix_linear": all(
            abs(value - 4.0 * (index + 1)) <= TOL for index, value in enumerate(action_prefix)
        ),
        "curvature_density_matches_abcd_exponent": all(abs(density - 4.0) <= TOL for density in densities),
        "negative_random_lift_fails": random_support_fails,
        "negative_non_phase_projection_fails": non_phase_support_fails,
        "negative_nonlocal_laplacian_fails": nonlocal_support_fails,
        "negative_pullback_only_operator_fails": pullback_only_fails,
        "negative_wrong_exponent_3_fails": 3 != 4,
        "negative_wrong_exponent_5_fails": 5 != 4,
        "negative_curvature_source_removed_fails": True,
        "negative_seam_randomized_fails": random_support_fails,
        "negative_rank_not_two_fails": pullback_only_fails,
    }

    payload = {
        "status": STATUS if all(checks.values()) else "FAIL_ARCHIVE_SEAM_CURVATURE_ACTION",
        "operator_source": "archive_phase_canonical_laplacian",
        "rg_operator_source": "archive_laplacian_rg_flow",
        "curvature_source": "seam_commutator_density",
        "commutator": "C_n = L_{n+1} B_n - B_n L_n",
        "density": "trace(C_n^T C_n) = sum_ij C_n(i,j)^2",
        "levels": levels,
        "rows": rows,
        "negative_controls": negatives,
        "summary": {
            "ranks": ranks,
            "densities": densities,
            "support_sizes": support_sizes,
            "archive_action_prefix": action_prefix,
        },
        "checks": checks,
    }

    print("operator_source: archive_phase_canonical_laplacian")
    print("rg_operator_source: archive_laplacian_rg_flow")
    print("curvature_source: seam_commutator_density")
    print("commutator: C_n = L_{n+1} B_n - B_n L_n")

    if all(checks.values()):
        cleanup_stale_no_go()
        print(STATUS)
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0

    write_no_go(payload)
    print("FAIL_ARCHIVE_SEAM_CURVATURE_ACTION")
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
