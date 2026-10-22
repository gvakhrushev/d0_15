#!/usr/bin/env python3
"""Original G2*STAR based-six-face exact rational Lorentz-local invariance
and the nonabelian two-end temporal-gauge Wilson-line obstruction.

No new action, no continuum/Gauss equation inserted, no GR closure claimed.
"""
from itertools import combinations
import sympy as s
import json

I=s.eye(4)
eta=s.diag(1,-1,-1,-1)
pairs=list(combinations(range(4),2))
G2=s.diag(*[eta[i,i]*eta[j,j] for i,j in pairs])
star=s.zeros(6,6)
star_map={
 (0,1):((2,3),-1),(0,2):((1,3),1),(0,3):((1,2),-1),
 (1,2):((0,3),1),(1,3):((0,2),-1),(2,3):((0,1),1)}
for x,(y,sign) in star_map.items():
    star[pairs.index(y),pairs.index(x)]=sign

def boost(j,a,b):
    U=s.eye(4)
    U[0,0]=U[j,j]=a
    U[0,j]=U[j,0]=b
    assert U.T*eta*U==eta and U.det()==1
    return U

def star_six(e,U,V):
    val=s.Rational(0)
    for r,t in pairs:
        # Original homogeneous spatial stencil:
        # for time-space faces the second link sits at the NEXT time.
        P=U[r]*(V[t] if r==0 else U[t])*U[r].inv()*U[t].inv()
        odd=(P-P.inv())/2
        C=odd*eta
        v=s.Matrix([C[i,j] for i,j in pairs])
        a,b=[j for j in range(4) if j not in (r,t)]
        W=s.Matrix([e[i,a]*e[j,b]-e[j,a]*e[i,b] for i,j in pairs])
        seq=[r,t,a,b]
        eps=(-1)**sum(seq[i]>seq[j] for i in range(4)
                      for j in range(i+1,4))
        val+=eps*(W.T*G2*star*v)[0]
    return val

def run():
    B1=boost(1,s.Rational(5,3),s.Rational(4,3))
    B2=boost(2,s.Rational(13,5),s.Rational(12,5))
    B3=boost(3,s.Rational(5,4),s.Rational(3,4))
    R=s.eye(4)
    R[2,2]=R[3,3]=s.Rational(3,5)
    R[2,3]=s.Rational(4,5)
    R[3,2]=-s.Rational(4,5)
    g=B1*R
    assert g.det()==1 and g.T*eta*g==eta
    Uprev=[B1,B2,B3,R]
    Ucur=[B2,B3,B1*R,R*B2]
    Unext=[B3,B1*B3,R*B1,B2*R]
    eprev=I
    ecur=s.Matrix([
        [s.Rational(7,5),s.Rational(1,8),0,0],
        [0,s.Rational(8,7),s.Rational(1,7),0],
        [0,0,s.Rational(9,8),s.Rational(1,12)],
        [0,0,0,s.Rational(10,9)]])
    old0=star_six(eprev,Uprev,Ucur)
    old1=star_six(ecur,Ucur,Unext)
    movedprev=Uprev.copy()
    movedcur=Ucur.copy()
    # One genuine local Lorentz change at a single time slice:
    # outgoing temporal U0(t) receives g on LEFT,
    # incoming U0(t-h) receives g^-1 on RIGHT.
    movedprev[0]=Uprev[0]*g.inv()
    movedcur[0]=g*Ucur[0]
    for j in (1,2,3):
        movedcur[j]=g*Ucur[j]*g.inv()
    assert star_six(eprev,movedprev,movedcur)==old0
    assert star_six(g*ecur,movedcur,Unext)==old1
    # Any local scalar Clifford kinetic q is invariant because
    # (g*e)^T eta(g*e)=e^T eta e.
    assert (g*ecur).T*eta*(g*ecur)==ecur.T*eta*ecur
    # A temporal gauge with initial g0=I uniquely recurses as
    # g_(t+1)=g_t U0(t), so fixing terminal gn=I in addition
    # is possible only if the ordered time Wilson product is I.
    Wline=B1*R*B2
    assert Wline!=I
    recursive=I
    for U0 in (B1,R,B2):recursive=recursive*U0
    assert recursive==Wline
    return dict(status="PASS_ORIGINAL_FINITE_GAUSS_AND_TWO_END_HOLONOMY",
       verified_exact_rational_two_neighbor_stars=True,
       internal_metric_and_CAR_q_invariant=True,
       temporal_gauge="U0(t)'=g_t U0(t) g_(t+1)^-1=I",
       unique_gauge_recursion="g_(t+1)=g_t U0(t)",
       both_end_fixed_condition="ordered product U0(t) = I",
       nontrivial_original_SO13_Wilson_counterexample=True,
       actual_full42_root=False,physical_Book03_selection=False,GR_closed=False)

if __name__=="__main__":
    print(json.dumps(run(),indent=2))
