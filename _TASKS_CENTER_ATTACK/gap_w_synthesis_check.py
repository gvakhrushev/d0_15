#!/usr/bin/env python3
"""gap_w_synthesis_check — BREAKTHROUGH-SYNTHESIS attack on the three GAP-W joints:
can W-BRIDGE-1', W-T1 and W-BIT be DERIVED from owned contract + owned Lean + finite
computation, instead of registered as assumptions?
(DRAFT companion to _TASKS_CENTER_ATTACK/GAP_W_SYNTHESIS_MEMO.md v2; no registry row
edited; extends, does not replace, gap_w_witness_check.py 10/10.)

POST-SKEPTIC-#1 STATE (repairs applied, kill accepted in full): Derivation I
(W-BRIDGE-1') was KILLED — named second object: the INVARIANT NON-SCALAR (circulant)
content of the owned emission channel, which check 2's own image exhibits and the NEW
check 18 records explicitly (adverse owned text BOOK_01:2002, six lines after the
memo's :1996 citation — the E-GW-1 citation-stops-short failure mode repeated).
Checks 1-5, 7 remain valid COMPUTATIONS but no longer carry a full derivation: they
exclude interior ELEMENT / SUBSET / absolute-address realizers only; the step from
"no interior realizer of THOSE kinds" to "adjoined base element" consumed the
unstated element-realization premise (= the old joint's core, now named W-ELEM).
Check 10 gained the SC-1 archive-layer extension (Derivation III repair). Check 15's
K-ADDRESS criterion ENCODES the dead S9 inference — the sweep has ZERO defensive
power for Derivation I and is retained only as bookkeeping under the repaired
premise set {W-ELEM, W-REC}.

CHECKS — 19 check() calls (0..18), exact integer/rational arithmetic
(fractions.Fraction; no floats). Independence stated honestly (per the E-GW-4
de-inflation lesson of the witness memo):

  INDEPENDENT conclusion-bearing computations: 1, 2, 3, 4, 5, 6, 7, 10, 11, 12, 14,
  18 (~12). Check 0 is a QUOTE-INTEGRITY guard (fails on text drift of the cited owned
  sentences, not on the mathematical conclusion). Check 8 is TEXTUAL (reads the Lean
  statement line; decisive for the genericity claim, but it verifies a formal-language
  fact, not an arithmetic one). Checks 9 and 13 are near-analytic demonstrations
  (they can only fail via encoding bugs). Checks 15-17 RE-READ the sweep criteria
  encoded from earlier checks — integrative, not independent, and for Derivation I
  DEFENSELESS (see the post-skeptic note above).

  Negative controls that can fail the CONCLUSION (trap (f) discipline):
  check 6 (a non-transitive circulation model SAVES an interior address — the
  W-BRIDGE-1' derivation genuinely leans on the owned transitive full-cycle model,
  BOOK_01:1996); check 14 (a second owned central Z2 — Q8 x C2 world — would SAVE
  labeled-V10: the W-BIT derivation genuinely leans on Z(Q8) having exactly one
  involution, owned by Dedekind 01.7.1A + D0-OMEGA8-CENTER-001). Check 2 includes a
  detection control (a non-invariant matrix must be DETECTED as non-invariant).

  No check constructs its key quantity from the conclusion: the averages, orbits,
  subgroup lattice and automorphism counts are built from the group actions alone;
  "9" never enters as an input.

   0. QUOTES_VERBATIM: every load-bearing owned sentence cited by the synthesis memo
      is re-read from disk at its exact file:line (trap (a) hardener).
   1. AVG_KILLS_INTERIOR_ADDRESSES (scope CORRECTED post-skeptic): the C8 orbit-
      average of EVERY elementary 8x8 record matrix E_ab is circulant with CONSTANT
      diagonal; every absolute-locus marker diag(e_a) averages to the uniform (1/8)I.
      The owned emission channel (BOOK_01:1996, WitnessHalting.lean orbitAverage)
      transmits zero ABSOLUTE-ADDRESS information about Omega8 interior loci. It does
      NOT show the channel is contentless — check 18 shows the opposite (the kill).
   2. AVG_IS_PROJECTION_ONTO_CIRCULANTS: the average is idempotent, its image is
      shift-invariant, shift-invariant == circulant (checked both directions on the
      full basis), and the detection control E_00 is correctly flagged NON-invariant.
   3. INVARIANT_SUBSETS_TRIVIAL: under the full cycle, exactly 2 of 256 subsets of
      Omega8 are invariant: the empty set and all of Omega8. No nonempty proper
      subset can serve as a stable interior realizer of the re-detection class.
   4. ELEMENT_AND_CENTRAL_FREENESS: every nontrivial shift is fixed-point-free on the
      8 signed roles (re-verification of the witness-memo computation), and on the
      actual Q8 table left translation by every g != 1 — in particular by the unique
      central involution -1 — moves every element.
   5. NINE_POINT_EXTENSION_FIXES_MARK: ALL 362880 permutations of a 9-point base are
      swept; exactly 40320 preserve the Omega8 block setwise, and every one of them
      fixes the 9th point. Block-extended averaging preserves the mark's marker
      diag(0,...,0,1) EXACTLY: the adjoined locus survives the sweep unaveraged.
      Stationarity of the single adjoined mark is forced by cardinality, not read
      off the word "stable".
   6. NC_CONJUGATION_MODEL_SAVES_INTERIOR (negative control): under a CONJUGATION
      reading of "circulation" (orbit sizes [1,1,2,2,2], max 2 < 8, incompatible with
      the owned full-traversal text :1996), the center marker is a NON-uniform
      invariant — an interior address WOULD survive and the m>=1 derivation would
      fail. Registered model-dependence, inherited from witness-memo check 5.
   7. TRANSITIVITY_SUFFICES (robustness to the G_8 ambiguity in :1996): marker
      homogenization holds for the dihedral group D8 (order 16) as well — any owned
      symmetry group CONTAINING the transitive cycle homogenizes; the derivation does
      not lean on G_8 being exactly C8.
   8. LEAN_COPY_LEMMA_IS_TYPE_FREE (Derivation II core): the formal STATEMENT of
      repeat_has_nontrivial_copy_symmetry is `1 < Fintype.card (Equiv.Perm (Fin 2))`
      — pure cardinal arithmetic, no zone token; same for first_instance_canonical
      (`Fin 1`); and the module docstring itself applies the schema cross-class
      ("Same forcing as ... via Dedekind").
   9. COPY_COUNT_TYPE_INVARIANT: the bijection count of a 2-element collection is 2
      for four different element TYPES (strings, frozensets, tuples, mark-atoms) —
      the Lean arithmetic consumes only the cardinality; instantiation on marks
      changes no quantity.
  10. DECORATIVE_VS_DYNAMICAL_HORNS (Derivation III fork, computed; SC-1 REPAIR
      APPLIED post-skeptic): the owned-structure model is EXTENDED to {role algebra,
      sign, circulation, ARCHIVE MEMORY LAYER (BOOK_01:1993)}; the archive's only
      owned write channel from the circulated sector is the :1996 emission, whose
      domain is the 8 cells ONLY — mark-blind by construction — so the mark-swap
      extends to an automorphism of the ENLARGED model and the H3 closure is
      unchanged. NB: this mark-blindness of the archive channel is the same
      channel-exhaustiveness reading as W-REC — H3 now leans on it (stated in the
      memo). A DECORATIVE label (referenced by nothing owned, invisible to the
      archive) leaves the swap a full automorphism — 2 compatible label assignments,
      the |S_2| catalogue persists; a DYNAMICAL distinguisher (mark coupled into the
      cycle) breaks the swap but produces cycle arity 9 != 8 (owned arity: |Omega8| =
      8, shiftMat over Fin 8), destroys the mark's stationarity, AND is visible to
      the archive (period change) — confirming decorative/dynamical is the archive-
      relevant split. Both horns close by computation.
  11. Q8_ONE_Z2_TRIPLE_COLLAPSE: on the explicit table, [Q8,Q8] = Z(Q8) = Phi(Q8) =
      {+-1} with the Frattini subgroup computed DIRECTLY (full subgroup enumeration:
      6 subgroups, 3 maximal proper, intersection {+-1}) — extending the Lean owner
      D0-OMEGA8-CENTER-001, which reaches Phi via the abelianization remark. Also:
      Q8 has EXACTLY ONE involution (-1). Every Z2 inside the owned role group IS the
      central one; there is no second owned bit to spend on marks.
  12. BIT_INVENTORY_EXHAUSTED_PIGEONHOLE: the owned bit space (two role dyads x sign)
      has 2^3 = 8 addresses, bijective with the Omega8 cells, ALL occupied; every
      possible owned-bit address for a 9th/10th object collides with an occupied
      circulating cell (8/8 collisions).
  13. LABELS_REDUCE_TO_BITS: over ALL label maps f: {mark0,mark1} -> L, |L| = 2..6
      (90 maps), f separates the pair IFF the induced indicator bit is nonconstant —
      every distinguishing label carries exactly one bit of separation; "it's a label,
      not a bit" is not an escape.
  14. NC_SECOND_OWNED_Z2_WOULD_SAVE_V10 (negative control): in a Q8 x C2 world the
      center has order 4 with THREE central involutions — a second owned central bit
      would exist and labeled-V10 would SURVIVE the one-Z2 kill. The kill fires iff
      the owned group has exactly one central involution — true for Q8 (owned), false
      in the counterfactual: the check tracks the owned input, not the desired output.
  15. SYNTHESIS_DICHOTOMY_SWEEP (integrative RE-READ of checks 1,3,4,10-14): bases
      B_m = Omega8 u {m marks} x distinguisher in {none, decorative, dynamical}:
      survivors = {(m=1, none)} exactly. POST-SKEPTIC CAVEAT: the K-ADDRESS criterion
      encodes the KILLED S9 inference (element-realization consumed silently) — for
      Derivation I this sweep has ZERO defensive power; K-ADDRESS is retained only as
      bookkeeping under the repaired premise set {W-ELEM, W-REC}.
  16. NO_OVERFIRE_AT_ONE (re-read): |S_1| = 1, no criterion fires at (1, none) — V9
      survives the machinery that kills V8 and V10.
  17. KILLS_SEPARATE (re-read): V8 dies ONLY by the address-existence chain; V10 dies
      ONLY by the distinguisher fork — the 8-kill and 10-kill remain independent
      obligations.
  18. SKEPTIC_SECOND_OBJECT_NONSCALAR_INVARIANT (NEW post-skeptic — the kill's named
      second object, computed; ADVERSE to Derivation I): the invariant image of the
      owned emission channel is STRICTLY BIGGER than the scalars — e.g. avg(E_01) is
      shift-invariant, nonzero and NOT a scalar multiple of I; the circulant algebra
      has dimension 8 > 1. Mirrors the adverse owned text BOOK_01:2002 ("This average
      is invariant, but it is **not** a scalar multiple of the identity unless
      irreducibility ... is separately proved"). The channel CAN carry stable
      invariant content without any base-element address — which is why "no interior
      ELEMENT realizer" does not imply "adjoined element" without W-ELEM.
"""
import sys
from fractions import Fraction
from itertools import permutations, product
from pathlib import Path

