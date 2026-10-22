#!/usr/bin/env python3
"""Independent finite controls for D0 #334 stopped Golden goal/clock/archive KL.

This checks a specified measured-code probability model, NOT Book03 selection,
physical input admission, or GR closure. Only Python standard library needed.
"""
from __future__ import annotations
import itertools
import json
import math

PHI = (1.0 + math.sqrt(5.0)) / 2.0
P = 1.0 / PHI
LOGPHI = math.log(PHI)

def kl(p, q):
    assert len(p) == len(q)
    return sum(x * math.log(x / y) / LOGPHI for x, y in zip(p, q))

def normalize(xs):
    s = sum(xs)
    return [x / s for x in xs]

def close(x, y, atol=1e-9, rtol=1e-9):
    assert math.isfinite(x) and math.isfinite(y)
    assert abs(x-y) <= atol + rtol * max(abs(x), abs(y)), (x,y)

def clock_kl(q, mu):
    """KL of (first class A, mismatch count N), NO archive of mismatch types."""
    return sum((2*x*math.log(x/y) + (1-x)*math.log((1-x)/(1-y)))/LOGPHI
               for x, y in zip(q, mu))

def mismatch_kl(q, mu):
    m = len(q)
    return sum((1-q[a])*kl([q[b]/(1-q[a]) for b in range(m) if b != a],
                           [mu[b]/(1-mu[a]) for b in range(m) if b != a])
               for a in range(m))

def clock_gradient(q, mu, dq):
    return sum((2*math.log(x/y) - math.log((1-x)/(1-y)))*d/LOGPHI
               for x, y, d in zip(q, mu, dq))

def mismatch_gradient(q, mu, dq):
    m = len(q)
    return (m-1)*sum(math.log(x/y)*d/LOGPHI for x,y,d in zip(q,mu,dq)) - sum(
        math.log((1-x)/(1-y))*(-d)/LOGPHI for x,y,d in zip(q,mu,dq))

def fisher_clock(q, dq):
    return sum(d*d*(2-x)/(x*(1-x)) for x,d in zip(q,dq))

def fisher_mismatch(q, dq):
    m=len(q)
    out=0.0
    for a in range(m):
        den=1-q[a]
        for b in range(m):
            if b==a: continue
            s=q[b]/den
            ds=dq[b]/den + q[b]*dq[a]/(den*den)
            out+=den*ds*ds/s
    return out

def conditional_site_info(w, r):
    bar=sum(ww*rr for ww,rr in zip(w,r))
    h=lambda t:-(t*math.log(t)+(1-t)*math.log(1-t))/LOGPHI
    return h(bar)-sum(ww*h(rr) for ww,rr in zip(w,r))

def three_atom(a, w, r):
    bar=sum(ww*rr for ww,rr in zip(w,r))
    q=[1-a,a*(1-bar),a*bar]
    mu=[1-a,a*P,a*P*P]
    # The coarsened fine law has 1+2*len(w) categories; all genuine
    # Golden-prefix conditional kernels are identical under P and mu.
    pf=[1-a]
    mf=[1-a]
    for ww,rr in zip(w,r):
        pf.extend((a*ww*(1-rr),a*ww*rr))
        mf.extend((a*ww*P,a*ww*P*P))
    return q,mu,pf,mf

def check_direct_stopped_enumeration():
    # Enumerate actual completed first-match category WORDS through N=8.
    # Check the partition identity on the truncated *unconditioned* subset,
    # without declaring the tail zero or postselecting it.
    q=[0.21,0.34,0.45]
    mu=[0.32,0.28,0.40]
    k_full=k_clock=k_mismatch=mass=0.0
    for a in range(3):
        others=[j for j in range(3) if j!=a]
        for n in range(9):
            xAN=q[a]**2*(1-q[a])**n
            yAN=mu[a]**2*(1-mu[a])**n
            loc_mass=0.0
            loc_full=0.0
            loc_hidden=0.0
            for seq in itertools.product(others,repeat=n):
                x=q[a]**2
                y=mu[a]**2
                for b in seq:
                    x*=q[b]
                    y*=mu[b]
                if x==0: continue
                loc_mass+=x
                loc_full+=x*math.log(x/y)/LOGPHI
                loc_hidden+=x*math.log((x/xAN)/(y/yAN))/LOGPHI
            close(loc_mass,xAN,1e-12)
            k_full+=loc_full
            k_clock+=xAN*math.log(xAN/yAN)/LOGPHI
            k_mismatch+=loc_hidden
            mass+=loc_mass
    close(k_full,k_clock+k_mismatch,1e-11)
    assert 0<mass<1
    return mass

def check_fisher_direct():
    q=[0.21,0.34,0.45]
    dq=[0.01,-0.035,0.025]
    out=0.0
    # True geometric distribution and score, no approximate finite differencing.
    for x,d in zip(q,dq):
        for n in range(220):
            prob=x*x*(1-x)**n
            score=(2/x-n/(1-x))*d
            out+=prob*score*score
    close(out,fisher_clock(q,dq),atol=1e-12,rtol=1e-9)
    close((len(q)+1)*sum(d*d/x for x,d in zip(q,dq)),
          fisher_clock(q,dq)+fisher_mismatch(q,dq),1e-12)

