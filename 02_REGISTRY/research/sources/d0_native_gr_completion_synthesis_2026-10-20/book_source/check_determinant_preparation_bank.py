#!/usr/bin/env python3
"""Exact controls for the conditional Golden preparation-bank composition.

This reuses the owned heralded fair seed and the two-query determinant map.
It does not prove the original 8D query, AND/OR compiler, required future task,
physical Book03 Info, or a complete primitive measurement/routing price.
The rational leaf examples use a declared gate ledger, canonical ready slots,
one identical post-ready query price, and a field independent of preparation
delay. All preparation records, aborts and unresolved query records remain.
Only the standard library is used. Checks remain active under python -O.
"""
from dataclasses import dataclass
from fractions import Fraction as Q
import json


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


# Exact Q[a]/(a^4+a^2-1); the intended real embedding has a>0 and p=a^2.
def element(*coefficients):
    return tuple(Q(x) for x in coefficients) + (Q(0),) * (4-len(coefficients))


ZERO, ONE, A = element(0), element(1), element(0, 1)


def add(x, y):
    return tuple(u+v for u, v in zip(x, y))


def scale(x, c):
    return tuple(Q(c)*u for u in x)


def mul(x, y):
    coefficients = [Q(0)] * 7
    for i, u in enumerate(x):
        for j, v in enumerate(y):
            coefficients[i+j] += u*v
    for degree in range(6, 3, -1):
        coefficients[degree-4] += coefficients[degree]
        coefficients[degree-2] -= coefficients[degree]
    return tuple(coefficients[:4])


def power(x, n):
    require(isinstance(n, int) and n >= 0, "nonnegative ring exponent")
    value = ONE
    while n:
        if n % 2:
            value = mul(value, x)
        x = mul(x, x)
        n //= 2
    return value


def ring_sum(values):
    value = ZERO
    for item in values:
        value = add(value, item)
    return value


P = power(A, 2)
G = ((A, scale(P, -1)), (P, A))
GT = tuple(zip(*G))


def gate(state, target, matrix):
    """Three qubits, basis index ABC; target 0,1,2 denotes A,B,C."""
    output = [ZERO] * 8
    mask = 1 << (2-target)
    for source, amplitude in enumerate(state):
        column = int(bool(source & mask))
        for row in range(2):
            destination = (source & ~mask) | (row*mask)
            output[destination] = add(
                output[destination], mul(matrix[row][column], amplitude))
    return output


def cnot(state, control, target):
    output = [ZERO] * 8
    for source, amplitude in enumerate(state):
        destination = source
        if source & (1 << (2-control)):
            destination ^= 1 << (2-target)
        output[destination] = amplitude
    return output


def basis(index):
    state = [ZERO] * 8
    state[index] = ONE
    return state


def norm(state):
    return ring_sum(power(x, 2) for x in state)


def exact_seed_and_bank():
    require(add(P, power(P, 2)) == ONE, "Golden p+p^2=1")
    ap, p2 = mul(A, P), power(P, 2)
    success = scale(power(P, 3), 2)
    failure = add(ONE, scale(success, -1))
    for inverse in (False, True):
        state = gate(gate(basis(0), 0, G), 1, GT if inverse else G)
        state = cnot(cnot(cnot(state, 0, 2), 1, 2), 0, 1)
        expected = [ZERO] * 8
        expected[0] = P
        expected[3] = scale(ap, -1 if inverse else 1)
        expected[7] = ap
        expected[4] = scale(p2, -1 if inverse else 1)
        require(state == expected, "all eight seed amplitudes and signs")
        require(norm(state) == ONE, "complete seed normalization")
        heralded = [x if i & 1 else ZERO for i, x in enumerate(state)]
        require(norm(heralded) == success, "herald probability is 2p^3")
        require(norm([x if not i & 1 else ZERO for i, x in enumerate(state)])
                == failure, "retained failure norm")
        require(power(state[3], 2) == power(state[7], 2),
                "conditional A is fair, with both B and C equal to one")
        require(all(x == ZERO for i, x in enumerate(heralded) if i not in (3, 7)),
                "heralded known-one byproducts")

    # A retained known-one B supplies X on A without changing that control.
    for index in (2, 6):
        state = cnot(gate(cnot(basis(index), 1, 0), 0, G), 1, 0)
        require(state == gate(basis(index), 0, GT), "known-one XGX equals G transpose")

    # A fair normalized conditional state does not assert a free fair unitary.
    # R_K=s sum_{j<K} r^j; consequently R_K/2 lies in Z[a].
    for cap in (1, 2, 3, 8):
        ready = add(ONE, scale(power(failure, cap), -1))
        series = ring_sum(power(failure, j) for j in range(cap))
        require(ready == mul(success, series), "exact finite-cap telescoping")
        require(scale(ready, Q(1, 2)) == mul(power(P, 3), series),
                "R_K/2=p^3 sum r^j")
        require(all(x.denominator == 1 for x in scale(ready, Q(1, 2))),
                "heralded half-probability is algebraically integral")
        require(ready != ONE, "finite cap has retained nonzero abort probability")

    # The positive root lies between these rationals, by monotonicity of
    # x^2+x-1 for x>0. This proves 0<r<rho without floating arithmetic.
    lo, hi, rho = Q(618, 1000), Q(619, 1000), Q(53, 100)
    require(lo*lo+lo-1 < 0 < hi*hi+hi-1, "rational Golden root enclosure")
    require(0 < 1-2*hi**3 < 1-2*lo**3 < rho, "0<r<53/100")
    cases = []
    for attempts in (1, 2, 7, 100):
        resources = 42*attempts  # Two +/- inputs and two twenty-fair-qubit coins.
        cap = 1
        while resources*rho**cap > Q(1, 2):
            cap += 1
        error = rho**cap
        require(resources*error <= Q(1, 2), "selected cap has union error <=1/2")
        require((1-error)**resources >= 1-resources*error >= Q(1, 2),
                "Bernoulli lower bound for the all-ready bank")
        cases.append({"N": attempts, "m": resources, "K": cap})
    # The all-m implication uses the same Bernoulli inequality
    # (1-x)^m >= 1-mx, 0<=x<=1; these finite cases exercise cap selection.
    return cases


