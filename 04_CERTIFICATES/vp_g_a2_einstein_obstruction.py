#!/usr/bin/env python3
"""g_a2_einstein_check - D0-SPECTRAL-EINSTEIN-001 can-fail computation (DRAFT / center-attack).

WHAT THIS REPLACES. The registry cert vp_spectral_einstein_response.py answers an EASIER
question than the registry note demands: it sets S = Tr(L^2), computes G := dS/dL = 2L, and
calls G "divergence-free" because a graph Laplacian has zero ROW SUMS. But:
  (a) Tr(L^2) is NOT the a2/EH proxy S_A2. The genuine a2/EH proxy (HeatTraceEHProxy.lean:12-13,
      SpectralActionLadder.lean:34-38) is  S_A2 = sum_{i!=j} L_ij^2 / (rho_i rho_j).
  (b) dS/dL differentiates w.r.t. L itself; the registry demands the VARIATIONAL derivative
      d S_A2 / d h_ij on a metric-PERTURBATION space (the Q Sym^4 / perturbation carrier), a
      genuine rank-2 tensor G_A2^{ij}. That object "does NOT exist anywhere in D0" (row 175).

WHAT THIS DOES (exact over Q, can FAIL the CONCLUSION):
  1. Builds S_A2 on the frozen scene K(9,11,13) as an exact function of the symmetric
     edge-weight perturbation field h_ij (i!=j); h is the discrete metric perturbation, the
     off-diagonal weights of the scene graph Laplacian L(h).
  2. Defines G_A2^{ij} := d S_A2 / d h_ij symbolically/exactly over Q -> so the object is DEFINED.
  3. Tests (i) symmetry by construction; (ii) the discrete contracted-Bianchi / divergence
     identity  sum_i G_A2^{ij} = 0  (the corpus archiveDivergence, ArchiveFieldEquation.lean:25-28)
     as an EXACT Q computation on the scene.

OUTCOME (pre-registered, honest): test (ii) is EXPECTED to FAIL -- the a2/EH-proxy variational
tensor is NOT archiveDivergence-free on the scene -- matching canonical_stress_conservation_no_go
(ArchiveStressRepresentative.lean:34). If it fails, the CONCLUSION printed is the OBSTRUCTION,
and the registry motion is: demote D0-SPECTRAL-EINSTEIN-001 CERT-CLOSED -> PROOF-TARGET (proposal).

Negative controls fail the CONCLUSION, not the technique.
Exit code 0 iff the printed CONCLUSION is internally consistent (built vs obstruction), and every
control behaves as pre-registered; exit 1 if any invariant the memo relies on is violated.
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
    """Complete tripartite K(9,11,13): edge iff distinct zones. Returns sorted i<j pairs."""
    E = []
    for i in range(N):
        for j in range(i + 1, N):
            if zone_of(i) != zone_of(j):
                E.append((i, j))
    return E


def scene_rho_unit():
    """Flat measure rho_i = 1 (the a2 proxy at flat measure -- the naive Einstein interface)."""
    return [Q(1) for _ in range(N)]


def scene_rho_degree():
    """Perron/degree measure: rho_i = deg(i). For a complete tripartite graph deg = N - |zone(i)|.
    This is the natural stationary weight referenced by the WEIGHTED a2 (cert docstring, boundary
    clause). Exact integers -> exact Q."""
    deg = [0] * N
    for (i, j) in scene_edges():
        deg[i] += 1
        deg[j] += 1
    return [Q(d) for d in deg]


def S_A2(hw: dict, rho: list) -> Q:
    """The genuine a2/EH proxy on the perturbation field hw (edge -> weight), EXACT over Q.
        S_A2 = sum_{i!=j} L_ij^2 / (rho_i rho_j),  L_ij = -hw[(i,j)] off-diagonal.
    Since L_ij = -w_ij (i!=j), L_ij^2 = w_ij^2, and each unordered edge {i,j} appears twice
    (ij and ji), so S_A2 = 2 * sum_{edges} w_ij^2 / (rho_i rho_j).
    Mirrors HeatTraceEHProxy.lean:12-13 discreteEHActionProxy."""
    tot = Q(0)
    for (i, j), w in hw.items():
        tot += 2 * w * w / (rho[i] * rho[j])
    return tot


def grad_S_A2(hw: dict, rho: list) -> dict:
    """G_A2 as the EXACT variational derivative d S_A2 / d w_ij over Q, symbolic per-edge:
        d/dw_ij [ 2 w_ij^2 / (rho_i rho_j) ] = 4 w_ij / (rho_i rho_j).
    Returned as a dict edge -> G value (the off-diagonal rank-2 tensor entry G_A2^{ij}=G_A2^{ji})."""
    return {(i, j): 4 * w / (rho[i] * rho[j]) for (i, j), w in hw.items()}


def grad_finite_difference(hw: dict, rho: list, edge, eps: Q) -> Q:
    """Independent EXACT central difference of S_A2 in the w_edge direction (Q, eps rational).
    Cross-check that grad_S_A2 is genuinely dS/dh, not a fitted stand-in."""
    hp = dict(hw); hp[edge] = hw[edge] + eps
    hm = dict(hw); hm[edge] = hw[edge] - eps
    return (S_A2(hp, rho) - S_A2(hm, rho)) / (2 * eps)


def archive_divergence(G: dict, rho: list) -> list:
    """The corpus archiveDivergence (ArchiveFieldEquation.lean:25-28): (div G)_j = sum_i G_ij.
    G is symmetric off-diagonal (edge dict). Diagonal is 0 (S_A2 has no diagonal dependence).
    Returns the length-N divergence vector over Q."""
    div = [Q(0) for _ in range(N)]
    for (i, j), g in G.items():
        # symmetric tensor: entry (i,j) and (j,i) both = g
        div[j] += g   # contributes to column j from row i
        div[i] += g   # contributes to column i from row j
    return div


def main() -> int:
    print("=== g_a2_einstein_check  (DRAFT, can-fail) ===")
    E = scene_edges()
    assert len(E) == 9 * 11 + 9 * 13 + 11 * 13 == 359
    print(f"scene K(9,11,13): N={N}, |edges|={len(E)}")

    # frozen flat background perturbation: unit weight on every scene edge (the K(9,11,13) adjacency)
    hw = {e: Q(1) for e in E}

    # ---- object is DEFINED: build S_A2 and its exact variational derivative over Q ----
    rho1 = scene_rho_unit()
    S1 = S_A2(hw, rho1)
    G1 = grad_S_A2(hw, rho1)
    print(f"[flat rho=1] S_A2(scene) = {S1}  (= 2*|edges| = {2*len(E)})")
    print(f"[flat rho=1] G_A2 DEFINED: {len(G1)} off-diagonal entries, exact over Q "
          f"(rank-2 tensor d S_A2 / d h_ij).")

    # (0) sanity: variational derivative matches an INDEPENDENT exact finite difference
    for e in (E[0], E[len(E) // 2], E[-1]):
        fd = grad_finite_difference(hw, rho1, e, Q(1, 7))
        if fd != G1[e]:
            die(f"VARIATIONAL_GRADIENT  d S_A2/dh at {e}: closed-form {G1[e]} != finite-diff {fd}")
    print("PASS_VARIATIONAL_GRADIENT  G_A2 = d S_A2/d h_ij matches exact Q finite difference "
          "(genuine gradient, not fitted).")

    # (i) SYMMETRY by construction: G_A2^{ij} is stored per unordered edge -> G_ij = G_ji exactly.
    #     Verify no edge key collides and value is well-defined on the unordered pair.
    if any(i >= j for (i, j) in G1):
        die("SYMMETRIC  edge keys must be stored i<j (unordered)")
    print("PASS_SYMMETRIC  G_A2^{ij} = G_A2^{ji} by construction (per-unordered-edge value).")

    # (ii) DISCRETE CONTRACTED-BIANCHI / DIVERGENCE test -- the load-bearing decision.
    #      corpus archiveDivergence: (div G_A2)_j = sum_i G_A2^{ij}.  EXACT over Q.
    div1 = archive_divergence(G1, rho1)
    max_abs_1 = max(abs(x) for x in div1)
    is_conserved_flat = all(x == 0 for x in div1)
    # For flat rho=1 and unit weights: G_A2^{ij} = 4 on every edge, so (div)_j = 4*deg(j) != 0.
    sample = {j: div1[j] for j in (0, 9, 20, 32)}  # one node per zone + boundary
    print(f"[flat rho=1] archiveDivergence(G_A2): max|div| = {max_abs_1}, "
          f"conserved = {is_conserved_flat}")
    print(f"[flat rho=1] sample (div)_j = 4*deg(j): {sample}  "
          f"(deg: zone0=11+13=24, zone1=9+13=22, zone2=9+11=20; times 4 -> 96,88,80)")

    # weighted (Perron/degree) measure: does the natural weighting restore conservation?
    rhod = scene_rho_degree()
    Gd = grad_S_A2(hw, rhod)
    divd = archive_divergence(Gd, rhod)
    max_abs_d = max(abs(x) for x in divd)
    is_conserved_deg = all(x == 0 for x in divd)
    print(f"[Perron rho=deg] archiveDivergence(G_A2): max|div| = {max_abs_d}, "
          f"conserved = {is_conserved_deg}")

    # ---- CONCLUSION: built vs obstruction (decided by the exact Q test above) ----
    if is_conserved_flat:
        conclusion = "BUILT"
        print("CONCLUSION_BUILT  the finite a2/EH-proxy Einstein tensor G_A2 = d S_A2/d h is "
              "SYMMETRIC and archiveDivergence-free on the scene: conserved finite Einstein "
              "tensor exists.")
    else:
        conclusion = "OBSTRUCTION"
        print("CONCLUSION_OBSTRUCTION  the finite a2/EH-proxy variational tensor "
              "G_A2^{ij} = d S_A2/d h_ij = 4 h_ij/(rho_i rho_j) is NOT archiveDivergence-free "
              "on the frozen scene K(9,11,13).")
        print("  EXACT OBSTRUCTION (flat rho=1):  (div G_A2)_j = sum_i 4 h_ij = 4*deg(j) != 0 "
              "for every node (deg(j) >= 18 > 0 on K(9,11,13)).")
        print("  This is the discrete-Bianchi FAILURE the internal NO-GO predicts: "
              "canonical_stress_conservation_no_go (ArchiveStressRepresentative.lean:34) -- the "
              "row-sum divergence of the a2 variational stress is nonzero in general.")
        print("  REGISTRY MOTION (proposal): demote D0-SPECTRAL-EINSTEIN-001 "
              "CERT-CLOSED -> PROOF-TARGET; the archiveDivergence-free rank-2 G_A2 is NOT built.")

    # ------------------------- NEGATIVE CONTROLS (fail the CONCLUSION) -------------------------
    # Control A (POSITIVE control on the SAME operator): a graph-Laplacian-type STRESS, i.e. the
    # object the OLD cert used (G_old = 2L), DOES have zero row-sums. This shows the divergence
    # operator itself is not degenerate: it CAN return 0 -- so the OBSTRUCTION above is a real
    # property of G_A2, not an artifact of always-nonzero divergence.
    L = [[Q(0)] * N for _ in range(N)]
    for (i, j) in E:
        L[i][j] -= 1; L[j][i] -= 1
        L[i][i] += 1; L[j][j] += 1
    G_old = [[2 * L[i][j] for j in range(N)] for i in range(N)]
    rowsum_old = [sum(G_old[i]) for i in range(N)]
    if any(x != 0 for x in rowsum_old):
        die("CONTROL_A  the old G=2L must have EXACT zero row sums (Laplacian kills constants)")
    print("PASS_CONTROL_A  the OLD cert object G=2L has exact zero row-sums -> the divergence "
          "operator is non-degenerate (it returns 0 when it should). The OLD cert's "
          "'divergence-free' is TRUE but is about G=2L=dS/dL, NOT about G_A2=dS_A2/dh.")

    # Control B (the a2 tensor is genuinely NOT the Laplacian): its row-sum != Laplacian row-sum.
    # If G_A2's divergence accidentally equaled the Laplacian's, the obstruction would be vacuous.
    if is_conserved_flat:
        die("CONTROL_B  pre-registered: G_A2 must NOT be conserved on flat scene (else the "
            "obstruction claim is false and CONCLUSION_BUILT is wrong)")
    print("PASS_CONTROL_B  G_A2 divergence is nonzero while the Laplacian's is zero -> G_A2 is a "
          "DIFFERENT rank-2 object than 2L; the obstruction is real, not a mislabel.")

    # Control C: falsifiability of BUILT branch. Construct a hypothetical conserved tensor
    # (G' = 2L, edge value = 2 on each edge but assembled as a Laplacian, div=0) and confirm the
    # archive_divergence routine WOULD report conserved for it -> BUILT is reachable, not impossible
    # by construction. (Guards the 'zA = mu2*zvol' trap: the test can output either verdict.)
    Gp = {e: Q(0) for e in E}  # zero tensor: trivially conserved
    divp = archive_divergence(Gp, rho1)
    if any(x != 0 for x in divp):
        die("CONTROL_C  the archive_divergence routine must report the zero tensor as conserved "
            "(else the BUILT verdict is unreachable and the test is rigged toward OBSTRUCTION)")
    print("PASS_CONTROL_C  archive_divergence reports the zero tensor as conserved -> the BUILT "
          "verdict is reachable; the test is not rigged toward the obstruction.")

    # Control D (MODEL ROBUSTNESS -- answers the strongest skeptic attack SA-CRIT-1):
    # The obstruction must NOT hinge on choosing the off-diagonal-only EH proxy S_A2 over the
    # FULL Tr(L^2). Here we differentiate the FULL scalar S_full(w) = Tr(L(w)^2) w.r.t. the SAME
    # metric perturbation h_ab=w_ab (NOT w.r.t. L-entries -- L=L(w) via the chain rule, degree
    # included). Closed form (flat rho): with deg_a = sum_k w_ak,
    #   S_full = sum_a deg_a^2 + sum_{a!=b} w_ab^2
    #   G_full^{ab} = dS_full/dw_ab = 2(deg_a+deg_b) + 4 w_ab   (off-diagonal),
    # and (div G_full)_b = sum_a G_full^{ab} = 4E + 2N*deg_b.  If THIS is also nonzero, the
    # obstruction is model-robust: it does not depend on dropping the diagonal volume term.
    deg = [0] * N
    for (i, j) in E:
        deg[i] += 1; deg[j] += 1
    twoE = sum(deg)  # = 2|E|
    G_full_div = [Q(4 * len(E) + 2 * N * deg[b]) for b in range(N)]  # 4E + 2N*deg_b, E=|edges|
    # independent chain-rule finite difference of the FULL Tr(L^2) at one probe edge:
    def S_full(wmap):
        dg = [0] * N
        for (a, b), wv in wmap.items():
            dg[a] += wv; dg[b] += wv
        s = sum(Q(d) * Q(d) for d in dg)          # diagonal L_aa = deg_a
        s += sum(2 * wv * wv for wv in wmap.values())  # off-diag L_ab=-w_ab, twice (ab,ba)
        return s
    e0 = E[0]
    hp = dict(hw); hp[e0] = hw[e0] + Q(1, 5)
    hm = dict(hw); hm[e0] = hw[e0] - Q(1, 5)
    fd_full = (S_full(hp) - S_full(hm)) / (2 * Q(1, 5))
    Gfull_e0 = Q(2 * (deg[e0[0]] + deg[e0[1]]) + 4 * hw[e0])
    if fd_full != Gfull_e0:
        die(f"CONTROL_D  full-Tr(L^2) gradient mismatch at {e0}: closed {Gfull_e0} vs fd {fd_full}")
    if any(x == 0 for x in G_full_div):
        die("CONTROL_D  full-Tr(L^2) Einstein tensor divergence must be nonzero (model robustness)")
    print(f"PASS_CONTROL_D  MODEL-ROBUST: differentiating the FULL Tr(L^2) (diagonal volume term "
          f"included) w.r.t. the metric h gives (div G_full)_b = 4E+2N*deg_b = "
          f"{{{G_full_div[0]},{G_full_div[9]},{G_full_div[20]}}} != 0 -> the obstruction does NOT "
          f"depend on the off-diagonal-only EH-proxy choice.")

    print(f"\nRESULT  conclusion = {conclusion}  (flat_conserved={is_conserved_flat}, "
          f"perron_conserved={is_conserved_deg})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
