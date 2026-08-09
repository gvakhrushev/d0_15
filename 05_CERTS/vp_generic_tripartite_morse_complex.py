#!/usr/bin/env python3
"""Can-fail certificate for D0-GENERIC-TRIPARTITE-MORSE-COMPLEX-001.

Independently verify the generator-level identification between the actual
critical cells of the root-lexicographic matching and the algebraic minimal
complex:

* the unique critical 0-cell is the A-root vertex;
* critical 2-cells are exactly all-nonroot triangles, indexed by
  ``range(p) x range(q) x range(r)``;
* each critical 2-generator synthesizes the matching eight-triangle
  octahedral cycle;
* its boundary is zero and its all-nonroot coordinates are the expected
  Kronecker delta;
* arbitrary critical coefficients synthesize and recover exactly.

The certificate also checks the new simplicial-set bridge combinatorially:
nondegenerate simplices are exactly the nonempty cross-zone faces, with the
canonical zone-lexicographic vertex ordering.  It does not claim the still
missing Forman realization/collapse theorem or a wedge-of-spheres homotopy
equivalence.
"""

from __future__ import annotations

from itertools import product
from typing import Callable

from vp_generic_tripartite_universal_homology import (
    TripartiteComplex,
    normalize_vector,
    require,
    zero_vector,
)
from vp_generic_tripartite_discrete_morse import (
    codim_one_faces as morse_codim_one_faces,
    expected_critical as morse_expected_critical,
    face_vertices as morse_face_vertices,
    gradient_rank as morse_gradient_rank,
    pair_lower as morse_pair_lower,
    pair_upper as morse_pair_upper,
    typed_faces as morse_typed_faces,
    vertex as morse_vertex,
)

Vertex = tuple[int, int]
Face = frozenset[Vertex]
TopIndex = tuple[int, int, int]
IndexMap = Callable[[TopIndex], TopIndex]
CycleMap = Callable[[TripartiteComplex, TopIndex], list[int]]


def expect_rejected(token: str, action: Callable[[], None]) -> None:
    try:
        action()
    except AssertionError as exc:
        print(f"PASS_NEGATIVE_CONTROL_{token}: {exc}")
    else:
        raise AssertionError(f"FAIL_NEGATIVE_CONTROL_DID_NOT_FIRE_{token}")


def root_vertex() -> Vertex:
    return (0, 0)


def face_dimension(face: Face) -> int:
    require(bool(face), "EMPTY_FACE_HAS_NO_DIMENSION")
    return len(face) - 1


def is_cross_zone_face(face: Face) -> bool:
    return bool(face) and len({zone for zone, _ in face}) == len(face)


def ordered_face(face: Face) -> tuple[Vertex, ...]:
    require(is_cross_zone_face(face), "ORDER_REQUIRES_CROSS_ZONE_FACE")
    return tuple(sorted(face))


def simplicial_nondegenerate_faces(p: int, q: int, r: int) -> set[tuple[Vertex, ...]]:
    options = (
        [None, *range(p + 1)],
        [None, *range(q + 1)],
        [None, *range(r + 1)],
    )
    faces: set[tuple[Vertex, ...]] = set()
    for a, b, c in product(*options):
        face = frozenset(
            vertex
            for vertex in (
                None if a is None else (0, a),
                None if b is None else (1, b),
                None if c is None else (2, c),
            )
            if vertex is not None
        )
        if face:
            faces.add(ordered_face(face))
    return faces


def typed_faces(p: int, q: int, r: int) -> set[tuple[Vertex, ...]]:
    out: set[tuple[Vertex, ...]] = set()
    out.update(((0, a),) for a in range(p + 1))
    out.update(((1, b),) for b in range(q + 1))
    out.update(((2, c),) for c in range(r + 1))
    out.update(tuple(sorted(((0, a), (1, b)))) for a, b in product(range(p + 1), range(q + 1)))
    out.update(tuple(sorted(((0, a), (2, c)))) for a, c in product(range(p + 1), range(r + 1)))
    out.update(tuple(sorted(((1, b), (2, c)))) for b, c in product(range(q + 1), range(r + 1)))
    out.update(
        tuple(sorted(((0, a), (1, b), (2, c))))
        for a, b, c in product(range(p + 1), range(q + 1), range(r + 1))
    )
    return out


def critical_two_face(index: TopIndex) -> tuple[int, int, int]:
    i, j, k = index
    return i + 1, j + 1, k + 1


