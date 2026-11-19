#!/usr/bin/env python3
"""Exact structural checks for finite current/correlation memory.

This checker does not classify a Bloch zero set.  It verifies the finite
combinatorics used by A4D_FINITE_CURRENT_CORRELATION_MEMORY.md:
  * the literal nearest-difference support has 21 shifts;
  * one multiplication by that stencil requires 131 shifts;
  * a Lorentz plaquette/action row has matrix-link degree at most four;
  * the temporal-B scalar transport factor is even while the odd response
    coefficient is odd under t -> -t.
"""
from __future__ import annotations

import sympy as sp

ETA = sp.diag(1, -1, -1, -1)


def check(name, cond):
    if not cond:
        raise AssertionError(name)
    print("PASS_" + name, flush=True)


def support21():
    out = {(0, 0, 0, 0)}
    for r in range(4):
        e = [0] * 4
        e[r] = 1
        out.add(tuple(e))
        e[r] = -1
        out.add(tuple(e))
    for r in range(4):
        for s in range(4):
            if r != s:
                d = [0] * 4
                d[r] = 1
                d[s] = -1
                out.add(tuple(d))
    return out


def total_degree_matrix(M, variables):
    degree = 0
    for x in M:
        p = sp.Poly(sp.expand(x), *variables)
        degree = max(degree, p.total_degree())
    return degree


def face_degree_check():
    # Four independent relative Lorentz matrix increments.  The Lorentz
    # inverse of R=I+U is eta R^T eta, affine-linear in U on the Lorentz
    # constraint manifold.  Degree checking may therefore use that expression
    # directly; no exponential/log chart is involved.
    Us = []
    vars_all = []
    Rs = []
    Rinv = []
    for k in range(4):
        vv = sp.symbols(f"u{k}_0:16")
        vars_all += list(vv)
        U = sp.Matrix(4, 4, vv)
        R = sp.eye(4) + U
        Us.append(U)
        Rs.append(R)
        Rinv.append(ETA * R.T * ETA)

    # Standard plaquette sign pattern +,+,-,-.
    P = Rs[0] * Rs[1] * Rinv[2] * Rinv[3]
    Pinv = Rs[3] * Rs[2] * Rinv[1] * Rinv[0]
    C = (P - Pinv) / 2

    check("PLAQUETTE_DEGREE_AT_MOST_FOUR",
          total_degree_matrix(P, vars_all) <= 4)
    check("INVERSE_PLAQUETTE_DEGREE_AT_MOST_FOUR",
          total_degree_matrix(Pinv, vars_all) <= 4)
    check("ODD_CURVATURE_DEGREE_AT_MOST_FOUR",
          total_degree_matrix(C, vars_all) <= 4)

    # A right-trivialized variation replaces one positive factor by R X.
    # X is constant, so the connection Euler face contribution remains degree 4.
    X = sp.zeros(4)
    X[0, 1] = X[1, 0] = 1
    dP_pos = (Rs[0] * X) * Rs[1] * Rinv[2] * Rinv[3]

    # If the underlying positive link occurs through R^{-1}, right variation
    # gives delta(R^{-1})=-X R^{-1}, again affine-linear in U.
    dP_inv = Rs[0] * Rs[1] * (-X * Rinv[2]) * Rinv[3]
    check("RIGHT_VARIATION_POSITIVE_FACTOR_DEGREE_AT_MOST_FOUR",
          total_degree_matrix(dP_pos, vars_all) <= 4)
    check("RIGHT_VARIATION_INVERSE_FACTOR_DEGREE_AT_MOST_FOUR",
          total_degree_matrix(dP_inv, vars_all) <= 4)

    # Hostile control: multiplying by one genuinely new candidate factor
    # raises the generic total degree to five.  The four-factor incidence is
    # therefore load-bearing in the degree-four statement.
    v5 = sp.symbols("u4_0:16")
    U5 = sp.Matrix(4, 4, v5)
    five = P * (sp.eye(4) + U5)
    check("FIFTH_FACTOR_WOULD_RAISE_DEGREE",
          total_degree_matrix(five, vars_all + list(v5)) == 5)


def boost_parity_check():
    t = sp.symbols("t", real=True)
    # Original flat #227 temporal-B face coefficient and its even transport
    # factor.  z changes sign, c does not.
    z = sp.cancel(4 * t / (4 - 3 * t**2))
    c = sp.cancel((4 + 3 * t**2) / (4 - 3 * t**2))
    check("BOOST_ODD_RESPONSE_COEFFICIENT", sp.cancel(z.subs(t, -t) + z) == 0)
    check("BOOST_EVEN_SCALAR_TRANSPORT_FACTOR", sp.cancel(c.subs(t, -t) - c) == 0)
    check("BOOST_CONSTITUTIVE_HYPERBOLA", sp.cancel(c**2 - 3*z**2 - 1) == 0)


def main():
    sigma = support21()
    check("NEAREST_DIFFERENCE_SUPPORT_SIZE_21", len(sigma) == 21)
    expected = {(0, 0, 0, 0)}
    for r in range(4):
        for sign in (-1, 1):
            d = [0] * 4
            d[r] = sign
            expected.add(tuple(d))
    for r in range(4):
        for s in range(4):
            if r != s:
                d = [0] * 4
                d[r] = 1
                d[s] = -1
                expected.add(tuple(d))
    check("NEAREST_DIFFERENCE_SUPPORT_EXACT", sigma == expected)

    sigma2 = {
        tuple(a[j] + b[j] for j in range(4))
        for a in sigma for b in sigma
    }
    check("ONE_SYMBOL_MULTIPLICATION_SHIFT_CLOSURE_131", len(sigma2) == 131)
    check("DOUBLE_SUPPORT_IS_SIGN_SYMMETRIC",
          all(tuple(-x for x in d) in sigma2 for d in sigma2))

    face_degree_check()
    boost_parity_check()

    print("RESULT A4D-FINITE-CURRENT-CORRELATION-MEMORY-CERTIFIED", flush=True)


if __name__ == "__main__":
    main()
