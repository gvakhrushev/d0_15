#!/usr/bin/env python3
"""Exact finite controls for the Lean spectral scene recognition theorem.

The strongest universal proof is D0.Synthesis.DenseOperatorSceneRigidity. This independent
integer-arithmetic certificate exhausts all labelled simple graphs through six
vertices, checks the scene under relabelling, and supplies a 33-vertex rival
with the same second and third moments but higher rank. It does not use data
fitting or floating-point eigenvalue thresholds.
"""
from __future__ import annotations

import argparse
import itertools
import math
import random


def rank(matrix: list[list[int]]) -> int:
    """Exact rational rank by fraction-free elimination and row gcd reduction."""
    a = [row[:] for row in matrix]
    r = 0
    for c in range(len(a)):
        pivot = next((i for i in range(r, len(a)) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        for i in range(r + 1, len(a)):
            if a[i][c]:
                p, q = a[r][c], a[i][c]
                a[i] = [p*x - q*y for x, y in zip(a[i], a[r])]
                divisor = math.gcd(*a[i])
                if divisor:
                    a[i] = [x // divisor for x in a[i]]
        r += 1
    return r


def tripartite(sizes: tuple[int, int, int]) -> list[list[int]]:
    labels = [i for i, count in enumerate(sizes) for _ in range(count)]
    return [[int(i != j) for j in labels] for i in labels]


def moments(a: list[list[int]]) -> tuple[int, int]:
    n = len(a)
    return (
        sum(a[i][j] * a[j][i] for i in range(n) for j in range(n)),
        sum(a[i][j] * a[j][k] * a[k][i]
            for i in range(n) for j in range(n) for k in range(n)),
    )


def recognize(a: list[list[int]], triangle: tuple[int, int, int]) -> list[int]:
    assert all(a[i][j] == int(i != j) for i in triangle for j in triangle)
    labels = []
    for row in a:
        profile = [row[i] for i in triangle]
        assert sum(profile) == 2, profile
        labels.append(profile.index(0))
    assert all(a[i][j] == int(labels[i] != labels[j])
               for i in range(len(a)) for j in range(len(a)))
    return labels


def exhaustive_small_graphs() -> tuple[int, int]:
    tested = recognized = 0
    for n in range(1, 7):
        pairs = list(itertools.combinations(range(n), 2))
        for mask in range(1 << len(pairs)):
            a = [[0] * n for _ in range(n)]
            for bit, (i, j) in enumerate(pairs):
                a[i][j] = a[j][i] = (mask >> bit) & 1
            tested += 1
            if not all(any(row) for row in a):
                continue
            triangle = next((t for t in itertools.combinations(range(n), 3)
                             if all(a[i][j] for i, j in itertools.combinations(t, 2))), None)
            if triangle is not None and rank(a) <= 3:
                recognize(a, triangle)
                recognized += 1
    return tested, recognized


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--mutate', action='store_true',
                        help='Deliberately break the input scene; this run must fail.')
    args = parser.parse_args()
    scene = tripartite((9, 11, 13))
    if args.mutate:
        scene[0][9] = scene[9][0] = 0
    assert rank(scene) == 3
    assert moments(scene) == (718, 7722)
    labels = recognize(scene, (0, 9, 20))
    assert sorted(labels.count(i) for i in range(3)) == [9, 11, 13]
    # Reconstruction must not depend on vertex addresses or on the anchor order.
    rng = random.Random(3591287)
    for _ in range(12):
        order = list(range(33))
        rng.shuffle(order)
        a = [[scene[i][j] for j in order] for i in order]
        anchor = [order.index(i) for i in (0, 9, 20)]
        rng.shuffle(anchor)
        zs = recognize(a, tuple(anchor))
        assert sorted(zs.count(i) for i in range(3)) == [9, 11, 13]
    print('PASS scene, exact moments, 12 vertex/anchor relabellings')

    # Same V,E,T is NOT sufficient outside the tripartite class. This graph
    # has 33 vertices, 359 edges, 1287 triangles, but rank 5 rather than 3.
    twin = tripartite((12, 12, 9))
    twin[0][12] = twin[12][0] = 0
    assert len(twin) == 33 and moments(twin) == (718, 7722)
    assert rank(twin) == 5
    assert sorted(map(sum, twin)) != sorted(map(sum, scene))
    print('PASS rank-deletion rival: K(12,12,9) minus one 12-to-12 edge, rank=5')

    # Carrier size is also observable: an invisible isolated vertex leaves
    # every positive moment and the rank unchanged.
    with_isolate = [row + [0] for row in scene] + [[0] * 34]
    assert rank(with_isolate) == 3 and moments(with_isolate) == (718, 7722)
    assert len(with_isolate) != 33
    print('PASS carrier-size deletion rival: scene plus one isolated vertex')

    # Without the quadratic moment, dimension and rank do not pick a scene.
    balanced = tripartite((11, 11, 11))
    assert len(balanced) == 33 and rank(balanced) == 3
    assert moments(balanced)[0] == 726 != 718
    assert sorted(map(sum, balanced)) != sorted(map(sum, scene))
    print('PASS quadratic-moment deletion rival: K(11,11,11)')

    # Independent finite arithmetic check: E=359 and at most 33 active vertices
    # admit exactly the selected unordered three-part sizes.
    triples = [(a, b, c) for a in range(1, 34) for b in range(a, 34)
               for c in range(b, 34) if a+b+c <= 33 and a*b+a*c+b*c == 359]
    assert triples == [(9, 11, 13)]
    assert 33**2 // 4 < 359 and 32**2 // 3 < 359
    print('PASS three-reading reduction and unique bounded part sizes')

    tested, recognized = exhaustive_small_graphs()
    assert tested == 33867
    assert recognized > 0
    print(f'PASS exhaustive simple graphs n<=6: tested={tested}, recognized={recognized}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
