#!/usr/bin/env python3
"""Small exact joint first-slow check, reusing the current finite owners.

No 20-curvature census, small-amplitude search, or nonlinear continuation is
rerun. A single literal face assembly and four-column range solve give the
five-column metric constraint on (d0 z,d1 z,d2 z,d3 z,b_dual).
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp
import a4d_y_curved_response_quotient_check as B
import a4d_y_curved_normaljet_compatibility_check as C

OUT = Path(__file__).with_name("a4d_y_joint_first_slow_injectivity_results.json")


def run(write=False):
    H, labels, faces0 = B.action_connection_hessian(sp.Integer(1))
    N = C.centers(H, labels, sp.Integer(1))
    A1, _A2, M0, M1, _M2, C0, C1, _C2, D = C.blocks_all(H, C.with_base_phases(faces0), labels)
    ny, nd = N[:, :1], N[:, 1:]
    forcing = sp.Matrix.hstack(*[a * ny for a in A1])
    Y = B.bordered_solve(H, N, -forcing)
    C.check("FIRST_SLOW_ALL_CONNECTION_ROWS", H * Y + forcing == sp.zeros(96, 4))
    C.check("FIRST_SLOW_ALL_COKERNEL_ROWS", N.T * forcing == sp.zeros(2, 4))
    C.check("Y_INVISIBLE_DUAL_VISIBLE", C0 * ny == sp.zeros(40, 1) and C0 * nd != sp.zeros(40, 1))
    M = sp.Matrix.hstack(*[C0 * Y[:, i:i+1] + C1[i] * ny for i in range(4)], C0 * nd)
    rows = [0, 1, 2, 4, 14]
    T = M[rows, :]
    expected = sp.Matrix([
        [sp.Rational(x) for x in row] for row in [
            ["625/1281", "-400/3843", "-400/3843", "-400/3843", "0"],
            ["-200/1281", "-9941/1281", "15731/1098", "-49703/7686", "0"],
            ["-200/1281", "-49703/7686", "-9941/1281", "15731/1098", "0"],
            ["-191/1281", "-3407/26901", "71805/23912", "-91115/30744", "1"],
            ["191/1281", "3407/26901", "116003/30744", "-273487/71736", "1"],
        ]])
    C.check("JOINT_FIRST_SLOW_MINOR", T == expected)
    determinant = sp.factor(T.det())
    C.check("JOINT_FIRST_SLOW_RANK5", determinant == -sp.Rational(975737200, 35590023))
    select = sp.zeros(5, 40)
    for i, row in enumerate(rows):
        select[i, row] = 1
    left = T.inv() * select
    C.check("EXACT_JOINT_LEFT_INVERSE", left * M == sp.eye(5))
    inverse_norm_squared = sp.factor(sum(x*x for x in T.inv()))
    C.check("QUANTITATIVE_INJECTIVITY_CONSTANT", 0 < inverse_norm_squared < 64)

    # The restriction does not erase the surviving physical curvature class.
    # g_spatial=-(P_n+exp(2 phi) P_perp), d0 phi=0, sum_i di phi=0.
    q = sp.Matrix([0, 0, 0, 0, -sp.Rational(4, 3), sp.Rational(2, 3),
                   sp.Rational(2, 3), -sp.Rational(4, 3), sp.Rational(2, 3), -sp.Rational(4, 3)])
    P = sp.Matrix.vstack(*[sp.eye(10)] * 4)
    C.check("CONFORMAL_PLANE_FROZEN_LINK_TANGENT_ZERO", M0 * q == sp.zeros(96, 1) and D * P * q == sp.zeros(40, 1))
    beta = sp.Matrix([[0, 1, -1], [-1, 0, 1], [1, -1, 0]])
    for k in (sp.Matrix([1, -1, 0]), sp.Matrix([1, 1, -2])):
        alpha = beta * k / 3
        a = sp.zeros(96, 1)
        for phase in range(4):
            for role in range(1, 4):
                for g, sign in ((3, 1), (4, -1), (5, 1)):
                    a[(phase*4+role)*6+g] = alpha[role-1] * sign
        b1q = -sum((k[i] * M1[i+1] * q for i in range(3)), sp.zeros(96, 1))
        C.check("CONFORMAL_PLANE_FIRST_SLOW_CONNECTION_" + str(list(k)), H*a+b1q == sp.zeros(96, 1))
        C.check("CONFORMAL_PLANE_FIRST_SLOW_METRIC_" + str(list(k)), C0*a == sp.zeros(40, 1))

    result = {
        "schema": "a4d-y-joint-first-slow-injectivity-v1",
        "input_head": "1d257c9902168a0631b6ac601c532e0de1800379",
        "base": "Q=eta, z=1, four real phases, genuine Gram/Lorentz quotient",
        "columns": ["d0_z", "d1_z", "d2_z", "d3_z", "order_h_boost_dual"],
        "full_metric_constraint": C.matrix_json(M),
        "minor_rows_zero_based": rows,
        "minor": C.matrix_json(T),
        "minor_determinant": str(determinant),
        "minor_inverse": C.matrix_json(T.inv()),
        "inverse_frobenius_norm_squared": str(inverse_norm_squared),
        "bound": "||M v||_2 >= ||v||_2 / ||T^-1||_F > ||v||_2/8 for v!=0",
        "joint_conclusion": "At fixed flat metric and raw smooth source O(h^2), a regular leading Y envelope has dz=0 and the order-h visible dual correction vanishes.",
        "symbol_consequence": "The fixed-metric stacked joint derivative has injective first-order center symbol in every nonzero real slow covector. Connection-only hyperbolic symbols are not free joint source-compatible modes.",
        "conformal_control": "For q=-2 phi P_perp, d0 phi=0 and n.grad(phi)=0, dz=b_dual=0 and a_i=(beta grad(phi))_i Y/3 solve all first-slow rows.",
        "nonclaims": ["no global Bloch gap", "no nonlinear exact curved branch", "no z-to-zero uniformity", "no full Einstein-response terminal"],
    }
    if write:
        OUT.write_text(json.dumps(result, indent=2) + "\n")
        print("WROTE", OUT)
    else:
        C.check("JOINT_FIRST_SLOW_RESULTS_MATCH", result == json.loads(OUT.read_text()))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    run(parser.parse_args().write)
