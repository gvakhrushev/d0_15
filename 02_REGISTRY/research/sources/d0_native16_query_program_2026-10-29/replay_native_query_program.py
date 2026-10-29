#!/usr/bin/env python3
"""Verify and replay the pinned #334 §7dy native QUERY programme."""
from __future__ import annotations

import hashlib
import json
import platform
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parents[3]
OWNER_MEMO = (
    "02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_"
    "2026_10_20.md"
)
SOURCE_MANIFEST = PACKAGE / "source_manifest.json"
REPLAY_MANIFEST = PACKAGE / "replay_manifest.json"
REPLAY = PACKAGE / "replay"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def record(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": sha(data)}


def verify_file(path: Path, expected: dict[str, object]) -> None:
    if record(path) != {"bytes": expected["bytes"], "sha256": expected["sha256"]}:
        raise SystemExit(f"pinned file mismatch: {path}")


def tagged(data: bytes, tag: str, language: str) -> bytes:
    opening = f"<!-- BEGIN {tag} -->\n```{language}\n".encode()
    closing = f"```\n<!-- END {tag} -->".encode()
    if data.count(opening) != 1 or data.count(closing) != 1:
        raise SystemExit(f"missing or duplicate owner block: {tag}")
    return data.split(opening, 1)[1].split(closing, 1)[0]


def verify_manifest(manifest: dict[str, object]) -> None:
    for rel, expected in manifest["artifacts"].items():
        verify_file(PACKAGE / rel, expected)

    owner = manifest["upstream"]
    section = (PACKAGE / owner["section_file"]).read_bytes()
    task = (PACKAGE / owner["task_excerpt_file"]).read_bytes()
    checker = (PACKAGE / owner["checker_file"]).read_bytes()
    receipt = (PACKAGE / owner["receipt_file"]).read_bytes()
    if sha(section) != owner["section_sha256"]:
        raise SystemExit("pinned §7dy source section changed")
    if sha(task) != owner["task_excerpt_sha256"]:
        raise SystemExit("pinned §7dy task excerpt changed")
    if tagged(section, "7dy NATIVE QUERY PROGRAM CHECKER", "python") != checker:
        raise SystemExit("checker is not the exact embedded §7dy block")
    if tagged(section, "7dy NATIVE QUERY PROGRAM RECEIPT", "json") != receipt:
        raise SystemExit("receipt is not the exact embedded §7dy block")

    inputs = manifest["runtime_inputs"]
    for rel, expected in inputs.items():
        path = ROOT / rel
        if not path.is_file() or sha(path.read_bytes()) != expected["sha256"]:
            raise SystemExit(f"runtime source pin changed: {rel}")

    prior = manifest["prior_intake"]
    prior_root = ROOT / prior["path"]
    prior_manifest_bytes = (prior_root / "source_manifest.json").read_bytes()
    if sha(prior_manifest_bytes) != prior["source_manifest_sha256"]:
        raise SystemExit("prior intake source manifest changed")
    prior_manifest = json.loads(prior_manifest_bytes)
    for rel, expected in prior["artifacts"].items():
        verify_file(PACKAGE / rel, expected)
        source_record = prior_manifest["artifacts"].get(expected["source_artifact"])
        if source_record is None:
            raise SystemExit(f"prior intake has no pinned source artifact: {rel}")
        if {"bytes": source_record["bytes"], "sha256": source_record["sha256"]} != {
            "bytes": expected["bytes"], "sha256": expected["sha256"]
        }:
            raise SystemExit(f"prior intake source changed: {rel}")


def main() -> int:
    manifest_bytes = SOURCE_MANIFEST.read_bytes()
    manifest = json.loads(manifest_bytes)
    verify_manifest(manifest)

    base = (PACKAGE / "inputs/upstream_receipts.md").read_bytes()
    section_dw = (PACKAGE / "inputs/upstream_section_7dw.md").read_bytes()
    section_dx = (PACKAGE / "inputs/upstream_section_7dx.md").read_bytes()
    section_dy = (PACKAGE / "upstream_section_7dy.md").read_bytes()
    paper = base + b"\n" + section_dw + b"\n" + section_dx + b"\n" + section_dy
    expected = (PACKAGE / "expected_receipt_7dy.json").read_bytes()
    checker = PACKAGE / "check_native_query_program.py"
    REPLAY.mkdir(parents=True, exist_ok=True)

    run_records: dict[str, dict[str, object]] = {}
    outputs: list[bytes] = []
    with tempfile.TemporaryDirectory(prefix="d0-native16-query-program-") as temp:
        scratch = Path(temp)
        paper_path = scratch / OWNER_MEMO
        paper_path.parent.mkdir(parents=True, exist_ok=True)
        paper_path.write_bytes(paper)
        for rel in manifest["runtime_inputs"]:
            destination = scratch / rel
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / rel, destination)

        for mode, flags in (("ordinary", ()), ("optimized", ("-O",)), ("repeat", ())):
            result = subprocess.run(
                [sys.executable, "-B", *flags, str(checker)],
                cwd=scratch, capture_output=True, check=False,
            )
            if result.returncode != 0:
                raise SystemExit(
                    f"{mode} checker failed ({result.returncode}): "
                    f"{result.stderr.decode(errors='replace')}"
                )
            if result.stderr:
                raise SystemExit(f"{mode} checker wrote to stderr")
            if result.stdout != expected:
                raise SystemExit(f"{mode} output differs from pinned owner receipt")
            decoded = json.loads(result.stdout)
            if decoded.get("status") != "PASS" or decoded.get("checks") != 156:
                raise SystemExit(f"{mode} returned unexpected status or check count")
            if decoded.get("scope", {}).get("GR_closed") is not False:
                raise SystemExit("§7dy receipt must retain GR_closed=false")

            stem = f"{mode}"
            (REPLAY / f"{stem}_stdout.json").write_bytes(result.stdout)
            (REPLAY / f"{stem}_stderr.txt").write_bytes(result.stderr)
            outputs.append(result.stdout)
            run_records[stem] = {
                "returncode": result.returncode,
                "stdout": record(REPLAY / f"{stem}_stdout.json"),
                "stderr": record(REPLAY / f"{stem}_stderr.txt"),
                "matches_owner_receipt": True,
                "checks": decoded["checks"],
            }

    if not (outputs[0] == outputs[1] == outputs[2]):
        raise SystemExit("ordinary, optimized and repeat outputs differ")
    replay_manifest = {
        "schema": "d0-native16-query-program-replay-v1",
        "status": "PASS",
        "owner_commit": manifest["upstream"]["commit"],
        "owner_memo_blob": manifest["upstream"]["memo_blob"],
        "owner_task_blob": manifest["upstream"]["task_blob"],
        "python": platform.python_version(),
        "source_manifest_sha256": sha(manifest_bytes),
        "replay_wrapper_sha256": sha(Path(__file__).read_bytes()),
        "owner_receipts_byte_identical_in_ordinary_optimized_repeat": True,
        "stderr_empty_for_all_runs": True,
        "runs": run_records,
    }
    REPLAY_MANIFEST.write_text(json.dumps(replay_manifest, indent=2, sort_keys=True) + "\n")
    print(json.dumps(replay_manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
