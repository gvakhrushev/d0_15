#!/usr/bin/env python3
"""Complete finite detector ledger under two declared Book bindings.

Exact rational leaf probabilities/jets and formal logarithm coefficients
verify the mean action and both different notions of first derivative.
Rational fixture probabilities are ledger controls, not native Golden gate
probabilities. No physical gain, aggregate, common normalizer or Book03
binding is selected. Standard library; all checks remain active with -O.
"""

from dataclasses import dataclass
from decimal import Decimal, localcontext
from fractions import Fraction as Q
import json

from check_determinant_preparation_bank import (
    ONE, P, ZERO, add, expect_rejection, mul, power, preparation_leaves,
    require, scale,
)


@dataclass(frozen=True)
class Stage:
    probability: Q
    ready: bool
    cost: Q
    record: str


@dataclass(frozen=True)
class Leaf:
    probability: Q
    jet: Q
    cost: Q
    powers: tuple
    terminal: str


def complete_leaves(preparation, stages, q, horizon):
    """Every prep abort, stage abort, ready report and unresolved cap word."""
    terms = len(preparation) + len(stages) + 2
    stage_offset = len(preparation)
    leaves = []

    def append(probability, cost, counts, terminal):
        score = Q(counts[-2]) / q - Q(counts[-1]) / (1 - q)
        leaves.append(Leaf(probability, probability * score, cost, tuple(counts), terminal))

    def visit(depth, probability, cost, powers):
        for index, stage in enumerate(stages):
            counts = list(powers)
            counts[stage_offset + index] += 1
            mass = probability * stage.probability
            clock = cost + stage.cost
            if not stage.ready:
                append(mass, clock, counts, "gate-abort")
                continue
            for continued in (False, True):
                report_counts = counts.copy()
                report_counts[-2 if continued else -1] += 1
                report_mass = mass * (q if continued else 1 - q)
                if continued and depth + 1 < horizon:
                    visit(depth + 1, report_mass, clock, tuple(report_counts))
                else:
                    append(report_mass, clock, report_counts,
                           "unresolved-horizon" if continued else "ready-no-click")

    for index, prep in enumerate(preparation):
        counts = [0] * terms
        counts[index] = 1
        if prep.ready:
            visit(0, prep.probability, prep.cost, tuple(counts))
        else:
            append(prep.probability, prep.cost, counts, "prep-abort")
    return leaves


def vector_zero(terms):
    # Slots are constant, 1/log(phi), then coefficients of log_phi(atoms).
    return (Q(0),) * (terms + 2)


def vector_sum(vectors, terms):
    result = vector_zero(terms)
    for vector in vectors:
        result = tuple(a + b for a, b in zip(result, vector))
    return result


def vscale(vector, value):
    return tuple(value * item for item in vector)


def vadd(left, right):
    return tuple(a + b for a, b in zip(left, right))


def decimal_fraction(value):
    return Decimal(value.numerator) / Decimal(value.denominator)


def evaluate(vector, atoms, ell):
    value = decimal_fraction(vector[0]) + decimal_fraction(vector[1]) / ell
    for coefficient, atom in zip(vector[2:], atoms):
        value += decimal_fraction(coefficient) * decimal_fraction(atom).ln() / ell
    return value


def direct_decimal_mean(leaves, atoms, q, q_new, theta, J0, Jprime, ell):
    """An independent numerical evaluation of the actual enumerated leaves."""
    result = Decimal(0)
    J = decimal_fraction(J0) + decimal_fraction(Jprime) * (q_new - decimal_fraction(q))
    for leaf in leaves:
        probability = Decimal(1)
        for index, exponent in enumerate(leaf.powers):
            atom = q_new if index == len(atoms) - 2 else 1 - q_new if index == len(atoms) - 1 else decimal_fraction(atoms[index])
            probability *= atom ** exponent
        result += probability * (-decimal_fraction(theta) * probability.ln() / ell - J)
    return result


