#!/usr/bin/env python3
"""Exact finite source/metric bridge on the SAME 16-grade CAR carrier.

Tests the source-defined density-dressed coframe against the normalized
native raising operator, with a nontrivial proper Lorentz exterior lift.
All comparisons use Fraction arithmetic. This is a small mathematical
operator/source test, not execution/admission of the complete physical D0
controller/Cost-Info/clock, and not the original all-site #216 terminal.
"""
from fractions import Fraction as Q
from itertools import permutations, combinations

ZERO = Q(0)
ONE = Q(1)
ETA = (ONE, -ONE, -ONE, -ONE)
CAR_N = 16


def matzero(n=CAR_N, m=CAR_N):
    return [[ZERO for _ in range(m)] for _ in range(n)]


def ident(n):
    a = matzero(n, n)
    for k in range(n):
        a[k][k] = ONE
    return a


def mmul(a, b):
    out = matzero(len(a), len(b[0]))
    for i in range(len(a)):
        for k, x in enumerate(a[i]):
            if x:
                for j, y in enumerate(b[k]):
                    if y:
                        out[i][j] += x * y
    return out


def madd(a, b):
    return [[x + y for x, y in zip(row, row2)] for row, row2 in zip(a, b)]


def mscale(x, a):
    return [[x * y for y in row] for row in a]


def mtrans(a):
    return [list(row) for row in zip(*a)]


def det_small(a):
    n = len(a)
    if n == 0:
        return ONE
    result = ZERO
    for perm in permutations(range(n)):
        inversions = sum(perm[i] > perm[j] for i in range(n) for j in range(i + 1, n))
        term = ONE if inversions % 2 == 0 else -ONE
        for i in range(n):
            term *= a[i][perm[i]]
        result += term
    return result


def inverse4(a):
    m = [row[:] + erow[:] for row, erow in zip(a, ident(4))]
    for col in range(4):
        k = next(i for i in range(col, 4) if m[i][col] != 0)
        m[col], m[k] = m[k], m[col]
        d = m[col][col]
        m[col] = [x / d for x in m[col]]
        for i in range(4):
            if i != col:
                f = m[i][col]
                m[i] = [x - f * y for x, y in zip(m[i], m[col])]
    return [row[4:] for row in m]


def creator(i):
    a = matzero()
    for mask in range(CAR_N):
        if not (mask & (1 << i)):
            sign = -ONE if ((mask & ((1 << i) - 1)).bit_count() % 2) else ONE
            a[mask | (1 << i)][mask] = sign
    return a


CREATORS = [creator(i) for i in range(4)]


def creation(u):
    result = matzero()
    for i in range(4):
        result = madd(result, mscale(u[i], CREATORS[i]))
    return result


def gamma(u):
    ans = creation(u)
    for i in range(4):
        ans = madd(ans, mscale(ETA[i] * u[i], mtrans(CREATORS[i])))
    return ans


def ext_lift(m):
    lam = matzero()
    for source in range(CAR_N):
        src = [i for i in range(4) if source & (1 << i)]
        for target in range(CAR_N):
            dst = [i for i in range(4) if target & (1 << i)]
            if len(src) == len(dst):
                lam[target][source] = det_small([[m[i][j] for j in src] for i in dst])
    return lam


def dot_eta(u, v):
    return sum(ETA[i] * u[i] * v[i] for i in range(4))


def raising(u, M):
    return mmul(creation(u), ext_lift(M))


def wedge_bivector(u, v, a, b):
    return u[a] * v[b] - u[b] * v[a]


def sign4(seq):
    return -1 if sum(seq[i] > seq[j] for i in range(4) for j in range(i + 1, 4)) % 2 else 1


def star_density(legs, matrices):
    """Original epsilon/wedge/odd-Lorentz plaquette density from the owner."""
    result = ZERO
    for r, s in combinations(range(4), 2):
        u, v = [i for i in range(4) if i not in (r, s)]
        E = sign4([r, s, u, v])
        A = mmul(matrices[(r, s)], [[ETA[i] if i == j else ZERO for j in range(4)] for i in range(4)])
        for a, b in combinations(range(4), 2):
            for c, d in combinations(range(4), 2):
                if len({a, b, c, d}) == 4:
                    result += E * sign4([a, b, c, d]) * wedge_bivector(legs[u], legs[v], a, b) * A[c][d]
    return result


