"""Actual comparator source on the full raw frame/matter chart.

Only existing definition modules are imported.  This consumer neither chooses
an aggregation/volume law nor executes an old certificate/receipt entrypoint.
The curved Lorentz control is inside the owned matter-clock matching family.
"""
from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path
import sys

import sympy as s


ROOT = Path(__file__).resolve().parents[4]
CLOCK_PATH = "02_REGISTRY/research/sources/d0_native_preparation_stationary_2026-10-16/matter_clock_binding.py"
ENGINE_PATH = "02_REGISTRY/research/certificates/a4d_native_closed_record_engine.py"
PINS = {
    CLOCK_PATH: "1b2c668bca6c99ca84a4be513274fddc2c9a82a832368abc4a75ee24f58fbb71",
    "02_REGISTRY/research/sources/d0_record_geometry_source_integration_2026-10-15/check_phase_metric_source.py":
        "8da7532d611a60be2137143286c23c2aa26c19297add7f079b57087495204b4d",
    "02_REGISTRY/research/sources/d0_lorentz_reflection_source_2026-10-16/native_current.py":
        "d9282fad2124f57addeeeece96e34ba017a041d63002f37f0c2e990661f175c3",
    ENGINE_PATH: "7aead2716c7bf7899a134eedbf4b87dbe1ef9c85900189b5afc8cdfeed13f0f9",
}


def require(condition, label):
    if not bool(condition):
        raise AssertionError(label)


