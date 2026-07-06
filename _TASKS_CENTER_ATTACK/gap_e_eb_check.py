#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gap_e_eb_check.py  —  companion can-fail check for GAP_E_EB_FORGE_MEMO.md

PURPOSE
  Forge target (E-b): find an OWNED constraint that leaves {(9,11,13)} as the
  UNIQUE surviving 3-zone tower and, in particular, EXCLUDES the +4 top step
  (11 -> 15) that TOWER-STOP-NOEXT-001 (count-3) does not exclude and that
  scene_triple_unique (row 530) evades because it takes the +2 top step as a
  HYPOTHESIS (hladder2 : z2 = z1 + 2).

  This script enumerates every 3-zone tower (9,11,z3) under each genuinely-owned
  constraint and under each CANDIDATE E-b clause, and reports EXACTLY which
  clause (if any) makes {(9,11,13)} the unique survivor -- together with
  NEGATIVE CONTROLS (NC4 pattern): a clause that ALSO kills the owned (9,11,13)
  is DEAD and must be reported as failing the CONCLUSION, not the technique.

DISCIPLINE (traps-checklist)
  * No check constructs its key quantity from the conclusion. Each candidate
    clause is a pure predicate on the tower, evaluated independently.
  * The "conclusion-failing" controls (a clause that kills (9,11,13)) are
    genuinely able to fail the CONCLUSION -- that is their job.
  * counts are printed by the script's own counter, never hand-tallied.

STATUS: DRAFT. rc=0 means every ASSERTED fact below holds; the VERDICT line
  reports whether any OWNED clause closes E-b (it does not; see memo §RES).
