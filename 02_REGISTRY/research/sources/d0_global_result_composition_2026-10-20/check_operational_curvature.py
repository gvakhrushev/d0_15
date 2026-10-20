#!/usr/bin/env python3
"""Exact, read-only checks of the NEW probability/curvature composition."""
from fractions import Fraction as F
import json


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def inverse_det(matrix):
    n = len(matrix)
    rows = [
        list(map(F, row)) + [F(i == j) for j in range(n)]
        for i, row in enumerate(matrix)
    ]
    determinant = F(1)
    for j in range(n):
        pivot = next((i for i in range(j, n) if rows[i][j]), None)
        require(pivot is not None, "singular evaluation map")
        if pivot != j:
            rows[pivot], rows[j] = rows[j], rows[pivot]
            determinant = -determinant
        diagonal = rows[j][j]
        determinant *= diagonal
        rows[j] = [v / diagonal for v in rows[j]]
        for i in range(n):
            if i != j:
                factor = rows[i][j]
                rows[i] = [a - factor * b for a, b in zip(rows[i], rows[j])]
    return [row[n:] for row in rows], determinant


def basis5(x, y):
    return [x*x+y*y, x*x-y*y, 2*x*y,
            x**3-3*x*y*y, 3*x*x*y-y**3]


def basis9(x, y):
    return [1, x, y] + basis5(x, y) + [x*y*(x*x-y*y)]


def mm(a, b):
    return [[sum(x*y for x, y in zip(row, col))
             for col in zip(*b)] for row in a]


def B(t):
    return 4*t*t*(1-t*t)


