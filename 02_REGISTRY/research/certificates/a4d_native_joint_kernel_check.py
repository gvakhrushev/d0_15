#!/usr/bin/env python3
"""Focused checks of the full joint reduction; no old suites or receipt writes."""
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
FOLDER = ROOT / "02_REGISTRY/research/sources/d0_native_joint_kernel_2026-10-16"
results = {}
for name, count_key in (("kernel_check", "checks"), ("native_chart_check", "exact_checks")):
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
print(json.dumps({"schema": "d0-native-full-joint-reduction-check/1", "results": results,
                  "scope": "regular stored chart and exact matter/kernel reduction",
                  "remaining_field_shell_kernel": "OPEN", "physical_GR": "OPEN"},
                 ensure_ascii=False, indent=2))
