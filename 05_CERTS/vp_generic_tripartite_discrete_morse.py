#!/usr/bin/env python3
"""Can-fail certificate for the generic tripartite discrete Morse matching.

For the nonempty faces of K(p+1,q+1,r+1), independently verify the
root-lexicographic matching formalized in
`D0.Topology.GenericTripartiteDiscreteMorse`:

* typed faces equal the nonempty optional-zone face coordinates;
* every matched pair is a codimension-one inclusion;
* upper/lower maps are inverse and their roles are disjoint;
* the only critical faces are one root vertex and p*q*r all-nonroot triangles;
* every Forman V-path step strictly decreases an explicit rank, hence no
  directed cycle exists;
* total faces = critical faces + twice the number of matched pairs.

The certificate does not promote the still-missing realization theorem from
an acyclic matching to a topological wedge of spheres.
"""

from __future__ import annotations

from itertools import product
from typing import Callable, Optional


Face = tuple[object, ...]
PairUpper = Callable[[Face], Optional[Face]]
Rank = Callable[[Face], int]


def require(condition: bool, token: str) -> None:
    if not condition:
        raise AssertionError(f"FAIL_{token}")


def expect_rejected(token: str, action: Callable[[], None]) -> None:
    try:
        action()
    except AssertionError as exc:
        print(f"PASS_NEGATIVE_CONTROL_{token}: {exc}")
    else:
        raise AssertionError(f"FAIL_NEGATIVE_CONTROL_DID_NOT_FIRE_{token}")


def vertex(zone: int, index: int) -> Face:
    return ("v", zone, index)


def edge(kind: str, left: int, right: int) -> Face:
    return ("e", kind, left, right)


def triangle(a: int, b: int, c: int) -> Face:
    return ("t", a, b, c)


def typed_faces(p: int, q: int, r: int) -> list[Face]:
    require(min(p, q, r) >= 0, "NEGATIVE_OFFSET")
    vertices = (
        [vertex(0, a) for a in range(p + 1)]
        + [vertex(1, b) for b in range(q + 1)]
        + [vertex(2, c) for c in range(r + 1)]
    )
    edges = (
        [edge("ab", a, b) for a, b in product(range(p + 1), range(q + 1))]
        + [edge("ac", a, c) for a, c in product(range(p + 1), range(r + 1))]
        + [edge("bc", b, c) for b, c in product(range(q + 1), range(r + 1))]
    )
    triangles = [
        triangle(a, b, c)
        for a, b, c in product(range(p + 1), range(q + 1), range(r + 1))
    ]
    return vertices + edges + triangles


def face_vertices(face: Face) -> frozenset[tuple[int, int]]:
    if face[0] == "v":
        return frozenset({(int(face[1]), int(face[2]))})
    if face[0] == "e":
        kind, x, y = str(face[1]), int(face[2]), int(face[3])
        if kind == "ab":
            return frozenset({(0, x), (1, y)})
        if kind == "ac":
            return frozenset({(0, x), (2, y)})
        if kind == "bc":
            return frozenset({(1, x), (2, y)})
    if face[0] == "t":
        return frozenset({(0, int(face[1])), (1, int(face[2])), (2, int(face[3]))})
    raise AssertionError(f"FAIL_UNKNOWN_FACE_{face}")


def optional_zone_faces(p: int, q: int, r: int) -> set[frozenset[tuple[int, int]]]:
    options_a = [None, *range(p + 1)]
    options_b = [None, *range(q + 1)]
    options_c = [None, *range(r + 1)]
    out: set[frozenset[tuple[int, int]]] = set()
    for a, b, c in product(options_a, options_b, options_c):
        chosen = []
        if a is not None:
            chosen.append((0, a))
        if b is not None:
            chosen.append((1, b))
        if c is not None:
            chosen.append((2, c))
        if chosen:
            out.add(frozenset(chosen))
    return out


def pair_upper(face: Face) -> Face | None:
    if face[0] == "v":
        zone, index = int(face[1]), int(face[2])
        if zone == 0:
            return None if index == 0 else edge("ab", index, 0)
        if zone == 1:
            return edge("ab", 0, index)
        if zone == 2:
            return edge("ac", 0, index)
    if face[0] == "e":
        kind, x, y = str(face[1]), int(face[2]), int(face[3])
        if kind == "ab":
            return None if x == 0 or y == 0 else triangle(x, y, 0)
        if kind == "ac":
            return None if x == 0 else triangle(x, 0, y)
        if kind == "bc":
            return triangle(0, x, y)
    return None


