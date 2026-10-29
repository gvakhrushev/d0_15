#!/usr/bin/env python3
"""Replay and preserve the exact #334 record-saturated field-stencil checker."""
from __future__ import annotations

import hashlib
import importlib.metadata
import json
import math
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
CHECKER = HERE / "check_record_saturated_field.py"
REPLAY = HERE / "replay"
OWNER_COMMIT = "418afd58c741713a60036a90f8246060d774fd56"
OWNER_BRANCH = "exp/a4d-joint-response-continuation-2026-10-16"
OWNER_PATH = (
    "02_REGISTRY/research/sources/"
    "d0_record_saturated_native_field_2026-10-29/"
    "check_record_saturated_field.py"
)
OWNER_BLOB = "81d78ce6ebcc3e9d98bceaacbd61ed0328943da9"
OWNER_CHECKER_SHA256 = "618d1d6267739e7468fea7c0108be22cff448c8d9abac28110081854ca502b65"
INPUT_COMMIT = "4b30fcb4dc743e7a04415c9701aae19a847e8dab"
EXPECTED_CHECKS = 867


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _finite(value: object) -> bool:
    if isinstance(value, float):
        return math.isfinite(value)
    if isinstance(value, dict):
        return all(_finite(item) for item in value.values())
    if isinstance(value, list):
        return all(_finite(item) for item in value)
    return True


def _write_exact(path: Path, data: bytes) -> None:
    if path.exists() and path.read_bytes() != data:
        raise FileExistsError(f"refusing to replace different saved evidence: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def _artifact_record(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": sha256(data)}


