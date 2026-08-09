#!/usr/bin/env python3
"""Can-fail certificate for D0-CARRIER-TOPOLOGICAL-SCENE-PASSPORT-001.

Audited class: ordered positive complete-tripartite zone triples `(a,b,c)`.
The certificate independently checks that either of the topological passports

    (V, chi) = (33, 961),
    (V, R)   = (33, 960)

uniquely reconstructs `(9,11,13)`, where

    chi   = V - E + T,
    R = (a-1)(b-1)(c-1).

The generic Lean boundary theorem and its explicit finite-carrier transport
now prove `R=beta2` over the rationals for every nonempty finite typed triple.
This arithmetic certificate retains the symbol `R` because it checks the
cardinality reconstruction independently of the Lean chain maps.
"""

from __future__ import annotations


TARGET = (9, 11, 13)
V_TARGET = 33
CHI_TARGET = 961
REDUCED_TARGET = 960


def ordered_positive(triple: tuple[int, int, int]) -> bool:
    a, b, c = triple
    return 0 < a <= b <= c


def invariants(
    triple: tuple[int, int, int],
) -> tuple[int, int, int, int, int]:
    a, b, c = triple
    vertices = a + b + c
    edges = a * b + a * c + b * c
    triangles = a * b * c
    chi = vertices - edges + triangles
    # Match Lean/Nat subtraction exactly, including the non-positive mutation.
    reduced_product = max(a - 1, 0) * max(b - 1, 0) * max(c - 1, 0)
    return vertices, edges, triangles, chi, reduced_product


def candidates_from_vertex_count(v: int) -> set[tuple[int, int, int]]:
    out: set[tuple[int, int, int]] = set()
    for a in range(1, v + 1):
        for b in range(a, v + 1):
            c = v - a - b
            triple = (a, b, c)
            if ordered_positive(triple):
                out.add(triple)
    return out


def candidates_from_reduced_product(
    reduced_target: int,
) -> set[tuple[int, int, int]]:
    out: set[tuple[int, int, int]] = set()
    # (a-1)(b-1)(c-1)=reduced_target.  Enumerate its ordered positive
    # factorisations without imposing the vertex target.
    for x in range(1, reduced_target + 1):
        if reduced_target % x:
            continue
        rem = reduced_target // x
        for y in range(x, rem + 1):
            if rem % y:
                continue
            z = rem // y
            if y <= z:
                out.add((x + 1, y + 1, z + 1))
    return out


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
        "STRUCTURE_FIXED_BEFORE_NUMBER: ordered positive complete-tripartite "
        "triples generate V/E/T, chi, and the reduced product before the "
        "(9,11,13) reconstruction claim."
    )

    v_set = candidates_from_vertex_count(V_TARGET)
    reduced_set = candidates_from_reduced_product(REDUCED_TARGET)
    chi_set = {
        triple
        for triple in v_set
        if invariants(triple)[3] == CHI_TARGET
    }
    v_beta = {
        triple
        for triple in v_set
        if invariants(triple)[4] == REDUCED_TARGET
    }

    require(
        invariants(TARGET) == (33, 359, 1287, 961, REDUCED_TARGET),
        "TARGET_TOPOLOGICAL_COORDINATES",
    )
    require(chi_set == {TARGET}, f"VERTEX_EULER_NOT_UNIQUE_{sorted(chi_set)}")
    require(v_beta == {TARGET}, f"VERTEX_BETA2_NOT_UNIQUE_{sorted(v_beta)}")
    print("PASS_VERTEX_EULER_RECONSTRUCTION: (V,chi)=(33,961) -> (9,11,13).")
    print("PASS_VERTEX_REDUCED_RECONSTRUCTION: (V,R)=(33,960) -> (9,11,13).")

    # Positive identity behind the equivalence of the two passports.
    for triple in v_set:
        vertices, edges, triangles, chi, reduced = invariants(triple)
        require(chi == 1 + reduced, f"EULER_PRODUCT_IDENTITY_{triple}")
        require(vertices == sum(triple), f"VERTEX_OWNER_ALIGNMENT_{triple}")
        require(chi == vertices - edges + triangles, f"EULER_FVECTOR_{triple}")
    print("PASS_POSITIVE_EULER_PRODUCT_IDENTITY: chi=1+(a-1)(b-1)(c-1).")

    # Euler/reduced-product alone is not sufficient.  The second object is a real
    # topological collision and differs only in the missing V coordinate.
    collision = (9, 9, 16)
    require(collision in reduced_set, "COLLISION_NOT_ENUMERATED")
    require(
        invariants(collision)[3:] == (CHI_TARGET, REDUCED_TARGET),
        "COLLISION_VALUES",
    )
    require(invariants(collision)[0] == 34, "COLLISION_WRONG_VERTEX_COUNT")
    print(
        "PASS_SINGLE_TOPOLOGICAL_FACE_INSUFFICIENT: "
        "(9,9,16) has chi=961 and R=960 but V=34."
    )

    expect_rejected(
        "EULER_ALONE_RECONSTRUCTS_SCENE",
        {t for t in reduced_set if invariants(t)[3] == CHI_TARGET} == {TARGET},
    )
    expect_rejected(
        "MUTATE_VERTEX_TARGET_34",
        {
            t
            for t in candidates_from_vertex_count(34)
            if invariants(t)[3] == CHI_TARGET
        }
        == {TARGET},
    )
    vertex_only_collision = (8, 11, 14)
    require(
        invariants(vertex_only_collision)[0] == V_TARGET
        and vertex_only_collision != TARGET,
        "VERTEX_ONLY_COLLISION",
    )
    expect_rejected(
        "VERTEX_ALONE_RECONSTRUCTS_SCENE",
        v_set == {TARGET},
    )
    permutation = (11, 9, 13)
    require(
        invariants(permutation)[0] == V_TARGET
        and invariants(permutation)[3] == CHI_TARGET,
        "ORDERING_COLLISION_VALUES",
    )
    expect_rejected(
        "DROP_ORDERING_PRESERVES_ORDERED_CONCLUSION",
        permutation == TARGET,
    )
    expect_rejected(
        "DROP_POSITIVITY_PRESERVES_IDENTITY",
        invariants((0, 2, 2))[3] == 1 + invariants((0, 2, 2))[4],
    )
    expect_rejected(
        "MUTATE_EULER_TARGET_960",
        {
            t
            for t in v_set
            if invariants(t)[3] == CHI_TARGET - 1
        }
        == {TARGET},
    )

    print(
        "PASS_CARRIER_TOPOLOGICAL_SCENE_PASSPORT: total carrier plus Euler "
        "(or its reduced-product factorization) uniquely reconstructs "
        "the ordered D0 scene."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
