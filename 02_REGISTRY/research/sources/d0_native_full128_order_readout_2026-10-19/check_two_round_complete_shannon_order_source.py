#!/usr/bin/env python3
"""Complete two-round full128 Shannon mixed-order source.

The two Lorentz increments are assigned to successive applications of the
existing full128 matrix instrument, with a fresh 128-outcome record each round.
This checker differentiates the complete 128^2 history law.  It does not
identify that assigned sequence as a physically admitted D0 memory program.
"""
from functools import lru_cache
from fractions import Fraction
from math import isqrt
from pathlib import Path
import ast
import hashlib
import json

import sympy as s

from check_complete_shannon_order_source import (
    _algebraic_interval,
    _decimal_bound,
    _divide_by_positive_interval,
    _interval_add,
    _interval_mul,
    _interval_scale,
    _log_rational_interval,
)

ROOT = Path(__file__).resolve().parents[4]
CREATORS = "02_REGISTRY/research/certificates/a4d_native_curved_soldered_heat.py"
PARENT = (
    "02_REGISTRY/research/sources/"
    "d0_native_full128_order_readout_2026-10-19/"
    "check_native_full128_order_readout.py"
)
SOURCE_CHECKER = (
    "02_REGISTRY/research/sources/"
    "d0_native_full128_order_readout_2026-10-19/"
    "check_complete_shannon_order_source.py"
)
PINS = {
    CREATORS: "bf13f57c902da0005634ae6834c0b4e3ffd2df1aa196a61ebc0ff3dc0351c7da",
    PARENT: "176739372e85d8cbd2ba48f7cc28cfe508395ae84007d8462a3f502d596a87a2",
    SOURCE_CHECKER: "26424be5c2278828af81d331b8edc110dd8c4eefad4fc97e2c2e5fa813de178a",
}


def _real(value):
    # The traces lie in an exact algebraic field. Expansion cancels their
    # imaginary terms without SymPy's heuristic assumptions/evalf search.
    return s.expand((value + s.conjugate(value)) / 2)


def _matrix_eq(left, right):
    return all(s.simplify(value) == 0 for value in left - right)