def main():
    points5 = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1)]
    m5 = [basis5(*z) for z in points5]
    inv5, det5 = inverse_det(m5)
    expected5 = [
        [F(1, 4), F(1, 4), F(1, 4), F(1, 4), 0],
        [F(1, 4), F(1, 4), F(-1, 4), F(-1, 4), 0],
        [F(1, 4), F(-3, 4), F(1, 4), F(-3, 4), F(1, 2)],
        [F(1, 2), F(-1, 2), 0, 0, 0],
        [0, 0, F(-1, 2), F(1, 2), 0],
    ]
    require(inv5 == expected5, "five-profile inverse differs from proof")
    require(det5 == -16, "five-profile determinant")

    points9 = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1),
               (2, 0), (0, 2), (1, 1), (1, 2)]
    m9 = [basis9(*z) for z in points9]
    inv9, det9 = inverse_det(m9)
    require(det9 == 3456, "nine-profile determinant")
    require(mm(inv9, m9) == [[F(i == j) for j in range(9)]
                              for i in range(9)], "inverse identity")
    rowsums = [sum(map(abs, row)) for row in inv9]
    expected_sums = [1, 2, 2, 2, 1, 6, F(4, 3), F(4, 3), 2]
    require(rowsums == expected_sums, "nine-profile error constants")

    # Column homogeneity proves the displayed all-a inverses. These exact
    # nonunit controls catch an omitted a^degree in the implemented decoder.
    degrees = [0, 1, 1, 2, 2, 2, 3, 3, 4]
    coefficients = [F(2, 7), F(-1, 9), F(3, 11), F(5, 13),
                    F(-2, 5), F(7, 17), F(1, 19), F(-3, 23), F(2, 29)]
    for a in (F(1, 4), F(3, 7)):
        sample = [sum(c*b for c, b in zip(coefficients, basis9(a*x, a*y)))
                  for x, y in points9]
        decoded = [sum(v*z for v, z in zip(row, sample))/a**degree
                   for row, degree in zip(inv9, degrees)]
        require(decoded == coefficients, "scaled operational inverse")
        _, determinant = inverse_det([basis9(a*x, a*y) for x, y in points9])
        require(determinant == 3456*a**18, "scaled determinant")

    # Owned quartic is a hostile control for using the cubic five-point
    # theorem outside its stated space. It survives the nine-point map.
    require(all(x*y*(x*x-y*y) == 0 for x, y in points5), "quartic alias")
    require(3*(1**2-0**2) == 3, "quartic nonzero mixed curvature")
    require(any(x*y*(x*x-y*y) != 0 for x, y in points9), "quartic lost")

    # Exact rational controls of the universal monotone probability law,
    # not substitutes for the native Golden compiler or actuation theorem.
    require(8*F(1, 2)*(1-2*F(1, 2)**2) == 2, "upper derivative")
    require(8*F(2, 3)*(1-2*F(2, 3)**2) == F(16, 27), "lower derivative")
    for left, right in ((F(1, 2), F(2, 3)),
                        (F(7, 12), F(5, 8)),
                        (F(3, 5), F(13, 20))):
        secant = (B(right)-B(left))/(right-left)
        require(secant == 4*(right+left)*(1-left*left-right*right),
                "complete probability contrast")
        require(F(16, 27) <= secant <= 2, "inverse norm budget")
        ready = F(2, 5)
        total_variation = (
            abs(ready*(B(right)-B(left)))
            + abs(ready*(B(left)-B(right)))
        )/2
        require(total_variation == ready*abs(B(right)-B(left)),
                "abort-retaining TV")

    # The unknown u-gradient cancels in the actual two-increment formula.
    delta_plus, delta_minus = F(1, 31), F(-1, 37)
    h, rho, s2, v4, H = F(1, 8), F(7, 5), F(9, 4), F(1, 13), F(2, 17)
    def query(delta):
        r = delta/h
        return s2/rho*(2*v4*r-H*r*r)
    reconstructed = -rho*h*h/s2*(
        query(delta_plus)/delta_plus-query(delta_minus)/delta_minus
    )/(delta_plus-delta_minus)
    require(reconstructed == H, "two-probe metric inverse")
    norm = (1/abs(delta_plus)+1/abs(delta_minus))/abs(delta_plus-delta_minus)
    require(norm == 1/abs(delta_plus*delta_minus), "two-probe sensitivity")

    # The real rest-observer pairing is not the identity in null
    # coordinates. Exact nonzero H controls catch that normalization and
    # the factor 1/4 in the inherited reachability distance bound.
    def pairing(profile, kappa):
        return [[kappa/2, -kappa*profile/4, 0, 0],
                [-kappa*profile/4, kappa*(2+profile*profile/8), 0, 0],
                [0, 0, kappa, 0], [0, 0, 0, kappa]]
    def inverse_metric(profile, kappa):
        return [[0, kappa, 0, 0], [kappa, -kappa*profile, 0, 0],
                [0, 0, -kappa, 0], [0, 0, 0, -kappa]]
    def trace(a):
        return sum(a[i][i] for i in range(len(a)))
    for initial, delta, kappa in ((F(0), F(1, 7), F(3, 5)),
                                  (F(-2, 3), F(-1, 11), F(5, 2)),
                                  (F(7, 9), F(2, 13), F(1))):
        Q0 = pairing(initial, kappa)
        Qinv, Qdet = inverse_det(Q0)
        q0 = inverse_metric(initial, kappa)
        q1 = inverse_metric(initial+delta, kappa)
        _, qdet = inverse_det(q1)
        require(Qdet == kappa**4 and qdet == -kappa**4,
                "fixed pairing determinant pins positive scalar")
        require(mm(mm(q0, Qinv), q0) == Q0, "reflection metric identity")
        require(trace(mm(Qinv, q1))+2 == -delta/2,
                "primary fixed-pairing trace defect")
        require(abs(trace(mm(Qinv, q1))+2)/2 == abs(delta)/4,
                "quantitative writer-image distance lower bound")
        moved = pairing(initial+delta, kappa)
        difference = [[moved[i][j]-Q0[i][j] for j in range(4)] for i in range(4)]
        expected = [[0, -kappa*delta/4, 0, 0],
                    [-kappa*delta/4, kappa*(initial*delta/4+delta*delta/8), 0, 0],
                    [0, 0, 0, 0], [0, 0, 0, 0]]
        require(difference == expected, "required coordinate-pairing escape")
    print(json.dumps({
        "status": "PASS",
        "groups": [
            "exact five/nine-profile inverse and scaled determinants",
            "quartic hostile control and full-space recovery",
            "abort-retaining probability and two-probe error norms",
            "fixed-pairing observable reachability gap and moving-pairing escape"
        ],
        "five_point_determinant_at_unit_scale": str(det5),
        "nine_point_determinant_at_unit_scale": str(det9),
        "nine_point_inverse_row_l1": list(map(str, rowsums)),
        "scope": "new algebra only; no native admission, price or GR closure"
    }, sort_keys=True))


if __name__ == "__main__":
    main()
