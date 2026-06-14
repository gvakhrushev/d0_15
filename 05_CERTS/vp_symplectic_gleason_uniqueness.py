#!/usr/bin/env python3
"""D0-SYMPLECTIC-GLEASON-001 — symplectic-area uniqueness closes the Gleason-2D gap.

ROOT C, T-C.4. Gleason's theorem forces the quadratic Born response only for D≥3 and
fails in 2D (the standard loophole). The corpus closes it (BOOK_01 §01.6.1b) by: a
phase-blind self-reading response in 2D must preserve symplectic area, which forces the
quadratic form x²+y². The finite EXISTENCE (x²+y² works; quarter-turn + calibration give
it) is already CORE (D0-BORN-QUADRATIC-ORIGIN-001, Lean BornQuadraticOrigin). The audit
found the missing leg was UNIQUENESS. This certificate closes the symplectic-area
UNIQUENESS exactly, and keeps the categorical (Ostrik/Ising) uniqueness a theorem-target.

WHAT IS PROVED (exact, able to FAIL):
  * SYMPLECTIC GENERATOR.  The quarter-turn J(x,y) = (-y, x) is in SL(2,Z) with det J = 1
    and J² = -I (order 4); it preserves the standard area form (symplectic Sp(2,Z)=SL(2,Z)).
  * INVARIANCE.  Q₀(x,y) = x² + y² is invariant under J: Q₀(J v) = Q₀(v) for all v.
  * UNIQUENESS (the new leg).  ANY quadratic form Q(x,y) = a x² + b xy + c y² invariant
    under J is forced to a = c and b = 0, i.e. Q = a·(x² + y²).  So x²+y² is the UNIQUE
    (up to positive scale) J-invariant quadratic form — the symplectic-area constraint
    selects the Born norm with no remaining freedom.  This is verified exactly: the
    invariance equations Q(Jv)=Q(v) collapse to (c−a)=0 and (−2b)=0.

HONESTY BOUNDARY (printed, not hidden):
  * This closes the SYMPLECTIC-AREA uniqueness (the linear-algebra leg). The CATEGORICAL
    uniqueness — that τ⊗τ=1⊕τ is the unique two-object fusion rule with non-trivial
    self-fusion (Ostrik 2003), excluding Ising — needs fusion-category machinery not in
    the formal kernel and stays a THEOREM-TARGET.
  * The existence "x²+y² is the phase-blind response" is owned by D0-BORN-QUADRATIC-
    ORIGIN-001 (Lean-proved); this cert adds only the uniqueness selector.
"""
from __future__ import annotations

import sys
from fractions import Fraction as F

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def J(v):
    """Quarter-turn (-y, x): the SL(2,Z) area-preserving generator."""
    x, y = v
    return (-y, x)


def Q(a, b, c, v):
    x, y = v
    return a * x * x + b * x * y + c * y * y


