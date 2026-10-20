#!/usr/bin/env python3
"""Exact checks of the prepared-history feedback map; standard library only.

The general proofs and exact input/action boundaries are in
prepared_price_feedback.md. Finite matrices check those identities, not a
physical admission theorem or uniform refinement estimate.
"""
from fractions import Fraction as Q
import json


class GoldenRoot:
    """Q[a]/(a^4+a^2-1), with the actual positive a=sqrt(phi^-1)."""

    def __init__(self, coefficients=0):
        if isinstance(coefficients, GoldenRoot):
            self.c = coefficients.c
            return
        if isinstance(coefficients, (int, Q)):
            coefficients = [coefficients]
        c = [Q(x) for x in coefficients]
        c += [Q(0)] * max(0, 4 - len(c))
        for degree in range(len(c) - 1, 3, -1):
            c[degree - 4] += c[degree]
            c[degree - 2] -= c[degree]
        self.c = tuple(c[:4])

    def __add__(self, other):
        other = GoldenRoot(other)
        return GoldenRoot([x + y for x, y in zip(self.c, other.c)])

    __radd__ = __add__

    def __neg__(self):
        return GoldenRoot([-x for x in self.c])

    def __sub__(self, other):
        return self + -GoldenRoot(other)

    def __rsub__(self, other):
        return GoldenRoot(other) + -self

    def __mul__(self, other):
        other = GoldenRoot(other)
        c = [Q(0)] * 7
        for i, x in enumerate(self.c):
            for j, y in enumerate(other.c):
                c[i + j] += x * y
        return GoldenRoot(c)

    __rmul__ = __mul__

    def __eq__(self, other):
        return self.c == GoldenRoot(other).c

    def encoded(self):
        return [str(x) for x in self.c]


def eye(n):
    return [[Q(i == j) for j in range(n)] for i in range(n)]


def tr(a):
    return sum(a[i][i] for i in range(len(a)))


def transpose(a):
    return list(map(list, zip(*a)))


def mul(a, b):
    return [[sum(x * y for x, y in zip(row, col))
             for col in zip(*b)] for row in a]


