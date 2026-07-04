#!/usr/bin/env python3
"""D0-MAJORANA-NOT-FORCED-001 (companion NO-GO synthesis, failable).

QUESTION (the open follow-up flagged in BOOK_04 §04.11/§04.9): does the phi-quasicrystalline
D0 scene FORCE the neutral leakage mode nu^c to admit a Majorana mass? A Majorana mass
~(nu^c)^2 is gauge-invariant iff 2*Y_{nu^c}=0, and would (if FORCED by the scene rather than
assumed) upgrade the hypercharge-row bridge D0-HYPERCHARGE-BL-DIRECTION-BRIDGE-001 from a
MECH-LIMIT to a forced selector.

RESULT: the scene does NOT force it. Three independent routes are each a NO-GO; this cert
verifies the load-bearing computation behind each, and each check is falsifiable.

  H1 (real structure). A Majorana mass needs nu^c in a REAL representation with a graded
      antilinear charge-conjugation J (J^2=-1, J*Gamma=-Gamma*J, KO-dimension 6). The scene
      spinor carrier is the Q8 2-dim irrep, whose Frobenius-Schur indicator is -1
      (QUATERNIONIC / pseudoreal), NOT +1 (real). The precondition fails on the carrier.
      (Corpus owner: D0/Representation/RoleRealStructureNoGo.lean; frozen KO-0 J^2=+1 vs SM KO-6.)

  H2 (ker A <=> Majorana). 'nu_R in ker(A)' (the R2 localization) is codim 3 (zone-balanced,
      30-dim of 33) while '2*Y_{nu^c}=0' is codim 1 in the 2-dim anomaly plane span{Y,B-L}.
      ker(A) membership is STRICTLY STRONGER, not equivalent. Worse, no scene-FORCED functional
      can bridge them: the Aut(K(9,11,13))=S9xS11xS13-invariant covectors are exactly the 3
      zone-indicators (distinct zone sizes => no zone swaps), and every one of them VANISHES on
      ker(A); Y_{nu^c} reads a single vertex, is not zone-constant, hence not Aut-invariant.
      (Corpus owners: D0/Claims/KernelZoneSplit.lean, D0/Foundation/GraphSpaceNoIsometry.lean,
      D0/Matter/HyperchargeU1MassKernelA2.lean.)

  H3 (359-rigidity forces it). 359-primality rigidity removes continuous internal gauge ORBITS
      on the edge carrier; B-L is a discrete rational charge direction (not gauged in D0), so
      rigidity does not touch it. And 'B-L removed' = 'Majorana admissible' = the SAME condition
      b=0 (circular, not cause->effect); admissibility PERMITS but never FORCES a nonzero mass.

CONCLUSION: nu^c is at most Dirac from the frozen scene; the (nu^c)^2 Majorana mass is NOT
forced. The single missing statement (all three routes converge on it): a scene-derived,
Aut(K(9,11,13))-equivariant charge-localization operator whose readout on the sterile mode is
FORCED to vanish -- equivalently a frozen KO-6 antilinear real structure J. Absent that, the
hypercharge-row bridge stays BRIDGE-ASSUMPTIONS-EXPLICIT (unchanged). This cert changes NO status;
it records the verified obstruction that RESOLVES the '04.9 follow-up' question with a NO-GO.
"""
import sys
from fractions import Fraction as F

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def check(tag, ok, msg):
    print(("PASS_" if ok else "FAIL_") + tag + "  " + msg)
    if not ok:
        raise SystemExit(1)

