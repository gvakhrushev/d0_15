"""Exact checks for full eight-class return, readiness, and a retained abort."""

from hashlib import sha256
from itertools import product
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[6]
RESEARCH = ROOT / "02_REGISTRY/research"
SOURCES = (
    "01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md",
    "02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/"
    "open/round148/RESULT.json",
    "02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/"
    "direct/round75/history/ORDERED_PRICE_RU.md",
    "02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/"
    "book_source/GOLDEN_EXACT_DETECTOR.md",
)
ELEMENTS = (1, 2, 3, 4, -1, -2, -3, -4)
INDEX = {value: i for i, value in enumerate(ELEMENTS)}
BASE_TABLE = (
    (1, 2, 3, 4),
    (2, -1, 4, -3),
    (3, -4, -1, 2),
    (4, 3, -2, -1),
)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def multiply(left, right):
    sign = 1 if left * right > 0 else -1
    return sign * BASE_TABLE[abs(left)-1][abs(right)-1]


def right_translations():
    matrices = {}
    for label in ELEMENTS:
        matrix = sp.zeros(8)
        for before in ELEMENTS:
            matrix[INDEX[multiply(before, label)], INDEX[before]] = 1
        matrices[label] = matrix
    return matrices


def check_split(matrices):
    q, x = sp.symbols("q x")
    even_split = (1-2*q)**2
    odd_split = (1-q)**2 + q**2
    ranks = {}
    for label in ELEMENTS:
        if label == 1:
            continue
        operator = (1-q)*matrices[1] + q*matrices[label]
        expected = ((x-1)**4*(x-even_split)**4 if label == -1
                    else (x-1)**2*(x-even_split)**2*(x-odd_split)**4)
        determinant = (operator.T*operator).charpoly(x).as_expr()
        require(sp.expand(determinant-expected) == 0, "All eight squared singular values")
        ranks[label] = operator.subs(q, sp.Rational(1, 2)).rank()
    require(ranks[-1] == 4 and all(ranks[i] == 6 for i in ranks if i != -1),
            "Visible central and noncentral centered ranks")
    return ranks


def check_readiness(matrices):
    gamma, q = sp.Rational(2, 7), sp.Rational(3, 7)
    bound = 1 - 2*gamma*q
    for g, h in product(ELEMENTS, repeat=2):
        if g == h:
            continue
        ready = gamma*((1-q)*matrices[g]+q*matrices[h])
        optimal = ready + (1-gamma)*matrices[g]
        require(min((optimal.T*optimal).eigenvals()) == bound**2,
                "The dominant ready class attains the minimum singular bound")
        other_failed_law = (matrices[1] + 2*matrices[-2])/3
        test = ready + (1-gamma)*other_failed_law
        # Characters or the odd paired coefficients determine exact singular values.
        weights = test[:, INDEX[1]]
        candidates = []
        for i_sign, j_sign in product((1, -1), repeat=2):
            character = (1, i_sign, j_sign, i_sign*j_sign)
            candidates.append(sum(weights[k]*character[k % 4] for k in range(8))**2)
        candidates.append(sum((weights[k]-weights[4+k])**2 for k in range(4)))
        require(min(candidates) <= bound**2, "The mixed failures cannot improve the bound")
    return str(bound)


def check_literal_failure(matrices, p):
    identity = matrices[1]
    central = matrices[-1]
    swap = sp.Matrix([[0, 1], [1, 0]])
    lifted_split = sp.BlockMatrix([
        [sp.sqrt(p)*identity, p*central],
        [p*identity, sp.sqrt(p)*identity],
    ]).as_explicit()
    echo = sp.eye(16) + p*sp.sqrt(p)*sp.kronecker_product(swap, identity+central)
    require((lifted_split.T*lifted_split-echo).applyfunc(sp.simplify) == sp.zeros(16),
            "Golden return retains both positive memory classes")
    a0 = p*sp.eye(16) + p**2*sp.kronecker_product(swap, central)
    b0 = p*sp.eye(16) + p**2*sp.kronecker_product(swap, identity)
    failure = b0*a0
    hidden = sp.kronecker_product(p**4*sp.eye(2)+p**3*swap, identity+central)
    require((failure-p**3*sp.eye(16)-hidden).applyfunc(sp.simplify) == sp.zeros(16),
            "Existing recorded failure contains a hidden opposite class pair")
    odd = (identity-central)/2
    require(hidden*sp.kronecker_product(sp.eye(2), odd) == sp.zeros(16),
            "Failure pair is invisible in the existing odd carrier")
    for label in ELEMENTS:
        corrected = failure*sp.kronecker_product(sp.eye(2), matrices[label])
        support = sum(v != 0 for v in corrected[:8, INDEX[1]])
        require(support == 2, "No fixed endpoint label corrects the two failure routes")


def check_classwise_example(p):
    raw = sp.Matrix([sp.Rational(1, 2), sp.Rational(1, 2)])
    factors = sp.Matrix([sp.sqrt(sp.Rational(3, 2)), sp.sqrt(sp.Rational(2, 3))])
    require(sp.prod(factors) == 1, "Centered classwise factors")
    adjusted = raw.multiply_elementwise(factors)
    total = sp.simplify(sum(adjusted))
    require(total == 5/(2*sp.sqrt(6)), "Absolute classwise normalizer")
    require((adjusted/total).applyfunc(sp.simplify) == sp.Matrix([sp.Rational(3, 5),
                                                               sp.Rational(2, 5)]),
            "Old aggregate class measure after reweighting")
    require(sp.Rational(3, 2) < 1/p < 2, "Strict margin for the fair edge")


def main():
    matrices = right_translations()
    p = (sp.sqrt(5)-1)/2
    ranks = check_split(matrices)
    readiness = check_readiness(matrices)
    check_literal_failure(matrices, p)
    check_classwise_example(p)
    require(RESEARCH.is_dir(), "Repository paths")
    print(json.dumps({
        "GR_closed": False,
        "actual_B148_path_to_class_map_proved": False,
        "centered_rank_with_opposite_signs": ranks[-1],
        "centered_rank_with_order_four_shift": ranks[2],
        "best_single_step_singular_value_at_gamma_2_7_q_3_7": readiness,
        "formal_signed_G_factory_failure_same_return_classes": ["1", "-1"],
        "retained_factory_failure_pair_visible_in_odd_Spin": False,
        "classwise_constant_factor_in_3_to_2_example": "5/(2*sqrt(6))",
        "source_sha256": {path: sha256((ROOT / path).read_bytes()).hexdigest()
                          for path in SOURCES},
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
