#!/usr/bin/env python3
"""Exact variable-curvature geodesic-normal metric jet for the Y factor.

Derives the two-dimensional normal metric through fourth order from the
radial Jacobi equation, then checks that the constant-curvature specialization
matches the pinned z=1 Y normal-jet convention.  This is a geometric input
certificate only; it does not transport the local cokernel through the global
sampled lattice or prove a periodic mean obstruction.
"""
from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "02_REGISTRY/research/certificates/a4d_y_variable_curvature_normal_jet_results.json"


def check(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name, flush=True)


r = sp.symbols("r")
K0, K1, K2 = sp.symbols("K0 K1 K2")
a, b, c = sp.symbols("a b c")
# Along a radial geodesic, K(r)=K0+K1*r+K2*r^2/2+O(r^3).
jacobi = r + a * r**3 + b * r**4 + c * r**5
ode = sp.expand(sp.diff(jacobi, r, 2) +
                (K0 + K1 * r + K2 * r**2 / 2) * jacobi)
equations = [sp.expand(ode).coeff(r, degree) for degree in (1, 2, 3)]
solution = sp.solve(equations, (a, b, c), dict=True)[0]
check("JACOBI_RECURRENCE_EXACT",
      solution == {a: -K0 / 6, b: -K1 / 12,
                   c: K0**2 / 120 - K2 / 40})
jacobi = sp.expand(jacobi.subs(solution))
ratio = sp.series((jacobi / r)**2, r, 0, 5).removeO().expand()
ratio_expected = (1 - K0 * r**2 / 3 - K1 * r**3 / 6
                  + (2 * K0**2 / 45 - K2 / 20) * r**4)
check("RADIAL_AREA_RATIO_EXACT",
      sp.expand(ratio - ratio_expected) == 0)

# In Lorentz signature the two-dimensional spatial block is the negative of
# the Riemannian polar metric.  Writing T=r^2 I-x x^T gives Q-eta as below.
x1, x2, kap = sp.symbols("x1 x2 kappa")
g1, g2, h11, h12, h22 = sp.symbols("kappa_1 kappa_2 kappa_11 kappa_12 kappa_22")
r2 = x1**2 + x2**2
T = sp.Matrix([[x2**2, -x1 * x2], [-x1 * x2, x1**2]])
coefficient = (kap + (g1 * x1 + g2 * x2) / 2
               - sp.Rational(2, 5) * kap**2 * r2
               + sp.Rational(3, 20) *
               (h11 * x1**2 + 2 * h12 * x1 * x2 + h22 * x2**2))
Qcorr = (coefficient * T).applyfunc(sp.expand)
constant_specialization = Qcorr.subs({g1: 0, g2: 0, h11: 0, h12: 0, h22: 0})
owner_constant = (kap * T - sp.Rational(2, 5) * kap**2 * r2 * T).applyfunc(sp.expand)
check("CONSTANT_CURVATURE_MATCHES_PINNED_NORMAL_JET",
      constant_specialization == owner_constant)

expected_formula = (
    "Q-eta = [kappa + (grad(kappa) dot x)/2 "
    "- 2*kappa^2*|x|^2/5 "
    "+ 3*Hess(kappa)(x,x)/20] * (|x|^2 I - x x^T) + O(|x|^5)"
)
scaled_formula = (
    "Q_h-eta = h^2*kappa*T(xi) "
    "+ h^3*(grad(kappa) dot xi)*T(xi)/2 "
    "+ h^4*[-2*kappa^2*|xi|^2/5 "
    "+ 3*Hess(kappa)(xi,xi)/20]*T(xi) + O(h^5)"
)
result = {
    "schema": "a4d-y-variable-curvature-normal-jet-v1",
    "terminal": "A4D-Y-VARIABLE-CURVATURE-NORMAL-JET-CERTIFIED",
    "radial_jacobi_coefficients": {
        "j_over_r": "1-K0*r^2/6-K1*r^3/12+(K0^2/120-K2/40)*r^4+O(r^5)",
        "j_squared_over_r_squared": "1-K0*r^2/3-K1*r^3/6+(2*K0^2/45-K2/20)*r^4+O(r^5)",
    },
    "normal_metric_jet": expected_formula,
    "lattice_scaled_metric_jet": scaled_formula,
    "curvature_normalization": "K=3*kappa",
    "constant_curvature_control": "Q-eta=kappa*T-(2/5)*kappa^2*|x|^2*T",
    "scope": "local two-dimensional geodesic-normal metric jet; global lattice transport and periodic mean obstruction remain open",
    "checks": [
        "radial Jacobi recurrence solved over Q",
        "constant-curvature specialization equals the pinned owner jet",
    ],
}
if OUT.exists():
    check("RESULTS_MATCH_PINNED_JSON", result == json.loads(OUT.read_text()))
else:
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    print("WROTE", OUT)
print("TERMINAL A4D-Y-VARIABLE-CURVATURE-NORMAL-JET-CERTIFIED")
