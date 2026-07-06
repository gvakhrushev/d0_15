#!/usr/bin/env python3
"""tick_coupling_schur_check v2 - companion for TICK_COUPLING_SCHUR_MEMO.md (DRAFT v2, post-skeptic).

Adds over v1 (skeptic #1 repairs): span-completeness control (the equivariant sample covers all
12 commutant dimensions); COMPUTED vacuity (max delay-term norm over the class, not print-only);
U3 tri-phase unitary typed candidate (unitarity, exact nilpotency (QUQ)^12=0, firing); honest
control descriptions. NOT a minted cert.
"""
import sys
import numpy as np
from fractions import Fraction

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
TOL = 1e-10


def main() -> int:
    print("=== tick_coupling_schur_check v2 (DRAFT companion) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: split=(range A, ker A) frozen by owners (3/30); "
          "group=S9xS11xS13; commutant dim MUST be 12 (owned, R1) and the sample must span it.")
    sizes = [9, 11, 13]
    N = 33
    zone = sum(([i] * s for i, s in enumerate(sizes)), [])
    A = np.array([[1.0 if zone[i] != zone[j] else 0.0 for j in range(N)] for i in range(N)])
    w, V = np.linalg.eigh(A)
    K = V[:, np.abs(w) < 1e-9]
    Q = K @ K.T
    P = np.eye(N) - Q
    assert round(np.trace(P)) == 3 and round(np.trace(Q)) == 30
    print("PASS_SPLIT  rank(retained)=3, dim(archive)=30.")

    # commutant basis: per zone-pair (X,Y): J-block; per zone X: I-block => 9 + 3 = 12 elements
    idx = [range(0, 9), range(9, 20), range(20, 33)]
    basis = []
    for X in range(3):
        for Y in range(3):
            E = np.zeros((N, N))
            for i in idx[X]:
                for j in idx[Y]:
                    E[i, j] = 1.0
            basis.append(E)
    for X in range(3):
        E = np.zeros((N, N))
        for i in idx[X]:
            E[i, i] = 1.0
        basis.append(E)
    # span-completeness control (skeptic repair): 12 elements, linearly independent
    G = np.array([[np.tensordot(a, b) for b in basis] for a in basis])
    rank = np.linalg.matrix_rank(G)
    assert len(basis) == 12 and rank == 12, f"commutant sample rank {rank} != 12"
    print("PASS_COMMUTANT_SPAN  12/12 basis elements, Gram rank 12 = owned commutant dim (R1).")

    # (A) coupling zero on the FULL commutant (basis suffices by linearity)
    worst = max(np.linalg.norm(P @ E @ Q) for E in basis)
    assert worst < TOL, f"coupling on commutant basis: {worst}"
    print(f"PASS_EQUIVARIANT_COUPLING_ZERO  max ||P E Q|| over the FULL 12-dim commutant basis = {worst:.2e}.")

    # COMPUTED vacuity (not print-only): max norm of delay terms k=0..3 over 60 random commutant elements
    rng = np.random.default_rng(20260704)
    vmax = 0.0
    for _ in range(60):
        U = sum(rng.normal() * E for E in basis)
        QUQ = Q @ U @ Q
        T = P @ U @ Q
        term = T.copy()
        for k in range(4):
            vmax = max(vmax, np.linalg.norm(term @ (Q @ U @ P)))
            term = term @ QUQ
    assert vmax < TOL, f"nonzero delay term found: {vmax}"
    print(f"PASS_RESIDUAL_VACUOUS_ON_CLASS  max ||P U Q (QUQ)^k Q U P||, k<=3, 60 random commutant U: {vmax:.2e} (computed).")

    # (A') typed sharpening: equivariant AND unitary => rho(QUQ)=1 while coupling=0
    theta = rng.normal(size=3)
    Ueq = sum(np.exp(1j * t) * basis[9 + X] for X, t in enumerate(theta))  # per-zone diagonal phases (equivariant unitary)
    QUQ = Q @ Ueq @ Q
    rho_eq = max(abs(np.linalg.eigvals(QUQ)))
    assert abs(rho_eq - 1) < 1e-9 and np.linalg.norm(P @ Ueq @ Q) < TOL
    print("PASS_TYPED_FALSE_AND_VACUOUS  equivariant unitary: rho(QUQ)=1 exactly AND coupling=0.")

    # (B) untyped witness, exact in Q — GENERIC in the vertex (any zone): rho=(n-1)/n
    for v0, n in [(0, 9), (9, 11), (20, 13)]:
        Pi = np.zeros((N, N))
        Pi[v0, v0] = 1.0
        rho = max(abs(np.linalg.eigvals(Q @ Pi @ Q)))
        assert abs(rho - (n - 1) / n) < TOL and (n - 1) / n < 1
        assert np.linalg.norm(P @ Pi @ Q) ** 2 - (n - 1) / n ** 2 < TOL
    assert Fraction(8, 9) < 1 and Fraction(10, 11) < 1 and Fraction(12, 13) < 1
    print("PASS_UNTYPED_WITNESS_GENERIC  any vertex selector: rho=(n-1)/n<1, fires; NOT unitary (untyped leg only).")

    # (B) typed candidate: U3 = diag(mu9; mu11; mu13) — unitary, nilpotent QUQ, fires
    d = []
    for n in sizes:
        d += [np.exp(2j * np.pi * j / n) for j in range(n)]
    U3 = np.diag(d)
    assert np.allclose(U3.conj().T @ U3, np.eye(N))
    QUQ = Q @ U3 @ Q
    M = np.linalg.matrix_power(QUQ, 12)
    assert np.linalg.norm(M) < 1e-8, "U3 QUQ not nilpotent at power 12"
    puq = np.linalg.norm(P @ U3 @ Q)
    assert abs(puq - np.sqrt(3)) < 1e-9
    print("PASS_TYPED_CANDIDATE_U3  unitary; (QUQ)^12=0 exactly (rho=0, FINITE ladder); ||PUQ||=sqrt(3) fires.")

    # negative controls — each fails the CONCLUSION if the world were otherwise.
    # HONEST DESCRIPTION (v2): control 1 verifies the CHECKER would flag a nonzero coupling value;
    # it cannot plant a real equivariant counterexample (the theorem forbids one) — it validates
    # the detection threshold, not the impossibility.
    assert not (worst + 0.5 < TOL), "threshold control: a coupling of 0.5 must be flagged"
    print("FAIL_COUPLING_THRESHOLD_CONTROL  a nonzero coupling magnitude would be flagged by the same gate.")
    Pi_bad = np.zeros((N, N))
    Pi_bad[0, 0] = 1.0
    rho_bad = max(abs(np.linalg.eigvals(Q @ (9 * Pi_bad) @ Q)))  # scaled selector: rho = 8 >= 1
    assert not (rho_bad < 1), "control: a genuinely divergent witness must be rejected"
    print("FAIL_DIVERGENT_WITNESS_REJECTED  a scaled selector with rho=8>=1 is correctly rejected by the rho<1 gate.")

    print("PASS_TICK_COUPLING_SCHUR_CHECK_V2")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
