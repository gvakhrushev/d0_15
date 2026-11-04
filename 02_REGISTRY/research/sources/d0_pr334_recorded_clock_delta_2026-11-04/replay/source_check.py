#!/usr/bin/env python3
"""Exact local off-shell source witness; no native root or compilation search."""
import hashlib
import json
from pathlib import Path

import sympy as s

checks = {}


def need(value, label):
    if value is not True:
        raise RuntimeError(label)
    checks[label] = True


def zero(value):
    if isinstance(value, s.MatrixBase):
        return all(s.simplify(x) == 0 for x in value)
    return s.simplify(value) == 0


u, v, x, y = s.symbols("u v x y", real=True)
coords = (u, v, x, y)
k, a, eps, chi, radius, nrm = s.symbols(
    "k a eps chi radius nrm", positive=True
)
H = k * a**2 * (x**2 + y**2)
g = s.Matrix([[H, 1, 0, 0], [1, 0, 0, 0],
              [0, 0, -1, 0], [0, 0, 0, -1]])
gi = g.inv()
need(g.det() == -1, "physical determinant minus one")
need(gi[0, 0] == 0, "du remains null")

christoffel = {}
for r in range(4):
    for m in range(4):
        for n in range(4):
            entry = s.simplify(sum(
                gi[r, t] * (s.diff(g[t, n], coords[m])
                            + s.diff(g[t, m], coords[n])
                            - s.diff(g[m, n], coords[t])) / 2
                for t in range(4)
            ))
            if entry != 0:
                christoffel[r, m, n] = entry


def gam(r, m, n):
    return christoffel.get((r, m, n), s.S.Zero)


ric = s.zeros(4)
for m in range(4):
    for n in range(4):
        ric[m, n] = s.simplify(sum(
            s.diff(gam(r, m, n), coords[r])
            - s.diff(gam(r, m, r), coords[n])
            + sum(gam(r, r, t) * gam(t, m, n)
                  - gam(r, n, t) * gam(t, m, r)
                  for t in range(4))
            for r in range(4)
        ))
expected_ric = s.zeros(4)
expected_ric[0, 0] = 2 * k * a**2
need(zero(ric - expected_ric), "full Ricci tensor has original positive uu sign")
scalar_r = s.simplify(s.trace(gi * ric))
need(scalar_r == 0, "scalar curvature zero")

psi = (a + eps) * u  # The cutoff is identically one on the test support.
gradient = s.Matrix([s.diff(psi, z) for z in coords])
q = s.simplify((gradient.T * gi * gradient)[0])
stress = 2 * gradient * gradient.T - g * q
need(q == 0, "local perturbed scalar gradient null")
need(zero(stress[0, 0] - 2 * (a + eps)**2), "original two-scalar stress factor two")
wave = s.simplify(sum(
    gi[m, n] * (s.diff(psi, coords[m], coords[n])
                - sum(gam(r, m, n) * s.diff(psi, coords[r])
                      for r in range(4)))
    for m in range(4) for n in range(4)
))
need(wave == 0, "scalar wave equation on cutoff plateau only")
einstein = ric - g * scalar_r / 2
residual = s.simplify(einstein - k * stress)  # lambda=-k.
expected_residual = s.zeros(4)
expected_residual[0, 0] = -2 * k * (2 * a * eps + eps**2)
need(zero(residual - expected_residual), "Einstein plus lambda T residual exact")

eta_n = s.Matrix([[0, 1, 0, 0], [1, 0, 0, 0],
                  [0, 0, -1, 0], [0, 0, 0, -1]])
coframe = s.eye(4)
coframe[1, 0] = H / 2
coframe_inv = coframe.inv()
need(coframe.det() == 1, "material coframe determinant one")
need(zero(coframe.T * eta_n * coframe - g), "original null coframe reproduces metric")

