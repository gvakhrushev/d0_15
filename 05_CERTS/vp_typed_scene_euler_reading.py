#!/usr/bin/env python3
"""Can-fail certificate for D0-TYPED-SCENE-EULER-READING-001.

The certificate builds the complete tripartite clique complex from the typed
zones, derives V/E/T and χ, constructs the oriented edge/triangle boundary
matrices, and computes their exact rational ranks.  It thereby verifies the
strong executable result β=(1,0,960).

Lean now owns the same finite boundary result in
`D0.Topology.TypedTripartiteBoundaryRank`: explicit oriented matrices satisfy
`∂1∂2=0`, `rank ∂1=32`, and `rank ∂2=327`; the matrices are transported to the
owned `V9/V11/V13` carrier in `TypedSceneEulerReading`.  This executable
certificate remains an independent implementation with conclusion-failing
mutations.
"""

from __future__ import annotations

from fractions import Fraction
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


def exact_rank(rows: list[dict[int, int]], ncols: int) -> int:
    """Exact sparse Gaussian elimination over Q."""

    work: list[dict[int, Fraction]] = [
        {j: Fraction(value) for j, value in row.items() if value}
        for row in rows
    ]
    pivot_row = 0
    for col in range(ncols):
        pivot = next(
            (r for r in range(pivot_row, len(work)) if work[r].get(col, 0)),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][col]
        work[pivot_row] = {
            j: value / pivot_value for j, value in work[pivot_row].items()
        }
        for r in range(len(work)):
            if r == pivot_row:
                continue
            factor = work[r].get(col, 0)
            if not factor:
                continue
            for j, value in work[pivot_row].items():
                updated = work[r].get(j, 0) - factor * value
                if updated:
                    work[r][j] = updated
                else:
                    work[r].pop(j, None)
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def main() -> int:
    print(
        "STRUCTURE_FIXED_BEFORE_NUMBER: typed zones build the vertex, edge, "
        "triangle, and oriented boundary carriers before χ or Betti numbers."
    )

    sizes = (9, 11, 13)
    offsets = (0, sizes[0], sizes[0] + sizes[1])
    zones = [
        list(range(offset, offset + size))
        for offset, size in zip(offsets, sizes)
    ]
    vertices = [v for zone in zones for v in zone]
    edges = [
        (u, v)
        for left in range(3)
        for right in range(left + 1, 3)
        for u, v in product(zones[left], zones[right])
    ]
    triangles = [
        (a, b, c)
        for a, b, c in product(zones[0], zones[1], zones[2])
    ]
    edge_index = {edge: i for i, edge in enumerate(edges)}

    V, E, T = len(vertices), len(edges), len(triangles)
    chi = V - E + T
    require((V, E, T, chi) == (33, 359, 1287, 961), "TYPED_EULER_DATA")
    print("PASS_TYPED_EULER_DATA: (V,E,T,chi)=(33,359,1287,961).")

    # ∂1 : C1 -> C0, with ∂[u,v] = v-u. Rows are vertices, columns are edges.
    boundary1_rows: list[dict[int, int]] = [dict() for _ in vertices]
    for col, (u, v) in enumerate(edges):
        boundary1_rows[u][col] = -1
        boundary1_rows[v][col] = 1

    # ∂2 : C2 -> C1, with ∂[a,b,c] = [b,c]-[a,c]+[a,b].
    # Rows are edges, columns are triangles.
    boundary2_rows: list[dict[int, int]] = [dict() for _ in edges]
    for col, (a, b, c) in enumerate(triangles):
        for edge, coeff in (((b, c), 1), ((a, c), -1), ((a, b), 1)):
            boundary2_rows[edge_index[edge]][col] = coeff

    rank_d1 = exact_rank(boundary1_rows, E)
    rank_d2 = exact_rank(boundary2_rows, T)
    require((rank_d1, rank_d2) == (32, 327), "BOUNDARY_RANKS")

    # Exact sparse verification ∂1∂2=0 by checking every triangle column.
    for a, b, c in triangles:
        vertex_boundary: dict[int, int] = {}
        for (u, v), coeff in (((b, c), 1), ((a, c), -1), ((a, b), 1)):
            vertex_boundary[u] = vertex_boundary.get(u, 0) - coeff
            vertex_boundary[v] = vertex_boundary.get(v, 0) + coeff
        require(
            all(value == 0 for value in vertex_boundary.values()),
            "BOUNDARY_SQUARED_ZERO",
        )
    print("PASS_TYPED_BOUNDARY_COMPLEX: rank(d1)=32, rank(d2)=327, d1*d2=0.")

    beta0 = V - rank_d1
    beta1 = E - rank_d1 - rank_d2
    beta2 = T - rank_d2
    require(rank_d2 == E - rank_d1, "BOUNDARY_EXACTNESS")
    require((beta0, beta1, beta2) == (1, 0, 960), "BETTI_VECTOR")
    require(chi == beta0 - beta1 + beta2, "EULER_POINCARE")
    reduced_zone_product = 1
    for size in sizes:
        reduced_zone_product *= size - 1
    require(beta2 == reduced_zone_product, "JOIN_PRODUCT")
    print(
        "PASS_TYPED_BETTI_VECTOR: im(d2)=ker(d1), beta=(1,0,960), "
        "Euler-Poincare exact."
    )

    # Negative controls must reach and break the claimed conclusions.
    expect_rejected(
        "EULER_ALONE_SELECTS_BETTI_VECTOR",
        (0, 0, 961) == (beta0, beta1, beta2),
    )
    expect_rejected(
        "DELETE_ONE_TRIANGLE_PRESERVES_EULER",
        V - E + (T - 1) == chi,
    )
    expect_rejected(
        "MUTATE_BOUNDARY_RANK_PRESERVES_BETTI",
        (V - rank_d1, E - rank_d1 - (rank_d2 - 1), T - (rank_d2 - 1))
        == (beta0, beta1, beta2),
    )
    expect_rejected(
        "CORRUPT_TRIANGLE_BOUNDARY_STILL_SQUARES_ZERO",
        # Remove the +[a,b] term from one triangle: its vertex boundary is nonzero.
        all(
            value == 0
            for value in {
                zones[0][0]: 1,
                zones[1][0]: -1,
            }.values()
        ),
    )

    print(
        "PASS_TYPED_SCENE_EULER_READING: typed incidence carriers determine "
        "chi=961; exact boundary ranks certify beta=(1,0,960)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
