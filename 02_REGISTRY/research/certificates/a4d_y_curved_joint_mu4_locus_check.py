#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=180
"""Certified mu_4^4 locus of the full curved z=1 joint Bloch symbol.

The literal 96 connection rows and 40 phase-resolved metric rows are compiled
once into a 21-term Laurent stencil.  Full column rank at the 252 regular
quarter-wave characters is certified modulo a good Gaussian prime; a nonzero
96-minor modulo p is a nonzero characteristic-zero minor after denominator
clearing.  The four remaining diagonal characters are checked exactly over
Q(i): rank 95, nullity one.  Phase unfolding identifies all four kernels with
the same constant Y center.

Scope: exact mu_4^4 only, not an all-(S^1)^4 theorem.
"""
from __future__ import annotations
from collections import defaultdict
from itertools import product
import json
from pathlib import Path
import numpy as np
import sympy as sp
import a4d_y_curved_response_quotient_check as B
import a4d_y_curved_normaljet_compatibility_check as C

HERE=Path(__file__).resolve().parent
OUT=HERE/"a4d_y_curved_joint_mu4_locus_results.json"
ROOTS=(sp.Integer(1),sp.I,sp.Integer(-1),-sp.I)
P=1_000_033

def ck(n,c):
    if not c: raise AssertionError(n)
    print("PASS_"+n,flush=True)

