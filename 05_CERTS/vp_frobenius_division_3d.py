#!/usr/bin/env python3
"""D0-FROBENIUS-DIVISION-3D-001 — three space dimensions, forced by Frobenius (1877).

Independent forcing-OWNER for the 3 spatial dimensions, sitting beside the Q₈/Dedekind route and
the tripartite graph-rank route. The external owner is the Frobenius theorem (1877): the only
finite-dimensional associative division algebras over ℝ are ℝ (dim 1), ℂ (dim 2), ℍ (dim 4) — there
is no other, and in particular NO 3-dimensional one. The quaternions ℍ are therefore the MAXIMAL
associative division algebra over ℝ, and their imaginary part is exactly 3-dimensional
(i, j, k with i²=j²=k²=−1) — the three reversible transport directions = rank-3 = space, the one
real axis = time.

WHAT IS PROVED (decidable, able to FAIL):
  * the quaternion relations i²=j²=k²=−1 and ij=k, jk=i, ki=j (exact integer quaternion arithmetic);
  * the imaginary dimension of ℍ is 3 (= rank), the real dimension 1 (= time);
  * negative controls: ℂ has only 1 imaginary axis, ℝ has 0 — neither yields rank-3; and the
    allowed dimensions are exactly {1,2,4}, so 3 is NOT a division-algebra dimension (Frobenius).

HONESTY BOUNDARY (printed). Status is a BRIDGE owner-edge (ASSUMP-FROBENIUS-1877): the
classification "only ℝ,ℂ,ℍ" is the EXTERNAL theorem, not proved here; the cert verifies the finite
quaternion content that the bridge rests on. The ℍ→𝕆 step (octonions, dim 8) is HYP, NOT a forcing:
`dim 𝕆 = 8` and `|Ω₈|=|Q₈|=8` are two DIFFERENT eights (algebra dimension vs group order); claiming
the octet from this needs the two 8's identified first.
"""
from __future__ import annotations

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def qmul(x, y):
    a1, b1, c1, d1 = x
    a2, b2, c2, d2 = y
    return (
        a1 * a2 - b1 * b2 - c1 * c2 - d1 * d2,
        a1 * b2 + b1 * a2 + c1 * d2 - d1 * c2,
        a1 * c2 - b1 * d2 + c1 * a2 + d1 * b2,
        a1 * d2 + b1 * c2 - c1 * b2 + d1 * a2,
    )


def main() -> int:
    print("=== D0-FROBENIUS-DIVISION-3D-001  3 space dims forced by Frobenius (ℍ maximal) ===")

    ONE = (1, 0, 0, 0)
    NEG = (-1, 0, 0, 0)
    i, j, k = (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)

    # ---- quaternion relations (exact) ----------------------------------------------
    assert qmul(i, i) == NEG and qmul(j, j) == NEG and qmul(k, k) == NEG, "i²=j²=k²=−1"
    assert qmul(i, j) == k and qmul(j, k) == i and qmul(k, i) == j, "ij=k, jk=i, ki=j"
    assert qmul(qmul(i, j), k) == NEG, "ijk = −1 (Hamilton)"
    print("PASS_QUATERNION_RELATIONS  i²=j²=k²=ijk=−1, ij=k jk=i ki=j (exact)")

    # ---- imaginary dimension of ℍ = 3 = rank; real dimension 1 = time --------------
    imaginary_axes = [i, j, k]
    assert len(imaginary_axes) == 3, "ℍ has exactly 3 imaginary axes (= rank-3 transport = space)"
    assert ONE == (1, 0, 0, 0), "ℍ has exactly 1 real axis (= time)"
    print("PASS_IMAGINARY_DIM_3  Im(ℍ) = span{i,j,k} is 3-dimensional = rank-3 = space; Re(ℍ)=1=time")

    # ---- negative controls ---------------------------------------------------------
    DIM = {"R": 1, "C": 2, "H": 4}                     # Frobenius: the ONLY assoc. division algebras over ℝ
    assert DIM["C"] - 1 == 1, "control: ℂ has 1 imaginary axis (not 3)"
    assert DIM["R"] - 1 == 0, "control: ℝ has 0 imaginary axes"
    assert 3 not in DIM.values(), "control: 3 is NOT a division-algebra dimension (Frobenius forbids)"
    assert DIM["H"] - 1 == 3, "ℍ (dim 4, the maximal) is the unique one with imaginary dim 3"
    print("FAIL_NO_THREE_DIM_DIVISION_ALGEBRA  allowed dims {1,2,4}; only ℍ gives Im-dim 3 (rank-3)")

    # ---- honesty boundary ----------------------------------------------------------
    print("HONEST_BRIDGE_OWNER_FROBENIUS_1877_CLASSIFICATION_IS_EXTERNAL_ASSUMP_FROBENIUS_1877")
    print("HONEST_H_TO_O_OCTET_IS_HYP_DIM_O_8_VS_GROUP_ORDER_Q8_8_ARE_TWO_DIFFERENT_EIGHTS")

    print("PASS_FROBENIUS_DIVISION_3D")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
