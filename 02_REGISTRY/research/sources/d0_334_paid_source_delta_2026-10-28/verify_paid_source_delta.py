#!/usr/bin/env python3
"""Verify the pinned PR #334 paid-source documents, inputs, and replay outputs."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import stat
import sys

PACKET = "02_REGISTRY/research/sources/d0_334_paid_source_delta_2026-10-28"
SOURCE_HEAD = "172876cdf38bfce6f87fdd4a059d524b60c10eb9"
BASE_HEAD = "c80d3dd2a917bbb2db2e2b1ab61d5216877c05e6"
MANIFEST_SHA256 = "4f0e2ba213465f65505ae55de15a75746146f42fa1784cdb32b00a9f59f27776"
EXTRACTED_CHECKS_SHA256 = "c84e960629a31345fb20828cfbd3efdf654bdf0348ad19e67f0a151a03866a15"
REPLAY_RECEIPT_SHA256 = "ea86b852195a9aaf9b24ce140c98828c65d3dfdd37be8aa3be65a3fa06fe354b"


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
            "Pinned upstream manifest SHA-256 mismatch")
    manifest = json.loads(manifest_data)
    require(manifest["source_commit"] == SOURCE_HEAD, "Unexpected source commit")
    require(manifest["base_source_commit"] == BASE_HEAD, "Unexpected base source commit")
    require(manifest["file_count"] == len(manifest["files"]) == 2,
            "Unexpected upstream source file count")
    observed = []
    upstream_paths = set()
    for item in manifest["files"]:
        path = f"{PACKET}/{item['snapshot_path']}"
        upstream_paths.add(item["snapshot_path"])
        data = read_file(root, path)
        digest = hashlib.sha256(data).hexdigest()
        blob = git_blob_sha1(data)
        require(len(data) == item["bytes"], f"Byte-count mismatch: {path}")
        require(digest == item["sha256"], f"SHA-256 mismatch: {path}")
        require(blob == item["git_blob"], f"Git blob mismatch: {path}")
        observed.append({"path": item["snapshot_path"], "bytes": len(data),
                         "sha256": digest, "git_blob": blob})
    actual_upstream_paths = set()
    for path in (root / PACKET / "upstream").rglob("*"):
        mode = path.lstat().st_mode
        if stat.S_ISDIR(mode):
            continue
        require(stat.S_ISREG(mode), f"Expected regular upstream file: {path}")
        actual_upstream_paths.add(path.relative_to(root / PACKET).as_posix())
    require(actual_upstream_paths == upstream_paths,
            "Unmanifested or missing upstream source files")

    extracted_path = f"{PACKET}/EXTRACTED_CHECKS.json"
    extracted_data = read_file(root, extracted_path)
    require(hashlib.sha256(extracted_data).hexdigest() == EXTRACTED_CHECKS_SHA256,
            "Pinned extracted-check manifest SHA-256 mismatch")
    extracted = json.loads(extracted_data)
    require(extracted["source_commit"] == SOURCE_HEAD, "Extracted checks use another source commit")
    input_count = 0
    for item in extracted["replay_input_files"]:
        path = f"{PACKET}/{item['snapshot_path']}"
        data = read_file(root, path)
        require(len(data) == item["bytes"], f"Replay input byte-count mismatch: {path}")
        require(hashlib.sha256(data).hexdigest() == item["sha256"],
                f"Replay input SHA-256 mismatch: {path}")
        require(git_blob_sha1(data) == item["git_blob"], f"Replay input Git blob mismatch: {path}")
        input_count += 1
    require(input_count == 7, "Unexpected replay input count")

    receipt_path = f"{PACKET}/replay/receipt.json"
    receipt_data = read_file(root, receipt_path)
    require(hashlib.sha256(receipt_data).hexdigest() == REPLAY_RECEIPT_SHA256,
            "Pinned replay receipt SHA-256 mismatch")
    receipt = json.loads(receipt_data)
    require(receipt["source_commit"] == SOURCE_HEAD, "Replay uses another source commit")
    require(receipt["status"] ==
            "PASS_ALL_THREE_CONTROLS_NORMAL_AND_OPTIMIZED_BYTE_IDENTICAL_TO_PUBLISHED_RESULTS",
            "Replay receipt does not record all controls passing")
    require(len(extracted["extracted_checks"]) == len(receipt["checks"]) == 3,
            "Unexpected embedded checker count")
    for source, check in zip(extracted["extracted_checks"], receipt["checks"]):
        require(source["script"] == check["script"], "Embedded-check receipt order/name mismatch")
        script_data = read_file(root, f"{PACKET}/replay/scripts/{source['script']}")
        expected_data = read_file(root, f"{PACKET}/replay/expected/{source['result']}")
        require(len(script_data) == source["script_bytes"], "Embedded checker byte-count mismatch")
        require(hashlib.sha256(script_data).hexdigest() == source["script_sha256"],
                "Embedded checker source SHA-256 mismatch")
        require(len(expected_data) == source["result_bytes"], "Published result byte-count mismatch")
        require(hashlib.sha256(expected_data).hexdigest() == source["result_sha256"],
                "Published result SHA-256 mismatch")
        require(check["status"] == json.loads(expected_data)["status"],
                "Replay result status differs from embedded published result")
        require(len(check["modes"]) == 2, "Missing normal or optimized replay")
        mode_hashes = set()
        for mode in check["modes"]:
            require(mode["exit_code"] == 0 and mode["matches_published_result_bytes"],
                    "A recorded checker replay did not match the published bytes")
            output_path = f"{PACKET}/replay/observed/{source['script']}.{mode['mode']}.json"
            output_data = read_file(root, output_path)
            digest = hashlib.sha256(output_data).hexdigest()
            require(digest == mode["stdout_sha256"], f"Replay output SHA-256 mismatch: {output_path}")
            require(output_data == expected_data, f"Replay output differs from published result: {output_path}")
            mode_hashes.add(digest)
        require(len(mode_hashes) == 1, "Ordinary and optimized replay outputs differ")

    return {
        "status": "PASS_PINNED_PAID_SOURCE_AND_REPLAY_BYTES",
        "base_source_commit": BASE_HEAD,
        "source_commit": SOURCE_HEAD,
        "upstream_files": observed,
        "replay_input_count": input_count,
        "replayed_checker_count": len(receipt["checks"]),
        "replay_modes": ["ordinary", "optimized"],
        "source_code_executed_by_verifier": False,
        "scientific_acceptance": False,
    }


def main() -> int:
    try:
        if len(sys.argv) > 2:
            raise ValueError("Usage: verify_paid_source_delta.py [repository-root]")
        root = Path(sys.argv[1]) if len(sys.argv) == 2 else Path(__file__).resolve().parents[4]
        print(json.dumps(verify(root), ensure_ascii=False, sort_keys=True, indent=2))
        return 0
    except (KeyError, OSError, TypeError, ValueError) as exc:
        print(f"FAIL_PAID_SOURCE_DELTA: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
