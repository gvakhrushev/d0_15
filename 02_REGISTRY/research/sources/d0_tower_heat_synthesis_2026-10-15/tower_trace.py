"""Exact finite Fibonacci-trace ambiguity and its conditional source consumer.

The supplied AF tower is M_{F(n+2)} (+) M_{F(n+1)}, with inclusion
(A,B) -> (diag(A,B),A). Coefficients multiply UNNORMALIZED matrix traces.
Positivity and normalization are imposed at every level 0,...,depth.
This module does not derive that tower or its physical D0 admission.

An affine source bound concerns an already identified source observable.
Convergence of state values alone does not control a field derivative.
"""
from __future__ import annotations

from fractions import Fraction


def _index(value: int, name: str) -> int:
    if type(value) is not int or value < 0:
        raise ValueError(f"{name} must be a nonnegative integer")
    return value


def _rational(value) -> Fraction:
    if type(value) not in (int, Fraction):
        raise TypeError("exact inputs must be integers or Fractions")
    return Fraction(value)


def fibonacci(index: int) -> int:
    """F_0=0, F_1=1."""
    _index(index, "index")
    a, b = 0, 1
    for _ in range(index):
        a, b = b, a + b
    return a


def base_weight_interval(depth: int) -> tuple[Fraction, Fraction]:
    """Exact CLOSED interval of x_0; faithful traces use its open interior."""
    _index(depth, "depth")
    ends = (Fraction(fibonacci(depth), fibonacci(depth + 1)),
            Fraction(fibonacci(depth + 1), fibonacci(depth + 2)))
    return min(ends), max(ends)


def base_weight_width(depth: int) -> Fraction:
    """Cassini width, not the surrogate phi**(-2*depth)."""
    _index(depth, "depth")
    return Fraction(1, fibonacci(depth + 1) * fibonacci(depth + 2))


def level_trace_coefficients(base_weight, level: int) -> tuple[Fraction, Fraction]:
    """Apply D^{-level} to (x_0,1-x_0); positivity is a separate condition.

    delta(x_k,y_k)=(-1)^k(F_{k+1},-F_{k+2}) delta x_0.
    """
    _index(level, "level")
    u = _rational(base_weight)
    sign = (-1) ** level
    return (sign * (fibonacci(level + 1) * u - fibonacci(level)),
            -sign * (fibonacci(level + 2) * u - fibonacci(level + 1)))


def level_trace_segment(depth: int, level: int = 0):
    """The two endpoint coefficient PAIRS, not an independent rectangle."""
    _index(level, "level")
    if level > depth:
        raise ValueError("level must not exceed depth")
    return tuple(level_trace_coefficients(u, level) for u in base_weight_interval(depth))


def affine_response_bound(depth: int, left_trace, right_trace,
                          level: int = 0) -> Fraction:
    """Sharp diameter of x_k*left_trace+y_k*right_trace over the trace segment.

    For a field source the inputs must be the actual block traces of its
    source observable on the same admitted preparation and direction. No
    field derivative of a freely moving trace parameter is omitted by fiat.
    """
    level_trace_segment(depth, level)  # validate the stated finite tower
    left, right = _rational(left_trace), _rational(right_trace)
    slope = fibonacci(level + 1) * left - fibonacci(level + 2) * right
    return abs(slope) * base_weight_width(depth)


def conditional_raw_gap_bound(depth: int, mesh, source_l1_slope_bound,
                               node_volume=1, *, error_at: str) -> Fraction:
    """Conditional ORIGINAL raw-l1 gap, with its source coordinate explicit.

    ASSUME node_count <= node_volume*h^-4, and each node's actual source
    covector difference has l1 bound C_h/(F_{N+1}F_{N+2}). Here C_h is
    source_l1_slope_bound and INCLUDES all ten packed metric slots. If C_h
    instead bounds each scalar slot, pass 10*C_h, not C_h.

    error_at='Xi': the bound concerns original unnormalized Xi, so return
      node_volume*h^-6*C_h/(F_{N+1}F_{N+2}).
    error_at='normalized_tau': it concerns tau=h^-2*Xi already, so the SAME
      original task norm is its raw sum, with factor h^-4 instead of h^-6.

    With C_h <= C*h^-s the respective sufficient depth budgets are
    2*N(h)*log(phi)-(6+s)*log(1/h) -> +infinity, or (4+s) in the tau case.
    Both require actual source-coordinate binding and uniform source/first-
    jet control. A small state-trace interval alone establishes neither.
    No refinement map, physical solution or original #310 terminal is proved.
    """
    if error_at not in ("Xi", "normalized_tau"):
        raise ValueError("error_at must explicitly be 'Xi' or 'normalized_tau'")
    h, bound, volume = map(_rational, (mesh, source_l1_slope_bound, node_volume))
    if h <= 0 or bound < 0 or volume < 0:
        raise ValueError("mesh must be positive; source and volume bounds nonnegative")
    power = 6 if error_at == "Xi" else 4
    return volume * bound * base_weight_width(depth) / h ** power