def owner(repo):
    for relative, digest in PINS.items():
        require(hashlib.sha256((repo/relative).read_bytes()).hexdigest() == digest,
                "record_frame_source_pin:"+relative)
    name = "record_frame_source_owned_clock_definition"
    spec = importlib.util.spec_from_file_location(name, repo/CLOCK_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("matter_clock_definition_unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    phase, native = module.owners(repo)
    return module, phase, native


def engine_definition(repo):
    """Only the pinned State/step definitions; never an engine entrypoint."""
    name = "record_frame_source_owned_closed_engine_definition"
    spec = importlib.util.spec_from_file_location(name, repo/ENGINE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("closed_engine_definition_unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def endpoint_channel(w, u, delta):
    """Exact leakage and all three derivatives on 0<w,u<1, real delta."""
    vw, vu = w*(1-w), u*(1-u)
    rw, ru = s.sqrt(vw), s.sqrt(vu)
    leakage = w+u-2*w*u-2*rw*ru*s.cos(delta)
    left = 1-2*u-(1-2*w)*ru*s.cos(delta)/rw
    right = 1-2*w-(1-2*u)*rw*s.cos(delta)/ru
    phase = 2*rw*ru*s.sin(delta)
    return leakage, left, right, phase


def ricci_two_dimensional_first_coordinate(metric, x):
    """Literal Levi-Civita/Ricci calculation; sphere-positive convention."""
    inverse = s.simplify(metric.inv())
    derivative = lambda value, coordinate: s.diff(value, x) if coordinate == 0 else 0
    Gamma = [[[s.simplify(sum(inverse[a, d]*(derivative(metric[d, c], b)
                 +derivative(metric[d, b], c)-derivative(metric[b, c], d))
                 for d in range(2))/2) for c in range(2)]
                 for b in range(2)] for a in range(2)]
    ricci = s.Matrix(2, 2, lambda b, d: s.simplify(sum(
        derivative(Gamma[a][b][d], a)-derivative(Gamma[a][b][a], d)
        +sum(Gamma[a][a][e]*Gamma[e][b][d]-Gamma[a][d][e]*Gamma[e][b][a]
             for e in range(2)) for a in range(2))))
    return ricci, s.simplify(s.trace(inverse*ricci))


def run(repo=None):
    repo = ROOT if repo is None else Path(repo).resolve()
    clock, phase, native = owner(repo)
    data = native.native_data(repo)
    C = data["C"]
    checks = []

    def eq(actual, expected, label):
        difference = actual-expected
        entries = list(difference) if isinstance(difference, s.MatrixBase) else [difference]
        require(all(C.red(s.simplify(s.trigsimp(value))) == 0 for value in entries), label)
        checks.append(label)

    def yes(condition, label):
        require(condition, label)
        checks.append(label)

    # One actual complete channel: retain its second (zero-leakage) mode.
    ax, bx, ay, by = s.symbols("ax bx ay by", positive=True)
    delta = s.Symbol("endpoint_phase_difference", real=True)
    Wx = s.Matrix([[ax, -bx*s.exp(-s.I*delta)],
                   [bx*s.exp(s.I*delta), ax]])
    Wy = s.Matrix([[ay, -by], [by, ay]])
    comparator = Wy.H*Wx
    P0 = s.diag(1, 0)
    feedback = P0*comparator.H*(s.eye(2)-P0)*comparator*P0
    amp_leakage = bx*bx*ay*ay+ax*ax*by*by-2*ax*bx*ay*by*s.cos(delta)
    eq(s.expand_complex(feedback[0, 0]), amp_leakage,
       "actual_complete_unitary_comparator_channel_leakage")
    eq(feedback[1, 1], 0, "second_channel_mode_retained_zero")
    w, u = s.symbols("left_weight right_weight", positive=True)
    f, Aleft, Aright, Aphase = endpoint_channel(w, u, delta)
    eq(s.diff(f, w), Aleft, "complete_left_amplitude_endpoint_derivative")
    eq(s.diff(f, u), Aright, "complete_right_amplitude_endpoint_derivative")
    eq(s.diff(f, delta), Aphase, "complete_phase_endpoint_derivative")
    z = s.Symbol("fixed_allowed_fugacity", positive=True)
    price = -s.log(1-z*f)
    for variable, response in ((w, Aleft), (u, Aright), (delta, Aphase)):
        eq(s.diff(price, variable), z*response/(1-z*f),
           "actual_logdet_price_source_"+str(variable))

    # All16 controls of each endpoint, using the OWNED affine wiring and k.
    reference = C.mat(data["m"].subs(data["parameter"], 1))
    raw = s.Matrix(s.symbols("full_rest0:16", real=True))
    weights, clocks = clock.encode(raw, reference, C.p)
    control = s.Matrix(weights+list(phase.k*clocks))
    Dcontrol = control.jacobian(raw)
    expected_control = s.eye(12).row_join(s.zeros(12, 4)).col_join(
        s.zeros(12, 12).row_join(phase.k))
    eq(Dcontrol, expected_control, "full16_actual_control_differential")
    left_amplitude = s.Matrix(s.symbols("left_amplitude_source0:12", real=True))
    phase_source = s.Matrix(s.symbols("phase_source0:12", real=True))
    eq(Dcontrol.T*s.Matrix.vstack(left_amplitude, phase_source),
       s.Matrix.vstack(left_amplitude, phase.k.T*phase_source),
       "all16_endpoint_covector_includes_four_clock_phase_slots")
    yes(phase.k.shape == (12, 4), "all12_channels_and_all16_rest_slots_retained")

    # Full exterior source at an actual point of the matching family.
    # c is kept positive and symbolic until the exact substitution c=p^3/2.
    c = s.Symbol("positive_record_scale", positive=True)
    B = s.diag(1, 1, 1, 1)
    B[:2, :2] = s.Matrix([[3, 2], [2, 3]])/s.sqrt(5)
    eta = s.diag(1, -1, -1, -1)
    Hstar = B*B
    F = B/s.sqrt(c)
    Finv = s.sqrt(c)*B.inv()
    rho = C.C.ext(F)
    rhoinv = C.C.ext(Finv)
    m = rho*reference
    eq(rhoinv*m, reference, "actual_matching_point_all16_rest_recovery")
    eq(B*eta*B.T, eta, "actual_positive_boost_root_is_Lorentz")
    eq(Finv.T*Hstar*Finv, c*s.eye(4), "actual_positive_native_metric_at_matching_point")
    eq(Finv.T*eta*Finv, c*eta, "actual_covariant_Lorentz_metric_at_matching_point")
    e0 = s.Matrix(s.symbols("full_rest_covector0:16", real=True))
    Em = rhoinv.T*e0
    Rcolumns = []
    for i in range(4):
        for j in range(4):
            dF = s.zeros(4)
            dF[i, j] = 1
            dRho = C.C.exterior_jet(dF*Finv)*rho
            column = dRho*reference
            Rcolumns.append(column)
            # Independent differentiation of the inverse exterior matrix.
            direct_inverse = C.C.dcompound(Finv, -Finv*dF*Finv)*m
            eq(direct_inverse, -rhoinv*column,
               "literal_inverse_exterior_frame_derivative_"+str((i, j)))
    R = s.Matrix.hstack(*Rcolumns)
    EF = -R.T*Em
    eq(rho.T*Em, e0, "all16_matter_cotangent_pullback")
    eq(EF+R.T*Em, s.zeros(16, 1), "complete_raw_frame_force_cancels_off_shell")
    # These are actual raw-chart h/O variations with m0 fixed.  All ten
    # symmetric rows and all six rotations are tested, not a fitted frame jet.
    for mu, nu in phase.slots:
        V = s.zeros(4)
        V[mu, nu] = V[nu, mu] = 1
        dF = -V*F/(2*c)
        vector = s.Matrix(list(dF))
        eq((EF.T*vector+Em.T*(R*vector))[0], 0,
           "zero_raw_h_costate_"+str((mu, nu)))
        A = dF*Finv
        eq(-c*(A.T+A), V, "actual_raw_h_variation_"+str((mu, nu)))
    for mu in range(4):
        for nu in range(mu+1, 4):
            omega = s.zeros(4)
            omega[mu, nu], omega[nu, mu] = 1, -1
            dF = omega*F
            vector = s.Matrix(list(dF))
            eq((EF.T*vector+Em.T*(R*vector))[0], 0,
               "zero_raw_O_costate_"+str((mu, nu)))
            eq(dF*Finv+(dF*Finv).T, s.zeros(4),
               "actual_O_motion_keeps_positive_metric_"+str((mu, nu)))

    # The curved control is the SAME full smooth matter-clock program.
    coordinates = s.Matrix(s.symbols("x0:4", real=True))
    rest_germ = reference+s.Matrix.vstack(s.zeros(12, 1), coordinates)
    flat_w, flat_X = clock.encode(rest_germ, reference, C.p)
    eq(s.Matrix(flat_w), s.ones(12, 1)*C.p**2, "same_program_germ_all12_weights_golden")
    eq(flat_X, coordinates, "same_program_germ_actual_four_matter_clocks")
    variance = C.p**3
    q_record = variance*phase.k.T*phase.k/12
    eq(q_record, variance*s.eye(4)/2, "actual_comparator_metric_flat_for_entire_germ")
    _, rest_r, rest_N, _ = native.rest_current_jacobian(C, reference)
    eq(rest_N, 3, "same_fullCAR_reference_norm_three")
    eq(rest_r, s.Matrix([-s.Rational(2, 3), 0, 0]), "same_fullCAR_reference_current")
    eq(Hstar, native.reflection(eta, s.Matrix([1, *rest_r])),
       "positive_root_bound_to_actual_fullCAR_reference")
    r1, r2, r3 = s.symbols("timelike_r1 timelike_r2 timelike_r3", real=True)
    H = native.reflection(eta, s.Matrix([1, r1, r2, r3]))
    eq(H*eta*H, eta, "entire_timelike_positive_pairing_is_Lorentz")
    kappa = s.Symbol("rotation_rate", real=True)
    t = coordinates[0]
    theta = kappa*t
    O = s.eye(4)
    O[:2, :2] = s.Matrix([[s.cos(theta), -s.sin(theta)],
                          [s.sin(theta), s.cos(theta)]])
    eq(O*O.T, s.eye(4), "actual_free_O_rotation_is_orthogonal")
    g = s.trigsimp(c*O*eta*O.T)
    eq(g[:2, :2], c*s.Matrix([[s.cos(2*theta), s.sin(2*theta)],
                              [s.sin(2*theta), -s.cos(2*theta)]]),
       "Lorentz_metric_of_same_matching_family")
    ric2, scalar = ricci_two_dimensional_first_coordinate(g[:2, :2], t)
    eq(scalar, 4*kappa**2*s.cos(2*theta)/c, "exact_nonzero_Lorentz_scalar_of_same_program")
    ric4 = s.zeros(4)
    ric4[:2, :2] = ric2
    einstein = s.trigsimp(ric4-g*scalar/2)
    eq(ric4.subs(t, 0), s.diag(2*kappa**2, -2*kappa**2, 0, 0),
       "actual_matching_family_Ricci_at_origin")
    eq(einstein.subs(t, 0), s.diag(0, 0, 2*kappa**2, 2*kappa**2),
       "same_program_does_not_force_vacuum_Lorentz_Einstein")
    eq(einstein, s.diag(0, 0, 2*kappa**2*s.cos(2*theta),
                                  2*kappa**2*s.cos(2*theta)),
       "entire_exact_Einstein_tensor_product_geometry")
    yes(not rest_germ.has(kappa) and not q_record.has(kappa),
        "actual_matter_clock_program_and_positive_metric_independent_of_rotation_rate")

    # A second ACTUAL matching point is also a literal Z[a] engine input.
    # The subsequent obstruction ranges over ALL Lorentz F', not sampled
    # frames.  Its proof uses the invariant norm of the retained first grade.
    fixed_metric_start = len(checks)
    engine = engine_definition(repo)
    ring_values = [engine.ZERO]*16
    ring_values[0] = -2*engine.A*engine.P
    ring_values[1] = engine.P*engine.P*engine.P
    for mask in (12, 13, 14, 15):
        ring_values[mask] = engine.ONE
    ring_input = engine.State(tuple(ring_values))

    def ring_vector(state):
        return C.mat(s.Matrix([sum(s.Integer(value)*C.a**degree
                                   for degree, value in enumerate(slot.coefficients))
                                for slot in state.matter]))

    dagger = reference+s.eye(16)[:, 12]+s.eye(16)[:, 15]
    eq(ring_vector(ring_input), dagger, "matching_dagger_is_actual_full16_ring_state")
    eq(dagger[1], C.p**3, "dagger_first_grade_is_positive_golden_cube")
    yes(ring_input.matter[1].sign() == 1 and engine.P.sign() == 1,
        "dagger_literal_engine_selects_positive_branch")
    yes(all(not ring_input.matter[mask] for mask in (2, 3, 4, 5, 8, 9)),
        "dagger_satisfies_all_six_actual_engine_guards")
    eq((dagger.T*dagger)[0], 5, "dagger_full_matter_normalizer_five")
    eq(C.current(s.eye(4), dagger), s.Matrix([1, 0, 0, 0]),
       "dagger_full_CAR_current_rest_without_grade_removal")
    eq(native.reflection(eta, C.current(s.eye(4), dagger)), s.eye(4),
       "dagger_native_positive_pairing_identity")
    dagger_weights, dagger_clocks = clock.encode(dagger, reference, C.p)
    eq(s.Matrix(dagger_weights), s.ones(12, 1)*C.p**2,
       "dagger_all_twelve_weights_still_golden")
    eq(dagger_clocks, s.Matrix([1, 0, 0, 1]), "dagger_actual_clock_offset")
    dagger_current_D, _dagger_r, _dagger_N, _ = native.rest_current_jacobian(C, dagger)
    expected_clock_current_D = s.zeros(3, 4)
    expected_clock_current_D[0, :] = s.Matrix([[2, -2, -2, 2]])/5
    eq(dagger_current_D[:, 12:16], expected_clock_current_D,
       "dagger_clock_jet_moves_retained_reference_in_matching_lift")

    ring_output = engine.step(ring_input)
    output = ring_vector(ring_output)
    time_coefficient = C.a*(4*C.p-3)
    expected_output = s.zeros(16, 1)
    expected_output[0], expected_output[1] = 5*C.p-4, time_coefficient
    expected_output[12] = expected_output[14] = C.a-C.p
    expected_output[13] = expected_output[15] = -C.a-C.p
    eq(output, expected_output, "dagger_actual_engine_output_all16_not_rest_reset")
    yes(ring_output.matter[1].sign() == -1,
        "dagger_actual_engine_output_pairing_nonzero_negative")
    eq((output.T*output)[0], 5, "dagger_actual_engine_retains_full_norm")
    eq(C.current(s.eye(4), output), s.Matrix([1, 0, 0, 0]),
       "dagger_output_CAR_current_does_not_rescue_probability_domain")
    eq(time_coefficient**2, 65*C.p-40,
       "dagger_output_first_grade_invariant_squared_length")

    rest_time = s.Symbol("new_frame_rest_time", real=True)
    lower, upper = 3*C.p-2, 3*C.p-s.Rational(3, 2)
    encoded_time_weight = C.p**2+rest_time-reference[1]
    eq(encoded_time_weight.subs(rest_time, lower), 0,
       "new_frame_probability_lower_endpoint_exact")
    eq(encoded_time_weight.subs(rest_time, upper), s.Rational(1, 2),
       "new_frame_probability_upper_endpoint_exact")
    eq(upper+lower, 6*C.p-s.Rational(7, 2),
       "probability_interval_maximum_absolute_endpoint")
    rational_lower, rational_upper = s.Rational(205, 332), s.Rational(2, 3)
    eq(rational_lower**2+rational_lower-1, -s.Rational(139, 332**2),
       "strict_positive_golden_root_rational_lower_witness")
    eq(rational_upper**2+rational_upper-1, s.Rational(1, 9),
       "strict_positive_golden_root_rational_upper_witness")
    yes(0 < rational_lower and rational_lower > s.Rational(7, 12)
        and rational_upper < s.Rational(3, 4),
        "rational_root_bracket_controls_both_endpoint_signs_and_engine_sign")
    eq(time_coefficient**2-upper**2, 83*C.p-s.Rational(205, 4),
       "output_invariant_exceeds_probability_upper_endpoint_squared")
    eq(83*C.p-s.Rational(205, 4), 83*(C.p-rational_lower),
       "strict_positive_endpoint_gap_uses_same_root_bracket")
    eq(time_coefficient**2-lower**2, 86*C.p-53,
       "output_invariant_exceeds_probability_lower_endpoint_squared")
    yes(86*rational_lower-53 > 0 and 6*rational_lower-s.Rational(7, 2) > 0,
        "strict_rational_gaps_reject_closed_probability_endpoints")
    inverse_column = s.Matrix(s.symbols("arbitrary_Lorentz_inverse_column0:4", real=True))
    rest_grade_one = time_coefficient*inverse_column
    unit_column_defect = (inverse_column.T*eta*inverse_column)[0]-1
    eq(rest_grade_one[0]**2-time_coefficient**2-
       sum(rest_grade_one[i]**2 for i in range(1, 4)),
       time_coefficient**2*unit_column_defect,
       "all_Lorentz_frames_first_grade_bound_from_exact_constraint")

    # Smooth input germ in the SAME matching family, with F(0)=I.
    # Only its zero-point is asserted to be a literal ring-engine input.
    clock_scale = s.Symbol("dagger_clock_scale", positive=True)
    bend = s.Symbol("dagger_weight_curvature", real=True)
    dagger_germ = (dagger+clock_scale*s.Matrix.vstack(s.zeros(12, 1), coordinates)
                   +bend*t*t*s.eye(16)[:, 0])
    bent_weights, bent_clocks = clock.encode(dagger_germ, reference, C.p)
    eq(s.Matrix(bent_weights), s.Matrix([C.p**2+bend*t*t]+[C.p**2]*11),
       "dagger_curved_germ_same_actual_weight_wiring")
    eq(bent_clocks, dagger_clocks+clock_scale*coordinates,
       "dagger_curved_germ_same_actual_clock_wiring")
    bent_v = bent_weights[0]*(1-bent_weights[0])
    e_time, k_first = s.eye(4)[:, 0], phase.k[0, :].T
    bent_q = (clock_scale**2*variance*s.eye(4)/2
              +clock_scale**2*(bent_v-variance)*k_first*k_first.T/12
              +(2*bend*t)**2*e_time*e_time.T/(48*bent_v))
    bent_q = bent_q.subs(clock_scale**2, 2/variance)
    eq(bent_q.subs(t, 0), s.eye(4), "dagger_clock_scale_makes_actual_record_metric_identity")
    eq(s.diff(bent_q, t).subs(t, 0), s.zeros(4), "dagger_curved_metric_first_jet_zero")
    second_q = s.diff(bent_q, t, 2).subs(t, 0)
    eq(second_q, bend*k_first*k_first.T/3+bend**2*e_time*e_time.T/(6*variance),
       "dagger_curved_metric_second_jet_from_literal_germ")
    eq(second_q[0, 0]-s.trace(second_q), -bend/3,
       "dagger_actual_positive_metric_curvature_minus_kappa_over_three")
    fixed_metric_checks = len(checks)-fixed_metric_start
    return {
        "exact_checks": len(checks),
        "source_pins": PINS,
        "full_rest_slots": 16,
        "raw_h_costates": "all10_identically_zero_for_this_record_sector",
        "raw_O_costates": "all6_identically_zero_for_this_record_sector",
        "record_scale": "c=p^3/2",
        "same_program_Lorentz_scalar": "4*k^2*cos(2*k*x0)/c",
        "same_program_Einstein_origin": "diag(0,0,2*k^2,2*k^2)",
        "fixed_metric_engine_obstruction_exact_checks": fixed_metric_checks,
        "matching_engine_input_normalizer": "5",
        "matching_engine_output_first_grade": "a*(4*p-3)*e0",
        "all_fixed_eta_Lorentz_reference_frames_probability_compatible": False,
        "matching_engine_input_curved_positive_metric_scalar": "-kappa/3 at origin",
        "coupled_metric_output_law_derived": False,
        "physical_aggregation_measure_or_transport_selected": False,
        "full_native_joint_criticality_claimed": False,
    }
