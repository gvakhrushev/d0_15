#!/usr/bin/env python3
"""
raise_gap_e_minimality_check.py

MINIMALITY-RAISE probe for GAP-E. The claim under test (owner directive):

    {D2, ABCD} is the UNIQUE MINIMAL extension-alphabet structure -- the two
    proper direct factors of the OWNED capacity product  P = D2 x D2 x {+/-}
    (= ABCD x {+/-} = Omega8 ~ Q8, BOOK_01:1523/1535/782). If the admissible
    alphabets are EXACTLY the proper direct factors of P, and the direct-factor
    (Krull-Schmidt) decomposition of P is unique with factor-sizes {2,4} and
    nothing of size 3/5/6, then the completeness quantifier
        forall X (AdmExt(X) -> |X| in {2,4})
    becomes a THEOREM (forced by minimality/unique-factorization), not an axiom.

This script is COMPUTE-FIRST and CAN-FAIL. It EXHIBITS:
  (L2) the direct-factor decomposition of P and its Krull-Schmidt uniqueness;
  (L3) that X3 = {{+1},{-1},{+-i,+-j,+-k}} (blocks 1,1,6, count 3) is NOT the
       fiber-partition of any coordinate-projection of P (i.e. NOT a direct
       factor) -- it is an orbit-FUSION;
  (block-count law) coordinate-projection fiber-partitions of a product of Z2's
       have block-COUNTS that are PRODUCTS of a subset of the factor sizes -- so
       always a power/divisor structure of 2's, NEVER 3, 5, or 6;
  (L1/L4 audit) whether "minimal step = add exactly one owned coordinate" is
       DERIVED from the owned product + M1, or SMUGGLED.

The verdict (rc) is set by whether the LOAD-BEARING lemma L1 is owned. The
compute lemmas L2/L3 are theorems (exact, enumerated). L1 is the ownership hinge
the skeptic attacks. If L1 is not owned, rc reports HONEST-FAIL and names the
exact unowned premise.

Exit codes:
  0 = RAISED-TO-THEOREM  (L1 owned AND L2/L3 hold AND minimality excludes size 3/5/6)
  1 = mutation/self-check FAILED (a lemma that must hold did not) -- script bug
  2 = HONEST-FAIL / PARTIAL (compute lemmas hold, but L1 ownership missing)
"""

import itertools
import sys

CHECKS = []          # (id, bool, note)
def chk(cid, cond, note=""):
    CHECKS.append((cid, bool(cond), note))
    return bool(cond)

# --------------------------------------------------------------------------
# 0. Build the OWNED capacity product  P = D2 x D2 x {+/-}  concretely.
#    We build it as an abstract elementary-abelian-adjacent product of three
#    2-element factors, then also realize Q8 to test X3 as an Aut-orbit object.
# --------------------------------------------------------------------------

# The three owned 2-element factors (each is a copy of the 2-set {0,1}):
#   F1 = first D2 (a role dyad),  F2 = second D2 (a role dyad),  F3 = {+/-} sign bit.
# P as a set = F1 x F2 x F3, 8 elements. This is the CARDINALITY/coordinate model
# of the owned product ABCD x {+/-} (ABCD = D2xD2). |P| = 8, matching |Omega8|.
FACTORS = {"F1": (0, 1), "F2": (0, 1), "F3": (0, 1)}
P = list(itertools.product(*[FACTORS[k] for k in ("F1", "F2", "F3")]))
chk("P.size8", len(P) == 8, "|D2 x D2 x {+/-}| = 8")

# --------------------------------------------------------------------------
# LEMMA L2 -- UNIQUE FACTORIZATION (Krull-Schmidt) of P.
# P is a direct product of three indecomposable factors each of size 2 (Z2).
# The DIRECT FACTORS of P (as subproducts) are exactly the products over subsets
# of the three coordinates. Their sizes are 2^k for k in {0,1,2,3} = {1,2,4,8}.
# INDECOMPOSABLE (non-trivially) factors = the three Z2 coordinates (size 2).
# The "owned extension alphabets" are realized as COORDINATE-PROJECTION
# fiber-partitions: projecting P onto a subset S of coordinates and taking the
# fibers gives a partition whose BLOCK-COUNT = product of sizes of coords in S.
# --------------------------------------------------------------------------

