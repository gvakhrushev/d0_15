#!/usr/bin/env python3
"""Quadratic Readout Task 3: CKM label/permutation bridge ledger."""

from __future__ import annotations

import numpy as np

from d0_graph import build_graph
from vp_ckm_oriented_polar_matrix import quotient_basis
from vp_ckm_quadratic_readout import run_vp_ckm_quadratic_readout


def _permute(mat: np.ndarray, order: tuple[int, int, int]) -> np.ndarray:
    return mat[np.ix_(order, order)]


def _metrics(prob: np.ndarray) -> dict[str, float]:
    offdiag = prob[np.triu_indices(3, k=1)]
    offdiag = offdiag[offdiag > 1e-15]
    return {
        "diagonal_sum": float(np.trace(prob)),
        "offdiag_max_over_min": float(np.max(offdiag) / np.min(offdiag)),
    }


def run_vp_ckm_label_permutation_bridge() -> dict[str, object]:
    graph = build_graph()
    readout = run_vp_ckm_quadratic_readout()
    amp = np.array(readout["amplitude_A_abs_U"], dtype=np.float64)
    prob = np.array(readout["probability_P_abs_U_squared"], dtype=np.float64)
    q = quotient_basis(graph)
    gq = q.T @ np.linalg.pinv(graph.l_sym) @ q
    compliance_diag = np.diag(gq)
    rules = {
        "part_size_9_11_13": tuple(np.argsort([9, 11, 13]).tolist()),
        "degree_24_22_20_desc": tuple(np.argsort([-24, -22, -20]).tolist()),
        "pno_stiffness_4_3_1_desc": tuple(np.argsort([-4, -3, -1]).tolist()),
        "runtime_compliance_diag_desc": tuple(np.argsort(-compliance_diag).tolist()),
    }
    ledgers = []
    for name, order in rules.items():
        pa = _permute(amp, order)
        pp = _permute(prob, order)
        ledgers.append(
            {
                "rule": name,
                "order": order,
                "permuted_A": pa.tolist(),
                "permuted_P": pp.tolist(),
                **_metrics(pp),
            }
        )
    best_diag = []
    for order in ((0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0)):
        pp = _permute(prob, order)
        best_diag.append({"order": order, **_metrics(pp)})
    diagnostic_best = max(best_diag, key=lambda item: float(item["diagonal_sum"]))
    return {
        "status": "PASS_CKM_LABEL_BRIDGE_LEDGER",
        "canonical_rule_ledgers": ledgers,
        "diagnostic_max_diagonal_only_not_canonical": diagnostic_best,
        "guardrail": "Do not announce physical CKM until D0 label bridge is canonical.",
    }


def main() -> None:
    result = run_vp_ckm_label_permutation_bridge()
    print(f"VP-CKM label permutation bridge: [{result['status']}]")
    for key, value in result.items():
        if key != "status":
            print(f"{key}= {value}")


if __name__ == "__main__":
    main()
