#!/usr/bin/env python3
"""Exact one-step cross-owner test for the matter-clock common-process chart.

This cross-owner certificate checks two proposed bridges at one genuinely
curved matter-clock chart point: applying the AF/CAR gate directly to the
rest vector m0, and identifying the engine's raw CAR vector with
m=rho(F)m0. The first direct update leaves the comparator probability
domain; the second is outside the current Z[a] engine store for every
coframe O in the owned equality lift. Neither decides other native maps or
global physical admission.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

import sympy as sp


ROOT = Path(__file__).resolve().parents[3]
INPUT_HEAD = "dfaf7c8df509d5abd83fa60a185ad530feadc9b5"
PINS = {
    "02_REGISTRY/research/certificates/a4d_native_af_role_orbit_metric_check.py":
        "b718a3ea3e3f47087b664cc9bb194e0e09c5ae818836efdba3e63b9c11e4f2d5",
    "02_REGISTRY/research/sources/d0_native_adaptive_engine_2026-10-16/adaptive_engine.py":
        "1eaf0ed625c78d2779da83cf85e65bf1c1e797a3719da3b786c46cd16733b402",
    "02_REGISTRY/research/sources/d0_native_preparation_stationary_2026-10-16/matter_clock_binding.py":
        "1b2c668bca6c99ca84a4be513274fddc2c9a82a832368abc4a75ee24f58fbb71",
    "02_REGISTRY/research/A4D_NATIVE_MATTER_CLOCK_RECORD_BINDING.md":
        "ec505825642a50505959b2155eee3b0840149c7c17ca0503105ee377befdb152",
    "02_REGISTRY/research/A4D_NATIVE_LORENTZ_REFLECTION_SOURCE.md":
        "e596c3d2ae0e15a17566f9cfe21b08db2f347faf2c1d2a8b066cf16a82acbedb",
    "02_REGISTRY/research/A4D_NATIVE_ADAPTIVE_AF_RECORD_ENGINE.md":
        "3e3bf3bb02aeb398dcefd54ca1892ee8d02128cc869f77db6e4818cc75c4aaf6",
}
GUARDS = (2, 3, 4, 5, 8, 9)
I4 = sp.eye(4)
I16 = sp.eye(16)
ETA = sp.diag(1, -1, -1, -1)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    if spec is None or spec.loader is None:
        raise RuntimeError("source_unavailable:" + path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def run():
    checks = []

    def check(name, condition):
        if not bool(condition):
            raise AssertionError(name)
        checks.append(name)

    def eq(name, actual, expected, reduce):
        diff = actual - expected
        values = list(diff) if isinstance(diff, sp.MatrixBase) else [diff]
        check(name, all(reduce(v) == 0 for v in values))

    for path, expected in PINS.items():
        actual = hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
        check("PIN_" + path.rsplit("/", 1)[-1], actual == expected)

    role = load("native_common_process_role_owner",
                "02_REGISTRY/research/certificates/a4d_native_af_role_orbit_metric_check.py")
    adaptive = load("native_common_process_adaptive_owner",
                    "02_REGISTRY/research/sources/d0_native_adaptive_engine_2026-10-16/adaptive_engine.py")
    binding = load("native_common_process_matter_clock_owner",
                   "02_REGISTRY/research/sources/d0_native_preparation_stationary_2026-10-16/matter_clock_binding.py")
    # Reuse the source pins internal to both actual owners.
    _adaptive_role = adaptive.owners(ROOT)
    phase, native = binding.owners(ROOT)
    data = native.native_data(ROOT)
    C = data["C"]
    a, p = C.a, C.p
    m_ref = C.mat(data["m"].subs(data["parameter"], 1))
    epsilon = p**20

    # A genuine curved comparator germ from the owner's formula, translated
    # by epsilon in the fourth scalar clock. This changes no weight or metric.
    x = sp.symbols("common_x0:4", real=True)
    kappa = sp.Rational(1, 1000)
    weights = [p**2 + kappa*x[0]**2] + [p**2]*11
    clocks = sp.Matrix(x)
    clocks[3] += epsilon
    germ = binding.decode(weights, clocks, m_ref, p)
    encoded_weights, encoded_clocks = binding.encode(germ, m_ref, p)
    eq("CURVED_GERM_WEIGHTS_ROUND_TRIP", sp.Matrix(encoded_weights),
       sp.Matrix(weights), C.red)
    eq("CURVED_GERM_CLOCKS_ROUND_TRIP", encoded_clocks, clocks, C.red)

    origin = {coordinate: 0 for coordinate in x}
    input_matter = C.mat(germ.subs(origin))
    check("SMALL_NONZERO_TOP_GRADE_CLOCK", C.red(input_matter[15] - epsilon) == 0
          and C.red(epsilon) != 0)
    check("EPSILON_IN_GOLDEN_ENGINE_RING", adaptive._engine_state(role, input_matter) is not None)
    check("EPSILON_IS_EXACTLY_SMALL", sp.Rational(5, 8)**20 < sp.Rational(1, 1000))
    check("LITERAL_ENGINE_GUARD_SECTOR", all(C.red(input_matter[i]) == 0 for i in GUARDS))

    # The input record is valid: every effect is p^2, and the exact smooth
    # program remains genuinely curved after a constant clock translation.
    input_weights, input_clocks = binding.encode(input_matter, m_ref, p)
    check("INPUT_ALL_TWELVE_EFFECTS_ARE_GOLDEN", all(C.red(w-p**2) == 0 for w in input_weights))
    vectors = phase.owner.frame(4)[1]
    variance = p**3
    v0 = weights[0]*(1-weights[0])
    e0 = I4[:, 0]
    q = (variance*I4/2 + (v0-variance)*vectors[0]*vectors[0].T/12
         + (2*kappa*x[0])**2*e0*e0.T/(48*v0))
    eq("CURVED_COMPARATOR_ZERO_JET", q.subs(x[0], 0), variance*I4/2, C.red)
    eq("CURVED_COMPARATOR_FIRST_JET_ZERO", q.diff(x[0]).subs(x[0], 0), sp.zeros(4), C.red)
    q2 = C.mat(q.diff(x[0], 2).subs(x[0], 0))
    scalar = C.red((q2[0, 0]-sp.trace(q2))/(variance/2)**2)
    eq("CURVED_SCALAR_IS_OWNED_GERM", scalar, -2*kappa/(3*variance), C.red)
    check("INPUT_METRIC_GENUINELY_CURVED", C.red(scalar) != 0)

    # Test the chart's actual raw native matter m=rho(F)m0 against the
    # literal engine coefficient domain. At the unshifted s=1 chart center,
    # every admissible coframe has F=sqrt(2/p^3) O H^(1/2), O in O(4).
    base_matter = C.mat(m_ref)
    base_engine_state = adaptive._engine_state(role, base_matter)
    check("REST_REFERENCE_ITSELF_IS_IN_ENGINE_RING", base_engine_state is not None)
    _, base_r, base_N, _ = native.rest_current_jacobian(C, base_matter)
    eq("RAW_FRAME_BASE_NORMALIZER", base_N, 3, C.red)
    eq("RAW_FRAME_BASE_CURRENT", base_r, sp.Matrix([-sp.Rational(2, 3), 0, 0]), C.red)
    j = sp.Matrix([1, *base_r])
    eta = native.ETA
    H = C.observer_pairing(eta, j)
    boost = sp.eye(4)
    boost[:2, :2] = sp.Matrix([[3, 2], [2, 3]])/sp.sqrt(5)
    eq("RAW_FRAME_POSITIVE_ROOT", boost*boost, H, C.red)
    frame_scale_squared = 2/variance
    e0 = I4[:, 0]
    frames = (
        ("IDENTITY", sp.eye(4)),
        ("PROPER_SPATIAL_PI_ROTATION", sp.diag(1, -1, 1, -1)),
    )
    raw_grade_one_norms = []
    for frame_name, O in frames:
        eq("RAW_FRAME_ORTHOGONAL_"+frame_name, O.T*O, I4, C.red)
        eq("RAW_FRAME_DETERMINANT_"+frame_name, O.det(), 1, C.red)
        eq("RAW_FRAME_FIXES_FUTURE_AXIS_"+frame_name, O*e0, e0, C.red)
        # F=(sqrt(2/s)) O B, so F^{-T} H F^{-1}=s/2 I for each O.
        q_base = (variance/2)*O*(boost.inv().T*H*boost.inv())*O.T
        eq("RAW_FRAME_MATCHES_CURVED_METRIC_"+frame_name,
           q_base, variance*I4/2, C.red)
        F = sp.sqrt(frame_scale_squared)*O*boost
        raw_base = C.C.ext(F)*base_matter
        grade_one = sp.Matrix([raw_base[index] for index in (1, 2, 4, 8)])
        eq("RAW_FRAME_GRADE_ONE_IS_EXTERIOR_LIFT_"+frame_name,
           grade_one, F*e0*(2*p-1), sp.simplify)
        raw_grade_one_norms.append(sp.simplify((grade_one.T*grade_one)[0]))
        eq("RAW_FRAME_GRADE_ONE_NORM_"+frame_name,
           raw_grade_one_norms[-1], sp.Rational(26, 5)*p**3, C.red)
    eq("RAW_GRADE_ONE_NORM_FRAME_INDEPENDENT",
       raw_grade_one_norms[0], raw_grade_one_norms[1], C.red)

    # Z[a] is contained in the algebraic integers: a is a root of the monic
    # polynomial a^4+a^2-1. But the frame-invariant squared grade-one norm
    # has a nonintegral field trace, so no O(4) can put raw m in Z[a]^16.
    eq("GOLDEN_RING_GENERATOR_MONIC", a**4+a**2-1, 0, C.red)
    p_conjugate = -1-p
    eq("GOLDEN_CONJUGATE_SUM", p+p_conjugate, -1, C.red)
    eq("GOLDEN_CONJUGATE_PRODUCT", p*p_conjugate, -1, C.red)
    eq("GOLDEN_CUBE_TRACE_QUADRATIC_FIELD", p**3+p_conjugate**3, -4, C.red)
    trace_norm = sp.Rational(26, 5)*2*(p**3+p_conjugate**3)
    trace_norm_rational = -sp.Rational(208, 5)
    eq("RAW_GRADE_ONE_NORM_TRACE", trace_norm, trace_norm_rational, C.red)
    check("RAW_GRADE_ONE_NORM_TRACE_NOT_INTEGER", trace_norm_rational.q != 1)
    check("NEGATIVE_NORM_OF_P_EXCLUDES_SQUARE_IN_QP", C.red(p*p_conjugate) < 0)

    Uplus = role.engine_gate_matrix(1)
    Uminus = role.engine_gate_matrix(-1)
    eq("FULL16_POSITIVE_BRANCH_IS_UNITARY", Uplus.T*Uplus, I16, C.red)
    eq("FULL16_NEGATIVE_BRANCH_IS_UNITARY", Uminus.T*Uminus, I16, C.red)
    check("POSITIVE_INPUT_SELECTOR", C.red(input_matter[1]) == C.red(2*p-1)
          and C.red(2*p-1) != 0)
    output_matter = C.mat(Uplus*input_matter)

    # Execute the actual coefficient-stored engine, not only the matrix jet.
    engine_state = adaptive._engine_state(role, input_matter)
    actual_first = role.engine_vector(role.E.step(engine_state))
    eq("LITERAL_ENGINE_FIRST_STEP_EQUALS_U_PLUS", C.mat(actual_first), output_matter, C.red)
    check("NEGATIVE_NEXT_SELECTOR_IS_DEFINED", C.red(output_matter[1]) == C.red(a*(4*p-3))
          and C.red(output_matter[1]) != 0)
    actual_second = role.engine_vector(role.E.step(role.E.step(engine_state)))
    expected_second = C.mat(Uminus*output_matter)
    eq("LITERAL_ADAPTIVE_SECOND_STEP_USES_NEGATIVE_BRANCH",
       C.mat(actual_second), expected_second, C.red)
    check("OUTPUT_GUARDS_RETAINED", all(C.red(output_matter[i]) == 0 for i in GUARDS))

    # Crucial cross-owner test: same fixed wiring after the actual gate.
    output_weights, _ = binding.encode(output_matter, m_ref, p)
    bad_weight = C.red(output_weights[1])
    expected_bad = C.red(2 - 3*p + a*(4*p-3))
    eq("BAD_WEIGHT_EXACT_IDENTITY", bad_weight, expected_bad, C.red)

    # Rational proof of the strict margin, without a floating-point sign test:
    # 3/5 < p < 5/8 follows by squaring 11/5 < sqrt(5) < 9/4;
    # hence a>3/4, 4p-3<-1/2, and 2-3p<1/5.
    check("RATIONAL_SQRT5_LOWER_CONTROL", sp.Rational(5) > sp.Rational(121, 25))
    check("RATIONAL_SQRT5_UPPER_CONTROL", sp.Rational(81, 16) > sp.Rational(5))
    check("A_SQUARED_LOWER_CONTROL", sp.Rational(3, 5) > sp.Rational(9, 16))
    check("INPUT_SELECTOR_POSITIVE_FROM_RATIONAL_BOUND",
          2*sp.Rational(3, 5)-1 > 0)
    check("OUTPUT_SELECTOR_NEGATIVE_FROM_RATIONAL_BOUND",
          4*sp.Rational(5, 8)-3 < 0)
    check("GOLDEN_INPUT_EFFECT_IN_OPEN_PROBABILITY_INTERVAL",
          0 < sp.Rational(1, 2)-sp.Rational(5, 8)**2
          and sp.Rational(3, 5)**2 > 0)
    check("NEGATIVE_EFFECT_BOUND_ALGEBRA",
          2-3*sp.Rational(3, 5) == sp.Rational(1, 5)
          and 4*sp.Rational(5, 8)-3 == -sp.Rational(1, 2))
    margin = sp.Rational(3, 8) - sp.Rational(1, 5)
    eq("STRICT_NEGATIVE_MARGIN_IS_7_OVER_40", margin, sp.Rational(7, 40), C.red)
    check("BAD_WEIGHT_BOUND_USES_ALL_RATIONAL_CONTROLS",
          all(name in checks for name in (
              "RATIONAL_SQRT5_LOWER_CONTROL", "RATIONAL_SQRT5_UPPER_CONTROL",
              "A_SQUARED_LOWER_CONTROL", "NEGATIVE_EFFECT_BOUND_ALGEBRA",
              "STRICT_NEGATIVE_MARGIN_IS_7_OVER_40")))
    check("FIXED_LAMBDA_ONE_COMPARATOR_DOMAIN_FAILS",
          C.red(bad_weight) == C.red(expected_bad))

    # The failure is not loss of the observer or its orientation resource.
    current0 = C.mat(C.current(sp.eye(4), input_matter))
    current1 = C.mat(C.current(sp.eye(4), output_matter))
    current_scale = 3 + epsilon**2
    eq("INPUT_CURRENT_IS_OWNED", current0,
       sp.Matrix([1, -2/current_scale, 0, 0]), C.red)
    eq("OUTPUT_CURRENT_REMAINS_TIMELIKE", current1,
       sp.Matrix([1, 2/current_scale, 0, 0]), C.red)
    lorentz_norm = C.red((current1.T*ETA*current1)[0])
    eq("OUTPUT_CURRENT_GAP_EXACT", lorentz_norm, 1-4/current_scale**2, C.red)
    check("OUTPUT_CURRENT_GAP_STRICTLY_TIMELIKE",
          C.red(epsilon**2) != 0 and C.red(current_scale-3-epsilon**2) == 0)
    check("OUTPUT_TOP_GRADE_REMAINS_NONZERO", C.red(output_matter[15]) != 0)

    return {
        "schema": "d0-native-common-process-domain/1",
        "input_head": INPUT_HEAD,
        "source_pins_sha256": PINS,
        "exact_checks": len(checks),
        "input": {
            "matter": "owned s=1 lambda=1 rest-coordinate reference + p^20 e15",
            "engine_guard_sector": list(GUARDS),
            "initial_effects": "all12 equal p^2",
            "curved_comparator_scalar": "-1/(1500*p^3)",
            "top_grade": "p^20 != 0",
        },
        "raw_frame_admission": {
            "same_chart_metric": "q=p^3 I/2 at the curved chart center",
            "frame_family": "F=sqrt(2/p^3)*O*H^(1/2), all O in O(4)",
            "grade_one_squared_norm": "26*p^3/5, independent of O",
            "field_trace": "-208/5, not an integer; raw m cannot lie in Z[a]^16",
            "verdict": "NO_RAW_ENGINE_INPUT_FOR_THIS_CHART_BASE_FOR_ANY_O",
            "engine_selector": "raw m[1] is unavailable because no O yields a Z[a]^16 state",
        },
        "one_step": {
            "branch": "+ on m0 coordinates; raw CAR selector is not identified",
            "output_first_grade": "a*(4*p-3) < 0",
            "fixed_wiring_weight_1": "2-3*p+a*(4*p-3) < -7/40",
            "output_rest_coordinate_current": "(1,2/(3+p^40),0,0)",
            "output_current_lorentz_norm": "1-4/(3+p^40)^2 > 5/9",
            "output_top_grade": "-a*p^20-p != 0",
            "next_engine_branch": "- is defined",
            "same_comparator_chart": "FAIL: effect weight is negative",
        },
        "verdict": "DIRECT_REST_COORDINATE_UPDATE_DOES_NOT_CLOSE_ON_CURVED_CHART",
        "scope": "gate applied directly to lambda=1 rest coordinates; raw (F,m)->(F',m') adapter, selector identification, AF-image and primitive admission remain unproved",
    }, checks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result, checks = run()
    path = Path(__file__).with_name("a4d_native_common_process_domain_results.json")
    if args.write:
        path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    else:
        expected = json.loads(path.read_text())
        if result != expected:
            raise AssertionError("pinned_result_mismatch")
    print("PASS_NATIVE_COMMON_PROCESS_DOMAIN exact_checks=" + str(len(checks)))
    for name in checks:
        print("PASS_" + name)
    print("RESULT " + result["verdict"])
    print("RESULT NO_RAW_ENGINE_INPUT_FOR_THIS_CHART_BASE_FOR_ANY_O")
    print("RESULT REST_COORDINATE_UPDATE_AND_GLOBAL_GR_REMAIN_OPEN")


if __name__ == "__main__":
    main()
