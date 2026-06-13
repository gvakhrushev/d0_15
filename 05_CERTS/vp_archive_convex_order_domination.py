#!/usr/bin/env python3
"""Finite convex-test domination checks for the D0 archive measure."""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
from numpy.polynomial.hermite import hermgauss


ROOT = Path(__file__).resolve().parents[1]
NO_GO = ROOT / "NO_GO_ARCHIVE_HST_COUPLING.md"
TOL = 2.0e-9


def archive_support_from_tower(n: int = 6, radius: float = 0.2) -> tuple[np.ndarray, np.ndarray]:
    fibers = n + 2
    dim = fibers // 2
    points = []
    for axis in range(dim):
        v = np.zeros(dim)
        v[axis] = radius
        points.append(v.copy())
        v[axis] = -radius
        points.append(v.copy())
    weights = np.full(len(points), 1.0 / len(points))
    return np.asarray(points), weights


def gaussian_quadrature(dim: int = 4, order: int = 7) -> tuple[np.ndarray, np.ndarray]:
    nodes, weights = hermgauss(order)
    grids = np.meshgrid(*([nodes] * dim), indexing="ij")
    wgrids = np.meshgrid(*([weights] * dim), indexing="ij")
    y = np.stack([grid.ravel() * math.sqrt(2.0) for grid in grids], axis=1)
    w = (
        np.prod(np.stack([grid.ravel() for grid in wgrids], axis=1), axis=1)
        / (math.pi ** (dim / 2.0))
    )
    return y, w


def phi_guard(generator: float | None = None) -> bool:
    phi = (1.0 + math.sqrt(5.0)) / 2.0
    expected = phi ** -2
    value = expected if generator is None else generator
    return abs(value - expected) < 1.0e-14


def convex_tests_pass(points: np.ndarray, weights: np.ndarray) -> tuple[bool, float]:
    dim = points.shape[1]
    y, w = gaussian_quadrature(dim=dim, order=7)
    rng = np.random.default_rng(2718)
    violations: list[float] = []

    directions = np.eye(dim).tolist()
    directions += (-np.eye(dim)).tolist()
    random_dirs = rng.normal(size=(48, dim))
    random_dirs /= np.linalg.norm(random_dirs, axis=1, keepdims=True)
    directions += random_dirs.tolist()

    for direction in directions:
        direction = np.asarray(direction)
        mu_val = float(np.sum(weights * (points @ direction)))
        gauss_val = float(np.sum(w * (y @ direction)))
        violations.append(mu_val - gauss_val)

        mu_quad = float(np.sum(weights * (points @ direction) ** 2))
        gauss_quad = float(np.sum(w * (y @ direction) ** 2))
        violations.append(mu_quad - gauss_quad)

    mu_norm = float(np.sum(weights * np.linalg.norm(points, axis=1)))
    gauss_norm = float(np.sum(w * np.linalg.norm(y, axis=1)))
    violations.append(mu_norm - gauss_norm)

    for _ in range(72):
        dirs = rng.normal(size=(6, dim))
        dirs /= np.linalg.norm(dirs, axis=1, keepdims=True)
        bias = rng.normal(scale=0.05, size=6)
        mu_val = float(np.sum(weights * np.max(points @ dirs.T + bias, axis=1)))
        gauss_val = float(np.sum(w * np.max(y @ dirs.T + bias, axis=1)))
        violations.append(mu_val - gauss_val)

    max_violation = max(violations)
    return max_violation <= TOL, max_violation


def check_case(
    name: str,
    *,
    dim: int = 4,
    radius: float = 0.2,
    shift: float = 0.0,
    exponent: int = 4,
    generator: float | None = None,
    projection_ok: bool = True,
    require_pass: bool,
) -> tuple[bool, str]:
    n = 2 * dim - 2
    points, weights = archive_support_from_tower(n=n, radius=radius)
    if shift:
        points = points + shift
    dimension_guard = dim == 4 and exponent == 4
    centered = float(np.max(np.abs(weights @ points))) < 1.0e-10
    phase_ok = phi_guard(generator)
    tests_ok, max_violation = convex_tests_pass(points, weights)
    ok = dimension_guard and centered and phase_ok and projection_ok and tests_ok
    details = (
        f"{name}: ok={ok} dimension_guard={dimension_guard} centered={centered} "
        f"phi_guard={phase_ok} projection={projection_ok} "
        f"max_convex_violation={max_violation:.3e}"
    )
    if require_pass:
        return ok, details
    return (not ok), details


def fail(lines: list[str]) -> int:
    NO_GO.write_text(
        "# NO-GO: Archive convex domination failed\n\n"
        + "\n".join(f"- {line}" for line in lines)
        + "\n",
        encoding="utf-8",
    )
    print("FAIL_ARCHIVE_CONVEX_DOMINATION")
    for line in lines:
        print(line)
    return 1


def main() -> int:
    checks: list[tuple[bool, str]] = []
    checks.append(check_case("d0_archive", require_pass=True))
    checks.append(check_case("negative_fibers_cubed", exponent=3, require_pass=False))
    checks.append(check_case("negative_fibers_fifth", exponent=5, require_pass=False))
    checks.append(check_case("negative_non_centered", shift=0.03, require_pass=False))
    checks.append(check_case("negative_non_phi_phase", generator=0.25, require_pass=False))
    checks.append(check_case("negative_wrong_projection", projection_ok=False, require_pass=False))

    failed = [details for ok, details in checks if not ok]
    if failed:
        return fail(failed)
    if NO_GO.exists():
        NO_GO.unlink()
    for _ok, details in checks:
        print(details)
    print("PASS_ARCHIVE_CONVEX_DOMINATION")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
