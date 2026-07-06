#!/usr/bin/env python3
"""gap_w_witness_check — GAP-W (OB-1 of the dissolve-window route): is the witness "+1"
forced — |V_base| = |Omega8| + 1 = 9, not 8 (no witness) and not 10 (two witnesses)?
(DRAFT companion to _TASKS_CENTER_ATTACK/GAP_W_WITNESS_MEMO.md; no registry row.)

CHECKS — 10 check() calls, exact integer/rational arithmetic (fractions.Fraction; no
floats). Failability, stated honestly (de-inflated per skeptic-#1 repair E-GW-4):
checks 2-4 can fail the CONCLUSION directly (a broken Q8 table or a fixed point inside
Omega8 would break GW as claimed). Check 1 is a DEFINITION MIRROR of FiniteTypes.lean —
failable only if the mirror is miscoded or the type model changes. Check 7 (dichotomy
sweep) encodes the three criteria the memo FORGES from owned parts — its conclusion-
failing power is real (any m != 1 surviving, or m = 1 dying, fails GW) but the CRITERIA
themselves are the memo's forging; a skeptic who rejects a criterion rejects the sweep.
Checks 8, 9, 10 RE-READ check 7's criteria function — they fail only via a criteria-
encoding bug, NOT independently of check 7 (their earlier billing as "fail the
CONCLUSION directly" was inflation; repaired). Checks 5-6 are negative controls that
document model-dependence and an over-claim guard: they can fail the conclusion of a
WRONG (stronger) version of GW and bound what this memo may claim.

  1. OWNED_CARD_CHAIN: |Omega8| = |Role x Orient| = (2*2)*2 = 8, |V9| = 8 + 1 = 9
     (mirrors FiniteTypes.lean card_omega8/card_v9; D0-OMEGA8-001).
  2. Q8_TABLE_IS_GROUP: the explicit Q8 = {+-1,+-i,+-j,+-k} multiplication table is a
     non-abelian group of order 8 with center {+-1} (owned identification Omega8 ~= Q8,
     BOOK_01:782/:844, D0-Q8-DEDEKIND-MINIMALITY-001).
  3. FULL_CYCLE_FIXED_POINT_FREE (8-kill, computable half): the owned circulation
     "traversed the full signed role cycle" (BOOK_01:1996); model = the 8 cyclic shifts
     (WitnessHalting.lean shiftMat). EVERY nontrivial shift has ZERO fixed points on the
     8 signed roles => nothing stationary inside Omega8; a stationary marked section must
     be ADJOINED. (Also: any 8-cycle permutation is fixed-point-free.)
  4. Q8_LEFT_TRANSLATION_FREE: same conclusion in the group model — left translation by
     every g != 1 is fixed-point-free, computed on the actual table (not by abstract
     cancellation).
  5. NC_CONJUGATION_MODEL_BREAKS_8KILL (model-dependence, registered): if "circulation"
     meant CONJUGATION instead of translation, the center {+-1} would be stationary
     INSIDE Omega8 and the +1 would be unforced. This control passing (= conjugation has
     interior fixed points) proves the 8-kill LEANS on the owned translation/full-cycle
     model — a named dependence, not decoration.
  6. NC_OPERATOR_FIXED_POINT_NEEDS_NO_WITNESS (over-claim guard): WitnessHalting's fixed
     point E = (1/8) sum_k P_k F P_k^T = (9/2) I (exact rationals) exists over PURE
     Omega8 — 8 slots, NO witness vertex. So witness_halting_cert does NOT force the +1;
     any claim that it does dies here. (Confirms skeptic-#1's finding computationally.)
  7. TEN_KILL_DICHOTOMY_SWEEP: base B_m = Omega8 |_| {m stationary marks}; owned bit
     inventory = 3 bits (two role dyads + sign; "no further bit can be added without an
     exogenous orientation catalog", BOOK_01:1539). Criteria:
       C-HALT: >= 1 stationary mark (halt quotient must close against a stationary
               marked section; BOOK_01:296/:366.5/:1541/:1993);
       C-COPY: marks carry zero distinguishing bits => mutually indistinguishable =>
               copy-symmetry S_m must be trivial: m! = 1 (reuses CASE-2 schema;
               |S_2| > 1 = repeat_has_nontrivial_copy_symmetry, NoExtension.lean:47);
       C-BIT:  distinguishing two marks needs a 4th bit — forbidden (:1539), so the
               "distinguishable pair" escape from C-COPY is closed (it either re-enters
               Omega8's owned bits or imports a catalog).
     Survivors over m in 0..3: exactly {m=1} => |V_base| = 8 + 1 = 9.
  8. NC_FAKE_TEN_MUST_FAIL: an explicit 10-element base (two indistinguishable marks) and
     a labeled-second-mark variant (4th bit) must BOTH fail; either passing = GW false as
     forged (the mandated control; NB it re-reads check 7's criteria — fails only via a
     criteria-encoding bug, E-GW-4).
  9. FIRST_INSTANCE_NO_OVERFIRE: |S_1| = 1! = 1 (mirrors first_instance_canonical,
     NoExtension.lean:52): the copy-kill does NOT fire at m = 1 — V9 itself survives the
     criterion that kills V10. Without this, the kill proves too much.
 10. KILLS_ARE_INDEPENDENT: V8 dies ONLY by C-HALT (passes C-COPY/C-BIT); V10 dies ONLY
     by C-COPY/C-BIT (passes C-HALT) — the 8-kill and the 10-kill are separate
     obligations, neither implies the other.
"""
import sys
from fractions import Fraction
from itertools import product

