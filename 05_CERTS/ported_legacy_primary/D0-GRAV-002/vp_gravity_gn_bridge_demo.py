#!/usr/bin/env python3
"""Gravity bridge demo from D0 beta_area to an SI G-scale.

This script executes the proposed bridge prototype literally enough to audit it,
while making two details explicit:

1. h = 2*pi*hbar is required for the non-reduced Compton wavelength.
2. The final G_runtime expression is a dimensional bridge diagnostic, not a
   closed SI prediction, because beta_area is dimensionless in the finite graph
   certificate and the l_star/ell_0 map is still open.
"""

from __future__ import annotations

import math

import numpy as np
from scipy.linalg import expm

from d0_graph import build_graph, delta_0, phi


def _projectors(graph) -> list[np.ndarray]:
    projectors: list[np.ndarray] = []
    n = graph.adjacency.shape[0]
    for part in graph.ranges:
        p = np.zeros((n, n), dtype=np.float64)
        p[part, part] = 1.0
        projectors.append(p)
    return projectors


def run_vp_gravity_gn_bridge_demo() -> dict[str, object]:
    graph = build_graph()
    num_edges = len(graph.edges)
    degree = np.diag(graph.degree)
    lap = degree - graph.adjacency

    alpha_top_inv = num_edges / (phi**2) - phi ** (-5)
    c_e = 1.0 / 38.0
    v_h = delta_0 / math.sqrt(39.0)
    d_e = math.sqrt(1.0 + delta_0 / 3.0)
    beta_area = 3.0 / (640.0 * math.pi**2 * num_edges * phi**4)

    heat = expm(-lap)
    g_space = np.zeros((3, 3), dtype=np.float64)
    for i, pi in enumerate(_projectors(graph)):
        for j, pj in enumerate(_projectors(graph)):
            g_space[i, j] = float(np.trace(pi @ heat @ pj))
    g_space = 0.5 * (g_space + g_space.T)

    det_cycle = delta_0**8
    g_time = float(-(det_cycle**2) * np.trace(heat))
    g_full = np.zeros((4, 4), dtype=np.float64)
    g_full[0, 0] = g_time
    g_full[1:, 1:] = g_space
    g_evals = np.linalg.eigvalsh(g_full)

    ts = np.array([delta_0**k for k in range(4)], dtype=np.float64)
    heat_trace = np.array([np.trace(expm(-t * lap)) for t in ts], dtype=np.float64)
    slope, intercept = np.polyfit(np.log(ts), np.log(heat_trace), 1)
    d_s = float(-2.0 * slope)

    x0 = ts ** (-d_s / 2.0)
    x1 = x0 * ts
    design = np.vstack([x0, x1]).T
    a_fit, ab_fit = np.linalg.lstsq(design, heat_trace, rcond=None)[0]
    b_fit = float(ab_fit / a_fit)
    r_avg = 6.0 * b_fit

    # SI bridge inputs from the prompt.
    hbar = 1.054571817e-34
    h = 2.0 * math.pi * hbar
    c = 2.99792458e8
    m_e = 9.10938356e-31
    g_newton = 6.67430e-11

    lambda_e_nonreduced = h / (m_e * c)
    lambda_e_reduced = hbar / (m_e * c)
    ell_0_nonreduced = c_e * lambda_e_nonreduced
    ell_0_reduced = c_e * lambda_e_reduced

    def estimate(ell_0: float) -> dict[str, float]:
        l_star = ell_0
        rho_edges = num_edges / (33.0 * l_star**4)
        g_runtime = 1.0 / (16.0 * math.pi * beta_area * rho_edges)
        return {
            "ell_0_m": float(ell_0),
            "rho_edges_m_minus_4": float(rho_edges),
            "G_runtime_bridge_number": float(g_runtime),
            "ratio_to_G_N": float(g_runtime / g_newton),
            "G_N_over_bridge": float(g_newton / g_runtime),
        }

    return {
        "status": "PASS_GRAVITY_GN_BRIDGE_DEMO_DIAGNOSTIC",
        "d0_inputs": {
            "phi": phi,
            "delta0": delta_0,
            "alpha_top_inv": float(alpha_top_inv),
            "D_e": d_e,
            "C_e": c_e,
            "v_H": v_h,
            "beta_area": beta_area,
            "edges": num_edges,
        },
        "metric_block": {
            "g_space": g_space.tolist(),
            "g_00": g_time,
            "g_full_eigenvalues": [float(x) for x in g_evals],
            "signature_raw": {
                "positive": int(np.sum(g_evals > 0.0)),
                "negative": int(np.sum(g_evals < 0.0)),
                "zero": int(np.sum(g_evals == 0.0)),
            },
            "signature_tol_1e-10": {
                "positive": int(np.sum(g_evals > 1e-10)),
                "negative": int(np.sum(g_evals < -1e-10)),
                "zero": int(np.sum(np.abs(g_evals) <= 1e-10)),
            },
        },
        "heat_kernel_block": {
            "t_window": [float(x) for x in ts],
            "heat_trace": [float(x) for x in heat_trace],
            "spectral_dimension_ds": d_s,
            "log_intercept": float(intercept),
            "A_fit": float(a_fit),
            "B_fit": b_fit,
            "R_avg_fit": float(r_avg),
        },
        "si_bridge_inputs": {
            "hbar_J_s": hbar,
            "h_J_s": h,
            "c_m_s": c,
            "m_e_kg": m_e,
            "G_N_reference": g_newton,
            "lambda_e_nonreduced_m": float(lambda_e_nonreduced),
            "lambda_e_reduced_m": float(lambda_e_reduced),
        },
        "G_bridge_estimates": {
            "using_nonreduced_Compton": estimate(ell_0_nonreduced),
            "using_reduced_Compton_diagnostic": estimate(ell_0_reduced),
        },
        "guardrail": (
            "The G_runtime number is not a closed SI prediction: the dimensional "
            "map between finite beta_area and continuum edge density is still open."
        ),
    }


def main() -> None:
    result = run_vp_gravity_gn_bridge_demo()
    print(f"VP gravity GN bridge demo: [{result['status']}]")
    for key, value in result.items():
        if key != "status":
            print(f"{key}= {value}")


if __name__ == "__main__":
    main()
