"""Exact finite-product variance checks and a certified literal H.1 threshold.

Run with Python 3.9+ using only the standard library. The JSON is on stdout.
"""
import json
from fractions import Fraction as Q
from itertools import product
from math import prod


def check(condition, message):
    if not condition:
        raise ArithmeticError(message)


def mean(weights, values):
    return sum(weights[b] * values[b] for b in weights)


def probabilities(q):
    return {b: prod(x if digit else 1-x for digit, x in zip(b, q))
            for b in product((0, 1), repeat=len(q))}


def moments(q, table):
    weights = probabilities(q)
    v = [x*(1-x) for x in q]
    base = mean(weights, table)
    variance = mean(weights, {b: (t-base)**2 for b, t in table.items()})
    diff = []
    for i, x in enumerate(q):
        e1 = sum(weights[b]*t for b, t in table.items() if b[i]) / x
        e0 = sum(weights[b]*t for b, t in table.items() if not b[i]) / (1-x)
        diff.append(e1-e0)
        shock = Q(1, 100)
        q_next = list(q)
        q_next[i] += shock
        check(mean(probabilities(q_next), table)-base == shock * diff[-1],
              "exact single-coordinate derivative of fixed table")
    linear = {b: sum(d*(b[i]-q[i]) for i, d in enumerate(diff)) for b in table}
    first = sum(w*d*d for w, d in zip(v, diff))
    check(mean(weights, linear) == 0, "first layer centered")
    check(mean(weights, {b: y*y for b, y in linear.items()}) == first,
          "first-layer variance")
    residue = {b: table[b]-base-linear[b] for b in table}
    check(variance-first == mean(weights, {b: r*r for b, r in residue.items()}),
          "orthogonal decomposition and Bessel")
    for i in range(len(q)):
        check(sum(weights[b]*r*(b[i]-q[i]) for b, r in residue.items()) == 0,
              "residual orthogonal to each centered label")
    return weights, v, base, diff, first, variance


def check_tables():
    q = [Q(2,5), Q(3,7), Q(5,12), Q(4,9)]
    bits = list(product((0,1), repeat=len(q)))
    table = {b: Q(8)+sum((i+1)*b[i] for i in range(4))
             - 3*b[0]*b[2]+4*b[1]*b[2]*b[3] for b in bits}
    weights, v, base, derivatives, first, variance = moments(q, table)
    gains = [Q(1,3),Q(2,5),Q(5,4),Q(6,7)]
    score = {b: sum(g*(b[i]-q[i])/v[i] for i,g in enumerate(gains)) for b in bits}
    diag = sum(g*d for g,d in zip(gains, derivatives))
    check(mean(weights, score) == 0, "diagonal score centered")
    check(mean(weights, {b:(table[b]-base)*score[b] for b in bits}) == diag,
          "diagonal paid covariance identity")
    check(diag**2 <= first*sum(g*g/w for g,w in zip(gains,v)), "directional bound")
    # A finite full parameter chart with independent and common rows; primal l-infinity norm.
    jacobian = [(Q(1),Q(1,2),Q(-2)),(Q(0),Q(3),Q(1,4)),
                (Q(-2),Q(0),Q(1)),(Q(1),Q(0),Q(0))]
    covector = [sum(d*row[j] for d,row in zip(derivatives,jacobian)) for j in range(3)]
    norm = sum(abs(x) for x in covector)
    rhs_squared = first*sum(sum(abs(x) for x in row)**2/w for row,w in zip(jacobian,v))
    check(norm**2<=rhs_squared,"complete covector bound for the dual l-one norm")
    # A frozen interaction with zero first layer, even though it is a large positive cost.
    large = 10**6
    interaction = {b: large*(1+(b[0]-q[0])*(b[1]-q[1])) for b in bits}
    _,_,_,d_interaction,first_interaction,var_interaction = moments(q,interaction)
    check(min(interaction.values())>0 and first_interaction==0
          and not any(d_interaction) and var_interaction == large**2*v[0]*v[1],
          "large pure interaction")
    # Positivity threshold is sharp on the true direction. Check its algebra on a
    # rational proxy slope; the exact literal slope is enclosed separately below.
    x, slope, count = Q(2,5),Q(3,11),5
    all_q = [x]*count
    cancelling = {b: 10-slope*sum(b) for b in probabilities(all_q)}
    _,_,_,d_cancel,first_cancel,_=moments(all_q,cancelling)
    check(first_cancel/count==x*(1-x)*slope*slope and sum(d_cancel)==-count*slope,
          "Cauchy equality and exact slope cancellation")
    # A field-dependent cost common to all leaves has no first layer but a direct derivative.
    drift = Q(17,3)
    shifted = {b:table[b]+drift for b in bits}
    check(moments(q,shifted)[4]==first and mean(weights,shifted)-base==drift,
          "a common moving cost needs its own derivative")
    return dict(finite_rational_chart=dict(q=list(map(str,q)),
                tariff_mean=str(base),conditional_derivatives=list(map(str,derivatives)),
                first_layer_variance=str(first),full_variance=str(variance),
                exact_diagonal_score=str(diag),full_dual_norm=str(norm),
                full_norm_bound_squared=str(rhs_squared)),
                high_variance_positive_tariff=dict(n_labels=4,
                full_variance=str(var_interaction),first_layer_variance="0",
                all_first_derivatives_zero=True),
                cancellation_boundary_verified=True,common_moving_cost_checked=True)


