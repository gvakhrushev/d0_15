#!/usr/bin/env python3
"""Reproducible checks for the explicit-price continuation, standard library only.

Exact Q(sqrt(5)) and rational checks are distinguished from Decimal/complex
diagnostics. Analytic uniform-in-cap/domain theorems are in the companion
proofs; a finite sampling of caps is not their proof. No native lattice,
protected-history compiler, or full coupled perturbation replay is claimed.
"""
from __future__ import annotations

import cmath
from decimal import Decimal as D, getcontext
from fractions import Fraction as Q
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
PARENT_CHECKER = HERE.parent / "d0_complete_price_nonvacuum_normal_form_2026-10-21" / "check_nonvacuum_normal_form.py"
spec = importlib.util.spec_from_file_location("prior_normal_form", PARENT_CHECKER)
old = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = old
spec.loader.exec_module(old)
getcontext().prec = 90


def polynomial_detector(x, y, p, z):
    v = p + p**2 * y
    bb = 4 * v**2 * (1 - v**2)
    ee = p**2 * (1 + x)
    ell = 4 * ee * (1 - ee)
    aa = ell + (1 - ell) * bb
    return 1 - (1 - z * bb) * (1 - z * aa)


def exact_detector_and_uniform_constants():
    G = old.Golden
    p, z = G(0, 1), Q(1, 2**20)
    qq, rr = 1 - z * (1 - p**6), 1 - z * (1 - p**12)
    by, byy = 8*p**6, 8*p**4*(1-6*p**2)
    ax, ay = 4*p**11, p**6*by
    axx, axy, ayy = -8*p**10, -4*p**5*by, p**6*byy
    rx, ry = z*qq*ax, z*(rr*by+qq*ay)
    rxx, rxy = z*qq*axx, z*qq*axy-z**2*by*ax
    ryy = z*(rr*byy+qq*ayy)-2*z**2*by*ay
    rho = ry / rx
    sz = -(rho**2 * rxx + 2 * rho * rxy + ryy) / ry
    closed_sz = 45 + 31 / p - 32 * z * p**5 / qq + 16 * z * p**12 / (rr + p**6 * qq)
    assert sz == closed_sz
    assert (sz - 4).sign() > 0 and (97 - sz).sign() > 0
    assert (G(Q(16, 5) * z) - 4 * ry).sign() > 0
    assert (rx.sign(), ry.sign(), rxx.sign(), rxy.sign(), ryy.sign()) == (1, 1, -1, -1, -1)

    # Exact values at nonzero points check the reorganized polynomial; its
    # identity for all arguments follows by expansion in the proof.
    for x, y in [(Q(1, 97), Q(-1, 4096)), (Q(-1, 101), Q(1, 4096)), (Q(0), Q(0))]:
        v = p + p**2 * y
        w = 1 - 2 * v**2
        cc = 1 - z + z * w**2
        aa = 4 * p**5 * z * cc * w**2
        rr_y = 1 - cc * (1 - z + z * p**6 * w**2)
        assert polynomial_detector(G(x), G(y), p, z) == rr_y + aa * (x - x**2 / p)

    eps = Q(1, 4096)
    discriminant_lower = Q(255, 256)**2 - 720 * eps
    assert discriminant_lower == Q(53505, 65536) > Q(3, 4)
    assert Q(17, 57) - Q(3, 256) > Q(1, 4)
    assert 202 * eps < Q(1, 16)
    d = 1 - 2 * z
    positive_outer_bound = Q(4, 5) / d**2 + 32 * z / d**3
    negative_outer_bound_magnitude = Q(128, 5) * z / d**2
    assert positive_outer_bound < 1
    assert negative_outer_bound_magnitude < 1
    assert 1 - 182 * z + 60 * z**2 - 40 * z**3 > 0
    return {
        "status": "PASS",
        "arithmetic": "exact Q(sqrt(5)) and rational arithmetic",
        "S_z_closed_identity": True,
        "S_z_decimal_display": str(sz.decimal()),
        "discriminant_strict_lower_bound": str(discriminant_lower),
        "all_cap_outer_upper_bound_below_one": str(positive_outer_bound),
        "uniform_interval_Y": "|Y| < 2^-13, analytic proof required and supplied",
    }