@dataclass(frozen=True)
class Prep:
    probability: Q
    record: tuple
    ready: bool
    successes: int
    failures: int
    cost: Q


def preparation_leaves(s, cap, trial_costs):
    """Every first-success trial record; abort immediately after a capped failure."""
    r = 1-s
    leaves = []

    def extend(record, probability, successes, failures, cost):
        resource = len(record)
        if resource == len(trial_costs):
            # Declared field-independent routing to canonical output slots.
            # Delays/prices differ by transcript, but the subsequent query does not.
            routing_cost = Q(1+sum(n*n for n in record))
            leaves.append(Prep(probability, record, True, successes, failures, cost+routing_cost))
            return
        for n in range(1, cap+1):
            extend(record+(n,), probability*s*r**(n-1), successes+1,
                   failures+n-1, cost+n*trial_costs[resource])
        leaves.append(Prep(probability*r**cap, record+("abort",), False,
                           successes, failures+cap, cost+cap*trial_costs[resource]))

    extend((), Q(1), 0, 0, Q(0))
    return leaves


@dataclass(frozen=True)
class Leaf:
    probability: Q
    jet: Q
    cost: Q
    powers: tuple  # Exponents of (s, 1-s, q, 1-q) in its actual mass.
    prep_record: tuple
    query_record: str
    ready: bool


def complete_leaves(preparation, q, query_cap, query_cost):
    leaves = []
    d = 1-q
    for prep in preparation:
        if not prep.ready:
            leaves.append(Leaf(prep.probability, Q(0), prep.cost,
                               (prep.successes, prep.failures, 0, 0),
                               prep.record, "not-started", False))
            continue
        for failed in range(query_cap):
            weight = q**failed*d
            jet = -q**failed
            if failed:
                jet += failed*q**(failed-1)*d
            leaves.append(Leaf(prep.probability*weight, prep.probability*jet,
                               prep.cost+(failed+1)*query_cost,
                               (prep.successes, prep.failures, failed, 1),
                               prep.record, "F"*failed+"S", True))
        leaves.append(Leaf(prep.probability*q**query_cap,
                           prep.probability*query_cap*q**(query_cap-1),
                           prep.cost+query_cap*query_cost,
                           (prep.successes, prep.failures, query_cap, 0),
                           prep.record, "F"*query_cap+" (unresolved)", True))
    return leaves


def aggregate(leaves):
    return {
        "mass": sum((x.probability for x in leaves), Q(0)),
        "mass_jet": sum((x.jet for x in leaves), Q(0)),
        "cost": sum((x.probability*x.cost for x in leaves), Q(0)),
        "cost_jet": sum((x.jet*x.cost for x in leaves), Q(0)),
        "entropy_logs": tuple(-sum((x.probability*x.powers[i] for x in leaves), Q(0))
                              for i in range(4)),
        "entropy_jet_logs": tuple(-sum((x.jet*x.powers[i] for x in leaves), Q(0))
                                  for i in range(4)),
    }


def expect_rejection(check, message):
    try:
        check()
    except RuntimeError as exc:
        require(str(exc) == message, "hostile control failed for an unintended reason")
        return message
    raise RuntimeError("hostile control was incorrectly accepted")


