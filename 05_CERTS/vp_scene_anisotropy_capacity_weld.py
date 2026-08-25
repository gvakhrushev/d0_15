#!/usr/bin/env python3
"""Finite certificate for D0-SCENE-ANISOTROPY-CAPACITY-WELD-001.

The certificate builds the D0 capacity values from their finite constructors:

    Dyad = 2
    ABCD = Dyad^2 = 4
    Omega8 = 2*ABCD = 8
    V9 = Omega8+1 = 9
    V11 = V9+Dyad = 11
    V13 = V9+ABCD = 13

It then compares the forced centered scene `(V11-Dyad,V11,V11+Dyad)` with the
equal-zone control `(V11,V11,V11)`.

Proved by exact integer arithmetic:

    squared zone deviation = Omega8
    equal-zone edge deficit = ABCD
    equal-zone triangle deficit = qT = lcm(ABCD,V11) = ABCD*V11

The same spread parameter gives the positive rank-3 cubic discriminant; spread
zero gives the isotropic discriminant-zero control.

Honest scope: exact finite combinatorics only. No observed spacetime anisotropy,
new coupling, or new empirical quantity is claimed.
"""

from __future__ import annotations

from math import gcd, lcm


def invariants(parts: tuple[int, int, int]) -> tuple[int, int, int]:
    a, b, c = parts
    return a + b + c, a * b + a * c + b * c, a * b * c


def squared_anisotropy(parts: tuple[int, int, int], center: int) -> int:
    return sum((n - center) ** 2 for n in parts)


def cubic_discriminant(edges: int, triangles: int) -> int:
    # charpoly = lambda^3 - E lambda - 2T
    return 4 * edges**3 - 108 * triangles**2


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


