#!/usr/bin/env python3
"""Read-only verifier for the pinned PR #334 retained-history source delta."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import stat


PACKET = "02_REGISTRY/research/sources/d0_334_retained_history_full_delta_2026-10-28"
MANIFEST_SHA256 = "e0629d69d9e82cda9d2b90871a2f52ededb430604085bc3e58ffb2aa6932f5e6"
RECEIPT_SHA256 = "bba210497913e9b70dc9aa0bcafc0da45b3e5dffa5098878ffeba1af2378b210"
BASE_HEAD = "46ebed17ddfa04faa8ab1a07a6a822b717f993ef"
SOURCE_HEAD = "716387e3cb4c9ff08c44b5ac532db882ee1e394a"
SOURCE_COMMITS = [
    "39b9c847dbea952016a0f464e786ad817e96d4ad",
    "110b672e09848893475db0c8fd786cc910a014f9",
    "716387e3cb4c9ff08c44b5ac532db882ee1e394a",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def read_file(root: Path, relative: str) -> bytes:
    parts = relative.split("/")
    require(parts and all(part not in ("", ".", "..") and "\\" not in part
                          for part in parts), f"Unsafe path: {relative}")
    current = root
    for part in parts[:-1]:
        current = current / part
        require(stat.S_ISDIR(current.lstat().st_mode), f"Expected directory: {current}")
    target = current / parts[-1]
    require(stat.S_ISREG(target.lstat().st_mode), f"Expected regular file: {target}")
    return target.read_bytes()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob_sha1(data: bytes) -> str:
    header = b"blob " + str(len(data)).encode("ascii") + b"\0"
    return hashlib.sha1(header + data).hexdigest()


def verify(root: Path) -> dict[str, object]:
    root = Path(root)
    manifest_bytes = read_file(root, f"{PACKET}/MANIFEST.json")
    require(sha256(manifest_bytes) == MANIFEST_SHA256, "Manifest SHA-256 mismatch")
    manifest = json.loads(manifest_bytes)
    require(manifest["schema"] == "d0-pr-source-delta-v1", "Unexpected manifest schema")
    require(manifest["owner_pr"] == 334 and manifest["base_source_commit"] == BASE_HEAD and
            manifest["source_commit"] == SOURCE_HEAD and
            [item["sha"] for item in manifest["source_commits"]] == SOURCE_COMMITS,
            "Unexpected source owner or commit range")
    require(manifest["file_count"] == len(manifest["files"]) == 7,
            "Unexpected artifact inventory size")

    upstream_snapshots = set()
    observed = []
    for entry in manifest["files"]:
        path = entry["snapshot_path"]
        data = read_file(root, f"{PACKET}/{path}")
        require(len(data) == entry["bytes"], f"Byte-count mismatch: {path}")
        require(sha256(data) == entry["sha256"], f"SHA-256 mismatch: {path}")
        require(git_blob_sha1(data) == entry["git_blob"], f"Git blob mismatch: {path}")
        observed.append(path)
        if path.startswith("upstream/"):
            upstream_snapshots.add(path)
    actual_upstream = set()
    upstream_root = root / PACKET / "upstream"
    for path in upstream_root.rglob("*"):
        mode = path.lstat().st_mode
        if stat.S_ISDIR(mode):
            continue
        require(stat.S_ISREG(mode), f"Expected regular upstream file: {path}")
        actual_upstream.add(path.relative_to(root / PACKET).as_posix())
    require(actual_upstream == upstream_snapshots, "Unmanifested upstream source or missing snapshot")

    receipt_bytes = read_file(root, f"{PACKET}/replay/receipt.json")
    require(sha256(receipt_bytes) == RECEIPT_SHA256, "Replay receipt SHA-256 mismatch")
    receipt = json.loads(receipt_bytes)
    require(receipt["base_source_commit"] == BASE_HEAD and
            receipt["source_commit"] == SOURCE_HEAD and
            receipt["source_commits"] == SOURCE_COMMITS,
            "Replay receipt uses another source range")
    require(receipt["status"] == "PASS_ORIGINAL_RETAINED_HISTORY_SOURCE" and
            receipt["checks"] == 163, "Pinned source checker did not pass")
    require(receipt["normal_optimized_stdout_byte_identical"] is True and
            receipt["normal_optimized_stderr_byte_identical"] is True,
            "Normal and optimized runs differ")
    require(receipt["runtime_warning_lines"] == 102 and receipt["runtime_warning_counts"] == {
        "divide by zero encountered in matmul": 34,
        "invalid value encountered in matmul": 34,
        "overflow encountered in matmul": 34,
    }, "Unexpected numerical warning inventory")
    require(receipt["scope_flags"] == {
        "GR_closed": False,
        "new_action_or_decoder": False,
        "original_42_field_source_transport_proved": False,
        "large_full_history_heat_replayed": False,
        "Lean_or_repository_CI_run": False,
    }, "Scientific scope was promoted")

    return {
        "status": "PASS_PINNED_RETAINED_HISTORY_SOURCE_DELTA",
        "owner_pr": 334,
        "base_source_commit": BASE_HEAD,
        "source_commit": SOURCE_HEAD,
        "artifact_files": len(observed),
        "upstream_source_snapshots": len(upstream_snapshots),
        "checker_status": receipt["status"],
        "checker_controls": receipt["checks"],
        "runtime_warning_lines_retained": receipt["runtime_warning_lines"],
        "normal_optimized_outputs_identical": True,
        "scientific_acceptance": False,
        "physical_admission": False,
        "GR_closed": False,
    }


def main() -> None:
    root = next((parent for parent in Path(__file__).resolve().parents
                 if (parent / "00_WORK" / "manifest.json").is_file()), None)
    require(root is not None, "Cannot locate repository root")
    print(json.dumps(verify(root), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
