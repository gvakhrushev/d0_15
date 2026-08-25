#!/usr/bin/env python3
"""Finite certificate for D0-TYPED-CAPACITY-RAW-SCENE-001.

Build a tagged carrier directly as

    V9 ⊔ V11 ⊔ V13

without starting from integer cut predicates. The constructor tag is the zone.
The certificate derives the complete-tripartite adjacency and raw self-reading
invariants, then constructs a block-preserving bijection to the canonical
`Fin 33` representation and checks labels/adjacency entrywise.

Honest scope: the order chosen inside each finite zone is representation gauge.
Only zone tags, cardinalities, and invariant graph content are claimed.
"""

from __future__ import annotations

from itertools import product


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


def adjacency(labels: list[int]) -> list[list[int]]:
    return [
        [0 if labels[i] == labels[j] else 1 for j in range(len(labels))]
        for i in range(len(labels))
    ]


def main() -> int:
    print(
        "STRUCTURE_FIXED_BEFORE_NUMBER: tagged V9/V11/V13 carrier is built "
        "before any Fin33 representation or numeric cut is introduced."
    )

    sizes = {"V9": 9, "V11": 11, "V13": 13}
    typed_vertices = [
        (tag, local)
        for tag in ("V9", "V11", "V13")
        for local in range(sizes[tag])
    ]
    typed_zone = {"V9": 0, "V11": 1, "V13": 2}
    labels = [typed_zone[tag] for tag, _ in typed_vertices]
    typed_adj = adjacency(labels)

    require(len(typed_vertices) == 33, "TYPED_CARDINALITY")
    degrees = [sum(row) for row in typed_adj]
    require(degrees == [24] * 9 + [22] * 11 + [20] * 13, "TYPED_DEGREES")
    require(sum(degrees) == 718, "TYPED_TWO_EDGES")
    trace_a2 = sum(
        typed_adj[i][k] * typed_adj[k][i]
        for i in range(33)
        for k in range(33)
    )
    require(trace_a2 == 718, "TYPED_TRACE_A2")
    pair_classes = {
        (labels[i], labels[j], i == j)
        for i, j in product(range(33), repeat=2)
    }
    require(len(pair_classes) == 12, "TYPED_PAIR_ORBITS")
    print(
        "PASS_TYPED_RAW_INVARIANTS: |V|=33, degrees 24^9/22^11/20^13, "
        "2|E|=trace(A^2)=718, pair-orbit commutant=12."
    )

    # Block-preserving representation in Fin33.
    offsets = {
        "V9": 0,
        "V11": sizes["V9"],
        "V13": sizes["V9"] + sizes["V11"],
    }
    to_raw = {
        vertex: offsets[vertex[0]] + vertex[1]
        for vertex in typed_vertices
    }
    require(set(to_raw.values()) == set(range(33)), "REPRESENTATION_NOT_BIJECTIVE")

    raw_labels = [0 if i < 9 else 1 if i < 20 else 2 for i in range(33)]
    require(
        all(raw_labels[to_raw[v]] == typed_zone[v[0]] for v in typed_vertices),
        "LABEL_NOT_PRESERVED",
    )
    raw_adj = adjacency(raw_labels)
    require(
        all(
            raw_adj[to_raw[v]][to_raw[w]]
            == typed_adj[i][j]
            for i, v in enumerate(typed_vertices)
            for j, w in enumerate(typed_vertices)
        ),
        "ADJACENCY_NOT_PRESERVED",
    )
    print(
        "PASS_BLOCK_PRESERVING_EQUIVALENCE: typed carrier bijects to Fin33 "
        "and preserves all 33 labels and 1089 adjacency entries."
    )

    # Within-zone renamings are gauge: reverse each local enumeration.
    renamed_vertices = [
        (tag, sizes[tag] - 1 - local)
        for tag, local in typed_vertices
    ]
    renamed_labels = [typed_zone[tag] for tag, _ in renamed_vertices]
    require(adjacency(renamed_labels) == typed_adj, "WITHIN_ZONE_GAUGE_CHANGED_GRAPH")
    print("PASS_WITHIN_ZONE_RENAMING_GAUGE: local reversals leave adjacency unchanged.")

    # Reachable conclusion-failing controls.
    wrong_labels = labels.copy()
    wrong_labels[0] = 1
    expect_rejected(
        "MOVE_VERTEX_ACROSS_ZONE_PRESERVES_GRAPH",
        adjacency(wrong_labels) == typed_adj,
    )
    wrong_offsets = {"V9": 0, "V11": 10, "V13": 20}
    expect_rejected(
        "WRONG_OFFSETS_FORM_BIJECTION",
        len({
            wrong_offsets[tag] + local
            for tag, local in typed_vertices
        }) == 33,
    )
    expect_rejected(
        "DELETE_OUTER_VERTEX_PRESERVES_CARDINALITY",
        len(typed_vertices[:-1]) == 33,
    )

    print(
        "PASS_TYPED_CAPACITY_RAW_SCENE: raw self-reading graph is constructed "
        "on V9⊔V11⊔V13 before its Fin33 representation."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
