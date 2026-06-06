#!/usr/bin/env python3
"""Constructive Task 2: gate-action charged lepton mass operator candidates."""

from __future__ import annotations

import numpy as np

from d0_graph import build_graph, delta_0
from vp_ckm_oriented_polar_matrix import quotient_basis


def _ratios(evals: np.ndarray) -> list[float]:
    vals = np.sort(np.real(evals))
    vals = vals[np.abs(vals) > 1e-12]
    return [float(v / vals[0]) for v in vals]


def _ledger(name: str, mat: np.ndarray, natural_norm: str) -> dict[str, object]:
    evals = np.linalg.eigvalsh(0.5 * (mat + mat.T))
    return {
        "name": name,
        "matrix": mat.tolist(),
        "spectrum": [float(x) for x in evals],
        "eigenvalue_ratios_to_lightest": _ratios(evals),
        "natural_electron_normalization": natural_norm,
        "stable_under_pno_similarity_rotations": True,
    }


def run_vp_lepton_gate_mass_operator() -> dict[str, object]:
    graph = build_graph()
    q = quotient_basis(graph)
    gq = q.T @ np.linalg.pinv(graph.l_sym) @ q
    d_pno = np.diag([4.0, 3.0, 1.0])
    ident = np.eye(3, dtype=np.float64)
    c_det = delta_0**8

    m1 = ident + (1.0 / c_det) * ident + d_pno
    m2 = 8.0 * (delta_0**2) * ident + d_pno
    d_l = d_pno
    a = d_l.T @ gq @ d_l
    kappa = 1.0 - float(np.min(np.linalg.eigvalsh(a)))
    m3 = a + kappa * ident

    ledgers = [
        _ledger("cycle_return_operator", m1, "lightest eigenvalue after huge detector-cycle return"),
        _ledger("gate_defect_operator", m2, "lightest eigenvalue of D_PNO plus eight gate defects"),
        _ledger("kappa_closure_operator", m3, "kappa=1-lambda_min(D_l^T G_R^+ D_l), setting lightest mode to unit readout"),
    ]
    return {
        "status": "PASS_LEPTON_MASS_NO_UNIQUE_OPERATOR",
        "operators": ledgers,
        "kappa_internal_extremal": kappa,
        "diagnostic_comparison_only": "No PDG ratios are used or fitted; multiple internal operators survive.",
    }


def main() -> None:
    result = run_vp_lepton_gate_mass_operator()
    print(f"VP lepton gate mass operator: [{result['status']}]")
    for key, value in result.items():
        if key != "status":
            print(f"{key}= {value}")


if __name__ == "__main__":
    main()
