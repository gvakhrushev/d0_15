#!/usr/bin/env python3
"""Exact first Shannon source of the complete original full128 outcome law.

This isolates one first jet from the full instrument.  It does not identify the
complete Book Cost-Info action or claim physical admission of the link tangent.
"""
from functools import lru_cache
from fractions import Fraction
from math import isqrt
from pathlib import Path
import ast
import hashlib
import json

import sympy as s

ROOT = Path(__file__).resolve().parents[4]
CREATORS = "02_REGISTRY/research/certificates/a4d_native_curved_soldered_heat.py"
PARENT = (
    "02_REGISTRY/research/sources/"
    "d0_native_full128_order_readout_2026-10-19/"
    "check_native_full128_order_readout.py"
)
PINS = {
    CREATORS: "bf13f57c902da0005634ae6834c0b4e3ffd2df1aa196a61ebc0ff3dc0351c7da",
    PARENT: "176739372e85d8cbd2ba48f7cc28cfe508395ae84007d8462a3f502d596a87a2",
}


def _interval_add(left, right):
    return (left[0] + right[0], left[1] + right[1])


def _interval_mul(left, right):
    values = (left[0] * right[0], left[0] * right[1],
              left[1] * right[0], left[1] * right[1])
    return (min(values), max(values))


def _interval_scale(interval, scalar):
    return _interval_mul(interval, (Fraction(scalar), Fraction(scalar)))


def _log_rational_interval(value, terms=64):
    """Rational enclosure for log(value), using the atanh series and tail."""
    if value <= 0:
        raise ValueError("log interval requires a positive rational")
    shift = 0
    reduced = value
    while reduced < 1:
        reduced *= 2
        shift -= 1
    while reduced >= 2:
        reduced /= 2
        shift += 1

    def unit_log(x):
        t = (x - 1) / (x + 1)
        lower = 2 * sum(
            (t ** (2 * j + 1) / (2 * j + 1) for j in range(terms)),
            Fraction(0),
        )
        remainder = (2 * t ** (2 * terms + 1)
                     / ((2 * terms + 1) * (1 - t * t)))
        return (lower, lower + remainder)

    ln_reduced = unit_log(reduced)
    ln_two = unit_log(Fraction(2))
    return _interval_add(ln_reduced, _interval_scale(ln_two, shift))


def _algebraic_interval(value, sqrt5_interval):
    root5 = s.sqrt(5)
    expanded = s.expand(value)
    constant = s.simplify(expanded.subs(root5, 0))
    radical = s.simplify((expanded - constant) / root5)
    if not constant.is_Rational or not radical.is_Rational:
        raise ArithmeticError("expected a Q(sqrt(5)) coefficient")
    a = Fraction(int(constant.p), int(constant.q))
    b = Fraction(int(radical.p), int(radical.q))
    return _interval_add(
        (a, a), _interval_mul((b, b), sqrt5_interval))


def _log_interval(interval):
    return (_log_rational_interval(interval[0])[0],
            _log_rational_interval(interval[1])[1])


def _divide_by_positive_interval(numerator, denominator):
    if denominator[0] <= 0:
        raise ArithmeticError("positive denominator interval required")
    reciprocal = (1 / denominator[1], 1 / denominator[0])
    return _interval_mul(numerator, reciprocal)


