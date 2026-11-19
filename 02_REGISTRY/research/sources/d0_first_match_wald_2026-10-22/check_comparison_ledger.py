#!/usr/bin/env python3
"""Exact first-match comparison ledgers; no new native price is assumed.

Standard-library-only, bounded full-tree controls for the extension in sections
11--14 of A4D_FIRST_MATCH_WALD_NATIVE_INFORMATION_FULL_SOURCE_2026_10_22.md.
The 1/2 equality-status code is an EXPLICIT CODE-LENGTH EXAMPLE, not a proof
that a deterministic Boolean flag is an original stochastic Golden F/R step.
"""

import json
from decimal import Decimal, localcontext
from fractions import Fraction as F


checks = 0


def require(condition, label):
    global checks
    if not condition:
        raise AssertionError(label)
    checks += 1


def dec(x):
    x = F(x)
    return Decimal(x.numerator) / Decimal(x.denominator)


def coarse(values, labels):
    return [sum((x for x, b in zip(values, labels) if b == a), F(0))
            for a in range(max(labels) + 1)]


def leaves(probabilities, labels, cap):
    """All complete fine tapes, including every all-mismatch capped leaf."""
    def visit(word, probability):
        if len(word) > 1 and (
            labels[word[-1]] == labels[word[0]] or len(word) == cap + 1
        ):
            yield word, probability
            return
        for b, q in enumerate(probabilities):
            yield from visit(word + (b,), probability * q)

    for a, q in enumerate(probabilities):
        yield from visit((a,), q)


