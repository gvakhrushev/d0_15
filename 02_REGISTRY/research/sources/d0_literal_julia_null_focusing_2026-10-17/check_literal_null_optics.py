#!/usr/bin/env python3
"""Exact independent geometry and finite golden port algebra; PR #334.

Inputs are the owner-proved actual first-exit probability and 128-outcome
Kraus port ratio. This script checks new Ricci/null/Euler consequences,
not the native gate admission, price selection or original h^-2 terminal.
"""
import sympy as sp

checks = 0


def require(ok, label):
    global checks
    if not bool(ok):
        raise RuntimeError(label)
    checks += 1


y = sp.symbols("y", real=True)
t, x, z = sp.symbols("t x z", real=True)
scale, beta = sp.symbols("scale beta", positive=True)
theta = sp.Function("theta")(y)
c, s = sp.cos(theta), sp.sin(theta)
eta = sp.diag(1, -1, -1, -1)
e = scale * sp.Matrix([[c, s, 0, 0], [-s, c, 0, 0],
                       [0, 0, 1, 0], [0, 0, 0, 1]])
g = sp.simplify(e.T * eta * e)
gi = sp.simplify(g.inv())
coordinates = (t, x, y, z)
dg = [g.diff(v) for v in coordinates]
Gamma = [[[sp.simplify(sum(gi[a, r] * (dg[b][r, d] +
                dg[d][r, b] - dg[r][b, d]) for r in range(4))/2)
           for d in range(4)] for b in range(4)] for a in range(4)]
Ric = sp.Matrix(4, 4, lambda a, b: sp.simplify(sum(
    sp.diff(Gamma[i][a][b], coordinates[i]) -
    sp.diff(Gamma[i][a][i], coordinates[b]) +
    sum(Gamma[i][i][j] * Gamma[j][a][b] -
        Gamma[i][b][j] * Gamma[j][a][i] for j in range(4))
    for i in range(4))))
dd = sp.diff(theta, y, 2)
d1_sq = sp.diff(theta, y)**2
expected = sp.Matrix([
    [-sp.sin(2*theta)*dd, sp.cos(2*theta)*dd, 0, 0],
    [sp.cos(2*theta)*dd, sp.sin(2*theta)*dd, 0, 0],
    [0, 0, 2*d1_sq, 0],
    [0, 0, 0, 0]])
require(all(sp.simplify(v) == 0 for v in Ric - expected), "full Ricci")
kx = sp.simplify(e.inv() * sp.Matrix([1, 1, 0, 0]))
ky = sp.simplify(e.inv() * sp.Matrix([1, 0, 1, 0]))
require(sp.simplify((kx.T*g*kx)[0]) == 0, "null x")
require(sp.simplify((ky.T*g*ky)[0]) == 0, "null y")
rx = sp.simplify((kx.T*Ric*kx)[0])
ry = sp.simplify((ky.T*Ric*ky)[0])
require(sp.simplify(rx - 2*dd/scale**2) == 0, "Ric x")
require(sp.simplify(ry - 2*d1_sq/scale**2) == 0, "Ric y")

A = 1-sp.exp(-beta/scale**2)
# Owner event: Q_chi(theta)-Q_chi(0) = <A*(theta')^2/(128s^2)>.
rate_density = A*d1_sq/(128*scale**2)
require(sp.simplify(rate_density - A*ry/256) == 0, "optical event")
Etheta = -sp.diff(sp.diff(rate_density, sp.diff(theta, y)), y)
require(sp.simplify(Etheta + A*rx/128) == 0, "optical source")

p = (sp.sqrt(5)-1)/2
require(sp.simplify(p**2+p-1) == 0, "golden normalization")
require(sp.simplify(p-p**2-p**3) == 0, "conditional information gain")
# Arbitrary NONCOMMUTING data operator and faithful normalized preparation.
L = sp.Matrix([[sp.Rational(1, 3), sp.Rational(2, 5)],
               [sp.Rational(1, 7), sp.Rational(1, 2)]])
rho = sp.diag(sp.Rational(2, 3), sp.Rational(1, 3))
q0 = sp.simplify(sp.trace(rho*(p*L).T*(p*L)))
q1 = sp.simplify(sp.trace(rho*(sp.sqrt(p)*L).T*(sp.sqrt(p)*L)))
require(sp.simplify(q1/(q0+q1)-p) == 0, "actual port constant")
r, affine = sp.symbols("r affine", real=True)
pw = p*(1-r*affine**2/2)
q_toy = pw/(pw+p**2)
require(sp.simplify(sp.diff(q_toy, affine, 2).subs(affine, 0)
                    +p**3*r) == 0, "invented area-biased port")
# Real rare-event Shannon has an h^2 log(1/h) coefficient.
h, rate = sp.symbols("h rate", positive=True)
dHdr = sp.log((1-h**2*rate)/(h**2*rate))
require(sp.limit(dHdr/(2*sp.log(1/h)), h, 0, dir="+") == 1,
        "rare-event entropy scale")
require(sp.simplify(Etheta.subs({dd: 0})) == 0, "winding Euler zero")
m = sp.symbols("m", positive=True)
require(sp.simplify(rate_density.subs({sp.diff(theta, y): m})) != 0,
        "winding value nonzero")
print("status=PASS; exact checks=", checks)
print("Ric(k_x,k_x) =", rx)
print("Ric(k_y,k_y) =", ry)
print("port1 given nonblank =", p)
print("subleading occurrence reads <Ric(k_y,k_y)> with A_beta/256")