FAILS = []
COUNT = 0
D0 = Path(__file__).resolve().parent.parent


def check(name: str, ok: bool, note: str = "") -> None:
    global COUNT
    COUNT += 1
    tag = "PASS" if ok else "FAIL"
    print(f"[{tag}] {name}" + (f" — {note}" if note else ""))
    if not ok:
        FAILS.append(name)


# ------------------------------------------------------------------ 0. quote integrity
B00 = D0 / "01_BOOKS" / "BOOK_00_ENTRY_CONTRACT_AND_ADMISSIBILITY.md"
B01 = D0 / "01_BOOKS" / "BOOK_01_CONDENSED_FOUNDATIONS_AND_GRAPH_BIRTH.md"
NOEXT = D0 / "09_LEAN_FORMALIZATION" / "D0" / "Tower" / "NoExtension.lean"

QUOTES = [
    # (file, 1-based line, substring)
    (B00, 143, "no exogenous parameters: no background dependence, no external catalog"),
    (B00, 162, "This strikes not at candidates but at **any** alternative at once"),
    (B00, 167, "A non-normal subgroup yields conjugate copies"),
    (B00, 177, "The detector must read itself autonomously"),
    (B00, 177, "external memory backgrounds are strictly forbidden"),
    (B00, 385, "assume not-X;"),
    (B00, 386, "requires extra structure theta"),
    (B01, 296, "has a halt quotient"),
    (B01, 363, "**operator lift:**"),
    (B01, 364, "**positive response:**"),
    (B01, 366, "**halt quotient:** the comparison has a terminal finite quotient"),
    (B01, 465, "registration is completed when further refinement"),
    (B01, 792, "Telling those copies apart requires an external catalog"),
    (B01, 806, "collapse to a single copy"),
    (B01, 846, "terminal four-role readout algebra obtained after"),
    (B01, 858, "comes only after this quotient"),
    (B01, 996, "stable re-detection classes over finite detector records"),
    (B01, 1166, "halt quotient and stable re-detection class;"),
    (B01, 1530, "That is the catalog M1 forbids"),
    (B01, 1539, "no further bit can be added without an exogenous orientation catalog"),
    (B01, 1541, "requires a stationary marked witness section"),
    (B01, 1556, "extra hidden marker"),
    (B01, 1987, "first addressable graph-birth shell"),
    (B01, 1993, "Continuous circulation inside"),
    (B01, 1993, "topological memory layer"),
    (B01, 1996, "the emitted archive trace is an orbit-averaged shell emission"),
    # post-skeptic-#1 additions:
    (B01, 2002, "invariant, but it is **not** a scalar multiple of the identity"),
    (B01, 253, "irreducible addressable record quantum"),
]
_lines = {}
quote_fails = []
for f, ln, sub in QUOTES:
    if f not in _lines:
        _lines[f] = f.read_text(encoding="utf-8").splitlines()
    text = _lines[f][ln - 1] if ln - 1 < len(_lines[f]) else ""
    if sub not in text:
        quote_fails.append(f"{f.name}:{ln} missing {sub!r}")