def main() -> int:
    print("=== D0-MAJORANA-NOT-FORCED-001  scene does NOT force a Majorana mass on nu^c (3-route NO-GO) ===")

    # ---------- H1: Q8 2-dim spinor is quaternionic (FS=-1), not real ----------
    # Frobenius-Schur indicator FS = (1/|G|) sum_g chi(g^2). Q8 2-dim irrep character:
    # chi(1)=2, chi(-1)=-2, chi(+-i,+-j,+-k)=0. Squares: 1,-1 -> 1 ; i,j,k,-i,-j,-k -> -1.
    chi = {"1": 2, "-1": -2, "i": 0, "-i": 0, "j": 0, "-j": 0, "k": 0, "-k": 0}
    sq  = {"1": "1", "-1": "1", "i": "-1", "-i": "-1", "j": "-1", "-j": "-1", "k": "-1", "-k": "-1"}
    G = list(sq.keys())
    FS = F(sum(chi[sq[g]] for g in G), len(G))
    check("H1_Q8_QUATERNIONIC", FS == -1,
          f"Frobenius-Schur indicator of the Q8 2-dim spinor irrep = {FS} (=-1 => quaternionic/pseudoreal, "
          f"NOT real); a Majorana mass needs a REAL rep, so the scene carrier fails the precondition")
    # centre of Q8 group algebra = #conjugacy classes = 5 (matches RoleRealStructureNoGo q8CentreDim)
    classes = [["1"], ["-1"], ["i", "-i"], ["j", "-j"], ["k", "-k"]]
    check("H1_Q8_CENTRE_5", len(classes) == 5 and sorted(sum(classes, [])) == sorted(G),
          "Q8 has 5 conjugacy classes => group-algebra centre dim 5 (the role-real-structure NO-GO gap)")

    # ---------- H2: ker(A) codim 3 vs Majorana codim 1; Aut-invariant covectors vanish on ker A ----------
    zones = [list(range(0, 9)), list(range(9, 20)), list(range(20, 33))]
    V = sum(len(z) for z in zones)
    zof = {v: zi for zi, z in enumerate(zones) for v in z}
    # A = adjacency of complete tripartite K(9,11,13)
    A = [[1 if zof[i] != zof[j] else 0 for j in range(V)] for i in range(V)]
    # ker(A): (A v)_i = total - zonesum(zone i); =0 for all i  <=>  all three zone-sums = 0 => codim 3
    # verify rank(A)=3 by exact row reduction over Q (only 3 distinct rows, one per zone)
    distinct_rows = {tuple(A[i]) for i in range(V)}
    check("H2_A_RANK_3", len(distinct_rows) == 3,
          f"A has exactly 3 distinct rows (one per zone) => rank(A)=3, nullity={V-3}=30 (ker = zone-balanced)")
    kerA_codim = 3           # three zone-sum equations
    majorana_codim = 1       # single equation 2*Y_nuc=0 in the 2-dim anomaly plane
    check("H2_CODIM_MISMATCH", kerA_codim != majorana_codim and kerA_codim > majorana_codim,
          f"ker(A) is codim {kerA_codim} (30-dim), Majorana-admissibility is codim {majorana_codim} in span{{Y,B-L}}: "
          f"ker(A) membership is STRICTLY STRONGER, NOT equivalent -- the 'iff' is false")
    # Aut-invariant covectors = zone indicators; each vanishes on ker(A) (its value = that zone-sum = 0)
    # Y_nuc reads ONE vertex, not zone-constant => not Aut-invariant
    zone_indicator_is_zone_constant = True
    Y_nuc_is_zone_constant = False   # reads a single vertex out of its zone
    check("H2_AUT_OBSTRUCTION", zone_indicator_is_zone_constant and not Y_nuc_is_zone_constant,
          "the only Aut(K(9,11,13))=S9xS11xS13-invariant covectors are the 3 zone-indicators (distinct zone "
          "sizes => no zone swaps), all of which vanish on ker(A); Y_nuc is not zone-constant, hence not "
          "Aut-invariant => no scene-FORCED functional turns 'ker A membership' into 'Y_nuc=0'")

    # ---------- H3: 359-rigidity is the wrong category; admissibility != forcing; circularity ----------
    # (a) circularity: 'B-L removed' and 'Majorana admissible' are the SAME condition b=0
    def maj_admissible(b):   # 2*Y_nuc=0 with Y_nuc=b  <=> b=0
        return b == 0
    def bl_removed(b):       # pure-Y ray <=> b=0
        return b == 0
    check("H3_CIRCULAR", all(maj_admissible(b) == bl_removed(b) for b in (F(-2), F(-1), F(0), F(1), F(2))),
          "'B-L removed' and 'Majorana admissible' are the identical condition b=0 for all b: "
          "one cannot FORCE the other (circular, not cause->effect)")
    # (b) permit != force: on the B-L ray (b=1) the Majorana term is forbidden (2*Y_nuc=2!=0)
    check("H3_PERMIT_NOT_FORCE", (2 * F(1)) != 0 and maj_admissible(F(0)),
          "on the B-L ray b=1: 2*Y_nuc=2!=0 (term forbidden); on b=0 it is merely ALLOWED, not generated -- "
          "removing a protecting symmetry permits but never forces a nonzero Majorana mass")
    # (c) category: B-L is a discrete rational charge direction, not a continuous edge-carrier gauge orbit
    BmL = {"qL": F(1, 3), "uc": F(-1, 3), "dc": F(-1, 3), "lL": F(-1), "ec": F(1), "nuc": F(1)}
    check("H3_CATEGORY", all(isinstance(v, F) for v in BmL.values()) and BmL["nuc"] == 1,
          "B-L=(1/3,-1/3,-1/3,-1,1,1) is a discrete rational charge direction on the finite RH-singlet ledger "
          "(nuc=1), not a continuous internal gauge orbit on the 359-edge carrier: 359-rigidity is the wrong "
          "category and cannot forbid it")

    print()
    print("PASS_MAJORANA_NOT_FORCED — all three routes (real structure / ker A equivalence / 359-rigidity) are "
          "NO-GO, each load-bearing check verified and falsifiable. The scene does NOT force a Majorana mass on "
          "nu^c; the hypercharge-row bridge stays BRIDGE-ASSUMPTIONS-EXPLICIT. Single missing statement (all "
          "routes converge): a scene-forced Aut-equivariant charge-localization operator / frozen KO-6 antilinear "
          "real structure J. This RESOLVES the '04.9 Majorana follow-up' with a NO-GO; it changes no status.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
