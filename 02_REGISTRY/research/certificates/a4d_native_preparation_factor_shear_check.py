#!/usr/bin/env python3
"""Exact composition of the owned AF preparation price with the flat factor shear.

This tests one concrete corrected golden-determinant/AF-price route.  It does
not classify the uncorrected archive action or establish native admission.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

import sympy as s

ROOT = Path(__file__).resolve().parents[3]
RESULT_PATH = Path(__file__).with_name("a4d_native_preparation_factor_shear_results.json")
PINS = {
    "02_REGISTRY/research/A4D_RECORD_NORMAL_VOLUME_SOURCE.md":
        "26a167bc03432fa575e0f4b32eca5cbb6fb2e8cef0f2d44ad60080cef3b3f0e0",
    "02_REGISTRY/research/A4D_GOLDEN_DETERMINANT_COMPILER.md":
        "c22d21cebacee987642cf2bed2974b6af9bfced8f99b0d4fa7f6292addf8facc",
    "02_REGISTRY/research/A4D_COHERENT_COMPILATION_COST_DESCENT.md":
        "72826a840aac882d1a93acaf0e1eba5c7e7c57cd5bfc770aff26c5824375f43c",
    "02_REGISTRY/research/sources/d0_coherent_compilation_2026-10-16/PREPARATION_SYNTHESIS.md":
        "5393e25db0267ad2b5a33b211c052b877c3b896d82366405caa420e8ee7f3867",
    "02_REGISTRY/research/A4D_NATIVE_PREPARATION_STATIONARY_SOURCE.md":
        "839b6590911a3fedb1543f8314e7e19b205fe927a169c5df37cb42fa56d2a45b",
    "02_REGISTRY/research/sources/d0_native_preparation_stationary_2026-10-16/preparation.py":
        "1e3c00dc0e28503e8c9103daf6ce3583f0500d65b64ee7bc4baf8e1bf4726ffd",
    "02_REGISTRY/research/sources/d0_jacobian_controlled_record_2026-10-16/controlled_record.py":
        "dd3b7aa6f661dbef4117b2913e62136447a14e2d08a16b08b325cb688874f4ff",
    "02_REGISTRY/research/sources/d0_flat_record_2026-10-15/check_flat_record.py":
        "acc5f43bc652f111ab46ea090357a9e9289b1153aca1cbdc4892ec893c9de1a2",
    "02_REGISTRY/research/sources/d0_golden_cylinder_curvature_2026-10-15/check_golden_curvature.py":
        "2cf15a9dcffe6c24bd609d88db9825b999ec3201b0ea724ab29f11008372ed3a",
    "02_REGISTRY/research/A4D_NATIVE_FACTOR_IMBALANCE_REMAINDER.md":
        "5fb7f4c5e7bbae5924b1b169c867c96993266d9eec52ac05e1ba6e451de722af",
    "02_REGISTRY/research/certificates/a4d_native_factor_imbalance_remainder_certificate.json":
        "5c2e3691feccf4f9c3bf4d62931f14aa965bf08a344f9aa1272fcef490946107",
    "02_REGISTRY/research/certificates/a4d_native_af_role_orbit_metric_results.json":
        "ad3630ea297bb6ec6d8e5481fa5e3ffd6ee8fd2c9a81108da679d5f0e016f53c",
    "02_REGISTRY/research/A4D_NATIVE_AF_ROLE_ORBIT_CAR_GEOMETRY_2026-10-16.md":
        "7a14491f4c14a24f7e44aa0ffefddad2a5b21c9ccd33a8f20f90a829289369b1",
}


def load(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    if spec is None or spec.loader is None:
        raise RuntimeError("owner_unavailable:" + relative)
    module = importlib.util.module_from_spec(spec)
    import sys
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def run_checks() -> dict:
    checks: list[str] = []

    def check(condition: object, label: str) -> None:
        if not bool(condition):
            raise AssertionError(label)
        checks.append(label)

    for relative, digest in PINS.items():
        actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
        check(actual == digest, "pinned_owner:" + relative)

    factor = json.loads((ROOT / "02_REGISTRY/research/certificates/"
                         "a4d_native_factor_imbalance_remainder_certificate.json").read_text())
    factor_scope = factor["scope"]
    check(factor["status"] == "PASS" and factor["analytic_all_L_factor_bound"] ==
          "2*(E1-E2)>1/10000", "owned_heat_factor_bound")
    check(factor_scope["fixed_gate_prepared_class_factor_derivative"] ==
          "2*(E1-E2)>1/10000_AT_beta_log2_ALL_L_GE_2",
          "owned_fixed_gate_heat_response")
    check(factor_scope["whole_feedback_remainder"].startswith("Jprime=Cphi*sigma") and
          factor["checks"].get("same_factor_path_complete_remainder_derivative_zero", 0) > 0,
          "owned_fixed_golden_feedback_source_zero")
    check(factor_scope["rho0_comparison"] ==
          "EXACT_ZERO_IN_ALL_TEN_SLOTS_ON_CONSTANT_FLAT_LORENTZ_READOUT",
          "owned_flat_Einstein_covector_zero")

    role = json.loads((ROOT / "02_REGISTRY/research/certificates/"
                       "a4d_native_af_role_orbit_metric_results.json").read_text())
    interface = role["AF_engine_cross_owner_joint_sector"]["complete_A1_activation_interface"]
    kernel = s.Matrix([[int(entry) for entry in row]
                       for row in interface["engine_support_kernel_basis"]]).T
    expected_kernel = s.Matrix([[1, 0], [0, 0], [0, 0], [1, 0], [0, 1]])
    check(kernel == expected_kernel and interface["engine_support_constraint_rank"] == 3,
          "owned_AF_engine_support_kernel")

    flat = load("preparation_factor_shear_flat_owner",
                "02_REGISTRY/research/sources/d0_flat_record_2026-10-15/check_flat_record.py")
    prep = load("preparation_factor_shear_preparation_owner",
                "02_REGISTRY/research/sources/d0_native_preparation_stationary_2026-10-16/preparation.py")
    AF, price = prep.owners(ROOT)
    address_AF, cylinder = price.owners(ROOT)
    check(address_AF.p == AF.p, "same_golden_AF_parameter_for_preparation_and_addresses")
    addressing = price.same_cost_addresses(cylinder, count=572, length=13, returns=4)
    check(addressing["available_settings"] == 715 and
          len(addressing["addresses"]) == 572,
          "572_distinct_equal_cost_addresses_exist_in_owned_carrier")
    check(addressing["prefix_cost"] == 17 and addressing["cut_cost"] == 20 and
          len(addressing["ready"]) == 10946 and len(addressing["pending"]) == 6765,
          "literal_native_cut_for_572_address_program")
    addressed_leaves = tuple(index for pair in addressing["addresses"] for index in pair)
    check(len(addressed_leaves) == 1144 and len(set(addressed_leaves)) == 1144,
          "all_572_settings_have_disjoint_success_failure_leaves")
    check(all(cylinder.cost(word) == addressing["cut_cost"]
              for word in addressing["ready"]) and
          all(cylinder.cost(word) == addressing["cut_cost"]+1
              for word in addressing["pending"]),
          "all_ready_and_pending_native_leaves_retained_at_exact_cost")
    _labels, k_vectors = flat.frame(4)
    check(len(k_vectors) == 12, "literal_twelve_active_flat_shape_vectors")
    shapes = [-2*k*k.T/s.sqrt(12*AF.p**3) for k in k_vectors]
    check(all(A.rank() == 1 for A in shapes), "all_twelve_owned_flat_shapes_rank_one")
    check(s.simplify(sum(s.trace(A)**2 for A in shapes) - 16/AF.p**3) == 0,
          "owned_flat_extrinsic_bending_kept")

    # The owner has 560 additional normal directions with zero shape operator.
    all_shapes = shapes + [s.zeros(4) for _ in range(560)]
    check(len(all_shapes) == 572, "complete_572_normal_shape_carrier")
    solder_scale = s.diag(2, s.Rational(1, 2), 1, 1)
    raw_factor_jet = s.diag(8, -s.Rational(1, 2), 0, 0)
    V = solder_scale.inv()*raw_factor_jet*solder_scale.inv()
    check(V == s.diag(2, -2, 0, 0), "factor_shear_whitens_to_shape_probe")
    scale = s.symbols("scale", nonzero=True, real=True)
    gamma = 2*AF.p**6
    zero = s.zeros(4)
    effect_values = []
    effect_jets = []
    for index, A in enumerate(all_shapes):
        # The raw owner has dA=-V*A. Conjugating into the orthonormal tangent
        # frame used by the determinant compiler gives the symmetric jet below.
        raw_dA = -V*A
        dA = -(V*A+A*V)/2
        check(dA.T == dA, "self_adjoint_shape_jet_"+str(index))
        e2 = s.simplify((s.trace(A)**2-s.trace(A*A))/2)
        de2 = s.simplify(s.trace(A)*s.trace(dA)-s.trace(A*dA))
        raw_de2 = s.simplify(s.trace(A)*s.trace(raw_dA)-s.trace(A*raw_dA))
        detA = s.simplify(A.det())
        ddetA = s.simplify(s.trace(A.adjugate()*dA))
        u = s.simplify(scale**2*e2+scale**4*detA)
        du = s.simplify(scale**2*de2+scale**4*ddetA)
        effect_values.append(s.simplify(AF.p**2*(1+gamma*u)))
        effect_jets.append(s.simplify(AF.p**2*gamma*du))
        raw_ddetA = s.simplify(s.trace(A.adjugate()*raw_dA))
        check(e2 == 0 and de2 == 0 and raw_de2 == 0,
              "zero_second_symmetric_invariant_"+str(index))
        check(detA == 0 and ddetA == 0 and raw_ddetA == 0,
              "zero_determinant_invariant_"+str(index))
        check(u == 0 and du == 0, "zero_compiled_effect_jet_"+str(index))
        check(dA == zero if index >= 12 else s.simplify(dA+A*V/2+V*A/2) == zero,
              "shape_jet_has_owned_rank_one_tangent_form_"+str(index))

    # E_eff=p^2[I+gamma*sum_i u_i Q_i] therefore remains the blank effect
    # through this complete 572-setting first jet.
    check(s.simplify(gamma) != 0, "golden_effect_coupling_is_nonzero")
    check(all(value == AF.p**2 for value in effect_values),
          "golden_determinant_even_effect_is_blank")
    check(all(value == 0 for value in effect_jets),
          "golden_determinant_effect_first_jet_is_zero")
    setting_parameters = [s.simplify(value/AF.p**2-1) for value in effect_values]
    setting_parameter_jets = [s.simplify(value/AF.p**2) for value in effect_jets]
    check(len(setting_parameters) == len(addressing["addresses"]) and
          all(value == 0 for value in setting_parameters) and
          all(value == 0 for value in setting_parameter_jets),
          "shape_index_to_actual_AF_address_compiler_map_is_blank_to_first_order")
    addressed_effect = price.addressed_effect_diagonal(AF.p, addressing, setting_parameters)
    check(all(value == AF.p**2 for block in addressed_effect for value in block),
          "all_572_compiled_settings_leave_complete_AF_effect_blank")
    hostile_parameters = [s.S.Zero]*len(addressing["addresses"])
    hostile_parameters[0] = s.Rational(1, 2)
    sqrt5 = s.sqrt(5)
    golden_p = (sqrt5-1)/2
    hostile_value = s.simplify((AF.p**2*(1+hostile_parameters[0])).subs(AF.p, golden_p))
    # For positive sqrt(5), 9>5 proves sqrt(5)<3 and 45>25 proves
    # 5<3*sqrt(5); hence 0<(9-3*sqrt(5))/4<1 exactly.
    check(s.simplify(hostile_value-(9-3*sqrt5)/4) == 0 and
          9 > 5 and 9*5 > 25,
          "hostile_one_setting_control_remains_a_strict_effect")
    hostile_effect = price.addressed_effect_diagonal(AF.p, addressing, hostile_parameters)
    hostile_pair = set(addressing["addresses"][0])
    changed_ready = {index for index, value in enumerate(hostile_effect[0])
                     if value != AF.p**2}
    check(changed_ready == hostile_pair and
          all(value == AF.p**2 for value in hostile_effect[1]),
          "hostile_nonzero_single_setting_changes_only_its_two_ready_leaves")
    check(role["AF_engine_cross_owner_joint_sector"][
              "engine_support_intersection_M2_coordinates"] == ["1", "0", "0", "1"],
          "blank_M2_scalar_direction_is_the_owned_engine_intersection")

    resolutions = ((s.eye(2), (AF.p**2, AF.p**2)), (s.eye(1), (AF.p**2,)))
    log_phi = s.Symbol("log_phi", positive=True)
    optimum = prep.faithful_preparation(AF, price, 1, resolutions, log_phi)
    C0, C1 = optimum["amplitude"]
    check(s.simplify(C0[0, 1]) == 0 and s.simplify(C0[1, 0]) == 0 and
          s.simplify(C0[0, 0]-C0[1, 1]) == 0,
          "blank_effect_optimizer_M2_amplitude_is_scalar_identity")
    optimizer_vector = s.Matrix([C0[0, 0], C0[0, 1], C0[1, 0], C0[1, 1], C1[0, 0]])
    check(kernel.rank() == kernel.row_join(optimizer_vector).rank(),
          "optimizer_direction_meets_linear_engine_support")
    source = prep.envelope_source(optimum["density"], optimum["conditional_derivative"],
                                  (s.zeros(2), s.zeros(1)))
    check(s.simplify(source) == 0, "optimized_AF_metric_source_zero_for_zero_effect_jet")

    return {
        "schema": "d0-native-preparation-factor-shear/1",
        "status": "PASS_SCOPED_FACTOR_SHEAR_TEST",
        "exact_checks": len(checks),
        "active_flat_shapes": 12,
        "zero_normal_shapes": 560,
        "complete_normal_settings": len(all_shapes),
        "actual_AF_addressed_settings": len(addressing["addresses"]),
        "address_construction": {
            "prefix_length": 13,
            "return_count": 4,
            "available_equal_cost_settings": addressing["available_settings"],
            "prefix_cost": addressing["prefix_cost"],
            "cut_cost": addressing["cut_cost"],
            "ready_leaves": len(addressing["ready"]),
            "pending_leaves": len(addressing["pending"]),
            "active_success_failure_leaves": len(addressed_leaves),
        },
        "metric_tangent_in_whitened_chart": ["2", "-2", "0", "0"],
        "compiled_even_effect": "E_eff=p^2*I; dE_eff=0",
        "hostile_one_setting_control": "one_nonzero_parameter_changes_exactly_its_two_ready_leaves",
        "optimized_AF_source": "0",
        "optimizer_M2_direction": "scalar_multiple_of_I2",
        "engine_support": "linear_support_direction_admitted; coefficient-level physical admission OPEN",
        "fixed_golden_two_tick_remainder": "0",
        "positive_heat_factor_source": "2*(E1-E2)>1/10000 at beta=log(2), all L>=2",
        "flat_Einstein_covector": "rho0=0 in all ten metric slots",
        "conclusion": "this corrected fixed-gate preparation price supplies no stress to cancel the owned heat factor source",
        "scope": "one actual flat golden record carrier, its complete normal shape family, the corrected determinant effect and the inherited AF preparation minimum",
        "uncorrected_archive_action_classified": False,
        "native_primitive_admission": False,
        "full_core_no_go": False,
        "GR_closed": False,
        "checks": checks,
    }


if __name__ == "__main__":
    result = run_checks()
    expected = json.loads(RESULT_PATH.read_text())
    if result != expected:
        raise ArithmeticError("factor_shear_certificate_result_mismatch")
    print("PASS_SCOPED_FACTOR_SHEAR_TEST "
          f"exact_checks={result['exact_checks']} "
          f"normal_shapes={result['complete_normal_settings']} "
          f"AF_addresses={result['actual_AF_addressed_settings']} "
          f"compiled_effect={result['compiled_even_effect']} "
          f"optimized_AF_source={result['optimized_AF_source']} "
          f"heat_source={result['positive_heat_factor_source']} "
          f"rho0={result['flat_Einstein_covector']}")
