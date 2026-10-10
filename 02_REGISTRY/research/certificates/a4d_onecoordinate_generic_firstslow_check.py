#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=180
"""Exact rank-four shared-link first-slow witness in a physical metric tangent.

Generalizes the owned warped first-slow face assembly at S=I from its one
diagonal derivative to an arbitrary symmetric Gram derivative. The old warp
is an entrywise negative control for the generalized code path.
"""
from __future__ import annotations

import argparse
import json
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path

import numpy as np

import a4d_warped_quarter_regular_response_check as W
from a4d_designated_full_gap_check import QI

OUT = Path(__file__).with_name("a4d_onecoordinate_generic_firstslow_results.json")


def check(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name, flush=True)


def first_smooth_data(d_s: np.ndarray):
    s = W.I.copy()
    weights, dweights = W.faceweights(s)
    triangles, dtriangles = W.transport(s, d_s)
    forcing = np.zeros(24, dtype=object)
    for r, t in W.PAIRS:
        u, v = [j for j in range(4) if j not in (r, t)]
        area = W.wedge(d_s[:, u], s[:, v]) + W.wedge(s[:, u], d_s[:, v])
        dweight = W.orient(r, t) * W.weight(area)
        for j, generator in enumerate(W.G):
            entry = np.sum(dweight * generator)
            forcing[6*r+j] += (t == 1) * entry
            forcing[6*t+j] -= (r == 1) * entry
    h = np.array([[x.re for x in row] for row in W.symbol(1, F(1))], dtype=object)
    smooth = -W.inverse(h) @ forcing
    b = np.array([sum(smooth[6*r+j]*W.G[j] for j in range(6))
                  for r in range(4)])
    return s, triangles, dtriangles, weights, dweights, b, smooth


def literal_jet(amplitudes, data, d_s, damps=None):
    """h^0,h^1 by t^0,t^1,t^2; all incident faces and boundary links."""
    s, triangles, dtriangles, weights, dweights, background, _ = data
    phases = np.array(amplitudes, dtype=object).reshape(2, 4)
    phases = np.array([phases[0], phases[1], -phases[0], -phases[1]])
    if damps is None:
        damps = np.zeros((2, 4), dtype=object)
    deriv = np.array(damps, dtype=object).reshape(2, 4)
    deriv = np.array([deriv[0], deriv[1], -deriv[0], -deriv[1]])
    dweight = []
    for r, t in W.PAIRS:
        u, v = [j for j in range(4) if j not in (r, t)]
        area = W.wedge(d_s[:, u], s[:, v]) + W.wedge(s[:, u], d_s[:, v])
        dweight.append(W.orient(r, t) * W.weight(area))
    ek = np.zeros((4, 2, 3, 24), dtype=object)
    eq = np.zeros((4, 2, 3, 10), dtype=object)
    for phase in range(4):
        for face, (r, t) in enumerate(W.PAIRS):
            roles = (r, t, r, t)
            offsets = (0, int(r == 1), int(t == 1), 0)
            shifts = (0, 1, 1, 0)

            def factors(base_phase, base_offset):
                result = []
                for j, role in enumerate(roles):
                    p = (base_phase + shifts[j]) % 4
                    offset = base_offset + offsets[j]
                    factor = W.links(
                        phases[p, role], triangles[role], dtriangles[role],
                        background[role], offset, cprime=deriv[p, role])
                    result.append(W.linv(factor) if j >= 2 else factor)
                return result

            product = W.const(W.I)
            for factor in factors(phase, 0):
                product = W.jm(product, factor)
            for h in range(2):
                for degree in range(3):
                    for row in range(10):
                        eq[phase, h, degree, row] += np.sum(
                            dweights[face, row] * product[h, degree])

            for j, role in enumerate(roles):
                base_phase = (phase - shifts[j]) % 4
                base_offset = -offsets[j]
                fac = factors(base_phase, base_offset)
                prefix = W.const(W.I)
                suffix = W.const(W.I)
                for factor in fac[:j]:
                    prefix = W.jm(prefix, factor)
                for factor in fac[j+1:]:
                    suffix = W.jm(suffix, factor)
                weight = W.const(weights[face].T)
                weight[1, 0] = base_offset * dweight[face].T
                covector = W.jm(W.jm(suffix, weight), prefix)
                term = -W.jm(fac[j], covector) if j >= 2 else W.jm(covector, fac[j])
                for h in range(2):
                    for degree in range(3):
                        for g, generator in enumerate(W.G):
                            ek[phase, h, degree, 6*role+g] += np.sum(
                                term[h, degree].T * generator)
    return ek, eq


def reduced_first_slow(data, d_s):
    joint, range_rows, range_inverse = W.joint_data(data)
    rest = [row for row in range(34) if row not in range_rows]
    basis = np.eye(8, dtype=object)
    b, d = [], []
    for i in range(4):
        for target, amplitudes, derivative in (
            (b, basis[i], np.zeros(8, dtype=object)),
            (d, np.zeros(8, dtype=object), basis[i]),
        ):
            ek, eq = literal_jet(amplitudes, data, d_s, derivative)
            source = np.concatenate([ek[:, 1, 1], eq[:, 1, 1]], axis=-1)
            check("ODD_FIRSTSLOW_PHASE_PARITY", np.array_equal(source[2:], -source[:2]))
            complex_source = np.array([QI(x, -y) for x, y in zip(source[0], source[1])],
                                      dtype=object)
            normal = -range_inverse @ complex_source[range_rows]
            target.append((complex_source + joint[:, W.COLS] @ normal)[rest])
    return np.array(b, dtype=object).T, np.array(d, dtype=object).T


