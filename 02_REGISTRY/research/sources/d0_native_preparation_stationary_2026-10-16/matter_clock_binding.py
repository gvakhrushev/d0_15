#!/usr/bin/env python3
"""One smooth comparator/native-pairing equality family, not an AF price identity.

Only pinned owner definitions are imported.  No old run/check entrypoint,
receipt, external output file, Lean compilation or physical admission is used.
The general smooth-field proof is in A4D_NATIVE_MATTER_CLOCK_RECORD_BINDING.md.
"""
from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path
import sys

import sympy as s


ROOT = Path(__file__).resolve().parents[4]
PINS = {
    "02_REGISTRY/research/sources/d0_flat_record_2026-10-15/check_flat_record.py":
        "acc5f43bc652f111ab46ea090357a9e9289b1153aca1cbdc4892ec893c9de1a2",
    "02_REGISTRY/research/sources/d0_record_geometry_source_integration_2026-10-15/check_phase_metric_source.py":
        "8da7532d611a60be2137143286c23c2aa26c19297add7f079b57087495204b4d",
    "02_REGISTRY/research/sources/d0_lorentz_reflection_source_2026-10-16/native_current.py":
        "d9282fad2124f57addeeeece96e34ba017a041d63002f37f0c2e990661f175c3",
}


def require(condition: object, name: str) -> None:
    if not bool(condition):
        raise AssertionError(name)


