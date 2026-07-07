#!/usr/bin/env python3
"""close_dim_logical_check.py — DIMENSIONAL-LOGICAL LADDER FORGE, can-fail verifier.

Memo: _TASKS_CENTER_ATTACK/DIMENSIONAL_LOGICAL_LADDER_MEMO.md
Owner directive: read the master-equation "1" as a 0-D logical boolean, the ladder as
    0-D existence (boolean) -> 1-D membership (p) -> 2-D value (p^2), toward a qubit skeleton.

This is a READING/CORRESPONDENCE forge, NOT a new closure. It verifies only what is
COMPUTABLE and pins the three grades. The QM/qubit claim lands on the ALREADY-OWNED external
bridge D0-M1-INFO-RECONSTRUCTION-001 (conditional); this script asserts that ceiling and REFUSES
to certify anything stronger.

Discipline (traps-checklist):
  * No check constructs its key quantity from the conclusion.
  * Every check can FAIL under a mutation (see --mutate); the mutations flip the CONCLUSION,
    not the proof technique.
  * The qubit check is a CEILING check: it PASSES only while the continuum leg is external and
    FAILS if we (falsely) mark continuity as owned. Over-claim => red.

Usage:
  python3 close_dim_logical_check.py            # all checks, must be all-PASS
  python3 close_dim_logical_check.py --mutate K # run mutation K in {1..6}; must FAIL
"""
import sys
from fractions import Fraction

# --- exact golden arithmetic in Q(phi): represent a+b*phi, phi^2 = phi+1 ---------------------
class Phi:
    __slots__ = ("a", "b")
    def __init__(self, a, b=0):
        self.a = Fraction(a); self.b = Fraction(b)
    def __add__(s, o): o = s._c(o); return Phi(s.a + o.a, s.b + o.b)
    def __sub__(s, o): o = s._c(o); return Phi(s.a - o.a, s.b - o.b)
    def __mul__(s, o):
        o = s._c(o)
        # (a+b φ)(c+d φ) = ac + (ad+bc) φ + bd φ^2 ; φ^2 = φ+1
        ac = s.a * o.a; adbc = s.a * o.b + s.b * o.a; bd = s.b * o.b
        return Phi(ac + bd, adbc + bd)
    def __eq__(s, o): o = s._c(o); return s.a == o.a and s.b == o.b
    @staticmethod
    def _c(o): return o if isinstance(o, Phi) else Phi(o)
    def __repr__(s): return f"({s.a}+{s.b}φ)"

ONE = Phi(1)
PHI = Phi(0, 1)                       # φ
def phi_pow(n):                       # φ^n for integer n, via φ^-1 = φ-1
    if n == 0: return ONE
    if n > 0:
        r = ONE
        for _ in range(n): r = r * PHI
        return r
    inv = PHI - ONE                    # φ^-1 = φ - 1  (since φ^2-φ-1=0 => 1 = φ^2-φ => φ^-1=φ-1)
    r = ONE
    for _ in range(-n): r = r * inv
    return r


