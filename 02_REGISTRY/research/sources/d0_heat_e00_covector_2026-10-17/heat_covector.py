"""Euler-Lagrange covectors of the pp-wave Einstein-Hilbert density and the owned heat density.

The heat identity L2 = -4*R(e.T@e)/3 + q(T) is checked against 8*|grad H|**2/3
before any variation is reported. No coefficient is chosen so that the two
covectors agree.
"""
from __future__ import annotations

import sympy as sp

ETA = sp.diag(1, -1, -1, -1)
N = sp.zeros(4)
N[0, 0] = N[0, 3] = sp.Rational(1, 2)
N[3, 0] = N[3, 3] = -sp.Rational(1, 2)
E00 = sp.zeros(4)
E00[0, 0] = 1
K = sp.Matrix([1, 0, 0, 1])
X = sp.symbols("x", real=True)
EPS = sp.symbols("eps", real=True)
PHI = sp.Function("phi", real=True)(X)
PROFILE = X**2 + sp.Rational(1, 4)


def require_sphere() -> None:
    theta, phi = sp.symbols("theta phi", real=True)
    metric = sp.diag(1, sp.sin(theta) ** 2)
    scalar, ric, _ = curvature(metric, [theta, phi])
    if sp.simplify(scalar - 2) != 0 or sp.simplify(ric[0, 0] - 1) != 0:
        raise ArithmeticError("sphere_control")


def curvature(metric: sp.Matrix, coords: list) -> tuple[sp.Expr, sp.Matrix, sp.Matrix]:
    """MTW contraction R_{sigma nu} = R^rho_{sigma rho nu}."""
    n = metric.shape[0]
    inverse = sp.simplify(metric.inv())
    gamma = [[[0 for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for rho in range(n):
        for mu in range(n):
            for nu in range(mu, n):
                acc = 0
                for sigma in range(n):
                    acc += inverse[rho, sigma] * (
                        sp.diff(metric[nu, sigma], coords[mu])
                        + sp.diff(metric[mu, sigma], coords[nu])
                        - sp.diff(metric[mu, nu], coords[sigma])
                    )
                value = sp.together(acc / 2)
                gamma[rho][mu][nu] = value
                gamma[rho][nu][mu] = value
    ric = sp.zeros(n)
    for sigma in range(n):
        for nu in range(sigma, n):
            acc = 0
            for rho in range(n):
                acc += sp.diff(gamma[rho][nu][sigma], coords[rho])
                acc -= sp.diff(gamma[rho][rho][sigma], coords[nu])
                for lam in range(n):
                    acc += gamma[rho][rho][lam] * gamma[lam][nu][sigma]
                    acc -= gamma[rho][nu][lam] * gamma[lam][rho][sigma]
            value = sp.simplify(acc)
            ric[sigma, nu] = value
            ric[nu, sigma] = value
    scalar = sp.simplify(sum(inverse[i, j] * ric[i, j] for i in range(n) for j in range(n)))
    return scalar, ric, inverse


def wave_frame(height) -> sp.Matrix:
    return sp.eye(4) + height * N


def lorentz_metric(frame: sp.Matrix) -> sp.Matrix:
    return sp.simplify(frame.T * ETA * frame)


def positive_metric(frame: sp.Matrix) -> sp.Matrix:
    return sp.simplify(frame.T * frame)


def anholonomy_quadratic(frame: sp.Matrix) -> sp.Expr:
    """q(T) in the natural coframe. Only x-dependence is admitted."""
    inverse = sp.simplify(frame.inv())
    de = frame.diff(X)
    full = {(a, b, c): 0 for a in range(4) for b in range(4) for c in range(4)}
    for a in range(4):
        for b in range(4):
            for c in range(b + 1, 4):
                acc = 0
                for r in range(4):
                    acc += inverse[1, b] * de[a, r] * inverse[r, c]
                    acc -= inverse[1, c] * de[a, r] * inverse[r, b]
                value = sp.expand(acc)
                full[(a, b, c)] = value
                full[(a, c, b)] = -value
    trace = [sum(full[(a, a, c)] for a in range(4)) for c in range(4)]
    triples = [(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]
    axial = 0
    for a, b, c in triples:
        cyclic = full[(a, b, c)] + full[(b, c, a)] + full[(c, a, b)]
        axial += sp.expand(cyclic**2)
    return sp.simplify(2 * axial - 4 * sum(item**2 for item in trace))


def heat_coefficient(frame: sp.Matrix) -> sp.Expr:
    scalar, _, _ = curvature(positive_metric(frame), _coords())
    return sp.simplify(-sp.Rational(4, 3) * scalar + anholonomy_quadratic(frame))


def einstein_hilbert_density(metric: sp.Matrix) -> sp.Expr:
    scalar, _, _ = curvature(metric, _coords())
    return sp.simplify(scalar * sp.sqrt(-metric.det()))


def probe_g00(metric: sp.Matrix) -> sp.Expr:
    _, ric, inverse = curvature(metric, _coords())
    raised = sp.simplify(inverse * ric * inverse)
    return sp.simplify(raised[0, 0])


def euler(raw: sp.Expr) -> tuple[sp.Expr, sp.Expr]:
    """∫ raw dx = ∫ el*phi dx + current, for raw linear in phi, phi', phi''."""
    p1 = sp.diff(PHI, X)
    p2 = sp.diff(PHI, X, 2)
    second = sp.simplify(raw.coeff(p2))
    rest = sp.simplify(raw - second * p2)
    first = sp.simplify(rest.coeff(p1))
    zero = sp.simplify(rest - first * p1)
    coef = sp.simplify(sp.together(zero / PHI))
    if sp.simplify(zero - coef * PHI) != 0:
        raise ArithmeticError("variation_not_linear_in_phi")
    el = sp.expand(sp.simplify(coef - sp.diff(first, X) + sp.diff(second, X, 2)))
    current = sp.simplify(first * PHI + second * p1 - sp.diff(second, X) * PHI)
    if sp.simplify(el * PHI + sp.diff(current, X) - raw) != 0:
        raise ArithmeticError("integration_by_parts")
    return el, current


def _coords() -> list:
    t, y, z = sp.symbols("t y z", real=True)
    return [t, X, y, z]


def e00_frame(height=PROFILE):
    frame0 = wave_frame(height)
    metric0 = lorentz_metric(frame0)
    delta = sp.simplify(frame0 * metric0.inv() * E00 * PHI / 2)
    return sp.simplify(frame0 + EPS * delta), frame0


def profile_frame(height=PROFILE):
    return wave_frame(height + EPS * PHI)


def varied(expression: sp.Expr) -> sp.Expr:
    return sp.simplify(sp.diff(expression, EPS).subs(EPS, 0))