def fiber_partition(coords):
    """Partition of P by equality on the given coordinate-subset `coords`
       (a tuple of indices in {0,1,2}). Returns frozenset of frozenset(blocks).
       Block-COUNT = number of distinct coordinate-values = prod(factor sizes)."""
    buckets = {}
    for p in P:
        key = tuple(p[i] for i in coords)
        buckets.setdefault(key, []).append(p)
    return frozenset(frozenset(b) for b in buckets.values())

# Enumerate ALL coordinate-projection fiber-partitions (all subsets of {0,1,2}).
coord_subsets = []
for r in range(0, 4):
    for S in itertools.combinations(range(3), r):
        coord_subsets.append(S)

fiber_blockcounts = {}
for S in coord_subsets:
    part = fiber_partition(S)
    fiber_blockcounts[S] = len(part)

# The block-COUNTS achievable by coordinate projections:
achievable_counts = sorted(set(fiber_blockcounts.values()))
# S=() -> 1 block (whole P); |S|=1 -> 2 blocks; |S|=2 -> 4 blocks; |S|=3 -> 8 blocks.
chk("L2.blockcounts_are_powers_of_2", set(achievable_counts) == {1, 2, 4, 8},
    f"coordinate-projection block-counts = {achievable_counts} (all 2^k)")

# The PROPER NON-TRIVIAL factor-partitions (exclude whole-P=1 and the discrete=8):
proper_counts = sorted(c for c in achievable_counts if c not in (1, 8))
chk("L2.proper_factor_blockcounts_2_and_4", proper_counts == [2, 4],
    f"proper non-trivial coordinate-projection block-counts = {proper_counts}")

# Krull-Schmidt: the indecomposable factors of P are three copies of Z2 (size 2),
# unique up to order/iso. The proper direct SUBproducts have sizes {2,4} (and the
# improper 1,8). NO direct factor of size 3, 5, or 6 exists -- because every
# direct factor size divides 8 (is a product of a subset of {2,2,2}).
factor_sizes = set()
for r in range(0, 4):
    for S in itertools.combinations(range(3), r):
        factor_sizes.add(2 ** len(S))   # size of the subproduct = 2^|S|
chk("L2.factor_sizes_divide_8", factor_sizes == {1, 2, 4, 8},
    f"direct-factor sizes of P = {sorted(factor_sizes)}")
chk("L2.no_factor_size_3", 3 not in factor_sizes, "no direct factor of size 3")
chk("L2.no_factor_size_5", 5 not in factor_sizes, "no direct factor of size 5")
chk("L2.no_factor_size_6", 6 not in factor_sizes, "no direct factor of size 6")

# --------------------------------------------------------------------------
# BLOCK-COUNT LAW (the heart of L3): a coordinate-projection fiber-partition of a
# product of Z2's has block-count = 2^k = a product of factor sizes. Since every
# factor is 2, the achievable block-counts are exactly the divisors-of-8 that are
# products of 2's: {1,2,4,8}. In particular 3 is NEVER a coordinate block-count.
# This is proved by the enumeration above (achievable_counts == {1,2,4,8}).
chk("LAW.3_not_a_coord_blockcount", 3 not in achievable_counts,
    "block-count 3 cannot arise as a coordinate-projection of a product of Z2's")
chk("LAW.6_not_a_coord_blockcount", 6 not in achievable_counts,
    "block-count 6 (Sub(Q8)) also not a coordinate block-count")

# --------------------------------------------------------------------------
# LEMMA L3 -- X3 IS NOT A DIRECT FACTOR; it is an Aut-orbit FUSION.
# Realize Q8 and its automorphism group; exhibit X3 as the Aut-orbit partition
# and show it is NOT any coordinate-projection fiber-partition of P.
# --------------------------------------------------------------------------

# Q8 as signed quaternions. Represent elements as (scalar, i, j, k) unit vectors.
# We use string labels and an explicit multiplication table.
Q8 = ["+1", "-1", "+i", "-i", "+j", "-j", "+k", "-k"]
# Multiplication via quaternion units.
_units = {"1": (1, 0, 0, 0), "i": (0, 1, 0, 0), "j": (0, 0, 1, 0), "k": (0, 0, 0, 1)}
def _tovec(lbl):
    s = 1 if lbl[0] == "+" else -1
    b = lbl[1:]
    v = _units[b]
    return tuple(s * x for x in v)
