#!/usr/bin/env python3
"""Exact controls for affine and homogeneous native contrast obstructions.

The arbitrary-dimension and refining-sequence proof is in
A4D_NATIVE_AFFINE_PROBE_NOGO.md. Finite fixtures are not its proof.
Default replay checks an immutable ledger; --output is an explicit write.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import sympy as sp

INPUTS = [
    "03_FORMALIZATION/D0/Geometry/ArchiveSeamCurvature.lean",
    "03_FORMALIZATION/D0/Geometry/ArchiveVariation.lean",
    "03_FORMALIZATION/D0/Geometry/ArchiveLocalLaplacianVariation.lean",
    "03_FORMALIZATION/D0/Geometry/ArchiveFieldEquation.lean",
    "03_FORMALIZATION/D0/Matter/ArchiveStressCoupling.lean",
    "03_FORMALIZATION/D0/Geometry/FinitePrimalDualHodgeParent.lean",
    "03_FORMALIZATION/D0/Geometry/ArchiveCanonicalLaplacian.lean",
    "03_FORMALIZATION/D0/Geometry/ArchiveLaplacianRG.lean",
    "03_FORMALIZATION/D0/Geometry/ArchiveWeightedGraph.lean",
    "03_FORMALIZATION/D0/Geometry/ArchivePhaseDistance.lean",
]

# Reviewed inputs remain tied to their published research snapshot. Replay of
# this self-contained new certificate does not require merging their parent.
PUBLISHED_INPUTS = {
    "02_REGISTRY/research/certificates/a4d_finite_probe_palatini_check.py": {
        "source_head": "af221e2fed92821c52afc88a5500774de8cd9a93",
        "sha256": "7f2d1c58fa4d4a8c52b2b3c76b9ca1369297f3c169d4216cbc5b7434ac787d6d"
    },
    "02_REGISTRY/research/certificates/a4d_finite_probe_palatini_results.json": {
        "source_head": "af221e2fed92821c52afc88a5500774de8cd9a93",
        "sha256": "e749641cef57f7dfa75c648dec773fdd88e2b682d339867f1f5760bb0669f98e"
    },
    "02_REGISTRY/research/certificates/a4d_native_seam_action_gate_check.py": {
        "source_head": "af221e2fed92821c52afc88a5500774de8cd9a93",
        "sha256": "215b85bd0f3bd508d2c8c792d0a57c987447392eee491d7b6cbe87a3c93fea7c"
    }
}


def cycle(m):
    assert m >= 3
    result = sp.zeros(m)
    for i in range(m):
        result[i, i] = 2
        result[i, (i-1) % m] = result[i, (i+1) % m] = -1
    return result


def lift(m):
    return sp.Matrix(m+1, m, lambda i, j: int(j == i % m))


def edge(m, i):
    vector = sp.zeros(m, 1)
    vector[i], vector[(i+1) % m] = 1, -1
    return vector*vector.T


def inner(a, b):
    return sum(x * y for x, y in zip(a, b))


def encode(matrix):
    return [[str(x) for x in row] for row in matrix.tolist()]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[3])
    parser.add_argument("--output", type=Path)
    parser.add_argument("--expect", type=Path)
    args = parser.parse_args()
    repo = args.repo.resolve()
    checks = []

    def check(name, condition):
        assert condition, name
        checks.append(name)
        print("PASS_" + name, flush=True)

    # The component identity proves convexity for every fixed positive weight.
    d, v, t, w = sp.symbols("d v t w", real=True)
    check("GENERIC_AFFINE_SECOND_REMAINDER",
          sp.expand((d+t*v)**2 - d*d - 2*t*d*v - t*t*v*v) == 0)
    a, b, theta = sp.symbols("a b theta", real=True)
    check("GENERIC_WEIGHTED_JENSEN_IDENTITY",
          sp.expand(w*(theta*a+(1-theta)*b)**2
                    - w*(theta*a*a+(1-theta)*b*b)
                    + theta*(1-theta)*w*(a-b)**2) == 0)

    # Actual cyclic J, with simultaneous fine/coarse affine directions.
    # No inference for all sizes is made from these fixtures.
    seam_rows = []
    for m in (3, 4, 7, 10):
        J, Lf, Lc = lift(m), cycle(m+1), cycle(m)
        D = Lf*J-J*Lc
        target = sp.zeros(m+1, m)
        target[0, 0], target[0, m-1] = -1, 1
        target[m, 0], target[m, 1] = -1, 1
        check(f"CANONICAL_TWO_ROW_SEAM_{m}", D == target)
        coarse_edge = edge(m, 0)
        check(f"CANONICAL_LOCAL_DERIVATIVE_SIX_{m}", -2*inner(D, J*coarse_edge) == 6)
        gradient = -2*J.T*D
        check(f"CANONICAL_FULL_SOURCE_GRADIENT_IS_NOT_SYMMETRIC_{m}",
              gradient[0, 1] == -2 and gradient[1, 0] == 0
              and gradient*sp.ones(m, 1) == sp.zeros(m, 1))
        fine_edge = edge(m+1, 1)
        delta = fine_edge*J-J*coarse_edge
        remainder = sp.expand(inner(D+t*delta, D+t*delta)
                              - inner(D, D)-2*t*inner(D, delta))
        check(f"JOINT_FINE_COARSE_EXACT_REMAINDER_{m}",
              remainder == t*t*inner(delta, delta) and inner(delta, delta) >= 0)
        seam_rows.append({"coarse_size": m, "seam_action": str(inner(D, D)),
                          "edge_derivative": 6, "gradient_01": "-2", "gradient_10": "0",
                          "joint_remainder_coefficient": str(inner(delta, delta))})

    # A rank-deficient auxiliary space: every stationary point gives the
    # same profile, while a genuine auxiliary kernel is retained.
    W = sp.diag(2, 3, 5, 7)
    K = sp.Matrix([[1, 0, 1], [0, 1, 0], [1, 0, 1], [0, 1, 0]])
    K0 = K[:, :2]
    P = K0*(K0.T*W*K0).inv()*K0.T*W
    check("WEIGHTED_PROJECTION_WITH_AUXILIARY_KERNEL",
          P*P == P and P.T*W == W*P and K*sp.Matrix([1, 0, -1]) == sp.zeros(4, 1))
    g0, g1, kernel = sp.symbols("g0 g1 kernel", real=True)
    B = sp.Matrix([[1, 2], [-1, 1], [2, 0], [0, 3]])
    r = sp.Matrix([1, -2, 3, 4])+B*sp.Matrix([g0, g1])
    y0 = -(K0.T*W*K0).inv()*K0.T*W*r
    ystar = sp.Matrix([y0[0]+kernel, y0[1], -kernel])
    residual = (sp.eye(4)-P)*r
    check("FULL_AUXILIARY_GATE_AND_KERNEL_INDEPENDENT_PROFILE",
          sp.simplify(r+K*ystar-residual) == sp.zeros(4, 1)
          and sp.simplify(K.T*W*residual) == sp.zeros(3, 1))
    y = sp.Matrix(sp.symbols("y0:3", real=True))
    value = ((r+K*y).T*W*(r+K*y))[0]
    profile = sp.expand((residual.T*W*residual)[0])
    gap = ((K*(y-ystar)).T*W*K*(y-ystar))[0]
    check("ALL_STATIONARY_POINTS_ARE_GLOBAL_MINIMA",
          sp.simplify(value-profile-gap) == 0)
    profile_hessian = sp.hessian(profile, (g0, g1))
    projected_B = (sp.eye(4)-P)*B
    check("PROFILE_HESSIAN_EXACT_GRAM",
          profile_hessian == 2*projected_B.T*W*projected_B
          and profile_hessian[0, 0] > 0 and profile_hessian.det() > 0)
    s, eps = sp.symbols("s eps", real=True)
    ell0, ell1 = sp.symbols("ell0 ell1", real=True)
    pencil = sp.expand(profile.subs({g0: 1+2*s, g1: -1+3*s}) + ell0 + ell1*s)
    secant = sp.expand((pencil.subs(s, s+eps)-pencil.subs(s, s-eps))/(2*eps))
    check("CENTERED_PROFILE_SECANT_IS_DERIVATIVE", sp.simplify(secant-sp.diff(pencil, s)) == 0)
    slope = sp.diff(secant, s)
    check("FIXED_SOURCE_DOES_NOT_CHANGE_SECANT_SLOPE", slope > 0 and not slope.has(ell0, ell1))

    # Derive the conformal curvature from all Christoffel/Ricci entries,
    # using the standard curvature sign. The literal owner is minus this.
    sig = [1, -1, -1, -1]
    eta = sp.diag(*sig)
    q = sp.symbols("q", positive=True)
    p, r2 = sp.symbols("p r2", real=True)
    conformal = []
    for k in range(4):
        metric, inverse = q*eta, eta/q

        def derivative(expr, direction):
            return sp.diff(expr, q)*p+sp.diff(expr, p)*r2 if direction == k else sp.S.Zero

        gamma = [[[sp.simplify(sum(inverse[c, d]*(derivative(metric[d, b], aa)
                      + derivative(metric[d, aa], b)-derivative(metric[aa, b], d))/2
                      for d in range(4))) for b in range(4)] for aa in range(4)] for c in range(4)]
        ricci = sp.Matrix(4, 4, lambda aa, b: sp.simplify(sum(
            derivative(gamma[c][aa][b], c)-derivative(gamma[c][aa][c], b)
            + sum(gamma[c][c][d]*gamma[d][aa][b]-gamma[c][b][d]*gamma[d][aa][c]
                  for d in range(4)) for c in range(4))))
        scalar = sp.simplify(sp.trace(inverse*ricci))
        expected_scalar = sig[k]*(-3*r2/q**2+sp.Rational(3, 2)*p*p/q**3)
        check(f"ALL_COMPONENT_CONFORMAL_RICCI_SIGN_{k}", sp.simplify(scalar-expected_scalar) == 0)
        owner_density = sp.simplify(-q*q*scalar/2)
        check(f"CONFORMAL_EH_DENSITY_MOD_PERIODIC_DIVERGENCE_{k}",
              sp.simplify(owner_density-sp.Rational(3, 2)*sig[k]*r2
                          + sp.Rational(3, 4)*sig[k]*p*p/q) == 0)
        conformal.append({"coordinate": k, "R_standard": str(scalar),
                          "literal_owner_density": str(owner_density)})

    # Independent ten-slot linearized Gram covector for each coordinate.
    # This includes off-diagonal packing; conformal directions are not gauge.
    pairs = [(aa, b) for aa in range(4) for b in range(aa, 4)]
    metric_rows = []
    for k in range(4):
        def response(Q):
            trace = sum(sig[c]*Q[c, c] for c in range(4))
            ricci = sp.Matrix(4, 4, lambda aa, b: (sig[k]*((aa == k)*Q[k, b]
                + (b == k)*Q[aa, k]-Q[aa, b])-(aa == k)*(b == k)*trace)/2)
            scalar = sum(sig[c]*ricci[c, c] for c in range(4))
            G = ricci-eta*scalar/2
            return sp.Matrix([sp.Rational(1, 2)*(1 if aa == b else 2)*sig[aa]*sig[b]*G[aa, b]
                              for aa, b in pairs])
        columns = []
        for aa, b in pairs:
            Q = sp.zeros(4)
            Q[aa, b] = Q[b, aa] = 1
            columns.append(response(Q))
        M = sp.Matrix.hstack(*columns)
        check(f"PACKED_ALL_TEN_COMPONENT_HESSIAN_SYMMETRY_{k}", M == M.T)
        for c in range(4):
            covector = sp.eye(4)[:, c]
            e = sp.eye(4)[:, k]
            Qgauge = e*covector.T+covector*e.T
            check(f"GENUINE_METRIC_GAUGE_NULL_{k}_{c}", response(Qgauge) == sp.zeros(10, 1))
        V = sp.Matrix([2*sig[aa] if aa == b else 0 for aa, b in pairs])
        check(f"CONFORMAL_SECOND_VARIATION_NORMALIZATION_{k}",
              (V.T*M*V)[0] == 6*sig[k] and M*V != sp.zeros(10, 1))
        metric_rows.append({"coordinate": k, "packed_response_matrix": encode(M),
                            "conformal_u_u_second_derivative_coefficient": 6*sig[k]})

    # Full nonlinear second variation of the reduced conformal density.
    ps = sp.Matrix(sp.symbols("p0:4", real=True))
    vs = sp.Matrix(sp.symbols("v0:4", real=True))
    vv = sp.symbols("v", real=True)
    density = -sp.Rational(3, 4)*(ps.T*eta*ps)[0]/q
    varied = density.subs({q: q+s*vv, **{ps[i]: ps[i]+s*vs[i] for i in range(4)}}, simultaneous=True)
    second = sp.diff(varied, s, 2).subs(s, 0)
    expected = -sp.Rational(3, 2)*((vs-vv*ps/q).T*eta*(vs-vv*ps/q))[0]/q
    check("NONLINEAR_AFFINE_CONFORMAL_SECOND_VARIATION", sp.simplify(second-expected) == 0)
    u = sp.symbols("u", real=True)
    us = sp.Matrix(sp.symbols("u0:4", real=True))
    factor = 1+2*s*u
    affine_pencil = expected.subs({q: q*factor, vv: 2*q*u,
        **{ps[i]: factor*ps[i]+2*s*q*us[i] for i in range(4)},
        **{vs[i]: 2*u*ps[i]+2*q*us[i] for i in range(4)}}, simultaneous=True)
    target_second = -6*q*(us.T*eta*us)[0]/factor**3
    check("CURVED_BASE_TWO_SIGN_AFFINE_PENCILS", sp.simplify(affine_pencil-target_second) == 0)
    x = sp.symbols("x", real=True)
    qbase = 1+sp.cos(2*sp.pi*x)/10
    uprime = sp.diff(sp.cos(2*sp.pi*x), x)
    norm_space = sp.integrate(qbase*uprime**2, (x, 0, 1))
    norm_time = sp.integrate(qbase, (x, 0, 1))*sp.integrate(uprime**2, (x, 0, 1))
    check("EXACT_PERIODIC_HESSIANS_OPPOSITE_SIGNS",
          -6*norm_time == -12*sp.pi**2 and 6*norm_space == 12*sp.pi**2)
    R_owner_at_zero = (-conformal_scalar_at(eta, 1, q, p, r2)).subs(
        {q: sp.Rational(11, 10), p: 0, r2: -2*sp.pi**2/5})
    check("BASE_IS_GENUINELY_CURVED", R_owner_at_zero == 120*sp.pi**2/121)

    # Controls rejecting extension to non-affine maps and mere residuals.
    z = sp.symbols("z", real=True)
    nonlinear = (1-z*z)**2
    check("NONLINEAR_READOUT_OR_CONSTRAINT_ESCAPES_CONVEXITY",
          sp.diff(nonlinear, z).subs(z, 0) == 0 and sp.diff(nonlinear, z, 2).subs(z, 0) == -4)
    yy = sp.symbols("y", real=True)
    off_shell = (1-yy)**2
    check("OFF_SHELL_PREPARATION_CANNOT_REPLACE_NATIVE_GATE",
          sp.diff(off_shell, yy).subs(yy, z*z) != 0)
    h = sp.symbols("h", positive=True)
    approximate = (h*h*yy-1)**2
    check("SMALL_RESIDUAL_WITHOUT_UNIFORM_RANGE_ESTIMATE_IS_INSUFFICIENT",
          sp.diff(approximate, yy).subs(yy, 0) == -2*h*h
          and approximate.subs(yy, 0)-approximate.subs(yy, 1/(h*h)) == 1)
    check("BOTH_FIXED_CALIBRATION_SIGNS_FAIL",
          -6*norm_time < 0 and 6*norm_space > 0)
    check("ERROR_COMPOSITION_H_OVER_EPS_PLUS_EPS_SQUARED",
          sp.simplify(h/(h**sp.Rational(1, 3))+(h**sp.Rational(1, 3))**2
                      - 2*h**sp.Rational(2, 3)) == 0)

    # The actual mixed-parent formula is homogeneous in all three fields
    # for a bilinear pairing. Operators may depend nonlinearly on the metric.
    # A full unconstrained field Euler gate then gives action value zero.
    psi = sp.Matrix(sp.symbols("psi0:2", real=True))
    chi = sp.Matrix(sp.symbols("chi0:2", real=True))
    lam = sp.Matrix(sp.symbols("lam0:2", real=True))
    star = sp.Matrix(2, 2, sp.symbols("s0:4", real=True))
    kinetic = sp.Matrix(2, 2, sp.symbols("k0:4", real=True))
    fields = list(psi)+list(chi)+list(lam)
    parent = sp.expand((chi.T*star*chi)[0]/2+(lam.T*(star*chi-kinetic*psi))[0])
    full_euler = sp.Matrix([sp.diff(parent, field) for field in fields])
    check("LITERAL_MIXED_PARENT_GENERIC_EULER_IDENTITY",
          sp.expand(sum(field*row for field, row in zip(fields, full_euler))-2*parent) == 0)
    scaled = parent.subs({field: t*field for field in fields}, simultaneous=True)
    check("MIXED_PARENT_FULL_FIELD_HOMOGENEITY", sp.expand(scaled-t*t*parent) == 0)
    root_zero = {field: 0 for field in fields}
    check("MIXED_PARENT_PREPARATION_FIBERS_ARE_NONEMPTY",
          full_euler.subs(root_zero) == sp.zeros(6, 1) and parent.subs(root_zero) == 0)
    # Two smooth, nonzero kernel roots for every metric parameter.
    kernel_parent = parent.subs(dict(zip(list(star)+list(kinetic), list(sp.eye(2))+list(sp.diag(q*q+1, 0)))))
    root_a = dict(zip(fields, [0, 1, 0, 0, 0, 0]))
    root_b = dict(zip(fields, [0, 2, 0, 0, 0, 0]))
    check("MIXED_PARENT_NONZERO_KERNEL_ROOTS_RETAINED",
          all(sp.diff(kernel_parent, field).subs(root_a) == 0 and
              sp.diff(kernel_parent, field).subs(root_b) == 0 for field in fields)
          and kernel_parent.subs(root_a) == kernel_parent.subs(root_b) == 0)
    # Full field stationarity does not imply zero metric Euler response
    # at a singular projection. This uses the same literal parent formula.
    metric_parameter = sp.symbols("metric_parameter", real=True)
    signed_star = sp.Matrix([[0, 1], [1, 0]])
    moving_kinetic = sp.Matrix([[0, metric_parameter], [metric_parameter, 1]])
    singular_parent = parent.subs(dict(zip(list(star)+list(kinetic), list(signed_star)+list(moving_kinetic))))
    singular_root = dict(zip(fields, [0, 1, 1, 0, -1, 0]))
    at_root = {**singular_root, metric_parameter: 0}
    check("MIXED_PARENT_SINGULAR_SOURCE_NOT_RECOVERED_FROM_ZERO_VALUE",
          all(sp.diff(singular_parent, field).subs(at_root) == 0 for field in fields)
          and singular_parent.subs(at_root) == 0
          and sp.diff(singular_parent, metric_parameter).subs(at_root) == 1
          and signed_star.det() == -1)
    # A function merely called pairing is not automatically bilinear.
    nonbilinear = (a*b-1)**2
    check("MIXED_PARENT_BILINEAR_PAIRING_HYPOTHESIS_IS_NECESSARY",
          sp.expand(nonbilinear.subs({a: t*a, b: t*b}, simultaneous=True)-t*t*nonbilinear) != 0)

    payload = {"status": "PASS", "input_head": "af221e2fed92821c52afc88a5500774de8cd9a93",
        "input_sha256": {path: hashlib.sha256((repo/path).read_bytes()).hexdigest() for path in INPUTS},
        "consumed_published_probe_inputs": PUBLISHED_INPUTS,
        "checks": checks, "seam_controls": seam_rows, "profile_fixture": str(profile),
        "profile_fixture_hessian": encode(profile_hessian), "profile_auxiliary_kernel_dimension": 1,
        "conformal_curvature_controls": conformal, "metric_controls": metric_rows,
        "curved_base": {"q": "1+cos(2*pi*y1)/10", "min_q": "9/10",
            "R_owner_y1_zero": str(R_owner_at_zero), "time_Hessian": "-12*pi**2", "space_Hessian": "12*pi**2"},
        "mixed_parent_controls": {"generic_action": str(parent), "full_field_Euler_identity": "sum(z_i*E_i)=2*B",
            "singular_on_shell_metric_response": "1", "full_field_stationary_action": "0",
            "assumptions": "Bilinear pairing; all three fields freely varied; no additional metric-only or inhomogeneous action term."},
        "scope": "Exact finite algebraic controls. General affine-profile and homogeneous-parent contrast obstructions are proved analytically in the memo; no all-native completeness or positive GR assertion."}
    if args.output:
        args.output.write_text(json.dumps(payload, indent=2, sort_keys=True)+"\n")
    expected_path = args.expect or (Path(__file__).with_name("a4d_native_affine_probe_nogo_results.json") if not args.output else None)
    if expected_path is not None:
        assert json.loads(expected_path.read_text()) == payload, "PINNED_LEDGER_MISMATCH"
        print("PASS_IMMUTABLE_PINNED_LEDGER", flush=True)
    print("PASS_AFFINE_NATIVE_COMPLETED_CONTRAST_CONTROLS", flush=True)


def conformal_scalar_at(eta, k, q, p, r2):
    return eta[k, k]*(-3*r2/q**2+sp.Rational(3, 2)*p*p/q**3)


if __name__ == "__main__":
    main()
