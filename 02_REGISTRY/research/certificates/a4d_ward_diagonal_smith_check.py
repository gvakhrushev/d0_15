#!/usr/bin/env python3
"""Exact diagonal determinant and local Smith-exponent certificate for A4D.

Rebuilds the 24x24 polarized connection Hessian from the finite plaquette
action, checks its diagonal determinant and the first derivative induced from
kernel to cokernel at z=i, then derives the local invariant-factor orders over
the one-variable DVR C[[w]]. No floating-point pole fitting is used.
"""
import sympy as sp, json, time
from itertools import combinations
from pathlib import Path
t0=time.time()
PAIRS=list(combinations(range(4),2)); PI={p:i for i,p in enumerate(PAIRS)}
I=sp.I
def rot(i,j):
    X=sp.zeros(4); X[i,j]=1; X[j,i]=-1; return X
def boost(i):
    X=sp.zeros(4); X[i,0]=X[0,i]=1; return X
GEN=[boost(1),boost(2),boost(3),rot(1,2),rot(1,3),rot(2,3)]
ETA=sp.diag(1,-1,-1,-1)
G2=sp.diag(*[ETA[a,a]*ETA[b,b] for a,b in PAIRS])
STAR=sp.zeros(6)
for src,(dst,s) in {(0,1):((2,3),-1),(0,2):((1,3),1),(0,3):((1,2),-1),
                    (1,2):((0,3),1),(1,3):((0,2),-1),(2,3):((0,1),1)}.items():
    STAR[PI[dst],PI[src]]=s
def wedge(u,v): return sp.Matrix([u[a]*v[b]-u[b]*v[a] for a,b in PAIRS])
def biv(X):
    Y=X*ETA; return sp.Matrix([Y[a,b] for a,b in PAIRS])
def co(f):
    c=[i for i in range(4) if i not in f]; seq=list(f)+c
    inv=sum(seq[i]>seq[j] for i in range(4) for j in range(i+1,4)); return -1 if inv%2 else 1
def mul4(X,Y): return (X[0]*Y[0],X[0]*Y[1]+X[1]*Y[0],X[0]*Y[2]+X[2]*Y[0],X[0]*Y[3]+X[1]*Y[2]+X[2]*Y[1]+X[3]*Y[0])
def exp4(A0,B0,pa=1,pb=1,inv=False):
    s=-1 if inv else 1
    return (sp.eye(4),s*pa*A0,s*pb*B0,sp.Rational(1,2)*pa*pb*(A0*B0+B0*A0))
def cmix(P): return P[3]-sp.Rational(1,2)*(P[1]*P[2]+P[2]*P[1])
bc=[sp.eye(4)[:,r] for r in range(4)]
av=sp.symbols("a0:24"); bv=sp.symbols("b0:24"); hv=sp.symbols("h0:16")
A_=[sum((av[6*r+j]*GEN[j] for j in range(6)),sp.zeros(4)) for r in range(4)]
Bc=[sum((bv[6*r+j]*GEN[j] for j in range(6)),sp.zeros(4)) for r in range(4)]
H=[sp.Matrix(hv[4*r:4*r+4]) for r in range(4)]
SYM=[(a,b) for a in range(4) for b in range(a,4)]
Bmet=sp.zeros(16,10)
for j,(a0,b0) in enumerate(SYM):
    q=sp.zeros(4); q[a0,b0]=q[b0,a0]=1; Hh=sp.Rational(1,2)*q*ETA
    for r in range(4):
        for c in range(4): Bmet[4*r+c,j]=Hh[r,c]
def build(Z):
    cb=0; cr=0
    for r,s in PAIRS:
        P=mul4((sp.eye(4),sp.zeros(4),sp.zeros(4),sp.zeros(4)),exp4(A_[r],Bc[r]))
        P=mul4(P,exp4(A_[s],Bc[s],Z[r],1/Z[r]))
        P=mul4(P,exp4(A_[r],Bc[r],Z[s],1/Z[s],True))
        P=mul4(P,exp4(A_[s],Bc[s],inv=True))
        u,v=[i for i in range(4) if i not in (r,s)]
        ar=wedge(bc[u],bc[v]); sg=co((r,s))
        cb+=sg*(ar.T*G2*STAR*biv(cmix(P)))[0]
        C1=(1/Z[r]-1)*Bc[s]-(1/Z[s]-1)*Bc[r]
        B1=wedge(H[u],bc[v])+wedge(bc[u],H[v])
        cr+=sg*(B1.T*G2*STAR*biv(cmix(P)))[0]
    cb=sp.expand(cb); cr=sp.expand(cr)
    Ar=sp.zeros(24); Cc=sp.zeros(24,16)
    for i in range(24):
        di=sp.diff(cb,av[i])
        for j in range(24): Ar[i,j]=sp.diff(di,bv[j])
        dj=sp.diff(cr,bv[i])
        for j in range(16): Cc[i,j]=sp.diff(dj,hv[j])
    Cc=sp.expand(Cc.subs({v:0 for v in av}))
    return sp.expand(Ar), sp.expand(Cc)
