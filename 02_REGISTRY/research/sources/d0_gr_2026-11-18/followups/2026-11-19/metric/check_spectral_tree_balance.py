"""A signed information ledger for a positive spectral tree, and the actual H.1 cost gap."""
from fractions import Fraction as F
from math import factorial
import json

from check_counted_separator import analysis as old_master
from check_extra_work import Span, span
from check_paid_tail_audit import analyze as paid_receipt
from check_reference_pf_path import ln_interval
from check_source_price import need


# Formal real linear combinations of 1 and log_phi(prime).
def add(*terms):
    total = {}
    for a, value in terms:
        for key, coefficient in value.items():
            total[key] = total.get(key, F(0)) + a*coefficient
    return {k: v for k, v in total.items() if v}


def log_form(x):
    result = {}
    for integer, sign in ((x.numerator,1), (x.denominator,-1)):
        divisor = 2
        while divisor*divisor <= integer:
            while integer % divisor == 0:
                result[divisor] = result.get(divisor, 0) + sign
                integer //= divisor
            divisor += 1
        if integer > 1:
            result[integer] = result.get(integer, 0) + sign
    return {k:v for k,v in result.items() if v}


def tree_test(nu):
    leaves = {"0": (F(1,5), F(1,4), 3), "10": (F(3,10), F(2,3), 5),
              "11": (F(1,2), F(5,9), 4)}
    total_weight = sum(a for _,a,_ in leaves.values())
    def subtree(h):
        return [(w,p,a,c) for w,(p,a,c) in leaves.items() if w.startswith(h)]
    values, entropy = {}, {}
    for h in ("","0","1","10","11"):
        rows=subtree(h)
        total=sum(p for _,p,_,_ in rows)
        law=[(p/total,a,c) for _,p,a,c in rows]
        entropy[h]=add(*[(-prob,log_form(prob)) for prob,_,_ in law])
        values[h]=add(*[(prob,add((1,{"unit":c}),(F(1,nu),log_form(a)))) for prob,a,c in law],
                      (-1,entropy[h]))
    for h in ("", "1"):
        total=sum(p for _,p,_,_ in subtree(h))
        next_p={b:sum(p for _,p,_,_ in subtree(h+b))/total for b in ("0","1")}
        expected=add(*[(prob,add((1,values[h+b]),(-1,values[h]))) for b,prob in next_p.items()])
        next_entropy=add(*[(-prob,log_form(prob)) for prob in next_p.values()])
        need(expected==next_entropy, "local Shannon condition at each native-tree-style prefix")
    avg_cost=sum(p*c for p,_,c in leaves.values())
    divergence=add(*[(p,log_form(p*total_weight/a)) for p,a,c in leaves.values()])
    root=add((1,{"unit":avg_cost}),(-1-F(1,nu),entropy[""]),
             (F(1,nu),log_form(total_weight)),(-F(1,nu),divergence))
    need(values[""]==root,"exact root obstruction in independent formal logs")
    for w,(_,a,c) in leaves.items():
        infos=add(*[(1,add((1,values[w[:j+1]]),(-1,values[w[:j]]))) for j in range(len(w))])
        # log_phi p^(nu*(C-I)) = log_phi A - nu*V(root).
        need(add((-nu,{"unit":c}),(nu,infos))==add((1,log_form(a)),(-nu,root)),
             "all absolute leaf weights including the same common factor")
    return {str(k):str(v) for k,v in root.items()}


def report():
    paid=paid_receipt()
    raw=old_master()
    p=(span(5).sqrt()-1)/2
    ell=ln_interval(1/p)
    beta=2*p**2
    x=beta/11
    # For L=3, n>=3, each successive Taylor term shrinks by a factor <=x/4.
    epsilon=2*x**3/(factorial(3)*(1-x/4))
    # exp(2 beta) <= exp(1.53) < 4.62, using a positive rational remainder.
    exponent=2*beta
    terms=[exponent**i/factorial(i) for i in range(15)]
    inv_m=sum(terms,span(0))+exponent**15/(factorial(15)*(1-exponent/16))
    kl_bound=epsilon**2*inv_m**2/(2*ell)
    need(kl_bound.hi<F(29,10**8), "L=3 whole-tree divergence below 2.9e-7 golden units")
    def interval(pair):
        return Span(F(pair[0]),F(pair[1]))
    dL=interval(paid["paid_token_length_delta"])
    dHfine=interval(paid["fine_entropy_delta_including_additional_detectors"])
    dLbefore=interval(raw["noise_plus"])-interval(raw["noise_minus"])
    h_tail=interval(paid["all_new_tails_binary_entropy_phi"])
    dHreports=dHfine-4*p**3*h_tail*p**2*dLbefore
    # In units 1e-48: rigorous upper on |Delta J'| and two-grade heat.
    z=F(1,2**20)
    boundJ=(p**64/(1-z))*span(F(raw["minus_delta_feedback"][1])*10**48)
    bound_heat=span(F(6*88*10**48,359*64**15*2**64))
    upper_graph=(boundJ+beta*bound_heat)/ell
    need(upper_graph.hi<10**9,"|Delta log_phi Z_N| < 1e-39")
    global_log_floor=(ln_interval(span(359))+167*ln_interval(span(2)))/ell
    rs={}
    for nu in (1,2):
        alpha=1+F(1,nu)
        root_lower=F(paid["conditional_budgets"][nu]["certified_deficit_lower_bound"])+(global_log_floor-kl_bound)/nu
        secular={}
        for key,h in (("paid_reports",dHreports),("full_computational_refinement",dHfine)):
            base=alpha*h-dL
            # KL is nonnegative on both endpoints: the difference is at most one bound.
            tol=(kl_bound+span(F(1,10**39)))/nu
            secular[key]=[(base-tol).fmt(12)[0],(base+tol).fmt(12)[1]]
        rs[nu]={"root_lower_for_true_absolute_Z_N":root_lower.fmt(12)[0],
                "extra_mean_work_secant_for_equal_sources":secular,"formal_tree_root":tree_test(nu)}
    return {"status":"PASS","true_Audit_sha256":paid["native_owner"],"births_in_audit":64,
            "last_birth_to_closure_L_lower":3,"entropy_error_cap_phi":kl_bound.fmt(15)[1],
            "true_log_phi_Z_N_lower":global_log_floor.fmt(12)[0],
            "abs_secant_log_phi_Z_N_upper": "1e-39","tests":rs,
            "economic_local_rule_forced_on_the_full_native_histories":False}


if __name__=="__main__":
    print(json.dumps(report(),indent=2,ensure_ascii=False))