def check_fixture(prep_success, prep_cap, stages, q, horizon, J0, Jprime):
    preparation = preparation_leaves(prep_success, prep_cap, (Q(5), Q(9)))
    require(sum((p.probability for p in preparation), Q(0)) == 1, "all prep probabilities retained")
    require(sum((t.probability for t in stages), Q(0)) == 1, "entire internal stage transcript retained")
    alpha = sum((p.probability for p in preparation if p.ready), Q(0))
    beta = sum((t.probability for t in stages if t.ready), Q(0))
    require(0 < alpha < 1 and 0 < beta < 1, "both preparation and gate aborts are genuine")
    require(len({t.cost for t in stages}) > 1, "stage costs are transcript correlated")
    ready_stage_cost = sum((t.probability * t.cost for t in stages if t.ready), Q(0)) / beta
    abort_stage_cost = sum((t.probability * t.cost for t in stages if not t.ready), Q(0)) / (1 - beta)
    require(ready_stage_cost != abort_stage_cost, "readiness and actual stage clock are correlated")
    leaves = complete_leaves(preparation, stages, q, horizon)
    atoms = [p.probability for p in preparation] + [t.probability for t in stages] + [q, 1 - q]
    terms = len(atoms)
    require(all(0 < atom < 1 for atom in atoms), "logarithm atoms have actual positive support")
    require(sum((leaf.probability for leaf in leaves), Q(0)) == 1, "full prep/stage/horizon leaf mass")
    require(sum((leaf.jet for leaf in leaves), Q(0)) == 0, "full leaf probability first jet")
    for leaf in leaves:
        reconstructed = Q(1)
        for atom, exponent in zip(atoms, leaf.powers):
            reconstructed *= atom ** exponent
        require(reconstructed == leaf.probability, "each full leaf has its actual product probability")
        require(leaf.jet == leaf.probability * (leaf.powers[-2] / q - leaf.powers[-1] / (1 - q)),
                "each full leaf first jet includes the entire chronological score")
    terminal_masses = {name: sum((leaf.probability for leaf in leaves if leaf.terminal == name), Q(0))
                       for name in ("prep-abort", "gate-abort", "unresolved-horizon", "ready-no-click")}
    require(all(mass > 0 for mass in terminal_masses.values()), "every required terminal type remains")
    require(terminal_masses["prep-abort"] == 1 - alpha, "initial bank paid exactly once")
    x = beta * q
    E = sum((x ** j for j in range(horizon)), Q(0))
    dE = beta * sum((j * x ** (j - 1) for j in range(1, horizon)), Q(0))
    require(dE > 0, "finite renewal has a nonzero field jet")
    H = (Q(0), Q(0)) + tuple(-sum((leaf.probability * leaf.powers[i] for leaf in leaves), Q(0))
                             for i in range(terms))
    DH = (Q(0), Q(0)) + tuple(-sum((leaf.jet * leaf.powers[i] for leaf in leaves), Q(0))
                              for i in range(terms))
    pre_H = (Q(0), Q(0)) + tuple(-p.probability for p in preparation) + (Q(0),) * (len(stages) + 2)
    stage_H = ((Q(0), Q(0)) + (Q(0),) * len(preparation)
               + tuple(-t.probability for t in stages) + (Q(0), Q(0)))
    binary_H = ((Q(0), Q(0)) + (Q(0),) * (len(preparation) + len(stages)) + (-q, -(1 - q)))
    binary_DH = ((Q(0), Q(0)) + (Q(0),) * (len(preparation) + len(stages)) + (Q(-1), Q(1)))
    expected_H = vadd(pre_H, vscale(vadd(stage_H, vscale(binary_H, beta)), alpha * E))
    expected_DH = vscale(vadd(vscale(vadd(stage_H, vscale(binary_H, beta)), dE),
                              vscale(binary_DH, beta * E)), alpha)
    require(H == expected_H, "H_full=H_pre+alpha*[H_T+beta*h(q)]*E_N(beta*q)")
    require(DH == expected_DH, "full entropy first source keeps internal records and renewal jet")
    prep_cost = sum((p.probability * p.cost for p in preparation), Q(0))
    stage_cost = sum((t.probability * t.cost for t in stages), Q(0))
    full_cost = sum((leaf.probability * leaf.cost for leaf in leaves), Q(0))
    full_cost_jet = sum((leaf.jet * leaf.cost for leaf in leaves), Q(0))
    require(full_cost == prep_cost + alpha * stage_cost * E, "all correlated clocks including aborts remain paid")
    require(full_cost_jet == alpha * stage_cost * dE, "actual mean clock source retained")

    # Formal coefficient identities suffice even when some logarithm atoms
    # coincide: no numerical independence of logarithms is assumed.
    bindings = []
    with localcontext() as context:
        context.prec = 85
        ell = ((Decimal(1) + Decimal(5).sqrt()) / 2).ln()
        entropy_value, entropy_source = evaluate(H, atoms, ell), evaluate(DH, atoms, ell)
        require(entropy_value > 0 and entropy_source != 0, "fixture has nonzero entropy and genuine mean source")
        for theta, label in [(Q(1, 2), "absolute amplitude"), (Q(1), "absolute scalar weight")]:
            actions, infos, path_derivatives = [], [], []
            mean_derivative_terms, mean_info_derivative_terms = [], []
            for leaf in leaves:
                # I=C+theta log_phi(P)+J; net action is -theta log_phi(P)-J.
                action = (-J0, Q(0)) + tuple(-theta * exponent for exponent in leaf.powers)
                info = (leaf.cost + J0, Q(0)) + tuple(theta * exponent for exponent in leaf.powers)
                require(vadd(action, info) == (leaf.cost, Q(0)) + (Q(0),) * terms,
                        "Book C-I cancellation is pointwise on the same priced leaf")
                score = leaf.jet / leaf.probability
                path_derivative = (-Jprime, -theta * score) + (Q(0),) * terms
                info_derivative = (Jprime, theta * score) + (Q(0),) * terms
                actions.append(vscale(action, leaf.probability))
                infos.append(vscale(info, leaf.probability))
                path_derivatives.append(vscale(path_derivative, leaf.probability))
                mean_derivative_terms.append(vadd(vscale(action, leaf.jet),
                                                  vscale(path_derivative, leaf.probability)))
                mean_info_derivative_terms.append(vadd(vscale(info, leaf.jet),
                                                       vscale(info_derivative, leaf.probability)))
            mean_action = vector_sum(actions, terms)
            mean_info = vector_sum(infos, terms)
            expected_mean = vadd(vscale(H, theta), (-J0, Q(0)) + (Q(0),) * terms)
            require(mean_action == expected_mean, "mean Book action is theta*H_full-J")
            require(vadd(mean_action, mean_info) == (full_cost, Q(0)) + (Q(0),) * terms,
                    "paid total cost equals full mean action plus mean gain")
            expected_differential = (-Jprime, Q(0)) + (Q(0),) * terms
            mean_differential = vector_sum(path_derivatives, terms)
            require(mean_differential == expected_differential, "E[dS]=-dJ; full probability score cancels")
            differential_mean = vector_sum(mean_derivative_terms, terms)
            expected_source = vadd(vscale(DH, theta), expected_differential)
            require(differential_mean == expected_source, "dE[S]=theta*dH_full-dJ")
            info_mean_jet = vector_sum(mean_info_derivative_terms, terms)
            cost_jet_vector = (full_cost_jet, Q(0)) + (Q(0),) * terms
            require(vadd(differential_mean, info_mean_jet) == cost_jet_vector,
                    "derivative of actual cost-minus-info mean retains distribution derivative")
            require(vadd(differential_mean, vscale(mean_differential, -1)) == vscale(DH, theta),
                    "differential-of-mean differs from mean-differential by theta*dH")
            source_value = evaluate(differential_mean, atoms, ell)
            averaged_differential = evaluate(mean_differential, atoms, ell)
            require(source_value != averaged_differential, "two source notions are genuinely different in this fixture")
            step = Decimal("1e-18")
            center = decimal_fraction(q)
            plus = direct_decimal_mean(leaves, atoms, q, center + step, theta, J0, Jprime, ell)
            minus = direct_decimal_mean(leaves, atoms, q, center - step, theta, J0, Jprime, ell)
            finite_difference = (plus - minus) / (2 * step)
            require(abs(finite_difference - source_value) < Decimal("1e-32"),
                    "independent high-precision full-leaf mean first derivative")
            bindings.append({"binding": label, "theta": str(theta),
                             "mean_action": str(evaluate(mean_action, atoms, ell)),
                             "mean_differential": str(averaged_differential),
                             "differential_of_mean": str(source_value),
                             "full_leaf_finite_difference": str(finite_difference)})

    # All these controls concern THIS complete tree, not a new price choice.
    kept_without_prep = sum((leaf.probability for leaf in leaves if leaf.terminal != "prep-abort"), Q(0))
    prep_rejection = expect_rejection(
        lambda: require(kept_without_prep == 1, "dropping prep aborts loses complete mass"),
        "dropping prep aborts loses complete mass")
    wrong_report_entropy = vadd(stage_H, binary_H)
    actual_report_entropy = vadd(stage_H, vscale(binary_H, beta))
    ready_rejection = expect_rejection(
        lambda: require(wrong_report_entropy == actual_report_entropy,
                        "conditional-ready report entropy loses beta"),
        "conditional-ready report entropy loses beta")
    without_stage_entropy_source = vscale(vadd(vscale(binary_H, beta * dE),
                                              vscale(binary_DH, beta * E)), alpha)
    stage_rejection = expect_rejection(
        lambda: require(without_stage_entropy_source == DH,
                        "field-independent internal entropy still has a renewal source"),
        "field-independent internal entropy still has a renewal source")
    require(Jprime != 0, "common normalizer has a genuine nonzero source")
    J_rejection = expect_rejection(
        lambda: require((-Jprime, Q(0)) + (Q(0),) * terms == vector_zero(terms),
                        "dropping common Jprime changes the mean action source"),
        "dropping common Jprime changes the mean action source")
    require(E != sum((q ** j for j in range(horizon)), Q(0)), "continuation is beta*q, not q")
    return {"prep_leaves": len(preparation), "stage_transcripts": len(stages),
            "complete_leaves": len(leaves), "alpha": str(alpha), "beta": str(beta),
            "q": str(q), "N": horizon, "J": str(J0), "Jprime": str(Jprime),
            "terminal_masses": {key: str(value) for key, value in terminal_masses.items()},
            "actual_mean_clock_cost": str(full_cost), "actual_mean_clock_jet": str(full_cost_jet),
            "log_atoms": [str(atom) for atom in atoms],
            "H_coefficients": [str(value) for value in H],
            "dH_coefficients": [str(value) for value in DH],
            "bindings": bindings,
            "negative_controls": [prep_rejection, ready_rejection, stage_rejection, J_rejection]}


