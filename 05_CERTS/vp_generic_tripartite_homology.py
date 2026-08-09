#!/usr/bin/env python3
"""Can-fail certificate for D0-GENERIC-TRIPARTITE-HOMOLOGY-001.

For the canonical complete-tripartite clique complex with zone sizes
`(p+1,q+1,r+1)`, independently construct the rational boundary matrices and
check

    rank d1 = p+q+r+2,
    rank d2 = pq+pr+qr+p+q+r+1,
    im d2 = ker d1,
    beta = (1,0,pqr),
    chi = 1+pqr.

The grid includes zero offsets.  Destructive controls corrupt a boundary
sign, delete a column of the explicit full-rank minor, mutate the d2 rank, and
move beta2 off by one.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product
from typing import Iterable


SparseRow = dict[int, int]


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


def exact_rank(rows: Iterable[SparseRow], ncols: int) -> int:
    """Exact sparse Gaussian elimination over Q."""

    work: list[dict[int, Fraction]] = [
        {j: Fraction(value) for j, value in row.items() if value}
        for row in rows
    ]
    pivot_row = 0
    for col in range(ncols):
        pivot = next(
            (i for i in range(pivot_row, len(work)) if work[i].get(col, 0)),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][col]
        work[pivot_row] = {
            j: value / pivot_value for j, value in work[pivot_row].items()
        }
        for i in range(len(work)):
            if i == pivot_row:
                continue
            factor = work[i].get(col, 0)
            if not factor:
                continue
            for j, value in work[pivot_row].items():
                updated = work[i].get(j, 0) - factor * value
                if updated:
                    work[i][j] = updated
                else:
                    work[i].pop(j, None)
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def build_complex(
    p: int, q: int, r: int
) -> tuple[
    list[tuple[int, int]],
    list[tuple[str, int, int]],
    list[tuple[int, int, int]],
    list[SparseRow],
    list[SparseRow],
    list[SparseRow],
]:
    """Return vertices, edges, triangles, d1 rows, d1 cols, and d2 cols."""

    require(min(p, q, r) >= 0, "NEGATIVE_OFFSET")
    vertices = (
        [(0, a) for a in range(p + 1)]
        + [(1, b) for b in range(q + 1)]
        + [(2, c) for c in range(r + 1)]
    )
    vertex_index = {vertex: i for i, vertex in enumerate(vertices)}
    edges = (
        [("ab", a, b) for a, b in product(range(p + 1), range(q + 1))]
        + [("ac", a, c) for a, c in product(range(p + 1), range(r + 1))]
        + [("bc", b, c) for b, c in product(range(q + 1), range(r + 1))]
    )
    edge_index = {edge: i for i, edge in enumerate(edges)}
    triangles = list(product(range(p + 1), range(q + 1), range(r + 1)))

    d1_rows: list[SparseRow] = [dict() for _ in vertices]
    d1_cols: list[SparseRow] = []
    for col, (kind, left, right) in enumerate(edges):
        if kind == "ab":
            source, target = (0, left), (1, right)
        elif kind == "ac":
            source, target = (0, left), (2, right)
        else:
            source, target = (1, left), (2, right)
        source_i, target_i = vertex_index[source], vertex_index[target]
        d1_rows[source_i][col] = -1
        d1_rows[target_i][col] = 1
        d1_cols.append({source_i: -1, target_i: 1})

    d2_cols: list[SparseRow] = []
    for a, b, c in triangles:
        d2_cols.append(
            {
                edge_index[("bc", b, c)]: 1,
                edge_index[("ac", a, c)]: -1,
                edge_index[("ab", a, b)]: 1,
            }
        )

    return vertices, edges, triangles, d1_rows, d1_cols, d2_cols


def rows_from_cols(columns: list[SparseRow], nrows: int) -> list[SparseRow]:
    rows: list[SparseRow] = [dict() for _ in range(nrows)]
    for col, entries in enumerate(columns):
        for row, value in entries.items():
            rows[row][col] = value
    return rows


def boundary_squared_zero(
    d1_cols: list[SparseRow], d2_cols: list[SparseRow]
) -> bool:
    for triangle_boundary in d2_cols:
        vertex_boundary: dict[int, int] = {}
        for edge, edge_coeff in triangle_boundary.items():
            for vertex, vertex_coeff in d1_cols[edge].items():
                value = vertex_boundary.get(vertex, 0) + edge_coeff * vertex_coeff
                if value:
                    vertex_boundary[vertex] = value
                else:
                    vertex_boundary.pop(vertex, None)
        if vertex_boundary:
            return False
    return True


def selected_minor(
    p: int,
    q: int,
    r: int,
    edges: list[tuple[str, int, int]],
    triangles: list[tuple[int, int, int]],
    d2_cols: list[SparseRow],
) -> list[SparseRow]:
    """The same non-tree-edge/selected-triangle minor used by the Lean proof."""

    selected_rows = (
        [("ab", a + 1, b) for a, b in product(range(p), range(q + 1))]
        + [("ac", a, c + 1) for a, c in product(range(p + 1), range(r))]
        + [("bc", b, 0) for b in range(q + 1)]
        + [("bc", b + 1, c + 1) for b, c in product(range(q), range(r))]
    )
    selected_cols = (
        [(a + 1, b, 0) for a, b in product(range(p), range(q + 1))]
        + [(a, 0, c + 1) for a, c in product(range(p + 1), range(r))]
        + [(0, b, 0) for b in range(q + 1)]
        + [(0, b + 1, c + 1) for b, c in product(range(q), range(r))]
    )
    edge_index = {edge: i for i, edge in enumerate(edges)}
    triangle_index = {triangle: i for i, triangle in enumerate(triangles)}
    row_position = {edge_index[edge]: i for i, edge in enumerate(selected_rows)}
    minor_rows: list[SparseRow] = [dict() for _ in selected_rows]
    for minor_col, triangle in enumerate(selected_cols):
        for edge, value in d2_cols[triangle_index[triangle]].items():
            if edge in row_position:
                minor_rows[row_position[edge]][minor_col] = value
    require(
        len(selected_rows) == len(selected_cols),
        f"MINOR_NOT_SQUARE_{p}_{q}_{r}",
    )
    return minor_rows


def verify_case(p: int, q: int, r: int, check_minor: bool = True) -> None:
    vertices, edges, triangles, d1_rows, d1_cols, d2_cols = build_complex(p, q, r)
    d2_rows = rows_from_cols(d2_cols, len(edges))

    vertices_expected = p + q + r + 3
    edges_expected = (
        (p + 1) * (q + 1)
        + (p + 1) * (r + 1)
        + (q + 1) * (r + 1)
    )
    triangles_expected = (p + 1) * (q + 1) * (r + 1)
    rank1_expected = p + q + r + 2
    rank2_expected = p * q + p * r + q * r + p + q + r + 1

    require(
        (len(vertices), len(edges), len(triangles))
        == (vertices_expected, edges_expected, triangles_expected),
        f"FACE_COUNTS_{p}_{q}_{r}",
    )
    require(boundary_squared_zero(d1_cols, d2_cols), f"D1_D2_{p}_{q}_{r}")
    rank1 = exact_rank(d1_rows, len(edges))
    rank2 = exact_rank(d2_rows, len(triangles))
    require(rank1 == rank1_expected, f"RANK_D1_{p}_{q}_{r}")
    require(rank2 == rank2_expected, f"RANK_D2_{p}_{q}_{r}")
    require(rank2 == len(edges) - rank1, f"EXACTNESS_{p}_{q}_{r}")

    beta = (
        len(vertices) - rank1,
        len(edges) - rank1 - rank2,
        len(triangles) - rank2,
    )
    require(beta == (1, 0, p * q * r), f"BETTI_{p}_{q}_{r}")
    chi = len(vertices) - len(edges) + len(triangles)
    require(chi == 1 + p * q * r, f"EULER_{p}_{q}_{r}")
    require(chi == beta[0] - beta[1] + beta[2], f"EULER_POINCARE_{p}_{q}_{r}")

    if check_minor:
        minor_rows = selected_minor(p, q, r, edges, triangles, d2_cols)
        require(
            exact_rank(minor_rows, len(minor_rows)) == rank2_expected,
            f"SELECTED_MINOR_{p}_{q}_{r}",
        )


def main() -> int:
    print(
        "STRUCTURE_FIXED_BEFORE_NUMBER: construct canonical vertices, edges, "
        "triangles, d1, d2, and the selected minor before reading ranks."
    )

    grid = list(product(range(4), repeat=3))
    for p, q, r in grid:
        verify_case(p, q, r)
    print(
        "PASS_GENERIC_GRID: 64 cases with 0<=p,q,r<=3 satisfy exactness, "
        "beta=(1,0,pqr), and chi=1+pqr."
    )

    # Full source-scene matrices, independent of the pre-existing typed cert.
    verify_case(8, 10, 12)
    print(
        "PASS_SOURCE_SPECIALIZATION: (p,q,r)=(8,10,12) gives "
        "rank(d1,d2)=(32,327), beta2=960, chi=961."
    )

    # Destructive control 1: reverse only the AB sign in one triangle.
    _, _, _, _, d1_cols, d2_cols = build_complex(1, 1, 1)
    corrupted = [dict(column) for column in d2_cols]
    first_ab_edge = next(edge for edge, value in corrupted[0].items() if value == 1)
    corrupted[0][first_ab_edge] = -1
    expect_rejected(
        "CORRUPT_TRIANGLE_SIGN_STILL_SQUARES_ZERO",
        boundary_squared_zero(d1_cols, corrupted),
    )

    # Destructive control 2: the Lean-selected square minor is invertible;
    # deleting one selected triangle column must destroy full rank.
    _, edges, triangles, _, _, d2_cols = build_complex(2, 2, 2)
    minor_rows = selected_minor(2, 2, 2, edges, triangles, d2_cols)
    full_minor_rank = exact_rank(minor_rows, len(minor_rows))
    deleted_column_rows = [
        {col: value for col, value in row.items() if col != 0}
        for row in minor_rows
    ]
    expect_rejected(
        "DELETE_SELECTED_TRIANGLE_PRESERVES_MINOR_RANK",
        exact_rank(deleted_column_rows, len(minor_rows)) == full_minor_rank,
    )

    # Destructive controls 3/4: arithmetic conclusions must not survive a
    # rank mutation or an off-by-one top Betti value.
    p, q, r = 2, 3, 4
    _, edges, triangles, d1_rows, _, d2_cols = build_complex(p, q, r)
    rank1 = exact_rank(d1_rows, len(edges))
    rank2 = exact_rank(rows_from_cols(d2_cols, len(edges)), len(triangles))
    expect_rejected(
        "MUTATE_D2_RANK_PRESERVES_EXACTNESS",
        rank2 - 1 == len(edges) - rank1,
    )
    beta2 = len(triangles) - rank2
    expect_rejected(
        "BETA2_OFF_BY_ONE",
        beta2 == p * q * r + 1,
    )

    print(
        "PASS_GENERIC_TRIPARTITE_HOMOLOGY: the parameteric rational homology "
        "formula survives the grid, source specialization, and destructive controls."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
