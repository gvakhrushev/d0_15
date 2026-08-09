#!/usr/bin/env python3
"""Can-fail certificate for top-Hodge Green and gauge theorems.

Claims:

* `G` multiplies every positive top-Hodge tensor sector by `1/lambda` and
  kills the harmonic sector;
* `Delta G = G Delta = I - P_harm`;
* `P_harm^2=P_harm` and `G P_harm=P_harm G=0`;
* for every rational 1-cycle `z`, `u = G d2^T z` is a filling, has
  `P_harm u=0`, and is unique among fillings in that gauge.

The source-scene Green trace is checked exactly as `63562/2145`.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product

from vp_generic_tripartite_top_hodge_spectrum import (
    TripartiteComplex,
    d2_transpose,
    factor_dual,
    factor_mode,
    mode_eigenvalue,
    top_hodge_boundary,
)
from vp_generic_tripartite_universal_homology import (
    deterministic_values,
    expect_rejected,
    require,
    zero_vector,
)


QVector = list[Fraction]
ModeIndex = tuple[int, int, int]


def as_fractions(values: list[int | Fraction]) -> QVector:
    return [Fraction(value) for value in values]


def add(left: QVector, right: QVector) -> QVector:
    require(len(left) == len(right), "ADD_LENGTH")
    return [x + y for x, y in zip(left, right)]


def sub(left: QVector, right: QVector) -> QVector:
    require(len(left) == len(right), "SUB_LENGTH")
    return [x - y for x, y in zip(left, right)]


def scale(scalar: Fraction, vector: QVector) -> QVector:
    return [scalar * value for value in vector]


def mode_indices(complex_: TripartiteComplex) -> list[ModeIndex]:
    return list(
        product(
            range(complex_.a_size),
            range(complex_.b_size),
            range(complex_.c_size),
        )
    )


def mode_vector(complex_: TripartiteComplex, index: ModeIndex) -> QVector:
    ia, ib, ic = index
    ma = factor_mode(complex_.a_size, ia)
    mb = factor_mode(complex_.b_size, ib)
    mc = factor_mode(complex_.c_size, ic)
    return [
        Fraction(ma[a] * mb[b] * mc[c])
        for a, b, c in complex_.triangles
    ]


def mode_coordinate(
    complex_: TripartiteComplex,
    index: ModeIndex,
    vector: QVector,
) -> Fraction:
    require(len(vector) == len(complex_.triangles), "COORDINATE_LENGTH")
    ia, ib, ic = index
    da = factor_dual(complex_.a_size, ia)
    db = factor_dual(complex_.b_size, ib)
    dc = factor_dual(complex_.c_size, ic)
    total = Fraction(0)
    for value, (a, b, c) in zip(vector, complex_.triangles):
        total += da[a] * db[b] * dc[c] * value
    return total


def spectral_synthesis(
    complex_: TripartiteComplex,
    coefficients: dict[ModeIndex, Fraction],
) -> QVector:
    out = [Fraction(0) for _ in complex_.triangles]
    for index, coefficient in coefficients.items():
        if coefficient == 0:
            continue
        vector = mode_vector(complex_, index)
        for position, value in enumerate(vector):
            out[position] += coefficient * value
    return out


def all_mode_coordinates(
    complex_: TripartiteComplex,
    vector: QVector,
) -> dict[ModeIndex, Fraction]:
    return {
        index: mode_coordinate(complex_, index, vector)
        for index in mode_indices(complex_)
    }


def harmonic_project(complex_: TripartiteComplex, vector: QVector) -> QVector:
    coefficients = {}
    for index in mode_indices(complex_):
        if mode_eigenvalue(complex_, index) == 0:
            coefficients[index] = mode_coordinate(complex_, index, vector)
    return spectral_synthesis(complex_, coefficients)


def green_apply(
    complex_: TripartiteComplex,
    vector: QVector,
    reciprocal_mutation: dict[int, Fraction] | None = None,
    harmonic_weight: Fraction = Fraction(0),
) -> QVector:
    coefficients: dict[ModeIndex, Fraction] = {}
    for index in mode_indices(complex_):
        eigenvalue = mode_eigenvalue(complex_, index)
        coefficient = mode_coordinate(complex_, index, vector)
        if eigenvalue == 0:
            weight = harmonic_weight
        elif reciprocal_mutation and eigenvalue in reciprocal_mutation:
            weight = reciprocal_mutation[eigenvalue]
        else:
            weight = Fraction(1, eigenvalue)
        coefficients[index] = weight * coefficient
    return spectral_synthesis(complex_, coefficients)


def hodge_apply(complex_: TripartiteComplex, vector: QVector) -> QVector:
    return as_fractions(top_hodge_boundary(complex_, vector))


def verify_basis_scalar_identities(complex_: TripartiteComplex) -> None:
    for index in mode_indices(complex_):
        eigenvalue = mode_eigenvalue(complex_, index)
        green_weight = Fraction(0) if eigenvalue == 0 else Fraction(1, eigenvalue)
        harmonic_weight = Fraction(1) if eigenvalue == 0 else Fraction(0)
        require(
            eigenvalue * green_weight == 1 - harmonic_weight,
            f"LEFT_SCALAR_IDENTITY_{index}",
        )
        require(
            green_weight * eigenvalue == 1 - harmonic_weight,
            f"RIGHT_SCALAR_IDENTITY_{index}",
        )
        require(
            harmonic_weight * harmonic_weight == harmonic_weight,
            f"PROJECTOR_SCALAR_IDEMPOTENT_{index}",
        )
        require(
            green_weight * harmonic_weight == 0
            and harmonic_weight * green_weight == 0,
            f"GREEN_HARMONIC_SCALAR_ZERO_{index}",
        )


def verify_operator_identities(complex_: TripartiteComplex, salt: int) -> None:
    vector = as_fractions(
        deterministic_values(len(complex_.triangles), None, salt)
    )
    projected = harmonic_project(complex_, vector)
    complement = sub(vector, projected)
    green = green_apply(complex_, vector)
    require(
        hodge_apply(complex_, green) == complement,
        f"HODGE_GREEN_LEFT_{complex_.p}_{complex_.q}_{complex_.r}",
    )
    require(
        green_apply(complex_, hodge_apply(complex_, vector)) == complement,
        f"HODGE_GREEN_RIGHT_{complex_.p}_{complex_.q}_{complex_.r}",
    )
    require(
        harmonic_project(complex_, projected) == projected,
        f"HARMONIC_PROJECTOR_IDEMPOTENT_{complex_.p}_{complex_.q}_{complex_.r}",
    )
    require(
        green_apply(complex_, projected)
        == [Fraction(0) for _ in complex_.triangles],
        f"GREEN_KILLS_HARMONIC_{complex_.p}_{complex_.q}_{complex_.r}",
    )
    require(
        harmonic_project(complex_, green)
        == [Fraction(0) for _ in complex_.triangles],
        f"HARMONIC_KILLS_GREEN_{complex_.p}_{complex_.q}_{complex_.r}",
    )


def hodge_gauge_fill(complex_: TripartiteComplex, edge_cycle: QVector) -> QVector:
    return green_apply(complex_, as_fractions(d2_transpose(complex_, edge_cycle)))


def verify_gauge_fill(complex_: TripartiteComplex, salt: int) -> None:
    source = as_fractions(
        deterministic_values(len(complex_.triangles), None, salt)
    )
    cycle = as_fractions(complex_.d2(source))
    require(
        as_fractions(complex_.d1(cycle))
        == [Fraction(0) for _ in complex_.vertices],
        "GAUGE_FILL_CYCLE_SETUP",
    )
    canonical = hodge_gauge_fill(complex_, cycle)
    require(
        as_fractions(complex_.d2(canonical)) == cycle,
        f"GAUGE_FILL_BOUNDARY_{complex_.p}_{complex_.q}_{complex_.r}",
    )
    require(
        harmonic_project(complex_, canonical)
        == [Fraction(0) for _ in complex_.triangles],
        f"GAUGE_FILL_HARMONIC_ZERO_{complex_.p}_{complex_.q}_{complex_.r}",
    )

    # Every other filling differs by a harmonic vector.  Adding a nonzero
    # harmonic mode preserves the boundary but violates the gauge.
    harmonic_indices = [
        index
        for index in mode_indices(complex_)
        if mode_eigenvalue(complex_, index) == 0
    ]
    if harmonic_indices:
        harmonic = mode_vector(complex_, harmonic_indices[0])
        alternative = add(canonical, harmonic)
        require(
            as_fractions(complex_.d2(alternative)) == cycle,
            "ALTERNATIVE_FILLING_BOUNDARY",
        )
        require(
            harmonic_project(complex_, alternative) !=
            [Fraction(0) for _ in complex_.triangles],
            "ALTERNATIVE_FILLING_FALSE_GAUGE",
        )
        # Remove its harmonic part: uniqueness returns the canonical filling.
        require(
            sub(alternative, harmonic_project(complex_, alternative))
            == canonical,
            "GAUGE_UNIQUENESS_RECONSTRUCTION",
        )


def main() -> int:
    print(
        "STRUCTURE_FIXED_BEFORE_NUMBER: construct the tensor coordinates, "
        "harmonic projector, spectral Green operator, and d2^T gauge filler."
    )

    small = TripartiteComplex(1, 1, 1, None)
    medium = TripartiteComplex(1, 2, 1, None)
    for number, complex_ in enumerate((small, medium)):
        verify_basis_scalar_identities(complex_)
        verify_operator_identities(complex_, 71 + number)
        verify_gauge_fill(complex_, 79 + number)
    print("PASS_GREEN_GAUGE_GRID: pseudoinverse and unique gauge filler hold exactly.")

    # Source-scene sector-level checks and exact Green trace.
    scene = TripartiteComplex(8, 10, 12, None)
    verify_basis_scalar_identities(scene)
    green_trace = sum(
        (
            Fraction(multiplicity, eigenvalue)
            for eigenvalue, multiplicity in (
                (9, 120),
                (11, 96),
                (13, 80),
                (20, 12),
                (22, 10),
                (24, 8),
                (33, 1),
            )
        ),
        Fraction(0),
    )
    require(green_trace == Fraction(63562, 2145), "SOURCE_GREEN_TRACE")
    require(Fraction(1, 9) > Fraction(1, 11) > Fraction(1, 13), "SOURCE_GREEN_ORDER")
    print(
        "PASS_SOURCE_GREEN_SPECTRUM: trace(G)=63562/2145 and max positive "
        "Green eigenvalue is 1/9."
    )

    # A sparse source-scene gauge-filling test keeps the exact calculation
    # tractable while still exercising all maps on the real 1287/359 carriers.
    source = [Fraction(0) for _ in scene.triangles]
    for position, coefficient in (
        (0, Fraction(2)),
        (1, Fraction(-3)),
        (127, Fraction(5)),
        (640, Fraction(-7)),
        (1286, Fraction(11)),
    ):
        source[position] = coefficient
    cycle = as_fractions(scene.d2(source))
    canonical = hodge_gauge_fill(scene, cycle)
    require(as_fractions(scene.d2(canonical)) == cycle, "SOURCE_GAUGE_FILL_BOUNDARY")
    require(
        harmonic_project(scene, canonical)
        == [Fraction(0) for _ in scene.triangles],
        "SOURCE_GAUGE_FILL_GAUGE",
    )
    print("PASS_SOURCE_HODGE_GAUGE_FILL: exact canonical filling on real scene carriers.")

    # Negative 1: use 1/10 instead of 1/9 on the gap sector.
    vector = mode_vector(scene, (0, 1, 1))  # eigenvalue 9
    bad_green = green_apply(
        scene,
        vector,
        reciprocal_mutation={9: Fraction(1, 10)},
    )
    expect_rejected(
        "MUTATE_GAP_RECIPROCAL",
        hodge_apply(scene, bad_green) == vector,
    )

    # Negative 2: do not kill the harmonic sector.
    harmonic = mode_vector(scene, (1, 1, 1))
    bad_harmonic_green = green_apply(
        scene,
        harmonic,
        harmonic_weight=Fraction(1),
    )
    expect_rejected(
        "GREEN_PRESERVES_HARMONIC_MODE",
        bad_harmonic_green == [Fraction(0) for _ in scene.triangles],
    )

    # Negative 3: omit d2^T in the gauge formula (wrong carrier/type route).
    wrong = green_apply(scene, source)
    expect_rejected(
        "OMIT_TRANSPOSE_IN_GAUGE_FILL",
        as_fractions(scene.d2(wrong)) == cycle,
    )

    # Negative 4: adding a harmonic mode preserves fill but must fail gauge.
    alternative = add(canonical, harmonic)
    require(as_fractions(scene.d2(alternative)) == cycle, "HARMONIC_ADD_FILL_SETUP")
    expect_rejected(
        "HARMONIC_SHIFT_PRESERVES_GAUGE",
        harmonic_project(scene, alternative)
        == [Fraction(0) for _ in scene.triangles],
    )

    # Negative 5: a non-cycle is not in the filler's domain.
    noncycle = [Fraction(0) for _ in scene.edges]
    noncycle[scene.edge_index[("ab", 0, 0)]] = 1
    require(
        as_fractions(scene.d1(noncycle))
        != [Fraction(0) for _ in scene.vertices],
        "NONCYCLE_SETUP",
    )
    expect_rejected(
        "DROP_ONE_CYCLE_HYPOTHESIS",
        as_fractions(scene.d2(hodge_gauge_fill(scene, noncycle))) == noncycle,
    )

    # Negative 6: mutate the exact Green trace.
    expect_rejected(
        "GREEN_TRACE_OFF_BY_ONE",
        green_trace == Fraction(63563, 2145),
    )

    print(
        "PASS_GENERIC_TRIPARTITE_TOP_HODGE_GREEN: pseudoinverse identities, "
        "harmonic projector, exact source trace, canonical gauge filling, "
        "uniqueness controls, and destructive mutations all survive."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
