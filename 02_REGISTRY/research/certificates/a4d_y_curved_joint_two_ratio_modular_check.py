#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=300
"""Exact three-prime modular elimination on one two-ratio interior stratum.

Zone-fold the curved z=1 full joint Bloch symbol and retain the 68 interior
rows (all connection+metric rows in fast phases 1 and 2).  On the representative
two-ratio plane

    rho0=1, rho1=x, rho2=y, rho3=1,

select four fixed 68-column charts.  For each chart, multiply every matrix
entry by 14*x*y.  Its entries then have bidegree at most (2,2).

For three independent good primes, the certificate:
* derives exact determinant degree windows by an integer Hungarian assignment;
* reconstructs each bivariate determinant exactly over F_p by root-of-unity
  evaluation/DFT inside those windows;
* forms two pair-resultants in y by exact Sylvester determinants and exact
  finite-difference interpolation in x;
* proves
      gcd(R_01,R_23) = x^229 (x-1)^11;
* at x=1, proves the gcd of all four chart determinants in y is
      (y-1)^3.

Therefore on (Fbar_p^*)^2 the common zero-set of these four minors is exactly
(x,y)=(1,1), for each pinned prime.

This is a modular elimination terminal only.  It does NOT by itself lift the
two-ratio rank theorem to characteristic zero and does not prove the full
three-ratio/all-Bloch locus.
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
OUT=HERE/"a4d_y_curved_joint_two_ratio_modular_results.json"
DEN=14
PRIMES=(664448401,996672601,1328896801)

CHARTS=(
(41,61,26,24,37,46,65,63,64,33,36,85,40,71,68,25,44,39,88,30,87,73,43,89,54,69,28,29,27,70,13,49,45,47,95,50,90,84,35,34,12,32,76,81,92,17,20,16,74,51,60,52,0,62,38,94,2,31,72,1,6,42,22,14,67,77,9,15),
(54,25,33,58,30,26,59,70,78,24,46,55,69,71,82,83,34,35,72,79,57,29,44,73,68,28,48,51,91,32,43,50,92,94,41,47,67,81,77,45,27,37,6,93,39,20,53,74,40,9,36,75,1,95,2,56,42,17,49,13,11,16,52,38,80,18,90,8),
(61,24,41,26,58,37,33,54,46,65,30,25,63,68,36,59,35,64,40,44,57,43,34,32,29,73,92,72,47,27,45,39,70,60,28,49,95,50,94,85,69,93,20,71,62,48,13,76,38,22,31,9,74,55,52,17,6,2,51,42,0,78,1,4,75,90,89,19),
(68,71,50,69,64,92,93,24,66,95,74,65,63,88,85,46,25,52,72,26,61,76,41,90,60,75,73,70,49,51,44,89,84,29,94,47,48,87,45,53,77,27,33,40,43,28,39,67,36,35,37,32,34,0,62,30,1,20,2,91,22,15,38,17,86,9,13,6),
)
CHART_HASHES=(
"d6c54b08aa8de87a8d59969acaf3b5f14f0aed8f5cda66d614c47f3b1bbe6586",
"14e26dbe1157b2ed917452970fc1ddfdc671b2c9bf86bf0dce20cd87cdd5050f",
"7a76061c6ee79d1112a005d8aa8b73af9151e2787fda7d219ad096cf02d7b078",
"89f83d51b6f121b435d122d23f6077e06bcec893524532ff6a148551c2d970b2",
)
EXPECTED_SHAPES=((41,35),(39,39),(44,41),(38,37))
EXPECTED_RESULTANT_DEGREES=(2576,2742)

def ck(name,cond):
    if not cond:
        raise AssertionError(name)
    print("PASS_"+name,flush=True)

for i,c in enumerate(CHARTS):
    ck("CHART_SIZE_"+str(i),len(c)==68 and len(set(c))==68)
    h=hashlib.sha256(",".join(map(str,c)).encode()).hexdigest()
    ck("CHART_HASH_"+str(i),h==CHART_HASHES[i])

# O(n^3) Hungarian algorithm for exact integer assignment costs.
def assignment_cost(cost):
    n=len(cost); m=len(cost[0])
    assert n==m
    INF=10**12
    u=[0]*(n+1); v=[0]*(m+1); p=[0]*(m+1); way=[0]*(m+1)
    for i in range(1,n+1):
        p[0]=i
        j0=0
        minv=[INF]*(m+1)
        used=[False]*(m+1)
        while True:
            used[j0]=True
            i0=p[j0]
            delta=INF
            j1=0
            for j in range(1,m+1):
                if used[j]:
                    continue
                cur=cost[i0-1][j-1]-u[i0]-v[j]
                if cur<minv[j]:
                    minv[j]=cur
                    way[j]=j0
                if minv[j]<delta:
                    delta=minv[j]
                    j1=j
            if delta>=INF:
                raise AssertionError("NO_PERFECT_MATCHING")
            for j in range(m+1):
                if used[j]:
                    u[p[j]]+=delta
                    v[j]-=delta
                else:
                    minv[j]-=delta
            j0=j1
            if p[j0]==0:
                break
        while True:
            j1=way[j0]
            p[j0]=p[j1]
            j0=j1
            if j0==0:
                break
    return -v[0]

def chart_terms(cols):
    cpos={c:j for j,c in enumerate(cols)}
    terms=[[{} for _ in range(68)] for __ in range(68)]

    for d,E in S.ATERMS.items():
        a,b=d[1]+1,d[2]+1
        ck("A_EXPONENT_RANGE_"+str(d),0<=a<=2 and 0<=b<=2)
        for (row,col),v0 in E.items():
            if not (24<=row<72) or col not in cpos:
                continue
            q=F(v0)*DEN
            ck("A_DENOMINATOR_CLEAR",q.denominator==1)
            rr=row-24
            cc=cpos[col]
            terms[rr][cc][(a,b)]=terms[rr][cc].get((a,b),0)+q.numerator

    for d,E in S.QTERMS.items():
        a,b=d[1]+1,d[2]+1
        ck("Q_EXPONENT_RANGE_"+str(d),0<=a<=2 and 0<=b<=2)
        for (row,col),v0 in E.items():
            if not (10<=row<30) or col not in cpos:
                continue
            q=F(v0)*DEN
            ck("Q_DENOMINATOR_CLEAR",q.denominator==1)
            rr=48+(row-10)
            cc=cpos[col]
            terms[rr][cc][(a,b)]=terms[rr][cc].get((a,b),0)+q.numerator

    for i in range(68):
        for j in range(68):
            terms[i][j]={ab:v for ab,v in terms[i][j].items() if v}

    bounds=[]
    BIG=10**6
    for axis in (0,1):
        lo=[[BIG]*68 for _ in range(68)]
        hi=[[BIG]*68 for _ in range(68)]
        for i in range(68):
            for j in range(68):
                if terms[i][j]:
                    ex=[ab[axis] for ab in terms[i][j]]
                    lo[i][j]=min(ex)
                    hi[i][j]=-max(ex)
        mn=assignment_cost(lo)
        mx=-assignment_cost(hi)
        bounds.append((mn,mx))
    return terms,tuple(bounds)

EXPECTED_ASSIGNMENT_BOUNDS=(
((45,99),(41,87)),
((41,90),(49,102)),
((43,98),(43,96)),
((50,104),(43,93)),
)

CHART_TERM_DATA=[]
for i,c in enumerate(CHARTS):
    terms,bounds=chart_terms(c)
    ck("ASSIGNMENT_BOUNDS_"+str(i),bounds==EXPECTED_ASSIGNMENT_BOUNDS[i])
    CHART_TERM_DATA.append((terms,bounds))

def detmod(A,p):
    A=np.remainder(A,p).astype(np.int64,copy=True)
    n=A.shape[0]
    det=1
    for c in range(n):
        nz=np.flatnonzero(A[c:,c])
        if not len(nz):
            return 0
        r=c+int(nz[0])
        if r!=c:
            A[[c,r]]=A[[r,c]]
            det=(-det)%p
        pv=int(A[c,c])
        det=det*pv%p
        inv=pow(pv,-1,p)
        ids=np.arange(c+1,n)
        ids=ids[A[ids,c]!=0]
        if len(ids):
            fac=(A[ids,c].copy()*inv)%p
            A[ids,c:]=(A[ids,c:]-fac[:,None]*A[c,c:])%p
    return int(det%p)

def primitive_root_of_order(p,n):
    ck("ORDER_DIVIDES_"+str(p)+"_"+str(n),(p-1)%n==0)
    g=int(sp.primitive_root(p))
    w=pow(g,(p-1)//n,p)
    ck("ROOT_ORDER_"+str(p)+"_"+str(n),pow(w,n,p)==1)
    for q in sp.factorint(n):
        ck("ROOT_PRIMITIVE_"+str(p)+"_"+str(n)+"_"+str(q),
           pow(w,n//q,p)!=1)
    return w

def reconstruct_chart_mod(terms,bounds,p):
    xmin,xmax=bounds[0]
    ymin,ymax=bounds[1]
    nx=xmax-xmin+1
    ny=ymax-ymin+1
    wx=primitive_root_of_order(p,nx)
    wy=primitive_root_of_order(p,ny)
    xs=[pow(wx,k,p) for k in range(nx)]
    ys=[pow(wy,k,p) for k in range(ny)]

    C=[[np.zeros((68,68),dtype=np.int64) for _ in range(3)] for __ in range(3)]
    for i in range(68):
        for j in range(68):
            for (a,b),v in terms[i][j].items():
                C[a][b][i,j]=v%p

    vals=np.zeros((nx,ny),dtype=np.int64)
    for ix,x in enumerate(xs):
        xp=(1,x,x*x%p)
        ay=[]
        for b in range(3):
            M=np.zeros((68,68),dtype=np.int64)
            for a in range(3):
                M=(M+xp[a]*C[a][b])%p
            ay.append(M)
        for iy,y in enumerate(ys):
            vals[ix,iy]=detmod((ay[0]+y*ay[1]+(y*y%p)*ay[2])%p,p)

    # Remove the certified Laurent-unit lower powers before inverse DFT.
    for ix,x in enumerate(xs):
        xx=pow(x,-xmin,p)
        for iy,y in enumerate(ys):
            vals[ix,iy]=vals[ix,iy]*xx%p*pow(y,-ymin,p)%p

    invx=pow(nx,-1,p)
    invy=pow(ny,-1,p)
    ty=np.zeros((nx,ny),dtype=np.int64)
    for ix in range(nx):
        for b in range(ny):
            wb=pow(wy,(-b)%ny,p)
            cur=1
            total=0
            for iy in range(ny):
                total=(total+int(vals[ix,iy])*cur)%p
                cur=cur*wb%p
            ty[ix,b]=total*invy%p

    coeff=np.zeros((nx,ny),dtype=np.int64)
    for a in range(nx):
        wa=pow(wx,(-a)%nx,p)
        powers=[pow(wa,ix,p) for ix in range(nx)]
        for b in range(ny):
            total=sum(int(ty[ix,b])*powers[ix] for ix in range(nx))%p
            coeff[a,b]=total*invx%p

    nz=np.argwhere(coeff!=0)
    ck("NONZERO_CHART_POLYNOMIAL",len(nz)>0)
    amin,amax=int(nz[:,0].min()),int(nz[:,0].max())
    bmin,bmax=int(nz[:,1].min()),int(nz[:,1].max())
    trimmed=np.zeros((amax-amin+1,bmax-bmin+1),dtype=np.int64)
    for a,b in nz:
        trimmed[int(a)-amin,int(b)-bmin]=coeff[int(a),int(b)]
    return trimmed,(amin,amax,bmin,bmax,len(nz))

def eval_ycoeff(C,x,p):
    out=np.zeros(C.shape[1],dtype=np.int64)
    for b in range(C.shape[1]):
        v=0
        for a in range(C.shape[0]-1,-1,-1):
            v=(v*x+int(C[a,b]))%p
        out[b]=v
    while len(out)>1 and out[-1]==0:
        out=out[:-1]
    return out

def resultant_at(A,B,x,p):
    a=eval_ycoeff(A,x,p)
    b=eval_ycoeff(B,x,p)
    m=len(a)-1
    n=len(b)-1
    Sly=np.zeros((m+n,m+n),dtype=np.int64)
    ad=a[::-1]
    bd=b[::-1]
    for r in range(n):
        Sly[r,r:r+m+1]=ad
    for r in range(m):
        Sly[n+r,r:r+n+1]=bd
    return detmod(Sly,p)

def interpolate_forward(values,p):
    cur=[int(v)%p for v in values]
    differences=[]
    for _ in range(len(values)):
        differences.append(cur[0])
        cur=[(cur[i+1]-cur[i])%p for i in range(len(cur)-1)]
    coeff=[0]*len(values)
    basis=[1]
    for j,cj in enumerate(differences):
        if cj:
            for k,b in enumerate(basis):
                coeff[k]=(coeff[k]+cj*b)%p
        if j+1<len(values):
            inv=pow(j+1,p-2,p)
            nxt=[0]*(len(basis)+1)
            for k,b in enumerate(basis):
                nxt[k]=(nxt[k]-j*b*inv)%p
                nxt[k+1]=(nxt[k+1]+b*inv)%p
            basis=nxt
    while len(coeff)>1 and coeff[-1]==0:
        coeff.pop()
    return np.array(coeff,dtype=np.int64)

def resultant_poly(A,B,p):
    degree_bound=(A.shape[1]-1)*(B.shape[0]-1)+(B.shape[1]-1)*(A.shape[0]-1)
    values=[resultant_at(A,B,x,p) for x in range(degree_bound+1)]
    coeff=interpolate_forward(values,p)
    for xv in (degree_bound+1,degree_bound+7,degree_bound+19):
        vv=0
        for c in coeff[::-1]:
            vv=(vv*xv+int(c))%p
        ck("RESULTANT_OUT_OF_SAMPLE_"+str(p)+"_"+str(xv),
           vv==resultant_at(A,B,xv,p))
    return coeff,degree_bound

def trim_poly(a,p):
    i=len(a)-1
    while i>0 and int(a[i])%p==0:
        i-=1
    return np.array(a[:i+1],dtype=np.int64)%p

def divrem_poly(a,b,p):
    a=trim_poly(a,p).copy()
    b=trim_poly(b,p)
    db=len(b)-1
    invb=pow(int(b[-1]),p-2,p)
    while len(a)-1>=db and not (len(a)==1 and int(a[0])==0):
        k=len(a)-1-db
        q=int(a[-1])*invb%p
        if q:
            a[k:k+db+1]=(a[k:k+db+1]-q*b)%p
        a=trim_poly(a,p)
    return a

def gcd_poly(a,b,p):
    a=trim_poly(a,p)
    b=trim_poly(b,p)
    while not (len(b)==1 and int(b[0])==0):
        a,b=b,divrem_poly(a,b,p)
    return trim_poly(a*pow(int(a[-1]),p-2,p)%p,p)

from math import comb

records=[]
for p in PRIMES:
    ck("GOOD_PRIME_"+str(p),sp.isprime(p) and p<2_000_000_000)
    polys=[]
    supports=[]
    for i,(terms,bounds) in enumerate(CHART_TERM_DATA):
        P,supp=reconstruct_chart_mod(terms,bounds,p)
        ck("CHART_SHAPE_"+str(p)+"_"+str(i),P.shape==EXPECTED_SHAPES[i])
        polys.append(P)
        supports.append(list(supp))

    r01,b01=resultant_poly(polys[0],polys[1],p)
    r23,b23=resultant_poly(polys[2],polys[3],p)
    ck("RESULTANT_BOUND_01_"+str(p),b01==2812)
    ck("RESULTANT_BOUND_23_"+str(p),b23==3028)
    ck("RESULTANT_DEGREE_01_"+str(p),len(r01)-1==EXPECTED_RESULTANT_DEGREES[0])
    ck("RESULTANT_DEGREE_23_"+str(p),len(r23)-1==EXPECTED_RESULTANT_DEGREES[1])

    g=gcd_poly(r01,r23,p)
    expected=np.zeros(241,dtype=np.int64)
    for k in range(12):
        expected[229+k]=comb(11,k)*((-1)**(11-k))%p
    ck("RESULTANT_GCD_"+str(p),np.array_equal(g,expected))

    gy=None
    for P in polys:
        cy=np.array([
            sum(int(P[a,b]) for a in range(P.shape[0]))%p
            for b in range(P.shape[1])
        ],dtype=np.int64)
        gy=cy if gy is None else gcd_poly(gy,cy,p)
    expected_y=np.array([p-1,3,p-3,1],dtype=np.int64)
    ck("X1_Y_GCD_"+str(p),np.array_equal(gy,expected_y))

    records.append({
      "prime":p,
      "chart_supports":supports,
      "resultant_degrees":[len(r01)-1,len(r23)-1],
      "resultant_gcd":"x^229*(x-1)^11",
      "x_equals_one_y_gcd":"(y-1)^3",
      "torus_zero_set":"(x,y)=(1,1)",
    })

result={
 "schema":"a4d-y-curved-joint-two-ratio-modular-v1",
 "terminal":"A4D-Y-CURVED-JOINT-TWO-RATIO-THREE-PRIME-MODULAR-ELIMINATION-CERTIFIED",
 "background":"z=1 exact Y vacuum; zone-folded 68-row interior joint operator",
 "ratio_plane":"rho0=1, rho1=x, rho2=y, rho3=1",
 "integer_clear":"multiply each selected entry by 14*x*y",
 "chart_column_hashes":list(CHART_HASHES),
 "assignment_bounds":[[[a,b] for a,b in q] for q in EXPECTED_ASSIGNMENT_BOUNDS],
 "trimmed_chart_shapes":[list(q) for q in EXPECTED_SHAPES],
 "primes":list(PRIMES),
 "records":records,
 "modular_conclusion":"for each pinned prime, on (Fbar_p^*)^2 the four selected 68-minors have common zero-set exactly (1,1)",
 "next_gate":"characteristic-zero lift of the two-ratio elimination, then the genuinely three-ratio interior locus",
 "scope_fence":[
   "exact finite-field elimination at three independent good primes",
   "does not by itself prove the characteristic-zero two-ratio theorem",
   "does not prove the full three-ratio or all-Bloch unit-torus locus",
   "no nonlinear continuation or task-level response terminal"
 ]
}
if "--write" in __import__("sys").argv:
    OUT.write_text(json.dumps(result,indent=2)+"\n")
    print("WROTE",OUT)
elif OUT.exists():
    ck("RESULTS_MATCH_PINNED_JSON",json.loads(OUT.read_text())==result)
print("TERMINAL A4D-Y-CURVED-JOINT-TWO-RATIO-THREE-PRIME-MODULAR-ELIMINATION-CERTIFIED")