check("QUOTES_VERBATIM", not quote_fails,
      f"{len(QUOTES)} owned sentences re-read at exact file:line"
      + ("; FAILS: " + "; ".join(quote_fails) if quote_fails else ""))

# ------------------------------------------- 1. averaging kills interior addresses
N = 8


def avg_c8(M):
    """C8 orbit average: (1/8) sum_k P_k M P_k^T, P_k: x -> x+k (mod 8)."""
    return [[sum(M[(i - k) % N][(j - k) % N] for k in range(N)) / Fraction(N)
             for j in range(N)] for i in range(N)]


def is_circulant(M):
    return all(M[i][j] == M[(i + 1) % N][(j + 1) % N]
               for i in range(N) for j in range(N))


def elem(a, b):
    return [[Fraction(1) if (i, j) == (a, b) else Fraction(0)
             for j in range(N)] for i in range(N)]


all_circ, all_diag_const = True, True
for a in range(N):
    for b in range(N):
        A = avg_c8(elem(a, b))
        if not is_circulant(A):
            all_circ = False
        if any(A[i][i] != A[0][0] for i in range(N)):
            all_diag_const = False
markers_uniform = all(
    avg_c8(elem(a, a)) == [[Fraction(1, N) if i == j else Fraction(0)
                            for j in range(N)] for i in range(N)]
    for a in range(N))
