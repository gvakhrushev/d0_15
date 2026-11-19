#!/usr/bin/env python3
"""Exact native Golden CAR16 two-density phase atlas inverse.

Consumes original owner equation (17) at g0=1/4 and equation (18b) at
g=p^2; verifies the claimed six-source inverse and no fitted coefficient.
Does not assert that physical D0 selects or executes these readouts.
"""
import sympy as sp

r = sp.sqrt(5)
p = (r-1)/2
g = sp.simplify(p**2)

M = sp.Matrix([
    [0, 7, 0, 5, 4, 0],
    [0, -2, 0, 2, -2, 0],
    [2, 0, 6, 0, 0, 0],
    [-4, 0, 4, 0, 0, 8],
    [0, 5, 0, 7, 4, 0],
    [-6, 0, -2, 0, 0, 0],
])
A0 = M / 240

K = sp.zeros(6)
H = sp.zeros(6)
for i, j in [(0, 2), (1, 3)]:
    for a in range(6):
        K[a, i] = (A0[a, i]-A0[a, j])/2
        K[a, j] = -K[a, i]
        H[a, i] = (A0[a, i]+A0[a, j])/2
        H[a, j] = H[a, i]
for a in range(6):
    K[a, 4] = A0[a, 4]  # actual compact J23
    H[a, 5] = A0[a, 5]  # actual noncompact B
assert A0 == K+H

s2 = sp.simplify(g*g+(1-g)**2)
compact_ratio = sp.simplify((g*g/s2)/sp.Rational(1, 10))
boost_ratio = sp.simplify((g*(2*g-1)/s2)/sp.Rational(-1, 5))
assert sp.simplify(compact_ratio-(5-r)) == 0
assert sp.simplify(boost_ratio-(3*r-5)/2) == 0

A = (compact_ratio*K+boost_ratio*H).applyfunc(sp.simplify)
claimed_inverse = sp.Matrix([
    [0, 0, 3*r, 0, 0, -15-6*r],
    [40+18*r, 20+12*r, 0, 0, -30-12*r, 0],
    [0, 0, 15+6*r, 0, 0, -3*r],
    [10+12*r, 20+12*r, 0, 0, -6*r, 0],
    [-30-6*r, -30-6*r, 0, 0, 30+6*r, 0],
    [0, 0, -15-9*r, 15+9*r, 0, -15-9*r],
])
assert (A*claimed_inverse-sp.eye(6)).applyfunc(sp.simplify) == sp.zeros(6)
assert (claimed_inverse*A-sp.eye(6)).applyfunc(sp.simplify) == sp.zeros(6)
assert sp.simplify(A.det()-p**9/sp.Integer(15552000)) == 0

row_max = 90+42*r
for i in range(6):
    abs_sum = sum(abs(float(claimed_inverse[i, j])) for j in range(6))
    assert abs_sum <= float(row_max)+1e-12
assert sp.simplify((claimed_inverse[1, 0]
      +claimed_inverse[1, 1]-claimed_inverse[1, 4])-row_max) == 0
assert float(row_max)<185

print("PASS exact original Golden six-generator/source inverse")
print("det D_phase =", sp.simplify(A.det()))
print("||D_phase^-1||_infty =", row_max, "~", float(row_max))
print("No seventh scalar needed for LOCAL smooth Lorentz recovery;")
print("physical native admission/price, source and GR remain open.")
