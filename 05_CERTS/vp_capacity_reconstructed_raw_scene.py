#!/usr/bin/env python3
"""Finite certificate for D0-CAPACITY-RECONSTRUCTED-RAW-SCENE-001.

The old raw self-reading graph starts from thresholds 9 and 20. This certificate
derives those thresholds from the upstream finite capacity chain:

    Dyad=2, ABCD=4, Omega8=8, V9=9, V11=11, qT=44.

The pair (ABCD,qT) reconstructs center=11 and spread=2, hence sizes 9/11/13
and cumulative cuts 9/20. The resulting label and adjacency are compared
entry-by-entry with the canonical raw graph, after which the raw invariants
2|E|=718, trace(A^2)=718, and pair-orbit commutant dimension 12 are recomputed.

Honest scope: finite complete-tripartite graph provenance only. No physical
spacetime identification or empirical anisotropy claim is made.
"""

from __future__ import annotations

from itertools import product
from math import lcm


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


def labels_from_cuts(n: int, cut1: int, cut2: int) -> list[int]:
    return [0 if i < cut1 else 1 if i < cut2 else 2 for i in range(n)]


def adjacency(labels: list[int]) -> list[list[int]]:
    return [
        [0 if labels[i] == labels[j] else 1 for j in range(len(labels))]
        for i in range(len(labels))
    ]


def main() -> int:
    print(
        "STRUCTURE_FIXED_BEFORE_NUMBER: capacity types construct center/spread "
        "and cuts before raw labels, adjacency, or graph invariants are read."
    )

    dyad = 2
    abcd = dyad**2
    omega8 = 2 * abcd
    v9 = omega8 + 1
    v11 = v9 + dyad
    q_t = lcm(abcd, v11)

    # Reverse reconstruction from the capacity-defect pair.
    solutions = [
        (m, d)
        for m in range(1, 100)
        for d in range(0, m + 1)
        if d**2 == abcd and m * d**2 == q_t
    ]
    require(solutions == [(11, 2)], f"CENTER_SPREAD_SOLUTIONS_{solutions}")
    center, spread = solutions[0]
    sizes = (center - spread, center, center + spread)
    cut1 = sizes[0]
    cut2 = sizes[0] + sizes[1]
    total = sum(sizes)
    require((sizes, cut1, cut2, total) == ((9, 11, 13), 9, 20, 33), "CAPACITY_CUTS")
    print(
        f"PASS_CAPACITY_RECONSTRUCTS_CUTS: sizes={sizes}, cuts=({cut1},{cut2}), "
        f"total={total}."
    )

    capacity_labels = labels_from_cuts(total, cut1, cut2)
    raw_labels = labels_from_cuts(33, 9, 20)
    require(capacity_labels == raw_labels, "LABEL_FUNCTION_MISMATCH")
    print("PASS_CAPACITY_LABEL_EQUALS_RAW_LABEL: all 33 vertex labels agree.")

    capacity_adj = adjacency(capacity_labels)
    raw_adj = adjacency(raw_labels)
    require(capacity_adj == raw_adj, "ADJACENCY_FUNCTION_MISMATCH")
    print("PASS_CAPACITY_ADJ_EQUALS_RAW_ADJ: all 1089 matrix entries agree.")

    degrees = [sum(row) for row in capacity_adj]
    require(degrees == [24] * 9 + [22] * 11 + [20] * 13, f"DEGREES_{degrees}")
    two_edges = sum(degrees)
    trace_a2 = sum(
        capacity_adj[i][k] * capacity_adj[k][i]
        for i in range(total)
        for k in range(total)
    )
    pair_classes = {
        (capacity_labels[i], capacity_labels[j], i == j)
        for i, j in product(range(total), repeat=2)
    }
    require(two_edges == 718, f"TWO_EDGES_{two_edges}")
    require(trace_a2 == 718, f"TRACE_A2_{trace_a2}")
    require(len(pair_classes) == 12, f"PAIR_ORBITS_{len(pair_classes)}")
    print(
        "PASS_CAPACITY_RAW_INVARIANTS: degree profile 24^9/22^11/20^13, "
        "2|E|=718, trace(A^2)=718, pair-orbit commutant=12."
    )

    # Reachable controls that fail the actual graph reconstruction.
    wrong_center_sizes = (10 - spread, 10, 10 + spread)
    wrong_center_labels = labels_from_cuts(sum(wrong_center_sizes), 8, 18)
    expect_rejected(
        "WRONG_CENTER_RECONSTRUCTS_RAW_GRAPH",
        wrong_center_labels == raw_labels,
    )
    wrong_spread_sizes = (center - 1, center, center + 1)
    wrong_spread_labels = labels_from_cuts(sum(wrong_spread_sizes), 10, 21)
    expect_rejected(
        "WRONG_SPREAD_RECONSTRUCTS_RAW_GRAPH",
        wrong_spread_labels == raw_labels,
    )
    shifted_labels = labels_from_cuts(33, 10, 20)
    expect_rejected(
        "SHIFTED_FIRST_CUT_PRESERVES_ADJACENCY",
        adjacency(shifted_labels) == raw_adj,
    )

    print(
        "PASS_CAPACITY_RECONSTRUCTED_RAW_SCENE: upstream (ABCD,qT) capacities "
        "recover the raw partition thresholds, adjacency, and self-reading invariants."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
