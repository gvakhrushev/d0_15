#!/usr/bin/env python3
"""Exact homogeneous curved-stationary controls for the A4D star dynamics.

Research-only exact SymPy certificate.

It proves:
1. the two exact generic homogeneous link backgrounds used by the landed
   joint-holonomy quotient-completeness packet have invertible 16x16 solder
   Hessians, so homogeneous solder stationarity forces zero solder;
2. three exact rank-12 / nullity-4 homogeneous link candidates selected by a
   broad exploratory word scan have nonzero-solder kernels, but a literal
   single-edge Lorentz connection Euler component kills a factor required by
   the kernel solder determinant.

The exploratory scan is not part of the theorem.  Only the exact candidates
listed below are certified.
"""
import sympy as sp
from itertools import combinations, product

PAIRS=list(combinations(range(4),2))
PINDEX={p:i for i,p in enumerate(PAIRS)}
ETA=sp.diag(1,-1,-1,-1)
I4=sp.eye(4)
G2=sp.zeros(6)
for i,(a,b) in enumerate(PAIRS):
    G2[i,i]=ETA[a,a]*ETA[b,b]

STAR=sp.zeros(6)
STAR_MAP={
    (0,1):((2,3),-1),(0,2):((1,3),1),(0,3):((1,2),-1),
    (1,2):((0,3),1),(1,3):((0,2),-1),(2,3):((0,1),1),
}
for p,(q,s) in STAR_MAP.items():
    STAR[PINDEX[q],PINDEX[p]]=s

def check(name,cond):
    if not cond:
        raise AssertionError(name)
    print("PASS_"+name)

def wedge(u,v):
    return sp.Matrix([u[a]*v[b]-u[b]*v[a] for a,b in PAIRS])

def biv(X):
    Y=X*ETA
    return sp.Matrix([sp.expand(Y[a,b]) for a,b in PAIRS])

def orient(face):
    comp=[i for i in range(4) if i not in face]
    seq=list(face)+comp
    inv=sum(seq[i]>seq[j] for i in range(4) for j in range(i+1,4))
    return -1 if inv%2 else 1

BOOST=sp.eye(4)
BOOST[0,0]=sp.Rational(5,3); BOOST[0,1]=sp.Rational(4,3)
BOOST[1,0]=sp.Rational(4,3); BOOST[1,1]=sp.Rational(5,3)

R1=sp.eye(4)
R1[1,1]=0; R1[1,2]=1; R1[2,1]=-1; R1[2,2]=0

R2=sp.eye(4)
R2[2,2]=0; R2[2,3]=1; R2[3,2]=-1; R2[3,3]=0

for name,g in (("BOOST",BOOST),("R1",R1),("R2",R2)):
    check(name+"_LORENTZ",sp.simplify(g.T*ETA*g-ETA)==sp.zeros(4))
    check(name+"_DET_ONE",sp.factor(g.det())==1)

WORDS={
    "I":I4,"B":BOOST,"R1":R1,"R2":R2,
    "BR1":BOOST*R1,"BR2":BOOST*R2,
    "R1R2":R1*R2,"R2R1":R2*R1,
    "BR1R2":BOOST*R1*R2,
}

PRIMARY=[
    BOOST*R1,
    BOOST*R2,
    R2*R1,
    BOOST*R1*R2*BOOST.inv(),
]
ALT=[
    BOOST*R1,
    BOOST*R2,
    R2*R1,
    BOOST*R2*R1.inv(),
]

vvars=sp.symbols("v0:16")
VS=[sp.Matrix(vvars[4*r:4*r+4]) for r in range(4)]

def homogeneous_action(linkset,Vs=VS):
    total=sp.Integer(0)
    for r,s in PAIRS:
        P=sp.simplify(linkset[r]*linkset[s]*linkset[r].inv()*linkset[s].inv())
        C=biv(sp.simplify((P-P.inv())/2))
        u,v=[i for i in range(4) if i not in (r,s)]
        total += orient((r,s))*(wedge(Vs[u],Vs[v]).T*G2*STAR*C)[0]
    return sp.expand(total)

# Generic quotient-complete controls from the joint-holonomy packet.
EXPECTED_GENERIC={
    "PRIMARY":sp.Rational(2388791431069696,22876792454961),
    "ALT":sp.Rational(803169544344371200,68630377364883),
}
for name,linkset in (("PRIMARY",PRIMARY),("ALT",ALT)):
    H=sp.hessian(homogeneous_action(linkset),vvars)
    check(name+"_SOLDER_HESSIAN_RANK_16",H.rank()==16)
    check(name+"_SOLDER_HESSIAN_DET",sp.factor(H.det())==EXPECTED_GENERIC[name])

# Literal periodic single-edge connection derivative.
SITES=list(product(range(2),repeat=4))
ORIGIN=(0,0,0,0)
LORENTZ=[]
for i in (1,2,3):
    X=sp.zeros(4); X[0,i]=1; X[i,0]=1; LORENTZ.append(X)
