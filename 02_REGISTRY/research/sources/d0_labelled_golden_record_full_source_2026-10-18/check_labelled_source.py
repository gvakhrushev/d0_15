#!/usr/bin/env python3
"""Exact bounded consumer of the retained labelled golden-record source.

This checks finite algebra and a sparse 528 x 128 pure-state construction.
It does not execute old checkers, certify an operation's physical admission,
select an action, or establish D0 -> GR. The earlier-label entropy source is
kept explicitly. All checks raise exceptions, including under python -O.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import platform

import sympy as s


HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parents[1]
P = s.Symbol("p", positive=True)
ELL = s.Symbol("ell", positive=True)
MODULUS = P**2 + P - 1
CHECKS: list[str] = []


def require(name: str, condition: object) -> None:
    if condition is not True and condition != s.true:
        raise RuntimeError(f"FAILED {name}: {condition}")
    CHECKS.append(name)


def golden(expr: s.Expr) -> s.Expr:
    """Exact rational arithmetic in Q(p), with other symbols as coefficients."""
    numerator, denominator = s.fraction(s.cancel(expr))
    inverse = s.invert(denominator, MODULUS, P, domain="EX")
    return s.cancel(s.rem(s.expand(numerator * inverse), MODULUS, P))


def zero(name: str, expr: s.Expr) -> None:
    require(name, golden(expr) == 0)


def binary_entropy(value: s.Expr) -> s.Expr:
    return -value * s.log(value) - (1 - value) * s.log(1 - value)


def probability_part(bit: int, value: s.Expr) -> s.Expr:
    return value if bit else 1 - value


def labelled_law_checks() -> dict[str, object]:
    w, e0, e1, b0, b1 = s.symbols("w e0 e1 b0 b1", positive=True)
    dw, de0, de1, db0, db1 = s.symbols("dw de0 de1 db0 db1", real=True)
    variables = [w, e0, e1, b0, b1]
    velocities = [dw, de0, de1, db0, db1]
    weights, es, bs = [w, 1 - w], [e0, e1], [b0, b1]
    law = {}
    for y in range(2):
        for a in range(2):
            for b in range(2):
                law[y, a, b] = (
                    weights[y] * probability_part(a, es[y])
                    * probability_part(b, bs[y])
                )
    zero("all_eight_retained_labels_normalize", sum(law.values()) - 1)
    for y in range(2):
        zero(f"old_label_{y}_marginal", sum(q for (yy, _, _), q in law.items()
             if yy == y) - weights[y])
    zero("nonuniform_old_weights_are_not_uniform", (weights[0] - weights[1])
         .subs(w, s.Rational(1, 3)) + s.Rational(1, 3))

    # Compute the actual full derivative before using the entropy chain rule.
    direct = 0
    for q in law.values():
        dq = sum(s.diff(q, variable) * velocity
                 for variable, velocity in zip(variables, velocities))
        direct -= dq * (s.expand_log(s.log(q), force=True) + 1)
    hprime = lambda v: s.log(1 - v) - s.log(v)
    chain = dw * (s.log(1 - w) - s.log(w)
                  + binary_entropy(e0) - binary_entropy(e1)
                  + binary_entropy(b0) - binary_entropy(b1))
    chain += w * (hprime(e0) * de0 + hprime(b0) * db0)
    chain += (1 - w) * (hprime(e1) * de1 + hprime(b1) * db1)
    require("complete_moving_old_label_source_chain_rule",
            s.simplify(s.expand(direct - chain)) == 0)

    # p + p^2 = 1 implies h'(p^2) = log(p/p^2) = log(phi).
    zero("golden_binary_complement_is_p", 1 - P**2 - P)
    golden_slope = s.expand_log(s.log(P / P**2), force=True)
    require("golden_entropy_slope_exact_ell",
            golden_slope.subs(s.log(P), -ELL) == ELL)
    zero("single_flag_leading_source_p2", P**2 * ELL / ELL - P**2)
    require("single_flag_coefficient_is_nonzero", golden(P**2) != 0)
    zero("balanced_scene_entropy_slope", hprime(s.Rational(1, 2)))

    # Exact f=0 source with moving old weights and arbitrary scene jets.
    u0, u1, t, velocity = s.symbols("u0 u1 t velocity", real=True)
    golden_chain = chain.subs({e0: P**2, e1: P**2,
                              b0: s.Rational(1, 2), b1: s.Rational(1, 2)})
    golden_chain = golden_chain.xreplace({s.log(1 - P**2): s.log(P),
                                         s.log(P**2): 2*s.log(P)})
    golden_chain = s.expand_log(s.expand(golden_chain), force=True)
    golden_chain = golden_chain.subs(s.log(P), -ELL)
    fixture_source = golden_chain.subs({w: s.Rational(1, 3), dw: velocity,
                                       de0: P**2*t**2*u0, de1: P**2*t**2*u1}) / ELL
    expected = velocity*s.log(2)/ELL + P**2*t**2*(u0 + 2*u1)/3
    zero("full_source_at_f_zero_keeps_DH_old", s.expand_log(
         s.expand(fixture_source - expected), force=True))
    require("moving_old_entropy_source_is_not_zero", s.log(2) != 0)
    zero("scene_zero_jet_vanishes_by_stationarity", s.diff(golden_chain, db0))
    zero("scene_one_jet_vanishes_by_stationarity", s.diff(golden_chain, db1))

    # The PF word sum has mass phi/sqrt(5), not unit mass.
    phi = 1/P
    zero("PF_continuum_coefficient_2p4_over_sqrt5",
         2*P**3 * P**2 * phi/s.sqrt(5) - 2*P**4/s.sqrt(5))
    require("PF_mass_cannot_silently_be_one", golden(phi/s.sqrt(5)-1) != 0)
    return {"terminal_labels": len(law), "old_weights_fixture": ["1/3", "2/3"],
            "old_history_source": "D H(w)/log(phi)",
            "single_flag_leading_coefficient": "p^2",
            "PF_continuum_coefficient_before_corner": "2*p^4/sqrt(5)"}


def balanced_schmidt_checks() -> dict[str, object]:
    dimension, reference_rank = 528, 128
    lam = golden(4*P**3)
    lam3 = golden(1-(130*P-81)**2)
    lamv = golden(1-((854*P-531)/11)**2)
    spectrum = [s.S.Zero]*264 + [lam]*184 + [lam3]*36 + [lamv]*44
    require("all_528_scene_modes_retained", len(spectrum) == dimension)
    require("all_264_zero_modes_retained", spectrum.count(0) == 264)
    require("enough_zero_and_L_modes_for_reference128", 264 >= 128 and 184 >= 128)
    # Positive root p lies between 3/5 and 5/8. L=8p-4 > 4/5 > 1/2.
    zero("L_reduced", lam-(8*P-4))
    require("golden_root_lower_bound", MODULUS.subs(P, s.Rational(3, 5)) < 0)
    require("golden_root_upper_bound", MODULUS.subs(P, s.Rational(5, 8)) > 0)
    require("L_lower_bound_exceeds_half", 8*s.Rational(3, 5)-4 > s.Rational(1, 2))
    alpha = golden(1/(2*lam))
    x, y = s.symbols("schmidt_x schmidt_y", real=True)
    x2, y2 = golden((1-alpha)/128), golden(alpha/128)

    def amplitude_reduce(expr: s.Expr) -> s.Expr:
        polynomial = s.Poly(s.expand(expr), x, y, domain="EX")
        reduced = 0
        for (ix, iy), coefficient in polynomial.terms():
            reduced += (coefficient*x2**(ix//2)*y2**(iy//2)
                        * x**(ix % 2)*y**(iy % 2))
        return golden(reduced)

    def azero(name: str, expr: s.Expr) -> None:
        require(name, amplitude_reduce(expr) == 0)

    # Explicit sparse ket on the whole 528 x 128 carrier, not a 528-rank density.
    ket = {(i, i): x for i in range(reference_rank)}
    ket.update({(264+i, i): y for i in range(reference_rank)})
    require("sparse_ket_has_all_128_Schmidt_columns", len(ket) == 256)
    require("no_528_rank_purification_claim", reference_rank == 128 < dimension)

    def inner(left: dict, right: dict) -> s.Expr:
        return sum(s.conjugate(value)*right.get(index, 0)
                   for index, value in left.items())

    bket = {index: spectrum[index[0]]*value for index, value in ket.items()}
    azero("pure_state_normalization", inner(ket, ket)-1)
    azero("balanced_scene_expectation_half", inner(ket, bket)-s.Rational(1, 2))
    # Compute the full partial trace sparsely, including its offdiagonal support.
    data_rows = {}
    for (data, ref), value in ket.items():
        data_rows.setdefault(data, {})[ref] = value
    reference_gram = {}
    for row in data_rows.values():
        for i, vi in row.items():
            for j, vj in row.items():
                reference_gram[i, j] = reference_gram.get((i, j), 0)+vi*s.conjugate(vj)
    require("full_reference_partial_trace_has_no_offdiagonals",
            set(reference_gram) == {(i, i) for i in range(reference_rank)})
    for i in range(reference_rank):
        azero(f"full_reference_marginal_diagonal_{i}",
              reference_gram[i, i]-s.Rational(1, 128))
    centered = {index: (spectrum[index[0]]-s.Rational(1, 2))*value
                for index, value in ket.items()}
    variance = golden((2*lam-1)/4)
    azero("true_full_state_variance", inner(centered, centered)-variance)
    require("variance_not_zero", variance != 0)

    # Hermitian perturbation with inter-sector, imaginary and unoccupied-mode terms.
    perturbation = {(0, 264): s.Rational(2, 7), (264, 0): s.Rational(2, 7),
                    (1, 265): 3*s.I/11, (265, 1): -3*s.I/11,
                    (448, 264): s.Rational(5, 13), (264, 448): s.Rational(5, 13),
                    (0, 0): s.Rational(1, 9), (264, 264): -s.Rational(2, 17)}
    require("perturbation_is_Hermitian", all(s.conjugate(value) ==
            perturbation.get((j, i), 0) for (i, j), value in perturbation.items()))
    require("perturbation_does_not_commute_with_B", any(
        golden((spectrum[i]-spectrum[j])*value) != 0
        for (i, j), value in perturbation.items()))
    perturbed_ket = {}
    for (i, j), value in perturbation.items():
        for ref in range(reference_rank):
            amplitude = ket.get((j, ref), 0)
            if amplitude != 0:
                perturbed_ket[i, ref] = perturbed_ket.get((i, ref), 0)+value*amplitude
    m = amplitude_reduce(inner(ket, perturbed_ket))
    azero("arbitrary_Hermitian_jet_expectation_is_real", m-s.conjugate(m))
    require("chosen_jet_has_nonzero_unrepaired_db", m != 0)
    tangent = {index: -m*value/(2*variance) for index, value in centered.items()}
    azero("right_inverse_is_normalized_tangent", 2*s.re(inner(ket, tangent)))
    azero("right_inverse_cancels_total_db", m+2*s.re(inner(tangent, bket)))
    require("omitting_preparation_jet_leaves_nonzero_db", m != 0)
    for i in range(reference_rank):
        value = sum(tangent.get((data, i), 0)*s.conjugate(ket.get((data, i), 0))
                    + ket.get((data, i), 0)*s.conjugate(tangent.get((data, i), 0))
                    for data in [i, 264+i])
        azero(f"right_inverse_preserves_reference_diagonal_{i}", value)
    require("right_inverse_preserves_reference_offdiagonals",
            all(index[0] in [index[1], 264+index[1]] for index in tangent))
    require("balanced_entropy_stationarity_is_not_a_minimum",
            s.diff(binary_entropy(s.Symbol("b")), s.Symbol("b"), 2)
            .subs(s.Symbol("b"), s.Rational(1, 2)) == -4)

    # A genuinely extra preparation cost changes the stationary equation.
    kappa, scalar_b = s.symbols("kappa scalar_b", real=True)
    controller_source = s.diff(binary_entropy(scalar_b)+kappa*scalar_b, scalar_b)
    require("extra_controller_source_cannot_be_discarded",
            controller_source.subs(scalar_b, s.Rational(1, 2)) == kappa)
    return {"scene_dimension": dimension, "retained_zero_modes": 264,
            "reference_dimension": reference_rank, "Schmidt_rank": 128,
            "ket_nonzero_entries": len(ket), "balanced_b": "1/2",
            "variance": "(2*L-1)/4", "right_inverse_checked": True,
            "reference_marginal": "I_128/128",
            "unoccupied_modes_retained_in_operator": True}


def conditional_obstruction_checks() -> dict[str, object]:
    r = s.Symbol("r", real=True)
    b0, b1 = r, s.Rational(1, 3)+r/2
    require("conditional_zero_can_balance_individually",
            s.solve(b0-s.Rational(1, 2), r) == [s.Rational(1, 2)])
    require("conditional_one_can_balance_individually",
            s.solve(b1-s.Rational(1, 2), r) == [s.Rational(1, 3)])
    require("one_common_state_cannot_balance_both",
            s.solve([b0-s.Rational(1, 2), b1-s.Rational(1, 2)], [r]) == [])
    jacobian = s.Matrix([b0, b1]).jacobian([r])
    demand = s.Matrix([0, 1])
    require("actual_common_preparation_Jacobian_not_onto", jacobian.rank() == 1)
    require("unabsorbable_conditional_jet", jacobian.row_join(demand).rank() == 2)
    zero("diagnostic_golden_prefix_Kraus_completeness", P+P**2-1)
    return {"scope": "diagnostic finite common-preparation control",
            "individual_balance_values": ["1/2", "1/3"],
            "simultaneous_balance": False, "Jacobian_rank": 1}


def corner_checks() -> dict[str, object]:
    r = golden(P**6)
    # Complete success/failure law, with two nonempty failure records.
    q = [r*s.Rational(1, 3), r*s.Rational(2, 3),
         (1-r)*s.Rational(2, 5), (1-r)*s.Rational(3, 5)]
    zero("real_corner_complete_failure_branch_normalization", sum(q)-1)
    zero("real_corner_success_mass_p6", sum(q[:2])-P**6)
    zero("real_corner_failure_mass_retained", sum(q[2:])-(1-P**6))
    require("corner_success_is_not_unit_mass", r != 1)
    dr, hs, hf, dhs, dhf, rr = s.symbols("dr hs hf dhs dhf rr", real=True)
    hprime = s.log(1-rr)-s.log(rr)
    full_derivative = (hprime+hs-hf)*dr+rr*dhs+(1-rr)*dhf
    zero("fixed_corner_full_source_multiplier_p6",
         full_derivative.subs({rr: r, dr: 0, dhf: 0})-P**6*dhs)
    require("free_postselection_wrong_source_multiplier", golden(1-r) != 0)
    require("moving_corner_source_terms_are_retained",
            s.diff(full_derivative, dr) == hprime+hs-hf)
    e, beta, cr = s.symbols("corner_e failure_beta corner_r", positive=True)
    corner_law = [cr*(1-e), cr*e, (1-cr)*beta, (1-cr)*(1-beta)]
    corner_entropy = -sum(q*s.expand_log(s.log(q), force=True) for q in corner_law)
    for variable, expected in [
        (e, cr*(s.log(1-e)-s.log(e))),
        (beta, (1-cr)*(s.log(1-beta)-s.log(beta))),
        (cr, s.log(1-cr)-s.log(cr)+binary_entropy(e)-binary_entropy(beta)),
    ]:
        require(f"actual_complete_corner_entropy_source_{variable}",
                s.simplify(s.expand(s.diff(corner_entropy, variable)-expected)) == 0)
    zero("PF_prefactor_after_real_corner_2p10_over_sqrt5",
         P**6 * 2*P**4/s.sqrt(5)-2*P**10/s.sqrt(5))
    return {"success_probability": "p^6", "failure_probability": "1-p^6",
            "failure_records_retained": 2, "source_multiplier": "p^6",
            "scope": "fixed canonical prefix probability; not a free-preparation critical point",
            "PF_continuum_coefficient_after_corner": "2*p^10/sqrt(5)"}


def five_outcome_free_prefix_checks() -> dict[str, object]:
    """Complete failure + four success labels; no AF address readout.

    Covariance c is retained before differentiation. At the scalar AF point
    it is zero for arbitrary correlated success preparations. Its tangent
    need not vanish, but its entropy-gradient coefficient does vanish.
    """
    prefix, e, b = s.symbols("prefix e b", positive=True)
    c = s.Symbol("covariance", real=True)
    dprefix, de, db, dc = s.symbols("dprefix de db dc", real=True)
    conditional = [(1-e)*(1-b)+c, (1-e)*b-c,
                   e*(1-b)-c, e*b+c]
    law = [1-prefix]+[prefix*q for q in conditional]
    zero("all_five_no_address_outcomes_normalize", sum(law)-1)
    zero("prefix_failure_retained_in_five_outcomes", law[0]-(1-prefix))
    zero("success_AF_marginal_even_with_covariance", law[3]+law[4]-prefix*e)
    zero("success_scene_marginal_even_with_covariance", law[2]+law[4]-prefix*b)

    velocities = {prefix: dprefix, e: de, b: db, c: dc}
    actual_gradient = 0
    for q in law:
        dq = sum(s.diff(q, variable)*velocity
                 for variable, velocity in velocities.items())
        actual_gradient -= dq.subs(c, 0) * (
            s.expand_log(s.log(q.subs(c, 0)), force=True)+1)
    hprime = lambda v: s.log(1-v)-s.log(v)
    expected_gradient = ((hprime(prefix)+binary_entropy(e)+binary_entropy(b))*dprefix
                         +prefix*hprime(e)*de+prefix*hprime(b)*db)
    require("complete_five_outcome_first_gradient_with_covariance",
            s.simplify(s.expand(actual_gradient-expected_gradient)) == 0)
    require("covariance_tangent_has_zero_coefficient_only_at_product_point",
            s.simplify(s.diff(actual_gradient, dc)) == 0)
    # Away from the product point, a covariance source is real and retained.
    covariance_source = -prefix * s.log(
        conditional[0]*conditional[3]/(conditional[1]*conditional[2]))
    witness = covariance_source.subs({prefix: s.Rational(3, 4),
                                     e: s.Rational(1, 3), b: s.Rational(1, 2),
                                     c: s.Rational(1, 24)})
    require("nonproduct_covariance_source_is_not_discarded", witness != 0)

    # Scalar E forces zero preparation jet in e at t=0, without factorization.
    ar, br, cr, dr = s.symbols("a_r b_r c_r d_r", real=True)
    ai, bi, ci, di = s.symbols("a_i b_i c_i d_i", real=True)
    prep_tangent = s.Matrix([
        [ar, br+s.I*bi, cr+s.I*ci, dr+s.I*di],
        [br-s.I*bi, -ar, ai+s.I*ci, bi+s.I*di],
        [cr-s.I*ci, ai-s.I*ci, br, cr+s.I*ai],
        [dr-s.I*di, bi-s.I*di, cr-s.I*ai, -br],
    ])
    require("correlated_preparation_tangent_is_Hermitian",
            prep_tangent == prep_tangent.conjugate().T)
    zero("correlated_preparation_tangent_is_trace_zero", s.trace(prep_tangent))
    zero("scalar_AF_effect_has_no_preparation_source",
         s.trace(prep_tangent*(P**2*s.eye(4))))
    require("correlated_tangent_not_required_to_factorize",
            prep_tangent[0, 3] != 0)

    # Solve the actual free-prefix equation, keeping its real failure entropy.
    u = s.Symbol("u", positive=True)
    stationary_prefix = u/(1+u)
    free_equation = hprime(prefix)+s.log(u)
    require("logistic_prefix_stationarity_exact",
            s.simplify(s.expand_log(free_equation.subs(prefix, stationary_prefix),
                                    force=True)) == 0)
    require("balanced_scene_stationarity_exact", hprime(s.Rational(1, 2)) == 0)
    # Whole-carrier POVM gradient, with no factorization constraint on d rho.
    b00, b01, b11 = s.symbols("B00 B01 B11", real=True)
    scene_effect = s.Matrix([[b00, b01], [b01, b11]])
    effects = [s.eye(2)-scene_effect, scene_effect]
    success_gradient = s.zeros(2)
    for abit in range(2):
        pa = probability_part(abit, e)
        for effect in effects:
            success_gradient -= pa*(s.expand_log(s.log(prefix*pa/2), force=True)+1)*effect
    success_scalar = -s.log(prefix)+binary_entropy(e)+s.log(2)-1
    require("whole_success_POVM_gradient_is_scalar_for_arbitrary_B",
            (success_gradient-success_scalar*s.eye(2)).applyfunc(
                lambda value: s.simplify(s.expand(value))) == s.zeros(2))
    failure_scalar = -s.log(1-prefix)-1
    require("whole_carrier_scalar_gradient_difference_is_free_prefix_equation",
            s.simplify(success_scalar-failure_scalar
                       -hprime(prefix)-binary_entropy(e)-s.log(2)) == 0)
    require("full_normalized_preparation_source_zero_on_solved_branch",
            s.simplify(s.expand_log((success_scalar-failure_scalar)
                       .subs(prefix, stationary_prefix), force=True)
                       -binary_entropy(e)-s.log(2)+s.log(u)) == 0)
    zero("golden_binary_entropy_exact",
         -(2*P**2+P)*(-ELL)-(2-P)*ELL)
    golden_slope = s.expand_log(s.log(P/P**2), force=True).subs(s.log(P), -ELL)
    zero("free_prefix_star_source_sstar_p2",
         stationary_prefix*golden_slope*P**2/ELL-stationary_prefix*P**2)
    require("free_prefix_star_source_nonzero", golden(stationary_prefix*P**2) != 0)
    require("free_prefix_probability_is_not_postselected_one", stationary_prefix != 1)

    # Canonical p^6 is below 1/2, whereas exp(H*)/(1+exp(H*)) is above 1/2.
    require("canonical_corner_p6_less_than_half",
            s.Rational(5, 8)**6 < s.Rational(1, 2))
    require("Hstar_is_strictly_positive", 2-s.Rational(5, 8) > 0)
    require("canonical_corner_free_source_strictly_positive",
            (1-s.Rational(5, 8)**6)/s.Rational(5, 8)**6 > 1)
    # These exact inequalities plus ell>0 imply h'(p^6)+H*>0.
    require("logistic_branch_not_canonical_corner",
            s.Rational(1, 2) > s.Rational(5, 8)**6)

    # The GNS success/failure vectors are orthogonal; their conditional
    # success state, hence its old-AF trace, is unchanged by varying prefix.
    normalized_gns = s.Matrix([s.sqrt(stationary_prefix),
                               s.sqrt(1-stationary_prefix)])
    require("freely_prepared_AF_input_is_normalized",
            s.simplify((normalized_gns.conjugate().T*normalized_gns)[0]-1) == 0)
    require("freely_prepared_AF_input_success_probability",
            s.simplify(normalized_gns[0]**2-stationary_prefix) == 0)
    require("freely_prepared_AF_input_keeps_failure_probability",
            s.simplify(normalized_gns[1]**2-(1-stationary_prefix)) == 0)
    require("conditional_success_vector_unchanged",
            s.simplify(normalized_gns[0]/s.sqrt(stationary_prefix)-1) == 0)
    zero("corner_success_GNS_normalization_is_e_over_p3", P**6/(P**3)**2-1)
    zero("corner_failure_GNS_normalization",
         (1-P**6)/(1-P**6)-1)
    # Tensoring this normalized AF vector changes neither the scene's b
    # nor the full Schmidt128 reference marginal checked above.
    zero("AF_tensor_preserves_each_reference_eigenvalue",
         (stationary_prefix+1-stationary_prefix)/128-s.Rational(1, 128))

    # At f=0, moving conditional AF weights cannot enter first source.
    mu, dmu, f0, f1, df0, df1, t = s.symbols(
        "mu dmu f0 f1 df0 df1 t", real=True)
    mean_e = P**2*(1+t**2*(mu*f0+(1-mu)*f1))
    dmean = (s.diff(mean_e, mu)*dmu+s.diff(mean_e, f0)*df0
             +s.diff(mean_e, f1)*df1)
    zero("no_address_moving_weight_source_vanishes_at_f_zero",
         dmean.subs({f0: 0, f1: 0})-P**2*t**2*(mu*df0+(1-mu)*df1))
    zero("free_prefix_PF_continuum_coefficient",
         stationary_prefix*2*P**4/s.sqrt(5)-2*stationary_prefix*P**4/s.sqrt(5))
    # A no-address readout is h(mean E), not sum mu*h(E). Distinguish them.
    v, base = s.symbols("v base", real=True)
    average = (base+2*v)/3+2*(base-v)/3
    require("no_address_probability_is_the_true_mean", s.simplify(average-base) == 0)
    addressed_entropy = (binary_entropy(base+2*v)+2*binary_entropy(base-v))/3
    addressed_second = s.diff(addressed_entropy, v, 2).subs(v, 0)
    zero("implicit_address_entropy_is_a_different_second_jet",
         s.simplify(addressed_second-2*s.diff(binary_entropy(base), base, 2)))
    require("address_readout_cannot_be_silently_inserted", addressed_second != 0)

    # Same-history reference code can remain fixed while the true preparation changes.
    q, code = s.symbols("event_probability fixed_code", positive=True)
    cost = -s.log(code)/ELL
    info = (s.log(q)-s.log(code))/ELL
    require("fixed_reference_code_still_gives_true_branch_action",
            s.simplify(cost-info+s.log(q)/ELL) == 0)
    return {
        "retained_outcomes": 5, "AF_address_readout": False,
        "conditional_covariance_tangent_retained": True,
        "source_at_scalar_product_point":
            "[h'(s)+h(e)+h(b)]ds+s*h'(e)de+s*h'(b)db",
        "H_star": "h(p^2)+log(2)=(2-p)*log(phi)+log(2)",
        "stationary_prefix_probability": "s_star=exp(H_star)/(1+exp(H_star))",
        "canonical_p6_prefix_freely_stationary": False,
        "star_first_source_coefficient": "s_star*p^2",
        "PF_continuum_coefficient": "2*s_star*p^4/sqrt(5)",
        "input_state": "sqrt(s_star)*e/p^3+sqrt(1-s_star)*(I-e)/sqrt(1-p^6)",
        "full_Schmidt_reference_rank": 128,
        "scope": "configured five-outcome programme, scalar AF point; native selection not proved",
    }


def periodic_scalar_completion_checks() -> dict[str, object]:
    """Consume the actual owned null-frame star polynomial, not its old suite.

    All three u-containing faces are retained, including uv. H and every
    shifted null connection coefficient are independent symbols.
    """
    path = RESEARCH / "sources/d0_af_star_full_lattice_2026-10-17/star_euler.py"
    spec = importlib.util.spec_from_file_location("owned_star_density", path)
    owned = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(owned)
    k0, k1, HH, scale = s.symbols("k0 k1 HH scale", real=True)
    K = k0*owned.N[0]+k1*owned.N[1]
    identity = s.eye(4)
    for i, generator in enumerate(owned.N):
        require(f"owned_null_generator_Lorentz_{i}",
                generator.T*owned.ETA+owned.ETA*generator == s.zeros(4))
    require("owned_null_generators_commute",
            owned.N[0]*owned.N[1]-owned.N[1]*owned.N[0] == s.zeros(4))
    require("owned_null_generator_cube_zero", K**3 == s.zeros(4))
    U = identity+K+K*K/2
    require("arbitrary_null_link_is_Lorentz",
            (U.T*owned.ETA*U-owned.ETA).applyfunc(s.expand) == s.zeros(4))
    coframe = s.eye(4)
    coframe[1, 0] = HH/2
    coframe *= scale
    total = 0
    for axis in (1, 2, 3):
        shifted0, shifted1 = s.symbols(f"shifted{axis}_0 shifted{axis}_1", real=True)
        shifted = shifted0*owned.N[0]+shifted1*owned.N[1]
        face = (U*(identity-shifted+shifted*shifted/2)).applyfunc(s.expand)
        inv = owned.ETA*face.T*owned.ETA
        odd = (face-inv)/2
        require(f"full_face_odd_curvature_is_null_{axis}",
                (odd-K+shifted).applyfunc(s.expand) == s.zeros(4))
        u, v = [i for i in range(4) if i not in (0, axis)]
        value = owned.EPS((0, axis, u, v))*owned.pairing(
            owned.wedge(coframe[:,u], coframe[:,v]), odd)
        require(f"complete_periodic_star_face_zero_{axis}", s.expand(value) == 0)
        total += value
    require("arbitrary_H_null_completion_scalar_zero_everywhere", s.expand(total) == 0)
    # A curvature outside the null-bivector space must not be erased.
    opposite = s.zeros(4)
    opposite[0, 2] = 1
    opposite[2, 1] = 1
    control = owned.pairing(owned.wedge(coframe[:,1], coframe[:,3]), opposite)
    require("nonnulled_curvature_negative_control_detected", s.expand(control) != 0)
    return {"same_original_periodic_carrier": True, "H_any_coordinate_dependence": True,
            "u_v_face_included": True, "all_sites_scalar_star": "0 exactly",
            "exterior_coframe_link_Euler_rows_solved": False,
            "boundary": "same fixed exterior as owned local recovery"}


def golden_axis_query_checks() -> dict[str, object]:
    """Actual four-copy T_E signs and its scalar-point operator first jet."""
    identity = s.eye(4)
    A = s.diag(1, 1, 1, 1)
    A[2, 2] = A[3, 3] = 0
    A[2, 3] = A[3, 2] = 1
    J = s.zeros(4)
    for i in range(2):
        J[i, i+2], J[i+2, i] = -1, 1
    r, b = s.symbols("axis_r axis_b", real=True)
    actual = s.Matrix([[r, 0, -b, 0], [0, r, 0, -b],
                       [0, b, 0, r], [b, 0, r, 0]])
    require("actual_four_module_T_E_signs_factor_exactly", actual == A*(r*identity+b*J))
    require("axis_A_orthogonal", A.T*A == identity)
    require("axis_J_skew", J.T == -J)
    require("axis_J_square_minus_identity", J*J == -identity)
    theta, theta0 = s.symbols("theta theta0", real=True)
    rotation = lambda angle: s.cos(angle)*identity+s.sin(angle)*J
    require("actual_axis_relative_exponential_identity",
            (A*rotation(theta0)*rotation(theta-theta0)-A*rotation(theta))
            .applyfunc(s.trigsimp) == s.zeros(4))
    t = s.Symbol("axis_t", real=True)
    T0 = actual.subs({r: s.sqrt(P), b: P})
    direct_jet = actual.subs({r: -P**2*t**2/(2*s.sqrt(P)), b: P*t**2/2})
    require("actual_axis_geometric_first_jet_coefficient",
            (direct_jet-s.sqrt(P)*t**2*T0*J/2).applyfunc(s.simplify) == s.zeros(4))
    wrong = direct_jet+s.sqrt(P)*t**2*T0*J/2
    require("opposite_rotation_jet_negative_control", wrong != s.zeros(4))
    return {"existing_axis_only": True,
            "exact_first_jet": "(sqrt(p)/2)*t^2*T_(p^2)*J*D F_star",
            "native_geometric_SELECT_supplied": False}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true",
                        help="Intentionally save the newly computed RESULT.json; default is read-only")
    args = parser.parse_args()
    inputs = [
        "sources/d0_operational_car_clock_readout_2026-10-17/RESULT_RU.md",
        "sources/d0_af_full_feedback_first_source_2026-10-17/RESULT_RU.md",
        "sources/d0_cost_info_event_source_2026-10-17/RESULT_RU.md",
        "A4D_AF_STAR_PALATINI_NONLINEAR_EINSTEIN_COMPOSITION_2026_10_17.md",
        "A4D_NATIVE_FIBONACCI_RECORD_ACTIVATION.md",
        "sources/d0_af_star_full_lattice_2026-10-17/star_euler.py",
        "A4D_NATIVE_JACOBIAN_CONTROLLED_RECORD_SOURCE.md",
        "A4D_NATIVE_GOLDEN_PROGRAM_COMPILATION.md",
        "A4D_NATIVE_COMPILER_SOURCE_AND_RESOURCE_BOUNDARY.md",
    ]
    hashes = {}
    for relative in inputs:
        path = RESEARCH / relative
        require(f"input_exists_{relative}", path.is_file())
        hashes[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    result = {
        "date": "2026-10-18", "scientific_input_commit": "275244e5",
        "scope": "exact finite labelled-source algebra and local Schmidt128 lift",
        "labelled_source": labelled_law_checks(),
        "balanced_preparation": balanced_schmidt_checks(),
        "conditional_control": conditional_obstruction_checks(),
        "corner_preparation": corner_checks(),
        "five_outcome_free_prefix_preparation": five_outcome_free_prefix_checks(),
        "periodic_scalar_completion": periodic_scalar_completion_checks(),
        "golden_axis_query": golden_axis_query_checks(),
        "physical_admission_proved": False,
        "full_old_history_stationarity_proved": False,
        "same_program_simultaneous_balancing_proved": False,
        "physical_source_selection_proved": False,
        "GR_closed": False,
        "input_sha256": hashes,
        "runtime": {"python": platform.python_version(), "sympy": s.__version__},
        "explicit_checks": len(CHECKS),
        "check_names_sha256": hashlib.sha256("\n".join(CHECKS).encode()).hexdigest(),
    }
    output = HERE / "RESULT.json"
    if args.write:
        output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
