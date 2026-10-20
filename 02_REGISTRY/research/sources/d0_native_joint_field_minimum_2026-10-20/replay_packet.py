#!/usr/bin/env python3
"""Read-only narrow replay of the joint-field-minimum packet.

Original inputs are copied to an isolated temporary path tree for the
prospective checker. The original all40 theorem and Lean suite are not run.
No generator overwrites a tracked expected result.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def verify_pins():
    manifest = json.loads((HERE / "SHA256SUMS.json").read_text())
    for name, expected in manifest["files"].items():
        path = HERE / name
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        require(actual == expected, "Frozen packet input changed: " + name)
    return len(manifest["files"])


def execute(script, *arguments):
    result = subprocess.run(
        [sys.executable, "-B", str(HERE / script), *map(str, arguments)],
        cwd=HERE, text=True, capture_output=True, check=False,
    )
    if result.returncode:
        raise RuntimeError(
            script + " failed:\n" + result.stdout + "\n" + result.stderr
        )
    require(not result.stderr, script + " emitted unexpected diagnostics: " + result.stderr)
    return json.loads(result.stdout)


def main():
    pin_count = verify_pins()
    sources = json.loads((HERE / "SOURCE_INPUTS.json").read_text())
    for item in sources["files"]:
        raw = (HERE / item["snapshot"]).read_bytes()
        require(hashlib.sha256(raw).hexdigest() == item["sha256"],
                "Historical source pin differs: " + item["source_path"])

    witness = execute("check_joint_minimum_witness.py")
    require(witness == json.loads((HERE / "WITNESS_RECEIPT.json").read_text()),
            "Direct original six-face witness differs from its frozen result")

    with tempfile.TemporaryDirectory(prefix="d0-field-price-inputs-") as temp:
        root = Path(temp)
        for item in sources["files"]:
            target = root / item["source_path"]
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(HERE / item["snapshot"], target)
        bridge = execute("check_prospective_field_bridge.py", "--repo", root)
    require(bridge == json.loads((HERE / "PROSPECTIVE_FIELD_BRIDGE_RESULT.json").read_text()),
            "Prospective field-and-price controls differ from their frozen result")

    info = execute("check_conditional_noise.py")
    require(info["status"] == "PASS" and info["cq_examples"] == 36,
            "Conditional-noise controls did not complete")
    require(info["max_direct_noise_entropy_error"] < 2e-12,
            "Direct stopped-entropy identity exceeded its stated tolerance")
    require(info["max_noise_derivative_error"] < 2e-7,
            "Conditional-noise derivative exceeded its stated tolerance")
    require(info["max_conditional_defect_error"] < 2e-12,
            "Quantum conditional-information identity exceeded its stated tolerance")
    require(info["max_pointer_q_derivative_at_T14"] < 0,
            "The declared paid conditional-pointer source lost its sign")
    require(info["script_sha256"] ==
            hashlib.sha256((HERE / "check_conditional_noise.py").read_bytes()).hexdigest(),
            "Conditional-noise checker identity mismatch")
    require(info["note_sha256"] ==
            hashlib.sha256((HERE / "CONDITIONAL_NOISE_SOURCE_NOTE.md").read_bytes()).hexdigest(),
            "Conditional-noise theorem identity mismatch")
    require(verify_pins() == pin_count, "Packet pins changed during replay")

    print(json.dumps({
        "status": "PASS",
        "source_commit": sources["source_commit"],
        "historical_snapshots": len(sources["files"]),
        "frozen_packet_pins": pin_count,
        "original_all40_theorem_replayed": False,
        "tracked_expected_results_written": False,
        "direct_original_mixed_witness": witness,
        "prospective_bridge": {
            "status": bridge["status"],
            "checks": bridge["checks"],
            "exact_frozen_result_match": True,
        },
        "conditional_noise": info,
        "scope": (
            "Exact finite mixed witness, analytical constant-family exclusion, "
            "prospective price-graph bridge and stated Info comparison. "
            "The analytical quantified theorems are independently reviewed; "
            "these controls do not establish physical native admission or GR closure."
        ),
    }, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
