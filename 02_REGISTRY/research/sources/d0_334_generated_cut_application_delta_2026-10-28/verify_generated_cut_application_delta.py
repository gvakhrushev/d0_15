#!/usr/bin/env python3
"""Read-only verifier for the pinned PR #334 generated-cut source delta."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import stat
import subprocess
import sys
import tempfile

PACKET = "02_REGISTRY/research/sources/d0_334_generated_cut_application_delta_2026-10-28"
SOURCE_HEAD = "5fe5203da2439d325dc9ef70f52c1111822fc22b"
BASE_HEAD = "172876cdf38bfce6f87fdd4a059d524b60c10eb9"
MANIFEST_SHA256 = "11512b031b3be8e6fa56d37914b6c2c5d93faca0c94b0f6ec2cb56456068c303"
EXTRACTED_SHA256 = "4bc48def3118181d62d6ddc992038672ff42bb6dd3513fe0cf11a28d9a62706f"
REPLAY_RECEIPT_SHA256 = "0e23e828beb7ba62232804318e7493520323f2474603ea3f711e4b5b5c89b91a"
NUMERIC_TOLERANCE = 3e-14


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def read_file(root: Path, relative: str) -> bytes:
    require(stat.S_ISDIR(root.lstat().st_mode), f"Expected real repository directory: {root}")
    parts = relative.split("/")
    require(parts and all(p not in ("", ".", "..") and "\\" not in p for p in parts),
            f"Unsafe source path: {relative}")
    current = root
    for part in parts[:-1]:
        current = current / part
        require(stat.S_ISDIR(current.lstat().st_mode), f"Expected real directory: {current}")
    target = current / parts[-1]
    require(stat.S_ISREG(target.lstat().st_mode), f"Expected regular file: {target}")
    return target.read_bytes()


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def extract_fence(document: bytes, label: bytes, language: bytes) -> bytes:
    marker = document.index(label)
    fence = document.index(b"```" + language, marker)
    start = document.index(b"\n", fence) + 1
    end = document.index(b"\n```", start)
    return document[start:end + 1]


def compare_json(expected, actual, path: str = "$", tolerance: float = NUMERIC_TOLERANCE) -> float:
    if isinstance(expected, bool) or isinstance(actual, bool):
        require(expected == actual, f"JSON value differs at {path}")
        return 0.0
    if isinstance(expected, (int, float)) and isinstance(actual, (int, float)):
        delta = abs(float(expected) - float(actual))
        require(delta <= tolerance, f"Numeric difference at {path} exceeds tolerance: {delta}")
        return delta
    require(type(expected) is type(actual), f"JSON type differs at {path}")
    if isinstance(expected, dict):
        require(set(expected) == set(actual), f"JSON object keys differ at {path}")
        return max((compare_json(expected[k], actual[k], f"{path}.{k}", tolerance)
                    for k in expected), default=0.0)
    if isinstance(expected, list):
        require(len(expected) == len(actual), f"JSON list lengths differ at {path}")
        return max((compare_json(a, b, f"{path}[{i}]", tolerance)
                    for i, (a, b) in enumerate(zip(expected, actual))), default=0.0)
    require(expected == actual, f"JSON value differs at {path}")
    return 0.0


def verify(root: Path) -> dict[str, object]:
    root = Path(root)
    manifest_data = read_file(root, f"{PACKET}/MANIFEST.json")
    require(hashlib.sha256(manifest_data).hexdigest() == MANIFEST_SHA256,
            "Pinned source manifest SHA-256 mismatch")
    manifest = json.loads(manifest_data)
    require(manifest["source_commit"] == SOURCE_HEAD and manifest["base_source_commit"] == BASE_HEAD,
            "Unexpected source checkpoint")
    require(manifest["schema"] == "d0-pr-source-delta-v2" and
            manifest["file_count"] == len(manifest["files"]) == 6,
            "Unexpected changed source file count")

    expected_upstream = set()
    expected_patches = set()
    observed_upstream = []
    source_by_upstream: dict[str, bytes] = {}
    for item in manifest["files"]:
        upstream_path = item["upstream_path"]
        if item["storage"] == "snapshot":
            snapshot_path = item["snapshot_path"]
            expected_upstream.add(snapshot_path)
            data = read_file(root, f"{PACKET}/{snapshot_path}")
        elif item["storage"] == "patch":
            require(item["base_source_commit"] == BASE_HEAD,
                    f"Unexpected patch base: {upstream_path}")
            expected_patches.add(item["patch_path"])
            base = read_file(root, item["base_snapshot_path"])
            require(len(base) == item["base_bytes"],
                    f"Patch-base byte-count mismatch: {upstream_path}")
            require(hashlib.sha256(base).hexdigest() == item["base_sha256"],
                    f"Patch-base SHA-256 mismatch: {upstream_path}")
            require(git_blob_sha1(base) == item["base_git_blob"],
                    f"Patch-base Git blob mismatch: {upstream_path}")
            patch_data = read_file(root, f"{PACKET}/{item['patch_path']}")
            require(len(patch_data) == item["patch_bytes"] and
                    hashlib.sha256(patch_data).hexdigest() == item["patch_sha256"],
                    f"Pinned source patch mismatch: {upstream_path}")
            with tempfile.TemporaryDirectory(prefix="d0-source-delta-") as temporary:
                temp_root = Path(temporary)
                destination = temp_root.joinpath(*upstream_path.split("/"))
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(base)
                try:
                    result = subprocess.run(
                        ["git", "apply", "--binary", "--whitespace=nowarn", "-"],
                        input=patch_data, cwd=temp_root, stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE, check=False,
                    )
                except OSError as exc:
                    raise ValueError("git is required to reconstruct pinned source patches") from exc
                require(result.returncode == 0,
                        f"Source patch did not apply: {upstream_path}: "
                        f"{result.stderr.decode('utf-8', errors='replace').strip()}")
                data = destination.read_bytes()
        else:
            raise ValueError(f"Unknown source storage method: {item['storage']}")
        require(len(data) == item["bytes"], f"Source byte-count mismatch: {upstream_path}")
        require(hashlib.sha256(data).hexdigest() == item["sha256"],
                f"Source SHA-256 mismatch: {upstream_path}")
        require(git_blob_sha1(data) == item["git_blob"],
                f"Source Git blob mismatch: {upstream_path}")
        source_by_upstream[upstream_path] = data
        observed_upstream.append({"path": upstream_path, "bytes": len(data),
                                  "sha256": item["sha256"], "git_blob": item["git_blob"]})
    actual_upstream = set()
    for path in (root / PACKET / "upstream").rglob("*"):
        mode = path.lstat().st_mode
        if stat.S_ISDIR(mode):
            continue
        require(stat.S_ISREG(mode), f"Expected regular upstream file: {path}")
        actual_upstream.add(path.relative_to(root / PACKET).as_posix())
    require(actual_upstream == expected_upstream, "Unmanifested or missing upstream files")
    actual_patches = set()
    for path in (root / PACKET / "patches").rglob("*"):
        mode = path.lstat().st_mode
        if stat.S_ISDIR(mode):
            continue
        require(stat.S_ISREG(mode), f"Expected regular patch file: {path}")
        actual_patches.add(path.relative_to(root / PACKET).as_posix())
    require(actual_patches == expected_patches, "Unmanifested or missing source patches")

    extracted_data = read_file(root, f"{PACKET}/EXTRACTED_CHECKS.json")
    require(hashlib.sha256(extracted_data).hexdigest() == EXTRACTED_SHA256,
            "Pinned extracted-check metadata SHA-256 mismatch")
    extracted = json.loads(extracted_data)
    require(extracted["source_commit"] == SOURCE_HEAD and
            extracted["base_source_commit"] == BASE_HEAD and
            len(extracted["embedded_checks"]) == 2,
            "Extracted-check metadata has an unexpected source or check count")

    receipt_data = read_file(root, f"{PACKET}/replay/receipt.json")
    require(hashlib.sha256(receipt_data).hexdigest() == REPLAY_RECEIPT_SHA256,
            "Pinned replay receipt SHA-256 mismatch")
    receipt = json.loads(receipt_data)
    require(receipt["source_commit"] == SOURCE_HEAD and receipt["base_source_commit"] == BASE_HEAD,
            "Replay used a different source checkpoint")
    require(receipt["status"] == "PASS_BOTH_QUERY_CUT_CONTROLS_NORMAL_AND_OPTIMIZED",
            "Replay receipt does not record both controls passing")
    require(receipt["source_code_executed_by_verifier"] is False and
            receipt["scientific_acceptance"] is False,
            "Verifier scope flags must remain false")

    native_inputs = []
    for item in manifest["replay_input_files"]:
        rel = f"{PACKET}/{item['snapshot_path']}"
        data = read_file(root, rel)
        require(len(data) == item["bytes"], f"Replay-input byte-count mismatch: {rel}")
        require(hashlib.sha256(data).hexdigest() == item["sha256"],
                f"Replay-input SHA-256 mismatch: {rel}")
        require(git_blob_sha1(data) == item["git_blob"], f"Replay-input Git blob mismatch: {rel}")
        native_inputs.append(item)
    require(len(native_inputs) == 3 and manifest["replay_input_file_count"] == 3,
            "Unexpected native input count")

    checks_by_name = {item["script"]: item for item in receipt["checks"]}
    require(len(checks_by_name) == 2, "Unexpected replay checker count")
    max_numeric_delta = 0.0
    for meta in extracted["embedded_checks"]:
        name = meta["script"]
        source = source_by_upstream[meta["source_upstream_path"]]
        script = read_file(root, f"{PACKET}/replay/scripts/{name}")
        if name == "d0_generated_cut_source_20261028.py":
            require(script == extract_fence(source, b"d0_generated_cut_source_20261028.py:", b"python"),
                    "Extracted generated-cut checker differs from its memo fence")
            expected_bytes = extract_fence(source, b"d0_generated_cut_source_20261028.json:", b"json")
        else:
            require(script == source, "QUERY-cut checker differs from its upstream source file")
            expected_bytes = read_file(root, f"{PACKET}/upstream/02_REGISTRY/research/sources/"
                                       "d0_root_boundary_reduction_2026-10-28/query_cut_result.json")
        require(hashlib.sha256(script).hexdigest() == meta["source_sha256"],
                f"Checker source hash differs: {name}")
        expected_copy = read_file(root, f"{PACKET}/replay/expected/{meta['result']}")
        require(expected_copy == expected_bytes, f"Stored expected result differs from source: {name}")
        require(hashlib.sha256(expected_copy).hexdigest() == meta["expected_sha256"],
                f"Expected result hash differs: {name}")
        check = checks_by_name[name]
        require(check["status"] == json.loads(expected_copy)["status"],
                f"Replay status differs from source result: {name}")
        require(check["source_sha256"] == meta["source_sha256"],
                f"Receipt source hash differs: {name}")
        mode_hashes = set()
        for mode in ("ordinary", "optimized"):
            mode_entry = next((row for row in check["modes"] if row["mode"] == mode), None)
            require(mode_entry is not None and mode_entry["exit_code"] == 0,
                    f"Missing successful {mode} replay: {name}")
            output_path = f"{PACKET}/replay/observed/{name}.{mode}.json"
            output = read_file(root, output_path)
            require(hashlib.sha256(output).hexdigest() == mode_entry["stdout_sha256"],
                    f"Observed output hash differs: {output_path}")
            local_delta = compare_json(json.loads(expected_copy), json.loads(output),
                                       tolerance=NUMERIC_TOLERANCE if name == "check_query_cut_orbit.py" else 0.0)
            require(local_delta == mode_entry["maximum_numeric_difference_from_published"],
                    f"Recorded numeric delta differs: {name}/{mode}")
            if name == "d0_generated_cut_source_20261028.py":
                require(output == expected_copy, f"Generated-cut checker output is not byte-exact: {name}/{mode}")
            mode_hashes.add(mode_entry["stdout_sha256"])
            max_numeric_delta = max(max_numeric_delta, local_delta)
        require(len(mode_hashes) == 1, f"Ordinary and optimized outputs differ: {name}")

    require(max_numeric_delta <= NUMERIC_TOLERANCE,
            "A local finite-control output exceeds the pinned numeric tolerance")
    return {
        "status": "PASS_PINNED_GENERATED_CUT_SOURCE_AND_REPLAY_BYTES",
        "source_commit": SOURCE_HEAD,
        "base_source_commit": BASE_HEAD,
        "upstream_file_count": len(observed_upstream),
        "upstream_bytes": sum(row["bytes"] for row in observed_upstream),
        "replay_input_count": len(native_inputs),
        "replayed_checker_count": len(checks_by_name),
        "max_numeric_difference_from_published": max_numeric_delta,
        "source_code_executed_by_verifier": False,
        "scientific_acceptance": False,
    }


def main() -> int:
    try:
        if len(sys.argv) > 2:
            raise ValueError("Usage: verify_generated_cut_application_delta.py [repository-root]")
        root = Path(sys.argv[1]) if len(sys.argv) == 2 else Path(__file__).resolve().parents[4]
        print(json.dumps(verify(root), ensure_ascii=False, sort_keys=True, indent=2))
        return 0
    except (KeyError, OSError, TypeError, ValueError, AssertionError) as exc:
        print(f"FAIL_GENERATED_CUT_APPLICATION_DELTA: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