def owners(repo: Path):
    modules = []
    for i, (path, digest) in enumerate(PINS.items()):
        require(hashlib.sha256((repo/path).read_bytes()).hexdigest() == digest,
                "source_pin:"+path)
        if i == 0:
            # The phase owner imports this same pinned frame definition itself.
            continue
        name = "matter_clock_binding_owned_definition_"+str(i)
        spec = importlib.util.spec_from_file_location(name, repo/path)
        if spec is None or spec.loader is None:
            raise RuntimeError("owner_definition_unavailable:"+path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        modules.append(module)
    return tuple(modules)


def encode(rest_matter, reference, p):
    """Explicit lambda=1 wiring, in the retained ordered full16 mask frame."""
    difference = rest_matter-reference
    return ([p**2+difference[a] for a in range(12)],
            s.Matrix(difference[12:16, :]))


def decode(weights, clocks, reference, p):
    return reference+s.Matrix([w-p**2 for w in weights]+list(clocks))


def clock_embedding(phase):
    """The actual theta=k X restriction of the owned full24 target."""
    embedding = s.zeros(24, 16)
    embedding[:12, :12] = s.eye(12)
    embedding[12:, 12:] = phase.k
    return embedding


def base_full_inverse(phase, golden_variance):
    """All16 outputs: four normality, ten packed metric, two chi slots."""
    inverse = s.zeros(16)
    for mu in range(4):
        inverse[12+mu, mu] = 2/golden_variance
    for col, (mu, nu) in enumerate(phase.slots):
        V = s.zeros(4)
        V[mu, nu] = V[nu, mu] = 1
        for a in range(12):
            inverse[a, 4+col] = (
                3*(phase.k[a, :]*V*phase.k[a, :].T)[0]-s.trace(V)
            )/golden_variance
    inverse[:12, 14:] = phase.K/golden_variance
    return inverse


def run_checks(repo: Path | None = None) -> dict:
    repo = ROOT if repo is None else Path(repo).resolve()
    phase, native = owners(repo)
    data = native.native_data(repo)
    C = data["C"]
    p, variance = C.p, C.p**3
    reference = C.mat(data["m"].subs(data["parameter"], 1))
    checks = []

    def eq(actual, expected, name):
        difference = actual-expected
        entries = list(difference) if isinstance(difference, s.MatrixBase) else [difference]
        require(all(C.red(s.simplify(value)) == 0 for value in entries), name)
        checks.append(name)

    # Consume the original ordered frame, its matching profiles and source split.
    labels, vectors = phase.owner.frame(4)
    require(labels == phase.labels and len(vectors) == 12, "literal_owned_pair_frame")
    eq(s.Matrix.vstack(*(v.T for v in vectors)), phase.k, "owned_k_reconstruction")
    eq(phase.k.T*phase.k, 6*s.eye(4), "complete_clock_frame_second_moment")
    eq(phase.M*phase.K, s.zeros(10, 2), "owned_matching_kernel_retained")
    eq(phase.K.T*phase.K, s.Matrix([[8, 4], [4, 8]]), "owned_matching_normalization")

    # No reset/selected matter sector: this affine chart has sixteen independent columns.
    raw = s.Matrix(s.symbols("rest0:16", real=True))
    weights, clocks = encode(raw, reference, p)
    eq(decode(weights, clocks, reference, p), raw, "all16_wiring_round_trip")
    control = s.Matrix([w-p**2 for w in weights]+list(clocks))
    eq(control.jacobian(raw), s.eye(16), "full16_control_jacobian_lambda_one")
    Dcurrent, rest_current, N, _alphas = native.rest_current_jacobian(C, reference)
    eq(N, 3, "actual_s1_full_matter_normalizer")
    eq(rest_current, s.Matrix([-s.Rational(2, 3), 0, 0]), "actual_s1_current")
    eq(1-(rest_current.T*rest_current)[0], s.Rational(5, 9),
       "actual_base_is_strictly_timelike")

    # Literal complete SU(2) channel and its actual endpoint comparator.
    # Positive a,b are kept independent until reducing a^2+b^2=1; this avoids
    # silently treating sqrt(1-w) as real outside the declared probability domain.
    aa, bb = s.symbols("channel_a channel_b", positive=True)
    turn, angle = s.symbols("channel_turn channel_angle", real=True)
    z = s.Symbol("comparator_z", positive=True)
    a_y = aa*s.cos(turn)-bb*s.sin(turn)
    b_y = bb*s.cos(turn)+aa*s.sin(turn)
    W0 = s.Matrix([[aa, -bb], [bb, aa]])
    Wy = s.Matrix([[a_y, -b_y*s.exp(-s.I*angle)],
                   [b_y*s.exp(s.I*angle), a_y]])

    def circle(value):
        value = s.cancel(s.trigsimp(s.expand(value)))
        numerator, denominator = s.fraction(value)
        relation = s.Poly(aa**2+bb**2-1, aa, domain="EX")
        numerator = s.Poly(numerator, aa, domain="EX").rem(relation).as_expr()
        denominator = s.Poly(denominator, aa, domain="EX").rem(relation).as_expr()
        return s.simplify(s.cancel(numerator/denominator))

    for row in range(2):
        for col in range(2):
            require(circle((Wy.H*Wy-s.eye(2))[row, col]) == 0,
                    "literal_channel_unitary_"+str(row)+str(col))
            checks.append("literal_channel_unitary_"+str(row)+str(col))
    P0 = s.diag(1, 0)
    comparator = Wy.H*W0
    leakage = P0*comparator.H*(s.eye(2)-P0)*comparator*P0
    price = -s.log((s.eye(2)-z*leakage).det())
    coincident = {turn: 0, angle: 0}
    require(circle(leakage[1, 1]) == 0, "comparator_unused_mode_is_retained_zero")
    for left, right, expected, name in (
        (turn, turn, 2*z, "literal_comparator_amplitude_angle_Hessian"),
        (angle, angle, 2*z*aa**2*bb**2, "literal_comparator_phase_Hessian"),
        (turn, angle, 0, "literal_comparator_mixed_Hessian"),
    ):
        require(circle(s.diff(price, left, right).subs(coincident)-expected) == 0, name)
        checks.append(name)
    # dw/dturn=2ab. Dividing this Hessian by2z yields exactly
    # dw^2/(4w(1-w))+w(1-w)dtheta^2, then1/12 for the full comparator.

    # Exact full12-column projector at the flat/curved common zero-jet.
    J = s.zeros(24, 12)
    for a in range(12):
        J[2*a, a], J[2*a+1, a] = C.a, p
    eq(J.H*J, s.eye(12), "all24_record_outcomes_full_isometry")
    P = J*J.H
    eq(P*P, P, "literal_rank12_projector")
    eq(s.trace(P), 12, "whole_projector_trace")

    # Restrict the actual24-target coefficient definition, not a second germ/connection.
    embedding = clock_embedding(phase)
    first_Z = s.zeros(16, 4)
    first_Z[12:, :] = s.eye(4)
    first = embedding*first_Z
    second = [[s.zeros(24, 1) for _nu in range(4)] for _mu in range(4)]
    weights0 = [p**2]*12
    F24, q0, gamma24, _normality24, _B24 = phase.coefficients(weights0, first, second)
    F0 = C.mat(F24*embedding)
    q0 = C.mat(q0)
    gamma = C.mat(embedding.T*gamma24*embedding)
    eq(q0, variance*s.eye(4)/2, "actual_comparator_flat_record_metric")
    expected_F0 = s.zeros(16)
    expected_F0[:4, 12:] = variance*s.eye(4)/2
    expected_F0[4:14, :12] = variance*phase.M/12
    expected_F0[14:, :12] = variance*phase.leftK
    eq(F0, expected_F0, "full16_clock_target_coefficient_matrix")
    inverse0 = base_full_inverse(phase, variance)
    eq(F0*inverse0, s.eye(16), "full16_base_inverse_including_normality")
    inverse_bound = max(sum(abs(C.red(variance*x)) for x in row)
                        for row in inverse0.tolist())
    eq(inverse_bound, 14, "full_eta_inverse_max_norm_not_just_normal_coefficients")

    # A genuinely curved SMOOTH program: only w_(01,+)=p^2+kappa*(x0)^2.
    # The whole exact formula is used, not arbitrary assigned generator jets.
    kappa = s.Rational(1, 1000)
    coordinates = s.symbols("clock_x0:4", real=True)
    y = coordinates[0]
    origin = dict.fromkeys(coordinates, 0)
    curved_weights = [p**2+kappa*y**2]+[p**2]*11
    curved_clocks = s.Matrix(coordinates)
    rest_germ = decode(curved_weights, curved_clocks, reference, p)
    re_w, re_X = encode(rest_germ, reference, p)
    eq(s.Matrix(re_w), s.Matrix(curved_weights), "same_program_curved_weights_round_trip")
    eq(re_X, curved_clocks, "same_program_curved_clocks_round_trip")
    eq(rest_germ.subs(origin), reference, "curved_program_uses_actual_timelike_base")
    Z_germ = s.Matrix(curved_weights+list(curved_clocks))
    eq(Z_germ.jacobian(coordinates).subs(origin), first_Z,
       "curved_first_jet_differentiated_from_full_smooth_program")
    v_y = curved_weights[0]*(1-curved_weights[0])
    q_y = (variance*s.eye(4)/2+(v_y-variance)*vectors[0]*vectors[0].T/12
           +(2*kappa*y)**2*s.eye(4)[:, 0]*s.eye(4)[:, 0].T/(48*v_y))
    eq(q_y.subs(y, 0), q0, "curved_program_zero_jet")
    eq(q_y.diff(y).subs(y, 0), s.zeros(4), "curved_program_first_metric_jet")
    second_q = C.mat(q_y.diff(y, 2).subs(y, 0))
    eq(second_q, kappa*variance*vectors[0]*vectors[0].T/6
       +kappa**2*s.eye(4)[:, 0]*s.eye(4)[:, 0].T/(6*variance),
       "curved_metric_from_exact_smooth_channel_formula")
    scalar = C.red((second_q[0, 0]-s.trace(second_q))/(variance/2)**2)
    eq(scalar, -2*kappa/(3*variance), "genuine_nonzero_intrinsic_scalar_curvature")
    require(scalar != 0, "curved_not_only_a_flat_metric_rank_witness")

    curved_second = [[embedding*Z_germ.diff(coordinates[mu]).diff(coordinates[nu]).subs(origin)
                      for nu in range(4)] for mu in range(4)]
    eq(curved_second[0][0], 2*kappa*s.eye(24)[:, 0],
       "curved_second_jet_differentiated_from_full_smooth_program")
    curved24, curved_q, _gamma2, _C2, _B2 = phase.coefficients(weights0, first, curved_second)
    curved_F = C.mat(curved24*embedding)
    perturbation = s.zeros(16)
    perturbation[4, 0] = -kappa/(12*variance)
    eq(curved_F, F0+perturbation, "literal_smooth_curved_full16_map")
    # The owner keeps p as a FORMAL real golden generator.  Its quotient
    # reducer proves identities, not positivity on a chosen real branch.
    # Select that branch only for this strict inequality.
    tube_margin_positive_branch = s.simplify(
        C.red(variance**2-s.Rational(7, 3)*kappa).subs(C.p, (s.sqrt(5)-1)/2))
    require(tube_margin_positive_branch.is_positive is True,
            "curved_full16_map_inside_safe_Neumann_tube")
    column, row = s.zeros(16, 1), s.zeros(1, 16)
    column[4], row[0, 0] = -kappa/(12*variance), 1
    denominator = C.red(1+(row*inverse0*column)[0])
    inverse = C.mat(inverse0-inverse0*column*row*inverse0/denominator)
    eq(curved_F*inverse, s.eye(16), "curved_full16_inverse_without_metric_inverse_PDE")
    eq(curved_q, q0, "curved_map_uses_the_same_projector_metric")

    # Independent differentiation of the metric.  Normality must hold as a FIELD:
    # C*d_mu eta=-(d_mu C)*eta; its remaining normal derivative drops out.
    normality = first_Z.T*gamma
    dnormality = [s.zeros(4, 16) for _mu in range(4)]
    dnormality[0][0, 0] = kappa/(24*variance)
    frozen_witness = False
    for col in range(12):
        eta = inverse[:, 4+col]
        eq(normality*eta, s.zeros(4, 1), "curved_true_normal_test_"+str(col))
        derivative_eta = [-first_Z*q0.inv()*D*eta for D in dnormality]
        metric_parameter_jet = s.zeros(16)
        for a in range(12):
            metric_parameter_jet[a, a] = -eta[a]/(48*variance)
        metric_parameter_jet[12:, 12:] = sum(
            (variance*eta[a]*vectors[a]*vectors[a].T/12 for a in range(12)), s.zeros(4))
        direct = first_Z.T*metric_parameter_jet*first_Z
        frozen = direct.copy()
        for mu in range(4):
            for nu in range(4):
                direct[mu, nu] += (derivative_eta[mu].T*gamma*first_Z[:, nu]
                                   +first_Z[:, mu].T*gamma*derivative_eta[nu])[0]
        expected = s.zeros(4)
        if col < 10:
            mu, nu = phase.slots[col]
            expected[mu, nu] = expected[nu, mu] = 1
        eq(direct, expected, "curved_full_metric_derivative_"+str(col))
        eq(variance*phase.leftK*eta[:12, :],
           s.eye(2)[:, col-10] if col >= 10 else s.zeros(2, 1),
           "curved_internal_chi_derivative_"+str(col))
        if any(C.red(x) != 0 for x in direct-frozen):
            frozen_witness = True
    require(frozen_witness, "hostile_frozen_clock_normal_field_rejected")

    # Exact native equality in whitened coordinates.  No giant arbitrary sqrt(F).
    eta = native.ETA
    j = s.Matrix([1, *rest_current])
    H = C.observer_pairing(eta, j)
    boost = s.eye(4)
    boost[:2, :2] = s.Matrix([[3, 2], [2, 3]])/s.sqrt(5)
    eq(boost*boost, H, "actual_current_positive_square_root")
    eq(boost*eta*boost.T, eta, "actual_root_is_Lorentz_boost")
    whitened_m = C.mat(C.C.ext(boost)*reference)
    whitened_J = C.current(boost, whitened_m)
    eq(whitened_J, s.sqrt(5)*s.eye(4)[:, 0]/3,
       "literal_current_of_transported_full16_state")
    eq(C.observer_pairing(eta, whitened_J), s.eye(4),
       "literal_native_pairing_equals_whitened_record_metric")
    eq(C.C.ext(boost.inv())*whitened_m, reference, "no_reset_rest_state_reconstruction")
    W = C.C.ext((boost*boost.T).inv())
    eq((whitened_m.T*W*whitened_m)[0], N,
       "retained_native_pairing_normalizer_not_frozen")

    # Generic tangent identity keeps ALL16 matter, ALL10 metric and ALL6 O jets.
    zeta = s.Matrix(s.symbols("matter_jet0:16", real=True))
    V = s.zeros(4)
    for value, (mu, nu) in zip(s.symbols("metric_jet0:10", real=True), phase.slots):
        V[mu, nu] = V[nu, mu] = value
    omega = s.zeros(4)
    for value, (mu, nu) in zip(s.symbols("orthogonal_jet0:6", real=True),
                              ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))):
        omega[mu, nu], omega[nu, mu] = value, -value
    dj = s.Matrix([0, *(Dcurrent*zeta)])
    dH = C.mat(native.reflection_jet(eta, j, s.zeros(4), dj))
    eigenframe = s.eye(4)
    eigenframe[:2, :2] = s.Matrix([[1, 1], [1, -1]])/s.sqrt(2)
    eigenvalues = [s.sqrt(5), 1/s.sqrt(5), 1, 1]
    transformed = eigenframe.T*dH*eigenframe
    root_jet = eigenframe*s.Matrix(4, 4, lambda i, j:
        transformed[i, j]/(eigenvalues[i]+eigenvalues[j]))*eigenframe.T
    eq(boost*root_jet+root_jet*boost, dH, "full16_actual_H_root_Sylvester_jet")
    scale = variance/2
    # This is sqrt(scale)*deltaF in a FIXED base whitening frame.
    dF_white = root_jet+omega*boost-V*boost/(2*scale)
    native_pairing_jet = (-dF_white*boost.inv()-boost.inv()*dF_white.T
                          +boost.inv()*dH*boost.inv())
    eq(native_pairing_jet, V/scale,
       "full10_16_6_joint_equality_jet_no_frozen_frame_or_matter")
    dJ_white = dF_white*j+boost*dj
    dg_white = -eta*(dF_white*eta*boost.T+boost*eta*dF_white.T)*eta
    eq(native.reflection_jet(eta, whitened_J, dg_white, dJ_white), V/scale,
       "native_current_normalizer_and_frame_source_match_same_metric_jet")

    return {
        "schema": "d0-matter-clock-record-binding/1",
        "source_pins_sha256": PINS, "exact_checks": len(checks),
        "record_program": "owned complete12-channel COMPARATOR; theta=kX",
        "record_carrier_complex_dimension": 24, "full_real_matter_components": 16,
        "orthogonal_frame_coordinates": 6, "equality_graph_field_slots": 22,
        "raw_native_field_slots": 32, "transverse_matching_equations_unclosed": 10,
        "wiring": "lambda=1; ordered12 amplitudes plus4 material scalar clocks",
        "base": "actual full-CAR s=1 state, N=3, timelike current gap5/9",
        "base_full_eta_inverse_max_norm": "14/p^3",
        "nearby_full_eta_bound": "28/p^3 if full16 map distance<=p^3/28",
        "curved_smooth_program": "w_(01,+)=p^2+(x0)^2/1000; otherw=p^2; X=x",
        "curved_scalar_at_origin": "-1/(1500*p^3)",
        "whole_neighbourhood_equality": "proved analytically in companion memo",
        "arbitrary_prescribed_metric_inverse_solved": False,
        "same_AF_W_E_spectral_price_or_metric_identified": False,
        "full_native_Euler_inferred_from_graph_stationarity": False,
        "wiring_or_primitive_admission_derived": False,
        "controller_archive_cost_or_physical_Info_selected": False,
        "new_JSON_or_Lean_or_old_suites": False,
    }