def pair_lower(face: Face) -> Face | None:
    if face[0] == "e":
        kind, x, y = str(face[1]), int(face[2]), int(face[3])
        if kind == "ab":
            if x == 0:
                return vertex(1, y)
            if y == 0:
                return vertex(0, x)
            return None
        if kind == "ac":
            return vertex(2, y) if x == 0 else None
        return None
    if face[0] == "t":
        a, b, c = int(face[1]), int(face[2]), int(face[3])
        if a == 0:
            return edge("bc", b, c)
        if b == 0:
            return edge("ac", a, c)
        if c == 0:
            return edge("ab", a, b)
    return None


def codim_one_faces(face: Face) -> tuple[Face, ...]:
    if face[0] == "e":
        kind, x, y = str(face[1]), int(face[2]), int(face[3])
        if kind == "ab":
            return vertex(0, x), vertex(1, y)
        if kind == "ac":
            return vertex(0, x), vertex(2, y)
        return vertex(1, x), vertex(2, y)
    if face[0] == "t":
        a, b, c = int(face[1]), int(face[2]), int(face[3])
        return edge("ab", a, b), edge("ac", a, c), edge("bc", b, c)
    return ()


def gradient_rank(face: Face) -> int:
    if face[0] == "v":
        return 1 if int(face[1]) == 0 and int(face[2]) != 0 else 0
    if face[0] == "e":
        kind, x, y = str(face[1]), int(face[2]), int(face[3])
        if kind == "ab":
            return 2 if x != 0 and y != 0 else 0
        if kind == "ac":
            return 1 if x != 0 else 0
    return 0


def expected_critical(p: int, q: int, r: int) -> set[Face]:
    return {vertex(0, 0)} | {
        triangle(a, b, c)
        for a, b, c in product(range(1, p + 1), range(1, q + 1), range(1, r + 1))
    }


def verify_matching(
    p: int,
    q: int,
    r: int,
    upper_fn: PairUpper = pair_upper,
    rank_fn: Rank = gradient_rank,
    expected: set[Face] | None = None,
) -> None:
    faces = typed_faces(p, q, r)
    face_set = set(faces)
    require(len(faces) == len(face_set), f"TYPED_FACE_DUPLICATE_{p}_{q}_{r}")

    actual_finsets = {face_vertices(face) for face in faces}
    require(
        len(actual_finsets) == len(faces),
        f"TYPED_FACE_TO_FINSET_NOT_INJECTIVE_{p}_{q}_{r}",
    )
    require(
        actual_finsets == optional_zone_faces(p, q, r),
        f"ABSTRACT_FACE_EQUIVALENCE_{p}_{q}_{r}",
    )

    lower_faces: list[Face] = []
    upper_faces: list[Face] = []
    critical_faces: set[Face] = set()
    gradient_edges: list[tuple[Face, Face]] = []

    for face in faces:
        upper = upper_fn(face)
        lower = pair_lower(face)

        require(not (upper is not None and lower is not None), f"ROLE_OVERLAP_{face}")

        if upper is not None:
            lower_faces.append(face)
            require(upper in face_set, f"UPPER_OUTSIDE_COMPLEX_{face}")
            require(pair_lower(upper) == face, f"UPPER_LOWER_INVERSE_{face}")
            lower_vertices = face_vertices(face)
            upper_vertices = face_vertices(upper)
            require(lower_vertices < upper_vertices, f"NOT_CODIM_ONE_SUBSET_{face}")
            require(
                len(upper_vertices) == len(lower_vertices) + 1,
                f"NOT_CODIM_ONE_CARD_{face}",
            )
            for next_face in codim_one_faces(upper):
                if next_face != face and upper_fn(next_face) is not None:
                    gradient_edges.append((face, next_face))

        if lower is not None:
            upper_faces.append(face)
            require(upper_fn(lower) == face, f"LOWER_UPPER_INVERSE_{face}")

        if upper is None and lower is None:
            critical_faces.add(face)

    expected_faces = expected_critical(p, q, r) if expected is None else expected
    require(critical_faces == expected_faces, f"CRITICAL_SET_{p}_{q}_{r}")
    require(len(critical_faces) == 1 + p * q * r, f"CRITICAL_COUNT_{p}_{q}_{r}")
    require(
        sum(1 for face in critical_faces if face[0] == "v") == 1,
        f"CRITICAL_VERTEX_COUNT_{p}_{q}_{r}",
    )
    require(
        sum(1 for face in critical_faces if face[0] == "e") == 0,
        f"CRITICAL_EDGE_COUNT_{p}_{q}_{r}",
    )
    require(
        sum(1 for face in critical_faces if face[0] == "t") == p * q * r,
        f"CRITICAL_TRIANGLE_COUNT_{p}_{q}_{r}",
    )

    require(len(lower_faces) == len(upper_faces), f"PAIR_COUNT_SPLIT_{p}_{q}_{r}")
    require(len(set(lower_faces)) == len(lower_faces), f"LOWER_DUPLICATE_{p}_{q}_{r}")
    require(len(set(upper_faces)) == len(upper_faces), f"UPPER_DUPLICATE_{p}_{q}_{r}")
    require(
        len(faces) == len(critical_faces) + 2 * len(lower_faces),
        f"MORSE_FACE_BALANCE_{p}_{q}_{r}",
    )

    expected_edge_count = (
        (p + 1) * (q + 1)
        + (p + 1) * (r + 1)
        + (q + 1) * (r + 1)
    )
    require(len(lower_faces) == expected_edge_count, f"PAIR_COUNT_EDGE_{p}_{q}_{r}")

    adjacency: dict[Face, list[Face]] = {face: [] for face in lower_faces}
    for source, target in gradient_edges:
        require(
            rank_fn(target) < rank_fn(source),
            f"GRADIENT_RANK_{source}_{target}",
        )
        adjacency[source].append(target)

    state: dict[Face, int] = {}

    def visit(face: Face) -> None:
        mark = state.get(face, 0)
        require(mark != 1, f"GRADIENT_CYCLE_{face}")
        if mark == 2:
            return
        state[face] = 1
        for target in adjacency.get(face, []):
            visit(target)
        state[face] = 2

    for face in lower_faces:
        visit(face)


