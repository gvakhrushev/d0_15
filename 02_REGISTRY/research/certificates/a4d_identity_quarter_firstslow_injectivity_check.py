#!/usr/bin/env python3
"""Exact first-slow injectivity of the full identity-quarter joint center.

At the flat identity connection and diagonal quarter character (i,i,i,i),
the literal stacked joint symbol J=(A;C) has complex nullity four, one
role-supported physical line per role. This checker eliminates an exact
20-column range chart and computes the first angular derivative of the
reduced 4-center symbol. It certifies that the reduced symbol has complex
column rank four for every nonzero real slow covector.

This is a frozen flat first-slow theorem. It is not a varying-coframe
nonlinear continuation or a full-Bloch H_TORUS theorem.
"""
from __future__ import annotations
from itertools import combinations
import hashlib, json, sys
from pathlib import Path
import sympy as sp

HERE=Path(__file__).resolve().parent
OUT=HERE/"a4d_identity_quarter_firstslow_injectivity_results.json"
I=sp.I
SIG=(1,-1,-1,-1)
PAIRS=list(combinations(range(4),2))
SYM=[(a,b) for a in range(4) for b in range(a,4)]
STAR_MAP=((5,-1),(4,1),(3,-1),(2,1),(1,-1),(0,1))

def ck(name,cond):
    if not cond: raise AssertionError(name)
    print("PASS_"+name, flush=True)

def wedge(u,v): return [u[a]*v[b]-u[b]*v[a] for a,b in PAIRS]
def orient(a,b):
    s=[a,b]+[j for j in range(4) if j not in (a,b)]
    return -1 if sum(s[i]>s[j] for i,j in combinations(range(4),2))%2 else 1

def gens():
    out=[]
    for j in (1,2,3):
        X=sp.zeros(4); X[0,j]=X[j,0]=1; out.append(X)
    for a,b in ((1,2),(1,3),(2,3)):
        X=sp.zeros(4); X[a,b]=1; X[b,a]=-1; out.append(X)
    return out
GEN=gens(); EYE=sp.eye(4)

def pairing(area,tangent):
    biv=[tangent[a,b]*SIG[b] for a,b in PAIRS]
    return sp.expand(sum(area[row]*SIG[PAIRS[row][0]]*SIG[PAIRS[row][1]]*sgn*biv[c]
                         for c,(row,sgn) in enumerate(STAR_MAP)))

def flat_symbols(phase):
    phase=[sp.sympify(z) for z in phase]
    A=sp.zeros(24,24); C=sp.zeros(10,24)
    for r,s in PAIRS:
        u,v=[j for j in range(4) if j not in (r,s)]
        area=wedge(EYE[:,u],EYE[:,v])
        roles=(r,s,r,s)
        direct=(1,phase[r],-phase[s],-1)
        inverse=(1,1/phase[r],-1/phase[s],-1)
        role=sp.zeros(4,4)
        for ii,jj in combinations(range(4),2):
            role[roles[ii],roles[jj]] += sp.Rational(1,2)*direct[ii]*inverse[jj]
            role[roles[jj],roles[ii]] -= sp.Rational(1,2)*inverse[ii]*direct[jj]
        for i,Xi in enumerate(GEN):
            for j,Xj in enumerate(GEN):
                val=orient(r,s)*pairing(area,Xi*Xj-Xj*Xi)
                if val:
                    for rr in range(4):
                        for ss in range(4):
                            if role[rr,ss]:
                                A[6*rr+i,6*ss+j]+=role[rr,ss]*val
        for mi,(aa,bb) in enumerate(SYM):
            lift=sp.zeros(4)
            lift[aa,bb]=sp.Rational(SIG[aa],2)
            lift[bb,aa]=sp.Rational(SIG[bb],2)
            da=[x+y for x,y in zip(wedge(lift[:,u],EYE[:,v]),
                                    wedge(EYE[:,u],lift[:,v]))]
            for j,Xj in enumerate(GEN):
                val=orient(r,s)*pairing(da,Xj)
                if val:
                    for p in range(4):
                        C[mi,6*roles[p]+j]+=direct[p]*val
    return A.applyfunc(sp.cancel), C.applyfunc(sp.cancel)

