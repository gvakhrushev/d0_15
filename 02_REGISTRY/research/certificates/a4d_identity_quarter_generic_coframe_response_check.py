#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=180
"""Exact 16-symbol coframe quarter-kernel and mean-response identity.

At the identity connection, the diagonal-quarter full joint symbol has one
triangle-bivector kernel line on each role for every constant coframe.  Its
rank is exactly 20 on a neighborhood of the standard coframe.  The mean
quadratic odd-curvature coefficient of a quarter wave is the difference of
within-role cosine/sine commutators; it vanishes on that entire joint kernel.

This is a frozen finite-stencil theorem, not a varying-coframe continuation.
"""
from __future__ import annotations

import argparse
import json
from fractions import Fraction
from itertools import combinations
from pathlib import Path

import sympy as sp

import a4d_designated_full_gap_check as OWNER

HERE = Path(__file__).resolve().parent
OUT = HERE / "a4d_identity_quarter_generic_coframe_response_results.json"
SIG = (1, -1, -1, -1)
ETA = sp.diag(*SIG)
PAIRS = list(combinations(range(4), 2))
STAR_MAP = ((5, -1), (4, 1), (3, -1), (2, 1), (1, -1), (0, 1))
S = sp.Matrix(4, 4, lambda i, j: sp.Symbol(f"s{i}{j}"))
GEN = [sp.Matrix(G) for G in OWNER.GEN]


def check(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name, flush=True)


def wedge(u: sp.Matrix, v: sp.Matrix) -> sp.Matrix:
    return sp.Matrix([u[a] * v[b] - u[b] * v[a] for a, b in PAIRS])


def orient(a: int, b: int) -> int:
    order = (a, b) + tuple(j for j in range(4) if j not in (a, b))
    inversions = sum(order[i] > order[j] for i in range(4)
                     for j in range(i + 1, 4))
    return -1 if inversions % 2 else 1


def pair(area: sp.Matrix, tangent: sp.Matrix) -> sp.Expr:
    biv = [tangent[a, b] * SIG[b] for a, b in PAIRS]
    return sum(area[row] * SIG[PAIRS[row][0]] * SIG[PAIRS[row][1]]
               * sign * biv[column]
               for column, (row, sign) in enumerate(STAR_MAP))


def triangle(role: int) -> sp.Matrix:
    a, b, c = [j for j in range(4) if j != role]
    u, v = S[:, b] - S[:, a], S[:, c] - S[:, a]
    matrix = v * (u.T * ETA) - u * (v.T * ETA)
    return sp.Matrix([matrix[0, 1], matrix[0, 2], matrix[0, 3],
                      matrix[1, 2], matrix[1, 3], matrix[2, 3]])


TRIANGLES = [triangle(role) for role in range(4)]
H = sp.zeros(24, 24)
C = sp.zeros(16, 24)  # Unrestricted coframe, before the 10 Gram rows.
for r, s in PAIRS:
    u, v = [j for j in range(4) if j not in (r, s)]
    area = wedge(S[:, u], S[:, v])
    roles = (r, s, r, s)
    direct = (1, sp.I, -sp.I, -1)
    inverse = (1, -sp.I, sp.I, -1)
    role_coefficient = sp.zeros(4)
    for i, j in combinations(range(4), 2):
        role_coefficient[roles[i], roles[j]] += direct[i] * inverse[j] / 2
        role_coefficient[roles[j], roles[i]] -= inverse[i] * direct[j] / 2
    commutator = sp.Matrix(6, 6, lambda i, j:
        orient(r, s) * pair(area, GEN[i] * GEN[j] - GEN[j] * GEN[i]))
    for target in range(4):
        for source in range(4):
            if role_coefficient[target, source]:
                H[6 * target:6 * target + 6,
                  6 * source:6 * source + 6] += (
                    role_coefficient[target, source] * commutator)
    for column in (u, v):
        for component in range(4):
            unit = sp.eye(4)[:, component]
            delta_area = (wedge(unit, S[:, v]) if column == u
                          else wedge(S[:, u], unit))
            for source in (r, s):
                weight = sum(direct[p] for p in range(4)
                             if roles[p] == source)
                for generator in range(6):
                    C[4 * column + component, 6 * source + generator] += (
                        weight * orient(r, s)
                        * pair(delta_area, GEN[generator]))

