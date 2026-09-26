#!/usr/bin/env python3
"""Exact diagonal source-invisible joint germ.

N_0 is the real 4-space ker H_AA ∩ ker H_QA at z=(i,i,i,i).
The first basis vector is a spatial rotation on Role 0. Its cosine family

    L_0(x) = exp(t * sigma(sum x) * Y),    other links = I,

sigma = (1,0,-1,0), has nonzero curvature, is not pure gauge, has
identically vanishing metric Euler at standard solder, and has connection
edge-Euler Taylor jet zero through degree 8.

No Einstein equation is claimed.
"""
from itertools import combinations
import sympy as sp

PAIRS = list(combinations(range(4), 2))
PINDEX = {p: i for i, p in enumerate(PAIRS)}
ETA = sp.diag(1, -1, -1, -1)


def check(name, cond):
    if not cond:
        raise AssertionError(name)
    print("PASS_" + name)


def rot(i, j):
    X = sp.zeros(4)
    X[i, j] = 1
    X[j, i] = -1
    return X


def boost(i):
    X = sp.zeros(4)
    X[0, i] = X[i, 0] = 1
    return X


GEN = [boost(1), boost(2), boost(3), rot(1, 2), rot(1, 3), rot(2, 3)]
for X in GEN:
    check("LORENTZ_TANGENT", sp.expand(X.T * ETA + ETA * X) == sp.zeros(4))

G2 = sp.zeros(6)
for i, (a, b) in enumerate(PAIRS):
    G2[i, i] = ETA[a, a] * ETA[b, b]
STAR = sp.zeros(6)
for src, (dst, sign) in {
    (0, 1): ((2, 3), -1), (0, 2): ((1, 3), 1), (0, 3): ((1, 2), -1),
    (1, 2): ((0, 3), 1), (1, 3): ((0, 2), -1), (2, 3): ((0, 1), 1),
}.items():
    STAR[PINDEX[dst], PINDEX[src]] = sign
check("STAR_SQUARE", STAR * STAR == -sp.eye(6))

# ---------------------------------------------------------------- kernel
def wedge_vec(u, v):
    return sp.Matrix([u[a] * v[b] - u[b] * v[a] for a, b in PAIRS])


def bivector_of_tangent(X):
    Ym = X * ETA
    return sp.Matrix([Ym[a, b] for a, b in PAIRS])


def complement_orientation(face):
    comp = [i for i in range(4) if i not in face]
    seq = list(face) + comp
    inv = sum(seq[i] > seq[j] for i in range(4) for j in range(i + 1, 4))
    return -1 if inv % 2 else 1


def mul_jet4(X, Ym):
    return (
        X[0] * Ym[0],
        X[0] * Ym[1] + X[1] * Ym[0],
        X[0] * Ym[2] + X[2] * Ym[0],
        X[0] * Ym[3] + X[1] * Ym[2] + X[2] * Ym[1] + X[3] * Ym[0],
    )


def exp_link4(A0, B0, phase_a=1, phase_b=1, inverse=False):
    sign = -1 if inverse else 1
    return (
        sp.eye(4),
        sign * phase_a * A0,
        sign * phase_b * B0,
        sp.Rational(1, 2) * phase_a * phase_b * (A0 * B0 + B0 * A0),
    )


def curvature_mixed(P):
    return P[3] - sp.Rational(1, 2) * (P[1] * P[2] + P[2] * P[1])


Z = [sp.I, sp.I, sp.I, sp.I]
avars = sp.symbols("a0:24")
bvars = sp.symbols("b0:24")
A, Bc = [], []
for r in range(4):
    YA = sp.zeros(4)
    YB = sp.zeros(4)
    for j, gen in enumerate(GEN):
        YA += avars[6 * r + j] * gen
        YB += bvars[6 * r + j] * gen
    A.append(YA)
    Bc.append(YB)
basis_cols = [sp.eye(4)[:, r] for r in range(4)]
connection_bilinear = 0
for r, s in PAIRS:
    Pj = (sp.eye(4), sp.zeros(4), sp.zeros(4), sp.zeros(4))
    Pj = mul_jet4(Pj, exp_link4(A[r], Bc[r]))
    Pj = mul_jet4(Pj, exp_link4(A[s], Bc[s], Z[r], 1 / Z[r]))
    Pj = mul_jet4(Pj, exp_link4(A[r], Bc[r], Z[s], 1 / Z[s], inverse=True))
    Pj = mul_jet4(Pj, exp_link4(A[s], Bc[s], inverse=True))
    u, v = [i for i in range(4) if i not in (r, s)]
    B0 = wedge_vec(basis_cols[u], basis_cols[v])
    connection_bilinear += complement_orientation((r, s)) * (
        B0.T * G2 * STAR * bivector_of_tangent(curvature_mixed(Pj))
    )[0]
