"""Literal adaptive AF/closed-engine intertwiner on the existing full carrier.

The selector is the engine's sign of first-grade m[1], not the nonlinear
correlated CAR current.  Every selected branch acts on all16 CAR entries,
the AF scalar channel and its whole identity complement.  Reusing H4 is
not a fresh AF activation.  The general proofs are in the companion memo.
Only pinned definitions and role.af_embedding are consumed; no old suite
entrypoint, generated receipt or Lean compilation is called.
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
    "a4d_native_af_role_orbit_metric_check.py":
        "b718a3ea3e3f47087b664cc9bb194e0e09c5ae818836efdba3e63b9c11e4f2d5",
    "a4d_native_fibonacci_record_activation.py":
        "9a016fa4b1a8261a29f626ed7450db7987727957e634799519aede0e3ab587ee",
    "a4d_native_fock_record_binding_check.py":
        "42e83e6f93b48ce4d4420f829d8e79c993a215d7b1a4c6a2f812bd45fd914078",
    "a4d_native_correlated_current_transition.py":
        "e659733a8ab4fea30f46de56663dc344249420c7e0a3ea65b2aa1a2091b76e0d",
    "a4d_native_closed_record_engine.py":
        "7aead2716c7bf7899a134eedbf4b87dbe1ef9c85900189b5afc8cdfeed13f0f9",
    "a4d_native_reference_memory_preparation.py":
        "67e416c75cc213efca6040cea8cb796efbcff78037e09b31fb6a83acdcfd0e3a",
    "a4d_native_record_metric_chronology_check.py":
        "16929d026206ee69e126484ed2ac7b1dfd2537c1e50c0fc4c4293408caf58527",
    "a4d_native_jones_record_transport.py":
        "b19f6c864af7e75c2a48d9892692b4d94337d06c04a83013b180148a1752c53f",
}


def require(condition: object, name: str) -> None:
    if not bool(condition):
        raise AssertionError(name)


def owners(repo: Path):
    for path, digest in PINS.items():
        require(hashlib.sha256((repo/CERT/path).read_bytes()).hexdigest() == digest,
                "source_pin:"+path)
    name = "adaptive_engine_owned_role_definitions"
    spec = importlib.util.spec_from_file_location(name, repo/CERT/next(iter(PINS)))
    if spec is None or spec.loader is None:
        raise RuntimeError("role_owner_definitions_unavailable")
    role = importlib.util.module_from_spec(spec)
    sys.modules[name] = role
    spec.loader.exec_module(role)
    return role


def rotation(AF, exponent: int):
    """Integer power of the OWNED golden rotation; no new phase parameter."""
    if type(exponent) is not int:
        raise ValueError("integer_rotation_charge_required")
    R = s.Matrix([[AF.a, -AF.p], [AF.p, AF.a]])
    factor = R if exponent >= 0 else R.T
    out = s.eye(2)
    for _ in range(abs(exponent)):
        out = AF.mat(factor*out)
    return out


def word_data(AF, signs) -> dict:
    """Exact closed form for every finite chronological sign word.

    Input order is chronological s1,...,sr; operators multiply Ur...U1.
    The two channels are in the owner's existing Hadamard CAR basis.
    """
    signs = tuple(signs)
    if any(type(value) is not int or value not in (-1, 1) for value in signs):
        raise ValueError("literal_observer_sign_word_required")
    plus = sum(signs)
    minus = sum((-1)**j*value for j, value in enumerate(signs))
    low = rotation(AF, plus)
    high = (s.diag(1, -1) if len(signs) % 2 else s.eye(2))*rotation(AF, minus)
    lp, lm = AF.red(low[1, 0]**2), AF.red(high[1, 0]**2)
    return {"ordinary_charge": plus, "alternating_charge": minus,
            "operator4": s.diag(low, high), "lambda_plus": lp, "lambda_minus": lm}


def canonical_car_state(AF, tick: int):
    """Closed formula on the ACTUAL activated trace orbit, not a reset.

    Tick0 is AFTER the initial AF.activate.  Beyond tick3 the first pair
    alternates while the grade3/4 archive keeps its full golden rotations.
    """
    if type(tick) is not int or tick < 0:
        raise ValueError("nonnegative_exact_tick_for_formula_only")
    e = s.Matrix([1, 0])
    if tick < 3:
        low = AF.p*rotation(AF, tick+1)*e
        high = (s.diag(1, -1)*rotation(AF, 1))**tick*s.Matrix([AF.a*AF.p, -AF.p**2])
    else:
        r, odd = divmod(tick-3, 2)
        low = AF.p*rotation(AF, 4+odd)*e
        high = AF.p*(s.diag(1, -1) if odd else s.eye(2))*rotation(AF, 2*r+odd)*e
    out = s.zeros(16, 1)
    out[0], out[1], out[14], out[15] = tuple(low)+tuple(high)
    return AF.mat(out)


def _engine_state(role, vector):
    """Exact same Z[a] storage used by the literal engine, all64 integers."""
    values = []
    for value in vector:
        poly = s.Poly(role.AF.red(value).subs(role.p, role.a**2), role.a)
        require(poly.degree() <= 3 or poly.is_zero, "canonical_engine_field_basis")
        coefficients = tuple(poly.nth(j) for j in range(4))
        require(all(item.is_Integer is True for item in coefficients), "exact_integer_engine_coefficients")
        values.append(role.E.Golden(tuple(int(item) for item in coefficients)))
    return role.E.State(tuple(values))


def _right_action(AF, old_type: int, row: int, column: int):
    frame = AF.frame(1)
    blocks = []
    for v, dimension in enumerate(frame["fine_sizes"]):
        A = s.zeros(dimension)
        for j, _path, offset in frame["segments"][v]:
            if j == old_type:
                A[offset+row, offset+column] = 1
        blocks.append(s.kronecker_product(s.eye(dimension), A.T))
    return s.diag(*blocks)


def _operator_factors(AF, vector):
    """Literal right-label extraction of the COMPLETE A7 density factors."""
    frame = AF.frame(1)
    sizes = frame["fine_sizes"]
    starts = (0, sizes[0]**2)
    answer = []
    for j, info in enumerate(AF.right_frames(1)):
        factor = s.zeros(info["dimension"], info["spectator_dimension"])
        for row, (v, k, old_row) in enumerate(info["labels"]):
            kind, _path, offset = frame["segments"][v][k]
            require(kind == j, "literal_old_right_label_type")
            for c in range(info["spectator_dimension"]):
                factor[row, c] = vector[starts[v]+old_row*sizes[v]+offset+c]
        answer.append(factor)
    return tuple(answer)


def run(repo: Path | None = None) -> dict:
    repo = ROOT if repo is None else Path(repo).resolve()
    role = owners(repo)
    AF, C, engine = role.AF, role.C, role.E
    checks = []
    def eq(actual, expected, label):
        difference = actual-expected
        entries = list(difference) if isinstance(difference, s.MatrixBase) else [difference]
        require(all(C.red(value) == 0 for value in entries), label)
        checks.append(label)
    def yes(condition, label):
        require(condition, label)
        checks.append(label)

    # This selected owner function checks its explicit gate/price/blank weld;
    # role.build_result(), old controls() and old entrypoints are NOT called.
    Psi, Wp, Bcar, Up, V, _Vm2, d = role.af_embedding(checks)
    _W, Paf, Baf, carrier = AF.full_operators(V, d)
    Pcar = s.diag(*(int(mask % 2 == 0) for mask in range(16)))
    Dcar, Daf = 2*Pcar-s.eye(16), 2*Paf-s.eye(89)
    Wm = AF.mat(Daf*Wp*Daf)
    Um = role.engine_gate_matrix(-1)
    eq(Up, role.engine_gate_matrix(1), "literal_engine_positive_gate_all16")
    eq(Um, Dcar*Up*Dcar, "literal_engine_negative_gate_all16_price_conjugacy")
    eq(Paf*Psi, Psi*Pcar, "actual_price_cut_is_time_occupation_complement")
    eq(Daf*Psi, Psi*Dcar, "same_owned_price_reflection_intertwines_all16")
    eq(Wm*Psi, Psi*Um, "adaptive_negative_AF_branch_intertwines_literal_engine_all16")
    eq(Daf.T*Daf, s.eye(89), "whole_AF_price_reflection_involution")
    eq(Wm.T*Wm, s.eye(89), "adaptive_AF_negative_branch_unitary_all89")
    eq(Daf*Baf, Baf*Daf, "retained_AF_blank_cut_is_not_reset")
    eq(Dcar*Bcar, Bcar*Dcar, "retained_full_CAR_blank_cut_is_unchanged")
    eq((s.eye(89)-carrier)*Wm, s.eye(89)-carrier, "all69_complement_modes_stay_identity")
    yes(V.shape == (89, 20) and d == 5, "full16_plus_scalar4_plus_complement69_retained")
    D4 = s.diag(1, 1, -1, -1)
    eq(V.H*Wm*V, s.kronecker_product(D4*AF.record()*D4, s.eye(5)),
       "negative_branch_keeps_complete_scalar_channel")
    for j, size in enumerate(AF.counts(1)):
        for row in range(size):
            for column in range(size):
                right = _right_action(AF, j, row, column)
                eq(Wp*right, right*Wp, "positive_branch_actual_old_right_"+str((j, row, column)))
                eq(Wm*right, right*Wm, "negative_branch_actual_old_right_"+str((j, row, column)))

    canonical = s.Matrix([AF.p, 0, 0, AF.p, AF.a*AF.p])
    x0 = AF.mat(Wp*V[:, :d]*canonical)
    m0 = C.mat(Psi.H*x0)
    eq(m0, canonical_car_state(AF, 0), "actual_whole_AF_activation_gives_canonical_engine_seed")
    eq(m0.T*m0, s.Matrix([[2*AF.p**2]]), "CAR_component_norm_without_discarding_scalar_mass")
    y_values = [AF.p**2, 2*AF.a*AF.p**2, 9*AF.p-5,
                4*AF.a*AF.p**5, 45-73*AF.p]
    signs = [1, 1, 1, 1, -1]
    for tick, (value, sign) in enumerate(zip(y_values, signs)):
        eq(canonical_car_state(AF, tick)[1], value, "canonical_exact_pairing_"+str(tick))
        yes(_engine_state(role, canonical_car_state(AF, tick)).matter[1].sign() == sign,
            "canonical_strict_engine_sign_"+str(tick))
    eq(Up**3*m0, canonical_car_state(AF, 3), "infinite_formula_base_from_actual_initial_seed")
    L3, L4 = (canonical_car_state(AF, k)[:2, :] for k in (3, 4))
    eq(rotation(AF, 1)*L3, L4, "positive_low_pair_transition_forever")
    eq(rotation(AF, -1)*L4, L3, "negative_low_pair_transition_forever")
    eq(C.mat(Um*canonical_car_state(AF, 4)), canonical_car_state(AF, 5),
       "fifth_transition_uses_negative_gate_not_fixed_AF_positive")
    actual_fifth = engine.step(_engine_state(role, canonical_car_state(AF, 4)))
    eq(role.engine_vector(actual_fifth), canonical_car_state(AF, 5),
       "actual_engine_selector_matches_adaptive_fifth_step")
    yes(not role.zero(Up*canonical_car_state(AF, 4)-canonical_car_state(AF, 5)),
        "old_fifth_fixed_gate_mismatch_is_not_erased")
    eq(canonical_car_state(AF, 1)[15], 0, "instantaneous_top_orientation_can_vanish")
    eq(canonical_car_state(AF, 1)[14], AF.p, "orientation_information_retained_in_grade3")
    eq(C.current(s.eye(4), canonical_car_state(AF, 4)), s.Matrix([1, 0, 0, 0]),
       "correlated_current_cannot_replace_engine_first_grade_sign")
    guard = s.diag(*(int(mask in (2, 3, 4, 5, 8, 9)) for mask in range(16)))
    for sign, gate in ((1, Up), (-1, Um)):
        eq(guard*gate*(s.eye(16)-guard), s.zeros(16), "six_guard_equations_invariant_"+str(sign))

    # Generic one-step induction proves every word, not an orbit census.
    cc, ss = s.symbols("rotation_cos rotation_sin", real=True)
    Rq, Z = s.Matrix([[cc, -ss], [ss, cc]]), s.diag(1, -1)
    for sign in (-1, 1):
        Rs = rotation(AF, sign)
        new_low = s.Matrix([[AF.a*cc-sign*AF.p*ss, -AF.a*ss-sign*AF.p*cc],
                           [AF.a*ss+sign*AF.p*cc, AF.a*cc-sign*AF.p*ss]])
        eq(Rs*Rq, new_low, "arbitrary_rotation_low_induction_"+str(sign))
        for parity in (0, 1):
            effective = (-1)**parity*sign
            next_rotation = s.Matrix([[AF.a*cc-effective*AF.p*ss, -AF.a*ss-effective*AF.p*cc],
                                     [AF.a*ss+effective*AF.p*cc, AF.a*cc-effective*AF.p*ss]])
            eq(Z*Rs*(Z if parity else s.eye(2))*Rq,
               (Z if not parity else s.eye(2))*next_rotation,
               "arbitrary_rotation_high_induction_"+str((sign, parity)))
    eq(Z*rotation(AF, -1)*Z, rotation(AF, 1), "all_future_high_archive_even_step_identity")
    eq(Z*rotation(AF, 1)*Rq,
       Z*s.Matrix([[AF.a*cc-AF.p*ss, -AF.a*ss-AF.p*cc],
                   [AF.a*ss+AF.p*cc, AF.a*cc-AF.p*ss]]),
       "all_future_high_archive_odd_step_identity")

    T = s.Matrix([[1, 0, 1, 0], [1, 0, -1, 0],
                  [0, 1, 0, 1], [0, 1, 0, -1]])/s.sqrt(2)
    PC = s.diag(1, 0, 1, 0)
    bases = {sign: AF.mat(T.T*(AF.record() if sign == 1 else D4*AF.record()*D4)*T)
             for sign in (-1, 1)}
    for sign in (-1, 1):
        eq(bases[sign], word_data(AF, (sign,))["operator4"], "literal_two_channel_decomposition_"+str(sign))
    for word in ((1, 1), (1, -1), (-1, 1), (-1, -1), (1, 1, -1, -1, 1)):
        data = word_data(AF, word)
        literal = s.eye(4)
        for sign in word:
            literal = AF.mat(bases[sign]*literal)
        eq(literal, data["operator4"], "closed_all_word_operator_control_"+str(word))
        feedback = AF.mat(PC*literal.T*(s.eye(4)-PC)*literal*PC)
        eq(feedback, s.diag(data["lambda_plus"], 0, data["lambda_minus"], 0),
           "closed_all_word_feedback_control_"+str(word))
    for word in ((1, 1), (1, -1)):
        data = word_data(AF, word)
        eq(data["lambda_plus"]+data["lambda_minus"], 4*AF.p**3,
           "two_ticks_switch_projector_not_feedback_price_"+str(word))
        eq(data["lambda_plus"]*data["lambda_minus"], 0,
           "two_ticks_only_one_active_feedback_channel_"+str(word))
    low4, high4 = s.diag(1, 0, 0, 0), s.diag(0, 0, 1, 0)
    car_basis = role.F.record_basis()
    car_low = car_basis*s.kronecker_product(low4, s.eye(4))*car_basis.T
    car_high = car_basis*s.kronecker_product(high4, s.eye(4))*car_basis.T
    af_low = V*s.kronecker_product(T*low4*T.T, s.eye(5))*V.H
    af_high = V*s.kronecker_product(T*high4*T.T, s.eye(5))*V.H
    for projectors, multiplicity, label in (((car_low, car_high), 4, "CAR"),
                                           ((af_low, af_high), 5, "AF")):
        left, right = projectors
        eq(left*left, left, "feedback_low_projection_"+label)
        eq(right*right, right, "feedback_high_projection_"+label)
        eq(left*right, s.zeros(left.rows), "feedback_channels_orthogonal_"+label)
        eq(s.trace(left), multiplicity, "complete_feedback_low_multiplicity_"+label)
        eq(s.trace(right), multiplicity, "complete_feedback_high_multiplicity_"+label)
    eq(af_low+af_high, Paf, "all_other79_AF_feedback_modes_retained_zero")
    for second_sign, target in ((1, af_low), (-1, af_high)):
        word = AF.mat((Wp if second_sign == 1 else Wm)*Wp)
        feedback = AF.mat(Paf*word.T*(s.eye(89)-Paf)*word*Paf)
        eq(feedback, 4*AF.p**3*target, "actual_all89_two_tick_feedback_"+str(second_sign))

    # These are COMPLETE A7 operator factors, not the smaller A4 left state.
    factors = _operator_factors(AF, x0)
    for j, factor in enumerate(factors):
        eq(factor.H*factor, AF.p**(2+j)*s.eye(AF.counts(1)[j]),
           "canonical_complete_A7_Schmidt_spectrum_"+str(j))
        eq(AF.p**(8+j), AF.p**6*AF.p**(2+j), "same_H4_reference_six_level_shift_"+str(j))
    gain = sum(AF.counts(1)[j]*AF.p**(2+j)*(2+j) for j in range(2))
    cost = sum(AF.counts(1)[j]*AF.p**(2+j)*(8+j) for j in range(2))
    eq(gain, 2+AF.p**3, "complete_A7_entropy_every_retained_word")
    eq(cost, 8+AF.p**3, "complete_A7_central_cost_every_retained_word")
    eq(cost-gain, 6, "complete_A7_old_price_not_repeated_fresh_activation")
    return {"exact_checks": len(checks), "checks": tuple(checks), "source_pins": PINS,
            "full_CAR_components": 16, "AF_scalar_components": 4,
            "identity_complement": 69, "working_GNS_dimension": 89,
            "canonical_infinite_orbit": "analytic recurrence; exact signs +,+,+,+,- then alternating",
            "all_word_formula": "sin²(theta sum s), sin²(theta alternating sum s)",
            "cos_theta": "a", "sin_theta": "p", "new_phase_parameter": False,
            "CAR_feedback_multiplicity_each": 4, "whole_AF_feedback_multiplicity_each": 5,
            "complete_A7_old_price_every_canonical_word": "6",
            "complete_A7_gain_every_canonical_word": "2+p³",
            "complete_A7_central_cost_every_canonical_word": "8+p³",
            "selector": "sign of actual first-grade m1, not correlated current",
            "branch_old_right_equivariance": True,
            "nonlinear_selector_equivariance_claimed": False,
            "fixed_finite_bit_capacity_or_physical_clock_derived": False,
            "repeated_fresh_AF_activation_claimed": False,
            "noncollinear_or_moving_pairing_transition_derived": False,
            "physical_admission_or_full_native_action_derived": False}
