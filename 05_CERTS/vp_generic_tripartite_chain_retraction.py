#!/usr/bin/env python3
"""Can-fail certificate for D0-GENERIC-TRIPARTITE-CHAIN-RETRACTION-001.

Test the three explicit chain-retraction identities

    d1 h0 + i0 p0 = id on C0,
    d2 h1 + h0 d1 = id on C1,
    h1 d2 + i2 p2 = id on C2,

where `p0` is augmentation, `i0` selects the root vertex, `p2` reads
all-nonroot triangle coordinates, and `i2` synthesizes octahedral cycles.

The checks include integers and the non-fields Z/4Z and Z/6Z.
"""

from __future__ import annotations

from itertools import product

from vp_generic_tripartite_universal_homology import (
    TripartiteComplex,
    deterministic_values,
    expect_rejected,
    normalize_vector,
    require,
    zero_vector,
)


Vector = list[int]


def add_vectors(complex_: TripartiteComplex, left: Vector, right: Vector) -> Vector:
    require(len(left) == len(right), "ADD_LENGTH")
    return normalize_vector(
        [x + y for x, y in zip(left, right)],
        complex_.modulus,
    )


def sub_vectors(complex_: TripartiteComplex, left: Vector, right: Vector) -> Vector:
    require(len(left) == len(right), "SUB_LENGTH")
    return normalize_vector(
        [x - y for x, y in zip(left, right)],
        complex_.modulus,
    )


def zero_inclusion(complex_: TripartiteComplex, coefficient: int) -> Vector:
    out = zero_vector(len(complex_.vertices))
    out[complex_.vertex_index[(0, 0)]] = complex_.norm(coefficient)
    return out


def reduced_zero_chain(complex_: TripartiteComplex, chain: Vector) -> Vector:
    return sub_vectors(
        complex_,
        chain,
        zero_inclusion(complex_, complex_.augmentation(chain)),
    )


def contract0(complex_: TripartiteComplex, chain: Vector) -> Vector:
    reduced = reduced_zero_chain(complex_, chain)
    require(complex_.augmentation(reduced) == 0, "CONTRACT0_REDUCED_AUGMENTATION")
    return complex_.h0_fill(reduced)


def reduced_one_chain(complex_: TripartiteComplex, chain: Vector) -> Vector:
    return sub_vectors(complex_, chain, contract0(complex_, complex_.d1(chain)))


def contract1(complex_: TripartiteComplex, chain: Vector) -> Vector:
    reduced = reduced_one_chain(complex_, chain)
    require(
        complex_.d1(reduced) == zero_vector(len(complex_.vertices)),
        "CONTRACT1_REDUCED_NOT_CYCLE",
    )
    return complex_.h1_fill(reduced)


def top_projection(complex_: TripartiteComplex, chain: Vector) -> dict[tuple[int, int, int], int]:
    return complex_.top_coordinates(chain)


def top_inclusion(
    complex_: TripartiteComplex,
    coordinates: dict[tuple[int, int, int], int],
) -> Vector:
    return complex_.top_synthesis(coordinates)


def verify_retraction(complex_: TripartiteComplex, salt: int) -> None:
    c0 = deterministic_values(len(complex_.vertices), complex_.modulus, salt)
    c1 = deterministic_values(len(complex_.edges), complex_.modulus, salt + 3)
    c2 = deterministic_values(len(complex_.triangles), complex_.modulus, salt + 7)

    degree0 = add_vectors(
        complex_,
        complex_.d1(contract0(complex_, c0)),
        zero_inclusion(complex_, complex_.augmentation(c0)),
    )
    require(
        degree0 == c0,
        f"DEGREE0_IDENTITY_{complex_.p}_{complex_.q}_{complex_.r}_{complex_.modulus}",
    )

    degree1 = add_vectors(
        complex_,
        complex_.d2(contract1(complex_, c1)),
        contract0(complex_, complex_.d1(c1)),
    )
    require(
        degree1 == c1,
        f"DEGREE1_IDENTITY_{complex_.p}_{complex_.q}_{complex_.r}_{complex_.modulus}",
    )

    degree2 = add_vectors(
        complex_,
        contract1(complex_, complex_.d2(c2)),
        top_inclusion(complex_, top_projection(complex_, c2)),
    )
    require(
        degree2 == c2,
        f"DEGREE2_IDENTITY_{complex_.p}_{complex_.q}_{complex_.r}_{complex_.modulus}",
    )

    coefficient = complex_.norm(salt * 7 - 3)
    require(
        complex_.augmentation(zero_inclusion(complex_, coefficient)) == coefficient,
        f"DEGREE0_SPLIT_{complex_.p}_{complex_.q}_{complex_.r}",
    )

    coordinates = {
        index: complex_.norm(
            (index[0] + 1) - 2 * (index[1] + 1) + 3 * (index[2] + 1)
        )
        for index in complex_.top_indices
    }
    require(
        top_projection(complex_, top_inclusion(complex_, coordinates)) == coordinates,
        f"DEGREE2_SPLIT_{complex_.p}_{complex_.q}_{complex_.r}",
    )


