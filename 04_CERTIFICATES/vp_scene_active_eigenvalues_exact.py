#!/usr/bin/env python3
"""D0-SCENE-ACTIVE-EIGENVALUES-001 — the two active scene-Laplacian eigenvalues are EXACTLY 3/2 ± √10/40.

BOOK_04 §04.2 reduces the normalized scene Laplacian L_sym(K(9,11,13)) on the part-constant subspace
to the 3×3 operator L_part = I − S, with S_ij = n_j/√(d_i d_j) (i≠j, zero diagonal), n=(9,11,13),
d=(24,22,20). §04.2 gives the two active eigenvalues only as NUMERICAL readouts
(1.420838683198…, 1.579158554151…) and explicitly says "do not cite as proven". This certificate
closes that to an EXACT closed form — and corrects the §04.2 decimals, which are slightly wrong.

EXACT DERIVATION (able to FAIL):
  * tr(S)=0 (zero diagonal); the Perron mode gives eigenvalue μ=1 of S (⇒ L_part eigenvalue 0).
  * The 3×3 zero-diagonal determinant is the sum of the two cyclic products:
        det(S) = S12 S23 S31 + S13 S21 S32 = 2·(9·11·13)/√(528·440·480) = 2·1287/10560 = 39/160,
    where √(528·440·480) = 10560 EXACTLY (10560² = 111 513 600 = 528·440·480).
  * tr(S)=0 ⇒ μ1+μ2 = −1; det(S)=μ1·μ2 (the third eigenvalue is 1) ⇒ μ1 μ2 = 39/160.
  * Active eigenvalues λ = 1−μ: λ1+λ2 = 2−(μ1+μ2) = 3; λ1 λ2 = (1−μ1)(1−μ2) = 2+det(S) = 359/160.
  * So λ1, λ2 are the roots of  160 λ² − 480 λ + 359 = 0,  i.e. λ = 3/2 ± √10/40 (exact in ℚ(√10)):
        160(3/2 ± √10/40)² − 480(3/2 ± √10/40) + 359 = (361 ± 12√10) − (720 ± 12√10) + 359 = 0.

HONESTY / ERROR CORRECTION (printed): §04.2's stated decimals 1.579158554151, 1.420838683198 are
WRONG — they sum to 2.999997… ≠ 3, but the exact eigenvalues must sum to tr(L_part)=3. The correct
values are 3/2 ± √10/40 = 1.57905694…, 1.42094306…. This is an exact theorem (roots of a rational
quadratic with det(S)=39/160), no longer a numerical readout.
"""
from __future__ import annotations

import sys
from fractions import Fraction as F

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

R10 = 10.0 ** 0.5


# exact a + b√10 over Q
def mul(x, y):
    a, b = x; c, d = y
    return (a * c + 10 * b * d, a * d + b * c)


def add(*xs):
    return (sum(x[0] for x in xs), sum(x[1] for x in xs))


def smul(c, x):
    return (c * x[0], c * x[1])


def val(x):
    return float(x[0]) + float(x[1]) * R10


def main() -> int:
    print("=== D0-SCENE-ACTIVE-EIGENVALUES-001  active eigenvalues = 3/2 ± √10/40 (exact) ===")

    n = (9, 11, 13)
    d = (24, 22, 20)

    # radicand 528·440·480 = (d0 d1)(d1 d2)(d0 d2) = (d0 d1 d2)² ⇒ √ = d0 d1 d2 = 10560 exactly
    radicand = (d[0] * d[1]) * (d[1] * d[2]) * (d[0] * d[2])
    assert radicand == 528 * 440 * 480 == 111_513_600, "radicand 528·440·480"
    assert 10560 ** 2 == radicand and 24 * 22 * 20 == 10560, "√(528·440·480) = 10560 = d0 d1 d2"
    print(f"PASS_SQRT_PRODUCT  √(528·440·480) = √{radicand} = 10560 = 24·22·20 (exact)")

    # det(S) = 2·(9·11·13)/10560 = 39/160
    detS = F(2 * (n[0] * n[1] * n[2]), 10560)
    assert detS == F(39, 160), f"det(S) must be 39/160, got {detS}"
    print(f"PASS_DET_S  det(S) = 2·1287/10560 = {detS} = 39/160")

    # active eigenvalues: sum = 3, product = 2 + det(S) = 359/160
    s = F(3)
    p = 2 + detS
    assert p == F(359, 160), f"λ1 λ2 must be 359/160, got {p}"
    print(f"PASS_SUM_PROD  λ1+λ2 = {s} (= tr L_part),  λ1 λ2 = 2+det(S) = {p} = 359/160")

    # quadratic 160 λ² − 480 λ + 359   (= λ² − 3λ + 359/160 scaled)
    # exact roots 3/2 ± √10/40
    lam_plus = (F(3, 2), F(1, 40))    # 3/2 + (1/40)√10
    lam_minus = (F(3, 2), F(-1, 40))  # 3/2 − (1/40)√10
    for lam, tag in [(lam_plus, "+"), (lam_minus, "-")]:
        q = add(smul(160, mul(lam, lam)), smul(-480, lam), (F(359), F(0)))
        assert q == (F(0), F(0)), f"160λ²−480λ+359 must vanish at 3/2{tag}√10/40: {q}"
    print("PASS_EXACT_ROOTS  160λ²−480λ+359 = 0 at λ = 3/2 ± √10/40 (exact in ℚ(√10))")

    # numeric: correct values, and §04.2's stated values are WRONG (sum ≠ 3)
    correct = (val(lam_plus), val(lam_minus))
    stated = (1.579158554151, 1.420838683198)
    assert abs(correct[0] + correct[1] - 3.0) < 1e-12, "exact eigenvalues sum to 3"
    assert abs(stated[0] + stated[1] - 3.0) > 1e-6, "§04.2 stated values do NOT sum to 3 (they are wrong)"
    print(f"PASS_CORRECT_NUMERIC  λ = {correct[0]:.9f}, {correct[1]:.9f} (sum exactly 3)")
    print(f"FAIL_BOOK_DECIMALS_WERE_WRONG  §04.2 stated {stated[0]:.9f}, {stated[1]:.9f} "
          f"(sum {stated[0]+stated[1]:.9f} ≠ 3) — corrected to 3/2 ± √10/40")

    # negative control: a wrong determinant gives a different quadratic / non-vanishing
    bad = add(smul(160, mul(lam_plus, lam_plus)), smul(-480, lam_plus), (F(360), F(0)))  # +360 not +359
    assert bad != (F(0), F(0)), "control: 160λ²−480λ+360 does NOT vanish at 3/2+√10/40"
    print("FAIL_CONTROL_WRONG_CONSTANT_DOES_NOT_VANISH  (359 is forced by det(S)=39/160)")

    print("HONEST_EXACT_CLOSED_FORM_3_HALVES_PLUS_MINUS_SQRT10_OVER_40_REPLACES_NUMERICAL_READOUT")
    print("HONEST_BOOK_04_2_STATED_DECIMALS_WERE_SLIGHTLY_WRONG_NOW_CORRECTED")
    print("PASS_SCENE_ACTIVE_EIGENVALUES")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
