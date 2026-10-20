#!/usr/bin/env python3
"""A rational negative direction from an existing certified Hessian enclosure.

This is a consumer of the pinned full-HJR interval packet, not a replay of
its full spectral Hessian. No float arithmetic or eigenvalue solver is used.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

PROOF = '02_REGISTRY/research/sources/d0_native_flag_source_minimum_2026-10-20/inputs/fixed_collar_root_07f2.md'
HESSIAN = '02_REGISTRY/research/sources/d0_native_flag_source_minimum_2026-10-20/inputs/collar_hessian_07f2.json'
PROOF_SHA = '60149e109412b7716384aca6e64091b8a67f3374c4dfa02b170df1182e58dd1d'
HESSIAN_SHA = 'a38386a86af4be283631d42a890caf66c035c12a4f9d421037160550d36989f4'
WIDE_PROOF = '02_REGISTRY/research/sources/d0_native_flag_source_minimum_2026-10-20/inputs/wide_collar_root_5b5.md'
WIDE_PACKET = '02_REGISTRY/research/sources/d0_native_flag_source_minimum_2026-10-20/inputs/wide_collar_5b5.json'
WIDE_CHECKER = '02_REGISTRY/research/sources/d0_native_flag_source_minimum_2026-10-20/inputs/wide_collar_checker_5b5.txt'
WIDE_PROOF_SHA = '9d90121a775dac6bd1df49cea04d398b248ca118fcf871b00e166000dd5db735'
WIDE_PACKET_SHA = 'dee20425e01aeba2f090a55e2b1d221d57160a667eff9240a1c58368cd87e305'
WIDE_CHECKER_SHA = '1956aff0f6227a72c4afe3224db898b846581268794d41eab1170b581a72bf28'
V = (-1, -2, -1, 0, -2, -1, 0, 0, 0, 1)


def ball(text):
    assert text.startswith('[') and text.endswith(']'), text
    mid, rad = text[1:-1].split('+/-')
    radius = F(rad.strip())
    assert radius >= 0
    return F(mid.strip() or '0'), radius


def transpose(A):
    return [list(row) for row in zip(*A)]


def mm(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B)))
             for j in range(len(B[0]))] for i in range(len(A))]


def add(A, B):
    return [[a + b for a, b in zip(x, y)] for x, y in zip(A, B)]


def quad(A, v):
    mid = sum(F(v[i] * v[j]) * A[i][j][0]
              for i in range(len(v)) for j in range(len(v)))
    rad = sum(abs(F(v[i] * v[j])) * A[i][j][1]
              for i in range(len(v)) for j in range(len(v)))
    return mid - rad, mid + rad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', type=Path, required=True)
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    pins = {PROOF: PROOF_SHA, HESSIAN: HESSIAN_SHA,
            WIDE_PROOF: WIDE_PROOF_SHA, WIDE_PACKET: WIDE_PACKET_SHA,
            WIDE_CHECKER: WIDE_CHECKER_SHA}
    for name, expected in pins.items():
        actual = hashlib.sha256((args.root / name).read_bytes()).hexdigest()
        assert actual == expected, (name, actual, expected)
    packet = json.loads((args.root / HESSIAN).read_text())
    assert packet['status'] == 'RIGOROUS_ARB_PASS'
    assert packet['L'] == 8 and packet['fixedRIGHT'] == 128
    assert len(packet['A']) == 10
    A = [[ball(s) for s in row] for row in packet['A']]
    assert all(len(row) == 10 for row in A)
    lo, hi = quad(A, V)
    assert lo == -F(2372501681, 4000000000)
    assert hi == -F(2372493199, 4000000000)
    assert hi < -F(593, 1000)
    # The source owner defines A as eight times the actual chart Hessian.
    actual_lo, actual_hi = lo / 8, hi / 8
    assert actual_hi < -F(7414, 100000)
    norm2 = sum(x * x for x in V)
    assert norm2 == 12
    # Removing cross terms would lose the actual negative direction.
    diagonal_lo = sum(V[i] ** 2 * (A[i][i][0] - A[i][i][1]) for i in range(10))
    assert diagonal_lo > 0
    # Literal fixed-space basis substitution in the owned ten-variable chart.
    eta = [[int(i == j) * (1 if i == 0 else -1) for j in range(4)] for i in range(4)]
    Q = [[-int(i == j) - 4 * int(i == 0 and j > 0) for j in range(4)] for i in range(4)]
    metric_generator = add(mm(transpose(Q), eta), mm(eta, Q))
    assert metric_generator == [[-2, -4, -4, -4], [-4, 2, 0, 0], [-4, 0, 2, 0], [-4, 0, 0, 2]]
    B = [[int(i == 0 and j > 0) + int(j == 0 and i > 0) for j in range(4)] for i in range(4)]
    assert add(mm(transpose(B), eta), mm(eta, B)) == [[0] * 4 for _ in range(4)]
    # The later theorem only appends to the original proof. Its bulk chart
    # uses the same action, Riesz section and periodic Fourier kernel H.
    assert (args.root / WIDE_PROOF).read_bytes().startswith((args.root / PROOF).read_bytes())
    wide = json.loads((args.root / WIDE_PACKET).read_text())
    assert wide['status'] == 'RIGOROUS_W7_BULK_COLLAR_PASS'
    assert wide['source_sha256'] == HESSIAN_SHA
    assert wide['source_certificate_status'] == packet['status']
    assert wide['L'] == 8 and wide['unknowns'] == 64
    assert wide['interior_slices'] == list(range(7)) and wide['fixed_collar_slice'] == 7
    assert wide['positions'] == [t for t in range(7) for _ in range(9)] + [7]
    assert wide['components'] == list(range(9)) * 7 + [5]
    embedding = list(range(9)) + [63]
    old_positions, old_components = [0] * 9 + [-1], list(range(9)) + [5]
    def old_kernel_key(i, j):
        return ((old_positions[i] - old_positions[j]) % 8,
                old_components[i], old_components[j])
    def wide_kernel_key(i, j):
        return ((wide['positions'][i] - wide['positions'][j]) % 8,
                wide['components'][i], wide['components'][j])
    # Verify every entry of E^T A_wide E = A, at the exact kernel-index level.
    # This is not a new numerical evaluation or inversion of A_wide.
    assert all(old_kernel_key(i, j) == wide_kernel_key(embedding[i], embedding[j])
               for i in range(10) for j in range(10))
    wide_v = [0] * 64
    for i, value in zip(embedding, V):
        wide_v[i] = value
    assert sum(value * value for value in wide_v) == norm2
    assert {i: value for i, value in enumerate(wide_v) if value} == {
        0: -1, 1: -2, 2: -1, 4: -2, 5: -1, 63: 1}
    # A wrong last coordinate would not preserve the incoming-link component.
    assert old_kernel_key(9, 0) != wide_kernel_key(62, 0)
    out = {
        'status': 'EXACT_RATIONAL_NEGATIVE_DIRECTION_PASS',
        'source_commit': '07f2f2b15b7050a612d0075aa73db8dc46087a95',
        'input_sha256': pins,
        'chart_direction': list(V),
        'chart_euclidean_norm_squared': norm2,
        'v_A_v_interval': [str(lo), str(hi)],
        'actual_second_variation_interval': [str(actual_lo), str(actual_hi)],
        'necessary_correction_second_variation_lower_bound': str(-actual_hi),
        'normalized_necessary_operator_bound': str(-actual_hi / norm2),
        'coframe_left_generator': Q,
        'metric_generator_nonzero': metric_generator,
        'incoming_time_link_generator': B,
        'outgoing_time_link_generator': [[-x for x in row] for row in B],
        'diagonal_only_false_minimum_control': str(diagonal_lo),
        'bulk_embedding': {
            'status': 'EXACT_10_TO_64_KERNEL_INDEX_EMBEDDING_PASS',
            'source_commit': '5b5c60047f1cfe518d4a8b42d9f71c6db033779c',
            'fixed_L': 8,
            'old_to_wide_indices': embedding,
            'embedded_direction_nonzero': {str(i): value for i, value in enumerate(wide_v) if value},
            'chart_euclidean_norm_squared': norm2,
            'matched_principal_compression_entries': 100,
            'actual_second_variation_interval': [str(actual_lo), str(actual_hi)],
            'normalization': 'A/8 in both charts at the same homogeneous root',
            'method': 'Same full action and Riesz section; exact period-eight Fourier kernel index identity. No wide spectral/Hessian replay.',
            'scope': 'Fixed L8 bulk chart and its sufficiently small curved branch by continuity. The delta-slice coframe C1_h tangent and link-log K=log(U)/h tangent have size of order 1/h; no uniform refinement instability or uniform-preparation theorem is inferred.'
        },
        'scope': 'Strict local minimization of the declared conditional whole HJR on its fixed-collar/full-Riesz fixedRIGHT128 family. Not a refutation of its exact stationary roots, of weighted laws or stationary GR, and not a derivation of native admission or complete D0 price.'
    }
    text = json.dumps(out, indent=2) + '\n'
    if args.output:
        args.output.write_text(text)
    print(text, end='')

if __name__ == '__main__':
    main()
