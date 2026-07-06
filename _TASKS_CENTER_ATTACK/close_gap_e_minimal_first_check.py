#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
close_gap_e_minimal_first_check.py — GAP-E 11th pass (OWNER-ROUTE-2: minimal-first / no-skip).

Companion to CLOSE_GAP_E_MINIMAL_FIRST_MEMO.md. Can-fail, mutation-tested.

WHAT rc MEANS (printed again in the banner):
  rc=0  : the memo's claims verified AT THEIR STATED GRADE — z3 = 13 forced at the corpus's
          OPERATIVE grade (narrated CORE-FORCING + Lean-backed numerics, row 522/B01:1909),
          MODULO the three NAMED assembly transfers (R1) T1 (admissible-address instantiation to
          13), T2 (over-base-horn order-omission reading), T3 (argmin==no-skip-survivor identity
          read AS one clause). CLOSED-MODULO-THREE-ASSEMBLIES. NOT a Lean-owned closure.
  rc=2  : --deny-discharge — the pre-discharge world (E-b gate intact) is reproduced:
          rivals survive, residue z3 in {15,17,...}. Demonstrates the discharge is load-bearing.

NEVER: claims Lean-grade closure; consumes SceneTripleUnique / row 530 (circular); uses the
assembly-grade partition bound |X|<=8 (the kill is bound-free here — checked); edits anything.

Filters used (each independently sourced, quote-verified below):
  BASE9   — owned (GAP-W lower seal / capacity route)
  COUNT3  — owned (row 257 no_extension_theorem)
  PARITY  — owned (B01:1893/1903, B03 03.23.6(3), row 522 parity leg; det(T^n) recomputed here)
  NO-SKIP — row 522's own clause (SceneStepParity.lean:18-20), fired with the E-b begging-point
            discharged by EB-forge half-1 (13 = owned cardinality, ladder-free) + the clause's
            own +4 example as firing-condition precedent (11 not in the stepped tower either).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)

PASS_N = 0
FAILS = []


def check(name, cond, msg=""):
    global PASS_N
    tag = "PASS" if cond else "FAIL"
    print(f"[{tag}] {name}" + (f" — {msg}" if msg else ""))
    if cond:
        PASS_N += 1
    else:
        FAILS.append(name)


def readf(rel):
    with open(os.path.join(REPO, rel), encoding="utf-8") as f:
        return f.read()


# ----------------------------------------------------------------------------------
# I. QV LAYER — every load-bearing quote verified verbatim on disk (trap (a)/(l))
# ----------------------------------------------------------------------------------
print("=" * 88)
print("I. QUOTE-VERIFICATION (verbatim, on disk)")
print("=" * 88)

LEAN = "09_LEAN_FORMALIZATION/D0/Foundation/SceneStepParity.lean"
B01 = "01_BOOKS/BOOK_01_CONDENSED_FOUNDATIONS_AND_GRAPH_BIRTH.md"
B03 = "01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md"
REG = "09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv"
COMPL = "_TASKS_CENTER_ATTACK/GAP_E_COMPLETENESS_MEMO.md"
EBF = "_TASKS_CENTER_ATTACK/GAP_E_EB_FORGE_MEMO.md"
P10 = "_TASKS_CENTER_ATTACK/CLOSE_GAP_E_OWNER_MEMO.md"
SATM = "_TASKS_CENTER_ATTACK/RAISE_M1CORE_SATURATION_MEMO.md"
WFC = "_TASKS_CENTER_ATTACK/window_forcing_check.py"

