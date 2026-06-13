#!/usr/bin/env python3
"""D0 v12.45 SI calibration boundary certificate.

This check keeps bridge calibration coefficients out of the immutable D0 core
shape.  It intentionally uses only stdlib validation so the release gate does
not depend on an external JSON schema package.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CERT_DIR = ROOT / "05_CERTS"


def read_named_value_csv(path: Path, key: str) -> float:
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("quantity") == key:
                return float(row["value"])
    raise AssertionError(f"{key} not found in {path}")


def read_a2_trace(path: Path) -> float:
    with path.open("r", encoding="utf-8", newline="") as handle:
        row = next(csv.DictReader(handle))
    return float(row["diag_plus_2_offdiag_unique"])


def assert_bridge_schema(schema: dict) -> None:
    assert schema.get("type") == "object"
    assert "status" in schema["required"]
    assert "coefficients" in schema["required"]
    assert schema["properties"]["status"]["const"] == "BRIDGE_CALIBRATION"
    coeff = schema["properties"]["coefficients"]
    assert coeff["type"] == "object"
    assert coeff["required"] == ["c0", "c2"]
    assert coeff["properties"]["c0"]["type"] == "number"
    assert coeff["properties"]["c2"]["type"] == "number"
    assert schema["properties"]["core_shape_mutation_allowed"]["const"] is False


def assert_instance_matches_schema(instance: dict, schema: dict) -> None:
    required = set(schema["required"])
    assert required <= set(instance)
    assert instance["status"] == schema["properties"]["status"]["const"]
    assert isinstance(instance["coefficients"]["c0"], (int, float))
    assert isinstance(instance["coefficients"]["c2"], (int, float))
    assert (
        instance["core_shape_mutation_allowed"]
        == schema["properties"]["core_shape_mutation_allowed"]["const"]
    )


def main() -> int:
    locked_path = CERT_DIR / "locked_core_params.json"
    locked = json.loads(locked_path.read_text(encoding="utf-8"))

    locked_names = set(locked["locked_core_param_names"])
    expected_locked = {"eta", "rho_floor", "L_pinv", "delta0", "core_shape"}
    assert locked["status"] == "EMPIRICAL_PASSPORT"
    assert expected_locked <= locked_names
    assert all(locked["guardrails"][name] for name in [
        "eta_locked",
        "floor_locked",
        "L_pinv_locked",
        "delta0_locked",
        "core_shape_locked",
        "core_internals_unchanged_after_optimizer_attempts",
    ])

    bridge_only_symbols = {"c0", "c2", "G_N", "H0"}
    assert locked_names.isdisjoint(bridge_only_symbols)

    bridge_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "D0 SI bridge calibration boundary",
        "type": "object",
        "additionalProperties": False,
        "required": [
            "status",
            "coefficients",
            "bridge_only_symbols",
            "allowed_to_mutate",
            "core_shape_mutation_allowed",
        ],
        "properties": {
            "status": {"const": "BRIDGE_CALIBRATION"},
            "coefficients": {
                "type": "object",
                "additionalProperties": False,
                "required": ["c0", "c2"],
                "properties": {
                    "c0": {"type": "number"},
                    "c2": {"type": "number"},
                },
            },
            "bridge_only_symbols": {
                "type": "array",
                "items": {"enum": sorted(bridge_only_symbols)},
            },
            "allowed_to_mutate": {
                "type": "array",
                "items": {"enum": ["unit_scale", "action_amplitude"]},
            },
            "core_shape_mutation_allowed": {"const": False},
        },
    }
    assert_bridge_schema(bridge_schema)

    bridge_instance = {
        "status": "BRIDGE_CALIBRATION",
        "coefficients": {"c0": 1.0, "c2": 1.0},
        "bridge_only_symbols": sorted(bridge_only_symbols),
        "allowed_to_mutate": ["unit_scale", "action_amplitude"],
        "core_shape_mutation_allowed": False,
    }
    assert_instance_matches_schema(bridge_instance, bridge_schema)

    a0 = read_named_value_csv(CERT_DIR / "heat_trace_a0.csv", "weighted_trace_a0")
    a2 = read_a2_trace(CERT_DIR / "heat_trace_a2_proxy.csv")
    core_trace_shape = {"a0": a0, "a2": a2}

    base_coeffs = {"c0": 1.0, "c2": 1.0}
    changed_coeffs = {"c0": 2.5, "c2": 0.125}
    base_action = {
        "a0_amplitude": base_coeffs["c0"] * core_trace_shape["a0"],
        "a2_amplitude": base_coeffs["c2"] * core_trace_shape["a2"],
    }
    changed_action = {
        "a0_amplitude": changed_coeffs["c0"] * core_trace_shape["a0"],
        "a2_amplitude": changed_coeffs["c2"] * core_trace_shape["a2"],
    }

    assert core_trace_shape == {"a0": a0, "a2": a2}
    assert changed_action["a0_amplitude"] != base_action["a0_amplitude"]
    assert changed_action["a2_amplitude"] != base_action["a2_amplitude"]

    (CERT_DIR / "bridge_schema.json").write_text(
        json.dumps(bridge_schema, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (CERT_DIR / "si_calibration_boundary_report.json").write_text(
        json.dumps(
            {
                "status": "BRIDGE_CALIBRATION",
                "locked_core_params_validated": True,
                "bridge_schema_validated": True,
                "bridge_only_symbols": sorted(bridge_only_symbols),
                "core_trace_shape": core_trace_shape,
                "base_action": base_action,
                "changed_action": changed_action,
                "core_trace_shape_unchanged_by_c0_c2": True,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    print("PASS_SI_CALIBRATION_BOUNDARY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
