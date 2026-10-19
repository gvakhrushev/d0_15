#!/usr/bin/env python3
"""Pull the original one-round full128 pointer back through the regular 12-gate atlas.

This is an endpoint-link calculation, not a simulation of twelve admitted D0
memory operations or their complete Book Cost-Info price.
"""
from fractions import Fraction
from functools import lru_cache
from math import isqrt
from pathlib import Path
import ast
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "02_REGISTRY/research/sources/d0_native_full128_order_readout_2026-10-19"))

import sympy as s
from sympy.polys.domains import QQ
from sympy.polys.matrices import DomainMatrix

from check_complete_shannon_order_source import (
    _algebraic_interval,
    _decimal_bound,
    _divide_by_positive_interval,
    _interval_add,
    _interval_mul,
    _interval_scale,
    _log_rational_interval,
)
from check_two_round_complete_shannon_order_source import _build_full128_pair

CREATORS = "02_REGISTRY/research/certificates/a4d_native_curved_soldered_heat.py"
PINS = {
    "02_REGISTRY/research/sources/d0_two_null_regular_atlas_2026-10-19/check_regular_two_null_atlas.py":
        "520f3ca1fb6e4653d82d51b61c2b647677d228c9bcfe444d25d239f7adcf55b1",
    "02_REGISTRY/research/sources/d0_native_full128_order_readout_2026-10-19/check_two_round_complete_shannon_order_source.py":
        "3759eb9a7826efdb167c73d2185acc5c8c82d271b5dde1b208d4e74db85f18ae",
    "02_REGISTRY/research/sources/d0_native_full128_order_readout_2026-10-19/check_complete_shannon_order_source.py":
        "26424be5c2278828af81d331b8edc110dd8c4eefad4fc97e2c2e5fa813de178a",
    CREATORS: "bf13f57c902da0005634ae6834c0b4e3ffd2df1aa196a61ebc0ff3dc0351c7da",
}


