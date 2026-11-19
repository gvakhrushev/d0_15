"""Source of the information in the original G^512 predicate and noisy CX record."""
import json
from fractions import Fraction as F

from check_extra_work import centre, check, span


def logarithm(x):
    # Reduce the entire input range, including the small Schmidt eigenvalue,
    # to the rapid, positive-argument interval series of the archived control.
    root = x.sqrt().sqrt().sqrt()
    return 8*((2*root).log_positive()-span(2).log_positive())


def entropy(x):
    return -x*logarithm(x)-(1-x)*logarithm(1-x)


def divergence(x, y):
    return x*logarithm(x/y)+(1-x)*logarithm((1-x)/(1-y))


def predicate_example():
    # Orthogonal predicate sectors at SC6; all three later commuting labels are
    # computed from the same prepared inputs. This finite rational example also
    # checks the branch probabilities independently of the physical constants.
    pi, visibility, noise = F(2,5), F(3,4), F(2,7)
    joint = {}
    for accept in (0,1):
        for event in (0,1):
            for born in (0,1):
                success = accept*visibility
                mass = (pi if accept else 1-pi)*(success if event else 1-success)
                joint[accept,event,born^event] = mass*(noise if born else 1-noise)
    check(sum(joint.values())==1, "complete three-label law")
    total = sum(mass for (a,e,b),mass in joint.items() if b)
    check(total==noise+(1-2*noise)*pi*visibility, "full CX output")
    for accept in (0,1):
        mass = sum(w for (a,e,b),w in joint.items() if a==accept and b)
        check(mass==(pi if accept else 1-pi)*(noise+(1-2*noise)*visibility*accept),
              "marginalizing the actual port at fixed predicate")


def main():
    predicate_example()
    q, ell = centre()
    p = (span(5).sqrt()-1)/2
    l = p**2
    contrast = p**3
    pi = 4*p**7
    c, s = p.sqrt(), p
    for _ in range(9):
        c, s = c*c-s*s, 2*c*s
    visibility = s*s
    u = l+contrast*visibility
    Q = pi*visibility
    predicted = l+(u-l)*pi
    check(predicted.lo<=q.hi and q.lo<=predicted.hi, "same true PC13 centre")
    mi_event = entropy(q)-entropy(l)
    mi_pred = mi_event-pi*(entropy(u)-entropy(l))
    base = 1-logarithm((1-q)/q)/ell
    global_floor = (entropy(u)-entropy(l))/(ell*(u-l))
    lower = 1-divergence(u,q)/(ell*(u-q))
    upper = 1+divergence(l,q)/(ell*(q-l))
    pred_slope = base+global_floor
    root = (1-4*p**6*Q*(1-Q)).sqrt()
    small = (1-root)/2
    bank_slope = 1-contrast*(1-2*Q)*logarithm((1-small)/small)/(ell*root)
    check(mi_pred.lo>0 and mi_event.lo>mi_pred.hi, "distinct informative targets")
    check(F('0.0619277')<global_floor.lo and F('0.19814')<lower.lo
          and base.lo>lower.hi and pred_slope.hi<upper.lo, "positive uniform guarantees")
    check(bank_slope.hi<F('-0.8640'), "opposite source for the coherent bank")
    tail_error = (1-(1-4*p**9).sqrt())/2
    kraft_cost = 1+q
    kraft_marginal = divergence(q,l)/ell
    kraft_pred = kraft_marginal+mi_pred/ell
    direct_pred = ((1-pi)*divergence(l,l)+pi*divergence(u,l))/ell
    check(direct_pred.lo<=kraft_pred.hi and kraft_pred.lo<=direct_pred.hi,
          "Kraft gain chain rule on the physical two-column comparator")
    before_tail = kraft_cost-kraft_marginal-mi_event/ell
    check(before_tail.lo<=(1+l).hi and (1+l).lo<=before_tail.hi,
          "original compensated Golden target with the exact port reading")
    fine_gain = (-(1-q)*logarithm(p)-q*logarithm(p**3)-entropy(q))/ell
    difference = fine_gain-kraft_marginal
    check(difference.lo<=q.hi and q.lo<=difference.hi,
          "merging 10 with the dark 11 loses exactly q in Golden gain")
    # LC4 restores the literal unread tail to v or |0>. Rotating sector
    # zero varies this pair while keeping the two marked effects fixed.
    lc_root = (1-4*q*(1-q)*p).sqrt()
    lc_error = (1-lc_root)/2
    lc_log_odds = logarithm((1-lc_error)/lc_error)
    lc_q = base+p*(1-2*q)*lc_log_odds/(ell*lc_root)
    lc_angle = -2*q*(1-q)*p.sqrt()*p*lc_log_odds/(ell*lc_root)
    check(lc_q.lo>F("0.79513") and lc_angle.hi<F("-1.15421"), "independent LC4 rows")
    state_norm_constants = []
    for x in (l,u):
        c_x=((1-x)*logarithm((1-l)/(1-u))+x*logarithm(u/l))/(2*ell)
        state_norm_constants.append(c_x.fmt(12))
    def fmt(x):
        return x.fmt(12)
    print(json.dumps({
        "scope":"registered H.1 report and the indicated prediction targets at the literal PC13 centre",
        "predicate_prior":fmt(pi), "port_probability":fmt(Q),
        "report_given_rejected_predicate":fmt(l), "report_given_accepted_predicate":fmt(u),
        "mutual_information_nats":{"port":fmt(mi_event),"predicate":fmt(mi_pred),
                                   "whole_coherent_bank_after_CX":fmt(entropy(small))},
        "net_price_source_per_dq":{"port_prediction":fmt(base),
            "predicate_or_resolving_classical_bank":fmt(pred_slope),
            "unchanged_protected_reference":1,
            "whole_coherent_bank_after_CX":fmt(bank_slope)},
        "fixed_conditional_quantum_hypothesis":{"full_prior_range_lower_bound":fmt(global_floor),
            "true_centre_lower_bound":fmt(lower),"true_centre_upper_bound":fmt(upper),
            "trace_norm_constants_per_conditional_state_before_prior_weight":state_norm_constants},
        "literal_complement_after_lc4":{"accessible_posterior_error":fmt(lc_error),
            "net_price_per_dq":fmt(lc_q),"fixed_effect_angle_source_per_radian":fmt(lc_angle),
            "feedback_fixed_effect_angle_source":0},
        "conditional_golden_likelihood_gain":{"marginal_report_gain":fmt(kraft_marginal),
            "gain_with_resolving_predicate":fmt(kraft_pred),
            "optimal_net_without_tail":fmt(1+l),"optimal_net_with_tail":fmt(entropy(tail_error)/ell),
            "both_net_field_sources":0},
        "three_reference_sources_at_original_optimum":{"same_field_fresh_report":fmt(base),
            "golden_two_outcomes":0,"canonical_three_sectors":-1,
            "fine_minus_coarse_gain_at_centre":fmt(difference)},
        "complete_physical_price_derived":False
    },indent=2))


if __name__=="__main__":
    main()
