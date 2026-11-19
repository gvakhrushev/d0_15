#!/usr/bin/env python3
"""Exact finite Bloch-rank control for the period-four #232 Y background.

The checker decomposes the original connection Hessian on the 4^4 periodic
carrier into its 64 Bloch sectors modulo the diagonal period-four reciprocal
vector.  The zero sector is checked over QQ; each nonzero sector is certified
full rank by one exact reduction Q(i) -> F_1009.  A full-rank image proves the
corresponding exact Q(i) matrix is nonsingular.  This is a finite linearized
control, not a nonlinear continuation or a refinement-uniform estimate.
"""
from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path
import sympy as sp
from sympy.polys.domains import QQ
from sympy.polys.matrices import DomainMatrix

import a4d_y_center_wave_cubic_vertex_check as vertex


HERE = Path(__file__).resolve().parent
OUT = HERE / "a4d_y_period_four_bloch_resonance_results.json"
PINS = {
    "a4d_y_center_wave_cubic_vertex_check.py":
        "21119792e670f5f105aecd5c45b83310e1ab19939ff42967002d86429c4f6c77",
    "a4d_y_curved_normaljet_compatibility_check.py":
        "942b72a2c8528975fe8571217efd95b92d4210786e4247b10e4e2431326b0649",
    "a4d_y_curved_response_quotient_check.py":
        "fdce0e5ea00ac848edd3f81e126600b0aae0fa84bb4a6f3228a0b87645c48cb4",
    "a4d_y_slow_exact_plane_check.py":
        "d85c644f22cdcd8b7c7ad63c72dd780c87af3184b4b35bf2b3e438bcde3afd21",
}
PRIME = 1009


def require(condition: bool, name: str) -> None:
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name, flush=True)


def check_pins() -> None:
    for name, expected in PINS.items():
        digest = hashlib.sha256((HERE / name).read_bytes()).hexdigest()
        require(digest == expected, "PIN_" + name)


def exact_bloch_blocks(faces, labels):
    """Return exact Hermitian 96x96 blocks as rational (real,imag) pairs."""
    blocks = {}
    hermitian_all = True
    for tail in itertools.product(range(4), repeat=3):
        momentum = (0,) + tail
        block = [
            [[sp.Rational(0), sp.Rational(0)] for _ in range(96)]
            for __ in range(96)
        ]
        for phase, a, b, _locs, local, Hloc, _factors in faces:
            shifts = [
                (0, 0, 0, 0),
                tuple(int(r == a) for r in range(4)),
                tuple(int(r == b) for r in range(4)),
                (0, 0, 0, 0),
            ]
            phase_power = [
                sum(momentum[r] * shift[r] for r in range(4)) % 4
                for shift in shifts
            ]
            for i, (pos_i, _gen_i, global_i) in enumerate(local):
                for j, (pos_j, _gen_j, global_j) in enumerate(local):
                    value = Hloc[i, j]
                    if value.is_Rational is not True:
                        raise AssertionError("LOCAL_HESSIAN_ENTRY_NOT_RATIONAL")
                    power = (phase_power[pos_j] - phase_power[pos_i]) % 4
                    if power == 0:
                        block[global_i][global_j][0] += value
                    elif power == 1:
                        block[global_i][global_j][1] += value
                    elif power == 2:
                        block[global_i][global_j][0] -= value
                    else:
                        block[global_i][global_j][1] -= value
        hermitian = all(
            block[i][j][0] == block[j][i][0]
            and block[i][j][1] == -block[j][i][1]
            for i in range(96) for j in range(96)
        )
        hermitian_all = hermitian_all and hermitian
        blocks[tail] = block
    require(hermitian_all, "ALL_64_BLOCH_BLOCKS_HERMITIAN")
    return blocks


def mod_rational(value: sp.Rational, prime: int) -> int:
    value = sp.Rational(value)
    denominator = int(value.q) % prime
    if denominator == 0:
        raise AssertionError("MODULAR_DENOMINATOR_NOT_INVERTIBLE")
    return (int(value.p) % prime) * pow(denominator, prime - 2, prime) % prime


