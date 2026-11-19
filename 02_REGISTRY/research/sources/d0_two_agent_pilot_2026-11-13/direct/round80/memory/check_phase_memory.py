"""Literal source slots, hidden cat phase at every local prefix, and a shared reader."""
from collections import Counter
from math import log
from itertools import combinations
from pathlib import Path
import sys

import numpy as np
import sympy as sp

SOURCE = Path(__file__).resolve().parents[4] / 'd0_native_execution_domain_2026-10-24'
sys.path.insert(0, str(SOURCE))
import native_execution as native

GATE = native.Gate
G = np.array(native.G_LOCAL, dtype=float)
CX = np.eye(4)[[0, 1, 3, 2]]
SOURCE_I = np.array(native.SOURCE_I_LOCAL, dtype=float)
V = np.array([float(native.A), float(native.P)])
P = float(native.P)
OPS = {'G': G, 'CX': CX, 'SourceI': SOURCE_I}


def close(actual, expected):
    np.testing.assert_allclose(actual, expected, atol=4e-13, rtol=3e-13, equal_nan=False)


def slot(choice, rail, port, spin):
    c = GATE('CX', (rail, port))
    s = GATE('SourceI', (port, *spin))
    return (c,s,s,c,s,s) if choice else (c,c,s,s,s,s)


def routed(rail, port, spin):
    swap = (GATE('CX', (rail, port)), GATE('CX', (port, rail)), GATE('CX', (rail, port)))
    return swap+(GATE('SourceI', (port, *spin)),)*2+swap


def apply(psi, gate):
    wires = gate.wires
    rest = tuple(j for j in range(psi.ndim) if j not in wires)
    perm = wires + rest
    flat = psi.transpose(perm).reshape(2**len(wires), -1)
    out = np.einsum('ij,jk->ik', OPS[gate.op], flat)
    return out.reshape((2,)*psi.ndim).transpose(np.argsort(perm))


def density(psi, keep):
    keep = tuple(keep)
    rest = tuple(j for j in range(psi.ndim) if j not in keep)
    flat = psi.transpose(keep+rest).reshape(2**len(keep), -1)
    return np.einsum('ik,jk->ij', flat, flat.conj())


def signed_cat(n, sign=1, external=False, balanced=False):
    # Port, Spin, spin reference and private seed reference are additional factors.
    right = np.array([1, 2j, -1, 1j, 1, 0, -1j, 0], dtype=complex)
    right /= np.linalg.norm(right)
    psi = np.zeros((2,)*(n+5), dtype=complex)
    coeff = np.ones(2)/np.sqrt(2) if balanced else V
    overlap = 0.6 if external else 1.0
    for bit, eta in enumerate(([1, 0], [overlap, np.sqrt(1-overlap**2)])):
        tail = np.kron(V, np.kron(right, eta)).reshape((2,)*5)
        psi[(bit,)*n] = coeff[bit]*(sign**bit)*tail
    return psi


def exact_slots():
    words = [slot(i, 0, 1, (2,3)) for i in range(2)]
    assert Counter(words[0]) == Counter(words[1])
    for c, word in enumerate(words):
        ex = native.Execution(4, (), (), word, profile=native.G_CX_SOURCE_I,
                              source_port=1, source_spin=(2,3))
        matrix = native.word_matrix(ex, max_qubits=4, max_expanded_stages=6)
        target = sp.diag(*([1]*8+[(-1)**c]*8))
        assert matrix == target


def prefix_test():
    n = 4
    sources = [signed_cat(n, sign, external=True) for sign in (1, -1)]
    others = tuple(range(n, n+5))
    for words in [slot(0, 1, n, (n+1,n+2)),slot(1, 1, n, (n+1,n+2)),
                  routed(1,n,(n+1,n+2))]:
        pair = list(sources)
        for gate in words:
            pair = [apply(psi, gate) for psi in pair]
            for rails in combinations(range(n), 2):
                close(density(pair[0], rails+others), density(pair[1], rails+others))
    # The routed rail lives in the port after the first three CX.
    pair = list(sources)
    for gate in routed(1,n,(n+1,n+2))[:3]:
        pair = [apply(psi, gate) for psi in pair]
    visible = (0,2,3)+others
    assert np.max(np.abs(density(pair[0], visible)-density(pair[1], visible))) > 0.04


def check_two_blocks():
    n = 3
    cat = np.zeros(2**n)
    cat[0], cat[-1] = V
    second = cat.copy()
    second[-1] *= -1
    # Both alternatives start after the same Z on the second block.
    inp = np.kron(np.kron(cat, second), np.kron(V, [1,0,0,0])).reshape((2,)*(2*n+3))
    pair = [inp, inp]
    for b in (0,1):
        for gate in routed(b*n,2*n,(2*n+1,2*n+2))[:3]:
            pair[b] = apply(pair[b], gate)
    disagree = []
    for psi in pair:
        d = density(psi, (1,2*n))
        disagree.append(d[1,1]+d[2,2])
    close(disagree, [0, 2*P**3])
    local = [density(apply(psi,GATE('G',(0,))), (0,))[1,1] for psi in pair]
    close(local[0]-local[1], 2*P**3)


def check_reader():
    n = 4
    for balanced in (True,False):
        for external in (True,False):
            for sign in (1,-1):
                initial = signed_cat(n, sign, external=external, balanced=balanced)
                psi = initial
                for i in range(n):
                    psi = apply(psi, GATE('CX',(n,i)))
                psi = apply(psi, GATE('G',(n,)))
                m = (1 if balanced else 2*V[0]*V[1])*(0.6 if external else 1)*sign
                close(density(psi,(n,))[1,1], 2*P**3*(1+m))
                if balanced and not external:
                    keep = [i for i in range(psi.ndim) if i != n]
                    close(density(psi,keep), density(initial,keep))
    # NC1 on the balanced pointer; measure only its actual coarse report.
    # All pre-report outputs remain coherent, including the original control T.
    report = (GATE('CX',(0,1)), GATE('CX',(1,2)), GATE('G',(2,)), GATE('CX',(1,2)))
    for sign in (1, -1):
        t = np.einsum('ij,j->i', G, V*np.array([1,sign]))
        bank = np.kron(t, np.kron(V,V)).reshape(2,2,2)
        for gate in report:
            bank = apply(bank,gate)
        # LC1: 10 is a single basis pair; 0 includes both values of the unread tail.
        q = float(np.sum(abs(bank[:,1,0])**2))
        close(np.sum(abs(bank[:,1,1])**2), 0)
        expected = P**2 + (4*P**6 if sign == 1 else 0)
        close(q,expected)
        entropy = -(q*log(q)+(1-q)*log(1-q))/log(1/P)
        divergence = (q*log(q/P**2)+(1-q)*log((1-q)/P))/log(1/P)
        close(1+q-entropy,divergence)
        if sign == 1:
            assert divergence > 0.20
            print('NC1 plus event %.12g, paid letters minus full CQ %.12g' % (q,divergence))
        else:
            close(divergence,0)
    # Golden cat direct cold Gram on the canonical RAW births.
    x_plus = (V[0]**(n+1) + P**(n+1))**2
    x_minus = (V[0]**(n+1) - P**(n+1))**2
    close(2*(x_plus-x_minus), 8*(V[0]*P)**(n+1))
    print('n = 4; Gram rectangle %.12g; balanced pointer contrast %.12g'
          % (2*(x_plus-x_minus), 4*P**3))


if __name__ == '__main__':
    exact_slots()
    prefix_test()
    check_two_blocks()
    check_reader()
    print('six-stage signed slot; all SWAP and SourceI prefixes; two-block witness; protected reader verified')
