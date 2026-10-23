#!/usr/bin/env python3
"""Exact unrestricted first variation of the original-face curvature square.

No external dependency. Fraction arithmetic differentiates every based face
containing a varied link, before evaluating on the Brinkmann configuration.
This is a targeted check of the new Q_h identity, not a replay of the owned
Palatini/Golden-J2 all40 theorem. See the accompanying recovery memo, section 10.
"""
from fractions import Fraction as F
from itertools import combinations, product
import json


def zero():
    return [[F(0) for _ in range(4)] for _ in range(4)]


def eye():
    return [[F(i == j) for j in range(4)] for i in range(4)]


def add(a, b):
    return [[a[i][j] + b[i][j] for j in range(4)] for i in range(4)]


def scale(c, a):
    return [[c * v for v in row] for row in a]


def mm(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(4))
             for j in range(4)] for i in range(4)]


def transpose(a):
    return [list(row) for row in zip(*a)]


def trace(a):
    return sum(a[i][i] for i in range(4))


I, Z = eye(), zero()
ETA = [[F(0), F(1), F(0), F(0)],
       [F(1), F(0), F(0), F(0)],
       [F(0), F(0), F(-1), F(0)],
       [F(0), F(0), F(0), F(-1)]]
N = []
for a in (2, 3):
    n = zero()
    n[1][a] = n[a][0] = F(1)
    N.append(n)
GENERATORS = []
for a, b in combinations(range(4), 2):
    lower = zero()
    lower[a][b], lower[b][a] = F(1), F(-1)
    x = mm(ETA, lower)
    assert add(mm(transpose(x), ETA), mm(ETA, x)) == Z
    GENERATORS.append((f"{a}{b}", x))
FACES = list(combinations(range(4), 2))
PAIRS = [(r, s) for r in range(4) for s in range(4) if r != s]


def shift(z, a, n=1):
    v = list(z)
    v[a] += n
    return tuple(v)


class Configuration:
    def __init__(self, h, hostile=False, weighted=False):
        self.h, self.hostile, self.weighted = h, hostile, weighted

    def coordinates(self, z):
        return tuple(self.h * F(i) for i in z)

    def profile(self, z):
        u, _, x, y = self.coordinates(z)
        if self.hostile:
            return x**4
        h = self.h
        # Nonzero, time-dependent Ricci plus harmonic degrees 2, 3, 4, 6.
        # The real quartic and sextic need genuine mesh-dependent corrections.
        w4 = x**4 - 6*x*x*y*y + y**4 - h*h*(x*x+y*y)
        w6 = (x**6 - 15*x**4*y*y + 15*x*x*y**4 - y**6
              - 5*h*h*(x**4-y**4))
        return ((1+u*u)*(x*x+y*y) + (1+u)*(x*x-y*y)
                + (2-u)*x*y + (1+u**3)*(x**3-3*x*y*y)/7
                + (1-u*u)*(3*x*x*y-y**3)/11
                + (1+u)*x*y*(x*x-y*y)/13 + w4/17 + w6/19)

    def k(self, z):
        z1 = shift(z, 0)
        a = (self.profile(z1)-self.profile(shift(z1, 2, -1)))/2
        b = (self.profile(z1)-self.profile(shift(z1, 3, -1)))/2
        return add(scale(a, N[0]), scale(b, N[1]))

    def link(self, z, direction, inverse=False):
        if direction != 0:
            return I
        k = self.k(z)
        return add(add(I, scale(-1 if inverse else 1, k)),
                   scale(F(1, 2), mm(k, k)))

    def coframe(self, z):
        e = eye()
        e[1][0] = self.profile(z)/2
        return e

    def inverse_coframe(self, z):
        e = eye()
        e[1][0] = -self.profile(z)/2
        return e

    def inverse_metric(self, z):
        ei = self.inverse_coframe(z)
        return mm(mm(ei, ETA), transpose(ei))

    def weight(self, z):
        return 1+self.coordinates(z)[2]/10 if self.weighted else F(1)

    def face(self, z, r, s, variation=None):
        # The four exact factors and their derivatives, at a fixed background.
        factors = [(z, r, False), (shift(z, r), s, False),
                   (shift(z, s), r, True), (z, s, True)]
        p, dp = I, Z
        for loc, direction, inverse in factors:
            a = self.link(loc, direction, inverse)
            da = Z
            if variation is not None:
                target, target_direction, x = variation
                if loc == target and direction == target_direction:
                    da = scale(-1, mm(a, x)) if inverse else mm(x, a)
            dp, p = add(mm(dp, a), mm(p, da)), mm(p, a)
        # P^{-1}=eta P^T eta, since every background factor is proper Lorentz.
        pi = mm(mm(ETA, transpose(p)), ETA)
        assert mm(p, pi) == I
        curvature = scale(1/(2*self.h**2), add(p, scale(-1, pi)))
        derivative = scale(1/(2*self.h**2), add(dp, mm(mm(pi, dp), pi)))
        return curvature, derivative

    def faces(self, z, variation=None):
        fields, derivatives = {}, {}
        for r, s in FACES:
            f, df = self.face(z, r, s, variation)
            fields[r, s], fields[s, r] = f, scale(-1, f)
            derivatives[r, s], derivatives[s, r] = df, scale(-1, df)
        return fields, derivatives


