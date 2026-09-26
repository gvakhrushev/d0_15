#!/usr/bin/env python3
"""Exact Einstein-ray detector for the A4D star + joint-residual family.

Research-only, exact SymPy arithmetic.

This checker proves the flat small-momentum metric Hessian of the accepted
A4D star density is exactly one quarter of the owned Lorentz Einstein ray
E_eta after eliminating the 24 auxiliary Lorentz-connection variables.

It also records the order-counting control for the polynomial two-holonomy
residual: near flat P_i=I+O(eps), t_i=O(eps), the residual is O(eps^5), so
every quadratic Q(R) is O(eps^10) and cannot modify the quadratic/linearized
Einstein detector.
"""
from itertools import combinations
import sympy as sp

PAIRS = list(combinations(range(4), 2))
PINDEX = {p:i for i,p in enumerate(PAIRS)}
ETA = sp.diag(1,-1,-1,-1)

def check(name, cond):
    if not cond:
        raise AssertionError(name)
    print("PASS_"+name)

LORENTZ=[]
for i in (1,2,3):
    X=sp.zeros(4); X[0,i]=1; X[i,0]=1; LORENTZ.append(X)
for i,j in ((1,2),(1,3),(2,3)):
    X=sp.zeros(4); X[i,j]=1; X[j,i]=-1; LORENTZ.append(X)
for X in LORENTZ:
    check("LORENTZ_TANGENT", X.T*ETA+ETA*X == sp.zeros(4))

G2=sp.zeros(6)
for i,(a,b) in enumerate(PAIRS):
    G2[i,i]=ETA[a,a]*ETA[b,b]

STAR=sp.zeros(6)
STAR_MAP={
    (0,1):((2,3),-1), (0,2):((1,3),+1), (0,3):((1,2),-1),
    (1,2):((0,3),+1), (1,3):((0,2),-1), (2,3):((0,1),+1),
}
for p,(q,s) in STAR_MAP.items():
    STAR[PINDEX[q],PINDEX[p]]=s
check("STAR_SQUARE_MINUS_ID", STAR*STAR == -sp.eye(6))

def wedge_vec(u,v):
    return sp.Matrix([u[a]*v[b]-u[b]*v[a] for a,b in PAIRS])

def bivector_of_tangent(X):
    Y=X*ETA
    return sp.Matrix([Y[a,b] for a,b in PAIRS])

def complement_orientation(face):
    comp=[i for i in range(4) if i not in face]
    seq=list(face)+comp
    inv=sum(seq[i]>seq[j] for i in range(4) for j in range(i+1,4))
    return -1 if inv%2 else 1

def mul_jet(X,Y):
    return (
        X[0]*Y[0],
        X[0]*Y[1]+X[1]*Y[0],
        X[0]*Y[2]+X[1]*Y[1]+X[2]*Y[0],
    )

def exp_link(A, scale=1, inverse=False):
    B=scale*A
    return (sp.eye(4), -B if inverse else B, B*B/2)

XVAR=sp.symbols("x0:40")

def quadratic_density(signs):
    h=[sp.Matrix(XVAR[4*r:4*r+4]) for r in range(4)]
    A=[]
    for r in range(4):
        Y=sp.zeros(4)
        for j,B in enumerate(LORENTZ):
            Y += XVAR[16+6*r+j]*B
        A.append(Y)
    basis=[sp.eye(4)[:,r] for r in range(4)]
    total=sp.Integer(0)
    for r,s in PAIRS:
        P=(sp.eye(4),sp.zeros(4),sp.zeros(4))
        P=mul_jet(P,exp_link(A[r]))
        P=mul_jet(P,exp_link(A[s],signs[r]))
        P=mul_jet(P,exp_link(A[r],signs[s],inverse=True))
        P=mul_jet(P,exp_link(A[s],inverse=True))
        P1,P2=P[1],P[2]
        C1=bivector_of_tangent(P1)
        C2=bivector_of_tangent(P2-P1*P1/2)
        u,v=[i for i in range(4) if i not in (r,s)]
        B0=wedge_vec(basis[u],basis[v])
        B1=wedge_vec(h[u],basis[v])+wedge_vec(basis[u],h[v])
        total += complement_orientation((r,s))*(
            (B0.T*G2*STAR*C2)[0] + (B1.T*G2*STAR*C1)[0]
        )
    return sp.expand(total)

def hessian(signs):
    return sp.hessian(quadratic_density(signs), XVAR)

H0=hessian((1,1,1,1))
HAA=H0[16:,16:]
HAH0=H0[16:,:16]
check("FLAT_CONNECTION_BLOCK_RANK_24", HAA.rank()==24)
check("ZERO_MOMENTUM_COFRAME_CONNECTION_CROSS_ZERO", HAH0==sp.zeros(24,16))
HAA_INV=HAA.inv()

