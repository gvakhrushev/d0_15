"""Extra-work profiles of the restored H.1 binary report; pure Python 3.

For t=P(branch), x=2-t and y=2 (t<=1/4) or sqrt(t)+sqrt(3(1-t)).
On t>=1/4, y'<=0 because 1-t<=3t, and y''<0. At 1/4 the derivative
is zero, hence both distances are globally concave and decreasing.
Increasing in this script means nondecreasing in each coordinate.

If Phi is concave and increasing, g(t)=Phi(x(t),y(t)) is concave and
decreasing. The Jensen product gap below proves f(t)=t*g(t) is concave:
first use concavity of g, then nonnegative product gap. Consequently
E(q)=f(q)+f(1-q) is symmetric concave and nondecreasing up to 1/2.
Indeed q2 in [q1,1/2] is a convex combination of q1 and 1-q1. This
proves the secant bound total(q2)-total(q1) >= P(q2)-P(q1), without
differentiating a possibly nonsmooth profile. Finite-valued infima of a
fixed family of such concave functions retain concavity (and symmetry
when applied to E). Separate minimizing choices for the two labels
instead amount to replacing g by its pointwise infimum before forming E.
The profile family and the calibrations must be fixed over comparisons.
"""
from fractions import Fraction as F
from math import isqrt
import json


GRID = 10**45


def check(ok, why):
    if not ok:
        raise ValueError(why)


