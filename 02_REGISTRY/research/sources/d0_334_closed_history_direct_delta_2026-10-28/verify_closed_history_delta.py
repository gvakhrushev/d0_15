#!/usr/bin/env python3
"""Verify the immutable, non-executing PR #334 closed-history source packet."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob_sha1(data: bytes) -> str:
    header = b"blob " + str(len(data)).encode("ascii") + b"\0"
    return hashlib.sha1(header + data).hexdigest()


def verify(root: Path = ROOT) -> dict:
    root = root.resolve()
    manifest_path = root / "MANIFEST.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("schema") != "d0-pr334-closed-history-direct-source-delta-v1":
        raise ValueError("Unknown source packet manifest schema")

    rows = manifest.get("snapshot_files")
    if not isinstance(rows, list):
        raise ValueError("Missing snapshot_files inventory")
    expected_files = {}
    for row in rows:
        rel = row.get("path")
        if not isinstance(rel, str) or Path(rel).is_absolute() or ".." in Path(rel).parts:
            raise ValueError(f"Unsafe snapshot path: {rel!r}")
        if rel in expected_files:
            raise ValueError(f"Duplicate snapshot path: {rel}")
        expected_files[rel] = row
    actual_files = {}
    for path in root.rglob("*"):
        if path.is_symlink():
            raise ValueError(f"Symlink in source packet: {path.relative_to(root)}")
        if path.is_file() and path != manifest_path:
            rel = path.relative_to(root).as_posix()
            actual_files[rel] = path
    if set(actual_files) != set(expected_files):
        missing = sorted(set(expected_files) - set(actual_files))
        extra = sorted(set(actual_files) - set(expected_files))
        raise ValueError(f"Snapshot file set mismatch; missing={missing}; extra={extra}")

    for rel, path in sorted(actual_files.items()):
        data = path.read_bytes()
        record = expected_files[rel]
        if len(data) != record["size_bytes"] or sha256(data) != record["sha256"]:
            raise ValueError(f"Snapshot digest mismatch: {rel}")

    for section in ("changed_owner_files", "replay_inputs"):
        for record in manifest[section]:
            rel = record["snapshot_path"]
            data = actual_files[rel].read_bytes()
            if git_blob_sha1(data) != record["head_blob"]:
                raise ValueError(f"Git blob pin mismatch: {rel}")

    for record in manifest["embedded_replays"]:
        for key, sha_key in (("script_path", "source_code_sha256"),
                             ("expected_result_path", "expected_result_sha256")):
            rel = record[key]
            if sha256(actual_files[rel].read_bytes()) != record[sha_key]:
                raise ValueError(f"Embedded replay pin mismatch: {rel}")

    return {
        "status": "PASS_PINNED_PR334_CLOSED_HISTORY_DELTA",
        "source_head": manifest["source_range"]["head_commit"],
        "changed_owner_files": len(manifest["changed_owner_files"]),
        "pinned_replay_inputs": len(manifest["replay_inputs"]),
        "embedded_replays": len(manifest["embedded_replays"]),
        "snapshot_files": len(expected_files),
        "actual_git_object_store_checked": False,
        "source_code_executed": False,
        "scientific_acceptance": False,
        "Lean_theorem_added": False,
        "physical_admission": False,
        "GR_closed": False,
    }


def main() -> int:
    print(json.dumps(verify(), sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
