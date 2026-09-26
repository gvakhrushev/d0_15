#!/usr/bin/env python3
"""Exact nonlinear obstruction for the three A4D Lorentz-null checkerboard sectors.

Research-only. Exact SymPy arithmetic.

The accepted flat quadratic analysis has three nonzero L=2 characters with
kappa_eta^2=0.  After quotienting the ten flat gauge directions, each carries
two extra Hessian-null directions.

This checker computes the cubic Lyapunov-Schmidt obstruction of the full
finite star action.  For a first-order physical null direction z in one of
those two-dimensional quotient-null planes, a necessary condition for a smooth
stationary branch

    field(t) = t z + t^2 z2 + ...

from the canonical flat solder is

    T(z,z,w) = 0

for every zero-momentum Hessian-null vector w, because H z2 lies in the image
of the symmetric flat Hessian and is orthogonal to its kernel.

For one fixed constant-solder kernel direction w0, the exact quadratic
obstruction form on each two-dimensional physical null plane is

    T(a u + b v, a u + b v, w0)
      = -(32/3) (a^2 + b^2).

Hence every nonzero physical combination is obstructed already at second order.

Scope: canonical flat solder / accepted star action / the three period-two
Lorentz-null sectors only.  This is not a no-go for all curved stationary
solutions and says nothing about a different constant-solder flat background
or an enlarged affine-completed action.
"""

from itertools import combinations, product
import sympy as sp

PAIRS = list(combinations(range(4), 2))
PINDEX = {p: i for i, p in enumerate(PAIRS)}
ETA = sp.diag(1, -1, -1, -1)
I4 = sp.eye(4)
SITES = list(product((0, 1), repeat=4))

def check(name, cond):
    if not cond:
        raise AssertionError(name)
    print("PASS_" + name)

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

G2 = sp.diag(*[
    ETA[a, a] * ETA[b, b]
    for a, b in PAIRS
])

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

def wedge(u, v):
    return sp.Matrix([
        u[a] * v[b] - u[b] * v[a]
        for a, b in PAIRS
    ])

def bivector_of_tangent(X):
    Y = X * ETA
    return sp.Matrix([
        sp.simplify(Y[a, b])
        for a, b in PAIRS
    ])

def orientation(face):
    comp = [i for i in range(4) if i not in face]
    seq = list(face) + comp
    inv = sum(
        seq[i] > seq[j]
        for i in range(4)
        for j in range(i + 1, 4)
    )
    return -1 if inv % 2 else 1

# ------------------------------------------------------------------
# Accepted quadratic Hessian
# ------------------------------------------------------------------

def mul_jet2(X, Y):
    return (
        X[0] * Y[0],
        X[0] * Y[1] + X[1] * Y[0],
        X[0] * Y[2] + X[1] * Y[1] + X[2] * Y[0],
    )

def exp_link2(A, scale=1, inverse=False):
    B = scale * A
    return (
        I4,
        -B if inverse else B,
        B * B / 2,
    )

def quadratic_density(amplitudes, signs):
    h = [
        sp.Matrix(amplitudes[4 * r:4 * r + 4])
        for r in range(4)
    ]
    Avec = []
    offset = 16
    for r in range(4):
        X = sp.zeros(4)
        for k, B in enumerate(LORENTZ):
            X += amplitudes[offset + 6 * r + k] * B
        Avec.append(X)

    basis = [I4[:, r] for r in range(4)]
    total = sp.Integer(0)

    for r, s in PAIRS:
        P = (I4, sp.zeros(4), sp.zeros(4))
        P = mul_jet2(P, exp_link2(Avec[r]))
        P = mul_jet2(P, exp_link2(Avec[s], signs[r]))
        P = mul_jet2(
            P,
            exp_link2(Avec[r], signs[s], inverse=True),
        )
        P = mul_jet2(P, exp_link2(Avec[s], inverse=True))

        P1, P2 = P[1], P[2]
        C1 = bivector_of_tangent(P1)
        C2 = bivector_of_tangent(P2 - P1 * P1 / 2)

        u, v = [i for i in range(4) if i not in (r, s)]
        B0 = wedge(basis[u], basis[v])
        B1 = (
            wedge(h[u], basis[v])
            + wedge(basis[u], h[v])
        )

        total += orientation((r, s)) * (
            (B0.T * G2 * STAR * C2)[0]
            + (B1.T * G2 * STAR * C1)[0]
        )

    return sp.expand(total)

