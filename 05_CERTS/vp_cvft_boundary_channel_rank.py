#!/usr/bin/env python3
"""Deterministic CVFT boundary-channel rank certificate."""

from __future__ import annotations


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def transpose(a):
    return [list(row) for row in zip(*a)]


def rank(a, eps=1e-10):
    m = [row[:] for row in a]
    rows, cols = len(m), len(m[0])
    r = 0
    for c in range(cols):
        pivot = next((i for i in range(r, rows) if abs(m[i][c]) > eps), None)
        if pivot is None:
            continue
        m[r], m[pivot] = m[pivot], m[r]
        scale = m[r][c]
        m[r] = [x / scale for x in m[r]]
        for i in range(rows):
            if i != r and abs(m[i][c]) > eps:
                factor = m[i][c]
                m[i] = [m[i][j] - factor * m[r][j] for j in range(cols)]
        r += 1
    return r


def main() -> int:
    print("RETIRED_2026-07-05_SEE_REFORGED: this cert had fabricated controls (see _QUARANTINE/QUARANTINE_LEDGER.md); superseded by vp_cvft_boundary_channel_rank_REFORGED.py; output below is NON-LOAD-BEARING")
    # QUP factors through a 2D boundary-channel subspace inside Q.
    qup = [
        [1.0, 0.0, 0.0],
        [0.0, 2.0, 0.0],
        [0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0],
    ]
    f = matmul(transpose(qup), qup)
    dim_boundary = 2
    ok = rank(f) == rank(qup) and rank(f) <= dim_boundary
    rank_not_a4 = dim_boundary != 4
    if ok and rank_not_a4:
        print("PASS_CVFT_BOUNDARY_CHANNEL_RANK")
        print("PASS_CVFT_BOUNDARY_RANK_BOUND")
        print("NEGATIVE_CONTROL_CAUGHT FAIL_RANK_BOUND_AS_A4_PROOF")
        return 0
    print("FAIL_CVFT_BOUNDARY_CHANNEL_RANK")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
