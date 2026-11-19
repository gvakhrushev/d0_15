#!/usr/bin/env python3
"""Narrow checks of the NEW two-density stationary normal form.

Python 3.11+ standard library only. No checkout, network, or old all40 checker
is required. Exact rational jets check the algebra, including shared variables
and internal-source pullbacks. Q(sqrt(5)) arithmetic checks the finite detector
coefficient. Decimal Newton solves test the new nonzero-density branch.

The Decimal diagnostics are not interval certificates or a proof of the
implicit-function theorem. The illustrative alpha, beta, kappa below are NOT
a replay of a native preparation bank. Repository operand binding is separate.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal, getcontext
from fractions import Fraction as Q
from pathlib import Path


class Jet:
    """Value, gradient, Hessian with exact Fraction coefficients."""

    def __init__(self, value, gradient, hessian):
        self.v = Q(value)
        self.g = tuple(map(Q, gradient))
        self.h = tuple(tuple(map(Q, row)) for row in hessian)
        self.n = len(self.g)

    @classmethod
    def constant(cls, value, n):
        return cls(value, [0] * n, [[0] * n for _ in range(n)])

    @classmethod
    def variable(cls, value, n, index):
        gradient = [0] * n
        gradient[index] = 1
        return cls(value, gradient, [[0] * n for _ in range(n)])

    def cast(self, other):
        return other if isinstance(other, Jet) else Jet.constant(other, self.n)

    def __add__(self, other):
        b = self.cast(other)
        return Jet(self.v + b.v, [u + v for u, v in zip(self.g, b.g)],
                   [[self.h[i][j] + b.h[i][j] for j in range(self.n)]
                    for i in range(self.n)])

    __radd__ = __add__

    def __neg__(self):
        return Jet(-self.v, [-u for u in self.g],
                   [[-v for v in row] for row in self.h])

    def __sub__(self, other):
        return self + (-self.cast(other))

    def __rsub__(self, other):
        return self.cast(other) - self

    def __mul__(self, other):
        b = self.cast(other)
        return Jet(self.v * b.v,
                   [self.g[i] * b.v + self.v * b.g[i] for i in range(self.n)],
                   [[self.h[i][j] * b.v + self.g[i] * b.g[j]
                     + self.g[j] * b.g[i] + self.v * b.h[i][j]
                     for j in range(self.n)] for i in range(self.n)])

    __rmul__ = __mul__

    def inverse(self):
        return Jet(1 / self.v, [-v / self.v**2 for v in self.g],
                   [[2 * self.g[i] * self.g[j] / self.v**3
                     - self.h[i][j] / self.v**2 for j in range(self.n)]
                    for i in range(self.n)])

    def __truediv__(self, other):
        return self * self.cast(other).inverse()

    def __rtruediv__(self, other):
        return self.cast(other) * self.inverse()

    def __pow__(self, n):
        if n < 0:
            return self.inverse() ** (-n)
        result = Jet.constant(1, self.n)
        for _ in range(n):
            result = result * self
        return result


def variables(values):
    return [Jet.variable(value, len(values), i) for i, value in enumerate(values)]


def coefficients(zeta):
    z0, z1 = zeta
    return [2 + z0, 3 + z1], [5 + 2 * z0, 7 - z1]


def baseline(zeta):
    z0, z1 = zeta
    return z0**2 + 3 * z1 + z0 * z1


def coupled_price(x, y, zeta):
    a, b = coefficients(zeta)
    z0, z1 = zeta
    # F_xx=[[2,2],[2,2]] is singular. The theorem must still work.
    return (z0 * z1 + z1**2 + sum(a[i] * x[i] + b[i] * y[i] for i in range(2))
            + x[0]**2 + 2 * x[0] * x[1] + x[1]**2
            + 3 * x[0] * y[0] - x[0] * y[1]
            + 2 * x[1] * y[0] + 4 * x[1] * y[1]
            + 2 * y[0]**2 + y[0] * y[1] - y[1]**2
            + x[0] * y[1]**2 / 3 + x[0]**2 * x[1] / 7
            + y[0]**2 * y[1] / 11)


def densities(u, link, matter, zeta):
    v0, v1 = link
    w0, w1 = matter
    z0, z1 = zeta
    x = [u[0] * (v0 + v1**2), u[1] * (2 * v0 - v1)]
    y = [(w0**2 - w1**2 + v1 * w0 + z0 * v0) / u[0],
         (2 * w0 * w1 + v0 * w1 + z1 * v1) / u[1]]
    return x, y


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def transpose(a):
    return [list(row) for row in zip(*a)]


def exact_rational_checks():
    values = [Q(6, 5), Q(7, 6), Q(1, 11), Q(-1, 13), Q(2, 3), Q(3, 7),
              Q(1, 5), Q(-1, 7), Q(1, 17), Q(-1, 19), Q(12, 5), Q(19, 7)]
    j = variables(values)
    u, link, matter, zeta, s, pi = j[:2], j[2:4], j[4:6], j[6:8], j[8:10], j[10:12]
    a, _ = coefficients(zeta)
    old_u = [a[i] / pi[i] * u[i] for i in range(2)]
    old_x, old_y = densities(old_u, link, matter, zeta)
    new_x, new_y = densities(u, link, matter, zeta)
    left = (baseline(zeta) + coupled_price(s, old_y, zeta)
            + sum(pi[i] * (old_x[i] - s[i]) for i in range(2)))
    right = (baseline(zeta) + sum(a[i] * new_x[i] - pi[i] * s[i] for i in range(2))
             + coupled_price(s, [pi[i] / a[i] * new_y[i] for i in range(2)], zeta))
    assert (left.v, left.g, left.h) == (right.v, right.g, right.h)

    z = [Q(1, 5), Q(-1, 7)]
    a0, b0 = coefficients(z)
    density_jets = variables([0, 0, 0, 0])
    f = coupled_price(density_jets[:2], density_jets[2:], z)
    fxx = [list(row[:2]) for row in f.h[:2]]
    assert fxx[0][0] * fxx[1][1] - fxx[0][1] * fxx[1][0] == 0
    aux = variables([0, 0, a0[0], a0[1], 0, 0])
    ss, pp, yy = aux[:2], aux[2:4], aux[4:6]
    g = (coupled_price(ss, [pp[i] / a0[i] * yy[i] for i in range(2)], z)
         - sum(pp[i] * ss[i] for i in range(2)))
    h = [list(row[:4]) for row in g.h[:4]]
    hinv = [[Q(0) for _ in range(4)] for _ in range(4)]
    for i in range(2):
        hinv[i][i + 2] = hinv[i + 2][i] = -1
        for k in range(2):
            hinv[i + 2][k + 2] = -fxx[i][k]
    assert matmul(h, hinv) == [[int(i == k) for k in range(4)] for i in range(4)]
    cross = [list(row[4:]) for row in g.h[:4]]
    correction = matmul(matmul(transpose(cross), hinv), cross)
    schur = [[g.h[i + 4][k + 4] - correction[i][k] for k in range(2)] for i in range(2)]
    tangent = [[b0[0] / a0[0], 0], [0, b0[1] / a0[1]], [1, 0], [0, 1]]
    predicted = matmul(matmul(transpose(tangent), f.h), tangent)
    assert schur == predicted
    assert schur[0][1] != 0  # Correlated price need not produce local K_i.
    assert tuple(g.g[:4]) == (0, 0, 0, 0)
    assert tuple(g.g[4:]) == tuple(b0)

    # Independent internal-source test: densities vanish but their internal
    # derivatives do not. Nonzero matter is retained, with nonzero dY.
    jn = variables([2, 3, 0, 0, 1, 1, Q(1, 5), Q(-1, 7)])
    un, vn, wn, zn = jn[:2], jn[2:4], jn[4:6], jn[6:8]
    xn = [un[0] * (vn[0] + zn[1] - z[1]), un[1] * vn[1]]
    yn = [(wn[0]**2 - wn[1]**2 + zn[0] - z[0]) / un[0],
          (2 * (wn[0] - wn[1]) * wn[0]) / un[1]]
    an, bn = coefficients(zn)
    fzero = coupled_price([0, 0], [0, 0], zn)
    actual = baseline(zn) + coupled_price(xn, yn, zn)
    linear = baseline(zn) + fzero + sum(an[i] * xn[i] + bn[i] * yn[i] for i in range(2))
    assert all(v.v == 0 for v in xn + yn)
    assert any(v != 0 for v in yn[0].g)
    assert (actual.v, actual.g) == (linear.v, linear.g)
    assert actual.h != linear.h  # First-source equality is not all-order equality.
    just_baseline = baseline(zn) + fzero
    assert actual.g[6] != just_baseline.g[6]
    assert actual.g[7] != just_baseline.g[7]
    dropped_baseline = linear - just_baseline
    assert actual.g[6:] != dropped_baseline.g[6:]

    return {
        "extended_identity_value_gradient_hessian": "exact",
        "fixture": "two coupled sites; 12 independent rational coordinates; not native all40",
        "singular_Fxx_auxiliary_inverse": "exact",
        "coupled_K_hessian_by_independent_Schur_complement": [[str(v) for v in row] for row in schur],
        "null_nonconstant_matter_first_source": "exact; full Hessian intentionally differs",
        "internal_density_dictionary_terms_retained": "exact; deleting them fails",
        "baseline_source_retained": "exact; deleting it fails",
    }


@dataclass(frozen=True)
class Golden:
    """u+v*p, where p^2+p=1 and p=(sqrt(5)-1)/2. Exact ordered field."""

    u: Q = Q(0)
    v: Q = Q(0)

    def __post_init__(self):
        object.__setattr__(self, "u", Q(self.u))
        object.__setattr__(self, "v", Q(self.v))

    @staticmethod
    def cast(value):
        return value if isinstance(value, Golden) else Golden(value)

    def __add__(self, other):
        b = self.cast(other)
        return Golden(self.u + b.u, self.v + b.v)

    __radd__ = __add__

    def __neg__(self):
        return Golden(-self.u, -self.v)

    def __sub__(self, other):
        return self + (-self.cast(other))

    def __rsub__(self, other):
        return self.cast(other) - self

    def __mul__(self, other):
        b = self.cast(other)
        return Golden(self.u * b.u + self.v * b.v,
                      self.u * b.v + self.v * b.u - self.v * b.v)

    __rmul__ = __mul__

    def inverse(self):
        norm = self.u**2 - self.u * self.v - self.v**2
        return Golden((self.u - self.v) / norm, -self.v / norm)

    def __truediv__(self, other):
        return self * self.cast(other).inverse()

    def __rtruediv__(self, other):
        return self.cast(other) * self.inverse()

    def __pow__(self, n):
        if n < 0:
            return self.inverse() ** (-n)
        result = Golden(1)
        for _ in range(n):
            result = result * self
        return result

    def sign(self):
        aa, bb = 2 * self.u - self.v, self.v
        if not bb:
            return (aa > 0) - (aa < 0)
        if not aa:
            return (bb > 0) - (bb < 0)
        if aa * bb > 0:
            return (aa > 0) - (aa < 0)
        sq = aa**2 - 5 * bb**2
        if sq > 0:
            return (aa > 0) - (aa < 0)
        return (bb > 0) - (bb < 0)

    def decimal(self):
        def dec(v):
            return Decimal(v.numerator) / Decimal(v.denominator)
        p = (Decimal(5).sqrt() - 1) / 2
        return dec(self.u) + dec(self.v) * p


def exact_golden_checks():
    p = Golden(0, 1)
    assert p**2 + p == Golden(1)
    assert p * (1 + p) == Golden(1)
    assert p * (1 / p) == Golden(1)
    z = Q(1, 2**20)
    ell = 4 * p**3
    aa = ell * (1 + p**6)
    qq, rr = 1 - z * ell, 1 - z * aa
    r0 = 1 - qq * rr
    assert ell == 1 - p**6
    assert aa == 1 - p**12
    assert (r0 - z).sign() == 1 and (2 * z - r0).sign() == 1
    rx = 4 * z * qq * p**11
    ry = 8 * z * (rr * p**6 + qq * p**12)
    ratio = ry / rx
    limit = 16 + 12 * p
    delta = 8 * z * p**4 / qq
    assert ratio == 2 * p**(-5) * rr / qq + 2 * p
    assert ratio == limit - delta
    assert delta.sign() == 1 and (ratio - limit).sign() == -1
    cap_bound = 51 - Q(40) / (1 - Q(1, 2**19))
    assert cap_bound > 10
    return {
        "arithmetic": "exact Q(sqrt(5)); signs decided by rational squares",
        "r0_strict_bounds": "2^-20 < r0 < 2^-19",
        "finite_coupling_ratio": str(ratio.decimal()),
        "zero_z_limit": str(limit.decimal()),
        "strict_positive_difference_limit_minus_finite": str(delta.decimal()),
        "all_caps_N_ge_2_derivative_bound_over_alpha_beta": str(cap_bound),
        "cap_bound_scope": "analytic: 0<alpha,beta<=1 and consumed kappa>53; no cap enumeration proof",
    }


D = Decimal


def detector_jet(x, y):
    p = (D(5).sqrt() - 1) / 2
    z = D(1) / D(2)**20
    w = p + p**2 * y
    bb = 4 * w**2 * (1 - w**2)
    by = 8 * p**2 * w * (1 - 2 * w**2)
    byy = 8 * p**4 * (1 - 6 * w**2)
    e = p**2 * (1 + x)
    ell, lx, lxx = 4 * e * (1 - e), 4 * p**2 * (1 - 2 * e), -8 * p**4
    aa = ell + (1 - ell) * bb
    ax, ay = lx * (1 - bb), (1 - ell) * by
    axx, axy, ayy = lxx * (1 - bb), -lx * by, (1 - ell) * byy
    qq, rr = 1 - z * bb, 1 - z * aa
    return (1 - qq * rr,
            z * qq * ax, z * (rr * by + qq * ay),
            z * qq * axx, z * qq * axy - z**2 * by * ax,
            z * (rr * byy + qq * ayy) - 2 * z**2 * by * ay)


def price_jet(x, y, cap, alpha, beta, kappa):
    r, rx, ry, rxx, rxy, ryy = detector_jet(x, y)
    assert 0 < r < 1
    lnphi = ((1 + D(5).sqrt()) / 2).ln()
    h = (-r * r.ln() - (1 - r) * (1 - r).ln()) / lnphi
    hp = ((1 - r) / r).ln() / lnphi
    hpp = -1 / (r * (1 - r) * lnphi)
    t = beta * r
    en = sum((t**j for j in range(cap)), D(0))
    ep = sum((j * t**(j - 1) for j in range(1, cap)), D(0))
    epp = sum((j * (j - 1) * t**(j - 2) for j in range(2, cap)), D(0))
    value = alpha * (kappa - beta * h) * en
    gp = alpha * beta * ((kappa - beta * h) * ep - hp * en)
    gpp = alpha * (-beta * hpp * en - 2 * beta**2 * hp * ep
                   + beta**2 * (kappa - beta * h) * epp)
    return (value, gp * rx, gp * ry,
            gpp * rx**2 + gp * rxx, gpp * rx * ry + gp * rxy,
            gpp * ry**2 + gp * ryy, gp)


def solve_auxiliary(y, cap, params, a):
    s, scale = D(0), D(1)  # scale=pi/a avoids unnecessary poor scaling.
    for iteration in range(30):
        f = price_jet(s, scale * y, cap, *params)
        e1, e2 = f[1] / a - scale, y / a * f[2] - s
        residual = max(abs(e1), abs(e2))
        if residual < D("1e-65"):
            assert scale > 0
            return f[0] - a * scale * s, scale * f[2], s, scale, residual, iteration
        h11, h12, h22 = f[3] / a, y / a * f[4] - 1, y**2 / a * f[5]
        det = h11 * h22 - h12**2
        assert det != 0
        ds = (h22 * e1 - h12 * e2) / det
        dw = (-h12 * e1 + h11 * e2) / det
        s, scale = s - ds, scale - dw
    raise AssertionError("Auxiliary Newton iteration did not converge")


def decimal_branch_checks():
    params = (D(3) / 5, D(5) / 7, D(54))
    alpha, beta, _ = params
    results = []
    tiny = D("1e-12")
    slopes = []
    for cap in (1, 2, 7, 31):
        f = price_jet(D(0), D(0), cap, *params)
        f0, a, b, fxx, fxy, fyy, gp = f
        assert a != 0
        assert gp < 0 if cap == 1 else gp > 10 * alpha * beta
        ratio = b / a
        slopes.append(ratio)
        kpp = fyy + 2 * ratio * fxy + ratio**2 * fxx
        if cap == 1:
            assert kpp > 0
        zero = solve_auxiliary(D(0), cap, params, a)
        assert zero[0] == f0 and zero[1] == b and zero[2] == 0 and zero[3] == 1
        positive = solve_auxiliary(tiny, cap, params, a)
        negative = solve_auxiliary(-tiny, cap, params, a)
        kpp_difference = (positive[1] - negative[1]) / (2 * tiny)
        relative_error = abs((kpp_difference - kpp) / kpp)
        assert relative_error < D("1e-18")
        nonzero = [solve_auxiliary(y, cap, params, a) for y in (D("-1e-4"), D("1e-4"))]
        # Full nonlinear matter is necessary: the quadratic residual survives.
        quadratic_remainder_ratio = (positive[0] + negative[0] - 2 * f0) / tiny**2
        assert abs((quadratic_remainder_ratio - kpp) / kpp) < D("1e-18")
        results.append({
            "cap": cap, "a": str(a), "b_over_a": str(ratio),
            "K_second_derivative": str(kpp),
            "central_envelope_derivative_relative_error": str(relative_error),
            "max_auxiliary_residual": str(max(v[4] for v in nonzero + [positive, negative])),
            "nonzero_Y": ["-1e-4", "1e-4"],
            "scale_pi_over_a_at_nonzero_Y": [str(v[3]) for v in nonzero],
        })
    assert max(slopes) - min(slopes) < D("1e-70")
    return {
        "precision_decimal_digits": getcontext().prec,
        "example_parameters": {"alpha": "3/5", "beta": "5/7", "kappa": "54"},
        "parameters_are": "illustrative admissible values, not asserted native bank output",
        "status": "non-interval numerical diagnostics; theorem is analytic",
        "branches": results,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Write the actual execution receipt as JSON")
    args = parser.parse_args()
    getcontext().prec = 85
    result = {
        "status": "PASS",
        "result": "exact stationary two-density normal form, with stated operand assumptions",
        "GR_closed": False,
        "run_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "fresh_repository_checkout": False,
        "publication": "not performed by this checker",
        "prior_source_commit": "963a9ae0a22ac05ba13b86e66f56bae68a6ec492",
        "checks": {
            "rational_source_and_auxiliary_checks": exact_rational_checks(),
            "finite_golden_coupling_and_cap_bound": exact_golden_checks(),
            "new_nonzero_density_branch": decimal_branch_checks(),
        },
        "not_checked": [
            "current branch head and current repository operand binding",
            "full native compiler or original 40+2 equations",
            "sitewise matter homogeneity for any additional Riesz-dependent dictionary",
            "independent preparation, clock, or absolute-Book internal stationary roots",
            "uniform neighborhood in cap, mesh size, or lattice size",
        ],
    }
    rendered = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