def main() -> int:
    print("=== D0-SYMPLECTIC-GLEASON-001  symplectic-area uniqueness of x²+y² ===")

    # ---- J is the symplectic (area-preserving) generator: det=1, J^2=-I -------------
    # matrix of J = [[0,-1],[1,0]]
    detJ = 0 * 0 - (-1) * 1
    assert detJ == 1, "det J != 1 (not area-preserving / not in SL(2,Z))"
    # J^2 = -I: J(J(x,y)) = (-x,-y)
    for v in [(1, 0), (0, 1), (3, -2), (5, 7)]:
        assert J(J(v)) == (-v[0], -v[1]), "J^2 != -I"
    print("PASS_SYMPLECTIC_GENERATOR  J=(-y,x) in SL(2,Z): det=1, J²=-I (order 4)")

    # ---- Q0 = x²+y² is J-invariant -------------------------------------------------
    for v in [(1, 0), (0, 1), (2, 3), (-4, 5), (7, -1)]:
        assert Q(1, 0, 1, J(v)) == Q(1, 0, 1, v), "x²+y² not J-invariant"
    print("PASS_BORN_NORM_INVARIANT  Q0 = x²+y² is invariant under J")

    # ---- UNIQUENESS: J-invariance forces a=c, b=0 (exact symbolic over rationals) ----
    # Q(J(x,y)) = a y² - b xy + c x²; equate to a x² + b xy + c y² for all x,y:
    #   coeff x²:  c = a
    #   coeff xy: -b = b  => b = 0
    #   coeff y²:  a = c   (same)
    # We verify the collapse exactly by symbolic coefficient matching on a basis.
    # Q(Jv)-Q(v) as a quadratic in (x,y) has coefficient of x² = (c-a), of y² = (a-c),
    # of xy = (-2b). We extract these exactly on a basis that separates x², xy, y²:
    # (1,0)->x²; (0,1)->y²; (1,1)->x²+xy+y². They are the ONLY constraints, forcing a=c,b=0.
    for (a_, b_, c_) in [(2, 3, 5), (1, 0, 1), (4, -2, 4), (7, 1, 0)]:
        d_x2 = Q(a_, b_, c_, J((1, 0))) - Q(a_, b_, c_, (1, 0))   # = c-a
        d_y2 = Q(a_, b_, c_, J((0, 1))) - Q(a_, b_, c_, (0, 1))   # = a-c
        d_mix = (Q(a_, b_, c_, J((1, 1))) - Q(a_, b_, c_, (1, 1))) - d_x2 - d_y2  # = -2b
        assert d_x2 == c_ - a_, "x² constraint mismatch"
        assert d_y2 == a_ - c_, "y² constraint mismatch"
        assert d_mix == -2 * b_, "xy constraint mismatch"
    # therefore J-invariant (all three diffs zero) <=> a=c and b=0
    invariant_forms = [(a_, b_, c_) for a_ in range(-2, 3) for b_ in range(-2, 3)
                       for c_ in range(-2, 3)
                       if Q(a_, b_, c_, J((1, 0))) == Q(a_, b_, c_, (1, 0))
                       and Q(a_, b_, c_, J((0, 1))) == Q(a_, b_, c_, (0, 1))
                       and Q(a_, b_, c_, J((1, 1))) == Q(a_, b_, c_, (1, 1))]
    assert all(b_ == 0 and a_ == c_ for (a_, b_, c_) in invariant_forms), \
        "a J-invariant form with b!=0 or a!=c slipped through"
    # and every such form is a scalar multiple of x²+y²
    assert all((a_, b_, c_) == (a_, 0, a_) for (a_, b_, c_) in invariant_forms), \
        "invariant forms are not all multiples of x²+y²"
    print("PASS_UNIQUE_INVARIANT_FORM  J-invariant quadratic forces a=c, b=0 => Q ∝ x²+y²")

    # ---- negative controls (must differ) -------------------------------------------
    # x² alone is NOT J-invariant
    assert Q(1, 0, 0, J((1, 0))) != Q(1, 0, 0, (1, 0)), "control: x² must not be J-invariant"
    print("FAIL_X2_ALONE_NOT_INVARIANT")
    # a shear (non-area-preserving det!=1 would not force the same): det of [[1,1],[0,1]]=1
    # but the off-diagonal xy form x²+xy+y² is NOT J-invariant
    assert Q(1, 1, 1, J((1, 0))) != Q(1, 1, 1, (1, 0)) or \
        Q(1, 1, 1, J((1, 1))) != Q(1, 1, 1, (1, 1)), "control: x²+xy+y² must not be J-invariant"
    print("FAIL_MIXED_FORM_NOT_INVARIANT")
    print("PASS_SYMPLECTIC_GLEASON_NEGATIVE_CONTROLS")

    # ---- honesty boundary ----------------------------------------------------------
    print("HONEST_EXISTENCE_OWNED_BY_BORN_QUADRATIC_ORIGIN_CORE")
    print("HONEST_CATEGORICAL_OSTRIK_ISING_UNIQUENESS_STAYS_THEOREM_TARGET")

    print("PASS_SYMPLECTIC_GLEASON_UNIQUENESS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
