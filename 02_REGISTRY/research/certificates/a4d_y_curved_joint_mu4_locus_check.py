#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=180
"""Exact mu_4^4 locus of the full curved z=1 joint Bloch symbol.

The literal 96 connection rows and 40 phase-resolved metric rows are assembled
directly over F_65537.  Since 65537 is prime and 256^2=-1 mod 65537, all four
quarter-wave characters 1,i,-1,-i are represented exactly.  Full rank modulo
p proves full rank in characteristic zero.  At folded points the modular rank
is 95; merged #232 (merge caa1e65087ddf15cda35325189ebfcbf51a56592)
supplies the exact nonzero Y tangent in the joint kernel, giving the matching
characteristic-zero upper bound.  Hence the exact characteristic-zero rank is
95 at the four folded diagonal characters and 96 at the other 252 mu_4^4
characters.

Scope: exact mu_4^4 torsion grid only.  This is not an all-Bloch theorem.
"""
from __future__ import annotations
from collections import defaultdict
from itertools import combinations, product
import json
from pathlib import Path
import numpy as np

P=65537
IROOT=256
INV2=pow(2,-1,P)
ROOTS=(1,IROOT,P-1,P-IROOT)
OUT=Path(__file__).with_name("a4d_y_curved_joint_mu4_locus_results.json")

def check(name,cond):
    if not cond:
        raise AssertionError(name)
    print("PASS_"+name,flush=True)

check("PRIME_FERMAT_65537",P==65537)
check("IROOT_SQUARE_MINUS_ONE",IROOT*IROOT%P==P-1)

I4=np.eye(4,dtype=np.int64)
ETA=np.diag([1,-1,-1,-1]).astype(np.int64)%P
PAIRS=list(combinations(range(4),2))
SYM=[(a,b) for a in range(4) for b in range(a,4)]

GEN=[]
for j in (1,2,3):
    X=np.zeros((4,4),dtype=np.int64)
    X[0,j]=X[j,0]=1
    GEN.append(X)
for a,b in ((1,2),(1,3),(2,3)):
    X=np.zeros((4,4),dtype=np.int64)
    X[a,b]=1
    X[b,a]=-1
    GEN.append(X%P)

G2=np.diag([(1 if (a==0)==(b==0) else -1) for a,b in PAIRS]).astype(np.int64)%P
STAR=np.zeros((6,6),dtype=np.int64)
for col,(row,sign) in enumerate(((5,-1),(4,1),(3,-1),(2,1),(1,-1),(0,1))):
    STAR[row,col]=sign%P

def mm(A,B):
    return (A@B)%P

def linv(M):
    return mm(mm(ETA,M.T),ETA)

def invmat(A):
    A=A.copy()%P
    n=A.shape[0]
    B=np.eye(n,dtype=np.int64)
    for c in range(n):
        piv=next(r for r in range(c,n) if A[r,c]%P)
        if piv!=c:
            A[[c,piv]]=A[[piv,c]]
            B[[c,piv]]=B[[piv,c]]
        q=pow(int(A[c,c]),-1,P)
        A[c]=(A[c]*q)%P
        B[c]=(B[c]*q)%P
        for r in range(n):
            if r==c:
                continue
            q=int(A[r,c])
            if q:
                A[r]=(A[r]-q*A[c])%P
                B[r]=(B[r]-q*B[c])%P
    return B%P

def wedge(u,v):
    return np.array(
        [(int(u[a])*int(v[b])-int(u[b])*int(v[a]))%P for a,b in PAIRS],
        dtype=np.int64,
    )

def biv(M):
    X=mm(M,ETA)
    return np.array([X[a,b]%P for a,b in PAIRS],dtype=np.int64)

def orient(a,b):
    seq=[a,b]+[j for j in range(4) if j not in (a,b)]
    inv=sum(seq[i]>seq[j] for i in range(4) for j in range(i+1,4))
    return -1 if inv%2 else 1

def prodm(items):
    out=I4
    for x in items:
        out=mm(out,x)
    return out

def cayley_y():
    Y=(GEN[3]-GEN[4]+GEN[5])%P
    return mm(invmat((I4-INV2*Y)%P),(I4+INV2*Y)%P)