def main() -> int:
    print(
        "STRUCTURE_FIXED_BEFORE_TOPOLOGY: construct the actual face carrier and "
        "root-lexicographic matching before reading the critical count."
    )

    for p, q, r in product(range(4), repeat=3):
        verify_matching(p, q, r)
    print("PASS_EXHAUSTIVE_SMALL_MORSE_GRID: all offsets 0..3 satisfy the matching.")

    verify_matching(8, 10, 12)
    scene_faces = len(typed_faces(8, 10, 12))
    require(scene_faces == 1679, "SCENE_FACE_COUNT")
    require(1 + 8 * 10 * 12 == 961, "SCENE_CRITICAL_COUNT")
    print(
        "PASS_SOURCE_DISCRETE_MORSE: 1679 faces split into 359 matched pairs "
        "and 961 critical faces (1 vertex + 960 triangles)."
    )

    def root_corruption(face: Face) -> Face | None:
        if face == vertex(0, 0):
            return edge("ab", 0, 0)
        return pair_upper(face)

    expect_rejected(
        "ROOT_MUST_REMAIN_CRITICAL",
        lambda: verify_matching(1, 1, 1, upper_fn=root_corruption),
    )

    def bad_bc_upper(face: Face) -> Face | None:
        if face == edge("bc", 1, 1):
            return triangle(1, 1, 1)
        return pair_upper(face)

    expect_rejected(
        "BC_PAIR_MUST_USE_A_ROOT",
        lambda: verify_matching(1, 1, 1, upper_fn=bad_bc_upper),
    )

    def flat_rank(_face: Face) -> int:
        return 0

    expect_rejected(
        "GRADIENT_RANK_CANNOT_BE_FLAT",
        lambda: verify_matching(1, 1, 1, rank_fn=flat_rank),
    )

    missing_critical = expected_critical(1, 1, 1)
    missing_critical.remove(triangle(1, 1, 1))
    expect_rejected(
        "CRITICAL_TRIANGLE_CANNOT_BE_DROPPED",
        lambda: verify_matching(1, 1, 1, expected=missing_critical),
    )

    print(
        "PASS_GENERIC_TRIPARTITE_DISCRETE_MORSE: actual-face equivalence, "
        "proper matching, exact critical cells, and acyclicity all survive "
        "exhaustive, source-scene, and destructive tests."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
