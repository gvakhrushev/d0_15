"""Exact local/global normalization checks for a stopped Golden ladder."""
from fractions import Fraction
from functools import reduce
import json


ZERO = (0, 0)
ONE = (1, 0)
P = (0, 1)


def require(condition, label):
    if not condition:
        raise ArithmeticError(label)


def add(left, right):
    return left[0] + right[0], left[1] + right[1]


def multiply(left, right):
    a, b = left
    c, d = right
    return a * c + b * d, a * d + b * c - b * d


def product(values):
    return reduce(multiply, values, ONE)


def total(values):
    return reduce(add, values, ZERO)


def inverse(value):
    a, b = value
    norm = a * a - a * b - b * b
    return Fraction(a - b, norm), Fraction(-b, norm)


BORN = (P, multiply(P, P))


def tree(visits, powers):
    """Return positive leaf masses using local outgoing powers w**nu."""
    leaves = [(1,) * depth + (0,) for depth in range(visits)] + [(1,) * visits]
    return {leaf: product(powers[depth][bit] for depth, bit in enumerate(leaf))
            for leaf in leaves}


def scaled_local_powers(normalizers):
    return [tuple(multiply(normalizer, value) for value in BORN) for normalizer in normalizers]


def globally_agrees(physical, raw):
    normalization = total(raw.values())
    return all(raw[leaf] == multiply(normalization, probability)
               for leaf, probability in physical.items())


def odds_cross(left, right, early):
    left_late = total(weight for leaf, weight in left.items() if leaf != early)
    right_late = total(weight for leaf, weight in right.items() if leaf != early)
    return multiply(left_late, right[early]), multiply(right_late, left[early])


def run():
    physical = tree(2, [BORN] * 2)
    require(physical == {(0,): P, (1, 0): product([P] * 3), (1, 1): product([P] * 4)},
            "actual two-visit Golden head law")
    require(total(physical.values()) == ONE, "all three recorded leaves retained")

    # Primitive p,p^2 as nu=1 weights, and the same numbers squared as nu=2 weights.
    squared_primitive = tuple(multiply(value, value) for value in BORN)
    require(multiply(squared_primitive[1], BORN[0]) != multiply(BORN[1], squared_primitive[0]),
            "using p,p^2 as amplitudes changes even the local odds")
    require(globally_agrees(physical, tree(2, [BORN] * 2)),
            "p,p^2 are consistent positive weights at nu=1")
    require(not globally_agrees(physical, tree(2, [squared_primitive] * 2)),
            "p,p^2 are not primitive amplitudes")

    # h^2=p, with both local squared weights still proportional to the native law.
    scaled = tree(2, scaled_local_powers([P, P]))
    left, right = odds_cross(scaled, physical, (0,))
    require(left == multiply(P, right), "depth odds differ by the surviving local normalizer")
    require(not globally_agrees(physical, scaled), "same local Born does not imply global Born")
    require(globally_agrees(physical, tree(2, scaled_local_powers([P, ONE]))),
            "a common root multiplier is invisible in normalized records")

    # Distinct absolute local factors and arbitrarily many reachable early STOPs.
    normalizers = [P, BORN[1], ONE, P, BORN[1]]
    ladder = tree(5, [BORN] * 5)
    raw = tree(5, scaled_local_powers(normalizers))
    require(total(ladder.values()) == ONE, "all five stop depths and cap endpoint")
    for depth in range(1, len(normalizers)):
        parent_stop, child_stop = (1,) * (depth - 1) + (0,), (1,) * depth + (0,)
        left = multiply(raw[child_stop], ladder[parent_stop])
        right = multiply(raw[parent_stop], ladder[child_stop])
        require(left == multiply(normalizers[depth], right), "adjacent stops isolate one factor")

    # All terminal factors are kept. This algebraic compensation is not a tariff assignment.
    compensated = {
        leaf: multiply(weight, inverse(product(normalizers[1:len(leaf)])))
        for leaf, weight in raw.items()
    }
    require(globally_agrees(ladder, compensated), "terminal weights can compensate local factors")
    require(total(compensated.values()) == P, "the countermodel leaves the common root factor")

    print(json.dumps({
        "exact_ring": "Q(p), p^2+p=1",
        "true_two_visit_law": ["p", "p^3", "p^4"],
        "primitive_p_p2_works_as_positive_weights": True,
        "primitive_p_p2_works_as_amplitudes": False,
        "scaled_local_Born_global_odds_factor": "p",
        "adjacent_stop_isolates_actual_nonroot_normalizer": True,
        "terminal_weight_can_cancel_normalizer": True,
        "common_root_remains_unidentified": True,
        "absolute_Book03_link_proved": False,
        "GR_closed": False,
    }, indent=2))


if __name__ == "__main__":
    run()