for i,j in ((1,2),(1,3),(2,3)):
    X=sp.zeros(4); X[i,j]=1; X[j,i]=-1; LORENTZ.append(X)

def add(x,r):
    y=list(x); y[r]^=1
    return tuple(y)

def dplaquette(base,x,r,s,var_key,X):
    keys=[(x,r),(add(x,r),s),(add(x,s),r),(x,s)]
    invs=[False,False,True,True]
    mats=[]; dmats=[]
    for key,inv in zip(keys,invs):
        L=base[key]
        if not inv:
            mats.append(L)
            dmats.append(X*L if key==var_key else sp.zeros(4))
        else:
            Li=L.inv()
            mats.append(Li)
            dmats.append(-Li*X if key==var_key else sp.zeros(4))
    P=mats[0]*mats[1]*mats[2]*mats[3]
    dP=sp.zeros(4)
    for j in range(4):
        if dmats[j]==sp.zeros(4):
            continue
        term=sp.eye(4)
        for k in range(4):
            term=term*(dmats[k] if k==j else mats[k])
        dP += term
    Pinv=P.inv()
    return sp.simplify((dP+Pinv*dP*Pinv)/2)

def connection_euler(base,Vs,var_key,X):
    total=sp.Integer(0)
    for x in SITES:
        for r,s in PAIRS:
            dC=dplaquette(base,x,r,s,var_key,X)
            if dC==sp.zeros(4):
                continue
            u,v=[i for i in range(4) if i not in (r,s)]
            total += orient((r,s))*(wedge(Vs[u],Vs[v]).T*G2*STAR*biv(dC))[0]
    return sp.factor(total)

CANDIDATES=[
    (
        "A",("R1","B","BR1R2","BR1"),
        sp.Rational(9,20),
        lambda c: c[0]*(c[2]-c[3])**2*(3*c[2]-5*c[3]),
        (2,0),
        lambda c: -sp.Rational(4,5)*c[0]*(c[2]-c[3]),
    ),
    (
        "B",("B","R1R2","BR1","BR1R2"),
        -sp.Rational(16,15),
        lambda c: c[0]*c[3]*(c[2]+4*c[3])*(c[1]-c[2]+6*c[3]),
        (2,0),
        lambda c: sp.Rational(142,45)*c[0]*c[3],
    ),
    (
        "C",("R1R2","R1","B","R2R1"),
        -sp.Integer(4),
        lambda c: c[1]*c[3]*(c[0]+c[3])*(2*c[2]-c[3]),
        (3,2),
        lambda c: -c[1]*c[3],
    ),
]

for tag,names,det_scale,det_core,euler_index,euler_expected in CANDIDATES:
    linkset=[WORDS[n] for n in names]
    H=sp.hessian(homogeneous_action(linkset),vvars)
    check(tag+"_SOLDER_HESSIAN_RANK_12",H.rank()==12)
    ns=H.nullspace()
    check(tag+"_SOLDER_KERNEL_DIM_4",len(ns)==4)
    c=sp.symbols("c0:4")
    vec=sum((c[i]*ns[i] for i in range(4)),sp.zeros(16,1))
    legs=[vec[4*r:4*r+4,:] for r in range(4)]
    detV=sp.factor(sp.Matrix.hstack(*legs).det())
    check(tag+"_KERNEL_DETERMINANT",
          sp.simplify(detV-det_scale*det_core(c))==0)

    base={(x,r):linkset[r] for x in SITES for r in range(4)}
    role,generator=euler_index
    e=connection_euler(base,legs,(ORIGIN,role),LORENTZ[generator])
    check(tag+"_CONNECTION_EULER_FACTOR",
          sp.simplify(e-euler_expected(c))==0)

    # Exact implication: the displayed Euler factor is a mandatory factor of
    # the nondegeneracy determinant.  If the full Euler system vanishes, this
    # component vanishes and hence det(V)=0.
    if tag=="A":
        check(tag+"_EULER_ZERO_KILLS_NONDEGENERACY_FACTOR",
              sp.factor(detV/e).is_polynomial(*c))
    elif tag=="B":
        check(tag+"_EULER_ZERO_KILLS_NONDEGENERACY_FACTOR",
              sp.factor(detV/e).is_polynomial(*c))
    else:
        check(tag+"_EULER_ZERO_KILLS_NONDEGENERACY_FACTOR",
              sp.factor(detV/e).is_polynomial(*c))

print("RESULT_GENERIC_CONTROLS: both exact generic quotient-complete homogeneous backgrounds have rank-16 solder Hessian; homogeneous solder stationarity forces V=0.")
print("RESULT_RANK12_A: connection Euler kills c0*(c2-c3), required by nondegenerate kernel solder.")
print("RESULT_RANK12_B: connection Euler kills c0*c3, required by nondegenerate kernel solder.")
print("RESULT_RANK12_C: connection Euler kills c1*c3, required by nondegenerate kernel solder.")
print("TERMINAL_SCOPED: FIVE-EXACT-HOMOGENEOUS-CURVED-CONTROLS-HAVE-NO-NONDEGENERATE-FULL-STATIONARY-POINT")
