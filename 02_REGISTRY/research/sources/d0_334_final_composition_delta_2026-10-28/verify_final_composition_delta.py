#!/usr/bin/env python3
"""Read-only verifier for the pinned PR #334 final-composition intake."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import stat


PACKET = "02_REGISTRY/research/sources/d0_334_final_composition_delta_2026-10-28"
SOURCE_HEAD = "22e729996b70a699710a2d1120a0caa7a08decf8"
BASE_HEAD = "5fe5203da2439d325dc9ef70f52c1111822fc22b"
MANIFEST_SHA256 = "81ca9ca6d07ca1101924c1c29be41c2ab4adbb447f797e22a02e47499b443d69"
REPLAY_RECEIPT_SHA256 = "f12ec8399da5fa76e624b3d6318bd278c618ea798364ff9121df0b9db3c818da"
SOURCE_PREFIX = "02_REGISTRY/research/sources"
NUMERIC_TOLERANCE = 3e-12


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def read_file(root: Path, relative: str) -> bytes:
    root = Path(root)
    require(stat.S_ISDIR(root.lstat().st_mode), f"Expected real repository directory: {root}")
    parts = relative.split("/")
    require(parts and all(part not in ("", ".", "..") and "\\" not in part
                          for part in parts), f"Unsafe path: {relative}")
    current = root
    for part in parts[:-1]:
        current = current / part
        require(stat.S_ISDIR(current.lstat().st_mode), f"Expected real directory: {current}")
    target = current / parts[-1]
    require(stat.S_ISREG(target.lstat().st_mode), f"Expected regular file: {target}")
    return target.read_bytes()


def git_blob_sha1(data: bytes) -> str:
    header = b"blob " + str(len(data)).encode("ascii") + b"\0"
    return hashlib.sha1(header + data).hexdigest()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def compare_intersection(expected, actual, path: str = "$") -> float:
    if isinstance(expected, bool) or isinstance(actual, bool):
        require(expected == actual, f"Boolean differs at {path}")
        return 0.0
    if isinstance(expected, (int, float)) and isinstance(actual, (int, float)):
        delta = abs(float(expected) - float(actual))
        require(delta <= NUMERIC_TOLERANCE,
                f"Numeric difference at {path} exceeds tolerance: {delta}")
        return delta
    require(type(expected) is type(actual), f"Type differs at {path}")
    if isinstance(expected, dict):
        return max((compare_intersection(expected[key], actual[key], f"{path}.{key}")
                    for key in set(expected).intersection(actual)), default=0.0)
    if isinstance(expected, list):
        require(len(expected) == len(actual), f"List length differs at {path}")
        return max((compare_intersection(left, right, f"{path}[{index}]")
                    for index, (left, right) in enumerate(zip(expected, actual))), default=0.0)
    require(expected == actual, f"Value differs at {path}: {expected!r} != {actual!r}")
    return 0.0


def verify(root: Path) -> dict[str, object]:
    root = Path(root)
    manifest_bytes = read_file(root, f"{PACKET}/MANIFEST.json")
    require(sha256(manifest_bytes) == MANIFEST_SHA256, "Pinned source manifest SHA-256 mismatch")
    manifest = json.loads(manifest_bytes)
    require(manifest["schema"] == "d0-pr-source-delta-v1", "Unexpected source manifest schema")
    require(manifest["source_commit"] == SOURCE_HEAD and
            manifest["base_source_commit"] == BASE_HEAD, "Unexpected source commit range")
    require(manifest["owner_pr"] == 334 and manifest["file_count"] == len(manifest["files"]) == 31,
            "Unexpected source manifest size or owner")

    expected_snapshots = set()
    observed = []
    for entry in manifest["files"]:
        path = entry["snapshot_path"]
        expected_snapshots.add(path)
        data = read_file(root, f"{PACKET}/{path}")
        require(len(data) == entry["bytes"], f"Byte-count mismatch: {path}")
        require(sha256(data) == entry["sha256"], f"SHA-256 mismatch: {path}")
        require(git_blob_sha1(data) == entry["git_blob"], f"Git blob mismatch: {path}")
        observed.append({"path": path, "bytes": len(data), "sha256": entry["sha256"],
                         "git_blob": entry["git_blob"]})

    actual_snapshots = set()
    upstream_root = root / PACKET / "upstream"
    for path in upstream_root.rglob("*"):
        mode = path.lstat().st_mode
        if stat.S_ISDIR(mode):
            continue
        require(stat.S_ISREG(mode), f"Expected regular upstream file: {path}")
        actual_snapshots.add(path.relative_to(root / PACKET).as_posix())
    require(actual_snapshots == expected_snapshots, "Unmanifested or missing upstream snapshot")

    receipt_bytes = read_file(root, f"{PACKET}/replay/receipt.json")
    require(sha256(receipt_bytes) == REPLAY_RECEIPT_SHA256, "Replay receipt SHA-256 mismatch")
    receipt = json.loads(receipt_bytes)
    runner_bytes = read_file(root, f"{PACKET}/replay/run_replays.py")
    require(receipt["replay_runner_sha256"] == sha256(runner_bytes), "Replay runner hash mismatch")
    require(receipt["source_commit"] == SOURCE_HEAD and
            receipt["base_source_commit"] == BASE_HEAD, "Replay used another source range")
    require(receipt["status"] in (
        "PASS_ALL_SEVEN_CHECKERS",
        "PASS_ALL_SEVEN_CHECKERS_WITH_NUMPY_RUNTIME_WARNINGS",
    ) and len(receipt["checks"]) == 7, "All seven source checkers did not pass")
    require(receipt["normal_optimized_byte_identical"] is True,
            "Normal and optimized checker outputs differ")
    require(receipt["scientific_acceptance"] is False and
            receipt["physical_admission"] is False and receipt["GR_closed"] is False,
            "Replay receipt promoted its scientific scope")
    require(receipt["native_execution_sha256"] ==
            "222eafaffa4b30f175919a32c940534b82f3a2b9af89c7897d318dd004a2007c",
            "Replay uses an unexpected native execution input")

    observed_outputs = set()
    for check in receipt["checks"]:
        expected_path = f"{PACKET}/upstream/{SOURCE_PREFIX}/{check['published_result']}"
        expected_bytes = read_file(root, expected_path)
        require(sha256(expected_bytes) == check["published_result_sha256"],
                f"Published result hash mismatch: {check['name']}")
        expected = json.loads(expected_bytes)
        require(expected.get("status") == check["published_status"] == check["observed_status"],
                f"Published and observed status differ: {check['name']}")
        require(len(check["modes"]) == 2, f"Missing replay modes: {check['name']}")
        mode_outputs = []
        mode_stderr = []
        for mode in check["modes"]:
            require(mode["exit_code"] == 0, f"Checker failed: {check['name']}/{mode['mode']}")
            name = check["name"]
            output_path = f"{PACKET}/replay/observed/{name}.{mode['mode']}.json"
            stderr_path = f"{PACKET}/replay/observed/{name}.{mode['mode']}.stderr.txt"
            output = read_file(root, output_path)
            stderr = read_file(root, stderr_path)
            observed_outputs.add(f"replay/observed/{name}.{mode['mode']}.json")
            observed_outputs.add(f"replay/observed/{name}.{mode['mode']}.stderr.txt")
            require(len(output) == mode["stdout_bytes"] and sha256(output) == mode["stdout_sha256"],
                    f"Observed stdout hash mismatch: {output_path}")
            require(len(stderr) == mode["stderr_bytes"] and sha256(stderr) == mode["stderr_sha256"],
                    f"Observed stderr hash mismatch: {stderr_path}")
            actual = json.loads(output)
            require(actual.get("status") == check["observed_status"],
                    f"Observed status changed: {output_path}")
            if "source_sha256" in actual:
                require(actual["source_sha256"] == check["script_sha256"],
                        f"Checker source hash differs: {output_path}")
            if "native_owner_sha256" in actual:
                require(actual["native_owner_sha256"] == receipt["native_execution_sha256"],
                        f"Native source hash differs: {output_path}")
            for flag in ("GR_closed", "physical_action_selection_proved",
                         "physical_admission_asserted"):
                require(actual.get(flag, False) is False, f"Scientific scope promoted: {output_path}")
            delta = compare_intersection(expected, actual)
            require(delta == mode["published_result_intersection_max_numeric_delta"],
                    f"Numeric delta receipt mismatch: {output_path}")
            mode_outputs.append(output)
            mode_stderr.append(stderr)
        require(mode_outputs[0] == mode_outputs[1], f"Modes are not byte-identical: {check['name']}")
        if check["name"] == "clock":
            expected_messages = {
                "divide by zero encountered in matmul",
                "invalid value encountered in matmul",
                "overflow encountered in matmul",
            }
            for stderr in mode_stderr:
                messages = {
                    line.split("RuntimeWarning: ", 1)[1]
                    for line in stderr.decode("utf-8").splitlines()
                    if "RuntimeWarning: " in line
                }
                require(messages == expected_messages,
                        "Clock checker emitted an unrecognized warning")
        else:
            require(not mode_stderr[0] and not mode_stderr[1],
                    f"Unexpected checker emitted stderr: {check['name']}")
    if receipt["stderr_empty_all_modes"]:
        require(receipt["stderr_warning_counts"] == {}, "Unexpected warning summary")
    else:
        require(receipt["status"] == "PASS_ALL_SEVEN_CHECKERS_WITH_NUMPY_RUNTIME_WARNINGS",
                "Unexpected non-empty stderr scope")
        require(receipt["stderr_warning_counts"] == {
            "divide by zero encountered in matmul": 2,
            "invalid value encountered in matmul": 2,
            "overflow encountered in matmul": 2,
        }, "Unrecognized NumPy warnings in the clock structural control")
        require(all(check["name"] == "clock" or
                    all(mode["stderr_bytes"] == 0 for mode in check["modes"])
                    for check in receipt["checks"]),
                "Unexpected checker emitted stderr")
    require(len(observed_outputs) == 28, "Unexpected replay output inventory")
    return {
        "status": "PASS_PINNED_FINAL_COMPOSITION_SOURCE_AND_REPLAYS",
        "source_commit": SOURCE_HEAD,
        "base_source_commit": BASE_HEAD,
        "file_count": len(observed),
        "source_bytes": sum(item["bytes"] for item in observed),
        "replayed_checker_count": len(receipt["checks"]),
        "source_code_executed_by_verifier": False,
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