def joint(phase):
    A,C=flat_symbols(phase)
    return A.col_join(C)

quarter=[I]*4
J0=joint(quarter)
ck("QUARTER_JOINT_RANK20", J0.rank()==20)

role_vectors=(
    (0,0,0,1,-1,1),
    (0,1,-1,0,0,1),
    (1,0,-1,0,1,0),
    (1,-1,0,1,0,0),
)
N=sp.zeros(24,4)
for r,v in enumerate(role_vectors):
    for g,x in enumerate(v):
        N[6*r+g,r]=x
ck("FOUR_ROLE_CENTER_IN_JOINT_KERNEL",
   J0*N==sp.zeros(34,4) and N.rank()==4)

COMP=[0,1,2,3,4,6,7,8,9,10,12,13,14,15,17,18,19,20,22,23]
PIV=[0,1,3,4,6,7,8,9,12,13,14,15,18,19,20,22,24,25,26,28]
REST=[r for r in range(34) if r not in PIV]
R=J0.extract(PIV,COMP)
ck("EXACT_RANGE_CHART_DETERMINANT4", sp.factor(R.det())==4)
Rinv=R.inv()

# Every entry is Laurent degree <=1 in each phase coordinate. At z=i,
# d/dtheta f(i exp(i theta))|_0 = -(f(z_k=1)-f(z_k=-1))/2.
Ds=[]
for axis in range(4):
    plus=[I]*4; minus=[I]*4
    plus[axis]=1; minus[axis]=-1
    Ds.append(-(joint(plus)-joint(minus))/2)

Gammas=[]
for axis,D in enumerate(Ds):
    source=D*N
    coeff=-Rinv*source.extract(PIV,range(4))
    W=sp.zeros(24,4)
    for i,c in enumerate(COMP):
        W[c,:]=coeff[i,:]
    Gamma=(source+J0*W).applyfunc(sp.expand)
    ck("RANGE_ROWS_ELIMINATED_"+str(axis),
       Gamma.extract(PIV,range(4))==sp.zeros(20,4))
    Gammas.append(Gamma.extract(REST,range(4)))

k0,k1,k2,k3=sp.symbols("k0 k1 k2 k3", real=True)
ks=(k0,k1,k2,k3)
G=sum((ks[j]*Gammas[j] for j in range(4)),sp.zeros(14,4)).applyfunc(sp.expand)

ck("FIRST_COLUMN_ROW_01",
   sp.expand(G[3,0]-((-1+I)*k0+(-1-I)*k1))==0)
ck("FIRST_COLUMN_ROW_02",
   sp.expand(G[4,0]-((1-I)*k0+(1+I)*k2))==0)
ck("FIRST_COLUMN_ROW_03",
   sp.expand(G[6,0]-((-1+I)*k0+(-1-I)*k3))==0)

M=G[8:14,1:4].copy()
M[0,:]=(sp.Rational(2,1)/(1+I))*M[0,:]
for r in range(1,6):
    M[r,:]=2*M[r,:]
M=M.applyfunc(sp.expand)
expected=sp.Matrix([
 [k2-k3, k1-k3, k1-k2],
 [-(1+I)*k0-2*k1+k2-I*k3, -k0+k1, -I*k0+I*k1],
 [(1+I)*k0+2*k1-k2+I*k3, -I*k0-k1+(1+I)*k3,
  -k0-I*k1+(1+I)*k2],
 [I*(k3-k0), I*(k0-k3), -I*(k1+k2)-2*k3],
 [-k2+k3, k0-k1+2*k2+2*I*k3, k0-k1+2*I*k2+2*k3],
 [I*(k0-k2), -I*(k1+k3)-2*k2, I*(k0-k2)],
])
ck("REDUCED_SIX_BY_THREE_MATRIX",
   all(sp.simplify(x)==0 for x in (M-expected)))

