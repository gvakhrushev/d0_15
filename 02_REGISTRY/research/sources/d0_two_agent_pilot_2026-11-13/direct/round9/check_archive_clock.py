#!/usr/bin/env python3
"""Literal six-copy archive layout and original growing-clock heat bound.

No external PVM channel or complete H.1 field execution is silently supplied.
Integer stage accounting and rational bounds are exact; small full-clock
controls are numerical, independently constructed on unequal stage fibres.
"""
from collections import Counter
from fractions import Fraction as Q
from itertools import product
import json
import math

import mpmath as mp
import numpy as np

checks = []


def mm(a, b):
    # Avoid platform BLAS warnings on these small, finite real controls.
    return np.einsum("ij,jk->ik", a, b, optimize=False)


def det(a):
    return complex(mp.det(mp.matrix(a.tolist())))


def ck(ok, label):
    if not bool(ok):
        raise ArithmeticError(label)
    checks.append(label)


def cx(a, b):
    return ("CX", (a, b))


def swap(a, b):
    return [cx(a, b), cx(b, a), cx(a, b)]


def inv_g(a):
    # Actual selective SourceI is on port 0 and the two opaque Spin wires.
    z = swap(0, a) + [("SourceI", (0, 3, 4))] * 2 + swap(0, a)
    return z + [("G", (a,))] + z


echo = [cx(1, 2)] + inv_g(2) + [cx(1, 2)] + inv_g(2)
births = [("Birth", (a,)) for a in range(5, 11)]
prep = [g for a in range(5, 11) for g in inv_g(a)]
deliver = []
for slot, wire in enumerate((1, 2, 1, 2)):
    deliver += swap(0, wire) + [cx(0, 5 + slot)]
    if slot >= 2:
        deliver += [cx(2 if slot == 2 else 1, 5 + slot + 2)]
    deliver += swap(0, wire)
stages = echo + births + prep + deliver
ck(Counter(op for op, _ in echo) == {"CX": 26, "G": 2, "SourceI": 8}, "36 actual echo calls")
ck(Counter(op for op, _ in prep + deliver) == {"CX": 102, "G": 6, "SourceI": 24}, "132 actual reader calls")
ck(len(stages) == 174 and len(deliver) == 30, "174 real added stages")
ck(stages[-1] == cx(0, 2), "last real deliver CX is the closing gate")

live = set(range(5))
width = 1  # Units of the complete original carrier dimension d.
dimension_sum = 0
detail = []
for j, (op, wires) in enumerate(stages):
    dimension_sum += width
    if op == "Birth":
        ck(wires[0] not in live, f"birth {wires[0]} is a new live address")
        detail.append((j + 1, width))
        live.add(wires[0])
        width *= 2
    else:
        ck(set(wires) <= live, f"stage {j} has only live addresses")
        ck(op == "SourceI" or not set(wires) & {3, 4}, f"stage {j} keeps opaque Spin addressing")
        if op == "SourceI":
            ck(wires == (0, 3, 4), f"stage {j} uses the real source port")
ages = [len(stages) - j for j, _ in detail]
ck(width == 64 and dimension_sum == 8547, "full final carrier 64d and clock increment 8547d")
ck(ages == [137, 136, 135, 134, 133, 132], "all actual new birth ages retained")
ck(174 + sum(age * rank for age, (_, rank) in zip(ages, detail)) == dimension_sum,
   "old details shift by174 and new detail ages reproduce the full dimension")
ck(132 * 64 <= dimension_sum, "D >= L times final dimension")

# Actual routed copies, including invalid 11 and arbitrary nonzero archive.
patterns = {}
for bits in product((0, 1), repeat=9):
    wires = (0, 1, 2, 5, 6, 7, 8, 9, 10)
    start = dict(zip(wires, bits))
    state = start.copy()
    for _, (a, b) in deliver:
        state[b] ^= state[a]
    r, t = start[1], start[2]
    ck(all(state[a] == start[a] for a in (0, 1, 2)), "all-column port/payload restoration")
    marks = tuple(state[a] ^ start[a] for a in range(5, 11))
    ck(marks == (r, t, r, t, t, r), "all six raw records including inactive slots")
    patterns[f"{r}{t}"] = list(marks)

# Original CL8, all33 scene modes and both Hodge degrees included.
x = Q(2, 55)


def heat_bound(age):
    return Q(176, 359) * x**age / math.factorial(age) / ((1 - x*x) * (1 - x/age))


mp.mp.dps = 100
bound = heat_bound(132)
as_mp = lambda value: mp.mpf(value.numerator) / value.denominator
ck(bound > 0 and bound < Q(1, 10**414), "exact full heat coefficient A132 below 1e-414")
ck(heat_bound(134) < bound, "literal CX pair improves minimum-age thermal bound")


