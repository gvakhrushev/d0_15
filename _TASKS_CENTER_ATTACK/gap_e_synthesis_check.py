#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GAP_E_SYNTHESIS check — the extension alphabet as the CANONICAL (characteristic)
SUBQUOTIENT list of the owned role group Q8 (= Omega8, BOOK_01 SS01.7.1A).

Companion to _TASKS_CENTER_ATTACK/GAP_E_SYNTHESIS_MEMO.md.

*** SKEPTIC #1 OUTCOME (2026-07-05/06): the CLOSURE claim built on these
*** computations was KILLED — the SSJ totality scan covered Aut-invariant
*** ELEMENT-SUBSETS only, while canonical role-DERIVED objects escape it:
*** Sub(Q8) (6 subgroups, family stable via the owned Dedekind property),
*** Out(Q8) ~ S3 (6 elements), the characteristic chain {1,Z,Q8} (3 members).
*** Section SSN below encodes these counter-objects as KILL-CONTROLS: it
*** verifies each escape and thereby FAILS the memo's original headline (a)
*** ("no size-6 object in the role algebra at all"); it also computes the
*** partition-grammar discriminator recorded in the memo's SSOWNERSHIP-CHECK.
*** Sections SSA-SSM remain valid as STRUCTURE results (scoped claims only:
*** no size-6 SUBQUOTIENT; canonical layers = {Z2, V4}; census).
*** FINAL VERDICT LINE: KILLED-AS-CLOSURE (computation layer holds).

WHAT IS COMPUTED (exact integer arithmetic; no floats; every quantity built from
independently-constructed group objects, never from the conclusion):

  SSA  Q8 built from integer quaternion tuples; group axioms verified.
  SSB  Full subgroup lattice of Q8 (expect 6 subgroups, orders [1,2,4,4,4,8]).
  SSC  Aut(Q8) by exhaustive enumeration of unit-fixing bijections that are
       homomorphisms (expect |Aut| = 24); Inn(Q8) from conjugations (expect 4);
       Out = Aut/Inn (expect order 6) acting on the C4-triple as full S3,
       TRANSITIVELY.
  SSD  Characteristic subgroups of Q8 (expect exactly {1, Z, Q8}); the three C4's
       are NOT characteristic (one Aut-orbit of size 3).
  SSE  Triple identity  [Q8,Q8] = Z(Q8) = Phi(Q8) = {+-1}  recomputed from scratch
       (commutator closure; center; Frattini = intersection of maximals).
  SSF  Canonical subquotient alphabet of Q8: pairs (H,K), H,K characteristic,
       K <= H, alphabet = H/K, PROPER (|H/K| < 8) and NONTRIVIAL (|H/K| > 1).
       EXPECT exactly two: Z/1 ~ Z2 (size 2) and Q8/Z ~ V4 (size 4) — computed,
       not asserted; sizes read off the computed lattice.
  SSG  The four cosets of Z(Q8) are exactly the sign-pairs {x, -x} — the four
       terminal roles A,B,C,D under the owned iso A->1, B->i, C->j, D->k
       (BOOK_01:782-786).  Q8/Z has exponent 2 (Klein four), matching the owned
       sentence "the abelianization Q8/[Q8,Q8] being the Klein four-group"
       (BOOK_01:830, CORE-FORMALIZED D0-OMEGA8-CENTER-001).
  SSH  Non-splitness: Q8 has exactly ONE involution (Z2^3 has 7); Q8 has NO Klein
       subgroup, hence NO section of Q8 -> Q8/Z: the central extension
       1 -> Z -> Q8 -> V4 -> 1 does not split.  The owned set-product
       Omega8 = ABCD x {+-} (BOOK_01:1535) is verified as a SET bijection
       (r,s) -> s*r and verified NOT to be a group product (Q8 is non-abelian,
       V4 x Z2 abelian) — the "x" is coset bookkeeping; the group content is
       exactly the central extension.
  SSI  Subquotient ORDER set of Q8 over ALL pairs K normal-in H (not only
       characteristic): expect {1,2,4,8}.  6 IS ABSENT — the Lagrange kill of the
       size-6 extension (+4 -> V15) is arithmetic, computed.
  SSJ  STRONGEST SELF-ATTACK (pre-registered): Aut-invariant SUBSETS of Q8.
       Element-orbits under Aut are {1}, {-1}, {6 imaginaries}; the UNIQUE
       invariant 6-subset is the imaginaries.  Computed: it is NOT composition-
       closed, and its generated closure is ALL of Q8 with hidden remainder
       {+-1} of size 2 — so the would-be catalog-free 6-alphabet is the whole
       role group with a 2-element hidden remainder (owned hidden-marker /
       whole-type-repeat grammar, BOOK_01:1556 V10 clause + NoExtension.lean:47).
  SSK  Aut(V4) is transitive on the three involutions of Q8/Z (S3): the three
       Z2-factors of ABCD = D2 x D2 are catalog-relative — "= D2^2" is
       bookkeeping, not canonical structure (matches GAP_E_DYAD_POWER EOR-1);
       and the three V4-involutions are exactly the images of the three C4's:
       the SAME S3 obstruction, upstairs and downstairs.
  SSL  FINGERPRINT CENSUS over ALL FIVE groups of order 8 (Z8, Z4xZ2, Z2^3, D4,
       Q8), same generic pipeline: number of proper nontrivial canonical
       subquotient pairs.  EXPECT: Q8 is the UNIQUE group of order 8 with
       EXACTLY TWO, with pairwise non-isomorphic alphabets, sizes {2,4}, each
       iso-type realized exactly once.  (Negative controls that can FAIL THE
       CONCLUSION: if D4 or Z8 were equally clean, the "tower structure is a Q8
       fingerprint" claim dies; if Z2^3 had layers, the non-split/non-abelian
       necessity reading dies.)
  SSM  Tower kill matrix (over-base fork, scan bound z3 <= 21 DECLARED): third-
       zone size 9+x admissible iff x is the size of a computed canonical
       alphabet not already consumed.  Survivor set must be computed as
       {(9,11,13)} — and the rival kill for each z3 is NAMED by prong.
       Negative control: the same scan run with D4 as role group must NOT
       yield a unique forced tower (it has 4 candidate alphabets -> selection
       catalog needed), i.e. the control can fail the conclusion.

