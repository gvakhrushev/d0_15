#!/usr/bin/env python3
"""Actual level-one controlled AF preparation against the named engine guards.

The smooth optimization is on the real engine-SUPPORT extension.  The literal
engine additionally stores Z[a] coefficients and tests its input/output pairing.
Only pinned definitions are imported; no old build_result/check suite is run.
"""
from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path
import sys

import sympy as s


ROOT = Path(__file__).resolve().parents[4]
CERT = "02_REGISTRY/research/certificates/"
ROLE_PATH = CERT+"a4d_native_af_role_orbit_metric_check.py"
PRICE_PATH = "02_REGISTRY/research/sources/d0_jacobian_controlled_record_2026-10-16/controlled_record.py"
PINS = {
    ROLE_PATH: "b718a3ea3e3f47087b664cc9bb194e0e09c5ae818836efdba3e63b9c11e4f2d5",
    CERT+"a4d_native_fibonacci_record_activation.py": "9a016fa4b1a8261a29f626ed7450db7987727957e634799519aede0e3ab587ee",
    CERT+"a4d_native_fock_record_binding_check.py": "42e83e6f93b48ce4d4420f829d8e79c993a215d7b1a4c6a2f812bd45fd914078",
    CERT+"a4d_native_correlated_current_transition.py": "e659733a8ab4fea30f46de56663dc344249420c7e0a3ea65b2aa1a2091b76e0d",
    CERT+"a4d_native_closed_record_engine.py": "7aead2716c7bf7899a134eedbf4b87dbe1ef9c85900189b5afc8cdfeed13f0f9",
    CERT+"a4d_native_reference_memory_preparation.py": "67e416c75cc213efca6040cea8cb796efbcff78037e09b31fb6a83acdcfd0e3a",
    CERT+"a4d_native_record_metric_chronology_check.py": "16929d026206ee69e126484ed2ac7b1dfd2537c1e50c0fc4c4293408caf58527",
    CERT+"a4d_native_jones_record_transport.py": "b19f6c864af7e75c2a48d9892692b4d94337d06c04a83013b180148a1752c53f",
    PRICE_PATH: "dd3b7aa6f661dbef4117b2913e62136447a14e2d08a16b08b325cb688874f4ff",
}
GUARDS = (2, 3, 4, 5, 8, 9)


def require(condition: object, name: str) -> None:
    if not bool(condition):
        raise AssertionError(name)


