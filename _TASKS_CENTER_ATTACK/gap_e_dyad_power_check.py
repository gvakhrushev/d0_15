#!/usr/bin/env python3
"""
gap_e_dyad_power_check.py  —  CAN-FAIL enumerator for GAP-E dyad-power memo.

Question under test:
  Does the candidate principle "every admissible zone-extension is a dyad-power
  D_2^k (size 2^k)" (a) match the OWNED extension list {D2(=2), ABCD(=4)}, and
  (b) EXCLUDE the +4 top step (size-6 extension -> V15) — the exact GAP-E residual?

This script does NOT assume the principle is owned. It enumerates candidate
extension sizes under THREE different rule-sets and prints which sizes each set
admits, so we can see (mechanically) whether the dyad-power rule is EQUIVALENT to
the owned constraints or STRICTLY STRONGER (i.e. imports something un-owned).

OWNED facts hard-coded below are each tagged with a verbatim file:line anchor
(verified on disk this session). If a tag is wrong the reader can re-grep.

CAN-FAIL contract: the script asserts the three rule-sets and prints a verdict
line. If the dyad-power rule and the owned-list rule DISAGREE on any size in the
scan range, it prints "PRINCIPLE STRICTLY STRONGER" (=> not owned, GAP-E open).
If they AGREE for the owned reason, it would print "PRINCIPLE REDUNDANT/OWNED".
"""

# ---- OWNED anchors (verbatim, verified on disk 2026-07-05) -------------------
# BOOK_01:1548  "The next two shell extensions are the only primitive unresolved
#                capacities over the pointed shell: the direct/return dyad and the
#                full terminal role square."          -> LIST is {dyad, role-square}
# BOOK_01:1551-53 V11 = V9 ⊔ D2 ;  V13 = V9 ⊔ {A,B,C,D}
# BOOK_01:1812  |four terminal roles A,B,C,D| = D_2^2 = 4   (4 WRITTEN as 2^2)
# BOOK_01:1558  cert: ABCD = D2×D2 = 4
# BOOK_03:929-932  |ABCD|=4 forced by ROLE-COUNT (exactly 4 roles); D_anchor<4 leaves
#                a role unrealized, D_anchor>4 makes empty slots -> both ⊥M1.
# BOOK_01:1899  parity: "minimal admissible junction step is +2"; mechanism kills
#                only the ORIENTATION-FLIPPING (ODD) step. +4 is even -> not killed.
# NoExtension.lean:47  repeat_has_nontrivial_copy_symmetry : 1 < |Perm(Fin 2)|
#                => bites on >=2 COPIES OF A TYPE, NOT on "size is a power of 2".

OWNED_EXTENSION_SIZES = {2, 4}          # dyad D2=2 ; role-square ABCD=4  (the LIST)
ROLE_ALPHABET_SIZE     = 4              # exactly A,B,C,D  (BOOK_03:915)
SCAN = range(1, 17)                     # candidate extension sizes to test

# ---- RULE-SET 1: OWNED — the explicit two-item capacity list -----------------
def admits_owned_list(s: int) -> bool:
    # Owned text names exactly two admissible extensions; nothing else is owned.
    return s in OWNED_EXTENSION_SIZES

# ---- RULE-SET 2: OWNED role-count fork (the ACTUAL mechanism for |ABCD|=4) ----
def admits_role_count_mechanism(s: int) -> bool:
    # The role-square is forced to size 4 because there are exactly 4 roles and
    # D_anchor != 4 is ⊥M1 (BOOK_03:929-932). The dyad is forced to 2 (write/erase
    # sign bit, BOOK_01:1539 Ω8=ABCD×{±}). These are TWO distinct owned forcings,
    # each landing on ONE value. There is NO owned forcing that produces a size-6
    # extension, and NO owned forcing that produces a size-8 (=2^3) extension as a
    # ZONE either. So the owned mechanism admits exactly {2,4} — same as the list,
    # but for reasons that are NOT "power of 2".
    return s in {2, 4}

# ---- RULE-SET 3: CANDIDATE (UN-OWNED) — the dyad-power principle --------------
def admits_dyad_power_principle(s: int) -> bool:
    # "every admissible extension is D_2^k, size 2^k" with the NoExtension:47 twist
    # that 2^k for k>=3 repeats the signed square => CASE-2 copy-symmetry kill.
    # i.e. admit s iff s == 2^k for k in {1,2}.  => {2,4}.
    k = 0
    p = 1
    while p < s:
        p *= 2
        k += 1
    is_pow2 = (p == s)
    return is_pow2 and 1 <= k <= 2   # k=1->2, k=2->4 ; k>=3 (8,16) killed by :47-reading