def small_clock(extra_pairs):
    """Direct G3 construction; deliberately not the whole large reader matrix."""
    p = (math.sqrt(5) - 1) / 2
    v = np.array([[math.sqrt(p)], [p]])
    G = np.array([[math.sqrt(p), -p], [p, math.sqrt(p)]])
    CX = np.eye(4)[:, [0, 1, 3, 2]]
    # birth, G, birth, G(first), CX, paid CX pairs, final G(second).
    F = [v, G, np.kron(np.eye(2), v), np.kron(G, np.eye(2)), CX]
    F += [CX] * (2 * extra_pairs)
    F += [np.kron(np.eye(2), G)]
    dims = [f.shape[1] for f in F]
    n, d = len(F), dims[-1]
    offsets = np.cumsum([0] + dims)
    D = int(offsets[-1])
    passive = [f if f.shape[0] != f.shape[1] else np.eye(f.shape[1]) for f in F[:-1]]
    B = [None] * n
    B[-1] = np.eye(d)
    for j in range(n - 2, -1, -1):
        B[j] = mm(B[j + 1], passive[j])
    R = np.zeros((D, d))
    Pi, detail_ops, age_rank = [], [], []
    for j in range(n):
        detail_j = np.eye(dims[j]) if j == 0 else np.eye(dims[j]) - mm(passive[j - 1], passive[j - 1].T)
        R[offsets[j]:offsets[j+1]] = mm(detail_j, B[j].T)
        Pi.append(mm(mm(B[j], detail_j), B[j].T))
        detail_ops.append(detail_j)
        rank = int(round(np.trace(detail_j)))
        if rank:
            age_rank.append((n-j, rank))
    T = np.zeros((D, D))
    for j in range(n-1):
        T[offsets[j+1]:offsets[j+2], offsets[j]:offsets[j+1]] = F[j]
    T[:, offsets[-2]:offsets[-1]] += mm(R, F[-1])
    ck(np.linalg.norm(mm(T.T, T) - np.eye(D)) < 2e-14, "full unequal-fibre clock is unitary")
    ck(sum(age*rank for age, rank in age_rank) == D, "complete detail-age dimension identity")
    L = min(age for age, _ in age_rank)
    power = np.eye(D)
    for k in range(1, L):
        power = mm(T, power)
        ck(abs(np.trace(power)) < 3e-14, "all low actual clock windings vanish")
    # True canonical completion: each detail begins at its own birth stage.
    # Tensoring an old gate with identity on an as-yet unborn wire is a
    # different all-column extension and gives a WRONG winding polynomial.
    W = np.zeros((d, d))
    for j in range(n):
        forward = F[-1].copy()
        for k in range(n-2, j-1, -1):
            forward = mm(forward, F[k])
        W += mm(mm(forward, detail_ops[j]), B[j].T)
    ck(np.linalg.norm(mm(W.T, W)-np.eye(d)) < 2e-14, "true birth-detail canonical completion is unitary")
    wrong_W = np.eye(d)
    for f in F:
        if f.shape[0] == f.shape[1]:
            wrong_W = mm(np.kron(f, np.eye(d // f.shape[0])), wrong_W)
    wrong_errors = []
    for zeta in (.13, -.21, .17 + .11j):
        C = sum(zeta**(n-j) * Pi[j] for j in range(n))
        err = abs(det(np.eye(D) - zeta*T) - det(np.eye(d) - mm(W, C)))
        ck(err < 4e-13, "original determinant winding identity on actual unequal fibres")
        wrong_errors.append(abs(det(np.eye(D)-zeta*T)-det(np.eye(d)-mm(wrong_W,C))))
    ck(max(wrong_errors) > 1e-10, "negative control rejects the padded raw endpoint on unborn complements")
    # Generated cuts; all old stages retained, complete complementary closure.
    P = np.zeros((D, D))
    A = np.ones((1, 1))
    for j in range(n):
        P[offsets[j]:offsets[j+1], offsets[j]:offsets[j+1]] = mm(A, A.T)
        if j < n-1:
            A = mm(F[j], A)
    Ccold = float((mm(mm(B[0].T, F[-1]), A))[0, 0])
    feedback = mm(mm(mm(mm(P, T.T), np.eye(D) - P), T), P)
    for zeta in (.2, .7):
        actual = det(np.eye(D) - zeta*feedback)
        ck(abs(actual - (1-zeta+zeta*Ccold**2)) < 2e-13, "same original full feedback determinant")
    return {"stages": n, "D": D, "L": L, "cold": Ccold,
            "wrong_completion_polynomial_defect": max(wrong_errors)}


controls = [small_clock(k) for k in range(3)]
ck(max(c["cold"] for c in controls) - min(c["cold"] for c in controls) < 1e-14,
   "paid identity pairs retain cold while changing the genuine clock")

# Negative control: a dephasing map is not one of the unitary clock stages.
plus = np.ones((2, 1)) / math.sqrt(2)
rho = mm(plus, plus.T)
dephased = np.diag(np.diag(rho))
ck(abs(np.trace(mm(rho, rho))-1) < 1e-14 and abs(np.trace(mm(dephased, dephased))-.5) < 1e-14,
   "external dephasing cannot be represented as a unitary on the same carrier")

print(json.dumps({
    "status": "PASS_LITERAL_ARCHIVE_GROWING_CLOCK",
    "checks": len(checks),
    "additional_stages": 174,
    "additional_clock_dimension_in_units_d": dimension_sum,
    "final_dimension_in_units_d": width,
    "new_detail_ages": ages,
    "new_detail_ranks_in_units_d": [rank for _, rank in detail],
    "minimum_age": 132,
    "full_modes": "425*(D_prefix+8547*d)",
    "harmonic_complement": "359*(D_prefix+8547*d)",
    "actual_last_gate": stages[-1],
    "archive_patterns": patterns,
    "A132_rational_numerator": str(bound.numerator),
    "A132_rational_denominator": str(bound.denominator),
    "A132_decimal": mp.nstr(as_mp(bound), 35),
    "log10_A132": mp.nstr(mp.log10(as_mp(bound)), 35),
    "normalized_full_heat_bound": "A132*C_full/Gamma, with the actual norm and positive gain",
    "small_full_clock_controls": controls,
    "entire_H1_execution_replayed": False,
    "external_measurement_dilation_supplied": False,
    "physical_Cost_Info_binding": False,
    "GR_closed": False,
}, indent=2))
