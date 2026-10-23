#!/usr/bin/env python3
"""Full native CAR current, unit-observer reflection and complete source jet.

The owned current uses its RETAINED reference/frame; normalizing its output
does not select or erase that input.  Covariant h is positive, covariant g
is Lorentzian (+---).  No state grade, direct matter equation, link equation
or physical admission is removed by this kinematic source calculation.
Only pinned Python owner definitions are imported, never their checks.
"""
from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path
import sys

import sympy as s


ROOT = Path(__file__).resolve().parents[4]
CERT = "02_REGISTRY/research/certificates/"
PINS = {
    "a4d_native_correlated_current_transition.py":
        "e659733a8ab4fea30f46de56663dc344249420c7e0a3ea65b2aa1a2091b76e0d",
    "a4d_native_reference_memory_preparation.py":
        "67e416c75cc213efca6040cea8cb796efbcff78037e09b31fb6a83acdcfd0e3a",
    "a4d_native_record_metric_chronology_check.py":
        "16929d026206ee69e126484ed2ac7b1dfd2537c1e50c0fc4c4293408caf58527",
    "a4d_native_fock_record_binding_check.py":
        "42e83e6f93b48ce4d4420f829d8e79c993a215d7b1a4c6a2f812bd45fd914078",
    "a4d_native_jones_record_transport.py":
        "b19f6c864af7e75c2a48d9892692b4d94337d06c04a83013b180148a1752c53f",
    "a4d_native_fibonacci_record_activation.py":
        "9a016fa4b1a8261a29f626ed7450db7987727957e634799519aede0e3ab587ee",
}
STATE_PROVENANCE = {
    "path": CERT+"a4d_native_engine_correlated_current_extension_check.py",
    "git_blob": "f134307e5ecd73621387adada0d796d97fb63ad0",
    "definition": "symbolic_transition_mismatch, lines 192-209",
    "state": "m=-2*a*p*e_mask0+(2*p-1)*e_mask1+s*(e_mask13+e_mask14)",
    "foreign_checker_imported_or_executed": False,
}
ETA = s.diag(1, -1, -1, -1)


def require(condition: object, name: str) -> None:
    if not bool(condition):
        raise AssertionError(name)


