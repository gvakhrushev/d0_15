#!/usr/bin/env python3
"""Exact rational witness and hostile controls for the D0 three-paid-word
D_min -> finite source -> Euler fork.

This proves its real-number inequalities in sampled exact rational cases and
the signed Book-return derivative formula. The universal inequality is
proved algebraically in its companion theorem markdown, NOT by sampling.
The simulated polynomial score families are NEGATIVE/POSITIVE LOGICAL
CONTROLS, NOT newly implemented D0-native words, which are owned by #334
section 7ay. No assumption that Book-price order equals actual D_min code
order is made or silently fitted. No physical GR closure.

Run python3 check_fork.py and python3 -O check_fork.py.
"""
from __future__ import annotations

from fractions import Fraction as Q
from itertools import product
import json


def require(condition, msg):
    if not bool(condition):
        raise ArithmeticError(msg)


COUNTS = {"exact_theorem_A": 0, "native_Book_derivatives": 0,
          "MDL_code_alignment": 0, "hostile_controls": 0}


def positive(x):
    return max(Q(0), Q(x))


def check_fork(b0, bp, bm, gamma, t, field_slope, secant_error,
               curvature_upper, even_error):
    """Check all hypotheses, then the exact bound and constructive cheaper
    competitor inequality. The mathematical proof is the identity
    |a-b|<=a+b+2(-a)_++2(-b)_+, with a=bp-b0, b=bm-b0.
    """
    vals = [b0, bp, bm, gamma, t, field_slope, secant_error,
            curvature_upper, even_error]
    b0, bp, bm, gamma, t, g, es, C2, ee = (Q(v) for v in vals)
    require(gamma > 0 and t > 0 and es >= 0 and C2 >= 0 and ee >= 0,
            "actual positive gain/timestep and nonnegative error budgets")
    secant = (bp-bm)/(2*gamma*t)
    require(abs(secant-g) <= es, "true first-source transfer hypothesis")
    even = bp+bm-2*b0
    require(even <= gamma*(C2*t*t+ee),
            "true even second-difference/curvature hypothesis")
    plus_debt = positive(b0-bp)
    minus_debt = positive(b0-bm)
    total_debt = plus_debt+minus_debt
    exact_core_rhs = even+2*total_debt
    require(abs(bp-bm) <= exact_core_rhs,
            "exact algebraic positive/negative-part fork")
    upper = es+(C2*t)/2+ee/(2*t)+total_debt/(gamma*t)
    require(abs(g)<=upper, "THEOREM A native source-to-Euler bound")
    construct_saving = gamma*t*(abs(g)-es)-gamma*(C2*t*t+ee)/2
    require(b0-min(bp,bm)>=construct_saving,
            "THEOREM A concrete Book-cheaper native alternative")
    if abs(g)>es+C2*t/2+ee/(2*t):
        require(min(bp,bm)<b0, "strict binary fork when field source nonzero")
    COUNTS["exact_theorem_A"]+=1
    return {
        "source": g, "bound": upper, "book_undershoot": total_debt,
        "actual_fork_saving": b0-min(bp,bm),
        "guaranteed_fork_saving": construct_saving,
    }


def check_selected_code(code0, codeplus, codeminus, price0, priceplus,
                        priceminus, scale_kappa, code_error,
                        gap_gamma, t, source_bound):
    """Check the exact reduction from a real native D_min length minimum
    and a separately PROVED finite same-task Book-vs-code alignment.
    """
    l0, lp, lm = (int(x) for x in [code0, codeplus, codeminus])
    kap, err, gm, t = (Q(v) for v in
                       [scale_kappa, code_error, gap_gamma, t])
    require(kap>0 and err>=0 and gm>0 and t>0, "MDL positive scales")
    require(l0<=lp and l0<=lm, "actual canonical shortest description")
    for length, price in [(lp, priceplus), (lm, priceminus)]:
        require(abs(Q(length-l0)-kap*(Q(price)-Q(price0)))<=err,
                "actual code/Book comparison must be independently verified")
        require(positive(Q(price0)-Q(price))<=err/kap,
                "code shortest implies at most finite Book price debt")
    debt = positive(Q(price0)-Q(priceplus))+positive(Q(price0)-Q(priceminus))
    require(debt<=2*err/kap,"both actual Book debts accounted")
    require(debt/(gm*t)<=2*err/(kap*gm*t),
            "endogenous code error contribution to Euler")
    require(Q(source_bound)>=0,"declared source bound")
    COUNTS["MDL_code_alignment"]+=1


