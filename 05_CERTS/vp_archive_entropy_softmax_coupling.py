#!/usr/bin/env python3
"""Entropy-selected softmax martingale-kernel check for the archive measure."""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
from numpy.polynomial.hermite import hermgauss


ROOT = Path(__file__).resolve().parents[1]
NO_GO = ROOT / "NO_GO_ARCHIVE_HST_COUPLING.md"
DIM = 4
RADIUS = 0.2
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


def gaussian_quadrature(dim: int = DIM, order: int = 7) -> tuple[np.ndarray, np.ndarray]:
    nodes, weights = hermgauss(order)
    grids = np.meshgrid(*([nodes] * dim), indexing="ij")
    wgrids = np.meshgrid(*([weights] * dim), indexing="ij")
    y = np.stack([grid.ravel() * math.sqrt(2.0) for grid in grids], axis=1)
    w = (
        np.prod(np.stack([grid.ravel() for grid in wgrids], axis=1), axis=1)
        / (math.pi ** (dim / 2.0))
    )
    return y, w


def softmax_values(
    y: np.ndarray, p: np.ndarray, u: np.ndarray, v: np.ndarray
) -> np.ndarray:
    logits = u[None, :] + y @ v.T
    logits = logits - logits.max(axis=1, keepdims=True)
    exp_logits = np.exp(logits)
    z = np.sum(p[None, :] * exp_logits, axis=1)
    return exp_logits / z[:, None]


