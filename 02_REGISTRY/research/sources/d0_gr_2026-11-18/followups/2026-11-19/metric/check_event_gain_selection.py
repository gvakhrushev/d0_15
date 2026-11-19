"""Finite repetitions that distinguish posterior uncertainty and event information."""
from fractions import Fraction as F
from math import factorial
import json

from check_counted_separator import native_fronts
from check_extra_work import span
from check_live_parser import controller
from check_reference_pf_path import ln_interval
from check_repeat_clock import local_native
from check_source_price import need


def run():
    digest, _ = native_fronts()
    need(controller()[0]==digest==local_native(), "same bank, full LIVE and changed fronts")
    p=(span(5).sqrt()-1)/2
    ell=ln_interval(1/p)
    u=p**2
    c,s=span(1),span(0)
    for _ in range(29):
        c,s=c*p.sqrt()-s*p,s*p.sqrt()+c*p
    v=s**2
    odds=v*(1-u)/((1-v)*u)
    gap=-ln_interval(odds)/ell
    def entropy(q):
        return -(q*ln_interval(q)+(1-q)*ln_interval(1-q))/ell
    for a,b in ((v,u),(u,u)):
        h=entropy(a)+entropy(b)
        for first in (0,1):
            for second in (0,1):
                weight=(a if first else (1-a))*(b if second else (1-b))
                literal=-ln_interval(weight)/ell
                surprisal=(-ln_interval(a if first else (1-a))-ln_interval(b if second else (1-b)))/ell
                diff=literal-surprisal
                need(diff.lo<=0<=diff.hi,"all true path surprises add")
                drop=(h-entropy(b))+entropy(b)
                delta=drop-h
                need(delta.lo<=0<=delta.hi,"all posterior entropy drops telescope")
    n=256
    op_brackets={}
    # Each integer m is certified by the interval for -n log_phi(q).
    for name,q in (("first_noise_minus",v),("first_noise_plus",u)):
        length=-n*ln_interval(q)/ell
        # u=p^2 is algebraically exact so no open numerical floor is needed.
        if name=="first_noise_plus":
            m=2*n
            need(length.lo<=m<=length.hi,"exact golden benchmark")
        else:
            m=length.lo//1
            need(m<=length.lo<=length.hi<m+1,"golden comparison order")
        op_brackets[name]=[str(F(m,n)),str(F(m+1,n))]
    delta=1/(n*ell)
    lower_error=(1-v)*delta/v
    # Last six births precede all 28 native square calls in the last unchanged LIVE.
    x=F(7,100)
    heat_cost_error=120*x**28/(factorial(28)*(1-x/29))
    need(2*u.hi/11 < x and ell.lo > F(1,3), "numerical constants for both heat odds")
    need(sum(F(8,5)**i/factorial(i) for i in range(12))+
         F(8,5)**12/(factorial(12)*(1-F(8,65)))<5 and 4*u.hi<F(8,5),
         "exp(2 beta)<5")
    need(heat_cost_error<F(2,10**60), "genuine Gibbs perturbation for both odds")
    cases={}
    for nu in (1,2):
        cases[nu]={"posterior_entropy_drop_required_cost_contrast":(gap/nu).fmt(14),
                   "event_surprisal_required_cost_contrast":((1+F(1,nu))*gap).fmt(14)}
    return {"status":"PASS","native_primitive_hash":digest,"u":u.fmt(16),"v":v.fmt(16),
            "odds_minus":odds.fmt(16),"golden_log_odds_gap":gap.fmt(15),
            "required_Born_contrasts_minus_relative_to_plus":cases,
            "absolute_change_from_using_genuine_Gibbs_odds_bound":"2e-60/nu",
            "n":n,"integer_monotone_golden_comparisons":op_brackets,
            "all_success_conditional_upper_error":delta.fmt(12),
            "all_success_conditional_lower_error_for_v":lower_error.fmt(12),
            "event_price_monotonicity_derived_in_Book":False}


if __name__=="__main__":
    print(json.dumps(run(),indent=2))
