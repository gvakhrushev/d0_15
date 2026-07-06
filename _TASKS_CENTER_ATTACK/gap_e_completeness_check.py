#!/usr/bin/env python3
"""GAP-E — extension-list completeness {D2, ABCD}: kill attribution + underdetermination map.

Companion to _TASKS_CENTER_ATTACK/GAP_E_COMPLETENESS_MEMO.md (DRAFT, pre-skeptic).
Status: NO registry row edited; this is an analysis cert for the GAP-E attack, not a claim cert.

WHAT IS COMPUTED (exact integer arithmetic only, no floats):
  I    The owned capacity chain and its two structurally-distinct readings (over-base vs
       consecutive) — numeric agreement, structural fork.
  II   The owned-alphabet inventory {1,2,4,8} vs the used extension list {2,4}: the coined
       "extensions = owned alphabet objects" principle UNDER-kills (admits +1, +8) — the
       remaining kills must be assembled, and their scoping predicate is the missing object.
  III  The scoping dilemma, computed: of the two candidate type-identity predicates, the
       broad one (factor-sharing) kills the OWNED tower itself; the narrow one (exact
       alphabet identity) gives the right answer but is coined. No owned text selects.
  IV   Kill matrix over candidate towers: which constraint tier kills which tower.
       Tiers: L0 = Lean-owned today; L0+ = L0 + window-free centre reading;
       G-CAP = narrated §01.20 extension list; G-STEP = narrated +2-minimality.
       Headline: (9,11,15) passes L0+ and dies ONLY on a narrated guard;
       (9,11,13,15) dies on owned COUNT-3 (tower-stop), NOT on GAP-E.
  V    R2 check: the §01.22 terminal-capacity ledger (q_T=44, m_T=7, phi(44)=20=d13,
       q_EW=710, m_EW=113, phi(710)=280=35*8) is computed twice — once from (9,11,13),
       once from (9,11,15) — showing the weld quantity d_top=20 does NOT change, i.e. the
       ledger runs DOWNSTREAM of the extension list and provides zero upward forcing.
  VI   Negative controls, each able to fail the CONCLUSION (not the technique).

FAILABILITY: every check() compares an independently-computed quantity against a fixed
target; none constructs its key quantity from the conclusion. The tower enumeration is a
brute scan over a declared finite range with the range printed (no candidate hidden).
"""
from __future__ import annotations

import sys
from itertools import combinations
from math import gcd

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# ---------------------------------------------------------------- owned constants
WITNESS = 1          # |{omega_0}|        FiniteTypes.lean:13-14 (posited PUnit)
DYAD = 2             # |D2|               FiniteTypes.lean:18  card_dyad
ORIENT = 2           # |{+,-}|            FiniteTypes.lean (Orient := Bool)
ROLE = 4             # |ABCD| = D2 x D2   FiniteTypes.lean:21  card_role; BOOK_03 03.23.1
OMEGA8 = 8           # |Omega8|           FiniteTypes.lean:24; DyadABCD.lean:17
BASE = OMEGA8 + WITNESS   # 9             card_v9
COUNT_ZONES = 3      # NoExtension.lean no_extension_theorem (count reading, docstring :25-27)

FAILED: list[str] = []
N_CHECK = 0


def check(name: str, cond: bool, note: str = "") -> None:
    global N_CHECK
    N_CHECK += 1
    tag = "PASS" if cond else "FAIL"
    if not cond:
        FAILED.append(name)
    print(f"{tag}  {name}" + (f"  :: {note}" if note else ""))


def lucas(n: int) -> int:
    a, b = 2, 1  # L0, L1
    if n == 0:
        return 2
    for _ in range(n - 1):
        a, b = b, a + b
    return b


def euler_phi(n: int) -> int:
    result, x, p = n, n, 2
    while p * p <= x:
        if x % p == 0:
            while x % p == 0:
                x //= p
            result -= result // p
        p += 1
    if x > 1:
        result -= result // x
    return result


# =================================================================================
print("=" * 88)
print("I. OWNED CHAIN — two readings of the same numbers (the extension-layer fork)")
print("=" * 88)
V9, V11, V13 = BASE, BASE + DYAD, BASE + ROLE
check("chain (9,11,13) from owned cardinalities", (V9, V11, V13) == (9, 11, 13),
      f"V9={V9} V11={V11} V13={V13}")
# over-base reading (S01.20/S01.22 + FiniteTypes types): extensions over V9 are {2,4}
over_base_exts = (V11 - V9, V13 - V9)
# consecutive reading (BOOK_03 ladder + address_ladder numerals): steps are {2,2}
consecutive_steps = (V11 - V9, V13 - V11)
check("over-base extension multiset {2,4}", over_base_exts == (2, 4), str(over_base_exts))
check("consecutive step multiset {2,2}", consecutive_steps == (2, 2), str(consecutive_steps))
check("fork agrees numerically ONLY because |ABCD| = 2*|D2| (4=2+2)",
      ROLE == DYAD + DYAD and ROLE == DYAD * DYAD,
      "4 = 2+2 = 2x2; the two readings coincide on cardinality, differ on structure")

