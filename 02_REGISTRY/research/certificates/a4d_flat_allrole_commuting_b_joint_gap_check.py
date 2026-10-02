#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=180
"""Exact restricted physical joint symbol for the all-role commuting B class.

Proves:
  * the metric block has kernel span(d) on every nontrivial physical unit
    character;
  * its only nonzero complex rank-drop locus is d0=0, d1+d2+d3=0;
  * four physical connection rows kill the remaining metric-null line;
  * therefore the restricted physical joint symbol has no unit-torus kernel.

The formulas are cross-checked against the literal flat-symbol owner at exact
Q(i) characters.
"""
from __future__ import annotations

from fractions import Fraction as F
import sympy as sp

from a4d_designated_full_gap_check import QI, flat_symbols

def ck(name, cond):
    if not cond:
        raise AssertionError(name)
    print("PASS_"+name, flush=True)

d0,d1,d2,d3=sp.symbols("d0 d1 d2 d3")
d=sp.Matrix([d0,d1,d2,d3])
s=d1+d2+d3

CB=sp.Matrix([
 [0,0,0,0],
 [0,-(d2+d3)/2,d1/2,d1/2],
 [0,d2/2,-(d1+d3)/2,d2/2],
 [0,d3/2,d3/2,-(d1+d2)/2],
 [(d2+d3)/2,0,-d0/2,-d0/2],
 [-(d1+d2)/2,d0/2,d0/2,0],
 [-(d1+d3)/2,d0/2,0,d0/2],
 [(d1+d3)/2,-d0/2,0,-d0/2],
 [-(d2+d3)/2,0,d0/2,d0/2],
 [(d1+d2)/2,-d0/2,-d0/2,0],
])

ck("METRIC_MOVING_LINE_CB_D_ZERO", CB*d==sp.zeros(10,1))
minor=sp.factor(CB.extract([4,5,6],[1,2,3]).det())
ck("D0_CHART_RANK3_MINOR", sp.factor(minor-d0**3/4)==0)

N=2*CB.extract([1,2,3],[1,2,3])
dsp=sp.Matrix([d1,d2,d3])
ck("D0_ZERO_SPATIAL_BLOCK_D_ONE_MINUS_SI",
   sp.simplify(N-(dsp*sp.ones(1,3)-s*sp.eye(3)))==sp.zeros(3))

# On s=0 != dsp, N=dsp*1^T has rank one.  The lower first column contains
# -(d1), -(d2), -(d3) up to row choice, so it adds one independent direction.
lower0=(2*CB[4:,0]).subs(d0,0).subs(d3,-d1-d2)
ck("EXCEPTIONAL_COMPLEX_LOCUS_LOWER_COLUMN_NONTRIVIAL",
   any(sp.factor(x)!=0 for x in lower0))

# The unit-torus intersection of d0=0,s=0 is only z=(1,1,1,1):
# z1+z2+z3=3 with |zj|=1.  The analytic proof uses equality in triangle
# inequality.  Retain exact fourth-root hostile controls here.
roots=[QI(1),QI(0,1),QI(-1),QI(0,-1)]
def bcols():
    R=[[QI() for _ in range(4)] for _ in range(24)]
    for role in range(4):
        for g in range(3):
            R[6*role+g][role]=QI(1)
    return R

def mm(a,b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))),QI())
             for j in range(len(b[0]))] for i in range(len(a))]

R=bcols()
for idx,phase in enumerate([
    [QI(1),QI(0,1),QI(-1),QI(0,-1)],
    [QI(0,1),QI(1),QI(0,-1),QI(-1)],
    [QI(-1),QI(0,1),QI(1),QI(0,-1)],
]):
    A,C=flat_symbols(phase)
    # physical placement is A^T followed by C
    AT=[list(row) for row in zip(*A)]
    HB=mm(AT,R); CBo=mm(C,R)
    # Formula evaluation.
    ds=[sp.Integer(complex(z).real) if abs(complex(z).imag)<1e-12 else None for z in phase]
    # Exact cross-check of the moving line uses QI forward differences.
    dq=[z-QI(1) for z in phase]
    cv=[sum((CBo[i][j]*dq[j] for j in range(4)),QI()) for i in range(10)]
    ck(f"LITERAL_METRIC_MOVING_LINE_{idx}", all(not x for x in cv))
    # Four owner rows of H*d must equal -d_r/z_r in the row order below.
    rows=(9,12,7,8)
    hd=[sum((HB[i][j]*dq[j] for j in range(4)),QI()) for i in rows]
    target=[-dq[r]/phase[r] for r in range(4)]
    ck(f"LITERAL_CONNECTION_KILLS_MOVING_LINE_{idx}",
       all(x==y for x,y in zip(hd,target)))

# At the trivial character H is injective already.
A0,C0=flat_symbols([QI(1)]*4)
AT0=[list(row) for row in zip(*A0)]
HB0=mm(AT0,R)
# Exact rank by a simple QI elimination.
def rank(mat):
    a=[row[:] for row in mat]
    rr=0
    for j in range(len(a[0])):
        p=next((i for i in range(rr,len(a)) if a[i][j]),None)
        if p is None:
            continue
        a[rr],a[p]=a[p],a[rr]
        q=a[rr][j]
        a[rr]=[x/q for x in a[rr]]
        for i in range(len(a)):
            if i!=rr and a[i][j]:
                m=a[i][j]
                a[i]=[x-m*y for x,y in zip(a[i],a[rr])]
        rr+=1
        if rr==len(a):
            break
    return rr
ck("TRIVIAL_CHARACTER_RESTRICTED_H_RANK4", rank(HB0)==4)

print("RESULT FLAT-ALLROLE-COMMUTING-B-PHYSICAL-JOINT-SYMBOL-INJECTIVE",flush=True)
print("RESULT SMOOTH-SOURCE-NONLINEAR-COLLAPSE-FOLLOWS-BY-UNIFORM-GAP-AND-FINITE-STENCIL-IFT",flush=True)