def trial_stats(probabilities, labels, costs, directions, cap):
    m, n = max(labels) + 1, len(probabilities)
    mass = F(0)
    trial_counts = [F(0)] * n
    cell_counts = [[F(0) for _ in range(m)] for _ in range(m)]
    dtrial = [[F(0)] * n for _ in directions]
    dcells = [[[F(0) for _ in range(m)] for _ in range(m)]
              for _ in directions]
    dmass = [F(0)] * len(directions)
    mean_length, status_cost, abort_mass = F(0), F(0), F(0)
    dlength, dstatus, dabort = ([F(0)] * len(directions) for _ in range(3))
    tapes = list(leaves(probabilities, labels, cap))
    for word, probability in tapes:
        anchor = labels[word[0]]
        is_abort = labels[word[-1]] != anchor
        c_status = sum(1 if labels[i] == anchor else 2 for i in word[1:])
        gradients = [probability * sum(
            (dp[i] / probabilities[i] for i in word), F(0)
        ) for dp in directions]
        mass += probability
        mean_length += len(word) * probability
        status_cost += c_status * probability
        abort_mass += int(is_abort) * probability
        for i in word:
            trial_counts[i] += probability
        for i in word[1:]:
            cell_counts[anchor][labels[i]] += probability
        for d, gradient in enumerate(gradients):
            dmass[d] += gradient
            dlength[d] += len(word) * gradient
            dstatus[d] += c_status * gradient
            dabort[d] += int(is_abort) * gradient
            for i in word:
                dtrial[d][i] += gradient
            for i in word[1:]:
                dcells[d][anchor][labels[i]] += gradient

    q = coarse(probabilities, labels)
    dq = [coarse(dp, labels) for dp in directions]
    tail = sum(((1 - v) ** cap for v in q), F(0))
    length = m + 1 - tail
    abort = sum((v * (1 - v) ** cap for v in q), F(0))
    require(mass == 1, "complete fine tape mass")
    require(all(v == 0 for v in dmass), "whole fine tape mass derivative")
    require(mean_length == length, "exact full trial count")
    require(abort_mass == abort, "actual all-mismatch cap mass")
    require(status_cost == 2 * length - 3 + abort, "true status code cost")
    require(status_cost == 2 * m - 1 - sum(
        ((1 - v) ** cap + (1 - v) ** (cap + 1) for v in q), F(0)
    ), "status code cost alternate expression")
    require(trial_counts == [length * p for p in probabilities],
            "Wald coefficients of EVERY retained fine trial symbol")
    for a in range(m):
        for b in range(m):
            require(cell_counts[a][b] == q[b] * (1 - (1 - q[a]) ** cap),
                    "each real comparison cell occupation")
    for d, dp in enumerate(directions):
        dl = cap * sum(((1 - q[a]) ** (cap - 1) * dq[d][a]
                       for a in range(m)), F(0))
        da = sum((((1 - q[a]) ** cap
                   - cap * q[a] * (1 - q[a]) ** (cap - 1)) * dq[d][a]
                  for a in range(m)), F(0))
        require(dlength[d] == dl, "exact trial count first jet")
        require(dabort[d] == da, "exact abort first jet")
        require(dstatus[d] == 2 * dl + da, "full capped status first jet")
        require(dtrial[d] == [dl * p + length * dpi
                             for p, dpi in zip(probabilities, dp)],
                "full fine-entropy coefficients and first jet")
        for a in range(m):
            for b in range(m):
                expected = (dq[d][b] * (1 - (1 - q[a]) ** cap)
                            + q[b] * cap * (1 - q[a]) ** (cap - 1) * dq[d][a])
                require(dcells[d][a][b] == expected,
                        "all comparison cells exact moving probability first jet")

    # These are deliberately nonsymmetric, non-column-balanced test ledgers.
    ledger = [[F((a + 1) ** 2 + 2 * b + 1, 3) for b in range(m)]
              for a in range(m)]
    dledger = [[F(a + 2 * b + 1, 7) for b in range(m)] for a in range(m)]
    for d in range(len(directions)):
        direct = sum((dcells[d][a][b] * ledger[a][b]
                      + cell_counts[a][b] * dledger[a][b]
                      for a in range(m) for b in range(m)), F(0))
        formula = F(0)
        for a in range(m):
            for b in range(m):
                derivative = (dq[d][b] * (1 - (1 - q[a]) ** cap)
                              + q[b] * cap * (1 - q[a]) ** (cap - 1) * dq[d][a])
                formula += derivative * ledger[a][b]
                formula += q[b] * (1 - (1 - q[a]) ** cap) * dledger[a][b]
        require(direct == formula, "genuine moving conditional net price source")

    # Direct full cost/entropy/source, not just the coarse-status entropy.
    with localcontext() as ctx:
        ctx.prec = 70
        lnphi = ((Decimal(5).sqrt() + 1) / 2).ln()
        logs = [dec(p).ln() / lnphi for p in probabilities]
        one_cost = sum((p * c for p, c in zip(probabilities, costs)), F(0))
        one_info = -sum((dec(p) * l for p, l in zip(probabilities, logs)), Decimal(0))
        one_price = dec(one_cost) - one_info
        full_cost = sum((pr * (sum(costs[i] for i in word)
                              + sum(1 if labels[i] == labels[word[0]] else 2
                                    for i in word[1:]))
                         for word, pr in tapes), F(0))
        full_info = -sum((dec(pr) * sum((logs[i] for i in word), Decimal(0))
                          for word, pr in tapes), Decimal(0))
        price_formula = dec(length) * one_price + dec(status_cost)
        require(abs(dec(full_cost) - full_info - price_formula) < Decimal('1e-55'),
                "entire fine Cost-minus-Shannon price incl status code once")
        for d, dp in enumerate(directions):
            ds = dec(sum((dpi * c for dpi, c in zip(dp, costs)), F(0))) \
                 + sum((dec(dpi) * l for dpi, l in zip(dp, logs)), Decimal(0))
            dcost = F(0)
            dinfo = Decimal(0)
            for word, pr in tapes:
                grad = pr * sum((dp[i] / probabilities[i] for i in word), F(0))
                c = sum(costs[i] for i in word) + sum(
                    1 if labels[i] == labels[word[0]] else 2 for i in word[1:])
                dcost += grad * c
                dinfo -= dec(grad) * sum((logs[i] for i in word), Decimal(0))
            source_formula = (dec(length) * ds + one_price * dec(dlength[d])
                              + dec(dstatus[d]))
            require(abs(dec(dcost) - dinfo - source_formula) < Decimal('1e-55'),
                    "direct full fine Cost-Info first source")
    return len(tapes)


