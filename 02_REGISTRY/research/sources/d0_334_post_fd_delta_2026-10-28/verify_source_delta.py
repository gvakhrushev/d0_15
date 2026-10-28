#!/usr/bin/env python3
"""Verify the exact #334 post-fd source packet and bounded local replays."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

PACKET = Path(__file__).resolve().parent
REPO = PACKET.parents[3]
BASE = "fd35893d77e4aa5f819bafa0c6428c8e7a8f1812"
HEAD = "1dce9b709109c3fc2921c97ff75a31b3bcb09d6c"
TASK_INPUT = "02_REGISTRY/research/A4D_TASK_FAITHFUL_RETURN_SOURCE_2026_10_28.md"
TASK_COMMIT = BASE
CHANGED_PATHS = [
    "00_WORK/tasks/EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE.md",
    "02_REGISTRY/research/A4D_FULL_CLOSURE_SOURCE_AUDIT_2026_10_28.md",
    "02_REGISTRY/research/A4D_INTERNAL_PROGRAM_AND_GLOBAL_QUERY_STATIONARITY_2026_10_28.md",
    "02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md",
    "02_REGISTRY/research/sources/d0_full_closure_audit_2026-10-28/check_closure_audit.py",
    "02_REGISTRY/research/sources/d0_full_closure_audit_2026-10-28/result.json",
    "02_REGISTRY/research/sources/d0_internal_program_source_2026-10-28/check_program_source.py",
    "02_REGISTRY/research/sources/d0_internal_program_source_2026-10-28/result.json",
]
SOURCE_DOCUMENT_PATHS = [
    "02_REGISTRY/research/A4D_FULL_CLOSURE_SOURCE_AUDIT_2026_10_28.md",
    "02_REGISTRY/research/A4D_INTERNAL_PROGRAM_AND_GLOBAL_QUERY_STATIONARITY_2026_10_28.md",
]
SOURCE_INPUT_PATHS = [
    TASK_INPUT,
    "02_REGISTRY/research/sources/d0_task_faithful_source_2026-10-28/PROOF_RU.md",
    "02_REGISTRY/research/sources/d0_task_faithful_source_2026-10-28/check_task_source.py",
    "02_REGISTRY/research/sources/d0_task_faithful_source_2026-10-28/result.json",
    "02_REGISTRY/research/sources/d0_task_faithful_source_2026-10-28/TWO_FIELD_HANDOFF_RU.md",
    "02_REGISTRY/research/A4D_REGULAR_APPARATUS_SOURCE_DESCENT_2026_10_28.md",
    "02_REGISTRY/research/sources/d0_apparatus_cotangent_descent_2026-10-28/PROOF_RU.md",
    "02_REGISTRY/research/sources/d0_apparatus_cotangent_descent_2026-10-28/check_descent.py",
    "02_REGISTRY/research/sources/d0_apparatus_cotangent_descent_2026-10-28/result.json",
]
APPARATUS_COMMIT = "73816d279dc23ee62be75662bf3081013a49ad55"
SOURCE_INPUT_COMMITS = {
    path: TASK_COMMIT for path in SOURCE_INPUT_PATHS[:5]
}
SOURCE_INPUT_COMMITS.update({
    path: APPARATUS_COMMIT for path in SOURCE_INPUT_PATHS[5:]
})
MAX_NUMERIC_DRIFT = 5e-15


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def regular(path: Path) -> bytes:
    require(not path.is_symlink() and path.is_file(), f"Expected regular file: {path}")
    return path.read_bytes()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def blob_sha1(data: bytes) -> str:
    header = b"blob " + str(len(data)).encode("ascii") + b"\0"
    return hashlib.sha1(header + data).hexdigest()


def git_bytes(*args: str) -> bytes:
    return subprocess.run(
        ["git", *args], cwd=REPO, check=True, stdout=subprocess.PIPE
    ).stdout


def compare_result(owner: object, replay: object, path: str = "") -> tuple[int, float]:
    differences = 0
    maximum = 0.0
    if isinstance(owner, dict) and isinstance(replay, dict):
        require(set(owner) == set(replay), f"JSON keys differ at {path or '/'}")
        for key in sorted(owner):
            if path == "/environment" and key in ("python", "numpy"):
                continue
            count, drift = compare_result(owner[key], replay[key], f"{path}/{key}")
            differences += count
            maximum = max(maximum, drift)
    elif isinstance(owner, list) and isinstance(replay, list):
        require(len(owner) == len(replay), f"JSON list length differs at {path}")
        for index, (left, right) in enumerate(zip(owner, replay)):
            count, drift = compare_result(left, right, f"{path}/{index}")
            differences += count
            maximum = max(maximum, drift)
    elif isinstance(owner, bool) or isinstance(replay, bool):
        require(owner == replay, f"JSON boolean differs at {path}")
    elif isinstance(owner, (int, float)) or isinstance(replay, (int, float)):
        require(isinstance(owner, (int, float)) and isinstance(replay, (int, float)),
                f"JSON numeric type differs at {path}")
        drift = abs(float(owner) - float(replay))
        require(drift <= MAX_NUMERIC_DRIFT, f"Numeric drift too large at {path}: {drift}")
        differences += drift != 0
        maximum = drift
    else:
        require(owner == replay, f"JSON value differs at {path}")
    return differences, maximum


def verify_source_objects(manifest: dict[str, object]) -> None:
    git_bytes("cat-file", "-e", f"{BASE}^{{commit}}")
    git_bytes("cat-file", "-e", f"{HEAD}^{{commit}}")
    subprocess.run(["git", "merge-base", "--is-ancestor", BASE, HEAD], cwd=REPO, check=True)
    rows = manifest["source_files"] + manifest["source_inputs"]
    for row in rows:
        source = regular(PACKET / row["packet_path"])
        blob = git_bytes("cat-file", "blob", row["git_blob_sha1"])
        require(blob == source, f"Git blob bytes differ: {row['repository_path']}")
        commit_blob = git_bytes("rev-parse", f"{row['commit']}:{row['repository_path']}").decode().strip()
        require(commit_blob == row["git_blob_sha1"], f"Commit path blob differs: {row['repository_path']}")

    commits = git_bytes("log", "--reverse", "--format=%H%x09%cI%x09%s", f"{BASE}..{HEAD}")
    require(commits == regular(PACKET / "COMMITS.tsv"), "Ordered commit list differs from Git")
    patch = git_bytes("diff", "--binary", f"{BASE}..{HEAD}", "--", *CHANGED_PATHS)
    require(patch == regular(PACKET / "SOURCE.patch"), "Source patch differs from Git range")
    changed_paths = git_bytes("diff", "--name-only", f"{BASE}..{HEAD}").decode("utf-8").splitlines()
    require(changed_paths == CHANGED_PATHS, "Changed-path inventory differs from Git range")


def verify_relative_links(manifest: dict[str, object]) -> None:
    """Keep the relative links among the restored source notes usable in-packet."""
    for row in manifest["source_inputs"] + [
        {"packet_path": f"upstream/{path}"} for path in SOURCE_DOCUMENT_PATHS
    ]:
        source = PACKET / row["packet_path"]
        if source.suffix.lower() != ".md":
            continue
        content = regular(source).decode("utf-8")
        for target in re.findall(r"\]\(([^)]+)\)", content):
            target = target.split("#", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            linked = (source.parent / target).resolve()
            try:
                linked.relative_to(PACKET.resolve())
            except ValueError as exc:
                raise ValueError(f"Source link escapes packet: {source}: {target}") from exc
            require(linked.exists(), f"Missing relative source link: {source}: {target}")


def verify() -> dict[str, object]:
    manifest_data = regular(PACKET / "MANIFEST.json")
    checksum = regular(PACKET / "MANIFEST.sha256").decode("ascii").split()[0]
    require(checksum == sha256(manifest_data), "Manifest SHA-256 mismatch")
    manifest = json.loads(manifest_data)
    require(manifest["schema"] == "d0-pr-source-range-intake-v1" and
            manifest["repository"] == "gvakhrushev/d0_15" and
            manifest["owner_pr"] == 334, "Unexpected source identity")
    require(manifest["source_range"] == {"base_commit": BASE, "head_commit": HEAD,
            "commits": 7}, "Unexpected source range")

    source_rows = manifest["source_files"]
    require([row["repository_path"] for row in source_rows] == CHANGED_PATHS,
            "Changed-source file list differs")
    require([row["commit"] for row in source_rows] == [HEAD] * len(CHANGED_PATHS),
            "Changed-source commit pins differ")
    require([row["packet_path"] for row in source_rows] ==
            [f"upstream/{path}" for path in CHANGED_PATHS],
            "Changed-source packet paths differ")

    expected = {row["path"] for row in manifest["artifacts"]}
    actual = {
        item.relative_to(PACKET).as_posix()
        for item in PACKET.rglob("*")
        if item.is_file() and item.name not in ("MANIFEST.json", "MANIFEST.sha256")
    }
    require(actual == expected, "Packet artifact inventory differs")
    for row in manifest["artifacts"]:
        data = regular(PACKET / row["path"])
        require(len(data) == row["bytes"] and sha256(data) == row["sha256"],
                f"Packet artifact digest mismatch: {row['path']}")

    for row in manifest["source_files"]:
        data = regular(PACKET / row["packet_path"])
        require(blob_sha1(data) == row["git_blob_sha1"],
                f"Changed-source Git blob ID mismatch: {row['repository_path']}")
    for row in manifest["source_inputs"]:
        data = regular(PACKET / row["packet_path"])
        require(blob_sha1(data) == row["git_blob_sha1"],
                f"Source Git blob ID mismatch: {row['repository_path']}")
        canonical = regular(REPO / row["repository_path"])
        require(canonical == data, f"Canonical restored source differs: {row['repository_path']}")

    internal = manifest["replays"]["internal_program"]
    internal_normal = regular(PACKET / internal["normal_output"])
    internal_optimized = regular(PACKET / internal["optimized_output"])
    require(internal_normal == internal_optimized, "Internal-program replay outputs differ")
    internal_value = json.loads(internal_normal)
    internal_checker = regular(PACKET / internal["checker"])
    require(internal_value["checks"] == 362 and
            internal_value["status"] == "PASS_INTERNAL_PROGRAM_SOURCE_CHART" and
            internal_value["scientific_input"] == BASE and
            internal_value["checker_sha256"] == sha256(internal_checker),
            "Unexpected internal-program replay result")
    require(internal_value["GR_closed"] is False and
            internal_value["task_law_selection_proved"] is False and
            internal_value["physical_controlled_evaluator_admitted"] is False and
            internal_value["full_physical_variation_domain_proved"] is False,
            "Replay scope flags changed")
    owner_internal = json.loads(regular(PACKET / internal["owner_result"]))
    int_count, int_drift = compare_result(owner_internal, internal_value)
    int_stderr = regular(PACKET / internal["normal_stderr"])
    require(int_stderr == regular(PACKET / internal["optimized_stderr"]),
            "Internal-program stderr differs by mode")
    warning_count = sum(b"RuntimeWarning" in line for line in int_stderr.splitlines())
    require(warning_count == internal["warning_records"], "RuntimeWarning record count differs")

    closure = manifest["replays"]["closure_audit"]
    closure_normal = regular(PACKET / closure["normal_output"])
    closure_optimized = regular(PACKET / closure["optimized_output"])
    require(closure_normal == closure_optimized, "Closure-audit outputs differ by mode")
    closure_stderr = regular(PACKET / closure["normal_stderr"])
    require(closure_stderr == regular(PACKET / closure["optimized_stderr"]),
            "Closure-audit stderr differs by mode")
    closure_environment = json.loads(regular(PACKET / closure["environment_file"]))
    require(closure_environment == {
            "python": "3.12.14", "numpy": "2.3.5", "scipy": "1.18.1",
            "sympy": "1.14.0", "mpmath": "1.3.0", "owner_receipt_available": True,
        }, "Unexpected closure-audit replay environment")
    closure_value = json.loads(closure_normal)
    closure_checker = regular(PACKET / closure["checker"])
    require(closure_value["checks"] == 65 and
            closure_value["status"] == "PASS_SCOPED_FULL_SOURCE_AUDIT" and
            closure_value["input_commit"] == "1595b9bd2cf9720900c1bf573df04cf9e2e7931f" and
            closure_value["checker_sha256"] == sha256(closure_checker),
            "Unexpected scoped closure-audit replay result")
    require(closure_value["GR_closed"] is False and
            closure_value["native_variation_domain_derived"] is False and
            closure_value["physical_GR_impossibility_proved"] is False and
            closure_value["new_full42_root_computed"] is False and
            closure_value["Lean_or_CI_run"] is False,
            "Closure-audit scope flags changed")
    owner_closure_bytes = regular(PACKET / closure["owner_result"])
    require(sha256(owner_closure_bytes) == closure["owner_result_sha256"] and
            sha256(owner_closure_bytes) ==
            "1768200f22870ec390fe843f7747f1db5a52380deaebf324f9202a79546008b8",
            "Closure-audit owner receipt digest differs")
    owner_closure = json.loads(owner_closure_bytes)
    closure_count, closure_drift = compare_result(owner_closure, closure_value)
    require(closure_count == 2 and closure_drift <= MAX_NUMERIC_DRIFT,
            "Unexpected closure-audit owner/local numerical comparison")

    task = manifest["replays"]["task_effect"]
    task_normal = regular(PACKET / task["normal_output"])
    task_optimized = regular(PACKET / task["optimized_output"])
    require(task_normal == task_optimized, "Task-effect replay outputs differ")
    task_value = json.loads(task_normal)
    task_checker = regular(PACKET / task["checker"])
    require(task_value["checks"] == 97 and
            task_value["status"] == "PASS_TASK_FAITHFUL_RETURN_SOURCE" and
            task_value["checker_sha256"] == sha256(task_checker),
            "Unexpected task-effect replay result")
    owner_task = json.loads(regular(PACKET / task["owner_result"]))
    task_count, task_drift = compare_result(owner_task, task_value)
    require(not regular(PACKET / task["normal_stderr"]) and
            not regular(PACKET / task["optimized_stderr"]),
            "Task-effect replay emitted unexpected stderr")

    canonical_inputs = manifest["source_inputs"]
    require([row["repository_path"] for row in canonical_inputs] == SOURCE_INPUT_PATHS,
            "Related source-input list differs")
    require([row["commit"] for row in canonical_inputs] ==
            [SOURCE_INPUT_COMMITS[path] for path in SOURCE_INPUT_PATHS],
            "Related source-input commit pins differ")
    verify_relative_links(manifest)
    return {
        "status": "PASS_SOURCE_BYTES_AND_BOUNDED_REPLAY",
        "source_head": HEAD,
        "changed_source_files": len(CHANGED_PATHS),
        "source_range_commits": 7,
        "related_source_input_files": len(SOURCE_INPUT_PATHS),
        "internal_program_checks": internal_value["checks"],
        "internal_program_owner_numeric_fields_differing": int_count,
        "internal_program_max_numeric_drift": int_drift,
        "internal_program_warning_records_per_mode": warning_count,
        "task_effect_checks": task_value["checks"],
        "task_effect_owner_numeric_fields_differing": task_count,
        "task_effect_max_numeric_drift": task_drift,
        "closure_audit_checks": closure_value["checks"],
        "closure_audit_owner_numeric_fields_differing": closure_count,
        "closure_audit_max_numeric_drift": closure_drift,
        "closure_audit_stderr_bytes": len(closure_stderr),
        "closure_audit_environment": closure_environment,
        "physical_admission_or_GR_closure": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify-source-objects", action="store_true")
    args = parser.parse_args()
    summary = verify()
    if args.verify_source_objects:
        manifest = json.loads(regular(PACKET / "MANIFEST.json"))
        verify_source_objects(manifest)
        summary["source_git_objects"] = "PASS"
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