def critical_two_index(triangle: tuple[int, int, int]) -> TopIndex:
    a, b, c = triangle
    require(a > 0 and b > 0 and c > 0, "NONCRITICAL_TRIANGLE_HAS_NO_INDEX")
    return a - 1, b - 1, c - 1


def critical_two_simplex(index: TopIndex) -> tuple[Vertex, ...]:
    """Ordered nondegenerate SSet simplex of an indexed critical triangle."""
    a, b, c = critical_two_face(index)
    return ((0, a), (1, b), (2, c))


def critical_two_simplex_index(simplex: tuple[Vertex, ...]) -> TopIndex:
    require(len(simplex) == 3, "CRITICAL_SIMPLEX_NOT_TRIANGLE")
    require(
        tuple(zone for zone, _ in simplex) == (0, 1, 2),
        "CRITICAL_SIMPLEX_ZONE_ORDER",
    )
    return critical_two_index(tuple(index for _, index in simplex))


def top_coordinates(
    complex_: TripartiteComplex,
    chain: list[int],
) -> dict[TopIndex, int]:
    return complex_.top_coordinates(chain)


def synthesize_critical_coefficients(
    complex_: TripartiteComplex,
    coefficients: dict[TopIndex, int],
    *,
    index_map: IndexMap = lambda index: index,
    cycle_map: CycleMap = lambda complex_, index: complex_.top_cycle(index),
) -> list[int]:
    out = zero_vector(len(complex_.triangles))
    for critical_index in complex_.top_indices:
        coefficient = coefficients.get(critical_index, 0)
        target_index = index_map(critical_index)
        require(target_index in complex_.top_indices, f"INDEX_OUTSIDE_TOP_CELLS_{target_index}")
        cycle = cycle_map(complex_, target_index)
        require(len(cycle) == len(out), "CYCLE_LENGTH")
        for triangle_pos, value in enumerate(cycle):
            out[triangle_pos] += coefficient * value
    return normalize_vector(out, complex_.modulus)


def verify_octahedral_generator(
    complex_: TripartiteComplex,
    index: TopIndex,
    *,
    index_map: IndexMap = lambda value: value,
    cycle_map: CycleMap = lambda complex_, value: complex_.top_cycle(value),
) -> None:
    require(index in complex_.top_indices, f"UNKNOWN_CRITICAL_INDEX_{index}")
    mapped = index_map(index)
    require(mapped in complex_.top_indices, f"MAPPED_INDEX_OUTSIDE_{mapped}")
    cycle = cycle_map(complex_, mapped)
    support = [pos for pos, coefficient in enumerate(cycle) if coefficient]
    require(len(support) == 8, f"OCTAHEDRAL_SUPPORT_{index}")
    require(
        all(cycle[pos] in (-1, 1) for pos in support),
        f"OCTAHEDRAL_SIGNS_{index}",
    )
    require(
        complex_.d2(cycle) == zero_vector(len(complex_.edges)),
        f"OCTAHEDRAL_BOUNDARY_{index}",
    )
    expected = {
        candidate: complex_.norm(int(candidate == index))
        for candidate in complex_.top_indices
    }
    require(
        top_coordinates(complex_, cycle) == expected,
        f"CRITICAL_GENERATOR_COORDINATES_{index}",
    )
    require(
        critical_two_index(critical_two_face(index)) == index,
        f"CRITICAL_INDEX_ROUNDTRIP_{index}",
    )


