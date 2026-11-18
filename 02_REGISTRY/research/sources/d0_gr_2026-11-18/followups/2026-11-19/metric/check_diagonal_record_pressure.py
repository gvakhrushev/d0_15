"""Exact checks on the common field axis of restored binary H.1 reports."""
from collections import Counter
from itertools import combinations, product
from math import comb
import json

import sympy as sp


x = sp.Symbol("x", real=True)
factor = 1 + x**2


def require(test, message):
    if not test:
        raise ArithmeticError(message)


def multiplicity(poly):
    order = 0
    while sp.rem(poly, factor, x) == 0:
        poly = sp.div(poly, factor, x)[0]
        order += 1
    return order


def event_checks():
    """For three bits check all 254 nontrivial groupings of the readout."""
    counts = Counter()
    words = list(product((0, 1), repeat=3))
    for size in range(1, len(words)):
        for group in combinations(words, size):
            numerator = sum(x ** (2 * sum(word)) for word in group)
            order = multiplicity(numerator)
            counts[order] += 1
            imbalance = sum((-1) ** sum(word) for word in group)
            require((order == 0) == (imbalance != 0), "parity imbalance")
    for m in range(1, 9):
        parity = sum(comb(m, j) * x**(2*j) for j in range(0, m+1, 2))
        require(parity.subs(x, sp.I) == 2**(m-1), "even parity")
        for j in range(1, m+1):
            word_prefix = x**(2*j) * factor**(m-j)
            require(multiplicity(word_prefix) == m-j, "partial word")
    return dict(three_bit_events_by_factor_order=dict(sorted(counts.items())),
                all_prefix_lengths_through=8)


def exact_probe_construction():
    """Each paid probe has LC2 amplitudes in both valid and invalid sectors."""
    p = (sp.sqrt(5)-1)/2
    root_p = sp.sqrt(p)
    coeff = sp.Matrix([root_p, p*root_p, p*p])
    require(sp.simplify(coeff.dot(coeff)-1) == 0, "true LC2 birth masses")
    prepared = sp.Matrix([1, x, 0])
    z = sp.Rational(1, 2**20)
    outputs = {}
    for m in (1, 2, 3):
        overlap = sp.factor(prepared.dot(coeff))
        require(sp.simplify(overlap.subs(x, sp.I) *
                            sp.conjugate(overlap.subs(x, sp.I))) > 0,
                "full denominator at the complex pole")
        # The fixed cold test acts on M probes independent of all target bits.
        # Factorizing the computational-basis contractions avoids large matrices.
        probe_sum = (prepared.dot(prepared))**m
        weighted_probe = (1-z)*probe_sum + z*overlap**(2*m)
        for group in ("parity", "all_zero", "first_one"):
            if group == "parity":
                target = sum(comb(m, j)*x**(2*j) for j in range(0, m+1, 2))
            elif group == "all_zero":
                target = sp.Integer(1)
            else:
                target = x*x*factor**(m-1)
            joint = target*weighted_probe
            same_mark = sp.cancel(joint/(factor**m*weighted_probe)-target/factor**m)
            require(same_mark == 0, "joint target mark")
        outputs[str(m)] = {"target_copy_count": m, "sufficient_extra_probes": m,
                           "minimum_extra_probes_from_parity": m}
    return outputs


def calibration_bound():
    """Reconstruct the variable part from nine noisy parity tests for M=2."""
    m = 2
    d = factor**m
    event = 1 + x**4
    event_inverse = sp.invert(event, d, x)
    nodes = [sp.Rational(80+i, 100) for i in range(9)]
    low, high = nodes[0], nodes[-1]
    amplitude_error = sp.Rational(1, 10**30)
    # A=diag(1,1+e,1,1+e), acting on |00>,|01>,|10>,|11>.
    amp = 1+amplitude_error
    S = sp.expand(1 + x*x*(1+amp**2) + amp**2*x**4)
    N = 1 + amp**2*x**4
    R = sp.expand(d*N-event*S)
    H = sp.cancel(S/d)
    remainder = sp.Integer(0)
    C = sp.Integer(0)
    errors = []
    for node in nodes:
        lagrange = sp.prod((x-other)/(node-other) for other in nodes if node != other)
        T = -sp.rem(event_inverse*lagrange, d, x)
        remainder += T*R.subs(x, node)
        # The triangle inequality on [low,high] gives a rational upper bound
        # for |(T/d)'|. All nodes are positive, hence d(x)>=d(low).
        deriv_num = sp.Poly(sp.diff(T,x)*d-T*sp.diff(d,x), x)
        upper = sum(abs(c)*high**i for (i,),c in deriv_num.terms())/d.subs(x,low)**2
        C += d.subs(x,node)**2 * upper
        observed_error = (N/S-event/d).subs(x,node)
        require(sp.simplify(R.subs(x,node)-observed_error*d.subs(x,node)*
                           S.subs(x,node)) == 0, "normalized measured disparity")
        errors.append(abs(observed_error))
    require(sp.rem(S-remainder, d, x) == 0, "normalized pressure interpolation")
    require(sp.cancel(sp.diff(S/d, x)-sp.diff(remainder/d,x)) == 0, "full slope")
    delta = max(errors)
    require(0 < C*delta*(high-low) < 1, "positive stability denominator")
    bound = C*delta/(1-(high-low)*C*delta)
    # Here H=(1+amp^2 x^2)/(1+x^2), so this bound controls the whole interval.
    exact_slope_upper = 2*high*(amp**2-1)/((1+low**2)*(1+amp**2*low**2))
    require(sp.cancel(H-(1+amp**2*x*x)/factor) == 0, "actual test mass")
    require(0 < exact_slope_upper < bound, "uniform measured mass bound")
    return dict(nodes=[str(i) for i in nodes], positive_fixed_amplitude_error=str(amplitude_error),
                max_observed_mark_error=str(sp.N(delta,8)),
                certified_upper_bound_for_C=str(sp.N(C,8)),
                uniform_relative_slope_bound=str(sp.N(bound,8)),
                example_true_slope_upper=str(sp.N(exact_slope_upper,8)),
                variable_part_reconstructed_exactly=True,
                decimal_values="rounded displays of quantities bounded with rational arithmetic")


def main():
    print(json.dumps(dict(events=event_checks(), native_probe=exact_probe_construction(),
                          stability=calibration_bound(),
                          scope="fixed complete terminal on frozen restored conditional frames",
                          added_probes_are_new_paid_history=True,
                          GR_closed=False), indent=2))


if __name__ == "__main__":
    main()