polys=[]
for rows in combinations(range(6),3):
    d=sp.expand(M.extract(rows,range(3)).det())
    for q in (sp.re(d),sp.im(d)):
        q=sp.Poly(sp.expand(q),*ks,domain=sp.QQ)
        if not q.is_zero:
            _,prim=q.primitive()
            e=prim.as_expr()
            if e not in polys and -e not in polys:
                polys.append(e)
ck("FORTY_REAL_MINOR_EQUATIONS", len(polys)==40)
GB=sp.groebner(polys,*ks,order="grevlex",method="f5b")
consequences=(
 (k2-k3)*(k2**2+k2*k3+k3**2),
 k3*(k0**2+k1**2+2*k1*k3),
 k3*(k0*k1-k1*k2-k1*k3+k3**2),
 k0**3+2*k1**2*k3+3*k1*k2*k3-2*k3**3,
 -k0*k3**2+k1**3+2*k1**2*k3+3*k1*k2*k3+k1*k3**2-2*k3**3,
)
for j,q in enumerate(consequences):
    ck("GROEBNER_CONSEQUENCE_"+str(j),
       sp.expand(GB.reduce(q)[1])==0)

a,b=sp.symbols("a b", real=True)
A=a*a+b*b+2*b
B=a*b-2*b+1
P=sp.factor(sp.resultant(A,B,a))
expectedP=b**4+2*b**3+4*b**2-4*b+1
ck("NONZERO_T_RESULTANT", sp.expand(P-expectedP)==0)
sos=(b**2+b-sp.Rational(1,2))**2+4*(b-sp.Rational(3,8))**2+sp.Rational(3,16)
ck("RESULTANT_STRICT_SOS", sp.expand(P-sos)==0)

def matrix_text(A):
    return ";".join(",".join(str(sp.expand(A[i,j]))
                              for j in range(A.cols))
                    for i in range(A.rows))
gamma_hash=hashlib.sha256("|".join(matrix_text(x)
                                    for x in Gammas).encode()).hexdigest()

result={
 "schema":"a4d-identity-quarter-firstslow-injectivity-v1",
 "terminal":"A4D-IDENTITY-QUARTER-FULL-CENTER-FIRSTSLOW-INJECTIVE",
 "background":"flat identity connection and solder",
 "quarter_character":["i","i","i","i"],
 "joint_shape":[34,24],
 "joint_rank":20,
 "center_complex_dimension":4,
 "range_columns":COMP,
 "range_rows":PIV,
 "range_chart_determinant":"4",
 "reduced_shape":[14,4],
 "gamma_sha256":gamma_hash,
 "rank_statement":"rank_C sum_j k_j Gamma_j = 4 for every real k != 0",
 "quantitative_consequence":"by homogeneity and compactness, sigma_min >= c |k| for some c>0 on real slow covectors",
 "groebner_real_minor_count":len(polys),
 "resultant":str(P),
 "resultant_sos":"(b^2+b-1/2)^2 + 4(b-3/8)^2 + 3/16",
 "scope_fence":[
   "frozen flat identity-quarter first-slow symbol only",
   "does not prove a varying-coframe nonlinear branch",
   "does not prove H_TORUS or an all-Bloch range inverse",
   "does not by itself give the h^-2 metric-response limit"
 ]
}
if "--write" in sys.argv:
    OUT.write_text(json.dumps(result,indent=2)+"\n")
    print("WROTE",OUT)
elif OUT.exists():
    ck("RESULTS_MATCH_PINNED_JSON", json.loads(OUT.read_text())==result)
print("TERMINAL",result["terminal"])
