#!/usr/bin/env python3
"""Exact second-order nonlinear-lift obstruction for the A4D null shells.

Research-only. Exact rational/symbolic arithmetic.

The accepted flat L=2 Hessian has three nonzero Lorentz-null checkerboard
sectors.  Each has a two-dimensional quotient kernel after the ten known gauge
directions are removed.

This certificate:

1. reconstructs the quadratic Hessian and the gauge tangent matrix;
2. verifies two explicit nongauge Hessian-null vectors in each of the three
   Lorentz-null sectors;
3. forms an arbitrary real physical null combination alpha*u + beta*v;
4. uses the exact second-order Cayley/Lorentz jet
       L = I + t A + t^2 A^2/2 + O(t^3)
   which agrees with any smooth Lorentz chart through quadratic order;
5. computes the O(t^2) zero-momentum solder-Euler source;
6. proves that in every null sector the source is proportional to
       alpha^2 + beta^2,
   so no nonzero real physical null direction can be lifted to a nonlinear
   stationary branch.

At zero momentum the linear curvature vanishes identically, hence the quadratic
action has no coframe row/cross block there.  A nonzero O(t^2) coframe source
therefore cannot be cancelled by any second-order zero-momentum correction.

The result is about the selected star/relative-solder density.  A direct-sum
full-affine term depending only on translational holonomy (for example R^T eta R)
has identically zero relative-solder Euler derivative and cannot cancel this
obstruction.  Cross-coupled solder/holonomy completions are outside this
certificate.
"""

from itertools import combinations, product
import sympy as sp

PAIRS = list(combinations(range(4), 2))
PINDEX = {p: i for i, p in enumerate(PAIRS)}
ETA = sp.diag(1, -1, -1, -1)
I4 = sp.eye(4)

def check(name, cond):
    if not cond:
        raise AssertionError(name)
    print("PASS_" + name)

# ---------------------------------------------------------------------------
# Lorentz / bivector algebra
# ---------------------------------------------------------------------------

LORENTZ = []
for i in (1, 2, 3):
    X = sp.zeros(4)
    X[0, i] = 1
    X[i, 0] = 1
    LORENTZ.append(X)
for i, j in ((1, 2), (1, 3), (2, 3)):
    X = sp.zeros(4)
    X[i, j] = 1
    X[j, i] = -1
    LORENTZ.append(X)

for X in LORENTZ:
    check("LORENTZ_TANGENT", X.T * ETA + ETA * X == sp.zeros(4))

G2 = sp.zeros(6)
for i, (a, b) in enumerate(PAIRS):
    G2[i, i] = ETA[a, a] * ETA[b, b]

STAR = sp.zeros(6)
STAR_MAP = {
    (0, 1): ((2, 3), -1),
    (0, 2): ((1, 3), +1),
    (0, 3): ((1, 2), -1),
    (1, 2): ((0, 3), +1),
    (1, 3): ((0, 2), -1),
    (2, 3): ((0, 1), +1),
}
for p, (q, s) in STAR_MAP.items():
    STAR[PINDEX[q], PINDEX[p]] = s

def wedge_vec(u, v):
    return sp.Matrix([
        u[a] * v[b] - u[b] * v[a]
        for a, b in PAIRS
    ])

def bivector_of_tangent(X):
    Y = X * ETA
    return sp.Matrix([Y[a, b] for a, b in PAIRS])

def complement_orientation(face):
    comp = [i for i in range(4) if i not in face]
    seq = list(face) + comp
    inv = sum(
        seq[i] > seq[j]
        for i in range(4)
        for j in range(i + 1, 4)
    )
    return -1 if inv % 2 else 1

def tangent_pairing_matrix(q):
    M = sp.zeros(4)
    for value, (a, b) in zip(q, PAIRS):
        M[a, b] += value
        M[b, a] -= value
    return M

# ---------------------------------------------------------------------------
# Exact flat Hessian / gauge tangents
# ---------------------------------------------------------------------------

def mul_jet(X, Y):
    return (
        X[0] * Y[0],
        X[0] * Y[1] + X[1] * Y[0],
        X[0] * Y[2] + X[1] * Y[1] + X[2] * Y[0],
    )

def exp_link(A, scale=1, inverse=False):
    B = scale * A
    return (I4, -B if inverse else B, B * B / 2)

