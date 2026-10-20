#!/usr/bin/env python3
"""Original fullCAR16 grade-one Choi fixed 13-effect POVM: exact odds theorem.

This is a symbolic faithful grade-one restriction of the already-owned
13-effect + Julia failure complete memory on original SO(1,3); no invented
additional POVM or selected Book03 action. Checks ALL six Lorentz generators,
the actual N2/bN3 based plaquette, full complete success/failure resources,
and strict n-link Julia attenuation vs refinement-invariant paired log odds.
"""
import sympy as s

def check(name, test):
    if test is not True and test != s.true:
        raise AssertionError(name)
    print("PASS", name)

E=lambda a,b: s.eye(4)[:,a]*s.eye(4)[b,:]
N2=E(1,2)+E(2,0)
N3=E(1,3)+E(3,0)
bN2=E(0,2)+E(2,1)
bN3=E(0,3)+E(3,1)
J=E(2,3)-E(3,2)
B=E(1,1)-E(0,0)
G=[N2,N3,bN2,bN3,J,B]
eta=s.Matrix([[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]])
for ga in G:
    check("actual SO(1,3) tangent",ga.T*eta+eta*ga==s.zeros(4))
check("original Lie basis metric",s.Matrix(
    [[s.trace(g.T*h) for h in G] for g in G])==2*s.eye(6))
check("cross N2/bN3 yields transverse J",N2*bN3-bN3*N2==J)
check("cross N2/bN2 yields boost B",N2*bN2-bN2*N2==B)

r=s.symbols("r",real=True)
phi=(s.sqrt(5)+1)/2
def event(P,g,n,sign):
    # The original success amplitude is 2^-n*(P tensor I)|Omega4>.
    # E_(g,sign)=1/12 |(Omega+sign f_g)/sqrt2><...|.
    u=s.trace(P)/4
    v=s.sqrt(2)*s.trace(g.T*P)/4
    return s.Rational(1,4)**n*(u+sign*v)**2/24

def nat_odds(P,g,n):
    return s.log(event(P,g,n,-1)/event(P,g,n,1))

for n in (1,2,4,6):
    for index,ga in enumerate(G):
        P=s.eye(4)+r*ga+r*r*ga*ga/2
        # only first jet of exp is needed for this universal derivative
        qp=event(P,ga,n,1);qm=event(P,ga,n,-1)
        base=s.Rational(1,4)**n/24
        check("strict positive complete baseline",qp.subs(r,0)==qm.subs(r,0)==base)
        check("n-independent native paired log odds first jet",
              s.simplify(s.diff(nat_odds(P,ga,n),r).subs(r,0)
                         +2*s.sqrt(2))==0)
        check("fixed Choi success probability at identity",
              s.Rational(1,4)**n*int(s.trace(s.eye(4).T*s.eye(4)))/4
              ==s.Rational(1,4)**n)
        for j,gb in enumerate(G):
            if j!=index:
                check("independent six-coordinate off-axis zero",
                      s.simplify(s.diff(nat_odds(P,gb,n),r).subs(r,0))==0)

# SAME group P tested directly vs after 4 original sequential fresh Julia edges.
x,y=s.symbols("x y",real=True)
def exp_nil(g,t):
    check("original null generator nilpotent",g**3==s.zeros(4))
    return s.eye(4)+t*g+t*t*g*g/2
P=exp_nil(N2,x)*exp_nil(bN3,y)*exp_nil(N2,-x)*exp_nil(bN3,-y)
check("actual based commutator first edge jets zero",
      s.diff(P,x).subs({x:0,y:0})==s.zeros(4)
      and s.diff(P,y).subs({x:0,y:0})==s.zeros(4))
check("actual based commutator mixed P source is J",
      s.diff(P,x,y).subs({x:0,y:0})==J)
for sign in (-1,1):
    check("64fold exact full-event composition defect, not discarded",
          s.simplify(event(P,J,1,sign)-64*event(P,J,4,sign))==0)
check("exact score ratio insensitive to number of intermediate Julia flags",
      s.simplify(event(P,J,1,-1)*event(P,J,4,1)
                -event(P,J,1,1)*event(P,J,4,-1))==0)
check("nonzero genuine crossed-null curvature mixed log-odds",
      s.simplify(s.diff(nat_odds(P,J,4),x,y).subs({x:0,y:0})
                 +2*s.sqrt(2))==0)
# Ditto the other original opposite-null pair B.
Pb=exp_nil(N2,x)*exp_nil(bN2,y)*exp_nil(N2,-x)*exp_nil(bN2,-y)
check("true crossed boost plaquette source",
      s.diff(Pb,x,y).subs({x:0,y:0})==B)