def explicit_trace(y):
    p = (D(5).sqrt() - 1) / 2
    z = D(1) / D(2)**20
    v = p + p**2 * y
    w, wp = 1 - 2 * v**2, -4 * p**2 * v
    cc = 1 - z + z * w**2
    aa = 4 * p**5 * z * cc * w**2
    hh = (1 - z) * (1 + p**6) + 2 * z * p**6 * w**2
    rr_over_a = -wp * hh / (2 * p**5 * w * cc)
    a_log_derivative = 2 * wp / w * (1 + z * w**2 / cc)
    kk = -y * a_log_derivative
    discriminant = (1 + kk)**2 - 4 * (2 + kk) * y * rr_over_a / p
    tau = 2 * y * rr_over_a / (1 + kk + discriminant.sqrt())
    return tau, aa, discriminant


def decimal_branch_and_auxiliary_checks():
    z, eps = D(2)**-20, D(2)**-12
    parameters = [(D(3)/5, D(5)/7, D(54)), (D(1), D(1), D("53.0001")), (D(2), D("0.001"), D(1000))]
    samples = [eps * D(j) / 4 for j in range(-4, 5)]
    worst_trace, worst_aux, worst_newton_difference = D(0), D(0), D(0)
    rows = []
    for params in parameters:
        for cap in (1, 2, 7, 31):
            f0 = old.price_jet(D(0), D(0), cap, *params)
            a, b = f0[1], f0[2]
            rho = b / a
            kpp = f0[5] + 2 * rho * f0[4] + rho**2 * f0[3]
            theta = kpp / b
            assert -128 < theta < -3
            assert kpp > 0 if cap == 1 else kpp < 0
            assert f0[6] < 0 if cap == 1 else f0[6] > 10 * params[0] * params[1]
            min_u, max_u, min_yprime = D(2), D(0), D(2)
            for y in samples:
                tau, aa, disc = explicit_trace(y)
                r, rx, ry, rxx, rxy, ryy = old.detector_jet(tau, y)
                trace = tau * rx - y * ry
                worst_trace = max(worst_trace, abs(trace / aa))
                assert abs(trace / aa) < D("1e-72")
                assert z < r < 2 * z and disc > D(3) / 4
                assert abs(tau) <= 48 * abs(y)
                tx = rx + tau * rxx - y * rxy
                ty = tau * rxy - ry - y * ryy
                tauprime = -ty / tx
                assert 0 < tauprime < 50
                assert abs(tx / aa - disc.sqrt()) < D("1e-72")
                f = old.price_jet(tau, y, cap, *params)
                pi, u = f[1], f[1] / a
                yy = y / u
                ulogprime = (f[3] * tauprime + f[4]) / pi
                yprime = (1 - y * ulogprime) / u
                assert D(15)/16 < u < D(16)/15
                assert abs(ulogprime) < 202 and yprime > 0
                min_u, max_u = min(min_u, u), max(max_u, u)
                min_yprime = min(min_yprime, yprime)
                aux = yy / a * f[2] - tau
                worst_aux = max(worst_aux, abs(aux))
                assert abs(aux) < D("1e-72")
                if y:
                    second_radial = f[6] * tx * (tau + y * tauprime)
                    expected_positive = (y > 0 and cap >= 2) or (y < 0 and cap == 1)
                    assert (second_radial > 0) == expected_positive
                    # Verify the same curvature directly from the full price jet.
                    direct = tau**2*f[3] - 2*tau*y*f[4] + y**2*f[5] + tau*f[1] + y*f[2]
                    assert abs((direct - second_radial) / max(abs(second_radial), D("1e-70"))) < D("1e-70")
                if params == parameters[0] and abs(y) == eps:
                    # An independent Newton route checks the explicit algebraic
                    # parametrization against the original auxiliary equations.
                    solved = old.solve_auxiliary(yy, cap, params, a)
                    normalized_k = f[0] - f0[0] - pi * tau
                    difference = max(abs(solved[2]-tau), abs(solved[3]-u), abs(solved[0]-f0[0]-normalized_k))
                    worst_newton_difference = max(worst_newton_difference, difference)
                    assert difference < D("1e-60")
            rows.append({"cap": cap, "parameters": [str(v) for v in params], "theta": str(theta), "u_min": str(min_u), "u_max": str(max_u), "Yprime_min": str(min_yprime)})
    return {
        "status": "PASS",
        "arithmetic": "90-digit Decimal diagnostics; not interval certificates",
        "scope": "12 cap/parameter choices, 9 points each; uniform statements are proved analytically",
        "worst_normalized_trace_residual": str(worst_trace),
        "worst_auxiliary_residual": str(worst_aux),
        "worst_difference_from_independent_auxiliary_Newton": str(worst_newton_difference),
        "samples": rows,
    }


