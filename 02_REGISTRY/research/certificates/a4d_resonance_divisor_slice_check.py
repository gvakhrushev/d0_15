#!/usr/bin/env python3
"""Exact exploratory slices of the owned four-character connection Hessian.

This certificate rebuilds the same 24x24 A(Z) convention as
`a4d_resonance_divisor_counterexample_check.py`. It does not claim a global
factorization or complete rank stratification.
"""
from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path

import sympy as sp

PAIR = list(combinations(range(4), 2))
PAIR_INDEX = {pair: i for i, pair in enumerate(PAIR)}
I = sp.I
ETA = sp.diag(1, -1, -1, -1)
G2 = sp.diag(*(ETA[a, a] * ETA[b, b] for a, b in PAIR))
STAR = sp.zeros(6)
for src, (dst, sign) in {
    (0, 1): ((2, 3), -1), (0, 2): ((1, 3), 1), (0, 3): ((1, 2), -1),
    (1, 2): ((0, 3), 1), (1, 3): ((0, 2), -1), (2, 3): ((0, 1), 1),
}.items():
    STAR[PAIR_INDEX[dst], PAIR_INDEX[src]] = sign


def boost(j: int) -> sp.Matrix:
    out = sp.zeros(4)
    out[0, j] = out[j, 0] = 1
    return out


def rotation(i: int, j: int) -> sp.Matrix:
    out = sp.zeros(4)
    out[i, j], out[j, i] = 1, -1
    return out


GEN = [boost(1), boost(2), boost(3), rotation(1, 2), rotation(1, 3), rotation(2, 3)]
BASIS = [sp.eye(4)[:, j] for j in range(4)]
AV = sp.symbols("a0:24")
BV = sp.symbols("b0:24")
A_LINKS = [sum((AV[6 * r + j] * GEN[j] for j in range(6)), sp.zeros(4)) for r in range(4)]
B_LINKS = [sum((BV[6 * r + j] * GEN[j] for j in range(6)), sp.zeros(4)) for r in range(4)]


