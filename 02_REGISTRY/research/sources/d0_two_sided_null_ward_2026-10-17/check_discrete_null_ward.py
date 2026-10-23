#!/usr/bin/env python3
"""Exact finite control for the two-sided null/Ward/global route (Draft #334).

This is a flat 4D periodic *mathematical model*, not a D0 native Ward
certificate. Its role is to test the integration-constant algebra and the
lossless weak adjoint identity, without rerunning the earlier null-basis test.
"""
from fractions import Fraction as F
from itertools import product

DIM = 4
SIG = (1, -1, -1, -1)
SITES = list(product(range(2), repeat=DIM))
WHERE = {p: i for i, p in enumerate(SITES)}
N = len(SITES)


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def move(x, a, direction):
    y = list(x)
    y[a] = (y[a] + direction) % 2
    return WHERE[tuple(y)]


def rank(matrix):
    a = [[F(x) for x in row] for row in matrix]
    piv = 0
    for col in range(len(a[0])):
        candidates = [r for r in range(piv, len(a)) if a[r][col]]
        if not candidates:
            continue
        r = candidates[0]
        a[piv], a[r] = a[r], a[piv]
        scale = a[piv][col]
        a[piv] = [v / scale for v in a[piv]]
        for r in range(len(a)):
            if r != piv:
                q = a[r][col]
                a[r] = [v - q * w for v, w in zip(a[r], a[piv])]
        piv += 1
        if piv == len(a):
            break
    return piv


def div_tensor(S):
    return [
        [
            sum(F(SIG[mu]) *
                (S[move(x, mu, 1)][mu][nu] - S[i][mu][nu])
                for mu in range(DIM))
            for nu in range(DIM)
        ]
        for i, x in enumerate(SITES)
    ]


def tracefree_split(S):
    f = [sum(F(SIG[a]) * S[i][a][a] for a in range(DIM)) / 4
         for i in range(N)]
    E = [
        [
            [S[i][a][b] - (F(SIG[a]) * f[i] if a == b else 0)
             for b in range(DIM)]
            for a in range(DIM)
        ]
        for i in range(N)
    ]
    require(all(sum(SIG[a] * E[i][a][a] for a in range(DIM)) == 0
                for i in range(N)), "tracefree projection")
    return f, E


def check():
    incidence = []
    for i, x in enumerate(SITES):
        for mu in range(DIM):
            row = [0] * N
            row[i] -= 1
            row[move(x, mu, 1)] += 1
            incidence.append(row)
    require(rank(incidence) == N - 1, "connected gradient has rank N-1")
    require(rank(incidence + [[1] * N]) == N,
            "one global scalar closes constant mode")

    # Without a Ward row, a spatially varying pure metric multiple
    # annihilates every null test yet remains physically nonconstant.
    f_bad = [F(1 if x[0] == 0 else -1) for x in SITES]
    pure = [[[F(SIG[a]) * f_bad[i] if a == b else F(0)
              for b in range(DIM)] for a in range(DIM)] for i in range(N)]
    nulls = ([F(1), F(1), F(0), F(0)],
             [F(1), F(-1), F(0), F(0)],
             [F(1), F(3, 5), F(4, 5), F(0)])
    require(all(sum(pure[i][a][b] * k[a] * k[b]
                    for a in range(DIM) for b in range(DIM)) == 0
                for i in range(N) for k in nulls),
            "metric multiple must be invisible to null rays")
    require(any(v != 0 for row in div_tensor(pure) for v in row),
            "inhomogeneous cosmological mode must violate Ward")

    # An exact Ward by itself permits non-Einstein tracefree responses.
    E_counter = [[[F(0) for _ in range(DIM)] for _ in range(DIM)]
                 for _ in range(N)]
    for i in range(N):
        E_counter[i][0][0] = -f_bad[i]
        E_counter[i][1][1] = -f_bad[i]
    S_counter = [[[pure[i][a][b] + E_counter[i][a][b]
                   for b in range(DIM)] for a in range(DIM)]
                 for i in range(N)]
    require(all(v == 0 for row in div_tensor(S_counter) for v in row),
            "counterexample to Ward-only closure")
    require(any(sum(S_counter[i][a][b] * nulls[0][a] * nulls[0][b]
                    for a in range(DIM) for b in range(DIM)) != 0
                for i in range(N)), "Ward-only source must be optically visible")

    # Exact discrete integration by parts keeps an off-shell Ward defect W.
    S = []
    for i, x in enumerate(SITES):
        M = [[F((a + 1) * (b + 1) + sum((r + 1) * z for r, z in enumerate(x))
                 + (a - b) ** 2, 1 + (a + b) % 3)
              for b in range(DIM)] for a in range(DIM)]
        for a in range(DIM):
            for b in range(a + 1, DIM):
                M[b][a] = M[a][b]
        S.append(M)
    f, E = tracefree_split(S)
    W = div_tensor(S)
    X = [[F((i + 2) * (nu + 1) + i % 3, 5 + (i + nu) % 4)
          for nu in range(DIM)] for i in range(N)]
    phi = [sum(X[i][nu] - X[move(x, nu, -1)][nu]
               for nu in range(DIM)) for i, x in enumerate(SITES)]
    require(sum(phi) == 0, "discrete test has zero mean")
    lhs = sum(f[i] * phi[i] for i in range(N))
    shape_term = -sum(
        F(SIG[mu]) * E[i][mu][nu] *
        (X[i][nu] - X[move(x, mu, -1)][nu])
        for i, x in enumerate(SITES)
        for mu in range(DIM) for nu in range(DIM))
    ward_term = -sum(W[i][nu] * X[i][nu]
                     for i in range(N) for nu in range(DIM))
    require(lhs == shape_term + ward_term, "exact dual Ward identity")
    require(lhs != shape_term and ward_term != 0,
            "freezing the comparator Ward defect must fail")

    # One null direction has a nilpotent shear with exact unit determinant:
    # (I + tN)^-1=I-tN and det(I+tN)=1 for every scalar t.
    k = [F(1), F(3, 5), F(4, 5), F(0)]
    lower = [SIG[a] * k[a] for a in range(DIM)]
    M = [[k[a] * lower[b] for b in range(DIM)] for a in range(DIM)]
    M2 = [[sum(M[a][c] * M[c][b] for c in range(DIM))
           for b in range(DIM)] for a in range(DIM)]
    require(sum(k[a] * lower[a] for a in range(DIM)) == 0,
            "null condition")
    require(all(v == 0 for row in M2 for v in row), "nilpotent shear")
    require(sum(M[a][a] for a in range(DIM)) == 0, "zero volume derivative")
    print("PASS null+Ward kernel: dimension one; global trace selects constant")
    print("PASS finite weak Ward dual with nonzero off-shell defect")
    print("PASS exact null shear has zero volume source; hostile controls passed")


if __name__ == "__main__":
    check()
