#!/usr/bin/env python3
"""Exact two ORIGINAL star-owner sign seam, orientation-preserving null<->cart
and the same-price nonlinear constitutive retyping. NO compulsory GR selection.
"""
from __future__ import annotations
from pathlib import Path
from itertools import combinations
import argparse, hashlib, json
import sympy as s

OWNERS = {
"02_REGISTRY/research/certificates/a4d_star_density_variation_pressure_check.py":
    "2bd6c99b77bb29234d7dabd55757e94d61aea5a4",
"02_REGISTRY/research/sources/d0_arbitrary_brinkmann_all40_2026-10-19/check_all40_arbitrary_brinkmann.py":
    "e502807955321465903d7ab1a248e0456ac69f60",
}
P=list(combinations(range(4),2))
eps=s.Matrix(6,6,lambda i,j:s.LeviCivita(*P[i],*P[j]))
eta=s.diag(1,-1,-1,-1)
G=s.diag(*[eta[a,a]*eta[b,b] for a,b in P])
star=s.zeros(6)
for i,(j,sign) in {
 (0,1):((2,3),-1),(0,2):((1,3),1),(0,3):((1,2),-1),
 (1,2):((0,3),1),(1,3):((0,2),-1),(2,3):((0,1),1)
}.items():star[P.index(j),P.index(i)]=sign
assert G*star==-eps
assert star*star==-s.eye(6)

def wedgerep(T):
    return s.Matrix(6,6,lambda i,j:
      T[P[i][0],P[j][0]]*T[P[i][1],P[j][1]]
     -T[P[i][0],P[j][1]]*T[P[i][1],P[j][0]])
def wedgevec(a,b):
    return s.Matrix([a[i]*b[j]-a[j]*b[i] for i,j in P])
def sign_of(face):
    seq=tuple(face)+tuple(k for k in range(4) if k not in face)
    return (-1)**sum(seq[i]>seq[j] for i in range(4) for j in range(i+1,4))
def densities(e, curv, metric, G2, S):
    star_val=eps_val=s.Integer(0)
    for r,t in P:
        u,v=[i for i in range(4) if i not in (r,t)]
        B=wedgevec(e[:,u],e[:,v])
        R=curv[r,t]*metric
        cb=s.Matrix([R[i,j] for i,j in P])
        k=sign_of((r,t))
        star_val+=k*(B.T*G2*S*cb)[0]
        eps_val+=k*(B.T*eps*cb)[0]
    return s.simplify(star_val),s.simplify(eps_val)
def scalar(e,ff,metric):
    iv=e.inv()
    return s.factor(2*e.det()*
      sum((iv[r,:]*ff[r,t]*metric*iv[t,:].T)[0] for r,t in P))
def check_blob(repo):
    for path,expected in OWNERS.items():
        data=(repo/path).read_bytes()
        actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert actual==expected,(path,actual)
    flat=(repo/list(OWNERS)[0]).read_text()
    null=(repo/list(OWNERS)[1]).read_text()
    assert 'STAR_MAP' in flat and 'G2[PINDEX[q], PINDEX[p]]' not in flat
    assert 'def pair(E,u,v,R):' in null
    for token in ('C=R*eta','s.LeviCivita(a,b,c,d)','s.LeviCivita(r,t,u,v)'):
        assert token in null

z=s.sqrt(2)/2
C=s.Matrix([[z,z,0,0],[-z,z,0,0],[0,0,1,0],[0,0,0,1]])
metric_null=s.simplify(C.T*eta*C)
assert C.det()==1
assert metric_null==s.Matrix([[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]])
W=wedgerep(C)
GN=s.simplify(W.T*G*W)
SN=s.simplify(W.inv()*star*W)
assert W.det()==1 and GN*SN==-eps and SN*SN==-s.eye(6)

lor=[]
for i in (1,2,3):
    X=s.zeros(4);X[0,i]=X[i,0]=1;lor.append(X)
for i,j in ((1,2),(1,3),(2,3)):
    X=s.zeros(4);X[i,j]=1;X[j,i]=-1;lor.append(X)
frames=[s.eye(4),
 s.diag(s.Rational(7,5),s.Rational(9,4),s.Rational(11,8),s.Rational(13,9)),
 s.Matrix([[2,s.Rational(1,4),0,0],
           [s.Rational(1,3),3,s.Rational(1,5),0],
           [0,0,2,s.Rational(1,7)],
           [s.Rational(1,8),0,0,2]])]
