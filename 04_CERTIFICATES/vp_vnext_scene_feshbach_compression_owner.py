#!/usr/bin/env python3
"""vp_vnext_scene_feshbach_compression_owner - D0-VNEXT-AF-D0-FESHBACH-COMPRESSION-OWNER-001 (POSITIVE).

RETRACTION + CLOSURE. An earlier iteration flipped this owner to NO-GO on the grounds that the Feshbach
effective operator W_eff = A - B(D - zI)^-1 C "needs image(Xi^dag)/kernel(Xi)" and Xi (the scene<->AF
UNITARY comparison map) is obstructed. That reasoning conflates two different objects: a Feshbach
compression needs a keep/trace PROJECTION SPLIT, NOT a unitary intertwiner. The scene carries its OWN
canonical split -- the Aut(scene)-invariant zone/archive partition (bulk zones 1,2 = 9+11 = 20 vertices;
traced boundary zone 3 = 13 vertices; V=33) -- and against that split the Feshbach compression of the
scene Laplacian EXISTS and is EXACT.

This cert forms it in exact rational arithmetic and verifies:
  (1) the traced boundary block is D_tt = 20*I_13 EXACTLY (zone 3 has no internal edges; each boundary
      vertex has degree 33-13 = 20), so D_tt is invertible and the Schur complement AT z=0 is exact:
      W_eff(0) = A_bb - (1/20) B B^T  on the 20-dim bulk. The Schur complement is a SAMPLE-z object
      W_eff(z) = A_bb - (20 - z)^-1 B B^T, exact at each z (house convention vp_feshbach_schur_dynamics.py
      :16-17); it is NOT z-independent (checked below: W_eff(1) != W_eff(0)). The 5->4 distinct-count
      reduction is the z = 0 statement.
  (2) W_eff(0) has eigenvalues {0, 22, 24, 33} with exact multiplicities {1, 10, 8, 1} (nullities computed
      by exact Gaussian elimination, completeness sum = 20) -> 4 DISTINCT eigenvalues on a 20-dim space.
  (3) the scene Laplacian itself has 5 distinct eigenvalues {0,20,22,24,33} -- COMPUTED here by the same
      nullity probing over integer candidates 0..V with a completeness check (multiplicity sum = V = 33),
      not asserted; it agrees with the frozen upstream owner vp_scene_laplacian_spectrum_forced.py
      (D0-SCENE-LAPLACIAN-SPECTRUM-FORCED-001). So the canonical Feshbach compression performs EXACTLY the
      5 -> 4 distinct-eigenvalue reduction that a UNITARY Xi provably cannot do (a unitary preserves the
      distinct-eigenvalue count). The compression is the correct transport object; the unitary NO-GO
      (vp_vnext_scene_matched_owners_derived_nogo.py) is scoped to unitaries only and does NOT obstruct
      the compression.
  (4) the split is CANONICAL, not hand-picked: the three zones are exactly the orbits of the scene's
      automorphism group acting on vertices -- COMPUTED from the adjacency structure: same-zone vertices
      are false twins (identical neighborhoods) so each zone lies in one orbit, and the zone degrees
      N-n_i = {24,22,20} are pairwise DISTINCT so no automorphism maps between zones. Hence orbits = zones
      exactly, and "bulk = zones 1,2 / boundary = zone 3" is Aut-natural.

Falsifiable: breaks (rc=1) if D_tt != 20*I, if any claimed multiplicity is wrong or incomplete, if the
computed distinct counts are not 4 (compression) and 5 (scene), if the Schur complement turns out
z-independent, or if a non-invariant split is passed off as canonical.
Reachable negative controls reject (a) a unitary transport claim -- shown discriminating by an equal-part
control scene K(11,11,11) on which the compression drops NO distinct eigenvalue (3->3), so the count-drop
obstruction is specific to the true distinct-size scene and not an artifact of the test; and (b) an
arbitrary cross-zone vertex split, which breaks the exact D_tt = 20*I structure.
"""
import sys
from fractions import Fraction as Fr
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SIZES = [9, 11, 13]
V = sum(SIZES)