def mul(u,v):
    a,b=u
    c,d=v
    return a*c+b*d, a*d+b*c-b*d   # p^2 = 1-p


def sign(u):
    # 2(a+bp)=(2a-b)+b sqrt(5); resolve opposite signs by exact squaring.
    a,b=u
    x=2*a-b
    if b==0:
        return (x>0)-(x<0)
    if x*b>=0:
        return 1 if b>0 else -1
    det=x*x-5*b*b
    return ((det>0)-(det<0)) * (1 if x>0 else -1)


def log_bounds(x):
    check(x>1,"positive atanh log input")
    t=(x-1)/(x+1)
    n=32
    s=2*sum(t**(2*k+1)/(2*k+1) for k in range(n))
    return s,s+2*t**(2*n+1)/((2*n+1)*(1-t*t))


def strings(lo,hi,places=15):
    scale=10**places
    def rounded(integer):
        whole,rest=divmod(integer,scale)
        return str(whole)+"."+str(rest).zfill(places)
    return [rounded((lo*scale)//1),rounded(-((-hi*scale)//1))]


def literal():
    # T_512(2p-1) from nine squarings in Z[p].
    t=(-1,2)
    for _ in range(9):
        a,b=mul(t,t)
        t=(2*a-1,2*b)
    p10=(1,0)
    for _ in range(10):
        p10=mul(p10,(0,1))
    a,b=mul(p10,(1-t[0],-t[1]))
    qstar=(1+2*a,-1+2*b)  # q* = p^2+2 p^10 [1-T_512(2p-1)].
    lo=Q("0.41246988056855516190")
    hi=Q("0.41246988056855516191")
    check(sign((qstar[0]-lo,qstar[1]))>0 and sign((qstar[0]-hi,qstar[1]))<0,
          "literal algebraic point enclosed")
    pl=Q("1.61803398874989484820")
    ph=Q("1.61803398874989484821")
    check(pl**2-pl-1<0<ph**2-ph-1,"golden ratio enclosed")
    ell_low,ell_high=log_bounds(pl)[0],log_bounds(ph)[1]
    odds_low,odds_high=(1-hi)/hi,(1-lo)/lo
    h_low,h_high=log_bounds(odds_low)[0]/ell_high,log_bounds(odds_high)[1]/ell_low
    dlow,dhigh=1-h_high,1-h_low
    check(0<dlow<=dhigh and 0<lo<hi<Q(1,2),"positive literal margin")
    # v=q(1-q) is increasing on this collar.
    low,high=lo*(1-lo)*dlow**2,hi*(1-hi)*dhigh**2
    return dict(q_star=strings(lo,hi,19),
                parsed_net_slope=strings(dlow,dhigh),
                variance_per_report_threshold=strings(low,high),
                exact_threshold="q*(1-q)*(1-log((1-q)/q)/log(phi))^2 at the literal q_star",
                enclosure="exact Z[p] comparisons and rational positive atanh tails")


if __name__=="__main__":
    print(json.dumps(dict(checks=check_tables(),literal=literal(),status="PASS",
                          physical_leaf_tariff_measured=False,GR_closed=False),indent=2))