eps=sp.symbols("eps")
D=[]
for r in range(4):
    signs=[1,1,1,1]
    signs[r]=1+eps
    H=hessian(signs)
    Dr=H[16:,:16].applyfunc(lambda z: sp.diff(z,eps).subs(eps,0))
    D.append(Dr)
    check("CROSS_DERIVATIVE_RANK_12_"+str(r), Dr.rank()==12)

SYM=[(a,b) for a in range(4) for b in range(a,4)]
B=sp.zeros(16,10)
for j,(a,b) in enumerate(SYM):
    q=sp.zeros(4)
    q[a,b]=1
    q[b,a]=1
    H=sp.Rational(1,2)*q*ETA
    for r in range(4):
        for c in range(4):
            B[4*r+c,j]=H[r,c]

KSTAR={}
for r in range(4):
    for s in range(r,4):
        if r==s:
            C=-B.T*D[r].T*HAA_INV*D[r]*B
        else:
            C=-B.T*(D[r].T*HAA_INV*D[s]+D[s].T*HAA_INV*D[r])*B
        KSTAR[(r,s)]=sp.simplify(C)

qvars=sp.symbols("q0:10")
Q=sp.zeros(4)
for j,(a,b) in enumerate(SYM):
    Q[a,b]=qvars[j]
    Q[b,a]=qvars[j]
k=sp.symbols("k0:4")
kv=sp.Matrix(k)
kup=ETA*kv
ksq=(kv.T*ETA*kv)[0]
tr=sum(ETA[a,a]*Q[a,a] for a in range(4))
v=sp.Matrix([sum(kup[c]*Q[c,b] for c in range(4)) for b in range(4)])
qq=sum(kup[c]*kup[d]*Q[c,d] for c in range(4) for d in range(4))
E=sp.zeros(4)
for a in range(4):
    for b in range(4):
        E[a,b]=sp.expand(
            ksq*Q[a,b]-k[a]*v[b]-k[b]*v[a]+k[a]*k[b]*tr
            +ETA[a,b]*qq-ETA[a,b]*ksq*tr
        )
EUP=ETA*E*ETA
SE=sp.Rational(1,2)*sum(Q[a,b]*EUP[a,b] for a in range(4) for b in range(4))
KETA=sp.hessian(sp.expand(SE),qvars)

KETA_COEFF={}
for r in range(4):
    for s in range(r,4):
        if r==s:
            C=KETA.applyfunc(lambda z: sp.diff(z,k[r],2)/2)
        else:
            C=KETA.applyfunc(lambda z: sp.diff(sp.diff(z,k[r]),k[s]))
        KETA_COEFF[(r,s)]=sp.simplify(C)

for key in KSTAR:
    check(
        "EINSTEIN_RAY_COEFF_"+str(key[0])+str(key[1]),
        sp.simplify(KSTAR[key]-sp.Rational(1,4)*KETA_COEFF[key]) == sp.zeros(10),
    )

def eval_quad(coeff,kval):
    out=sp.zeros(10)
    for r in range(4):
        for s in range(r,4):
            out += coeff[(r,s)]*kval[r]*kval[s]
    return sp.simplify(out)

for tag,kval,rank in (
    ("TIMELIKE",(1,0,0,0),6),
    ("SPACELIKE",(0,1,0,0),6),
    ("NULL",(1,1,0,0),4),
    ("GENERIC",(1,2,3,4),6),
):
    check("STAR_METRIC_RANK_"+tag, eval_quad(KSTAR,kval).rank()==rank)

A=sp.Matrix([[1,2,0,0],[0,1,1,0],[0,0,1,1],[1,0,0,2]])
B2=sp.Matrix([[2,0,1,0],[1,1,0,1],[0,1,2,0],[0,0,1,1]])
u=sp.Matrix([1,2,3,4]); w=sp.Matrix([-1,0,2,1])
z=sp.symbols("z")
M1=z*A
M2=z*B2
t1=z*u; t2=z*w
R=sp.simplify(M1.det()*t2 - M2*M1.adjugate()*t1)
check("JOINT_RESIDUAL_ORDER_FIVE", all(sp.factor(c/z**5).has(z)==False for c in R))
Qres=sp.expand((R.T*R)[0])
check("QUADRATIC_RESIDUAL_ORDER_TEN", sp.limit(Qres/z**10,z,0).is_finite)
for n in range(10):
    check("QUADRATIC_RESIDUAL_DERIV_ZERO_"+str(n), sp.diff(Qres,z,n).subs(z,0)==0)

print("RESULT_F5: K_star,metric(k) = (1/4) K_E_eta(k) exactly on all ten k_a k_b coefficients.")
print("RESULT_EXTRA_RAY: the E_sp coefficient is therefore exactly zero in the owned two-ray Lorentz response space.")
print("RESULT_Q_ORDER: every quadratic two-holonomy residual term is O(eps^10) near flat and cannot alter the quadratic Einstein detector.")
print("TERMINAL: A4D-STAR-FLAT-METRIC-HESSIAN-IS-PURE-EINSTEIN-RAY")
