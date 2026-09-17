#!/usr/bin/env python3
"""D0-GAUGE-MASS-GAP-PLAQUETTE-001 - FINITE D0 gauge excitation floor (NOT continuum Yang-Mills).

In the finite D0 gauge complex, a nontrivial non-abelian seam excitation has strictly positive
constructive cost. Two exact finite witnesses (already Lean-proved, here re-asserted with controls):
  * off-kernel seam gap: frobSq([B, I]) = 0 (commuting), frobSq([B, J]) = 2 > 0 (non-commuting) -- the
    finite non-abelian obstruction gap (D0.Claims.NonabelianSeamGap, native_decide on Z 2x2);
  * step-cost quantum: DeltaS_min = phi^-2 > 0 with phi^-1 + phi^-2 = 1 (D0.Gauge.MassGapCostQuantum).

This is a FINITE D0 mass-gap statement. It is explicitly NOT the classical continuum Yang-Mills mass
gap (the spectral E1-E0 >= c*DeltaS_min over the continuum theory). The continuous-model positive-gap
of D0.Gauge.NonAbelianSeamObstructionGap (which currently proves only seam energy >= 0) stays an OPEN
internal theorem-target, NOT claimed here.

CONSOLIDATION (honest): the finite gap is already CORE/LEAN under D0-NONABELIAN-SEAM-001 +
D0-MASSGAP-COSTQUANTUM-001; this row is the sprint's plaquette-gap statement over those owners.
"""
import sys
from fractions import Fraction as F

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PHI = (1.0 + 5.0 ** 0.5) / 2.0


def comm(A, B):
    # 2x2 commutator [A,B] = AB - BA
    def mm(X, Y):
        return [[X[0][0] * Y[0][0] + X[0][1] * Y[1][0], X[0][0] * Y[0][1] + X[0][1] * Y[1][1]],
                [X[1][0] * Y[0][0] + X[1][1] * Y[1][0], X[1][0] * Y[0][1] + X[1][1] * Y[1][1]]]
    AB, BA = mm(A, B), mm(A, B) if False else mm(B, A)
    AB = mm(A, B)
    return [[AB[i][j] - BA[i][j] for j in range(2)] for i in range(2)]


def frobsq(M):
    return sum(M[i][j] ** 2 for i in range(2) for j in range(2))


def main() -> int:
    print("=== D0-GAUGE-MASS-GAP-PLAQUETTE-001  finite gauge excitation floor (NOT continuum Yang-Mills) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: finite non-abelian seam complex; the excitation cost is the exact "
          "Frobenius commutator energy + the phi^-2 step-cost quantum, fixed before any value")
    I = [[1, 0], [0, 1]]
    B = [[0, 1], [0, 0]]
    J = [[0, 0], [1, 0]]
    # off-kernel gap: commuting -> 0, non-commuting -> 2
    g_comm = frobsq(comm(B, I))
    g_off = frobsq(comm(B, J))
    assert g_comm == 0, f"commuting seam must have zero cost: {g_comm}"
    assert g_off == 2 and g_off > 0, f"off-kernel non-abelian seam must have positive cost 2: {g_off}"
    print(f"PASS_OFFKERNEL_SEAM_GAP  frobSq([B,I])={g_comm} (kernel), frobSq([B,J])={g_off}>0 (finite non-abelian gap)")

    # step-cost quantum DeltaS_min = phi^-2 > 0, with the golden split phi^-1 + phi^-2 = 1
    dS = (F(2), F(-1))   # phi^-2 = 2 - phi
    w_ext = (F(-1), F(1))  # phi^-1
    assert (w_ext[0] + dS[0], w_ext[1] + dS[1]) == (F(1), F(0)), "golden split phi^-1 + phi^-2 = 1 must hold"
    dS_val = 2.0 - PHI
    assert dS_val > 0, "DeltaS_min = phi^-2 must be > 0"
    print(f"PASS_STEPCOST_QUANTUM  DeltaS_min = phi^-2 = {dS_val:.6f} > 0; phi^-1 + phi^-2 = 1 (cost-weight closure)")

    # negative controls
    assert frobsq(comm(I, J)) == 0, "control: identity commutes with everything -> zero cost (trivial vacuum)"
    print("FAIL_TRIVIAL_VACUUM_ZERO_COST  frobSq([I,J])=0 -- the trivial/commuting vacuum has zero cost (the gap is OFF-kernel only)")
    assert dS_val < 1.0, "control: the finite step-cost is sub-unit (NOT a continuum spectral gap E1-E0)"
    print("HONEST_NOT_CONTINUUM_YANG_MILLS  finite excitation floor only; the continuum Yang-Mills mass gap E1-E0>=c*DeltaS_min "
          "is NOT claimed; the NonAbelianSeamObstructionGap continuous-model positive-gap stays an OPEN theorem-target. "
          "Owners: D0-NONABELIAN-SEAM-001 + D0-MASSGAP-COSTQUANTUM-001.")
    print("PASS_GAUGE_MASS_GAP_PLAQUETTE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
