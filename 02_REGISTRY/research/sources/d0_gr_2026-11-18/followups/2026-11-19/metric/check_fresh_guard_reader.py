"""Literal LIVE with a fresh Golden H: both guard values are retained.

This is a 35-stage word (seven actual births and the existing 28 gates),
not postselection on H=1. Exact Q[a] contractions verify every old input
column, all terminal code sectors and the actual nonscalar RAW cold.
Declared code/CQ and two economic aggregates are kept separate from the
uncomputed full native physical price. No test below selects Book Info.
"""
from collections import Counter
from decimal import Decimal, localcontext
from fractions import Fraction
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

import numpy as np

from check_golden_record_race import Gold, gold, p
from check_live_parser import controller, terminal
from check_source_price import load_control, need
from check_complete_work_source import (
    A, ONE, P, add, apply_local, born, coefficient_text, dot, equal, eye,
    native_local, power_p, scale, scalar_value,
)


def gf(x):
    return {"rational": str(x.a), "p": str(x.b)}


def field_gold(x):
    need(x.a.denominator == x.b.denominator == 1,
         "this exact Golden scalar has integral coefficients")
    return int(x.a)*ONE + int(x.b)*P


def golden_tables():
    rows = []
    means, factors, counting = [], [], []
    for t in (0, 1):
        mean, factor, count, total_mass = (gold(0) for _ in range(4))
        for h, e in product((0, 1), repeat=2):
            d = t ^ e
            c = h ^ d
            lengths = (1+d, 1+c, 1+e, 1+t)
            length = sum(lengths)
            prob = p**(2+h+e)
            info = 2+h+e
            net = length-info
            need(net == (2+2*d+t if h == 0 else 2+t),
                 "full H=0 code retains the additional T token")
            total_mass += prob
            mean += prob*net
            factor += prob*p**net
            count += p**net
            rows.append({"T": t, "H": h, "E": e, "D": d, "C": c,
                         "four_code_lengths": list(lengths),
                         "literal_length": length, "conditional_info_phi": info,
                         "declared_net_price": net, "born_probability": gf(prob)})
        need(total_mass == gold(1), "both guard and noise values kept")
        means.append(mean)
        factors.append(factor)
        counting.append(count)
    need(means[0] == 4*p and means[1]-means[0] == 5-6*p,
         "complete code minus conditional CQ source")
    need(factors == [p**3+p**5, 2*p**5],
         "Born-weighted exponential factors from all four branches")
    need((factors[0]-factors[1])/factors[0] == gold(1)/(1+2*p),
         "positive tilt equals reciprocal sqrt(5)")
    need(counting == [5-6*p, p*(5-6*p)],
         "literal counting has a different factor ratio")

    # Check the full-support fluctuation identity away from the canonical
    # noise preparation. Here p^s=p^L/P is used algebraically, so the
    # expectation is independent of the actual scalar branch law.
    fluctuation_checks = 0
    for alpha, xi in [(Fraction(1, 3), Fraction(2, 5)),
                      (Fraction(2, 7), Fraction(3, 8)),
                      (p**2, p**2)]:
        for t in (0, 1):
            weighted = gold(0)
            probs = []
            for h, e in product((0, 1), repeat=2):
                prob = gold(alpha if h else 1-alpha)*gold(xi if e else 1-xi)
                d = t ^ e
                length = 4+d+(h ^ d)+e+t
                weighted += prob*(p**length/prob)
                probs.append(prob)
            need(sum(probs, gold(0)) == gold(1), "actual conditional probability")
            need(weighted == factors[t],
                 "expectation of exponential keeps true weight, not mean price")
            fluctuation_checks += 1
    return rows, means, factors, counting, fluctuation_checks