def exhaustive_retraction(complex_: TripartiteComplex) -> None:
    modulus = complex_.modulus
    require(modulus is not None, "EXHAUSTIVE_REQUIRES_MODULUS")

    for values in product(range(modulus), repeat=len(complex_.vertices)):
        chain = list(values)
        lhs = add_vectors(
            complex_,
            complex_.d1(contract0(complex_, chain)),
            zero_inclusion(complex_, complex_.augmentation(chain)),
        )
        require(lhs == chain, "EXHAUSTIVE_DEGREE0")

    for values in product(range(modulus), repeat=len(complex_.edges)):
        chain = list(values)
        lhs = add_vectors(
            complex_,
            complex_.d2(contract1(complex_, chain)),
            contract0(complex_, complex_.d1(chain)),
        )
        require(lhs == chain, "EXHAUSTIVE_DEGREE1")

    for values in product(range(modulus), repeat=len(complex_.triangles)):
        chain = list(values)
        lhs = add_vectors(
            complex_,
            contract1(complex_, complex_.d2(chain)),
            top_inclusion(complex_, top_projection(complex_, chain)),
        )
        require(lhs == chain, "EXHAUSTIVE_DEGREE2")


def main() -> int:
    print(
        "STRUCTURE_FIXED_BEFORE_NUMBER: construct p0/i0, h0, h1, p2/i2 "
        "before testing the three chain identities."
    )

    cases = (
        TripartiteComplex(0, 0, 0, None),
        TripartiteComplex(2, 3, 1, None),
        TripartiteComplex(1, 0, 0, 6),
        TripartiteComplex(1, 1, 1, 4),
    )
    for index, complex_ in enumerate(cases):
        verify_retraction(complex_, salt=11 + index)
    print("PASS_CHAIN_RETRACTION_GRID: integer, Z/4Z, and Z/6Z identities hold.")

    # Exhaust all chains for a small non-field complex.
    exhaustive_retraction(TripartiteComplex(1, 0, 0, 4))
    print("PASS_NONFIELD_CHAIN_EXHAUSTION: every chain over Z/4Z satisfies the identities.")

    # Source scene: includes the 960-coordinate degree-two projection.
    scene = TripartiteComplex(8, 10, 12, None)
    verify_retraction(scene, salt=29)
    require(len(scene.top_indices) == 960, "SCENE_RETRACTION_TOP_COUNT")
    print(
        "PASS_SOURCE_CHAIN_RETRACTION: scene retracts to Z in degree 0 "
        "and Z^960 in degree 2."
    )

    cube = TripartiteComplex(1, 1, 1, None)
    c0 = deterministic_values(len(cube.vertices), None, 31)
    c1 = deterministic_values(len(cube.edges), None, 37)
    c2 = deterministic_values(len(cube.triangles), None, 41)

    # Negative 1: corrupt the root inclusion.
    bad_i0 = zero_inclusion(cube, cube.augmentation(c0))
    bad_i0[cube.vertex_index[(1, 0)]] += 1
    expect_rejected(
        "CORRUPT_DEGREE0_INCLUSION",
        add_vectors(cube, cube.d1(contract0(cube, c0)), bad_i0) == c0,
    )

    # Negative 2: omit the tree correction before applying h1.
    expect_rejected(
        "OMIT_H0_CORRECTION_IN_DEGREE1",
        add_vectors(
            cube,
            cube.d2(cube.h1_fill(c1)),
            contract0(cube, cube.d1(c1)),
        )
        == c1,
    )

    # Negative 3: use root-triangle readings instead of all-nonroot p2.
    wrong_coordinates = {
        index: c2[cube.triangle_index[(0, index[1] + 1, index[2] + 1)]]
        for index in cube.top_indices
    }
    expect_rejected(
        "ROOT_COORDINATES_PRESERVE_DEGREE2_IDENTITY",
        add_vectors(
            cube,
            contract1(cube, cube.d2(c2)),
            top_inclusion(cube, wrong_coordinates),
        )
        == c2,
    )

    # Negative 4: drop the top-homology projection entirely.
    expect_rejected(
        "DROP_TOP_PROJECTION",
        contract1(cube, cube.d2(c2)) == c2,
    )

    # Negative 5: corrupt one coefficient in the octahedral inclusion.
    coordinates = top_projection(cube, c2)
    bad_top = top_inclusion(cube, coordinates)
    first_nonzero = next(i for i, value in enumerate(bad_top) if value)
    bad_top[first_nonzero] += 1
    expect_rejected(
        "CORRUPT_TOP_INCLUSION",
        add_vectors(cube, contract1(cube, cube.d2(c2)), bad_top) == c2,
    )

    print(
        "PASS_GENERIC_TRIPARTITE_CHAIN_RETRACTION: all three explicit "
        "chain-homotopy identities survive non-field, source, exhaustive, "
        "and destructive tests."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