check("AVG_KILLS_INTERIOR_ADDRESSES",
      all_circ and all_diag_const and markers_uniform,
      "all 64 averaged basis records circulant, constant diagonal; every locus "
      "marker -> uniform (1/8)I: the owned emission channel carries no interior "
      "address")

# ------------------------------------------- 2. average = projection onto circulants


def shift_conj(M, k):
    return [[M[(i - k) % N][(j - k) % N] for j in range(N)] for i in range(N)]


proj_idem, image_inv = True, True
for a in range(N):
    for b in range(N):
        A = avg_c8(elem(a, b))
        if avg_c8(A) != A:
            proj_idem = False
        if any(shift_conj(A, k) != A for k in range(N)):
            image_inv = False
# both directions on the basis: shift-invariant <=> circulant
directions = all(
    is_circulant(A) == all(shift_conj(A, k) == A for k in range(N))
    for a in range(N) for b in range(N)
    for A in [avg_c8(elem(a, b)), elem(a, b)])
# detection control: E_00 must be flagged NON-invariant (the test can fail things)
control_detects = not all(shift_conj(elem(0, 0), k) == elem(0, 0) for k in range(N))
check("AVG_IS_PROJECTION_ONTO_CIRCULANTS",
      proj_idem and image_inv and directions and control_detects,
      "idempotent; image shift-invariant; invariant<=>circulant on the basis; "
      "control: E_00 correctly detected non-invariant")

# ------------------------------------------- 3. invariant subsets are trivial
inv_subsets = [S for S in range(1 << N)
               if S == ((S << 1) & 0xFF) | (S >> (N - 1))]
check("INVARIANT_SUBSETS_TRIVIAL",
      sorted(inv_subsets) == [0, 0xFF],
      "2 of 256 subsets cycle-invariant: only {} and Omega8 — no proper nonempty "
      "interior realizer at subset level")

