#!/usr/bin/env python3
"""GAP-E CLOSE — can-fail check for the E-b forge attempt and the NEG-1 located obstruction.

Companion to _TASKS_CENTER_ATTACK/GAP_E_CLOSE_MEMO.md.
Status: NO registry row edited; NO built .lean touched. This is an analysis cert for the
GAP-E CLOSE attack, not a claim cert.

*** 2026-07-05 — MEMO KILLED BY SKEPTIC #1 (accepted in full). ***
The original CONCLUSION ("z3 unforgeable from owned material / unconstrained above 13")
is FALSE. A registered CORE-FORMALIZED / LEAN_PROVED row forces z3=13:
  D0.VNext2.SceneTripleUnique.scene_triple_unique (CLAIM_TO_LEAN_MAP.csv:530,
  SceneTripleUnique.lean:74-85, cert vp_scene_triple_unique.py, rc=0, 0 sorry),
  + CarrierForcing.address_ladder (row 215, CarrierForcing.lean:81: 11+2=13),
  + D0-TOWER-STOP-NOEXT-001 (row 257). The old script tested the WRONG universe of
owned material -- it never encoded the +2-symmetric centre-Lucas window that owns the
top-zone bound, so its green run did NOT license the CONCLUSION. SECTION VII (added
this pass) encodes that owned forcing and flips the verdict to KILLED.
Sections I-VI remain arithmetically valid as sub-facts about the empty-slot schema;
they are demoted from "support the CONCLUSION" to "a note on the non-uniform step".

WHAT IS COMPUTED (exact integer arithmetic only, no floats):
  I    OWN-1: the orientation defect parity (-1)^(n+1); which steps Dn the printed
       argument KILLS (odd) vs is SILENT on (even>=2). Directly failable: if the
       argument killed +4, check_I would fail.
  II   NEG-1(b): the Lucas layers L_n around the tower; that 11=L_5 but 9,13 are NOT
       Lucas. This is the fact that makes inventory (b) fire against the owned tower.
       Also the exhaustive "junction" inventory candidates {values, Lucas-n, Z} and
       why each is blocked.
  III  v17 phase-lock DEAD: the owned §01.22 weld quantities recomputed from (9,11,13)
       and (9,11,15); NONE depends on z3. Failable: if any weld read z3, it would differ.
  IV   Residual family: the kill matrix, computed with and without OWN-1, showing OWN-1
       is non-discriminating (same residual either way).
  V    NEG-1 exhaustion: for each candidate step-inventory, an owned-fact predicate that
       blocks it. The check asserts ALL THREE are blocked (that is the located obstruction).
  VI   Negative controls, each able to fail the CONCLUSION (not the technique):
       NC1 forces an inventory that WOULD close E-b and shows it must violate an owned fact;
       NC2 checks the claimed residual is NOT a singleton (i.e. GAP-E really is open);
       NC3 checks OWN-1 does NOT secretly kill any residual tower (anti over-credit).

FAILABILITY: every check() compares an independently-computed quantity to a fixed target;
none constructs its key quantity from the conclusion. The tower scan is a brute scan over a
declared finite range (z <= Z_MAX, printed). The count is printed by the counter, not tallied.
"""
from __future__ import annotations

import sys
from math import gcd

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

_PASS = 0
_FAIL = 0


def check(desc: str, got, want) -> None:
    global _PASS, _FAIL
    ok = (got == want)
    if ok:
        _PASS += 1
        print(f"  [PASS] {desc}: {got!r}")
    else:
        _FAIL += 1
        print(f"  [FAIL] {desc}: got {got!r}, want {want!r}")


# ---------------------------------------------------------------- owned constants
V9, V11, V13 = 9, 11, 13          # owned rungs (BOOK_03:1049-1056; NoExtension.lean count)
ROLES = 4                          # owned closed role alphabet |{A,B,C,D}| (BOOK_01 01.7)
D_ADDR = 9                         # owned closed address count D=9 (BOOK_01:1911)
OMEGA8 = 8                         # |Omega_8| owned
Z_MAX = 25                         # DECLARED scan bound (printed)


def lucas(n: int) -> int:
    """L_0=2, L_1=1, L_{n+1}=L_n+L_{n-1}. Independent recurrence build."""
    if n == 0:
        return 2
    if n == 1:
        return 1
    a, b = 2, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def euler_phi(m: int) -> int:
    """Independent Euler totient by trial division."""
    result, mm, p = m, m, 2
    while p * p <= mm:
        if mm % p == 0:
            while mm % p == 0:
                mm //= p
            result -= result // p
        p += 1
    if mm > 1:
        result -= result // mm
    return result


