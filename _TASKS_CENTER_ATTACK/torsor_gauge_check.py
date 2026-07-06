#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
torsor_gauge_check.py — computational companion to TORSOR_GAUGE_SYNTHESIS_MEMO.md
(center-attack BREAKTHROUGH-SYNTHESIS pass, 2026-07-05).

CLAIM UNDER TEST (candidate, DRAFT v2 — DEMOTED per skeptic #1 from "derived
gauge principle" to ORGANIZING LEMMA / reading layer over C1 + row 549 + M2):
the M1 selector no-go (D0-CANONICAL-WITHIN-ZONE-SELECTOR-M1-NOGO-001) + the M2
torsor (D0-M2-PHASE-LABELING-V9-SHELL-001) have the structure of a gauge-fixing
impossibility, and the import ledger is FOUR-typed:

  T. the within-zone labelings of K(9,11,13) form a principal homogeneous space
     (torsor) under G = S9 x S11 x S13 = Aut(K(9,11,13)); the owned Q8-typing on
     the detector-layer shell V9 is a REDUCTION of the zone-9 structure group
     S9 -> Stab(omega0)=S8 (both rungs OWNED) -> G_res in {(Z/2)^3, V4, 1}
     (rungs BELOW S8 are READING-CONDITIONAL: R-weak/mid/strong is 3-way OPEN,
     M2 memo A3); "no canonical selector" = "no canonical (equivariant) global
     section".
  A. class A (invariant under the DECLARED group AND determined by frozen
     data): rank/nullity, counts, isotype multiplicity, tick fingerprint
     {80/81, -1/9}, delay weight 8/9, traces, lepton resolvent skeleton,
     seam-moment arithmetic — computed here.
  C. class C (point-choice on an OWNED torsor = gauge-fixing): per-slot values,
     membership, block->generation assignment, per-slot hypercharge attachment
     — computed negatives.
  D. class D (choice of UN-OWNED ansatz/reduction structure — NOT gauge-fixing,
     NOT contentless): the cyclic-order datum behind cos(pi/9). Its value is
     family-canonical across the ansatz class but conditional on structure the
     scene does not own (row 544) — check D1 computes both facts. Skeptic #1's
     strongest finding: conflating C and D was the v1 soundness gap.
  B. class B (invariant under the declared group but UNDETERMINED), sub-typed
     B-meas (experimental number) / B-adj (open internal adjudication) /
     B-ext (corpus-typed NEW primitive/extension). The CKM completion is B-ext
     per its own row ("a canonical selector ... is a NEW primitive (extension),
     not a present-core theorem"); the 16/25 vs 144/169 arithmetic is that
     row's Lean-proved content, REPRODUCED (not owned) in check C4; the
     common-rotation "gauge half" of C4 is an ILLUSTRATION of the un-minted
     commutant-layer extension (memo risk R3), not a scene-torsor fact.

Negative controls (each can fail the CONCLUSION, not the technique):
  N1: C1 broken (distinct vertex weights) => a canonical selector EXISTS
      (the gauge principle is contingent on C1, not a tautology).
  N2: equal parts K(2,2) => Aut strictly larger than S2xS2 (part swap); the
      gauge group is computed from the scene, not assumed.
  N3: a 6/3 sign split gives 72/81 != 80/81 (fingerprint discriminates).
  N4: a non-equivariant ingredient breaks the invariance lemma (hypothesis
      load-bearing).

Exact arithmetic (fractions.Fraction / int) everywhere load-bearing; floats
appear ONLY in the U3-comparator and cos(pi/9) corroboration checks, labelled
FLOAT-CORROBORATION.

Frozen inputs: the scene K(9,11,13) (BOOK_01 §01.20, C1 at BOOK_01:1570);
V9 = Omega8 ⊔ {omega0} with Omega8 ≅ Q8 (BOOK_01:782); Feshbach split
P = proj(range A), Q = proj(ker A) (tick owner; TICK_COUPLING_SCHUR_MEMO.md).
No quantity is constructed from the conclusion: transported and untransported
values are computed independently and compared.
"""

import sys, random, itertools
from fractions import Fraction as Fr

random.seed(20260705)

PASS = []
FAIL = []

def check(name, ok, detail=""):
    (PASS if ok else FAIL).append(name)
    print(("PASS " if ok else "FAIL ") + name + ((" — " + detail) if detail else ""))

# ----------------------------------------------------------------------------
# exact linear algebra over Fraction
# ----------------------------------------------------------------------------

def mat(rows):
    return [[Fr(x) for x in r] for r in rows]

def zeros(n, m):
    return [[Fr(0)] * m for _ in range(n)]

def eye(n):
    return [[Fr(1) if i == j else Fr(0) for j in range(n)] for i in range(n)]

def mmul(A, B):
    n, k, m = len(A), len(B), len(B[0])
    Bt = list(zip(*B))
    return [[sum(A[i][t] * Bt[j][t] for t in range(k)) for j in range(m)] for i in range(n)]

def madd(A, B, sb=Fr(1)):
    return [[A[i][j] + sb * B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def msub(A, B):
    return madd(A, B, Fr(-1))

def mscale(A, s):
    return [[s * x for x in r] for r in A]

def transpose(A):
    return [list(r) for r in zip(*A)]

def frob2(A):
    return sum(x * x for r in A for x in r)

def mat_eq(A, B):
    return all(A[i][j] == B[i][j] for i in range(len(A)) for j in range(len(A[0])))

def is_zero(A):
    return all(x == 0 for r in A for x in r)

def perm_matrix(p):
    n = len(p)
    M = zeros(n, n)
    for i in range(n):
        M[p[i]][i] = Fr(1)          # column i -> row p[i]:  (M v)_{p(i)} = v_i
    return M

def conj_by_perm(M, p):
    """g M g^{-1} for the permutation matrix g of p (exact)."""
    n = len(M)
    out = zeros(n, n)
    for i in range(n):
        for j in range(n):
            out[p[i]][p[j]] = M[i][j]
    return out

def rank_frac(A):
    """exact rank by Gaussian elimination over Q."""
    M = [row[:] for row in A]
    n, m = len(M), len(M[0])
    r = 0
    for c in range(m):
        piv = next((i for i in range(r, n) if M[i][c] != 0), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        inv = Fr(1) / M[r][c]
        M[r] = [x * inv for x in M[r]]
        for i in range(n):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [M[i][j] - f * M[r][j] for j in range(m)]
        r += 1
        if r == n:
            break
    return r

# ----------------------------------------------------------------------------
# the frozen scene
# ----------------------------------------------------------------------------

Z9 = list(range(0, 9))
Z11 = list(range(9, 20))
Z13 = list(range(20, 33))
ZONES = [Z9, Z11, Z13]
N = 33

def scene_adjacency():
    A = zeros(N, N)
    for a, b in itertools.combinations(range(3), 2):
        for i in ZONES[a]:
            for j in ZONES[b]:
                A[i][j] = Fr(1)
                A[j][i] = Fr(1)
    return A

A = scene_adjacency()

# P = projector onto range(A) = zone-constant vectors; Q = I - P (ker A).
def proj_P():
    P = zeros(N, N)
    for zone in ZONES:
        n = len(zone)
        for i in zone:
            for j in zone:
                P[i][j] = Fr(1, n)
    return P

P = proj_P()
Q = msub(eye(N), P)

def random_zone_perm():
    """random element of S9 x S11 x S13 as a permutation of range(33)."""
    p = list(range(N))
    for zone in ZONES:
        img = zone[:]
        random.shuffle(img)
        for src, dst in zip(zone, img):
            p[src] = dst
    return p

# ----------------------------------------------------------------------------
# SECTION T — the gauge structure is exact (bundle data, torsor, reduction)
# ----------------------------------------------------------------------------
print("\n== SECTION T: bundle/torsor structure ==")

# T1: C1 holds computationally: g A g^{-1} = A for 20 random g in G, and g
# commutes with P and Q (so G acts on the frozen Feshbach split).
ok = True
for _ in range(20):
    g = random_zone_perm()
    if not mat_eq(conj_by_perm(A, g), A):
        ok = False
    if not mat_eq(conj_by_perm(P, g), P):
        ok = False
check("T1_C1_invariance_gAg=A_and_gP=Pg", ok,
      "20 random g in S9xS11xS13: gAg^-1=A and gPg^-1=P exactly")

# T2: within-zone labelings form a G-torsor: the action is free and transitive
# with a UNIQUE transporter (simply transitive).  A labeling of zone Vn is a
# bijection Vn -> Ln; Sn acts by post/pre-composition; two labelings differ by
# exactly one group element.
def compose(p, q):          # (p*q)(i) = p[q[i]]
    return [p[q[i]] for i in range(len(p))]

def inv_perm(p):
    q = [0] * len(p)
    for i, v in enumerate(p):
        q[v] = i
    return q

ok = True
for n in (9, 11, 13):
    b1 = list(range(n)); random.shuffle(b1)
    b2 = list(range(n)); random.shuffle(b2)
    # transporter g with b2 = b1 o g  =>  g = b1^{-1} o b2 ; uniqueness = freeness
    g = compose(inv_perm(b1), b2)
    if compose(b1, g) != b2:
        ok = False
    # freeness: b1 o h = b1 forces h = id (checked on 5 random non-identity h)
    for _ in range(5):
        h = list(range(n)); random.shuffle(h)
        if h == list(range(n)):
            continue
        if compose(b1, h) == b1:
            ok = False
check("T2_labelings_are_G_torsor", ok,
      "transitive with unique transporter; free (n=9,11,13)")

# T3: no equivariant global section.  Ground truth by enumeration for n<=4,
# structural identity for the scene sizes: b o g = b  <=>  g = id.
ok = True
for n in (2, 3, 4):
    fixed = 0
    for b in itertools.permutations(range(n)):
        if all(tuple(b[g[i]] for i in range(n)) == b
               for g in map(list, itertools.permutations(range(n)))):
            fixed += 1
    if fixed != 0:
        ok = False
# n=1 control: exactly one (a section exists when the torsor is trivial)
fixed1 = sum(1 for b in itertools.permutations(range(1)))
if fixed1 != 1:
    ok = False
# scene sizes: composing b o g = b with b^{-1} gives g = id; witnessed on
# 50 random (g != id, b) pairs for n = 9, 11, 13
for n in (9, 11, 13):
    for _ in range(50):
        g = list(range(n)); random.shuffle(g)
        if g == list(range(n)):
            continue
        b = list(range(n)); random.shuffle(b)
        if compose(b, g) == b:
            ok = False
check("T3_no_equivariant_section", ok,
      "0 fixed labelings for n=2,3,4 (enumerated); 1 for n=1; free action at 9/11/13")

# T4: the owned Q8-typing is a REDUCTION OF STRUCTURE GROUP on zone 9:
#   S9 (362880)  ⊃ Stab(omega0)=S8 (40320)      [both rungs OWNED]
#   ⊃ R-weak (Z/2)^3 (8) ⊃ R-mid V4 (4) ⊃ R-strong 1
#     [rungs below S8 READING-CONDITIONAL: which one is G_res depends on the
#      un-adjudicated R-weak/mid/strong reading (M2 memo A3, 3-way OPEN); the
#      script computes all three CANDIDATE rungs and their subgroup chain]
# licensing data: omega0 marked witness BOOK_01:1541 (owned); typed axes +
# group structure BOOK_01:782,1530 (binds under R-weak or stronger); Hamilton
# ijk=-1 as role fact BOOK_01:824 (binds under R-mid or stronger); act/undo
# section BOOK_01:1539 (binds under R-strong only).
# Q8 as integer quaternion 4-tuples.
Q8 = {
    '1': (1, 0, 0, 0), '-1': (-1, 0, 0, 0),
    'i': (0, 1, 0, 0), '-i': (0, -1, 0, 0),
    'j': (0, 0, 1, 0), '-j': (0, 0, -1, 0),
    'k': (0, 0, 0, 1), '-k': (0, 0, 0, -1),
}
Q8elems = list(Q8.values())

def qmul(a, b):
    a0, a1, a2, a3 = a
    b0, b1, b2, b3 = b
    return (a0*b0 - a1*b1 - a2*b2 - a3*b3,
            a0*b1 + a1*b0 + a2*b3 - a3*b2,
            a0*b2 - a1*b3 + a2*b0 + a3*b1,
            a0*b3 + a1*b2 - a2*b1 + a3*b0)

AXES = {'A': [Q8['1'], Q8['-1']], 'B': [Q8['i'], Q8['-i']],
        'C': [Q8['j'], Q8['-j']], 'D': [Q8['k'], Q8['-k']]}

def axis_flip_map(eps):     # eps = dict axis -> +-1
    m = {}
    for ax, pair in AXES.items():
        plus, minus = pair
        if eps[ax] == 1:
            m[plus] = plus; m[minus] = minus
        else:
            m[plus] = minus; m[minus] = plus
    return m

def is_group_hom(m):
    return all(m[qmul(x, y)] == qmul(m[x], m[y]) for x in Q8elems for y in Q8elems)

# full Aut(Q8) by brute force over bijections fixing the identity
idq = Q8['1']
others = [e for e in Q8elems if e != idq]
auts = 0
inns = set()
for perm in itertools.permutations(others):
    m = {idq: idq}
    m.update(dict(zip(others, perm)))
    if is_group_hom(m):
        auts += 1
for g in Q8elems:
    gi = next(e for e in Q8elems if qmul(g, e) == idq)
    inns.add(tuple(sorted((x, qmul(qmul(g, x), gi)) for x in Q8elems)))
check("T4a_AutQ8_24_Inn_4", auts == 24 and len(inns) == 4,
      "Aut(Q8)=%d (=24), Inn(Q8)=%d (=4, V4)" % (auts, len(inns)))

# the 16 axis-preserving sign maps: which are admissible under each reading
weak = mid = strong = 0
weak_maps, mid_maps = [], []
for bits in itertools.product((1, -1), repeat=4):
    eps = dict(zip('ABCD', bits))
    m = axis_flip_map(eps)
    # R-weak: group structure up to iso pins the A axis pointwise (identity is
    # structurally unique; -1 the unique order-2 element) => eps_A = +1
    if eps['A'] == 1:
        weak += 1
        weak_maps.append(m)
        # R-mid: Hamilton ijk = -1 owned as a ROLE fact:
        # (eB i)(eC j)(eD k) = eB eC eD (ijk) = -1  <=>  eB*eC*eD = +1
        if eps['B'] * eps['C'] * eps['D'] == 1:
            mid += 1
            mid_maps.append(m)
            if bits == (1, 1, 1, 1):
                strong += 1
# the admissible-map sets are groups and form ONE orbit on labelings (torsor):
# closure under composition suffices for these abelian flip sets
def maps_closed(maps):
    keyset = {tuple(sorted(m.items())) for m in maps}
    for m1 in maps:
        for m2 in maps:
            comp = {x: m1[m2[x]] for x in Q8elems}
            if tuple(sorted(comp.items())) not in keyset:
                return False
    return True

check("T4b_reduction_chain_orders",
      weak == 8 and mid == 4 and strong == 1
      and maps_closed(weak_maps) and maps_closed(mid_maps),
      "S9(362880) > S8(40320) [owned] > candidate rungs (Z/2)^3(%d) > V4(%d) > "
      "1(%d) [reading-conditional, G_res 3-way OPEN]; flip sets closed"
      % (weak, mid, strong))

# T4c: the 4 admissible R-mid maps are exactly the automorphisms among the
# axis-preserving flips (= Inn(Q8) as permutation action): the owned Hamilton
# role fact and the group law select the SAME V4.
auto_flips = sum(1 for m in weak_maps if is_group_hom(m))
mid_are_homs = all(is_group_hom(m) for m in mid_maps)
check("T4c_Rmid_equals_flip_automorphisms", auto_flips == 4 and mid_are_homs,
      "axis-preserving flip automorphisms = 4 = R-mid set (Inn action)")

# ----------------------------------------------------------------------------
# SECTION A — the invariant ring (class A: gauge-invariant AND determined)
# every value computed from frozen data, then re-computed after 20 random
# torsor relabelings and compared EXACTLY.
# ----------------------------------------------------------------------------
print("\n== SECTION A: invariant ring (class A) ==")

GS = [random_zone_perm() for _ in range(20)]

# A1: rank/nullity and the quotient characteristic polynomial with the owned
# counts as coefficients: char(B) = x^3 - 359 x - 2574, 359 = cross edges,
# 2574 = 2 * 1287 triangles.
ok = rank_frac(A) == 3
# kernel: within-zone zero-sum vectors (30 independent) are annihilated
for zone in ZONES:
    for t in range(1, len(zone)):
        v = [Fr(0)] * N
        v[zone[0]] = Fr(1)
        v[zone[t]] = Fr(-1)
        Av = [sum(A[i][j] * v[j] for j in range(N)) for i in range(N)]
        if any(x != 0 for x in Av):
            ok = False
Bq = mat([[0, 11, 13], [9, 0, 13], [9, 11, 0]])
# char poly of 3x3 exactly: x^3 - tr x^2 + e2 x - det
tr = Bq[0][0] + Bq[1][1] + Bq[2][2]
e2 = (Bq[0][0]*Bq[1][1] - Bq[0][1]*Bq[1][0] + Bq[0][0]*Bq[2][2]
      - Bq[0][2]*Bq[2][0] + Bq[1][1]*Bq[2][2] - Bq[1][2]*Bq[2][1])
det = (Bq[0][0]*(Bq[1][1]*Bq[2][2] - Bq[1][2]*Bq[2][1])
       - Bq[0][1]*(Bq[1][0]*Bq[2][2] - Bq[1][2]*Bq[2][0])
       + Bq[0][2]*(Bq[1][0]*Bq[2][1] - Bq[1][1]*Bq[2][0]))
ok = ok and (tr == 0) and (e2 == Fr(-359)) and (det == Fr(2574))
check("A1_rank3_nullity30_charpoly_owned_counts", ok,
      "rank(A)=3; ker ⊇ 30-dim zero-sum space; char(Bq)=x^3-359x-2574 "
      "(359=cross edges, 2574=2*1287 triangles)")

# A2: counts computed from A and from every relabeled A agree exactly.
def count_edges(M):
    return sum(1 for i in range(N) for j in range(i + 1, N) if M[i][j] == 1)

def count_triangles(M):
    M2 = mmul(M, M)
    M3 = mmul(M2, M)
    trace = sum(M3[i][i] for i in range(N))
    return trace / 6

E0, T0 = count_edges(A), count_triangles(A)
ok = (E0 == 359 and T0 == 1287)
for g in GS[:5]:
    Ag = conj_by_perm(A, g)
    if count_edges(Ag) != E0 or count_triangles(Ag) != T0:
        ok = False
check("A2_counts_33_359_1287_invariant", ok,
      "edges=359, triangles=1287, invariant under relabeling")

# A3: trivial-isotype multiplicity = dim of G-fixed subspace = 3 (exact):
# stack (g - I) over per-zone cycle+transposition generators; nullity = 3.
def gen_perms():
    gens = []
    for zone in ZONES:
        cyc = list(range(N))
        for t, v in enumerate(zone):
            cyc[v] = zone[(t + 1) % len(zone)]
        gens.append(cyc)
        tr_ = list(range(N))
        tr_[zone[0]], tr_[zone[1]] = tr_[zone[1]], tr_[zone[0]]
        gens.append(tr_)
    return gens

stack = []
for g in gen_perms():
    Pg = perm_matrix(g)
    D = msub(Pg, eye(N))
    stack.extend(D)
nullity = N - rank_frac(stack)
check("A3_trivial_isotype_multiplicity_3", nullity == 3,
      "dim fixed subspace = %d (= generation count = rank A)" % nullity)

# A4: the tick fingerprint (M2 consumers): all four owned carriers give
# ||PUQ||_F^2 = 80/81 and exact ladder ratio -1/9; delay weight 8/9;
# rho(QUQ)=1 with the eigenvalue-1 directions orthogonal to the ladder;
# all EXACT and torsor-invariant.
# zone-9 slot order: [omega0, 1, -1, i, -i, j, -j, k, -k]
CHI = {
    'chi_B': [1,  1, 1,  1, 1, -1, -1, -1, -1],
    'chi_C': [1,  1, 1, -1, -1, 1, 1, -1, -1],
    'chi_D': [1,  1, 1, -1, -1, -1, -1, 1, 1],
    's_act': [1,  1, -1, 1, -1, 1, -1, 1, -1],
}

def carrier(d9):
    U = eye(N)
    for t, v in enumerate(Z9):
        U[v][v] = Fr(d9[t])
    return U

def fingerprint(U):
    PUQ = mmul(mmul(P, U), Q)
    QUP = mmul(mmul(Q, U), P)
    QUQ = mmul(mmul(Q, U), Q)
    f2 = frob2(PUQ)
    t0 = mmul(PUQ, QUP)
    t1 = mmul(PUQ, mmul(QUQ, QUP))
    t2 = mmul(PUQ, mmul(QUQ, mmul(QUQ, QUP)))
    return f2, t0, t1, t2

ok = True
details = []
for name, d9 in CHI.items():
    s = sum(d9)
    f2, t0, t1, t2 = fingerprint(carrier(d9))
    closed = Fr(81 - s * s, 81)
    # ladder ratio: t1 = r * t0 entrywise with r = -1/9 (sign from s=+1)
    r = None
    for i in range(N):
        for j in range(N):
            if t0[i][j] != 0:
                r = t1[i][j] / t0[i][j]
                break
        if r is not None:
            break
    ratio_ok = (r == Fr(-1, 9)) and mat_eq(t1, mscale(t0, r)) \
               and mat_eq(t2, mscale(t0, r * r))
    # z=1 delay weight = f2 * 1/(1 - r) = (80/81)*(9/10) = 8/9
    weight = f2 / (1 - r) if r is not None else None
    ok = ok and (f2 == Fr(80, 81) == closed) and ratio_ok and (weight == Fr(8, 9))
    details.append("%s: |PUQ|^2=%s ratio=%s weight=%s" % (name, f2, r, weight))
check("A4a_fingerprint_80_81_ratio_-1_9_weight_8_9", ok, "; ".join(details[:2]) + " ...")

# rho(QUQ) = 1, witnessed off the ladder: ONE explicit eigenvalue-1 direction
# (a zone-11 zero-sum vector) is exhibited and shown ORTHOGONAL to the ladder
# columns (range QUP and range QUQ*QUP), computed exactly.  SINGLE-WITNESS
# statement, not a full spectral decomposition (skeptic #1 repair: v1 wording
# overstated; the dead `*0` control line — content-free, always true — is
# REPLACED by the realized orthogonality computation: script EoR-S3).
U = carrier(CHI['chi_B'])
QUQ = mmul(mmul(Q, U), Q)
v = [Fr(0)] * N
v[Z11[0]], v[Z11[1]] = Fr(1), Fr(-1)
Qv = [sum(QUQ[i][j] * v[j] for j in range(N)) for i in range(N)]
QUP = mmul(mmul(Q, U), P)
QUQ_QUP = mmul(QUQ, QUP)
ortho1 = all(sum(v[i] * QUP[i][j] for i in range(N)) == 0 for j in range(N))
ortho2 = all(sum(v[i] * QUQ_QUP[i][j] for i in range(N)) == 0 for j in range(N))
col_touch = any(QUP[i][j] != 0 for i in Z11 for j in range(N))
check("A4b_rho1_single_witness_off_ladder",
      Qv == v and ortho1 and ortho2 and not col_touch,
      "one zone-11 zero-sum direction: QUQ-fixed (eigenvalue 1), exactly "
      "orthogonal to ladder columns (v^T QUP = v^T QUQ QUP = 0), no zone-11 "
      "support in QUP")

# omega0-extension bit (NAMED, not owned): flipping chi(omega0) keeps 80/81,
# flips the ratio sign, moves the weight 8/9 -> 10/9 (both computed).
d9v = CHI['chi_B'][:]
d9v[0] = -1
f2v, t0v, t1v, _ = fingerprint(carrier(d9v))
rv = None
for i in range(N):
    for j in range(N):
        if t0v[i][j] != 0:
            rv = t1v[i][j] / t0v[i][j]
            break
    if rv is not None:
        break
check("A4c_omega0_bit_quantified", f2v == Fr(80, 81) and rv == Fr(1, 9)
      and f2v / (1 - rv) == Fr(10, 9),
      "flip: |PUQ|^2=80/81 kept, ratio=+1/9, weight=10/9")

# A4d: TORSOR INVARIANCE of the fingerprint: for 20 random g the relabeled
# carrier U' = gUg^-1 gives the SAME exact (80/81, -1/9, 8/9).
ok = True
for g in GS:
    Ug = conj_by_perm(carrier(CHI['chi_C']), g)
    f2g, t0g, t1g, _ = fingerprint(Ug)
    rg = None
    for i in range(N):
        for j in range(N):
            if t0g[i][j] != 0:
                rg = t1g[i][j] / t0g[i][j]
                break
        if rg is not None:
            break
    if f2g != Fr(80, 81) or rg != Fr(-1, 9):
        ok = False
check("A4d_fingerprint_torsor_invariant", ok,
      "20 random relabelings: exact (80/81, -1/9) unchanged")

# A5: power traces (heat-trace/spectral-action germs) exact and invariant.
A2m = mmul(A, A)
A3m = mmul(A2m, A)
A4m = mmul(A3m, A)
tr2 = sum(A2m[i][i] for i in range(N))
tr3 = sum(A3m[i][i] for i in range(N))
tr4 = sum(A4m[i][i] for i in range(N))
ok = (tr2 == 718 and tr3 == 7722)
for g in GS[:3]:
    Ag = conj_by_perm(A, g)
    B2 = mmul(Ag, Ag)
    if sum(B2[i][i] for i in range(N)) != tr2:
        ok = False
check("A5_power_traces_invariant", ok,
      "Tr A^2=718=2*359, Tr A^3=7722=6*1287, Tr A^4=%s; invariant" % tr4)

# A6: the general invariance lemma exercised: any word in {A, P, Q} with
# random rational coefficients has torsor-invariant trace / Frobenius data.
ok = True
for trial in range(10):
    c1, c2, c3 = (Fr(random.randint(-5, 5), random.randint(1, 7)) for _ in range(3))
    W = madd(madd(mscale(A, c1), mscale(mmul(A, A), c2)), mscale(P, c3))
    trW = sum(W[i][i] for i in range(N))
    fW = frob2(W)
    g = GS[trial % len(GS)]
    Wg = conj_by_perm(W, g)
    if sum(Wg[i][i] for i in range(N)) != trW or frob2(Wg) != fW:
        ok = False
check("A6_invariance_lemma_words", ok,
      "10 random words in {A, A^2, P}: trace+Frobenius invariant exactly")

# A7: seam-moment arithmetic (cross-ref, NOT re-derived): mu2 = 12288/5 =
# 2^12 * rho with rho = Z/D_Sigma = 3/5 (ALPHA_SEAM_NOGO_V2.md); mu1 = 1/3.
# The gauge point: these are traces over the P/Q split of scene-derived
# operators => class functions => torsor-invariant BY THE LEMMA (A6);
# their VALUES are owned by their certs, only the arithmetic identity is
# verified here.
rho = Fr(3, 5)
check("A7_seam_moment_arithmetic", Fr(12288, 5) == Fr(2) ** 12 * rho,
      "mu2 = 12288/5 = 2^12 * rho, rho = 3/5 (identity only; owner: alpha certs)")

# A8: lepton skeleton (shell-torus, 7 points): det(I - zU) = (1-z^4)(1-z^3);
# order 12; (4,3) the unique order-12 cycle type among the 15 partitions of 7.
# All conjugation-invariant (type data).
def poly_mul(p, q):
    out = [0] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i + j] += a * b
    return out

def det_I_minus_zU(perm):
    # product over cycles of (1 - z^len)
    seen = [False] * len(perm)
    poly = [1]
    for i in range(len(perm)):
        if not seen[i]:
            ln = 0
            j = i
            while not seen[j]:
                seen[j] = True
                j = perm[j]
                ln += 1
            cyc = [1] + [0] * (ln - 1) + [-1]
            poly = poly_mul(poly, cyc)
    return poly

sigmaA = [1, 2, 3, 0, 5, 6, 4]        # (0123)(456)
polyA = det_I_minus_zU(sigmaA)
target = poly_mul([1, 0, 0, 0, -1], [1, 0, 0, -1])   # (1-z^4)(1-z^3)
from math import lcm
def partitions(n, mx=None):
    if mx is None:
        mx = n
    if n == 0:
        yield []
        return
    for k in range(min(n, mx), 0, -1):
        for rest in partitions(n - k, k):
            yield [k] + rest

order12types = [p for p in partitions(7) if lcm(*p) == 12]
npart = sum(1 for _ in partitions(7))
ok = (polyA == target and order12types == [[4, 3]] and npart == 15)
# invariance under S7 conjugation
for _ in range(10):
    h = list(range(7)); random.shuffle(h)
    hin = inv_perm(h)
    sig_g = [h[sigmaA[hin[t]]] for t in range(7)]
    if det_I_minus_zU(sig_g) != target:
        ok = False
check("A8_lepton_skeleton_type_invariant", ok,
      "det(I-zU)=(1-z^4)(1-z^3); (4,3) unique order-12 type of 15; conj-invariant")

# ----------------------------------------------------------------------------
# SECTION C — the gauge-dependent boundary (class C) and the class-B separation
# ----------------------------------------------------------------------------
print("\n== SECTION C: gauge variables (class C) and class-B separation ==")

# C1: per-slot values are NOT torsor-invariant: exhibit g moving a -1 onto a
# +1 slot of chi_B; the -1-support SET moves too (membership is gauge).
Uc = carrier(CHI['chi_B'])
g = list(range(N))
g[Z9[3]], g[Z9[5]] = g[Z9[5]], g[Z9[3]]        # swap i-slot (+1) with j-slot (-1)
Ug = conj_by_perm(Uc, g)
slot = Z9[3]
check("C1_per_slot_value_not_invariant",
      Uc[slot][slot] == 1 and Ug[slot][slot] == -1,
      "slot %d: value +1 -> -1 under an admissible relabeling" % slot)

# C2: the E-projector refinement exists ONLY on the REDUCED bundle:
# E3 (rank 3, chi-span) is invariant under every G_res flip (all readings)
# but moves under generic S8 relabelings of the shell.
# Build E0/E3/E4 on the 8 shell slots (indices Z9[1..8] in the fixed order).
shell = Z9[1:]
chiB8 = [1, 1, 1, 1, -1, -1, -1, -1]     # on [1,-1,i,-i,j,-j,k,-k]
chiC8 = [1, 1, -1, -1, 1, 1, -1, -1]
chiD8 = [1, 1, -1, -1, -1, -1, 1, 1]
one8 = [1] * 8

def outer_scaled(v, s):
    return [[Fr(v[i] * v[j], s) for j in range(8)] for i in range(8)]

E0m = outer_scaled(one8, 8)
E3m = madd(madd(outer_scaled(chiB8, 8), outer_scaled(chiC8, 8)), outer_scaled(chiD8, 8))
E4m = msub(msub(eye(8), E0m), E3m)
ok = mat_eq(mmul(E3m, E3m), E3m) and mat_eq(mmul(E0m, E0m), E0m) \
     and mat_eq(mmul(E4m, E4m), E4m) \
     and rank_frac(E0m) == 1 and rank_frac(E3m) == 3 and rank_frac(E4m) == 4
# flips act on shell slots as the 8 permutations swapping +- within axes B,C,D
flip_perms = []
for bits in itertools.product((0, 1), repeat=3):
    p = list(range(8))
    for axi, bit in enumerate(bits):
        if bit:
            a = 2 + 2 * axi
            p[a], p[a + 1] = p[a + 1], p[a]
    flip_perms.append(p)
for p in flip_perms:
    E3g = [[E3m[p[i]][p[j]] for j in range(8)] for i in range(8)]
    if not mat_eq(E3g, E3m):
        ok = False
# generic S8 relabelings move E3 (find at least 8/10 moving it; a fixed one is
# fine — the point is NON-invariance generically)
moved = 0
for _ in range(10):
    p = list(range(8)); random.shuffle(p)
    E3g = [[E3m[p[i]][p[j]] for j in range(8)] for i in range(8)]
    if not mat_eq(E3g, E3m):
        moved += 1
check("C2_reduction_buys_refinement", ok and moved >= 8,
      "E0/E3/E4 idempotent ranks (1,3,4); invariant under all 8 G_res flips; "
      "moved by %d/10 generic S8 relabelings" % moved)

# C3: block->generation assignment is a gauge point-choice: sigmaA and sigmaB
# (R4) are CONJUGATE (same invariants: order 12, type (4,3), same resolvent)
# but DIFFERENT maps — the invariant data cannot separate them.
sigmaB = [1, 2, 0, 4, 5, 6, 3]        # (012)(3456)
def perm_order(p):
    o = 1
    q = p[:]
    while q != list(range(len(p))):
        q = compose(p, q)
        o += 1
    return o
# explicit conjugator: map cycle structure of A onto B
# sigmaA cycles: (0 1 2 3)(4 5 6);  sigmaB cycles: (3 4 5 6)(0 1 2)
h = [3, 4, 5, 6, 0, 1, 2]
hin = inv_perm(h)
conj = [h[sigmaA[hin[t]]] for t in range(7)]
check("C3_branch_assignment_gauge",
      perm_order(sigmaA) == 12 and perm_order(sigmaB) == 12
      and det_I_minus_zU(sigmaB) == target and conj == sigmaB
      and sigmaA != sigmaB,
      "sigmaA ~ sigmaB conjugate (h found), same resolvent, different maps")

# C4 (LOAD-BEARING SEPARATION, class B != class C): the two admissible CKM
# completions change an INVARIANT (16/25 vs 144/169) => that freedom is NOT
# gauge.  CREDIT (skeptic #1 repair): the 16/25 vs 144/169 arithmetic is the
# Lean-proved content of D0-CKM-OVERLAP-UNDERDETERMINATION-NOGO-001, which
# itself types the resolution "a NEW primitive (extension), not a present-core
# theorem" => the freedom files as class B-ext (extension import), NOT
# B-measurement.  The common-rotation half (V = B_up^T B_down unchanged) is an
# ILLUSTRATION of the un-minted commutant-layer extension (memo risk R3), not
# a scene-torsor fact — kept as illustration only.
def rot345():
    return mat([[Fr(3, 5), Fr(-4, 5), 0], [Fr(4, 5), Fr(3, 5), 0], [0, 0, 1]])

def rot51213():
    return mat([[Fr(5, 13), Fr(-12, 13), 0], [Fr(12, 13), Fr(5, 13), 0], [0, 0, 1]])

R1, R2 = rot345(), rot51213()
I3 = eye(3)
orth = mat_eq(mmul(transpose(R1), R1), I3) and mat_eq(mmul(transpose(R2), R2), I3)
v12_1 = R1[0][1] ** 2          # |V_12|^2 completion 1
v12_2 = R2[0][1] ** 2
# gauge direction: common rotation g0 applied to both bases leaves V invariant
g0 = rot345()
Bup, Bdown = I3, R1
V = mmul(transpose(Bup), Bdown)
Vg = mmul(transpose(mmul(g0, Bup)), mmul(g0, Bdown))
check("C4_classB_separation_CKM",
      orth and v12_1 == Fr(16, 25) and v12_2 == Fr(144, 169)
      and v12_1 != v12_2 and mat_eq(V, Vg),
      "completions differ on the invariant (16/25 vs 144/169, reproducing the "
      "CKM row's Lean content) => class B-ext (row-typed extension); common "
      "rotation leaves V unchanged (R3-extension illustration)")

# C5: anomaly-sum split: the SUMS are symmetric functions (class A, mirrors
# LEAN_PROVED D0-GAUGE-MATTER-002); the per-slot attachment is class C
# (mirrors PROOF-TARGET D0-HYPERCHARGE-GRAPH-FLOW-OWNER-001).
Ys = [Fr(1, 6)] * 6 + [Fr(-2, 3)] * 3 + [Fr(1, 3)] * 3 + [Fr(-1, 2)] * 2 + [Fr(1)]
sY = sum(Ys)
sY3 = sum(y ** 3 for y in Ys)
p = list(range(15)); random.shuffle(p)
Yp = [Ys[p[i]] for i in range(15)]
check("C5_anomaly_sums_vs_slots",
      sY == 0 and sY3 == 0 and sum(Yp) == 0 and sum(y**3 for y in Yp) == 0
      and Yp != Ys,
      "Sum Y = Sum Y^3 = 0 invariant; the slot row moved under permutation")

# D1 (RE-FILED from v1's "C6" per skeptic #1's strongest finding): rho =
# cos(pi/9) is CLASS D — un-owned-ansatz import — NOT class C.  Any 9-cycle
# through omega0, symmetrized and Feshbach-compressed (omega0 deleted), gives
# the P8 path whose top eigenvalue is cos(pi/9) — 2cos(pi/9) is a root of
# x^3 - 3x - 1 (EXACT: polynomial division of char(P8 adjacency)).  The value
# is FAMILY-CANONICAL (same for every point of the ansatz class), so treating
# the cyclic order as harmless class-C gauge-fixing would promote cos(pi/9) to
# a determined internal invariant — exactly what row 544 + the M2 memo forbid.
# The two computed facts (family-canonicity + pattern-dependence, K9 control
# gives 3.5) are what SEPARATE class D from class C: a class-C choice adds NO
# new invariant; a class-D choice does, conditionally on the ansatz.
def charpoly_int(M):
    # Faddeev-LeVerrier over Fractions
    n = len(M)
    coeffs = [Fr(1)]
    Mk = [row[:] for row in M]
    for k in range(1, n + 1):
        c = -sum(Mk[i][i] for i in range(n)) / k
        coeffs.append(c)
        for i in range(n):
            Mk[i][i] += c
        if k < n:
            Mk = mmul(M, Mk)
    return coeffs        # x^n + c1 x^{n-1} + ...

path8 = zeros(8, 8)
for i in range(7):
    path8[i][i + 1] = Fr(1)
    path8[i + 1][i] = Fr(1)
cp = charpoly_int(path8)          # degree 8 in x (for adjacency, eigen 2cos)
# divide by x^3 - 3x - 1 exactly
def poly_divmod(num, den):
    num = num[:]
    q = []
    while len(num) >= len(den):
        f = num[0] / den[0]
        q.append(f)
        for i in range(len(den)):
            num[i] -= f * den[i]
        num.pop(0)
    return q, num

qout, rem = poly_divmod(cp, [Fr(1), Fr(0), Fr(-3), Fr(-1)])
exact_div = all(x == 0 for x in rem)
# float corroboration: top eigenvalue of sym 9-cycle compressed = cos(pi/9)
import math
def top_eig_sym(Mf, iters=4000):
    # SCRIPT ERROR-OF-RECORD FIX (first run FAIL C6): the compressed 9-cycle is
    # the bipartite path P8, whose spectrum comes in +-lambda pairs, so the
    # unshifted power iteration oscillates between the two extreme
    # eigenvectors and the Rayleigh quotient of the mixture is meaningless.
    # Fix: shift by +I (eigenvalues 1+lambda, strictly dominant top for these
    # matrices), iterate, subtract 1.  Technique bug, not a content failure.
    n = len(Mf)
    v = [random.random() for _ in range(n)]
    M = [[Mf[i][j] + (1.0 if i == j else 0.0) for j in range(n)] for i in range(n)]
    for _ in range(iters):
        w = [sum(M[i][j] * v[j] for j in range(n)) for i in range(n)]
        lam = max(abs(x) for x in w)
        if lam == 0:
            return -1.0
        v = [x / lam for x in w]
    num = sum(v[i] * sum(M[i][j] * v[j] for j in range(n)) for i in range(n))
    den = sum(x * x for x in v)
    return num / den - 1.0

vals = set()
for _ in range(6):
    order = [0] + random.sample(range(1, 9), 8)     # a 9-cycle through slot 0
    C = [[0.0] * 9 for _ in range(9)]
    for t in range(9):
        a, b = order[t], order[(t + 1) % 9]
        C[a][b] += 0.5
        C[b][a] += 0.5
    # compress out omega0 = slot 0
    sub = [[C[i][j] for j in range(1, 9)] for i in range(1, 9)]
    vals.add(round(top_eig_sym(sub), 9))
family_canonical = (len(vals) == 1 and abs(list(vals)[0] - math.cos(math.pi / 9)) < 1e-7)
# a DIFFERENT un-owned pattern: complete graph K9 symmetrized/2, compressed
K8 = [[0.0 if i == j else 0.5 for j in range(8)] for i in range(8)]
alt = top_eig_sym(K8)
check("D1_cos_pi_9_classD_unowned_ansatz",
      exact_div and family_canonical and abs(alt - 3.5) < 1e-7,
      "x^3-3x-1 | char(P8) exact; all 9-cycles give cos(pi/9)=0.939693 "
      "[FLOAT-CORROBORATION] (family-canonical => NOT contentless => class D, "
      "not C); K9 pattern gives 3.5 (ansatz-dependent)")

# ----------------------------------------------------------------------------
# comparator (FLOAT-CORROBORATION, non-load-bearing): U3 = diag(mu9;mu11;mu13)
# nilpotent fingerprint and its torsor invariance (TICK memo B / M2 X4).
# ----------------------------------------------------------------------------
print("\n== comparator (float corroboration) ==")
import cmath
def carrier_U3():
    U = [[0j] * N for _ in range(N)]
    for zi, zone in enumerate(ZONES):
        n = len(zone)
        for t, v in enumerate(zone):
            U[v][v] = cmath.exp(2j * cmath.pi * t / n)
    return U

def cmmul(Ax, Bx):
    n = len(Ax)
    Bt = list(zip(*Bx))
    return [[sum(Ax[i][t] * Bt[j][t] for t in range(n)) for j in range(n)] for i in range(n)]

Pf = [[float(P[i][j]) for j in range(N)] for i in range(N)]
Qf = [[float(Q[i][j]) for j in range(N)] for i in range(N)]
U3 = carrier_U3()
QU3Q = cmmul(cmmul(Qf, U3), Qf)
Mk = [row[:] for row in QU3Q]
for _ in range(11):
    Mk = cmmul(Mk, QU3Q)
n12 = max(abs(x) for r in Mk for x in r)
PU3Q = cmmul(cmmul(Pf, U3), Qf)
fro = math.sqrt(sum(abs(x) ** 2 for r in PU3Q for x in r))
# torsor conjugation
gp = random_zone_perm()
U3g = [[0j] * N for _ in range(N)]
for i in range(N):
    for j in range(N):
        U3g[gp[i]][gp[j]] = U3[i][j]
QU3Qg = cmmul(cmmul(Qf, U3g), Qf)
Mkg = [row[:] for row in QU3Qg]
for _ in range(11):
    Mkg = cmmul(Mkg, QU3Qg)
n12g = max(abs(x) for r in Mkg for x in r)
PU3Qg = cmmul(cmmul(Pf, U3g), Qf)
frog = math.sqrt(sum(abs(x) ** 2 for r in PU3Qg for x in r))
check("X_U3_comparator_invariance", n12 < 1e-9 and abs(fro - math.sqrt(3)) < 1e-9
      and n12g < 1e-9 and abs(frog - math.sqrt(3)) < 1e-9,
      "(QU3Q)^12=0, |PU3Q|_F=sqrt(3), both preserved under relabeling "
      "[FLOAT-CORROBORATION]")

# ----------------------------------------------------------------------------
# SECTION N — negative controls (each can fail the CONCLUSION)
# ----------------------------------------------------------------------------
print("\n== SECTION N: negative controls ==")

# N1: if C1 fails (distinct per-vertex weights), a canonical selector EXISTS:
# weight-sorting is an owned-in-that-world internal rule picking one labeling.
w = list(range(N))          # distinct weights 0..32
random.shuffle(w)
distinct = len(set(w)) == N
# any automorphism of (A, diag(w)) must fix every vertex: check transpositions
# within a zone (the only candidates that preserve A) never preserve w.
ok_auto = all(w[i] != w[j] for zone in ZONES for i in zone for j in zone if i < j)
# the selector: label vertices of each zone by rank of weight — a bijection.
sel = {}
for zone in ZONES:
    ranks = sorted(zone, key=lambda vv: w[vv])
    for label, vv in enumerate(ranks):
        sel[vv] = label
sel_ok = all(sorted(sel[vv] for vv in zone) == list(range(len(zone))) for zone in ZONES)
check("N1_C1_broken_selector_exists", distinct and ok_auto and sel_ok,
      "distinct weights => trivial stabilizer => canonical weight-sort labeling "
      "(conclusion CONTINGENT on C1)")

# N2: the gauge group is computed, not assumed: K(2,2) has the part-swap
# (|Aut| = 8 > |S2xS2| = 4); K(2,3) does not (|Aut| = 12 = |S2xS3|).
def count_aut(sizes):
    n = sum(sizes)
    zones_ = []
    at = 0
    for s in sizes:
        zones_.append(list(range(at, at + s)))
        at += s
    Ax = [[0] * n for _ in range(n)]
    for a, b in itertools.combinations(range(len(sizes)), 2):
        for i in zones_[a]:
            for j in zones_[b]:
                Ax[i][j] = Ax[j][i] = 1
    cnt = 0
    for p in itertools.permutations(range(n)):
        if all(Ax[p[i]][p[j]] == Ax[i][j] for i in range(n) for j in range(n)):
            cnt += 1
    return cnt

check("N2_gauge_group_computed_not_assumed",
      count_aut([2, 2]) == 8 and count_aut([2, 3]) == 12,
      "K(2,2): 8 (part swap present); K(2,3): 12 = |S2 x S3| (absent)")

# N3: the fingerprint discriminates the owned pattern: a 6/3 split gives
# 72/81, not 80/81.
d63 = [1, 1, 1, 1, 1, 1, -1, -1, -1]
f2_63 = frob2(mmul(mmul(P, carrier(d63)), Q))
check("N3_fingerprint_discriminates", f2_63 == Fr(72, 81),
      "6/3 split: 72/81 != 80/81 (value follows the owned 5/4 pattern)")

# N4: non-equivariant ingredient breaks the invariance lemma: a word including
# a FIXED external per-slot catalog D0 is NOT torsor-invariant.
# SCRIPT ERROR-OF-RECORD FIX (first run FAIL N4): the original control
# conjugated A by g in G — but gAg^-1 = A identically (that is C1), so the two
# words were EQUAL by construction and the control could never fire.  The
# correct control transports the CARRIER (as in A4d) while holding the
# external catalog fixed: invariance then breaks, showing the lemma's
# hypothesis (ALL inputs scene-derived/equivariantly transported) is
# load-bearing.
D0diag = eye(N)
D0diag[Z9[2]][Z9[2]] = Fr(7)               # external catalog: weight 7 at one slot
Un4 = carrier(CHI['chi_B'])
gn4 = list(range(N))
gn4[Z9[2]], gn4[Z9[5]] = gn4[Z9[5]], gn4[Z9[2]]   # moves a -1 onto the weighted slot
Un4g = conj_by_perm(Un4, gn4)              # carrier transported, catalog held fixed
tr_bad = sum((D0diag[i][i] * Un4[i][i]) for i in range(N))
tr_badg = sum((D0diag[i][i] * Un4g[i][i]) for i in range(N))
f_bad = frob2(mmul(P, mmul(mmul(D0diag, Un4), Q)))
f_badg = frob2(mmul(P, mmul(mmul(D0diag, Un4g), Q)))
check("N4_lemma_hypothesis_load_bearing",
      tr_bad != tr_badg and f_bad != f_badg,
      "catalog-weighted trace %s -> %s and |P(D0 U)Q|^2 %s -> %s under relabeling"
      % (tr_bad, tr_badg, f_bad, f_badg))

# ----------------------------------------------------------------------------
print("\n===================================================================")
print("TOTAL: %d PASS / %d FAIL" % (len(PASS), len(FAIL)))
if FAIL:
    print("FAILED:", *FAIL, sep="\n  ")
    sys.exit(1)
print("ALL CHECKS PASS")
sys.exit(0)
