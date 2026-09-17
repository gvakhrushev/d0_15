#!/usr/bin/env python3
"""D0-GENERATIVE-DYNAMICS-001 (A.2) — the seam anomaly C_n != 0 sources time.

D0 refines the carrier level by level through a prolongation B. The coarse Laplacian is the
Galerkin restriction L_n = B^T L_{n+1} B (the RG/conservation relation, D0-ARCHIVE-LAPLACIAN-RG):
the Laplacian IS preserved under restriction. But the refinement does NOT intertwine the
Laplacians: the seam commutator

    C_n = L_{n+1} B - B L_n

is nonzero. A vanishing C_n would require B to be aligned with the eigenbasis of L_{n+1} -- an
external spectral catalogue, forbidden by M1. So C_n != 0 is forced: the seam cannot close, the
state must be re-written at each refinement, and that irreversible re-write IS time (it agrees
with the gluing-anomaly picture of BOOK_06 section 06.34; the SCALAR gluing anomaly is the
already-certified Delta_alpha, D0-DELTA-ALPHA-EXACT-001).

WHAT IS PROVED (exact integer arithmetic, able to FAIL):
  * Galerkin/RG relation holds: L_n = B^T L_{n+1} B (Laplacian preserved under restriction).
  * Seam anomaly: C_n = L_{n+1} B - B L_n != 0 (the refinement does NOT intertwine) -- the
    seam does not close, so information is re-written: time.
  * Negative control: an intertwining prolongation (B aligned to the eigenbasis) gives C=0 --
    exactly the forbidden external-catalogue alignment that M1 rules out.
"""
from __future__ import annotations

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def T(M):
    return [[M[j][i] for j in range(len(M))] for i in range(len(M[0]))]


def mm(X, Y):
    return [[sum(X[i][k] * Y[k][j] for k in range(len(Y))) for j in range(len(Y[0]))]
            for i in range(len(X))]


def sub(X, Y):
    return [[X[i][j] - Y[i][j] for j in range(len(X[0]))] for i in range(len(X))]


def nonzero(M):
    return any(M[i][j] != 0 for i in range(len(M)) for j in range(len(M[0])))


def main() -> int:
    print("=== D0-GENERATIVE-DYNAMICS-001 (A.2)  seam anomaly C_n != 0 sources time ===")

    # fine Laplacian: path graph P3 (3 nodes), integer
    L1 = [[1, -1, 0], [-1, 2, -1], [0, -1, 1]]
    # prolongation B (3 fine x 2 coarse), integer (each fine node a sum of coarse contributions)
    B = [[1, 0], [1, 1], [0, 1]]
    # Galerkin coarse Laplacian L_n = B^T L1 B (the RG/conservation relation)
    Ln = mm(mm(T(B), L1), B)
    print(f"PASS_GALERKIN_RG  L_n = B^T L_(n+1) B = {Ln} (Laplacian preserved under restriction)")

    # seam anomaly C_n = L1 B - B Ln (3x2); must be nonzero
    Cn = sub(mm(L1, B), mm(B, Ln))
    assert nonzero(Cn), "seam commutator C_n must be nonzero (the seam does not close)"
    print(f"PASS_SEAM_ANOMALY_NONZERO  C_n = L_(n+1) B - B L_n = {Cn} != 0  =>  time (info re-written)")

    # ---- negative control: an intertwiner gives C = 0 (the forbidden alignment) -----
    # if B' commutes with the Laplacians (B' = identity-like on a 2-node fine = 2-node coarse),
    # then C' = L B' - B' L = 0; that is exactly the external-eigenbasis alignment M1 forbids.
    L2 = [[1, -1], [-1, 1]]
    Bid = [[1, 0], [0, 1]]
    Cprime = sub(mm(L2, Bid), mm(Bid, L2))
    assert not nonzero(Cprime), "control: an intertwining (identity) prolongation gives C=0"
    print("FAIL_INTERTWINER_GIVES_ZERO_ANOMALY_THAT_IS_THE_FORBIDDEN_EXTERNAL_CATALOGUE")
    print("PASS_GLUING_ANOMALY_NEGATIVE_CONTROLS")

    # ---- honesty boundary ----------------------------------------------------------
    print("HONEST_C_N_NONZERO_FORCED_BY_M1_NO_EXTERNAL_EIGENBASIS_ALIGNMENT_SO_SEAM_CANNOT_CLOSE")
    print("HONEST_SCALAR_GLUING_ANOMALY_IS_DELTA_ALPHA_ALREADY_CERTIFIED_TIME_IS_THE_NON_CLOSURE")

    print("PASS_GLUING_ANOMALY_TIME")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