# ------------------------------------------- 4. element + central freeness
UNITS = ["1", "i", "j", "k"]
Q8 = [(s, u) for s in (1, -1) for u in UNITS]
BASIS = {
    ("1", "1"): (1, "1"), ("1", "i"): (1, "i"), ("1", "j"): (1, "j"), ("1", "k"): (1, "k"),
    ("i", "1"): (1, "i"), ("i", "i"): (-1, "1"), ("i", "j"): (1, "k"), ("i", "k"): (-1, "j"),
    ("j", "1"): (1, "j"), ("j", "i"): (-1, "k"), ("j", "j"): (-1, "1"), ("j", "k"): (1, "i"),
    ("k", "1"): (1, "k"), ("k", "i"): (1, "j"), ("k", "j"): (-1, "i"), ("k", "k"): (-1, "1"),
}


def mul(a, b):
    s, u = BASIS[(a[1], b[1])]
    return (a[0] * b[0] * s, u)


ONE, NEG = (1, "1"), (-1, "1")
shift_free = all(all((x + k) % N != x for x in range(N)) for k in range(1, N))
translation_free = all(all(mul(g, x) != x for x in Q8) for g in Q8 if g != ONE)
neg_moves_all = all(mul(NEG, x) != x for x in Q8)
check("ELEMENT_AND_CENTRAL_FREENESS",
      shift_free and translation_free and neg_moves_all,
      "no nontrivial shift fixes a signed role; Q8 left translation free for all "
      "g != 1, including the central involution -1")

# ------------------------------------------- 5. the 9th point is auto-fixed
count_pres, violations = 0, 0
for p in permutations(range(9)):
    if all(v < 8 for v in p[:8]):          # preserves the Omega8 block setwise
        count_pres += 1
        if p[8] != 8:
            violations += 1
W9 = [[Fraction(1) if i == j == 8 else Fraction(0) for j in range(9)]
      for i in range(9)]


def avg_c8_ext(M):
    """Block-extended average: shifts act on 0..7, fix point 8."""
    def img(x, k):
        return (x + k) % 8 if x < 8 else 8
    return [[sum(M[[r for r in range(9) if img(r, k) == i][0]]
                 [[c for c in range(9) if img(c, k) == j][0]]
                 for k in range(8)) / Fraction(8)
             for j in range(9)] for i in range(9)]


mark_marker_survives = (avg_c8_ext(W9) == W9)
check("NINE_POINT_EXTENSION_FIXES_MARK",
      count_pres == 40320 and violations == 0 and mark_marker_survives,
      "40320/362880 permutations preserve Omega8 setwise; ALL fix the 9th point; "
      "the mark's marker survives block averaging exactly — stationarity forced by "
      "cardinality")

# ------------------------------------------- 6. NC: conjugation model saves interior


def inv(a):
    return next(b for b in Q8 if mul(a, b) == ONE)


orbits = []
seen = set()
for x in Q8:
    if x in seen:
        continue
    orb = {mul(mul(g, x), inv(g)) for g in Q8}
    seen |= orb
    orbits.append(len(orb))
idx = {x: n for n, x in enumerate(Q8)}
center_marker = [Fraction(1) if Q8[n] in (ONE, NEG) else Fraction(0)
                 for n in range(N)]
conj_avg = [sum(center_marker[idx[mul(mul(inv(g), Q8[n]), g)]] for g in Q8)
            / Fraction(len(Q8)) for n in range(N)]
nonuniform_invariant = (conj_avg == center_marker
                        and len(set(center_marker)) > 1)
check("NC_CONJUGATION_MODEL_SAVES_INTERIOR",
      sorted(orbits) == [1, 1, 2, 2, 2] and max(orbits) < 8
      and nonuniform_invariant,
      "conjugation orbits [1,1,2,2,2] (max 2 < 8: no full traversal, contra :1996); "
      "center marker survives conjugation-averaging NON-uniformly — an interior "
      "address would live: the derivation leans on the owned transitive model")

# ------------------------------------------- 7. any transitive G_8 homogenizes
D8 = [("r", k) for k in range(8)] + [("s", k) for k in range(8)]


def d8_apply(g, x):
    t, k = g
    return (x + k) % 8 if t == "r" else (k - x) % 8


d8_closed = all(
    any(all(d8_apply(h, d8_apply(g, x)) == d8_apply(f, x) for x in range(8))
        for f in D8)
    for g in D8 for h in D8)
d8_transitive = all(any(d8_apply(g, 0) == y for g in D8) for y in range(8))
d8_uniform = all(
    [sum(Fraction(1) for g in D8 if d8_apply(g, a) == x) / Fraction(len(D8))
     for x in range(8)] == [Fraction(1, 8)] * 8
    for a in range(8))
