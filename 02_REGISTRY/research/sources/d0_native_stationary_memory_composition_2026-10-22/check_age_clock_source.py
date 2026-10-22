#!/usr/bin/env python3
"""Actual native age-entropy spectral check, with analytic derivatives.

The exact original CAR16 spectral fixture is consumed from the pinned
Ward owner in PROVENANCE.json. Decimal numbers are nominal evaluations;
strict bounds are proved by check_age_clock_rational_bound.py.
The thermal/feedback expressions are declared candidates, not a selected
full physical Book03 action. No original full128 matrix replay is claimed.
"""
from decimal import Decimal as D, getcontext
getcontext().prec = 80
p=(D(5).sqrt()-1)/2
t=2*p*p
zeta=D(2)**-20
mu=D(141489)/10240000
h=D(69399)/5030720
mur=-D(328779)/204800000
hr=-D(20040939)/9885993640

def at(dm, dh):
    e=(mu*(mu-h)).sqrt()
    de=((2*mu-h)*dm-mu*dh)/(2*e)
    ls=[mu-e,mu+e]
    dl=[dm-de,dm+de]
    w=[(mu+e)/(2*mu),(mu-e)/(2*mu)]
    dw=[(de*mu-e*dm)/(2*mu*mu),-(de*mu-e*dm)/(2*mu*mu)]
    ss=[(1-t*l)**2 for l in ls]
    ds=[-2*t*(1-t*l)*v for l,v in zip(ls,dl)]
    hg=lambda s:-(1-s).ln()-s*s.ln()/(1-s)
    hp=lambda s:-s.ln()/(1-s)**2
    Ia=sum(a*hg(s) for a,s in zip(w,ss))
    dIa=sum(da*hg(s)+a*hp(s)*v for a,da,s,v in zip(w,dw,ss,ds))
    Sr=D(8).ln()-sum(a*a.ln() for a in w)
    dSr=-sum(da*a.ln() for a,da in zip(w,dw))
    J=-1024*sum((1-zeta+zeta*s*s).ln() for s in ss)
    dJ=-1024*sum(2*zeta*s*v/(1-zeta+zeta*s*s) for s,v in zip(ss,ds))
    H=(16/h/(2*t)).ln()/t
    dH=-dh/(t*h)
    return dict(I_age=Ia,dI_age=dIa,Srho=Sr,dSrho=dSr,Sjoint=Sr+Ia,
                dSjoint=dSr+dIa,J2=J,dJ2=dJ,H_age=H,dH_age=dH,
                candidate_old_modular_source=dSr/t+dJ,
                candidate_age_entropy_source=(dSr+dIa)/t+dJ,
                candidate_bare_age_heat_source=dH+dJ)

for name,dm,dh in [('proper_boost',mur,hr),('one_port_null',mur-mu*hr/h,D(0))]:
    print(name)
    for key,value in at(dm,dh).items():
        print(key,format(value,'.45g'))

# Exact-spectral, normalized stationary age partition at a finite cap.
e=(mu*(mu-h)).sqrt()
ls=[mu-e,mu+e]
weights=[(mu+e)/(2*mu),(mu-e)/(2*mu)]
for cap in [1,2,9,100]:
    for l,w in zip(ls,weights):
        s=(1-t*l)**2
        probs=[(1-s)*s**n for n in range(cap)]+[s**cap]
        assert abs(sum(probs)-1)<D('1e-75')
        H=-sum(q*q.ln() for q in probs)
        hg=-(1-s).ln()-s*s.ln()/(1-s)
        assert abs(H-(1-s**cap)*hg)<D('1e-72')
print('finite_age_partition_and_entropy_identity=PASS')

from fractions import Fraction as F
r=F(49,50); cap=4096
assert 6*r**cap < F(7,10**36)
assert (8+F(3,25)*cap/r)*r**cap < F(6,10**34)
assert r**cap < F(201248,10**7)
print('K4096_exact_rational_value_and_source_tail_bounds=PASS')

for l in ls:
    b=1-t*l; s=b*b; cap=4096
    # Sum all resolved finite heat Boltzmann blocks plus the genuine tail.
    zfinite=(1+b)/2*(1-s**cap)/(1-s)+s**cap/(2*(1-b))
    assert abs(zfinite-1/(2*(1-b)))<D('1e-70')
    tail_heat=(-2*cap*b.ln()+(2*(1-b)).ln())/t
    assert tail_heat>0
print('K4096_exact_finite_clock_Gibbs_tail_positive=PASS')
