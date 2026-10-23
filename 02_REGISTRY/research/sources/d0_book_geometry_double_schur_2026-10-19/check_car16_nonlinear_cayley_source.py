#!/usr/bin/env python3
"""NONLINEAR original G2/STAR finite curvature from SIX left marked-event scores.
Original CAR16 Golden marked probability; original Lorentz carrier.
Research representation only: not physical Book03/full128 action selection.
"""
import sympy as s
from itertools import combinations
I=s.eye(4); eta=s.diag(1,-1,-1,-1)
p=(s.sqrt(5)-1)/2
def E(i,j):
    z=s.zeros(4);z[i,j]=1;return z
K=[E(0,i)+E(i,0) for i in (1,2,3)]
J=[E(2,3)-E(3,2),E(3,1)-E(1,3),E(1,2)-E(2,1)]
lie=K+J
G=s.Matrix([[s.trace(X*Y) for Y in lie] for X in lie])
assert G==s.diag(2,2,2,-2,-2,-2)
assert all(X.T*eta+eta*X==s.zeros(4) for X in lie)
cay=lambda X,t:(I+t*X)*(I-t*X).inv()
P=cay(K[0],s.Rational(1,20))*cay(J[0],s.Rational(1,30))*cay(K[1],s.Rational(1,25))
assert P.T*eta*P==eta and P.det()==1
assert (P+I).det()!=0
C=(P-I)*(P+I).inv()
M=(I-C*C).inv()
F=(P-P.inv())/2
assert C.T*eta+eta*C==s.zeros(4)
assert M.T*eta==eta*M
assert F==2*C*M
mark=lambda U:p*p*s.det(I+U)**2/256
assert s.simplify(mark(P)-mark(P.inv()))==0
z=s.symbols('z')
scores=[]
for X in lie:
    dl=s.diff(s.log(mark((I+z*X)*P)),z).subs(z,0)
    assert s.simplify(dl-s.trace(X*C))==0
    scores.append(s.trace(X*C))
assert sum((v*X for v,X in zip(G.inv()*s.Matrix(scores),lie)),s.zeros(4))==C
area=list(combinations(range(4),2))
idx={pair:i for i,pair in enumerate(area)}
G2=s.diag(*(eta[i,i]*eta[j,j] for i,j in area))
STAR=s.zeros(6)
smap={(0,1):((2,3),-1),(0,2):((1,3),1),(0,3):((1,2),-1),
      (1,2):((0,3),1),(1,3):((0,2),-1),(2,3):((0,1),1)}
for a,(b,v) in smap.items():STAR[idx[b],idx[a]]=v
assert STAR*STAR==-s.eye(6)
def XB(B):
    low=eta*B*eta
    H=s.Matrix(4,4,lambda a,b:sum(s.LeviCivita(a,b,i,j)*low[i,j]
                                  for i in range(4) for j in range(4))/2)
    return H*eta
def bF(Y):return s.Matrix([(Y*eta)[i,j] for i,j in area])
for Y in lie:
    Q=cay(Y,s.Rational(1,13))
    CQ=(Q-I)*(Q+I).inv();MQ=(I-CQ*CQ).inv()
    FQ=(Q-Q.inv())/2
    assert FQ==2*CQ*MQ
    for ab in area:
        B=E(*ab)-E(ab[1],ab[0]); X=XB(B)
        w=s.zeros(6,1);w[idx[ab]]=1
        original=(w.T*G2*STAR*bF(FQ))[0]
        Xtilde=(X*MQ+MQ*X)/2
        assert Xtilde.T*eta+eta*Xtilde==s.zeros(4)
        assert s.simplify(original+s.trace(Xtilde*CQ))==0
# KILL 1: marked value cannot produce original signed star at finite curvature.
t=s.symbols('t',real=True); R=cay(J[0],t)
B=E(0,1)-E(1,0); X=XB(B)
assert s.simplify(mark(R)-p*p/(1+t*t)**2)==0
assert s.simplify(-s.trace(X*(R-R.inv())/2)/2-2*t/(1+t*t))==0
assert s.simplify(mark(R)-mark(R.inv()))==0
# KILL 2: one marked event on serial holonomy is not multiplicative.
R=I+s.Rational(4,5)*J[0]+s.Rational(2,5)*J[0]**2
assert s.simplify(mark(R)-s.Rational(16,25)*p*p)==0
assert s.simplify(mark(R*R)-s.Rational(81,625)*p*p)==0
assert s.simplify(mark(R*R)/(mark(R)*mark(R)/p**2)-s.Rational(81,256))==0
print('PASS original full nonlinear Cayley curvature recovered from SIX positive marked-event LEFT scores')
print('PASS all 36 literal G2/STAR finite-curvature controls, exact rational')
print('PASS G0 kill: single marked-value even under inverse, nonmultiplicative for serial path (81/256)')
print('FIREWALL: original physically selected full128/Book03 action remains unproved; GR_closed=false')
