"""Pinned historical sources for one pairing-refinement certificate replay.

The saved source blobs are used only inside a fresh detached research-runner
worktree. Their receipt validates the historical calculation and Lean output;
it does not validate the maintained Lean sources or make a physical claim.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import tempfile


DIRECTORY = "02_REGISTRY/research/sources/d0_native_pairing_refinement_historical_2026-10-27"
MANIFEST = DIRECTORY + "/MANIFEST.json"
MANIFEST_SHA256 = "606b4774d19e103901f19ac639484b07044157ec8e141969d6e9cf1139e69989"
SOURCE_COMMIT = "2f3360c5d3bfcb40d4791b23ade8e82e03f887c8"
BASE = "02_REGISTRY/research/certificates/a4d_native_pairing_refinement_source"
ENTRYPOINT = BASE + "_check.py"
LEDGER = BASE + "_certificate.json"
RECEIPT = BASE + "_lean_results.json"
SCOPE = "HISTORICAL_PINNED_SOURCE_CLOSURE_NOT_CURRENT_SOURCE_PROOF"
EXPECTED_SOURCES = (
    "03_FORMALIZATION/D0/Geometry/A4DPathCovariantHodge.lean",
    "03_FORMALIZATION/D0/Geometry/A4DRawSolderFrameAction.lean",
    "03_FORMALIZATION/D0/Geometry/A4DSolderMetricCompletion.lean",
    "03_FORMALIZATION/D0/Geometry/Archive1DCochainRefinement.lean",
    "03_FORMALIZATION/D0/Geometry/ArchiveCARDirac.lean",
    "03_FORMALIZATION/D0/Geometry/ArchiveCARRelations.lean",
    "03_FORMALIZATION/D0/Geometry/ArchiveCubicalCochainCarrier.lean",
    "03_FORMALIZATION/D0/Geometry/ArchiveExteriorFrameLift.lean",
    "03_FORMALIZATION/D0/Geometry/ArchiveGradedRefinementChainMap.lean",
    "03_FORMALIZATION/D0/Geometry/ArchiveMetricMeasureHodgeLift.lean",
    "03_FORMALIZATION/D0/Geometry/ArchiveRefinementHodgeWeights.lean",
)
ARTIFACT_HASHES = {
    ENTRYPOINT: "3b1d03a3357773587746e9fe556857f7f07d7a2ae09ee707103198de5c117864",
    LEDGER: "fff8606d0a48cbb043fd960ac3661ca46bc8e81fb040c60e568c0efbe9e4fe3e",
    RECEIPT: "112cd9614769d6c72081d16f9cbd041ece32b1e4b0fe7e33288968d5a7eee5d2",
    BASE + ".py": "b804b0a42aae5043efd11dc10ba96a5bf6049e7fcb4f0459ffc3366a554a5923",
    BASE + ".lean": "65d1aff45f17907fcacdcbdc6da889bc0e44b3982b1590a5254f2e8e5ad38d10",
    BASE + "_lean_output.txt": "e5713ea9be413879498983d96731db2c8441b8e83124df5a5c065d7dd0ea296f",
    "02_REGISTRY/research/A4D_NATIVE_PAIRING_REFINEMENT_SOURCE.md":
        "25b76bcb8d276dd45d32b207fa72b3a8c6aee7b5d4fba16426e3a73a71f9977a",
}
LEDGER_INPUT_COUNT = 66
RECEIPT_INPUT_COUNT = 12
SNAPSHOTS = {DIRECTORY + "/lean/" + path for path in EXPECTED_SOURCES}
SELECTION_INPUTS = set(EXPECTED_SOURCES) | SNAPSHOTS | set(ARTIFACT_HASHES) | {
    MANIFEST, "tools/native_pairing_refinement_inputs.py", "tools/run_research_certs.py",
    "tools/research_input_closure.py",
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def safe_path(root: Path, relative: str) -> Path:
    if not isinstance(relative, str) or "\\" in relative or "\0" in relative:
        raise ValueError("Unsafe historical input path")
    rel = PurePosixPath(relative)
    if rel.is_absolute() or not rel.parts or ".." in rel.parts or rel.as_posix() != relative:
        raise ValueError("Unsafe historical input path: " + relative)
    path = root
    for part in rel.parts:
        path = path / part
        if path.is_symlink():
            raise ValueError("Historical input uses a symlink: " + relative)
    if not path.resolve().is_relative_to(root.resolve()) or not path.is_file():
        raise ValueError("Historical input missing or outside isolated tree: " + relative)
    return path


def read(root: Path, relative: str) -> bytes:
    return safe_path(root, relative).read_bytes()


def clean_git_environment() -> dict[str, str]:
    """Do not inherit another checkout's repository, index or object paths."""
    env = os.environ.copy()
    for name in ("GIT_DIR", "GIT_WORK_TREE", "GIT_COMMON_DIR", "GIT_INDEX_FILE",
                 "GIT_OBJECT_DIRECTORY", "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_PREFIX",
                 "GIT_CEILING_DIRECTORIES"):
        env.pop(name, None)
    return env