at_identity = {S[i, j]: int(i == j)
               for i in range(4) for j in range(4)}
at_standard = [[int(value) for value in t.subs(at_identity)]
               for t in TRIANGLES]
check("TRIANGLES_MATCH_FOUR_OWNED_CENTER_GENERATORS", at_standard == [
    [0, 0, 0, 1, -1, 1],
    [0, 1, -1, 0, 0, 1],
    [1, 0, -1, 0, 1, 0],
    [1, -1, 0, 1, 0, 0],
])

quarter = [OWNER.QI(Fraction(0), Fraction(1))] * 4
owner_h, owner_c = OWNER.flat_symbols(quarter)


def from_owner(value: OWNER.QI) -> sp.Expr:
    return sp.Rational(value.re.numerator, value.re.denominator) + (
        sp.I * sp.Rational(value.im.numerator, value.im.denominator))


check("SYMBOLIC_CONNECTION_BLOCK_MATCHES_LITERAL_FLAT_OWNER",
      H.subs(at_identity) == sp.Matrix([[from_owner(x) for x in row]
                                        for row in owner_h]))
gram_lift = sp.zeros(16, 10)
for metric_column, (a, b) in enumerate(OWNER.SYM):
    gram_lift[4 * b + a, metric_column] = sp.Rational(SIG[a], 2)
    gram_lift[4 * a + b, metric_column] = sp.Rational(SIG[b], 2)
check("UNRESTRICTED_COFRAME_ROWS_MATCH_LITERAL_GRAM_OWNER",
      gram_lift.T * C.subs(at_identity) ==
      sp.Matrix([[from_owner(x) for x in row] for row in owner_c]))

zero_connection, zero_coframe = 0, 0
for role, triangle_vector in enumerate(TRIANGLES):
    embedded = sp.zeros(24, 1)
    embedded[6 * role:6 * role + 6, 0] = triangle_vector
    h_output, c_output = H * embedded, C * embedded
    zero_connection += len(h_output)
    zero_coframe += len(c_output)
    check(f"ALL_24_CONNECTION_ROWS_ZERO_ON_ROLE_{role}",
          all(sp.expand(value) == 0 for value in h_output))
    check(f"ALL_16_COFRAME_ROWS_ZERO_ON_ROLE_{role}",
          all(sp.expand(value) == 0 for value in c_output))

flat_joint_rank = OWNER.elimination(owner_h + owner_c)[0]
check("FLAT_QUARTER_JOINT_RANK_20", flat_joint_rank == 20)
check("FULL_16_ROW_COFRAME_JOINT_RANK_20_AT_IDENTITY",
      H.subs(at_identity).col_join(C.subs(at_identity)).rank() == 20)
check("FOUR_TRIANGLES_ARE_INDEPENDENT_AT_IDENTITY",
      all(any(value for value in vector) for vector in at_standard))


def bracket(left: dict[str, Fraction], right: dict[str, Fraction]):
    words: dict[str, Fraction] = {}
    for a, alpha in left.items():
        for b, beta in right.items():
            words[a + b] = words.get(a + b, Fraction(0)) + alpha * beta
            words[b + a] = words.get(b + a, Fraction(0)) - beta * alpha
    return words


def quarter_log(role: int, phase: int) -> dict[str, Fraction]:
    letter = ("A" if phase % 2 == 0 else "B") + str(role)
    return {letter: Fraction(1 if phase < 2 else -1)}