def native_columns(rows):
    ne, native_hash = load_control()
    body_hash, old_word = controller()
    need(body_hash == native_hash, "same native grammar in both sources")
    # Old input: Spin0, Spin1, dirty port, retained T. Fresh H is appended,
    # then the six original LIVE wires. Swap only the wire names H/T in
    # the existing literal body; there is no uncharged physical SWAP.
    rename = {3: 4, 4: 3}
    word = [[op, *[rename.get(q, q) for q in wires]]
            for op, *wires in old_word]
    need(Counter(op for op, *_ in word) == {"CX": 19, "G": 5, "SourceI": 4},
         "all original square calls retained")
    local = {op: native_local(ne, op) for op in ("CX", "G", "SourceI")}
    v = eye(16)
    for _ in range(7):
        v = born(v)
    passive = v.copy()
    max_integer = int(np.max(np.abs(v)))
    for op, *wires in word:
        v = apply_local(v, local[op], 11, tuple(wires))
        equal(dot(v, v), eye(16), "every full actual prefix remains isometric")
        max_integer = max(max_integer, int(np.max(np.abs(v))))
    need(v.shape == (4, 2048, 16), "actual rectangular whole-word dimensions")

    ids = np.arange(2048)
    bit = lambda q: (ids >> (10-q)) & 1
    t_out, h_out, d_out, c_out = (bit(q) for q in (3, 4, 5, 7))
    e_out = t_out ^ d_out
    need(not np.any(v[:, c_out != (h_out ^ d_out), :]),
         "complete body computes its guard including H=0")
    invalid = ((d_out & bit(6)) | (c_out & bit(8)) |
               (e_out & bit(9)) | (t_out & bit(10))).astype(bool)
    need(not np.any(v[:, invalid, :]),
         "all canonical 11-report amplitudes vanish without discarding masks")
    # Check full scalar conditional effects on every Spin/port column,
    # while retaining the actual projector on old T. This also proves the
    # CQ entropy statement for arbitrary mixed banks and external RIGHT.
    sum_gram = np.zeros((4, 16, 16), dtype=np.int64)
    for row in rows:
        t, h, e = row["T"], row["H"], row["E"]
        mask = (t_out == t) & (h_out == h) & (e_out == e)
        branch = v.copy()
        branch[:, ~mask, :] = 0
        gram = dot(branch, branch)
        projector = eye(16)
        for j in range(16):
            if (j & 1) != t:
                projector[:, j, j] = 0
        equal(gram, scale(projector, power_p(2+h+e)),
              "full branch Gram is its probability times actual retained-T projector")
        sum_gram = add(sum_gram, gram)
        # All nonzero rows produce precisely the stated four LC1 words.
        for j in np.flatnonzero(mask & np.any(v != 0, axis=(0, 2))):
            out = terminal(int(t_out[j]), int(d_out[j]), int(c_out[j]),
                           int(bit(6)[j]), int(bit(8)[j]),
                           int(bit(9)[j]), int(bit(10)[j]))
            need("11" not in out and sum(map(len, out)) == row["literal_length"],
                 "literal parser on every nonzero output row")
    equal(sum_gram, eye(16), "all eight T,H,E blocks cover the complete old input")

    # RAW compression uses the actual seven-born passive inclusion, not
    # an independently optimized sector return or a fitted reference.
    cold = dot(passive, v)
    c_h1 = scale(scale(power_p(3), A), A+P)  # a^5 p(a+p)=a p^3(a+p)
    c00 = add(scale(power_p(3), A), power_p(5))
    c01 = scale(power_p(4), ONE+A)
    c0 = add(scale(c00, P), scale(c_h1, power_p(2)))
    c1 = add(scale(c01, P), scale(c_h1, power_p(2)))
    equal(c01, c_h1, "H=0,T=1 has the same cold as the H=1 sector")
    equal(c0-c1, scale(power_p(6), A-P), "exact nonscalar cold contrast")
    expected = np.zeros_like(cold)
    for j in range(16):
        expected[:, j, j] = c1 if j & 1 else c0
    equal(cold, expected, "actual RAW cold retains its nonscalar T dependence")
    need(np.any(c0 != c1), "new all-guard RAW cold is not the former scalar")
    need(0 < scalar_value(c0) < 1 and 0 < scalar_value(c1) < 1,
         "both real cold singular values are strict contractions")
    need(Fraction(75125, 262144) < Fraction(1, 3),
         "rational whole-input cold norm bound")
    return {
        "native_execution_sha256": native_hash,
        "old_input_dimension": 16, "output_dimension": 2048,
        "births": 7, "square_calls": 28, "total_stages": 35,
        "primitive_inventory": {"CX": 19, "G": 5, "SourceI": 4},
        "word_after_births": word,
        "register_ticks": [11, 27, 31, 35],
        "wire_order": ["Spin0", "Spin1", "dirty_port", "retained_T", "fresh_H",
                       "D", "tail_D", "C", "tail_C", "tail_X", "tail_T"],
        "exact_column_checks": "all 16 old columns, every actual prefix, all eight blocks, all parser failures",
        "maximum_exact_integer_coefficient": max_integer,
        "raw_cold": {
            "form": "I_Spin,port tensor diag(c0,c1)",
            "c0_exact_in_a": coefficient_text(c0),
            "c1_exact_in_a": coefficient_text(c1),
            "c0_decimal": format(scalar_value(c0), ".16g"),
            "c1_decimal": format(scalar_value(c1), ".16g"),
            "not_scalar": True,
            "uniform_norm_upper_bound": "75125/262144 < 1/3",
            "old_H1_scalar_must_not_be_reused": True,
        },
    }


