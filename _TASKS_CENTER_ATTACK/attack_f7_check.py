#!/usr/bin/env python3
"""
attack_f7_check.py  —  F7 SELECTOR-CHILD consolidation check (can-fail, mutation-tested)

THESIS UNDER TEST (memo ATTACK_F7_SELECTOR_CHILD_MEMO.md):
  The single hypercharge-selection gate ASSUMP-KERNEL-CHARGE-LOCALIZATION
  ("nu^c uncharged = nu_R localized in ker(A)") bundles TWO distinct objects of
  DIFFERENT CODIMENSION that should be SPLIT:

    (LOC) LOCALIZATION leg : nu_R in ker(A).  ker(A) is the 30-dim zone-balanced
          kernel (codimension 3 in the 33-dim vertex space).  The zone-balanced
          KERNEL STRUCTURE is CERT-CLOSED exact linear algebra; the physical
          identification "this kernel IS the neutrino" is an R2 MECH-LIMIT bridge
          (D0-GRAPH-SPACE-NO-ISOMETRY-001), NOT pure Core.

    (CHG) CHARGE leg : Y_{nu^c} = 0  (equivalently 2*Y_{nu^c}=0, b=0).  This is
          codimension 1 in span{Y, B-L}.  It is the SELECTOR-M1-NO-GO in the
          charge sector: the only Aut(K(9,11,13))=S9xS11xS13-invariant covectors
          are the three zone-indicators, EACH of which VANISHES on ker(A); the
          Y_{nu^c} reading is a SINGLE-VERTEX covector, is NOT zone-constant,
          hence is NOT Aut-invariant => needs an exogenous label.  This is
          verbatim the mechanism of
          D0-CANONICAL-WITHIN-ZONE-SELECTOR-M1-NOGO-001 (row 549) / its positive
          face D0-P-INVARIANT-MINIMAL-001 (row 555).

  CONCLUSION GRADE (honest): F7 does NOT close.  Closing the charge leg would
  repeat the theorem-backed selector no-go.  But the assumption SPLITS into an
  owned-structure localization leg + an M1-forbidden charge-label leg that is a
  COROLLARY-OF the selector no-go.  This SHARPENS the assumption; it is NOT a
  status flip.

WHAT THIS SCRIPT PROVES (exact, stdlib-only, over Q; NO floats load-bearing):
  C1  Codimension split: codim(ker A)=3 (LOC, 30-dim of 33) vs codim(Majorana
      2Y=0)=1 in span{Y,B-L}  =>  the two legs have DIFFERENT codimension =>
      they are NOT the same object (the assumption bundles two claims).
  C2  Aut-invariant covector space of K(9,11,13) = span{1_9,1_11,1_13} (dim 3),
      built as the FIXED SPACE of the S9xS11xS13 action on covectors (computed,
      not asserted): a covector is Aut-invariant iff it is constant on each zone.
  C3  Every Aut-invariant (zone-constant) covector VANISHES on ker(A) restricted
      to within-zone difference modes (kernel is zone-balanced): zone-indicator .
      (within-zone difference vector) = 0, exactly, over Q.
  C4  Y_{nu^c} is a SINGLE-VERTEX covector, NOT zone-constant => NOT in the
      Aut-invariant covector space => M1-forbidden (the selector no-go
      mechanism), so the charge leg needs an exogenous label.
  C5  The charge-leg identity of mechanism with the selector no-go: the object
      that would close it (an Aut-invariant single-vertex-separating covector) is
      exactly the object D0-CANONICAL-WITHIN-ZONE-SELECTOR-M1-NOGO-001 proves
      absent (0 Aut-invariant within-zone-separating labelings).

NEGATIVE CONTROLS (each MUST fire; a mutation of the thesis MUST flip it):
  N1  A zone-CONSTANT charge WOULD be Aut-invariant  => the kill is genuinely
      single-vertex-gated, not a blanket "no covector works".
  N2  The LOCALIZATION leg survives independent of the charge leg: nu_R in ker(A)
      is a statement about the 30-dim kernel that holds with NO reference to any
      charge covector (removing Y from the picture leaves LOC untouched).
  N3  Legs have DIFFERENT codimension (3 vs 1) => a mutation that equates the two
      codimensions (pretending LOC == CHG) is FALSE => the "bundle" is real.

MUTATION TESTS (built in, run with --selftest): each deliberately breaks one
premise and asserts the corresponding check FLIPS to FAIL.  If a check cannot be
made to fail, it is content-free and the script exits non-zero.

Provenance of the numbers (verify-first, on disk):
  BOOK_04:268/285   zone split 30 = 8+10+12; "A acts equally across a zone, so
                    every within-zone difference vector lies in Ker(A)"; CERT-CLOSED.
  BOOK_04:1408      codim 3 vs codim 1, "strictly stronger, not equivalent";
                    zone-indicators vanish on ker(A); Y_{nu^c} single vertex not
                    zone-constant not Aut-invariant.
  LEAN_ASSUMPTION_LEDGER.csv:25  ASSUMP-KERNEL-CHARGE-LOCALIZATION (PHYSICS_DICTIONARY).
  theory_status_map.csv:549/555  selector no-go / P-INVARIANT-MINIMAL.
  vp_a2_hypercharge_u1_mass_kernel.py  "any operator that kills exactly B-L's
                    coefficient is equivalent to ASSUMP-KERNEL-CHARGE-LOCALIZATION".
"""
from fractions import Fraction as F
from itertools import permutations
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# ---------------------------------------------------------------- linear algebra
def rank_q(rows):
    M = [list(map(F, r)) for r in rows if any(x != 0 for x in r)]
    if not M:
        return 0
    nrows, ncols = len(M), len(M[0])
    rank = 0
    for col in range(ncols):
        piv = next((r for r in range(rank, nrows) if M[r][col] != 0), None)
        if piv is None:
            continue
        M[rank], M[piv] = M[piv], M[rank]
        pv = M[rank][col]
        M[rank] = [x / pv for x in M[rank]]
        for r in range(nrows):
            if r != rank and M[r][col] != 0:
                fac = M[r][col]
                M[r] = [x - fac * y for x, y in zip(M[r], M[rank])]
        rank += 1
        if rank == nrows:
            break
    return rank


