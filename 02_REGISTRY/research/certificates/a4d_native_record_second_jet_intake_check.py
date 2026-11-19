#!/usr/bin/env python3
"""Consume five immutable user inputs; no old suites or output-writing tail."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "02_REGISTRY/research/sources/d0_record_second_jet_intake_2026-10-15"
PINS = {
    "INPUT_A4D_NATIVE_GEOMETRIC_READING_INTERFACE.md":
        "ca94ccb5c93f0f35c3d0343a45f0c71723dc1d296ba66710a8c7761a7cf82692",
    "INPUT_heat_window_results.json":
        "caf812083e67e90dee7c4a7d71dd40c24253d1e5321e57e8d38e08b9c35543d6",
    "INPUT_check_heat_window.py":
        "9665f8d0cd19057861b8b9c644cd51aba9cb847bb0961ffb53001e0c01034d60",
    "INPUT_check_record_2jet.py":
        "2b99efc7c09df0aad2b3c8df25600d423582d203031c19c98af71d293931c3a3",
    "INPUT_A4D_NATIVE_RECORD_SECOND_JET_SOURCE_CLOSURE.md":
        "05c507bb0cae41ace9895d9a484f1b797d8fac789a3ff77f18e08a57162cb30d",
}


def verify_inputs() -> None:
    provenance = json.loads((SOURCE / "provenance.json").read_text())
    recorded = {x["archived"]: x for x in provenance["inputs"]}
    if set(recorded) != set(PINS):
        raise AssertionError("exact_five_input_manifest_required")
    for name, expected in PINS.items():
        data = (SOURCE / name).read_bytes()
        actual = hashlib.sha256(data).hexdigest()
        if actual != expected or recorded[name]["sha256"] != expected:
            raise AssertionError("immutable_input_changed:" + name)
        if recorded[name]["bytes"] != len(data):
            raise AssertionError("input_byte_count_changed:" + name)


def main() -> None:
    verify_inputs()
    sys.path.insert(0, str(SOURCE))
    from heat_consumer import run_checks as heat_checks
    from record_consumer import run_checks as record_checks
    result = {
        "status": "PASS_RECORD_SECOND_JET_INTAKE",
        "heat": heat_checks(ROOT),
        "record": record_checks(ROOT),
        "immutable_input_count": len(PINS),
        "physical_native_admission_proved": False,
        "native_action_identified": False,
        "GR_closed": False,
        "old_suites_executed": False,
    }
    verify_inputs()
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