def main() -> int:
    print(
        "STRUCTURE_FIXED_BEFORE_NUMBER: Dyad/ABCD/Omega8/V9/V11/V13 are "
        "constructed first; anisotropy defects are computed afterwards."
    )

    dyad = 2
    abcd = dyad * dyad
    omega8 = 2 * abcd
    v9 = omega8 + 1
    v11 = v9 + dyad
    v13 = v9 + abcd

    scene = (v11 - dyad, v11, v11 + dyad)
    equal_zone = (v11, v11, v11)

    require(scene == (9, 11, 13), f"SCENE_LADDER_{scene}")
    require(v13 == scene[2], f"V13_MISMATCH_{v13}_{scene[2]}")
    print(f"PASS_CAPACITY_CENTERED_SCENE: {scene} from center V11={v11}, spread Dyad={dyad}.")

    _, edge_scene, triangle_scene = invariants(scene)
    _, edge_equal, triangle_equal = invariants(equal_zone)
    edge_defect = edge_equal - edge_scene
    triangle_defect = triangle_equal - triangle_scene
    anisotropy = squared_anisotropy(scene, v11)
    q_t = lcm(abcd, v11)

    require(anisotropy == omega8, f"SQUARED_ANISOTROPY_{anisotropy}_NE_OMEGA8_{omega8}")
    require(edge_defect == abcd, f"EDGE_DEFECT_{edge_defect}_NE_ABCD_{abcd}")
    require(triangle_defect == q_t, f"TRIANGLE_DEFECT_{triangle_defect}_NE_QT_{q_t}")
    require(gcd(abcd, v11) == 1, "ABCD_V11_NOT_COPRIME")
    require(q_t == abcd * v11 == 44, f"QT_PRODUCT_{q_t}")

    print(f"PASS_SQUARED_ANISOTROPY_IS_OMEGA8: {anisotropy} = {omega8}.")
    print(f"PASS_EDGE_DEFECT_IS_ABCD: {edge_equal}-{edge_scene} = {edge_defect} = {abcd}.")
    print(
        f"PASS_TRIANGLE_DEFECT_IS_TERMINAL_WINDOW: "
        f"{triangle_equal}-{triangle_scene} = {triangle_defect} = qT={q_t}."
    )

    # Generic centered identities, tested beyond the physical-positive range too:
    # signed centers and spreads larger than the center exercise the polynomial
    # theorem rather than only valid graph partitions.
    for center in range(-24, 25):
        for spread in range(0, 31):
            parts = (center - spread, center, center + spread)
            _, e_actual, t_actual = invariants(parts)
            _, e_equal, t_equal = invariants((center, center, center))
            require(
                squared_anisotropy(parts, center) == 2 * spread**2,
                f"GENERIC_VARIANCE_m{center}_d{spread}",
            )
            require(e_equal - e_actual == spread**2, f"GENERIC_EDGE_m{center}_d{spread}")
            require(
                t_equal - t_actual == center * spread**2,
                f"GENERIC_TRIANGLE_m{center}_d{spread}",
            )
    print("PASS_GENERIC_CENTERED_IDENTITIES: exact signed grid m=-24..24, d=0..30.")

    disc_scene = cubic_discriminant(edge_scene, triangle_scene)
    disc_equal = cubic_discriminant(edge_equal, triangle_equal)
    require(disc_scene == 6_185_264 and disc_scene > 0, f"SCENE_DISC_{disc_scene}")
    require(disc_equal == 0, f"EQUAL_ZONE_DISC_{disc_equal}")
    print(
        f"PASS_DISCRIMINANT_WELD: scene Delta={disc_scene}>0; "
        f"equal-zone control Delta={disc_equal}."
    )

    # Reverse reconstruction from the two capacity defects.
    reconstructions: set[tuple[int, int, tuple[int, int, int]]] = set()
    for center in range(1, 100):
        for spread in range(0, center + 1):
            parts = (center - spread, center, center + spread)
            _, e_actual, t_actual = invariants(parts)
            _, e_equal, t_equal = invariants((center, center, center))
            if e_equal - e_actual == abcd and t_equal - t_actual == q_t:
                reconstructions.add((center, spread, parts))
    require(
        reconstructions == {(11, 2, scene)},
        f"CAPACITY_RECONSTRUCTION_{sorted(reconstructions)}",
    )
    print(
        "PASS_CAPACITY_DEFECTS_RECONSTRUCT_SCENE: "
        "(edge defect, triangle defect)=(ABCD,qT) uniquely gives "
        "(center,spread)=(V11,Dyad)=(11,2)."
    )

    # Single-face minimality controls.
    edge_only = (10 - dyad, 10, 10 + dyad)
    triangle_only = (44 - 1, 44, 44 + 1)
    require(
        invariants((10, 10, 10))[1] - invariants(edge_only)[1] == abcd
        and edge_only != scene,
        "EDGE_FACE_SECOND_OBJECT",
    )
    require(
        invariants((44, 44, 44))[2] - invariants(triangle_only)[2] == q_t
        and triangle_only != scene,
        "TRIANGLE_FACE_SECOND_OBJECT",
    )
    print(
        "PASS_SINGLE_CAPACITY_FACE_INSUFFICIENT: edge-only second object "
        f"{edge_only}; triangle-only second object {triangle_only}."
    )

    # Reachable conclusion-failing controls.
    spread1 = (v11 - 1, v11, v11 + 1)
    spread3 = (v11 - 3, v11, v11 + 3)
    center10 = (10 - dyad, 10, 10 + dyad)
    expect_rejected(
        "SPREAD_ONE_IS_OMEGA8",
        squared_anisotropy(spread1, v11) == omega8,
    )
    expect_rejected(
        "SPREAD_THREE_EDGE_DEFECT_IS_ABCD",
        invariants(equal_zone)[1] - invariants(spread3)[1] == abcd,
    )
    expect_rejected(
        "CENTER_TEN_TRIANGLE_DEFECT_IS_QT",
        invariants((10, 10, 10))[2] - invariants(center10)[2] == q_t,
    )

    print(
        "PASS_SCENE_ANISOTROPY_CAPACITY_WELD: Dyad -> ABCD/Omega8 -> "
        "V11-centered scene -> qT; the pair (ABCD,qT) reconstructs the scene, "
        "and the same spread controls the cubic anisotropy discriminant."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
