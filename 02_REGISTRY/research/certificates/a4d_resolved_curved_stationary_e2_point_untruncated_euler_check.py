#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=600
"""Untruncated link and solder Euler at (rho,t,p)=(1,0,0).

The connection is the exact Cayley of generators0 + v + X, with the
rational particular amplitude of the affine solution. The coframe is the
§9.23 conformal solder at r=-1, rho=1, t=0. Translations are not varied:
the order-4 affine rows were already measured. This is one modulus point.
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
from pathlib import Path

import sympy as sp


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name, flush=True)


p = Path(__file__).with_name(
    "a4d_resolved_curved_stationary_e2_support7_order1_check.py"
)
spec = importlib.util.spec_from_file_location("support7_order1_owner", p)
owner = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(owner)

R = sp.Rational
rho, t, u = R(1), R(0), R(8, 3)
amp = (R(0), R(0), R(-10, 3), R(-8, 3), R(0), R(4, 9), R(0))
# §9.22 at t=0, kept by §9.23. Lower block from the §9.23 r=-1 solution.
p3, p4, p5, p7 = R(-5, 12), R(-5, 12), R(-1, 3), R(-2, 3)
c, d = R(-3, 2), R(3, 2)
lam = sp.symbols("lam")
K1, N2, N3 = owner.K1, owner.N2, owner.N3
v_roles = [
    -4 * rho * K1 + t * N3,
    t * N3,
    u * K1 - N2,
    N3,
]
x_roles = [sp.zeros(4) for _ in range(4)]
for coeff, (_, role, gen) in zip(amp, owner.SELECTED_SPECS):
    x_roles[role] += coeff * gen
A = [owner.generators0[r] + v_roles[r] + x_roles[r] for r in range(4)]
for r, a in enumerate(A):
    chart = sp.factor((owner.I4 - a / 2).det())
    print("CHART", r, chart, flush=True)
    check(f"ROLE_{r}_CAYLEY_CHART_OPEN", chart != 0)
roles = [owner.cayley(a) for a in A]
for r, U in enumerate(roles):
    check(f"ROLE_{r}_LORENTZ", sp.simplify(U.T * owner.ETA * U - owner.ETA) == sp.zeros(4))

base_roles = list(owner.role0)
base_n2 = owner.d_star(base_roles, owner.generators0, 0, owner.N2)
check("BASE_ROLE0_N2_REPRODUCED", sp.together(base_n2) == -16)


def link_at(theta, role_index, h):
    du = owner.cayley_diff(A[role_index], h)
    coframe = [theta[:, r] for r in range(4)]
    site = 0
    for r, s in owner.PAIRS:
        ur, us = roles[r], roles[s]
        uri, usi = ur.inv(), us.inv()
        dur = du if r == role_index else sp.zeros(4)
        dus = du if s == role_index else sp.zeros(4)
        duri = -uri * dur * uri if r == role_index else sp.zeros(4)
        dusi = -usi * dus * usi if s == role_index else sp.zeros(4)
        hol = ur * us * uri * usi
        dhol = (
            dur * us * uri * usi
            + ur * dus * uri * usi
            + ur * us * duri * usi
            + ur * us * uri * dusi
        )
        dc = owner.bivector_of_tangent(owner.d_curvature(hol, dhol))
        u_ax, v_ax = [i for i in range(4) if i not in (r, s)]
        site += owner.orientation((r, s)) * (
            owner.wedge(coframe[u_ax], coframe[v_ax]).T * owner.G2 * owner.STAR * dc
        )[0]
    return sp.together(sp.expand(16 * site))


def solder_at(theta):
    grad = sp.zeros(4)
    action = 0
    for r, s in owner.PAIRS:
        hol = roles[r] * roles[s] * roles[r].inv() * roles[s].inv()
        pi = owner.ETA * hol.T * owner.ETA
        curv = (hol - pi) / 2
        response = owner.G2 * owner.STAR * owner.bivector_of_tangent(curv)
        u_ax, v_ax = [i for i in range(4) if i not in (r, s)]
        vu, vv = theta[:, u_ax], theta[:, v_ax]
        sign = owner.orientation((r, s))
        action += 16 * sign * (owner.wedge(vu, vv).T * response)[0]
        for a in range(4):
            axis = sp.eye(4)[:, a]
            for b in range(4):
                leg = sp.zeros(6, 1)
                if b == u_ax:
                    leg += owner.wedge(axis, vv)
                if b == v_ax:
                    leg += owner.wedge(vu, axis)
                grad[a, b] += 16 * sign * (leg.T * response)[0]
    return sp.simplify(action), grad.applyfunc(sp.simplify)


T = sp.Matrix(
    [
        [1 + rho + lam, 1 + lam, p3, p4],
        [rho + lam, lam, p3, p4],
        [p5, p5, d, c],
        [p7, p7, -c, d],
    ]
)
check("LEADING_SOLDER_DET", sp.factor(T.det()) == -sp.Rational(9, 2) * rho)

eta_rows = []
for role_index in range(4):
    for name, h in owner.ALL_TESTS:
        val = owner.d_star(roles, A, role_index, h)
        eta_rows.append(sp.together(val))
        if val != 0:
            print("ETA_LINK", role_index, name, val, flush=True)
check("ETA_COFRAME_LINK_EULER_NONZERO", any(val != 0 for val in eta_rows))

chart_rows = []
for role_index in range(4):
    for name, h in owner.ALL_TESTS:
        val = link_at(T, role_index, h)
        chart_rows.append(val)
        if val != 0:
            print("CHART_LINK", role_index, name, val, flush=True)
nonzero_chart = [val for val in chart_rows if val != 0]
check("CHART_SOLDER_LINK_EULER_NONZERO", len(nonzero_chart) > 0)
# Two integer samples show the vector is not identically zero. The constant
# numerator gcd below is what excludes a common lambda root.
for probe in (0, 1):
    vals = [sp.together(val.subs(lam, probe)) for val in nonzero_chart]
    check(f"CHART_LINK_NONZERO_AT_LAMBDA_{probe}", any(v != 0 for v in vals))
def numer_poly(val):
    num, _den = sp.fraction(sp.together(val))
    return sp.Poly(sp.expand(num), lam)
link_gcd = numer_poly(chart_rows[0])
for val in chart_rows[1:]:
    link_gcd = sp.gcd(link_gcd, numer_poly(val))
check("CHART_LINK_GCD_IS_NONZERO_CONSTANT", link_gcd.degree() == 0 and link_gcd.LC() != 0)

action, grad = solder_at(T)
flat = sum(T[i, j] * grad[i, j] for i in range(4) for j in range(4))
check("SOLDER_SCALE_IDENTITY", sp.together(sp.expand(flat - 2 * action)) == 0)
nz_grad = [
    (i, j, sp.together(grad[i, j]))
    for i in range(4)
    for j in range(4)
    if grad[i, j] != 0
]
print("SOLDER_GRAD_NONZERO", nz_grad, flush=True)
check("SOLDER_GRADIENT_NONZERO", len(nz_grad) > 0)
for probe in (0, 1):
    vals = [sp.together(val.subs(lam, probe)) for _, _, val in nz_grad]
    check(f"SOLDER_GRADIENT_NONZERO_AT_LAMBDA_{probe}", any(v != 0 for v in vals))
grad_gcd = numer_poly(grad[0, 0])
for i in range(4):
    for j in range(4):
        if (i, j) == (0, 0):
            continue
        grad_gcd = sp.gcd(grad_gcd, numer_poly(grad[i, j]))
check("SOLDER_GRADIENT_GCD_IS_NONZERO_CONSTANT", grad_gcd.degree() == 0 and grad_gcd.LC() != 0)
witness = sp.together(chart_rows[4].subs(lam, 0))
print("WITNESS_ROLE0_N2_AT_LAMBDA_0", witness, flush=True)
check("WITNESS_ROLE0_N2_LAMBDA0", witness == 16 * R(-7422763) / 11024667)
print("DONE", flush=True)
