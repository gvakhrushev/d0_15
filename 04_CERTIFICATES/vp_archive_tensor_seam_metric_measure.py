#!/usr/bin/env python3
"""Tensor Seam Metric-Measure Field Certificate.

Pure standard-library implementation.
Verifies:
  1. Mass density: mu(x) = prod_s m(x_s) with m(j) in {1, 2}.
  2. Directional conductances: c_r(x) = prod_(s != r) m(x_s) = mu(x) / m(x_r).
  3. In 4D, c_r(x) takes values in {1, 2, 4, 8}.
  4. Principal inverse metric: g^(rr)(x) = c_r(x) / mu(x) = 1 / m(x_r).
  5. Effective metric component: g_rr(x) = m(x_r).
  6. Reachable mutation control:
       Adding a transverse coupling term breaks the exact identity g_rr(x) == m(x_r).
"""

from __future__ import annotations
import itertools
import math
import sys

def m(coord: int) -> int:
    return 2 if coord == 0 else 1

def mu(x: tuple[int, ...]) -> int:
    prod = 1
    for xi in x:
        prod *= m(xi)
    return prod

def conductance(r: int, x: tuple[int, ...], mutate: bool = False) -> int:
    prod = 1
    for s, xs in enumerate(x):
        if s != r:
            prod *= m(xs)
    if mutate and r == 0:
        prod += 1  # corrupt conductance
    return prod

def test_metric_measure():
    L = 3
    D = 4
    all_points = list(itertools.product(range(L), repeat=D))
    assert len(all_points) == L**D

    conductance_values = set()

    for x in all_points:
        mu_x = mu(x)
        assert 1 <= mu_x <= 16

        for r in range(D):
            c_r = conductance(r, x)
            conductance_values.add(c_r)
            # Check c_r(x) = mu(x) / m(x_r)
            assert c_r * m(x[r]) == mu_x, f"Relation failed at x={x}, r={r}"

            # Check g_rr(x) = mu(x) / c_r(x) = m(x_r)
            g_rr = mu_x // c_r
            assert g_rr == m(x[r]), f"g_rr mismatch at x={x}, r={r}"

    # In 4D, c_r must take values in {1, 2, 4, 8}
    assert conductance_values == {1, 2, 4, 8}, f"Unexpected conductances: {conductance_values}"

    # Mutation control: corrupted conductance violates g_rr == m(x_r)
    corrupted_found = False
    for x in all_points:
        c_mut = conductance(0, x, mutate=True)
        if c_mut * m(x[0]) != mu(x):
            corrupted_found = True
            break
    assert corrupted_found, "Mutation control failed: corruption was not detected"

if __name__ == "__main__":
    test_metric_measure()
    print("PASS: vp_archive_tensor_seam_metric_measure certified with reachable negative control.")