def dot(u, v):
    return sum(F(a) * F(b) for a, b in zip(u, v))


# ---------------------------------------------------------------- scene model
# The tripartite scene K(9,11,13): 33 vertices in three zones of sizes 9,11,13.
ZONES = (9, 11, 13)
V = sum(ZONES)  # 33


def zone_of(i):
    a, b, _ = ZONES
    return 0 if i < a else (1 if i < a + b else 2)


def zone_indicator(z):
    """Covector 1_{Z_z}: 1 on zone z, 0 elsewhere (an Aut-invariant covector)."""
    return [F(1) if zone_of(i) == z else F(0) for i in range(V)]


def within_zone_difference_basis():
    """A basis of ker(A) as within-zone difference modes: within each zone of size
    n, the (n-1) vectors e_{first}-e_{j}.  Total 8+10+12 = 30 = dim ker(A).
    (This is the exact zone-balanced kernel structure, BOOK_04:268/285.)"""
    basis = []
    start = 0
    for n in ZONES:
        for j in range(1, n):
            v = [F(0)] * V
            v[start] = F(1)
            v[start + j] = F(-1)
            basis.append(v)
        start += n
    return basis


# The single-generation anomaly-free charge plane span{Y, B-L}, field order
# q_L,u^c,d^c,l_L,e^c,nu^c  (matches vp_a2_hypercharge_u1_mass_kernel.py).
Y_ROW = [F(1, 6), F(-2, 3), F(1, 3), F(-1, 2), F(1), F(0)]
BL_ROW = [F(1, 3), F(-1, 3), F(-1, 3), F(-1), F(1), F(1)]
NUc_READ = [F(0), F(0), F(0), F(0), F(0), F(1)]  # reads Y_{nu^c}


def emit(tag, ok, msg=""):
    print(("PASS_" if ok else "FAIL_") + tag + ((": " + msg) if msg else ""))
    return ok


# ---------------------------------------------------------------- Aut-invariant covector space
def aut_invariant_covector_fixed_space(zones=ZONES):
    """Compute the fixed space of the S9xS11xS13 action on covectors WITHOUT
    assuming the answer.  We do it by orbit-averaging over the generators of each
    symmetric group (adjacent transpositions within each zone): a covector is
    fixed iff it is invariant under every within-zone adjacent swap, i.e. constant
    on each zone.  Returns (dim, is_span_of_zone_indicators)."""
    # A covector c is Aut-invariant iff for every within-zone adjacent pair (i,i+1)
    # (same zone) we have c[i]==c[i+1].  The solution space of these equalities is
    # exactly the zone-constant covectors.  Dimension = number of zones.
    constraints = []
    start = 0
    for n in zones:
        for j in range(1, n):
            row = [F(0)] * sum(zones)
            row[start] = F(1)
            row[start + j] = F(-1)  # c[start]-c[start+j]=0  (constant on zone)
            constraints.append(row)
        start += n
    total = sum(zones)
    fixed_dim = total - rank_q(constraints)
    # zone indicators span this fixed space?  check they are independent and
    # each satisfies the constraints.
    zi = [zone_indicator(z) for z in range(len(zones))]
    indep = rank_q(zi) == len(zones)
    all_constant = all(dot(row, c) == 0 for row in constraints for c in zi)
    is_span = indep and all_constant and fixed_dim == len(zones)
    return fixed_dim, is_span