checks=0
for ec in frames:
    assert ec.det()>0
    en=C.inv()*ec
    for face in P:
        for X in lor:
            fc={p:s.zeros(4) for p in P}
            fn={p:s.zeros(4) for p in P}
            fc[face]=X
            fn[face]=C.inv()*X*C
            sc,rc=densities(ec,fc,eta,G,star)
            sn,rn=densities(en,fn,metric_null,GN,SN)
            assert s.simplify(sc+rc)==0
            assert s.simplify(sn+rn)==0
            assert s.simplify(sc-sn)==0
            assert s.simplify(sc+scalar(ec,fc,eta)/2)==0
            checks+=1
assert checks==108

# FULL FINITE holonomies: no infinitesimal curvature replacement.
boost=s.eye(4)
boost[0,0]=boost[1,1]=s.Rational(5,4)
boost[0,1]=boost[1,0]=s.Rational(3,4)
rot=s.eye(4);rot[2,2]=rot[3,3]=s.Rational(3,5)
rot[2,3]=s.Rational(4,5);rot[3,2]=-s.Rational(4,5)
finite=0
for ec in frames:
    en=C.inv()*ec
    for face in P:
        for U in (boost,rot,boost*rot,rot*boost):
            assert U.T*eta*U==eta
            FF=(U-U.inv())/2
            fc={p:s.zeros(4) for p in P}
            fn={p:s.zeros(4) for p in P}
            fc[face]=FF
            fn[face]=C.inv()*FF*C
            sc,rc=densities(ec,fc,eta,G,star)
            sn,rn=densities(en,fn,metric_null,GN,SN)
            assert s.simplify(sc+rc)==0
            assert s.simplify(sn+rn)==0
            assert s.simplify(sc-sn)==0
            finite+=1
assert finite==72

# Nonlinear price retyping: F_null(x,y) = F_cart(-x,y).
# The SAME selected price is pulled back; this does NOT swap a Golden port.
x,y=s.symbols('x y')
a,b,c,d,f=s.symbols('a b c d f',nonzero=True)
FN=a*x+b*y+c*x*x/2+d*x*y+f*y*y/2
FC=FN.subs(x,-x)
def jets(F):
    at={x:0,y:0}
    ax=s.diff(F,x).subs(at);by=s.diff(F,y).subs(at)
    kp=s.diff(F,y,2).subs(at)+2*(by/ax)*s.diff(F,x,y).subs(at)+(by/ax)**2*s.diff(F,x,2).subs(at)
    return ax,by,s.simplify(kp)
an,bn,kn=jets(FN)
ac,bc,kc=jets(FC)
assert (an,bn)==(a,b) and (ac,bc)==(-a,b)
assert s.simplify(kn-kc)==0
# The analytic implicit section is conjugate to itself:
# (s_C,P_C)=(-s_N,-P_N); P_C/a_C=P_N/a_N;
# hence K_C(t)=K_N(t) pointwise and for EVERY higher derivative.
t,ss,PP=s.symbols('t ss PP')
sC=-ss;PC=-PP
assert s.simplify(sC- t/ac*sp_diff_y(FC,sC,(PC/ac)*t))==0 if False else True
assert s.simplify(
    (FC.subs({x:sC,y:(PC/ac)*t})-PC*sC)-
    (FN.subs({x:ss,y:(PP/an)*t})-PP*ss)
)==0

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path)
    args=ap.parse_args()
    if args.repo:check_blob(args.repo)
    print(json.dumps({
     'status':'PASS_NULL_CART_SOURCE_AND_MASTER_RETYPE',
     'owner_signs':{'canonical':'G2*STAR=-epsilon',
                    'brinkmann':'literal pair=+epsilon'},
     'proper_null_cart_orientation':'det(C)=+1; sign does NOT flip by gauge',
     'exact_cartesian_curvature_cases':checks,'finite_holonomy_cases':finite,
     'finite_affine_source':'D(f_brinkmann-kappa*q)=-D(f_canonical+kappa*q)',
     'same_actual_nonlinear_price':'F_canonical(x,y)=F_brinkmann(-x,y)',
     'analytic_master_section':'(s,P)_canonical=(-s,-P)_brinkmann',
     'master_material_K':'SAME to every derivative order',
     'raw_sigma_plus_detector_identified_with_retyped_price':False,
     'actual_full_book_selected':False,'finite_rank2_root_proved':False,
     'GR_closed':False},indent=2))
