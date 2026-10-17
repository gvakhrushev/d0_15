"""Executable controls for the candidate moving-scale Euler table.

Negative controls falsify a stated conclusion. An exception in the arithmetic
is a coding error, not one of those falsifications.
"""

from __future__ import annotations

import itertools
import pathlib
import sys
import unittest

import sympy as sp

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import moving_scale as ms


def christoffel(g, dg):
    inv = [1 / g[i] for i in range(4)]
    gamma = [[[0 for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for k, i, j in itertools.product(range(4), repeat=3):
        acc = 0
        if j == k:
            acc += dg[i][j]
        if i == k:
            acc += dg[j][i]
        if i == j:
            acc -= dg[k][i]
        gamma[k][i][j] = inv[k] * acc / 2
    return gamma


def curvature(g, dg, d2g):
    gamma = christoffel(g, dg)
    inv = [1 / g[i] for i in range(4)]
    dgamma = [[[[0 for _ in range(4)] for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for m, k, i, j in itertools.product(range(4), repeat=4):
        acc = 0
        if j == k:
            acc += d2g[m][i][j]
        if i == k:
            acc += d2g[m][j][i]
        if i == j:
            acc -= d2g[m][k][i]
        dgamma[m][k][i][j] = inv[k] * acc / 2 - (dg[m][k] / g[k]) * gamma[k][i][j]
    riem_up = [[[[0 for _ in range(4)] for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for r, s, m, n in itertools.product(range(4), repeat=4):
        acc = dgamma[m][r][n][s] - dgamma[n][r][m][s]
        for lam in range(4):
            acc += gamma[r][m][lam] * gamma[lam][n][s]
            acc -= gamma[r][n][lam] * gamma[lam][m][s]
        riem_up[r][s][m][n] = acc
    ric = [[0 for _ in range(4)] for _ in range(4)]
    for s, n in itertools.product(range(4), repeat=2):
        ric[s][n] = sum(riem_up[r][s][r][n] for r in range(4))
    scalar = sum(inv[s] * ric[s][s] for s in range(4))
    riem2 = 0
    ric2 = 0
    for a, s, m, n in itertools.product(range(4), repeat=4):
        lowered = g[a] * riem_up[a][s][m][n]
        riem2 += lowered * inv[a] * inv[s] * inv[m] * inv[n] * lowered
    for a, s in itertools.product(range(4), repeat=2):
        ric2 += ric[a][s] * inv[a] * inv[s] * ric[a][s]
    return {
        "gamma": gamma,
        "Ric": ric,
        "R": scalar,
        "E4": riem2 - 4 * ric2 + scalar**2,
        "Riem_up": riem_up,
        "inv": inv,
    }


def one_var(gvals, d1, d2):
    g = list(gvals)
    dg = [[0 for _ in range(4)] for _ in range(4)]
    d2g = [[[0 for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for i in range(4):
        dg[0][i] = d1[i]
        d2g[0][0][i] = d2[i]
    return g, dg, d2g


def r_short(b, c, d, b1, c1, d1, b2, c2, d2):
    return (
        -b2 / b
        + b1**2 / (2 * b**2)
        - c2 / c
        + c1**2 / (2 * c**2)
        - d2 / d
        + d1**2 / (2 * d**2)
        - b1 * c1 / (2 * b * c)
        - b1 * d1 / (2 * b * d)
        - c1 * d1 / (2 * c * d)
    )


class FamilyIdentities(unittest.TestCase):
    def test_sign_controls(self):
        one = sp.Integer(1)
        g, dg, d2g = one_var([one, one, one, one], [0, 0, 0, 0], [0, -2, 0, 0])
        sphere = curvature(g, dg, d2g)
        self.assertEqual(sp.simplify(sphere["R"] - 2), 0)
        self.assertEqual(sp.simplify(sphere["E4"]), 0)

        g = [sp.Integer(1)] * 4
        dg = [[0 for _ in range(4)] for _ in range(4)]
        d2g = [[[0 for _ in range(4)] for _ in range(4)] for _ in range(4)]
        d2g[0][0][1] = -2
        d2g[2][2][3] = -2
        product = curvature(g, dg, d2g)
        self.assertEqual(sp.simplify(product["R"]), 4)
        self.assertEqual(sp.simplify(product["E4"]), 8)

    def test_e4_is_the_transgression_and_matches_the_closed_euler(self):
        b, c, d = sp.symbols("b c d", positive=True)
        b1, c1, d1 = sp.symbols("b1 c1 d1")
        b2, c2, d2 = sp.symbols("b2 c2 d2")
        f1, f2 = sp.symbols("f1 f2")
        g, dg, d2g = one_var([1, b, c, d], [0, b1, c1, d1], [0, b2, c2, d2])
        curv = curvature(g, dg, d2g)
        self.assertEqual(sp.simplify(curv["R"] - r_short(b, c, d, b1, c1, d1, b2, c2, d2)), 0)
        vol = sp.sqrt(b * c * d)
        capital = b1 * c1 * d1 / vol
        d_capital = (
            sp.diff(capital, b) * b1
            + sp.diff(capital, c) * c1
            + sp.diff(capital, d) * d1
            + sp.diff(capital, b1) * b2
            + sp.diff(capital, c1) * c2
            + sp.diff(capital, d1) * d2
        )
        self.assertEqual(sp.simplify(sp.together(curv["E4"] * vol - d_capital)), 0)

        density = -f1 * capital
        jets = [b, c, d, b1, c1, d1, f1]
        ders = [b1, c1, d1, b2, c2, d2, f2]

        def total(expr):
            return sum(sp.diff(expr, var) * der for var, der in zip(jets, ders))

        for name, q, q1, slot in (("b", b, b1, 0), ("c", c, c1, 1), ("d", d, d1, 2)):
            el = sp.diff(density, q) - total(sp.diff(density, q1))
            closed = ms.e4_family_contravariant(b, c, d, b1, c1, d1, b2, c2, d2, f1, f2)[slot]
            self.assertEqual(sp.simplify(el / vol - closed), 0)

    def test_constant_coefficient_bulk_vanishes_and_field_dependent_does_not(self):
        zero = ms.e4_family_contravariant(2, 3, 5, 1, -1, 4, 7, 8, 9, 0, 0)
        self.assertEqual(zero, (0, 0, 0))
        witness = ms.e4_family_contravariant(1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1)
        self.assertEqual(witness[0], 1)
        self.assertNotEqual(witness, (0, 0, 0))

    def test_einstein_hilbert_matches_the_owned_tensor(self):
        b, c, d = sp.symbols("b c d", positive=True)
        b1, c1, d1 = sp.symbols("b1 c1 d1")
        b2, c2, d2 = sp.symbols("b2 c2 d2")
        b3, c3, d3 = sp.symbols("b3 c3 d3")
        b4, c4, d4 = sp.symbols("b4 c4 d4")
        f, f1, f2 = sp.symbols("f f1 f2")
        f3, f4 = sp.symbols("f3 f4")
        vol = sp.sqrt(b * c * d)
        lagrangian = f * r_short(b, c, d, b1, c1, d1, b2, c2, d2) * vol
        pairs = [
            (b, b1), (c, c1), (d, d1),
            (b1, b2), (c1, c2), (d1, d2),
            (b2, b3), (c2, c3), (d2, d3),
            (b3, b4), (c3, c4), (d3, d4),
            (f, f1), (f1, f2), (f2, f3), (f3, f4),
        ]

        def ddx(expr):
            return sum(sp.diff(expr, var) * der for var, der in pairs)

        def euler(q, q1, q2):
            return sp.diff(lagrangian, q) - ddx(sp.diff(lagrangian, q1)) + ddx(ddx(sp.diff(lagrangian, q2)))

        g, dg, d2g = one_var([1, b, c, d], [0, b1, c1, d1], [0, b2, c2, d2])
        curv = curvature(g, dg, d2g)
        gamma = curv["gamma"]
        inv = curv["inv"]
        hess = [[0 for _ in range(4)] for _ in range(4)]
        for i, j in itertools.product(range(4), repeat=2):
            acc = f2 if i == j == 0 else 0
            hess[i][j] = acc - gamma[0][i][j] * f1
        box = sum(inv[i] * hess[i][i] for i in range(4))
        for slot, q, q1, q2 in ((1, b, b1, b2), (2, c, c1, c2), (3, d, d1, d2)):
            ric_up = inv[slot] * inv[slot] * curv["Ric"][slot][slot]
            einstein = ric_up - sp.Rational(1, 2) * curv["R"] * inv[slot]
            raised_hess = inv[slot] * inv[slot] * hess[slot][slot]
            owned = (-f * einstein + raised_hess - inv[slot] * box) * vol
            self.assertEqual(sp.simplify(euler(q, q1, q2) - owned), 0)
            self.assertEqual(sp.simplify(sp.diff(lagrangian, f) - curv["R"] * vol), 0)

    def test_boundary_flux_on_the_transverse_slot(self):
        b, c, d = sp.symbols("b c d", positive=True)
        b1, c1, d1 = sp.symbols("b1 c1 d1")
        b2, c2, d2 = sp.symbols("b2 c2 d2")
        b3 = sp.symbols("b3")
        f, f1 = sp.symbols("f f1")
        beta, beta1 = sp.symbols("beta beta1")
        vol = sp.sqrt(b * c * d)
        lagrangian = f * r_short(b, c, d, b1, c1, d1, b2, c2, d2) * vol
        pairs = [
            (b, b1), (c, c1), (d, d1),
            (b1, b2), (c1, c2), (d1, d2),
            (b2, b3), (f, f1),
        ]

        def ddx(expr):
            return sum(sp.diff(expr, var) * der for var, der in pairs)

        endpoint = (sp.diff(lagrangian, b1) - ddx(sp.diff(lagrangian, b2))) * beta + sp.diff(lagrangian, b2) * beta1
        inv = [1, 1 / b, 1 / c, 1 / d]
        slopes = {1: b1, 2: c1, 3: d1}

        def gamma(k, i, j):
            def partial(coord, comp):
                return slopes.get(comp, 0) if coord == 0 else 0

            acc = 0
            if j == k:
                acc += partial(i, j)
            if i == k:
                acc += partial(j, i)
            if i == j:
                acc -= partial(k, i)
            return inv[k] * acc / 2

        v_up = beta / b**2
        div = gamma(0, 1, 1) * v_up
        tau = beta / b
        d_tau = sp.diff(tau, b) * b1 + sp.diff(tau, beta) * beta1
        w0 = sp.together(div - d_tau)
        bracket = f * w0 + tau * f1
        self.assertEqual(sp.simplify(endpoint - vol * bracket), 0)
        dropped_tau = sp.simplify(endpoint - vol * (f * w0))
        self.assertNotEqual(dropped_tau, 0)
        # Endpoint value of β does not fix the flux: the coefficient of β' is nonzero.
        coeff_beta1 = sp.simplify(sp.diff(endpoint, beta1).subs({b: 1, c: 1, d: 1, f: 1}))
        self.assertEqual(coeff_beta1, -1)

    def test_normal_slot_uses_the_gradient_contraction(self):
        a, b = sp.symbols("a b", positive=True)
        a1, b1 = sp.symbols("a1 b1")
        a2, b2 = sp.symbols("a2 b2")
        a3, b3 = sp.symbols("a3 b3")
        f, f1 = sp.symbols("f f1")
        alpha, alpha1 = sp.symbols("alpha alpha1")
        g, dg, d2g = one_var([a, b, 1, 1], [a1, b1, 0, 0], [a2, b2, 0, 0])
        scalar = curvature(g, dg, d2g)["R"]
        vol = sp.sqrt(a * b)
        lagrangian = f * scalar * vol
        pairs = [
            (a, a1), (b, b1), (a1, a2), (b1, b2), (a2, a3), (b2, b3), (f, f1),
        ]

        def ddx(expr):
            return sum(sp.diff(expr, var) * der for var, der in pairs)

        endpoint = (sp.diff(lagrangian, a1) - ddx(sp.diff(lagrangian, a2))) * alpha + sp.diff(lagrangian, a2) * alpha1
        inv = [1 / a, 1 / b, 1, 1]
        slopes = {0: a1, 1: b1}

        def gamma_component(k, i, j):
            def partial(coord, comp):
                return slopes.get(comp, 0) if coord == 0 else 0

            acc = 0
            if j == k:
                acc += partial(i, j)
            if i == k:
                acc += partial(j, i)
            if i == j:
                acc -= partial(k, i)
            return inv[k] * acc / 2

        v_up = alpha / a**2
        div = sp.diff(v_up, a) * a1 + sp.diff(v_up, alpha) * alpha1
        for nu, lam in itertools.product(range(4), repeat=2):
            if lam == nu == 0:
                div += gamma_component(0, nu, lam) * v_up
            if lam == 0:
                div += gamma_component(nu, nu, lam) * v_up
        tau = alpha / a
        d_tau = sp.diff(tau, a) * a1 + sp.diff(tau, alpha) * alpha1
        w0 = div - inv[0] * d_tau
        n_down = sp.sqrt(a)
        n_up = 1 / sp.sqrt(a)
        grad_f_v_n = f1 * v_up * n_down
        bracket = f * w0 - grad_f_v_n + tau * n_up * f1
        self.assertEqual(sp.simplify(endpoint - vol * bracket), 0)
        self.assertNotEqual(sp.simplify(endpoint - vol * (f * w0 + tau * n_up * f1)), 0)


class LorentzAndTransport(unittest.TestCase):
    def test_section7_flat_positive_metric_has_nonzero_lorentz_einstein(self):
        kk = sp.symbols("kk", positive=True)
        g = [sp.Integer(1), sp.Integer(-1), sp.Integer(-1), sp.Integer(-1)]
        dg = [[0, 0, 0, 0] for _ in range(4)]
        d2g = [[[0, 0, 0, 0] for _ in range(4)] for _ in range(4)]
        d2g[1][1][0] = -4 * kk**2
        d2g[1][1][1] = -4 * kk**2
        curv = curvature(g, dg, d2g)
        self.assertEqual(sp.simplify(curv["R"] + 4 * kk**2), 0)
        inv = curv["inv"]
        slot = 2
        einstein = inv[slot] ** 2 * curv["Ric"][slot][slot] - sp.Rational(1, 2) * curv["R"] * inv[slot]
        self.assertEqual(sp.simplify(einstein + 2 * kk**2), 0)
        zero = sp.Integer(0)
        one = sp.Integer(1)
        flat = curvature([one, one, one, one], [[zero] * 4 for _ in range(4)], [[[zero] * 4 for _ in range(4)] for _ in range(4)])
        self.assertEqual(sp.simplify(flat["R"]), 0)

    def test_quadratic_observer_algebra(self):
        theta, sigma, omega = sp.symbols("theta sigma Omega")
        shear_square = sigma**2 + theta**2 / 3
        lhs = sp.Rational(4, 3) * theta**2 - 2 * sigma**2 - 2 * omega**2
        rhs = 2 * (theta**2 - shear_square - omega**2)
        self.assertEqual(sp.simplify(lhs - rhs), 0)

    def test_source_transport_keeps_current_orthogonality(self):
        s, q, p = sp.symbols("s q p", positive=True)
        base = sp.diag(s, 1, 1, 1)
        current = sp.Matrix([q, 1, 0, 0])
        euler = sp.Matrix([[1, 2, 0, 0], [2, 3, 0, 0], [0, 0, 4, 0], [0, 0, 0, 5]])

        def reflected(metric):
            leg = sp.simplify(metric * current)
            kappa = sp.simplify((current.T * metric * current)[0])
            positive = sp.simplify(-metric + 2 * leg * leg.T / kappa)
            pairing = sum(euler[i, j] * positive[i, j] for i in range(4) for j in range(4))
            zed = sp.simplify(euler * leg)
            s0 = sp.simplify((leg.T * euler * leg)[0])
            metric_source = sp.simplify(
                -euler + (2 / kappa) * (zed * current.T + current * zed.T) - (2 * s0 / kappa**2) * current * current.T
            )
            current_source = sp.simplify((4 / kappa) * (metric * zed - (s0 / kappa) * leg))
            return pairing, metric_source, current_source, kappa

        pairing, metric_source, current_source, _kappa = reflected(base)
        self.assertEqual(sp.simplify((current_source.T * current)[0]), 0)
        self.assertEqual(sp.simplify(sp.diff(pairing, s) - metric_source[0, 0]), 0)
        self.assertEqual(sp.simplify(sp.diff(pairing, q) - current_source[0]), 0)
        moved = base.copy()
        moved[0, 1] = moved[1, 0] = p
        pairing_p, metric_p, _current_p, _kappa_p = reflected(moved)
        pair = sp.simplify((metric_p[0, 1] + metric_p[1, 0]).subs(p, 0))
        self.assertEqual(sp.simplify(sp.diff(pairing_p, p).subs(p, 0) - pair), 0)


class NormalizersAndPullback(unittest.TestCase):
    def test_volume_source_and_centered_cancellation(self):
        self.assertEqual(ms.volume_source_factor(sp.Integer(7)), sp.Rational(7, 2))
        self.assertEqual(ms.volume_source_frobenius_square(7), 49)
        prices = (sp.Integer(0), sp.Integer(4))
        weights = (sp.Integer(1), sp.Integer(3))
        d_weights = (sp.Integer(1), sp.Integer(-1))
        d_prices = (sp.Integer(0), sp.Integer(2))
        bare, average = ms.centered_directional(weights, prices, d_weights, d_prices)
        shifted, average_k = ms.centered_directional(
            weights, tuple(price + 5 for price in prices), d_weights, d_prices
        )
        self.assertEqual(bare, shifted)
        self.assertEqual(average_k - average, 5)

    def test_two_normalizers_and_the_observer_slope(self):
        centered, _average = ms.centered_directional(
            (sp.Integer(1), sp.Integer(1)),
            (sp.Integer(0), sp.Integer(4)),
            (sp.Integer(1), sp.Integer(0)),
            (sp.Integer(0), sp.Integer(0)),
        )
        prepared = ms.preparation_directional(sp.Integer(1), sp.Integer(2), sp.Integer(1))
        self.assertEqual(centered, -1)
        self.assertEqual(prepared, sp.Rational(-1, 2))
        self.assertNotEqual(centered, prepared)
        # Observer on the second cell only: A=(0+4 θ u(c))/2, slope in θ is 2 u(c).
        u_c = sp.symbols("u_c")
        theta = sp.symbols("theta")
        slope = sp.diff((4 * theta * u_c) / 2, theta)
        self.assertEqual(sp.simplify(slope), 2 * u_c)
        self.assertNotEqual(sp.simplify(slope.subs(u_c, 1)), 0)

    def test_partial_t_freeze_and_flat_hessian(self):
        full, frozen_zone, frozen_numerator = ms.quotient_t_derivatives(sp.Integer(1))
        self.assertEqual(full, sp.Rational(1, 2))
        self.assertEqual(frozen_zone, 1)
        self.assertEqual(frozen_numerator, sp.Rational(-1, 2))
        self.assertNotEqual(full, frozen_zone)
        self.assertEqual(ms.flat_partial_freeze_yy(sp.Integer(3)), -6)

    def test_chain_rule_then_finite_cut(self):
        p = (sp.sqrt(5) - 1) / 2
        self.assertEqual(sp.simplify(p + p**2 - 1), 0)
        gamma = 2 * p**6
        alpha, t = sp.symbols("alpha t", positive=True)
        d_alpha, d_t = sp.symbols("d_alpha d_t")
        coefficient = ms.chain_coefficient(gamma, alpha, t)
        differential = ms.chain_differential(gamma, alpha, t, d_alpha, d_t)
        self.assertEqual(sp.simplify(sp.diff(gamma * alpha * t**2 / 2, t) * d_t + sp.diff(gamma * alpha * t**2 / 2, alpha) * d_alpha - differential), 0)
        self.assertEqual(sp.simplify(coefficient - gamma * alpha * t**2 / 2), 0)
        f0, f1 = sp.symbols("f0 f1")
        step, x_next, y_next = ms.finite_alpha_step(p, sp.Integer(3), sp.Integer(5), f0, f1)
        self.assertEqual(sp.simplify(x_next - ((3 + 5) - p**2 * 3)), 0)
        self.assertEqual(sp.simplify(step - p**2 * (f0 - f1) * (x_next - 3)), 0)
        ratio = ((-p**2) - 1) / sp.log(-p**2)
        self.assertNotEqual(sp.simplify(ratio - 1), 0)
        # Spatially constant cut, moving t: u(Δc) = γ (Δα) t u(t).
        u_t, delta = sp.symbols("u_t delta")
        directional = sp.simplify(gamma * delta * t * u_t)
        self.assertNotEqual(directional.subs({delta: 1, t: 1, u_t: 1}), 0)

    def test_l1_of_the_coefficient_does_not_control_the_box(self):
        x = sp.symbols("x")
        self.assertEqual(sp.integrate(x**2, (x, 0, 1)), sp.Rational(1, 3))
        self.assertEqual(sp.diff(x**2, x, 2), 2)
        self.assertEqual(sp.diff(sp.Rational(1, 3), x, 2), 0)

    def test_measure_slot_stays_out_of_the_einstein_tensor(self):
        missing = ms.measure_slot(None, error=sp.Integer(4), d_error=sp.Integer(1))
        self.assertEqual(missing["status"], "unevaluated")
        self.assertIsNone(missing["error"])
        self.assertFalse(missing["absorbed_into_G"])
        supplied = ms.measure_slot(("cell",), error=sp.Integer(4), d_error=sp.Integer(1))
        self.assertEqual(supplied["status"], "supplied")
        self.assertFalse(supplied["absorbed_into_G"])
        self.assertNotEqual(supplied["error"], 0)


class SpanRejection(unittest.TestCase):
    def test_curvature_hessian_columns_do_not_span_the_family_euler(self):
        seeds = [
            (1, 2, 3, 1, -1, 2, 0, 1, -2, 3, 5),
            (2, 1, 4, -1, 2, 1, 3, 0, 1, -2, 1),
            (3, 5, 2, 2, 2, -1, 1, -1, 2, 4, -3),
            (4, 3, 2, 0, 1, -1, 2, 3, 0, 1, 1),
        ]
        rows = []
        targets = []
        for seed in seeds:
            values = list(map(sp.Integer, seed))
            b, c, d, b1, c1, d1, b2, c2, d2, f1, f2 = values
            g, dg, d2g = one_var([1, b, c, d], [0, b1, c1, d1], [0, b2, c2, d2])
            curv = curvature(g, dg, d2g)
            gamma = curv["gamma"]
            hess = [[0 for _ in range(4)] for _ in range(4)]
            for i, j in itertools.product(range(4), repeat=2):
                acc = f2 if i == j == 0 else 0
                hess[i][j] = acc - gamma[0][i][j] * f1
            inv = curv["inv"]
            box = sum(inv[i] * hess[i][i] for i in range(4))
            ric = curv["Ric"]
            scalar = curv["R"]
            tg = ms.e4_family_contravariant(b, c, d, b1, c1, d1, b2, c2, d2, f1, f2)
            for slot, target in zip((1, 2, 3), tg):
                ric_hess = 0
                for lam in range(4):
                    ric_hess += (inv[slot] * inv[lam] * ric[slot][lam]) * (inv[slot] * hess[lam][slot])
                ric_hess *= 2
                ric_box = inv[slot] * inv[slot] * ric[slot][slot] * box
                ric_double = sum(inv[a] * inv[b] * ric[a][b] * hess[a][b] for a, b in itertools.product(range(4), repeat=2))

                def rup(a, s, m, n, slot=slot):
                    return inv[a] * inv[s] * inv[m] * inv[n] * curv["Riem_up"][a][s][m][n] * g[a]

                r_forms = []
                for kind in range(4):
                    acc = 0
                    for a, bb in itertools.product(range(4), repeat=2):
                        if kind == 0:
                            comp = rup(slot, a, slot, bb)
                        elif kind == 1:
                            comp = rup(slot, a, bb, slot)
                        elif kind == 2:
                            comp = rup(a, slot, slot, bb)
                        else:
                            comp = rup(a, bb, slot, slot)
                        acc += comp * hess[a][bb]
                    r_forms.append(acc)
                cols = [
                    scalar * inv[slot] * inv[slot] * hess[slot][slot],
                    inv[slot] * scalar * box,
                    ric_hess,
                    inv[slot] * ric_double,
                    ric_box,
                    *r_forms,
                ]
                rows.append([sp.together(col) for col in cols])
                targets.append(sp.together(target))
        matrix = sp.Matrix(rows)
        augmented = matrix.row_join(sp.Matrix(targets))
        self.assertLess(matrix.rank(), augmented.rank())


if __name__ == "__main__":
    unittest.main()
