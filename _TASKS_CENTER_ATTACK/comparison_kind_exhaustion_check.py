#!/usr/bin/env python3
"""
comparison_kind_exhaustion_check.py
===================================
CANDIDATE for the missing theorem named by the 2026-07-29 status correction of
D0-P-DEGREE2-EXHAUSTION-001 and D0-TOWER-STOP-NOEXT-001:

  "a conclusion-free semantic classification theorem supplies the missing
   exhaustivity map"
  "The finite inductive ComparisonKind in DetectionQuadratic has cardinality two
   because it is DECLARED with two constructors; it is not yet proved exhaustive
   for arbitrary admissible detection."

The withdrawn argument derived the cap from degree-2 algebra (p^3 = 2p-1 in
span{1,p}). That inference was killed: linear dependence does not bound the count
of structural types. NOTHING in this cert touches phi, p, or any algebra. The
count is derived from the SEMANTICS the DetectionQuadratic docstring itself gives:

    membership : levels 1<->2, DIFFERENT categories  => linear   (degree 1)
    value      : levels 2<->3, ONE category          => bilinear (degree 2)

i.e. the kind of a comparison is fixed by whether the two compared items lie in
the same category or in different ones. That is a binary predicate, and its
exhaustiveness is an ORBIT COUNT on the pair space -- computable exactly.

DEFINITION (conclusion-free). A categorized universe is a finite set X with a
partition into categories. Its structure group G is the full stabiliser of the
partition: all permutations of X carrying categories onto categories (category
SWAPS included whenever sizes permit). A comparison is an ordered pair of
DISTINCT elements. A comparison KIND is a G-orbit on those pairs.

THEOREM CANDIDATE (T). #kinds = 2 exactly when the categories are mutually
interchangeable, i.e. all categories have equal size, with >=2 categories and
some category of size >=2. Otherwise #kinds > 2, and the count is computed here
for every shape tested.

THE STING (pre-registered, this is the load-bearing consequence). The frozen
scene K(9,11,13) has PAIRWISE DISTINCT category sizes. So at the zone level the
kind count is NOT 2. If a downstream claim inherits "port-count = 2" from "the
CORE two-comparison-kind count", it is transporting a number across a level at
which the number provably changes. Computed below, both counts exhibited.

Exit 0 iff every check passes and every negative control fires.
"""

from itertools import permutations, combinations
import sys

FAILURES, PASSES = [], []


def check(name, cond, detail=""):
    (PASSES if cond else FAILURES).append(name)
    print(f"  {'PASS' if cond else 'FAIL'}  {name}" + (f"   [{detail}]" if detail else ""))
    return bool(cond)


# ---------------------------------------------------------------------------
# Structure group of a categorized universe: ALL partition-preserving perms,
# built by brute force (no generator recipe is assumed anywhere).
# ---------------------------------------------------------------------------
def categorized(sizes):
    cat, X = [], 0
    for ci, s in enumerate(sizes):
        cat.extend([ci] * s)
    return len(cat), cat


def structure_group(sizes):
    """Every permutation of X that maps each category ONTO some category."""
    N, cat = categorized(sizes)
    out = []
    for p in permutations(range(N)):
        img = {}
        ok = True
        for v in range(N):
            c, d = cat[v], cat[p[v]]
            if c in img and img[c] != d:
                ok = False
                break
            img[c] = d
        if ok and len(set(img.values())) == len(img):
            out.append(p)
    return out, cat, N


