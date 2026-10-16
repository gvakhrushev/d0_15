#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=240
"""Exact one-ratio transverse joint-rank theorem at the curved z=1 Y vacuum.

For each spatial axis s=1,2,3 consider
    lambda_0=1, lambda_s=x, all other lambda=1.
Two explicit 96x96 minors of the literal 136x96 joint Bloch symbol are used:
  D0: all 96 connection rows;
  D1: replace connection row 50 by metric row 100.

After multiplying every selected row by 14*x, both determinants are integer
polynomials of structural degree <=192. They are reconstructed exactly by
CRT from 21 pinned ~1e9 primes. A coefficient l1/Hadamard bound is computed
from the integer polynomial matrix and the CRT modulus is required to exceed
twice that bound, making centered reconstruction unique.

For all three spatial axes the primitive gcd is exactly x^64*(x-1)^2.
Hence for x in C^* with x!=1 the full joint symbol has column rank 96. At
x=1 the owned folded result gives rank 95 with the physical Y kernel.

This is three one-ratio slices, not the full four-variable all-Bloch theorem.
"""
from __future__ import annotations
from collections import defaultdict
import json
import math
from pathlib import Path
import numpy as np
import sympy as sp
import a4d_y_curved_response_quotient_check as B
import a4d_y_curved_normaljet_compatibility_check as C

HERE=Path(__file__).resolve().parent
OUT=HERE/"a4d_y_curved_joint_one_ratio_slices_results.json"
MU4=HERE/"a4d_y_curved_joint_mu4_locus_results.json"
PRIMES=[
  999999937,999998929,999997891,999996827,999995819,999994813,999993811,
  999992783,999991669,999990631,999989567,999988547,999987503,999986501,
  999985471,999984463,999983459,999982457,999981449,999980419,999979417
]
NDEG=192

def ck(name,cond):
    if not cond: raise AssertionError(name)
    print("PASS_"+name,flush=True)

H,LABELS,FACES0=B.action_connection_hessian(sp.Integer(1))
FACES=C.with_base_phases(FACES0)
IDX={x:i for i,x in enumerate(LABELS)}
UNIT=[B.I4[:,j] for j in range(4)]
T=defaultdict(lambda:sp.zeros(136,96))

for phase,a,b,locs,local,Hloc,factors in FACES:
    shifts=[(0,0,0,0),tuple(int(r==a) for r in range(4)),
            tuple(int(r==b) for r in range(4)),(0,0,0,0)]
    slot=[]
    for shift in shifts: slot += [shift]*6
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
                value=sp.cancel(B.orientation(a,b)*(area.T*B.G2*B.STAR*dFb)[0])
                T[shifts[pos]][96+10*phase+mi,gi]+=value

rows0=list(range(96))
rows1=[r for r in range(96) if r!=50]+[100]
x=sp.symbols("x")

def integer_coeff_matrices(axis,rows):
    mats=[sp.zeros(96) for _ in range(3)]
    for d,M in T.items():
        mats[d[axis]+1]+=M.extract(rows,range(96))
    # Literal entries have denominators dividing 14. Multiplication by x
    # clears the Laurent exponent and 14 clears all rational denominators.
    out=[]
    for M in mats:
        A=14*M
        ck("INTEGER_COEFFICIENT_MATRIX_AXIS"+str(axis),
           all(sp.Rational(v).q==1 for v in A))
        out.append(np.array(A.tolist(),dtype=np.int64))
    return out

def determinant_mod(A,p):
    A=np.remainder(A,p).astype(np.int64,copy=True)
    det=1
    n=A.shape[0]
    for col in range(n):
        nz=np.flatnonzero(A[col:,col])
        if nz.size==0: return 0
        pivot=col+int(nz[0])
        if pivot!=col:
            A[[col,pivot]]=A[[pivot,col]]
            det=(-det)%p
        pv=int(A[col,col])
        det=det*pv%p
        inv=pow(pv,p-2,p)
        if col+1<n:
            row=np.remainder(A[col,col+1:]*inv,p)
            inds=np.flatnonzero(A[col+1:,col])+col+1
            if inds.size:
                q=A[inds,col].copy()
                A[inds,col+1:]=np.remainder(
                    A[inds,col+1:]-q[:,None]*row[None,:],p
                )
                A[inds,col]=0
    return int(det)

def interpolate_forward(values,p):
    cur=[int(v)%p for v in values]
    differences=[]
    for _ in range(len(values)):
        differences.append(cur[0])
        cur=[(cur[i+1]-cur[i])%p for i in range(len(cur)-1)]
    coeff=[0]*len(values)
    basis=[1]  # binomial(x,0)
    for j,cj in enumerate(differences):
        for k,b in enumerate(basis):
            coeff[k]=(coeff[k]+cj*b)%p
        if j+1<len(values):
            inv=pow(j+1,p-2,p)
            nxt=[0]*(len(basis)+1)
            for k,b in enumerate(basis):
                nxt[k]=(nxt[k]-j*b*inv)%p
                nxt[k+1]=(nxt[k+1]+b*inv)%p
            basis=nxt
    return coeff

