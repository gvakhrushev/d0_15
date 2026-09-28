#!/usr/bin/env python3
"""Exact counterexample to the proposed phase-count nullity law.

The 24 x 24 polarized connection Hessian is rebuilt from the same second
variation of the finite plaquette action used by the A4D character scans.
All entries and ranks are exact over Q(i).

The proposed rule assigns nullity 2*max(n_+i,n_-i) whenever both counts are
even and their sum is at least two.  At the character below the counts are
(2,0), but the exact nullity is 2, not 4.  A separate full-rank point shows
that det(A) is not identically zero, while this rank-22 point makes it zero;
therefore its zero locus in the character torus is a nonempty proper
hypersurface (a divisor), though this script does not factor its components.
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
A = [sum((AV[6*r+j] * GEN[j] for j in range(6)), sp.zeros(4)) for r in range(4)]
B = [sum((BV[6*r+j] * GEN[j] for j in range(6)), sp.zeros(4)) for r in range(4)]


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
    """Return A_ij = d²S/(da_i db_j) at the supplied four characters."""
    action = sp.Integer(0)
    for r, s in PAIR:
        plaquette = (sp.eye(4), sp.zeros(4), sp.zeros(4), sp.zeros(4))
        plaquette = mul4(plaquette, exp4(A[r], B[r]))
        plaquette = mul4(plaquette, exp4(A[s], B[s], characters[r], 1/characters[r]))
        plaquette = mul4(plaquette, exp4(A[r], B[r], characters[s], 1/characters[s], True))
        plaquette = mul4(plaquette, exp4(A[s], B[s], inverse=True))
        u, v = [j for j in range(4) if j not in (r, s)]
        area = wedge(BASIS[u], BASIS[v])
        action += orientation((r, s)) * (
            area.T * G2 * STAR * bivector(curvature_mixed(plaquette))
        )[0]
    action = sp.expand(action)
    return sp.Matrix(24, 24, lambda i, j: sp.diff(sp.diff(action, AV[i]), BV[j]))


def exact_rank(matrix: sp.Matrix, domain) -> int:
    # DomainMatrix performs elimination in the exact algebraic number field,
    # avoiding numerical tolerances and expression swell from generic EX.
    return int(matrix.to_DM().convert_to(domain).rank())


COUNTEREXAMPLE = (-sp.Integer(1), -sp.Integer(1), I, I)
GENERIC = (sp.Integer(1),) * 4
FIELD = sp.QQ.algebraic_field(I)

A_generic = connection_hessian(GENERIC)
rank_generic = exact_rank(A_generic, FIELD)
assert rank_generic == 24, rank_generic

A_counterexample = connection_hessian(COUNTEREXAMPLE)
rank_counterexample = exact_rank(A_counterexample, FIELD)
nullity_counterexample = 24 - rank_counterexample
n_plus_i = sum(sp.simplify(z - I) == 0 for z in COUNTEREXAMPLE)
n_minus_i = sum(sp.simplify(z + I) == 0 for z in COUNTEREXAMPLE)
predicted_nullity = 2 * max(n_plus_i, n_minus_i)

# Control a supplied scan point written with unevaluated exp(+-2*pi*i/3).
# Normalize those roots of unity before exact elimination.
sqrt3 = sp.sqrt(3)
normalized_root_control = (-sqrt3/2 - I/2, sqrt3/2 - I/2, I, I)
root_field = sp.QQ.algebraic_field(I, sqrt3)
rank_normalized_root_control = exact_rank(
    connection_hessian(normalized_root_control), root_field
)

assert (n_plus_i, n_minus_i) == (2, 0)
assert n_plus_i % 2 == n_minus_i % 2 == 0 and n_plus_i + n_minus_i >= 2
assert rank_counterexample == 22
assert nullity_counterexample == 2
assert nullity_counterexample != predicted_nullity == 4
assert rank_normalized_root_control == 20

print("PASS_GENERIC_FULL_RANK", rank_generic)
print("COUNTEREXAMPLE_Z", [str(z) for z in COUNTEREXAMPLE])
print("EXACT_FIELD", FIELD)
print("COUNTS_n_plus_i_n_minus_i", n_plus_i, n_minus_i)
print("RANK_NULLITY", rank_counterexample, nullity_counterexample)
print("COUNT_RULE_PREDICTS", predicted_nullity)
print("NORMALIZED_EXP_PM_2PI3_RANK", rank_normalized_root_control)
print("TERMINAL A4D_PHASE_COUNT_NULLITY_LAW_REFUTED_ON_FULL_TORUS")

result = {
    "generic_character": [str(z) for z in GENERIC],
    "generic_rank": rank_generic,
    "counterexample_character": [str(z) for z in COUNTEREXAMPLE],
    "exact_field": str(FIELD),
    "n_plus_i": n_plus_i,
    "n_minus_i": n_minus_i,
    "rank": rank_counterexample,
    "nullity": nullity_counterexample,
    "count_rule_prediction": predicted_nullity,
    "normalized_exp_pm_2pi_over_3_control_rank": rank_normalized_root_control,
    "terminal": "A4D_PHASE_COUNT_NULLITY_LAW_REFUTED_ON_FULL_TORUS",
}
out = Path(__file__).with_name("a4d_resonance_divisor_counterexample_results.json")
out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
print("RESULT_JSON", out)
