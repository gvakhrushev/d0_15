"""Verify the positive table family, centre derivative and absolute-arm decoder."""
from fractions import Fraction as F

import sympy as sp


def tilt(table, factor):
    shifted = []
    for plus, minus in zip(*table):
        total = plus + minus
        weighted = factor * plus + minus
        shifted.append((total * factor * plus / weighted, total * minus / weighted))
    return tuple(zip(*shifted))


def odds(table, first, second):
    plus, minus = table
    return plus[first] * minus[second] / (plus[second] * minus[first])


pi, q, delta_plus, delta_minus, slope = sp.symbols(
    "pi q delta_plus delta_minus slope", nonzero=True)
t = sp.Symbol("t")
positive = q + t * delta_plus
negative = q + t * delta_minus
reference = ((pi * positive, pi * (1 - positive)),
             ((1 - pi) * negative, (1 - pi) * (1 - negative)))
candidate = tilt(reference, 1 + t * slope)


def first(expr):
    return sp.factor(sp.diff(expr, t).subs(t, 0))


for before, after in zip(reference, candidate):
    for b in range(2):
        assert first(after[b] / sum(after) - before[b] / sum(before)) == 0
row_plus, row_minus = (sum(row) for row in candidate)
assert sp.simplify(first(row_plus) - pi * (1 - pi) * slope) == 0
assert sp.simplify(first(sp.log(row_plus / row_minus)) - slope) == 0
assert sp.simplify(first(candidate[0][0] - reference[0][0]) -
                   pi * (1 - pi) * q * slope) == 0
p = (sp.sqrt(5) - 1) / 2
assert sp.simplify(p * (1 - p) * p**2 - p**5) == 0 and p**5 > 0

# Non-identical arms, arbitrary finite recorded output, exact noninfinitesimal tilt.
journal = ((F(2, 17), F(4, 17), F(3, 17)),
           (F(5, 17), F(2, 17), F(1, 17)))
for factor in (F(1, 31), F(7, 3), F(12)):
    moved = tilt(journal, factor)
    assert sum(map(sum, moved)) == 1
    assert all(sum(c) == sum(d) for c, d in zip(zip(*journal), zip(*moved)))
    for i, j in ((0, 1), (1, 2), (0, 2)):
        assert odds(moved, i, j) == odds(journal, i, j)
    assert sum(moved[0]) != sum(journal[0])

# Recovery from one genuinely joint cell; every permitted s is attained.
c, r, s = sp.symbols("c r s", positive=True)
plus0 = s * (1 - c) / (s + r * (c - s))
restored = ((s, plus0), (c - s, 1 - c - plus0))
assert sp.factor(odds(restored, 0, 1) - r) == 0
assert sp.factor(sp.diff(sum(restored[0]), s) - 1 -
                 c * r * (1 - c) / (s + r * (c - s))**2) == 0
assert sum(restored[0]).subs(s, 0) == 0
assert sp.simplify(sum(restored[0]).subs(s, c) - 1) == 0
print("PASS: all late marginals and odds preserved, arm first jets agree, "
      "absolute differential arbitrary, one joint cell recovers it.")