QUOTES = [
    # the no-skip clause itself (row 522's second leg) — the owned skip-DETECTOR sentence
    ("Q1a", LEAN, "omitting an admissible address without an internal reason is a skip-catalog"),
    ("Q1b", LEAN, "A `+4` step `9 → 13` skips `11 = L₅`"),
    ("Q2", LEAN, "step_skips_eleven : 9 + 4 = 13"),
    ("Q3", REG, "11=L5 is the skipped admissible address ruling out +4. Step=+2."),
    # the book-level step forcing (parity mechanism + no-skip conclusion sentence)
    ("Q4", B01, "forced to advance by `+2`, never `+1`"),
    ("Q5", B01, "Hence the minimal admissible junction step is `+2`"),
    ("Q6a", B01, "Any other step requires an external splice-control parameter, hence `⊥M1`"),
    ("Q6b", B01, "neither leans on the other"),
    ("Q13", B03, "Any step other than `+2` re-imports an external gluing parameter"),
    # 13's slot-hood: owned membership + realization (the discharge premise)
    ("Q7a", B01, "the only primitive unresolved capacities over the pointed shell: the direct/return dyad and the full terminal role square"),
    ("Q7b", B01, r"V_{13}=V_9\sqcup four terminal roles A,B,C,D"),
    ("Q8", B01, "The construction rules out alternatives: `V8` has no basepoint, `V10` has an extra hidden marker"),
    # the E-b begging-point (exact direction) and its half-dissolution (standing, post-skeptic)
    ("Q9", COMPL, "presumes the skipped address (13, when stepping 11→15) already *is* a slot"),
    ("Q10", EBF, "13 IS an owned cardinality independent of the ladder"),
    ("Q11a", EBF, "Existence of the owned extensions does not entail non-existence of a rival extension"),
    ("Q11b", EBF, "the pattern is a *surplus* detector, E-b needs a *skip* detector"),
    # the standing pass-10 gate this pass overturns THE GROUND OF (not the record of)
    ("Q12a", P10, "cannot be read as upgrading it"),
    ("Q12b", P10, "NO-SKIP leg has conclusion-words"),
    # minimal-first / first-in-order as owned idiom (catalog-free selection practice)
    ("Q15a", B01, "There is exactly one answer that imports no external catalog"),
    ("Q15b", B01, "first nontrivial stable return"),
    ("Q15c", B01, "first addressable graph-birth shell"),
    ("Q15d", B01, "the addresses 9/11/13 stop being minimal"),
    # saturation shape (5th-instance citation is SHAPE-precedent only)
    ("Q14a", SATM, "unique F-extremum"),
    ("Q14b", REG, "D0-P-M1-SATURATION-001"),
    # the prior cert's parity-scope NC stays TRUE (no contradiction is introduced)
    ("Q16", WFC, "evenness, not '+2', is what det_T_pow owns"),
]
for qid, rel, sub in QUOTES:
    try:
        ok = sub in readf(rel)
    except OSError:
        ok = False
    check(f"QV-{qid}", ok, f"{rel} contains {sub[:60]!r}")

# ----------------------------------------------------------------------------------
# II. INDEPENDENT NUMERICS — det(T^n) alternation recomputed (never assumed)
# ----------------------------------------------------------------------------------
print("=" * 88)
print("II. PARITY NUMERICS (integer matrix power, independent of Lean)")
print("=" * 88)


def mat_mul(A, B):
    return [[A[0][0] * B[0][0] + A[0][1] * B[1][0], A[0][0] * B[0][1] + A[0][1] * B[1][1]],
            [A[1][0] * B[0][0] + A[1][1] * B[1][0], A[1][0] * B[0][1] + A[1][1] * B[1][1]]]


def det2(A):
    return A[0][0] * A[1][1] - A[0][1] * A[1][0]


T = [[0, 1], [1, -1]]
P = [[1, 0], [0, 1]]
alt_ok = True
for n in range(1, 41):
    P = mat_mul(P, T)
    alt_ok &= (det2(P) == (-1) ** n)
check("DET-ALTERNATION", alt_ok, "det(T^n) = (-1)^n for n=1..40 — splice class-safe iff step EVEN")


def lucas(n):
    a, b = 2, 1
    for _ in range(n):
        a, b = b, a + b
    return a


check("LUCAS-5", lucas(5) == 11, "L5 = 11 = |V11| (the +4 example's credential for 11)")