def quadratic_density(amplitudes, signs):
    h = [
        sp.Matrix(amplitudes[4 * r:4 * r + 4])
        for r in range(4)
    ]
    A = []
    for r in range(4):
        X = sp.zeros(4)
        for k, B in enumerate(LORENTZ):
            X += amplitudes[16 + 6 * r + k] * B
        A.append(X)

    basis = [I4[:, r] for r in range(4)]
    total = sp.Integer(0)

    for r, s in PAIRS:
        P = (I4, sp.zeros(4), sp.zeros(4))
        P = mul_jet(P, exp_link(A[r]))
        P = mul_jet(P, exp_link(A[s], signs[r]))
        P = mul_jet(P, exp_link(A[r], signs[s], inverse=True))
        P = mul_jet(P, exp_link(A[s], inverse=True))

        P1, P2 = P[1], P[2]
        C1 = bivector_of_tangent(P1)
        C2 = bivector_of_tangent(P2 - P1 * P1 / 2)

        u, v = [i for i in range(4) if i not in (r, s)]
        B0 = wedge_vec(basis[u], basis[v])
        B1 = (
            wedge_vec(h[u], basis[v])
            + wedge_vec(basis[u], h[v])
        )

        total += complement_orientation((r, s)) * (
            (B0.T * G2 * STAR * C2)[0]
            + (B1.T * G2 * STAR * C1)[0]
        )

    return sp.expand(total)

def hessian(signs):
    x = sp.symbols("x0:40")
    return sp.hessian(quadratic_density(x, signs), x)

def gauge_matrix(signs):
    cols = []
    basis = [I4[:, r] for r in range(4)]

    for k, X in enumerate(LORENTZ):
        v = []
        for r in range(4):
            v += list(X * basis[r])
        for r in range(4):
            for j in range(6):
                v.append((1 - signs[r]) if j == k else 0)
        cols.append(sp.Matrix(v))

    for a in range(4):
        xi = I4[:, a]
        v = []
        for r in range(4):
            v += list((signs[r] - 1) * xi)
        v += [0] * 24
        cols.append(sp.Matrix(v))

    return sp.Matrix.hstack(*cols)

# Explicit physical quotient-null bases obtained from exact Hessian nullspaces.
PHYSICAL = {
    (-1, -1, +1, +1): (
        sp.Matrix([
            0,0,0,0, 0,0,0,0, 0,0,0,-sp.Rational(1,2),
            0,0,-sp.Rational(1,2),0,
            0,0,0,0,0,0, 0,0,0,0,0,0,
            0,0,-1,0,1,0, 0,-1,0,1,0,0,
        ]),
        sp.Matrix([
            0,0,0,0, 0,0,0,0, 0,0,sp.Rational(1,2),0,
            0,0,0,-sp.Rational(1,2),
            0,0,0,0,0,0, 0,0,0,0,0,0,
            0,1,0,-1,0,0, 0,0,-1,0,1,0,
        ]),
    ),
    (-1, +1, -1, +1): (
        sp.Matrix([
            0,0,0,0, 0,0,0,sp.Rational(1,2), 0,0,0,0,
            0,sp.Rational(1,2),0,0,
            0,0,0,0,0,0, 0,0,1,0,0,-1,
            0,0,0,0,0,0, 1,0,0,1,0,0,
        ]),
        sp.Matrix([
            0,0,0,0, 0,sp.Rational(1,2),0,0, 0,0,0,0,
            0,0,0,-sp.Rational(1,2),
            0,0,0,0,0,0, 1,0,0,1,0,0,
            0,0,0,0,0,0, 0,0,-1,0,0,1,
        ]),
    ),
    (-1, +1, +1, -1): (
        sp.Matrix([
            0,0,0,0, 0,0,sp.Rational(1,2),0,
            0,sp.Rational(1,2),0,0, 0,0,0,0,
            0,0,0,0,0,0, 0,1,0,0,0,1,
            1,0,0,0,1,0, 0,0,0,0,0,0,
        ]),
        sp.Matrix([
            0,0,0,0, 0,-sp.Rational(1,2),0,0,
            0,0,sp.Rational(1,2),0, 0,0,0,0,
            0,0,0,0,0,0, -1,0,0,0,-1,0,
            0,1,0,0,0,1, 0,0,0,0,0,0,
        ]),
    ),
}

for signs, (u, v) in PHYSICAL.items():
    H = hessian(signs)
    G = gauge_matrix(signs)

    tag = "".join("P" if s == 1 else "M" for s in signs)
    check("NULL_SHELL_RANK_28_" + tag, H.rank() == 28)
    check("GAUGE_RANK_10_" + tag, G.rank() == 10)
    check("PHYSICAL_U_HESSIAN_NULL_" + tag, H * u == sp.zeros(40, 1))
    check("PHYSICAL_V_HESSIAN_NULL_" + tag, H * v == sp.zeros(40, 1))
    check("PHYSICAL_PAIR_INDEPENDENT_MOD_GAUGE_" + tag,
          G.row_join(u).row_join(v).rank() == 12)

# At zero momentum every first-order plaquette curvature is
# A_r + A_s - A_r - A_s = 0.  Therefore the quadratic density has no h
# dependence and no h-a cross term.
H0 = hessian((+1, +1, +1, +1))
check("ZERO_MOMENTUM_COFRAME_ROWS_ZERO",
      H0[:16, :] == sp.zeros(16, 40))
check("ZERO_MOMENTUM_CONNECTION_BLOCK_RANK_24",
      H0[16:, 16:].rank() == 24)

