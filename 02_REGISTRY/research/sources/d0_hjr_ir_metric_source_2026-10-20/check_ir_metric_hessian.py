#!/usr/bin/env python3
"""Rigorous rational homogeneous HJR metric Hessian vs vacuum Palatini.

READ ONLY: consumes the already accepted original full-CAR16/full-site/RIGHT128
q=0 Arb symbol; does not solve the spectral problem or promote GR.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from fractions import Fraction as F
from pathlib import Path

SOURCE = (
    "02_REGISTRY/research/sources/d0_curved_whole_hjr_collar_2026-10-20/"
    "COLLAR_HESSIAN_ARB.json"
)
SOURCE_SHA = "a38386a86af4be283631d42a890caf66c035c12a4f9d421037160550d36989f4"
NUM = r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?"
BALL = re.compile(r"^\[\s*(?:(" + NUM + r")\s+)?\+/-\s*(" + NUM + r")\s*\]$")
PI = (0, 2, 3)         # true non-Lorentz homogeneous metric tangents
JI = (4, 5, 6, 7, 8)   # S4 observer-relative coframe + four proper link families
MICRO = F(1, 10**6)


def ball(s: str) -> tuple[F, F]:
    m = BALL.fullmatch(s)
    if m is None:
        raise ValueError(f"Expected REAL Arb q=0 interval: {s!r}")
    center, radius = F(m.group(1) or "0"), F(m.group(2))
    assert radius >= 0
    return center, radius


def inverse_exact(a: list[list[F]]) -> list[list[F]]:
    n = len(a)
    m = [
        list(row) + [F(i == k) for k in range(n)]
        for i, row in enumerate(a)
    ]
    for k in range(n):
        pivot_row = max(range(k, n), key=lambda i: abs(m[i][k]))
        assert m[pivot_row][k] != 0, f"noninvertible rational midpoint at {k}"
        m[k], m[pivot_row] = m[pivot_row], m[k]
        pivot = m[k][k]
        m[k] = [entry / pivot for entry in m[k]]
        for i in range(n):
            if i != k:
                q = m[i][k]
                m[i] = [m[i][j] - q * m[k][j] for j in range(2 * n)]
    inv = [row[n:] for row in m]
    assert matmul(a, inv) == [[F(i == j) for j in range(n)] for i in range(n)]
    return inv


def transpose(a: list[list[F]]) -> list[list[F]]:
    return [list(row) for row in zip(*a)]


def matmul(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    bt = transpose(b)
    return [[sum((x * y for x, y in zip(row, col)), F(0)) for col in bt] for row in a]


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[4])
    a = p.parse_args()
    raw = (a.root / SOURCE).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == SOURCE_SHA, "INPUT HASH CHANGED"
    j = json.loads(raw)
    assert j["status"] == "RIGOROUS_ARB_PASS" and j["L"] == 8
    assert j["all_momenta"] == 4096 and j["fullCAR"] == 16
    assert j["fixedRIGHT"] == 128
    assert len(j["K9"]) >= 1

    intervals = [[ball(s) for s in row] for row in j["K9"][0]]
    assert len(intervals) == 9 and all(len(row) == 9 for row in intervals)

    # Symmetric exact Hessian is in both interval enclosures of each ij,ji;
    # their rational-averaged centers still enclose it with averaged radii.
    centers = [
        [(intervals[i][k][0] + intervals[k][i][0]) / 2 for k in range(9)]
        for i in range(9)
    ]
    radii = [
        [(intervals[i][k][1] + intervals[k][i][1]) / 2 for k in range(9)]
        for i in range(9)
    ]
    assert all(radii[i][k] < MICRO for i in range(9) for k in range(9))
    assert all(centers[i][k] == centers[k][i] for i in range(9) for k in range(9))

    block = lambda rr, cc: [[centers[i][k] for k in cc] for i in rr]
    A, B, C = block(PI, PI), block(PI, JI), block(JI, JI)

    # TRUE interval Gershgorin, not just midpoint regularity.
    c_gaps = []
    for i, ii in enumerate(JI):
        off_upper = sum(
            (abs(centers[ii][jj]) + radii[ii][jj] for j, jj in enumerate(JI) if j != i),
            F(0),
        )
        c_gaps.append(centers[ii][ii] - radii[ii][ii] - off_upper)
    assert min(c_gaps) > F(4)  # true C and midpoint C0 are SPD
    assert max(abs(x) for row in B for x in row) < 6

    ci = inverse_exact(C)
    bcb = matmul(matmul(B, ci), transpose(B))
    mid = [[A[i][k] - bcb[i][k] for k in range(3)] for i in range(3)]
    assert all(mid[i][k] == mid[k][i] for i in range(3) for k in range(3))

    s_gaps = [
        mid[i][i] - sum((abs(mid[i][k]) for k in range(3) if k != i), F(0))
        for i in range(3)
    ]
    assert min(s_gaps) > F(249, 100)

    # Guaranteed norm bounds using dimensions 3x3,3x5,5x5 and |entry|<1e-6.
    # True ||C^{-1}||2 and midpoint ||C0^{-1}||2 are both <1/4.
    # ||B0||2<=||B0||F < sqrt(15)*6 <30.
    ea, eb, ec = F(3,10**6), F(4,10**6), F(5,10**6)
    norm_error = ea + (2 * eb * 30) / 4 + (eb**2) / 4 + (30**2 * ec) / 16
    assert norm_error < F(1,1000)
    assert min(s_gaps) - norm_error > F(248,100)

    # The selected three variations change true metric, not local Lorentz
    # frame: in eta=diag(+---) their independent nonzero metric slots are
    # (00), (11), (12), respectively.
    def metric_jet(s: list[list[int]]) -> list[list[int]]:
        eta = [1, -1, -1, -1]
        return [[eta[i]*s[i][k]+eta[k]*s[k][i] for k in range(4)] for i in range(4)]
    s0 = [[int(i == k == 0) for k in range(4)] for i in range(4)]
    s2 = [[int(i == k and i > 0) for k in range(4)] for i in range(4)]
    s3 = [[int(i > 0 and k > 0 and i != k) for k in range(4)] for i in range(4)]
    m0,m2,m3 = map(metric_jet,(s0,s2,s3))
    assert (m0[0][0],m0[1][1],m0[1][2]) == (2,0,0)
    assert (m2[0][0],m2[1][1],m2[1][2]) == (0,-2,0)
    assert (m3[0][0],m3[1][1],m3[1][2]) == (0,0,-2)

    print("EXACT_RATIONAL_HJR_IR_METRIC_GAP_PASS")
    print(f"SHA256 input: {SOURCE_SHA}")
    print(f"true internal C Gershgorin margins: {[round(float(x),9) for x in c_gaps]}")
    print("symmetry-invariant metric q=0 Schur midpoint:")
    for row in mid:
        print("  ", " ".join(f"{float(x): .12f}" for x in row))
    print(f"midpoint metric row margins: {[round(float(x),9) for x in s_gaps]}")
    print(f"norm-error upper bound: {float(norm_error):.12g}")
    print("PROVED: lambda_min(metric zero-mode HJR Schur) > 248/100")
    print("REFERENCE: vacuum six-face Palatini homogeneous metric Hessian = 0")
    print("Scope: conditional full HJR at exact L8 flat stationary root, not selected full D0 price.")


if __name__ == "__main__":
    main()