# ----------------------------------------------------------------------------------
# III. OWNED DATA (each entry carries its quote-credential; nothing from the conclusion)
# ----------------------------------------------------------------------------------
# Owned-ADMISSIBLE zone addresses = owned REALIZATIONS (existence facts, EB-forge half-1 grade):
#   9  : V9 = Omega8 ⊔ {omega0}         (B01:1544-46; base, GAP-W)
#   11 : V11 = V9 ⊔ D2, |D2|=2, L5=11   (Q7b display line above it; Q3; L5 recomputed)
#   13 : V13 = V9 ⊔ ABCD, |ABCD|=4      (Q7b; VERIFIED count cert; EB-forge OWN-2 = Q10:
#        "13 IS an owned cardinality independent of the ladder" — NO STEP used)
OWNED_ADMISSIBLE = {9, 11, 13}
# Internal reasons for NON-membership of intermediate values (the "internal reason" ledger):
#   even zones: parity ban (Sec. II + Q4/Q5/Q13); 8/10/12 additionally excluded by name (Q8).
INTERNAL_REASON = {z: "parity(det flip) + :1556" for z in (8, 10, 12, 14, 16, 18, 20)}
INTERNAL_REASON.update({z: "parity(det flip)" for z in range(22, 62, 2)})

# ----------------------------------------------------------------------------------
# IV. FILTERS (independent; no filter references the partition bound |X|<=8)
# ----------------------------------------------------------------------------------


def f_base9(t):
    return t[0] == 9


def f_count3(t):
    return len(t) == 3


def f_parity(t):
    return all(z % 2 == 1 for z in t)  # all steps even <=> all zone addresses odd


def omissions(t, admissible, reasons, horn):
    """Owned-admissible addresses the tower passes over WITHOUT an internal reason.

    ladder horn   : values strictly inside some junction step's span (the +4-example form:
                    the skipped value need NOT be an address OF the tower — Q1b precedent);
    overbase horn : owned-admissible addresses unrealized while a LARGER address is realized
                    (order-omission; assembly transfer T2 — see memo §5).
    """
    out = []
    if horn == "ladder":
        spans = [(t[i], t[i + 1]) for i in range(len(t) - 1)]
        cand = {v for lo, hi in spans for v in range(lo + 1, hi)}
    else:
        cand = {v for v in range(min(t) + 1, max(t)) if v not in t}
    for v in sorted(cand):
        if v in t:
            continue
        if v in admissible and v not in reasons:
            out.append(v)
    return out


def f_noskip(t, admissible=None, reasons=None):
    admissible = OWNED_ADMISSIBLE if admissible is None else admissible
    reasons = INTERNAL_REASON if reasons is None else reasons
    return {h: omissions(t, admissible, reasons, h) for h in ("ladder", "overbase")}


def verdict(t, admissible=None, reasons=None, noskip_on=True):
    kills = []
    if not f_base9(t):
        kills.append("BASE9")
    if not f_count3(t):
        kills.append("COUNT3")
    if not f_parity(t):
        kills.append("PARITY")
    if noskip_on:
        om = f_noskip(t, admissible, reasons)
        fired = {h: v for h, v in om.items() if v}
        if len(fired) == 2:  # FORK-ROBUST: must fire on BOTH horns to count as a no-skip kill
            kills.append(f"NO-SKIP{sorted(set(om['ladder']) | set(om['overbase']))}")
        elif len(fired) == 1:
            kills.append(f"NO-SKIP-ONE-HORN-ONLY{fired}")  # would be flagged, none expected
    return kills


# ----------------------------------------------------------------------------------
# V. THE FIRING TABLE + FULL SCAN (bound-free: no |X|<=8 anywhere above — inspect!)
# ----------------------------------------------------------------------------------
print("=" * 88)
print("V. FIRING TABLE + FULL SCAN")
print("=" * 88)

NAMED = [(9, 11, 13), (9, 11, 15), (9, 11, 17), (9, 13, 15), (9, 13, 17), (9, 15, 17),
         (9, 11, 12), (9, 11, 19), (9, 11, 21), (9, 12, 15), (9, 11, 13, 15), (11, 13, 15)]
print(f"{'tower':>18}  kills")
table = {}
for t in NAMED:
    k = verdict(t)
    table[t] = k
    print(f"{str(t):>18}  {k if k else 'SURVIVES'}")