def rank_mod_gaussian(block, prime: int, root_i: int) -> int:
    matrix = [
        [
            (mod_rational(real, prime)
             + root_i * mod_rational(imag, prime)) % prime
            for real, imag in row
        ]
        for row in block
    ]
    size = len(matrix)
    rank = 0
    for column in range(size):
        pivot = next((r for r in range(rank, size)
                      if matrix[r][column] != 0), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        pivot_value = matrix[rank][column]
        inv = pow(pivot_value, prime - 2, prime)
        pivot_row = [(value * inv) % prime for value in matrix[rank]]
        matrix[rank] = pivot_row
        for row in range(rank + 1, size):
            coefficient = matrix[row][column]
            if coefficient:
                matrix[row] = [
                    (matrix[row][j] - coefficient * pivot_row[j]) % prime
                    for j in range(size)
                ]
        rank += 1
        if rank == size:
            break
    return rank


def block_as_matrix(block):
    return sp.Matrix([
        [real + sp.I * imag for real, imag in row]
        for row in block
    ])


def run(write: bool = False) -> dict:
    check_pins()
    require(sp.isprime(PRIME), "CERTIFY_PRIME")
    require(PRIME % 4 == 1, "PRIME_SPLITS_I")
    root_i = next(r for r in range(2, PRIME) if r * r % PRIME == PRIME - 1)
    require(root_i * root_i % PRIME == PRIME - 1, "FINITE_FIELD_SQUARE_ROOT_MINUS_ONE")

    hessian, labels, faces0 = vertex.build_hessian(sp.Integer(1), sp.Integer(0))
    faces = vertex.C.with_base_phases(faces0)
    require(len(faces) == 24, "SIX_FACES_AT_EACH_OF_FOUR_PHASES")
    center = vertex.center_basis(sp.Integer(1), labels)
    require(hessian * center == sp.zeros(96, 2) and center.rank() == 2,
            "EXACT_TWO_DIMENSIONAL_ZERO_MOMENTUM_CENTER")
    blocks = exact_bloch_blocks(faces, labels)
    zero = block_as_matrix(blocks[(0, 0, 0)])
    require(zero == hessian, "ZERO_BLOCH_BLOCK_MATCHES_OWNED_HESSIAN")
    zero_rank = DomainMatrix.from_Matrix(zero).convert_to(QQ).rank()
    require(zero_rank == 94, "EXACT_ZERO_SECTOR_RANK_94")

    nonzero = []
    full_rank_all = True
    for momentum, block in sorted(blocks.items()):
        if momentum == (0, 0, 0):
            continue
        modular_rank = rank_mod_gaussian(block, PRIME, root_i)
        full_rank_all = full_rank_all and modular_rank == 96
        nonzero.append({
            "representative": [0, *momentum],
            "rank_mod_prime": modular_rank,
            "prime": PRIME,
            "sqrt_minus_one": root_i,
        })
    require(len(nonzero) == 63, "ALL_63_NONZERO_SECTORS_COVERED")
    require(full_rank_all, "ALL_63_NONZERO_SECTORS_EXACTLY_NONSINGULAR")

    result = {
        "schema": "a4d-y-period-four-bloch-resonance-v1",
        "carrier": "original six-based-plaquette connection Hessian; 4^4 periodic grid",
        "background": "flat solder; exact period-four Y wave; Cayley amplitude z=1; dual center d=0",
        "bloch_representatives": "k=(0,m1,m2,m3), mj in Z/4; quotient by k~k+(1,1,1,1)",
        "zero_sector": {
            "representative": [0, 0, 0, 0],
            "exact_QQ_rank": zero_rank,
            "kernel_dimension": 2,
            "kernel_equals_owned_center": True,
        },
        "nonzero_sectors": nonzero,
        "all_64_blocks_hermitian": True,
        "all_nonzero_sectors_exactly_nonsingular": len(nonzero) == 63,
        "exactness": (
            "rank 96 modulo the split prime 1009 implies nonzero determinant over Q(i); "
            "all rational denominators are checked invertible before reduction"
        ),
        "scope_fence": [
            "finite L=4 Bloch spectrum only",
            "connection Hessian at fixed flat solder, not the full joint metric-link Hessian",
            "does not control larger refinement lattices or near-resonant modes",
            "does not prove nonlinear continuation, source matching, or normalized response",
        ],
    }
    if OUT.exists() and not write:
        require(result == json.loads(OUT.read_text()), "RESULTS_MATCH_PINNED_JSON")
    else:
        OUT.write_text(json.dumps(result, indent=2) + "\n")
        print("WROTE", OUT, flush=True)
    print("TERMINAL A4D-Y-PERIOD-FOUR-NONZERO-BLOCH-SECTORS-NONSINGULAR")
    return result


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    run(parser.parse_args().write)