def bound_git(root: Path, *args: str) -> subprocess.CompletedProcess[bytes]:
    root = root.resolve()
    return subprocess.run(["git", "-C", str(root), f"--work-tree={root}", *args],
                          env=clean_git_environment(), capture_output=True, check=False)


def linked_worktree_git_dir(root: Path) -> Path:
    """Verify the worktree gitfile and its reciprocal Git administrative link."""
    root = root.resolve()
    gitfile = root / ".git"
    if gitfile.is_symlink() or not gitfile.is_file():
        raise ValueError("Historical input requires a linked worktree")
    gitfile_text = gitfile.read_text(encoding="utf-8").strip()
    if not gitfile_text.startswith("gitdir: ") or "\n" in gitfile_text:
        raise ValueError("Invalid linked worktree gitfile")
    declared = Path(gitfile_text.removeprefix("gitdir: "))
    if not declared.is_absolute():
        declared = root / declared
    actual = bound_git(root, "rev-parse", "--absolute-git-dir")
    if actual.returncode:
        raise ValueError("Cannot resolve linked worktree Git directory")
    git_dir = Path(os.fsdecode(actual.stdout).strip()).resolve()
    if declared.resolve() != git_dir or not git_dir.is_dir():
        raise ValueError("Linked worktree Git directory mismatch")
    backlink = git_dir / "gitdir"
    if backlink.is_symlink() or not backlink.is_file():
        raise ValueError("Linked worktree Git backlink is missing")
    backlink_path = Path(backlink.read_text(encoding="utf-8").strip())
    if not backlink_path.is_absolute():
        backlink_path = git_dir / backlink_path
    if backlink_path.resolve() != gitfile.resolve():
        raise ValueError("Linked worktree Git backlink mismatch")
    return git_dir


def verify_isolated_worktree(root: Path, isolation_parent: Path | None) -> str:
    if isolation_parent is None:
        raise ValueError("Historical pairing input requires an isolated runner worktree")
    parent = isolation_parent.resolve()
    root = root.resolve()
    temporary_root = Path(tempfile.gettempdir()).resolve()
    if (parent.parent != temporary_root or not parent.name.startswith("d0-research-cert-")
            or root != parent / "tree" or not root.is_dir()):
        raise ValueError("Historical pairing input requires an isolated runner worktree")
    linked_worktree_git_dir(root)
    def git(*args: str) -> subprocess.CompletedProcess[bytes]:
        return bound_git(root, *args)
    top = git("rev-parse", "--show-toplevel")
    if top.returncode or Path(os.fsdecode(top.stdout).strip()).resolve() != root:
        raise ValueError("Historical pairing input worktree root mismatch")
    branch = git("symbolic-ref", "-q", "HEAD")
    if branch.returncode != 1:
        raise ValueError("Historical pairing input requires detached HEAD")
    status = git("status", "--porcelain=v1", "--untracked-files=all")
    if status.returncode or status.stdout:
        raise ValueError("Historical pairing input requires a clean isolated worktree")
    head = git("rev-parse", "HEAD")
    if head.returncode:
        raise ValueError("Historical pairing input cannot resolve worktree HEAD")
    return head.stdout.decode("ascii").strip()


@dataclass
class Overlay:
    entries: list[tuple[Path, bytes, bytes]]
    provenance: dict

    def restore(self) -> bool:
        """Restore unchanged overlays only; signal any mutation by the checker."""
        mutated = False
        for path, maintained, snapshot in reversed(self.entries):
            if path.is_symlink() or not path.is_file() or path.read_bytes() != snapshot:
                mutated = True
            else:
                path.write_bytes(maintained)
        return mutated