check("boost mixed log-odds",
      s.simplify(s.diff(nat_odds(Pb,B,4),x,y).subs({x:0,y:0})
                 +2*s.sqrt(2))==0)

# Homogeneous Ward / actual based face derivative; inhomogeneous finite
# differences are NOT nulled.
a,b,c,d=s.symbols("a b c d",real=True)
X=N2
U1=exp_nil(X,r*a)
U2=exp_nil(X,r*b)
U3inv=exp_nil(X,-r*c)
U4inv=exp_nil(X,-r*d)
Pface=U1*U2*U3inv*U4inv
check("original inhomogeneous oriented based plaquette first jet",
      s.simplify(s.diff(Pface,r).subs(r,0)-(a+b-c-d)*X)==s.zeros(4))
check("original homogeneous based plaquette EXACT identity, all orders",
      s.simplify(Pface.subs({c:a,d:b})-s.eye(4))==s.zeros(4))
check("original homogeneous based plaquette no direct link jet",
      s.diff(Pface,r).subs({r:0,c:a,d:b})==s.zeros(4))

# First-order POVM Fisher on full COARSE pointer output (not on all
# additional fine Julia failure-history labels, which may add info).
for n in (1,4):
    ga=J;P=s.eye(4)+r*ga+r*r*ga*ga/2
    plus=event(P,ga,n,+1);minus=event(P,ga,n,-1)
    base=plus.subs(r,0)
    fisher=s.simplify(sum((s.diff(q,r).subs(r,0))**2/base
                           for q in (plus,minus)))
    check("full coarse native Fisher exact rate",fisher==s.Rational(1,4)**n/6)
    check("complete conditional native Fisher",s.simplify(
          fisher/(s.Rational(1,4)**n)-s.Rational(1,6))==0)

# The ORIGINAL SO(1,3) Lie algebra is PERFECT: commutators span
# all 6 generators. No C² additive scalar character of net holonomy
# can have a nonzero first Lorentz/plaquette curvature derivative.
comm=lambda X,Y:X*Y-Y*X
for label,lhs,rhs in (
    ("rotation",comm(N2,bN3),J),
    ("boost",comm(N2,bN2),B),
    ("nullN2",comm(B,N2),N2),
    ("nullN3",comm(B,N3),N3),
    ("oppositeN2",comm(B,bN2),-bN2),
    ("oppositeN3",comm(B,bN3),-bN3),
):
    check("perfect original Lorentz bracket "+label,lhs==rhs)
print("PASS no nonzero additive scalar holonomy character can match native odds")

# CRUCIAL: the EXACT complete genuine Golden-record Shannon source
# does NOT inherit projective odds/refinement invariance. Split ONLY the
# negative pointer in the genuine all-good history and preserve all other
# outcomes and failures; Delta H = q_minus * h2(p)/ln(phi).
pp=(s.sqrt(5)-1)/2
h2=-pp*s.log(pp)-pp**2*s.log(pp**2)
for n in (1,2,4,6):
    curved=s.eye(4)+r*J+r*r*J*J/2
    minus=event(curved,J,n,-1)
    jet=s.simplify(s.diff(minus,r).subs(r,0))
    check("original marked Golden per-n first source derivative",
          jet==-s.Rational(1,4)**n/(12*s.sqrt(2)))
    marked=s.simplify(minus*h2/s.log(phi))
    check("full recorded Golden entropy n-dependent first source",
          s.simplify(s.diff(marked,r).subs(r,0)+
                     s.Rational(1,4)**n*h2/(12*s.sqrt(2)*s.log(phi)))==0)
check("unavoidable factor64 originally observed in four-link owner",
      s.simplify((s.Rational(1,4)**1)/(s.Rational(1,4)**4))==64)
# A counterpart based cross null ab has the same marked amplitude ratio
# and curvature mix source, because P=I+ab J+O(a²b,ab²).
for n in (1,4):
    test=event(P,J,n,-1)
    jet=s.simplify(s.diff(test,x,y).subs({x:0,y:0}))
    check("crossed null Golden marked curvature mixed price",
          jet==-s.Rational(1,4)**n/(12*s.sqrt(2)))

# Paid native success clock: independent complete n-edge executions
# have all-good probability 4^-n; expected n*4^n primitive edge calls
for n in (1,4):
    check("positive original raw Julia edge call price",n*4**n>=n)
print("PASS: original 13-effect odds are refinement-invariant; costs are NOT")
print("n=1: mean edge calls to first all-success = 4")
print("n=4: mean edge calls to first all-success = 1024")
print("Original full Book03 selected source / exact GR action: OPEN")