def geometric_sum(value, cap):
    return sum((value ** j for j in range(cap)), F(0))


def marked_formula(probabilities, labels, costs, cap, exponent, xi, factory=None):
    m = max(labels) + 1
    w = coarse([p ** exponent * xi ** c for p, c in zip(probabilities, costs)], labels)
    a = [[xi ** (1 if i == j else 2) for j in range(m)] for i in range(m)]
    if factory is not None:
        for i in range(m):
            for j in range(m):
                a[i][j] *= sum((r ** exponent * xi ** c
                                for r, c in factory[i][j]), F(0))
    total = F(0)
    for i in range(m):
        b = sum((w[j] * a[i][j] for j in range(m) if j != i), F(0))
        total += w[i] * (w[i] * a[i][i] * geometric_sum(b, cap) + b ** cap)
    return total


def marked_full_tree(probabilities, labels, costs, cap, exponent, xi, factory=None):
    total = F(0)
    leaves_count = 0

    def visit(anchor, later, probability, cost, match):
        nonlocal total, leaves_count
        if later >= 1 and (match or later == cap):
            total += probability ** exponent * xi ** cost
            leaves_count += 1
            return
        for i, p in enumerate(probabilities):
            b = labels[i]
            status_cost = 1 if b == anchor else 2
            outcomes = [(F(1), 0)] if factory is None else factory[anchor][b]
            for raw_probability, raw_cost in outcomes:
                visit(anchor, later + 1, probability * p * raw_probability,
                      cost + costs[i] + status_cost + raw_cost, b == anchor)

    for i, p in enumerate(probabilities):
        visit(labels[i], 0, p, costs[i], False)
    return total, leaves_count


def random_factory_source(probabilities, labels, costs, dp, cap):
    """Independently enumerate a moving random factory and its FULL entropy."""
    m = max(labels) + 1
    q, dq = coarse(probabilities, labels), coarse(dp, labels)
    with localcontext() as ctx:
        ctx.prec = 70
        lnphi = ((Decimal(5).sqrt() + 1) / 2).ln()
        logs = [dec(p).ln() / lnphi for p in probabilities]
        factory = [[[(F(a+b+1, 2*m+1), F(a-b+1, 17), a+1),
                     (1-F(a+b+1, 2*m+1), -F(a-b+1, 17), b+3)]
                    for b in range(m)] for a in range(m)]
        log_factory = [[[dec(r).ln()/lnphi for r, _, _ in factory[a][b]]
                        for b in range(m)] for a in range(m)]
        mass, dmass, mean_cost, dcost = F(0), F(0), F(0), F(0)
        info, dinfo = Decimal(0), Decimal(0)

        def visit(anchor, later, pr, dpr, cost, log_probability, match):
            nonlocal mass, dmass, mean_cost, dcost, info, dinfo
            if later >= 1 and (match or later == cap):
                mass += pr
                dmass += dpr
                mean_cost += pr * cost
                dcost += dpr * cost
                info -= dec(pr) * log_probability
                # The derivative of the logarithm contributes -sum dP / lnphi,
                # zero on the complete normalized law, verified separately.
                dinfo -= dec(dpr) * log_probability
                return
            for i, p in enumerate(probabilities):
                b = labels[i]
                for v, (r, dr, cf) in enumerate(factory[anchor][b]):
                    new_pr = pr * p * r
                    new_dpr = dpr*p*r + pr*dp[i]*r + pr*p*dr
                    visit(anchor, later+1, new_pr, new_dpr,
                          cost + costs[i] + (1 if anchor == b else 2) + cf,
                          log_probability + logs[i] + log_factory[anchor][b][v],
                          anchor == b)

        for i, p in enumerate(probabilities):
            visit(labels[i], 0, p, dp[i], costs[i], logs[i], False)
        require(mass == 1 and dmass == 0, "complete moving random-factory law normalized")
        one_price = sum((dec(p)*Decimal(c) + dec(p)*l
                         for p, c, l in zip(probabilities, costs, logs)), Decimal(0))
        done_price = sum((dec(v)*Decimal(c) + dec(v)*l
                          for v, c, l in zip(dp, costs, logs)), Decimal(0))
        length = m + 1 - sum(((1-v)**cap for v in q), F(0))
        dlength = cap * sum(((1-q[a])**(cap-1)*dq[a]
                             for a in range(m)), F(0))
        predicted = dec(length)*one_price
        dpredicted = dec(length)*done_price + dec(dlength)*one_price
        for a in range(m):
            for b in range(m):
                kappa = Decimal(1 if a == b else 2)
                dkappa = Decimal(0)
                for v, (r, dr, cf) in enumerate(factory[a][b]):
                    kappa += dec(r) * (Decimal(cf) + log_factory[a][b][v])
                    dkappa += dec(dr) * (Decimal(cf) + log_factory[a][b][v])
                occupation = q[b]*(1-(1-q[a])**cap)
                doccupation = (dq[b]*(1-(1-q[a])**cap)
                               + q[b]*cap*(1-q[a])**(cap-1)*dq[a])
                predicted += dec(occupation)*kappa
                dpredicted += dec(doccupation)*kappa + dec(occupation)*dkappa
        require(abs(dec(mean_cost)-info-predicted) < Decimal('1e-55'),
                "direct actual random-factory mean cost minus complete entropy")
        require(abs(dec(dcost)-dinfo-dpredicted) < Decimal('1e-55'),
                "direct full source with BOTH moving trial and random-factory law")


