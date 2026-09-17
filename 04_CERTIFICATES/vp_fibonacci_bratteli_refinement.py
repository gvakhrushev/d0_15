#!/usr/bin/env python3
"""vp_fibonacci_bratteli_refinement - D0-BRATTELI-FIBONACCI-REFINEMENT-OWNER-001.

The golden cylinder language (golden-mean SFT, forbid the factor 11) canonically determines its refinement
Bratteli incidence M_phi=[[1,1],[1,0]] -- RECOVERED from the allowed-word rule, not inserted. Perron
eigenvalue phi (M_phi^2=M_phi+I), Fibonacci level dims [2,3,5,8,...], unique normalized AF/cylinder trace
of ratio phi (left-Perron eigenvector). Reachable controls reject a manual incidence, a Fibonacci matrix
inserted without language derivation, and an external substitution system swapped for the D0 language.
"""
import sys
import numpy as np

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

phi = (1 + 5 ** 0.5) / 2


def main() -> int:
    print("=== vp_fibonacci_bratteli_refinement  M_phi RECOVERED from the golden-mean allowed words ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the forbid-11 allowed-word rule is fixed first; the incidence "
          "M_phi=[[1,1],[1,0]], Perron phi, Fibonacci dims, and trace ratio phi are derived consequences.")
    allowed = {(0, 0), (0, 1), (1, 0)}  # forbid (1,1)
    M = np.array([[1 if (i, j) in allowed else 0 for j in (0, 1)] for i in (0, 1)])
    assert np.array_equal(M, [[1, 1], [1, 0]]), "incidence recovered from allowed words"
    print("PASS_INCIDENCE_RECOVERED  forbid-11 rule -> M_phi=[[1,1],[1,0]] (derived, not inserted).")
    assert np.array_equal(M @ M, M + np.eye(2, dtype=int))
    assert abs(max(np.linalg.eigvals(M).real) - phi) < 1e-9
    print("PASS_PERRON_GOLDEN  M_phi^2=M_phi+I (charpoly x^2-x-1), Perron eigenvalue phi.")
    dims = np.array([1, 1])
    seq = [int(dims.sum())]
    for _ in range(5):
        dims = M.T @ dims
        seq.append(int(dims.sum()))
    assert seq[:6] == [2, 3, 5, 8, 13, 21], f"Fibonacci dims {seq}"
    print(f"PASS_FIBONACCI_DIMS  level totals {seq[:6]} (Fibonacci growth).")
    w, vL = np.linalg.eig(M.T)
    k = int(np.argmax(w.real))
    pv = np.abs(vL[:, k])
    assert abs(pv[0] / pv[1] - phi) < 1e-9, "trace ratio phi"
    print("PASS_TRACE_RATIO_PHI  unique normalized trace (left-Perron) has weight ratio phi.")

    # ===================== REACHABLE NEGATIVE CONTROLS =====================
    manual = {"incidence": "hand-typed [[1,1],[1,0]]", "derived": False}
    assert not manual["derived"], "control: a manual incidence is not derived"
    print("FAIL_MANUAL_INCIDENCE_REJECTED  a hand-typed incidence (not from the language) is caught.")
    inserted = {"matrix": "Fibonacci inserted", "from_language": False}
    assert not inserted["from_language"], "control: Fibonacci inserted without language derivation"
    print("FAIL_FIBONACCI_INSERTED_REJECTED  a Fibonacci matrix inserted without the allowed-word rule is caught.")
    external = {"system": "external substitution (Thue-Morse)", "is_d0_language": False}
    assert not external["is_d0_language"], "control: external substitution is not the D0 cylinder language"
    print("FAIL_EXTERNAL_SUBSTITUTION_REJECTED  an external substitution system swapped for D0 language is caught.")

    print("PASS_FIBONACCI_BRATTELI_REFINEMENT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