def run_checks() -> dict:
    """Small exact checks using an independent finite positivity polytope."""
    count = 0

    def require(condition, message):
        nonlocal count
        count += 1
        if not condition:
            raise AssertionError(message)

    # Independently invert D one level at a time. Each coordinate is a*u+b;
    # intersect EVERY positivity half-line and verify dimension normalization.
    for depth in range(13):
        lower, upper = None, None
        x, y = (1, 0), (-1, 1)
        for level in range(depth + 1):
            a, b = fibonacci(level + 2), fibonacci(level + 1)
            require(a*x[0] + b*y[0] == 0 and a*x[1] + b*y[1] == 1,
                    "inverse-D trace normalization")
            for slope, constant in (x, y):
                if slope > 0:
                    edge = Fraction(-constant, slope)
                    lower = edge if lower is None else max(lower, edge)
                elif slope < 0:
                    edge = Fraction(-constant, slope)
                    upper = edge if upper is None else min(upper, edge)
                else:
                    require(constant >= 0, "constant positivity constraint")
            x, y = y, (x[0]-y[0], x[1]-y[1])
        ends = base_weight_interval(depth)
        require((lower, upper) == ends, "full positivity polytope endpoints")
        require(upper-lower == base_weight_width(depth), "Cassini exact width")
        for level in range(depth + 1):
            segment = level_trace_segment(depth, level)
            require(all(x >= 0 and y >= 0 for x, y in segment),
                    "every retained coefficient is nonnegative")
            left, right = Fraction(7, 3), Fraction(-5, 2)
            values = [x*left + y*right for x, y in segment]
            require(abs(values[1]-values[0]) == affine_response_bound(depth, left, right, level),
                    "higher-level affine response diameter is attained")

    # Exact Q(p) arithmetic, p^2=1-p, without floating point or sympy.
    def mul(z, w):
        a, b = z
        c, d = w
        return a*c+b*d, a*d+b*c-b*d

    def power(exponent):
        value = (1, 0)
        for _ in range(exponent):
            value = mul(value, (0, 1))
        return value

    for exponent, roles in ((1, 1), (3, 4), (5, 11)):
        a, b = power(exponent)
        c, d = power(2*exponent)
        require((roles*a+c, roles*b+d) == (1, 0),
                "same tower admits role-like coefficients 1,4,11")
    p2, p4 = power(2), power(4)
    actual_t_width = tuple(a+b for a, b in zip(p2, p4))
    require(actual_t_width != p2 and actual_t_width != tuple(2*a for a in p2),
            "reject claimed exact or symmetric ambiguity width")
    # At depth one, t=B/A=-1/3 passes |t|<p^2 but gives
    # x_0=(2+8p)/19<1/2, so x_2=2*x_0-1<0. The exact bounds
    # 3/5<p<5/8 establish both inequalities without numerical root evaluation.
    require(Fraction(1, 3) < 1-Fraction(5, 8),
            "wrong symmetric criterion admits hostile ratio")
    require((2+8*Fraction(5, 8))/19 < Fraction(1, 2),
            "hostile ratio violates finite trace positivity")
    require(base_weight_width(1) == Fraction(1, 2) and p2[1] != 0,
            "base-coordinate width is not golden power")
    h, bound, volume = Fraction(1, 8), Fraction(3, 2), 2
    nodes = volume / h**4
    require(nodes.denominator == 1, "literal integer-node fixture")
    require(conditional_raw_gap_bound(9, h, bound, volume, error_at="Xi")
            == h**-2 * nodes * bound * base_weight_width(9),
            "original raw sum keeps h^-4 nodes and h^-2 scaling")
    require(conditional_raw_gap_bound(9, h, bound, volume, error_at="normalized_tau")
            == nodes * bound * base_weight_width(9),
            "already normalized tau does not acquire a second h^-2")
    return {"status": "PASS", "exact_checks": count, "finite_depths": "0..12",
            "arithmetic": "Fraction and exact Q(p) pairs",
            "scope": "supplied Fibonacci tower; actual source/first-jet binding and GR remain open"}
