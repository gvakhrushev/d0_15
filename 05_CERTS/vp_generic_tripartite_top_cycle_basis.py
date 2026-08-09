#!/usr/bin/env python3
"""Can-fail certificate for D0-GENERIC-TRIPARTITE-TOP-CYCLE-BASIS-001.

For `K(p+1,q+1,r+1)`, construct the octahedral top cycles

    (e_(i+1)-e_0) tensor (e_(j+1)-e_0) tensor (e_(k+1)-e_0)

indexed by `0<=i<p`, `0<=j<q`, `0<=k<r`.  Check exact boundary cancellation,
the identity coordinate matrix on all-nonroot triangles, linear independence,
and equality of the basis count with the full top-kernel dimension `p*q*r`.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product
from typing import Iterable


SparseVector = dict[int, int]


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


def exact_rank(rows: Iterable[SparseVector], ncols: int) -> int:
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


def complex_data(
    p: int, q: int, r: int
) -> tuple[
    list[tuple[str, int, int]],
    list[tuple[int, int, int]],
    dict[tuple[str, int, int], int],
    dict[tuple[int, int, int], int],
]:
    require(min(p, q, r) >= 0, "NEGATIVE_OFFSET")
    edges = (
        [("ab", a, b) for a, b in product(range(p + 1), range(q + 1))]
        + [("ac", a, c) for a, c in product(range(p + 1), range(r + 1))]
        + [("bc", b, c) for b, c in product(range(q + 1), range(r + 1))]
    )
    triangles = list(product(range(p + 1), range(q + 1), range(r + 1)))
    return (
        edges,
        triangles,
        {edge: i for i, edge in enumerate(edges)},
        {triangle: i for i, triangle in enumerate(triangles)},
    )


def root_difference(index: int, vertex: int) -> int:
    if vertex == index + 1:
        return 1
    if vertex == 0:
        return -1
    return 0


def octahedral_cycle(
    i: int,
    j: int,
    k: int,
    triangles: list[tuple[int, int, int]],
) -> SparseVector:
    return {
        col: value
        for col, (a, b, c) in enumerate(triangles)
        if (
            value := (
                root_difference(i, a)
                * root_difference(j, b)
                * root_difference(k, c)
            )
        )
    }


def triangle_boundary(
    triangle: tuple[int, int, int],
    edge_index: dict[tuple[str, int, int], int],
) -> SparseVector:
    a, b, c = triangle
    return {
        edge_index[("bc", b, c)]: 1,
        edge_index[("ac", a, c)]: -1,
        edge_index[("ab", a, b)]: 1,
    }


def boundary_of_chain(
    chain: SparseVector,
    triangles: list[tuple[int, int, int]],
    edge_index: dict[tuple[str, int, int], int],
) -> SparseVector:
    out: SparseVector = {}
    for triangle_col, triangle_coeff in chain.items():
        for edge, boundary_coeff in triangle_boundary(
            triangles[triangle_col], edge_index
        ).items():
            updated = out.get(edge, 0) + triangle_coeff * boundary_coeff
            if updated:
                out[edge] = updated
            else:
                out.pop(edge, None)
    return out


def d2_rows(
    edges: list[tuple[str, int, int]],
    triangles: list[tuple[int, int, int]],
    edge_index: dict[tuple[str, int, int], int],
) -> list[SparseVector]:
    rows: list[SparseVector] = [dict() for _ in edges]
    for col, triangle in enumerate(triangles):
        for edge, value in triangle_boundary(triangle, edge_index).items():
            rows[edge][col] = value
    return rows


def add_scaled(target: SparseVector, source: SparseVector, scalar: int) -> None:
    for index, value in source.items():
        updated = target.get(index, 0) + scalar * value
        if updated:
            target[index] = updated
        else:
            target.pop(index, None)


def verify_case(p: int, q: int, r: int, compute_rank: bool = True) -> None:
    edges, triangles, edge_index, triangle_index = complex_data(p, q, r)
    indices = list(product(range(p), range(q), range(r)))
    cycles = {
        index: octahedral_cycle(*index, triangles)
        for index in indices
    }

    for index, cycle in cycles.items():
        require(
            boundary_of_chain(cycle, triangles, edge_index) == {},
            f"OCTAHEDRAL_BOUNDARY_{p}_{q}_{r}_{index}",
        )
        require(
            set(cycle.values()) <= {-1, 1},
            f"OCTAHEDRAL_COEFFICIENTS_{p}_{q}_{r}_{index}",
        )
        require(
            len(cycle) == 8,
            f"OCTAHEDRAL_SUPPORT_{p}_{q}_{r}_{index}",
        )

    # The all-nonroot triangle coordinates form the identity matrix.
    for row_index in indices:
        coordinate = triangle_index[
            (row_index[0] + 1, row_index[1] + 1, row_index[2] + 1)
        ]
        for col_index in indices:
            require(
                cycles[col_index].get(coordinate, 0)
                == int(row_index == col_index),
                f"IDENTITY_COORDINATE_{p}_{q}_{r}_{row_index}_{col_index}",
            )

    require(len(cycles) == p * q * r, f"BASIS_COUNT_{p}_{q}_{r}")
    if compute_rank:
        rank_d2 = exact_rank(d2_rows(edges, triangles, edge_index), len(triangles))
        kernel_dim = len(triangles) - rank_d2
        require(kernel_dim == p * q * r, f"KERNEL_DIMENSION_{p}_{q}_{r}")
        require(len(cycles) == kernel_dim, f"BASIS_COMPLETE_{p}_{q}_{r}")

    # Exact reconstruction on a deterministic nontrivial linear combination.
    coefficients = {
        index: (index[0] + 1) - 2 * (index[1] + 1) + 3 * (index[2] + 1)
        for index in indices
    }
    chain: SparseVector = {}
    for index, coefficient in coefficients.items():
        add_scaled(chain, cycles[index], coefficient)
    require(
        boundary_of_chain(chain, triangles, edge_index) == {},
        f"COMBINATION_BOUNDARY_{p}_{q}_{r}",
    )
    recovered = {
        index: chain.get(
            triangle_index[(index[0] + 1, index[1] + 1, index[2] + 1)],
            0,
        )
        for index in indices
    }
    require(recovered == coefficients, f"COORDINATE_RECONSTRUCTION_{p}_{q}_{r}")


def main() -> int:
    print(
        "STRUCTURE_FIXED_BEFORE_NUMBER: choose roots, construct reduced "
        "coordinate tensors, then test boundaries and coordinates."
    )

    # Nonempty basis cases, including thin directions.
    for p, q, r in product(range(1, 4), repeat=3):
        verify_case(p, q, r)
    # Degenerate offsets have zero top cycles and zero top-kernel dimension.
    for case in ((0, 0, 0), (0, 2, 3), (2, 0, 3), (2, 3, 0)):
        verify_case(*case)
    print(
        "PASS_TOP_CYCLE_GRID: octahedral cycles are a complete basis on "
        "27 positive and 4 zero-offset control cases."
    )

    # The full D0 scene: check all 960 cycles and the identity coordinates.
    verify_case(8, 10, 12, compute_rank=False)
    require(8 * 10 * 12 == 960, "SOURCE_BASIS_COUNT")
    print(
        "PASS_SOURCE_TOP_CYCLE_BASIS: the scene has 960 explicit "
        "eight-triangle octahedral basis cycles."
    )

    # Destructive control 1: flip one coefficient; edge cancellation must fail.
    edges, triangles, edge_index, triangle_index = complex_data(2, 2, 2)
    good = octahedral_cycle(0, 0, 0, triangles)
    corrupted = dict(good)
    first_triangle = next(iter(corrupted))
    corrupted[first_triangle] *= -1
    expect_rejected(
        "CORRUPT_OCTAHEDRAL_SIGN_STILL_CYCLE",
        boundary_of_chain(corrupted, triangles, edge_index) == {},
    )

    # Destructive control 2: duplicate one family element; identity coordinates fail.
    indices = list(product(range(2), repeat=3))
    cycles = {index: octahedral_cycle(*index, triangles) for index in indices}
    duplicated = dict(cycles)
    duplicated[indices[-1]] = duplicated[indices[0]]
    identity_ok = all(
        duplicated[col_index].get(
            triangle_index[
                (row_index[0] + 1, row_index[1] + 1, row_index[2] + 1)
            ],
            0,
        )
        == int(row_index == col_index)
        for row_index in indices
        for col_index in indices
    )
    expect_rejected("DUPLICATE_BASIS_PRESERVES_IDENTITY", identity_ok)

    # Destructive control 3: remove one cycle; the family no longer has kernel size.
    rank_d2 = exact_rank(d2_rows(edges, triangles, edge_index), len(triangles))
    kernel_dim = len(triangles) - rank_d2
    expect_rejected(
        "DELETE_BASIS_VECTOR_PRESERVES_COMPLETENESS",
        len(indices) - 1 == kernel_dim,
    )

    # Destructive control 4: read one coefficient at the root triangle instead.
    coefficients = {index: index[0] + 2 * index[1] + 3 * index[2] + 1 for index in indices}
    chain: SparseVector = {}
    for index, coefficient in coefficients.items():
        add_scaled(chain, cycles[index], coefficient)
    wrong_recovered = {
        index: chain.get(triangle_index[(0, index[1] + 1, index[2] + 1)], 0)
        for index in indices
    }
    expect_rejected(
        "ROOT_COORDINATE_PRESERVES_RECONSTRUCTION",
        wrong_recovered == coefficients,
    )

    print(
        "PASS_GENERIC_TRIPARTITE_TOP_CYCLE_BASIS: explicit octahedral cycles "
        "give computable coordinates for every rational top class."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
