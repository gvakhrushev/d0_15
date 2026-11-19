"""Finite Golden-scale comparison on SC1/SC4/SC7. All bounds are rational."""
from collections import Counter
from fractions import Fraction as F
import json

from check_extra_work import Span, span


def require(test, label):
    if not test:
        raise ArithmeticError(label)


P = (span(5).sqrt()-1)/2
PHI2 = 1/P**2
Z = F(1, 2**20)
L = 4*P**2*(1-P**2)


def reporter_y(t):
    """r_y(0,-t)/z and its first two t derivatives from SC1."""
    u = P - P**2*t
    b = 4*u**2*(1-u**2)
    by = 8*P**2*u*(1-2*u**2)
    byy = 8*P**4*(1-6*u**2)
    byyy = -96*P**6*u
    d = Z*(1-L)
    prefactor = 2-L-Z*L-2*d*b
    return (prefactor*by, -prefactor*byy+2*d*by**2,
            prefactor*byyy-6*d*by*byy)


def sc1_over_z(x, y):
    e = P**2*(1+x)
    local_l = 4*e*(1-e)
    u = P+P**2*y
    b = 4*u**2*(1-u**2)
    a = local_l+(1-local_l)*b
    return a+b-Z*a*b


def close_enclosure(a, b):
    return max(a.lo,b.lo) <= min(a.hi,b.hi)


def verify_reporter():
    domain = Span(0,F(1,1024))
    u, up, upp = reporter_y(domain)
    elasticity_derivative = up/u+domain*(upp/u-(up/u)**2)
    require(u.lo>0 and up.lo>0 and elasticity_derivative.lo>3,
            "positive reporter, increasing tail and uniformly increasing logarithmic elasticity")
    rest = 4*P**2*(1-P**2)
    rx_over_z = 4*P**2*(1-2*P**2)*(1-rest)*(1-Z*rest)
    k0 = reporter_y(span(0))[0]/rx_over_z
    require(k0.lo>23 and k0.hi<24,"full original matter coefficient")
    # The input reporter on x=0 has degree at most eight. Recover its exact
    # derivative by Lagrange differentiation on nine central nodes, independently
    # of reporter_y's derivative formula. Sample three points in the interval.
    from math import factorial
    weights = []
    for j in range(-4,5):
        if j == 0:
            weights.append(F(0))
        else:
            weights.append(F((-1)**(abs(j)+1)*factorial(4)**2,
                             j*factorial(4-j)*factorial(4+j)))
    for target in (span(0),span(F(1,2048)),span(F(1,1024))):
        step = F(1,4096)
        diff = sum((w*sc1_over_z(0,-target+j*step)/step
                    for j,w in zip(range(-4,5),weights)),span(0))
        require(close_enclosure(diff,reporter_y(target)[0]),"independent exact SC1 differentiation")
    return k0, elasticity_derivative


def check_lattice(b, c):
    h=F(1,4)
    psi=(0,h*b,0,h*c)
    time_d = [(psi[(n+1)%4]-psi[n])/h for n in range(4)]
    require(time_d==[b,-b,c,-c],"periodic forward differences including wrap")
    weights=Counter(d*d for d in time_d for space in range(4**3))
    require(weights=={b*b:128,c*c:128} and len(time_d)*4**3==256,
            "all sites and physical uniform measure")
    require(max(map(abs,psi))<P.lo and min(1-P.hi-f*f for f in psi)>0,
            "full material carrier slack")
    return time_d


def main():
    k0,elasticity=verify_reporter()
    eps, b, c=F(1,2**14), F(1,4), F(1,2)
    d=check_lattice(b,c)
    require((eps*PHI2*c**2).hi<F(1,1024),"both complete scales in verified chart")
    def ratios(scale2):
        ub,uc = (reporter_y(eps*scale2*x*x)[0] for x in (b,c))
        h=uc/ub
        return (-k0*(b*b+c*c*h)/4, -k0*(c*c+b*b/h)/4, h)
    rb1,rc1,h1=ratios(span(1))
    rb2,rc2,h2=ratios(PHI2)
    db,dc=rb2-rb1,rc2-rc1
    # d log[h(lambda)]/d lambda >= 3(c²-b²); h>=1, so the same
    # lower bound applies to h'. This bound is valid at every allowed eps.
    lower_h = 3*(c*c-b*b)*eps*(PHI2-1)
    require(h1.lo>1 and (h2-h1-lower_h).lo>0,"integrated scale separation for all eps")
    require(db.hi<0<dc.lo,"opposed readings from the very same two preparations")
    require((-db-k0*c*c*lower_h/4).lo>0 and
            (dc-k0*b*b*lower_h/(4*h1*h2)).lo>0,"both finite lower bounds")
    target = -k0*(b*b+c*c)/4
    require(rb1.hi<target.lo<target.hi<rc1.lo,"target lies strictly between the paid responses")
    # If every central numerator and denominator error is bounded by eta
    # times its own exact denominator, |Rhat-R|<=eta(1+|R|)/(1-eta).
    eta=F(1,10**7)
    rmax=max(max(-r.lo,r.hi) for r in (rb1,rc1,rb2,rc2))
    worst=span(2*eta*(1+rmax)/(1-eta))
    require(worst.hi<min(-db.hi,dc.lo),"a common relative error budget resolves both signs")
    print(json.dumps({
        "status":"PASS",
        "squared_scale":["1","phi^2"],"cell_weights":["128/256","128/256"],
        "forward_time_differences":[str(x) for x in d],
        "strict_Aprime_interval_on_0_to_1_over_1024":elasticity.fmt(13),
        "SC1_k0":k0.fmt(13),"raw_coframe":"I","material_volume":"1",
        "epsilon_fixture":str(eps),"R_target_radial":target.fmt(15),
        "R_b_1":rb1.fmt(15),"R_b_phi":rb2.fmt(15),"shift_b":db.fmt(15),
        "R_c_1":rc1.fmt(15),"R_c_phi":rc2.fmt(15),"shift_c":dc.fmt(15),
        "shape_price_response_ratio_Dprice_zc_over_Dprice_zb":h1.fmt(15),
        "per_row_relative_accuracy_in_fixture":str(eta),
        "error_for_two_ratios_at_that_accuracy":worst.fmt(15),
        "native_implementation":"Finite common-clock realization follows under the stated compiler and price bounds; no word emitted here.",
        "scope":"Exact finite response of specified readout; growing-clock bounds and microscopic valuation have separate hypotheses."
    },indent=2))


if __name__=="__main__":
    main()
