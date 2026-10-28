#!/usr/bin/env python3
"""Verify the stored local replay of the pinned moving-cut checker."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess

PACKET = Path(__file__).resolve().parent
REPO = PACKET.parents[4]
SOURCE_COMMIT = "eebcb5e467742df3e9cf7fa9702042d7294aa742"
CHECKER_PATH = "02_REGISTRY/research/sources/d0_root_moving_cut_2026-10-28/check_root_moving_cut.py"
RESULT_PATH = "02_REGISTRY/research/sources/d0_root_moving_cut_2026-10-28/result.json"


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def regular(path: Path) -> bytes:
    require(not path.is_symlink() and path.is_file(), f"Expected regular file: {path}")
    return path.read_bytes()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob_sha1(data: bytes) -> str:
    header = b"blob " + str(len(data)).encode("ascii") + b"\0"
    return hashlib.sha1(header + data).hexdigest()


def git_bytes(*args: str) -> bytes:
    return subprocess.run(["git", *args], cwd=REPO, check=True,
                          stdout=subprocess.PIPE).stdout


def compare(owner: object, replay: object, path: str = "") -> tuple[int, float]:
    count = 0
    maximum = 0.0
    if isinstance(owner, dict) and isinstance(replay, dict):
        require(set(owner) == set(replay), f"JSON keys differ at {path or '/'}")
        for key in sorted(owner):
            n, d = compare(owner[key], replay[key], f"{path}/{key}")
            count += n
            maximum = max(maximum, d)
    elif isinstance(owner, list) and isinstance(replay, list):
        require(len(owner) == len(replay), f"JSON list length differs at {path}")
        for index, (left, right) in enumerate(zip(owner, replay)):
            n, d = compare(left, right, f"{path}/{index}")
            count += n
            maximum = max(maximum, d)
    elif isinstance(owner, bool) or isinstance(replay, bool):
        require(owner == replay, f"JSON boolean differs at {path}")
    elif isinstance(owner, (int, float)) or isinstance(replay, (int, float)):
        require(isinstance(owner, (int, float)) and isinstance(replay, (int, float)),
                f"JSON numeric type differs at {path}")
        delta = abs(float(owner) - float(replay))
        count += delta != 0
        maximum = max(maximum, delta)
    else:
        require(owner == replay, f"JSON value differs at {path}")
    return count, maximum


def verify(verify_source_objects: bool = False) -> dict[str, object]:
    manifest_data = regular(PACKET / "LOCAL_REPLAY_MANIFEST.json")
    checksum = regular(PACKET / "LOCAL_REPLAY_MANIFEST.sha256").decode("ascii").split()[0]
    require(checksum == sha256(manifest_data), "Local replay manifest checksum mismatch")
    manifest = json.loads(manifest_data)
    require(manifest["source_commit"] == SOURCE_COMMIT and
            manifest["checker_path"] == CHECKER_PATH and
            manifest["owner_result_path"] == RESULT_PATH,
            "Pinned source identity differs")

    expected = {row["path"] for row in manifest["artifacts"]}
    actual = {
        item.relative_to(PACKET).as_posix()
        for item in PACKET.rglob("*")
        if item.is_file() and item.name not in
        ("LOCAL_REPLAY_MANIFEST.json", "LOCAL_REPLAY_MANIFEST.sha256")
    }
    require(actual == expected, "Local replay artifact inventory differs")
    for row in manifest["artifacts"]:
        data = regular(PACKET / row["path"])
        require(len(data) == row["bytes"] and sha256(data) == row["sha256"],
                f"Replay artifact digest mismatch: {row['path']}")

    checker = regular(REPO / CHECKER_PATH)
    owner_result = regular(REPO / RESULT_PATH)
    require(sha256(checker) == manifest["checker_sha256"], "Checker SHA-256 differs")
    require(sha256(owner_result) == manifest["owner_result_sha256"],
            "Pinned owner result SHA-256 differs")

    normal = regular(PACKET / "normal.json")
    optimized = regular(PACKET / "optimized.json")
    require(normal == optimized, "Ordinary and optimized outputs differ")
    actual_value = json.loads(normal)
    owner_value = json.loads(owner_result)
    require(actual_value["status"] == "PASS_FULL_BOOTSTRAP_MOVING_CUT" and
            actual_value["GR_closed"] is False and
            actual_value["native_full42_replayed"] is False and
            actual_value["lean_or_ci_run"] is False,
            "Replay scope or status changed")
    require(actual_value["moving_cut_control_source"] == 0.06218198611141448,
            "Moving-cut control source differs")
    differences, maximum = compare(owner_value, actual_value)
    require(differences == manifest["owner_numeric_differences"] and
            abs(maximum - manifest["owner_max_numeric_drift"]) < 1e-25,
            "Owner/local numerical delta differs")

    normal_stderr = regular(PACKET / "normal.stderr")
    optimized_stderr = regular(PACKET / "optimized.stderr")
    require(normal_stderr == optimized_stderr, "Ordinary and optimized stderr differs")
    warning_count = sum(b"RuntimeWarning" in line for line in normal_stderr.splitlines())
    require(warning_count == manifest["warning_records_per_mode"],
            "RuntimeWarning record count differs")

    if verify_source_objects:
        for path, expected_blob in (
            (CHECKER_PATH, manifest["checker_git_blob_sha1"]),
            (RESULT_PATH, manifest["owner_result_git_blob_sha1"]),
        ):
            observed = git_bytes("rev-parse", f"{SOURCE_COMMIT}:{path}").decode().strip()
            require(observed == expected_blob, f"Pinned Git tree blob differs: {path}")
            require(git_bytes("cat-file", "blob", expected_blob) == regular(REPO / path),
                    f"Pinned Git object bytes differ: {path}")

    return {
        "status": "PASS_PINNED_MOVING_CUT_REPLAY",
        "source_commit": SOURCE_COMMIT,
        "ordinary_equals_optimized": True,
        "local_max_fd_error": actual_value["max_fd_error"],
        "owner_max_fd_error": owner_value["max_fd_error"],
        "owner_numeric_fields_differing": differences,
        "owner_max_numeric_drift": maximum,
        "warning_records_per_mode": warning_count,
        "GR_closed": actual_value["GR_closed"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify-source-objects", action="store_true")
    args = parser.parse_args()
    result = verify(args.verify_source_objects)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