VERDICT line printed at the end; exit code 0 iff all checks pass.
"""

import sys
from itertools import permutations, combinations

CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok)))
    tag = "PASS" if ok else "FAIL"
    line = f"[{tag}] {name}"
    if detail:
        line += f"  -- {detail}"
    print(line)
    return ok


# ----------------------------------------------------------------------------
# Generic finite-group machinery (element set + multiplication callable).
# ----------------------------------------------------------------------------

class G:
    def __init__(self, name, elems, mul, one):
        self.name = name
        self.elems = list(elems)
        self.mul = mul
        self.one = one
        self.n = len(self.elems)
        self._inv = {}
        for a in self.elems:
            for b in self.elems:
                if mul(a, b) == one:
                    self._inv[a] = b
        assert len(self._inv) == self.n, f"{name}: not a group (missing inverses)"

    def inv(self, a):
        return self._inv[a]

    def is_group(self):
        E = set(self.elems)
        for a in self.elems:
            for b in self.elems:
                if self.mul(a, b) not in E:
                    return False
        for a in self.elems:
            for b in self.elems:
                for c in self.elems:
                    if self.mul(self.mul(a, b), c) != self.mul(a, self.mul(b, c)):
                        return False
        return all(self.mul(self.one, a) == a and self.mul(a, self.one) == a
                   for a in self.elems)

    def order_of(self, a):
        k, x = 1, a
        while x != self.one:
            x = self.mul(x, a)
            k += 1
        return k

    def closure(self, seed):
        S = set(seed) | {self.one}
        frontier = True
        while frontier:
            frontier = False
            for a in list(S):
                for b in list(S):
                    c = self.mul(a, b)
                    if c not in S:
                        S.add(c)
                        frontier = True
                d = self.inv(a)
                if d not in S:
                    S.add(d)
                    frontier = True
        return frozenset(S)

    def subgroups(self):
        subs = set()
        # closures of all subsets of size <= 3 suffice for |G| = 8
        # (every subgroup of an order-8 group is generated by <= 3 elements).
        idx = self.elems
        subs.add(self.closure([]))
        for r in (1, 2, 3):
            for combo in combinations(idx, r):
                subs.add(self.closure(combo))
        return sorted(subs, key=lambda s: (len(s), sorted(map(repr, s))))

    def automorphisms(self):
        """Exhaustive: all bijections fixing identity that are homomorphisms."""
        others = [e for e in self.elems if e != self.one]
        auts = []
        for perm in permutations(others):
            f = {self.one: self.one}
            for a, b in zip(others, perm):
                f[a] = b
            ok = True
            for a in self.elems:
                if not ok:
                    break
                for b in self.elems:
                    if f[self.mul(a, b)] != self.mul(f[a], f[b]):
                        ok = False
                        break
            if ok:
                auts.append(f)
        return auts

    def inner_automorphisms(self):
        inns = []
        seen = set()
        for g in self.elems:
            f = {a: self.mul(self.mul(g, a), self.inv(g)) for a in self.elems}
            key = tuple(sorted((repr(k), repr(v)) for k, v in f.items()))
            if key not in seen:
                seen.add(key)
                inns.append(f)
        return inns

    def center(self):
        return frozenset(a for a in self.elems
                         if all(self.mul(a, b) == self.mul(b, a) for b in self.elems))

    def commutator_subgroup(self):
        comms = [self.mul(self.mul(a, b), self.mul(self.inv(a), self.inv(b)))
                 for a in self.elems for b in self.elems]
        return self.closure(comms)

    def frattini(self):
        subs = self.subgroups()
        full = frozenset(self.elems)
        proper = [s for s in subs if s != full]
        maximal = [s for s in proper
                   if not any(s < t for t in proper)]
        F = set(self.elems)
        for m in maximal:
            F &= m
        return frozenset(F)

    def is_normal(self, K, H):
        """K normal in H (both frozensets, K subset of H)."""
        return all(self.mul(self.mul(h, k), self.inv(h)) in K
                   for h in H for k in K)

    def quotient_iso_type(self, H, K):
        """Isomorphism type of H/K for |H/K| in {1,2,4,8} via invariants."""
        cosets = []
        seen = set()
        for h in H:
            c = frozenset(self.mul(h, k) for k in K)
            if c not in seen:
                seen.add(c)
                cosets.append(c)
        n = len(cosets)

        def cmul(c1, c2):
            h1 = next(iter(c1))
            h2 = next(iter(c2))
            p = self.mul(h1, h2)
            for c in cosets:
                if p in c:
                    return c
            raise RuntimeError("coset product not found")

        idc = None
        for c in cosets:
            if self.one in c:
                idc = c
        orders = []
        for c in cosets:
            k, x = 1, c
            while x != idc:
                x = cmul(x, c)
                k += 1
            orders.append(k)
        abelian = all(cmul(a, b) == cmul(b, a) for a in cosets for b in cosets)
        expnt = 1
        for o in orders:
            # lcm
            a, b = expnt, o
            while b:
                a, b = b, a % b
            expnt = expnt * o // a
        if n == 1:
            return "1"
        if n == 2:
            return "Z2"
        if n == 4:
            return "Z4" if expnt == 4 else "V4"
        if n == 8:
            if not abelian:
                inv_count = sum(1 for o in orders if o == 2)
                return "Q8" if inv_count == 1 else "D4"
            if expnt == 8:
                return "Z8"
            if expnt == 4:
                return "Z4xZ2"
            return "Z2^3"
        return f"order{n}"


def characteristic_subgroups(g, subs, auts):
    out = []
    for s in subs:
        if all(frozenset(f[x] for x in s) == s for f in auts):
            out.append(s)
    return out


def canonical_alphabet(g):
    """Proper nontrivial canonical subquotients: pairs (H,K), H,K characteristic
    in g, K <= H, K normal in H, 1 < |H/K| < |g|.  Returns list of
    (|H|, |K|, size, iso_type)."""
    subs = g.subgroups()
    auts = g.automorphisms()
    chars = characteristic_subgroups(g, subs, auts)
    pairs = []
    for H in chars:
        for K in chars:
            if K < H or K == H:
                if K <= H and g.is_normal(K, H):
                    size = len(H) // len(K)
                    if 1 < size < g.n:
                        pairs.append((len(H), len(K), size,
                                      g.quotient_iso_type(H, K)))
    return sorted(set(pairs)), chars, auts, subs


# ----------------------------------------------------------------------------
# SSA  Q8 from integer quaternion tuples
# ----------------------------------------------------------------------------
print("=" * 78)
print("SSA  Q8 construction (integer quaternion tuples)")
print("=" * 78)


def qmul(x, y):
    a1, b1, c1, d1 = x
    a2, b2, c2, d2 = y
    return (a1 * a2 - b1 * b2 - c1 * c2 - d1 * d2,
            a1 * b2 + b1 * a2 + c1 * d2 - d1 * c2,
            a1 * c2 - b1 * d2 + c1 * a2 + d1 * b2,
            a1 * d2 + b1 * c2 - c1 * b2 + d1 * a2)


ONE = (1, 0, 0, 0)
NEG = (-1, 0, 0, 0)
I = (0, 1, 0, 0)
J = (0, 0, 1, 0)
K = (0, 0, 0, 1)
Q8_ELEMS = [ONE, NEG, I, (0, -1, 0, 0), J, (0, 0, -1, 0), K, (0, 0, 0, -1)]

q8 = G("Q8", Q8_ELEMS, qmul, ONE)
check("A1: Q8 is a group of order 8", q8.is_group() and q8.n == 8)
check("A2: Hamilton relations i^2=j^2=k^2=ijk=-1",
      qmul(I, I) == NEG and qmul(J, J) == NEG and qmul(K, K) == NEG
      and qmul(qmul(I, J), K) == NEG)
check("A3: non-abelian (ij=k, ji=-k)",
      qmul(I, J) == K and qmul(J, I) == (0, 0, 0, -1))

# ----------------------------------------------------------------------------
# SSB  subgroup lattice
# ----------------------------------------------------------------------------
print("=" * 78)
print("SSB  Subgroup lattice of Q8")
print("=" * 78)
subs_q8 = q8.subgroups()
orders = sorted(len(s) for s in subs_q8)
print(f"  subgroup orders: {orders}")
check("B1: exactly 6 subgroups", len(subs_q8) == 6)
check("B2: orders are [1,2,4,4,4,8]", orders == [1, 2, 4, 4, 4, 8])
Zsub = frozenset({ONE, NEG})
check("B3: the unique order-2 subgroup is {+-1}",
      [s for s in subs_q8 if len(s) == 2] == [Zsub])
C4s = [s for s in subs_q8 if len(s) == 4]
check("B4: the three order-4 subgroups are <i>,<j>,<k> (each cyclic, contains Z)",
      all(Zsub <= s for s in C4s)
      and all(q8.quotient_iso_type(s, frozenset({ONE})) == "Z4" for s in C4s))
check("B5: every subgroup is normal in Q8 (Hamiltonian/Dedekind, SS01.7.1A)",
      all(q8.is_normal(s, frozenset(Q8_ELEMS)) for s in subs_q8))
check("B6: Q8 has NO Klein (V4) subgroup",
      all(q8.quotient_iso_type(s, frozenset({ONE})) != "V4" for s in subs_q8))

# ----------------------------------------------------------------------------
# SSC  Aut / Inn / Out and the action on the C4 triple
# ----------------------------------------------------------------------------
print("=" * 78)
print("SSC  Aut(Q8), Inn(Q8), Out(Q8) on the C4-triple")
print("=" * 78)
auts_q8 = q8.automorphisms()
inns_q8 = q8.inner_automorphisms()
check("C1: |Aut(Q8)| = 24", len(auts_q8) == 24, f"|Aut|={len(auts_q8)}")
check("C2: |Inn(Q8)| = 4 (= Q8/Z)", len(inns_q8) == 4, f"|Inn|={len(inns_q8)}")

C4_sorted = sorted(C4s, key=lambda s: sorted(map(repr, s)))
def triple_perm(f):
    return tuple(C4_sorted.index(frozenset(f[x] for x in s)) for s in C4_sorted)

perm_images = set(triple_perm(f) for f in auts_q8)
check("C3: Aut(Q8) induces ALL 6 permutations of {<i>,<j>,<k>} (full S3)",
      len(perm_images) == 6)
check("C4: the triple action is TRANSITIVE (single orbit of size 3)",
      any(triple_perm(f)[0] == 1 for f in auts_q8)
      and any(triple_perm(f)[0] == 2 for f in auts_q8))
kernel = [f for f in auts_q8 if triple_perm(f) == (0, 1, 2)]
check("C5: kernel of the triple action has order 4; Out(Q8) ~ S3 (order 24/4 = 6)",
      len(kernel) == 4 and len(auts_q8) // len(kernel) == 6)
inn_keys = set(tuple(sorted((repr(k), repr(v)) for k, v in f.items())) for f in inns_q8)
ker_keys = set(tuple(sorted((repr(k), repr(v)) for k, v in f.items())) for f in kernel)
check("C6: Inn(Q8) = kernel of the triple action (inner autos fix each <i>,<j>,<k>)",
      inn_keys == ker_keys)
check("C7: every automorphism fixes -1 (the unique involution) pointwise",
      all(f[NEG] == NEG for f in auts_q8))

# ----------------------------------------------------------------------------
# SSD  characteristic subgroups
# ----------------------------------------------------------------------------
print("=" * 78)
print("SSD  Characteristic subgroups of Q8")
print("=" * 78)
chars_q8 = characteristic_subgroups(q8, subs_q8, auts_q8)
char_orders = sorted(len(s) for s in chars_q8)
print(f"  characteristic subgroup orders: {char_orders}")
check("D1: characteristic subgroups are EXACTLY {1, Z, Q8} (orders [1,2,8])",
      char_orders == [1, 2, 8])
check("D2: no C4 is characteristic (the triple is one Aut-orbit of size 3)",
      all(s not in chars_q8 for s in C4s))
orbit = set()
for f in auts_q8:
    orbit.add(frozenset(f[x] for x in C4s[0]))
check("D3: Aut-orbit of <i> is the full triple {<i>,<j>,<k>} (size 3)",
      orbit == set(C4s))

# ----------------------------------------------------------------------------
# SSE  triple identity  [Q8,Q8] = Z(Q8) = Phi(Q8) = {+-1}
# ----------------------------------------------------------------------------
print("=" * 78)
print("SSE  Triple identity (recomputed from scratch)")
print("=" * 78)
Zc = q8.center()
Dc = q8.commutator_subgroup()
Fc = q8.frattini()
check("E1: Z(Q8) = {+-1}", Zc == Zsub)
check("E2: [Q8,Q8] = {+-1}", Dc == Zsub)
check("E3: Phi(Q8) = {+-1} (maximals are the three C4's)", Fc == Zsub)
check("E4: triple identity Z = [Q8,Q8] = Phi (BOOK_01:809, THEOREM b01-31)",
      Zc == Dc == Fc)
comm_ij = qmul(qmul(I, J), qmul(q8.inv(I), q8.inv(J)))
check("E5: [i,j] = -1 realizes the remainder (Omega8Center.lean witness)",
      comm_ij == NEG)

# ----------------------------------------------------------------------------
# SSF  the canonical subquotient alphabet of Q8
# ----------------------------------------------------------------------------
print("=" * 78)
print("SSF  Canonical (characteristic) subquotient alphabet of Q8")
print("=" * 78)
alpha_q8, _, _, _ = canonical_alphabet(q8)
print(f"  proper nontrivial canonical subquotients (|H|,|K|,size,type): {alpha_q8}")
check("F1: EXACTLY TWO proper nontrivial canonical subquotients",
      len(alpha_q8) == 2, f"{alpha_q8}")
check("F2: they are Z/1 ~ Z2 (size 2) and Q8/Z ~ V4 (size 4)",
      alpha_q8 == [(2, 1, 2, "Z2"), (8, 2, 4, "V4")])
check("F3: sizes read off the computation = {2, 4} (D2 and ABCD sizes)",
      sorted(p[2] for p in alpha_q8) == [2, 4])
check("F4: the two alphabets are NON-isomorphic (Z2 vs V4) — zero instance freedom",
      alpha_q8[0][3] != alpha_q8[1][3])
check("F5: characteristic subgroups form a CHAIN 1 < Z < Q8; the two alphabets are "
      "its successive quotients (the two layers of 1 -> Z -> Q8 -> V4 -> 1)",
      chars_q8[0] < chars_q8[1] < chars_q8[2] if len(chars_q8) == 3 else False)

# ----------------------------------------------------------------------------
# SSG  cosets of Z are the sign-pairs = the four terminal roles
# ----------------------------------------------------------------------------
print("=" * 78)
print("SSG  Q8/Z cosets = sign-pairs = ABCD (owned iso A->1,B->i,C->j,D->k)")
print("=" * 78)
cosets = []
seen = set()
for h in Q8_ELEMS:
    c = frozenset(qmul(h, k) for k in Zsub)
    if c not in seen:
        seen.add(c)
        cosets.append(c)
check("G1: exactly 4 cosets of Z in Q8", len(cosets) == 4)
check("G2: every coset is a sign-pair {x, -x}",
      all(len(c) == 2 and
          all(qmul(NEG, x) in c for x in c) for c in cosets))
role_reps = {ONE: "A", I: "B", J: "C", K: "D"}
covered = set()
for c in cosets:
    for rep, role in role_reps.items():
        if rep in c:
            covered.add(role)
check("G3: the four cosets carry exactly the four roles A,B,C,D (via the owned iso)",
      covered == {"A", "B", "C", "D"})
check("G4: Q8/Z has exponent 2 => Klein four-group (BOOK_01:830 'abelianization ... "
      "Klein four-group')",
      q8.quotient_iso_type(frozenset(Q8_ELEMS), Zsub) == "V4")

# ----------------------------------------------------------------------------
# SSH  non-splitness of 1 -> Z -> Q8 -> V4 -> 1
# ----------------------------------------------------------------------------
print("=" * 78)
print("SSH  Non-splitness: the 'x' in Omega8 = ABCD x {+-} is coset bookkeeping")
print("=" * 78)
inv_count_q8 = sum(1 for a in Q8_ELEMS if a != ONE and qmul(a, a) == ONE)
check("H1: Q8 has exactly ONE involution (-1)", inv_count_q8 == 1)
check("H2: no V4 subgroup => no section of Q8 -> Q8/Z => extension NON-SPLIT",
      all(q8.quotient_iso_type(s, frozenset({ONE})) != "V4" for s in subs_q8))
# set bijection ABCD x {+-} -> Q8, (r, s) -> s*r
pairs_set = set()
for rep in (ONE, I, J, K):
    for sgn in (ONE, NEG):
        pairs_set.add(qmul(sgn, rep))
check("H3: (role, sign) -> sign*role is a SET bijection ABCD x {+-} <-> Q8",
      pairs_set == set(Q8_ELEMS))
# group product would force abelian: V4 x Z2 is abelian, Q8 is not
check("H4: Q8 is NOT V4 x Z2 as a group (non-abelian vs abelian; 1 vs 7 involutions)",
      qmul(I, J) != qmul(J, I))

# ----------------------------------------------------------------------------
# SSI  subquotient order set — the Lagrange kill of size 6
# ----------------------------------------------------------------------------
print("=" * 78)
print("SSI  Subquotient orders of Q8 over ALL pairs K normal-in H")
print("=" * 78)
sq_orders = set()
for H in subs_q8:
    for Ksub in subs_q8:
        if Ksub <= H and q8.is_normal(Ksub, H):
            sq_orders.add(len(H) // len(Ksub))
print(f"  subquotient order set: {sorted(sq_orders)}")
check("I1: subquotient order set = {1, 2, 4, 8}", sq_orders == {1, 2, 4, 8})
check("I2: 6 is NOT a subquotient order (Lagrange: 6 does not divide 8)",
      6 not in sq_orders and 8 % 6 != 0)
check("I3: 3 and 5 are not subquotient orders either (all odd sizes > 1 die)",
      3 not in sq_orders and 5 not in sq_orders)

# ----------------------------------------------------------------------------
# SSJ  strongest self-attack: Aut-invariant subsets (the imaginary 6-set)
# ----------------------------------------------------------------------------
print("=" * 78)
print("SSJ  Pre-registered self-attack: Aut-invariant SUBSETS of Q8")
print("=" * 78)
elem_orbits = []
placed = set()
for a in Q8_ELEMS:
    if a in placed:
        continue
    orb = frozenset(f[a] for f in auts_q8)
    elem_orbits.append(orb)
    placed |= orb
orbit_sizes = sorted(len(o) for o in elem_orbits)
print(f"  Aut element-orbit sizes: {orbit_sizes}")
check("J1: Aut element-orbits are {1}, {-1}, {six imaginaries} (sizes [1,1,6])",
      orbit_sizes == [1, 1, 6])
# all invariant subsets = unions of orbits
inv_subset_sizes = set()
from itertools import chain
for r in range(len(elem_orbits) + 1):
    for combo in combinations(elem_orbits, r):
        inv_subset_sizes.add(sum(len(o) for o in combo))
print(f"  invariant subset sizes: {sorted(inv_subset_sizes)}")
check("J2: invariant subset sizes are {0,1,2,6,7,8}",
      inv_subset_sizes == {0, 1, 2, 6, 7, 8})
imag6 = [o for o in elem_orbits if len(o) == 6][0]
check("J3: the UNIQUE invariant 6-subset is the six imaginary units",
      imag6 == frozenset(Q8_ELEMS) - frozenset({ONE, NEG}))
closed6 = all(qmul(a, b) in imag6 for a in imag6 for b in imag6)
check("J4: the imaginary 6-set is NOT composition-closed (i*j=k in, i*i=-1 OUT)",
      not closed6 and qmul(I, I) not in imag6)
closure6 = q8.closure(imag6)
check("J5: its generated closure is ALL of Q8; hidden remainder = {+-1}, size 2",
      closure6 == frozenset(Q8_ELEMS)
      and closure6 - imag6 == frozenset({ONE, NEG}))
# which invariant subsets ARE composition-closed?
closed_inv = []
for r in range(1, len(elem_orbits) + 1):
    for combo in combinations(elem_orbits, r):
        S = frozenset(chain(*combo))
        if all(qmul(a, b) in S for a in S for b in S):
            closed_inv.append(S)
check("J6: composition-closed invariant subsets are EXACTLY the characteristic "
      "subgroups {1}, Z, Q8",
      sorted(len(s) for s in closed_inv) == [1, 2, 8])

# ----------------------------------------------------------------------------
# SSK  Aut(V4) transitive: no canonical Z2-factorization of ABCD; same S3
# ----------------------------------------------------------------------------
print("=" * 78)
print("SSK  ABCD = D2 x D2 is bookkeeping: Aut(V4) ~ S3 permutes the factors")
print("=" * 78)
# build V4 = Q8/Z as an explicit group of cosets
cos_elems = cosets
def cosmul(c1, c2):
    p = qmul(next(iter(c1)), next(iter(c2)))
    for c in cos_elems:
        if p in c:
            return c
    raise RuntimeError
idcoset = [c for c in cos_elems if ONE in c][0]
v4 = G("V4=Q8/Z", cos_elems, cosmul, idcoset)
auts_v4 = v4.automorphisms()
check("K1: |Aut(V4)| = 6 (= S3)", len(auts_v4) == 6)
invols_v4 = [c for c in cos_elems if c != idcoset]
orb_v4 = set(frozenset(map(lambda x: tuple(sorted(map(repr, f[x]))), invols_v4))
             for f in auts_v4)  # sanity container
one_orbit = set()
for f in auts_v4:
    one_orbit.add(tuple(sorted(map(repr, f[invols_v4[0]]))))
check("K2: Aut(V4) is TRANSITIVE on the 3 involutions of Q8/Z "
      "(no canonical D2 factor of ABCD)",
      len(one_orbit) == 3)
# the three involutions of Q8/Z are the images of the three C4's
c4_images = set()
for s in C4s:
    img = frozenset(frozenset({x, qmul(NEG, x)}) for x in s) - {frozenset(Zsub)}
    # each C4 = {1,-1,x,-x} maps to {Z, xZ}; its nonidentity image is xZ
    c4_images.add(next(iter(img)))
check("K3: the 3 involutions of Q8/Z are exactly the images of the 3 C4's "
      "(same S3 obstruction upstairs and downstairs)",
      c4_images == set(invols_v4))
# the induced Aut(Q8)-action on the layers: trivial on Z, S3 on Q8/Z
check("K4: induced Aut(Q8)-action on layer Z is TRIVIAL (canonical letters +-1); "
      "on layer Q8/Z it is S3 on {B,C,D} (no within-zone letter selection - "
      "matches owned selector NO-GO row 549)",
      all(f[NEG] == NEG for f in auts_q8) and len(perm_images) == 6)

# ----------------------------------------------------------------------------
# SSL  fingerprint census over ALL five groups of order 8
# ----------------------------------------------------------------------------
print("=" * 78)
print("SSL  Census: canonical alphabets of ALL five groups of order 8")
print("=" * 78)


def make_z8():
    els = list(range(8))
    return G("Z8", els, lambda a, b: (a + b) % 8, 0)


def make_z4z2():
    els = [(a, b) for a in range(4) for b in range(2)]
    return G("Z4xZ2", els,
             lambda x, y: ((x[0] + y[0]) % 4, (x[1] + y[1]) % 2), (0, 0))


def make_z2c3():
    els = [(a, b, c) for a in range(2) for b in range(2) for c in range(2)]
    return G("Z2^3", els,
             lambda x, y: tuple((x[i] + y[i]) % 2 for i in range(3)), (0, 0, 0))


def make_d4():
    els = [(r, s) for r in range(4) for s in range(2)]

    def mul(x, y):
        r1, s1 = x
        r2, s2 = y
        r = (r1 + (r2 if s1 == 0 else -r2)) % 4
        return (r, (s1 + s2) % 2)
    return G("D4", els, mul, (0, 0))


census = {}
for gg in (make_z8(), make_z4z2(), make_z2c3(), make_d4(), q8):
    assert gg.is_group()
    alpha, chars, auts, subs = canonical_alphabet(gg)
    iso_types = [p[3] for p in alpha]
    clean = (len(alpha) == 2
             and len(set(iso_types)) == 2
             and sorted(p[2] for p in alpha) == [2, 4])
    census[gg.name] = (len(alpha), alpha, clean, len(auts))
    print(f"  {gg.name:7s}: |Aut|={len(auts):3d}  canonical alphabet pairs = {alpha}"
          f"   CLEAN={clean}")

check("L1: Q8 census entry is clean (exactly 2, non-isomorphic, sizes {2,4})",
      census["Q8"][2])
check("L2: NEGATIVE CONTROL (can fail conclusion): D4 is NOT clean "
      "(5 pairs incl. a rival Z4 size-4 alphabet -> selection catalog needed)",
      not census["D4"][2] and census["D4"][0] == 5
      and "Z4" in [p[3] for p in census["D4"][1]])
check("L3: NEGATIVE CONTROL: Z8 is NOT clean (chain gives repeated iso-types)",
      not census["Z8"][2] and census["Z8"][0] >= 4)
check("L4: NEGATIVE CONTROL: Z4xZ2 is NOT clean",
      not census["Z4xZ2"][2])
check("L5: NEGATIVE CONTROL: Z2^3 has NO canonical layers at all "
      "(split/abelian case: the tower could not even start)",
      census["Z2^3"][0] == 0)
check("L6: Q8 is the UNIQUE group of order 8 whose canonical alphabet is clean",
      [n for n, v in census.items() if v[2]] == ["Q8"])
check("L7: |Aut| sanity: Z8:4, Z4xZ2:8, Z2^3:168, D4:8, Q8:24",
      census["Z8"][3] == 4 and census["Z4xZ2"][3] == 8
      and census["Z2^3"][3] == 168 and census["D4"][3] == 8
      and census["Q8"][3] == 24)

# ----------------------------------------------------------------------------
# SSM  tower kill matrix (over-base fork; scan bound DECLARED: z3 <= 21)
# ----------------------------------------------------------------------------
print("=" * 78)
print("SSM  Tower kill matrix (over-base fork, z3 <= 21)")
print("=" * 78)

ALPHA_SIZES = sorted(p[2] for p in alpha_q8)          # computed, NOT hardcoded
SQ_ORDERS = sq_orders                                  # computed above


def third_zone_verdict(x):
    """x = |X| of the candidate third-zone extension V9 |_| X, given the second
    zone already consumed the size-2 canonical layer.  Returns (ok, reason)."""
    if x == ALPHA_SIZES[1] and x in [p[2] for p in alpha_q8]:
        return True, "canonical layer Q8/Z (size 4) — the owned ABCD extension"
    if x not in SQ_ORDERS:
        return False, (f"size {x} is not a subquotient order of Q8 "
                       f"(orders={sorted(SQ_ORDERS)}; Lagrange)")
    if x == 8:
        return False, ("size 8 = Q8 itself: improper — repeats the base zone's "
                       "typing alphabet (V9 is Q8-typed) => CASE-2 copy kill "
                       "(NoExtension.lean:47)")
    if x == 1:
        return False, ("size 1: marker-only extension = the owned V10 'extra "
                       "hidden marker' exclusion (BOOK_01:1556)")
    if x == 2:
        return False, ("size 2 again: the Z2 layer is already consumed at V11 — "
                       "two indistinguishable realizations of ONE canonical "
                       "capacity => CASE-2 copy kill (NoExtension.lean:47)")
    if x == 4:
        return True, "size 4"
    return False, "unreachable"


survivors = []
print("  scan of 3-zone towers (9, 11, z3), z3 = 9+x, x = 1..12 (z3 <= 21):")
for x in range(1, 13):
    z3 = 9 + x
    ok, reason = third_zone_verdict(x)
    status = "SURVIVES" if ok else "DIES"
    print(f"    z3 = {z3:2d} (x = {x:2d}): {status:8s} {reason}")
    if ok:
        survivors.append(z3)
check("M1: unique survivor z3 = 13 => tower (9,11,13) forced",
      survivors == [13])
check("M2: (9,11,15) DIES by computed Lagrange (6 not a subquotient order)",
      not third_zone_verdict(6)[0] and "Lagrange" in third_zone_verdict(6)[1])
check("M3: (9,11,17) DIES (size 8 improper: base-type repeat)",
      not third_zone_verdict(8)[0])
check("M4: (9,11,11) DIES (Z2 layer re-use: CASE-2)",
      not third_zone_verdict(2)[0])
check("M5: POSITIVE CONTROL: the owned tower (9,11,13) passes every prong",
      third_zone_verdict(4)[0])

# the six-subset escape named explicitly at z3 = 15:
check("M6: the ONLY catalog-free size-6 role-object (imaginary 6-set) is not an "
      "alphabet: not composition-closed, closure = whole Q8 with hidden {+-1} "
      "(computed SSJ) — the V15 escape has NO canonical realization",
      not closed6 and closure6 == frozenset(Q8_ELEMS))

# NEGATIVE CONTROL on the WHOLE PIPELINE (can fail the conclusion): rerun the
# tower scan with D4 as the role group.  D4 has FOUR canonical pairs including
# two distinct size-4 alphabets (Z4 and V4) and two distinct size-2 alphabets:
# the third-zone typing is NOT forced (selecting among rival canonical
# alphabets of equal size = an instance catalog).  If D4 gave a forced unique
# typing too, the Q8-fingerprint conclusion would FAIL here.
d4_alpha = census["D4"][1]
d4_size4 = [p for p in d4_alpha if p[2] == 4]
d4_size2 = [p for p in d4_alpha if p[2] == 2]
check("M7: NEGATIVE CONTROL: with D4 as role group the third zone has TWO rival "
      "canonical size-4 alphabets (Z4 vs V4) and the second zone THREE rival "
      "size-2 realizations of one iso-type => tower typing NOT forced (needs a "
      "catalog); the forcing is Q8-specific",
      len(d4_size4) == 2 and len(set(p[3] for p in d4_size4)) == 2
      and len(d4_size2) == 3 and set(p[3] for p in d4_size2) == {"Z2"})

# COUNT cross-check: the number of canonical layers of Q8 equals the owned
# extension COUNT (= 2 = 3 zones - 1 base, D0-TOWER-STOP-NOEXT-001 reading).
check("M8: number of canonical layers (computed = 2) matches owned COUNT-3 "
      "(3 zones - 1 base); after both layers the characteristic chain 1<Z<Q8 "
      "is EXHAUSTED => no 4th zone alphabet exists",
      len(alpha_q8) == 2 and len(chars_q8) == 3)

# ----------------------------------------------------------------------------
# SSN  SKEPTIC #1 KILL-CONTROLS (added post-verdict, accepted in full).
#      These checks PASS by CONFIRMING the counter-objects that FALSIFY the
#      memo's original closure headline. A future repair that makes any of
#      them fail must be reported to the owner (it would mean the counter-
#      object analysis itself broke, not that the closure revives).
# ----------------------------------------------------------------------------
print("=" * 78)
print("SSN  Skeptic #1 kill-controls: canonical role-DERIVED objects that")
print("     escape the trichotomy (=> KILLED-AS-CLOSURE)")
print("=" * 78)

# N1: Sub(Q8) — size 6, Aut-invariant as a family, stable under meet/join.
sub_family = set(subs_q8)
aut_stable = all(frozenset(f[x] for x in s) in sub_family
                 for f in auts_q8 for s in subs_q8)
meets_ok = all((a & b) in sub_family for a in subs_q8 for b in subs_q8)
joins_ok = all(q8.closure(a | b) in sub_family for a in subs_q8 for b in subs_q8)
check("N1: KILL-CONTROL: Sub(Q8) is a canonical role-derived object of SIZE 6 "
      "(Aut-invariant family; stable under meet and join; every member normal "
      "by the owned Dedekind property) — escapes prongs 1-4",
      len(subs_q8) == 6 and aut_stable and meets_ok and joins_ok)

# N2: Out(Q8) — size 6.
out_order = len(auts_q8) // len(inns_q8)
check("N2: KILL-CONTROL: Out(Q8) has SIZE 6 (= |Aut|/|Inn| = 24/4) — a second "
      "canonical role-derived size-6 object",
      out_order == 6)

# N3: the characteristic chain — size 3.
check("N3: KILL-CONTROL: the characteristic chain {1, Z, Q8} is a canonical "
      "role-derived object of SIZE 3 (odd size, outside the subquotient orders)",
      len(chars_q8) == 3)

# N4: the frame error — the memo's own survivor Q8/Z is NOT an element-subset
#     of Q8, so the SSJ scan frame (element-subsets) never contained the type
#     of the survivors, let alone the rivals.
coset_elems_are_subsets = all(isinstance(c, frozenset) and c <= frozenset(Q8_ELEMS)
                              for c in cosets)
q8_over_z_is_element_subset = frozenset(cosets) <= frozenset(Q8_ELEMS)
check("N4: KILL-CONTROL (frame error, trap f): the survivor Q8/Z is a set of "
      "COSETS, not an element-subset of Q8 — SSJ's totality frame excluded the "
      "survivors' own type",
      coset_elems_are_subsets and not q8_over_z_is_element_subset)

# N5: the falsification itself — the original headline (a) said "NO size-6
#     object in the role algebra AT ALL"; N1/N2 exhibit two. This control
#     FAILS the original conclusion (it passes by confirming the kill).
check("N5: KILL: canonical role-derived size-6 objects EXIST (N1, N2) => the "
      "original headline (a) is FALSE as stated; only 'no size-6 SUBQUOTIENT' "
      "(SSI) survives",
      len(subs_q8) == 6 and out_order == 6 and 6 not in sq_orders)

# N6: partition-grammar discriminator (memo SSOWNERSHIP-CHECK): every OWNED
#     alphabet is a partition-block family realized as added vertices, while
#     every counter-object is a NON-partition family.
#     (a) the 4 cosets of Z partition Q8 (disjoint, cover);
cosets_disjoint = all(a == b or not (a & b) for a in cosets for b in cosets)
cosets_cover = frozenset().union(*cosets) == frozenset(Q8_ELEMS)
#     (b) Z's letters are elements (trivially partition Z itself);
#     (c) Sub(Q8) members pairwise OVERLAP in the identity => never a partition;
subs_overlap = all(ONE in (a & b) for a in subs_q8 for b in subs_q8)
#     (d) the characteristic chain is NESTED, not disjoint;
chain_nested = chars_q8[0] < chars_q8[1] < chars_q8[2]
#     (e) Out's letters partition Aut(Q8), NOT the role material Q8.
check("N6: partition-grammar discriminator: owned alphabets are partition-block "
      "families of role material (cosets of Z partition Q8: disjoint+cover), "
      "while Sub(Q8) members pairwise overlap in 1 and the chain is nested — "
      "the sharpened missing object (alphabet-grammar clause) separates exactly "
      "these; NOT owned as a rule (memo SSOWNERSHIP-CHECK), so no closure",
      cosets_disjoint and cosets_cover and subs_overlap and chain_nested)

# ----------------------------------------------------------------------------
# verdict
# ----------------------------------------------------------------------------
print("=" * 78)
n_pass = sum(1 for _, ok in CHECKS if ok)
n_tot = len(CHECKS)
all_ok = n_pass == n_tot
print(f"CHECKS: {n_pass}/{n_tot} PASS")
print("VERDICT:", "KILLED-AS-CLOSURE (computation layer holds; counter-objects "
      "confirmed; GAP-E stays OPEN)" if all_ok else "FAILURE (report to owner)")
sys.exit(0 if all_ok else 1)
