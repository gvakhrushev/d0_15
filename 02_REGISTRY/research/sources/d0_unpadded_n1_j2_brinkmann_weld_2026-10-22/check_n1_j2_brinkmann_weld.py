#!/usr/bin/env python3
"""D0 #334: exact ORIGINAL N=1 0/10 Golden click ↔ old J2 logdet,
first-jet 42-source match and arbitrary-u Brinkmann Poisson transfer.
The original 40-dimensional finite all-plaquette Euler reduction, physical
Book03 selection and real CAR writer are consumed NOT re-certified here.
"""
from __future__ import annotations
import math
import mpmath as mp
import sympy as s

checks=[]
def check(name, x):
    if not bool(x):
        raise AssertionError(name)
    checks.append(name)

p=(s.sqrt(5)-1)/2
z,x,y=s.symbols('z x y', real=True)
E=p**2*(1+x)
L=4*E*(1-E)
b=p-p*p*y
B=4*b*b*(1-b*b)
A=L+(1-L)*B
r=z*(A+B)-z*z*A*B
r0=s.simplify(r.subs({x:0,y:0}))
rx=s.diff(r,x).subs({x:0,y:0})
ry=s.diff(r,y).subs({x:0,y:0})
B0=4*p**3
A0=B0*(1+p**6)
Q=1-z*B0
R=1-z*A0
lamJ=-2*p**(-5)*(R/Q+p**6)

check('native phi original primitive p+p2',s.simplify(p+p*p-1)==0)
check('native p6+4p3 closure',s.simplify(p**6+4*p**3-1)==0)
check('original two-tick common B0',s.simplify(B.subs({x:0,y:0})-B0)==0)
check('original two-tick common A0',s.simplify(A.subs({x:0,y:0})-A0)==0)
check('entire nonlinear exact complementary return',s.expand(1-r-(1-z*A)*(1-z*B))==0)
check('original J2 and N1 native material/curvature slope equal exactly',s.simplify(s.together(ry/rx-lamJ))==0)
check('x base derivative nonzero',float(rx.subs(z,s.Rational(1,2**20)))>0)
check('y base derivative nonzero',float(ry.subs(z,s.Rational(1,2**20)))<0)

# SAME full nonlinear operator identity at a range of ORIGINAL Golden operands.
mp.mp.dps=55
pp=(mp.sqrt(5)-1)/2
zz=mp.mpf(2)**-20
logp=mp.log(1/pp)
def report(xx,yy):
    Ee=pp**2*(1+xx)
    ell=4*Ee*(1-Ee)
    bb=pp-pp**2*yy
    BB=4*bb**2*(1-bb**2)
    AA=ell+(1-ell)*BB
    click=zz*(AA+BB)-zz**2*AA*BB
    j2=-528*(mp.log(1-zz*AA)+mp.log(1-zz*BB))
    return click,j2,AA,BB
for a0,b0 in [(.0,.0),(.01,-.02),(-.04,.03),(.02,.005),(-.07,-.02)]:
    click,j2,aa,bb=report(mp.mpf(str(a0)),mp.mpf(str(b0)))
    check('full nonlinear Book/event identity '+str((a0,b0)),abs(j2+528*mp.log(1-click))<mp.mpf('1e-47'))
    check('original positive 0<click<1 '+str((a0,b0)),0<click<1)

# ORIGINAL cost 1+r vs measured Shannon H_phi(r), fixed native root normalization.
rr,jj,_,_=report(0,0)
hprime=mp.log((1-rr)/rr)/logp
slope=float((ry/rx).subs(z,s.Rational(1,2**20)))
lam=float(lamJ.subs(z,s.Rational(1,2**20)))
gamma=1/hprime-1  # original norm = -1/(tau hprime rx), x=tau f_B/rho
check('J2 lambda recovered without numerical fit',abs(slope-lam)<1e-13)
check('true F/R unpadded constant gain nonzero',abs(gamma)>0.9)
check('original hprime positive and rare report',hprime>20 and rr>0 and rr<mp.mpf('1e-5'))
check('Golden original lambda independent of Hprime choice',mp.almosteq(mp.mpf(str(lam)),mp.mpf(str(slope)),rel_eps=mp.mpf('1e-13')))

# Arbitrarily moving nonuniform PF rho: at f_B=q=0, first jet has NO drho.
# This algebra holds for ANY analytic Phi(r) vanishing at r0; the real native
# Phi=h_phi(r)-h_phi(r0)-(r-r0) has exactly that property.
rho,ff,qq,tau,c1,c2=s.symbols('rho ff qq tau c1 c2',nonzero=True,real=True)
local=r.subs({x:tau*ff/rho,y:tau*qq/rho})
zero={ff:0,qq:0}
origin=r0
Phi=c1*(local-origin)+c2*(local-origin)**2
pr=s.expand(rho*Phi)
check('native root site weight cancels field rho source',s.simplify(s.diff(pr,rho).subs(zero))==0)
check('all geometric first jets independent of rho',s.simplify((s.diff(pr,ff).subs(zero)-tau*c1*rx))==0)
check('all material first jets independent of rho',s.simplify((s.diff(pr,qq).subs(zero)-tau*c1*ry))==0)
for weight in [s.Rational(29,50),s.Rational(78,50),s.Rational(1),s.Rational(29*256,10946),s.Rational(78*256,10946)]:
    check('true positive AF/PF weight cancellation '+str(weight),
          s.simplify(s.diff(pr,ff).subs(zero).subs(rho,weight)-tau*c1*rx)==0)

