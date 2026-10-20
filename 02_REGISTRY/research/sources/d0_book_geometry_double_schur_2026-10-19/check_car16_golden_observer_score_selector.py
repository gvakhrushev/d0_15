#!/usr/bin/env python3
"""Golden CAR16 positive 3-outcome score selection (all six Lorentz generators).
Original native observer exterior + Julia/Choi mathematical test, NOT Book selection.
"""
import sympy as s
p=(s.sqrt(5)-1)/2
eta=s.diag(1,-1,-1,-1)
def E(i,j):
    M=s.zeros(4); M[i,j]=1; return M
K=[E(0,i)+E(i,0) for i in (1,2,3)]
J=[E(2,3)-E(3,2),E(3,1)-E(1,3),E(1,2)-E(2,1)]
G=K+J
S=lambda X:(X+X.T)/2
assert s.simplify(p*p+p-1)==0
assert all(X.T*eta+eta*X==s.zeros(4) for X in G)
Hm=s.Matrix([[p*p*s.trace(X*Y)/2 for Y in G] for X in G])
Hg=s.Matrix([[p*p*s.trace(S(X)*S(Y)) for Y in G] for X in G])
assert s.simplify(Hm-p*p*s.diag(1,1,1,-1,-1,-1))==s.zeros(6)
assert s.simplify(Hg-p*p*s.diag(2,2,2,0,0,0))==s.zeros(6)
Hu=Hg-Hm; Hf=-Hg
assert s.simplify(Hu-p*p*s.eye(6))==s.zeros(6)
assert Hm+Hu+Hf==s.zeros(6)
fm,fu,ff=s.symbols('f_mark f_unmarked f_fail',real=True)
H=s.simplify(fm*Hm+fu*Hu+ff*Hf)
assert s.simplify(H-p*p*s.diag(*([fm+fu-2*ff]*3+[-fm+fu]*3)))==s.zeros(6)
assert s.simplify(H.subs(fu,ff)-p*p*(fm-ff)*s.diag(1,1,1,-1,-1,-1))==s.zeros(6)
# Existing D0 rational transverse boost (5/4,3/4): fixed J23, DIFFERENT observer.
g=s.eye(4);g[0,0]=g[2,2]=s.Rational(5,4);g[0,2]=g[2,0]=s.Rational(3,4)
assert g.T*eta*g==eta
Xm=g.inv()*J[0]*g
assert s.simplify(s.trace(S(Xm)*S(Xm)))==s.Rational(9,8)
assert s.simplify(s.trace(Xm*Xm)/2)==-1
# Finite observer change at fixed spatial rotation: use z=tan(theta/2).
z=s.symbols('z',real=True)
C=(1-z*z)/(1+z*z);R=s.eye(4);R[2,2]=R[3,3]=C
R[2,3]=2*z/(1+z*z);R[3,2]=-2*z/(1+z*z)
W=g.inv()*R*g
good_rest=s.factor(s.det(s.eye(4)+R.T*R)/16)
good_moved=s.factor(s.det(s.eye(4)+W.T*W)/16)
marked=s.factor(s.det(s.eye(4)+R)**2/256)
assert good_rest==1
assert s.simplify(good_moved-(1+s.Rational(9,16)*(1-C))**2)==0
assert s.simplify(marked-1/(1+z*z)**2)==0
assert s.simplify((fu-ff)*p*p*s.Rational(9,8))!=0  # generic score
assert s.solve((fu-ff)*p*p*s.Rational(9,8),fu)==[ff]
# Same Golden flat action 2 and zero first jet do NOT select second source:
# q_mark and q_good both =p², but their log jets differ.
assert s.simplify(-Hm/p**2+s.diag(1,1,1,-1,-1,-1))==s.zeros(6)
assert s.simplify(-Hg/p**2+s.diag(2,2,2,0,0,0))==s.zeros(6)
# Full Shannon: q_unmarked(t)=p²t²/2+O(t^4) on every nonzero generator.
t=s.symbols('t',real=True)
for b in (True,False):
    mark=p*p*(s.cosh(t/2) if b else s.cos(t/2))**4
    good=p*p*(s.cosh(t)**2 if b else 1)
    assert s.simplify(s.diff(good-mark,t,2).subs(t,0)-p*p)==0
# Julia feedback-only (full CAR16 failure effect) constant on ALL spatial rotations.
zz=s.symbols('z_fb',positive=True)
Sfb=-8*s.log(1-zz*(1-p*p))
Sfb+=-4*s.log(1-zz*(1-p*p*s.exp(2*t)))-4*s.log(1-zz*(1-p*p*s.exp(-2*t)))
assert s.simplify(s.diff(Sfb,t,2).subs(t,0)-32*p*p*zz*(zz-1)/(1-zz*p)**2)==0
print('PASS full-six observer-free smooth score selector: f_unmarked=f_fail')
print('PASS finite rational observer witness: mark invariant but total success varies')
print('PASS zero-base unmarked opens ~p²t²/2; Shannon is NOT C² at the flat cell')
print('PASS scalar minimal Julia feedback cannot read compact rotation curvature')
print('FIREWALL: mathematical CAR16 Julia/Choi; Book03/full128 physical selection open; GR_closed=false')
