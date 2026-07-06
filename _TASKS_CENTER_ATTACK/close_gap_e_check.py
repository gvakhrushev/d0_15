#!/usr/bin/env python3
# close_gap_e_check.py — can-fail computational spine for CLOSE_GAP_E_MEMO.md
# =============================================================================
# VERDICT: KILLED-AS-CLOSURE (Skeptic #1, 2026-07-06). This script was written to
# TEST a candidate GAP-E closure and, applied honestly, it KILLS it. It now
# EXHIBITS the killing object rather than confirming a hardcoded answer.
#
# WHAT SURVIVES (computed, real): the DERIVED PARTITION RULE
#     (PARTITION-RULE)  an admissible extension alphabet is a set of added
#     vertices = addressable record quanta occupying PAIRWISE-DISJOINT addresses
#     => a PARTITION-BLOCK family of the role material.
# excludes the three ORIGINAL counter-objects Sub(Q8), Out(Q8), chain{1,Z,Q8}
# (R4b.*). This part is an assembly-grade owned-schema transfer, retained.
#
# WHAT IS KILLED (the closure): the SIZE clause. A canonical (Aut-invariant)
# size-3 partition X3 = {{+1},{-1},{+-i,+-j,+-k}} (the Aut-ORBIT partition) IS a
# partition and IS Aut-invariant, so it passes both the partition rule and the
# "canonical" clause -- yet has size 3 => z3=12. The window upper bound is NOT
# sealed. R5.* EXHIBITS X3 and the full enumeration of Aut-invariant partitions
# (block-counts include 3). The earlier "admissible_sizes={2,4}" was a hardcoded
# literal (compute-first violation) + a silent narrowing of "canonical" to
# "coset-partition-of-characteristic-subgroup" that is NOT owned and is applied
# inconsistently (the kept size-2 Z-split is itself not such a coset partition).
#
# CAN-FAIL DISCIPLINE: the exit code is KILLED (rc=2) iff the killing object X3
# is confirmed present; the surviving structure checks (R4b) still pass; and the
# size clause is confirmed NON-forced. Nothing reads {2,4}/13/tower as input.
# =============================================================================

from itertools import product
from fractions import Fraction  # exact only; no float anywhere

# ---------------------------------------------------------------------------
# Q8 as integer-quaternion tuples (w,x,y,z). Owned iso A<->1,B<->i,C<->j,D<->k.
# ---------------------------------------------------------------------------
ONE  = (1,0,0,0);  mONE = (-1,0,0,0)
I    = (0,1,0,0);  mI   = (0,-1,0,0)
J    = (0,0,1,0);  mJ   = (0,0,-1,0)
K    = (0,0,0,1);  mK   = (0,0,0,-1)
Q8 = [ONE,mONE,I,mI,J,mJ,K,mK]

def qmul(a,b):
    w1,x1,y1,z1=a; w2,x2,y2,z2=b
    return (w1*w2-x1*x2-y1*y2-z1*z2,
            w1*x2+x1*w2+y1*z2-z1*y2,
            w1*y2-x1*z2+y1*w2+z1*x2,
            w1*z2+x1*y2-y1*x2+z1*w2)

def qinv(a):  # unit quaternion inverse = conjugate
    w,x,y,z=a; return (w,-x,-y,-z)

results=[]
def check(name, cond):
    results.append((name, bool(cond)))
    return bool(cond)

# ---------------------------------------------------------------------------
# 0. sanity: Q8 is a group, |Q8|=8, one involution (-1), nonabelian
# ---------------------------------------------------------------------------
check("Q0.card8", len(set(Q8))==8)
closed = all(qmul(a,b) in set(Q8) for a in Q8 for b in Q8)
check("Q0.closed", closed)
involutions=[g for g in Q8 if g!=ONE and qmul(g,g)==ONE]
check("Q0.one_involution", involutions==[mONE])
check("Q0.nonabelian", qmul(I,J)!=qmul(J,I))