def add(a, b):
    return [[x + y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def scale(c, a):
    return [[c * x for x in row] for row in a]


def sub(a, b):
    return add(a, scale(-1, b))


def block(a, b, c, d):
    return [ar + br for ar, br in zip(a, b)] + [cr + dr for cr, dr in zip(c, d)]


def inv2(a):
    determinant = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    return [[a[1][1] / determinant, -a[0][1] / determinant],
            [-a[1][0] / determinant, a[0][0] / determinant]]


def det2(a):
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def run():
    checks = []

    def verify(name, condition):
        if not condition:
            raise AssertionError(name)
        checks.append(name)

    a = GoldenRoot([0, 1])
    p = a * a
    delta = (a - p) * (a - p)
    verify("golden_probability", p + p * p == 1)
    verify("native_K0_K1_complete", p * p + p * p * p * p + 2 * p * p * p == 1)
    # F-G as a polynomial in the ACTUAL operator R=p epsilon Delta.
    f = [1 - p * p, -2 * p * (a - p), -delta]
    g = [p, p * p - p, GoldenRoot(0)]
    verify("golden_feedback_constant", f[0] == g[0])
    verify("golden_feedback_linear_work_complement", f[1] - g[1] == delta)
    verify("golden_feedback_quadratic_work_complement", f[2] - g[2] == -delta)
    verify("golden_cost_marker", p * p - p == -(p * p * p))

    # A genuine noncommuting operator variation: no scalar-eigenmode shortcut.
    r = [[Q(1, 7), Q(0)], [Q(0), Q(1, 3)]]
    dr = [[Q(1, 5), Q(2, 7)], [Q(2, 7), Q(-1, 11)]]
    verify("variation_does_not_commute", mul(r, dr) != mul(dr, r))
    rr = add(mul(r, dr), mul(dr, r))
    df = sub(scale(-2 * p * (a - p), dr), scale(delta, rr))
    dg = scale(-(p * p * p), dr)
    dl = scale(delta, sub(dr, rr))
    verify("complete_noncommuting_first_source", df == add(dg, dl))
    verify("dropping_work_complement_changes_source", df != dg)

    # Rational full four-coordinate echo: two work states, both marker ports.
    # B=sqrt(I-E), S=sqrt(E) are both exact, so no numerical square root.
    w = [[Q(3, 5), Q(-4, 5)], [Q(4, 5), Q(3, 5)]]
    # dW/dt at t=1/2 for the rational orthogonal rotation.
    dw = [[Q(-32, 25), Q(-24, 25)], [Q(24, 25), Q(-32, 25)]]
    b = [[Q(3, 5), Q(0)], [Q(0), Q(5, 13)]]
    s = [[Q(4, 5), Q(0)], [Q(0), Q(12, 13)]]
    e = mul(s, s)
    zero = [[Q(0), Q(0)], [Q(0), Q(0)]]
    verify("full_work_unitary", mul(transpose(w), w) == eye(2))
    verify("actual_isometry_tangent", add(mul(transpose(dw), w), mul(transpose(w), dw)) == zero)
    verify("marker_full_complement", add(mul(b, b), e) == eye(2))
    j = block(b, scale(-1, s), s, b)
    w2 = block(w, zero, zero, w)
    u = mul(mul(transpose(w2), j), w2)
    verify("entire_echo_unitary", mul(transpose(u), u) == eye(4))

    # P_in retains only the first work state in marker0; Q is ALL other states.
    qin = eye(4)
    qin[0][0] = 0
    whole_feedback = mul(mul(transpose(u), qin), u)[0][0]
    aw = mul(mul(transpose(w), b), w)
    gw = mul(mul(transpose(w), e), w)
    aa, gg = aw[0][0], gw[0][0]
    leakage = sum(u[row][0] * u[row][0] for row in (1,))
    verify("prepared_cut_true_feedback", whole_feedback == 1 - aa * aa)
    verify("all_output_work_complement", whole_feedback == gg + leakage)
    verify("complement_strictly_present", leakage > 0)
    verify("selected_marker_is_not_original_complement", whole_feedback != gg)

    da = add(mul(mul(transpose(dw), b), w), mul(mul(transpose(w), b), dw))[0][0]
    dgw = add(mul(mul(transpose(dw), e), w), mul(mul(transpose(w), e), dw))
    dff = -2 * aa * da
    dll = dff - dgw[0][0]
    verify("nonzero_work_complement_first_source", dll != 0)

    # On the full-work active cut the counting determinant has zero source.
    z = Q(1, 3)
    resolvent = inv2(sub(eye(2), scale(z, gw)))
    all_source = z * tr(mul(resolvent, dgw))
    verify("full_work_determinant_identity", det2(sub(eye(2), scale(z, gw))) == det2(sub(eye(2), scale(z, e))))
    verify("full_work_determinant_source_zero", all_source == 0)
    verify("prepared_partition_source_nonzero", dgw[0][0] != 0)

    # Direct check of the centred covariance form used in the C2 proof.
    ve = [[w[0][0]], [w[1][0]]]
    de = sub(b, eye(2))
    covariance = mul(mul(transpose(ve), mul(de, de)), ve)[0][0] - mul(mul(transpose(ve), de), ve)[0][0] ** 2
    verify("centred_work_covariance_identity", covariance == leakage)

    return {
        "status": "PASS", "arithmetic": "exact rational and Q[a]/(a^4+a^2-1)",
        "scope": "operator/source identities; no physical Info or apparatus admission",
        "checks": checks,
        "golden_complement_coefficient_basis_1_a_a2_a3": delta.encoded(),
        "complete_echo": {
            "paid_partition_effect": str(gg), "true_feedback": str(whole_feedback),
            "work_complement": str(leakage), "work_complement_first_source": str(dll),
            "prepared_partition_first_source": str(dgw[0][0]),
            "full_work_feedback_source": str(all_source),
        },
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, ensure_ascii=False))