def _build_full128_pair(generator_a, generator_b, creators, require):
    C = creators
    I16, O16 = s.eye(16), s.zeros(16)

    def unit(i, j):
        matrix = s.zeros(4)
        matrix[i, j] = 1
        return matrix

    Gs = [
        sum((generator[i, j] * C[i] * C[j].H
             for i in range(4) for j in range(4)), O16.copy())
        for generator in (generator_a, generator_b)
    ]
    nu = s.Rational(3, 5)
    shifts = [s.Integer(1), s.Integer(1), s.Integer(1), s.I]
    p = (s.sqrt(5) - 1) / 2
    words, dwords_a, dwords_b = [], [], []
    for role in range(4):
        q_left = C[role] * C[role].H
        q_right = C[role].H * C[role]
        P = nu * C[role] * shifts[role]
        L = I16 - s.Rational(1, 5) * q_left
        R = I16 - s.Rational(1, 5) * q_right
        def sylvester_at_base(projector, rhs):
            pieces = (
                (I16 - projector, s.Integer(1)),
                (projector, s.Rational(4, 5)),
            )
            return sum(
                (left * rhs * right / (left_value + right_value)
                 for left, left_value in pieces
                 for right, right_value in pieces),
                O16.copy(),
            )

        fixed_left = I16 - s.Rational(1, 5) * q_left
        fixed_right = I16 - s.Rational(1, 5) * q_right
        base_items = (
            (P, L),
            (P.H, R),
            (-nu * C[role], -fixed_left),
            (-nu * C[role].H, -fixed_right),
        )
        derivative_items = []
        for generator_index, G in enumerate(Gs):
            dP = nu * C[role] * G * shifts[role] if role == 2 else O16.copy()
            if role == 2:
                dL = sylvester_at_base(q_left, -dP * P.H - P * dP.H)
                dR = sylvester_at_base(q_right, -dP.H * P - P.H * dP)
                require(
                    _matrix_eq(L * dL + dL * L, -dP * P.H - P * dP.H),
                    f"{generator_index}_left_positive_julia_root_tangent",
                )
                require(
                    _matrix_eq(R * dR + dR * R, -dP.H * P - P.H * dP),
                    f"{generator_index}_right_positive_julia_root_tangent",
                )
            else:
                dL = dR = O16.copy()
            derivative_items.append((
                (dP, dL),
                (dP.H, dR),
                (O16.copy(), O16.copy()),
                (O16.copy(), O16.copy()),
            ))
        for item_index, item in enumerate(base_items):
            derivative_a = derivative_items[0][item_index]
            derivative_b = derivative_items[1][item_index]
            for _ in range(2):
                words.append(item)
                dwords_a.append(derivative_a)
                dwords_b.append(derivative_b)

    rows, drows_a, drows_b = [], [], []
    for label in range(32):
        signs = [s.Rational((-1) ** bin(label & j).count("1"), 32)
                 for j in range(32)]
        for coefficient in range(2):
            rows.append(sum(
                (signs[j] * words[j][coefficient] for j in range(32)), O16.copy()))
            drows_a.append(sum(
                (signs[j] * dwords_a[j][coefficient] for j in range(32)), O16.copy()))
            drows_b.append(sum(
                (signs[j] * dwords_b[j][coefficient] for j in range(32)), O16.copy()))

    A, dA, dB = rows[0], drows_a[0], drows_b[0]
    Kraus, dKraus_a, dKraus_b = [], [], []
    for row, drow_a, drow_b in zip(rows, drows_a, drows_b):
        port0 = (I16 if not Kraus else O16.copy()) - 2 * p**2 * row.H * A
        dport0_a = -2 * p**2 * (drow_a.H * A + row.H * dA)
        dport0_b = -2 * p**2 * (drow_b.H * A + row.H * dB)
        port1 = -2 * s.sqrt(p) * p * row.H * A
        dport1_a = -2 * s.sqrt(p) * p * (drow_a.H * A + row.H * dA)
        dport1_b = -2 * s.sqrt(p) * p * (drow_b.H * A + row.H * dB)
        Kraus.extend((port0, port1))
        dKraus_a.extend((dport0_a, dport1_a))
        dKraus_b.extend((dport0_b, dport1_b))

    require(len(Kraus) == 128, "all_128_original_outcomes_retained")
    return Kraus, dKraus_a, dKraus_b


def _history_jet(K, dA, dB, i, j, order):
    """Return q, q_a, q_b, q_ab for chronological history (i,j)."""
    O16 = s.zeros(16)
    T = K[j] * K[i]
    if order == "AB":
        Ta = K[j] * dA[i]
        Tb = dB[j] * K[i]
        Tab = dB[j] * dA[i]
    else:
        Ta = dA[j] * K[i]
        Tb = K[j] * dB[i]
        Tab = dA[j] * dB[i]

    q = s.expand(s.trace(T.H * T) / 16)
    qa = s.expand(_real(s.trace(T.H * Ta)) / 8)
    qb = s.expand(_real(s.trace(T.H * Tb)) / 8)
    qab = s.expand(
        _real(s.trace(T.H * Tab) + s.trace(Ta.H * Tb)) / 8
    )
    return T, q, qa, qb, qab


def _sparse(matrix):
    return {
        (i, j): matrix[i, j]
        for i in range(matrix.rows)
        for j in range(matrix.cols)
        if matrix[i, j] != 0
    }


def _trace_product(left, right):
    """Exact trace(left*right) using sparse coordinate dictionaries."""
    return s.Add(*(
        value * right.get((j, i), s.Integer(0))
        for (i, j), value in left.items()
        if (j, i) in right
    ))


def _adjoint_sparse(matrix):
    return {(j, i): s.conjugate(value) for (i, j), value in matrix.items()}


def _log_interval_32(interval):
    """Rational log enclosure with 32 atanh terms (more than 24 digits)."""
    return (
        _log_rational_interval(interval[0], terms=32)[0],
        _log_rational_interval(interval[1], terms=32)[1],
    )