def hessian(signs):
    x = sp.symbols("x0:40")
    return sp.hessian(
        quadratic_density(x, signs),
        x,
    )

def gauge_matrix(signs):
    cols = []
    basis = [I4[:, r] for r in range(4)]

    for k, X in enumerate(LORENTZ):
        v = []
        for r in range(4):
            v += list(X * basis[r])
        for r in range(4):
            for j in range(6):
                v.append(
                    (1 - signs[r])
                    if j == k
                    else 0
                )
        cols.append(sp.Matrix(v))

    for a in range(4):
        xi = I4[:, a]
        v = []
        for r in range(4):
            v += list((signs[r] - 1) * xi)
        v += [0] * 24
        cols.append(sp.Matrix(v))

    return sp.Matrix.hstack(*cols)

def physical_null_basis(signs):
    H = hessian(signs)
    G = gauge_matrix(signs)

    check(
        "NULL_SECTOR_HESSIAN_RANK_28_" + str(signs),
        H.rank() == 28,
    )
    check(
        "NULL_SECTOR_GAUGE_RANK_10_" + str(signs),
        G.rank() == 10,
    )
    check(
        "NULL_SECTOR_GAUGE_IS_NULL_" + str(signs),
        H * G == sp.zeros(40, 10),
    )

    K = sp.Matrix.hstack(*H.nullspace())
    M = G.copy()
    out = []
    for j in range(K.cols):
        c = K[:, j]
        if M.row_join(c).rank() > M.rank():
            out.append(c)
            M = M.row_join(c)
        if len(out) == 2:
            break

    check(
        "PHYSICAL_NULL_COMPLEMENT_DIM_2_" + str(signs),
        len(out) == 2 and M.rank() == 12,
    )
    return out

# ------------------------------------------------------------------
# Cubic coefficient of the full 16-site action
# ------------------------------------------------------------------

def series_mul(A, B, N):
    out = [sp.zeros(4) for _ in range(N + 1)]
    for n in range(N + 1):
        acc = sp.zeros(4)
        for k in range(n + 1):
            acc += A[k] * B[n - k]
        out[n] = sp.simplify(acc)
    return out

def series_inv(A, N):
    out = [I4] + [sp.zeros(4) for _ in range(N)]
    for n in range(1, N + 1):
        acc = sp.zeros(4)
        for k in range(1, n + 1):
            acc += A[k] * out[n - k]
        out[n] = sp.simplify(-acc)
    return out

def exp_series(A, N=3, inverse=False):
    sign = -1 if inverse else 1
    out = [I4]
    for n in range(1, N + 1):
        out.append(
            sp.simplify(
                sign ** n * A ** n / sp.factorial(n)
            )
        )
    return out

def site_add(x, r):
    y = list(x)
    y[r] = (y[r] + 1) % 2
    return tuple(y)

def site_direction(vec40, signs):
    h0 = [
        sp.Matrix(vec40[4 * r:4 * r + 4])
        for r in range(4)
    ]

    A0 = []
    offset = 16
    for r in range(4):
        X = sp.zeros(4)
        for k, B in enumerate(LORENTZ):
            X += vec40[offset + 6 * r + k] * B
        A0.append(sp.simplify(X))

    h = {}
    A = {}
    for x in SITES:
        chi = sp.Integer(1)
        for r in range(4):
            chi *= signs[r] ** x[r]
        for r in range(4):
            h[(x, r)] = sp.simplify(chi * h0[r])
            A[(x, r)] = sp.simplify(chi * A0[r])

    return h, A

def add_directions(h1, A1, h2, A2, scale2=1):
    h = {
        key: sp.simplify(h1[key] + scale2 * h2[key])
        for key in h1
    }
    A = {
        key: sp.simplify(A1[key] + scale2 * A2[key])
        for key in A1
    }
    return h, A