def mm(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def madd(a, b):
    return [[x + y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def scale(a, v):
    return [[v * x for x in row] for row in a]


def adjoint(a):
    return [[a[j][i].conjugate() for j in range(len(a))] for i in range(len(a[0]))]


def normmax(a):
    return max(abs(x) for row in a for x in row)


def rotating_transport(u, k, gamma, omega):
    """Closed-form ordered transport for C=a(cos(omega*u),sin(omega*u))."""
    identity = [[1+0j, 0j], [0j, 1+0j]]
    jj = [[0j, -1+0j], [1+0j, 0j]]
    rotation = [[math.cos(omega*u), -math.sin(omega*u)], [math.sin(omega*u), math.cos(omega*u)]]
    generator = [[-1j*k*gamma, omega+0j], [-omega+0j, 0j]]
    centered = madd(generator, scale(identity, 1j*k*gamma/2))
    nu = math.sqrt(omega**2 + (k*gamma/2)**2)
    exponential = scale(madd(scale(identity, math.cos(nu*u)), scale(centered, math.sin(nu*u)/nu)), cmath.exp(-1j*k*gamma*u/2))
    transport = mm(rotation, exponential)
    # Differentiate the closed form analytically using constant generator M.
    derivative = madd(scale(mm(mm(jj, rotation), exponential), omega), mm(rotation, mm(generator, exponential)))
    projector = [[rotation[i][0]*rotation[j][0] for j in range(2)] for i in range(2)]
    return transport, derivative, projector


def rotating_curved_wave_checks():
    params = D(3)/5, D(5)/7, D(54)
    f = old.price_jet(D(0), D(0), 7, *params)
    rho = f[2] / f[1]
    theta = float((f[5] + 2*rho*f[4] + rho**2*f[3]) / f[2])
    eta, amplitude, omega = 0.1, 0.7, 1.3
    c = -eta**2
    gamma = c * theta * amplitude**2
    identity = [[1+0j, 0j], [0j, 1+0j]]
    worst_ode = worst_unitarity = worst_wave = worst_reality = 0.0
    for u in (0.0, 0.125, 0.8, 1.7):
        for k in (0.0, 0.3, 2.1, -1.2):
            uu, du, proj = rotating_transport(u, k, gamma, omega)
            rhs = scale(mm(proj, uu), -1j*k*gamma)
            worst_ode = max(worst_ode, normmax(madd(du, scale(rhs, -1))))
            worst_unitarity = max(worst_unitarity, normmax(madd(mm(adjoint(uu), uu), scale(identity, -1))))
            um = rotating_transport(u, -k, gamma, omega)[0]
            worst_reality = max(worst_reality, normmax(madd(um, scale([[v.conjugate() for v in row] for row in uu], -1))))
            if k > 0:
                # Curved Brinkmann H=x^2+4*y^2: Ric_uu=5; nonzero traceless
                # transverse Hessian gives Weyl != 0. This is a K-sector
                # propagation fixture, not a full native-background replay.
                x, y = 0.4, -0.3
                hh = x*x + 4*y*y
                gaussian = cmath.exp(1.5j*u - k*(x*x+2*y*y)/2)
                vector = [[gaussian], [(0.2+0.4j)*gaussian]]
                zprime = scale(vector, 1.5j)
                lapz = scale(vector, k*k*hh - 3*k)
                xi = mm(uu, vector)
                xiprime = madd(mm(du, vector), mm(uu, zprime))
                wave = madd(scale(xiprime, 2j*k), madd(scale(xi, k*k*hh), scale(mm(uu, lapz), -1)))
                corrected = madd(wave, scale(mm(proj, xi), -2*gamma*k*k))
                worst_wave = max(worst_wave, normmax(corrected))
    proj0 = rotating_transport(0, 1, gamma, omega)[2]
    proj1 = rotating_transport(0.43, 1, gamma, omega)[2]
    commutator = normmax(madd(mm(proj0, proj1), scale(mm(proj1, proj0), -1)))
    assert commutator > 0.1  # This fixture genuinely needs matrix ordering.
    assert max(worst_ode, worst_unitarity, worst_wave, worst_reality) < 2e-13
    return {
        "status": "PASS", "arithmetic": "IEEE complex diagnostics with analytic matrix derivatives",
        "theta_used_cap_7": theta, "profile": "C(u)=0.7*(cos(1.3u),sin(1.3u))",
        "curved_profile_H": "x^2+4y^2", "max_generator_residual": worst_ode,
        "max_unitarity_residual": worst_unitarity, "max_reality_residual": worst_reality,
        "max_full_K_sector_wave_residual": worst_wave,
        "nonzero_projector_commutator": commutator,
        "scope": "reduced geometry held, spectator matter sources absent; not full coupled D0 equations",
    }


def exact_null_metric_check():
    hh, chi = Q(7, 3), Q(11, 5)
    metric = [[hh, 1, 0, 0], [1, 0, 0, 0], [0, 0, -1, 0], [0, 0, 0, -1]]
    effective_inverse = [[0, 1, 0, 0], [1, -hh+chi, 0, 0], [0, 0, -1, 0], [0, 0, 0, -1]]
    effective_metric = [[hh-chi, 1, 0, 0], [1, 0, 0, 0], [0, 0, -1, 0], [0, 0, 0, -1]]
    assert mm(effective_inverse, effective_metric) == [[int(i == j) for j in range(4)] for i in range(4)]
    # A generic effective null ray; its g-norm is exactly chi*(du(v))^2.
    vector = [Q(1), (Q(1, 4)+Q(1, 9)-hh+chi)/2, Q(1, 2), Q(1, 3)]
    contraction = lambda g: sum(g[i][j]*vector[i]*vector[j] for i in range(4) for j in range(4))
    assert contraction(effective_metric) == 0
    assert contraction(metric) == chi > 0
    return {"status": "PASS", "arithmetic": "exact rational", "inverse_identity": True, "nested_cone_ray_g_norm": str(chi)}



def exact_bianchi_identities():
    """All-time symbolic curvature identities in Q[t,t0], not sampled times."""
    class Poly:
        def __init__(self, coefficients):
            if not isinstance(coefficients, dict):
                coefficients = {(0, 0): Q(coefficients)}
            self.c = {k: Q(v) for k, v in coefficients.items() if v}
        def cast(self, other):
            return other if isinstance(other, Poly) else Poly(other)
        def __add__(self, other):
            other = self.cast(other)
            out = dict(self.c)
            for k, v in other.c.items():
                out[k] = out.get(k, Q(0)) + v
            return Poly(out)
        __radd__ = __add__
        def __neg__(self):
            return Poly({k: -v for k, v in self.c.items()})
        def __sub__(self, other):
            return self + -self.cast(other)
        def __rsub__(self, other):
            return self.cast(other) + -self
        def __mul__(self, other):
            other = self.cast(other)
            out = {}
            for (i, j), v in self.c.items():
                for (k, l), w in other.c.items():
                    index = i+k, j+l
                    out[index] = out.get(index, Q(0)) + v*w
            return Poly(out)
        __rmul__ = __mul__
        def __truediv__(self, scalar):
            return self * (Q(1) / scalar)
        def derivative(self):
            return Poly({(i-1, j): i*v for (i, j), v in self.c.items() if i})
        def __eq__(self, other):
            return self.c == self.cast(other).c
    t, t0 = Poly({(1, 0): 1}), Poly({(0, 1): 1})
    volume = t*(t+t0)
    denominator = 3*volume
    numerators = [2*t-t0, 2*(t+t0), 2*(t+t0)]
    # H_i=n_i/denominator. Every displayed tensor component below has
    # denominator^2, enabling exact polynomial verification for all t,t0.
    hprime = [n.derivative()*denominator-n*denominator.derivative() for n in numerators]
    riemann0i0i = [d+n*n for d, n in zip(hprime, numerators)]
    r00 = -sum(riemann0i0i)
    rii_over_a2 = [d+n*sum(numerators) for d, n in zip(hprime, numerators)]
    scalar = r00-sum(rii_over_a2)
    g00 = r00-scalar/2
    gii_over_a2 = [r+scalar/2 for r in rii_over_a2]
    assert g00 == 4*denominator
    assert all(g == 0 for g in gii_over_a2)
    assert scalar == -4*denominator
    weyl = [r-(ri-r00)/2-scalar/6 for r, ri in zip(riemann0i0i, rii_over_a2)]
    assert all(e == weight*t0*(t+t0) for e, weight in zip(weyl, (4, -2, -2)))
    assert sum(weyl) == 0
    # Volume integration, scalar current and dust conservation:
    assert sum(numerators) == 3*volume.derivative()
    assert volume.derivative()*4*denominator - volume*4*denominator.derivative() == 0

    eta, y = D("0.2"), -D(2)**-13
    xx = explicit_trace(y)[0]
    product_a = -3*xx/(4*eta**2)
    scalar_velocity_squared = -y/eta**2
    assert product_a > 0 and scalar_velocity_squared > 0
    params = D(3)/5, D(5)/7, D(54)
    worst_metric_source = D(0)
    for cap in (1, 2, 7, 31):
        f = old.price_jet(xx, y, cap, *params)
        source = (D(4)*product_a/3)*f[1]-scalar_velocity_squared*f[2]
        residual = abs(source / (abs(f[1])+abs(f[2])))
        worst_metric_source = max(worst_metric_source, residual)
        assert residual < D("1e-72")
    return {
        "status": "PASS", "curvature_arithmetic": "symbolic exact Q[t,t0] polynomial identities, all t>0,t0>=0",
        "G00": "4/(3*t*(t+t0))", "Gii_over_ai_squared": "0 for all three i",
        "R": "-4/(3*t*(t+t0))", "Weyl_0i0i": "(4,-2,-2)*t0/(9*t^2*(t+t0))",
        "volume_times_dust_density_derivative": "exactly zero",
        "sample_x": str(xx), "sample_y": str(y), "sample_product_Ai": str(product_a),
        "worst_full_inverse_metric_source_diagnostic": str(worst_metric_source),
        "source_arithmetic": "90-digit Decimal at one nonzero trace branch point and four finite caps",
        "scope": "explicit fixed-measure continuum action and constant internal parameters; not a native finite-lattice implementation proof",
    }


def main():
    result = {
        "date": "2026-10-21", "status": "PASS",
        "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "parent_checker_sha256": hashlib.sha256(PARENT_CHECKER.read_bytes()).hexdigest(),
        "GR_closed": False,
        "exact_detector_and_uniform_constants": exact_detector_and_uniform_constants(),
        "explicit_branch": decimal_branch_and_auxiliary_checks(),
        "null_metric": exact_null_metric_check(),
        "nonnull_Bianchi_continuum": exact_bianchi_identities(),
        "rotating_curved_propagation": rotating_curved_wave_checks(),
        "not_claimed": ["fresh repository owner/complete-price audit", "finite-grid proof of uniform theorems", "native finite-lattice full nonnull solution", "full coupled perturbation solution", "physical clock or compulsory action selection"],
    }
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "CHECK_RESULTS.json"
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n")
    print(json.dumps({"status": result["status"], "receipt": str(target), "sections": [key for key, value in result.items() if isinstance(value, dict)]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
