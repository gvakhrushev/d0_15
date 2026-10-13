#!/usr/bin/env python3
"""Same stored soldered operator on an exactly selfadjoint curved-metric class.

Spatial Fourier blocks retain all sixteen exterior components. No bootstrap
heat selection or curved on-shell equation is supplied by this program.
"""
from functools import lru_cache
from itertools import product
import importlib.util
from pathlib import Path
import sys
import sympy as s

spec = importlib.util.spec_from_file_location('homogeneous_soldered_input',
    Path(__file__).with_name('a4d_native_soldered_heat_source.py'))
H = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = H
spec.loader.exec_module(H)

EXTERIOR_ORDER = (0, 2, 3, 1)  # A,C,D,B: actual local roleCode order
JW_ORDER = (0, 1, 2, 3)        # A,B,C,D: actual roleOrderIndex order


@lru_cache(None)
def creator(r, order=EXTERIOR_ORDER):
    C = s.zeros(16)
    predecessors = order[:order.index(r)]
    for mask in range(16):
        if not mask & (1 << r):
            C[mask | (1 << r), mask] = (-1)**sum(bool(mask & (1 << j)) for j in predecessors)
    return C


def basis_phase():
    return s.diag(*[(-1)**(int(bool(m & 2))*(int(bool(m & 4))+int(bool(m & 8))))
                    for m in range(16)])


def shift(L):
    return s.Matrix(L, L, lambda i, j: int(j == (i+1) % L))


def roots(L):
    if L == 2:
        return (1, -1)
    if L == 4:
        return (1, s.I, -1, -s.I)
    raise ValueError('Exact blocks use L=2,4; the theorem covers all L>=2.')


def warp_block(a, momenta, order=EXTERIOR_ORDER):
    """Full L*16 block after Fourier transform in three spatial axes."""
    L = len(a)
    S = shift(L)
    forward = L*(S-s.eye(L))
    reverse_adjoint = forward.T
    C0 = creator(0, order)
    K0 = s.kronecker_product(forward, C0)+s.kronecker_product(reverse_adjoint, C0.T)
    spatial = []
    for r, k in enumerate(momenta, 1):
        z = L*(roots(L)[k]-1)
        Cr = creator(r, order)
        spatial.append(s.kronecker_product(s.eye(L), z*Cr+s.conjugate(z)*Cr.T))
    M = s.kronecker_product(s.diag(*a), s.eye(16))
    D = K0+M*spatial[0]+spatial[1]+spatial[2]
    Delta = D*D
    scalar = [16*t for t in range(L)]
    twoform = [16*t+3 for t in range(L)]  # A wedge B has the same sign in both orders
    return {'D': D, 'Delta': Delta, 'K0': K0, 'K1': spatial[0],
            'K2': spatial[1], 'K3': spatial[2], 'M': M,
            'A': Delta.extract(scalar, scalar),
            'B01': Delta.extract(twoform, scalar),
            'scalar_rows': scalar, 'twoform_rows': twoform}


def scalar_block(a, momenta):
    L = len(a)
    forward = L*(shift(L)-s.eye(L))
    energies = [s.expand(L**2*(roots(L)[k]-1)*(s.conjugate(roots(L)[k])-1)) for k in momenta]
    return forward.T*forward+energies[0]*s.diag(*[x*x for x in a])+(energies[1]+energies[2])*s.eye(L)


def mixing_block(a, k1):
    L = len(a)
    diff = s.diag(*[a[(t+1) % L]-a[t] for t in range(L)])
    return L**2*(roots(L)[k1]-1)*diff*shift(L)


def full_mixing_norm_sq(a):
    L = len(a)
    return 2*L**7*sum((a[(t+1) % L]-a[t])**2 for t in range(L))


def tangent_symbol(k):
    """All allowed raw rows at one Fourier frequency; unweighted metric slots."""
    active = [r for r in range(4) if k[r] == 0]
    columns = []
    for r in active:
        for j in range(4):
            dF = s.zeros(4)
            dF[r, j] = 1
            dq = dF+dF.T
            columns.append(s.Matrix([dq[i, j] for i, j in H.SLOTS]))
    return s.Matrix.hstack(*columns) if columns else s.zeros(10, 0)


def scalar_real_space(a):
    """Literal full four-role weighted graph compression, all L^4 scalar sites."""
    L = len(a)
    sites = list(product(range(L), repeat=4))
    index = {x: i for i, x in enumerate(sites)}
    A = s.MutableSparseMatrix(len(sites), len(sites), {})
    for x in sites:
        i = index[x]
        for r in range(4):
            coefficient = a[x[0]]**2 if r == 1 else 1
            for sign in (-1, 1):
                y = list(x)
                y[r] = (y[r]+sign) % L
                A[i, i] += L**2*coefficient
                A[i, index[tuple(y)]] -= L**2*coefficient
    return A, sites


if __name__ == '__main__':
    a = [3, 2, 1, 2]
    print('Full scalar-to-two-form mixing norm squared:', full_mixing_norm_sq(a))
    print('Curved metric and selfadjoint operator: exact finite class.')
    print('Native heat identification / joint on-shell / GR: OPEN')
