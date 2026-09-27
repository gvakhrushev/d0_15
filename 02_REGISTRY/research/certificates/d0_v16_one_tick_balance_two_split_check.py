#!/usr/bin/env python3
"""Exact finite certificate for the D0 v16 one-tick balance owner.

All arithmetic is fractions.Fraction.  The positive witness deliberately uses
rank(P)=2 and rank(Q)=3.  Hostile controls include sector preservation,
nonunitarity, and Q-sector identity padding.
"""
from __future__ import annotations

from fractions import Fraction as F


def q(x):
    return x if isinstance(x, F) else F(x)


def mat(rows):
    return [[q(x) for x in row] for row in rows]


def transpose(a):
    return [list(row) for row in zip(*a)]


def mm(a, b):
    assert len(a[0]) == len(b)
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
    assert len(a) == len(a[0])
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


def channel_data(u, r):
    a, b, c, d = block(u, r)
    leak = trace(gram(c))
    emit = trace(gram(b))
    retained = trace(gram(a))
    archived = trace(gram(d))
    return a, b, c, d, leak, emit, retained, archived


# Unequal-rank positive witness: P has rank 2, Q has rank 3.
c1, s1 = F(3, 5), F(4, 5)
c2, s2 = F(5, 13), F(12, 13)
u = mat(
    [
        [c1, 0, -s1, 0, 0],
        [0, c2, 0, -s2, 0],
        [s1, 0, c1, 0, 0],
        [0, s2, 0, c2, 0],
        [0, 0, 0, 0, 1],
    ]
)
assert is_orthogonal(u)
a, b, c, d, leak, emit, retained, archived = channel_data(u, 2)

expected_channel = F(6304, 4225)
expected_retained = F(2146, 4225)
assert leak == expected_channel
assert emit == expected_channel
assert retained == expected_retained
assert retained + leak == 2
assert archived + emit == 3
assert (emit - leak) == 0

# P <-> Q companion identities.
assert emit == F(3) - archived
assert leak == F(2) - retained

# Sector-preserving hostile control.
identity = eye(5)
_, _, _, _, leak_i, emit_i, retained_i, archived_i = channel_data(identity, 2)
assert leak_i == emit_i == 0
assert retained_i == 2
assert archived_i == 3

# Deliberately nonunitary hostile control: C != 0 but B = 0.
bad = eye(5)
bad[2][0] = F(1)
assert not is_orthogonal(bad)
_, _, _, _, leak_bad, emit_bad, _, _ = channel_data(bad, 2)
assert leak_bad == 1
assert emit_bad == 0
assert leak_bad != emit_bad

# Q-padding control: add one identity spectator to Q.
u_pad = [row + [F(0)] for row in u] + [[F(0)] * 5 + [F(1)]]
assert is_orthogonal(u_pad)
_, _, _, _, leak_p, emit_p, retained_p, archived_p = channel_data(u_pad, 2)
assert leak_p == leak
assert emit_p == emit
assert retained_p == retained
assert retained_p + leak_p == 2
assert archived_p + emit_p == 4

print("rank(P)=2 rank(Q)=3")
print("Tr F_N =", leak)
print("Tr F_Q_emit =", emit)
print("Tr A^*A =", retained)
print("P budget =", retained + leak)
print("Q budget =", archived + emit)
print("nonunitary hostile traces =", leak_bad, emit_bad)
print("D0-V16-ONE-TICK-BALANCE-OWNER-CERTIFIED")