def run(repo=None):
    repo = ROOT if repo is None else Path(repo).resolve()
    checks = []

    def require(condition, name):
        if not bool(condition):
            raise ArithmeticError("regular_atlas_full128:" + name)
        checks.append(name)

    def matrix_equal(left, right):
        return all(s.simplify(value) == 0 for value in left - right)

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
    require(len(nodes) == 2, "load_only_owned_full16_creator_and_order")
    scope = {"s": s, "lru_cache": lru_cache}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), CREATORS, "exec"), scope)
    C16 = [scope["creator"](role) for role in range(4)]

    def unit(i, j):
        matrix = s.zeros(4)
        matrix[i, j] = 1
        return matrix

    I4 = s.eye(4)
    eta = s.Matrix([[0, 1, 0, 0], [1, 0, 0, 0],
                    [0, 0, -1, 0], [0, 0, 0, -1]])
    N2 = unit(1, 2) + unit(2, 0)
    Nbar3 = unit(0, 3) + unit(3, 1)
    primitive = (N2, Nbar3, N2, Nbar3, N2, Nbar3)
    baseline = [s.Rational(value, 40) for value in (1, 1, 1, 1, 2, 1)]

    def expnull(generator, value):
        return I4 + value * generator + value**2 * generator**2 / 2

    forwards = [expnull(X, t) for X, t in zip(primitive, baseline)]
    base_word = I4
    for factor in forwards:
        base_word *= factor
    reverse_inverse = [expnull(X, -t)
                       for X, t in zip(primitive[::-1], baseline[::-1])]
    closed_word = base_word
    for factor in reverse_inverse:
        closed_word *= factor
    require(closed_word == I4, "twelve_gate_baseline_is_exact_identity")
    require(all(X.T * eta * X == eta
                for X in forwards + reverse_inverse),
            "all_twelve_primitives_are_original_proper_lorentz")
    require(max(baseline) == s.Rational(1, 20)
            and max(baseline) < s.Rational(1, 10),
            "regular_word_controls_stay_inside_existing_small_chart")

    # The endpoint derivative of G(t)G(t0)^-1 is Ad(prefix_j)X_j.
    prefix = I4
    control_tangents = []
    for X, factor in zip(primitive, forwards):
        control_tangents.append(prefix * X * prefix.inv())
        prefix *= factor
    require(all(V.T * eta + eta * V == s.zeros(4)
                for V in control_tangents),
            "six_endpoint_controls_are_proper_lorentz_tangents")
    require(s.Matrix.hstack(*(V.reshape(16, 1)
                              for V in control_tangents)).rank() == 6,
            "regular_atlas_endpoint_jacobian_rank_six")

    # Keep the Lie-coordinate coefficients as a replayable cross-check that
    # the exact same six-dimensional tangent is passed to the original channel.
    J23 = unit(2, 3) - unit(3, 2)
    N3 = unit(1, 3) + unit(3, 0)
    Nbar2 = unit(0, 2) + unit(2, 1)
    B = unit(1, 1) - unit(0, 0)
    lie_basis = (N2, N3, Nbar2, Nbar3, J23, B)
    lie_matrix = s.Matrix.hstack(*(G.reshape(16, 1) for G in lie_basis))
    lie_coordinates = []
    for index, V in enumerate(control_tangents):
        solution = s.linsolve((lie_matrix, V.reshape(16, 1)))
        require(len(solution) == 1, f"unique_lorentz_coordinates_{index}")
        coefficients = s.Matrix(next(iter(solution)))
        require(lie_matrix * coefficients == V.reshape(16, 1),
                f"lorentz_coordinate_reconstruction_{index}")
        lie_coordinates.append(coefficients)

    base_probabilities = None
    probability_columns = []
    entropy_rows = []
    for control_index, tangent in enumerate(control_tangents):
        kraus, d_kraus, _ = _build_full128_pair(
            tangent, tangent, C16, require
        )
        require(len(kraus) == 128 and len(d_kraus) == 128,
                f"complete_original_128_outputs_{control_index}")
        completeness = sum((K.H * K for K in kraus), s.zeros(16))
        tangent_completeness = sum(
            (K.H * dK + dK.H * K for K, dK in zip(kraus, d_kraus)),
            s.zeros(16),
        )
        require(matrix_equal(completeness, s.eye(16)),
                f"full128_completeness_{control_index}")
        require(matrix_equal(tangent_completeness, s.zeros(16)),
                f"full128_derivative_normalization_{control_index}")

        probabilities = [s.simplify(s.trace(K.H * K) / 16) for K in kraus]
        derivatives = [s.simplify(
            (s.trace(dK.H * K) + s.trace(K.H * dK)) / 16
        ) for K, dK in zip(kraus, d_kraus)]
        require(s.simplify(sum(probabilities) - 1) == 0,
                f"probabilities_sum_to_one_{control_index}")
        require(s.simplify(sum(derivatives)) == 0,
                f"probability_tangent_sums_to_zero_{control_index}")
        if base_probabilities is None:
            base_probabilities = probabilities
        else:
            require(probabilities == base_probabilities,
                    f"same_closed_baseline_probabilities_{control_index}")

        zero = [i for i, q in enumerate(probabilities) if q == 0]
        positive = [i for i, q in enumerate(probabilities) if q > 0]
        require(len(zero) == 86 and len(positive) == 42,
                f"original_42_positive_86_dark_support_{control_index}")
        require(all(derivatives[i] == 0 for i in zero),
                f"dark_outcomes_have_zero_first_jet_{control_index}")
        probability_columns.append(derivatives)

        grouped = {}
        for q, dq in zip(probabilities, derivatives):
            if q > 0:
                grouped[q] = grouped.get(q, s.Integer(0)) + dq
        grouped = {q: s.simplify(dq) for q, dq in grouped.items() if dq != 0}
        source = -sum((dq * s.log(q) for q, dq in grouped.items()),
                      s.Integer(0)) / s.log((1 + s.sqrt(5)) / 2)
        grouped_text = "\n".join(
            f"{q}: {grouped[q]}" for q in sorted(grouped, key=str)
        )

        scale = 10**80
        root5_floor = isqrt(5 * scale * scale)
        root5 = (Fraction(root5_floor, scale),
                 Fraction(root5_floor + 1, scale))
        numerator = (Fraction(0), Fraction(0))
        for q, dq in grouped.items():
            q_interval = _algebraic_interval(q, root5)
            dq_interval = _algebraic_interval(dq, root5)
            log_q = (_log_rational_interval(q_interval[0], terms=32)[0],
                     _log_rational_interval(q_interval[1], terms=32)[1])
            numerator = _interval_add(
                numerator, _interval_mul(dq_interval, log_q)
            )
        phi_interval = ((Fraction(1) + root5[0]) / 2,
                        (Fraction(1) + root5[1]) / 2)
        log_phi = (_log_rational_interval(phi_interval[0], terms=32)[0],
                   _log_rational_interval(phi_interval[1], terms=32)[1])
        source_interval = _interval_scale(
            _divide_by_positive_interval(numerator, log_phi), -1
        )
        if grouped:
            require(source_interval[0] > 0 or source_interval[1] < 0,
                    f"Shannon_source_sign_interval_{control_index}")
        entropy_rows.append({
            "control": control_index,
            "exact_expression": str(source),
            "numeric_35_digits": str(s.N(source, 35)),
            "interval_24_digits": [
                _decimal_bound(source_interval[0], 24, False),
                _decimal_bound(source_interval[1], 24, True),
            ],
            "positive_probability_groups": len(grouped),
            "grouped_coefficients_sha256": hashlib.sha256(
                grouped_text.encode("utf-8")
            ).hexdigest(),
        })

    probability_jacobian = s.Matrix(
        128, 6,
        lambda row, column: probability_columns[column][row],
    )
    probability_rank = DomainMatrix.from_Matrix(
        probability_jacobian
    ).convert_to(QQ.algebraic_field(s.sqrt(5))).rank()
    require(probability_rank == 3,
            "standard_full128_probability_response_has_exact_rank_three")

    return {
        "status": "PASS_SCOPED_FULL128_ATLAS_ENDPOINT_RESPONSE",
        "checks": len(checks),
        "geometry": {
            "word": "G(t)G(t0)^-1; six forward and six fixed reverse original null exponentials",
            "baseline": [str(x) for x in baseline],
            "endpoint": "I4",
            "endpoint_jacobian_rank": 6,
            "lie_basis_order": ["N2", "N3", "Nbar2", "Nbar3", "J23", "B"],
            "control_tangent_coordinates": [
                [str(x) for x in vector] for vector in lie_coordinates
            ],
        },
        "instrument": {
            "carrier": "original full16 CAR, complete 128-outcome one-round instrument",
            "reference": "fixed reference128 spectator",
            "preparation": "I16/16",
            "link": "role 2; endpoint link M2=W(t); other links identity",
            "background": "L=4, h=1/4, Fourier phases (1,1,1,i), nu=3/5",
            "probability_jacobian_rank_over_Q_sqrt5": probability_rank,
            "outcomes": 128,
            "base_support": {"positive": 42, "zero": 86},
        },
        "complete_pointer_shannon_first_sources": entropy_rows,
        "nonclaims": [
            "the calculation measures the endpoint link and is not twelve sequential fresh-register executions",
            "the complete compulsory Book Cost-Info action, controller, work, preparation and clock terms are not included",
            "the twelve controls are not thereby physically admitted or priced by foundational D0",
            "no same-history source pullback, joint physical root, refinement or positive GR closure is established",
        ],
        "pins": {
            path: hashlib.sha256((repo / path).read_bytes()).hexdigest()
            for path in PINS
        },
    }


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, sort_keys=True, indent=2))
