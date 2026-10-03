#!/usr/bin/env python3
"""Exact tensor control for spatial-equal metric tangents at the Y vacuum.

This checks a geometric incompatibility with the *linearized* surviving
normal-jet curvature direction.  It does not solve the nonlinear joint Euler
equations on a curved metric.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
OUT = HERE / "a4d_y_spatial_equal_curvature_tangent_results.json"


def check(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name, flush=True)


# In the owner (0,1,2,3) basis, Y=J12-J13+J23 is the bivector of the
# spatial plane perpendicular to (1,1,1).  Spatial-equal Fourier covectors
# have the form (k0,ks,ks,ks), at every nonzero frequency.
beta = sp.zeros(4)
for a, b, value in ((1, 2, 1), (1, 3, -1), (2, 3, 1)):
    beta[a, b], beta[b, a] = value, -value
k0, ks = sp.symbols("k0 ks")
k = sp.Matrix((k0, ks, ks, ks))
check("SPATIAL_EQUAL_WAVE_COVECTOR_ANNIHILATES_Y",
      beta * k == sp.zeros(4, 1))

q = sp.zeros(4)
for a in range(4):
    for b in range(a, 4):
        q[a, b] = q[b, a] = sp.Symbol(f"q{a}{b}")


def linear_riemann(a: int, b: int, c: int, d: int) -> sp.Expr:
    # Overall Fourier sign is immaterial for the zero-contraction identity.
    return (k[b] * k[c] * q[a, d] + k[a] * k[d] * q[b, c]
            - k[a] * k[c] * q[b, d] - k[b] * k[d] * q[a, c]) / 2


pairing = sp.expand(sum(
    beta[a, b] * beta[c, d] * linear_riemann(a, b, c, d)
    for a in range(4) for b in range(4)
    for c in range(4) for d in range(4)
))
beta_norm_sq = sum(beta[a, b] ** 2 for a in range(4) for b in range(4))
check("LINEAR_RIEMANN_Y_Y_CONTRACTION_VANISHES_FOR_ALL_METRIC_TANGENTS",
      pairing == 0 and beta_norm_sq == 6)
check("SURVIVING_Y_TENSOR_Y_DIRECTION_HAS_NONZERO_PAIRING",
      sp.expand(sum(beta[a, b] * beta[c, d] * beta[a, b] * beta[c, d]
                    for a in range(4) for b in range(4)
                    for c in range(4) for d in range(4))) == 36)

# The differential Bianchi identity for R=kappa*beta tensor beta requires
# k wedge beta=0 at each nonzero Fourier mode of kappa.  In this coordinate
# basis, its two independent equations are k0=0 and k1+k2+k3=0.  Thus the
# genuine surviving curvature lives on the transverse-character two-torus.
k1, k2, k3 = sp.symbols("k1 k2 k3")
general_k = sp.Matrix((k0, k1, k2, k3))
wedge = {
    "012": general_k[0] * beta[1, 2]
           + general_k[1] * beta[2, 0]
           + general_k[2] * beta[0, 1],
    "013": general_k[0] * beta[1, 3]
           + general_k[1] * beta[3, 0]
           + general_k[3] * beta[0, 1],
    "023": general_k[0] * beta[2, 3]
           + general_k[2] * beta[3, 0]
           + general_k[3] * beta[0, 2],
    "123": general_k[1] * beta[2, 3]
           + general_k[2] * beta[3, 1]
           + general_k[3] * beta[1, 2],
}
check("BIANCHI_RESTRICTS_CURVATURE_TO_Y_TRANSVERSE_CHARACTER_TORUS",
      wedge == {"012": k0, "013": -k0, "023": k0,
                "123": k1 + k2 + k3})

# Conversely, for any nonzero transverse Fourier covector, a conformal
# tangent on the Y plane realizes that single curvature direction.  This
# proves sufficiency of the Bianchi support condition after solving a
# two-dimensional Poisson equation for any mean-zero smooth kappa.
a, b, phi = sp.symbols("a b phi")
transverse_k = sp.Matrix((0, a, b, -a - b))
normal = sp.Matrix((1, 1, 1))
plane = sp.eye(3) - normal * normal.T / 3
conformal_q = sp.zeros(4)
for i in range(1, 4):
    for j in range(1, 4):
        conformal_q[i, j] = 2 * phi * plane[i - 1, j - 1]


def transverse_riemann(i: int, j: int, m: int, n: int) -> sp.Expr:
    z = transverse_k
    p = conformal_q
    return (z[j] * z[m] * p[i, n] + z[i] * z[n] * p[j, m]
            - z[i] * z[m] * p[j, n] - z[j] * z[n] * p[i, m]) / 2


transverse_length_sq = sum(transverse_k[i] ** 2 for i in range(4))
check("EVERY_NONZERO_TRANSVERSE_MODE_HAS_CONFORMAL_METRIC_REALIZATION",
      all(sp.expand(transverse_riemann(i, j, m, n)
                    + phi * transverse_length_sq * beta[i, j] * beta[m, n] / 3) == 0
          for i in range(4) for j in range(4)
          for m in range(4) for n in range(4)))

# Independent exact geometric control: a periodic scalar warped metric in
# adapted coordinates (t,s,u,v) cannot have curvature solely in the Y=(u,v)
# plane unless its warp is constant.  The owner normal-jet compatibility is
# only known at the flat Y vacuum, so this is not used as a nonlinear Euler
# theorem at finite warp amplitude.
t, s, u, v = sp.symbols("t s u v")
coordinates = (t, s, u, v)
f = sp.Function("f")(t, s)
metric = sp.diag(1, -1, -f**2, -f**2)
inverse = sp.diag(1, -1, -f**-2, -f**-2)


def gamma(a: int, b: int, c: int) -> sp.Expr:
    return sp.factor(sum(inverse[a, e] * (
        sp.diff(metric[e, b], coordinates[c])
        + sp.diff(metric[e, c], coordinates[b])
        - sp.diff(metric[b, c], coordinates[e])) / 2
        for e in range(4)))


def riemann(a: int, b: int, c: int, d: int) -> sp.Expr:
    return sp.factor(sum(metric[a, m] * (
        sp.diff(gamma(m, d, b), coordinates[c])
        - sp.diff(gamma(m, c, b), coordinates[d])
        + sum(gamma(m, c, n) * gamma(n, d, b)
              - gamma(m, d, n) * gamma(n, c, b) for n in range(4)))
        for m in range(4)))


mixed = {
    "R_tutu": riemann(0, 2, 0, 2),
    "R_susu": riemann(1, 2, 1, 2),
    "R_tusu": riemann(0, 2, 1, 2),
}
expected_mixed = {
    "R_tutu": f * sp.diff(f, t, 2),
    "R_susu": f * sp.diff(f, s, 2),
    "R_tusu": f * sp.diff(f, t, s),
}
check("EXACT_WARPED_MIXED_CURVATURE_IS_F_TIMES_BASE_HESSIAN",
      all(sp.simplify(mixed[name] - expected_mixed[name]) == 0
          for name in mixed))
vertical = riemann(2, 3, 2, 3)
check("EXACT_WARPED_VERTICAL_CURVATURE_CONTROL",
      sp.simplify(vertical + f**2 * (sp.diff(f, t)**2
                                    - sp.diff(f, s)**2)) == 0)

result = {
    "schema": "a4d-y-spatial-equal-curvature-tangent-v1",
    "sector": "lambda=(mu,mu*r,mu*r,mu*r); smooth tangents depend on t and s=x1+x2+x3",
    "y_bivector": "dx1^dx2-dx1^dx3+dx2^dx3",
    "wave_covector": "(k0,ks,ks,ks)",
    "wave_covector_y_contraction": "0",
    "linear_riemann_y_y_contraction": str(pairing),
    "y_tensor_y_self_pairing": str(beta_norm_sq**2),
    "bianchi_k_wedge_y_components": {key: str(value) for key, value in wedge.items()},
    "surviving_curvature_character_torus": "lambda0=1,lambda1*lambda2*lambda3=1",
    "conformal_realization_formal_derivative_symbol": (
        "R[2*phi*Pperp]=-(phi*|k|^2/3)*Y tensor Y "
        "for k=(0,a,b,-a-b)"
    ),
    "warped_mixed_curvature": {key: str(value) for key, value in mixed.items()},
    "warped_vertical_curvature": str(vertical),
    "consequence": (
        "The intersection of spatial-equal linearized metric curvatures with "
        "the owned one-dimensional -Y tensor Y normal-jet compatibility "
        "direction is zero.  A smooth periodic compatible linearized "
        "curvature has mean zero and depends only on x2-x1,x3-x1; every "
        "such profile is geometrically realizable by a metric tangent. "
        "Independently, a positive periodic scalar warp whose exact "
        "curvature is purely Y-plane is constant."
    ),
    "scope_fence": [
        "linearized metric curvature at eta for the owner compatibility intersection",
        "the finite-amplitude owner joint Euler equations are not inferred",
        "other Fourier sectors and singular center branches remain open",
        "neither task-level terminal is asserted",
    ],
}
parser = argparse.ArgumentParser()
parser.add_argument("--write", action="store_true")
args = parser.parse_args()
if OUT.exists() and not args.write:
    check("RESULTS_MATCH_PINNED_JSON", result == json.loads(OUT.read_text()))
else:
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    print("WROTE", OUT, flush=True)
print("TERMINAL A4D-Y-SPATIAL-EQUAL-CURVATURE-TANGENT-INCOMPATIBLE", flush=True)