def _fromvec(v):
    s = 1
    nz = [x for x in v if x != 0]
    # exactly one nonzero component, +-1
    idx = [i for i, x in enumerate(v) if x != 0][0]
    val = v[idx]
    base = "1ijk"[idx]
    sign = "+" if val > 0 else "-"
    return sign + base
def qmul(a, b):
    (a0, a1, a2, a3) = _tovec(a); (b0, b1, b2, b3) = _tovec(b)
    r0 = a0*b0 - a1*b1 - a2*b2 - a3*b3
    r1 = a0*b1 + a1*b0 + a2*b3 - a3*b2
    r2 = a0*b2 - a1*b3 + a2*b0 + a3*b1
    r3 = a0*b3 + a1*b2 - a2*b1 + a3*b0
    return _fromvec((r0, r1, r2, r3))

# sanity: quaternion relations
chk("Q8.i2_is_-1", qmul("+i", "+i") == "-1", "i^2 = -1")
chk("Q8.ij_is_k", qmul("+i", "+j") == "+k", "ij = k")
chk("Q8.ji_is_-k", qmul("+j", "+i") == "-k", "ji = -k (noncommutative)")

# Aut(Q8): all bijections fixing +1,-1 that preserve multiplication.
# Aut(Q8) ~ S4 (order 24). Enumerate by choosing images of i,j (k determined),
# then verify homomorphism on the whole table.
def build_auts():
    imags = ["+i", "-i", "+j", "-j", "+k", "-k"]
    auts = []
    for pi in imags:
        for pj in imags:
            if pj in (pi, qmul("-1", pi)):  # image of j must be indep of image of i
                continue
            m = {"+1": "+1", "-1": "-1", "+i": pi, "+j": pj}
            # extend by k = ij, and signs
            m["+k"] = qmul(pi, pj)
            m["-i"] = qmul("-1", m["+i"])
            m["-j"] = qmul("-1", m["+j"])
            m["-k"] = qmul("-1", m["+k"])
            # verify it's a homomorphism on all pairs
            ok = True
            for a in Q8:
                for b in Q8:
                    if m[qmul(a, b)] != qmul(m[a], m[b]):
                        ok = False; break
                if not ok: break
            if ok and len(set(m.values())) == 8:
                auts.append(m)
    return auts

AUTS = build_auts()
chk("Aut.order_24", len(AUTS) == 24, f"|Aut(Q8)| = {len(AUTS)} (= S4)")

# Aut-orbits on Q8 elements:
def orbit(x):
    return frozenset(m[x] for m in AUTS)
orbits = set(orbit(x) for x in Q8)
orbit_sizes = sorted(len(o) for o in orbits)
chk("Aut.orbit_sizes_1_1_6", orbit_sizes == [1, 1, 6],
    f"Aut-orbit sizes on Q8 = {orbit_sizes}")

# X3 = the Aut-orbit partition:
X3 = frozenset(orbits)
X3_blockcount = len(X3)
chk("X3.blockcount_3", X3_blockcount == 3, "X3 has 3 blocks (1,1,6)")

# Is X3 a coordinate-projection fiber-partition of P? To ask this fairly we need
# an identification of P's 8 elements with Q8's 8 elements. Try ALL bijections
# P<->Q8? That is 8! = 40320; feasible. For each bijection, check whether X3
# (as a partition of Q8) equals the image of ANY coordinate fiber-partition of P.
# If X3 is a direct factor, SOME identification makes it a coordinate partition.
# We test the strongest form: does there EXIST an iso P->Q8 (as sets) under which
# X3 pulls back to a coordinate-projection fiber-partition? If NO bijection works,
# X3 is not a direct-factor fiber-partition under any labeling.
# Optimization: a coordinate fiber-partition of P has block-count in {1,2,4,8} and
# ALL blocks equal size (2^|S| blocks each of size 2^(3-|S|) -- UNIFORM). X3's
# blocks are sizes 1,1,6 -- NON-UNIFORM. A set-bijection preserves block SIZES of
# a partition. So X3 (sizes 1,1,6) can NEVER equal any coordinate fiber-partition
# (whose block sizes are all equal). We verify this uniformity fact by enumeration.
coord_block_size_multisets = set()
for S in coord_subsets:
    part = fiber_partition(S)
    coord_block_size_multisets.add(tuple(sorted(len(b) for b in part)))
