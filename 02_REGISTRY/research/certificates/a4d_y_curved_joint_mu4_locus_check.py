#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=600
"""Exact quarter-wave torsion locus of the full curved z=1 joint Bloch symbol.

Builds the literal 96 connection rows and 40 phase-resolved metric rows from
the current curved-Y face Hessian owners. All ranks are exact over Q(i).

This is deliberately a mu_4^4 certificate, not an all-Bloch theorem.
"""
from __future__ import annotations
from itertools import product
import sympy as sp
import a4d_y_curved_response_quotient_check as B
import a4d_y_curved_normaljet_compatibility_check as C

ROOTS=(sp.Integer(1),sp.I,sp.Integer(-1),-sp.I)

def ck(n,c):
    if not c: raise AssertionError(n)
    print("PASS_"+n,flush=True)

def mon(lam,d):
    out=sp.Integer(1)
    for r,e in enumerate(d): out*=lam[r]**e
    return out

# Assemble the literal local data once. The 256 torsion characters below only
# change Laurent monomials; rebuilding the face Hessians would be redundant.
_H,LABELS,FACES0=B.action_connection_hessian(sp.Integer(1))
FACES=C.with_base_phases(FACES0)
IDX={x:i for i,x in enumerate(LABELS)}
UNIT=[B.I4[:,j] for j in range(4)]

def joint_symbol(lam):
    A=sp.zeros(96); Q=sp.zeros(40,96)
    for phase,a,b,locs,local,Hloc,factors in FACES:
        shifts=[(0,0,0,0),tuple(int(r==a) for r in range(4)),
                tuple(int(r==b) for r in range(4)),(0,0,0,0)]
        slot=[]
        for s in shifts: slot += [s]*6
        for ii,(_pi,_gi,gi) in enumerate(local):
            for jj,(_pj,_gj,gj) in enumerate(local):
                d=tuple(slot[jj][r]-slot[ii][r] for r in range(4))
                A[gi,gj]+=Hloc[ii,jj]*mon(lam,d)
        u,v=[j for j in range(4) if j not in (a,b)]
        darea=[]
        for qa,qb in B.SYM:
            dS=B.metric_lift(qa,qb)
            darea.append(B.wedge(dS[:,u],UNIT[v])+B.wedge(UNIT[u],dS[:,v]))
        for pos,(q,role,inverse) in enumerate(locs):
            for g,X in enumerate(B.GEN):
                dFfactor=-X*factors[pos] if inverse else factors[pos]*X
                dP=B.I4
                for n,F in enumerate(factors):
                    dP=dP*(dFfactor if n==pos else F)
                dF=(dP-B.linv(dP))/2
                dFb=B.biv(dF)
                gi=IDX[(q,role,g)]
                phase_factor=mon(lam,shifts[pos])
                for mi,area in enumerate(darea):
                    val=sp.cancel(B.orientation(a,b)*(area.T*B.G2*B.STAR*dFb)[0])
                    Q[10*phase+mi,gi]+=val*phase_factor
    return A.col_join(Q).applyfunc(sp.cancel)

def exact_rank(M):
    return M.to_DM(extension=True).rank()

folded=[]; regular=0
for ids in product(range(4),repeat=4):
    lam=tuple(ROOTS[i] for i in ids)
    R=exact_rank(joint_symbol(lam))
    if R<96:
        folded.append((ids,R))
        ck("SINGULAR_IS_DIAGONAL_"+"".join(map(str,ids)),
           len(set(ids))==1 and R==95)
    else:
        regular+=1

ck("MU4_EXACT_SINGULAR_SET",
   folded==[((j,j,j,j),95) for j in range(4)])
ck("MU4_REGULAR_COUNT_252",regular==252)

for ids,_ in folded:
    M=joint_symbol(tuple(ROOTS[i] for i in ids))
    ns=M.nullspace()
    ck("FOLDED_KERNEL_DIM1_"+str(ids[0]),
       len(ns)==1 and M*ns[0]==sp.zeros(136,1))

print("TERMINAL A4D-Y-CURVED-JOINT-MU4-LOCUS-CERTIFIED")
print("SCOPE exact mu_4^4 torsion grid only; no all-Bloch zero-locus claim")