def book_scalar_gradients():
    """Exact rational differentiation of the OWNED one-report full Book
    -r ln(1-zeta+zeta (1-dq)^2). No float finite differences needed.
    """
    z=Q(1,2**20)
    rate=Q(4)
    d=Q(3,2)
    q=Q(1,5)
    s=1-d*q
    A=1-z+z*s*s
    first=2*rate*z*d*s/A
    second=2*rate*z*d*d*(z*s*s-(1-z))/(A*A)
    require(0<z<Q(1,2) and 0<s<1 and 0<d*q<1,"literal Book regular collar")
    require(first>0 and second<0,"native full-Book j(q) increases and is concave")
    require(-second>0 and A>0, "strict nonzero source and finite return")
    COUNTS["native_Book_derivatives"]+=1
    return str(first), str(second)


def main():
    for a,b,c,n,decay in product(
        [-2,-1,0,1,2], [-3,-1,0,1,3], [-1,0,2],
        [5,17,101], [0,16]):
        t=Q(1,n)
        gm=Q(1,2**decay)
        A=Q(a); B=Q(b); C=Q(c)
        b0=Q(100)
        bp=b0+gm*(A*t+B*t*t+C*t*t*t)
        bm=b0+gm*(-A*t+B*t*t-C*t*t*t)
        check_fork(b0,bp,bm,gm,t,A,abs(C)*t*t,2*abs(B),0)

    # A true stationary saddle: cheaper competitors at quadratic order
    # DO NOT imply a nonzero first Euler row.
    saddle=[]
    for n in [10,100,1000,10000]:
        t=Q(1,n); gm=Q(1,2**30);b0=Q(2)
        b=b0-2*gm*t*t
        info=check_fork(b0,b,b,gm,t,0,0,4,0)
        require(info["book_undershoot"]/(gm*t)==4*t,
                "quadratic saddle Book debt is o(t) even if not a minimum")
        saddle.append(str(info["bound"]))
    COUNTS["hostile_controls"]+=1

    # Secant-only is insufficient. Both alternatives are more costly
    # while having a nonzero centered source, because curvature diverges.
    t=Q(1,100)
    b0=Q(0)
    bp=1+t
    bm=1-t
    require(bp>b0 and bm>b0 and (bp-bm)/(2*t)==1,
            "hostile secant-only smooth-source inference fails")
    require(bp+bm-2*b0==2,
            "second difference NOT uniformly O(t²)")
    COUNTS["hostile_controls"]+=1

    # Equal full stage/gate inventory is NOT native D_min-to-Book fidelity.
    t=Q(1,100); gm=Q(1,2**20); b0=Q(2)
    bp=b0+gm*t
    bm=b0-gm*t
    lengths=[21,21,21]
    require(len(set(lengths))==1 and bm<b0<bp,
            "same primitive-count description, distinct full Book price")
    kappa=1/(gm*t)
    needed=max(abs((lengths[i]-lengths[0])-kappa*(v-b0))
               for i,v in [(1,bp),(2,bm)])
    require(needed==1,"zero gate-count gap forces non-small code/Book order error")
    COUNTS["hostile_controls"]+=1

    # Separately PROVED integer code/Book fidelity would suffice;
    # this is a LOGICAL diagnostic, not a constructed D0 code.
    t=Q(1,100);gm=Q(1,2**20);b0=Q(100)
    bp=b0+gm*t*t
    bm=bp
    K=1/(gm*t*t)
    check_selected_code(3,4,4,b0,bp,bm,K,0,gm,t,0)
    info=check_fork(b0,bp,bm,gm,t,0,0,2,0)
    require(info["bound"]==t,"stationary nonnegative curvature fork")
    COUNTS["hostile_controls"]+=1

    jp,jpp=book_scalar_gradients()
    print(json.dumps({
        "status":"PASS_EXACT_RATIONAL_DMIN_THREE_PAID_WORD_TO_EULER_FORK",
        "checks":sum(COUNTS.values()),
        "groups":COUNTS,
        "sample_nonzero_Book_source":jp,
        "sample_strict_negative_Book_curvature":jpp,
        "saddle_Euler_bound_tends_to_zero":saddle,
        "scope":"universal algebraic fork; actual same-task Book-code "
                "price ordering and uniformly admitted native execution OPEN",
        "GR_closed":False,
        "physical_Dmin_Book_price_order_selected":False
    },sort_keys=True,indent=2))


if __name__=="__main__":
    main()