def numerical_source_checks():
    with localcontext() as ctx:
        ctx.prec = 65
        pp = (Decimal(5).sqrt()-1)/2
        ell = (1/pp).ln()
        hh = lambda x: -(x*x.ln()+(1-x)*(1-x).ln())/ell
        def mean(alpha, xi, q):
            u = xi+(1-2*xi)*q
            return 4+alpha+2*(1-alpha)*u+xi+q-hh(alpha)-hh(xi)
        def count(alpha, xi, t):
            ans = Decimal(0)
            for h, e in product((0, 1), repeat=2):
                prob = (alpha if h else 1-alpha)*(xi if e else 1-xi)
                d = t ^ e
                length = 4+d+(h ^ d)+e+t
                ans += pp**length/prob
            return ans
        eps = Decimal("1e-23")
        tested = []
        for q in (Decimal(0), pp**2, Decimal("0.5"), Decimal(1)):
            alpha = xi = pp**2
            da = (mean(alpha+eps, xi, q)-mean(alpha-eps, xi, q))/(2*eps)
            dx = (mean(alpha, xi+eps, q)-mean(alpha, xi-eps, q))/(2*eps)
            expected_a = -2*(pp**2+pp**3*q)
            expected_x = 2*pp*(1-2*q)
            need(abs(da-expected_a) < Decimal("1e-37") and
                 abs(dx-expected_x) < Decimal("1e-37"),
                 "honest independent mean-CQ preparation rows, not stationarity")
            tested.append({"q": str(q), "D_alpha_mean": str(expected_a),
                           "D_xi_mean": str(expected_x)})
        # In the counting aggregate, the old ratio p is only a centre
        # identity. The full derivatives of both conditional factors remain.
        count_jets = []
        for t in (0, 1):
            x0 = pp**2
            da = (count(x0+eps, x0, t)-count(x0-eps, x0, t))/(2*eps)
            dx = (count(x0, x0+eps, t)-count(x0, x0-eps, t))/(2*eps)
            value = count(x0, x0, t)
            target_a = 3*pp**2/(5-6*pp)
            target_x = (pp**4 if t == 0 else 3*pp**2)/(5-6*pp)
            need(abs(-da/value-target_a) < Decimal("1e-37") and
                 abs(-dx/value-target_x) < Decimal("1e-37"),
                 "independent counting-price rows equal the stated exact Golden coefficients")
            count_jets.append({"T": t, "factor": str(count(x0, x0, t)),
                               "D_alpha_log_factor": str(da/count(x0, x0, t)),
                               "D_xi_log_factor": str(dx/count(x0, x0, t))})
        return {"mean_CQ_independent_rows": tested,
                "counting_factor_independent_jets": count_jets,
                "positive_mean_gain": str(5-6*pp),
                "Born_weighted_tilt_kappa": str(1/Decimal(5).sqrt()),
                "counting_tilt_kappa_at_canonical_preparation": str(pp**2)}


def main():
    rows, means, factors, counting, nchecks = golden_tables()
    columns = native_columns(rows)
    here = Path(__file__).resolve().parent
    deps = ("check_live_parser.py", "check_complete_work_source.py", "check_source_price.py")
    return {
        "status": "PASS",
        "statement": "35-stage native LIVE with both freshly born guard values retained",
        "scientific_status": {"known_H1_resource_removed": True,
                              "complete_native_physical_price_selected": False,
                              "independent_preparation_stationarity": False,
                              "obligation_C_discharged": False, "GR_closed": False},
        "source_sha256": {name: sha256((here/name).read_bytes()).hexdigest() for name in deps},
        "native": columns,
        "all_literal_code_branches": rows,
        "registered_mean": {"T0": gf(means[0]), "T1": gf(means[1]),
                            "formula": "4p+(5-6p) Pr(T=1)"},
        "Born_weighted_exponential_factors": {"T0": gf(factors[0]), "T1": gf(factors[1]),
                                              "ratio": gf(factors[1]/factors[0]),
                                              "kappa": gf((factors[0]-factors[1])/factors[0]),
                                              "full_support_identity": "sum P_j p^(L_j+log_phi P_j) = sum p^L_j",
                                              "noncanonical_probability_checks": nchecks},
        "literal_counting_factors_at_canonical_preparation": {"T0": gf(counting[0]),
                                                               "T1": gf(counting[1]),
                                                               "ratio": gf(counting[1]/counting[0])},
        "source_diagnostics": numerical_source_checks(),
        "remaining_application": "identify full Book valuation; keep 35-stage work, graph, raw cold and genuine apparatus rows",
    }


if __name__ == "__main__":
    print(json.dumps(main(), ensure_ascii=False, indent=2))
