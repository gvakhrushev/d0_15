"""Original book inputs for twenty-seven bound historical certificate checks.

Editorial book revisions must not replace an old certificate's expected bytes.
The isolated research runner applies these inputs only to the named unchanged
checkers. A successful replay says nothing about the maintained book's new prose.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
import os
from pathlib import Path
import tempfile

from native_pairing_refinement_inputs import (
    bound_git, git_blob, linked_worktree_git_dir, read, safe_path, sha256,
)


DIRECTORY = "02_REGISTRY/research/sources/d0_book_editorial_inputs_2026-10-28"
MANIFEST = DIRECTORY + "/HISTORICAL_INPUT.json"
MANIFEST_SHA256 = "38a139466bd89dbbca02d96d867f3f36b95246e70a373f34daf7da402fac66d8"
SOURCE_COMMIT = "34dc2ddd6cf40803b95cf8afe66f9dd87f0bf22a"
CHECKER_SOURCE_COMMIT = "30ffef0f5a4353874f8966a4b69d09e534f3c47d"
SCOPE = "HISTORICAL_BOOK_INPUT_REPLAY_NOT_CURRENT_BOOK_PROOF"
CERT = "02_REGISTRY/research/certificates/"
NAMES = (
    "a4d_book03_feedback_variation",
    "a4d_native_addressed_third_role",
    "a4d_native_archive_apparatus_realization",
    "a4d_native_uniform_memory_actuation",
    "a4d_native_verified_archive_actuation",
    "a4d_native_code_price_resolution",
    "a4d_native_condensed_price_naturality",
    "a4d_native_hodge_connes_metric",
    "a4d_native_positive_heat_radial_balance",
    "a4d_native_strict_observable_descent",
    "a4d_native_modular_preparation_boundary",
    "a4d_native_af_trace_preparation",
    "a4d_native_composed_feedback_dynamics",
    "a4d_native_curved_soldered_heat",
    "a4d_native_cyclic_history_price",
    "a4d_native_cyclic_memory_minimum",
    "a4d_native_full_preparation_fiber",
    "a4d_native_golden_fixed_calibration",
    "a4d_native_golden_history_preparation",
    "a4d_native_golden_hodge_state_separation",
    "a4d_native_golden_program_compilation",
    "a4d_native_history_spectral_completion",
    "a4d_native_joint_adjoint_source",
    "a4d_native_retained_record_admission",
    "a4d_native_scene_af_metric_refinement",
    "a4d_native_scene_history_feedback",
    "a4d_native_soldered_heat_source",
)
ENTRYPOINTS = {CERT + name + "_check.py" for name in NAMES}
RECEIPTS = {
    CERT + name + ("_result.json" if index == 0 else
                   "_results.json" if index < 11 else "_certificate.json")
    for index, name in enumerate(NAMES)
}
BOOK_PATHS = {
    "01_BOOKS/BOOK_00_ENTRY_CONTRACT_AND_ADMISSIBILITY.md",
    "01_BOOKS/BOOK_01_CONDENSED_FOUNDATIONS_AND_GRAPH_BIRTH.md",
    "01_BOOKS/BOOK_02_MATHEMATICAL_PROOF_SPINE_AND_INVARIANT_CALCULUS.md",
    "01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md",
    "01_BOOKS/BOOK_06_EVOLUTION_FORGETTING_AND_TIME.md",
}
SNAPSHOTS = {
    DIRECTORY + "/BOOK_00.md",
    DIRECTORY + "/BOOK_02.md",
    "02_REGISTRY/gr_assembly/sources/d0_actionprotocol_book03_boundary_2026-10-19/BOOK_01.md",
    "02_REGISTRY/gr_assembly/sources/d0_actionprotocol_book03_boundary_2026-10-19/BOOK_03.md",
    "02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/inputs/"
    "01_BOOKS/BOOK_06_EVOLUTION_FORGETTING_AND_TIME.md",
}
SELECTION_INPUTS = ENTRYPOINTS | RECEIPTS | BOOK_PATHS | SNAPSHOTS | {
    MANIFEST, "tools/historical_book_inputs.py", "tools/run_research_certs.py",
    "tools/research_input_closure.py", "tools/native_pairing_refinement_inputs.py",
}


def validate(root: Path, entrypoint: str) -> tuple[dict, list[dict]]:
    """Validate exact recorded evidence; never infer a binding from a new checker."""
    if entrypoint not in ENTRYPOINTS:
        raise ValueError("Unregistered historical book consumer: " + entrypoint)
    raw = read(root, MANIFEST)
    if sha256(raw) != MANIFEST_SHA256:
        raise ValueError("Historical book manifest hash mismatch")
    data = json.loads(raw)
    if (data.get("schema") != "d0-book-editorial-historical-input/1"
            or data.get("scope") != SCOPE
            or data.get("book_source_commit") != SOURCE_COMMIT
            or data.get("checker_source_commit") != CHECKER_SOURCE_COMMIT
            or set(data["entrypoints"]) != ENTRYPOINTS
            or {row["path"] for row in data["books"].values()} != BOOK_PATHS
            or {row["snapshot_path"] for row in data["books"].values()} != SNAPSHOTS):
        raise ValueError("Unexpected historical book source, scope or consumer set")
    binding = data["entrypoints"][entrypoint]
    if sha256(read(root, entrypoint)) != binding["sha256"]:
        raise ValueError("Historical book checker binding mismatch: " + entrypoint)
    receipt_bytes = read(root, binding["receipt"])
    if sha256(receipt_bytes) != binding["receipt_sha256"]:
        raise ValueError("Historical book receipt binding mismatch: " + binding["receipt"])
    receipt = json.loads(receipt_bytes)
    prepared = []
    for pin in binding["book_pins"]:
        book = data["books"][pin["book"]]
        value = receipt
        for key in pin["receipt_pointer"]:
            value = value[key]
        if value != book["sha256"]:
            raise ValueError("Receipt does not pin the declared historical book")
        snapshot = read(root, book["snapshot_path"])
        if (sha256(snapshot) != book["sha256"] or git_blob(snapshot) != book["git_blob"]
                or len(snapshot) != book["bytes"] or book["source_commit"] != SOURCE_COMMIT):
            raise ValueError("Historical book snapshot hash/blob mismatch: " + book["snapshot_path"])
        maintained = read(root, book["path"])
        prepared.append({**book, "snapshot": snapshot, "maintained": maintained})
    return binding, prepared


@dataclass
class BookOverlay:
    root: Path
    inputs: list[dict]
    provenance: dict

    def restore(self) -> bool:
        """Restore only unchanged overlaid bytes; report any input mutation."""
        mutated = False
        for item in self.inputs:
            try:
                target = safe_path(self.root, item["path"])
                if target.read_bytes() != item["snapshot"]:
                    mutated = True
                    continue
                target.write_bytes(item["maintained"])
            except (OSError, ValueError):
                mutated = True
        return mutated


def apply(root: Path, entrypoint: str, *, isolation_parent: Path) -> BookOverlay | None:
    # Earlier committed revisions and unregistered consumers keep normal replay.
    if entrypoint not in ENTRYPOINTS or not (root / MANIFEST).exists():
        return None
    root = root.resolve()
    parent = isolation_parent.resolve()
    temporary_root = Path(tempfile.gettempdir()).resolve()
    if (parent.parent != temporary_root or not parent.name.startswith("d0-research-cert-")
            or root != parent / "tree" or not root.is_dir()):
        raise ValueError("Historical books require the runner's isolated worktree")
    linked_worktree_git_dir(root)
    top = bound_git(root, "rev-parse", "--show-toplevel")
    if top.returncode or Path(os.fsdecode(top.stdout).strip()).resolve() != root:
        raise ValueError("Historical book worktree root mismatch")
    branch = bound_git(root, "symbolic-ref", "-q", "HEAD")
    if branch.returncode != 1:
        raise ValueError("Historical books require detached HEAD")
    # The runner may already have applied a validated native-input overlay.
    # Its deliberate worktree dirtiness must not defeat this second overlay.
    binding, prepared = validate(root, entrypoint)
    provenance = {
        "mode": SCOPE, "entrypoint": entrypoint,
        "checker_source_commit": CHECKER_SOURCE_COMMIT,
        "checker_sha256": binding["sha256"],
        "manifest": MANIFEST, "manifest_sha256": MANIFEST_SHA256,
        "receipt_path": binding["receipt"], "receipt_sha256": binding["receipt_sha256"],
        "books": [
            {key: item[key] for key in ("path", "snapshot_path", "source_commit", "git_blob", "sha256")}
            | {"maintained_sha256": sha256(item["maintained"])}
            for item in prepared
        ],
        "current_book_prose_certified": False,
    }
    overlay = BookOverlay(root, prepared, provenance)
    written = []
    try:
        for item in prepared:
            safe_path(root, item["path"]).write_bytes(item["snapshot"])
            written.append(item)
    except OSError:
        BookOverlay(root, written, provenance).restore()
        raise
    return overlay