def wedge(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.Matrix([left[a] * right[b] - left[b] * right[a] for a, b in PAIR])


def bivector(matrix: sp.Matrix) -> sp.Matrix:
    lowered = matrix * ETA
    return sp.Matrix([lowered[a, b] for a, b in PAIR])


def orientation(face: tuple[int, int]) -> int:
    complement = [j for j in range(4) if j not in face]
    sequence = list(face) + complement
    inversions = sum(sequence[i] > sequence[j]
                     for i in range(4) for j in range(i + 1, 4))
    return -1 if inversions % 2 else 1


def mul4(left, right):
    return (
        left[0] * right[0],
        left[0] * right[1] + left[1] * right[0],
        left[0] * right[2] + left[2] * right[0],
        left[0] * right[3] + left[1] * right[2]
        + left[2] * right[1] + left[3] * right[0],
    )


def exp4(left, right, phase_left=1, phase_right=1, inverse=False):
    sign = -1 if inverse else 1
    return (
        sp.eye(4),
        sign * phase_left * left,
        sign * phase_right * right,
        sp.Rational(1, 2) * phase_left * phase_right
        * (left * right + right * left),
    )


def curvature_mixed(plaquette):
    return plaquette[3] - sp.Rational(1, 2) * (
        plaquette[1] * plaquette[2] + plaquette[2] * plaquette[1]
    )


def connection_hessian(characters: tuple[sp.Expr, ...]) -> sp.Matrix:
    action = sp.Integer(0)
    for r, s in PAIR:
        plaquette = (sp.eye(4), sp.zeros(4), sp.zeros(4), sp.zeros(4))
        plaquette = mul4(plaquette, exp4(A_LINKS[r], B_LINKS[r]))
        plaquette = mul4(plaquette, exp4(A_LINKS[s], B_LINKS[s], characters[r], 1 / characters[r]))
        plaquette = mul4(plaquette, exp4(A_LINKS[r], B_LINKS[r], characters[s], 1 / characters[s], True))
        plaquette = mul4(plaquette, exp4(A_LINKS[s], B_LINKS[s], inverse=True))
        u, v = [j for j in range(4) if j not in (r, s)]
        area = wedge(BASIS[u], BASIS[v])
        action += orientation((r, s)) * (
            area.T * G2 * STAR * bivector(curvature_mixed(plaquette))
        )[0]
    action = sp.expand(action)
    return sp.Matrix(24, 24, lambda i, j: sp.diff(sp.diff(action, AV[i]), BV[j]))


def exact_rank(matrix: sp.Matrix, domain) -> int:
    return int(matrix.to_DM().convert_to(domain).rank())


def check(label: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(label)
    print("PASS_" + label, flush=True)


z = sp.symbols("z0:4")
A = connection_hessian(z)
check("OWNER_SHAPE_24x24", A.shape == (24, 24))
check("OWNER_NONZERO_COUNT_96", sum(value != 0 for value in A) == 96)

# Entrywise Laurent complexity after exact cancellation.
entry_terms = []
entry_degrees = []
entry_denominators = set()
for value in A:
    numerator, denominator = sp.fraction(sp.cancel(value))
    numerator_poly = sp.Poly(numerator, *z)
    entry_terms.append(len(numerator_poly.terms()))
    entry_degrees.append(numerator_poly.total_degree())
    entry_denominators.add(str(sp.factor(denominator)))
check("ENTRY_TERMS_AT_MOST_4", max(entry_terms) <= 4)
check("ENTRY_NUMERATOR_TOTAL_DEGREE_AT_MOST_2", max(entry_degrees) <= 2)
check("ENTRY_DENOMINATORS_OWNED", entry_denominators <= {"1", *(f"2*{zj}" for zj in z)})

# Each 6x6 role-to-role block has rank four over Q(z0,z1,z2,z3).
function_field = sp.QQ.frac_field(*z)
block_ranks = []
for r in range(4):
    row = []
    for s in range(4):
        block = A.extract(range(6 * r, 6 * r + 6), range(6 * s, 6 * s + 6))
        row.append(int(block.to_DM().convert_to(function_field).rank()))
    block_ranks.append(row)
check("ALL_ROLE_BLOCK_GENERIC_RANK_4", block_ranks == [[4] * 4 for _ in range(4)])

x = sp.symbols("x")
one, minus_one = sp.Integer(1), sp.Integer(-1)
slices = {
    "(x,1,1,1)": ((x, one, one, one), (3 * x**4 - 22 * x**2 + 3)**2 / x**4),
    "(x,x,1,1)": ((x, x, one, one), sp.Integer(256)),
    "(x,1/x,1,1)": ((x, 1 / x, one, one), (x**4 - 2 * x**3 - 2 * x**2 - 2 * x + 1)**4 / x**8),
    "(x,x,x,1)": ((x, x, x, one), (x**8 + 6 * x**6 + 18 * x**4 + 6 * x**2 + 1)**2 / (4 * x**8)),
    "(x,-1,1,1)": ((x, minus_one, one, one), (x**6 - 3 * x**5 - x**4 - 10 * x**3 - x**2 - 3 * x + 1)**2 / x**6),
}
slice_results = {}
for label, (characters, expected) in slices.items():
    determinant = sp.factor(sp.cancel(connection_hessian(characters).det(method="domain-ge")))
    check("SLICE_" + label.replace(" ", "").replace(",", "_").replace("(", "").replace(")", "").replace("/", "over"),
          sp.simplify(determinant - expected) == 0)
    slice_results[label] = str(determinant)

# Exact negative controls inherited from the merged phase-count-law refutation.
A_generic = connection_hessian((one, one, one, one))
A_counterexample = connection_hessian((minus_one, minus_one, I, I))
field_i = sp.QQ.algebraic_field(I)
rank_generic = exact_rank(A_generic, field_i)
rank_counterexample = exact_rank(A_counterexample, field_i)
check("NEGATIVE_CONTROL_FULL_RANK_AT_ONE", rank_generic == 24)
check("NEGATIVE_CONTROL_COUNT_LAW_COUNTEREXAMPLE", rank_counterexample == 22)

# A global square up to a Laurent unit would have a fixed square-class on
# every point whose four character coordinates are rational squares. Ratios
# of two such determinant values would therefore be rational squares.
square_points = {
    "(4,9,16,25)": (sp.Integer(4), sp.Integer(9), sp.Integer(16), sp.Integer(25)),
    "(1,4,9,16)": (sp.Integer(1), sp.Integer(4), sp.Integer(9), sp.Integer(16)),
    "(4,1,25,9)": (sp.Integer(4), sp.Integer(1), sp.Integer(25), sp.Integer(9)),
}
specialized_determinants = {
    label: sp.Rational(connection_hessian(characters).det(method="domain-ge"))
    for label, characters in square_points.items()
}


def is_rational_square(value: sp.Expr) -> bool:
    numerator, denominator = sp.fraction(sp.cancel(value))
    numerator_root, numerator_is_square = sp.integer_nthroot(abs(int(numerator)), 2)
    denominator_root, denominator_is_square = sp.integer_nthroot(int(denominator), 2)
    return numerator_is_square and denominator_is_square and int(numerator) >= 0


square_class_ratios = {}
labels = list(specialized_determinants)
for i in range(len(labels)):
    for j in range(i + 1, len(labels)):
        ratio = sp.factor(specialized_determinants[labels[i]] / specialized_determinants[labels[j]])
        square_class_ratios[f"{labels[i]} / {labels[j]}"] = str(ratio)
check("GLOBAL_DETERMINANT_NOT_LAURENT_UNIT_TIMES_SQUARE",
      all(not is_rational_square(
          specialized_determinants[labels[i]] / specialized_determinants[labels[j]]
      ) for i in range(len(labels)) for j in range(i + 1, len(labels))))

result = {
    "owner": "a4d_resonance_divisor_counterexample_check.py connection_hessian convention",
    "symbol_shape": [24, 24],
    "nonzero_entries": 96,
    "max_entry_numerator_terms": max(entry_terms),
    "max_entry_numerator_total_degree": max(entry_degrees),
    "entry_denominators": sorted(entry_denominators),
    "role_block_generic_ranks_over_Q(z)": block_ranks,
    "exact_slice_determinants": slice_results,
    "negative_controls": {
        "rank_at_(1,1,1,1)": rank_generic,
        "rank_at_(-1,-1,i,i)_over_Q(i)": rank_counterexample,
    },
    "square_character_specializations": {
        "determinants": {label: str(value) for label, value in specialized_determinants.items()},
        "ratios": square_class_ratios,
        "conclusion": "global determinant is not a rational Laurent unit times a square",
    },
    "global_multivariable_factorization": "OPEN",
    "complete_rank_stratification": "OPEN",
}
output = Path(__file__).with_name("a4d_resonance_divisor_slice_results.json")
output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
print("TERMINAL A4D_RESONANCE_DIVISOR_EXACT_SLICES_CERTIFIED", flush=True)
print("RESULT_JSON", output, flush=True)
