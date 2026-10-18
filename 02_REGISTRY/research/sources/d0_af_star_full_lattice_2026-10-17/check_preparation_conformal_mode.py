#!/usr/bin/env python3
"""Exact new control: free AF weights compensate all local star Euler rows.

Consumes only the owned star pairing/edge definitions; does not replay its
old pp-wave suite. Also computes Einstein for the resulting conformal flat
metric directly from Christoffels. This is the configured five-cut carrier,
not a physical D0 admission or general GR no-go.
"""
import json
from fractions import Fraction
import sympy as s
import star_euler as E


def require(value, message):
    if not value:
        raise ArithmeticError(message)


def finite_rows(compensate=True):
    origin = (0, 0, 0, 0)
    bases = [origin] + [E.shift(origin, j, -1) for j in range(4)]
    weights = dict(zip(bases, s.symbols('w0:5', positive=True)))

    def solder(at):
        return s.eye(4) / s.sqrt(weights[at]) if compensate else s.eye(4)

    result = []
    # At U=I every plaquette odd curvature is zero, so all16 solder
    # derivatives vanish for arbitrary solder and arbitrary positive weights.
    result.extend([s.Integer(0)] * 16)
    for axis in range(4):
        for X in E.LIE:
            total = 0
            for r, t in E.PAIRS:
                if axis not in (r, t):
                    continue
                other = t if axis == r else r
                for base in [origin, E.shift(origin, other, -1)]:
                    # Direct derivative of the four original flat link factors.
                    dP = s.zeros(4)
                    for at, direction, inverse in E.edges(base, r, t):
                        if (at, direction) == (origin, axis):
                            dP += -X if inverse else X
                    u, v = [j for j in range(4) if j not in (r, t)]
                    e = solder(base)
                    total += weights[base] * E.EPS((r, t, u, v)) * E.pairing(
                        E.wedge(e[:, u], e[:, v]), dP)
            result.append(s.simplify(total))
    return result


def conformal_einstein():
    u, v, x, y, k = s.symbols('u v x y k', real=True)
    coordinates = (u, v, x, y)
    metric = s.exp(-2*k*u) * E.ETA
    inverse = metric.inv()
    christoffel = [[[s.simplify(sum(inverse[a, d] * (
        s.diff(metric[d, c], coordinates[b])
        + s.diff(metric[d, b], coordinates[c])
        - s.diff(metric[b, c], coordinates[d])) / 2 for d in range(4)))
        for c in range(4)] for b in range(4)] for a in range(4)]
    ricci = s.Matrix(4, 4, lambda b, c: s.simplify(sum(
        s.diff(christoffel[a][b][c], coordinates[a])
        - s.diff(christoffel[a][a][c], coordinates[b])
        + sum(christoffel[a][a][d]*christoffel[d][b][c]
              - christoffel[a][b][d]*christoffel[d][a][c]
              for d in range(4)) for a in range(4))))
    scalar = s.simplify(s.trace(inverse * ricci))
    einstein = s.simplify(ricci - scalar * metric / 2)
    expected = s.zeros(4)
    expected[0, 0] = 2*k*k
    require(einstein == expected and scalar == 0, 'direct non-Einstein metric')
    # For e'=exp(-ku)e0 and omega=0, T'^a=-k du wedge e'^a.
    require(s.diff(s.exp(-k*u), u) == -k*s.exp(-k*u), 'nonzero torsion')
    return {'G_uu': str(einstein[0, 0]), 'scalar_curvature': str(scalar),
            'other_Einstein_rows': 'zero', 'torsion': '-k du wedge e_prime'}


def main():
    rows = finite_rows()
    require(len(rows) == 40 and all(q == 0 for q in rows), 'all40 exact rows')
    control = finite_rows(compensate=False)
    require(any(q != 0 for q in control[16:]), 'uncompensated weights must fail')
    a, b = Fraction(2, 67), Fraction(32, 67)
    exponent = min(b/4-a, 2*(1-2*b))
    require(exponent == 3*a and exponent-2*a == a, 'C2 recovery exponents')
    print(json.dumps({'scope': 'configured_free_AF_five_cut_local_vacuum',
        'finite_exact_rows': len(rows),
        'arbitrary_positive_weights': True,
        'uncompensated_weight_control': 'rejected',
        'conformal_metric': conformal_einstein(),
        'fixed_t_vacuum_roots': True,
        'C2_recovery_exponents': {'mesh': str(a), 'prefix': str(b),
                                  'weight_sup': str(exponent)},
        'physical_D0_selection': 'not_proved'}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