def native_q0_sign_control():
    # Consume the owned original two-query baseline only. No query or gate
    # compilation and no determinant/geometry certificate is replayed.
    z = Q(1, 2 ** 20)
    B0 = scale(power(P, 3), 4)
    A0 = mul(B0, add(ONE, power(P, 6)))
    q0 = add(ONE, scale(mul(add(ONE, scale(A0, -z)), add(ONE, scale(B0, -z))), -1))
    expected = add(scale(add(A0, B0), z), scale(mul(A0, B0), -z ** 2))
    require(q0 == expected != ZERO, "original complete two-query click baseline")
    lo, hi = Q(618, 1000), Q(619, 1000)
    require(lo * lo + lo - 1 < 0 < hi * hi + hi - 1, "exact Golden root enclosure")
    require(B0 == add(ONE, scale(power(P, 6), -1)) and
            A0 == add(ONE, scale(power(P, 12), -1)), "both actual feedback bands are inside(0,1)")
    lower, upper = z * (1 - hi ** 6), 2 * z
    require(0 < lower < upper < Q(1, 2), "q0>z*B0>0 and q0<2z<1/2")
    phi_upper = Q(13, 8)
    require((2 * phi_upper - 1) ** 2 > 5 and phi_upper > 1,
            "positive Golden base phi<13/8")
    require(phi_upper ** 27 < 2 ** 19 - 1,
            "phi^27<(13/8)^27<2^19-1 implies h'_phi(q0)>27")
    scalar_entropy_source = Q(1, 2) * Q(1, 2) * Q(99, 100) * 27
    amplitude_entropy_source = scalar_entropy_source / 2
    require(amplitude_entropy_source == Q(2673, 800) > 3 and
            scalar_entropy_source == Q(2673, 400) > 6,
            "entropy component theta*alpha*c_H has the stated strict lower bounds")
    # At this owned q0, h_phi(q0)>0 and h'_phi(q0)>0. Thus for a
    # nontrivial retained stage and fixed J, theta*dH/dq is positive.
    return {"q0_coefficients_in_1_a_a2_a3": [str(v) for v in q0],
            "strict_q0_lower": str(lower), "strict_q0_upper": str(upper),
            "binary_entropy_slope_strict_lower": 27,
            "entropy_source_component_strict_lowers": {
                "theta_half": str(amplitude_entropy_source), "theta_one": str(scalar_entropy_source)},
            "source_bound_conditions": "alpha>=1/2,beta>1/2,d0>99/100; these bounds concern theta*dH, with -dJ retained separately",
            "consequence": "h_phi(q0)>0,h'_phi(q0)>27; no common-J source is set to zero"}