# ---------------------------------------------------------------------------
# 1. Subgroup lattice: exactly 6 subgroups; the three C4 = <i>,<j>,<k>; center Z
# ---------------------------------------------------------------------------
def generated(seed):
    S=set(seed)|{ONE}
    changed=True
    while changed:
        changed=False
        for a in list(S):
            for b in list(S):
                p=qmul(a,b)
                if p not in S: S.add(p); changed=True
                pi=qinv(a)
                if pi not in S: S.add(pi); changed=True
    return frozenset(S)

subs=set()
for g in Q8: subs.add(generated([g]))
for a in Q8:
    for b in Q8: subs.add(generated([a,b]))
subs=sorted(subs, key=lambda s:(len(s), sorted(map(str,s))))
check("Q1.six_subgroups", len(subs)==6)
Z = frozenset({ONE,mONE})
check("Q1.center_is_Z", Z in subs)
C4s=[s for s in subs if len(s)==4]
check("Q1.three_C4", len(C4s)==3)
# Dedekind: every subgroup normal
def is_normal(H):
    return all(frozenset(qmul(qmul(g,h),qinv(g)) for h in H)==H for g in Q8)
check("Q1.all_normal_dedekind", all(is_normal(H) for H in subs))

# ---------------------------------------------------------------------------
# 2. Aut(Q8): enumerate unit-fixing multiplicative bijections. |Aut|=24.
#    characteristic subgroups = Aut-invariant subgroups = {1, Z, Q8}.
# ---------------------------------------------------------------------------
imags=[I,mI,J,mJ,K,mK]
auts=[]
for img_i in imags:
    for img_j in imags:
        # a hom is fixed by images of i and j (generators); build & test
        table={ONE:ONE, mONE:mONE, I:img_i, mI:qinv(img_i), J:img_j, mJ:qinv(img_j)}
        img_k=qmul(img_i,img_j)
        table[K]=img_k; table[mK]=qinv(img_k)
        vals=set(table.values())
        if len(vals)!=8: continue
        if all(table[qmul(a,b)]==qmul(table[a],table[b]) for a in Q8 for b in Q8):
            auts.append(table)
check("Q2.aut_order_24", len(auts)==24)
def apply_aut(phi,S): return frozenset(phi[x] for x in S)
char_subs=[H for H in subs if all(apply_aut(phi,H)==H for phi in auts)]
check("Q2.characteristic_chain", sorted(char_subs,key=len)==[frozenset({ONE}),Z,frozenset(Q8)])
# induced action on the C4 triple is transitive (S3)
triple=[frozenset(c) for c in C4s]
orbit={triple[0]}
for phi in auts: orbit.add(apply_aut(phi,triple[0]))
check("Q2.C4_triple_transitive", orbit==set(triple))

# ---------------------------------------------------------------------------
# 3. Cosets of Z = the four roles A,B,C,D; they PARTITION Q8 (the alphabet ABCD)
# ---------------------------------------------------------------------------
def left_cosets(H):
    seen=set(); cs=[]
    for g in Q8:
        c=frozenset(qmul(g,h) for h in H)
        if c not in seen: seen.add(c); cs.append(c)
    return cs
cosetsZ=left_cosets(Z)
check("Q3.four_cosets", len(cosetsZ)==4)
# partition test: pairwise disjoint + cover
def is_partition(blocks, universe):
    U=set(universe)
    seen=set()
    for b in blocks:
        if seen & set(b): return False        # overlap
        seen|=set(b)
    return seen==U
check("Q3.cosetsZ_partition_Q8", is_partition(cosetsZ, Q8))
# each coset is a sign-pair {x,-x}
signpair_ok=all(frozenset({c,qmul(mONE,c)})<=cs for cs in cosetsZ for c in [next(iter(cs))])
check("Q3.cosets_are_signpairs", all(len(cs)==2 and qmul(mONE,next(iter(cs))) in cs for cs in cosetsZ))

