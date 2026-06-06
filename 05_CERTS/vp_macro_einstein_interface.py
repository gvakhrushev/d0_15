#!/usr/bin/env python3
"""Macro Einstein-interface dependency certificate.

This cert does not solve continuum GR.  It checks that the macro interface
depends on the finite D0 owners and certificates named by the books and claim
map: entropic archive gravity, explicit TT spin-2, higher-curvature finite
cut, and spectral A2/EH proxy.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


ROOT = Path(__file__).resolve().parents[1]
CERTS = ROOT / "05_CERTS"
LEAN = ROOT / "09_LEAN_FORMALIZATION" / "D0"
CLAIM_MAP = ROOT / "09_LEAN_FORMALIZATION" / "docs" / "CLAIM_TO_LEAN_MAP.csv"
STATUS = "PASS_MACRO_EINSTEIN_INTERFACE"


def run_cert(script_name: str, token: str) -> tuple[bool, str]:
    proc = subprocess.run(
        [sys.executable, str(CERTS / script_name)],
        cwd=str(ROOT),
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    return proc.returncode == 0 and token in proc.stdout, proc.stdout


def file_has(path: Path, tokens: list[str]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8")
    return all(token in text for token in tokens)


def higher_curvature_report_ok() -> bool:
    report = CERTS / "higher_curvature_bound_report.json"
    if not report.exists():
        return False
    data = json.loads(report.read_text(encoding="utf-8"))
    bounds = data.get("higher_curvature_bounds", {})
    return (
        bool(data.get("double_count_assertion"))
        and bool(data.get("factor_guard_assertion"))
        and all(bool(bounds.get(str(k), {}).get("passes")) for k in (3, 4, 5))
    )


def main() -> int:
    cert_checks = {
        "entropic_archive_cert": run_cert(
            "vp_entropic_archive_gravity.py",
            "PASS_ENTROPIC_ARCHIVE_GRAVITY",
        )[0],
        "finite_spin2_cert": run_cert(
            "vp_finite_spin2_wave_operator.py",
            "PASS_FINITE_SPIN2_WAVE_OPERATOR_CONCRETE",
        )[0],
        "spectral_a2_eh_cert": run_cert(
            "vp_spectral_action_eh_coefficient.py",
            "PASS_SPECTRAL_ACTION_EH_ADMISSIBILITY",
        )[0],
    }

    owner_checks = {
        "entropic_archive_owner": file_has(
            LEAN / "Gravity" / "EntropicArchiveInterface.lean",
            [
                "boundary_capacity_nonnegative",
                "graph_laplacian_symmetric",
                "conserved_flux_no_creation",
                "entropic_tension_energy_nonnegative",
            ],
        ),
        "macro_einstein_owner": file_has(
            LEAN / "Gravity" / "MacroEinsteinInterface.lean",
            [
                "finite_gravity_macro_constraints_closed",
                "macro_tension_einstein_hilbert_interface_closed",
                "finite_gravity_witness_yields_einstein_hilbert_interface",
            ],
        ),
        "spin2_wave_owner": file_has(
            LEAN / "Geometry" / "FiniteSpin2WaveOperator.lean",
            [
                "PiTT4",
                "WTT4",
                "finite_spin2_supplies_tt_macro_carrier",
            ],
        ),
        "higher_curvature_owner": file_has(
            LEAN / "Geometry" / "HigherCurvatureSuppression.lean",
            ["higher_curvature_terms_below_finite_readout_cut"],
        ),
        "claim_map_lists_gravity": file_has(
            CLAIM_MAP,
            [
                "D0-GRAVITY-ENTROPIC-ARCHIVE-001",
                "D0-GRAVITY-MACRO-EINSTEIN-INTERFACE-001",
            ],
        ),
        "higher_curvature_report": higher_curvature_report_ok(),
    }

    checks = cert_checks | owner_checks
    print("--- D0 MACRO EINSTEIN INTERFACE CERTIFICATE ---")
    for label, ok in checks.items():
        print(f"[{'PASS' if ok else 'FAIL'}] {label}")

    if all(checks.values()):
        print(f"[CERT-CLOSED] {STATUS}")
        return 0
    print("FAIL_MACRO_EINSTEIN_INTERFACE")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
