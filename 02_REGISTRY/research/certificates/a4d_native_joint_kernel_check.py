#!/usr/bin/env python3
"""Focused checks of the full joint reduction; no old suites or receipt writes."""
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
FOLDER = ROOT / "02_REGISTRY/research/sources/d0_native_joint_kernel_2026-10-16"
results = {}
for name, count_key in (("kernel_check", "checks"), ("native_chart_check", "exact_checks"),
                        ("ordered_operator_check", "exact_checks")):
    command = [sys.executable] + (["-O"] if sys.flags.optimize else [])
    command += [str(FOLDER / (name + ".py"))]
    process = subprocess.run(command, text=True, capture_output=True, check=True, timeout=60)
    data = json.loads(process.stdout)
    if type(data.get(count_key)) is not int or data[count_key] <= 0:
        raise ArithmeticError("no executed joint-system checks: " + name)
    results[name] = data

chart = results["native_chart_check"]
if (not chart["all16_exterior_grades_retained"]
        or not chart["all43_original_directions_constrained_not_frozen"]
        or chart["physical_primitive_or_current_binding_selected"]
        or chart["full_joint_Euler_kernel_solved"]):
    raise ArithmeticError("native chart scope drift")
command = [sys.executable] + (["-O"] if sys.flags.optimize else [])
command += [str(FOLDER / "full_symbol_interval.py")]
process = subprocess.run(command, text=True, capture_output=True, check=True, timeout=60)
symbol = json.loads(process.stdout)
if (symbol["status"] != "VALIDATED_FULL_Q3300_SYMBOL"
        or symbol["momenta"] != 4096 or symbol["exterior_dimension"] != 16
        or symbol["reference_dimension"] != 128
        or symbol["all19_native_field_columns"] != 19
        or symbol["restriction_dimension"] != 13
        or not symbol["mode_phase_conversion_error_included"]
        or not symbol["floating_operator_assembly_error_included"]
        or symbol["phase_root_float_error_upper"] >= 2.0**-50
        or not 0 <= symbol["Hermitian_operator_distance_from_signature_upper"] < 1
        or symbol["complex_full19_inertia_at_owned_stationary_root"]
           != {"positive": 12, "negative": 1, "representation_zero": 6}
        or symbol["other_Fourier_frequencies_solved"]
        or symbol["physical_gauge_quotient_asserted"]
        or symbol["physical_admission_or_GR_claim"]):
    raise ArithmeticError("full native q3300 symbol scope drift")
# Runtime is diagnostic metadata, excluded from the scientific comparison
# between normal and optimized execution. The exact decimal B stays present.
symbol.pop("seconds")
results["full_q3300_symbol"] = symbol
print(json.dumps({"schema": "d0-native-full-joint-reduction-check/1", "results": results,
                  "scope": "exact joint reduction, ordered jets and complete native q3300 field symbol",
                  "remaining_field_shell_kernel": "OPEN_OTHER_MODES", "physical_GR": "OPEN"},
                 ensure_ascii=False, indent=2))