def metric_lift(a,b):
    q=np.zeros((4,4),dtype=np.int64)
    q[a,b]=q[b,a]=1
    return mm(ETA,q)*INV2%P

U=cayley_y()
W=[U,I4,linv(U),I4]
LABELS=[(ph,role,g) for ph in range(4) for role in range(4) for g in range(6)]
IDX={x:i for i,x in enumerate(LABELS)}
BASIS=[I4[:,j] for j in range(4)]
ATERMS=defaultdict(lambda:np.zeros((96,96),dtype=np.int64))
QTERMS=defaultdict(lambda:np.zeros((40,96),dtype=np.int64))

for phase in range(4):
    for a,b in PAIRS:
        locs=[
            (phase,a,False),
            ((phase+1)%4,b,False),
            ((phase+1)%4,a,True),
            (phase,b,True),
        ]
        factors=[]
        first=[]
        for q,role,inverse in locs:
            K=W[q] if role==0 else I4
            F=linv(K) if inverse else K
            factors.append(F)
            first.append([((-mm(X,F)) if inverse else mm(F,X))%P for X in GEN])

        local=[]
        for pos,(q,role,_inverse) in enumerate(locs):
            for g in range(6):
                local.append((pos,g,IDX[(q,role,g)]))

        u,v=[j for j in range(4) if j not in (a,b)]
        area=wedge(BASIS[u],BASIS[v])
        Hloc=np.zeros((24,24),dtype=np.int64)
        for ii,(pi,gi,_x) in enumerate(local):
            for jj in range(ii,24):
                pj,gj,_y=local[jj]
                if pi==pj:
                    Q=(mm(GEN[gi],GEN[gj])+mm(GEN[gj],GEN[gi]))*INV2%P
                    Q=mm(Q,factors[pi]) if locs[pi][2] else mm(factors[pi],Q)
                    items=[Q if n==pi else factors[n] for n in range(4)]
                else:
                    items=[
                        first[n][gi] if n==pi
                        else first[n][gj] if n==pj
                        else factors[n]
                        for n in range(4)
                    ]
                d2P=prodm(items)
                d2F=(d2P-linv(d2P))*INV2%P
                val=int(area @ mm(G2,mm(STAR,biv(d2F).reshape(6,1))).reshape(6))%P
                if orient(a,b)<0:
                    val=(-val)%P
                Hloc[ii,jj]=Hloc[jj,ii]=val

        shifts=[
            (0,0,0,0),
            tuple(int(r==a) for r in range(4)),
            tuple(int(r==b) for r in range(4)),
            (0,0,0,0),
        ]
        slot=[]
        for s in shifts:
            slot += [s]*6
        for ii,(_pi,_gi,ggi) in enumerate(local):
            for jj,(_pj,_gj,ggj) in enumerate(local):
                d=tuple(slot[jj][r]-slot[ii][r] for r in range(4))
                ATERMS[d][ggi,ggj]=(ATERMS[d][ggi,ggj]+Hloc[ii,jj])%P

        darea=[]
        for qa,qb in SYM:
            dS=metric_lift(qa,qb)
            darea.append((wedge(dS[:,u],BASIS[v])+wedge(BASIS[u],dS[:,v]))%P)

        for pos,(q,role,inverse) in enumerate(locs):
            for g,X in enumerate(GEN):
                dFfactor=(-mm(X,factors[pos]))%P if inverse else mm(factors[pos],X)
                items=[dFfactor if n==pos else factors[n] for n in range(4)]
                dP=prodm(items)
                dF=(dP-linv(dP))*INV2%P
                db=biv(dF)
                gidx=IDX[(q,role,g)]
                for mi,ar in enumerate(darea):
                    val=int(ar @ mm(G2,mm(STAR,db.reshape(6,1))).reshape(6))%P
                    if orient(a,b)<0:
                        val=(-val)%P
                    QTERMS[shifts[pos]][10*phase+mi,gidx]=(
                        QTERMS[shifts[pos]][10*phase+mi,gidx]+val
                    )%P

def mpow(x,e):
    if e>=0:
        return pow(int(x),e,P)
    return pow(pow(int(x),-1,P),-e,P)