def owners(repo: Path):
    for relative, digest in PINS.items():
        require(hashlib.sha256((repo/relative).read_bytes()).hexdigest() == digest,
                "source_pin:"+relative)
    modules = []
    for index, path in enumerate((ROLE_PATH, PRICE_PATH)):
        name = "engine_preparation_owned_definition_"+str(index)
        spec = importlib.util.spec_from_file_location(name, repo/path)
        if spec is None or spec.loader is None:
            raise RuntimeError("engine_preparation_owner_unavailable:"+path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        modules.append(module)
    return tuple(modules)


def actual_embedding(AF, fock_owner):
    """Same actual Psi as the role owner; inverse on complex states is Psi.H."""
    frame = AF.frame(1)
    V, d = frame["V"], frame["old_dimension"]
    V_m2 = V[:, [q*d+i for q in range(4) for i in range(4)]]
    chi = s.Matrix([[1, 0, 0, 1], [0, 1, -s.I, 0],
                    [0, 1, s.I, 0], [1, 0, 0, -1]])/s.sqrt(2)
    T = s.Matrix([[1, 0, 1, 0], [1, 0, -1, 0],
                  [0, 1, 0, 1], [0, 1, 0, -1]])/s.sqrt(2)
    Psi = V_m2*s.kronecker_product(T, chi)*fock_owner.record_basis().T
    return frame, Psi


def full_car_from_products(D, B):
    """All sixteen literal mask coefficients; D=R*C2, B=sqrt(E2)*C2."""
    def coordinates(M):
        return ((M[0, 0]+M[1, 1])/2, (M[0, 1]+M[1, 0])/2,
                s.I*(M[0, 1]-M[1, 0])/2, (M[0, 0]-M[1, 1])/2)
    d, b = coordinates(D), coordinates(B)
    return s.Matrix([d[0], b[0], d[1], b[1], d[2], b[2], d[3], -b[3],
                     d[3], b[3], -d[2], b[2], d[1], -b[1], d[0], -b[0]])


def support_matrix(R, B):
    """Exact complex-linear six-row K_E on (C00,C01,C10,C11,Cscalar)."""
    c = s.symbols("support_c00 support_c01 support_c10 support_c11 support_scalar")
    C = s.Matrix(2, 2, c[:4])
    return full_car_from_products(R*C, B*C)[list(GUARDS), :].jacobian(c)


def scalar_minimum(p, log_phi, conditional_f0, conditional_f1):
    """Support-compatible density minimum, retaining the AF scalar channel."""
    lam0 = 2*p**2*s.exp(-log_phi*conditional_f0)
    lam1 = p**3*s.exp(-log_phi*conditional_f1)
    Z = lam0+lam1
    return {"normalizer": Z, "M2_mass": lam0/Z, "scalar_mass": lam1/Z,
            "price": 6-s.log(Z)/log_phi,
            "raw_positive_M2_amplitude": s.eye(2),
            "raw_scalar_amplitude": s.sqrt(p*s.exp(log_phi*(conditional_f0-conditional_f1)))}


def scalar_source(x, dx, log_phi, conditional_f0, conditional_f1,
                  f0_prime, f1_prime, de, df, p):
    """Full scalar-stratum price source, including the preparation/normalizer."""
    return (s.log(x*p/((1-x)*2))/log_phi+conditional_f0-conditional_f1)*dx \
        +x*f0_prime*de+(1-x)*f1_prime*df


def run(repo: Path | None = None) -> dict:
    repo = ROOT if repo is None else Path(repo).resolve()
    role, price = owners(repo)
    AF, current, engine = role.AF, role.C, role.E
    checks = []

    def zero(expr):
        return AF.red(s.fraction(s.cancel(s.together(expr)))[0]) == 0

    def eq(actual, expected, name):
        difference = actual-expected
        require(all(zero(v) for v in difference) if isinstance(difference, s.MatrixBase)
                else zero(difference), name)
        checks.append(name)

    frame, Psi = actual_embedding(AF, role.F)
    V, d = frame["V"], frame["old_dimension"]
    eq(Psi.H*Psi, s.eye(16), "actual_full16_complex_AF_CAR_isometry")
    require(V.shape == (89, 20) and 16-len(GUARDS) == 10,
            "whole89_space_and_ten_allowed_real_slots")
    checks.append("whole89_space_and_ten_allowed_real_slots")
    entries = s.symbols("r00 r01 r10 r11 b00 b01 b10 b11 c00 c01 c10 c11 cs")
    R, B, C = (s.Matrix(2, 2, entries[start:start+4]) for start in (0, 4, 8))
    raw0, raw3 = s.Matrix(list(R*C)+[entries[12]]), s.Matrix(list(B*C)+[entries[12]])
    literal = Psi.H*(V[:, :d]*raw0+V[:, 3*d:]*raw3)
    closed = full_car_from_products(R*C, B*C)
    eq(literal, closed, "all16_controlled_output_from_literal_AF_frame")
    K = support_matrix(R, B)
    eq(K, literal[list(GUARDS), :].jacobian(entries[8:]),
       "six_actual_guard_rows_are_exact_moving_K_E")
    eq(K[:, 4], s.zeros(6, 1), "full_AF_scalar_retained_CAR_invisible")
    r, b, c, z, r1, b1 = s.symbols("r b c z r1 b1", positive=True)
    Ks = support_matrix(r*s.eye(2), b*s.eye(2))
    basis = s.Matrix.hstack(s.Matrix([1, 0, 0, 1, 0]), s.Matrix([0, 0, 0, 0, 1]))
    eq(Ks*basis, s.zeros(6, 2), "scalar_effect_trace_plus_scalar_kernel")
    require(Ks.rank() == 3, "scalar_effect_guard_rank_three")
    checks.append("scalar_effect_guard_rank_three")

    # Supplied exact positive roots of the actual non-scalar fixture effect.
    rn, bn = s.diag(s.Rational(4, 5), s.Rational(3, 5)), s.diag(s.Rational(3, 5), s.Rational(4, 5))
    eq(rn*rn+bn*bn, s.eye(2), "nonscalar_positive_roots_unitary_control")
    Kn = support_matrix(rn, bn)
    require(Kn.rank() == 4 and Kn.nullspace() == [s.Matrix([0, 0, 0, 0, 1])],
            "nonscalar_effect_actual_visible_kernel_zero")
    checks.append("nonscalar_effect_actual_visible_kernel_zero")
    # Freezing the gold kernel or dropping sqrt(E)*C guards gives wrong inputs.
    trace = basis[:, 0]
    eq(Ks*trace, s.zeros(6, 1), "gold_frozen_kernel_would_accept_trace")
    require(Kn*trace != s.zeros(6, 1), "hostile_frozen_gold_constraint_rejected")
    checks.append("hostile_frozen_gold_constraint_rejected")
    failure_only = full_car_from_products(rn*rn.inv(), bn*rn.inv())
    eq(failure_only[[2, 4, 8], :], s.zeros(3, 1), "success_only_constraint_would_accept_inverse_root")
    require(failure_only[list(GUARDS), :] != s.zeros(6, 1),
            "hostile_missing_failure_guard_rejected")
    checks.append("hostile_missing_failure_guard_rejected")

    # The moving-kernel compatibility equation excludes all traceless dE.
    u, v, w = s.symbols("dEdiag dEreal dEimag", real=True)
    traceless = s.Matrix([[u, v+s.I*w], [v-s.I*w, -u]])
    # Solving the R*C guard requires dC_tr=c*dE_tr/(2r^2).
    dC = c*traceless/(2*r*r)
    dD = r*dC-c*traceless/(2*r)
    dF = b*dC+c*traceless/(2*b)
    eq(dD, s.zeros(2), "moving_kernel_success_tangent_solved")
    eq(dF, c*(r*r+b*b)*traceless/(2*b*r*r),
       "moving_kernel_failure_tangent_forces_dE_traceless_zero")

    complete_raw = V[:, :d]*s.Matrix([r*c, 0, 0, r*c, r1*z]) \
        +V[:, 3*d:]*s.Matrix([b*c, 0, 0, b*c, b1*z])
    norm = s.expand((complete_raw.H*complete_raw)[0]).subs({b**2: 1-r**2, b1**2: 1-r1**2})
    eq(norm, 2*c*c+z*z, "complete_AF_normalizer_keeps_scalar_mass")
    trace_car = full_car_from_products(r*c*s.eye(2), b*c*s.eye(2))
    eq(Psi.H*complete_raw, trace_car, "retained_scalar_does_not_cancel_CAR_guards")
    eq((trace_car.H*trace_car)[0], 2*c*c*(r*r+b*b), "CAR_normalizer_distinct_from_full_AF_normalizer")
    eq(current.current(s.eye(4), trace_car), s.Matrix([1, 0, 0, 0]),
       "full_owned_current_has_no_spatial_component_on_scalar_branch")
    eq(current.observer_pairing(s.diag(1, -1, -1, -1), s.Matrix([1, 0, 0, 0])), s.eye(4),
       "native_observer_pairing_fixed_on_scalar_branch")

    # Literal ring-engine acceptance is checked only at actual golden points.
    pos = [engine.ZERO]*16
    pos[0] = pos[14] = engine.A
    pos[1], pos[15] = engine.P, -engine.P
    state = engine.State(tuple(pos))
    after = engine.step(state)
    require(after.matter[1] == 2*engine.A*engine.P and after.matter[1].sign() == 1,
            "positive_golden_trace_is_literal_engine_accepted")
    checks.append("positive_golden_trace_is_literal_engine_accepted")
    eq(role.engine_vector(state), trace_car.subs({c: 1, r: AF.a, b: AF.p}),
       "accepted_ring_state_is_actual_AF_CAR_projection")
    try:
        engine.step(engine.State(tuple(-value for value in pos)))
    except ValueError as exc:
        require(str(exc) == "OUTPUT_FIRST_GRADE_PAIRING_SINGULARITY",
                "negative_golden_trace_has_expected_pairing_failure")
    else:
        raise AssertionError("negative_golden_trace_must_halt")
    checks.append("negative_golden_trace_halts_not_an_engine_phase_gauge")

    ell = s.Symbol("log_phi", positive=True)
    e = s.Symbol("scalar_effect", positive=True)
    for j in (0, 1):
        fine = price.conditional_probabilities(AF, j, e)
        eq(sum(fine[0]+fine[1]), 1, "owned_all_path_probability_normalization_"+str(j))
        kl = sum(q*(s.log(q)+(3+v-j)*ell) for v in (0, 1) for q in fine[v])/ell
        eq(price.conditional_old_price(AF, j, e, ell), kl, "owned_conditional_price_is_actual_KL_"+str(j))
    eq(2*AF.p**2+AF.p**3, 1, "complete_old_PF_mass")
    x, lam0, lam1 = s.symbols("x lambda0 lambda1", positive=True)
    Z = lam0+lam1
    optimum_x = lam0/Z
    action = 6+(x*s.log(x/lam0)+(1-x)*s.log((1-x)/lam1))/ell
    gap = (x*s.log(x/optimum_x)+(1-x)*s.log((1-x)/(1-optimum_x)))/ell
    eq(1-optimum_x, lam1/Z, "normalized_complement_probability_exact")
    # Normalize this positive rational probability BEFORE expanding logs.
    # Otherwise SymPy retains log(1-lambda0/Z) as an opaque atom.
    normalized_complement = {1-optimum_x: lam1/Z}
    gap = gap.xreplace(normalized_complement)
    # The declared domain is 0<x<1 and lambda_i>0.
    eq(s.expand_log(action-(6-s.log(Z)/ell)-gap, force=True), 0,
       "exact_scalar_Bernoulli_gap_one_global_normalizer")
    stationary = s.diff(action, x).subs(x, optimum_x).xreplace(normalized_complement)
    eq(s.expand_log(stationary, force=True), 0, "true_kernel_preparation_stationary_mass")
    eq(s.diff(action, x, 2), 1/(ell*x*(1-x)), "true_kernel_preparation_strictly_convex_mass")
    dc, dz = s.symbols("dc dz", real=True)
    tau = 2*c*c+z*z
    mass = 2*c*c/tau
    dtau = 4*c*dc+2*z*dz
    dx = s.diff(mass, c)*dc+s.diff(mass, z)*dz
    eq(dx, (4*c*dc*tau-2*c*c*dtau)/tau**2, "moving_full_normalizer_in_mass_source")
    eq(dx.subs({dc: c, dz: z}), 0, "raw_radial_preparation_source_cancels")
    eq((4*c*dc/tau).subs(dc, c), 2*mass, "hostile_frozen_normalizer_would_add_false_source")
    F0, F1 = s.symbols("actual_f0 actual_f1", real=True)
    ppos = s.Symbol("positive_p", positive=True)
    Dmass, Fp0, Fp1, de, df = s.symbols("dx f0prime f1prime de df", real=True)
    physical = 6+(x*s.log(x/(2*ppos**2))+
                  (1-x)*s.log((1-x)/ppos**3))/ell+x*F0+(1-x)*F1
    direct_source = s.diff(physical, x)*Dmass+x*Fp0*de+(1-x)*Fp1*df
    eq(s.expand_log(scalar_source(x, Dmass, ell, F0, F1, Fp0, Fp1, de, df, ppos)
                    -direct_source, force=True), 0, "complete_scalar_source_matches_actual_price_differential")
    minimum = scalar_minimum(ppos, ell, F0, F1)
    eq(s.diff(minimum["price"], F0), minimum["M2_mass"], "exact_envelope_source_first_block")
    eq(s.diff(minimum["price"], F1), minimum["scalar_mass"], "exact_envelope_source_retained_scalar")
    zraw = minimum["raw_scalar_amplitude"]
    eq(2/(2+zraw*zraw), minimum["M2_mass"], "positive_trace_lift_attains_full_faithful_density_minimum")
    return {"exact_checks": len(checks), "checks": checks, "source_pins": PINS,
            "engine_zero_guard_masks": list(GUARDS), "engine_allowed_real_slots": 10,
            "scalar_effect_guard_rank": 3, "nonscalar_effect_guard_rank": 4,
            "retained_AF_scalar_channel": True,
            "minimum_attained_in_real_support_extension": True,
            "all_right_unitary_fibers_engine_compatible": False,
            "nonconstant_smooth_ring_engine_admission_derived": False,
            "scope": "named_level_one_AF_CAR_interface_not_higher_AF_no_go"}
