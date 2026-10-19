#!/usr/bin/env python3
"""Exact small-matrix consumer of the pre-owned Y period-4 L2/M2 certificate.

Scope: 96 link x 40 Gram first Hessian at the FLAT periodic solder.
No native D0 full Cost-Info, finite diffeomorphism gauge, continuum GR,
nonlinear Y lift, physical matter source, or h-uniform refinement claim.
"""
from __future__ import annotations
import json
from pathlib import Path
import sympy as s

SOURCE = (Path(__file__).resolve().parents[2] / "certificates"
          / "a4d_y_slow_joint_cross_matrices.json")
j = json.loads(SOURCE.read_text())
assert j["schema"] == 1
L = s.Matrix([[int(a) for a in row] for row in j["L2"]])
M = s.Matrix([[int(a) for a in row] for row in j["M2"]])
assert L.shape == (96, 96) and M.shape == (40, 96)
assert L == L.T
assert j["ranks"]["L0"] == 80
assert j["ranks"]["M0_stacked_L0"] == 88

def embed(profile, dim):
    return s.kronecker_product(s.Matrix(profile), s.eye(dim))

profiles = {"zero": [[1,1,1,1]],
            "alternate": [[1,-1,1,-1]],
            "quarter": [[1,0,-1,0], [0,1,0,-1]]}
assert embed([1,1,1,1], 10).T * M == s.zeros(10, 96)
mode = {}
for name, ps in profiles.items():
    C = s.Matrix.hstack(*[embed(x,24) for x in ps])
    G = s.Matrix.hstack(*[embed(x,10) for x in ps])
    l = C.T * L * C
    m = G.T * M * C
    data = (l.rank(), m.rank(), s.Matrix.vstack(l, m).rank())
    mode[name] = (l, m, data)
    print("MODE", name, "link_dims", l.cols, "ranks(L,M,stack)", data)

assert mode["zero"][2] == (24, 0, 24)
assert mode["alternate"][2] == (24, 9, 24)
assert mode["quarter"][2] == (32, 18, 40)
assert sum(mode[x][2][0] for x in profiles) == 80
assert sum(mode[x][2][2] for x in profiles) == 88

# Check all distinct mode blocks are orthogonal under BOTH exact owner maps.
keys = list(profiles)
for i, a in enumerate(keys):
    for b in keys[i+1:]:
        Ca = s.Matrix.hstack(*[embed(x,24) for x in profiles[a]])
        Cb = s.Matrix.hstack(*[embed(x,24) for x in profiles[b]])
        Ga = s.Matrix.hstack(*[embed(x,10) for x in profiles[a]])
        assert Ca.T * L * Cb == s.zeros(Ca.cols, Cb.cols)
        assert Ga.T * M * Cb == s.zeros(Ga.cols, Cb.cols)

Lq, Mq, _ = mode["quarter"]
K = s.Matrix.hstack(*Lq.nullspace())
assert K.shape == (48,16)
R = Mq * K
assert R.rank() == 8

# Ten Gram coordinates: 00,01,02,03,11,12,13,22,23,33.
C4 = s.Matrix([
    [1,0,0,-2, 0,-1, 1,0, 1,0],
    [0,1,0,-1, 0,-1, 0,0, 1,0],
    [0,0,1,-1, 0,-1, 1,0, 0,0],
    [0,0,0, 0, 1,-1,-1,1,-1,1],
])
C8 = s.diag(C4, C4)
assert C8.shape == (8,20) and C8.rank() == 8
assert s.Matrix.vstack(R.T, C8).rank() == 8

coords = [(a,b) for a in range(4) for b in range(a,4)]
k = [1,1,1,1]
D = s.Matrix([[(k[a] if b==mu else 0) +
               (k[b] if a==mu else 0) for mu in range(4)]
              for a,b in coords])
assert D.rank() == 4 and C4*D == s.zeros(4,4)
def pack(X):
    return s.Matrix([X[a,b] for a,b in coords])
E1 = s.diag(0,1,-1,0)
E2 = s.diag(0,1,1,-2)
assert C4 * pack(E1) == s.zeros(4,1)
assert C4 * pack(E2) == s.zeros(4,1)
assert s.Matrix.hstack(D, pack(E1), pack(E2)).rank() == 6
assert 10-C4.rank() == 6

# Direct standard Einstein symbol (formal k=(1,1,1,1) comparison).
eta = s.diag(1,-1,-1,-1)
kcov = s.Matrix(k)
kup = eta * kcov
ksq = (kcov.T*kup)[0]
def linear_einstein(X):
    tr = s.trace(eta * X)
    xx = (kup.T * X * kup)[0]
    Z = s.zeros(4)
    for a in range(4):
        for b in range(4):
            vals = sum(kcov[a]*kup[c]*X[b,c] +
                       kcov[b]*kup[c]*X[a,c] for c in range(4))
            Z[a,b] = s.Rational(1,2) * (
                vals - ksq*X[a,b] - kcov[a]*kcov[b]*tr
                - eta[a,b]*(xx-ksq*tr))
    upper = eta * Z * eta
    return s.Matrix([upper[a,b] * (2 if a != b else 1)
                     for a,b in coords])
def sym_basis(a,b):
    X = s.zeros(4)
    X[a,b] = X[b,a] = 1
    return X
GE = s.Matrix.hstack(*[linear_einstein(sym_basis(a,b))
                      for a,b in coords])
assert GE.rank() == 6 and GE * D == s.zeros(10,4)
P = s.zeros(4,10)
for a in (0,1,2,5):
    P[0,a] = -1
    P[1,a] = -1
    P[2,a] = -1
P[1,7] = -1
P[2,4] = -1
P[3,0] = 1
assert P*GE == C4

# Hostile controls: the 2 shear representatives are NOT generic TT waves.
u = s.Matrix([0,1,-1,0])
v = s.Matrix([0,1,1,-2])
TTplus = 3*u*u.T - v*v.T
TTcross = u*v.T + v*u.T
assert C4*pack(TTplus) != s.zeros(4,1)
assert C4*pack(TTcross) != s.zeros(4,1)
assert C4*pack(eta) != s.zeros(4,1)

# A surviving shear can have zero on-restriction quadratic Einstein action
# while the full Euler vector remains nonzero: zero action != on-shell.
SHEAR = s.Matrix.hstack(pack(E1), pack(E2))
assert SHEAR.T*GE*SHEAR == s.zeros(2,2)
assert (GE*SHEAR).rank() == 2

print("PASS: exact 96-link modes 24/24/48 and 40 Gram readout")
print("PASS: all 16 resonant connection nulls confined to quarter-wave")
print("PASS: eight Fredholm forms = four per real quadrature")
print("PASS: each 10D quarter-Gram compatible kernel = 4 formal gradients + 2 diagonal trace-free shears")
print("PASS: C4 = P K_G(k) with explicitly integer coefficients at formal k=(1,1,1,1)")
print("FIREWALL: flat finite symbol only; NOT finite gauge, TT propagation, native source, h-uniform or GR")