# =================================================================================
print()
print("=" * 88)
print("II. R1 — coined principle 'extensions = owned alphabet objects': UNDER-kills")
print("=" * 88)
owned_alphabet_sizes = sorted({WITNESS, DYAD, ORIENT, ROLE, OMEGA8})  # {1,2,4,8}
used_extension_sizes = sorted(set(over_base_exts))                    # {2,4}
check("owned alphabet size set = {1,2,4,8}", owned_alphabet_sizes == [1, 2, 4, 8],
      str(owned_alphabet_sizes))
check("used extensions {2,4} PROPER subset of owned sizes",
      set(used_extension_sizes) < set(owned_alphabet_sizes),
      "the coined principle alone admits +1 (witness copy) and +8 (Omega8 copy)")
r1_admits_extra = sorted(set(owned_alphabet_sizes) - set(used_extension_sizes))
check("R1 residue needing separate kills = {1,8}", r1_admits_extra == [1, 8],
      "+1 kill: witness repeat (CASE-2 assembled); +8 kill: needs type-identity predicate")

# =================================================================================
print()
print("=" * 88)
print("III. THE SCOPING DILEMMA — the missing type-identity predicate, computed")
print("=" * 88)
# Owned base construction: V9 = (ABCD x {+,-}) u {omega_0}. Factors present in the base:
# witness (1), the two dyad factors of ABCD, the orient dyad, ABCD itself, Omega8 itself.
# Candidate predicate P_broad(X):  X shares a constituent alphabet with the base => repeat.
# Candidate predicate P_narrow(X): X IS an alphabet already realized as a whole in the base
#                                  construction chain (Omega8, or the witness point).
base_constituents = {"witness", "dyad", "role", "omega8"}  # all appear in V9's construction


def p_broad(ext: str) -> bool:   # kills if ANY constituent already in base
    constituents = {"dyad": {"dyad"}, "role": {"role", "dyad"},
                    "omega8": {"omega8", "role", "dyad"}, "witness": {"witness"}}[ext]
    return bool(constituents & base_constituents)


def p_narrow(ext: str) -> bool:  # kills only exact whole-alphabet repeats of base layers
    return ext in {"omega8", "witness"}


broad_kills = {e for e in ["witness", "dyad", "role", "omega8"] if p_broad(e)}
narrow_kills = {e for e in ["witness", "dyad", "role", "omega8"] if p_narrow(e)}
check("P_broad (factor-sharing) kills EVERYTHING incl. the owned D2 and ABCD",
      broad_kills == {"witness", "dyad", "role", "omega8"},
      "too strong: destroys the owned tower itself -> not the corpus predicate")
check("P_narrow (whole-alphabet identity) kills exactly {witness, omega8}",
      narrow_kills == {"witness", "omega8"},
      "right answer {D2,ABCD} survives -- but P_narrow is COINED, no owned text states it")
check("the two candidate predicates DISAGREE on the owned extensions",
      (broad_kills != narrow_kills) and ("dyad" in broad_kills) and ("dyad" not in narrow_kills),
      "the choice between them is exactly the missing owned object (GAP-E's core)")

# =================================================================================
print()
print("=" * 88)
print("IV. KILL MATRIX — candidate towers vs constraint tiers")
print("=" * 88)
ZMAX = 21  # declared scan bound (all zone sizes <= ZMAX; printed, nothing hidden)
lucas_vals = {lucas(n) for n in range(1, 12)}


def tier_L0(t: tuple) -> bool:
    """Lean-owned today: base 9 (card_v9), zone count 3 (NoExtension reading),
    all consecutive steps even (det_T_pow evenness), strictly increasing."""
    return (len(t) == COUNT_ZONES and t[0] == BASE
            and all(b > a for a, b in zip(t, t[1:]))
            and all((b - a) % 2 == 0 for a, b in zip(t, t[1:])))


def tier_L0_centre(t: tuple) -> bool:
    """L0 + window-free centre reading: z2 = smallest Lucas value > Omega8 = 8
    ([Iter25] BOOK_01:1500 narrated reading; Lean numerics level_five_forced)."""
    smallest_lucas_gt_8 = min(v for v in lucas_vals if v > OMEGA8)
    return tier_L0(t) and t[1] == smallest_lucas_gt_8