check("TRANSITIVITY_SUFFICES",
      len(set(tuple(d8_apply(g, x) for x in range(8)) for g in D8)) == 16
      and d8_closed and d8_transitive and d8_uniform,
      "dihedral D8 (order 16, transitive) also averages every locus marker to "
      "uniform — robustness to the G_8 ambiguity in :1996")

# ------------------------------------------- 8. the Lean copy lemma is type-free
noext = NOEXT.read_text(encoding="utf-8").splitlines()
stmt2 = next((l for l in noext if "theorem repeat_has_nontrivial_copy_symmetry" in l), "")
stmt1 = next((l for l in noext if "theorem first_instance_canonical" in l), "")
forbidden = ["Zone", "zone", "Z4", "Omega", "omega"]
crossclass = any("Same forcing as" in l for l in noext)
check("LEAN_COPY_LEMMA_IS_TYPE_FREE",
      "1 < Fintype.card (Equiv.Perm (Fin 2))" in stmt2
      and "Fintype.card (Equiv.Perm (Fin 1)) = 1" in stmt1
      and not any(t in stmt2 or t in stmt1 for t in forbidden)
      and crossclass,
      "statements are pure Perm(Fin n) cardinal arithmetic, zero zone tokens; module "
      "docstring itself applies the schema cross-class ('Same forcing as ... via "
      "Dedekind')")

# ------------------------------------------- 9. copy count is type-invariant
collections = [("zoneA", "zoneB"),
               (frozenset([1]), frozenset([2])),
               ((0,), (1,)),
               ("mark0", "mark1")]
counts = [sum(1 for _ in permutations(c)) for c in collections]
single = sum(1 for _ in permutations(("mark0",)))
check("COPY_COUNT_TYPE_INVARIANT",
      counts == [2, 2, 2, 2] and single == 1,
      "|bijections| = 2 for 2-element collections of four different element types; "
      "= 1 for a singleton: the arithmetic consumes only cardinality")

# ------------------------------------------- 10. decorative vs dynamical horns
PTS = list(range(10))            # 0..7 = Omega8 cells, 8/9 = marks


def succ_owned(x):
    return (x + 1) % 8 if x < 8 else x   # circulation inside Omega8 (:1993); marks fixed


labels = {8: "a", 9: "b"}         # decorative: referenced by NOTHING owned


def swap(x):
    return {8: 9, 9: 8}.get(x, x)


swap_is_auto = (all(swap(succ_owned(x)) == succ_owned(swap(x)) for x in PTS)
                and {swap(x) for x in range(8)} == set(range(8))
                and all(succ_owned(swap(m)) == swap(m) for m in (8, 9)))
relabel = {m: labels[swap(m)] for m in (8, 9)}
two_assignments = (relabel != labels)


# SC-1 REPAIR (skeptic #1, accepted): enlarge the owned model with the ARCHIVE
# MEMORY LAYER (BOOK_01:1993). Its only owned write channel from the circulated
# sector is the :1996 emission — domain = the 8 cells ONLY, mark-blind by
# construction (this mark-blindness is the same channel-exhaustiveness reading as
# W-REC; the lean is stated in the memo, §IV).
def archive_write(succ_fn):
    """Integrate the cell-record along each cell's circulation orbit and record the
    return period — reads CELLS only; never evaluates marks or labels."""
    out = []
    for i in range(8):
        total, x, steps = Fraction(0), i, 0
        while True:
            if x < 8:
                total += Fraction(x + 1)
            x = succ_fn(x)
            steps += 1
            if x == i or steps > 20:
                break
        out.append((total, steps))
    return tuple(out)


def succ_swapped(x):
    return swap(succ_owned(swap(x)))       # the whole model transported by the swap


arch_owned = archive_write(succ_owned)
archive_mark_blind = (archive_write(succ_swapped) == arch_owned)
archive_uniform = all(v == (Fraction(36), 8) for v in arch_owned)
# dynamical horn: couple mark 8 into the cycle


def succ_dyn(x):
    if x == 7:
        return 8
    if x == 8:
        return 0
    return (x + 1) % 8 if x < 8 else x


orbit_len = 1
y = succ_dyn(0)
while y != 0:
    y = succ_dyn(y)
    orbit_len += 1