def check_site_jet():
    a=2*10946*P**23
    w=[0.17,0.24,0.59]
    r=[0.00071,0.0012,0.0024]
    dr=[+0.02,-0.017,0.009]
    q,mu,pf,mf=three_atom(a,w,r)
    i=conditional_site_info(w,r)
    close(kl(pf,mf),kl(q,mu)+a*i,1e-12)
    close(4*kl(pf,mf),clock_kl(q,mu)+mismatch_kl(q,mu)+4*a*i,1e-12)
    delta=2e-7
    def perturb(sign):
        rr=[t+sign*delta*d for t,d in zip(r,dr)]
        Q,M,PF,MF=three_atom(a,w,rr)
        return 4*kl(PF,MF),clock_kl(Q,M),mismatch_kl(Q,M),4*a*conditional_site_info(w,rr)
    plus=perturb(1); minus=perturb(-1)
    deriv=[(x-y)/(2*delta) for x,y in zip(plus,minus)]
    close(deriv[0],sum(deriv[1:]),1e-7)
    # Independently use the actual exact per-site entropy/code derivative.
    prime=lambda t:1-math.log((1-t)/t)/LOGPHI
    source=4*a*sum(ww*prime(rr)*d for ww,rr,d in zip(w,r,dr))
    close(deriv[0],source,2e-7)
    # At a common-null reporter, inhomogeneous site tangents invisible to A,N.
    rr=[0.001]*3
    dr=[1,-w[0]/w[1],0]
    dbar=sum(ww*d for ww,d in zip(w,dr))
    close(dbar,0,1e-15)
    full_fisher=4*a*sum(ww*d*d for ww,d in zip(w,dr))/(rr[0]*(1-rr[0]))
    assert full_fisher > 0
    clock_fisher=fisher_clock([1-a,a*(1-rr[0]),a*rr[0]],
                                [0,-a*dbar,a*dbar])
    close(clock_fisher,0,1e-15)

def check_controls():
    q=[0.21,0.34,0.45]
    mu=[0.32,0.28,0.40]
    dq=[0.01,-0.035,0.025]
    close((len(q)+1)*kl(q,mu),clock_kl(q,mu)+mismatch_kl(q,mu),1e-13)
    # All original q are free probability coordinates on the simplex.
    close((len(q)+1)*sum(math.log(x/y)*d/LOGPHI for x,y,d in zip(q,mu,dq)),
          clock_gradient(q,mu,dq)+mismatch_gradient(q,mu,dq),1e-12)
    # Binary: given initial class and N, every mismatch label is forced.
    qb=[0.19,0.81]
    mb=[P,P*P]
    close(mismatch_kl(qb,mb),0,1e-13)
    close(clock_kl(qb,mb),3*kl(qb,mb),1e-13)
    # Three outcomes: if q != reference, mismatch archive is positive.
    assert mismatch_kl(q,mu)>0
    close(mismatch_kl(mu,mu),0,1e-13)
    # Native identity: q_U=mu_U => nonready-first contribution equals 1-trial KL.
    a=2*10946*P**23
    z=2**-20
    L=4*P**3
    r=1-(1-z*L)*(1-z*L*(1+P**6))
    q=[1-a,a*(1-r),a*r]
    mu=[1-a,a*P,a*P*P]
    val=kl(q,mu)
    goal=clock_kl(q,mu)
    miss=mismatch_kl(q,mu)
    close(4*val,goal+miss,2e-12)
    assert miss>=val
    # Hard original rare-signal Fischer split, FIRST SOURCE not enough.
    dq=[0,-a,a]
    full_fisher=4*sum(d*d/x for d,x in zip(dq,q))
    goal_fisher=fisher_clock(q,dq)
    rest_fisher=fisher_mismatch(q,dq)
    close(full_fisher,goal_fisher+rest_fisher,1e-8)
    assert 0<goal_fisher/full_fisher<1
    close(goal_fisher/full_fisher,0.5000003982787,2e-9)
    # Native source is not preserved by the goal-clock projection.
    d_stop=4*sum(math.log(x/y)*d/LOGPHI for x,y,d in zip(q,mu,dq))
    d_goal=clock_gradient(q,mu,dq)
    d_rest=mismatch_gradient(q,mu,dq)
    close(d_stop,d_goal+d_rest,1e-10)
    assert abs(d_rest)>1
    return {'phi':PHI,'ready':a,'report':r,'q':q,'mu':mu,
            'stopped_kl':4*val,'goal_clock_kl':goal,'nonmatch_archive_kl':miss,
            'missing_kl_fraction':miss/(4*val),'report_source_full':d_stop,
            'report_source_goal_clock':d_goal,'report_source_nonmatch':d_rest,
            'fisher_full':full_fisher,'fisher_goal_clock':goal_fisher,
            'fisher_nonmatch':rest_fisher,'fisher_goal_clock_fraction':goal_fisher/full_fisher}

def main():
    close(P+P*P,1,1e-14)
    controls=check_controls()
    check_direct_stopped_enumeration()
    check_fisher_direct()
    check_site_jet()
    print(json.dumps({'status':'SCOPED_PASS','test_groups':4,'native':controls,
          'physical_selection':'UNDEFINED','Book03_Info':'UNDEFINED',
          'GR_closed':False,'raw216_closed':False},sort_keys=True,indent=2))

if __name__=='__main__': main()
