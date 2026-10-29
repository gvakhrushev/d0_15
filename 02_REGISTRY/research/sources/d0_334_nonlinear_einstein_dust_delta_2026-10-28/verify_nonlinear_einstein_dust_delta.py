#!/usr/bin/env python3
"""Verify the pinned #334 nonlinear Einstein-dust delta and replay receipt."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import stat
import zipfile


PACKET = "02_REGISTRY/research/sources/d0_334_nonlinear_einstein_dust_delta_2026-10-28"
MANIFEST_SHA256 = "bf80589cfc1498a7f5236fc6aa49ea2aed2ea304bc48bff9067c514cee2c9806"
BASE_HEAD = "9f23ec82c8e4e044121521658afec4a5e9b8c2f7"
SOURCE_HEAD = "c296829fc2e74d673a2a679baa1e10a49524b290"
EXPECTED_COMMITS = [SOURCE_HEAD]
EXPECTED_UPSTREAM = {
    "02_REGISTRY/research/A4D_CLOSED_HISTORY_DIRECT_PROOF_2026_10_28.md",
    "02_REGISTRY/research/A4D_CLOSED_HISTORY_NONLINEAR_EINSTEIN_DUST_2026_10_28.md",
    "02_REGISTRY/research/certificates/a4d_closed_history_af_word_embedding_check.py",
    "02_REGISTRY/research/certificates/a4d_closed_history_af_word_embedding_result_2026_10_28.json",
    "02_REGISTRY/research/certificates/a4d_closed_history_nonlinear_dust_check.py",
    "02_REGISTRY/research/certificates/a4d_closed_history_nonlinear_dust_result_2026_10_28.json",
}
EXPECTED_CHECKS = {"nonlinear_dust": 19, "af_word_embedding": 24}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def read_regular(root: Path, relative: str) -> bytes:
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
    manifest_bytes = read_regular(root, f"{PACKET}/MANIFEST.json")
    require(sha256(manifest_bytes) == MANIFEST_SHA256, "Manifest SHA-256 mismatch")
    manifest = json.loads(manifest_bytes)
    require(manifest["schema"] == "d0-pr-source-application-delta-v1" and
            manifest["repository"] == "gvakhrushev/d0_15" and
            manifest["owner_pr"] == 334, "Unexpected source owner or schema")
    require(manifest["base_source_commit"] == BASE_HEAD and
            manifest["source_commit"] == SOURCE_HEAD and
            [item["sha"] for item in manifest["source_commits"]] == EXPECTED_COMMITS,
            "Unexpected source range")
    require({item["upstream_path"] for item in manifest["source_files"]
             if item["kind"] == "upstream_snapshot"} ==
            EXPECTED_UPSTREAM, "Unexpected upstream file inventory")
    require(manifest["changed_upstream_paths"] == sorted(EXPECTED_UPSTREAM),
            "Changed-path inventory differs from the source range")

    archive_meta = manifest["archive"]
    archive_path = f"{PACKET}/{archive_meta['path']}"
    archive_bytes = read_regular(root, archive_path)
    require(len(archive_bytes) == archive_meta["bytes"] and
            sha256(archive_bytes) == archive_meta["sha256"],
            "Source archive byte count or SHA-256 mismatch")
    with zipfile.ZipFile(root / archive_path) as archive:
        names = archive.namelist()
        expected_names = {item["archive_member"] for item in manifest["source_files"]}
        require(len(names) == len(set(names)) and set(names) == expected_names,
                "Archive contains duplicate, unmanifested or missing paths")
        contents = {}
        for item in manifest["source_files"]:
            data = archive.read(item["archive_member"])
            require(len(data) == item["bytes"] and
                    sha256(data) == item["sha256"] and
                    git_blob_sha1(data) == item["git_blob"],
                    f"Source snapshot mismatch: {item['archive_member']}")
            contents[item["upstream_path"]] = data

    replay_files = {}
    for item in manifest["local_replay_artifacts"]:
        data = read_regular(root, f"{PACKET}/{item['path']}")
        require(len(data) == item["bytes"] and sha256(data) == item["sha256"],
                f"Replay artifact mismatch: {item['path']}")
        replay_files[item["path"]] = data
    receipt_bytes = replay_files[manifest["local_replay_receipt_path"]]
    require(sha256(receipt_bytes) == manifest["local_replay_receipt_sha256"],
            "Local replay receipt SHA-256 mismatch")
    receipt = json.loads(receipt_bytes)
    require(receipt["source_head"] == SOURCE_HEAD and
            receipt["base_source_head"] == BASE_HEAD and
            receipt["input_commit_in_checker"] == manifest["owner_input_head"],
            "Replay receipt uses a different source input")
    require(receipt["environment"] == {"python": "3.9.6", "sympy": "1.14.0"},
            "Unexpected replay environment")
    require(receipt["scope"] == manifest["scope_flags"] and
            receipt["scope"]["GR_closed"] is False and
            receipt["scope"]["physical_admission"] is False,
            "Scientific scope was promoted")

    observed = {}
    for item in receipt["checkers"]:
        name = item["name"]
        require(name in EXPECTED_CHECKS and item["checks"] == EXPECTED_CHECKS[name],
                f"Unexpected checker result for {name}")
        script_bytes = contents[item["script_path"]]
        published = contents[item["published_result_path"]]
        require(sha256(script_bytes) == item["script_sha256"],
                f"Checker source hash mismatch: {name}")
        require(sha256(published) == item["published_result_sha256"] ==
                item["stdout_sha256"], f"Published result hash mismatch: {name}")
        result = json.loads(published)
        reported_count = result.get("checks_count", result.get("checks"))
        require(reported_count == item["checks"], f"Owner result check count mismatch: {name}")
        if name == "af_word_embedding":
            require(result["status"] == "PASS" and result["scope"].endswith(
                "no physical frame-addressability assertion"), "Unexpected AF scope")
        for mode in ("normal", "optimized"):
            out = replay_files[f"replay/observed/{name}.{mode}.stdout.json"]
            err = replay_files[f"replay/observed/{name}.{mode}.stderr.txt"]
            require(out == published and err == b"", f"Observed {mode} replay differs: {name}")
            observed[(name, mode)] = out
        require(item["normal_optimized_stdout_identical"] is True and
                item["normal_optimized_stderr_identical"] is True and
                item["stderr_bytes"] == 0 and
                observed[(name, "normal")] == observed[(name, "optimized")],
                f"Normal/optimized replay mismatch: {name}")
    require({item["name"] for item in receipt["checkers"]} == set(EXPECTED_CHECKS),
            "Missing replay checker")
    return {
        "status": "PASS_PINNED_NONLINEAR_EINSTEIN_DUST_DELTA_WITH_REPLAY",
        "owner_pr": 334,
        "source_commit": SOURCE_HEAD,
        "source_snapshots": len(EXPECTED_UPSTREAM),
        "local_checker_controls": sum(EXPECTED_CHECKS.values()),
        "normal_optimized_and_owner_outputs_match": True,
        "physical_admission": False,
        "scientific_acceptance": False,
        "GR_closed": False,
    }


def main() -> None:
    root = next((parent for parent in Path(__file__).resolve().parents
                 if (parent / "00_WORK" / "manifest.json").is_file()), None)
    require(root is not None, "Cannot locate repository root")
    print(json.dumps(verify(root), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