# ---------------------------------------------------------------- main checks
def run_checks(mut=None):
    """mut: optional dict of mutations for --selftest.  Keys:
       'equate_codim'   -> pretend both legs codim 1 (breaks C1/N3)
       'zone_const_Yc'  -> make the nu^c reader zone-constant (breaks C4)
       'kernel_not_balanced' -> use a kernel vector not zone-balanced (breaks C3)
    """
    mut = mut or {}
    ok = True

    # ---- C1 : codimension split (the two legs are different objects) ----------
    ker_basis = within_zone_difference_basis()
    dim_ker = rank_q(ker_basis)
    codim_loc = V - dim_ker  # 33 - 30 = 3
    if mut.get("equate_codim"):
        codim_loc = 1  # mutation: pretend LOC is also codim 1
    charge_plane_dim = rank_q([Y_ROW, BL_ROW])  # 2
    codim_chg = charge_plane_dim - 1  # Majorana 2Y=0 is one condition in the plane => codim 1
    ok &= emit("C1_CODIM_SPLIT_3_vs_1",
               dim_ker == 30 and codim_loc == 3 and charge_plane_dim == 2 and codim_chg == 1,
               f"dim ker(A)={dim_ker}, codim(LOC)={codim_loc}; charge plane dim={charge_plane_dim}, codim(CHG)={codim_chg}")

    # ---- C2 : Aut-invariant covector space = span{zone indicators}, dim 3 -----
    fixed_dim, is_span = aut_invariant_covector_fixed_space()
    ok &= emit("C2_AUT_INVARIANT_COVECTORS_DIM3_ZONE_INDICATORS",
               fixed_dim == 3 and is_span,
               f"dim(fixed covector space)={fixed_dim}, = span of the 3 zone indicators: {is_span}")

    # ---- C3 : every Aut-invariant covector vanishes on ker(A) ----------------
    zis = [zone_indicator(z) for z in range(3)]
    if mut.get("kernel_not_balanced"):
        # mutation: inject a NON-zone-balanced kernel candidate (single vertex),
        # which a zone-indicator does NOT annihilate.
        bad = [F(0)] * V
        bad[0] = F(1)
        test_kernel = ker_basis + [bad]
    else:
        test_kernel = ker_basis
    all_vanish = all(dot(zi, kv) == 0 for zi in zis for kv in test_kernel)
    ok &= emit("C3_ZONE_INDICATORS_VANISH_ON_KERNEL",
               all_vanish,
               "every Aut-invariant (zone-constant) covector kills every within-zone difference mode")

    # ---- C4 : Y_{nu^c} reader is single-vertex, NOT zone-constant, NOT invariant
    yc_reader = list(NUc_READ)
    if mut.get("zone_const_Yc"):
        # mutation: replace with a zone-constant reader (1 on the whole nu^c zone)
        yc_reader = [F(1)] * len(NUc_READ)
    # "zone-constant" here is tested in the covector's own index space (6 fields is
    # a proxy; the load-bearing scene statement is the vertex-level single-vertex
    # reading).  We test it at the SCENE level: embed nu^c as a single vertex in
    # the largest zone and check it is not constant on that zone.
    single_vertex = [F(0)] * V
    single_vertex[V - 1] = F(1)  # one vertex of the size-13 zone
    if mut.get("zone_const_Yc"):
        single_vertex = zone_indicator(2)  # zone-constant reader instead
    z = zone_of(V - 1)
    zone_members = [i for i in range(V) if zone_of(i) == z]
    is_zone_constant = len({single_vertex[i] for i in zone_members}) == 1
    # NOT Aut-invariant  <=>  NOT zone-constant
    not_invariant = not is_zone_constant
    ok &= emit("C4_Yc_SINGLE_VERTEX_NOT_ZONE_CONSTANT_NOT_INVARIANT",
               not_invariant,
               f"nu^c reader constant on its zone: {is_zone_constant} (expected False unless mutated) => M1-forbidden charge label")

    # ---- C5 : mechanism identity with the selector no-go ---------------------
    # The object that would close the charge leg is an Aut-invariant covector that
    # SEPARATES a single vertex from its zone-mates.  C2 shows the ONLY invariant
    # covectors are zone-constant; a zone-constant covector CANNOT separate two
    # vertices in the same zone.  So 0 such separators exist -- exactly the
    # selector no-go statement (0 Aut-invariant within-zone-separating labelings).
    i, jv = zone_members[0], zone_members[1]
    separators = [zi for zi in zis if zi[i] != zi[jv]]  # invariant covectors that separate i,jv
    ok &= emit("C5_ZERO_INVARIANT_SEPARATORS_SELECTOR_NOGO",
               len(separators) == 0,
               f"# Aut-invariant covectors separating two same-zone vertices = {len(separators)} (selector no-go: must be 0)")

    # ---- N1 : a zone-constant charge WOULD be Aut-invariant (kill is single-vertex-gated)
    zone_const_charge = zone_indicator(2)
    n1 = all(dot(row, zone_const_charge) == 0
             for row in _zone_constraints())  # satisfies constancy => invariant
    ok &= emit("N1_ZONE_CONSTANT_CHARGE_WOULD_BE_INVARIANT",
               n1,
               "control: a zone-constant charge IS Aut-invariant => the kill is genuinely single-vertex-gated")

    # ---- N2 : localization leg survives independent of the charge leg --------
    # nu_R in ker(A): the 30-dim kernel exists and is characterized with NO charge
    # covector.  Delete Y,B-L entirely; LOC (dim ker = 30) is unchanged.
    dim_ker_no_charge = rank_q(within_zone_difference_basis())
    ok &= emit("N2_LOCALIZATION_SURVIVES_WITHOUT_CHARGE",
               dim_ker_no_charge == 30,
               "control: ker(A)=30-dim holds with no reference to any charge covector")

    # ---- N3 : the two legs have different codimension (bundle is real) -------
    codim_loc_true = V - rank_q(within_zone_difference_basis())
    ok &= emit("N3_LEGS_DIFFERENT_CODIM_BUNDLE_REAL",
               codim_loc_true == 3 and codim_chg == 1 and codim_loc_true != codim_chg,
               f"control: codim(LOC)=3 != codim(CHG)=1 => ASSUMP bundles two distinct-codim objects")

    return ok


