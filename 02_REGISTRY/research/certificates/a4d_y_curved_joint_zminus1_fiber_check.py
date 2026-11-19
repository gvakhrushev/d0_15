#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=1800
"""Exact characteristic-zero interior-rank theorem on rho=(1,x,y,-1).

Reconstruct the four 68-column chart minors of the literal 68-row interior
joint symbol at the fixed unit-circle ratio z=-1. Multiply entries by 14*x*y,
then recover each integer bivariate determinant by coefficientwise root-of-
unity DFT and CRT beyond twice a row-norm coefficient bound. An independent
prime replays every coefficient. Finally, two fixed-degree Sylvester
resultants and a primitive-gcd reduction prove the four minors have no common
zero on (C*)^2, so the interior has row rank 68 throughout this fiber.

This is one exact fiber of the interior operator. It is not an all-Bloch
rank theorem for the full 136-by-96 joint symbol and does not close the
normalized-response task.
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

try:
    from flint import fmpz_mpoly_ctx, nmod_mat, nmod_mpoly_ctx
except ImportError:
    fmpz_mpoly_ctx = None
    nmod_mat = None
    nmod_mpoly_ctx = None

HERE=Path(__file__).resolve().parent
OUT=HERE/"a4d_y_curved_joint_zminus1_fiber_results.json"
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
(8,49,6,41,1229),
(6,44,9,47,1276),
(6,49,7,47,1436),
(12,49,6,42,1158),
)
EXPECTED_BIDEGREES=((41,35),(38,38),(43,40),(37,36))
PRIME=500000003
STENCIL_SHA256="d4cf844b027f8cc34540c385b48922f3a5bcfc42cbedf08d5a704cfb7adb0daa"

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

def chart_terms(cols, z0=-1):
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
                q=F(v0)*DEN*F(z0)**d[3]
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
    # Optional exact C backend; the NumPy path remains the dependency-free
    # fallback beyond this owner's existing NumPy/SymPy requirements.
    if nmod_mat is not None:
        n = A.shape[0]
        return int(nmod_mat(n, n, A.reshape(-1).tolist(), p).det())
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
      "coefficient_bound":str(bound),
      "crt_prime_count":len(primes),
      "crt_primes":primes,
      "crt_modulus_digits":len(str(modulus)),
      "crt_modulus":str(modulus),
      "verification_prime":vp,
      "exact_support":[amin+xmin,amax+xmin,bmin+ymin,bmax+ymin,len(nz)],
      "coefficient_ledger_sha256":h,
      "coefficient_ledger":ledger,
    })


# Rebuild the primitive Z[x,y] chart polynomials from the exact ledgers.
ck("LITERAL_STENCIL_HASH",hashlib.sha256(Path(S.__file__).read_bytes()).hexdigest()==STENCIL_SHA256)
exact_ctx=fmpz_mpoly_ctx.get(("x","y"),"lex")
polys=[]; contents=[]; chart_degrees=[]
for ci,record in enumerate(records):
    ledger=record["coefficient_ledger"]
    payload=";".join(f"{a},{b},{c}" for a,b,c in ledger)
    ck("LEDGER_HASH_"+str(ci),hashlib.sha256(payload.encode()).hexdigest()==record["coefficient_ledger_sha256"])
    amin=min(a for a,b,c in ledger); bmin=min(b for a,b,c in ledger)
    content,P=exact_ctx.from_dict({(a-amin,b-bmin):c for a,b,c in ledger}).primitive()
    contents.append(abs(int(content)))
    polys.append(P)
    chart_degrees.append(tuple(int(v) for v in P.degrees()))
ck("PRIMITIVE_CHART_BIDEGREES",tuple(chart_degrees)==EXPECTED_BIDEGREES)

# A compact Hungarian dual is an exact proof of every valuation/degree bound:
# replay u_i+v_j against every exponent in each nonzero Sylvester entry.
def assignment_dual(cost):
    n=len(cost); infinity=10**12
    u=[0]*(n+1); v=[0]*(n+1); p=[0]*(n+1); way=[0]*(n+1)
    for i in range(1,n+1):
        p[0]=i; j0=0; minv=[infinity]*(n+1); used=[False]*(n+1)
        while True:
            used[j0]=True; i0=p[j0]; delta=infinity; j1=0
            for j in range(1,n+1):
                if used[j]: continue
                cur=cost[i0-1][j-1]-u[i0]-v[j]
                if cur<minv[j]: minv[j]=cur; way[j]=j0
                if minv[j]<delta: delta=minv[j]; j1=j
            if delta>=infinity: raise AssertionError("NO_PERFECT_MATCHING")
            for j in range(n+1):
                if used[j]: u[p[j]]+=delta; v[j]-=delta
                else: minv[j]-=delta
            j0=j1
            if p[j0]==0: break
        while True:
            j1=way[j0]; p[j0]=p[j1]; j0=way[j0]
            if j0==0: break
    return u[1:],v[1:]

def sylvester_entries_xy(A,B):
    m=int(A.degrees()[1]); n=int(B.degrees()[1]); size=m+n
    entries=[[{} for _ in range(size)] for _ in range(size)]
    for offset,count,P,degree in ((0,n,A,m),(n,m,B,n)):
        coeffs=[{} for _ in range(degree+1)]
        for (a,b),c in P.to_dict().items():
            coeffs[degree-int(b)][int(a)]=int(c)
        for row in range(count):
            for col,C in enumerate(coeffs): entries[offset+row][row+col]=C
    return entries

def certified_assignment_bound(entries,kind):
    size=len(entries); big=10**8
    costs=[]
    for row in entries:
        out=[]
        for C in row:
            if not C: out.append(big)
            elif kind=="valuation": out.append(min(C))
            elif kind=="degree": out.append(-max(C))
            else: raise AssertionError("BAD_BOUND_KIND")
        costs.append(out)
    u,v=assignment_dual(costs)
    for i,row in enumerate(entries):
        for j,C in enumerate(row):
            if C:
                threshold=min(C) if kind=="valuation" else -max(C)
                if u[i]+v[j]>threshold: raise AssertionError("DUAL_INEQUALITY")
    value=sum(u)+sum(v)
    return (value if kind=="valuation" else -value),u,v

E03=sylvester_entries_xy(polys[0],polys[3])
E12=sylvester_entries_xy(polys[1],polys[2])
ord03,u03,v03=certified_assignment_bound(E03,"valuation")
ord12,u12,v12=certified_assignment_bound(E12,"valuation")
deg03,ud03,vd03=certified_assignment_bound(E03,"degree")
ck("R03_X_VALUATION_LOWER_BOUND_230",ord03==230)
ck("R12_X_VALUATION_LOWER_BOUND_272",ord12==272)
ck("R03_X_DEGREE_UPPER_BOUND_2511",deg03==2511)

# One good prime suffices after the exact common divisor x^230 and the exact
# R03 degree are established above.
ck("CHARZERO_PRIME",sp.isprime(PRIME))
ck("PRIME_DOES_NOT_DIVIDE_CHART_CONTENTS",all(c%PRIME for c in contents))
crt_primes={p for r in records for p in r["crt_primes"]}
ck("CHARZERO_PRIME_DISTINCT_FROM_CRT",PRIME not in crt_primes)
mod_ctx=nmod_mpoly_ctx.get(names=("x","y"),ordering="lex",modulus=PRIME)
modpolys=[mod_ctx.from_dict({ab:int(c)%PRIME for ab,c in P.to_dict().items() if int(c)%PRIME}) for P in polys]
ck("Y_DEGREES_PRESERVED",all(int(modpolys[i].degrees()[1])==int(polys[i].degrees()[1]) for i in range(4)))
R03=modpolys[0].resultant(modpolys[3],"y")
R12=modpolys[1].resultant(modpolys[2],"y")
ck("R03_DEGREE_PRESERVED_AT_EXACT_BOUND",int(R03.degrees()[0])==deg03)
ck("R12_MODULAR_RESULTANT_DEGREE",int(R12.degrees()[0])==2863)
xgen,_=mod_ctx.gens()
mod_gcd=R03.gcd(R12)
ck("MODULAR_RESULTANT_GCD_X230",mod_gcd==xgen**230)

result={
    "schema":"a4d-y-curved-joint-zminus1-interior-fiber-v1",
    "terminal":"A4D-Y-CURVED-JOINT-ZMINUS1-INTERIOR-FIBER-CERTIFIED",
    "fixed_ratio":"rho=(1,x,y,-1)",
    "domain":"(x,y) in (C*)^2",
    "operator":"68-row phase-1/phase-2 interior block of the literal 136x96 joint symbol",
    "literal_stencil_sha256":STENCIL_SHA256,
    "entry_denominator_clearance":"14*x*y",
    "chart_primitive_bidegrees":[list(v) for v in chart_degrees],
    "charts":[{
        "chart_index":r["chart_index"],
        "assignment_bounds":r["assignment_bounds"],
        "coefficient_bound":r["coefficient_bound"],
        "crt_prime_count":r["crt_prime_count"],
        "crt_primes":r["crt_primes"],
        "crt_modulus":r["crt_modulus"],
        "verification_prime":r["verification_prime"],
        "exact_support":r["exact_support"],
        "coefficient_ledger_sha256":r["coefficient_ledger_sha256"],
        "coefficient_ledger":r["coefficient_ledger"],
    } for r in records],
    "resultant_pairing":["R03=Res_y(P0,P3)","R12=Res_y(P1,P2)"],
    "exact_structural_divisor":"x^230",
    "exact_x_valuation_lower_bounds":{"R03":ord03,"R12":ord12},
    "exact_R03_degree_upper_bound":deg03,
    "assignment_duals":{
        "R03_valuation":{"rows":u03,"cols":v03},
        "R12_valuation":{"rows":u12,"cols":v12},
        "R03_degree":{"rows":ud03,"cols":vd03},
    },
    "good_prime":PRIME,
    "modular_resultant_degrees":{"R03":int(R03.degrees()[0]),"R12":int(R12.degrees()[0])},
    "modular_resultant_gcd":"x^230",
    "charzero_resultant_gcd":"x^230",
    "four_minor_common_zero_set_in_complex_torus":"empty",
    "interior_rank_conclusion":"rank 68 at every (x,y) in (C*)^2 for rho=(1,x,y,-1)",
    "proof":"Exact CRT minors; checked Hungarian duals prove x^230 divides both resultants and deg R03<=2511; at one good prime deg R03=2511 and gcd(R03,R12)=x^230. The primitive-gcd reduction lemma gives the characteristic-zero gcd. A common zero of all four minors would force a nonzero common root of R03 and R12, impossible.",
    "scope_fence":[
        "one fixed z=-1 fiber only",
        "interior 68-row block only; not full 136x96 column rank",
        "does not prove H_TORUS, a compact-complement gap, or normalized response decoupling",
        "does not prove the generic z fiber or remaining boundary-row rank"
    ]
}
if "--write" in __import__("sys").argv:
    OUT.write_text(json.dumps(result,indent=2)+"\n")
    print("WROTE",OUT,flush=True)
elif OUT.exists():
    ck("RESULTS_MATCH_PINNED_JSON",json.loads(OUT.read_text())==result)
print("TERMINAL",result["terminal"],flush=True)
