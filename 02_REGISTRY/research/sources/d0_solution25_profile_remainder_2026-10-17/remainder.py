"""Profile Euler densities of owned extras on Palatini solution (25).

The recorded remainder is the Euler density obtained by differentiating the
owned scalar formula. It is not defined as a gap to the Einstein tensor.
No constant is solved so that the two agree.
"""
from __future__ import annotations

import sympy as sp

ETA = sp.diag(1, -1, -1, -1)
N = sp.zeros(4)
N[0, 0] = N[0, 3] = sp.Rational(1, 2)
N[3, 0] = N[3, 3] = -sp.Rational(1, 2)
K = sp.Matrix([1, 0, 0, 1])


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
    ricci = sp.zeros(n)
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
            ricci[sigma, nu] = value
            ricci[nu, sigma] = value
    scalar = sp.simplify(sum(inverse[i, j] * ricci[i, j] for i in range(n) for j in range(n)))
    return scalar, ricci, inverse


def require_sphere() -> None:
    theta, phi = sp.symbols("theta phi", real=True)
    metric = sp.diag(1, sp.sin(theta) ** 2)
    scalar, ricci, _ = curvature(metric, [theta, phi])
    if sp.simplify(scalar - 2) != 0 or sp.simplify(ricci[0, 0] - 1) != 0:
        raise ArithmeticError("sphere_control")


def wave_frame(height) -> sp.Matrix:
    return sp.eye(4) + height * N


def anholonomy_quadratic(frame: sp.Matrix, coords: list) -> sp.Expr:
    """Same axial-minus-trace combination as the merged x-only checker, all coordinates."""
    inverse = sp.simplify(frame.inv())
    full = {(a, b, c): 0 for a in range(4) for b in range(4) for c in range(4)}
    for a in range(4):
        for b in range(4):
            for c in range(b + 1, 4):
                acc = 0
                for mu, coord in enumerate(coords):
                    de = sp.diff(frame, coord)
                    for r in range(4):
                        acc += inverse[mu, b] * de[a, r] * inverse[r, c]
                        acc -= inverse[mu, c] * de[a, r] * inverse[r, b]
                value = sp.expand(acc)
                full[(a, b, c)] = value
                full[(a, c, b)] = -value
    trace = [sp.expand(sum(full[(a, a, c)] for a in range(4))) for c in range(4)]
    axial = 0
    for a, b, c in ((0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)):
        cyclic = full[(a, b, c)] + full[(b, c, a)] + full[(c, a, b)]
        axial += sp.expand(cyclic**2)
    return sp.simplify(2 * axial - 4 * sum(item**2 for item in trace))


def profile_geometry(height):
    """N-frame geometry for a transverse profile H(x, y)."""
    t, x, y, z = sp.symbols("t x y z", real=True)
    coords = [t, x, y, z]
    frame = wave_frame(height)
    positive = sp.simplify(frame.T * frame)
    lorentz = sp.simplify(frame.T * ETA * frame)
    pos_scalar, _, _ = curvature(positive, coords)
    lorentz_scalar, lorentz_ricci, lorentz_inverse = curvature(lorentz, coords)
    q_value = anholonomy_quadratic(frame, coords)
    grad2 = sp.diff(height, x) ** 2 + sp.diff(height, y) ** 2
    return {
        "coords": coords,
        "frame_det": sp.factor(frame.det()),
        "positive_det": sp.factor(positive.det()),
        "lorentz_det": sp.factor(lorentz.det()),
        "positive_scalar": pos_scalar,
        "lorentz_scalar": lorentz_scalar,
        "lorentz_ricci": lorentz_ricci,
        "lorentz_inverse": lorentz_inverse,
        "q": q_value,
        "grad2": sp.simplify(grad2),
    }


def grad_square_euler(alpha, height, test, x, y) -> tuple[sp.Expr, sp.Expr]:
    """Euler density of alpha*|grad H|^2 and the raw first variation.

    The identity el*test + div(current) = raw is the integration-by-parts check.
    """
    eps = sp.symbols("eps")
    shifted = height + eps * test
    density = alpha * (sp.diff(shifted, x) ** 2 + sp.diff(shifted, y) ** 2)
    raw = sp.simplify(sp.diff(density, eps).subs(eps, 0))
    momentum_x = sp.simplify(2 * alpha * sp.diff(height, x) * test)
    momentum_y = sp.simplify(2 * alpha * sp.diff(height, y) * test)
    el = sp.simplify(-sp.diff(2 * alpha * sp.diff(height, x), x) - sp.diff(2 * alpha * sp.diff(height, y), y))
    divergence = sp.diff(momentum_x, x) + sp.diff(momentum_y, y)
    if sp.simplify(el * test + divergence - raw) != 0:
        raise ArithmeticError("integration_by_parts")
    return el, raw