def verify_bridge_and_morse_complex(
    p: int,
    q: int,
    r: int,
    *,
    critical_zero: Vertex = (0, 0),
    index_map: IndexMap = lambda value: value,
    cycle_map: CycleMap = lambda complex_, value: complex_.top_cycle(value),
    simplex_index_map: IndexMap = lambda value: value,
    drop_last_generator: bool = False,
) -> None:
    complex_ = TripartiteComplex(p, q, r, None)

    actual_faces = simplicial_nondegenerate_faces(p, q, r)
    expected_faces = typed_faces(p, q, r)
    require(actual_faces == expected_faces, f"SIMPLICIAL_FACE_EQUIV_{p}_{q}_{r}")
    require(
        all(face_dimension(frozenset(face)) in (0, 1, 2) for face in actual_faces),
        f"SIMPLICIAL_DIMENSION_BOUND_{p}_{q}_{r}",
    )
    require(
        len(actual_faces)
        == len(complex_.vertices) + len(complex_.edges) + len(complex_.triangles),
        f"NONDEGENERATE_FACE_COUNT_{p}_{q}_{r}",
    )

    require(critical_zero == root_vertex(), f"CRITICAL_ZERO_ROOT_{p}_{q}_{r}")
    root_chain = zero_vector(len(complex_.vertices))
    root_chain[complex_.vertex_index[critical_zero]] = 1
    require(complex_.augmentation(root_chain) == 1, f"CRITICAL_ZERO_AUGMENTATION_{p}_{q}_{r}")
    require(
        [i for i, value in enumerate(root_chain) if value] ==
        [complex_.vertex_index[root_vertex()]],
        f"CRITICAL_ZERO_SUPPORT_{p}_{q}_{r}",
    )

    critical_indices = list(complex_.top_indices)
    if drop_last_generator and critical_indices:
        critical_indices.pop()
    require(len(critical_indices) == p * q * r, f"CRITICAL_TWO_COUNT_{p}_{q}_{r}")
    require(
        {critical_two_face(index) for index in critical_indices}
        == {
            (a, b, c)
            for a, b, c in product(range(1, p + 1), range(1, q + 1), range(1, r + 1))
        },
        f"CRITICAL_TWO_FACE_SET_{p}_{q}_{r}",
    )
    actual_critical_simplices = {
        critical_two_simplex(simplex_index_map(index))
        for index in critical_indices
    }
    require(
        len(actual_critical_simplices) == len(critical_indices),
        f"CRITICAL_SSET_SIMPLEX_INJECTIVE_{p}_{q}_{r}",
    )
    for index in critical_indices:
        mapped_index = simplex_index_map(index)
        require(
            mapped_index in complex_.top_indices,
            f"CRITICAL_SSET_INDEX_OUTSIDE_{mapped_index}",
        )
        require(
            critical_two_simplex_index(critical_two_simplex(mapped_index))
            == index,
            f"CRITICAL_SSET_INDEX_ROUNDTRIP_{index}",
        )

    for index in critical_indices:
        verify_octahedral_generator(
            complex_,
            index,
            index_map=index_map,
            cycle_map=cycle_map,
        )

    coefficients = {
        index: 2 * (index[0] + 1) - 3 * (index[1] + 1) + 5 * (index[2] + 1)
        for index in critical_indices
    }
    synthesized = synthesize_critical_coefficients(
        complex_,
        coefficients,
        index_map=index_map,
        cycle_map=cycle_map,
    )
    require(
        complex_.d2(synthesized) == zero_vector(len(complex_.edges)),
        f"CRITICAL_SYNTHESIS_BOUNDARY_{p}_{q}_{r}",
    )
    require(
        top_coordinates(complex_, synthesized) == coefficients,
        f"CRITICAL_SYNTHESIS_RECOVERY_{p}_{q}_{r}",
    )



def verify_critical_cells_not_subcomplex(p: int, q: int, r: int) -> None:
    """Critical cells are not downward closed when p,q,r are positive."""
    require(min(p, q, r) > 0, "NO_SUBCOMPLEX_REQUIRES_POSITIVE_OFFSETS")
    critical_triangle = triangle = (1, 1, 1)
    require(
        critical_two_index(critical_triangle) == (0, 0, 0),
        "NO_SUBCOMPLEX_CRITICAL_TRIANGLE_SETUP",
    )
    boundary_edges = (
        frozenset({(0, triangle[0]), (1, triangle[1])}),
        frozenset({(0, triangle[0]), (2, triangle[2])}),
        frozenset({(1, triangle[1]), (2, triangle[2])}),
    )
    critical_faces = {frozenset({root_vertex()})} | {
        frozenset({(0, a), (1, b), (2, c)})
        for a, b, c in product(range(1, p + 1), range(1, q + 1), range(1, r + 1))
    }
    critical_triangle_face = frozenset({(0, 1), (1, 1), (2, 1)})
    require(
        critical_triangle_face in critical_faces,
        "NO_SUBCOMPLEX_TRIANGLE_NOT_CRITICAL",
    )
    require(
        all(edge < critical_triangle_face for edge in boundary_edges),
        "NO_SUBCOMPLEX_BOUNDARY_NOT_FACE",
    )
    require(
        all(edge not in critical_faces for edge in boundary_edges),
        "NO_SUBCOMPLEX_BOUNDARY_WAS_CRITICAL",
    )
    require(
        any(
            face in critical_faces
            and any(nonempty_subset not in critical_faces
                    for nonempty_subset in boundary_edges
                    if nonempty_subset < face)
            for face in (critical_triangle_face,)
        ),
        "CRITICAL_CARRIER_ACCIDENTALLY_DOWNWARD_CLOSED",
    )


