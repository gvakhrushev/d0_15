#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=1800
"""Exact Z[x,y] reconstruction of the four two-ratio interior minors.

This lifts the four modular chart determinants used by
a4d_y_curved_joint_two_ratio_modular_check.py to characteristic zero.

On rho0=1, rho1=x, rho2=y, rho3=1, select the same four 68-column charts
of the 68-row phase-1/phase-2 interior joint operator.  Multiply every entry
by 14*x*y.  All matrix entries are then integer polynomials of bidegree <=(2,2).

For each chart:
* derive exact determinant exponent windows by integer assignment;
* bound the determinant coefficient l1 norm by the product of row l1 norms;
* reconstruct every coefficient by root-of-unity DFT modulo enough good primes
  that the CRT modulus exceeds twice the coefficient bound;
* center the CRT lift, trim exact zero borders, and verify the pinned support;
* replay the exact integer polynomial at an independent good prime.

No floating arithmetic enters.  This certificate owns the exact four
characteristic-zero minors, but does not itself prove their common zero-set.
"""
from __future__ import annotations
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path

import numpy as np
import sympy as sp
import a4d_y_curved_joint_rational_stencil as S

HERE=Path(__file__).resolve().parent
OUT=HERE/"a4d_y_curved_joint_two_ratio_integer_minors_results.json"
DEN=14

CHARTS=(
(41,61,26,24,37,46,65,63,64,33,36,85,40,71,68,25,44,39,88,30,87,73,43,89,54,69,28,29,27,70,13,49,45,47,95,50,90,84,35,34,12,32,76,81,92,17,20,16,74,51,60,52,0,62,38,94,2,31,72,1,6,42,22,14,67,77,9,15),
(54,25,33,58,30,26,59,70,78,24,46,55,69,71,82,83,34,35,72,79,57,29,44,73,68,28,48,51,91,32,43,50,92,94,41,47,67,81,77,45,27,37,6,93,39,20,53,74,40,9,36,75,1,95,2,56,42,17,49,13,11,16,52,38,80,18,90,8),
(61,24,41,26,58,37,33,54,46,65,30,25,63,68,36,59,35,64,40,44,57,43,34,32,29,73,92,72,47,27,45,39,70,60,28,49,95,50,94,85,69,93,20,71,62,48,13,76,38,22,31,9,74,55,52,17,6,2,51,42,0,78,1,4,75,90,89,19),
(68,71,50,69,64,92,93,24,66,95,74,65,63,88,85,46,25,52,72,26,61,76,41,90,60,75,73,70,49,51,44,89,84,29,94,47,48,87,45,53,77,27,33,40,43,28,39,67,36,35,37,32,34,0,62,30,1,20,2,91,22,15,38,17,86,9,13,6),
)
EXPECTED_ASSIGNMENT_BOUNDS=(
((45,99),(41,87)),
((41,90),(49,102)),
((43,98),(43,96)),
((50,104),(43,93)),
)
EXPECTED_TRIMMED_SUPPORTS=(
(9,49,6,40,1184),
(6,44,9,47,1271),
(6,49,7,47,1448),
(12,49,6,42,1174),
)

def ck(name,cond):
    if not cond: raise AssertionError(name)
    print("PASS_"+name,flush=True)

def assignment_cost(cost):
    n=len(cost); assert n==len(cost[0])
    INF=10**12
    u=[0]*(n+1); v=[0]*(n+1); p=[0]*(n+1); way=[0]*(n+1)
    for i in range(1,n+1):
        p[0]=i; j0=0
        minv=[INF]*(n+1); used=[False]*(n+1)
        while True:
            used[j0]=True; i0=p[j0]; delta=INF; j1=0
            for j in range(1,n+1):
                if used[j]: continue
                cur=cost[i0-1][j-1]-u[i0]-v[j]
                if cur<minv[j]:
                    minv[j]=cur; way[j]=j0
                if minv[j]<delta:
                    delta=minv[j]; j1=j
            if delta>=INF: raise AssertionError("NO_PERFECT_MATCHING")
            for j in range(n+1):
                if used[j]: u[p[j]]+=delta; v[j]-=delta
                else: minv[j]-=delta
            j0=j1
            if p[j0]==0: break
        while True:
            j1=way[j0]; p[j0]=p[j1]; j0=j1
            if j0==0: break
    return -v[0]

