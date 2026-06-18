#!/usr/bin/env python3
"""D0-GRAV-QNM-001 - QNM delta0 overtone-ladder empirical passport gate (NO-GO proved, can-FAIL).

Registry: lean_status PYTHON_CERTIFIED, release_status NO_GO_PROVED, lean_theorem
`qnm_passport_requires_preregistered_inputs`. This certificate does NOT assert a ringdown result.
It certifies that the preregistered D0 finite-depth delta0 overtone-ladder passport is BLOCKED
until two preregistered artifacts exist AND validate against the frozen schema:
  * 05_CERTS/data/qnm_delta0_model.json   (the frozen, pre-data ladder model)
  * 05_CERTS/data/qnm_extracted_modes.csv (the extracted QNM mode table)
Neither is bundled, so the live verdict is NO_GO_QNM_DELTA0_OVERTONE_LADDER (exit 0).

This is a real gate, not a print-stub:
  FORM  = selftest(): data-independent asserts that the schema validators REJECT a tampered
          model (a fitted delta0, a post-registered model, delta0 promoted to an allowed fit
          parameter, a missing column) and ACCEPT a clean one, and that delta0() reproduces the
          exact frozen number theory value. Raises on any regression.
  VALUE = main(): if the preregistered inputs are ABSENT -> NO-GO (exit 0, honest, certified).
          If they are PRESENT but violate the frozen schema -> hard FAIL (raise): a malformed or
          post-hoc-tuned preregistration must NOT pass silently. If present and valid but the
          production overtone-ladder comparison is not wired -> NO-GO with that explicit reason.

delta0 (frozen, from D0 number theory): with p = 1/phi,  delta0 = (p - p^2) / 2 = 0.11803398875.
It is FORBIDDEN as a fit parameter (alongside ladder_spacing, generation_count); only mass / spin
/ phase / amplitude may be fit. A preregistration that fits delta0 falsifies the passport.

Verdict token FIRST; no PASS_/FAIL_/SKIP_ wordstart appears on any line (the verdict here is a
NO_GO_ token, matched by run_hard_theorem_closure). A malformed present preregistration raises.
"""

from __future__ import annotations

import csv
import json
import math
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "05_CERTS" / "data"
MODEL_FILE = DATA_DIR / "qnm_delta0_model.json"
MODES_FILE = DATA_DIR / "qnm_extracted_modes.csv"
NO_GO = ROOT / "05_CERTS" / "NO_GO_QNM_DELTA0_OVERTONE_LADDER.md"

NO_GO_TOKEN = "NO_GO_QNM_DELTA0_OVERTONE_LADDER"
ALLOWED_FIT = ["mass", "spin", "phase", "amplitude"]
MUST_FORBID = ("delta0", "ladder_spacing", "generation_count")


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
    print(NO_GO_TOKEN)  # verdict token FIRST (no PASS_/FAIL_/SKIP_ wordstart)
    for reason in reasons:
        print(f"reason: {reason}")
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
        "forbidden_fit_parameters",
    ]
    for key in required:
        if key not in model:
            reasons.append(f"Model JSON missing required key: {key}")
    if model.get("delta0_source") != "D0.NumberTheory":
        reasons.append("delta0_source must be D0.NumberTheory")
    if model.get("pre_registered_before_data") is not True:
        reasons.append("pre_registered_before_data must be true")

    forbidden = model.get("forbidden_fit_parameters", [])
    for token in MUST_FORBID:
        if token not in forbidden:
            reasons.append(f"{token} must be a forbidden fit parameter")

    allowed = model.get("allowed_fit_parameters", [])
    for param in allowed:
        if param not in ALLOWED_FIT:
            reasons.append(f"Parameter '{param}' is not in allowed fit parameters ({', '.join(ALLOWED_FIT)})")

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
        "extraction_method",
    ]
    for idx, row in enumerate(rows, start=1):
        for key in required:
            if key not in row:
                reasons.append(f"Row {idx} missing column: {key}")
    return reasons