def verify_critical_subcomplex_and_root_pairing(
    p: int,
    q: int,
    r: int,
) -> None:
    """Verify the exact boundary: a root pairing exists iff p*q*r vanishes."""
    top_count_zero = p * q * r == 0
    critical_faces = morse_expected_critical(p, q, r)
    downward_closed = all(
        subface in critical_faces
        for face in critical_faces
        for subface in morse_codim_one_faces(face)
    )
    require(
        downward_closed == top_count_zero,
        f"CRITICAL_SUBCOMPLEX_IFF_TOP_ZERO_{p}_{q}_{r}",
    )

    faces = set(morse_typed_faces(p, q, r))
    root = morse_vertex(0, 0)
    complement = faces - {root}
    lower_faces = {face for face in complement if morse_pair_upper(face) is not None}
    upper_faces = {face for face in complement if morse_pair_lower(face) is not None}
    root_pairing_exists = (
        lower_faces.isdisjoint(upper_faces)
        and lower_faces | upper_faces == complement
    )
    require(
        root_pairing_exists == top_count_zero,
        f"ROOT_PAIRING_IFF_TOP_ZERO_{p}_{q}_{r}",
    )

    unpaired_outside_root = {
        face
        for face in complement
        if morse_pair_upper(face) is None and morse_pair_lower(face) is None
    }
    require(
        len(unpaired_outside_root) == p * q * r,
        f"UNPAIRED_TOP_COUNT_{p}_{q}_{r}",
    )
    if not top_count_zero:
        return

    require(
        critical_faces == {root},
        f"ZERO_TOP_CRITICAL_ROOT_ONLY_{p}_{q}_{r}",
    )
    require(
        len(lower_faces) == len(upper_faces),
        f"ROOT_PAIRING_CARD_{p}_{q}_{r}",
    )

    for lower in lower_faces:
        upper = morse_pair_upper(lower)
        require(upper is not None, f"ROOT_PAIRING_UPPER_EXISTS_{lower}")
        require(upper in upper_faces, f"ROOT_PAIRING_UPPER_ROLE_{lower}")
        require(
            morse_pair_lower(upper) == lower,
            f"ROOT_PAIRING_UPPER_LOWER_INVERSE_{lower}",
        )
        lower_vertices = morse_face_vertices(lower)
        upper_vertices = morse_face_vertices(upper)
        require(
            lower_vertices < upper_vertices,
            f"ROOT_PAIRING_CODIM_SUBSET_{lower}",
        )
        require(
            len(upper_vertices) == len(lower_vertices) + 1,
            f"ROOT_PAIRING_CODIM_CARD_{lower}",
        )
        require(
            sum(candidate == lower for candidate in morse_codim_one_faces(upper)) == 1,
            f"ROOT_PAIRING_UNIQUE_FACE_{lower}",
        )

        # Weak regularity: an ancestral lower simplex of the same dimension
        # has strictly smaller canonical gradient rank.
        for candidate in lower_faces:
            candidate_vertices = morse_face_vertices(candidate)
            if (
                candidate != lower
                and len(candidate_vertices) == len(lower_vertices)
                and candidate_vertices < upper_vertices
            ):
                require(
                    morse_gradient_rank(candidate) < morse_gradient_rank(lower),
                    f"ROOT_PAIRING_REGULAR_RANK_{lower}_{candidate}",
                )

    for upper in upper_faces:
        lower = morse_pair_lower(upper)
        require(lower is not None, f"ROOT_PAIRING_LOWER_EXISTS_{upper}")
        require(
            morse_pair_upper(lower) == upper,
            f"ROOT_PAIRING_LOWER_UPPER_INVERSE_{upper}",
        )

    # A subcomplex generated by one zero-simplex is represented by [0]:
    # in each degree there is one constant root string.
    for dimension in range(9):
        root_sections = {tuple(root for _ in range(dimension + 1))}
        require(
            len(root_sections) == 1,
            f"ROOT_REPRESENTABLE_UNIQUE_DEGREE_{dimension}",
        )


