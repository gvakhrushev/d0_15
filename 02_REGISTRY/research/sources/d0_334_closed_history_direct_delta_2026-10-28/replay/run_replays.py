#!/usr/bin/env python3
"""Replay the three pinned #334 checkers and retain machine-local outputs."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


PACKAGE = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def copy_replay_inputs(temp_root: Path, manifest: dict) -> None:
    for row in manifest["replay_inputs"]:
        rel = Path(row["source_path"])
        source = PACKAGE / row["snapshot_path"]
        target = temp_root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(source.read_bytes())


def run_json(command: list[str], cwd: Path) -> tuple[dict, bytes, bytes]:
    completed = subprocess.run(command, cwd=cwd, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, check=False)
    if completed.returncode != 0:
        raise RuntimeError(
            f"command failed ({completed.returncode}): {command!r}\n"
            + completed.stderr.decode("utf-8", errors="replace")[-4000:]
        )
    try:
        result = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"checker stdout is not JSON: {command!r}") from exc
    return result, completed.stdout, completed.stderr


def check_7cx(actual: dict, expected: dict) -> bool:
    if actual.get("status") != "PASS":
        raise RuntimeError("7cx checker did not pass its internal assertions")
    for key in ("source_owner", "source_owner_sha256", "dimension", "carrier", "scope"):
        if actual.get(key) != expected.get(key):
            raise RuntimeError(f"7cx invariant differs from the pinned record: {key}")
    errors = actual["matrix_identity_errors"]
    if max(errors.values()) >= 1e-11:
        raise RuntimeError("7cx matrix identity residual exceeded 1e-11")
    if max(actual["echo_KdaggerK_equals_Fpower_errors"]) >= 1e-11:
        raise RuntimeError("7cx echo residual exceeded 1e-11")
    if max(actual["normalized_odd_state_derivative_norms_theta_nu"]) >= 1e-9:
        raise RuntimeError("7cx normalized-state derivative residual exceeded 1e-9")
    if max(actual["odd_unnormalized_derivative_errors_theta_nu"]) >= 1e-9:
        raise RuntimeError("7cx unnormalized-state derivative residual exceeded 1e-9")
    if max(actual["joint_mu_formula_errors"]) >= 1e-14:
        raise RuntimeError("7cx joint-probability formula residual exceeded 1e-14")
    if max(actual["joint_mu_derivative_fd_errors_theta_nu"]) >= 1e-9:
        raise RuntimeError("7cx finite-difference derivative residual exceeded 1e-9")
    for item in actual["feedback_sources_and_tails"]:
        if not item["spectral_tail_bound"] >= 0 or not item["roundoff_allowance"] >= 0:
            raise RuntimeError("7cx reported a negative tail allowance")
    return actual == expected


def run_all(output_dir: Path | None) -> dict:
    manifest = load_json(PACKAGE / "MANIFEST.json")
    sympy_version = importlib.metadata.version("sympy")
    if sympy_version != "1.14.0":
        raise RuntimeError(f"7cy/direct replay requires SymPy 1.14.0, found {sympy_version}")
    uv = shutil.which("uv")
    if uv is None:
        raise RuntimeError("7cx replay requires uv to provide Python 3.12 and NumPy 2.0.2")

    observed = {}
    with tempfile.TemporaryDirectory(prefix="d0-pr334-closed-history-") as temporary:
        temp_root = Path(temporary)
        copy_replay_inputs(temp_root, manifest)

        expected_7cx = load_json(PACKAGE / "replay/expected/7cx.json")
        script_7cx = PACKAGE / "replay/scripts/check_7cx.py"
        actual_7cx, stdout_7cx, stderr_7cx = run_json([
            uv, "run", "--quiet", "--python", "3.12", "--with", "numpy==2.0.2",
            str(script_7cx), str(temp_root),
        ], temp_root)
        exact_7cx = check_7cx(actual_7cx, expected_7cx)
        warning_lines = [line for line in stderr_7cx.decode("utf-8", errors="replace").splitlines()
                         if "RuntimeWarning:" in line]
        observed["7cx"] = {
            "status": "PASS_INTERNAL_TOLERANCE_CHECKS",
            "matches_embedded_json_exactly": exact_7cx,
            "python": "3.12 (uv)",
            "numpy": "2.0.2",
            "runtime_warning_lines": len(warning_lines),
            "stdout": stdout_7cx,
            "stderr": stderr_7cx,
            "result": actual_7cx,
        }

        expected_7cy = load_json(PACKAGE / "replay/expected/7cy.json")
        script_7cy = PACKAGE / "replay/scripts/check_7cy.py"
        actual_7cy, stdout_7cy, stderr_7cy = run_json([
            sys.executable, str(script_7cy),
        ], temp_root)
        if actual_7cy != expected_7cy:
            raise RuntimeError("7cy output differs from the embedded exact result")
        observed["7cy"] = {
            "status": actual_7cy["status"],
            "matches_embedded_json_exactly": True,
            "python": sys.version.split()[0],
            "sympy": sympy_version,
            "stdout": stdout_7cy,
            "stderr": stderr_7cy,
            "result": actual_7cy,
        }

        direct_rel = next(
            row["source_path"] for row in manifest["changed_owner_files"]
            if row["source_path"].endswith("a4d_closed_history_direct_source_check.py")
        )
        direct_result_rel = next(
            row["source_path"] for row in manifest["changed_owner_files"]
            if row["source_path"].endswith("a4d_closed_history_direct_source_result_2026_10_28.json")
        )
        direct_bytes = (PACKAGE / "upstream" / direct_rel).read_bytes()
        direct_path = temp_root / direct_rel
        direct_path.parent.mkdir(parents=True, exist_ok=True)
        direct_path.write_bytes(direct_bytes)
        expected_direct = load_json(PACKAGE / "upstream" / direct_result_rel)
        actual_direct, stdout_direct, stderr_direct = run_json([
            sys.executable, str(direct_path),
        ], temp_root)
        if actual_direct != expected_direct:
            raise RuntimeError("direct-source output differs from the pinned exact result")
        observed["direct_source"] = {
            "status": actual_direct["status"],
            "matches_embedded_json_exactly": True,
            "python": sys.version.split()[0],
            "sympy": sympy_version,
            "stdout": stdout_direct,
            "stderr": stderr_direct,
            "result": actual_direct,
        }

    receipt = {
        "schema": "d0-pr334-closed-history-replay-receipt-v1",
        "source_head": manifest["source_range"]["head_commit"],
        "python39_runner": sys.version,
        "sympy": sympy_version,
        "checkers": {},
        "scope": {"Lean_theorem_added": False, "physical_admission": False,
                  "GR_closed": False},
    }
    for name, item in observed.items():
        receipt["checkers"][name] = {
            key: value for key, value in item.items() if key not in ("stdout", "stderr", "result")
        }
        receipt["checkers"][name]["stdout_sha256"] = sha256(item["stdout"])
        receipt["checkers"][name]["stderr_sha256"] = sha256(item["stderr"])
        receipt["checkers"][name]["result"] = item["result"]

    if output_dir is not None:
        output_dir.mkdir(parents=True, exist_ok=False)
        for name, item in observed.items():
            stem = "direct_source" if name == "direct_source" else name
            (output_dir / f"{stem}.stdout.json").write_bytes(item["stdout"])
            (output_dir / f"{stem}.stderr.txt").write_bytes(item["stderr"])
        (output_dir / "receipt.json").write_text(
            json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path,
                        help="new directory for exact stdout/stderr and the replay receipt")
    args = parser.parse_args()
    receipt = run_all(args.output_dir)
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