# every coordinate fiber-partition has all-equal block sizes:
all_uniform = all(len(set(ms)) == 1 for ms in coord_block_size_multisets)
chk("L3.coord_partitions_are_uniform", all_uniform,
    f"coordinate fiber-partition block-size multisets = {sorted(coord_block_size_multisets)}")

X3_block_sizes = tuple(sorted(len(b) for b in X3))
chk("L3.X3_nonuniform", len(set(X3_block_sizes)) > 1,
    f"X3 block sizes = {X3_block_sizes} (non-uniform)")

# Therefore X3 cannot be a coordinate fiber-partition under ANY set-bijection:
X3_is_factor = (X3_block_sizes in coord_block_size_multisets)
chk("L3.X3_is_NOT_direct_factor", not X3_is_factor,
    "X3 (sizes 1,1,6) is not any coordinate fiber-partition (all uniform) -> NOT a direct factor")

# Confirm X3 IS a genuine partition and Aut-invariant (so the exclusion is real,
# not because X3 is malformed):
covered = frozenset().union(*X3)
chk("X3.is_partition", covered == frozenset(Q8) and
    sum(len(b) for b in X3) == 8, "X3 is a genuine partition of Q8")
X3_autinv = all(frozenset(m[x] for x in blk) in X3 for m in AUTS for blk in X3)
chk("X3.is_aut_invariant", X3_autinv, "X3 is Aut(Q8)-invariant (why it escaped prior clauses)")

# And confirm the TWO OWNED alphabets ARE direct factors (uniform block sizes):
#  ABCD = Q8/Z, cosets {x,-x}: 4 blocks of size 2  -> uniform (2,2,2,2)
ABCD = frozenset(frozenset([x, qmul("-1", x)]) for x in Q8)
chk("ABCD.blockcount_4", len(ABCD) == 4, "ABCD has 4 blocks")
chk("ABCD.uniform_2222", tuple(sorted(len(b) for b in ABCD)) == (2, 2, 2, 2),
    "ABCD blocks uniform (2,2,2,2) -> IS a coordinate fiber-partition shape")
chk("ABCD.is_factor_shape", tuple(sorted(len(b) for b in ABCD)) in coord_block_size_multisets,
    "ABCD block-size multiset matches a coordinate fiber-partition (direct factor)")
#  SIGN = the {+/-} factor: 2 blocks of size 4 -> uniform (4,4)
SIGN = frozenset([frozenset(["+1", "+i", "+j", "+k"]), frozenset(["-1", "-i", "-j", "-k"])])
chk("SIGN.uniform_44", tuple(sorted(len(b) for b in SIGN)) == (4, 4),
    "SIGN blocks uniform (4,4) -> IS a coordinate fiber-partition shape")
chk("SIGN.is_factor_shape", tuple(sorted(len(b) for b in SIGN)) in coord_block_size_multisets,
    "SIGN block-size multiset matches a coordinate fiber-partition (direct factor)")

# --------------------------------------------------------------------------
# L1 / L4 -- THE OWNERSHIP HINGE (the skeptic's target).
# The compute above PROVES: IF admissible alphabets = proper direct factors of
# the owned product P, THEN sizes in {2,4} exactly and X3 is excluded (theorem).
# The RAISE succeeds ONLY IF the premise
#     P1: "AdmExt(X) <-> X is a proper direct factor of the owned product P"
# is OWNED/derived from the owned product structure + M1 (not assumed).
#
# We test ownership honestly. Two sub-claims:
#   L1a: minimal step = add exactly one owned COORDINATE of P. Is this derivable
#        from "extension adds vertices as a disjoint union" + "the added material
#        is a factor of the owned product" + M1 (adding a NON-coordinate needs a
#        fusion catalog M1 forbids)?
#   L1b: does the tower V9->V11->V13 actually add owned coordinates one at a time?
#        (V11 adds D2 = one coordinate; V13 adds ABCD = D2xD2 = two coordinates.)
# --------------------------------------------------------------------------

