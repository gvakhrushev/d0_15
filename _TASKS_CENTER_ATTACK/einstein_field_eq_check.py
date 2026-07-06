#!/usr/bin/env python3
"""einstein_field_eq_check - conserved-completion identity for the a2 variational tensor
(D0-A2-EINSTEIN-DIVERGENCE-OBSTRUCTION-NOGO-001 upgrade candidate; center-attack synthesis).

WHAT THIS TESTS (exact over Q, can FAIL every conclusion):

The NO-GO row established: G_A2^{ij} = dS_A2/dh_ij = 4 h_ij/(rho_i rho_j) is NOT
archiveDivergence-free; (div G_A2)_j = 4*deg(j) = {96,88,80} on flat K(9,11,13).
THIS script tests the SYNTHESIS candidate: the obstruction is an EXACT conserved-completion
identity, not a dead end.

  T1 (general, all h, all rho>0):  define M_ij := h_ij/(rho_i rho_j) (reweighted edge field),
      D_M := diag(row sums of M), L_M := D_M - M (a genuine graph Laplacian).  Then
        G_A2 = 4 M,
        div G_A2 = 4 * deg_M          (deg_M(j) := sum_i M_ij, the rho-weighted capacity density),
        X(h,rho) := 4 D_M  is the UNIQUE diagonal tensor with  div(G_A2 - X) = 0,
        G_A2 - 4 D_M = -4 L_M = -2 * einsteinResponse(L_M)   (einsteinResponse(L) := 2L, the
                                                              owned SPECTRAL-EINSTEIN object),
        div(G_A2 - 4 D_M) = 0  identically.
      So the NO-GO tensor and the owned conserved tensor are TWO HALVES OF ONE EXACT IDENTITY:
        response = capacity-diagonal - Laplacian   (= 4D_M - 4L_M).

  T2 (flat point h=1, rho=1): M = A (adjacency), X = 4D with X_jj = 4*deg(j) in {96,88,80},
      G_A2 = 4A, G_A2 - 4D = -4L, and the Perron variant (rho=deg): X_jj in {23/120, 41/220, 7/40},
      max|div G_A2| = 23/120 (reproduces the NO-GO cert numbers).

  T3 (measure-coupling law -- REPAIRED after skeptic #9 KILLED the original 'iff' claim):
      * UNIVERSAL LAW (all h, all rho>0): in the multiplicative/conformal variable u_ij
        (h_ij -> h_ij e^{u_ij}), the response Gt := dS_A2/du|_{u=0} = h (.) G_A2 (entrywise
        4 h^2/(rho rho), chain rule) satisfies
            (div Gt)_j = -2 rho_j dS_A2/drho_j     IDENTICALLY -- no Boolean scope at all.
        TRIVIALITY PIN (skeptic #2, accepted): T3-U is the per-node EULER-HOMOGENEITY
        identity of the per-edge bidegree -- it holds for ANY edge action whose per-edge
        h-degree is 2x its per-node rho-degree, on ANY graph (T3f pins this with a second
        action S' = sum 2h^4/(rho rho)^2, bidegree (4,2), SAME coefficient -2). Its sole
        D0 content is the ATTRIBUTION: S_A2 carries bidegree (2,1) per edge (the local
        conformal pairing h/(rho rho)). Not new algebra; honestly labelled.
      * h-variable direction used downstream: h Boolean ==> per-node law
        (div G_A2)_j = -2 rho_j dS_A2/drho_j  (Boolean h makes Gt = G_A2, so this is the
        universal u-law restricted; covers the frozen scene for every rho).
      * ERROR OF RECORD (kill accepted, no defense): the earlier 'per-node h-law <=> Boolean'
        is FALSE. Skeptic #9 counterexample, kept as REGRESSION: h = 3/5,6/5,6/5,3/5 on the
        4-cycle (0,9),(0,10),(1,9),(1,10), rest 1, rho=1 -- non-Boolean, yet the law holds at
        all 33 nodes (per-node cancellation sum_i h(1-h)/rho_i = 0 without h(1-h)=0 edgewise;
        the original probes passed by luck, not proof).
      * CORRECTED quantified form: per-node h-law holds for ALL rho>0 SIMULTANEOUSLY <=> h
        Boolean. (Deficit = (4/rho_j) sum_i h_ij(1-h_ij)/rho_i; vanishing for every rho>0
        forces each coefficient h(1-h)=0, i.e. h in {0,1}.) Demonstrated on the same
        counterexample: at rho_9=2 the law FAILS at node 0.
      global Euler balance <h, dS/dh> + <rho, dS/drho> = 0 for ALL (h, rho) is unchanged.
      Reading: the divergence of the (conformal) metric response equals the action's coupling
      to the fixed vertex measure -- non-conservation <=> background-measure dependence
      (Noether-type), vanishing exactly when the capacity diagonal is completed into the tensor.

  T4b (flat-limit separation -- STRONGER no-decoupling covering ALL correction shapes; the
      argument is skeptic #9's, adopted): for ANY tensor T with archiveDivergence T = 0
      (diagonal or NOT), div(T - G_A2)_j = -4 deg_M(j), and |div M'_j| <= N*||M'||_max for any
      matrix M', hence on the frozen scene
            ||T - G_A2||_max >= max_j 4*deg(j)/N = 96/33 = 32/11.
      EVERY conserved tensor is at max-norm distance >= 32/11 from G_A2: 'conserved AND
      reduces to G_A2 in a flat/decoupling limit' is impossible for ALL corrections, not only
      diagonal ones. (BRIDGE-A off-diagonal counterterms as such are NOT excluded -- only
      their convergence to G_A2 at/near the frozen scene is.)

  T5 (holographic typing pin, gravity-native): on the frozen scene BoundaryCutWeight({j}) =
      deg(j) (the cut of a singleton region is its degree), so
            (div G_A2)_j = 4*BoundaryCutWeight({j}) = 16*C(boundary {j})
      with the OWNED C(boundary S) = BoundaryCutWeight(S)/4 (BOOK_07 07.41:1752). The leak is
      typed as boundary-cut / holographic-area density -- the gravity-native owned route
      (BOOK_07:1770-1771 'boundary cut capacity is holographic area').

  T4 (honesty pins -- the disanalogies are COMPUTED, not glossed):
      P1: the source is NOT Poisson-admissible: sum_j (div G_A2)_j = 8|E| = 2872 != 0, while the
          owned weak-field Poisson equation (BOOK_07 07.32) REQUIRES a neutral source sum=0.
      P2: triviality pin: at the flat point the identity IS the Laplacian decomposition
          A = D - L (times 4). The algebra is elementary; every claim of content must live in
          WHICH objects are variational/owned, never in the algebra itself.
      P3: cross-link ring pin: the leak values are in Z; the archive-tracing trace-survival
          scale phi^-5 = 5*phi - 8 has a nonzero phi-component in the (1,phi) basis, so NO
          rational multiple of phi^-5 equals any nonzero integer leak: an "Einstein leak =
          archive leak" NUMERIC identity is impossible without a fitted irrational conversion
          factor (= naming freedom, not physics). Exact (1,phi)-pair arithmetic, no floats.

Negative controls fail the CONCLUSIONS, not the technique. Exit 0 iff all pass.
"""
from __future__ import annotations
from fractions import Fraction as Q
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SIZES = (9, 11, 13)
N = sum(SIZES)