def main() -> None:
    CHECKER_BYTES = CHECKER.read_bytes()
    if sha256(CHECKER_BYTES) != OWNER_CHECKER_SHA256:
        raise AssertionError("local checker is not byte-identical to the pinned #334 source")
    blob = subprocess.check_output(
        ["git", "rev-parse", f"{OWNER_COMMIT}:{OWNER_PATH}"], cwd=ROOT, text=True
    ).strip()
    if blob != OWNER_BLOB:
        raise AssertionError("#334 source blob does not match its recorded pin")
    subprocess.run(
        ["git", "merge-base", "--is-ancestor", INPUT_COMMIT, OWNER_COMMIT],
        cwd=ROOT, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
    )

    REPLAY.mkdir(parents=True, exist_ok=True)
    stdout_by_mode: list[bytes] = []
    stderr_by_mode: list[bytes] = []
    outputs_by_mode: list[dict[str, bytes]] = []
    runs: list[dict[str, object]] = []

    with tempfile.TemporaryDirectory(prefix="d0-record-saturated-field-") as temp:
        scratch = Path(temp)
        for label, flags in (("ordinary", ()), ("optimized", ("-O",)), ("repeat", ())):
            outdir = scratch / label
            completed = subprocess.run(
                [sys.executable, *flags, "-B", str(CHECKER), "--out", str(outdir)],
                cwd=ROOT,
                capture_output=True,
                check=False,
            )
            if completed.returncode:
                raise RuntimeError(
                    f"{label} checker exited {completed.returncode}: "
                    f"{completed.stderr.decode('utf-8', errors='replace')}"
                )
            try:
                summary = json.loads(completed.stdout)
                result_bytes = (outdir / "result.json").read_bytes()
                programmes_bytes = (outdir / "programmes.json").read_bytes()
                result = json.loads(result_bytes)
                programmes = json.loads(programmes_bytes)
            except (OSError, json.JSONDecodeError) as error:
                raise RuntimeError(f"{label} replay omitted valid JSON outputs") from error
            if summary.get("status") != "PASS_NATIVE_RECORD_SATURATED_42_SOURCE_STENCILS":
                raise AssertionError(f"{label} checker status changed: {summary}")
            if summary.get("checks") != EXPECTED_CHECKS or result.get("checks") != EXPECTED_CHECKS:
                raise AssertionError(f"{label} checker did not complete {EXPECTED_CHECKS} checks")
            if summary.get("GR_closed") is not False or result.get("GR_closed") is not False:
                raise AssertionError("the checker must retain GR_closed=false")
            if result.get("checker_sha256") != OWNER_CHECKER_SHA256:
                raise AssertionError("generated receipt does not identify the pinned checker")
            if not _finite(summary) or not _finite(result) or not _finite(programmes):
                raise AssertionError(f"{label} replay produced a non-finite JSON number")

            stdout_path = REPLAY / f"{label}_stdout.json"
            stderr_path = REPLAY / f"{label}_stderr.log"
            _write_exact(stdout_path, completed.stdout)
            _write_exact(stderr_path, completed.stderr)
            stdout_by_mode.append(completed.stdout)
            stderr_by_mode.append(completed.stderr)
            outputs_by_mode.append({"result.json": result_bytes, "programmes.json": programmes_bytes})
            warning_categories = re.findall(
                rb"RuntimeWarning: ([^\r\n]+)", completed.stderr
            )
            runs.append({
                "mode": label,
                "command_flags": list(flags),
                "returncode": completed.returncode,
                "stdout_bytes": len(completed.stdout),
                "stdout_sha256": sha256(completed.stdout),
                "stderr_bytes": len(completed.stderr),
                "stderr_sha256": sha256(completed.stderr),
                "runtime_warning_lines": len(warning_categories),
                "runtime_warning_categories": sorted({
                    item.decode("utf-8", errors="replace") for item in warning_categories
                }),
                "result_sha256": sha256(result_bytes),
                "programmes_sha256": sha256(programmes_bytes),
                "checks": result["checks"],
                "status": result["status"],
            })

    stdout_identical = stdout_by_mode[0] == stdout_by_mode[1] == stdout_by_mode[2]
    result_identical = all(
        outputs_by_mode[0][name] == outputs_by_mode[i][name]
        for i in (1, 2) for name in ("result.json", "programmes.json")
    )
    if not stdout_identical or not result_identical:
        raise AssertionError("ordinary, -O and repeat outputs differ")

    for name, data in outputs_by_mode[0].items():
        _write_exact(HERE / name, data)

    runtime = {name: importlib.metadata.version(name)
               for name in ("numpy", "scipy", "sympy", "mpmath")}
    runtime["python"] = sys.version.split()[0]
    warning_present = any(stderr_by_mode)
    replay_manifest = {
        "schema": "d0-record-saturated-native-field-replay-v1",
        "status": "PASS_WITH_CAPTURED_RUNTIME_WARNINGS" if warning_present else "PASS",
        "checker_status": "PASS_NATIVE_RECORD_SATURATED_42_SOURCE_STENCILS",
        "checks": EXPECTED_CHECKS,
        "checker_sha256": OWNER_CHECKER_SHA256,
        "owner_commit": OWNER_COMMIT,
        "owner_blob": OWNER_BLOB,
        "input_commit_pin": INPUT_COMMIT,
        "input_pin_is_ancestor_of_owner_commit": True,
        "runtime": runtime,
        "stdout_identical_across_modes": stdout_identical,
        "generated_json_identical_across_modes": result_identical,
        "stderr_empty_for_all_runs": not warning_present,
        "stderr_identical_across_modes": stderr_by_mode[0] == stderr_by_mode[1] == stderr_by_mode[2],
        "warnings_resolved": not warning_present,
        "warning_note": (
            "The local NumPy/BLAS run emits captured RuntimeWarnings (divide by zero, "
            "overflow, invalid value) during matrix multiplication. The checker exits "
            "successfully and its JSON outputs are finite, but this replay does not "
            "establish that the warnings are harmless."
            if warning_present else ""
        ),
        "runs": runs,
        "result_sha256": sha256((HERE / "result.json").read_bytes()),
        "programmes_sha256": sha256((HERE / "programmes.json").read_bytes()),
        "result_metrics": {
            "max_coordinate_error": json.loads((HERE / "result.json").read_bytes())
                ["stencil"]["max_coordinate_error"],
            "dual_max_norm_error": json.loads((HERE / "result.json").read_bytes())
                ["stencil"]["dual_max_norm_error"],
            "dual_max_norm_proved_bound": json.loads((HERE / "result.json").read_bytes())
                ["stencil"]["dual_max_norm_proved_bound"],
            "programmes": json.loads((HERE / "result.json").read_bytes())
                ["stencil"]["programmes"],
            "expanded_calls_per_word": json.loads((HERE / "result.json").read_bytes())
                ["stencil"]["expanded_calls_per_word"],
        },
        "scope": {
            "Lean_or_CI_run": False,
            "runtime_field_reader_implemented": False,
            "physical_variation_domain_derived": False,
            "all42_mesh_root_proved": False,
            "GR_closed": False,
        },
    }
    replay_bytes = (json.dumps(replay_manifest, indent=2, sort_keys=True) + "\n").encode()
    (HERE / "replay_manifest.json").write_bytes(replay_bytes)

    integrated_paths = [
        "PROOF_RU.md", "check_record_saturated_field.py", "replay_record_saturated_field.py",
        "result.json", "programmes.json", "replay_manifest.json",
        *(f"replay/{label}_{suffix}" for label in ("ordinary", "optimized", "repeat")
          for suffix in ("stdout.json", "stderr.log")),
    ]
    source_manifest = {
        "schema": "d0-record-saturated-native-field-intake-v1",
        "upstream": {
            "pull_request": 334,
            "branch": OWNER_BRANCH,
            "commit": OWNER_COMMIT,
            "path": OWNER_PATH,
            "blob": OWNER_BLOB,
            "sha256": OWNER_CHECKER_SHA256,
            "commit_title": "test(#334): compile actual record-saturated Golden words and bound all42 source stencils",
            "upstream_result_receipt_in_commit": False,
        },
        "input": {
            "commit": INPUT_COMMIT,
            "is_ancestor_of_owner_commit": True,
            "meaning": "checker PIN: fixed Golden/native16 source configuration",
        },
        "integrated_artifacts": {
            rel: _artifact_record(HERE / rel) for rel in integrated_paths
        },
        "replay": {
            "manifest": "replay_manifest.json",
            "status": replay_manifest["status"],
            "warning_resolved": replay_manifest["warnings_resolved"],
            "GR_closed": False,
        },
        "scope": {
            "phase": "native realization supporting calculation",
            "parent_substitution": (
                "A fixed-Golden, retained-record finite stencil compares the complete "
                "native source against the declared 42 pointwise Palatini-coordinate "
                "derivatives for one configured field point."
            ),
            "remaining": [
                "resolve or reproduce without the captured local NumPy RuntimeWarnings",
                "derive the admitted physical variation domain and runtime field compiler",
                "prove all42 mesh/root and refinement transport",
                "bind complete selected Book03 Cost-Info, clock and boundary equations",
                "Lean formalization and CI",
                "physical selection and GR closure",
            ],
            "GR_closed": False,
        },
    }
    source_bytes = (json.dumps(source_manifest, indent=2, sort_keys=True) + "\n").encode()
    (HERE / "source_manifest.json").write_bytes(source_bytes)
    print(replay_bytes.decode("utf-8"), end="")


if __name__ == "__main__":
    main()