def polynomial_mod(mats,p):
    reduced=[np.remainder(M,p).astype(np.int64) for M in mats]
    values=[]
    for xv in range(NDEG+1):
        M=np.remainder(
            reduced[0]+xv*reduced[1]+((xv*xv)%p)*reduced[2],p
        )
        values.append(determinant_mod(M,p))
    return interpolate_forward(values,p)

def coefficient_bound(mats):
    # The l1 norm of all determinant coefficients is at most the product,
    # over rows, of the row l1 norms in the polynomial coefficient matrix.
    row_bounds=[]
    for i in range(96):
        total=0
        for M in mats:
            total+=sum(abs(int(v)) for v in M[i,:])
        row_bounds.append(total)
    return math.prod(row_bounds)

def reconstruct_pair(mats0,mats1):
    bound=max(coefficient_bound(mats0),coefficient_bound(mats1))
    r0=[0]*(NDEG+1)
    r1=[0]*(NDEG+1)
    modulus=1
    for prime in PRIMES:
        c0=polynomial_mod(mats0,prime)
        c1=polynomial_mod(mats1,prime)
        inv=pow(modulus%prime,prime-2,prime)
        for i in range(NDEG+1):
            r0[i]+=(((c0[i]-r0[i])%prime)*inv%prime)*modulus
            r1[i]+=(((c1[i]-r1[i])%prime)*inv%prime)*modulus
        modulus*=prime
    ck("CRT_MODULUS_EXCEEDS_TWICE_BOUND",modulus>2*bound)
    def centered(values):
        out=[v if v<=modulus//2 else v-modulus for v in values]
        while len(out)>1 and out[-1]==0: out.pop()
        return out
    return centered(r0),centered(r1),modulus,bound

records=[]
for axis in (1,2,3):
    mats0=integer_coeff_matrices(axis,rows0)
    mats1=integer_coeff_matrices(axis,rows1)
    c0,c1,modulus,bound=reconstruct_pair(mats0,mats1)
    D0=sp.Poly(sum(sp.Integer(c)*x**i for i,c in enumerate(c0)),x,domain=sp.ZZ)
    D1=sp.Poly(sum(sp.Integer(c)*x**i for i,c in enumerate(c1)),x,domain=sp.ZZ)
    ck("DEGREE_WITHIN_STRUCTURAL_BOUND_AXIS"+str(axis),
       D0.degree()<=NDEG and D1.degree()<=NDEG)
    primitive=sp.gcd(D0,D1).primitive()[1].monic()
    expected=sp.Poly(x**64*(x-1)**2,x,domain=sp.QQ)
    ck("PRIMITIVE_GCD_AXIS"+str(axis),primitive==expected)
    records.append({
      "spatial_axis":axis,
      "minor0_degree":D0.degree(),
      "minor1_degree":D1.degree(),
      "primitive_gcd":"x^64*(x-1)^2",
      "coefficient_bound_digits":len(str(bound)),
      "crt_modulus_digits":len(str(modulus)),
      "prime_count":len(PRIMES)
    })

mu4=json.loads(MU4.read_text())
ck("X_EQUALS_ONE_IS_OWNED_FOLDED_Y_POINT",
   mu4["singular_characters"][0]["rank"]==95
   and mu4["unfolded_physical_kernel"]=="constant Y center")

result={
 "schema":"a4d-y-curved-joint-one-ratio-slices-v1",
 "terminal":"A4D-Y-CURVED-JOINT-ONE-RATIO-SLICES-CERTIFIED",
 "z":"1",
 "slices":[
   "(1,x,1,1)","(1,1,x,1)","(1,1,1,x)"
 ],
 "minor_rows":{
   "D0":"connection rows 0..95",
   "D1":"connection rows except 50, plus metric row 100"
 },
 "integer_clear":"multiply every selected row by 14*x",
 "structural_degree_bound":NDEG,
 "crt_primes":PRIMES,
 "records":records,
 "rank_conclusion":"on every listed slice and every x in C^* with x!=1, at least one certified 96-minor is nonzero, hence rank Q=96",
 "x_equals_one":"rank 95 with the physical Y center by the folded owner",
 "scope_fence":[
   "three coordinate one-ratio complex slices are exact",
   "simultaneous variation of two or three ratios remains open",
   "this does not by itself prove the full unit-torus zero locus",
   "no nonlinear continuation or task-level response terminal is claimed"
 ]
}
if "--write" in __import__("sys").argv:
    OUT.write_text(json.dumps(result,indent=2)+"\n")
    print("WROTE",OUT)
elif OUT.exists():
    ck("RESULTS_MATCH_PINNED_JSON",json.loads(OUT.read_text())==result)
print("TERMINAL A4D-Y-CURVED-JOINT-ONE-RATIO-SLICES-CERTIFIED")