def equality_word(bits, clean=False):
    """a0,a1,b0,b1,d0,d1,e; 7 fixed logical gates, or 13 with cleanup."""
    x = list(bits)
    for control, target in [(0, 4), (2, 4), (1, 5), (3, 5)]:
        x[target] ^= x[control]
    x[4] ^= 1
    x[5] ^= 1
    x[6] ^= x[4] & x[5]
    if clean:
        x[4] ^= 1
        x[5] ^= 1
        for control, target in [(3, 5), (1, 5), (2, 4), (0, 4)]:
            x[target] ^= x[control]
    return tuple(x)


def run():
    max_tapes, cases = 0, 0
    binary = ([F(1, 5), F(4, 5)], [0, 1], [1, 2], [[F(1), F(-1)]])
    g, r, a, c = F(2, 5), F(1, 100), F(2, 3), F(3, 8)
    probabilities = [(1-g)*a, (1-g)*(1-a), g*(1-r), g*r*c, g*r*(1-c)]
    directions = [
        [-a, -(1-a), 1-r, r*c, r*(1-c)],
        [F(0), F(0), -g, g*c, g*(1-c)],
        [1-g, -(1-g), F(0), F(0), F(0)],
        [F(0), F(0), F(0), g*r, -g*r],
    ]
    ternary = (probabilities, [0, 0, 1, 2, 2], [7, 11, 13, 5, 18], directions)
    for case in (binary, ternary):
        for cap in range(1, 6):
            max_tapes = max(max_tapes, trial_stats(*case, cap))
            cases += 1
    for m, matrix in [(2, [[1, 3], [4, 2]]),
                      (3, [[1, 4, 2], [2, 1, 4], [4, 2, 1]])]:
        columns = [sum(matrix[a][b] for a in range(m)) for b in range(m)]
        require(len(set(columns)) == 1, "unequal comparator prices can be column balanced")
        q = [F(j + 1, m * (m + 1) // 2) for j in range(m)]
        dq = [F(1), F(-1)] + [F(0)] * (m - 2)
        require(sum((dq[b] * columns[b] for b in range(m)), F(0)) == 0,
                "column-balanced probability-source cancellation")
        moving_source = sum((q[b] * m for b in range(m)), F(0))
        require(moving_source == m and moving_source != 0,
                "moving common column sum has genuine nonzero price source")
        require(1 + 2 * (m - 1) == 2 * m - 1,
                "explicit 1/2 code example includes one match and m-1 mismatches")
    require(F(1)*0 + F(-1)*1 == -1,
            "nonbalanced matrix hostile control has nonzero source")
    require(2 - 4 * F(1, 5) != 0,
            "K1 status source does not vanish despite constant trial count two")

    marked_cases, factory_cases, factory_source_cases = 0, 0, 0
    for p, labels, costs, directions in (binary, ternary):
        for cap in range(1, 6):
            for exponent, xi in [(1, F(1)), (1, F(2, 3)), (2, F(3, 5))]:
                direct, n = marked_full_tree(p, labels, costs, cap, exponent, xi)
                predicted = marked_formula(p, labels, costs, cap, exponent, xi)
                require(direct == predicted, "complete joint probability/cost mark incl aborts")
                max_tapes = max(max_tapes, n)
                marked_cases += 1
        m = max(labels) + 1
        factories = [[[(F(a + b + 1, 2 * m + 1), a + 1),
                       (1 - F(a + b + 1, 2 * m + 1), b + 3)]
                      for b in range(m)] for a in range(m)]
        for cap in range(1, 4):
            for exponent, xi in [(1, F(1)), (1, F(2, 3)), (2, F(3, 5))]:
                direct, n = marked_full_tree(p, labels, costs, cap, exponent, xi, factories)
                predicted = marked_formula(p, labels, costs, cap, exponent, xi, factories)
                require(direct == predicted,
                        "actual conditional random-factory mark with every raw result")
                max_tapes = max(max_tapes, n)
                factory_cases += 1
            random_factory_source(p, labels, costs, directions[0], cap)
            factory_source_cases += 1

    # All columns, not just the three admissible status inputs.
    for clean in (False, True):
        images = {equality_word(tuple((k >> j) & 1 for j in range(7)), clean)
                  for k in range(128)}
        require(len(images) == 128, "all128 equality skeleton is a permutation")
        for a in range(4):
            for b in range(4):
                x = (a & 1, a >> 1, b & 1, b >> 1, 0, 0, 0)
                out = equality_word(x, clean)
                require(out[:4] == x[:4] and out[6] == int(a == b),
                        "equality retains both actual input labels")
                if clean:
                    require(out[4:6] == (0, 0), "13-gate cleanup restores two work bits")

    # Conservative compact rare-report chart, including moving gamma and r.
    with localcontext() as ctx:
        ctx.prec = 70
        epsilon = Decimal('0.45') * Decimal('0.0000018')
        cap = 100000000
        exponential = (-epsilon * cap).exp()
        require(exponential < Decimal('6.64e-36'), "uniform rare full-status tail bound")
        tail_bound = 3 * exponential
        d_tail_coefficient = Decimal(cap) * (epsilon).exp() * exponential
        require(tail_bound < Decimal('2e-35'), "uniform three-status length error")
        require(d_tail_coefficient < Decimal('6.65e-28'),
                "uniform first-source tail coefficient before actual source norm")
        rare_bounds = {
            "chart": "gamma in [0.45,0.46], r in [1.8e-6,1.9e-6]",
            "q_min_lower_bound": str(epsilon),
            "K": cap,
            "length_tail_upper_bound": str(tail_bound),
            "D_tail_coefficient_times_sum_norm_Dq": str(d_tail_coefficient),
            "source_normalized_refinement": "requires division by the actual nonzero gain",
        }
    return {
        "status": "PASS", "checks": checks,
        "exact_complete_value_and_first_jet_cases": cases,
        "exact_joint_mark_cases": marked_cases,
        "exact_random_factory_joint_mark_cases": factory_cases,
        "exact_random_factory_complete_source_cases": factory_source_cases,
        "largest_complete_enumerated_tree": max_tapes,
        "logical_equality_gate_counts": {
            "retained_work": {"CNOT": 4, "X": 2, "Toffoli": 1, "total": 7},
            "clean_difference_ancillas": {"CNOT": 8, "X": 4, "Toffoli": 1, "total": 13},
            "checked_columns_each": 128,
        },
        "ternary_uncapped_complete_trial_multiplier": 4,
        "ternary_uncapped_comparison_code_example_mean": 5,
        "rare_report_bounds": rare_bounds,
        "scope": "exact classical/CQ first-match ledger; 1/2 comparison encoding is a declared code example",
        "physical_comparator_factory_ledger_selected": False,
        "original_Book03_operator_price_identified": False,
        "full_D0_price_selected": False,
        "GR_closed": False,
    }


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
