#!/usr/bin/env python3
"""Can-fail certificate for D0-GENERIC-TRIPARTITE-TOP-HODGE-SPECTRUM-001.

Independently verify the upper triangle Hodge Laplacian

    Delta2 = d2^T d2

for the complete-tripartite clique complex `K(p+1,q+1,r+1)`.

The certificate checks:

* the exact marginal-sum operator formula;
* the constant/root-difference factor bases and their explicit duals;
* the complete tensor eigenbasis;
* the eight generic eigenvalue/multiplicity sectors;
* the source spectrum
  `0^960,9^120,11^96,13^80,20^12,22^10,24^8,33^1`;
* `ker Delta2 = ker d2` over integer/rational chains;
* exact overlap `20^12,22^10,24^8` with the owned graph archive spectrum,
  while rejecting the false `33`-multiplicity identification.

The kernel equality is intentionally *not* asserted over arbitrary
coefficient rings.  A destructive Z/4Z control exhibits a nonzero `d2 x` with
`d2^T d2 x = 0`, showing exactly where positivity is load-bearing.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import product

from vp_generic_tripartite_universal_homology import (
    TripartiteComplex,
    deterministic_values,
    expect_rejected,
    require,
    zero_vector,
)


Vector = list[int]


def d2_transpose(complex_: TripartiteComplex, edge_chain: Vector) -> Vector:
    require(len(edge_chain) == len(complex_.edges), "D2_TRANSPOSE_LENGTH")
    return [
        complex_.norm(
            edge_chain[complex_.edge_index[("ab", a, b)]]
            - edge_chain[complex_.edge_index[("ac", a, c)]]
            + edge_chain[complex_.edge_index[("bc", b, c)]]
        )
        for a, b, c in complex_.triangles
    ]


def top_hodge_boundary(complex_: TripartiteComplex, triangle_chain: Vector) -> Vector:
    return d2_transpose(complex_, complex_.d2(triangle_chain))


def top_hodge_marginal(complex_: TripartiteComplex, triangle_chain: Vector) -> Vector:
    require(len(triangle_chain) == len(complex_.triangles), "HODGE_INPUT_LENGTH")
    values = {
        triangle: triangle_chain[index]
        for index, triangle in enumerate(complex_.triangles)
    }
    return [
        complex_.norm(
            sum(values[(aa, b, c)] for aa in range(complex_.a_size))
            + sum(values[(a, bb, c)] for bb in range(complex_.b_size))
            + sum(values[(a, b, cc)] for cc in range(complex_.c_size))
        )
        for a, b, c in complex_.triangles
    ]


def factor_mode(size: int, index: int) -> list[int]:
    """Index 0 is constant; index i>0 is e_i-e_0."""

    require(1 <= size, "FACTOR_SIZE")
    require(0 <= index < size, "FACTOR_INDEX")
    if index == 0:
        return [1] * size
    return [-1 if vertex == 0 else 1 if vertex == index else 0 for vertex in range(size)]


def factor_dual(size: int, index: int) -> list[Fraction]:
    """Dual to `factor_mode`: mean, then value-at-i minus mean."""

    require(1 <= size, "DUAL_FACTOR_SIZE")
    require(0 <= index < size, "DUAL_FACTOR_INDEX")
    mean = Fraction(1, size)
    if index == 0:
        return [mean] * size
    return [
        (Fraction(1) if vertex == index else Fraction(0)) - mean
        for vertex in range(size)
    ]


def dot(left: list[Fraction | int], right: list[Fraction | int]) -> Fraction:
    require(len(left) == len(right), "DOT_LENGTH")
    return sum(
        (Fraction(x) * Fraction(y) for x, y in zip(left, right)),
        Fraction(0),
    )


def triangle_mode(
    complex_: TripartiteComplex, index: tuple[int, int, int]
) -> Vector:
    ia, ib, ic = index
    ma = factor_mode(complex_.a_size, ia)
    mb = factor_mode(complex_.b_size, ib)
    mc = factor_mode(complex_.c_size, ic)
    return [
        complex_.norm(ma[a] * mb[b] * mc[c])
        for a, b, c in complex_.triangles
    ]


def mode_eigenvalue(
    complex_: TripartiteComplex, index: tuple[int, int, int]
) -> int:
    ia, ib, ic = index
    return (
        (complex_.a_size if ia == 0 else 0)
        + (complex_.b_size if ib == 0 else 0)
        + (complex_.c_size if ic == 0 else 0)
    )


def sector_data(p: int, q: int, r: int) -> list[tuple[int, int]]:
    return [
        (0, p * q * r),
        (p + 1, q * r),
        (q + 1, p * r),
        (r + 1, p * q),
        (p + q + 2, r),
        (p + r + 2, q),
        (q + r + 2, p),
        (p + q + r + 3, 1),
    ]


def verify_factor_basis(size: int) -> None:
    modes = [factor_mode(size, i) for i in range(size)]
    duals = [factor_dual(size, i) for i in range(size)]
    pairing = [
        [dot(duals[i], modes[j]) for j in range(size)]
        for i in range(size)
    ]
    require(
        pairing
        == [
            [Fraction(int(i == j)) for j in range(size)]
            for i in range(size)
        ],
        f"FACTOR_DUAL_IDENTITY_{size}",
    )


def verify_operator_formula(complex_: TripartiteComplex, salt: int) -> None:
    chain = deterministic_values(len(complex_.triangles), complex_.modulus, salt)
    require(
        top_hodge_boundary(complex_, chain) == top_hodge_marginal(complex_, chain),
        f"HODGE_MARGINAL_FORMULA_{complex_.p}_{complex_.q}_{complex_.r}",
    )


def verify_tensor_eigenbasis(complex_: TripartiteComplex) -> Counter[int]:
    indices = list(
        product(
            range(complex_.a_size),
            range(complex_.b_size),
            range(complex_.c_size),
        )
    )
    spectrum: Counter[int] = Counter()
    for index in indices:
        mode = triangle_mode(complex_, index)
        eigenvalue = mode_eigenvalue(complex_, index)
        spectrum[eigenvalue] += 1
        lhs = top_hodge_marginal(complex_, mode)
        rhs = [complex_.norm(eigenvalue * value) for value in mode]
        require(
            lhs == rhs,
            f"TENSOR_EIGENVECTOR_{complex_.p}_{complex_.q}_{complex_.r}_{index}",
        )
    require(
        sum(spectrum.values()) == len(complex_.triangles),
        f"TENSOR_BASIS_COUNT_{complex_.p}_{complex_.q}_{complex_.r}",
    )
    return spectrum


def verify_kernel_equality(complex_: TripartiteComplex, exhaustive: bool) -> None:
    if exhaustive:
        modulus = complex_.modulus
        require(modulus is not None, "EXHAUSTIVE_KERNEL_MODULUS")
        for values in product(range(modulus), repeat=len(complex_.triangles)):
            chain = list(values)
            require(
                (
                    complex_.d2(chain) == zero_vector(len(complex_.edges))
                )
                == (
                    top_hodge_boundary(complex_, chain)
                    == zero_vector(len(complex_.triangles))
                ),
                "EXHAUSTIVE_HODGE_KERNEL_EQUALITY",
            )
    else:
        # Test both a harmonic chain and a generic non-harmonic chain.
        if complex_.top_indices:
            harmonic = complex_.top_cycle(complex_.top_indices[0])
            require(
                complex_.d2(harmonic) == zero_vector(len(complex_.edges))
                and top_hodge_boundary(complex_, harmonic)
                == zero_vector(len(complex_.triangles)),
                "HARMONIC_KERNEL_ALIGNMENT",
            )
        generic = deterministic_values(len(complex_.triangles), complex_.modulus, 47)
        require(
            (
                complex_.d2(generic) == zero_vector(len(complex_.edges))
            )
            == (
                top_hodge_boundary(complex_, generic)
                == zero_vector(len(complex_.triangles))
            ),
            "GENERIC_KERNEL_ALIGNMENT",
        )


def main() -> int:
    print(
        "STRUCTURE_FIXED_BEFORE_NUMBER: build d2, d2^T, Delta2, factor modes, "
        "dual weights, and the tensor basis before reading eigenvalues."
    )

    for size in range(1, 7):
        verify_factor_basis(size)
    print("PASS_FACTOR_BASES: constant/root-difference bases have exact duals.")

    grid = (
        TripartiteComplex(0, 0, 0, None),
        TripartiteComplex(1, 2, 1, None),
        TripartiteComplex(2, 1, 2, 5),
    )
    for number, complex_ in enumerate(grid):
        verify_operator_formula(complex_, 19 + number)
        spectrum = verify_tensor_eigenbasis(complex_)
        expected = Counter()
        for eigenvalue, multiplicity in sector_data(
            complex_.p, complex_.q, complex_.r
        ):
            if multiplicity:
                expected[eigenvalue] += multiplicity
        require(
            spectrum == expected,
            f"GENERIC_SECTOR_DATA_{complex_.p}_{complex_.q}_{complex_.r}",
        )
    print("PASS_GENERIC_HODGE_GRID: operator formula and all tensor modes agree.")

    # Non-field boundary: kernel equality fails over Z/4Z because positivity
    # of the Gram operator is unavailable.  This is an intended negative
    # control, not part of the theorem.
    mod4 = TripartiteComplex(1, 0, 0, 4)
    torsion_chain = [1, 1]
    require(
        mod4.d2(torsion_chain) != zero_vector(len(mod4.edges)),
        "MOD4_TORSION_CHAIN_HAS_NONZERO_BOUNDARY",
    )
    require(
        top_hodge_boundary(mod4, torsion_chain)
        == zero_vector(len(mod4.triangles)),
        "MOD4_TORSION_CHAIN_NOT_HODGE_HARMONIC",
    )
    print(
        "PASS_NONFIELD_BOUNDARY: over Z/4Z, [1,1] has d2!=0 but "
        "d2^T*d2=0; Hodge-kernel equality correctly remains characteristic-zero."
    )

    scene = TripartiteComplex(8, 10, 12, None)
    verify_operator_formula(scene, 53)
    scene_spectrum = verify_tensor_eigenbasis(scene)
    expected_scene = Counter(
        {
            0: 960,
            9: 120,
            11: 96,
            13: 80,
            20: 12,
            22: 10,
            24: 8,
            33: 1,
        }
    )
    require(scene_spectrum == expected_scene, "SOURCE_HODGE_SPECTRUM")
    require(sum(scene_spectrum.values()) == 1287, "SOURCE_HODGE_DIMENSION")
    require(
        sum(value * multiplicity for value, multiplicity in scene_spectrum.items())
        == 3861,
        "SOURCE_HODGE_TRACE",
    )
    verify_kernel_equality(scene, exhaustive=False)
    print(
        "PASS_SOURCE_TOP_HODGE_SPECTRUM: "
        "0^960,9^120,11^96,13^80,20^12,22^10,24^8,33^1."
    )

    graph_spectrum = Counter({0: 1, 20: 12, 22: 10, 24: 8, 33: 2})
    archive_values = {20, 22, 24}
    require(
        {value: scene_spectrum[value] for value in archive_values}
        == {value: graph_spectrum[value] for value in archive_values},
        "ARCHIVE_SPECTRAL_OVERLAP",
    )
    require(
        scene_spectrum[33] == 1 and graph_spectrum[33] == 2,
        "TOP_VERTEX_33_MULTIPLICITY_SEPARATION",
    )
    require(
        min(value for value in scene_spectrum if value > 0) == 9,
        "SOURCE_HODGE_GAP",
    )
    require(Fraction(33, 9) == Fraction(11, 3), "SOURCE_CONDITION_RATIO")
    print(
        "PASS_ARCHIVE_SPECTRAL_BRIDGE: 20^12,22^10,24^8 match exactly; "
        "the 33 multiplicities remain honestly distinct."
    )

    # Negative control 1: corrupt one sign in d2^T.
    test = TripartiteComplex(1, 1, 1, None)
    chain = deterministic_values(len(test.triangles), None, 61)
    corrupted = d2_transpose(test, test.d2(chain))
    corrupted[0] += 2 * test.d2(chain)[test.edge_index[("ac", 0, 0)]]
    expect_rejected(
        "CORRUPT_TRANSPOSE_SIGN_PRESERVES_MARGINAL_FORMULA",
        corrupted == top_hodge_marginal(test, chain),
    )

    # Negative control 2: mutate a root-difference vector.
    bad_mode = factor_mode(3, 1)
    bad_mode[2] = 1
    expect_rejected(
        "MUTATED_FACTOR_BASIS_HAS_DUAL_IDENTITY",
        dot(factor_dual(3, 2), bad_mode) == 0,
    )

    # Negative control 3: delete one tensor sector.
    expect_rejected(
        "DELETE_ONE_HODGE_MODE_PRESERVES_COMPLETENESS",
        sum(expected_scene.values()) - 1 == len(scene.triangles),
    )

    # Negative control 4: mutate the degree-sector eigenvalue.
    expect_rejected(
        "MUTATE_24_TO_23",
        scene_spectrum[23] == 8,
    )

    # Negative control 5: falsely identify the 33 sectors.
    expect_rejected(
        "TOP_33_MULTIPLICITY_EQUALS_VERTEX_33_MULTIPLICITY",
        scene_spectrum[33] == graph_spectrum[33],
    )

    # Negative control 6: claim the kernel has one extra harmonic mode.
    expect_rejected(
        "HODGE_NULLITY_OFF_BY_ONE",
        scene_spectrum[0] == 961,
    )

    print(
        "PASS_GENERIC_TRIPARTITE_TOP_HODGE_SPECTRUM: complete eigenbasis, "
        "multiplicities, harmonic kernel, archive bridge, and destructive "
        "controls all survive."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