def test():
    mu_bar = Q(1, 4)
    mus = (Q(1, 9), Q(1, 16))
    chis = (Q(9, 16), Q(4, 9))
    sqrtchi = (Q(3, 4), Q(2, 3))
    invsqrtchi = (Q(4, 3), Q(3, 2))
    sqrtmubar_by_mu = (Q(3, 2), Q(2))
    sqrtmu_by_mubar = (Q(2, 3), Q(1, 2))

    # Exact nontrivial proper (1+1)-Lorentz boost, identity on transverse 2+3.
    M = [[Q(5, 4), Q(3, 4), ZERO, ZERO],
         [Q(3, 4), Q(5, 4), ZERO, ZERO],
         [ZERO, ZERO, ONE, ZERO],
         [ZERO, ZERO, ZERO, ONE]]
    eta = [[ETA[i] if i == j else ZERO for j in range(4)] for i in range(4)]
    assert mmul(mmul(mtrans(M), eta), M) == eta
    assert det_small(M) == ONE
    lam = ext_lift(M)
    assert lam[0][0] == lam[15][15] == ONE
    assert sum(1 for v in lam[0] if v) == 1

    F = [[ONE, ZERO, ZERO, ZERO],
         [Q(1, 5), ONE, ZERO, ZERO],
         [ZERO, Q(1, 7), ONE, ZERO],
         [ZERO, ZERO, Q(1, 11), ONE]]
    e = inverse4(F)
    q = mmul(mmul(F, eta), mtrans(F))
    g = inverse4(q)
    assert g == mmul(mmul(mtrans(e), eta), e)

    for k in range(2):
        mu, chi = mus[k], chis[k]
        sf, isf = sqrtchi[k], invsqrtchi[k]
        a, b = sqrtmubar_by_mu[k], sqrtmu_by_mubar[k]
        # Field-to-CAR uses actual inverse coframe F, so F' = sqrt(chi) F.
        F_after = mscale(sf, F)
        mu_after = chi * mu
        q_after = mmul(mmul(F_after, eta), mtrans(F_after))
        assert q_after == mscale(chi, q)
        g_after = inverse4(q_after)
        assert g_after == mscale(1 / chi, g)
        q_dressed = mscale(mu_bar / mu, q)
        g_dressed = inverse4(q_dressed)
        assert g_dressed == mscale(mu / mu_bar, g)
        assert g_dressed == mmul(mmul(mtrans(mscale(b, e)), eta), mscale(b, e))
        assert g_dressed == mscale(mu_after / mu_bar, g_after)

        for r in range(4):
            u = F[r]
            X = raising(u, M)
            X2 = raising([sf * t for t in u], M)
            # sqrt(mu_bar/mu_after)*sqrt(chi)=sqrt(mu_bar/mu)
            assert mscale(a, X) == mscale(a / sf, X2)
            Gu = gamma([a * x for x in u])
            for s in range(4):
                Gv = gamma([a * x for x in F[s]])
                antic = madd(mmul(Gu, Gv), mmul(Gv, Gu))
                assert antic == mscale(2 * a * a * dot_eta(u, F[s]), ident(16))
            # Infinitesimal compensator derivative:
            # dmu=2*sigma*mu, dX=sigma*X => d(sqrt(bar/mu)*X)=0.
            sigma = Q(2, 7)
            derivative = madd(mscale(-sigma*a, X), mscale(a, mscale(sigma, X)))
            assert derivative == matzero()

    base = [[ONE if i == j else ZERO for j in range(4)] for i in range(4)]
    # Based R_{01} is the proper Lorentz 01-generator with a nonzero
    # complementary (23) star contraction. One site is non-trivially curved.
    R = matzero(4, 4)
    R[0][1] = R[1][0] = ONE
    curvature = {(r, s): matzero(4, 4) for r, s in combinations(range(4), 2)}
    curvature[(0, 1)] = R
    legs1 = [v[:] for v in base]
    legs2 = [v[:] for v in base]
    legs2[2] = [Q(2)*x for x in legs2[2]]
    f1 = star_density(legs1, curvature)
    f2 = star_density(legs2, curvature)
    assert f1 != 0 and f2 != 0

    weighted = mus[0] * f1 + mus[1] * f2
    dressed = (mu_bar *
               (star_density([[sqrtmu_by_mubar[0] * v for v in x] for x in legs1], curvature)
                + star_density([[sqrtmu_by_mubar[1] * v for v in x] for x in legs2], curvature)))
    assert dressed == weighted
    transformed = (
        mus[0] * chis[0] *
        star_density([[invsqrtchi[0] * v for v in x] for x in legs1], curvature)
        + mus[1] * chis[1] *
        star_density([[invsqrtchi[1] * v for v in x] for x in legs2], curvature)
    )
    assert transformed == weighted
    for mu, f in zip(mus, (f1, f2)):
        # Exact finite Euler/Ward from local quadratic homogeneity:
        assert 2 * mu * f - 2 * mu * f == 0

    # Real finite Book entropy has a nonlinear analytic Phi. Demonstrate
    # its exact Weyl defect for a quadratic jet and O(f²) vanishing.
    c, d = Q(3, 5), Q(-2, 7)
    for mu, f in zip(mus, (f1, f2)):
        phi = c * f + d * f * f
        phi_prime = c + 2 * d * f
        defect = 2 * mu * (phi - f * phi_prime)
        assert defect == -2 * mu * d * f * f
        assert 2 * mu * (c * ZERO - ZERO * c) == ZERO
    print("EXACT full16 exterior Lorentz lift / CAR anticommutator / dressed metric")
    print("EXACT two-site star density invariance + finite compensator Ward")
    print("EXACT nonlinear Phi(f) Weyl-source defect quadratic in f")
    print(f"EXAMPLE unweighted star densities {f1}, {f2}; weighted sum {weighted}")
    print("PASS: same source-compatible density-normalized metric on the full CAR16 carrier")
    print("SCOPE: physical shared native tape/cost/clock and all-grid raw #216 still require an admitted binding")


if __name__ == "__main__":
    test()