# ---------------------------------------------------------------------------
# 4. THE DERIVED RULE, mechanized.
#    A candidate extension alphabet X is a FAMILY of "letters", each letter a
#    subSET of the role material (elements of Q8 = the addressable positions).
#    ADMISSIBLE (partition rule) iff the letters are pairwise-disjoint nonempty
#    blocks (a partition of the set they cover).  We do NOT require they cover
#    all of Q8 (an extension adds a sub-alphabet), only that they be a partition
#    of their union -- i.e. NO two letters share an address (M1 identity-of-
#    indiscernibles :325 + no-subaddress :1574-1579).
# ---------------------------------------------------------------------------
def admissible_partition_alphabet(letters):
    letters=[frozenset(L) for L in letters]
    if any(len(L)==0 for L in letters): return False
    # letters must be role material (subsets of Q8 elements = addressable quanta)
    if any(not L<=set(Q8) for L in letters): return False
    return is_partition(letters, set().union(*letters))

# --- 4a. The two OWNED extensions are admissible -------------------------
# D2  = the direct/return dyad realized as 2 added vertices (2 blocks size 1).
#       Under the coset/center reading its two letters are {+1},{-1} (Z split)
#       OR the two-port role pair -- either way, 2 disjoint singletons.
D2_letters = [frozenset({ONE}), frozenset({mONE})]
check("R4a.D2_admissible", admissible_partition_alphabet(D2_letters))
check("R4a.D2_size2", len(D2_letters)==2)
# ABCD = the four cosets of Z (the coset reading, S-5), a partition of Q8.
ABCD_letters = cosetsZ
check("R4a.ABCD_admissible", admissible_partition_alphabet(ABCD_letters))
check("R4a.ABCD_size4", len(ABCD_letters)==4)

# --- 4b. The THREE named counter-objects are EXCLUDED by the rule --------
# (i) Sub(Q8): the 6 subgroups AS LETTERS. They pairwise share the identity ONE.
subgroups_as_letters = [frozenset(H) for H in subs]
# every pair of the >=2-element subgroups overlaps at ONE -> NOT a partition.
overlap_at_one = any((set(a)&set(b))>= {ONE}
                     for i,a in enumerate(subgroups_as_letters)
                     for b in subgroups_as_letters[i+1:])
check("R4b.Sub_overlaps_at_identity", overlap_at_one)
check("R4b.Sub_EXCLUDED", not admissible_partition_alphabet(subgroups_as_letters))
check("R4b.Sub_size6", len(subgroups_as_letters)==6)   # the escaped size-6 object