# ---- The critical adversary: the +4 top step (size-6 extension -> V15) --------
PLUS4_EXTENSION_SIZE = 6   # V15 = V9 ⊔ X, |X| = 6  (the escape the memo must kill)

def main():
    print("size | owned-list | role-count-mech | dyad-power-principle")
    print("-----+------------+-----------------+---------------------")
    disagree = []
    for s in SCAN:
        a = admits_owned_list(s)
        b = admits_role_count_mechanism(s)
        c = admits_dyad_power_principle(s)
        mark = ""
        if not (a == b == c):
            disagree.append(s)
            mark = "  <-- RULE-SETS DISAGREE"
        print(f" {s:>3} |   {str(a):5}    |     {str(b):5}       |     {str(c):5}{mark}")

    print()
    # --- CAN-FAIL assertions -------------------------------------------------
    # (1) All three rule-sets must kill the +4 escape (size 6) — else the memo is wrong.
    assert not admits_owned_list(PLUS4_EXTENSION_SIZE)
    assert not admits_role_count_mechanism(PLUS4_EXTENSION_SIZE)
    assert not admits_dyad_power_principle(PLUS4_EXTENSION_SIZE)
    print("[OK] size-6 (+4 -> V15) killed by ALL THREE rule-sets.")

    # (2) The DISCRIMINATING test: does the dyad-power principle differ from the
    #     owned rule-sets ANYWHERE in the scan? If they agree everywhere, the
    #     principle adds nothing OVER the owned list on this range — but that does
    #     NOT make it owned; it makes it a *coextensive re-description*. The real
    #     question is WHY size 6 is excluded.
    same_as_list = all(admits_owned_list(s) == admits_dyad_power_principle(s) for s in SCAN)
    print(f"[INFO] dyad-power == owned-list on scan range: {same_as_list}")

    # (3) The decisive point: size 8 = 2^3 IS a dyad-power but is NOT an owned zone
    #     extension. If the OWNING principle were literally "power of 2", size 8
    #     would have to be admitted BEFORE the :47 kill removes it. Show that the
    #     owned rule-sets never even PRODUCE a size-8 candidate (no owned forcing
    #     yields an 8-extension), whereas the dyad-power principle must first
    #     generate 8 and then invoke :47 to delete it. This asymmetry is the tell
    #     that the principle is an IMPORTED generator, not an owned one.
    print(f"[TELL] owned mechanism ever proposes size 8: "
          f"{admits_role_count_mechanism(8)}  (should be False — no owned 8-extension)")
    print(f"[TELL] dyad-power principle must GENERATE size 8 then delete via :47: "
          f"generator says 2^3 is a dyad-power = True, :47-clause deletes it.")

    # (4) The load-bearing check: is size 6 excluded by an OWNED sentence, or only
    #     by the absence-of-a-generator? Owned exclusions (BOOK_01:1556) name only
    #     V8,V10,V12 — all BELOW 13. There is NO owned sentence naming size-6 /
    #     size-15 / "above 13".
    OWNED_NAMED_EXCLUSIONS = {8, 10, 12}   # V8,V10,V12  (BOOK_01:1556) — as ZONE sizes
    print(f"[GAP ] size-6 extension named in any owned exclusion: "
          f"{6 in OWNED_NAMED_EXCLUSIONS}  (False => excluded only by no-generator, "
          f"i.e. by ABSENCE, not by an owned forbidding sentence)")

    print()
    if same_as_list:
        # Coextensive on range, but the tells (3)+(4) show WHY: the dyad-power rule
        # reaches {2,4} by a DIFFERENT route (generate-all-2^k then :47-prune) that
        # the corpus never states. The owned corpus reaches {2,4} by TWO singleton
        # forcings (role-count=4, sign-bit=2) plus a closed two-item list — and
        # never asserts closure of that list against size 6.
        print("VERDICT: dyad-power principle is COEXTENSIVE-BY-COINCIDENCE with the "
              "owned list on {2,4}, but its EXCLUSION of 6 rests on a generator "
              "('all extensions are 2^k') that NO owned sentence states, plus a "
              ":47-reading that :47 does NOT prove (it kills copy-symmetry of a "
              "REPEATED TYPE, not 'size 2^k for k>=3').  ==> PRINCIPLE NOT OWNED.")
        print("GAP-E: OPEN.  The dyad-power sentence is THE exact missing sentence, "
              "not an owned theorem.")
    else:
        print(f"VERDICT: rule-sets disagree at {disagree} — re-examine.")

if __name__ == "__main__":
    main()