def eval_joint(lam):
    M=np.zeros((136,96),dtype=np.int64)
    for d,A in ATERMS.items():
        ph=1
        for r,e in enumerate(d):
            ph=ph*mpow(lam[r],e)%P
        M[:96]=(M[:96]+ph*A)%P
    for d,Q in QTERMS.items():
        ph=1
        for r,e in enumerate(d):
            ph=ph*mpow(lam[r],e)%P
        M[96:]=(M[96:]+ph*Q)%P
    return M

def rank_mod(A):
    A=A.copy()%P
    nr,nc=A.shape
    r=0
    for c in range(nc):
        nz=np.flatnonzero(A[r:,c])
        if not len(nz):
            continue
        q=r+int(nz[0])
        if q!=r:
            A[[r,q]]=A[[q,r]]
        inv=pow(int(A[r,c]),-1,P)
        A[r]=(A[r]*inv)%P
        rows=np.flatnonzero((np.arange(nr)!=r)&(A[:,c]!=0))
        if len(rows):
            A[rows]=(A[rows]-A[rows,c,None]*A[r,None,:])%P
        r+=1
        if r==nc:
            break
    return r

M1=eval_joint((1,1,1,1))
check("FOLDED_CONNECTION_RANK94_MOD_P",rank_mod(M1[:96])==94)
check("FOLDED_JOINT_RANK95_MOD_P",rank_mod(M1)==95)

# Reduction of the exact #232 Y tangent.  Overall rational Cayley scale is
# irrelevant for the kernel test.
ny=np.zeros(96,dtype=np.int64)
for phase,sgn in ((0,1),(2,-1)):
    for g,coeff in ((3,1),(4,-1),(5,1)):
        ny[IDX[(phase,0,g)]]=sgn*coeff%P
check("FOLDED_Y_TANGENT_REDUCES_TO_KERNEL",np.all((M1@ny)%P==0))

folded=[]
counts={}
for ids in product(range(4),repeat=4):
    r=rank_mod(eval_joint(tuple(ROOTS[i] for i in ids)))
    counts[r]=counts.get(r,0)+1
    if r<96:
        folded.append((ids,r))

expected=[((j,j,j,j),95) for j in range(4)]
check("MU4_ONLY_FOLDED_DIAGONAL_SINGULAR",folded==expected)
check("MU4_FULL_RANK_COUNT_252",counts=={95:4,96:252})

result={
    "schema":"a4d-y-curved-joint-mu4-locus-v1",
    "terminal":"A4D-Y-CURVED-JOINT-MU4-LOCUS-CERTIFIED",
    "background":"z=1 exact Y vacuum; standard solder",
    "joint_symbol_shape":[136,96],
    "prime":P,
    "sqrt_minus_one_mod_prime":IROOT,
    "modular_rank_counts":{"95":4,"96":252},
    "folded_character_ids":[list(x[0]) for x in expected],
    "folded_characters":["(1,1,1,1)","(i,i,i,i)","(-1,-1,-1,-1)","(-i,-i,-i,-i)"],
    "folded_connection_rank_mod_p":94,
    "folded_joint_rank_mod_p":95,
    "characteristic_zero_argument":{
        "regular_points":"rank mod p = 96 implies characteristic-zero rank 96",
        "folded_points":"rank mod p = 95 gives lower bound 95; merged #232 exact nonzero Y joint-kernel tangent gives upper bound 95; diagonal zone folding identifies the four physical copies",
        "exact_kernel_owner":"PR #232 merge caa1e65087ddf15cda35325189ebfcbf51a56592"
    },
    "conclusion":"on mu_4^4 the full curved joint symbol has exact rank 95 only at the four folded diagonal characters and rank 96 at all other 252 characters",
    "scope_fence":[
        "exact mu_4^4 torsion grid only",
        "no all-Bloch complex or unit-torus zero-locus theorem",
        "no uniform singular-value lower bound between sampled characters",
        "no nonlinear range theorem or task-level response terminal"
    ]
}
if OUT.exists():
    check("RESULTS_MATCH_PINNED_JSON",json.loads(OUT.read_text())==result)
else:
    OUT.write_text(json.dumps(result,indent=2)+"\n")
    print("WROTE",OUT,flush=True)

print("TERMINAL A4D-Y-CURVED-JOINT-MU4-LOCUS-CERTIFIED")
