#!/usr/bin/env python3
"""Exact observer-pairing identity and endpoint-isometry compatibility test."""
import json
import sympy as sp


def require(condition, label, checks):
    if not bool(condition):
        raise ArithmeticError(label)
    checks.append(label)


H, kappa, eps, chi, c = sp.symbols(
    "H kappa eps chi c", real=True, nonzero=True
)
e = sp.eye(4)
e[1, 0] = H / 2
T = sp.Matrix([
    [1, sp.Rational(1, 2), 0, 0],
    [1, -sp.Rational(1, 2), 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1],
])
eta_rest = sp.diag(1, -1, -1, -1)
F = sp.sqrt(kappa) * e.inv() * T.inv()
q = sp.simplify(F * eta_rest * F.T)
e0 = sp.Matrix([1, 0, 0, 0])
v = sp.simplify(c * F * e0)
k = sp.simplify((v.T * q.inv() * v)[0])
Q_observer = sp.simplify(-q + 2 * v * v.T / k)
Q_solder = sp.simplify(F * F.T)
Q_H = kappa * sp.Matrix([
    [sp.Rational(1, 2), -H / 4, 0, 0],
    [-H / 4, 2 + H**2 / 8, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1],
])

checks = []
require(sp.simplify(k - c**2) == 0, "timelike normalization k=c^2", checks)
require(Q_observer.equals(Q_solder), "native observer pairing equals F F^T", checks)
require(sp.simplify(Q_solder - Q_H) == sp.zeros(4), "F_H F_H^T equals the moving-solder Q_H", checks)

delta_Q = sp.simplify(Q_H.subs(H, H + eps * chi) - Q_H)
require(sp.simplify(delta_Q[0, 1] + kappa * eps * chi / 4) == 0,
        "moving-pairing off-diagonal increment is -kappa eps chi/4", checks)
require(sp.simplify(sp.diff(Q_H, H)[0, 1] + kappa / 4) == 0,
        "moving-pairing first derivative is nonzero", checks)

# The existing completed four-mask CAR word changes only grades 14 and 15.
# Its first-grade rest component and q=eta_rest are therefore unchanged.
a0, c0, d, b, alpha = sp.symbols("a0 c0 d b alpha", real=True, nonzero=True)
m_before = sp.zeros(16, 1)
m_before[0], m_before[1], m_before[14], m_before[15] = c0, a0, d, b
m_after = m_before.copy()
m_after[14] = d * sp.cos(alpha) - b * sp.sin(alpha)
m_after[15] = d * sp.sin(alpha) + b * sp.cos(alpha)
P1_rest = sp.zeros(4, 16)
P1_rest[0, 1] = 1
v_before = P1_rest * m_before
after_first_grade = P1_rest * m_after
require(sp.simplify(after_first_grade - v_before) == sp.zeros(4, 1),
        "completed profile actuator leaves the first-grade current fixed", checks)
q_rest = eta_rest
k_before = sp.simplify((v_before.T * q_rest.inv() * v_before)[0])
k_after = sp.simplify((after_first_grade.T * q_rest.inv() * after_first_grade)[0])
Q_before = sp.simplify(-q_rest + 2 * v_before * v_before.T / k_before)
Q_after = sp.simplify(-q_rest + 2 * after_first_grade * after_first_grade.T / k_after)
require(sp.simplify(k_before - a0**2) == 0 and sp.simplify(k_after - k_before) == 0
        and sp.simplify(Q_before - sp.eye(4)) == sp.zeros(4)
        and sp.simplify(Q_after - Q_before) == sp.zeros(4),
        "held REST metric and fixed first grade keep the observer pairing at I4", checks)

print(json.dumps({
    "checks": checks,
    "count": len(checks),
    "scope": {
        "rest_aligned_timelike_observer_only": True,
        "same_native_endpoint_isometry_can_follow_nonzero_H_step": False,
        "physical_admission": False,
        "primary_null_matter_identified": False,
        "GR_closed": False,
        "profile_sensitive_CAR_actuator_changes_observer_pairing": False,
    },
    "status": "PASS",
}, indent=2, sort_keys=True))