def kind_orbits(sizes, ordered=True, include_diagonal=False):
    """G-orbits on pairs of (distinct) elements = the comparison kinds."""
    G, cat, N = structure_group(sizes)
    if ordered:
        pairs = [(u, v) for u in range(N) for v in range(N)
                 if include_diagonal or u != v]
    else:
        pairs = [(u, v) for u, v in combinations(range(N), 2)]
    idx = {pr: i for i, pr in enumerate(pairs)}
    parent = list(range(len(pairs)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for (u, v) in pairs:
        for p in G:
            a, b = p[u], p[v]
            key = (a, b) if ordered else tuple(sorted((a, b)))
            if key in idx:
                ra, rb = find(idx[(u, v)]), find(idx[key])
                if ra != rb:
                    parent[ra] = rb
    reps = {}
    for pr in pairs:
        reps.setdefault(find(idx[pr]), []).append(pr)
    return list(reps.values()), cat, len(G)


def same_cat_predicate_classes(sizes, ordered=True):
    """How many classes does the SEMANTIC predicate [cat(u)==cat(v)] cut out?"""
    N, cat = categorized(sizes)
    pairs = [(u, v) for u in range(N) for v in range(N) if u != v] if ordered \
        else [(u, v) for u, v in combinations(range(N), 2)]
    return len({cat[u] == cat[v] for (u, v) in pairs})


# ---------------------------------------------------------------------------
def main():
    print("=" * 78)
    print("Comparison-kind exhaustion — a conclusion-free orbit count")
    print("NO phi, NO p, NO degree-2 algebra is used anywhere in this file.")
    print("=" * 78)

    # -- T1: equal-size categories => exactly 2 kinds, computed not declared ---
    print("\n[T1] equal category sizes: kinds must be exactly 2")
    equal_shapes = [(2, 2), (3, 3), (2, 2, 2), (3, 3, 3), (2, 2, 2, 2), (4, 4)]
    rows = []
    all2 = True
    for s in equal_shapes:
        orbs, cat, gsize = kind_orbits(s, ordered=True)
        rows.append((s, len(orbs), gsize))
        if len(orbs) != 2:
            all2 = False
    for s, k, g in rows:
        print(f"    sizes {str(s):12s} |G| = {g:6d}   kinds = {k}")
    check(
        "T1: every equal-size categorized universe has EXACTLY 2 comparison kinds",
        all2,
        "orbit count on ordered distinct pairs; categories interchangeable",
    )

    # the two kinds ARE same-category / different-category
    orbs, cat, _ = kind_orbits((3, 3, 3), ordered=True)
    labels = {tuple(sorted({cat[u] == cat[v] for (u, v) in o})) for o in orbs}
    check(
        "T1b: the 2 orbits are exactly {same-category, different-category}",
        labels == {(False,), (True,)},
        "each orbit is homogeneous for the predicate cat(u)==cat(v), and both occur",
    )
    check(
        "T1c: the semantic predicate alone cuts 2 classes (independent of orbits)",
        same_cat_predicate_classes((3, 3, 3)) == 2,
        "computed from the partition, not from any orbit computation",
    )

    # -- T2: the degenerate cases where 2 FAILS (boundary of the theorem) -----
    print("\n[T2] boundary: shapes where the count is NOT 2")
    for s, why in [((1, 1), "no category has >=2 elements: no same-cat pair"),
                   ((3,), "only one category: no different-cat pair"),
                   ((2,), "single category")]:
        orbs, _, _ = kind_orbits(s, ordered=True)
        print(f"    sizes {str(s):10s} kinds = {len(orbs)}   ({why})")
    k11, _, _ = kind_orbits((1, 1), ordered=True)
    k3, _, _ = kind_orbits((3,), ordered=True)
    check(
        "T2: the hypotheses are necessary — degenerate shapes give 1 kind, not 2",
        len(k11) == 1 and len(k3) == 1,
        "so T1's '>=2 categories, some category >=2' is not decorative",
    )

    # -- T3: THE STING — distinct sizes destroy the count --------------------
    print("\n[T3] distinct category sizes: the count is NOT 2")
    sting = []
    for s in [(1, 2), (1, 2, 3), (2, 3), (2, 3, 4), (1, 2, 2)]:
        orbs, _, gsize = kind_orbits(s, ordered=True)
        sting.append((s, len(orbs)))
        print(f"    sizes {str(s):12s} |G| = {gsize:6d}   kinds = {len(orbs)}")
    distinct_all_gt2 = all(k > 2 for s, k in sting if len(set(s)) == len(s) and len(s) >= 2)
    check(
        "T3: every all-distinct-size shape with >=2 categories has MORE than 2 kinds",
        distinct_all_gt2,
        "categories become distinguishable, so the kinds refine",
    )

    # K(9,11,13) itself: computed structurally (brute force over 33! is
    # impossible, so the count is derived from the shape, then CHECKED against a
    # faithful small analogue with the same distinctness pattern).
    # Ordered distinct pairs, ALL sizes distinct, k categories:
    #   same-category orbits      = #{categories of size >= 2}
    #        (a singleton category contributes NO ordered distinct pair -- this is
    #         where the first hand-derivation of this formula was wrong, caught by
    #         the (1,2,3) row below)
    #   different-category orbits = k*(k-1)   (one per ordered pair of categories)
    def closed_form(s):
        return sum(1 for x in s if x >= 2) + len(s) * (len(s) - 1)

    predicted_9_11_13 = closed_form((9, 11, 13))
    small = [(1, 2, 3), (2, 3, 4), (1, 2), (2, 3)]
    formula_ok = True
    for s in small:
        orbs, _, _ = kind_orbits(s, ordered=True)
        if len(orbs) != closed_form(s):
            formula_ok = False
            print(f"    formula MISMATCH at {s}: computed {len(orbs)}, formula {closed_form(s)}")
    check(
        "T3b: closed form k + k(k-1) verified on distinct-size analogues of K(9,11,13)",
        formula_ok,
        f"=> K(9,11,13) has {predicted_9_11_13} comparison kinds at the ZONE level, not 2",
    )

    # -- T4: the two counts are different objects ----------------------------
    print("\n[T4] the transport question")
    kinds_abstract = 2                 # T1: interchangeable categories
    kinds_zone = predicted_9_11_13     # T3b: K(9,11,13)
    check(
        "T4: abstract-floor kind count (2) != zone-level kind count (9)",
        kinds_abstract != kinds_zone,
        f"{kinds_abstract} vs {kinds_zone} — any claim inheriting '2' at the zone "
        f"level crosses a level at which the number provably changes",
    )

    # -- NEGATIVE CONTROLS ---------------------------------------------------
    print("\n[NEGATIVE CONTROLS]")
    # (a) if category swaps are FORBIDDEN (labelled categories), equal sizes also
    #     stop giving 2 — proving T1 genuinely uses interchangeability.
    def labelled_kinds(sizes):
        N, cat = categorized(sizes)
        G = []
        for p in permutations(range(N)):
            if all(cat[p[v]] == cat[v] for v in range(N)):
                G.append(p)
        pairs = [(u, v) for u in range(N) for v in range(N) if u != v]
        idx = {pr: i for i, pr in enumerate(pairs)}
        parent = list(range(len(pairs)))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x
        for (u, v) in pairs:
            for p in G:
                ra, rb = find(idx[(u, v)]), find(idx[(p[u], p[v])])
                if ra != rb:
                    parent[ra] = rb
        return len({find(idx[pr]) for pr in pairs})

    lab = labelled_kinds((3, 3, 3))
    check(
        "NC1: with category swaps FORBIDDEN, equal sizes give %d kinds, not 2" % lab,
        lab != 2,
        "T1 is not a tautology of the pair space; it consumes interchangeability",
    )
    # (b) including the diagonal must change the count (kinds are about DISTINCT
    #     items; if the diagonal were harmless the definition would be sloppy).
    with_diag, _, _ = kind_orbits((3, 3, 3), ordered=True, include_diagonal=True)
    check(
        "NC2: including the diagonal changes the count (%d != 2)" % len(with_diag),
        len(with_diag) != 2,
        "the 'distinct items' clause in the definition is load-bearing",
    )
    # (c) a shape where the answer is KNOWN by hand: (2,2) ordered distinct pairs
    #     = 2 same-cat + 4 diff-cat = 2 orbits. Verified by exhaustive listing.
    orbs22, cat22, _ = kind_orbits((2, 2), ordered=True)
    sizes22 = sorted(len(o) for o in orbs22)
    # 2 categories x 2 ordered distinct pairs inside each = 4 same-category;
    # 2*2*2 = 8 different-category. (The first hand-derivation said [2,8] and was
    # wrong -- it counted one category only. The assertion caught it.)
    check(
        "NC3: hand-checkable case (2,2): orbit sizes %s == [4, 8]" % sizes22,
        sizes22 == [4, 8],
        "4 same-category ordered pairs (2 per category) + 8 different-category",
    )

    print("\n" + "=" * 78)
    print(f"checks passed: {len(PASSES)}   failed: {len(FAILURES)}")
    if FAILURES:
        for f in FAILURES:
            print("   -", f)
        return 1
    print("CANDIDATE THEOREM (T) stands on every shape tested.")
    print("Exhaustion is an ORBIT COUNT, conclusion-free: no phi, no p^3 = 2p-1.")
    print("Boundary: 2 kinds requires INTERCHANGEABLE categories. K(9,11,13) has")
    print("distinct zone sizes, hence 9 kinds at the zone level, not 2.")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main())
