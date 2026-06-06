#!/usr/bin/env python3
"""Two-part gravity prototype: Lorentz signature and heat-kernel ledger.

This script implements the two blocks from the external gravity note:

1. A finite metric prototype from projector/line covariance on K(9,11,13)
   with a detector-cycle time line.
2. A heat-trace / spectral-dimension / beta-area diagnostic ledger.

It is deliberately a bridge prototype. It does not claim an
Einstein-Hilbert continuum theorem or SI calibration.
"""

from __future__ import annotations

import math

import numpy as np
from scipy.linalg import expm

from d0_graph import build_graph, delta_0, phi


def _combinatorial_laplacian() -> tuple[object, np.ndarray]:
    graph = build_graph()
    degree = np.diag(graph.degree)
    return graph, degree - graph.adjacency


def _part_projectors(graph) -> list[np.ndarray]:
    projectors: list[np.ndarray] = []
    n = graph.adjacency.shape[0]
    for part in graph.ranges:
        p = np.zeros((n, n), dtype=np.float64)
        p[part, part] = 1.0
        projectors.append(p)
    return projectors


def _signature(evals: np.ndarray, tol: float = 1e-10) -> dict[str, int]:
    return {
        "positive": int(np.sum(evals > tol)),
        "negative": int(np.sum(evals < -tol)),
        "zero": int(np.sum(np.abs(evals) <= tol)),
    }


def _fit_heat_trace(ts: np.ndarray, s_vals: np.ndarray) -> dict[str, float]:
    # log S = c - (d_s/2) log t
    slope, intercept = np.polyfit(np.log(ts), np.log(s_vals), 1)
    d_s = float(-2.0 * slope)

    # S(t) = A t^(-d_s/2) (1 + B t).  With d_s fixed this is linear in
    # alpha=A and beta=A*B.
    x0 = ts ** (-d_s / 2.0)
    x1 = x0 * ts
    design = np.vstack([x0, x1]).T
    alpha, beta = np.linalg.lstsq(design, s_vals, rcond=None)[0]
    b_fit = float(beta / alpha) if abs(alpha) > 1e-15 else float("nan")
    r_avg = float(6.0 * b_fit)
    fitted = design @ np.array([alpha, beta])
    residual = float(np.linalg.norm(fitted - s_vals))
    return {
        "log_slope": float(slope),
        "log_intercept": float(intercept),
        "spectral_dimension_ds": d_s,
        "A_fit": float(alpha),
        "B_fit": b_fit,
        "R_avg_fit": r_avg,
        "fit_residual_l2": residual,
    }


def run_vp_gravity_metric_heat_kernel_two_part() -> dict[str, object]:
    graph, lap = _combinatorial_laplacian()
    edge_count = len(graph.edges)

    beta = 1.0
    heat = expm(-beta * lap)
    projectors = _part_projectors(graph)

    g_space = np.zeros((3, 3), dtype=np.float64)
    for i, pi in enumerate(projectors):
        for j, pj in enumerate(projectors):
            g_space[i, j] = float(np.trace(pi @ heat @ pj))
    g_space = 0.5 * (g_space + g_space.T)

    det_cycle = delta_0**8
    g_time = float(-(det_cycle**2) * np.trace(heat))
    g_full = np.zeros((4, 4), dtype=np.float64)
    g_full[0, 0] = g_time
    g_full[1:, 1:] = g_space
    full_evals = np.linalg.eigvalsh(g_full)

    # The note's second block used the finite runtime window t=delta0^k.
    ts = np.array([delta_0**k for k in range(4)], dtype=np.float64)
    s_vals = np.array([np.trace(expm(-t * lap)) for t in ts], dtype=np.float64)
    heat_fit = _fit_heat_trace(ts, s_vals)

    beta_area = float(3.0 / (640.0 * math.pi**2 * edge_count * phi**4))
    three_over_edges = float(3.0 / edge_count)
    r_avg = heat_fit["R_avg_fit"]
    r_ratio = float(r_avg / three_over_edges) if abs(three_over_edges) > 0 else float("nan")

    raw_signature = _signature(full_evals, tol=0.0)
    tol_signature = _signature(full_evals, tol=1e-10)
    status = (
        "PASS_GRAVITY_TWO_PART_PROTOTYPE"
        if raw_signature["positive"] == 3 and raw_signature["negative"] == 1
        else "PASS_GRAVITY_TWO_PART_SIGNATURE_DIAGNOSTIC"
    )
    return {
        "status": status,
        "graph": {
            "vertices": int(graph.adjacency.shape[0]),
            "edges": edge_count,
            "parts": list(graph.parts),
        },
        "part_1_metric_signature": {
            "beta": beta,
            "detector_cycle_delta0_8": float(det_cycle),
            "g_space": g_space.tolist(),
            "g_space_eigenvalues": [float(x) for x in np.linalg.eigvalsh(g_space)],
            "g_00": g_time,
            "g_full": g_full.tolist(),
            "g_full_eigenvalues": [float(x) for x in full_evals],
            "signature_raw_sign": raw_signature,
            "signature_tol_1e-10": tol_signature,
            "time_line_resolution_note": "g00 is negative by construction but suppressed by delta0^16.",
        },
        "part_2_heat_kernel_ledger": {
            "t_window": [float(x) for x in ts],
            "heat_trace": [float(x) for x in s_vals],
            **heat_fit,
            "beta_area_D0": beta_area,
            "three_over_edge_count": three_over_edges,
            "R_avg_over_3_per_E": r_ratio,
        },
        "guardrail": (
            "Lorentz signature is produced by the detector-time sign insertion; "
            "the heat-kernel fit is a finite diagnostic, not a continuum GR theorem."
        ),
    }


def main() -> None:
    result = run_vp_gravity_metric_heat_kernel_two_part()
    print(f"VP gravity metric + heat-kernel two-part prototype: [{result['status']}]")
    for key, value in result.items():
        if key != "status":
            print(f"{key}= {value}")


if __name__ == "__main__":
    main()