# ---------------------------------------------------------------------------
# O(t^2) zero-momentum solder source for the physical null plane
# ---------------------------------------------------------------------------

SITES = list(product(range(2), repeat=4))

def site_add(x, r):
    y = list(x)
    y[r] ^= 1
    return tuple(y)

def character(signs, x):
    out = 1
    for i, s in enumerate(signs):
        if x[i]:
            out *= s
    return out

def series_mul(X, Y):
    out = [sp.zeros(4) for _ in range(3)]
    for i in range(3):
        for j in range(3 - i):
            out[i + j] += X[i] * Y[j]
    return out

def series_inv(S):
    R = [sp.zeros(4) for _ in range(3)]
    R[0] = S[0].inv()
    for n in range(1, 3):
        acc = sp.zeros(4)
        for k in range(1, n + 1):
            acc += S[k] * R[n - k]
        R[n] = -R[0] * acc
    return R

def second_order_solder_source(signs, u, v):
    alpha, beta = sp.symbols("alpha beta", real=True)

    h = []
    A = []
    for r in range(4):
        hu = sp.Matrix(u[4 * r:4 * r + 4, 0])
        hv = sp.Matrix(v[4 * r:4 * r + 4, 0])
        h.append(alpha * hu + beta * hv)

        X = sp.zeros(4)
        for k, G in enumerate(LORENTZ):
            X += (
                alpha * u[16 + 6 * r + k, 0]
                + beta * v[16 + 6 * r + k, 0]
            ) * G
        A.append(X)

    links = {}
    for x in SITES:
        chi = character(signs, x)
        for r in range(4):
            # Cayley and exponential coordinates agree through O(t^2).
            links[(x, r)] = [
                I4,
                chi * A[r],
                A[r] * A[r] / 2,
            ]

    curvature = {}
    for x in SITES:
        for r, s in PAIRS:
            xr = site_add(x, r)
            xs = site_add(x, s)

            P = [I4, sp.zeros(4), sp.zeros(4)]
            P = series_mul(P, links[(x, r)])
            P = series_mul(P, links[(xr, s)])
            P = series_mul(P, series_inv(links[(xs, r)]))
            P = series_mul(P, series_inv(links[(x, s)]))

            Pi = series_inv(P)
            R1 = (P[1] - Pi[1]) / 2
            R2 = (P[2] - Pi[2]) / 2
            curvature[(x, r, s)] = (
                bivector_of_tangent(R1),
                bivector_of_tangent(R2),
            )

    sources = []
    for x in SITES:
        chi = character(signs, x)
        grads = [sp.zeros(4, 1) for _ in range(4)]

        for r, s in PAIRS:
            urole, vrole = [i for i in range(4) if i not in (r, s)]
            C1, C2 = curvature[(x, r, s)]

            M1 = tangent_pairing_matrix(
                complement_orientation((r, s)) * G2 * STAR * C1
            )
            M2 = tangent_pairing_matrix(
                complement_orientation((r, s)) * G2 * STAR * C2
            )

            eu = I4[:, urole]
            ev = I4[:, vrole]
            hu = chi * h[urole]
            hv = chi * h[vrole]

            grads[urole] += M2 * ev + M1 * hv
            grads[vrole] += M2.T * eu + M1.T * hu

        sources.append(sp.Matrix.vstack(*grads))

    check("SECOND_ORDER_SOURCE_IS_ZERO_MOMENTUM",
          all(s == sources[0] for s in sources))

    return alpha, beta, sp.Matrix([
        sp.factor(q)
        for q in sources[0]
    ])

EXPECTED_PATTERN = sp.Matrix([
    -2, -2, 0, 0,
     2,  2, 0, 0,
     0,  0, 0, 0,
     0,  0, 0, 0,
])

for signs, (u, v) in PHYSICAL.items():
    alpha, beta, source = second_order_solder_source(signs, u, v)
    tag = "".join("P" if s == 1 else "M" for s in signs)

    check("SECOND_ORDER_SOURCE_PATTERN_" + tag,
          source == (alpha**2 + beta**2) * EXPECTED_PATTERN)

    nonzero_polys = list(dict.fromkeys([
        sp.factor(q)
        for q in source
        if q != 0
    ]))
    gb = sp.groebner(nonzero_polys, alpha, beta, order="lex")

    check("LIFT_OBSTRUCTION_GROEBNER_" + tag,
          list(gb) == [alpha**2 + beta**2])

print("RESULT: every real physical quotient-null plane on the three L=2 Lorentz-null checkerboard sectors is obstructed at second order.")
print("RESULT: the rank-28/rank-4 flat drop does not integrate to a small-amplitude nonlinear curved stationary branch of the star/relative-solder density.")
print("RESULT: adding a direct-sum translational-holonomy scalar with no relative-solder dependence cannot cancel this coframe obstruction.")
print("SCOPE: finite-amplitude disconnected branches and cross-coupled solder/holonomy completions remain open.")
