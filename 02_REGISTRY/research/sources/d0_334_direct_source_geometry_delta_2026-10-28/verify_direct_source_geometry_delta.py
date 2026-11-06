#!/usr/bin/env python3
"""Verify the pinned #334 direct-source/geometry intake without running it."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import stat
import zipfile


PACKET = "02_REGISTRY/research/sources/d0_334_direct_source_geometry_delta_2026-10-28"
MANIFEST_SHA256 = "c2df40121a44f7ce7047d50c252305bea5f3a5f152aa5f85dd0ed61f6875f6da"
BASE_HEAD = "716387e3cb4c9ff08c44b5ac532db882ee1e394a"
SOURCE_HEAD = "9f23ec82c8e4e044121521658afec4a5e9b8c2f7"
EXPECTED_COMMITS = [
    "2b3d114479456d0c72078328b88ece9d89259ae8",
    "28f0443fca3df4b829f22497dea93253a97b27bb",
    "5140d2ab86a9b5829ccab1be32d11f367e4dca43",
    "9f23ec82c8e4e044121521658afec4a5e9b8c2f7",
]
EXPECTED_UPSTREAM = {
    "00_WORK/tasks/EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE.md",
    "02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md",
    "02_REGISTRY/research/A4D_ORIGINAL_RETAINED_HISTORY_DIRECT_SOURCE_2026_10_28.md",
    "02_REGISTRY/research/sources/d0_original_retained_history_source_2026-10-28/PROOF_RU.md",
    "02_REGISTRY/research/sources/d0_original_retained_history_source_2026-10-28/result.json",
}


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
    require(manifest["file_count"] == len(manifest["files"]) == 6,
            "Unexpected source artifact inventory")
    upstream_paths = {item["upstream_path"] for item in manifest["files"]
                      if item["kind"] == "upstream_snapshot"}
    require(upstream_paths == EXPECTED_UPSTREAM, "Unexpected upstream file inventory")
    require(manifest["changed_upstream_paths"] == sorted(EXPECTED_UPSTREAM),
            "Changed-path inventory differs from the source range")

    archive_meta = manifest["container"]
    archive_path = f"{PACKET}/{archive_meta['path']}"
    archive_bytes = read_regular(root, archive_path)
    require(len(archive_bytes) == archive_meta["bytes"] and
            sha256(archive_bytes) == archive_meta["sha256"],
            "Source archive byte count or SHA-256 mismatch")
    with zipfile.ZipFile(root / archive_path) as archive:
        names = archive.namelist()
        expected_names = {item["archive_member"] for item in manifest["files"]}
        require(len(names) == len(set(names)) and set(names) == expected_names,
                "Archive contains duplicate, unmanifested or missing paths")
        for item in manifest["files"]:
            data = archive.read(item["archive_member"])
            require(len(data) == item["bytes"],
                    f"Byte-count mismatch: {item['archive_member']}")
            require(sha256(data) == item["sha256"],
                    f"SHA-256 mismatch: {item['archive_member']}")
            require(git_blob_sha1(data) == item["git_blob"],
                    f"Git blob mismatch: {item['archive_member']}")
        result_item = next(item for item in manifest["files"]
                           if item["upstream_path"].endswith("/result.json"))
        result = json.loads(archive.read(result_item["archive_member"]))

    require(result["status"] == manifest["owner_receipt_status"] ==
            "PASS_ORIGINAL_RETAINED_HISTORY_SOURCE" and
            result["checks"] == manifest["owner_receipt_checks"] == 163,
            "The pinned owner receipt does not match the manifest")
    require(result["checker_sha256"] == manifest["retained_history_checker_sha256"] and
            result["input_commit"] == "46ebed17ddfa04faa8ab1a07a6a822b717f993ef",
            "Unexpected checker or checker input")
    require(manifest["scope_flags"] == {
        "original_history_operator_map_supplied": True,
        "original_40_direction_source_formula_supplied": True,
        "complete_same_realization_heat_source_formula_supplied": True,
        "native_execution_admission_proved": False,
        "source_gain_and_mesh_uniform_norm_proved": False,
        "compatible_physical_refinement_proved": False,
        "full_history_heat_replayed": False,
        "Lean_or_repository_CI_run_for_source_delta": False,
        "scientific_acceptance": False,
        "GR_closed": False,
    }, "Scientific scope was promoted")
    return {
        "status": "PASS_PINNED_DIRECT_SOURCE_GEOMETRY_DELTA",
        "owner_pr": 334,
        "source_commit": SOURCE_HEAD,
        "incoming_commits": len(EXPECTED_COMMITS),
        "upstream_snapshots": len(upstream_paths),
        "owner_checker_controls": result["checks"],
        "source_check_replayed_here": False,
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