def guard_cap(t: tuple) -> bool:
    """G-CAP, narrated S01.20 ('the only primitive unresolved capacities'):
    over-base extensions are exactly {D2, ABCD} = {+2, +4}."""
    return tier_L0(t) and sorted((t[1] - t[0], t[2] - t[0])) == [DYAD, ROLE]


def guard_step(t: tuple) -> bool:
    """G-STEP, narrated S01.22:1901-1907 minimality / S00.2:52 Darboux strictness:
    every consecutive junction step is exactly +2."""
    return tier_L0(t) and all(b - a == 2 for a, b in zip(t, t[1:]))


three_towers = [(9, a, b) for a in range(10, ZMAX + 1) for b in range(a + 1, ZMAX + 1)]
L0_pass = [t for t in three_towers if tier_L0(t)]
L0c_pass = [t for t in three_towers if tier_L0_centre(t)]
cap_pass = [t for t in three_towers if guard_cap(t)]
step_pass = [t for t in three_towers if guard_step(t)]

print(f"scan: 3-zone towers (9,z2,z3), z3 <= {ZMAX}")
print(f"  L0   (Lean-owned: base+count+evenness)     -> {len(L0_pass)} pass: {L0_pass}")
print(f"  L0+  (L0 + centre z2=11 narrated reading)  -> {len(L0c_pass)} pass: {L0c_pass}")
print(f"  G-CAP  (narrated extension list)           -> {cap_pass}")
print(f"  G-STEP (narrated +2-minimality)            -> {step_pass}")

check("L0 admits an unbounded family (many towers in range)", len(L0_pass) > 10,
      f"{len(L0_pass)} towers pass Lean-owned constraints alone")
check("L0+ residual family is exactly (9,11,z3), z3 odd >= 13",
      L0c_pass == [(9, 11, z) for z in range(13, ZMAX + 1, 2)],
      "after every owned+centre constraint, ONLY the top zone size is free")
check("(9,11,15) PASSES L0+ (the WINDOW memo WEAKEST_LINK_DEMO, reproduced + centre)",
      (9, 11, 15) in L0c_pass)
check("G-CAP alone pins the unique tower (9,11,13)", cap_pass == [(9, 11, 13)])
check("G-STEP alone pins the unique tower (9,11,13)", step_pass == [(9, 11, 13)])
check("EITHER narrated guard suffices; they agree on the survivor",
      cap_pass == step_pass == [(9, 11, 13)],
      "upper end is doubly guarded -- both guards narrated, neither Lean")

# 4-zone towers: die on owned COUNT-3, not on GAP-E
four_towers = [(9, a, b, c) for a in range(10, ZMAX + 1)
               for b in range(a + 1, ZMAX + 1) for c in range(b + 1, ZMAX + 1)]
count3_kills_4zone = all(not tier_L0(t) for t in four_towers)  # len!=3 fails tier_L0
check("(9,11,13,15) and ALL 4-zone towers die on owned COUNT-3 (tower-stop)",
      count3_kills_4zone and (9, 11, 13, 15) in four_towers,
      "the tower-stop no-go carries 4-zone kills; GAP-E carries only the 3-zone top size")

# once-only, assembled from owned pieces: equal-size zones => nontrivial zone-swap
def equal_size_zones(t: tuple) -> bool:
    return len(set(t)) < len(t)


reuse_tower = (9, 11, 11)  # over-base D2 re-used => two size-11 zones
check("over-base capacity RE-USE => equal-size zones => owned S2 zone-swap kill",
      equal_size_zones(reuse_tower) and not tier_L0(reuse_tower),
      "|S2|>1 Lean (NoExtension:47) + size-distinctness reading (BOOK_01:1518) -- ASSEMBLED")

# =================================================================================
print()
print("=" * 88)
print("V. R2 — the S01.22 terminal-capacity ledger runs DOWNSTREAM (zero upward forcing)")
print("=" * 88)


def ledger(v9: int, v11: int, v13: int) -> dict:
    V = v9 + v11 + v13
    d_top = v9 + v11                       # degree of every top-zone vertex
    q_T = (ROLE * v11) // gcd(ROLE, v11)   # lcm(|ABCD|, V11)
    m_T = ROLE + 3                         # |ABCD| + rank(A_K) = 4 + 3
    B = ROLE + 1                           # pointed terminal alphabet = 5
    L = 2 * V + B                          # bilateral scene line
    q_EW = 2 * B * L
    m_EW = B * euler_phi(q_T) + v13
    return {"V": V, "d_top": d_top, "q_T": q_T, "phi_qT": euler_phi(q_T), "m_T": m_T,
            "B": B, "L": L, "q_EW": q_EW, "m_EW": m_EW, "phi_qEW": euler_phi(q_EW)}