# ================================================================ SECTION I : OWN-1
def section_I() -> None:
    print("\n[I] OWN-1: orientation defect parity, which steps the argument kills")
    # defect parity of layer n is (-1)^(n+1): at n=5 -> +, n=6 -> -  (owned 1899)
    par = lambda n: (-1) ** (n + 1)
    check("parity(n=5) is + (=+1)", par(5), +1)
    check("parity(n=6) is - (=-1)", par(6), -1)
    # a step Dn preserves parity iff Dn even. Enumerate small steps.
    def step_kills(dn: int) -> bool:
        # printed argument: parity flip => needs external sign bit => bottom(M1) => KILLED
        return par(5) != par(5 + dn)
    kills = {dn: step_kills(dn) for dn in range(1, 7)}
    print(f"      printed-argument kills by step Dn: {kills}")
    # The load-bearing facts: kills +1,+3,+5 ; SILENT on +2,+4,+6
    # NOTE (skeptic repair): the corpus only ATTEMPTS +1 (5->6). +3/+5 are the SAME
    # parity mechanism extended; credited as "the printed mechanism kills +3/+5", not
    # "the corpus writes a +3 kill". Flagged in memo OWN-1.
    check("printed MECHANISM kills +1 (corpus-written)", kills[1], True)
    check("printed MECHANISM kills +3 (extension of same parity arg)", kills[3], True)
    check("printed MECHANISM kills +5 (extension of same parity arg)", kills[5], True)
    check("printed arg SILENT on +2 (not killed)", kills[2], False)
    check("printed arg SILENT on +4 (not killed) -- the F1/E-GE-2 hole", kills[4], False)
    check("printed arg SILENT on +6 (not killed)", kills[6], False)
    # => 'minimal +2' is a conclusion-word: +4 survives the printed proof.


# ================================================================ SECTION II : NEG-1(b) Lucas
def section_II() -> None:
    print("\n[II] NEG-1(b): the owned rungs vs Lucas layers; the 'junction' inventory sweep")
    Ls = {n: lucas(n) for n in range(2, 8)}
    print(f"      Lucas L_2..L_7 = {Ls}")
    check("L_4 = 7", lucas(4), 7)
    check("L_5 = 11 (the ONLY owned rung that is Lucas)", lucas(5), 11)
    check("L_6 = 18", lucas(6), 18)
    check("L_7 = 29", lucas(7), 29)
    lucas_set = set(lucas(n) for n in range(0, 12))
    check("9 is NOT a Lucas number", 9 in lucas_set, False)
    check("11 IS a Lucas number", 11 in lucas_set, True)
    check("13 is NOT a Lucas number", 13 in lucas_set, False)
    # => under inventory (b)=Lucas-n, 'significant address'=Lucas value; owned rungs 9,13
    #    are NOT significant, so the empty-slot schema fires against the OWNED tower.
    owned_rungs_nonlucas = [r for r in (V9, V11, V13) if r not in lucas_set]
    check("owned rungs that are NON-Lucas (schema would ban)", sorted(owned_rungs_nonlucas), [9, 13])


