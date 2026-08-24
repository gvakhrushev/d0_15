#!/usr/bin/env python3
"""BRIDGE D0-INVARIANT-GENERATION-BRIDGE-001 — compute check.

CLAIM (span identity on Fin 33, exact over Q): the two separately built and
certified registry objects

  (A) R^Aut = (C^V)^Aut  — the extremal-minimal observable algebra of the frozen
      scene K(9,11,13)  (RAISE_SELECTOR_MINIMAL_MEMO.md, row D0-P-INVARIANT-MINIMAL-001),
      described as: class functions, dim = #orbits = 3, basis = zone indicators;

  (B) the OWNED generation space — the trivial-isotype multiplicity space
      span{1_9, 1_11, 1_13} that the M3 commutant block acts on
      (W2_QUANTITY_IDENT_MEMO.md:126-128, rows D0-MATTER-REP-001,
      D0-REPRESENTATION-RECONSTRUCTION-MAXIMALITY-NOGO-001)

are THE SAME subspace of C^33.

HONESTY CLAUSE (stated up front, repeated in the memo): mathematically the
Aut-fixed subspace and the trivial-isotype subspace of a permutation rep are the
image of the SAME projector (the Reynolds / orbit-averaging operator); the
identity is a definition-unfolding, not a nontrivial computation.  The can-fail
content of this script is therefore:
  (i)  THREE independently can-fail constructions coincide exactly over Q with
       dim 3 and basis {1_9,1_11,1_13} — i.e. BOTH memos' described bases/dims
       are as printed on disk:
         A: orbit-indicator span from the zone partition;
         B: exact nullspace of {P_g - I} over a GENERATING SET of S9 x S11 x S13;
         D: the invariant subspace the 9-dim M3 commutant block acts on,
            rebuilt from the pair-orbit basis.
       Route C (Reynolds image over generator-derived orbits) is kept but is
       NOT counted as independent: given the separately checked partition
       identity "orbits = zones", span C = span A is entailed; C's
       idempotence/symmetry/commutation lines are implementation checks;
  (ii) negative controls: lockstep on modified scenes (zone-count != 3 moves
       both readings together), repeated-size collapse (K(3,3,5) + swap
       generator collapses both to dim 2), wrong-space controls (transversal
       section, mean-zero standard vector) REJECTED;
  (iii) --mutate: every check must FAIL under a targeted corruption.

Exact arithmetic only (int / Fraction). Deliverable of the F1 flagship forge;
NOT registered, NOT a 05_CERTS cert. Companion memo:
_TASKS_CENTER_ATTACK/BRIDGE_INVARIANT_GENERATION_MEMO.md.
"""
from __future__ import annotations

import sys
from fractions import Fraction

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

FAILURES = []


def check(name, ok, detail=""):
    tag = "PASS" if ok else "FAIL"
    print(f"[{tag}] {name}" + (f"  -- {detail}" if detail else ""))
    if not ok:
        FAILURES.append(name)
    return ok


# --------------------------------------------------------------------------- scene
def scene(sizes):
    """K(sizes): zone map, 0/1 adjacency."""
    zone = []
    for zi, s in enumerate(sizes):
        zone += [zi] * s
    n = len(zone)
    A = [[1 if zone[i] != zone[j] else 0 for j in range(n)] for i in range(n)]
    return zone, A


def zone_blocks(zone):
    blocks = {}
    for v, z in enumerate(zone):
        blocks.setdefault(z, []).append(v)
    return [blocks[z] for z in sorted(blocks)]


