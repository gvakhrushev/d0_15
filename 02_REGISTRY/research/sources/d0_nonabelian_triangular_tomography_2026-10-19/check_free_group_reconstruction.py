#!/usr/bin/env python3
"""Exact free-group check of the 327-triangle nonabelian reconstruction."""

from __future__ import annotations


def mul(*words: tuple[int, ...]) -> tuple[int, ...]:
    out: list[int] = []
    for word in words:
        for letter in word:
            if out and out[-1] == -letter:
                out.pop()
            else:
                out.append(letter)
    return tuple(out)


def inv(word: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(-letter for letter in reversed(word))


def put(edges: dict[tuple[int, int], tuple[int, ...]], u: int, v: int,
        value: tuple[int, ...]) -> None:
    assert u < v
    edges[(u, v)] = value


def get(edges: dict[tuple[int, int], tuple[int, ...]], u: int,
        v: int) -> tuple[int, ...]:
    return edges[(u, v)] if u < v else inv(edges[(v, u)])


def face(edges: dict[tuple[int, int], tuple[int, ...]], i: int, j: int,
         k: int) -> tuple[int, ...]:
    a, b, c = i, 9 + j, 20 + k
    return mul(get(edges, a, b), get(edges, b, c), get(edges, c, a))


def main() -> None:
    identity: tuple[int, ...] = ()
    tree = {
        *((0, 9 + j) for j in range(11)),
        *((0, 20 + k) for k in range(13)),
        *((i, 9) for i in range(1, 9)),
    }
    assert len(tree) == 32

    # A free generator labels each non-tree edge, so reductions below are
    # identities in the free group and hence hold in every group.
    source: dict[tuple[int, int], tuple[int, ...]] = {
        edge: identity for edge in tree
    }
    generator = 1
    for i in range(9):
        for j in range(11):
            edge = (i, 9 + j)
            if edge not in tree:
                source[edge] = (generator,)
                generator += 1
    for i in range(9):
        for k in range(13):
            edge = (i, 20 + k)
            if edge not in tree:
                source[edge] = (generator,)
                generator += 1
    for j in range(11):
        for k in range(13):
            edge = (9 + j, 20 + k)
            source[edge] = (generator,)
            generator += 1
    assert generator - 1 == 327
    assert len(source) == 359

    recovered: dict[tuple[int, int], tuple[int, ...]] = {
        edge: identity for edge in tree
    }

    # 11*13 = 143 triangles recover all B-C links.
    for j in range(11):
        for k in range(13):
            put(recovered, 9 + j, 20 + k, face(source, 0, j, k))

    # 8*13 = 104 triangles recover the remaining A-C links.
    for i in range(1, 9):
        for k in range(13):
            put(recovered, i, 20 + k,
                mul(inv(face(source, i, 0, k)), get(recovered, 9, 20 + k)))

    # 8*10 = 80 triangles recover the remaining A-B links.
    for i in range(1, 9):
        for j in range(1, 11):
            put(recovered, i, 9 + j,
                mul(face(source, i, j, 0), get(recovered, i, 20),
                    inv(get(recovered, 9 + j, 20))))

    assert len(recovered) == 359
    recovered_edges = sum(
        get(recovered, u, v) == get(source, u, v)
        for u, v in source
    )
    assert recovered_edges == 359

    # Every one of the 960 omitted faces has the same ordered seven-factor
    # expression in the 327 reference faces.
    omitted_faces = 0
    for i in range(1, 9):
        for j in range(1, 11):
            for k in range(1, 13):
                rhs = mul(
                    face(source, i, j, 0),
                    inv(face(source, i, 0, 0)),
                    face(source, 0, 0, 0),
                    inv(face(source, 0, j, 0)),
                    face(source, 0, j, k),
                    inv(face(source, 0, 0, k)),
                    face(source, i, 0, k),
                )
                assert face(source, i, j, k) == rhs
                assert face(recovered, i, j, k) == rhs
                omitted_faces += 1
    assert omitted_faces == 960

    print({
        "status": "PASS_EXACT_FREE_GROUP_TRIANGLE_RECONSTRUCTION",
        "tree_edges": len(tree),
        "independent_oriented_triangles": 327,
        "reconstructed_directed_edge_pairs": recovered_edges,
        "ordered_omitted_face_identities": omitted_faces,
        "ambient_group": "arbitrary group; SO(1,3) is a specialization",
        "physical_D0_admission_proved": False,
        "native_Book_price_proved": False,
        "GR_closed": False,
    })


if __name__ == "__main__":
    main()
