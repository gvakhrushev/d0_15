#!/usr/bin/env python3
"""Finite certificate for D0-TYPED-SCENE-SELF-RECONSTRUCTION-001.

The certificate executes the complete loop:

  typed capacities -> tagged vertex graph -> incidence carriers
  -> cubic coefficients/discriminant -> reverse zone reconstruction.

It separately verifies representation invariance under within-zone renaming and
rejects one-face reconstruction, mutated incidence carriers, and a cross-zone
vertex move.

Honest scope: finite consistency/fixed-point theorem. The two directions are
not counted as independent evidence and no physical metric is inferred.
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


def solve_from_edge_triangle(edge_target: int, triangle_target: int):
    out = []
    for a in range(1, 100):
        for b in range(a, 100):
            numerator = edge_target - a * b
            denominator = a + b
            if numerator <= 0 or numerator % denominator:
                continue
            c = numerator // denominator
            if c >= b and a * b * c == triangle_target:
                out.append((a, b, c))
    return out


def solve_from_edge(edge_target: int):
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
        "STRUCTURE_FIXED_BEFORE_NUMBER: capacity types and tagged graph build "
        "incidence carriers before cubic coefficients or reverse reconstruction."
    )

    sizes = {"V9": 9, "V11": 11, "V13": 13}
    vertices = [
        (tag, i)
        for tag in ("V9", "V11", "V13")
        for i in range(sizes[tag])
    ]
    zone = {"V9": 0, "V11": 1, "V13": 2}
    labels = [zone[tag] for tag, _ in vertices]
    adjacency = [
        [0 if labels[i] == labels[j] else 1 for j in range(33)]
        for i in range(33)
    ]
    require(sum(map(len, [range(sizes[t]) for t in sizes])) == 33, "VERTEX_CAPACITY")

    edges = [
        (u, v)
        for u, v in product(vertices, repeat=2)
        if zone[u[0]] < zone[v[0]]
    ]
    directed_edges = [
        (u, v)
        for u, v in product(vertices, repeat=2)
        if zone[u[0]] != zone[v[0]]
    ]
    triangles = [
        (u, v, w)
        for u, v, w in product(vertices, repeat=3)
        if zone[u[0]] < zone[v[0]] < zone[w[0]]
    ]

    edge_count = len(edges)
    directed_count = len(directed_edges)
    triangle_count = len(triangles)
    require((edge_count, directed_count, triangle_count) == (359, 718, 1287),
            "INCIDENCE_CARDINALITIES")
    print("PASS_FORWARD_TYPED_INCIDENCE: V/E/dE/T = 33/359/718/1287.")

    linear_coeff = -edge_count
    constant_coeff = -2 * triangle_count
    discriminant = -4 * linear_coeff**3 - 27 * constant_coeff**2
    require((linear_coeff, constant_coeff) == (-359, -2574), "CUBIC_COEFFICIENTS")
    require(discriminant == 6_185_264 and discriminant > 0, "CUBIC_DISCRIMINANT")
    print(
        "PASS_TYPED_CUBIC: lambda^3-359lambda-2574, "
        "Delta=6185264>0 generated from carrier cardinalities."
    )

    recovered = solve_from_edge_triangle(edge_count, triangle_count)
    require(recovered == [(9, 11, 13)], f"REVERSE_RECONSTRUCTION_{recovered}")
    require(tuple(sizes.values()) == recovered[0], "REVERSE_NOT_SOURCE")
    print("PASS_REVERSE_RETURNS_SOURCE: (E,T) carrier sizes recover (V9,V11,V13).")

    # The upstream capacity-defect route returns the same center/spread.
    capacity_solutions = [
        (center, spread)
        for center in range(1, 100)
        for spread in range(0, center + 1)
        if spread**2 == 4 and center * spread**2 == 44
    ]
    require(capacity_solutions == [(11, 2)], f"CAPACITY_ROUTE_{capacity_solutions}")
    require(
        (capacity_solutions[0][0] - capacity_solutions[0][1],
         capacity_solutions[0][0],
         capacity_solutions[0][0] + capacity_solutions[0][1])
        == recovered[0],
        "CAPACITY_AND_INCIDENCE_ROUTES_DISAGREE",
    )
    print("PASS_CAPACITY_AND_INCIDENCE_ROUTES_AGREE: both return (9,11,13).")

    # Representation gauge: reverse local names inside each typed zone.
    renamed = [
        (tag, sizes[tag] - 1 - i)
        for tag, i in vertices
    ]
    renamed_labels = [zone[tag] for tag, _ in renamed]
    renamed_adj = [
        [0 if renamed_labels[i] == renamed_labels[j] else 1 for j in range(33)]
        for i in range(33)
    ]
    require(renamed_adj == adjacency, "WITHIN_ZONE_GAUGE_CHANGED_GRAPH")
    print("PASS_REPRESENTATION_GAUGE: arbitrary local reversal preserves the graph.")

    # Negative controls.
    edge_only = solve_from_edge(edge_count)
    triangle_only = solve_from_triangle(triangle_count)
    require((7, 10, 17) in edge_only, "EDGE_ONLY_SECOND_OBJECT")
    require((1, 3, 429) in triangle_only, "TRIANGLE_ONLY_SECOND_OBJECT")
    expect_rejected(
        "EDGE_FACE_ALONE_RECONSTRUCTS_SOURCE",
        edge_only == [(9, 11, 13)],
    )
    expect_rejected(
        "TRIANGLE_FACE_ALONE_RECONSTRUCTS_SOURCE",
        triangle_only == [(9, 11, 13)],
    )
    expect_rejected(
        "DELETE_EDGE_FAMILY_PRESERVES_CUBIC",
        (9 * 11 + 9 * 13, triangle_count) == (edge_count, triangle_count),
    )
    moved_labels = labels.copy()
    moved_labels[0] = 1
    moved_adj = [
        [0 if moved_labels[i] == moved_labels[j] else 1 for j in range(33)]
        for i in range(33)
    ]
    expect_rejected(
        "CROSS_ZONE_MOVE_IS_REPRESENTATION_GAUGE",
        moved_adj == adjacency,
    )
    expect_rejected(
        "MUTATED_TRIANGLE_COUNT_PRESERVES_RECONSTRUCTION",
        solve_from_edge_triangle(edge_count, triangle_count + 1) == [(9, 11, 13)],
    )

    print(
        "PASS_TYPED_SCENE_SELF_RECONSTRUCTION: capacity types -> typed graph "
        "-> incidence carriers -> cubic -> same zone capacities."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