def ceiling(x):
    return -((-x.numerator)//x.denominator)


class Span:
    """Rational outward-rounded enclosure on a decimal grid."""
    def __init__(self, lo, hi=None):
        lo = F(lo)
        hi = lo if hi is None else F(hi)
        check(lo <= hi, "unordered interval")
        self.lo = F((lo*GRID)//1, GRID)
        self.hi = F(ceiling(hi*GRID), GRID)

    def __add__(self, b):
        b = span(b)
        return Span(self.lo+b.lo, self.hi+b.hi)

    __radd__ = __add__

    def __neg__(self):
        return Span(-self.hi, -self.lo)

    def __sub__(self, b):
        return self+(-span(b))

    def __rsub__(self, b):
        return span(b)+(-self)

    def __mul__(self, b):
        b = span(b)
        products = [i*j for i in (self.lo,self.hi) for j in (b.lo,b.hi)]
        return Span(min(products),max(products))

    __rmul__ = __mul__

    def __truediv__(self, b):
        b = span(b)
        check(b.lo>0 or b.hi<0, "interval division by zero")
        return self*Span(1/b.hi,1/b.lo)

    def __rtruediv__(self, b):
        return span(b)/self

    def __pow__(self, n):
        check(isinstance(n,int) and n>=0, "nonnegative integer powers")
        val=span(1)
        for _ in range(n):
            val=val*self
        return val

    def sqrt(self):
        check(self.lo>=0, "sqrt on negative input")
        def floor_root(a):
            return isqrt((a.numerator*GRID**2)//a.denominator)
        return Span(F(floor_root(self.lo),GRID),F(floor_root(self.hi)+1,GRID))

    def log_positive(self):
        # log z=2*(s+s^3/3+...), s=(z-1)/(z+1), all uses have z>1.
        check(self.lo>1, "log-series sign")
        t=(self-1)/(self+1)
        t2=t*t
        power=t
        total=span(0)
        for k in range(50):
            total=total+2*power/(2*k+1)
            power=power*t2
        rem=2*power.hi/(101*(1-t.hi**2))
        return total+Span(0,rem)

    def fmt(self, digits=12):
        scale=10**digits
        def decimal(k):
            integer,rest=divmod(abs(k),scale)
            return ("-" if k<0 else "")+str(integer)+"."+str(rest).zfill(digits)
        return [decimal((self.lo*scale)//1),decimal(ceiling(self.hi*scale))]


def span(x):
    return x if isinstance(x,Span) else Span(x)


def min_span(*values):
    return Span(min(x.lo for x in values),min(x.hi for x in values))


def exact_structural_checks():
    # Polynomial identity for arbitrary x,y,u,v,theta: bilinear in (x,y),
    # (u,v), quadratic in theta. Coordinate bases and 3 points prove it.
    for x,y in ((1,0),(0,1)):
        for u,v in ((1,0),(0,1)):
            for a in (F(0),F(1,2),F(1)):
                t=a*x+(1-a)*y
                gap=t*(a*u+(1-a)*v)-a*x*u-(1-a)*y*v
                check(gap==a*(1-a)*(y-x)*(u-v),"Jensen product identity")
    # Reg and cohesive agree with their native two-stage definitions.
    # Exact swap identity covers any prices, not just positive costs.
    for q in (F(0),F(1,3),F(1,2)):
        for c0,c1 in ((0,1),(1,0)):
            cur=(1-q)*c0+q*c1
            swapped=(1-q)*c1+q*c0
            check(cur-swapped==(1-2*q)*(c0-c1),"swap affine identity")
    # Sharp example: swapped tariff with overhead eps is available, and
    # the original is eta above it. This checks the epsilon+eta numerator.
    q,eps,eta=F(2,5),F(1,50),F(1,100)
    c0,c1=(eps+eta)/(1-2*q),F(0)
    cur=(1-q)*c0+q*c1
    alt=(1-q)*c1+q*c0+eps
    check(cur-alt==eta and c1-c0==-(eps+eta)/(1-2*q),"sharp swap estimate")
    # The restored complete binary effects are scalar on the protected
    # input: summing all four recorded paths gives the product report law.
    # Compare exact bilinear coefficients on a basis of the square.
    for s in (F(0),F(1)):
        for t in (F(0),F(1)):
            probs=tuple(a*b for a in (1-s,s) for b in (1-t,t))
            match=probs[0]+probs[3]
            check(sum(probs)==1 and match==1-s-t+2*s*t,"all four report rows")
            check(probs[1]+probs[2]==s+t-2*s*t,"complementary mismatch")


def centre():
    p=(span(5).sqrt()-1)/2
    c,s=p.sqrt(),p
    for _ in range(9):
        c,s=c*c-s*s,2*c*s
    q=p**2+4*p**10*s*s
    check(q.lo>F("0.4124698805685") and q.hi<F("0.4124698805686"),"true q star")
    return q,(1/p).log_positive()


def profiles(q,ell):
    x=1-2*q
    u=(q*(1-q)).sqrt()
    r=(1+2*u).sqrt()
    c=span(3).sqrt()-1
    entropy=((1-q)/q).log_positive()/ell
    base=1-entropy
    delta_reg=x
    # sqrt(q)+sqrt(3)*sqrt(1-q), less the swapped branch value.
    delta_coh=c*((1-q).sqrt()-q.sqrt())
    coh_der=x*((1+c*u)/r+c*r)/(2*u)
    return base,entropy,[(delta_reg,2*x),(delta_coh,coh_der)]


def inf_examples():
    # Both profiles are nonnegative affine coordinatewise increasing.
    # At q*, different labels prefer different functions. The two infimum
    # placements therefore implement genuinely different prices.
    def components(t):
        x=2-t
        y=t.sqrt()+(3*(1-t)).sqrt()
        return x+F(21,50),y
    def costs(q):
        a,b=components(q)
        c,d=components(1-q)
        shared=min_span(q*a+(1-q)*c,q*b+(1-q)*d)
        separate=q*min_span(a,b)+(1-q)*min_span(c,d)
        return separate,shared
    samples=[span(F(n,1000)) for n in (382,390,400,415,430,450,470,490,500)]
    old=costs(samples[0])
    for q in samples[1:]:
        new=costs(q)
        check(all(a.hi<b.lo for a,b in zip(old,new)), "both infima nondecreasing")
        old=new
    q,_=centre()
    separate,shared=costs(q)
    check(separate.hi<shared.lo,"shared and separate infima contrast")
    return {"separate_at_q_star":separate.fmt(),"shared_at_q_star":shared.fmt(),
            "exact_general_basis":"Jensen product and symmetric concavity; test grid is supplementary"}


def power_derivative(q,n):
    return ((2-q)**(n-1)*(2-(n+1)*q)
            +(1+q)**(n-1)*(n-1-(n+1)*q))


def main():
    exact_structural_checks()
    q,ell=centre()
    x=1-2*q
    collar=Span("0.41246","0.41248")
    base,entropy,data=profiles(q,ell)
    base_band=1-((1-collar)/collar).log_positive()/ell
    check(F("0.26484698")<base.lo and base.hi<F("0.26484699"),"true P-prime")
    check(base_band.lo>F("0.2647"),"positive lower slope on the wider interval")
    matched={}
    for name,(delta,der) in zip(("registered","coherent"),data):
        alpha=1/delta
        check(alpha.lo>0 and (alpha*delta).lo<=1<=(alpha*delta).hi,"unit report fee difference")
        additive=base+alpha*der
        substitute=alpha*der-entropy
        check(additive.lo>0 and substitute.lo>0,"fixed matched derivative")
        matched[name]={"branch_gap":delta.fmt(),"frozen_alpha":alpha.fmt(),
                       "additive_P_plus_alpha_E_derivative":additive.fmt(),
                       "substitute_alpha_E_minus_entropy_derivative":substitute.fmt()}
    adversarial={}
    for n in (16,32):
        alpha=1/((2-q)**n-(1+q)**n)
        d=power_derivative(collar,n)
        raw=base_band+d
        matched_net=base_band+alpha*d
        check(raw.hi<0 and matched_net.hi<0,"convex counterexample on the whole interval")
        adversarial[str(n)]={"uncalibrated_net_whole_collar":raw.fmt(6),
                             "same_branch_gap_frozen_alpha":alpha.fmt(15),
                             "matched_net_whole_collar":matched_net.fmt(9)}
    work={}
    for name,sign in (("match",-1),("mismatch",1)):
        row=base+sign*2*x
        diagonal=2*row
        check((row.hi<0 and diagonal.hi<0) if sign==-1 else (row.lo>0 and diagonal.lo>0),
              "paid two-report control")
        collar_row=base_band+sign*2*(1-2*collar)
        check(collar_row.hi<0 if sign==-1 else collar_row.lo>0,"two-report interval sign")
        work[name]={"one_independent_row":row.fmt(),"equal_q_diagonal":diagonal.fmt(),
                    "one_row_whole_collar":collar_row.fmt(9)}
    budget=x*base
    check(F("0.0463")<budget.lo and budget.hi<F("0.0464"),"swap threshold")
    result={"status":"PASS","scope":"specified restored two-stage profiles and optional real reports; no identification of all physical Cost-Info",
            "literal_q_star":q.fmt(14),"literal_P_prime":base.fmt(14),
            "P_prime_whole_interval":base_band.fmt(9),"interval":["0.41246","0.41248"],
            "infima":inf_examples(),"linear_branch_gap_calibration":matched,
            "convex_power_counterexamples":adversarial,
            "approximate_swap":{"conditional_slope_bound":"c1-c0 >= -(epsilon+eta)/(1-2q)",
                                "literal_positive_slope_budget":budget.fmt(14),
                                "sharp_affine_witness":True,
                                "source_scope":"fixed tariffs or active affine slopes; a moving family has its own source"},
            "two_restored_reports_fee_2":work,"GR_closed":False}
    print(json.dumps(result,indent=2,ensure_ascii=True))


if __name__=="__main__":
    main()