orth=sp.Matrix([0,32,32,0,0,0,0,0,0,32,32,0,0,-32,0,-32,0,0,0,0,-32,0,-32,0])
F7  =sp.Matrix([0,0,0,-128,-128,0,0,-128,-128,0,0,0,0,128,0,128,0,0,0,0,128,0,128,0])
out={}
# 1) det closed form (spot verify at symbolic z)
z,w=sp.symbols("z w")
Aw=build([z,z,z,z])[0]
det=sp.factor(sp.together(Aw.det()))
out["det_A_diagonal"]=str(det)
out["det_matches_(z^2+1)^12/(16z^12)"]=bool(sp.simplify(det-(z**2+1)**12/(16*z**12))==0)
print("det A(z) =",out["det_A_diagonal"],"| matches:",out["det_matches_(z^2+1)^12/(16z^12)"],flush=True)
# 2) local degeneration matrix M = NL^T A' NK
A0w=build([I+w,I+w,I+w,I+w])[0]
A0=A0w.subs(w,0); A1=sp.diff(A0w,w).subs(w,0)
kerA=sp.Matrix(A0).nullspace(); leftA=sp.Matrix(A0).T.nullspace()
NK=sp.Matrix.hstack(*kerA); NL=sp.Matrix.vstack(*[v.T for v in leftA])
M=sp.Matrix(len(leftA),len(kerA),lambda i,j: sp.simplify((NL*sp.Matrix(A1)*NK)[i,j]))
out["rkA0"]=int(sp.Matrix(A0).rank())
out["nullity"]=24-out["rkA0"]
out["rank_M"]=int(M.rank())
print("rk A0 =",out["rkA0"],"nullity =",out["nullity"],"rank M =",out["rank_M"],flush=True)

# At a one-variable analytic matrix germ, the nonunit local Smith factors are
# w**e_j. Their number is nullity(A(0)); rank(N_L A'(0) N_K) counts e_j=1;
# ord(det A) is their sum. These three exact data determine every e_j here.
nullity = 24 - out["rkA0"]
det_numerator, det_denominator = sp.fraction(sp.together(det))
def multiplicity_at(poly_expr, root):
    poly = sp.Poly(poly_expr, z, extension=I)
    factor = sp.Poly(z - root, z, extension=I)
    multiplicity = 0
    while True:
        quotient, remainder = poly.div(factor)
        if not remainder.is_zero:
            return multiplicity
        poly = quotient
        multiplicity += 1

zero_order = multiplicity_at(det_numerator, I) - multiplicity_at(det_denominator, I)
smith_exponents = [1] * out["rank_M"] + [2] * (nullity - out["rank_M"])
assert out["det_matches_(z^2+1)^12/(16z^12)"] is True
assert out["rkA0"] == 16 and nullity == 8 and out["rank_M"] == 4
assert zero_order == 12
assert len(smith_exponents) == nullity and sum(smith_exponents) == zero_order
assert smith_exponents == [1, 1, 1, 1, 2, 2, 2, 2]
out["det_zero_order_at_i"] = zero_order
out["local_nonunit_smith_exponents_at_i"] = smith_exponents
out["smith_exponent_multiplicities"] = {"1": 4, "2": 4}
out["smith_derivation"] = "nullity=8, rank(N_L A_prime N_K)=4 counts exponent 1, ord(det)=12"
out["terminal"] = "A4D_DIAGONAL_LOCAL_SMITH_1x4_2x4_EXACT"
out_path = Path(__file__).with_name("a4d_ward_diagonal_smith_results.json")
out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
print("LOCAL_SMITH_EXPONENTS", smith_exponents, flush=True)
print("TERMINAL A4D_DIAGONAL_LOCAL_SMITH_1x4_2x4_EXACT", flush=True)
print("RESULT_JSON", out_path, flush=True)
print("TIME %.1fs" % (time.time() - t0), flush=True)