def moving_setup_source_control():
    """One independent first-jet ledger for the complete moving-setup rule.

    The local probability lines are normalized and positive near zero.
    They are a formal fixture, not a claim of moving native gate weights.
    """
    preparation = preparation_leaves(Q(2, 5), 2, (Q(5), Q(9)))
    stages = [Stage(Q(1, 5), False, Q(7), "abort"),
              Stage(Q(1, 3), True, Q(20), "ready-early"),
              Stage(Q(7, 15), True, Q(50), "ready-late")]
    q, dq, horizon = Q(2, 7), Q(2, 9), 3
    prep_jets = [Q(0)] * len(preparation)
    first_ready = next(i for i, item in enumerate(preparation) if item.ready)
    first_abort = next(i for i, item in enumerate(preparation) if not item.ready)
    prep_jets[first_ready], prep_jets[first_abort] = Q(1, 50), Q(-1, 50)
    stage_jets = [Q(1, 17), Q(-2, 17), Q(1, 17)]
    require(sum(prep_jets) == sum(stage_jets) == 0, "moving preparation and stage probability lines normalized")
    alpha = sum((item.probability for item in preparation if item.ready), Q(0))
    dalpha = sum((jet for item, jet in zip(preparation, prep_jets) if item.ready), Q(0))
    beta = sum((item.probability for item in stages if item.ready), Q(0))
    dbeta = sum((jet for item, jet in zip(stages, stage_jets) if item.ready), Q(0))
    require(dalpha != 0 and dbeta != 0 and dq != 0, "every moving setup source is genuine")
    atoms = [p.probability for p in preparation] + [t.probability for t in stages] + [q, 1 - q]
    atom_jets = prep_jets + stage_jets + [dq, -dq]
    terms = len(atoms)
    leaves = complete_leaves(preparation, stages, q, horizon)
    full_jets = [leaf.probability * sum((count * jet / atom
                                       for count, jet, atom in zip(leaf.powers, atom_jets, atoms)), Q(0))
                 for leaf in leaves]
    require(sum(full_jets) == 0, "moving full-tree mass derivative remains zero")
    actual_DH = (Q(0), Q(0)) + tuple(-sum((jet * leaf.powers[i] for leaf, jet in zip(leaves, full_jets)), Q(0))
                                     for i in range(terms))
    zeros_pre = (Q(0),) * len(preparation)
    zeros_stage = (Q(0),) * len(stages)
    DHpre = (Q(0), Q(0)) + tuple(-jet for jet in prep_jets) + zeros_stage + (Q(0), Q(0))
    HT = (Q(0), Q(0)) + zeros_pre + tuple(-t.probability for t in stages) + (Q(0), Q(0))
    DHT = (Q(0), Q(0)) + zeros_pre + tuple(-jet for jet in stage_jets) + (Q(0), Q(0))
    h = (Q(0), Q(0)) + zeros_pre + zeros_stage + (-q, -(1 - q))
    hprime = (Q(0), Q(0)) + zeros_pre + zeros_stage + (Q(-1), Q(1))
    A = vadd(HT, vscale(h, beta))
    x = beta * q
    E = sum((x ** j for j in range(horizon)), Q(0))
    Eprime = sum((j * x ** (j - 1) for j in range(1, horizon)), Q(0))
    contributions = [DHpre, vscale(A, E * dalpha), vscale(DHT, alpha * E),
                     vscale(vadd(vscale(h, E), vscale(A, q * Eprime)), alpha * dbeta),
                     vscale(vadd(vscale(hprime, E), vscale(A, Eprime)), alpha * beta * dq)]
    expected_DH = vector_sum(contributions, terms)
    require(actual_DH == expected_DH, "complete moving-setup entropy differential(9)")
    require(all(term != vector_zero(terms) for term in contributions), "no moving setup term was silently frozen")
    return {"complete_leaves": len(leaves), "Dalpha": str(dalpha), "Dbeta": str(dbeta), "Dq": str(dq),
            "all_five_setup_contributions_nonzero": True,
            "exact_differential": "DHpre+A*E*Dalpha+alpha*E*DHT+alpha*(h*E+q*A*Eprime)*Dbeta+alpha*beta*(hprime*E+A*Eprime)*Dq",
            "dH_coefficients": [str(value) for value in actual_DH]}