def cubic_action(hdir, Adir):
    N = 3
    basis = [I4[:, r] for r in range(4)]
    total = sp.Integer(0)

    for x in SITES:
        for r, s in PAIRS:
            xr = site_add(x, r)
            xs = site_add(x, s)

            P = [I4] + [sp.zeros(4) for _ in range(N)]
            for factor in (
                exp_series(Adir[(x, r)], N),
                exp_series(Adir[(xr, s)], N),
                exp_series(Adir[(xs, r)], N, inverse=True),
                exp_series(Adir[(x, s)], N, inverse=True),
            ):
                P = series_mul(P, factor, N)

            Pinv = series_inv(P, N)
            C = [
                bivector_of_tangent(
                    sp.simplify(
                        (P[n] - Pinv[n]) / 2
                    )
                )
                for n in range(N + 1)
            ]

            u, v = [i for i in range(4) if i not in (r, s)]
            hu = hdir[(x, u)]
            hv = hdir[(x, v)]

            B0 = wedge(basis[u], basis[v])
            B1 = (
                wedge(hu, basis[v])
                + wedge(basis[u], hv)
            )
            B2 = wedge(hu, hv)

            total += orientation((r, s)) * (
                (B0.T * G2 * STAR * C[3])[0]
                + (B1.T * G2 * STAR * C[2])[0]
                + (B2.T * G2 * STAR * C[1])[0]
            )

    return sp.simplify(total)

# At zero momentum H has rank 24 and its kernel contains all 16 pure
# constant-solder coordinate directions.  Use w0 = uniform h_A^A.
H0 = hessian((1, 1, 1, 1))
check("ZERO_MOMENTUM_HESSIAN_RANK_24", H0.rank() == 24)

w0 = sp.zeros(40, 1)
w0[0] = 1
check("W0_IS_ZERO_MOMENTUM_HESSIAN_NULL",
      H0 * w0 == sp.zeros(40, 1))

w0_h, w0_A = site_direction(
    w0,
    (1, 1, 1, 1),
)
check("PURE_W0_CUBIC_ZERO",
      cubic_action(w0_h, w0_A) == 0)

NULL_SECTORS = [
    (-1, -1, +1, +1),
    (-1, +1, -1, +1),
    (-1, +1, +1, -1),
]

def cubic_projection(z, signs):
    zh, zA = site_direction(z, signs)

    hp, Ap = add_directions(
        zh, zA, w0_h, w0_A, +1
    )
    hm, Am = add_directions(
        zh, zA, w0_h, w0_A, -1
    )

    # Polarization:
    # q(z+w)-q(z-w)=6 T(z,z,w)+2 q(w),
    # and q(w0)=0 here.
    return sp.simplify(
        (
            cubic_action(hp, Ap)
            - cubic_action(hm, Am)
        ) / 6
    )

for signs in NULL_SECTORS:
    u, v = physical_null_basis(signs)

    q11 = cubic_projection(u, signs)
    q22 = cubic_projection(v, signs)
    qsum = cubic_projection(u + v, signs)
    q12 = sp.simplify(
        (qsum - q11 - q22) / 2
    )

    tag = "".join("P" if s == 1 else "M" for s in signs)

    check(
        "CUBIC_OBSTRUCTION_Q11_" + tag,
        q11 == sp.Rational(-32, 3),
    )
    check(
        "CUBIC_OBSTRUCTION_Q22_" + tag,
        q22 == sp.Rational(-32, 3),
    )
    check(
        "CUBIC_OBSTRUCTION_Q12_ZERO_" + tag,
        q12 == 0,
    )

    print(
        "OBSTRUCTION_FORM",
        signs,
        "-32/3 * (a^2+b^2)",
    )

print("RESULT: every nonzero physical quotient-null combination in each of the three Lorentz-null L=2 sectors has a nonzero cubic Lyapunov-Schmidt projection onto a zero-momentum Hessian-null solder direction.")
print("RESULT: none of the six extra flat quotient null directions continues as a smooth stationary branch from the canonical flat solder.")
print("SCOPE: this does not exclude curved stationary points disconnected from that flat background, branches from a different constant-solder flat representative, or solutions of a later enlarged affine-completed action.")