# (ii) Out(Q8) = S3: its elements are AUTOMORPHISMS, not subsets of Q8.
#     They are not role material (not addressable record quanta / vertices):
#     they fail the "letters are subsets of Q8" typing outright.
out_as_letters = [frozenset([("aut", id(phi))]) for phi in auts[:6]]  # symbolic
# these are not subsets of Q8 -> rule rejects on the typing clause
check("R4b.Out_not_role_material", not admissible_partition_alphabet(out_as_letters))
# |Out| = |Aut|/|Inn|; Inn = Q8/Z has order 4 -> Out order 6
check("R4b.Out_size6", len(auts)//4==6)

# (iii) characteristic chain {1,Z,Q8}: NESTED -> {1}subsetZsubsetQ8 overlap.
chain_as_letters=[frozenset({ONE}), Z, frozenset(Q8)]
nested = (set(chain_as_letters[0])<set(chain_as_letters[1])<set(chain_as_letters[2]))
check("R4b.chain_nested", nested)
check("R4b.chain_EXCLUDED", not admissible_partition_alphabet(chain_as_letters))
check("R4b.chain_size3", len(chain_as_letters)==3)


# ---------------------------------------------------------------------------
# 4c. NEGATIVE CONTROLS on the surviving partition rule (these MUST hold).
#     NC-1: WITHOUT the partition rule (allow overlap), Sub(Q8) and the chain
#           READMIT -> the rule is exactly what excludes them. Load-bearing.
# ---------------------------------------------------------------------------
def is_aut_invariant_family(blocks):
    bset=set(frozenset(b) for b in blocks)
    return all(set(apply_aut(phi,b) for b in bset)==bset for phi in auts)
def admissible_NO_RULE(letters):
    letters=[frozenset(L) for L in letters]
    return len(set(letters))==len(letters) and all(L for L in letters) and all(L<=set(Q8) for L in letters)
check("NC1.sub6_readmits_without_rule", admissible_NO_RULE(subgroups_as_letters))
check("NC1.chain_readmits_without_rule", admissible_NO_RULE(chain_as_letters))
check("NC1.rule_is_the_difference",
      admissible_NO_RULE(subgroups_as_letters) and not admissible_partition_alphabet(subgroups_as_letters))

# ---------------------------------------------------------------------------
# 5. THE KILL (R5): full enumeration of ALL Aut-invariant partitions of the role
#    material. The partition rule + "canonical" (Aut-invariant) clause do NOT
#    pin the size to {2,4}: the Aut-ORBIT partition X3 is a size-3 survivor.
#    We ENUMERATE (not cherry-pick) and EXHIBIT it. Nothing here reads {2,4}.
# ---------------------------------------------------------------------------
def all_set_partitions(items):
    items=list(items)
    if not items:
        yield []; return
    first=items[0]
    for rest in all_set_partitions(items[1:]):
        # add first to each existing block, or as its own block
        for i in range(len(rest)):
            yield rest[:i]+[[first]+rest[i]]+rest[i+1:]
        yield [[first]]+rest
# enumerate ALL partitions of Q8, keep the Aut-invariant ones (canonical):
canonical_partitions=[]
for part in all_set_partitions(Q8):
    blocks=[frozenset(b) for b in part]
    if is_aut_invariant_family(blocks):
        canonical_partitions.append(blocks)
canonical_block_counts=sorted({len(p) for p in canonical_partitions})
# proper nontrivial canonical partitions: >1 block, not the all-singletons(8),
# not the whole-group(1):
proper=[p for p in canonical_partitions if 1 < len(p) < 8]
proper_sizes=sorted({len(p) for p in proper})
check("R5.enumeration_ran", len(canonical_partitions) >= 1)
# THE KILLING FACT: a canonical size-3 partition EXISTS (= the orbit partition).
X3=[frozenset({ONE}),frozenset({mONE}),frozenset({I,mI,J,mJ,K,mK})]
check("R5.X3_is_partition", admissible_partition_alphabet(X3))
check("R5.X3_is_aut_invariant", is_aut_invariant_family(X3))
check("R5.X3_size3_z3_is_12", len(X3)==3 and 9+len(X3)==12)
check("R5.X3_in_enumeration", any(set(map(frozenset,p))==set(X3) for p in canonical_partitions))
# hence "size in {2,4}" is FALSE under partition+canonical alone:
check("R5.size_clause_NOT_forced", 3 in proper_sizes)   # <-- the kill, computed
# the memo's old NC2 cherry-picked a NON-invariant size-3 set and over-generalized:
part3_cherry=[frozenset({ONE,mONE}),frozenset({I,mI}),frozenset({J,mJ,K,mK})]
check("R5.cherry_pick_was_noninvariant", not is_aut_invariant_family(part3_cherry))
check("R5.but_a_canonical_size3_exists", is_aut_invariant_family(X3))

# ---------------------------------------------------------------------------
# 6. THE SHARPENED RESIDUE (R6): the ONLY computed property separating the two
#    KEPT alphabets (Z-split size2, Q8/Z size4) from the KILLING X3 (size3) is
#    UNIFORM BLOCK SIZE. This names the minimal missing lemma. (Not owned as an
#    alphabet rule -> the residue; see memo §RESIDUE.)
# ---------------------------------------------------------------------------
def uniform_blocks(part): return len({len(b) for b in part})==1
Z_split=[frozenset({ONE}),frozenset({mONE})]
# CRITICAL COMPUTED FINDING (deeper than the memo's first residue guess):
# the two OWNED alphabets partition DIFFERENT universes --
#   * ABCD = Q8/Z : a canonical partition OF Q8 (size 4, uniform blocks {2,2,2,2})
#   * D2/Z-split  : a partition of the CENTER Z (or the two-port dyad), NOT of Q8.
# As a partition OF Q8, the Z-split {{+1},{-1}} is NOT even Aut-invariant/canonical
# (its complement is one 6-block); the canonical size-2 partitions of Q8 all have
# blocks {1,7} or {2,6} -- NON-uniform. So among canonical partitions OF Q8, the
# UNIQUE uniform-block one is size 4 alone -- NOT {2,4}.
check("R6.ABCD_uniform_partition_of_Q8", uniform_blocks(cosetsZ) and is_aut_invariant_family(cosetsZ))
# Z-split IS an Aut-invariant family, but it does NOT cover Q8 -> it is a partition
# of the CENTER Z, not of Q8. That is the real asymmetry: the two owned alphabets
# partition DIFFERENT universes.
check("R6.Zsplit_is_aut_invariant_family", is_aut_invariant_family(Z_split))
check("R6.Zsplit_does_NOT_cover_Q8", set().union(*Z_split) != set(Q8))
check("R6.Zsplit_covers_center_Z", set().union(*Z_split) == set(Z))
check("R6.X3_NOT_uniform", not uniform_blocks(X3))         # 1,1,6 -> not uniform
proper_uniform_sizes=sorted({len(p) for p in proper if uniform_blocks(p)})
# the uniform clause over partitions-of-Q8 gives ONLY {4}, not {2,4}: it kills X3
# (good) but ALSO fails to recover the size-2 dyad -- so it is not even the right
# clause. The dyad lives on a different universe (the center / two-port dyad).
check("R6.uniform_clause_gives_only_4_not_2and4", proper_uniform_sizes==[4])
# ==> the minimal missing lemma is SHARPER than "uniform blocks": it must license
# TWO DIFFERENT universes (Z for the dyad, Q8 for ABCD) AND a uniform/coset shape
# on each. No single owned partition clause does this -> the true residue.

# ---------------------------------------------------------------------------
# 7. POSITIVE CONTROL (what WOULD close, IF the uniform-block lemma were owned).
#    Only here does 13 appear -- and it is explicitly conditional on R6.
# ---------------------------------------------------------------------------
base=9
# the uniform-block clause alone gives size {4} (kills X3 but loses the dyad) -->
# it is necessary-but-not-sufficient; the dyad needs a SECOND owned universe.
check("PC.uniform_kills_X3", 3 not in proper_uniform_sizes)
check("PC.uniform_alone_loses_dyad", 2 not in proper_uniform_sizes)
# UNCONDITIONALLY (no owned size clause): the upper bound is NOT sealed; z3=12 admissible.
check("PC.upper_bound_NOT_sealed_unconditionally", 3 in proper_sizes)

# ---------------------------------------------------------------------------
# 8. MUTATION SELF-TEST: dropping the partition rule readmits Sub(Q8); this must
#    flip. Confirms the SURVIVING rule (R4b) is load-bearing, not decorative.
# ---------------------------------------------------------------------------
check("MUT.partition_rule_flips_the_verdict",
      admissible_NO_RULE(subgroups_as_letters) != admissible_partition_alphabet(subgroups_as_letters))

# ---------------------------------------------------------------------------
# REPORT + VERDICT
# ---------------------------------------------------------------------------
npass=sum(1 for _,v in results if v)
nfail=len(results)-npass
print("="*70)
for name,v in results:
    print(f"  [{'PASS' if v else 'FAIL'}] {name}")
print("="*70)
print(f"  {npass}/{len(results)} checks pass; {nfail} fail.")
print(f"  SURVIVES: partition rule excludes Sub(Q8), Out(Q8), chain (R4b).")
print(f"  KILLS CLOSURE: canonical size-3 orbit partition X3 survives")
print(f"                 -> z3=12 admissible -> upper bound NOT sealed (R5).")
print(f"  RESIDUE: only 'uniform block size' separates kept alphabets from X3")
print(f"           (R6) -> minimal missing lemma; NOT owned as an alphabet rule.")
print(f"  canonical proper-partition block-counts (computed) = {proper_sizes}")
print("="*70)
print("  VERDICT: KILLED-AS-CLOSURE (rc=2). GAP-E completeness clause OPEN.")
print("="*70)
import sys
# rc: 1 if any structural check unexpectedly failed (script bug);
#     2 = the intended KILLED verdict (all checks pass AND X3 confirmed killing);
#     0 reserved for a genuine future closure (would require size_clause forced).
if nfail>0:
    sys.exit(1)
# closure is killed exactly when a canonical size-3 partition exists:
sys.exit(2 if (3 in proper_sizes) else 0)
