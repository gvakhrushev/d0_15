#!/usr/bin/env python3
"""window_forcing_check — G1 window-bounds residual: what owns [9,13], and does the
dissolve-window restatement carry the same load? (DRAFT companion to
_TASKS_CENTER_ATTACK/WINDOW_9_13_FORCING_MEMO.md; no registry row.)

CHECKS — 11 check() calls, exact integer arithmetic; ~10 independent (WINDOW_ENDPOINTS_DERIVED
is a projection of OWNED_CHAIN_TRIPLE). Failability, stated honestly: the OWNED_CHAIN_* and
NC_* checks can fail the CONCLUSION; the new-criteria half of KILL_MATRIX_AGREEMENT mirrors
the owned chain by construction, so on its own it is failable mainly through a mirror-coding
error — its conclusion-failing power lives in the OLD-criteria column plus the agreement
requirement (skeptic-pass repair B-1):
  1. OWNED-CHAIN: the Lean-owned cardinality chain (FiniteTypes.lean: card Omega8 = 8,
     Witness = 1, Dyad = 2, Role = 4; V9 = Omega8 (+) Witness, V11 = V9 (+) Dyad,
     V13 = V9 (+) Role) yields exactly (9,11,13) with steps (+2,+2) — no interval used.
  2. FORK: 9 has TWO owned decompositions, 8+1 (BOOK_01 §01.20/§01.8) and 4+5
     (BOOK_03 03.23.6 / BOOK_04 §04.1.START). Numerically equal, structurally
     unidentified — flagged, not resolved.
  3. KILL MATRIX: for each alternative triple, which owned killer fires?
     Killers: BASE-9 (V9 capacity, needs GAP-W for the +1), STEP-SET (extensions are
     exactly {Dyad, Role}, GAP-E), COUNT-3 (NoExtension), PARITY (det T^n = (-1)^n:
     steps must be EVEN — note: parity does NOT single out +2), OLD-WINDOW (Lucas
     centre in [9,13] — the criterion being dissolved).
     Load-bearing demo: (9,11,15) passes BASE-9 + PARITY + COUNT-3 and is killed
     ONLY by STEP-SET (GAP-E) — GAP-E is the weakest link, not tower-stop.
  4. LEVEL-5 MINIMALITY IS PARITY-FREE: the first n>=1 with L_n > 8 is n=5 in the FULL
     Lucas sequence (L_2=3, L_4=7 both <=8): the "smallest ODD" restriction in
     level_five_forced is consistent but not load-bearing for minimality.
  5. NEGATIVE CONTROLS:
     (a) mutate |Omega8| -> 10: chain gives (11,13,15) != (9,11,13) — conclusion fails;
     (b) old route: widening the window to [9,29] admits L_7=29 (uniqueness breaks);
         new route: unaffected (consumes no window) — the load moves where claimed;
     (c) even-step parity admits +4: (9,13,17) passes PARITY — so PARITY alone cannot
         replace STEP-SET (if this control ever fails, parity would secretly own +2).
"""
import sys

def lucas(n: int) -> int:
    a, b = 2, 1  # L_0, L_1
    if n == 0:
        return 2
    for _ in range(n - 1):
        a, b = b, a + b
    return b

FAILS = []

def check(name: str, cond: bool, detail: str = ""):
    tag = "PASS" if cond else "FAIL"
    print(f"{tag} {name}" + (f" :: {detail}" if detail else ""))
    if not cond:
        FAILS.append(name)

print("=== window_forcing_check — G1 [9,13] residual (DRAFT, no registry row) ===\n")

# --- 1. OWNED-CHAIN (mirrors FiniteTypes.lean abbrevs + card theorems) -------------
card_dyad = 2          # card_dyad    (FiniteTypes.lean:18)
card_role = card_dyad * card_dyad   # card_role = 4 (FiniteTypes.lean:21); Role := Dyad x Dyad
card_orient = 2        # Orient := Bool
card_omega8 = card_role * card_orient  # card_omega8 = 8 (FiniteTypes.lean:24); Omega8 := Role x Orient
card_witness = 1       # Witness := PUnit
V9 = card_omega8 + card_witness       # V9  := Sum Omega8 Witness
V11 = V9 + card_dyad                  # V11 := Sum V9 Dyad
V13 = V9 + card_role                  # V13 := Sum V9 Role
check("OWNED_CHAIN_TRIPLE", (V9, V11, V13) == (9, 11, 13), f"({V9},{V11},{V13})")
check("OWNED_CHAIN_STEPS_+2_+2", (V11 - V9, V13 - V11) == (2, 2),
      f"steps=({V11-V9},{V13-V11}) from card Dyad=2, card Role-card Dyad=2")
check("CENTRE_IS_L5", V11 == lucas(5), f"V11={V11}, L_5={lucas(5)}")
check("WINDOW_ENDPOINTS_DERIVED", (V9, V13) == (9, 13),
      "[9,13] = [card V9, card V13] — endpoints are outputs, not inputs")

