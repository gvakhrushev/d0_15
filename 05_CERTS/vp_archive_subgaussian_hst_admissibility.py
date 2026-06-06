#!/usr/bin/env python3
"""Certify finite archive hypotheses used by the HST entropy interface."""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
NO_GO = ROOT / "NO_GO_ARCHIVE_HST_COUPLING.md"
TOL = 1.0e-10


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


def phi_guard(generator: float | None = None) -> bool:
    phi = (1.0 + math.sqrt(5.0)) / 2.0
    expected = phi ** -2
    value = expected if generator is None else generator
    return abs(value - expected) < 1.0e-14


def projection_guard(points: np.ndarray) -> bool:
    centered = points - points.mean(axis=0, keepdims=True)
    return np.linalg.matrix_rank(centered, tol=1.0e-12) == points.shape[1]


def mgf_bound(points: np.ndarray, weights: np.ndarray, sigma: float) -> tuple[bool, float]:
    rng = np.random.default_rng(1729)
    directions = np.eye(points.shape[1]).tolist()
    directions += (-np.eye(points.shape[1])).tolist()
    random_dirs = rng.normal(size=(64, points.shape[1]))
    random_dirs /= np.linalg.norm(random_dirs, axis=1, keepdims=True)
    directions += random_dirs.tolist()
    t_values = np.linspace(-4.0, 4.0, 17)
    max_violation = -math.inf
    for direction in directions:
        direction = np.asarray(direction)
        values = points @ direction
        for t in t_values:
            lhs = float(np.sum(weights * np.exp(t * values)))
            rhs = math.exp(0.5 * sigma * sigma * t * t)
            max_violation = max(max_violation, lhs - rhs)
    return max_violation <= 5.0e-12, max_violation


def check_case(
    name: str,
    *,
    dim: int = 4,
    radius: float = 0.2,
    sigma: float = 0.5,
    shift: float = 0.0,
    generator: float | None = None,
    require_pass: bool,
) -> tuple[bool, str]:
    n = 2 * dim - 2
    points, weights = archive_support_from_tower(n=n, radius=radius)
    if shift:
        points = points + shift

    finite_support = len(points) == 2 * dim and dim == 4
    weights_ok = bool(np.all(weights >= 0.0) and abs(weights.sum() - 1.0) < TOL)
    mean = weights @ points
    centered = float(np.max(np.abs(mean))) < TOL
    covariance = (points * weights[:, None]).T @ points
    cov_eigs = np.linalg.eigvalsh(covariance)
    covariance_slack = float(cov_eigs[-1]) <= sigma * sigma + TOL
    mgf_ok, mgf_violation = mgf_bound(points, weights, sigma)
    non_hyperplane = projection_guard(points)
    phase_ok = phi_guard(generator)

    ok = all(
        [
            finite_support,
            weights_ok,
            centered,
            covariance_slack,
            mgf_ok,
            non_hyperplane,
            phase_ok,
        ]
    )
    details = (
        f"{name}: ok={ok} finite={finite_support} weights={weights_ok} "
        f"centered={centered} cov_max={cov_eigs[-1]:.6g} "
        f"mgf_violation={mgf_violation:.3e} non_hyperplane={non_hyperplane} "
        f"phi_guard={phase_ok}"
    )
    if require_pass:
        return ok, details
    return (not ok), details


def fail(lines: list[str]) -> int:
    NO_GO.write_text(
        "# NO-GO: Archive HST admissibility failed\n\n"
        + "\n".join(f"- {line}" for line in lines)
        + "\n",
        encoding="utf-8",
    )
    print("FAIL_ARCHIVE_SUBGAUSSIAN_HST_ADMISSIBILITY")
    for line in lines:
        print(line)
    return 1


def main() -> int:
    checks: list[tuple[bool, str]] = []
    checks.append(check_case("d0_archive", require_pass=True))
    checks.append(check_case("negative_wrong_dimension_3", dim=3, require_pass=False))
    checks.append(check_case("negative_wrong_dimension_5", dim=5, require_pass=False))
    checks.append(check_case("negative_non_centered", shift=0.03, require_pass=False))
    checks.append(check_case("negative_no_slack", sigma=0.05, require_pass=False))
    checks.append(check_case("negative_non_phi_phase", generator=0.25, require_pass=False))

    failed = [details for ok, details in checks if not ok]
    if failed:
        return fail(failed)
    if NO_GO.exists():
        NO_GO.unlink()
    for _ok, details in checks:
        print(details)
    print("PASS_ARCHIVE_SUBGAUSSIAN_HST_ADMISSIBILITY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
