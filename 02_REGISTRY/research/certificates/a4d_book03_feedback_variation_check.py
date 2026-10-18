#!/usr/bin/env python3
"""Exact finite controls for the constrained Book 03 feedback variation.

The general identities are proved in
../A4D_NATIVE_BOOK03_OPERATOR_VARIATION_BOUNDARY.md. This checker pins the
Book 01 complement owner and Book 03 feedback owner, then checks the constrained
product rule, complete source, and equal-base/different-source witness. It does
not claim physical field admission.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import sys

import sympy as sp

EXPECTED_BOOK01_SHA256 = (
    "668fc904b0585cc7fd5175babead5225c22051422c9c64e197d7b0d42d225342"
)
EXPECTED_BOOK01_BLOB = "87f3dbd0e5e760d46a577a275aabc16623d3f09e"
EXPECTED_BOOK03_SHA256 = (
    "dfa47d91c4994fa8eea64cda67115590056d8aaf48605daf61a1750aaaf0646d"
)
EXPECTED_BOOK03_BLOB = "ecdd31abb52c94e9f2a157a80c7c49a6f5ac31aa"


def main() -> None:
    root = pathlib.Path(__file__).resolve().parents[3]
    books = {
        "book01": root / "01_BOOKS/BOOK_01_CONDENSED_FOUNDATIONS_AND_GRAPH_BIRTH.md",
        "book03": root / "01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md",
    }
    hashes = {key: hashlib.sha256(path.read_bytes()).hexdigest()
              for key, path in books.items()}
    if hashes["book01"] != EXPECTED_BOOK01_SHA256:
        raise SystemExit(f"Book 01 SHA mismatch: {hashes['book01']}")
    if hashes["book03"] != EXPECTED_BOOK03_SHA256:
        raise SystemExit(f"Book 03 SHA mismatch: {hashes['book03']}")

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
    t, a, c, d, z = sp.symbols("t a c d z", real=True)
    J = sp.Matrix([[0, -1], [1, 0]])
    I2 = sp.eye(2)
    P0 = sp.diag(1, 0)
    Q0 = I2 - P0

    def rot(angle: sp.Expr) -> sp.Matrix:
        return sp.Matrix(
            [[sp.cos(angle), -sp.sin(angle)],
             [sp.sin(angle), sp.cos(angle)]]
        )

    P = rot(a * t) * P0 * rot(-a * t)
    Q = I2 - P
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
    zero("Q_exact_complement", P + Q - I2)
    zero("Q_tangent_is_minus_P_tangent", Qdot + Pdot)
    zero("Q_projector_tangent", Qdot * Q0 + Q0 * Qdot - Qdot)
    zero("unitary_tangent_skew", K.T + K)

    Rdot = U0.T * (Qdot + Q0 * K - K * Q0) * U0
    Fdot_expected = (
        Pdot * R0 * P0 + P0 * Rdot * P0 + P0 * R0 * Pdot
    ).applyfunc(sp.trigsimp)
    zero("constrained_P_U_product_rule", Fdot - Fdot_expected)
    zero("base_feedback_operator", F0 - sp.Rational(1, 2) * P0)
    wrong_sign_Rdot = (
        U0.T * (Qdot + K * Q0 - Q0 * K) * U0
    ).applyfunc(sp.trigsimp)
    nonzero(
        "wrong_unitary_commutator_sign_rejected",
        (Rdot - wrong_sign_Rdot).subs({a: 0, c: 1}),
    )

    A0 = I2 - z * F0
    resolvent = A0.inv()
    source_direct = sp.diff(-sp.log((I2 - zt * F).det()), t).subs(t, 0)
    Pi0 = z * resolvent
    source_expected = (
        z * sp.trace(resolvent * Fdot)
        + d * sp.trace(resolvent * F0)
    )
    zero("full_feedback_source_including_dz", source_direct - source_expected)
    nonzero(
        "dropping_fugacity_leg_rejected",
        (source_direct - z * sp.trace(resolvent * Fdot)).subs(d, 1),
    )

    GP = R0 * P0 * Pi0 + Pi0 * P0 * R0
    GQ = U0 * P0 * Pi0 * P0 * U0.T
    source_by_constrained_gradient = (
        sp.trace((GP - GQ) * Pdot)
        + sp.trace(GQ * (Q0 * K - K * Q0))
        + d * sp.trace(resolvent * F0)
    )
    zero(
        "constrained_gradient_source_identity",
        source_direct - source_by_constrained_gradient,
    )

    V = sp.diag(-1, 1)
    zero("stabilizer_commutes_with_Q", V * Q0 - Q0 * V)
    Ug = V * U0
    Fg = P0 * Ug.T * Q0 * Ug * P0
    zero("finite_Q_stabilizer_redundancy", Fg - F0)

    theta = sp.pi / 4
    ell = sp.symbols("ell", real=True)
    Ubase = rot(theta)
    Fbase = P0 * Ubase.T * Q0 * Ubase * P0
    Ufixed = rot(theta)
    Uslope = rot(theta + ell * t)
    Ffixed = P0 * Ufixed.T * Q0 * Ufixed * P0
    Fslope = P0 * Uslope.T * Q0 * Uslope * P0
    zero("same_base_pullback_operator", Ffixed.subs(t, 0) - Fslope.subs(t, 0))
    Sfixed = -sp.log((I2 - z * Ffixed).det())
    Sslope = -sp.log((I2 - z * Fslope).det())
    fixed_source = sp.diff(Sfixed, t).subs(t, 0)
    slope_source = sp.diff(Sslope, t).subs(t, 0)
    zero("constant_pullback_zero_source", fixed_source)
    zero(
        "arbitrary_complement_preserving_lift_source_exact",
        slope_source - ell * z / (1 - z / 2),
    )
    nonzero("unit_slope_pullback_source_nonzero", slope_source.subs(ell, 1))
    if sp.simplify(Fbase - sp.Rational(1, 2) * P0) != sp.zeros(2):
        raise ArithmeticError("same_base_formula_control")
    checks.append("same_base_formula_control")

    result = {
        "status": "PASS_SCOPED_BOOK03_CONSTRAINED_OPERATOR_VARIATION",
        "checks": checks,
        "check_count": len(checks),
        "book01_sha256": hashes["book01"],
        "book01_git_blob": EXPECTED_BOOK01_BLOB,
        "book03_sha256": hashes["book03"],
        "book03_git_blob": EXPECTED_BOOK03_BLOB,
        "python": sys.version.split()[0],
        "sympy": sp.__version__,
        "native_geometric_pullback_derived": False,
        "full_book_price_closed": False,
        "matter_ward_derived": False,
        "physical_gr_closed": False,
    }
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
