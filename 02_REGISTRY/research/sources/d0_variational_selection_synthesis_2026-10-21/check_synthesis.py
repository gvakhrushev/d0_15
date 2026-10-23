#!/usr/bin/env python3
"""Replay six bounded synthesis checks against two frozen scientific input roots.

This verifies provenance and reproduces diagnostics, not the general analytical
theorems. Their hypotheses are stated in the core proofs and late applications.
No expected receipt or source file is rewritten. Python >=3.10, NumPy, SciPy and SymPy
are required; no network, Git executable, or repository checkout is required.
"""
from pathlib import Path
import hashlib
import json
import math
import os
import platform
import subprocess
import sys


HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def same_receipt(actual, expected, path="result"):
    """Keep exact data exact; tolerate only binary floating diagnostic roundoff."""
    require(type(actual) is type(expected), f"Type changed at {path}")
    if isinstance(expected, dict):
        require(actual.keys() == expected.keys(), f"Keys changed at {path}")
        for key, value in expected.items():
            same_receipt(actual[key], value, f"{path}.{key}")
    elif isinstance(expected, list):
        require(len(actual) == len(expected), f"Length changed at {path}")
        for i, (a, e) in enumerate(zip(actual, expected)):
            same_receipt(a, e, f"{path}[{i}]")
    elif isinstance(expected, float):
        require(math.isfinite(actual) and math.isfinite(expected),
                f"Nonfinite diagnostic at {path}")
        require(math.isclose(actual, expected, rel_tol=5e-12, abs_tol=5e-13),
                f"Float diagnostic changed at {path}: {actual} != {expected}")
    else:
        require(actual == expected, f"Exact receipt changed at {path}")


def verify_sources(pins, root_name="inputs"):
    for row in pins["sources"]:
        data = (HERE / root_name / row["path"]).read_bytes()
        require(len(data) == row["bytes"], "Source length: " + row["path"])
        require(hashlib.sha256(data).hexdigest() == row["sha256"],
                "Source SHA256: " + row["path"])
        blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        require(blob == row["git_blob"], "Source Git blob: " + row["path"])


def verify_artifacts(artifacts):
    for rel, expected in artifacts["sha256"].items():
        require(hashlib.sha256((HERE / rel).read_bytes()).hexdigest() == expected,
                "Reviewed artifact changed: " + rel)


def main():
    pins = json.loads((HERE / "SOURCE_PINS.json").read_text())
    verify_sources(pins)
    late_pins = json.loads((HERE / "LATE_SOURCE_PINS.json").read_text())
    verify_sources(late_pins, "late_inputs")
    artifacts = json.loads((HERE / "CHECKER_PINS.json").read_text())
    verify_artifacts(artifacts)

    source_root = str(HERE / "inputs")
    late_root = str(HERE / "late_inputs")
    commands = [
        ("book_binding", "check_binding.py", "RESULT.json", ["--repo", source_root]),
        ("input_price", "check_input_obstruction.py", "RESULT.json", [source_root]),
        ("paid_source", "check_saddle_and_weak_source.py", "RESULT.json", [source_root]),
        ("clock_bracket", "check_clock_bracket.py", "RESULT.json", []),
        ("clock_bracket", "check_frame_compensation.py", "FRAME_RESULT.json", [source_root]),
        ("late_application", "check_coframe_residual.py", "RESULT.json", [source_root, late_root]),
    ]
    env = os.environ.copy()
    env["OPENBLAS_NUM_THREADS"] = "1"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    receipts = {}
    for lane, script, result_file, args in commands:
        completed = subprocess.run(
            [sys.executable, str(HERE / lane / script), *args],
            cwd=HERE, env=env, text=True, capture_output=True, timeout=180, check=True,
        )
        require(not completed.stderr.strip(), f"Unexpected stderr in {lane}: {completed.stderr}")
        actual = json.loads(completed.stdout)
        expected = json.loads((HERE / lane / result_file).read_text())
        same_receipt(actual, expected, lane + "/" + script)
        receipts[lane + "/" + script] = {
            "replay": "PASS",
            "expected_sha256": hashlib.sha256(
                (HERE / lane / result_file).read_bytes()).hexdigest(),
        }

    verify_sources(pins)
    verify_sources(late_pins, "late_inputs")
    verify_artifacts(artifacts)

    import importlib.metadata
    environment = {name: importlib.metadata.version(name)
                   for name in ("numpy", "scipy", "sympy")}
    environment["python"] = platform.python_version()

    print(json.dumps({
        "status": "PASS_BOUNDED_VARIATIONAL_SELECTION_AND_NATIVE_CLOCK_SYNTHESIS",
        "scientific_input_ref": pins["input_ref"],
        "late_application_input_ref": late_pins["input_ref"],
        "environment": environment,
        "frozen_source_files": len(pins["sources"]),
        "frozen_late_source_files": len(late_pins["sources"]),
        "reviewed_artifacts_checked": len(artifacts["sha256"]),
        "receipt_rule": "Exact types, keys, integers, strings and Decimal/rational strings; binary float diagnostics rel5e-12 abs5e-13",
        "lanes": receipts,
        "scope": {
            "analytical_proofs_replaced_by_fixtures": False,
            "physical_Book_selection_proved": False,
            "complete_native_controller_selection_proved": False,
            "finite_all42_roots_for_full_nonlinear_price_proved": False,
            "physical_clock_and_canonical_constraint_algebra_proved": False,
            "GR_closed": False,
        },
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