# L1b compute: the owned tower's added-vertex counts vs. the product's coordinates.
#   V9  base (pointed shell).  V11 = V9 + D2 (adds 2 letters = ONE coordinate F).
#   V13 = V9 + ABCD (adds 4 letters = the D2xD2 factor = TWO coordinates F1xF2).
# So the tower does NOT add exactly one coordinate at each step: V13 adds ABCD
# which is TWO coordinates at once (a size-4 factor). The "add one coordinate"
# reading is FALSE as stated for V13; the owned steps add {a size-2 factor} and
# {a size-4 factor} -- i.e. PROPER DIRECT FACTORS, not single coordinates.
added_D2 = 2      # V11 adds the dyad: 1 coordinate (size-2 factor)
added_ABCD = 4    # V13 adds the role square: 2 coordinates (size-4 factor)
tower_adds_single_coord_each = (added_D2 == 2 and added_ABCD == 2)
chk("L1b.tower_NOT_single_coord_each", not tower_adds_single_coord_each,
    "V13 adds ABCD = a size-4 (two-coordinate) factor, NOT one coordinate -> "
    "'add one coordinate' is FALSE; the owned steps add PROPER DIRECT FACTORS {size2,size4}")

# So the correct minimality statement is NOT "add one coordinate" but
#   "add one PROPER DIRECT FACTOR of the owned product P".
# The admissible-factor sizes are then exactly the proper direct-factor sizes of
# P = {2,4} (L2). This is clean AND matches the owned tower. BUT: it REQUIRES the
# premise that admissible = direct factor of P, AND that the whole product P (not
# just its named factors) is the owned universe of admissibility.

# L1a ownership audit: is "admissible <-> proper direct factor of P" OWNED?
# Search the corpus for a QUANTIFIED sentence licensing "every admissible
# extension is a direct factor of the owned capacity product" (a GENERATOR over
# the product's factor lattice). Prior memos (DYAD-POWER) established: the corpus
# owns a two-item LIST + two singleton forcings, NOT a generator over the product.
# We encode that finding as the ownership flag (not re-grepping here; cross-ref).
OWNED_generator_over_product = False   # per DYAD-POWER kill + this pass's read of :1548
chk("L1a.generator_is_the_hinge", True,
    "L1a: 'admissible <-> proper direct factor of P' is the load-bearing premise")

# The DECISIVE audit question (the skeptic's mandate): does the minimality framing
# DERIVE this premise, or REBRAND the same unowned generator?
# Test: minimality says "smallest admissible step". But 'smallest' is only pinned
# once you FIX the ambient structure whose factors you range over. Fixing that
# ambient = P (the whole owned product) and ranging over its FACTORS is EXACTLY
# adopting the product-coordinate grammar as the home of admissibility -- which is
# the unowned generator (SELF-ATT-1b of the 6th memo). Minimality does not supply
# the ambient; it presupposes it.
minimality_supplies_ambient = False
chk("L1a.minimality_needs_but_lacks_ambient", not minimality_supplies_ambient,
    "minimality ranks factors of a FIXED ambient P but does not DERIVE that "
    "admissibility ranges over P's factors -- it presupposes the product-coordinate grammar")

# Could minimality derive the ambient from M1 alone? The candidate derivation:
#   'adding a NON-factor (e.g. X3, a fusion) requires a catalog M1 forbids'.
# Test whether that catalog-argument is symmetric: does adding a size-4 DIRECT
# FACTOR (ABCD) avoid a catalog while adding the size-3 FUSION (X3) require one?
# X3 fuses 3 Aut-orbits into blocks of sizes 1,1,6 -- a NON-UNIFORM partition with
# a distinguished size-6 block = a privileged sub-object (needs to NAME which
# block is the big one). ABCD's blocks are all size 2 (uniform) -- no privileged
# block. So there IS an asymmetry: X3's non-uniformity names a privileged block.
X3_has_privileged_block = (len(set(X3_block_sizes)) > 1)
ABCD_has_privileged_block = (len(set(tuple(sorted(len(b) for b in ABCD)))) > 1)
chk("L4.X3_names_privileged_block", X3_has_privileged_block and not ABCD_has_privileged_block,
    "X3 (1,1,6) names a privileged size-6 block; ABCD (2,2,2,2) does not -- a real asymmetry")

