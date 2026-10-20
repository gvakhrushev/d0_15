#!/usr/bin/env python3
"""Read-only replay of the bounded global mathematical composition."""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
TOLERANCE = 2e-11


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def verify_pins():
    manifest = json.loads((HERE / "SHA256SUMS.json").read_text())
    for name, expected in manifest["files"].items():
        actual = hashlib.sha256((HERE / name).read_bytes()).hexdigest()
        require(actual == expected, "Frozen packet input changed: " + name)
    return len(manifest["files"])


def compare(actual, expected, path):
    if isinstance(expected, float):
        require(type(actual) is float and math.isfinite(actual)
                and math.isfinite(expected)
                and abs(actual - expected) <= TOLERANCE,
                "Frozen numerical result differs: " + path)
    elif isinstance(expected, dict):
        require(isinstance(actual, dict) and actual.keys() == expected.keys(),
                "Frozen dictionary differs: " + path)
        for key in expected:
            compare(actual[key], expected[key], path + "/" + key)
    elif isinstance(expected, list):
        require(isinstance(actual, list) and len(actual) == len(expected),
                "Frozen result length differs: " + path)
        for index, (left, right) in enumerate(zip(actual, expected)):
            compare(left, right, path + "/" + str(index))
    else:
        require(type(actual) is type(expected) and actual == expected,
                "Frozen exact result differs: " + path)


def main():
    pin_count = verify_pins()
    sources = json.loads((HERE / "SOURCE_INPUTS.json").read_text())
    for item in sources["files"]:
        raw = (HERE / item["snapshot"]).read_bytes()
        require(len(raw) == item["bytes"], "Snapshot size changed")
        require(hashlib.sha256(raw).hexdigest() == item["sha256"],
                "Snapshot SHA changed: " + item["snapshot"])
        blob = b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw
        require(hashlib.sha1(blob).hexdigest() == item["git_blob"],
                "Original Git blob differs: " + item["snapshot"])

    frozen = json.loads((HERE / "FROZEN_REPLAY.json").read_text())["results"]
    summaries = {}
    for name in ("check_operational_curvature.py", "check_holonomy_source.py",
                 "check_full_price.py"):
        result = subprocess.run([sys.executable, "-B", "-O", str(HERE / name)],
                                cwd=HERE, text=True, capture_output=True,
                                check=False)
        require(result.returncode == 0,
                name + " failed:\n" + result.stdout + "\n" + result.stderr)
        require(not result.stderr, name + " emitted unexpected diagnostics")
        actual = json.loads(result.stdout)
        require(actual["status"] == "PASS", name + " did not pass")
        if name == "check_full_price.py":
            compare(actual, frozen[name], name)
            require(actual["maximum_observed_log_identity_error"] <= TOLERANCE,
                    "Complete-price logarithm identities exceed tolerance")
        else:
            require(actual == frozen[name], name + " exact result differs")
        summaries[name] = {"status": "PASS", "groups": len(actual["groups"])}
    require(verify_pins() == pin_count, "Packet changed during replay")
    print(json.dumps({
        "status": "PASS",
        "historical_snapshots": len(sources["files"]),
        "frozen_packet_pins": pin_count,
        "new_narrow_checks": summaries,
        "groups": sum(item["groups"] for item in summaries.values()),
        "tracked_expected_results_written": False,
        "old_scientific_suites_replayed_by_this_wrapper": False,
        "physical_GR_closed": False,
        "scope": "New operational reconstruction and complete-price composition; analytical quantified statements are independently reviewed.",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