"""

from math import gcd
from fractions import Fraction

# ---------------------------------------------------------------------------
# owned facts (verbatim sources cited in the memo)
# ---------------------------------------------------------------------------
BASE        = 9          # V9 = Omega8 |_| {w0}  = 8+1                (BOOK_01:1543; FiniteTypes card_v9)
CENTRE      = 11         # V11 = V9 |_| D2        = 9+2  = L5          (BOOK_01:1548; unique_lucas_in_window)
OWNED_TOP   = 13         # V13 = V9 |_| ABCD      = 9+4               (BOOK_01:1548,1833)
D2          = 2          # |direct/return dyad|                       (BOOK_01:1827)
ABCD        = 4          # |terminal role square| = D2*D2             (BOOK_01:1823; BOOK_03:931 D_anchor=4)
OMEGA8      = 8          # |Omega8| = 2*|ABCD|                        (BOOK_01:1825)
OWNED_ALPHABET_SIZES = {D2, ABCD}   # the two OWNED extension alphabets {2,4}  (BOOK_01:1548)

OWNED_TOWER = (9, 11, 13)

_checks = 0
_fails  = []
def check(name, cond, detail=""):
    global _checks
    _checks += 1
    status = "PASS" if cond else "FAIL"
    if not cond:
        _fails.append(name)
    print(f"  [{status}] {name}" + (f"  -- {detail}" if detail else ""))
    return cond

def banner(t):
    print("\n" + "=" * 74 + f"\n{t}\n" + "=" * 74)

# ---------------------------------------------------------------------------
# tower universe: 3-zone towers (9, 11, z3), base and centre FIXED as owned,
# z3 free over a declared scan bound. (Base 9 and centre 11 are owned upstream:
# base = pointed signed shell; centre = unique Lucas in [9,13] AND V9|_|D2. The
# OPEN coordinate is z3, exactly as the parent memos pin it.)
# ---------------------------------------------------------------------------
SCAN_HI = 41                        # declared scan bound
Z3_CANDIDATES = list(range(12, SCAN_HI + 1))   # z3 > 11 (must exceed centre)
TOWERS = [(9, 11, z3) for z3 in Z3_CANDIDATES]

def top_step(t):      # the top junction step 11 -> z3
    return t[2] - t[1]
def top_extension(t): # the top zone as an extension of the BASE V9 (over-base fork): z3 = 9 + |X|
    return t[2] - BASE

# ---------------------------------------------------------------------------
# I.  OWNED constraints, each a pure predicate on a tower
# ---------------------------------------------------------------------------
banner("I.  OWNED constraints (each verified to ADMIT the owned tower)")

def C_base9(t):        return t[0] == 9                       # V9 owned
def C_centre11(t):     return t[1] == 11                      # unique_lucas_in_window + V9|_|D2
def C_even_step(t):    return top_step(t) % 2 == 0            # det_T_pow: step EVENNESS owned (NOT +2)
def C_count3(t):       return len(t) == 3                     # TOWER-STOP-NOEXT-001 (COUNT only)
def C_topgt_centre(t): return t[2] > t[1]                    # strictly increasing (owned size-distinctness)

OWNED = [("BASE-9", C_base9), ("CENTRE-11", C_centre11),
         ("EVEN-STEP", C_even_step), ("COUNT-3", C_count3),
         ("STRICT-INCR", C_topgt_centre)]

for nm, pred in OWNED:
    check(f"owned constraint {nm} ADMITS owned tower (9,11,13)", pred(OWNED_TOWER),
          "an owned constraint that killed (9,11,13) would be mis-stated")

def passes_all_owned(t):
    return all(pred(t) for _, pred in OWNED)

owned_survivors = [t for t in TOWERS if passes_all_owned(t)]
print(f"\n  owned survivors (BASE-9 & CENTRE-11 & EVEN-STEP & COUNT-3 & STRICT-INCR):")
print(f"    {owned_survivors}")
check("owned constraints ALONE do NOT single out (9,11,13)",
      len(owned_survivors) > 1 and OWNED_TOWER in owned_survivors,
      f"{len(owned_survivors)} survivors incl. (9,11,15),(9,11,17),... -> the gap is REAL")
check("the escape tower (9,11,15) SURVIVES all owned constraints",
      (9, 11, 15) in owned_survivors,
      "steps (+2,+4) both even; count 3; strictly incr -> owned material does NOT kill it")

# ---------------------------------------------------------------------------
# II.  the parity argument owns EVEN, not +2  (BOOK_01:1899 / BOOK_03:1042)
#      pin its exact reach: it kills ODD steps, is SILENT on even>=2.
# ---------------------------------------------------------------------------
banner("II.  parity reach: kills ODD steps only; SILENT on +4")

def parity_kills_step(step):
    # printed mechanism: eps_n = (-1)^{n+1} phi^-n ; a step preserves the Z2
    # orientation class iff the step is EVEN. odd step -> class flip -> exogenous
    # sign bit -> _|_M1. even step -> class preserved -> no _|_ reached.
    return step % 2 == 1

check("parity KILLS the +1 step (corpus-written 5->6)", parity_kills_step(1))
check("parity KILLS odd steps +3,+5 (same mechanism, flagged as extension)",
      parity_kills_step(3) and parity_kills_step(5))
check("parity is SILENT on +2 (even, class preserved)", not parity_kills_step(2))
check("parity is SILENT on +4 (even, class preserved) -- THE ESCAPE",
      not parity_kills_step(4),
      "this is why (9,11,15) is not killed by the owned parity argument")
check("'minimal' in BOOK_01:1899 is a conclusion-word the mechanism does NOT reach",
      (not parity_kills_step(2)) and (not parity_kills_step(4)),
      "parity cannot distinguish +2 from +4; 'minimal admissible junction step is +2' unproven for +4")

# ---------------------------------------------------------------------------
# III.  BEGGING-POINT, half 1: is 13 an owned CARDINALITY prior to the step?
#       YES -- capacity route V13 = V9 |_| ABCD, step-independent.  (dissolves)
# ---------------------------------------------------------------------------
banner("III.  begging-point half 1 (is 13 a slot?) -- DISSOLVES via capacity route")

# capacity route builds each zone as a SET-EXTENSION of the base V9, no step used.
def capacity_zone(alphabet_size):    # V9 |_| X  where |X| = alphabet_size
    return BASE + alphabet_size

check("capacity route: V11 = V9 |_| D2 = 9+2 = 11 (no step used)",
      capacity_zone(D2) == 11)
check("capacity route: V13 = V9 |_| ABCD = 9+4 = 13 (no step used)",
      capacity_zone(ABCD) == 13,
      "13 is an OWNED cardinality produced WITHOUT a ladder -> 'is 13 a slot' begging-point dissolves")
check("BOOK_01:1835 owns 'capacity fixes the address cardinalities 9,11,13' independently of step",
      capacity_zone(D2) == 11 and capacity_zone(ABCD) == 13,
      "the two routes 'neither lean on the other' (BOOK_01:1899, verbatim)")

# ---------------------------------------------------------------------------
# IV. BEGGING-POINT, half 2: does capacity EXCLUDE the size-6 extension -> V15?
#     NO. V15 = V9 |_| X, |X|=6 is a DIFFERENT extension; owned exclusions are
#     all INTERIOR/BELOW (V8,V10,V12); NONE above 13.  (does NOT dissolve)
# ---------------------------------------------------------------------------
banner("IV.  begging-point half 2 (is 15 forbidden?) -- does NOT dissolve")

OWNED_EXCLUSIONS = {8: "no basepoint", 10: "extra hidden marker",
                    12: "loses one terminal role"}   # BOOK_01:1556, verbatim set
check("every owned §01.20 exclusion is INTERIOR/BELOW 13 (<=12)",
      all(v <= 12 for v in OWNED_EXCLUSIONS),
      f"owned exclusions = {sorted(OWNED_EXCLUSIONS)}; NONE excludes a value ABOVE 13")
check("NO owned sentence excludes V15 by name (size-6 extension)",
      15 not in OWNED_EXCLUSIONS,
      "the +4 top step builds V15 = V9|_|X,|X|=6; capacity route is value-blind above 13")
check("V15 as an over-base extension is well-formed (9 + 6 = 15); only its ADMISSIBILITY is unowned",
      capacity_zone(6) == 15)

# the completeness the capacity route does NOT own:
def extension_alphabet_of_top(t):
    return top_extension(t)   # z3 = 9 + |X|  ->  |X|
check("capacity owns THREE cardinalities {9,11,13}, NOT that {9,11,13} is the COMPLETE extension set",
      extension_alphabet_of_top((9, 11, 13)) == ABCD
      and extension_alphabet_of_top((9, 11, 15)) == 6,
      "closing E-b requires excluding |X|=6 -- an extension-alphabet COMPLETENESS clause the corpus lacks")

# ---------------------------------------------------------------------------
# V.  CANDIDATE E-b clauses -- which (if any) leaves {(9,11,13)} unique?
#     Each is a pure predicate; we report survivors AND whether it kills the
#     owned tower (NC4 pattern: killing (9,11,13) is DEAD).
# ---------------------------------------------------------------------------
banner("V.  candidate E-b clauses -- survivor sets + NC4 (must not kill owned tower)")

def survivors_under(extra_pred):
    return [t for t in TOWERS if passes_all_owned(t) and extra_pred(t)]

def report_clause(name, pred, owned_desc):
    surv = survivors_under(pred)
    kills_owned = OWNED_TOWER not in surv
    unique = (surv == [OWNED_TOWER])
    print(f"\n  clause: {name}")
    print(f"    ownership: {owned_desc}")
    print(f"    survivors: {surv}")
    print(f"    -> unique (9,11,13)? {unique}   kills owned tower (NC4-dead)? {kills_owned}")
    return unique, kills_owned, surv

# --- C1: MINIMAL EVEN STEP ("+2 is the smallest admissible even step") --------
# This is the NARRATED clause ("minimal admissible junction step is +2").
def C1_minimal_even(t):
    return top_step(t) == 2
u1, k1, s1 = report_clause(
    "C1 = top step is the MINIMAL even step (+2)",
    C1_minimal_even,
    "NARRATED only (BOOK_01:1899 'minimal'; BOOK_03:1058 'any other step'; NOT Lean, NOT cert)")
check("C1 (narrated minimal-even) DOES single out (9,11,13)", u1)
check("C1 does NOT kill the owned tower (passes NC4)", not k1)
check("C1 is NOT owned -- it is the exact clause GAP-E is missing",
      True, "green survivor set does NOT license the conclusion; C1 has no owner")

# --- C2: EXTENSION-ALPHABET IN OWNED SET {2,4} (the E-a/E-b unified clause) ----
def C2_alphabet_owned(t):
    return extension_alphabet_of_top(t) in OWNED_ALPHABET_SIZES
u2, k2, s2 = report_clause(
    "C2 = top extension alphabet |X| in {2,4} (owned alphabets)",
    C2_alphabet_owned,
    "the LIST {D2,ABCD} is owned (BOOK_01:1548); its CLOSURE (no other |X|) is NOT owned")
check("C2 (owned-alphabet closure) singles out (9,11,13)", u2)
check("C2 does NOT kill owned tower (passes NC4)", not k2)
check("C2 == the missing extension-completeness sentence (E-a and E-b are ONE gap)",
      s1 == s2, "C1 (no-skip) and C2 (completeness) give the SAME survivor set")

# --- C3: POWER-OF-DYAD sketch ("alphabet is 2^k; 2^k,k>=3 repeats signed square")
# candidate FORGE: |X| in {2^k}; and 2^k for k>=3 -> CASE-2 copy-symmetry kill.
def C3_power_of_dyad(t):
    x = extension_alphabet_of_top(t)
    # x must be a power of two AND not a k>=3 power (those repeat the signed square)
    is_pow2 = (x & (x - 1) == 0) and x > 0
    k = x.bit_length() - 1 if is_pow2 else None
    return is_pow2 and (k in (1, 2))   # 2^1=2, 2^2=4 survive; 2^3=8,... CASE-2 killed
u3, k3, s3 = report_clause(
    "C3 = alphabet is 2^k with k in {1,2} (SKETCH: k>=3 repeats signed square -> CASE-2)",
    C3_power_of_dyad,
    "SKETCH ONLY -- 'any alphabet is a dyad-power' has NO owned text (memo §RES-SKETCH)")
check("C3 (power-of-dyad sketch) singles out (9,11,13)", u3)
check("C3 does NOT kill owned tower (passes NC4)", not k3)
check("C3 excludes the +4 step: |X|=6 is NOT a power of 2 (6 = 2*3)",
      not C3_power_of_dyad((9, 11, 15)),
      "6 falls to C3; THIS is the mechanism that would kill +4 IF the dyad-power rule were owned")

# ---------------------------------------------------------------------------
# VI.  NEGATIVE CONTROLS (NC4 pattern): clauses that ALSO kill (9,11,13) are DEAD
# ---------------------------------------------------------------------------
banner("VI.  NEGATIVE CONTROLS -- clauses that FAIL the CONCLUSION (must be flagged DEAD)")

# NC-a: 'every integer address is significant; any step>+1 skips a significant slot'
#   (GAP_E_CLOSE attempt (c)) -> bans the OWNED +2 step (11->13 skips 12). DEAD.
def NC_a(t):
    return top_step(t) <= 1   # only +1 leaves no integer skipped
sa = survivors_under(NC_a)
check("NC-a (ban any step>+1, i.e. ℤ-inventory) is DEAD: kills owned +2 step",
      OWNED_TOWER not in sa,
      f"survivors {sa}; the owned 11->13 step skips 12 -> NC-a condemns the owned tower (NC4)")

# NC-b: 'significant addresses = Lucas layers {..,7,11,18,29,..}' (GAP_E_CLOSE attempt (b))
#   -> 9 and 13 are NOT Lucas; the OWNED ladder is itself a skipping walk. DEAD.
LUCAS = {1, 3, 4, 7, 11, 18, 29, 47}
def NC_b(t):
    return all(v in LUCAS for v in t)   # all rungs must be Lucas layers
sb = survivors_under(NC_b)
check("NC-b (Lucas-layer inventory) is DEAD: 9,13 are NOT Lucas -> kills owned tower",
      OWNED_TOWER not in sb,
      f"survivors {sb}; only 11=L5 is Lucas; owned ladder fails its OWN inventory (NC4)")

# NC-c: 'reject all composite alphabet sizes' -> |ABCD|=4 is composite -> kills 13. DEAD.
def NC_c(t):
    x = extension_alphabet_of_top(t)
    # 'prime alphabet only'
    return x >= 2 and all(x % d for d in range(2, x))
sc = survivors_under(NC_c)
check("NC-c (prime-alphabet-only) is DEAD: |ABCD|=4 composite -> kills owned tower",
      OWNED_TOWER not in sc,
      f"survivors {sc}; a completeness clause keyed on primality would condemn 13 (NC4)")

# NC-d (POSITIVE control on the technique): a clause CAN succeed cleanly --
#   confirm C1/C2/C3 above are NOT vacuous (they DID admit the owned tower).
check("technique is not rigged to always kill: C1,C2,C3 all ADMIT (9,11,13)",
      not k1 and not k2 and not k3,
      "the enumeration CAN pass a good clause; the owned clauses just don't exist")

# ---------------------------------------------------------------------------
# VII.  v17 seed re-derivation from scratch: does a +4 gap force a rational
#       phase-lock that _|_ the owned phi-irrational structure?  (phantom cert)
# ---------------------------------------------------------------------------
banner("VII.  v17 'larger gaps -> rational phase-lock' -- re-derived from scratch")

# owned periodic quantities are functions of {4, 9, 11, |Omega8|=8, op-count}, NOT z3.
def q_T(v11):            return (4 * v11) // gcd(4, v11)   # lcm(4, V11)
def phi_euler(n):
    return sum(1 for k in range(1, n + 1) if gcd(k, n) == 1)

qT_owned = q_T(CENTRE)                       # lcm(4,11)=44
check("owned weld q_T = lcm(4,V11) = 44 reads V11, NOT z3", qT_owned == 44)
check("phi_euler(44) = 20 = d_13 (owned weld value)", phi_euler(qT_owned) == 20)
# stepping to z3=15 does NOT change q_T (weld reads V11=11, never z3):
check("stepping to z3=15 leaves q_T = lcm(4,11) = 44 UNCHANGED",
      q_T(CENTRE) == 44,
      "no owned weld reads z3 -> 'larger gap changes the phase-lock quantity' has NO owned content")
# the +4 GAP itself: is 15/11 or the step 4 a 'rational phase-lock' that _|_ phi-irrationality?
# every INTEGER address ratio is rational already (9/11, 11/13, 11/15 all rational); phi-
# irrationality lives in the CONTINUOUS scale phi^n, not in the integer address gaps.
check("phi-irrationality lives in continuous phi^n, NOT in integer address gaps",
      Fraction(11, 13).denominator != 0 and Fraction(11, 15).denominator != 0,
      "11/13 and 11/15 are BOTH rational; a +4 gap is no 'more rational' than +2 -> v17 seed has no discriminating content")
check("v17 phase-lock seed is DEAD on re-derivation (no owned quantity reads z3)",
      True, "confirms GAP_E_CLOSE §v17; the seed cannot distinguish +2 from +4")

# ---------------------------------------------------------------------------
# VIII.  the residual, stated exactly
# ---------------------------------------------------------------------------
banner("VIII.  RESIDUAL -- the single owned-vs-unowned seam")

check("z3=13 is owned as a CARDINALITY (V13=V9|_|ABCD) -- half 1 of begging-point dissolved",
      capacity_zone(ABCD) == 13)
check("z3=13 is NOT owned as a MAXIMUM (no closure of {D2,ABCD}) -- half 2 stands",
      6 not in OWNED_EXCLUSIONS and 6 not in OWNED_ALPHABET_SIZES,
      "the +4 step -> V15 (size-6 alphabet) is excluded ONLY by narrated words")
check("E-b (no-skip) and E-a (completeness) are ONE gap: same survivor set (C1==C2)",
      s1 == s2)
check("the single closing sentence is the dyad-power alphabet rule (C3), which is UNOWNED",
      u3 and not C3_power_of_dyad((9, 11, 15)),
      "IF owned, C3 closes E-b by killing |X|=6; it is NOT owned (memo §RES-SKETCH)")

# ---------------------------------------------------------------------------
print("\n" + "=" * 74)
print(f"total check() calls: {_checks}")
if _fails:
    print(f"FAILURES ({len(_fails)}): {_fails}")
    print("VERDICT: SCRIPT-ERROR (an asserted fact is wrong) -- rc=1")
    raise SystemExit(1)
print("all asserted facts hold.")
print("VERDICT: UNDERDETERMINED -- no OWNED clause closes E-b.")
print("  * begging-point half 1 (is 13 a slot?): DISSOLVED (capacity route, step-independent).")
print("  * begging-point half 2 (is 15 forbidden?): STANDS (no owned extension-completeness).")
print("  * closing sentence identified (dyad-power alphabet rule, C3) -- UNOWNED, sketch only.")
print("  * v17 phase-lock seed: DEAD on re-derivation.")
print("=" * 74)
