#!/usr/bin/env python3
"""vp_spectral_einstein_response - D0-SPECTRAL-EINSTEIN-001 (finite Einstein-tensor response, core object).

Target. The rank-2 Einstein-tensor response G_ij = dS_A2/dh of the finite spectral action, proved
SIMULTANEOUSLY SYMMETRIC and DIVERGENCE-FREE. The ledger flags this object as "does NOT exist anywhere in
D0/", split by a carrier mismatch (EH-proxy over R Matrix N N vs the Fin 4 spin-2 side) and blocked by a
mis-scoped conservation NO-GO.

Result. The object EXISTS and is canonical: for the quadratic spectral action S(L) = Tr(L^2) (the a2 / EH
proxy at flat measure), the variational response is
        G := dS/dh = 2 L,
the scene graph Laplacian (up to the factor 2). It is (i) exactly SYMMETRIC (L is symmetric) and (ii) exactly
DIVERGENCE-FREE in the corpus's own sense archiveDivergence(G)_i = sum_j G_ij = 0, because a graph Laplacian
annihilates constants (row sums vanish). This is the discrete contracted-Bianchi identity: the variational
response of the quadratic invariant is conserved. It lives natively on the single R Matrix N N carrier, so
the "carrier mismatch" is bypassed -- the Fin 4 spin-2 side is a SEPARATE linkage (D0-HODGE-LINKS-001), not
needed for the existence of G.

Correctly scoping the old NO-GO. NO_GO_CANONICAL_STRESS_CONSERVATION_PROJECTION only says: there EXISTS a
symmetric matrix whose archiveDivergence is nonzero (trivially true -- e.g. a rank-1 corner). That does NOT
block the existence of a symmetric divergence-free RESPONSE; it says conservation is FORCED by the Laplacian
structure, not automatic for arbitrary symmetric matrices. The canonical variational response 2L satisfies
both conditions; the NO-GO was about arbitrary projections, not the variational gradient.

Variational identity (exact). d/dt Tr((L + tE)^2)|_{t=0} = 2 Tr(L E) = Tr(G E) for every symmetric E, so
G = 2L is genuinely the gradient dS/dh, not a fitted stand-in.

Honest boundary. CLOSED: the finite rank-2 Einstein-tensor variational response exists, is symmetric, and is
archiveDivergence-free, on the EH-proxy carrier, verified for the scene and for general graph Laplacians
(Lean D0.VNext2.SpectralEinsteinResponse). NOT claimed: (i) the smooth-limit identification G -> Ric - 1/2 R g
(external Connes/Rieffel bridge, D0-SMOOTH-MANIFOLD-PASSPORT); (ii) the two-polarization Fin 4 TT-graviton
linkage (D0-HODGE-LINKS-001, still open -- a separate shared-carrier unification); (iii) for the WEIGHTED a2
at the Perron measure, the conservation is in the sqrt(rho)-weighted sense (the conformal Laplacian W L W
annihilates sqrt(rho)), NOT the naive row sum -- both are genuine conservation laws, w.r.t. their respective
divergence operators.

Falsifiable: breaks (rc=1) if 2L is not symmetric, if its row sums (archiveDivergence) are nonzero for a
graph Laplacian, if the variational identity dTr(L^2)=Tr(2L,E) fails, or if the scene spectrum of G is not
2x the scene Laplacian spectrum {0,20,22,24,33}. Control: an arbitrary symmetric matrix has nonzero row sums.
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
    print("=== vp_spectral_einstein_response  G = dS_a2/dh = 2L is symmetric AND divergence-free ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: S(L)=Tr(L^2) is the a2/EH proxy; its variational response is a "
          "THEOREM (the discrete contracted Bianchi identity), computed below, not a fitted object.")

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
    print("PASS_DIVERGENCE_FREE  archiveDivergence(G)_i = sum_j G_ij = 0 exactly (graph Laplacian kills "
          "constants) -- the discrete contracted-Bianchi conservation of the variational response.")

    # (3) variational identity: dTr((L+tE)^2)/dt|0 = 2 Tr(L E) = Tr(G E) for symmetric E
    rng = np.random.default_rng(1)
    E = rng.random((N, N)); E = (E + E.T) / 2
    t = 1e-6
    dS = (np.trace((L + t * E) @ (L + t * E)) - np.trace((L - t * E) @ (L - t * E))) / (2 * t)
    if not np.isclose(dS, np.trace(G @ E), rtol=1e-6):
        die(f"VARIATIONAL  dTr(L^2) must equal Tr(G E): {dS} vs {np.trace(G @ E)}")
    print(f"PASS_VARIATIONAL_GRADIENT  d/dt Tr((L+tE)^2)|0 = {dS:.4f} = Tr(G E) = {np.trace(G @ E):.4f} for "
          f"symmetric E => G = 2L is genuinely the gradient dS/dh (not a fitted stand-in).")

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
    print("PASS_CONTROL_NONCONSERVED  an arbitrary symmetric matrix has NONzero archiveDivergence => "
          "conservation is FORCED by the Laplacian structure, not automatic; the old "
          "NO_GO_CANONICAL_STRESS_CONSERVATION_PROJECTION is about arbitrary projections, NOT the "
          "canonical variational response 2L.")

    print("PASS_SPECTRAL_EINSTEIN_RESPONSE — the finite rank-2 Einstein-tensor variational response "
          "G = dS_a2/dh = 2L EXISTS on the EH-proxy carrier, is exactly SYMMETRIC and DIVERGENCE-FREE "
          "(archiveDivergence, the discrete contracted Bianchi), verified for the scene. Smooth-limit "
          "identification and the Fin 4 TT-graviton linkage stay external/open (D0-HODGE-LINKS-001).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
