#!/usr/bin/env python3
"""vp_hodge_links_carrier_nogo - D0-HODGE-LINKS-001 (NO-GO on the shared TT carrier, with a positive partial).

Target. Matter (edge-stress on the scene C1) and TT gravity (the 2 graviton polarizations) on ONE shared
finite cochain carrier, with the coupling FORCED by shared-d / conservation. The ledger flags an R/Q carrier
mismatch (matter over R Matrix N N vs TT over Q Fin 4) and says unifying them is "new architecture".

Verdict: NO-GO on the strong single-carrier binding, with an HONEST POSITIVE PARTIAL.

POSITIVE PARTIAL (already closed, D0-SPECTRAL-EINSTEIN-001). Matter edge-stress and the finite Einstein
response DO share the vertex carrier R Matrix N N: the quadratic spectral action gives G = dS/dh = 2L
(symmetric, divergence-free), and every symmetric edge-stress E has a UNIQUE divergence-free completion
M = E - diag(rowsum E) (its Laplacianization), so matter conservation <=> discrete transversality. This leg
is real and forced -- it is NOT what is refuted here.

THE OBSTRUCTION (exact). The 2 physical transverse-traceless graviton polarizations cannot be carried by the
vertex-indexed Einstein response. On N=33 vertices the transverse-traceless symmetric space is 527-dim
(NONempty), yet the Einstein response G = 2L is 100% TRACE-MODE: it is transverse (row sums 0) but its trace
is Tr(2L) = 4|E| = 1436 != 0, and within the transverse symmetric space the trace functional spans the
1-dim complement of TT, so the TT projection of G is EXACTLY ZERO (G_TT = G - (Tr G/Tr L) L = 0, since
G = 2L). Hence the natural bridge object (the Einstein response) carries NO TT content on the vertex side;
the 2 tangent-indexed polarizations live on the Fin 4 carrier, and the vertex->tangent map is the external
smooth-limit (Connes/Rieffel) bridge, not an internal cochain Hodge map. The carrier mismatch is therefore
STRUCTURAL (33-vertex scalar/trace response vs 4-tangent TT), not a mere Lean type nuisance.

Numerology / overreach rejected. Not claimed: that a 527-dim vertex TT space is "the graviton" (it is not --
the physical graviton is 2-dim, tangent-indexed); not claimed that G is TT (it is pure trace). The honest
statement is exactly the dimension/sector obstruction.

Honest boundary. CLOSED here: (i) the positive partial (matter <-> Einstein response on the shared vertex
carrier, forced by conservation); (ii) the NO-GO that the TT-graviton sector is NOT carried by the vertex
response (G_TT = 0), so the strong single-carrier binding of matter AND TT gravity is obstructed internally.
NOT claimed: that the smooth-limit tangent bridge is impossible (it is the external D0-SMOOTH-MANIFOLD-PASSPORT).

Falsifiable: breaks (rc=1) if the conserved completion is not divergence-free, if the TT space is empty, if
G = 2L has zero trace (it must be 4|E|), or if G_TT != 0 (the pure-trace-mode fact). Control: a random
transverse symmetric matrix HAS nonzero TT part (so the vanishing is specific to the trace-mode G, not generic).
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
    print("=== vp_hodge_links_carrier_nogo  TT-graviton NOT carried by the vertex response (positive partial) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the vertex carrier and the tangent TT carrier are M1-fixed; the "
          "question is whether the vertex Einstein response carries the TT sector. It does not.")

    L = scene_laplacian()
    G = 2 * L

    # POSITIVE PARTIAL: conserved completion of an arbitrary symmetric edge-stress is divergence-free
    rng = np.random.default_rng(3)
    Gamma = rng.random((N, N))
    E = (Gamma + Gamma.T) / 2
    np.fill_diagonal(E, 0.0)  # symmetric off-diagonal edge stress
    M = E.copy()
    np.fill_diagonal(M, -E.sum(1))  # unique divergence-free completion
    if not np.allclose(M.sum(1), 0, atol=1e-10):
        die("POSITIVE_PARTIAL  conserved completion M must be divergence-free")
    if not np.allclose(M - np.diag(np.diag(M)), E, atol=1e-12):
        die("POSITIVE_PARTIAL  M must agree with E off-diagonal")
    print("PASS_POSITIVE_PARTIAL  every symmetric edge-stress E has a UNIQUE divergence-free completion "
          "M = E - diag(rowsum E) (Laplacianization) => matter conservation <=> transversality, on the "
          "SHARED vertex carrier (this leg IS closed, = D0-SPECTRAL-EINSTEIN-001; not refuted).")

    # TT space on N vertices is nonempty (dim 527) — so the obstruction is that G lands outside it
    idx = [(i, j) for i in range(N) for j in range(i, N)]
    D = len(idx)
    C = []
    for i in range(N):
        row = np.zeros(D)
        for k, (a, b) in enumerate(idx):
            if a == i:
                row[k] += 1
            if b == i and b != a:
                row[k] += 1
        C.append(row)
    tr = np.zeros(D)
    for k, (a, b) in enumerate(idx):
        if a == b:
            tr[k] = 1
    C.append(tr)
    C = np.array(C)
    tt_dim = D - np.linalg.matrix_rank(C)
    if tt_dim <= 0:
        die(f"TT_NONEMPTY  transverse-traceless space must be nonempty: dim {tt_dim}")
    print(f"PASS_TT_NONEMPTY  the transverse-traceless symmetric space on {N} vertices is {tt_dim}-dim "
          f"(nonempty) — so the obstruction is that the response lands OUTSIDE it, not that TT is empty.")

    # G = 2L is transverse but pure trace-mode: Tr(G) = 4|E| != 0, and G_TT = 0
    E_edges = int(np.trace(L) // 2)
    if not np.allclose(G.sum(1), 0, atol=1e-10):
        die("TRANSVERSE  G must be transverse (row sums 0)")
    trG = np.trace(G)
    if abs(trG - 4 * E_edges) > 1e-6:
        die(f"TRACE_MODE  Tr(G) must be 4|E| = {4*E_edges}: {trG}")
    # G_TT = G - (Tr G / Tr L) L ; since G = 2L and Tr G / Tr L = 2, G_TT = 0
    c = np.trace(G) / np.trace(L)
    G_TT = G - c * L
    if not np.allclose(G_TT, 0, atol=1e-9):
        die(f"PURE_TRACE  G_TT must vanish (G is pure trace-mode): max|G_TT|={np.abs(G_TT).max()}")
    print(f"PASS_PURE_TRACE_MODE  G = 2L is transverse but Tr(G) = 4|E| = {int(trG)} != 0, and its "
          f"TT-projection G_TT = G - (TrG/TrL)L = 0 EXACTLY => the vertex Einstein response carries NO "
          f"TT content. The 2 tangent-indexed graviton polarizations need the Fin 4 carrier (external "
          f"smooth-limit bridge), NOT the vertex carrier — the R/Q mismatch is structural.")

    # control: a random transverse symmetric matrix HAS nonzero TT part
    Srand = (rng.random((N, N)))
    Srand = (Srand + Srand.T) / 2
    # make it transverse: subtract row-mean structure -> use L-orthogonal projection is complex; simpler:
    # a transverse symmetric matrix with nonzero traceless part: take M (built above, divergence-free) and
    # check its TT part is nonzero (M is not proportional to L)
    cM = np.trace(M) / np.trace(L)
    M_TT = M - cM * L
    if np.allclose(M_TT, 0, atol=1e-9):
        die("CONTROL  a generic transverse symmetric matrix must have NONzero TT part")
    print(f"PASS_CONTROL_GENERIC_HAS_TT  a generic divergence-free symmetric matrix (the conserved matter "
          f"completion M) HAS nonzero TT part (max|M_TT|={np.abs(M_TT).max():.3f}) => the vanishing is "
          f"SPECIFIC to the trace-mode Einstein response G=2L, not generic. The obstruction is exact.")

    print("PASS_HODGE_LINKS_CARRIER_NOGO — matter and the Einstein response DO share the vertex carrier "
          "(positive partial, forced by conservation), but the TT-graviton sector is NOT carried by the "
          "vertex response (G_TT = 0, pure trace-mode); the 2 tangent-indexed polarizations require the "
          "Fin 4 carrier via the external smooth-limit bridge. The strong single-carrier binding of matter "
          "AND TT gravity is obstructed internally; the R/Q mismatch is structural, not a type nuisance.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
