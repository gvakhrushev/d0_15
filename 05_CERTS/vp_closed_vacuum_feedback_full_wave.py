#!/usr/bin/env python3
"""Aggregate D0 closed vacuum feedback full-wave passport."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PASSPORT = ROOT / "08_PASSPORTS" / "VacuumFeedback"
SCRIPTS = [
    "vp_internal_feedback_resolvent.py",
    "vp_feedback_partition_function.py",
    "vp_finite_feedback_equation_of_state.py",
    "vp_terminal_feedback_modes.py",
    "vp_pressure_capacity_balance.py",
    "vp_sde_feedback_reduction.py",
]
REQUIRED = [
    "PASS_INTERNAL_FEEDBACK_RESOLVENT",
    "PASS_FEEDBACK_DETERMINANT_RETURN_CYCLES",
    "PASS_FINITE_FEEDBACK_PARTITION_FUNCTION",
    "PASS_FEEDBACK_PRESSURE_TRACE_LOG",
    "PASS_FINITE_PVT_EQUATION_OF_STATE",
    "PASS_TERMINAL_FEEDBACK_MODE_CRITERION",
    "PASS_PRESSURE_CAPACITY_BALANCE_REGIMES",
    "PASS_SDE_TWO_MODE_FEEDBACK_REDUCTION",
    "PASS_DESI_FAILURE_BOUNDARY_FEEDBACK_DIAGNOSIS",
    "PASS_SPARC_FAILURE_BOUNDARY_FEEDBACK_DIAGNOSIS",
    "PASS_THEOREM_GRADE_BOUNDARY_DERIVATIVE_DIAGNOSTIC",
    "FAIL_EXTERNAL_MIRROR_MODEL",
    "FAIL_PHOTON_ACCELERATION_MODEL",
    "FAIL_IDEAL_GAS_CORE_POSTULATE",
    "FAIL_DESI_ROOT_REFIT_REPAIR",
    "FAIL_DESI_WINDOW_REFIT_REPAIR",
    "FAIL_ARBITRARY_KERNEL_REPAIR",
    "FAIL_MATTER_AS_ARBITRARY_EIGENVALUE",
]


def main() -> int:
    PASSPORT.mkdir(parents=True, exist_ok=True)
    outputs: dict[str, str] = {}
    combined = ""
    for script in SCRIPTS:
        proc = subprocess.run([sys.executable, str(ROOT / "05_CERTS" / script)], text=True, capture_output=True, cwd=ROOT)
        outputs[script] = proc.stdout + proc.stderr
        combined += outputs[script] + "\n"
        if proc.returncode != 0:
            print(f"FAIL_CLOSED_VACUUM_FEEDBACK_FULL_WAVE: {script}")
            print(outputs[script])
            return proc.returncode
    missing = [token for token in REQUIRED if token not in combined]
    status = "PASS_CLOSED_VACUUM_FEEDBACK_FULL_WAVE" if not missing else "FAIL_CLOSED_VACUUM_FEEDBACK_FULL_WAVE"
    summary = {
        "status": status,
        "package": "D0_CLOSED_VACUUM_FEEDBACK_THERMODYNAMICS_FULL_WAVE",
        "required_tokens": REQUIRED,
        "missing": missing,
        "scripts": outputs,
    }
    (PASSPORT / "full_wave_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(status)
    if missing:
        print("missing:", ",".join(missing))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
