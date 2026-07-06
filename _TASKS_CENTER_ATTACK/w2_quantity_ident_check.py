#!/usr/bin/env python3
"""W2 — quantity-identification check for cluster J (T1 "Obstruction=Equation" uplift).

Targets: R1 (commutant M3+C+C+C), R2 (rescale 2|E|=718), R3 (Perron floor 718/33),
R5 (1/(3 ln phi) retype ONLY — the alpha-seam stays CLOSED per ALPHA_SEAM_NOGO_V2.md),
E1 (nc = p^2+q^2+3 as graded-commutant dimension), E2 (15708-14990 = 718 backtracking bijection).

Method: every quantity is built INDEPENDENTLY from the zone sizes (9,11,13) alone —
no target constant is an input to its own check (trap (f)). All decisions are exact
(int / Fraction); floats appear only in the R5 convergence ILLUSTRATION, whose decision
is the symbolic identity 3*ln(phi) = ln(phi^3).

Deliverable of TASK W2; NOT registered, NOT a 05_CERTS cert (kept out of the CI glob).
Companion memo: _TASKS_CENTER_ATTACK/W2_QUANTITY_IDENT_MEMO.md.

Built-in mutation tests: `--mutate` runs every check against a targeted wrong input and
requires the check to FAIL (controls can fail the CONCLUSION, not just the technique).
"""
from __future__ import annotations

import math
import sys
from fractions import Fraction
from itertools import combinations

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


# --------------------------------------------------------------------------- scene
def scene(sizes):
    """Complete multipartite graph K(sizes): zone map, adjacency (0/1 ints), degrees."""
    zone = []
    for zi, s in enumerate(sizes):
        zone += [zi] * s
    n = len(zone)
    A = [[1 if zone[i] != zone[j] else 0 for j in range(n)] for i in range(n)]
    deg = [sum(row) for row in A]
    return zone, A, deg


