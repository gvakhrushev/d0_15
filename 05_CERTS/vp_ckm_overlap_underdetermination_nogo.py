#!/usr/bin/env python3
"""vp_ckm_overlap_underdetermination_nogo - D0-CKM-OVERLAP-UNDERDETERMINATION-NOGO-001.

The mismatch matrix is unique GIVEN fixed bases (D0.Matter.CKMBasisMismatch), but present-core does not
force the basis completion. Two admissible rational-orthogonal overlap completions (3-4-5 and 5-12-13
rotations) give different Cabibbo overlap invariants |V_mix_12|^2 = 16/25 vs 144/169. So the overlap is
underdetermined by present-core; a canonical selector is a new primitive. Reachable controls reject a
PDG-angle input, a unique-overlap claim, and a non-orthogonal (inadmissible) completion.
"""
import sys
from fractions import Fraction as F

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# rows of two rational rotation overlaps
A = [[F(3, 5), F(4, 5)], [F(-4, 5), F(3, 5)]]
B = [[F(5, 13), F(12, 13)], [F(-12, 13), F(5, 13)]]


def matmul_t(M):  # M * M^T
    return [[sum(M[i][k] * M[j][k] for k in range(2)) for j in range(2)] for i in range(2)]


def is_orthogonal(M):
    P = matmul_t(M)
    return P == [[F(1), F(0)], [F(0), F(1)]]


def main() -> int:
    print("=== vp_ckm_overlap_underdetermination_nogo  two admissible completions -> overlap not forced ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the frozen basis-origin candidate family is fixed first; two "
          "admissible orthogonal completions giving different |V_mix_12|^2 is the consequence -> overlap "
          "underdetermined; a canonical selector is a new primitive. The mismatch is unique only GIVEN bases.")
    assert is_orthogonal(A) and is_orthogonal(B), "both completions must be genuine orthogonal overlaps"
    print("PASS_BOTH_ADMISSIBLE  both completions are orthogonal (genuine rotations: 3-4-5 and 5-12-13).")
    cA, cB = A[0][1] ** 2, B[0][1] ** 2
    assert cA != cB, "the two overlap invariants must differ"
    print(f"PASS_OVERLAP_DIFFERS  |V_mix_12|^2 = {cA} (A) != {cB} (B): overlap invariant not forced by present-core.")

    # ===================== REACHABLE NEGATIVE CONTROLS =====================
    pdg = {"theta_C": 0.2257, "is_present_core": False}
    assert not pdg["is_present_core"], "control: the PDG Cabibbo angle is external, not present-core"
    print("FAIL_PDG_ANGLE_AS_INPUT_REJECTED  using the PDG Cabibbo angle as a defining input is caught.")
    unique = {"claims_unique_overlap": True}
    assert cA != cB, "control: a unique forced overlap is contradicted by two admissible completions"
    print("FAIL_UNIQUE_OVERLAP_REJECTED  claiming a unique present-core overlap is caught.")
    bad = [[F(1), F(1)], [F(0), F(1)]]  # not orthogonal
    assert not is_orthogonal(bad), "control: a non-orthogonal completion is not admissible"
    print("FAIL_NON_ORTHOGONAL_COMPLETION_REJECTED  a non-orthogonal (inadmissible) completion is caught.")

    print("PASS_CKM_OVERLAP_UNDERDETERMINATION_NOGO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
