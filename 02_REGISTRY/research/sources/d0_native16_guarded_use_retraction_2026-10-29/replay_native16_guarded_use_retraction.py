#!/usr/bin/env python3
"""Replay the exact #334 §7dw and §7dx checkers against pinned source blocks."""
from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
PACKAGE = Path(__file__).resolve().parent
OWNER_MEMO = (
    "02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_"
    "2026_10_20.md"
)
SOURCE_MANIFEST = PACKAGE / "source_manifest.json"
REPLAY_MANIFEST = PACKAGE / "replay_manifest.json"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_record(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": sha(data)}


def verify_artifact(path: Path, expected: dict[str, object]) -> None:
    actual = file_record(path)
    if actual != {"bytes": expected["bytes"], "sha256": expected["sha256"]}:
        raise SystemExit(f"artifact mismatch: {path.relative_to(PACKAGE)}")


def tagged(data: bytes, tag: str, language: str) -> bytes:
    opening = f"<!-- BEGIN {tag} -->\n```{language}\n".encode()
    closing = f"```\n<!-- END {tag} -->".encode()
    if data.count(opening) != 1 or data.count(closing) != 1:
        raise SystemExit(f"missing or duplicate source block: {tag}")
    return data.split(opening, 1)[1].split(closing, 1)[0]


def verify_source_manifest(manifest: dict[str, object]) -> None:
    for rel, expected in manifest["artifacts"].items():
        verify_artifact(PACKAGE / rel, expected)
    for key, record in manifest["upstream"].items():
        for field in ("section_file", "task_excerpt_file", "checker_file", "receipt_file"):
            expected = manifest["artifacts"][record[field]]
            verify_artifact(PACKAGE / record[field], expected)
        section = (PACKAGE / record["section_file"]).read_bytes()
        checker = (PACKAGE / record["checker_file"]).read_bytes()
        receipt = (PACKAGE / record["receipt_file"]).read_bytes()
        checker_tag, receipt_tag = {
            "7dw": ("7dw SAME USE RECORD GUARD CHECKER", "7dw SAME USE RECORD GUARD RECEIPT"),
            "7dx": ("7dx GUARD COTANGENT RETRACTION CHECKER", "7dx GUARD COTANGENT RETRACTION RECEIPT"),
        }[key]
        if tagged(section, checker_tag, "python") != checker:
            raise SystemExit(f"checker extraction differs from pinned §{key}")
        if tagged(section, receipt_tag, "json") != receipt:
            raise SystemExit(f"receipt extraction differs from pinned §{key}")


def main() -> int:
    manifest_bytes = SOURCE_MANIFEST.read_bytes()
    manifest = json.loads(manifest_bytes)
    verify_source_manifest(manifest)

    dependency_pins = {
        "02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py":
            "222eafaffa4b30f175919a32c940534b82f3a2b9af89c7897d318dd004a2007c",
        "02_REGISTRY/research/sources/d0_clock_winding_source_2026-10-28/PROOF_RU.md":
            "ff430c80b070d03b2d6860603575b1898394334775177d9d15feb54179fe4418",
    }
    for rel, expected in dependency_pins.items():
        if sha((ROOT / rel).read_bytes()) != expected:
            raise SystemExit(f"consumed input hash mismatch: {rel}")

    base_receipts = (PACKAGE / "inputs/upstream_receipts.md").read_bytes()
    section_dw = (PACKAGE / "upstream_section_7dw.md").read_bytes()
    section_dx = (PACKAGE / "upstream_section_7dx.md").read_bytes()
    paper = base_receipts + b"\n" + section_dw + b"\n" + section_dx

    run_records: dict[str, dict[str, object]] = {}
    with tempfile.TemporaryDirectory(prefix="d0-native16-retraction-") as temp:
        temp_root = Path(temp)
        paper_path = temp_root / OWNER_MEMO
        paper_path.parent.mkdir(parents=True, exist_ok=True)
        paper_path.write_bytes(paper)
        for rel in dependency_pins:
            target = temp_root / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.symlink_to((ROOT / rel).resolve())

        for key, record in manifest["upstream"].items():
            expected = (PACKAGE / record["receipt_file"]).read_bytes()
            checker = PACKAGE / record["checker_file"]
            modes = {
                "ordinary": [sys.executable, str(checker)],
                "optimized": [sys.executable, "-O", str(checker)],
                "repeat": [sys.executable, str(checker)],
            }
            outputs = []
            for mode, argv in modes.items():
                result = subprocess.run(argv, cwd=temp_root, capture_output=True, check=False)
                if result.returncode != 0:
                    raise SystemExit(
                        f"§{key} {mode} failed with exit {result.returncode}: "
                        f"{result.stderr.decode(errors='replace')}"
                    )
                if result.stderr:
                    raise SystemExit(f"§{key} {mode} wrote to stderr")
                if result.stdout != expected:
                    raise SystemExit(f"§{key} {mode} output differs from owner receipt")
                outputs.append(result.stdout)
                stem = f"{key}_{mode}"
                (PACKAGE / "replay" / f"{stem}_stdout.json").write_bytes(result.stdout)
                (PACKAGE / "replay" / f"{stem}_stderr.txt").write_bytes(result.stderr)
                run_records[stem] = {
                    "returncode": result.returncode,
                    "stdout": file_record(PACKAGE / "replay" / f"{stem}_stdout.json"),
                    "stderr": file_record(PACKAGE / "replay" / f"{stem}_stderr.txt"),
                    "matches_owner_receipt": True,
                }
            if not (outputs[0] == outputs[1] == outputs[2]):
                raise SystemExit(f"§{key} ordinary, optimized and repeat outputs differ")

    replay_manifest = {
        "schema": "d0-native16-guarded-use-source-retraction-replay-v1",
        "status": "PASS",
        "python": platform.python_version(),
        "source_manifest_sha256": sha(manifest_bytes),
        "replay_wrapper_sha256": sha(Path(__file__).read_bytes()),
        "consumed_input_sha256": dependency_pins,
        "owner_receipts_byte_identical_in_ordinary_optimized_repeat": True,
        "stderr_empty_for_all_runs": True,
        "runs": run_records,
    }
    REPLAY_MANIFEST.write_text(json.dumps(replay_manifest, indent=2, sort_keys=True) + "\n")
    print(json.dumps(replay_manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