mean_word_identity = {}
for r, s in PAIRS:
    mean: dict[str, Fraction] = {}
    for phase in range(4):
        logs = [quarter_log(r, phase), quarter_log(s, (phase + 1) % 4),
                {key: -value for key, value in
                 quarter_log(r, (phase + 1) % 4).items()},
                {key: -value for key, value in quarter_log(s, phase).items()}]
        for i, j in combinations(range(4), 2):
            for word, coefficient in bracket(logs[i], logs[j]).items():
                mean[word] = mean.get(word, Fraction(0)) + coefficient / 8
    mean = {word: value for word, value in mean.items() if value}
    expected = {
        f"A{r}B{r}": Fraction(-1, 2),
        f"B{r}A{r}": Fraction(1, 2),
        f"A{s}B{s}": Fraction(1, 2),
        f"B{s}A{s}": Fraction(-1, 2),
    }
    check(f"FREE_LIE_MEAN_QUARTER_FACE_{r}{s}", mean == expected)
    mean_word_identity[f"{r}{s}"] = {word: str(value)
                                        for word, value in sorted(mean.items())}

# Hostile control: quarter waves on a single role need not have zero metric
# mean when its cosine/sine generators fail to commute.  Put A_0=K1,
# B_0=K2, with all other amplitudes zero.  The free-Lie identity gives
# -[K1,K2]/2 on every (0,s) face.  The literal solder variation detects it.
hostile_bracket = GEN[0] * GEN[1] - GEN[1] * GEN[0]
hostile_coframe = sp.zeros(16, 1)
for r, s in PAIRS:
    if r != 0:
        continue
    u, v = [j for j in range(4) if j not in (r, s)]
    for column in (u, v):
        for component in range(4):
            unit = sp.eye(4)[:, component]
            delta_area = (wedge(unit, sp.eye(4)[:, v]) if column == u
                          else wedge(sp.eye(4)[:, u], unit))
            hostile_coframe[4 * column + component] -= (
                sp.Rational(1, 2) * orient(r, s)
                * pair(delta_area, hostile_bracket))
hostile_nonzero = {str(i): str(value)
                   for i, value in enumerate(hostile_coframe) if value}
check("NONCOMMUTING_SAME_ROLE_HOSTILE_METRIC_RESPONSE",
      hostile_nonzero == {"4": "1/2", "8": "-1/2"})
hostile_gram = gram_lift.T * hostile_coframe
check("NONCOMMUTING_HOSTILE_RESPONSE_SURVIVES_GRAM_QUOTIENT",
      any(value != 0 for value in hostile_gram))

result = {
    "schema": "a4d-identity-quarter-generic-coframe-response-v1",
    "background": "identity links, arbitrary constant 4x4 coframe symbols",
    "character": "(i,i,i,i) and real conjugate",
    "symbolic_coframe_variable_count": 16,
    "connection_shape": [24, 24],
    "coframe_mixed_shape": [16, 24],
    "triangle_generators_at_identity": at_standard,
    "symbolic_connection_zero_entries": zero_connection,
    "symbolic_coframe_zero_entries": zero_coframe,
    "joint_rank_at_identity": flat_joint_rank,
    "full_coframe_joint_rank_at_identity": 20,
    "generic_near_identity_joint_nullity": 4,
    "mean_quarter_free_lie_words": mean_word_identity,
    "noncommuting_same_role_hostile_coframe_mean": hostile_nonzero,
    "noncommuting_same_role_hostile_gram_mean": [str(v) for v in hostile_gram],
    "conclusion": (
        "On an open coframe neighborhood of eta the whole four-complex-"
        "dimensional diagonal-quarter joint kernel consists of one "
        "triangle-bivector line per role, and its zero-character quadratic "
        "metric response is identically zero."
    ),
    "proof_boundary": [
        "frozen constant coframes; no varying-background nonlinear gluing",
        "other Bloch characters and possible rank-drop coframes not classified",
        "no finite-amplitude or owner-sum response theorem",
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
print("TERMINAL A4D-IDENTITY-QUARTER-GENERIC-COFRAME-QUADRATIC-RESPONSE-NULL",
      flush=True)
