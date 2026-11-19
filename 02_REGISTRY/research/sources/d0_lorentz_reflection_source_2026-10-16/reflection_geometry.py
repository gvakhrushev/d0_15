"""Exact metric jets for the moving-observer signature reflection.

Conventions: h is a positive COVARIANT metric; g=2*omega*omega.T-h
has signature (+---), omega=h*u, h(u,u)=1.  Ricci is positive on a
round positive sphere.  Omega_ab uses half antisymmetrization, while
Omega_squared sums BOTH index orders.  The generic tensor proof is in
A4D_NATIVE_LORENTZ_REFLECTION_SOURCE.md; finite jet fixtures are controls.
No physical metric binding, observer law, or engine admission is selected.
"""
from __future__ import annotations

from pathlib import Path
from random import Random

import sympy as s


DIM = 4
INDICES = range(DIM)
ETA = s.diag(1, -1, -1, -1)
ROOT = Path(__file__).resolve().parents[4]


def require(condition: object, name: str) -> None:
    if not bool(condition):
        raise AssertionError(name)


def red(value):
    if isinstance(value, s.MatrixBase):
        return value.applyfunc(s.simplify)
    return s.simplify(value)


def metric_geometry(metric, first, second) -> dict:
    """Levi-Civita/Ricci/Einstein from an arbitrary nondegenerate 2-jet.

    first[a][i,j]=partial_a metric_ij; second[a][b][i,j]=partial_ab
    metric_ij.  No adapted-frame assumption is made by this calculator.
    """
    inverse = metric.inv()
    inverse_first = [-inverse*first[a]*inverse for a in INDICES]
    gamma = [[[red(sum(inverse[k, l]*(first[i][j, l]+first[j][i, l]
                               -first[l][i, j])/2 for l in INDICES))
               for j in INDICES] for i in INDICES] for k in INDICES]
    dgamma = [[[[red(sum((inverse_first[a][k, l]
                          *(first[i][j, l]+first[j][i, l]-first[l][i, j])
                          +inverse[k, l]*(second[a][i][j, l]
                                           +second[a][j][i, l]
                                           -second[a][l][i, j]))/2
                         for l in INDICES))
                 for j in INDICES] for i in INDICES] for k in INDICES]
              for a in INDICES]
    ricci = s.Matrix(DIM, DIM, lambda i, j: red(sum(
        dgamma[k][k][i][j]-dgamma[j][k][i][k]
        +sum(gamma[k][k][l]*gamma[l][i][j]
             -gamma[k][j][l]*gamma[l][i][k] for l in INDICES)
        for k in INDICES)))
    scalar = red(s.trace(inverse*ricci))
    einstein = red(ricci-metric*scalar/2)
    return {"inverse": inverse, "gamma": gamma, "dgamma": dgamma,
            "ricci": ricci, "scalar": scalar, "einstein_cov": einstein,
            "einstein_contra": red(inverse*einstein*inverse)}


def observer_kinematics(metric, first, geometry, u, du, ddu=None) -> dict:
    """Complete h-kinematics from the contravariant unit-vector jet.

    du[a] is partial_a u; ddu[a][b] is partial_ab u.  The moving metric
    contributes to the covector jet and to the expansion's derivative.
    """
    inverse, gamma = geometry["inverse"], geometry["gamma"]
    omega = metric*u
    domega = [first[a]*u+metric*du[a] for a in INDICES]
    B = s.Matrix(DIM, DIM, lambda a, b: red(domega[a][b]
        -sum(gamma[c][a][b]*omega[c] for c in INDICES)))
    acceleration = red(B.T*u)
    spatial = red(B-omega*acceleration.T)
    K, twist = red((spatial+spatial.T)/2), red((spatial-spatial.T)/2)
    theta = red(s.trace(inverse*K))
    answer = {"omega": omega, "B": B, "acceleration": acceleration,
              "K": K, "Omega": twist, "theta": theta,
              "K_squared": red(s.trace(inverse*K*inverse*K.T)),
              "Omega_squared": red(s.trace(inverse*twist*inverse*twist.T))}
    if ddu is not None:
        dtheta = s.Matrix([red(sum(ddu[b][a][a]
            +sum(geometry["dgamma"][b][a][a][c]*u[c]
                 +gamma[a][a][c]*du[b][c] for c in INDICES)
            for a in INDICES)) for b in INDICES])
        answer["div_theta_u"] = red((u.T*dtheta)[0]+theta**2)
        # Independent coordinate divergence of a^j=u^b partial_b u^j
        # +Gamma^j_bd u^b u^d, retaining the connection's derivative.
        acceleration_vector = inverse*acceleration
        diva = sum(sum(du[j][b]*du[b][j]+u[b]*ddu[j][b][j]
                       for b in INDICES)
            +sum(geometry["dgamma"][j][j][b][c]*u[b]*u[c]
                 +gamma[j][b][c]*(du[j][b]*u[c]+u[b]*du[j][c])
                 for b in INDICES for c in INDICES)
            +sum(gamma[j][j][c]*acceleration_vector[c] for c in INDICES)
            for j in INDICES)
        answer["div_acceleration"] = red(diva)
    return answer