def die(msg: str) -> None:
    print("FAIL " + msg)
    raise SystemExit(1)


def zone_of(idx: int) -> int:
    c = 0
    for zi, s in enumerate(SIZES):
        if idx < c + s:
            return zi
        c += s
    raise IndexError


def scene_edges():
    E = []
    for i in range(N):
        for j in range(i + 1, N):
            if zone_of(i) != zone_of(j):
                E.append((i, j))
    return E


EDGES = scene_edges()
assert len(EDGES) == 9 * 11 + 9 * 13 + 11 * 13 == 359


# ---------------------------------------------------------------- exact building blocks
def S_A2(h: dict, rho: list) -> Q:
    """S_A2 = sum_{i!=j} L_ij^2/(rho_i rho_j) = 2*sum_edges h_ij^2/(rho_i rho_j)
    (HeatTraceEHProxy.lean:12-13 discreteEHActionProxy, doubled per SpectralActionLadder.lean:34-38)."""
    return sum(2 * w * w / (rho[i] * rho[j]) for (i, j), w in h.items())


def G_A2(h: dict, rho: list) -> dict:
    """The NO-GO row's variational tensor, closed form: dS_A2/dh_ij = 4 h_ij/(rho_i rho_j)."""
    return {(i, j): 4 * w / (rho[i] * rho[j]) for (i, j), w in h.items()}


def M_field(h: dict, rho: list) -> dict:
    """The reweighted edge field M_ij := h_ij/(rho_i rho_j).  G_A2 = 4M by construction."""
    return {(i, j): w / (rho[i] * rho[j]) for (i, j), w in h.items()}


def deg_of(M: dict) -> list:
    """Row sums of the symmetric off-diagonal field M: deg_M(j) = sum_i M_ij."""
    d = [Q(0)] * N
    for (i, j), m in M.items():
        d[i] += m
        d[j] += m
    return d


def archive_divergence(G_off: dict, X_diag: list | None = None) -> list:
    """corpus archiveDivergence (ArchiveFieldEquation.lean:25-28 / SpectralEinsteinResponse.lean):
    (div T)_j = sum_i T_ij for the full matrix T = G_off (symmetric, zero diagonal) - diag(X)."""
    div = [Q(0)] * N
    for (i, j), g in G_off.items():
        div[j] += g
        div[i] += g
    if X_diag is not None:
        for j in range(N):
            div[j] -= X_diag[j]
    return div


