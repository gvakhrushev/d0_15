#!/usr/bin/env python3
"""Replay the pinned PR #334 full-source and final-composition checkers."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from tempfile import TemporaryDirectory


PACKET = "02_REGISTRY/research/sources/d0_334_final_composition_delta_2026-10-28"
SOURCE_PREFIX = "02_REGISTRY/research/sources"
NATIVE_REL = "02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py"
NATIVE_SHA256 = "222eafaffa4b30f175919a32c940534b82f3a2b9af89c7897d318dd004a2007c"
NUMERIC_TOLERANCE = 3e-12

CHECKS = (
    ("clock", "d0_clock_winding_source_2026-10-28/check_clock_winding.py",
     "d0_clock_winding_source_2026-10-28/result.json"),
    ("query", "d0_native_final_composition_2026-10-28/check_query_stationarity.py",
     "d0_native_final_composition_2026-10-28/QUERY_RESULT.json"),
    ("gauge", "d0_native_final_composition_2026-10-28/check_gauge_moment.py",
     "d0_native_final_composition_2026-10-28/GAUGE_RESULT.json"),
    ("memory", "d0_native_final_composition_2026-10-28/check_retained_memory.py",
     "d0_native_final_composition_2026-10-28/MEMORY_RESULT.json"),
    ("terminal", "d0_native_final_composition_2026-10-28/check_terminal_graph.py",
     "d0_native_final_composition_2026-10-28/TERMINAL_RESULT.json"),
    ("phase", "d0_native_final_composition_2026-10-28/check_phase_descent.py",
     "d0_native_final_composition_2026-10-28/PHASE_RESULT.json"),
    ("native_phase", "d0_native_final_composition_2026-10-28/phase_native_check.py",
     "d0_native_final_composition_2026-10-28/NATIVE_PHASE_RESULT.json"),
)


def repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "00_WORK" / "manifest.json").is_file():
            return parent
    raise RuntimeError("Cannot locate repository root")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def compare_intersection(expected, actual, path: str = "$") -> float:
    """Compare shared receipt fields; source receipts may add wrapper fields."""
    if isinstance(expected, bool) or isinstance(actual, bool):
        if expected != actual:
            raise ValueError(f"Boolean differs at {path}")
        return 0.0
    if isinstance(expected, (int, float)) and isinstance(actual, (int, float)):
        delta = abs(float(expected) - float(actual))
        if delta > NUMERIC_TOLERANCE:
            raise ValueError(f"Numeric difference at {path} exceeds tolerance: {delta}")
        return delta
    if type(expected) is not type(actual):
        raise ValueError(f"Type differs at {path}")
    if isinstance(expected, dict):
        return max((compare_intersection(expected[k], actual[k], f"{path}.{k}")
                    for k in set(expected).intersection(actual)), default=0.0)
    if isinstance(expected, list):
        if len(expected) != len(actual):
            raise ValueError(f"List length differs at {path}")
        return max((compare_intersection(left, right, f"{path}[{i}]")
                    for i, (left, right) in enumerate(zip(expected, actual))), default=0.0)
    if expected != actual:
        raise ValueError(f"Value differs at {path}: {expected!r} != {actual!r}")
    return 0.0


def package_version(name: str) -> str:
    module = __import__(name)
    return str(getattr(module, "__version__", "unknown"))


def main() -> None:
    root = repo_root()
    packet = root / PACKET
    manifest = json.loads((packet / "MANIFEST.json").read_text(encoding="utf-8"))
    native_input = (root / "02_REGISTRY/research/sources/d0_334_paid_source_delta_2026-10-28"
                    / "replay/inputs" / NATIVE_REL)
    native_bytes = native_input.read_bytes()
    if sha256(native_bytes) != NATIVE_SHA256:
        raise ValueError("Pinned native_execution.py input digest mismatch")

    receipt = {
        "schema": "d0-pr-source-replay-v1",
        "repository": "gvakhrushev/d0_15",
        "owner_pr": 334,
        "base_source_commit": manifest["base_source_commit"],
        "source_commit": manifest["source_commit"],
        "native_execution_sha256": NATIVE_SHA256,
        "replay_runner_sha256": sha256(Path(__file__).read_bytes()),
        "python": sys.version.split()[0],
        "dependencies": {name: package_version(name)
                         for name in ("sympy", "numpy", "scipy", "mpmath")},
        "numeric_tolerance": NUMERIC_TOLERANCE,
        "normal_optimized_byte_identical": True,
        "stderr_empty_all_modes": True,
        "stderr_warning_counts": {},
        "scientific_acceptance": False,
        "physical_admission": False,
        "GR_closed": False,
        "checks": [],
    }

    with TemporaryDirectory(prefix="d0-pr334-final-replay-") as temporary:
        scratch = Path(temporary)
        native_target = scratch / NATIVE_REL
        native_target.parent.mkdir(parents=True, exist_ok=True)
        native_target.write_bytes(native_bytes)

        for name, script_rel, expected_rel in CHECKS:
            script = packet / "upstream" / SOURCE_PREFIX / script_rel
            expected_path = packet / "upstream" / SOURCE_PREFIX / expected_rel
            expected = json.loads(expected_path.read_text(encoding="utf-8"))
            script_sha = sha256(script.read_bytes())
            outputs: list[bytes] = []
            modes = []

            for mode in ("ordinary", "optimized"):
                command = [sys.executable]
                if mode == "optimized":
                    command.append("-O")
                command.append(str(script))
                if name == "memory":
                    command.extend(("--repo", str(scratch)))
                result = subprocess.run(command, cwd=scratch, capture_output=True,
                                        text=True, timeout=600, check=False)
                if result.returncode != 0:
                    raise RuntimeError(f"{name}/{mode} exited {result.returncode}: "
                                       f"{result.stderr[-1000:]}")
                try:
                    actual = json.loads(result.stdout)
                except json.JSONDecodeError as error:
                    raise RuntimeError(f"{name}/{mode} did not emit JSON") from error
                if actual.get("status") != expected.get("status"):
                    raise RuntimeError(f"{name}/{mode} status differs from source receipt")
                for flag in ("GR_closed", "physical_action_selection_proved",
                             "physical_admission_asserted"):
                    if flag in actual and actual[flag] is not False:
                        raise RuntimeError(f"{name}/{mode} promotes scope flag {flag}")
                if actual.get("native_owner_sha256", NATIVE_SHA256) != NATIVE_SHA256:
                    raise RuntimeError(f"{name}/{mode} uses an unexpected native input")

                maximum_delta = compare_intersection(expected, actual)
                stdout = result.stdout.encode("utf-8")
                stderr = result.stderr.encode("utf-8")
                observed_dir = packet / "replay" / "observed"
                observed_dir.mkdir(parents=True, exist_ok=True)
                (observed_dir / f"{name}.{mode}.json").write_bytes(stdout)
                (observed_dir / f"{name}.{mode}.stderr.txt").write_bytes(stderr)
                receipt["stderr_empty_all_modes"] &= not stderr
                warning_messages = re.findall(
                    r"RuntimeWarning: ([^\n]+)", result.stderr
                )
                for message in warning_messages:
                    receipt["stderr_warning_counts"][message] = (
                        receipt["stderr_warning_counts"].get(message, 0) + 1
                    )
                outputs.append(stdout)
                modes.append({
                    "mode": mode,
                    "exit_code": result.returncode,
                    "stdout_bytes": len(stdout),
                    "stdout_sha256": sha256(stdout),
                    "stderr_bytes": len(stderr),
                    "stderr_sha256": sha256(stderr),
                    "published_result_intersection_max_numeric_delta": maximum_delta,
                })

            same = outputs[0] == outputs[1]
            receipt["normal_optimized_byte_identical"] &= same
            if not same:
                raise RuntimeError(f"ordinary and optimized output differ for {name}")
            receipt["checks"].append({
                "name": name,
                "script": script_rel,
                "script_sha256": script_sha,
                "published_result": expected_rel,
                "published_result_sha256": sha256(expected_path.read_bytes()),
                "published_status": expected.get("status"),
                "observed_status": json.loads(outputs[0])["status"],
                "modes": modes,
            })
            print(f"PASS {name}: {expected.get('status')}; ordinary and -O byte-identical",
                  flush=True)

    if not receipt["stderr_empty_all_modes"]:
        require_counts = {
            "divide by zero encountered in matmul": 2,
            "invalid value encountered in matmul": 2,
            "overflow encountered in matmul": 2,
        }
        if receipt["stderr_warning_counts"] != require_counts:
            raise RuntimeError("Unexpected stderr warnings; inspect the observed replay files")
        if any(check["name"] != "clock" and
               any(mode["stderr_bytes"] for mode in check["modes"])
               for check in receipt["checks"]):
            raise RuntimeError("A non-clock checker emitted stderr")
    receipt["status"] = (
        "PASS_ALL_SEVEN_CHECKERS" if receipt["stderr_empty_all_modes"] else
        "PASS_ALL_SEVEN_CHECKERS_WITH_NUMPY_RUNTIME_WARNINGS"
    )
    receipt_path = packet / "replay" / "receipt.json"
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2,
                                       sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": receipt["status"],
        "receipt_sha256": sha256(receipt_path.read_bytes()),
        "stderr_empty_all_modes": receipt["stderr_empty_all_modes"],
        "stderr_warning_counts": receipt["stderr_warning_counts"],
        "normal_optimized_byte_identical": receipt["normal_optimized_byte_identical"],
        "python": receipt["python"],
        "dependencies": receipt["dependencies"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
