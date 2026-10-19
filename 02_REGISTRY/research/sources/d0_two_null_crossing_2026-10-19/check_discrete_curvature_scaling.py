#!/usr/bin/env python3
"""Exact stencil check for raw and area-normalized plaquette curvature."""

import sympy as s

h, x, y = s.symbols("h x y", nonzero=True)
H = s.Function("H")

k2 = (H(x, y) - H(x - h, y)) / (2 * h)
k3 = (H(x, y) - H(x, y - h)) / (2 * h)
raw = s.Matrix([
    [k2 - k2.subs(x, x + h), k3 - k3.subs(x, x + h)],
    [k2 - k2.subs(y, y + h), k3 - k3.subs(y, y + h)],
])
lap = (
    H(x + h, y) + H(x - h, y) + H(x, y + h) + H(x, y - h)
    - 4 * H(x, y)
) / h**2

assert s.simplify(s.trace(raw) + h * lap / 2) == 0

# The finite Euler row carries h^3, so its trace representation uses the
# area-normalized curvature h times the raw logarithmic plaquette coefficient.
curvature = h * raw
euler = -h**3 * lap / 2
assert s.simplify(euler - h * s.trace(curvature)) == 0
assert s.simplify(-s.trace(curvature) / h**2 - lap / 2) == 0

W = x**3 - 3 * x * y**2
w2 = (W - W.subs(x, x - h)) / (2 * h)
w3 = (W - W.subs(y, y - h)) / (2 * h)
raw_weyl = s.Matrix([
    [w2 - w2.subs(x, x + h), w3 - w3.subs(x, x + h)],
    [w2 - w2.subs(y, y + h), w3 - w3.subs(y, y + h)],
])
expected = h**2 * s.Matrix([
    [-3 * x, 3 * y - s.Rational(3, 2) * h],
    [3 * y + s.Rational(3, 2) * h, 3 * x],
])
assert (h * raw_weyl).applyfunc(s.expand) == expected.applyfunc(s.expand)
assert s.simplify(s.trace(raw_weyl)) == 0
assert raw_weyl != s.zeros(2)

lam, energy, nsites, delta = s.symbols("lambda energy nsites delta")
area = h**2 * nsites
source_flux = nsites * (-h**2 * delta / 2).subs(delta, -4 * lam * energy)
assert s.simplify(source_flux - 2 * lam * energy * area) == 0

print("PASS: raw plaquette-log trace = -h/2 times the standard central Laplacian")
print("PASS: area-normalized curvature gives the exact surviving Euler-row scaling")
print("PASS: cubic discrete harmonic has zero trace and nonzero Weyl matrix")
print("PASS: summed normalized trace has the stated area-scaled source")
print("SCOPE: normalization and stencil identities only; no full native readout or GR closure")
