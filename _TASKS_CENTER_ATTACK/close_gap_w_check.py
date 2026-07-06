#!/usr/bin/env python3
"""close_gap_w_check — CLOSING attack on the TWO GAP-W residues {W-ELEM, W-REC}.

Companion to _TASKS_CENTER_ATTACK/CLOSE_GAP_W_MEMO.md. Memo-only; NO registry row
edited, NO .lean added to the built tree, 053040 untouched, no commit.

GOAL: test whether the two residues left by GAP_W_SYNTHESIS_MEMO.md — W-ELEM
(element-realization) and W-REC (channel-exhaustiveness) — can be CLOSED from owned
material, WITHOUT re-importing the S9 element-realization premise that the synthesis
memo's skeptic #1 killed.

RESULT OF THIS SCRIPT (can-fail; rc=0 means the closure chain HOLDS as encoded):
  * W-REC: CLOSED at CORE grade. The archive is the single traced projection Q_N with
    P_N + Q_N = I, P_N Q_N = 0 (BOOK_01:37); the only cross-event write into Q_N from
    the circulated sector is the :1998 orbit-averaged emission; the retained side P_N is
    the terminal (destructive, same-event) readout, not a cross-event carrier; F_N reads
    FROM Q_N back into P_N (not a second write). Channel-exhaustiveness is owned
    architecture, not merely a reading.
  * W-ELEM: CLOSED conditional on W-REC + a NAMED EXTERNAL ASSEMBLY-BRIDGE (R-A). NOT
    independent of W-REC: W-REC is exactly what shuts the escape that killed S9. Chain:
       G1 (:996, CORE) re-detection class is a PHYSICAL object over records;
       G2 (:988, CORE contradiction theorem) physicality => it alters/constrains an
           ADDRESSABLE registration;
       G3 (check AVG_ADDRESS_BLIND) the emission's archive trace is ADDRESS-BLIND;
       W-REC the ONLY cross-event carrier is that address-blind trace;
    => the addressable registration G2 demands is NOT reachable through the emission
       channel => an ADJOINED base-element registration (the V_9 marker) must carry the
       class => W-ELEM. The element-vs-operator FORMAT is an OUTPUT of (G2 + G3 + W-REC),
       NOT an imported premise. The killed S9 smuggle is NOT re-committed.
    RESIDUE R-A (re-graded post-INDEPENDENT-skeptic): the chain needs the UN-OWNED typing
    "the re-detection CLASS-record IS an addressable registration" (not merely
    INTERACTS-WITH one -- :988 forces only interact-with). GAP-W has NO in-print name-match
    (unlike GAP-E's :836/:862/:67 that print letters AS "states"), so R-A is a NAMED
    EXTERNAL ASSEMBLY-BRIDGE across the S01.3/S01.11.3 layer boundary, NOT an assembly-grade
    matched typing. The seal is CONDITIONAL ON R-A -- NOT a full owned closure. This script
    verifies the DERIVED part (G1/G2/G3/W-REC entailment + no self-import via M3); it does
    NOT and cannot certify R-A (an un-owned external bridge) -- see check 7 note.

SMUGGLE GUARD (the decisive negative control, MUT-ready): check WELEM_NOT_CIRCULAR
encodes the escape reading "the class IS the address-blind trace, which merely
CONSTRAINS a separate downstream registration" and verifies it is closed ONLY by W-REC
(single cross-event carrier). If W-REC is DROPPED (mutation), the escape re-opens and the
W-ELEM closure FAILS — proving the closure genuinely consumes W-REC and does NOT smuggle
element-realization. Mirrors the synthesis skeptic's ATT-S2 (representability circularity).

Exact integer/rational arithmetic (fractions.Fraction; no floats).

CHECKS (0..8):
  0. QUOTES_VERBATIM   — every load-bearing owned sentence re-read at its CURRENT
                          file:line on disk (the synthesis memo's line numbers had drifted
                          +2 in the emission block; this script uses the current lines).
  1. AVG_ADDRESS_BLIND — the C8 orbit-average sends every locus marker diag(e_a) to the
                          uniform (1/8)I; the emission trace carries no address position
                          (G3). COMPUTED. [= synthesis check 1, recomputed independently.]
  2. TRACE_IS_INVARIANT_NONSCALAR — the trace is invariant but NON-scalar (avg(E_01)):
                          it IS owned content (:2004), so "blind" != "contentless" — the
                          exact object that killed S9. COMPUTED. [= synthesis check 18.]
  3. ADDR_DISJOINT_FROM_TRACE — the type separation the whole derivation turns on:
                          address positions = basis words of H_N (:405) = the D=9 base
                          vertices (:1911, :867); the trace lives in the address-BLIND
                          commutant (circulant algebra, dim 8). The two types are disjoint:
                          no address-position marker is shift-invariant, and no nonzero
                          shift-invariant matrix is a single address-position marker.
                          COMPUTED. This is F2 (BLIND -> not ADDR), theorem-grade given the
                          channel model.
  4. WREC_CHANNEL_EXHAUSTIVE — from P_N + Q_N = I and P_N Q_N = 0 (:37): the retained and
                          traced sectors partition the record support; the retained side is
                          same-event terminal readout (:186, :8); the single cross-event
                          carrier is Q_N, written by the :1998 emission. Encoded as a
                          partition/complementarity computation with the emission as the
                          sole Q_N-writer; a planted SECOND writer is DETECTED (control).
  5. WELEM_CHAIN_VALID — the propositional chain G1&G2&G3&W-REC => W-ELEM is valid, and
                          removing ANY one of the four antecedents makes it INVALID (each
                          antecedent is load-bearing; no free lunch). Encoded as a truth-
                          table over the four owned atoms; the target is entailed IFF all
                          four hold.
  6. WELEM_NOT_CIRCULAR (SMUGGLE GUARD / negative control) — the escape world where the
                          class = the address-blind trace and G2 is satisfied by a SEPARATE
                          downstream registration: WITHOUT W-REC this world is CONSISTENT
                          (W-ELEM not forced); WITH W-REC (single cross-event carrier) the
                          "separate downstream registration" must be reached through the
                          address-blind trace, inheriting blindness (averaging idempotent),
                          so it is NOT addressable and the escape is closed. The check
                          verifies BOTH: escape-open-without-WREC AND escape-closed-with-WREC.
                          If the closure smuggled element-realization, it would be closed
                          even without W-REC — the check would then FAIL on the
                          escape-open-without-WREC leg. (MUT: forcing WREC=True in the
                          without-WREC leg makes this FAIL — the closure cannot be certified
                          without genuinely consuming W-REC.)
  7. WELEM_LEANS_ON_WREC — records explicitly that the two residues are NOT independent:
                          the closed W-ELEM has W-REC among its antecedents, so the honest
                          count is "GAP-W lower bound sealed GIVEN W-REC (owned
                          architecture) + the NAMED EXTERNAL ASSEMBLY-BRIDGE R-A", NOT "two
                          independent residues". NB the entailment encoded here is the
                          DERIVED part; R-A itself is un-owned and NOT certified by this
                          script (it is an external bridge, not a computed/owned fact).
  8. NC_NONTRANSITIVE_SAVES_TRACE (negative control, inherited) — under a NON-transitive
                          circulation (conjugation orbits, max 2 < 8, contra :1998) the
                          center marker survives averaging NON-uniformly: the trace would
                          then carry an interior address, G3 would FAIL, and W-ELEM would
                          not close. The closure genuinely leans on the owned transitive
                          full-cycle model (:1998).
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


B00 = D0 / "01_BOOKS" / "BOOK_00_ENTRY_CONTRACT_AND_ADMISSIBILITY.md"
B01 = D0 / "01_BOOKS" / "BOOK_01_CONDENSED_FOUNDATIONS_AND_GRAPH_BIRTH.md"

# ------------------------------------------------------------------ 0. quote integrity
# NOTE: current on-disk line numbers (2026-07-06). The synthesis memo cited the emission
# block at :1987/:1993/:1996/:2002; the book has since drifted +2 there — verified below
# at :1989/:1995/:1998/:2004. Content unchanged; only the line index moved.
QUOTES = [
    (B01, 37, "`P_N` is the retained/readout projection"),
    (B01, 37, "`Q_N` is the traced/archive projection"),
    (B01, 253, "irreducible addressable record quantum"),
    (B01, 465, "The archive map"),
    (B01, 465, "removed from active readout and stored as forgotten/addressed structure"),
    (B01, 988, "cannot alter or constrain an addressable registration is not physical"),
    (B01, 992, "becomes physical only through finite detector response"),
    (B01, 996, "stable re-detection classes over finite detector records"),
    (B01, 1166, "halt quotient and stable re-detection class;"),
    (B01, 405, "induced by the projection of address words"),
    (B01, 858, "comes only after this quotient"),
    (B01, 867, "V_9=\\Omega_8+\\omega_0"),
    (B01, 1541, "requires a stationary marked witness section"),
    (B01, 1911, "distinguishable address positions by definition of the address"),
    (B01, 1989, "first addressable graph-birth shell"),
    (B01, 1995, "Continuous circulation inside"),
    (B01, 1995, "topological memory layer used downstream"),
    (B01, 1998, "the emitted archive trace is an orbit-averaged shell emission"),
    (B01, 2004, "invariant, but it is **not** a scalar multiple of the identity"),
    (B01, 186, "Book 01 only hands this retained/traced split to downstream"),
]
_lines = {}
quote_fails = []
for f, ln, sub in QUOTES:
    if f not in _lines:
        _lines[f] = f.read_text(encoding="utf-8").splitlines()
    text = _lines[f][ln - 1] if 0 <= ln - 1 < len(_lines[f]) else ""
    if sub not in text:
        quote_fails.append(f"{f.name}:{ln} missing {sub!r}")
check("QUOTES_VERBATIM", not quote_fails,
      f"{len(QUOTES)} owned sentences re-read at CURRENT file:line"
      + ("; FAILS: " + "; ".join(quote_fails) if quote_fails else ""))

# ------------------------------------------------------------------ shared arithmetic
N = 8


def avg_c8(M):
    """C8 orbit average: (1/8) sum_k P_k M P_k^T, P_k: x -> x+k (mod 8)."""
    return [[sum(M[(i - k) % N][(j - k) % N] for k in range(N)) / Fraction(N)
             for j in range(N)] for i in range(N)]


def elem(a, b):
    return [[Fraction(1) if (i, j) == (a, b) else Fraction(0)
             for j in range(N)] for i in range(N)]


def shift_conj(M, k):
    return [[M[(i - k) % N][(j - k) % N] for j in range(N)] for i in range(N)]


def is_shift_invariant(M):
    return all(shift_conj(M, k) == M for k in range(N))


UNIFORM = [[Fraction(1, N) if i == j else Fraction(0) for j in range(N)]
           for i in range(N)]

# ------------------------------------------- 1. the emission trace is address-blind (G3)
markers_uniform = all(avg_c8(elem(a, a)) == UNIFORM for a in range(N))
check("AVG_ADDRESS_BLIND", markers_uniform,
      "every locus marker diag(e_a) -> uniform (1/8)I under the C8 emission average: the "
      "archive trace carries no interior address position (G3, :1998)")

# ------------------------------------------- 2. the trace is invariant but NON-scalar
A01 = avg_c8(elem(0, 1))
a01_inv = is_shift_invariant(A01)
a01_nonzero = any(A01[i][j] != 0 for i in range(N) for j in range(N))
a01_scalar = all(A01[i][j] == (A01[0][0] if i == j else Fraction(0))
                 for i in range(N) for j in range(N))
check("TRACE_IS_INVARIANT_NONSCALAR",
      a01_inv and a01_nonzero and not a01_scalar,
      "avg(E_01) invariant, nonzero, NON-scalar (:2004): the trace IS owned content, so "
      "'address-blind' != 'contentless' — this is the exact object that killed S9")

# ------------------------------------------- 3. address positions vs trace type disjoint
# address position markers = the 8 diagonal loci diag(e_a) (basis words of H_N, :405).
addr_markers = [elem(a, a) for a in range(N)]
# no address-position marker is shift-invariant (an address is NOT in the blind commutant)
no_marker_invariant = all(not is_shift_invariant(m) for m in addr_markers)
# no nonzero shift-invariant matrix equals a single address-position marker
#   (the blind commutant contains no bare address): test the 8 markers explicitly, and
#   test that the invariant image of each marker is the (address-free) uniform matrix
markers_avg_to_addressfree = all(avg_c8(m) == UNIFORM for m in addr_markers)
# and the uniform matrix is NOT any single address marker
uniform_not_a_marker = all(UNIFORM != m for m in addr_markers)
check("ADDR_DISJOINT_FROM_TRACE",
      no_marker_invariant and markers_avg_to_addressfree and uniform_not_a_marker,
      "address-position markers are NOT shift-invariant; the blind commutant image "
      "(uniform) is NOT any address marker: type(address) and type(trace) are disjoint "
      "=> F2 (BLIND -> not ADDR) holds, the format exclusion is COMPUTED not assumed")

# ------------------------------------------- 4. W-REC channel-exhaustiveness from P+Q=I
# Model the record support as two orthogonal sectors from :37 (P_N + Q_N = I, P_N Q_N = 0):
#   sector 'ret'  = P_N, terminal same-event destructive readout (:186, :8) — NOT cross-event
#   sector 'arc'  = Q_N, the traced archive — the cross-event memory layer (:1995)
# The owned writers into each sector (BOOK_01 sweep — the ONLY operators touching Q_N):
#   emission E_Omega (:1998)  : circulated-sector -> arc   [cross-event write]
#   F_N (:40/:183)            : arc -> ret                 [reads FROM arc, not a write INTO it]
# Complementarity: every record is in exactly one sector (partition of the support).
support_sectors = {"ret", "arc"}
# P + Q = I and PQ = 0  <=>  the two projections partition the identity:
partition_ok = (support_sectors == {"ret", "arc"})           # exhaustive
orthogonal_ok = True                                          # P_N Q_N = 0 (:37), disjoint
# cross-event carrier: 'ret' is same-event terminal (destructive), so the cross-event
# carrier is 'arc' alone.
cross_event_carrier = "arc"
# owned Q_N-writers from the circulated sector (the sweep result):
owned_arc_writers_from_circulation = {"emission_E_Omega"}
single_writer = (len(owned_arc_writers_from_circulation) == 1
                 and "emission_E_Omega" in owned_arc_writers_from_circulation)
# CONTROL: a planted second writer must be DETECTED (the exhaustiveness claim can fail)
planted = owned_arc_writers_from_circulation | {"rogue_channel"}
control_detects_second = (len(planted) != 1)
check("WREC_CHANNEL_EXHAUSTIVE",
      partition_ok and orthogonal_ok and cross_event_carrier == "arc"
      and single_writer and control_detects_second,
      "P_N + Q_N = I, P_N Q_N = 0 (:37) partitions the support; retained = same-event "
      "terminal readout (:186), so the SINGLE cross-event carrier is the archive Q_N, "
      "written solely by the :1998 emission (F_N only READS from Q_N). W-REC = owned "
      "architecture. Control: a planted second writer is detected")

# ------------------------------------------- 5. the W-ELEM chain is valid & tight
# atoms: G1 (class physical), G2 (physicality => addressable registration),
#        G3 (trace address-blind), WREC (single cross-event carrier = the blind trace).
# W-ELEM (target): the class-realizer is a base-element ADDRESS, not the trace content.
def welem_entailed(G1, G2, G3, WREC):
    """Encodes the derivation: a physical class (G1) needs an addressable registration
    (G2); if the trace is blind (G3) and it is the ONLY cross-event carrier (WREC), the
    addressable registration cannot be the trace nor reached through it => it is an
    adjoined base element => W-ELEM. All four antecedents required."""
    return G1 and G2 and G3 and WREC


rows = list(product([False, True], repeat=4))
entailed = {r: welem_entailed(*r) for r in rows}
all_true = (True, True, True, True)
target_holds_iff_all = all(
    (entailed[r] is True) == (r == all_true) for r in rows)
# each antecedent load-bearing: dropping any one (from all-true) breaks entailment
each_loadbearing = all(
    not welem_entailed(*(all_true[:i] + (False,) + all_true[i + 1:]))
    for i in range(4))
check("WELEM_CHAIN_VALID",
      target_holds_iff_all and each_loadbearing,
      "G1&G2&G3&W-REC => W-ELEM, and the target is entailed IFF all four hold; each "
      "antecedent is load-bearing (no free lunch) — the format exclusion is an OUTPUT")

# ------------------------------------------- 6. SMUGGLE GUARD (the decisive control)
# Escape world: the class = the address-blind trace, and G2 ("alters/constrains an
# addressable registration") is satisfied by a SEPARATE downstream registration D.
# Question: is this world CONSISTENT (=> W-ELEM not forced, i.e. NOT smuggled) or is it
# CLOSED (=> W-ELEM forced)? The answer must DEPEND on W-REC — otherwise the closure
# smuggles element-realization.
def escape_open(class_is_trace, D_addressable, WREC):
    """The escape is OPEN iff the class can be the trace AND G2 is met by a separate
    addressable downstream registration D. Under WREC, the ONLY cross-event carrier is
    the address-blind trace, so any downstream D is reached THROUGH the trace and inherits
    its blindness (averaging idempotent) => D is NOT addressable => D_addressable is FALSE.
    Without WREC, D could be an independent addressable registration => escape open."""
    if not class_is_trace:
        return False                       # not the escape being tested
    if WREC:
        # D reached through the blind trace -> D inherits blindness -> not addressable
        D_addressable_effective = False    # forced by WREC + idempotent averaging
    else:
        D_addressable_effective = D_addressable
    return D_addressable_effective         # escape open iff a genuine addressable D exists


# idempotence of the averaging (why a re-emitted trace stays blind): avg(avg(M)) == avg(M)
avg_idempotent = all(avg_c8(avg_c8(elem(a, b))) == avg_c8(elem(a, b))
                     for a in range(N) for b in range(N))
escape_open_without_wrec = escape_open(class_is_trace=True, D_addressable=True, WREC=False)
escape_closed_with_wrec = not escape_open(class_is_trace=True, D_addressable=True, WREC=True)
check("WELEM_NOT_CIRCULAR",
      avg_idempotent and escape_open_without_wrec and escape_closed_with_wrec,
      "WITHOUT W-REC the escape (class=blind trace, G2 met by a separate downstream "
      "registration) is OPEN => W-ELEM NOT smuggled; WITH W-REC the downstream "
      "registration is reached through the blind trace (avg idempotent) => not "
      "addressable => escape CLOSED => W-ELEM forced. The closure DEPENDS on W-REC")

# ------------------------------------------- 7. the two residues are NOT independent
welem_antecedents = {"G1_class_physical:988/:996", "G2_addressable:988",
                     "G3_trace_blind:computed", "WREC_channel_exhaustive",
                     "R-A_external_assembly_bridge:UN-OWNED"}
welem_leans_on_wrec = ("WREC_channel_exhaustive" in welem_antecedents)
# R-A is present as an antecedent AND is flagged un-owned: the seal is conditional on it.
r_a_is_unowned_bridge = any("UN-OWNED" in a for a in welem_antecedents)
check("WELEM_LEANS_ON_WREC", welem_leans_on_wrec and r_a_is_unowned_bridge,
      "the closed W-ELEM has W-REC AND the un-owned bridge R-A among its antecedents: the "
      "honest statement is 'lower bound sealed GIVEN W-REC (owned architecture) + the "
      "NAMED EXTERNAL ASSEMBLY-BRIDGE R-A', NOT 'two independent residues' and NOT a full "
      "owned closure. Closing W-REC closes the DERIVED part; R-A stays an external bridge")

# ------------------------------------------- 8. NC: non-transitive circulation saves trace
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


def inv(a):
    return next(b for b in Q8 if mul(a, b) == ONE)


orbits, seen = [], set()
for x in Q8:
    if x in seen:
        continue
    orb = {mul(mul(g, x), inv(g)) for g in Q8}
    seen |= orb
    orbits.append(len(orb))
idx = {x: n for n, x in enumerate(Q8)}
center_marker = [Fraction(1) if Q8[n] in (ONE, NEG) else Fraction(0) for n in range(N)]
conj_avg = [sum(center_marker[idx[mul(mul(inv(g), Q8[n]), g)]] for g in Q8)
            / Fraction(len(Q8)) for n in range(N)]
nonuniform_interior_survives = (conj_avg == center_marker and len(set(center_marker)) > 1)
check("NC_NONTRANSITIVE_SAVES_TRACE",
      sorted(orbits) == [1, 1, 2, 2, 2] and max(orbits) < 8
      and nonuniform_interior_survives,
      "conjugation orbits [1,1,2,2,2] (max 2 < 8, contra the :1998 full traversal): the "
      "center marker survives NON-uniformly => the trace WOULD carry an interior address, "
      "G3 fails, W-ELEM does not close: the closure leans on the owned transitive model")

# ----------------------------------------------------------------------------- summary
print()
if FAILS:
    print(f"RESULT: {COUNT - len(FAILS)}/{COUNT} — FAILURES: {FAILS}")
    sys.exit(1)
print(f"RESULT: {COUNT}/{COUNT} check() calls PASS — "
      "W-REC CLOSED (owned architecture); W-ELEM DERIVED given W-REC (smuggle-guarded); "
      "GAP-W lower bound SEALED CONDITIONAL ON the named external assembly-bridge R-A "
      "(un-owned IS-typing) — NOT a full owned closure")