FAILS = []
COUNT = 0


def check(name: str, ok: bool, note: str = "") -> None:
    global COUNT
    COUNT += 1
    tag = "PASS" if ok else "FAIL"
    print(f"[{tag}] {name}" + (f" — {note}" if note else ""))
    if not ok:
        FAILS.append(name)


# ---------------------------------------------------------------- 1. owned card chain
DYAD = 2
ROLE = DYAD * DYAD          # 4  (card_role)
OMEGA8 = ROLE * 2           # 8  (card_omega8: Role x Orient)
WITNESS = 1                 # PUnit (card = 1)
V9 = OMEGA8 + WITNESS       # 9  (card_v9)
check("OWNED_CARD_CHAIN", (ROLE, OMEGA8, V9) == (4, 8, 9),
      "|Role|=4, |Omega8|=8, |V9|=8+1=9 (FiniteTypes.lean)")

# ---------------------------------------------------------------- 2. Q8 explicit table
# Elements: (s, u) with s in {+1,-1}, u in {'1','i','j','k'};  8 elements.
UNITS = ["1", "i", "j", "k"]
Q8 = [(s, u) for s in (1, -1) for u in UNITS]

# Basis multiplication: (sign, unit) for u*v.
BASIS = {
    ("1", "1"): (1, "1"), ("1", "i"): (1, "i"), ("1", "j"): (1, "j"), ("1", "k"): (1, "k"),
    ("i", "1"): (1, "i"), ("i", "i"): (-1, "1"), ("i", "j"): (1, "k"), ("i", "k"): (-1, "j"),
    ("j", "1"): (1, "j"), ("j", "i"): (-1, "k"), ("j", "j"): (-1, "1"), ("j", "k"): (1, "i"),
    ("k", "1"): (1, "k"), ("k", "i"): (1, "j"), ("k", "j"): (-1, "i"), ("k", "k"): (-1, "1"),
}

def mul(a, b):
    s, u = BASIS[(a[1], b[1])]
    return (a[0] * b[0] * s, u)

ONE = (1, "1")
closure = all(mul(a, b) in Q8 for a in Q8 for b in Q8)
assoc = all(mul(mul(a, b), c) == mul(a, mul(b, c)) for a in Q8 for b in Q8 for c in Q8)
identity = all(mul(ONE, a) == a and mul(a, ONE) == a for a in Q8)
inverses = all(any(mul(a, b) == ONE and mul(b, a) == ONE for b in Q8) for a in Q8)
nonabelian = any(mul(a, b) != mul(b, a) for a in Q8 for b in Q8)
center = [x for x in Q8 if all(mul(g, x) == mul(x, g) for g in Q8)]
check("Q8_TABLE_IS_GROUP",
      closure and assoc and identity and inverses and nonabelian
      and len(Q8) == 8 and sorted(center) == sorted([(1, "1"), (-1, "1")]),
      "non-abelian, |Q8|=8, Z(Q8)={+-1} (BOOK_01:782/:844)")

# ------------------------------------------------- 3. full-cycle freeness (8-kill core)
# WitnessHalting.lean shiftMat: x -> x + k (mod 8); BOOK_01:1996 full signed role cycle.
shift_fixed = {k: [x for x in range(8) if (x + k) % 8 == x] for k in range(8)}
free_shifts = all(shift_fixed[k] == [] for k in range(1, 8))
# Any 8-cycle permutation is fixed-point-free (single orbit of length 8 > 1):
cyc = [(i + 1) % 8 for i in range(8)]  # the canonical 8-cycle
eight_cycle_fpf = all(cyc[x] != x for x in range(8))
check("FULL_CYCLE_FIXED_POINT_FREE", free_shifts and eight_cycle_fpf,
      "no nontrivial shift fixes any signed role; nothing stationary INSIDE Omega8")

# ------------------------------------------------- 4. Q8 left translation is free
lt_fixed = {g: [x for x in Q8 if mul(g, x) == x] for g in Q8 if g != ONE}
check("Q8_LEFT_TRANSLATION_FREE", all(v == [] for v in lt_fixed.values()),
      "g*x = x has no solution for g != 1, on the actual table")

# ------------------------------------------------- 5. NC: conjugation model non-free
def inv(a):
    return next(b for b in Q8 if mul(a, b) == ONE)