def reflected_jets(metric, first, second, omega, domega, ddomega):
    """Differentiate the full covariant reflection, with moving omega."""
    reflected = 2*omega*omega.T-metric
    reflected_first = [2*(domega[a]*omega.T+omega*domega[a].T)-first[a]
                       for a in INDICES]
    reflected_second = [[2*(ddomega[a][b]*omega.T
        +omega*ddomega[a][b].T+domega[a]*domega[b].T
        +domega[b]*domega[a].T)-second[a][b]
        for b in INDICES] for a in INDICES]
    return reflected, reflected_first, reflected_second


def _adapted_contractions(eq):
    """Polynomial identities with arbitrary a(3), symmetric K(6), Omega(3)."""
    a = s.Matrix(s.symbols("a1:4", real=True))
    kvals = s.symbols("K11 K12 K13 K22 K23 K33", real=True)
    K = s.Matrix([[kvals[0], kvals[1], kvals[2]],
                  [kvals[1], kvals[3], kvals[4]],
                  [kvals[2], kvals[4], kvals[5]]])
    o12, o13, o23 = s.symbols("O12 O13 O23", real=True)
    O = s.Matrix([[0, o12, o13], [-o12, 0, o23], [-o13, -o23, 0]])
    B, fullK, fullO, fulla = s.zeros(4), s.zeros(4), s.zeros(4), s.zeros(4, 1)
    B[0, 1:4], B[1:4, 1:4] = a.T, K+O
    fullK[1:4, 1:4], fullO[1:4, 1:4], fulla[1:4, 0] = K, O, a
    u = s.eye(4)[:, 0]
    dg = [2*(B[a0, :].T*u.T+u*B[a0, :]) for a0 in INDICES]
    C = [[[s.expand(sum(ETA[c, d]*(dg[a0][b, d]+dg[b][a0, d]
                  -dg[d][a0, b])/2 for d in INDICES))
           for b in INDICES] for a0 in INDICES] for c in INDICES]
    formula = [[[2*u[c]*fullK[a0, b]-2*u[a0]*u[b]*fulla[c]
                 -2*u[a0]*fullO[b, c]-2*u[b]*fullO[a0, c]
                 for b in INDICES] for a0 in INDICES] for c in INDICES]
    eq(s.Matrix(4, 16, lambda c, j: C[c][j//4][j % 4]),
       s.Matrix(4, 16, lambda c, j: formula[c][j//4][j % 4]),
       "general_adapted_connection_all64_components")
    eq(s.Matrix([sum(C[c][a0][c] for c in INDICES) for a0 in INDICES]),
       s.zeros(4, 1), "general_connection_trace_zero")
    theta = s.trace(K)
    contracted = s.Matrix([sum(ETA[a0, b]*C[c][a0][b]
                         for a0 in INDICES for b in INDICES) for c in INDICES])
    eq(contracted, -2*(theta*u+fulla), "general_connection_metric_contraction")
    omega_squared = sum(O[i, j]**2 for i in range(3) for j in range(3))
    # Since h is normal and u=e0, partial_c g^{ab}=2(B_ca u_b+u_a B_cb).
    derivative_contraction = sum(2*(B[c, a0]*u[b]+u[a0]*B[c, b])*C[c][a0][b]
                                for c in INDICES for a0 in INDICES for b in INDICES)
    eq(derivative_contraction, 8*omega_squared,
       "general_moving_inverse_metric_contraction_eight_twist")
    quadratic = sum(ETA[a0, b]*C[c][b][d]*C[d][a0][c]
        for a0 in INDICES for b in INDICES for c in INDICES for d in INDICES)
    eq(quadratic, -4*omega_squared, "general_quadratic_connection_minus_four_twist")


def _conformal_fixture(B, f, T):
    """Actual realizable h=e^(2f)I, omega=e^f(1,z)/sqrt(1+|z|²).

    f(0)=df(0)=z(0)=0, dz=B[:,1:], d²z=T.  Both covector and vector
    second jets include unit normalization; these are not independent
    unconstrained observer derivatives.
    """
    metric, omega = s.eye(4), s.eye(4)[:, 0]
    first = [s.zeros(4) for _ in INDICES]
    second = [[2*f[a, b]*s.eye(4) for b in INDICES] for a in INDICES]
    domega = [B[a, :].T for a in INDICES]
    ddomega = [[s.Matrix([f[a, b]-sum(B[a, i]*B[b, i] for i in range(1, 4)),
                           *T[a][b][1:]]) for b in INDICES] for a in INDICES]
    du = domega
    ddu = [[ddomega[a][b]-second[a][b]*omega for b in INDICES] for a in INDICES]
    return metric, first, second, omega, domega, ddomega, du, ddu


def _jet_controls(eq):
    rng = Random(571)
    for trial in range(8):
        B = s.Matrix([[s.Integer(rng.randrange(-3, 4))*(j != 0)
                       for j in INDICES] for _ in INDICES])
        f = s.zeros(4)
        T = [[[s.Integer(0) for _ in INDICES] for _ in INDICES] for _ in INDICES]
        for a in INDICES:
            for b in range(a, 4):
                f[a, b] = f[b, a] = rng.randrange(-2, 3)
                T[a][b] = T[b][a] = [s.Integer(0)]+[
                    s.Integer(rng.randrange(-2, 3)) for _ in range(1, 4)]
        fixture = _conformal_fixture(B, f, T)
        h, dh, ddh, omega, dw, ddw, du, ddu = fixture
        hg = metric_geometry(h, dh, ddh)
        g, dg, ddg = reflected_jets(h, dh, ddh, omega, dw, ddw)
        gg = metric_geometry(g, dg, ddg)
        obs = observer_kinematics(h, dh, hg, omega, du, ddu)
        theta, K2, O2, div = [obs[k] for k in
            ("theta", "K_squared", "Omega_squared", "div_theta_u")]
        eq(hg["scalar"], -6*s.trace(f), "curved_h_scalar_"+str(trial))
        eq(obs["B"], B, "complete_observer_first_jet_"+str(trial))
        eq(div, 3*f[0, 0]-sum(B[0, i]**2 for i in range(1, 4))
           +sum(T[0][i][i] for i in range(1, 4))+theta**2,
           "unit_normalized_observer_second_jet_"+str(trial))
        eq(gg["scalar"]+hg["scalar"], 2*(theta**2-K2-O2)-4*div,
           "full_curved_scalar_reflection_"+str(trial))
        # Independently compute acceleration divergence from the vector jet.
        utheta = div-theta**2
        diva = obs["div_acceleration"]
        eq(hg["ricci"][0, 0], diva-utheta-K2+O2,
           "independent_unit_vector_Raychaudhuri_"+str(trial))
        eq(gg["scalar"], -hg["scalar"]+2*hg["ricci"][0, 0]
           -2*(div+diva)-4*O2, "Ricci_divergence_reflection_"+str(trial))
    B = s.zeros(4)
    B[1, 2], B[2, 1] = 1, -1
    zeroT = [[[s.Integer(0) for _ in INDICES] for _ in INDICES] for _ in INDICES]
    h, dh, ddh, omega, dw, ddw, du, ddu = _conformal_fixture(B, s.zeros(4), zeroT)
    hg = metric_geometry(h, dh, ddh)
    obs = observer_kinematics(h, dh, hg, omega, du, ddu)
    g, dg, ddg = reflected_jets(h, dh, ddh, omega, dw, ddw)
    actual = metric_geometry(g, dg, ddg)["scalar"]
    eq(obs["Omega_squared"], 2, "hostile_twist_two_index_norm")
    eq(actual, -4, "hostile_twist_required_in_scalar")
    require(actual != 0, "hostile_twist_deletion_rejected")


def _actual_native_geometry(data, eq):
    h_y, u_y, y = (data[k] for k in ("h_y", "u_y", "coordinate"))
    h = red(h_y.subs(y, 0))
    dh, ddh = [s.zeros(4) for _ in INDICES], [[s.zeros(4) for _ in INDICES] for _ in INDICES]
    dh[2], ddh[2][2] = red(h_y.diff(y).subs(y, 0)), red(h_y.diff(y, 2).subs(y, 0))
    u = red(u_y.subs(y, 0))
    du = [s.zeros(4, 1) for _ in INDICES]
    ddu = [[s.zeros(4, 1) for _ in INDICES] for _ in INDICES]
    du[2], ddu[2][2] = red(u_y.diff(y).subs(y, 0)), red(u_y.diff(y, 2).subs(y, 0))
    hg = metric_geometry(h, dh, ddh)
    obs = observer_kinematics(h, dh, hg, u, du, ddu)
    eq((u.T*h*u)[0], 1, "actual_positive_unit_observer")
    eq(hg["scalar"], -s.Rational(32, 25), "actual_native_positive_metric_curvature")
    eq(obs["acceleration"], s.zeros(4, 1), "actual_native_acceleration_zero")
    eq(obs["theta"], 0, "actual_native_expansion_zero")
    eq(obs["K_squared"], s.Rational(8, 25), "actual_native_shear_contraction")
    eq(obs["Omega_squared"], s.Rational(8, 25), "actual_native_twist_contraction")
    eq(obs["div_theta_u"], 0, "actual_native_expansion_divergence_zero")
    omega_y = red(h_y*u_y)
    w = red(omega_y.subs(y, 0))
    dw = [s.zeros(4, 1) for _ in INDICES]
    ddw = [[s.zeros(4, 1) for _ in INDICES] for _ in INDICES]
    dw[2], ddw[2][2] = red(omega_y.diff(y).subs(y, 0)), red(omega_y.diff(y, 2).subs(y, 0))
    g, dg, ddg = reflected_jets(h, dh, ddh, w, dw, ddw)
    eq(g, ETA, "actual_native_reflected_Lorentz_metric_flat_value")
    eq(s.Matrix.hstack(*dg), s.zeros(4, 16), "actual_native_reflected_metric_first_jet_zero")
    eq(s.Matrix.hstack(*(ddg[a][b] for a in INDICES for b in INDICES)),
       s.zeros(4, 64), "actual_native_reflected_metric_second_jet_zero")
    gg = metric_geometry(g, dg, ddg)
    eq(gg["scalar"], 0, "actual_native_Lorentz_scalar_zero")
    eq(hg["scalar"]+gg["scalar"],
       2*(obs["theta"]**2-obs["K_squared"]-obs["Omega_squared"])
       -4*obs["div_theta_u"], "actual_native_full_reflection_curvature_identity")
    # h depends algebraically on s and s=1+y.  At unit determinant the
    # covariant-metric Euler tensor for integral Rh is -G_h^{ab}.
    euler = red(-s.trace(hg["einstein_contra"].T*dh[2]))
    eq(euler, -s.Rational(192, 125), "independent_tensor_material_Euler_matches_reduced_IBP")
    return {"Rh": "-32/25", "Rg": "0", "K_squared": "8/25",
            "Omega_squared": "8/25", "material_Euler": "-192/125"}


def run_checks(repo: Path | None = None, native: dict | None = None) -> dict:
    """Narrow exact controls; no foreign checker or old suite is executed."""
    repo = ROOT if repo is None else Path(repo).resolve()
    checks = []
    def eq(actual, expected, name):
        difference = actual-expected
        entries = list(difference) if isinstance(difference, s.MatrixBase) else [difference]
        require(all(s.expand(value) == 0 or s.simplify(value) == 0 for value in entries), name)
        checks.append(name)
    _adapted_contractions(eq)
    _jet_controls(eq)
    actual = _actual_native_geometry(native, eq) if native is not None else None
    return {"schema": "d0-lorentz-reflection-geometry/1", "exact_checks": len(checks),
            "general_polynomial_connection_identities": True,
            "exact_curved_moving_observer_jets": 8,
            "hostile_nonzero_twist_fixture": True, "actual_native_geometry": actual,
            "controls_are_not_the_general_proof": True,
            "physical_metric_binding_or_admission_derived": False}
