#!/usr/bin/env python3
"""f3_antidiagonal_check.py v2 — compute layer for the F3 antidiagonal EMBEDDING candidate (post-kill).

v2 (post skeptic #17): U1/U2/U4/U5 are ILLUSTRATIONS ONLY (they pass for non-ι encodings too —
the row-547 13th-pass tautology precedent); U3 is the sole SELECTIVE check (typing kills the
diagonal); U6 is the carrier guard (the partition carrier and 33-count are UNCHANGED by the
embedding — the v1 "literal nesting" reading is dead, EoR-2). The candidate is the EMBEDDING
ι(d) = (d, σd), image {C,D}, presentation-grade; see F3_ANTIDIAGONAL_CANDIDATE_MEMO.md v2.

CANDIDATE v2 (NOT owned, NOT minted): the EMBEDDING ι(d) = (d, σd) of the direct/return dyad
into its own terminal square — image the exchange pair {C, D}, orientation name-fixed
(direct ↦ C₊ forward, return ↦ D₋ return). PRESENTATION-grade only. The v1 subset reading
("dyad IS {C,D} ⊆ ABCD", "zones nest literally") is KILLED (EoR-1/EoR-2) and is NOT asserted
by any check below; the v1 duplication reductio is DEAD (cross-shell ABCD + zone-index
discriminator) and is NOT asserted either.

Checks (integers/frozensets only, can-fail):
  U1. ILLUSTRATION ONLY: the presentation-layer picture V9 ⊂ V9∪{C,D} ⊂ V9∪{A,B,C,D} has the
      cardinal ladder 9, 11, 13. NOT selective (any 2-of-4 pair passes); NOT a carrier fact
      (see U6 collapse exhibit).
  U2. ILLUSTRATION ONLY: the independence encoding carries two disjoint 2-sets. The forcing
      reading of this is DEAD (see memo §2); retained as bookkeeping, claims nothing.
  U3. THE SOLE SELECTIVE CHECK: the owned forward/return typing (exchange readouts (3,4)/(4,3),
      B01:760) passes the antidiagonal image {C,D} and FAILS the diagonal image {A,B}.
  U4. ILLUSTRATION ONLY: the presentation-layer inclusion order matches the owned outside-in
      direction; reversed chain fails.
  U5. Aut-hygiene: the image is an unordered pair, no V9 vertex selected — row 549 untouched.
  U6. CARRIER GUARD (load-bearing): built from the ACTUAL ι-sets — tagged zone copies keep
      |V| = 33 (the owned partition carrier), while the UNTAGGED union collapses to 13 — the
      exhibited EoR-2 control; plus no-basepoint (σd ≠ d) and port-swap invariance of the image.

rc=0: all checks pass (candidate ARMED at compute level; ownership stays with the owner).
rc=1: a check failed (candidate broken).
"""
import sys

