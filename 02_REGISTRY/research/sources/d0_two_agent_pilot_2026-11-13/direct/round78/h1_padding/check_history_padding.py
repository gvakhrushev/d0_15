"""History-dependent equalization and the primary two-component H.1 comparison."""
from fractions import Fraction as Q
from itertools import product
from math import isqrt

import sympy as sp


def primary_level():
    p=(sp.sqrt(5)-1)/2
    phi=1/p
    s,k,eps,t=sp.symbols("s k eps t", positive=True)
    f=4*s**2*(1+2*s**2-s**4)/(1+s**2)**4
    base=f.subs(s,sp.Rational(1,4))
    assert base == sp.Rational(18368,83521)
    assert f.diff(s).subs(s,sp.Rational(1,4)) == sp.Rational(2171392,1419857)
    # V=(1,-1) in the two physical f coordinates. Both are realized near base.
    A,B=base+t,base-t
    Kphi=sp.symbols("Kphi",positive=True)
    result=k*(eps*(A+B)-phi*eps**2*(A**2/p+B**2/(1-p)))
    Dold=sp.simplify(5644800*p**36*result.diff(t).subs(t,0))
    assert sp.simplify(Dold-5644800*p**36*2*k*phi*eps**2*base)==0
    assert sp.diff(Kphi*(A+B),t)==0
    for j_is_1,out in product((False,True),repeat=2):
        w=int(j_is_1 and out)
        assert w+(1-w)==1
        # One paid 0/10 decision in each history; parsed length is 2-w.
        assert w+len(("0","10")[1-w])==2
    print("genuine raw J=1,B=1 excess has positive derivative on fixed Q;",
          "exact supplemented costs 1 or 2 in the two schedules")


def correlated_history(m):
    mu=Q(2,5)
    mass=Q(0)
    fisher=Q(0)
    conditional_sum=Q(0)
    derivative=sp.S.Zero
    mean=sp.S.Zero
    differentiated_mass=Q(0)
    for path in product(range(2),repeat=m):
        prob=Q(1)
        score=Q(0)
        conditional_info=Q(0)
        previous=0
        singles=double=0
        for j,z in enumerate(path):
            chance=mu if j==0 else (mu+previous)/2
            slope=Q(1) if j==0 else Q(1,2)
            conditional_info+=slope**2/(chance*(1-chance))
            prob*=chance if z else 1-chance
            score+=slope/chance if z else -slope/(1-chance)
            singles+=z
            double+=z*previous
            previous=z
        # W = sqrt(2) for each 1 and another 1/3 for each successive 11.
        # K=2, c=1. Ceil(2m-W) is computed by integer square root only.
        floor_w=(double+isqrt(18*singles*singles))//3
        extra=2*m-floor_w
        w=singles*sp.sqrt(2)+sp.Rational(double,3)
        residual=w+extra-2*m
        assert extra>=0 and residual>=0 and residual<1
        mass+=prob
        differentiated_mass+=prob*score
        mean+=prob*residual/m
        derivative+=prob*score*residual/m
        fisher+=prob*score**2
        conditional_sum+=prob*conditional_info
    assert mass==1 and differentiated_mass==0 and fisher==conditional_sum
    assert sp.simplify(mean)>=0 and sp.simplify(sp.Rational(1,m)-mean)>0
    assert sp.simplify(fisher/(4*m*m)-derivative**2)>0
    print("m",m,"mean excess per history",float(mean),"derivative",float(derivative),
          "score bound",float(sp.sqrt(fisher)/(2*m)))


if __name__=="__main__":
    primary_level()
    for length in (1,3,7):
        correlated_history(length)