def apply(root: Path, entrypoint: str, *, isolation_parent: Path | None = None) -> Overlay | None:
    if entrypoint != ENTRYPOINT:
        return None
    root = root.resolve()
    head = verify_isolated_worktree(root, isolation_parent)
    # A previously published snapshot predating this binding keeps its own
    # ordinary replay. Once this helper is tracked, the manifest is mandatory.
    manifest_path = root / MANIFEST
    if not manifest_path.exists():
        tracked = bound_git(root, "cat-file", "-e", "HEAD:tools/native_pairing_refinement_inputs.py")
        if tracked.returncode == 0:
            raise ValueError("Historical pairing manifest is missing")
        return None
    manifest_bytes = read(root, MANIFEST)
    if sha256(manifest_bytes) != MANIFEST_SHA256:
        raise ValueError("Historical pairing manifest hash mismatch")
    manifest = json.loads(manifest_bytes)
    required = {
        "schema": "d0-pairing-refinement-historical-input/1", "scope": SCOPE,
        "source_commit": SOURCE_COMMIT, "entrypoint": ENTRYPOINT,
        "ledger_path": LEDGER, "lean_receipt_path": RECEIPT,
        "artifact_sha256": ARTIFACT_HASHES,
    }
    if set(manifest) != set(required) | {"sources"} or any(manifest.get(k) != v for k, v in required.items()):
        raise ValueError("Historical pairing manifest scope or artifact binding mismatch")
    for path, expected in ARTIFACT_HASHES.items():
        if sha256(read(root, path)) != expected:
            raise ValueError("Historical pairing artifact binding mismatch: " + path)
    ledger = json.loads(read(root, LEDGER))
    receipt = json.loads(read(root, RECEIPT))
    if (ledger.get("schema") != "d0-native-pairing-refinement-source/1"
            or ledger.get("input_source_sha") != SOURCE_COMMIT
            or receipt.get("source_commit") != SOURCE_COMMIT
            or receipt.get("status") != "PASS" or receipt.get("compiler_exit_code") != 0):
        raise ValueError("Historical pairing ledger or Lean receipt scope mismatch")
    bindings = {
        "checker_sha256": ENTRYPOINT, "program_sha256": BASE + ".py",
        "proof_sha256": "02_REGISTRY/research/A4D_NATIVE_PAIRING_REFINEMENT_SOURCE.md",
        "Lean_capsule_sha256": BASE + ".lean", "Lean_output_sha256": BASE + "_lean_output.txt",
        "Lean_receipt_sha256": RECEIPT,
    }
    if any(ledger.get(field) != ARTIFACT_HASHES[path] for field, path in bindings.items()):
        raise ValueError("Historical pairing ledger artifact fingerprint mismatch")
    inputs = ledger.get("input_sha256")
    receipt_inputs = receipt.get("input_sha256")
    if (not isinstance(inputs, dict) or len(inputs) != LEDGER_INPUT_COUNT
            or not isinstance(receipt_inputs, dict) or len(receipt_inputs) != RECEIPT_INPUT_COUNT
            or any(inputs.get(path) != digest for path, digest in receipt_inputs.items())):
        raise ValueError("Historical pairing input closure or Lean receipt mismatch")
    if any(not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value)
           for value in inputs.values()):
        raise ValueError("Historical pairing input SHA-256 malformed")
    sources = manifest.get("sources")
    if not isinstance(sources, list) or len(sources) != len(EXPECTED_SOURCES):
        raise ValueError("Historical pairing source set mismatch")
    if any(not isinstance(item, dict) or set(item) != {"source_path", "snapshot_path", "git_blob", "sha256"}
           for item in sources):
        raise ValueError("Historical pairing source entry malformed")
    if {item["source_path"] for item in sources} != set(EXPECTED_SOURCES):
        raise ValueError("Historical pairing source set mismatch")
    snapshots: dict[str, tuple[bytes, dict]] = {}
    for item in sources:
        path = item["source_path"]
        expected_snapshot = DIRECTORY + "/lean/" + path
        if item["snapshot_path"] != expected_snapshot or inputs.get(path) != item["sha256"]:
            raise ValueError("Historical pairing source/ledger binding mismatch: " + str(path))
        data = read(root, expected_snapshot)
        if sha256(data) != item["sha256"] or git_blob(data) != item["git_blob"]:
            raise ValueError("Historical pairing source blob mismatch: " + str(path))
        snapshots[path] = (data, item)
    if set(snapshots) != set(EXPECTED_SOURCES):
        raise ValueError("Historical pairing source set mismatch")

    # Validate the entire immutable ledger before changing any file. Only the
    # eleven explicit Lean sources are eligible for a historical overlay.
    entries: list[tuple[Path, bytes, bytes]] = []
    details = []
    for path, digest in sorted(inputs.items()):
        current_path = safe_path(root, path)
        maintained = current_path.read_bytes()
        current_sha = sha256(maintained)
        if path in snapshots:
            data, item = snapshots[path]
            if current_sha != digest:
                entries.append((current_path, maintained, data))
            details.append({"target_path": path, "snapshot_path": item["snapshot_path"],
                            "git_blob": item["git_blob"], "historical_sha256": digest,
                            "maintained_sha256": current_sha, "overlaid": current_sha != digest})
        elif current_sha != digest:
            raise ValueError("Historical pairing unbound input mismatch: " + path)
    if not set(EXPECTED_SOURCES) <= set(inputs):
        raise ValueError("Historical pairing source absent from immutable ledger")
    provenance = {
        "mode": SCOPE, "entrypoint": ENTRYPOINT, "target_path": LEDGER,
        "source_head": SOURCE_COMMIT, "replay_head": head,
        "historical_sha256": ARTIFACT_HASHES[LEDGER], "manifest": MANIFEST,
        "manifest_sha256": MANIFEST_SHA256, "ledger_input_count": len(inputs),
        "lean_receipt_input_count": len(receipt_inputs), "overlaid_source_count": len(entries),
        "sources": details,
        "current_source_compilation": "SEPARATE_REQUIRED_LEAN_COMPATIBILITY_CHECK",
    }
    applied: list[tuple[Path, bytes, bytes]] = []
    try:
        for target, maintained, snapshot in entries:
            target.write_bytes(snapshot)
            applied.append((target, maintained, snapshot))
    except Exception:
        Overlay(applied, provenance).restore()
        raise
    return Overlay(entries, provenance)