def _decimal_bound(value, digits, upper):
    scale = 10 ** digits
    scaled = value * scale
    integer = (-((-scaled).numerator // (-scaled).denominator)
               if upper else scaled.numerator // scaled.denominator)
    sign = "-" if integer < 0 else ""
    magnitude = abs(integer)
    return (f"{sign}{magnitude // scale}."
            f"{magnitude % scale:0{digits}d}")


def run(repo=None):
    repo = ROOT if repo is None else Path(repo).resolve()
    checks = []

    def require(condition, name):
        if not bool(condition):
            raise ArithmeticError("complete_shannon_order_source:" + name)
        checks.append(name)

    def matrix_eq(left, right, name):
        require(all(s.simplify(value) == 0 for value in left - right), name)

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
    require(len(nodes) == 2, "only_owned_CAR_creator_and_order_loaded")
    scope = {"s": s, "lru_cache": lru_cache}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), CREATORS, "exec"), scope)
    C = [scope["creator"](role) for role in range(4)]
    I16, O16 = s.eye(16), s.zeros(16)

    def unit(i, j):
        matrix = s.zeros(4)
        matrix[i, j] = 1
        return matrix

    J23 = unit(2, 3) - unit(3, 2)
    GJ = sum(
        (J23[i, j] * C[i] * C[j].H
         for i in range(4) for j in range(4)),
        O16.copy(),
    )
    h, nu = s.Rational(1, 4), s.Rational(3, 5)
    shifts = [s.Integer(1), s.Integer(1), s.Integer(1), s.I]
    p = (s.sqrt(5) - 1) / 2

    words, dwords = [], []
    for role in range(4):
        q_left = C[role] * C[role].H
        q_right = C[role].H * C[role]
        P = nu * C[role] * shifts[role]
        L = I16 - s.Rational(1, 5) * q_left
        R = I16 - s.Rational(1, 5) * q_right
        dP = nu * C[role] * GJ * shifts[role] if role == 2 else O16.copy()

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

        if role == 2:
            dL = sylvester_at_base(q_left, -dP * P.H - P * dP.H)
            dR = sylvester_at_base(q_right, -dP.H * P - P.H * dP)
            matrix_eq(L * dL + dL * L, -dP * P.H - P * dP.H,
                      "left_defect_root_exact_sylvester")
            matrix_eq(R * dR + dR * R, -dP.H * P - P.H * dP,
                      "right_defect_root_exact_sylvester")
        else:
            dL = dR = O16.copy()

        fixed_left = I16 - s.Rational(1, 5) * q_left
        fixed_right = I16 - s.Rational(1, 5) * q_right
        items = (
            ((P, L), (dP, dL)),
            ((P.H, R), (dP.H, dR)),
            ((-nu * C[role], -fixed_left), (O16.copy(), O16.copy())),
            ((-nu * C[role].H, -fixed_right), (O16.copy(), O16.copy())),
        )
        for item, derivative in items:
            for _ in range(2):
                words.append(item)
                dwords.append(derivative)

    rows, drows = [], []
    for label in range(32):
        signs = [s.Rational((-1) ** bin(label & j).count("1"), 32)
                 for j in range(32)]
        for coefficient in range(2):
            rows.append(sum(
                (signs[j] * words[j][coefficient] for j in range(32)), O16.copy()))
            drows.append(sum(
                (signs[j] * dwords[j][coefficient] for j in range(32)), O16.copy()))

    A, dA = rows[0], drows[0]
    Ks, dKs = [], []
    for row, drow in zip(rows, drows):
        port0 = (I16 if not Ks else O16.copy()) - 2 * p**2 * row.H * A
        dport0 = -2 * p**2 * (drow.H * A + row.H * dA)
        port1 = -2 * s.sqrt(p) * p * row.H * A
        dport1 = -2 * s.sqrt(p) * p * (drow.H * A + row.H * dA)
        Ks.extend((port0, port1))
        dKs.extend((dport0, dport1))

    completeness = sum((K.H * K for K in Ks), O16.copy())
    tangent_completeness = sum(
        (K.H * dK + dK.H * K for K, dK in zip(Ks, dKs)), O16.copy())
    matrix_eq(completeness, I16, "all_128_kraus_effects_complete")
    matrix_eq(tangent_completeness, O16,
              "all_128_first_probability_derivatives_normalize")

    probabilities, derivatives = [], []
    for K, dK in zip(Ks, dKs):
        probabilities.append(s.simplify(s.trace(K.H * K) / 16))
        derivatives.append(s.simplify(
            (s.trace(dK.H * K) + s.trace(K.H * dK)) / 16))
    require(s.simplify(sum(probabilities) - 1) == 0,
            "maximally_mixed_full16_probability_sum_one")
    require(s.simplify(sum(derivatives)) == 0,
            "maximally_mixed_full16_source_sum_zero")

    groups = {}
    for index, (q, dq) in enumerate(zip(probabilities, derivatives)):
        groups.setdefault(q, []).append((index, dq))
    group_rows = []
    positive_terms = []
    zero_indices = []
    port1_source = s.Integer(0)
    for q, entries in groups.items():
        aggregate = s.simplify(sum((dq for _, dq in entries), s.Integer(0)))
        if q == 0:
            zero_indices.extend(index for index, _ in entries)
            require(all(dq == 0 for _, dq in entries),
                    "each_zero_base_probability_has_zero_first_jet")
        else:
            require(q.is_positive is True,
                    "positive_base_probability_group_" + str(len(positive_terms)))
            positive_terms.append((q, aggregate))
        group_rows.append({
            "probability": str(q),
            "multiplicity": len(entries),
            "source_sum": str(aggregate),
        })
    require(len(probabilities) == 128, "original_128_outcomes_retained")
    require(len(zero_indices) == 86, "86_zero_base_outcomes_retained")
    require(all(Ks[index] == O16 for index in zero_indices),
            "zero_base_probability_means_zero_Kraus_operator")
    require(sum(len(entries) for entries in groups.values()) == 128,
            "probability_groups_cover_all_outcomes")
    require(derivatives[0] == (
        s.Rational(42633, 5120000)
        - s.Rational(14157, 5120000) * s.sqrt(5)),
        "blank_pointer_source_matches_parent_certificate")

    # The original one-step binary port code has lengths 1 and 2.
    port1_source = s.simplify(sum(derivatives[1::2], s.Integer(0)))
    port1_probability = s.simplify(sum(probabilities[1::2], s.Integer(0)))
    require(s.simplify(sum(probabilities[::2], s.Integer(0))
                       + port1_probability - 1) == 0,
            "two_golden_ports_complete")
    require(s.simplify(
        port1_probability - s.trace(sum(
            (K.H * K for K in Ks[1::2]), O16.copy())) / 16) == 0,
        "port1_probability_is_original_complete_instrument_marginal")

    log_phi = s.log(1 / p)
    shannon_source = sum(
        (-dq * s.log(q) / log_phi for q, dq in positive_terms),
        s.Integer(0),
    )
    source_numeric = s.N(shannon_source, 70)
    port_cost_source = port1_source
    partial_code_minus_info = s.simplify(port_cost_source - shannon_source)
    sqrt5_scale = 10 ** 80
    sqrt5_floor = isqrt(5 * sqrt5_scale * sqrt5_scale)
    sqrt5_interval = (
        Fraction(sqrt5_floor, sqrt5_scale),
        Fraction(sqrt5_floor + 1, sqrt5_scale),
    )
    log_numerator_interval = (Fraction(0), Fraction(0))
    for q, dq in positive_terms:
        q_interval = _algebraic_interval(q, sqrt5_interval)
        dq_interval = _algebraic_interval(dq, sqrt5_interval)
        log_q_interval = _log_interval(q_interval)
        log_numerator_interval = _interval_add(
            log_numerator_interval,
            _interval_mul(dq_interval, log_q_interval),
        )
    phi_interval = (
        (Fraction(1) + sqrt5_interval[0]) / 2,
        (Fraction(1) + sqrt5_interval[1]) / 2,
    )
    log_phi_interval = _log_interval(phi_interval)
    shannon_source_interval = _interval_scale(
        _divide_by_positive_interval(log_numerator_interval, log_phi_interval),
        -1,
    )
    require(shannon_source_interval[1] < 0,
            "rational_interval_proves_full_pointer_shannon_source_negative")
    require(source_numeric != 0, "full_pointer_shannon_source_nonzero")
    require(s.simplify(port_cost_source - s.Rational(0)) != 0,
            "known_golden_port_code_has_nonzero_source")

    result = {
        "status": "PASS_SCOPED_COMPLETE_FULL128_SHANNON_FIRST_SOURCE",
        "checks": len(checks),
        "labels": checks,
        "input": {
            "grid": "L=4, h=1/4",
            "fourier_mode": [0, 0, 0, 1],
            "link_role": 2,
            "generator": "J23=[N2,Nbar3]",
            "state": "I16/16",
            "outcomes": 128,
            "strict_base_contraction_bound": "3/5 < 1",
        },
        "probability_law": {
            "positive_outcomes": 128 - len(zero_indices),
            "zero_outcomes": len(zero_indices),
            "groups": group_rows,
            "sum": "1",
            "first_source_sum": "0",
        },
        "complete_pointer_shannon": {
            "base": "-sum_j q_j log(q_j)/log(phi), all 128 outcomes retained",
            "first_source_exact": "-sum_{q_j>0} q'_j log(q_j)/log(phi); q'_j=0 at every zero base outcome",
            "first_source_numeric_70_digits": str(source_numeric),
            "first_source_rational_interval": {
                "lower": _decimal_bound(shannon_source_interval[0], 24, False),
                "upper": _decimal_bound(shannon_source_interval[1], 24, True),
                "method": "rational atanh-series log bounds with exact Q(sqrt(5)) interval arithmetic",
            },
        },
        "known_original_golden_port_code": {
            "lengths": [1, 2],
            "expected_cost": "1 + Pr(port1)",
            "first_source_exact": str(port_cost_source),
            "first_source_numeric": str(s.N(port_cost_source, 40)),
            "port_code_source_minus_full_pointer_shannon_source_numeric": str(
                s.N(partial_code_minus_info, 40)),
            "scope": "port-code contribution only; not the complete 128-label Book Cost-Info action",
        },
        "nonclaims": [
            "no complete event-label code-cost map for all 128 outputs",
            "no selected full native Cost-Info action",
            "no physical admission of the selected link variation",
            "no smooth second jet of the Shannon functional at zero-probability branches",
            "no physical GR source, refinement, or closure",
        ],
    }
    result["pins"] = {
        path: hashlib.sha256((repo / path).read_bytes()).hexdigest()
        for path in PINS
    }
    return result


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, sort_keys=True, indent=2))