def solution_height():
    x, y = sp.symbols("x y", real=True)
    source, palatini_c, polarization = sp.symbols("s c a", nonzero=True)
    height = (source**2 / (4 * palatini_c) + polarization) * x**2 + (
        source**2 / (4 * palatini_c) - polarization
    ) * y**2
    return height, x, y, source, palatini_c, polarization


def brinkmann_solution() -> dict:
    """Tensor check of synthesis solution (25) in coordinates (u, v, x, y)."""
    u, v, x, y = sp.symbols("u v x y", real=True)
    height, _, _, source, palatini_c, _ = solution_height()
    metric = sp.zeros(4)
    metric[0, 0] = height
    metric[0, 1] = 1
    metric[1, 0] = 1
    metric[2, 2] = -1
    metric[3, 3] = -1
    scalar, ricci, inverse = curvature(metric, [u, v, x, y])
    einstein = sp.simplify(ricci - sp.Rational(1, 2) * metric * scalar)
    stress = sp.zeros(4)
    stress[0, 0] = source**2
    psi = source * u
    kinetic = sp.simplify(sum(inverse[i, j] * sp.diff(psi, [u, v, x, y][i]) * sp.diff(psi, [u, v, x, y][j]) for i in range(4) for j in range(4)))
    volume = sp.sqrt(-metric.det())
    box_vector = sp.Matrix([sp.simplify(sum(volume * inverse[i, j] * sp.diff(psi, [u, v, x, y][j]) for j in range(4))) for i in range(4)])
    box = sp.simplify(sum(sp.diff(box_vector[i], [u, v, x, y][i]) for i in range(4)) / volume)
    return {
        "det": sp.factor(metric.det()),
        "scalar": scalar,
        "ricci_uu": sp.simplify(ricci[0, 0]),
        "gap": sp.simplify(2 * palatini_c * einstein - stress),
        "kinetic": kinetic,
        "box": box,
        "raised_uu": sp.simplify(inverse[0, 0]),
    }


def trace_reversal_involution(dimension: int) -> sp.Matrix:
    entries = sp.Matrix(dimension, dimension, lambda i, j: sp.symbols(f"m{dimension}_{i}{j}"))
    trace = sp.Trace(entries).doit()
    once = sp.simplify(entries - trace * sp.eye(dimension) / 2)
    twice = sp.simplify(once - sp.Trace(once).doit() * sp.eye(dimension) / 2)
    return sp.simplify(twice - entries)


def metric_reversal_involution() -> sp.Matrix:
    """sigma(V)=V-(g/2)Tr(g^{-1}V) on the wave metric, all 10 symmetric slots.

    The audited carrier is the wave metric. A second call with a diagonal
    matrix is made by the test. This does not quantify over every metric.
    """
    height = sp.symbols("H")
    metric = sp.simplify(ETA + height * (K * K.T))
    variation = sp.zeros(4)
    for i in range(4):
        for j in range(i, 4):
            symbol = sp.symbols(f"v{i}{j}")
            variation[i, j] = symbol
            variation[j, i] = symbol
    inverse = sp.simplify(metric.inv())
    contracted = sp.simplify(sp.Trace(inverse * variation).doit())
    once = sp.simplify(variation - metric * contracted / 2)
    twice_contracted = sp.simplify(sp.Trace(inverse * once).doit())
    twice = sp.simplify(once - metric * twice_contracted / 2)
    return sp.simplify(twice - variation)


def kl_simplex(count: int = 3) -> dict:
    weights = sp.Matrix(count, 1, lambda i, _: sp.symbols(f"w{i}", positive=True))
    reference = sp.Matrix(count, 1, lambda i, _: sp.symbols(f"r{i}", positive=True))
    step = sp.Matrix(count, 1, lambda i, _: sp.symbols(f"dw{i}"))
    reference_step = sp.Matrix(count, 1, lambda i, _: sp.symbols(f"dr{i}"))
    kl = sum(weights[i] * sp.log(weights[i] / reference[i]) for i in range(count))
    gradient = sp.Matrix([sp.diff(kl, weights[i]) for i in range(count)])
    reference_gradient = sp.Matrix([sp.diff(kl, reference[i]) for i in range(count)])
    at_equilibrium = {weights[i]: reference[i] for i in range(count)}
    grad_eq = sp.simplify(gradient.subs(at_equilibrium))
    ref_eq = sp.simplify(reference_gradient.subs(at_equilibrium))
    hessian = sp.zeros(count)
    for i in range(count):
        for j in range(count):
            hessian[i, j] = sp.diff(gradient[i], weights[j])
    hessian_eq = sp.simplify(hessian.subs(at_equilibrium))
    quadratic = sp.simplify((step.T * hessian_eq * step)[0])
    return {
        "weight_gradient_at_equilibrium": grad_eq,
        "weight_contraction": sp.simplify(sum(grad_eq[i] * step[i] for i in range(count))),
        "reference_gradient_at_equilibrium": ref_eq,
        "reference_contraction": sp.simplify(sum(ref_eq[i] * reference_step[i] for i in range(count))),
        "hessian_quadratic": quadratic,
    }
