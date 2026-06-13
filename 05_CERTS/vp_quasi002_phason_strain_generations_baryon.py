#!/usr/bin/env python3
"""D0-QUASI-002 phason-strain generations / baryon S3 certificate."""

from __future__ import annotations

import json
from fractions import Fraction
from itertools import permutations
from pathlib import Path


PASS_TOKEN = "PASS_QUASI002_PHASON_STRAIN_GENERATIONS_BARYON"


def mat_zero(rows: int, cols: int | None = None) -> list[list[Fraction]]:
    width = rows if cols is None else cols
    return [[Fraction(0, 1) for _ in range(width)] for _ in range(rows)]


def mat_mul(a: list[list[Fraction]], b: list[list[Fraction]]) -> list[list[Fraction]]:
    rows = len(a)
    inner = len(a[0]) if rows else 0
    cols = len(b[0]) if b else 0
    if len(b) != inner:
        raise ValueError(f"matrix shape mismatch: {rows}x{inner} times {len(b)}x{cols}")
    out = mat_zero(rows, cols)
    for i in range(rows):
        for k in range(cols):
            value = Fraction(0, 1)
            for j in range(inner):
                value += a[i][j] * b[j][k]
            out[i][k] = value
    return out


def mat_eq(a: list[list[Fraction]], b: list[list[Fraction]]) -> bool:
    if len(a) != len(b):
        return False
    if a and b and len(a[0]) != len(b[0]):
        return False
    return all(a[i][j] == b[i][j] for i in range(len(a)) for j in range(len(a[0])))


def mat_add_inplace(a: list[list[Fraction]], b: list[list[Fraction]]) -> None:
    for i in range(len(a)):
        for j in range(len(a)):
            a[i][j] += b[i][j]


def rank(matrix: list[list[Fraction]]) -> int:
    a = [row[:] for row in matrix]
    rows = len(a)
    cols = len(a[0]) if rows else 0
    r = 0
    for c in range(cols):
        pivot = None
        for i in range(r, rows):
            if a[i][c] != 0:
                pivot = i
                break
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        pivot_value = a[r][c]
        a[r] = [x / pivot_value for x in a[r]]
        for i in range(rows):
            if i == r or a[i][c] == 0:
                continue
            factor = a[i][c]
            a[i] = [a[i][j] - factor * a[r][j] for j in range(cols)]
        r += 1
        if r == rows:
            break
    return r


def inverse_perm(p: tuple[int, int, int]) -> tuple[int, int, int]:
    inv = [0, 0, 0]
    for i, image in enumerate(p):
        inv[image] = i
    return tuple(inv)


def act(p: tuple[int, int, int], t: tuple[int, int, int]) -> tuple[int, int, int]:
    inv = inverse_perm(p)
    return tuple(t[inv[i]] for i in range(3))


def permutation_matrix(
    p: tuple[int, int, int],
    triples: list[tuple[int, int, int]],
    index: dict[tuple[int, int, int], int],
) -> list[list[Fraction]]:
    n = len(triples)
    mat = mat_zero(n)
    for col, triple in enumerate(triples):
        row = index[act(p, triple)]
        mat[row][col] = Fraction(1, 1)
    return mat


def main() -> dict:
    phason_modes = list(range(3))
    triples = [(a, b, c) for a in phason_modes for b in phason_modes for c in phason_modes]
    index = {triple: i for i, triple in enumerate(triples)}
    s3 = list(permutations(range(3)))
    rho = {p: permutation_matrix(p, triples, index) for p in s3}

    pi_sym = mat_zero(len(triples))
    for mat in rho.values():
        mat_add_inplace(pi_sym, mat)
    for i in range(len(pi_sym)):
        for j in range(len(pi_sym)):
            pi_sym[i][j] /= len(s3)

    pi_square = mat_mul(pi_sym, pi_sym)
    left_invariance = all(mat_eq(mat_mul(rho[p], pi_sym), pi_sym) for p in s3)
    right_invariance = all(mat_eq(mat_mul(pi_sym, rho[p]), pi_sym) for p in s3)
    sorted_representatives = sorted({tuple(sorted(t)) for t in triples})

    nucleon_line_basis = [(0, 0, 0), (1, 1, 1), (2, 2, 2)]
    projected_line = []
    for triple in nucleon_line_basis:
        vec = [[Fraction(0, 1)] for _ in triples]
        vec[index[triple]][0] = Fraction(1, 1)
        projected_line.append([row[0] for row in mat_mul(pi_sym, vec)])
    projected_line_rank = rank(projected_line)

    checks = {
        "phason_mode_count_eq_3": len(phason_modes) == 3,
        "triple_carrier_eq_27": len(triples) == 27,
        "s3_order_eq_6": len(s3) == 6,
        "pi_sym_idempotent": mat_eq(pi_square, pi_sym),
        "pi_sym_rank_eq_10": rank(pi_sym) == 10,
        "pi_sym_left_invariant": left_invariance,
        "pi_sym_right_invariant": right_invariance,
        "sorted_symmetric_sector_eq_10": len(sorted_representatives) == 10,
        "nucleon_line_does_not_span_decuplet": projected_line_rank < 10,
    }

    result = {
        "status": PASS_TOKEN if all(checks.values()) else "FAIL",
        "phason_modes": len(phason_modes),
        "ordered_triples": len(triples),
        "s3_order": len(s3),
        "rank_pi_sym": rank(pi_sym),
        "symmetric_sector_representatives": ["".join(map(str, t)) for t in sorted_representatives],
        "nucleon_line_projected_rank": projected_line_rank,
        "checks": checks,
    }
    return result


if __name__ == "__main__":
    out = main()
    here = Path(__file__).resolve().parent
    (here / "vp_quasi002_phason_strain_generations_baryon_results.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(out["status"])
    for name, ok in out["checks"].items():
        print(f"{name}: {ok}")
    if out["status"] != PASS_TOKEN:
        raise SystemExit(1)
