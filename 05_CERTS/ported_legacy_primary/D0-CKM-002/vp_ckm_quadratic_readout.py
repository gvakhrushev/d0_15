#!/usr/bin/env python3
"""Quadratic Readout Task 2: CKM amplitude/probability readout."""

from __future__ import annotations

import numpy as np

from vp_ckm_line_exchange_ordering import run_vp_ckm_line_exchange_ordering


def _hierarchy(prob: np.ndarray) -> dict[str, float]:
    offdiag = prob[np.triu_indices(3, k=1)]
    offdiag = offdiag[offdiag > 1e-15]
    return {
        "offdiag_max": float(np.max(offdiag)),
        "offdiag_min": float(np.min(offdiag)),
        "offdiag_max_over_min": float(np.max(offdiag) / np.min(offdiag)),
        "diagonal_sum": float(np.trace(prob)),
    }


def run_vp_ckm_quadratic_readout() -> dict[str, object]:
    ordering = run_vp_ckm_line_exchange_ordering()
    canonical = ordering["canonical_form"]
    form = ordering["forms"][canonical]  # type: ignore[index]
    raw = np.array(form["raw_matrix"], dtype=np.float64)  # type: ignore[index]
    u = np.array(form["polar_unitary"], dtype=np.float64)  # type: ignore[index]
    amp = np.abs(u)
    prob = amp * amp
    row_sums = prob.sum(axis=1)
    col_sums = prob.sum(axis=0)

    permutations = []
    for row_perm in ((0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0)):
        for col_perm in ((0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0)):
            p = prob[np.ix_(row_perm, col_perm)]
            permutations.append(
                {
                    "row_perm": row_perm,
                    "col_perm": col_perm,
                    "diagonal_sum": float(np.trace(p)),
                }
            )
    best_diag = max(permutations, key=lambda item: float(item["diagonal_sum"]))
    stochastic_error = float(np.sum(np.abs(row_sums - 1.0)) + np.sum(np.abs(col_sums - 1.0)))
    return {
        "status": "PASS_CKM_QUADRATIC_READOUT_MATRIX" if stochastic_error < 1e-12 and canonical == "O_G_D" else "FAIL_CKM_QUADRATIC_READOUT_MATRIX",
        "canonical_form": canonical,
        "raw_T": raw.tolist(),
        "polar_unitary_U": u.tolist(),
        "amplitude_A_abs_U": amp.tolist(),
        "probability_P_abs_U_squared": prob.tolist(),
        "row_sums_P": row_sums.tolist(),
        "col_sums_P": col_sums.tolist(),
        "double_stochastic_l1_error": stochastic_error,
        "best_diagonal_permutation_diagnostic": best_diag,
        "hierarchy": _hierarchy(prob),
        "comparison_note": "No PDG fitting. Permutations are diagnostic unless selected by D0 label bridge.",
    }


def main() -> None:
    result = run_vp_ckm_quadratic_readout()
    print(f"VP-CKM quadratic readout: [{result['status']}]")
    for key, value in result.items():
        if key != "status":
            print(f"{key}= {value}")


if __name__ == "__main__":
    main()