def main():
    fixtures = [
        check_fixture(Q(2, 5), 2,
                      [Stage(Q(1, 5), False, Q(7), "abort"),
                       Stage(Q(1, 3), True, Q(20), "ready-early"),
                       Stage(Q(7, 15), True, Q(50), "ready-late")],
                      Q(2, 7), 3, Q(2, 5), Q(3, 7)),
        check_fixture(Q(3, 7), 1,
                      [Stage(Q(1, 7), False, Q(8), "abort-early"),
                       Stage(Q(2, 7), False, Q(19), "abort-late"),
                       Stage(Q(1, 7), True, Q(31), "ready-even"),
                       Stage(Q(3, 7), True, Q(47), "ready-odd")],
                      Q(3, 5), 4, Q(-1, 3), Q(-2, 9)),
    ]
    print(json.dumps({
        "status": "PASS: complete retained detector Book-mean ledger, conditional bindings only",
        "exact_entropy": "H_full=H_pre+alpha*[H_T+beta*h_phi(q)]*E_N(beta*q)",
        "conditional_mean_action": "E[S_theta]=theta*H_full-J, theta=1/2 or1",
        "mean_differential": "E[dS_theta]=-dJ",
        "differential_of_mean": "dE[S_theta]=theta*dH_full-dJ",
        "coefficient_slots": "constant,1/log(phi),log_phi(each listed rational atom)",
        "Decimal_precision": 85, "finite_difference_step": "1e-18", "finite_difference_absolute_tolerance": "1e-32",
        "complete_leaf_fixtures": fixtures, "moving_setup_source_fixture": moving_setup_source_control(),
        "owned_native_baseline_sign_control": native_q0_sign_control(),
        "scope": [
            "Fixtures are rational ledger examples, not new Golden gadget probabilities or physical prices",
            "Both absolute-amplitude and scalar-weight binding hypotheses are checked without selecting either",
            "Complete costs, preparation abort, gate abort, internal records and unresolved cap remain",
            "The common raw normalizer J and its nonzero first jet are retained",
            "Physical Book03 gain/aggregate, native admission and the full physical GR source remain open",
        ],
    }, indent=2))


if __name__ == "__main__":
    main()