def main() -> int:
    failures = []

    # Owned raw material (B01:749-758, :766-776, :1523-1553; B00:289-299).
    ROLES = {"A": (3, 3), "B": (4, 4), "C": (3, 4), "D": (4, 3)}
    COALESCENT = {r for r, (x, y) in ROLES.items() if x == y}          # {A, B}
    EXCHANGE = {r for r, (x, y) in ROLES.items() if x != y}            # {C, D}
    OMEGA8 = {(r, s) for r in ROLES for s in ("+", "-")}
    V9 = frozenset(OMEGA8 | {"omega0"})                                 # |V9| = 9

    # Candidate ι: dyad letters = exchange roles (direct ↦ C, return ↦ D).
    DYAD_IMG = frozenset({("role", "C"), ("role", "D")})
    ROLE_SQUARE = frozenset({("role", r) for r in ROLES})

    V11_iota = V9 | DYAD_IMG
    V13_iota = V9 | ROLE_SQUARE

    # U1 — literal nesting + cardinal ladder.
    ok = (V9 < V11_iota < V13_iota) and (len(V9), len(V11_iota), len(V13_iota)) == (9, 11, 13)
    print(f"U1 [illustration] presentation-ladder: {'PASS' if ok else 'FAIL'} "
          f"(cards {len(V9)},{len(V11_iota)},{len(V13_iota)})")
    if not ok: failures.append("U1")

    # U2 — independence reading duplicates the forward/return capacity.
    V11_indep = V9 | {("dyad", "direct"), ("dyad", "return")}
    fr_copies_indep = [{("dyad", "direct"), ("dyad", "return")},
                       {("role", "C"), ("role", "D")}]  # two disjoint realizations
    disjoint = fr_copies_indep[0].isdisjoint(fr_copies_indep[1])
    import math
    register_bits = math.ceil(math.log2(len(fr_copies_indep)))
    ok = disjoint and register_bits >= 1 and len(V11_indep) == 11
    print(f"U2 [illustration, forcing DEAD] bookkeeping: {'PASS' if ok else 'FAIL'} "
          f"(copies=2 disjoint={disjoint}, register>={register_bits} bit)")
    if not ok: failures.append("U2")

    # U3 — typing match: antidiagonal passes, diagonal rival fails.
    def typing_match(pair: set) -> bool:
        # the dyad is owned-typed as forward/return = separated/exchange readouts (B01:760, :794)
        return all(ROLES[r][0] != ROLES[r][1] for r in pair)
    anti_ok = typing_match({"C", "D"})
    diag_fails = not typing_match({"A", "B"})
    ok = anti_ok and diag_fails and EXCHANGE == {"C", "D"} and COALESCENT == {"A", "B"}
    print(f"U3 typing-match (anti passes, diag fails): {'PASS' if ok else 'FAIL'}")
    if not ok: failures.append("U3")

    # U4 — nesting direction (outside-in) is an order, not a convention.
    ok = not (V13_iota < V11_iota) and not (V11_iota < V9)
    print(f"U4 direction-control: {'PASS' if ok else 'FAIL'}")
    if not ok: failures.append("U4")

    # U5 — no within-zone vertex order named: image is an unordered PAIR; the C<->D swap is the
    # direct<->return relabel (blocked only by the owned names), and no vertex of V9 is selected.
    swap_img = frozenset({("role", "D"), ("role", "C")})
    ok = (swap_img == DYAD_IMG) and DYAD_IMG.isdisjoint(V9)
    print(f"U5 aut-hygiene (unordered pair, no V9 selection): {'PASS' if ok else 'FAIL'}")
    if not ok: failures.append("U5")

    # U6 — CARRIER GUARD (v2, load-bearing): the embedding is presentation-grade; the owned
    # partition carrier (tagged zone copies) is unchanged: |V9|+|V11|+|V13| = 33 with pairwise
    # disjoint tagged blocks, and the antidiagonal image is computed from the dyad itself
    # (no base point: sigma(d) != d for both letters; port-swap invariance of the image).
    sigma = {0: 1, 1: 0}
    iota = {d: (d, sigma[d]) for d in (0, 1)}
    img = frozenset(iota.values())
    img_swapped = frozenset((b, a) for (a, b) in img)
    # the ACTUAL iota-sets (skeptic #17 v2 repair): tagged copies preserve the owned 33-carrier;
    # the untagged union is the exhibited EoR-2 collapse (13, NOT 33) — why v1 was killed.
    tagged = ([("z9", v) for v in V9] + [("z11", v) for v in V11_iota]
              + [("z13", v) for v in V13_iota])
    untagged_union = V9 | V11_iota | V13_iota
    ok = (img == {(0, 1), (1, 0)} == img_swapped
          and all(sigma[d] != d for d in (0, 1))
          and len(tagged) == len(set(tagged)) == 33
          and len(untagged_union) == 13)
    print(f"U6 carrier-guard (tagged 33 / untagged collapse 13, no-basepoint, swap-inv): "
          f"{'PASS' if ok else 'FAIL'}")
    if not ok: failures.append("U6")

    print(f"RESULT: {'PASS 6/6 rc=0' if not failures else 'FAIL ' + ','.join(failures) + ' rc=1'}")
    return 0 if not failures else 1

if __name__ == "__main__":
    sys.exit(main())