def moment_for_beta(
    beta: float, points: np.ndarray, p: np.ndarray, y: np.ndarray, w: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    u = np.zeros(len(points))
    v = beta * points
    f = softmax_values(y, p, u, v)
    moments = (w[:, None, None] * y[:, :, None] * f[:, None, :]).sum(axis=0).T
    return moments, f


def solve_beta(points: np.ndarray, p: np.ndarray, y: np.ndarray, w: np.ndarray) -> float:
    target = float(np.linalg.norm(points[0]))
    lo, hi = 0.0, 8.0
    for _ in range(90):
        mid = 0.5 * (lo + hi)
        moments, _f = moment_for_beta(mid, points, p, y, w)
        value = float(np.linalg.norm(moments[0]))
        if value < target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def objective(
    points: np.ndarray,
    p: np.ndarray,
    y: np.ndarray,
    w: np.ndarray,
    u: np.ndarray,
    v: np.ndarray,
) -> float:
    linear = float(np.sum(p * (u + np.sum(v * points, axis=1))))
    logits = u[None, :] + y @ v.T
    max_logits = logits.max(axis=1, keepdims=True)
    log_z = (
        max_logits[:, 0]
        + np.log(np.sum(p[None, :] * np.exp(logits - max_logits), axis=1))
    )
    return linear - float(np.sum(w * log_z))


def projected_hessian_eigenvalues(
    points: np.ndarray,
    p: np.ndarray,
    y: np.ndarray,
    w: np.ndarray,
    u: np.ndarray,
    v: np.ndarray,
) -> np.ndarray:
    atoms, dim = points.shape
    param_count = atoms * (dim + 1)
    hessian = np.zeros((param_count, param_count))
    f = softmax_values(y, p, u, v)
    q = p[None, :] * f
    for yy, ww, qq in zip(y, w, q):
        features = np.zeros((atoms, param_count))
        for atom in range(atoms):
            offset = atom * (dim + 1)
            features[atom, offset] = 1.0
            features[atom, offset + 1 : offset + 1 + dim] = yy
        mean = (qq[:, None] * features).sum(axis=0)
        second = (
            qq[:, None, None]
            * np.einsum("ia,ib->iab", features, features, optimize=True)
        ).sum(axis=0)
        hessian -= ww * (second - np.outer(mean, mean))

    constraints = np.zeros((dim + 1, param_count))
    for atom in range(atoms):
        offset = atom * (dim + 1)
        constraints[0, offset] = p[atom]
        for coord in range(dim):
            constraints[coord + 1, offset + 1 + coord] = p[atom]

    _u, singular_values, vt = np.linalg.svd(constraints)
    rank = int(np.sum(singular_values > 1.0e-12))
    basis = vt[rank:].T
    projected = basis.T @ hessian @ basis
    return np.linalg.eigvalsh(projected)


def check_softmax(require_pass: bool = True) -> tuple[bool, str]:
    points, p = archive_support_from_tower(n=6)
    y, w = gaussian_quadrature()
    beta = solve_beta(points, p, y, w)
    u = np.zeros(len(points))
    v = beta * points
    f = softmax_values(y, p, u, v)

    integral_f = np.sum(w[:, None] * f, axis=0)
    moments = (w[:, None, None] * y[:, :, None] * f[:, None, :]).sum(axis=0).T
    weighted_partition = np.sum(p[None, :] * f, axis=1)

    gauge_u = abs(float(np.sum(p * u)))
    gauge_v = float(np.max(np.abs(np.sum(p[:, None] * v, axis=0))))
    normalization_residual = max(
        float(np.max(np.abs(integral_f - 1.0))),
        float(np.max(np.abs(weighted_partition - 1.0))),
    )
    moment_residual = float(np.max(np.abs(moments - points)))
    kkt_residual = max(normalization_residual, moment_residual, gauge_u, gauge_v)

    eigs = projected_hessian_eigenvalues(points, p, y, w, u, v)
    hessian_negative = float(eigs[-1]) < -1.0e-6

    base_obj = objective(points, p, y, w, u, v)
    rng = np.random.default_rng(31415)
    concavity_ok = True
    for _ in range(24):
        du = rng.normal(size=u.shape)
        dv = rng.normal(size=v.shape)
        du -= np.sum(p * du)
        dv -= np.sum(p[:, None] * dv, axis=0)
        scale = 1.0e-3 / math.sqrt(float(np.sum(du * du) + np.sum(dv * dv)))
        du *= scale
        dv *= scale
        second_diff = (
            objective(points, p, y, w, u + du, v + dv)
            + objective(points, p, y, w, u - du, v - dv)
            - 2.0 * base_obj
        )
        concavity_ok = concavity_ok and second_diff < 0.0

    ok = (
        gauge_u < TOL
        and gauge_v < TOL
        and normalization_residual < TOL
        and moment_residual < TOL
        and kkt_residual < TOL
        and hessian_negative
        and concavity_ok
    )
    details = (
        f"d0_entropy_softmax: ok={ok} beta={beta:.12g} "
        f"gauge_u={gauge_u:.3e} gauge_v={gauge_v:.3e} "
        f"normalization={normalization_residual:.3e} "
        f"moment={moment_residual:.3e} kkt={kkt_residual:.3e} "
        f"hessian_max={eigs[-1]:.3e} concavity={concavity_ok}"
    )
    if require_pass:
        return ok, details
    return (not ok), details


def negative_without_gauge() -> tuple[bool, str]:
    points, p = archive_support_from_tower(n=6)
    y, w = gaussian_quadrature()
    beta = solve_beta(points, p, y, w)
    u = np.full(len(points), 0.1)
    v = beta * points + 0.1
    gauge_u = abs(float(np.sum(p * u)))
    gauge_v = float(np.max(np.abs(np.sum(p[:, None] * v, axis=0))))
    ok = gauge_u < TOL and gauge_v < TOL
    return (not ok), f"negative_without_gauge: ok={ok} gauge_u={gauge_u:.3e} gauge_v={gauge_v:.3e}"


def negative_wrong_dimension() -> tuple[bool, str]:
    points, _p = archive_support_from_tower(n=4)
    ok = points.shape[1] == 4
    return (not ok), f"negative_wrong_dimension: ok={ok} dim={points.shape[1]}"


def negative_without_slack() -> tuple[bool, str]:
    points, p = archive_support_from_tower(n=6, radius=1.5)
    covariance = (points * p[:, None]).T @ points
    cov_max = float(np.linalg.eigvalsh(covariance)[-1])
    ok = cov_max <= 0.25
    return (not ok), f"negative_without_slack: ok={ok} cov_max={cov_max:.6g}"


def fail(lines: list[str]) -> int:
    NO_GO.write_text(
        "# NO-GO: Archive entropy softmax coupling failed\n\n"
        + "\n".join(f"- {line}" for line in lines)
        + "\n",
        encoding="utf-8",
    )
    print("FAIL_ARCHIVE_ENTROPY_COUPLING")
    for line in lines:
        print(line)
    return 1


def main() -> int:
    checks = [
        check_softmax(require_pass=True),
        negative_without_gauge(),
        negative_wrong_dimension(),
        negative_without_slack(),
    ]
    failed = [details for ok, details in checks if not ok]
    if failed:
        return fail(failed)
    if NO_GO.exists():
        NO_GO.unlink()
    for _ok, details in checks:
        print(details)
    print("PASS_ARCHIVE_ENTROPY_COUPLING")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
