"""Exact golden prefix sums and rational enclosures for the last LIVE noise."""
from fractions import Fraction as F
import json

from check_extra_work import Span, span
from check_golden_record_race import gold, p
from check_live_parser import terminal
from check_reference_pf_path import binary_kl, ln_interval
from check_source_price import need


def weight(word):
    return p**(len(word)+word.count("1"))


def complete_tree(seed,depth):
    # Both children are kept whenever the current leaf is refined.
    tips=[""]
    for level in range(depth):
        next_level=[]
        for word in tips:
            active=level==0 or (len(word)==level and
                (int(word or "0",2)+seed+len(word))%5!=0)
            next_level.extend([word+"0",word+"1"] if active else [word])
        tips=next_level
    return tips


def mass(tips):
    ordered=sorted(tips)
    need(all(not b.startswith(a) for a,b in zip(ordered,ordered[1:])),
         "distinct terminal cylinders form an antichain")
    return sum((weight(w) for w in tips),gold(0))


def main():
    eps=(span(5).sqrt()-1)/2
    u=eps**2
    H=-u*ln_interval(u)-(1-u)*ln_interval(1-u)
    rows=[]
    for i,stratum in enumerate([
          ("0.0324276829699111","0.0324276829699113"),
          ("0.8736311345495272","0.8736311345495275")]):
        lo,hi=map(lambda s: span(F(s)),stratum)
        f0=binary_kl(u,lo)-H
        f1=binary_kl(u,hi)-H
        need((f0.lo>0 and f1.hi<0) if i==0 else (f0.hi<0 and f1.lo>0),
             "rational log-series signs bracket both unique zeros")
        r=Span(lo.lo,hi.hi)
        ratio=r/((1-r)*eps) if i==0 else eps*(1-r)/r
        rows.append({"bounded_ratio":"tau_error/tau_success" if i==0 else "tau_success/tau_error",
            "ratio_threshold":ratio.fmt(13),"missing_reference_mass_fraction_minimum":(1-ratio).fmt(13)})
    trees=[complete_tree(seed,8+seed%3) for seed in range(10)]
    for tips in trees:
        need(mass(tips)==gold(1),"full finite stopping rule includes every timeout")
    for t in (0,1):
        lengths=[]
        for x in (0,1):
            d=t^x
            lengths.append(sum(map(len,terminal(t,d,1^d,0,0,0,0))))
        need(lengths==[5+t,6+t],"actual LIVE four charged words")
        m0=p**lengths[0]*mass(trees[t])
        m1=p**lengths[1]*mass(trees[9-t])
        need(m1/(m0+m1)==p**2,"exact golden reference still equals original noise law")
    for n in (1,5,6,7):
        mask=["0"*n+w for w in trees[n]]
        need(mass(mask)==p**n,"strict sublanguage has exact reference loss")
    def certify_offset(n, sign):
        exponent=1+n
        odds=eps**exponent if exponent>=0 else 1/(eps**(-exponent))
        r=odds/(1+odds)
        f=binary_kl(u,r)-H
        need(f.lo>0 if sign>0 else f.hi<0,"sharp integer differential for deterministic extras")
    for n,sign in ((6,-1),(7,1),(-5,-1),(-6,1)):
        certify_offset(n,sign)
    print(json.dumps({"status":"PASS","complete_trees":len(trees),
        "number_of_tip_cylinders":[len(tips) for tips in trees],
        "exact_conditional_error_reference_in_basis_1_p":(p**2).strings(),
        "branch_thresholds":rows,"minimal_integer_extra_error_minus_success_gaps":[-6,7],
        "physical_identification_of_all_hidden_traversal_prices":False},
        ensure_ascii=False,sort_keys=True,indent=2))


if __name__=="__main__":
    main()
