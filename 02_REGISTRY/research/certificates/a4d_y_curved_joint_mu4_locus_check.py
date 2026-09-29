#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=600
"""Certified mu_4^4 locus of the full curved z=1 joint Bloch symbol.

Literal 96 connection + 40 metric rows are compiled as a Laurent stencil.
Full column rank is certified modulo a good Gaussian prime; rank 95 and the
kernel at the four diagonal folded characters are then checked exactly over
Q(i).  Modular full rank is rigorous: a nonzero 96-minor modulo p is a
nonzero characteristic-zero minor after denominator clearing.

Scope: mu_4^4 only, not an all-Bloch theorem.
"""
from __future__ import annotations
from collections import defaultdict
from itertools import product
import sympy as sp
import a4d_y_curved_response_quotient_check as B
import a4d_y_curved_normaljet_compatibility_check as C

ROOTS=(sp.Integer(1),sp.I,sp.Integer(-1),-sp.I)
P=1_000_033  # P == 1 mod 4, so sqrt(-1) exists in F_P.
I_MOD=pow(P-1,(P+1)//4,P) if False else None

def ck(n,c):
    if not c: raise AssertionError(n)
    print("PASS_"+n,flush=True)

# Find an exact square root of -1 modulo P without external dependencies.
def sqrt_minus_one(p):
    for g in range(2,100):
        x=pow(g,(p-1)//4,p)
        if x*x%p==p-1: return x
    raise AssertionError("no sqrt(-1) found")
IM=sqrt_minus_one(P)

_H,LABELS,FACES0=B.action_connection_hessian(sp.Integer(1))
FACES=C.with_base_phases(FACES0)
IDX={x:i for i,x in enumerate(LABELS)}
UNIT=[B.I4[:,j] for j in range(4)]
ATERMS=defaultdict(lambda:sp.zeros(96))
QTERMS=defaultdict(lambda:sp.zeros(40,96))

for phase,a,b,locs,local,Hloc,factors in FACES:
    shifts=[(0,0,0,0),tuple(int(r==a) for r in range(4)),
            tuple(int(r==b) for r in range(4)),(0,0,0,0)]
    slot=[]
    for s in shifts: slot += [s]*6
    for ii,(_pi,_gi,gi) in enumerate(local):
        for jj,(_pj,_gj,gj) in enumerate(local):
            d=tuple(slot[jj][r]-slot[ii][r] for r in range(4))
            ATERMS[d][gi,gj]+=Hloc[ii,jj]
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
            for mi,area in enumerate(darea):
                val=sp.cancel(B.orientation(a,b)*(area.T*B.G2*B.STAR*dFb)[0])
                QTERMS[shifts[pos]][10*phase+mi,gi]+=val

def mon(lam,d):
    out=1
    for r,e in enumerate(d): out*=lam[r]**e
    return out

def joint_symbol(lam):
    A=sum((mon(lam,d)*M for d,M in ATERMS.items()),sp.zeros(96))
    Q=sum((mon(lam,d)*M for d,M in QTERMS.items()),sp.zeros(40,96))
    return A.col_join(Q)

def qmod(x):
    x=sp.cancel(x)
    num,den=sp.fraction(x)
    # At mu_4 points entries lie in Q(i); substitute i -> IM in F_P.
    num=int(sp.Poly(num,sp.I,extension=sp.I).eval(IM))%P if num.has(sp.I) else int(num)%P
    den=int(sp.Poly(den,sp.I,extension=sp.I).eval(IM))%P if den.has(sp.I) else int(den)%P
    if den==0: raise AssertionError("bad modular denominator")
    return num*pow(den,P-2,P)%P

def rank_mod(M):
    A=[[qmod(M[i,j]) for j in range(M.cols)] for i in range(M.rows)]
    row=0
    for col in range(M.cols):
        pivot=next((r for r in range(row,M.rows) if A[r][col]),None)
        if pivot is None: continue
        A[row],A[pivot]=A[pivot],A[row]
        inv=pow(A[row][col],P-2,P)
        A[row]=[(v*inv)%P for v in A[row]]
        for r in range(row+1,M.rows):
            if A[r][col]:
                q=A[r][col]
                A[r]=[(u-q*v)%P for u,v in zip(A[r],A[row])]
        row+=1
        if row==M.cols: break
    return row

ck("JOINT_SHAPE",joint_symbol(ROOTS).shape==(136,96))
candidates=[]; regular=0
for ids in product(range(4),repeat=4):
    M=joint_symbol(tuple(ROOTS[i] for i in ids))
    r=rank_mod(M)
    if r==96:
        regular+=1
    else:
        candidates.append((ids,r))

expected=[((j,j,j,j),95) for j in range(4)]
ck("MODULAR_CANDIDATES_ONLY_FOLDED",candidates==expected)
ck("MODULAR_FULL_RANK_COUNT_252",regular==252)

for ids,_ in candidates:
    M=joint_symbol(tuple(ROOTS[i] for i in ids))
    r=M.to_DM(extension=True).rank()
    ck("FOLDED_EXACT_RANK95_"+str(ids[0]),r==95)
    ns=M.nullspace()
    ck("FOLDED_EXACT_KERNEL_DIM1_"+str(ids[0]),
       len(ns)==1 and M*ns[0]==sp.zeros(136,1))

print("TERMINAL A4D-Y-CURVED-JOINT-MU4-LOCUS-CERTIFIED")
print("MODULUS",P,"I_MOD",IM)
print("SCOPE exact mu_4^4 torsion grid only; no all-Bloch zero-locus claim")