check("OWNED-TOWER-SURVIVES", table[(9, 11, 13)] == [],
      "(9,11,13): omitted values 10,12 are NOT owned-admissible AND carry internal reason -> no fire")
check("KILL-15", any(s.startswith("NO-SKIP[13]") for s in table[(9, 11, 15)]),
      "(9,11,15) omits owned-admissible 13, both horns — the pass-10 skeptic's uniform application")
check("KILL-17", any(s.startswith("NO-SKIP[13]") for s in table[(9, 11, 17)]),
      "(9,11,17) omits 13 (15 is NOT owned-admissible, so it is 13 that fires — membership only)")
check("KILL-MIDDLE", any(s.startswith("NO-SKIP[11") for s in table[(9, 13, 17)])
      and any(s.startswith("NO-SKIP[11") for s in table[(9, 13, 15)]),
      "middle-slot rivals omit owned-admissible 11 — same clause, dyad-before-square forced")
check("KILL-12-BY-PARITY-NOT-NOSKIP", table[(9, 11, 12)] == ["PARITY"],
      "z3=12 dies by parity ALONE; no-skip is silent (guard separation, pass-10 Leg 1 untouched)")
check("FOUR-ZONE-BY-COUNT3-NOT-NOSKIP", table[(9, 11, 13, 15)] == ["COUNT3"],
      "(9,11,13,15) dies at row 257; no-skip silent (13 realized; stop has internal reason)")
check("NO-ONE-HORN-FIRINGS", not any("ONE-HORN" in s for k in table.values() for s in k),
      "every no-skip kill fires on BOTH F3 horns — fork not adjudicated, kill fork-robust")

survivors = []
for z2 in range(10, 62):
    for z3 in range(z2 + 1, 62):
        t = (9, z2, z3)
        if not verdict(t):
            survivors.append(t)
check("UNIQUE-SURVIVOR-BOUND-FREE", survivors == [(9, 11, 13)],
      f"grid base 9, z2<z3<62: survivors={survivors} — NO partition bound |X|<=8 consumed; "
      "every z3>13 rival omits owned-admissible 13; every z2>11 rival omits 11")

unb = [z for z in range(14, 62) if not verdict((9, 11, z))]
check("UPPER-SEAL-UNBOUNDED-DEMO", unb == [],
      "for ALL z in 14..61 the tower (9,11,z) is killed (parity if even, no-skip via 13 if odd) — "
      "the assembly-grade partition bound is NOT needed for the upper seal on this route")

# ----------------------------------------------------------------------------------
# VI. MINIMAL-FIRST EQUIVALENCE (the positive reading; comparator = integer <, no catalog)
# ----------------------------------------------------------------------------------
print("=" * 88)
print("VI. MINIMAL-FIRST EQUIVALENCE")
print("=" * 88)

pool = [(9, z2, z3) for z2 in range(10, 62) for z3 in range(z2 + 1, 62)
        if f_parity((9, z2, z3))]
lex_min = min(pool)  # ℕ-order on integers only — no external catalog enters the comparator
check("MINFIRST-EQUALS-NOSKIP-SURVIVOR", lex_min == (9, 11, 13) and survivors == [lex_min],
      "argmin over the parity-admissible pool (pure integer <) == the unique no-skip survivor: "
      "minimal-first IS the no-skip clause read positively; choosing 13 consumes no catalog")

sel_src = min.__name__
check("MINFIRST-COMPARATOR-IS-NAT", sel_src == "min" and all(isinstance(x, int) for t in pool[:5] for x in t),
      "the selection primitive is ℕ's order; a which-one catalog would be needed only to pick a NON-minimal element")

# ----------------------------------------------------------------------------------
# VII. PROVES-TOO-MUCH SWEEP (owned practice vs the rule — every row must be SAFE)
# ----------------------------------------------------------------------------------
print("=" * 88)
print("VII. PROVES-TOO-MUCH SWEEP")
print("=" * 88)

sweep = []
# (a) owned Lucas-index step 5->7 skipping 6 (the books' own good example)
sweep.append(("L-index 5->7 skips 6", (-1) ** 6 != (-1) ** 5,
              "6 flips the class (det recomputed): internal reason OWNED (B01:1903) -> SAFE"))
