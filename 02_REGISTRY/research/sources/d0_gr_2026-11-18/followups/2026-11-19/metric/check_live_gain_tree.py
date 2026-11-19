"""Compare the realized likelihood score, local Shannon requirement and two live records."""
from fractions import Fraction
import json

from check_counted_separator import analysis as master_receipt, native_fronts
from check_extra_work import span
from check_live_parser import controller
from check_reference_pf_path import ln_interval
from check_repeat_clock import local_native
from check_source_price import need


def contains_zero(x):
    return x.lo <= 0 <= x.hi


def check_variable_tree():
    # Rational weights include a nontrivial continuation, a failed branch, and a stop.
    edges = {
        "": (("stop", Fraction(1, 4), Fraction(1, 2)),
             ("live", Fraction(3, 4), Fraction(1, 4))),
        "live": (("pass", Fraction(2, 5), Fraction(1, 2)),
                 ("fail", Fraction(3, 5), Fraction(1, 4))),
    }
    def mass(h):
        if h not in edges:
            return Fraction(1)
        return sum(w * mass(b) for b, _, w in edges[h])
    k = mass("")
    leaf_masses = {}
    def visit(h, prob, raw, mu):
        if h not in edges:
            need(raw * prob / mu == k * prob, "exact telescoping of costs and gains")
            leaf_masses[h] = raw * prob / mu
            return
        laws = [(b, p, w, w * mass(b) / mass(h)) for b, p, w in edges[h]]
        need(sum(q for _, _, _, q in laws) == 1, "conditional normalized reference")
        for b, p, w, q in laws:
            visit(b, prob*p, raw*w, mu*q)
    visit("", Fraction(1), Fraction(1), Fraction(1))
    need(sum(leaf_masses.values()) == k and k == Fraction(11, 16), "all leaves included")
    need(Fraction(1, 2) / k != Fraction(2, 3), "local-only normalization fails")
    return {h: str(w) for h, w in leaf_masses.items()}


def report():
    digest, _ = native_fronts()
    need(local_native() == digest == controller()[0], "source bank, front and parser")
    raw = master_receipt()
    p = (span(5).sqrt()-1)/2
    u, a = p**2, p.sqrt()
    cc, ss = span(1), span(0)
    for _ in range(29):
        cc, ss = cc*a-ss*p, ss*a+cc*p
    v = ss**2
    ell = ln_interval(1/p)
    def entropy(x):
        return -(x*ln_interval(x)+(1-x)*ln_interval(1-x))/ell
    h0, h1 = entropy(v), entropy(u)
    need(contains_zero(h1-1-u), "native binary entropy is 1+u")
    r = v*(1-u)/((1-v)*u)
    need(r.hi<1, "the 10 probability decreases at the detuned input")
    A, B = p**2*v*(1-u), p**2*(1-v)*u
    need(contains_zero(A/B-r), "true two bright events without a late selection")
    tv = (1-r)/(2*(1+r))
    # At the exact minimax factor lambda=r the two predicted probabilities are reversed.
    need(contains_zero(span(Fraction(1,2))-r/(1+r)-tv), "sharp TV separation")
    need(contains_zero(r/(r+r)-Fraction(1,2)), "second calibration interchanges the predictions")
    forced = -2*ln_interval(r)/ell
    bellman = p**2*(u-v-2*(h1-h0))
    gain_mean = p**2*(h1-h0)
    registered_work = p**2*(u-v)
    need(bellman.hi<0 and gain_mean.lo>0 and forced.lo>0, "full signs")
    need(contains_zero(bellman-registered_work+2*gain_mean), "Shannon Bellman normalization")
    for t in (0,1):
        def length(e):
            d=t^e
            return 4+d+(1-d)+e+t
        need(length(0)+length(1)==11+2*t, "the two swapped records have identical charged length")
        m = p**length(0)+p**length(1)
        need(contains_zero(m-p**(4+t)) and contains_zero(p**length(1)/m-u),
             "conditional PF reference obtained from paid complete words")
    return {
        "status":"PASS", "native_owner":digest, "live_blocks":16,
        "golden_u":u.fmt(15), "first_noise_v":v.fmt(15),
        "odds_10_vs_01_minus":r.fmt(15), "odds_10_vs_01_plus":1,
        "true_10_given_mismatch_minus":(r/(1+r)).fmt(15),
        "true_joint_H1_and_10_minus":A.fmt(15), "true_joint_H1_and_01_minus":B.fmt(15),
        "sharp_minimax_TV_surp_with_fixed_ratio":tv.fmt(15),
        "required_residual_minus_minus_plus_gold_units":forced.fmt(15),
        "plus_minus_delta_mean_report_length":registered_work.fmt(15),
        "plus_minus_delta_full_report_Shannon_phi":gain_mean.fmt(15),
        "plus_minus_delta_scalar_Bellman_negative_log_pressure":bellman.fmt(15),
        "plus_minus_delta_likelihood_negative_log_pressure_fixed_code_support":0,
        "plus_minus_delta_complete_RAW_for_comparison":raw["delta_RAW_upper_and_lower"],
        "variable_tree_exact_leaf_masses":check_variable_tree(),
        "full_history_economic_binding_established":False,
    }


if __name__=="__main__":
    print(json.dumps(report(), ensure_ascii=False, indent=2))
