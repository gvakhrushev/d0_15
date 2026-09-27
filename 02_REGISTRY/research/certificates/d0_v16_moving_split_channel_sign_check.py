#!/usr/bin/env python3
"""Exact certificate for a nontrivial D0 v16 history channel sign.

The carrier has equal-rank P and Q sectors.  Every individual unitary tick has
zero unrestricted global sign; a nonzero sign appears only when two frozen
history points are compared.  All arithmetic is fractions.Fraction.
"""
from __future__ import annotations

from fractions import Fraction as F


def mat(rows):
    return [[x if isinstance(x, F) else F(x) for x in row] for row in rows]


def transpose(a):
    return [list(row) for row in zip(*a)]


def mm(a, b):
    return [
        [
            sum((a[i][k] * b[k][j] for k in range(len(b))), F(0))
            for j in range(len(b[0]))
        ]
        for i in range(len(a))
    ]


def eye(n):
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]


def trace(a):
    return sum((a[i][i] for i in range(len(a))), F(0))


def gram(a):
    return mm(transpose(a), a)


def block(u, r):
    return (
        [row[:r] for row in u[:r]],
        [row[r:] for row in u[:r]],
        [row[:r] for row in u[r:]],
        [row[r:] for row in u[r:]],
    )


def is_orthogonal(u):
    return mm(transpose(u), u) == eye(len(u)) and mm(u, transpose(u)) == eye(len(u))


def make_tick(c1, s1, c2, s2):
    return mat(
        [
            [c1, 0, -s1, 0],
            [0, c2, 0, -s2],
            [s1, 0, c1, 0],
            [0, s2, 0, c2],
        ]
    )


def channels(u, r=2):
    _, b, c, _ = block(u, r)
    return trace(gram(c)), trace(gram(b))


def sign(a, b):
    return F(0) if a + b == 0 else (b - a) / (b + a)


# Frozen equal-rank split and full-sector windows:
# Pi_in=P, Pi_out=Q, rank 2 each.
u_n = make_tick(F(4, 5), F(3, 5), F(12, 13), F(5, 13))
u_np = make_tick(F(3, 5), F(4, 5), F(12, 13), F(5, 13))
assert is_orthogonal(u_n)
assert is_orthogonal(u_np)

leak_n, emit_n = channels(u_n)
leak_np, emit_np = channels(u_np)

# Same-tick global sign is zero at both history points.
assert leak_n == emit_n == F(2146, 4225)
assert leak_np == emit_np == F(3329, 4225)
assert sign(leak_n, emit_n) == 0
assert sign(leak_np, emit_np) == 0

# History comparison.
a_n = leak_n
b_np = emit_np
sigma_budget = sign(a_n, b_np)
assert sigma_budget == F(1183, 5475)
assert sigma_budget > 0

# Equal-rank density normalization.
rank_in = rank_out = F(2)
a_density = a_n / rank_in
b_density = b_np / rank_out
sigma_density = sign(a_density, b_density)
assert sigma_density == sigma_budget

# History-covariant P<->Q swap and time reversal.
# Reblocking after P<->Q exchanges leak and emission.  We compute from the
# original channel data at reversed times, not by negating sigma_budget.
swapped_input_leak = emit_np
swapped_output_emit = leak_n
sigma_swapped = sign(swapped_input_leak, swapped_output_emit)
assert sigma_swapped == -sigma_budget

# Sector-preserving history: both budgets vanish.
ident = eye(4)
leak_i, emit_i = channels(ident)
assert leak_i == emit_i == 0
assert sign(leak_i, emit_i) == 0

# No temporal change: nonzero channels but zero history sign.
assert sign(leak_n, emit_n) == 0

# The unchanged second channel is an exact spectator.  The numerator comes
# only from 16/25 - 9/25 = 7/25; its 25/169 contribution cancels.
assert (b_np - a_n) == F(7, 25)

print("one-tick n traces =", leak_n, emit_n)
print("one-tick n' traces =", leak_np, emit_np)
print("history budget sign =", sigma_budget)
print("history density sign =", sigma_density)
print("history-swapped sign =", sigma_swapped)
print("D0-V16-MOVING-SPLIT-CHANNEL-SIGN-CERTIFIED")
