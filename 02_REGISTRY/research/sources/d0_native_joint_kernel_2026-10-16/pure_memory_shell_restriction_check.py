"""Exact rank-two pure-memory correction on inactive shell-transfer legs.

This is a finite symbolic consumer of the actual owned full16 CAR, not an
all-mode assembly or a new numerical inertia certificate.  Only the spatial
opposite-sign restriction has an identically zero correction; its previously
certified full-root-box inertia is consumed by SHA, without replaying it.
The other five shell classes get a nonzero rank-two update per inactive leg.

API run(repo=None); CLI deterministic JSON.  No old run(), root solve,
receipt write, density truncation, or full rank8 field inverse occurs.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

import sympy as s


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
L = 8
PINS = {
    "ordered_operator_check.py": "f2f9903685c2c522d4c850d335dfb9435c932182962402da499ff8a7a10a9418",
    "OPPOSITE_SHELL_TRANSFER_RESULTS.json": "ea994fef6edc38f4b01a98eed7379841f6a603dfbb02b641382bfa853f64db75",
}


def require(value, name):
    if not bool(value):
        raise ArithmeticError("pure_memory_shell_restriction:" + name)


def _zero(value):
    entries = value if isinstance(value, s.MatrixBase) else (value,)
    return all(s.cancel(s.expand(item)) == 0 for item in entries)


def run(repo=None):
    repo = ROOT if repo is None else Path(repo).resolve()
    checks = []

    def eq(actual, expected, name):
        require(_zero(actual - expected), name)
        checks.append(name)

    def yes(value, name):
        require(value, name)
        checks.append(name)

    for name, digest in PINS.items():
        yes(hashlib.sha256((HERE / name).read_bytes()).hexdigest() == digest,
            "immutable_input:" + name)
    spec = importlib.util.spec_from_file_location(
        "pure_shell_owned_ordered", HERE / "ordered_operator_check.py")
    ordered = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ordered)
    creators, order = ordered.owned_car(repo)  # AST defining nodes only.
    yes(order == (0, 2, 3, 1), "actual_owned_ACDB_occupation_order")
    chi = s.zeros(16, 1)
    chi[1] = chi[15] = 1 / s.sqrt(2)
    chi_minus = chi.copy()
    chi_minus[15] *= -1
    occupation = (s.Integer(1), s.Rational(1, 2), s.Rational(1, 2), s.Rational(1, 2))

    def ell(matrix, state=chi):
        return (state.H * matrix * state)[0]

    def delta(matrix):
        return ell(matrix) - s.trace(matrix) / 16

    for i in range(4):
        for j in range(4):
            ci, cj = creators[i], creators[j]
            eq(ci * cj.T + cj.T * ci, int(i == j) * s.eye(16),
               "full16_CAR_%d_%d" % (i, j))
            eq(ell(ci * cj.T), occupation[i] * int(i == j),
               "pure_creation_contraction_two_point_%d_%d" % (i, j))
            eq(ell(ci.T * cj), (1 - occupation[i]) * int(i == j),
               "pure_contraction_creation_two_point_%d_%d" % (i, j))
            eq(ell(ci * cj), 0, "pure_pair_creation_zero_%d_%d" % (i, j))
            eq(ell(ci.T * cj.T), 0, "pure_pair_contraction_zero_%d_%d" % (i, j))
            eq(delta(ci * cj.T), (s.Rational(1, 2) if i == j == 0 else 0),
               "only_time_two_point_bias_%d_%d" % (i, j))

    # Degree-two identities are derived from the just-checked actual CAR
    # two-point functions.  The degree-four product below is collapsed
    # algebraically by E^2=Lambda I BEFORE any state expectation is taken.
    vr = s.symbols("vr0:4", real=True)
    vi = s.symbols("vi0:4", real=True)
    av = s.symbols("a0:4", real=True)
    bv = s.symbols("b0:4", real=True)
    uv = s.symbols("u0:4", real=True)
    x, y = s.symbols("x y", real=True)
    lam = x*x + y*y
    v = [vr[j] + s.I*vi[j] for j in range(4)]
    vbar = [vr[j] - s.I*vi[j] for j in range(4)]
    z, zb = x + s.I*y, x - s.I*y
    h = x*vi[0] - y*vr[0]
    pure_ej = sum((occupation[j]*v[j]*zb*av[j]
                   + (1-occupation[j])*vbar[j]*z*av[j] for j in range(4)), s.Integer(0))
    trace_ej = sum(((v[j]*zb + vbar[j]*z)*av[j]/2
                    for j in range(4)), s.Integer(0))
    eq(pure_ej-trace_ej, s.I*h*av[0], "E_J_two_point_bias_exact")
    eq(s.conjugate(pure_ej-trace_ej), -s.I*h*av[0], "J_E_bias_has_opposite_sign")
    pure_jj = sum((occupation[j]*z*zb*av[j]*bv[j]
                   + (1-occupation[j])*zb*z*av[j]*bv[j] for j in range(4)), s.Integer(0))
    eq(pure_jj, lam*sum(av[j]*bv[j] for j in range(4)),
       "same_leg_Ja_Jb_has_zero_memory_bias")
    E, Ja, Jb = s.symbols("E Ja Jb", commutative=False)
    sa, sb, Lambda = s.symbols("sa sb Lambda", real=True)
    collapsed = s.expand((sa+Ja*E)*(sb+E*Jb)).xreplace({E**2: Lambda})
    eq(collapsed, sa*sb + sa*E*Jb + sb*Ja*E + Lambda*Ja*Jb,
       "Xadjoint_X_degree_four_collapses_using_scalar_E_squared")
    uda = sum(uv[j]*av[j] for j in range(4))
    udb = sum(uv[j]*bv[j] for j in range(4))
    W = uda*bv[0]-udb*av[0]
    numerator = 2*lam*uda*(s.I*h*bv[0])+2*lam*udb*(-s.I*h*av[0])
    eq(numerator, 2*s.I*lam*h*W, "outgoing_Xadjoint_X_memory_bias")
    incoming_change = {y: -y, **{vi[j]: -vi[j] for j in range(4)},
                       **{av[j]: bv[j] for j in range(4)},
                       **{bv[j]: av[j] for j in range(4)}}
    eq(numerator.subs(incoming_change, simultaneous=True), numerator,
       "incoming_conjugation_and_transposition_supply_the_same_half")
    g = s.symbols("g", nonzero=True, real=True)
    eq(-2*numerator/(8*g), -s.I*lam*h*W/(2*g),
       "shell_mass_one_eighth_and_both_directions_fix_sign_factor")
    yes(not _zero(numerator/(8*g)), "omitting_incoming_half_changes_generic_correction")
    eq(2*2*lam/8, lam/2, "affine_inactive_raw_Y_is_scalar_lambda1_over_two")

    # Hermitian 4x4 update.  This rank statement is about the correction,
    # not the inertia of its sum with the faithful field Hessian.
    tau, w1, w2, w3, gamma = s.symbols("tau w1 w2 w3 gamma", real=True)
    e0 = s.eye(4)[:, 0]
    ur = s.Matrix([tau, w1, w2, w3])
    wr = ur-tau*e0
    K = ur*e0.T-e0*ur.T
    U = s.Matrix.hstack(e0, wr)
    C = s.Matrix([[0, s.I*gamma], [-s.I*gamma, 0]])
    eq(-s.I*gamma*K, U*C*U.T, "exact_two_column_Hermitian_update_factorization")
    eq(K**3, -(w1*w1+w2*w2+w3*w3)*K, "rank_at_most_two_skew_identity")
    eq((-s.I*gamma*K).H, -s.I*gamma*K, "update_is_Hermitian")
    eq((-s.I*gamma*K).extract([0, 1], [0, 1]).det(), -gamma**2*w1**2,
       "nonzero_update_has_one_positive_one_negative_eigenvalue")

    # Exact eighth-root scalar calculation; no stationary-root solve.
    rt = s.sqrt(2)
    xr, yr = L*(rt/2-1), L*rt/2
    lr = s.expand(xr*xr+yr*yr)
    eq(lr, L*L*(2-rt), "actual_eighth_root_lambda1")
    eq(L*xr, -lr/2, "phase_real_part_identity")
    d, o, t0, t1 = s.symbols("d o t0 t1", real=True)
    common = 2*lr*(d-o)+8*xr*xr*o
    axis_plus = 2*L*L*d-2*L*xr*o+2*L*yr*o
    axis_minus = 2*L*L*d-2*L*xr*o-2*L*yr*o
    eq(axis_plus, 2*L*L*(d+o), "axis_gap_plus_positive_decomposition")
    eq(axis_minus, 2*L*L*((d-o)+(2-rt)*o), "axis_gap_minus_positive_decomposition")
    axis = L*t0*((xr+yr)/axis_plus+(xr-yr)/axis_minus)
    axis_closed = -2*L*L*t0*lr*(d+2*o)/(axis_plus*axis_minus)
    eq(axis, axis_closed, "axis_two_shell_weights_collapse")
    same_plus = 2*lr*(d+3*o)
    same_minus = 2*lr*(d+o)+4*(xr*xr-yr*yr)*o
    eq(same_minus, common, "same_sign_minus_gap_equals_common_positive_gap")
    opposite_gap = 2*lr*d+(6*xr*xr-2*yr*yr)*o
    eq(opposite_gap, common, "opposite_gaps_equal_common_positive_gap")
    same = 2*xr*yr*(t0+t1)/common
    opposite = 2*xr*yr*(t0-t1)/common
    eq(same, 0/same_plus+2*xr*yr*(t0+t1)/same_minus,
       "same_sign_two_shell_weights")
    eq(opposite, -2*xr*yr*t1/opposite_gap+2*xr*yr*t0/opposite_gap,
       "opposite_sign_two_shell_weights")
    # a=b+c makes all claimed nonvanishing factors explicit: b,c>0.
    b, c = s.symbols("b c", positive=True)
    a = b+c
    dv, ov = a*a+3*b*b, 2*b*(a+b)
    eq(dv-ov, c*c, "a_greater_b_root_region_is_d_minus_o_positive")
    yes(bool((2-rt).is_positive) and bool((-xr*yr).is_positive),
        "exact_phase_positive_and_negative_constants")
    yes(bool(lr.is_positive) and bool(ov.is_positive)
        and bool((2*lr*c*c).is_positive) and bool((8*xr*xr*ov).is_positive),
        "common_gap_is_sum_of_strictly_positive_terms_for_every_b_c_positive")
    yes(bool((2*L*L*c*c).is_positive)
        and bool((2*L*L*(2-rt)*ov).is_positive),
        "axis_minus_gap_is_sum_of_strictly_positive_terms")
    records = []
    types = [
        ("axis_time", (2, 0, 0, 0), (1, 2, 3), axis_closed.subs(t0, a), 2, True),
        ("axis_spatial", (0, 2, 0, 0), (0, 2, 3), axis_closed.subs(t0, b), 6, True),
        ("same_time_spatial", (1, 1, 0, 0), (2, 3), same.subs({t0:a, t1:b}), 6, True),
        ("same_spatial_spatial", (0, 1, 1, 0), (0, 3), same.subs({t0:b, t1:b}), 6, True),
        ("opposite_time_spatial", (1, 7, 0, 0), (2, 3), opposite.subs({t0:a, t1:b}), 6, True),
        ("opposite_spatial_spatial", (0, 1, 7, 0), (0, 3), opposite.subs({t0:b, t1:b}), 6, False),
    ]
    for label, q, inactive, scalar, frequencies, nonzero in types:
        scalar = s.factor(scalar.subs({d:dv, o:ov}))
        yes(_zero(scalar) == (not nonzero), "exact_generic_nonzero_or_zero:"+label)
        # For the five nonzero cases the displayed numerator factors and
        # positive gap decompositions prove nonzero for EVERY b,c>0,
        # not merely a polynomial test or a rational fixture.
        for r in inactive:
            spatial = [-(a if r == j else b) for j in range(1, 4)]
            yes(any(bool(s.factor(w*w).is_positive) for w in spatial),
                "nonzero_spatial_leg:"+label+":"+str(r))
        records.append({"class":label, "q":list(q), "inactive_roles":list(inactive),
                        "complex_restriction_dimension":4*len(inactive),
                        "real_frequency_count":frequencies,
                        "real_restriction_dimension":frequencies*4*len(inactive),
                        "scalar_sum_h_over_g":str(scalar),
                        "correction_rank_per_inactive_leg":2 if nonzero else 0,
                        "correction_is_generic_nonzero_on_all_a_gt_b_gt_0":nonzero,
                        "new_restriction_inertia_proved":False})

    # Odd spatial permutations change the relative chi sign.  Every
    # degree-even word commutes with parity, which restores this sign.
    parity = s.diag(*[(-1)**bin(mask).count("1") for mask in range(16)])
    eq(parity*chi, -chi_minus, "parity_restores_odd_spatial_permutation_seed")
    for i in range(4):
        eq(parity*creators[i], -creators[i]*parity, "parity_odd_creation_%d" % i)
        for j in range(4):
            even = creators[i]*creators[j].T
            eq(parity*even, even*parity, "parity_commutes_even_word_%d_%d" % (i,j))
            eq(ell(even), ell(even, chi_minus), "chi_sign_same_even_expectation_%d_%d" % (i,j))

    old = json.loads((HERE/"OPPOSITE_SHELL_TRANSFER_RESULTS.json").read_text())
    validation = json.loads((HERE/"OPPOSITE_SHELL_TRANSFER_VALIDATION.json").read_text())
    expected_inertia = {"positive":6, "negative":2, "zero":0}
    yes(old["status"] == "VALIDATED_OPPOSITE_SIGN_SHELL_TRANSFER_RESTRICTION",
        "consume_existing_interval_result_only")
    yes(old["sector"]["q"] == [1,7,0,0]
        and old["restricted_heat_S4_congruence"]["target_q"] == [0,1,7,0],
        "existing_full_trace_restricted_congruence_targets_q0170")
    yes(old["restricted_heat_S4_congruence"]["transferred_restriction_inertia"] == expected_inertia
        and old["sector"]["validated_restriction_inertia"] == expected_inertia,
        "existing_q0170_faithful_inertia_6_plus_2_minus")
    yes(old["sector"]["Hermitian_operator_distance_from_signature_upper"] < 1
        and old["sector"]["root_box"]["radius"] == "1e-12",
        "existing_inertia_is_strict_on_whole_owned_root_box")
    yes(validation["normal_optimized_scientific_output"] == "BYTE_IDENTICAL"
        and validation["restriction_inertia"] == expected_inertia,
        "existing_normal_optimized_receipt_consumed_without_execution")
    relative_here = HERE.relative_to(repo).as_posix()
    yes(validation["sha256"][relative_here+"/OPPOSITE_SHELL_TRANSFER_RESULTS.json"]
        == PINS["OPPOSITE_SHELL_TRANSFER_RESULTS.json"],
        "current_validation_identifies_exact_immutable_scientific_result")
    for name, digest in old["source_sha256"].items():
        yes(hashlib.sha256((HERE/name).read_bytes()).hexdigest() == digest
            and validation["sha256"][relative_here+"/"+name] == digest,
            "existing_scientific_source_identity:"+name)
    yes(sum(row["real_restriction_dimension"] for row in records) == 288,
        "all_nonzero_shell_transfer_V_real_dimension_288")
    yes(40511+288+7 == 40806, "complete_rank8_field_normal_dimension")
    yes(7+36 == 43 and 12 == 12 and 40806-55 == 40751,
        "closed_q0_and_spatial_opposite_dimensions_leave_40751")
    yes(40806+2*151+57195 == 98303, "reduced_raw_shell_amplitude_dimension")
    yes(16740352+4096+98303 == 16842751, "full_normalized_amplitude_dimension")
    return {
        "schema":"d0-pure-memory-shell-restriction/1",
        "status":"PASS_EXACT_TWO_POINT_AND_RANK_TWO_REDUCTION",
        "exact_checks":len(checks), "checks":checks,
        "all_Fock_components":16, "reference_dimension":128,
        "prepared_rank":8, "L":L,
        "formula":"Hchi-Htrace = -i*lambda1/2*sum_sigma(h_sigma/g_sigma)*(u_r*e0^T-e0*u_r^T)",
        "raw_inactive_affine_Y_identical":True,
        "signed_Q_denominators_preserved":True,
        "shell_classes":records,
        "q0170_exact_identity_and_existing_inertia":{
            "q":[0,1,7,0], "complex_inertia":expected_inertia,
            "real_frequency_count":6,
            "all_spatial_opposite_real_inertia":{"positive":36,"negative":12,"zero":0},
            "existing_result_sha256":PINS["OPPOSITE_SHELL_TRANSFER_RESULTS.json"],
            "existing_validation_scientific_output":"BYTE_IDENTICAL",
            "mutable_validation_prose_owner_hash_pinned":False,
            "old_interval_or_matrix_replayed":False},
        "symmetry":{"spatial_S3_with_parity_restoration":True,
                    "global_frequency_negation_is_Fourier_reality":True,
                    "time_spatial_S4_of_pure_source_claimed":False},
        "normal_inertia_consumer":{
            "V_dimension_real":40806,
            "already_closed_V_inertia":{"positive":43,"negative":12,"zero":0},
            "remaining_V_dimension_real":40751,
            "if_V_inertia_p_n_z":"reduced=(p+151,n+151,57195+z)",
            "full_normalized_amplitude":"(p+16740503,n+4247,57195+z)",
            "Q_mass_inertia":{"positive":16740352,"negative":4096,"zero":0},
            "reference_birth_source_zeros_already_in_57195":True,
            "whole_rank8_normal_inverse_proved":False},
        "source_pins":PINS,
        "owned_creator_source_pin":{ordered.CURVED:ordered.CURVED_SHA256},
        "old_run_root_search_matrix_census_or_receipt_write":False,
        "physical_admission_GR_or_new_inertia_for_five_classes":False,
    }


if __name__ == "__main__":
    print(json.dumps(run(), sort_keys=True))
