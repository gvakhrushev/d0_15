#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=600
"""Exact mu_4^4 locus of the full curved z=1 joint Bloch symbol.

The literal 96 connection rows and 40 phase-resolved metric rows are compiled
as a rational Laurent stencil.  Full rank is certified by reduction modulo
p=65537 (where 256^2=-1), which is a rigorous lower bound for characteristic
zero because no denominator vanishes mod p.  At the four folded diagonal
characters an explicit exact Y kernel supplies the matching upper bound.

Terminal is intentionally only the mu_4^4 torsion grid, not all Bloch phases.
"""
from __future__ import annotations
from collections import defaultdict
from itertools import product
import numpy as np
import sympy as sp
import a4d_y_curved_response_quotient_check as B
import a4d_y_curved_normaljet_compatibility_check as C

P=65537
I_P=256
ROOTS_EX=(sp.Integer(1),sp.I,sp.Integer(-1),-sp.I)
ROOTS_P=(1,I_P,P-1,P-I_P)

def ck(n,c):
    if not c: raise AssertionError(n)
    print("PASS_"+n,flush=True)

def mon(lam,d):
    out=1
    for r,e in enumerate(d): out*=lam[r]**e
    return out

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

def modq(x):
    x=sp.Rational(x)
    den=int(x.q)
    ck("DENOMINATOR_NONZERO_MOD_P",den%P!=0)
    return (int(x.p)%P)*pow(den,-1,P)%P

# Convert each rational Laurent coefficient matrix once.
MODTERMS={}
for d in set(ATERMS)|set(QTERMS):
    M=ATERMS.get(d,sp.zeros(96)).col_join(QTERMS.get(d,sp.zeros(40,96)))
    A=np.zeros((136,96),dtype=np.int64)
    for i,j in zip(*M.todok().keys()) if False else []:
        pass
    for (i,j),x in M.todok().items():
        A[i,j]=modq(x)
    MODTERMS[d]=A

def rank_mod(lam):
    A=np.zeros((136,96),dtype=np.int64)
    for d,M in MODTERMS.items():
        phase=1
        for r,e in enumerate(d):
            if e>=0:
                phase=phase*pow(int(lam[r]),e,P)%P
            else:
                phase=phase*pow(pow(int(lam[r]),-1,P),-e,P)%P
        A=(A+phase*M)%P
    rank=0
    for col in range(96):
        nz=np.flatnonzero(A[rank:,col])
        if not len(nz): continue
        q=rank+int(nz[0])
        if q!=rank: A[[rank,q]]=A[[q,rank]]
        inv=pow(int(A[rank,col]),-1,P)
        A[rank]=(A[rank]*inv)%P
        mask=np.arange(136)!=rank
        factors=A[:,col].copy()
        rows=np.flatnonzero(mask & (factors!=0))
        if len(rows):
            A[rows]=(A[rows]-factors[rows,None]*A[rank][None,:])%P
        rank+=1
        if rank==96: break
    return rank

# Exact lambda=1 joint matrix and its Y center.
def joint_exact(lam):
    A=sum((mon(lam,d)*M for d,M in ATERMS.items()),sp.zeros(96))
    Q=sum((mon(lam,d)*M for d,M in QTERMS.items()),sp.zeros(40,96))
    return A.col_join(Q)

M1=joint_exact((1,1,1,1))
H1=M1[:96,:]
C1=M1[96:,:]
N=C.centers(_H,LABELS,sp.Integer(1))
ny,nd=N[:,0],N[:,1]
ck("FOLDED_Y_EXACT_KERNEL_AT_ONE",M1*ny==sp.zeros(136,1))
ck("DUAL_REMOVED_BY_METRIC_ROWS",H1*nd==sp.zeros(96,1) and C1*nd!=sp.zeros(40,1))
ck("MU4_ONE_MODULAR_RANK95",rank_mod((1,1,1,1))==95)

folded=[]; regular=0
for ids in product(range(4),repeat=4):
    rp=rank_mod(tuple(ROOTS_P[i] for i in ids))
    if rp<96:
        folded.append((ids,rp))
    else:
        regular+=1
ck("MU4_MODULAR_SINGULAR_SET",
   folded==[((j,j,j,j),95) for j in range(4)])
ck("MU4_REGULAR_COUNT_252",regular==252)

# Exact diagonal zone folding:
# A(zeta)=D^-1 A(1) D, C(zeta)=R^-1 C(1) D.
for j,zeta in enumerate(ROOTS_EX):
    D=sp.diag(*[zeta**phase for phase,role,g in LABELS])
    R=sp.diag(*sum(([zeta**phase]*10 for phase in range(4)),[]))
    lam=(zeta,zeta,zeta,zeta)
    M=joint_exact(lam)
    ck("FOLDED_CONNECTION_SIMILARITY_"+str(j),
       M[:96,:]==D.inv()*H1*D)
    ck("FOLDED_METRIC_SIMILARITY_"+str(j),
       M[96:,:]==R.inv()*C1*D)
    x=D.inv()*ny
    ck("FOLDED_EXACT_Y_KERNEL_"+str(j),M*x==sp.zeros(136,1))
    # rank_mod=95 gives rank_Q >=95; exact nonzero kernel gives rank_Q <=95.
    ck("FOLDED_EXACT_RANK95_"+str(j),
       rank_mod(tuple(ROOTS_P[j] for _ in range(4)))==95 and x!=sp.zeros(96,1))

print("TERMINAL A4D-Y-CURVED-JOINT-MU4-LOCUS-CERTIFIED")
print("RESULT exact char-0 rank 96 at 252 mu4 points and rank 95 at the four folded diagonal points")
print("SCOPE exact mu_4^4 torsion grid only; no all-Bloch zero-locus claim")
