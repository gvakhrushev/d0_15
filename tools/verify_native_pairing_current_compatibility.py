#!/usr/bin/env python3
"""Compile the pinned pairing capsule against the current supported Lean tree."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

if __package__:
    from . import lean_task_build
else:
    import lean_task_build


ROOT = Path(__file__).resolve().parents[1]
FORMAL = ROOT / "03_FORMALIZATION"
CAPSULE_RELATIVE = "02_REGISTRY/research/certificates/a4d_native_pairing_refinement_source.lean"
CAPSULE = ROOT / CAPSULE_RELATIVE
CAPSULE_SHA256 = "65d1aff45f17907fcacdcbdc6da889bc0e44b3982b1590a5254f2e8e5ad38d10"
BUILD_TARGETS = [
    "D0.Geometry.ArchiveMetricMeasureHodgeLift",
    "D0.Geometry.ArchiveRefinementHodgeWeights",
]
STANDARD_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
AXIOM_REPORT = re.compile(
    r"^'([^']+)'\s+(?:depends on axioms:\s*\[([^\]]*)\]|"
    r"does not depend on any axioms)",
    re.MULTILINE,
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run(command: list[str], cwd: Path) -> subprocess.CompletedProcess[bytes]:
    result = subprocess.run(command, cwd=cwd, capture_output=True, check=False)
    if result.returncode:
        raise RuntimeError(
            f"command {command!r} failed with exit {result.returncode}:\n"
            f"{result.stdout.decode('utf-8', errors='replace')}\n"
            f"{result.stderr.decode('utf-8', errors='replace')}"
        )
    return result


def pinned_capsule(stage: str) -> bytes:
    contents = CAPSULE.read_bytes()
    actual = sha256(contents)
    if actual != CAPSULE_SHA256:
        raise RuntimeError(f"capsule SHA mismatch at {stage}: {actual}")
    return contents


def git_state() -> tuple[str, bytes]:
    head = run(["git", "rev-parse", "HEAD"], ROOT).stdout.decode("utf-8").strip()
    status = run(["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"], ROOT).stdout
    return head, status


def audit_output(capsule: str, output: str, stderr: str) -> dict[str, list[str]]:
    if "sorryAx" in output or "sorryAx" in stderr:
        raise RuntimeError("Lean output contains sorryAx")
    if "Lean.trustCompiler" in output or "Lean.trustCompiler" in stderr:
        raise RuntimeError("Lean output contains Lean.trustCompiler")

    expected_axioms = re.findall(r"^#print axioms ([A-Za-z0-9_.]+)\s*$", capsule, re.MULTILINE)
    reports = AXIOM_REPORT.findall(output)
    if len(reports) != len(expected_axioms):
        raise RuntimeError(f"expected {len(expected_axioms)} axiom reports, got {len(reports)}")
    axioms: dict[str, list[str]] = {}
    for name, body in reports:
        if name in axioms:
            raise RuntimeError(f"duplicate axiom report for {name}")
        dependencies = [item.strip() for item in body.split(",") if item.strip()]
        unexpected = set(dependencies) - STANDARD_AXIOMS
        if unexpected:
            raise RuntimeError(f"nonstandard axioms for {name}: {sorted(unexpected)}")
        axioms[name] = dependencies
    if set(axioms) != set(expected_axioms):
        raise RuntimeError("axiom report names do not match the capsule requests")

    expected_prints = re.findall(
        r"^#print (?!axioms\b)([A-Za-z0-9_.]+)\s*$", capsule, re.MULTILINE
    )
    for name in expected_prints:
        pattern = r"^(?:def|theorem|opaque|axiom|instance)\s+" + re.escape(name) + r"(?:\s|:)"
        if not re.search(pattern, output, re.MULTILINE):
            raise RuntimeError(f"missing printed definition or theorem: {name}")
    expected_checks = re.findall(r"^#check ([A-Za-z0-9_.]+)\s*$", capsule, re.MULTILINE)
    for name in expected_checks:
        pattern = r"^" + re.escape(name) + r"(?:\.\{[^}]*\})?(?:\s|:)"
        if not re.search(pattern, output, re.MULTILINE):
            raise RuntimeError(f"missing checked declaration: {name}")
    return axioms


def main() -> int:
    try:
        with lean_task_build.build_lock(lean_task_build.LOCK):
            with lean_task_build.materialize_windows_lean_symlinks():
                head_before, status_before = git_state()
                source_before = lean_task_build.source_digest()
                verifier_before = sha256(Path(__file__).read_bytes())
                helper_path = Path(lean_task_build.__file__).resolve()
                helper_before = sha256(helper_path.read_bytes())
                capsule_bytes = pinned_capsule("before build")
                capsule_text = capsule_bytes.decode("utf-8")
                toolchain = (FORMAL / "lean-toolchain").read_text(encoding="utf-8").strip()

                build_command = ["lake", "build", *BUILD_TARGETS]
                build = run(build_command, FORMAL)
                source_after_build = lean_task_build.source_digest()
                pinned_capsule("after build")
                if source_before != source_after_build:
                    raise RuntimeError("Lean sources changed during the import build")

                version = run(["lake", "env", "lean", "--version"], FORMAL)
                query_command = ["lake", "env", "lean", str(CAPSULE)]
                query = run(query_command, FORMAL)
                source_after_query = lean_task_build.source_digest()
                pinned_capsule("after query")
                if source_after_build != source_after_query:
                    raise RuntimeError("Lean sources changed during the compatibility query")
                if sha256(Path(__file__).read_bytes()) != verifier_before:
                    raise RuntimeError("verifier changed during compatibility verification")
                if sha256(helper_path.read_bytes()) != helper_before:
                    raise RuntimeError("Lean build helper changed during compatibility verification")
                head_after, status_after = git_state()
                if head_before != head_after:
                    raise RuntimeError("Git HEAD changed during compatibility verification")

                output = query.stdout.decode("utf-8")
                stderr = query.stderr.decode("utf-8")
                axioms = audit_output(capsule_text, output, stderr)
                receipt = {
                    "schema": "d0-native-pairing-current-compatibility-v1",
                    "status": "PASS",
                    "scope": "Current Lean compatibility only; this does not validate the historical overlay or accept the scientific source-to-claim relation.",
                    "git_snapshot": head_before,
                    "worktree_dirty_before": bool(status_before),
                    "worktree_dirty_after": bool(status_after),
                    "git_status_sha256_before": sha256(status_before),
                    "git_status_sha256_after": sha256(status_after),
                    "source_digest": source_before,
                    "source_digest_before_build": source_before,
                    "source_digest_after_build": source_after_build,
                    "source_digest_after_query": source_after_query,
                    "source_digest_scope": "Repository Lean sources, Lake configuration, manifest and toolchain as defined by lean_task_build.source_digest; package checkouts are excluded.",
                    "verifier_sha256": verifier_before,
                    "lean_build_helper_sha256": helper_before,
                    "toolchain": toolchain,
                    "lean_version": version.stdout.decode("utf-8").strip(),
                    "capsule_path": CAPSULE_RELATIVE,
                    "capsule_sha256": CAPSULE_SHA256,
                    "build_command": build_command,
                    "build_exit_code": build.returncode,
                    "build_stdout_sha256": sha256(build.stdout),
                    "build_stderr_sha256": sha256(build.stderr),
                    "query_command": query_command,
                    "query_exit_code": query.returncode,
                    "lean_stdout": output,
                    "lean_stdout_sha256": sha256(query.stdout),
                    "lean_stderr": stderr,
                    "lean_stderr_sha256": sha256(query.stderr),
                    "axioms": axioms,
                    "allowed_axioms": sorted(STANDARD_AXIOMS),
                }
                sys.stdout.buffer.write((json.dumps(receipt, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
                return 0
    except lean_task_build.BuildLockBusy:
        print("FAIL D0 Lean build/cache is busy; retry after it finishes", file=sys.stderr)
        return 1
    except (OSError, RuntimeError, UnicodeDecodeError) as error:
        print(f"FAIL {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