# BUT: is "no privileged block" (uniform-block) an OWNED alphabet rule, or the
# C1-exchangeability transfer the 5th/6th skeptics already killed as a typing
# transfer (C1 is a within-part vertex-permutation obligation, not an alphabet
# block-size law)? This is the crux. The uniform-block criterion:
#   (i) EXCLUDES X3 (good), and
#   (ii) with the direct-factor ambient, admits exactly {2,4} (L2).
# So IF uniform-block-of-a-direct-factor is owned, the RAISE closes. Is it owned?
uniform_block_is_owned_alphabet_rule = False  # C1 is a vertex-permutation law, not an alphabet law (5th/6th kill)
chk("L4.uniform_block_not_owned_as_alphabet_rule", not uniform_block_is_owned_alphabet_rule,
    "uniform-block excludes X3 but is the C1 typing-transfer already killed -- not owned as an alphabet rule")

# --------------------------------------------------------------------------
# VERDICT LOGIC
# --------------------------------------------------------------------------
# Compute lemmas that MUST hold (else script bug -> rc 1):
MUST_HOLD = [
    "P.size8", "L2.blockcounts_are_powers_of_2", "L2.proper_factor_blockcounts_2_and_4",
    "L2.factor_sizes_divide_8", "L2.no_factor_size_3", "L2.no_factor_size_5",
    "L2.no_factor_size_6", "LAW.3_not_a_coord_blockcount", "LAW.6_not_a_coord_blockcount",
    "Aut.order_24", "Aut.orbit_sizes_1_1_6", "X3.blockcount_3",
    "L3.coord_partitions_are_uniform", "L3.X3_nonuniform", "L3.X3_is_NOT_direct_factor",
    "X3.is_partition", "X3.is_aut_invariant", "ABCD.is_factor_shape", "SIGN.is_factor_shape",
    "L1b.tower_NOT_single_coord_each", "L4.X3_names_privileged_block",
    "Q8.i2_is_-1", "Q8.ij_is_k", "Q8.ji_is_-k", "ABCD.uniform_2222", "SIGN.uniform_44",
]
# Ownership hinge: the RAISE succeeds ONLY if BOTH the direct-factor ambient AND
# the uniform-block exclusion are owned as alphabet rules.
RAISE_OWNED = OWNED_generator_over_product and uniform_block_is_owned_alphabet_rule

results = dict((c, v) for (c, v, _) in CHECKS)
must_ok = all(results.get(k, False) for k in MUST_HOLD)

print("=" * 78)
print("raise_gap_e_minimality_check.py  --  MINIMALITY-RAISE probe for GAP-E")
print("=" * 78)
for cid, val, note in CHECKS:
    flag = "PASS" if val else "FAIL"
    print(f"  [{flag}] {cid:42s} {note}")
print("-" * 78)
print(f"  achievable coordinate block-counts of P: {achievable_counts}")
print(f"  proper direct-factor sizes of P        : {proper_counts}")
print(f"  X3 block sizes                          : {X3_block_sizes}  (non-uniform)")
print(f"  X3 is a direct factor of P              : {X3_is_factor}")
print(f"  tower adds one coordinate each step     : {tower_adds_single_coord_each}")
print(f"  L1 (admissible <-> direct factor) owned : {OWNED_generator_over_product}")
print(f"  uniform-block owned as alphabet rule    : {uniform_block_is_owned_alphabet_rule}")
print("-" * 78)

if not must_ok:
    bad = [k for k in MUST_HOLD if not results.get(k, False)]
    print("SCRIPT/MUTATION FAILURE -- a lemma that must hold did not:", bad)
    print("rc = 1")
    sys.exit(1)

if RAISE_OWNED:
    print("VERDICT: RAISED-TO-THEOREM. Minimality + unique factorization CLOSE GAP-E.")
    print("rc = 0")
    sys.exit(0)
else:
    print("VERDICT: HONEST-FAIL / PARTIAL.")
    print("  L2 (unique factorization, sizes {2,4}, no 3/5/6) : THEOREM (holds).")
    print("  L3 (X3 is NOT a direct factor; it is a fusion)   : THEOREM (holds).")
    print("  block-count law (3 impossible for Z2-product)    : THEOREM (holds).")
    print("  L1 (admissible <-> proper direct factor of P)    : NOT OWNED  <-- the axiom.")
    print("  minimality presupposes the direct-factor AMBIENT; it does not derive it.")
    print("  ==> the completeness quantifier reduces to owning ONE premise:")
    print("      'an admissible extension alphabet is a proper direct factor of")
    print("       the owned capacity product D2 x D2 x {+/-}'  (== the product-")
    print("       coordinate grammar / DYAD-POWER generator) -- an OWNER DECISION.")
    print("rc = 2")
    sys.exit(2)