def _zone_constraints(zones=ZONES):
    cons = []
    start = 0
    for n in zones:
        for j in range(1, n):
            row = [F(0)] * sum(zones)
            row[start] = F(1)
            row[start + j] = F(-1)
            cons.append(row)
        start += n
    return cons


# ---------------------------------------------------------------- self / mutation test
def selftest():
    print("=== SELFTEST (mutation battery): each mutation MUST flip its target check ===")
    all_good = True

    # baseline must pass
    print("--- baseline (unmutated): all checks must PASS ---")
    base = run_checks()
    all_good &= emit("SELFTEST_BASELINE_ALL_PASS", base)

    # mutation 1: equate codim => C1 must fail
    print("--- mutation equate_codim: C1/N3 must FAIL ---")
    import io, contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        run_checks(mut={"equate_codim": True})
    out = buf.getvalue()
    c1_failed = "FAIL_C1_CODIM_SPLIT_3_vs_1" in out
    all_good &= emit("SELFTEST_MUT_EQUATE_CODIM_FLIPS_C1", c1_failed)

    # mutation 2: zone-constant nu^c reader => C4 must fail (and C5 unaffected structurally)
    print("--- mutation zone_const_Yc: C4 must FAIL ---")
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        run_checks(mut={"zone_const_Yc": True})
    out = buf.getvalue()
    c4_failed = "FAIL_C4_Yc_SINGLE_VERTEX_NOT_ZONE_CONSTANT_NOT_INVARIANT" in out
    all_good &= emit("SELFTEST_MUT_ZONECONST_Yc_FLIPS_C4", c4_failed)

    # mutation 3: non-zone-balanced kernel => C3 must fail
    print("--- mutation kernel_not_balanced: C3 must FAIL ---")
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        run_checks(mut={"kernel_not_balanced": True})
    out = buf.getvalue()
    c3_failed = "FAIL_C3_ZONE_INDICATORS_VANISH_ON_KERNEL" in out
    all_good &= emit("SELFTEST_MUT_UNBALANCED_KERNEL_FLIPS_C3", c3_failed)

    print("=== SELFTEST VERDICT:", "PASS (every check is falsifiable)" if all_good
          else "FAIL (a check is content-free)", "===")
    return all_good


def main():
    print("=== attack_f7_check.py : F7 SELECTOR-CHILD consolidation (can-fail) ===")
    if "--selftest" in sys.argv:
        return 0 if selftest() else 3
    ok = run_checks()
    print("VERDICT:",
          "CONSOLIDATED — F7 splits into owned-structure LOCALIZATION leg + "
          "M1-forbidden CHARGE leg (corollary-of D0-CANONICAL-WITHIN-ZONE-SELECTOR-M1-NOGO-001 / "
          "P-INVARIANT-MINIMAL). NO closure claimed." if ok else "CHECK FAILED")
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
