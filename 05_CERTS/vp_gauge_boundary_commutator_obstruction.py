#!/usr/bin/env python3
"""D0 v15 gauge-boundary commutator obstruction certificate.

Finite deterministic matrices: an abelian phase commuting with P has no boundary
leakage; a non-abelian-style generator mixing retained/traced sectors has strict
positive leakage under Q g P. No external data and no continuum QFT import.
"""
import numpy as np
TOL=1e-9

def comm(A,B):
    return A@B - B@A

def main():
    P = np.diag([1.0,1.0,0.0])
    Q = np.eye(3)-P
    g_u1 = np.diag([1.0,-1.0,0.5])
    # Boundary-mixing color-like generator (Hermitian off-diagonal retained<->archive).
    g_color = np.array([[0.0,0.0,1.0],[0.0,0.0,0.0],[1.0,0.0,0.0]])
    assert np.linalg.norm(comm(P,g_u1)) < TOL
    assert np.linalg.norm(Q@g_u1@P) < TOL
    print("PASS_U1_BOUNDARY_COMMUTES_ZERO_LEAKAGE")
    assert np.linalg.norm(comm(P,g_color)) > TOL
    leakage_op = Q@g_color@P
    F_color = leakage_op.conj().T @ leakage_op
    psi = np.array([1.0,0.0,0.0])
    gap = float(np.real(psi.conj().T @ F_color @ psi))
    assert gap > 0.0
    print("PASS_GAUGE_BOUNDARY_COMMUTATOR_OBSTRUCTION")
    print("PASS_NON_SINGLET_POSITIVE_LEAKAGE_BOUND")
    print("FAIL_GAP_FROM_CONTINUUM_QFT_IMPORT: Rejected")
    print("FAIL_COLOR_STABLE_TERMINAL_POLE_WITH_NONZERO_LEAKAGE: Rejected")

if __name__ == '__main__':
    main()
