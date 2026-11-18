"""Rooted K(9,11,13) central histories, two existing tariffs, and their pressures."""
from collections import Counter
from itertools import product

import sympy as sp


vertices = range(33)
u, x = sp.symbols("u x", positive=True)
p = (sp.sqrt(5) - 1) / 2
zones = [0] * 9 + [1] * 11 + [2] * 13
cells = [[0], list(range(1, 9)), [9], list(range(10, 20)), list(range(20, 33))]


def legal(i, j):
    return zones[i] != zones[j]


def sign(i, j):
    return -1 if {i, j} == {0, 9} else 1


def weight(i, j, twist, mark):
    if not legal(i, j):
        return 0
    return (sign(i, j) if twist else 1) * (mark if (i, j) == (0, 9) else 1)


triangles = Counter()
for i, j in product(vertices, repeat=2):
    edges = [(0, i), (i, j), (j, 0)]
    if all(legal(a, b) for a, b in edges):
        parity = sp.prod(sign(a, b) for a, b in edges)
        triangles[parity, edges.count((0, 9))] += 1
assert triangles == {(1, 0): 260, (-1, 0): 13, (-1, 1): 13}
a, b = 260, 13 * (1 + u)
regular = a**2 + b**2
spin = (a - b)**2
odd_fraction = spin / (2 * regular)
for f, direction in [(regular, 1), (spin, -1), (odd_fraction, -1)]:
    assert sp.simplify(direction * (f.subs(u, 1) - f.subs(u, p))).is_positive

# Entropy in natural units here. Multiplication by ln(phi) converts Golden units
# to natural units. The Golden splitter contributes h conditionally on a minus loop.
h = sp.symbols("h", positive=True)
z = a + b
total_info = sp.log(z) - (13 * u / z) * sp.log(u) + b / z * h
uniform_path_mass = 1 / z
raised_path_mass = u / z
direct_info = (-273 * uniform_path_mass * sp.log(uniform_path_mass)
               - 13 * raised_path_mass * sp.log(raised_path_mass) + b / z * h)
assert sp.simplify(sp.expand_log(direct_info - total_info)) == 0
edge_cost_in_nats = -6 * sp.log(p) - 13 * u / z * sp.log(u)
rate = edge_cost_in_nats - total_info
assert sp.simplify(rate.diff(u) + 1 / (21 + u) + 20 * h / (21 + u)**2) == 0
assert sp.simplify(total_info.diff(u) - (20 * h - 21 * sp.log(u)) / (21 + u)**2) == 0
assert sp.simplify(4 * p**3 + p**6 - 1) == 0

# Arbitrary stationary conditional archive corrections, in natural units.
t, g0, g1 = sp.symbols("t g0 g1", positive=True)
transport = (g0 + t * (g1 - g0))
edge_minus_path_entropy = -6 * sp.log(p) - sp.log(z)
total_t = -6 * sp.log(p) - sp.log(273) + sp.log(1 - t) + transport
assert sp.simplify(sp.logcombine(
    (total_t - transport).subs(t, u / (21 + u)) - edge_minus_path_entropy,
    force=True)) == 0
assert sp.simplify(total_t.diff(t, 2) + 1 / (1 - t)**2) == 0
t1, tp = sp.Rational(1, 22), p / (21 + p)
assert sp.simplify(transport.subs(t, tp) - transport.subs(t, t1)
                   - (tp - t1) * (g1 - g0)) == 0

# The signed-cover support is primitive: every state is reachable from (0,+)
# and the undirected support has both a 2-return and a positive 3-return there.
seen = {(0, 1)}
front = set(seen)
while front:
    front = {(j, parity * sign(i, j)) for i, parity in front
             for j in vertices if legal(i, j)} - seen
    seen.update(front)
assert len(seen) == 66 and sign(0, 9) * sign(9, 0) == 1
assert sign(0, 10) * sign(10, 20) * sign(20, 0) == 1

members = sp.Matrix([[int(i in cell) for cell in cells] for i in vertices])
bounds = {}
for twist in [False, True]:
    s = -1 if twist else 1
    reduced = sp.Matrix([[0, 0, s*u, 10, 13], [0, 0, 1, 10, 13], [s, 8, 0, 0, 13],
                         [1, 8, 0, 0, 13], [1, 8, 1, 10, 0]])
    assert sp.expand((reduced**3)[0, 0] - (a + s*b)) == 0
    assert sp.expand((reduced**2)[0, 0] - (23 + u)) == 0
    for endpoint in (0, 1):
        matrix = sp.Matrix([[weight(i, j, twist, endpoint) for j in vertices] for i in vertices])
        assert matrix * members == members * reduced.subs(u, endpoint)
        square = matrix**2
        assert min(square) >= 5
        # Each 2-walk uses the sole directed marked edge at most once, so
        # all square entries and all entrywise comparisons interpolate affinely.
        assert square[0, 20] == 10 + s * endpoint
    f = reduced.charpoly("t").as_expr().subs(sp.Symbol("t"), x)
    roots = sp.Poly(f.subs(u, 1), x).sqf_part().intervals(eps=sp.Rational(1, 10**12))
    low, high = roots[-1][0]
    bounds[s] = (low, high)
    mid = (low + high) / 2
    slope = -f.diff(u).subs({x: mid, u: 1}) / (mid * f.diff(x).subs({x: mid, u: 1}))
    assert s * slope > 0
    print(f"sector {s:+d}: lambda(1)={float(mid):.10f}, d log(lambda)/du={float(slope):+.10f}")

even_lo, even_hi = bounds[1]
odd_lo, odd_hi = bounds[-1]
assert sp.Rational(989, 1000) < (odd_lo / even_hi)**2
assert (odd_hi / even_lo)**2 < sp.Rational(990, 1000)
print("286 rooted triangles, paid edge mark; finite cut signs and full classical entropy verified.")
print("66-state cover primitive; 33-site square and 5-cell quotient verified; leakage base in (0.989,0.990).")
