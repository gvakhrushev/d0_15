#!/usr/bin/env python3
"""Reusable exact rational Laurent stencil for the curved z=1 Y joint symbol.

This module avoids the expensive symbolic Hessian builder.  At z=1 the exact
Y Cayley link is
    U = I + (4/7) Y + (2/7) Y^2,
so every local face derivative can be assembled directly over Q.

Exports:
    LABELS
    ATERMS : shift -> {(row,col): Fraction}, 96x96 connection block
    QTERMS : shift -> {(row,col): Fraction}, 40x96 metric-incidence block
    build_stencil()
"""
from __future__ import annotations
from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations

Z=F(0)
O=F(1)
PAIRS=list(combinations(range(4),2))
SYM=[(a,b) for a in range(4) for b in range(a,4)]
ETA_SIG=(1,-1,-1,-1)

def zero(r=4,c=4):
    return [[Z for _ in range(c)] for _ in range(r)]

def eye(n=4):
    A=zero(n,n)
    for i in range(n):
        A[i][i]=O
    return A

I4=eye()

def madd(A,B):
    return [[A[i][j]+B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def msub(A,B):
    return [[A[i][j]-B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def mscale(q,A):
    return [[q*x for x in row] for row in A]

def mm(A,B):
    nr,nk,nc=len(A),len(B),len(B[0])
    C=zero(nr,nc)
    for i in range(nr):
        for k in range(nk):
            a=A[i][k]
            if not a:
                continue
            for j in range(nc):
                b=B[k][j]
                if b:
                    C[i][j]+=a*b
    return C

def linv(A):
    return [[F(ETA_SIG[i]*ETA_SIG[j])*A[j][i] for j in range(4)] for i in range(4)]

def prod(items):
    A=I4
    for M in items:
        A=mm(A,M)
    return A

def basis(j):
    return [O if i==j else Z for i in range(4)]

def wedge(u,v):
    return [u[a]*v[b]-u[b]*v[a] for a,b in PAIRS]

def biv(M):
    return [M[a][b]*F(ETA_SIG[b]) for a,b in PAIRS]

def orient(a,b):
    seq=[a,b]+[j for j in range(4) if j not in (a,b)]
    inv=sum(seq[i]>seq[j] for i in range(4) for j in range(i+1,4))
    return -1 if inv%2 else 1

GEN=[]
for j in (1,2,3):
    X=zero()
    X[0][j]=X[j][0]=O
    GEN.append(X)
for a,b in ((1,2),(1,3),(2,3)):
    X=zero()
    X[a][b]=O
    X[b][a]=-O
    GEN.append(X)

Y=madd(msub(GEN[3],GEN[4]),GEN[5])
Y2=mm(Y,Y)
U=madd(I4,madd(mscale(F(4,7),Y),mscale(F(2,7),Y2)))
W=(U,I4,linv(U),I4)
BASIS=[basis(j) for j in range(4)]
G2DIAG=[F(ETA_SIG[a]*ETA_SIG[b]) for a,b in PAIRS]
STAR_MAP=((5,-1),(4,1),(3,-1),(2,1),(1,-1),(0,1))
LABELS=[(p,r,g) for p in range(4) for r in range(4) for g in range(6)]
IDX={x:i for i,x in enumerate(LABELS)}

def pair_star(area,db):
    out=Z
    for col,(row,sgn) in enumerate(STAR_MAP):
        out += area[row]*G2DIAG[row]*F(sgn)*db[col]
    return out

def metric_lift(a,b):
    q=zero()
    q[a][b]=q[b][a]=O
    return [[F(ETA_SIG[i],2)*q[i][j] for j in range(4)] for i in range(4)]

def addterm(D,key,val):
    if val:
        D[key]=D.get(key,Z)+val

@lru_cache(None)
def build_stencil():
    ATERMS=defaultdict(dict)
    QTERMS=defaultdict(dict)

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
                FF=linv(K) if inverse else K
                factors.append(FF)
                first.append([mscale(-1,mm(X,FF)) if inverse else mm(FF,X) for X in GEN])

            local=[]
            for pos,(q,role,_inverse) in enumerate(locs):
                for g in range(6):
                    local.append((pos,g,IDX[(q,role,g)]))

            u,v=[j for j in range(4) if j not in (a,b)]
            area=wedge(BASIS[u],BASIS[v])
            Hloc=[[Z]*24 for _ in range(24)]
            for ii,(pi,gi,_x) in enumerate(local):
                for jj in range(ii,24):
                    pj,gj,_y=local[jj]
                    if pi==pj:
                        Q=mscale(F(1,2),madd(mm(GEN[gi],GEN[gj]),mm(GEN[gj],GEN[gi])))
                        Q=mm(Q,factors[pi]) if locs[pi][2] else mm(factors[pi],Q)
                        items=[Q if n==pi else factors[n] for n in range(4)]
                    else:
                        items=[
                            first[n][gi] if n==pi
                            else first[n][gj] if n==pj
                            else factors[n]
                            for n in range(4)
                        ]
                    d2P=prod(items)
                    d2F=mscale(F(1,2),msub(d2P,linv(d2P)))
                    val=F(orient(a,b))*pair_star(area,biv(d2F))
                    Hloc[ii][jj]=Hloc[jj][ii]=val

            shifts=[
                (0,0,0,0),
                tuple(int(r==a) for r in range(4)),
                tuple(int(r==b) for r in range(4)),
                (0,0,0,0),
            ]
            slot=[]
            for sh in shifts:
                slot += [sh]*6
            for ii,(_pi,_gi,ggi) in enumerate(local):
                for jj,(_pj,_gj,ggj) in enumerate(local):
                    d=tuple(slot[jj][r]-slot[ii][r] for r in range(4))
                    addterm(ATERMS[d],(ggi,ggj),Hloc[ii][jj])

            darea=[]
            for qa,qb in SYM:
                dS=metric_lift(qa,qb)
                du=wedge([dS[i][u] for i in range(4)],BASIS[v])
                dv=wedge(BASIS[u],[dS[i][v] for i in range(4)])
                darea.append([x+y for x,y in zip(du,dv)])

            for pos,(q,role,inverse) in enumerate(locs):
                for g,X in enumerate(GEN):
                    dFfactor=mscale(-1,mm(X,factors[pos])) if inverse else mm(factors[pos],X)
                    dP=prod([dFfactor if n==pos else factors[n] for n in range(4)])
                    dF=mscale(F(1,2),msub(dP,linv(dP)))
                    db=biv(dF)
                    gidx=IDX[(q,role,g)]
                    for mi,ar in enumerate(darea):
                        addterm(
                            QTERMS[shifts[pos]],
                            (10*phase+mi,gidx),
                            F(orient(a,b))*pair_star(ar,db),
                        )

    ATERMS={d:{ij:v for ij,v in E.items() if v} for d,E in ATERMS.items()}
    QTERMS={d:{ij:v for ij,v in E.items() if v} for d,E in QTERMS.items()}
    ATERMS={d:E for d,E in ATERMS.items() if E}
    QTERMS={d:E for d,E in QTERMS.items() if E}
    return ATERMS,QTERMS

ATERMS,QTERMS=build_stencil()

if __name__=="__main__":
    assert len(ATERMS)==21
    assert len(QTERMS)==5
    assert sum(map(len,ATERMS.values()))==1944
    assert sum(map(len,QTERMS.values()))==1044
    print("TERMINAL A4D-Y-CURVED-JOINT-RATIONAL-LAURENT-STENCIL")
