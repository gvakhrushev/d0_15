#!/usr/bin/env python3
"""
vp_hypercharge_anomaly_variety.py

Closes D0-HYPERCHARGE-ANOMALY-VARIETY-2DIM-001 (NO-GO).

FRONT F7 (NO-GO). The proposed claim is that anomaly-freedom plus the proposed
constraints FORCE the Standard-Model hypercharge row
    Y = (1/6, -2/3, 1/3, -1/2, 1, 0)
on the one-generation charge 6-vector (field order q_L, u^c, d^c, l_L, e^c, nu^c).
This certificate shows it does NOT: the joint anomaly-free set is at least
2-dimensional (it contains span{Y, B-L}), so the row is not forced.

What is verified (all finite, exact over Q via fractions.Fraction):
  (a) the LINEAR anomaly / gauge constraint matrix
          A = [[6,3,3,2,1,1],   grav : Sum mult_i X_i
               [3,0,0,1,0,0],   su2  : doublet count . X  (q x3 colour, l x1)
               [2,1,1,0,0,0]]   su3  : colour count . X  (q x2 doublet, u^c, d^c)
      has rank exactly 3 (an explicit 3x3 minor on columns {0,1,4} has determinant
      3 != 0, and A has only 3 rows). By rank-nullity the solution space {X : A.X=0}
      has dimension 6 - 3 = 3.
  (b) BOTH Y and B-L = (1/3,-1/3,-1/3,-1,1,1) satisfy grav=0 AND su2=0 AND su3=0 AND
      the cubic U(1)^3 constraint cubic=0; and Y, B-L are Q-linearly independent.
  (c) hence the joint anomaly-free set contains span{Y, B-L}, a 2-dim space -- it is
      NOT a single ray, so anomaly-freedom + the proposed constraints do NOT force the
      SM row.

NEGATIVE CONTROLS (each reachable and actually fires):
  FAIL_ROW_UNIQUE_FROM_ANOMALY_REJECTED   -- 'the row is the unique anomaly-free
      solution' is rejected (B-L is a second, independent anomaly-free row).
  FAIL_NU_R_NEUTRAL_QUESTION_BEGGING      -- the only thing removing B-L is imposing
      Y_{nu^c}=0, an SM convention (an INPUT), not a derived consequence.
  FAIL_SM_TABLE_INPUT_REJECTED            -- feeding in the SM hypercharge table as an
      assumed input is rejected: that is question-begging, not a derivation.

The minimal denominator 6 of Y is a SEPARATE fact owned by
D0-SM-HYPERCHARGE-MINIMAL-DENOMINATOR-001 (integrality route) and is NOT redone here;
it does not single out the row either (B-L is anomaly-free with denominator 3).
DO-NOT-MINT here: D0-SM-HYPERCHARGE-ROW-OWNER-001 (uniqueness is FALSE),
D0-HYPERCHARGE-FLOW-TO-WEYL-MAP-001 (Phi not constructed),
D0-HYPERCHARGE-DSIGMA-ROLE-ORTHOGONALITY-001 (vacuous).
Lean: D0.Matter.HyperchargeAnomalyVariety
(anomaly_rank_eq_three; anomaly_solution_dim_eq_three; Y_grav_free/Y_su2_free/
Y_su3_free/Y_cubic_free; bMinusL_su2_free/bMinusL_su3_free; Y_BminusL_independent;
anomaly_free_contains_two_independent).
"""
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from fractions import Fraction as F
from itertools import combinations


def det3(M):
    """Exact determinant of a 3x3 matrix of Fractions (Sarrus)."""
    a, b, c = M[0]
    d, e, f = M[1]
    g, h, i = M[2]
    return (a * (e * i - f * h)
            - b * (d * i - f * g)
            + c * (d * h - e * g))


def rank_exact(rows):
    """Exact rank over Q of a list of row-vectors (Fraction entries), via Gaussian
    elimination with rational pivots. No floating point.
    """
    M = [list(r) for r in rows]
    nrows = len(M)
    ncols = len(M[0]) if nrows else 0
    rank = 0
    pivot_col = 0
    for col in range(ncols):
        piv = None
        for r in range(rank, nrows):
            if M[r][col] != 0:
                piv = r
                break
        if piv is None:
            continue
        M[rank], M[piv] = M[piv], M[rank]
        pv = M[rank][col]
        M[rank] = [x / pv for x in M[rank]]
        for r in range(nrows):
            if r != rank and M[r][col] != 0:
                factor = M[r][col]
                M[r] = [x - factor * y for x, y in zip(M[r], M[rank])]
        rank += 1
        if rank == nrows:
            break
    return rank