def die(msg: str) -> None:
    print("FAIL " + msg)
    raise SystemExit(1)


def laplacian(zone):
    n = len(zone)
    return [[(sum(1 for k in range(n) if zone[k] != zone[i]) if i == j
              else (-1 if zone[i] != zone[j] else 0)) for j in range(n)] for i in range(n)]


def exact_rank(M):
    M = [[Fr(x) for x in row] for row in M]
    rows, cols = len(M), len(M[0]); r = 0
    for c in range(cols):
        piv = next((i for i in range(r, rows) if M[i][c] != 0), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        inv = Fr(1) / M[r][c]; M[r] = [x * inv for x in M[r]]
        for i in range(rows):
            if i != r and M[i][c] != 0:
                f = M[i][c]; M[i] = [M[i][j] - f * M[r][j] for j in range(cols)]
        r += 1
    return r


def solve(D, C):
    """Return X with D X = C (D square invertible, C is m x p, both over Fr); raise if D singular."""
    m, p = len(D), len(C[0])
    aug = [[Fr(D[i][j]) for j in range(m)] + [Fr(C[i][j]) for j in range(p)] for i in range(m)]
    r = 0
    for c in range(m):
        piv = next((i for i in range(r, m) if aug[i][c] != 0), None)
        if piv is None:
            raise ValueError("singular D_tt")
        aug[r], aug[piv] = aug[piv], aug[r]
        inv = Fr(1) / aug[r][c]; aug[r] = [x * inv for x in aug[r]]
        for i in range(m):
            if i != r and aug[i][c] != 0:
                f = aug[i][c]; aug[i] = [aug[i][j] - f * aug[r][j] for j in range(m + p)]
        r += 1
    return [[aug[i][m + j] for j in range(p)] for i in range(m)]


def schur_z(L, keep, trace, z):
    """W_eff(z) = A_bb - B (D_tt - zI)^-1 C on the kept block (house sample-z convention)."""
    A = [[Fr(L[i][j]) for j in keep] for i in keep]
    if not trace:
        return A
    B = [[Fr(L[i][j]) for j in trace] for i in keep]
    C = [[Fr(L[i][j]) for j in keep] for i in trace]
    D = [[Fr(L[trace[a]][trace[b]]) - (Fr(z) if a == b else Fr(0)) for b in range(len(trace))]
         for a in range(len(trace))]
    X = solve(D, C)
    return [[A[i][j] - sum(B[i][k] * X[k][j] for k in range(len(trace))) for j in range(len(keep))]
            for i in range(len(keep))]


def distinct_spectrum(W, cand_max):
    """Multiplicity dict over integer candidate eigenvalues 0..cand_max, by exact nullity probing."""
    n = len(W)
    mults = {}
    for lam in range(cand_max + 1):
        Wl = [[Fr(W[i][j]) - (Fr(lam) if i == j else Fr(0)) for j in range(n)] for i in range(n)]
        nul = n - exact_rank(Wl)
        if nul > 0:
            mults[lam] = nul
    return mults


def dtt_is_20I(L, trace):
    """True iff the trace block of L is exactly 20*I."""
    m = len(trace)
    d0 = L[trace[0]][trace[0]]
    return d0 == 20 and all(L[trace[a]][trace[b]] == (d0 if a == b else 0)
                            for a in range(m) for b in range(m))


def zone_split(zone, trace_zone=2):
    keep = [i for i in range(len(zone)) if zone[i] != trace_zone]
    trace = [i for i in range(len(zone)) if zone[i] == trace_zone]
    return keep, trace


def main() -> int:
    print("=== vp_vnext_scene_feshbach_compression_owner  canonical Feshbach compression of the scene ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the Aut-invariant zone/archive split (bulk 20 / boundary 13) is "
          "fixed first; that the z=0 Schur complement is exact and does the 5->4 reduction is the consequence.")
    zone = sum(([zi] * s for zi, s in enumerate(SIZES)), [])
    L = laplacian(zone)
    keep, trace = zone_split(zone)

    # (1) traced boundary block D_tt = 20*I_13, exactly.
    if not dtt_is_20I(L, trace):
        die("D_TT_20I  traced boundary block must be exactly 20*I_13")
    print("PASS_D_TT_EXACT  D_tt = 20*I_13 exactly (boundary zone edge-free, degree 33-13=20); the Schur "
          "complement at z=0 is exact: W_eff(0) = A_bb - (1/20) B B^T (sample-z object, not z-independent).")

    # (2) W_eff(0) spectrum, computed with a completeness check (nullities total = bulk dim).
    W0 = schur_z(L, keep, trace, 0)
    nbulk = len(W0)
    comp_mults = distinct_spectrum(W0, V)
    if sum(comp_mults.values()) != nbulk:
        die(f"WEFF_COMPLETENESS  W_eff(0) integer nullities must total dim {nbulk}: {comp_mults}")
    if comp_mults != {0: 1, 22: 10, 24: 8, 33: 1} or nbulk != 20:
        die(f"WEFF_SPECTRUM  W_eff(0) spectrum/multiplicities wrong: {comp_mults} on dim {nbulk}")
    n_distinct_comp = len(comp_mults)
    print(f"PASS_WEFF_SPECTRUM  W_eff(0) (20-dim bulk) eigenvalues {{0:1, 22:10, 24:8, 33:1}} "
          f"(exact nullities, completeness sum={nbulk}).")

    # (3) scene distinct count -- COMPUTED (not hardcoded) by the same probing + completeness sum = V.
    scene_mults = distinct_spectrum(L, V)
    if sum(scene_mults.values()) != V:
        die(f"SCENE_COMPLETENESS  scene integer nullities must total V={V}: {scene_mults}")
    n_scene_distinct = len(scene_mults)
    if n_distinct_comp != 4 or n_scene_distinct != 5:
        die(f"REDUCTION  compression must have 4 distinct eigs (got {n_distinct_comp}), "
            f"scene 5 (got {n_scene_distinct})")
    print(f"PASS_5_TO_4_REDUCTION  scene has {n_scene_distinct} distinct eigenvalues {sorted(scene_mults)}; "
          f"the compression has {n_distinct_comp} -> the boundary trace REMOVES the eigenvalue 20 (the "
          f"boundary block's own value). This is exactly the reduction a UNITARY Xi cannot perform "
          f"(unitaries preserve distinct-eigenvalue count). (Agrees with vp_scene_laplacian_spectrum_forced.)")

    # (1b) z-DEPENDENCE: the Schur complement is a sample-z object, NOT z-independent. The 5->4 claim
    # is the z=0 statement; confirm W_eff genuinely varies with z (house convention, not z=0-by-fiat).
    W1 = schur_z(L, keep, trace, 1)
    if W0 == W1:
        die("Z_DEPENDENCE  W_eff must depend on z (D_tt=20*I => W_eff(z)=A_bb-(20-z)^-1 BB^T)")
    print("PASS_Z0_ANCHOR  W_eff(1) != W_eff(0): the Schur complement is a sample-z object per the house "
          "convention (vp_feshbach_schur_dynamics.py:16-17); the 5->4 reduction is the EXACT z=0 statement.")

    # (4) canonicity, COMPUTED: the zones ARE the Aut(scene) vertex orbits.
    #   (a) same-zone vertices are false twins (identical neighborhoods) -> each zone lies in one orbit;
    #   (b) zone degrees N-n_i are pairwise distinct -> no automorphism maps between zones.
    adj = [frozenset(j for j in range(V) if L[i][j] == -1) for i in range(V)]
    offset = 0
    zone_degs = []
    for zi, ni in enumerate(SIZES):
        base = adj[offset]
        if any(adj[i] != base for i in range(offset, offset + ni)):
            die(f"ORBIT_TWINS  zone {zi} vertices must be false twins (share one neighborhood)")
        zone_degs.append(len(base))
        offset += ni
    if len(set(zone_degs)) != 3 or sorted(zone_degs) != [20, 22, 24]:
        die(f"ORBIT_DEGREES  zone degrees must be pairwise-distinct {{24,22,20}}: {zone_degs}")
    print(f"PASS_CANONICAL_SPLIT  same-zone vertices are false twins and zone degrees {sorted(zone_degs)} "
          "are pairwise distinct -> orbits = zones exactly; the bulk/boundary split is Aut-invariant.")

    # ===================== REACHABLE NEGATIVE CONTROLS =====================
    # Control 1: the distinct-count DROP is what forbids a unitary transport, and it is SPECIFIC to the
    # true distinct-size scene. On the equal-part control scene K(11,11,11) the compression drops NO
    # distinct eigenvalue -- so there a unitary is NOT obstructed. The control fires only if the true
    # scene reduces AND the equal-part scene does not; this die is reachable under any mutation that
    # equalizes the two counts or breaks the equal-part no-reduction.
    ctrl_zone = sum(([zi] * 11 for zi in range(3)), [])   # K(11,11,11)
    ctrl_L = laplacian(ctrl_zone)
    ctrl_keep, ctrl_trace = zone_split(ctrl_zone)
    ctrl_scene_dc = len(distinct_spectrum(ctrl_L, len(ctrl_zone)))
    ctrl_comp = distinct_spectrum(schur_z(ctrl_L, ctrl_keep, ctrl_trace, 0), len(ctrl_zone))
    ctrl_comp_dc = len(ctrl_comp)
    true_reduces = n_scene_distinct > n_distinct_comp
    ctrl_reduces = ctrl_scene_dc > ctrl_comp_dc
    if true_reduces and not ctrl_reduces:
        print(f"FAIL_UNITARY_TRANSPORT_REJECTED  the true scene drops a distinct eigenvalue "
              f"({n_scene_distinct}->{n_distinct_comp}) so NO unitary transports it; the equal-part control "
              f"K(11,11,11) drops none ({ctrl_scene_dc}->{ctrl_comp_dc}) -> the count-drop obstruction is "
              f"specific to the distinct-size scene, not an artifact of the test.")
    else:
        die(f"control: expected true-scene reduction and equal-part no-reduction "
            f"(true {n_scene_distinct}->{n_distinct_comp}, ctrl {ctrl_scene_dc}->{ctrl_comp_dc})")

    # Control 2: an arbitrary cross-zone split of the SAME scene graph (swap one bulk vertex into the
    # trace and one boundary vertex into the bulk) breaks the exact D_tt = 20*I structure -> not a
    # canonical Feshbach split. Uses the fixed scene L; only the keep/trace partition is mutated.
    bad_trace = [i for i in trace if i != V - 1] + [0]   # drop last boundary vertex, add a bulk vertex
    if not dtt_is_20I(L, bad_trace):
        print("FAIL_ARBITRARY_SPLIT_REJECTED  a non-zone (cross-zone) vertex split breaks D_tt=20*I "
              "(the trace block gains internal edges) -> not a canonical Feshbach split.")
    else:
        die("control: arbitrary cross-zone split should have broken the exact boundary block")

    print("PASS_VNEXT_SCENE_FESHBACH_COMPRESSION_OWNER — the canonical Feshbach compression of the scene "
          "Laplacian EXISTS and is exact (W_eff(0) on the 20-dim bulk, 4 distinct eigenvalues); it performs "
          "the 5->4 reduction unitarily impossible. Status NO-GO -> CERT-CLOSED (retracts the earlier "
          "over-scoped unitary-only flip).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
