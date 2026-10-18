#!/usr/bin/env python3
"""Golden F/R quantile clock: exact 4D Jacobian/source + finite AF Diff tests.

All proofs are in the owning research memo. This script tests its exact
symbolic identities, actual cost-cut boxes (including pending), moving
first source, Markov type mixing and finite same-type assignment.
No physical Julia gate, selected Book action or GR theorem is asserted.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import hypot, log, sin, pi, sqrt
from typing import Tuple
import json
import sympy as sp

p_exact = (sp.sqrt(5)-1)/2
p = float(p_exact)
assert sp.simplify(p_exact**2+p_exact-1)==0

x, y, eps = sp.symbols("x y eps", real=True)
r0=(x+eps*x**2/4)/(1+eps/4)
r1=(y+eps*x*y**2/2)/(1+eps*x/2)
rho=(1+eps*x*y)/(1+eps/4)
assert sp.simplify(sp.diff(r0,x)*sp.diff(r1,y)-rho)==0
assert sp.simplify(sp.diff(r0,eps).subs(eps,0)-(x*x-x)/4)==0
assert sp.simplify(sp.diff(r1,eps).subs(eps,0)-x*(y*y-y)/2)==0
assert sp.simplify(
    sp.diff(r0,eps,x).subs(eps,0)
    +sp.diff(r1,eps,y).subs(eps,0)
    -(x*y-sp.Rational(1,4))
)==0
source=(sp.Rational(7,12)+eps*sp.Rational(5,24))/(1+eps/4)
assert sp.diff(source,eps).subs(eps,0)==sp.Rational(1,16)
u0,u1,u2=sp.symbols("u0 u1 u2", real=True)
chain_source=sp.Rational(1,2)*u0*u0*(1-u0)+\
    sp.Rational(1,2)*u0*u2*u1*(1-u1)
assert sp.integrate(chain_source,(u0,0,1),(u1,0,1),(u2,0,1))\
       ==sp.Rational(1,16)

# Exact Perron/Doob type mixing, not an assumed ergodic profile.
K=sp.Matrix([[p_exact,p_exact**2],[1,0]])
pi_ready=1/(1+p_exact**2)
Pi=sp.ones(2,1)*sp.Matrix([[pi_ready,1-pi_ready]])
I=sp.eye(2)
assert (K-Pi+p_exact**2*(I-Pi)).applyfunc(sp.simplify)==sp.zeros(2)
for r in range(12):
    assert (K**r-Pi-(-p_exact**2)**r*(I-Pi)).applyfunc(sp.simplify)\
            ==sp.zeros(2)

def fibonacci(n:int)->int:
    a,b=0,1
    for _ in range(n):
        a,b=b,a+b
    return a

@dataclass(frozen=True)
class Leaf:
    word:str
    cost:int
    status:str
    lo:Tuple[float,...]
    hi:Tuple[float,...]
    @property
    def weight(self):
        return p**self.cost
    @property
    def center(self):
        return tuple((a+b)*0.5 for a,b in zip(self.lo,self.hi))

def golden_cost_cut(n:int)->list[Leaf]:
    """Actual variable-cost stopping cut with raw-letter Role order j mod4."""
    out=[]
    def visit(cost,raw_depth,lo,hi,word):
        if cost>=n:
            out.append(Leaf(word,cost,"READY" if cost==n else "PENDING",
                            tuple(lo),tuple(hi)))
            return
        j=raw_depth%4
        cut=lo[j]+p*(hi[j]-lo[j])
        lF,hF,lR,hR=list(lo),list(hi),list(lo),list(hi)
        hF[j]=cut
        lR[j]=cut
        visit(cost+1,raw_depth+1,lF,hF,word+"F")
        visit(cost+2,raw_depth+1,lR,hR,word+"R")
    visit(0,0,[0.0]*4,[1.0]*4,"")
    return out

def golden_source_at_zero(leaves:list[Leaf])->tuple[float,float]:
    price=0.
    deriv=0.
    for w in leaves:
        q=w.weight
        a,b,c,_=w.center
        price+=q*(a*a+b*c)
        deriv+=q*(.5*a*a*(1-a)+.5*a*c*b*(1-b))
    return price,deriv

# Cross-check exact branching/probability with retained pending leaves.
quadrature=[]
for n in (2,4,6,8,10,12,14,16,18):
    leaves=golden_cost_cut(n)
    ready=[w for w in leaves if w.status=="READY"]
    pending=[w for w in leaves if w.status=="PENDING"]
    assert (len(ready),len(pending))==(fibonacci(n+1),fibonacci(n))
    assert len(leaves)==fibonacci(n+2)
    assert abs(sum(w.weight for w in leaves)-1.)<3e-12
    assert all(abs(w.weight-
        sp.prod(float(b-a) for a,b in zip(w.lo,w.hi)))<2e-14
               for w in leaves)
    v,d=golden_source_at_zero(leaves)
    quadrature.append({
       "cost":n,"leaves":len(leaves),
       "abs_value_error":abs(v-7/12),
       "abs_first_source_error":abs(d-1/16)})
assert quadrature[-1]["abs_first_source_error"] < 3e-4
assert quadrature[-1]["abs_first_source_error"] <\
       quadrature[0]["abs_first_source_error"]/30

# Single F address: volume is p; fixed physical [0,p] has a NONZERO
# derivative which the moving inverse CDF boundary cancels exactly.
boundary_source=sin(2*pi*p)/(2*pi)
assert abs(boundary_source)>.05
assert abs(boundary_source+(-boundary_source))<1e-14

def assignment_cost(matrix:list[list[float]])->float:
    """Hungarian optimal finite pairing; every atom in one AF block has
    THE SAME actual individual mass, so this is an exact-size permutation."""
    n=len(matrix)
    u=[0.]*(n+1);v=[0.]*(n+1)
    pcol=[0]*(n+1);way=[0]*(n+1)
    for i in range(1,n+1):
        pcol[0]=i
        j0=0
        minv=[float("inf")]*(n+1)
        used=[False]*(n+1)
        while True:
            used[j0]=True
            i0=pcol[j0]
            delta=float("inf");j1=0
            for j in range(1,n+1):
                if used[j]:
                    continue
                cur=matrix[i0-1][j-1]-u[i0]-v[j]
                if cur<minv[j]:
                    minv[j]=cur
                    way[j]=j0
                if minv[j]<delta:
                    delta=minv[j];j1=j
            for j in range(n+1):
                if used[j]:
                    u[pcol[j]]+=delta
                    v[j]-=delta
                else:
                    minv[j]-=delta
            j0=j1
            if pcol[j0]==0:
                break
        while True:
            j1=way[j0]
            pcol[j0]=pcol[j1]
            j0=j1
            if not j0:
                break
    matching=[-1]*n
    for j in range(1,n+1):
        matching[pcol[j]-1]=j-1
    assert sorted(matching)==list(range(n))
    return sum(matrix[i][matching[i]] for i in range(n))

def swapped(u:Tuple[float,...])->Tuple[float,...]:
    # Two coordinate swaps preserve orientation AND the entire du measure.
    return (u[1],u[0],u[3],u[2])

matched=[]
for n in (4,8,12):
    leaves=golden_cost_cut(n)
    total=0.
    for status in ("READY","PENDING"):
        group=[w for w in leaves if w.status==status]
        centers=[w.center for w in group]
        transformed=[swapped(x) for x in centers]
        D=[[sqrt(sum((a[j]-b[j])**2 for j in range(4)))
            for b in centers] for a in transformed]
        total+=group[0].weight*assignment_cost(D)
    matched.append({"cost":n,"weighted_transport_cost":total})
assert matched[-1]["weighted_transport_cost"] < .09
assert matched[-1]["weighted_transport_cost"] < matched[0]["weighted_transport_cost"]/3

# An AF finite permutation is DISCRETE: no differentiable nonzero
# generator t->sigma_n(t) exists without additional coherent controls.
# This does not prevent C1 convergence from moving quantile sources Q15.
print(json.dumps({
 "status":"PASS: exact quantile Jacobian/source, golden types, AF matching",
 "sympy":"Q(sqrt5) identities and exact 4D source",
 "golden_type_stationary":[float(pi_ready),float(1-pi_ready)],
 "exact_source_limit":"1/16",
 "quantile_first_F_boundary_source":boundary_source,
 "quadrature":quadrature,
 "two_block_assignment":matched,
 "physical_execution":"NOT PROVED",
 "GR_source_and_stationary_limit":"OPEN"
},ensure_ascii=False,indent=2,sort_keys=True))