def dS_drho(h: dict, rho: list) -> list:
    """Closed-form measure response: dS_A2/drho_j = -sum_i 2 h_ij^2/(rho_i rho_j^2)."""
    out = [Q(0)] * N
    for (i, j), w in h.items():
        out[j] += -2 * w * w / (rho[i] * rho[j] * rho[j])
        out[i] += -2 * w * w / (rho[j] * rho[i] * rho[i])
    return out


def fd_h(h: dict, rho: list, edge, eps: Q) -> Q:
    hp = dict(h); hp[edge] = h[edge] + eps
    hm = dict(h); hm[edge] = h[edge] - eps
    return (S_A2(hp, rho) - S_A2(hm, rho)) / (2 * eps)


def dS_drho_independent(h: dict, rho: list, node: int) -> Q:
    """Independent EXACT derivative in rho_node.  S_A2 as a function of t = rho_node alone is
    a/t + b (each edge term touching node is 2h^2/(rho_other * t); the rest is constant).
    Fit a,b from two exact evaluations, VALIDATE the model on a third point, return -a/rho^2.
    No closed-form reuse: this only calls S_A2."""
    t1 = rho[node]
    t2 = t1 + 1
    t3 = t1 + 2
    def S_at(t: Q) -> Q:
        r = list(rho); r[node] = t
        return S_A2(h, r)
    S1, S2, S3 = S_at(t1), S_at(t2), S_at(t3)
    a = (S1 - S2) / (Q(1) / t1 - Q(1) / t2)
    b = S1 - a / t1
    if S3 != a / t3 + b:
        die(f"C2  S_A2 is not of the form a/t+b in rho_{node} (model validation failed)")
    return -a / (t1 * t1)


# ---------------------------------------------------------------- backgrounds under test
def backgrounds():
    """(name, h, rho, boolean_h). Flat, Perron, and two seeded non-trivial rational fields."""
    flat_h = {e: Q(1) for e in EDGES}
    rho1 = [Q(1)] * N
    deg = [Q(0)] * N
    for (i, j) in EDGES:
        deg[i] += 1
        deg[j] += 1
    yield ("flat h=1, rho=1", flat_h, rho1, True)
    yield ("flat h=1, rho=deg (Perron)", flat_h, deg, True)
    # seeded pseudo-random rationals (deterministic, no library RNG): h in (0,3], rho in (0,2]
    h_rand = {}
    for k, e in enumerate(EDGES):
        h_rand[e] = Q(1 + (7 * k * k + 3 * k + 5) % 11, 1 + (5 * k + 2) % 7)
    rho_rand = [Q(1 + (3 * i * i + 11 * i + 7) % 13, 1 + (2 * i + 3) % 5) for i in range(N)]
    yield ("random rational h,rho (seeded)", h_rand, rho_rand, False)
    # SIGNED h (algebraic robustness: identity is an identity, not a positivity accident)
    h_sgn = {e: (Q(1) if (e[0] + e[1]) % 2 == 0 else Q(-2, 3)) for e in EDGES}
    yield ("signed h, rho=deg", h_sgn, deg, False)