def contraction(a, b, gi, gj):
    value = F(0)
    for r, s in PAIRS:
        for t, w in PAIRS:
            coefficient = gi[r][t] * gj[s][w]
            if coefficient:
                value += coefficient * trace(mm(a[r, s], b[t, w]))
    return value


def link_row(config, target, direction, generator):
    sites = {target}
    sites.update(shift(target, a, -1) for a in range(4) if a != direction)
    total = F(0)
    for z in sites:
        fields, derivatives = config.faces(z, (target, direction, generator))
        gi = config.inverse_metric(z)
        total += (config.weight(z)*config.h**4/2
                  * contraction(derivatives, fields, gi, gi))
    return total


def coframe_rows(config, z):
    fields, _ = config.faces(z)
    e, ei, gi = config.coframe(z), config.inverse_coframe(z), config.inverse_metric(z)
    invariant = contraction(fields, fields, gi, gi)
    rows = []
    for a, r in product(range(4), repeat=2):
        de = zero()
        de[a][r] = F(1)
        dg = add(mm(mm(transpose(de), ETA), e), mm(mm(transpose(e), ETA), de))
        dgi = scale(-1, mm(mm(gi, dg), gi))
        ddet = trace(mm(ei, de))
        rows.append(config.weight(z)*config.h**4/4 * (
            ddet*invariant + contraction(fields, fields, dgi, gi)
            + contraction(fields, fields, gi, dgi)))
    return invariant, rows


def predicted_v_row(config, z, x):
    divergence = zero()
    for a in (2, 3):
        f, _ = config.face(z, 0, a)
        zm = shift(z, a, -1)
        fm, _ = config.face(zm, 0, a)
        divergence = add(divergence, add(scale(config.weight(zm), fm),
                                        scale(-config.weight(z), f)))
    return config.h**2 * trace(mm(divergence, x))


def verify(config, z):
    invariant, solder = coframe_rows(config, z)
    assert invariant == 0 and all(v == 0 for v in solder)
    rows = []
    for direction, (name, x) in product(range(4), GENERATORS):
        value = link_row(config, z, direction, x)
        expected = predicted_v_row(config, z, x) if direction == 1 else F(0)
        assert value == expected, (direction, name, value, expected)
        rows.append(value)
    return rows


def main():
    cases = []
    for h, z in [(F(1), (0, 0, 0, 0)),
                 (F(1, 3), (2, 1, -1, 2))]:
        rows = verify(Configuration(h), z)
        assert all(v == 0 for v in rows)
        cases.append({"h": str(h), "site": z, "coframe_rows": 16,
                      "independent_link_rows": 24, "exact_residual": "0"})
    hostile = verify(Configuration(F(1), hostile=True), (0, 0, 0, 0))
    assert any(hostile)
    weighted = verify(Configuration(F(1, 3), weighted=True), (2, 0, 1, -1))
    assert any(weighted)
    # The designated opposite-null generator gives exactly -12 at h=1,x=0.
    m2 = zero()
    m2[0][2] = m2[2][1] = F(1)
    hostile_value = link_row(Configuration(F(1), hostile=True),
                             (0, 0, 0, 0), 1, m2)
    assert hostile_value == -12
    # A fixed Dirichlet collar alone is insufficient for the enlarged stencil.
    # The original Poisson equation holds at x=1,2, but fails at collar x=0.
    class BoundaryConfiguration(Configuration):
        def profile(self, z):
            return F(3, 5) if z[2] == -1 else F(0)
    boundary = BoundaryConfiguration(F(1))
    for coordinate in (1, 2):
        center = (0, 0, coordinate, 0)
        assert sum(boundary.profile(shift(center, a, sign))
                   for a in (2, 3) for sign in (-1, 1)) - 4*boundary.profile(center) == 0
    boundary_rows = verify(boundary, (0, 0, 1, 0))
    assert any(boundary_rows)
    boundary_value = link_row(boundary, (0, 0, 1, 0), 1, m2)
    assert boundary_value == -F(3, 5)
    print(json.dumps({"status": "PASS", "arithmetic": "Fraction, exact",
                      "on_shell": cases,
                      "hostile_H_x4_Q_density": "0",
                      "hostile_H_x4_opposite_null_row": str(hostile_value),
                      "nonuniform_weight_nonzero_rows": [str(v) for v in weighted if v],
                      "incompatible_collar_opposite_null_row": str(boundary_value),
                      "scope": "Q_h unrestricted first source only; no native full-price identification"},
                     indent=2))


if __name__ == "__main__":
    main()