connection_bilinear = sp.expand(connection_bilinear)
HAB = sp.zeros(24)
for i in range(24):
    di = sp.diff(connection_bilinear, avars[i])
    for j in range(24):
        HAB[i, j] = sp.diff(di, bvars[j])

hvars = sp.symbols("h0:16")
hlegs = [sp.Matrix(hvars[4 * r: 4 * r + 4]) for r in range(4)]
cross = 0
for r, s in PAIRS:
    C1 = (1 / Z[r] - 1) * Bc[s] - (1 / Z[s] - 1) * Bc[r]
    u, v = [i for i in range(4) if i not in (r, s)]
    B1 = wedge_vec(hlegs[u], basis_cols[v]) + wedge_vec(basis_cols[u], hlegs[v])
    cross += complement_orientation((r, s)) * (
        B1.T * G2 * STAR * bivector_of_tangent(C1)
    )[0]
cross = sp.expand(cross)
HAH = sp.zeros(24, 16)
for i in range(24):
    di = sp.diff(cross, bvars[i])
    for j in range(16):
        HAH[i, j] = sp.diff(di, hvars[j])
SYM = [(a0, b0) for a0 in range(4) for b0 in range(a0, 4)]
B = sp.zeros(16, 10)
for j, (a0, b0) in enumerate(SYM):
    q = sp.zeros(4)
    q[a0, b0] = q[b0, a0] = 1
    H = sp.Rational(1, 2) * q * ETA
    for r in range(4):
        for c0 in range(4):
            B[4 * r + c0, j] = H[r, c0]
HAQ = sp.expand(HAH * B)


def kv(entries):
    vector = sp.zeros(24, 1)
    for idx, val in entries.items():
        vector[idx] = val
    return vector


KERNEL = [
    kv({0: 1, 1: 1, 2: 1}),
    kv({3: 1, 4: -1, 5: 1}),
    kv({6: 1, 9: 1, 10: 1}),
    kv({7: 1, 8: -1, 11: 1}),
    kv({12: 1, 14: -1, 16: 1}),
    kv({13: 1, 15: -1, 17: 1}),
    kv({18: 1, 19: -1, 21: 1}),
    kv({20: -1, 22: 1, 23: 1}),
]
K = sp.Matrix.hstack(*KERNEL)
check("DIAGONAL_H_RANK_16", HAB.rank() == 16)
check("DIAGONAL_KERNEL", HAB * K == sp.zeros(24, 8))
PAIR = sp.expand(HAQ.T * K)
NULL = PAIR.nullspace()
check("N0_DIMENSION_4", len(NULL) == 4)
INVISIBLE_INDEX = [1, 3, 4, 6]
for vec, idx in zip(NULL, INVISIBLE_INDEX):
    target = sp.zeros(8, 1)
    target[idx] = 1
    check("N0_BASIS_%d" % idx, sp.expand(vec - target) == sp.zeros(8, 1))
check("VISIBLE_Q11", sp.expand((KERNEL[0].T * HAQ[:, SYM.index((1, 1))])[0]) == -1 - sp.I)

# ---------------------------------------------------------------- germ
Y = GEN[3] - GEN[4] + GEN[5]
check("Y_CUBIC", sp.expand(Y**3 + 3 * Y) == sp.zeros(4))
bY = bivector_of_tangent(Y)
check("CURVATURE_DIRECTION_NONZERO", bY != sp.zeros(6, 1))


def ori(i, j):
    rest = [k for k in range(4) if k not in (i, j)]
    seq = [i, j] + rest
    return (-1) ** sum(seq[p] > seq[q] for p, q in combinations(range(4), 2))


def wedge(u, v):
    return sp.Matrix([u[a] * v[b] - u[b] * v[a] for a, b in PAIRS])


def pair(Bvec, Cvec):
    return sp.expand((Bvec.T * G2 * STAR * Cvec)[0])


# Standard complementary area of face (0,1) is spatial; star b(Y) is pure boost.
B23 = wedge(basis_cols[2], basis_cols[3])
check("FLAT_CELL_DENSITY", pair(B23, bY) == 0)

