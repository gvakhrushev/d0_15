#!/usr/bin/env python3
"""Compose exact q0 matter constraints and full-normalizer Gram convexity.

This new bounded consumer does not repeat old root or matrix-symbol suites.
The nonlinear homogeneous critical-locus conclusion has its analytic proof
in Section9 of the existing joint-system owner; numerical ranks do not
substitute for it. Inertia is the REAL reduced density/field q0 block.
"""
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
FOLDER = ROOT / "02_REGISTRY/research/sources/d0_native_joint_kernel_2026-10-16"


def require(condition, label):
    if not bool(condition):
        raise ArithmeticError("native_zero_mode:"+label)


def execute(name):
    command = [sys.executable] + (["-O"] if sys.flags.optimize else [])
    command.append(str(FOLDER/(name+".py")))
    process = subprocess.run(command, text=True, capture_output=True, check=True, timeout=60)
    data = json.loads(process.stdout)
    require(type(data.get("exact_checks")) is int and data["exact_checks"] > 0,
            "nonempty_exact_consumer:"+name)
    return data


constraints = execute("zero_mode_constraint_check")
convexity = execute("homogeneous_price_convexity")
require(constraints["mode"] == [0, 0, 0, 0]
        and constraints["carrier"]["sites"] == 4096
        and constraints["carrier"]["Fock_dimension"] == 16
        and constraints["carrier"]["shell_rank"] == 128
        and constraints["carrier"]["reference_dimension"] == 128,
        "original_full_carrier_and_real_zero_mode")
require(constraints["rank_coframe"] == 3 and constraints["rank_link"] == 4
        and constraints["rank_T0"] == 7
        and constraints["scope"]["all16_carrier_and_full_reference_retained"]
        and not constraints["scope"]["signed_resolvent_replaced_by_positive_one"]
        and not constraints["scope"]["annihilators_classified_as_gauge"], "full_constraint_split")
require(convexity["status"] == "PASS_FINITE_M_FULL_NORMALIZER_GRAM_CONVEXITY_AND_SO4_ORBIT"
        and convexity["all10_Gram_directions_strictly_positive"]
        and convexity["native_whole_root_rectangle_bound"]["full_normalizer_retained"]
        and not convexity["full_native_action_selection_or_GR_claim"], "full_price_and_scope")
field = constraints["field_dimension_real"]
density = constraints["q0_density_tangent_dimension_real"]
rank = constraints["rank_T0"]
positive = constraints["equal_diagonal_Gram_dimension"]
frames = constraints["full_frame_orbit_dimension"]
observers = constraints["kernel_split"]["observer"]
require(constraints["field_kernel_dimension_real"] == positive+frames+observers == field-rank,
        "complete_constrained_Gram_and_frame_image")
annihilator = density-rank
require(annihilator == constraints["preparation_adjoint_annihilator_dimension_real"],
        "full_density_annihilator_retained")
inertia = {"positive": positive+rank, "negative": rank,
           "zero": frames+observers+annihilator}
require(sum(inertia.values()) == field+density, "complete_reduced_KKT_dimension")
# Required mathematical dimensions are read from the executed premises;
# explicit field names also make a changed child interface fail closed.
print(json.dumps({"schema": "d0-native-zero-mode-composition/1",
                  "constraints": constraints, "convexity": convexity,
                  "q0_scalar_field": "REAL", "field_dimension": field,
                  "shell_density_tracezero_dimension": density,
                  "transfer_rank": rank, "kerT_field_dimension": field-rank,
                  "positive_Gram_directions": positive,
                  "field_zero_directions": {"SO4_constant_coframe": frames, "observer": observers,
                                            "Lorentz_Gram_changes_beyond_proved_representations":
                                            convexity["homogeneous_SO4_orbit"]["nongauge_Lorentz_Gram_directions"]},
                  "retained_preparation_annihilator_dimension": annihilator,
                  "reduced_real_density_field_KKT_inertia": inertia,
                  "reduced_real_density_field_KKT_dimension": field+density,
                  "nonlinear_consumer": "joint-system owner Section9: local translation-invariant critical manifold dimension2049",
                  "normal_coordinate": "epsilon-(128-64sqrt2)*d",
                  "all_reference_unitaries_or_affine_shifts_included_in_inertia": False,
                  "inhomogeneous_critical_points_classified": False,
                  "physical_preparation_choice_or_refinement_or_GR_closed": False},
                 ensure_ascii=False, indent=2))