# The independent compatible Lorentz connection remains unchanged.
omega = []
for m in range(4):
    gamma_m = s.Matrix(4, 4, lambda r, t: gam(r, m, t))
    omega_m = s.simplify(
        coframe * gamma_m * coframe_inv
        - coframe.diff(coords[m]) * coframe_inv
    )
    omega.append(omega_m)
    need(zero(omega_m.T * eta_n + eta_n * omega_m),
         f"compatible connection Lorentz row {m}")
for m in range(4):
    for n in range(m + 1, 4):
        torsion = (coframe[:, n].diff(coords[m])
                   - coframe[:, m].diff(coords[n])
                   + omega[m] * coframe[:, n]
                   - omega[n] * coframe[:, m])
        need(zero(torsion), f"torsion pair {m},{n} exactly zero")

# Full inverse-metric variation, not merely a change in the vv component.
kvec = s.Matrix([1, 0, 0, 0])
dg_inv = chi * kvec * kvec.T
dg_cov = -g * dg_inv * g
v_hat = -chi * (coframe * kvec) * (g * kvec).T / 2
need(zero(v_hat.T * eta_n * coframe + coframe.T * eta_n * v_hat
          - dg_cov), "physical coframe lift gives full covariant metric variation")
need(zero(-gi * dg_cov * gi - dg_inv), "inverse metric test has only uu component")

# GENERAL(2), at m=det(e)=1: retain its complete 16-dimensional Jacobian.
def material_jacobian(tangent):
    return s.simplify(tangent - coframe * s.trace(coframe_inv * tangent) / 2)


raw_lift = material_jacobian(v_hat)
need(zero(material_jacobian(raw_lift) - v_hat),
     "full material inverse lifts the physical witness")
for j in range(16):
    basis = s.zeros(4)
    basis[j // 4, j % 4] = 1
    need(zero(material_jacobian(material_jacobian(basis)) - basis),
         f"material inverse on independent coframe axis {j}")
need(not zero(raw_lift - v_hat),
     "raw and physical tangent are not identified at det one")

pairing_density = s.simplify(sum(
    residual[m, n] * dg_inv[m, n] / 2
    for m in range(4) for n in range(4)
))
need(zero(pairing_density + k * (2 * a * eps + eps**2) * chi),
     "GENERAL half-R action pairing has correct factor and sign")

t = s.symbols("t", real=True)
bump = (1 - t**2)**4
for order in range(4):
    for endpoint in (-1, 1):
        need(s.diff(bump, t, order).subs(t, endpoint) == 0,
             f"compact polynomial test C3 endpoint {endpoint} order {order}")
integral_1d = s.integrate(bump, (t, -1, 1))
need(integral_1d == s.Rational(256, 315), "exact compact test integral")
margin = k * (2 * a * eps + eps**2) * (radius * integral_1d)**4 / nrm
need(margin.is_positive is True, "normalized physical source margin strictly positive")
need(s.simplify(margin - margin / 4 - margin / 4 - margin / 2) == 0,
     "two quarter budgets leave half the actual source margin")

source_path = Path(__file__)
result = {
    "status": "PASS",
    "checks": checks,
    "number_of_checks": len(checks),
    "convention": "GENERAL(3): half R + lambda q; lambda=-k; metric 2du dv+Hdu2-dx2-dy2",
    "ricci_uu": str(ric[0, 0]),
    "residual_uu": str(residual[0, 0]),
    "pairing_density": str(pairing_density),
    "positive_normalized_margin": str(margin),
    "scope": "local cutoff plateau, exact full material Jacobian and compact test; native decoding uses the owned source estimates",
    "not_claimed": [
        "exact native implementation of the continuum field",
        "emitted compiled native word or numerically evaluated whole heat",
        "global scalar wave equation in the cutoff transition",
        "stationary native root or unrestricted GR closure",
    ],
    "checker_sha256": hashlib.sha256(source_path.read_bytes()).hexdigest(),
}
source_path.with_suffix(".json").write_text(
    json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
    encoding="utf-8",
)
print(json.dumps(result, ensure_ascii=False, sort_keys=True))