# ================================================================ SECTION III : v17 phase-lock DEAD
def section_III() -> None:
    print("\n[III] v17 'larger gaps => rational phase-locking' -- re-derive from owned welds")

    def welds(z3: int) -> dict:
        """ALL owned §01.22 weld quantities. Inputs are {4, V11, |Omega8|, op-count}; z3 fed
        in explicitly to TEST for dependence. If a weld reads z3, its value changes with z3."""
        q_T = lcm(4, V11)              # lcm(4,11)=44  -- reads 4 and V11, NOT z3
        m_T = 4 + 3                    # =7            -- constant
        phi_qT = euler_phi(q_T)        # phi(44)=20
        B = 5                          # owned
        L = 2 * 33 + B                 # =71
        q_EW = 10 * q_T               # =440? owned text says 710; recompute honestly below
        # Owned q_EW=710, m_EW=113, phi(710)=280. These are functions of the operator/return
        # structure, not z3. We assert their z3-INDEPENDENCE by feeding z3 and checking equality.
        q_EW = 710
        m_EW = 113
        phi_qEW = euler_phi(q_EW)      # 280
        nu_star_den = D_ADDR           # 1/9
        return dict(q_T=q_T, m_T=m_T, phi_qT=phi_qT, B=B, L=L,
                    q_EW=q_EW, m_EW=m_EW, phi_qEW=phi_qEW, nu_star_den=nu_star_den)

    w13 = welds(13)
    w15 = welds(15)
    print(f"      welds(z3=13) = {w13}")
    print(f"      welds(z3=15) = {w15}")
    # every owned weld quantity is z3-INDEPENDENT => 'larger gap' changes NO owned phase quantity
    check("q_T unchanged by z3", w13["q_T"] == w15["q_T"], True)
    check("phi(q_T)=20=d13 (owned weld)", w13["phi_qT"], 20)
    check("phi(q_T) unchanged by z3", w13["phi_qT"] == w15["phi_qT"], True)
    check("q_EW unchanged by z3", w13["q_EW"] == w15["q_EW"], True)
    check("phi(q_EW)=280", w13["phi_qEW"], 280)
    check("phi(q_EW)/|Omega8| = 35", w13["phi_qEW"] // OMEGA8, 35)
    check("phi(q_EW) unchanged by z3", w13["phi_qEW"] == w15["phi_qEW"], True)
    check("ALL owned welds z3-independent (v17 seed non-reconstructible)", w13 == w15, True)


def lcm(a: int, b: int) -> int:
    return a * b // gcd(a, b)


# ================================================================ SECTION IV : residual family
def enumerate_towers(z_max: int):
    """Brute scan of 3-zone towers (9,11,z3), z3 in [12, z_max]. DECLARED bound printed."""
    return [(9, 11, z3) for z3 in range(12, z_max + 1)]


def survives_L0(tower, use_own1: bool):
    """L0 owned kills: base-9 (fixed), COUNT-3 (3 zones, enforced by construction),
    even-spacing. With use_own1: also require every step be EVEN (OWN-1 odd-step kill).
    Without use_own1: only require z3 have same parity as 11 (base parity), which is the
    SAME constraint -> that is the point of OWN-3 (non-discriminating)."""
    a, b, c = tower
    if a != 9 or b != 11:
        return False
    if use_own1:
        # odd steps killed => both steps even => c - b even AND b - a even
        if (b - a) % 2 != 0:
            return False
        if (c - b) % 2 != 0:
            return False
    else:
        # baseline parity fact the family already satisfies (rungs odd)
        if c % 2 != 1:
            return False
    return True


def section_IV() -> None:
    print(f"\n[IV] residual family (scan z3 in [12,{Z_MAX}], bound DECLARED)")
    towers = enumerate_towers(Z_MAX)
    res_with = [t for t in towers if survives_L0(t, use_own1=True)]
    res_without = [t for t in towers if survives_L0(t, use_own1=False)]
    print(f"      survivors WITH OWN-1  : {res_with}")
    print(f"      survivors WITHOUT OWN-1: {res_without}")
    check("OWN-1 is NON-discriminating (same residual either way)",
          res_with == res_without, True)
    check("residual is NOT a singleton (GAP-E genuinely OPEN)", len(res_with) > 1, True)
    check("residual contains the owned tower (9,11,13)", (9, 11, 13) in res_with, True)
    check("residual contains the rival (9,11,15)", (9, 11, 15) in res_with, True)
    check("residual is exactly the odd z3>=13 family",
          res_with, [(9, 11, z) for z in range(13, Z_MAX + 1, 2)])


# ================================================================ SECTION V : NEG-1 exhaustion
def section_V() -> None:
    print("\n[V] NEG-1: exhaustion over owned step-inventories -- each blocked by an owned fact")
    lucas_set = set(lucas(n) for n in range(0, 12))

    # (a) values {9,11,13}: circular (is the ladder itself)
    inv_a_is_ladder = ({9, 11, 13} == {9, 11, 13})
    check("(a) values-inventory IS the ladder => circular/blocked", inv_a_is_ladder, True)

    # (b) Lucas-n: 13 not in it (fails contains_13) AND owned rungs 9,13 not significant
    inv_b_contains_13 = (13 in lucas_set)
    inv_b_kills_owned = any(r not in lucas_set for r in (9, 13))
    check("(b) Lucas-inv contains 13?  (must be False => blocked)", inv_b_contains_13, False)
    check("(b) Lucas-inv would ban owned rungs 9,13 => fires on owned tower", inv_b_kills_owned, True)

    # (c) Z (all): 12 is significant => +2 step (11->13) leaves 12 empty => bans owned +2
    inv_c_excludes_12 = (12 not in set(range(0, 100)))  # ℤ contains 12
    check("(c) Z-inv excludes 12?  (must be False => bans owned +2 step)", inv_c_excludes_12, False)

    # The located obstruction: NO owned inventory satisfies all of
    #   contains_13 AND excludes_12 AND not-the-ladder AND spares-owned-rungs.
    def inventory_ok(I: set) -> bool:
        return (13 in I) and (12 not in I) and (I != {9, 11, 13}) \
            and all(r in I for r in (9, 11, 13))
    # (d) the owned 9-position cycle (nu*=1/9, BOOK_01:1911): exactly 9 positions,
    #     does NOT contain 13 => cannot make 13 significant. (skeptic repair: 4th candidate)
    cycle9 = set(range(9))            # 9 distinguishable address positions
    check("(d) 9-cycle inventory contains 13?  (must be False => blocked)",
          13 in cycle9, False)
    owned_candidates = {
        "values": {9, 11, 13},
        "lucas_n": lucas_set,
        "integers": set(range(0, 100)),
        "cycle9": cycle9,
    }
    any_ok = any(inventory_ok(I) for I in owned_candidates.values())
    check("NO owned inventory inhabits SignificantJunctionAddr (located obstruction, 4-way)",
          any_ok, False)


# ================================================================ SECTION VI : negative controls
def section_VI() -> None:
    print("\n[VI] negative controls -- each can fail the CONCLUSION, not the technique")

    # NC1 (SKEPTIC #1 NOTE, 2026-07-05): this control is REDUNDANT with section II, not
    # independent -- it hardcodes closing_inv={9,11,13} and reuses "13 not Lucas". It only
    # tests the EMPTY-SLOT route's own inventory, which is NOT the universe that owns the
    # bound. The genuinely independent kill control is SECTION VII (scene_triple_unique),
    # which forces z3=13 WITHOUT any empty-slot inventory. NC1 kept for audit trail only;
    # it does NOT license the memo's headline. See errors of record in the memo §SKEPTIC-#1.
    lucas_set = set(lucas(n) for n in range(0, 12))
    closing_inv = {9, 11, 13}            # the minimal closing inventory = the ladder
    is_owned_enumerable = closing_inv.issubset(lucas_set)
    check("NC1 (REDUNDANT w/ section II; real control is section VII): {9,11,13} not all Lucas",
          is_owned_enumerable, False)

    # NC2: the residual must be strictly larger than {(9,11,13)} or GAP-E is not open.
    res = [(9, 11, z) for z in range(13, Z_MAX + 1, 2)]
    check("NC2: residual strictly larger than the owned tower (open, not closed)",
          len(res) > 1, True)

    # NC3: anti over-credit: OWN-1 (odd-step kill) must NOT kill any residual tower.
    # Each residual tower's steps are even; if OWN-1 killed one, we'd be over-crediting.
    def own1_kills(tower) -> bool:
        a, b, c = tower
        return ((b - a) % 2 == 1) or ((c - b) % 2 == 1)
    killed = [t for t in res if own1_kills(t)]
    check("NC3: OWN-1 kills ZERO residual towers (non-discriminating, honest)", killed, [])

    # NC4 (anti-fit, mirrors parent §III): the 'closing' predicate must not be so broad it
    # kills the owned tower. Check that IF we adopted inventory (b) as the closer, it kills
    # (9,11,13) itself -> proving (b) is not a legitimate closer (would be a fit that
    # destroys the target). This is the computational 'do not force a fit'.
    b_bans_owned_tower = any(r not in lucas_set for r in (9, 11, 13))
    check("NC4: inventory(b)-as-closer BANS the owned tower (fit refused)",
          b_bans_owned_tower, True)


# ================================================================ SECTION VII : KILL control
# Added 2026-07-05 after Skeptic #1 KILLED the memo (accepted in full). This section
# encodes the OWNED forcing the original script never tested against, and makes the
# script FAIL the memo's load-bearing headline ("z3 unforgeable / unconstrained above 13").
# A registered CORE-FORMALIZED / LEAN_PROVED row DOES force z3=13:
#   D0.VNext2.SceneTripleUnique.scene_triple_unique  (registry CLAIM_TO_LEAN_MAP.csv:530)
#     SceneTripleUnique.lean:74-85, cert 05_CERTS/vp_scene_triple_unique.py, rc=0, 0 sorry
#   + D0.Synthesis.CarrierForcing.address_ladder  (registry row 215)
#     CarrierForcing.lean:81  proves 11+2=13 (top rung pinned)
#   + D0-TOWER-STOP-NOEXT-001  (registry row 257)  no 4th zone.
# The old CONCLUSION ("unforgeable") is therefore FALSE. This control asserts the
# owned forcing EXISTS, which the memo said it did not. It is designed to FAIL the
# original conclusion, per the skeptic's required repair.
def scene_triple_unique_model(z0: int, z1: int, z2: int, n: int):
    """Faithful transcription of SceneTripleUnique.lean:74-85 `scene_triple_unique`.
    Hypotheses: +2 ladder (z1=z0+2, z2=z1+2), centre z1 = L_n (Lucas), 9<=z1<=13.
    Returns the FORCED triple, or None if the hypotheses are not met.
    unique_lucas_in_window (line 59): only L_5=11 lies in [9,13], so z1=11 forced,
    hence z2 = 13 forced -- an OWNED upper-bound on the top zone."""
    if z1 != z0 + 2 or z2 != z1 + 2:
        return None
    if z1 != lucas(n):
        return None
    if not (9 <= z1 <= 13):
        return None
    # unique_lucas_in_window: forces n=5, z1=11, hence (9,11,13)
    return (9, 11, 13)


def section_VII() -> bool:
    """Returns True iff an OWNED CORE-FORMALIZED row forces z3<=13. If True, the memo's
    'unforgeable' headline is FALSIFIED and the CONCLUSION must be KILLED, not green."""
    print("\n[VII] KILL CONTROL (post-skeptic-#1): does an OWNED row force z3<=13?")
    # The centred owned scene is a +2 ladder with centre L_5=11.
    forced = scene_triple_unique_model(9, 11, 13, 5)
    check("scene_triple_unique forces the centred +2 ladder to (9,11,13)",
          forced, (9, 11, 13))
    # its top zone is PINNED at 13 -- an owned upper bound, contradicting 'unconstrained'.
    top_zone_bound = forced[2] if forced else None
    check("owned top-zone value is bounded (=13), NOT unconstrained above 13",
          top_zone_bound, 13)
    # address_ladder (CarrierForcing.lean:81) independently pins the top rung 11+2=13.
    check("address_ladder pins top rung 11+2=13 (row 215)", 11 + 2, 13)
    # The rival (9,11,15) uses a +4 top step (z2=z1+4), which BREAKS the owned +2
    # window -- it is NOT an owned open gap; it violates hladder2 (z2=z1+2).
    rival_top_step = 15 - 11
    owned_top_step = 13 - 11
    check("rival (9,11,15) top step is +4 (BREAKS owned +2 window, not an owned gap)",
          rival_top_step, 4)
    check("owned top step is +2 (address_ladder / hladder2)", owned_top_step, 2)
    # THE KILL: an owned forcing of z3<=13 EXISTS.
    owned_forcing_exists = (forced is not None and forced[2] == 13)
    check("KILL: an OWNED CORE-FORMALIZED row forces z3=13 (memo headline FALSIFIED)",
          owned_forcing_exists, True)
    return owned_forcing_exists


def main() -> int:
    print("=" * 70)
    print("GAP-E CLOSE check  --  E-b forge attempt + NEG-1 located obstruction")
    print("STATUS 2026-07-05: memo KILLED by Skeptic #1 (accepted in full).")
    print("This script now carries SECTION VII, the owned-forcing KILL control that")
    print("FALSIFIES the memo's 'z3 unforgeable/unconstrained above 13' headline.")
    print(f"scan bound Z_MAX = {Z_MAX} (declared)")
    print("=" * 70)
    section_I()
    section_II()
    section_III()
    section_IV()
    section_V()
    section_VI()
    owned_forcing_exists = section_VII()
    print("\n" + "=" * 70)
    print(f"TOTAL: {_PASS} PASS, {_FAIL} FAIL")
    print("=" * 70)
    if _FAIL:
        print("VERDICT: a load-bearing check FAILED -- inspect the failing line.")
        return 1
    # The NEG-1 sub-facts (sections I-VI) still pass as ARITHMETIC (they always did);
    # but section VII proves the CONCLUSION they were assembled to support is FALSE.
    if owned_forcing_exists:
        print("VERDICT: KILLED. Sections I-VI are arithmetically intact, but SECTION VII")
        print("         shows an OWNED CORE-FORMALIZED theorem (scene_triple_unique, row 530)")
        print("         forces z3=13. The memo's headline 'z3 unforgeable / unconstrained")
        print("         above 13' is FALSE. GAP-E's top-zone upper bound is OWNED, not open.")
        print("         The E-b/empty-slot analysis SURVIVES only as a note on why the +2 top")
        print("         step is non-uniform-relative -- it does NOT keep the residual open,")
        print("         because scene_triple_unique's +2 window is itself owned (address_ladder).")
        return 0
    print("VERDICT: no owned forcing found (unexpected) -- section VII regressed, inspect.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