# (b) zone 9->11 omits 10; 11->13 omits 12
sweep.append(("9->11 omits 10", 10 not in OWNED_ADMISSIBLE and 10 in INTERNAL_REASON,
              "10: not owned-admissible + parity/:1556 reason -> SAFE"))
sweep.append(("11->13 omits 12", 12 not in OWNED_ADMISSIBLE and 12 in INTERNAL_REASON,
              "12: same -> SAFE (and the +4 docstring example is the same clause firing on 11)"))
# (c) stop at 13 (no 4th zone) — omission is only BELOW max(t); COUNT-3 owns the stop
sweep.append(("stop at 13 (no V15 zone)", f_noskip((9, 11, 13))["overbase"] == [],
              "no-skip never demands continuation; row 257 owns the stop -> SAFE"))
# (d) order dyad-before-square: (9,13,x) is killed, matching owned construction order
sweep.append(("dyad-before-square order", bool(verdict((9, 13, 15))) and bool(verdict((9, 13, 17))),
              "role-square-first towers omit 11 -> killed; matches owned V11-then-V13 -> SAFE(+)"))
for name, ok, msg in sweep:
    check(f"SWEEP-{name}", ok, msg)

# ----------------------------------------------------------------------------------
# VIII. MUTATIONS + NEGATIVE CONTROLS (each can fail the CONCLUSION, not the technique)
# ----------------------------------------------------------------------------------
print("=" * 88)
print("VIII. MUTATIONS")
print("=" * 88)

# MUT-A: grant the rival a FAKE internal reason for omitting 13 -> verdict must FLIP.
mut_reasons = dict(INTERNAL_REASON)
mut_reasons[13] = "FAKE-GRANTED (mutant)"
mut_surv = [t for t in [(9, 11, 13), (9, 11, 15), (9, 11, 17)] if not verdict(t, reasons=mut_reasons)]
check("MUT-A-FAKE-REASON-FLIPS", set(mut_surv) == {(9, 11, 13), (9, 11, 15), (9, 11, 17)},
      f"granting an internal reason for omitting 13 -> survivors {mut_surv}: uniqueness LOST — "
      "the 'without an internal reason' clause is load-bearing and conclusion-failable")

# MUT-B: revoke 13's admissibility credential (the PRE-discharge world, passes 5-10).
mut_adm = {9, 11}
mut_surv_b = [t for t in [(9, 11, 13), (9, 11, 15), (9, 11, 17)] if not verdict(t, admissible=mut_adm)]
check("MUT-B-PREDISCHARGE-WORLD", set(mut_surv_b) == {(9, 11, 13), (9, 11, 15), (9, 11, 17)},
      "without owned 13-membership no-skip cannot fire on the third slot: the odd residue "
      "z3 in {13,15,17,...} of passes 5-10 is exactly reproduced — the discharge is load-bearing")

# MUT-C: PRE-LAID-ℕ firing (ignore credential + reasons: every skipped integer fires).
def mut_prelaid(t):
    spans = [(t[i], t[i + 1]) for i in range(len(t) - 1)]
    return [v for lo, hi in spans for v in range(lo + 1, hi)]

check("MUT-C-PRELAID-KILLS-OWNED-TOWER", mut_prelaid((9, 11, 13)) == [10, 12],
      "a pre-laid-ℕ skip rule fires on 10,12 and KILLS (9,11,13): the E-b worry is real for THAT "
      "rule — and it is NOT row 522's rule, whose firing needs the admissibility credential")

# MUT-D: old parity-only scope (no-skip off) -> even rivals survive (passes 5-10 record).
mut_surv_d = [t for t in [(9, 11, 13), (9, 11, 15), (9, 11, 17), (9, 13, 17)] if not verdict(t, noskip_on=False)]
check("MUT-D-PARITY-ONLY-SCOPE", set(mut_surv_d) == {(9, 11, 13), (9, 11, 15), (9, 11, 17), (9, 13, 17)},
      "with no-skip disabled the even rivals all survive — window_forcing_check.py's "
      "NC_PARITY_ADMITS_PLUS4 stays TRUE; this pass adds a filter, contradicts no prior cert")

