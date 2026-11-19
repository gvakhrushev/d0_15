#!/usr/bin/env python3
"""Consume the actual rank8 source submersion and pure-memory second jet.

Only the two new bounded algebra calculations execute. The immutable q0
Gram-convexity result is consumed by source identity, without old replay.
The full inhomogeneous rank8 normal field inverse remains an open premise.
"""
import hashlib
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
FOLDER = ROOT / "02_REGISTRY/research/sources/d0_native_joint_kernel_2026-10-16"
PINS = {
    "rank8_source_submersion.py": "04d5fba2d34538e2c7e4b41748fafb4e88e041174f4380bd0e7990111ffc6afd",
    "pure_memory_curvature_check.py": "2c3ff9a9efa8920c958999e090e81fd3c2ee2f4448bc2e34868766e4ffbb6db9",
    "ZERO_MODE_RESULTS.json": "3191fff348ea6b4f16fa50013899f681c47428bca3f9e8db2bf22825bff94e38",
}


def require(condition, label):
    if not bool(condition):
        raise ArithmeticError("native_rank8_source:" + label)


def check_pins():
    for name, expected in PINS.items():
        require(hashlib.sha256((FOLDER / name).read_bytes()).hexdigest() == expected,
                "frozen_consumer_input:" + name)


def execute(name):
    path = FOLDER / (name + ".py")
    spec = importlib.util.spec_from_file_location("rank8_consumer_" + name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    result = module.run(ROOT)
    require(result["status"] == "PASS_EXACT" and result["exact_checks"] > 0,
            "nonempty_actual_algebra:" + name)
    return result


def run():
    check_pins()
    source = execute("rank8_source_submersion")
    curvature = execute("pure_memory_curvature_check")
    convexity = json.loads((FOLDER / "ZERO_MODE_RESULTS.json").read_text())
    require(source["carrier"] == {"sites": 4096, "Fock": 16, "shell": 128, "reference": 128}
            and source["rank_total_real"] == 151 and source["rank_q0_real"] == 7,
            "complete_native_carrier_and_all_source_rows")
    require(len(source["cases"]) == 6
            and sorted(x["rank"] for x in source["cases"]) == [3, 3, 5, 5, 5, 5],
            "all_spatial_time_sign_shell_classes")
    require(curvature["prepared_rank"] == 8
            and curvature["full_Fock_dimension"] == 16
            and curvature["reference_dimension_retained"] == 128
            and not curvature["rank8_field_inertia_or_new_joint_branch_proved"],
            "actual_pure_memory_second_jet_scope")
    require(convexity["positive_Gram_directions"] == 7
            and convexity["transfer_rank"] == 7
            and convexity["convexity"]["all10_Gram_directions_strictly_positive"]
            and convexity["convexity"]["native_whole_root_rectangle_bound"]["full_normalizer_retained"],
            "unchanged_finite_m_full_normalizer_Gram_premise")
    # Raw shell amplitudes retain right reference directions and rank births.
    sphere = 2 * 128 * 128 - 1
    source_rank = source["rank_total_real"]
    fibre = sphere - source_rank
    flat_fields = 6 * 4096 + 3
    normal_fields = 16 * 4096 - source_rank - flat_fields
    graded_amplitudes = 8 * 2 * 16 * 16 - 1
    q0_rank, gram = source["rank_q0_real"], convexity["positive_Gram_directions"]
    inertia = {"positive": q0_rank + gram, "negative": q0_rank,
               "zero": 23 - q0_rank - gram + graded_amplitudes - q0_rank}
    require(fibre == 32616 and flat_fields + fibre == 57195 and normal_fields == 40806,
            "amplitude_submersion_and_remaining_actual_normal_operator")
    require(inertia == {"positive": 14, "negative": 7, "zero": 4097}
            and sum(inertia.values()) == 23 + graded_amplitudes == 4118,
            "q0_graded_amplitude_normal_congruence")
    check_pins()
    return {"schema": "d0-native-rank8-source-consumer/1", "status": "PASS_EXACT",
            "source": source, "pure_memory_curvature": curvature,
            "consumed_unchanged_q0_Gram_result_sha256": PINS["ZERO_MODE_RESULTS.json"],
            "source_sphere_dimension": sphere, "stationary_amplitude_fibre_dimension": fibre,
            "exact_full_flat_amplitude_family_dimension": flat_fields + fibre,
            "q0_fixed_reference_momentum_slice_inertia": inertia,
            "q0_fixed_reference_momentum_slice_dimension": 4118,
            "remaining_inhomogeneous_normal_field_dimension": normal_fields,
            "full_rank8_field_inverse_or_inertia_proved": False,
            "old_calculation_replayed": False, "new_Lean_build": False,
            "physical_admission_refinement_or_GR_closed": False,
            "input_sha256": PINS,
            "entrypoint_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
