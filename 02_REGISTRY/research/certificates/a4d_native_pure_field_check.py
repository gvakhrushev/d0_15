#!/usr/bin/env python3
"""Complete the native rank8 normal operator at the owned finite v8 root.

The 488 NEW interval blocks consume previously frozen scalar definitions.
The unchanged q0 and spatial-opposite restrictions are consumed by identity,
without historical runs. Fixed decimal choices have no proof status before
the outward congruence test. No root search, density inverse, Lean build,
physical admission or refinement claim is made here.
"""
import hashlib
import importlib.util
import json
import math
from fractions import Fraction
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[3]
FOLDER = ROOT / "02_REGISTRY/research/sources/d0_native_joint_kernel_2026-10-16"
PINS = {
    "pure_memory_interval.py": "19d4e33f7c74465da9079ec4e3c90e0b20b3b1aad448a0cdb1957a3fc61ef41f",
    "pure_memory_symbol.py": "1ef97d8f72d5133c75c2c071ed75b8b9ce295322c407c49e91bf589afd2af9fd",
    "pure_memory_choices.py": "7b26627292730abef6b36bd592398488bfea3085058570e6206c3938b078d506",
    "PURE_MEMORY_CHOICES.json": "be4facb35ddd2532f137db5a27a4ec6da3b97943980e93f9ddea9a8241390d6a",
    "field_inverse_choice.py": "1fa0f1022301d3eb529d1394a99c41849f193ea0e4980f94936674d29e7d5c8a",
    "pure_memory_shell_restriction_check.py": "ba1b75d8be0853f8ef047fae269b50bd3cfa86627935304dc92cdb63ca8277e2",
    "OPPOSITE_SHELL_TRANSFER_RESULTS.json": "ea994fef6edc38f4b01a98eed7379841f6a603dfbb02b641382bfa853f64db75",
    "ZERO_MODE_RESULTS.json": "3191fff348ea6b4f16fa50013899f681c47428bca3f9e8db2bf22825bff94e38",
    "RANK8_SOURCE_RESULTS.json": "2091dfb04335648ab2229cb7730dc5d0834de68fdf2bdd2268593150f3ccb4f7",
}
CHANGED_SHELL = ((2, 0, 0, 0), (0, 2, 0, 0), (1, 1, 0, 0),
                 (1, 7, 0, 0), (0, 1, 1, 0))


def require(condition, label):
    if not bool(condition):
        raise ArithmeticError("native_pure_field:" + label)


def pins():
    for name, digest in PINS.items():
        require(hashlib.sha256((FOLDER / name).read_bytes()).hexdigest() == digest,
                "immutable_input:" + name)