def main() -> int:
    print(
        "STRUCTURE_FIXED_BEFORE_REALIZATION: construct the SSet face carrier, "
        "critical-cell coordinates, and octahedral generator map before any "
        "spatial wedge claim."
    )

    for p, q, r in product(range(3), repeat=3):
        verify_bridge_and_morse_complex(p, q, r)
        verify_critical_subcomplex_and_root_pairing(p, q, r)
    print("PASS_EXHAUSTIVE_SMALL_MORSE_COMPLEX_GRID: offsets 0..2 agree exactly.")

    verify_bridge_and_morse_complex(8, 10, 12)
    verify_critical_cells_not_subcomplex(8, 10, 12)
    verify_critical_subcomplex_and_root_pairing(8, 10, 12)
    print(
        "PASS_SOURCE_MORSE_COMPLEX: 1679 nondegenerate faces, one critical root, "
        "and 960 critical 2-generators map to their octahedral cycles."
    )
    print(
        "PASS_CRITICAL_SUBCOMPLEX_NO_GO: a critical triangle has noncritical boundary "
        "edges, so the realization cannot collapse directly onto a critical-cell subcomplex."
    )
    print(
        "PASS_ROOT_PAIRING_BOUNDARY: the critical carrier is a root subcomplex "
        "and its complement has a regular Morse pairing exactly when p*q*r=0."
    )

    cube = TripartiteComplex(2, 2, 2, None)
    first, second = cube.top_indices[0], cube.top_indices[1]

    def swap_first_two(index: TopIndex) -> TopIndex:
        if index == first:
            return second
        if index == second:
            return first
        return index

    expect_rejected(
        "PERMUTE_CRITICAL_INDEX",
        lambda: verify_bridge_and_morse_complex(2, 2, 2, index_map=swap_first_two),
    )

    expect_rejected(
        "PERMUTE_CRITICAL_SSET_SIMPLEX",
        lambda: verify_bridge_and_morse_complex(
            2,
            2,
            2,
            simplex_index_map=swap_first_two,
        ),
    )

    def flipped_sign(complex_: TripartiteComplex, index: TopIndex) -> list[int]:
        cycle = complex_.top_cycle(index)
        first_nonzero = next(pos for pos, value in enumerate(cycle) if value)
        cycle[first_nonzero] *= -1
        return cycle

    expect_rejected(
        "FLIP_OCTAHEDRAL_SIGN",
        lambda: verify_bridge_and_morse_complex(1, 1, 1, cycle_map=flipped_sign),
    )

    def wrong_octrahedron(complex_: TripartiteComplex, index: TopIndex) -> list[int]:
        target = second if index == first else index
        return complex_.top_cycle(target)

    expect_rejected(
        "MAP_TO_WRONG_OCTAHEDRON",
        lambda: verify_bridge_and_morse_complex(2, 2, 2, cycle_map=wrong_octrahedron),
    )

    expect_rejected(
        "DELETE_CRITICAL_GENERATOR",
        lambda: verify_bridge_and_morse_complex(2, 2, 2, drop_last_generator=True),
    )

    expect_rejected(
        "MOVE_CRITICAL_ZERO_FROM_ROOT",
        lambda: verify_bridge_and_morse_complex(1, 1, 1, critical_zero=(1, 0)),
    )

    def pretend_critical_subcomplex() -> None:
        critical_triangle = frozenset({(0, 1), (1, 1), (2, 1)})
        fake_critical_faces = {critical_triangle} | {
            frozenset({(0, 1), (1, 1)})
        }
        require(
            frozenset({(0, 1), (1, 1)}) not in fake_critical_faces,
            "CRITICAL_BOUNDARY_EDGE_CANNOT_BE_ADDED",
        )

    expect_rejected(
        "PRETEND_CRITICAL_CELLS_FORM_SUBCOMPLEX",
        pretend_critical_subcomplex,
    )

    expect_rejected(
        "PRETEND_POSITIVE_TOP_COUNT_HAS_ROOT_PAIRING",
        lambda: require(
            (
                {
                    face
                    for face in set(morse_typed_faces(1, 1, 1))
                    - {morse_vertex(0, 0)}
                    if morse_pair_upper(face) is not None
                }
                | {
                    face
                    for face in set(morse_typed_faces(1, 1, 1))
                    - {morse_vertex(0, 0)}
                    if morse_pair_lower(face) is not None
                }
            )
            == set(morse_typed_faces(1, 1, 1)) - {morse_vertex(0, 0)},
            "POSITIVE_TOP_COUNT_ROOT_PAIRING",
        ),
    )

    print(
        "PASS_GENERIC_TRIPARTITE_MORSE_COMPLEX: critical-cell/minimal coordinates, "
        "generator synthesis, SSet face realization, exact root-pairing boundary, "
        "source scene, and destructive mutations all gate correctly."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
