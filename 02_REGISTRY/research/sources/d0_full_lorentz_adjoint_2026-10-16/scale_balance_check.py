#!/usr/bin/env python3
"""Narrow exact controls for owner Section7; no root/spectrum replay.

The minmax theorem is the analytic argument in the owner, not a finite test.
No assertions are used: rejection is unchanged by Python's optimized mode.
"""
import hashlib
import importlib.util
import json
from pathlib import Path

import sympy as s

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent


def run():
    checks = []

    def require(condition, label):
        if not bool(condition):
            raise ArithmeticError("scale_balance:" + label)
        checks.append(label)

    def equal(actual, expected, label):
        require(s.simplify(actual - expected) == 0, label)

    # A complete scalar-block spectrum, with ALL16 retained in each block.
    # The preparation is normalized separately from the thermal trace.
    t = s.symbols("t", real=True)
    alpha, m, beta = s.Rational(1, 4), 3, s.Rational(3, 4)
    z, M, workspace = s.Rational(1, 5), 128, 128 ** 3
    spectrum = [s.Rational(0), s.Rational(1, 3), s.Rational(2, 3)]
    probabilities = [s.Rational(1, 2), s.Rational(1, 3), s.Rational(1, 6)]
    mult = 16
    B = [1 - alpha * lam for lam in spectrum]
    Z = mult * sum(b ** m for b in B)
    feedback = [1 - z + z * b ** m for b in B]
    T1 = mult * sum(lam * b ** (m - 1) for lam, b in zip(spectrum, B))
    T2 = mult * sum(lam * b ** (m - 1) / f
                    for lam, b, f in zip(spectrum, B, feedback))
    R = sum(lam * p for lam, p in zip(spectrum, probabilities))
    Bt = [1 - alpha * s.exp(2 * t) * lam for lam in spectrum]
    Zt = mult * sum(b ** m for b in Bt)
    Ft = [1 - z + z * b ** m for b in Bt]
    heat = s.log(workspace * Zt) / beta
    record = -M * mult * sum(s.log(f) for f in Ft)
    matter = s.exp(2 * t) * R
    derivative = lambda expression: s.diff(expression, t).subs(t, 0)
    equal(beta, m * alpha, "actual_beta_m_alpha")
    require(all(0 < b <= 1 for b in B) and 0 < z < 1,
            "positive_full_survival_feedback_domain")
    equal(derivative(heat), -2 * T1 / Z, "full_trace_heat_derivative")
    equal(derivative(record), 2 * M * z * beta * T2,
          "feedback_derivative_retains_reference_multiplicity")
    equal(derivative(matter), 2 * R, "normalized_fixed_preparation_derivative")
    equal(derivative(heat + record + matter) / 2,
          -T1 / Z + M * z * beta * T2 + R, "full_price_scale_identity")
    equal(derivative(s.log(Zt) / beta), derivative(heat),
          "retained_workspace_constant_cancels_only_from_heat_source")
    require(T2 > T1 > 0, "strict_feedback_weight_on_positive_modes")

    # Exact threshold witness using the actual integer M=128 and R=0.
    # Dropping J, the full16 factor, or the reference gives the wrong verdict.
    zcrit = 1 / (M * beta * Z)
    Fc = [1 - zcrit + zcrit * b ** m for b in B]
    T2c = mult * sum(lam * b ** (m - 1) / f
                    for lam, b, f in zip(spectrum, B, Fc))
    equal(M * zcrit * beta * Z, 1, "exact_mu_one_threshold")
    require(0 < zcrit < 1, "threshold_fugacity_in_domain")
    full_threshold_source = -T1 / Z + M * zcrit * beta * T2c
    require(full_threshold_source > 0, "strict_positive_source_even_mu_one_R_zero")
    require(-T1 / Z < 0, "hostile_omitting_feedback_reverses_verdict")
    equal(M * zcrit * beta * (Z / 16), s.Rational(1, 16),
          "hostile_dropping_full16_misses_threshold")
    equal(zcrit * beta * Z, s.Rational(1, 128),
          "hostile_dropping_reference_misses_threshold")

    # beta=m alpha is a premise. This exact counterexample rejects silently
    # using the fixed-beta source formula with unrelated beta.
    wrong_beta = 2 * beta
    actual_wrong_heat = derivative(s.log(workspace * Zt) / wrong_beta)
    equal(actual_wrong_heat, -T1 / Z,
          "independent_beta_retains_m_alpha_over_beta_factor")
    require(actual_wrong_heat != -2 * T1 / Z,
            "hostile_unrelated_beta_rejects_short_formula")

    # An off-shell normalized preparation can move under a different lift.
    w = s.Matrix([1 + t, 1 - t])
    rho = w * w.T / (w.T * w)[0]
    delta = s.diag(0, 1)
    rho_dot = rho.diff(t).subs(t, 0)
    equal(s.trace(rho_dot), 0, "moving_preparation_normalizer_retained")
    equal(s.trace(delta * rho_dot), -1,
          "hostile_offshell_moving_preparation_source_nonzero")
    equal(derivative(s.trace(s.exp(2 * t) * delta * rho)), 0,
          "full_moving_matter_derivative_includes_extra_term")
    w_shell = s.Matrix([1, t, 0])
    rho_shell = w_shell * w_shell.T / (w_shell.T * w_shell)[0]
    equal(s.trace(s.diag(2, 2, 5) * rho_shell.diff(t).subs(t, 0)), 0,
          "stationary_eigenshell_kills_normalized_preparation_extra_term")

    # Reuse the literal CAR definitions without running the older89 checks.
    spec = importlib.util.spec_from_file_location(
        "existing_full_lorentz_source", HERE / "full_lorentz_boost_source_check.py")
    existing = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(existing)
    creators, _ = existing._creators(ROOT)
    L = 4
    shift = s.zeros(L)
    for x in range(L):
        shift[x, (x + 1) % L] = 1
    S = s.kronecker_product(shift, s.eye(16))
    coeff = s.kronecker_product(s.diag(*[s.Rational(1, 8 - x)
                                       for x in range(L)]), creators[0])
    identity = s.eye(16 * L)
    T = L * coeff * (S - identity)
    frozen = L * coeff.H * (S.H - identity)
    correction = L * (S.H * coeff.H - coeff.H * S.H)
    require(T.H == frozen + correction,
            "full16_variable_coefficient_true_adjoint_identity")
    require(correction != s.zeros(16 * L) and T.H != frozen,
            "hostile_missing_adjoint_coefficient_difference_rejected")

    # An exact positive-remainder identity proves Bernoulli on [0,1].
    x = s.symbols("x", real=True)
    for power in (1, 2, 3, 8, 32):
        positive = x ** 2 * sum((power - 1 - j) * (1 - x) ** j
                               for j in range(power - 1))
        equal(s.expand((1 - x) ** power - 1 + power * x), positive,
              "Bernoulli_positive_remainder_m" + str(power))
    # These finite edge cases guard floors and saturation; the all-L proof
    # is the inequalities in the owner, not an extrapolation of this loop.
    edge_cases = 0
    for mesh in range(4, 65):
        for depth in (1, 2, 3, 8, 32, 128):
            c0, a = s.Rational(1, 16), s.Rational(1, 8)
            heat_time = depth * c0 / mesh ** 2
            if heat_time > a ** 2:
                continue
            q = min(mesh // 4, int(s.floor(a / s.sqrt(heat_time))))
            c = min(c0 ** 2 / 32, 8 * a ** 4)
            if not (q >= 1 and 8 * (2 * q + 1) ** 4 >= c / heat_time ** 2):
                raise ArithmeticError("scale_balance:floor_saturation_edge")
            edge_cases += 1
    require(edge_cases > 200, "floor_saturation_and_all_depth_edge_cases")
    return {
        "schema": "d0-full-price-scale-controls/1",
        "checks": len(checks), "passed": checks,
        "floor_edge_cases": edge_cases,
        "mu_one_source_half_exact": str(full_threshold_source),
        "threshold_z_exact": str(zcrit),
        "theorem": "conditional_full_joint_stationarity_requires_M_z_beta_Z_lt_1",
        "analytic_consumer": "owner Section7 finite minmax, no Weyl assumption",
        "old_root_spectrum_or_CAR_replay": False,
        "physical_admission_or_original_terminal_closed": False,
        "definition_sha256": {
            str((HERE / "full_lorentz_boost_source_check.py").relative_to(ROOT)):
                hashlib.sha256((HERE / "full_lorentz_boost_source_check.py").read_bytes()).hexdigest(),
            "02_REGISTRY/research/certificates/a4d_native_curved_soldered_heat.py":
                hashlib.sha256((ROOT / "02_REGISTRY/research/certificates/a4d_native_curved_soldered_heat.py").read_bytes()).hexdigest()
        }
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