conj_fixed_interior = any(
    g != ONE and mul(mul(g, x), inv(g)) == x for g in Q8 for x in Q8
)
# stronger: the whole center is stationary under EVERY conjugation
center_stationary = all(mul(mul(g, z), inv(g)) == z for g in Q8 for z in center)
check("NC_CONJUGATION_MODEL_BREAKS_8KILL", conj_fixed_interior and center_stationary,
      "conjugation has stationary elements INSIDE Omega8 (center +-1) — the 8-kill "
      "leans on the owned translation/full-cycle model, registered dependence")

# ------------------------------------------------- 6. NC: operator fixed point, exact
# E = (1/8) sum_k P_k F P_k^T with F = diag(1..8): exact rational matrix arithmetic.
def matmul(A, B):
    return [[sum(A[i][t] * B[t][j] for t in range(8)) for j in range(8)] for i in range(8)]

def transpose(A):
    return [[A[j][i] for j in range(8)] for i in range(8)]

F = [[Fraction(i + 1) if i == j else Fraction(0) for j in range(8)] for i in range(8)]
P = {}
for k in range(8):
    P[k] = [[Fraction(1) if a == (b + k) % 8 else Fraction(0) for b in range(8)]
            for a in range(8)]
S = [[Fraction(0)] * 8 for _ in range(8)]
for k in range(8):
    M = matmul(matmul(P[k], F), transpose(P[k]))
    S = [[S[i][j] + M[i][j] for j in range(8)] for i in range(8)]
E = [[S[i][j] / 8 for j in range(8)] for i in range(8)]
scalar_92 = all(E[i][j] == (Fraction(9, 2) if i == j else 0)
                for i in range(8) for j in range(8))
shift_inv = all(matmul(matmul(P[k], E), transpose(P[k])) == E for k in range(8))
check("NC_OPERATOR_FIXED_POINT_NEEDS_NO_WITNESS", scalar_92 and shift_inv,
      "E = (9/2) I exists over PURE Omega8 (no witness vertex): witness_halting_cert "
      "does NOT force the +1 — over-claim guard (confirms skeptic #1)")

# ------------------------------------------------- 7. ten-kill dichotomy sweep
OWNED_BITS = 3  # two role dyads + the sign bit; BOOK_01:1539 forbids a 4th

def factorial(n):
    out = 1
    for t in range(2, n + 1):
        out *= t
    return out

def admissible(m: int, marks_labeled: bool = False):
    """Apply the three forged criteria to base B_m = Omega8 |_| {m marks}.
    Returns (ok, killers)."""
    killers = []
    if m < 1:
        killers.append("C-HALT")            # no stationary mark to close against
    if marks_labeled and m >= 2:
        killers.append("C-BIT")             # a 4th bit distinguishes the marks: :1539
    if not marks_labeled and factorial(m) > 1:
        killers.append("C-COPY")            # |S_m| > 1: copy catalogue (CASE-2 schema)
    return (killers == [], killers)

sweep = {m: admissible(m) for m in range(0, 4)}
survivors = [m for m, (ok, _) in sweep.items() if ok]
check("TEN_KILL_DICHOTOMY_SWEEP", survivors == [1],
      f"survivors over m=0..3: {survivors}; base card = 8 + 1 = 9; kills: "
      + "; ".join(f"m={m}:{ks}" for m, (ok, ks) in sweep.items() if not ok))

# ------------------------------------------------- 8. NC: fake tens must fail
ok_copies, k_copies = admissible(2, marks_labeled=False)
ok_labeled, k_labeled = admissible(2, marks_labeled=True)
check("NC_FAKE_TEN_MUST_FAIL", (not ok_copies) and (not ok_labeled),
      f"10-as-copies killed by {k_copies}; 10-as-labeled killed by {k_labeled}; "
      "either passing = GW false as forged")

# ------------------------------------------------- 9. no over-fire at m = 1
check("FIRST_INSTANCE_NO_OVERFIRE", factorial(1) == 1 and admissible(1)[0],
      "|S_1| = 1 (first_instance_canonical): the copy-kill does not fire on the single "
      "witness — V9 survives the criterion that kills V10")

# ------------------------------------------------- 10. kill independence
v8_ok, v8_kills = admissible(0)
v10_ok, v10_kills = admissible(2)
check("KILLS_ARE_INDEPENDENT",
      v8_kills == ["C-HALT"] and "C-HALT" not in v10_kills and not v8_ok and not v10_ok,
      f"V8 dies only by {v8_kills}; V10 dies by {v10_kills} (halt satisfied): "
      "8-kill and 10-kill are separate obligations")

# ----------------------------------------------------------------------------- summary
print()
if FAILS:
    print(f"RESULT: {COUNT - len(FAILS)}/{COUNT} — FAILURES: {FAILS}")
    sys.exit(1)
print(f"RESULT: {COUNT}/{COUNT} check() calls PASS")
