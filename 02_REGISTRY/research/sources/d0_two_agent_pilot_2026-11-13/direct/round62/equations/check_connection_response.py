"""Exact rank and projection checks for the spin-connection row on the Bianchi coframe."""
from fractions import Fraction
from itertools import combinations
from math import prod

DIM = 4
ETA = (1, -1, -1, -1)
ROWS = [(a, b, c) for a, b in combinations(range(DIM), 2) for c in range(DIM)]


def antisymmetric_component(row, a, b, c):
    if a == b:
        return 0
    if a < b:
        return row[a, b, c]
    return -row[b, a, c]


def trace(row):
    return tuple(sum(ETA[b] * antisymmetric_component(row, a, b, b)
                     for b in range(DIM)) for a in range(DIM))


def gradient_row(k):
    return {(a, b, c): (ETA[b] * k[a] if b == c else 0)
                        - (ETA[a] * k[b] if a == c else 0)
            for a, b, c in ROWS}


def orientation(indices):
    if len(set(indices)) != DIM:
        return 0
    inversions = sum(a > b for a, b in combinations(indices, 2))
    return (-1) ** inversions


def hodge_row(k):
    # Minus the exterior Hodge star of k wedge Sigma_ab, with eps_0123=+1.
    row = {}
    for a, b, c in ROWS:
        i, j = (v for v in range(DIM) if v not in (a, b))
        row[a, b, c] = -orientation((a, b, i, j)) * sum(
            k[m] * prod(ETA[v] for v in (m, i, j)) * orientation((m, i, j, c))
            for m in range(DIM))
    return row


def project(row):
    return gradient_row(tuple(Fraction(t, 3) for t in trace(row)))


def run():
    for i in range(DIM):
        unit = tuple(int(a == i) for a in range(DIM))
        assert hodge_row(unit) == gradient_row(unit)
        assert trace(gradient_row(unit)) == tuple(3*t for t in unit)
    projector_trace = 0
    for index in ROWS:
        row = {r: int(r == index) for r in ROWS}
        part = project(row)
        assert project(part) == part
        remainder = {r: row[r] - part[r] for r in ROWS}
        assert trace(remainder) == (0, 0, 0, 0)
        projector_trace += part[index]
        if index == (0, 1, 2):
            assert row == remainder
    assert projector_trace == 4 and len(ROWS) - projector_trace == 20
    print("Exact basis check: rank(P)=4 and rank(1-P)=20.")


if __name__ == "__main__":
    run()
