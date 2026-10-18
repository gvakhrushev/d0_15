#!/usr/bin/env python3
"""Exact finite controls for the Book 03 feedback-operator variation.

The general identities are proved in
../A4D_NATIVE_HISTORY_ACTION_BOUNDARY.md. This checker pins the actual
Book 03 owner and checks the full product-rule source, the z derivative,
the (U,Q) representation redundancy, and the two same-base pullbacks.
It does not claim physical field admission.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import sys

import sympy as sp


EXPECTED_BOOK_SHA256 = (
    "dfa47d91c4994fa8eea64cda67115590056d8aaf48605daf61a1750aaaf0646d"
)
EXPECTED_BOOK_BLOB = "ecdd31abb52c94e9f2a157a80c7c49a6f5ac31aa"


def main() -> None:
    root = pathlib.Path(__file__).resolve().parents[3]
    book = root / "01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md"
    book_bytes = book.read_bytes()
    book_sha = hashlib.sha256(book_bytes).hexdigest()
    if book_sha != EXPECTED_BOOK_SHA256:
        raise SystemExit(f"Book 03 SHA mismatch: {book_sha}")

    def zero(name: str, value: sp.Expr | sp.MatrixBase) -> None:
        if isinstance(value, sp.MatrixBase):
            ok = all(sp.trigsimp(sp.simplify(entry)) == 0 for entry in value)
        else:
            ok = sp.trigsimp(sp.simplify(value)) == 0
        if not ok:
            raise ArithmeticError(name)
        checks.append(name)

    def nonzero(name: str, value: sp.Expr | sp.MatrixBase) -> None:
        if isinstance(value, sp.MatrixBase):
            ok = any(sp.trigsimp(sp.simplify(entry)) != 0 for entry in value)
        else:
            ok = sp.trigsimp(sp.simplify(value)) != 0
        if not ok:
            raise ArithmeticError(name)
        checks.append(name)

    checks: list[str] = []
    t, a, b, c, d, z = sp.symbols("t a b c d z", real=True)
    J = sp.Matrix([[0, -1], [1, 0]])
    I2 = sp.eye(2)
    P0 = sp.diag(1, 0)
    Q0 = sp.diag(1, 0)

    def rot(angle: sp.Expr) -> sp.Matrix:
        return sp.Matrix(
            [[sp.cos(angle), -sp.sin(angle)],
             [sp.sin(angle), sp.cos(angle)]]
        )

    P = rot(a * t) * P0 * rot(-a * t)
    Q = rot(b * t) * Q0 * rot(-b * t)
    U = rot(sp.pi / 4 + c * t)
    zt = z + d * t
    F = P * U.T * Q * U * P

    Pdot = P.diff(t).subs(t, 0).applyfunc(sp.trigsimp)
    Qdot = Q.diff(t).subs(t, 0).applyfunc(sp.trigsimp)
    U0 = U.subs(t, 0).applyfunc(sp.trigsimp)
    Udot = U.diff(t).subs(t, 0).applyfunc(sp.trigsimp)
    K = (Udot * U0.T).applyfunc(sp.trigsimp)
    R0 = (U0.T * Q0 * U0).applyfunc(sp.trigsimp)
    F0 = F.subs(t, 0).applyfunc(sp.trigsimp)
    Fdot = F.diff(t).subs(t, 0).applyfunc(sp.trigsimp)

    zero("projector_P_tangent", Pdot * P0 + P0 * Pdot - Pdot)
    zero("projector_P_tangent_hermitian", Pdot.T - Pdot)
    zero("projector_P_tangent_diagonal_blocks",
         P0 * Pdot * P0 + (I2 - P0) * Pdot * (I2 - P0))
    zero("projector_Q_tangent", Qdot * Q0 + Q0 * Qdot - Qdot)
    zero("projector_Q_tangent_hermitian", Qdot.T - Qdot)
    zero("projector_Q_tangent_diagonal_blocks",
         Q0 * Qdot * Q0 + (I2 - Q0) * Qdot * (I2 - Q0))
    zero("unitary_tangent_skew", K.T + K)

    Rdot = U0.T * (Qdot + Q0 * K - K * Q0) * U0
    Fdot_expected = (
        Pdot * R0 * P0 + P0 * Rdot * P0 + P0 * R0 * Pdot
    ).applyfunc(sp.trigsimp)
    zero("full_P_U_Q_product_rule", Fdot - Fdot_expected)
    zero("base_feedback_operator", F0 - sp.Rational(1, 2) * P0)
    wrong_sign_Rdot = (
        U0.T * (Qdot + K * Q0 - Q0 * K) * U0
    ).applyfunc(sp.trigsimp)
    nonzero(
        "wrong_unitary_commutator_sign_rejected",
        (Rdot - wrong_sign_Rdot).subs({a: 0, b: 0, c: 1}),
    )

    A0 = I2 - z * F0
    resolvent = A0.inv()
    source_direct = sp.diff(-sp.log((I2 - zt * F).det()), t).subs(t, 0)
    source_expected = (
        z * sp.trace(resolvent * Fdot)
        + d * sp.trace(resolvent * F0)
    )
    zero("full_feedback_source_including_dz", source_direct - source_expected)
    nonzero(
        "dropping_fugacity_leg_rejected",
        (source_direct - z * sp.trace(resolvent * Fdot)).subs(d, 1),
    )

    V = rot(a)
    Qg = V * Q0 * V.T
    Ug = V * U0
    Fg = P0 * Ug.T * Qg * Ug * P0
    zero("finite_UQ_representation_redundancy", Fg - F0)
    Qg_dot = J * Q0 - Q0 * J
    Ug_dot = J * U0
    Rg_dot = (
        Ug_dot.T * Q0 * U0
        + U0.T * Qg_dot * U0
        + U0.T * Q0 * Ug_dot
    )
    zero("tangent_UQ_redundancy", Rg_dot)

    theta = sp.pi / 4
    Ubase = rot(theta)
    Fbase = P0 * Ubase.T * Q0 * Ubase * P0
    Ufixed = rot(theta)
    Umoving = rot(theta + t)
    Ffixed = P0 * Ufixed.T * Q0 * Ufixed * P0
    Fmoving = P0 * Umoving.T * Q0 * Umoving * P0
    zero("same_base_pullback_operator", Ffixed.subs(t, 0) - Fmoving.subs(t, 0))
    Sfixed = -sp.log((I2 - z * Ffixed).det())
    Smoving = -sp.log((I2 - z * Fmoving).det())
    fixed_source = sp.diff(Sfixed, t).subs(t, 0)
    moving_source = sp.diff(Smoving, t).subs(t, 0)
    zero("constant_pullback_zero_source", fixed_source)
    zero(
        "moving_pullback_nonzero_source_exact",
        moving_source + z / (1 - z / 2),
    )
    if sp.simplify(Fbase - sp.Rational(1, 2) * P0) != sp.zeros(2):
        raise ArithmeticError("same_base_formula_control")
    checks.append("same_base_formula_control")

    result = {
        "status": "PASS_SCOPED_BOOK03_OPERATOR_VARIATION",
        "checks": checks,
        "check_count": len(checks),
        "book03_sha256": book_sha,
        "book03_git_blob": EXPECTED_BOOK_BLOB,
        "python": sys.version.split()[0],
        "sympy": sp.__version__,
        "native_field_map_derived": False,
        "full_book_price_closed": False,
        "matter_ward_derived": False,
        "physical_gr_closed": False,
    }
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