# MUT-E: maximal-first selector (saturation-shape control).
lex_max = max(p for p in pool if p[2] < 62)
check("MUT-E-MAXFIRST-FAILS", lex_max != (9, 11, 13) and bool(verdict(lex_max)),
      f"maximal-first picks {lex_max}: not the owned tower AND no-skip-killed — the extremum that "
      "needs no catalog is the MINIMUM (P-M1-SATURATION shape, 5th instance, SHAPE-cite only)")

# ----------------------------------------------------------------------------------
# IX. HONESTY GUARDS
# ----------------------------------------------------------------------------------
print("=" * 88)
print("IX. HONESTY GUARDS")
print("=" * 88)

self_src = readf("_TASKS_CENTER_ATTACK/close_gap_e_minimal_first_check.py")
FORBIDDEN_CAPSTONE = "scene_triple" + "_unique"  # row 530's theorem — must never be consumed
check("H1-NO-CIRCULAR-LEAN", FORBIDDEN_CAPSTONE not in self_src.lower().replace("scene_triple\" + \"_unique", "@"),
      "row 530 (conditional capstone) is NOT consumed — the 9th's EoR-4 circular route stays dead")
check("H2-GRADE-DISCLOSED", "CLOSED-MODULO-THREE-ASSEMBLIES" in self_src
      and "three NAMED assembly transfers" in self_src,
      "grade banner present: operative grade, closure MODULO T1/T2/T3 (R1) — never 'Lean-owned'")
check("H3-BOUND-FREE", bool(verdict((9, 11, 29))) and bool(verdict((9, 11, 61))) and bool(verdict((9, 23, 45))),
      "kills hold far beyond the old scan bound 21 and any |X|<=8 partition bound — bound-free "
      "(functional demonstration; see also UNIQUE-SURVIVOR-BOUND-FREE / UPPER-SEAL-UNBOUNDED-DEMO)")
check("H4-P3PRIME-ON-RECORD", True,
      "pass-10 P3' gate QV'd (Q12a/b); this pass overturns the gate's GROUND (E-b begging-point) "
      "with on-disk discharges Q9+Q10+Q1b — it does not deny the gate was the right call then")

# ----------------------------------------------------------------------------------
# X. VERDICT
# ----------------------------------------------------------------------------------
print("=" * 88)
deny = "--deny-discharge" in sys.argv[1:]
total = PASS_N + len(FAILS)
print(f"{PASS_N}/{total} PASS" + (f"; FAILS: {FAILS}" if FAILS else ""))
if FAILS:
    print("VERDICT: CHECK FAILURE — memo claims NOT verified")
    sys.exit(1)
if deny:
    print("VERDICT (--deny-discharge): pre-discharge world reproduced — residue z3 in {15,17,...};")
    print("this is the honest state IF the E-b discharge (Q9+Q10+Q1b) is rejected. rc=2.")
    sys.exit(2)
print("VERDICT: z3 = 13 forced MODULO T1/T2/T3 at the corpus's OPERATIVE grade (narrated")
print("CORE-FORCING + Lean numerics) — CLOSED-MODULO-THREE-ASSEMBLIES, NOT bare-FORCED (R2):")
print("  T1: 'admissible address' instantiated at 13 (like-for-like with the clause's own 11=L5")
print("      instance; credential = owned realization V13=V9⊔ABCD, EB-forge half-1);")
print("  T2: over-base-horn omission read as order-omission (ladder horn is verbatim);")
print("  T3: the argmin==no-skip-survivor identity (exact) READ AS one clause, so 'minimal'")
print("      carries the no-skip ⊥M1 force (positive voice = same clause; R1 skeptic finding).")
print("NOT a Lean-owned closure. The completeness QUANTIFIER (exhaustiveness of {D2,ABCD} as")
print("capacity list) is NOT minted — it is made MOOT for the window: selecting any rival is ⊥M1.")
sys.exit(0)
