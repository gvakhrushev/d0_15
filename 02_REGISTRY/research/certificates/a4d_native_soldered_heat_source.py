#!/usr/bin/env python3
"""Literal homogeneous soldered-CAR symbols and their finite heat covector.

The bootstrap identification of this operator square remains an explicit
interface. This program does not define a physical Gibbs preparation.
"""
from functools import lru_cache
from itertools import combinations, product
import sympy as s

ETA = s.diag(1, -1, -1, -1)
SLOTS = tuple((i, j) for i in range(4) for j in range(i, 4))
BLADES = tuple(tuple(i for i in range(4) if mask & (1 << i)) for mask in range(16))


@lru_cache(None)
def creator(i):
    C = s.zeros(16)
    for mask in range(16):
        if not (mask & (1 << i)):
            C[mask | (1 << i), mask] = (-1) ** sum(j < i for j in BLADES[mask])
    return C


def create(v):
    return sum((v[i] * creator(i) for i in range(4)), s.zeros(16))


def contract(covector):
    return sum((covector[i] * creator(i).T for i in range(4)), s.zeros(16))


def observer(n):
    return -ETA + 2 * (ETA*n) * (ETA*n).T


def exterior_gram(h):
    return s.Matrix(16, 16, lambda i, j: 0 if len(BLADES[i]) != len(BLADES[j])
                    else h.extract(BLADES[i], BLADES[j]).det())


def symbol(F, n, z):
    h = observer(n)
    D = s.zeros(16)
    for r in range(4):
        leg = ETA * F.row(r).T
        D += z[r]*create(leg) + s.conjugate(z[r])*contract(h*leg)
    return D


def positive_symbol(q, v):
    sigma = (v.T*q.inv()*v)[0]
    return -q + 2*v*v.T/sigma


def symbol_tangent(q, v, H):
    w = q.inv()*v
    sigma = (v.T*w)[0]
    return -H + 2*v*v.T*(w.T*H*w)[0]/sigma**2


def source(q, v, W):
    w = q.inv()*v
    sigma = (v.T*w)[0]
    return W - 2*(v.T*W*v)[0]*w*w.T/sigma**2


def observer_source(q, v, W):
    w = q.inv()*v
    sigma = (v.T*w)[0]
    return -4*W*v/sigma + 4*(v.T*W*v)[0]*w/sigma**2


def joint_tangent(q, v, H, u):
    w = q.inv()*v
    sigma = (v.T*w)[0]
    ds = 2*(w.T*u)[0] - (w.T*H*w)[0]
    return -H + 2*(u*v.T+v*u.T)/sigma - 2*ds*v*v.T/sigma**2


def basis(slot):
    i, j = slot
    B = s.zeros(4)
    B[i, j] = B[j, i] = 1
    return B


def pack(M):
    return s.Matrix([M[i, j]*(1 if i == j else 2) for i, j in SLOTS])


def feature(z):
    W = s.re(z*z.conjugate().T)
    return pack(W)


def modes(L):
    if L == 2:
        roots = [1, -1]
    elif L == 4:
        roots = [1, s.I, -1, -s.I]
    else:
        raise ValueError('Exact replay uses L=2,4; all-L proof is analytic.')
    for k in product(range(L), repeat=4):
        yield k, s.Matrix([L*(roots[j]-1) for j in k])


def exact_heat(diagonal, L=4):
    """beta=log(2)/32, L=4 and integer positive diagonal: rational weights."""
    if L != 4 or any(d <= 0 or int(d) != d for d in diagonal):
        raise ValueError('Exact rational thermal slice requires positive integer diagonal and L=4.')
    Z = s.S.Zero
    W = s.zeros(4)
    m = s.zeros(10, 1)
    m2 = s.zeros(10)
    for _, z in modes(L):
        energy = (z.conjugate().T*s.diag(*diagonal)*z)[0].expand()
        weight = s.Rational(2)**(-energy/32)
        f = feature(z)
        Z += weight
        W += weight*s.re(z*z.conjugate().T)
        m += weight*f
        m2 += weight*f*f.T
    W /= Z
    m /= Z
    return {'scalar_partition': Z, 'full_partition': 16*Z,
            'W': W, 'mean_features': m, 'covariance': m2/Z-m*m.T}


def variable_axis(L, legs):
    S = s.zeros(L)
    for x in range(L):
        S[x, (x+1) % L] = 1
    M = s.diag(*legs)
    forward = L*M*(S-s.eye(L))
    stored_backward = -L*M*(s.eye(L)-S.T)
    return forward, stored_backward


if __name__ == '__main__':
    result = exact_heat([1, 1, 1, 1])
    print('Homogeneous square interface; beta=log(2)/32, L=4')
    print('Packed q covector:', list(pack(source(ETA, s.eye(4)[:, 0], result['W']))))
    print('Native bootstrap binding / curved full source / GR: OPEN')
