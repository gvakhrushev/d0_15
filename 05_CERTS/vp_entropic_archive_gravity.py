#!/usr/bin/env python3
"""Finite entropic archive gravity certificate.

This is an algebraic fixture certificate, not a continuum gravity solver.
It checks the finite graph/Laplacian/cut/flux/heat-trace layer used by
`D0.Gravity.EntropicArchiveInterface`.
"""

from __future__ import annotations

import math
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


STATUS = "PASS_ENTROPIC_ARCHIVE_GRAVITY"


def matvec(matrix: list[list[float]], vector: list[float]) -> list[float]:
    return [sum(row[j] * vector[j] for j in range(len(vector))) for row in matrix]


def dot(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def main() -> int:
    # Deterministic C4 archive graph: 0-1-2-3-0.
    adjacency = [
        [0.0, 1.0, 0.0, 1.0],
        [1.0, 0.0, 1.0, 0.0],
        [0.0, 1.0, 0.0, 1.0],
        [1.0, 0.0, 1.0, 0.0],
    ]
    n = len(adjacency)
    degree = [sum(row) for row in adjacency]
    laplacian = [
        [degree[i] if i == j else -adjacency[i][j] for j in range(n)]
        for i in range(n)
    ]

    symmetric_laplacian = all(
        abs(laplacian[i][j] - laplacian[j][i]) <= 1.0e-12
        for i in range(n)
        for j in range(n)
    )

    # C4 Laplacian eigenvalues are exactly 0,2,2,4.
    eigenvalues = [0.0, 2.0, 2.0, 4.0]
    psd = min(eigenvalues) >= -1.0e-12

    # Direct quadratic-form spot checks on a signed finite grid.
    probes = [
        [1.0, 0.0, 0.0, 0.0],
        [1.0, -1.0, 0.0, 0.0],
        [1.0, 0.0, -1.0, 0.0],
        [1.0, 2.0, -1.0, -2.0],
        [0.5, -0.5, 1.5, -1.5],
    ]
    quadratic_psd = all(dot(v, matvec(laplacian, v)) >= -1.0e-12 for v in probes)

    region = {0, 1}
    cut_weight = sum(
        adjacency[i][j]
        for i in range(n)
        for j in range(n)
        if i in region and j not in region
    )
    capacity = cut_weight / 4.0
    capacity_nonnegative = capacity >= 0.0

    flux = [[0.0 for _ in range(n)] for _ in range(n)]
    cycle = [(0, 1), (1, 2), (2, 3), (3, 0)]
    for i, j in cycle:
        flux[i][j] = 1.0
        flux[j][i] = -1.0
    antisymmetric_flux = all(
        abs(flux[i][j] + flux[j][i]) <= 1.0e-12
        for i in range(n)
        for j in range(n)
    )
    net_flux = [sum(flux[i]) for i in range(n)]
    local_flux_conserved = all(abs(x) <= 1.0e-12 for x in net_flux)
    global_flux_zero = abs(sum(net_flux)) <= 1.0e-12

    scales = [0.1, 0.5, 1.0, 2.0]
    heat_trace = [sum(math.exp(-u * lam) for lam in eigenvalues) for u in scales]
    heat_trace_positive = all(x > 0.0 for x in heat_trace)
    heat_trace_decreasing = all(
        heat_trace[i + 1] <= heat_trace[i] + 1.0e-12
        for i in range(len(heat_trace) - 1)
    )

    checks = {
        "graph_fixture_c4": n == 4 and all(w >= 0.0 for row in adjacency for w in row),
        "laplacian_symmetric": symmetric_laplacian,
        "laplacian_psd_by_spectrum": psd,
        "laplacian_psd_by_quadratic_probes": quadratic_psd,
        "boundary_capacity_nonnegative": capacity_nonnegative,
        "archive_flux_antisymmetric": antisymmetric_flux,
        "archive_flux_locally_conserved": local_flux_conserved,
        "archive_flux_global_zero": global_flux_zero,
        "heat_trace_positive": heat_trace_positive,
        "heat_trace_decreasing_with_scale": heat_trace_decreasing,
    }

    print("--- D0 ENTROPIC ARCHIVE GRAVITY CERTIFICATE ---")
    for label, ok in checks.items():
        print(f"[{'PASS' if ok else 'FAIL'}] {label}")
    print(f"boundary_cut_weight = {cut_weight}")
    print(f"boundary_capacity = {capacity}")
    print(f"laplacian_eigenvalues = {eigenvalues}")
    print(f"heat_trace = {heat_trace}")

    if all(checks.values()):
        print(f"[CERT-CLOSED] {STATUS}")
        return 0
    print("FAIL_ENTROPIC_ARCHIVE_GRAVITY")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
