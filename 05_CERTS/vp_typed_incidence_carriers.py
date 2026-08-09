#!/usr/bin/env python3
"""Finite certificate for D0-TYPED-INCIDENCE-CARRIERS-001.

Build explicit typed carriers:

  Edge = (V9xV11) + (V9xV13) + (V11xV13)
  DirectedEdge = Edge x Bool
  Triangle = V9xV11xV13

and compare them bijectively with adjacency/triangle supports in the typed raw
scene. Then solve the reverse cardinality problem: an ordered positive triple
whose typed edge and triangle carriers have sizes 359 and 1287 must be
(9,11,13).

Honest scope: carrier support only. No gauge connection, holonomy selector,
physical edge dynamics, or empirical object is inferred from cardinality.
"""

from __future__ import annotations

from itertools import product
from math import isqrt


def require(condition: bool, token: str) -> None:
    if not condition:
        raise AssertionError(f"FAIL_{token}")


def expect_rejected(token: str, condition: bool) -> None:
    try:
        require(condition, token)
    except AssertionError as exc:
        print(f"PASS_NEGATIVE_CONTROL_{token}: {exc}")
    else:
        raise AssertionError(f"FAIL_NEGATIVE_CONTROL_DID_NOT_FIRE_{token}")


def edge_carrier(a: range, b: range, c: range):
    return (
        [("ab", x, y) for x, y in product(a, b)]
        + [("ac", x, z) for x, z in product(a, c)]
        + [("bc", y, z) for y, z in product(b, c)]
    )


def triangle_carrier(a: range, b: range, c: range):
    return list(product(a, b, c))


def solve_from_edge_triangle(edge_target: int, triangle_target: int):
    out = []
    for a in range(1, 100):
        for b in range(a, 100):
            numerator = edge_target - a * b
            denominator = a + b
            if numerator <= 0 or numerator % denominator:
                continue
            c = numerator // denominator
            if c < b:
                continue
            if a * b * c == triangle_target:
                out.append((a, b, c))
    return out


def solve_from_edge(edge_target: int):
    """All ordered positive triples with ab+ac+bc=edge_target."""
    out = []
    for a in range(1, isqrt(edge_target) + 1):
        for b in range(a, isqrt(edge_target) + 1):
            numerator = edge_target - a * b
            denominator = a + b
            if numerator <= 0 or numerator % denominator:
                continue
            c = numerator // denominator
            if c >= b:
                out.append((a, b, c))
    return out


def solve_from_triangle(triangle_target: int):
    """All ordered positive factor triples with abc=triangle_target."""
    out = []
    for a in range(1, isqrt(triangle_target) + 1):
        if triangle_target % a:
            continue
        remainder = triangle_target // a
        for b in range(a, isqrt(remainder) + 1):
            if remainder % b:
                continue
            c = remainder // b
            if c >= b:
                out.append((a, b, c))
    return out


def main() -> int:
    print(
        "STRUCTURE_FIXED_BEFORE_NUMBER: typed vertex zones construct edge, "
        "orientation, and triangle carriers before cardinalities are read."
    )

    a, b, c = range(9), range(11), range(13)
    edges = edge_carrier(a, b, c)
    directed = [(e, orient) for e in edges for orient in (False, True)]
    triangles = triangle_carrier(a, b, c)

    require(len(edges) == 359, f"EDGE_CARD_{len(edges)}")
    require(len(directed) == 718, f"DIRECTED_EDGE_CARD_{len(directed)}")
    require(len(triangles) == 1287, f"TRIANGLE_CARD_{len(triangles)}")
    print("PASS_TYPED_CARRIER_CARDINALITIES: Edge=359, DirectedEdge=718, Triangle=1287.")

    # Typed raw-scene support.
    vertices = (
        [("V9", x) for x in a]
        + [("V11", y) for y in b]
        + [("V13", z) for z in c]
    )
    zone = {"V9": 0, "V11": 1, "V13": 2}
    edge_support = [
        (u, v)
        for u, v in product(vertices, repeat=2)
        if zone[u[0]] < zone[v[0]]
    ]
    directed_support = [
        (u, v)
        for u, v in product(vertices, repeat=2)
        if zone[u[0]] != zone[v[0]]
    ]
    triangle_support = [
        (u, v, w)
        for u, v, w in product(vertices, repeat=3)
        if zone[u[0]] < zone[v[0]] < zone[w[0]]
    ]

    edge_map = {
        ("ab", x, y): (("V9", x), ("V11", y)) for x, y in product(a, b)
    }
    edge_map |= {
        ("ac", x, z): (("V9", x), ("V13", z)) for x, z in product(a, c)
    }
    edge_map |= {
        ("bc", y, z): (("V11", y), ("V13", z)) for y, z in product(b, c)
    }
    require(set(edge_map.values()) == set(edge_support), "EDGE_SUPPORT_BIJECTION")

    directed_map = {}
    for e, orient in directed:
        canonical = edge_map[e]
        directed_map[(e, orient)] = canonical if not orient else canonical[::-1]
    require(set(directed_map.values()) == set(directed_support), "DIRECTED_SUPPORT_BIJECTION")

    triangle_map = {
        (x, y, z): (("V9", x), ("V11", y), ("V13", z))
        for x, y, z in triangles
    }
    require(set(triangle_map.values()) == set(triangle_support), "TRIANGLE_SUPPORT_BIJECTION")
    print(
        "PASS_INCIDENCE_SUPPORT_BIJECTIONS: typed carriers equal ordered-edge, "
        "directed-adjacency, and increasing-zone triangle supports."
    )

    solutions = solve_from_edge_triangle(len(edges), len(triangles))
    require(solutions == [(9, 11, 13)], f"REVERSE_SOLUTIONS_{solutions}")
    print("PASS_TYPED_INCIDENCE_RECONSTRUCTION: (Edge,Triangle)=(359,1287) -> (9,11,13).")

    # One carrier alone is insufficient — full independent single-invariant
    # enumerations, not a second hand-picked invariant.
    edge_only = solve_from_edge(359)
    triangle_only = solve_from_triangle(1287)
    require((9, 11, 13) in edge_only, "EDGE_TARGET_MISSING")
    require((7, 10, 17) in edge_only, "EDGE_ONLY_SECOND_OBJECT")
    require((9, 11, 13) in triangle_only, "TRIANGLE_TARGET_MISSING")
    require((1, 3, 429) in triangle_only, "TRIANGLE_ONLY_SECOND_OBJECT")
    require(len(edge_only) > 1, "EDGE_ALONE_UNEXPECTEDLY_UNIQUE")
    require(len(triangle_only) > 1, "TRIANGLE_ALONE_UNEXPECTEDLY_UNIQUE")
    print(
        "PASS_SINGLE_CARRIER_INSUFFICIENT: "
        f"edge-size 359 has {len(edge_only)} ordered triples including (7,10,17); "
        f"triangle-size 1287 has {len(triangle_only)} including (1,3,429)."
    )

    # Reachable controls.
    expect_rejected(
        "DROP_ONE_EDGE_FAMILY_PRESERVES_359",
        len([e for e in edges if e[0] != "bc"]) == 359,
    )
    expect_rejected(
        "REMOVE_ORIENTATION_PRESERVES_718",
        len(edges) == 718,
    )
    expect_rejected(
        "TWO_ZONE_PRODUCT_PRESERVES_TRIANGLE_1287",
        len(list(product(a, b))) == 1287,
    )

    print(
        "PASS_TYPED_INCIDENCE_CARRIERS: scene counts are cardinalities of "
        "explicit finite incidence types and reconstruct their zone capacities."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