def chart_terms(cols):
    cpos={c:j for j,c in enumerate(cols)}
    terms=[[{} for _ in range(68)] for __ in range(68)]
    for data,rowoff in ((S.ATERMS,0),(S.QTERMS,48)):
        for d,E in data.items():
            a,b=d[1]+1,d[2]+1
            if not (0<=a<=2 and 0<=b<=2): raise AssertionError(("ENTRY_EXPONENT_RANGE",d))
            for (row,col),v0 in E.items():
                if data is S.ATERMS:
                    if not (24<=row<72): continue
                    rr=row-24
                else:
                    if not (10<=row<30): continue
                    rr=48+(row-10)
                if col not in cpos: continue
                q=F(v0)*DEN
                if q.denominator!=1: raise AssertionError(("DENOMINATOR_CLEAR",d,row,col))
                cc=cpos[col]
                terms[rr][cc][(a,b)]=terms[rr][cc].get((a,b),0)+q.numerator
    for i in range(68):
        for j in range(68):
            terms[i][j]={ab:v for ab,v in terms[i][j].items() if v}

    BIG=10**6; bounds=[]
    for axis in (0,1):
        lo=[[BIG]*68 for _ in range(68)]
        hi=[[BIG]*68 for _ in range(68)]
        for i in range(68):
            for j in range(68):
                if terms[i][j]:
                    es=[ab[axis] for ab in terms[i][j]]
                    lo[i][j]=min(es); hi[i][j]=-max(es)
        bounds.append((assignment_cost(lo),-assignment_cost(hi)))

    # Determinant coefficient l1 norm <= product over rows of the row l1
    # norm in the polynomial-entry coefficient ring.
    row_bounds=[]
    for i in range(68):
        total=0
        for j in range(68):
            total+=sum(abs(v) for v in terms[i][j].values())
        if total<=0: raise AssertionError(("ZERO_ROW_L1",i))
        row_bounds.append(total)
    coeff_bound=math.prod(row_bounds)
    return terms,tuple(bounds),coeff_bound

def detmod(A,p):
    A=np.remainder(A,p).astype(np.int64,copy=True)
    det=1; n=A.shape[0]
    for c in range(n):
        nz=np.flatnonzero(A[c:,c])
        if not len(nz): return 0
        r=c+int(nz[0])
        if r!=c:
            A[[c,r]]=A[[r,c]]; det=(-det)%p
        pv=int(A[c,c]); det=det*pv%p; inv=pow(pv,p-2,p)
        ids=np.arange(c+1,n); ids=ids[A[ids,c]!=0]
        if len(ids):
            fac=(A[ids,c].copy()*inv)%p
            A[ids,c:]=(A[ids,c:]-fac[:,None]*A[c,c:])%p
    return int(det%p)

def prime_1mod(start,n):
    q=start+((1-start)%n)
    while not sp.isprime(q): q+=n
    return int(q)

