#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=180
"""Exact generic-coframe control for all eight quarter role axes.

The accompanying proof uses external role permutation and polynomial
continuation of the owned all-coframe Y theorem.  This independent rational
point replays all 96 link and 64 unrestricted solder rows on every axis; it
is a control, not a replacement for the analytic all-coframe argument.
"""
from __future__ import annotations

import argparse
import json
from fractions import Fraction as F
from pathlib import Path

import numpy as np

import a4d_identity_quarter_nonlinear_response_check as FLAT

HERE = Path(__file__).resolve().parent
OUT = HERE / "a4d_identity_quarter_generic_axes_results.json"
I4 = np.eye(4, dtype=object)
S = np.array([
    [F(1), F(0), F(0), F(0)],
    [F(1, 7), F(1), F(1, 5), F(0)],
    [F(1, 11), F(1, 9), F(1), F(1, 6)],
    [F(0), F(1, 8), F(1, 10), F(1)],
], dtype=object)
ETA = np.diag(FLAT.SIG).astype(object)


def check(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name, flush=True)


TRIANGLES = []
for role in range(4):
    a, b, c = [j for j in range(4) if j != role]
    u, v = S[:, b] - S[:, a], S[:, c] - S[:, a]
    TRIANGLES.append(np.outer(v, u @ ETA) - np.outer(u, v @ ETA))

WEIGHT, DWEIGHT = [], []
for r, s in FLAT.PAIRS:
    u, v = [j for j in range(4) if j not in (r, s)]
    WEIGHT.append(FLAT.orient(r, s) * FLAT.weight(
        FLAT.wedge(S[:, u], S[:, v])))
    variations = []
    for column in range(4):
        for component in range(4):
            unit = np.array([F(j == component) for j in range(4)],
                            dtype=object)
            area = (FLAT.wedge(unit, S[:, v]) if column == u
                    else FLAT.wedge(S[:, u], unit) if column == v
                    else np.zeros(6, dtype=object))
            variations.append(FLAT.orient(r, s) * FLAT.weight(area))
    DWEIGHT.append(np.array(variations, dtype=object))


def literal_euler(links: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    connection = np.zeros((4, 4, 6), dtype=object)
    solder = np.zeros((4, 16), dtype=object)
    for phase in range(4):
        for face, (r, s) in enumerate(FLAT.PAIRS):
            locations = [
                (phase, r, False), ((phase + 1) % 4, s, False),
                ((phase + 1) % 4, r, True), (phase, s, True),
            ]
            factors = [
                FLAT.jinv(links[p, role][None])[0] if inverse
                else links[p, role]
                for p, role, inverse in locations
            ]
            prefix = [I4]
            for factor in factors:
                prefix.append(prefix[-1] @ factor)
            suffix = [None] * 5
            suffix[4] = I4
            for j in range(3, -1, -1):
                suffix[j] = factors[j] @ suffix[j + 1]
            product = prefix[4]
            for row in range(16):
                solder[phase, row] += np.sum(DWEIGHT[face][row] * product)
            for j, (p, role, inverse) in enumerate(locations):
                covector = suffix[j + 1] @ WEIGHT[face].T @ prefix[j]
                jet = (-factors[j] @ covector if inverse
                       else covector @ factors[j])
                for generator in range(6):
                    connection[p, role, generator] += np.sum(
                        jet.T * FLAT.G[generator])
    return connection, solder


amplitude = F(1, 5)
records = []
for role, triangle in enumerate(TRIANGLES):
    cube = triangle @ triangle @ triangle
    pivot = next((i, j) for i in range(4) for j in range(4)
                 if triangle[i, j])
    kappa = F(cube[pivot], triangle[pivot])
    check(f"SIMPLE_BIVECTOR_CUBIC_{role}",
          np.array_equal(cube, kappa * triangle))
    denominator = 4 - kappa * amplitude**2
    check(f"CAYLEY_DENOMINATOR_NONZERO_{role}", denominator != 0)
    square = triangle @ triangle
    forward = I4 + (4 * amplitude * triangle
                    + 2 * amplitude**2 * square) / denominator
    backward = I4 + (-4 * amplitude * triangle
                     + 2 * amplitude**2 * square) / denominator
    check(f"EXACT_LORENTZ_INVERSE_{role}",
          np.array_equal(forward @ backward, I4))
    for parity in (0, 1):
        links = np.array([[I4.copy() for _ in range(4)]
                          for _ in range(4)], dtype=object)
        links[parity, role] = forward
        links[parity + 2, role] = backward
        connection, solder = literal_euler(links)
        check(f"ALL_96_CONNECTION_ROWS_ROLE_{role}_PARITY_{parity}",
              not np.any(connection))
        check(f"ALL_64_SOLDER_ROWS_ROLE_{role}_PARITY_{parity}",
              not np.any(solder))
        records.append({
            "role": role, "parity": parity,
            "connection_nonzero": int(np.count_nonzero(connection)),
            "solder_nonzero": int(np.count_nonzero(solder)),
            "kappa": str(kappa), "cayley_denominator": str(denominator),
        })

result = {
    "schema": "a4d-identity-quarter-generic-axes-control-v1",
    "coframe": [[str(value) for value in row] for row in S],
    "amplitude": str(amplitude),
    "axis_records": records,
    "conclusion": "all eight role/parity Cayley axes are exact joint vacua at this nonorthogonal rational coframe",
    "scope_fence": [
        "one exact rational coframe/amplitude control; all-coframe theorem uses role permutation and polynomial continuation",
        "no classification of mixed amplitudes away from the identity chart",
        "no varying-coframe nonlinear continuation or owner-sum response limit",
    ],
}
parser = argparse.ArgumentParser()
parser.add_argument("--write", action="store_true")
args = parser.parse_args()
if OUT.exists() and not args.write:
    check("RESULTS_MATCH_PINNED_JSON", result == json.loads(OUT.read_text()))
else:
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    print("WROTE", OUT, flush=True)
print("TERMINAL A4D-IDENTITY-QUARTER-GENERIC-COFRAME-EIGHT-AXES-CONTROL",
      flush=True)
