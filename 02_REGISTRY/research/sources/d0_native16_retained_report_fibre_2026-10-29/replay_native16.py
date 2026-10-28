#!/usr/bin/env python3
"""Replay the byte-preserved #334 native16 checker from the pinned inputs."""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
CHECKER = HERE / "check_native16.py"
EXPECTED = HERE / "expected_receipt.json"
RECEIPT_FIXTURE = HERE / "inputs" / "upstream_receipts.md"
REPLAY = HERE / "replay"
PAPER_REL = Path(
    "02_REGISTRY/research/"
    "A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md"
)
INPUT_PROOFS = (
    "d0_task_faithful_source_2026-10-28/PROOF_RU.md",
    "d0_apparatus_cotangent_descent_2026-10-28/PROOF_RU.md",
    "d0_canonical_stationary_family_2026-10-28/PROOF_RU.md",
    "d0_clock_winding_source_2026-10-28/PROOF_RU.md",
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    REPLAY.mkdir(parents=True, exist_ok=True)
    expected_bytes = EXPECTED.read_bytes()
    expected = json.loads(expected_bytes)
    outputs: list[bytes] = []
    run_rows = []

    with tempfile.TemporaryDirectory(prefix="d0-native16-retained-report-") as temp:
        scratch = Path(temp)
        paper = scratch / PAPER_REL
        paper.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(RECEIPT_FIXTURE, paper)

        for rel in INPUT_PROOFS:
            source = ROOT / "02_REGISTRY/research/sources" / rel
            if not source.is_file():
                raise FileNotFoundError(source)
            target = scratch / "02_REGISTRY/research/sources" / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)

        for label, flags in (
            ("ordinary", ()),
            ("optimized", ("-O",)),
            ("repeat", ()),
        ):
            completed = subprocess.run(
                [sys.executable, *flags, "-B", str(CHECKER)],
                cwd=scratch,
                capture_output=True,
                check=False,
            )
            if completed.returncode:
                raise RuntimeError(
                    f"{label} checker exited {completed.returncode}: "
                    f"{completed.stderr.decode('utf-8', errors='replace')}"
                )
            (REPLAY / f"{label}_stdout.json").write_bytes(completed.stdout)
            (REPLAY / f"{label}_stderr.log").write_bytes(completed.stderr)
            if completed.stderr:
                raise RuntimeError(f"{label} checker wrote to stderr")
            outputs.append(completed.stdout)
            result = json.loads(completed.stdout)
            run_rows.append({
                "mode": label,
                "returncode": completed.returncode,
                "stdout_bytes": len(completed.stdout),
                "stdout_sha256": sha256(completed.stdout),
                "stderr_bytes": len(completed.stderr),
                "status": result.get("status"),
                "checks": result.get("checks"),
                "runtime": result.get("runtime"),
            })

    if not outputs[0] == outputs[1] == outputs[2]:
        raise AssertionError("ordinary, -O, and repeated checker outputs differ")

    actual = json.loads(outputs[0])
    if actual.get("status") != "PASS" or actual.get("checks") != 288:
        raise AssertionError("the exact upstream checker did not report PASS/288")
    if actual.get("checker_sha256") != expected.get("checker_sha256"):
        raise AssertionError("the checker bytes differ from the pinned receipt")
    if actual.get("input_pins") != expected.get("input_pins"):
        raise AssertionError("an upstream checker input does not match its pin")

    runtime_matches = actual.get("runtime") == expected.get("runtime")
    if runtime_matches:
        if outputs[0] != expected_bytes:
            raise AssertionError("the exact author-runtime receipt differs")
    else:
        actual_without_runtime = dict(actual)
        expected_without_runtime = dict(expected)
        actual_without_runtime.pop("runtime", None)
        expected_without_runtime.pop("runtime", None)
        if actual_without_runtime != expected_without_runtime:
            raise AssertionError("the replay differs beyond the runtime version")

    manifest = {
        "schema": "d0-native16-retained-report-fibre-replay-v1",
        "status": "PASS",
        "checks": 288,
        "checker_sha256": sha256(CHECKER.read_bytes()),
        "expected_receipt_sha256": sha256(expected_bytes),
        "replay_outputs_byte_identical": True,
        "exact_published_receipt_match": outputs[0] == expected_bytes,
        "runtime_matches_published_receipt": runtime_matches,
        "runtime": actual.get("runtime"),
        "runs": run_rows,
        "stderr_empty_for_all_runs": True,
        "scope": actual.get("scope"),
        "remaining": actual.get("remaining"),
        "GR_closed": actual.get("remaining", {}).get("GR_closed"),
    }
    (HERE / "replay_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
