"""Direct H.1 terminal-source bounds and a retained-command test on native SC1."""
import json
import sys
from fractions import Fraction as R
from math import comb
from pathlib import Path

sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"round75/work"))
from check_pointer_weyl import I,O


def main():
    one=I(1.)
    p=(I(5.).sqrt()-1)/2
    def power(x,n):
        a=one
        for _ in range(n):
            a=a*x
        return a
    p2,p3=p.square(),power(p,3)
    p36=power(p,36)
    counts=[5644800,4939200,4390400,3087000,1580544,548800,115200,11025]
    O.require(sum(counts)==20316969 and all(R(c*j*j,comb(8,j))==705600 for j,c in enumerate(counts,1)),
              "actual direct and complemented selector populations")
    active=p36*sum(counts)
    qhi=p2+6*power(p,10)
    O.require(qhi.hi<.432 and qhi.hi<p.lo,"each active native positive report <1/2")
    low,high=active*p2,active*p
    slo,shi=p3*(1+low),p3*(1+high)
    O.require(low.lo>.23 and high.hi<.38 and slo.lo>.29 and shi.hi<.325,
              "unguarded event and its independent guard")
    logphi=-O.logarithm(p)
    lo,hi=I.rational(R(23,100)),I.rational(R(38,100))
    source_floor=I(3.)-O.logarithm((one-lo)/lo)/logphi
    reg_floor=2*(one-2*hi)
    sqrt3=I(3.).sqrt()
    # 2u <= 1, sqrt(1+2u) <= sqrt(2), u >= sqrt(3)/4 in the second regime.
    coh_floor=(one-2*hi)*(sqrt3+3*(sqrt3-1)*sqrt3/4)/I(2.).sqrt()
    O.require(source_floor.lo>.489 and reg_floor.lo>.47999 and coh_floor.lo>.4553,
              "uniform strictly positive slopes for the three terminal costs")
    O.require((I(.5)+sqrt3/4).lo>.93 and (2*p3).hi<.5,
              "low-s coherent regime and both guarded conditional coins")
    def terminal(s):
        def child(v):
            return I(2.) if v.hi<.25 else v.sqrt()+sqrt3*(one-v).sqrt()
        h=-(s*O.logarithm(s)+(one-s)*O.logarithm(one-s))/logphi
        return 1+3*s-h,1+2*s*(one-s),s*child(s)+(one-s)*child(one-s)
    chords=[v-u for u,v in zip(terminal(p3),terminal(2*p3))]
    O.require(all(a.lo>b for a,b in zip(chords,(.40669,.13776,.14757))),
              "old T registered, fresh selector not exposed")
    # Compute the eight actual conditional-reader jets along a constant-I line.
    # SC2 supplies the scalar readiness for this numerical witness.
    z=I.rational(R(1,2**20))
    base=4*p3
    rf=4*p2*(one-2*p2)*z*(one-z*base)*(one-base)
    rq=8*p3*(one-2*p2)*(z*(I(2.)-base)-z.square()*(base+(one-base)*base*2))
    b=rf/(2*rq)
    o=one-2*p2
    for _ in range(9):
        o=2*o.square()-1
    vis=(one-o)*power(p,7)/2
    ready=21892*power(p,23)
    q0=p2+4*p3*vis
    factor=p3*vis*ready.square()
    a2=-4*power(p,4)*z*(one-base)*(one-z*base)
    f=I.rational(R(1,7))
    def rgeom(x):
        # r(x,0)-r(0,0); quadratic coefficients from the native SC1 formula.
        return rf*x+a2*x.square()
    def rmatter(y):
        u=p+p2*y
        fixed_L=base
        B=4*u.square()*(one-u.square())
        A=fixed_L+(one-fixed_L)*B
        return z*(A+B)-z.square()*A*B
    sources=dict(registered=I(0.),coherent=I(0.),entropy=I(0.),probability=I(0.))
    for j,number in enumerate(counts,1):
        e=I.rational(R(j,256))
        A=rmatter(b*e)-rmatter(-b*e)
        q=q0+factor*A*(p*rgeom(e*f/p)+p2*rgeom(e*f/p2))
        rate=factor*A*2*a2*e.square()*f*(one/p-one/p2)
        O.require(A.lo>0 and rate.lo>0 and q.lo>.25 and q.hi<.432,
                  "all genuine conditional reader rates positive along DI=0")
        mass=number*p36
        u=(q*(one-q)).sqrt()
        lc=(one-2*q)*(sqrt3+3*(sqrt3-1)*u)/(2*u*(1+2*u).sqrt())
        sources["registered"]+=mass*2*(one-2*q)*rate
        sources["coherent"]+=mass*lc*rate
        sources["entropy"]+=mass*O.logarithm((one-q)/q)*rate/logphi
        sources["probability"]+=(1 if j%2 else -1)*mass*rate
    O.require(sources["probability"].contains(0) and all(sources[k].lo>0 for k in
              ("registered","coherent","entropy")),"signed overlap and branch-resolved witness")
    O.require(all(sum((-1)**(j-1)*comb(8,j)*j**k for j in range(1,9))==0
                  for k in range(1,8)),"exact zero for the odd degree-seven reference")
    return {"Q_outer": [float(low.lo),float(high.hi)],
            "guard_outer":[float(slo.lo),float(shi.hi)],
            "terminal_min_Fprime":O.bounds(source_floor),
            "terminal_min_Lrec":O.bounds(reg_floor),
            "terminal_Lcoh_lower_bound":O.bounds(coh_floor),
            "old_T_resolved_guarded_F_Lr_Lc_slopes":[O.bounds(v) for v in chords],
            "command_resolved_SC2_jets":{k:O.bounds(v) for k,v in sources.items()}}


if __name__=="__main__":
    print(json.dumps(main(),indent=2))
