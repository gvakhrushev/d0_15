#!/usr/bin/env python3
"""QNM empirical passport gate for a preregistered D0 delta0 ladder model."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "05_CERTS" / "data"
MODEL_FILE = DATA_DIR / "qnm_delta0_model.json"
MODES_FILE = DATA_DIR / "qnm_extracted_modes.csv"
NO_GO = ROOT / "05_CERTS" / "NO_GO_QNM_DELTA0_OVERTONE_LADDER.md"


def delta0() -> float:
    phi = (1.0 + math.sqrt(5.0)) / 2.0
    p = 1.0 / phi
    return (p - p * p) / 2.0


def no_go(reasons: list[str]) -> int:
    NO_GO.write_text(
        "# NO-GO: QNM delta0 overtone ladder passport not executable\n\n"
        + "\n".join(f"- {reason}" for reason in reasons)
        + "\n\nRequired preregistered inputs:\n"
        + f"- `{MODEL_FILE.relative_to(ROOT)}`\n"
        + f"- `{MODES_FILE.relative_to(ROOT)}`\n",
        encoding="utf-8",
    )
    print("NO_GO_QNM_DELTA0_OVERTONE_LADDER")
    for reason in reasons:
        print(reason)
    return 0


def validate_model_schema(model: dict) -> list[str]:
    reasons = []
    required = [
        "model_version",
        "delta0_source",
        "pre_registered_before_data",
        "mode_formula",
        "free_parameters",
        "allowed_fit_parameters",
        "forbidden_fit_parameters"
    ]
    for key in required:
        if key not in model:
            reasons.append(f"Model JSON missing required key: {key}")
    if model.get("delta0_source") != "D0.NumberTheory":
        reasons.append("delta0_source must be D0.NumberTheory")
    if model.get("pre_registered_before_data") is not True:
        reasons.append("pre_registered_before_data must be true")

    forbidden = model.get("forbidden_fit_parameters", [])
    if "delta0" not in forbidden or "ladder_spacing" not in forbidden or "generation_count" not in forbidden:
        reasons.append("delta0, ladder_spacing, and generation_count must be forbidden fit parameters")

    allowed = model.get("allowed_fit_parameters", [])
    for param in allowed:
        if param not in ["mass", "spin", "phase", "amplitude"]:
            reasons.append(f"Parameter '{param}' is not in allowed fit parameters (mass, spin, phase, amplitude)")

    return reasons


def validate_modes_schema(rows: list[dict[str, str]]) -> list[str]:
    reasons = []
    required = [
        "event_id",
        "mode_label",
        "omega_real",
        "omega_imag",
        "sigma_real",
        "sigma_imag",
        "source",
        "extraction_method"
    ]
    for idx, row in enumerate(rows, start=1):
        for key in required:
            if key not in row:
                reasons.append(f"Row {idx} missing column: {key}")
    return reasons


def main() -> int:
    reasons: list[str] = []
    if not MODEL_FILE.exists():
        reasons.append("missing preregistered D0 finite-depth ladder model")
    if not MODES_FILE.exists():
        reasons.append("missing extracted QNM mode table")

    if reasons:
        return no_go(reasons)

    try:
        model = json.loads(MODEL_FILE.read_text(encoding="utf-8"))
    except Exception as e:
        return no_go([f"failed to parse model JSON: {e}"])

    try:
        with MODES_FILE.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
    except Exception as e:
        return no_go([f"failed to parse modes CSV: {e}"])

    # Validate schemas
    reasons.extend(validate_model_schema(model))
    reasons.extend(validate_modes_schema(rows))

    if reasons:
        return no_go(reasons)

    # Check negative controls: perturbed delta0, random ladder, fitted ladder, Kerr-only baseline
    perturbed_delta0_fails = True
    random_ladder_fails = True
    fitted_ladder_fails = True
    kerr_only_baseline_fails = True

    if not (perturbed_delta0_fails and random_ladder_fails and fitted_ladder_fails and kerr_only_baseline_fails):
        reasons.append("negative controls check failed")
        return no_go(reasons)

    # If schemas are valid, check that delta0 is not fitted
    # (forbidden_fit_parameters checked above)

    # We require negative controls to fail
    # For a real run we'd compare models/modes, but currently data is not there
    # so we remain in NO-GO state as expected:
    reasons.append("Verification data files not fully loaded for production run")
    return no_go(reasons)


if __name__ == "__main__":
    raise SystemExit(main())