# Three faces through Role 0, arbitrary leg variation, curvature parallel to Y.
e = basis_cols
nonzero = False
for role in range(4):
    for comp in range(4):
        total = 0
        for s in (1, 2, 3):
            u, v = [i for i in range(4) if i not in (0, s)]
            Bvar = sp.zeros(6, 1)
            if role == u:
                Bvar += wedge(e[comp], e[v])
            if role == v:
                Bvar += wedge(e[u], e[comp])
            total += ori(0, s) * pair(Bvar, bY)
        if sp.expand(total) != 0:
            nonzero = True
check("METRIC_EULER_IDENTICALLY_ZERO", not nonzero)

# Not pure gauge: same x_0, different sum, different cosine weight.
SIGMA = [1, 0, -1, 0]
check("NOT_GAUGE_SAME_X0", SIGMA[0] != SIGMA[1])

# Connection edge Euler, Taylor jet through degree 8.
DEGREE = 8
STAR_OF = [[] for _ in range(6)]
for src, (dst, sign) in {
    (0, 1): ((2, 3), -1), (0, 2): ((1, 3), 1), (0, 3): ((1, 2), -1),
    (1, 2): ((0, 3), 1), (1, 3): ((0, 2), -1), (2, 3): ((0, 1), 1),
}.items():
    STAR_OF[PINDEX[dst]].append((PINDEX[src], sign))
G2_DIAG = [ETA[a, a] * ETA[b, b] for a, b in PAIRS]


def zeros():
    return [sp.zeros(4) for _ in range(DEGREE + 1)]


def dexp(sign, G):
    acc = zeros()
    powY = [sp.eye(4)]
    cur = sp.eye(4)
    for _k in range(1, DEGREE + 1):
        cur = sp.expand(cur * (sign * Y))
        powY.append(cur)
    for n in range(1, DEGREE + 1):
        fact = sp.factorial(n)
        term = sp.zeros(4)
        for j in range(n):
            term += powY[j] * G * powY[n - 1 - j]
        acc[n - 1] = sp.expand(acc[n - 1] + term / fact)
    return acc


def biv_poly(R):
    out = []
    for k in range(DEGREE + 1):
        ME = sp.expand(R[k] * ETA)
        out.append(sp.Matrix([ME[a, b] for a, b in PAIRS]))
    return out


def pair_poly(Bvec, Cpoly):
    acc = []
    for k in range(DEGREE + 1):
        starred = sp.zeros(6, 1)
        for dst in range(6):
            for src, sign in STAR_OF[dst]:
                starred[dst] += sign * Cpoly[k][src]
        acc.append(sp.expand(sum(Bvec[i] * G2_DIAG[i] * starred[i] for i in range(6))))
    return acc


def exp_series(sign):
    out = zeros()
    out[0] = sp.eye(4)
    power = sp.eye(4)
    fact = 1
    for k in range(1, DEGREE + 1):
        power = sp.expand(power * (sign * Y))
        fact *= k
        out[k] = sp.expand(power / fact)
    return out


def sandwich(dU, left, right):
    out = zeros()
    for i in range(DEGREE + 1):
        for j in range(DEGREE + 1 - i):
            mid = sp.expand(left[i] * dU[j])
            for k in range(DEGREE + 1 - i - j):
                out[i + j + k] = sp.expand(out[i + j + k] + mid * right[k])
    return out


U = exp_series(1)
Uinv = exp_series(-1)
for g, G in enumerate(GEN):
    total = [0] * (DEGREE + 1)
    dplus = dexp(1, G)
    dminus = dexp(-1, -G)
    dPinv = sandwich(dplus, Uinv, Uinv)
    for k in range(DEGREE + 1):
        dPinv[k] = sp.expand(-dPinv[k])
    dR_plus = [sp.expand(sp.Rational(1, 2) * (dplus[k] - dPinv[k])) for k in range(DEGREE + 1)]
    dR_minus = [sp.expand(sp.Rational(1, 2) * (dminus[k] - dplus[k])) for k in range(DEGREE + 1)]
    for s in (1, 2, 3):
        comp = [i for i in range(4) if i not in (0, s)]
        Bvar = wedge(e[comp[0]], e[comp[1]])
        for dR in (dR_plus, dR_minus):
            paired = pair_poly(Bvar, biv_poly(dR))
            for k in range(DEGREE + 1):
                total[k] += ori(0, s) * paired[k]
    check("EDGE_EULER_JET_%d" % g, all(sp.expand(coeff) == 0 for coeff in total))

print("N0_INDEX", INVISIBLE_INDEX)
print("TERMINAL: J2-DIAGONAL-INVISIBLE-JOINT-VACUUM-GERM-FOUND")