def primitive_root_of_order(p,n):
    g=int(sp.primitive_root(p)); w=pow(g,(p-1)//n,p)
    ck("ROOT_ORDER_"+str(p)+"_"+str(n),pow(w,n,p)==1)
    for q in sp.factorint(n):
        ck("ROOT_PRIMITIVE_"+str(p)+"_"+str(n)+"_"+str(q),pow(w,n//q,p)!=1)
    return w

def coeff_mod(terms,bounds,p):
    xmin,xmax=bounds[0]; ymin,ymax=bounds[1]
    nx=xmax-xmin+1; ny=ymax-ymin+1
    wx=primitive_root_of_order(p,nx); wy=primitive_root_of_order(p,ny)
    xs=[pow(wx,k,p) for k in range(nx)]
    ys=[pow(wy,k,p) for k in range(ny)]
    C=[[np.zeros((68,68),dtype=np.int64) for _ in range(3)] for __ in range(3)]
    for i in range(68):
        for j in range(68):
            for (a,b),v in terms[i][j].items(): C[a][b][i,j]=v%p
    vals=np.zeros((nx,ny),dtype=np.int64)
    for ix,x in enumerate(xs):
        xp=(1,x,x*x%p); ay=[]
        for b in range(3):
            M=np.zeros((68,68),dtype=np.int64)
            for a in range(3): M=(M+xp[a]*C[a][b])%p
            ay.append(M)
        for iy,y in enumerate(ys):
            vals[ix,iy]=detmod((ay[0]+y*ay[1]+(y*y%p)*ay[2])%p,p)
    # Shift assignment minima to exponent 0 before inverse DFT.
    for ix,x in enumerate(xs):
        sx=pow(x,-xmin,p)
        for iy,y in enumerate(ys):
            vals[ix,iy]=vals[ix,iy]*sx%p*pow(y,-ymin,p)%p
    invx=pow(nx,-1,p); invy=pow(ny,-1,p)
    ty=np.zeros((nx,ny),dtype=np.int64)
    for ix in range(nx):
        for b in range(ny):
            wb=pow(wy,(-b)%ny,p); cur=1; total=0
            for iy in range(ny):
                total=(total+int(vals[ix,iy])*cur)%p; cur=cur*wb%p
            ty[ix,b]=total*invy%p
    out=np.zeros((nx,ny),dtype=np.int64)
    for a in range(nx):
        wa=pow(wx,(-a)%nx,p)
        powers=[pow(wa,ix,p) for ix in range(nx)]
        for b in range(ny):
            out[a,b]=sum(int(ty[ix,b])*powers[ix] for ix in range(nx))%p*invx%p
    return out

records=[]
fiber_x1=[]
fiber_y1=[]
exact_arrays=[]
for ci,cols in enumerate(CHARTS):
    terms,bounds,bound=chart_terms(cols)
    ck("ASSIGNMENT_BOUNDS_"+str(ci),bounds==EXPECTED_ASSIGNMENT_BOUNDS[ci])
    xmin,xmax=bounds[0]; ymin,ymax=bounds[1]
    nx=xmax-xmin+1; ny=ymax-ymin+1
    order=math.lcm(nx,ny)

    residues=np.zeros((nx,ny),dtype=object)
    residues[:,:]=0
    modulus=1; primes=[]; start=500_000_000
    while modulus<=2*bound:
        p=prime_1mod(start,order); start=p+order
        ck("GOOD_PRIME_"+str(ci)+"_"+str(p),p<2_000_000_000)
        C=coeff_mod(terms,bounds,p)
        inv=pow(modulus%p,p-2,p)
        for a in range(nx):
            for b in range(ny):
                old=int(residues[a,b])
                residues[a,b]=old+(((int(C[a,b])-old)%p)*inv%p)*modulus
        modulus*=p; primes.append(p)
    ck("CRT_MODULUS_EXCEEDS_TWICE_BOUND_"+str(ci),modulus>2*bound)

    exact=np.empty((nx,ny),dtype=object)
    for a in range(nx):
        for b in range(ny):
            z=int(residues[a,b])
            exact[a,b]=z if z<=modulus//2 else z-modulus
    ck("ALL_COEFFICIENTS_WITHIN_BOUND_"+str(ci),
       all(abs(int(exact[a,b]))<=bound for a in range(nx) for b in range(ny)))

    nz=[(a,b,int(exact[a,b])) for a in range(nx) for b in range(ny) if exact[a,b]]
    exact_arrays.append(exact.copy())
    amin=min(a for a,b,c in nz); amax=max(a for a,b,c in nz)
    bmin=min(b for a,b,c in nz); bmax=max(b for a,b,c in nz)
    supp=(amin,amax,bmin,bmax,len(nz))
    ck("TRIMMED_SUPPORT_"+str(ci),supp==EXPECTED_TRIMMED_SUPPORTS[ci])

    # Independent prime replay, outside the CRT prime set.
    vp=prime_1mod(start+10_000_000,order)
    ck("VERIFY_PRIME_DISTINCT_"+str(ci),vp not in primes)
    Cv=coeff_mod(terms,bounds,vp)
    ok=True
    for a in range(nx):
        for b in range(ny):
            if int(exact[a,b])%vp!=int(Cv[a,b])%vp:
                ok=False; break
        if not ok: break
    ck("INDEPENDENT_PRIME_REPLAY_"+str(ci),ok)

    # Store only the exact nonzero coefficient ledger shifted back to the
    # original cleared determinant exponents.  This is the reusable Z[x,y]
    # artifact for characteristic-zero elimination.
    ledger=[[a+xmin,b+ymin,c] for a,b,c in nz]
    payload=";".join(f"{a},{b},{c}" for a,b,c in ledger)
    h=hashlib.sha256(payload.encode()).hexdigest()
    # Exact coordinate-fiber specializations. Assignment-minimum monomials
    # are units on the torus; strip any remaining coordinate monomial before gcd.
    yy=sp.symbols("yy")
    cy=[sum(int(exact[a,b]) for a in range(nx)) for b in range(ny)]
    while len(cy)>1 and cy[0]==0: cy=cy[1:]
    Py=sp.Poly(sum(sp.Integer(c)*yy**k for k,c in enumerate(cy)),yy,domain=sp.ZZ)
    fiber_x1.append(Py.primitive()[1])
    xx=sp.symbols("xx")
    cx=[sum(int(exact[a,b]) for b in range(ny)) for a in range(nx)]
    while len(cx)>1 and cx[0]==0: cx=cx[1:]
    Px=sp.Poly(sum(sp.Integer(c)*xx**k for k,c in enumerate(cx)),xx,domain=sp.ZZ)
    fiber_y1.append(Px.primitive()[1])

    records.append({
      "chart_index":ci,
      "assignment_bounds":[list(bounds[0]),list(bounds[1])],
      "coefficient_bound_digits":len(str(bound)),
      "crt_prime_count":len(primes),
      "crt_primes":primes,
      "crt_modulus_digits":len(str(modulus)),
      "verification_prime":vp,
      "exact_support":[amin+xmin,amax+xmin,bmin+ymin,bmax+ymin,len(nz)],
      "coefficient_ledger_sha256":h,
    })

gx=fiber_x1[0]
for P in fiber_x1[1:]: gx=sp.gcd(gx,P)
gx=sp.Poly(gx.monic(),yy,domain=sp.QQ)
ck("EXACT_X1_COMMON_GCD_Y_MINUS_1_CUBED",
   gx==sp.Poly((yy-1)**3,yy,domain=sp.QQ))

gy=fiber_y1[0]
for P in fiber_y1[1:]: gy=sp.gcd(gy,P)
gy=sp.Poly(gy.monic(),xx,domain=sp.QQ)
print("EXACT_Y1_COMMON_GCD",sp.factor(gy.as_expr()),flush=True)

# Characteristic-zero elimination without reconstructing the huge integer
# resultants.  Exact determinant supports give structural x-degree windows for
# each Sylvester determinant.  One good modular prime certifies that both edge
# coefficients attain those windows, hence the resultant degrees are preserved
# under specialization.  Exact Sylvester nullity at x=1 supplies the matching
# characteristic-zero (x-1)^e divisibility lower bound.

def trim_exact(E):
    nz=[(a,b) for a in range(E.shape[0]) for b in range(E.shape[1]) if E[a,b]]
    a0=min(a for a,b in nz); a1=max(a for a,b in nz)
    b0=min(b for a,b in nz); b1=max(b for a,b in nz)
    A=np.empty((a1-a0+1,b1-b0+1),dtype=object)
    for a in range(a0,a1+1):
        for b in range(b0,b1+1):
            A[a-a0,b-b0]=int(E[a,b])
    return A,(a0,a1,b0,b1)

TRIMMED=[trim_exact(E)[0] for E in exact_arrays]

def coeff_x_support(A,ydeg):
    ex=[a for a in range(A.shape[0]) if A[a,ydeg]]
    return None if not ex else (min(ex),max(ex))

def sylvester_x_bounds(A,B):
    m=A.shape[1]-1; n=B.shape[1]-1; N=m+n; BIG=10**9
    lo=[[BIG]*N for _ in range(N)]
    hi=[[BIG]*N for _ in range(N)]
    ac=[coeff_x_support(A,b) for b in range(m,-1,-1)]
    bc=[coeff_x_support(B,b) for b in range(n,-1,-1)]
    for r in range(n):
        for j,sup in enumerate(ac):
            if sup is not None:
                lo[r][r+j]=sup[0]; hi[r][r+j]=-sup[1]
    for r in range(m):
        rr=n+r
        for j,sup in enumerate(bc):
            if sup is not None:
                lo[rr][r+j]=sup[0]; hi[rr][r+j]=-sup[1]
    return assignment_cost(lo),-assignment_cost(hi)

def detmod_square(A,p):
    A=np.remainder(A,p).astype(np.int64,copy=True); n=A.shape[0]; det=1
    for c in range(n):
        nz=np.flatnonzero(A[c:,c])
        if not len(nz): return 0
        r=c+int(nz[0])
        if r!=c:
            A[[c,r]]=A[[r,c]]; det=(-det)%p
        pv=int(A[c,c]); det=det*pv%p; inv=pow(pv,p-2,p)
        ids=np.arange(c+1,n); ids=ids[A[ids,c]!=0]
        if len(ids):
            fac=(A[ids,c].copy()*inv)%p
            A[ids,c:]=(A[ids,c:]-fac[:,None]*A[c,c:])%p
    return int(det%p)

def eval_ycoeff(A,x,p):
    out=np.zeros(A.shape[1],dtype=np.int64)
    for b in range(A.shape[1]):
        v=0
        for a in range(A.shape[0]-1,-1,-1):
            v=(v*x+int(A[a,b]))%p
        out[b]=v
    return out

def resultant_at(A,B,x,p):
    a=eval_ycoeff(A,x,p); b=eval_ycoeff(B,x,p)
    m=A.shape[1]-1; n=B.shape[1]-1
    M=np.zeros((m+n,m+n),dtype=np.int64)
    ad=a[::-1]; bd=b[::-1]
    for r in range(n): M[r,r:r+m+1]=ad
    for r in range(m): M[n+r,r:r+n+1]=bd
    return detmod_square(M,p)

def interpolate_forward(values,p):
    cur=[int(v)%p for v in values]; dif=[]
    for _ in range(len(values)):
        dif.append(cur[0]); cur=[(cur[i+1]-cur[i])%p for i in range(len(cur)-1)]
    coeff=[0]*len(values); basis=[1]
    for j,cj in enumerate(dif):
        if cj:
            for k,b in enumerate(basis): coeff[k]=(coeff[k]+cj*b)%p
        if j+1<len(values):
            inv=pow(j+1,p-2,p); nxt=[0]*(len(basis)+1)
            for k,b in enumerate(basis):
                nxt[k]=(nxt[k]-j*b*inv)%p
                nxt[k+1]=(nxt[k+1]+b*inv)%p
            basis=nxt
    while len(coeff)>1 and coeff[-1]==0: coeff.pop()
    return np.array(coeff,dtype=np.int64)

def resultant_mod(A,B,p,hi):
    vals=[resultant_at(A,B,x,p) for x in range(hi+1)]
    return interpolate_forward(vals,p)

def val0(a,p):
    k=0
    while k<len(a) and int(a[k])%p==0: k+=1
    return k

def trim_poly(a,p):
    a=np.array(a,dtype=np.int64)%p
    while len(a)>1 and int(a[-1])==0: a=a[:-1]
    return a

def divrem_poly(a,b,p):
    a=trim_poly(a,p).copy(); b=trim_poly(b,p)
    db=len(b)-1; inv=pow(int(b[-1]),p-2,p)
    while len(a)-1>=db and not(len(a)==1 and int(a[0])==0):
        k=len(a)-1-db; q=int(a[-1])*inv%p
        if q: a[k:k+db+1]=(a[k:k+db+1]-q*b)%p
        a=trim_poly(a,p)
    return a

def gcd_poly(a,b,p):
    a=trim_poly(a,p); b=trim_poly(b,p)
    while not(len(b)==1 and int(b[0])==0):
        a,b=b,divrem_poly(a,b,p)
    a=trim_poly(a,p)
    return a*pow(int(a[-1]),p-2,p)%p

def divide_x_minus_one(a,p):
    a=trim_poly(a,p)
    if sum(int(x) for x in a)%p: return None
    n=len(a)-1
    if n==0: return None
    q=np.zeros(n,dtype=np.int64)
    q[n-1]=a[n]%p
    for k in range(n-1,0,-1):
        q[k-1]=(int(a[k])+int(q[k]))%p
    ck("SYNTHETIC_DIVISION_REMAINDER",(-int(q[0])-int(a[0]))%p==0)
    return trim_poly(q,p)

def pure_one_factor(a,p):
    q=trim_poly(a,p); e=0
    while True:
        qq=divide_x_minus_one(q,p)
        if qq is None: break
        q=qq; e+=1
    return e,(len(q)==1 and int(q[0])%p!=0)

def sylvester_nullity_x1(A,B):
    aa=[sum(int(A[x,b]) for x in range(A.shape[0])) for b in range(A.shape[1])]
    bb=[sum(int(B[x,b]) for x in range(B.shape[0])) for b in range(B.shape[1])]
    m=len(aa)-1; n=len(bb)-1
    M=sp.zeros(m+n,m+n)
    ad=list(reversed(aa)); bd=list(reversed(bb))
    for r in range(n):
        for j,v in enumerate(ad): M[r,r+j]=v
    for r in range(m):
        for j,v in enumerate(bd): M[n+r,r+j]=v
    return m+n-M.to_DM().convert_to(sp.QQ).rank()

ELIM_PRIME=664448401
PAIR_LIST=[(i,j) for i in range(4) for j in range(i+1,4)]
pair_records=[]
mod_resultants=[]
for i,j in PAIR_LIST:
    A=TRIMMED[i]; B=TRIMMED[j]
    lo,hi=sylvester_x_bounds(A,B)
    R=resultant_mod(A,B,ELIM_PRIME,hi)
    vlo=val0(R,ELIM_PRIME); vhi=len(R)-1
    edges=(vlo==lo and vhi==hi and int(R[vlo])%ELIM_PRIME!=0 and int(R[vhi])%ELIM_PRIME!=0)
    print("RESULTANT_EDGE_PRESERVATION_"+str(i)+"_"+str(j),edges,flush=True)
    nul=sylvester_nullity_x1(A,B)
    pair_records.append({
      "pair":[i,j],"structural_x_bounds":[lo,hi],
      "modular_x_support":[vlo,vhi],
      "degree_preserved":bool(edges),
      "exact_sylvester_nullity_at_x1":nul,
    })
    mod_resultants.append(R[vlo:])

selection=None
for a in range(len(PAIR_LIST)):
    for b in range(a+1,len(PAIR_LIST)):
        if not (pair_records[a]["degree_preserved"] and pair_records[b]["degree_preserved"]):
            continue
        g=gcd_poly(mod_resultants[a],mod_resultants[b],ELIM_PRIME)
        e,pure=pure_one_factor(g,ELIM_PRIME)
        if pure and e>0:
            na=pair_records[a]["exact_sylvester_nullity_at_x1"]
            nb=pair_records[b]["exact_sylvester_nullity_at_x1"]
            if min(na,nb)>=e:
                selection=(a,b,e,g)
                break
    if selection is not None: break
ck("CHARZERO_ELIMINATION_PAIR_FOUND",selection is not None)
ia,ib,eg,_g=selection
ck("POSITIVE_COMMON_MULTIPLICITY",eg>0)

# Degree preservation at ELIM_PRIME gives
# deg gcd_Q <= deg gcd_Fp = eg.  Exact Sylvester nullities give
# (x-1)^eg dividing both characteristic-zero resultants, so equality holds.
# Therefore their characteristic-zero gcd on C^* is exactly (x-1)^eg.
selected_pairs=[PAIR_LIST[ia],PAIR_LIST[ib]]
selected_nullities=[
 pair_records[ia]["exact_sylvester_nullity_at_x1"],
 pair_records[ib]["exact_sylvester_nullity_at_x1"],
]
charzero_conclusion=(
 "the selected exact pair-resultants have characteristic-zero gcd, after "
 "removing Laurent x-units, equal to (x-1)^%d; hence any common torus zero "
 "of all four minors has x=1, and the exact x=1 fiber gcd (y-1)^3 then "
 "forces y=1" % eg
)

result={
 "schema":"a4d-y-curved-joint-two-ratio-integer-minors-v2",

 "terminal":"A4D-Y-CURVED-JOINT-TWO-RATIO-CHARZERO-LOCUS-CERTIFIED",
 "background":"z=1 exact Y vacuum; 68-row zone-folded interior operator",
 "ratio_plane":"rho0=1, rho1=x, rho2=y, rho3=1",
 "integer_clear":"multiply every selected matrix entry by 14*x*y",
 "charts":[list(c) for c in CHARTS],
 "records":records,
 "exact_coordinate_fibers":{
   "x_equals_1_common_gcd":str(sp.factor(gx.as_expr())),
   "y_equals_1_common_gcd":str(sp.factor(gy.as_expr()))
 },
 "characteristic_zero_elimination":{
   "prime":ELIM_PRIME,
   "pair_records":pair_records,
   "selected_resultant_pairs":[list(selected_pairs[0]),list(selected_pairs[1])],
   "selected_exact_nullities":selected_nullities,
   "normalized_modular_gcd":"(x-1)^"+str(eg),
   "conclusion":charzero_conclusion
 },
 "rank_conclusion":"on the representative complex two-ratio torus plane, the four certified 68-minors have common zero-set exactly (x,y)=(1,1); hence the 68-row interior operator has full row rank away from the diagonal ratio on this plane",
 "scope_fence":[
   "owns four exact characteristic-zero determinant polynomials in Z[x,y]",
   "characteristic-zero common zero-set is certified on the representative two-ratio plane",
   "does not prove the genuinely three-ratio or all-Bloch locus",
   "no nonlinear response terminal"
 ]
}
if "--write" in __import__("sys").argv:
    OUT.write_text(json.dumps(result,indent=2)+"\n")
    print("WROTE",OUT)
elif OUT.exists():
    ck("RESULTS_MATCH_PINNED_JSON",json.loads(OUT.read_text())==result)
print("RESULT_RECORDS",json.dumps(records,sort_keys=True),flush=True)
print("CHARZERO_SELECTION",json.dumps(result["characteristic_zero_elimination"],sort_keys=True),flush=True)
print("TERMINAL A4D-Y-CURVED-JOINT-TWO-RATIO-CHARZERO-LOCUS-CERTIFIED")