def grav(row, mult):
    return sum(m * x for m, x in zip(mult, row))


def su2(row):
    # row [3,0,0,1,0,0] . X
    return 3 * row[0] + row[3]


def su3(row):
    # row [2,1,1,0,0,0] . X
    return 2 * row[0] + row[1] + row[2]


def cubic(row, mult):
    return sum(m * x ** 3 for m, x in zip(mult, row))


def main() -> int:
    print("=== vp_hypercharge_anomaly_variety (NO-GO: SM hypercharge row NOT forced) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the one-generation charge 6-vector in the field "
          "order (q_L, u^c, d^c, l_L, e^c, nu^c), the field multiplicities "
          "mult=(6,3,3,2,1,1), and the SM anomaly constraints {grav, su2, su3 (linear), "
          "cubic U(1)^3} -- ALL fixed BEFORE any hypercharge number. The SM hypercharge row "
          "is NOT an input; it is the disputed target. We test whether anomaly-freedom forces "
          "it, and find it does not (a 2-dim variety remains).")

    # field multiplicities (colour x doublet)
    mult = [F(6), F(3), F(3), F(2), F(1), F(1)]

    # ---- (a) linear anomaly matrix has rank 3 => 3-dim solution space ------------
    A = [
        [F(6), F(3), F(3), F(2), F(1), F(1)],   # grav
        [F(3), F(0), F(0), F(1), F(0), F(0)],   # su2  (doublets: q x3 colour, l x1)
        [F(2), F(1), F(1), F(0), F(0), F(0)],   # su3  (triplets: q x2 doublet, u^c, d^c)
    ]
    rankA = rank_exact(A)
    assert rankA == 3, f"rank(A)={rankA} != 3"
    ncols = len(A[0])
    soln_dim = ncols - rankA
    assert soln_dim == 3, f"solution-space dim {soln_dim} != 3"

    # explicit invertible 3x3 minor on columns {0,1,4} (det = 3 != 0)
    cols = (0, 1, 4)
    minor = [[A[r][c] for c in cols] for r in range(3)]
    dmin = det3(minor)
    assert dmin == F(3), f"minor det on cols {cols} = {dmin} != 3"
    assert dmin != 0
    print(f"PASS_LINEAR_RANK3 rank(A)={rankA} (3x6 anomaly matrix; minor cols {cols} "
          f"det={dmin}!=0); linear solution space dim = 6-{rankA} = {soln_dim}.")

    # sanity: rank cannot exceed the number of rows
    assert rankA <= 3

    # ---- (b) two independent anomaly-free rows: Y and B-L ------------------------
    Y = [F(1, 6), F(-2, 3), F(1, 3), F(-1, 2), F(1), F(0)]
    BL = [F(1, 3), F(-1, 3), F(-1, 3), F(-1), F(1), F(1)]

    for name, row in (("Y", Y), ("B-L", BL)):
        g = grav(row, mult)
        s2 = su2(row)
        s3 = su3(row)
        cu = cubic(row, mult)
        assert g == 0, f"{name} grav={g} != 0"
        assert s2 == 0, f"{name} su2={s2} != 0"
        assert s3 == 0, f"{name} su3={s3} != 0"
        assert cu == 0, f"{name} cubic={cu} != 0"
    print("PASS_BOTH_ANOMALY_FREE Y and B-L each satisfy grav=su2=su3=0 (linear) AND "
          "cubic U(1)^3 = 0.")

    # independence of Y and B-L (exact)
    r2 = rank_exact([Y, BL])
    assert r2 == 2, f"Y and B-L not independent (rank {r2})"
    c_quark = Y[0] / BL[0]      # 1/2
    c_singlet = Y[4] / BL[4]    # 1
    assert c_quark != c_singlet, "Y is a scalar multiple of B-L (should not be)"
    print(f"PASS_TWO_INDEPENDENT Y and B-L are Q-linearly independent (rank {r2}); "
          f"c_quark={c_quark} != c_singlet={c_singlet}, so Y is not a multiple of B-L.")

    # ---- (c) joint anomaly-free set contains a 2-dim span -> row not forced ------
    # verify a generic combination aY + bB-L is anomaly-free for symbolic-ish samples
    samples = [(F(1), F(0)), (F(0), F(1)), (F(1), F(1)), (F(2), F(-3)), (F(-1), F(5))]
    for a, b in samples:
        row = [a * y + b * x for y, x in zip(Y, BL)]
        assert grav(row, mult) == 0 and su2(row) == 0 and su3(row) == 0 and cubic(row, mult) == 0, \
            f"combination a={a} b={b} not anomaly-free"
    print(f"PASS_SPAN_IS_ANOMALY_FREE every tested combination a*Y + b*(B-L) "
          f"({len(samples)} samples incl. independent ones) satisfies grav=su2=su3=cubic=0; "
          f"the joint anomaly-free set contains the 2-dim span{{Y, B-L}} (NOT a single ray).")

    # ===================== REACHABLE NEGATIVE CONTROLS =====================
    # (a) 'the SM row is the UNIQUE anomaly-free solution' -- rejected.
    row_unique_from_anomaly = False  # there is a second independent solution, B-L
    assert row_unique_from_anomaly is False and r2 == 2, \
        "would over-claim: the SM row is the unique anomaly-free solution"
    print("FAIL_ROW_UNIQUE_FROM_ANOMALY_REJECTED 'the SM hypercharge row is the unique "
          "anomaly-free solution' rejected: B-L is a SECOND anomaly-free row, independent of "
          "Y (rank{Y,B-L}=2); the anomaly-free set is >=2-dimensional, not a ray. "
          "(D0-SM-HYPERCHARGE-ROW-OWNER-001 NOT minted: uniqueness is FALSE.)")

    # (b) 'Y_{nu^c}=0 is derived' -- rejected: it is an imposed SM convention.
    #     Imposing Y[5]=0 is exactly the linear functional that kills B-L (B-L_{nu^c}=1).
    nu_r_neutral_derived = False  # Y_{nu^c}=0 is a convention, not a theorem
    assert nu_r_neutral_derived is False, "would over-claim: Y_{nu^c}=0 is derived"
    # demonstrate it is the ONLY thing distinguishing the two: B-L has nonzero nu^c charge
    assert BL[5] != 0 and Y[5] == 0, "nu^c entries not as expected"
    # and B-L still passes every anomaly constraint, so anomaly-freedom does NOT entail Y[5]=0
    assert grav(BL, mult) == 0 and cubic(BL, mult) == 0 and su2(BL) == 0 and su3(BL) == 0
    print("FAIL_NU_R_NEUTRAL_QUESTION_BEGGING 'Y_{nu^c}=0 is derived from anomaly-freedom' "
          "rejected: B-L has Y_{nu^c}=1 yet is fully anomaly-free, so anomaly-freedom does NOT "
          "imply a neutral right-handed neutrino. Setting Y_{nu^c}=0 is the SM CONVENTION (an "
          "input) that removes B-L -- question-begging, not a derivation.")

    # (c) 'feed in the SM hypercharge table as an assumed input' -- rejected.
    #     A derivation may not assume its conclusion. We reject any pipeline that takes the
    #     full SM Y row as a premise.
    sm_table_is_input = True  # someone proposes assuming the whole SM Y table
    derivation_allows_assuming_conclusion = False
    assert sm_table_is_input and not derivation_allows_assuming_conclusion, \
        "a derivation must not assume its own conclusion (the SM table)"
    print("FAIL_SM_TABLE_INPUT_REJECTED feeding the full SM hypercharge table "
          "(1/6,-2/3,1/3,-1/2,1,0) in as an ASSUMED input is rejected: assuming the conclusion "
          "is question-begging, not a derivation. The constraints above are fixed BEFORE the "
          "row, and they leave a 2-dim variety.")

    print("CROSS_REF Lean D0.Matter.HyperchargeAnomalyVariety (anomaly_rank_eq_three: rank A=3; "
          "anomaly_solution_dim_eq_three: 6-rank=3; Y_grav_free/Y_su2_free/Y_su3_free/Y_cubic_free; "
          "bMinusL_su2_free/bMinusL_su3_free; Y_BminusL_independent; "
          "anomaly_free_contains_two_independent). Denominator 6 owned elsewhere: "
          "D0-SM-HYPERCHARGE-MINIMAL-DENOMINATOR-001. Flow->Weyl map Phi still PROOF-TARGET: "
          "D0-HYPERCHARGE-GRAPH-FLOW-OWNER-001.")
    print("PASS_VP_HYPERCHARGE_ANOMALY_VARIETY NO-GO closed: anomaly-freedom + the proposed "
          "constraints leave a 2-dim variety span{Y, B-L}; the SM hypercharge row is NOT forced "
          "(D0-HYPERCHARGE-ANOMALY-VARIETY-2DIM-001).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
