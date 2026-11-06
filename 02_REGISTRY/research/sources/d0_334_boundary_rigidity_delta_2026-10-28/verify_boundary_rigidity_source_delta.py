#!/usr/bin/env python3
"""Verify the exact source bytes and replay receipt for the PR #334 delta."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import stat
import sys

PACKET = "02_REGISTRY/research/sources/d0_334_boundary_rigidity_delta_2026-10-28"
SOURCE_HEAD = "c80d3dd2a917bbb2db2e2b1ab61d5216877c05e6"
BASE_HEAD = "c4a92cb0f2326bf7ae2a8127c49f5b65ea71ce5a"
MANIFEST_SHA256 = "55144fe548f0e743e148192e2594449d14f89067d08e516bcefb42344acb6999"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def read_file(root: Path, relative: str) -> bytes:
    require(stat.S_ISDIR(root.lstat().st_mode), f"Expected real repository directory: {root}")
    current = root
    parts = relative.split("/")
    require(parts and all(p not in ("", ".", "..") and "\\" not in p for p in parts),
            f"Unsafe source path: {relative}")
    for part in parts[:-1]:
        current = current / part
        require(stat.S_ISDIR(current.lstat().st_mode), f"Expected real directory: {current}")
    target = current / parts[-1]
    require(stat.S_ISREG(target.lstat().st_mode), f"Expected regular file: {target}")
    return target.read_bytes()


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def verify(root: Path) -> dict[str, object]:
    root = Path(root)
    manifest_path = f"{PACKET}/MANIFEST.json"
    manifest_data = read_file(root, manifest_path)
    require(hashlib.sha256(manifest_data).hexdigest() == MANIFEST_SHA256,
            "Pinned manifest SHA-256 mismatch")
    manifest = json.loads(manifest_data)
    require(manifest["source_commit"] == SOURCE_HEAD, "Unexpected source commit")
    require(manifest["base_source_commit"] == BASE_HEAD, "Unexpected base source commit")
    files = manifest["files"]
    require(manifest["file_count"] == len(files) == 21, "Unexpected source file count")
    observed = []
    expected_paths = set()
    for item in files:
        path = f"{PACKET}/{item['snapshot_path']}"
        expected_paths.add(item["snapshot_path"])
        data = read_file(root, path)
        digest = hashlib.sha256(data).hexdigest()
        blob = git_blob_sha1(data)
        require(len(data) == item["bytes"], f"Byte-count mismatch: {path}")
        require(digest == item["sha256"], f"SHA-256 mismatch: {path}")
        require(blob == item["git_blob"], f"Git blob mismatch: {path}")
        observed.append({"path": item["snapshot_path"], "bytes": len(data),
                         "sha256": digest, "git_blob": blob})
    upstream_root = root / PACKET / "upstream"
    actual_paths = set()
    for path in upstream_root.rglob("*"):
        mode = path.lstat().st_mode
        if stat.S_ISDIR(mode):
            continue
        require(stat.S_ISREG(mode), f"Expected regular source file: {path}")
        actual_paths.add(path.relative_to(root / PACKET).as_posix())
    require(actual_paths == expected_paths, "Unmanifested or missing upstream source files")
    total_bytes = sum(x["bytes"] for x in observed)
    return {
        "status": "PASS_PINNED_BOUNDARY_RIGIDITY_SOURCE_BYTES",
        "base_source_commit": BASE_HEAD,
        "source_commit": SOURCE_HEAD,
        "file_count": len(observed),
        "total_bytes": total_bytes,
        "manifest_sha256": MANIFEST_SHA256,
        "files": observed,
        "local_replay_receipt": f"{PACKET}/replay/receipt.json",
        "source_code_executed_by_verifier": False,
        "scientific_acceptance": False,
    }


def main() -> int:
    try:
        if len(sys.argv) > 2:
            raise ValueError("Usage: verify_boundary_rigidity_source_delta.py [repository-root]")
        root = Path(sys.argv[1]) if len(sys.argv) == 2 else Path(__file__).resolve().parents[4]
        print(json.dumps(verify(root), ensure_ascii=False, sort_keys=True, indent=2))
        return 0
    except (KeyError, OSError, TypeError, ValueError) as exc:
        print(f"FAIL_BOUNDARY_RIGIDITY_SOURCE: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