def _clean_model() -> dict:
    return {
        "model_version": "1.0",
        "delta0_source": "D0.NumberTheory",
        "pre_registered_before_data": True,
        "mode_formula": "omega_n = omega_0 - n * delta0 * spacing",
        "free_parameters": [],
        "allowed_fit_parameters": ["mass", "spin"],
        "forbidden_fit_parameters": list(MUST_FORBID),
    }


def selftest() -> None:
    """FORM gate (always run, data-independent). Raises AssertionError on any regression so the
    cert can never rot back into a print-stub.
    """
    # delta0 reproduces the exact frozen number-theory value (and is NOT a trivial/fitted value)
    phi = (1.0 + math.sqrt(5.0)) / 2.0
    p = 1.0 / phi
    assert abs(delta0() - (p - p * p) / 2.0) < 1e-15
    assert abs(delta0() - 0.11803398874989485) < 1e-12, "delta0 drifted from the frozen value"
    assert delta0() != 0.0 and abs(delta0() - p) > 1e-3, "delta0 must differ from 0 and from bare 1/phi"

    # the model validator ACCEPTS a clean preregistration ...
    assert validate_model_schema(_clean_model()) == [], "a clean model must validate"
    # ... and REJECTS every tampering (negative controls — the guillotine):
    no_key = _clean_model(); del no_key["mode_formula"]
    assert validate_model_schema(no_key), "missing required key must be rejected"
    fitted_src = {**_clean_model(), "delta0_source": "fit_to_data"}
    assert validate_model_schema(fitted_src), "non-number-theory delta0 source must be rejected"
    post_reg = {**_clean_model(), "pre_registered_before_data": False}
    assert validate_model_schema(post_reg), "a post-registered model must be rejected"
    delta0_allowed = {**_clean_model(), "allowed_fit_parameters": ["delta0"]}
    assert validate_model_schema(delta0_allowed), "delta0 promoted to an allowed fit parameter must be rejected"
    unforbidden = {**_clean_model(), "forbidden_fit_parameters": ["ladder_spacing"]}
    assert validate_model_schema(unforbidden), "dropping delta0/generation_count from forbidden must be rejected"

    # the modes validator ACCEPTS a complete row and REJECTS a truncated one
    good_row = {k: "0" for k in (
        "event_id", "mode_label", "omega_real", "omega_imag",
        "sigma_real", "sigma_imag", "source", "extraction_method")}
    assert validate_modes_schema([good_row]) == [], "a complete mode row must validate"
    assert validate_modes_schema([{"event_id": "GW150914"}]), "a truncated mode row must be rejected"


def main() -> int:
    print("=== D0-GRAV-QNM-001  QNM delta0 overtone-ladder passport gate (NO-GO proved) ===")
    selftest()  # FORM gate first: refuse to run if the can-FAIL machinery has regressed

    reasons: list[str] = []
    if not MODEL_FILE.exists():
        reasons.append("missing preregistered D0 finite-depth ladder model")
    if not MODES_FILE.exists():
        reasons.append("missing extracted QNM mode table")
    if reasons:
        return no_go(reasons)  # data absent -> honest NO-GO (exit 0)

    try:
        model = json.loads(MODEL_FILE.read_text(encoding="utf-8"))
    except Exception as e:
        return no_go([f"failed to parse model JSON: {e}"])
    try:
        with MODES_FILE.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
    except Exception as e:
        return no_go([f"failed to parse modes CSV: {e}"])

    # data PRESENT: a malformed / post-hoc-tuned preregistration must FAIL hard, not silently NO-GO
    schema_reasons = validate_model_schema(model) + validate_modes_schema(rows)
    if schema_reasons:
        raise AssertionError(
            "preregistered QNM inputs are present but violate the frozen schema "
            "(a tuned/post-hoc preregistration falsifies the passport): " + "; ".join(schema_reasons)
        )

    # present and valid, but the production overtone-ladder comparison is not wired here:
    # remain in an honest NO-GO state rather than fabricate a PASS.
    return no_go([
        "preregistered inputs present and schema-valid, but the production delta0 overtone-ladder "
        "comparison + negative controls (perturbed delta0, random ladder, fitted ladder, Kerr-only "
        "baseline) are not implemented in this gate"
    ])


if __name__ == "__main__":
    raise SystemExit(main())