def load(name):
    spec = importlib.util.spec_from_file_location("pure_field_entry_" + name,
                                                FOLDER / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run():
    pins()
    intervals, domain = load("pure_memory_interval"), load("field_inverse_choice")
    representatives, differences = domain.domain()
    data = json.loads((FOLDER / "PURE_MEMORY_CHOICES.json").read_text())
    choices = data["choices"]
    expected = representatives + list(CHANGED_SHELL)
    require([tuple(row["q"]) for row in choices] == expected and len(expected) == 488,
            "all483_field_classes_and_exactly_five_changed_shell_classes")
    capsule = load("pure_memory_shell_restriction_check").run(ROOT)
    require(capsule["status"] == "PASS_EXACT_TWO_POINT_AND_RANK_TWO_REDUCTION",
            "exact_shell_rank_two_formula_and_q0170_identity")
    source = json.loads((FOLDER / "RANK8_SOURCE_RESULTS.json").read_text())
    q0 = json.loads((FOLDER / "ZERO_MODE_RESULTS.json").read_text())
    require(source["source"]["rank_total_real"] == 151
            and source["exact_full_flat_amplitude_family_dimension"] == 57195
            and q0["positive_Gram_directions"] == 7
            and q0["convexity"]["all10_Gram_directions_strictly_positive"],
            "unchanged_source_submersion_flat_family_and_q0_strict_convexity")
    shared = intervals.prepare_shared(ROOT)
    rows, covering, field_dimension, shell_dimension = [], set(), 0, 0
    inertia = {"positive": 43, "negative": 12, "zero": 0}
    field_inertia = {"positive": 0, "negative": 0, "zero": 0}
    old_sector = json.loads((FOLDER / "OPPOSITE_SHELL_TRANSFER_RESULTS.json").read_text())["sector"]
    old_B2 = sum(Fraction(real)**2+Fraction(imag)**2
                 for row in old_sector["exact_decimal_preconditioner"] for real, imag in row)
    reused_inverse_integer = math.ceil(old_B2/(1-Fraction(
        old_sector["Hermitian_operator_distance_from_signature_upper"])))
    worst, worst_q, inverse_integer = 0, None, reused_inverse_integer
    for index, choice in enumerate(choices):
        q = tuple(choice["q"])
        orbit = set(domain.orbit(q))
        require(len(orbit) == choice["orbit_size"] and not (covering & orbit),
                "disjoint_real_frequency_orbit:" + str(q))
        require(choice["real_amplitudes_only"] == all((2*x) % 8 == 0 for x in q),
                "self_conjugate_real_counting:" + str(q))
        covering |= orbit
        result = intervals.evaluate(q, choice, shared, strict=True)
        require(result["status"] == "VALIDATED" and result["zero"] == 0,
                "whole_root_box_nonzero_signature:" + str(q))
        restricted = q in differences
        require(restricted == choice["shell_kerT_restriction"], "complete_kerT_section")
        real_dimension = len(orbit)*result["dimension"]
        if restricted:
            shell_dimension += real_dimension
            spatial_coordinate_norm_squared = 1
        else:
            field_dimension += real_dimension
            # The fixed spatial mean section maps by a congruence whose
            # squared norm is <= number of active Fourier coordinates.
            spatial_coordinate_norm_squared = sum(x != 0 for x in q)
            for key in field_inertia:
                field_inertia[key] += len(orbit)*result[key]
        for key in inertia:
            inertia[key] += len(orbit)*result[key]
        bound = Fraction(result["inverse_native_coefficient_norm_upper"])
        inverse_integer = max(inverse_integer,
                              math.ceil(bound*spatial_coordinate_norm_squared))
        if result["distance_from_signature_upper"] > worst:
            worst, worst_q = result["distance_from_signature_upper"], list(q)
        # Runtime and repeated immutable metadata do not belong to each
        # deterministic scientific block. All error rows are retained.
        for key in ("seconds", "root_box", "source_pins", "carrier", "scope"):
            result.pop(key)
        result.update(orbit_size=len(orbit), real_dimension=real_dimension,
                      real_amplitudes_only=choice["real_amplitudes_only"])
        rows.append(result)
        if (index+1) % 25 == 0 or index+1 == len(choices):
            print("new pure root-box blocks %d/488; max distance %.9g at %s" %
                  (index+1, worst, worst_q), file=sys.stderr, flush=True)
    require(field_dimension == 40511 and shell_dimension == 240
            and len(covering) == 4089, "exact_new40751_normal_directions")
    require(sum(inertia.values()) == 40806 and inertia["zero"] == 0,
            "complete_native_rank8_normal_operator")
    reduced = {"positive": inertia["positive"]+151,
               "negative": inertia["negative"]+151, "zero": 57195}
    full = {"positive": inertia["positive"]+16740503,
            "negative": inertia["negative"]+4247, "zero": 57195}
    require(sum(reduced.values()) == 98303 and sum(full.values()) == 16842751,
            "raw_reference_rank_birth_and_Q_dimensions_counted_once")
    pins()
    for name, digest in shared["source_pins"].items():
        path = ROOT / name if "/" in name else FOLDER / name
        require(hashlib.sha256(path.read_bytes()).hexdigest() == digest,
                "unchanged_scalar_definition_after_execution:" + name)
    return {"schema": "d0-native-pure-memory-complete-normal-operator/1",
            "status": "VALIDATED_NATIVE_RANK8_LOCAL_FLAT_CRITICAL_LOCUS",
            "carrier": {"L": 8, "thermal_momenta": 4096, "Fock": 16,
                        "shell": 128, "reference": 128, "prepared_rank": 8},
            "root_box": shared["core"]["root_box"], "interval_precision_decimal": 80,
            "new_interval_classes": 488, "new_real_normal_directions": 40751,
            "reused_real_normal_directions": 55,
            "exact_shell_algebra": capsule,
            "field_only_inertia_real": field_inertia,
            "normal_V_inertia_real": inertia, "normal_V_dimension": 40806,
            "maximum_distance_from_signature_upper": worst, "maximum_distance_q": worst_q,
            "canonical_nonzero_V_inverse_norm_integer_upper": inverse_integer,
            "reused_q0170_inverse_norm_integer_upper": reused_inverse_integer,
            "q0_Gram_coercivity_consumed_separately": True,
            "reduced_raw_shell_amplitude_inertia": reduced,
            "full_normalized_amplitude_inertia": full,
            "exact_flat_amplitude_critical_family_dimension": 57195,
            "local_critical_locus_equals_exact_flat_family": True,
            "normal_IFT_uses_actual_rank8_source_submersion": True,
            "reference_and_rank_birth_directions_counted_once": True,
            "scope": {"conditional_finite_v8_only": True,
                      "actual_native_chi_mask1_plus_mask15": True,
                      "true_chart_second_jet_full_Z_and_signed_Q": True,
                      "other_preparations_distant_roots_or_refinement_closed": False,
                      "physical_preparation_admission_or_original_fixed_g_tau_raw_GR_closed": False,
                      "historical_root_full_matrix_or_Lean_replayed": False},
            "input_sha256": {**shared["source_pins"], **PINS},
            "entrypoint_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "blocks": rows}


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, sort_keys=True, indent=2))
