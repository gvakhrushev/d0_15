#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=180
"""Exact S3 reduction of the full joint symbol on spatial-equal characters.

On lambda=(mu,mu*r,mu*r,mu*r), the spatial 3-cycle and a spatial swap
with phase+2 act by signed permutation representations on the 96 inputs
and 136 outputs.  The full symbol intertwines those actions coefficientwise.
The input representation is 16 trivial + 16 sign + 32 standard copies.
The standard block is tested on its 32-dimensional swap-minus half; group
equivariance supplies its swap-plus half.  This is a reduction of the
two-complex-dimensional locus problem, not a full rank-locus theorem.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import sympy as sp
from sympy.polys.domains import QQ
from sympy.polys.matrices import DomainMatrix

import a4d_y_curved_joint_rational_stencil as S

HERE = Path(__file__).resolve().parent
OUT = HERE / "a4d_y_curved_joint_spatial_equal_s3_results.json"


def ck(name, condition):
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name, flush=True)


def action(pi, generator_map, phase_shift):
    on_input = np.zeros((96, 96), dtype=np.int64)
    on_output = np.zeros((136, 136), dtype=np.int64)
    for column, (phase, role, generator) in enumerate(S.LABELS):
        image_generator, sign = generator_map[generator]
        target = S.IDX[((phase + phase_shift) % 4,
                        pi[role], image_generator)]
        on_input[target, column] = sign
        on_output[target, column] = sign
    for row in range(96, 136):
        phase = (row - 96) // 10
        a, b = S.SYM[(row - 96) % 10]
        image_pair = tuple(sorted((pi[a], pi[b])))
        target = 96 + 10 * ((phase + phase_shift) % 4) + S.SYM.index(image_pair)
        on_output[target, row] = 1
    return on_input, on_output


cycle, cycle_out = action(
    {0: 0, 1: 2, 2: 3, 3: 1},
    {0: (1, 1), 1: (2, 1), 2: (0, 1),
     3: (5, 1), 4: (3, -1), 5: (4, -1)}, 0)
swap, swap_out = action(
    {0: 0, 1: 1, 2: 3, 3: 2},
    {0: (0, 1), 1: (2, 1), 2: (1, 1),
     3: (4, 1), 4: (3, 1), 5: (5, -1)}, 2)


def group_checks(name, c, t):
    ident = np.eye(len(c), dtype=np.int64)
    ck(name + "_ORTHOGONAL_SIGNED_PERMUTATIONS",
       np.array_equal(c.T @ c, ident) and np.array_equal(t.T @ t, ident))
    ck(name + "_S3_RELATIONS",
       np.array_equal(c @ c @ c, ident)
       and np.array_equal(t @ t, ident)
       and np.array_equal(t @ c @ t, c @ c))
    n = len(c)
    chi_c, chi_t = int(np.trace(c)), int(np.trace(t))
    multiplicities = ((n + 3*chi_t + 2*chi_c) // 6,
                      (n - 3*chi_t + 2*chi_c) // 6,
                      (n - chi_c) // 3)
    ck(name + "_CHARACTER_DECOMPOSITION",
       6*multiplicities[0] == n + 3*chi_t + 2*chi_c
       and 6*multiplicities[1] == n - 3*chi_t + 2*chi_c
       and 3*multiplicities[2] == n - chi_c
       and multiplicities[0] + multiplicities[1]
           + 2*multiplicities[2] == n)
    return [chi_c, chi_t], list(multiplicities)


input_characters, input_multiplicities = group_checks("INPUT", cycle, swap)
output_characters, output_multiplicities = group_checks(
    "OUTPUT", cycle_out, swap_out)
ck("EXPECTED_INPUT_16_16_32", input_multiplicities == [16, 16, 32])
ck("EXPECTED_OUTPUT_24_24_44", output_multiplicities == [24, 24, 44])

# Coefficients of 14*mu*r*Q(mu,mu*r,mu*r,mu*r). Every exponent is 0, 1 or 2.
coeff = np.zeros((3, 3, 136, 96), dtype=np.int64)
for owner, offset in ((S.ATERMS, 0), (S.QTERMS, 96)):
    for shift, entries in owner.items():
        mu_degree = 1 + sum(shift)
        r_degree = 1 + sum(shift[1:])
        ck("BIDEGREE_" + str(shift),
           0 <= mu_degree <= 2 and 0 <= r_degree <= 2)
        for (row, column), value in entries.items():
            scaled = 14 * value
            if scaled.denominator != 1:
                raise AssertionError("DENOMINATOR_14")
            coeff[mu_degree, r_degree, offset + row, column] += scaled.numerator
ck("SMALL_INTEGER_COEFFICIENTS", int(np.max(np.abs(coeff))) <= 21)

nonzero_bidegrees = []
for mu_degree in range(3):
    for r_degree in range(3):
        matrix = coeff[mu_degree, r_degree]
        if not np.any(matrix):
            continue
        nonzero_bidegrees.append([mu_degree, r_degree])
        ck("CYCLE_INTERTWINER_%d_%d" % (mu_degree, r_degree),
           np.array_equal(matrix @ cycle, cycle_out @ matrix))
        ck("SWAP_INTERTWINER_%d_%d" % (mu_degree, r_degree),
           np.array_equal(matrix @ swap, swap_out @ matrix))
ck("SEVEN_BIDEGREE_BLOCKS", len(nonzero_bidegrees) == 7)

physical_y = np.zeros(96, dtype=np.int64)
for phase, sign in ((0, 1), (2, -1)):
    physical_y[24*phase+3:24*phase+6] = sign*np.array((1, -1, 1))
ck("FOLDED_KERNEL_CONTAINS_LITERAL_PHYSICAL_Y",
   np.array_equal(np.sum(coeff, axis=(0, 1)) @ physical_y,
                  np.zeros(136, dtype=np.int64)))

ident = np.eye(96, dtype=np.int64)
rotation_sum = ident + cycle + cycle @ cycle
projectors = {
    "trivial": rotation_sum @ (ident + swap),
    "sign": rotation_sum @ (ident - swap),
    "standard_swap_minus": (3*ident - rotation_sum) @ (ident - swap),
}
expected_dimensions = {"trivial": 16, "sign": 16,
                       "standard_swap_minus": 32}
bases = {}
basis_columns = {}
for name, projector in projectors.items():
    _, pivot_columns = DomainMatrix.from_Matrix(
        sp.Matrix(projector).T).convert_to(QQ).rref()
    basis = projector[:, list(pivot_columns)]
    ck(name.upper() + "_EXACT_DIMENSION",
       basis.shape == (96, expected_dimensions[name]))
    sign = 1 if name == "trivial" else -1
    ck(name.upper() + "_SWAP_EIGENSPACE",
       np.array_equal(swap @ basis, sign*basis))
    ck(name.upper() + "_ROTATION_ISOTYPIC",
       np.array_equal(rotation_sum @ basis,
                      (0 if name == "standard_swap_minus" else 3)*basis))
    bases[name] = basis
    basis_columns[name] = list(pivot_columns)

# The plus half of each standard copy is generated from its minus half.
standard_minus = bases["standard_swap_minus"]
standard_plus = (ident + swap) @ cycle @ standard_minus
ck("STANDARD_PLUS_SWAP_EIGENSPACE",
   np.array_equal(swap @ standard_plus, standard_plus))
all_columns = np.column_stack((bases["trivial"], bases["sign"],
                               standard_minus, standard_plus))
ck("THREE_BLOCKS_GENERATE_ALL_INPUTS",
   all_columns.shape == (96, 96)
   and DomainMatrix.from_Matrix(sp.Matrix(all_columns)).convert_to(QQ).rank()
       == 96)

output_ident = np.eye(136, dtype=np.int64)
output_rotation_sum = output_ident + cycle_out + cycle_out @ cycle_out
output_standard_minus_projector = (
    (3*output_ident-output_rotation_sum) @ (output_ident-swap_out))
_, output_pivots = DomainMatrix.from_Matrix(
    sp.Matrix(output_standard_minus_projector).T).convert_to(QQ).rref()
output_standard_minus = output_standard_minus_projector[:, list(output_pivots)]
output_standard_plus = (output_ident+swap_out) @ cycle_out @ output_standard_minus
ck("OUTPUT_STANDARD_HALVES_GENERATE_FULL_ISOTYPIC",
   output_standard_minus.shape == (136, 44)
   and DomainMatrix.from_Matrix(sp.Matrix(np.column_stack((
       output_standard_minus, output_standard_plus)))).convert_to(QQ).rank()
       == 88)


def evaluate_block(basis, mu, ratio):
    block_coeff = np.einsum("abij,jk->abik", coeff, basis, optimize=True)
    powers_mu = np.array([1, mu, mu*mu], dtype=np.int64)
    powers_r = np.array([1, ratio, ratio*ratio], dtype=np.int64)
    return np.einsum("a,b,abij->ij", powers_mu, powers_r,
                     block_coeff, optimize=True)


block_records = []
for name, basis in bases.items():
    block_coeff = np.einsum("abij,jk->abik", coeff, basis, optimize=True)
    ck(name.upper() + "_BOUNDED_INTEGER_ARITHMETIC",
       int(np.max(np.abs(block_coeff))) <= 1000)
    point_ranks = {}
    for mu, ratio in ((2, 3), (3, 2), (1, 1), (1, -1)):
        matrix = evaluate_block(basis, mu, ratio)
        rank = DomainMatrix.from_Matrix(sp.Matrix(matrix)).convert_to(QQ).rank()
        point_ranks["%d,%d" % (mu, ratio)] = rank
    ck(name.upper() + "_GENERIC_FULL_RANK",
       point_ranks["2,3"] == expected_dimensions[name]
       and point_ranks["3,2"] == expected_dimensions[name])
    expected_fold = 15 if name == "trivial" else expected_dimensions[name]
    ck(name.upper() + "_FOLDED_RANK",
       point_ranks["1,1"] == expected_fold)
    raw = ",".join(str(int(x)) for x in block_coeff.flat).encode()
    block_records.append({
        "name": name,
        "input_dimension": expected_dimensions[name],
        "basis_pivot_columns": basis_columns[name],
        "coefficient_shape": list(block_coeff.shape),
        "coefficient_sha256": hashlib.sha256(raw).hexdigest(),
        "exact_point_ranks": point_ranks,
    })

result = {
    "schema": "a4d-y-curved-joint-spatial-equal-s3-v1",
    "terminal": "A4D-Y-CURVED-JOINT-SPATIAL-EQUAL-S3-REDUCTION-CERTIFIED",
    "surface": "lambda=(mu,mu*r,mu*r,mu*r), mu*r != 0",
    "scaled_matrix": "14*mu*r*Q",
    "input_characters_cycle_swap": input_characters,
    "output_characters_cycle_swap": output_characters,
    "input_multiplicities_trivial_sign_standard": input_multiplicities,
    "output_multiplicities_trivial_sign_standard": output_multiplicities,
    "nonzero_bidegrees": nonzero_bidegrees,
    "standard_output_halves": [44, 44],
    "block_records": block_records,
    "rank_test": "full Q rank 96 iff trivial rank 16, sign rank 16, and standard-swap-minus rank 32",
    "generic_surface_rank": 96,
    "folded_rank_at_mu_r_one": 95,
    "folded_kernel_contains_literal_physical_y": True,
    "scope_fence": [
        "exact S3 reduction on the spatial-equal two-complex-dimensional surface",
        "finite point ranks do not classify continuous surface rank drops",
        "not the full three-ratio physical torus or nonlinear curved response",
    ],
}
if __name__ == "__main__" and "--write" in __import__("sys").argv:
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    print("WROTE", OUT, flush=True)
else:
    ck("RESULTS_MATCH_PINNED_JSON", json.loads(OUT.read_text()) == result)
print("TERMINAL", result["terminal"])
