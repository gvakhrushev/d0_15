#!/usr/bin/env python3
"""New exact shell reduction plus its two validated full field restrictions.

No old q3300/root suite is run. Original full-amplitude inertia and physical
admission are not asserted: the inertia below is the reduced shell-density/
field KKT after the already proved Q-amplitude elimination.
"""
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
FOLDER = ROOT / "02_REGISTRY/research/sources/d0_native_joint_kernel_2026-10-16"


def require(condition, label):
    if not bool(condition):
        raise ArithmeticError("shell_transfer_consumer:"+label)


def execute(name):
    command = [sys.executable] + (["-O"] if sys.flags.optimize else [])
    command.append(str(FOLDER/(name+".py")))
    process = subprocess.run(command, text=True, capture_output=True, check=True, timeout=60)
    result = json.loads(process.stdout)
    result.pop("seconds", None)  # runtime only; all scientific bounds remain.
    return result


exact = execute("shell_transfer_reduction")
interval = execute("full_shell_transfer_interval")
require(exact["status"] == "PASS_EXACT_ALL_A_GREATER_B_POSITIVE"
        and type(exact["exact_checks"]) is int and exact["exact_checks"] > 0,
        "executed_exact_rank_theorem")
require(interval["status"] == "VALIDATED_SHELL_TRANSFER_RESTRICTIONS"
        and interval["momenta_per_sector"] == 4096
        and interval["exterior_dimension"] == exact["exterior_dimension"] == 16
        and interval["reference_dimension"] == 128, "complete_original_carrier")
require(len(exact["cases"]) == len(interval["sectors"]) == 2, "both_complete_sectors")
combined = []
for case, sector in zip(exact["cases"], interval["sectors"]):
    require(case["q"] == sector["q"], "same_frequency")
    rank = case["exact_transfer_rank"]
    field = case["chart_complex_dimension"]
    density = case["shell_density_block_complex_dimension"]
    inertia = sector["validated_restriction_inertia"]
    require(rank == sector["independently_required_exact_rank_T"]
            and case["complete_inactive_coefficient_dimension"] == sector["restriction_dimension"]
            and field-rank == sector["restriction_dimension"]+6,
            "interval_restriction_is_complete_kerT_modulo_representation")
    require(0 <= sector["Hermitian_operator_distance_from_signature_upper"] < 1
            and inertia["zero"] == 0
            and inertia["positive"]+inertia["negative"] == sector["restriction_dimension"],
            "nonsingular_restriction_with_strict_inertia")
    require(not sector["full_unconstrained_19_or_21_field_nonsingularity_claim"]
            and not sector["shell_density_kernel_S_in_kerTadjoint_removed_as_gauge"]
            and not exact["independent_native_preparation_admission_proved"],
            "physical_and_density_scope_preserved")
    saddle = {"positive": inertia["positive"]+rank, "negative": inertia["negative"]+rank,
              "zero": 6+density-rank}
    require(sum(saddle.values()) == field+density, "full_reduced_saddle_dimension")
    combined.append({"q": case["q"], "exact_transfer_rank": rank,
                     "full_field_complex_dimension": field,
                     "full_shell_density_complex_dimension": density,
                     "reduced_density_field_KKT_complex_dimension": field+density,
                     "reduced_density_field_KKT_complex_inertia": saddle,
                     "only_field_kernel_is_proved_representation_directions": 6,
                     "retained_density_annihilator_complex_dimension": density-rank,
                     "Q_amplitude_and_reference_vertical_inertia_included": False})

print(json.dumps({"schema": "d0-native-shell-transfer-complete-KKT/1",
                  "exact_reduction": exact, "interval_restrictions": interval,
                  "complete_reduced_KKT_sectors": combined,
                  "all_other_Fourier_modes": "OPEN", "nonflat_root": "OPEN",
                  "physical_admission_refinement_GR": "OPEN"}, ensure_ascii=False, indent=2))