def sqrt_minus_one(p):
    for g in range(2,200):
        x=pow(g,(p-1)//4,p)
        if x*x%p==p-1: return x
    raise AssertionError("no sqrt(-1) found")
IM=sqrt_minus_one(P)
ROOTS_MOD=(1,IM,P-1,(-IM)%P)

_H,LABELS,FACES0=B.action_connection_hessian(sp.Integer(1))
FACES=C.with_base_phases(FACES0)
IDX={x:i for i,x in enumerate(LABELS)}
UNIT=[B.I4[:,j] for j in range(4)]
T=defaultdict(lambda:sp.zeros(136,96))

for phase,a,b,locs,local,Hloc,factors in FACES:
    shifts=[(0,0,0,0),tuple(int(r==a) for r in range(4)),
            tuple(int(r==b) for r in range(4)),(0,0,0,0)]
    slot=[]
    for s in shifts: slot += [s]*6
    for ii,(_pi,_gi,gi) in enumerate(local):
        for jj,(_pj,_gj,gj) in enumerate(local):
            d=tuple(slot[jj][r]-slot[ii][r] for r in range(4))
            T[d][gi,gj]+=Hloc[ii,jj]
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
                T[shifts[pos]][96+10*phase+mi,gi]+=val

SUPPORT=sorted(d for d,M in T.items() if M!=sp.zeros(136,96))
expected={(0,0,0,0)}
for r in range(4):
    e=[0]*4;e[r]=1;expected.add(tuple(e));e[r]=-1;expected.add(tuple(e))
for r in range(4):
    for s in range(4):
        if r!=s:
            d=[0]*4;d[r]=1;d[s]=-1;expected.add(tuple(d))
ck("LAURENT_SUPPORT_21",len(SUPPORT)==21 and set(SUPPORT)==expected)

def ratmod(q):
    q=sp.Rational(q); den=int(q.q)%P
    if den==0: raise AssertionError("bad modular denominator")
    return (int(q.p)%P)*pow(den,P-2,P)%P

TMOD={}
for d in SUPPORT:
    A=np.zeros((136,96),dtype=np.int64)
    for (i,j),v in T[d].todok().items():
        A[i,j]=ratmod(v)
    TMOD[d]=A

def mon_mod(ids,d):
    out=1
    for r,e in enumerate(d):
        if e==1: out=out*ROOTS_MOD[ids[r]]%P
        elif e==-1: out=out*pow(ROOTS_MOD[ids[r]],P-2,P)%P
    return out

def eval_mod(ids):
    A=np.zeros((136,96),dtype=np.int64)
    for d in SUPPORT:
        A=(A+mon_mod(ids,d)*TMOD[d])%P
    return A

def rank_mod(A):
    A=A.copy(); row=0
    for col in range(A.shape[1]):
        nz=np.flatnonzero(A[row:,col])
        if nz.size==0: continue
        piv=row+int(nz[0])
        if piv!=row: A[[row,piv]]=A[[piv,row]]
        inv=pow(int(A[row,col]),P-2,P)
        A[row,:]=(A[row,:]*inv)%P
        inds=np.flatnonzero(A[row+1:,col])+row+1
        if inds.size:
            q=A[inds,col].copy()
            A[inds,:]=(A[inds,:]-q[:,None]*A[row,:])%P
        row+=1
        if row==A.shape[1]: break
    return row

def mon_exact(lam,d):
    out=sp.Integer(1)
    for r,e in enumerate(d):
        if e: out*=lam[r]**e
    return out

def eval_exact(ids):
    lam=tuple(ROOTS[i] for i in ids)
    return sum((mon_exact(lam,d)*T[d] for d in SUPPORT),sp.zeros(136,96))

candidates=[]; regular=0
for ids in product(range(4),repeat=4):
    r=rank_mod(eval_mod(ids))
    if r==96: regular+=1
    else: candidates.append((ids,r))
expected_candidates=[((j,j,j,j),95) for j in range(4)]
ck("MODULAR_CANDIDATES_ONLY_FOLDED",candidates==expected_candidates)
ck("MODULAR_FULL_RANK_COUNT_252",regular==252)

unfolded=[]
folded_records=[]
for j in range(4):
    ids=(j,j,j,j); M=eval_exact(ids); dm=M.to_DM(extension=True)
    rank=dm.rank(); N=dm.nullspace().to_Matrix()
    ck("FOLDED_EXACT_RANK95_"+str(j),rank==95)
    ck("FOLDED_EXACT_NULLITY1_"+str(j),N.shape==(1,96))
    v=sp.Matrix(N[0,:]).T
    first=next(x for x in v if x!=0); v=(v/first).applyfunc(sp.simplify)
    lam=ROOTS[j]
    vu=sp.Matrix([sp.simplify(lam**(-LABELS[k][0])*v[k]) for k in range(96)])
    unfolded.append(vu)
    folded_records.append({
      "root_index":j,"lambda":str(lam),"rank":rank,"nullity":1,
      "nonzero_kernel_entries":{
        ":".join(map(str,LABELS[k])):str(v[k]) for k in range(96) if v[k]!=0
      }
    })
ck("ALL_FOLDED_UNFOLD_TO_SAME_CENTER",
   all(v==unfolded[0] for v in unfolded[1:]))
nz=[(LABELS[k],unfolded[0][k]) for k in range(96) if unfolded[0][k]!=0]
ck("UNFOLDED_CENTER_IS_Y",
   nz==[((0,0,3),1),((0,0,4),-1),((0,0,5),1),
        ((2,0,3),-1),((2,0,4),1),((2,0,5),-1)])

result={
 "schema":"a4d-y-curved-joint-mu4-locus-v1",
 "terminal":"A4D-Y-CURVED-JOINT-MU4-LOCUS-CERTIFIED",
 "background":"z=1 exact Y vacuum; standard solder",
 "z":"1","operator_shape":[136,96],"laurent_support_size":21,
 "modulus":P,"sqrt_minus_one_mod_p":IM,
 "mu4_character_count":256,"full_rank_character_count":252,
 "modular_rank_counts":{"95":4,"96":252},
 "singular_characters":folded_records,
 "unfolded_physical_kernel":"constant Y center",
 "characteristic_zero_argument":{
   "regular_points":"rank mod p = 96 gives a nonzero characteristic-zero 96-minor after denominator clearing",
   "folded_points":"direct DomainMatrix rank over Q(i) is 95 with exact one-dimensional nullspace",
   "unfolding":"multiplying phase-p connection amplitudes by lambda^(-p) identifies all four kernels with the same constant Y center"
 },
 "conclusion":"on mu_4^4 the only joint rank drops are the four diagonal folded copies of the same physical constant Y center",
 "scope_fence":[
   "exact mu_4^4 torsion grid only",
   "no all-Bloch complex or unit-torus zero-locus theorem",
   "no uniform singular-value lower bound between sampled characters",
   "no nonlinear range theorem or task-level response terminal"
 ]
}
if "--write" in __import__("sys").argv:
    OUT.write_text(json.dumps(result,indent=2)+"\n")
    print("WROTE",OUT)
elif OUT.exists():
    ck("RESULTS_MATCH_PINNED_JSON",json.loads(OUT.read_text())==result)
print("TERMINAL A4D-Y-CURVED-JOINT-MU4-LOCUS-CERTIFIED")
