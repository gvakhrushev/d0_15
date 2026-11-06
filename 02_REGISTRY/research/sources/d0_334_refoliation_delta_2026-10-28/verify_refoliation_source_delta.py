#!/usr/bin/env python3
"""Verify the literal four-file PR #334 refoliation source snapshot."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import stat
import sys

SOURCE_HEAD = "c4a92cb0f2326bf7ae2a8127c49f5b65ea71ce5a"
PACKET = "02_REGISTRY/research/sources/d0_334_refoliation_delta_2026-10-28"
EXPECTED = {
    f"{PACKET}/upstream/A4D_ROOT_CUT_TO_REFOLIATION_CLOSURE_2026_10_28.md":
        ("d0af048a5ebaf91b02a98cbf27d8faee69592908f7669c446963cbf712fe2125", "9f8bf5574179073c297eb8ecbd3616984e5c56a8"),
    f"{PACKET}/upstream/PROOF_RU.md":
        ("6155eb31068ffeeb72439dcb9860bd3b82dbd3072fbc2b75a1fe91276d2be71a", "03ad9147c46411099667658871f847e9f3bee883"),
    f"{PACKET}/upstream/check_refoliation_closure.py":
        ("d2b83484e840b91e62b8ac2af4155d5fd8c8e5748ee3027f6cbea0b19263da33", "615e2b2a0421e11485c9f15497edaa47fd2b37e1"),
    f"{PACKET}/upstream/result.json":
        ("3b13c4146e3fdb3990572ac56db837d2badaf22794eca78ce7f72f159d791204", "334ab85094699082a71fa56db4c089c6a28e9e76"),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def read_pinned_file(root: Path, relative: str) -> bytes:
    require(stat.S_ISDIR(root.lstat().st_mode), f"Expected real repository directory: {root}")
    current = root
    parts = relative.split("/")
    require(parts and all(part not in ("", ".", "..") and "\\" not in part for part in parts),
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
    files = []
    for path, (expected_sha256, expected_blob) in EXPECTED.items():
        data = read_pinned_file(Path(root), path)
        sha256 = hashlib.sha256(data).hexdigest()
        blob = git_blob_sha1(data)
        require(sha256 == expected_sha256, f"SHA-256 mismatch: {path}")
        require(blob == expected_blob, f"Git blob ID mismatch: {path}")
        files.append({"path": path, "bytes": len(data), "sha256": sha256, "git_blob": blob})
    return {
        "status": "PASS_PINNED_REFOLIATION_SOURCE_BYTES",
        "source_commit": SOURCE_HEAD,
        "files": files,
        "file_count": len(files),
        "actual_git_object_store_checked": False,
        "source_code_executed": False,
        "scientific_acceptance": False,
    }


def main() -> int:
    try:
        if len(sys.argv) > 2:
            raise ValueError("Usage: verify_refoliation_source_delta.py [repository-root]")
        root = Path(sys.argv[1]) if len(sys.argv) == 2 else Path(__file__).resolve().parents[4]
        print(json.dumps(verify(root), sort_keys=True, indent=2))
        return 0
    except (OSError, TypeError, ValueError) as exc:
        print(f"FAIL_REFOLIATION_SOURCE: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