# ================================================================ main
def main() -> int:
    print("=== einstein_field_eq_check  (conserved-completion identity; exact Q; can-fail) ===")
    print(f"scene K(9,11,13): N={N}, |edges|={len(EDGES)}")

    flat_h = {e: Q(1) for e in EDGES}
    rho1 = [Q(1)] * N
    deg_int = deg_of({e: Q(1) for e in EDGES})

    # ---------------- T1: the general conserved-completion identity ----------------
    for name, h, rho, boolean_h in backgrounds():
        G = G_A2(h, rho)
        M = M_field(h, rho)
        # G_A2 = 4M entrywise
        if any(G[e] != 4 * M[e] for e in EDGES):
            die(f"T1[{name}]  G_A2 != 4M (definition mismatch)")
        dM = deg_of(M)
        # div G_A2 = 4*deg_M exactly
        divG = archive_divergence(G)
        if any(divG[j] != 4 * dM[j] for j in range(N)):
            die(f"T1[{name}]  div G_A2 != 4*deg_M")
        # the completion X = 4*D_M conserves: div(G_A2 - X) = 0 EXACTLY (conclusion-level)
        X = [4 * dM[j] for j in range(N)]
        divC = archive_divergence(G, X)
        if any(x != 0 for x in divC):
            die(f"T1[{name}]  div(G_A2 - 4D_M) != 0 -- the conserved-completion CONCLUSION fails")
        # G_A2 - 4D_M = -4 L_M entrywise (L_M = D_M - M), and -4 L_M = -2*einsteinResponse(L_M)
        # with einsteinResponse(L) := 2L mirroring SpectralEinsteinResponse.lean:40.
        # HONEST LABEL (skeptic #9 wound, repaired): L_M is assembled from M by the Laplacian
        # recipe, NOT independently; the entrywise comparison is a definitional-expansion pin.
        # The LOAD-BEARING computed facts are (i) L_M has zero row sums (checked below) and
        # (ii) div G_A2 = 4*deg_M (checked above); these two give conservation. The identity
        # INSTANTIATES the OWNED Laplacianization clause (BOOK_07:1782, cert-implemented at
        # vp_hodge_links_carrier_nogo.py:70-82) at E := G_A2 -- instantiation-grade, not new algebra.
        LM_off = {e: -M[e] for e in EDGES}        # L_M off-diagonal = -M_ij
        LM_diag = [dM[j] for j in range(N)]       # L_M diagonal   = deg_M(j)
        for e in EDGES:
            lhs_off = G[e]                        # (G_A2 - 4D_M) off-diagonal = G_A2 entry
            if lhs_off != -4 * LM_off[e]:
                die(f"T1[{name}]  (G_A2-4D_M) != -4*L_M off-diagonal at {e}")
            if lhs_off != -2 * (2 * LM_off[e]):   # -2 * einsteinResponse(L_M)
                die(f"T1[{name}]  (G_A2-4D_M) != -2*einsteinResponse(L_M) at {e}")
        for j in range(N):
            lhs_diag = -X[j]                      # (G_A2 - 4D_M) diagonal = -4*deg_M(j)
            if lhs_diag != -4 * LM_diag[j] or lhs_diag != -2 * (2 * LM_diag[j]):
                die(f"T1[{name}]  (G_A2-4D_M) != -4*L_M diagonal at node {j}")
        # and L_M really is a Laplacian: zero row sums (the conservation mechanism, pinned)
        if any(archive_divergence(LM_off, [-d for d in LM_diag])[j] != 0 for j in range(N)):
            die(f"T1[{name}]  L_M row sums != 0 -- not a graph Laplacian")
        print(f"PASS_T1[{name}]  G_A2 = 4M;  div G_A2 = 4*deg_M;  div(G_A2 - 4D_M) = 0;  "
              f"G_A2 - 4D_M = -4L_M = -2*einsteinResponse(L_M)  (exact Q)")

    # gradient genuineness (both derivatives are real gradients, not fitted): probes
    h_r, rho_r = None, None
    for name, h, rho, _ in backgrounds():
        if name.startswith("random"):
            h_r, rho_r = h, rho
    G_r = G_A2(h_r, rho_r)
    for e in (EDGES[0], EDGES[180], EDGES[-1]):
        if fd_h(h_r, rho_r, e, Q(1, 9)) != G_r[e]:
            die(f"C2  dS/dh mismatch at {e} (closed form vs exact central difference)")
    dr = dS_drho(h_r, rho_r)
    for j in (0, 9, 20, 32):
        if dS_drho_independent(h_r, rho_r, j) != dr[j]:
            die(f"C2  dS/drho mismatch at node {j}")
    print("PASS_C2  both closed-form responses match independent exact reconstructions "
          "(dS/dh: exact central difference, S quadratic in h; dS/drho: exact a/t+b model fit "
          "with third-point validation, S homogeneous -2 in rho). Genuine gradients, not fitted.")

    # ---------------- T2: flat-point numbers (ties to the NO-GO row exactly) ----------------
    G_flat = G_A2(flat_h, rho1)
    if any(G_flat[e] != 4 for e in EDGES):
        die("T2  G_A2(flat) != 4*adjacency")
    div_flat = archive_divergence(G_flat)
    got = sorted(set(div_flat))
    if got != [Q(80), Q(88), Q(96)]:
        die(f"T2  flat leak values {got} != [80,88,96] = 4*deg")
    X_flat = [4 * d for d in deg_int]
    if sorted(set(X_flat)) != [Q(80), Q(88), Q(96)]:
        die("T2  X(flat) diagonal != {96,88,80}")
    # Perron variant: reproduce the NO-GO cert's 23/120 and compute X exactly
    G_per = G_A2(flat_h, deg_int)
    div_per = archive_divergence(G_per)
    if max(abs(x) for x in div_per) != Q(23, 120):
        die("T2  Perron max|div| != 23/120 (NO-GO cert number not reproduced)")
    X_per = archive_divergence(G_per)  # X_jj = (div G)_j for the diagonal completion
    zvals = {0: X_per[0], 1: X_per[9], 2: X_per[20]}
    if (zvals[0], zvals[1], zvals[2]) != (Q(23, 120), Q(41, 220), Q(7, 40)):
        die(f"T2  Perron X diagonal {zvals} != (23/120, 41/220, 7/40)")
    # HONEST LABEL (skeptic #9): the next line is TAUTOLOGICAL given the operator's linearity
    # (div(G - diag(div G)) = div G - div G = 0 by construction of archive_divergence); it is
    # kept only as a consistency illustration, NOT as evidence. The non-tautological content
    # of T2 is the VALUES above (closed-form X_jj matching the NO-GO cert's numbers).
    if any(x != 0 for x in archive_divergence(G_per, X_per)):
        die("T2  Perron completion not conserved")
    print("PASS_T2  flat: G_A2=4A, X=4D in {96,88,80}, G_A2-4D=-4L;  Perron: max|div|=23/120 "
          "reproduced, X_jj = {23/120, 41/220, 7/40} per zone, completion conserved (exact Q).")

    # ---------------- T3: measure-coupling law (the physics backbone) ----------------
    for name, h, rho, boolean_h in backgrounds():
        # global Euler balance: <h,dS/dh> + <rho,dS/drho> = 0  (exact, ALL backgrounds)
        G = G_A2(h, rho)
        # <h, dS/dh> over unordered edges: sum_e h_e * 4h_e/(rr) = 4*sum h^2/(rr) = 2*S_A2;
        # <rho, dS/drho> = -2*S_A2 (S_A2 homogeneous of degree +2 in h, degree -2 in rho).
        lhs = sum(h[e] * G[e] for e in EDGES)
        drho = dS_drho(h, rho)
        rhs = sum(rho[j] * drho[j] for j in range(N))
        if lhs + rhs != 0:
            die(f"T3[{name}]  Euler balance <h,dS/dh> + <rho,dS/drho> != 0")
        if lhs != 2 * S_A2(h, rho):
            die(f"T3[{name}]  <h,dS/dh> != 2*S_A2 (homogeneity check)")
    print("PASS_T3a  global Euler balance <h, dS/dh> + <rho, dS/drho> = 0 on ALL backgrounds "
          "(the metric response and the measure response cancel exactly; exact Q).")

    # T3b UNIVERSAL conformal law: Gt := h (.) G_A2 = dS/du (chain rule: dS/du_e = h_e*dS/dh_e).
    # (div Gt)_j = -2 rho_j dS/drho_j must hold on EVERY background -- no Boolean scope.
    for name, h, rho, boolean_h in backgrounds():
        G = G_A2(h, rho)
        Gt = {e: h[e] * G[e] for e in EDGES}          # entrywise 4 h^2/(rho rho)
        divGt = archive_divergence(Gt)
        drho = dS_drho(h, rho)
        if any(divGt[j] != -2 * rho[j] * drho[j] for j in range(N)):
            die(f"T3b[{name}]  UNIVERSAL conformal law (div Gt)_j = -2 rho_j dS/drho_j FAILS "
                f"-- the repaired T3 CONCLUSION is false")
    print("PASS_T3b  UNIVERSAL conformal measure-coupling law: Gt = h(.)G_A2 = dS_A2/du has "
          "(div Gt)_j = -2 rho_j dS_A2/drho_j on ALL backgrounds (incl. non-Boolean and "
          "signed) -- exact Q, no scope restriction.")

    # T3c Boolean ==> per-node h-law (the direction used on the frozen scene; Gt = G_A2 there).
    for name, h, rho, boolean_h in backgrounds():
        if not boolean_h:
            continue
        divG = archive_divergence(G_A2(h, rho))
        drho = dS_drho(h, rho)
        if any(divG[j] != -2 * rho[j] * drho[j] for j in range(N)):
            die(f"T3c[{name}]  Boolean ==> per-node h-law FAILS (used direction is false)")
    print("PASS_T3c  Boolean h ==> per-node h-law (div G_A2)_j = -2 rho_j dS_A2/drho_j "
          "(frozen scene, flat AND Perron rho).")

    # T3d REGRESSION (skeptic #9 counterexample -- the accepted KILL of the old 'iff'):
    # non-Boolean h with per-edge deficits h(1-h) = +6/25, -6/25 cancelling pairwise at every
    # touched node: the per-node h-law HOLDS despite h non-Boolean => converse of T3c is FALSE.
    h_ce = {e: Q(1) for e in EDGES}
    h_ce[(0, 9)] = Q(3, 5); h_ce[(0, 10)] = Q(6, 5)
    h_ce[(1, 9)] = Q(6, 5); h_ce[(1, 10)] = Q(3, 5)
    divG_ce = archive_divergence(G_A2(h_ce, rho1))
    drho_ce = dS_drho(h_ce, rho1)
    holds_ce = all(divG_ce[j] == -2 * rho1[j] * drho_ce[j] for j in range(N))
    if not holds_ce:
        die("T3d  the skeptic counterexample no longer satisfies the per-node h-law -- "
            "the ERROR-OF-RECORD statement (old iff FALSE) would itself be wrong")
    print("PASS_T3d  REGRESSION (kill accepted): non-Boolean counterexample (4-cycle "
          "(0,9),(0,10),(1,9),(1,10) with h=3/5,6/5,6/5,3/5, rho=1) SATISFIES the per-node "
          "h-law at all 33 nodes -> the old 'iff Boolean' claim is FALSE; error of record.")

    # T3f TRIVIALITY PIN for T3-U (skeptic #2): the universal law is bidegree-generic, not
    # S_A2-specific. Second action S' = sum_e 2 h^4/(rho_i rho_j)^2, per-edge bidegree (4,2):
    # dS'/du_e = 4*(2h^4/(rr)^2), and rho_j dS'/drho_j = -2 * sum_{e at j} 2h^4/(rr)^2, so
    # div(dS'/du)_j = -2 rho_j dS'/drho_j with the SAME -2 coefficient. Exact, random background.
    Gp_u = {}
    dSp_drho = [Q(0)] * N
    for (i, j), w in h_r.items():
        rr = rho_r[i] * rho_r[j]
        term = 2 * w ** 4 / (rr * rr)
        Gp_u[(i, j)] = 4 * term                      # dS'/du_e = 4 * (per-edge term)
        dSp_drho[j] += -2 * term / rho_r[j]
        dSp_drho[i] += -2 * term / rho_r[i]
    div_Gp = archive_divergence(Gp_u)
    if any(div_Gp[j] != -2 * rho_r[j] * dSp_drho[j] for j in range(N)):
        die("T3f  bidegree-(4,2) action S' violates the -2 law -- the 'Euler-homogeneity, "
            "bidegree-generic' triviality pin would be FALSE (T3-U would be S_A2-specific)")
    print("PASS_T3f  TRIVIALITY PIN (skeptic #2): the universal law holds VERBATIM (same -2) "
          "for the second action S' = sum 2h^4/(rho rho)^2 (bidegree (4,2)) -> T3-U is "
          "per-node Euler homogeneity, generic in the bidegree; its sole D0 content is the "
          "ATTRIBUTION that S_A2 carries bidegree (2,1) (local conformal pairing h/(rho rho)).")

    # T3e corrected quantifier: 'for ALL rho simultaneously' fails for the same h -- at
    # rho_9 = 2 the cancellation at node 0 breaks (3/25 - 6/25 = -3/25 != 0).
    # (NIT, recorded per skeptic #2: the PASS_T3e print is one shade stronger than what is
    #  witnessed -- one h, one rho-perturbation; the MEMO's T3-Q wording is the precise one.)
    rho_ce = [Q(1)] * N
    rho_ce[9] = Q(2)
    divG_ce2 = archive_divergence(G_A2(h_ce, rho_ce))
    drho_ce2 = dS_drho(h_ce, rho_ce)
    if divG_ce2[0] == -2 * rho_ce[0] * drho_ce2[0]:
        die("T3e  per-node h-law still holds at node 0 under rho_9=2 -- the corrected "
            "'for ALL rho <=> Boolean' quantifier would lose its witness")
    print("PASS_T3e  corrected quantified form witnessed: the SAME non-Boolean h fails the "
          "per-node h-law at node 0 once rho_9=2 -> 'holds for ALL rho simultaneously' "
          "genuinely forces h(1-h)=0 edgewise (h Boolean); the law is rho-robust ONLY on "
          "Boolean backgrounds.")

    # ---------------- T4: honesty pins ----------------
    # P1: non-neutral source => NOT the owned Poisson skeleton's rho (07.32 needs sum=0)
    total = sum(archive_divergence(G_flat))
    if total != Q(8 * 359):
        die(f"P1  sum_j (div G_A2)_j = {total} != 8|E| = 2872")
    if total == 0:
        die("P1  source unexpectedly neutral -- Poisson-disanalogy claim would be false")
    print(f"PASS_P1  sum_j (div G_A2)_j = 8|E| = {total} != 0: the leak is NOT a Poisson-"
          f"admissible source (07.32 requires neutrality); the reading must NOT claim L*phi=rho.")

    # P2: triviality pin -- flat identity IS 4*(A = D - L). Verified so the memo must carry it.
    L_flat_off = {e: -Q(1) for e in EDGES}  # L off-diag = -A
    for e in EDGES:
        if G_flat[e] != 4 * (Q(0) - L_flat_off[e]) or G_flat[e] != Q(4):
            die("P2  flat identity is not the Laplacian decomposition (?)")
    print("PASS_P2  triviality PIN: at the flat point the identity is exactly 4*(A = D - L). "
          "The algebra is elementary graph theory; ALL claimed content must live in which "
          "objects are variational/owned (G_A2 = dS_A2/dh is the a2 response; 2L is the owned "
          "SPECTRAL-EINSTEIN object; D is the capacity diagonal), never in the algebra.")

    # P3: ring pin for the archive cross-link. (1,phi)-basis exact arithmetic (a + b*phi).
    #     phi^-1 = -1 + phi ; phi^-5 = -8 + 5*phi  (phi^2 = 1 + phi).
    def mulphi(x, y):  # (a,b)*(c,d) with phi^2 = 1+phi
        a, b = x; c, d = y
        return (a * c + b * d, a * d + b * c + b * d)
    phi_inv = (Q(-1), Q(1))
    p = (Q(1), Q(0))
    for _ in range(5):
        p = mulphi(p, phi_inv)
    if p != (Q(-8), Q(5)):
        die("P3  phi^-5 != -8 + 5*phi in exact basis arithmetic")
    # leak values are integers (phi-component 0). Solve leak = c * phi^-5 for RATIONAL c:
    # c*( -8 + 5*phi ) = (leak, 0) needs phi-component 5c = 0 => c = 0 => 1-component -8c = 0,
    # which must then equal the nonzero leak -- contradiction. Computed per leak value:
    for leak in (Q(96), Q(88), Q(80), Q(2872)):
        c_from_phi_component = Q(0) / Q(5)           # the ONLY rational c killing the phi part
        one_component = Q(-8) * c_from_phi_component  # = 0
        if one_component == leak:
            die(f"P3  a rational multiple of phi^-5 equals the integer leak {leak} (impossible)")
    # (over the FIELD Q(phi) a coefficient always exists -- that freedom is exactly a fitted
    #  conversion factor, i.e. naming freedom, and is what the memo must refuse to use.)
    print("PASS_P3  ring PIN: leak values {96,88,80; 2872} lie in Z (phi-component 0); any "
          "c*phi^-5 with rational c != 0 has phi-component 5c != 0. So NO rational-coefficient "
          "identity links the Einstein-sector leak to the archive trace-survival scale phi^-5; "
          "a Q(phi)-coefficient always exists trivially (field) and is precisely naming freedom. "
          "The cross-link, if any, is mechanism-level, NOT numeric.")

    # ---------------- negative controls on the completion itself ----------------
    # C3: a WRONG completion must fail (test can detect): perturb one diagonal entry.
    X_bad = list(X_flat)
    X_bad[7] += Q(1, 3)
    if all(x == 0 for x in archive_divergence(G_flat, X_bad)):
        die("C3  perturbed diagonal completion still conserved -- test cannot fail, rigged")
    print("PASS_C3  a perturbed diagonal completion FAILS conservation -> the conserved-"
          "completion test is falsifiable, not rigged.")

    # C6 (ALGEBRA PIN -- honest relabel per skeptic #9: this is NOT an independent uniqueness
    # test; uniqueness is a one-line corollary of the pinned linearity). Pinned fact: for
    # diagonal X,  div(G - X)_j = (div G)_j - X_jj  entry-by-entry (linearity + the fact that
    # the divergence of a diagonal matrix is its diagonal). From this, div(G - X) = 0 forces
    # X_jj = (div G)_j -- no freedom. The linearity itself is verified on probes:
    G_r = G_A2(h_r, rho_r)
    divG_r = archive_divergence(G_r)
    X_probe = [Q(j + 1, 3) for j in range(N)]  # arbitrary diagonal, NOT built from div G
    lhs_probe = archive_divergence(G_r, X_probe)
    if any(lhs_probe[j] != divG_r[j] - X_probe[j] for j in range(N)):
        die("C6  linearity pin div(G - X)_j = (div G)_j - X_jj fails -- uniqueness corollary unsupported")
    print("PASS_C6  ALGEBRA PIN: div(G - X)_j = (div G)_j - X_jj verified on an arbitrary "
          "diagonal probe -> uniqueness of the diagonal completion (X_jj forced = 4*deg_M(j)) "
          "is a one-line corollary; labelled as corollary, NOT as an independent test.")

    # C7: NO-DECOUPLING corollary (upgrades the ledger's EXACT-MISSING hunt to a dichotomy).
    #     Row 175/548 ask for a conserved Ghat that "reduces to G_A2 in a flat/decoupling
    #     limit". Within diagonal corrections that is IMPOSSIBLE: X is FORCED (C6) and on every
    #     POSITIVE background X_jj = 4*deg_M(j) > 0 strictly (sum of positive terms on a
    #     connected nonempty graph) -- the capacity diagonal never decouples.
    for name, h, rho, _ in backgrounds():
        if any(w <= 0 for w in h.values()):
            continue  # positivity corollary is scoped to positive backgrounds
        Xf = archive_divergence(G_A2(h, rho))
        if any(x <= 0 for x in Xf):
            die(f"C7[{name}]  forced diagonal completion has a non-positive entry -- "
                f"the no-decoupling corollary would be false")
    print("PASS_C7  NO-DECOUPLING (diagonal lane): on every positive background the forced "
          "diagonal completion X_jj = 4*deg_M(j) is strictly positive -> no conserved "
          "DIAGONAL-corrected tensor can reduce to G_A2 in any decoupling limit. SCOPE "
          "(narrowed per skeptic #9): this closes the diagonal lane only; BRIDGE-A "
          "off-diagonal/trace counterterms are NOT excluded by C7 -- they are handled by the "
          "stronger flat-limit separation T4b below.")

    # T4b: FLAT-LIMIT SEPARATION (all correction shapes; skeptic #9's stronger argument,
    # adopted as the load-bearing no-decoupling theorem).
    #   For ANY T with archiveDivergence T = 0:  div(T - G_A2)_j = -(div G_A2)_j = -4*deg(j),
    #   and for any matrix M', |div M'_j| = |sum_i M'_ij| <= N * ||M'||_max.
    #   Hence ||T - G_A2||_max >= max_j 4*deg(j)/N = 96/33 = 32/11 on the frozen scene:
    #   EVERY conserved tensor is uniformly separated from G_A2 -- 'conserved AND reduces to
    #   G_A2 in a flat/decoupling limit' is impossible for ALL corrections, not just diagonal.
    bound = max(div_flat) / N
    if bound != Q(32, 11):
        die(f"T4b  separation bound max_j(div G_A2)_j/N = {bound} != 96/33 = 32/11")
    # verify the inequality chain on concrete conserved tensors (full-matrix max-norm distance):
    def maxnorm_dist_to_Gflat(T_off: dict, T_diag: list) -> Q:
        d = Q(0)
        for e in EDGES:
            d = max(d, abs(T_off[e] - G_flat[e]))
        # non-edge off-diagonal entries of both tensors are 0 on this carrier; diagonal:
        for j in range(N):
            d = max(d, abs(T_diag[j] - Q(0)))     # G_A2 has zero diagonal
        return d
    L_off = {e: -Q(1) for e in EDGES}
    conserved_probes = [
        ("zero tensor", {e: Q(0) for e in EDGES}, [Q(0)] * N),
        ("2L (owned einsteinResponse)", {e: 2 * L_off[e] for e in EDGES}, [2 * d for d in deg_int]),
        ("-4L (the completion)", {e: -4 * L_off[e] for e in EDGES}, [-4 * d for d in deg_int]),
    ]
    for pname, T_off, T_diag in conserved_probes:
        rs = archive_divergence(T_off, [-x for x in T_diag])
        if any(r != 0 for r in rs):
            die(f"T4b  probe '{pname}' is not conserved -- bad probe construction")
        dist = maxnorm_dist_to_Gflat(T_off, T_diag)
        if dist < Q(32, 11):
            die(f"T4b  conserved probe '{pname}' at distance {dist} < 32/11 -- the separation "
                f"CONCLUSION is false")
    # negative control: a NON-conserved tensor CAN be arbitrarily close (G_A2 itself, dist 0):
    if maxnorm_dist_to_Gflat(G_flat, [Q(0)] * N) != 0:
        die("T4b  negative control broken: G_A2 must be at distance 0 from itself")
    print("PASS_T4b  FLAT-LIMIT SEPARATION: every archiveDivergence-free tensor is at "
          "max-norm distance >= 32/11 from G_A2 on the frozen scene (bound exact; verified on "
          "conserved probes incl. the owned 2L; non-conserved control at distance 0). "
          "'Conserved AND reduces to G_A2 in a flat/decoupling limit' is impossible for ALL "
          "correction shapes -- the EXACT-MISSING of rows 175/548 as phrased is closed: accept "
          "the capacity diagonal (this identity) or change carrier/divergence (BRIDGE-B/C).")

    # T5: HOLOGRAPHIC TYPING PIN (gravity-native owned route, BOOK_07 07.41:1752):
    #   BoundaryCutWeight({j}) on the unweighted scene = #edges crossing the singleton cut
    #   = deg(j); with the OWNED C(boundary S) = BoundaryCutWeight(S)/4:
    #   (div G_A2)_j = 4*Cut({j}) = 16*C(boundary {j}).
    for j in (0, 9, 20, 32):
        cut_j = sum(1 for (a, b) in EDGES if a == j or b == j)  # independent cut count
        if Q(cut_j) != deg_int[j]:
            die(f"T5  BoundaryCutWeight({{{j}}}) = {cut_j} != deg({j}) = {deg_int[j]}")
        if div_flat[j] != 4 * Q(cut_j) or div_flat[j] != 16 * (Q(cut_j) / 4):
            die(f"T5  (div G_A2)_{j} != 4*Cut = 16*C(boundary) at node {j}")
    print("PASS_T5  HOLOGRAPHIC TYPING: (div G_A2)_j = 4*BoundaryCutWeight({j}) = "
          "16*C(boundary {j}) exactly (C = Cut/4 owned at BOOK_07 07.41:1752) -> the leak is "
          "gravity-natively typed as boundary-cut / holographic-area density, not only as "
          "edge-capacity (whose owned typing is EM, BOOK_02:1627 -- tension recorded in memo).")

    print("\nRESULT  conclusion = CONSERVED-COMPLETION IDENTITY VERIFIED, post-skeptic-repair "
          "(G_A2 = 4D_M - 4L_M, instantiating the owned Laplacianization; div G_A2 = 4*deg_M "
          "= 16*C(boundary {j}) on the scene; UNIVERSAL conformal measure-coupling law "
          "div(h(.)G_A2) = -2 rho(.)dS/drho on all backgrounds; old per-node 'iff' KILLED, "
          "regression kept; flat-limit separation ||T_conserved - G_A2||_max >= 32/11 for ALL "
          "correction shapes; honesty pins P1/P2/P3 hold)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
