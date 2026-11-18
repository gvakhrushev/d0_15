"""Check finite positive-weight pressure on a complete Bernoulli archive.

The current H.1 parsed bit and the older Doob return mark are separate tests.
Uses the Python standard library and the sibling variance certificate.
"""
from fractions import Fraction as Q
from itertools import combinations
import json
from math import comb, prod
from pathlib import Path
from runpy import run_path

# Reads the source directly, including when run with -I from another directory.
helper = run_path(str(Path(__file__).with_name("check_tariff_variance.py")))
probabilities = helper["probabilities"]
mean = helper["mean"]
check = helper["check"]


def tilt(q, weights):
    mu = probabilities(q)
    z = mean(mu, weights)
    check(all(value > 0 for value in weights.values()), "strictly positive weights")
    nu = {b: mass*weights[b]/z for b, mass in mu.items()}
    check(sum(nu.values()) == 1, "normalized weighted law")
    v = [x*(1-x) for x in q]
    marginal = [sum(mass*b[i] for b, mass in nu.items()) for i in range(len(q))]
    shift = [n-x for n, x in zip(marginal, q)]
    k = sum(delta**2/var for delta,var in zip(shift,v))
    density = {b: weights[b]/z-1 for b in mu}
    residual = {b: density[b]-sum(shift[i]*(b[i]-x)/v[i] for i,x in enumerate(q))
                for b in mu}
    chi2 = mean(mu, {b: value**2 for b,value in density.items()})
    check(chi2 == k + mean(mu,{b: value**2 for b,value in residual.items()}),
          "exact Bessel identity for density minus one")
    return mu,nu,z,v,shift,k,chi2


def derivative_at_zero(values,h):
    # Exact Lagrange derivative on the equispaced nodes for polynomials of degree <= d.
    degree = len(values)-1
    return sum((-1)**(i+1)*comb(degree,i)*(values[i]-values[0])/(i*h)
               for i in range(1,degree+1))


def general_test():
    q = [Q(2,5), Q(3,7), Q(5,12), Q(4,9)]
    bits = probabilities(q)
    weights = {b: Q(3)+2*b[1]+3*b[0]*b[2]+b[0]*b[1]*b[3] for b in bits}
    mu,nu,z,v,delta,k,chi2 = tilt(q,weights)
    gains = [Q(1,3),Q(-2,5),Q(5,4),Q(6,7)]
    h = Q(1,2000)
    linear = sum(d*g/var for d,g,var in zip(delta,gains,v))
    degree = len(q)
    partition = []
    moving = []
    # A known field direction of each absolute weight, positive throughout the fixture.
    dw = {b: Q(1,3)+Q(5,2)*b[1]-b[2] for b in bits}
    for i in range(degree+2):
        t = i*h
        path = probabilities([x+t*g for x,g in zip(q,gains)])
        partition.append(mean(path,weights))
        moving.append(mean(path,{b:weights[b]+t*dw[b] for b in bits}))
    check(derivative_at_zero(partition[:degree+1],h)/z == linear,
          "fixed-weight normalized log-partition derivative")
    score = {b: sum(g*(b[i]-x)/v[i] for i,(x,g) in enumerate(zip(q,gains))) for b in bits}
    check(mean(nu,score)==linear and mean(mu,score)==0,"signed paid score")
    check(linear**2<=k*sum(g*g/var for g,var in zip(gains,v)),"directional pressure bound")
    movement = mean(nu,{b:dw[b]/weights[b] for b in bits})
    check(derivative_at_zero(moving,h)/z == linear+movement,"moving-weight source")
    scaled = {b:5*value for b,value in weights.items()}
    _,nu2,z2,*_ = tilt(q,scaled)
    check(nu2==nu and z2==5*z, "one common absolute scale invisible to marginals")
    # Any moving common scale s(t) multiplies the full Z(t) while preserving nu at every t.
    scaled_path = [(5+3*i*h)*value for i,value in enumerate(partition)]
    check(derivative_at_zero(scaled_path,h)/z2 == linear+Q(3,5),
          "common moving scale contributes its full log derivative")
    return dict(fixed_partition=str(z), baseline_probabilities=list(map(str,q)),
                paid_marginal_shifts=list(map(str,delta)),
                marginal_discrepancy_K=str(k), full_chi_squared=str(chi2),
                fixed_log_Z_direction=str(linear),moving_weight_correction=str(movement),
                common_moving_scale_log_derivative="3/5")


