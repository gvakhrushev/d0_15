#!/usr/bin/env python3
"""vp_spectral_einstein_response - legacy doubled graph-Laplacian response certificate.

Truth-repaired scope (C1/A1, 2026-09-20).

This certificate checks the genuine matrix statement behind the historical
D0-SPECTRAL-EINSTEIN-001 implementation:

    S(L) = Tr(L^2),        grad_L S = 2L.

For a symmetric graph Laplacian L, the matrix 2L is symmetric and has zero row
sums. The spectrum check on K(9,11,13) is also exact up to the script's numerical
eigensolver rounding guard.

It does NOT certify that 2L is the A1 edge variational response dS_A2/dh, an
Einstein tensor, a signed-current Bianchi object, or a TT operator. The row-sum
map archiveDivergence used here is a matrix row-sum functional; C1 distinguishes
it from the oriented signed current divergence B_-.

The variational finite-difference control below differentiates with respect to
the matrix variable L along a symmetric matrix direction E:
    d/dt Tr((L+tE)^2)|_0 = Tr((2L)E).

Falsifiable: breaks (rc=1) if 2L is not symmetric, if graph-Laplacian row sums
fail to vanish, if the matrix-gradient identity fails, or if the scene spectrum
is not 2x the scene Laplacian spectrum.
"""
import sys
import numpy as np

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SIZES = [9, 11, 13]
N = sum(SIZES)


def die(msg):
    print("FAIL " + msg)
    raise SystemExit(1)


def scene_laplacian():
    zone = []
    for zi, s in enumerate(SIZES):
        zone += [zi] * s
    A = np.array([[0 if zone[u] == zone[v] else 1 for v in range(N)] for u in range(N)], float)
    return np.diag(A.sum(1)) - A


def main():
    print("=== vp_spectral_einstein_response  grad_L Tr(L^2) = 2L: symmetry + zero row sums ===")
    print("SCOPE: this cert checks the matrix gradient grad_L Tr(L^2)=2L and graph-Laplacian row-sum zero; "
          "it does not identify 2L with the A1 edge response, Einstein tensor, or signed Bianchi current.")

    L = scene_laplacian()
    G = 2 * L

    # (1) symmetric
    if not np.allclose(G, G.T, atol=1e-12):
        die("SYMMETRIC  G = 2L must be symmetric")
    print("PASS_SYMMETRIC  G = 2L is exactly symmetric (max|G - G^T| = 0).")

    # (2) archiveDivergence-free: row sums vanish (graph Laplacian annihilates constants)
    rowsums = G.sum(1)
    if not np.allclose(rowsums, 0, atol=1e-10):
        die(f"DIVERGENCE_FREE  archiveDivergence(G) (row sums) must vanish: max {np.abs(rowsums).max()}")
    print("PASS_ROW_SUM_ZERO  archiveDivergence(G)_i = sum_j G_ij = 0 exactly because the graph Laplacian kills constants.")

    # (3) variational identity: dTr((L+tE)^2)/dt|0 = 2 Tr(L E) = Tr(G E) for symmetric E
    rng = np.random.default_rng(1)
    E = rng.random((N, N)); E = (E + E.T) / 2
    t = 1e-6
    dS = (np.trace((L + t * E) @ (L + t * E)) - np.trace((L - t * E) @ (L - t * E))) / (2 * t)
    if not np.isclose(dS, np.trace(G @ E), rtol=1e-6):
        die(f"VARIATIONAL  dTr(L^2) must equal Tr(G E): {dS} vs {np.trace(G @ E)}")
    print(f"PASS_MATRIX_GRADIENT  d/dt Tr((L+tE)^2)|0 = {dS:.4f} = Tr(G E) = {np.trace(G @ E):.4f} for "
          f"symmetric E => G = 2L is the gradient with respect to the matrix variable L.")

    # (4) scene spectrum = 2 * {0,20,22,24,33}
    from collections import Counter
    ev = Counter(int(round(x)) for x in np.linalg.eigvalsh(G))
    want = {0: 1, 40: 12, 44: 10, 48: 8, 66: 2}
    if ev != want:
        die(f"SCENE_SPECTRUM  G spectrum must be 2x scene Laplacian spectrum {want}: {dict(ev)}")
    print(f"PASS_SCENE_SPECTRUM  G spectrum = 2*{{0,20,22,24,33}} = {{0:1,40:12,44:10,48:8,66:2}} "
          f"(the forced scene Laplacian spectrum, scaled).")

    # control: arbitrary symmetric matrix has nonzero archiveDivergence (correctly scopes the old NO-GO)
    Erand = rng.random((N, N)); Erand = (Erand + Erand.T) / 2
    if np.allclose(Erand.sum(1), 0, atol=1e-6):
        die("CONTROL  an arbitrary symmetric matrix must have NONzero row sums")
    print("PASS_CONTROL_NONZERO_ROWSUM  an arbitrary symmetric matrix has nonzero row sums => the zero-row-sum property is forced by graph-Laplacian structure, not symmetry alone.")

    print("PASS_SPECTRAL_EINSTEIN_RESPONSE — legacy API certificate passed: 2L is the exact "
          "matrix gradient grad_L Tr(L^2), symmetric, with zero graph-Laplacian row sums on the scene. "
          "No A1 edge-gradient, Einstein-tensor, signed-Bianchi, or TT identification is certified here.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
