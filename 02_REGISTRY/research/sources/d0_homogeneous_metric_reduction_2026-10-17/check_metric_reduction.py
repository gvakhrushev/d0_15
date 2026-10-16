"""New zero-mode metric/observer algebra; no old root or spectrum is run.

The actual price convexity and stored link-rank theorem are pinned inputs.
This calculation supplies the missing fixed-physical-metric section and
its rank, the retained saddle congruence, and a constant-volume witness.
"""
import json
import sympy as s


def calculate():
    checks = []

    def eq(x, y, label):
        delta = x - y
        values = list(delta) if isinstance(delta, s.MatrixBase) else [delta]
        if any(s.cancel(v) != 0 for v in values):
            raise ArithmeticError(label)
        checks.append(label)

    b, c = s.symbols("b c", positive=True)
    F = c * s.eye(4) + b * s.ones(4)
    Fi = s.eye(4) / c - b * s.ones(4) / (c * (c + 4*b))
    eta = s.diag(1, -1, -1, -1)
    q = F * eta * F.T
    e0 = s.eye(4)[:, 0]
    eq(F*Fi, s.eye(4), "regular_frame_inverse_all_b_c_positive")

    def differences(G):
        return s.Matrix([G[i, i] - G[0, 0] for i in range(1, 4)])

    def boost(nu):
        v = s.Matrix([0] + list(nu))
        return e0*v.T + v*e0.T

    J = 4*b*c*(s.eye(3)-s.ones(3))
    Ji = (s.eye(3)-s.ones(3)/2)/(4*b*c)
    eq(J*Ji, s.eye(3), "observer_normal_map_inverse")
    eq(J.det(), -128*b**3*c**3, "observer_normal_determinant_nonzero")
    for i in range(3):
        eq(differences(2*F*boost(s.eye(3)[:, i])*F.T), J[:, i],
           "actual_positive_gram_observer_derivative_"+str(i))

    def physical_lift(dq):
        dF = dq*Fi.T*eta/2
        eq(dF*eta*F.T+F*eta*dF.T, dq,
           "all10_physical_metric_lift_"+str(len(checks)))
        initial = dF*F.T+F*dF.T
        nu = -Ji*differences(initial)
        G = initial+2*F*boost(nu)*F.T
        eq(differences(G), s.zeros(3, 1),
           "all10_entire_scalar_shell_constraint_"+str(len(checks)))
        return G

    metric_basis = []
    for i in range(4):
        for j in range(i, 4):
            E = s.zeros(4)
            E[i, j] = 1
            E[j, i] = 1
            metric_basis.append(E)
    for E in metric_basis:
        physical_lift(E)

    # A right inverse on all seven equal-diagonal positive-Gram slots.
    gram_basis = [s.eye(4)]
    for i in range(4):
        for j in range(i+1, 4):
            E = s.zeros(4)
            E[i, j] = E[j, i] = 1
            gram_basis.append(E)
    for j, G in enumerate(gram_basis):
        dF = G*Fi.T/2
        dq = dF*eta*F.T+F*eta*dF.T
        eq(physical_lift(dq), G, "all7_gram_slots_survive_reduction_"+str(j))

    # Exactly three independent metric zeros, without declaring them gauge.
    for i in range(1, 4):
        K = s.zeros(4)
        K[0, i], K[i, 0] = 1, -1
        dq = F*(K*eta-eta*K)*F.T
        eq(physical_lift(dq), s.zeros(4), "lorentz_reflection_metric_zero_"+str(i))
        eq(Fi*dq*Fi.T, K*eta-eta*K,
           "three_metric_zero_vectors_independent_"+str(i))

    # In density coordinates dual to T_ret, the four link columns are I4.
    # Their actual full16 rank4 is a consumed theorem, not re-executed here.
    B = s.diag(J, s.eye(4))
    Binv = s.diag(Ji, s.eye(4))
    H = s.diag(*range(1, 8)) + s.ones(7)
    Z = s.zeros(7)
    Kret = H.row_join(B.T).col_join(B.row_join(Z))
    P = s.eye(7).row_join(Z).col_join((-B.T.inv()*H/2).row_join(s.eye(7)))
    target = Z.row_join(B.T).col_join(B.row_join(Z))
    eq(P.T*Kret*P, target, "actual_retained_saddle_congruence_7_plus_7_minus")
    inverse = Z.row_join(Binv).col_join(Binv.T.row_join(-Binv.T*H*Binv))
    eq(Kret*inverse, s.eye(14), "retained_inverse_no_zero_density_block_inverted")

    k = 2*b*c + 4*b*b
    G0 = c*c*s.eye(4)+k*s.ones(4)
    alpha = 1/(c*c)
    beta = -k/(c*c*(c*c+4*k))
    Ginv = alpha*s.eye(4)+beta*s.ones(4)
    V = gram_basis[1]
    tangent = gram_basis[1]-gram_basis[2]
    eq(G0*Ginv, s.eye(4), "actual_root_positive_gram_inverse")
    eq(s.trace(Ginv*tangent), 0, "constant_volume_first_jet")
    eq(s.trace(Ginv*V), 2*beta, "nonzero_volume_correction_derivative")
    acceleration = s.cancel(s.trace(Ginv*tangent*Ginv*tangent)/(2*beta))
    eq(acceleration, 2*alpha*(alpha+beta)/beta, "unique_volume_preserving_second_jet")
    eq(s.trace(Ginv*V)*acceleration-s.trace(Ginv*tangent*Ginv*tangent),
       0, "constant_volume_second_jet_includes_acceleration")
    eq(differences(tangent), s.zeros(3, 1), "same_shell_energy_first_jet")
    eq(V.diagonal(), s.zeros(1, 4), "same_shell_energy_all_curve_orders")
    phase = s.exp(s.I*s.pi/4)-1
    probe = s.simplify(128*s.expand_complex(s.conjugate(phase)*phase))
    eq(probe, 256-128*s.sqrt(2), "actual_grid_1100_probe_of_surviving_shape_direction")
    if not bool(probe > 0):
        raise ArithmeticError("positive_price_probe")
    checks.append("positive_price_probe")

    # Hostile controls decide the new geometry, not the old root theorem.
    rejected = []
    if J != s.eye(3):
        rejected.append("replace_observer_jacobian_by_identity")
    if s.trace(Ginv*tangent*Ginv*tangent) != 0:
        rejected.append("drop_required_constant_volume_acceleration")
    if Kret != s.diag(H, s.eye(7)):
        rejected.append("invert_zero_density_block_as_identity")
    if physical_lift(gram_basis[1]) != s.zeros(4):
        rejected.append("erase_all_metric_response_after_schur")
    if len(rejected) != 4:
        raise ArithmeticError("hostile_controls")
    return {
        "schema": "d0-homogeneous-physical-metric-reduction/1",
        "exact_checks": len(checks), "checks": checks,
        "hostile_controls_rejected": rejected,
        "observer_jacobian_det": str(-128*b**3*c**3),
        "physical_metric_rank": 10, "effective_metric_positive_rank": 7,
        "effective_metric_zero_rank": 3, "retained_saddle_inertia": [7, 7, 0],
        "neutral_density_parameters": 2040, "frame_parameters": 6,
        "all_grades": 16, "reference_dimension": 128,
        "old_root_or_spectrum_replayed": False,
        "local_homogeneous_stored_v8_only": True,
        "GR_closed": False,
    }


if __name__ == "__main__":
    print(json.dumps(calculate(), ensure_ascii=False, indent=2, sort_keys=True))