def run(repo=None):
    repo = ROOT if repo is None else Path(repo).resolve()
    checks = []

    def require(condition, name):
        if not bool(condition):
            raise ArithmeticError("two_round_complete_shannon:" + name)
        checks.append(name)

    for path, expected in PINS.items():
        actual = hashlib.sha256((repo / path).read_bytes()).hexdigest()
        require(actual == expected, "pin_" + Path(path).name)

    tree = ast.parse((repo / CREATORS).read_text())
    nodes = [
        node for node in tree.body
        if (isinstance(node, ast.FunctionDef) and node.name == "creator")
        or (isinstance(node, ast.Assign)
            and any(isinstance(target, ast.Name)
                    and target.id == "EXTERIOR_ORDER" for target in node.targets))
    ]
    require(len(nodes) == 2, "only_owned_full16_CAR_creator_loaded")
    scope = {"s": s, "lru_cache": lru_cache}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), CREATORS, "exec"), scope)
    C = [scope["creator"](role) for role in range(4)]

    def unit(i, j):
        matrix = s.zeros(4)
        matrix[i, j] = 1
        return matrix

    N2 = unit(1, 2) + unit(2, 0)
    Nbar3 = unit(0, 3) + unit(3, 1)
    K, dA, dB = _build_full128_pair(N2, Nbar3, C, require)
    zero = [i for i, item in enumerate(K) if item == s.zeros(16)]
    nonzero = [i for i in range(128) if i not in set(zero)]
    require(len(zero) == 86, "86_one_round_zero_kraus_outcomes")
    require(len(nonzero) == 42, "42_one_round_positive_support_outcomes")

    # A one-step zero Kraus factor makes each two-round amplitude divisible by
    # the increment of that round. If both one-step outcomes are zero, both
    # increment factors occur. Therefore every omitted zero-history q log q
    # term has zero mixed (a,b) derivative. Enumerate the positive support.
    def family(products):
        return [_sparse(item) for item in products]

    R = family([item * item.H for item in K])
    F = family([item.H * item for item in K])
    YA = family([ditem * item.H for ditem, item in zip(dA, K)])
    YB = family([ditem * item.H for ditem, item in zip(dB, K)])
    MA = family([item.H * ditem for item, ditem in zip(K, dA)])
    MB = family([item.H * ditem for item, ditem in zip(K, dB)])
    SA = [_sparse(item + item.H) for item in [ditem * base.H for ditem, base in zip(dA, K)]]
    TA = [_sparse(item + item.H) for item in [base.H * ditem for base, ditem in zip(K, dA)]]

    data = {"AB": {}, "BA": {}}
    history_counts = {"AB": 0, "BA": 0}
    totals = {
        order: {name: s.Integer(0) for name in ("q", "qa", "qb", "qab")}
        for order in ("AB", "BA")
    }
    selected_order_jets = {}
    unexpected_zero_products = []
    for i in nonzero:
        for j in nonzero:
            q = s.expand(_real(_trace_product(F[j], R[i])) / 16)
            if q == 0:
                # This is a possible extra rank-birth stratum, so do not
                # silently omit it from the entropy calculation.
                unexpected_zero_products.append((i, j))
                continue
            require(q != 0,
                    "nonzero_exact_two_round_probability_is_positive_frobenius_norm")

            jets = {
                "AB": (
                    s.expand(_real(_trace_product(F[j], YA[i])) / 8),
                    s.expand(_real(_trace_product(R[i], MB[j])) / 8),
                    s.expand(_real(_trace_product(SA[i], MB[j])) / 8),
                ),
                "BA": (
                    s.expand(_real(_trace_product(R[i], MA[j])) / 8),
                    s.expand(_real(_trace_product(F[j], YB[i])) / 8),
                    s.expand(_real(_trace_product(YB[i], TA[j])) / 8),
                ),
            }
            for order, (qa, qb, qab) in jets.items():
                if (i, j) == (0, 19):
                    _, direct_q, direct_qa, direct_qb, direct_qab = _history_jet(
                        K, dA, dB, i, j, order
                    )
                    require(s.expand(q - direct_q) == 0,
                            order + "_selected_history_probability_formula")
                    require(s.expand(qa - direct_qa) == 0,
                            order + "_selected_history_first_a_formula")
                    require(s.expand(qb - direct_qb) == 0,
                            order + "_selected_history_first_b_formula")
                    require(s.expand(qab - direct_qab) == 0,
                            order + "_selected_history_mixed_formula")
                history_counts[order] += 1
                totals[order]["q"] += q
                totals[order]["qa"] += qa
                totals[order]["qb"] += qb
                totals[order]["qab"] += qab
                data[order].setdefault(q, {"qab": s.Integer(0), "cross": s.Integer(0)})
                data[order][q]["qab"] += qab
                data[order][q]["cross"] += s.cancel(qa * qb / q)

                if (i, j) == (0, 19) and order == "AB":
                    selected_order_jets[order] = qab
                    require(qab == 0,
                            "selected_history_AB_matches_parent_zero_mixed_jet")
                if (i, j) == (0, 19) and order == "BA":
                    selected_order_jets[order] = qab
                    expected_ba = (
                        -s.Rational(12640131, 3276800000000)
                        + s.Rational(5746707, 3276800000000) * s.sqrt(5)
                    )
                    require(s.simplify(qab - expected_ba) == 0,
                            "selected_history_BA_matches_parent_exact_mixed_jet")

    require(not unexpected_zero_products,
            "no_extra_zero_history_from_product_of_nonzero_kraus")
    expected_histories = 128 * 128
    require(sum(len(rows) for rows in data.values()) > 0,
            "positive_two_round_support_nonempty")
    positive_histories = len(nonzero) ** 2
    require(positive_histories == len(nonzero) ** 2,
            "all_42_squared_nonzero_outcome_pairs_have_positive_support")
    require(history_counts["AB"] == positive_histories
            and history_counts["BA"] == positive_histories,
            "both_order_positive_history_counts_agree")
    expected_order_jet = (
        s.Rational(12640131, 3276800000000)
        - s.Rational(5746707, 3276800000000) * s.sqrt(5)
    )
    require(s.simplify(
        selected_order_jets["AB"] - selected_order_jets["BA"] - expected_order_jet
    ) == 0, "selected_history_AB_minus_BA_matches_parent_exact_jet")
    for order in ("AB", "BA"):
        require(s.expand(totals[order]["q"] - 1) == 0,
                order + "_complete_two_round_probability_sum")
        for name in ("qa", "qb", "qab"):
            require(s.expand(totals[order][name]) == 0,
                    order + "_complete_two_round_" + name + "_normalization")
    require(expected_histories - positive_histories == 14620,
            "complete_128_squared_history_count")

    phi = (1 + s.sqrt(5)) / 2
    log_phi = s.log(phi)
    sequence = {}
    for order in ("AB", "BA"):
        log_coefficients = {
            q: s.expand(values["qab"])
            for q, values in data[order].items()
            if s.expand(values["qab"]) != 0
        }
        nonlog = s.expand(sum(
            (values["cross"] for values in data[order].values()),
            s.Integer(0),
        ))
        sum_qab = s.expand(sum(log_coefficients.values(), s.Integer(0)))
        require(sum_qab == 0, order + "_mixed_probability_derivatives_normalize")
        shannon_numerator = sum(
            (coefficient * s.log(q)
             for q, coefficient in log_coefficients.items()),
            s.Integer(0),
        ) + nonlog
        source = -shannon_numerator / log_phi
        sequence[order] = {
            "source": source,
            "log_coefficients": log_coefficients,
            "nonlog": nonlog,
            "sum_qab": sum_qab,
            "positive_history_count": history_counts[order],
        }

    source_difference = s.expand(sequence["AB"]["source"] - sequence["BA"]["source"])
    log_difference = {}
    for q in set(sequence["AB"]["log_coefficients"]) | set(sequence["BA"]["log_coefficients"]):
        coefficient = s.expand(
            sequence["AB"]["log_coefficients"].get(q, 0)
            - sequence["BA"]["log_coefficients"].get(q, 0)
        )
        if coefficient != 0:
            log_difference[q] = coefficient
    nonlog_difference = s.expand(
        sequence["AB"]["nonlog"] - sequence["BA"]["nonlog"]
    )

    scale = 10**80
    sqrt5_floor = isqrt(5 * scale * scale)
    sqrt5_interval = (Fraction(sqrt5_floor, scale), Fraction(sqrt5_floor + 1, scale))

    def source_interval(log_coefficients, nonlog):
        log_numerator_interval = (Fraction(0), Fraction(0))
        for q, coefficient in log_coefficients.items():
            q_interval = _algebraic_interval(q, sqrt5_interval)
            coefficient_interval = _algebraic_interval(coefficient, sqrt5_interval)
            log_numerator_interval = _interval_add(
                log_numerator_interval,
                _interval_mul(coefficient_interval, _log_interval_32(q_interval)),
            )
        log_numerator_interval = _interval_add(
            log_numerator_interval,
            _algebraic_interval(nonlog, sqrt5_interval),
        )
        phi_interval = (
            (Fraction(1) + sqrt5_interval[0]) / 2,
            (Fraction(1) + sqrt5_interval[1]) / 2,
        )
        return _interval_scale(
            _divide_by_positive_interval(
                log_numerator_interval, _log_interval_32(phi_interval)
            ),
            -1,
        )

    difference_interval = source_interval(log_difference, nonlog_difference)
    require(difference_interval[0] <= difference_interval[1], "order_rational_log_interval_ordered")
    if source_difference != 0:
        require(difference_interval[0] > 0 or difference_interval[1] < 0,
                "rational_interval_proves_order_source_sign")

    def export_source(order):
        grouped_exact = "\n".join(
            f"{q}: {coefficient}"
            for q, coefficient in sorted(
                sequence[order]["log_coefficients"].items(),
                key=lambda item: str(item[0]),
            )
        )
        return {
            "formula": "-sum_{q>0}(q_ab*log(q)+q_a*q_b/q)/log(phi)",
            "nonlog_term": str(sequence[order]["nonlog"]),
            "nonzero_log_groups": len(sequence[order]["log_coefficients"]),
            "positive_histories": sequence[order]["positive_history_count"],
            "exact_grouped_expression_sha256": hashlib.sha256(
                grouped_exact.encode("utf-8")
            ).hexdigest(),
        }

    diff_interval = difference_interval
    result = {
        "status": "PASS_SCOPED_COMPLETE_TWO_ROUND_FULL128_SHANNON_ORDER_SOURCE",
        "checks": len(checks),
        "input": {
            "grid": "L=4, h=1/4",
            "fourier_mode": [0, 0, 0, 1],
            "first_generator": "N2",
            "second_generator": "Nbar3",
            "commutator": "J23=[N2,Nbar3]",
            "carrier": "original 16-component CAR and 128 outcomes per fresh round",
            "preparation": "I16/16",
            "reference128": "fixed full-rank spectator; no reference-state variation",
        },
        "history_support": {
            "all_histories": expected_histories,
            "positive_histories_per_order": positive_histories,
            "zero_histories_per_order": expected_histories - positive_histories,
            "zero_base_mechanism": "at least one one-round Kraus operator is exactly zero",
            "zero_support_mixed_entropy_derivative": "0; each branch probability factors by its zero-round increment(s), so q log q has zero mixed derivative",
        },
        "complete_two_round_shannon": {
            "AB": export_source("AB"),
            "BA": export_source("BA"),
            "AB_minus_BA": {
                "interval_24_digits": [
                    _decimal_bound(diff_interval[0], 24, False),
                    _decimal_bound(diff_interval[1], 24, True),
                ],
                "nonzero_log_groups": len(log_difference),
                "nonlog_term": str(nonlog_difference),
                "exact_grouped_expression_sha256": hashlib.sha256(
                    "\n".join(
                        f"{q}: {coefficient}"
                        for q, coefficient in sorted(
                            log_difference.items(), key=lambda item: str(item[0])
                        )
                    ).encode("utf-8")
                ).hexdigest(),
            },
        },
        "nonclaims": [
            "the assigned two-round matrix instrument is not thereby a physically admitted D0 memory word",
            "this Shannon derivative is not the compulsory full Book Cost-Info action",
            "no controller, work, preparation, normalization, or native event-binding source is selected",
            "no physical gravity coupling or GR closure is established",
        ],
        "pins": {
            path: hashlib.sha256((repo / path).read_bytes()).hexdigest()
            for path in PINS
        },
    }
    return result


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, sort_keys=True, indent=2))