def rank_exact(M):
    """Exact rank over Q (Fraction Gaussian elimination)."""
    M = [[Fraction(x) for x in row] for row in M]
    if not M:
        return 0
    rows, cols = len(M), len(M[0])
    r = 0
    for c in range(cols):
        piv = next((i for i in range(r, rows) if M[i][c] != 0), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        pv = M[r][c]
        for i in range(rows):
            if i != r and M[i][c] != 0:
                f = M[i][c] / pv
                M[i] = [M[i][k] - f * M[r][k] for k in range(cols)]
        r += 1
        if r == rows:
            break
    return r


def matmul(X, Y):
    n, m, p = len(X), len(Y[0]), len(Y)
    Yt = list(zip(*Y))
    return [[sum(X[i][k] * Yt[j][k] for k in range(p)) for j in range(m)] for i in range(n)]


def perm_generators(sizes, add_swap01=False):
    """Generators of S_{n1} x S_{n2} x ... as vertex permutations (adjacent transposition
    + full cycle per zone). Optionally the zone-0 <-> zone-1 swap (only valid if equal sizes)."""
    gens = []
    off = 0
    for s in sizes:
        idx = list(range(off, off + s))
        if s >= 2:
            t = list(range(sum(sizes)))
            t[idx[0]], t[idx[1]] = t[idx[1]], t[idx[0]]
            gens.append(t)
            c = list(range(sum(sizes)))
            for k in range(s):
                c[idx[k]] = idx[(k + 1) % s]
            gens.append(c)
        off += s
    if add_swap01:
        assert sizes[0] == sizes[1]
        t = list(range(sum(sizes)))
        for k in range(sizes[0]):
            t[k], t[sizes[0] + k] = t[sizes[0] + k], t[k]
        gens.append(t)
    return gens


def pair_orbits(n, gens):
    """Orbits of the generated group on ordered pairs (i,j) — BFS. Returns orbit id map."""
    orb = {}
    nxt = 0
    for start in ((i, j) for i in range(n) for j in range(n)):
        if start in orb:
            continue
        orb[start] = nxt
        stack = [start]
        while stack:
            i, j = stack.pop()
            for g in gens:
                p = (g[i], g[j])
                if p not in orb:
                    orb[p] = nxt
                    stack.append(p)
        nxt += 1
    return orb, nxt


# --------------------------------------------------------------------------- R1 / E1 machinery
def commutant_data(sizes, add_swap01=False):
    """Build the commutant of the zone-permutation group as the span of pair-orbit
    indicator matrices. Returns dict with orbit count, basis, zone data."""
    zone, A, deg = scene(sizes)
    n = len(zone)
    gens = perm_generators(sizes, add_swap01=add_swap01)
    orb, n_orb = pair_orbits(n, gens)
    basis = []
    for o in range(n_orb):
        B = [[1 if orb[(i, j)] == o else 0 for j in range(n)] for i in range(n)]
        basis.append(B)
    return {"zone": zone, "A": A, "deg": deg, "n": n, "basis": basis, "n_orb": n_orb,
            "sizes": sizes}


def orbit_constant(M, basis):
    """True iff M is constant on every pair-orbit (i.e. lies in span(basis))."""
    for B in basis:
        vals = {M[i][j] for i in range(len(M)) for j in range(len(M)) if B[i][j]}
        if len(vals) > 1:
            return False
    return True


def pi_gen(M, zone, sizes):
    """Action of a commutant element on the zone-indicator span (generation space):
    returns 3x3 Fraction matrix or None if M does not preserve zone-constancy."""
    n = len(zone)
    k = len(sizes)
    cols = []
    for z in range(k):
        v = [Fraction(sum(M[i][j] for j in range(n) if zone[j] == z)) for i in range(n)]
        col = [None] * k
        for i in range(n):
            zi = zone[i]
            if col[zi] is None:
                col[zi] = v[i]
            elif col[zi] != v[i]:
                return None  # not zone-constant
        cols.append(col)
    return [[cols[z][w] for z in range(k)] for w in range(k)]  # entry (w,z): value on zone w of M*1_z


def std_scalar(M, zone, z):
    """Scalar by which M acts on within-zone-z difference vectors, or None."""
    idxs = [i for i in range(len(zone)) if zone[i] == z]
    if len(idxs) < 2:
        return None
    u0, u1 = idxs[0], idxs[1]
    # w = M (e_u0 - e_u1)
    w = [Fraction(M[i][u0] - M[i][u1]) for i in range(len(zone))]
    c = w[u0]  # must equal c on u0, -c on u1, 0 elsewhere
    ref = [Fraction(0)] * len(zone)
    ref[u0], ref[u1] = c, -c
    if w != ref:
        return None
    # confirm on a second independent difference
    if len(idxs) >= 3:
        u2 = idxs[2]
        w2 = [Fraction(M[i][u0] - M[i][u2]) for i in range(len(zone))]
        ref2 = [Fraction(0)] * len(zone)
        ref2[u0], ref2[u2] = c, -c
        if w2 != ref2:
            return None
    return c


def centralizer_dim(basis, G):
    """dim over Q of {X in span(basis) : XG = GX}, exact."""
    n = len(G)
    cols = []
    for B in basis:
        C = [[sum(B[i][k] * G[k][j] - G[i][k] * B[k][j] for k in range(n))
              for j in range(n)] for i in range(n)]
        cols.append([C[i][j] for i in range(n) for j in range(n)])
    # dim of null space of the (n^2 x n_basis) matrix
    Mt = list(map(list, zip(*cols)))  # rows = n^2, cols = basis
    return len(basis) - rank_exact(Mt)


# --------------------------------------------------------------------------- checks (each -> bool)
def check_R1(sizes=(9, 11, 13), expect_orb=12, expect_m3_rank=9, verbose=True):
    """R1: commutant dim = 12 with algebra structure M3 (+) C (+) C (+) C, where the M3 factor is
    End(generation space) = End(span of zone indicators), and every basis element is scalar on
    the std blocks. Also: the degree operator D lies in the commutant and its centralizer there
    has dim 6 (typed collapse of M3 to the diagonal — COLOUR row leg A)."""
    cd = commutant_data(sizes)
    ok = True
    n_orb = cd["n_orb"]
    if verbose:
        print(f"  [R1] pair-orbit count (= commutant dim) = {n_orb}")
    ok &= (n_orb == expect_orb)

    # closure: products of basis elements stay orbit-constant (algebra, not just space)
    closed = all(orbit_constant(matmul(B1, B2), cd["basis"])
                 for B1 in cd["basis"] for B2 in cd["basis"])
    if verbose:
        print(f"  [R1] closure under multiplication (all {n_orb}x{n_orb} products in span): {closed}")
    ok &= closed

    # structure map: X -> (pi_gen(X), c_9(X), c_11(X), c_13(X))
    coords = []
    all_scalar = True
    for B in cd["basis"]:
        pg = pi_gen(B, cd["zone"], sizes)
        if pg is None:
            all_scalar = False
            break
        sc = [std_scalar(B, cd["zone"], z) for z in range(len(sizes))]
        if any(s is None for s in sc):
            all_scalar = False
            break
        coords.append([pg[i][j] for i in range(3) for j in range(3)] + sc)
    if verbose:
        print(f"  [R1] every basis element zone-constant on indicators AND scalar on std blocks: {all_scalar}")
    ok &= all_scalar
    if not all_scalar:
        return False

    m3_rank = rank_exact([c[:9] for c in coords])
    full_rank = rank_exact(coords)
    if verbose:
        print(f"  [R1] rank of pi_gen images in M3 = {m3_rank} (=9 <=> M3 factor is FULL)")
        print(f"  [R1] rank of full structure map = {full_rank} (={expect_orb} <=> iso onto M3+C+C+C)")
    ok &= (m3_rank == expect_m3_rank and full_rank == expect_orb)

    # multiplicativity bridge (skeptic #1 repair, required): the structure map is an ALGEBRA
    # homomorphism, checked DIRECTLY on all basis pairs:
    #   coords(Bi @ Bj) == (pi_gen(Bi) * pi_gen(Bj), c_z(Bi) * c_z(Bj)).
    # (Restriction to invariant subspaces is automatically multiplicative; this makes it computed,
    # so rank 12 + multiplicativity = ALGEBRA isomorphism, not merely a linear one.)
    pis = [pi_gen(B, cd["zone"], sizes) for B in cd["basis"]]
    scs = [[std_scalar(B, cd["zone"], z) for z in range(len(sizes))] for B in cd["basis"]]
    mult_ok = True
    for i, Bi in enumerate(cd["basis"]):
        for j, Bj in enumerate(cd["basis"]):
            P = matmul(Bi, Bj)
            if (pi_gen(P, cd["zone"], sizes) != matmul(pis[i], pis[j])
                    or [std_scalar(P, cd["zone"], z) for z in range(len(sizes))]
                    != [scs[i][z] * scs[j][z] for z in range(len(sizes))]):
                mult_ok = False
    if verbose:
        print(f"  [R1] structure map multiplicative on all {len(cd['basis'])}^2 basis pairs"
              f" (ALGEBRA homomorphism, not merely linear): {mult_ok}")
    ok &= mult_ok

    # typed collapse: D = diag(deg) is IN the commutant; its centralizer there has dim 6
    n = cd["n"]
    D = [[cd["deg"][i] if i == j else 0 for j in range(n)] for i in range(n)]
    d_in = orbit_constant(D, cd["basis"])
    cdim = centralizer_dim(cd["basis"], D)
    if verbose:
        print(f"  [R1] degree operator D in commutant: {d_in}; centralizer of D in commutant dim = {cdim}"
              f" (= 3 diag on M3 + 3 std scalars — typed collapse, COLOUR leg A)")
    ok &= d_in and (cdim == 6)
    return ok


def check_E1(sizes=(9, 11, 13), verbose=True):
    """E1: nc(p,q) = p^2+q^2+3 IS the dimension of the graded commutant — the centralizer, inside
    the R1 commutant, of a grading acting with signature (p,q) on the generation space. Computed
    exactly for all 4 signatures; also S3-robustness (which axes carry the -1 does not matter);
    also a NON-involution 'grading' breaks the formula (the formula is signature-specific)."""
    cd = commutant_data(sizes)
    zone, n, k = cd["zone"], cd["n"], len(sizes)

    def gamma(signs, std_sign=1):
        """Gamma = sum_z eps_z J_z/n_z + std_sign * (I_z - J_z/n_z) — grading with pi_gen = diag(signs)."""
        G = [[Fraction(0)] * n for _ in range(n)]
        off = 0
        for z, s in enumerate(sizes):
            for i in range(off, off + s):
                for j in range(off, off + s):
                    G[i][j] += Fraction(signs[z] - std_sign, s)
                    if i == j:
                        G[i][j] += std_sign
            off += s
        return G

    ok = True
    sig_axes = {(3, 0): [(1, 1, 1)], (2, 1): [(1, 1, -1), (1, -1, 1), (-1, 1, 1)],
                (1, 2): [(1, -1, -1), (-1, 1, -1), (-1, -1, 1)], (0, 3): [(-1, -1, -1)]}
    for (p, q), axes in sig_axes.items():
        dims = {centralizer_dim(cd["basis"], gamma(sgn)) for sgn in axes}
        want = p * p + q * q + 3
        good = (dims == {want})
        if verbose:
            print(f"  [E1] signature ({p},{q}): graded-commutant dim(s) {sorted(dims)} == p^2+q^2+3 = {want}"
                  f" (axis-independent): {good}")
        ok &= good
    # negative structure control: a non-involution element (pi_gen = diag(1,2,3)) is NOT a grading;
    # its centralizer dim (6) matches NO admissible nc value {8,12} — the formula is signature-specific.
    G3 = gamma((1, 2, 3))
    d3 = centralizer_dim(cd["basis"], G3)
    good3 = d3 not in {p * p + q * q + 3 for (p, q) in sig_axes}
    if verbose:
        print(f"  [E1] control: non-involution diag(1,2,3) centralizer dim = {d3} not in {{8,12}}: {good3}")
    ok &= good3
    return ok


def check_capacity(sizes=(9, 11, 13), expect=None, verbose=True):
    """R2/R3/E2/REHEATING unified capacity block. Independently computes, from sizes alone:
      C  = sum(deg) = 2|E| = Tr L = #directed edges = #backtracking depth-2 walks (bijection)
      C/N = mean degree = mean Laplacian eigenvalue (REHEATING ratio) = R3 Rayleigh floor
      archive spectrum (L on ker A) = degrees; rescaled by C all < 1 (R2)
      depth-2 all-walks vs non-backtracking counts and their gap (E2)
    `expect` (only for the frozen scene) pins the corpus constants — the COMPARISON is the check;
    the constants are never used in the construction."""
    zone, A, deg = scene(sizes)
    n = len(zone)
    ok = True

    # --- capacity, three independent faces
    C_handshake = sum(deg)
    E_edges = sum(A[i][j] for i in range(n) for j in range(n) if i < j)
    L = [[(deg[i] if i == j else 0) - A[i][j] for j in range(n)] for i in range(n)]
    C_trace = sum(L[i][i] for i in range(n))
    dir_edges = [(i, j) for i in range(n) for j in range(n) if A[i][j]]
    ok &= (C_handshake == 2 * E_edges == C_trace == len(dir_edges))
    if verbose:
        print(f"  [CAP] C = sum(deg) = {C_handshake} = 2|E| = {2*E_edges} = Tr L = {C_trace}"
              f" = #directed-edges = {len(dir_edges)} : {ok}")

    # --- E2: depth-2 walk counts by DIRECT ENUMERATION (independent of the sum-formulas)
    walks2 = [(a, b, c) for a in range(n) for b in range(n) for c in range(n)
              if A[a][b] and A[b][c]]
    nb2 = [w for w in walks2 if w[2] != w[0]]
    bt2 = [w for w in walks2 if w[2] == w[0]]
    gap = len(walks2) - len(nb2)
    # explicit bijection: backtracking walk (a,b,a) <-> directed edge (a,b)
    bij = sorted((a, b) for (a, b, _) in bt2) == sorted(dir_edges)
    ok &= (gap == len(bt2) == C_handshake) and bij
    if verbose:
        print(f"  [E2] all-walks depth-2 = {len(walks2)}, non-backtracking = {len(nb2)},"
              f" gap = {gap} = #backtracking = C; bijection bt2 <-> directed edges: {bij}")

    # --- Laplacian spectrum, exact (multiplicity via rank; candidate eigenvalues verified,
    #     completeness via multiplicity sum). Candidates: 0, each degree value, N.
    cand = sorted(set([0] + deg + [n]))
    spec = {}
    for lam in cand:
        Mm = [[L[i][j] - (lam if i == j else 0) for j in range(n)] for i in range(n)]
        m = n - rank_exact(Mm)
        if m > 0:
            spec[lam] = m
    complete = (sum(spec.values()) == n)
    wsum = sum(Fraction(lam * m) for lam, m in spec.items())
    ok &= complete and (wsum == C_handshake)
    if verbose:
        print(f"  [REH] Laplacian spectrum {spec} complete={complete};"
              f" spectralWeightSum = {wsum} = C : {wsum == C_handshake}")

    # --- R3 floor / REHEATING ratio: mean degree as exact Fraction; > phi^3 exactly in Q(phi)
    ratio = Fraction(C_handshake, n)
    # phi^3 = 1 + 2*phi ; ratio > 1 + 2*phi  <=>  (ratio-1)/2 > phi  <=>  ((ratio-1)/2 - 1/2)*2 > sqrt5
    #   <=> (ratio - 2) > sqrt5  <=> (ratio-2)^2 > 5 (given ratio > 2)
    r2 = ratio - 2
    above_phi3 = (ratio > 2) and (r2 * r2 > 5)
    ok &= above_phi3
    if verbose:
        print(f"  [R3] Perron floor = C/N = {ratio} = mean degree = REHEATING threshold;"
              f" exact (C/N - 2)^2 = {r2*r2} > 5 <=> C/N > phi^3: {above_phi3}")

    # --- R2: archive sector = ker A; L acts there with spectrum = degrees; rescale by C < 1
    rkA = rank_exact(A)
    dim_ker = n - rkA
    # within-zone difference vectors: verify in ker A and L-eigen with eigenvalue deg(zone)
    arch_ok = True
    zone_first = {}
    for i, z in enumerate(zone):
        zone_first.setdefault(z, i)
    diffs = 0
    for i in range(n):
        z = zone[i]
        i0 = zone_first[z]
        if i == i0:
            continue
        v = [0] * n
        v[i0], v[i] = 1, -1
        Av = [sum(A[r][c] * v[c] for c in range(n)) for r in range(n)]
        Lv = [sum(L[r][c] * v[c] for c in range(n)) for r in range(n)]
        arch_ok &= all(x == 0 for x in Av) and (Lv == [deg[i0] * x for x in v])
        diffs += 1
    ok &= arch_ok and (diffs == dim_ker)
    shares = sorted({Fraction(d, C_handshake) for d in deg}, reverse=True)
    contr = all(s < 1 for s in shares)
    total_share = sum(Fraction(deg[i], C_handshake) for i in range(n))
    ok &= contr and (total_share == 1)
    if verbose:
        print(f"  [R2] dim ker A = {dim_ker} (= sum(n_z - 1)); L|ker eigenvalues = zone degrees"
              f" {sorted(set(deg), reverse=True)} (verified on all {diffs} spanning diffs): {arch_ok}")
        print(f"  [R2] capacity shares deg/C = {[str(s) for s in shares]} all < 1: {contr};"
              f" sum over vertices = {total_share} (stationary normalization)")

    if expect is not None:
        pin = (C_handshake == expect["C"] and len(walks2) == expect["W2"]
               and len(nb2) == expect["NB2"] and ratio == Fraction(*expect["ratio"])
               and sorted(set(deg), reverse=True) == expect["degs"]
               and spec == expect["spec"])
        ok &= pin
        if verbose:
            print(f"  [PIN] matches frozen-scene corpus constants"
                  f" (718 / 15708 / 14990 / 718:33 / degrees / spectrum): {pin}")
    return ok


def check_gap_identity_universal(verbose=True):
    """E2 provenance: gap(all-walks, non-backtracking, depth 2) == 2|E| is a GRAPH IDENTITY
    (backtracking walk <-> directed edge), verified on unrelated control graphs — so the
    IDENTIFICATION is structural, while the VALUE 718 is scene-specific (see mutations)."""
    def gap_of(adj):
        n = len(adj)
        w = sum(1 for a in range(n) for b in range(n) for c in range(n) if adj[a][b] and adj[b][c])
        nb = sum(1 for a in range(n) for b in range(n) for c in range(n)
                 if adj[a][b] and adj[b][c] and c != a)
        twoE = sum(adj[a][b] for a in range(n) for b in range(n))
        return (w - nb) == twoE

    graphs = {
        "P5 path": [[1 if abs(i - j) == 1 else 0 for j in range(5)] for i in range(5)],
        "C6 cycle": [[1 if (i - j) % 6 in (1, 5) else 0 for j in range(6)] for i in range(6)],
        "K1,4 star": [[1 if (i == 0) != (j == 0) else 0 for j in range(5)] for i in range(5)],
        "K4": [[1 if i != j else 0 for j in range(4)] for i in range(4)],
        "Petersen-ish (C5 x K2 join sample)": None,
    }
    graphs.pop("Petersen-ish (C5 x K2 join sample)")
    ok = all(gap_of(adj) for adj in graphs.values())
    if verbose:
        print(f"  [E2-prov] gap == 2|E| on control graphs {list(graphs)}: {ok}")
    return ok


def check_R5(verbose=True):
    """R5 retype (constant only; NO alpha-seam claim): 1/(3 ln phi) = 1/ln(phi^3) — the reciprocal
    log of the critical Perron rate phi^3 named by D0-ALPHA-PRESENT-CORE-MAXIMALITY-NOGO-001; with
    the owned I_f = ln phi (D0-FIBONACCI-IF-FORCING-001 / D0-IF-KS-FORMULA-FIX-001, MECH-LIMIT) it
    reads 1/(3 I_f). Decision = symbolic identity; numeric convergence is illustration + controls."""
    phi = (1 + math.sqrt(5)) / 2
    ok = True
    # symbolic: 3 ln phi == ln(phi^3) (log law; float smoke test at 1e-14)
    ident = abs(3 * math.log(phi) - math.log(phi ** 3)) < 1e-13
    ok &= ident
    if verbose:
        print(f"  [R5] 3*ln(phi) == ln(phi^3) (log law, smoke 1e-13): {ident}")

    def log_cesaro(base, a, K):
        """Ordinary log-Cesaro partial value for a tower with multiplicity m_N = round(base^{a*N})
        and singular value s = base^{-3N} per block, through block K:
        (sum of s_j over j) / ln(number of terms)."""
        tot_s, tot_n = 0.0, 0.0
        for N in range(1, K + 1):
            m = round(base ** (a * N))
            tot_s += m * base ** (-3 * N)
            tot_n += m
        return tot_s / math.log(tot_n)

    v30, v40 = log_cesaro(phi, 3, 30), log_cesaro(phi, 3, 40)
    target = 1 / (3 * math.log(phi))
    conv = abs(v40 - target) < abs(v30 - target) and abs(v40 - target) < 0.01
    ok &= conv
    if verbose:
        print(f"  [R5] critical tower a=3: partials {v30:.6f} -> {v40:.6f} -> 1/(3 ln phi) = {target:.6f}: {conv}")
    # control 1 (fails the conclusion for subcritical): a=2 partials head to 0, not the constant
    w30, w40 = log_cesaro(phi, 2, 30), log_cesaro(phi, 2, 40)
    sub = w40 < w30 and w40 < 0.05
    ok &= sub
    if verbose:
        print(f"  [R5] control a=2 (trace-class): partials {w30:.6f} -> {w40:.6f} -> 0 (NOT the constant): {sub}")
    # control 2 (identification tracks ln(rate), not the number): base-2 tower -> 1/(3 ln 2)
    u25, u35 = log_cesaro(2.0, 3, 25), log_cesaro(2.0, 3, 35)
    t2 = 1 / (3 * math.log(2))
    trk = abs(u35 - t2) < abs(u25 - t2) and abs(u35 - t2) < 0.01 and abs(t2 - target) > 0.2
    ok &= trk
    if verbose:
        print(f"  [R5] control base-2 tower: partials -> {u35:.6f} vs 1/(3 ln 2) = {t2:.6f}"
              f" != 1/(3 ln phi): {trk}")
    # RESTATEMENT of the row-464 conclusion (limit != mu2 = 12288/5) — NOT a new check
    # (skeptic #1 relabel: decorative by design). Recorded only to document that this retype
    # makes no mu2/alpha-seam claim; the seam stays CLOSED per ALPHA_SEAM_NOGO_V2.md.
    guard = abs(target - 12288 / 5) > 1
    ok &= guard
    if verbose:
        print(f"  [R5] row-464 conclusion restated (decorative): retyped constant {target:.6f}"
              f" != mu2=2457.6; no seam object touched: {guard}")
    return ok


# --------------------------------------------------------------------------- mutation harness
def mutations():
    """Each mutation must make its check FAIL — proves the checks can fail their CONCLUSIONS."""
    muts = []

    # R1: degenerate zone sizes + the extra swap automorphism -> commutant is NOT 12-dim M3+C^3
    def m_r1():
        cd = commutant_data((9, 9, 13), add_swap01=True)
        return cd["n_orb"] == 12  # must be False (it is 7)
    muts.append(("R1 conclusion fails on K(9,9,13)+swap (orbit count != 12)", m_r1))

    def m_r1b():
        # M3-fullness fails under the swap: pi_gen images cannot span all of M3
        cd = commutant_data((9, 9, 13), add_swap01=True)
        coords = []
        for B in cd["basis"]:
            pg = pi_gen(B, cd["zone"], (9, 9, 13))
            if pg is None:
                return True  # unexpected; treat as not-failing
            coords.append([pg[i][j] for i in range(3) for j in range(3)])
        return rank_exact(coords) == 9  # must be False
    muts.append(("R1 M3-fullness fails on K(9,9,13)+swap (rank < 9)", m_r1b))

    # E1: wrong formula p^2+q^2+2 must be rejected by the computed centralizer dims
    def m_e1():
        cd = commutant_data((9, 11, 13))
        n, sizes = cd["n"], (9, 11, 13)

        def gamma(signs):
            G = [[Fraction(0)] * n for _ in range(n)]
            off = 0
            for z, s in enumerate(sizes):
                for i in range(off, off + s):
                    for j in range(off, off + s):
                        G[i][j] += Fraction(signs[z] - 1, s)
                        if i == j:
                            G[i][j] += 1
                off += s
            return G
        d = centralizer_dim(cd["basis"], gamma((1, 1, -1)))
        return d == 2 * 2 + 1 * 1 + 2  # wrong formula (+2): must be False
    muts.append(("E1 wrong formula p^2+q^2+2 rejected by computed dim", m_e1))

    # CAP/E2/R3: mutated scene K(9,11,15) -> constants move off (718, 15708, 14990, 718/33)
    def m_cap():
        return check_capacity((9, 11, 15), expect={
            "C": 718, "W2": 15708, "NB2": 14990, "ratio": (718, 33),
            "degs": [24, 22, 20], "spec": {0: 1, 20: 12, 22: 10, 24: 8, 33: 2}}, verbose=False)
    muts.append(("CAP pins fail on K(9,11,15) (all four constants move)", m_cap))

    # E2 identification: gap == |E| (the WRONG identification) must fail on the frozen scene
    def m_e2():
        zone, A, deg = scene((9, 11, 13))
        n = len(zone)
        w = sum(1 for a in range(n) for b in range(n) for c in range(n) if A[a][b] and A[b][c])
        nb = sum(1 for a in range(n) for b in range(n) for c in range(n)
                 if A[a][b] and A[b][c] and c != a)
        E = sum(deg) // 2
        return (w - nb) == E  # gap == |E| is FALSE (gap == 2|E|)
    muts.append(("E2 wrong identification gap==|E| rejected", m_e2))

    # R3: a scene with mean degree BELOW phi^3 (e.g. C6 cycle, mean degree 2) must fail the floor
    def m_r3():
        ratio = Fraction(2)  # mean degree of any 2-regular graph
        r2 = ratio - 2
        return (ratio > 2) and (r2 * r2 > 5)  # False
    muts.append(("R3 floor fails for a mean-degree-2 carrier (2 < phi^3)", m_r3))

    # R5: wrong retype 1/(2 ln phi) must NOT match the critical-tower limit
    def m_r5():
        phi = (1 + math.sqrt(5)) / 2
        tot_s, tot_n = 0.0, 0.0
        for N in range(1, 41):
            m = round(phi ** (3 * N))
            tot_s += m * phi ** (-3 * N)
            tot_n += m
        val = tot_s / math.log(tot_n)
        return abs(val - 1 / (2 * math.log(phi))) < 0.01  # wrong constant: must be False
    muts.append(("R5 wrong retype 1/(2 ln phi) rejected by the tower limit", m_r5))

    return muts


# --------------------------------------------------------------------------- main
def main() -> int:
    print("=== W2 quantity-identification check — cluster J (R1, R2, R3, R5, E1, E2) ===")
    print("All decisions exact (int/Fraction) except the R5 convergence illustration.")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: every object is built from the zone sizes (9,11,13);")
    print("no corpus constant enters its own construction (pins compare only).")
    ok = True

    print("\n-- R1: commutant = M3(+)C(+)C(+)C with M3 = End(generation space) --")
    r1 = check_R1()
    print(f"  R1 RESULT: {'PASS' if r1 else 'FAIL'}")
    ok &= r1

    print("\n-- E1: nc(p,q) = p^2+q^2+3 = graded-commutant dimension --")
    e1 = check_E1()
    print(f"  E1 RESULT: {'PASS' if e1 else 'FAIL'}")
    ok &= e1

    print("\n-- R2/R3/E2/REHEATING: the capacity block (one quantity, four faces) --")
    cap = check_capacity(expect={
        "C": 718, "W2": 15708, "NB2": 14990, "ratio": (718, 33),
        "degs": [24, 22, 20], "spec": {0: 1, 20: 12, 22: 10, 24: 8, 33: 2}})
    print(f"  CAP RESULT: {'PASS' if cap else 'FAIL'}")
    ok &= cap

    print("\n-- E2 provenance: gap == 2|E| is a graph identity (controls) --")
    prov = check_gap_identity_universal()
    print(f"  E2-PROV RESULT: {'PASS' if prov else 'FAIL'}")
    ok &= prov

    print("\n-- R5: retype 1/(3 ln phi) = 1/ln(phi^3) (constant only; seam untouched) --")
    r5 = check_R5()
    print(f"  R5 RESULT: {'PASS' if r5 else 'FAIL'}")
    ok &= r5

    print("\n-- MUTATION TESTS (each targeted wrong input must make its check FAIL) --")
    all_fired = True
    for name, m in mutations():
        fired = not m()
        all_fired &= fired
        print(f"  {'FIRES' if fired else 'DEAD '}  {name}")
    ok &= all_fired

    print(f"\nRESULT: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