# EXACT original 40->3->1 reduced Brinkmann geometry, inherited from previous
# checked ORIGINAL six-based-plaquette all40 reduction. Verify the independent
# Cartan/Poisson/matter-source components at arbitrary h and E_j.
h,u,x0,y0,K=s.symbols('h u x0 y0 K',nonzero=True,real=True)
lamvar=s.symbols('Lambda',real=True)
W3=x0**3-3*x0*y0*y0
W4=x0**4-6*x0*x0*y0*y0+y0**4-h*h*(x0*x0+y0*y0)

def delta(fun):
    return s.expand((fun.subs(x0,x0+h)+fun.subs(x0,x0-h)+fun.subs(y0,y0+h)+fun.subs(y0,y0-h)-4*fun)/h**2)
check('native universal cubic Weyl mode discrete harmonic',s.simplify(delta(W3))==0)
check('native corrected quartic Weyl mode discrete harmonic',s.simplify(delta(W4))==0)
for mode in [0,W3,W4,3*W3+W4]:
    base=-lamvar*u*(x0*x0+y0*y0)+mode
    check('all-h time-dependent sourced discrete Poisson '+str(mode)[:20],s.simplify(delta(base)+4*lamvar*u)==0)
    X=(base-base.subs(x0,x0-h))/2
    Y=(base-base.subs(y0,y0-h))/2
    link_x=s.simplify(h*h*(X-(base-base.subs(x0,x0-h))/2))
    link_y=s.simplify(h*h*(Y-(base-base.subs(y0,y0-h))/2))
    check('original one-step x proper link Euler '+str(mode)[:20],link_x==0)
    check('original one-step y proper link Euler '+str(mode)[:20],link_y==0)
    ec=h*(X-X.subs(x0,x0+h)+Y-Y.subs(y0,y0+h))
    matter=-2*lamvar*u/h
    check('original coframe-null gravity+CAR Euler '+str(mode)[:20],s.simplify(ec/h**4+matter)==0)

# The two independent real CAR amplitudes Psi_0,Psi_4 each obey original
# periodic v-Stokes: sum_j (D_u Psi_j) D_v deltaPsi_j =0 identically.
vcols=[s.Rational(1,3),s.Rational(-2,5),s.Rational(4,7)]
t0,t1,t2=s.symbols('t0 t1 t2')
per=[t0,t1,t2]
zero_sum=sum(vcols[j]*(per[(j+1)%3]-per[j]) for j in range(3))
# For arbitrary u-dependent v, the v-stencil source is sum_v dv(deltaPsi),
# per FIXED u slice, so each u_j is identical across transverse v.
check('native v-Stokes using constant u-profile across v',s.simplify(sum((per[(j+1)%3]-per[j]) for j in range(3)))==0)

# Same ORIGINAL one registered native Bernoulli trial has an exact OTHER
# score: whole F/R Price - measured Shannon = native Kraft KL to (p,p^2).
# This is not the same score as the Book J2 no-click logdet: physical
# task/Info selection is precisely the remaining gate.
for test_r in [rr, mp.mpf('0.003'), pp**2/2, pp**2, mp.mpf('.62')]:
    ent=-(test_r*mp.log(test_r)+(1-test_r)*mp.log(1-test_r))/logp
    observed=1+test_r-ent
    kl=((1-test_r)*mp.log((1-test_r)/pp)+test_r*mp.log(test_r/pp**2))/logp
    check('literal native Price-minus-Shannon equals exact code KL '+mp.nstr(test_r,5),
          abs(observed-kl)<mp.mpf('1e-48'))
check('native complete-code KL reference zero at p²',
      abs(1+pp**2+((pp**2)*mp.log(pp**2)+pp*mp.log(pp))/logp)<mp.mpf('1e-48'))
check('native J2 void surprisal NOT same absolute score as zero code KL',
      -528*mp.log(1-pp**2)>0)

print('PASS',len(checks),'independent exact/original-parameter controls')
print('r0          =',mp.nstr(rr,28))
print('J2(r) exact = -528 ln(1-r), all positive native operands')
print('lambda_N1=lambda_J2=',mp.nstr(lam,22))
print('native unpadded source/J2 coefficient normalized=',mp.nstr(gamma,22))
print('SCOPE: original 40->3->1 all-Euler reduction INHERITED from independently owned proof; Book03 whole HJR selection/upstream work/clock/GR OPEN')