led_owned = ledger(9, 11, 13)
led_1115 = ledger(9, 11, 15)
print(f"  ledger(9,11,13): {led_owned}")
print(f"  ledger(9,11,15): {led_1115}")
check("owned ledger reproduces S01.22 exactly: q_T=44, phi=20=d_top, m_T=7, q_EW=710, m_EW=113, phi=280",
      (led_owned["q_T"], led_owned["phi_qT"], led_owned["d_top"], led_owned["m_T"],
       led_owned["q_EW"], led_owned["m_EW"], led_owned["phi_qEW"]) == (44, 20, 20, 7, 710, 113, 280)
      and led_owned["phi_qEW"] // OMEGA8 == 35 and led_owned["phi_qEW"] % OMEGA8 == 0)
check("the weld quantity d_top = 20 = phi(44) is UNCHANGED for (9,11,15)",
      led_1115["d_top"] == 20 and led_1115["q_T"] == 44 and led_1115["phi_qT"] == 20,
      "d_top = |V9|+|V11| never sees z3 -- the weld cannot detect the top size")
check("downstream EW numbers change for (9,11,15) but nothing owned pins them a priori",
      led_1115["q_EW"] != 710 and led_1115["m_EW"] != 113,
      f"q_EW={led_1115['q_EW']}, m_EW={led_1115['m_EW']}: detection-after-the-fact, not forcing")
check("R2 verdict: the ONE candidate a-priori weld identity phi(q_T)=d_top HOLDS FOR BOTH towers",
      led_owned["phi_qT"] == led_owned["d_top"] and led_1115["phi_qT"] == led_1115["d_top"],
      "the S01.22 weld cannot discriminate (9,11,13) from (9,11,15): no upward forcing exists")

# =================================================================================
print()
print("=" * 88)
print("VI. NEGATIVE CONTROLS (each can fail the CONCLUSION)")
print("=" * 88)
# NC1: if the corpus DID own an interval/size-cap at the extension layer, (9,11,15)
# would fail L0+. It does not fail -> the gap is real (this control failing would
# mean GAP-E is already closed and this memo is moot).
check("NC1 gap-is-real: (9,11,15) NOT killed by any Lean-owned constraint",
      (9, 11, 15) in L0c_pass)

# NC2: mutate the owned alphabet -- hypothetical owned size-6 object would make
# an R1-style G-CAP admit (9,11,15). E-ENUM's kill power is inventory-dependent.
mutated_sizes = set(owned_alphabet_sizes) | {6}
def guard_cap_mut(t):
    return tier_L0(t) and all(d in mutated_sizes for d in (t[1] - t[0], t[2] - t[0]))
check("NC2 inventory-sensitivity: adding a size-6 owned object would admit (9,11,15)",
      guard_cap_mut((9, 11, 15)),
      "an alphabet-based completeness principle is falsifiable by the owned inventory")

# NC3: mutate zone count 3 -> 4: (9,11,13,15) becomes admissible under a count-4 tier.
def tier_L0_count4(t):
    return (len(t) == 4 and t[0] == BASE and all(b > a for a, b in zip(t, t[1:]))
            and all((b - a) % 2 == 0 for a, b in zip(t, t[1:])))
check("NC3 COUNT-3 load: with count=4 the tower (9,11,13,15) passes",
      tier_L0_count4((9, 11, 13, 15)),
      "confirms 4-zone kills trace to NoExtension count, which IS owned")

# NC4: the anti-fit control -- P_broad applied as the completeness predicate kills the
# owned tower (no admissible extension at all), so no honest fit is available cheaply.
no_ext_survives_broad = [e for e in ["dyad", "role"] if not p_broad(e)]
check("NC4 anti-fit: the broad predicate leaves NO admissible extension (owned tower dies)",
      no_ext_survives_broad == [],
      "any forced-fit attempt at the predicate must thread between too-strong and coined")

# NC5: evenness (what Lean owns) admits +4 steps: (9,13,17) passes L0 (no centre).
check("NC5 evenness-only: (9,13,17) passes L0 -- det_T_pow owns evenness, not +2",
      (9, 13, 17) in L0_pass,
      "reproduces WINDOW memo NC_PARITY_ADMITS_PLUS4 at the tower level")

# =================================================================================
print()
print("=" * 88)
n_pass = N_CHECK - len(FAILED)
print(f"RESULT: {n_pass}/{N_CHECK} checks PASS" + ("" if not FAILED else f"; FAILED: {FAILED}"))
print("VERDICT: R1 near-miss (skeleton owned; ONE predicate missing, computed underdetermined")
print("         between P_broad/P_narrow); R2 no-forcing (ledger downstream); R3 spec stands:")
print("         missing object = owned type-identity/enumeration clause OR owned +2-no-skip")
print("         clause; EITHER pins (9,11,13) uniquely (Section IV).")
sys.exit(0 if not FAILED else 1)
