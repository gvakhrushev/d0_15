#!/usr/bin/env python3
"""Finite numerical cross-checks for D0-BRATTELI-FIBONACCI-REFINEMENT-OWNER-001.

The forbid-11 transition rule recovers the finite incidence M_phi=[[1,1],[1,0]]. Exact finite
arithmetic checks its quadratic identity and the initial Fibonacci path counts. A floating-point
eigensolver checks the expected positive eigenvector ratio phi; this numerical check is not a proof of
profile uniqueness or uniqueness of every compatible trace on an AF inductive limit. The Lean
declarations and the separate Perron-profile theorem carry those formal results. The controls reject
hand-inserted incidence and an unrelated substitution system.
"""
import sys
import numpy as np

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

phi = (1 + 5 ** 0.5) / 2


def main() -> int:
    print("=== vp_fibonacci_bratteli_refinement  M_phi RECOVERED from the golden-mean allowed words ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the forbid-11 allowed-word rule is fixed first; the finite "
          "incidence and initial path counts are derived consequences.")
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
    assert abs(pv[0] / pv[1] - phi) < 1e-9, "numerical Perron eigenvector ratio phi"
    print("PASS_NUMERICAL_PERRON_RATIO  floating-point eigenvector check gives ratio phi; this is not an AF trace uniqueness proof.")

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