def current_owner(repo: Path):
    for path, digest in PINS.items():
        require(hashlib.sha256((repo/CERT/path).read_bytes()).hexdigest() == digest,
                "source_pin:"+path)
    name = "lorentz_reflection_owned_current_definition"
    spec = importlib.util.spec_from_file_location(name, repo/CERT/next(iter(PINS)))
    if spec is None or spec.loader is None:
        raise RuntimeError("owned_current_definition_unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def reflection(g: s.MatrixBase, J: s.MatrixBase):
    """h=-g+2(gJ)(gJ)^T/g(J,J), on the open timelike current domain."""
    kappa = (J.T*g*J)[0]
    b = g*J
    return -g+2*b*b.T/kappa


def reflection_jet(g, J, dg, dJ):
    """Complete numerator AND current/metric normalization derivative."""
    kappa = (J.T*g*J)[0]
    b, db = g*J, dg*J+g*dJ
    dkappa = (J.T*dg*J+2*J.T*g*dJ)[0]
    return -dg+2*(db*b.T+b*db.T)/kappa-2*b*b.T*dkappa/kappa**2


def reflection_source(g, J, E):
    """Metric/current cotangent pair for ANY symmetric h-covector E.

    Convention dA=Tr(E^T dh)=Tr(M^T dg)+B^T dJ.  Packed symmetric
    off-diagonal coordinates consequently carry their ordinary factor two.
    The complete native metric covector also includes (D_g J)^* B; the
    complete matter covector is direct_matter+(D_m J)^* B on ALL16 slots.
    """
    kappa = (J.T*g*J)[0]
    b = g*J
    c = E*b
    scalar = (b.T*c)[0]
    M = -E+2*(c*J.T+J*c.T)/kappa-2*scalar*J*J.T/kappa**2
    B = 4*(g*c-scalar*b/kappa)/kappa
    return M, B


def rest_current_jacobian(C, m):
    """All16 real matter columns of the actual normalized CAR current."""
    alphas = C.car_operators()[3]
    N = C.red((m.T*m)[0])
    require(N != 0, "nonzero_full_matter_required")
    r = s.Matrix([C.red((m.T*A*m)[0]/N) for A in alphas])
    D = s.Matrix.vstack(*(2*m.T*(A-r[i]*s.eye(16))/N
                          for i, A in enumerate(alphas)))
    return C.mat(D), r, N, tuple(alphas)


def full_current_jet(C, F, m, dF, dm):
    """All frame/pairing/operator/normalizer terms via owned covariance.

    Owned exterior covariance gives current(F,m)=F*current(I,rho(F)^-1 m).
    Differentiating it retains dW, d(alpha), and reference-frame motion;
    it does not treat the CAR matrices as fixed under a metric variation.
    """
    inverse = F.inv()
    exterior_inverse = C.C.ext(inverse)
    rest = exterior_inverse*m
    frame_generator = C.C.exterior_jet(dF*inverse)
    drest = exterior_inverse*(dm-frame_generator*m)
    D, r, _N, _alpha = rest_current_jacobian(C, rest)
    return C.mat(dF*s.Matrix([1, *r])+F*s.Matrix([0, *(D*drest)]))


def literal_rest_current_jet(C, m, dF, dm):
    """Independent direct derivative of the literal C.current at F=I.

    dW and the W-adjoint inside each alpha are explicitly differentiated.
    This is used only as a narrow binding of the compact covariance formula.
    """
    dG = -dF-dF.T
    dW = C.C.dcompound(s.eye(4), dG)
    creators, beta, gammas, alphas = C.car_operators()
    dcreators = [C.C.creator(dF[:, i]) for i in range(4)]
    dadj = [dcreators[i].T+creators[i].T*dW-dW*creators[i].T
            for i in range(4)]
    dbeta = dcreators[0]+dadj[0]
    N = C.red((m.T*m)[0])
    dN = C.red((dm.T*m+m.T*dm+m.T*dW*m)[0])
    r, dots = [], []
    for i in range(3):
        value = C.red((m.T*alphas[i]*m)[0]/N)
        dalpha = dbeta*gammas[i]+beta*(dcreators[i+1]-dadj[i+1])
        numerator = (dm.T*alphas[i]*m+m.T*alphas[i]*dm
                     +m.T*(dW*alphas[i]+dalpha)*m)[0]
        r.append(value)
        dots.append(C.red((numerator-value*dN)/N))
    return C.mat(dF*s.Matrix([1, *r])+s.Matrix([0, *dots]))


def matter_lift(C, m, spatial_current_tangent):
    """Construct all three current directions inside the full16 tangent.

    Timelike |r|<1 makes I-r*r^T positive.  The lift is norm-tangent;
    no other grade or direct matter equation is removed.
    """
    _D, r, _N, alphas = rest_current_jacobian(C, m)
    coefficient = (s.eye(3)-r*r.T).inv()*spatial_current_tangent/2
    return C.mat(sum((coefficient[i]*(A-r[i]*s.eye(16))*m
                      for i, A in enumerate(alphas)), s.zeros(16, 1)))


def fixed_current_line_lift(C, F, m, dF):
    """Compensate any metric/frame jet by full native matter directions.

    The invariant condition is dJ=lambda*J, not dJ=0: the retained frame
    can change the time component.  A radial matter term also preserves
    the moving W-norm.  This is a kinematic tangent construction, not a
    state-selected engine transition or a new physical preparation rule.
    """
    inverse = F.inv()
    exterior = C.C.ext(F)
    exterior_inverse = C.C.ext(inverse)
    rest = exterior_inverse*m
    _D, r, N, _alphas = rest_current_jacobian(C, rest)
    metric_current_jet = inverse*full_current_jet(C, F, m, dF, s.zeros(16, 1))
    scale = metric_current_jet[0]
    target = scale*r-metric_current_jet[1:4, :]
    tangent = exterior*matter_lift(C, rest, target)
    generator = C.C.exterior_jet(dF*inverse)
    radial = C.red((rest.T*exterior_inverse*generator*m)[0]/N)
    return C.mat(tangent+radial*m), C.red(scale)


def native_data(repo: Path | None = None) -> dict:
    repo = ROOT if repo is None else Path(repo).resolve()
    C = current_owner(repo)
    parameter = s.Symbol("s", real=True)
    m = s.zeros(16, 1)
    m[0], m[1], m[13], m[14] = -2*C.a*C.p, 2*C.p-1, parameter, parameter
    J = C.current(s.eye(4), m)
    K = 1+4*parameter**2
    u = s.Matrix([1+2*parameter**2, -2*parameter**2, 0, 0])/s.sqrt(K)
    h = s.simplify(reflection(ETA, J))
    y = s.Symbol("y", real=True)
    return {"C": C, "parameter": parameter, "m": m, "J": J, "u": u,
            "g": ETA, "h": h, "coordinate": y,
            "h_y": h.subs(parameter, 1+y), "u_y": u.subs(parameter, 1+y)}


def run_checks(repo: Path | None = None) -> dict:
    data = native_data(repo)
    C, t, m, J, u, h = (data[k] for k in ("C", "parameter", "m", "J", "u", "h"))
    checks = []
    def eq(actual, expected, name):
        difference = actual-expected
        entries = list(difference) if isinstance(difference, s.MatrixBase) else [difference]
        require(all(C.red(x) == 0 for x in entries), name)
        checks.append(name)
    # For rational expressions containing the real amplitude parameter, the
    # owner reducer has its existing EX coefficient domain.
    def reqeq(actual, expected, name):
        difference = actual-expected
        entries = list(difference) if isinstance(difference, s.MatrixBase) else [difference]
        require(all(C.red(x) == 0 for x in entries), name)
        checks.append(name)
    reqeq((m.T*m)[0], 1+2*t**2, "actual_full16_preparation_normalizer")
    reqeq(J, s.Matrix([1, -2*t**2/(1+2*t**2), 0, 0]), "literal_owned_current_on_family")
    reqeq((J.T*ETA*J)[0], (1+4*t**2)/(1+2*t**2)**2,
          "actual_current_is_timelike_for_all_real_amplitudes")
    reqeq((u.T*ETA*u)[0], 1, "normalized_unit_observer")
    reqeq(J, s.sqrt(1+4*t**2)*u/(1+2*t**2), "observer_is_normalized_actual_current")
    reqeq(h, C.observer_pairing(ETA, J), "reflection_equals_actual_pairing_owner")
    reqeq(h*u, ETA*u, "same_observer_covector_for_both_metrics")
    reqeq((u.T*h*u)[0], 1, "positive_metric_unit_observer")
    reqeq(h.det(), 1, "same_absolute_volume_determinant")
    reqeq(reflection(h, J), ETA, "exact_reflection_involution")
    point_m = m.subs(t, 1)
    point_J = J.subs(t, 1)
    point_h = h.subs(t, 1)
    point_dm = m.diff(t).subs(t, 1)
    D, r, N, alphas = rest_current_jacobian(C, point_m)
    eq(N, 3, "actual_point_full_norm_three")
    eq(r, s.Matrix([-s.Rational(2, 3), 0, 0]), "actual_point_spatial_current")
    eq(J.diff(t).subs(t, 1), s.Matrix([0, -s.Rational(4, 9), 0, 0]),
       "current_jet_contains_moving_state_normalizer")
    frozen = C.red((point_dm.T*alphas[0]*point_m+point_m.T*alphas[0]*point_dm)[0]/N)
    eq(frozen, -s.Rational(4, 3), "hostile_frozen_current_normalizer_differs")
    require(frozen != -s.Rational(4, 9), "frozen_normalizer_rejected")
    features = s.Matrix.hstack(*((A-r[i]*s.eye(16))*point_m for i, A in enumerate(alphas)))
    for i, A in enumerate(alphas):
        eq(A.T, A, "owned_current_selfadjoint_"+str(i))
        for j, B in enumerate(alphas):
            eq(A*B+B*A, (2 if i == j else 0)*s.eye(16),
               "owned_full_CAR_current_relation_"+str(i)+str(j))
    eq(features.T*features, N*(s.eye(3)-r*r.T), "full16_current_Gram_identity")
    eq((s.eye(3)-r*r.T).inv(), s.diag(s.Rational(9, 5), 1, 1),
       "timelike_Gram_has_three_positive_directions")
    lift = s.Matrix.hstack(*(matter_lift(C, point_m, s.eye(3)[:, i]) for i in range(3)))
    eq(D*lift, s.eye(3), "constructive_lift_all_three_observer_directions")
    eq(point_m.T*lift, s.zeros(1, 3), "lift_preserves_complete_state_norm_to_first_order")
    # This price-independent symmetric E simultaneously tests every h-covector.
    slots = [(i, j) for i in range(4) for j in range(i, 4)]
    coefficients = s.symbols("E0:10", real=True)
    E = s.zeros(4)
    for value, (i, j) in zip(coefficients, slots):
        E[i, j] = E[j, i] = value
    M, B = reflection_source(ETA, point_J, E)
    eq((B.T*point_J)[0], 0, "current_radial_amplitude_has_no_reflection_source")
    metric_columns, matter_columns, fixed_line_metric_columns = [], [], []
    for kind, dimension in (("metric", 10), ("matter", 16)):
        for index in range(dimension):
            dg, dm = s.zeros(4), s.zeros(16, 1)
            if kind == "metric":
                i, j = slots[index]
                dg[i, j] = dg[j, i] = 1
                # g=F^-T eta F^-1: this is the exact full metric/coframe jet.
                dF = -ETA*dg/2
            else:
                dm[index] = 1
                dF = s.zeros(4)
            dJ = full_current_jet(C, s.eye(4), point_m, dF, dm)
            eq(dJ, literal_rest_current_jet(C, point_m, dF, dm),
               "literal_vs_covariant_current_jet_"+kind+str(index))
            dh = reflection_jet(ETA, point_J, dg, dJ)
            curve = s.Symbol("curve", real=True)
            independent = reflection(ETA+curve*dg, point_J+curve*dJ).diff(curve).subs(curve, 0)
            eq(dh, independent, "independent_reflection_derivative_"+kind+str(index))
            eq(s.trace(E.T*independent), s.trace(M.T*dg)+(B.T*dJ)[0],
               "complete_price_independent_Euler_pullback_"+kind+str(index))
            if kind == "metric":
                compensator, scale = fixed_current_line_lift(C, s.eye(4), point_m, dF)
                line_jet = full_current_jet(C, s.eye(4), point_m, dF, compensator)
                eq(line_jet, scale*point_J, "actual_fixed_current_line_lift_"+str(index))
                moving_W = C.C.dcompound(s.eye(4), -dF-dF.T)
                eq((2*point_m.T*compensator+point_m.T*moving_W*point_m)[0], 0,
                   "fixed_line_lift_preserves_moving_full_state_norm_"+str(index))
                eq((B.T*line_jet)[0], 0, "all10_compensated_observer_sources_zero_"+str(index))
                fixed_dh = reflection_jet(ETA, point_J, dg, s.zeros(4, 1))
                eq(reflection_jet(ETA, point_J, dg, line_jet), fixed_dh,
                   "metric_jet_holds_current_line_not_vector_"+str(index))
                fixed_line_metric_columns.append(s.Matrix([fixed_dh[i, j] for i, j in slots]))
            (metric_columns if kind == "metric" else matter_columns).append(dJ)
    require(s.Matrix.hstack(*matter_columns).shape == (4, 16), "all16_matter_columns_retained")
    require(s.Matrix.hstack(*metric_columns).shape == (4, 10), "all10_metric_columns_retained")
    eq(s.Matrix.hstack(*fixed_line_metric_columns).det(), 1,
       "fixed_current_line_all10_metric_Jacobian_invertible")
    # Exact transverse geometry jets, supplied to the independent geometry owner.
    eq(point_h, s.Matrix([[s.Rational(13, 5), s.Rational(12, 5), 0, 0],
                         [s.Rational(12, 5), s.Rational(13, 5), 0, 0],
                         [0, 0, 1, 0], [0, 0, 0, 1]]), "actual_transverse_positive_metric")
    reqeq(h.diff(t).subs(t, 1), s.Matrix([[s.Rational(96, 25), s.Rational(104, 25), 0, 0],
                                       [s.Rational(104, 25), s.Rational(96, 25), 0, 0],
                                       [0, 0, 0, 0], [0, 0, 0, 0]]), "actual_transverse_metric_first_jet")
    reqeq(u.diff(t).subs(t, 1), s.Matrix([8, -12, 0, 0])/(5*s.sqrt(5)),
          "actual_observer_derivative_is_not_frozen")
    chi_s = -4*t/(1+4*t**2)
    reqeq(chi_s.subs(t, 1), -s.Rational(4, 5), "actual_rapidity_transverse_derivative")
    # a=h*u=g*u.  For a(y), (a wedge da)_(t,x1,y)=a1*a0'-a0*a1'.
    observer_covector = ETA*u
    twist = observer_covector[1]*observer_covector[0].diff(t)-observer_covector[0]*observer_covector[1].diff(t)
    reqeq(twist.subs(t, 1), -s.Rational(4, 5), "actual_Frobenius_twist_nonzero")
    # Reduced material Euler operator AFTER integration by parts, not partial_s R.
    first, second = s.symbols("s_y s_yy", real=True)
    reduced_L = -2*chi_s**2*first**2
    reduced_EL = (s.diff(reduced_L, t)-s.diff(s.diff(reduced_L, first), t)*first
                  -s.diff(s.diff(reduced_L, first), first)*second)
    reqeq(reduced_EL, 4*chi_s*(s.diff(chi_s, t)*first**2+chi_s*second),
          "reduced_curvature_matter_Euler_after_IBP")
    reqeq(reduced_EL.subs({t: 1, first: 1, second: 0}), -s.Rational(192, 125),
          "actual_transverse_material_Euler_nonzero")
    reqeq(s.diff(reduced_L, t).subs({t: 1, first: 1}), s.Rational(192, 125),
          "hostile_pointwise_partial_is_opposite_to_Euler_source")
    return {"schema": "d0-native-lorentz-current-source/1", "source_pins_sha256": PINS,
            "state_owner": STATE_PROVENANCE, "exact_checks": len(checks),
            "native_matter_components": 16, "metric_directions": 10,
            "observer_directions": 3, "current_kernel_is_not_matter_gauge": True,
            "current": "(1,-2*s^2/(1+2*s^2),0,0)", "state_normalizer": "1+2*s^2",
            "current_jet_s1": "(0,-4/9,0,0)", "frozen_normalizer_wrong_jet": "-4/3",
            "transverse_unit_observer_s1": "(3,-2,0,0)/sqrt(5)",
            "positive_metric_volume": 1, "transverse_twist_coefficient": "-4/5",
            "reduced_Rh_material_Euler_s1": "-192/125",
            "pointwise_partial_s_Rh_s1": "+192/125",
            "price_independent_metric_and_full_matter_Euler_pullback": True,
            "all10_metric_directions_have_norm_preserving_current_LINE_lifts": True,
            "reference_frame_pairing_operator_and_normalizer_jets_retained": True,
            "retained_reference_selected_or_erased": False,
            "parallel_or_twistfree_observer_forced": False,
            "physical_admission_or_native_on_shell_derived": False}