# --------------------------------------------------------------- exact linear algebra
def rref(M):
    """Reduced row echelon over Q; returns (rref_rows_nonzero, rank)."""
    M = [[Fraction(x) for x in row] for row in M]
    if not M:
        return [], 0
    rows, cols = len(M), len(M[0])
    r = 0
    for c in range(cols):
        piv = next((i for i in range(r, rows) if M[i][c] != 0), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        pv = M[r][c]
        M[r] = [x / pv for x in M[r]]
        for i in range(rows):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [M[i][k] - f * M[r][k] for k in range(cols)]
        r += 1
        if r == rows:
            break
    return [row for row in M[:r]], r


def rank(M):
    return rref(M)[1]


def same_span(B1, B2):
    """Exact span equality over Q via rank of stacked bases."""
    r1, r2 = rank(B1), rank(B2)
    return r1 == r2 == rank(B1 + B2)


def nullspace(M):
    """Exact nullspace basis over Q of an m x n matrix."""
    R, r = rref(M)
    n = len(M[0]) if M else 0
    piv_cols = []
    for row in R:
        piv_cols.append(next(c for c in range(n) if row[c] != 0))
    free = [c for c in range(n) if c not in piv_cols]
    basis = []
    for fc in free:
        v = [Fraction(0)] * n
        v[fc] = Fraction(1)
        for i, pc in enumerate(piv_cols):
            v[pc] = -R[i][fc]
        basis.append(v)
    return basis


# ----------------------------------------------------------------- group machinery
def perm_matrix_minus_I_rows(perm, n):
    """Rows of (P_g - I) acting on functions: (P_g f)(v) = f(g^{-1} v).
    For span equality of FIXED VECTORS it suffices to use coordinates:
    f fixed  <=>  f(g(v)) = f(v) for all v.  Row per v: e_{g(v)} - e_v."""
    rows = []
    for v in range(n):
        w = perm[v]
        if w == v:
            continue
        row = [Fraction(0)] * n
        row[w] += 1
        row[v] -= 1
        rows.append(row)
    return rows


def within_zone_generators(zone, extra_swaps=()):
    """Adjacent transpositions within each zone (generate S_{z} per zone),
    plus optional whole-zone swap permutations (for repeated-size controls)."""
    n = len(zone)
    gens = []
    blocks = zone_blocks(zone)
    for blk in blocks:
        for a, b in zip(blk, blk[1:]):
            p = list(range(n))
            p[a], p[b] = p[b], p[a]
            gens.append(p)
    for (i, j) in extra_swaps:
        bi, bj = blocks[i], blocks[j]
        assert len(bi) == len(bj)
        p = list(range(n))
        for a, b in zip(bi, bj):
            p[a], p[b] = b, a
        gens.append(p)
    return gens


def is_automorphism(perm, A):
    n = len(A)
    return all(A[perm[i]][perm[j]] == A[i][j] for i in range(n) for j in range(n))


# ------------------------------------------------------------------- the four routes
def route_A_indicators(zone):
    """(A) selector face as printed: span of zone-indicator vectors."""
    n = len(zone)
    return [[Fraction(1) if zone[v] == z else Fraction(0) for v in range(n)]
            for z in sorted(set(zone))]


def route_B_generator_fixed(gens, n):
    """(B) fixed subspace = exact nullspace of stacked (coordinate) constraints
    f(g(v)) = f(v) over a generating set.  Fixed under generators = fixed under
    the whole group (can-fail: generators verified as automorphisms upstream)."""
    rows = []
    for g in gens:
        rows += perm_matrix_minus_I_rows(g, n)
    if not rows:
        return [[Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(n)]
    return nullspace(rows)


def orbits_from_generators(gens, n):
    """True Aut-orbits from the generating set (union-find). This is the
    group-derived partition — NOT assumed equal to the zone partition."""
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for g in gens:
        for v in range(n):
            a, b = find(v), find(g[v])
            if a != b:
                parent[a] = b
    groups = {}
    for v in range(n):
        groups.setdefault(find(v), []).append(v)
    return sorted(groups.values(), key=lambda blk: blk[0])


def route_C_orbit_average(gens, n):
    """(C) trivial-isotype projector = the Reynolds operator (1/|G|) sum_g P_g,
    computed exactly as averaging over the TRUE generator-derived orbits
    (a standard identity for permutation reps: the group average of e_v is the
    uniform vector on the orbit of v).  Returns (T, image_basis, orbits)."""
    orbs = orbits_from_generators(gens, n)
    T = [[Fraction(0)] * n for _ in range(n)]
    for blk in orbs:
        s = Fraction(1, len(blk))
        for i in blk:
            for j in blk:
                T[i][j] = s
    image = [T[blk[0]] for blk in orbs]
    return T, image, orbs


def mat_mul(X, Y):
    n, m, p = len(X), len(Y), len(Y[0])
    return [[sum(X[i][k] * Y[k][j] for k in range(m)) for j in range(p)] for i in range(n)]


def route_D_commutant_block(zone, A):
    """(D) generation face: pair-orbit basis of the commutant; keep the 9
    zone-block-constant matrices B_(a,b) (value 1 on zone_a x zone_b pattern,
    diagonal handled within-zone); verify each maps span{1_z} into itself and
    that the restricted 3x3 matrices span the FULL M3 (rank 9).  Returns
    (invariant_ok, m3_rank, restricted_span_basis)."""
    n = len(zone)
    zones = sorted(set(zone))
    indicators = route_A_indicators(zone)
    restricted_flat = []
    invariant_ok = True
    for za in zones:
        for zb in zones:
            # pair-orbit basis matrix: E[i][j] = 1 iff zone(i)=za and zone(j)=zb
            # (for za==zb this is the all-ones within-zone block incl. diagonal;
            #  off-diag/diag split adds the identity which is also commutant —
            #  span unchanged, kept coarse deliberately)
            E = [[Fraction(1) if (zone[i] == za and zone[j] == zb) else Fraction(0)
                  for j in range(n)] for i in range(n)]
            # image of each indicator under E
            resticted_matrix = []
            for ind in indicators:
                img = [sum(E[i][j] * ind[j] for j in range(n)) for i in range(n)]
                # img must lie in span(indicators): it equals (zone_zb size or 0) * 1_za
                if not same_span(indicators, indicators + [img]):
                    invariant_ok = False
                # coordinates of img in the indicator basis (indicators are
                # disjointly supported: coordinate = value on first vertex of each zone)
                firsts = [zone_blocks(zone)[z][0] for z in zones]
                resticted_matrix.append([img[f] for f in firsts])
            restricted_flat.append([x for row in resticted_matrix for x in row])
    m3_rank = rank(restricted_flat)
    return invariant_ok, m3_rank, restricted_flat


# ----------------------------------------------------------------------- main checks
def run_bridge(sizes, expect_dim, extra_swaps=(), label=""):
    """Full four-route coincidence on K(sizes); returns dims for lockstep checks."""
    zone, A = scene(sizes)
    n = len(zone)
    gens = within_zone_generators(zone, extra_swaps=extra_swaps)
    lbl = label or f"K{tuple(sizes)}"

    check(f"{lbl}: all generators are automorphisms of A",
          all(is_automorphism(g, A) for g in gens), f"{len(gens)} generators")

    VA = route_A_indicators(zone)
    VB = route_B_generator_fixed(gens, n)
    T, VC, orbs = route_C_orbit_average(gens, n)

    dimA, dimB, dimC = rank(VA), rank(VB), rank(VC)

    if not extra_swaps:
        check(f"{lbl}: orbits (group-derived) = zones (the partition identity)",
              orbs == zone_blocks(zone), f"{len(orbs)} orbits")
        check(f"{lbl}: dim route A (zone indicators) = {expect_dim}", dimA == expect_dim, f"dim={dimA}")
    check(f"{lbl}: dim route B (generator-fixed nullspace) = {expect_dim}", dimB == expect_dim, f"dim={dimB}")
    check(f"{lbl}: dim route C (Reynolds image) = {expect_dim}", dimC == expect_dim, f"dim={dimC}")

    check(f"{lbl}: T idempotent (T^2 = T)", mat_mul(T, T) == T)
    check(f"{lbl}: T symmetric", all(T[i][j] == T[j][i] for i in range(n) for j in range(n)))
    check(f"{lbl}: T commutes with every generator",
          all(all(T[g[i]][g[j]] == T[i][j] for i in range(n) for j in range(n)) for g in gens))

    if extra_swaps:
        # repeated-size control: zones != orbits, indicator span is NOT the fixed space
        check(f"{lbl}: orbits != zones (swap merges the repeated zones)",
              orbs != zone_blocks(zone), f"{len(orbs)} orbits vs {len(zone_blocks(zone))} zones")
        check(f"{lbl}: span B = span C still (both group-derived, exact over Q)",
              same_span(VB, VC))
        check(f"{lbl}: per-listed-zone indicators STRICTLY BIGGER than fixed space (collapse)",
              not same_span(VA, VB) and rank(VA) > dimB,
              f"dim indicators={rank(VA)}, dim fixed={dimB}")
        return dimB

    check(f"{lbl}: span A = span B (exact over Q)", same_span(VA, VB))
    check(f"{lbl}: span A = span C (exact over Q)", same_span(VA, VC))
    check(f"{lbl}: span B = span C (exact over Q)", same_span(VB, VC))

    inv_ok, m3rank, _ = route_D_commutant_block(zone, A)
    nz = len(sizes)
    check(f"{lbl}: commutant pair-orbit block preserves the indicator span", inv_ok)
    check(f"{lbl}: restricted block spans FULL M{nz} (rank {nz*nz})", m3rank == nz * nz, f"rank={m3rank}")
    return dimB


def wrong_space_controls():
    zone, A = scene([9, 11, 13])
    n = len(zone)
    gens = within_zone_generators(zone)
    VA = route_A_indicators(zone)
    blocks = zone_blocks(zone)

    # transversal section: first vertex of each zone — dim 3 but NOT the space
    W = []
    for blk in blocks:
        v = [Fraction(0)] * n
        v[blk[0]] = Fraction(1)
        W.append(v)
    check("CONTROL: transversal section {e_v0} has dim 3 but is NOT the bridge space",
          rank(W) == 3 and not same_span(W, VA))
    moved = any(g[blocks[0][0]] != blocks[0][0] for g in gens)
    check("CONTROL: transversal section is not Aut-invariant (a generator moves it)", moved)

    # mean-zero standard vector in zone 9 is orthogonal to / outside the space
    v = [Fraction(0)] * n
    v[blocks[0][0]], v[blocks[0][1]] = Fraction(1), Fraction(-1)
    check("CONTROL: mean-zero (standard-isotype) vector lies OUTSIDE the bridge space",
          not same_span(VA, VA + [v]))
    # and the Reynolds projector kills it
    T, _, _ = route_C_orbit_average(gens, n)
    Tv = [sum(T[i][j] * v[j] for j in range(n)) for i in range(n)]
    check("CONTROL: Reynolds projector annihilates the standard vector",
          all(x == 0 for x in Tv))


def mutation_tests():
    """Each mutation must make a core check FAIL (recorded as PASS of the mutation test)."""
    zone, A = scene([9, 11, 13])
    n = len(zone)

    # m1: drop the S11 and S13 generators -> fixed space of PARTIAL group is bigger
    gens_partial = [g for g in within_zone_generators(zone) if all(g[v] == v for v in range(9, 33))]
    VB_partial = route_B_generator_fixed(gens_partial, n)
    check("MUTATE m1: partial generating set inflates the fixed space (25 != 3)",
          rank(VB_partial) == 1 + 11 + 13 and not same_span(route_A_indicators(zone), VB_partial))

    # m2: corrupt the projector (wrong orbit size) -> idempotence fails
    T, _, _ = route_C_orbit_average(within_zone_generators(zone), n)
    Tbad = [row[:] for row in T]
    Tbad[0][0] = Fraction(1, 8)  # wrong 1/|orbit|
    check("MUTATE m2: corrupted Reynolds (1/8 on a 9-orbit) loses idempotence",
          mat_mul(Tbad, Tbad) != Tbad)

    # m3: a non-automorphism 'generator' (cross-zone transposition) is caught
    p = list(range(n))
    p[0], p[9] = p[9], p[0]
    check("MUTATE m3: cross-zone transposition rejected as automorphism",
          not is_automorphism(p, A))

    # m4: wrong claimed dim on a 4-zone scene
    zone4, _ = scene([2, 3, 4, 5])
    VB4 = route_B_generator_fixed(within_zone_generators(zone4), len(zone4))
    check("MUTATE m4: K(2,3,4,5) fixed-space dim is 4, not 3", rank(VB4) == 4 and rank(VB4) != 3)

    # m5: perturbed indicator basis (one vertex flipped to wrong zone) breaks span equality
    VAbad = route_A_indicators(zone)
    VAbad[0][9] = Fraction(1)  # 1_9 grabs a zone-11 vertex
    VB = route_B_generator_fixed(within_zone_generators(zone), n)
    check("MUTATE m5: corrupted indicator (zone-11 vertex in 1_9) breaks span equality",
          not same_span(VAbad, VB))


def main():
    mutate = "--mutate" in sys.argv
    print("=" * 78)
    print("BRIDGE D0-INVARIANT-GENERATION-BRIDGE-001 — four-route coincidence check")
    print("=" * 78)

    # THE scene
    d = run_bridge([9, 11, 13], expect_dim=3, label="K(9,11,13)")
    zone, _ = scene([9, 11, 13])
    VA = route_A_indicators(zone)
    check("K(9,11,13): basis is exactly {1_9, 1_11, 1_13} (disjoint 0/1 supports 9/11/13)",
          [sum(v) for v in VA] == [9, 11, 13] and all(x in (0, 1) for v in VA for x in v))
    check("K(9,11,13): trivial-isotype multiplicity (= fixed dim) = generation count 3", d == 3)

    print("-" * 78)
    print("NEGATIVE CONTROLS (lockstep + wrong-space + repeated-size)")
    print("-" * 78)
    # lockstep: zone-count != 3 moves BOTH readings together
    d2 = run_bridge([9, 11], expect_dim=2, label="LOCKSTEP K(9,11)")
    d4 = run_bridge([2, 3, 4, 5], expect_dim=4, label="LOCKSTEP K(2,3,4,5)")
    check("LOCKSTEP: zone-count != 3 changes both faces together (2 and 4, never 3)",
          d2 == 2 and d4 == 4)
    # repeated sizes: zone swap collapses BOTH readings below the listed zone count
    dswap = run_bridge([3, 3, 5], expect_dim=2, extra_swaps=[(0, 1)], label="REPEAT K(3,3,5)+swap")
    check("REPEAT: K(3,3,5) with swap collapses BOTH readings to dim 2 (distinct sizes are load-bearing)",
          dswap == 2)
    wrong_space_controls()

    if mutate:
        print("-" * 78)
        print("MUTATION TESTS (each corruption must be caught)")
        print("-" * 78)
        mutation_tests()

    print("=" * 78)
    if FAILURES:
        print(f"RESULT: FAIL ({len(FAILURES)} failed): {FAILURES}")
        sys.exit(1)
    print("RESULT: ALL CHECKS PASS")
    sys.exit(0)


if __name__ == "__main__":
    main()