def determinant4(matrix):
    total = QI()
    for perm in permutations(range(4)):
        inversions = sum(perm[i] > perm[j] for i in range(4) for j in range(i+1, 4))
        product = QI.of(1)
        for i, j in enumerate(perm):
            product *= matrix[i, j]
        total += (-1 if inversions % 2 else 1) * product
    return total


def compute():
    warp_slope = np.diag([F(0), F(0), F(1), F(1)]).astype(object)
    baseline_b, baseline_d = W.reduced_first_slow(W.setup())
    warp_data = first_smooth_data(warp_slope)
    check("FIRST_SMOOTH_WARP_COEFFICIENT_MATCHES_OWNER",
          np.array_equal(warp_data[-1], W.setup()[-1]))
    warp_b, warp_d = reduced_first_slow(warp_data, warp_slope)
    check("GENERAL_SHARED_LINK_JET_REPLAYS_WARP_B_AND_D_ENTRYWISE",
          np.array_equal(warp_b, baseline_b) and np.array_equal(warp_d, baseline_d))
    derivative_rows = [1, 3, 9, 11]
    warp_selector = np.zeros((4, len(warp_d)), dtype=object)
    for i, row in enumerate(derivative_rows):
        warp_selector[i, row] = 1
    warp_left = W.qi_inverse(warp_d[derivative_rows]) @ warp_selector
    warp_compatibility = warp_b - warp_d @ warp_left @ warp_b
    check("OWNED_DIAGONAL_WARP_COMPATIBILITY_RANK_TWO",
          len(W.independent_rows(warp_compatibility)) == 2)

    qraw = np.array([[(a+1)*(b+2)+(a+b+1) for b in range(4)]
                     for a in range(4)], dtype=object)
    q = (qraw + qraw.T) * F(1, 2)
    d_s = W.ETA @ q * F(1, 2)
    check("PHYSICAL_SYMMETRIC_GRAM_TANGENT", np.array_equal(q, q.T) and
          np.array_equal(d_s.T @ W.ETA @ W.I + W.I.T @ W.ETA @ d_s, q))
    data = first_smooth_data(d_s)
    ek0, eq0 = literal_jet(np.zeros(8, dtype=object), data, d_s)
    check("ALL_BACKGROUND_FIRST_ORDER_CONNECTION_ROWS", not np.any(ek0[:, 1, 0]))
    check("ALL_BACKGROUND_FIRST_ORDER_METRIC_ROWS", not np.any(eq0[:, 1, 0]))
    b, d = reduced_first_slow(data, d_s)
    check("CENTER_DERIVATIVE_RANK_FOUR", len(W.independent_rows(d)) == 4 and
          len(W.independent_rows(d[derivative_rows])) == 4)
    selector = np.zeros((4, len(d)), dtype=object)
    for i, row in enumerate(derivative_rows):
        selector[i, row] = 1
    left = W.qi_inverse(d[derivative_rows]) @ selector
    compatibility = b - d @ left @ b
    rows = W.independent_rows(compatibility)
    check("GENERIC_PHYSICAL_GRADIENT_COMPATIBILITY_RANK_FOUR", len(rows) == 4)
    minor = determinant4(compatibility[rows])
    check("EXACT_COMPLEX_FOUR_BY_FOUR_MINOR_NONZERO", minor != 0)
    return {
        "schema": "a4d-onecoordinate-generic-firstslow-v1",
        "coframe": "S=I",
        "warp_negative_control": "generalized literal shared-link B,D reproduce owned warp entrywise; rank K=2",
        "gram_derivative": [[str(x) for x in row] for row in q],
        "coframe_derivative": [[str(x) for x in row] for row in d_s],
        "first_smooth_log": [str(x) for x in data[-1]],
        "selected_D_rows": derivative_rows,
        "compatibility_rows": rows,
        "compatibility_minor": {"re": str(minor.re), "im": str(minor.im)},
        "compatibility_rank": 4,
        "scope_fence": [
            "one exact physical metric derivative witness; openness and density follow analytically from a nonzero polynomial minor",
            "one-coordinate smooth metrics near identity, not general four-dimensional metrics",
            "first-slow linear compatibility; nonlinear isolation consumes the separate all-frequency parity theorem",
            "no unrestricted response terminal or new source selector",
        ],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = compute()
    if OUT.exists() and not args.write:
        check("RESULTS_MATCH_PINNED_JSON", result == json.loads(OUT.read_text()))
    else:
        OUT.write_text(json.dumps(result, indent=2) + "\n")
        print("WROTE", OUT, flush=True)
    print("TERMINAL A4D-ONECOORDINATE-GENERIC-PHYSICAL-GRADIENT-RANK4", flush=True)
