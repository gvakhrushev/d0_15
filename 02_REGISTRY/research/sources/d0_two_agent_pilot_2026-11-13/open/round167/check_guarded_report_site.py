"""Exact guarded REPORT trees and independent coherent SITE averaging."""

from fractions import Fraction as Q
from itertools import product
import json
from pathlib import Path
import subprocess

import sympy as sp


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[5]
PILOT = HERE.parents[1].relative_to(REPO)
B162 = "1d47593adde9f4a472ad9c7c151d74160e317f82"


def require(condition, label):
    if not condition:
        raise ArithmeticError(label)


def check_tree(field, p, outer_cap, service_cap, attenuators, pair, copy_count):
    one = field.one
    q = pair[0]**2
    cross = pair[0]*pair[1]
    off = Q(1,37)
    eta = Q(8,9)
    f = (1-eta)**service_cap
    g = (1-off)*(1-f)
    beta = 2*q*(1-q)
    alpha = 1-beta
    printed = copy_count > 0
    report_weights = (p**4,p**7) if printed else (p,p*p)
    guard_weights = report_weights
    coarse_service = p**8 if printed else p*p
    coarse_other = p**11 if printed else p**3
    report = (
        lambda vec: ((1-q)*vec[0]-cross*vec[1],-cross*vec[0]+q*vec[1]),
        lambda vec: (q*vec[0]+cross*vec[1],cross*vec[0]+(1-q)*vec[1]),
    )
    leaves = []

    def visit(vector, passive, born, depth):
        for bit, operation in enumerate(report):
            state = operation(vector)
            weight = passive*report_weights[bit]
            if depth == 0 and printed:
                weight *= p**(copy_count*(3+2*bit))*p**(2*copy_count*(1-bit))
            leaves.append(("service", state, weight*guard_weights[0], born*off))
            measure(state, weight*guard_weights[1]*p**attenuators, born*(1-off), depth)

    def measure(state, passive, born, depth):
        for _ in range(service_cap):
            hit = (state[0], Q(0))
            miss = (Q(0), state[1])
            leaves.append(("success", hit, passive*coarse_other, born*eta))
            if depth == outer_cap-1:
                leaves.append(("overflow", miss, passive*coarse_other, born*eta))
            else:
                visit(miss, passive*coarse_other, born*eta, depth+1)
            passive, born = passive*coarse_service, born*(1-eta)
        leaves.append(("service", state, passive, born))

    def exact(rational):
        return field.convert(sp.Rational(rational.numerator, rational.denominator))

    visit((Q(1),Q(0)), one, Q(1), 0)
    compression = field.zero
    total_mass = overflow = service = Q(0)
    for kind, vector, passive, born in leaves:
        squared = vector[0]**2+vector[1]**2
        require(squared > 0 and born > 0, "fixed positive occupied rank")
        compression += passive*exact(vector[0]**2/squared)
        total_mass += born*squared
        if kind == "overflow":
            overflow += born*squared
        if kind == "service":
            service += born*squared
    loops = sum((2*service_cap)**j for j in range(outer_cap))
    require(len(leaves) == (2*service_cap+4)*loops+(2*service_cap)**outer_cap,
            "wrong complete leaf count")
    a = coarse_service**service_cap
    ell = coarse_other*sum((coarse_service**j for j in range(service_cap)),field.zero)
    y = p**attenuators
    carried = guard_weights[1]*y*ell
    aborted = guard_weights[0]+guard_weights[1]*y*a
    w0,w1 = report_weights
    active_mass = carried*(w0+w1)
    expansion = sum((active_mass**j for j in range(outer_cap)),field.zero)
    expected = p**(5*copy_count)*expansion*(active_mass+aborted*(w0-(w0-w1)*exact(q)))
    require(compression == expected, "guarded spectral compression differs")
    visits = 1+g*beta*sum((g*alpha)**j for j in range(outer_cap-1))
    require(total_mass == 1 and service == (1-g)*visits <= 2*(1-g),
            "guard/service probability or full Born sum differs")
    require(overflow == g**outer_cap*beta*alpha**(outer_cap-1), "wrong outer cap")


def check_protected_site(field,p):
    counts = []
    for bits in range(1,4):
        addresses = list(product((0,1),repeat=bits))
        # Independent finite test law and nonconstant conditional responses.
        mu = {site:p**(bits+sum(site)) for site in addresses}
        report = {site:p**(1+(sum(site)%3)) for site in addresses}
        require(sum(mu.values(),field.zero) == field.one, "PF normalized")
        expected = p**(3*bits)*sum((mu[site]*report[site] for site in addresses),field.zero)
        for old in addresses:
            value = field.zero
            for left,right in product(addresses,repeat=2):
                if any(i==j for i,j in zip(left,right)):
                    continue
                masked = tuple(i^j for i,j in zip(old,left))
                weight = p**(2*bits+sum(left)+sum(right))
                value += weight*mu[masked]*report[masked]
            require(value == expected, "protected SITE dependence")
        counts.append(len(addresses))
    return counts


def check_native_guard():
    raw = subprocess.check_output(
        ["git","show",f"{B162}:{PILOT}/open/round162/RESULT.json"],cwd=REPO)
    prior = json.loads(raw)["balanced_rotated_pointer"]
    require(prior["positive_G_power_including_birth"] == 1048, "changed native power")
    lower,upper = map(lambda x:Q(str(x)),prior["mark_contrast"])
    require(Q("7.056e-9") < lower**2 < upper**2 < Q("7.073e-9"),
            "double-angle readiness mass bound")
    return {"positive_G_power_including_birth":2096,
            "strict_Born_H_zero_bracket":["7.056e-9","7.073e-9"],
            "passive_H_zero":"p"}


def main():
    p_symbol = (sp.sqrt(5)-1)/2
    field = sp.QQ.algebraic_field(p_symbol)
    p = field.convert(p_symbol)
    cases = 0
    pairs = ((Q(3,5),Q(4,5)),(Q(5,13),Q(12,13)))
    for outer,service,tails,pair,copies in product(range(1,4),range(1,3),(0,2),pairs,(0,6,9)):
        check_tree(field,p,outer,service,tails,pair,copies)
        cases += 1
    print(json.dumps({
        "status":"PASS",
        "exact_guarded_and_attenuated_trees":cases,
        "initial_REPORT_printer_copies_in_cases":[0,6,9],
        "native_guard":check_native_guard(),
        "all_old_SITE_values_per_exact_fixture":check_protected_site(field,p),
        "unknown_SITE_constant_effect_factor":"eta_flag*p^(3*d)",
        "full_physical_Cost_minus_Info":False,
        "GR_closed":False,
    },indent=2))


if __name__ == "__main__":
    main()
