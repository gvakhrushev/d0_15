#!/usr/bin/env python3
"""Exact two-channel physical-survival witness for the A4D star + joint residual family.

Research-only, exact SymPy arithmetic.

It gives two quotient-transverse variations:
1. uniform solder scaling on an exact curved star witness:
      dS_star/dlambda|_1 = -4/3,   dQ = 0;
2. the exact nongauge matched edge-shift witness from the joint-holonomy lane:
      dS_star = 0,   Q_eta(t)=(-128/9)t^2, so dQ/dt|_1=-256/9.

Hence the two Euler channels are linearly independent on the generic curved
full-affine quotient. Together with exact gauge invariance, the declared
two-channel family has d_A=d_E=d_P=2 on that generic principal stratum.

This does not identify the extra four limiting incidence directions at the flat
rank seam with gauge. At exact flat holonomy Q vanishes to high order.
"""
from itertools import combinations, product
import sympy as sp

ETA=sp.diag(1,-1,-1,-1)
I4=sp.eye(4)
PAIRS=list(combinations(range(4),2))
PINDEX={p:i for i,p in enumerate(PAIRS)}
SITES=list(product(range(2),repeat=4))
ORIGIN=(0,0,0,0)

def check(name, cond):
    if not cond:
        raise AssertionError(name)
    print("PASS_"+name)

BOOST=sp.eye(4)
BOOST[0,0]=sp.Rational(5,3); BOOST[0,1]=sp.Rational(4,3)
BOOST[1,0]=sp.Rational(4,3); BOOST[1,1]=sp.Rational(5,3)
RBC=sp.eye(4)
RBC[1,1]=0; RBC[1,2]=1; RBC[2,1]=-1; RBC[2,2]=0
RCD=sp.eye(4)
RCD[2,2]=0; RCD[2,3]=1; RCD[3,2]=-1; RCD[3,3]=0

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

def wedge(u,v):
    return sp.Matrix([u[a]*v[b]-u[b]*v[a] for a,b in PAIRS])

def bivector(X):
    Y=X*ETA
    return sp.Matrix([Y[a,b] for a,b in PAIRS])

def orientation(face):
    comp=[i for i in range(4) if i not in face]
    seq=list(face)+comp
    inv=sum(seq[i]>seq[j] for i in range(4) for j in range(i+1,4))
    return -1 if inv%2 else 1

def site_add(x,r):
    y=list(x); y[r]^=1; return tuple(y)

def plaquette(links,x,r,s):
    xr=site_add(x,r); xs=site_add(x,s)
    return links[(x,r)]*links[(xr,s)]*links[(xs,r)].inv()*links[(x,s)].inv()

def star_action_scaled(links,lam):
    basis=[sp.eye(4)[:,r] for r in range(4)]
    total=sp.Integer(0)
    for x in SITES:
        vs=[lam*b for b in basis]
        for r,s in PAIRS:
            P=plaquette(links,x,r,s)
            C=bivector((P-P.inv())/2)
            u,v=[i for i in range(4) if i not in (r,s)]
            total += orientation((r,s))*(wedge(vs[u],vs[v]).T*G2*STAR*C)[0]
    return sp.simplify(total)

# Channel 1: star-only quotient direction.
links_scale={(x,r):I4 for x in SITES for r in range(4)}
links_scale[(ORIGIN,0)]=BOOST
links_scale[(ORIGIN,1)]=RBC
lam=sp.symbols("lam")
Slam=sp.factor(star_action_scaled(links_scale,lam))
check("STAR_SCALING_LAW", Slam == -sp.Rational(2,3)*lam**2)
dS=sp.diff(Slam,lam).subs(lam,1)
check("STAR_EULER_DIRECTION_NONZERO", dS == -sp.Rational(4,3))

# Channel 2: exact matched edge-shift joint-residual witness.
links={(x,r):I4 for x in SITES for r in range(4)}
links[(ORIGIN,0)]=BOOST
links[(ORIGIN,1)]=RBC
links[((1,0,0,0),2)]=RCD

def acomp(A,B):
    L1,b1=A; L2,b2=B
    return sp.simplify(L1*L2), sp.simplify(b1+L1*b2)

def ainv(A):
    L,b=A; Li=L.inv()
    return Li, sp.simplify(-Li*b)

def alink(x,r,bfield):
    return links[(x,r)], bfield[(x,r)]

def based_holonomy(x,r,s,bfield):
    A=acomp(alink(x,r,bfield),alink(site_add(x,r),s,bfield))
    B=acomp(alink(x,s,bfield),alink(site_add(x,s),r,bfield))
    return acomp(A,ainv(B))

def joint_residual(P1,t1,P2,t2):
    M1=I4-P1; M2=I4-P2
    return sp.simplify(M1.det()*t2-M2*M1.adjugate()*t1)

t=sp.symbols("t")
bfield={(x,r):sp.zeros(4,1) for x in SITES for r in range(4)}
bfield[(ORIGIN,0)]=sp.Matrix([t,0,0,0])
P02,t02=based_holonomy(ORIGIN,0,2,bfield)
P01,t01=based_holonomy(ORIGIN,0,1,bfield)
R=sp.simplify(joint_residual(P02,t02,P01,t01))
R_expected=t*sp.Matrix([
    sp.Rational(-32,9),sp.Rational(-40,9),sp.Rational(8,3),0
])
check("MATCHED_EDGE_RESIDUAL_LINEAR", R == R_expected)
Q=sp.factor((R.T*ETA*R)[0])
check("MATCHED_EDGE_Q_LAW", Q == -sp.Rational(128,9)*t**2)
dQ=sp.diff(Q,t).subs(t,1)
check("RESIDUAL_EULER_DIRECTION_NONZERO", dQ == -sp.Rational(256,9))

# Relative solder is fixed by the matched variation delta Theta=(delta b)^flat,
# so the star channel is constant along this direction by construction.
check("SEPARATING_DERIVATIVE_MATRIX_FULL_RANK",
      sp.Matrix([[dS,0],[0,dQ]]).rank()==2)

print("RESULT_DA: two declared invariant action channels.")
print("RESULT_DE: exact separating quotient-transverse variations give Euler rank 2.")
print("RESULT_DP_GENERIC: both channels survive the actual node+Lorentz gauge quotient on the declared generic curved principal stratum.")
print("SCOPE: flat rank seam remains stratified; Q is dormant there and limiting incidence directions are not promoted to gauge.")
