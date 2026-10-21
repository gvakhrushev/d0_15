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

print(json.dumps({
    "checks": checks,
    "count": len(checks),
    "scope": {
        "rest_aligned_timelike_observer_only": True,
        "same_native_endpoint_isometry_can_follow_nonzero_H_step": False,
        "physical_admission": False,
        "primary_null_matter_identified": False,
        "GR_closed": False,
    },
    "status": "PASS",
}, indent=2, sort_keys=True))