swap_breaks_dyn = any(swap(succ_dyn(x)) != succ_dyn(swap(x)) for x in PTS)
archive_sees_dynamical = (archive_write(succ_dyn) != arch_owned)
check("DECORATIVE_VS_DYNAMICAL_HORNS",
      swap_is_auto and two_assignments
      and archive_mark_blind and archive_uniform and archive_sees_dynamical
      and orbit_len == 9 and orbit_len != 8 and succ_dyn(8) != 8
      and swap_breaks_dyn,
      "decorative: mark-swap is an automorphism of ALL owned structure INCLUDING "
      "the archive layer (mark-blind :1996 channel — SC-1 repair) => 2 compatible "
      "assignments, |S_2| catalogue persists; dynamical: cycle arity becomes 9 != 8 "
      "(owned arity 8), the mark stops being stationary, and the archive SEES the "
      "coupling (period change)")

# ------------------------------------------- 11. Q8: one Z2, triple collapse
subgroups = []
for mask in range(1, 1 << 8):
    S = [Q8[n] for n in range(8) if mask >> n & 1]
    if ONE in S and all(mul(a, b) in S for a in S for b in S) \
            and all(inv(a) in S for a in S):
        subgroups.append(frozenset(S))
subgroups = sorted(set(subgroups), key=len)
maximal = [H for H in subgroups if len(H) < 8
           and not any(len(K) < 8 and H < K for K in subgroups)]
frattini = frozenset.intersection(*maximal) if maximal else frozenset()
commutators = {mul(mul(a, b), mul(inv(a), inv(b))) for a in Q8 for b in Q8}
comm_sub = frozenset(commutators)      # already closed for Q8; verify anyway
comm_closed = all(mul(a, b) in comm_sub for a in comm_sub for b in comm_sub)
center = frozenset(x for x in Q8 if all(mul(g, x) == mul(x, g) for g in Q8))
pm1 = frozenset({ONE, NEG})
involutions = [x for x in Q8 if x != ONE and mul(x, x) == ONE]
check("Q8_ONE_Z2_TRIPLE_COLLAPSE",
      len(subgroups) == 6 and len(maximal) == 3
      and all(len(H) == 4 for H in maximal)
      and comm_closed and comm_sub == center == frattini == pm1
      and involutions == [NEG],
      "6 subgroups, 3 maximal (order 4), Frattini = [Q8,Q8] = Z(Q8) = {+-1} by "
      "direct enumeration; EXACTLY ONE involution (-1): every Z2 in the owned role "
      "group is the central one")

# ------------------------------------------- 12. owned bit inventory exhausted
addresses = list(product((0, 1), (0, 1), ("+", "-")))
role_of = {(0, 0): "A", (0, 1): "B", (1, 0): "C", (1, 1): "D"}
cells = {(role_of[(d1, d2)], s) for (d1, d2, s) in addresses}
omega8_cells = {(r, s) for r in "ABCD" for s in "+-"}
collisions = sum(1 for a in addresses
                 if (role_of[(a[0], a[1])], a[2]) in omega8_cells)
check("BIT_INVENTORY_EXHAUSTED_PIGEONHOLE",
      len(addresses) == 8 and cells == omega8_cells and collisions == 8,
      "2^3 = 8 owned-bit addresses, bijective with Omega8 cells, ALL occupied: "
      "every owned-bit address for an extra object collides with a circulating cell")

# ------------------------------------------- 13. labels reduce to bits
total, mismatches = 0, 0
for k in range(2, 7):
    for f in product(range(k), repeat=2):
        total += 1
        separates = f[0] != f[1]
        induced_bit_nonconstant = (int(f[1] != f[0]) != 0)
        if separates != induced_bit_nonconstant:
            mismatches += 1
check("LABELS_REDUCE_TO_BITS",
      total == 90 and mismatches == 0,
      "over all 90 label maps (|L| = 2..6): separating <=> induced indicator bit "
      "nonconstant — every distinguishing label IS one bit of separation")

# ------------------------------------------- 14. NC: a second owned Z2 saves V10
Q8xC2 = [(q, c) for q in Q8 for c in (0, 1)]


def mul2(x, y):
    return (mul(x[0], y[0]), (x[1] + y[1]) % 2)


E2 = (ONE, 0)
center2 = [x for x in Q8xC2
           if all(mul2(g, x) == mul2(x, g) for g in Q8xC2)]
central_inv2 = [x for x in center2 if x != E2 and mul2(x, x) == E2]
central_inv_q8 = [x for x in Q8 if x != ONE and mul(x, x) == ONE
                  and all(mul(g, x) == mul(x, g) for g in Q8)]


def one_z2_kill_fires(n_central_involutions):
    return n_central_involutions == 1     # a UNIQUE owned bit => no second source