def connected_test():
    q = [Q(2,5),Q(3,7),Q(5,12),Q(4,9)]
    bits = probabilities(q)
    # q values here are frozen constants in the weight. Change only the trial law when differentiating.
    weights = {b: 2+prod(b[i]-x for i,x in enumerate(q)) for b in bits}
    mu,nu,z,v,delta,k,chi2 = tilt(q,weights)
    check(mu!=nu and not any(delta) and k==0 and chi2==prod(v)/4>0,
          "invisible connected weight, nontrivial complete measure")
    for size in range(1,len(q)):
        for subset in combinations(range(len(q)),size):
            for b in bits:
                event = [s for s in bits if all(s[i]==b[i] for i in subset)]
                check(sum(mu[s] for s in event)==sum(nu[s] for s in event),
                      "proper marginal of pure connected weight")
    return dict(number_of_marks=len(q),partition=str(z),marginal_discrepancy_K="0",
                complete_chi_squared=str(chi2),all_proper_marginals_agree=True,
                complete_measures_differ=True)


def scalar_return():
    # One rational informative return fixture. This bit is the earlier born-return projector,
    # with terminal 1 on return and 1-z on nonreturn, not the H.1 noisy parser.
    qr,zeta=Q(5,13),Q(1,19)
    _,nu,z,v,delta,k,chi2=tilt([qr],{(1,):Q(1),(0,):1-zeta})
    expected=1-zeta+zeta*qr
    check(z==expected and nu[(1,)]==qr/expected,"supplied Doob return terminal")
    check(delta[0]==zeta*v[0]/expected and delta[0]/v[0]==zeta/expected,
          "old positive log normalizer source and mark shift")
    check(k==chi2,"binary one-mark Bessel equality")
    return dict(return_probability=str(qr),zeta=str(zeta),weighted_return=str(nu[(1,)]),
                mark_shift=str(delta[0]),log_Z_derivative_wrt_return=str(zeta/expected),
                pressure_derivative="minus the log-Z derivative divided by log(phi)",
                return_mark_distinct_from_H1_parsed_report=True)


def sharp_boundary():
    # In scaled units a=ell P', an independently tilted positive product
    # with marginal n=x+a*v saturates the K-bound for a common field direction.
    x=Q(2,5)
    a=Q(1,8)
    v=x*(1-x)
    n=x+a*v
    count=4
    q=[x]*count
    mu=probabilities(q)
    model=probabilities([n]*count)
    weights={b:model[b]/mu[b] for b in mu}
    _,nu,z,_,shift,k,_=tilt(q,weights)
    check(z==1 and nu==model and all(d==a*v for d in shift),"positive tilted product")
    check(k/count==a*a*v and sum(d/v for d in shift)==count*a,
          "sharp pressure cancellation boundary in scaled units")
    return dict(real_positive_table_boundary_verified=True,common_shift=str(n-x))


def literal_threshold():
    # Recompute the sibling exact Z[p] bound (the JSON receipt is not used).
    source=helper["literal"]()
    ql,qh=map(Q,source["q_star"])
    dl,dh=map(Q,source["parsed_net_slope"])
    pl,ph=Q("1.61803398874989484820"),Q("1.61803398874989484821")
    check(pl**2-pl-1<0<ph**2-ph-1 and qh<Q(1,2) and dl>0,"input domains")
    el=helper["log_bounds"](pl)[0]
    eh=helper["log_bounds"](ph)[1]
    low=el**2*ql*(1-ql)*dl**2
    high=eh**2*qh*(1-qh)*dh**2
    return dict(exact_formula="log(phi)^2*q*(1-q)*P_prime(q)^2, at the literal q_star",
                marginal_discrepancy_per_mark_threshold=helper["strings"](low,high),
                q_star=source["q_star"],parsed_net_slope=source["parsed_net_slope"],
                terminal_pressure_units="minus log(Z)/log(phi)")


if __name__=="__main__":
    print(json.dumps(dict(status="PASS",general=general_test(),higher_order=connected_test(),
                          return_control=scalar_return(),boundary=sharp_boundary(),
                          literal=literal_threshold(),physical_weighted_law_supplied=False,
                          GR_closed=False),indent=2))
