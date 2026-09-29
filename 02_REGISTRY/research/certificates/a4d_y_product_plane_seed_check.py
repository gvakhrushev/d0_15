#!/usr/bin/env python3
"""Nonlinear product-plane seed: exact response erasure, exact EK obstruction.

All assertions have finite algebraic scope. The seed is not an exact stationary
branch. Its all-row first-slow check is nonlinear in the conformal factor.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sympy as sp
import a4d_y_slow_exact_plane_check as E

OUT = Path(__file__).with_name("a4d_y_product_plane_seed_results.json")
I = sp.eye(4)
ZERO = sp.zeros(4)
Y = E.GEN[3] - E.GEN[4] + E.GEN[5]
B = E.GEN[0] + E.GEN[1] + E.GEN[2]
P = -Y**2 / 3


def product(items):
    result = (I, ZERO)
    for a, b in items:
        x, y = result
        result = (x*a, x*b+y*a)
    return result


def first_slow_rows(f, g1, g2):
    grad = [0, g1, g2, -g1-g2]
    beta = Y[1:4, 1:4]
    alpha = beta * sp.Matrix(grad[1:]) / (3*f)
    U = E.cayley_simple(Y, 3, sp.Integer(1))
    wave = [U, I, E.linv(U), I]
    S = I + (f-1)*P
    rows0, rows1 = [], []
    origin = (0, 0, 0, 0)

    def link(offset, role, phase):
        return ((wave[(phase+sum(offset)) % 4], ZERO) if role == 0
                else (I, alpha[role-1]*Y))

    for phase in range(4):
        for role in range(4):
            for generator in E.GEN:
                value0 = value1 = sp.Integer(0)
                for a, b in E.PAIRS:
                    if role == a:
                        corners = [(origin, 0), (E.shift(origin, b, -1), 2)]
                    elif role == b:
                        corners = [(E.shift(origin, a, -1), 1), (origin, 3)]
                    else:
                        continue
                    for base, corner in corners:
                        places = [(base, a, False), (E.shift(base, a), b, False),
                                  (E.shift(base, b), a, True), (base, b, True)]
                        factors = []
                        for offset, r, inverse in places:
                            pair = link(offset, r, phase)
                            factors.append(tuple(E.linv(x) for x in pair) if inverse else pair)
                        holonomy = product(factors)
                        inverse = tuple(E.linv(x) for x in holonomy)
                        varied = factors.copy()
                        pair = factors[corner]
                        varied[corner] = (tuple(x*generator for x in pair) if corner < 2
                                          else tuple(-generator*x for x in pair))
                        dp = product(varied)
                        second = product([inverse, dp, inverse])
                        dc = tuple((dp[i]+second[i])/2 for i in range(2))
                        u, v = [j for j in range(4) if j not in (a, b)]
                        dS = sum(grad[j]*base[j] for j in range(4))*P
                        area0 = E.wedge(S[:, u], S[:, v])
                        area1 = E.wedge(dS[:, u], S[:, v]) + E.wedge(S[:, u], dS[:, v])
                        sign = E.orientation(a, b)
                        value0 += sign*(area0.T*E.G2*E.STAR*E.bivector(dc[0]))[0]
                        value1 += sign*(area1.T*E.G2*E.STAR*E.bivector(dc[0])
                                        + area0.T*E.G2*E.STAR*E.bivector(dc[1]))[0]
                rows0.append(sp.factor(value0))
                rows1.append(sp.factor(value1))
    return rows0, rows1


def run(write=False):
    f, z, t = sp.symbols("f z t", real=True, nonzero=True)
    S = I + (f-1)*P
    U = E.cayley_simple(Y, 3, z)
    V = E.cayley_simple(Y, 3, t)
    E.check("PRODUCT_PLANE_PROJECTOR", P*P == P and P.rank() == 2)
    E.check("ROTATION_AND_BOOST_HAVE_DISJOINT_SUPPORT", Y*B == ZERO and B*Y == ZERO)
    E.check("ROTATION_FIXES_DUAL_INSERTION", E.reduced(U*B-B) == ZERO and E.reduced(V*B-B) == ZERO)
    E.check("COMMUTING_SPATIAL_LINKS", E.reduced(U*V-V*U) == ZERO)
    E.check("PRODUCT_GRAM", E.reduced(S.T*E.ETA*S-(E.ETA+(1-f*f)*P)) == ZERO)

    # Every temporal plaquette has the same multiple of Y at a given phase.
    # This tests the unrestricted solder derivative, not a restricted f variation.
    solder_uv = sp.zeros(4)
    dual_face_coefficients = []
    for i in range(1, 4):
        u, v = [j for j in range(4) if j not in (0, i)]
        sign = E.orientation(0, i)
        dual_face_coefficients.append(sp.factor(sign*(E.wedge(S[:, u], S[:, v]).T
                                                      *E.G2*E.STAR*E.bivector(B))[0]))
        for row in range(4):
            for col in (u, v):
                direction = sp.zeros(4)
                direction[row, col] = 1
                area = E.wedge(direction[:, u], S[:, v]) + E.wedge(S[:, u], direction[:, v])
                solder_uv[row, col] += sign*(area.T*E.G2*E.STAR*E.bivector(Y))[0]
    E.check("ALL_16_UV_SOLDER_ROWS_ZERO", E.reduced(solder_uv) == ZERO)
    E.check("EXACT_TIME_DUAL_EULER_WEIGHTS", dual_face_coefficients == [f*f]*3)

    g1, g2 = sp.symbols("g1 g2", real=True)
    zeroth, first = first_slow_rows(f, g1, g2)
    E.check("ALL_96_NONLINEAR_FROZEN_ROWS_ZERO", zeroth == [0]*96)
    E.check("ALL_96_NONLINEAR_FIRST_SLOW_ROWS_ZERO", first == [0]*96)

    # Exact hostile seed on a periodic plane profile. This is not a no-go
    # for the full connection space: order-h^2 transverse corrections matter.
    eps, omega, u, h = sp.symbols("eps omega u h", real=True)
    profile = 1+eps*sp.cos(omega*u)
    curvature_at_peak = sp.factor((-2*sp.diff(sp.log(profile)/2, u, 2)/profile).subs(u, 0))
    residual_at_peak = 2*eps*(1-sp.cos(omega*h))
    E.check("GENUINELY_CURVED_PROFILE", curvature_at_peak == eps*omega**2/(1+eps)**2)
    E.check("SEED_RESIDUAL_NORMALIZED_LIMIT", sp.limit(residual_at_peak/h**2, h, 0) == eps*omega**2)

    # On this nonconstant periodic mode, the shift-row residual is exactly
    # the discrete operator applied to an O(1) correction. This does not
    # assert a uniformly bounded inverse on every mean-zero lattice mode.
    mode = sp.cos(omega*u)
    shift_row_mode = 3*mode-sp.cos(omega*(u-h))-sp.cos(omega*(u+h))-mode
    shift_row_residual = 2*eps*(1-sp.cos(omega*h))*mode
    E.check("SHIFT_ROW_COSINE_SYMBOL", sp.trigsimp(shift_row_mode-2*(1-sp.cos(omega*h))*mode) == 0)
    E.check("SHIFT_ROW_EXACT_MEAN_ZERO_CORRECTION",
            sp.trigsimp(eps*shift_row_mode-shift_row_residual) == 0)

    result = {
        "schema": "a4d-y-product-plane-seed-v1",
        "input_head": "1d257c9902168a0631b6ac601c532e0de1800379",
        "coframe": "S=I+(f-1)P_perp, P_perp=-Y^2/3; f>0, d0 f=0, (d1+d2+d3)f=0",
        "links": "L0=W_p(z); Li=exp(h alpha_i Y), alpha=Y_spatial grad(log f)/3, i=1,2,3",
        "exact_response_identity": "All 16 UV solder rows vanish; E_Q with W_p(z) equals E_Q with L0=I and the same spatial links, site by site, for every h and z in the Cayley chart.",
        "first_slow_scope": "At z=1, all 96 EK coefficients at h^0 and h^1 vanish identically for arbitrary f,g1,g2; no linearization in f is used.",
        "exact_connection_row": "E_(K0,B)(x)=3 f(x)^2 - sum_(i=1)^3 f(x-h e_i)^2, B=K1+K2+K3",
        "periodic_obstruction": "The exact row can vanish at every site of a connected periodic spatial lattice only if f^2 is spatially constant (discrete maximum principle). This excludes only the commuting seed ansatz.",
        "hostile_profile": "f^2=1+eps cos(omega(x1-x2)), |eps|<1",
        "gaussian_curvature_at_peak": str(curvature_at_peak),
        "connection_residual_at_peak": str(residual_at_peak),
        "normalized_residual_limit": "eps*omega^2",
        "shift_row_mode_identity": "L_h cos(omega*(x1-x2))=2*(1-cos(omega*h))*cos(omega*(x1-x2))",
        "shift_row_exact_correction": "for nonconstant allowed periodic modes, L_h^-1 residual=eps*cos(omega*(x1-x2)); this is mode-specific, not a global uniform inverse bound",
        "nonclaims": ["seed is not exactly connection-stationary on nonconstant periodic f", "no restriction of the full connection space to SO(2)", "no nonlinear continuation terminal", "this obstruction does not force z to shrink"]}
    if write:
        OUT.write_text(json.dumps(result, indent=2)+"\n")
        print("WROTE", OUT)
    else:
        E.check("PRODUCT_PLANE_SEED_RESULTS_MATCH", result == json.loads(OUT.read_text()))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    run(parser.parse_args().write)
