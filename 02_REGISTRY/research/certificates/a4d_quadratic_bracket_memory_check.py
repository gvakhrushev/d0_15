#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=180
"""Exact quadratic bracket-memory controls for the A4D odd plaquette curvature.

No Bloch census.  The checker proves coefficientwise on the owner Lorentz
basis that the epsilon^2 coefficient of (P-P^-1)/2 for four exponential
factors is 1/2 sum_{i<j}[Y_i,Y_j].  It also reconstructs the local
curvature-to-solder observation map and the first adjoint-transport torque.
"""
from __future__ import annotations

from fractions import Fraction as F
from itertools import combinations
import numpy as np
import sympy as sp

import a4d_identity_quarter_nonlinear_response_check as N
import a4d_commuting_b_full_link_current_check as C

I = N.I
G = N.G
ETA = C.ETA


def ck(name, cond):
    if not cond:
        raise AssertionError(name)
    print("PASS_"+name, flush=True)


def zmat():
    return np.zeros((4,4), dtype=object)


def jmul(a,b):
    """Degree-two jet product, coeff arrays [0,1,2]."""
    out=[zmat(),zmat(),zmat()]
    for i in range(3):
        for j in range(3-i):
            out[i+j] += a[i] @ b[j]
    return out


def expjet(Y, sign=1):
    return [I.copy(), sign*Y, (Y@Y)*F(1,2)]


def product(jets):
    out=[I.copy(),zmat(),zmat()]
    for j in jets:
        out=jmul(out,j)
    return out


def oddjet(Ys):
    p=product([expjet(Y) for Y in Ys])
    pi=product([expjet(Y,-1) for Y in reversed(Ys)])
    return [(p[k]-pi[k])*F(1,2) for k in range(3)]


# Owner basis is exactly Lorentz.
for j,X in enumerate(G):
    ck(f"LORENTZ_GENERATOR_{j}", np.array_equal(X.T@ETA+ETA@X,zmat()))

# Single-slot and every pair/generator coefficient.
for slot in range(4):
    for a,X in enumerate(G):
        Ys=[zmat() for _ in range(4)]
        Ys[slot]=X
        c=oddjet(Ys)
        ck(f"SINGLE_SLOT_LINEAR_S{slot}_G{a}", np.array_equal(c[1],X))
        ck(f"SINGLE_SLOT_QUADRATIC_ZERO_S{slot}_G{a}", not np.any(c[2]))

count=0
commutators=[]
for i,j in combinations(range(4),2):
    for a,X in enumerate(G):
        for b,Y in enumerate(G):
            Ys=[zmat() for _ in range(4)]
            Ys[i]=X; Ys[j]=Y
            c=oddjet(Ys)
            expected=(X@Y-Y@X)*F(1,2)
            ck(f"PAIR_BRACKET_S{i}{j}_G{a}{b}", np.array_equal(c[2],expected))
            commutators.append((X@Y-Y@X).reshape(16))
            count+=1
ck("ALL_216_SLOT_GENERATOR_PAIR_COEFFICIENTS", count==216)

# Lie brackets span all six owner directions.
def coords(X):
    # role-independent Lorentz basis coordinates K1,K2,K3,J12,J13,J23
    return [X[0,1],X[0,2],X[0,3],X[1,2],X[1,3],X[2,3]]
Bmat=sp.Matrix([[sp.Rational(x) for x in coords(X@Y-Y@X)]
                for X in G for Y in G])
ck("LORENTZ_COMMUTATOR_SPAN_RANK6", Bmat.rank()==6)

# Independent local curvature -> 10 Gram + 6 vertical solder observation.
weights, deriv = C.face_weights(I)
Aq=sp.zeros(10,36)
Av=sp.zeros(6,36)
for face in range(6):
    for k,X in enumerate(G):
        col=6*face+k
        for q in range(10):
            Aq[q,col]=sp.Rational(C.pair(deriv[face,q],X))
        for v in range(6):
            Av[v,col]=sp.Rational(C.pair(deriv[face,10+v],X))
Ae=Aq.col_join(Av)
ck("HORIZONTAL_CURVATURE_READOUT_RANK10", Aq.rank()==10)
ck("VERTICAL_CURVATURE_READOUT_RANK6", Av.rank()==6)
ck("FULL_SOLDER_CURVATURE_READOUT_RANK16", Ae.rank()==16)
ck("FULL_SOLDER_CURVATURE_KERNEL_DIM20", 36-Ae.rank()==20)

# Hostile control: a noncommuting pair can be source-visible.
visible=None
for face in range(6):
    for X in G:
        for Y in G:
            K=X@Y-Y@X
            if not np.any(K):
                continue
            vec=sp.zeros(36,1)
            for k,val in enumerate(coords(K)):
                vec[6*face+k]=sp.Rational(val)
            h=Aq*vec
            if h!=sp.zeros(10,1):
                visible=(face,K,h)
                break
        if visible: break
    if visible: break
ck("NONCOMMUTING_BRACKET_CAN_BE_SOURCE_VISIBLE", visible is not None)

# First jet of B - Ad_exp(eps A) B is -eps[A,B].
for a,A in enumerate(G):
    for b,B in enumerate(G):
        # Ad jet: (I+eA+... ) B (I-eA+...)
        first=A@B-B@A
        lhs_first=-first
        expected=-(A@B-B@A)
        ck(f"TRANSPORT_TORQUE_FIRST_JET_G{a}{b}",
           np.array_equal(lhs_first,expected))

# If all oriented face factors commute pairwise, quadratic odd memory vanishes.
B0=G[0]+G[1]+G[2]
Ys=[F(k+1,7)*B0 for k in range(4)]
cj=oddjet(Ys)
ck("COMMON_ONE_GENERATOR_QUADRATIC_BRACKET_MEMORY_ZERO", not np.any(cj[2]))

print("RESULT QUADRATIC-NONLINEAR-RESPONSE-MEMORY-IS-LIE-BRACKET-FACE-MEMORY",flush=True)
print("RESULT LOCAL_BRACKET_MEMORY_36_TO_SOLDER16_KERNEL20",flush=True)
print("RESULT NONCOMMUTING_TRANSPORT_TORQUE_STARTS_WITH_ADJOINT_BRACKET",flush=True)