# --- 2. FORK: two owned decompositions of 9 ---------------------------------------
d_anchor, d_sigma = 4, 5
check("FORK_NUMERIC_AGREEMENT", card_omega8 + 1 == d_anchor + d_sigma == 9,
      "8+1 (BOOK_01 §01.20) = 4+5 (BOOK_03 03.23.6) = 9; NO owned identification of the summand structures")

# --- 3. KILL MATRIX ----------------------------------------------------------------
# Owned killers, each as a predicate on a zone-size tuple.
def base9(t):      # BASE-9: first zone is the pointed shell |Omega8|+1 (GAP-W carries the +1)
    return t[0] == card_omega8 + card_witness

def step_set(t):   # STEP-SET (GAP-E): extensions over V9 are exactly {Dyad, Role} => sizes V9+2, V9+4
    return len(t) >= 3 and t[1] == t[0] + card_dyad and t[2] == t[0] + card_role

def count3(t):     # COUNT-3 (NoExtension reading): exactly three zones
    return len(t) == 3

def parity(t):     # PARITY (det_T_pow): consecutive steps even (orientation class preserved)
    return all((b - a) % 2 == 0 and b > a for a, b in zip(t, t[1:]))

def old_window(t): # OLD-WINDOW: centre is a Lucas number inside [9,13]
    if len(t) != 3:
        return False
    c = t[1]
    return any(lucas(n) == c for n in range(0, 15)) and 9 <= c <= 13 \
        and t[0] == c - 2 and t[2] == c + 2

CANDS = [
    (9, 11, 13),        # the scene
    (8, 10, 12),        # no witness (V8 base)
    (9, 11, 15),        # 3rd zone oversized: 15 = 9+6, no owned 6-extension
    (9, 13, 17),        # +4 ladder — parity-even, wrong steps
    (9, 12, 15),        # +3 ladder — odd step
    (11, 13, 15),       # base 11 (skips the pointed shell)
    (7, 9, 11),         # base 7 (loses one signed role)
    (9, 11, 13, 15),    # 4 zones
    (9, 29, 49),        # centre L_7 with +20 steps (even!) — old window kills, so does step-set
]
print("\ncandidate            BASE9 STEPSET COUNT3 PARITY OLDWIN  admitted-by-new admitted-by-old")
agree = True
for t in CANDS:
    b, s, c, p, w = base9(t), step_set(t), count3(t), parity(t), old_window(t)
    new_ok = b and s and c          # dissolve-route criteria (parity subsumed by step-set)
    old_ok = w and c                # old capstone criteria (ladder+lucas+window)
    agree &= (new_ok == old_ok == (t == (9, 11, 13)))
    print(f"{str(t):20} {b!s:5} {s!s:7} {c!s:6} {p!s:6} {w!s:6}  {new_ok!s:15} {old_ok}")
check("KILL_MATRIX_AGREEMENT", agree,
      "new (base+steps+count) and old (ladder+lucas+window) admit exactly {(9,11,13)}")

t_weak = (9, 11, 15)
check("WEAKEST_LINK_DEMO", base9(t_weak) and parity(t_weak) and count3(t_weak)
      and not step_set(t_weak),
      "(9,11,15) passes BASE-9+PARITY+COUNT-3; ONLY the narrated STEP-SET (GAP-E) kills it — "
      "tower-stop does NOT bound sizes")

# --- 4. LEVEL-5 MINIMALITY IS PARITY-FREE ------------------------------------------
first_over_8 = next(n for n in range(1, 20) if lucas(n) > 8)
check("LEVEL5_MINIMAL_ALL_PARITIES", first_over_8 == 5,
      f"L_n for n=1..5: {[lucas(n) for n in range(1,6)]}; first >8 at n={first_over_8} "
      "(L_2=3, L_4=7 also <=8: odd-restriction not load-bearing for minimality)")

# --- 5. NEGATIVE CONTROLS ----------------------------------------------------------
fake_omega8 = 10
fV9 = fake_omega8 + 1
fake_triple = (fV9, fV9 + card_dyad, fV9 + card_role)
check("NC_MUTATED_OMEGA8_FAILS_CONCLUSION", fake_triple != (9, 11, 13),
      f"|Omega8|->10 gives {fake_triple}: the chain CAN fail if the owned count were wrong")

wide = [n for n in range(0, 15) if 9 <= lucas(n) <= 29]
check("NC_OLD_ROUTE_NEEDS_WINDOW", wide == [5, 6, 7],
      f"window widened to [9,29] admits Lucas levels {wide} — old-route uniqueness breaks, and the "
      "EVEN level 6 (L_6=18) is admitted too: the old Lean statement quantifies over ALL n, so the "
      "odd-parity leg was decorative there — the window carried even the parity's load; "
      "new route consumes no window, unaffected")

check("NC_PARITY_ADMITS_PLUS4", parity((9, 13, 17)),
      "+4 ladder passes PARITY — evenness, not '+2', is what det_T_pow owns")

print()
if FAILS:
    print("FAIL", FAILS)
    sys.exit(1)
print("ALL PASS (draft check; owns no registry claim)")
sys.exit(0)
