"""Replay the checks declared in TESTS.json in a temporary copy of the bundle."""
import hashlib
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def matches(actual, expected):
    if isinstance(expected, dict):
        return (isinstance(actual, dict) and actual.keys() == expected.keys()
                and all(matches(actual[k], v) for k, v in expected.items()))
    if isinstance(expected, list):
        return (isinstance(actual, list) and len(actual) == len(expected)
                and all(matches(a, b) for a, b in zip(actual, expected)))
    if isinstance(expected, float):
        return (type(actual) in (float, int) and
                math.isclose(actual, expected, rel_tol=1e-11, abs_tol=2e-14))
    return type(actual) is type(expected) and actual == expected


def main():
    root = Path(__file__).resolve().parent
    manifest = json.loads((root / "TESTS.json").read_text())
    for name, expected_digest in manifest["sha256"].items():
        actual_digest = hashlib.sha256((root / name).read_bytes()).hexdigest()
        if actual_digest != expected_digest:
            raise ValueError(f"File fingerprint mismatch: {name}")
    with tempfile.TemporaryDirectory(prefix="d0-heat-proof-") as temporary:
        temporary_root = Path(temporary)
        bundle = temporary_root / "proofs"
        shutil.copytree(root, bundle)
        working = temporary_root / "empty"
        working.mkdir()
        env = dict(os.environ, PYTHONPATH="", OPENBLAS_NUM_THREADS="1",
                   OMP_NUM_THREADS="1")
        for entry in manifest["checks"]:
            args = [str(bundle / x) if x.endswith(".py") else x
                    for x in entry["arguments"]]
            command = [sys.executable, "-I", "-B", str(bundle / entry["check"]), *args]
            run = subprocess.run(command, cwd=working, env=env,
                                 text=True, capture_output=True)
            if run.returncode:
                sys.stderr.write(run.stderr)
                raise RuntimeError(f"Check failed: {entry['check']}")
            expected = json.loads((bundle / entry["expected"]).read_text())
            if not matches(json.loads(run.stdout), expected):
                raise ValueError(f"Result differs: {entry['check']}")
            print("PASS", entry["check"], flush=True)


if __name__ == "__main__":
    main()