def finite_leaf_control(s, q, cap, query_cap):
    # 5 and 7 are declared gate-ledger fixture costs (including XGX overhead).
    # They are not asserted to price real measurements, reset, routing or clocks.
    trial_costs, query_cost = (Q(5), Q(7)), Q(11)
    prep = preparation_leaves(s, cap, trial_costs)
    leaves = complete_leaves(prep, q, query_cap, query_cost)
    total = aggregate(leaves)
    r, ready = 1-s, 1-(1-s)**cap
    alpha = ready**len(trial_costs)
    expected_prep_trials = sum((r**j for j in range(cap)), Q(0))
    pre_cost = sum((p.probability*p.cost for p in prep), Q(0))
    route_cost = sum((p.probability*(1+sum(n*n for n in p.record))
                      for p in prep if p.ready), Q(0))
    require(pre_cost == route_cost+expected_prep_trials*
            sum((ready**i*c for i, c in enumerate(trial_costs)), Q(0)),
            "complete preparation clock includes aborted trials and ready routing")
    require(sum((p.probability for p in prep), Q(0)) == 1, "complete preparation mass")
    require(sum((p.probability for p in prep if p.ready), Q(0)) == alpha,
            "all-ready probability (1-r^K)^m")
    query_rounds = sum((q**j for j in range(query_cap)), Q(0))
    query_rounds_jet = sum((j*q**(j-1) for j in range(1, query_cap)), Q(0))
    require(total["mass"] == 1 and total["mass_jet"] == 0, "complete leaf mass and jet")
    require(total["cost"] == pre_cost+alpha*query_cost*query_rounds,
            "complete clock is preparation plus alpha times query clock")
    require(total["cost_jet"] == alpha*query_cost*query_rounds_jet,
            "field-independent preparation leaves the alpha-weighted clock source")

    prep_entropy = tuple(-sum((p.probability*(p.successes if i == 0 else p.failures)
                               for p in prep), Q(0)) for i in range(2))
    prep_rounds = expected_prep_trials*sum((ready**i for i in range(len(trial_costs))), Q(0))
    require(prep_entropy == (-s*prep_rounds, -r*prep_rounds),
            "preparation entropy retains every success-trial and abort record")
    expected_entropy = prep_entropy+(-alpha*q*query_rounds, -alpha*(1-q)*query_rounds)
    expected_jet = (Q(0), Q(0), -alpha*(query_rounds+q*query_rounds_jet),
                    alpha*(query_rounds-(1-q)*query_rounds_jet))
    require(total["entropy_logs"] == expected_entropy, "full entropy chain-rule coefficients")
    require(total["entropy_jet_logs"] == expected_jet, "full entropy first-source coefficients")
    # d(-P log P)=-P' log P-P'/ln(phi). The non-logarithmic term sums to zero.
    require(sum((x.probability*(Q(x.powers[2], 1)/q-Q(x.powers[3], 1)/(1-q))
                 for x in leaves), Q(0)) == total["mass_jet"] == 0,
            "normalizer derivative cancels the constant entropy-jet term")
    full_source = (total["cost_jet"],)+tuple(-x for x in total["entropy_jet_logs"])
    query_source = (query_cost*query_rounds_jet, Q(0), Q(0),
                    query_rounds+q*query_rounds_jet,
                    -query_rounds+(1-q)*query_rounds_jet)
    require(full_source == tuple(alpha*x for x in query_source),
            "complete Cost-minus-Info first source is alpha times the query source")
    # Hence, coefficient by coefficient, S=S_prep+alpha*S_query and
    # dS=alpha*dS_query. The owned query identifies dS_query=c*dJ2;
    # that determinant/source theorem is an input, not re-proved here.

    only_ready = [x for x in leaves if x.ready]
    dropped = aggregate(only_ready)
    require(dropped["mass"] == alpha < 1, "strict missing abort mass")
    lost_abort = expect_rejection(
        lambda: require(dropped["mass"] == 1, "dropping preparation aborts loses normalization"),
        "dropping preparation aborts loses normalization")
    conditioned_cost_jet = dropped["cost_jet"]/alpha
    lost_alpha = expect_rejection(
        lambda: require(conditioned_cost_jet == total["cost_jet"],
                        "conditioning on all-ready loses the alpha source factor"),
        "conditioning on all-ready loses the alpha source factor")
    return {
        "s": str(s), "q": str(q), "K": cap, "N": query_cap,
        "prep_leaves": len(prep), "complete_leaves": len(leaves),
        "alpha": str(alpha), "cost": str(total["cost"]),
        "cost_jet": str(total["cost_jet"]), "hostile_controls": [lost_abort, lost_alpha],
        "price_jet_coefficients_constant_log_s_log_r_log_q_log_1minusq": [str(x) for x in full_source],
    }


def main():
    banks = exact_seed_and_bank()
    leaves = [finite_leaf_control(Q(2, 7), Q(3, 5), 2, 3),
              finite_leaf_control(Q(3, 5), Q(2, 7), 3, 2)]
    print(json.dumps({
        "exact_ring": "Q[a]/(a^4+a^2-1)",
        "seed": "all 8 amplitudes, both signs, complete norms and retained XGX control",
        "bank_bound": "m=42N; choose m*(53/100)^K<=1/2; alpha>=(1-(53/100)^K)^m>=1/2",
        "bank_examples": banks,
        "complete_leaf_controls": leaves,
        "composition": "D S_total=alpha*c*D J2, conditional on the owned common post-ready query",
        "retained_assumptions": [
            "Canonical resource slots and transcript-independent post-ready word and cost",
            "Field/readout stationary through the variable preparation delay",
            "All preparation/controller/routing costs and source independence as declared",
            "Actual 8D query, AND/OR and primitive admission remain inputs",
            "Physical Book03 Info and compulsory future task remain unproved",
        ],
        "status": "PASS: conditional resource composition only",
    }, indent=2))


if __name__ == "__main__":
    main()
