#!/usr/bin/env python3
"""Exact pullback control for the existing three-coin golden-mode price."""

import sympy as sp


def require(name, condition):
    if not condition:
        raise AssertionError(name)


def main():
    x, lam = sp.symbols("x lam", real=True)
    sqrt5 = sp.sqrt(5)
    p = (sqrt5 - 1) / 2
    phi = (1 + sqrt5) / 2
    r = p**3 / 4
    w0 = 4 * p**3

    require("golden_recurrence", sp.simplify(p**2 + p - 1) == 0)
    require("phi_inverse", sp.simplify(phi * p - 1) == 0)
    require("coin_weight", sp.simplify(w0 - (1 - p**6)) == 0)
    require("derived_fugacity", sp.simplify(w0 * r - p**6) == 0)

    G = sp.Matrix([[sp.sqrt(p), -p], [p, sp.sqrt(p)]])
    R = sp.Matrix(
        [[sp.cos(lam * x), -sp.sin(lam * x)],
         [sp.sin(lam * x), sp.cos(lam * x)]]
    )
    U = G * R
    identity = sp.eye(2)
    require("golden_gate_unitarity", sp.simplify(G.T * G - identity) == sp.zeros(2))
    require("rotation_unitarity", sp.trigsimp(R.T * R - identity) == sp.zeros(2))
    require("unitary_field_germ", sp.trigsimp(U.T * U - identity) == sp.zeros(2))

    P = sp.diag(1, 0)
    Q = identity - P
    F = sp.simplify((P * U.T * Q * U * P)[0, 0])
    F0 = sp.simplify(F.subs(x, 0))
    dF0 = sp.simplify(sp.diff(F, x).subs(x, 0))
    require("shared_reference_leakage", sp.simplify(F0 - p**2) == 0)
    require(
        "exact_field_leakage_jet",
        sp.simplify(dF0 - 2 * lam * p * sp.sqrt(p)) == 0,
    )

    # Directly test Book 03's existing feedback component.  Here zeta is its
    # fugacity; 0 < zeta < 1 keeps the log-det domain for every unitary U.
    zeta = sp.symbols("zeta", real=True)
    F_matrix = sp.simplify(P * U.T * Q * U * P)
    S_fb = -sp.log(sp.det(identity - zeta * F_matrix))
    S_fb_base = sp.simplify(S_fb.subs(x, 0))
    S_fb_source = sp.simplify(sp.diff(S_fb, x).subs(x, 0))
    expected_S_fb_source = 2 * lam * zeta * p * sp.sqrt(p) / (1 - zeta * p**2)
    require(
        "book03_feedback_base_operator",
        sp.simplify(F_matrix.subs(x, 0) - p**2 * P) == sp.zeros(2),
    )
    require(
        "book03_feedback_base_price",
        sp.simplify(S_fb_base + sp.log(1 - zeta * p**2)) == 0,
    )
    require(
        "book03_feedback_field_source",
        sp.simplify(S_fb_source - expected_S_fb_source) == 0,
    )
    require(
        "book03_feedback_constant_map_zero_source",
        sp.simplify(S_fb_source.subs(lam, 0)) == 0,
    )
    require(
        "book03_feedback_same_base_distinct_source",
        sp.simplify(S_fb_source.subs(lam, 1)) != 0,
    )
    require(
        "book03_feedback_free_slope_is_response_visible",
        sp.simplify(S_fb_source.subs(lam, 2) - 2 * S_fb_source.subs(lam, 1)) == 0,
    )

    J_r = -sp.log(1 - r * F)
    S_mode = (-2 * sp.log(w0) + 2 * J_r) / sp.log(phi)
    source = sp.simplify(sp.diff(S_mode, x).subs(x, 0))
    expected = lam * p ** sp.Rational(9, 2) / (
        sp.log(phi) * (1 - p**5 / 4)
    )
    require("golden_mode_pullback", sp.simplify(source - expected) == 0)
    require("constant_germ_zero_source", sp.simplify(source.subs(lam, 0)) == 0)
    require(
        "varying_germ_nonzero_source",
        sp.simplify(source.subs(lam, 1)) != 0,
    )

    k0 = sp.simplify(1 - 2 * p**6)
    require("exact_mode_floor", sp.simplify(k0 - (8 * sqrt5 - 17)) == 0)
    margin = sp.simplify(k0**2 - sp.Rational(1, 2))
    exact_margin = (sp.Integer(1217) - 544 * sqrt5) / 2
    require("exact_unique_mode_margin", sp.simplify(margin - exact_margin) == 0)
    require("margin_rational_square_witness", 1217**2 - 5 * 544**2 == 1409)
    require("positive_mode_floor_square_witness", 8**2 * 5 > 17**2)

    print("PASS: U_lambda(0)=G and F_lambda(0)=p^2 for every lambda")
    print("PASS: D F_lambda(0)[K]=2*lambda*p*sqrt(p)")
    print("PASS: Book03 S_fb base is -log(1-zeta*p^2) for every lambda")
    print("PASS: D S_fb(0)[K]=2*lambda*zeta*p^(3/2)/(1-zeta*p^2)")
    print("PASS: same Book03 gate and feedback price admit zero and nonzero kinematic source germs")
    print("PASS: D S_mode(0)[K]=lambda*p^(9/2)/(log(phi)*(1-p^5/4))")
    print("PASS: lambda=0 and lambda=1 give zero and nonzero sources")
    print("PASS: exact unique-mode margin remains strictly above 1/2")
    print("SCOPE: smooth unitary-germ interface; physical D0 admission not proved")


if __name__ == "__main__":
    main()