check("NC_SECOND_OWNED_Z2_WOULD_SAVE_V10",
      len(center2) == 4 and len(central_inv2) == 3
      and len(central_inv_q8) == 1
      and one_z2_kill_fires(len(central_inv_q8))
      and not one_z2_kill_fires(len(central_inv2)),
      "Z(Q8xC2) has order 4 with 3 central involutions: there the kill would NOT "
      "fire and labeled-V10 would survive; it fires for Q8 (exactly 1) — the kill "
      "tracks the owned Dedekind/center input")

# ------------------------------------------- 15. synthesis dichotomy sweep (re-read)


def factorial(n):
    out = 1
    for t in range(2, n + 1):
        out *= t
    return out


def verdict(m, dist):
    """Criteria encoded from checks 1,3,4 (R-ADDRESS), 9/10/13 (copy/decorative),
    10 (dynamical), 11/12/14 (no second owned bit). Returns (survives, killers)."""
    killers = []
    if dist == "dynamical":
        # coupling any mark into the owned dynamics: arity != 8 and mark moves
        killers.append("K-ARITY/STATIONARITY")
        m_stationary = m - 1            # the coupled mark is no longer a mark
    else:
        m_stationary = m
    if m_stationary < 1:
        killers.append("K-ADDRESS")     # no interior realizer exists (checks 1,3,4)
    if dist == "none" and factorial(m_stationary) > 1:
        killers.append("K-COPY")        # |S_m| > 1 catalogue
    if dist == "decorative" and m_stationary >= 2:
        killers.append("K-COPY(swap-auto)")   # check 10: swap still an automorphism
        killers.append("K-NO-SECOND-BIT")     # checks 11,12,14
    return (not killers, killers)


cases = [(m, d) for m in range(4)
         for d in (("none", "dynamical") if m < 2
                   else ("none", "decorative", "dynamical"))]
sweep = {c: verdict(*c) for c in cases}
survivors = [c for c, (ok, _) in sweep.items() if ok]
check("SYNTHESIS_DICHOTOMY_SWEEP", survivors == [(1, "none")],
      f"survivors: {survivors}; base card = 8 + 1 = 9; "
      + "; ".join(f"{c}:{ks}" for c, (ok, ks) in sweep.items() if not ok))

# ------------------------------------------- 16. no over-fire at m = 1 (re-read)
check("NO_OVERFIRE_AT_ONE",
      factorial(1) == 1 and sweep[(1, "none")][0],
      "|S_1| = 1 (first_instance_canonical mirror); nothing fires at (1, none): "
      "V9 survives its own kill machinery")

# ------------------------------------------- 17. kills separate (re-read)
v8 = sweep[(0, "none")][1]
v10n = sweep[(2, "none")][1]
v10d = sweep[(2, "decorative")][1]
check("KILLS_SEPARATE",
      v8 == ["K-ADDRESS"] and "K-ADDRESS" not in v10n + v10d
      and v10n == ["K-COPY"] and "K-NO-SECOND-BIT" in v10d,
      f"V8 dies only by {v8}; V10 dies by {v10n} / {v10d} (address satisfied): "
      "8-kill and 10-kill remain separate obligations")

# ------------------------------------------- 18. the kill's named second object
A01 = avg_c8(elem(0, 1))
a01_invariant = all(shift_conj(A01, k) == A01 for k in range(N))
a01_nonzero = any(A01[i][j] != 0 for i in range(N) for j in range(N))
a01_scalar = all(A01[i][j] == (A01[0][0] if i == j else Fraction(0))
                 for i in range(N) for j in range(N))
# the invariant image spans the full 8-dim circulant algebra: the 8 averaged band
# representatives avg(E_0b), b = 0..7, are pairwise distinct band matrices
bands = {tuple(tuple(r) for r in avg_c8(elem(0, b))) for b in range(N)}
check("SKEPTIC_SECOND_OBJECT_NONSCALAR_INVARIANT",
      a01_invariant and a01_nonzero and (not a01_scalar) and len(bands) == N,
      "avg(E_01) is shift-invariant, nonzero and NOT a scalar multiple of I; the "
      "invariant image is the 8-dim circulant algebra (BOOK_01:2002) — the owned "
      "channel CAN carry stable invariant content with no base-element address: "
      "ADVERSE to Derivation I; 'no interior element realizer' does not give '+1' "
      "without W-ELEM")

# ----------------------------------------------------------------------------- summary
print()
if FAILS:
    print(f"RESULT: {COUNT - len(FAILS)}/{COUNT} — FAILURES: {FAILS}")
    sys.exit(1)
print(f"RESULT: {COUNT}/{COUNT} check() calls PASS")