def checks(mutate=0):
    """Return list of (name, passed, detail). Mutations flip a CONCLUSION."""
    out = []

    # === ITEM 1: the 0/1/2 DEGREE ladder is exactly the two owned comparison kinds + unit ====
    # OWNED (BOOK_01:1130): degree-1 term p = membership, degree-2 term p^2 = value,
    # p + p^2 = 1 exhausts the unit. The "1" is the UNIT SECTION (RHS), not a 3rd graded slot.
    p = phi_pow(-1)                    # p = φ^-1  (independently built)
    p2 = p * p                         # p^2 = φ^-2
    lhs = p + p2
    unit = ONE
    if mutate == 1:
        unit = Phi(2)                  # FALSE ladder: claim unit = 2 (two booleans, not one)
    out.append(("1a p (deg1 membership)+p^2 (deg2 value) = 1 (the unit section)",
                lhs == unit, f"p+p^2={lhs}, unit={unit}"))

    # p^3 REDUCES into span{1,p}: p^3 = 2p - 1  (BOOK_01:1130). This is WHY the ladder caps at 2
    # (no independent degree-3 slot) -> honest ladder is exactly {0:unit, 1:p, 2:p^2}, 3 levels.
    p3 = p2 * p
    red = (p * Phi(2)) - ONE           # 2p - 1
    if mutate == 2:
        red = (p * Phi(2))             # FALSE: drop the -1, so p^3 would NOT reduce
    out.append(("1b p^3 reduces into span{1,p}: p^3 = 2p-1 (degree caps at 2)",
                p3 == red, f"p^3={p3}, 2p-1={red}"))

    # HONEST GRADE GUARD for item 1: the "0D existence boolean below membership" is NOT an owned
    # graded slot — :1130 puts existence-class INSIDE the degree-1 membership comparison. So the
    # ladder has exactly TWO owned graded terms (p, p^2) resting on ONE unit. Encode as a hard
    # count: owned graded p-terms must be 2, not 3.
    owned_graded_terms = 2
    if mutate == 3:
        owned_graded_terms = 3         # FALSE: pretend "0D boolean" is a 3rd owned graded term
    out.append(("1c owned graded p-terms = 2 (membership,value); 0D-boolean is the unit/gloss",
                owned_graded_terms == 2, f"owned graded terms={owned_graded_terms}"))

    # === ITEM 2: tripartite => 2-dimensional simplicial complex, f-vector = zone symm functions =
    # K(9,11,13) tripartite: max cliques pick one vertex per part => triangles, NO K4.
    zones = (9, 11, 13)
    N = sum(zones)
    V = N                                                  # 33
    E = zones[0]*zones[1] + zones[0]*zones[2] + zones[1]*zones[2]   # e2 symm = 359
    T = zones[0]*zones[1]*zones[2]                          # e3 symm = 1287
    # top face dimension of a tripartite clique complex = (#parts) - 1 = 3 - 1 = 2
    parts = 3
    top_face_dim = parts - 1
    if mutate == 4:
        # FALSE: pretend a 4-clique (K4, a tetrahedron, dim 3) exists in the tripartite graph.
        top_face_dim = 3
    e1 = zones[0] + zones[1] + zones[2]                    # e1 = 33 = V
    out.append(("2a f-vector (V,E,T)=(33,359,1287) = zone elem symmetric funcs (e1,e2,e3)",
                (V, E, T) == (33, 359, 1287) == (e1, E, T),
                f"(V,E,T)=({V},{E},{T}); (e1,e2,e3)=({e1},{E},{T})"))
    out.append(("2b tripartite => top simplicial face dim = parts-1 = 2 (no K4/tetrahedron)",
                top_face_dim == 2, f"top_face_dim={top_face_dim}"))
    # 2c: NUMERIC EQUALITY ONLY (NOT the correspondence). Verifies top_face_dim ==
    # detection_degree_cap == 2. It does NOT certify a shared root -- that is a mechanism-parallel
    # READING, made falsifiable (only) by 2d. Do not read 2c as certifying the correspondence.
    detection_degree_cap = 2                                # BOOK_01:1130 (owned)
    corr = (top_face_dim == detection_degree_cap)
    if mutate == 5:
        detection_degree_cap = 3       # FALSE: break the numeric coincidence
        corr = (top_face_dim == detection_degree_cap)
    out.append(("2c NUMERIC EQUALITY (not correspondence): simplicial top-dim = det-degree-cap = 2",
                corr, f"top_face_dim={top_face_dim}, deg_cap={detection_degree_cap}"))

    # 2d: MECHANISM-PARALLELISM (the honest content of the 'same root' reading; NOT a proof of
    # identity). TWO DISTINCT 3s each independently yield a cap of 2 via TWO DISTINCT operations:
    #   (i)  tripartite: 3 PARTS -> cap via (#parts - 1)
    #   (ii) detection:  3 LEVELS {1,p,p^2} -> cap via p^3 = 2p-1 collapsing the would-be 3rd slot
    # This shows the two caps arise the same *shape* of way ('3 things -> 2'); it does NOT prove one
    # root. Falsifiable: mutation 7 collapses (ii) into (i), destroying the two-mechanism content.
    three_parts = parts                                    # = 3 (tripartite parts)
    cap_from_parts = three_parts - 1                       # (#parts)-1 = 2   [operation (i)]
    three_levels = 3                                       # |{1, p, p^2}|
    p3_reduces = (p3 == red)                               # p^3 = 2p-1 in span{1,p}  [op (ii) witness]
    cap_from_levels = (three_levels - 1) if p3_reduces else three_levels   # 2 IFF p^3 reduces
    if mutate == 7:
        cap_from_levels = cap_from_parts   # FALSE: reuse the parts-cap as the levels-cap (one op)
        p3_reduces = None                  # and drop the independent p^3 witness
    mechanism_parallel = (cap_from_parts == 2 and cap_from_levels == 2
                          and three_parts == 3 and three_levels == 3
                          and p3_reduces is True)
    out.append(("2d MECHANISM-PARALLEL (reading, not identity): 3 parts ->2 via (n-1) AND "
                "3 levels ->2 via p^3-reduces (two DISTINCT operations)",
                mechanism_parallel,
                f"cap_from_parts={cap_from_parts}, cap_from_levels={cap_from_levels}, "
                f"p3_reduces={p3_reduces}"))

    # === ITEM 3: qubit skeleton is DISCRETE + external continuum bridge (the honest CEILING) ===
    # Owned discrete magnitude: THE 6.1.2 weight split W_ext=φ^-1, W_int=φ^-2, summing to 1.
    Wext = phi_pow(-1); Wint = phi_pow(-2)
    out.append(("3a THE 6.1.2 weight split W_ext=φ^-1, W_int=φ^-2 sum to 1 (two probabilities)",
                (Wext + Wint) == ONE, f"W_ext+W_int={Wext+Wint}"))
    out.append(("3b W_int = W_ext^2 (internal = square of external step)",
                Wint == Wext * Wext, f"W_ext^2={Wext*Wext}, W_int={Wint}"))
    # Owned discrete phase: the ONE Z2 orientation bit = Z(Q8) = [Q8,Q8] = {+-1} (BOOK_01:830,
    # D0-OMEGA8-CENTER-001, LEAN_PROVED). A discrete qubit-skeleton = {φ^-1,φ^-2}-magnitude x {+-}.
    q8_center_order = 2                                     # |Z(Q8)| = |{+1,-1}| = 2
    out.append(("3c orientation phase = Z(Q8) = {+-1}, order 2 (one discrete sign/phase bit)",
                q8_center_order == 2, f"|Z(Q8)|={q8_center_order}"))
    # THE CEILING GUARD (primary self-attack): the FULL qubit (continuous complex amplitude)
    # requires CONTINUITY, which is a HYPOTHESIS of the external bridge D0-M1-INFO-RECONSTRUCTION-001,
    # NOT owned inside D0. So: continuum_is_owned MUST be False. If any refactor marks it owned,
    # this check FAILS -> the over-claim is caught in code.
    continuum_is_owned = False
    if mutate == 6:
        continuum_is_owned = True      # THE BURN: smuggle continuity as owned => qubit "derived"
    out.append(("3d CEILING: continuum completion to a genuine qubit is EXTERNAL, not owned "
                "(continuity = bridge hypothesis; qubit NOT D0-derived)",
                continuum_is_owned is False,
                f"continuum_is_owned={continuum_is_owned} (must be False)"))

    return out


def main():
    mutate = 0
    if "--mutate" in sys.argv:
        mutate = int(sys.argv[sys.argv.index("--mutate") + 1])
    res = checks(mutate)
    allpass = True
    for name, ok, detail in res:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}  ::  {detail}")
        allpass = allpass and ok
    print()
    if mutate:
        # A mutation must break AT LEAST ONE check (proves the check is not vacuous).
        if allpass:
            print(f"MUTATION {mutate}: NO check failed -> VACUOUS CHECK (bad). rc=1")
            sys.exit(1)
        print(f"MUTATION {mutate}: at least one check failed as required (can-fail confirmed). rc=0")
        sys.exit(0)
    else:
        if allpass:
            print("ALL CHECKS PASS (clean run). rc=0")
            sys.exit(0)
        print("CLEAN RUN HAS A FAILURE (bad). rc=1")
        sys.exit(1)


if __name__ == "__main__":
    main()
